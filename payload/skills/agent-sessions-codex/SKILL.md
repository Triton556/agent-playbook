---
name: agent-sessions-codex
description: Run work in OpenAI Codex sessions that the user can watch in the Codex app, acting as the orchestrator that finds out the requirements, splits the work, writes the briefs, gets the user's approval of the whole plan, starts or continues the sessions, and checks the results. Use when the user asks to give a task to Codex, run something "in Codex" or continue a Codex chat, and when part of the current work would clearly gain from a separate Codex session (independent parallel pieces, long work, an independent review); then propose it and wait for the user's yes. Do not use for small work you can do yourself.
---

# Codex sessions

You are the orchestrator: you understand what the user wants, hand pieces of work to Codex sessions, and check what comes back. The user watches each session in the Codex app and may step in there.

Run Codex through `scripts/codex-chat.mjs`. It starts `codex app-server` on the user's own Codex home, so the thread shows up in the app with the name you give it. Do not use `codex exec`: those threads are hidden from the app's list. Do not use a temporary `CODEX_HOME`, which keeps the thread out of the user's history entirely. Do not pass `--ignore-user-config`, which drops the user's instructions, skills and hooks. The only exception is an isolated experiment that the user asked to be isolated.

## Fixed rules

- **Separate Codex sessions, never built-in subagents.** Delegated work always goes to a separate Codex session started with `scripts/codex-chat.mjs`. Do not use built-in subagent tools for it (`spawn_agent` or multi-agent tools in Codex, `Task` or `Agent` in Claude Code, and similar): the user cannot see those in the thread list, cannot step into them or continue them, and the work has no thread of its own.
- **Briefs are in English.** Every task you give Codex is written in English, whatever language the user speaks. Quote the user verbatim where exact wording matters.
- **Reports follow the reader.** Codex reports to you in English. Everything the user reads is in the user's language: your messages, and Codex's user-facing output such as interface text and documents, unless the user asked otherwise.
- **The user chooses the model.** Never pick the model yourself. If the user has not named one, ask. A standing choice ("use X for everything") holds until the user changes it.
- **You choose the effort, from the lowest level that fits.** Follow the effort table below; never use `ultra` by default.
- **Nothing starts before the user approves the whole plan,** with the briefs already written.
- **Briefs and Codex reports stay local.** Never commit them to the project or publish them.

## Workflow

### 1. Find out the requirements

Follow [finding out the requirements](references/requirements-interview.md): restate the goal, collect the facts yourself, then ask the user in rounds, each question with your recommended answer, until no open decision would change the plan. Skip this for a small, unambiguous task or when an accepted brief exists.

### 2. Split the work

Decide what you do yourself and what goes to Codex sessions. Delegate only when it pays: independent pieces that can run in parallel, long work, an independent review or a second variant. Do small or tightly coupled work yourself; each session starts cold and costs a brief and a check.

- One session, one task. Two sessions never edit the same files.
- Note dependencies: a session that needs another's result waits until that result is checked.
- For a correction or follow-up on work a thread already did, plan to continue that thread, not a new one.

### 3. Choose effort and access

Effort, per session. Codex levels: minimal, low, medium, high, xhigh, ultra. Start from the lowest level that fits; every step up needs a reason from this table.

| Level | Use for | Examples |
|---|---|---|
| `low` | one small, clear change | fix a typo or a config value, rename one thing, run the tests and report |
| `medium` | mechanical work across many files against a clear spec | renames or migrations by a mapping, moving files, writing tests to a given spec, applying an existing pattern elsewhere, updating docs across files |
| `high` | ordinary engineering that needs judgment | a feature across layers, a bug with an unknown cause, code review, building a UI from an accepted design, a performance investigation |
| `xhigh` | costly mistakes or many interacting parts | designing a subsystem, a large refactor, security-sensitive changes, concurrency, data migration with a risk of loss |
| `ultra` | only the three cases below | |

`ultra` is allowed only when:

1. the task is open creative or design exploration with no single right answer;
2. a lower level already failed on this same task; or
3. the user asked for it.

Never use `ultra` for mechanical work, documentation edits, running tests or reviewing a small change. More than one `ultra` session in one plan needs its own justification. If a session fails, continue the same thread one level higher with a concrete correction.

Access mode, per session, passed with `--sandbox`; recommend one, the user decides:

- `read-only`: review, investigation, audit. Reads files, changes nothing.
- `workspace-write` (default): writes only inside `--cwd`. On Windows it cannot write inside `.git`.
- `danger-full-access`: no sandbox. Only when the user chose it for that session; say why it is needed, for example the session must itself start Codex sessions or write outside its folder.

### 4. Write the briefs

Follow [writing the brief](references/brief-writing.md). Write every brief before asking for approval, so the user approves the actual tasks. Save each one to a local file outside the project's tracked files. Codex has its own workflow and skills; describe the outcome, not every step.

### 5. Get approval with a summary

Show the user one summary in their language and wait:

```
Task: <one line: what and for whom>
Done when: <two to four observable checks>

| # | Session | Does | Model | Effort and why | Access | Folder | Waits for | Brief |
|---|---------|------|-------|----------------|--------|--------|-----------|-------|
| 1 | <name the user will see in the Codex app> | <one line> | <user's choice> | <level: reason> | <mode> | <path> | - | <brief file> |
| 2 | ... | ... | ... | ... | ... | ... | 1 | ... |

I do meanwhile: <your own part, or "nothing">
How I will check: <per session, the checks you will run yourself>
Approve?
```

A yes covers the sessions in that table with the settings and briefs shown, including follow-up turns needed to reach the agreed result. A new session, or a different model, access mode, goal or substantially changed brief, needs a new yes. If the user changes something in the reply, update the table and the briefs, and show what changed.

### 6. Run and check

Follow [running and checking sessions](references/running-and-checking.md). The command for a session:

```bash
node <skill-dir>/scripts/codex-chat.mjs --cwd <work folder> --name "<session name from the table>" \
  --prompt <brief file> --sandbox <mode> --model <user's choice> --effort <your choice> \
  --out <final.md> --log <events.jsonl>
```

- Continue a thread with `--thread <threadId>` from the JSON line printed last by the previous run, and a short follow-up brief. Pass `--sandbox`, `--model` and `--effort` again: they are not remembered between runs.
- Approval requests and questions inside the session are declined automatically: the run is unattended. If a task needs a permission, decide that before starting, or let the user run it in the app.
- Exit code 0 means the turn completed. The last stdout line is `{threadId, turnId, status, out}`.

### 7. Report to the user

In the user's language, per session: what it did, what you verified and how, what remains unverified, and what the user needs to decide next.

## Known limits

- When the orchestrator itself runs inside a Codex sandbox, starting `codex app-server` fails with `spawn EPERM` (exit code 3) and no thread is created. Tell the user and ask them to approve the command or choose an access mode for you. Do not work around it.
- On Windows the workspace-write sandbox blocks writes inside `.git`, so Codex cannot commit. Review its changes and commit them yourself only if the user asked for a commit. Pushing and publishing need the user's explicit permission each time.
- The sandbox may block launching a browser (EPERM). For visual checks, inspect the result yourself or ask the user to look.
- The user's hooks from Codex settings, including any memory hooks, also run in these sessions. If the final message is about a hook or memory error instead of the task, read the task's result from the files and `events.jsonl`.
- `--proxy` works only when an app-server daemon is running (`codex app-server daemon start`). The desktop app usually runs its own server and does not expose this socket; the default mode does not need it.
- If the CLI is not found, set `CODEX_BIN` to the codex executable.
