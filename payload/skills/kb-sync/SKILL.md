---
name: kb-sync
description: Synchronize the configured knowledge base when requested or through its authorized schedule.
---

# Knowledge transport

Verify the configured vault and repository owner/private visibility. Preserve unsent files before fetching. Connection settings belong to SYSTEM/connection.json, not the skill. For a new/unfamiliar installation, use [layout](../kb-common/references/layout.md).

- Git clone: inspect the supplied sync helper on first use, then run `node SYSTEM/scripts/kb.mjs sync` in the vault. It commits, fetches, merges and pushes; report the actual result.
- Cloud file snapshot without .git: follow [API exchange](../kb-common/references/cloud-exchange.md). Do not run Git sync or call a local STATUS.md an API receipt.

If the remote changed or a write outcome is uncertain, reread before retrying. Preserve both versions of conflicts and the local queue; no force/reset or deleting unsent data to make sync pass. Success requires the remote commit/content. It does not prove delivery to an offline device. Synchronization moves data, not semantic curation.
