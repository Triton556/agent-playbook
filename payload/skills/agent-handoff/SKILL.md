---
name: agent-handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
---

## Local Codex scope

Action scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

Use only on explicit user selection. Save a uniquely named handoff in the OS temporary directory (Windows: `$env:TEMP`), outside the workspace. Include goal, completed work, current state, source paths/URLs, next steps, blockers and success criteria. Creating a handoff does not itself send it or start another agent.


Write a handoff document summarising the current conversation so a fresh agent can continue the work.

Include a "suggested skills" section in the document, naming relevant installed skills and their SKILL.md paths to read when that stage is reached.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
