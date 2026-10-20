# Characters, creatures, vehicles and props

## People and creatures

For a shared humanoid kit, expose head/torso/limb ratios and socket positions. Costume modules can change occupancy: a hood, skirt, helmet, boot, cloak or backpack changes the silhouette, while a jersey emblem is paint. Generate mirrored limbs first, then authored asymmetry. Keep facial signs sparse at the intended distance. Articulation requirements: see the articulation paragraph below.

For original creatures, union connected body fields with limb/neck paths, then attach distinctive ears, horns, wings, beak or tail. Color regions should follow anatomy. A conversion from a smooth CC0 source can produce many fine contour bands; viewing those bands does not recover the conversion settings or original author's process. Use them to reason about sampling, not as a hidden generation recipe.

Evidence: [Character Kit](https://opengameart.org/content/voxel-character-kit), [Character Starter](https://opengameart.org/content/voxel-character-starter-pack), [Walrus Guy](https://opengameart.org/content/voxel-walrus-guy), [Creature Pack1](https://opengameart.org/content/voxel-creature-pack1). Root inspected the Starter and Creature grid files; the Kit rig was visually reviewed, not independently rig-tested.

For articulation, preserve a local grid, parent, pivot and clearance envelope per moving part. A rotated voxel-style part need not remain aligned to the global grid. [Magic Voxel Skull](https://sketchfab.com/3d-models/magic-voxel-skull-flat-shaded-033a366f754a470795e8c7472c931407) was reviewed in front/side/back and animation/pause; its page names a MagicaVoxel→Blender workflow. Source weights/curves and native grid were not inspected.

## Vehicles and machines

Parameterize wheelbase, track, wheel radius, ground clearance and lengths of hood/cabin/cargo. Wheel pairs and axle pivots follow the articulation paragraph above. Functional openings: see [built-form, Function, cavities and localized wear](built-form.md#function-cavities-and-localized-wear). In addition, parameterize arches and cargo spaces from the vehicle dimensions. Use identity accents sparingly: lamps, service markings, bumper and cabin glazing.

The [Vehicle Starter](https://opengameart.org/content/voxel-vehicle-starter-pack) was read visually and as nested native files: four body families have with-wheel/without-wheel variants plus a separate tire. The [Forklift](https://free3d.com/ru/3d-model/voxel-forklift-5703.html) was a public premium preview study only. It suggests a general machine grammar of chassis, wheels, cage, mast, constrained carriage and functional attachment; no purchased geometry was used.

Check contact, aligned axles, cage gaps and moving-part clearances in the intended view. A prop vehicle, riggable vehicle and physically simulated vehicle have different acceptance criteria.

## Props, repeated parts and food

Choose the characteristic silhouette/negative space, then extrude a stepped mask or build a shell/profile. Books need distinguishable cover/pages/binding; bottles a height-width profile; keys a ring/shaft/teeth; instruments a body waist/neck/cavity; a container a cavity and rim under [built-form, Function, cavities and localized wear](built-form.md#function-cavities-and-localized-wear). For inventory-sized output, exaggerate a thin identifying feature deliberately rather than increasing all resolution.

For repetitive devices, derive overall width from count/pitch and preserve gaps: radiator ribs, vending stock rows, grille slats and roof lattice are modules. Keep functional framing fixed while content modules vary. Root's [vending file](https://opengameart.org/content/voxel-vending-machine) also contains floor/wall context; it is a scene, not an isolated prop.

For food/organic props, separate shape occupancy from continuous surface coordinates. Build clusters/stems or sampled ellipsoids; apply low-frequency coherent stripes/patches and sparse seeds. [Watermelon](https://free3d.com/ru/3d-model/voxel-watermelon-1964.html) was studied in color and clay views; its page advertises Alembic/mesh outputs, not a verified native grid. Distinguish fine-grid fruit from a coarse mascot style before combining them.
