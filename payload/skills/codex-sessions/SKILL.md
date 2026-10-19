---
name: codex-sessions
description: Run work in OpenAI Codex sessions that the user can watch in the Codex app, acting as the orchestrator that writes the brief, starts or continues the session, and checks the result. Use when the user asks to give a task to Codex, run something "in Codex", have Codex do it, or continue a Codex chat. Do not use for work you should do yourself, and do not start sessions on your own initiative.
---

# Codex sessions

You are the orchestrator: you understand what the user wants, hand a piece of work to a Codex session, and check what comes back. The user watches the session in the Codex app and may step in there.

Run Codex through `scripts/codex-chat.mjs`. It starts `codex app-server` on the user's own Codex home, so the thread shows up in the app with the name you give it. Do not use `codex exec`: those threads are hidden from the app's list. Do not use a temporary `CODEX_HOME`, which keeps the thread out of the user's history entirely. Do not pass `--ignore-user-config`, which drops the user's instructions, skills and hooks. The only exception is an isolated experiment that the user asked to be isolated.

## Before starting

- Start a session only when the user asked for this work to go to Codex. One request covers that request's sessions, not later ones.
- Decide whether this is a new task or the next step of an existing thread. For a correction, a follow-up or a review comment on work a thread already did, continue that thread (`--thread <id>`). The thread already holds the context, and the user sees the conversation in one place.
- Give one thread one task. For parallel work, give each writer its own folder or git worktree; two sessions never edit the same files.

## Write the brief

Codex starts from the brief, the files and its own instructions, not from your conversation. Write the brief in the user's language and include:

- The goal and who it is for, in the user's words. Quote the user where wording matters.
- Where to work: folder, branch, the files that matter and what to read first.
- What done looks like: observable acceptance, plus the checks to run.
- Boundaries: what not to touch, what is not permitted (pushing, publishing, deleting, network calls), and decisions it must leave to the user.
- What to report at the end: what changed, the results of checks, what was not verified.

Describe the task, not your own solution. Codex has its own workflow and skills; over-prescribing steps lowers the quality. Do not paste secrets, tokens or private data the task does not need.

Save the brief to a file next to the work, or in your scratch directory, and pass it with `--prompt`.

## Run

```bash
node <skill-dir>/scripts/codex-chat.mjs --cwd <work folder> --name "<short title the user will recognize>" \
  --prompt brief.md --out final.md --log events.jsonl [--effort <level>] [--model <id>]
```

- Continue a thread: add `--thread <threadId>`, using the ID from the JSON line printed last by the previous run.
- `--sandbox` defaults to `workspace-write`: Codex writes only inside `--cwd`. Use `read-only` for review or investigation. Use `danger-full-access` only when the user explicitly allows it for this task.
- Approval requests and questions are declined automatically: the run is unattended. If a task needs a permission, decide that before starting, or let the user run it in the app.
- Large tasks take tens of minutes. Run the command in the background and wait to be notified; do not poll in a loop. Tell the user the session's name so they can open it.
- Exit code 0 means the turn completed. The last stdout line is `{threadId, turnId, status, out}`.

## Check the result

The final message is a report, not proof. Before telling the user the work is done:

- Read the actual diff or files. Run the checks yourself where that is cheap.
- Compare the result with the brief's acceptance. Note anything missing or invented.
- If something is wrong, continue the same thread with a concrete correction rather than fixing it silently. Fix it yourself only when it is small and continuing the thread is not worth it, and say that you did.
- Report what the session did, what you verified, and what remains unverified.

## Known limits

- On Windows the workspace-write sandbox blocks writes inside `.git`, so Codex cannot commit. Review its changes and commit them yourself only if the user asked for a commit. Pushing and publishing need the user's explicit permission each time.
- The sandbox may block launching a browser (EPERM). For visual checks, inspect the result yourself or ask the user to look.
- The user's hooks from Codex settings, including any memory hooks, also run in these sessions. If the final message is about a hook or memory error instead of the task, read the task's result from the files and `events.jsonl`.
- `--proxy` works only when an app-server daemon is running (`codex app-server daemon start`). The desktop app usually runs its own server and does not expose this socket; the default mode does not need it.
- If the CLI is not found, set `CODEX_BIN` to the codex executable.
