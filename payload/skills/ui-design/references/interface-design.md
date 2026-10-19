# Interfaces: creation, refinement and redesign

For a specific question about expression, typography or composition, use [Anthropic frontend-design](../vendor/anthropic-frontend-design/INSTRUCTIONS.md). The [Hitbullets Codex adaptation](../vendor/codex-frontend-design/INSTRUCTIONS.md) is an additional reference when a more concrete token/layout plan is needed; do not load both on every request.

## Establish scope

- **Refinement:** preserve identity, components, content and behavior. Correct affected hierarchy, rhythm, typography or interaction. “More beautiful” alone does not authorize changing the product's purpose.
- **Redesign:** reconsider the visual system/composition within scope while preserving product facts, scenarios and constraints. An existing screen is evidence of current behavior, not a mandatory visual template. After listing what already works and must survive, explore directions with [creative-direction](../../creative-direction/SKILL.md).
- **New surface:** establish audience, main task and relationship to the existing product. Produce distinct directions with [creative-direction](../../creative-direction/SKILL.md) before choosing; decide routine details yourself and ask only about material unknowns.

For product UI, task completion, scannability and predictability come first. For marketing, attention, understanding the offer and action. For documentation, reading; for a portfolio, the showcased work. Choose the mode by surface: an app's landing page and working screen have different goals.

## Form and implement a direction

Use one visual system: font roles, semantic colors, text scale, spacing, grid and component states. In an existing project, first find these decisions in components/tokens; changing one screen does not create a competing system. Produce a new token plan only when actually needed.

Ground design character in the subject, audience and content. Select one expressive technique; the rest supports it. Source prohibitions of fonts, colors and familiar compositions warn against arbitrary templates; they do not ban an accepted design system. Actual content, figures, testimonials, logos and promises need evidence; label demos as demos.

For an unknown UX/stack question, use existing `{{HARNESS_ROOT}}/skills/ui-reference/SKILL.md` and one relevant search/reference. Search output is guidance, not a new design system. Taste v1 remains an additional source only when specifically useful; do not load it on every UI request.

Preserve accessible focus/keyboard states, reduced motion, readability and responsiveness. Check real messages, long names and empty/loading/error states relevant to the scenario. After UI implementation, move to [ui-review](../../ui-review/SKILL.md).
