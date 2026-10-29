# Capture new knowledge

Extract only useful new information from the available conversation: facts, preferences, decisions with reasons, tasks and execution status, project updates, ideas, sourced research and grounded hypotheses. Do not infer information from inaccessible chats.

Write knowledge in Russian. Establish confirmation from user statements or observable results, not model confidence. Task statuses: `open`, `in-progress`, `done`, `cancelled`; `done` requires confirmed results. The script assigns hypotheses `unconfirmed`.

At the end of a substantive stage, pass JSON through stdin to `node SYSTEM/scripts/kb.mjs capture`. The script saves files without model calls; the main agent or designated memory agent can execute it. For Codex, use real hook-provided session_id and turn_id. For Rumi/Cloud without platform-provided identifiers, choose conversation/stage UUIDs, retain them in your current work record and reuse them on retry.

On PC, when MCP `danil_kb_writer` is available, use `kb_capture({payload})` with the same JSON or `kb_checkpoint({session_id,turn_id})` without a note. Danil approved standing access to these two operations on 12 October 2026; the tool works only with the fixed vault. Verify presence in this chat's tool catalog: registration alone does not establish loading by the active client. If absent, the existing CLI remains available under current filesystem permissions. Success requires a receipt and an existing file; retries retain identity.

This example deliberately keeps saved content in Russian while machine keys remain unchanged:

```json
{
  "schema_version": 1,
  "title": "Короткое название новых сведений",
  "source": {"kind": "codex", "session_id": "actual-session-id", "turn_id": "actual-turn-id"},
  "batch_key": "final",
  "final": true,
  "items": [
    {
      "type": "decision",
      "text": "Принятое решение и его причина.",
      "evidence": "Какими словами пользователя или результатом это подтверждено.",
      "status": "recorded",
      "topics": ["название проекта"],
      "links": []
    }
  ]
}
```

Supported type values: `fact`, `preference`, `decision`, `task`, `project-update`, `idea`, `research`, `hypothesis`. Source kind: `codex`, `rumi`, `cloud`, `manual`. At an intermediate stage, use a separate `batch_key` and `final: false`; a final record marks the whole current response as processed. Different content under the same source/batch_key is rejected: choose a new key for a genuinely new stage.

If there is no useful new knowledge, `node SYSTEM/scripts/kb.mjs checkpoint --session <session_id> --turn <turn_id>` marks the response without an empty note. Mark it only after assessing the current response. Never mark persistence complete after a write error.

On PC, capture stays local. Windows Task Scheduler performs PC Git-sync hourly and at sign-in; Rumi exchanges her cloud copy through GitHub connector/API daily or on request. Upload failure does not undo the saved file. Capture success means an existing file and returned ID; sync success means successful Git push and STATUS.md evidence. Capture receipts do not depend on summary-status refresh or Git diagnostics. STATUS.md updates through status or sync; status_refresh_pending indicates pending refresh. Record operation durations/outcomes without note content in .kb/operation-events.jsonl and .kb/hook-events.jsonl.

## Delegated memory capture

- Danil's standing permission allows one memory agent when summary volume justifies delegation. The main agent remains responsible for completed persistence.
- Give only relevant facts, decisions, evidence and limitations, plus original `source.kind`, `session_id`, `turn_id` and chosen `batch_key`. Do not substitute the helper chat's identity. When context selection is available, provide a concise task without full history.
- Assign one writer per knowledge set. The memory agent calls `capture` with `final: false` and returns command output, ID and an existing file path. If its own hook requires a mark, it checkpoints its own response without recording these facts again.
- The main agent checks the capture receipt and file existence. With no further new knowledge, checkpoint the original response; save additional information under a separate batch_key. A helper's promise is not persistence evidence. On failure, first check whether a record appeared; retry the same set with the same batch_key to avoid duplicates.
- Danil's prohibition on saving content survives delegation. Memory-agent permission does not expand data access, authorize main-task agents or separately authorize synchronization.

## Author-style additions

From the available current conversation, capture material user edits, explicit writing preferences and small suitable authentic fragments under author-style. Record real author, exact quotation, source ID, purpose, audience and genre. Label AI drafts as AI drafts; do not turn a typo or momentary frustration into a rule.

For edits, record original/correction source IDs, “before → user correction → inference,” applicability and confidence. An actual correction adds a record; preserve the original. Without an original/correction pair, do not create an editorial decision.

Before capture, check source IDs in saved author-style records and the three style notes. Skip identical duplicates; preserve conflicts with evidence. Use real capture IDs and stable batch_key author-style-v1 for one source; include each original's ID in evidence too. Do not overwrite an earlier identity with changed content. If nothing suitable is new, use an ordinary checkpoint for this response.

Capturing fragments does not apply the user's voice to ordinary replies. Load PERSONAL/Авторский стиль only for writing/editing on the user's behalf. Do not collect inaccessible chats or save full chats/secrets.
