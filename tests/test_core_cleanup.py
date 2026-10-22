"""Behavioral installation/dependency and 1.6->2.0 migration regressions."""
import hashlib,io,json,subprocess,sys,tarfile,unittest
from pathlib import Path
from test_install import ROOT,call,target_directory
from test_migration import snapshot,release_archive

class CoreSelection(unittest.TestCase):
    def test_selected_routes_do_not_expand_optional_links(self):
        expected={
            'dev-debug':{'dev-debug','dev-flow'},
            'dev-flow':{'dev-flow'},
            'you-are-brain':{'you-are-brain','agent-sessions','agent-sessions-codex','dev-flow'},
            'jam-board':{'jam-board','agent-sessions','agent-sessions-codex','dev-plan','dev-flow'},
        }
        for skill,names in expected.items():
            with self.subTest(skill=skill),target_directory() as td:
                result=call('install','--skills',skill,'--target',td)
                self.assertEqual(set(result['installed_skills']),names)
                found={p.parent.name for p in (Path(td)/'.agents/skills').glob('*/SKILL.md')}
                self.assertEqual(found,names)
                self.assertFalse((Path(td)/'.agents/skills/voxel-models').exists())
                self.assertIn('optional routes',(Path(td)/'AGENTS.md').read_text())
                self.assertEqual(call('verify','--target',td)['status'],'pass')
    def test_retired_alias_does_not_install_replacement(self):
        with target_directory() as td:
            call('install','--skills','ui-ux-pro-max','--target',td,ok=2)
            self.assertEqual(snapshot(Path(td)),{})

class CoreUpgrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context=target_directory();cls.legacy=Path(cls.context.__enter__())
        with tarfile.open(fileobj=io.BytesIO(release_archive('586c922484810c76bfa53383df434aaf4dc914eb'))) as bundle:
            bundle.extractall(cls.legacy,filter='data')
    @classmethod
    def tearDownClass(cls):cls.context.__exit__(None,None,None)
    def old_install(self,target):
        subprocess.run([sys.executable,str(self.legacy/'harness.py'),'install','--profile','full','--target',str(target)],cwd=self.legacy,capture_output=True,check=True)
        old=json.loads((target/'.agents/harness-install.json').read_text())
        # Transfer the legitimate private receipt between these two test installer checkouts.
        identity=hashlib.sha256((str(target.resolve())+'\n'+'codex').encode()).hexdigest()+'.json'
        f=self.legacy/'.harness-state/receipts'/identity
        dest=ROOT/'.harness-state/receipts'/identity;dest.parent.mkdir(exist_ok=True,parents=True);dest.write_bytes(f.read_bytes())
        self.addCleanup(lambda:dest.unlink(missing_ok=True))
        return old
    def test_upgrade_removes_owned_vendor_keeps_unowned_neighbor(self):
        with target_directory() as td:
            target=Path(td);neighbor=target/'.agents/skills/my-private-skill/SKILL.md';neighbor.parent.mkdir(parents=True);neighbor.write_text('Private instructions')
            # Preexisting identical retired skill is unowned and must survive.
            unowned=target/'.agents/skills/ui-taste-reference/LICENSE';unowned.parent.mkdir(parents=True);unowned.write_bytes((self.legacy/'payload/skills/ui-taste-reference/LICENSE').read_bytes())
            self.old_install(target)
            result=call('install','--profile','full','--target',target)
            self.assertEqual(result['migration_from'],'1.6.0')
            self.assertEqual(len(result['installed_skills']),20)
            self.assertFalse((target/'.agents/skills/ui-reference/SKILL.md').exists())
            self.assertFalse((target/'.agents/skills/dev-verify/vendor').exists())
            self.assertEqual(neighbor.read_text(),'Private instructions');self.assertTrue(unowned.exists())
            self.assertEqual(call('verify','--target',target)['status'],'pass')
            call('remove','--target',target);self.assertTrue(neighbor.exists());self.assertTrue(unowned.exists())
    def test_edited_retired_file_refuses_before_any_writes(self):
        with target_directory() as td:
            target=Path(td);self.old_install(target)
            retired=target/'.agents/skills/ui-reference/SKILL.md';retired.write_text('User customization')
            before=snapshot(target)
            call('install','--profile','full','--target',target,ok=2)
            self.assertEqual(snapshot(target),before)
