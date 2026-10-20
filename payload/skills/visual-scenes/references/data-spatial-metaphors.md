# Data and spatial metaphors

## Define the encoding before the world

Write a small mapping table: quantity → visual channel → units/domain → transform → missing-value rule. A street, crowd, mountain or factory is useful when it reveals relationships a viewer can read. Keep an ordinary exact card, table or chart available for comparison.

| Question | Useful metaphor | Exact companion |
| --- | --- | --- |
| How do jobs move and where do they wait? | Parcels, queues, workstations and routes | Queue length, throughput, latency and event log |
| How do groups compare? | Equal-width height bars or ordered landmarks | Shared-baseline chart and value table |
| How does a system evolve? | Paths, trails, dated layers or terrain | Timeline, timestamps, change values |
| How is one object related to others? | Network or adjacency landscape | List of neighbors and edge meaning |

Make scale honest. For an intended linear length encoding, use `length ∝ value`; for area use `radius ∝ sqrt(value)`; for volume use `side ∝ cbrt(value)`. If a compressive transform helps a scene fit, disclose it and retain raw values. Perspective and occlusion can still distort perceived comparisons even with a correct mapping.

Particle count should not imply literal people or transactions unless that is what it represents. Use a documented density scale or weight per particle. Flow speed, path width and count are separate channels; avoid unintentionally encoding the same quantity three times.

## Live, snapshot, approximate, absent

Track data source, retrieval time, effective date, coverage and transform. A fallback snapshot is a different status from live data. A fetch may succeed while individual fields remain missing; track provenance at the appropriate field or dataset level. Keep missing distinct from zero, untested distinct from low-scoring, and interpolation distinct from observation. A failed or stale result must not appear as a successful empty response; label freshness.

A composite ranking requires named component metrics, normalization, weights, coverage and tie handling. Averaging available components can favor an incompletely measured entity. Explain the comparison's limits and provide underlying values rather than treating scenery as a universal score.

When animating between observations, show the observation dates. Smooth motion does not prove continuous measurement. Do not let a prominent animated counter momentarily appear to be the final value for the new selection; settle or label the transition.

## Preserve identity while changing layout

Stable identity: see [causal-state-interaction, Guided presets and direct control](causal-state-interaction.md#guided-presets-and-direct-control). Provide a non-spatial route through the same records.

Reduce background salience around the active record. Highlight the measured attribute and its path, not every decorative feature. Crowds and environment are an attention device; their detail should not swamp the data or the interaction budget.

Observed references: [Token Town](https://sael.net/token-town/) pairs shop selection with a model card and source status; [Benchmark Mountain](https://sael.net/benchmark-mountain/) pairs terrain with rankings, domain selection, history and missing results. The research verified selected UI behavior, not the correctness or freshness of upstream rankings. Use these patterns for original data stories with your own defensible mappings.
