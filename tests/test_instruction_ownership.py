"""Release invariants for policy placement, mirrored guides and installation."""
import re
from pathlib import Path
from urllib.parse import unquote
import unittest

from test_install import ROOT, call, target_directory, payload_bytes

def markdown_destinations(path):
    text = path.read_text(encoding='utf8')
    # Include images and example links; example project paths use literal code.
    for match in re.finditer(r'!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)', text):
        target = match[1].strip('<>')
        if re.match(r'^[a-zA-Z][\w+.-]*:|^/|^\{\{', target):
            continue
        relative, _, fragment = target.partition('#')
        yield (path.parent / unquote(relative)).resolve() if relative else path, unquote(fragment), target


def heading_ids(path):
    result = []
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', path.read_text(encoding='utf8'), re.M):
        base = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        slug, index = base, 0
        while slug in result:
            index += 1
            slug = f'{base}-{index}'
        result.append(slug)
    return result


class InstructionOwnership(unittest.TestCase):
    def test_you_are_brain_standalone_install_both_clients(self):
        for client, native in [('codex', '.agents'), ('claude', '.claude')]:
            with self.subTest(client=client), target_directory() as folder:
                target = Path(folder)
                before = b'# User instructions\r\nKeep this content.\r\n'
                entry = target / ('AGENTS.md' if client == 'codex' else 'CLAUDE.md')
                entry.write_bytes(before)
                args = ['--client', client, '--target', target, '--skills', 'you-are-brain']
                plan = call('plan', *args)
                self.assertEqual(plan['requested_skills'], ['you-are-brain'])
                self.assertEqual(set(plan['installed_skills']), {
                    'you-are-brain',
                })
                result = call('install', *args)
                self.assertEqual(result['installed_skills'], plan['installed_skills'])
                self.assertFalse(result['workflow_activated'])
                for name in ['SKILL.md', 'references/brain-profile.md', 'references/setup-interview.md']:
                    self.assertEqual(
                        payload_bytes('payload/skills/you-are-brain/'+name,target,client),
                        (target / native / 'skills/you-are-brain' / name).read_bytes(),
                    )
                self.assertTrue(entry.read_bytes().startswith(before))
                self.assertEqual(call('verify', '--client', client, '--target', target)['status'], 'pass')
                for path in (target / native / 'skills').rglob('*.md'):
                    for destination, fragment, raw in markdown_destinations(path):
                        self.assertTrue(destination.exists(), (path, raw))
                self.assertFalse((target / native / 'BASE-RULES.md').exists())
                self.assertIn("# The user's working rules", entry.read_text(encoding='utf8'))

    def test_every_relative_payload_markdown_destination_exists(self):
        checked = 0
        for path in (ROOT / 'payload').rglob('*.md'):
            # Memory runtime documents are copied from the live vault and link to vault-only files.
            if 'memory' in path.relative_to(ROOT / 'payload').parts[:2]:
                continue
            for destination, fragment, raw in markdown_destinations(path):
                with self.subTest(source=str(path.relative_to(ROOT)), link=raw):
                    self.assertTrue(destination.exists(), str(destination))
                checked += 1
        self.assertGreater(checked, 0, 'The link check must inspect the active payload')

    def test_owned_instruction_fragments_resolve(self):
        # Third-party reference bodies remain intact; validate active local anchors.
        for path in (ROOT / 'payload').rglob('*.md'):
            if {'vendor', 'data', 'licenses'} & set(path.parts):
                continue
            for destination, fragment, raw in markdown_destinations(path):
                if fragment and destination.is_file() and destination.suffix == '.md':
                    with self.subTest(source=str(path.relative_to(ROOT)), link=raw):
                        self.assertIn(fragment, heading_ids(destination))

    def test_recipient_language_channels_and_continuation(self):
        base = (ROOT / 'payload/AGENTS.md').read_text(encoding='utf8')
        owner = (ROOT / 'payload/skills/agent-sessions/references/brief-writing.md').read_text(encoding='utf8')
        language = owner.split('## Language\n', 1)[1].split('## Form\n', 1)[0]
        for channel in ['briefs and follow-ups', 'commentary', 'progress updates', 'questions', 'final responses', 'written reports']:
            self.assertIn(channel, language)
        self.assertIn('intended recipient, not by who can view the session', language)
        self.assertIn('recipient is the orchestrator unless the current user instruction explicitly addresses a particular output directly to the user', language)
        self.assertIn('On continuation, retain that assignment unless the current user instruction changes it', language)
        template = owner.split('## Template\n', 1)[1].split('```markdown\n', 1)[1].split('\n```', 1)[0]
        self.assertLess(template.index('## Audience and language'), template.index('## Goal'))
        self.assertIn('delegated worker addressing the agent orchestrator', template)
        self.assertIn('the final response and the written report', template)
        self.assertIn('name each deliverable and its required language', template)
        # Even a handoff consisting only of a report link remains a final response
        # to the orchestrator; a separate report's language cannot exempt it.
        self.assertIn('final responses', language)
        self.assertIn('does not change the surrounding message or report to the orchestrator', language)
        self.assertIn('Communicate directly with the user in Russian and write knowledge-base content in Russian', base)
        self.assertIn('unless the user requests another language', base)
        self.assertNotIn('brief-writing.md', base)  # BASE has no indirect language-policy expansion.
        self.assertIn('Preserve exact source quotations, identifiers, paths, commands and required product text in their original language', language)
        self.assertIn('Mark quotations as quotations', language)
        # Preservation and deliverable language are policy, not a dependency
        # on a particular fictional example remaining in the guide.
        self.assertIn('Preserve exact quotations, identifiers and required product text', template)
        self.assertIn('Write interface text, documents and other user-facing deliverables in the language specified for that output', language)
        self.assertNotRegex(language.lower(), r'(ban|forbid|reject).*cyrillic|automatic.*(translat|detect)')

    def test_language_owner_installed_for_orchestration_selections(self):
        # Exercise actual selection/rendering, both clients, full and standalone.
        for client, native in [('codex', '.agents'), ('claude', '.claude')]:
            for selection in [('profile', 'full'), ('skills', 'agent-sessions'), ('skills', 'you-are-brain')]:
                with self.subTest(client=client, selection=selection), target_directory() as folder:
                    target = Path(folder)
                    entry = target / ('AGENTS.md' if client == 'codex' else 'CLAUDE.md')
                    before = b'# User instructions\r\nKeep this content.\r\n'
                    entry.write_bytes(before)
                    neighbor = target / 'user-owned.txt'
                    neighbor.write_bytes(b'Unrelated user file\r\n')
                    args = ['--client', client, '--target', target, '--'+selection[0], selection[1]]
                    planned = call('plan', *args)
                    result = call('install', *args)
                    self.assertEqual(planned['installed_skills'], result['installed_skills'])
                    if selection[0] == 'profile':
                        self.assertEqual(len(result['installed_skills']), 7)
                    else:
                        expected = {'you-are-brain'}
                        self.assertEqual(set(result['installed_skills']), expected)
                    installed = target / native
                    base = entry.read_text(encoding='utf8')
                    owner = installed / 'skills/agent-sessions/references/brief-writing.md'
                    self.assertNotIn(owner.as_posix()+'#language', base)
                    self.assertIn('## Audience and language', owner.read_text(encoding='utf8'))
                    self.assertFalse((installed / 'BASE-RULES.md').exists())
                    for path in [owner, installed / 'skills/agent-sessions/references/running-and-checking.md', installed / 'skills/agent-sessions/references/session-guide.md']:
                        for destination, fragment, raw in markdown_destinations(path):
                            if destination.exists():
                                if fragment and destination.suffix == '.md':
                                    self.assertIn(fragment, heading_ids(destination))
                            else:
                                relative = destination.relative_to(installed)
                                source = ROOT / 'payload' / relative
                                self.assertTrue(source.exists(), (path, raw))
                                self.assertEqual(relative.parts[0], 'skills')
                                self.assertNotIn(relative.parts[1], result['installed_skills'])
                                if fragment and source.suffix == '.md':
                                    self.assertIn(fragment, heading_ids(source))
                    self.assertEqual(call('verify', '--client', client, '--target', target)['status'], 'pass')
                    doctor = call('doctor', '--client', client, '--target', target)
                    self.assertEqual(doctor['instruction_integrity'], 'pass')
                    self.assertEqual(doctor['status'], 'integrity-verified-runtime-unverified')
                    self.assertTrue(entry.read_bytes().startswith(before))
                    self.assertEqual(neighbor.read_bytes(), b'Unrelated user file\r\n')


if __name__ == '__main__':
    unittest.main()
