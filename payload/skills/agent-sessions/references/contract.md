# Adapter contract

An adapter is one executable script, `adapters/<agent>.mjs`, that runs one turn of one worker session in a particular client and reports back in a fixed shape. The orchestrator only talks to adapters through this contract, so any client that satisfies it can be a worker.

Contract version **2** adds optional detached execution and shared waiting. All v1 foreground commands, result shapes and exit codes 0–4 remain unchanged.

## Describe

`node adapters/<agent>.mjs --describe` prints one JSON object and exits 0 without starting anything:

```json
{
  "agent": "codex",
  "contract": 2,
  "detach": true,
  "verified": true,
  "visible_in": "Codex app: the thread list, under the given name",
  "resume": true,
  "access_modes": {
    "read-only": "what this mode actually enforces in this client",
    "workspace-write": "...",
    "danger-full-access": "..."
  },
  "effort": ["low", "medium", "high"],
  "notes": "anything the orchestrator must tell the user before choosing"
}
```

- `detach: true` advertises support for the detached lifecycle below; v1 adapters without it remain foreground-only.
- `access_modes` lists only the modes the adapter supports. Each value says in plain words what the client enforces: an OS sandbox, a permission mode, a tool list. An adapter must not claim a protection that the client does not provide.
- `verified` is true only when the live checks from [writing an adapter](writing-an-adapter.md) passed. An unverified adapter may work, but the orchestrator must say so in its plan.
- `visible_in` says where the user can watch and step into the session, or `null` if they cannot.

Bundled adapters also advertise `launch_checks: ["assignment", "resume-run", "host-prompt-input"]` and `current_host_readiness: "unverified"`. These optional additions preserve contract-v2 result/exit shapes. Historical `verified` never certifies the leading host or a new model run.

## Host readiness

The leading client chooses the launch tool; the worker backend cannot reconfigure it. A skill cannot remove native tools or override higher-priority client instructions. Check the leading host separately before claiming the adapter route is ready. Confirmed competing orchestration is a conflict: do not substitute built-in subagents or silently claim compliance. Continue independent authorized work and explain the required integration change. Missing evidence is unverified, not conflict or success.

`node adapters/host-readiness.mjs --client codex --version <host version> --prompt-input <private preview.json>` reads an existing Codex `debug prompt-input` JSON array, without launching any process, model or network request. It emits only status (`compatible`, `conflict`, `unverified`), reason, version and an evidence hash; it never prints the prompt. Input is bounded to 2 MiB. A recognized active proactive-native mode in system/developer messages establishes a preview conflict; quoted user/brief text does not. Merely available native tools or an unrecognized mode stays unverified, not a confirmed conflict. A valid marker-free preview is classified compatible only for tested CLI 0.160.1; unsupported shapes/versions/clients remain unverified. Every report has `scope: supplied-prompt-preview` and `active_session: unverified`: a snapshot cannot certify the current desktop context or model behavior.

The optional launch flags `--host-client`, `--host-version` and `--host-prompt-input` run this check before any worker/supervisor starts. Conflict or unreadable/unsupported evidence refuses with exit 4; an otherwise unverified result is reported without claiming compatibility. Omitting the flags keeps legacy commands working without a readiness claim. Fresh host evidence is not inherited by `--resume-run`.

The source package's `docs/INTEGRATIONS.md` describes version-specific host setup. Current [official Codex configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents) documents `[agents] enabled = false`. Applying that option needs actual owner authorization and fresh leading-session verification; no automatic global configuration edit is authorized.

## Checked brief assignment

`--assignment <private file.json>` adds an explicit audience block to the prompt and checks this small metadata object before starting anything:

```json
{"recipient":"orchestrator","communication_language":"en","deliverables":[{"name":"UI","language":"ru"}],"memory_writer":"orchestrator","scope":"Only the approved fixture"}
```

All five fields are required. Recipient is `orchestrator` or `user`; memory writer is `orchestrator`, `worker` or `none`. Deliverables may be empty; each has a name and a language tag. A non-English communication language or a direct-to-user recipient needs `owner_override`, a reference to the current owner's explicit choice. Changing a recovered recipient/communication language also needs that reference. Metadata records a claimed choice; it cannot validate actual human consent or expand permissions.

The check rejects unknown/missing fields, invalid values and inconsistent exact `Recipient:`, `Communication language:` or `Memory writer:` declarations in unquoted, non-fenced brief text. It does not infer language from Cyrillic, translate quotations, or interpret arbitrary natural-language instructions. The orchestrator still reviews the whole brief, especially its Return/Result section, for contradictions such as asking for a Russian worker report while assigning English communication. User-facing deliverables and source quotations keep their assigned languages.

Without `--assignment`, older commands pass their prompt unchanged and make no brief-check claim. A short correction can reuse the assignment with explicit `--thread`, or inherit its frozen snapshot through `--resume-run`. Do not repeat the whole initial brief just to satisfy a template. Assignment files, their snapshots and owner references are private execution artifacts under the skill's Worker artifacts rule.

## Access modes

The modes are read-only for investigation, workspace-write (default) for the working folder, and danger-full-access for unrestricted execution. Describe actual enforcement per client: an OS sandbox, permission mode or tool list are different guarantees. Refuse unsupported enforcement or a missing working folder with exit 4 before starting, instead of silently changing modes or folders. Session access selection belongs to [agent-sessions, step 3](../SKILL.md#3-choose-effort-and-access).

## Run

```
node adapters/<agent>.mjs --cwd <dir> --prompt <brief file> [--name <title>] [--thread <id>]
     [--sandbox <mode>] [--model <id>] [--effort <level>] [--out <file>] [--log <file>]
```

| Option | Meaning |
|---|---|
| `--cwd` | Working folder of the worker. Required. |
| `--prompt` | File with the brief. If omitted, the brief is read from stdin. |
| `--name` | Display name for a new session. Ignored when continuing. |
| `--thread` | Continue this session with the brief as the next turn. Without it a new session starts. |
| `--sandbox` | `read-only`, `workspace-write` (default) or `danger-full-access`. Pass the mode on every turn, including continuations. |
| `--model`, `--effort` | API-optional only. Orchestration must select and pass both under [agent-sessions, Fixed rules and step 3](../SKILL.md#3-choose-effort-and-access); use client aliases from describe. |
| `--out` | Write the worker's final answer here. Without it the answer goes to stderr. |
| `--log` | Append the client's raw event stream here, for debugging and checking. |
| `--assignment` | Optional checked private audience/language/scope metadata; see Checked brief assignment. |
| `--host-client`, `--host-version`, `--host-prompt-input` | Optional evidence about the leading host; see Host readiness. |
| `--resume-run` | Optional terminal status file supplying the existing thread/settings/assignment; see Recover a run. |

## Recover a run

First observe pending runs using `wait --status` and inspect terminal reports under [running-and-checking](running-and-checking.md#before-starting). A next turn is a deliberate correction, not automatic retry or acceptance:

```text
node adapters/codex.mjs --resume-run <recorded statusFile> --prompt <short correction> --detach --run-dir <recorded directory>
```

For newly recorded runs, `--resume-run` reads the existing status, requires the same worker, terminal status, thread ID and launch metadata, and supplies `--thread` plus saved cwd/model/effort/sandbox and the assignment snapshot. It never modifies the old status or reuses the old out/log paths. Explicit new output/log arguments apply only to the new turn. A conflicting thread/folder refuses before launch. Settings supplied explicitly take precedence, but their authorization remains the orchestrator's responsibility. No new approval is inferred from a status record.

Running runs refuse: wait, inspect or obtain an authorized cancellation instead. Old records without launch metadata or a missing thread refuse without creating a replacement; use the recorded explicit `--thread`, reviewed settings and assignment after checking the old result. Independent reviewer continuation remains governed by independent-review. A legacy foreground result has no detached status; continue it with its explicit thread/settings.

## Detached runs and waiting

```text
node adapters/<agent>.mjs --cwd <worker dir> --prompt <brief> --model <id> --effort <level> --sandbox <mode> --detach [--run-dir <dir>]
node adapters/wait.mjs --runs <id,id,...> [--run-dir <dir>] [--mode any|all] [--timeout <seconds>]
node adapters/wait.mjs --status --runs <id,id,...> [--run-dir <dir>]
node adapters/wait.mjs --cancel <runId> [--run-dir <dir>]
```

`--detach` starts the same turn in a detached child supervisor, surviving the launching command, and returns immediately after the supervisor has written running status (not after worker completion). Its last stdout line is `{"agent":"codex","runId":"<id>","status":"started","statusFile":"<absolute path>"}`, exit 0. Startup does not guarantee the client starts successfully: inspect the eventual status/exitCode. Unsupported options still refuse before launch; unattended approval rules are unchanged.

The shared runtime `adapters/run-runtime.mjs` owns lifecycle/storage for both adapters. Run directory precedence is `--run-dir`, then `AGENT_RUNS_DIR`, then `.agent-runs/` under the parent of the worker's `--cwd`. Relative overrides resolve against the launching command's current directory. Resolve existing symlinks/junctions and refuse a directory equal to or inside worker cwd (exit 4, before creating it); choose an external override if cwd is a filesystem root. This keeps runtime metadata outside the worker workspace. `wait` has no worker cwd: pass the recorded run directory or the same environment override; absent either, its default is `.agent-runs/` under its own current directory's parent. Do not guess a directory when resuming from another folder.

Each run has `<runId>.json`, replaced atomically in the same directory:

```json
{"runId":"<id>","agent":"codex","pid":1234,"threadId":null,"status":"running","exitCode":null,"out":"<absolute path>","log":"<absolute path>","startedAt":"<ISO timestamp>","endedAt":null}
```

`pid` identifies the supervisor/process-tree root. `threadId` is updated once known. Status is `running`, `completed`, `failed` or `interrupted`; terminal records contain exitCode and endedAt. New bundled runs also record `launch: {settings, assignment, host_readiness}` and optional `continued_from` in the same status, and freeze a supplied assignment in `<runId>.assignment.json`. These are execution context, not acceptance or permission records. Out/log honor explicit paths (resolved at launch); otherwise they are `<runId>.out.md` and `<runId>.events.jsonl` in the run directory. The brief, supervisor configuration and stderr diagnostic file are stored alongside them for recovery; keep this private local execution material uncommitted under Worker artifacts. A terminal record is a transport result, not acceptance of the worker's claims.

`wait` watches the run directory for atomic replacements and checks at a slow 2-second fallback interval on filesystems with unreliable/unsupported watches. It blocks without busy CPU until any requested run is terminal (`--mode any`) or all are terminal (`--mode all`, default). Completion includes failed/interrupted runs so the brain can inspect them. It prints one JSON line:

```json
{"done":[{"runId":"<id>","status":"completed","threadId":"<thread>","exitCode":0,"out":"<absolute path>"}],"running":["<other id>"],"timedOut":false}
```

Default timeout is **540 seconds** to fit typical tool-call limits. Clients with lower limits must pass a smaller `--timeout` below that limit and call again on the still-pending IDs. Timeout returns the current snapshot with timedOut true and exit 5; it neither fails nor cancels workers. Condition satisfied returns exit 0 even when a worker failed. Unknown run IDs, invalid options or unreadable/malformed status return exit 2. Wait/status only observe records and never infer failure from a PID probe. If external cleanup kills a supervisor before it writes terminal status, the wait can time out with a stale running record; explicit cancel records interruption.

`--status` returns the same JSON immediately (timedOut false), without blocking. `--cancel` stops the detached process tree (Windows taskkill /T /F; POSIX process-group SIGKILL), then atomically writes interrupted with exitCode 1, and returns the same snapshot, exit 0. Already-terminal cancellation is a no-op, preserving its result. Cancellation errors return 2. Forced OS/client cleanup is outside the survival guarantee; do not delete run metadata while processes are live.

Orchestrator scheduling, bounded waits and turn handoff have one owner: [running-and-checking, Waiting for workers](running-and-checking.md#waiting-for-workers).

## Result

The last line on stdout is one JSON object:

```json
{"agent": "codex", "threadId": "...", "status": "completed", "out": "final.md"}
```

`threadId` is the value to pass as `--thread` next time. `status` is `completed` when the turn finished normally; anything else is a failure description.

Progress (commands run, tools called) goes to stderr as short lines, for example `[cmd] npm test`.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | The turn completed. |
| 1 | The worker ran but the turn did not complete (error, interrupted, limit reached). |
| 2 | Driver or protocol error after the client started. |
| 3 | The client could not be started (not installed, or blocked by the orchestrator's own sandbox). No session was created. |
| 5 | Shared wait timed out; workers keep running. |
| 4 | An option is not supported, for example an access mode this client cannot enforce. Nothing was started. |

Access refusal: see Access modes above.

## Unattended runs

Adapters run without a person at the worker. Approval requests and questions from the worker are declined, never auto-approved. Authorized asynchronous board questions and blocked-return behavior: see [running-and-checking, Questions and blocked workers](running-and-checking.md#questions-and-blocked-workers).
