# Shared human-perspective protocol

## Quick start: look at it as the user will

Do this before reporting any result a person will see, read or use. It takes minutes and catches what technical checks miss.

1. **Open it the way the user will.** The user's device and window size, normal speed, real content. For motion, watch it move; for text, read it from the top.
2. **First impression.** In the first 10–20 seconds, before reading your own notes, write down what you recognize, what feels alive or dead, what is confusing and what works.
3. **Side by side.** Compare with the accepted version, the user's own material or the reference in the same view. Check every item on the intent card's "what already works" list: is it still there and still discoverable?
4. **The user's three likely objections.** Take the rejection reasons from the intent card and check each one directly. Add any new one your first impression revealed.
5. **Report honestly.** Separate what you saw yourself, what tests confirmed and what only the user can judge. A count of passed checks is not a quality claim.

The rest of this document is the detailed method behind these steps.

## Detailed method

Apply to a created/changed result a person must recognize, understand or use. For a small edit, check the affected part; for a series, inspect a representative, edge cases and discovered error classes. This method supplements specialist checks; it does not prescribe identical views, pixels, realism or interfaces for every artifact.

## Inputs and four criteria

From the request, accepted decisions and examples, establish the viewer/user, goal, prior knowledge, attention mode, device/scale/pace, interaction and cost of error. Reuse known facts; state material unknowns instead of inventing a persona. Before creating, inspect the original feedback and named materials.

| Criterion | What must be observable |
| --- | --- |
| Style | Agreed concrete features of character, voice, simplification and composition are preserved |
| Context | Scale, environment, era, data, platform and relationships fit the task conditions |
| Clarity | The object, conclusion or action reads correctly at the target presentation without the author's explanation |
| Use | Function, controls, result and recovery work; for a static file, its actual purpose/export |

Give a reason for an inapplicable criterion. Detail, decoration and realism are separate decisions, not universal quality improvements.

## Subject-specific acceptance basis

Use the task and inspected primary materials to identify features that distinguish the required result from something merely plausible. An agreed design intent can ground an original decision; reproducing a fact requires a source. Compare the cheap initial basis against these grounds: your own mockup, 2D view, retelling or successful test can also be wrong.

For each material property, fill in the existing acceptance program:

**Grounds → expected feature/relationship → state and action → what stays and what changes → verification method.**

Also identify a distinguishing failure: which plausible but incorrect state must the check reject? Choose the list by purpose and risk; item count does not measure completeness. An independent reviewer may refine features directly from sources while preserving original requirements.

Check not only absence of interference but also presence, membership and preservation of what is needed: a part, context, relationship, value, argument or available action. After a state change, compare expected changes and invariants. Follow the inspection sequence below.

## Preservation during revision

Preservation criteria: see [task brief and acceptance, section 2](task-brief-and-acceptance.md#2-understand-the-intent). Inspect the accepted version to construct observable comparison scenarios for those criteria.

For each criterion, record what is recognized/understood, the action and received result. Compare its transfer in the new version against actual evidence; a saved baseline supports rollback.

Preservation authority: see task brief and acceptance, section 2. Example: "decorative motion must not pose as a live project event" limits how motion is labeled; it does not justify deleting people, animals or water that made the accepted world feel alive. When a rule and an accepted quality conflict, keep the quality, adjust its presentation, and state the conflict.

For user-authored material, compare section by section and list removed, moved or rewritten parts under the preservation criteria.

Check preservation across a coherent segment of experience: a clear interface transition, a video sequence's rhythm, a document's argument, a system request's result or an action in a spatial scene. For a small edit, the affected property and its dependencies suffice; rechecking the entire system is unnecessary.

## Inspection sequence

1. **First reading.** Receive the minimum viewer brief and the artifact; record what is recognized, what the action promises, what feels strange and what works. Add author explanations and the prepared defect list afterward. On a recheck, the original finding is available. An author who knows the construction calls this pass self-checking.
2. **Direct comparison.** After first reading, refine the subject basis from the task and primary materials. For a critical property, directly compare relevant source/result areas side by side or sequentially with retained viewpoint/context and criterion. Record a concrete match or difference in form, composition, material, meaning or behavior. Cover distinguishable sides and material states; one successful fragment does not cover the rest. General similarity and memory of an example do not suffice for a specific pass. An unsuitable source view/scale creates a gap and targeted research, not a guess.
3. **Change boundaries.** For a material action, establish from evidence exactly what is affected and what around it must remain. Compare before, during and after: membership of the changed set, its complete meaningful boundaries, neighboring context and required relationships. Supplement the correct class of action with a check of the correct extent/composition of its consequences. Observe motion at normal speed and across transitions. Diagnose with a close-up, data or measurements; assess impact at the target presentation.
4. **Interpretation.** Separate what is visible, the predicted human reaction and the cause. “Looks like a carpet” is an observation/association, not a proven geometric cause. Perspective and multiple views do not replace sufficient measurements. When the result reads incorrectly, investigate form, material, light, viewpoint, occlusion, behavior and information presentation.
5. **Assessment against intent.** Prioritize harm to the goal, function, recognition and style under the user's conditions. Silhouette → recognition → relationships → color → details is a useful object heuristic, not a law for every modality. Deliberate asymmetry/emptiness/simplification is allowed. There is no defect quota; preserving a successful result is a valid outcome.
6. **Repair and regression.** Transition: see [WORKFLOW, Work route](../../../workflow/WORKFLOW.md#work-route). Recheck affected character, preserved qualities, actions, relationships and protected examples in their new integration.

A check must distinguish subject-specific errors. Absence of intersections in a moving part does not prove correct membership; compare action boundaries with the source. In UI check retained elements/data; in text check surviving meaning/conditions. If the method cannot distinguish a property, record the gap and use the selected human checkpoint. Actual feedback corrects current status without rewriting the earlier report. Further rounds: see WORKFLOW, step 6.

Group repetitions into a class with affected instances and a representative check. A shared cause stays hypothetical until confirmed; many small repetitions are not automatically a critical defect.

## Finding card

Object/version · location and visibility conditions · observation · expected/possible reading · grounds (goal/style/example/feedback) · type (defect/risk/option/acceptable) and impact · cause (confirmed/hypothesis/unknown) · correction · **preserve** · verification · current result.

One short observation suffices for a small edit. Connected human-readable feedback and a structured record can share the same grounds. Praise or a human tone does not make a diagnosis more reliable.

## Adaptation by medium

| Result | Actual verification |
| --- | --- |
| UI | Main action → visible accessible response → confirmed result → recovery; required context is preserved and related states agree. Use [UI interaction quality](../../ui-design/references/interaction-quality.md) for the applicable branch |
| 3D / voxel | Distinguishable views and characteristic contours/material regions; action membership/boundaries, support/contact, scale and target distance; geometric diagnosis uses separate data |
| Animation | Normal speed, intention/weight/rhythm, transitions and problematic frames; a still frame does not verify movement |
| Chart / dashboard | Data, units, scales and denominators; shared result handling: see causal-state-interaction, One model, several views; encoding: see data-spatial-metaphors, Live, snapshot, approximate, absent |
| Document / text | Reading order, conclusion and its grounds, preservation of material qualifications when shortening, voice/audience; actual rendering where layout matters |
| Audio | Listening with an available tool; a spectrum description does not establish a listener's experience |

## Readiness and transfer

Each pass claim names the property, version, conditions, verification method and concrete observation; its scope cannot exceed the evidence. If one criterion combines properties with different outcomes/modalities, separate their statuses in the existing record. Opening a card, for example, proves navigation; readability of its spatial object requires inspecting the object, and the activity's meaning requires observing action in context. Likewise, a valid video file does not verify sequence pacing, and a successful component test does not establish an end-to-end system result.

Justify no findings through coverage of critical features/states. Evidence versions: see [quality-ledger, Schema version 1](quality-ledger.md#schema-version-1). Numerical/geometric expected results: see [dev-verify, Behavior verification](../../dev-verify/SKILL.md#behavior-verification).

Record technical pass, agent inspection and human assessment separately. Test/source counts and file presence describe scope; a quality conclusion needs evidence of the named property. Human acceptance comes only from an actual response; it is not a mandatory new approval for every ordinary step. An unavailable modality stays unverified; a material semantic failure stays unready. For a ledger, use existing kind/criterion/evidence fields; no new universal format is required.

A lesson contains a trigger, confirmed observation, cause status, repair/preservation result, scope, exception and example/counterexample. Save an observation even if its cause is unknown; a technical rule needs a confirmed mechanism. Keep the active lesson selection focused and do not delete lessons; read every lesson that matches the current deliverable. This document owns the general method; specialist branches own subject rules.

Grounds: workflow-review-20261013 and workflow-human-review-20261013 documents in {{EVIDENCE_ROOT}}; Gen2.1 comparisons. Author self-descriptions and predicted reactions are not independent research. Test transfer through [workflow-pilot](workflow-pilot.md).
