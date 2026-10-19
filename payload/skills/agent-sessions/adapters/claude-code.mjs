#!/usr/bin/env node
// agent-sessions adapter for Claude Code (contract 1, see references/contract.md).
// Runs one turn of a headless Claude Code session (`claude -p`).
// Checked 2026-10-19 on Windows, Claude Code 2.1.299: describe/exit 4, and a missing login is reported
// as a failure. Live task checks (new, continue, access modes, visibility) not yet run.
//
//   node claude-code.mjs --describe
//   node claude-code.mjs --cwd <dir> --name "<title>" [--prompt brief.md] [--out final.md]
//        [--log events.jsonl] [--thread <session-id>] [--model <id>] [--effort <level>]
//        [--sandbox workspace-write|read-only|danger-full-access]
//
// Uses the user's own Claude Code login, settings, skills and hooks.
// Nothing prompts: anything that would ask for permission is denied (--permission-prompts none).
import { spawn, spawnSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import readline from 'node:readline';

const FLAGS = new Set(['describe']);
const args = {};
for (let i = 2; i < process.argv.length; i++) {
  const key = process.argv[i].replace(/^--/, '');
  if (FLAGS.has(key)) args[key] = true;
  else args[key] = process.argv[++i];
}

// Claude Code has permission modes, not an OS sandbox; the descriptions say exactly that.
const MODES = {
  'read-only': ['--permission-mode', 'plan'],
  'workspace-write': ['--permission-mode', 'acceptEdits'],
  'danger-full-access': ['--permission-mode', 'bypassPermissions'],
};
const DESCRIPTION = {
  agent: 'claude-code',
  contract: 1,
  verified: false,
  visible_in: 'Claude Code session history for --cwd: `claude --resume` in a terminal opened in that folder lists it by name. Not guaranteed to appear in the desktop app.',
  resume: true,
  access_modes: {
    'read-only': 'permission mode "plan": reads and searches files, makes no edits and runs no changing commands',
    'workspace-write': 'permission mode "acceptEdits": file edits inside --cwd are accepted; shell commands run only if the user\'s Claude Code settings already allow them, everything else is denied. Not an OS sandbox.',
    'danger-full-access': 'permission mode "bypassPermissions": every tool, command and file without checks',
  },
  effort: ['low', 'medium', 'high', 'xhigh', 'max'],
  notes: 'UNVERIFIED: live task checks have not been run. Needs a Claude Code CLI that is logged in on its own (run `claude` once and /login). The CLI bundled with the desktop app gets its login from the app and reports "Not logged in" when started separately.',
};
if (args.describe) {
  console.log(JSON.stringify(DESCRIPTION, null, 2));
  process.exit(0);
}
const sandbox = args.sandbox || 'workspace-write';
if (!MODES[sandbox]) {
  process.stderr.write(`[driver] unsupported access mode: ${sandbox}\n`);
  process.exit(4);
}

function findClaude() {
  if (process.env.CLAUDE_BIN) return process.env.CLAUDE_BIN;
  const which = spawnSync(process.platform === 'win32' ? 'where' : 'which', ['claude'], { encoding: 'utf8' });
  const onPath = which.status === 0 && which.stdout.split(/\r?\n/).find(Boolean);
  if (onPath) return onPath.trim();
  const home = os.homedir();
  const candidates = [path.join(home, '.local/bin/claude'), path.join(home, '.claude/local/claude')];
  // Builds kept by the desktop app: <base>/<version>/<build>/claude(.exe).
  const bases = process.platform === 'win32'
    ? [path.join(process.env.APPDATA || path.join(home, 'AppData/Roaming'), 'Claude/claude-code')]
    : [path.join(home, 'Library/Application Support/Claude/claude-code')];
  for (const base of bases) {
    if (!fs.existsSync(base)) continue;
    for (const version of fs.readdirSync(base)) {
      const dir = path.join(base, version);
      if (!fs.statSync(dir).isDirectory()) continue;
      for (const build of fs.readdirSync(dir)) candidates.push(path.join(dir, build, process.platform === 'win32' ? 'claude.exe' : 'claude'));
    }
  }
  const found = candidates.filter(f => fs.existsSync(f)).sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs);
  if (found[0]) return found[0];
  return null;
}

const cwd = path.resolve(args.cwd || process.cwd());
if (!fs.existsSync(cwd)) {
  process.stderr.write(`[driver] cwd does not exist: ${cwd}\n`);
  process.exit(4);
}
const prompt = args.prompt ? fs.readFileSync(args.prompt, 'utf8') : fs.readFileSync(0, 'utf8');
if (!prompt.trim()) {
  process.stderr.write('[driver] empty prompt\n');
  process.exit(4);
}
const bin = findClaude();
if (!bin) {
  process.stderr.write('[driver] Claude Code CLI not found. Set CLAUDE_BIN to the claude executable. No session was created.\n');
  process.exit(3);
}

// A new session gets its id up front, so it is known even if the run fails midway.
const threadId = args.thread || crypto.randomUUID();
const cli = ['-p', '--output-format', 'stream-json', '--verbose', '--permission-prompts', 'none', ...MODES[sandbox]];
if (args.thread) cli.push('--resume', args.thread);
else {
  cli.push('--session-id', threadId);
  if (args.name) cli.push('--name', args.name);
}
if (args.model) cli.push('--model', args.model);
if (args.effort) cli.push('--effort', args.effort);

// When the orchestrator is itself a Claude Code session, drop the host's session variables
// so the worker is a separate top-level session with its own login.
const env = { ...process.env };
for (const key of Object.keys(env)) {
  if (key === 'CLAUDECODE' || key.startsWith('CLAUDE_CODE_') || key.startsWith('CLAUDE_AGENT_SDK') || key === 'CLAUDE_PID' || key === 'CLAUDE_EFFORT') delete env[key];
}

const child = spawn(bin, cli, { cwd, env, stdio: ['pipe', 'pipe', 'pipe'] });
const log = args.log ? fs.createWriteStream(args.log, { flags: 'a' }) : null;
let stderrText = '';
child.stderr.on('data', chunk => { stderrText += chunk; if (args.verbose) process.stderr.write(chunk); });
child.on('error', error => {
  process.stderr.write(`[driver] cannot start Claude Code: ${error.code || error.message}. No session was created.\n`);
  process.exit(3);
});
child.stdin.end(prompt);

let result = null;
let lastText = '';
readline.createInterface({ input: child.stdout }).on('line', line => {
  if (!line.trim()) return;
  log?.write(line + '\n');
  let msg;
  try { msg = JSON.parse(line); } catch { return; }
  if (msg.type === 'assistant') {
    for (const part of msg.message?.content || []) {
      if (part.type === 'text') lastText = part.text;
      if (part.type === 'tool_use') {
        const detail = part.input?.command || part.input?.file_path || part.input?.pattern || '';
        process.stderr.write(`[tool] ${part.name} ${String(detail).slice(0, 140)}\n`);
      }
    }
  }
  if (msg.type === 'result') result = msg;
});

child.on('close', code => {
  const answer = result?.result ?? lastText;
  if (args.out) fs.writeFileSync(args.out, answer || '');
  else process.stderr.write((answer || '') + '\n');
  let status;
  if (result && !result.is_error && result.subtype === 'success') status = 'completed';
  else if (result) status = `failed: ${result.subtype}${result.is_error && answer ? ': ' + String(answer).slice(0, 200) : ''}`;
  else status = `failed: claude exited with ${code}${stderrText ? ': ' + stderrText.trim().split('\n').pop().slice(0, 200) : ''}`;
  console.log(JSON.stringify({ agent: 'claude-code', threadId: result?.session_id || threadId, status, out: args.out || null }));
  process.exit(status === 'completed' ? 0 : 1);
});
