# Профили Agent Playbook2.1

Профиль выбирает каталожные входы и их явно объявленные зависимости. Reference-only файлы и драйверы доставляются отдельно; файл на диске не означает прочитанный контекст.

| Профиль | Выбрано | Входов с зависимостями | Имена |
| --- | --- | --- | --- |
| full | 13 | 13 | agent-instructions, creative-direction, dev-debug, dev-plan, dev-verify, kb-curate, kb-find, kb-save, kb-status, kb-sync, ui-design, voxel-models, you-are-brain |
| engineering | 7 | 7 | agent-instructions, creative-direction, dev-debug, dev-plan, dev-verify, ui-design, you-are-brain |
| visual | 3 | 3 | creative-direction, ui-design, voxel-models |
| voxel | 2 | 2 | creative-direction, voxel-models |
| memory | 5 | 5 | kb-curate, kb-find, kb-save, kb-status, kb-sync |
| instructions | 2 | 2 | agent-instructions, you-are-brain |

`you-are-brain` — единый вход мозга: настройка, восстановление, выбранный native/adapter-маршрут. `ui-design` — проектирование и проверка через реальные действия пользователя. `dev-implement` не отдельный вход, его метод находится в reference планирования. `visual-scenes` не заменён новым навыком; предметные материалы остаются справочниками.

Воксельный маршрут сохраняет паспорт, шесть согласованных видов и проверку узнаваемой формы. Для UI зелёные unit-тесты не заменяют открытые модалки, проверенные состояния и читаемость.

```bash
python harness.py plan --client codex --target ../my-project --profile engineering
```

Установка — по [руководству](../INSTALL_FOR_AGENTS.md), изменения — [2.1](EXPLICIT_ROUTES_2.1.md). Проверки пакета не доказывают качество или соблюдение инструкций моделью.

Навык Jam Board устанавливается отдельно из приложения для выбранного проекта, без зависимости от этого плейбука.
