---
name: kb-save
description: Save new useful knowledge from the user's current conversation to the file-based INBOX with its source, evidence and status.
---

## Knowledge capture

PC vault: `{{MEMORY_ROOT}}`. In Cloud, use the verified copy of the designated curator's repository.

Read SYSTEM/workflows/capture.md only on first use or when the procedure changes. Save short records yourself; a substantial summary may use one memory agent only with the current installation owner's consent under AGENTS.md. The same workflow defines handoff and verification; delegation is optional. Prepare concise JSON of new knowledge using its schema. On PC, prefer available and authorized `harness_kb_writer` tools: `kb_capture({payload})` or `kb_checkpoint({session_id,turn_id})`. Persistent tool access requires the current owner's actual approval. If absent from this chat's tool catalog, use the existing CLI through stdin: `node SYSTEM/scripts/kb.mjs capture` from the vault, respecting current filesystem permissions. In PowerShell, use an object → ConvertTo-Json → stdin; never interpolate user text into shell code. From another directory, use the script's absolute path.

Use real hook-provided identifiers; give a new stage a new batch_key and reuse the previous key for a retry. If the user prohibits saving content or there is no new knowledge, checkpoint without saving content. Confirm persistence using a successful receipt and an existing file. Transport: see [kb-sync, Knowledge transport](../kb-sync/SKILL.md#knowledge-transport). Curation: see [kb-curate, Knowledge curation](../kb-curate/SKILL.md#knowledge-curation). Language defaults: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

## Delegated work

Assign one writer per knowledge set: normally the orchestrator captures and workers only checkpoint when their own hooks require a turn mark. State a different assignment explicitly when needed.

For an authorized memory helper:
- Give only relevant facts, decisions, evidence and limits, with the original source.kind, session_id, turn_id and batch_key; never substitute the helper chat identity. Prefer a concise task without full history.
- The assigned helper captures with final:false and returns command output, ID and an existing path. Its own required turn mark is a checkpoint without duplicate facts.
- The orchestrator verifies receipt and file existence, then checkpoints the original turn if no further knowledge remains. New knowledge uses a separate batch_key. After failure, check for an existing record before retrying the same identity.
- Consent, access and saving prohibitions follow AGENTS; transport follows kb-sync, Knowledge transport.
