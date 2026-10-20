---
name: jam-board
description: Plan and run project work through Jam Board when the user mentions Jam Board, a jam-board MCP server is connected, or the user asks to work "on the board" / «на доске». Do not use board operations without a connected server; guide connection using references/connect.md from the app's docs/mcp.md. Unrelated task boards use their own workflow.
---

# Jam Board

Jam Board is a local desktop task board (Tauri 2, Rust, SQLite). MCP and the desktop share the same data: Epic (`JB-E1`) → Story (`JB-S1`) → Task (`JB-12`). Use the board as the current task basis, including decisions, briefs, references, questions and evidence. Keep worker briefs/reports local; do not commit or publish them. Communicate with the user in their language (Russian for Danil); write worker briefs and reports to the brain in English, preserving user quotations verbatim.

If no server is available, stop board mutations and show [connection instructions](references/connect.md); do not claim the board was updated. The mapping targets the app's v2.1 [MCP contract](https://github.com/Triton556/jam-board/blob/main/docs/mcp.md). Read the connected schemas before calls; if they differ, reconcile the contract before the affected mutation. Input fields use **camelCase**, even though database/document field names use snake_case. Arrays replace whole lists; read current values before updating. Tool errors have `isError: true` and structured `code`, `message`, optional `field`; resolve the cause without bypassing a denial.

## Decide the role per epic/task

- **Brain:** the user appoints you in chat, or the epic already names your MCP member as brain. Verify with `get_epic`; `become_brain` claims an unappointed slot only after that authorization. An existing brain/human uses `set_brain` to hand over. A chat appointment does not overwrite another brain automatically. Plan, review and talk to the user.
- **Worker:** implement a Ready task and report evidence. Claiming a task does not appoint a brain.
- You may be brain on one epic and worker on another. **Never review your own task**, including after becoming brain; request a human or another authorized brain. A board role grants no new shell, network, spending or delegation permissions.

## Brain procedure

Follow [WORKFLOW](../../workflow/WORKFLOW.md) and [dev-plan](../dev-plan/SKILL.md) through the board. Read [brain-loop](references/brain-loop.md) for call shapes and a worked two-task example; use [field-guide](references/field-guide.md) while drafting.

1. Recover context with `get_project`, `get_board`, `list_epics`, then `get_epic` for the selected epic. Read `list_changes_since` from the saved cursor; on first use start at `0`. Store the last processed event `seq` in an explicitly labeled operational-notes block in the epic's `decidedMd` (there is no separate notes field), never in personal memory. Preserve decisions, and advance only after processing the events. Use the project-wide feed to include pre-epic questions and human project edits.
2. **Start the interview with `ask_user`**, following [requirements-interview](../agent-sessions/references/requirements-interview.md): one question per material decision, concrete options with `recommendedIndex`, one shared `roundLabel` per round. Scope to the epic, or project before it exists. Read `decidedMd` and open/answered `list_questions`; never ask again what is settled. Use `wait_for_answer` with `timeoutSeconds: 60`, doing independent work between calls. A timeout or recommendation is not the user's answer; never answer your own questions.
3. Play back the result following [task brief and acceptance](../dev-flow/references/task-brief-and-acceptance.md): `update_epic` writes `goalMd`, `doneWhenMd`, `notIncludedMd`, `decidedMd`, `openQuestionsMd`. Select participation and reviewer separately, exactly as the user chose; record any reviewer scope, stages and round limit in `decidedMd`. **The user chooses the worker model; `workerModel` comes only from their explicit choice, never your default or recommendation.** If unknown, ask and keep it unset; never invent decisions. Confirm the interview playback through `ask_user` before dependent session planning.
4. `set_epic_status` from `draft` to `active` only after goal and done-when are filled and material decisions are resolved. A plan-only request authorizes planning, not implementation or launching workers.
5. `create_story` / `update_story`: one user-visible outcome per story. Fill outcome, basis, preserve, scale, rejection risks, open decisions, and `acceptance` with a nonempty `check` for every criterion. `set_story_status` to `active` needs outcome plus a mandatory criterion. Preserve human checkpoints before dependent expensive work.
6. One task = one worker session's job. Write `create_task` / `update_task_brief` by [brief-writing](../agent-sessions/references/brief-writing.md): numbers instead of adjectives, exact strings, each Change with Now / Cause when known / Required / Where / Follow / Keep; each Test setup → expected; explicit Boundaries and Result format; verbatim user's words in `userQuotesMd` (the user_quotes field). Attach readable assets/notes/URLs with `add_reference`, existing items with `link_reference`; inspect inherited references with `list_references` or `get_task`. **Ready requires `check_ready` → fix every missing code (`goal`, `where`, `change`, `test`, `result`, `story_active`) → `mark_ready`; it also requires a usable full brief, not just passing minimum fields.** Only a human or appointed brain can override with a real recorded reason the user would accept; never use it to hide an unresolved decision. Brief edits invalidate an earlier override.
7. Use `set_status` at every step change, scoped to the current epic/story/task: short concrete text, e.g. `interviewing: round 2` or `writing briefs for JB-S3` (at most 120 characters).
8. For tasks in `review`, read the current-round report with `get_task`, invoke the `review_task` **prompt** if available, and apply [task brief and acceptance §7](../dev-flow/references/task-brief-and-acceptance.md#7-execution-verification-and-completion). Check actual changes, tests and story acceptance against epic scope; reports alone are not proof. Then call the `review_task` **tool** with `accept`, or `changes_requested` and concrete `commentsMd` plus `failedTests` using exact report test names. Repeat after correction until accepted; missing evidence stays unverified. When all story tasks are Done, verify story criteria and call `set_story_status`. Ask the user before epic Done for `each_iteration` or `first_sketch`; `autonomous` still needs current evidence. Use `set_epic_status` only after all included stories are Done. Never fabricate human acceptance.
9. Poll `list_changes_since` at recovery and before dispatch/review/closure. On a human edit, attachment or answer, re-read the affected epic/story/task and references; refine unclaimed briefs and add an `add_comment` describing changed task requirements (epic/story changes can be recorded in `decidedMd` and relevant task comments). For In progress work, do not silently change the brief: notify the worker in a comment, wait for a report/review, and have the brain revise after review. Keep the change cursor in the operational-notes block.

## Worker procedure

Read [worker-loop](references/worker-loop.md) for call and report examples.

1. `list_tasks` with `status: ["ready"]`, preferring `assignee: "me", changesRequested: true`; then other unassigned Ready tasks. Follow pagination. `ready: true` alone is not a status filter.
2. `get_task`: read the whole brief, story acceptance, epic not-included, references/assets and prior reviews. A flag `Needs info` requires reading the pending question; do not guess the answer.
3. `claim_task`, then `set_status`. Handle a claim conflict by choosing different available work. Do not start implementation before a successful claim.
4. Do the authorized work through [dev-flow](../dev-flow/SKILL.md); record baseline, changed files and actual checks. Stay within task boundaries.
5. If a decision blocks work, `ask_user` scoped to the **task**, with options/recommendation. Wait in calls of at most 60 seconds, continue independent work, and use `release_task` only if relinquishing ownership. Never answer for the user or edit the brief yourself.
6. `submit_report` from In progress: changed files; **every test** with name, command, expected, actual and `PASS` / `FAIL` / `NOT_RUN`; deviations; not verified. Submission moves to Review. Preserve failed evidence; a correction uses the next report round.
7. Never mark your own task Done or review it. Wait for the human/brain; returned work is Ready with `changesRequested` and retained assignee. Claim again, read feedback and fix the failed test plus affected regressions.

## Separate sessions

The brain may orchestrate workers using [agent-sessions](../agent-sessions/SKILL.md) or [agent-sessions-codex](../agent-sessions-codex/SKILL.md). Prepare a local worker brief from the current `jam://task/{key}` resource (full hierarchy/context and linked assets) and pass run settings separately. The model is the epic's user-chosen `workerModel`; choose effort by the session skill and explain why. Obtain explicit approval for count, scope, actual briefs, model, access and any separate reviewer before launch; Ready or `reviewer: final` is not launch consent. Use visible sessions, never built-in subagents. Workers connect as distinct MCP identities and report with `submit_report`; the board remains the single source of truth. Re-read the resource before starting/resuming a session if board changes arrived.

## Hard boundaries

- No hard deletes. Use archival only within authorized scope; retain reports and review history.
- Never edit a brief while In progress, except by the brain after a review. Prefer revision while returned Ready; comment on conflicts and human edits instead of overwriting them.
- Never answer your own questions or infer consent from a timeout.
- Never invent user decisions, model choices, executed tests or acceptance. Ask when unknown.
