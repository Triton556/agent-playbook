---
name: product-engineering
description: Route and carry an end-to-end software task through the relevant planning, implementation, debugging, testing, and UI stages. Use for multi-stage development or requests to finish a product or feature. A narrow planning, bug, test, or design task can use its specialist skill directly. Excludes general research, creative writing, and household advice.
---

# Выбор инженерного этапа

Координатор выбирает профиль по ближайшему результату; общий порядок задачи принадлежит [WORKFLOW](../../workflow/WORKFLOW.md). Узкий запрос может сразу использовать нужный этап. Смена навыка не создаёт нового агента и не требует нового опроса/плана.

| Нужный результат | Вход |
| --- | --- |
| Требования, архитектурные варианты, исполнимый план | [product-planning](../product-planning/SKILL.md) |
| Работающая фича или интеграция | [product-implementation](../product-implementation/SKILL.md) |
| Причина сбоя, регрессии или flaky | [product-debugging](../product-debugging/SKILL.md) |
| Проверка поведения или ревью кода | [product-testing](../product-testing/SKILL.md) |
| UI-сценарий и визуальное решение | [product-ui-design](../product-ui-design/SKILL.md) |
| Фактический осмотр реализованного UI | [product-ui-review](../product-ui-review/SKILL.md) |
| Разрешённый разбор бинарника/протокола | [Обратная разработка](references/reverse-engineering.md) |

Для полной разработки связывай законченные сценарии и переходи по результату: достаточный план → рабочий срез → относящиеся проверки. UI подключает design до нового визуального решения и review после render. Неясный сбой направляется в debugging. Запрос только на план/ревью заканчивается этим результатом.

Общие процедуры открывай по их триггеру из WORKFLOW; не загружай весь набор. Навыки владеют предметными методами и источниками: [состав и адаптации](references/composition.md).
