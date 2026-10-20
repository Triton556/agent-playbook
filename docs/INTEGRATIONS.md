# Activate equivalent tools without inheriting access

File installation is the first layer. The original setup also has native tools, a limited knowledge writer, lifecycle hooks and scheduled maintenance. These must be configured and exercised in the destination. Missing enforcement is not full integration parity.

## Codex startup budget and discovery

The installer checks the visible project instruction chain against a declared byte budget, defaults to 32768, and refuses a target AGENTS.override.md which would shadow the installed block. It never shortens the original body to make it fit. Codex's actual instruction discovery, override precedence and default limit are documented in [AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

If an existing project's instructions make the complete block too large:

```bash
python harness.py plan --client codex --target /path/to/project --profile full --project-doc-max-bytes 65536
python harness.py install --client codex --target /path/to/project --profile full --project-doc-max-bytes 65536
codex --cd /path/to/project -c project_doc_max_bytes=65536
```

The installer option is a declaration, not a config change. The Codex launch override affects this invocation. Inspect actual global instructions, fallback names, repository ancestry and nested overrides too; a later working-directory change can select different instructions. In the desktop app use its supported configuration mechanism with the owner's agreement and confirm the effective value. No copied trust hash or imagined session configuration counts as proof.

Start a new session. Verify the catalog resolves the selected names to this project's native folders and that the full startup body, including its ending, is actually loaded. The tested Codex CLI0.160.0 catalog call is `skills/list` with the project `cwds` and `forceReload:true`; it requires no model-generation request. Catalog discovery is separate from startup/body interpretation and a live task result.

## Interpreter and shell

The original method references include Windows PowerShell examples. Adapt only shell quoting/invocation, preserving helper, arguments, input schema and criteria:

| Shell | Execute the actual Python interpreter |
|---|---|
| PowerShell | `& '/absolute/python.exe' '/absolute/script.py' ...` |
| bash/zsh | `'/absolute/python' '/absolute/script.py' ...` |
| Windows cmd | `"C:\absolute\python.exe" "C:\absolute\script.py" ...` |

`agent-worklog.mjs` invokes the same sibling `quality_ledger.py`. Set `HARNESS_PYTHON` to the actual executable if `python` on PATH is missing/different. Set this in the process environment, including any quality-hook process. Node and Python spawning must be permitted by the client's sandbox. A denied spawn remains an unavailable check; do not replace it with an unconditional success.

The preserved Impeccable context wrapper is PowerShell. A destination's signing/execution policy can reject it. Do not disable that protection to claim compatibility: follow the skill's existing unavailable-wrapper branch, read actual project context directly, and record the wrapper as unavailable. The verified standalone engine can supply permitted mechanical analysis; its upstream orchestration messages are source material and do not grant extra agents/access.

## agent-sessions-codex for orchestrators

`agent-sessions-codex` equips the host agent (Claude, another Codex or another client) to write a brief, start or continue work in Codex, and check the actual result. It is selected by `full`, `engineering` and `instructions`, or separately:

```bash
python harness.py install --client claude --target /path/to/project --skills agent-sessions-codex
python harness.py verify --client claude --target /path/to/project
```

Use `--client codex` for a Codex host. Read the installed `skills/agent-sessions-codex/SKILL.md` before launching. The host needs permitted shell/file access, Node.js 22+ and a configured Codex CLI with the user's account/settings. The driver finds `codex` on PATH or in supported desktop locations; `CODEX_BIN` can name the actual executable. No Codex binary, account, authentication or host configuration is installed by the harness.

Codex runtime/home/settings/history/hooks and continuation: see [agent-sessions-codex, Codex sessions and step 6](../payload/skills/agent-sessions-codex/SKILL.md#codex-sessions).

Launch: see [agent-sessions, step 5](../payload/skills/agent-sessions/SKILL.md#5-get-approval-with-a-summary). Access semantics: see [adapter contract, Access modes](../payload/skills/agent-sessions/references/contract.md#access-modes). Runtime limitations: see agent-sessions-codex, Known limits. Checking: see running-and-checking, Checking a finished session.

For runtime acceptance, obtain authorization for a small real task, confirm the named thread is visible in the app, then continue the same thread and inspect its actual result. Exercise memory only against the user's authorized setup if selected. Release 0.4.0 packaging checks do not launch sessions or independently reproduce the source owner's reported live trials.

## Limited memory MCP

Initialize the authorized vault with init-memory. Configure fixed HARNESS_KB_ROOT and discover the writer’s capture/checkpoint schemas through tools/list. Capture/identity/receipt handling: see [kb-save, Knowledge capture](../payload/skills/kb-save/SKILL.md#knowledge-capture).

Codex config example, **merge only after actual owner approval** in the appropriate local/project config; do not replace existing config:

```toml
[mcp_servers.harness_kb_writer]
command = "/absolute/node"
args = ["/project/.agents/workflow/kb-writer.mjs"]
env = { HARNESS_KB_ROOT = "/authorized/private/vault" }
```

For another client configure its stdio MCP transport with the same command/fixed environment; actual host approval is required. Agent capture procedure: see kb-save, Knowledge capture. Integration acceptance uses synthetic records to exercise initialize/list, capture, repeat, conflicting identity, checkpoint and unknown fields.

The portable guides use the server alias `harness_kb_writer`; the server reports `harness-kb-writer`. If choosing another alias, explicitly map the two discovered tool names for the agent. Version 0.3.0 uses the generic `source.kind=curator` for curator captures in both CLI and MCP; configure new producers accordingly. Existing saved records are not rewritten.

## Lifecycle hooks

The installed `runtime/integrations/codex-hooks.template.json` retains the actual three configured operations and their original limits/timeouts:

| Event | Operation | Expected behavior |
|---|---|---|
| UserPromptSubmit | Knowledge runtime `hook` | Record this turn and provide the short save/checkpoint instruction |
| Stop | Knowledge runtime `hook` | Check a real completion mark; one continuation if missing, no endless loop |
| Stop | `workflow/quality-stop.mjs` | Diagnose stale/incomplete declared work; bounded nonblocking message |

Review the rendered commands, vault/root/interpreter paths, event schemas and duplicate existing hooks. With owner consent, merge the template's hooks into the appropriate project `.codex/hooks.json` (preserve existing content). Native Codex must review/trust the exact current definitions. **Never copy another installation's `hooks.state` or trusted hashes.** Multiple hook sources are additive; inspect for duplicate registration. These rules come from [Codex Hooks](https://learn.chatgpt.com/docs/hooks).

Claude hooks use .claude/settings.json or .claude/settings.local.json under [Claude hooks](https://code.claude.com/docs/en/hooks). Map native fields and test real events; DeepSeek/generic support is not certified. Identity/persistence: see kb-save, Knowledge capture.

No hook registers during ordinary file installation. This keeps access changes reviewable. Full operational readiness requires the selected integrations to be authorized and tested.

## UI detector and other services

Acquire the pinned Impeccable engine from the exact official URL in `manifest.json`, verify its SHA256, and place it at the declared path. The Windows wrapper and original launcher are retained; set its skill/runtime location for the installed target. Version0.1.14 and its SHA are mandatory for the measured reproduction. Other platforms need their verified official engine equivalent. Browser/image inspection remains a separate requirement even with a working detector.

Use native image generation, rendered document/PDF/slide/spreadsheet tools and a genuine fresh-context review provider when a selected route requires them. The package does not copy provider internals, accounts or tool permissions. For a six-view concept an authorized native code representation is allowed when the original pipeline permits it; an uninspected placeholder is not an equivalent accepted concept.

## Knowledge maintenance

Memory service/schedule authorization and verification: see [kb-sync, Knowledge transport](../payload/skills/kb-sync/SKILL.md#knowledge-transport). Configure the deployment’s own timezone and scheduler; the daily INBOX filename convention retains Asia/Vladivostok and does not prove a scheduler exists.

Personal VM control is excluded from this public package. No source owner's VM, remote memory repository, credentials or scheduler grant is transferred.

## Retrieval and structural memory audits (0.2.0)

After explicit memory initialization, read-only search is available as:

```bash
node /authorized/private/vault/SYSTEM/scripts/kb-search.mjs "specific project" --mode current --limit 8
node /authorized/private/vault/SYSTEM/scripts/kb-search.mjs "past decision" --mode history --limit 8
```

Before audits, create deployment-owned SYSTEM/coverage/coverage.json and SYSTEM/navigation/parents.json using synthetic SYSTEM/examples as schemas. Prepare twelve fixed retrieval cases under SYSTEM/workflows/retrieval-quality.md. Source-owner registries/questions are excluded; semantic handling: see kb-curate, Knowledge curation.

Before curation/navigation audits, create your own SYSTEM/coverage/coverage.json and SYSTEM/navigation/parents.json. SYSTEM/examples contains synthetic schema templates; replace example sources/paths with real authorized records and topology. Define twelve fixed retrieval cases with expected topic/source, answer and caveat before the pilot in SYSTEM/workflows/retrieval-quality.md. The source owner's actual registries, questions and private notes are not distributed.

```bash
node /authorized/private/vault/SYSTEM/scripts/kb-coverage.mjs /authorized/private/vault
node /authorized/private/vault/SYSTEM/scripts/kb-navigation.mjs /authorized/private/vault
```

Receipt claim grades: see [human-perspective-review, Readiness and transfer](../payload/skills/dev-flow/references/human-perspective-review.md#readiness-and-transfer). Record selected layers: composition, actual startup/catalog, helper scenarios, writer receipts/lifecycle, viewer capabilities and selected runtime scenario; link each observation to the relevant procedure.

## Destination acceptance receipt

Record independently: installed selection/closure; package and installed hashes; startup body/end and effective budget; actual catalog; interpreter/helper scenarios; MCP real receipts; real lifecycle events/trust; viewer/image/format capabilities; fresh-review capability/consent only when selected; a representative authorized task and the actual observations, identifying self-review separately. Mark missing/unverified layers explicitly. The final owner verdict is its own evidence.

## Agent sessions for any worker

Shared orchestration policy: see [agent-sessions](../payload/skills/agent-sessions/SKILL.md), Fixed rules, Worker artifacts and steps 3–5. Worker language: see [brief-writing, Language](../payload/skills/agent-sessions/references/brief-writing.md#language). Session checking/status/reporting: see [running-and-checking](../payload/skills/agent-sessions/references/running-and-checking.md).

Adapters use [contract, Run](../payload/skills/agent-sessions/references/contract.md#run) for options/result/exit codes. Client-specific setup facts follow below; access semantics: see contract, Access modes.

- `codex`: Codex app-server, threads visible in the Codex app. Live-checked: new thread, continue, `read-only` refused a write, `workspace-write` refused a write outside the folder.
- `claude-code`: headless `claude -p` with permission modes (`plan`, `acceptEdits`, `bypassPermissions`) rather than an OS sandbox. Unverified. It needs a Claude Code CLI logged in on its own; the CLI bundled with the desktop app reports "Not logged in" when started separately.

For another client use [writing-an-adapter](../payload/skills/agent-sessions/references/writing-an-adapter.md). Launch authorization: see agent-sessions, step 5.
