---
name: ui-ux-pro-max
description: "Targeted UI/UX reference for web, mobile, and desktop for product-ui-design and product-ui-review. Use when an interface task needs searchable accessibility, UX, palette, typography, chart, motion, or stack-specific guidance. Can also be requested directly. Existing product design takes precedence; skip household, research-only, and backend-only work."
---

# Адресный UI/UX-справочник

Поставляет рекомендации для выбранного UI-вопроса. [Product-ui-design](../product-ui-design/SKILL.md) владеет решением, [product-ui-review](../product-ui-review/SKILL.md) — фактическим осмотром. Поиск не создаёт отдельного интервью, реализации или приёмки.

Сначала сформулируй вопрос: доступность, сценарий, типографика, палитра, график, движение или особенность стека. Выполни один релевантный поиск; расширяй по непокрытому вопросу. CLI и доступные domains/stacks: `scripts/search.py --help`.

```text
python <skill>/scripts/search.py "keyboard focus in a dense desktop table" --domain ux --max-results 3
python <skill>/scripts/search.py "accessible dialog" --stack react --max-results 3
```

Используй существующий Python; не устанавливай другой интерпретатор ради примера. Короткий вывод обычно достаточен; `--json` или `--full` нужны для конкретных данных, а не по умолчанию.

Для действительно нового общего визуального направления доступен `--design-system`; это предложение для решения основного design-этапа, не обязательная генерация для каждой новой страницы. Существующие компоненты и принятая система переиспользуются. Не запускай параллельно конкурирующую систему из Taste или другого пресета.

Сохраняй результат только когда проекту нужен отдельный файл системы: `--persist --output-dir <project-root>`. Прочитай существующий MASTER/override до изменения; обычный запуск сохраняет их без перезаписи. `--force` требует разрешённой замены. Параметры variance/motion/density — опциональные подсказки; доступность, reduced motion, производительность и цель пользователя определяют выбор.

Заимствуй рекомендацию с основанием и областью применения, не весь набор. Данные и scripts остаются профильными источниками; они не доказывают качество будущего интерфейса. Лицензии/происхождение сохраняются в установленном пакете.
