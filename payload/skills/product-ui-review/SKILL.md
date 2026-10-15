---
name: product-ui-review
description: Inspect and improve an existing rendered interface with Impeccable guidance and tools. Use after UI implementation, or for visual critique, polish, responsive checks, accessibility, interaction states, and UI readiness. Assess the changed surface at relevant viewports; initial design choices belong to product-ui-design.
---

# Визуальная проверка и доводка

Прочитай [visual-quality](references/visual-quality.md) и выполни применимую проверку затронутой поверхности: реальный render, целевые размеры, главный сценарий, состояния и исправление существенных дефектов в разрешённом объёме. Для маленькой правки достаточно соответствующего компонента и состояний.

В review-only режиме выдай находки с наблюдаемым эффектом и местом. В разрешённой доработке исправь их и перепроверь. Новый визуальный язык или существенная переработка UX возвращаются в [product-ui-design](../product-ui-design/SKILL.md); функциональный баг с неясной причиной — в [product-debugging](../product-debugging/SKILL.md).

Impeccable принадлежит этому навыку: vendor содержит профильные справки и Windows launcher, scripts содержит локальную обёртку context. Загружай только нужную справку; обёртка возвращает факты о проекте и исключает upstream-директивы интервью и субагентов. Условия доступа и использования инструментов определяются действующими правилами.

Готовность подтверждают просмотренные изображения, проверенные действия и устранённые существенные дефекты. Отсутствие возможности запуска или осмотра указывай как непроведённую проверку. Стилистические предупреждения детектора оценивай относительно принятого бренда.

Закреплённый источник: [sources.json](sources.json). Проверенный engine и SHA-256: [binary.json](binary.json). Лицензия: [LICENSE](licenses/pbakaus--impeccable-LICENSE).

Для восприятия, сохранения стиля и интерпретации дефектов используй [единый протокол](../product-engineering/references/human-perspective-review.md). Первое считывание получает минимальный brief до авторских объяснений, затем проверяется действием/данными. При состояниях, вводе, таблице или фильтрах прочитай затронутую ветку [interaction-quality](../product-ui-design/references/interaction-quality.md). Выполни основной сценарий и относящийся к риску путь отказа/восстановления; статичный кадр не доказывает взаимодействие, задержку или эмоцию человека.
