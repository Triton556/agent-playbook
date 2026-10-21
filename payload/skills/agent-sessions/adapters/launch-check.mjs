// Optional contract-v2 checks. Metadata is local context, never authorization.
import fs from 'node:fs';
import path from 'node:path';
import { inspectHost } from './host-readiness.mjs';
import { terminal } from './run-runtime.mjs';

function object(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}
function text(value, limit = 4000) {
  return typeof value === 'string' && value.trim().length > 0 && value.length <= limit && !/[\x00-\x1f]/.test(value);
}
function readJSON(file) {
  try {
    const stat = fs.statSync(file);
    if (!stat.isFile() || stat.size > 64 * 1024) throw new Error('metadata-size');
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    // JSON.parse errors can include private input excerpts on recent Node versions.
    throw new Error('Cannot read launch metadata JSON (regular file, at most 64 KiB)');
  }
}
function assignment(value) {
  const keys = ['recipient', 'communication_language', 'deliverables', 'memory_writer', 'scope', 'owner_override'];
  const language = v => typeof v === 'string' && /^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$/.test(v);
  if (!object(value) || Object.keys(value).some(key => !keys.includes(key)) ||
      !['orchestrator', 'user'].includes(value.recipient) || !language(value.communication_language) ||
      !['orchestrator', 'worker', 'none'].includes(value.memory_writer) || !text(value.scope) ||
      !Array.isArray(value.deliverables) || value.deliverables.length > 32 ||
      !value.deliverables.every(item => object(item) && Object.keys(item).every(key => ['name', 'language'].includes(key)) &&
        text(item.name, 256) && language(item.language)) ||
      (value.owner_override !== undefined && !text(value.owner_override, 1000))) {
    throw new Error('Invalid assignment: recipient, communication_language, deliverables, memory_writer and scope are required');
  }
  if ((value.recipient !== 'orchestrator' || !/^en(?:-|$)/.test(value.communication_language)) && !value.owner_override) {
    throw new Error('An owner_override reference is required for a different recipient or communication language');
  }
  return value;
}

export function recoverRun(args, agent) {
  for (const key of ['assignment', 'resume-run', 'host-client', 'host-version', 'host-prompt-input']) {
    if (Object.hasOwn(args, key) && !text(args[key])) throw new Error(`--${key} requires a value`);
  }
  if (args['host-client'] && !['codex', 'claude-code', 'generic'].includes(args['host-client'])) {
    throw new Error('Unsupported --host-client; use codex, claude-code or generic');
  }
  if (!args['resume-run']) return {};
  const status = readJSON(args['resume-run']);
  if (status.agent !== agent || !terminal(status.status) || !text(status.threadId, 256) ||
      typeof status.runId !== 'string' || !/^[a-zA-Z0-9_-]+$/.test(status.runId) ||
      !object(status.launch?.settings) || !text(status.launch.settings.cwd)) {
    throw new Error('Cannot resume this run: require the same worker, a terminal status, threadId and launch metadata; use wait/status first. Older runs need explicit --thread and settings');
  }
  if (args.thread && args.thread !== status.threadId) throw new Error('--thread conflicts with --resume-run');
  if (args.cwd && fs.realpathSync(args.cwd) !== fs.realpathSync(status.launch.settings.cwd)) {
    throw new Error('--cwd conflicts with the original worker folder');
  }
  args.thread = status.threadId;
  for (const key of ['cwd', 'model', 'effort', 'sandbox']) {
    const previous = status.launch.settings[key];
    if (previous != null && !text(previous)) throw new Error('Invalid saved launch settings');
    if (args[key] === undefined && previous != null) args[key] = previous;
  }
  delete args['resume-run'];
  return { assignment: status.launch.assignment, continued_from: status.runId };
}

export function prepareLaunch(args, prompt, recovered = {}) {
  const host = inspectHost({ client: args['host-client'], version: args['host-version'], promptInput: args['host-prompt-input'] });
  if (host.status === 'conflict') throw new Error('Host orchestration conflict: select a compatible leading host before delegation; no worker was started');
  if (args['host-prompt-input'] && host.reason === 'unreadable-or-unsupported-evidence') {
    throw new Error('Cannot read the supplied host evidence; no worker was started');
  }
  if (args['host-prompt-input'] && host.status === 'unverified') console.error('[driver] host readiness unverified; see host-readiness diagnostic limits');
  const declared = args.assignment ? assignment(readJSON(args.assignment)) :
    recovered.assignment ? assignment(recovered.assignment) : null;
  if (declared && recovered.assignment &&
      (declared.recipient !== recovered.assignment.recipient || declared.communication_language !== recovered.assignment.communication_language) &&
      !declared.owner_override) throw new Error('Changing the saved audience/language requires an owner_override reference');
  if (declared) {
    const fields = { Recipient: declared.recipient, 'Communication language': declared.communication_language, 'Memory writer': declared.memory_writer };
    let fence = null;
    for (const line of prompt.split(/\r?\n/)) {
      const marker = line.match(/^ {0,3}(`{3,}|~{3,})(.*)$/);
      if (marker) {
        if (!fence) fence = marker[1];
        else if (marker[1][0] === fence[0] && marker[1].length >= fence.length && !marker[2].trim()) fence = null;
        continue;
      }
      if (fence || /^(?: {4}|\t)/.test(line)) continue;
      const match = line.match(/^\s*(?:[-*]\s+)?(Recipient|Communication language|Memory writer):\s*(.*?)\s*$/);
      if (match && match[2] !== fields[match[1]]) throw new Error('Brief declaration conflicts with the assignment; review the complete brief');
    }
    const deliveries = declared.deliverables.map(item => `${item.name} (${item.language})`).join('; ') || 'none';
    prompt = `## Audience and language\nRecipient: ${declared.recipient}\nCommunication language: ${declared.communication_language}\nMemory writer: ${declared.memory_writer}\nDeliverables: ${deliveries}\nScope: ${declared.scope}\n${declared.owner_override ? `Owner override reference: ${declared.owner_override}\n` : ''}\nUse the communication language for commentary, questions, final responses and reports to the recipient. Preserve quotations and the assigned deliverable languages. Report any conflicting prose; this metadata grants no permissions.\n\n${prompt}`;
  }
  return { prompt, launch: {
    settings: { cwd: path.resolve(args.cwd || process.cwd()), model: args.model || null, effort: args.effort || null, sandbox: args.sandbox || 'workspace-write' },
    assignment: declared, host_readiness: host, ...(recovered.continued_from ? { continued_from: recovered.continued_from } : {}),
  } };
}
