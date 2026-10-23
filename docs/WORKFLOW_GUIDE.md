# Workflow and context layers — 2.2

The executable installer selects files; Markdown describes the agent's behavior. Neither file installation nor a static instruction check proves that a model followed a route.

## Start with an observed event

The authoritative short table is [WORKFLOW](../payload/workflow/WORKFLOW.md): event → action → observable output. It is not a requirement to execute every row. User choices, new failures, changed files and named unresolved risks identify the branch; unchanged accepted work is reused.

- User selected the brain role or delegated a task/project: [you-are-brain](../payload/skills/you-are-brain/SKILL.md). Restore saved route/profile/current worker IDs; establish missing setup once. Assign covered work without a new per-worker approval ceremony. Uncovered access, model/cost or scope decisions remain questions. Native tools and external adapters are different execution routes.
- A non-UI contract changes: [implementation reference](../payload/skills/dev-plan/references/implementation.md), with [dev-verify](../payload/skills/dev-verify/SKILL.md) for independent contract checks. A failure enters [dev-debug](../payload/skills/dev-debug/SKILL.md).
- New/redesigned voxel: [voxel-models](../payload/skills/voxel-models/SKILL.md), including required passport and six coherent views, then actual voxel/export checks.
- A knowledge operation: use the named kb-* operation; its data/ownership invariants remain. Jam Board integration is delivered by its application, outside this playbook.

## Layers

1. Actual client/system/tool permissions and current user instructions.
2. Project startup text: short deployment header plus four-rule BASE in full mode.
3. Installed skill metadata for 11 entries.
4. A selected entrypoint, then the reference whose named question/operation is present.
5. Executable helpers when that concrete operation is invoked.

Reference-only modules can deliver files on disk without an extra SKILL.md or automatic context loading. No body-read trace or model-token cost is inferred from inventory. See [2.1 migration](EXPLICIT_ROUTES_2.1.md) and [validation](VALIDATION.md).
