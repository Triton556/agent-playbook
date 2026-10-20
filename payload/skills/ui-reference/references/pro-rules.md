# Common Rules for Professional UI + Pre-Delivery Checklist

Use for applicable native/mobile presentation checks after the [targeted-search entrypoint](../SKILL.md#targeted-uiux-reference). Device/theme/state scope: see [UI design preflight, section 2](../../ui-design/references/design-preflight.md#2-link-screens-states-and-sizes).

Apply only to supported devices, themes and states recorded in that brief. Native examples below are conditional; web/desktop uses [quick-reference](quick-reference.md#quick-reference).

These are frequently overlooked issues that make UI look unprofessional.

## Icons & Visual Elements

| Rule | Standard | Avoid | Why It Matters |
|------|----------|--------|----------------|
| **No Emoji as Structural Icons** | Use vector-based icons (e.g., Lucide, react-native-vector-icons, @expo/vector-icons). | Using emojis (🎨 🚀 ⚙️) for navigation, settings, or system controls. | Emojis are font-dependent, inconsistent across platforms, and cannot be controlled via design tokens. |
| **Vector-Only Assets** | Use SVG or platform vector icons that scale cleanly and support theming. | Raster PNG icons that blur or pixelate. | Ensures scalability, crisp rendering, and dark/light mode adaptability. |
| **Contextual Semantics** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `icon-context`. | — | — |
| **Stable Interaction States** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `transform-performance`. | — | — |
| **Correct Brand Logos** | Use official brand assets and follow their usage guidelines (spacing, color, clear space). | Guessing logo paths, recoloring unofficially, or modifying proportions. | Prevents brand misuse and ensures legal/platform compliance. |
| **Consistent Icon Sizing** | Define icon sizes as design tokens (e.g., icon-sm, icon-md = 24pt, icon-lg). | Mixing arbitrary values like 20pt / 24pt / 28pt randomly. | Maintains rhythm and visual hierarchy across the interface. |
| **Stroke Consistency** | Use a consistent stroke width within the same visual layer (e.g., 1.5px or 2px). | Mixing thick and thin stroke styles arbitrarily. | Inconsistent strokes reduce perceived polish and cohesion. |
| **Filled vs Outline Discipline** | Use one icon style per hierarchy level. | Mixing filled and outline icons at the same hierarchy level. | Maintains semantic clarity and stylistic coherence. |
| **Touch Target Minimum** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `touch-target-size`. | — | — |
| **Icon Alignment** | Align icons to text baseline and maintain consistent padding. | Misaligned icons or inconsistent spacing around them. | Prevents subtle visual imbalance that reduces perceived quality. |
| **Icon Contrast** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `contrast-data`. | — | — |

## Interaction (App)

| Rule | Do | Don't |
|------|----|----- |
| **Tap feedback** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `tap-feedback-speed`, `press-feedback`. | — |
| **Animation timing** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `duration-timing`. | — |
| **Accessibility focus** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `keyboard-nav`, `icon-context`. | — |
| **Disabled state clarity** | Use disabled semantics (`disabled`/native disabled props), reduced emphasis, and no tap action | Controls that look tappable but do nothing |
| **Touch target minimum** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `touch-target-size`. | — |
| **Gesture conflict prevention** | Keep one primary gesture per region and avoid nested tap/drag conflicts | Overlapping gestures causing accidental actions |
| **Semantic native controls** | Prefer native interactive primitives (`Button`, `Pressable`, platform equivalents) with proper accessibility roles | Generic containers used as primary controls without semantics |

## Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|----|----- |
| **Surface readability (light)** | Keep cards/surfaces clearly separated from background with sufficient opacity/elevation | Overly transparent surfaces that blur hierarchy |
| **Text contrast (light)** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `color-contrast`. | — |
| **Text contrast (dark)** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `color-contrast`. | — |
| **Border and divider visibility** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `contrast-data`. | — |
| **State contrast parity** | See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `state-clarity`. | — |
| **Token-driven theming** | Use semantic color tokens mapped per theme across app surfaces/text/icons | Hardcoded per-screen hex values |
| **Scrim and modal legibility** | Measure the composed result and use a scrim strong enough to isolate foreground content | Reusing one opacity without checking the actual background |

## Layout & Spacing

| Rule | Do | Don't |
|------|----|----- |
| **Safe-area compliance** | Respect top/bottom safe areas for all fixed headers, tab bars, and CTA bars | Placing fixed UI under notch, status bar, or gesture area |
| **System bar clearance** | Add spacing for status/navigation bars and gesture home indicator | Let tappable content collide with OS chrome |
| **Consistent content width** | Keep predictable content width per device class (phone/tablet) | Mixing arbitrary widths between screens |
| **8dp spacing rhythm** | Use a consistent 4/8dp spacing system for padding/gaps/section spacing | Random spacing increments with no rhythm |
| **Readable text measure** | Keep long-form text readable on large devices (avoid edge-to-edge paragraphs on tablets) | Full-width long text that hurts readability |
| **Section spacing hierarchy** | Define clear vertical rhythm tiers (e.g., 16/24/32/48) by hierarchy | Similar UI levels with inconsistent spacing |
| **Adaptive gutters by breakpoint** | Increase horizontal insets on larger widths and in landscape | Same narrow gutter on all device sizes/orientations |
| **Scroll and fixed element coexistence** | Add bottom/top content insets so lists are not hidden behind fixed bars | Scroll content obscured by sticky headers/footers |

---

## Applicable presentation checklist

Use applicable items in the existing UI pass; shared behavior is referenced by rule ID below.
### Process
- [ ] Ran only searches relevant to the interface, such as `"keyboard focus modal" --domain ux` for modal keyboard behavior
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `keyboard-nav`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), coverage: see [UI design preflight, section 2](../../ui-design/references/design-preflight.md#2-link-screens-states-and-sizes).
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `reduced-motion` and `dynamic-type`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `color-contrast`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `touch-target-size`.
### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons come from a consistent icon family and style
- [ ] Official brand assets are used with correct proportions and clear space
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `transform-performance`.
- [ ] Semantic theme tokens are used consistently (no ad-hoc per-screen hardcoded colors)
### Interaction
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `press-feedback`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `touch-target-size`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `duration-timing`.
- [ ] Disabled states are visually clear and non-interactive
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `keyboard-nav`.
- [ ] Gesture regions avoid nested/conflicting interactions (tap/drag/back-swipe conflicts)
### Light/Dark Mode
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `color-contrast`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `contrast-data`.
- [ ] Modal/drawer scrim is measured against the real background and preserves foreground legibility
### Layout
- [ ] Safe areas are respected for headers, tab bars, and bottom CTA bars
- [ ] Scroll content is not hidden behind fixed/sticky bars
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), coverage: see [UI design preflight, section 2](../../ui-design/references/design-preflight.md#2-link-screens-states-and-sizes).
- [ ] Horizontal insets/gutters adapt correctly by device size and orientation
- [ ] 4/8dp spacing rhythm is maintained across component, section, and page levels
- [ ] Long-form text measure remains readable on larger devices (no edge-to-edge paragraphs)
### Accessibility
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `icon-context`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `input-labels`, `input-helper-text` and `error-placement`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `color-not-only`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `reduced-motion` and `dynamic-type`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `focus-not-obscured`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `dragging-alternative`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `accessible-authentication`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `auto-rotation-controls`.
- [ ] See [quick-reference, Quick Reference](quick-reference.md#quick-reference), rule IDs `error-summary`.
