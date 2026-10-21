# Running and checking sessions

Launch gate: see [agent-sessions, step 5](../../agent-sessions/SKILL.md#5-get-approval-with-a-summary). Generic command: see [adapter contract, Run](../../agent-sessions/references/contract.md#run); the Codex-specific driver command is in [agent-sessions-codex, step 6](../../agent-sessions-codex/SKILL.md#6-run-and-check).

## Before starting

1. **One place per writer.** Assign one task per session. Each session that changes files gets its own folder or git worktree. Two sessions never share files. Read-only sessions may share a folder.
2. **A known starting point.** Make sure each working folder has a clean state you can compare against: `git status` is clean, or you note the current commit. Without it you cannot tell later what the session changed.
3. **Artifact storage.** See [agent-sessions, Worker artifacts](../../agent-sessions/SKILL.md#worker-artifacts). Store logs alongside that authorized local execution material.
4. **A session log.** Keep one table for the whole task and update it whenever a session changes stage:

   ```
   | # | Session | Worker | Stage | Since | Next | threadId | runId | statusFile | Brief |
   |---|---------|--------|-------|-------|------|----------|-------|------------|-------|
   | 1 | <name>  | <client, model, effort> | <stage> | <time> | <what happens next> | <thread id> | <run id> | <status path> | <brief file> |
   ```

   Stages, in order: `waiting for #N` (depends on another session), `running`, `checking` (you are verifying the result), `fix requested` (a follow-up turn is running), `accepted`, `failed` (cannot continue; say why). For foreground runs, threadId comes from the final JSON line. For detached runs, record runId and statusFile immediately, then threadId from the status file or wait result once known; threadId continues the session, while runId identifies just this turn.

The log owns execution metadata only; requirements/acceptance follow [task-state, Long-task state and completeness](../../dev-flow/references/task-state.md). When Jam Board owns task state, keep session metadata in its labeled operational notes and link task IDs; board task status/verdict stays authoritative. Else keep the log in the existing plan. Do not copy requirements or acceptance into it.

## Starting

- Start independent sessions together. A session that waits for another starts only after you have checked and accepted the one it depends on.
- Start each session with exactly the name shown in the approval table, in the user's language, so the user finds it in the session list. Tell the user the names and where to watch them.
- If a run exits with 3 (client could not start) or 4 (unsupported option), nothing was created. Tell the user; do not retry with different settings on your own.

## Waiting for workers

Use [contract, Detached runs and waiting](contract.md#detached-runs-and-waiting) for commands, paths and result shapes. This is the single owner of orchestration waiting rules; a board is optional.

- **The orchestrator has background notifications.** Claude Code background Bash tasks notify the orchestrator when they finish. Either put the foreground adapter command in such a background task and use its notification, or use `--detach` plus `wait`. Never sleep-poll. Codex app automations or other notification mechanisms are unverified here; use this case only when the current client actually provides completion notifications.
- **The orchestrator has no notifications.** In Codex and most CLIs, start each independent worker with `--detach`, record runId/statusFile in the session log, and do independent work. Then call `node adapters/wait.mjs --runs <pending ids> --run-dir <recorded directory> --mode any --timeout 60`, with a timeout below the current tool-call limit. After each return, check each finished worker using Checking a finished session below, recover threadId, and remove its runId from the pending set before waiting again. Use `--mode all` only when nothing else can proceed. Repeat bounded blocking waits until done or the user's time budget is reached. At that limit report exactly what is still running, runIds, known threadIds and how to resume.
- **The turn must end before workers finish.** For client limits or a user-requested stop of orchestration, leave detached workers running unless the user also asked to cancel them. Report their runIds, known threadIds, status files and run directory. On the next turn begin with `node adapters/wait.mjs --status --runs <ids> --run-dir <recorded directory>` and check completed results before continuing. Explicit cancellation uses the contract's `--cancel` command.

Client evidence: the Codex adapter waits for the turn before its foreground command exits; its notes describe the separate app-server, not an orchestrator wakeup facility. The installed Codex execution tool can yield a process session ID that requires an explicit read; this does not notify the brain of completion. Use blocking `wait` as the completion tool, and resume that same tool process if the host yields it. Notification behavior in other Codex versions/clients is unverified. Claude Code background command behavior is documented in [Interactive mode](https://code.claude.com/docs/en/interactive-mode#background-bash-commands); live Claude orchestration was not exercised here. Detach survives the launching command; forced client/OS process cleanup can still stop it.

## Status updates

When addressing the user as orchestrator, keep the user informed of work, stage and worker. Language: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries). Worker-to-orchestrator updates follow [brief-writing, Language](brief-writing.md#language).

- **When:** after you start sessions; when a session finishes; when you accept a result or request a fix; when something blocks; whenever the user asks; and in your final message of every turn while any session of the task is not yet accepted. Do not send updates when nothing changed.
- **Format:** one line on the whole task, then the session log without the threadId, runId, statusFile and brief columns (include IDs and resume commands when handing off unfinished runs):

  ```
  Task: <name> - 1 of 3 accepted, 1 running, 1 waiting.

  | # | Session | Worker | Stage | Since | Next |
  |---|---------|--------|-------|-------|------|
  | 1 | CSV export | codex, sol, high | accepted | 14:20 | - |
  | 2 | Export review | codex, sol, high | running | 14:22 | I check its findings |
  | 3 | Docs | codex, sol, medium | waiting for #2 | - | starts after #2 is accepted |
  ```

- Add one line for anything the user must do or decide, and say plainly if nothing is needed from them.
- Keep the stage names from the session log so the same word always means the same thing.

## Checking a finished session

The final message is the worker's claim. Check it against the files before you accept anything.

1. **Read the report.** Write down what the worker says it did, which checks it ran and what it says it did not verify. If the final message is about something else (a hook or memory error), read the event log for the real report.
2. **See what actually changed.** `git status` and `git diff --stat` in the working folder, against the starting point. Then read the diff of the files that matter. Look for changes nobody asked for.
3. **Rerun the checks.** Run the tests, builds and commands from the brief's acceptance yourself, at least the cheap ones. A test the worker reports as passed but that fails for you is a failure.
4. **Go through the requirements.** For each numbered requirement in the brief, name the evidence: a file and line, a test, a command output. A requirement without evidence is not done.
5. **Check the boundaries.** Check actual changes against AGENTS authorization and the brief’s allowed files/actions; check old names/leftovers when required. Worker artifacts follow agent-sessions, Worker artifacts.
6. **Try the behaviour, not only the tests.** Run the real scenario the user cares about, including an edge case: install and then upgrade, open the screen, feed an empty or very large input, run from a fresh clone. Tests passing while the real scenario fails is common. Typical findings of this step: files left behind after a migration, logic that works for only one version, a pipeline that fails in a clean environment.
7. **Decide.**
   - **Accepted:** every requirement has evidence and nothing is outside the boundaries.
   - **Fix requested:** something specific is wrong or missing. Continue the same session with a short follow-up brief (see [writing the brief](brief-writing.md)): what is wrong, what to do, how it will be checked. Choose continuation effort under [agent-sessions, step 3](../../agent-sessions/SKILL.md#3-choose-effort-and-access); preserve other approved settings.
   - **Redo:** the result is wrong at its core. Continue the same normal worker with a corrected brief; effort changes follow agent-sessions, step 3.
   - Fix it yourself only when it is small and continuing the session is not worth it. Say that you did.
8. **Update the log** with the verdict and what you verified.

Independent reviewer continuation and replacement: see [independent-review, After the report](../../../workflow/independent-review.md#after-the-report).

## Questions and blocked workers

Native unattended approval/question prompts follow [adapter contract, Unattended runs](../../agent-sessions/references/contract.md#unattended-runs). In addition to that transport rule, an authorized asynchronous Jam Board question is a stored board operation, not a native prompt. Post it under the task and work on independent parts. Wait only within the approved run/time budget; if the decision is still pending when that budget ends or no independent work remains, return a blocked report with question ID and resume conditions. Retain the claim unless explicitly relinquishing it under Jam Board, Worker procedure.

## Reporting

After all sessions are accepted, or when you need the user's decision, report directly to the user per session using AGENTS language defaults. Worker-to-orchestrator reports and final responses follow [brief-writing, Language](brief-writing.md#language).

- what it did;
- what you verified and how (which commands you ran, what you opened);
- what remains unverified and why;
- what the user needs to decide next: commit, push, publish, a choice between variants.

Git authorization: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries); worker artifacts: see agent-sessions, Worker artifacts.
