---
name: lab-vm-control
description: Control the user's fixed lab Linux VM through the existing bounded CLI or MCP, read host inventory and diagnose access. Use for these VMs and their sessions, not arbitrary shells, desktop GUI control or VPN Guard deployment.
---

# Lab VMs: CLI / MCP

Context and dated checks: [VM control MCP](<{{MEMORY_ROOT}}/PROJECTS/MCP управление VM.md>). History does not replace current authorization and state.

## Channel selection

- Inspect the actual tool catalog. When `rumi_health_probe` tools are available, use their supported schemas: `health({})`, `lab_inventory({})`, `lab_vm_status({vm:'linux'|'windows'})`; five guest tools are listed below. Host inventory may require ordinary UAC.
- Authorized guest actions can use the existing CLI `{{LAB_CLI}}`, Node `{{NODE}}`. Call `help` and `status` first. The CLI imports the same `guest-session.mjs` from `{{LAB_RUNTIME}}` without MCP transport. An absent MCP tool does not itself prohibit an already authorized CLI; label the result `local-cli`, not direct MCP.
- The CLI does not provide host inventory, Windows control, GUI or arbitrary deployment. State the specific boundary for an unavailable operation; do not invent a command, server or channel.

## Target and session

Linux: `{{LAB_VM_NAME}}`, VM UUID `{{LAB_VM_UUID}}`, MAC `{{LAB_VM_MAC}}`. Historical guest identity: hostname `debian`, UID 1000, Debian 13.7. Before a guest action, match fresh status, the exact VM/session and guest identity; require `state=ready`, an unexpired session and authorization for that operation. `guestAuthenticated=true` in a closed session is a historical field, not access. An identity mismatch requires stopping for diagnosis.

Use the explicit session ID from current status; never copy old IDs from reports. CLI `start` opens a temporary visible serial helper through ordinary UAC; it requires explicit agreement for this session and personal non-root login/F12, for at most 20 minutes. Do not read/save the password or console input. Do not automatically start when closed/not-ready. Perform already authorized ordinary read-only actions in a ready session without asking again.

CLI `write`/`close` require your own ownership receipt bound to `CODEX_THREAD_ID` and an explicit `--session`. Do not forge a receipt/identity or take over someone else's `alreadyOpen` session. Close only your own session; after authenticated close, verify `closed` and `cleanupVerified=true`. Preserve session ownership with MCP too.

## Actual calls

Without creating a session:

```powershell
$labCli = '{{LAB_CLI}}'
& '{{NODE}}' $labCli help
& '{{NODE}}' $labCli status
```

After verifying an authorized ready session, set `$labSession` to its real ID:

```powershell
& '{{NODE}}' $labCli command hostname --session $labSession --timeout-ms 5000 --max-output-bytes 4096
& '{{NODE}}' $labCli command id --session $labSession --timeout-ms 5000 --max-output-bytes 4096
& '{{NODE}}' $labCli read /etc/os-release --session $labSession
& '{{NODE}}' $labCli network --session $labSession
```

MCP equivalents (use the available tool's current schema):

- `linux_guest_session({vmId,action:'status',sessionId})` (also `start`/`close` within authorization).
- `linux_guest_command({vmId,sessionId,command:'hostname',timeoutMs:5000,maxOutputBytes:4096})`; the enum also includes `id`, `exit-test`, `timeout-test`, `output-limit-test`.
- `linux_guest_read_file({vmId,sessionId,file:'/etc/os-release'})`; also `test-marker`.
- `linux_guest_network_snapshot({vmId,sessionId})` — addresses/routes snapshot only.
- `linux_guest_write_test_file({vmId,sessionId,marker})` / CLI `write`: only an agreed nonsecret `MCP_LINUX_` + 32 hex marker in your own `/tmp/vpnguard-mcp-*`; no arbitrary files/overwrites.

Commands are restricted to the original enum, timeout 100..10000 ms, stdout/stderr separately 1..16384 bytes; reads up to 16 KiB, host deadline 25 s. Check JSON `ok`, `exitCode`, `timedOut`, `durationMs`, truncation and process exit. Exit 2=input, 3=backend, 4=session unavailable, 124=timeout; guest 1..255 propagate as process exit. Expected test exit 7 does not mean an ordinary command succeeded. Bound shell output and waits; do not copy full logs into the KB.

## Boundaries and blockers

The skill/CLI grants no new authority and does not guarantee every command complies with every policy. Network/WFP/VPN, accounts, credentials, ACL, getty enable/autologin, allowlists, hooks, endpoints, configuration and permanent access are outside these operations; changes require separate specific authorization and required confirmations. Do not bypass explicit sandbox/tool/approval denial through another channel. For a blocker, state verified transport, target, state/exit and the minimum permitted next step; do not repeat the same denial without new grounds.

Before changes, identify the current owner of the work; do not interfere with parallel processes, windows or networks without coordination. The user determines current scope; historical acceptance does not automatically authorize another start, reboot or test write.
