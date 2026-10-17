---
name: product-implementation
description: Implement an agreed software feature, integration, application, or code improvement as working behavior across the required layers. Use for building from a clear brief or plan and for routine implementation decisions. Route unexplained failures to product-debugging and substantial open architecture to product-planning.
---

# Реализация

Вход — ясная задача либо сохранённый план; результат — работающий сценарий через нужные слои. Общий порядок требований, состояния и приёмки задаёт [WORKFLOW](../../workflow/WORKFLOW.md); не создавай вторую спецификацию.

Прочитай относящийся код и незакоммиченные изменения, найди существующие компоненты, контракты и команды проекта. Работай вертикальными срезами: действие пользователя → необходимые слои → наблюдаемый результат → проверка. Заверши полезный срез перед расширением поверхности; интегрируй заявленное поведение с реальными данными/логикой, обозначай демонстрационные заглушки.

Переиспользуй существующие модули. Для сложной границы адресно читай [codebase-design](vendor/matt-pocock/codebase-design/INSTRUCTIONS.md); для длинной реализации — [implement](vendor/matt-pocock/implement/INSTRUCTIONS.md). Они не добавляют обязательных агентов или публикаций.

- Новое UI-решение — [design](../product-ui-design/SKILL.md), после реализации — [review](../product-ui-review/SKILL.md).
- Неясный сбой — [debugging](../product-debugging/SKILL.md) с фактическим симптомом.
- Проверка поведения/кода — [testing](../product-testing/SKILL.md) по риску.

Специалист может использовать тот же актуальный результат проверки; его подключение не требует повторять уже покрытый сценарий. Источники: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
