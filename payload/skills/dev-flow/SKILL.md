---
name: dev-flow
description: Coordinate multi-stage software work from the relevant stage to verified delivery. Narrow planning, bug, test or UI tasks can use the specialist directly.
---

# Select an engineering stage

The coordinator selects a specialist by the nearest deliverable; [WORKFLOW](../../workflow/WORKFLOW.md) owns general task progression. A narrow request may use the relevant stage directly. Changing skills does not create an agent or require another interview/plan.

| Required result | Entry |
| --- | --- |
| Requirements, architecture alternatives, executable plan | [dev-plan](../dev-plan/SKILL.md) |
| Working feature or integration | [dev-implement](../dev-implement/SKILL.md) |
| Cause of failure, regression or flakiness | [dev-debug](../dev-debug/SKILL.md) |
| Behavior verification or code review | [dev-verify](../dev-verify/SKILL.md) |
| UI flow and visual decisions | [ui-design](../ui-design/SKILL.md) |
| Actual inspection of implemented UI | [ui-review](../ui-review/SKILL.md) |
| Authorized binary/protocol analysis | [Reverse engineering](references/reverse-engineering.md) |

For end-to-end development, connect finished scenarios and advance by results: sufficient plan → working slice → relevant checks. UI uses design before new visual decisions and review after rendering. Route unexplained failures to debugging. Deliverable scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

Loading: see WORKFLOW, step 2. Skills own subject methods and sources: [composition and adaptations](references/composition.md).
