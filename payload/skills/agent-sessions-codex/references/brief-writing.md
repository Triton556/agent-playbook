# Writing the brief

The brief is the worker's whole view of the task. The worker does not see your conversation with the user, your notes or your reasoning: only the brief, the files and its own instructions. A vague or unstructured brief makes the worker either take liberties or stall. Write it so that a capable engineer who has never heard of the project could do the work and prove it is done.

## Language

- Write the brief in English, whatever language the user speaks.
- Use English for all agent-to-agent communication: briefs and follow-ups, commentary, progress updates, questions, final responses and written reports. Choose the language by the intended recipient, not by who can view the session.
- In a delegated worker session, the recipient is the orchestrator unless the current user instruction explicitly addresses a particular output directly to the user. A session visible to the user does not make a worker-to-orchestrator message user-facing.
- Include an explicit Audience and language block in every initial brief. State the recipient and the language of each user-facing deliverable. On continuation, retain that assignment unless the current user instruction changes it; restate any change explicitly.
- Preserve exact source quotations, identifiers, paths, commands and required product text in their original language. Mark quotations as quotations. Write interface text, documents and other user-facing deliverables in the language specified for that output; their language does not change the surrounding message or report to the orchestrator.
- Direct conversation with the user and knowledge-base prose follow [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries), including the user's explicit language exceptions. A report to another agent is agent-to-agent communication.

## Checked launch review

Prepare the private [checked assignment](../../agent-sessions/references/contract.md#checked-brief-assignment) alongside the initial brief and pass it with `--assignment` for bundled adapters. It makes recipient, communication/deliverable languages, scope and memory-writer assignment explicit. It is not a permission grant or a prose-language detector.

Before launch, read the entire brief, including Result/Return, against that assignment. Remove contradictory report-language instructions; a correct audience heading does not neutralize a later conflicting sentence. Keep exact quotations and deliverable-language requirements. A genuine current-owner exception is recorded with `owner_override`; do not invent one to bypass a failed check. For short corrections, inherit the frozen assignment through [run recovery](../../agent-sessions/references/contract.md#recover-a-run) or pass the reviewed assignment with the existing thread ID. Do not regenerate the initial brief or reset the setup.

## Form

- Use short headings or numbered requirements when they help referencing; a small brief may use concise prose.
- Use concrete behavior or grounded limits instead of vague adjectives: "returns 413" rather than "fails". Do not invent numeric thresholds the task does not require.
- Exact strings in quotes: messages, labels, error codes, file names, commands.
- Each material requirement has a sufficient observable check; one check can cover several requirements. A check may be an existing test, actual interaction, render or source inspection appropriate to the property; it need not be a new automated test.

Detail goes into what must be true and how it will be checked. It does not go into step-by-step instructions for writing the code: the worker has its own workflow, and prescribing every step lowers the quality. Name a specific approach only when the user decided it, or when the project already has a pattern the change must follow.

Independent reviewer briefs: [independent-review, Preparation](../../../workflow/independent-review.md#preparation) owns information staging and overrides the generic cause/baseline fields below.

## Template

```markdown
# Task: <one line: what should exist or change>

## Audience and language
Recipient: orchestrator
Communication language: en
Memory writer: orchestrator
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

## Verification: scoped required checks
- Record a baseline when comparison or diagnosis needs it; reuse existing evidence for the same revision and conditions. Do not run unrelated baseline suites.
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
  changed files and result; required checks with command or method and PASS/FAIL/NOT_RUN, plus actual output for failures or material observations;
  deviations from the brief, with reasons; what was not verified.
- Final message: <exact format, for example "the report path and the line 'PASS x/N'">.
```

Use only sections needed to communicate the task, boundaries and acceptance. Keep audience/language and checked assignment fields required by the launch contract. A short task gets a short brief; the template is not a documentation quota.

## Rules

- **Self-contained.** No "as discussed", "the usual way" or "the file from before". Name the file and quote the decision.
- **Concrete paths and names.** Exact folders, files, functions, commands, branches.
- **Similar cases named.** If a change could be confused with a neighbouring case (another error with the same code, another screen with the same component), say which one must stay as it is.
- **Baseline first.** For anything that compares before and after, the worker records the baseline before editing.
- **Boundaries that cannot be misread.** State material restrictions and already authorized actions the task needs; do not invent an approval checklist for ordinary steps. Resolve ambiguous permissions for: image generation, network access, package installs, browser, running servers, deleting files. Avoid umbrella words such as "local only" or "no external services": a worker may read them as forbidding a tool the task needs, or as allowing one it must not use.
- **One task per brief.** Independent pieces go to separate sessions.
- **Nothing private that is not needed.** No secrets, tokens, personal data or unrelated history. Tell the worker never to print keys it uses.
- **Memory.** Retain the launch contract’s writer assignment; perform capture only when an authorized integration is active and there is new reusable knowledge. Required integration checkpoints still apply. See [kb-save, Delegated work](../../kb-save/SKILL.md#delegated-work).
- **Run settings are not in the brief.** Model, effort and access mode are passed to the adapter.

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
