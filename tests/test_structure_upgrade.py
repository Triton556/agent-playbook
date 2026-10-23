"""2.1 installation/migration and real preflight-helper behavior, not model compliance."""
import hashlib
import io
import json
import shutil
import struct
import subprocess
import sys
import tarfile
import unittest
import zlib
from pathlib import Path

from test_install import ROOT, call, target_directory
from test_migration import release_archive, snapshot

BASELINE = '60317a3b83ef5bd9ef620a899bf95a099f7c926f'
RETIRED = {'agent-sessions', 'agent-sessions-codex', 'dev-flow', 'ui-review', 'visual-scenes', 'dev-implement'}


class StructureUpgrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = target_directory()
        cls.legacy = Path(cls.context.__enter__())
        with tarfile.open(fileobj=io.BytesIO(release_archive(BASELINE))) as bundle:
            bundle.extractall(cls.legacy, filter='data')

    @classmethod
    def tearDownClass(cls):
        cls.context.__exit__(None, None, None)

    def old_install(self, target, client, selection):
        subprocess.run([sys.executable, str(self.legacy/'harness.py'), 'install',
                        '--client', client, '--target', str(target), *selection],
                       cwd=self.legacy, capture_output=True, check=True)
        identity = hashlib.sha256((str(target.resolve())+'\n'+client).encode()).hexdigest()+'.json'
        destination = ROOT/'.harness-state/receipts'/identity
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((self.legacy/'.harness-state/receipts'/identity).read_bytes())
        self.addCleanup(lambda: destination.unlink(missing_ok=True))

    def test_full_upgrade_removes_owned_entrypoints_not_drivers_or_user_files(self):
        for client, native, entry in [('codex', '.agents', 'AGENTS.md'), ('claude', '.claude', 'CLAUDE.md')]:
            with self.subTest(client=client), target_directory() as folder:
                target = Path(folder)
                user = b'# User rules\r\nMy chosen project behavior.\r\n'
                (target/entry).write_bytes(user)
                self.old_install(target, client, ['--profile', 'full'])
                note = target/native/'skills/agent-sessions/user-note.txt'
                note.write_bytes(b'Private note retained')
                result = call('install', '--client', client, '--target', target, '--profile', 'full')
                self.assertEqual(result['migration_from'], '2.0.0')
                self.assertEqual(len(result['installed_skills']), 11)
                self.assertTrue(RETIRED.isdisjoint(result['installed_skills']))
                for name in RETIRED:
                    self.assertFalse((target/native/'skills'/name/'SKILL.md').exists(), name)
                for relative in ['agent-sessions/adapters/codex.mjs', 'agent-sessions/adapters/claude-code.mjs',
                                 'agent-sessions/adapters/wait.mjs', 'agent-sessions/adapters/run-runtime.mjs',
                                 'agent-sessions-codex/scripts/codex-chat.mjs']:
                    self.assertEqual((target/native/'skills'/relative).read_bytes(),
                                     (self.legacy/'payload/skills'/relative).read_bytes(), relative)
                self.assertEqual(note.read_bytes(), b'Private note retained')
                self.assertTrue((target/entry).read_bytes().startswith(user))
                self.assertEqual(call('verify', '--client', client, '--target', target)['status'], 'pass')
                after = snapshot(target)
                call('install', '--client', client, '--target', target, '--profile', 'full')
                self.assertEqual(snapshot(target), after)

    def test_unowned_retired_entrypoint_is_preserved_not_reclassified(self):
        with target_directory() as folder:
            target = Path(folder)
            unowned = target/'.agents/skills/visual-scenes/SKILL.md'
            unowned.parent.mkdir(parents=True)
            original = (self.legacy/'payload/skills/visual-scenes/SKILL.md').read_bytes().replace(
                b'{{HARNESS_ROOT}}', (target/'.agents').as_posix().encode()).replace(
                b'{{MEMORY_ROOT}}', (target/'.harness-memory').as_posix().encode())
            self.assertNotIn(b'{{', original)
            unowned.write_bytes(original)
            self.old_install(target, 'codex', ['--profile', 'full'])
            receipt = json.loads((target/'.agents/harness-install.json').read_text())
            self.assertFalse(next(row for row in receipt['files'] if row['relative'].endswith('/visual-scenes/SKILL.md'))['owned'])
            call('install', '--target', target, '--profile', 'full')
            self.assertEqual(unowned.read_bytes(), original)
            call('remove', '--target', target)
            self.assertEqual(unowned.read_bytes(), original)

    def test_old_ui_review_selection_is_retired(self):
        with target_directory() as folder:
            target = Path(folder)
            self.old_install(target, 'codex', ['--skills', 'ui-review'])
            before=snapshot(target)
            call('install', '--target', target, '--skills', 'ui-review',ok=2)
            self.assertEqual(snapshot(target),before)

    def test_changed_retired_entrypoint_blocks_upgrade_without_any_writes(self):
        for name in RETIRED:
            with self.subTest(skill=name), target_directory() as folder:
                target = Path(folder)
                self.old_install(target, 'codex', ['--profile', 'full'])
                (target/'.agents/skills'/name/'SKILL.md').write_text('User changed this instruction')
                before = snapshot(target)
                call('install', '--target', target, '--profile', 'full', ok=2)
                self.assertEqual(snapshot(target), before)

    def test_old_session_selection_upgrades_to_brain_without_unrelated_skill_catalog(self):
        for old in ['agent-sessions', 'agent-sessions-codex']:
            with self.subTest(old=old), target_directory() as folder:
                target = Path(folder)
                self.old_install(target, 'codex', ['--skills', old])
                result = call('install', '--target', target, '--skills', old)
                self.assertEqual(result['installed_skills'], ['you-are-brain'])
                entries = {p.parent.name for p in (target/'.agents/skills').glob('*/SKILL.md')}
                self.assertEqual(entries, {'you-are-brain'})
                self.assertTrue((target/'.agents/skills/agent-sessions/adapters/codex.mjs').is_file())
                self.assertEqual(call('verify', '--target', target)['status'], 'pass')

    def test_verification_does_not_install_a_design_bundle(self):
        with target_directory() as folder:
            target = Path(folder)
            result = call('install', '--target', target, '--skills', 'dev-verify')
            self.assertEqual(result['installed_skills'], ['dev-verify'])
            for name in ['ui-design','ui-review','creative-direction']:
                self.assertFalse((target/'.agents/skills'/name).exists())
            self.assertEqual(call('verify', '--target', target)['status'], 'pass')

    def test_retired_switches_refuse_without_replacement_or_writes(self):
        for skill in ['dev-flow', 'product-engineering', 'visual-scenes', 'visual-experiment-craft', 'dev-implement', 'product-implementation']:
            with self.subTest(skill=skill), target_directory() as folder:
                call('install', '--target', folder, '--skills', skill, ok=2)
                self.assertEqual(snapshot(Path(folder)), {})

    def test_installed_brain_adapter_describe_is_real_no_model_launch(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('Node unavailable')
        with target_directory() as folder:
            target = Path(folder)
            call('install', '--target', target, '--skills', 'you-are-brain')
            script = target/'.agents/skills/agent-sessions/adapters/codex.mjs'
            run = subprocess.run([node, str(script), '--describe'], capture_output=True, text=True, cwd=target)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['agent'], 'codex')


    def test_license_notices_are_preserved_while_voxel_asset_gate_is_removed(self):
        # Attribution files are package data, not a prompt instruction to inspect asset terms.
        notices = [p for p in (self.legacy/'payload').rglob('*') if p.is_file()
                   and ('license' in p.name.lower() or 'notice' in p.name.lower())]
        self.assertTrue(notices)
        for old in notices:
            current = ROOT/old.relative_to(self.legacy)
            if not current.exists() and old.parent.name=="licenses":
                current=ROOT/"docs/retired-attribution"/old.parent.parent.name/old.name
            self.assertTrue(current.is_file(), str(current))
            self.assertEqual(current.read_bytes(), old.read_bytes(), str(current))
        entry = (ROOT/'payload/skills/voxel-models/SKILL.md').read_text().lower()
        self.assertNotIn('reuse rights:', entry)
        self.assertNotIn('noai', entry)
        self.assertNotIn('view-only', entry)
        self.assertNotIn('license', entry)
        preflight = (ROOT/'payload/skills/voxel-models/references/design-preflight.md').read_text()
        self.assertIn('front, back, left, right, top and bottom', preflight)
        self.assertIn('six actual inspectable views exist', preflight)
        self.assertIn('design_preflight.py', preflight)


class VoxelPassportBehavior(unittest.TestCase):
    """Synthetic images exercise schema/metadata gate only; not visual quality."""
    SCRIPT = ROOT/'payload/skills/voxel-models/scripts/design_preflight.py'

    def helper(self, target, command, expected=0, review=True):
        args = [sys.executable, str(self.SCRIPT), command, '--root', str(target), '--passport', 'passport.json']
        if review and command == 'validate':
            args += ['--review', 'review.json']
        result = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout+result.stderr)
        return json.loads(result.stdout)

    def fixture(self, target):
        def chunk(kind, data):
            return struct.pack('>I', len(data))+kind+data+struct.pack('>I', zlib.crc32(kind+data)&0xffffffff)
        png = b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('>IIBBBBB',480,480,8,2,0,0,0))+chunk(b'IDAT', zlib.compress((b'\x00'+b'\xff\xff\xff'*480)*480))+chunk(b'IEND', b'')
        (target/'basis.txt').write_text('Synthetic cube geometry and authored six-view fixture, not inspected art.')
        views = {}
        for name in ['front','back','left','right','top','bottom']:
            (target/(name+'.png')).write_bytes(png)
            views[name] = {'path':name+'.png','projection':'orthographic','pose':'rest','pixels_per_meter':480,
                           'span_m':[1,1],'landmarks_2d_m':{'origin':[0,0]}}
        passport = {'schema_version':1,'asset':{'id':'synthetic-cube','dimensions_m':[1,1,1],'master_pitch_m':0.1,
                    'origin_m':[0,0,0],'ground_z_m':0,'pose':'rest','forward':'-Y','up':'+Z',
                    'style_features':['cube'],'context':'synthetic test','intended_use':'schema check'},
                    'basis':[{'path':'basis.txt','observations':'Synthetic fixture only'}],
                    'critical_features':[{'id':'cube','basis':[0],'check':'unit dimensions'}],
                    'landmarks_m':{'origin':[0,0,0]},'views':views,'kit':{'mode':'standalone'}}
        self.write_passport(target, passport)
        self.review(target)
        return passport

    def write_passport(self, target, passport):
        (target/'passport.json').write_text(json.dumps(passport))

    def review(self, target):
        digest = self.helper(target, 'snapshot')['input_digest']
        record = {'schema_version':1,'input_digest':digest,'reviewer':{'kind':'agent','name':'synthetic-fixture'},
                  'observed_at':'2026-10-23T00:00:00+00:00','inspected':True,
                  'gates':{k:{'verdict':'pass','observation':'Synthetic attestation, no visual-quality claim'} for k in
                           ['coherence','style','context','function','readability','usability']}}
        (target/'review.json').write_text(json.dumps(record))

    def test_six_views_pass_metadata_gate_five_views_do_not(self):
        with target_directory() as folder:
            target = Path(folder)
            passport = self.fixture(target)
            self.assertTrue(self.helper(target, 'validate')['ready_to_voxelize'])
            del passport['views']['bottom']
            self.write_passport(target, passport)
            self.review(target)
            result = self.helper(target, 'validate', expected=2)
            self.assertIn('six named orthographic views required', result['blockers'])

    def test_missing_passport_or_stale_review_does_not_pass(self):
        with target_directory() as folder:
            target = Path(folder)
            passport = self.fixture(target)
            passport['asset']['pose'] = 'changed'
            self.write_passport(target, passport)
            self.assertIn('design review absent or stale', self.helper(target, 'validate', expected=2)['blockers'])
            (target/'passport.json').unlink()
            self.assertFalse(self.helper(target, 'validate', expected=1)['ready_to_voxelize'])


class InstructionRouteContracts(unittest.TestCase):
    """Document contract regressions only: do not establish that a model obeys them."""
    def test_base_has_only_four_rules_without_reference_expansion(self):
        text = (ROOT/'payload/AGENTS.md').read_text()
        bullets = [line for line in text.splitlines() if line.startswith('- ')]
        self.assertEqual(bullets, [
            '- Communicate directly with the user in Russian and write knowledge-base content in Russian, unless the user requests another language.',
            '- Distinguish verified facts, assumptions and unknowns.',
            '- Commit, push and publication require the user’s request for that action in the current task.',
            '- Finish with the result, what was verified and any remaining limitations.',
        ])
        self.assertNotIn('](', text)
        self.assertNotIn('{{', text)

    def test_brain_has_distinct_continuation_setup_and_execution_routes(self):
        text = (ROOT/'payload/skills/you-are-brain/SKILL.md').read_text()
        rows = [line.split('|')[1:-1] for line in text.splitlines() if line.startswith('| ') and '---' not in line]
        routes = {row[0].strip(): ' '.join(row[1:]).strip() for row in rows}
        continuation = routes['Continuing a task or recovering context']
        self.assertIn('worker IDs', continuation)
        self.assertIn('setup', continuation.lower())
        self.assertIn('First setup, or the user changes client/model/route', routes)
        self.assertIn('Launching a native worker', routes)
        self.assertIn('Launching or resuming an external CLI worker', routes)
        self.assertIn('Do not load external-adapter commands', routes['Launching a native worker'])
        self.assertIn('reported startup blocker', routes['Launching or resuming an external CLI worker'])

    def test_verification_keeps_only_direct_user_scenario_check(self):
        text = (ROOT/'payload/skills/dev-verify/SKILL.md').read_text()
        self.assertIn('Execute the changed user scenario',text)
        self.assertIn('open affected dialogs/menus',text)
        self.assertIn('visible result and readability',text)
        for removed in ['ui-design','creative-direction']:
            self.assertNotIn(removed,text)
            self.assertFalse((ROOT/'payload/skills'/removed/'SKILL.md').exists())


if __name__ == '__main__':
    unittest.main()
