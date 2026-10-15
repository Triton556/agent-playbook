import hashlib,json,shutil,subprocess,unittest
from pathlib import Path
from test_install import target_directory,call

class PortableRetrieval(unittest.TestCase):
    def write(self,root,relative,value):
        p=root/relative;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(value,ensure_ascii=False) if not isinstance(value,str) else value,encoding='utf-8')
    def execute(self,vault,helper,*args,code=0):
        proc=subprocess.run([shutil.which('node'),str(vault/'SYSTEM/scripts'/helper),*map(str,args)],capture_output=True)
        self.assertEqual(proc.returncode,code,proc.stderr.decode('utf-8',errors='replace'))
        return json.loads(proc.stdout) if proc.stdout else proc.stderr.decode('utf-8',errors='replace')
    def hashes(self,vault):
        return {p.relative_to(vault).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in vault.rglob('*') if p.is_file()}
    def initialize(self,p):
        call('install','--profile','memory','--target',p);call('init-memory','--target',p)
        return p/'.harness-memory'

    def test_current_history_search_and_inbox_are_read_only(self):
        with target_directory() as td:
            vault=self.initialize(Path(td))
            self.write(vault,'PROJECTS/Harbour.md','# Harbour project\n\nHarbour decision: the bridge is approved.\n')
            self.write(vault,'ARCHIVE/old.md','# Harbour project\n\nHarbour decision: the obsolete bridge was proposed.\n')
            self.write(vault,'INBOX/new.md','# Harbour update\n\nHarbour decision still needs source review.\n')
            before=self.hashes(vault)
            current=self.execute(vault,'kb-search.mjs','harbour','--mode','current','--limit','8')
            history=self.execute(vault,'kb-search.mjs','harbour','--mode','history','--limit','8')
            self.assertEqual(current['results'][0]['path'],'PROJECTS/Harbour.md')
            self.assertEqual(history['results'][0]['path'],'ARCHIVE/old.md')
            self.assertEqual(current['inbox'][0]['path'],'INBOX/new.md')
            self.assertEqual(self.hashes(vault),before)
            self.assertTrue((vault/'SYSTEM/examples/retrieval-cases.template.json').is_file())

    def test_coverage_requires_own_registry_and_detects_lost_topic(self):
        with target_directory() as td:
            vault=self.initialize(Path(td))
            self.execute(vault,'kb-coverage.mjs',vault,code=2)
            self.write(vault,'INDEX.md','# Index\n\n[Harbour](PROJECTS/Harbour.md)\n')
            self.write(vault,'INBOX/example.md','# Example source\n\n## 1. decision\n\nThe bridge is approved.\n')
            self.write(vault,'PROJECTS/Harbour.md','# Harbour\n\nApproved bridge. Source: example-source\n')
            self.write(vault,'SYSTEM/coverage/coverage.json',{'entries':[{'id':'example-source','source':'INBOX/example.md','items':[{'item':1,'disposition':'covered','summary':'Approved bridge','topics':['PROJECTS/Harbour.md']}]}]})
            before=self.hashes(vault);good=self.execute(vault,'kb-coverage.mjs',vault)
            self.assertEqual(good['errors'],0);self.assertEqual(good['itemCount'],1)
            self.assertEqual(self.hashes(vault),before)
            self.write(vault,'INDEX.md','# Index\n\nNo reachable project.\n')
            bad=self.execute(vault,'kb-coverage.mjs',vault,code=1)
            self.assertTrue(any('Unreachable topic' in s for s in bad['findings']))

    def test_navigation_requires_own_topology_and_detects_root_shortcut(self):
        with target_directory() as td:
            vault=self.initialize(Path(td))
            self.execute(vault,'kb-navigation.mjs',vault,code=2)
            self.write(vault,'INDEX.md','# Index\n\n[Projects](AREAS/Projects.md)\n')
            self.write(vault,'AREAS/Projects.md','# Projects\n\n[Back](../INDEX.md)\n[Harbour](../PROJECTS/Harbour.md)\n')
            self.write(vault,'PROJECTS/Harbour.md','# Harbour\n\n[Projects](../AREAS/Projects.md)\n')
            self.write(vault,'SYSTEM/navigation/parents.json',{'top_levels':['AREAS/Projects.md'],'parents':{'AREAS/Projects.md':'INDEX.md','PROJECTS/Harbour.md':'AREAS/Projects.md'},'preserved_history':[],'root_support':[],'root_support_history':[],'allowed_root_incoming':['AREAS/Projects.md']})
            before=self.hashes(vault);good=self.execute(vault,'kb-navigation.mjs',vault)
            self.assertEqual(good['errors'],0);self.assertEqual(good['reachableSubjects'],1)
            self.assertEqual(self.hashes(vault),before)
            self.write(vault,'PROJECTS/Harbour.md','# Harbour\n\n[Wrong direct root](../INDEX.md)\n')
            bad=self.execute(vault,'kb-navigation.mjs',vault,code=1)
            self.assertTrue(any(f['code']=='subject-to-root' for f in bad['findings']))
