---
name: product-planning
description: Plan a software product, feature, integration, or substantial redesign from a brief and repository context. Use for requirements, specifications, architecture tradeoffs, decomposition, and acceptance criteria before implementation. Produces a scoped plan; an existing clear plan or tiny fix does not need a new planning cycle.
---

# Планирование разработки

Результат — исполнимый план в масштабе задачи. [Задание и приёмка](../product-engineering/references/task-brief-and-acceptance.md) владеет опросом, сохранёнными ответами, режимами участия и критериями; используй ту же основу.

1. Установи пользователя, его действие и наблюдаемый результат. Проверь существенные предположения по репозиторию, документам и доступным источникам.
2. Найди точки интеграции, данные, контракты и ограничения. Сравни варианты только для решений с существенным влиянием на продукт, стоимость, сложность или обратимость.
3. Разложи реализацию на проверяемые пользовательские сценарии, зависимости и места изменений. Для рискованной миграции/выпуска укажи проверку и восстановление; незакрытые вопросы отдели от решений.

Для существенного UX-решения используй [product-ui-design](../product-ui-design/SKILL.md) в режиме проектирования. Термины/ADR подключают domain-modeling, когда это действительно часть результата. Материалы [to-spec](vendor/matt-pocock/to-spec/INSTRUCTIONS.md) — адресная справка; обязательные upstream-интервью и публикации не являются дополнительными этапами.

План связывает требование, место реализации и способ проверки. Ясная задача с готовым планом не получает новый цикл planning. При запросе только на план отдай его; в уже разрешённой полной разработке переходи к [реализации](../product-implementation/SKILL.md). Общие переходы и завершение — [WORKFLOW](../../workflow/WORKFLOW.md).

Источники: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
