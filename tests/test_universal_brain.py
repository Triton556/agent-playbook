"""Generic orchestration and narrow deployment header: no board/private-domain policy."""
import re
import unittest
from pathlib import Path
from test_install import ROOT, call, target_directory
import harness


class UniversalBrain(unittest.TestCase):
    def test_brain_and_support_do_not_require_board_vocabulary(self):
        documents = list((ROOT/'payload/skills/you-are-brain').rglob('*.md'))
        for relative in ['agent-sessions/references', 'agent-sessions-codex/references']:
            documents += list((ROOT/'payload/skills'/relative).glob('*.md'))
        documents.append(ROOT/'payload/workflow/WORKFLOW.md')
        for document in documents:
            with self.subTest(path=str(document.relative_to(ROOT))):
                self.assertNotRegex(document.read_text().lower(), r'\b(epic|epics|story|stories|board|card|cards|jam-board)\b')
        self.assertTrue(documents)

    def test_installable_instructions_have_no_private_finance_or_lab_rules(self):
        pattern = re.compile(r'\b(financial|finances|testnet|refunds?|provider signature|lab access|laboratory access)\b', re.I)
        for document in (ROOT/'payload').rglob('*.md'):
            with self.subTest(path=str(document.relative_to(ROOT))):
                self.assertIsNone(pattern.search(document.read_text()))
        # A general quality ledger or a quoted demo named Lab is not a private policy.

    def test_startup_header_is_not_a_hidden_workflow_loader(self):
        root = Path('/example/project/.agents')
        block = harness.instructions_block('2.1.0', root, {'HARNESS_ROOT':str(root)}, True)
        body = (ROOT/'payload/AGENTS.md').read_text()
        self.assertIn(body, block)
        header = block.split(body, 1)[0]
        self.assertNotIn('Read policy', header)
        for retired_route in ['WORKFLOW.md', 'session-guide', 'jam-board', 'financial', 'lab access']:
            self.assertNotIn(retired_route, header)
        self.assertIn('not new permissions', header)
        self.assertIn("owner's actual authorization", header)

    def test_standalone_brain_install_has_no_board_dependency(self):
        with target_directory() as folder:
            target=Path(folder)
            result=call('install', '--client', 'codex', '--target', target, '--skills', 'you-are-brain')
            self.assertEqual(result['installed_skills'], ['you-are-brain'])
            self.assertFalse((target/'.agents/skills/jam-board').exists())
            self.assertTrue((target/'.agents/skills/agent-sessions/adapters/codex.mjs').is_file())
            self.assertEqual(call('verify', '--target', target)['status'], 'pass')


if __name__ == '__main__':
    unittest.main()
