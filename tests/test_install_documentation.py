"""Current install guidance resolves to the delivered unified entry and references."""
import unittest
from pathlib import Path
from test_install import ROOT, call, target_directory
from test_instruction_ownership import markdown_destinations, heading_ids


class InstallDocumentation(unittest.TestCase):
    def test_current_installation_links_and_entry_names(self):
        for name in ('INSTALL_FOR_AGENTS.md', 'docs/INTEGRATIONS.md', 'docs/COMPATIBILITY.md'):
            document = ROOT/name
            for target, fragment, raw in markdown_destinations(document):
                with self.subTest(document=name, link=raw):
                    self.assertTrue(target.exists(), raw)
                    if fragment and target.suffix == '.md':
                        self.assertIn(fragment, heading_ids(target))
            text = document.read_text()
            self.assertNotIn('skills/agent-sessions-codex/SKILL.md', text)
            self.assertNotIn('ui-design/ui-review', text)
        integration = (ROOT/'docs/INTEGRATIONS.md').read_text()
        self.assertIn('--skills you-are-brain', integration)
        self.assertNotIn('--skills agent-sessions-codex', integration)

    def test_documented_brain_route_delivers_actual_entry_and_driver_reference(self):
        for client, native in [('codex', '.agents'), ('claude', '.claude')]:
            with self.subTest(client=client), target_directory() as folder:
                target = Path(folder)
                installed = call('install', '--client', client, '--target', target,
                                 '--skills', 'you-are-brain')
                self.assertEqual(installed['installed_skills'], ['you-are-brain'])
                self.assertTrue((target/native/'skills/you-are-brain/SKILL.md').is_file())
                self.assertTrue((target/native/'skills/agent-sessions-codex/references/codex-driver.md').is_file())
                self.assertFalse((target/native/'skills/agent-sessions-codex/SKILL.md').exists())
                self.assertEqual(call('verify', '--client', client, '--target', target)['status'], 'pass')


if __name__ == '__main__':
    unittest.main()
