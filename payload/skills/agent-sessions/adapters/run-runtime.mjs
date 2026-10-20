// Shared detached-run transport. Adapters keep owning their foreground protocol.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

export const terminal = status => ['completed', 'failed', 'interrupted'].includes(status);
export function atomicJSON(file, value) {
  const temp = `${file}.${process.pid}.${crypto.randomUUID()}.tmp`;
  try {
    fs.writeFileSync(temp, JSON.stringify(value) + '\n', { flag: 'wx', mode: 0o600 });
    fs.renameSync(temp, file);
  } finally {
    if (fs.existsSync(temp)) fs.unlinkSync(temp);
  }
}
export function readStatus(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}
export function statusPath(dir, id) {
  if (!/^[a-zA-Z0-9_-]+$/.test(id)) throw new Error(`Invalid run id: ${id}`);
  return path.join(dir, `${id}.json`);
}
// Resolve existing ancestors as well, so a symlink cannot put metadata inside cwd.
function canonical(file) {
  const resolved = path.resolve(file);
  if (fs.existsSync(resolved)) return fs.realpathSync(resolved);
  return path.join(canonical(path.dirname(resolved)), path.basename(resolved));
}
export function runDirectory(args, workerCwd) {
  const dir = canonical(args['run-dir'] || process.env.AGENT_RUNS_DIR ||
    path.join(path.dirname(workerCwd || process.cwd()), '.agent-runs'));
  if (workerCwd) {
    const relative = path.relative(canonical(workerCwd), dir);
    if (!relative || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative))) {
      throw new Error('--run-dir must be outside the worker --cwd');
    }
  }
  return dir;
}
export function recordThread(threadId) {
  const file = process.env.AGENT_RUN_STATUS_FILE;
  if (!file) return;
  const status = readStatus(file);
  if (!terminal(status.status)) atomicJSON(file, { ...status, threadId });
}
export async function detach(agent, args, prompt, adapterURL) {
  const cwd = path.resolve(args.cwd || process.cwd());
  const dir = runDirectory(args, cwd);
  fs.mkdirSync(dir, { recursive: true });
  const runId = crypto.randomUUID();
  const statusFile = statusPath(dir, runId);
  const promptFile = path.join(dir, `${runId}.prompt.md`);
  const configFile = path.join(dir, `${runId}.config.json`);
  const options = { ...args, cwd, prompt: promptFile,
    out: path.resolve(args.out || path.join(dir, `${runId}.out.md`)),
    log: path.resolve(args.log || path.join(dir, `${runId}.events.jsonl`)) };
  delete options.detach;
  delete options['run-dir'];
  fs.writeFileSync(promptFile, prompt, { mode: 0o600 });
  atomicJSON(configFile, { agent, runId, statusFile, options, adapter: fileURLToPath(adapterURL) });
  const stderr = fs.openSync(path.join(dir, `${runId}.stderr.log`), 'a', 0o600);
  let child;
  try {
    child = spawn(process.execPath, [fileURLToPath(import.meta.url), '--supervise', configFile], {
      detached: true, windowsHide: true, stdio: ['ignore', 'ignore', stderr, 'ipc'],
      // A new detached run must never update the containing run's metadata.
      env: { ...process.env, AGENT_RUN_STATUS_FILE: '' },
    });
    await new Promise((resolve, reject) => {
      child.once('error', reject);
      child.once('exit', code => reject(new Error(`Supervisor exited before ready: ${code}`)));
      child.once('message', message => message.ready ? resolve() : reject(new Error(message.error)));
    });
    if (child.connected) child.disconnect();
    child.unref();
    console.log(JSON.stringify({ agent, runId, status: 'started', statusFile }));
  } finally {
    fs.closeSync(stderr);
  }
}
export function killTree(pid) {
  if (!Number.isInteger(pid) || pid <= 0) throw new Error('Run has no valid process id');
  if (process.platform === 'win32') {
    const result = spawnSync('taskkill', ['/PID', String(pid), '/T', '/F'], { windowsHide: true, encoding: 'utf8' });
    if (result.error) throw result.error;
    if (result.status !== 0 && alive(pid)) throw new Error(result.stderr || result.stdout || 'taskkill failed');
  } else {
    try { process.kill(-pid, 'SIGKILL'); } catch (error) { if (error.code !== 'ESRCH') throw error; }
  }
}
export function alive(pid) {
  try { process.kill(pid, 0); return true; } catch (error) { return error.code === 'EPERM'; }
}

async function supervise(configFile) {
  const { agent, runId, statusFile, options, adapter } = readStatus(configFile);
  atomicJSON(statusFile, { runId, agent, pid: process.pid, threadId: options.thread || null,
    status: 'running', exitCode: null, out: options.out, log: options.log,
    startedAt: new Date().toISOString(), endedAt: null });
  process.send?.({ ready: true });
  const argv = Object.entries(options).flatMap(([key, value]) => value === true ? [`--${key}`] : [`--${key}`, String(value)]);
  const child = spawn(process.execPath, [adapter, ...argv], {
    windowsHide: true, stdio: ['ignore', 'pipe', 'inherit'],
    env: { ...process.env, AGENT_RUN_STATUS_FILE: statusFile },
  });
  let buffer = '', lastLine = '';
  child.stdout.setEncoding('utf8');
  child.stdout.on('data', chunk => {
    buffer += chunk;
    let newline;
    while ((newline = buffer.indexOf('\n')) !== -1) {
      const line = buffer.slice(0, newline).trim();
      buffer = buffer.slice(newline + 1);
      if (line) lastLine = line;
    }
  });
  const finish = (code, signal) => {
    const previous = readStatus(statusFile);
    if (terminal(previous.status)) return;
    let result;
    try { result = JSON.parse(buffer.trim() || lastLine); } catch { /* driver failed before result */ }
    atomicJSON(statusFile, { ...previous, threadId: result?.threadId || previous.threadId,
      status: signal ? 'interrupted' : code === 0 && result?.status === 'completed' ? 'completed' : 'failed',
      exitCode: code ?? 1, endedAt: new Date().toISOString() });
  };
  child.once('error', error => { console.error(error.message); finish(3); });
  child.once('close', finish);
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url) && process.argv[2] === '--supervise') {
  try { await supervise(process.argv[3]); }
  catch (error) { process.send?.({ error: error.message }); console.error(error.message); process.exitCode = 2; }
}
