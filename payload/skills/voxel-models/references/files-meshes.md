# Files and meshes

## Inspect the actual representation

The `.vox` suffix is shared by incompatible formats. MagicaVoxel begins with `VOX ` and uses bounded chunks including SIZE/XYZI and palette data. Its palette index0 represents air; RGBA entries0–254 map to indices1–255. Slab6's legacy VOX begins with three dimensions, then a dense grid and a6-bit RGB palette;255 denotes air. Detect signature, dimensions and expected payload length before choosing a reader.

Primary specifications: [MagicaVoxel format](https://github.com/ephtracy/voxel-model/blob/master/MagicaVoxel-file-format-vox.txt), [scene extensions](https://github.com/ephtracy/voxel-model/blob/master/MagicaVoxel-file-format-vox-extension.txt), [Ken Silverman's legacy VOX](https://www.advsys.net/ken/build.htm). Modern scene transforms, layers, materials and frame references require more than reading grid chunks. Preserve or explicitly reject unsupported scene information; never flatten untransformed parts as if they were the original scene.

Inspect archives without executing their contents. Bound entry count, uncompressed size and nested depth. Some legitimate kits use an inner ZIP for each export format. A page may advertise VOX while a selected attachment contains only OBJ/FBX; record what was actually obtained.

Assembly origins: see [mixed-grids, Mixed local grids in a metric world](mixed-grids.md#mixed-local-grids-in-a-metric-world). Example: the studied 25×25×96 road container has a flat 625-cell tile; automatic trim needs its retained placement offset.

## Preserve visible geometry while exporting

Cull faces between occupied cells. Merge adjacent coplanar faces only when direction and semantic rendering keys match. For an opaque unlit palette baseline the key is plane/direction/color. Materials, transparency, ambient occlusion, UV layout and per-face lighting may require more keys. Greedy rectangles reduce geometry; they are not guaranteed globally minimal and should not erase color boundaries.

The original helper verifies exact surface/color coverage, non-overlap and winding on a cuboid, a mixed-color cavity and eight specimens. It writes flat OBJ faces with MTL colors and transforms z-up cells into `(x,z,-y)` for y-up output. This is a coordinate convention, not external-editor acceptance. Native VOX remains the editable source; the mesh is derived.

Moving parts: see [objects, People and creatures](objects.md#people-and-creatures). Runtime measurement: see [runtime-accessibility, Budget the complete result](../../visual-scenes/references/runtime-accessibility.md#budget-the-complete-result). Compare mesher counts only under matching representation and material/light constraints.

Algorithm reference: [Mikola Lysenko's original meshing article](https://0fps.net/2012/06/30/meshing-in-a-minecraft-game/). The helper is independently written for this study and handles opaque palette data; it is not a copied asset exporter.
