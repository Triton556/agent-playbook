# Codex local mode and provenance

Upstream: https://github.com/anthropics/skills/tree/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/skill-creator

Revision: `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`. License: Apache-2.0; see `../LICENSE.txt`. This adaptation is named `anthropic-workflow-creator` and does not replace Codex's built-in `skill-creator`.

Local changes: rewritten SKILL.md for a small, evidence-based workflow cycle; grader guidance moved to a reference; UTF-8 file reading; a limited standard-library frontmatter checker replacing the upstream PyYAML validator; optional deterministic output checks; packager import and path safeguards; Codex interface metadata and installation provenance.

Omitted: upstream `run_eval.py`, `run_loop.py`, `improve_description.py`, benchmark/report automation, comparator/analyzer agents, HTML viewers and their local servers. Originals are retained in the installation workspace backup. Upstream CLI automation assumes Claude and its command layout. Claude CLI and PyYAML were not available during installation; no replacement model SDK, API key or dependency was installed.

This local cycle is not an executed LLM benchmark or model-quality test. It does not evaluate skill triggering, compare models, supply an isolated evaluator or prove semantic correctness. Human/agent review and actual project checks remain necessary. Required-field validation is not complete YAML validation. Codex's fresh native skills/list scan is the installation discovery check.

## Windows PowerShell examples

Use the existing bundled Python interpreter and quote paths. Replace the example project paths with the user's authorized paths.

```powershell
& '{{PYTHON}}' '{{HARNESS_ROOT}}/skills/anthropic-workflow-creator/scripts/quick_validate.py' 'C:/path/to/my-workflow'
& '{{PYTHON}}' '{{HARNESS_ROOT}}/skills/anthropic-workflow-creator/scripts/check_outputs.py' 'C:/path/to/checks.json' 'C:/path/to/outputs'
& '{{PYTHON}}' '{{HARNESS_ROOT}}/skills/anthropic-workflow-creator/scripts/package_skill.py' 'C:/path/to/my-workflow' 'C:/path/to/dist'
```

Output checks accept one JSON object. Paths must be relative to the existing output directory and cannot traverse links/junctions. Each selected file is limited to 8 MiB. The script prints JSON evidence; redirect it only to an authorized destination outside the inputs.

```json
{
  "checks": [
    {"text": "Report exists and is nonempty", "kind": "file_nonempty", "path": "report.md"},
    {"text": "Report identifies the source", "kind": "text_contains", "path": "report.md", "expected": "source:"},
    {"text": "Recorded status is complete", "kind": "json_equals", "path": "result.json", "pointer": "/status", "expected": "complete"}
  ]
}
```

Exit codes: 0 all assertions passed; 1 an assertion failed; 2 malformed or unsafe input. An empty checklist is rejected. JSON pointers follow RFC 6901 (`~0` for `~`, `~1` for `/`). Invalid JSON output fails its assertion. No arbitrary expression, shell command or script check is supported.
