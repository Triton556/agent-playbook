# Adapter contract

An adapter is one executable script, `adapters/<agent>.mjs`, that runs one turn of one worker session in a particular client and reports back in a fixed shape. The orchestrator only talks to adapters through this contract, so any client that satisfies it can be a worker.

## Describe

`node adapters/<agent>.mjs --describe` prints one JSON object and exits 0 without starting anything:

```json
{
  "agent": "codex",
  "contract": 1,
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

- `access_modes` lists only the modes the adapter supports. Each value says in plain words what the client enforces: an OS sandbox, a permission mode, a tool list. An adapter must not claim a protection that the client does not provide.
- `verified` is true only when the live checks from [writing an adapter](writing-an-adapter.md) passed. An unverified adapter may work, but the orchestrator must say so in its plan.
- `visible_in` says where the user can watch and step into the session, or `null` if they cannot.

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
| `--model`, `--effort` | Optional. Effort uses the client's own level names; see `effort` in describe. |
| `--out` | Write the worker's final answer here. Without it the answer goes to stderr. |
| `--log` | Append the client's raw event stream here, for debugging and checking. |

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
| 4 | An option is not supported, for example an access mode this client cannot enforce. Nothing was started. |

Refuse with 4 rather than silently running in a weaker or stronger mode than the user chose.

## Unattended runs

Adapters run without a person at the worker. Approval requests and questions from the worker are declined, never auto-approved. Anything the task needs must be allowed by the chosen access mode before the run.
