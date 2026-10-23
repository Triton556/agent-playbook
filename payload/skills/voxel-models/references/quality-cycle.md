# Function, scale and evidence after Gen2 feedback

Read the general [artifact quality cycle](../../dev-flow/references/quality-cycle.md) for repeated defects or a batch. Keep that workflow general; the following are voxel adapters and scoped examples.

Construction preflight: see [design-preflight, Orthographic design before voxel construction](design-preflight.md#orthographic-design-before-voxel-construction).
Scale quantities: see [resolution-lod, Keep four quantities separate](resolution-lod.md#keep-four-quantities-separate). In addition, use common pixels-per-meter side sheets for kit proportions; label auto-fit previews.
- Name the functional face and its feature: face/eyes, headlights/windshield, passenger door, book spines, controls, latch or useful cavity. Render four distinct directions when occlusion matters; a before/after pair at one angle remains one direction. Zoom must retain full-grid occluders, not crop geometry to expose a hidden eye. Inspect creature heads front and both profiles, and ambiguous hand grips at their real review size.
- An eye gate applies when visible eyes belong to the intended design. A deliberately eyeless creature has an explicit style exception. A flat instrument's1.05m length is not its Z thickness; declare the primary dimension/orientation before deriving pitch and common-scale captions.
- Capture part ownership before union. Test forbidden overlap independently of colors. Axle/hub and wing-root contacts are required attachments; free wheel/membrane clearance is separate. A contact check does not know that a hand is holding the bow frame rather than its string: use typed subparts and inspect the action.
- A static opaque master may omit hidden core cells while preserving exterior colors/geometry, load cores and editable connections. Restore original-cell bridges if hollowing disconnects branches. Export declared opaque exterior to avoid inaccessible inner faces. Collision/volume uses its own representation; no universal shell threshold applies. Performance claims: see [runtime-accessibility, Budget the complete result](../../visual-scenes/references/runtime-accessibility.md#budget-the-complete-result).
- Choose wear from cause and material: damp bases, staggered irregular masonry, edge chips, contact abrasion, seams along wood grain and gravity/deposition of snow. Maintain deliberate quiet surfaces; three tones is a useful local choice, not a universal gate. Major missing joints/cracks have geometry; small pigment wear may remain palette-only.
- Scenes declare land/water/path/dock/boat substrates, object contact footprints, epoch/biome and a life anchor. A bridge can cross water; an ordinary dirt path cannot. A desert oven needs a plausible bread-making story, rather than an automatic ban. Ground infill follows actual feet/roots instead of stamping a rectangular bounding-box podium.

## Versioned original examples

`python scripts/gen21_generate.py --model oak --seed 153 --output <directory>` produces original Gen2.1 VOX/OBJ/MTL plus a construction manifest. Use `--category` or omit selectors for all40. Earlier Gen1 and Gen2 helpers remain available. These recipes demonstrate repairs, not general-purpose reconstruction of any reference. OBJ uses voxel-cell units; apply the declared pitch for a scene in metres.

Use `scripts/semantic_contract.py` for declared ray visibility, allowed contacts, forbidden overlap, clearance, material depth and substrate coverage. A missing mask returns unknown. These static checks do not judge recognition, biological correctness, pose naturalness or beauty. Pair them with inspected current images and revision-aware evidence; use the general ledger when machine validation is needed.

Pilot evidence: human Gen2 feedback; saved GLM audit reconciled against actual grids; independent bad/good fixtures; four-view and head/hand inspection. The [official Toyota NNP10 archive](https://www.toyota-global.com/company/history_of_toyota/75years/vehicle_lineage/car/id60012578/) and its front/side photograph supply compact-van proportions; other world sizes are authored stylized targets. Source observations and their limits remain in [Evidence](evidence.md).

Observation and cause hygiene: see [human-perspective-review, Inspection sequence](../../dev-flow/references/human-perspective-review.md#inspection-sequence). Voxel-specific view/eye/grip/contact/palette checks remain here.

## Mixed grids and major material contours

Cross-model metric comparisons: see [mixed-grids, Mixed local grids in a metric world](mixed-grids.md#mixed-local-grids-in-a-metric-world). Material contour inspection: use [Major material boundaries](material-boundaries.md) with unshadowed side/underside/oblique views where tiny steps recede; long axial runs and major turns trigger a source/stylization check.
