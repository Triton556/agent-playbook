# Changelog

## 1.6.0

- Restore the selected adapter-session route, saved task choices and worker audience after context recovery. Add a read-only host-preview diagnostic with explicit limits; a supplied preview does not certify the active desktop session.
- Add optional checked `--assignment` and `--resume-run` support to the Codex/Claude adapters and legacy Codex foreground driver. New detached runs retain launch settings and assignment snapshots; recovery continues the original thread with separate reports and logs.
- Refuse explicit recovery output/log paths that alias the previous status, report or event log, including normalized paths and existing file aliases, before starting a backend. Preserve the previous run evidence.
- Fix the quoted-brief preservation check for Windows CRLF without changing the forwarded source text or product labels. Existing approval, access, installation and publication boundaries remain in effect.
- Behavioral pilots observed correct continuation preparation in both versions and automatic context restoration in the new version. Successful model-driven crash recovery and a general reliability improvement remain unverified; see [validation](docs/VALIDATION.md#version-160-release-verification).

## 1.5.1

- Clarified English for every agent-to-agent channel by intended recipient, including final handoffs; initial briefs assign audience and deliverable languages, retained on continuation. Direct user conversation and knowledge-base prose keep Russian defaults and explicit user exceptions; exact source/product text is preserved.
- Preserved the language owner, exact brief mirrors and Codex running pointer; refreshed export provenance and added static policy and isolated installation checks. These checks do not establish live model compliance.

## 1.5.0

- Added adapter contract v2 with detached Codex/Claude Code turns, atomic external run metadata and one shared wait/status/cancel tool. Foreground commands, result shapes and exit codes 0–4 remain compatible; wait timeout uses exit 5. The Codex legacy driver remains explicitly foreground-only.
- Split orchestration waiting by client notification support, added runId/statusFile to the session log, and replaced the Codex running-reference mirror with a pointer to its single policy owner.
- Added board-aware waiting for detached workers and the confirmed Jam Board wait_for_changes contract; list_changes_since remains recovery. Tool availability/schema must be checked against the connected app before use.
- Added synthetic wait/cancellation and Codex protocol integration coverage plus full-profile installation checks. Live smoke results and client verification limits are recorded in the local DETACH_WAIT_REPORT.md; no live Claude task or model-quality comparison is claimed.

## 1.4.0

- Resolved all 61 audit findings through single policy owners and caller pointers, including reviewer execution/rounds, explicit decision consent, one launch gate, effort precedence, output language, artifact publication, UI and voxel references. Added an ownership map and regression checks; the three shared orchestration references remain byte-identical.
- Added user-supplied you-are-brain with private brain profiles and setup interview; orchestration uses agent-sessions. Refreshed the two session skills from the supplied sources while retaining public Codex hooks wording/runtime identity.
- Added the new skill to full, engineering, instructions and jam-board profiles. The package contains 26 skills and 310 payload files. Linked policy owners remain installation dependencies.
- Updated inventory, provenance and export hashes; added standalone Codex/Claude installation, policy uniqueness and payload-link coverage. No live workers, model-quality pilot or publication were run.
- Restored the full interview method in its owner, `dev-flow/references/task-brief-and-acceptance.md`, section 3 "How to run the rounds": restate, collect facts, list open decisions, order them as a tree, the Q/recommended-answer format, round size, and a worked example. The session interview reference points to it.
- Sessions start with exactly the name from the approval table, in the user's language; status updates also appear in the orchestrator's final message of every turn while any session is not yet accepted. Both came from a live you-are-brain run (Codex sol as brain, Astra and Sol as workers), which otherwise passed end to end.
- Restored what each brain routing mode means (Rules, Auto, Ask) in `you-are-brain/references/brain-profile.md`, its owner, after deduplication had left it undefined.

## 1.3.0

- Added `jam-board`: Epic → Story → Task planning and execution through the Jam Board MCP contract, with brain/worker roles, scoped interview rounds, user-selected worker models, complete briefs, readiness, references/assets, reports and review. Existing playbook procedures are linked rather than copied; no other skill content changes.
- Added a worked brain loop with two full task briefs and a failed/repaired review, a worker report example, a field guide and verbatim app connection examples for Codex/Claude Code. The board is the task source of truth. Follow the project's policy on publishing worker briefs and reports; if none is stated, keep them local and ask before committing or publishing them. Self-review is forbidden and session launch still needs explicit consent.
- Added profile `jam-board` (the skill plus `dev-flow`, `dev-plan`, `agent-sessions`, `agent-sessions-codex`); `full` and `engineering` include it. The package now contains 25 skills and 307 payload files. Trusted complete-workflow upgrades add the new module while retaining existing conflict/ownership validation.
- Added catalog/profile, MCP vocabulary/JSON example, relative-link/anchor, source-connection fidelity and isolated Codex install/verify/doctor checks. File integrity and author dry reading do not establish live MCP execution, independent model review or human acceptance.

## 1.2.0

- Orchestration skills (`agent-sessions`, `agent-sessions-codex`) now require separate visible sessions for delegated work and forbid the client's built-in subagents for it.
- Approval is one summary in the user's language: the task, done-when checks, a table of sessions (what each does, model, effort with reason, access, folder, dependencies, brief file) and how each will be checked. Briefs are written before approval, so the user approves the actual tasks.
- Effort is chosen from the lowest fitting level using a table of task types with examples; the maximum is allowed only for open creative or design exploration, after a lower level failed, or on the user's request.
- Added `references/running-and-checking.md` to both skills: preparing folders and a starting point, a session log, background runs and dependencies, an eight-step check (report, real diff, rerun checks, evidence per requirement, boundaries, behaviour beyond tests, verdict, log) and the report to the user.
- Briefs must name each tool and action as allowed or forbidden instead of umbrella words such as "local only"; briefs and worker reports stay local and are never committed or published.

## 1.1.0

- `agent-sessions` and `agent-sessions-codex` now follow one six-step workflow: find out the requirements, propose the plan, write the briefs, run, check, report.
- Fixed rules: briefs to workers are in English; workers report to the orchestrator in English, while everything the user reads is in the user's language; the user chooses each worker's model; the orchestrator chooses effort per session and states why.
- Added `references/requirements-interview.md`: restate the goal, collect facts yourself, then ask in rounds (adapted from the "grilling" approach in Matt Pocock's skills): each round asks every decision that can be settled now, each with a recommended answer, until no open decision would change the plan. The size of a round is limited, not the number of rounds.
- Added `references/brief-writing.md`: a structured template (per-change Now / Required / Where / Follow / Keep, numbered tests with expected values and a baseline, boundaries, a report with PASS/FAIL per test and deviations, an exact final-message format), form rules (lists instead of paragraphs, numbers instead of adjectives, exact strings), three complete examples, a follow-up brief and a weak versus strong brief. Both skills carry identical copies, kept equal by a test.

## 1.0.1

- Renamed the remaining app display names to match the 1.0.0 skill names: Agent Handoff, Dev Domain Model, Visual Scenes.
- `agent-sessions` and `agent-sessions-codex` now ask the orchestrator to choose worker effort per task (low, medium, high, xhigh, maximum) and state it with a reason in the session plan, instead of using the client's default.
- The installer now upgrades any trusted older release in place (previously only 0.x to exactly 1.0.0), so 1.0.0 installations update to 1.0.1 without removal. Added a test for the 1.0.0 upgrade.

## 1.0.0

- Renamed the public package from `agent-workflow-harness` to `agent-playbook`; clone URL: https://github.com/Triton556/agent-playbook. The GitHub repository rename is handled separately before publication; the old address redirects to the new address after that rename.
- Applied the approved names below across the retained payload, profiles, installer, manifest and documentation. Third-party source identities and licenses are unchanged.

| Previous skill | Public skill |
|---|---|
| `product-engineering` | `dev-flow` |
| `product-planning` | `dev-plan` |
| `product-implementation` | `dev-implement` |
| `product-debugging` | `dev-debug` |
| `product-testing` | `dev-verify` |
| `domain-modeling` | `dev-domain-model` |
| `product-ui-design` | `ui-design` |
| `product-ui-review` | `ui-review` |
| `ui-ux-pro-max` | `ui-reference` |
| `design-taste-frontend-v1` | `ui-taste-reference` |
| `codex-sessions` | `agent-sessions-codex` |
| `handoff` | `agent-handoff` |
| `writing-for-agents` | `agent-instructions` |
| `grilling` | `stress-test` |
| `grill-with-docs` | `stress-test-with-docs` |
| `visual-experiment-craft` | `visual-scenes` |
| `voxel-model-craft` | `voxel-models` |

- Unchanged: `agent-sessions`, `creative-direction` and all `kb-*` skills. Removed `anthropic-workflow-creator` (compatibility stub) and `lab-vm-control` (personal VM control), including their 12 files and active routes. The package contains 24 skills and 296 payload files.
- Old `--skills` names resolve to new names with a warning; removed names fail with an explanation. Trusted 0.x receipts migrate in place: verify all old content, install new paths and retire only unchanged owned files. User files and startup text outside the managed block survive. Missing/edited content, untrusted records and conflicts refuse migration before writes. Keep the original private receipt store and repeat the original options.
- Added regression coverage for aliases, removals and actual 0.5.0-to-1.0.0 installations, including conflict and ownership preservation. No live agent sessions, model pilot or independent review are claimed.
- Preserved profile dependency sets under the new names: ordinary stress-test prose and protocol client identities no longer create accidental skill dependencies. No exception to the approved rename scheme was needed.

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
