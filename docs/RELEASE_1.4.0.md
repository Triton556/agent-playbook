# Release 1.4.0 verification

Prepared on main from df75cb8 (1.3.0). All 61 supplied findings were checked, including D36, which is present in the audit despite the task’s shorthand D1–D35 range. No finding was left unresolved. This is author verification; no separate reviewer, live worker or model-quality experiment was run.

## Baseline

The requested Python runtime ran both commands before source edits:

| Command | Expected | Actual | Result |
| --- | --- | --- | --- |
| python harness.py check-package | Package passes | 307 payload files; exit 0 | PASS |
| python -B -m unittest discover -s tests | All tests pass | 41 tests, 399.136 seconds; two Jam Board system-TEMP PermissionErrors; exit 1 | FAIL |

The two tests now use the existing bounded repository test-directory helper with inherited permissions. Access controls were not changed and denied system-TEMP access was not bypassed.

## Changed files by area

### Release, installer and public guides

- [CHANGELOG.md](../CHANGELOG.md)
- [INSTALL_FOR_AGENTS.md](../INSTALL_FOR_AGENTS.md)
- [README.md](../README.md)
- [README.ru.md](../README.ru.md)
- [docs/COMPATIBILITY.md](../docs/COMPATIBILITY.md)
- [docs/FIDELITY.md](../docs/FIDELITY.md)
- [docs/INSTRUCTION_MAINTENANCE.md](../docs/INSTRUCTION_MAINTENANCE.md)
- [docs/INTEGRATIONS.md](../docs/INTEGRATIONS.md)
- [docs/PROFILES.ru.md](../docs/PROFILES.ru.md)
- [docs/RELEASE_1.4.0.md](../docs/RELEASE_1.4.0.md)
- [docs/VALIDATION.md](../docs/VALIDATION.md)
- [docs/WORKFLOW_GUIDE.md](../docs/WORKFLOW_GUIDE.md)
- [harness.py](../harness.py)
- [manifest.json](../manifest.json)

### Shared workflow and instruction owners

- [payload/AGENTS.md](../payload/AGENTS.md)
- [payload/skills/agent-handoff/SKILL.md](../payload/skills/agent-handoff/SKILL.md)
- [payload/skills/agent-instructions/SKILL.md](../payload/skills/agent-instructions/SKILL.md)
- [payload/skills/dev-debug/SKILL.md](../payload/skills/dev-debug/SKILL.md)
- [payload/skills/dev-domain-model/GLOSSARY-FORMAT.md](../payload/skills/dev-domain-model/GLOSSARY-FORMAT.md)
- [payload/skills/dev-domain-model/SKILL.md](../payload/skills/dev-domain-model/SKILL.md)
- [payload/skills/dev-flow/SKILL.md](../payload/skills/dev-flow/SKILL.md)
- [payload/skills/dev-flow/references/human-perspective-review.md](../payload/skills/dev-flow/references/human-perspective-review.md)
- [payload/skills/dev-flow/references/quality-cycle.md](../payload/skills/dev-flow/references/quality-cycle.md)
- [payload/skills/dev-flow/references/quality-ledger.md](../payload/skills/dev-flow/references/quality-ledger.md)
- [payload/skills/dev-flow/references/reference-grounding.md](../payload/skills/dev-flow/references/reference-grounding.md)
- [payload/skills/dev-flow/references/task-brief-and-acceptance.md](../payload/skills/dev-flow/references/task-brief-and-acceptance.md)
- [payload/skills/dev-flow/references/task-state.md](../payload/skills/dev-flow/references/task-state.md)
- [payload/skills/dev-implement/SKILL.md](../payload/skills/dev-implement/SKILL.md)
- [payload/skills/dev-plan/SKILL.md](../payload/skills/dev-plan/SKILL.md)
- [payload/skills/dev-verify/SKILL.md](../payload/skills/dev-verify/SKILL.md)
- [payload/skills/jam-board/SKILL.md](https://github.com/Triton556/agent-playbook/blob/60317a3b83ef5bd9ef620a899bf95a099f7c926f/payload/skills/jam-board/SKILL.md)
- [payload/skills/jam-board/references/brain-loop.md](https://github.com/Triton556/agent-playbook/blob/60317a3b83ef5bd9ef620a899bf95a099f7c926f/payload/skills/jam-board/references/brain-loop.md)
- [payload/skills/jam-board/references/field-guide.md](https://github.com/Triton556/agent-playbook/blob/60317a3b83ef5bd9ef620a899bf95a099f7c926f/payload/skills/jam-board/references/field-guide.md)
- [payload/skills/jam-board/references/worker-loop.md](https://github.com/Triton556/agent-playbook/blob/60317a3b83ef5bd9ef620a899bf95a099f7c926f/payload/skills/jam-board/references/worker-loop.md)
- [payload/skills/stress-test-with-docs/SKILL.md](../payload/skills/stress-test-with-docs/SKILL.md)
- [payload/skills/stress-test/SKILL.md](../payload/skills/stress-test/SKILL.md)
- [payload/workflow/WORKFLOW.md](../payload/workflow/WORKFLOW.md)
- [payload/workflow/agent-worklog.mjs](../payload/workflow/agent-worklog.mjs)
- [payload/workflow/independent-review.md](../payload/workflow/independent-review.md)

### Memory

- [payload/runtime/memory/SYSTEM/workflows/capture.md](../payload/runtime/memory/SYSTEM/workflows/capture.md)
- [payload/runtime/memory/SYSTEM/workflows/curate.md](../payload/runtime/memory/SYSTEM/workflows/curate.md)
- [payload/skills/kb-curate/SKILL.md](../payload/skills/kb-curate/SKILL.md)
- [payload/skills/kb-find/SKILL.md](../payload/skills/kb-find/SKILL.md)
- [payload/skills/kb-save/SKILL.md](../payload/skills/kb-save/SKILL.md)
- [payload/skills/kb-status/SKILL.md](../payload/skills/kb-status/SKILL.md)
- [payload/skills/kb-sync/SKILL.md](../payload/skills/kb-sync/SKILL.md)

### Orchestration and brain setup

- [payload/skills/agent-sessions-codex/SKILL.md](../payload/skills/agent-sessions-codex/SKILL.md)
- [payload/skills/agent-sessions-codex/references/brief-writing.md](../payload/skills/agent-sessions-codex/references/brief-writing.md)
- [payload/skills/agent-sessions-codex/references/requirements-interview.md](../payload/skills/agent-sessions-codex/references/requirements-interview.md)
- [payload/skills/agent-sessions-codex/references/running-and-checking.md](../payload/skills/agent-sessions-codex/references/running-and-checking.md)
- [payload/skills/agent-sessions/SKILL.md](../payload/skills/agent-sessions/SKILL.md)
- [payload/skills/agent-sessions/references/brief-writing.md](../payload/skills/agent-sessions/references/brief-writing.md)
- [payload/skills/agent-sessions/references/contract.md](../payload/skills/agent-sessions/references/contract.md)
- [payload/skills/agent-sessions/references/requirements-interview.md](../payload/skills/agent-sessions/references/requirements-interview.md)
- [payload/skills/agent-sessions/references/running-and-checking.md](../payload/skills/agent-sessions/references/running-and-checking.md)
- [payload/skills/agent-sessions/references/writing-an-adapter.md](../payload/skills/agent-sessions/references/writing-an-adapter.md)
- [payload/skills/you-are-brain/SKILL.md](../payload/skills/you-are-brain/SKILL.md)
- [payload/skills/you-are-brain/references/brain-profile.md](../payload/skills/you-are-brain/references/brain-profile.md)
- [payload/skills/you-are-brain/references/setup-interview.md](../payload/skills/you-are-brain/references/setup-interview.md)

### UI and creative references

- [payload/skills/creative-direction/SKILL.md](../payload/skills/creative-direction/SKILL.md)
- [payload/skills/creative-direction/references/content.md](../payload/skills/creative-direction/references/content.md)
- [payload/skills/creative-direction/references/ui-ux.md](../payload/skills/creative-direction/references/ui-ux.md)
- [payload/skills/ui-design/SKILL.md](../payload/skills/ui-design/SKILL.md)
- [payload/skills/ui-design/references/design-preflight.md](../payload/skills/ui-design/references/design-preflight.md)
- [payload/skills/ui-design/references/interaction-quality.md](../payload/skills/ui-design/references/interaction-quality.md)
- [payload/skills/ui-design/references/interface-design.md](../payload/skills/ui-design/references/interface-design.md)
- [payload/skills/ui-design/references/landing-design.md](../payload/skills/ui-design/references/landing-design.md)
- [payload/skills/ui-reference/SKILL.md](../payload/skills/ui-reference/SKILL.md)
- [payload/skills/ui-reference/references/pro-rules.md](../payload/skills/ui-reference/references/pro-rules.md)
- [payload/skills/ui-reference/references/quick-reference.md](../payload/skills/ui-reference/references/quick-reference.md)
- [payload/skills/ui-review/SKILL.md](../payload/skills/ui-review/SKILL.md)
- [payload/skills/ui-review/references/critique-adapted.md](../payload/skills/ui-review/references/critique-adapted.md)
- [payload/skills/ui-review/references/visual-quality.md](../payload/skills/ui-review/references/visual-quality.md)
- [payload/skills/ui-taste-reference/SKILL.md](../payload/skills/ui-taste-reference/SKILL.md)
- [payload/skills/ui-taste-reference/references/taste-v1-recipes.md](../payload/skills/ui-taste-reference/references/taste-v1-recipes.md)

### Voxel and visual references

- [payload/skills/visual-scenes/SKILL.md](../payload/skills/visual-scenes/SKILL.md)
- [payload/skills/visual-scenes/references/causal-state-interaction.md](../payload/skills/visual-scenes/references/causal-state-interaction.md)
- [payload/skills/visual-scenes/references/composition-materials.md](../payload/skills/visual-scenes/references/composition-materials.md)
- [payload/skills/visual-scenes/references/data-spatial-metaphors.md](../payload/skills/visual-scenes/references/data-spatial-metaphors.md)
- [payload/skills/visual-scenes/references/procedural-graphics.md](../payload/skills/visual-scenes/references/procedural-graphics.md)
- [payload/skills/visual-scenes/references/runtime-accessibility.md](../payload/skills/visual-scenes/references/runtime-accessibility.md)
- [payload/skills/visual-scenes/references/validation.md](../payload/skills/visual-scenes/references/validation.md)
- [payload/skills/voxel-models/SKILL.md](../payload/skills/voxel-models/SKILL.md)
- [payload/skills/voxel-models/references/anatomy-support.md](../payload/skills/voxel-models/references/anatomy-support.md)
- [payload/skills/voxel-models/references/built-form.md](../payload/skills/voxel-models/references/built-form.md)
- [payload/skills/voxel-models/references/design-passport.md](../payload/skills/voxel-models/references/design-passport.md)
- [payload/skills/voxel-models/references/design-preflight.md](../payload/skills/voxel-models/references/design-preflight.md)
- [payload/skills/voxel-models/references/environments.md](../payload/skills/voxel-models/references/environments.md)
- [payload/skills/voxel-models/references/files-meshes.md](../payload/skills/voxel-models/references/files-meshes.md)
- [payload/skills/voxel-models/references/gen2.md](../payload/skills/voxel-models/references/gen2.md)
- [payload/skills/voxel-models/references/mixed-grids.md](../payload/skills/voxel-models/references/mixed-grids.md)
- [payload/skills/voxel-models/references/objects.md](../payload/skills/voxel-models/references/objects.md)
- [payload/skills/voxel-models/references/organic-form.md](../payload/skills/voxel-models/references/organic-form.md)
- [payload/skills/voxel-models/references/probe-library.md](../payload/skills/voxel-models/references/probe-library.md)
- [payload/skills/voxel-models/references/procedural.md](../payload/skills/voxel-models/references/procedural.md)
- [payload/skills/voxel-models/references/quality-cycle.md](../payload/skills/voxel-models/references/quality-cycle.md)
- [payload/skills/voxel-models/references/resolution-lod.md](../payload/skills/voxel-models/references/resolution-lod.md)
- [payload/skills/voxel-models/references/shape-palette.md](../payload/skills/voxel-models/references/shape-palette.md)

### Tests

- [tests/test_install.py](../tests/test_install.py)
- [tests/test_instruction_ownership.py](../tests/test_instruction_ownership.py)
- [tests/test_jam_board.py](../tests/test_jam_board.py)
- [tests/test_migration.py](../tests/test_migration.py)

## Finding recheck

Each location below was read back in the final working tree. Pointers use the named owner and section. The three mandated physical mirrors are one logical policy owner and are checked byte-for-byte.

| ID | Fixed at | Resolution |
| --- | --- | --- |
| C1 | `payload/workflow/independent-review.md:18`; `payload/skills/agent-sessions/SKILL.md:12` | Review launches defer to session execution policy. |
| C2 | `payload/workflow/independent-review.md:27` | Fresh-round and non-continuation rule; runner has the reviewer exception. |
| C3 | `payload/skills/dev-flow/references/task-brief-and-acceptance.md:32` | Explicit acceptance only; briefly re-ask unanswered material questions. |
| C4 | `payload/skills/agent-sessions/SKILL.md:19` | Project-specific explicit publication exception; board callers point here. |
| C5 | `payload/skills/agent-sessions/SKILL.md:70` | One launch gate; interview and board playback no longer request another confirmation. |
| C6 | `payload/skills/agent-sessions/SKILL.md:38` | Explicit level, difficulty-only escalation, otherwise table/maximum cases. |
| C7 | `payload/skills/agent-sessions/references/running-and-checking.md:61` | Continuation refers to step 3 and preserves other approved settings. |
| C8 | `payload/AGENTS.md:5`; `payload/skills/agent-sessions/references/brief-writing.md:7` | Default and worker-channel exception have separate owners. |
| C9 | `payload/skills/creative-direction/references/ui-ux.md:7` | Creative-direction owns accepted/open direction triggers; UI callers point there. |
| C10 | `payload/skills/ui-design/references/design-preflight.md:31` | Reference checklists are scoped to the recorded device/theme/state coverage. |
| C11 | `payload/skills/ui-reference/references/quick-reference.md:70` | Fixed loading thresholds replaced with operation-specific feedback owner. |
| C12 | `payload/skills/ui-taste-reference/references/taste-v1-recipes.md:215` | Removed the additional mandatory Taste delivery pass. |
| S1 | `payload/AGENTS.md:18`; `payload/workflow/WORKFLOW.md:12` | Both general entrypoints route delegation to agent-sessions. |
| S2 | `payload/AGENTS.md:10` | Current-task Git authorization centralized; client restrictions retained as facts. |
| S3 | `payload/skills/kb-save/SKILL.md:16` | Writer assignment, checkpoint-only workers and memory-helper handoff owned here. |
| S4 | `payload/skills/agent-sessions/references/running-and-checking.md:70` | Native prompts distinguished from async board questions; blocked-return condition stated. |
| S5 | `payload/skills/agent-sessions/references/contract.md:48`; `payload/skills/agent-sessions/SKILL.md:45` | API optionality defers to deliberate settings; minimal is mapped in step 3. |
| S6 | `payload/skills/agent-sessions/references/running-and-checking.md:20` | Session metadata placement reconciles plan and board ownership. |
| S7 | `payload/skills/agent-sessions/references/brief-writing.md:20` | Independent-review staging overrides generic diagnosis/baseline fields. |
| R1 | `payload/workflow/independent-review.md:3` | Correct numbered reviewer-selection anchor. |
| R2 | `payload/skills/ui-design/references/interaction-quality.md:47` | Missing document replaced by actual preflight sections 1–2 governing applicability. |
| R3 | `payload/workflow/WORKFLOW.md:16` | Uses current engineering stage owner instead of retired stage names. |
| R4 | `payload/skills/ui-reference/references/quick-reference.md:3` | Both UI indexes point to current search entry, not an absent priority table. |
| R5 | `payload/skills/agent-sessions/references/running-and-checking.md:3` | Direct contract Run link replaces circular run-command pointer. |
| R6 | `docs/WORKFLOW_GUIDE.md:59` | Removed unavailable Anthropic compatibility route. |
| D1 | `payload/skills/agent-sessions/SKILL.md:14` | Model selection and standing brain-profile choices centralized. |
| D2 | `payload/skills/agent-sessions/SKILL.md:47` | Only generic step 3 maintains the effort table; Codex retains aliases. |
| D3 | `payload/skills/agent-sessions/references/brief-writing.md:7` | Worker language owned here; exactly mirrored by the required Codex reference. |
| D4 | `payload/skills/agent-sessions/SKILL.md:70` | Approval procedure removed from other entrypoints and public guides. |
| D5 | `payload/skills/agent-sessions/references/running-and-checking.md:7` | Scheduling/isolation/dependencies and normal continuation owned by runner. |
| D6 | `payload/skills/agent-sessions/references/contract.md:30` | Access semantics/refusal centralized; adapter/client mappings retained. |
| D7 | `payload/skills/agent-sessions/references/running-and-checking.md:51` | Worker-result checking centralized; board maps verdicts to its API. |
| D8 | `payload/skills/agent-sessions/references/running-and-checking.md:72` | Per-session report fields have one owner. |
| D9 | `payload/skills/agent-sessions-codex/SKILL.md:10` | Codex home/history/settings/hooks/driver operation kept in client skill. |
| D10 | `payload/skills/dev-flow/references/task-brief-and-acceptance.md:26` | Ordinary interview owner retained; sessions add delegation fields; stress-test marks its variant. |
| D11 | `payload/skills/dev-flow/references/task-brief-and-acceptance.md:42` | Participation/reviewer selection centralized; board stores fields. |
| D12 | `payload/AGENTS.md:7` | Authority and review-only scope centralized; specialists point here. |
| D13 | `payload/skills/dev-flow/references/task-state.md:5` | Record relationships centralized; schemas retain their exact machine fields. |
| D14 | `payload/skills/dev-flow/references/task-brief-and-acceptance.md:16` | Preservation criteria owned by intent card; perception keeps verification method. |
| D15 | `payload/workflow/WORKFLOW.md:10` | Shared repair/recheck/new-signal loop retained; domain checks supplement it. |
| D16 | `payload/skills/dev-flow/references/quality-ledger.md:22` | Freshness/history centralized; exact schema invalidation contracts remain explicit supplements. |
| D17 | `payload/skills/dev-flow/references/human-perspective-review.md:92` | Claim grades centralized, including helper result text pointing to owner. |
| D18 | `payload/skills/dev-flow/references/human-perspective-review.md:58` | Observation order centralized; review preparation adds only staging exception. |
| D19 | `payload/skills/voxel-models/references/design-preflight.md:13` | Voxel/route callers reference reference-grounding trigger list. |
| D20 | `payload/skills/dev-flow/references/task-brief-and-acceptance.md:63` | Single reuse rule; caller summaries replaced with pointers. |
| D21 | `payload/skills/dev-flow/references/workflow-pilot.md:3` | Pilot owns authorization/method/limits; prose and public guides retain trigger links. |
| D22 | `payload/skills/kb-save/SKILL.md:12` | Capture/checkpoint procedure centralized; installation/integration guides link it. |
| D23 | `payload/skills/kb-sync/SKILL.md:14`; `payload/skills/kb-curate/SKILL.md:10` | Transport safeguards and semantic curation have separate owners. |
| D24 | `payload/skills/agent-handoff/SKILL.md:10` | One cross-platform destination with Windows binding. |
| D25 | `payload/skills/agent-instructions/SKILL.md:13` | Placement/creator routing owned here; general routes and docs point here. |
| D26 | `README.md:125` | README upgrade/discovery copies reduced to installation/activation owner links. |
| D27 | `payload/skills/ui-review/SKILL.md:10` | Actual UI comparison invokes UI preflight section 4. |
| D28 | `payload/skills/ui-reference/references/quick-reference.md:12` | Reusable rule IDs own accessibility bodies; contextual/native callers use those IDs. |
| D29 | `payload/skills/visual-scenes/references/causal-state-interaction.md:13`; `payload/skills/visual-scenes/references/data-spatial-metaphors.md:20` | Revision/identity owner retained; missing encoding owned by data-spatial-metaphors. |
| D30 | `payload/skills/voxel-models/SKILL.md:35` | Entry/catalog/check adapters point to voxel preflight and its reuse contract. |
| D31 | `payload/skills/voxel-models/references/resolution-lod.md:5`; `payload/skills/voxel-models/references/objects.md:11`; `payload/skills/voxel-models/references/built-form.md:5` | Scale, articulation and cavities keep specialist owners; other branches point to them. |
| D32 | `payload/skills/visual-scenes/references/runtime-accessibility.md:5` | Actual runtime measurement owner retained; voxel representation caveats point here. |
| D33 | `payload/skills/dev-flow/references/reference-grounding.md:20` | Shared reuse rights owner retained; voxel NoAI/view-only rule marked as addition. |
| D34 | `payload/workflow/WORKFLOW.md:6` | Loading/recovery owner retained; specialists keep branch triggers and pointers. |
| D35 | `payload/skills/dev-flow/references/human-perspective-review.md:61` | Observation/cause/no-quota method centralized; domain measurement checks retained. |
| D36 | `payload/skills/dev-flow/references/human-perspective-review.md:90` | Independent expected-result construction points to dev-verify. |

## Required checks

All Python commands used the task-provided executable. U = `python -B -m unittest discover -s tests -v`. O = `python -B -m unittest discover -s tests -p test_instruction_ownership.py -v`. Local logs and scratch validators are under `artifacts/fix-1.4/scratch/`.

| # | Command / covered test | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| 1 | `python harness.py check-package` | Valid package | 310 payload files; exit 0 | PASS |
| 2 | U | Entire suite passes | 47 tests in 574.119s; no failures/skips | PASS |
| 3 | O: `test_each_map_rule_has_one_policy_owner` | Every map rule has its owning phrase once | 16 rules each have one logical owner; only approved physical mirrors exempted | PASS |
| 4 | O: `test_all_three_shared_references_are_identical`; U: existing mirror test | Three reference pairs byte-identical | All 3 pairs match; status and blocked-return sections included | PASS |
| 5 | O: `test_you_are_brain_standalone_install_both_clients` | New skill requests alone, agent-sessions dependency, verify passes | Codex and Claude install/verify pass; existing instructions preserved; installed links resolve | PASS |
| 6 | `python -B artifacts/fix-1.4/scratch/check_report.py` | Every supplied ID has a current disposition | 61 fixed, 0 left; locations read back; 16 supplied source hashes checked; protected bodies unchanged | PASS |
| 7 | O: `test_every_relative_payload_markdown_destination_exists` | No missing relative Markdown target | 569 relative links; 0 missing; local instruction fragments also pass | PASS |

The full suite passed before the final instruction-only clarifications (failed input, waiting actions, failed/stale data and the worker-client approval column). No installer or test code changed afterward. Package integrity and all five affected ownership/mirror/link/Codex+Claude installation tests were rerun after those restorations and passed in 20.471 seconds. The full suite was not repeated after those wording-only changes.

Supplemental author checks: `node --check payload/workflow/agent-worklog.mjs` passed; `git -c core.whitespace=cr-at-eol diff --check` passed. The one-shot Git option accounts for preserved CRLF without changing configuration. Failed intermediate receipts remain in ignored scratch logs.


## Deviations and limits

- The requested scratch directory is outside the repository-only write boundary. Scratch/logs use ignored artifacts/fix-1.4/scratch; isolated installer fixtures use the existing tests/.tmp helper.
- Required single-owner links enlarge dependency closures. Profiles explicitly select brain setup wherever agent-sessions is selected. Upgrade validation now recomputes current dependency closure only after matching the original explicit selection and permitted release-profile additions; binding, receipt, old-file/conflict and user-content safeguards remain checked. Added real 1.3.0 full/selected upgrade coverage.
- AGENTS is deployed as BASE-RULES.md and also inlined at project root. Policy links use the existing HARNESS_ROOT binding; installed-link tests cover this relocation. The generated startup language text points to that owner.
- Three glossary example destinations were nonexistent template paths. They now appear as literal code paths, preserving the examples without false Markdown links.
- The optional native skill-creator quick_validate.py could not run: PyYAML is unavailable. No dependency was installed. Catalog/frontmatter, source/export and actual installer checks provide structural evidence instead.
- No push, publication, network call, new dependency or global client/configuration change. No commit/tag was attempted because .git is read-only in this sandbox. Changes remain in the working tree.
- Vendor/data/license bodies and source directories outside this repository were not modified. Historical release descriptions retain their historical counts and policies. Search datasets remain source guidance; maintained rule owners govern active policy.
- Unverified: live client discovery/startup interpretation, app visibility, worker execution, live Jam Board MCP behavior, model quality, independent review and human acceptance. The two baseline system-TEMP directories were inaccessible to cleanup; their later state is unverified.

PASS 7/7, FIXED 61/61
