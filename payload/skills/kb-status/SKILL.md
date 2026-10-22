---
name: kb-status
description: Check knowledge persistence, pending records, synchronization and maintenance status when requested or required by active maintenance.
---

Run `node SYSTEM/scripts/kb.mjs status` in the verified vault directory. On PC this is `{{MEMORY_ROOT}}`; in Cloud determine the actual path. The command updates STATUS.md in the current copy.

Report the last capture, successful sync, INBOX count, pending_turns, unpushed commits and error. Delivery status: see [kb-sync, Knowledge transport](../kb-sync/SKILL.md#knowledge-transport). Semantic status: see [kb-curate, Knowledge curation](../kb-curate/SKILL.md#knowledge-curation). Without fetch, Git behind reflects only the last known server state. Your own copy's status cannot establish the offline PC's queue or the designated curator's schedule: check those with a separately available tool. Language defaults: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).
