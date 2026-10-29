"""Read-only host evidence and adapter launch boundaries; no real model calls."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest

from test_install import ROOT, call, target_directory

NODE = shutil.which('node')
ADAPTERS = ROOT / 'payload/skills/agent-sessions/adapters'


@unittest.skipUnless(NODE, 'Node required for orchestration checks')
class Orchestration(unittest.TestCase):
    def run_node(self, script, *args, input=None, env=None, code=0):
        result = subprocess.run([NODE, str(script), *map(str, args)], input=input,
                                env=env, capture_output=True, text=True, encoding='utf8', timeout=12)
        self.assertEqual(result.returncode, code, (result.stdout, result.stderr))
        return result

    def write_json(self, file, value):
        file.write_text(json.dumps(value, ensure_ascii=False), encoding='utf8')
        return file

    def assignment(self, folder, **changes):
        value = {'recipient': 'orchestrator', 'communication_language': 'en',
                 'deliverables': [{'name': 'UI', 'language': 'ru'}],
                 'memory_writer': 'orchestrator', 'scope': 'Only the approved fixture'}
        value.update(changes)
        return self.write_json(folder / 'assignment.json', value)

    def evidence(self, folder, native=False, role='developer'):
        text = ('<multi_agent_role>Native team</multi_agent_role>'
                '<multi_agent_mode>Proactive delegation active.</multi_agent_mode>') if native else 'Local client instructions'
        return self.write_json(folder / 'host.json', [
            {'type': 'message', 'role': 'developer', 'content': [{'type': 'input_text', 'text': 'Base'}]},
            {'type': 'message', 'role': role, 'content': [{'type': 'input_text', 'text': text}]},
        ])

    def stub(self, folder, fail_first=False):
        script = folder / 'codex-stub.cjs'
        script.write_text('''
const fs=require('fs'),readline=require('readline');
fs.appendFileSync(process.env.RPC_LOG, JSON.stringify({spawn:process.argv.slice(2)})+'\\n');
readline.createInterface({input:process.stdin}).on('line',line=>{
 const m=JSON.parse(line);
 fs.appendFileSync(process.env.RPC_LOG,JSON.stringify(m)+'\\n');
 if(m.id===undefined)return;
 const result=m.method==='thread/start'?{thread:{id:'original-thread'}}:
   m.method==='turn/start'?{turn:{id:'turn'}}:{};
 console.log(JSON.stringify({id:m.id,result}));
 if(m.method==='turn/start'&&process.env.FAIL_FIRST_TURN==='1'&&!fs.existsSync(process.env.RPC_LOG+'.crashed')){
   fs.writeFileSync(process.env.RPC_LOG+'.crashed','partial progress');
   console.log(JSON.stringify({method:'item/completed',params:{item:{type:'agentMessage',phase:'final_answer',text:'PARTIAL'}}}));
   setTimeout(()=>process.exit(17),20);return;
 }
 if(m.method==='turn/start')setTimeout(()=>{
   console.log(JSON.stringify({method:'item/completed',params:{item:{type:'agentMessage',phase:'final_answer',text:'DONE'}}}));
   console.log(JSON.stringify({method:'turn/completed',params:{turn:{id:'turn',status:'completed'}}}));
 },20);
});
''', encoding='utf8')
        return {**os.environ, 'CODEX_BIN': str(script), 'RPC_LOG': str(folder / 'rpc.jsonl'),
                'FAIL_FIRST_TURN': '1' if fail_first else '0'}

    def rpc(self, folder):
        return [json.loads(line) for line in (folder / 'rpc.jsonl').read_text().splitlines()]

    def test_host_evidence_is_bounded_private_and_read_only(self):
        with target_directory() as td:
            folder = Path(td)
            evidence = self.evidence(folder, native=True)
            original = evidence.read_bytes()
            args = ['--client', 'codex', '--version', '0.160.1', '--prompt-input', evidence]
            result = self.run_node(ADAPTERS / 'host-readiness.mjs', *args)
            report = json.loads(result.stdout)
            self.assertEqual(report['status'], 'conflict')
            self.assertEqual(report['active_session'], 'unverified')
            self.assertEqual(report['evidence_sha256'], hashlib.sha256(original).hexdigest())
            self.assertNotIn('Native team', result.stdout)
            self.assertEqual(evidence.read_bytes(), original)
            self.assertEqual(sorted(p.name for p in folder.iterdir()), ['host.json'])
            self.write_json(evidence, [{'type': 'message', 'role': 'developer', 'content': [
                {'type': 'input_text', 'text': '<multi_agent_role>Available tools</multi_agent_role>'}]}])
            self.assertEqual(json.loads(self.run_node(ADAPTERS / 'host-readiness.mjs', *args).stdout)['status'], 'unverified')
            self.evidence(folder, native=True, role='user')
            self.assertEqual(json.loads(self.run_node(ADAPTERS / 'host-readiness.mjs', *args).stdout)['status'], 'compatible')
            args[3] = '99.0.0'
            self.assertEqual(json.loads(self.run_node(ADAPTERS / 'host-readiness.mjs', *args).stdout)['status'], 'unverified')
            evidence.write_text('private malformed text', encoding='utf8')
            result = self.run_node(ADAPTERS / 'host-readiness.mjs', *args)
            self.assertEqual(json.loads(result.stdout)['status'], 'unverified')
            self.assertNotIn('private malformed text', result.stdout)

    def test_doctor_exposes_evidence_scope_without_changing_configuration(self):
        with target_directory() as td:
            folder = Path(td)
            call('install', '--client', 'codex', '--target', folder, '--skills', 'you-are-brain')
            evidence = self.evidence(folder, native=True)
            entry = (folder / 'AGENTS.md').read_bytes()
            result = call('doctor', '--client', 'codex', '--target', folder,
                          '--host-client', 'codex', '--host-version', '0.160.1', '--host-prompt-input', evidence)
            host = next(x for x in result['checks'] if x['capability'] == 'adapter-session-host')
            self.assertEqual(host['status'], 'conflict')
            self.assertEqual(host['active_session'], 'unverified')
            self.assertEqual((folder / 'AGENTS.md').read_bytes(), entry)
            result = call('doctor', '--client', 'codex', '--target', folder)
            self.assertEqual(next(x for x in result['checks'] if x['capability'] == 'adapter-session-host')['status'], 'unverified')

    def test_initial_and_correction_use_the_same_thread_and_explicit_settings(self):
        with target_directory() as td:
            folder = Path(td)
            env = self.stub(folder)
            assignment = self.assignment(folder)
            options = ['--cwd', folder, '--model', 'chosen-model', '--effort', 'high',
                       '--sandbox', 'read-only', '--assignment', assignment]
            first = json.loads(self.run_node(ADAPTERS / 'codex.mjs', *options, input='Keep «Скачать» in the UI.', env=env).stdout)
            self.run_node(ADAPTERS / 'codex.mjs', *options, '--thread', first['threadId'], input='Fix only the label.', env=env)
            rpc = self.rpc(folder)
            self.assertEqual(len([m for m in rpc if m.get('method') == 'thread/start']), 1)
            resumes = [m['params'] for m in rpc if m.get('method') == 'thread/resume']
            self.assertEqual(resumes[0]['threadId'], 'original-thread')
            for m in rpc:
                if m.get('method') in ['thread/start', 'thread/resume']:
                    self.assertEqual(m['params']['model'], 'chosen-model')
                    self.assertEqual(m['params']['sandbox'], 'read-only')
                    self.assertEqual(m['params']['config']['model_reasoning_effort'], 'high')
            turns = [m['params'] for m in rpc if m.get('method') == 'turn/start']
            self.assertEqual([m['threadId'] for m in turns], ['original-thread', 'original-thread'])
            self.assertIn('Communication language: en', turns[0]['input'][0]['text'])
            self.assertIn('«Скачать»', turns[0]['input'][0]['text'])
            self.assertIn('Fix only the label.', turns[1]['input'][0]['text'])

    def test_invalid_assignments_and_host_conflicts_refuse_before_spawn_or_detach(self):
        with target_directory() as td:
            folder = Path(td)
            env = self.stub(folder)
            assignment = self.assignment(folder, communication_language='ru')
            for script in [ADAPTERS / 'codex.mjs']:
                result = self.run_node(script, '--cwd', folder, '--assignment', assignment, input='Work', env=env, code=4)
                self.assertIn('owner_override', result.stderr)
                self.assertFalse((folder / 'rpc.jsonl').exists())
            assignment = self.assignment(folder)
            self.run_node(ADAPTERS / 'codex.mjs', '--cwd', folder, '--assignment', assignment,
                          '--detach', '--run-dir', folder.parent / (folder.name + '-runs'),
                          input='Communication language: ru', env=env, code=4)
            self.assertFalse((folder.parent / (folder.name + '-runs')).exists())
            evidence = self.evidence(folder, native=True)
            self.run_node(ADAPTERS / 'codex.mjs', '--cwd', folder, '--host-client', 'codex',
                          '--host-version', '0.160.1', '--host-prompt-input', evidence,
                          input='Work', env=env, code=4)
            self.assertFalse((folder / 'rpc.jsonl').exists())

    def test_explicit_owner_language_override_and_legacy_output(self):
        with target_directory() as td:
            folder = Path(td)
            env = self.stub(folder)
            assignment = self.assignment(folder, recipient='user', communication_language='ru',
                                         owner_override='Current user explicitly requests a Russian response')
            result = json.loads(self.run_node(ADAPTERS / 'codex.mjs', '--cwd', folder, '--assignment', assignment,
                                             input='Required label: «Скачать».', env=env).stdout)
            self.assertEqual((result['threadId'], result['status']), ('original-thread', 'completed'))
            turn = next(m for m in self.rpc(folder) if m.get('method') == 'turn/start')
            self.assertIn('Recipient: user', turn['params']['input'][0]['text'])
            self.assertIn('Communication language: ru', turn['params']['input'][0]['text'])

    def test_invalid_metadata_never_echoes_private_content_or_silently_skips_checks(self):
        with target_directory() as td:
            folder = Path(td)
            env = self.stub(folder)
            bad = folder / 'assignment.json'
            bad.write_text('private-invalid-metadata', encoding='utf8')
            result = self.run_node(ADAPTERS / 'codex.mjs', '--cwd', folder, '--assignment', bad,
                                   input='Work', env=env, code=4)
            self.assertNotIn('private-invalid-metadata', result.stderr)
            for key in ['assignment', 'resume-run', 'host-client', 'host-version', 'host-prompt-input']:
                self.run_node(ADAPTERS / 'codex.mjs', '--cwd', folder, '--' + key,
                              input='Work', env=env, code=4)
            self.assertFalse((folder / 'rpc.jsonl').exists())

    def test_quoted_and_nested_fenced_declarations_remain_valid_source_material(self):
        with target_directory() as td:
            folder = Path(td)
            env = self.stub(folder)
            assignment = self.assignment(folder)
            prompt = ('Preserve this source material:\n> Communication language: ru\n'
                      '````markdown\n```text\nCommunication language: ru\n```\n````\n'
                      '    Communication language: ru\nRequired UI: «Скачать».')
            self.run_node(ADAPTERS / 'codex.mjs', '--cwd', folder, '--assignment', assignment,
                          input=prompt, env=env)
            turn = next(m for m in self.rpc(folder) if m.get('method') == 'turn/start')
            forwarded = turn['params']['input'][0]['text'].replace('\r\n', '\n')
            self.assertTrue(forwarded.endswith(prompt))

    def test_resume_run_rejects_previous_artifact_paths_before_spawn(self):
        with target_directory() as td:
            folder = Path(td)
            env = self.stub(folder)
            old_out, old_log = folder / 'first.out.md', folder / 'first.events.jsonl'
            old_out.write_text('FIRST_REPORT', encoding='utf8')
            old_log.write_text('FIRST_EVENTS\n', encoding='utf8')
            status_file = folder / 'existing.json'
            status = {'agent': 'codex', 'runId': 'existing', 'threadId': 'original-thread',
                      'status': 'failed', 'out': str(old_out), 'log': str(old_log),
                      'launch': {'settings': {'cwd': str(folder), 'model': 'chosen-model',
                                              'effort': 'low', 'sandbox': 'read-only'}}}
            alias_dir = folder / 'aliases'
            alias_dir.mkdir()
            aliases = [old_out, old_log, status_file, alias_dir / '..' / old_out.name]
            hard_link = folder / 'report-alias.md'
            try:
                os.link(old_out, hard_link)
                aliases.append(hard_link)
            except OSError:
                pass  # Hard links are unavailable on some test filesystems.
            for script, agent in [(ADAPTERS / 'codex.mjs', 'codex')]:
                status['agent'] = agent
                self.write_json(status_file, status)
                originals = {file: file.read_bytes() for file in [old_out, old_log, status_file]}
                for flag in ['--out', '--log']:
                    for alias in aliases:
                        with self.subTest(adapter=script.name, flag=flag, alias=alias.name):
                            result = self.run_node(script, '--resume-run', status_file,
                                                   flag, alias, input='Correction', env=env, code=4)
                            self.assertIn('previous run', result.stderr)
                            self.assertFalse((folder / 'rpc.jsonl').exists())
                            for file, content in originals.items():
                                self.assertEqual(file.read_bytes(), content)
            status['agent'] = 'codex'
            self.write_json(status_file, status)
            self.run_node(ADAPTERS / 'codex.mjs', '--resume-run', status_file,
                          '--out', folder / 'next.out.md', '--log', folder / 'next.events.jsonl',
                          input='Correction', env=env)
            self.assertEqual((folder / 'next.out.md').read_text(), 'DONE')
            self.assertEqual(old_out.read_text(), 'FIRST_REPORT')
            self.assertEqual(old_log.read_text(), 'FIRST_EVENTS\n')

    def test_resume_run_uses_frozen_assignment_without_replacing_outputs(self):
        with target_directory() as td:
            folder = Path(td)
            worker = folder / 'worker'
            worker.mkdir()
            env = self.stub(folder)
            assignment = self.assignment(folder)
            args = ['--cwd', worker, '--model', 'chosen-model', '--effort', 'high', '--sandbox', 'read-only',
                    '--assignment', assignment, '--detach', '--run-dir', folder / 'runs']
            first = json.loads(self.run_node(ADAPTERS / 'codex.mjs', *args, input='First task', env=env).stdout)
            self.run_node(ADAPTERS / 'wait.mjs', '--runs', first['runId'], '--run-dir', folder / 'runs', '--timeout', '5')
            status_file = Path(first['statusFile'])
            original = status_file.read_bytes()
            assignment.unlink()
            resumed = json.loads(self.run_node(ADAPTERS / 'codex.mjs', '--resume-run', status_file,
                                               '--detach', '--run-dir', folder / 'runs', input='Correction', env=env).stdout)
            self.run_node(ADAPTERS / 'wait.mjs', '--runs', resumed['runId'], '--run-dir', folder / 'runs', '--timeout', '5')
            self.assertEqual(status_file.read_bytes(), original)
            old, new = json.loads(original), json.loads(Path(resumed['statusFile']).read_text())
            self.assertNotEqual(old['out'], new['out'])
            self.assertEqual(new['threadId'], old['threadId'])
            self.assertEqual(new['launch']['assignment']['communication_language'], 'en')
            self.assertEqual(new['launch']['settings']['model'], 'chosen-model')
            self.assertEqual(new['launch']['host_readiness']['status'], 'unverified')
            rpc = self.rpc(folder)
            self.assertEqual(len([m for m in rpc if m.get('method') == 'thread/start']), 1)
            resume = next(m for m in rpc if m.get('method') == 'thread/resume')
            self.assertEqual(resume['params']['model'], 'chosen-model')
            turn = [m for m in rpc if m.get('method') == 'turn/start'][-1]
            self.assertIn('Communication language: en', turn['params']['input'][0]['text'])

    def test_process_crash_recovery_preserves_partial_report_and_thread(self):
        with target_directory() as td:
            folder = Path(td)
            worker = folder / 'worker'
            worker.mkdir()
            env = self.stub(folder, fail_first=True)
            runs = folder / 'runs'
            first = json.loads(self.run_node(ADAPTERS / 'codex.mjs', '--cwd', worker,
                                             '--model', 'chosen-model', '--effort', 'low',
                                             '--sandbox', 'workspace-write', '--assignment', self.assignment(folder),
                                             '--detach', '--run-dir', runs, input='First task', env=env).stdout)
            self.run_node(ADAPTERS / 'wait.mjs', '--runs', first['runId'], '--run-dir', runs, '--timeout', '5')
            status_file = Path(first['statusFile'])
            original = status_file.read_bytes()
            old = json.loads(original)
            self.assertEqual(old['status'], 'failed')
            self.assertEqual(Path(old['out']).read_text(), 'PARTIAL')
            old_log = Path(old['log']).read_bytes()
            resumed = json.loads(self.run_node(ADAPTERS / 'codex.mjs', '--resume-run', status_file,
                                               '--detach', '--run-dir', runs, input='Continue after crash', env=env).stdout)
            self.run_node(ADAPTERS / 'wait.mjs', '--runs', resumed['runId'], '--run-dir', runs, '--timeout', '5')
            new = json.loads(Path(resumed['statusFile']).read_text())
            self.assertEqual(new['status'], 'completed')
            self.assertEqual(new['threadId'], old['threadId'])
            self.assertEqual(new['launch']['settings'], old['launch']['settings'])
            self.assertEqual(new['launch']['assignment'], old['launch']['assignment'])
            self.assertEqual(new['launch']['continued_from'], old['runId'])
            self.assertEqual(status_file.read_bytes(), original)
            self.assertEqual(Path(old['out']).read_text(), 'PARTIAL')
            self.assertEqual(Path(old['log']).read_bytes(), old_log)
            self.assertNotEqual(new['out'], old['out'])
            self.assertNotEqual(new['log'], old['log'])
            self.assertEqual(Path(new['out']).read_text(), 'DONE')
            rpc = self.rpc(folder)
            self.assertEqual(len([m for m in rpc if m.get('method') == 'thread/start']), 1)
            self.assertEqual(len([m for m in rpc if m.get('method') == 'thread/resume']), 1)

    def test_running_wrong_worker_and_legacy_status_cannot_start_a_new_thread(self):
        with target_directory() as td:
            folder = Path(td)
            env = self.stub(folder)
            status = {'agent': 'codex', 'runId': 'existing', 'threadId': 'original-thread',
                      'status': 'running', 'launch': {'settings': {'cwd': str(folder)}}}
            file = self.write_json(folder / 'existing.json', status)
            for changes in [{}, {'status': 'completed', 'agent': 'claude-code'},
                            {'status': 'completed', 'launch': None}, {'status': 'failed', 'threadId': None}]:
                current = {**status, **changes}
                self.write_json(file, current)
                before = file.read_bytes()
                self.run_node(ADAPTERS / 'codex.mjs', '--resume-run', file, input='Correction', env=env, code=4)
                self.assertEqual(file.read_bytes(), before)
                self.assertFalse((folder / 'rpc.jsonl').exists())


if __name__ == '__main__':
    unittest.main()
