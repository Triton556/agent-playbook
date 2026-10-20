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

`pid` identifies the supervisor/process-tree root. `threadId` is updated once known. Status is `running`, `completed`, `failed` or `interrupted`; terminal records contain exitCode and endedAt. Out/log honor explicit paths (resolved at launch); otherwise they are `<runId>.out.md` and `<runId>.events.jsonl` in the run directory. The brief, supervisor configuration and stderr diagnostic file are stored alongside them for recovery; keep this private local execution material uncommitted under Worker artifacts. A terminal record is a transport result, not acceptance of the worker's claims.

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
