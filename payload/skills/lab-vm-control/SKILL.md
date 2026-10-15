---
name: lab-vm-control
description: Управлять фиксированной лабораторной Linux VM пользователь через существующий ограниченный CLI или MCP; читать host inventory и диагностировать доступ. Использовать для этих VM и их сессий, не для произвольного shell, GUI компьютера или развёртывания VPN Guard.
---

# Лабораторные VM: CLI / MCP

Контекст и датированные проверки: [MCP управление VM](<{{MEMORY_ROOT}}/PROJECTS/MCP управление VM.md>). История не заменяет текущие разрешения и состояние.

## Выбор канала

- Проверь фактический каталог инструментов. Если доступны tools сервера `rumi_health_probe`, используй их штатную schema: `health({})`, `lab_inventory({})`, `lab_vm_status({vm:'linux'|'windows'})`; пять guest tools описаны ниже. Host inventory может потребовать обычный UAC.
- Для разрешённых гостевых действий доступен существующий CLI `{{LAB_CLI}}`, Node `{{NODE}}`. Сначала вызови `help` и `status`. CLI импортирует тот же `guest-session.mjs` из `{{LAB_RUNTIME}}`, без MCP транспорта. Отсутствие MCP-tool в каталоге само по себе не запрещает уже разрешённый CLI; результат называй `local-cli`, не direct MCP.
- CLI не предоставляет host inventory, управление Windows, GUI или произвольное развёртывание. Для отсутствующей операции сообщи конкретную границу; не изобретай команду, новый сервер или канал.

## Цель и сессия

Linux: `{{LAB_VM_NAME}}`, VM UUID `{{LAB_VM_UUID}}`, MAC `{{LAB_VM_MAC}}`. Историческая guest identity: hostname `debian`, UID 1000, Debian 13.7. Перед guest действием сопоставь свежий status, точную VM/session и guest identity; требуются `state=ready`, непросроченная сессия и разрешение на конкретную операцию. `guestAuthenticated=true` у закрытой сессии — историческое поле, не доступ. Расхождение identity — остановка для диагностики.

Используй явный session ID из текущего status; не копируй старые ID из отчётов. CLI `start` открывает временный видимый serial helper через обычный UAC; он требует явного согласования этой сессии и личного non-root login/F12, максимум 20 минут. Пароль и консольный ввод не читать/сохранять. Не запускай start автоматически при closed/not-ready. Уже разрешённые обычные read-only действия в готовой сессии выполняй без повторного вопроса.

CLI `write`/`close` требуют собственную ownership receipt, связанную с `CODEX_THREAD_ID`, и явный `--session`. Не подделывай receipt/identity, не присваивай чужую `alreadyOpen` сессию. Закрывай только свою сессию; после authenticated close проверь `closed` и `cleanupVerified=true`. Для MCP также сохраняй принадлежность собственной сессии.

## Реальные вызовы

Без создания сессии:

```powershell
$labCli = '{{LAB_CLI}}'
& '{{NODE}}' $labCli help
& '{{NODE}}' $labCli status
```

После проверки разрешённой ready-сессии установи `$labSession` в её реальный ID:

```powershell
& '{{NODE}}' $labCli command hostname --session $labSession --timeout-ms 5000 --max-output-bytes 4096
& '{{NODE}}' $labCli command id --session $labSession --timeout-ms 5000 --max-output-bytes 4096
& '{{NODE}}' $labCli read /etc/os-release --session $labSession
& '{{NODE}}' $labCli network --session $labSession
```

MCP-эквиваленты (бери актуальную schema доступного tool):

- `linux_guest_session({vmId,action:'status',sessionId})` (также `start`/`close` в согласованном объёме).
- `linux_guest_command({vmId,sessionId,command:'hostname',timeoutMs:5000,maxOutputBytes:4096})`; enum также `id`, `exit-test`, `timeout-test`, `output-limit-test`.
- `linux_guest_read_file({vmId,sessionId,file:'/etc/os-release'})`; также `test-marker`.
- `linux_guest_network_snapshot({vmId,sessionId})` — только снимок адресов/маршрутов.
- `linux_guest_write_test_file({vmId,sessionId,marker})` / CLI `write`: только согласованный nonsecret `MCP_LINUX_` + 32 hex marker в собственном `/tmp/vpnguard-mcp-*`; никаких произвольных файлов/перезаписи.

Команды ограничены исходным enum, timeout 100..10000 ms, stdout/stderr отдельно 1..16384 bytes; чтение до 16 KiB, host deadline 25 s. Проверяй JSON `ok`, `exitCode`, `timedOut`, `durationMs`, truncation и process exit. Exit 2=input, 3=backend, 4=session unavailable, 124=timeout; guest 1..255 передаются как process exit. Ожидаемый exit 7 теста не означает успешную обычную команду. Ограничивай shell-вывод и ожидание; полные логи не переносить в базу.

## Границы и блокеры

Навык/CLI не дают новых полномочий и не гарантируют соответствие любой команды всем политикам. Сетевые/WFP/VPN, accounts, credentials, ACL, getty enable/autologin, allowlist, hooks, endpoints, конфигурация и постоянный доступ не входят в эти операции; соответствующие изменения требуют отдельного конкретного разрешения и обязательных подтверждений. Не обходи явный отказ sandbox/tool/approval альтернативным каналом. При блокере укажи проверенный transport, target, состояние/exit и минимальный разрешённый следующий шаг; не повторяй тот же отказ без новых оснований.

Перед изменениями проверь текущего владельца работы; не вмешивайся в параллельные процессы, окна или сеть без координации. Нынешний объём определяет пользователь; исторический acceptance не разрешает повторный start, reboot или тестовую запись автоматически.
