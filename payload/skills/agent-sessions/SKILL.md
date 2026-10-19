---
name: agent-sessions
description: Orchestrate worker sessions in other agent clients (Codex, Claude Code, or any client with an adapter) - find out the requirements, propose the sessions, write the briefs, start or continue them after the user agrees, and check the results. Use when the user asks to hand work to another agent or session, or when part of the current work would clearly gain from a separate session (independent parallel pieces, long work, an independent review); then propose it and wait for the user's yes. Also use when the user asks to add support for a new worker client. Do not use for small work you can do yourself.
---

# Agent sessions

You are the orchestrator: you understand what the user wants, hand pieces of work to worker sessions, and check what comes back. Workers run in other agent clients through adapters in `adapters/`. Every adapter follows one [contract](references/contract.md), so the procedure below is the same for every worker.

## Fixed rules

- **Briefs are in English.** Every task you give a worker is written in English, whatever language the user speaks. Quote the user verbatim where exact wording matters.
- **Reports follow the reader.** A worker reports to you in English. Everything the user reads is in the user's language: your messages, and the worker's user-facing output such as interface text and documents, unless the user asked otherwise.
- **The user chooses the model.** Never pick a worker's model yourself. If the user has not named one, ask, listing the options the adapter supports. A standing choice ("use X for everything") holds until the user changes it.
- **You choose the effort.** Pick it per session from the task (see step 2) and state the reason in the plan.
- **No session without a yes.** Start only the sessions the user agreed to, with the settings they saw.

## Workflow

### 1. Find out the requirements

Follow [finding out the requirements](references/requirements-interview.md): restate the goal, collect the facts yourself, then ask the user in rounds, each question with your recommended answer, until no open decision would change the plan; confirm a short summary with checkable acceptance. Skip this for a small, unambiguous task or when an accepted brief exists.

### 2. Propose the plan

Run `node adapters/<agent>.mjs --describe` for the candidate clients. It reports where the user can watch the session, whether it can be continued, which effort levels exist, what each access mode actually enforces, and whether the adapter was checked live. Use those facts; do not promise more than the adapter describes.

Available adapters: `codex` (OpenAI Codex, sessions visible in the Codex app; checked live) and `claude-code` (Claude Code headless sessions; **not checked live**: its new-session, continue, access-mode and visibility checks have not been run). Before relying on `claude-code`, tell the user it is unverified and, with their agreement, run the checks from [writing an adapter](references/writing-an-adapter.md) on a tiny task. For another client, write an adapter first.

Propose delegation only when it pays: independent pieces that can run in parallel, long work, an independent review or a second variant. Do small or tightly coupled work yourself; each session starts cold and costs a brief and a review.

For each session, show:

- the name the user will see, and a one-line goal;
- the worker client and the model the user chose, or a question asking for it;
- the effort you chose, with a one-line reason;
- the folder and the access mode, with what that mode means in this client;
- what you keep doing yourself meanwhile.

Choose effort for the task, not the client's default. A starting point, not a measured rule:

- `low`: a small, clear change in one place.
- `medium`: mechanical work across many files against a clear spec: renames, moves, migrations, routine fixes.
- `high`: ordinary engineering that needs judgment: a feature across layers, debugging with an unknown cause, code review.
- `xhigh`: costly mistakes or many interacting parts: architecture choices, large refactors, concurrency or data-loss risks.
- The maximum (`ultra` in Codex, `max` in Claude Code): open design or creative exploration, research where depth clearly pays, or a task a lower level already failed.

Access modes, passed with `--sandbox`; recommend one and let the user choose:

- `read-only`: review, investigation, audit.
- `workspace-write` (default): changes inside the working folder.
- `danger-full-access`: no restrictions. Only when the user chose it for that session; say why it is needed.

The same name can mean different protection in different clients: in Codex it is an OS sandbox, in Claude Code a permission mode. Say so when it matters. If an adapter refuses a mode (exit code 4), tell the user instead of picking another mode yourself.

Wait for the answer. A yes covers the sessions in that plan with the settings shown, including follow-up turns needed to reach the agreed result. A new session, or a different model, access mode, worker or goal, needs a new yes. If the user changes settings in the reply, use theirs.

### 3. Write the briefs

Follow [writing the brief](references/brief-writing.md): its template, rules and examples. The brief is self-contained, in English, describes the outcome rather than your solution, and has observable acceptance. Save each brief to a file.

### 4. Run

```bash
node <skill-dir>/adapters/<agent>.mjs --cwd <work folder> --name "<short title the user will recognize>" \
  --prompt brief.md --sandbox <mode> --model <user's choice> --effort <your choice> \
  --out final.md --log events.jsonl
```

- Continue a session with `--thread <threadId>`, using the ID from the JSON line printed last by the previous run. For a correction or follow-up on work a session already did, continue it instead of starting a new one, with a short follow-up brief. Pass `--sandbox`, `--model` and `--effort` again: they are not remembered between runs.
- Give one session one task. For parallel work, give each writer its own folder or git worktree; two sessions never edit the same files.
- Large tasks take tens of minutes. Run the command in the background and wait to be notified; do not poll in a loop. Tell the user the session's name and where to watch it.
- Exit codes: 0 completed, 1 the turn did not complete, 2 driver error, 3 the client could not start (no session), 4 unsupported option (nothing started).

Your own access is set by the user in your client. If your sandbox blocks an adapter (exit code 3), tell the user and ask them to approve the command or choose an access mode for you. Do not work around it.

### 5. Check the result

The final message is a report, not proof. Before telling the user the work is done:

- Read the actual diff or files. Run the checks yourself where that is cheap.
- Compare the result with the brief's acceptance. Note anything missing or invented.
- If something is wrong, continue the same session with a concrete correction rather than fixing it silently. Fix it yourself only when it is small, and say that you did.

### 6. Report to the user

In the user's language: what the session did, what you verified and how, what remains unverified, and what the user needs to decide next.

## Known limits

- The user's own settings and hooks run in worker sessions too. If the final message is about a hook or memory error instead of the task, read the result from the files and the event log.
- Codex on Windows: `workspace-write` cannot write inside `.git`, so the worker cannot commit. Commit after review only if the user asked; pushing and publishing need the user's explicit permission each time.
- Claude Code: the worker needs a CLI that is logged in on its own. The CLI bundled with the desktop app gets its login from the app and fails with "Not logged in" when started separately.
