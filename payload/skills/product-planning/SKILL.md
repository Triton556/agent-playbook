---
name: product-planning
description: Plan a software product, feature, integration, or substantial redesign from a brief and repository context. Use for requirements, specifications, architecture tradeoffs, decomposition, and acceptance criteria before implementation. Produces a scoped plan; an existing clear plan or tiny fix does not need a new planning cycle.
---

# Development planning

Produce an executable plan scaled to the task. [Task brief and acceptance](../product-engineering/references/task-brief-and-acceptance.md) owns the interview, saved answers, participation modes and criteria; use that same basis.

1. Establish the user, their action and observable result. Check material assumptions against the repository, documents and available sources.
2. Find integration points, data, contracts and constraints. Compare alternatives only for decisions with material effects on the product, cost, complexity or reversibility.
3. Decompose implementation into verifiable user scenarios, dependencies and change locations. State verification and recovery for risky migrations/releases; separate open questions from decisions.

For substantial UX decisions, use [product-ui-design](../product-ui-design/SKILL.md) in design mode. Use domain-modeling for terminology/ADRs when actually part of the deliverable. [to-spec](vendor/matt-pocock/to-spec/INSTRUCTIONS.md) is a targeted reference; mandatory upstream interviews and publication are not additional stages.

Connect each requirement with its implementation location and verification. A clear task with a ready plan does not get another planning cycle. Deliver the plan for a plan-only request; in already authorized end-to-end development, proceed to [implementation](../product-implementation/SKILL.md). [WORKFLOW](../../workflow/WORKFLOW.md) owns shared transitions and completion.

Sources: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
