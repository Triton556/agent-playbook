# Interfaces: creation, refinement and redesign

For a specific question about expression, typography or composition, use [Anthropic frontend-design](../vendor/anthropic-frontend-design/INSTRUCTIONS.md). The [Hitbullets Codex adaptation](../vendor/codex-frontend-design/INSTRUCTIONS.md) is an additional reference when a more concrete token/layout plan is needed; do not load both on every request.

## Establish scope

- **Refinement:** correct affected hierarchy, rhythm, typography or interaction. Preservation: see [task-brief-and-acceptance, 2. Understand the intent](../../dev-flow/references/task-brief-and-acceptance.md#2-understand-the-intent). Scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).
- **Redesign:** reconsider visual system/composition within scope; current behavior is evidence rather than a required visual template. Preservation: see [task-brief-and-acceptance, 2. Understand the intent](../../dev-flow/references/task-brief-and-acceptance.md#2-understand-the-intent). Direction exploration: see [creative-direction, Creative direction](../../creative-direction/SKILL.md#creative-direction).
- **New surface:** establish audience, main task and relationship to the product. Direction exploration: see [creative-direction, Creative direction](../../creative-direction/SKILL.md#creative-direction).

For product UI, task completion, scannability and predictability come first. For marketing, attention, understanding the offer and action. For documentation, reading; for a portfolio, the showcased work. Choose the mode by surface: an app's landing page and working screen have different goals.

## Form and implement a direction

Use one visual system: font roles, semantic colors, text scale, spacing, grid and component states. In an existing project, first find these decisions in components/tokens; changing one screen does not create a competing system. Produce a new token plan only when actually needed.

Ground design character in the subject, audience and content. Select one expressive technique; the rest supports it. Source prohibitions of fonts, colors and familiar compositions warn against arbitrary templates; they do not ban an accepted design system. Actual content, figures, testimonials, logos and promises need evidence; label demos as demos.

For an unknown UX/stack question, use existing `{{HARNESS_ROOT}}/skills/ui-reference/SKILL.md` and one relevant search/reference. Search output is guidance, not a new design system. Taste v1 remains an additional source only when specifically useful; do not load it on every UI request.

Accessibility: see [ui-reference, Quick Reference](../../ui-reference/references/quick-reference.md#quick-reference). Check real messages, long names and empty/loading/error states relevant to the scenario. After UI implementation, move to [ui-review](../../ui-review/SKILL.md).
