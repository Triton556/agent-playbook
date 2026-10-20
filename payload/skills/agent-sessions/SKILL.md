---
name: agent-sessions
description: Orchestrate worker sessions in other agent clients (Codex, Claude Code, or any client with an adapter) - find out the requirements, split the work, write the briefs, get the user's approval of the whole plan, start or continue the sessions, and check the results. Use when the user asks to hand work to another agent or session, or when part of the current work would clearly gain from a separate session (independent parallel pieces, long work, an independent review); then propose it and wait for the user's yes. Also use when the user asks to add support for a new worker client. Do not use for small work you can do yourself.
---

# Agent sessions

You are the orchestrator: you understand what the user wants, hand pieces of work to worker sessions, and check what comes back. Workers run in other agent clients through adapters in `adapters/`. Every adapter follows one [contract](references/contract.md), so the procedure below is the same for every worker.

## Fixed rules

- **Separate sessions, never built-in subagents.** Delegated work always goes to a separate session started through an adapter. Do not use your client's built-in subagent tools for it (`spawn_agent` or multi-agent tools in Codex, `Task` or `Agent` in Claude Code, and similar): the user cannot see those, cannot step into them or continue them, and the work has no thread of its own.
- **Briefs are in English.** Every task you give a worker is written in English, whatever language the user speaks. Quote the user verbatim where exact wording matters.
- **Reports follow the reader.** A worker reports to you in English. Everything the user reads is in the user's language: your messages, and the worker's user-facing output such as interface text and documents, unless the user asked otherwise.
- **The user chooses the model.** Never pick a worker's model yourself. If the user has not named one, ask, listing the options the adapter supports. A standing choice ("use X for everything") holds until the user changes it.
- **You choose the effort, from the lowest level that fits.** Follow the effort table below; never use the maximum by default.
- **Nothing starts before the user approves the whole plan,** with the briefs already written.
- **Briefs and worker reports stay local.** Never commit them to the project or publish them.

## Workflow

### 1. Find out the requirements

Follow [finding out the requirements](references/requirements-interview.md): restate the goal, collect the facts yourself, then ask the user in rounds, each question with your recommended answer, until no open decision would change the plan. Skip this for a small, unambiguous task or when an accepted brief exists.

### 2. Split the work

Decide what you do yourself and what goes to sessions. Delegate only when it pays: independent pieces that can run in parallel, long work, an independent review or a second variant. Do small or tightly coupled work yourself; each session starts cold and costs a brief and a check.

- One session, one task. Two sessions never edit the same files.
- Note dependencies: a session that needs another's result waits until that result is checked.
- For a correction or follow-up on work a session already did, plan to continue that session, not a new one.
- Choose the worker client: run `node adapters/<agent>.mjs --describe`. It reports where the user can watch the session, whether it can be continued, its effort levels, what each access mode actually enforces, and whether the adapter was checked live (`verified`). Do not promise more than it describes.

Available adapters: `codex` (OpenAI Codex, sessions visible in the Codex app; checked live) and `claude-code` (Claude Code headless sessions; **not checked live**). Before relying on `claude-code`, tell the user it is unverified and, with their agreement, run the checks from [writing an adapter](references/writing-an-adapter.md) on a tiny task. For another client, write an adapter first.

### 3. Choose effort and access

Effort, per session. Start from the lowest level that fits; every step up needs a reason from this table.

| Level | Use for | Examples |
|---|---|---|
| `low` | one small, clear change | fix a typo or a config value, rename one thing, run the tests and report |
| `medium` | mechanical work across many files against a clear spec | renames or migrations by a mapping, moving files, writing tests to a given spec, applying an existing pattern elsewhere, updating docs across files |
| `high` | ordinary engineering that needs judgment | a feature across layers, a bug with an unknown cause, code review, building a UI from an accepted design, a performance investigation |
| `xhigh` | costly mistakes or many interacting parts | designing a subsystem, a large refactor, security-sensitive changes, concurrency, data migration with a risk of loss |
| maximum (`ultra` in Codex, `max` in Claude Code) | only the three cases below | |

The maximum is allowed only when:

1. the task is open creative or design exploration with no single right answer;
2. a lower level already failed on this same task; or
3. the user asked for it.

Never use the maximum for mechanical work, documentation edits, running tests or reviewing a small change. More than one session at the maximum in one plan needs its own justification. If a worker fails, continue the same session one level higher with a concrete correction.

Effort names differ between clients; use the levels from the adapter's description.

Access mode, per session, passed with `--sandbox`; recommend one, the user decides:

- `read-only`: review, investigation, audit.
- `workspace-write` (default): changes inside the working folder.
- `danger-full-access`: no restrictions. Only when the user chose it for that session; say why it is needed.

The same name can mean different protection in different clients: in Codex it is an OS sandbox, in Claude Code a permission mode. Say so when it matters. If an adapter refuses a mode (exit code 4), tell the user instead of picking another mode yourself.

### 4. Write the briefs

Follow [writing the brief](references/brief-writing.md). Write every brief before asking for approval, so the user approves the actual tasks. Save each one to a local file outside the project's tracked files.

### 5. Get approval with a summary

Show the user one summary in their language and wait:

```
Task: <one line: what and for whom>
Done when: <two to four observable checks>

| # | Session | Does | Model | Effort and why | Access | Folder | Waits for | Brief |
|---|---------|------|-------|----------------|--------|--------|-----------|-------|
| 1 | <name the user will see> | <one line> | <user's choice> | <level: reason> | <mode> | <path> | - | <brief file> |
| 2 | ... | ... | ... | ... | ... | ... | 1 | ... |

I do meanwhile: <your own part, or "nothing">
How I will check: <per session, the checks you will run yourself>
Approve?
```

A yes covers the sessions in that table with the settings and briefs shown, including follow-up turns needed to reach the agreed result. A new session, or a different model, access mode, worker, goal or substantially changed brief, needs a new yes. If the user changes something in the reply, update the table and the briefs, and show what changed.

### 6. Run and check

Follow [running and checking sessions](references/running-and-checking.md): prepare folders, start the sessions in the background, keep a session log, and check every result yourself before accepting it. The final message of a session is a report, not proof.

### 7. Report to the user

In the user's language, per session: what it did, what you verified and how, what remains unverified, and what the user needs to decide next.

## Known limits

- Your own access is set by the user in your client. If your sandbox blocks an adapter (exit code 3), tell the user and ask them to approve the command or choose an access mode for you. Do not work around it.
- The user's own settings and hooks run in worker sessions too. If the final message is about a hook or memory error instead of the task, read the result from the files and the event log.
- Codex on Windows: `workspace-write` cannot write inside `.git`, so the worker cannot commit. Commit after review only if the user asked; pushing and publishing need the user's explicit permission each time.
- Claude Code: the worker needs a CLI that is logged in on its own. The CLI bundled with the desktop app gets its login from the app and fails with "Not logged in" when started separately.
