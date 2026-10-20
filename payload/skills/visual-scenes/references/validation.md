# Validation protocol

## Compare artifact revisions

Record the baseline, one question, the proposed change and a concrete comparison state. Match model inputs, revision, seed, camera, time, viewport and relevant rendering settings. When the hypothesis concerns one of those fields, make that the explicit independent variable.

Evaluate in three separate columns:

| Model and behavior | Rendered communication | Runtime |
| --- | --- | --- |
| Correct dependency, numerical invariant, consistent views, valid transitions | Readable subject, consequence, hierarchy, material, labels, controls | Response latency, full-frame cost, load/failure behavior |

Claim scope: see [human-perspective-review, Readiness and transfer](../../dev-flow/references/human-perspective-review.md#readiness-and-transfer). Retain a change when observed benefits outweigh regressions for the task; further iteration follows WORKFLOW, step 6.

## Proportional checks

- **Model:** use meaningful known cases and invariants. For a queue, conservation/order; for optics, critical boundaries and energy; for a graph, correspondence after operations; for a chart, truthful scale and missing data. Check unit conversions. Keep illustrative models labeled.
- **State:** preset → manual edit → pause → edit → reset; add cancel/undo and stale-result checks when those features exist. Verify the output actually settles. An immediate DOM read during easing may contain transitional values.
- **Render:** inspect the actual images at the viewport sizes required by the brief. For a desktop dashboard, prioritize its desktop working area; add narrow/mobile acceptance when requested or required by the product. Verify crucial labels, contrast, object silhouette, camera fit and essential paths. Save the reviewed frames with state notes. Inspect rather than inferring aesthetics from file existence.
- **Input:** complete the main scenario by keyboard and the intended pointer method. Reduced motion, focus, disabled/pending controls and failure states should preserve comprehension.
- **Runtime:** build/type/lint and console checks; Speed claims: see [runtime-accessibility, Budget the complete result](runtime-accessibility.md#budget-the-complete-result).

## Evidence record

```text
Date and URL/build:
Input and state (including settled/transition):
Action:
Observed image and values:
Screenshot/artifact:
Model/source facts separately:
Interpretation / proposed transfer:
Unverified limits:
```

Evidence grades: see [human-perspective-review, Readiness and transfer](../../dev-flow/references/human-perspective-review.md#readiness-and-transfer). Record the instrument-specific coverage actually observed.

Instruction authoring: see [agent-instructions, Pointers and authority](../../agent-instructions/SKILL.md#pointers-and-authority). Workflow experiments: see [workflow-pilot](../../dev-flow/references/workflow-pilot.md).

For repeated defects/batches use [quality-cycle](../../dev-flow/references/quality-cycle.md). Declare shape-normalized versus common world framing and retain useful independent views/crops. Evidence grades: see [human-perspective-review, Readiness and transfer](../../dev-flow/references/human-perspective-review.md#readiness-and-transfer).
