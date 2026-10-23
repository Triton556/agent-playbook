# Inspection and refinement

This is the actual-render/action procedure selected by [ui-design](../../ui-design/SKILL.md) after implementation or for an audit of an existing UI. Use the current accepted behavior and changed flow; do not launch a separate reviewer.

## Render and behavior verification

1. Open the real application route with the scenario's data and target window/zoom. Check that assets/fonts have loaded and record blocking console/network errors. A source file or screenshot of an older revision does not establish the current result.
2. Perform the human steps in order. Open affected menus, dialogs, popovers and expanded sections. At each reached state, record the expected result and actual observation. Check return/close paths and preservation of the user's unfinished input, filters or selection against the accepted behavior.
3. Inspect the reached surface at its working size: readable text, understandable labels, visible action, hierarchy, spacing, overflow and clipping. Use a crop/region when a full-page thumbnail cannot resolve a detail. Exercise keyboard/focus where that interaction changed; an image cannot prove focus behavior.
4. For a pending operation, observe visible loading feedback and the resulting success/error. For changed validation/recovery, execute the invalid/failed path and retry. Empty/no-results states are different from loading or missing data. Use controlled fixtures or a supported failure path; label states that could not be produced.
5. If a design basis exists, compare the same route/state/data/window with it. Record whether a mismatch is an implementation defect, an agreed adaptation or a problem with the basis itself. A faithful copy of an unreadable mockup still fails readability.
6. Fix observed defects within the task scope and rerun their steps plus dependent transitions. Do not replace an unperformed action with a passing build or a source assertion. Repeat the whole flow after a shared state/navigation change that can affect its later steps.

Use an available browser/CUA or an appropriate browser test tool under its actual permissions. Automated checks support the recorded observations; do not infer emotion, readability or success of unexecuted steps from them. Important illustration faces/poses/contacts must be inspected at their displayed size when those illustrations changed; record the observed defect rather than adding a universal illustration checklist to unrelated screens.

## Readiness

Report the flow and its step results: PASS, FAIL or NOT_RUN, with concrete observations and the checked revision/window. UI acceptance requires the requested path and changed states to be observed, readable and free of discovered material defects. If rendering or interaction was unavailable, say “implemented, UI flow unverified” and name the missing step. Do not claim human acceptance from your own inspection.
