# Orthographic design before voxel construction

For a new asset, changed silhouette/action, new family, or integration that changes the design/scale contract, complete this stage before detailed voxel construction. Start from an object-and-kit passport, make consistent 2D design views, inspect them, repair discrepancies, then build voxels. Later voxel renders remain required. Unchanged export/reproduction of an accepted model may reuse its inspected design; do not rerun a design exercise merely to copy files.

For a procedural family/batch, preflight representative parameter extremes and record the accepted range and invariants. Variants inside that checked design range can reuse the family plan while retaining their later voxel checks; a new action, identity, world requirement or out-of-range shape triggers a new design iteration. Do not require a fresh paid image call for every unchanged seed/export.

## 1. Build the object-and-kit passport

Use the user's brief, relevant KB decisions, inspected references and accepted local models. Memory supplies traceable decisions and exemplars, not a claim that the model remembers every hidden side. Identify each critical feature's basis and planned check. Mark an unseen side as an authored choice or unknown. Inspect the actual source before using it as evidence.

Record objective, intended stylization and rejected tendencies, functional front, action/pose, materials/palette roles, world width/depth/height, origin/ground, native master voxel pitch, target camera/display and intended use. For an existing set, load its current kit specification and accepted style/scale exemplars. Record final integration pitch separately from the detailed master: independent masters can be finer; resampling later must recheck eyes, contacts and clearances. Do not stretch an asset merely to match equal-height thumbnails.

**Reference trigger:** a critical feature has no inspected basis or explicit permissible design choice; sources contradict; a shared module conflicts with the target class; the required feature is not assessable in available views; or a repeated defect has no reproduced cause. Resolve the affected uncertainty through source inspection, targeted references or a bounded prototype. Questions to the user concern unresolved material choices/private references, not ordinary continuation. A critical unknown blocks its dependent detailed construction, while independent preparation continues.

**Done:** critical features have a basis and observable check; dimensions/style/pose/context are explicit; existing-kit constraints are loaded or the work is explicitly standalone. Missing important constraints remain unknown, not guessed facts.

## 2. Create one coherent six-view design

Produce front, back, left, right, top and bottom from the **same object, pose and dimensions**. The front is the functional side. Use orthographic projection, common pixels per metre, labelled axes/dimensions and a shared origin/ground. Identify recognition features, openings, eyes, grips, attachments and clearances. Add a 3/4 concept for style or closeups when the orthographic sheet cannot show the intent. For an existing kit, include a separate same-scale comparison with an accepted object/person.

Views can be original vector sketches, generated concept imagery or projections of a lightweight analytic/block layout. A block layout is a design aid, before detailed occupied voxel geometry. Use imagegen for AI bitmap concepts when appropriate. A request for six image panels does not itself guarantee consistent geometry; inspect and reconcile the outputs. Do not use six recoloured copies of one angle. Deliberate symmetry is declared, not used to skip an uninspected side.

For image generation, provide the same passport and accepted visual exemplars in every revision. Ask for one fixed identity/pose, true orthographic views, preserved component counts and positions, and the selected style. Check whether the returned views satisfy this; a written prompt is not a pass. Retain failing sheets with their revision.

Multi-view consistency is a technical concern in [MVDream](https://arxiv.org/abs/2308.16512); that research is supporting context, not a statement that our ordinary image tool implements its method. Even consistent silhouettes do not uniquely determine hidden volume or prove valid 3D topology.

**Done:** six actual inspectable views exist; cross-view dimensions/landmarks agree; functional features are assessable; a kit comparison is available when applicable. Metadata and frame count alone do not satisfy visual inspection.

## 3. Run the design review loop

Inspect the actual sheet and relevant closeups at intended review size. Write separate current observations for:

| Criterion | Required observation |
| --- | --- |
| Coherence | Same identity, pose, component count, dimensions and landmark locations across all six views; no invented different back |
| Style | Compare named silhouette/proportion/palette/detail traits against the accepted exemplar; retain intentional simplification and character |
| Context | Correct world proportions, material/use/era/biome, target camera/device; same-scale kit comparison confirms the proposed integration |
| Function | Explain the action, supports, grip/socket, opening and moving clearance; distinguish necessary contact from collision |
| Readability | Identify the object/action and key feature in the intended view without relying on the title; zoom when the overview cannot decide |
| Usability | Confirm the intended use and, for a viewer, the inspection scenario and legible controls. State the relevant static use when the artifact has no UI |

Record defect -> cause hypothesis -> changed passport/sheet -> recheck. If a view, pose, dimension or style choice changes, update the other affected views and invalidate the previous design review. Finish when these criteria pass for the current plan. An unchanged failed loop needs a new cause/reference, not another blind image call. Routine repairs follow the chosen participation mode: show the design at an agreed human checkpoint and wait before dependent construction; autonomous mode uses author self-review. This stage adds no new approval point.

## 4. Bind readiness, then voxelize

Use `scripts/design_preflight.py snapshot --root <project> --passport <relative-json>` to bind the passport, all view images, kit and local basis files. After actual inspection, save the reviewer, timestamp, digest and observations. Then run:

```text
python <skill>/scripts/design_preflight.py validate --root <project> --passport <relative-json> --review <relative-review-json> --output <relative-report-json>
```

Exit0 means the declared geometric/kit constraints and all required current design-review records pass. Exit2 means design readiness is incomplete; exit1 means malformed input. The helper does not call models, inspect image content, judge style, guarantee truthful review or infer hidden geometry. It validates the authored contract and actual file hashes; see [passport format](design-passport.md).

Voxel construction uses the accepted passport revision, landmarks, palette roles, native pitch and planned sockets. Preserve the accepted 2D design. Render the resulting voxels in matching views and compare their silhouette/scale/features against the design, then run the existing technical/semantic/style/context/readability/use checks. A passing concept does not automatically approve its 3D implementation. Record justified design changes as a new revision and recheck the affected plan.

The [reference triggers](../../product-engineering/references/reference-grounding.md) and [shared perception protocol](../../product-engineering/references/human-perspective-review.md) are common authorities. This branch specifies the six-view representation and kit constraints. Its review follows the participation mode in the task brief; human feedback is recorded only when actually received. Retain stylization and successful exceptions rather than increasing realism by default.

## Material contour and mixed-grid scope

Review the major contour of principal material/color regions independently of cross-view agreement and later3D transfer; use [Major material boundaries](material-boundaries.md) for prominent natural markings. Preserve supported stylization and ordinary cell-scale steps. Schema1 remains a single-integration-kit check; [Mixed local grids](mixed-grids.md) explains separate world/model/mechanics contracts without weakening its existing constraints.
