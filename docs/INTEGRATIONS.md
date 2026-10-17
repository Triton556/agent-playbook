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

## Limited memory MCP

Initialize the authorized vault first with `init-memory`. The writer needs a fixed `HARNESS_KB_ROOT`; it exposes only `kb_capture` and `kb_checkpoint`. It accepts structured source/session/turn identity, rejects unknown fields and suspected credentials, and returns a real local receipt. Its schemas are obtained through MCP `tools/list`.

Codex config example, **merge only after actual owner approval** in the appropriate local/project config; do not replace existing config:

```toml
[mcp_servers.danil_kb_writer]
command = "/absolute/node"
args = ["/project/.agents/workflow/kb-writer.mjs"]
env = { HARNESS_KB_ROOT = "/authorized/private/vault" }
```

For another client use its stdio MCP configuration with the same command, argument and fixed environment. The host decides tool approval. Persistent approval is a distinct owner choice; no configuration file grants it. Verify initialize/list, capture/read-back, identical repeat, conflicting identity rejection, checkpoint and unknown-field rejection. Do not test on genuine personal records.

The original guides name the server alias `danil_kb_writer`; retaining that component alias keeps native tool discovery consistent. It identifies the writer, not the vault's owner or an inherited access grant. If choosing another alias, explicitly map the two discovered tool names for the agent.

## Lifecycle hooks

The installed `runtime/integrations/codex-hooks.template.json` retains the actual three configured operations and their original limits/timeouts:

| Event | Operation | Expected behavior |
|---|---|---|
| UserPromptSubmit | Knowledge runtime `hook` | Record this turn and provide the short save/checkpoint instruction |
| Stop | Knowledge runtime `hook` | Check a real completion mark; one continuation if missing, no endless loop |
| Stop | `workflow/quality-stop.mjs` | Diagnose stale/incomplete declared work; bounded nonblocking message |

Review the rendered commands, vault/root/interpreter paths, event schemas and duplicate existing hooks. With owner consent, merge the template's hooks into the appropriate project `.codex/hooks.json` (preserve existing content). Native Codex must review/trust the exact current definitions. **Never copy another installation's `hooks.state` or trusted hashes.** Multiple hook sources are additive; inspect for duplicate registration. These rules come from [Codex Hooks](https://learn.chatgpt.com/docs/hooks).

Claude uses hooks in `.claude/settings.json` or `.claude/settings.local.json`, described in [Claude hooks](https://code.claude.com/docs/en/hooks). Translate configuration fields using current native documentation; do not assume Codex `commandWindows`, `additionalContextLimit`, diagnostics or identity fields are identical. Preserve the handler semantics and test real event input/output. DeepSeek/generic hook support is not certified by this package: map to a supported native mechanism and exercise it, or disclose missing lifecycle enforcement. Do not manufacture lifecycle or turn IDs.

No hook registers during ordinary file installation. This keeps access changes reviewable. Full operational readiness requires the selected integrations to be authorized and tested.

## UI detector and other services

Acquire the pinned Impeccable engine from the exact official URL in `manifest.json`, verify its SHA256, and place it at the declared path. The Windows wrapper and original launcher are retained; set its skill/runtime location for the installed target. Version0.1.14 and its SHA are mandatory for the measured reproduction. Other platforms need their verified official engine equivalent. Browser/image inspection remains a separate requirement even with a working detector.

Use native image generation, rendered document/PDF/slide/spreadsheet tools and a genuine fresh-context review provider when a selected route requires them. The package does not copy provider internals, accounts or tool permissions. For a six-view concept an authorized native code representation is allowed when the original pipeline permits it; an uninspected placeholder is not an equivalent accepted concept.

## Knowledge maintenance and laboratory access

Hourly PC Git synchronization and daily curation/cloud exchange are retained as procedures and helper code, with the original privacy/conflict/receipt checks. Configure your own verified private repository, timezone and actual scheduler. The runtime's daily INBOX filename convention currently retains Asia/Vladivostok; this is a naming convention, not evidence that a scheduler exists. Windows scheduled-sync installation is Windows-specific and is not executed by `init-memory`.

Lab control requires your own fixed authorized inventory and a provider meeting the original restricted operation/session/identity contract. Placeholder VM bindings are unconfigured. No source owner's VM, remote memory repository, credentials or scheduler grant is transferred.

## Retrieval and structural memory audits (0.2.0)

After explicit memory initialization, read-only search is available as:

```bash
node /authorized/private/vault/SYSTEM/scripts/kb-search.mjs "specific project" --mode current --limit 8
node /authorized/private/vault/SYSTEM/scripts/kb-search.mjs "past decision" --mode history --limit 8
```

Current/history ranking and separate INBOX results help select sources; they do not establish truth or recency. Read the actual matching records and retain source caveats. The original kb.mjs search stays available.

Before curation/navigation audits, create your own SYSTEM/coverage/coverage.json and SYSTEM/navigation/parents.json. SYSTEM/examples contains synthetic schema templates; replace example sources/paths with real authorized records and topology. Define twelve fixed retrieval cases with expected topic/source, answer and caveat before the pilot in SYSTEM/workflows/retrieval-quality.md. The source owner's actual registries, questions and private notes are not distributed.

```bash
node /authorized/private/vault/SYSTEM/scripts/kb-coverage.mjs /authorized/private/vault
node /authorized/private/vault/SYSTEM/scripts/kb-navigation.mjs /authorized/private/vault
```

Missing registries stop these checks as unconfigured. Structural zero errors only covers the records declared in the supplied registry; a template or empty registry is not evidence that a working vault is fully covered. These helpers read files and links, while semantic reconciliation remains a separate inspection. No hook, scheduler, remote or persistent tool approval is registered.

## Destination acceptance receipt

Record independently: installed selection/closure; package and installed hashes; startup body/end and effective budget; actual catalog; interpreter/helper scenarios; MCP real receipts; real lifecycle events/trust; viewer/image/format capabilities; fresh-review capability/consent only when selected; a representative authorized task and the actual observations, identifying self-review separately. Mark missing/unverified layers explicitly. The final owner verdict is its own evidence.
