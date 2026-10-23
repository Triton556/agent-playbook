---
name: ui-design
description: Design, implement or inspect a user interface through actual user steps, reached states and readable results. Includes review of the rendered UI.
---

# UI design and user-flow verification

The acceptance unit is a human scenario, not a test count. Use the current request and accepted project components/tokens. A design-only request ends with a clearly labelled design; it does not claim a working UI.

| Event | Action | Observable output / next step |
| --- | --- | --- |
| A new action/flow is requested or an existing action changes meaning | Write entry state → human steps → expected visible result; identify opened dialogs/menus and return paths | A compact flow map with relevant loading/error/empty/success states; use [design basis](references/design-preflight.md) |
| Only a label, spacing or other bounded property changes | Keep the accepted flow; name the affected control, state and window | Inspect that property in the real reached state, without a new concept exercise |
| The user requests alternatives or a concept choice is unresolved | Use [creative-direction](../creative-direction/SKILL.md) for that choice | A selected/delegated direction; references and sketches remain optional aids |
| A form, refresh, async operation, table or filter changes | Read its branch in [interaction-quality](references/interaction-quality.md) | Expected feedback, committed result, recovery and retained user data |
| A dialog/menu or new input mechanism is introduced | Apply [accessible interaction checks](references/accessibility.md) to its controls and focus/return path | Reachable named controls, visible focus and recoverable errors |
| The implementation is available | Open the actual route and execute the flow in [render and behavior verification](../ui-review/references/visual-quality.md#render-and-behavior-verification) | Per-step actual observations; inspect reached hidden surfaces at the user's window size |
| A step fails or text is unreadable/ambiguous | Record the step, state, expected and actual result; repair and repeat that step and its dependent path | Current observed correction, not merely a green build |
| The app/browser or required data cannot be opened | Report the blocked step and cause; distinguish implementation from observed UI | Mark the scenario unverified; do not claim visual acceptance |

## Record the scenario

Keep the map in the existing task/plan: **step → action → reached surface/state → expected result → actual observation → PASS / FAIL / NOT_RUN**. Add the target window/zoom and the data that exposes clipping, long labels or empty/error states. Include an affected modal or dropdown by opening it, not by checking its component source. Inspect hierarchy, wording, contrast, spacing, overflow and action discoverability at the reached state; a full-page thumbnail is not a detail check.

Choose expected results from the request or accepted behavior before judging the implementation. A screenshot shows a state, not that the actions work; a browser assertion shows the tested behavior, not that wording is clear. Unit/API/regression tests can support technical correctness but cannot substitute for this flow and readability inspection.

## Example: card editing and refresh

For a board whose accepted flow is inline notes:

1. Add a note → the note appears on the board, without an unexpected creation modal.
2. Type body text, with and without a title → both allowed forms remain readable and saved as specified.
3. Open its options or a related dialog → controls and text fit; focus/close/back work, and unfinished input is retained where the accepted flow promises it.
4. Refresh → pending feedback appears while the request is actually pending; repeat activation does not duplicate work.
5. Finish or simulate a supported failure → the updated result or actionable error is visible; recovery retains the relevant edit/filter state.

This is a worked example, not a requirement that every product have notes, modals or refresh. Test the changed flow's actual actions and promised outcomes. Report the passed steps, concrete defects and unperformed checks; “tests passed” alone is not a UI acceptance report.
