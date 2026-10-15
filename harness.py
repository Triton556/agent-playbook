#!/usr/bin/env python3
"""Install the intact workflow payload. Python standard library only."""
from __future__ import annotations
import argparse,hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path

REPO=Path(__file__).resolve().parent
CLIENT_ROOT={'codex':'.agents','claude':'.claude','deepseek':'.dsh','generic':'.agent-harness'}
BEGIN='\n<!-- agent-workflow-harness:begin -->\n'
END='\n<!-- agent-workflow-harness:end -->\n'
class HarnessError(Exception):pass
def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def read_json(p:Path):return json.loads(p.read_text(encoding='utf-8-sig'))
def write_json(p:Path,obj):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def linksafe(path:Path):
    p=path.absolute()
    for part in [p,*p.parents]:
        if part.is_symlink() or (hasattr(part,'is_junction') and part.is_junction()):raise HarnessError('Symlink/junction not allowed: '+str(part))
    return p.resolve()
def safe(base:Path,rel:str):
    p=linksafe(base/rel)
    try:p.relative_to(base.absolute())
    except ValueError:raise HarnessError('Path escapes selected target: '+rel)
    if '..' in Path(rel).parts or Path(rel).is_absolute():raise HarnessError('Unsafe relative path: '+rel)
    return p
def trust_record(target,client):
    # Separate from destination-project data. Do not infer ownership from a forged project receipt.
    store=linksafe(REPO/'.harness-state/receipts')
    identity=sha((str(target)+'\n'+client).encode('utf8'))
    return safe(store,identity+'.json')
def manifest():
    m=read_json(REPO/'manifest.json')
    if m.get('schema_version')!=1:raise HarnessError('Unsupported manifest schema')
    for f in m['files']:
        p=safe(REPO,f['path'])
        if not p.is_file() or sha(p.read_bytes())!=f['sha256']:raise HarnessError('Payload integrity failed: '+f['path'])
    return m
def catalog(m):
    c={}
    for f in m['files']:
        if f['path'].startswith('payload/skills/') and f['path'].endswith('/SKILL.md') and len(f['path'].split('/'))==4:
            text=(REPO/f['path']).read_text(encoding='utf-8-sig')
            head=text.split('---',2)[1]
            name=re.search(r'^name:\s*["\']?([^\n"\']+)',head,re.M).group(1).strip()
            description=re.search(r'^description:\s*(.+)',head,re.M).group(1).strip().strip('"\'')
            c[name]={'name':name,'description':description,'dependencies':set()}
    # All sibling skill references are retained. Cycles mean closure, not a new dispatcher.
    for f in m['files']:
        owner=f['module']
        if owner not in c or Path(f['path']).suffix.lower() not in ['.md','.py','.mjs','.ps1']:continue
        text=(REPO/f['path']).read_text(encoding='utf-8-sig')
        for other in c:
            named=re.search(r'(?<![\w-])'+re.escape(other)+r'(?![\w-])',text) if '-' in other else re.search(r'[`\"\[]'+re.escape(other)+r'[`\"\]]',text)
            if other!=owner and (named or f'/skills/{other}/' in text or re.search(r'\.\./(?:\.\./)?'+re.escape(other)+r'/',text)):
                c[owner]['dependencies'].add(other)
    # Local workflow creators actually depend on the native structure creator, disclosed separately.
    return c
def selection(args,m,c):
    profiles={'full':set(c),'engineering':{x for x in c if x.startswith('product-')}|{'ui-ux-pro-max','writing-for-agents','domain-modeling'},'visual':{'product-ui-design','product-ui-review','visual-experiment-craft','voxel-model-craft'},'voxel':{'voxel-model-craft'},'memory':{x for x in c if x.startswith('kb-')},'instructions':{'writing-for-agents','anthropic-workflow-creator'}}
    chosen=set()
    if args.profile:chosen|=profiles[args.profile]
    for v in args.skills or []:chosen|={x for x in v.split(',') if x}
    if not chosen:raise HarnessError('Select --profile or --skills; nothing is installed implicitly')
    missing=chosen-set(c)
    if missing:raise HarnessError('Unknown skill: '+','.join(sorted(missing)))
    requested=set(chosen)
    if args.workflow:chosen=set(c)
    while True:
        expanded=chosen|set().union(*(c[x]['dependencies'] for x in chosen))
        if expanded==chosen:break
        chosen=expanded
    return requested,chosen
def settings(args,root,target):
    memory=str(Path(args.memory_root).absolute().as_posix()) if args.memory_root else str((target/'.harness-memory').as_posix())
    return {'HARNESS_ROOT':root.as_posix(),'MEMORY_ROOT':memory,'MEMORY_REPO':args.memory_repo or '[configure own verified private memory repository]','CLOUD_MEMORY_ROOT':args.cloud_memory_root or '[configure authorized cloud copy path]','CURATION_SCHEDULE':args.curation_schedule or '[configure daily time, timezone and actual scheduler receipt]','EVIDENCE_ROOT':str(Path(args.evidence_root).absolute().as_posix()) if args.evidence_root else str((target/'optional-evidence').as_posix()),'PYTHON':Path(sys.executable).as_posix(),'NODE':Path(shutil.which('node') or 'node').as_posix(),'LAB_CLI':args.lab_cli or '[configure authorized lab CLI]','LAB_RUNTIME':args.lab_runtime or '[configure authorized lab runtime]','LAB_VM_NAME':args.lab_vm_name or '[configure exact VM name]','LAB_VM_UUID':args.lab_vm_uuid or '[configure exact VM UUID]','LAB_VM_MAC':args.lab_vm_mac or '[configure exact VM MAC]','HISTORICAL_SOURCE_ROOT':str((target/'optional-evidence/historical-source').as_posix())}
def render(data,values,path):
    try:text=data.decode('utf-8-sig')
    except UnicodeDecodeError:return data
    for key,value in values.items():
        marker='{{'+key+'}}'
        if marker in text:
            # Only documents use file-system binding substitution. Runtime code uses env/relative imports.
            if Path(path).suffix.lower() in ['.js','.mjs','.py','.ps1','.cmd']:
                raise HarnessError('Unported executable binding: '+path+' '+marker)
            text=text.replace(marker,value)
    if re.search(r'\{\{[A-Z_]+\}\}',text):raise HarnessError('Unresolved binding: '+path)
    return text.encode('utf8') if text!=data.decode('utf-8-sig') else data
def strip_block(text):
    if BEGIN not in text and END not in text:return text,None
    if text.count(BEGIN)!=1 or text.count(END)!=1:raise HarnessError('Malformed existing managed instructions block')
    first=text.index(BEGIN);last=text.index(END)+len(END)
    if last<first:raise HarnessError('Malformed managed block order')
    return text[:first]+text[last:],text[first:last]
def instruction_diagnostics(target,prospective=None,declared_budget=32768):
    override=target/'AGENTS.override.md';files=[]
    root=next((p for p in [target,*target.parents] if (p/'.git').exists()),target)
    chain=[];p=target
    while True:
        chain.append(p)
        if p==root:break
        p=p.parent
    for folder in reversed(chain):
        preferred=folder/'AGENTS.override.md';candidate=preferred if preferred.is_file() else folder/'AGENTS.md'
        if folder==target and prospective is not None and not preferred.is_file():size=len(prospective.encode('utf8'))
        elif candidate.is_file():size=candidate.stat().st_size
        else:continue
        files.append({'path':str(candidate),'bytes':size})
    size=sum(x['bytes'] for x in files)
    return {'status':'fail' if override.is_file() or size>declared_budget else 'project-files-within-declared-budget','project_bytes':size,'declared_budget':declared_budget,'override_shadows_installation':override.is_file(),'files':files,'limits':'Declared limit only. Effective client settings, global instructions, fallback files and future nested overrides require actual session verification.'}
def instructions_block(version,root,values,full):
    header=f"\nInstalled workflow harness {version}. Read policy `{root.as_posix()}/harness-policy.json` first. Historical permissions in installed skills apply only when backed by this installation owner's actual authorization; policy files do not grant tool access. Native capabilities must be checked before use.\n\n"
    if full:
        body=render((REPO/'payload/AGENTS.md').read_bytes(),values,'BASE-RULES.md').decode('utf-8-sig')
        return BEGIN+header+body+'\n'+END
    return BEGIN+header+'Selected skills only; the complete global workflow is not activated. Read the applicable installed skill and its references when the task calls for it.\n'+END
def plan(args):
    m=manifest();c=catalog(m);requested,chosen=selection(args,m,c)
    target=linksafe(Path(args.target).absolute());root=safe(target,CLIENT_ROOT[args.client])
    values=settings(args,root,target);entries=[]
    for f in m['files']:
        rel=f['path'].removeprefix('payload/')
        if rel=='AGENTS.md':rel='BASE-RULES.md'
        selected=(f['module'] in chosen or f['module']=='workflow' or (f['module']=='memory-runtime' and any(x.startswith('kb-') for x in chosen)))
        if not selected:continue
        data=render((REPO/f['path']).read_bytes(),values,rel)
        entries.append({'relative':CLIENT_ROOT[args.client]+'/'+rel,'sha256':sha(data),'data':data,'source':f['path']})
    activate=args.workflow or args.profile=='full'
    policy={'reviewer_consent':args.reviewer_consent,'consent_source':args.consent_source or None,'requires_actual_user_authorization':True,'capability_declarations':{},'source_version':m['version'],'scope':'project','client':args.client,'full_workflow':activate,'bindings':values,'requested_skills':sorted(requested),'installed_skills':sorted(chosen)}
    if policy['reviewer_consent']=='one-per-round' and not args.consent_source:raise HarnessError('Standing reviewer consent needs --consent-source pointing to actual human authorization')
    policy['project_doc_max_bytes_declared']=args.project_doc_max_bytes
    policy_bytes=(json.dumps(policy,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    entries.append({'relative':CLIENT_ROOT[args.client]+'/harness-policy.json','sha256':sha(policy_bytes),'data':policy_bytes,'source':'generated-policy'})
    instruction_file='CLAUDE.md' if args.client=='claude' else 'AGENTS.md'
    block=instructions_block(m['version'],root,values,activate)
    return m,target,root,entries,block,instruction_file,policy
def install(args):
    m,target,root,entries,block,instruction_file,policy=plan(args)
    receipt_path=safe(root,'harness-install.json')
    old=read_json(receipt_path) if receipt_path.is_file() else None
    trusted=trust_record(target,args.client)
    if old and (not trusted.is_file() or trusted.read_bytes()!=receipt_path.read_bytes()):raise HarnessError('Project receipt differs from the installer private record; preserve files for inspection')
    if trusted.exists() and old is None:raise HarnessError('Original installation record exists but project receipt is missing; preserve files for inspection')
    oldfiles={x['relative']:x for x in (old or {}).get('files',[])}
    # All conflicts detected before any destination write, including existing user-managed files.
    for e in entries:
        p=safe(target,e['relative'])
        e['owned']=oldfiles.get(e['relative'],{}).get('owned',False) if p.exists() else True
        if p.exists() and (not p.is_file() or sha(p.read_bytes())!=e['sha256']):
            raise HarnessError('Existing file differs; preserved, install refused: '+e['relative'])
    ip=safe(target,instruction_file);original=ip.read_bytes().decode('utf8') if ip.is_file() else ''
    if ip.exists() and not ip.is_file():raise HarnessError('Instructions target is not a file')
    base,existing=strip_block(original)
    if args.client=='codex':
        diagnostic=instruction_diagnostics(target,original if existing else original+block,args.project_doc_max_bytes)
        if diagnostic['override_shadows_installation']:raise HarnessError('AGENTS.override.md shadows the startup block; preserve it and resolve the instruction-source choice before installation')
        if diagnostic['status']=='fail':raise HarnessError('Project startup instructions exceed declared Codex byte budget ('+str(diagnostic['project_bytes'])+' > '+str(args.project_doc_max_bytes)+'). Use an explicit larger --project-doc-max-bytes and matching session launch configuration; instructions were not shortened or written.')
    if block and existing is not None and existing!=block:raise HarnessError('Existing managed instructions differ; preserved')
    if old and (old['client']!=args.client or old['installed_skills']!=policy['installed_skills']):raise HarnessError('Existing installation has another selection; remove safely or use a different target')
    if args.dry_run:return {'status':'planned','target':str(target),'client':args.client,'requested_skills':policy['requested_skills'],'installed_skills':policy['installed_skills'],'files':len(entries),'workflow_activated':policy['full_workflow'],'writes':0}
    trusted.parent.mkdir(parents=True,exist_ok=True)
    for e in entries:
        p=safe(target,e['relative']);p.parent.mkdir(parents=True,exist_ok=True)
        if not p.exists():p.write_bytes(e['data'])
    written_instructions=False
    if block and existing is None:
        ip.parent.mkdir(parents=True,exist_ok=True)
        ip.write_bytes((original+block).encode('utf8'));written_instructions=True
    receipt={'schema_version':1,'version':m['version'],'client':args.client,'requested_skills':policy['requested_skills'],'installed_skills':policy['installed_skills'],'workflow_activated':policy['full_workflow'],'instruction_file':instruction_file,'managed_block_sha256':sha(block.encode('utf8')),'managed_block_owned':old.get('managed_block_owned',False) if old else written_instructions,'instruction_preexisting':old.get('instruction_preexisting') if old else ip.is_file() and bool(original),'files':[{k:e[k] for k in ['relative','sha256','source','owned']} for e in entries]}
    receipt['policy_snapshot']=policy
    write_json(receipt_path,receipt)
    write_json(trusted,receipt)
    return {'status':'installed','target':str(target),'files':len(entries),'installed_skills':policy['installed_skills'],'workflow_activated':policy['full_workflow'],'instructions_changed':written_instructions,'note':'File installation is not a claim of tool readiness or model-output equivalence; run doctor and live acceptance.'}
def installed(args):
    target=linksafe(Path(args.target).absolute());root=safe(target,CLIENT_ROOT[args.client]);p=safe(root,'harness-install.json')
    if not p.is_file():raise HarnessError('No harness installation receipt for selected target/client')
    receipt=read_json(p)
    trusted=trust_record(target,args.client)
    if not trusted.is_file() or trusted.read_bytes()!=p.read_bytes():raise HarnessError('Project receipt does not match the installer private ownership record; preserve files for inspection')
    if receipt.get('schema_version')!=1 or receipt.get('client')!=args.client:raise HarnessError('Invalid installation receipt')
    # A receipt is project data, not authority to delete neighboring files.
    m=manifest(); sources={f['path']:f for f in m['files']};c=catalog(m)
    policy=read_json(root/'harness-policy.json')
    if receipt.get('policy_snapshot')!=policy:raise HarnessError('Deployment policy differs from original receipt snapshot; preserve files for inspection')
    expected_policy_bytes=(json.dumps(receipt['policy_snapshot'],ensure_ascii=False,indent=2)+'\n').encode('utf8')
    expected_sources={f['path'] for f in m['files'] if f['module'] in set(policy.get('installed_skills',[])) or f['module']=='workflow' or (f['module']=='memory-runtime' and any(x.startswith('kb-') for x in policy.get('installed_skills',[])))}|{'generated-policy'}
    if len(receipt.get('files',[]))!=len(expected_sources) or {f.get('source') for f in receipt.get('files',[])}!=expected_sources:raise HarnessError('Installation receipt omits or adds expected files')
    if policy.get('installed_skills')!=receipt.get('installed_skills') or policy.get('client')!=args.client:raise HarnessError('Receipt/policy selection mismatch')
    chosen=set(policy['installed_skills'])
    if not chosen or not chosen<=set(c):raise HarnessError('Invalid installed module selection')
    if policy.get('bindings',{}).get('HARNESS_ROOT')!=root.as_posix():raise HarnessError('Invalid installation root binding')
    if receipt.get('workflow_activated')!=policy.get('full_workflow'):raise HarnessError('Receipt/policy activation mismatch')
    expected_block=instructions_block(m['version'],root,policy['bindings'],policy['full_workflow'])
    if receipt.get('managed_block_sha256')!=sha(expected_block.encode('utf8')):raise HarnessError('Receipt instruction hash does not match packaged instructions')
    expected_entry='CLAUDE.md' if args.client=='claude' else 'AGENTS.md'
    if receipt.get('instruction_file') not in [None,expected_entry]:raise HarnessError('Invalid instruction path in receipt')
    seen=set()
    for row in receipt.get('files',[]):
        source=row.get('source')
        if source=='generated-policy':relative=CLIENT_ROOT[args.client]+'/harness-policy.json'
        elif source in sources:
            f=sources[source]
            allowed=f['module'] in chosen or f['module']=='workflow' or (f['module']=='memory-runtime' and any(x.startswith('kb-') for x in chosen))
            if not allowed:raise HarnessError('Receipt includes an unselected module')
            rel=source.removeprefix('payload/')
            if rel=='AGENTS.md':rel='BASE-RULES.md'
            relative=CLIENT_ROOT[args.client]+'/'+rel
        else:raise HarnessError('Unknown source in installation receipt')
        if row.get('relative')!=relative or relative in seen:raise HarnessError('Invalid file path in installation receipt')
        if not re.fullmatch('[0-9a-f]{64}',row.get('sha256','')):raise HarnessError('Invalid file hash in installation receipt')
        if not isinstance(row.get('owned'),bool):raise HarnessError('Missing ownership record; preserve this installation for manual inspection')
        if source!='generated-policy' and row['sha256']!=sha(render((REPO/source).read_bytes(),policy['bindings'],rel)):raise HarnessError('Receipt hash does not match packaged source')
        if source=='generated-policy' and row['sha256']!=sha(expected_policy_bytes):raise HarnessError('Receipt policy hash differs from installation snapshot')
        seen.add(relative)
    return target,root,receipt
def verify(args):
    target,root,receipt=installed(args);fail=[]
    for f in receipt['files']:
        p=safe(target,f['relative'])
        if not p.is_file() or sha(p.read_bytes())!=f['sha256']:fail.append(f['relative'])
    if receipt.get('managed_block_sha256'):
        p=safe(target,receipt['instruction_file'])
        if not p.is_file():fail.append(receipt['instruction_file'])
        else:
            _,b=strip_block(p.read_bytes().decode('utf8'))
            if b is None or sha(b.encode('utf8'))!=receipt['managed_block_sha256']:fail.append('managed-instructions-block')
    return {'status':'pass' if not fail else 'fail','checked_files':len(receipt['files']),'failures':fail,'limits':'Integrity only; this does not prove human perception, runtime capabilities or model parity.'}
def doctor(args):
    v=verify(args);target,root,r=installed(args);policy=read_json(root/'harness-policy.json')
    checks=[{'capability':'integrity','status':v['status']},{'capability':'python','status':'pass','version':sys.version.split()[0]},{'capability':'node','status':'pass' if shutil.which('node') else 'missing'}, {'capability':'file-reading-and-shell','status':'unverified','check':'Agent must read installed instructions and execute a permitted helper.'},{'capability':'fresh-independent-reviewer','status':'unverified','consent':policy['reviewer_consent'],'check':'Verify actual fresh context support and owner authorization; installation files do not grant it.'}]
    selected=set(r['installed_skills'])
    if args.client=='codex':checks.append({'capability':'startup-instructions','client_load':'unverified',**instruction_diagnostics(target,declared_budget=policy.get('project_doc_max_bytes_declared',32768))})
    if selected&{'product-ui-design','product-ui-review','visual-experiment-craft','voxel-model-craft'}:
        checks.append({'capability':'actual-image-and-browser-inspection','status':'unverified','check':'Inspect the actual output and interaction in the client, not just a file list.'})
    if 'product-ui-review' in selected:
        binary=root/'skills/product-ui-review/vendor/impeccable/scripts/bin/windows-x64/impeccable.exe'
        checks.append({'capability':'impeccable-engine-0.1.14','status':'pass' if binary.is_file() and sha(binary.read_bytes())=='38e09451694973ba664a24e67e1502a6913e6d0e533a0a5ae1e04c5963a804b1' else 'missing','check':'Pinned runtime asset; acquire separately or disclose missing automatic detector.'})
    if any(x.startswith('kb-') for x in selected):
        vault=Path(policy['bindings']['MEMORY_ROOT']);checks.append({'capability':'authorized-knowledge-vault','status':'configured' if (vault/'SYSTEM/connection.json').is_file() else 'missing','check':'Initialize an empty personal vault or configure your existing authorized one; do not copy another owner data.'})
    if 'lab-vm-control' in selected:checks.append({'capability':'authorized-fixed-lab-provider','status':'unverified','check':'Supply own exact target inventory and restricted CLI/MCP; no VM/session is provisioned by this installer.'})
    return {'status':'integrity-verified-runtime-unverified' if v['status']=='pass' else 'fail','checks':checks,'quality_parity':'not-established','instruction_integrity':v['status'],'limits':'Capability declarations and file presence are not executed client validation.'}
def remove(args):
    target,root,r=installed(args);conflicts=[]
    for f in r['files']:
        p=safe(target,f['relative'])
        if p.exists() and (not p.is_file() or sha(p.read_bytes())!=f['sha256']):conflicts.append(f['relative'])
    ip=safe(target,r['instruction_file']) if r['instruction_file'] else None
    if ip and ip.is_file():
        base,b=strip_block(ip.read_bytes().decode('utf8'))
        if b is None or sha(b.encode('utf8'))!=r['managed_block_sha256']:conflicts.append('managed-instructions-block')
    if conflicts:raise HarnessError('Modified files preserved; removal refused: '+', '.join(conflicts))
    if args.dry_run:return {'status':'removal-planned','files':len(r['files']),'writes':0}
    for f in r['files']:
        p=safe(target,f['relative'])
        if p.is_file() and f.get('owned',False):p.unlink()
    if ip and ip.is_file() and r.get('managed_block_owned',False):
        base,b=strip_block(ip.read_bytes().decode('utf8'))
        if base.strip() or r['instruction_preexisting']:ip.write_bytes(base.encode('utf8'))
        else:ip.unlink()
    safe(root,'harness-install.json').unlink()
    trust_record(target,args.client).unlink()
    return {'status':'removed','preserved':'Unmanaged files/directories and memory data; no recursive deletion.'}
def init_memory(args):
    target,root,r=installed(args);policy=read_json(root/'harness-policy.json')
    if not any(x.startswith('kb-') for x in r['installed_skills']):raise HarnessError('Install the memory profile first')
    vault=linksafe(Path(policy['bindings']['MEMORY_ROOT']))
    entries=[]
    for source in sorted((root/'runtime/memory/SYSTEM').rglob('*')):
        if source.is_file():entries.append((source.relative_to(root/'runtime/memory').as_posix(),source.read_bytes()))
    connection={'schema_version':1,'url':None,'branch':'main','private_verified_at':None,'note':'Local empty vault. A real private remote must be separately configured and verified before sync.'}
    entries.extend([('SYSTEM/connection.json',(json.dumps(connection,indent=2)+'\n').encode('utf8')),('INDEX.md',b'# Knowledge index\n\nNo personal records have been imported.\n')])
    for rel,data in entries:
        p=safe(vault,rel)
        if p.exists() and (not p.is_file() or p.read_bytes()!=data):raise HarnessError('Existing vault file preserved; initialization refused: '+rel)
    for folder in ['INBOX','PERSONAL','AREAS','PROJECTS','IDEAS','HYPOTHESES','ARCHIVE','SYSTEM']:safe(vault,folder).mkdir(parents=True,exist_ok=True)
    for rel,data in entries:
        p=safe(vault,rel);p.parent.mkdir(parents=True,exist_ok=True)
        if not p.exists():p.write_bytes(data)
    return {'status':'local-vault-initialized','root':str(vault),'remote_sync':'not-configured','scheduler':'not-activated','data_imported':False}
def main(argv=None):
    if sys.version_info<(3,12):
        print(json.dumps({'status':'error','message':'Python 3.12+ required (including Windows junction checks)'}),file=sys.stderr);return 2
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    sub.add_parser('catalog');sub.add_parser('check-package')
    for command in ['plan','install','verify','doctor','remove','init-memory']:
        p=sub.add_parser(command);p.add_argument('--target',required=True);p.add_argument('--client',choices=CLIENT_ROOT,default='codex')
        if command in ['plan','install']:
            p.add_argument('--profile',choices=['full','engineering','visual','voxel','memory','instructions']);p.add_argument('--skills',action='append');p.add_argument('--workflow',action='store_true');p.add_argument('--memory-root');p.add_argument('--reviewer-consent',choices=['ask','one-per-round'],default='ask');p.add_argument('--consent-source')
            p.add_argument('--project-doc-max-bytes',type=int,default=32768,help='Declared Codex project instruction budget; does not change client config. Match actual session settings.')
            for name in ['evidence-root','memory-repo','cloud-memory-root','curation-schedule']:p.add_argument('--'+name)
            for name in ['lab-cli','lab-runtime','lab-vm-name','lab-vm-uuid','lab-vm-mac']:p.add_argument('--'+name)
        if command in ['plan','install','remove']:p.add_argument('--dry-run',action='store_true')
    args=ap.parse_args(argv)
    try:
        if args.command=='catalog':
            m=manifest();result={'version':m['version'],'skills':[{**v,'dependencies':sorted(v['dependencies'])} for v in catalog(m).values()]}
        elif args.command=='check-package':m=manifest();result={'status':'pass','payload_files':len(m['files']),'limits':'Hashes do not prove behavior or quality.'}
        elif args.command=='plan':args.dry_run=True;result=install(args)
        else:result=globals()[args.command.replace('-','_')](args)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 1 if result.get('status')=='fail' else 0
    except (HarnessError,ValueError,OSError,KeyError,TypeError) as e:
        print(json.dumps({'status':'error','message':str(e)},ensure_ascii=False),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
