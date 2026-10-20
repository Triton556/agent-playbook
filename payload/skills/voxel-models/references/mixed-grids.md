# Mixed local grids in a metric world

Clarification recorded in the source workflow on 15 October 2026. Choose the relevant scale contract before construction; this note does not require resampling existing models.

Four scale quantities: see [resolution-lod, Keep four quantities separate](resolution-lod.md#keep-four-quantities-separate). In addition to that scale contract, mixed assets declare an instance transform and separate mechanics/proxy grid.
- In addition to resolution-lod, Keep four quantities separate, a specific modular seam or cross-object voxel operation declares its required common pitch.
- p/2p/4p is a proposed comparison, not a mandatory ratio or chosen physical pitch. Independent props need not have mathematically commensurate cells.
- Preserve world dimensions, origin, orientation, normalization offset, support plane and sockets. Articulated pivots: see [objects, People and creatures](objects.md#people-and-creatures).
- Convert mixed-model contacts, overlap and clearance into a declared metric frame or explicit shared proxy before comparison. The current semantic_contract.py expects integer cells in one declared source space; direct comparison of different local indices is invalid.
- Collision/navigation/destruction can use their own representations and precision. Express cross-object operations in world units with explicit local conversion, rounding and minimum fragments. Cell mass at fixed material density scales with pitch cubed.
- Design passport schema1 / design_preflight.py checks the declared single-integration kit. Its successful shared/independent-master check does not validate arbitrary mixed runtime integration. Keep its current constraints intact until a separate mixed contract is implemented.

Inspect a connected scene at the intended camera: scale and grain, useful features, seams and supports, interaction/contact, then LOD transitions and measured frame cost. Multiple pitches alone establish neither stylistic coherence nor failure. Gen2.1 already uses individual voxelPitchMeters; current models and generators remain authoritative and unchanged.

Research basis: the source owner's mixed-voxel-scales-research-ru.md, 15 October 2026 (not bundled). Full materialization on this Windows executor is currently blocked by the official Library helper's missing os.setxattr; only the verified reading and synthesis are retained here.
Primary references: https://www.openvdb.org/documentation/doxygen/transformsAndMaps.html ; https://teardowngame.com/modding/api.html#GetShapeSize ; https://transvoxel.org/ .
