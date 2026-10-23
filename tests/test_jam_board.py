"""Core/Jam application boundary and real safe migration; no app or model calls."""
import hashlib
import io
import json
import subprocess
import sys
import tarfile
import unittest
from pathlib import Path

from test_install import ROOT, call, target_directory
from test_migration import release_archive, snapshot

BASELINE = '60317a3b83ef5bd9ef620a899bf95a099f7c926f'


class JamSeparation(unittest.TestCase):
    def test_core_catalog_manifest_and_dependencies_do_not_ship_jam(self):
        catalog = call('catalog')['skills']
        self.assertEqual(len(catalog), 11)
        self.assertNotIn('jam-board', {skill['name'] for skill in catalog})
        manifest = json.loads((ROOT/'manifest.json').read_text())
        self.assertFalse((ROOT/'payload/skills/jam-board').exists())
        self.assertFalse(any('skills/jam-board/' in row['path'] for row in manifest['files']))
        self.assertNotIn('jam-board', manifest['skill_dependencies'])
        self.assertFalse(any('jam-board' in names for names in manifest['skill_dependencies'].values()))
        self.assertFalse(any('jam-board' in names for names in manifest.get('support_modules', {}).values()))

    def test_retired_profile_and_skill_give_application_direction_without_writes(self):
        for command in ['plan', 'install']:
            for selector in ['--profile', '--skills']:
                with self.subTest(command=command, selector=selector), target_directory() as folder:
                    result = call(command, '--target', folder, selector, 'jam-board', ok=2)
                    self.assertEqual(result['status'], 'error')
                    self.assertIn('jam', result['message'].lower())
                    self.assertIn('app', result['message'].lower())
                    self.assertEqual(snapshot(Path(folder)), {})

    def test_full_engineering_and_brain_installations_have_no_jam_for_both_clients(self):
        for client, native in [('codex', '.agents'), ('claude', '.claude')]:
            for selection in [['--profile', 'full'], ['--profile', 'engineering'], ['--skills', 'you-are-brain']]:
                with self.subTest(client=client, selection=selection), target_directory() as folder:
                    target = Path(folder)
                    result = call('install', '--client', client, '--target', target, *selection)
                    self.assertNotIn('jam-board', result['installed_skills'])
                    self.assertFalse((target/native/'skills/jam-board').exists())
                    self.assertTrue((target/native/'skills/you-are-brain/SKILL.md').is_file())
                    self.assertTrue((target/native/'skills/agent-sessions/adapters/codex.mjs').is_file())
                    self.assertEqual(call('verify', '--client', client, '--target', target)['status'], 'pass')
                    if selection == ['--skills', 'you-are-brain']:
                        self.assertEqual(result['installed_skills'], ['you-are-brain'])
                        self.assertFalse((target/native/'skills/dev-plan/SKILL.md').exists())


class JamSeparationMigration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = target_directory()
        cls.legacy = Path(cls.context.__enter__())
        with tarfile.open(fileobj=io.BytesIO(release_archive(BASELINE))) as bundle:
            bundle.extractall(cls.legacy, filter='data')

    @classmethod
    def tearDownClass(cls):
        cls.context.__exit__(None, None, None)

    def install_old(self, target, client, profile="full"):
        run = subprocess.run([sys.executable, str(self.legacy/'harness.py'), 'install',
                              '--client', client, '--target', str(target), '--profile', profile],
                             cwd=self.legacy, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
        identity = hashlib.sha256((str(target.resolve())+'\n'+client).encode()).hexdigest()+'.json'
        destination = ROOT/'.harness-state/receipts'/identity
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((self.legacy/'.harness-state/receipts'/identity).read_bytes())
        self.addCleanup(lambda: destination.unlink(missing_ok=True))
        return json.loads((target/('.agents' if client == 'codex' else '.claude')/'harness-install.json').read_text())

    def test_upgrade_removes_unchanged_owned_jam_files_preserves_user_neighbors(self):
        for client, native, entry in [('codex', '.agents', 'AGENTS.md'), ('claude', '.claude', 'CLAUDE.md')]:
            with self.subTest(client=client), target_directory() as folder:
                target = Path(folder)
                user = b'# Project\r\nKeep my user rules.\r\n'
                (target/entry).write_bytes(user)
                old = self.install_old(target, client)
                neighbor = target/native/'skills/jam-board/user-notes.md'
                neighbor.write_bytes(b'Private integration notes')
                owned = [row for row in old['files'] if '/skills/jam-board/' in row['relative'] and row['owned']]
                self.assertTrue(owned)
                result = call('install', '--client', client, '--target', target, '--profile', 'full')
                self.assertEqual(result['migration_from'], '2.0.0')
                self.assertNotIn('jam-board', result['installed_skills'])
                for row in owned:
                    self.assertFalse((target/row['relative']).exists(), row['relative'])
                self.assertEqual(neighbor.read_bytes(), b'Private integration notes')
                self.assertTrue((target/entry).read_bytes().startswith(user))
                self.assertEqual(call('verify', '--client', client, '--target', target)['status'], 'pass')

    def test_engineering_profile_upgrade_normalizes_old_request_without_jam(self):
        for client, native in [('codex', '.agents'), ('claude', '.claude')]:
            with self.subTest(client=client), target_directory() as folder:
                target = Path(folder)
                old = self.install_old(target, client, profile='engineering')
                self.assertIn('jam-board', old['requested_skills'])
                planned = call('plan', '--client', client, '--target', target, '--profile', 'engineering')
                self.assertEqual(planned['migration_from'], '2.0.0')
                upgraded = call('install', '--client', client, '--target', target, '--profile', 'engineering')
                receipt = json.loads((target/native/'harness-install.json').read_text())
                self.assertEqual(receipt['requested_skills'], planned['requested_skills'])
                self.assertEqual(upgraded['installed_skills'], planned['installed_skills'])
                self.assertEqual(set(receipt['requested_skills']), {
                    'dev-plan', 'dev-debug', 'dev-verify',
                    'you-are-brain', 'agent-instructions',
                })
                self.assertFalse((target/native/'skills/jam-board').exists())
                self.assertTrue((target/native/'skills/agent-sessions/adapters/codex.mjs').is_file())
                self.assertEqual(call('verify', '--client', client, '--target', target)['status'], 'pass')

    def test_modified_jam_entry_or_reference_blocks_before_any_writes(self):
        for relative in ['SKILL.md', 'references/brain-loop.md']:
            for client, native in [('codex', '.agents'), ('claude', '.claude')]:
                with self.subTest(client=client, relative=relative), target_directory() as folder:
                    target = Path(folder)
                    self.install_old(target, client)
                    modified = target/native/'skills/jam-board'/relative
                    modified.write_text('My custom Jam integration instruction')
                    before = snapshot(target)
                    call('install', '--client', client, '--target', target, '--profile', 'full', ok=2)
                    self.assertEqual(snapshot(target), before)

    def test_unowned_jam_entry_is_preserved_after_upgrade_and_remove(self):
        for client, native in [('codex', '.agents'), ('claude', '.claude')]:
            with self.subTest(client=client), target_directory() as folder:
                target = Path(folder)
                unowned = target/native/'skills/jam-board/SKILL.md'
                unowned.parent.mkdir(parents=True)
                content = (self.legacy/'payload/skills/jam-board/SKILL.md').read_bytes().replace(
                    b'{{HARNESS_ROOT}}', (target/native).as_posix().encode()).replace(
                    b'{{MEMORY_ROOT}}', (target/'.harness-memory').as_posix().encode())
                self.assertNotIn(b'{{', content)
                unowned.write_bytes(content)
                old = self.install_old(target, client)
                self.assertFalse(next(row for row in old['files'] if row['relative'].endswith('/jam-board/SKILL.md'))['owned'])
                call('install', '--client', client, '--target', target, '--profile', 'full')
                self.assertEqual(unowned.read_bytes(), content)
                call('remove', '--client', client, '--target', target)
                self.assertEqual(unowned.read_bytes(), content)


if __name__ == '__main__':
    unittest.main()
