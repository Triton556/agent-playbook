# Landing pages: gpt-taste adaptation

Use for landing, promotional, campaign and marketing pages, including refinement/redesign. It does not apply to dashboards/settings/editors. Original: [gpt-taste](../vendor/gpt-taste/INSTRUCTIONS.md); below is the current local adaptation.

1. Choose hero composition by product, content and goal: centered, asymmetric, editorial split or another suitable option. Briefly compare two options when the first is an obvious familiar template. Prompt length and random seed are not design criteria.
2. Use AIDA as optional sequencing of attention, interest, trust and action. Sections, CTAs, pricing and navigation appear only when the actual offer needs them; fixed structure and mandatory “exactly two CTAs” were removed.
3. Set headline width/scale for readable, coherent composition at target sizes. Check wrapping in the render; `max-w-*` does not guarantee line count. Russian text and mobile may need a different composition.
4. Make the grid meaningful and balanced. Bento is optional. `grid-auto-flow: dense` is acceptable when visual order matches reading and keyboard navigation. Whitespace can be intentional; hidden overflow does not fix a layout error.
5. Add an expressive motion when it improves the story or action. GSAP/pinning/scrubbing are optional; check existing dependencies, reduced motion, target devices, cleanup and effect cost. A high-quality static page is valid.
6. Choose actual appropriate images/illustrations or authorized generation. A `picsum` seed does not imply thematic relevance. Check each important asset’s content/loading; reuse rights: see [reference-grounding, How to investigate](../../dev-flow/references/reference-grounding.md#how-to-investigate). Do not invent customer logos, testimonials or metrics.
7. Preserve an accepted brand when refining an existing landing page. For an agreed redesign, update the system across the scoped surface. Do not mandate new fonts, dark theme, gradients or huge vertical spacing.

Before delivery, check the first visible area, offer/CTA clarity, whole-page rhythm, text/button readability, target sizes and link/form behavior through [ui-review](../../ui-review/SKILL.md). No mock Python logs, invented execution or mathematical “guarantee” without actual verification.
