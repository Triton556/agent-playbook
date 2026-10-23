---
name: kb-curate
description: Organize new INBOX knowledge or explicitly requested topic restructuring into sourced leaves and indexes.
---

# Curate knowledge

The user-appointed agent performs the curation. Vault: {{MEMORY_ROOT}}, or the verified cloud copy. The portable [layout](../kb-common/references/layout.md) defines folders, indexes and leaf sizes; read it for first use or structural changes. Local repository instructions define its ownership, access and additional project conventions, not a replacement for this procedure.

1. Pin the current repository revision; inspect local unsent files. Select the new INBOX batch and compare IDs/fingerprints with INBOX, ARCHIVE and open PRs. An explicit restructure can select existing topics instead. Leave later arrivals outside the batch.
2. For each material item, update the appropriate current leaf: decision/fact, reason, date, status and source link. Preserve conflicting evidence; mark superseded decisions. Put unsupported interpretations in HYPOTHESES, not facts. Read the related leaf and source, not the whole vault.
3. Check changed active pages: review at 20,000 UTF-8 bytes or four independently useful subtopics; split above 40,000 bytes. Keep the old page path as a short index, create named leaves for coherent questions, and separate dated history. Leaves normally 3–12 KB; no padding or splitting an indivisible source. Indexes normally below 4 KB.
4. Check the changed route from INDEX through its parent to each leaf and original. Retain source IDs and meaningful qualifications, repair affected links/anchors, and answer the actual recovery question from the result. Existing coverage/navigation helpers support this check; they do not prove semantic completeness. No mandatory whole-vault benchmark for an ordinary batch.
5. Move each processed original INBOX → ARCHIVE without changing ID, fingerprint or bytes. This is preservation at a new path, not destruction. Retain prior topic text as dated history when restructuring; do not label old status current.
6. Publish only within the user's repository/branch permission. In a Git clone use its configured transport; in a cloud snapshot use [API exchange](../kb-common/references/cloud-exchange.md). Commit related topic/index/archive changes together against the current head; reread/reconcile concurrent changes without force.
7. Read back the commit and changed content; check original bytes/blob equality. Report the substantive result and unresolved items. Record processed IDs/commit locally. Separate successful curation from delivery to other computers.

For changes to the retrieval algorithm itself, use a fixed relevant set of recovery questions before/after. For normal curation, verify the changed knowledge, not an unrelated test quota. Keep project-specific projections and schedules in that project's setup; do not activate them merely by installing this skill.
