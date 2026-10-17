---
name: product-ui-review
description: Inspect and improve an existing rendered interface with Impeccable guidance and tools. Use after UI implementation, or for visual critique, polish, responsive checks, accessibility, interaction states, and UI readiness. Assess the changed surface at relevant viewports; initial design choices belong to product-ui-design.
---

# Проверка работающего интерфейса

Этот этап владеет фактическим render и действиями. Используй текущую [программу приёмки](../product-engineering/references/task-brief-and-acceptance.md); [visual-quality](references/visual-quality.md) задаёт один проход затронутой поверхности. Свободный осмотр дополняет критерии.

При наличии макета сравни ту же точку: маршрут, состояние, данные, размер/zoom. По [UI preflight, этап 4](../product-ui-design/references/design-preflight.md#4-сравнить-работающий-ui-с-основой) различай качество основы, перенос и работу сценария. При отсутствии макета проверяй доступные требования/текущую систему и отмечай этот пробел; ретроспективное описание не доказывает preflight.

Для поведения используй относящуюся ветку [interaction-quality](../product-ui-design/references/interaction-quality.md). Один фактический сценарий и его актуальное свидетельство могут покрыть UI, поведенческие и смысловые критерии; не выполняй его снова только из-за другого названия проверки. Восприятие/сохраняемое оценивается по [единому протоколу](../product-engineering/references/human-perspective-review.md), без второго общего осмотра.

В review-only выдай наблюдаемые находки и места. Разрешённые исправления следуют WORKFLOW; новый визуальный язык возвращается в [design](../product-ui-design/SKILL.md), неясная функциональная причина — в [debugging](../product-debugging/SKILL.md).

Impeccable — профильная справка/детектор, не второй обязательный аудит. Scripts содержит локальную context-обёртку без upstream-интервью и субагентов. Фактический осмотр выше абстрактного счётчика; стилистические предупреждения сопоставляй с брендом. Источники: [sources.json](sources.json), [binary.json](binary.json), [LICENSE](licenses/pbakaus--impeccable-LICENSE).
