---
name: agent-instructions
description: Edit agent-facing rules and workflow documents. Use for a requested instruction change; skill creation uses the built-in skill-creator.
---

# Writing instructions for agents

This skill owns instruction prose and information placement. Skill packaging, metadata and installation belong to the built-in skill-creator supplied by the selected client (verify availability). A requested workflow experiment follows the single [pilot procedure](../dev-flow/references/workflow-pilot.md). These are different operations, not three consecutive authoring cycles.

## Edit the existing instruction

1. Establish the requested behavior, affected entrypoints and existing owner. Reuse the user's decisions and the project's format. A source example or past defect is evidence, not automatically a universal requirement.
2. Keep each meaning in one authoritative location. Entry points carry the condition for opening a reference; references contain the procedure. Inspect callers before moving material and preserve useful paths with short redirects where needed.
3. State the outcome and the decisions that change it. A step needs an observable completion condition proportional to the task; exhaustive checking applies to the declared scope, not every possible artifact. Fixed sequences are useful for fragile operations, while creative work needs room for judgment.
4. Put essential shared guidance in the entrypoint and conditional detail beside its trigger. Group a concept, its constraints and exceptions. Remove duplicate procedures, stale instructions and generic advice that adds no decision value; preserve real permissions and non-obvious invariants.
5. Check affected links and consistency with callers. If executable behavior changes, use its relevant checks. Workflow experiments: see workflow-pilot, Pilot task and metrics.

## Pointers and authority

A useful pointer states what the target supplies and when to open it. Distinguish independent branches rather than listing synonyms. Do not copy readily discoverable commands/configuration into several guides. Loading and recovery: see WORKFLOW, step 2.

The local [WORKFLOW](../../workflow/WORKFLOW.md) owns task progression. A specialist adds its subject-specific method instead of restating the interview, permissions, state and acceptance loop. To repair a duplicated rule, choose its owner, update callers and remove the redundant bodies in the same change.

Action scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).
