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

- Set physical size and voxel pitch first when producing a coherent kit. The research previews auto-fit each object and are not a common-scale comparison. Native SIZE and occupied cells describe the design grid, not meters.
- Do not enlarge a coarse array by nearest-neighbor replication and call it new detail. Reconstruct wheel profile, facial parts, frames, branch structure and thickness at the intended pitch. Three initial detailed probes were rebuilt this way after the user's resolution feedback.
- Keep a common part anchor while changing dimensions. Check the order of additive and subtractive operations: hollowing a bucket after drawing its rope accidentally removed the support; putting the rope back after the cavity operation fixed the actual geometry.
- Thin oblique roofs and membranes need enough cell overlap to preserve intended six-neighbor connectivity. A continuous-looking render can hide disconnected diagonal strips. The probes were corrected after component inspection; a one-component result still does not prove physical soundness or animation readiness.
- Derive attached detail from the underlying surface. Dragon spines originally used a fixed height and floated above the tapering tail; sampling the local column's top before attaching each spine corrected it.
- Keep the meaning of the seed honest. A deterministic fixed preset is reproducible without exposing variation. Fir, oak and bookshelf use seed variation; other presets require explicit recipe changes or new semantic parameters. Compact examples generated with different seeds can collide in geometry.

## Actual verification and limits

The research builder generated forty unique hashes, five per category; checked deterministic generation, coordinate bounds and VOX read/write cell equality; produced two opposing diagnostic views and inspected the eight category sheets. Exports use the separately checked opaque palette mesher. These checks establish inspectable prototypes. External editor import, UV/texturing, rigging, collisions, LOD transitions and GPU performance were not validated.

For game production, split moving parts and preserve pivots, choose the coherent physical scale, author collision proxies, then measure the actual rendering target. A single connected static sculpture is not automatically a correct riggable character or vehicle.


Gen1 passed file checks but received later feedback about anatomy, overly regular forms and unsupported water. For new work needing those improvements, use [Gen2](gen2.md) and the relevant anatomy/organic/built method. Keeping these examples supports honest version comparison, not a claim that Gen1 is the current quality target.
