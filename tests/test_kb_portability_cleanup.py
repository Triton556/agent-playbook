"""Real install/upgrade/capture/retrieval scenarios, no model-quality claim."""
import os,hashlib,io,json,subprocess,sys,tarfile,unittest
from pathlib import Path
from test_install import ROOT,call,target_directory
from test_migration import release_archive,snapshot

BASE='738d570f488e070f18cb01fc512f4c91ec1be253'
class PortableKB(unittest.TestCase):
 def test_each_kb_entry_supplies_its_manual_without_vault(self):
  for name in ['kb-find','kb-save','kb-curate','kb-sync','kb-status']:
   with self.subTest(skill=name),target_directory() as td:
    root=Path(td);call('install','--target',root,'--skills',name)
    self.assertFalse((root/'.harness-memory').exists())
    refs=root/'.agents/skills/kb-common/references'
    self.assertTrue((refs/'layout.md').is_file())
    self.assertTrue((refs/'capture.md').is_file())
    self.assertTrue((refs/'cloud-exchange.md').is_file())
    self.assertEqual({p.parent.name for p in (root/'.agents/skills').glob('*/SKILL.md')},{name})
    entry=(root/'.agents/skills'/name/'SKILL.md').read_text()
    self.assertNotIn('Read SYSTEM/workflows/',entry)
    self.assertEqual(call('verify','--target',root)['status'],'pass')
 def test_capture_archive_and_retrieve_on_new_computer_without_vault_manual(self):
  with target_directory() as td:
   root=Path(td);call('install','--target',root,'--profile','memory');call('init-memory','--target',root)
   vault=root/'.harness-memory'
   # No procedure copied from an existing personal vault is available.
   for p in (vault/'SYSTEM/workflows').glob('*.md'):p.unlink()
   source={'schema_version':1,'title':'Synthetic harbour decision','source':{'kind':'manual','session_id':'portable-kb-test','turn_id':'first'},'batch_key':'decision','final':True,'items':[{'type':'decision','text':'Harbour bridge approved; keep pedestrian access.','evidence':'Synthetic user decision.'}]}
   def node(script,*args,input=None):
    r=subprocess.run(['node',str(vault/'SYSTEM/scripts'/script),*args],input=input,capture_output=True,text=True,cwd=vault)
    self.assertEqual(r.returncode,0,r.stderr);return json.loads(r.stdout)
   capture=node('kb.mjs','capture',input=json.dumps(source));original=vault/capture['path'];raw=original.read_bytes()
   archived=vault/'ARCHIVE'/original.name;original.rename(archived)
   project=vault/'PROJECTS/Harbour.md';project.write_text('# Harbour\n\nHarbour bridge approved; pedestrian access retained.\n\n[Source](../ARCHIVE/'+archived.name+')\n')
   (vault/'INDEX.md').write_text('# Index\n\n[Harbour](PROJECTS/Harbour.md)\n')
   self.assertEqual(archived.read_bytes(),raw)
   again=node('kb.mjs','capture',input=json.dumps(source));self.assertTrue(again['duplicate'])
   self.assertFalse(original.exists())
   found=node('kb-search.mjs','Harbour','--mode','current','--limit','8')
   self.assertEqual(found['results'][0]['path'],'PROJECTS/Harbour.md')
   self.assertIn('pedestrian access',project.read_text())
   self.assertTrue((root/'.agents/skills/kb-curate/SKILL.md').is_file())

class CleanupUpgrade(unittest.TestCase):
 def setUp(self):
  from unittest.mock import patch
  clean=dict(os.environ);clean.pop('CODEX_HOME',None);env=patch.dict(os.environ,clean,clear=True);env.start();self.addCleanup(env.stop)
 @classmethod
 def setUpClass(cls):
  cls.context=target_directory();cls.legacy=Path(cls.context.__enter__())
  with tarfile.open(fileobj=io.BytesIO(release_archive(BASE))) as archive:archive.extractall(cls.legacy,filter='data')
 @classmethod
 def tearDownClass(cls):cls.context.__exit__(None,None,None)
 def old(self,root,client):
  subprocess.run([sys.executable,str(self.legacy/'harness.py'),'install','--scope','user','--target',str(root),'--client',client,'--profile','full'],cwd=self.legacy,check=True,capture_output=True)
  key=hashlib.sha256((str(root.resolve())+'\n'+client).encode()).hexdigest()+'.json'
  dest=ROOT/'.harness-state/receipts'/key;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((self.legacy/'.harness-state/receipts'/key).read_bytes());self.addCleanup(lambda:dest.unlink(missing_ok=True))
 def test_upgrade_211_user_scope_removes_design_keeps_vault_and_project(self):
  for client,native in [('codex','.agents'),('claude','.claude')]:
   with self.subTest(client=client),target_directory() as td:
    root=Path(td);self.old(root,client)
    for rel in ['project/.agents/skills/design-system/SKILL.md','.harness-memory/PROJECTS/Owned.md','.harness-memory/SYSTEM/workflows/curate.md']:
     p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'Owner content\r\n')
    before={p:p.read_bytes() for p in root.rglob('*') if p.is_file() and p.read_bytes()==b'Owner content\r\n'}
    result=call('install','--scope','user','--target',root,'--client',client,'--profile','full')
    self.assertEqual(result['migration_from'],'2.1.1');self.assertEqual(len(result['installed_skills']),11)
    for name in ['ui-design','ui-review','creative-direction']:
     self.assertFalse(any((root/native/'skills'/name).rglob('*.*')))
    for p,data in before.items():self.assertEqual(p.read_bytes(),data)
    self.assertEqual(call('verify','--scope','user','--client',client,'--target',root)['status'],'pass')
    after=snapshot(root);call('install','--scope','user','--target',root,'--client',client,'--profile','full');self.assertEqual(snapshot(root),after)
 def test_edited_design_blocks_upgrade_without_data_loss(self):
  with target_directory() as td:
   root=Path(td);self.old(root,'codex');p=root/'.agents/skills/ui-design/SKILL.md';p.write_text('My custom design rules')
   before=snapshot(root);call('install','--scope','user','--target',root,'--profile','full',ok=2);self.assertEqual(snapshot(root),before)
