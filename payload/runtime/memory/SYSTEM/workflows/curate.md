# The designated curator's daily curation

The designated curator performs this directly, without separate agents. PC synchronization requires a separately authorized setup; the cloud copy exchanges through GitHub/API under cloud-connector.md. API exchange is not shell Git-sync. Language defaults: see [AGENTS policy]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

Follow the current owner's publication policy. This procedure does not introduce mandatory PRs for initial or recurring curation.

1. Verify owner/privacy, pin the main commit and current blob SHAs. Read INDEX and necessary instructions.
2. Check the local queue and id/fingerprint across INBOX, ARCHIVE and existing open PRs. Do not duplicate processed material. Leave records arriving during curation for the next run.
3. Read only new INBOX. Preserve current facts/decisions/tasks, dates and original references. Mark old decisions superseded; preserve both versions of conflicts. Put assumptions separately in HYPOTHESES with grounds.
   For author-style, compare source IDs against current “Профиль стиля”, “Примеры”, “Редакторские решения” notes. Add only new authentic fragments with authorship/purpose/audience and actual edits with applicability. Distinguish correspondence, posts and working prose; label small-corpus observations as hypotheses. Preserve manual edits and existing records when rereading; update a specific sourced point rather than rewriting pages. A new correction cites the superseded decision; conflicts remain visible. AI drafts and synthetic tests do not enter the authentic corpus.
4. Move INBOX originals → ARCHIVE with identical IDs, fingerprints and bytes. Update INDEX and project state.
5. Publish related changes to main in one tree/commit with current parent and force=false. If main advances, reread/reconcile without overwriting others' records.
6. Read main back and verify new files and original blob-SHA equality for archiving. Do not claim success before verification.
7. Record a local API/curation receipt with commit, time and processed IDs. Do not supply a fake PR URL to old `curation-record --pr`. Distinguish scheduled execution from manual work.

If no new INBOX exists, perform only exchange and verification. Report material results, errors or required decisions; stay quiet when unchanged. Report the first actual scheduled run separately.

## Verify original → topic → index

During semantic curation, follow [retrieval-quality](retrieval-quality.md): item-level coverage and omission reasons, topic reachability, recovery questions and separate delivery verification. An original/link does not prove transfer of its decision/reason/status. Verify delivery through the current environment's route: Windows Git-sync for PC, GitHub/API for the designated curator's cloud copy.
