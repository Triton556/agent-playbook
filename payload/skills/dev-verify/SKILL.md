---
name: dev-verify
description: Verify software behavior and review code changes against requirements. Use for tests, regressions, TDD, test strategy, code review, and release-readiness evidence. Covers behavioral and code checks; rendered interface quality belongs to ui-review, and diagnosing a failing check belongs to dev-debug.
---

# Testing and code review

Select the requested deliverable: change verification, tests/TDD or review-only. Establish the revision/working diff, including relevant uncommitted changes, requirements and risk. Use criteria from the [saved acceptance program](../dev-flow/references/task-brief-and-acceptance.md), without a new specification.

## Behavior verification

Check actual project commands. Run applicable type/build/lint checks and scenarios that distinguish correct from incorrect behavior. Choose the smallest sufficient set; run the full suite when project requirements or risk breadth demand it.

A new test observes results across a public boundary. Derive expectations from the contract/verified example, not by repeating the implementation's computation. Use real test seams; isolate external nondeterminism without losing the check's meaning. Financial logic requires tests.

For significant regressions, add a failing test before the fix when applicable. A reversible visual edit needs the relevant render/scenario and necessary existing checks. TDD: one observable behavior → red → minimal implementation → green → appropriate refactoring. Flakiness requires evidence about conditions and repeatability, not one green result. Targeted references: [tdd](vendor/matt-pocock/tdd/INSTRUCTIONS.md), [tests](vendor/matt-pocock/tdd/tests.md), [mocking](vendor/matt-pocock/tdd/mocking.md).

A detail’s presence in code does not establish its meaning. UI render/scenario: see [ui-review](../ui-review/SKILL.md). Evidence reuse: see [task-brief-and-acceptance, 7. Execution, verification and completion](../dev-flow/references/task-brief-and-acceptance.md#7-execution-verification-and-completion). Send unexplained failures to dev-debug with actual output.

## Code review

Review the current diff against requirements, contracts and project patterns; open [code-review](vendor/matt-pocock/code-review/INSTRUCTIONS.md) when needed. A finding includes a concrete trigger, incorrect behavior, impact and location. Distinguish taste recommendations from defects. This is self-review if you authored the change; the skill does not launch another agent.

Review scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries). Repairs: see [WORKFLOW, step 6](../../workflow/WORKFLOW.md#work-route). Reporting grades: see [human-perspective-review, Readiness and transfer](../dev-flow/references/human-perspective-review.md#readiness-and-transfer).

Workflow comparison: see [workflow-pilot](../dev-flow/references/workflow-pilot.md). Sources: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
