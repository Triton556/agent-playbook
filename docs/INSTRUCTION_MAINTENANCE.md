# Instruction maintenance and ownership

Instruction placement and creator routing: see [agent-instructions, Pointers and authority](../payload/skills/agent-instructions/SKILL.md#pointers-and-authority).
Workflow experiments: see [workflow-pilot](../payload/skills/dev-flow/references/workflow-pilot.md).
The client-native creator and its validator are external capabilities; the former compatibility creator is excluded.
UI comparison: see [UI preflight, section 4](../payload/skills/ui-design/references/design-preflight.md#4-compare-the-working-ui-with-the-basis).
Voxel design: see [voxel preflight](../payload/skills/voxel-models/references/design-preflight.md).

## Ownership map

The rows below name policy locations, not additional procedures. The two shared orchestration references, requirements-interview.md and brief-writing.md, are intentional byte-identical mirrors; their agent-sessions paths are the logical owners. The Codex running-and-checking.md path is a compatibility pointer to its owner.

| Topic | Owning file and section | Characteristic phrase |
| --- | --- | --- |
| Model choice | [payload/skills/agent-sessions/SKILL.md#fixed-rules](../payload/skills/agent-sessions/SKILL.md#fixed-rules) | `The user chooses the model.` |
| Effort selection and changes | [payload/skills/agent-sessions/SKILL.md#3-choose-effort-and-access](../payload/skills/agent-sessions/SKILL.md#3-choose-effort-and-access) | `mechanical work across many files against a clear spec` |
| Session execution mechanism | [payload/skills/agent-sessions/SKILL.md#fixed-rules](../payload/skills/agent-sessions/SKILL.md#fixed-rules) | `Separate sessions, never built-in subagents.` |
| Worker-channel language | [payload/skills/agent-sessions/references/brief-writing.md#language](../payload/skills/agent-sessions/references/brief-writing.md#language) | `Write the brief in English` |
| Default output language | [payload/AGENTS.md#goal-communication-and-boundaries](../payload/AGENTS.md#goal-communication-and-boundaries) | `Communicate directly with the user in Russian` |
| Launch approval | [payload/skills/agent-sessions/SKILL.md#5-get-approval-with-a-summary](../payload/skills/agent-sessions/SKILL.md#5-get-approval-with-a-summary) | `This is the only session-launch approval gate` |
| Git action authorization | [payload/AGENTS.md#goal-communication-and-boundaries](../payload/AGENTS.md#goal-communication-and-boundaries) | `Commit, push and publication require` |
| Worker artifact publication | [payload/skills/agent-sessions/SKILL.md#worker-artifacts](../payload/skills/agent-sessions/SKILL.md#worker-artifacts) | `Briefs and worker reports are never committed or published` |
| Capture identity and persistence | [payload/skills/kb-save/SKILL.md#knowledge-capture](../payload/skills/kb-save/SKILL.md#knowledge-capture) | `give a new stage a new batch_key` |
| Worker memory assignment | [payload/skills/kb-save/SKILL.md#delegated-work](../payload/skills/kb-save/SKILL.md#delegated-work) | `Assign one writer per knowledge set` |
| Memory transport | [payload/skills/kb-sync/SKILL.md#knowledge-transport](../payload/skills/kb-sync/SKILL.md#knowledge-transport) | `Do not bypass a conflict with reset` |
| Semantic curation | [payload/skills/kb-curate/SKILL.md#knowledge-curation](../payload/skills/kb-curate/SKILL.md#knowledge-curation) | `Move INBOX originals to ARCHIVE with identical IDs` |
| Participation and reviewer selection | [payload/skills/dev-flow/references/task-brief-and-acceptance.md#5-two-decisions-about-how-to-work](../payload/skills/dev-flow/references/task-brief-and-acceptance.md#5-two-decisions-about-how-to-work) | `**Separate reviewer:** default to author self-checks` |
| Reviewer rounds and independence | [payload/workflow/independent-review.md#after-the-report](../payload/workflow/independent-review.md#after-the-report) | `An independent reviewer is not continued as a normal worker session` |
| Board acceptance | [payload/skills/jam-board/SKILL.md#brain-procedure](../payload/skills/jam-board/SKILL.md#brain-procedure) | `Board acceptance is by a human or an appointed brain` |
| Decision consent | [payload/skills/dev-flow/references/task-brief-and-acceptance.md#3-ask-only-what-changes-the-work](../payload/skills/dev-flow/references/task-brief-and-acceptance.md#3-ask-only-what-changes-the-work) | `silence is not an answer` |

Brain setup adds configuration only: [you-are-brain](../payload/skills/you-are-brain/SKILL.md) defers policy to agent-sessions.


Host diagnostic and checked assignment/recovery option semantics live in [the adapter contract](../payload/skills/agent-sessions/references/contract.md#host-readiness). Source integration setup links to that owner. Task recovery uses the existing session log; private assignment snapshots live in its existing run metadata, not a second registry. Bootstrap opens the execution owner before choosing a delegation mechanism, including after context recovery.
