---
name: agent-sessions
description: Orchestrate worker sessions in other agent clients (Codex, Claude Code, or any client with an adapter) - find out the requirements, split the work, write the briefs, get the user's approval of the whole plan, start or continue the sessions, and check the results. Use when the user asks to hand work to another agent or session, or when part of the current work would clearly gain from a separate session (independent parallel pieces, long work, an independent review); then propose it and wait for the user's yes. Also use when the user asks to add support for a new worker client. Do not use for small work you can do yourself.
---

# Agent sessions

You are the orchestrator: you understand what the user wants, hand pieces of work to worker sessions, and check what comes back. Workers run in other agent clients through adapters in `adapters/`. Every adapter follows one [contract](references/contract.md), so the procedure below is the same for every worker.

## Fixed rules

- **Separate sessions, never built-in subagents.** In this selected route, delegated work goes to a separate session started through an adapter. Do not substitute your client's built-in subagent tools (`spawn_agent` or multi-agent tools in Codex, `Task` or `Agent` in Claude Code, and similar). Native subagents may be visible in current clients; visibility alone does not provide the selected adapter lifecycle. A skill cannot disable native tools or override higher-priority client instructions: use [host readiness](references/contract.md#host-readiness) before claiming compatibility. A current explicit user choice of another mechanism is a different route; report it as such within actual permissions.
- Worker-channel language: see [brief-writing, Language](references/brief-writing.md#language); output defaults: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).
- **The user chooses the model.** The user names it directly, or once through a brain profile (the `you-are-brain` skill: Rules, Auto or Ask mode). Without either, never pick a worker's model yourself: ask, listing the options the adapter supports. A standing choice ("use X for everything") holds until the user changes it. Rules mode uses the chosen routing table, Auto delegates model selection, and Ask leaves selection to the user at step 5; an unmatched Rules entry needs an explicit fallback or a question.
- Effort and access: see step 3; launch: see step 5.

## Worker artifacts

Briefs and worker reports are never committed or published unless the user explicitly requests that exception for a specific project. Keep them in local scratch or ignored storage otherwise.

## Workflow

### 1. Find out the requirements

Use [requirements-interview](references/requirements-interview.md) for session-specific additions to the shared task interview.

### 2. Split the work

Decide what you do yourself and what goes to sessions. Delegate only when it pays: independent pieces that can run in parallel, long work, an independent review or a second variant. Do small or tightly coupled work yourself; each session starts cold and costs a brief and a check.

- Scheduling, isolation and continuation: see [running-and-checking, Before starting and Checking a finished session](references/running-and-checking.md#before-starting).
- Choose the worker client: run `node adapters/<agent>.mjs --describe`. It reports where the user can watch the session, whether it can be continued, its effort levels, what each access mode actually enforces, and whether the adapter was checked live (`verified`). Do not promise more than it describes.
- Establish the leading host's readiness under [the contract](references/contract.md#host-readiness), separately from the worker backend. A confirmed conflict blocks this delegation route, not independent authorized work. Missing evidence stays unverified; `verified: true` is historical adapter evidence, not certification of the current host. A client configuration change needs the owner's actual authorization and a fresh host check; installation never implies it.

Available adapters: `codex` (OpenAI Codex, sessions visible in the Codex app; checked live) and `claude-code` (Claude Code headless sessions; **not checked live**). Before relying on `claude-code`, tell the user it is unverified and, with their agreement, run the checks from [writing an adapter](references/writing-an-adapter.md) on a tiny task. For another client, write an adapter first.

### 3. Choose effort and access

Select model and effort deliberately for every turn; adapter API defaults do not make this decision. Effort precedence:
1. The user's explicit request for a level always wins.
2. After failure, raise one supported level only when task difficulty caused the failure. If the brief caused it, repair the brief and keep the effort. Reviewer rounds remain governed by independent-review.
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

Recommend access per session; the user selects it at step 5. Mode meanings, default and refusal: see [adapter contract, Access modes](references/contract.md#access-modes). Codex mapping: see [agent-sessions-codex, step 3](../agent-sessions-codex/SKILL.md#3-choose-effort-and-access).

### 4. Write the briefs

Follow [writing the brief](references/brief-writing.md). Write every brief before step 5. For bundled adapters, prepare the checked [launch assignment](references/contract.md#checked-brief-assignment); it is retained for short corrections without repeating the whole brief. Older commands remain supported but do not claim these additional checks. Storage: see Worker artifacts above.

### 5. Get approval with a summary

Use [AGENTS language defaults]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries). This is the only session-launch approval gate: show one summary with the actual briefs and wait for explicit approval.

```
Task: <one line: what and for whom>
Done when: <two to four observable checks>

| # | Session | Client | Does | Model | Effort and why | Access | Folder | Waits for | Brief |
|---|---------|--------|------|-------|----------------|--------|--------|-----------|-------|
| 1 | <name the user will see> | <worker client> | <one line> | <user's choice> | <level: reason> | <mode> | <path> | - | <brief file> |
| 2 | ... | ... | ... | ... | ... | ... | ... | 1 | ... |

I do meanwhile: <your own part, or "nothing">
How I will check: <per session, the checks you will run yourself>
Approve?
```

A yes covers the sessions in that table with the settings and briefs shown, including normal-worker follow-up turns needed to reach the agreed result; independent reviewer rounds and non-continuation are owned by [independent-review, After the report](../../workflow/independent-review.md#after-the-report). A new session, or a different model, access mode, worker, goal or substantially changed brief, needs a new yes. If the user changes something in the reply, update the table and the briefs, and show what changed.

### 6. Run and check

Use [running-and-checking](references/running-and-checking.md), including Waiting for workers (choose by orchestrator client) and Status updates. Generic execution command: [adapter contract, Run](references/contract.md#run).

### 7. Report to the user

Report format: see [running-and-checking, Reporting](references/running-and-checking.md#reporting).

## Known limits

- Your own access is set by the user in your client. If your sandbox blocks an adapter (exit code 3), tell the user and ask them to approve the command or choose an access mode for you. Do not work around it.
- Codex configuration and hook handling: see [agent-sessions-codex, Known limits](../agent-sessions-codex/SKILL.md#known-limits).
- Git actions: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries); Codex restrictions: see agent-sessions-codex, Known limits.
- Claude Code: the worker needs a CLI that is logged in on its own. The CLI bundled with the desktop app gets its login from the app and fails with "Not logged in" when started separately.
