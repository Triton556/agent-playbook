# Release 2.2.0 verification

Local Linux verification: Python 3.12, Node.js 22; 106 tests passed. After the final reference wording cleanup, all 7 ownership/link checks passed again. The fixed release publisher is exercised against ten fake-API scenarios per version (2.1 and 2.2), including stale heads, conflicting tags, foreign events and API failures. GitHub's Linux/Windows CI is the publication gate; this file does not pre-claim its result.

Behavior exercised:
- Clean installs across supported client layouts and user/project scopes.
- Full 2.1.1 user installation → 2.2.0 for Codex/Claude: retired owned files disappear; KB contents, an existing vault manual and project design-system files survive; a repeat install is idempotent.
- A modified retired design skill stops migration before any write. Unowned content is not deleted.
- Each KB skill installs its portable references with no pre-existing vault and no extra native skill discovery.
- Fresh-vault capture → byte-identical archive move → deduplicated repeat capture → current topic retrieval, with vault-local procedure manuals removed. This scripted synthetic scenario verifies the tools and supplied route, not autonomous semantic reasoning.
- Existing worker adapters and voxel passport/six-view implementation files are unchanged.

## Byte accounting against 2.1.1

See CONTEXT_STATS_2.2.json for the reproducible method and full metrics.

- Discoverable skills: 13 → 11.
- Reconstructed catalog metadata: 2,419 → 1,734 UTF-8 bytes (about 28% less).
- All skill entry bodies: 36,493 → 26,451 bytes (about 28% less); these are not all loaded at startup.
- Five KB entry bodies: 7,922 → 6,931 bytes (about 13% less). kb-curate grows from 1,375 to 2,916 bytes because it now contains its actual procedure rather than forwarding to the vault. Other KB entries shrink.
- Four-rule BASE unchanged, 431 bytes.
- Payload files: 142 → 122. Historical notices live outside installed skills.

No measured runtime-token saving, model-quality improvement, active client discovery, user-machine deployment or live model pilot is claimed. The user's observation that UI work was better without design skills is the reason for removal, not a controlled benchmark result.
