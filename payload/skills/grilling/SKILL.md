---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

## Local Codex scope

User requirements, existing project formats and action permissions take precedence. Load this skill only for its stated task; it does not authorize agents, messaging, new services or security changes.

Use when the user asks to stress-test thinking or when selected through grill-with-docs. Keep the interview within the requested scope.


Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. Read relevant environment facts yourself with available tools; don't ask the user for facts you can look up. Delegation is optional and requires the user's existing explicit authorization and applicable agent rules. While investigating facts, ask independent substantial decisions; dependent questions wait for the evidence. The _new substantial decisions_ are the user's: put each to them and wait. Reuse decisions and authorization already supplied.

The session is done when the relevant decision frontier is empty and new substantial questions are resolved. Do not mechanically reconfirm an already approved decision or require a second closing approval for authorized work. Unanswered new substantial decisions and required action permissions remain prerequisites; follow all existing permission checks before acting.
