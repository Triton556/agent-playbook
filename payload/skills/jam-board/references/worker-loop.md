# Worker loop

Use the [entrypoint](../SKILL.md#worker-procedure) and [brief-writing](../../agent-sessions/references/brief-writing.md). The board uses Backlog, Ready, In progress, Review, Done; Changes requested and Needs info are flags. Do not interpret a flag as a column.

The following are MCP tool calls, shown as `name(JSON arguments)`. Names and inputs follow the app's `docs/mcp.md`; returned keys/IDs are illustrative. Check actual responses before the next call.

```text
list_tasks({"status":["ready"],"assignee":"me","changesRequested":true,"limit":50})
list_tasks({"status":["ready"],"assignee":"unassigned","limit":50})
get_task({"key":"JB-12"})
```

Prefer your returned work; do not run the second selection if the first already gives an eligible task. Follow `nextCursor` using `cursor`. Read the current brief, inherited story/epic, references/assets, comments, report rounds and review. Obtain the `jam://task/JB-12` resource for a session brief when needed. Read linked assets with permitted tools; a reference record does not prove the file is accessible. Report a missing file instead of substituting an invented design.

```text
claim_task({"key":"JB-12"})
set_status({"text":"implementing JB-12: title layout","scope":{"type":"task","id":"JB-12"}})
```

Claim must succeed before implementation. On `claim_conflict`, read the current holder and choose another available task. On `not_ready`, ask the brain to repair readiness; never force the task into In progress. Use [dev-flow](../../dev-flow/SKILL.md), retain baseline output, and perform the brief's checks. For the complete fictional menu task in [brain-loop](brain-loop.md), a blocked asset decision could be:

```text
ask_user({"scope":{"type":"task","id":"JB-12"},"title":"Какой вариант логотипа использовать?","bodyMd":"В прикреплённой папке два файла. Выбор меняет title-screen.png; работа над layout может продолжаться.","options":[{"label":"logo-final.png","description":"Совпадает с утверждённым эскизом."},{"label":"logo-alt.png","description":"Меняет согласованный силуэт."}],"recommendedIndex":0,"roundLabel":"JB-12/assets/1","allowFreeText":true})
wait_for_answer({"questionIds":["<returned-question-id>"],"timeoutSeconds":60})
```

Decision consent: see [task brief and acceptance, section 3](../../dev-flow/references/task-brief-and-acceptance.md#3-ask-only-what-changes-the-work). Worker return/wait behavior: see [running-and-checking, Questions and blocked workers](../../agent-sessions/references/running-and-checking.md#questions-and-blocked-workers). Withdrawn questions appear in neither returned array. Re-read `list_questions` or the affected task before assuming a pending decision has disappeared. If ownership must be relinquished, comment with the dependency and call `release_task` (default Backlog); explain that it now needs the brain's readiness decision.

## Example report

These outcomes are **fictional teaching data**, not executed game tests. The first report deliberately fails test `2`. Keep exact test names so review can identify them. Every expected test must appear, including NOT_RUN when unavailable; never turn an unexecuted test into PASS.

```text
set_status({"text":"submitting JB-12: test 2 failed","scope":{"type":"task","id":"JB-12"}})
submit_report({"key":"JB-12","summaryMd":"Created the title scene and layout test. Test 2 fails at 1280x720; awaiting brain review.","changedFiles":["scenes/title.tscn","tests/title_layout.gd"],"tests":[{"name":"1","command":"Baseline: godot --headless --path . --editor --quit; then godot --headless --path . --script tests/title_layout.gd -- --size=1920x1080","expected":"No new import errors versus baseline; layout exit 0; title and all 3 buttons inside viewport.","actual":"Baseline exit 0, saved tmp/title-menu/baseline.log; no new import errors; layout exit 0; title and all 3 buttons inside viewport.","result":"PASS"},{"name":"2","command":"godot --headless --path . --script tests/title_layout.gd -- --size=1280x720","expected":"Exit 0; title and all 3 buttons inside viewport.","actual":"Exit 1; Quit button bottom=744 exceeds 720.","result":"FAIL"},{"name":"3","command":"godot --path . --editor; inspect title scene at 1280x720 and 1920x1080","expected":"Both sizes show title and 3 buttons without clipping; compare with attached sketch.","actual":"No GUI display available in this session; not inspected.","result":"NOT_RUN"}],"deviationsMd":"No runtime menu actions were changed; they belong to JB-13.","notVerifiedMd":"Visual acceptance test 3 is unverified; brain must obtain inspection evidence before acceptance."})
```

Submission moves the task to Review. The brain can return it; the assignee remains. Read `get_task` again, `claim_task` the returned Ready task, follow [WORKFLOW, step 6](../../../workflow/WORKFLOW.md#work-route), then submit a new current-round report. A brain reviewing this task must not be its assignee or report author. The task author never uses the review tool to accept their own work.
