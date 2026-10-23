# Explicit routes 2.1

This revision follows the owner's decisions of 23 October 2026. It is an intentional instruction change, not a claim of unchanged model behavior. Current validation and unverified claims belong in VALIDATION.md.

## Discoverable entrypoints

13 entries: agent-instructions, you-are-brain, creative-direction, dev-plan, dev-debug, dev-verify, ui-design, voxel-models, kb-find, kb-save, kb-status, kb-sync, kb-curate.

- `you-are-brain` is the single orchestration entry. Existing Codex/Claude adapters, foreground driver, detached run/wait/recovery helpers and their relative imports remain at their existing technical paths. Keeping a driver folder does not make it a separate skill.
- `ui-design` owns design and actual user-flow inspection. A UI result is assessed through observed steps, opened states, readability, outcomes and recovery, not the existence of a test suite. Technical unit/API/regression checks remain evidence for their own contracts, not a replacement for user-flow inspection.
- `dev-implement` is no longer a separate entry; its short implementation method is a planning reference.
- `dev-flow` is no longer a catalog switch. Shared reference files remain without SKILL.md. WORKFLOW is a short event/action/output map, not a second mandatory project process.
- `visual-scenes` is no longer a separate skill, and no alias skill replaces it. Subject references remain file resources for a specified optical, spatial or rendering question, not required startup reading.
- `voxel-models` retains the required passport and six consistent design views, recognizable silhouette/form, actual rendered inspection and export validation. Asset-license/paid-asset prompt procedures are removed from this selected route. Real license files, notices, source credits and executable assets remain intact.
- `dev-plan`, `dev-debug` and knowledge integrity remain; board integrity belongs to the separate Jam application skill. `dev-plan/references/implementation.md` and `dev-verify` cover concrete implementation and technical verification; the UI path points to observed user-flow inspection.

## Startup and selected context

BASE has four rules: Russian user/knowledge prose, facts versus assumptions, requested publication, final result/checks/limits. Its source body is6073 ->431 UTF-8 bytes. This is not the full startup context: installer bootstrap, project instructions, client instructions and skill catalog are additional layers. Runtime tokens, billing and model compliance are not inferred from byte counts.

Manifest `skill_dependencies` lists actual catalog dependencies. `support_modules` separately names reference-only file groups. These files are delivered on disk without creating catalog entries or instructing the model to read them all. Loading conditions belong at the calling entry; a file path is not itself a read requirement.

## Migration

The existing receipt-checked upgrade detects modified or missing old files before target writes. Removed managed SKILL.md files can be removed only after the old trusted receipt and current bytes match. User-modified retired entries cause refusal; user-owned neighboring files remain. Existing agent-sessions / agent-sessions-codex selection aliases map to you-are-brain, and ui-review maps to ui-design. dev-flow, dev-implement, visual-scenes and jam-board requests return an explicit retirement explanation rather than silently installing a new synonym.

User scope installs user-level instructions and skills; it does not change credentials or client permissions, launch paid models, grant extra access or prove the current app's capabilities. Native versus external workers are actual available routes selected for the task; worker answers do not imply an automatic wakeup mechanism.

## Universal orchestration correction

The brain entry and its setup/profile/session support now use tasks, plans, workers, questions and acceptance without Jam Board concepts or a dependency on that application. Jam Board integration is owned and delivered separately by the Jam Board application, not by this package. Installable instructions contain no private financial or lab-access rules. Runtime sandbox parameters, generic quality ledgers, source credits and named external visual examples are not such rules and are preserved.

The startup deployment header identifies the installation and receipt, retains actual-authorization boundaries, and does not require reading policy as a workflow entry. [Measured components](STARTUP_COMPONENTS_2.1.json) distinguish BASE, deployment header and wrappers at an explicit example path; they exclude the client/system/project context and skill catalog.

## Jam Board separation in 2.1

Jam Board owns its standalone project-local skill and MCP integration. Install that skill from the Jam Board application for the selected project/client; this playbook no longer ships it or adds brain/planning dependencies for it. Old `--profile jam-board` and `--skills jam-board` requests stop with this explanation instead of installing another profile.

During an upgrade of an existing playbook installation, unchanged receipt-owned Jam files are removed; modified managed files stop the upgrade before writes, and unowned files are preserved. Keep both versions and reconcile the reported files explicitly before retrying. Independently installed/global copies are not silently removed.
