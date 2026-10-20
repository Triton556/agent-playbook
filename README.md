# Agent Playbook

An installable, modular workflow for coding agents, creative direction, human-centered UI review, visual experiments, voxel creation and durable knowledge. Version 1.4.0 includes 26 custom skills with the public dev-, ui- and agent- names, including orchestration through agent-sessions and agent-sessions-codex. Current configured instructions, references, datasets and helpers, including intent and preservation checks before building, are retained.

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

Activation and installation verification: see [INSTALL_FOR_AGENTS, section 6](INSTALL_FOR_AGENTS.md#6-start-a-new-session-and-exercise-the-selected-route) and [client integration](docs/INTEGRATIONS.md#codex-startup-budget-and-discovery).

For Claude Code use `--client claude`; for DeepSeek Harness use `--client deepseek`. Generic clients use `--client generic` and need an explicit discovery/bootstrap integration. See the compatibility matrix before claiming support.

## Complete workflow or selected skills

```bash
# One skill, with every linked sibling dependency and its supporting resources.
python harness.py install --client codex --target ../my-project --skills dev-domain-model

# Voxel pipeline and its dependency closure.
python harness.py install --client deepseek --target ../voxel-project --profile voxel

# Whole workflow: expands the selection to all 26 modules.
python harness.py install --client claude --target ../visual-project --profile visual --workflow
```

| Profile | Entry points |
|---|---|
| `full` | All 26 custom skills and the complete workflow bootstrap |
| `jam-board` | Jam Board planning, worker briefs, reports and review with the linked playbook procedures |
| `engineering` | Creative direction, planning, implementation, debugging, testing, UI, Codex session orchestration and supporting methods |
| `visual` | Creative direction, UI design/review, interactive experiments and voxel craft |
| `voxel` | Creative direction, voxel construction and linked methods/checks |
| `memory` | Find, save, status, sync and curation with the existing memory runtime |
| `instructions` | Agent-document editing, worker-session orchestration and references to the shared workflow-pilot procedure |

Dependencies can include several siblings. The plan shows requested and actually installed skills before writing. `--workflow` installs all 26 modules because the complete startup rules can route to any of them. Selecting a single skill without this flag does not activate the whole workflow. Bodies and resources are retained; references are loaded only when their original triggers apply.

Codex client prerequisites/driver: see [session integration](docs/INTEGRATIONS.md#agent-sessions-codex-for-orchestrators); orchestration policy: see [agent-sessions](payload/skills/agent-sessions/SKILL.md).

`agent-sessions` generalizes this to any worker client through adapters with one [contract](payload/skills/agent-sessions/references/contract.md). It ships a live-checked `codex` adapter, an unverified `claude-code` adapter, and a guide for writing an adapter for another client such as OpenCode or a DeepSeek harness. Each adapter states what its access modes actually enforce and refuses a mode it cannot provide. It is selected by `engineering`, `instructions` and `full`, or with `--skills agent-sessions`.

`you-are-brain` sets up a private brain profile, then follows [agent-sessions](payload/skills/agent-sessions/SKILL.md). Included wherever that skill is selected by a profile: full, engineering, instructions and jam-board.

## Jam Board

[Jam Board](https://github.com/Triton556/jam-board) is a local desktop task board. This repository is the source of truth for its skill: the brain interviews and plans Epic → Story → Task, workers claim Ready work and submit evidence, and a human or a different appointed brain reviews it.

| Skill | Use |
|---|---|
| [`jam-board`](payload/skills/jam-board/SKILL.md) | Run the playbook through the connected Jam Board MCP server, from planning to acceptance |

```bash
python harness.py plan --client codex --target ../my-project --profile jam-board
python harness.py install --client codex --target ../my-project --profile jam-board
python harness.py verify --client codex --target ../my-project
python harness.py doctor --client codex --target ../my-project
```

The jam-board profile selects the board and linked playbook procedures; see catalog/plan for closure. Connection: [examples](payload/skills/jam-board/references/connect.md). Model and launch policy: see agent-sessions, Fixed rules and step 5.

## How the workflow works

1. Recover the real request, current decisions, feedback and allowed scope.
2. Resolve critical unknowns using sources, references or a bounded experiment.
3. Test an inexpensive coherent representation before expensive construction.
4. Create the requested outputs and preserve current state/evidence.
5. Inspect technical behavior, meaning and actual human-scale presentation separately.
6. Participation and reviewer selection: see [task brief and acceptance, section 5](payload/skills/dev-flow/references/task-brief-and-acceptance.md#5-two-decisions-about-how-to-work).
7. Complete the declared scope and save transferable lessons with their limits.

Workflow procedure locations: see [ownership map](docs/INSTRUCTION_MAINTENANCE.md#ownership-map).

## Knowledge and integrations

The memory profile packages the runtime and curation references. Initialization: see [INSTALL_FOR_AGENTS, Knowledge](INSTALL_FOR_AGENTS.md#knowledge); transport and curation policy: see kb-sync and kb-curate.

Client capability requirements: see [Compatibility](docs/COMPATIBILITY.md). Claim grades: see [human-perspective-review, Readiness and transfer](payload/skills/dev-flow/references/human-perspective-review.md#readiness-and-transfer).

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

Validation claim grades: see [human-perspective-review, Readiness and transfer](payload/skills/dev-flow/references/human-perspective-review.md#readiness-and-transfer). [Fidelity](docs/FIDELITY.md#what-tests-can-establish) maps executed package checks to their limited claims.

Detailed test evidence and limitations belong in [Validation](docs/VALIDATION.md). The old dispatcher and the reverted five-instruction experiment are not activated by this package.

Language defaults: see [AGENTS](payload/AGENTS.md#goal-communication-and-boundaries); worker exception: see [brief-writing, Language](payload/skills/agent-sessions/references/brief-writing.md#language).

## Upgrade from 0.x to 1.0.0

See [INSTALL_FOR_AGENTS, Upgrade](INSTALL_FOR_AGENTS.md#upgrade-from-0x-to-100).
