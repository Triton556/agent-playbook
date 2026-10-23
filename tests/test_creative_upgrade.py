"""Real 2.0 -> current installation and creative conflict preservation; no model calls."""
import hashlib
import io
import subprocess
import sys
import tarfile
import unittest
from pathlib import Path

from test_install import ROOT, call, target_directory
from test_migration import release_archive, snapshot

BASELINE = '60317a3b83ef5bd9ef620a899bf95a099f7c926f'


class CreativeUpgrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = target_directory()
        cls.legacy = Path(cls.context.__enter__())
        with tarfile.open(fileobj=io.BytesIO(release_archive(BASELINE))) as bundle:
            bundle.extractall(cls.legacy, filter='data')

    @classmethod
    def tearDownClass(cls):
        cls.context.__exit__(None, None, None)

    def install_old(self, target, client):
        subprocess.run([sys.executable, str(self.legacy/'harness.py'), 'install',
                        '--profile', 'full', '--client', client,
                        '--target', str(target)], cwd=self.legacy,
                       capture_output=True, check=True)
        # Transfer the legitimate private receipt between these test checkouts.
        identity = hashlib.sha256((str(target.resolve())+'\n'+client).encode()).hexdigest()+'.json'
        source = self.legacy/'.harness-state/receipts'/identity
        destination = ROOT/'.harness-state/receipts'/identity
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        self.addCleanup(lambda: destination.unlink(missing_ok=True))

    def test_upgrade_replaces_owned_creative_preserves_user_content(self):
        for client, native, entry in [('codex', '.agents', 'AGENTS.md'),
                                      ('claude', '.claude', 'CLAUDE.md')]:
            with self.subTest(client=client), target_directory() as folder:
                target = Path(folder)
                original = b'# Project\r\nMy current accepted creative direction.\r\n'
                (target/entry).write_bytes(original)
                neighbor = target/'user-owned.txt'
                neighbor.write_bytes(b'Keep this work')
                self.install_old(target, client)
                result = call('install', '--profile', 'full',
                              '--client', client, '--target', target)
                self.assertEqual(result['migration_from'], '2.0.0')
                self.assertFalse((target/native/'skills/creative-direction/SKILL.md').exists())
                self.assertNotIn('creative-direction',result['installed_skills'])
                self.assertTrue((target/entry).read_bytes().startswith(original))
                self.assertEqual(neighbor.read_bytes(), b'Keep this work')
                self.assertEqual(call('verify', '--client', client, '--target', target)['status'], 'pass')

    def test_edited_creative_refuses_upgrade_before_any_writes(self):
        with target_directory() as folder:
            target = Path(folder)
            self.install_old(target, 'codex')
            edited = target/'.agents/skills/creative-direction/references/content.md'
            edited.write_text('User-owned creative guidance')
            before = snapshot(target)
            call('install', '--profile', 'full', '--target', target, ok=2)
            self.assertEqual(snapshot(target), before)


if __name__ == '__main__':
    unittest.main()
