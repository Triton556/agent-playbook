# Composition and materials

## Choose the representation

| Representation | Strong use | Cost or ambiguity to resolve |
| --- | --- | --- |
| DOM + SVG | Relationships, finite graphs, annotated mechanisms, exact charts | Large numbers of nodes; keep semantics in DOM and batch drawing if needed |
| Canvas 2D | Many traces, particles, fields, dense drawing | Supply semantic controls and a textual result outside the bitmap |
| WebGL / Three.js | Depth, occlusion, material response, spatial assembly | Camera, picking, color management, GPU cost, fallback |
| Pre-rendered raster | Fixed scene, illustration, background | Cannot explain an interactive mechanism by itself |

Choose the least costly medium that preserves the needed relationship. An arbitrary 3D chart often hides values; use depth when spatial structure itself matters.

## Compose the causal path

Begin with three bounding regions: cause, mechanism, result. Put the important transition in open space, away from controls. A glass object with its incoming beam outside the frame is an incomplete explanation. A data metaphor needs its selected object and exact reading visible together.

Use a low-detail blockout to set a clear dominant shape, secondary mechanism and quiet support. Inspect the silhouette at the final display size. Thin rods, fine wire, bevels and tiny labels that exist in geometry may disappear in the delivered image.

Choose camera poses by meaning: overview → mechanism → result. Perspective emphasizes scale and depth; orthographic views improve geometric comparison. A guided move should preserve a landmark so the viewer understands where they went. User input takes ownership immediately; resuming the tour is explicit.

For perspective fitting, start with vertical distance `d ≥ h / (2 tan(fov/2))` and the corresponding horizontal bound using aspect ratio. Fit the relevant object, then account for panel occlusion and margins; this simple bound is not a substitute for rendering. On mobile, change pose or arrange the mechanism vertically rather than only increasing camera distance until everything becomes tiny.

## Make materials legible

Build distinct **material roles**: structural shell, working surface, active channel, fastener, transparent boundary. Use roughness and highlight width as strongly as base color. A tiny amount of bevel creates a useful silhouette highlight; excessive identical shine erases hierarchy.

- **Metal:** give it an environment with bright and dark shapes to reflect. Decide whether polished, brushed or coated. Keep directional grain related to manufacturing geometry.
- **Glass:** reveal front/back edges, thickness and a recognizable reflected environment. A transparent fill without edges often vanishes. Separate surface appearance from the mathematical path of light. Real transmission is useful only when its cost and distortion clarify the scene.
- **Wood, fabric, stone:** use spatially coherent scale and orientation. Start with broad pattern, add restrained fine variation; inspect for repetition and aliasing at the actual camera distance. Bake static procedural appearance when it is otherwise recomputed every frame.
- **Emissive objects:** show a sharp source plus a restrained halo; nearby surfaces may need light or a justified approximation. Bloom does not automatically illuminate the scene.
- **Ground contact:** contact shadows, supports and occlusion tell the viewer where an object sits. Floating is meaningful only when intentional.

Use a small lighting hierarchy: key for shape, fill for the mechanism's dark side, rim or reflection for transparent edges. Tune material roughness, exposure and environment together before adjusting bloom. Test a light and dark presentation if users can switch environments; additive effects that read on black may wash out on white.

## Labels are a second renderer

Entity identity: see [causal-state-interaction, Guided presets and direct control](causal-state-interaction.md#guided-presets-and-direct-control). In addition to that identity rule, each label needs a world anchor, screen projection, priority and visibility rule. Position after the camera/model update. Hide anchors behind the camera; handle offscreen and occluded labels deliberately. Resolve important collisions, or move selected details into a fixed card with a leader. Numeric units and small text belong in DOM when possible.

Reserve foreground contrast for the selected subject; quiet surrounding geometry with lower saturation, detail or light. Keep text out of the depth-of-field pass. Background blur should organize attention, never blur the only evidence of the mechanism.

Observed references: [Plane of Focus](https://sael.net/plane-of-focus/) for layered assembly; [Interior](https://sael.net/interior/) for coherent material/light changes; [Cube Graph](https://sael.net/cube-graph/) for a scene paired with a sharp 2D diagram. These motivate original recipes, not a requirement to reproduce their style.
