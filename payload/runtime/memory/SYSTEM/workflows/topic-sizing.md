# Topic sizing and progressive disclosure

Agreed by Danil on 23 October 2026; source: ARCHIVE/2026-10-23-b524f4a68229e650a7b6543b.md. These are initial vault heuristics, not measured model-token limits.

## Trigger and scope

During curation, check only created/changed active topics and their navigation parents. Use UTF-8 bytes, not character counts or model-token estimates.

- At 20,000 bytes or four independently useful subtopics: review the page's boundaries. Record either the split or a concrete reason the explanation remains one unit.
- Above 40,000 bytes: split the active page before completing curation. If one indivisible original is larger, retain it as a source and write a concise sourced leaf rather than cutting the original.
- A leaf answers one question or covers one coherent area; normally 3,000–12,000 bytes. This is a target, not a minimum or permission to pad text.
- A project index normally stays below 4,000 bytes: purpose, current-status pointer, named leaves with descriptions, history pointer, nearest parent. Do not duplicate release numbers and status narratives at each index level.
- Do not create an index for two short paragraphs. Four headings are not automatically four independent subtopics; use the questions readers need answered.

Raw INBOX/ARCHIVE, preserved historical originals, source reports, manifests and code are not split to meet active-page limits. History is opened for a specific date/question, not preloaded. New historical excerpts should stay bounded; the original remains reconstructable/unchanged.

## Split procedure

1. Pin the current page and identify topic boundaries, dates, source IDs and incoming file/heading links.
2. Keep the old path as an index; create descriptive leaves, not generic part-1/part-2 active topics. Separate current decisions from dated history. Keep decision, reason and source together.
3. Preserve every original and superseded qualification. For mechanical relocation, verify exact source reconstruction; for summaries, record source → item → leaf and manually check material meaning. Do not promote old permissions or old current-state headings into today's decisions.
4. Update nearest-parent links, navigation registry and coverage targets. Retarget known heading links or leave small compatibility anchors at the old path. Do not mutate raw originals to repair navigation.
5. Run `node SYSTEM/scripts/kb-topic-size.mjs <changed-path> ...`, navigation and link checks. Reproduce user questions through index → selected leaf → source. Report actual files/bytes opened, not claimed tokens saved.
6. Publish with the current parent and verify readback. If main advanced, reconcile; do not overwrite new captures. A successful local check is not delivery to the PC/Mac.

Root INDEX and section indexes explain where knowledge lives. Put dated curation ledgers and release history in historical pages, not repeated status paragraphs in root navigation.
