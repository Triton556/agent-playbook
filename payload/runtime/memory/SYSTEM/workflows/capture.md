# Capture new knowledge

Extract only useful new information from the available conversation: facts, preferences, decisions with reasons, tasks and execution status, project updates, ideas, sourced research and grounded hypotheses. Do not infer information from inaccessible chats.

Language defaults: see [AGENTS policy]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries). Establish confirmation from user statements or observable results, not model confidence. Task statuses: `open`, `in-progress`, `done`, `cancelled`; `done` requires confirmed results. The script assigns hypotheses `unconfirmed`.

At the end of a substantive stage, pass JSON through stdin to `node SYSTEM/scripts/kb.mjs capture`. The script saves files without model calls; the main agent or designated memory agent can execute it. For Codex, use real hook-provided session_id and turn_id. For the designated curator/Cloud without platform-provided identifiers, choose conversation/stage UUIDs, retain them in your current work record and reuse them on retry.

On PC, when MCP `harness_kb_writer` is available and authorized by the current installation owner, use `kb_capture({payload})` with the same JSON or `kb_checkpoint({session_id,turn_id})` without a note. The tool works only with the fixed authorized vault; persistent access requires the current owner's actual approval. Verify presence in this chat's tool catalog: registration alone does not establish loading by the active client. If absent, the existing CLI remains available under current filesystem permissions. Success requires a receipt and an existing file; retries retain identity.

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

Supported type values: `fact`, `preference`, `decision`, `task`, `project-update`, `idea`, `research`, `hypothesis`. Source kind: `codex`, `curator`, `cloud`, `manual`. At an intermediate stage, use a separate `batch_key` and `final: false`; a final record marks the whole current response as processed. Different content under the same source/batch_key is rejected: choose a new key for a genuinely new stage.

If there is no useful new knowledge, `node SYSTEM/scripts/kb.mjs checkpoint --session <session_id> --turn <turn_id>` marks the response without an empty note. Mark it only after assessing the current response. Never mark persistence complete after a write error.

On PC, capture stays local. Git-sync, cloud exchange and curation run only through separately configured and authorized services or direct requests; no schedule is active merely because these procedures are installed. Upload failure does not undo the saved file. Capture success means an existing file and returned ID; sync success means successful Git push and STATUS.md evidence. Capture receipts do not depend on summary-status refresh or Git diagnostics. STATUS.md updates through status or sync; status_refresh_pending indicates pending refresh. Record operation durations/outcomes without note content in .kb/operation-events.jsonl and .kb/hook-events.jsonl.

## Delegated memory capture

Writer assignment and handoff: see [kb-save, Delegated work]({{HARNESS_ROOT}}/skills/kb-save/SKILL.md#delegated-work).

## Author-style additions

From the available current conversation, capture material user edits, explicit writing preferences and small suitable authentic fragments under author-style. Record real author, exact quotation, source ID, purpose, audience and genre. Label AI drafts as AI drafts; do not turn a typo or momentary frustration into a rule.

For edits, record original/correction source IDs, “before → user correction → inference,” applicability and confidence. An actual correction adds a record; preserve the original. Without an original/correction pair, do not create an editorial decision.

Before capture, check source IDs in saved author-style records and the three style notes. Skip identical duplicates; preserve conflicts with evidence. Use real capture IDs and stable batch_key author-style-v1 for one source; include each original's ID in evidence too. Do not overwrite an earlier identity with changed content. If nothing suitable is new, use an ordinary checkpoint for this response.

Capturing fragments does not apply the user's voice to ordinary replies. Load PERSONAL/Авторский стиль only for writing/editing on the user's behalf. Do not collect inaccessible chats or save full chats/secrets.
