---
name: dev-verify
description: Verify changed software contracts or review code. UI acceptance uses ui-design user steps and actual rendered observations, not test counts.
---

# Testing and code review

## Behavior verification

| Changed surface or observed issue | Check | Evidence to report |
| --- | --- | --- |
| A person-facing action, screen or state changed | Follow [ui-design](../ui-design/SKILL.md) through the real steps, opened surfaces and relevant recovery states | Expected and actual observations per step; readability and unperformed steps |
| A public API/data operation changed | Exercise that boundary against expected results from its agreed contract or a verified independent example | Input, expected result, actual result and failure handling |
| A reproduced bug was repaired | Repeat the original failing case; add a regression test when it can distinguish that bug from correct behavior | The original symptom no longer occurs; dependent contract checks remain correct |
| Project configuration requires build/type/lint/test commands | Run the applicable commands for this change | Actual command outcomes; these do not establish UI acceptance |
| A failure is intermittent | Record the conditions and reproduce across those conditions; use dev-debug | Reproduction limits and observations, not one green run |
| The command, UI, data or environment is unavailable | State the unavailable operation and reason | NOT_RUN or unverified, not PASS |

Derive the expected behavior from the request, contract or independent reference before asserting the result. A test that repeats the implementation's computation can confirm consistency with the code while missing the user's requirement. Unit, API and regression tests remain valid supporting tools; they are not a quota or a substitute for human-flow evidence.

For an explicitly requested TDD change: choose one observable contract case, observe its failure, implement that behavior, then rerun and refactor while preserving it. External nondeterminism may be isolated when the tested contract remains observable.

## Code review

Review the current diff, including relevant uncommitted changes, against the agreed behavior and project contracts. A finding names the triggering input/step, incorrect result, impact and location. Distinguish a defect from a taste preference. Reviewing your own change is self-review and does not launch another reviewer.

After applicable checks pass, repeat or broaden only for a new change, an observed failure or a named unresolved risk. The final report distinguishes functional observations, technical checks and UI inspection; none silently stands in for the others.
