---
name: dev-implement
description: Build an agreed software change across its required layers. Use for a clear brief; unexplained failures use dev-debug, open architecture uses dev-plan.
---

# Implementation

Input: a clear task or saved plan. Output: a working scenario across the required layers. Task records: see [task-state, Long-task state and completeness](../dev-flow/references/task-state.md#long-task-state-and-completeness).

Read relevant code and uncommitted changes; find existing components, contracts and project commands. Work in vertical slices: user action → required layers → observable result → verification. Complete a useful slice before widening the surface; integrate declared behavior with real data/logic and identify demonstration stubs.

Reuse existing modules and public boundaries. Add abstraction only for a demonstrated shared need; do not introduce agents or publication as implementation prerequisites.

- New UI decisions: [design](../ui-design/SKILL.md), then [review](../ui-review/SKILL.md) after implementation.
- Unexplained failure: [debugging](../dev-debug/SKILL.md) with the actual symptom.
- Behavior/code verification: [testing](../dev-verify/SKILL.md) proportional to risk.

Evidence reuse: see [task-brief-and-acceptance, 7. Execution, verification and completion](../dev-flow/references/task-brief-and-acceptance.md#7-execution-verification-and-completion). Sources: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
