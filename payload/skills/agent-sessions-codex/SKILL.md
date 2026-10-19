---
name: agent-sessions-codex
description: Run work in OpenAI Codex sessions that the user can watch in the Codex app, acting as the orchestrator that finds out the requirements, proposes the sessions, writes the briefs, starts or continues them after the user agrees, and checks the results. Use when the user asks to give a task to Codex, run something "in Codex" or continue a Codex chat, and when part of the current work would clearly gain from a separate Codex session (independent parallel pieces, long work, an independent review); then propose it and wait for the user's yes. Do not use for small work you can do yourself.
---

# Codex sessions

You are the orchestrator: you understand what the user wants, hand pieces of work to Codex sessions, and check what comes back. The user watches each session in the Codex app and may step in there.

Run Codex through `scripts/codex-chat.mjs`. It starts `codex app-server` on the user's own Codex home, so the thread shows up in the app with the name you give it. Do not use `codex exec`: those threads are hidden from the app's list. Do not use a temporary `CODEX_HOME`, which keeps the thread out of the user's history entirely. Do not pass `--ignore-user-config`, which drops the user's instructions, skills and hooks. The only exception is an isolated experiment that the user asked to be isolated.

## Fixed rules

- **Briefs are in English.** Every task you give Codex is written in English, whatever language the user speaks. Quote the user verbatim where exact wording matters.
- **Reports follow the reader.** Codex reports to you in English. Everything the user reads is in the user's language: your messages, and Codex's user-facing output such as interface text and documents, unless the user asked otherwise.
- **The user chooses the model.** Never pick the model yourself. If the user has not named one, ask. A standing choice ("use X for everything") holds until the user changes it.
- **You choose the effort.** Pick it per session from the task (see step 2) and state the reason in the plan.
- **No session without a yes.** Start only the sessions the user agreed to, with the settings they saw.

## Workflow

### 1. Find out the requirements

Follow [finding out the requirements](references/requirements-interview.md): restate the goal, collect the facts yourself, then ask the user in rounds, each question with your recommended answer, until no open decision would change the plan; confirm a short summary with checkable acceptance. Skip this for a small, unambiguous task or when an accepted brief exists.

### 2. Propose the plan

Propose delegation only when it pays: independent pieces that can run in parallel, long work, an independent review or a second variant. Do small or tightly coupled work yourself; each session starts cold and costs a brief and a review. For a correction or follow-up on work a thread already did, plan to continue that thread instead of starting a new one.

For each session, show:

- the name the user will see in the Codex app, and a one-line goal;
- the model the user chose, or a question asking for it;
- the effort you chose, with a one-line reason;
- the folder and the access mode;
- what you keep doing yourself meanwhile.

Choose effort for the task, not the client's default. Codex levels: minimal, low, medium, high, xhigh, ultra. A starting point, not a measured rule:

- `low`: a small, clear change in one place.
- `medium`: mechanical work across many files against a clear spec: renames, moves, migrations, routine fixes.
- `high`: ordinary engineering that needs judgment: a feature across layers, debugging with an unknown cause, code review.
- `xhigh`: costly mistakes or many interacting parts: architecture choices, large refactors, concurrency or data-loss risks.
- `ultra`: open design or creative exploration, research where depth clearly pays, or a task a lower level already failed.

Access modes, passed with `--sandbox`; recommend one and let the user choose:

- `read-only`: review, investigation, audit. Reads files, changes nothing.
- `workspace-write` (default): writes only inside `--cwd`. On Windows it cannot write inside `.git`.
- `danger-full-access`: no sandbox. Only when the user chose it for that session; say why it is needed, for example the session must itself start Codex sessions or write outside its folder.

Wait for the answer. A yes covers the sessions in that plan with the settings shown, including follow-up turns needed to reach the agreed result. A new session, or a different model, access mode or goal, needs a new yes. If the user changes settings in the reply, use theirs.

### 3. Write the briefs

Follow [writing the brief](references/brief-writing.md): its template, rules and examples. The brief is self-contained, in English, describes the outcome rather than your solution, and has observable acceptance. Codex has its own workflow and skills; over-prescribing steps lowers the quality. Save each brief to a file next to the work or in your scratch directory.

### 4. Run

```bash
node <skill-dir>/scripts/codex-chat.mjs --cwd <work folder> --name "<short title the user will recognize>" \
  --prompt brief.md --sandbox <mode> --model <user's choice> --effort <your choice> \
  --out final.md --log events.jsonl
```

- Continue a thread with `--thread <threadId>`, using the ID from the JSON line printed last by the previous run, and a short follow-up brief. Pass `--sandbox`, `--model` and `--effort` again: they are not remembered between runs.
- Give one thread one task. For parallel work, give each writer its own folder or git worktree; two sessions never edit the same files.
- Approval requests and questions are declined automatically: the run is unattended. If a task needs a permission, decide that before starting, or let the user run it in the app.
- Large tasks take tens of minutes. Run the command in the background and wait to be notified; do not poll in a loop. Tell the user the session's name so they can open it.
- Exit code 0 means the turn completed. The last stdout line is `{threadId, turnId, status, out}`.

Your own access is set by the user in your client. If your sandbox blocks the driver, tell the user and ask them to approve the command or choose an access mode for you. Do not work around it.

### 5. Check the result

The final message is a report, not proof. Before telling the user the work is done:

- Read the actual diff or files. Run the checks yourself where that is cheap.
- Compare the result with the brief's acceptance. Note anything missing or invented.
- If something is wrong, continue the same thread with a concrete correction rather than fixing it silently. Fix it yourself only when it is small and continuing the thread is not worth it, and say that you did.

### 6. Report to the user

In the user's language: what the session did, what you verified and how, what remains unverified, and what the user needs to decide next.

## Known limits

- When the orchestrator itself runs inside a Codex sandbox, starting `codex app-server` fails with `spawn EPERM` (exit code 3) and no thread is created. The user decides how you may run it.
- On Windows the workspace-write sandbox blocks writes inside `.git`, so Codex cannot commit. Review its changes and commit them yourself only if the user asked for a commit. Pushing and publishing need the user's explicit permission each time.
- The sandbox may block launching a browser (EPERM). For visual checks, inspect the result yourself or ask the user to look.
- The user's hooks from Codex settings, including any memory hooks, also run in these sessions. If the final message is about a hook or memory error instead of the task, read the task's result from the files and `events.jsonl`.
- `--proxy` works only when an app-server daemon is running (`codex app-server daemon start`). The desktop app usually runs its own server and does not expose this socket; the default mode does not need it.
- If the CLI is not found, set `CODEX_BIN` to the codex executable.
