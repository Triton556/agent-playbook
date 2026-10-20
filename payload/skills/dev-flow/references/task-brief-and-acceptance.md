# Task brief and acceptance

For a new substantial, ambiguous or multi-stage task, and for revision of accepted work. A small clear edit needs only a short record. Record placement: see [task-state, Long-task state and completeness](task-state.md#long-task-state-and-completeness).

The most expensive failure is building the wrong thing well. A result can pass every technical check and still be rejected because it lost what the user cared about. This procedure exists to catch that before the expensive work.

## 1. Recover what is known

Start from what already exists: the request in the user's words, their latest corrections, accepted versions, their own materials and earlier decisions. Read an accepted version and the user's materials directly; a summary or report about them is only a pointer. Discover technical facts yourself instead of asking. The existing implementation is evidence of current behavior, not an automatic requirement for the result.

## 2. Understand the intent

Before choosing an approach, fill in this intent card in the plan. Keep it short; an unknown field is an open question, not a guess.

- **Outcome.** What the user wants to have, do or feel when this is done, in the user's words. Why, and for whom.
- **Whose material is the basis.** When the user supplies their own draft, text, order, design or world, that material is the basis. Keep its structure, order, voice and content. Your changes are proposals: list them separately, each with its reason, and let the user choose. Do not silently reorder, shorten, merge or replace the user's material.
- **What already works.** For a revision of accepted work, list what made it accepted. Include the personal and playful parts, not only the technical ones: lore, references to the user's life, easter eggs, in-jokes, recognizable places, living motion, the overall mood. Ground each item in the user's words or in your own inspection of the accepted version. Every item becomes a preservation criterion.
- **Scale of change.** Match the size of the change to the request. "Improve" or "rework" does not mean "rebuild from scratch". Propose a larger restructuring with its reasons before doing it.
- **How it could fail.** Name the three most likely reasons the user would reject the result, judged by what the user values rather than by what is easy to measure. Each one becomes a distinguishing check.
- **Open decisions.** Choices that would change the product, the experience, the style or the scope.

Example: The user asks to rework an accepted world map into voxels. "Keep the atmosphere" is too vague to protect anything. Useful entries are: "people, animals and water move; each land has a clear meaning; the lore section and the easter egg stay discoverable; new assets fit the theme of their land." Likely rejection: "the world looks dead, cluttered and meaningless, even though the assets look better."

Example: The user shares a raw essay draft and asks what could be made from it. The basis is their order and thoughts. Show what their structure already does well, then offer changes as separate options: "move X before Y because ...". Do not answer with your own composition that starts elsewhere.

## 3. Ask only what changes the work

Before asking, check: which next step or which part of the result changes depending on the answer? If none, decide yourself and state the assumption.

Initiate questions yourself when an unknown choice materially changes the goal, experience, style or scope. Applicable themes: audience and goal; scenarios and content; actions, errors and recovery; style and examples; device, scale and constraints; what to preserve and when the result is sufficient. Make taste concrete through examples and observable features.

Run short rounds of related questions; answers determine the next round. There is no fixed number of questions. After each round, save the material answers, decisions and open issues. A critical question waits for an answer or for an explicit delegation of the choice; silence is not an answer. A recommendation becomes a decision only after explicit acceptance (“as recommended” counts). Ask an unanswered question again briefly; never record non-objection as acceptance. Continue independent work meanwhile. If the user limits the interview, record the permitted assumptions.

### How to run the rounds

1. **Restate first.** In one or two sentences say what you understood: what should exist or change, and for whom. If the user corrects you, restate again before asking anything else.
2. **Collect facts yourself.** Read files, code, earlier decisions and the conversation. Never ask the user what you can look up: the framework in use, where a file is, the current behaviour.
3. **List the open decisions.** Check these points and write down each one that is still open and would change the work: goal and audience; what "done" looks like to the user (a screen, a passing check, a file, a number); scope and what must not be touched; existing material and earlier decisions to build on; constraints (stack, platform, design system, performance, deadlines, budget); irreversible actions (deleting, publishing, pushing, sending, spending, migrating data); priorities when quality, speed and scope conflict.
4. **Order them as a tree.** Some decisions depend on others: the file format matters only once you know there is an export at all. A round contains every open decision that can be answered now, that is, every one that does not wait for another open answer. Dependent questions go to a later round.
5. **Ask the round** in this format, in the user's language:

   ```
   **Q1 - <short title>:** <question with concrete options>
   ➡️ Recommended: <your answer and a one-line reason>

   **Q2 - <short title>:** <question>
   ➡️ Recommended: <your answer>
   ```

   Keep a round readable: if more than about five questions are open at once, ask the ones that change the work most and move the rest to the next round. That limits the size of a round, not the number of rounds.
6. **Update and repeat.** Record the answers; settled decisions unblock the ones that waited for them. Ask the next round. Stop when no open decision would change the work, then play back (section 4).

Example. Request: "Add an export button to the expenses dashboard." Restate: "You want to download the expenses shown on the dashboard and work with them in a spreadsheet. Right?" Facts collected without asking: the dashboard is React, the table is built from `src/data/expenses.ts`, filters live in `src/components/Filters.tsx`.

Round 1:

```
**Q1 - What to export:** only the rows that match the current filters, or all expenses?
➡️ Recommended: the filtered rows, since that is what you see when you press the button.

**Q2 - Format:** CSV or an Excel file?
➡️ Recommended: CSV; it opens in Excel and Google Sheets and needs no new library.
```

The user answers "as recommended". A decision that waited for Q2 opens. Round 2:

```
**Q3 - Excel in Russian:** should the file open correctly in Russian Excel by double click (`;` separators, decimal commas)?
➡️ Recommended: yes, format for Russian Excel.
```

## 4. Play back before expensive work

Before the first expensive step, and at the start of a discussion answer about the user's own material, state your understanding briefly:

> You want X for Y. I keep Z, and your A stays the basis. I will change B. I will not do C. Success means D, which I will check by E. Open: F.

This lets the user correct a wrong interpretation while it is cheap. It is a check of understanding, not an extra approval step: continue within the agreed scope unless a critical point is open.

## 5. Two decisions about how to work

In the closing part of the initial interview, select separately:

1. **The user's participation:** each meaningful iteration / first coherent sketch to correct direction, then autonomous refinement / fully autonomous. At a human checkpoint, show the version, what to assess and its limitations; dependent expensive work waits for the answer. Make minor technical fixes within a stage yourself. A material change of accepted direction requires alignment.
2. **Separate reviewer:** none / one final pass / agreed stages. Explain the benefit and additional cost; record the user’s explicit choice, scope, stages and round limit. Autonomy does not select a reviewer. Launch approval: see [agent-sessions, step 5](../../agent-sessions/SKILL.md#5-get-approval-with-a-summary); rounds and independence: see [independent-review, After the report](../../../workflow/independent-review.md#after-the-report).

On continuation, reuse the saved choice. Recommend self-checks for ordinary text and discussion; for engineering, name the concrete risk that a second view would address. Author technical and substantive checks apply in every mode.

## 6. One task basis

Required task content belongs in the existing project format; placement and relationships: see [task-state, Long-task state and completeness](task-state.md).

- **Grounds:** the request and exact sources, answers and latest decisions, and the intent card. Separate interpretation, assumptions and delegated choices. Deliverable, mandatory outputs, audience and context, style, preservation and boundaries.
- **Execution:** next verifiable steps and their dependencies, with each step's result. Refine distant steps as evidence arrives. Discover an unknown command before running it.
- **Acceptance:** each material criterion with its grounds, mandatory or optional status, the state or action and expected observable result, and a sufficient verification method; later add the version, evidence and outcome. Preservation items from the intent card are criteria. For a critical property, name a plausible failure the check must reject, starting with the rejection reasons from the intent card.

Criterion or file counts do not measure completeness. Requirements connect function, meaning, style, context, important edge cases and preservation within the task scope. Check the source directly: your own 2D view, preflight or test can be wrong. Before an expensive new decision, a cheap coherent representation is enough; verifying it refines the same basis. The human-perspective protocol owns observation details; task-state owns the machine-state format.

## 7. Execution, verification and completion

One current observation may support several criteria when version, conditions, modality and required independence suffice for each. Reuse sufficient unchanged evidence rather than repeating a pass because another skill names it; freshness is governed by quality-ledger, Schema version 1.

Recovery: see [WORKFLOW, Work route](../../../workflow/WORKFLOW.md#work-route). After a stage, update the current result and material decisions; history: see quality-ledger, Schema version 1.

The author checks the current version and follows the selected human checkpoints. Independent review method: see [independent-review](../../../workflow/independent-review.md). Evidence grades: see [human-perspective-review, Readiness and transfer](human-perspective-review.md#readiness-and-transfer).

A defect adds a distinguishing check; criterion changes retain their grounds. Do not remove a general criterion just to obtain a pass. Evidence history: see [quality-ledger, Schema version 1](quality-ledger.md#schema-version-1). Repairs: see [WORKFLOW, Work route](../../../workflow/WORKFLOW.md#work-route). Scope changes: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

Done means mandatory outputs exist, material criteria have current supporting evidence, preserved qualities remain, and discovered material defects are closed. A critical gap leaves the result partial/blocked. Unperformed checks: see [human-perspective-review, Readiness and transfer](human-perspective-review.md#readiness-and-transfer). Further rounds: see [WORKFLOW, Work route](../../../workflow/WORKFLOW.md#work-route).
