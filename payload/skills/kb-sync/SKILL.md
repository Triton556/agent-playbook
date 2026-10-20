---
name: kb-sync
description: Synchronize a file copy of the user's personal knowledge base with its verified private GitHub repository on request or during the designated curator's daily maintenance.
---

## Knowledge transport

Use the verified vault directory. On PC: `{{MEMORY_ROOT}}`; Cloud has a separate path and authorization. SYSTEM/connection.json must contain the URL, main branch and date of actual privacy verification. Before first execution in a new environment, inspect the script and remote owner. Synchronization, cloud exchange and schedules require the current owner’s authorization and actual service/schedule verification; do not rely on another installation’s receipts.

On PC or in a verified Git clone of the main copy, run `node SYSTEM/scripts/kb.mjs sync`. In the designated curator's cloud file copy without `.git`, read SYSTEM/workflows/cloud-connector.md and exchange through the authorized GitHub connector/API; do not run Git-sync there or treat its STATUS.md as evidence of API exchange.

Git-sync saves local changes, fetches remote, merges independent records and pushes without force. Semantic curation: see [kb-curate, Knowledge curation](../kb-curate/SKILL.md#knowledge-curation).

On failure, data and local commits remain for the next run. Do not bypass a conflict with reset, force push, stash or deletion of local files. Report the error and inspect STATUS.md. The script tries to push at most twice; endless retries are unnecessary.
