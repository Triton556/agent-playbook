# Session guide

Open when the selected execution route is an external CLI adapter. Native workers use the host's native tools; this guide does not forbid them or launch either route automatically. The public entrypoint is [you-are-brain](../../you-are-brain/SKILL.md).

## Fixed rules

Use the selected adapter and the task's model routing. The user chooses models directly or delegates selection through Rules/Auto; Ask mode requires the missing choice. Do not silently switch the mechanism on recovery. Language and checked assignment: [brief-writing](brief-writing.md).

## Worker artifacts

Briefs, reports and run metadata stay in local scratch/ignored storage unless the user requests publication for that project.

## Workflow

### 1. Find out the requirements

Use the current task's outputs and acceptance scenarios. Read [requirements-interview](requirements-interview.md) only when a missing worker-specific choice blocks assignment; do not start another general interview.

### 2. Split the work

Assign independent outputs and a non-overlapping writable folder/worktree per simultaneous writer. Record dependencies and the brain's own work. One task does not require multiple workers by default.

For the selected adapter, run `node <agent-sessions>/adapters/<name>.mjs --describe`; verify the named CLI is present. Its historical `verified` field does not certify this host or its access. On an unsupported option, startup error or confirmed host conflict, report that blocker; do not change permissions or routes to conceal it. [Contract](contract.md#host-readiness) contains adapter-specific checks. Creating an adapter or running a live model probe requires authorization for that work.

### 3. Choose effort and access

Select model and effort deliberately for every turn; adapter API defaults do not make this decision. Effort precedence:
1. The user's explicit request for a level always wins.
2. After failure, raise one supported level only when task difficulty caused the failure. If the brief caused it, repair the brief and keep the effort.
3. Otherwise use the lowest fitting level in this table and the maximum restriction below.

| Level | Use for | Examples |
|---|---|---|
| `minimal` (Codex) | trivial lookups only; never changes | locate an already known identifier |
| `low` | one small, clear change | fix a typo or a config value, rename one thing, run the tests and report |
| `medium` | mechanical work across many files against a clear spec | renames or migrations by a mapping, moving files, writing tests to a given spec, applying an existing pattern elsewhere, updating docs across files |
| `high` | ordinary engineering that needs judgment | a feature across layers, a bug with an unknown cause, code review, building a UI from an accepted design, a performance investigation |
| `xhigh` | costly mistakes or many interacting parts | designing a subsystem, a large refactor, security-sensitive changes, concurrency, data migration with a risk of loss |
| maximum (`ultra` in Codex, `max` in Claude Code) | only the three cases below | |

Subject to precedence above, the maximum is allowed only when:

1. the task is open creative or design exploration with no single right answer;
2. a lower level already failed on this same task because of its difficulty; or
3. the user asked for it.

Otherwise mechanical work, documentation edits, running tests and small reviews do not justify maximum effort. More than one maximum-effort session in one plan needs its own justification.

Effort names differ between clients; use the levels from the adapter's description.

Use the task/profile access selection; ask when the next launch requires an uncovered access mode. Mode meanings, default and refusal: see [adapter contract, Access modes](contract.md#access-modes). Codex maps the modes to its OS sandbox; workspace-write is bounded by the working folder and on Windows also blocks writes inside .git.

### 4. Write the briefs

Use [brief-writing](brief-writing.md) for the initial brief and its explicit recipient, outputs, scope and acceptance scenario. Bundled adapters can check the [assignment](contract.md#checked-brief-assignment). A continuation inherits that assignment and receives the concrete correction, not another initial interview.

### 5. Check the authorized scope and launch

The launch boundary is the current user-authorized task/project plus its selected route, model routing, access and cost scope. Record worker, output, model, effort, access, folder, dependency and brief in the task table. Launch covered assignments without asking for a new yes for each worker.

Ask before an uncovered provider/model selection, access/cost expansion, new scope, or a separate independent reviewer that was not selected. A user answer may cover a batch of assignments; record what it covers. A profile and a prior report are not new permission. Native tool approval prompts remain controlled by the host.

### 6. Run and check

Use [running-and-checking](running-and-checking.md) for launch/status/wait/report events. Run command and output semantics: [contract](contract.md#run). Codex runs through `<agent-sessions>/adapters/codex.mjs`: it starts `codex app-server` on the user's own Codex home, so the thread appears in the Codex app under its name. Do not use `codex exec` (hidden threads), a temporary `CODEX_HOME` or `--ignore-user-config` unless the user asked for an isolated experiment. Pass model, effort and access again on every continuation. After worker completion, inspect the delivered output against the task's user steps/contract; process exit alone does not accept it.

### 7. Report to the user

Report material state changes: launched, blocked, returned, accepted or returned for a specific correction. At completion list results, actual checks and remaining limits; [running-and-checking](running-and-checking.md#reporting) defines adapter metadata.

## Known limits

An adapter startup denial does not authorize a workaround. Report the exact failed operation and continue independent covered work. Model availability, login and actual access must be checked on the selected client.

Codex-specific limits:
- Started from inside a Codex sandbox, `codex app-server` fails with `spawn EPERM` (exit code 3) and no thread is created. Tell the user and ask for approval or another access mode; do not work around it.
- The sandbox may block launching a browser; inspect visual results yourself or ask the user to look.
- The user's Codex hooks, including memory hooks, run in these sessions too. If the final message is about a hook error instead of the task, read the result from the output files and the event log.
- `--proxy` works only with a running `codex app-server daemon`; the default mode does not need it.
- If the CLI is not found, set `CODEX_BIN` to the codex executable.
