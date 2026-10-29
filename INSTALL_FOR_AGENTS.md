# Installation procedure for an agent

The user chooses the client, the target and what to install, and authorizes access, costs and integrations. The installer writes only to the explicit project or user-home target, its private receipt store in this checkout and, on a separate request, the explicit knowledge vault. It does not edit client configuration.

Requirements: Python 3.12+, Node.js 22+ for the knowledge helpers and the Codex adapter, and a client that discovers local `SKILL.md` bundles. Read [integration setup](docs/INTEGRATIONS.md) for startup budgets, MCP and hooks.

## 1. Inspect the plan

```bash
python harness.py catalog
python harness.py plan --client codex --scope user --target <HOME> --profile full
```

Clients: `codex`, `claude`, `deepseek`, `generic`. Profiles: `full` (all 7 skills and the working rules), `brain` (you-are-brain), `voxel` (voxel-models), `memory` (the five kb-* skills). `--skills name1,name2` selects named skills. `--scope user --target <HOME>` installs into the native user folders; the default scope is a project folder.

Inspect the target's existing AGENTS.md/CLAUDE.md and skill folders. A different existing file stops installation before any write; resolve it with the user instead of deleting it.

## 2. Install and verify

```bash
python harness.py install --client codex --scope user --target <HOME> --profile full \
  --memory-root /path/to/existing/vault --memory-repo git@github.com:owner/private-vault.git
python harness.py verify --client codex --scope user --target <HOME>
python harness.py doctor --client codex --scope user --target <HOME>
```

Other bindings: `--cloud-memory-root`, `--curation-schedule`, `--evidence-root`. The working rules from `payload/AGENTS.md` are inserted into a managed block of AGENTS.md/CLAUDE.md; text outside the block stays. Repeating the same installation is idempotent. Keep this checkout's gitignored `.harness-state/receipts/` until removal: it is the ownership record for `verify` and `remove`.

## 3. Connect the knowledge base

An existing vault: clone its private repository and pass it as `--memory-root`. Its own `SYSTEM/scripts` stay authoritative; installation never overwrites the vault.

A new empty vault, only on request:

```bash
python harness.py init-memory --client codex --scope user --target <HOME>
```

It copies the memory runtime (the same scripts as the live vault) and creates an empty INDEX and connection template; it configures no remote and no schedule.

Codex writer: the installation renders `<native-root>/runtime/integrations/codex-kb-writer.template.toml` with the real paths. With the owner's approval, add its block to the Codex `config.toml`. The writer loads `kb.mjs` from the vault itself and exposes only `kb_capture` and `kb_checkpoint`. Memory hooks: `<native-root>/runtime/integrations/codex-hooks.template.json`; Claude Code uses the vault's `SYSTEM/scripts/kb-claude.mjs hook`.

## 4. Check in a new session

Open a new session, confirm the client lists the selected skills, and run one real task per route: a memory capture with read-back and an idempotent repeat; a you-are-brain launch of a Codex worker through `skills/agent-sessions/adapters/codex.mjs`; a voxel task through its design preflight. Report what ran, what did not and the missing capabilities.

## Removal and clean reinstall

Inspect `remove --dry-run` first. Removal deletes only unchanged owned files and the owned instruction block; edited files stop it. For a clean reinstall: remove with the same options, delete leftover folders from older versions only after the user confirms them, then install again and reconnect the existing vault.

Language policy: [working rules](payload/AGENTS.md); worker briefs: [brief-writing, Language](payload/skills/agent-sessions/references/brief-writing.md#language).
