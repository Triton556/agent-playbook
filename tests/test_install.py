import hashlib,json,os,subprocess,sys,tempfile,unittest,shutil,uuid
from contextlib import contextmanager
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEMP_ROOT=ROOT/'tests/.tmp'
TEMP_ROOT.mkdir(exist_ok=True)
def payload_bytes(relative,target,client='codex'):
    # Source prose uses the declared relocation binding; compare the complete
    # expected body after that documented substitution, without a summary.
    native={'codex':'.agents','claude':'.claude','deepseek':'.dsh','generic':'.agent-harness'}[client]
    return (ROOT/relative).read_bytes().replace(
        b'{{HARNESS_ROOT}}',(Path(target).resolve()/native).as_posix().encode('utf8')).replace(b'{{MEMORY_ROOT}}',(Path(target).resolve()/'.harness-memory').as_posix().encode('utf8'))
@contextmanager
def target_directory():
    # Use ordinary inherited workspace permissions for synthetic test artifacts.
    # tempfile's Windows 0700 directory ACL is unreadable to some restricted tokens.
    folder=(TEMP_ROOT/('case-'+uuid.uuid4().hex)).resolve();folder.mkdir()
    folder.relative_to(TEMP_ROOT.resolve())
    try:yield str(folder)
    finally:
        # Verify the final absolute delete target stays inside the named test workspace.
        folder.resolve().relative_to(TEMP_ROOT.resolve())
        if folder.is_symlink():raise AssertionError('Unexpected symbolic test root')
        shutil.rmtree(folder)
def call(*args,ok=0):
    p=subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/'harness.py'),*map(str,args)],capture_output=True,cwd=ROOT)
    stdout=p.stdout.decode('utf8',errors='replace');stderr=p.stderr.decode('utf8',errors='replace')
    if p.returncode!=ok:raise AssertionError((p.returncode,stdout,stderr))
    return json.loads(stdout or stderr)
class InstallBehavior(unittest.TestCase):
    def test_complete_roundtrip_preserves_utf8_bom_crlf_and_user_changes(self):
        with target_directory() as td:
            p=Path(td);old=b'\xef\xbb\xbf# Project\r\nKeep my instructions.';(p/'AGENTS.md').write_bytes(old)
            call('install','--profile','full','--target',p)
            self.assertEqual(call('verify','--target',p)['status'],'pass')
            self.assertTrue((p/'AGENTS.md').read_bytes().startswith(old))
            first=(p/'AGENTS.md').read_bytes();call('install','--profile','full','--target',p)
            self.assertEqual(first,(p/'AGENTS.md').read_bytes())
            # An unrelated edit after installation is retained; only exact managed content is owned.
            (p/'AGENTS.md').write_bytes(first+b'\nNew user rule.\r\n')
            call('remove','--target',p)
            self.assertEqual((p/'AGENTS.md').read_bytes(),old+b'\nNew user rule.\r\n')
    def test_existing_identical_skill_is_not_deleted(self):
        with target_directory() as td:
            p=Path(td);dest=p/'.agents/skills/kb-find/SKILL.md';dest.parent.mkdir(parents=True)
            data=payload_bytes('payload/skills/kb-find/SKILL.md',p);dest.write_bytes(data)
            call('install','--skills','kb-find','--target',p)
            call('remove','--target',p)
            self.assertEqual(dest.read_bytes(),data)
    def test_conflict_is_detected_before_other_writes(self):
        with target_directory() as td:
            p=Path(td);dest=p/'.agents/skills/voxel-models/SKILL.md';dest.parent.mkdir(parents=True);dest.write_text('My different skill')
            before=sorted(str(x.relative_to(p)) for x in p.rglob('*'))
            call('install','--skills','voxel-models','--target',p,ok=2)
            self.assertEqual(before,sorted(str(x.relative_to(p)) for x in p.rglob('*')))
            self.assertEqual(dest.read_text(),'My different skill')
    def test_changed_owned_file_blocks_remove_and_is_retained(self):
        with target_directory() as td:
            p=Path(td);call('install','--skills','kb-find','--target',p)
            changed=p/'.agents/skills/kb-find/SKILL.md';changed.write_text('My edit')
            self.assertEqual(call('verify','--target',p,ok=1)['status'],'fail')
            call('remove','--target',p,ok=2);self.assertEqual(changed.read_text(),'My edit')
    def test_native_layouts_have_same_complete_skill_body(self):
        for client,folder,entry in [('codex','.agents','AGENTS.md'),('claude','.claude','CLAUDE.md'),('deepseek','.dsh','AGENTS.md'),('generic','.agent-harness','AGENTS.md')]:
            with self.subTest(client=client),target_directory() as td:
                p=Path(td);result=call('install','--skills','kb-find','--workflow','--client',client,'--target',p)
                self.assertTrue(result['workflow_activated']);self.assertTrue((p/entry).is_file())
                self.assertEqual(len(result['installed_skills']),7)
                self.assertIn('you-are-brain',result['installed_skills'])
                for relative in ['references/session-guide.md','adapters/codex.mjs']:
                    self.assertEqual(payload_bytes('payload/skills/agent-sessions/'+relative,p,client),(p/folder/'skills/agent-sessions'/relative).read_bytes())
                self.assertEqual(payload_bytes('payload/skills/kb-find/SKILL.md',p,client),(p/folder/'skills/kb-find/SKILL.md').read_bytes())
                self.assertFalse((p/folder/'AGENTS.md').exists());self.assertFalse((p/folder/'BASE-RULES.md').exists())
                self.assertIn("# The user's working rules",(p/entry).read_text(encoding='utf8'))
                self.assertEqual(call('verify','--client',client,'--target',p)['status'],'pass')
    def test_reviewer_consent_cannot_be_asserted_without_source(self):
        with target_directory() as td:
            call('install','--skills','kb-find','--reviewer-consent','one-per-round','--target',td,ok=2)
            self.assertEqual(list(Path(td).iterdir()),[])
    def test_removed_skills_are_refused_without_writes(self):
        with target_directory() as td:
            for name in ['ui-design','creative-direction','dev-plan','dev-debug','dev-verify','agent-instructions','dev-flow','visual-scenes']:
                call('install','--skills',name,'--target',td,ok=2)
            for profile in ['engineering','visual','instructions']:
                call('plan','--profile',profile,'--target',td,ok=2)
            self.assertEqual(list(Path(td).iterdir()),[])
    def test_profiles_and_brain_adapters(self):
        with target_directory() as td:
            for profile,skills in [('full',7),('brain',1),('voxel',1),('memory',5)]:
                with self.subTest(profile=profile):
                    planned=call('plan','--profile',profile,'--target',td)
                    self.assertEqual(len(planned['requested_skills']),skills)
                    self.assertEqual('you-are-brain' in planned['requested_skills'],profile in ['full','brain'])
            self.assertEqual(list(Path(td).iterdir()),[])
        files=['references/session-guide.md','references/contract.md','references/brief-writing.md','adapters/codex.mjs','adapters/wait.mjs']
        for client,folder in [('codex','.agents'),('claude','.claude')]:
            with self.subTest(client=client),target_directory() as td:
                # Old orchestration names stay accepted as aliases of you-are-brain.
                result=call('install','--skills','agent-sessions-codex','--client',client,'--target',td)
                self.assertEqual(result['installed_skills'],['you-are-brain']);self.assertFalse(result['workflow_activated'])
                for relative in files:
                    self.assertEqual(payload_bytes('payload/skills/agent-sessions/'+relative,td,client),(Path(td)/folder/'skills/agent-sessions'/relative).read_bytes())
                self.assertFalse((Path(td)/folder/'skills/agent-sessions/adapters/claude-code.mjs').exists())
                self.assertEqual(call('verify','--client',client,'--target',td)['status'],'pass')
        node=shutil.which('node')
        if not node:self.skipTest('Node is required to check the Codex adapter')
        script=str(ROOT/'payload/skills/agent-sessions/adapters/codex.mjs')
        described=subprocess.run([node,script,'--describe'],capture_output=True,cwd=ROOT)
        self.assertEqual(described.returncode,0,described.stderr.decode('utf8',errors='replace'))
        info=json.loads(described.stdout)
        self.assertEqual((info['agent'],info['contract'],info['verified']),('codex',2,True))
        self.assertEqual(set(info['access_modes']),{'read-only','workspace-write','danger-full-access'})
        refused=subprocess.run([node,script,'--sandbox','unknown-mode','--cwd',str(ROOT)],capture_output=True,cwd=ROOT,input=b'')
        self.assertEqual(refused.returncode,4)
    def test_brain_references_stay_inside_the_package(self):
        self.assertIn(b'Write the brief in English',(ROOT/'payload/skills/agent-sessions/references/brief-writing.md').read_bytes())
        text=(ROOT/'payload/skills/you-are-brain/SKILL.md').read_text(encoding='utf8')
        self.assertIn('session-guide.md', text)
        guide=(ROOT/'payload/skills/agent-sessions/references/session-guide.md').read_text(encoding='utf8')
        self.assertIn('adapters/codex.mjs',guide);self.assertIn('codex exec',guide);self.assertIn('spawn EPERM',guide)
    def test_plan_creates_nothing_and_doctor_does_not_claim_quality(self):
        with target_directory() as td:
            call('plan','--profile','full','--target',td);self.assertEqual(list(Path(td).iterdir()),[])
            call('install','--skills','kb-find','--target',td)
            self.assertEqual(call('doctor','--target',td)['quality_parity'],'not-established')
    def test_unmanaged_neighbor_is_preserved(self):
        with target_directory() as td:
            p=Path(td);neighbor=p/'my-work.txt';neighbor.write_bytes(b'unmanaged')
            call('install','--skills','kb-find','--target',p);call('remove','--target',p)
            self.assertEqual(neighbor.read_bytes(),b'unmanaged')
    def test_forged_receipt_cannot_delete_a_neighbor(self):
        with target_directory() as td:
            p=Path(td);call('install','--skills','kb-find','--target',p)
            neighbor=p/'my-work.txt';neighbor.write_bytes(b'unmanaged')
            receipt=p/'.agents/harness-install.json';r=json.loads(receipt.read_text())
            r['files'].append({'relative':'my-work.txt','sha256':hashlib.sha256(b'unmanaged').hexdigest(),'source':'generated-policy','owned':True})
            receipt.write_text(json.dumps(r));call('remove','--target',p,ok=2)
            self.assertEqual(neighbor.read_bytes(),b'unmanaged')
    def test_forged_canonical_entry_cannot_delete_unselected_skill(self):
        with target_directory() as td:
            p=Path(td);call('install','--skills','kb-find','--target',p)
            neighbor=p/'.agents/skills/agent-handoff/SKILL.md';neighbor.parent.mkdir(parents=True);neighbor.write_bytes(b'My own handoff')
            receipt=p/'.agents/harness-install.json';r=json.loads(receipt.read_text())
            r['files'].append({'relative':'.agents/skills/agent-handoff/SKILL.md','sha256':hashlib.sha256(neighbor.read_bytes()).hexdigest(),'source':'payload/skills/agent-handoff/SKILL.md','owned':True})
            receipt.write_text(json.dumps(r));call('remove','--target',p,ok=2)
            self.assertEqual(neighbor.read_bytes(),b'My own handoff')
    def test_forged_hash_cannot_reclassify_edited_file_as_owned_payload(self):
        with target_directory() as td:
            p=Path(td);call('install','--skills','kb-find','--target',p)
            edited=p/'.agents/skills/kb-find/SKILL.md';edited.write_bytes(b'My edit')
            receipt=p/'.agents/harness-install.json';r=json.loads(receipt.read_text())
            for f in r['files']:
                if f['relative']=='.agents/skills/kb-find/SKILL.md':f['sha256']=hashlib.sha256(edited.read_bytes()).hexdigest()
            receipt.write_text(json.dumps(r));call('remove','--target',p,ok=2)
            self.assertEqual(edited.read_bytes(),b'My edit')
    def test_named_dependency_and_skills_only_permission_guard(self):
        with target_directory() as td:
            p=Path(td);r=call('install','--skills','voxel-models','--target',p)
            self.assertEqual(r['installed_skills'],['voxel-models']);self.assertFalse(r['workflow_activated'])
            text=(p/'AGENTS.md').read_text(encoding='utf8')
            self.assertIn("owner's actual authorization",text)
            self.assertNotIn('# Общие правила работы',text)
    def test_codex_instruction_truncation_is_rejected_before_writes(self):
        with target_directory() as td:
            # Existing instructions fit exactly; any full bootstrap exceeds the default budget.
            p=Path(td);prefix=b'# Project\n';original=prefix+b'x'*(32768-len(prefix));(p/'AGENTS.md').write_bytes(original)
            call('install','--profile','full','--target',p,ok=2)
            self.assertEqual((p/'AGENTS.md').read_bytes(),original);self.assertFalse((p/'.agents').exists())
            call('install','--profile','full','--target',p,'--project-doc-max-bytes','65536')
            checks=call('doctor','--target',p)['checks'];startup=next(x for x in checks if x['capability']=='startup-instructions')
            self.assertEqual(startup['declared_budget'],65536);self.assertGreater(startup['project_bytes'],32768)
    def test_codex_override_is_preserved_and_installation_refused(self):
        with target_directory() as td:
            p=Path(td);(p/'AGENTS.override.md').write_bytes(b'My override')
            call('install','--skills','kb-find','--target',p,ok=2)
            self.assertEqual((p/'AGENTS.override.md').read_bytes(),b'My override');self.assertFalse((p/'.agents').exists())
    def test_removed_external_bundles_are_not_distributed(self):
        m=json.loads((ROOT/'manifest.json').read_text())
        self.assertEqual(m['runtime_assets'],[])
        self.assertFalse(any('/vendor/' in f['path'] for f in m['files']))
        # 3.0 ships no license copies or upstream source records inside skills.
        self.assertFalse(any('/licenses/' in f['path'] or f['path'].endswith(('/sources.json','/LICENSE')) for f in m['files']))
        self.assertFalse(list((ROOT/'payload').rglob('licenses')));self.assertFalse((ROOT/'docs/retired-attribution').exists())
    def test_receipt_cannot_hide_a_missing_entrypoint(self):
        with target_directory() as td:
            p=Path(td);call('install','--skills','kb-find','--target',p)
            skill=p/'.agents/skills/kb-find/SKILL.md';skill.unlink()
            receipt=p/'.agents/harness-install.json';r=json.loads(receipt.read_text())
            r['files']=[f for f in r['files'] if f['relative']!='.agents/skills/kb-find/SKILL.md'];receipt.write_text(json.dumps(r))
            call('verify','--target',p,ok=2);call('remove','--target',p,ok=2)
            self.assertTrue((p/'.agents/skills/kb-find').is_dir())
    def test_edited_policy_and_rehashed_receipt_are_preserved(self):
        with target_directory() as td:
            p=Path(td);call('install','--skills','kb-find','--target',p)
            policy=p/'.agents/harness-policy.json';v=json.loads(policy.read_text());v['user_notes']='My actual edit';policy.write_text(json.dumps(v))
            edited=policy.read_bytes();receipt=p/'.agents/harness-install.json';r=json.loads(receipt.read_text())
            for f in r['files']:
                if f['source']=='generated-policy':f['sha256']=hashlib.sha256(edited).hexdigest()
            receipt.write_text(json.dumps(r));call('verify','--target',p,ok=2);call('remove','--target',p,ok=2)
            self.assertEqual(policy.read_bytes(),edited)
    def test_mutually_consistent_destination_forgery_is_not_trusted(self):
        with target_directory() as td:
            p=Path(td);dest=p/'.agents/skills/kb-find/SKILL.md';dest.parent.mkdir(parents=True)
            before=payload_bytes('payload/skills/kb-find/SKILL.md',p);dest.write_bytes(before)
            call('install','--skills','kb-find','--target',p)
            receipt=p/'.agents/harness-install.json';r=json.loads(receipt.read_text())
            policy=p/'.agents/harness-policy.json';v=json.loads(policy.read_text());v['user_notes']='My actual added note'
            raw=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf8');policy.write_bytes(raw);r['policy_snapshot']=v
            for f in r['files']:
                if f['source']=='generated-policy':f['sha256']=hashlib.sha256(raw).hexdigest()
                if f['relative']=='.agents/skills/kb-find/SKILL.md':f['owned']=True
            receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
            call('verify','--target',p,ok=2);call('remove','--target',p,ok=2)
            self.assertEqual(dest.read_bytes(),before);self.assertEqual(policy.read_bytes(),raw)
    def test_memory_cli_and_limited_mcp_on_empty_authorized_vault(self):
        node=shutil.which('node')
        if not node:self.skipTest('Node is required for the memory helper route')
        with target_directory() as td:
            p=Path(td);call('install','--profile','memory','--target',p);call('init-memory','--target',p)
            vault=p/'.harness-memory';cli=vault/'SYSTEM/scripts/kb.mjs'
            payload={'schema_version':1,'title':'Synthetic test','source':{'kind':'manual','session_id':'fixture-session','turn_id':'fixture-turn'},'batch_key':'cli','final':True,'items':[{'type':'fact','text':'Canary apple exists.','evidence':'Synthetic test only.'}]}
            def execute(script,*args,data=None,env=None):
                r=subprocess.run([node,str(script),*args],input=None if data is None else data.encode('utf8'),capture_output=True,cwd=p,env=env)
                self.assertEqual(r.returncode,0,r.stderr.decode('utf8',errors='replace'));return r.stdout.decode('utf8')
            first=json.loads(execute(cli,'capture',data=json.dumps(payload)));again=json.loads(execute(cli,'capture',data=json.dumps(payload)))
            self.assertFalse(first['duplicate']);self.assertTrue(again['duplicate']);self.assertTrue((vault/first['path']).is_file())
            env=os.environ.copy();env['HARNESS_KB_ROOT']=str(vault)
            def request(i,name,args):return {'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':name,'arguments':args}}
            curator={**payload,'source':{**payload['source'],'kind':'rumi'},'batch_key':'mcp'}
            messages=[{'jsonrpc':'2.0','id':1,'method':'tools/list'},request(2,'kb_checkpoint',{'session_id':'fixture-session','turn_id':'empty'}),request(3,'kb_capture',{'payload':curator}),request(4,'kb_capture',{'payload':payload,'path':'../forbidden'}),request(5,'sync',{})]
            out=execute(p/'.agents/workflow/kb-writer.mjs',data=''.join(json.dumps(x)+'\n' for x in messages),env=env);rows=[json.loads(x) for x in out.splitlines()]
            self.assertEqual({x['name'] for x in rows[0]['result']['tools']},{'kb_capture','kb_checkpoint'})
            self.assertFalse(rows[1]['result']['isError']);self.assertFalse(rows[2]['result']['isError']);self.assertTrue(rows[3]['result']['isError']);self.assertIn('error',rows[4])
            saved=json.loads(rows[2]['result']['content'][0]['text'])
            self.assertTrue((vault/saved['path']).is_file())
            self.assertIn('rumi',(vault/saved['path']).read_text(encoding='utf8'))
    def test_memory_initialization_is_explicit_idempotent_and_preserves_data(self):
        with target_directory() as td:
            p=Path(td);vault=p/'private-vault';call('install','--profile','memory','--target',p,'--memory-root',vault)
            self.assertFalse(vault.exists());call('init-memory','--target',p)
            call('init-memory','--target',p)
            self.assertTrue((vault/'SYSTEM/scripts/kb.mjs').is_file())
            (vault/'INDEX.md').write_bytes(b'My actual knowledge')
            call('init-memory','--target',p,ok=2)
            self.assertEqual((vault/'INDEX.md').read_bytes(),b'My actual knowledge')
            call('remove','--target',p);self.assertEqual((vault/'INDEX.md').read_bytes(),b'My actual knowledge')
if __name__=='__main__':unittest.main()
