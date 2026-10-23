> **User-wide installation (2.1.1):** use `--scope user --target <HOME>` for Codex or Claude on plan/install/verify/doctor/remove. Skills and the four-rule managed block are installed in native user paths, not in the working project. See [clean installation](docs/CLEAN_INSTALL_FOR_AGENTS.md#4-plan-and-install-into-the-explicit-target).

> **Version 2.1:** [explicit routes, reference modules and safe upgrade](docs/EXPLICIT_ROUTES_2.1.md). Older external bundles and detectors described in historical release material are no longer shipped.

# Installation procedure for an agent

Read this document before changing the destination. The user chooses what to install and authorizes access, costs and integrations. The installer writes to the explicit project or user-home target, its private receipt store in this checkout, and, when separately requested, the explicit knowledge vault. It does not change the source author's configuration.

## 1. Establish the requested installation

Recover the user's selected client, project, full workflow or skills/profile, existing instructions and authorized tools. Reuse choices already provided. Substantial new access, paid services, permissions or a different installation format require the owner's actual decision. Running a normal step inside the selected scope does not require repeated “continue?” questions.

Use a fresh checkout at a pinned Git commit or release. Check provenance, [third-party licenses](THIRD_PARTY_NOTICES.md), `harness.py` and `manifest.json` before execution. Keep provider credentials outside the repository and command output.

Requirements:

Read [integration setup](docs/INTEGRATIONS.md) for interpreter bindings, startup budgets/overrides, MCP, actual hooks and capability acceptance. [Workflow guide](docs/WORKFLOW_GUIDE.md) maps the preserved routes and context layers.

- Python 3.12+ for the installer, including Windows junction checks. Use the actual available interpreter.
- Node.js 22+ for task-state, limited memory MCP and knowledge helpers.
- A client that discovers local `SKILL.md` bundles and project instructions, or a verified explicit discovery integration for generic mode.
- Actual browser/image inspection for visual work. Appropriate format/image generation tools where the selected task needs them.
- A genuine fresh-context review tool only when separate review is explicitly selected for the current task.

## 2. Inspect the complete plan

```bash
python harness.py catalog
python harness.py plan --client codex --target /path/to/project --profile full
```

Available clients: `codex`, `claude`, `deepseek`, `generic`. Profiles: `full`, `engineering`, `visual`, `voxel`, `memory`, `instructions`. `--skills name1,name2` selects named skills; dependency closure includes only explicit required modules. References and helper files stay complete.

`full` activates the complete workflow. `--workflow` also expands the selection to all 13 entrypoints. The four-rule BASE does not automatically route through every skill. Skills-only installation preserves individual entry points without claiming all global behavior is active.

`you-are-brain` is selected by `full`, `engineering` and `instructions`, or explicitly with `--skills you-are-brain`, for any client including Claude; its technical support includes the unchanged Codex drivers. Read its [integration requirements](docs/INTEGRATIONS.md#you-are-brain-codex-route) before an authorized session launch; installation alone does not start Codex or configure it.

Inspect the target's existing AGENTS.md/CLAUDE.md and native skill directories. A different existing file stops installation before writes. Resolve a real conflict by a scoped human decision or a different target; do not delete or overwrite existing settings to make installation pass.

## 3. Supply the new owner's environment

Paths are deployment bindings. Set them explicitly when applicable:

```bash
python harness.py install --client codex --target /path/to/project --profile full \
  --memory-root /authorized/private/vault \
  --evidence-root /authorized/reference-projects
```

Other supported bindings: `--memory-repo`, `--cloud-memory-root`, `--curation-schedule`. Personal VM control and lab-specific bindings are outside the public package.

Task participation/reviewer selection: see [task brief and acceptance, section 5](payload/skills/dev-flow/references/task-brief-and-acceptance.md#5-two-decisions-about-how-to-work). Legacy --reviewer-consent one-per-round --consent-source fields retain deployment-record compatibility; current authority remains with AGENTS.

## 4. Install and verify files

```bash
python harness.py install --client codex --target /path/to/project --profile full
python harness.py verify --client codex --target /path/to/project
python harness.py doctor --client codex --target /path/to/project
```

The full base instructions are inserted verbatim after environment binding into a managed startup block. Existing project text remains. BASE-RULES.md stores the same complete base without introducing a second automatically loaded nested AGENTS.md. User scope installs native user instructions and skills. No permission setting, API key, hook or scheduler is registered.

Repeat installation with the same options is idempotent. Changing selection or bindings is a distinct installation decision: retain the old state, inspect removal and reinstall safely or choose a new target. Edits to owned files are preserved and cause verification/removal to stop.

Retain this installer checkout's private `.harness-state/receipts/` until removal. It stores the original ownership record separately from mutable destination files and is gitignored; never publish it. `verify`/`remove` reject destination receipts changed, pruned or rehashed to disguise modified files. A replacement checkout needs the original trusted private record through an authorized migration; missing records preserve files and stop removal. A malicious change to both trusted installer/store and destination is outside this ownership boundary. No copied private record is a new tool permission.

## 5. Provision selected integrations separately

### Knowledge

For a new empty authorized vault:

```bash
python harness.py init-memory --client codex --target /path/to/project
```

This copies the memory runtime/procedures and creates an empty INDEX/connection template. Existing different vault files stop initialization. It imports no personal records, configures no remote and starts no schedules.

Use the unchanged CLI contract against that vault:

```bash
node /authorized/private/vault/SYSTEM/scripts/kb.mjs status
node /authorized/private/vault/SYSTEM/scripts/kb.mjs search "specific project" --limit 8
```

Capture/checkpoint procedure: see [kb-save, Knowledge capture](payload/skills/kb-save/SKILL.md#knowledge-capture).

The limited writer lives at `<native-root>/workflow/kb-writer.mjs`. Configure `HARNESS_KB_ROOT` as the authorized fixed vault for that process. It exposes only capture/checkpoint; it does not grant shell, arbitrary paths, deletion or sync. Registering its persistent access in a client requires the owner's actual approval. Use the client's official MCP instructions; no config is silently edited by this installer.

Memory transport: see [kb-sync, Knowledge transport](payload/skills/kb-sync/SKILL.md#knowledge-transport). Semantic curation: see [kb-curate, Knowledge curation](payload/skills/kb-curate/SKILL.md#knowledge-curation).

### UI checks

Use the unified `ui-design` entry for actual rendered interaction and user-flow checks. No bundled external detector or binary is required.

### Native/client capabilities

Required capabilities: see [Compatibility](docs/COMPATIBILITY.md). Unavailable operations: see [human-perspective-review, Readiness and transfer](payload/skills/dev-flow/references/human-perspective-review.md#readiness-and-transfer).

## 6. Start a new session and exercise the selected route

Inspect the native skill catalog for this target and confirm complete selected names/body loading; client-specific activation: see [Integrations, Codex startup budget and discovery](docs/INTEGRATIONS.md#codex-startup-budget-and-discovery). Instruction loading: see WORKFLOW, step 2.

Run an authorized representative task for the selected route. Use the real user brief and the original acceptance criteria. Examples:

- UI: primary action, visible correct result, invalid input recovery, preserved state, actual intended viewport.
- Voxel: use [voxel design preflight](payload/skills/voxel-models/references/design-preflight.md) and its later model comparison.
- Memory: capture/read-back/idempotent repeat/checkpoint; sync remains disabled until private remote approval/verification.
- Instructions: follow [agent-instructions](payload/skills/agent-instructions/SKILL.md) and verify affected references.

Review selection: see task brief and acceptance, section 5; selected execution: see [independent-review](payload/workflow/independent-review.md). Workflow experiments: see [workflow-pilot](payload/skills/dev-flow/references/workflow-pilot.md).

## 7. Report the actual installation state

Report selected/requested modules, dependency closure, target/client, integrity, actual discovery, executed helper/client scenarios and missing capabilities. Claim grades: see [human-perspective-review, Readiness and transfer](payload/skills/dev-flow/references/human-perspective-review.md#readiness-and-transfer).

Installation evidence levels are interpreted under human-perspective-review, Readiness and transfer; source bytes alone establish no model-output equivalence.

## Removal

Inspect `remove --dry-run` first. Actual removal deletes only matching owned files and the matching owned instruction block. Modified files stop removal; preexisting identical files, other project content and knowledge data remain. The installer performs no recursive directory delete. Do not use reset, force deletion or overwrite to clear conflicts.

## Instruction and output languages

Language policy: see [AGENTS, Goal, communication and boundaries](payload/AGENTS.md#goal-communication-and-boundaries); worker exception: see [brief-writing, Language](payload/skills/agent-sessions/references/brief-writing.md#language).

## Upgrade from 0.x to 1.0.0

Update this same checkout and keep its gitignored `.harness-state/receipts/` private store. Repeat the original `plan` and `install` commands with the same target, client, profile/skills, workflow flag and retained deployment bindings, then run `verify`. Omit retired lab flags; their old values are ignored during migration. `plan` reports `migration_from` and `obsolete_owned_files` without writing. Original skill names in `--skills` are aliases that warn on stderr; the plan and installed catalog use the new names. See the complete [rename table](CHANGELOG.md#100). Removed modules return an explicit error when requested directly.

The installer checks the destination receipt against its original private record, validates every old file and the managed startup block, replaces unchanged owned files, and removes only obsolete owned files. Renamed skills appear at their new paths; removed modules are retired. User neighbors, preexisting identical files and text outside the managed block remain intact, including BOM/CRLF. Edited or missing old files, a changed block, different options, missing private records or new-path conflicts stop the upgrade before writes. Resolve the reported conflict without deleting user content, then retry. A separate checkout needs an authorized transfer of the original private record; a destination receipt alone is insufficient. Empty old directories may remain. Back up the project and private receipts before upgrading; retain the 0.x checkout for recovery. User scope changes its native user instructions and skills; credentials and other settings remain unchanged.

## Jam Board separation in 2.1

Jam Board owns its standalone project-local skill and MCP integration. Install that skill from the Jam Board application for the selected project/client; this playbook no longer ships it or adds brain/planning dependencies for it. Old `--profile jam-board` and `--skills jam-board` requests stop with this explanation instead of installing another profile.

During an upgrade of an existing playbook installation, unchanged receipt-owned Jam files are removed; modified managed files stop the upgrade before writes, and unowned files are preserved. Keep both versions and reconcile the reported files explicitly before retrying. Independently installed/global copies are not silently removed.

Clean replacement of an existing installation: [agent procedure](docs/CLEAN_INSTALL_FOR_AGENTS.md). Preserve original receipts, user edits and knowledge data.
