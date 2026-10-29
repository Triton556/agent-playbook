#!/usr/bin/env node
// Claude Code adapter for the personal knowledge vault.
// Scheduled sync hash-checks its reviewed local copy of kb.mjs.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { DEFAULT_ROOT, capture, checkpoint, hook } from './kb.mjs';

const SCRIPT = fileURLToPath(import.meta.url).replaceAll('\\', '/');
const LABEL = 'Claude Code';
const IDENTITY = /^[a-zA-Z0-9:._-]{1,128}$/;
const digest = value => crypto.createHash('sha256').update(value).digest('hex');

function currentFile(root, session) {
  return path.join(root, '.kb/claude', `${digest(session).slice(0, 32)}.json`);
}
function readCurrent(root, session) {
  try { return JSON.parse(fs.readFileSync(currentFile(root, session), 'utf8')); } catch { return null; }
}
function writeCurrent(root, session, turn) {
  const file = currentFile(root, session);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temp = `${file}.${crypto.randomUUID()}.tmp`;
  fs.writeFileSync(temp, JSON.stringify({ session_id: session, turn_id: turn, started_at: new Date().toISOString() }) + '\n', { mode: 0o600 });
  fs.renameSync(temp, file);
}
function instruction(root, session, turn) {
  const base = `node ${SCRIPT}`;
  return `Danil's personal knowledge base: ${root.replaceAll('\\', '/')}. Use kb-find for context about Danil or his projects. `
    + `Before finishing, save new useful knowledge from this turn through kb-save: JSON on stdin to ${base} capture. Write knowledge in Russian. `
    + `source={"kind":"claude","session_id":"${session}","turn_id":"${turn}"}. `
    + `If nothing is new: ${base} checkpoint --session ${session} --turn ${turn}. `
    + `No secrets or full chats; distinguish hypotheses from facts; Danil's prohibition on saving takes precedence.`;
}

export function claudeHook(root, input) {
  const session = input?.session_id;
  if (typeof session !== 'string' || !IDENTITY.test(session)) throw new Error('Hook input is missing a valid session_id');
  if (input.hook_event_name === 'UserPromptSubmit') {
    const turn = `c${Date.now().toString(36)}${crypto.randomBytes(4).toString('hex')}`;
    writeCurrent(root, session, turn);
    // kb.hook marks the turn as started and records the event without prompt text.
    hook(root, { hook_event_name: 'UserPromptSubmit', session_id: session, turn_id: turn });
    return { hookSpecificOutput: { hookEventName: 'UserPromptSubmit', additionalContext: instruction(root, session, turn) } };
  }
  if (input.hook_event_name === 'Stop') {
    const current = readCurrent(root, session);
    if (!current?.turn_id) return {};
    const result = hook(root, { hook_event_name: 'Stop', session_id: session, turn_id: current.turn_id, stop_hook_active: Boolean(input.stop_hook_active) });
    if (result.decision === 'block') return { decision: 'block', reason: instruction(root, session, current.turn_id) + ' This is a one-time persistence check; do not repeat the main answer.' };
    return result;
  }
  return {};
}

export function claudeCapture(root, input) {
  if (!input || typeof input !== 'object') throw new Error('Invalid input JSON');
  const source = input.source || {};
  if (source.kind !== 'claude') throw new Error('source.kind must be "claude"');
  // The vault schema has no "claude" kind yet; "manual" with a label keeps the origin visible.
  const label = source.label ? `${LABEL} · ${source.label}` : LABEL;
  return capture(root, { ...input, source: { kind: 'manual', session_id: source.session_id, turn_id: source.turn_id, label: label.slice(0, 256) } });
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) out[argv[i].slice(2)] = argv[++i]; else out._.push(argv[i]);
  }
  return out;
}
async function readStdin() {
  let data = '';
  for await (const chunk of process.stdin) { data += chunk; if (data.length > 1024 * 1024) throw new Error('Input too large'); }
  try { return JSON.parse(data.replace(/^﻿/, '')); } catch { throw new Error('Invalid input JSON'); }
}
async function main() {
  const args = parseArgs(process.argv.slice(2));
  const root = args.root ? path.resolve(args.root) : DEFAULT_ROOT;
  const command = args._[0];
  try {
    let result;
    if (command === 'hook') result = claudeHook(root, await readStdin());
    else if (command === 'capture') result = claudeCapture(root, await readStdin());
    else if (command === 'checkpoint') result = checkpoint(root, { session_id: args.session, turn_id: args.turn });
    else throw new Error('Commands: hook, capture, checkpoint');
    process.stdout.write(JSON.stringify(result) + '\n');
  } catch (error) {
    // A broken memory hook must not block the conversation; it reports and lets the turn finish.
    if (command === 'hook') { process.stdout.write(JSON.stringify({ systemMessage: 'Claude personal memory hook error; inspect .kb/hook-events.jsonl.' }) + '\n'); return; }
    process.stderr.write(error.message + '\n');
    process.exitCode = 1;
  }
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
