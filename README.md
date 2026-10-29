# Agent Playbook 3.0

A small personal set of agent skills: a brain that drives Codex worker sessions, voxel models and a knowledge base. The client provides models and tools; the installer does not launch models, change global permissions or register hooks.

**[Русский](README.ru.md) · [Install](INSTALL_FOR_AGENTS.md) · [Integration](docs/INTEGRATIONS.md) · [Changelog](CHANGELOG.md)**

## Skills

- `you-are-brain`: task breakdown, worker briefs and Codex sessions through `agent-sessions/adapters/codex.mjs`.
- `voxel-models`: voxel assets with design preflight, recipes and mesh/VOX helpers.
- `kb-find`, `kb-save`, `kb-status`, `kb-sync`, `kb-curate`: the knowledge base; each is one self-contained `SKILL.md`.

## Install

Python 3.12+ for installation; Node.js 22+ for the helpers.

```bash
python harness.py plan --client codex --scope user --target <HOME> --profile full
python harness.py install --client codex --scope user --target <HOME> --profile full --memory-root <vault>
python harness.py verify --client codex --scope user --target <HOME>
```

Profiles: `full`, `brain`, `voxel`, `memory`. Removal deletes only unchanged owned files; inspect `remove --dry-run` first.

## Verification

```bash
python harness.py check-package
python -B -m unittest discover -s tests -v
```

The tests exercise installation, ownership protection, the Codex adapter, the knowledge writer and helpers. They do not establish model quality.
