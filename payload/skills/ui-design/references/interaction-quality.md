# Interaction: expectation, response and recovery

Open while designing/checking a main action, states, form, table, filters or complex working UI. Use the affected steps and states from [UI design preflight](design-preflight.md#2-link-screens-states-and-sizes).

## Action and data contract

For the changed action, record in the existing plan: **action → user expectation → visible accessible response → confirmed result → recovery → preservation → verification**. For a new flow, map the main screen/action before coding; a label or spacing edit reuses the accepted flow and checks its reached state.

| State | What must be clear |
| --- | --- |
| Waiting | Contextual response: see [interaction-quality, Graphics, motion and waiting](interaction-quality.md#graphics-motion-and-waiting). |
| Actual zero | Data encoding: see [data-spatial-metaphors, Live, snapshot, approximate, absent](../../visual-scenes/references/data-spatial-metaphors.md#live-snapshot-approximate-absent). |
| No measurement / unknown | See data-spatial-metaphors, Live, snapshot, approximate, absent |
| No matches | Applied conditions and a way to relax/remove filters are visible |
| Error / stale result | See causal-state-interaction, One model, several views; recovery follows [accessible interaction checks](accessibility.md) for actionable errors and preserved user input |
| Success | Observe a visible committed result; see [accessible interaction checks](accessibility.md) |

Align units, denominators and rounding; an identifier needs no denominator, a proportion does. Result propagation: see [causal-state-interaction, One model, several views](../../visual-scenes/references/causal-state-interaction.md#one-model-several-views). Persisted settings have a clear scope and reset path.

## Input and errors

- Controls have visible names or accessible labels, unfamiliar icons have explanations, and required fields are identified; see [accessible interaction checks](accessibility.md). Remove unjustified fields while preserving sufficient data; task context determines field count and wizard steps.
- Preserve valid input after a recoverable error; see [accessible interaction checks](accessibility.md). In addition to that rule, validation respects input completeness: tabbing untouched fields should not create a queue of errors; password assistance while typing may help.
- Errors identify the affected field and next action; focus moves predictably so the user can reach that field. See [accessible interaction checks](accessibility.md). Normalize formatting only while preserving meaning; server contracts remain mandatory.
- Clearing data, canceling, resetting filters and restoring a default view are different operations. Loss cost determines undo/confirmation; do not require confirmation for every harmless action.

## Tables, filters and dense desktop UI

- Align text/comparable numbers by meaning; tabular numerals have equal width without requiring a monospace font. Short statuses/checkboxes may be centered.
- Show selection boundaries, active filters, result count and removal of conditions. Bulk actions make scope clear, including selections beyond the page. No matches is not absence of all data.
- Freeze, resize, reorder, density changes and command palettes are accelerators when useful for the task/frequent user; they do not replace a clear initial view and ordinary path.
- Actions are discoverable and usable without hover; important controls cannot exist only on hover. Present detail in a way suited to data amount and context preservation; there is no universal tooltip/modal/sidebar hierarchy.
- Provide orientation for deep navigation according to the task. Success, errors, returns and effort matter more than a fixed click count.

## Graphics, motion and waiting

Length/position support precise comparison; choose charts by question. Color can encode another quantity, but values/labels/another channel also convey the content. An exploratory dashboard is valid when overview, comparison and detail have clear transitions.

Response matches the operation. 0.1/1/10 seconds are heuristics, not one SLA for every action. When percentage is unknown, show stages/measured volume or an indeterminate indicator. Skeletons match future structure; they are not mandatory after a universal threshold. During pending actions, expose supported continuation/cancellation and ground any displayed deadline. Optimistic changes suit only controlled reversibility/errors. Sound/micro-motion should be restrained and disableable; respect reduced-motion settings as described in [accessible interaction checks](accessibility.md).

## How to verify

Perform the main scenario at the target window. Include failure/recovery when validation, async handling or the retry/return behavior changed. When controls or dialogs changed, exercise their keyboard/focus/input paths using [accessible interaction checks](accessibility.md). Async revision checks: see causal-state-interaction, One model, several views. A still image does not measure latency or establish user emotion.

Acceptance and evidence grades: see task brief and acceptance, section 7, and human-perspective-review, Readiness and transfer.

Sources: [NN/g response times](https://www.nngroup.com/articles/response-times-3-important-limits/), [long waits](https://www.nngroup.com/articles/designing-for-waits-and-interruptions/), [forms](https://www.nngroup.com/articles/errors-forms-design-guidelines/), [three-click rule](https://www.nngroup.com/articles/3-click-rule/); W3C [keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [status messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html), [use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). Applicability: see [UI design preflight, sections 1–2](design-preflight.md#1-record-the-scenario-brief).
