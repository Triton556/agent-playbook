# 2.2: remove design procedures, make KB skills portable

Owner-approved scope: remove ui-design and creative-direction completely, including UI review support and automatic routes. Do not relocate their methods into another skill. Keep only the existing development verification's direct changed-scenario/readability check. Voxel passport, six views, orchestration adapters, global installation and knowledge data remain.

## Knowledge ownership

The installed kb-* entries own the operation; kb-common/references supplies the portable layout, capture schema and API exchange. No native kb-common skill is exposed. Each KB entry installs these supporting files without requiring that every reference be read. The operation names when to open its reference.

The vault owns knowledge, source records, connection details, its project-specific integrations and local access policy. New vault SYSTEM/workflows files are compatibility pointers into the installed package. Existing vaults are not overwritten during a playbook update. An older local rule conflicting with the user's requested procedure must be surfaced, not silently deleted.

Curation: selected INBOX batch → deduplicate IDs/fingerprints → update sourced current leaves → check changed page sizes/navigation → preserve old path as index when split → move original bytes to ARCHIVE → publish within permission → read back. Review at 20,000 UTF-8 bytes or four independent subtopics; split above 40,000 bytes. Typical leaves 3–12 KB and indexes below 4 KB, not token budgets or padding targets. No mandatory 12-case search comparison for every curation; retrieval algorithm changes use their own fixed relevant cases.

## Upgrade and removal

- Full 2.1.1 → full 2.2.0 retains user scope, bindings, existing KB and project design-system files. Unchanged files owned by the installer are removed when obsolete.
- User-modified or unowned files are preserved. A conflict stops before writes; inspect/archive the user's customization rather than force-delete it.
- A standalone installation consisting only of a retired skill cannot silently become a full installation. Remove its managed files with the matching old installer after review, then choose the new desired profile. Explicit retired names fail without writes.
- Restart the agent session and inspect its current skill catalog after upgrading; filesystem tests cannot establish a running client's discovery refresh.
- No changes to the user's computers are performed by publishing this package.

## Evidence and limits

The release exercises actual clean installs, user-scope 2.1.1 upgrades, conflict preservation, capture/deduplication after archiving, and current retrieval in a newly initialized vault with its local procedural manuals removed. These are synthetic fixture workflows, not an autonomous-model evaluation or proof of creative/UI quality. Source-byte measurements are not billed tokens.
