---
name: product-testing
description: Verify software behavior and review code changes against requirements. Use for tests, regressions, TDD, test strategy, code review, and release-readiness evidence. Covers behavioral and code checks; rendered interface quality belongs to product-ui-review, and diagnosing a failing check belongs to product-debugging.
---

# Тестирование и ревью кода

Выбери результат запроса: проверка изменения, тесты/TDD или review-only. Установи ревизию/рабочий diff, включая относящиеся незакоммиченные изменения, требования и риск. Используй критерии из [сохранённой программы приёмки](../product-engineering/references/task-brief-and-acceptance.md), без новой спецификации.

## Проверка поведения

Проверь реальные команды проекта. Выполни применимые type/build/lint и сценарии, различающие правильное и ошибочное поведение. Выбирай минимальный достаточный набор; общий suite нужен по требованиям проекта или широте риска.

Новый тест наблюдает результат через публичную границу. Ожидаемое берётся из контракта/проверенного примера, а не повторения вычисления реализации. Используй реальные test seams; внешнюю недетерминированность изолируй без потери смысла проверки. Для финансовой логики тесты обязательны.

Для существенной регрессии добавь failing test до исправления, когда применимо. Для обратимой визуальной правки достаточно относящегося render/сценария и нужных существующих проверок. TDD: одно наблюдаемое поведение → red → минимальная реализация → green → уместный рефакторинг. Flaky требует данных об условиях и повторяемости, а не одного зелёного результата. Адресные справки: [tdd](vendor/matt-pocock/tdd/INSTRUCTIONS.md), [tests](vendor/matt-pocock/tdd/tests.md), [mocking](vendor/matt-pocock/tdd/mocking.md).

Наличие детали в коде не подтверждает её функцию/смысл. UI-сценарии и rendered evidence принадлежат [product-ui-review](../product-ui-review/SKILL.md); один текущий проход может покрывать оба набора критериев. Неясное падение передай в [debugging](../product-debugging/SKILL.md) с фактическим выводом.

## Ревью кода

Проверь текущий diff на требования, контракты и паттерны проекта; [code-review](vendor/matt-pocock/code-review/INSTRUCTIONS.md) открывай по необходимости. Находка содержит конкретный триггер, неверное поведение, влияние и место. Вкусовую рекомендацию отделяй от дефекта. Это самопроверка, если ты же писал изменение; skill не запускает другого агента.

В review-only режиме отдай находки и пробелы. Исправления, повтор затронутых проверок и завершение следуют [WORKFLOW](../../workflow/WORKFLOW.md). Отчёт связывает команды/сценарии, наблюдения и ограничения с текущей ревизией; непроведённое не получает pass.

Проверка самого workflow использует единый [пилот](../product-engineering/references/workflow-pilot.md) только при таком поручении. Источники: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
