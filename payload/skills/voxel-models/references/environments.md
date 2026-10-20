# Nature, architecture, terrain and scenes

## Plants and seasonal forms

Represent a tree with a structural trunk/branch graph and attached crown groups. Species controls taper, branch tiers and crown profile; age controls coherent height/width rather than arbitrary per-cell growth. A conifer can use layered shrinking profiles; a broadleaf crown can use connected lobe volumes. Retain primary silhouette while adding limited irregular edges.

Tie seasonal surfaces to geometry: snow belongs on exposed upward regions, foliage changes by connected crown groups, bark follows trunk/branch regions. Do not let a color mask hide unsupported floating leaves. Ground contact and projection gaps need inspection at the intended camera. These are original construction inferences; this study did not recover an author's tree-generation code.

## Buildings and interiors

Use footprint, floor/wall thickness, facade bay spacing, floor count and roof profile as explicit variables. Functional openings: see [built-form, Function, cavities and localized wear](built-form.md#function-cavities-and-localized-wear). In addition, construct the building shell and repeated modules from its footprint variables. A facade may be richer than a back wall by design, but a reusable freestanding asset needs a conscious decision about all views. Cavity inspection follows built-form.

The inspected [Voxel Buildings](https://opengameart.org/content/voxel-buildings) grids repeat stories, roof lines and window recesses with small palettes. Their occupied cell counts vary widely; a large SIZE container can remain mostly empty. The [Modular Bathroom](https://opengameart.org/content/modular-bathroom-voxel-art) has common wall containers20×40×80 and a corner20×20×80. Kit assembly: see [mixed-grids](mixed-grids.md#mixed-local-grids-in-a-metric-world); a common container is evidence of a module relationship, not proof of its assembly algorithm.

In addition to built-form’s cavity rule, inspect basin/bath rims, basket openings, chair/bed spaces and appliance grilles as applicable. Keep environment geometry separate from the asset if the requested output is a library part. In a staged room, removed walls can be an intentional camera cutaway rather than an incomplete model.

## Terrain and tile contracts

Specify boundary elevations, path connectors and a consistent tile origin. Adjacent modules must agree at shared edges. Road examples [I](https://opengameart.org/content/road-i), [L](https://opengameart.org/content/road-l-0), [T](https://opengameart.org/content/road-t), [X](https://opengameart.org/content/road-x) use25×25 bases; their path identity is largely paint on a fully occupied square. Thus appearance and route topology should be separate states in a generator.

For original terrain, sample a controlled height field, quantize it to the grid and define connected routes before placing props. Reserve clearance around doors, crossings and intended views. Geological strata, cliffs and caves should be coherent volumes or cuts, not scattered dark cells. Preserve boundary constraints when generating variants.

## Diorama composition

Choose large support masses and a small number of landmarks first, then connected medium-scale repetition and sparse accents. Camera, cut plane and source scale are part of the deliverable. The studied [Desert Mountain City](https://sketchfab.com/3d-models/desert-mountain-city-bdf7ec273179460eae41781947a51695) reads through terraced masses, repeated small architecture and a few roof accents; orbit reveals a flat back cut plane. Geometry is credited to yaelsagi, uploaded by ephtracy. Root viewed three angles; no native file was inspected.

For an original settlement, combine a terrace field, route graph, reachable building sockets and facade/roof grammar. Validate traversal/collisions independently of attractive composition. A beautiful path is not evidence that an agent or character can navigate it.

The catalog and environment research retain source-specific visual notes. Read those only when they help choose a style or construction approach; this branch supplies general decisions, not a requirement to imitate one scene.
# Expanded scene observations: practical transfer

For new procedural work, keep source appearance observations separate from these original engineering decisions:

- **Grid versus appearance:** a large cubic envelope can carry fine painted pixels without fine geometry. Choose world extent W and grid count N independently (pitch W/N); compare fixed-camera renders and occupancy, not only auto-fitted thumbnails.
- **Shape versus gradient:** quantize the height/shape field separately from the palette field. Contour bands, grass/sand/coast zones and foliage colors can follow height or semantic regions. More palette bands do not automatically add geometric resolution.
- **Water representation:** distinguish a surface, falling strip, shoreline/support mask and an optional depth cutaway. A static thick blue side face does not establish fluid motion, refraction or conservation. Label an illustrative waterfall as such unless a physical model is actually implemented and checked.
- **Navigation versus projection:** intersecting stair flights in one camera do not prove a valid 3D connection. Give each run endpoint/landing IDs and local up; verify the adjacency graph with another view or matched diagram. Screen-space contact is not a navigable edge.
- **Season versus density:** branch skeleton, canopy occupancy and palette need independent controls. A seasonal color change should not unintentionally change species or branch structure. Check small leaves and frame infill at the actual viewing size; surviving outer silhouette does not mean thin detail remains readable.

These criteria came from twelve enlarged environment previews plus source metadata checks. Their original cell resolutions, hidden geometry and author algorithms remain unknown. Full evidence and source-specific rights are in the local study's `research/environments/entries.json`, `expansion/deep-source-review.json` and `recipes.md`.

