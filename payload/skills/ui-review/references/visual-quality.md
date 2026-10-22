# Inspection and refinement

Inspect the changed surface against the agreed criteria; repair only within authorized scope. Reuse project context and prior sufficient evidence.

## Render and behavior verification

Inspection method: see [human-perspective-review, Inspection sequence](../../dev-flow/references/human-perspective-review.md#inspection-sequence). [interaction-quality](../../ui-design/references/interaction-quality.md) supplies contextual actions/states.

1. Launch the app normally and open the actual changed route. Account for console/network errors and asset/font loading. Wait for stable screenshot state; entrance animation must not hide content. Prefer an available browser/CUA; use Playwright when available and appropriate. Follow the chosen tool's rules.
2. Capture and actually inspect the changed surface at brief-defined sizes, including the user's actual window area when known. Check desktop and mobile when both supported modes are in scope; begin with desktop for a desktop dashboard and affected states for a narrow fix. Do not judge details from a reduced full-page thumbnail: use crops/regions. For spatial objects, choose the functional face and necessary independent views; the same angle before/after is not two directions. Bind inspected images to the actual revision, camera/scale and marked states.
3. Basis comparison: see [design-preflight, 4. Compare the working UI with the basis](../../ui-design/references/design-preflight.md#4-compare-the-working-ui-with-the-basis). In the same actual-render pass perform the uninterrupted scenario, transitions, forms and failure/recovery. Check overflow, hierarchy, spacing and fit.
   If important human illustrations appear, actually inspect faces, poses and contacts at presentation size; enlarge suspicious areas too. Compare visible eye count/placement and facial features with viewpoint and accepted stylization: profile, closed eyes and intentional simplification are valid; unintended “cyclops” recognition requires a fix or new visual decision. After repair, recheck the entire section at working size. File format or automated pass does not replace this inspection.
4. Use a targeted automated check only when it distinguishes a concrete risk; report checks that could not run.
5. List material defects as one coherent batch. Repair/recheck transition: see [WORKFLOW, Work route](../../../workflow/WORKFLOW.md#work-route). Use the agreed inspection budget and report any remaining blocker.

## Readiness

User criteria are met, the main scenario checked, material discovered defects fixed, screenshots inspected and applicable checks passed after the latest changes. Without rendering, label the result “implemented, visually unverified,” not production-ready. Do not require extra rounds for taste alternatives after completed acceptance.
