---
name: dev-implement
description: Implement an agreed software feature, integration, application, or code improvement as working behavior across the required layers. Use for building from a clear brief or plan and for routine implementation decisions. Route unexplained failures to dev-debug and substantial open architecture to dev-plan.
---

# Implementation

Input: a clear task or saved plan. Output: a working scenario across the required layers. Task records: see [task-state, Long-task state and completeness](../dev-flow/references/task-state.md#long-task-state-and-completeness).

Read relevant code and uncommitted changes; find existing components, contracts and project commands. Work in vertical slices: user action → required layers → observable result → verification. Complete a useful slice before widening the surface; integrate declared behavior with real data/logic and identify demonstration stubs.

Reuse existing modules. For a complex boundary, consult [codebase-design](vendor/matt-pocock/codebase-design/INSTRUCTIONS.md); for a lengthy implementation, [implement](vendor/matt-pocock/implement/INSTRUCTIONS.md). They do not add mandatory agents or publication.

- New UI decisions: [design](../ui-design/SKILL.md), then [review](../ui-review/SKILL.md) after implementation.
- Unexplained failure: [debugging](../dev-debug/SKILL.md) with the actual symptom.
- Behavior/code verification: [testing](../dev-verify/SKILL.md) proportional to risk.

Evidence reuse: see [task-brief-and-acceptance, 7. Execution, verification and completion](../dev-flow/references/task-brief-and-acceptance.md#7-execution-verification-and-completion). Sources: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
