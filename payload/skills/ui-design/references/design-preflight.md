# UI design basis: scenario, style and related states

Open for a new flow, changed action meaning or screen reorganization. Map the human steps before implementing that change. A bounded label/spacing fix keeps the accepted flow and checks its affected reached state. Use the existing task/plan and project components; this reference does not require a separate document, schema, Figma file or image-generation call.

## 1. Record the scenario brief

Record the entry route/data, the person's goal, actions, expected result, target window/input method and project components/tokens. Preserve the user's named qualities and existing behavior outside the change.

If two interpretations change what the person can do or what result they receive, ask about that choice; reuse the [saved brief](../../dev-flow/references/task-brief-and-acceptance.md) rather than running another interview. If the question concerns a new creative direction, use creative-direction only for that open choice. If it concerns a factual contradiction, inspect the sources for that property using [reference-grounding](../../dev-flow/references/reference-grounding.md#observable-triggers).

**Output:** a named route, user goal, expected completion, window and accepted design basis; unanswered choices are identified, not silently guessed.

## 2. Link screens, states and sizes

Write **human step → action → reached surface/state → expected observation → return/recovery**. A verification point includes route, state, data and window/zoom.

| Actual change | Include in the map |
| --- | --- |
| New or changed async action | Pending feedback, committed result, supported failure and retry; prevent unintended duplicate work |
| Input or validation | Normal input, invalid input, correction and preservation of valid data |
| Dialog, menu, drawer or popover | Trigger, opened surface, readable content, focus, close/back and retained parent context |
| Filter/search | Matching data, no matches, clearing conditions and retained selection/filter behavior |
| Layout or responsive boundary | The supported window and the boundary where wrapping/collapse changes; no unrequested mobile redesign |
| Shared data shown in multiple places | Same current result/state across the affected views; older async results cannot overwrite a newer result |

These are branches of the changed scenario, not a mandatory cross-product of every state/device/theme. Use real long labels and data that can expose overflow. Include the main uninterrupted path from entry to completion.

**Output:** a traceable path to the result and the changed failure/return paths, including hidden surfaces that must actually be opened later.

## 3. Verify the mockup or prototype before full implementation

Use a representation only when it can resolve an open design choice: wireframe for information order, styled region for typography/hierarchy, interactive prototype for navigation or transition behavior. An accepted flow and existing components do not require a new mockup before a bounded change.

Check the disputed property at the target window with actual label lengths/content. Record the observed choice and carry it into the existing basis. A wireframe does not verify typography; a still does not verify interaction. A design-only request ends here, with working behavior explicitly unverified.

**Output:** the open design choice is resolved, or its remaining uncertainty and dependent implementation step are stated. No fixed number of sketches or references is required.

## 4. Compare the working UI with the basis

Continue in [ui-design](../SKILL.md) using the [actual-render/action procedure](../../ui-review/references/visual-quality.md#render-and-behavior-verification). Open the same route/state/data/window and execute the mapped actions; inspect all affected hidden surfaces at their reached states.

Record separately:

- Whether the result preserves the accepted design decisions.
- Whether the actual steps produce their promised outcomes and retain/recover user work.
- Whether content and controls are readable, understandable and reachable at the intended size.

A faithful copy of a poor mockup can still fail the user's task. Classify a mismatch as an implementation defect, an agreed adaptation or a basis problem. When no mockup exists, compare against current requirements/components; do not invent a retrospective preflight claim.

**Output:** actual per-step observations, corrected defects and explicit NOT_RUN/unverified steps. After a repair, repeat the failed step and dependent transitions; a shared navigation/state change calls for the connected path to be rerun. The [work route](../../../workflow/WORKFLOW.md#check-repair-and-finish) defines when to stop.

## Proportional application example

For a desktop table: search → open a record card → edit or cancel → return with the promised filters/selection retained. Open the card and its options, rather than inferring their spacing from the table. Exercise no matches/reset if filtering changed; exercise pending/error/retry if saving changed. A button-spacing fix checks that button in its reached states without redesigning the whole flow.
