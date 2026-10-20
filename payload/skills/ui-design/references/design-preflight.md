# UI design basis: scenario, style and related states

For a new flow, substantial redesign or screen series, verify the design basis before full implementation. The transfer from voxel work is a brief, consistent representations, intent verification and comparison with the result. UI representations are linked by actions, data and window adaptation; the scenario determines their number.

Use existing project design documents and mockup links. Record relationships: see [task-state, Long-task state and completeness](../../dev-flow/references/task-state.md#long-task-state-and-completeness). A separate JSON schema, Figma or image generation is not mandatory. For a small edit record its property/states/check; use the reuse conditions in task brief and acceptance, section 7. A new flow, action meaning, visual system or unverified size needs a targeted addition.

## 1. Record the scenario brief

When material requirements are ambiguous, initiate the [themed interview and saved brief/acceptance](../../dev-flow/references/task-brief-and-acceptance.md) before dependent design decisions. The scenario brief refines the same basis; reuse known answers and save new ones. Mockup verification adds properties to check later in the working UI.

From the brief, current product, relevant decisions and inspected examples, record:

| Part | Sufficient record |
| --- | --- |
| Goal and scenario | Who/why the screen serves; entry/initial data → main action → visible result and completion. [interaction-quality](interaction-quality.md) refines material transitions, failure and recovery |
| Conditions | Route/product location, target device and input; known working window area in CSS px, scale/zoom when relevant. Needed extra sizes and why; explicitly label unknowns |
| Visual system | Existing component/token references, text/color roles, density and composition principle. Preserve one system; describe a new direction with observable features |
| Grounds and preservation | Inspected references/accepted screens and transferable qualities; important decisions, reasons and sources. Identify actions, data and character that must survive |
| Verification and version | Success criteria, required representations and verification method; basis version and artifact links. Distinguish author choice, agent verification and the user's actual acceptance |

A reference grounds a particular technique; it does not replace the product scenario wholesale. Resolve a critical unknown through [reference-grounding](../../dev-flow/references/reference-grounding.md); only dependent work waits. Reuse known conditions without another interview.

For a new landing page or research dashboard, apply [accepted UI lessons](accepted-ui-lessons.md): substantive continuation after the first screen, imagery/color roles and the sequence of data explanation. Adapt them to the goal and accepted project style.

**Done:** goal, action, style, preservation and test conditions are defined; critical assumptions are visible and have a verification method.

## 2. Link screens, states and sizes

Identify a verification point as **screen/route + state + data + window size**. Keep a compact transition map/table in the existing plan: where the user came from, what they did, what changed, how to return and what remained. Cover the main uninterrupted path and risk-relevant failure/return. Add loading, empty, error, success, focus and other states according to the actual scenario.

Related states share components and semantic roles. Input/filter retention: see ui-reference, state-preservation; coupled results: see causal-state-interaction, One model, several views. Scope supported devices, themes and states explicitly in the brief. For each supported size define wrapping/collapse/availability. Representative combinations and risky boundaries suffice; exhaustive combinations require corresponding risk. A desktop scenario does not automatically get a mobile version.

**Done:** the map supports a path from entry to result/recovery; important states/sizes remain in verification and data/behavior contradictions are resolved.

## 3. Verify the mockup or prototype before full implementation

Choose the cheapest medium that can test the disputed property: sketch/wireframe for structure, styled key screen for style/hierarchy, linked or working prototype for transitions. A bounded code prototype is allowed. A rough wireframe does not verify typography; a static image does not verify working interaction. For a new visual direction, add a sufficient styled fragment; for an accepted system, use its actual components/examples.

Verify the styled fragment with representative content: actual label lengths, units/dates, required chart geometry and important illustration at target size. Replacing these with neutral placeholders leaves their readability/recognition unverified.

Observation order: see [human-perspective-review, Inspection sequence](../../dev-flow/references/human-perspective-review.md#inspection-sequence). Then assess the basis:

| Criterion | Observable evidence |
| --- | --- |
| Scenario and function | Main action is discoverable; promise and result agree; failure/return can be explained through linked states |
| Consistency | Data, components and states describe one scenario; transitions do not lose important context without cause |
| Style and context | Accepted features, content and density suit the product and target window; reference techniques help the task |
| Clarity and accessibility | Hierarchy/labels explain the action without author commentary; material keyboard/focus and responsive decisions are planned |

Repairs follow WORKFLOW, step 6. In addition, a shared design decision updates related states/sizes. Record current basis version and inspected representations; participation: see task brief and acceptance, section 5.

**Advance to full implementation:** critical mockup contradictions are resolved, the main path and needed edge cases are considered, and the design basis is saved. List properties verifiable only in working UI for later checks. A design-only request ends here; do not claim readiness of a working interface.

## 4. Compare the working UI with the basis

Pass the brief/plan, accepted mockup version, state map and preserved decisions to [ui-review](../../ui-review/SKILL.md). Compare the actual render with the basis at comparable points: identical route, state, data and size/zoom. Check hierarchy, components/tokens, density, content and main-action accessibility; assess responsive changes under the accepted adaptation rule. Automated overlays/diffs can help, but pixel equality is not a universal criterion.

Record **original design quality**, **implementation fidelity to the basis** and **actual scenario behavior** separately. Faithfully copying a poor mockup does not make UI ready. Reuse: see [task-brief-and-acceptance, 7. Execution, verification and completion](../../dev-flow/references/task-brief-and-acceptance.md#7-execution-verification-and-completion). [visual-quality](../../ui-review/references/visual-quality.md) owns the actual render/action sequence.

Classify discrepancies as transfer defects, justified adaptations or basis problems. Basis decisions update the existing plan. Evidence versions: see [quality-ledger, Schema version 1](../../dev-flow/references/quality-ledger.md#schema-version-1). Repairs: see [WORKFLOW, Work route](../../../workflow/WORKFLOW.md#work-route). Series: see quality-cycle.

When auditing existing UI without a mockup, compare current requirements, components and source screens; explicitly note the missing verified design basis. A retrospective description does not prove pre-implementation preflight. Verify current UI while leaving comparison with an absent mockup unverified.

**Done:** discrepancies are explained/fixed and current scenario/preservation checks are complete. Assessment grades: see [human-perspective-review, Readiness and transfer](../../dev-flow/references/human-perspective-review.md#readiness-and-transfer).

## Proportional application example

For a desktop table: search for a record → open its card → return with filters and selected row preserved. Basis: current design system; representations: search results, no matches/reset, card/return and applicable error. A mockup checks hierarchy/placement in the working window; a bounded prototype checks transitions. Verify working UI with actual actions on the same data/sizes. A single button-spacing fix uses the accepted basis and affected button states.
