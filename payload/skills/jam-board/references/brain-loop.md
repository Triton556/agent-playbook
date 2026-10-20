# Brain loop and worked example

Use [requirements-interview](../../agent-sessions/references/requirements-interview.md), [task brief and acceptance](../../dev-flow/references/task-brief-and-acceptance.md), [dev-plan](../../dev-plan/SKILL.md) and [brief-writing](../../agent-sessions/references/brief-writing.md) for their procedures; this file maps those procedures to board operations. [Field guide](field-guide.md) explains field content; [worker-loop](worker-loop.md) shows evidence submission.

## Recover, interview, plan, dispatch, review, react

1. Read project/board/epics, then the relevant epic tree. Verify your appointment and active project before writes. When no epic exists, create a draft from the user's stated goal; do not invent completion criteria or decisions.
2. Read the project change feed from the operational cursor in `decidedMd`. Read relevant questions and referenced materials. Separate user edits from your own status/checkpoint events using event actor and payload; `list_members` resolves identities if needed. For every affected task, re-read `get_task`. Comments attach to tasks; do not pass epic/story keys to `add_comment`.
3. Ask only unresolved material decisions, one `ask_user` per decision, sharing the round label. Ask participation, reviewer and worker-model choices separately. A recommendation is advisory; do not infer answers from silence. Wait at most 60 seconds per call and do independent work between waits. Record actual human answers, with question IDs, in the epic. Reuse decisions across recovery.
4. Write the playback into epic fields and ask for confirmation. Store reviewer launch limits and session approvals in `decidedMd`; do not mistake an enum for consent. Activate after the required fields/answers exist. Make stories with checkable acceptance and full one-session task briefs. Attach assets and check readiness; a technical readiness pass does not settle product questions or authorize execution.
5. Before dispatch, read new events and regenerate the session brief from the task resource if changed. Follow [agent-sessions](../../agent-sessions/SKILL.md) or [agent-sessions-codex](../../agent-sessions-codex/SKILL.md) for session settings and approval. Do not launch during a plan-only request. One worker per task, separate identities, no overlapping file ownership. Record dependencies in task Context; the brain withholds Ready for dependent work until its prerequisite is accepted.
6. Before review, read the latest task/report and story criteria; use the `review_task` prompt, compare actual artifacts and rerun sufficient checks by acceptance §7. Only the human/appointed brain can accept; never review your own task. A missing critical check prevents acceptance. Return precise failures using report test names, read the repaired version, then accept when supported. Stored optional reviewer choices do not remove ordinary author checks or the board's human/brain acceptance gate.
7. Close a story only after all its tasks and criteria are complete. Honor human checkpoints throughout. Ask before epic Done in `each_iteration`/`first_sketch`. Preserve failures and limitations. Reconcile human changes before closing, then advance the cursor only through processed events.

There is no dedicated epic notes property. Keep a labeled block such as `<!-- jam-board operational notes -->\nChange cursor: 124` in `decidedMd`, preserving the actual decisions. Read/merge the current field before writing to reduce lost updates, then re-read when concurrent changes are possible. Use the last processed `seq`, not a timestamp or guessed next value. The `list_changes_since` result is an array, not `{nextCursor}`. Its project-wide form covers human project edits and pre-epic answers; `epicKey` is an optional filter when deliberately reading only that tail. Cursor writes generate another event; process these normally without writing a new checkpoint just to acknowledge your own checkpoint. Keep the cursor out of personal memory and session settings.

## Worked example: title screen and menu

Danil says in chat: **«спланируй на доске эпик про меню и титульный экран»** and appoints this session as brain. This is a **fictional example**: IDs, repository facts, assets, answers, commands and outcomes below are teaching data. Discover the real project facts first. No calls below have been executed against Danil's board. Tool invocations use `name(JSON arguments)`; capture returned keys/IDs rather than assuming sequence numbers.

### Recovery and draft

```text
get_project({})
get_board({})
list_epics({})
list_changes_since({"cursor":0})
```

Assume inspection finds an empty Godot game project at `C:/work/title-game`, branch `feature/title-menu`, `scenes/game.tscn` and an accepted theme `themes/menu.tres`. There is no existing relevant epic. Capture the request without expanding scope:

```text
create_epic({"title":"Меню и титульный экран","goalMd":"Спланировать вход игрока в игру через титульный экран и меню.","notIncludedMd":"Реализация и запуск исполнителей пока не разрешены."})
become_brain({"epicKey":"JB-E1"})
get_epic({"key":"JB-E1"})
set_status({"text":"interviewing: round 1","scope":{"type":"epic","id":"JB-E1"}})
list_questions({"scope":{"type":"epic","id":"JB-E1"}})
```

### One interview round, five separate decisions

Recommendations address scope and process; the worker-model options must come from the actual client's supported choices. Here the fictional user previously named `model-a` and `model-b` as available; they are placeholders, never real default models.

```text
ask_user({"scope":{"type":"epic","id":"JB-E1"},"title":"Какие действия нужны в первом меню?","bodyMd":"Предлагаю один экран и три действия; это ограничивает первую проверяемую версию.","options":[{"label":"Начать / Настройки / Выйти","description":"Настройки пока показывают согласованную заглушку."},{"label":"Ещё и Продолжить","description":"Потребуется загрузка сохранения и отдельная стори."}],"recommendedIndex":0,"roundLabel":"JB-E1/round-1"})
ask_user({"scope":{"type":"epic","id":"JB-E1"},"title":"Какой результат считать готовым?","options":[{"label":"1280×720 и 1920×1080, мышь и клавиатура","description":"Две проверки размеров плюс полный маршрут действий."},{"label":"Только 1920×1080 и мышь","description":"Клавиатура и меньший экран остаются за пределами."}],"recommendedIndex":0,"roundLabel":"JB-E1/round-1"})
ask_user({"scope":{"type":"epic","id":"JB-E1"},"title":"Как вы хотите участвовать?","options":[{"label":"Первый связный эскиз","description":"Сверяем направление до дорогой реализации; далее автономно, эпик закрываем с вами."},{"label":"Каждая значимая итерация","description":"Больше промежуточных проверок с вашим участием."},{"label":"Автономно","description":"Агент выполняет согласованный объём со своими проверками."}],"recommendedIndex":0,"roundLabel":"JB-E1/round-1"})
ask_user({"scope":{"type":"epic","id":"JB-E1"},"title":"Нужен ли отдельный ревьюер?","options":[{"label":"Нет","description":"Авторские проверки и приёмка мозгом сохраняются; дополнительной сессии нет."},{"label":"Один финальный проход","description":"Дополнительные затраты; объём, модель и лимит раундов согласуем до запуска."},{"label":"На выбранных этапах","description":"Нужно отдельно определить этапы и лимит раундов."}],"recommendedIndex":0,"roundLabel":"JB-E1/round-1"})
ask_user({"scope":{"type":"epic","id":"JB-E1"},"title":"Какую модель использовать для исполнителей?","bodyMd":"Вы ранее назвали доступные model-a и model-b. Рекомендую явно выбрать из них; я не назначаю модель за вас.","options":[{"label":"model-a","description":"Первый из названных вами вариантов."},{"label":"model-b","description":"Второй из названных вами вариантов."}],"recommendedIndex":0,"roundLabel":"JB-E1/round-1","allowFreeText":true})
wait_for_answer({"questionIds":["q-scope","q-done","q-participation","q-reviewer","q-model"],"timeoutSeconds":60})
```

Replace the five symbolic IDs with those returned by the calls. Between waits inspect existing scenes/theme and the supplied sketch; do not start the unresolved menu implementation. The hypothetical human chooses each first option, explicitly **model-a**. If only some answers arrive, wait for the remaining IDs; verify withdrawn/missing questions through `list_questions`. Do not treat a timeout as accepting a recommendation.

### Playback and activation

```text
update_epic({"key":"JB-E1","goalMd":"Игрок видит титульный экран и запускает игру из меню.","doneWhenMd":"На 1280×720 и 1920×1080 видны название и три кнопки. Мышь и клавиатура запускают игру, открывают заглушку настроек и завершают приложение. Согласованный эскиз сохранён.","notIncludedMd":"Продолжение сохранения, настоящий экран настроек, геймплей и новые аудио/арт-ассеты. Текущий запрос — план; реализация требует отдельного поручения.","decidedMd":"Ответы q-scope/q-done/q-participation/q-reviewer/q-model: Начать / Настройки / Выйти; 2 размера; мышь+клавиатура; first_sketch; reviewer none; явно выбрана model-a. Основа: пользовательский sketch.png, themes/menu.tres. На эскизе проверяем компоновку до действий меню.\n<!-- jam-board operational notes -->\nChange cursor: 0","openQuestionsMd":"Ожидается подтверждение playback.","participation":"first_sketch","reviewer":"none","workerModel":"model-a"})
ask_user({"scope":{"type":"epic","id":"JB-E1"},"title":"Верно ли резюме плана?","bodyMd":"Титульный экран и 3 действия; 2 размера; мышь и клавиатура; сохраняем ваш sketch.png и тему. Сохранения, настоящие настройки и новый арт не входят. Сейчас готовлю только план. Модель исполнителей — выбранная вами model-a.","options":[{"label":"Да","description":"Можно детализировать стори и брифы."},{"label":"Нужны поправки","description":"Уточните их текстом."}],"recommendedIndex":0,"roundLabel":"JB-E1/playback"})
wait_for_answer({"questionIds":["q-playback"],"timeoutSeconds":60})
```

Only after the hypothetical human confirms:

```text
update_epic({"key":"JB-E1","openQuestionsMd":"Нет открытых решений; реализация ещё не поручена."})
set_epic_status({"key":"JB-E1","status":"active"})
set_status({"text":"writing briefs for JB-S1","scope":{"type":"epic","id":"JB-E1"}})
create_story({"epicKey":"JB-E1","title":"Вход в игру через титульное меню","outcomeMd":"Игрок читает название и выбирает одно из трёх действий мышью или клавиатурой.","basisMd":"Пользовательский sketch.png; подтверждённый playback q-playback; themes/menu.tres.","preserveMd":"Название «Северный свет», порядок Начать / Настройки / Выйти, палитра текущей темы.","scaleMd":"Одна титульная сцена и её действия; игровой процесс не меняем.","rejectionRisksMd":"Кнопка обрезана на 720p; клавиатура теряет фокус; меню заменяет авторский эскиз.","openDecisionsMd":"Нет; настройки — заглушка «Скоро».","acceptance":[{"id":"A1","criterion":"Название и 3 кнопки внутри viewport на двух размерах; соответствуют sketch.png.","mandatory":true,"check":"JB-12 tests 1–3: layout asserts at 1280x720/1920x1080 plus direct visual comparison."},{"id":"A2","criterion":"Все три действия доступны мышью и клавиатурой; Esc закрывает заглушку.","mandatory":true,"check":"JB-13 tests 1–3: menu action assertions and interactive keyboard/mouse walkthrough."}]})
```

### Two complete task briefs

Task inputs are top-level camelCase brief fields, not a nested `brief`. These example boundaries explicitly permit the checks they require. Assets already exist and are readable at the fictional path. Exact user quote is preserved; the agreed details remain attributed to the playback rather than fabricated quotes.

```text
create_task({"storyKey":"JB-S1","title":"Титульная сцена и компоновка","idempotencyKey":"title-menu/layout/1","goalMd":"1. Show the player the title and 3 menu buttons, matching the user's sketch.\n2. User-facing text is Russian.","contextMd":"1. Read AGENTS.md, scenes/game.tscn, themes/menu.tres and inherited sketch reference.\n2. Confirmed q-playback: 1280x720 and 1920x1080, first_sketch checkpoint before menu actions.\n3. No title scene exists; Godot is installed. Record command outputs before editing.\n4. Brain owns knowledge capture; worker only checkpoints if required by its hooks.","whereMd":"C:/work/title-game; branch feature/title-menu; scenes/title.tscn and tests/title_layout.gd. Use the project's installed Godot executable as godot.","changes":[{"title":"Title layout","now":"Startup opens scenes/game.tscn; no title scene exists.","cause":"Title entry flow has not been implemented.","required":"Create scenes/title.tscn with title «Северный свет» and buttons «Начать», «Настройки», «Выйти» in that order; all visible at 1280x720 and 1920x1080. No action wiring in this task.","where":"scenes/title.tscn; tests/title_layout.gd","follow":"themes/menu.tres and the attached sketch.png.","keep":"scenes/game.tscn gameplay, existing palette and exact Russian labels."}],"tests":[{"setup":"1. Before editing: run godot --headless --path . --editor --quit; save baseline output to ignored tmp/title-menu/. After editing run godot --headless --path . --script tests/title_layout.gd -- --size=1920x1080.","expected":"Baseline has no new import errors; layout command exits 0 and asserts title and all 3 buttons are inside the viewport."},{"setup":"2. Run godot --headless --path . --script tests/title_layout.gd -- --size=1280x720.","expected":"Exit 0; title and all 3 buttons inside viewport; Quit bottom <=720."},{"setup":"3. Open scenes/title.tscn with godot --path . --editor; inspect at both sizes beside sketch.png, capture screenshots in ignored tmp/title-menu/.","expected":"Title and 3 buttons have no clipping; order and palette match sketch/theme. Brain presents this coherent sketch to the user before dependent work."}],"boundariesMd":"1. Change only scenes/title.tscn and tests/title_layout.gd.\n2. File reading, shell Godot checks, GUI editor and screenshot capture are allowed. Creating ignored tmp/title-menu/ evidence is allowed. Stop owned Godot processes.\n3. No network, package installs, image generation, extra worker sessions, deleting files, commits, push or publication.\n4. Keep the sketch/theme and gameplay unchanged. Do not wire actions or change project.godot. Ask the brain if a path or command differs.","resultMd":"Submit through submit_report in English: changed files; summary per change; tests named 1, 2, 3 with command, expected, actual, PASS/FAIL/NOT_RUN; deviations; not verified. Store screenshots/baseline under ignored tmp/title-menu/ and attach readable evidence. Final message: JB-12 report submitted; PASS x/3. Do not commit reports.","userQuotesMd":"Danil: «спланируй на доске эпик про меню и титульный экран»"})
create_task({"storyKey":"JB-S1","title":"Действия меню мышью и клавиатурой","idempotencyKey":"title-menu/actions/1","goalMd":"1. Let the player start the game, open the settings placeholder and quit from the accepted title screen.\n2. User-facing text is Russian.","contextMd":"1. Read AGENTS.md, scenes/title.tscn, scenes/game.tscn and project.godot after JB-12 is accepted.\n2. Dependency: JB-12 Done plus the user's first-sketch approval. Keep this task Backlog until both exist.\n3. Confirmed q-playback: settings is only the placeholder «Скоро»; no save loading.\n4. Brain owns knowledge capture; worker only checkpoints if a hook requires it.","whereMd":"C:/work/title-game; branch feature/title-menu; scripts/title_menu.gd, project.godot, tests/menu_actions.gd. Do not edit scenes/title.tscn; attach actions through the startup script.","changes":[{"title":"Menu routing and focus","now":"Accepted scenes/title.tscn has 3 inert buttons; startup still opens game.tscn.","cause":"JB-12 intentionally implements layout only.","required":"Set startup to scenes/title.tscn. «Начать» opens scenes/game.tscn; «Настройки» shows «Скоро», Esc closes it and restores focus to «Настройки»; «Выйти» quits with exit 0. Initial focus is «Начать»; Tab cycles all 3 buttons and Enter activates. Mouse click activates each action.","where":"scripts/title_menu.gd, project.godot; tests/menu_actions.gd","follow":"Existing scenes/game.tscn startup convention and Godot Control focus handling.","keep":"Accepted title layout, theme, button labels/order and game scene behaviour."}],"tests":[{"setup":"1. Before editing run godot --headless --path . --editor --quit and save baseline under ignored tmp/title-menu/. Add tests/menu_actions.gd, then run godot --headless --path . --script tests/menu_actions.gd -- --case=start.","expected":"No new import errors versus baseline; command exits 0; startup is title.tscn and Start changes to game.tscn exactly once."},{"setup":"2. Run godot --headless --path . --script tests/menu_actions.gd -- --case=settings-focus.","expected":"Exit 0; initial focus Start; Tab cycles Start/Settings/Quit; Settings shows «Скоро»; Esc closes it and restores Settings focus."},{"setup":"3. Run godot --path . at 1280x720 and 1920x1080; exercise each action by mouse and keyboard in fresh runs, capture evidence in ignored tmp/title-menu/.","expected":"At both sizes Start opens game, Settings/Esc round-trip restores focus, Quit exits 0; title/buttons remain unclipped. Record all 6 action/input combinations per size."}],"boundariesMd":"1. Change only scripts/title_menu.gd, project.godot, tests/menu_actions.gd. Read the accepted layout but do not edit it.\n2. Shell checks, GUI game runs, screenshots and ignored tmp/title-menu/ evidence are allowed; stop owned processes.\n3. No network, new dependencies, image generation, extra sessions, file deletion, commits, push or publication. No gameplay, audio or saved-game changes.\n4. If attaching the script requires an out-of-scope layout edit, ask before proceeding; never silently widen the task.","resultMd":"Submit through submit_report in English: changed files; summary; tests named 1, 2, 3 with command, expected, actual, PASS/FAIL/NOT_RUN; deviations and not verified. Include screenshot paths and baseline location. Final message: JB-13 report submitted; PASS x/3. Reports remain local.","userQuotesMd":"Danil: «спланируй на доске эпик про меню и титульный экран»"})
add_reference({"kind":"asset","filePath":"C:/work/title-game/reference/sketch.png","title":"User's title sketch","caption":"Confirmed layout basis; preserve title and button order.","frameEpicKey":"JB-E1","linkTo":"JB-S1"})
link_reference({"itemId":"<returned-reference-id>","targetKey":"JB-12"})
```

An asset reference does not copy the file. Ensure workers have authorized read access to that path. Story-linked items are inherited by both tasks; the explicit task link demonstrates reuse. Notes use `add_reference` kind `note` with `text`, URLs kind `link` with `url`; stored URLs do not imply a fetch or permission to fetch.

### A Ready failure and its fix

```text
check_ready({"key":"JB-12"})
```

Illustrative response: `{"ready":false,"missing":[{"code":"story_active","message":"The story is still draft"}]}`. The task is complete, but its parent is draft. Fix the parent rather than override the gate:

```text
set_story_status({"key":"JB-S1","status":"active"})
check_ready({"key":"JB-12"})
mark_ready({"key":"JB-12"})
add_comment({"key":"JB-13","body":"Dependency: keep Backlog until JB-12 is accepted and the user approves the first coherent sketch. No worker launch is authorized by this plan."})
set_status({"text":"plan ready: JB-12 Ready, JB-13 awaits sketch","scope":{"type":"epic","id":"JB-E1"}})
```

The second check returns `ready:true`. This ends the original plan-only request. No sessions start. A later **explicit** implementation request and approved session plan are required for the following hypothetical execution/review. The chosen model is read from `get_epic().epic.workerModel`, passed to the session adapter with separately approved access and effort. The worker receives current `jam://task/JB-12` content, claims the task and submits the first report from [worker-loop](worker-loop.md).

### Review: return failed test 2, accept repaired round

```text
set_status({"text":"reviewing JB-12: round 0","scope":{"type":"task","id":"JB-12"}})
get_task({"key":"JB-12"})
get_epic({"key":"JB-E1"})
review_task({"key":"JB-12","verdict":"changes_requested","commentsMd":"Test 2: Quit bottom=744 at 1280x720, expected <=720. Correct anchors/spacing without changing labels/order/theme. Rerun tests 1–2 and obtain the missing visual comparison for test 3; mandatory A1 cannot be accepted with NOT_RUN.","failedTests":["2","3"]})
```

Now Ready, `changesRequested:true`, `reviewRound:1`, assignee retained. The worker re-reads, claims and repairs. If the brief needs correction, the brain may use `update_task_brief` now after review, preserving history and explaining the change in a comment; do not rewrite it while the worker is implementing.

The following calls belong to the **worker identity**, not the reviewing brain. These are fictional outcomes; in real work execute and inspect before reporting.

```text
get_task({"key":"JB-12"})
claim_task({"key":"JB-12"})
set_status({"text":"fixing JB-12: 720p anchors","scope":{"type":"task","id":"JB-12"}})
submit_report({"key":"JB-12","summaryMd":"Adjusted vertical anchors; obtained both-size visual evidence.","changedFiles":["scenes/title.tscn","tests/title_layout.gd"],"tests":[{"name":"1","command":"godot --headless --path . --script tests/title_layout.gd -- --size=1920x1080","expected":"Exit 0; title and 3 buttons inside viewport.","actual":"Exit 0; all inside viewport.","result":"PASS"},{"name":"2","command":"godot --headless --path . --script tests/title_layout.gd -- --size=1280x720","expected":"Exit 0; Quit bottom <=720.","actual":"Exit 0; Quit bottom=680.","result":"PASS"},{"name":"3","command":"godot --path . --editor; inspect title at 1280x720 and 1920x1080 beside sketch.png","expected":"No clipping; order/palette match basis at both sizes.","actual":"Inspected both sizes; screenshots tmp/title-menu/720.png and 1080.png match order/palette and show 3 unclipped buttons.","result":"PASS"}],"deviationsMd":"None.","notVerifiedMd":"Menu actions belong to JB-13 and were not implemented in this task."})
```

Back as the **brain**, inspect the real diff and screenshots, rerun tests 1–2 and compare A1 with the basis; never accept just because the fictional report says PASS:

```text
get_task({"key":"JB-12"})
review_task({"key":"JB-12","verdict":"accept","commentsMd":"Round 1: reran layout tests 1–2; inspected both screenshots against sketch.png and theme. Quit bottom=680 at 720p. A1 evidence complete; actions remain JB-13.","failedTests":[]})
ask_user({"scope":{"type":"epic","id":"JB-E1"},"title":"Первый эскиз: продолжаем с этой компоновкой?","bodyMd":"Покажите приложенные 720p/1080p снимки рядом с вашим эскизом. Все 3 кнопки видны; действия ещё не подключены.","options":[{"label":"Да","description":"Можно выполнять JB-13 в уже согласованном объёме."},{"label":"Нужны изменения","description":"Опишите их до следующего шага."}],"recommendedIndex":0,"roundLabel":"JB-E1/first-sketch"})
wait_for_answer({"questionIds":["q-sketch"],"timeoutSeconds":60})
```

Attach screenshot files with `add_reference` as in the earlier asset call before asking the user to inspect them. After the real human approves, record that answer in `decidedMd`, re-read incoming edits, check and mark JB-13 Ready, and resume only within the approved session plan. After JB-13's distinct worker report is verified and accepted, finish as follows:

```text
get_epic({"key":"JB-E1"})
set_story_status({"key":"JB-S1","status":"done"})
ask_user({"scope":{"type":"epic","id":"JB-E1"},"title":"Закрыть эпик меню?","bodyMd":"Обе задачи приняты; A1 и A2 проверены. Реальные настройки и сохранения остаются вне объёма.","options":[{"label":"Закрыть","description":"Результат соответствует согласованному объёму."},{"label":"Есть замечания","description":"Уточним замечания до закрытия."}],"recommendedIndex":0,"roundLabel":"JB-E1/closure"})
wait_for_answer({"questionIds":["q-close"],"timeoutSeconds":60})
```

Only after the human agrees, re-read new events and affected records, record the decision and call `set_epic_status` with `status:"done"`. A new goal becomes a separately agreed scope; keep prior evidence rather than replacing failed rounds.

### React to human edits and save progress

Suppose the saved cursor is 124:

```text
list_changes_since({"cursor":124})
get_task({"key":"JB-13"})
list_references({"taskKey":"JB-13"})
```

If a human added a new sketch or answered a question, read that item and the current epic/story. For an unclaimed Backlog/Ready task refine only affected brief fields with `update_task_brief`, preserving entire arrays; run `check_ready` again before `mark_ready`. Record the change with `add_comment`, e.g. `Human replaced the menu sketch; updated the Settings focus check to match the confirmed answer q-focus. Labels and gameplay scope retained.` If it changes agreed scope, ask first. While In progress, comment and coordinate; wait until review before a brain brief revision. Then read/merge the latest `decidedMd` and save `Change cursor: <last-processed-seq>` through `update_epic`. Do not use memory as the change cursor store.
