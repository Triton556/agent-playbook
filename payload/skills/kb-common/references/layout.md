# Portable knowledge-base layout

Use the configured vault path; moving computers changes bindings, not knowledge. On an existing vault, preserve its established names and data. A missing local copy means restore needed files from the verified repository, not silently create a competing vault. A new empty vault is created only when requested, with the installer init-memory command; no repository, credentials or schedule is created automatically.

- INDEX.md: short map to section indexes, project indexes and relevant leaves. Describe what each destination answers; keep current detail in its owning leaf.
- PERSONAL/: personal context. AREAS/: ongoing domains and section indexes. PROJECTS/: project indexes/current leaves. IDEAS/: proposals. HYPOTHESES/: explicitly unconfirmed interpretations.
- INBOX/: immutable captured originals waiting for curation. ARCHIVE/: the same originals after curation, with stable IDs and bytes. Topics cite these originals.
- SYSTEM/: runtime helpers, connection settings, optional navigation/coverage registries and project integrations. Procedures supplied by the installed skills work without a pre-existing SYSTEM/workflows manual.
- .kb/: local operational receipts and queue metadata; never secrets in committed notes.

Read route: INDEX → section/project index → relevant leaf → cited original if evidence is needed. Search first when the index has no exact pointer. Current state can be newer in INBOX; compare dates. Historical pages are reached for a particular date/question, not preloaded.

A leaf answers one coherent question. At 20,000 UTF-8 bytes or four independent subtopics review its boundary; above 40,000 bytes split it. Keep the old path as an index, preserve dated history and repair affected links/anchors. Target leaves 3–12 KB and indexes below 4 KB, without artificial padding. Raw sources/history are not cut to meet current-leaf budgets.

On another computer configure MEMORY_ROOT and the existing private repository, then verify actual read/capture behavior. Preserve existing files on conflicts. A cloud snapshot is not a Git clone. A local write, GitHub publication and delivery to another computer are different outcomes.
