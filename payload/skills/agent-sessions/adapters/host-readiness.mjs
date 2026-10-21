// Inspect a private Codex prompt preview. Never start clients or emit its text.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

export function inspectHost({ client, version, promptInput } = {}) {
  const report = {
    capability: 'adapter-session-host', mode: 'adapter-sessions',
    client: ['codex', 'claude-code', 'generic'].includes(client) ? client : 'unknown',
    host_version: /^(?:codex-cli )?\d+\.\d+\.\d+$/.test(version || '') ? version.replace(/^codex-cli /, '') : null,
    status: 'unverified', scope: 'supplied-prompt-preview', active_session: 'unverified',
    reason: 'no-prompt-evidence',
    limits: 'A CLI preview is not the active desktop session. Absence of known markers is not proof of model compliance; no configuration is changed.',
  };
  if (!promptInput) return report;
  let bytes, messages;
  try {
    const stat = fs.statSync(promptInput);
    if (!stat.isFile() || stat.size > 2 * 1024 * 1024) throw new Error('evidence-size');
    bytes = fs.readFileSync(promptInput);
    report.evidence_sha256 = crypto.createHash('sha256').update(bytes).digest('hex');
    messages = JSON.parse(bytes.toString('utf8'));
    if (!Array.isArray(messages) || !messages.length || !messages.every(message =>
      message?.type === 'message' && ['system', 'developer', 'user', 'assistant'].includes(message.role) &&
      Array.isArray(message.content) && message.content.every(part =>
        ['input_text', 'output_text', 'text'].includes(part?.type) && typeof part.text === 'string'))) {
      throw new Error('evidence-shape');
    }
  } catch {
    return { ...report, reason: 'unreadable-or-unsupported-evidence' };
  }
  if (report.client !== 'codex') return { ...report, reason: 'unsupported-host-client' };
  const instructions = messages.filter(message => ['system', 'developer'].includes(message.role))
    .flatMap(message => message.content.map(part => part.text));
  if (!instructions.some(text => text.trim())) return { ...report, reason: 'missing-host-instructions' };
  // Narrow mode signature observed in 0.160.1, not a natural-language policy parser.
  // Merely exposing native tools does not prove that the client requires their use.
  if (instructions.some(text => [...text.matchAll(/<multi_agent_mode>([\s\S]*?)<\/multi_agent_mode>/g)]
    .some(match => /\bproactive\b/i.test(match[1]) && /\bactive\b/i.test(match[1]) &&
      !/\b(?:not|disabled|inactive)\b/i.test(match[1])))) {
    return { ...report, status: 'conflict', reason: 'native-orchestration-present' };
  }
  if (instructions.some(text => /<multi_agent_(?:role|mode)>/.test(text))) {
    return { ...report, reason: 'native-tools-without-recognized-active-mode' };
  }
  if (report.host_version !== '0.160.1') return { ...report, reason: 'unverified-host-version' };
  return { ...report, status: 'compatible', reason: 'no-known-native-orchestration-in-preview' };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const args = {};
    for (let i = 2; i < process.argv.length; i += 2) {
      const key = process.argv[i];
      if (!['--client', '--version', '--prompt-input'].includes(key) || !process.argv[i + 1]) throw new Error('options');
      args[key.slice(2)] = process.argv[i + 1];
    }
    console.log(JSON.stringify(inspectHost({ client: args.client, version: args.version, promptInput: args['prompt-input'] })));
  } catch {
    console.error('[diagnostic] expected --client, --version and optional --prompt-input');
    process.exitCode = 4;
  }
}
