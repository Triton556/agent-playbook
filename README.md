# Agent Workflow Harness

An installable, modular workflow for coding agents, human-centered UI review, visual experiments, voxel creation and durable knowledge. The package preserves the configured instructions, references, datasets and helpers instead of rewriting them into shorter prompts.

**[Русское описание](README.ru.md) · [Agent installation guide](INSTALL_FOR_AGENTS.md) · [Workflow guide](docs/WORKFLOW_GUIDE.md) · [Integrations and startup limits](docs/INTEGRATIONS.md) · [Compatibility](docs/COMPATIBILITY.md) · [Fidelity contract](docs/FIDELITY.md) · [Licenses](THIRD_PARTY_NOTICES.md)**

The client runs the model and supplies its tools. This package installs instructions and local helpers into a project. It does not add an autonomous model dispatcher, call paid APIs, change approval settings, register hooks or copy another owner's memory.

## Quick start

Python 3.12+ is required for the installer, including Windows junction checks. Node.js 22+ is needed for task-state and knowledge helpers. Use an explicit target project; the installer leaves your global client configuration alone.

```bash
git clone https://github.com/Triton556/agent-workflow-harness.git
cd agent-workflow-harness
python harness.py catalog
python harness.py plan --client codex --target ../my-project --profile full
python harness.py install --client codex --target ../my-project --profile full
python harness.py verify --client codex --target ../my-project
python harness.py doctor --client codex --target ../my-project
```

Start a new client session in `my-project`. Inspect the native skill catalog and run the relevant live acceptance scenario. `verify` proves installed file integrity. `doctor` reports missing/unverified capabilities; neither command proves future model quality.

For Claude Code use `--client claude`; for DeepSeek Harness use `--client deepseek`. Generic clients use `--client generic` and need an explicit discovery/bootstrap integration. See the compatibility matrix before claiming support.

## Complete workflow or selected skills

```bash
# One skill, with every linked sibling dependency and its supporting resources.
python harness.py install --client codex --target ../my-project --skills domain-modeling

# Voxel pipeline and its dependency closure.
python harness.py install --client deepseek --target ../voxel-project --profile voxel

# Whole workflow: expands the selection to all 23 modules.
python harness.py install --client claude --target ../visual-project --profile visual --workflow
```

| Profile | Entry points |
|---|---|
| `full` | All 23 custom skills and the complete workflow bootstrap |
| `engineering` | Planning, implementation, debugging, testing, UI and supporting methods |
| `visual` | UI design/review, interactive experiments and voxel craft |
| `voxel` | Voxel construction plus linked methods and checks |
| `memory` | Find, save, status, sync and curation with the existing memory runtime |
| `instructions` | Agent instruction writing and repeatable workflow creation |

Dependencies can include several siblings. The plan shows requested and actually installed skills before writing. `--workflow` installs all 23 modules because the complete startup rules can route to any of them. Selecting a single skill without this flag does not activate the whole workflow. Bodies and resources are retained; references are loaded only when their original triggers apply.

## How the workflow works

1. Recover the real request, current decisions, feedback and allowed scope.
2. Resolve critical unknowns using sources, references or a bounded experiment.
3. Test an inexpensive coherent representation before expensive construction.
4. Create the requested outputs and preserve current state/evidence.
5. Inspect technical behavior, meaning and actual human-scale presentation separately.
6. The author tests and briefs a **new independent reviewer**. The reviewer checks the real request and concrete expectations; the author verifies causes and fixes confirmed defects.
7. Complete the declared scope and save transferable lessons with their limits.

The author keeps technical tests. A reviewer is not automatically assigned the author's complete test suite. Initial impressions precede author self-assessments; a new acceptance round gets another fresh reviewer. Actual user authorization and client capabilities govern delegation.

## Knowledge and integrations

The memory profile includes the original capture/checkpoint/search/status/sync runtime and curation/cloud-exchange procedures. Initialize an empty authorized local vault with `init-memory`; existing files that differ are preserved. Private GitHub remote verification, hourly PC sync and daily curation require the new owner's real setup and consent. No previous owner's records, repository settings, credentials, schedule receipts or VM identities are bundled.

Browser/image inspection, image generation, document-format tools, a fresh context reviewer and restricted lab VM tools are **client capabilities**, not capabilities granted by a Markdown file. Missing checks remain unverified. See [Compatibility](docs/COMPATIBILITY.md).

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
