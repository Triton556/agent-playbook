#!/usr/bin/env node
// Run one turn in a Codex thread that is visible in the Codex app.
//
//   node codex-chat.mjs --cwd <dir> --name "<title>" [--prompt brief.md] [--out final.md]
//        [--log events.jsonl] [--thread <id>] [--model <id>] [--effort <level>]
//        [--sandbox workspace-write|read-only|danger-full-access] [--proxy]
//
// The prompt comes from --prompt or stdin. Without --thread a new thread is started;
// with --thread the prompt becomes the next turn of that thread.
// The last stdout line is JSON: {threadId, turnId, status, out}.
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

const FLAGS = new Set(['proxy']);
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

const cwd = path.resolve(args.cwd || process.cwd());
const prompt = args.prompt ? fs.readFileSync(args.prompt, 'utf8') : fs.readFileSync(0, 'utf8');
if (!prompt.trim()) throw new Error('Empty prompt');
if (!fs.existsSync(cwd)) throw new Error(`cwd does not exist: ${cwd}`);

const child = spawn(findCodex(), args.proxy ? ['app-server', 'proxy'] : ['app-server'], { stdio: ['pipe', 'pipe', 'pipe'] });
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

try {
  await request('initialize', {
    clientInfo: { name: 'codex-sessions-driver', title: 'Codex sessions driver', version: '1.0.0' },
    capabilities: { experimentalApi: true, requestAttestation: false },
  });
  send({ method: 'initialized' });

  // Resume does not keep the sandbox of the earlier run, so pass it every time.
  const params = { cwd, sandbox: args.sandbox || 'workspace-write', approvalPolicy: 'never' };
  if (args.model) params.model = args.model;
  let threadId = args.thread;
  if (threadId) {
    await request('thread/resume', { ...params, threadId, excludeTurns: true });
  } else {
    const started = await request('thread/start', { ...params, threadSource: 'user' });
    threadId = started.thread.id;
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
  console.log(JSON.stringify({ threadId, turnId, status: result?.status, out: args.out || null }));
  child.kill();
  process.exit(result?.status === 'completed' ? 0 : 1);
} catch (error) {
  process.stderr.write(`[driver] ${error.message}\n`);
  child.kill();
  process.exit(2);
}
