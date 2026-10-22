#!/usr/bin/env python3
"""Compare source bytes at a Git baseline with this checkout; never calls a model."""
import argparse,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--baseline',default='586c922484810c76bfa53383df434aaf4dc914eb');args=ap.parse_args()
def git(path):return subprocess.check_output(['git','show',args.baseline+':'+path],cwd=ROOT)
def summary(manifest,read):
    entries=[]
    for row in manifest['files']:
        p=row['path']
        if p.startswith('payload/skills/') and p.count('/')==3 and p.endswith('/SKILL.md'):
            raw=read(p);t=raw.decode('utf-8-sig');head=t.split('---',2)[1]
            name=re.search(r'^name:\s*["\']?([^\n"\']+)',head,re.M)[1].strip()
            desc=re.search(r'^description:\s*(.+)',head,re.M)[1].strip().strip('"\'')
            entries.append((name,desc,len(raw)))
    catalog='\n'.join(f'- {n}: {d} (file: r1/{n}/SKILL.md)' for n,d,_ in sorted(entries))+'\n'
    base=read('payload/AGENTS.md').decode().replace('{{HARNESS_ROOT}}','/project/.agents').replace('{{MEMORY_ROOT}}','/project/.harness-memory')
    # Reproduce the old dependency rule for the baseline; current uses its explicit map.
    deps={n:set() for n,_,_ in entries}
    if 'skill_dependencies' in manifest:
        deps={n:set(manifest['skill_dependencies'].get(n,[])) for n in deps}
    else:
        for row in manifest['files']:
            owner=row['module'];p=row['path']
            if owner not in deps or Path(p).suffix.lower() not in ['.md','.py','.mjs','.ps1']:continue
            text=read(p).decode('utf-8-sig');text=re.sub(r'''(clientInfo:\s*\{\s*name:\s*)['"][^'"]*['"]''',r'\1""',text)
            for other in deps:
                named=re.search(r'(?<![\w-])'+re.escape(other)+r'(?![\w-])',text) if '-' in other and other not in {'stress-test','agent-handoff'} else re.search(r'[`\"\[]'+re.escape(other)+r'[`\"\]]',text)
                if other!=owner and (named or f'/skills/{other}/' in text or re.search(r'\.\./(?:\.\./)?'+re.escape(other)+r'/',text)):deps[owner].add(other)
    closure={};selected_catalog={}
    for n in deps:
        seen={n}
        while True:
            expanded=seen|set().union(*(deps[x] for x in seen))
            if seen==expanded:break
            seen=expanded
        closure[n]=len(seen)
        selected_catalog[n]=len(("\n".join(f"- {name}: {desc} (file: r1/{name}/SKILL.md)" for name,desc,_ in sorted(entries) if name in seen)+"\n").encode())
    return {'version':manifest['version'],'skills':len(entries),'payload_files':len(manifest['files']),'base_bound_utf8_bytes':len(base.encode()),'catalog_reconstructed_utf8_bytes':len(catalog.encode()),'base_plus_catalog_bytes':len(base.encode())+len(catalog.encode()),'all_skill_bodies_bytes':sum(s for _,_,s in entries),'all_reference_md_bytes':sum(len(read(r['path'])) for r in manifest['files'] if '/references/' in r['path'] and r['path'].endswith('.md')),'payload_bytes':sum(len(read(r['path'])) for r in manifest['files']),'installed_closure_by_skill':closure,'selected_catalog_utf8_bytes':selected_catalog}
old=json.loads(git('manifest.json'));new=json.loads((ROOT/'manifest.json').read_text())
print(json.dumps({'baseline_commit':args.baseline,'method':'UTF-8 source byte accounting with identical /project bindings and catalog format; catalog BEFORE client budget/truncation; NOT actual runtime load, tokens, billed prompt or quality benchmark','before':summary(old,git),'after':summary(new,lambda p:(ROOT/p).read_bytes())},ensure_ascii=False,indent=2))
