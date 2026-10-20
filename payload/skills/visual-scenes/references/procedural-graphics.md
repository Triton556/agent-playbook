# Procedural graphics

## Geometry at several scales

Build a recognizable primary structure before surface noise. Separate large shape, medium structural repetition and small appearance variation. Use seeded randomness so A/B images and test cases remain comparable. Scale variation should follow a reason: tree age, terrain slope, manufacturing repeat or a measured distribution.

Repeated geometry can share buffers or instances; static parts can be merged by material. Choose based on independent movement and picking needs, not a universal instancing rule. Maintain IDs outside the draw batches. Update only changed ranges and reuse scratch vectors, attributes and buffers in a hot loop.

## Flow and trails

Represent a route by positions and cumulative arc length. Sampling by distance gives approximately consistent particle speed even when control points are uneven. Keep simulated time and display time separate; provide pause and reset.

For a ribbon, sample tangents and construct stable transverse directions; guard near-zero segments and frame flips. Keep width tied to a defined quantity or explicit display scale. Clip or split discontinuities instead of connecting them across space. In cyclic flow, avoid a long spurious tail connecting end to start.

Exposure trails should follow past route positions, not a straight stretch along today's velocity when the path curves. Bound history length and samples. Label them as exposure/illustration when they are not integrated measurements. A trail can reveal time but also hide overlap; provide an instantaneous view.

## Fields and cross-sections

An animated particle field can show direction while a cross-section reveals what the surface hides. Use color and arrow direction consistently, provide units and scale, and make the slice location visible in the overview. Fields with strong range differences may need a stated logarithmic or normalized display mapping.

Terrain, isosurfaces and heightmaps benefit from a scale legend. If vertical scale is exaggerated, show the multiplier. Material bands, age bands or contour lines should encode a meaningful quantity; decorative noise should not resemble measurement.

## Deformation and changing topology

Model revision: see [causal-state-interaction, One model, several views](causal-state-interaction.md#one-model-several-views). In addition, keep smoothed display geometry distinct and state solver convergence/residual criteria; iteration count is not physical time or convergence proof.

Bound solver work per frame under causal-state-interaction, One model, several views. In addition, topology changes may conceal/rebuild/reveal for continuity but must not fabricate intermediate physical states; absent phenomena clear their dependent readings.

## Use in other domains

The same techniques serve packet routes, factory lines, population flows, geographic change and dependency propagation. Replace decorative particles with entities or clearly weighted samples. Preserve the domain's invariant—conservation, ordering, reachability, provenance—in the model before tuning spectacle.

Observed references: [River Bend](https://sael.net/river-bend/) for flow, evolving banks and cross-sections; [Soap Bubble](https://sael.net/soap-bubble/) for shape and surface appearance; [Token Town](https://sael.net/token-town/) for repeated objects and curved motion trails. These are visual and targeted-source references, not independently calibrated simulations.
