# Accepted UI lessons

Apply to a new landing page or research dashboard according to the task, existing design system and accessibility. The UI route uses a scenario brief, linked states/sizes, mockup verification and implementation-to-basis comparison. Below are grounds and subject guidance, not a mandatory palette or composition template.

## Landing page: meaning and imagery throughout

After the hero, ensure the page develops its promise through understandable real-life episodes, reasons and a useful action. Name each important illustration's role: what it helps the viewer understand, feel or imagine in this particular section. Coordinate imagery/colors across the page; decorative expression does not replace substantive continuation. Assess the page's middle and CTA result alongside the first screen.

## Research dashboard: sequential explanation

Guide the reader from question and key comparison to a chart, short adjacent explanation and available details/sources. Check whether the conclusion and limits can be understood in that order without retaining all sections simultaneously. Remove competing emphasis, repetition and excessive density; preserve necessary comparisons, units, controls and qualifications. Judge concision by ease of reading and answer completeness, not card count.

A dense overview may be appropriate for operational monitoring requiring simultaneous comparison of many signals. Sequential presentation of research does not require hiding important data behind extra navigation.

## Research dashboard: accepted example (12 October 2026)

Task: audit the agent's skills, instructions and memory, and present the findings as an interactive dashboard with charts, not a dry wiki.

- **Rejected first version.** A topical catalog: system inventory, skill sizes, chat catalog, overlaps, journal, code checks. Feedback found it hard to read and its conclusion unclear. An earlier research dashboard with a mobile version also failed to explain the findings; the requested result was easy to understand, with charts and blocks to inspect and click.
- **Accepted version.** Human feedback accepted a version whose title is the reader's question and whose sections follow the reader's reasoning:
  1. Title: "Why the agent stops — and what to do about it".
  2. Current state: the path from request to answer, with two or three headline numbers.
  3. Problems as mechanisms: each complaint, its mechanism and the concrete place in the instructions.
  4. Changes: the concrete place and the expected change.
  5. The same task before and after: the current likely failure next to the behavior after the changes.
  6. Comparison with the other audit, the combined plan and the expected result.

How to apply it to an analysis, audit or research dashboard:

- Before choosing charts, write the one-sentence answer the reader should leave with, and list the sections as the questions the reader will ask in order: what is happening now, why, what to change, what will change.
- Each section opens with its conclusion; the chart or block proves it; details and sources come last.
- A catalog of components with filters, maps and matrices is reference material. Put it behind details or at the end; it is not the dashboard's structure.
- Desktop at the user's window size is the default viewing context. Add a mobile layout only when the task asks for it.
- Check a draft by first reading: from the title, the section headings and the first screen alone, can a fresh reader state the conclusion and the proposed changes? If not, restructure before adding more data.

Optional source evidence: `{{EVIDENCE_ROOT}}/codex-audit-comparison-20261012/index.html` (accepted), `sources/codex.html` (rejected first version) and `sources/harness.html` (comparison example). These private artifacts are not bundled; bind only an authorized evidence copy. Personal feedback quotations and conversation identifiers are omitted; the accepted reading sequence and its checks are retained.

## Illustrations: verify recognition

Include the actual important illustration in a styled preflight. Faces, poses and interactions must read in the accepted stylization and presentation size; inspect the finished UI using [visual-quality](../../product-ui-review/references/visual-quality.md). A style name and valid SVG do not establish recognition.

## Grounds and limits

In local UI A/B × Ultra/Medium comparisons on 15 October 2026, human feedback preferred B in all four comparisons. The Medium landing page stood out for imagery/colors; the Ultra landing page for meaning/imagery in its middle; the Ultra dashboard for explanations/sequential reading; and the Medium dashboard for concision, visual lightness and colors. Faces in both Ultra landing pages read as cyclopes; this feedback did not establish the technical cause. Personal and family details are omitted.

Medium was preferred to Ultra in this viewing. This is a local observation, not grounds to automatically change model or effort level. One run does not prove the workflow's causal effect; the human preference for B suffices for the adopted product decision. Historical agent preferences remain separate.

Original feedback/materials: `{{EVIDENCE_ROOT}}/ui-preflight-ab-20261015/HUMAN-REVIEW.md`; installation/checks: `{{EVIDENCE_ROOT}}/ui-preflight-adoption-20261015`.
