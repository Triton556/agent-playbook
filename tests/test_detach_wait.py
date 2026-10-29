"""Detached transport checks, using synthetic processes and an app-server stub."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import unittest
from contextlib import contextmanager

from test_install import ROOT, call, target_directory

NODE = shutil.which('node')
ADAPTERS = ROOT / 'payload/skills/agent-sessions/adapters'
WAIT = ADAPTERS / 'wait.mjs'


@unittest.skipUnless(NODE, 'Node required for detached transport')
class DetachedRuns(unittest.TestCase):
    @contextmanager
    def run_folder(self):
        with target_directory() as td:
            self.fake_processes = []
            try:
                yield td
            finally:
                for process, name in self.fake_processes:
                    if process.poll() is None:
                        self.command(WAIT, '--cancel', name, '--run-dir', td)
                    process.wait(timeout=8)
                    process.stdout.close()
                    process.stderr.close()

    def command(self, script, *args, expected=0, env=None, input=None):
        result = subprocess.run([NODE, str(script), *map(str, args)], capture_output=True,
                                text=True, encoding='utf8', env=env, input=input, timeout=20)
        self.assertEqual(result.returncode, expected, (result.stdout, result.stderr))
        return json.loads(result.stdout if '--describe' in args else result.stdout.splitlines()[-1])

    def fake_run(self, folder, name, delay=1000, descendant=False):
        folder = Path(folder)
        status = folder / f'{name}.json'
        stub = folder / f'{name}.cjs'
        stub.write_text('''
const fs = require('fs');
const {spawn} = require('child_process');
const [file, delay, marker, tree] = process.argv.slice(2);
let child;
if (tree === 'yes') child = spawn(process.execPath, ['-e',
  'setTimeout(()=>require("fs").writeFileSync(process.argv[1],"orphan"),1200)', marker], {stdio:'ignore'});
console.log(JSON.stringify({pid:process.pid, child:child?.pid}));
setTimeout(() => {
  const data=JSON.parse(fs.readFileSync(file));
  fs.writeFileSync(file+'.tmp',JSON.stringify({...data,status:'completed',exitCode:0,endedAt:new Date().toISOString()}));
  fs.renameSync(file+'.tmp',file);
}, Number(delay));
''', encoding='utf8')
        options = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}
        process = subprocess.Popen([NODE, str(stub), str(status), str(delay), str(folder / 'orphan'), 'yes' if descendant else 'no'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, **options)
        ready = json.loads(process.stdout.readline())
        status.write_text(json.dumps({'runId': name, 'agent': 'stub', 'pid': ready['pid'], 'threadId': f'thread-{name}',
                          'status': 'running', 'exitCode': None, 'out': str(folder / f'{name}.out'),
                          'log': None, 'startedAt': '2026-01-01T00:00:00Z', 'endedAt': None}), encoding='utf8')
        self.fake_processes.append((process, name))
        return process

    def test_wait_any_then_all(self):
        with self.run_folder() as td:
            first = self.fake_run(td, 'first', 900)
            last = self.fake_run(td, 'last', 3000)
            any_result = self.command(WAIT, '--runs', 'first,last', '--run-dir', td, '--mode', 'any')
            self.assertEqual([x['runId'] for x in any_result['done']], ['first'])
            self.assertEqual(any_result['running'], ['last'])
            self.assertIsNone(last.poll())
            all_result = self.command(WAIT, '--runs', 'first,last', '--run-dir', td, '--mode', 'all')
            self.assertEqual(len(all_result['done']), 2)
            self.assertFalse(all_result['running'])
            self.assertFalse(all_result['timedOut'])
            first.wait(timeout=3)
            last.wait(timeout=3)

    def test_timeout_status_unknown_and_invalid_options(self):
        with self.run_folder() as td:
            process = self.fake_run(td, 'slow', 60000)
            start = time.monotonic()
            result = self.command(WAIT, '--status', '--runs', 'slow', '--run-dir', td)
            self.assertLess(time.monotonic() - start, 2)
            self.assertEqual(result, {'done': [], 'running': ['slow'], 'timedOut': False})
            result = self.command(WAIT, '--runs', 'slow', '--run-dir', td, '--timeout', '.2', expected=5)
            self.assertTrue(result['timedOut'])
            for args in [('--runs', 'missing'), ('--runs', '../escape'), ('--runs', 'slow', '--mode', 'bad'),
                         ('--runs', 'slow', '--timeout', '-1')]:
                error = subprocess.run([NODE, str(WAIT), '--run-dir', td, *args], capture_output=True, timeout=4)
                self.assertEqual(error.returncode, 2, error.stderr)
            self.command(WAIT, '--cancel', 'slow', '--run-dir', td)
            process.wait(timeout=3)

    def test_cancel_stops_tree_and_preserves_interrupted(self):
        with self.run_folder() as td:
            process = self.fake_run(td, 'tree', 60000, descendant=True)
            result = self.command(WAIT, '--cancel', 'tree', '--run-dir', td)
            process.wait(timeout=3)
            self.assertEqual(result['done'][0]['status'], 'interrupted')
            # A bounded wait verifies the descendant cannot create its delayed artifact.
            self.command(WAIT, '--runs', 'tree', '--mode', 'all', '--run-dir', td)
            time.sleep(1.4)
            self.assertFalse((Path(td) / 'orphan').exists())
            self.assertEqual(json.loads((Path(td) / 'tree.json').read_text())['status'], 'interrupted')
            self.command(WAIT, '--cancel', 'tree', '--run-dir', td)  # idempotent

    def stub_codex(self, folder):
        stub = Path(folder) / 'codex-stub.cjs'
        stub.write_text('''
const readline = require('readline');
const send = obj => console.log(JSON.stringify(obj));
readline.createInterface({input:process.stdin}).on('line', line => {
 const msg=JSON.parse(line);
 if (msg.id === 999 && msg.result?.decision === 'decline') {
   setTimeout(()=>{
    send({method:'item/completed',params:{item:{type:'agentMessage',phase:'final_answer',text:'READY'}}});
    send({method:'turn/completed',params:{turn:{id:'stub-turn',status:'completed'}}});
   },1600);
   return;
 }
 if (msg.id === undefined) return;
 if (process.env.STUB_ERROR && msg.method === 'thread/start') {
   send({id:msg.id,error:{code:-32000,message:'synthetic protocol error'}}); return;
 }
 const result = msg.method === 'thread/start' ? {thread:{id:'stub-thread'}} :
   msg.method === 'turn/start' ? {turn:{id:'stub-turn'}} : {};
 send({id:msg.id,result});
 if (msg.method === 'turn/start') send({id:999,method:'item/commandExecution/requestApproval',params:{}});
});
''', encoding='utf8')
        return {**os.environ, 'CODEX_BIN': str(stub)}

    def test_codex_detach_and_foreground_compatibility(self):
        with target_directory() as td:
            folder = Path(td)
            cwd = folder / 'worker'
            cwd.mkdir()
            env = self.stub_codex(folder)
            start = time.monotonic()
            started = self.command(ADAPTERS / 'codex.mjs', '--detach', '--cwd', cwd,
                                   '--model', 'stub', '--effort', 'low', '--sandbox', 'read-only', input='Reply READY', env=env)
            self.assertLess(time.monotonic() - start, 2)
            self.assertEqual(started['status'], 'started')
            status_file = Path(started['statusFile'])
            self.assertEqual(status_file.parent, folder / '.agent-runs')
            status = json.loads(status_file.read_text())
            self.assertEqual(status['status'], 'running')
            self.assertGreater(status['pid'], 0)
            pending = self.command(WAIT, '--runs', started['runId'], '--run-dir', status_file.parent,
                                   '--timeout', '.4', expected=5)
            self.assertEqual(pending['running'], [started['runId']])
            self.assertEqual(json.loads(status_file.read_text())['threadId'], 'stub-thread')
            result = self.command(WAIT, '--runs', started['runId'], '--run-dir', status_file.parent, '--mode', 'all', '--timeout', '10')
            self.assertEqual(result['done'][0]['threadId'], 'stub-thread')
            self.assertEqual(result['done'][0]['status'], 'completed')
            self.assertEqual(Path(result['done'][0]['out']).read_text(), 'READY')
            status = json.loads(status_file.read_text())
            self.assertEqual(status['exitCode'], 0)
            self.assertIsNotNone(status['endedAt'])
            self.assertIn('requestApproval', Path(status['log']).read_text())
            foreground = self.command(ADAPTERS / 'codex.mjs', '--cwd', cwd, input='Reply READY', env=env)
            self.assertEqual(foreground, {'agent': 'codex', 'threadId': 'stub-thread', 'turnId': 'stub-turn', 'status': 'completed', 'out': None})

    def test_run_directory_override_refusal_and_descriptions(self):
        with target_directory() as td:
            folder = Path(td)
            cwd = folder / 'worker'
            cwd.mkdir()
            env = self.stub_codex(folder)
            for name in ('codex',):
                description = self.command(ADAPTERS / f'{name}.mjs', '--describe')
                self.assertEqual(description['contract'], 2)
                self.assertTrue(description['detach'])
                refused = subprocess.run([NODE, str(ADAPTERS / f'{name}.mjs'), '--detach', '--cwd', str(cwd),
                                          '--run-dir', str(cwd / 'metadata')], input='test', env=env, text=True, capture_output=True)
                self.assertEqual(refused.returncode, 4, refused.stderr)
                self.assertFalse((cwd / 'metadata').exists())
            env['AGENT_RUNS_DIR'] = str(folder / 'custom')
            started = self.command(ADAPTERS / 'codex.mjs', '--detach', '--cwd', cwd, input='READY', env=env)
            self.assertEqual(Path(started['statusFile']).parent, folder / 'custom')
            self.command(WAIT, '--cancel', started['runId'], env=env)

    def test_symlink_cannot_put_run_metadata_inside_worker(self):
        with target_directory() as td:
            folder = Path(td)
            cwd = folder / 'worker'
            cwd.mkdir()
            link = folder / 'alias'
            created = subprocess.run([NODE, '-e', "require('fs').symlinkSync(process.argv[1],process.argv[2],process.platform==='win32'?'junction':'dir')",
                                      str(cwd), str(link)], capture_output=True)
            if created.returncode:
                self.skipTest('OS does not allow a temporary symlink/junction')
            try:
                result = subprocess.run([NODE, str(ADAPTERS / 'codex.mjs'), '--detach', '--cwd', str(cwd),
                                         '--run-dir', str(link / 'runs')], input='READY', text=True, capture_output=True)
                self.assertEqual(result.returncode, 4, result.stderr)
                self.assertFalse((cwd / 'runs').exists())
            finally:
                os.rmdir(link) if os.name == 'nt' else link.unlink()

    def test_wait_fallback_without_filesystem_notifications(self):
        with self.run_folder() as td:
            self.fake_run(td, 'fallback', 2800)
            preload = Path(td) / 'no-watch.cjs'
            preload.write_text("require('fs').watch = () => { throw new Error('watch unsupported'); };", encoding='utf8')
            env = {**os.environ, 'NODE_OPTIONS': f'--require="{preload.as_posix()}"'}
            start = time.monotonic()
            result = self.command(WAIT, '--runs', 'fallback', '--run-dir', td, '--timeout', '8', env=env)
            self.assertEqual(result['done'][0]['status'], 'completed')
            self.assertGreaterEqual(time.monotonic() - start, 3.5)

    def test_status_observation_never_rewrites_worker_state(self):
        with target_directory() as td:
            folder = Path(td)
            status_file = folder / 'race.json'
            status_file.write_text(json.dumps({'runId': 'race', 'agent': 'stub', 'pid': 123456,
                                              'threadId': 'race-thread', 'status': 'running', 'out': None}), encoding='utf8')
            preload = folder / 'completion-race.cjs'
            preload.write_text("process.kill = () => { throw new Error('Status must not signal or probe processes'); };", encoding='utf8')
            env = {**os.environ, 'NODE_OPTIONS': f'--require="{preload.as_posix()}"'}
            before = status_file.read_bytes()
            result = self.command(WAIT, '--status', '--runs', 'race', '--run-dir', td, env=env)
            self.assertEqual(result['running'], ['race'])
            self.assertEqual(status_file.read_bytes(), before)

    def test_detached_start_and_protocol_failures(self):
        with target_directory() as td:
            folder = Path(td)
            cwd = folder / 'worker'
            cwd.mkdir()
            env = self.stub_codex(folder)
            env['STUB_ERROR'] = '1'
            for code in (2, 3):
                if code == 3:
                    env['CODEX_BIN'] = str(folder / 'nonexistent-codex')
                started = self.command(ADAPTERS / 'codex.mjs', '--detach', '--cwd', cwd, input='READY', env=env)
                result = self.command(WAIT, '--runs', started['runId'], '--run-dir', Path(started['statusFile']).parent, '--timeout', '10')
                self.assertEqual(result['done'][0]['status'], 'failed')
                self.assertEqual(result['done'][0]['exitCode'], code)

    def test_full_profile_installs_wait_and_runtime(self):
        call('catalog')
        with target_directory() as td:
            common = ['--target', td, '--client', 'codex', '--profile', 'full']
            call('plan', *common)
            call('install', *common)
            self.assertEqual(call('verify', '--target', td, '--client', 'codex')['status'], 'pass')
            for name in ('wait.mjs', 'run-runtime.mjs'):
                self.assertTrue((Path(td) / '.agents/skills/agent-sessions/adapters' / name).is_file())


if __name__ == '__main__':
    unittest.main()
