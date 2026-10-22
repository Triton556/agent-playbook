# Agent Playbook 2.0

A project-local core workflow for brain/worker sessions, Jam Board, development, UI, creative direction, visual/voxel work and knowledge. The client provides models and tools; this package does not launch paid models, change global permissions or register hooks on installation.

**[Русский](README.ru.md) · [Install](INSTALL_FOR_AGENTS.md) · [2.0 inventory and migration](docs/CORE_CLEANUP_2.0.md) · [Integration](docs/INTEGRATIONS.md) · [Licenses](THIRD_PARTY_NOTICES.md)**

## Install deliberately

Python 3.12+ for installation; Node.js 22+ for the selected helpers. Inspect the plan first. Use an explicit project, not a global home.

```bash
python harness.py catalog
python harness.py plan --client codex --target ../my-project --profile engineering
python harness.py install --client codex --target ../my-project --profile engineering
python harness.py verify --client codex --target ../my-project
python harness.py doctor --client codex --target ../my-project
```

Clients: codex, claude, deepseek, generic. Profiles: full, engineering, jam-board, visual, voxel, memory, instructions. `full` or `--workflow` explicitly installs all 20 core skills and the full startup rules. Other profiles/`--skills` select entrypoints plus **explicit required dependencies**, not every skill mentioned in prose.

```bash
python harness.py plan --client codex --target ../my-project --skills you-are-brain
python harness.py plan --client codex --target ../my-project --skills dev-debug
```

The brain selection installs four skills; debugging installs two. Optional routes are used only if relevant and available. A file on disk is not a full body loaded at startup; skills metadata and client limits are separate.

## What remains

- Brain profile and resumable worker sessions: `you-are-brain`, `agent-sessions`, `agent-sessions-codex`.
- Jam Board planning, claims, reports and selected acceptance: `jam-board`.
- Development stages: `dev-flow`, `dev-plan`, `dev-implement`, `dev-debug`, `dev-verify`.
- Interface and creative work: `ui-design`, `ui-review`, `creative-direction`, `visual-scenes`, `voxel-models`.
- Knowledge: `kb-find`, `kb-save`, `kb-status`, `kb-sync`, `kb-curate`.
- Instruction editing: `agent-instructions`.

Version 2.0 removes six imported skills, bundled vendor workflows and the external UI detector. It retains useful local criteria, source attribution, privacy and permissions. Tests follow the changed behavior/risk; additional reviewers, interviews or full-suite reruns are not automatic. [Rationale and OpenAI guidance](docs/CORE_CLEANUP_2.0.md).

## Safety and upgrade

Retain the original checkout's private `.harness-state/receipts/`. Inspect upgrade `plan` with the same target/client/profile/bindings. Only unchanged owned obsolete files can be removed. Edited, unowned and unrelated files are preserved; conflicts stop before writes. No global Mac/PC settings are changed. Retired explicit skill names fail clearly rather than silently choosing another workflow.

```bash
python harness.py remove --client codex --target ../my-project --dry-run
```

Actual removal requires the user's scope. Knowledge data is not recursively deleted. No force/reset recovery.

## Verification

```bash
python harness.py check-package
python -B -m unittest discover -s tests -v
```

The suite exercises installation, migration, ownership protection, session helpers and explicit dependency selection. Integrity/behavioral helper tests do not establish model-quality improvement. No model benchmark or token savings is claimed from static byte counts. [Changelog](CHANGELOG.md).
