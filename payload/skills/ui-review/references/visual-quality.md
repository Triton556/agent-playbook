# Impeccable: inspection and refinement

Use after UI implementation/change and for requested visual review. Deliver findings for review-only; repair them yourself for authorized refinement. Checks are scoped to the affected surface and user criteria. The complete upstream toolkit remains in [vendor/impeccable](../vendor/impeccable/INSTRUCTIONS.md), including detector and specialist references; this adaptation owns orchestration.

## Tools and context

For context, use the local wrapper that returns only project facts:

```powershell
& '{{HARNESS_ROOT}}/skills/ui-review/scripts/impeccable-context.ps1' -TargetPath '<source-file-or-route>'
```

When toolkit project facts are needed, run once per surface/session from the project root; do not recollect sufficient context already available. The wrapper excludes upstream mandatory interview/subagent directives; local rules apply. Do not call raw `context` for workflow instructions. If unavailable, read existing project documents/components and continue through an available browser; report unperformed automated analysis. Creating a missing PRODUCT.md or introducing DESIGN.md is not a prerequisite. Existing project conventions outrank toolkit formats.

Load Impeccable references selectively:

| Observable need | Reference in vendor/impeccable/reference/ |
| --- | --- |
| General aesthetic critique, hierarchy, coherence | [local critique](critique-adapted.md), craft-floor.md |
| Final polish of an agreed design | polish.md |
| Errors, forms, long text, i18n, edge cases | harden.md, clarify.md |
| Responsive / accessibility / technical audit | adapt.md, audit.md; native variant for native UI |
| Typography / spacing / motion / speed | typeset.md / layout.md / animate.md / optimize.md |
| Complex creation/redesign of a visual world | new-work.md; local rules replace interview/delegation procedures |

Upstream references include extra roles, questions and hooks. They do not expand the task: work as the current single agent, reuse accepted decisions and introduce no repeat interview or automatic hooks. One-agent self-checking is not independent review.

## Render and behavior verification

Use the [shared protocol](../../dev-flow/references/human-perspective-review.md) for first reading, interpretation and preservation of character. Record viewer conditions and observations before author explanations; do not call your own review independent. Check style, context, clarity and use through concrete observations. [Interaction-quality](../../ui-design/references/interaction-quality.md) refines states/forms/tables/filters; test result accessibility and recovery through actual actions.

1. Launch the app normally and open the actual changed route. Account for console/network errors and asset/font loading. Wait for stable screenshot state; entrance animation must not hide content. Prefer an available browser/CUA; use Playwright when available and appropriate. Follow the chosen tool's rules.
2. Capture and actually inspect the changed surface at brief-defined sizes, including the user's actual window area when known. Check desktop and mobile when both supported modes are in scope; begin with desktop for a desktop dashboard and affected states for a narrow fix. Do not judge details from a reduced full-page thumbnail: use crops/regions. For spatial objects, choose the functional face and necessary independent views; the same angle before/after is not two directions. Bind inspected images to the actual revision, camera/scale and marked states.
3. When a mockup exists, compare its saved version with the actual render at comparable state, data and size/zoom under [UI design preflight, stage 4](../../ui-design/references/design-preflight.md#4-compare-the-working-ui-with-the-basis). In the same pass, perform the main uninterrupted scenario: actions, transitions, forms, observable result and applicable failure/recovery. Check relevant loading/empty/error/success states, keyboard/focus and reduced motion. Check overflow, text scale, contrast, hierarchy, spacing, preservation and reference/brief fit. Distinguish basis defects from transfer defects; do not replace an absent mockup with retrospective approval.
   If important human illustrations appear, actually inspect faces, poses and contacts at presentation size; enlarge suspicious areas too. Compare visible eye count/placement and facial features with viewpoint and accepted stylization: profile, closed eyes and intentional simplification are valid; unintended “cyclops” recognition requires a fix or new visual decision. After repair, recheck the entire section at working size. File format or automated pass does not replace this inspection.
4. When a detector can resolve a specific technical/stylistic question, run it on the affected source or URL; it is not a mandatory second audit of every substantial web edit. Check argument format with `detect --help`:

```powershell
& '{{HARNESS_ROOT}}/skills/ui-review/vendor/impeccable/scripts/impeccable.cmd' detect '<target>' --json
```

The detector is supporting evidence, not the brand's judge. Distinguish a mechanical defect, stylistic recommendation and deliberate project decision. Do not replace mandated Inter, palette, logo or content to reach a zero count. Skip the HTML/CSS detector for native UI with an explanation; use a simulator/emulator or available native render.
5. List material defects briefly and repair them as one coherent batch. Repeat affected screenshots, scenarios and checks. The usual budget is initial inspection plus confirmation after repairs. If a material defect remains, pursue a new concrete hypothesis within the agreed budget or state the blocker honestly; a polish limit does not turn failure into success.

## Readiness

User criteria are met, the main scenario checked, material discovered defects fixed, screenshots inspected and applicable checks passed after the latest changes. Without rendering, label the result “implemented, visually unverified,” not production-ready. Do not require extra rounds for taste alternatives after completed acceptance.
