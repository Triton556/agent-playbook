# Codex driver

Read only for a selected external Codex adapter route. Native workers use the host tools through [you-are-brain](../../you-are-brain/SKILL.md).


You are the orchestrator: you understand what the user wants, hand pieces of work to Codex sessions, and check what comes back. The user watches each session in the Codex app and may step in there.

For detached runs use `../../agent-sessions/adapters/codex.mjs` and its shared `<agent-sessions>/adapters/wait.mjs` under [contract v2](../../agent-sessions/references/contract.md#detached-runs-and-waiting). `<agent-sessions-codex>/scripts/codex-chat.mjs` is the legacy single-turn foreground variant: it has no detach/wait interface and preserves its original result shape. For foreground runs, run Codex through `<agent-sessions-codex>/scripts/codex-chat.mjs`. It starts `codex app-server` on the user's own Codex home, so the thread shows up in the app with the name you give it. Do not use `codex exec`: those threads are hidden from the app's list. Do not use a temporary `CODEX_HOME`, which keeps the thread out of the user's history entirely. Do not pass `--ignore-user-config`, which drops the user's instructions, skills and hooks. The only exception is an isolated experiment that the user asked to be isolated.

## Shared orchestration

Follow [agent-sessions](../../agent-sessions/references/session-guide.md): Fixed rules for execution and model selection, Worker artifacts for storage/publication, steps 1–2 for requirements/splitting, step 4 for briefs and step 5 for the current launch scope. Worker language: see [brief-writing, Language](brief-writing.md#language); defaults: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

Check the leading host under [host readiness](../../agent-sessions/references/contract.md#host-readiness) before delegation; a separate Codex backend does not change the leading host's native orchestration mode. The legacy driver supports the same optional assignment/host-evidence checks and terminal-run recovery as the adapters, preserving its original foreground result shape.

### 3. Choose effort and access

Effort selection and changes: see [agent-sessions, step 3](../../agent-sessions/references/session-guide.md#3-choose-effort-and-access). Driver aliases are minimal, low, medium, high, xhigh, ultra; ultra is the generic maximum.
Access selection: see agent-sessions, step 3; semantics/refusal: see [adapter contract, Access modes](../../agent-sessions/references/contract.md#access-modes).
Codex maps these to its OS sandbox; workspace-write is bounded by the configured working folder and on Windows also blocks writes inside .git.

### 6. Run and check

Follow [running and checking sessions](../../agent-sessions/references/running-and-checking.md), including its status updates to the user. The command for a session:

```bash
node <skill-dir>/scripts/codex-chat.mjs --cwd <work folder> --name "<recorded session name>" \
  --prompt <brief file> --sandbox <mode> --model <user's choice> --effort <your choice> \
  --assignment <private assignment.json> \
  --out <final.md> --log <events.jsonl>
```

- Continue a thread with `--thread <threadId>` from the JSON line printed last by the previous run, and a short follow-up brief. Pass `--sandbox`, `--model` and `--effort` again: they are not remembered between runs.
- Restore the selected route/session table first. For checked detached metadata, [recover a run](../../agent-sessions/references/contract.md#recover-a-run) after observing its terminal result; this is an explicit next turn, not an automatic retry or permission grant.
- Native unattended prompts and worker questions: see [running-and-checking, Questions and blocked workers](../../agent-sessions/references/running-and-checking.md#questions-and-blocked-workers).
- Exit code 0 means the turn completed. The last stdout line is `{threadId, turnId, status, out}`.

### 7. Report to the user

Report format: see [running-and-checking, Reporting](../../agent-sessions/references/running-and-checking.md#reporting).

## Known limits

- When the orchestrator itself runs inside a Codex sandbox, starting `codex app-server` fails with `spawn EPERM` (exit code 3) and no thread is created. Tell the user and ask them to approve the command or choose an access mode for you. Do not work around it.
- On Windows the workspace-write sandbox blocks writes inside `.git`, so Codex cannot commit. Git authorization: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).
- The sandbox may block launching a browser (EPERM). For visual checks, inspect the result yourself or ask the user to look.
- The user's hooks from Codex settings, including any memory hooks, also run in these sessions. If the final message is about a hook or memory error instead of the task, read the task's result from the files and `events.jsonl`.
- `--proxy` works only when an app-server daemon is running (`codex app-server daemon start`). The desktop app usually runs its own server and does not expose this socket; the default mode does not need it.
- If the CLI is not found, set `CODEX_BIN` to the codex executable.
