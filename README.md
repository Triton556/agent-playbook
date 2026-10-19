# Agent Playbook

An installable, modular workflow for coding agents, creative direction, human-centered UI review, visual experiments, voxel creation and durable knowledge. Version 1.0.0 includes 24 custom skills with the public dev-, ui- and agent- names, including orchestration through agent-sessions and agent-sessions-codex. Current configured instructions, references, datasets and helpers, including intent and preservation checks before building, are retained.

**[Русское описание](README.ru.md) · [Agent installation guide](INSTALL_FOR_AGENTS.md) · [Workflow guide](docs/WORKFLOW_GUIDE.md) · [Integrations and startup limits](docs/INTEGRATIONS.md) · [Compatibility](docs/COMPATIBILITY.md) · [Fidelity contract](docs/FIDELITY.md) · [Licenses](THIRD_PARTY_NOTICES.md)**

The client runs the model and supplies its tools. This package installs instructions and local helpers into a project. It does not add an autonomous model dispatcher, call paid APIs, change approval settings, register hooks or copy another owner's memory.

## Quick start

**See the process before installing:** [illustrated profile guide (Russian)](docs/PROFILES.ru.md) — what the harness does, which profile to choose, and the outputs between stages, including a six-view robot design and rotating voxel model.

Python 3.12+ is required for the installer, including Windows junction checks. Node.js 22+ is needed for task-state, knowledge and Codex session helpers. Use an explicit target project; the installer leaves your global client configuration alone.

```bash
git clone https://github.com/Triton556/agent-playbook.git
cd agent-playbook
python harness.py catalog
python harness.py plan --client codex --target ../my-project --profile full
python harness.py install --client codex --target ../my-project --profile full
python harness.py verify --client codex --target ../my-project
python harness.py doctor --client codex --target ../my-project
```

On Windows, clone with `git clone -c core.longpaths=true https://github.com/Triton556/agent-playbook.git` to enable long paths for this checkout's nested resources.

Start a new client session in `my-project`. Inspect the native skill catalog and run the relevant live acceptance scenario. `verify` proves installed file integrity. `doctor` reports missing/unverified capabilities; neither command proves future model quality.

For Claude Code use `--client claude`; for DeepSeek Harness use `--client deepseek`. Generic clients use `--client generic` and need an explicit discovery/bootstrap integration. See the compatibility matrix before claiming support.

## Complete workflow or selected skills

```bash
# One skill, with every linked sibling dependency and its supporting resources.
python harness.py install --client codex --target ../my-project --skills dev-domain-model

# Voxel pipeline and its dependency closure.
python harness.py install --client deepseek --target ../voxel-project --profile voxel

# Whole workflow: expands the selection to all 24 modules.
python harness.py install --client claude --target ../visual-project --profile visual --workflow
```

| Profile | Entry points |
|---|---|
| `full` | All 24 custom skills and the complete workflow bootstrap |
| `engineering` | Creative direction, planning, implementation, debugging, testing, UI, Codex session orchestration and supporting methods |
| `visual` | Creative direction, UI design/review, interactive experiments and voxel craft |
| `voxel` | Creative direction, voxel construction and linked methods/checks |
| `memory` | Find, save, status, sync and curation with the existing memory runtime |
| `instructions` | Agent-document editing, worker-session orchestration and references to the shared workflow-pilot procedure |

Dependencies can include several siblings. The plan shows requested and actually installed skills before writing. `--workflow` installs all 24 modules because the complete startup rules can route to any of them. Selecting a single skill without this flag does not activate the whole workflow. Bodies and resources are retained; references are loaded only when their original triggers apply.

`agent-sessions-codex` lets Claude, another Codex or any agent with the required local tools write a brief, start or continue a Codex thread visible in the Codex app, and check the result. It is selected by `full`, `engineering` and `instructions`, or separately with `--skills agent-sessions-codex`, including `--client claude`. The orchestrator proposes each session with its access mode and starts it only after the user agrees. Sessions require Node.js and an available Codex CLI using the user's own settings/history. See [session integration](docs/INTEGRATIONS.md#agent-sessions-codex-for-orchestrators).

`agent-sessions` generalizes this to any worker client through adapters with one [contract](payload/skills/agent-sessions/references/contract.md). It ships a live-checked `codex` adapter, an unverified `claude-code` adapter, and a guide for writing an adapter for another client such as OpenCode or a DeepSeek harness. Each adapter states what its access modes actually enforce and refuses a mode it cannot provide. It is selected by `engineering`, `instructions` and `full`, or with `--skills agent-sessions`.

## How the workflow works

1. Recover the real request, current decisions, feedback and allowed scope.
2. Resolve critical unknowns using sources, references or a bounded experiment.
3. Test an inexpensive coherent representation before expensive construction.
4. Create the requested outputs and preserve current state/evidence.
5. Inspect technical behavior, meaning and actual human-scale presentation separately.
6. The author checks the result and follows the selected human checkpoints. A separate reviewer runs only when explicitly chosen for this task, with agreed scope, stages and round limit.
7. Complete the declared scope and save transferable lessons with their limits.

The initial interview selects human participation (each meaningful iteration / first coherent sketch / autonomous) and separately whether a reviewer is needed. Autonomous work does not authorize delegation. An agreed reviewer uses a fresh context; a repair does not automatically create another round. One current observation may support several acceptance criteria. See [instruction ownership and pilots](docs/INSTRUCTION_MAINTENANCE.md).

## Knowledge and integrations

The memory profile includes the original capture/checkpoint/search/status/sync runtime and curation/cloud-exchange procedures. Initialize an empty authorized local vault with `init-memory`; existing files that differ are preserved. Private GitHub remote verification, hourly PC sync and daily curation require the new owner's real setup and consent. No previous owner's records, repository settings, credentials, schedule receipts or VM identities are bundled.

Browser/image inspection, image generation, document-format tools, a fresh context reviewer and separately authorized lab tools are **client capabilities**, not capabilities granted by a Markdown file. Missing checks remain unverified. See [Compatibility](docs/COMPATIBILITY.md).

## Preservation and removal

`manifest.json` binds every payload file to source/export hashes and records environment-binding changes. Existing different files stop installation before writes. Identical preexisting files are not owned by the installer. Repeat installation is idempotent; edited owned files stop verification/removal.

```bash
python harness.py remove --client codex --target ../my-project --dry-run
python harness.py remove --client codex --target ../my-project
```

Removal touches matching owned files and the matching managed instruction block. Other files, directories and knowledge data stay in place.

Keep this checkout's gitignored `.harness-state/receipts/`: the private ownership record is independent of mutable destination metadata. Missing/changed records stop verification and removal. It is local installation state and must not be published. See the migration and trust boundary in INSTALL_FOR_AGENTS.md.

## Validation and limits

```bash
python harness.py check-package
python -B -m unittest discover -s tests -v
```

Integrity, installation behavior, helper reproduction, actual client discovery, model behavior and human acceptance are separate claims. Preserve original acceptance criteria and compare actual artifacts on matched tasks before asserting quality parity. Model, reasoning effort, tools, context, permissions and input references can change outputs even when instructions are identical.

Detailed test evidence and limitations belong in [Validation](docs/VALIDATION.md). The old dispatcher and the reverted five-instruction experiment are not activated by this package.

Agent-facing instructions are maintained in English. User communication and knowledge-base content default to Russian, unless the user explicitly requests another output language. Exact data, identifiers and Russian human documentation retain their intended language.

## Upgrade from 0.x to 1.0.0

Update this same checkout and keep its gitignored `.harness-state/receipts/` private store. Repeat the original `plan` and `install` commands with the same target, client, profile/skills, workflow flag and retained deployment bindings, then run `verify`. Omit retired lab flags; their old values are ignored during migration. `plan` reports `migration_from` and `obsolete_owned_files` without writing. Original skill names in `--skills` are aliases that warn on stderr; the plan and installed catalog use the new names. See the complete [rename table](CHANGELOG.md#100). Removed modules return an explicit error when requested directly.

The installer checks the destination receipt against its original private record, validates every old file and the managed startup block, replaces unchanged owned files, and removes only obsolete owned files. Renamed skills appear at their new paths; removed modules are retired. User neighbors, preexisting identical files and text outside the managed block remain intact, including BOM/CRLF. Edited or missing old files, a changed block, different options, missing private records or new-path conflicts stop the upgrade before writes. Resolve the reported conflict without deleting user content, then retry. A separate checkout needs an authorized transfer of the original private record; a destination receipt alone is insufficient. Empty old directories may remain. Back up the project and private receipts before upgrading; retain the 0.x checkout for recovery. No global client settings are changed.
