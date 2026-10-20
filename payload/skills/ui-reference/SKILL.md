---
name: ui-reference
description: "Targeted UI/UX reference for web, mobile, and desktop for ui-design and ui-review. Use when an interface task needs searchable accessibility, UX, palette, typography, chart, motion, or stack-specific guidance. Can also be requested directly. Existing product design takes precedence; skip household, research-only, and backend-only work."
---

# Targeted UI/UX reference

Provides guidance for a selected UI question. [Product-ui-design](../ui-design/SKILL.md) owns decisions and [ui-review](../ui-review/SKILL.md) owns actual inspection. A search does not create a separate interview, implementation or acceptance cycle.

First state the question: accessibility, user flow, typography, palette, chart, motion or stack-specific behavior. Loading/recovery: see WORKFLOW, step 2. Search by the selected question. CLI and available domains/stacks: `scripts/search.py --help`.

```text
python <skill>/scripts/search.py "keyboard focus in a dense desktop table" --domain ux --max-results 3
python <skill>/scripts/search.py "accessible dialog" --stack react --max-results 3
```

Use the existing Python; do not install an interpreter for an example. Brief output usually suffices; `--json` or `--full` is for particular data, not the default.

Use `--design-system` for a genuinely new overall visual direction; it proposes input to the primary design stage, not mandatory generation for every new page. Reuse existing components and the accepted system. Do not launch a competing system from Taste or another preset in parallel.

Persist only when the project needs a separate system file: `--persist --output-dir <project-root>`. Read existing MASTER/override before changes; normal execution preserves them without overwriting. `--force` requires authorized replacement. Variance/motion/density parameters are optional hints; accessibility, reduced motion, performance and user goals determine the choice.

Adopt a grounded recommendation with its applicability, not the entire collection. Data and scripts remain specialist sources; they do not establish future interface quality. Preserve installed licenses/provenance.
