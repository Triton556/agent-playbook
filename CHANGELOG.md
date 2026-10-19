# Changelog

## 0.5.0

- Added `agent-sessions`: the same orchestration procedure as `codex-sessions` (propose sessions with access modes, start after the user agrees, brief, check), with workers in any client through adapters that follow one contract (options, final JSON line, exit codes 0–4, `--describe` with real access-mode guarantees and a `verified` flag).
- Included a live-checked `codex` adapter, an unverified `claude-code` adapter (headless `claude -p`, permission modes instead of an OS sandbox) and a guide for writing and live-checking adapters for other clients.
- Selected the skill in `full`, `engineering` and `instructions`. The package now contains 26 custom skills and 308 payload files. `codex-sessions` is unchanged.

## 0.4.0

- Added `codex-sessions` for orchestrators such as Claude, another Codex or any agent with local shell/file access: write a brief, start or resume a Codex thread visible in the Codex app, and verify its result. The orchestrator proposes sessions with a name, goal, model/effort and access mode (`read-only`, `workspace-write` or `danger-full-access`) and starts them only after the user agrees; full access only when the user chooses it for that session.
- Preserved the supplied `codex-chat.mjs` driver byte for byte. The complete skill procedure is retained with a generic reference to the user's hooks from Codex settings, including memory hooks. The driver also stores the requested effort as the thread default and reports a clear error (exit code 3) when it cannot start `codex app-server`, for example inside a Codex sandbox. Both files have source/export hashes and explicit transformations in the manifest.
- Selected the skill in `full`, `engineering` and `instructions`; standalone installation and all client layouts, including Claude, remain supported. The package now contains 25 custom skills and 303 payload files.
- Updated profile counts, integration requirements and documentation; added profile/client installation coverage and a `node --check` syntax test. This is a minor release because it adds a capability while retaining existing installer and helper contracts.

## 0.3.0

- Refreshed the complete base/workflow, engineering acceptance and human-perspective checks, and UI guidance from the approved `creative` source snapshot. Preserve the user's intent, own material and accepted qualities; read the relevant criteria and examples before planning.
- Added `creative-direction` with UI/UX, content, game-design and visual/motion/3D references. All 24 skills are available in full mode; creative direction is selected by the engineering, visual and voxel profiles and included through linked dependencies where needed.
- Removed personal model/project rules, dated approval history, inherited scheduler claims, private feedback identity and historical lab identity. Memory delegation and persistent MCP access require the current installation owner's consent.
- Generalized memory integration names to `harness_kb_writer` / `harness-kb-writer`, curator capture source to `source.kind=curator`, and the opt-in scheduled-sync task to `Harness-Knowledge-Sync`. New producers/configuration must use these names; existing saved records are not rewritten. Capture/checkpoint operations, identity/idempotency checks, fixed-vault boundaries and sync safeguards remain intact.
- Corrected owner-neutral grammar, documented Windows cloning with `git clone -c core.longpaths=true`, and refreshed profile counts and source/export provenance. Datasets, attribution and licenses are preserved.

## 0.2.3

- Refined the source-approved clarification rule before choosing an approach: establish the user outcome, context, constraints, preservation/redesign boundaries and observable acceptance criteria.
- Resolve identified material product, architecture, scope and acceptance choices through concise question rounds or explicit delegation. Reuse known answers, discover technical facts and decide routine details autonomously.
- Do not silently inherit the existing implementation as a requirement. No numerical confidence gate, repeated confirmations, mandatory interview for clear small tasks, new runtime behavior or access grant is introduced.

## 0.2.2

- Translated maintained agent instructions, specialist references and memory-hook context into English.
- Explicit Russian communication and knowledge-content defaults apply in full and skills-only startup blocks; a specific user request can override output language.
- Preserved acceptance, authorization, machine schemas, helper computation, existing portability/privacy boundaries and Russian knowledge examples.

## 0.2.1

- Refreshed the current source-approved instruction roles: document editing, native skill creation and one shared workflow-pilot procedure; the Anthropic entry is a compatibility redirect.
- Added explicit task-level human participation and separate reviewer choice/round limits, the saved acceptance basis, UI preflight and current source-grounded perception checks.
- Removed duplicated general procedures from specialist entries; UX Pro Max/Taste supply targeted guidance, and current evidence can serve several criteria.
- Preserved runtime code/schemas, helper behavior, datasets, licenses and private installation boundaries. No new orchestrator, standing reviewer grant or model benchmark is introduced.
- Made the startup-budget regression fixture independent of the former long bootstrap; the installer guard itself is unchanged.

## 0.2.0

- Added the illustrated Russian profile guide with visible intermediate outputs, real six-view BUOY—02 design, camera-orbit GIF and static alternative.
- Updated the voxel pipeline from the current configured source: major material/color contours are reviewed separately from faithful 2D-to-3D transfer; metric world scale, local grid density and mechanics/proxy grids are distinguished.
- Kept existing design passport schema1 and integer source-space semantic checks within their original limits. No automatic resampling or new mixed-grid validator is claimed.
- Updated selective knowledge retrieval and curation guidance. Included the original read-only current/history search, navigation and structural coverage helpers.
- Added synthetic setup templates for destination-owned memory registries/cases; no personal data, twelve-question source fixture or private research document is bundled.
- Preserved the configured A workflow, 23 skill entry points, permissions model, full source bodies and supporting resources. No dispatcher, reverted five-instruction experiment, mandatory judge/watchdog or model-quality parity claim added.

Source change and portability boundaries are documented in [Fidelity](docs/FIDELITY.md); installation and runtime acceptance remain in [INSTALL_FOR_AGENTS.md](INSTALL_FOR_AGENTS.md) and [Integrations](docs/INTEGRATIONS.md).

### Existing installations

Retain the old pinned checkout and its private ownership receipts for verification/removal of an existing 0.1.0 installation. Review the new plan before installation; a separate target is the simplest comparison path. For replacement in the same project, use the old checkout's guarded removal first, preserving the knowledge vault and user files. Do not overwrite modified instructions or ownership records.

Existing vault runtime files are not silently upgraded by init-memory: conflicting files stop it before writes. Back up and review an explicit runtime migration for an existing authorized vault, or initialize a separate empty vault. The new search/navigation/coverage tools need no change to the pinned capture/sync core.
