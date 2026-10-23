# Work route

Use this table to choose the next action, not to run every row. Continue from the current task state. A route selects instruction text; it does not launch another agent.

| Observed event | Action | Observable output / next step |
| --- | --- | --- |
| The requested outcome or a consequential choice is unresolved | Read [task brief, questions](../skills/dev-flow/references/task-brief-and-acceptance.md#3-ask-only-what-changes-the-work); ask about that choice, retaining known answers | A resolved choice or a named blocked decision; continue independent work |
| A plan or architecture decision is requested | Use [dev-plan](../skills/dev-plan/SKILL.md) | Requirements mapped to changes and checks; implementation only when requested |
| A UI action, label, layout or state changes | Use [ui-design](../skills/ui-design/SKILL.md) | Human steps and expected observations; then actual render/action results |
| A non-UI feature has an agreed contract | Use [implementation](../skills/dev-plan/references/implementation.md) | A working scenario across its required layers; verify the contract |
| An observed result differs from its expected result | Use [dev-debug](../skills/dev-debug/SKILL.md) with the symptom and output | Reproduced cause, repair and the original failing case rerun |
| Changed code needs technical verification, or code review is requested | Use [dev-verify](../skills/dev-verify/SKILL.md) | Contract-based results/findings; UI acceptance still requires the human path |
| The user selects the brain role or delegates a task or project | Use [you-are-brain](../skills/you-are-brain/SKILL.md) | Restore or establish the selected worker route and task scope |
| A voxel asset is created or its silhouette/action/kit integration changes | Use [voxel-models](../skills/voxel-models/SKILL.md) | Passport and six coherent design views before detailed voxels; then inspect the actual model |
| The user requests creative directions, or an open concept requires their choice | Use [creative-direction](../skills/creative-direction/SKILL.md) | A direction grounded in the user's intent; no idea/reference quota |
| An instruction or its routing changes | Use [agent-instructions](../skills/agent-instructions/SKILL.md) | One updated owner and consistent callers |
| A requested fact conflicts with sources, a required property lacks evidence, or the same defect recurs | Read [reference-grounding](../skills/dev-flow/references/reference-grounding.md#observable-triggers) for that property | Evidence, a distinguishing experiment or an explicitly unresolved assumption |
| A workflow comparison is explicitly requested | Read [workflow-pilot](../skills/dev-flow/references/workflow-pilot.md) | Comparable cases and stated measurement limits; no automatic model benchmark |
| The user asks for an ordinary explanation or practical answer | Answer directly; verify factual claims against their source | The requested answer, not a software-project ritual |

## Context loading and recovery

Open the row's owner and a reference only when its named question, operation or failure is present. Once the next action and its expected observation are defined, perform it instead of following every link. Reuse a document already read in the current context; reread it after a file change, or after recovery if the relevant decision/state is missing. Restore the current result, unresolved choices and running worker identities before continuing; a correction is not a new setup interview.

## Check, repair and finish

Choose expected observations from the user's requested behavior, an existing contract or a verified example, not by translating the current implementation into assertions. For UI, follow the steps and inspect the reached states. For non-UI code, use project-required commands and tests at the changed public boundary.

When a check fails, preserve its symptom/output, establish the cause, repair it and rerun that case plus the dependent contract checks. Broaden a check only for a new change, an observed failure or a named unresolved risk. After required checks pass and discovered material defects are resolved, deliver the result and remaining limitations; a repeated identical inspection is not new evidence.

For a series with a shared repeated defect, [quality-cycle](../skills/dev-flow/references/quality-cycle.md) describes family-level correction. Record long-task state in the existing plan; [task-state](../skills/dev-flow/references/task-state.md) supplies a schema only when a machine-readable state record is being used. These references do not create new reviewer sessions or user approvals.
