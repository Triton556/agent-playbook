# Resolution, world scale and LOD

Choose initial grid density from the task's style, camera distance and performance requirements. Start detailed exploratory probes when detail is part of the brief; reduce density deliberately. Coarse art is a legitimate stylistic/technical choice, but should not silently become the baseline for detailed probes.

## Keep four quantities separate

- **World size:** how large the house/person/tree is in the intended scene. Use actual chosen units; an arbitrary design-grid unit is not a measured meter.
- **Voxel pitch:** world length of one cell. For a coherent scene kit, decide whether a common pitch or deliberate per-asset densities are appropriate.
- **Grid resolution:** dimensions of the source container and its occupied bounds. A64-cell character and64-cell house do not automatically share world scale or visible detail density.
- **Projected detail:** how many screen pixels a cell or feature occupies at the required camera. Auto-fitting every object into an equal image card hides scale differences.

Build the detailed master first when the brief allows. New sampling should refine silhouettes and useful geometry: curved profiles, wheel arches, frame thickness, face/accessory shapes, material boundaries. Splitting each old cell into eight children preserves the old staircase and adds no new geometric information.

Three fresh master probes were constructed after feedback: house54×46×51, van30×58×31 and ranger22×23×64. These are new original construction grids with extra geometry, not resized downloaded models or upscaled prior grids. World-meter pitch was not established in these examples; their labels say object-space design grids.

## Derive lower-resolution output deliberately

Keep the master as authoritative data; cache derived grids/meshes separately with source hash, scale, voxel pitch, bounds/origin, palette strategy and reason. A2×coarser grid means2×cell pitch at the same world size, not a half-sized object. Assembly transforms: see [mixed-grids, Mixed local grids in a metric world](mixed-grids.md#mixed-local-grids-in-a-metric-world). Pivots: see [objects, People and creatures](objects.md#people-and-creatures).

Block aggregation is only a baseline. “Any occupied child” expands contours and closes gaps; majority occupancy erases thin structures. Majority colors can erase eyes, lamps or stripes. For important features use semantic protection, a dedicated LOD shape or retain the finer level. Inspect silhouette, openings, material regions and the actual required camera.

For perspective projection, a small feature's pixel extent is approximately `worldExtent × viewportHeight / (2 × distance × tan(verticalFov/2))`; for orthographic projection it is `worldExtent × viewportHeight / visibleWorldHeight`. Use stated camera units and the model's projected error, not an unexplained distance constant. Select a coarser level only when its error is acceptable for the required view. Use hysteresis if runtime switching would otherwise flicker.

Runtime measurement: see [runtime-accessibility, Budget the complete result](../../visual-scenes/references/runtime-accessibility.md#budget-the-complete-result). This research did not implement or benchmark runtime LOD switching.

## Mixed local grids

Per-asset density/mechanics details: see [Mixed local grids](mixed-grids.md).
