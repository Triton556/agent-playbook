# Verify semantic curation and recovery

Use during curate and knowledge-map changes. Ordinary retrieval starts with INDEX and one branch; do not preload the whole archive.

1. Pin the snapshot, new source IDs/fingerprints and deduplication across INBOX/ARCHIVE/open PRs. Preserve new arrivals outside the chosen batch for a separate stage.
2. For each material original item, record source, item, topic and the concise transferable decision/reason/status in a separate coverage JSON. A duplicate/omission needs explicit grounds. Do not change raw records to satisfy coverage.
3. Verify original → topic: the topic cites the source and retains the material qualification. A URL establishes a link, not meaning; read the actual corresponding paragraph.
4. Verify topic → index: root INDEX provides an understandable route through a thematic index/project. Do not create a node for every raw record. Date history and superseded decisions.
5. Before continuing, answer from sources: goal, latest decision and reason, cancellations, actual verification, proposals only, unknowns and nearest step. Do not invent missing information.
6. Run `node SYSTEM/scripts/kb-lint.mjs --json` and `node SYSTEM/scripts/kb-coverage.mjs`. The latter checks registry structure; semantic assessment remains manual.
7. On 12 fixed [cases](../examples/retrieval-cases.template.json), compare original `kb.mjs search` with `kb-search.mjs`: expected topic/source in top-8, answer correctness and required qualification. Record opened file/byte counts as this experiment's volume, not actual model tokens.
8. After writing, separately verify delivery through the agreed environment route: existing Windows Git-sync on PC; GitHub/API under cloud-connector.md in the designated curator's cloud copy. Confirm commit/content. Do not change pinned scheduler scripts for retrieval. Successful curation does not establish delivery to another device.

`kb-search.mjs` supports current/history and shows relevant INBOX separately. Topic priority does not make it newer than the queue; always compare source/event dates. The old search command remains available.

Full research documents and captures are different originals. For unavailable documents, preserve the exact pointer/access limitation and do not claim full recovery. No full chats/secrets in Git.

## Primary navigation verification

After structural changes, run `node SYSTEM/scripts/kb-navigation.mjs`. SYSTEM/navigation/parents.json assigns one nearest parent per topic. Checks cover both parent ↔ topic directions, root incoming links and reachability without historical maps. Preserve semantic crosslinks. Change history and Obsidian filters only within separately agreed scope.

## Setup for another vault

Before verification, the owner supplies their own SYSTEM/coverage/coverage.json, SYSTEM/navigation/parents.json and 12 actual recovery cases. SYSTEM/examples contains only synthetic schema templates: populate them with your verified sources/topics. Private source-owner registries and questions are not supplied. Missing setup is not a successful check; an empty/demo registry does not establish coverage of a working vault. Helpers verify links/files; meaning needs separate assessment under the steps above.
