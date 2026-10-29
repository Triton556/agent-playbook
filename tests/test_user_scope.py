import json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from test_install import ROOT,call,target_directory
class UserScope(unittest.TestCase):
 def setUp(self):
  from unittest.mock import patch
  clean=dict(os.environ);clean.pop("CODEX_HOME",None);self.env=patch.dict(os.environ,clean,clear=True);self.env.start();self.addCleanup(self.env.stop)
 def test_clean_user_install_preserves_project_and_removes_owned_only(self):
  for client,sub,entry in [('codex','.agents','.codex/AGENTS.md'),('claude','.claude','.claude/CLAUDE.md')]:
   with self.subTest(client=client),target_directory() as d:
    home=Path(d);project=home/'work';project.mkdir();(project/'AGENTS.md').write_text('Design system only\n');ip=home/entry;ip.parent.mkdir(parents=True,exist_ok=True);ip.write_text('My existing preference\n')
    args=['--client',client,'--target',home,'--scope','user'];vault=home/'knowledge';vault.mkdir();(vault/'INDEX.md').write_text('Keep me')
    self.assertEqual(call('plan',*args,'--profile','full','--memory-root',vault)['writes'],0)
    self.assertFalse((home/sub/'skills').exists())
    got=call('install',*args,'--profile','full','--memory-root',vault);self.assertEqual(len(got['installed_skills']),7)
    self.assertIn('My existing preference',ip.read_text());self.assertIn('agent-playbook:begin',ip.read_text());self.assertFalse((home/'AGENTS.md').exists());self.assertFalse((project/'.agents').exists())
    self.assertEqual((project/'AGENTS.md').read_text(),'Design system only\n');self.assertEqual(call('verify',*args)['status'],'pass')
    neighbor=home/sub/'skills/design-system';neighbor.mkdir();(neighbor/'SKILL.md').write_text('Keep DS')
    call('install',*args,'--profile','full','--memory-root',vault)
    call('remove',*args);self.assertEqual(ip.read_text(),'My existing preference\n');self.assertTrue((neighbor/'SKILL.md').exists());self.assertEqual((vault/'INDEX.md').read_text(),'Keep me')
 def test_modified_user_instruction_blocks_remove_and_wrong_scope(self):
  with target_directory() as d:
   home=Path(d);args=['--target',home,'--scope','user'];call('install',*args,'--profile','full')
   for cmd in [['verify','--target',str(home)],['remove','--target',str(home)]]:
    p=subprocess.run([sys.executable,str(ROOT/'harness.py'),*cmd],capture_output=True,text=True);self.assertNotEqual(p.returncode,0)
   ip=home/'.codex/AGENTS.md';ip.write_text(ip.read_text().replace('Communicate directly','Changed directly'))
   p=subprocess.run([sys.executable,str(ROOT/'harness.py'),'remove',*map(str,args)],capture_output=True,text=True);self.assertNotEqual(p.returncode,0);self.assertTrue(ip.exists());self.assertTrue((home/'.agents/skills/you-are-brain/SKILL.md').exists())
 def test_override_and_custom_codex_home_refuse_without_writes(self):
  with target_directory() as d:
   home=Path(d);(home/'.codex').mkdir();(home/'.codex/AGENTS.override.md').write_text('Keep override')
   cmd=[sys.executable,str(ROOT/'harness.py'),'install','--target',str(home),'--scope','user','--profile','full']
   p=subprocess.run(cmd,capture_output=True,text=True);self.assertNotEqual(p.returncode,0);self.assertFalse((home/'.agents').exists())
   (home/'.codex/AGENTS.override.md').unlink();p=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'CODEX_HOME':str(home/'other-config')});self.assertNotEqual(p.returncode,0);self.assertFalse((home/'.agents').exists())
if __name__=='__main__':unittest.main()
