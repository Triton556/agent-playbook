#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

// This runner and kb.mjs are copied to an ignored, local runtime at installation.
// Downloaded script changes require review and reinstallation before execution.
const hashFile = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const startedAt = new Date().toISOString();
let recordFolder;
let renderReviewedStatus;
function writeRecord(name, value) {
  const file = path.join(recordFolder, name);
  const temp = `${file}.${crypto.randomUUID()}.tmp`;
  fs.writeFileSync(temp, JSON.stringify(value, null, 2) + '\n');
  fs.renameSync(temp, file);
}
try {
  if (process.argv.length !== 4 || process.argv[2] !== '--manifest') throw new Error('Expected --manifest <local installation.json>');
  const manifestPath = path.resolve(process.argv[3]);
  const install = JSON.parse(fs.readFileSync(manifestPath, 'utf8').replace(/^\uFEFF/, ''));
  const root = path.resolve(install.vault);
  if (manifestPath !== path.join(root, '.kb/scheduler/installation.json')) throw new Error('Installation path does not match the vault');
  recordFolder = path.dirname(manifestPath);
  const runtimeFolder = path.dirname(fileURLToPath(import.meta.url));
  if (runtimeFolder !== path.join(recordFolder, 'runtime')) throw new Error('Use the installed local runtime');
  const runtimeCore = path.join(runtimeFolder, 'kb.mjs');
  if (hashFile(runtimeCore) !== install.core_sha256 || hashFile(fileURLToPath(import.meta.url)) !== install.runner_sha256) throw new Error('Installed runtime changed; review before reinstalling');
  // Only the integrity-checked installed module may refresh local status.
  const reviewedCore = await import(pathToFileURL(runtimeCore).href);
  renderReviewedStatus = () => reviewedCore.renderStatus(root);
  if (hashFile(path.join(root, 'SYSTEM/scripts/kb.mjs')) !== install.core_sha256 || hashFile(path.join(root, 'SYSTEM/scripts/scheduled-sync.mjs')) !== install.runner_sha256) throw new Error('Repository scripts changed; review and reinstall the scheduler runtime');
  process.env.PATH = path.dirname(install.git) + path.delimiter + (process.env.PATH || '');
  const result = reviewedCore.sync(root);
  const record = { schema_version: 1, task: install.task_name, started_at: startedAt, completed_at: new Date().toISOString(), status: 'ok', last_sync_at: result.at };
  writeRecord('latest-run.json', record);
  writeRecord('last-success.json', record);
  renderReviewedStatus();
  console.log(JSON.stringify(record));
} catch (error) {
  const record = { schema_version: 1, started_at: startedAt, completed_at: new Date().toISOString(), status: 'failed', error: error.message };
  if (recordFolder) writeRecord('latest-run.json', record);
  try { renderReviewedStatus?.(); } catch {} // Never import an unverified module on failure.
  console.error(JSON.stringify(record));
  process.exitCode = 1;
}
