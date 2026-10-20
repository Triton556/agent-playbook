---
name: jam-board
description: Plan and run project work through Jam Board when the user mentions Jam Board, a jam-board MCP server is connected, or the user asks to work "on the board" / «на доске». Do not use board operations without a connected server; guide connection using references/connect.md from the app's docs/mcp.md. Unrelated task boards use their own workflow.
---

# Jam Board

Jam Board is a local desktop task board (Tauri 2, Rust, SQLite). MCP and desktop share Epic (JB-E1) → Story (JB-S1) → Task (JB-12). In addition to [task-state’s record relationships](../dev-flow/references/task-state.md#long-task-state-and-completeness), the connected board owns current task decisions, briefs, references, questions and acceptance evidence. Worker artifact publication: see [agent-sessions, Worker artifacts](../agent-sessions/SKILL.md#worker-artifacts). Worker language: see [brief-writing, Language](../agent-sessions/references/brief-writing.md#language). Output language: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

If no server is available, stop board mutations and show [connection instructions](references/connect.md); do not claim the board was updated. The mapping targets the app's v2.1 [MCP contract](https://github.com/Triton556/jam-board/blob/main/docs/mcp.md). Read the connected schemas before calls; if they differ, reconcile the contract before the affected mutation. Input fields use **camelCase**, even though database/document field names use snake_case. Arrays replace whole lists; read current values before updating. Tool errors have `isError: true` and structured `code`, `message`, optional `field`; resolve the cause without bypassing a denial.

## Decide the role per epic/task

- **Brain:** the user appoints you in chat, or the epic already names your MCP member as brain. Verify with `get_epic`; `become_brain` claims an unappointed slot only after that authorization. An existing brain/human uses `set_brain` to hand over. A chat appointment does not overwrite another brain automatically. Plan, review and talk to the user.
- **Worker:** implement a Ready task and report evidence. Claiming a task does not appoint a brain.
- You may be brain on one epic and worker on another. **Never review your own task**, including after becoming brain; request a human or another authorized brain. A board role grants no new shell, network, spending or delegation permissions.

## Brain procedure

Follow [WORKFLOW](../../workflow/WORKFLOW.md) and [dev-plan](../dev-plan/SKILL.md) through the board. Read [brain-loop](references/brain-loop.md) for call shapes and a worked two-task example; use [field-guide](references/field-guide.md) while drafting.

1. Recover context with `get_project`, `get_board`, `list_epics`, then `get_epic` for the selected epic. Read `list_changes_since` from the saved cursor; on first use start at `0`. Store the last processed event `seq` in an explicitly labeled operational-notes block in the epic's `decidedMd` (there is no separate notes field), never in personal memory. Preserve decisions, and advance only after processing the events. Use the project-wide feed to include pre-epic questions and human project edits.
2. **Use ask_user for the shared interview** under [task brief and acceptance, section 3](../dev-flow/references/task-brief-and-acceptance.md#3-ask-only-what-changes-the-work). Map each material question to one call with options/recommendedIndex and shared roundLabel. Scope to epic or project before it exists. Recover decidedMd and list_questions. Use wait_for_answer with timeoutSeconds: 60; unanswered handling follows that owner.
3. Write playback to goalMd, doneWhenMd, notIncludedMd, decidedMd and openQuestionsMd under task brief and acceptance, section 4. Participation/reviewer fields map section 5. Store model choice in workerModel under [agent-sessions, Fixed rules](../agent-sessions/SKILL.md#fixed-rules). Launch gate: see agent-sessions, step 5.
4. set_epic_status draft → active after goal/done-when and resolved material decisions. Action scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).
5. `create_story` / `update_story`: one user-visible outcome per story. Fill outcome, basis, preserve, scale, rejection risks, open decisions, and `acceptance` with a nonempty `check` for every criterion. `set_story_status` to `active` needs outcome plus a mandatory criterion. Preserve human checkpoints before dependent expensive work.
6. Map [brief-writing, Template](../agent-sessions/references/brief-writing.md#template) to create_task/update_task_brief using [field-guide](references/field-guide.md). Store verbatim quotes in userQuotesMd; attach/link references with add_reference/link_reference and read inherited references. Ready requires check_ready → fix missing codes (goal, where, change, test, result, story_active) → mark_ready plus a usable full brief. Only a human/appointed brain may override with a real recorded reason; never hide an unresolved choice. Brief edits invalidate an override.
7. Use `set_status` at every step change, scoped to the current epic/story/task: short concrete text, e.g. `interviewing: round 2` or `writing briefs for JB-S3` (at most 120 characters).
8. For review tasks, get_task reads the current report; invoke the review_task prompt when available. Verification: see [running-and-checking, Checking a finished session](../agent-sessions/references/running-and-checking.md#checking-a-finished-session). Board acceptance is by a human or an appointed brain who did not author/claim the task: review_task tool records accept or changes_requested with concrete commentsMd and exact failedTests names. After accepted tasks, check story criteria and set_story_status. Epic Done requires included stories Done and checkpoints under task brief and acceptance, section 5; then set_epic_status.
9. Poll `list_changes_since` at recovery and before dispatch/review/closure. On a human edit, attachment or answer, re-read the affected epic/story/task and references; refine unclaimed briefs and add an `add_comment` describing changed task requirements (epic/story changes can be recorded in `decidedMd` and relevant task comments). For In progress work, do not silently change the brief: notify the worker in a comment, wait for a report/review, and have the brain revise after review. Keep the change cursor in the operational-notes block.

## Worker procedure

Read [worker-loop](references/worker-loop.md) for call and report examples.

1. `list_tasks` with `status: ["ready"]`, preferring `assignee: "me", changesRequested: true`; then other unassigned Ready tasks. Follow pagination. `ready: true` alone is not a status filter.
2. `get_task`: read the whole brief, story acceptance, epic not-included, references/assets and prior reviews. A flag `Needs info` requires reading the pending question; do not guess the answer.
3. `claim_task`, then `set_status`. Handle a claim conflict by choosing different available work. Do not start implementation before a successful claim.
4. Do the authorized work through [dev-flow](../dev-flow/SKILL.md); record baseline, changed files and actual checks. Stay within task boundaries.
5. A blocking decision uses task-scoped ask_user. Unattended/board handling and return conditions: see [running-and-checking, Questions and blocked workers](../agent-sessions/references/running-and-checking.md#questions-and-blocked-workers); use release_task only when relinquishing ownership. Brief edits stay with the brain.
6. `submit_report` from In progress: changed files; **every test** with name, command, expected, actual and `PASS` / `FAIL` / `NOT_RUN`; deviations; not verified. Submission moves to Review. Preserve failed evidence; a correction uses the next report round.
7. Self-acceptance follows Brain procedure, step 8. Returned work is Ready with changesRequested and retained assignee: claim again and read feedback. Repair/recheck: see [WORKFLOW, Work route](../../workflow/WORKFLOW.md#work-route).

## Separate sessions

Delegate through [agent-sessions, steps 1–6](../agent-sessions/SKILL.md), with Codex client details in agent-sessions-codex. Prepare the local brief from current jam://task/{key}, including hierarchy/assets; re-read it after board changes. Store the model under workerModel (selection: agent-sessions, Fixed rules), and keep run settings outside the brief. Workers use distinct MCP identities and submit_report. Execution metadata placement: see running-and-checking, Before starting.

## Hard boundaries

- No hard deletes. Use archival only within authorized scope; retain reports and review history.
- Never edit a brief while In progress, except by the brain after a review. Prefer revision while returned Ready; comment on conflicts and human edits instead of overwriting them.
- Decision consent and unanswered questions: see task brief and acceptance, section 3.
- Do not invent board decisions, executed tests or acceptance; record actual sources and outcomes.
