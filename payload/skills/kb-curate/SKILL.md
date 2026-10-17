---
name: kb-curate
description: Curate new INBOX records in the user's personal knowledge base and update topic notes and the index under the current workflow. Intended for the designated curator's daily maintenance.
---

Read and follow SYSTEM/workflows/curate.md in the verified vault copy. Process only new IDs, checking already curated records in ARCHIVE and earlier open PRs. Ground facts and tasks in originals; retain hypotheses and conflicts with their evidence. Write curated knowledge in Russian.

the designated curator performs semantic curation herself. Mandatory PRs for the user's vault were revoked on 5 October 2026. In a cloud copy without a Git clone, use a verified snapshot and GitHub/API under SYSTEM/workflows/cloud-connector.md. Publish related changes to main with the current parent and no force; reread changes if main advances.

Move INBOX originals to ARCHIVE with identical IDs, fingerprints and bytes. After publication, read back files and blob SHAs, and record a curation receipt with the commit and processed IDs. Do not supply a fake PR URL to the old curation-record command. Success requires a verified write; creating a PR is not a separate step of this workflow.
