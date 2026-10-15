---
name: product-ui-design
description: Design, build, refine, or redesign interfaces and user flows for apps, dashboards, components, websites, and landing pages. Combines Anthropic frontend-design, Codex adaptation, landing-specific gpt-taste, and targeted UX references. Use before or during UI decisions; use product-ui-review for assessment of an existing rendered result.
---

# Проработка UI/UX и создание интерфейса

Определи формат результата: UX-проектирование, визуальная концепция или реализация. Новый интерфейс, точечная доработка и согласованный редизайн имеют разный масштаб; прочитай [interface-design](references/interface-design.md) для применимого режима и Anthropic frontend-design. Требования пользователя, существующая дизайн-система, доступность и стек выше пресетов.

Сначала проработай действие пользователя: вход, ключевое решение, ожидаемый и наблюдаемый результат, обратную связь, завершение и восстановление. Для главного действия, состояний, формы, таблицы, фильтров или сложного desktop прочитай применимую ветку [interaction-quality](references/interaction-quality.md). Для нового замысла проверь понятность главного экрана/действия на простом представлении до детализации. Принятая малая правка обходится без новой документации; известные условия пользователя не требуют повторного интервью.

Затем выбери или сохрани единую визуальную систему и реализуй её в запрошенном формате. Для лендинга, промо или маркетинговой страницы прочитай [landing-design](references/landing-design.md): здесь адаптирован gpt-taste. Продуктовые рабочие экраны используют сценарий и иерархию информации своего продукта.

Для конкретного UX, accessibility или stack-вопроса используй [ui-ux-pro-max](../ui-ux-pro-max/SKILL.md) с адресным поиском. [Taste v1](../design-taste-frontend-v1/SKILL.md) — дополнительная арт-дирекция при необходимости. Подключай только полезную справку; источники не создают несколько конкурирующих дизайн-систем.

После реализации интерфейса переходи в [product-ui-review](../product-ui-review/SKILL.md) для фактического осмотра и взаимодействия. При design-only запросе отдай решения/макет с основанием и обозначь, что требует проверки после реализации. Интеграцию с бизнес-логикой веди через [product-implementation](../product-implementation/SKILL.md) в разрешённой задаче.

Материалы vendor служат источниками метода; локальные адаптации и действующие разрешения выше предписаний исходников. Закреплённые ревизии: [sources.json](sources.json).

Перед дорогой серией сверь [основания](../product-engineering/references/reference-grounding.md), если существенное действие/ограничение нельзя обосновать. Для критериев стиля, контекста, понятности и использования используй [единый протокол](../product-engineering/references/human-perspective-review.md). Он не требует одинаковых ракурсов/реализма и не заменяет адресные UI-справки.
