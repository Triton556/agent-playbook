---
name: product-ui-design
description: Design, build, refine, or redesign interfaces and user flows for apps, dashboards, components, websites, and landing pages. Combines Anthropic frontend-design, Codex adaptation, landing-specific gpt-taste, and targeted UX references. Use before or during UI decisions; use product-ui-review for assessment of an existing rendered result.
---

# Проработка UI/UX

Этот этап владеет сценарием и визуальным решением; общие требования и точки участия берутся из [WORKFLOW](../../workflow/WORKFLOW.md) и сохранённого задания. Определи результат: UX-план, концепция или реализация. [Interface-design](references/interface-design.md) различает новую поверхность, доработку и редизайн.

До композиции установи действие, ожидаемый результат и восстановление. Новый сценарий, существенный редизайн или серия экранов используют [UI preflight](references/design-preflight.md): связанные состояния, достаточный макет/прототип и сохранённая основа. Маленькая правка использует принятую основу и затронутые состояния. [Interaction-quality](references/interaction-quality.md) — адресные критерии действия, формы, таблицы, фильтров или сложного desktop.

Используй одну дизайн-систему, начиная с компонентов и токенов проекта. Для нового дашборда/существенного редизайна сделай адресный поиск [UI/UX Pro Max](../ui-ux-pro-max/SKILL.md), просмотри полезные реальные примеры и свяжи выбранный приём с задачей. Для конкретного UX/accessibility/stack-вопроса достаточно его справки. [Taste v1](../design-taste-frontend-v1/SKILL.md) поставляет отдельный художественный приём по необходимости, без второй дизайн-системы и обязательной анимации.

Лендинг/промо использует [landing-design](references/landing-design.md). Рабочие экраны следуют своей продуктовой задаче. Условия пользователя, существующий бренд, доступность и стек определяют выбор выше рецептов.

После реализации передай основу и текущий UI в [product-ui-review](../product-ui-review/SKILL.md). Design-only заканчивается решениями/макетом и перечнем свойств, доступных только в реализации; интеграция поведения — [product-implementation](../product-implementation/SKILL.md) при соответствующем поручении. Источники и локальная адаптация: [sources.json](sources.json).
