---
name: kb-find
description: Find facts, decisions or current project state in the configured knowledge base.
---

# Find knowledge

Vault: {{MEMORY_ROOT}}; use the verified cloud copy when working in Cloud. Folder roles: INDEX.md is the short map; PERSONAL/, AREAS/ and PROJECTS/ hold section/project indexes and current leaves; IDEAS/ proposals; HYPOTHESES/ unconfirmed interpretations; INBOX/ uncurated captured originals; ARCHIVE/ the same originals after curation; SYSTEM/ helpers and settings.

1. Open INDEX.md, then the matching section/project index and the leaf answering the question. If no pointer matches, run `node SYSTEM/scripts/kb-search.mjs "terms" --mode current --limit 8` from the vault.
2. For current state, check matching uncurated INBOX records as well: compare event dates, cancellations and sources. Open cited originals to resolve missing evidence or conflicts.
3. Use `--mode history` only for a historical question. Report facts, hypotheses and unknowns separately; an absent record is not proof that an event did not happen.

Return the answer and relevant source paths. Retrieval does not trigger saving, sync or curation.
