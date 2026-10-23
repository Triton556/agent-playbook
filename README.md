> 2.2.0: explicit user-wide installation with `--scope user --target <HOME>` (Codex/Claude). [Clean installation](docs/CLEAN_INSTALL_FOR_AGENTS.md).

# Agent Playbook 2.2

A portable core workflow for brain/worker sessions, development, voxel work and knowledge. No UI-design or creative-direction skill. The client provides models and tools; this package does not launch paid models, change global permissions or register hooks on installation.

**[Русский](README.ru.md) · [Install](INSTALL_FOR_AGENTS.md) · [2.1 routes and migration](docs/EXPLICIT_ROUTES_2.1.md) · [Integration](docs/INTEGRATIONS.md) · [Licenses](THIRD_PARTY_NOTICES.md)**

## Install deliberately

Python 3.12+ for installation; Node.js 22+ for the selected helpers. Inspect the plan first. Choose an explicit user home with --scope user, or an isolated project with --scope project.

```bash
python harness.py catalog
python harness.py plan --client codex --target ../my-project --profile engineering
python harness.py install --client codex --target ../my-project --profile engineering
python harness.py verify --client codex --target ../my-project
python harness.py doctor --client codex --target ../my-project
```

Clients: codex, claude, deepseek, generic. Profiles: full, engineering, visual, voxel, memory, instructions. `full` or `--workflow` explicitly installs all 11 core skills and the full startup rules. Other profiles/`--skills` select entrypoints plus **explicit required dependencies**, not every skill mentioned in prose.

```bash
python harness.py plan --client codex --target ../my-project --skills you-are-brain
python harness.py plan --client codex --target ../my-project --skills dev-debug
```

The brain selection installs one catalog entry plus its technical support files; debugging installs one entry plus shared references. Optional routes are used only if relevant and available. A file on disk is not a full body loaded at startup; skills metadata and client limits are separate.

## What remains

- Brain profile and resumable worker sessions: `you-are-brain`; existing adapter/driver files are technical support, not separate catalog entries.
- Development stages: `dev-plan`, `dev-debug`, `dev-verify`; implementation is a shared planning reference.
- Voxel assets: `voxel-models`. UI design and creative-direction procedures are not included.
- Knowledge: `kb-find`, `kb-save`, `kb-status`, `kb-sync`, `kb-curate`.
- Instruction editing: `agent-instructions`.

Version 2.0 removes six imported skills, bundled vendor workflows and the external UI detector. It retains useful local criteria, source attribution, privacy and permissions. Tests follow the changed behavior/risk; additional reviewers, interviews or full-suite reruns are not automatic. [Rationale and OpenAI guidance](docs/CORE_CLEANUP_2.0.md).

## Safety and upgrade

Retain the original checkout's private `.harness-state/receipts/`. Inspect upgrade `plan` with the same target/client/profile/bindings. Only unchanged owned obsolete files can be removed. Edited, unowned and unrelated files are preserved; conflicts stop before writes. User scope changes only its native user instruction block and skills; other client settings remain unchanged. Retired explicit skill names fail clearly rather than silently choosing another workflow.

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

## Jam Board separation in 2.1

Jam Board owns its standalone project-local skill and MCP integration. Install that skill from the Jam Board application for the selected project/client; this playbook no longer ships it or adds brain/planning dependencies for it. Old `--profile jam-board` and `--skills jam-board` requests stop with this explanation instead of installing another profile.

During an upgrade of an existing playbook installation, unchanged receipt-owned Jam files are removed; modified managed files stop the upgrade before writes, and unowned files are preserved. Keep both versions and reconcile the reported files explicitly before retrying. Independently installed/global copies are not silently removed.

Clean replacement of an existing installation: [agent procedure](docs/CLEAN_INSTALL_FOR_AGENTS.md). Preserve original receipts, user edits and knowledge data.


KB procedures and the portable folder/index/leaf layout are supplied under the installed kb-* skills and kb-common references. An existing vault keeps its data and settings; updating the playbook does not overwrite its SYSTEM directory. New vault workflow files are compatibility pointers, not a second procedural authority.
