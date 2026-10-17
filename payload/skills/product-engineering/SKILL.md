---
name: product-engineering
description: Route and carry an end-to-end software task through the relevant planning, implementation, debugging, testing, and UI stages. Use for multi-stage development or requests to finish a product or feature. A narrow planning, bug, test, or design task can use its specialist skill directly. Excludes general research, creative writing, and household advice.
---

# Select an engineering stage

The coordinator selects a specialist by the nearest deliverable; [WORKFLOW](../../workflow/WORKFLOW.md) owns general task progression. A narrow request may use the relevant stage directly. Changing skills does not create an agent or require another interview/plan.

| Required result | Entry |
| --- | --- |
| Requirements, architecture alternatives, executable plan | [product-planning](../product-planning/SKILL.md) |
| Working feature or integration | [product-implementation](../product-implementation/SKILL.md) |
| Cause of failure, regression or flakiness | [product-debugging](../product-debugging/SKILL.md) |
| Behavior verification or code review | [product-testing](../product-testing/SKILL.md) |
| UI flow and visual decisions | [product-ui-design](../product-ui-design/SKILL.md) |
| Actual inspection of implemented UI | [product-ui-review](../product-ui-review/SKILL.md) |
| Authorized binary/protocol analysis | [Reverse engineering](references/reverse-engineering.md) |

For end-to-end development, connect finished scenarios and advance by results: sufficient plan → working slice → relevant checks. UI uses design before new visual decisions and review after rendering. Route unexplained failures to debugging. A plan-only/review-only request ends with that deliverable.

Open shared procedures at their WORKFLOW triggers; do not load the entire set. Skills own subject methods and sources: [composition and adaptations](references/composition.md).
