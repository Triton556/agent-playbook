# Agent Playbook — workflow для агентов

Этот пакет переносит workflow версии 1.6.0 и 26 локальных навыков с полными текстами, справками, данными и помощниками. Можно подключить всё целиком, профиль или отдельный навык с его зависимостями. Модели и инструменты предоставляет выбранный клиент.

Главное требование: упаковка сохраняет метод, критерии и проверки. Тексты не заменяются краткими пересказами; изменение машинных путей и привязок явно фиксируется в manifest.json. Разные модели всё же могут давать разные результаты — равенство будущих работ не объявляется доказанным.

## Установка

**Сначала посмотрите [визуальный гид по профилям](docs/PROFILES.ru.md):** назначение харнесса, выбор по задаче и результаты между этапами — от шести видов робота до вращающейся модели.

Нужен Python 3.12+ (в том числе для проверки Windows junction). Для помощников состояния, памяти и сессий Codex нужен Node.js 22+. На Windows вместо `python` можно указать полный путь к своему интерпретатору.

```text
git clone https://github.com/Triton556/agent-playbook.git
cd agent-playbook
python harness.py plan --client codex --target ../мой-проект --profile full
python harness.py install --client codex --target ../мой-проект --profile full
python harness.py verify --client codex --target ../мой-проект
python harness.py doctor --client codex --target ../мой-проект
```

На Windows клонируй с `git clone -c core.longpaths=true https://github.com/Triton556/agent-playbook.git`: эта настройка включает длинные пути для вложенных ресурсов данного клона.

Активация и проверка установки: [INSTALL_FOR_AGENTS, раздел 6](INSTALL_FOR_AGENTS.md#6-start-a-new-session-and-exercise-the-selected-route) и [интеграция клиента](docs/INTEGRATIONS.md#codex-startup-budget-and-discovery).

Клиенты: `codex`, `claude`, `deepseek`, `generic`. Установщик записывает в проект, а не в глобальную конфигурацию клиента. Для полного режима он встраивает весь основной набор инструкций в управляемый блок AGENTS.md или CLAUDE.md, сохраняя существующий текст.

## Что подключать

| Цель | Выбор |
|---|---|
| Весь процесс | `--profile full` |
| Работа через Jam Board | `--profile jam-board` |
| Разработка | `--profile engineering` |
| UI, объяснения, визуальные миры | `--profile visual` |
| Воксельные ассеты | `--profile voxel` |
| Память | `--profile memory` |
| Работа над инструкциями | `--profile instructions` |
| Отдельный навык | `--skills dev-domain-model` или другое имя из `catalog` |

`creative-direction` помогает выбрать замысел до реализации: UI, игра, текст, видео, движение или 3D. Он входит в `full`, `engineering`, `visual` и `voxel`; при уже принятом направлении повторный поиск вариантов не требуется.

Клиент Codex и драйвер: [интеграция сессий](docs/INTEGRATIONS.md#agent-sessions-codex-for-orchestrators); общие правила: [agent-sessions](payload/skills/agent-sessions/SKILL.md).

`agent-sessions` обобщает это на любых исполнителей через адаптеры с единым [контрактом](payload/skills/agent-sessions/references/contract.md). В комплекте проверенный вживую адаптер `codex`, непроверенный `claude-code` и справка, как написать адаптер для другого клиента, например OpenCode или DeepSeek harness. Каждый адаптер сообщает, что на самом деле обеспечивают его режимы доступа, и отказывается от режима, который не может обеспечить. Входит в `engineering`, `instructions` и `full`, отдельно — `--skills agent-sessions`.

`you-are-brain` настраивает приватный профиль оркестратора и передаёт работу [agent-sessions](payload/skills/agent-sessions/SKILL.md). Входит в full, engineering, instructions и jam-board.

`--workflow` включает полный маршрут и все 26 модулей: иначе его ветки могли бы указывать на отсутствующие навыки. Перед записью `plan` показывает полный состав с зависимостями, включая вызовы навыка по имени. Отдельный навык получает небольшой блок с правилами доступа новой установки; весь общий маршрут при этом не активируется.

Подробнее: [руководство для установки агентом](INSTALL_FOR_AGENTS.md), [маршрут и загрузка контекста](docs/WORKFLOW_GUIDE.md), [интеграции, хуки и лимиты инструкций](docs/INTEGRATIONS.md). Установщик проверяет бюджет проектных инструкций Codex и конфликт AGENTS.override.md; он не обрезает текст и не меняет глобальный config.toml. MCP, доверие хукам и обслуживание собственной памяти настраиваются и проверяются отдельно по этому руководству.

## Jam Board

[Jam Board](https://github.com/Triton556/jam-board) — локальная настольная доска задач. Этот репозиторий — источник истины для навыка: мозг проводит интервью и планирует эпики → стори → задачи; исполнители берут Ready и отправляют отчёты; человек или другой назначенный мозг проверяет результат.

| Навык | Назначение |
|---|---|
| [`jam-board`](payload/skills/jam-board/SKILL.md) | Вести процесс playbook через подключённый MCP Jam Board, от планирования до приёмки |

```bash
python harness.py plan --client codex --target ../мой-проект --profile jam-board
python harness.py install --client codex --target ../мой-проект --profile jam-board
python harness.py verify --client codex --target ../мой-проект
python harness.py doctor --client codex --target ../мой-проект
```

Профиль jam-board включает доску и связанные процедуры; состав показывает plan. Подключение: [примеры](payload/skills/jam-board/references/connect.md). Модель и запуск: agent-sessions, Fixed rules и шаг 5.

## Порядок работы

Участие пользователя и выбор ревьюера: [task brief and acceptance, раздел 5](payload/skills/dev-flow/references/task-brief-and-acceptance.md#5-two-decisions-about-how-to-work).

Порядок осмотра: [human-perspective-review, Inspection sequence](payload/skills/dev-flow/references/human-perspective-review.md#inspection-sequence).

## Что нужно настроить у себя

Свежий ревьюер требует фактического разрешения владельца и инструмента нового контекста. Браузер, изображения, генерация изображений и документы требуют доступных инструментов клиента. Память использует свою разрешённую базу. Управление личной VM исключено из публичного пакета. Личные данные автора пакета не импортируются.

Для памяти можно создать пустую базу через `python harness.py init-memory --target ../мой-проект --client codex`. Синхронизация и расписание при этом не включаются. Подробности — в [установке для агентов](INSTALL_FOR_AGENTS.md) и [совместимости](docs/COMPATIBILITY.md).

Все проведённые проверки и ограничения указаны в [VALIDATION](docs/VALIDATION.md). Диспетчер и отменённые пять дополнений не возвращаются.

Языковые правила: [AGENTS](payload/AGENTS.md#goal-communication-and-boundaries); исключение для исполнителей: [brief-writing, Language](payload/skills/agent-sessions/references/brief-writing.md#language).

## Обновление 0.x → 1.0.0

Порядок обновления: [INSTALL_FOR_AGENTS, Upgrade](INSTALL_FOR_AGENTS.md#upgrade-from-0x-to-100).
