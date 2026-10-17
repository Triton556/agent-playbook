---
name: product-testing
description: Verify software behavior and review code changes against requirements. Use for tests, regressions, TDD, test strategy, code review, and release-readiness evidence. Covers behavioral and code checks; rendered interface quality belongs to product-ui-review, and diagnosing a failing check belongs to product-debugging.
---

# Testing and code review

Select the requested deliverable: change verification, tests/TDD or review-only. Establish the revision/working diff, including relevant uncommitted changes, requirements and risk. Use criteria from the [saved acceptance program](../product-engineering/references/task-brief-and-acceptance.md), without a new specification.

## Behavior verification

Check actual project commands. Run applicable type/build/lint checks and scenarios that distinguish correct from incorrect behavior. Choose the smallest sufficient set; run the full suite when project requirements or risk breadth demand it.

A new test observes results across a public boundary. Derive expectations from the contract/verified example, not by repeating the implementation's computation. Use real test seams; isolate external nondeterminism without losing the check's meaning. Financial logic requires tests.

For significant regressions, add a failing test before the fix when applicable. A reversible visual edit needs the relevant render/scenario and necessary existing checks. TDD: one observable behavior → red → minimal implementation → green → appropriate refactoring. Flakiness requires evidence about conditions and repeatability, not one green result. Targeted references: [tdd](vendor/matt-pocock/tdd/INSTRUCTIONS.md), [tests](vendor/matt-pocock/tdd/tests.md), [mocking](vendor/matt-pocock/tdd/mocking.md).

A detail's presence in code does not establish its function/meaning. [product-ui-review](../product-ui-review/SKILL.md) owns UI scenarios and rendered evidence; one current pass may cover both sets of criteria. Send unexplained failures to [debugging](../product-debugging/SKILL.md) with actual output.

## Code review

Review the current diff against requirements, contracts and project patterns; open [code-review](vendor/matt-pocock/code-review/INSTRUCTIONS.md) when needed. A finding includes a concrete trigger, incorrect behavior, impact and location. Distinguish taste recommendations from defects. This is self-review if you authored the change; the skill does not launch another agent.

In review-only mode, deliver findings and gaps. Repairs, affected rechecks and completion follow [WORKFLOW](../../workflow/WORKFLOW.md). Relate commands/scenarios, observations and limitations to the current revision; unperformed work cannot receive pass.

Verify the workflow itself using the single [pilot](../product-engineering/references/workflow-pilot.md) only when requested. Sources: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
