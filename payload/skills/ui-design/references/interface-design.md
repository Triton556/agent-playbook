# Interfaces: creation, refinement and redesign

Use the project’s existing components, tokens and accepted examples. Research a specific unresolved design question only when it changes the next decision.

## Establish scope

- **Refinement:** correct affected hierarchy, rhythm, typography or interaction. Preservation: see [task-brief-and-acceptance, 2. Understand the intent](../../dev-flow/references/task-brief-and-acceptance.md#2-understand-the-intent). Scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).
- **Redesign:** reconsider visual system/composition within scope; current behavior is evidence rather than a required visual template. Preservation: see [task-brief-and-acceptance, 2. Understand the intent](../../dev-flow/references/task-brief-and-acceptance.md#2-understand-the-intent). If the user requests alternatives or a concept choice is unresolved, use [creative-direction](../../creative-direction/SKILL.md#creative-direction) for that choice.
- **New surface:** establish audience, main task and relationship to the product. If the user requests alternatives or a concept choice is unresolved, use [creative-direction](../../creative-direction/SKILL.md#creative-direction) for that choice.

For product UI, task completion, scannability and predictability come first. For marketing, attention, understanding the offer and action. For documentation, reading; for a portfolio, the showcased work. Choose the mode by surface: an app's landing page and working screen have different goals.

## Form and implement a direction

Use one visual system: font roles, semantic colors, text scale, spacing, grid and component states. In an existing project, first find these decisions in components/tokens; changing one screen does not create a competing system. Add token decisions when a new visual role cannot be represented by the accepted components/tokens; keep existing roles unchanged outside the agreed redesign.

Ground design character in the subject, audience and content. Choose expressive techniques by the intended reading/action, not a fixed technique count. Source prohibitions of fonts, colors and familiar compositions warn against arbitrary templates; they do not ban an accepted design system. Actual content, figures, testimonials, logos and promises need evidence; label demos as demos.

For accessibility, check keyboard access, visible focus, readable contrast and labels on the affected path. Inspect real messages, long names and relevant empty/loading/error states. After implementation, continue with the actual-flow verification in [ui-design](../SKILL.md).
