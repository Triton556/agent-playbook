# Meaningful worlds and inhabited scenes

Use when creating or revising a narrative, personal-memory or inhabited spatial world, or when individually valid assets fail to form a coherent place. A single object, ordinary chart or small material experiment stays on its existing branch. A static diorama can use the composition steps without adding inhabitants or animation.

## 1. Define what belongs together

Recover the intended experience and the accepted baseline through the [shared perception protocol](../../dev-flow/references/human-perspective-review.md). Name the places, relationships and actions that must survive the revision; account for relevant follow-up discussions before choosing new assets.

Separate the roles in this particular world. A territory may hold a stable theme; a place holds a scene; a scene contains actors, props and activity; a source record supplies a fact or story. These are useful distinctions, not a required storage schema. Several records may share one workshop, and one personal episode may connect several places. Choose the few focal landmarks by meaning; fill the remaining places only where their role is clear.

Keep three kinds of state explicit:

- **Evidence:** dated facts, sources, project status and what remains unknown.
- **Artistic scene:** fictional residents, daily activity, weather and authored transitions.
- **Runtime:** loading, selection, playback, camera and actual live events if the product has them.

A paused historical project can coexist with an inhabited village. An artistic ride need not report a real trip. If a visual channel represents telemetry, define its encoding using [data and spatial metaphors](data-spatial-metaphors.md). Otherwise identify it as illustration and let the scene serve its artistic purpose. Personal atmosphere comes from the author's choice or dated account, not an inference about their mood or worth from activity counts.

**Exit:** each focal scene has an intended reading, a reason to be here and an observable action or static relationship; factual claims and artistic choices are distinguishable.

## 2. Plan places, circulation and visibility

Lay out terrain and large thematic masses, then destinations and their connections. Give a door, quay, garden, workshop or resting place an approach consistent with its purpose. Use a simple path graph or authored routes when that is sufficient; a decorative atlas does not require a general physics engine.

Reserve the spaces that can conflict:

| Space | Check |
| --- | --- |
| Solid/support | Foundations, trunks, feet and terrain make intended contacts; incompatible solids remain separate |
| Action and sweep | A moving arm, rotor, vehicle or carried prop has clearance and intended contact throughout the relevant cycle |
| Circulation | The route reaches its destination, fits its actor and respects the rendered ground, shore and height changes |
| View | The focal object and consequence remain visible from the intended camera after panels and labels occupy their area |
| Organic group | Canopies may overlap intentionally; density, species and gaps support the local place rather than a universal spacing rule |

These spaces can have different shapes. A tree's supported root does not describe its crown or its effect on a camera. AABB overlap is a candidate for diagnosis, not a collision verdict. Label intended contacts and inspect the relevant geometry before claiming a physical cause.

**Exit:** the scene can be explained as a usable place, with named allowed contacts and the important routes/views protected.

## 3. Prove a whole scene before a kit or world-sized batch

Block one representative scene and the important boundary case with simple masses and the real UI rectangle. Include its main subject, surrounding place, source of meaning and required activity. For animation, establish actor → target → action → visible consequence → next state, including rest where appropriate. A moving scene needs a temporal prototype; a static scene needs a clear arrangement of relationships.

Observe the scene at the intended distance before adding detailed assets. The prototype succeeds when the intended place/action is readable and the main interaction reaches a visible result and recovery. A model sheet or isolated animation does not cover their integration. Resolve a failing reading at this stage, then scale the pattern to distinct places without turning every scene into a clone.

Select or adapt assets to the proven roles. Reusing a model is appropriate when it preserves the subject's identity; changes of context, scale or purpose trigger [reference grounding](../../dev-flow/references/reference-grounding.md). New voxel focal forms use the applicable [voxel design preflight](../../voxel-models/references/design-preflight.md). Preserve detailed masters while judging the actual scene representation at its normal distance.

**Exit:** an integrated representative works; each reused family has a known purpose and boundary of applicability.

## 4. Make life legible in time

Choose activity because it belongs to the place: arrival, tending, fetching, exchange, inspection, play or rest. Set routes, targets, contacts and transitions before motion polish. A convincing idle scene can be quiet; neither constant movement nor a fixed number of inhabitants is required.

Keep atmosphere and activity separately inspectable. Wind, water, smoke and birds can support the place, while residents and user-triggered actions carry other meanings. Match the amplitude, pace and contrast to the ordinary view. Verify that declared motion changes the rendered result rather than only an internal clock. When local weather is useful, share the relevant local wind across dependent effects and retain a coherent global sun; keep the weather's meaning explicit.

Test the full intended cycle and its important transitions at normal speed, then pause/resume and the applicable reduced-motion state. Check routes against the final ground and moving clearance, not only the starting pose. Record the observed interval and state. Separated screenshots support positional changes; continuous rhythm or smoothness requires actual playback observation.

**Exit:** the intended activity or quiet state reads in its place, remains honest about evidence, and survives playback controls.

## 5. Inspect discovery and retain the right evidence

Start from the ordinary entry view, discover the focal scene, act, inspect the consequence and return. Let labels clarify identities while geometry and activity explain the place. An exact technical project name may require text; an obscured scene cannot be repaired by a correct label alone.

At the target viewport and normal camera, inspect the actual free rectangle with the panel open. Let camera movement settle. Check foreground occlusion, hierarchy and the subject's usable screen size. Use a close-up to diagnose, then return to the intended view to judge the repair. UI control checks follow the installed product UI workflow.

Use the shared protocol's property-specific verdicts. Pair a bounded geometry check with a view of its visual consequence; record unavailable modalities as unverified. Replay the accepted baseline's protected experiences in the new revision and retain the improvements introduced by the new one. Stop when the substantial criteria pass; further work needs a remaining defect or a new scoped request.

**Exit:** discovery, reading, use and preservation have current evidence at their actual scope. Source correctness, scene integration and human acceptance retain separate status.

## Transfer example and limits

Memory world V2 preserved a blue car model but removed its ride, animated scenery around static residents, and opened a selected garden behind dominant crowns. The useful transfer is to protect actions/relationships and inspect a whole scene in time, not to mandate cars, villagers, sparse trees or voxel art elsewhere. Dense forest, deliberate stillness and unusual architecture remain valid when they serve the accepted intent.

Local evidence directory: `{{EVIDENCE_ROOT}}/memory-biomes-voxel-2.1-20261014/audit/`. Read the comparison audit in that authorized evidence copy for this regression; ordinary use needs only the relevant lesson. Installing this reference proves availability, not improved outcomes on a future artifact.
