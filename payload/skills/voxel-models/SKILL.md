---
name: voxel-models
description: Create, inspect and procedurally generate voxel art models as editable grids and palette-preserving meshes. Use for voxel assets, modular kits, voxel creatures and voxel dioramas; ordinary low-poly modeling and general UI design use their own workflows.
---

# Voxel model craft

Build a recognizable original object on an intentional cell grid. Study references to recover useful decisions about silhouette, scale, palette and modularity; reviewing a model does not reveal its author's construction history. This skill stores methods and original helpers, not a trained model or a library of copied assets.

## Choose the relevant branch

| Work | Read |
| --- | --- |
| New asset, redesigned silhouette/action, new family or existing-world integration: 2D design before voxels | [Orthographic design preflight](references/design-preflight.md) |
| Shape, proportions, palette, readable details and manual construction | [Shape and palette](references/shape-palette.md) |
| Choose detailed source grids or derive a lower-resolution version | [Resolution and LOD](references/resolution-lod.md) |
| Terrain, plants, buildings, rooms and modular scenes | [Environments](references/environments.md) |
| People, creatures, vehicles, machinery and props | [Objects](references/objects.md) |
| Limb joints, feet, stance and anatomical negative space | [Anatomy and support](references/anatomy-support.md) |
| Irregular plants, terrain, damage and connected water | [Organic form](references/organic-form.md) |
| Functional cavities, construction rhythm and localized wear | [Built form](references/built-form.md) |
| Functional face/eyes/grips, world scale, contacts, storage budgets and Gen2.1 | [Quality cycle adapters](references/quality-cycle.md) |
| Gen2 examples, versioning and defect-specific checks | [Gen2](references/gen2.md) |
| Seeded variants, semantic constraints and grammar | [Procedural construction](references/procedural.md) |
| Reuse/adapt one of forty original construction probes | [Probe library](references/probe-library.md) |
| Inspect/export VOX, mesh it or diagnose a format mismatch | [Files and meshes](references/files-meshes.md) |
| Study coverage, sources and limits of the recipes | [Evidence](references/evidence.md) |

Load the branch needed for the object and deliverable; the entire catalog is not a required context load.

## From brief to a model

Establish the object's role, intended view/distance, style, approximate world size and required output. Respect an agreed target: an editable grid, game mesh, static diorama and riggable character have different structure. Use reference images across enough views to understand the volume; mark hidden sides unknown rather than reconstructing them as facts.

For new construction or a changed silhouette/action/scale contract, first complete the [2D design preflight](references/design-preflight.md): traceable object/kit passport, six coherent orthographic views and a same-scale kit comparison when applicable. Inspect style, context, function, readability and intended use; resolve cross-view/scale contradictions before detailed occupied voxels. Bind the current design review with `scripts/design_preflight.py`; do not substitute later finished-model renders for this preconstruction step. Unchanged export/reproduction may reuse an accepted inspected design. Follow the chosen participation mode at its existing checkpoints; this stage adds no new approval request. A local repair that preserves the accepted design uses that basis and affected model checks. If schema1-bound inputs change, its digest/review must be refreshed; no scoped schema or bypass is implied.

Declare a common metric scale and an explicit density policy, then block the main masses. A coherent scene may use deliberate per-asset pitches; retain a shared pitch where the declared kit/seam requires it. Read [Mixed local grids](references/mixed-grids.md) when combining assets or mechanics at different resolutions. Put recognition into silhouette and negative space before small detail. A roof ridge, horn, wheel spacing, cavity or large hat often carries more identity than surface texture. Check a neutral light view and the intended camera before spending cells on detail.

For the user's exploratory probes, prefer a detailed master grid as the baseline. Choose lower density for stated requirements, camera-distance LOD or performance needs; low density is a valid choice, not a quality failure. Separate world size, voxel pitch and grid resolution as explained in [Resolution and LOD](references/resolution-lod.md).

Assign palette roles to connected material/semantic regions. For prominent natural markings, separately inspect the [major material contour](references/material-boundaries.md) before accepting its 2D-to-3D transfer. Distinguish silhouette variation, attached-part variation and painted variation. Shape comes before noise; spatially coherent color masks remain legible and allow larger mesh rectangles. Keep an optional baked-light palette separate from base albedo when another renderer will light the model.

For modular or moving assets, preserve anchors, scale, sockets and independently moving parts. Occupied bounds help camera fitting; trimming empty grid space must not silently change a module's origin. Separate a prop from its presentation floor/wall when the requested output is an asset rather than a scene.

Review body support, useful cavities, branch attachment and flow paths as semantic structure. File validity or one connected component does not supply these checks. Read the relevant anatomy, organic or built reference when this structure matters.

For procedural work, represent primary dimensions, modules, palette roles and bounded variation explicitly. Use seeds, semantic constraints and meaningful parameter ranges. Verify changes in the relevant view and structural invariants; changing a seed must not merely scatter disconnected cells.

Deliver the requested files and a concise provenance/validation note. Validate coordinate bounds, palette mapping and meaningful roundtrips; inspect silhouette, contact and occlusion in rendered views. File checks do not establish aesthetic quality, animation readiness, external-editor compatibility or FPS. Record those separately when actually tested.

For repeated defects or a multi-model batch, use the general artifact quality cycle through the quality adapter above. Bind checks and inspected views to the current source/artifact revision; preserve accepted style exemplars. Semantic contact/visibility tests require declared part masks and do not establish natural action or beauty.

## Helpers on demand

Choose a helper by the actual operation: [files and meshes](references/files-meshes.md) for VOX inspection/mesh export; [quality adapter](references/quality-cycle.md) for Gen2.1 repairs; [Gen2](references/gen2.md) or [probe library](references/probe-library.md) only when adapting those examples. Scripts export geometry/metadata, not visual approval. Recipes are original starting points, not a universal generator or the default quality target. Preserve format, palette, origin and mesh invariants while adapting a recipe.

Public viewing, free pricing and reuse rights are different. Record a source asset's own license before copying or adapting its data; preserve required credits. Unknown, paid or NoAI-marked assets remain view-only references in this study and are not bundled in the skill. Creating original geometry from general form principles does not require importing the reference asset.

Use the [shared perception protocol](../dev-flow/references/human-perspective-review.md) for intended character, context, recognition and use at the agreed scale. First reading, geometric diagnosis and actual human acceptance remain separate. The six-view design preflight and later voxel inspection have different purposes; approved family ranges can be reused with their stated limits. For batch completeness and recovery, keep the declared output list through [task-state](../dev-flow/references/task-state.md).
