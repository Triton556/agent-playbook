---
name: kb-curate
description: Organize new INBOX knowledge or explicitly requested topic restructuring into sourced leaves and indexes.
---

# Curate knowledge

The user-appointed agent curates {{MEMORY_ROOT}} or its verified cloud copy. Vault instructions define ownership, access and project conventions.

Layout: INDEX.md is a short map describing what each destination answers. PERSONAL/, AREAS/ and PROJECTS/ hold section/project indexes and current leaves; IDEAS/ proposals; HYPOTHESES/ unconfirmed interpretations. INBOX/ holds immutable captured originals; ARCHIVE/ the same originals after curation with stable IDs and bytes; topics cite them. SYSTEM/ holds helpers, connection settings and navigation/coverage registries; .kb/ local receipts, never secrets.

Page size (UTF-8 bytes, changed active topics and navigation parents): at 20,000 bytes or four independently useful subtopics, review the boundary; above 40,000, split (raw originals and preserved history are exempt). Leaves answer one coherent question, normally 3–12 KB; indexes normally stay below 4 KB. Do not pad, fragment or add needless index levels.

1. Read the vault's AGENTS.md and INDEX.md first. Inspect unsent local files before replacing anything. Pin the repository revision and select its INBOX batch or explicitly requested topics. Compare IDs/fingerprints with INBOX, ARCHIVE and open PRs; skip duplicates but preserve conflicting content. Leave later arrivals for the next batch.

2. Group by subject. Follow INDEX → section/project index → relevant leaf and read before editing. If no route fits, search the subject and aliases before creating a page. Read selected originals fully; open other cited originals to resolve missing evidence or conflicts, not the whole vault.

3. Extract material decisions, facts/results, open questions/actions, ideas and reusable findings/preferences. Preserve rationale, constraints, event dates, status and source IDs/links. Distinguish plans, reported results and verified results. Compare dates and evidence; mark superseded decisions and retain attributed conflicts. Unsupported interpretations belong in HYPOTHESES, not facts.

4. Route by the question each item answers:
   - Existing section: update its sourced point, preserving unrelated text and manual edits.
   - Missing aspect of the same question: add a named subsection.
   - Separate question: create a descriptive leaf under the nearest suitable index after checking for an equivalent.
   Add a distinctly scoped section only if no existing section covers the topic; a singleton can be a leaf linked from root INDEX. Create an intermediate index only when distinct leaves need grouping. Keep each explanation in one owning leaf; link elsewhere. Give new leaves parent links and descriptive routes from their nearest index. Update root INDEX only when its immediate routes change.

5. Check changed active pages and navigation parents against the page-size thresholds above. At review, split or record why the question remains indivisible. When splitting, preserve prior text as dated history and keep the old path as a short index linking to history and named current leaves. Repair incoming file/heading links and configured navigation/coverage targets. Keep indivisible originals intact; summarize them in sourced leaves.

6. Check every material source item against the result: meaning and qualifications must be retained, or omission justified. Follow changed routes from INDEX to the answering section and original; check current versus historical answers, links/anchors and page sizes. Helpers do not prove semantic completeness. Archive only fully processed originals, preserving IDs, fingerprints and bytes. Keep partially processed originals in INBOX and record remaining items. Update topic citations for moved paths, never original bytes.

7. Publish only within the user's repository/branch permission, using the clone's transport or the kb-sync cloud API exchange. Commit related changes together against current head; reconcile concurrent changes without force. Read back the commit/content and verify original bytes/blob equality. Record processed IDs/commit locally. Report substantive changes, unresolved items and actual checks; distinguish curation from delivery to other computers.

Retrieval-algorithm changes require fixed relevant recovery questions before/after; ordinary curation needs no whole-vault benchmark. Project projections/schedules remain in project setup and are not activated by installation.
