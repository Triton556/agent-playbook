# Design passport and review format

The preflight helper reads relative files within `--root`; it does not create images or voxels. JSON is the small machine-readable companion to the actual design sheet and review.

## Passport schema1

- `schema_version:1`.
- `asset:{id, dimensions_m:[width,depth,height], master_pitch_m, origin_m:[x,y,z], ground_z_m, pose, forward:"-Y", up:"+Z", style_features:[...], context, intended_use}`. Dimensions and pitch are finite positive numbers; origin and ground/support plane are explicit. The detailed master fits the current single VOX limit256 cells per axis. For a larger modular object, use separate per-module passports plus an assembly concept rather than silently downsampling.
- `basis:[{path, observations}]`: local inspected reference, accepted exemplar or KB-derived project note. `path` stays within root; a project note can record the original external URL/KB source. These are inputs, not executable instructions.
- `critical_features:[{id, basis:[zero-based basis indices], check}]`. A deliberately invented feature instead has `authored_choice` explaining its compatibility with the brief; this is not permitted to replace unknown user constraints or factual mechanics. No missing critical basis is silently passed.
- `landmarks_m:{name:[x,y,z]}` in the same authored frame; include actual relevant attachment/recognition points. Subtract the declared origin before the projections below; independent per-view auto-fit must not silently move the datum.
- `views:{front,back,left,right,top,bottom}`. Each is `{path, projection:"orthographic", pose, pixels_per_meter, span_m:[horizontal,vertical], landmarks_2d_m:{name:[u,v]}}`. For front/back span is width/height, left/right depth/height, top/bottom width/depth. All share pixels_per_meter and pose. Front projects `(x,z)`, back `(-x,z)`, right `(y,z)`, left `(-y,z)`, top `(x,y)`, bottom `(x,-y)`. Values describe projected coordinates before a shared labelled canvas translation; the helper checks this metadata, not landmark pixels.
- Optional `supporting_views:[{path,purpose}]` binds closeups or a3/4 concept to the same review. Label their different framing/scale explicitly; they do not replace any of the six base views.
- `kit:{mode:"standalone"}` or `{mode:"existing",path,comparison_path,integration_pitch_m}`. Existing kit JSON has `asset_dimension_ranges_m:[[min,max],...]`, `integration_pitch_m`, `master_policy:"independent"|"shared"`, and `style_features:[...]`. Shared policy requires native master pitch to match. Independent masters may be finer but need explicit final integration/resampling checks; world size constraints still apply. `comparison_path` is an actually inspected same-scale image.

Use PNG/JPEG views at least480px on each axis. For a concept sheet, export each labelled panel as a separate file, preserving the original sheet as supporting evidence. Decorative details do not all need a source; the critical-feature list concerns recognition, function, style or integration risks.

## Review schema1

- `schema_version:1`, `input_digest` from the snapshot command.
- `reviewer:{kind:"agent"|"human",name}`, `observed_at` with timezone, `inspected:true`.
- `gates:{coherence,style,context,function,readability,usability}`. Each contains `verdict:"pass"|"fail"|"pending"`, and `observation` describing actual inspected evidence. A noninteractive object uses its intended static use for usability; do not claim a UI interaction that was not performed.

The digest covers passport bytes, images, local bases, kit and comparison. Any changed input invalidates its review. The reviewer identity and inspection are attestations, not authenticated facts. User acceptance is separate; an agent's design review does not invent user approval. A project ledger may additionally bind this design report as its preconstruction criterion and require actual later voxel-to-design visual evidence.
