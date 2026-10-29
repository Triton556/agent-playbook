---
name: kb-save
description: Save new reusable knowledge to the configured vault INBOX; skip duplicates and empty notes.
---

# Save knowledge

Vault: {{MEMORY_ROOT}}; in Cloud use its verified file copy. Write saved content in Russian unless the user asks otherwise; machine keys stay as below.

## What to save

Extract only useful new information from the available conversation: facts, preferences, decisions with reasons, tasks and their status, project updates, ideas, sourced research and grounded hypotheses. Do not infer from inaccessible chats; never save secrets or full chats. Confirmation comes from user statements or observable results, not model confidence. Task statuses: `open`, `in-progress`, `done` (requires a confirmed result), `cancelled`. Use one writer per knowledge set; capture directly unless the user explicitly assigns a helper, who keeps the original source identity and returns the receipt. Check for an existing record before saving again.

## How to save

1. If this chat has the MCP writer tools `kb_capture` / `kb_checkpoint` (Codex server `danil_kb_writer`), use `kb_capture({payload})`. They work inside the sandbox and only on the fixed vault.
2. Otherwise pass the JSON through stdin to `node SYSTEM/scripts/kb.mjs capture` in the vault (Claude Code: `kb-claude.mjs capture`, as its hook says). In PowerShell build an object and convert it to JSON; never interpolate user text into shell code.

```json
{
  "schema_version": 1,
  "title": "Короткое название новых сведений",
  "source": {"kind": "codex", "session_id": "actual-session-id", "turn_id": "actual-turn-id"},
  "batch_key": "final",
  "final": true,
  "items": [
    {"type": "decision", "text": "Принятое решение и его причина.", "evidence": "Чем это подтверждено.", "status": "recorded", "topics": ["проект"], "links": []}
  ]
}
```

- `type`: `fact`, `preference`, `decision`, `task`, `project-update`, `idea`, `research`, `hypothesis` (hypotheses are saved as unconfirmed). `links` take web URLs only; put local paths in text or evidence.
- `source.kind`: `codex`, `rumi`, `cloud`, `manual`. Use the real hook-provided session_id/turn_id. Without platform IDs, choose stable UUIDs, keep them in the work record and reuse them on retry.
- An intermediate stage uses its own `batch_key` and `final: false`; a final record marks the whole response as processed. Different content under the same source/batch_key is rejected: pick a new key for a genuinely new stage.
- Nothing new: `kb_checkpoint({session_id,turn_id})` or `node SYSTEM/scripts/kb.mjs checkpoint --session <id> --turn <id>`, only after assessing the response and only when hooks expect a turn mark.

Success is a returned ID and an existing file. It is local persistence, not GitHub delivery; never claim persistence after a write error. Saving does not launch curation or sync.

## Author style

From the current conversation, capture material user edits, explicit writing preferences and small authentic fragments under topic author-style: real author, exact quotation, source ID, purpose, audience, genre. Label AI drafts as such; a typo or momentary frustration is not a rule. For an edit record "before → user correction → inference" with both source IDs, applicability and confidence; without such a pair do not create an editorial decision. Check saved author-style records and the three style notes for duplicates first; use batch_key `author-style-v1` per source. Load PERSONAL/Авторский стиль only when writing on the user's behalf.
