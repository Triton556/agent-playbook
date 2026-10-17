---
name: kb-save
description: Save new useful knowledge from the user's current conversation to the file-based INBOX with its source, evidence and status. Write the knowledge in Russian.
---

PC vault: `{{MEMORY_ROOT}}`. In Cloud, use the verified copy of the designated curator's repository.

Read SYSTEM/workflows/capture.md only on first use or when the procedure changes. Save short records yourself; a substantial summary may use one memory agent under the user's standing permission in AGENTS.md. The same workflow defines handoff and verification; delegation is optional. Prepare concise JSON of new knowledge using its schema. On PC, prefer available `danil_kb_writer` tools: `kb_capture({payload})` or `kb_checkpoint({session_id,turn_id})`. the user approved their bounded standing access on 12 October 2026. If absent from this chat's tool catalog, use the existing CLI through stdin: `node SYSTEM/scripts/kb.mjs capture` from the vault, respecting current filesystem permissions. In PowerShell, use an object → ConvertTo-Json → stdin; never interpolate user text into shell code. From another directory, use the script's absolute path.

Use real hook-provided identifiers; give a new stage a new batch_key and reuse the previous key for a retry. If the user prohibits saving content or there is no new knowledge, checkpoint without saving content. Confirm persistence using a successful receipt and an existing file. On PC, data stays local until Windows Task Scheduler Git-sync, hourly and at sign-in. the designated curator syncs her cloud copy and performs daily curation. Keep saved titles, facts, evidence and summaries in Russian; preserve machine keys, IDs and exact source quotations.
