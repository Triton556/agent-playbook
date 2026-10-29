# Agent Playbook 3.0

Небольшой личный набор навыков агента: мозг, который запускает рабочие сессии Codex, воксельные модели и база знаний. Модели и инструменты даёт клиент; установщик не запускает модели, не меняет глобальные разрешения и не регистрирует хуки.

[Установка](INSTALL_FOR_AGENTS.md) · [Интеграции](docs/INTEGRATIONS.md) · [Изменения](CHANGELOG.md) · [English](README.md)

## Навыки

- `you-are-brain` — разбиение задачи, брифы воркерам и сессии Codex через `agent-sessions/adapters/codex.mjs`.
- `voxel-models` — воксельные модели с предварительным дизайном, рецептами и инструментами для VOX и мешей.
- `kb-find`, `kb-save`, `kb-status`, `kb-sync`, `kb-curate` — база знаний; каждый навык — один самодостаточный `SKILL.md`.

## Установка

```bash
python harness.py plan --client codex --scope user --target <HOME> --profile full
python harness.py install --client codex --scope user --target <HOME> --profile full --memory-root <база>
python harness.py verify --client codex --scope user --target <HOME>
```

Профили: `full`, `brain`, `voxel`, `memory`. Удаление стирает только неизменённые файлы этой установки; сначала смотрите `remove --dry-run`.
