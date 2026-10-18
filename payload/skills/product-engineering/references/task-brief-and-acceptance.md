# Task brief and acceptance

For a new substantial, ambiguous or multi-stage task, and for any revision of work the user has already accepted. A small clear edit needs only a short record. Use the existing plan. This is the current agent's procedure and does not launch another agent.

The most expensive failure is building the wrong thing well. A result can pass every technical check and still be rejected because it lost what the user cared about. This procedure exists to catch that before the expensive work.

## 1. Recover what is known

Start from what already exists: the request in the user's words, their latest corrections, accepted versions, their own materials and earlier decisions. Read an accepted version and the user's materials directly; a summary or report about them is only a pointer. Discover technical facts yourself instead of asking.

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

Run short rounds of related questions; answers determine the next round. There is no fixed number of questions. After each round, save the material answers, decisions and open issues. A critical question waits for an answer or for an explicit delegation of the choice; silence is not an answer. Continue independent work meanwhile. If the user limits the interview, record the permitted assumptions.

## 4. Play back before expensive work

Before the first expensive step, and at the start of a discussion answer about the user's own material, state your understanding briefly:

> You want X for Y. I keep Z, and your A stays the basis. I will change B. I will not do C. Success means D, which I will check by E. Open: F.

This lets the user correct a wrong interpretation while it is cheap. It is a check of understanding, not an extra approval step: continue within the agreed scope unless a critical point is open.

## 5. Two decisions about how to work

In the closing part of the initial interview, select separately:

1. **The user's participation:** each meaningful iteration / first coherent sketch to correct direction, then autonomous refinement / fully autonomous. At a human checkpoint, show the version, what to assess and its limitations; dependent expensive work waits for the answer. Make minor technical fixes within a stage yourself. A material change of accepted direction requires alignment.
2. **Separate reviewer:** none / one final pass / agreed stages. Explain the benefit and the additional cost; record scope, stages and round limit. No launch without explicit consent, including during autonomous development. A repair does not automatically create another round.

On continuation, reuse the saved choice. Recommend self-checks for ordinary text and discussion; for engineering, name the concrete risk that a second view would address. Author technical and substantive checks apply in every mode.

## 6. One task basis

Save in the existing plan, in the project's format; a separate JSON schema is not required.

- **Grounds:** the request and exact sources, answers and latest decisions, and the intent card. Separate interpretation, assumptions and delegated choices. Deliverable, mandatory outputs, audience and context, style, preservation and boundaries.
- **Execution:** next verifiable steps and their dependencies, with each step's result. Refine distant steps as evidence arrives. Discover an unknown command before running it.
- **Acceptance:** each material criterion with its grounds, mandatory or optional status, the state or action and expected observable result, and a sufficient verification method; later add the version, evidence and outcome. Preservation items from the intent card are criteria. For a critical property, name a plausible failure the check must reject, starting with the rejection reasons from the intent card.

Criterion or file counts do not measure completeness. Requirements connect function, meaning, style, context, important edge cases and preservation within the task scope. Check the source directly: your own 2D view, preflight or test can be wrong. Before an expensive new decision, a cheap coherent representation is enough; verifying it refines the same basis. The human-perspective protocol owns observation details; task-state owns the machine-state format.

## 7. Execution, verification and completion

At a new stage, on context recovery and at acceptance, read the current basis, state and relevant criteria; do not reconstruct the specification from all previous reports. After a stage, update the current result and material decisions. Keep failure history accessible by reference.

The author checks the current version and follows the selected human checkpoints. An agreed independent review uses its separate procedure and sufficient available tools. Neither an automated pass nor a predicted reaction is human acceptance.

A defect adds a distinguishing check; preserve the initial failure and the reason for any changed criterion. After a repair, repeat the affected checks and their dependencies; reuse unchanged evidence when its independence is established. Do not remove a general criterion to obtain a pass. A new product goal requires agreement; ordinary verification of an existing requirement is within scope.

Done means the mandatory outputs exist, material criteria have current supporting evidence, preserved qualities are still present, and material discovered defects are closed. A critical unverified requirement leaves the result partial or blocked; state any acceptable limitation explicitly. Unperformed checks stay unverified. Another round requires a new signal, change or hypothesis; a completed checklist does not close an observed failure of the goal.
