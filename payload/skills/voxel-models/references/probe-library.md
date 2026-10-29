# Gen1: forty preserved construction probes

Use the relevant recipe as editable example code, not as a mandatory art style. All geometry is original. `scripts/library_recipes.py --category <category> --output <directory>` writes five VOX/OBJ/MTL sets; `--model <slug>` selects one. CLI uses only the Python standard library. Preview generation belongs to the separate research project, not a dependency of this skill.

| Category / CLI value | Slugs | What the five constructions teach |
|---|---|---|
| Plants / `nature` | fir, oak, willow, palm, mushroom | Tiered cones; connected branch/canopy masses; hanging foliage; curved leaf ribs; domed cap with a distinct underside. |
| Buildings / `architecture` | cottage, chalet, watchtower, gatehouse, pagoda | Openings and separate roof; frame and balcony; hollow tower and crenellation; true arch passage; diminishing tiers and curved eaves. |
| People / `characters` | ranger, knight, north, mage, farmer | One detailed body with silhouette-changing clothing/equipment; visor, shield, fur cap, robe/staff and fork. These are static grids, not rigs. |
| Creatures / `creatures` | fox, wolf, bear, deer, dragon | Body/head/leg proportions; distinct tail or muzzle; broad heavy mass; branching antlers; membrane and connected dorsal spines. |
| Vehicles / `transport` | blue-compact, pickup, bus, tractor, boat | Wheel arches and glazing; open bed; repeated windows; different wheel diameters; hollow tapered hull and sail. The blue compact is an original fictional vehicle, not an exact Toyota model. |
| Props / `props` | well, guitar, chest, bookshelf, vending | Cut cavities; contiguous thin details; barrel-profile lid; repeated shelves and books; functional front regions. |
| Land / `terrain` | snow-mountain, mesa, river-gorge, island, rock-arch | Radial height field; layered plateau; sinuous channel and drop; coast band; explicit arch subtraction. |
| Dioramas / `scenes` | knight-camp, farmstead, harbour, alpine-camp, desert-market | Ground/path-first staging; agricultural repetitions; shore/dock/boat contact; snow and tree hierarchy; stalls and a circulation lane. |

## Adaptation decisions

Scale choices: see [resolution-lod, Keep four quantities separate](resolution-lod.md#keep-four-quantities-separate). These research previews auto-fit each object.
- Do not enlarge a coarse array by nearest-neighbor replication and call it new detail. Reconstruct wheel profile, facial parts, frames, branch structure and thickness at the intended pitch. Three initial detailed probes were rebuilt this way after the user's resolution feedback.
Part anchors: see [mixed-grids, Mixed local grids in a metric world](mixed-grids.md#mixed-local-grids-in-a-metric-world). In addition, operation order matters: hollowing a bucket after adding the rope removed its support; adding the rope after subtraction repaired it.
Connectivity expectations: see [built-form, Function, cavities and localized wear](built-form.md#function-cavities-and-localized-wear). In addition, these thin oblique roofs/membranes need overlap for intended six-neighbor connectivity; component inspection revealed disconnected diagonal strips.
- Derive attached detail from the underlying surface. Dragon spines originally used a fixed height and floated above the tapering tail; sampling the local column's top before attaching each spine corrected it.
- Keep the meaning of the seed honest. A deterministic fixed preset is reproducible without exposing variation. Fir, oak and bookshelf use seed variation; other presets require explicit recipe changes or new semantic parameters. Compact examples generated with different seeds can collide in geometry.

## Actual verification and limits

The research builder generated forty unique hashes, five per category; checked determinism, bounds and cell roundtrip; inspected eight category sheets with two opposing views. Exports use the checked opaque palette mesher. External editor import, UV/texturing, rigging, collisions and LOD transitions were not validated.

Game articulation: see [objects, People and creatures](objects.md#people-and-creatures). Physical scale: see [resolution-lod, Keep four quantities separate](resolution-lod.md#keep-four-quantities-separate). Author collision proxies as required.


Gen1 passed file checks but received later feedback about anatomy, overly regular forms and unsupported water. For new work needing those improvements, use [Gen2](gen2.md) and the relevant anatomy/organic/built method. Keeping these examples supports honest version comparison, not a claim that Gen1 is the current quality target.
