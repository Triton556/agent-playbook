# Core cleanup 2.0

This is an intentional owner-authorized behavior change from 1.6.0, not a packaging-only fidelity update. The former requirement to retain every external body is superseded for the components listed here. Recovery is available from Git commit `586c922484810c76bfa53383df434aaf4dc914eb`; do not restore old files over user edits.

## Official baseline and local decisions

Read [OpenAI GPT-6 guidance](https://developers.openai.com/api/docs/guides/latest-model#instruction-following), checked 2026-10-22. Its recommendations motivate explicit instruction priority, identifying a blocking rule, purposeful delegation, proportional verification and no repeated/broader checks after success without a new reason. They are guidance to evaluate, not proof that this package improves every model.

Our policy: verify the changed behavior and relevant risks using independent expected results; do not write tests that mirror implementation. Preserve relevant functional/render/interaction checks, financial invariants and project-required checks. Once these pass, finish unless a new change, failure or named uncertainty calls for more. Separate reviewers are optional and require the task's selection; self-review is not independent acceptance. Existing brief/profile/checkpoints are reused rather than re-interviewed. Short tasks need no orchestration ritual.

[OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills) distinguishes initial metadata from full skill bodies, which are read on selection. The catalog can be shortened by client budgets. Our installer now distinguishes required module dependencies from optional prose routes; installing a file does not prove a model read it.

## Inventory

Retained 20: agent-instructions; agent-sessions; agent-sessions-codex; you-are-brain; jam-board; kb-find; kb-save; kb-status; kb-sync; kb-curate; dev-flow; dev-plan; dev-implement; dev-debug; dev-verify; ui-design; ui-review; creative-direction; visual-scenes; voxel-models.

Removed six imported entrypoints: ui-reference (UI/UX Pro Max), ui-taste-reference (Taste), stress-test, stress-test-with-docs, dev-domain-model and agent-handoff (imported interview/domain/handoff methods). Removed all bundled vendor trees from dev/UI, Impeccable scripts and its runtime declaration. These are no longer installed or invoked. Historical source attribution and applicable licenses remain for retained adaptations.

Practical handoffs, context recovery, precise terminology, worker briefs/reports, selected model/effort/access, brain/session adapters, Jam Board, knowledge integrity, creative and visual/voxel criteria remain. A glossary or handoff can still be requested without an imported mandatory workflow. Added a short local accessibility reference rather than retaining an entire searchable design toolkit.

## Dependencies and routing

`manifest.json.skill_dependencies` is the only required skill installation graph. Optional links and mentions never create edges. `--profile full` explicitly selects all 20; `--workflow` does the same. A selected stage includes its required shared procedure owner, not every optional stage linked by that owner. Inspect `plan` before installation.

Before following an optional skill route, check the installed catalog. If missing and genuinely needed, report that capability; do not pretend it was installed or silently install it. A skill body/reference is read only for the active decision, not because a package dependency exists. System/client rules and current user permissions remain higher priority than skill guidance; source references do not grant tools, access or reviewers.

## Safe upgrade and removal

Use the original trusted installer checkout/receipt store. Inspect `plan` with the same target/client/profile and bindings first. A normal upgrade validates the old private receipt, every recorded file and the owned startup block before writing. It removes only obsolete files marked owned and still matching the old receipt. Edited/missing files, changed bindings or missing trusted records stop the migration; preserve both versions and resolve the scope deliberately. Preexisting identical unowned files and unrelated installed skills remain untouched.

An explicitly requested retired skill returns a clear error before writes; choose a current core stage rather than silently replacing it. Removing a shared dependency is not permission to delete another skill installed outside this receipt. Existing global/Mac configurations are not modified by this release. No force/reset cleanup.

## Validation and measurement boundaries

Use installer roundtrip, actual old-release upgrade, edited-file refusal, unowned-neighbor preservation, dependency-closure and helper behavioral tests. Static link/integrity checks supplement these; they do not establish model compliance or UI quality. No paid model pilot is required or run.

Report UTF-8 bytes separately for base instructions, reconstructed metadata and skill/reference bodies. Use identical paths/format for before/after. These are not token counts or billing savings. Actual Mac startup, hidden/tool context, cache and model quality remain unmeasured without a controlled authorized run.
