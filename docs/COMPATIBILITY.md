# Client and capability compatibility

Layout support and executed client support are different claims. The installer retains bodies/resources and uses documented native locations:

| Client | Native project root | Startup instructions | Current claim |
|---|---|---|---|
| Codex | `.agents/skills/<name>/SKILL.md` | Project AGENTS.md full managed block | Layout implemented; actual discovery evidence reported separately |
| Claude Code | `.claude/skills/<name>/SKILL.md` | Project CLAUDE.md full managed block | Layout implemented; live model execution not established by file tests |
| DeepSeek Harness | `.dsh/skills/<name>/SKILL.md` | Project AGENTS.md full managed block | Flat native layout implemented; live model execution not established by file tests |
| Generic | `.agent-harness/skills/<name>/SKILL.md` | Project AGENTS.md | Requires a real native discovery/bootstrap adapter; no automatic compatibility claim |

Primary location references: [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code skills](https://code.claude.com/docs/en/skills), [DeepSeek local skill discovery](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md). Checked15October2026. Client versions can change; inspect the installed client before activation.

Claim grades and unavailable modalities: see [human-perspective-review, Readiness and transfer](../payload/skills/dev-flow/references/human-perspective-review.md#readiness-and-transfer).

## Required operations

| Operation | Required capability | If missing |
|---|---|---|
| Load actual source/feedback/current project | File/document reading and search | Dependent interpretation remains incomplete |
| Run local helper/tests | Permitted shell, Python/Node as needed | Record exact missing execution; source presence is not a pass |
| Orchestrate a user-requested Codex session visible in the app | Host shell/file access, Node.js and a configured local Codex CLI using the user's own home/settings | Skill files alone do not establish CLI availability, app visibility or live execution |
| Inspect image/model/document | Actual image or rendered artifact inspection | Visual acceptance remains unverified |
| Inspect UI/animation | Browser/computer interaction and actual temporal observation | Static/source checks do not satisfy behavior or motion |
| Generate an AI bitmap concept | Authorized image generation tool when that method is chosen | Use another permitted design representation where the original branch allows it; otherwise report missing modality |
| Independent review | Session provider under agent-sessions; context under independent-review | See human-perspective-review, Readiness and transfer |
| Knowledge persistence | Own authorized vault or limited MCP writer | No fictitious saved receipt |
| Private sync/cloud curation | Verified private remote, authorized transport and scheduler if requested | Keep local data; exchange/schedule remains unconfigured/unverified |
| External laboratory integration | A separately supplied, authorized provider | Personal VM control is excluded from the public package |
| Document/PDF/presentation/spreadsheet work | Relevant available native format skill/tool and render checks | Install/authorize a suitable provider before claiming that route works |

The package does not redistribute proprietary native plugins or credentials. Native `skill-creator`, document/image tooling and client computer-use interfaces are provider dependencies. The common route preserves their role rather than assuming they are universally installed.

`agent-sessions-codex` installs into the selected host's native skill root, including `.claude/skills/agent-sessions-codex` for Claude and `.agents/skills/agent-sessions-codex` for Codex. Its execution backend is the separate local Codex CLI. Any other host must actually discover the skill and supply the required tools; see [session integration](INTEGRATIONS.md#agent-sessions-codex-for-orchestrators).

## Fresh reviewer adapters

Reviewer execution: see [agent-sessions, Fixed rules](../payload/skills/agent-sessions/SKILL.md#fixed-rules); scope, staging and rounds: see [independent-review](../payload/workflow/independent-review.md). Selection: see task brief and acceptance, section 5.

## Context parity

Full mode places the whole base rules inline in startup instructions, then preserves route/skill/reference loading by the existing triggers. Selected skills retain full bodies and resources. Do not replace the base with an optional unread pointer, summarize a pipeline, load every reference unconditionally or introduce a deterministic dispatcher.

Same model/effort, context, available tools, permissions, task inputs/references and native provider versions provide the closest conditions. They are controls, not a guarantee of identical creativity or successful human perception. Validate actual matched tasks before asserting equivalence.

Codex startup byte budgets, overriding instruction files, shell/interpreter conversion and actual tool/hook registration are covered in [Integrations](INTEGRATIONS.md). All four layouts are installer-tested; only Codex CLI catalog discovery is presently executed. No live Claude/DeepSeek/generic model equivalence is claimed.

Native skill-creator, template-creator and skill-installer are external client capabilities, not bundled modules. Verify availability before selecting one; an unavailable native creator is not an installed success. The bundled writing guidance and shared pilot do not emulate a provider-native packaging or template API.
