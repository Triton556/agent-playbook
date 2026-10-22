"""Jam Board discovery, MCP vocabulary, links and an isolated real install."""
import json
import os
from pathlib import Path
import re
import tempfile
import unittest

from test_install import ROOT, call, target_directory

SKILL = ROOT / 'payload/skills/jam-board'
APP_DOC = Path(os.environ.get('JAM_BOARD_DOC_PATH', str(ROOT.parent / 'jam-board/docs/mcp.md')))
FIXTURE = ROOT / 'tests/fixtures/jam-board-tools.txt'


def parse_tools(document):
    # Bound the table: the readiness table also has snake_case entries.
    header = re.search(r'## Tool contract \((\d+) tools\)', document)
    if not header:
        raise AssertionError('Missing app tool contract table')
    count = int(header[1])
    table = document[header.end():].split('### Project and planning fields', 1)[0]
    names = re.findall(r'^\| ([a-z]+(?:_[a-z]+)+) \|', table, re.M)
    if len(names) != count or len(set(names)) != count:
        raise AssertionError(f'Expected {count} unique tools from the app contract')
    return set(names)


def fixture_tools():
    return {line for line in FIXTURE.read_text(encoding='utf8').splitlines() if line and not line.startswith('#')}


def relative_links(path):
    # Markdown links, excluding images/absolute/remote links. Return fragments too.
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^\s)]+)\)', path.read_text(encoding='utf8')):
        if not re.match(r'^[a-zA-Z][\w+.-]*:|^/', target):
            yield target


def check_relative_links(case, path):
    for target in relative_links(path):
        relative, _, fragment = target.partition('#')
        if relative.startswith('{{HARNESS_ROOT}}/'):
            # Source instructions bind AGENTS' deployed BASE-RULES filename.
            suffix = relative.removeprefix('{{HARNESS_ROOT}}/')
            dest = ROOT / 'payload' / ('AGENTS.md' if suffix == 'BASE-RULES.md' else suffix)
        else:
            dest = (path.parent / relative).resolve() if relative else path
        case.assertTrue(dest.is_file(), (path, target))
        if fragment:
            # GitHub-style heading anchors, including duplicate-heading suffixes.
            text = dest.read_text(encoding='utf8')
            slugs = []
            for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
                slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
                base = slug
                index = 0
                while slug in slugs:
                    index += 1
                    slug = f'{base}-{index}'
                slugs.append(slug)
            case.assertIn(fragment, slugs, (path, target))


class JamBoardSkill(unittest.TestCase):
    def test_catalog_description_and_profile_selections(self):
        catalog = call('catalog')
        skill = next(s for s in catalog['skills'] if s['name'] == 'jam-board')
        self.assertTrue(skill['description'])
        self.assertIn('Jam Board', skill['description'])
        required = {'jam-board', 'dev-flow', 'dev-plan', 'agent-sessions', 'agent-sessions-codex', 'you-are-brain'}
        with target_directory() as td:
            for profile in ['full', 'engineering', 'jam-board']:
                with self.subTest(profile=profile):
                    plan = call('plan', '--client', 'codex', '--profile', profile, '--target', td)
                    self.assertTrue(required <= set(plan['requested_skills']))
                    self.assertTrue(required <= set(plan['installed_skills']))
                    if profile == 'jam-board':
                        self.assertEqual(set(plan['requested_skills']), required)
                        self.assertFalse(plan['workflow_activated'])
            self.assertEqual(list(Path(td).iterdir()), [])

    def test_mcp_tool_names_and_example_json(self):
        # Prefer the current authoritative app contract when available; otherwise
        # use the generated portable fixture. Exercise both sources where possible.
        tools = parse_tools(APP_DOC.read_text(encoding='utf8')) if APP_DOC.is_file() else fixture_tools()
        self.assertEqual(len(fixture_tools()), 44)
        self.assertEqual(tools - {'wait_for_changes'}, fixture_tools() - {'wait_for_changes'})
        # Its presence is checked separately; an older checkout can still verify
        # the existing vocabulary while the new contract comparison is skipped.
        tools |= {'wait_for_changes'}
        used = set()
        for path in SKILL.rglob('*.md'):
            text = path.read_text(encoding='utf8')
            # Detect tool-shaped names in prose, tables, inline code and examples,
            # including misspellings, rather than intersecting with known names.
            candidates = set(re.findall(r'(?<![\w-])(?:get|list|create|update|set|become|check|mark|claim|release|submit|add|review|ask|wait_for|withdraw|move|archive|link|delete)_[a-z_]+', text))
            # Documented data field and error code, not tool invocations.
            candidates -= {'review_round', 'claim_conflict'}
            self.assertFalse(candidates - tools, (path, sorted(candidates - tools)))
            used |= candidates
            for name, raw in re.findall(r'^([a-z]+(?:_[a-z]+)+)\((\{.*\})\)$', text, re.M):
                self.assertIn(name, tools, path)
                args = json.loads(raw)
                self.assertIsInstance(args, dict)
                self.assertTrue(all('_' not in key for key in args), (path, name))
        self.assertTrue({'ask_user', 'check_ready', 'mark_ready', 'submit_report', 'review_task'} <= used)

    def test_wait_for_changes_contract_and_examples(self):
        if not APP_DOC.is_file() or 'wait_for_changes' not in parse_tools(APP_DOC.read_text(encoding='utf8')):
            self.skipTest('Pending contract: wait_for_changes absent from app docs/mcp.md')
        source = APP_DOC.read_text(encoding='utf8')
        section = source.split('### wait_for_changes', 1)[1].split('### Project and planning fields', 1)[0]
        examples = []
        for path in SKILL.rglob('*.md'):
            for raw in re.findall(r'^\s*wait_for_changes\((\{.*\})\)$', path.read_text(encoding='utf8'), re.M):
                args = json.loads(raw)
                self.assertEqual(set(args) - {'cursor', 'epicKey', 'includeProject', 'actions', 'actorKind', 'excludeSelf', 'timeoutSeconds'}, set())
                self.assertGreaterEqual(args['cursor'], 0)
                self.assertIn(args['timeoutSeconds'], range(1, 61))
                for action in args.get('actions', []):
                    self.assertIn(f'`{action}`', section)
                examples.append(args)
        self.assertTrue(examples, 'A real JSON tool-call example must be present')
        for key in ('events', 'nextCursor', 'timedOut', 'includeProject', 'excludeSelf'):
            self.assertIn(key, section)

    def test_relative_links_and_fragments(self):
        paths = list(SKILL.rglob('*.md'))
        self.assertEqual(len(paths), 5)
        for path in paths:
            with self.subTest(path=path):
                check_relative_links(self, path)

    @unittest.skipUnless(APP_DOC.is_file(), 'App checkout absent; connection source comparison unavailable')
    def test_connection_examples_are_verbatim_from_app(self):
        source = APP_DOC.read_text(encoding='utf8')
        expected = source[source.index('### Codex: stdio'):source.index('## Transports and authentication')]
        expected = expected.replace('(agent-playbook-compatibility.md)', '(https://github.com/Triton556/jam-board/blob/cf2e8fd03d5753a9ea316c9408e6da9f74f0cbc7/docs/agent-playbook-compatibility.md)')
        self.assertIn(expected, (SKILL / 'references/connect.md').read_text(encoding='utf8'))

    def test_codex_jam_board_profile_plan_install_verify_doctor(self):
        # Use an isolated project under the permitted repository test workspace.
        with target_directory() as td:
            target = Path(td).resolve()
            self.assertIn(ROOT.resolve(), target.parents)
            user_rules = b'# Existing project\r\nKeep this rule.\r\n'
            (target / 'AGENTS.md').write_bytes(user_rules)
            (target / 'user-file.txt').write_bytes(b'keep')
            common = ['--client', 'codex', '--profile', 'jam-board', '--target', target]
            planned = call('plan', *common)
            self.assertEqual((target / 'AGENTS.md').read_bytes(), user_rules)
            self.assertFalse((target / '.agents').exists())
            installed = call('install', *common)
            self.assertEqual(planned['installed_skills'], installed['installed_skills'])
            required = [
                'jam-board/SKILL.md', 'jam-board/references/brain-loop.md',
                'jam-board/references/worker-loop.md', 'jam-board/references/field-guide.md',
                'jam-board/references/connect.md', 'dev-flow/SKILL.md',
                'dev-flow/references/task-brief-and-acceptance.md', 'dev-plan/SKILL.md',
                'agent-sessions/SKILL.md', 'agent-sessions/references/requirements-interview.md',
                'agent-sessions/references/brief-writing.md', 'agent-sessions-codex/SKILL.md',
            ]
            for relative in required:
                self.assertTrue((target / '.agents/skills' / relative).is_file(), relative)
            self.assertTrue((target / '.agents/workflow/WORKFLOW.md').is_file())
            for path in (target / '.agents/skills/jam-board').rglob('*.md'):
                check_relative_links(self, path)
            inspection = ['--client', 'codex', '--target', target]
            self.assertEqual(call('verify', *inspection)['status'], 'pass')
            diagnosed = call('doctor', *inspection)
            self.assertEqual(diagnosed['instruction_integrity'], 'pass')
            self.assertEqual(diagnosed['status'], 'integrity-verified-runtime-unverified')
            self.assertEqual(diagnosed['quality_parity'], 'not-established')
            self.assertTrue((target / 'AGENTS.md').read_bytes().startswith(user_rules))
            self.assertEqual((target / 'user-file.txt').read_bytes(), b'keep')
            # A repeated install remains idempotent.
            entry = (target / 'AGENTS.md').read_bytes()
            call('install', *common)
            self.assertEqual((target / 'AGENTS.md').read_bytes(), entry)


if __name__ == '__main__':
    unittest.main()
