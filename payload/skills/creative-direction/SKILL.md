---
name: creative-direction
description: Find and choose a creative direction before building. Use when the task asks to come up with, propose or pick an idea, concept or direction - a new interface or a redesign direction, a game idea or mechanic, a video, essay or content concept, angle or structure, a motion, visual or 3D concept - or when the user shares things they like and asks what could be made from them. Skip for small refinements and when an accepted direction or creative brief already exists.
---

# Creative direction

The most likely idea is the most ordinary one. Left alone, an agent proposes the first plausible concept, copies the surface of whatever the user said they like, and polishes that single option. This skill replaces that with a short search: understand what should be felt, generate widely, keep a few genuinely different directions, show them concretely, let the user choose.

The user may bring a direction from Claude or from their own work. If a creative brief or an accepted direction already exists, it is the basis: execute and refine it, do not regenerate alternatives unless asked.

Separate two kinds of input. **Things the user likes from others** (a game, a film, a product) are references: extract the principle and do not copy their surface. User material: see [task brief and acceptance, section 2](../dev-flow/references/task-brief-and-acceptance.md#2-understand-the-intent). In addition to that preservation rule, raise a creative risk once with a solution inside the user’s idea. Domain guidance: [UI/UX](references/ui-ux.md), [content](references/content.md), [game design](references/gamedev.md), [visual, motion and 3D](references/visual.md). Open the one that matches the deliverable; a mixed task opens each.

## 1. Find the principle, not the surface

When the user names things they like (a game, a film, a product, a past result), ask what experience or quality they give the user and why. Write it as a principle in plain words: what the person feels, does or understands. Then name the surface you will not copy: the reference's setting, signature mechanic, layout or style.

Example: "I loved the map in a metroidvania" can mean "earning orientation in a hostile place" or "the pleasure of seeing a blank area fill in". Neither requires a map screen. A direction that rebuilds the same map system is a reskin, not an idea.

If the principle is unclear, ask about a concrete memory ("which moment made you want to continue?") rather than offering an abstract either/or.

## 2. Diverge before choosing

Write 15–20 raw ideas, one line each, in a few minutes. Vary them along the axes listed in the domain reference, so they differ in structure and not only in theme or color. Then list what a typical agent would propose for this request and mark those ideas as obvious. Keep an obvious idea only when it clearly serves the principle better than the rest, and say so.

## 3. Shape three different directions

Pick three directions that differ from each other in how they work, not in decoration. For each, write:

- **The moment:** one concrete scene from the user's, player's or viewer's side - what they see, do and feel. Avoid lists of features or mechanics.
- **Why it fits:** which part of the principle it delivers.
- **What makes it distinct:** what would be lost if it were swapped for one of the others.
- **Cost and risk:** effort, the main thing that could make it fail.

Recommend one with its main tradeoff, but keep all three visible.

## 4. Make taste concrete

Taste is easier to see in reactions to examples than in answers to questions. Find 4–6 real references (products, screens, games, frames, articles) relevant to the directions, and ask the user what attracts or repels them in each. Use available browser, image search or image generation; if none is available, describe the references precisely and link them. Record the user's reactions as observable features ("dense tables with one bold number", "no glossy gradients"), not adjectives.

## 5. Sketch before building

When the choice is visual or experiential, make the cheapest sketch per direction before any full build: a wireframe in existing components, a style frame, a 30-second script, a paragraph of play. Sketches are for choosing, not polishing; label them as such.

## 6. Hand over a creative brief

After the user chooses (or delegates the choice), save a short creative brief in the existing plan and continue with the execution skill for the domain:

- Goal and audience, in the user's words.
- Principle and the surface not to copy.
- Chosen direction as its moment; what must survive into the final result.
- References with the user's reactions; constraints (design system, brand, platform, budget, scope).
- What not to do; open questions.

The brief is the same whether Codex, Claude or the user wrote it. Later stages check the result against it.

## Self-check before showing directions

- Is any direction a reskin of a named reference?
- Would most agents have proposed it first? If yes, is it kept for a stated reason?
- Do the three directions differ in structure, not just in theme, color or wording?
- Is each one described as a concrete moment someone experiences?
- Did taste come from the user's reactions to examples, not from your defaults?
- Preservation: see task brief and acceptance, section 2.
