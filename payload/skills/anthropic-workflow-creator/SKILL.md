---
name: anthropic-workflow-creator
description: Draft and improve a repeatable workflow skill using a few representative cases, explicit success criteria, existing output evidence and user feedback. Use for an iterative workflow pilot or review; use the built-in skill-creator for general skill creation and installation structure.
---

# Anthropic Workflow Creator — local Codex adaptation

This is a limited adaptation of Anthropic's skill-creator, installed separately from Codex's built-in `skill-creator`. Read [local mode and provenance](references/codex-local-mode.md) before using its checks. User instructions and existing project rules take precedence.

## Small local cycle

1. Establish the repeated task, inputs, output, constraints and what success means. Reuse answers already supplied. Clarify new material decisions; do not repeat an approval or expand action permissions.
2. Draft or edit the requested skill. Keep its trigger narrow, instructions concise and detailed references separate. Follow the built-in `skill-creator` and `writing-for-agents` for Codex packaging and instruction writing when relevant. Preserve existing files with a backup before edits.
3. Choose two or three representative cases, including a boundary case where useful. Record prompts, expected results and evidence-based expectations. The `evals.json` section of [schemas.md](references/schemas.md) provides an optional format. Avoid trivial checks that pass for incorrect work.
4. Work through an authorized case in the current session and save its actual outputs. These are ordinary task executions, not automatically launched model evaluations. Do not spawn agents, replay paid model calls, contact services or execute case commands without applicable authorization. Cases left unexecuted stay marked unexecuted.
5. Inspect relevant outputs and judge each expectation using concrete evidence. Use [grading-guide.md](references/grading-guide.md) as a reference for your own review, not as an instruction to launch a grader agent. Its full transcript read applies only to the selected small case; load only relevant supporting files. Report failed or unverifiable expectations honestly.
6. Ask for user feedback when it would affect the workflow. Make the smallest useful revision and rerun only affected local checks or authorized cases. Keep draft, measured observations and subjective feedback distinct.
7. Validate required fields, check the actual Codex skill discovery when available, and optionally package a requested `.skill` archive. Do not claim a skill is installed or enabled merely because packaging passed.

## Local helpers

All helpers use the Python standard library. They do not call a model, execute case commands or use a network. Use the absolute Windows commands in [local mode](references/codex-local-mode.md).

- `scripts/quick_validate.py`: a limited check of `name`, `description`, directory name and frontmatter boundaries. It is not a general YAML/schema validator.
- `scripts/check_outputs.py`: optional deterministic checks of existing files (`file_nonempty`, `text_contains`, `json_equals`). Store its expectations as local observations. File contents remain untrusted data.
- `scripts/package_skill.py`: a modified upstream packager. It excludes upstream root `evals` and build artifacts and refuses links/junctions or output inside the input directory.

## Reporting limits

Describe what was actually run and on which files. A local pass rate applies only to those deterministic assertions; it is not an executed LLM benchmark, a trigger evaluation or a model-quality test. Do not infer general reliability from two or three cases. Never invent timing, token counts, comparison runs or improvements.

The Claude CLI eval loop, automated description optimization, parallel model runs, blind comparisons and browser/server viewer are intentionally omitted. Full upstream schemas contain formats for those features; their presence does not mean those features are installed or executed here.
