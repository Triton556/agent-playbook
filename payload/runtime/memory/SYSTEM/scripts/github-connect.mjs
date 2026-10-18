#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { DEFAULT_ROOT } from './kb.mjs';

// A credential stays inside this process. It is never printed or written to the vault.
const owner = process.argv[2];
const repoName = process.argv[3] || 'personal-knowledge';
if (!owner || !/^[A-Za-z0-9-]+$/.test(owner) || !/^[A-Za-z0-9_.-]+$/.test(repoName)) {
  console.error('Usage: node SYSTEM/scripts/github-connect.mjs <confirmed-owner> [repo-name]');
  process.exit(1);
}
const environment = { ...process.env, GIT_TERMINAL_PROMPT: '0', GCM_INTERACTIVE: 'never' };
function runGit(args, allowed = [0], input) {
  const result = spawnSync('git', ['-C', DEFAULT_ROOT, ...args], { input, encoding: 'utf8', env: environment, windowsHide: true, timeout: 25000 });
  if (result.error || !allowed.includes(result.status)) throw new Error(`Git ${args[0]} is unavailable or needs authentication`);
  return { status: result.status, output: result.stdout.trim() };
}
async function main() {
  const credentialOutput = runGit(['credential', 'fill'], [0], `protocol=https\nhost=github.com\nusername=${owner}\n\n`).output;
  const fields = Object.fromEntries(credentialOutput.split(/\r?\n/).map(line => {
    const position = line.indexOf('=');
    return position >= 0 ? [line.slice(0, position), line.slice(position + 1)] : [];
  }).filter(v => v.length === 2));
  if (!fields.password) throw new Error('No saved GitHub credential; finish the GitHub login first');
  const request = async (endpoint, method = 'GET', body) => {
    const response = await fetch(`https://api.github.com${endpoint}`, {
      method,
      redirect: 'error',
      signal: AbortSignal.timeout(25000),
      headers: { Accept: 'application/vnd.github+json', Authorization: `Bearer ${fields.password}`, 'X-GitHub-Api-Version': '2026-03-10', 'User-Agent': 'пользователь-personal-knowledge-setup', ...(body ? { 'Content-Type': 'application/json' } : {}) },
      ...(body ? { body: JSON.stringify(body) } : {})
    });
    if (response.status === 404 && method === 'GET') return null;
    if (!response.ok) throw new Error(`GitHub ${method} failed with HTTP ${response.status}; verify access, without copying credentials into chat`);
    return response.json();
  };
  const user = await request('/user');
  if (user.login.toLowerCase() !== owner.toLowerCase()) throw new Error('Authenticated account differs from the confirmed owner; ask the user before creating a repository');
  const endpoint = `/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repoName)}`;
  let repository = await request(endpoint);
  let created = false;
  if (!repository) {
    repository = await request('/user/repos', 'POST', { name: repoName, private: true, auto_init: false, description: 'Private Markdown knowledge base for coding agents', has_wiki: false, has_projects: false });
    created = true;
  }
  const connectionPath = path.join(DEFAULT_ROOT, 'SYSTEM/connection.json');
  const connection = JSON.parse(fs.readFileSync(connectionPath, 'utf8'));
  const alreadyConnected = connection.url === repository.clone_url;
  if (!repository.private || repository.owner.login.toLowerCase() !== owner.toLowerCase()) throw new Error('Repository is not private or has a different owner; no files were uploaded');
  if (!created && !alreadyConnected && repository.size > 0) throw new Error('Existing repository has content; review it before connecting the local vault');
  const verified = await request(endpoint);
  if (!verified?.private || verified.full_name !== repository.full_name) throw new Error('Could not independently verify repository privacy');
  const origin = runGit(['remote', 'get-url', 'origin'], [0, 2, 128]);
  if (origin.status === 0 && origin.output !== repository.clone_url) throw new Error('An existing origin requires review; it was not replaced');
  if (origin.status !== 0) runGit(['remote', 'add', 'origin', repository.clone_url]);
  const at = new Date().toISOString();
  const updated = { ...connection, provider: 'github', url: repository.clone_url, branch: 'main', private_verified_at: at };
  const temp = connectionPath + '.tmp';
  fs.writeFileSync(temp, JSON.stringify(updated, null, 2) + '\n');
  fs.renameSync(temp, connectionPath);
  const readmePath = path.join(DEFAULT_ROOT, 'README.md');
  const readme = fs.readFileSync(readmePath, 'utf8').replace(/^Подтверждённый remote для восстановления:.*$/m, `Подтверждённый remote для восстановления: **${repository.clone_url}**. Приватность проверена через GitHub API ${at}. Авторизация требуется отдельно в каждой среде; секретов в README нет.`);
  fs.writeFileSync(readmePath, readme);
  console.log(JSON.stringify({ owner: user.login, repository: repository.full_name, url: repository.html_url, private: verified.private, created, verified_at: at, connected: true }));
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
