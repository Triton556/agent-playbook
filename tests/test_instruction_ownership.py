"""Release invariants for policy placement, mirrored guides and installation."""
import re
from pathlib import Path
from urllib.parse import unquote
import unittest

from test_install import ROOT, call, target_directory, payload_bytes

MIRRORS = {
    'payload/skills/agent-sessions-codex/references/' + name:
    'payload/skills/agent-sessions/references/' + name
    for name in ('requirements-interview.md', 'brief-writing.md', 'running-and-checking.md')
}


def owned_rules():
    document = (ROOT / 'docs/INSTRUCTION_MAINTENANCE.md').read_text(encoding='utf8')
    return re.findall(
        r'^\| ([^|]+?) \| \[(payload/[^#]+)#([^\]]+)\]\([^)]*\) \| '+chr(96)+r'([^'+chr(96)+r']+)'+chr(96)+r' \|$',
        document, re.M,
    )


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
    def test_each_map_rule_has_one_policy_owner(self):
        rules = owned_rules()
        self.assertEqual(len(rules), 16, 'Every ownership-map rule needs a sentinel')
        self.assertEqual(len({row[0] for row in rules}), len(rules))
        instructions = {
            p.relative_to(ROOT).as_posix(): p.read_text(encoding='utf8')
            for p in (ROOT / 'payload').rglob('*.md')
            if not {'vendor', 'data', 'licenses'} & set(p.parts)
            and p.relative_to(ROOT).as_posix() not in MIRRORS
        }
        for topic, owner, section, phrase in rules:
            with self.subTest(topic=topic):
                self.assertIn(section, heading_ids(ROOT / owner))
                found = {path: text.count(phrase) for path, text in instructions.items() if phrase in text}
                self.assertEqual(found, {owner: 1})

    def test_all_three_shared_references_are_identical(self):
        for mirror, owner in MIRRORS.items():
            with self.subTest(reference=owner):
                self.assertEqual((ROOT / mirror).read_bytes(), (ROOT / owner).read_bytes())
        running = (ROOT / MIRRORS['payload/skills/agent-sessions-codex/references/running-and-checking.md']).read_text(encoding='utf8')
        self.assertIn('## Status updates', running)
        self.assertIn('## Questions and blocked workers', running)

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
                self.assertIn('agent-sessions', plan['installed_skills'])
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
                # AGENTS.md is installed as BASE-RULES.md, and its body is also
                # inlined at project root. Source-relative AGENTS links fail here.
                for path in (target / native / 'skills').rglob('*.md'):
                    for destination, fragment, raw in markdown_destinations(path):
                        self.assertTrue(destination.exists(), (path, raw))
                text = (target / native / 'skills/you-are-brain/SKILL.md').read_text(encoding='utf8')
                self.assertIn((target / native / 'BASE-RULES.md').as_posix(), text)

    def test_every_relative_payload_markdown_destination_exists(self):
        checked = 0
        for path in (ROOT / 'payload').rglob('*.md'):
            for destination, fragment, raw in markdown_destinations(path):
                with self.subTest(source=str(path.relative_to(ROOT)), link=raw):
                    self.assertTrue(destination.exists(), str(destination))
                checked += 1
        self.assertGreater(checked, 330)

    def test_owned_instruction_fragments_resolve(self):
        # Third-party reference bodies remain intact; validate active local anchors.
        for path in (ROOT / 'payload').rglob('*.md'):
            if {'vendor', 'data', 'licenses'} & set(path.parts):
                continue
            for destination, fragment, raw in markdown_destinations(path):
                if fragment and destination.is_file() and destination.suffix == '.md':
                    with self.subTest(source=str(path.relative_to(ROOT)), link=raw):
                        self.assertIn(fragment, heading_ids(destination))


if __name__ == '__main__':
    unittest.main()
