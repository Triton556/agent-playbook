#!/usr/bin/env node
// agent-sessions adapter for OpenAI Codex (contract 2, see references/contract.md).
// Runs one turn in a Codex thread that is visible in the Codex app.
// Live checks passed 2026-10-19 on Windows, Codex app-server: describe/exit 4, new session, continue
// with --thread, read-only refused a write, workspace-write refused a write outside --cwd, thread
// visible in the Codex app.
//
//   node codex.mjs --describe
//   node codex.mjs --cwd <dir> --name "<title>" [--prompt brief.md] [--out final.md]
//        [--log events.jsonl] [--thread <id>] [--model <id>] [--effort <level>]
//        [--sandbox workspace-write|read-only|danger-full-access] [--proxy]
//
// It starts its own `codex app-server` over stdio on the user's CODEX_HOME (default
// ~/.codex), so threads land in the same history as the app. --proxy instead attaches
// to an already running app-server daemon (`codex app-server proxy`).
// Approval and input requests are declined: the run is unattended.
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import readline from 'node:readline';
import { detach, recordThread, runDirectory } from './run-runtime.mjs';
import { recoverRun, prepareLaunch } from './launch-check.mjs';

const FLAGS = new Set(['proxy', 'describe', 'detach']);
const args = {};
for (let i = 2; i < process.argv.length; i++) {
  const key = process.argv[i].replace(/^--/, '');
  if (FLAGS.has(key)) args[key] = true;
  else args[key] = process.argv[++i];
}

function findCodex() {
  if (process.env.CODEX_BIN) return process.env.CODEX_BIN;
  const which = spawnSync(process.platform === 'win32' ? 'where' : 'which', ['codex'], { encoding: 'utf8' });
  const onPath = which.status === 0 && which.stdout.split(/\r?\n/).find(Boolean);
  if (onPath) return onPath.trim();
  const candidates = [];
  if (process.platform === 'win32') {
    // The desktop app keeps versioned CLI builds here; take the newest.
    const base = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData/Local'), 'OpenAI/Codex/bin');
    if (fs.existsSync(base)) {
      for (const dir of fs.readdirSync(base)) {
        const exe = path.join(base, dir, 'codex.exe');
        if (fs.existsSync(exe)) candidates.push({ exe, mtime: fs.statSync(exe).mtimeMs });
      }
    }
  } else {
    for (const exe of ['/Applications/Codex.app/Contents/Resources/codex', '/opt/homebrew/bin/codex', '/usr/local/bin/codex']) {
      if (fs.existsSync(exe)) candidates.push({ exe, mtime: fs.statSync(exe).mtimeMs });
    }
  }
  candidates.sort((a, b) => b.mtime - a.mtime);
  if (candidates[0]) return candidates[0].exe;
  throw new Error('Codex CLI not found. Set CODEX_BIN to the codex executable.');
}

const DESCRIPTION = {
  agent: 'codex',
  contract: 2,
  detach: true,
  verified: true,
  visible_in: 'Codex app: the thread list, under the given name; the user can open the thread and write in it',
  resume: true,
  launch_checks: ['assignment', 'resume-run', 'host-prompt-input'],
  current_host_readiness: 'unverified',
  access_modes: {
    'read-only': 'Codex sandbox: reads files, writes nothing, runs only read-only commands',
    'workspace-write': 'Codex sandbox: writes only inside --cwd; on Windows it cannot write inside .git',
    'danger-full-access': 'no sandbox: full access to files, commands and network as the user',
  },
  effort: ['minimal', 'low', 'medium', 'high', 'xhigh', 'ultra'],
  notes: "Uses the user's Codex home, settings, skills and hooks. Starting it from inside a Codex sandbox fails with exit code 3.",
};
if (args.describe) {
  console.log(JSON.stringify(DESCRIPTION, null, 2));
  process.exit(0);
}
let recovered;
try { recovered = recoverRun(args, 'codex'); }
catch (error) { console.error(`[driver] ${error.message}`); process.exit(4); }
const sandbox = args.sandbox || 'workspace-write';
if (!DESCRIPTION.access_modes[sandbox]) {
  process.stderr.write(`[driver] unsupported access mode: ${sandbox}
`);
  process.exit(4);
}

const cwd = path.resolve(args.cwd || process.cwd());
const rawPrompt = args.prompt ? fs.readFileSync(args.prompt, 'utf8') : fs.readFileSync(0, 'utf8');
if (!rawPrompt.trim()) throw new Error('Empty prompt');
if (!fs.existsSync(cwd)) throw new Error(`cwd does not exist: ${cwd}`);
let checked;
try { checked = prepareLaunch(args, rawPrompt, recovered); }
catch (error) { console.error(`[driver] ${error.message}`); process.exit(4); }
const prompt = checked.prompt;

if (args.detach) {
  // Reject a metadata directory inside the worker before creating anything.
  try { runDirectory(args, cwd); }
  catch (error) { console.error(`[driver] ${error.message}`); process.exit(4); }
  try { await detach('codex', args, rawPrompt, import.meta.url, checked.launch); process.exit(0); }
  catch (error) { console.error(`[driver] ${error.message}`); process.exit(3); }
}
// Explicit JS CLI paths also allow protocol fixtures without a real Codex process.
const bin = findCodex();
const cli = args.proxy ? ['app-server', 'proxy'] : ['app-server'];
const child = spawn(/\.[cm]?js$/i.test(bin) ? process.execPath : bin,
  /\.[cm]?js$/i.test(bin) ? [bin, ...cli] : cli, { windowsHide: true, stdio: ['pipe', 'pipe', 'pipe'] });
child.stderr.on('data', chunk => { if (args.verbose) process.stderr.write(chunk); });
const log = args.log ? fs.createWriteStream(args.log, { flags: 'a' }) : null;
const pending = new Map();
let nextId = 1;
let finalText = '';
let lastText = '';
let turnId = null;
let settle;
const finished = new Promise(resolve => { settle = resolve; });

const send = msg => child.stdin.write(JSON.stringify(msg) + '\n');
const request = (method, params) => new Promise((resolve, reject) => {
  const id = nextId++;
  pending.set(id, { resolve, reject, method });
  send({ id, method, params });
});

// Unattended run: refuse every approval or question the agent raises.
function declineServerRequest(msg) {
  const decline = {
    'item/commandExecution/requestApproval': { decision: 'decline' },
    'item/fileChange/requestApproval': { decision: 'decline' },
    applyPatchApproval: { decision: 'denied' },
    execCommandApproval: { decision: 'denied' },
    'mcpServer/elicitation/request': { action: 'decline', content: null, _meta: null },
  }[msg.method];
  process.stderr.write(`[driver] declined ${msg.method}\n`);
  if (decline) send({ id: msg.id, result: decline });
  else send({ id: msg.id, error: { code: -32000, message: 'Unattended driver: request declined' } });
}

readline.createInterface({ input: child.stdout }).on('line', line => {
  if (!line.trim()) return;
  let msg;
  try { msg = JSON.parse(line); } catch { return; }
  log?.write(line + '\n');
  if (msg.id !== undefined && !msg.method) {
    const p = pending.get(msg.id);
    if (!p) return;
    pending.delete(msg.id);
    if (msg.error) p.reject(new Error(`${p.method}: ${JSON.stringify(msg.error)}`));
    else p.resolve(msg.result);
    return;
  }
  if (msg.id !== undefined && msg.method) return declineServerRequest(msg);
  const p = msg.params || {};
  const item = p.item;
  if (msg.method === 'item/completed' && item?.type === 'agentMessage') {
    lastText = item.text ?? lastText;
    if (item.phase === 'final_answer') finalText = item.text;
  }
  if (msg.method === 'item/started' && item?.type === 'commandExecution') process.stderr.write(`[cmd] ${String(item.command).slice(0, 160)}\n`);
  if (msg.method === 'item/started' && item?.type === 'mcpToolCall') process.stderr.write(`[tool] ${item.server}.${item.tool}\n`);
  if (msg.method === 'error') process.stderr.write(`[error] ${JSON.stringify(p).slice(0, 400)}\n`);
  if (msg.method === 'turn/completed' && (!turnId || p.turn?.id === turnId)) settle(p.turn);
});
child.on('exit', code => settle({ status: `app-server-exited-${code}` }));
child.on('error', error => {
  // Inside a Codex sandbox the child process is usually refused (spawn EPERM).
  process.stderr.write(`[driver] cannot start codex app-server: ${error.code || error.message}. No thread was created. If this runs inside a Codex sandbox, run the command outside it (approval) or ask the user.
`);
  process.exit(3);
});

try {
  await request('initialize', {
    clientInfo: { name: 'agent-sessions-codex', title: 'Agent sessions: Codex adapter', version: '1.0.0' },
    capabilities: { experimentalApi: true, requestAttestation: false },
  });
  send({ method: 'initialized' });

  // Resume does not keep the sandbox of the earlier run, so pass it every time.
  const params = { cwd, sandbox, approvalPolicy: 'never' };
  if (args.model) params.model = args.model;
  // Effort is set per turn; also store it as the thread default so the app shows the real value.
  if (args.effort) params.config = { model_reasoning_effort: args.effort };
  let threadId = args.thread;
  if (threadId) {
    recordThread(threadId);
    await request('thread/resume', { ...params, threadId, excludeTurns: true });
  } else {
    const started = await request('thread/start', { ...params, threadSource: 'user' });
    threadId = started.thread.id;
    recordThread(threadId);
    if (args.name) await request('thread/name/set', { threadId, name: args.name });
  }
  process.stderr.write(`[driver] thread ${threadId}\n`);

  const turnParams = { threadId, input: [{ type: 'text', text: prompt, text_elements: [] }] };
  if (args.effort) turnParams.effort = args.effort;
  const turn = await request('turn/start', turnParams);
  turnId = turn.turn?.id ?? null;

  const result = await finished;
  const answer = finalText || lastText;
  if (args.out) fs.writeFileSync(args.out, answer);
  else process.stderr.write(answer + '\n');
  console.log(JSON.stringify({ agent: 'codex', threadId, turnId, status: result?.status, out: args.out || null }));
  child.kill();
  process.exit(result?.status === 'completed' ? 0 : 1);
} catch (error) {
  process.stderr.write(`[driver] ${error.message}\n`);
  child.kill();
  process.exit(2);
}
