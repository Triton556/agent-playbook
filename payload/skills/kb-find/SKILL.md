---
name: kb-find
description: Find personal information, decisions, tasks and project state in the user's shared knowledge base by selectively loading relevant notes.
---

PC vault: `{{MEMORY_ROOT}}`. In Cloud, locate the actually verified repository copy described in README.

Read the short INDEX.md. If it has no exact pointer, run `node SYSTEM/scripts/kb-search.mjs "search terms" --mode current --limit 8` from the vault. Load only relevant files. For current-state questions, also check new INBOX records that have not yet been curated. Search Russian notes using appropriate Russian terms using [AGENTS language defaults]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

Distinguish HYPOTHESES and `unconfirmed` status from facts. Check the date, source and current status of a decision or task. Show conflicting versions with their evidence. Say when current data is missing; an absent record does not prove an event did not occur.

Use `--mode history` for history and canceled decisions. Relevant INBOX entries appear separately: check date and source before answering about current state. The old `kb.mjs search` remains a fallback.
