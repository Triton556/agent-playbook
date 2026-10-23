# Профили Agent Playbook 2.2

Профиль выбирает каталожные входы и их явно объявленные зависимости. Reference-only файлы и драйверы доставляются отдельно; файл на диске не означает прочитанный контекст.

| Профиль | Выбрано | Входов с зависимостями | Имена |
| --- | --- | --- | --- |
| full | 11 | 11 | agent-instructions, dev-debug, dev-plan, dev-verify, kb-curate, kb-find, kb-save, kb-status, kb-sync, voxel-models, you-are-brain |
| engineering | 5 | 5 | agent-instructions, dev-debug, dev-plan, dev-verify, you-are-brain |
| visual | 3 | 3 | creative-direction, voxel-models |
| voxel | 1 | 1 | voxel-models |
| memory | 5 | 5 | kb-curate, kb-find, kb-save, kb-status, kb-sync |
| instructions | 2 | 2 | agent-instructions, you-are-brain |

`you-are-brain` — единый вход мозга: настройка, восстановление, выбранный native/adapter-маршрут. UI-design и creative-direction удалены без замены другим дизайн-навыком. `dev-implement` не отдельный вход, его метод находится в reference планирования. `visual-scenes` не заменён новым навыком; предметные материалы остаются справочниками.

Воксельный маршрут сохраняет паспорт, шесть согласованных видов и проверку узнаваемой формы. Для UI зелёные unit-тесты не заменяют открытые модалки, проверенные состояния и читаемость.

```bash
python harness.py plan --client codex --target ../my-project --profile engineering
```

Установка — по [руководству](../INSTALL_FOR_AGENTS.md), изменения — [2.1](EXPLICIT_ROUTES_2.1.md). Проверки пакета не доказывают качество или соблюдение инструкций моделью.

Навык Jam Board устанавливается отдельно из приложения для выбранного проекта, без зависимости от этого плейбука.
