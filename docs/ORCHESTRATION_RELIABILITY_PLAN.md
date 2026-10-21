# Adapter-session orchestration reliability plan

Status: implementation added in this PR. The original plan below is retained as the acceptance basis; live model behavior and active desktop adoption remain unverified.
Baseline: Agent Playbook 1.5.1, commit `4f283da3b076c31a23a49c7231b853c26d27ef21`.
Audit date: 2026-10-21.

## Problem and evidence

Selecting `you-are-brain` should route delegated work through `agent-sessions` adapters into separate, user-continuable sessions. Observed leading sessions instead called the client's built-in `spawn_agent`, including after initially using the correct adapter.

| Observation | What it establishes | Limit |
| --- | --- | --- |
| Package integrity passed for 312 payload files; installation verification passed for 313 installed files. | The inspected installation matched the package. | Hashes do not establish instruction following. |
| Three leading sessions called a built-in subagent after loading the adapter-only rule. One reloaded the rule after context compaction and still used the wrong mechanism. | Missing discovery or compaction alone does not explain the failures. | This is a historical sample, not a measured failure rate. |
| The inspected Codex host supplied competing built-in orchestration guidance. With CLI 0.160.1, read-only prompt rendering with `-c agents.enabled=false` removed that guidance and the built-in agent role. | A supported client configuration can remove the observed conflict from the rendered context. | No model was run with that override; desktop adoption and future versions require verification. |
| Six inspected adapter worker sessions had no built-in subagent calls; corrections used their existing thread IDs. | The sampled new-session/resume flow worked. | This does not establish general model compliance or live readiness everywhere. |
| One generated brief omitted the required audience assignment and explicitly requested a Russian final report to the orchestrator. | The leading agent introduced a language contradiction; the worker followed it. | Natural-language intent cannot be certified by a heading or a regex. |

Only generalized observations are published here. Private session IDs, transcripts, prompts, project material and installation paths remain outside this repository.

The current [execution rule](../payload/skills/agent-sessions/SKILL.md#fixed-rules) is already explicit. A skill cannot disable native tools or override higher-priority client instructions. Repeating the prohibition in more files is insufficient. Separately, a correct launcher does not repair a contradictory brief.

## Required outcome and boundaries

1. In the selected adapter-session mode, initial delegation and ordinary corrections use adapters; corrections resume the same worker session.
2. Detect or disclose incompatible host configuration before delegation instead of claiming that a skill has enforced it.
3. Preserve the selected execution mode, approved settings, worker identities and audience assignment across follow-ups and context recovery.
4. Keep recipient language separate from deliverable language: English worker-to-orchestrator communication by default; user-facing outputs follow the current owner's explicit choices.
5. Preserve actual authorization, model selection, access, independent-review rules, provider configuration, authentication and existing worker continuity.
6. Keep package integrity, diagnostic evidence, protocol behavior and observed model behavior as distinct claims.

This plan does not authorize installation, global configuration edits, new workers, paid evaluations, hooks, a dispatcher or a background service. A user's current explicit choice may override skill defaults within actual client capabilities and permissions; report that choice as a different mode.

## Implementation sequence

### 1. Establish host readiness before adapter delegation

Update [Codex integration guidance](INTEGRATIONS.md#agent-sessions-codex-for-orchestrators) and [compatibility claims](COMPATIBILITY.md). Add a bounded, read-only diagnostic through the existing `harness.py doctor` path or a linked helper.

- Distinguish the leading host from the worker backend. Disabling built-in agents only inside a newly started worker does not fix a leading host that still chooses `spawn_agent`.
- Check observable host version, selected mode and available configuration evidence. Use local prompt rendering only when supported; inspect the minimum needed signals and keep raw context private.
- Report `compatible`, `conflict` or `unverified` with evidence and limits. Adapter `verified: true` remains historical adapter evidence, not a certificate for the current host.
- A confirmed conflict must not silently fall back to a built-in subagent. Explain the integration requirement and continue independent authorized work. Missing diagnostic support must not be treated as a confirmed conflict or a pass.
- For the tested Codex version, document the supported option below and verify its effective scope/version before applying it. Let the owner select any persistent configuration change; preserve unrelated settings and verify in a fresh host session.

```toml
[agents]
enabled = false
```

The installer must continue to leave global client configuration unchanged. Do not bypass a denial, replace the user's configuration or change provider/authentication to achieve readiness.

Reference: [official Codex subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents). The observed diagnostic command was `codex -c agents.enabled=false debug prompt-input`; it rendered context without a model call. This is evidence for the tested CLI, not a portable command requirement for every client.

### 2. Route initial work and recovery through the existing policy owners

Use the [ownership map](INSTRUCTION_MAINTENANCE.md#ownership-map); do not copy the orchestration procedure into each entrypoint.

| Location | Proposed change |
| --- | --- |
| [payload/AGENTS.md](../payload/AGENTS.md#agents-and-selected-acceptance) and [WORKFLOW step 2](../payload/workflow/WORKFLOW.md#work-route) | Route a decision to delegate through the orchestration owner before selecting a launch mechanism. The current wording about opening it before separate sessions must not leave built-in delegation outside the trigger. Recovery restores the selected route and execution state. |
| [agent-sessions](../payload/skills/agent-sessions/SKILL.md) | Own the adapter-session requirement and readiness branch. Explain the required user-continuable lifecycle; avoid the outdated blanket claim that native subagents are never visible. Visibility alone does not make them the selected adapter route. |
| [you-are-brain](../payload/skills/you-are-brain/SKILL.md) and its [profile reference](../payload/skills/you-are-brain/references/brain-profile.md) | Treat setup as setup, then retain the task's selected mode. Use existing task state for task-only choices; save a private profile only when requested. Do not repeat the setup interview on each correction or infer a permanent profile from one task. |
| [running-and-checking](../payload/skills/agent-sessions/references/running-and-checking.md) | Recover the session table, pending run IDs, worker thread IDs, accepted scope and audience before the next launch. Resume normal corrections with the existing thread ID. Keep independent-review continuation rules separate. |
| [agent-sessions-codex](../payload/skills/agent-sessions-codex/SKILL.md) | Link to the host-readiness guidance and the shared execution owner; retain foreground/detached compatibility and explicit per-turn model, effort and access settings. |

Store execution metadata in the existing session log/task basis. Do not add a second registry or put the whole conversation into each follow-up. Preserve authorized session-launch consent and its existing limits; recovery must neither invent permission nor add a duplicate approval loop.

### 3. Check brief consistency before initial and follow-up launches

Keep [brief-writing](../payload/skills/agent-sessions/references/brief-writing.md#language) authoritative and update its intentional Codex mirror together.

- The initial brief identifies the recipient, communication language, deliverable languages, allowed scope and memory-writer assignment.
- Normal follow-ups inherit the original assignment and state only corrections, checks and authorized changes. A new language instruction must reflect an actual current owner choice.
- Review the complete brief for contradictions, including its final-report instructions. An English heading cannot compensate for a later instruction requiring a Russian worker report.
- Keep model/effort/access in launch arguments rather than treating prose as enforcement.
- Add a small dependency-free launch check for explicit, machine-checkable assignments and their inheritance. It must not require a full repeated template for short follow-ups, classify language from Cyrillic characters or claim to understand arbitrary prose. Keep semantic review with the leading agent.
- Reject clearly inconsistent explicit assignments before a process starts; allow exact Russian quotations, Russian UI/documents and explicit owner language exceptions.

Reuse existing launch paths and artifact storage. Do not turn this into a general prompt parser or impose a new task-management schema.

### 4. Verify behavior at the appropriate boundary

Extend existing test seams rather than adding a test framework.

| Scenario | Acceptance evidence |
| --- | --- |
| Conflicting host configuration | Read-only diagnostic distinguishes conflict from unavailable evidence; no worker starts as a diagnostic side effect and no configuration changes. |
| First adapter launch | An app-server stub records one `thread/start` and a `turn/start` on the returned thread; the selected settings and brief are passed through. |
| Ordinary correction | Stub records `thread/resume` with the original thread ID and the new brief; no replacement `thread/start`; settings remain explicit. |
| Recovery of a pending/completed run | Existing run/status metadata is consumed before any launch; already completed work is checked and is not duplicated. |
| Initial brief and short follow-up | Check missing/conflicting explicit assignments and inherited assignments; accept Russian deliverables/quotations and an actual owner override. |
| Existing transport behavior | Foreground, detach/wait/status/cancel, sandbox refusal and approval handling retain their contract-v2 behavior. |
| Packaging and preservation | Installation/removal, user-owned files, instruction links/mirrors, bindings, provenance and hashes remain valid. |

Primary locations: [tests/test_detach_wait.py](../tests/test_detach_wait.py), [tests/test_install.py](../tests/test_install.py) and [tests/test_instruction_ownership.py](../tests/test_instruction_ownership.py). Add focused helper tests only where the new diagnostic/check needs them. Assert observable outputs and protocol messages, not merely the presence of new policy wording.

Protocol stubs cannot prove that a model chooses the right tool after compaction. If the owner authorizes a bounded behavioral pilot, use the existing [pilot procedure](../payload/skills/dev-flow/references/workflow-pilot.md) for a fresh initial request, an ordinary correction and a context-recovery case. Record actual tool calls, continuity, recipient language, interventions and limits. No built-in subagent call is acceptable for the selected adapter-session cases. Keep new evaluations opt-in and separate from ordinary CI; label any unrun cases unverified.

### 5. Package and release only the implemented result

After implementation, update [fidelity](FIDELITY.md), [validation evidence](VALIDATION.md), affected integration/ownership documentation and `manifest.json` for changed payload files. Follow the repository's versioning practice without claiming that text/hash tests establish live reliability.

Run the existing package checks in an isolated workspace:

```sh
python harness.py check-package
python -B -X utf8 -m unittest discover -s tests -v
```

Verify clean installation and upgrade preservation for the affected selections. Record the tested client version, active host route and unperformed runtime/model checks. Do not merge or deploy as part of this plan.

## Completion criteria and recovery

The implementation is ready only when:

- The host's route is demonstrably compatible or its limitation is explicitly reported.
- Initial work and ordinary corrections satisfy the adapter/session continuity checks.
- Brief checks preserve recipient/deliverable distinctions and valid owner exceptions.
- Existing authorization, transport and installation behavior still passes.
- Documentation states precisely which deterministic and live checks ran.

For recovery, revert only the implementation's changed files and use existing verified installation receipts. Any optional client configuration change has its own recorded prior value and owner-approved rollback; never restore an entire global configuration over unrelated edits. Preserve existing worker threads, local profiles and user data.

## Implementation status

- Host diagnostic: `host-readiness.mjs`, linked from `harness.py doctor`; read-only supplied-preview evidence with explicit scope/version limits.
- Route/recovery: bootstrap and existing policy owners updated; bundled adapters and the legacy driver accept checked assignments and terminal-run recovery.
- Brief checks: explicit metadata validation and inherited snapshots; full-prose semantic review stays with the orchestrator.
- Deterministic regression coverage: `tests/test_orchestration.py` records protocol requests, pre-spawn refusals and recovery/output preservation. Existing transport and installer suites remain the regression baseline.
- Packaging/version/provenance: updated for 1.6.0. Executed results are in [validation](VALIDATION.md).
- Not executed: new paid model pilot, fresh desktop session acceptance or changes to the owner's installed/global configuration. These are distinct follow-up acceptance/deployment steps under their actual authorization.

