# Installation procedure for an agent

Read this document before changing the destination. The user chooses what to install and authorizes access, costs and integrations. The installer writes to the explicit project target, its private receipt store in this checkout, and, when separately requested, the explicit knowledge vault. It does not change the source author's configuration.

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

Available clients: `codex`, `claude`, `deepseek`, `generic`. Profiles: `full`, `engineering`, `visual`, `voxel`, `memory`, `instructions`. `--skills name1,name2` selects named skills; dependency closure includes every linked sibling. References and helper files stay complete.

`full` activates the complete workflow. `--workflow` also expands the selection to all 24 modules: the global rules route to all of them, so partial activation would leave broken routes. Skills-only installation preserves individual entry points without claiming all global behavior is active.

`agent-sessions-codex` is selected by `full`, `engineering` and `instructions`, or explicitly with `--skills agent-sessions-codex`, for any client including Claude. Read its [integration requirements](docs/INTEGRATIONS.md#agent-sessions-codex-for-orchestrators) before an authorized session launch; installation alone does not start Codex or configure it.

Inspect the target's existing AGENTS.md/CLAUDE.md and native skill directories. A different existing file stops installation before writes. Resolve a real conflict by a scoped human decision or a different target; do not delete or overwrite existing settings to make installation pass.

## 3. Supply the new owner's environment

Paths are deployment bindings. Set them explicitly when applicable:

```bash
python harness.py install --client codex --target /path/to/project --profile full \
  --memory-root /authorized/private/vault \
  --evidence-root /authorized/reference-projects
```

Other supported bindings: `--memory-repo`, `--cloud-memory-root`, `--curation-schedule`. Personal VM control and lab-specific bindings are outside the public package.

The originating user's permissions and schedule receipts are not authorization for another owner. In each actual task, select human participation and separately whether a reviewer is needed, with scope, stages and round limit. Default reviewer policy is `ask`; autonomous execution does not imply consent. The legacy `--reviewer-consent one-per-round --consent-source ...` fields remain for compatibility with explicitly supplied deployment records; they do not create a standing grant for future tasks or override the current task's decision.

## 4. Install and verify files

```bash
python harness.py install --client codex --target /path/to/project --profile full
python harness.py verify --client codex --target /path/to/project
python harness.py doctor --client codex --target /path/to/project
```

The full base instructions are inserted verbatim after environment binding into a managed startup block. Existing project text remains. BASE-RULES.md stores the same complete base without introducing a second automatically loaded nested AGENTS.md. No global client config, permission setting, API key, hook or scheduler is registered.

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

`capture` receives structured JSON on stdin; real source/session/turn identity and idempotent batch identity are required. No new knowledge uses `checkpoint`. Confirm returned receipt and an existing file. Respect a user's “do not save” request.

The limited writer lives at `<native-root>/workflow/kb-writer.mjs`. Configure `HARNESS_KB_ROOT` as the authorized fixed vault for that process. It exposes only capture/checkpoint; it does not grant shell, arbitrary paths, deletion or sync. Registering its persistent access in a client requires the owner's actual approval. Use the client's official MCP instructions; no config is silently edited by this installer.

Read the copied capture/curate/cloud-exchange procedures before enabling sync. A private remote must be independently verified. Keep local capture, Git sync, API exchange, PC exchange and scheduled curation separate. Hourly PC sync and daily curation are preserved procedures, but activation and timezone belong to the new deployment. Preserve originals and conflicts; no force push or obligatory fictitious PR.

### UI detector

The configured engine is Impeccable0.1.14, Windows x64. Its official URL and expected SHA are in `manifest.json`. The original launcher is retained. On an authorized installation, obtain that exact engine into the declared asset path and verify SHA before use. Other platforms require a separately verified official equivalent. Missing automatic analysis stays missing; actual browser inspection is still required by the existing workflow.

### Native/client capabilities

Use [Compatibility](docs/COMPATIBILITY.md) to map operations to the client. Native generation, format skills, shell, file access and reviewer context separation must actually exist. Do not replace unavailable visual review with a hash pass or unavailable fresh review with author self-review. Keep useful independent work moving and report the precise dependent blocker.

## 6. Start a new session and exercise the selected route

Inspect the client's native skill catalog. Confirm paths point into this target, names/descriptions are complete and no unrelated same-name skill is silently substituted. Confirm the whole base block and selected workflow are loaded when full mode is active. Do not concatenate every reference into startup context: preserve original progressive disclosure.

Run an authorized representative task for the selected route. Use the real user brief and the original acceptance criteria. Examples:

- UI: primary action, visible correct result, invalid input recovery, preserved state, actual intended viewport.
- Voxel: inspected references/kit, coherent six-view preflight before detailed geometry, native exports and later matching-view inspection.
- Memory: capture/read-back/idempotent repeat/checkpoint; sync remains disabled until private remote approval/verification.
- Instructions: another agent can construct a concrete review brief and identify the next permitted step without reading a summary in place of the actual source.

The author runs its relevant checks. If a separate reviewer was explicitly selected, provide the original request, corrections, expected behavior, conditions, version/launch and agreed scope. Initial impressions precede author diagnoses. A repair does not automatically authorize another round; only an agreed next round uses a new fresh reviewer. A workflow experiment follows the single workflow-pilot procedure and is not an installation prerequisite.

## 7. Report the actual installation state

Report selected/requested modules, dependency closure, target/client, file integrity, actual discovery, executed helper/client scenarios, missing capabilities and limitations. Keep these separate from model quality and human acceptance.

Use these levels: files installed → integrity verified → client discovery verified → route executed → independent acceptance → human feedback. An early level cannot be relabeled as a later one. Same source bytes do not guarantee identical nondeterministic model output.

## Removal

Inspect `remove --dry-run` first. Actual removal deletes only matching owned files and the matching owned instruction block. Modified files stop removal; preexisting identical files, other project content and knowledge data remain. The installer performs no recursive directory delete. Do not use reset, force deletion or overwrite to clear conflicts.

## Instruction and output languages

The maintained agent instructions are English. The startup block for full and selected-skills installations explicitly defaults user communication and knowledge-base content to Russian. Honor a user's explicit language request for a particular output. Preserve exact paths, identifiers, schema keys and source quotations. Russian examples, stored knowledge and human-facing Russian documentation are intentional.

## Upgrade from 0.x to 1.0.0

Update this same checkout and keep its gitignored `.harness-state/receipts/` private store. Repeat the original `plan` and `install` commands with the same target, client, profile/skills, workflow flag and retained deployment bindings, then run `verify`. Omit retired lab flags; their old values are ignored during migration. `plan` reports `migration_from` and `obsolete_owned_files` without writing. Original skill names in `--skills` are aliases that warn on stderr; the plan and installed catalog use the new names. See the complete [rename table](CHANGELOG.md#100). Removed modules return an explicit error when requested directly.

The installer checks the destination receipt against its original private record, validates every old file and the managed startup block, replaces unchanged owned files, and removes only obsolete owned files. Renamed skills appear at their new paths; removed modules are retired. User neighbors, preexisting identical files and text outside the managed block remain intact, including BOM/CRLF. Edited or missing old files, a changed block, different options, missing private records or new-path conflicts stop the upgrade before writes. Resolve the reported conflict without deleting user content, then retry. A separate checkout needs an authorized transfer of the original private record; a destination receipt alone is insufficient. Empty old directories may remain. Back up the project and private receipts before upgrading; retain the 0.x checkout for recovery. No global client settings are changed.
