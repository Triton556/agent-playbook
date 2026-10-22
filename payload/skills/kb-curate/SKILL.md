---
name: kb-curate
description: Curate new knowledge INBOX records into sourced topics and an index during authorized maintenance; preserve original records.
---

## Knowledge curation

Read and follow SYSTEM/workflows/curate.md in the verified vault copy. Process only new IDs, checking already curated records in ARCHIVE and earlier open PRs. Ground facts and tasks in originals; retain hypotheses and conflicts with their evidence. Language defaults: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

The designated curator performs semantic curation directly. Follow the current owner's publication policy; this procedure does not introduce mandatory PRs. In a cloud copy without a Git clone, use a verified snapshot and GitHub/API under SYSTEM/workflows/cloud-connector.md. In addition to [kb-sync, Knowledge transport](../kb-sync/SKILL.md#knowledge-transport), publish authorized related curation changes with the current parent; reread if main advances.

Move INBOX originals to ARCHIVE with identical IDs, fingerprints and bytes. After publication, read back files and blob SHAs, and record a curation receipt with the commit and processed IDs. Do not supply a fake PR URL to the old curation-record command. Success requires a verified write; creating a PR is not a separate step of this workflow.
