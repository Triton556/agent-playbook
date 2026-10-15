# Procedural construction

## A useful asset grammar

Keep four layers distinct: structural dimensions and anchor graph; optional attached modules; palette/material roles; presentation camera/light. Give the seed stable control of bounded choices. Parameters should express age, species, floor count, roof pitch, wheelbase or equipment rather than unrestricted cell noise.

Use a shared cell grid with constructive addition/subtraction: boxes and shells for buildings, ellipsoids/capsules for body masses, integer profiles for stepped roofs/arches, and sampled connected paths for limbs/branches. A sample point alone is not a connected branch; union overlapping cross-sections or fill the path.

Variation order: primary proportion → secondary module selection → connected palette mask → limited surface irregularity. Generate comparable views with the same seed and camera while testing one change. A variant's identity features should stay legible in silhouette.

## Semantic constraints

| Family | Parameters | Structural checks |
| --- | --- | --- |
| Tree | height, crown width, taper, branch tiers, season | trunk reaches canopy; crown groups attach; snow follows upward exposure |
| Building | footprint, wall/floor thickness, bays, floor count, roof | entrance connects outside to inside; roof covers shell; modules share pitch/origin |
| Creature | torso/head ratios, limb paths, appendages | limbs contact torso; eyes on head surface; characteristic contour survives variation |
| Vehicle | width/length, wheelbase, cabin/cargo, wheel radius | axle pairs align; wheels fit arches; roof/glass/body remain distinct |
| Prop | shell, characteristic opening, braces/accent | cavity remains open where intended; thin detail survives required view |
| Road/terrain | connector masks, elevation, edge profile | adjoining edges match; paths connect; decorations leave passage clear |

Choose a connected-component expectation per asset. A single creature often needs one main connected body, but separate wheels, companions, floating effects or scene modules can be intentional. Treat component counts as inspection evidence, not a universal deletion command.

## Demonstrated transfer

Eight original recipes—conifer, broadleaf tree, cottage, van, ranger, fox, crate and arch—were generated with three seeds each. They serialize to native MagicaVoxel grids; roundtrip cell/color equality and reproducibility were checked. Eight baseline meshes were exported as OBJ/MTL. No downloaded geometry was used. This validates these small examples; complex rigs, large scene graphs and an all-category production generator remain future work.

A matched-geometry color-mask experiment changed only the conifer's palette assignment. Occupancy stayed3492 cells and visible surface stayed2522 unit faces. Greedy rectangles fell from2102 to1292 when fragmented paint was replaced with coherent regions. The result measures this opaque palette mesher's output, not FPS or a universal speed gain.
