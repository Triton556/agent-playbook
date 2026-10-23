---
name: kb-save
description: Save new reusable knowledge to the configured vault INBOX; skip duplicates and empty notes.
---

# Save knowledge

Vault: {{MEMORY_ROOT}}; in Cloud use its verified file copy. The portable [capture contract](../kb-common/references/capture.md) defines the JSON schema, identity and exact commands. Read it for capture, not other KB operations. For a new/unfamiliar vault, read [layout](../kb-common/references/layout.md).

Extract new facts, decisions with reasons, tasks or sourced findings. Keep evidence and status; save hypotheses as unconfirmed. Use one writer for a knowledge set. Capture directly unless the user explicitly assigns a helper.

Use available authorized `harness_kb_writer.kb_capture`, otherwise pass JSON through stdin to `node SYSTEM/scripts/kb.mjs capture` in the vault. In PowerShell use an object converted to JSON, not user text interpolated into shell code. Preserve source/batch identity on retry and check an existing record first.

Success is a returned ID and an existing file. It is local persistence, not proof of GitHub delivery. Checkpoint without content only if configured hooks require a turn mark. Saving does not launch curation or synchronization; these follow the user's separate request or configured schedule.
