#!/usr/bin/env node
// Read-only, dependency-free link/provenance audit. Does not repair or move files.
// Checks file targets, not heading/block anchors. Historical raw-link findings
// are warnings by default; duplicate raw identities are integrity errors.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const ignored = new Set(['.git', '.kb', '.obsidian', '.agents', 'node_modules']);
const rawPath = file => /^(INBOX|ARCHIVE)\//.test(file);
const normalizeName = name => process.platform === 'win32' ? name.toLocaleLowerCase() : name;
const blank = text => text.replace(/[^\r\n]/g, ' ');

function metadata(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) return {data: {}, length: 0};
  const source = match[1].trim();
  if (source.startsWith('{')) {
    try {return {data: JSON.parse(source), length: match[0].length};}
    catch {return {data: {}, length: match[0].length, invalid: true};}
  }
  // Only the scalar/list provenance fields are needed; this is not a YAML parser.
  const data = {};
  let listKey;
  const scalar = value => value.trim().replace(/^(['"])([\s\S]*)\1$/, '$2');
  for (const line of source.split(/\r?\n/)) {
    const field = line.match(/^(id|fingerprint|source_id|source_ids|sources):\s*(.*?)\s*$/);
    if (field) {
      const [, key, value] = field;
      listKey = value ? null : key;
      data[key] = !value ? [] : value.startsWith('[') && value.endsWith(']')
        ? value.slice(1, -1).split(',').map(scalar).filter(Boolean) : scalar(value);
    } else if (listKey && /^\s+-\s+/.test(line)) data[listKey].push(scalar(line.replace(/^\s+-\s+/, '')));
    else if (/^\S/.test(line)) listKey = null;
  }
  return {data, length: match[0].length};
}

function withoutCode(text, frontLength) {
  let masked = blank(text.slice(0, frontLength)) + text.slice(frontLength);
  let fence;
  masked = masked.split(/(?<=\n)/).map(line => {
    const marker = line.match(/^ {0,3}(`{3,}|~{3,})/);
    if (fence) {
      if (marker && marker[1][0] === fence.char && marker[1].length >= fence.length && /^\s*$/.test(line.slice(marker[0].length))) fence = null;
      return blank(line);
    }
    if (marker) {fence = {char: marker[1][0], length: marker[1].length}; return blank(line);}
    // Preserve indented list items, but omit indented code examples.
    if (/^(?: {4}|\t)/.test(line) && !/^\s*(?:[-+*]|\d+[.)])\s/.test(line)) return blank(line);
    return line;
  }).join('');
  return masked.replace(/<!--[^]*?-->/g, blank).replace(/(`+)([^]*?)\1/g, blank);
}

function destination(value) {
  value = value.trim();
  if (value.startsWith('<')) return value.slice(1, value.indexOf('>') < 0 ? undefined : value.indexOf('>'));
  return value.replace(/\s+(?:"[^"]*"|'[^']*'|\([^)]*\))\s*$/, '').trim();
}

function liveLinks(masked) {
  const links = [];
  const definitions = new Map();
  let scan = masked.replace(/^ {0,3}\[([^\]\n]+)\]:\s*(.+)$/gm, (whole, label, value) => {
    definitions.set(label.trim().toLocaleLowerCase(), destination(value));
    return blank(whole);
  });
  scan = scan.replace(/!?\[\[([^\]\n]+)\]\]/g, (whole, target, index) => {
    links.push({target: target.split('|')[0], index, wiki: true});
    return blank(whole);
  });
  // Balanced destinations support angle-quoted spaces and parentheses in filenames.
  for (const match of scan.matchAll(/!?\[[^\]\n]*\]\(/g)) {
    const start = match.index + match[0].length;
    let depth = 1, angle = false, escaped = false, end = start;
    for (; end < scan.length; end++) {
      const char = scan[end];
      if (char === '\n' || char === '\r') break;
      if (escaped) {escaped = false; continue;}
      if (char === '\\') {escaped = true; continue;}
      if (char === '<') angle = true;
      if (char === '>') angle = false;
      if (!angle && char === '(') depth++;
      if (!angle && char === ')' && --depth === 0) break;
    }
    if (depth === 0) links.push({target: destination(scan.slice(start, end)), index: match.index, wiki: false});
  }
  scan = scan.replace(/(?<!!)\[([^\]\n]+)\]\[([^\]\n]*)\]/g, (whole, label, reference, index) => {
    const key = (reference || label).trim().toLocaleLowerCase();
    if (definitions.has(key)) links.push({target: definitions.get(key), index, wiki: false});
    else links.push({target: key, index, unresolvedReference: true});
    return blank(whole);
  });
  for (const match of scan.matchAll(/(?<!!)\[([^\]\n]+)\](?![\[(])/g)) {
    const key = match[1].trim().toLocaleLowerCase();
    if (definitions.has(key)) links.push({target: definitions.get(key), index: match.index, wiki: false});
  }
  return links;
}

export function lintVault(root, {strictRaw = false, navigationOnly = false} = {}) {
  root = path.resolve(root);
  if (strictRaw && navigationOnly) throw new Error('Choose --strict-raw or --navigation-only, not both');
  const findings = [], files = new Map(), notes = [];
  let localLinksChecked = 0, sourceReferencesChecked = 0;
  function finding(file, code, target, index = 0, integrity = false) {
    const raw = rawPath(file);
    const scope = integrity ? 'integrity' : raw ? 'raw' : 'navigation';
    const severity = integrity || !raw || strictRaw ? 'error' : 'warning';
    const content = files.get(file)?.text || '';
    findings.push({severity, scope, code, file, line: 1 + (content.slice(0, index).match(/\n/g) || []).length, target});
  }
  function within(file) {
    const relative = path.relative(root, file);
    return relative !== '..' && !relative.startsWith('..' + path.sep) && !path.isAbsolute(relative);
  }
  function safeFile(file, directoryLink = false) {
    if (!within(file)) return {unsafe: 'outside-vault'};
    let current = root;
    for (const segment of path.relative(root, file).split(path.sep).filter(Boolean)) {
      current = path.join(current, segment);
      try {if (fs.lstatSync(current).isSymbolicLink()) return {unsafe: 'symlink-target'};}
      catch (error) {if (error.code === 'ENOENT' || error.code === 'ENOTDIR') return {}; throw error;}
    }
    try {const stats = fs.lstatSync(file); return {exists: stats.isFile() || (directoryLink && stats.isDirectory())};}
    catch (error) {if (error.code === 'ENOENT' || error.code === 'ENOTDIR') return {}; throw error;}
  }
  function walk(folder) {
    for (const entry of fs.readdirSync(folder, {withFileTypes: true})) {
      if (ignored.has(entry.name)) continue;
      const file = path.join(folder, entry.name), relative = path.relative(root, file).replaceAll('\\', '/');
      const stats = fs.lstatSync(file);
      if (stats.isSymbolicLink()) {finding(relative, 'symlink-entry', relative, 0, true); continue;}
      if (stats.isDirectory()) {walk(file); continue;}
      if (!stats.isFile()) continue;
      files.set(relative, {});
      if (!/\.md$/i.test(entry.name)) continue;
      if (stats.size > 2 * 1024 * 1024) {finding(relative, 'markdown-too-large', relative); continue;}
      const text = fs.readFileSync(file, 'utf8'), front = metadata(text);
      files.set(relative, {text, front});
      notes.push(relative);
      if (front.invalid) finding(relative, 'invalid-json-frontmatter', relative);
    }
  }
  const rootStats = fs.lstatSync(root);
  let rootHasSymlink = rootStats.isSymbolicLink();
  for (let parent = path.dirname(root); !rootHasSymlink;) {
    rootHasSymlink = fs.lstatSync(parent).isSymbolicLink();
    const next = path.dirname(parent);
    if (next === parent) break;
    parent = next;
  }
  if (rootHasSymlink || !rootStats.isDirectory()) finding('.', 'unsafe-vault-root', '.', 0, true);
  else walk(root);

  const identities = new Map(), fingerprints = new Map();
  for (const file of notes.filter(rawPath)) {
    const meta = files.get(file).front.data;
    for (const [key, map, code] of [['id', identities, 'duplicate-raw-id'], ['fingerprint', fingerprints, 'duplicate-raw-fingerprint']]) {
      const value = meta[key];
      if (typeof value !== 'string' || !value) continue;
      if (map.has(value)) finding(file, code, map.get(value), 0, true);
      else map.set(value, file);
    }
  }

  function resolve(file, rawTarget, wiki, index = 0) {
    let target = rawTarget.trim();
    if (!target || target.startsWith('#')) return;
    if (/^[A-Za-z]:[\\/]|^\\\\/.test(target)) {finding(file, 'absolute-local-target', target, index); return;}
    if (/^[A-Za-z][A-Za-z0-9+.-]*:/.test(target) || target.startsWith('//')) return;
    target = target.split('#')[0].split('?')[0];
    try {target = decodeURIComponent(target);} catch {finding(file, 'invalid-url-encoding', rawTarget, index); return;}
    target = target.replace(/\\([()\[\]<> ])/g, '$1').replaceAll('\\', '/');
    if (!target || target.includes('\0') || path.isAbsolute(target) || path.win32.isAbsolute(target)) {finding(file, 'unsafe-link-target', rawTarget, index); return;}
    localLinksChecked++;
    const extension = path.posix.extname(target);
    const names = extension ? [target] : [target, target + '.md'];
    if (wiki && !/^\.\.?\//.test(target)) {
      const matches = [...files.keys()].filter(candidate => names.some(name => normalizeName(candidate) === normalizeName(name) || (target.includes('/') ? normalizeName(candidate).endsWith('/' + normalizeName(name)) : normalizeName(path.posix.basename(candidate)) === normalizeName(name))));
      if (matches.length > 1) {finding(file, 'ambiguous-target', matches.join(', '), index); return;}
      if (matches.length === 1) return;
    }
    const base = wiki && !/^\.\.?\//.test(target) ? root : path.dirname(path.join(root, file));
    for (const name of names) {
      const candidate = path.resolve(base, name);
      const result = safeFile(candidate, !wiki && target.endsWith('/'));
      if (result.unsafe) {finding(file, result.unsafe, rawTarget, index); return;}
      if (result.exists) return;
    }
    finding(file, 'missing-target', rawTarget, index);
  }

  for (const file of notes) {
    const {text, front} = files.get(file);
    for (const link of liveLinks(withoutCode(text, front.length))) {
      if (link.unresolvedReference) finding(file, 'missing-reference-definition', link.target, link.index);
      else resolve(file, link.target, link.wiki, link.index);
    }
    for (const key of ['source_id', 'source_ids', 'sources']) {
      const values = front.data[key] === undefined ? [] : Array.isArray(front.data[key]) ? front.data[key] : [front.data[key]];
      for (let reference of values) {
        reference = typeof reference === 'object' && reference ? reference.id || reference.path : reference;
        if (typeof reference !== 'string' || !reference.trim()) continue;
        sourceReferencesChecked++;
        if (identities.has(reference)) continue;
        if (/[/\\.]|^[A-Za-z][A-Za-z0-9+.-]*:/.test(reference)) resolve(file, reference, false);
        else finding(file, 'missing-source-id', reference);
      }
    }
  }
  const visible = navigationOnly ? findings.filter(item => item.scope !== 'raw') : findings;
  return {root, scannedMarkdown: notes.length, localLinksChecked, sourceReferencesChecked,
    errors: visible.filter(item => item.severity === 'error').length,
    warnings: visible.filter(item => item.severity === 'warning').length,
    navigationErrors: findings.filter(item => item.scope === 'navigation' && item.severity === 'error').length,
    integrityErrors: findings.filter(item => item.scope === 'integrity').length,
    legacyWarnings: findings.filter(item => item.scope === 'raw' && item.severity === 'warning').length,
    findings: visible};
}

function main() {
  const args = process.argv.slice(2);
  const options = {};
  let root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..'), json = false;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--root' && args[i + 1] && !args[i + 1].startsWith('--')) root = args[++i];
    else if (args[i] === '--strict-raw') options.strictRaw = true;
    else if (args[i] === '--navigation-only') options.navigationOnly = true;
    else if (args[i] === '--json') json = true;
    else if (args[i] === '--help') {console.log('kb-lint [--root VAULT] [--json] [--navigation-only | --strict-raw]\nRead-only file-target/source audit; headings are not validated. Raw links warn by default; raw identity duplicates error.'); return;}
    else throw new Error('Unknown or incomplete argument: ' + args[i]);
  }
  const result = lintVault(root, options);
  if (json) console.log(JSON.stringify(result));
  else {
    console.log(`${result.scannedMarkdown} Markdown; ${result.localLinksChecked} local links; ${result.errors} errors; ${result.warnings} warnings (${result.legacyWarnings} legacy warnings).`);
    for (const item of result.findings) console.log(`${item.severity.toUpperCase()} ${item.file}:${item.line} ${item.code}: ${item.target}`);
  }
  process.exitCode = result.errors ? 1 : 0;
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {main();} catch (error) {console.error(error.message); process.exitCode = 2;}
}
