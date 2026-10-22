"""Public 1.0 names and real 0.5.0 receipt migration, without network access."""
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import unittest

from test_install import ROOT, call, target_directory

RENAMES={
    'product-engineering':'dev-flow',
    'product-planning':'dev-plan',
    'product-implementation':'dev-implement',
    'product-debugging':'dev-debug',
    'product-testing':'dev-verify',
    'domain-modeling':'dev-domain-model',
    'product-ui-design':'ui-design',
    'product-ui-review':'ui-review',
    'ui-ux-pro-max':'ui-reference',
    'design-taste-frontend-v1':'ui-taste-reference',
    'codex-sessions':'agent-sessions-codex',
    'handoff':'agent-handoff',
    'writing-for-agents':'agent-instructions',
    'grilling':'stress-test',
    'grill-with-docs':'stress-test-with-docs',
    'visual-experiment-craft':'visual-scenes',
    'voxel-model-craft':'voxel-models',
}
RETIRED={'ui-reference','ui-taste-reference','stress-test','stress-test-with-docs','dev-domain-model','agent-handoff'}
REMOVED={'anthropic-workflow-creator','lab-vm-control'}|RETIRED


def snapshot(folder):
    return {p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob('*') if p.is_file()}



def release_archive(sha):
    """Earlier release from git history; shallow clones skip instead of failing."""
    if subprocess.run(['git','cat-file','-e',sha+'^{commit}'],cwd=ROOT,capture_output=True).returncode!=0:
        raise unittest.SkipTest('Release '+sha+' is not in this clone; fetch full history (git fetch --unshallow) to run migration tests')
    return subprocess.run(['git','archive','--format=tar',sha],cwd=ROOT,capture_output=True,check=True).stdout

class PublicNames(unittest.TestCase):
    def test_every_old_cli_name_warns_and_selects_the_new_skill(self):
        with target_directory() as td:
            for old,new in RENAMES.items():
                if new in RETIRED:continue
                with self.subTest(old=old):
                    result=subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/'harness.py'),'plan','--target',td,'--skills',old],capture_output=True,cwd=ROOT)
                    self.assertEqual(result.returncode,0,result.stderr.decode('utf8'))
                    plan=json.loads(result.stdout)
                    self.assertEqual(plan['requested_skills'],[new])
                    self.assertIn(new,plan['installed_skills'])
                    self.assertIn('Warning:',result.stderr.decode('utf8'))
                    self.assertIn(old,result.stderr.decode('utf8'))
                    self.assertIn(new,result.stderr.decode('utf8'))
                    self.assertTrue(set(plan['installed_skills']).isdisjoint(RENAMES))
            self.assertEqual(snapshot(Path(td)),{})

    def test_removed_cli_names_fail_clearly_without_writes(self):
        for command in ['plan','install']:
            for name in REMOVED:
                with self.subTest(command=command,name=name),target_directory() as td:
                    result=call(command,'--target',td,'--skills',name,ok=2)
                    self.assertIn('Removed skill: '+name,result['message'])
                    self.assertEqual(snapshot(Path(td)),{})

    def test_catalog_inventory_frontmatter_and_profile_membership(self):
        m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
        self.assertEqual(m['name'],'agent-playbook');self.assertTrue(m['version'].startswith('2.'))
        self.assertFalse(any('/vendor/' in f['path'] for f in m['files']))
        self.assertEqual({f['path'] for f in m['files']},{p.relative_to(ROOT).as_posix() for p in (ROOT/'payload').rglob('*') if p.is_file()})
        skills={s['name'] for s in call('catalog')['skills']}
        self.assertEqual(skills,(set(RENAMES.values())-RETIRED)|{'you-are-brain','jam-board','agent-sessions','creative-direction','kb-find','kb-save','kb-curate','kb-status','kb-sync'})
        for name in skills:
            self.assertIn('\nname: '+name+'\n',(ROOT/'payload/skills'/name/'SKILL.md').read_text(encoding='utf8'))
        with target_directory() as td:
            plan=call('plan','--target',td,'--profile','engineering')
            self.assertEqual(set(plan['requested_skills']),{'dev-flow','dev-plan','dev-implement','dev-debug','dev-verify','ui-design','ui-review','agent-sessions','agent-sessions-codex','you-are-brain','creative-direction','agent-instructions','jam-board'})
            self.assertEqual(len(plan['installed_skills']),13)
            self.assertNotIn('stress-test',plan['installed_skills'])
            plan=call('plan','--target',td,'--profile','instructions')
            self.assertEqual(set(plan['requested_skills']),{'agent-sessions','agent-sessions-codex','you-are-brain','agent-instructions'})
            self.assertEqual(len(plan['installed_skills']),5)


class LegacyMigration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Immutable local 0.5.0 release; no remote fetch or global configuration.
        cls.legacy_context=target_directory()
        cls.legacy=Path(cls.legacy_context.__enter__())
        archive=release_archive('7534298')
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(cls.legacy,filter='data')
        if json.loads((cls.legacy/'manifest.json').read_text(encoding='utf8'))['version']!='0.5.0':
            raise AssertionError('Legacy fixture must be actual 0.5.0')

    @classmethod
    def tearDownClass(cls):
        cls.legacy_context.__exit__(None,None,None)

    def legacy_install(self,target,client='codex',skills=None):
        options=['--skills',skills] if skills else ['--profile','full']
        result=subprocess.run([sys.executable,'-B','-X','utf8',str(self.legacy/'harness.py'),'install','--target',str(target),'--client',client,*options],cwd=self.legacy,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr.decode('utf8'))
        folder='.claude' if client=='claude' else '.agents'
        old=json.loads((target/folder/'harness-install.json').read_text(encoding='utf8'))
        self.assertEqual(old['version'],'0.5.0')
        # Simulate updating the checkout while retaining its private receipt store.
        identity=hashlib.sha256((str(target.resolve())+'\n'+client).encode('utf8')).hexdigest()+'.json'
        trust=ROOT/'.harness-state/receipts'/identity
        trust.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(self.legacy/'.harness-state/receipts'/identity,trust)
        self.addCleanup(lambda:trust.unlink(missing_ok=True))
        return old,trust

    def test_actual_050_full_upgrade_codex_and_claude_preserves_user_content(self):
        for client,folder,entry in [('codex','.agents','AGENTS.md'),('claude','.claude','CLAUDE.md')]:
            with self.subTest(client=client),target_directory() as td:
                p=Path(td);original=b'\xef\xbb\xbf# User project\r\nKeep this rule.\r\n'
                (p/entry).write_bytes(original)
                unowned=p/folder/'skills/handoff/SKILL.md';unowned.parent.mkdir(parents=True)
                unowned.write_bytes((self.legacy/'payload/skills/handoff/SKILL.md').read_bytes())
                unowned_bytes=unowned.read_bytes()
                neighbor=unowned.parent/'user-notes.txt';neighbor.write_bytes(b'private user file')
                old,_=self.legacy_install(p,client)
                with (p/entry).open('ab') as out:out.write(b'\r\nNew user rule.\r\n')
                before=snapshot(p)
                plan=call('plan','--client',client,'--target',p,'--profile','full')
                self.assertEqual(plan['migration_from'],'0.5.0')
                self.assertGreater(plan['obsolete_owned_files'],0)
                self.assertEqual(snapshot(p),before)
                result=call('install','--client',client,'--target',p,'--profile','full')
                self.assertEqual(result['migration_from'],'0.5.0')
                self.assertEqual(len(result['installed_skills']),20)
                receipt=json.loads((p/folder/'harness-install.json').read_text(encoding='utf8'))
                self.assertEqual(receipt['version'],json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))['version'])
                current={row['relative'] for row in receipt['files']}
                for row in old['files']:
                    if row['owned'] and row['relative'] not in current:self.assertFalse((p/row['relative']).exists(),row['relative'])
                self.assertEqual(neighbor.read_bytes(),b'private user file')
                for gone in ['product-testing','lab-vm-control','anthropic-workflow-creator']:self.assertFalse((p/folder/'skills'/gone).exists(),gone)
                self.assertTrue(neighbor.parent.is_dir())
                self.assertEqual(unowned.read_bytes(),unowned_bytes)
                self.assertTrue((p/entry).read_bytes().startswith(original))
                self.assertTrue((p/entry).read_bytes().endswith(b'\r\nNew user rule.\r\n'))
                self.assertEqual(call('verify','--client',client,'--target',p)['status'],'pass')
                migrated=snapshot(p)
                call('install','--client',client,'--target',p,'--profile','full')
                self.assertEqual(snapshot(p),migrated)
                call('remove','--client',client,'--target',p)
                self.assertEqual((p/entry).read_bytes(),original+b'\r\nNew user rule.\r\n')
                self.assertEqual(unowned.read_bytes(),unowned_bytes)
                self.assertEqual(neighbor.read_bytes(),b'private user file')

    def test_actual_050_selected_skill_upgrade_using_old_alias(self):
        for old,new in [('agent-sessions','agent-sessions')]:
            with self.subTest(skill=old),target_directory() as td:
                p=Path(td);self.legacy_install(p,skills=old)
                result=call('install','--target',p,'--skills',old)
                self.assertEqual(result['installed_skills'],
                                 call('plan','--target',p,'--skills',new)['installed_skills'])
                self.assertIn(new,result['installed_skills'])
                if new=='agent-sessions':self.assertNotIn('you-are-brain',result['installed_skills'])
                if old!=new:self.assertFalse((p/'.agents/skills'/old/'SKILL.md').exists())
                self.assertTrue((p/'.agents/skills'/new/'SKILL.md').is_file())
                self.assertEqual(call('verify','--target',p)['status'],'pass')

    def test_legacy_conflicts_refuse_before_any_write(self):
        for defect in ['edited','missing','block','policy','new-path','forged-receipt','missing-trust','different-options','unowned-update']:
            with self.subTest(defect=defect),target_directory() as td:
                p=Path(td)
                if defect=='unowned-update':
                    document=p/'.agents/workflow/WORKFLOW.md';document.parent.mkdir(parents=True)
                    raw=(self.legacy/'payload/workflow/WORKFLOW.md').read_bytes().decode('utf8')
                    raw=raw.replace('{{HARNESS_ROOT}}',(p/'.agents').as_posix()).replace('{{EVIDENCE_ROOT}}',(p/'optional-evidence').as_posix())
                    self.assertNotIn('{{',raw)
                    document.write_bytes(raw.encode('utf8'))
                _,trust=self.legacy_install(p,skills='domain-modeling' if defect!='unowned-update' else None)
                dest=p/'.agents/skills/domain-modeling/SKILL.md'
                if defect=='edited':dest.write_bytes(b'User edit')
                elif defect=='missing':dest.unlink()
                elif defect=='block':
                    ip=p/'AGENTS.md';ip.write_bytes(ip.read_bytes().replace(b'Installed workflow harness',b'Changed by user'))
                elif defect=='policy':
                    policy=p/'.agents/harness-policy.json';policy.write_bytes(policy.read_bytes()+b' ')
                elif defect=='new-path':
                    new=p/'.agents/skills/dev-domain-model/SKILL.md';new.parent.mkdir(parents=True);new.write_bytes(b'My different skill')
                elif defect=='forged-receipt':
                    receipt=p/'.agents/harness-install.json';r=json.loads(receipt.read_text(encoding='utf8'));r['files']=[];receipt.write_text(json.dumps(r),encoding='utf8')
                elif defect=='missing-trust':trust.unlink()
                before=snapshot(p)
                options=['--profile','full'] if defect=='unowned-update' else ['--skills','kb-find']
                if defect=='different-options':options+=['--memory-root',str(p/'different-vault')]
                result=call('install','--target',p,*options,ok=2)
                self.assertEqual(result['status'],'error')
                self.assertEqual(snapshot(p),before)


if __name__=='__main__':unittest.main()


class PatchUpgrade(unittest.TestCase):
    """A trusted 1.0.0 installation updates in place to the current release."""
    def test_actual_130_upgrade_adds_brain_and_policy_dependencies(self):
        for client, selection in [('codex', ['--profile', 'full']),
                                  ('claude', ['--skills', 'agent-sessions'])]:
            with self.subTest(client=client), target_directory() as release_dir, target_directory() as td:
                release, target = Path(release_dir), Path(td)
                with tarfile.open(fileobj=io.BytesIO(release_archive('df75cb8'))) as bundle:
                    bundle.extractall(release, filter='data')
                options = ['--client', client, '--target', str(target), *selection]
                entry = target / ('AGENTS.md' if client == 'codex' else 'CLAUDE.md')
                user_rules = b'# User rules\r\nPreserve this content.\r\n'
                entry.write_bytes(user_rules)
                old = subprocess.run([sys.executable, '-B', str(release/'harness.py'), 'install', *options],
                                     cwd=release, capture_output=True)
                self.assertEqual(old.returncode, 0, old.stderr.decode('utf8'))
                identity = hashlib.sha256((str(target.resolve())+'\n'+client).encode('utf8')).hexdigest()+'.json'
                trust = ROOT/'.harness-state/receipts'/identity
                trust.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(release/'.harness-state/receipts'/identity, trust)
                self.addCleanup(lambda p=trust: p.unlink(missing_ok=True))
                planned = call('plan', *options)
                self.assertIn('agent-sessions', planned['installed_skills'])
                upgraded = call('install', *options)
                self.assertEqual(upgraded['migration_from'], '1.3.0')
                self.assertEqual(upgraded['installed_skills'], planned['installed_skills'])
                self.assertTrue(entry.read_bytes().startswith(user_rules))
                self.assertEqual(call('verify', '--client', client, '--target', target)['status'], 'pass')
                # An explicit selection change is still refused before writes.
                before = snapshot(target)
                call('install', '--client', client, '--target', target, '--skills', 'kb-find', ok=2)
                self.assertEqual(snapshot(target), before)

    def test_actual_120_selected_workflow_upgrade_keeps_original_request(self):
        # --workflow also installs the full catalog, but requested_skills remains
        # the explicitly selected skill, rather than the full-profile selection.
        with target_directory() as release_dir,target_directory() as td:
            release=Path(release_dir);p=Path(td)
            with tarfile.open(fileobj=io.BytesIO(release_archive('9db2db7'))) as bundle:
                bundle.extractall(release,filter='data')
            self.assertEqual(json.loads((release/'manifest.json').read_text(encoding='utf8'))['version'],'1.2.0')
            options=['--client','codex','--target',str(p),'--skills','kb-find','--workflow']
            result=subprocess.run([sys.executable,'-B','-X','utf8',str(release/'harness.py'),'install',*options],cwd=release,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr.decode('utf8'))
            identity=hashlib.sha256((str(p.resolve())+'\ncodex').encode('utf8')).hexdigest()+'.json'
            trust=ROOT/'.harness-state/receipts'/identity
            trust.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(release/'.harness-state/receipts'/identity,trust)
            self.addCleanup(lambda:trust.unlink(missing_ok=True))
            upgraded=call('install',*options)
            self.assertEqual(upgraded['migration_from'],'1.2.0')
            receipt=json.loads((p/'.agents/harness-install.json').read_text(encoding='utf8'))
            self.assertEqual(receipt['requested_skills'],['kb-find'])
            self.assertIn('jam-board',upgraded['installed_skills'])
            self.assertEqual(call('verify','--client','codex','--target',p)['status'],'pass')

    def test_actual_100_full_upgrade_codex(self):
        with target_directory() as release_dir,target_directory() as td:
            release=Path(release_dir);p=Path(td)
            archive=release_archive('390a28b')
            with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:bundle.extractall(release,filter='data')
            self.assertEqual(json.loads((release/'manifest.json').read_text(encoding='utf8'))['version'],'1.0.0')
            result=subprocess.run([sys.executable,'-B','-X','utf8',str(release/'harness.py'),'install','--target',str(p),'--client','codex','--profile','full'],cwd=release,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr.decode('utf8'))
            identity=hashlib.sha256((str(p.resolve())+'\ncodex').encode('utf8')).hexdigest()+'.json'
            trust=ROOT/'.harness-state/receipts'/identity
            trust.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(release/'.harness-state/receipts'/identity,trust)
            self.addCleanup(lambda:trust.unlink(missing_ok=True))
            current=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))['version']
            upgraded=call('install','--client','codex','--target',p,'--profile','full')
            self.assertEqual(upgraded['migration_from'],'1.0.0')
            receipt=json.loads((p/'.agents/harness-install.json').read_text(encoding='utf8'))
            self.assertEqual(receipt['version'],current)
            self.assertEqual((p/'.agents/skills/agent-instructions/agents/openai.yaml').read_bytes(),(ROOT/'payload/skills/agent-instructions/agents/openai.yaml').read_bytes())
            self.assertEqual(call('verify','--client','codex','--target',p)['status'],'pass')
