# Integrations

File installation is the first layer. The knowledge writer, hooks and the Codex worker route must be configured and exercised in the destination with the owner's approval; the installer never edits client configuration.

| Client | Skills folder | Startup instructions |
|---|---|---|
| Codex | `.agents/skills/<name>/SKILL.md` | AGENTS.md managed block |
| Claude Code | `.claude/skills/<name>/SKILL.md` | CLAUDE.md managed block |
| DeepSeek Harness | `.dsh/skills/<name>/SKILL.md` | AGENTS.md managed block |
| Generic | `.agent-harness/skills/<name>/SKILL.md` | AGENTS.md; needs its own discovery adapter |

## Codex startup budget and discovery

The installer checks the visible project instruction chain against a declared byte budget (default 32768) and refuses a target AGENTS.override.md that would shadow the installed block. If existing instructions make the block too large, pass `--project-doc-max-bytes 65536` to plan/install and start Codex with `-c project_doc_max_bytes=65536`; the installer option is a declaration, not a config change. Start a new session and check that the catalog lists the selected skills and the full startup block is loaded.

## you-are-brain: Codex workers from another host

`you-are-brain` lets a host agent (Claude Code, GLM or another client) start, continue and check Codex worker sessions. Codex itself uses its native agents. The route runs `skills/agent-sessions/adapters/codex.mjs`, which starts `codex app-server` on the user's own Codex home, so the threads appear in the Codex app. The host needs shell access, Node.js 22+ and a configured Codex CLI; `CODEX_BIN` can name the executable. Procedure: [session guide](../payload/skills/agent-sessions/references/session-guide.md); options, results and exit codes: [adapter contract](../payload/skills/agent-sessions/references/contract.md#run); access modes: [contract, Access modes](../payload/skills/agent-sessions/references/contract.md#access-modes); host readiness diagnostics: [contract, Host readiness](../payload/skills/agent-sessions/references/contract.md#host-readiness).

For acceptance, run a small authorized task, confirm the named thread is visible in the app, then continue the same thread and inspect its result.

## Limited knowledge writer (MCP)

`workflow/kb-writer.mjs` is a stdio MCP server with only `kb_capture` and `kb_checkpoint`. It requires `HARNESS_KB_ROOT` and loads `SYSTEM/scripts/kb.mjs` from that vault, so it always uses the vault's own runtime. The installation renders `runtime/integrations/codex-kb-writer.template.toml` with the real node, writer and vault paths; merge it into the Codex `config.toml` only with the owner's approval, preserving the rest of the file. Accepted `source.kind` values come from the vault's `kb.mjs`. Capture procedure: [kb-save](../payload/skills/kb-save/SKILL.md).

## Lifecycle hooks

`runtime/integrations/codex-hooks.template.json` registers the vault's `kb.mjs hook` on UserPromptSubmit (records the turn and gives the save/checkpoint instruction) and Stop (checks the completion mark, one continuation at most). Merge it into `.codex/hooks.json` with the owner's consent, preserving existing hooks; never copy another installation's trusted hashes. Claude Code uses `node <vault>/SYSTEM/scripts/kb-claude.mjs hook` in `.claude/settings.json`.

## Knowledge helpers

```bash
node <vault>/SYSTEM/scripts/kb.mjs status
node <vault>/SYSTEM/scripts/kb-search.mjs "specific project" --mode current --limit 8
node <vault>/SYSTEM/scripts/kb-coverage.mjs <vault>
node <vault>/SYSTEM/scripts/kb-navigation.mjs <vault>
```

Coverage and navigation audits need the vault's own SYSTEM/coverage and SYSTEM/navigation registries; SYSTEM/examples contains schema templates only. Sync and schedules: [kb-sync](../payload/skills/kb-sync/SKILL.md).
