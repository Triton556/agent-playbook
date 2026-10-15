# Runtime and accessibility

## Budget the complete result

Choose a target viewport/device and an acceptable response/frame budget. Measure simulation, main render, reflection/shadow passes, post-processing and DOM work separately and together where instrumentation permits. RAF callback frequency is not proof of full-frame throughput. GPU timing requires appropriate tools and interpretation; CPU submission time is not GPU completion time.

Capture dimensions, device/browser, pixel ratio, scene count, effects and model state with a performance result. Avoid comparing a warm steady state to compilation/loading. Include input responsiveness and a costly interaction, not just idle.

Use a pixel budget: a starting estimate is `dpr ≤ sqrt(maxPixels/(cssWidth*cssHeight))`, capped by device and quality needs. Degrade the least explanatory features first: decorative density, reflection/update rate, expensive blur, shadow/postprocess resolution. Keep essential paths, selected object, labels and numbers. Use hysteresis and recovery; relative FPS alone can miss an initially slow device.

Separate model-dirty and view-dirty work. Recompute a model only on relevant input; render on demand if nothing moves. Pause background animation while hidden, clamp resumed delta time, and dispose of observers/listeners/GPU resources when the surface leaves. If WebGL fails, provide an explicit fallback diagram or readable explanation and controls rather than a black frame.

## Responsive composition

Set the target devices from the brief. Desktop work can require resizing and browser zoom without requiring a separate mobile design. The rules below apply to the sizes the product actually supports; do not turn a desktop task into a mobile redesign.

Measure the free drawing rectangle after controls and safe areas. Fit essential geometry to it, then inspect. Move secondary details into a disclosure or stack them below the scene. A smaller screen often needs a different camera or layout, not a scaled desktop HUD. Verify short viewports as well as narrow ones.

Labels and overlays have a joint budget. Give measurements and interaction targets priority over promotions or ambient annotations. Avoid fixed bottom panels covering sliders or legal/source information. Preserve page zoom and native vertical scrolling unless a gesture is deliberately scoped to the scene.

## Input and accessibility

Use native labeled buttons, range inputs, selects and text readouts when possible. Keep units in accessible value text. Custom sliders need arrows, Home/End, visible focus and exposed min/max/current values; follow the [WAI slider pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider/). A role alone does not implement keyboard behavior.

Canvas picking needs an equivalent semantic control path for important objects. Give interactive objects stable names and descriptions. Keyboard events should respect text fields and normal browser shortcuts. Direct manipulation needs a visible selected state and a discoverable instruction.

Honor `prefers-reduced-motion` by starting with a stable readable state, replacing camera tours with cuts and offering manual playback. Pause should stop all intended animation sources, not just the camera. Preserve the scientific/data consequence when removing motion. Announce committed result changes as useful summaries, not a stream every animation frame.

Use shape, labels or line style alongside color. Small thin colored rays require sufficient contrast at the actual resolution. Validate with keyboard and real assistive technology when such support is part of acceptance; a DOM check alone is not full accessibility certification.

Official implementation references: [Three.js color management](https://threejs.org/manual/pages/color-management.html), [Three.js responsive design](https://threejs.org/manual/pages/responsive.html), [WAI keyboard interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/). Check the project's installed library version before adopting APIs.
