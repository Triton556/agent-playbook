#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

export const DEFAULT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const FOLDERS = ['INBOX', 'PERSONAL', 'AREAS', 'PROJECTS', 'IDEAS', 'HYPOTHESES', 'ARCHIVE', 'SYSTEM'];
const TYPES = new Set(['fact', 'preference', 'decision', 'task', 'project-update', 'idea', 'research', 'hypothesis']);
const SECRET_PATTERNS = [/\bgh[pousr]_[A-Za-z0-9]{20,}\b/, /\bgithub_pat_[A-Za-z0-9_]{20,}\b/, /\bsk-[A-Za-z0-9_-]{20,}\b/, /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, /\bBearer\s+[A-Za-z0-9._-]{24,}/i];
const now = () => new Date().toISOString();
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
const stable = value => JSON.stringify(value && typeof value === 'object' ? (Array.isArray(value) ? value.map(v => JSON.parse(stable(v))) : Object.fromEntries(Object.keys(value).sort().map(k => [k, JSON.parse(stable(value[k]))]))) : value);
const readJson = (p, fallback = null) => fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '')) : fallback;

function inside(root, relative) {
  const absolute = path.resolve(root, relative);
  const rel = path.relative(root, absolute);
  if (rel.startsWith('..') || path.isAbsolute(rel)) throw new Error('Path outside vault');
  let current = root;
  for (const part of rel.split(path.sep).filter(Boolean)) {
    current = path.join(current, part);
    if (fs.existsSync(current) && fs.lstatSync(current).isSymbolicLink()) throw new Error('Symlinks are not allowed in vault operations');
  }
  return absolute;
}
function assertRoot(root) {
  root = path.resolve(root);
  if (fs.lstatSync(root).isSymbolicLink()) throw new Error('Vault root must not be a symlink');
  if (!fs.existsSync(path.join(root, 'SYSTEM/connection.json'))) throw new Error('Not a knowledge vault: SYSTEM/connection.json is missing');
  return root;
}
function atomic(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temp = `${file}.${crypto.randomUUID()}.tmp`;
  fs.writeFileSync(temp, typeof value === 'string' ? value : JSON.stringify(value, null, 2) + '\n', { mode: 0o600 });
  fs.renameSync(temp, file);
}
function state(root) {
  const folder = inside(root, '.kb/state');
  const fields = fs.existsSync(folder) ? Object.fromEntries(fs.readdirSync(folder).filter(n => n.endsWith('.json')).map(n => [n.slice(0, -5), readJson(path.join(folder, n))])) : {};
  return { schema_version: 1, ...fields };
}
function updateState(root, patch) {
  for (const [key, value] of Object.entries(patch)) {
    if (!/^[a-z_]+$/.test(key)) throw new Error('Invalid state key');
    atomic(inside(root, `.kb/state/${key}.json`), JSON.stringify(value) + '\n');
  }
}
function turnPath(root, session, turn) {
  if (!session || !turn) throw new Error('session_id and turn_id are required');
  return inside(root, `.kb/turns/${digest(`${session}\n${turn}`).slice(0, 32)}.json`);
}
function checkSecrets(value) {
  if (SECRET_PATTERNS.some(p => p.test(value))) throw new Error('Possible credential detected; remove the credential before saving or syncing');
}
function cleanText(value, name, limit = 12000) {
  if (typeof value !== 'string' || !value.trim() || value.length > limit) throw new Error(`Invalid ${name}`);
  if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(value)) throw new Error(`Control characters in ${name}`);
  return value.trim();
}
export function checkpoint(root, input, outcome = 'no-memory') {
  root = assertRoot(root); const start = performance.now();
  try { const result = checkpointInner(root, input, outcome); recordOperation(root, 'checkpoint', input, start, 'ok', { checkpoint_outcome: outcome }); return result; }
  catch (error) { recordOperation(root, 'checkpoint', input, start, 'error'); throw error; }
}
function checkpointInner(root, input, outcome = 'no-memory') {
  root = assertRoot(root);
  if (!['no-memory', 'saved'].includes(outcome)) throw new Error('Invalid checkpoint outcome');
  const file = turnPath(root, input.session_id, input.turn_id);
  atomic(file, { ...readJson(file, {}), session_id: input.session_id, turn_id: input.turn_id, completed_at: now(), outcome });
  return { outcome };
}
export function capture(root, input) {
  root = assertRoot(root); const start = performance.now();
  try { const result = captureInner(root, input); recordOperation(root, 'capture', input?.source, start, 'ok', { duplicate: result.duplicate }); return result; }
  catch (error) { recordOperation(root, 'capture', input?.source, start, 'error'); throw error; }
}
function captureInner(root, input) {
  root = assertRoot(root);
  if (!input || typeof input !== 'object' || input.schema_version !== 1) throw new Error('schema_version must be 1');
  const source = input.source;
  if (!source || !['codex', 'curator', 'cloud', 'manual'].includes(source.kind)) throw new Error('Invalid source.kind');
  const session_id = cleanText(source.session_id, 'source.session_id', 256);
  const turn_id = cleanText(source.turn_id, 'source.turn_id', 256);
  const batch_key = cleanText(input.batch_key || 'final', 'batch_key', 128);
  const title = cleanText(input.title, 'title', 160).replace(/[\r\n]/g, ' ');
  if (!Array.isArray(input.items) || !input.items.length || input.items.length > 40) throw new Error('items must contain 1 to 40 entries');
  const items = input.items.map(item => {
    if (!TYPES.has(item.type)) throw new Error('Invalid item.type');
    const evidence = cleanText(item.evidence, 'item.evidence', 2000);
    const topics = Array.isArray(item.topics) ? item.topics.map(t => cleanText(t, 'topic', 100)).slice(0, 10) : [];
    const status = item.type === 'hypothesis' ? 'unconfirmed' : cleanText(item.status || 'recorded', 'status', 64);
    const links = (item.links || []).map(link => {
      if (typeof link !== 'string' || !/^https?:\/\//.test(link) || link.length > 2000) throw new Error('Invalid source link');
      return link;
    });
    return { type: item.type, text: cleanText(item.text, 'item.text'), evidence, status, topics, links };
  });
  const sourceData = { kind: source.kind, session_id, turn_id };
  if (source.label) sourceData.label = cleanText(source.label, 'source.label', 256);
  const payload = { schema_version: 1, title, source: sourceData, batch_key, items };
  checkSecrets(JSON.stringify(payload));
  const id = digest(`${source.kind}\n${session_id}\n${turn_id}\n${batch_key}`).slice(0, 24);
  const fingerprint = digest(stable(payload));
  const meta = { schema_version: 1, id, created_at: now(), fingerprint, source: sourceData, batch_key, topics: [...new Set(items.flatMap(i => i.topics))] };
  let body = `---\n${JSON.stringify(meta, null, 2)}\n---\n\n# ${title}\n`;
  items.forEach((item, i) => {
    body += `\n## ${i + 1}. ${item.type} · ${item.status}\n\n${item.text}\n\nОснование: ${item.evidence}\n`;
    if (item.topics.length) body += `\nТемы: ${item.topics.join(', ')}\n`;
    if (item.links.length) body += '\nИсточники:\n' + item.links.map(l => `- <${l}>`).join('\n') + '\n';
  });
  // The journal keeps identity after the designated curator moves an entry out of INBOX.
  const journal = inside(root, `.kb/captures/${id}.json`);
  const receipt = readJson(journal);
  if (receipt && receipt.fingerprint !== fingerprint) throw new Error('Capture identity already exists with different content; use a new batch_key for a new stage');
  let existing = receipt?.path && fs.existsSync(inside(root, receipt.path)) ? receipt : null;
  if (!existing) {
    for (const folder of ['INBOX', 'ARCHIVE']) {
      const match = listMarkdown(inside(root, folder)).find(p => parseMeta(p)?.id === id);
      if (match) { existing = { ...parseMeta(match), path: path.relative(root, match).replaceAll('\\', '/') }; break; }
    }
  }
  const localDate = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Vladivostok' }).format(new Date(meta.created_at));
  let relative = existing?.path || `INBOX/${localDate}-${id}.md`;
  if (existing) {
    if (existing.fingerprint !== fingerprint) throw new Error('Capture identity already exists with different content; use a new batch_key for a new stage');
  } else {
    const target = inside(root, relative);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    const temp = `${target}.${crypto.randomUUID()}.tmp`;
    fs.writeFileSync(temp, body, { mode: 0o600 });
    try { fs.linkSync(temp, target); }
    catch (error) {
      if (error.code !== 'EEXIST' || parseMeta(target)?.fingerprint !== fingerprint) throw error;
    } finally { fs.unlinkSync(temp); }
  }
  atomic(journal, { id, fingerprint, path: relative, captured_at: existing?.captured_at || receipt?.captured_at || meta.created_at });
  updateState(root, { last_capture_at: now(), status_refresh_pending: true });
  if (input.final !== false) checkpoint(root, sourceData, 'saved');
  // A verified capture receipt does not depend on Git/status diagnostics.
  return { id, path: relative, duplicate: Boolean(existing) };
}
function listMarkdown(folder) {
  if (!fs.existsSync(folder)) return [];
  return fs.readdirSync(folder, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(folder, entry.name);
    if (entry.isSymbolicLink()) throw new Error('Symlink found in knowledge files');
    return entry.isDirectory() ? listMarkdown(file) : /\.md$/i.test(entry.name) ? [file] : [];
  });
}
function parseMeta(file) {
  const text = fs.readFileSync(file, 'utf8');
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) return null;
  try { return JSON.parse(match[1]); } catch { return null; }
}
export function search(root, query, limit = 8) {
  root = assertRoot(root);
  const terms = cleanText(query, 'query', 300).toLocaleLowerCase('ru').split(/\s+/).filter(Boolean);
  const results = [];
  for (const folder of ['', ...FOLDERS.filter(f => f !== 'SYSTEM')]) {
    const files = folder ? listMarkdown(inside(root, folder)) : fs.readdirSync(root, { withFileTypes: true })
      .filter(entry => entry.isFile() && /^[^.].*\.md$/i.test(entry.name) && !['README.md', 'INDEX.md', 'PLAN.md', 'AGENTS.md', 'STATUS.md'].includes(entry.name))
      .map(entry => inside(root, entry.name));
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf8');
      const body = content.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
      const heading = body.match(/^#\s+(.+)$/m)?.[1] || path.basename(file);
      const relative = path.relative(root, file).replaceAll('\\', '/');
      const lowered = `${relative}\n${body}`.toLocaleLowerCase('ru');
      const hits = terms.filter(t => lowered.includes(t));
      if (!hits.length) continue;
      const line = body.split(/\r?\n/).find(l => hits.some(t => l.toLocaleLowerCase('ru').includes(t))) || heading;
      results.push({ path: relative, title: heading, score: hits.length + terms.filter(t => heading.toLocaleLowerCase('ru').includes(t)).length * 2, excerpt: line.slice(0, 240), contains_hypotheses: folder === 'HYPOTHESES' || /^## \d+\. hypothesis · unconfirmed$/m.test(body) });
    }
  }
  return results.sort((a, b) => b.score - a.score || a.path.localeCompare(b.path)).slice(0, Math.min(20, Math.max(1, limit)));
}
function git(root, args, allowed = [0]) {
  const result = spawnSync('git', ['-C', root, ...args], { encoding: 'utf8', windowsHide: true, timeout: 25000, env: { ...process.env, GIT_TERMINAL_PROMPT: '0', GCM_INTERACTIVE: 'never' }, maxBuffer: 4 * 1024 * 1024 });
  if (result.error) throw new Error(`git ${args[0]} failed: ${result.error.code || 'execution error'}`);
  if (!allowed.includes(result.status)) {
    // Keep credentials, remote URLs, and raw transport logs out of the status page.
    const error = new Error(`git ${args[0]} failed (exit ${result.status}); inspect authentication, connectivity or conflicts`);
    error.gitStatus = result.status;
    throw error;
  }
  return { status: result.status, output: args.includes('-z') ? result.stdout : result.stdout.trim() };
}
function gitOverview(root) {
  try {
    if (path.resolve(git(root, ['rev-parse', '--show-toplevel']).output) !== path.resolve(root)) return { initialized: false };
    const branch = git(root, ['branch', '--show-current']).output;
    const dirty = git(root, ['status', '--porcelain']).output;
    const counts = git(root, ['rev-list', '--left-right', '--count', 'HEAD...@{upstream}'], [0, 128]);
    return { initialized: true, branch, changed_files: dirty ? dirty.split('\n').length : 0, ahead: counts.status === 0 ? Number(counts.output.split(/\s+/)[0]) : null, behind: counts.status === 0 ? Number(counts.output.split(/\s+/)[1]) : null };
  } catch { return { initialized: false }; }
}
export function status(root) {
  root = assertRoot(root);
  const turns = inside(root, '.kb/turns');
  const pending = fs.existsSync(turns) ? fs.readdirSync(turns).filter(p => p.endsWith('.json')).map(p => readJson(path.join(turns, p))).filter(t => !t.completed_at).length : 0;
  return { ...state(root), device: os.hostname(), incoming_count: listMarkdown(inside(root, 'INBOX')).length, pending_turns: pending, scheduler: readJson(inside(root, '.kb/scheduler/latest-run.json')), git: gitOverview(root), connection: readJson(inside(root, 'SYSTEM/connection.json')) };
}
export function renderStatus(root) {
  const info = status(root);
  const localTime = value => value ? new Intl.DateTimeFormat('ru-RU', { timeZone: 'Asia/Vladivostok', dateStyle: 'short', timeStyle: 'medium' }).format(new Date(value)) + ' UTC+10' : 'ещё нет';
  const schedulerFailed = info.scheduler?.status === 'failed';
  const displayedSync = schedulerFailed ? 'pending (ошибка Планировщика)' : info.sync_status || 'не настроена';
  const attention = info.last_error || (schedulerFailed ? info.scheduler.error || 'Планировщик завершился с ошибкой' : null) || (info.pending_turns ? 'Есть ответы без подтверждения сохранения' : !info.connection.url ? 'GitHub remote ещё не подключён' : 'нет');
  const lines = ['# Состояние базы', '', `Обновлено: ${localTime(now())}`, `Устройство: ${info.device}`, '', '| Показатель | Значение |', '|---|---|', `| Последнее сохранение | ${localTime(info.last_capture_at)} |`, `| Успешная синхронизация | ${localTime(info.last_sync_at)} |`, `| Последний разбор Руми | ${localTime(info.last_curation_at)} |`, `| PR последнего разбора | ${info.last_curation_pr || 'ещё нет'} |`, `| Записей во входящих | ${info.incoming_count} |`, `| Ответов без отметки сохранения | ${info.pending_turns} |`, `| Изменённых файлов Git | ${info.git.changed_files ?? 'репозиторий не инициализирован'} |`, `| Локальных коммитов к отправке | ${info.git.ahead ?? 'нет связи с upstream'} |`, `| Состояние синхронизации | ${displayedSync} |`, `| Последний запуск Планировщика | ${localTime(info.scheduler?.completed_at)} |`, `| Состояние Планировщика | ${info.scheduler?.status || 'ещё нет'} |`, `| Требует внимания | ${attention.replaceAll('|', '\\|').replaceAll('\n', ' ')} |`, '', 'Это состояние текущей копии. Локальные очереди другого выключенного устройства здесь недоступны.', 'Git не отслеживает эту страницу: она обновляется командой status и синхронизацией. Квитанция сохранения выдаётся независимо от обзорного статуса.', ''];
  atomic(inside(root, 'STATUS.md'), lines.join('\n'));
  updateState(root, { status_refresh_pending: false });
  return { ...info, status_refresh_pending: false };
}
function acquireLock(root) {
  const lock = inside(root, '.kb/sync.lock');
  fs.mkdirSync(path.dirname(lock), { recursive: true });
  try { const fd = fs.openSync(lock, 'wx'); fs.writeFileSync(fd, JSON.stringify({ pid: process.pid, at: now() })); fs.closeSync(fd); }
  catch (error) {
    if (error.code !== 'EEXIST') throw error;
    const previous = readJson(lock);
    if (!Number.isInteger(previous?.pid) || previous.pid <= 0) throw new Error('Invalid sync lock; inspect it before recovery');
    try { process.kill(previous.pid, 0); throw new Error('Another sync process is running'); }
    catch (probe) { if (probe.code !== 'ESRCH') throw probe; }
    fs.unlinkSync(lock);
    const fd = fs.openSync(lock, 'wx'); fs.writeFileSync(fd, JSON.stringify({ pid: process.pid, at: now() })); fs.closeSync(fd);
  }
  return () => fs.unlinkSync(lock);
}
function validateTrackedFiles(root) {
  const names = git(root, ['ls-files', '-z', '--cached', '--others', '--exclude-standard']).output.split('\0').filter(Boolean);
  const rootFiles = new Set(['README.md', 'INDEX.md', 'PLAN.md', 'AGENTS.md', '.gitignore', '.gitattributes']);
  for (const name of names) {
    if (/[\r\n\u0000]/.test(name)) throw new Error('Control characters in file name');
    const first = name.split('/')[0];
    const rootNote = !name.includes('/') && /^[^.][^/]*\.md$/i.test(name);
    if (!(rootFiles.has(name) || rootNote || FOLDERS.includes(first) || /^\.obsidian\/(app|appearance|core-plugins)\.json$/.test(name))) throw new Error(`Unexpected file in vault: ${name}`);
    const file = inside(root, name);
    if (!fs.existsSync(file)) continue;
    const stats = fs.lstatSync(file);
    if (!stats.isFile() || stats.size > 1024 * 1024) throw new Error(`Unsupported knowledge file: ${name}`);
    if (!/\.(md|json|mjs|yaml|yml|toml|txt)$/i.test(name) && !['.gitignore', '.gitattributes', '.gitkeep'].includes(path.basename(name))) throw new Error(`Unsupported file type: ${name}`);
    const text = fs.readFileSync(file, 'utf8');
    if (text.includes('\u0000')) throw new Error(`Binary file found: ${name}`);
    checkSecrets(text);
  }
  return [...new Set(names)];
}
export function sync(root, options = {}) {
  root = assertRoot(root);
  const release = acquireLock(root);
  try {
    const connection = readJson(inside(root, 'SYSTEM/connection.json'));
    if (!connection.url || !connection.private_verified_at) throw new Error('Private GitHub remote is not configured and verified');
    const normalizeRemote = url => url.replace(/^git@github\.com:/, 'https://github.com/').replace(/\.git$/, '');
    if (!options.testTransport && !/^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(normalizeRemote(connection.url))) throw new Error('Remote must be a GitHub HTTPS or SSH URL without embedded credentials');
    if (path.resolve(git(root, ['rev-parse', '--show-toplevel']).output) !== root) throw new Error('Vault must be its own Git repository');
    if (git(root, ['branch', '--show-current']).output !== connection.branch) throw new Error('Daily sync is allowed only on the main knowledge branch');
    if (normalizeRemote(git(root, ['remote', 'get-url', 'origin']).output) !== normalizeRemote(connection.url)) throw new Error('origin differs from the verified remote');
    if (git(root, ['ls-files', '--unmerged']).output) throw new Error('Resolve existing merge conflicts first');
    if (git(root, ['diff', '--cached', '--name-only']).output) throw new Error('Existing staged changes require review before automatic sync');
    // Verify the configured remote independently of any previous fetch ref.
    updateState(root, { sync_status: 'running', last_sync_attempt_at: now(), last_error: null });
    const names = validateTrackedFiles(root);
    if (names.length) git(root, ['add', '--', ...names]);
    if (git(root, ['diff', '--cached', '--name-only']).output) git(root, ['commit', '-m', `knowledge: save ${os.hostname()} ${now()}`]);
    for (let attempt = 0; attempt < 2; attempt++) {
      git(root, ['fetch', 'origin']);
      const remote = `refs/remotes/origin/${connection.branch}`;
      if (git(root, ['show-ref', '--verify', '--quiet', remote], [0, 1]).status === 0) {
        try { git(root, ['merge', '--no-edit', remote]); }
        catch (error) {
          const conflicts = git(root, ['diff', '--name-only', '--diff-filter=U']).output;
          const mergeHead = git(root, ['rev-parse', '-q', '--verify', 'MERGE_HEAD'], [0, 1]).status === 0;
          if (mergeHead) git(root, ['merge', '--abort']);
          throw new Error(conflicts ? `Merge conflict; local commits kept: ${conflicts.split('\n').join(', ')}` : error.message);
        }
      }
      // Validate incoming remote content too; fetched instructions are never executed by sync.
      validateTrackedFiles(root);
      const result = git(root, ['push', '--set-upstream', 'origin', `HEAD:refs/heads/${connection.branch}`], [0, 1, 128]);
      if (result.status === 0) {
        const at = now();
        updateState(root, { sync_status: 'ok', last_sync_at: at, last_error: null });
        return { synced: true, at, git: renderStatus(root).git };
      }
    }
    throw new Error('Push failed twice; local commits kept for the next sync');
  } catch (error) {
    updateState(root, { sync_status: 'pending', last_error: error.message, last_sync_attempt_at: now() });
    renderStatus(root);
    throw error;
  } finally { release(); }
}
function metricId(value) {
  return typeof value === 'string' && /^[a-zA-Z0-9:._-]{1,128}$/.test(value) && !SECRET_PATTERNS.some(p => p.test(value)) ? value : null;
}
function recordOperation(root, event, input, start, outcome, extra = {}) {
  // Metrics are best-effort; an unavailable journal cannot revoke a saved receipt.
  try { const file = inside(root, '.kb/operation-events.jsonl'); fs.mkdirSync(path.dirname(file), { recursive: true }); fs.appendFileSync(file, JSON.stringify({ schema_version: 2, at: now(), event, session_id: metricId(input?.session_id), turn_id: metricId(input?.turn_id), duration_ms: Number((performance.now() - start).toFixed(3)), outcome, ...extra }) + '\n'); } catch {}
}
function recordHookEvent(root, input, result, error, duration) {
  root = assertRoot(root); const file = inside(root, '.kb/hook-events.jsonl'); fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, JSON.stringify({ schema_version: 2, at: now(), event: ['Stop', 'UserPromptSubmit'].includes(input?.hook_event_name) ? input.hook_event_name : 'unknown', session_id: metricId(input?.session_id), turn_id: metricId(input?.turn_id), stop_hook_active: Boolean(input?.stop_hook_active), node_version: process.version, outcome: error ? 'error' : result?.decision === 'block' ? 'blocked' : 'ok', error: error ? error.code || 'hook_error' : null, ...(Number.isFinite(duration) ? { duration_ms: Number(duration.toFixed(3)) } : {}) }) + '\n');
}
export function hook(root, input) {
  root = assertRoot(root); const start = performance.now();
  try { const result = handleHook(root, input); recordHookEvent(root, input, result, null, performance.now() - start); return result; }
  catch (error) { try { recordHookEvent(root, input, null, error, performance.now() - start); error.hookEventRecorded = true; } catch {} throw error; }
}
function handleHook(root, input) {
  root = assertRoot(root);
  if (!input.session_id || !input.turn_id) throw new Error('Hook input is missing session_id or turn_id');
  const file = turnPath(root, input.session_id, input.turn_id);
  const script = path.join(root, 'SYSTEM/scripts/kb.mjs');
  const nodeCommand = process.platform === 'win32' ? `& '${process.execPath.replaceAll("'", "''")}'` : 'node';
  const args = `--session ${JSON.stringify(input.session_id)} --turn ${JSON.stringify(input.turn_id)}`;
  const instruction = `Personal knowledge base: ${root}. Before finishing this response, save new useful knowledge through kb-save or JSON on stdin to ${nodeCommand} "${script}" capture. Write knowledge content in Russian. source.kind=codex, source.session_id=${input.session_id}, source.turn_id=${input.turn_id}. If nothing is new: ${nodeCommand} "${script}" checkpoint ${args}. Data stays local until separately configured and authorized synchronization. Cloud exchange and curation require their own verified setup. A memory agent requires the installation owner's current authorization; kb-save owns handoff and verification. Other agents require current agreement with the user.`;
  if (input.hook_event_name === 'UserPromptSubmit') {
    if (!fs.existsSync(file)) atomic(file, { session_id: input.session_id, turn_id: input.turn_id, started_at: now() });
    return { hookSpecificOutput: { hookEventName: 'UserPromptSubmit', additionalContext: instruction } };
  }
  if (input.hook_event_name === 'Stop') {
    const mark = readJson(file);
    if (mark?.completed_at) return {};
    if (input.stop_hook_active) {
      updateState(root, { last_error: 'A turn finished without a memory checkpoint; inspect pending turns', status_refresh_pending: true });
      return { systemMessage: 'Memory persistence is unconfirmed; the turn was logged locally. Summary status refresh is separate.' };
    }
    return { decision: 'block', reason: instruction + ' This is a one-time persistence check; complete it without repeating the main answer.' };
  }
  return {};
}
function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) out[argv[i].slice(2)] = argv[++i]; else out._.push(argv[i]);
  }
  return out;
}
async function main() {
  const args = parseArgs(process.argv.slice(2));
  const root = args.root ? path.resolve(args.root) : DEFAULT_ROOT;
  const command = args._[0];
  let result;
  let hookInput;
  try {
  if (command === 'capture' || command === 'hook') {
    let data = '';
    for await (const chunk of process.stdin) { data += chunk; if (data.length > 1024 * 1024) throw new Error('Input too large'); }
    let input;
    try { input = JSON.parse(data.replace(/^\uFEFF/, '')); }
    catch { throw new Error('Invalid input JSON'); }
    if (command === 'hook') hookInput = input;
    result = command === 'capture' ? capture(root, input) : hook(root, input);
  } else if (command === 'checkpoint') result = checkpoint(root, { session_id: args.session, turn_id: args.turn });
  else if (command === 'search') result = search(root, args._.slice(1).join(' '), Number(args.limit || 8));
  else if (command === 'status') result = renderStatus(root);
  else if (command === 'sync') result = sync(root);
  else if (command === 'curation-record') {
    assertRoot(root);
    if (!args.pr || !/^https:\/\/github\.com\/[^/]+\/[^/]+\/pull\/\d+$/.test(args.pr)) throw new Error('A verified PR URL is required');
    updateState(root, { last_curation_at: now(), last_curation_pr: args.pr });
    result = renderStatus(root);
  } else throw new Error('Commands: capture, checkpoint, search, status, sync, hook, curation-record');
  process.stdout.write(JSON.stringify(result) + '\n');
  } catch (error) {
    if (command === 'hook') {
      if (!error.hookEventRecorded) { try { recordHookEvent(root, hookInput, null, error); } catch {} }
      process.stdout.write(JSON.stringify({ systemMessage: 'Personal memory hook error; inspect .kb/hook-events.jsonl.' }) + '\n');
    }
    throw error;
  }
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => {
    process.stderr.write(error.message + '\n');
    process.exitCode = 1;
  });
}
