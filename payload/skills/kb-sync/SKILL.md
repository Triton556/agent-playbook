---
name: kb-sync
description: Synchronize the configured knowledge base when requested or through its authorized schedule.
---

# Knowledge transport

Verify the configured vault ({{MEMORY_ROOT}}) and that the repository ({{MEMORY_REPO}}) is the owner's and private. Preserve unsent files before fetching. Connection settings belong to SYSTEM/connection.json, not the skill.

- Git clone: inspect the supplied sync helper on first use, then run `node SYSTEM/scripts/kb.mjs sync` in the vault. It commits, fetches, merges and pushes; report the actual result.
- Cloud file snapshot without .git: use the API exchange below. Do not run Git sync or call a local STATUS.md an API receipt.

If the remote changed or a write outcome is uncertain, reread before retrying. Preserve both versions of conflicts and the local queue; no force/reset or deleting unsent data to make sync pass. Success requires the remote commit/content. It does not prove delivery to an offline device. Synchronization moves data, not semantic curation.

## New computer

Clone the existing private repository and point MEMORY_ROOT at it; moving computers changes bindings, not knowledge. Keep established names and data; preserve existing files on conflicts. A missing local copy means restoring from the verified repository, not creating a competing vault. A new empty vault is created only on request with the installer's `init-memory`; it creates no repository, credentials or schedule. Verify actual read and capture afterwards.

## Cloud copy through the GitHub API

Only for the owner's authorized cloud copy ({{CLOUD_MEMORY_ROOT}}) without Git/SSH. It is a file copy whose persistence after environment recreation is unproven; GitHub holds only confirmed uploads. The designated curator works directly, without launching other agents.

- Download: read repository metadata, main and the file/blob-SHA listing; pin a commit. Fetch only needed files, rejecting symlinks and root escapes; inspect code before executing it. Keep base SHAs and receipts in .kb. If a local file differs from its base SHA, keep local and remote separately. An absent local file never authorizes remote deletion.
- Upload: capture with `node SYSTEM/scripts/kb.mjs capture`. Before uploading INBOX, check id/fingerprint in INBOX, ARCHIVE and open PRs; a match is a duplicate, different content is a conflict to preserve. New raw INBOX records may go to main; never alter existing raw records. Change existing files with their current blob SHA; related changes go in one tree/commit with a fast-forward ref update, never force. Success requires a commit SHA and readback of the exact file. On failure reread before retrying and keep the local queue.
- Status: keep API receipts (commit, paths/SHAs, time, errors; no credentials) in .kb/connector-state.json. Schedule: {{CURATION_SCHEDULE}}; it is active only once actually configured. Report only a material result, error or required decision.
