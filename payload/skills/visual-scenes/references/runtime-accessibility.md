# Runtime and accessibility

## Budget the complete result

Choose a target viewport/device and an acceptable response/frame budget. Measure simulation, main render, reflection/shadow passes, post-processing and DOM work separately and together where instrumentation permits. RAF callback frequency, file/build success and voxel/quad counts do not prove full-frame throughput. GPU timing requires appropriate tools and interpretation; CPU submission time is not GPU completion time.

Capture dimensions, device/browser, pixel ratio, scene count, effects and model state with a performance result. Avoid comparing a warm steady state to compilation/loading. Include input responsiveness and a costly interaction, not just idle.

Use a pixel budget: a starting estimate is `dpr ≤ sqrt(maxPixels/(cssWidth*cssHeight))`, capped by device and quality needs. Degrade the least explanatory features first: decorative density, reflection/update rate, expensive blur, shadow/postprocess resolution. Keep essential paths, selected object, labels and numbers. Use hysteresis and recovery; relative FPS alone can miss an initially slow device.

Separate model-dirty and view-dirty work. Recompute a model only on relevant input; render on demand if nothing moves. Pause background animation while hidden, clamp resumed delta time, and dispose of observers/listeners/GPU resources when the surface leaves. If WebGL fails, provide an explicit fallback diagram or readable explanation and controls rather than a black frame.

## Responsive composition

Target device/theme scope: see [design-preflight, 2. Link screens, states and sizes](../../ui-design/references/design-preflight.md#2-link-screens-states-and-sizes).

Measure the free drawing rectangle after controls and safe areas. Fit essential geometry to it, then inspect. Move secondary details into a disclosure or stack them below the scene. A smaller screen often needs a different camera or layout, not a scaled desktop HUD. Verify short viewports as well as narrow ones.

Labels and overlays have a joint budget. Give measurements and interaction targets priority over promotions or ambient annotations. Avoid fixed bottom panels covering sliders or legal/source information. Preserve page zoom and native vertical scrolling unless a gesture is deliberately scoped to the scene.

## Input and accessibility

Shared controls: see [accessible interaction checks](../../ui-design/references/accessibility.md), input-labels, keyboard-nav, focus-states and icon-context. In addition to those rules, custom sliders expose units and min/max/current values with arrows and Home/End under the [WAI slider pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider/); a role alone does not implement behavior.

In addition to [accessible interaction checks](../../ui-design/references/accessibility.md), keyboard-nav and dragging-alternative, canvas picking needs a semantic control path for important objects, stable names/descriptions, visible selection and discoverable instructions.

Reduced motion/rotation: see [accessible interaction checks](../../ui-design/references/accessibility.md), reduced-motion and auto-rotation-controls. In addition, start with a stable readable state and make scene pause stop all intended animation sources; cuts/manual playback preserve the scientific/data consequence. Announce committed summaries rather than every frame.

Contrast and redundant channels: see [accessible interaction checks](../../ui-design/references/accessibility.md), color-not-only, color-contrast and contrast-data. In addition, inspect thin colored rays at actual resolution and use real assistive technology when required by acceptance.

Official implementation references: [Three.js color management](https://threejs.org/manual/pages/color-management.html), [Three.js responsive design](https://threejs.org/manual/pages/responsive.html), [WAI keyboard interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/). Check the project's installed library version before adopting APIs.
