#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { atomicJSON, readStatus, runDirectory, statusPath, terminal, killTree } from './run-runtime.mjs';

async function main() {
  const args = {};
  for (let i = 2; i < process.argv.length; i++) {
    const key = process.argv[i];
    if (key === '--status') args.status = true;
    else if (['--runs', '--run-dir', '--mode', '--timeout', '--cancel'].includes(key) && process.argv[i + 1] && !process.argv[i + 1].startsWith('--')) args[key.slice(2)] = process.argv[++i];
    else throw new Error(`Invalid option: ${key}`);
  }
  const mode = args.mode || 'all';
  const timeout = Number(args.timeout ?? 540);
  if (!['any', 'all'].includes(mode) || !Number.isFinite(timeout) || timeout < 0 || timeout > 2147483) throw new Error('Invalid mode or timeout');
  if (args.cancel && (args.runs || args.status)) throw new Error('--cancel cannot be combined with --runs or --status');
  const ids = [...new Set((args.cancel || args.runs || '').split(',').filter(Boolean))];
  if (!ids.length || (args.cancel && ids.length !== 1)) throw new Error('Supply --runs <id,id,...> or --cancel <id>');
  const dir = runDirectory(args);
  const files = ids.map(id => statusPath(dir, id));
  const watchedNames = new Set(files.map(file => path.basename(file)));
  // Validate every id before cancellation or entering a wait.
  files.forEach(readStatus);
  if (args.cancel) {
    const status = readStatus(files[0]);
    if (!terminal(status.status)) {
      killTree(status.pid);
      atomicJSON(files[0], { ...readStatus(files[0]), status: 'interrupted', exitCode: 1, endedAt: new Date().toISOString() });
    }
  }
  const snapshot = () => {
    const done = [], running = [];
    files.forEach((file, index) => {
      const status = readStatus(file);
      if (terminal(status.status)) done.push({ runId: ids[index], status: status.status,
        threadId: status.threadId ?? null, exitCode: status.exitCode ?? null, out: status.out ?? null });
      else running.push(ids[index]);
    });
    return { done, running, timedOut: false };
  };
  const satisfied = result => mode === 'any' ? result.done.length > 0 : result.running.length === 0;
  if (args.status || args.cancel) { console.log(JSON.stringify(snapshot())); return; }
  let watcher, interval, timer;
  try {
    const result = await new Promise((resolve, reject) => {
      let ended = false;
      const check = (expired = false) => {
        if (ended) return;
        try {
          const result = snapshot();
          if (satisfied(result) || expired) {
            ended = true;
            result.timedOut = !satisfied(result);
            resolve(result);
          }
        } catch (error) { ended = true; reject(error); }
      };
      // Watch the directory, since each atomic write replaces the file inode.
      try {
        watcher = fs.watch(dir, (_event, filename) => {
          if (!filename || watchedNames.has(String(filename))) check();
        });
        watcher.on('error', () => watcher.close());
      }
      catch { /* Filesystems without watch support use the slow fallback. */ }
      interval = setInterval(check, 2000);
      timer = setTimeout(() => check(true), timeout * 1000);
      check(); // After installing the watch: no missed completion at startup.
    });
    console.log(JSON.stringify(result));
    process.exitCode = result.timedOut ? 5 : 0;
  } finally { watcher?.close(); clearInterval(interval); clearTimeout(timer); }
}
try { await main(); }
catch (error) { console.error(`[wait] ${error.message}`); process.exitCode = 2; }
