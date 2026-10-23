---
name: voxel-models
description: Create or refine requested voxel models and their presentation, with actual render checks. Ordinary UI and non-voxel scenes use their own skills.
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

Loading and recovery: see [WORKFLOW, Work route](../../workflow/WORKFLOW.md#work-route).

## From brief to a model

Establish the object's role, intended view/distance, style, approximate world size and required output. Respect an agreed target: an editable grid, game mesh, static diorama and riggable character have different structure. Use reference images across enough views to understand the volume; mark hidden sides unknown rather than reconstructing them as facts.

Before detailed construction: see [design-preflight, Orthographic design before voxel construction](references/design-preflight.md#orthographic-design-before-voxel-construction).

Scale: see [resolution-lod, Keep four quantities separate](references/resolution-lod.md#keep-four-quantities-separate). Combining grids: see [mixed-grids, Mixed local grids in a metric world](references/mixed-grids.md#mixed-local-grids-in-a-metric-world). Put recognition into silhouette/negative space before detail; roof ridge, horn, wheel spacing, cavity or hat often carries identity. Inspect neutral light and intended camera before spending cells on detail.

Exploratory density choice: see [Resolution and LOD](references/resolution-lod.md#resolution-world-scale-and-lod).

Assign palette roles to connected material/semantic regions. For prominent natural markings, separately inspect the [major material contour](references/material-boundaries.md) before accepting its 2D-to-3D transfer. Distinguish silhouette variation, attached-part variation and painted variation. Shape comes before noise; spatially coherent color masks remain legible and allow larger mesh rectangles. Keep an optional baked-light palette separate from base albedo when another renderer will light the model.

Assembly frame: see [mixed-grids, Mixed local grids in a metric world](references/mixed-grids.md#mixed-local-grids-in-a-metric-world). Moving parts: see [objects, People and creatures](references/objects.md#people-and-creatures). Separate an asset from its presentation floor/wall when an asset rather than a scene is requested.

Review body support, useful cavities, branch attachment and flow paths as semantic structure. File validity or one connected component does not supply these checks. Read the relevant anatomy, organic or built reference when this structure matters.

For procedural work, represent primary dimensions, modules, palette roles and bounded variation explicitly. Use seeds, semantic constraints and meaningful parameter ranges. Verify changes in the relevant view and structural invariants; changing a seed must not merely scatter disconnected cells.

Deliver requested files and a concise provenance/validation note. Validate bounds, palette and roundtrips; inspect silhouette/contact/occlusion in rendered views. Result grades: see [human-perspective-review, Readiness and transfer](../dev-flow/references/human-perspective-review.md#readiness-and-transfer). Performance evidence: see [runtime-accessibility, Budget the complete result](../visual-scenes/references/runtime-accessibility.md#budget-the-complete-result).

For repeated defects or a multi-model batch, use the quality adapter above. Evidence revisions: see [quality-ledger, Schema version 1](../dev-flow/references/quality-ledger.md#schema-version-1). Semantic contact/visibility requires declared part masks; quality claims: see human-perspective-review, Readiness and transfer.

## Helpers on demand

Choose a helper by the actual operation: [files and meshes](references/files-meshes.md) for VOX inspection/mesh export; [quality adapter](references/quality-cycle.md) for Gen2.1 repairs; [Gen2](references/gen2.md) or [probe library](references/probe-library.md) only when adapting those examples. Scripts export geometry/metadata, not visual approval. Recipes are original starting points, not a universal generator or the default quality target. Preserve format, palette, origin and mesh invariants while adapting a recipe.


Perception method: see [human-perspective-review, Inspection sequence](../dev-flow/references/human-perspective-review.md#inspection-sequence). Preflight/reuse: see [design-preflight, Orthographic design before voxel construction](references/design-preflight.md#orthographic-design-before-voxel-construction). Batch completeness: see [task-state](../dev-flow/references/task-state.md).
