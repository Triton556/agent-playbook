# UI/UX: creative directions inside real constraints

In product work the design system, brand, components and regulations are fixed. Creativity lives in how the task is solved: the flow, the structure of information, the interaction, the states and the words. A new color or card style is rarely the idea.

## When to diverge

- **New screen or flow:** divergence trigger: see [creative-direction, Creative direction](../SKILL.md#creative-direction).
- **Redesign:** use the same divergence trigger; preservation criteria: see [task brief and acceptance, section 2](../../dev-flow/references/task-brief-and-acceptance.md#2-understand-the-intent).
- **Refinement:** follow that trigger; this branch adds structural axes only.

## Axes that make directions structurally different

- **Flow shape:** single page vs step-by-step wizard vs inline editing in place vs a summary with drill-down.
- **Entry point:** where the user starts - from a list, from a notification, from a search, from the object itself.
- **Information priority:** what is first and largest - status, next action, amount, comparison, history.
- **Density and disclosure:** everything visible for experts vs progressive disclosure for occasional users.
- **Interaction model:** forms vs direct manipulation vs choosing from smart defaults vs conversational.
- **Error and edge handling:** prevent, recover, or explain - designed into the direction, not added later.

Directions that share the same flow and differ only in layout or style are variations of one direction.

## References

Relevant products or the project's own screens can help clarify an open choice. Use targeted primary sources for an unresolved UX question. Show only enough relevant examples to distinguish the open choices; reuse an accepted direction.

## Sketch

When a sketch helps resolve an open choice, show the main scenario using the existing design system components: the key screens in order, with real content lengths and the main states (empty, loading, error, success). If comparing sketches, use the same scenario and window size.

## Hand-over

The chosen direction continues in ui-design (preflight, states, mockup) and ui-review after implementation. The creative brief names the flow shape, the information priority and what must not change in the existing product.
