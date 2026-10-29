# Cloud exchange through the GitHub connection

Agreed by Danil on 4 October 2026 in conversation with Rumi. This procedure replaces direct Git/SSH requirements only for Rumi's cloud environment. The PC keeps existing kb-sync.

## Boundaries

- Repository: Triton556/personal-knowledge; verify owner and visibility=private before exchange.
- Rumi performs the work herself. Do not launch additional agents or chats.
- Current cloud working path: /workspace/shared/personal-knowledge. This is a file copy, not a Git clone. Persistence after environment recreation is unproven.
- GitHub stores confirmed uploads. An unsent local queue can be lost if the environment is destroyed; do not promise indefinite local storage.
- There is no direct PC access. The agreed Windows Task Scheduler uploads the PC queue hourly and at sign-in, without AI. An offline PC retains its queue until it returns; being connected does not prove exchange completed.

## Download

1. Read repository metadata, main and the file/blob-SHA listing. Pin a commit for a consistent snapshot.
2. Download needed files through GitHub. Check paths, absence of symlinks and root escapes. Do not load the entire history.
3. Keep base SHAs and receipts in .kb. If a local file differs from its base SHA, preserve local and remote separately instead of overwriting.
4. If the copy disappears, restore needed instructions, INDEX and records from GitHub. An absent local file does not authorize remote deletion.
5. Inspect downloaded code before executing it. Read only needed instructions.

## Upload

- Capture uses existing `node SYSTEM/scripts/kb.mjs capture`, without model calls.
- Before uploading new INBOX, check id/fingerprint in INBOX, ARCHIVE and open PRs. Treat a match as a duplicate; preserve a conflict if content differs.
- New raw INBOX records may be created on main. Success requires a commit SHA and readback of the exact file, not just a local write.
- Do not alter existing raw records.
- Supply the current blob SHA when changing an existing file; reread/compare on conflict, never force.
- Use one Git tree/commit and fast-forward ref update for related changes; no force update. Do not delete records created concurrently.
- On failure/uncertain outcome, reread the target path/branch before retrying. Preserve the local queue.

## Curation

Follow SYSTEM/workflows/curate.md. Danil explicitly removed mandatory PRs. Publish agreed curation to main in one tree/commit and fast-forward update, force=false. INBOX → ARCHIVE originals retain blob SHA. On concurrent changes, reread main and preserve both versions when conflicting.

## Status

Distinguish local capture, API exchange, Git sync, PC exchange and scheduled run. kb.mjs STATUS.md does not establish API synchronization. Keep API receipts in .kb/connector-state.json: commit, paths/SHAs, time and errors; no credentials. PLAN.md records verified results and remaining limitations.

## Schedule

Daily at 06:00 Asia/Vladivostok. The task was enabled on 4 October 2026, DTSTART=2026-10-05 06:00; the service's saved next_run_time was null. Verify the first actual run separately. Stay quiet when unchanged; report only a material result, error or required decision.
