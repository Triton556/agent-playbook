---
name: stress-test
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

## Local Codex scope

Action scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

Use when the user asks to stress-test thinking or when selected through stress-test-with-docs. Keep the interview within the requested scope.


In addition to [task brief and acceptance, section 3](../dev-flow/references/task-brief-and-acceptance.md#3-ask-only-what-changes-the-work), this explicitly selected challenge uses the frontier variant below. Map this as a **design tree**: every decision branches into the decisions that hang off it.

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

Fact gathering and material choices: see [task-brief-and-acceptance, 3. Ask only what changes the work](../dev-flow/references/task-brief-and-acceptance.md#3-ask-only-what-changes-the-work). Delegation boundaries: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

The session is done when the relevant decision frontier is empty and new substantial questions are resolved. Do not mechanically reconfirm an already approved decision or require a second closing approval for authorized work. Unanswered new substantial decisions and required action permissions remain prerequisites; follow all existing permission checks before acting.
