---
name: agent-sessions
description: Orchestrate worker sessions in other agent clients (Codex, Claude Code, or any client with an adapter) - propose the sessions, write the briefs, start or continue them after the user agrees, and check the results. Use when the user asks to hand work to another agent or session, or when part of the current work would clearly gain from a separate session (independent parallel pieces, long work, an independent review); then propose it and wait for the user's yes. Also use when the user asks to add support for a new worker client. Do not use for small work you can do yourself.
---

# Agent sessions

You are the orchestrator: you understand what the user wants, hand pieces of work to worker sessions, and check what comes back. Workers run in other agent clients through adapters in `adapters/`. Every adapter follows one [contract](references/contract.md), so the procedure below is the same for every worker.

## Choose the worker

Run `node adapters/<agent>.mjs --describe` for the candidate clients. It reports where the user can watch the session, whether it can be continued, and what each access mode actually enforces in that client. Use those facts in your plan; do not promise more than the adapter describes.

Available adapters: `codex` (OpenAI Codex, sessions visible in the Codex app; checked live) and `claude-code` (Claude Code headless sessions; **not checked live**: its new-session, continue, access-mode and visibility checks have not been run). Before relying on `claude-code`, tell the user it is unverified and, with their agreement, run the checks from [writing an adapter](references/writing-an-adapter.md) on a tiny task. For another client, write an adapter first: see [writing an adapter](references/writing-an-adapter.md).

## Propose, then start

Never start a session without the user's yes for it.

- When the user asks to delegate, or you see a piece worth delegating, first show a short plan: for each session, its name, a one-line goal, the worker client and model, effort, folder, access mode, and what you will keep doing yourself. Then wait for the answer.
- Propose delegation only when it pays: independent pieces that can run in parallel, long work, an independent review or a second variant. Do small or tightly coupled work yourself; each session starts cold and costs a brief and a review.
- A yes covers the sessions in that plan with the settings shown, including follow-up turns needed to reach the agreed result. A new session, a different access mode, worker or goal needs a new yes.
- If the user changes the settings in their reply, use theirs.

## Access modes

Show an access mode for every proposed session, with your recommendation and what it means in that client (from `--describe`), and let the user choose. Pass the choice with `--sandbox`:

- `read-only`: review, investigation, audit.
- `workspace-write` (default): changes inside the working folder.
- `danger-full-access`: no restrictions. Only when the user chose it for that session; say why it is needed.

The same name can mean different protection in different clients: in Codex it is an OS sandbox, in Claude Code a permission mode. Say so when it matters. If an adapter refuses a mode (exit code 4), tell the user instead of picking another mode yourself.

A mode applies only to the session it was chosen for. Your own access is set by the user in your client. If your sandbox blocks an adapter (exit code 3), tell the user and ask them to approve the command or choose an access mode for you. Do not work around it.

## Write the brief

The worker starts from the brief, the files and its own instructions, not from your conversation. Write the brief in the user's language and include:

- The goal and who it is for, in the user's words. Quote the user where wording matters.
- Where to work: folder, branch, the files that matter and what to read first.
- What done looks like: observable acceptance, plus the checks to run.
- Boundaries: what not to touch, what is not permitted (pushing, publishing, deleting, network calls), and decisions it must leave to the user.
- What to report at the end: what changed, the results of checks, what was not verified.

Describe the task, not your own solution; the worker has its own workflow. Do not paste secrets or private data the task does not need. Save the brief to a file and pass it with `--prompt`.

## Run

```bash
node <skill-dir>/adapters/<agent>.mjs --cwd <work folder> --name "<short title the user will recognize>" \
  --prompt brief.md --sandbox <mode> --out final.md --log events.jsonl [--model <id>] [--effort <level>]
```

- Continue a session with `--thread <threadId>`, using the ID from the JSON line printed last by the previous run. For a correction or follow-up on work a session already did, continue it instead of starting a new one. Pass `--sandbox` again: it is not remembered between runs.
- Give one session one task. For parallel work, give each writer its own folder or git worktree; two sessions never edit the same files.
- Large tasks take tens of minutes. Run the command in the background and wait to be notified; do not poll in a loop. Tell the user the session's name and where to watch it.
- Exit codes: 0 completed, 1 the turn did not complete, 2 driver error, 3 the client could not start (no session), 4 unsupported option (nothing started).

## Check the result

The final message is a report, not proof. Before telling the user the work is done:

- Read the actual diff or files. Run the checks yourself where that is cheap.
- Compare the result with the brief's acceptance. Note anything missing or invented.
- If something is wrong, continue the same session with a concrete correction rather than fixing it silently. Fix it yourself only when it is small, and say that you did.
- Report what the session did, what you verified, and what remains unverified.

## Known limits

- The user's own settings and hooks run in worker sessions too. If the final message is about a hook or memory error instead of the task, read the result from the files and the event log.
- Codex on Windows: `workspace-write` cannot write inside `.git`, so the worker cannot commit. Commit after review only if the user asked; pushing and publishing need the user's explicit permission each time.
- Claude Code: the worker needs a CLI that is logged in on its own. The CLI bundled with the desktop app gets its login from the app and fails with "Not logged in" when started separately.
