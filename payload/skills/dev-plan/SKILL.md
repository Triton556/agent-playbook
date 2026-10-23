---
name: dev-plan
description: Scope software requirements, architecture choices, decomposition and acceptance before implementation. Skip a new planning cycle for an existing clear plan or tiny fix.
---

# Development planning

Produce an executable plan scaled to the task. [Task brief and acceptance](../dev-flow/references/task-brief-and-acceptance.md) owns the interview, saved answers, participation modes and criteria; use that same basis.

1. Establish the user, their action and observable result. Check material assumptions against the repository, documents and available sources.
2. Find integration points, data, contracts and constraints. Compare alternatives only for decisions with material effects on the product, cost, complexity or reversibility.
3. Decompose implementation into verifiable user scenarios, dependencies and change locations. State verification and recovery for risky migrations/releases; separate open questions from decisions.

For substantial UX decisions, use [ui-design](../ui-design/SKILL.md) in design mode. Name domain terms and record architectural decisions only when needed for the deliverable; reuse an existing glossary or ADR format.

Connect each requirement with its implementation location and verification. A clear task with a ready plan does not get another planning cycle. Deliverable scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries). For authorized implementation, continue to [dev-implement](references/implementation.md). [WORKFLOW](../../workflow/WORKFLOW.md) owns shared transitions and completion.

Sources: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
