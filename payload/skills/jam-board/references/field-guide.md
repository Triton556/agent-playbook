# Board field guide

Use this while writing the board, together with [brief-writing](../../agent-sessions/references/brief-writing.md#a-weak-brief-and-a-strong-one) and the [intent/acceptance procedure](../../dev-flow/references/task-brief-and-acceptance.md). The guide maps fields; it does not replace either procedure. Examples below use a fictional title/menu feature. Worker briefs are English, exact human quotations retain their language. Interview summaries and user-facing board labels use the user's language.

## Epic

The database uses snake_case; tool inputs are camelCase and returned entity fields are camelCase. Omitted update fields are preserved. Do not clear values just because the current session has not read their source.

| Database field / MCP input | What to write | Strong example | Weak example |
| --- | --- | --- | --- |
| title / title | User-recognizable scope | `Меню и титульный экран` | `Улучшения` |
| color / color | Existing palette token m1..m6, retain human choice | `m2` from current epic | Invent `blue` |
| goal_md / goalMd | Outcome, audience and purpose | `Игрок запускает игру через титульное меню.` | `Сделать UI` |
| done_when_md / doneWhenMd | Observable completion and checks | `3 действия мышью и клавиатурой на 1280×720 и 1920×1080; сравнить с sketch.png.` | `Всё красиво и работает` |
| not_included_md / notIncludedMd | Explicit exclusions and authorization limits | `Без сохранений, нового арта и настоящих настроек; пока только план.` | `Ничего лишнего` |
| decided_md / decidedMd | Actual answers with sources; distinguish operational notes | `q-scope: 3 кнопки; q-model: явно выбрана model-a. Operational notes: Change cursor: 124.` | `Наверное, model-a; всё обсудили` |
| open_questions_md / openQuestionsMd | Unresolved decision, dependency, question ID | `q-focus: восстанавливать фокус после Esc? Блокирует JB-13.` | `Уточнить детали` |
| participation / participation | User's exact selected enum | `first_sketch` with first-sketch checkpoint recorded | Pick `autonomous` to avoid waiting |
| reviewer / reviewer | User's separate none/final/stages choice; consent limits in decidedMd | `final`; decidedMd records one final read-only pass, scope/model/access approved separately | `final` interpreted as permission to launch |
| worker_model / workerModel | Explicit user-selected supported model ID; null if not chosen | Exact ID from answered q-model | Your default model or an invented alias |
| brain_member_id / brain assignment | Verified appointed member; use become_brain/set_brain, not update_epic | `set_brain` with `epicKey` and confirmed `memberHandle` | Set yourself on every epic |
| status / set_epic_status | draft → active after goal/done-when; Done after included children/checkpoints | `active` after confirmed playback | `done` while a story remains incomplete |

There is no standalone epic notes field. Keep a clearly labeled operational-notes block in `decidedMd`, separate from human decisions. Save a processed event sequence there; do not replace the field with only a cursor. A project-wide cursor includes human project edits and pre-epic answers. Store reviewer stage/round limits here too because the reviewer enum does not encode them.

## Story

| Database field / MCP input | What to write | Strong example | Weak example |
| --- | --- | --- | --- |
| epic_id / epicKey on creation | Existing intended parent | `JB-E1`, verified via get_epic | Create an unrelated parent to bypass a gate |
| title / title | One visible outcome | `Вход в игру через титульное меню` | `Frontend work` |
| outcome_md / outcomeMd | User action/result | `Игрок читает название и запускает игру мышью или клавиатурой.` | `Экран готов` |
| basis_md / basisMd | Named user material/decision/reference | `sketch.png, q-playback, themes/menu.tres` | `Как обсуждали` |
| preserve_md / preserveMd | Specific accepted qualities and their check | `Название «Северный свет», порядок 3 кнопок, палитра menu.tres; сравнить с эскизом.` | `Сохранить атмосферу` |
| scale_md / scaleMd | How much may change | `Одна титульная сцена и её действия; игровой процесс не меняем.` | `Можно улучшить всё` |
| rejection_risks_md / rejectionRisksMd | Plausible user objections that checks reject | `Обрезка Quit на 720p; потеря фокуса после Esc; замена авторского эскиза.` | `Могут быть баги` |
| open_decisions_md / openDecisionsMd | Material open choices or explicit none with basis | `Нет: настройки — «Скоро», подтверждено q-playback.` | Blank treated as settled |
| acceptance_json / acceptance | Array of criteria tied to user result | See row details below | A list of file names |
| status / set_story_status | draft/active/done/archived with actual gates | `active` after outcome plus mandatory acceptance; `done` after all tasks and criteria | Activate without acceptance |

Each acceptance object:

| Field | What to write | Strong | Weak |
| --- | --- | --- | --- |
| id | Unique stable ID within story | `A1` | Duplicate `A1` |
| criterion | Observable property grounded in intent | `3 buttons remain inside both 1280x720 and 1920x1080 viewports.` | `Responsive` |
| mandatory | Whether failure prevents completion | `true` for required keyboard navigation | Mark required navigation optional to get a pass |
| check | Action/setup and evidence needed | `JB-12 tests 1–3: two layout commands and side-by-side screenshots against sketch.png.` | `Looks OK` |

## Task brief

Use exact paths, strings and numbers. Each requirement needs a distinguishing check. Notes (`description`) do not substitute for the structured brief. TaskDetail exposes a `brief` object; creation/update inputs are top-level fields.

| Database field / MCP input | What to write | Strong example | Weak example |
| --- | --- | --- | --- |
| story_id / storyKey on creation | Parent story with acceptance/context | `JB-S1`, read before creating | Task without a story |
| title / title | One worker session's bounded job | `Титульная сцена и компоновка` | `Build the game` |
| goal_md / goalMd | For whom and why | `Let the player see the title and choose from 3 menu actions.` | `Implement UI` |
| context_md / contextMd | Existing behavior, decisions, first reads, dependency, baseline instructions | `Read scenes/game.tscn and menu.tres; q-playback fixes 2 sizes; JB-13 waits for accepted JB-12 and sketch approval.` | `See chat` |
| where_md / whereMd | Repository, folder, branch, exact relevant files | `C:/work/title-game; feature/title-menu; scenes/title.tscn, tests/title_layout.gd.` | `Somewhere in frontend` |
| changes_json / changes | One object per concrete change | `Title layout` object with exact labels and bounds | `Make it nicer` |
| tests_json / tests | Array of setup → expected, with baseline and permitted scratch location | `Run layout script at 1280x720 → exit 0, Quit bottom <=720.` | `Test everything` |
| boundaries_md / boundariesMd | Allowed files/tools/actions, forbidden actions and user decisions | `Godot GUI/shell/screenshots allowed; no network, dependencies, image generation, extra sessions, deletes, commits or push; gameplay unchanged.` | `Local only` |
| result_md / resultMd | Report destination, exact evidence schema and final-message format | `submit_report: files, tests 1–3 with command/expected/actual/result, deviations, not verified. Final: JB-12 report submitted; PASS x/3.` | `Tell me when done` |
| user_quotes_md / userQuotesMd | Exact user words with attribution | `The user: «спланируй на доске эпик про меню и титульный экран»` | Rephrased quote with requirements the user never said |

Change object fields:

| Field | What to write | Strong | Weak |
| --- | --- | --- | --- |
| title | Short change identity | `Title layout` | `Fix` |
| now | Observed current behavior and file | `Startup opens scenes/game.tscn; title scene absent.` | `Broken` |
| cause | Verified cause, or explicitly unknown | `JB-12 intentionally omitted action wiring.` | An unsupported diagnosis |
| required | Exact future behavior | `Settings shows «Скоро»; Esc closes it and restores Settings focus.` | `Settings works` |
| where | Change location | `scripts/title_menu.gd` | `In code` |
| follow | Existing pattern/source, or explicit none | `themes/menu.tres and linked sketch.png` | `Best practices` |
| keep | Neighboring behavior/qualities to preserve | `Keep game.tscn gameplay, palette and button order.` | `Keep everything else` |

Test object fields:

| Field | What to write | Strong | Weak |
| --- | --- | --- | --- |
| setup | Numbered reproducible setup/command; record baseline before edits | `2. godot --headless --path . --script tests/title_layout.gd -- --size=1280x720` | `Try a small screen` |
| expected | Concrete result that rejects the failure | `Exit 0; all 3 buttons in viewport; Quit bottom <=720.` | `PASS` |

## Task metadata, evidence and derived fields

| Field / operation | What belongs here | Strong | Weak |
| --- | --- | --- | --- |
| description_md / description input | Free-form Notes, rationale and pointers, not the brief | `Sketch approval is q-sketch; evidence linked to task.` | Put the only test in Notes and leave tests empty |
| status | backlog/ready/in_progress/review/done through workflow tools | `claim_task` after Ready; `submit_report` to Review; human/brain acceptance | Worker marks own task Done |
| priority | low/medium/high/critical, grounded in ordering | `high` because it unblocks agreed demo | Every task `critical` |
| tags | Existing project vocabulary, max 24 characters each | `ui`, `qa` | Personal invented taxonomy on every task |
| estimate | 1/2/3/5/8 or null; agreed project scale | `3` on the project's existing scale | `2.5 days` as invalid enum |
| due_at / dueAt | Agreed RFC3339 UTC date, null clears it | `2026-10-30T00:00:00Z` from user deadline | Guess a deadline |
| idempotency_key / idempotencyKey | Stable per-actor creation retry key | `title-menu/layout/1` reused after uncertain response | New random key on each retry |
| assignee_id / claim_task | MCP caller after successful claim | Task owned by implementing worker identity | Assume claim succeeded without reading response |
| changes_requested / changesRequested | Derived review flag; retained until report | Prefer own returned Ready work | Clear flag to hide failed tests |
| needs_info / needsInfo | Derived from open task/ancestor questions | Read scoped question and wait | Treat as a manually editable status |
| review_round / reviewRound | Server-managed report/review round | Read current report round after return | Overwrite past report to hide failure |
| reports / submit_report | summaryMd, changedFiles, unique named tests with command/expected/actual/result; deviationsMd, notVerifiedMd | `2: expected exit 0; actual exit 1, bottom=744; FAIL` | Claim PASS from an unrun check |
| reviews / review_task | verdict, commentsMd, failedTests using report names | `changes_requested`, `failedTests:["2"]`, exact defect and recheck | `Bad, try harder` |
| comments / add_comment | Specific task updates and coordination | `Human supplied a new sketch; brief waits until review before revision.` | Silent brief rewrite during In progress |
| references/assets | add_reference/link_reference records; caption, tags, inherited target links | Absolute readable sketch path with source caption and JB-S1 link | A filename nobody can access |

Epic/Story/Task `id`, `key`, `jamId`, parent IDs, `position`, audit fields (`createdBy`, `updatedBy`, `createdAt`, `updatedAt`, `archivedAt`) and returned hierarchy/journal/history are server-managed context, not invented input. A strong use is to retain returned `JB-12`, inspect latest history, use documented status/order tools, and preserve audit history. A weak use is guessing keys, treating an opaque updatedAt as a timestamp to edit, or deleting history. Task summaries also derive epic key/color and story IDs; do not patch these as independent fields. Archived records remain archived unless an authorized human restores them through planning status commands. Never hard-delete data.
