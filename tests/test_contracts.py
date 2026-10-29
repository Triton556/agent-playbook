"""3.0 package contracts and real preflight-helper behavior, not model compliance."""
import json
import os
import re
import struct
import subprocess
import sys
import unittest
import zlib
from pathlib import Path

from test_install import ROOT, target_directory


class VoxelPassportBehavior(unittest.TestCase):
    """Synthetic images exercise schema/metadata gate only; not visual quality."""
    SCRIPT = ROOT/'payload/skills/voxel-models/scripts/design_preflight.py'

    def helper(self, target, command, expected=0, review=True):
        args = [sys.executable, str(self.SCRIPT), command, '--root', str(target), '--passport', 'passport.json']
        if review and command == 'validate':
            args += ['--review', 'review.json']
        result = subprocess.run(args, capture_output=True, text=True, encoding='utf8', env={**os.environ, 'PYTHONUTF8': '1'})
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
    def test_base_rules_are_short_and_self_contained(self):
        text = (ROOT/'payload/AGENTS.md').read_text(encoding='utf8')
        bullets = [line for line in text.splitlines() if line.startswith('- ')]
        self.assertEqual(len(bullets), 6)
        self.assertIn('not as passed', text)
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

    def test_skills_are_minimal_and_kb_entries_are_self_contained(self):
        skills = sorted(p.parent.name for p in (ROOT/'payload/skills').glob('*/SKILL.md'))
        self.assertEqual(skills, ['kb-curate', 'kb-find', 'kb-save', 'kb-status', 'kb-sync', 'voxel-models', 'you-are-brain'])
        for name in [s for s in skills if s.startswith('kb-')]:
            with self.subTest(skill=name):
                folder = ROOT/'payload/skills'/name
                self.assertEqual([p.name for p in folder.iterdir()], ['SKILL.md'])
                self.assertNotRegex(folder.joinpath('SKILL.md').read_text(encoding='utf8'), r'\]\((?!https?:)')
        for gone in ['dev-flow', 'visual-scenes', 'kb-common', 'agent-sessions-codex', 'agent-instructions']:
            self.assertFalse((ROOT/'payload/skills'/gone).exists(), gone)
        self.assertFalse(list((ROOT/'payload').rglob('BASE-RULES.md')))
        self.assertFalse((ROOT/'payload/workflow/WORKFLOW.md').exists())

    def test_kb_writer_uses_the_vault_runtime(self):
        text = (ROOT/'payload/workflow/kb-writer.mjs').read_text(encoding='utf8')
        self.assertIn("path.join(VAULT,'SYSTEM/scripts/kb.mjs')", text)
        self.assertNotIn('../runtime/memory', text)
        template = (ROOT/'payload/runtime/integrations/codex-kb-writer.template.toml').read_text(encoding='utf8')
        self.assertIn('HARNESS_KB_ROOT = "{{MEMORY_ROOT}}"', template)
        self.assertTrue((ROOT/'payload/runtime/memory/SYSTEM/scripts/kb-claude.mjs').is_file())


if __name__ == '__main__':
    unittest.main()
