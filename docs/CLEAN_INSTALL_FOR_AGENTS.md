# Clean installation for an agent

Use this procedure when the owner asks to replace their previous instruction/skill setup with a clean Agent Playbook installation. It is not a reset of the agent client, computer, project or knowledge base. Choose user scope for one global installation, or project scope for a deliberately isolated installation. Do not install both by default.

## Outcome and scope

Establish the actual client, selected project directory, requested release/commit, existing knowledge-vault location, and the owner's keep/remove choices. Reuse answers already supplied. Ask only when a target, file ownership or consequential access choice is genuinely unresolved; continue independent work while that decision is pending.

A full 2.2.x installation has 11 discoverable entries:

- `agent-instructions`
- `dev-debug`
- `dev-plan`
- `dev-verify`
- `voxel-models`
- `you-are-brain`
- `kb-find`
- `kb-save`
- `kb-status`
- `kb-sync`
- `kb-curate`

Jam Board is a separate application-owned integration, not a member of this list. The old `jam-board` profile/skill selection is retired. Install a separately versioned board skill only from a compatible Jam Board release; existing application releases may still expose the legacy playbook installer, which should not be used for this clean setup. Do not install an old board skill from a historical playbook or reintroduce it through dependencies. Application data and independent connections are outside a core cleanup unless explicitly included by the owner.

Technical reference/adapter directories may retain legacy names without `SKILL.md`. Their presence is not a duplicate skill. Judge discovery by entrypoints and the installed client's behavior, not directory names alone.

## 1. Inspect the active setup

Before writing, inspect the selected client's supported instruction and skill discovery for its actual installed version. Inventory:

1. User-level instructions and skills.
2. The chosen project's instructions, parent instruction chain, overrides and native skill paths.
3. Symlinks/junctions and plugins that expose duplicate skills.
4. Relevant old managed blocks, hooks and MCP registrations.
5. The old installer checkout, destination receipts and its private `.harness-state/receipts/` store.
6. Existing knowledge bindings and unsynchronized local records.

Use a short inventory with path, provenance, scope, active/inactive status and proposed disposition: keep, replace, quarantine or unresolved. Do not scan unrelated private projects or print credentials/configuration secrets. A copy in the old installer repository is not proof that it is active; a new local catalog is not proof that a global duplicate is inactive.

Project requirements such as build commands, architecture or design-system rules are not disposable merely because they share an `AGENTS.md` with an old managed block. Distinguish project knowledge from the general workflow being replaced. Respect the owner's explicit exceptions, such as retaining project-specific design-system skills and their necessary resources.

## 2. Make the cleanup reversible

Create a dated local backup/quarantine **outside every active discovery path**. Renaming a skill folder inside a scanned directory may leave its `SKILL.md` discoverable. Preserve original bytes, paths, link targets, changed configuration entries and the old trusted installer receipts. Write a small restoration manifest. Keep private backups out of source control and external reports; preserve existing access protections.

Do not erase client homes, credentials, accounts, histories, knowledge records, application databases or repository worktrees. Do not disable system/built-in skills or organizational controls as a shortcut to a smaller catalog. Avoid `reset --hard`, forced overwrites and recursive deletion of shared configuration directories.

### A. An intact managed installation exists

Use the original installer checkout with its trusted private receipt store:

```sh
<PYTHON> harness.py remove --client <CLIENT> --target <PROJECT> --dry-run
```

Inspect that plan, then use the same command without `--dry-run` within the owner's requested cleanup scope. Removal deletes only matching owned files and its matching instruction block; other project content and knowledge data remain.

If ownership records or current bytes disagree, stop that operation. Do not modify a receipt, hash or installed file to make removal pass. Preserve both versions and reconcile the conflict. A destination receipt alone is not a replacement for the trusted private record.

### B. An untracked or modified legacy installation exists

Do not pretend the managed remover verified it. Identify the old setup by evidence, preserve it, and quarantine only the owner-authorized, attributable files. In shared instructions/configuration, remove or replace the exact old block/entry rather than the entire file. An uncertain mixed-purpose file remains unresolved until ownership/scope is established.

Disable only attributable old hooks/plugin registrations in the requested scope. Preserve independent working integrations. A permission change, persistent credential configuration or new access still requires the host's applicable approval; this document is not such approval.

### C. The requested cleanup is actually an upgrade

A receipt-checked upgrade is also supported. Use the original checkout/private receipts, preserve deployment choices, inspect `plan`, and apply the current installer. Unchanged owned obsolete files are retired; edited files block before writes. Do not describe an upgrade that preserves independent old skills as proof of a completely clean catalog. See [the installation procedure](../INSTALL_FOR_AGENTS.md#upgrade-from-0x-to-100).

## 3. Pin and inspect the new package

Use the requested published release/tag and verify the immutable commit it resolves to. Use the requested release; a normal installation does not require a separate manual commit audit. Do not silently substitute an unpublished development branch. Preserve unsaved work in any existing checkout; use a separate clean checkout when appropriate. Keep the new checkout and its future private receipts available for removal/upgrade.

Read [INSTALL_FOR_AGENTS.md](../INSTALL_FOR_AGENTS.md), the selected bindings in [INTEGRATIONS.md](INTEGRATIONS.md), and applicable repository instructions. Follow relevant references, not every linked skill body.

Requirements are Python 3.12+ for the installer and Node.js 22+ for selected knowledge/runtime helpers. Use the real interpreters and shell quoting on this computer. In PowerShell, an absolute executable path is invoked with `&`; in bash/zsh invoke the quoted executable path normally. The angle-bracket tokens below are placeholders, not literal paths.

Run from the pinned checkout:

```sh
<PYTHON> harness.py check-package
<PYTHON> harness.py catalog
```

`check-package` verifies package integrity, not model behavior or user-flow quality.

## 4. Plan and install into the explicit target

For one user-wide installation, supported for Codex and Claude, use the user home as the explicit target and `--scope user` on plan/install/verify/doctor/remove. Codex skills go into `~/.agents/skills`, instructions into `~/.codex/AGENTS.md`; Claude uses `~/.claude/skills` and `~/.claude/CLAUDE.md`. Existing unrelated instruction text is retained. No project gets a copied installation. A non-default CODEX_HOME is reported rather than silently written to the wrong location.

```sh
<PYTHON> harness.py plan --client codex --scope user --target <HOME> --profile full --memory-root <VAULT>
<PYTHON> harness.py install --client codex --scope user --target <HOME> --profile full --memory-root <VAULT>
<PYTHON> harness.py verify --client codex --scope user --target <HOME>
<PYTHON> harness.py doctor --client codex --scope user --target <HOME>
```

For a deliberately project-local installation, omit `--scope user` and use the actual project:

```sh
<PYTHON> harness.py plan --client <CLIENT> --target <PROJECT> --profile full --memory-root <VAULT>
<PYTHON> harness.py install --client <CLIENT> --target <PROJECT> --profile full --memory-root <VAULT>
<PYTHON> harness.py verify --client <CLIENT> --target <PROJECT>
<PYTHON> harness.py doctor --client <CLIENT> --target <PROJECT>
```

Supported clients are `codex`, `claude`, `deepseek` and `generic`; discovery/integration support must be checked for the actual host. Do not install into all clients just because their directories exist.

Use the same verified bindings for `plan` and `install`. Supported optional bindings include `--memory-repo`, `--cloud-memory-root`, `--evidence-root` and `--curation-schedule`. Supply them only from the destination's verified configuration and authorization. A path or schedule string does not create a connection, scheduler or permission. Do not substitute the source author's environment.

Read the plan before writes. Resolve collisions without deleting user content to satisfy the installer. The full profile includes the four-rule BASE and the selected core; it does not install third-party UI bundles or a board integration. User scope adds its managed block to the native user instruction file; it does not change credentials, hooks, MCP configuration or schedulers.

An overriding instruction file or actual startup-budget problem needs a scoped resolution. Do not increase a limit and claim that it removed stale instructions. The installer budget option is a declaration; the effective client setting is separate.

## 5. Reconnect the existing knowledge base

Identify the vault from working configuration and local evidence. Read its own `AGENTS.md`, `README.md`, `INDEX.md` and the relevant capture/connector instructions. Verify local queued and unpushed changes before any synchronization. A file snapshot is not a Git clone. Never replace unsynchronized local records with a remote copy during setup.

For an existing vault:

- Bind its actual absolute path with `--memory-root`.
- Do not run `init-memory` over it or create a second empty default vault.
- Preserve raw records byte-for-byte; no mass curation, restructuring or chat import is part of installation.
- Preserve a working authorized CLI/MCP route; distinguish file installation from actual tool access.
- Use an existing schedule if it is in scope; do not duplicate hooks, background agents or scheduler entries.
- Keep a local-only work vault local. Do not attach a remote or transmit its contents merely to complete this checklist.

New memory initialization is a separate choice for a genuinely new, empty authorized vault. New persistent writer access also needs the host's actual approval. The limited writer uses a fixed `HARNESS_KB_ROOT`; it is not arbitrary filesystem access. Follow [the memory integration](INTEGRATIONS.md#limited-memory-mcp) for a selected writer, without silently editing client config.

Verify a narrow retrieval with a source file. The documented search helper can be used from the vault if present:

```sh
<NODE> SYSTEM/scripts/kb-search.mjs "a known topic" --mode current --limit 8
```

`kb.mjs status` updates local `STATUS.md`; do not label it read-only. Its local state does not prove synchronization to another machine. Test synthetic capture/idempotency on a disposable vault, not by filling the owner's live knowledge base with false facts. A real migration note may be saved only under the vault's current authorized capture procedure, with deduplication and read-back. Do not publish test data.

## 6. Verify fresh-session discovery and behavior

Use the actual client's supported catalog/reload mechanism, then start or ask the owner to start a fresh session in the selected project. Existing conversations may retain old instructions. A file's existence and a successful `verify` command do not prove runtime discovery or adherence.

Check these observable results:

- The requested core entrypoints resolve to the intended installation.
- Old global/project duplicate `SKILL.md` entries are not active.
- Built-in client skills are identified separately, not removed to force a count of 11.
- Retained project-specific skills and their referenced resources still resolve.
- The universal brain has no required board/story/epic procedure.
- Jam is absent from the core installation.
- No old override/managed block shadows or appends the removed workflow.
- The full managed startup block is discoverable, not truncated.
- Knowledge retrieval uses the correct vault and source.
- Preserved project content, credentials and independent integrations remain intact.

Check a small routing matrix without starting development or worker sessions solely for setup: a reproducible failure → `dev-debug`, orchestration → `you-are-brain`, knowledge lookup → `kb-find`, ordinary explanation → direct answer. Separate inspecting descriptions from observing an actual model choice. No paid A/B benchmark is implied.

If the task includes an actual interface change, acceptance must reproduce the human action and inspect its resulting state/readability; a passing package hash is not a UI test. For installation-only work, do not invent an unrelated implementation task to manufacture a pass.

## 7. Report and retain recovery information

Report:

1. Actual release/tag, commit, client and project target.
2. Attributable old components removed from discovery and exceptions retained.
3. Local backup location and scoped restoration steps, without secret contents.
4. Catalog entries actually observed in the fresh session and their source paths.
5. Knowledge path and separate read/capture/sync statuses.
6. Commands/scenarios executed, findings repaired and remaining `NOT_RUN` or blockers.
7. The smallest remaining action for the owner, if any.

Measure startup layers separately where observable: BASE, managed header/block, project/user instructions and skill metadata. Bytes or tokenizer estimates are not billed-token measurements or proof of faster/better model behavior. Keep raw private prompt previews out of repositories and reports.

Clean installation is complete only for the inspected scopes. Do not claim all projects or machines were cleaned after changing one target.


KB procedures and the portable folder/index/leaf layout are supplied under the installed kb-* skills and kb-common references. An existing vault keeps its data and settings; updating the playbook does not overwrite its SYSTEM directory. New vault workflow files are compatibility pointers, not a second procedural authority.
