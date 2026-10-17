# Validation protocol

## Compare artifact revisions

Record the baseline, one question, the proposed change and a concrete comparison state. Match model inputs, revision, seed, camera, time, viewport and relevant rendering settings. When the hypothesis concerns one of those fields, make that the explicit independent variable.

Evaluate in three separate columns:

| Model and behavior | Rendered communication | Runtime |
| --- | --- | --- |
| Correct dependency, numerical invariant, consistent views, valid transitions | Readable subject, consequence, hierarchy, material, labels, controls | Response latency, full-frame cost, load/failure behavior |

A win in one column does not prove the other two. Save the observed improvement and regressions; retain the change only when it helps the task. Stop polishing when the acceptance criteria are met, unless a new concrete defect warrants another iteration.

## Proportional checks

- **Model:** use meaningful known cases and invariants. For a queue, conservation/order; for optics, critical boundaries and energy; for a graph, correspondence after operations; for a chart, truthful scale and missing data. Check unit conversions. Keep illustrative models labeled.
- **State:** preset → manual edit → pause → edit → reset; add cancel/undo and stale-result checks when those features exist. Verify the output actually settles. An immediate DOM read during easing may contain transitional values.
- **Render:** inspect the actual images at the viewport sizes required by the brief. For a desktop dashboard, prioritize its desktop working area; add narrow/mobile acceptance when requested or required by the product. Verify crucial labels, contrast, object silhouette, camera fit and essential paths. Save the reviewed frames with state notes. Inspect rather than inferring aesthetics from file existence.
- **Input:** complete the main scenario by keyboard and the intended pointer method. Reduced motion, focus, disabled/pending controls and failure states should preserve comprehension.
- **Runtime:** appropriate build/type/lint tests, relevant console errors, and bounded performance evidence. Only make speed claims supported by comparable measurements.

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

Use precise coverage language: catalog card, rendered page, interaction, targeted source reading, complete source audit and independently reproduced mechanism are different claims. Record what was actually done. A screenshot of one desktop state cannot establish all mobile interactions; source presence cannot establish successful execution.

This document checks the visual instrument, not the skill-authoring process. Creating/editing a skill follows the built-in skill-creator; an explicitly requested workflow experiment follows the single [workflow-pilot](../../product-engineering/references/workflow-pilot.md). An artifact check does not automatically launch that pilot. Structural validation does not establish future aesthetic judgment; call a self-review a self-review.

For repeated defects or a batch of authored artifacts, use [the quality cycle](../../product-engineering/references/quality-cycle.md) and its evidence guidance; use the existing ledger when its machine validation is needed. Keep function/style/context acceptance separate from file validity. Declare whether framing is shape-normalized or common world scale; keep useful independent views/crops with the actual revision. General model commentary, measured/source findings, agent visual observations and human feedback retain their different evidence grades.
