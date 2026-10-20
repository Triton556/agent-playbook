# Shape and palette

## Cell size follows recognition

Pick the smallest silhouette feature the object needs at its intended viewing distance. A one-cell eye, thin rim or axle can survive close inspection and disappear in a distant top-down scene. Choose pitch with that distance in mind; a higher matrix resolution is not automatically more readable. Scale: see [resolution-lod, Keep four quantities separate](resolution-lod.md#keep-four-quantities-separate).

Block primary masses, then structural secondary features, then small identifying accents. For organic subjects use overlapping ellipsoids/capsules, stepped profiles and connected limb paths; for built objects use shells, repeated bays and explicit openings. These primitives are construction options, not proof of how a source model was authored.

Recognition checklist by shape: tree trunk/crown split; animal torso/head/limb ratios and characteristic ears or horns; vehicle wheelbase, cabin profile and cargo volume; building roof and repeated facade; prop's characteristic cavity or projection. View the neutral silhouette from the required angles. A diorama may intentionally expose a flat cut plane on the back; a freestanding prop requires a different decision.

## Paint meaningful regions

Use roles such as body, structure, dark recess, light trim, foliage and identity accent. Roles can map to a handful of colors with shadow/highlight ramps, then to file-local palette indices. The studied grids use one to31 colors; that is an observed range, not a rule to enforce. Character Starter uses five to12 colors while preserving a common16×16×32 matrix.

Place large patches where the object explains them: beagle's coat, ranger's clothing, vehicle glass, roof material. Random per-cell color fragments surfaces and weakens material reading. If variation is useful, correlate it in space or tie it to geometry/exposure. Let the renderer supply ordinary lighting; preserved palette bands may already contain baked shading.

Shape versus paint: see [built-form, Function, cavities and localized wear](built-form.md#function-cavities-and-localized-wear). The road samples illustrate the distinction: a full square grid can contain a path that is entirely a color mask.

## Transfer observations into choices

Record an example's visible mass ratios, the two or three identity features, palette roles, repeating modules, view dependence and unknown sides. Convert each observation into a parameter or constraint. Prefer “wheel centers share an axle and do not intersect the chassis” over “add more car detail.” Keep the proposed procedure explicitly an inference.

Sources examined: [Character Starter](https://opengameart.org/content/voxel-character-starter-pack), [Creature Pack1](https://opengameart.org/content/voxel-creature-pack1), [Vehicle Starter](https://opengameart.org/content/voxel-vehicle-starter-pack), [Classical Guitar](https://opengameart.org/content/voxel-classical-guitar). The conclusions combine observed images and inspected grid files; author construction steps were not recovered.

## Decisions clarified by the expanded visual study

- At coarse pitch, a muzzle, brow or nose often needs a separate geometric depth level; a flat color patch does not replace the projection. Test your own object as a small one-color silhouette before spending detail on texture.
- Fine-grid staircase shading can become a strong surface pattern. Compare flat color, soft light and directional light on the same original object. Keep palette variation inside connected anatomy/material regions so that color noise and lighting do not compete.
- Minimum connection thickness and minimum readable gap are independent constraints. A limb or brace may remain connected while its adjacent opening disappears in the intended view. Give gaps explicit dimensions rather than hoping they survive every parameter combination.
- For modular machinery, roles such as shell/joint/active/marker organize color better than random palettes. A small indicator can repeat the working element's accent at a smaller scale while dark joints remain narrower and recessed.
- Render RGB is not the source palette. Grain, chromatic shifts, illumination and oblique bevels can create edges/colors absent from a strict native grid. Tag MagicaVoxel and a block-like silhouette alone do not prove native VOX, axis alignment or exact cell resolution.

These are original modeling criteria derived from visual observations; they do not reconstruct the studied authors' algorithms. Full observed examples and limitations live in the local study's `research/objects/extension-takeaways.md` and `extension-deep-reviews.md`.
