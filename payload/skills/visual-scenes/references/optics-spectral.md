# Optics and spectral graphics

Use this branch when light behavior is the subject. A decorative glass UI does not need an optical solver.

## Separate the paths

Maintain distinct concerns: physical or geometric solver, apparatus geometry, observer camera, result/sensor image, display appearance. Synchronize them through causal inputs and a result revision. A camera image blurred from a depth map is not a multi-surface lens trace; describe the chosen approximation.

For a geometric trace, retain wavelength, medium, surface/element IDs, segment endpoints, direction, power, event type and termination reason. Snell refraction, total internal reflection and Fresnel branching must use consistent normals, medium transitions and units. Test normal incidence, near-tangent intersections, the critical-angle boundary and bounded energy accounting. A thin-lens approximation has a different validity range from tracing curved surfaces.

## Draw light without changing the measurement

Build ray geometry from the trace. Keep display gains, minimum pixel width, halo, saturation and exposure outside the solver. A bright beam is an illustration of its path, not evidence of physically correct radiance. Show a narrow core and a restrained halo where appropriate; select blending for the background.

Spectrum ribbons need compatible paths. Join adjacent wavelength samples only while their surface/event topology matches; split the ribbon when rays leave through different faces or reflect internally. Avoid inventing a colored surface between unrelated endpoints. Compute detector readings from the same hits; record missed and terminated rays explicitly.

Use bounded sample/branch counts, small-energy cutoffs and loop handling. Report truncation rather than calling an incomplete trace converged. During interaction, use a cheaper preview and refine the newest revision after release. A changed solver resolution must not silently change the meaning of a measurement.

## Thin films and spectral appearance

Thin-film color depends on optical thickness and viewing geometry; use a spectral-to-display mapping for that subject, with its assumed index, illumination and integration convention. An expensive appearance function may become a sampled lookup texture; compare interpolation error at difficult regions and choose resolution for the needed fidelity.

Do not add interference rainbows to an ordinary lens merely because they are attractive. Fresnel edge reflections, volume thickness and environment cues usually explain transparent geometry better. Gamma/color-space errors can change apparent brightness and color without any solver change; follow the installed rendering library's color workflow.

References and status: [Plane of Focus](https://sael.net/plane-of-focus/), [Prism Room](https://sael.net/prism-room/), [Soap Bubble](https://sael.net/soap-bubble/), [Prismatic](https://sael.net/prismatic/). Detailed implementation observations in the earlier KB are historical source reviews; current live observations and their limits are in [Evidence](evidence.md). The optical safeguards above are original engineering recommendations and require independent validation in the new application.
