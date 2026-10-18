#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const folder = path.join(root, '.kb/scheduler');
const runtime = path.join(folder, 'runtime');
const taskName = 'Harness-Knowledge-Sync';
const description = 'Private knowledge vault: hourly Git sync without AI; local reviewed runtime.';
const psQuote = value => "'" + value.replaceAll("'", "''") + "'";
const psExe = path.join(process.env.SystemRoot || 'C:/Windows', 'System32/WindowsPowerShell/v1.0/powershell.exe');
function powershell(script) {
  const result = spawnSync(psExe, ['-NoProfile', '-NonInteractive', '-Command', '-'], { input: script, encoding: 'utf8', windowsHide: true, timeout: 30000 });
  if (result.error || result.status !== 0) throw new Error(result.stderr?.trim() || 'Task Scheduler operation failed');
  return result.stdout.trim();
}
try {
  const updateRuntime = process.argv.slice(2).length === 1 && process.argv[2] === '--update-reviewed-runtime';
  if (process.argv.length > 2 && !updateRuntime) throw new Error('Only --update-reviewed-runtime is supported');
  const existing = powershell(`$ErrorActionPreference='Stop'\n$t = Get-ScheduledTask -TaskName ${psQuote(taskName)} -ErrorAction SilentlyContinue\nif ($t) { @{TaskName=$t.TaskName;Actions=@($t.Actions | Select-Object Execute,Arguments,WorkingDirectory);Enabled=$t.Settings.Enabled;RunLevel=$t.Principal.RunLevel.ToString();LogonType=$t.Principal.LogonType.ToString();TaskUserSid=([Security.Principal.NTAccount]::new($t.Principal.UserId)).Translate([Security.Principal.SecurityIdentifier]).Value;CurrentUserSid=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value} | ConvertTo-Json -Depth 5 -Compress } else { Write-Output 'null' }\n`);
  const task = existing ? JSON.parse(existing) : null;
  if (task && !updateRuntime) throw new Error('Task already exists. Review it before changing or reinstalling; it was not overwritten.');
  if (updateRuntime && !task) throw new Error('Runtime update requires the existing owned task');
  const gitExe = powershell("$ErrorActionPreference='Stop'\n(Get-Command git -ErrorAction Stop).Source\n");
  const hash = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
  const manifestPath = path.join(folder, 'installation.json');
  let previous;
  if (updateRuntime) {
    previous = JSON.parse(fs.readFileSync(manifestPath, 'utf8').replace(/^\uFEFF/, ''));
    const action = task.Actions[0];
    const samePath = (a, b) => typeof a === 'string' && path.resolve(a).toLowerCase() === path.resolve(b).toLowerCase();
    const expectedCommand = `& ${psQuote(process.execPath)} ${psQuote(path.join(runtime, 'scheduled-sync.mjs'))} --manifest ${psQuote(manifestPath)}; exit $LASTEXITCODE`;
    const expectedArguments = `-NoProfile -NonInteractive -WindowStyle Hidden -Command "${expectedCommand}"`;
    if (task.TaskName !== taskName || task.Actions.length !== 1 || !samePath(action.Execute, psExe) || !samePath(action.WorkingDirectory, root) || action.Arguments !== expectedArguments || task.TaskUserSid !== task.CurrentUserSid || task.RunLevel !== 'Limited' || task.LogonType !== 'Interactive') throw new Error('Existing task ownership or access scope differs; runtime was not changed');
    if (task.Enabled) throw new Error('Disable the owned task before updating its reviewed runtime');
    if (previous.task_name !== taskName || !samePath(previous.vault, root) || !samePath(previous.node, process.execPath) || !samePath(previous.git, gitExe) || previous.interval_minutes !== 60) throw new Error('Installation scope differs; runtime was not changed');
  }
  fs.mkdirSync(runtime, { recursive: true });
  for (const name of ['kb.mjs', 'scheduled-sync.mjs']) fs.copyFileSync(path.join(root, 'SYSTEM/scripts', name), path.join(runtime, name));
  const manifest = { schema_version: 1, task_name: taskName, vault: root, node: process.execPath, git: gitExe, interval_minutes: 60, installed_at: new Date().toISOString(), core_sha256: hash(path.join(runtime, 'kb.mjs')), runner_sha256: hash(path.join(runtime, 'scheduled-sync.mjs')) };
  if (updateRuntime) { manifest.installed_at = previous.installed_at; manifest.reviewed_update_at = new Date().toISOString(); }
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
  if (updateRuntime) {
    console.log(JSON.stringify({TaskName: taskName, RuntimeUpdated: true, TaskDefinitionChanged: false, CoreSHA256: manifest.core_sha256, RunnerSHA256: manifest.runner_sha256}));
  } else {
  const command = `& ${psQuote(process.execPath)} ${psQuote(path.join(runtime, 'scheduled-sync.mjs'))} --manifest ${psQuote(manifestPath)}; exit $LASTEXITCODE`;
  const argumentsText = `-NoProfile -NonInteractive -WindowStyle Hidden -Command "${command}"`;
  const registration = `$ErrorActionPreference='Stop'
$kbIdentity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$kbAction = New-ScheduledTaskAction -Execute ${psQuote(psExe)} -Argument ${psQuote(argumentsText)} -WorkingDirectory ${psQuote(root)}
$kbLogon = New-ScheduledTaskTrigger -AtLogOn -User $kbIdentity
$kbHourly = New-ScheduledTaskTrigger -Once -At (Get-Date).AddHours(1) -RepetitionInterval (New-TimeSpan -Hours 1)
$kbPrincipal = New-ScheduledTaskPrincipal -UserId $kbIdentity -LogonType Interactive -RunLevel Limited
$kbSettings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName ${psQuote(taskName)} -Description ${psQuote(description)} -Action $kbAction -Trigger @($kbLogon,$kbHourly) -Principal $kbPrincipal -Settings $kbSettings | Out-Null
$kbTask = Get-ScheduledTask -TaskName ${psQuote(taskName)}
@{TaskName=$kbTask.TaskName; State=$kbTask.State.ToString(); Interval=$kbTask.Triggers[1].Repetition.Interval; AtLogon=$kbTask.Triggers[0].UserId; RunLevel=$kbTask.Principal.RunLevel.ToString()} | ConvertTo-Json -Compress
`;
  console.log(powershell(registration));
  }
} catch (error) { console.error(error.message); process.exitCode = 1; }
