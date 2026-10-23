# Long-task state and completeness

Use the existing project plan. When a verifiable graph/output series is needed, use local `.workflow/task-<id>.json` through `{{HARNESS_ROOT}}/workflow/agent-worklog.mjs`. A short task needs no separate file. The tool reads stdin JSON, operates in the current project, launches no models/network and expands no access. For a linked ledger, it calls only the fixed supported validator without a shell.

Record the brief path/version under existing decisions/next fields, without a new schema field. When used, machine state owns progress/relationships, the plan owns requirements, and an optional ledger owns detailed evidence. Use paths/IDs and necessary hashes rather than copied values. Session execution metadata: see [running-and-checking, Before starting](../../agent-sessions/references/running-and-checking.md#before-starting). Loading/recovery: see WORKFLOW, Context loading and recovery.

## Compatible short format v1

`command=state`, `state` field: schema_version=1, task_id and five fields: result — result; scope — agreed actions/boundaries; decisions — accepted decisions; next — step with its criterion; blocker — specific dependency or empty string. The old format and events remain supported. Legacy state supports continuation but does not establish verified series completeness.

Recovered records and consent: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

## Graph and outputs v2

Long/serial work retains the five v1 fields and adds:

- `status`: in_progress, blocked, ready, complete, paused, cancelled. Paused/cancelled reflect user instructions; diagnostics do not restart them.
- `session_id`: actual chat identifier when known. Diagnostics bind only to this chat/project; do not select neighboring tasks by file time.
- `approved_actions`: optional `{id,action,resource,conditions,source:{kind:"user",reference}}` records of real consent. Authority: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).
- `outputs`: declared in advance as `{id,status,required?,path?,sha256?,rationale?}`. Status: pending, ready, not_applicable. Ready requires an existing file/hash; not_applicable requires a reason. Do not remove a mandatory output to get green; changing the list requires grounds in scope.
- `stages`: `{id,status,required?,skill?,dependencies,output_ids,inputs,evidence,observation?,rationale?}`. Status: pending, in_progress, pass, partial, failed, blocked, not_applicable. Inputs/evidence are `{path,sha256}` arrays. Pass requires current inputs, evidence and an observation; nonapplicable requires a reason. References/graph are checked; cycles are prohibited.
- `dependency_policy`: conservative by default — a changed linked file requires rechecking the entire passed set. Declared requires `independence:{observation,files:[{path,sha256}]}` documenting actually tested independence. A stale record restores conservative mode. Under declared independence, recheck affected stages and descendants.
- `quality_ledger`: optional relative path to an existing ledger. The inspector additionally calls its fixed validator within the project.
- `blocker_kind`: timeout, access, validation, external or user. A blocker does not authorize access; independent stages may continue.

Paths are relative to the project root, with no escape or links/junctions. For files larger than 128 MiB, use an appropriate project check/ledger and its evidence. Declared dependencies do not prove their own completeness.

Task_id is unique within a project; use a unique suffix across chats. Another chat cannot overwrite state with session_id or remove its ownership. For a real handoff, the new chat reads prior state, transfers authorized context and creates its own identity. Changing the mandatory list requires `manifest_change:{reason,source:{kind:"user",reference}}` with real grounds; the field does not grant consent. A mandatory output is linked to a stage; replacing v2 with v1 to bypass validation is prohibited.

## Commands and transitions

Pass JSON through stdin to the existing Node from the project root:

```text
{"command":"snapshot","paths":["source/file","output/file"]}
{"command":"state","state":{...}}
{"command":"inspect","task_id":"task-id"}
{"command":"metrics"}
```

Snapshot returns SHA256. Inspect returns output/stage freshness, reasons for incompleteness and runnable next steps. Partial, missing, stale, failed and blocked results are distinct. Ready/complete and task-done for v2 are rejected when incomplete/stale. The tool checks records/files, not whether an inspection really happened.

Stage handoff: artifact/revision, evidence, status, open issues and next step. Repair/recheck: see WORKFLOW, Check, repair and finish; authorization and user stop: see AGENTS, Goal, communication and boundaries. The graph controls local transitions; it is not a background model executor.

## Events and metrics

`command=record`, `event` field: task_id, stable event_id and event: task-start, task-done, question, manual-nudge, blocker, reference, interruption or human-feedback. Repeating an identity is idempotent; different content with the same identity is rejected. Messages/secrets are not recorded.

Question.kind: repeated, clarification, new_scope, technical. Blocker.type: timeout, access, validation, external. Interruption.kind: connection, user, external. Task-done requires verified=true and a ready v2 manifest if one exists. Duration_ms is optional; absence is not zero. Stage: existing context/implementation/review/memory/approval/tool plus references/preflight/verification.

Metrics returns counts and the repeat denominator: repeated + clarification + new_scope; technical questions are separate. A zero denominator yields rate=null. The source is agent labeling; completeness is unknown until checked. Other metrics: [workflow-pilot](workflow-pilot.md).

## Completion and diagnostic hook

Before finishing, check mandatory outputs, criteria and material defects. For a ledger, run `quality_ledger.py validate <ledger> --root <project> --require-ready`. Result grades: see [human-perspective-review, Readiness and transfer](human-perspective-review.md#readiness-and-transfer).

`quality-stop.mjs` is an optional Stop diagnostic for this session_id/cwd's active v2 state. It warns without blocking, continuing the chat or reading transcripts; the same unchanged failure is not repeated. A hook file does not establish trust/activation: Codex requires review/trust of its exact definition. Pre-delivery checks remain in the instructions and work without the hook. Memory hooks are a separate process with no ordering dependency.
