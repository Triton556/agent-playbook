# Writing the brief

The brief is the worker's whole view of the task. The worker does not see your conversation with the user, your notes or your reasoning: only the brief, the files and its own instructions. A vague or unstructured brief makes the worker either take liberties or stall. Write it so that a capable engineer who has never heard of the project could do the work and prove it is done.

## Language

- Write the brief in English, whatever language the user speaks.
- Use English for all agent-to-agent communication: briefs and follow-ups, commentary, progress updates, questions, final responses and written reports. Choose the language by the intended recipient, not by who can view the session.
- In a delegated worker session, the recipient is the orchestrator unless the current user instruction explicitly addresses a particular output directly to the user. A session visible to the user does not make a worker-to-orchestrator message user-facing.
- Include an explicit Audience and language block in every initial brief. State the recipient and the language of each user-facing deliverable. On continuation, retain that assignment unless the current user instruction changes it; restate any change explicitly.
- Preserve exact source quotations, identifiers, paths, commands and required product text in their original language. Mark quotations as quotations. Write interface text, documents and other user-facing deliverables in the language specified for that output; their language does not change the surrounding message or report to the orchestrator.
- Direct conversation with the user and knowledge-base prose follow [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries), including the user's explicit language exceptions. A report to another agent is agent-to-agent communication.

## Form

- Headings and numbered lists, not paragraphs. One fact or requirement per item; a paragraph longer than three lines should become a list.
- Numbers instead of adjectives: "200 000 characters", "returns 413", "under 2 seconds", not "large", "fails", "fast".
- Exact strings in quotes: messages, labels, error codes, file names, commands.
- Each requirement has at least one test that shows it is met.

Detail goes into what must be true and how it will be checked. It does not go into step-by-step instructions for writing the code: the worker has its own workflow, and prescribing every step lowers the quality. Name a specific approach only when the user decided it, or when the project already has a pattern the change must follow.

Independent reviewer briefs: [independent-review, Preparation](../../../workflow/independent-review.md#preparation) owns information staging and overrides the generic cause/baseline fields below.

## Template

```markdown
# Task: <one line: what should exist or change>

## Audience and language
- You are a delegated worker addressing the agent orchestrator. Use English for commentary, progress updates, questions, the final response and the written report, even when the user can view the session.
- User-facing deliverables: <name each deliverable and its required language, or "none">. Preserve exact quotations, identifiers and required product text.

## Goal
What the result is for and who uses it. Quote the user where wording matters.

## Context
- What exists now and what was already decided, with reasons.
- What to read first.

## Where
Repository or folder, branch, key files.

## Changes
### 1. <short name of the first change or problem>
- Now: current behaviour, with file names.
- Cause: if known.
- Required: the exact behaviour after the change, with exact texts and values.
- Where: the file, module or layer to change.
- Follow: an existing place in the code that already does it this way, if any.
- Keep: similar cases that must keep their current behaviour.

### 2. <next change>
...

## Tests: run all of them and record each result
- Before changing anything, record the baseline (test results, build or type-check diagnostics) to compare against.
- Where scratch scripts and fixtures go. Secrets and keys are never printed.
1. <setup or command> → <expected result with concrete values>.
2. ...
- Stop every process you started, except those listed in the report.

## Boundaries
- Do not touch: ...
- Not permitted: pushing, publishing, deleting, network calls, new dependencies (keep the ones that apply).
- Test-only shortcuts: what is allowed in tests, and what must never be bypassed in normal operation.
- Leave to the user: decisions the worker must not make; stop and report, or take a stated default.

## Result
- Report: where to write it (a file path, or the final message) and what it contains:
  changed files; what was done per change; each test with command, expected, actual, PASS/FAIL;
  deviations from the brief, with reasons; what was not verified.
- Final message: <exact format, for example "the report path and the line 'PASS x/N'">.
```

Leave out a section only when it truly has nothing to say. A short task gets a short brief; the template sets the order, not the length.

## Rules

- **Self-contained.** No "as discussed", "the usual way" or "the file from before". Name the file and quote the decision.
- **Concrete paths and names.** Exact folders, files, functions, commands, branches.
- **Similar cases named.** If a change could be confused with a neighbouring case (another error with the same code, another screen with the same component), say which one must stay as it is.
- **Baseline first.** For anything that compares before and after, the worker records the baseline before editing.
- **Boundaries that cannot be misread.** Name each tool and action the task may need and say whether it is allowed: image generation, network access, package installs, browser, running servers, deleting files. Avoid umbrella words such as "local only" or "no external services": a worker may read them as forbidding a tool the task needs, or as allowing one it must not use.
- **One task per brief.** Independent pieces go to separate sessions.
- **Nothing private that is not needed.** No secrets, tokens, personal data or unrelated history. Tell the worker never to print keys it uses.
- **Memory.** Specify the writer assignment required by [kb-save, Delegated work](../../kb-save/SKILL.md#delegated-work).
- **Run settings are not in the brief.** Model, effort and access mode are passed to the adapter.

## Example 1: mechanical work

Effort `medium`, access `workspace-write`.

```markdown
# Task: Rename three modules to the approved names

## Goal
The user approved clearer module names. Apply them everywhere without changing behaviour.

## Context
- The mapping below is final; do not change it.
- Old names keep working for one release as import aliases.
- The CHANGELOG history keeps old names as they are.

## Where
This repository, branch `main`. Modules are in `src/modules/`.

## Changes
### 1. Rename
- Required: rename the folders and the `name` field in each `module.json`:
  `alpha-old` → `alpha`, `beta-old` → `beta`, `gamma-old` → `gamma`.
### 2. References
- Required: update every reference to the old names: code, configuration, tests, documentation.
### 3. Aliases
- Required: importing an old name loads the new module and logs "renamed to <new name>".
- Follow: the existing alias for `delta` in `src/modules/aliases.ts`.

## Tests: run all of them and record each result
1. `npm test` → passes.
2. `npm run build` → passes.
3. A search for `alpha-old`, `beta-old`, `gamma-old` → found only in CHANGELOG history and the alias table and its tests.
4. Import `alpha-old` in a scratch script → the `alpha` module loads and the warning is logged.

## Boundaries
- Do not change module behaviour beyond the names.
- Not permitted: pushing, new dependencies.
- If a rename would break something important, do not rename that module; explain in the report.

## Result
- Report in the final message: what was renamed, how aliases work, tests 1-4 with PASS/FAIL, deviations.
- Last line: "PASS x/4".
```

## Example 2: a feature with an interface

Effort `high`, access `workspace-write`.

```markdown
# Task: Add CSV export of the filtered expenses to the dashboard

## Goal
The user wants to download the expenses currently shown on the dashboard and analyse them
in a spreadsheet. The button label is the user's wording: «Скачать CSV».

## Context
- Agreed with the user: export only the rows matching the current filters; CSV formatted for
  Russian Excel; the button sits next to the filters.
- The dashboard is React + Vite. Data comes from `src/data/expenses.ts`.
- Read `src/components/Filters.tsx` and `src/pages/Dashboard.tsx` first.

## Where
Repository `expenses-dashboard`, new branch `feature/csv-export` from `main`.

## Changes
### 1. Export button
- Now: there is no way to download the data.
- Required: a button «Скачать CSV» next to the filters. It downloads `expenses-<YYYY-MM-DD>.csv`
  with exactly the rows shown, in the table's column order.
- Follow: the style of the existing filter buttons.
### 2. File format
- Required: UTF-8 with BOM, `;` separator, decimal comma, values containing `;` or quotes are quoted.
- Required: with no matching rows the file contains only the header row.
- Keep: the existing JSON export for the API is unchanged.

## Tests: run all of them and record each result
- Before changing anything, save the output of `npm test` and `npm run build` as the baseline.
- Scratch files go to `tmp/csv-export/`, which is ignored by git.
1. Unit test for the CSV builder: 3 normal rows → header + 3 rows, amounts with a decimal comma.
2. Unit test: an empty list → header only.
3. Unit test: a description containing `;` and `"` → the value is quoted and escaped.
4. `npm test` → passes; no test that passed in the baseline fails.
5. `npm run build` → passes with no new warnings compared with the baseline.
6. In the browser: filter to one category, export, open the file → the rows match the table on screen.
   If you cannot open a browser, write FAIL with the reason; do not skip silently.
- Stop the dev server you started.

## Boundaries
- Do not change the filters, charts or data loading.
- Not permitted: new dependencies, pushing, changes to `main`.
- For this fictional brief the user explicitly requested Russian interface text and English code/comments.

## Result
- Report: `tmp/csv-export/REPORT.md` with changed files, what was done for each change, tests 1-6 with
  command, expected, actual and PASS/FAIL, and deviations with reasons.
- Final message: the report path and the line "PASS x/6".
```

## Example 3: a review without changes

Effort `high`, access `read-only`.

```markdown
# Task: Review the payment retry logic for double charges

## Goal
The user saw two charges for one order last week and wants to know whether the retry code
can charge twice. Find the risks; do not fix them.

## Context
- Retries were added in commit `a1b2c3d`.
- The payment provider's API is idempotent only when an `Idempotency-Key` header is sent.

## Where
Repository `shop-backend`, branch `main`. Start with `src/payments/` and `src/jobs/retry.ts`.

## Questions to answer
1. Every path where a charge request can be sent more than once for the same order.
2. For each: file and line, the sequence of events that leads to a second charge, how likely it is.
3. Whether every charge request sends an idempotency key, and whether the key stays the same across retries.

## Boundaries
- Read only: change no files, run no payments or network calls.

## Result
- Final message: findings ordered by severity, each with file:line and a concrete sequence of events;
  then what you checked and found safe. If you found no path to a double charge, say so and list what you checked.
```

## Continuing a session

A follow-up turn in the same session does not repeat the whole brief. Say what is wrong, what to do and how it will be checked:

```markdown
The export works, but two things need fixing:
1. Amounts are written with a dot ("1234.50"); Russian Excel needs a comma ("1234,50").
2. The file name uses the local time; use the date of the newest exported row.

Keep everything else as it is.
Tests: add unit tests for both cases; `npm test` passes.
Report: what changed and the test results. Last line: "PASS x/2".
```

## A weak brief and a strong one

Weak: one paragraph, no structure.

```markdown
The export on the dashboard is broken, the user says the Russian text looks wrong in Excel and
maybe something else too, please look into it and make it better, also check the amounts and
make sure everything works and test it properly before you finish.
```

The worker does not know which file is involved, what "wrong" looks like, what "better" means, which tests prove it, or what to report.

Strong:

```markdown
# Task: Fix the garbled Russian text in the dashboard CSV export

## Goal
The user opens the exported CSV in Excel and sees «Ð¿Ñ€Ð¾...» instead of Russian category names.

## Where
Repository `expenses-dashboard`, branch `main`. The export is built in `src/export/csv.ts`.

## Changes
### 1. Encoding
- Now: the file is UTF-8 without a BOM, so Excel reads it as a legacy code page.
- Required: Russian text opens correctly in Excel on Windows by double click.
- Keep: the separator and column order.

## Tests: run all of them and record each result
1. Unit test: the generated file starts with the UTF-8 BOM → passes.
2. `npm test` → passes.

## Boundaries
- Change only the CSV export. No new dependencies.

## Result
- Final message: the cause, the change, tests 1-2 with PASS/FAIL. Last line: "PASS x/2".
```
