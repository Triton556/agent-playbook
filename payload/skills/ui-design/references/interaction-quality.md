# Interaction: expectation, response and recovery

Open while designing/checking a main action, states, form, table, filters or complex working UI. Load only the applicable branch. Accepted design and target device outrank recommendations; desktop work does not become mobile by default.

## Action and data contract

For a material action, record in the existing plan: **action → user expectation → visible accessible response → confirmed result → recovery → preservation → verification**. Before detail, check the main screen/action with a simple representation; a clear small edit can reuse the accepted basis.

| State | What must be clear |
| --- | --- |
| Waiting | Action was accepted, what is happening, how to continue/cancel when supported; percentages/deadlines have grounds |
| Actual zero | What was measured, period/sample and meaning of zero |
| No measurement / unknown | Why the value is unknown; never substitute zero. The contract defines NULL, not one universal interpretation |
| No matches | Applied conditions and a way to relax/remove filters are visible |
| Error / stale result | Do not present it as a successful empty response; clear cause/next step, preserved work and freshness label |
| Success | Result is distinguishable; extra notification only when useful for noticing it/recovering context |

Align units, denominators, rounding, selected scenario, counts and conclusions. An identifier needs no denominator; a proportion does. Filtering updates dependent charts/labels/conclusions, and a late response must not replace a newer one. Persisted settings have a clear scope and way to restore defaults.

## Input and errors

- Show labels, required status and rules before entry; placeholder is not the only instruction. Remove unjustified fields while preserving sufficient data. The task determines field count and wizard steps.
- Preserve input on error. Validation respects interaction and input completeness; tabbing through an untouched form should not create a queue of red errors. Password assistance while typing may be useful.
- An error names the problem and correction, accessible near the action/field; a linked summary suits long forms. Do not clear successful fields. Normalize format only while preserving meaning; server contracts remain mandatory.
- Clearing data, canceling, resetting filters and restoring a default view are different operations. Loss cost determines undo/confirmation; do not require confirmation for every harmless action.

## Tables, filters and dense desktop UI

- Align text/comparable numbers by meaning; tabular numerals have equal width without requiring a monospace font. Short statuses/checkboxes may be centered.
- Show selection boundaries, active filters, result count and removal of conditions. Bulk actions make scope clear, including selections beyond the page. No matches is not absence of all data.
- Freeze, resize, reorder, density changes and command palettes are accelerators when useful for the task/frequent user; they do not replace a clear initial view and ordinary path.
- Actions are discoverable and usable without hover; important controls cannot exist only on hover. Present detail in a way suited to data amount and context preservation; there is no universal tooltip/modal/sidebar hierarchy.
- Provide orientation for deep navigation according to the task. Success, errors, returns and effort matter more than a fixed click count.

## Graphics, motion and waiting

Length/position support precise comparison; choose charts by question. Color can encode another quantity, but values/labels/another channel also convey the content. An exploratory dashboard is valid when overview, comparison and detail have clear transitions.

Response matches the operation. 0.1/1/10 seconds are heuristics, not one SLA for every action. When percentage is unknown, show stages/measured volume or an indeterminate indicator. Skeletons match future structure; they are not mandatory after a universal threshold. Optimistic changes suit only controlled reversibility/errors. Sound/micro-motion should be restrained and disableable; honor reduced motion.

## How to verify

In the actual target window, perform the main scenario and risk-relevant failure/recovery. Check available keyboard paths, focus, preserved inputs/conditions and data consistency. For asynchronous UI, check slow/failed responses and changing conditions. A still image does not measure latency or establish the user's emotion.

Acceptance: scenario completes, result is visible/correct, material errors are recoverable within stated bounds, and current evidence covers the latest changes. Unperformed checks remain unverified.

Sources: [NN/g response times](https://www.nngroup.com/articles/response-times-3-important-limits/), [long waits](https://www.nngroup.com/articles/designing-for-waits-and-interruptions/), [forms](https://www.nngroup.com/articles/errors-forms-design-guidelines/), [three-click rule](https://www.nngroup.com/articles/3-click-rule/); W3C [keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [status messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html), [use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). Applicability and qualifications remain in ui-perception-integration.md rather than a universal beauty score.
