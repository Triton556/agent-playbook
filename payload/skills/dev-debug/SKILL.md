---
name: dev-debug
description: Diagnose and fix observed software failures, regressions, crashes, build errors, flaky tests, or performance symptoms. Use when behavior is wrong or a check fails and the cause needs evidence. A request for new behavior starts with implementation; aesthetic redesign starts with ui-design.
---

# Diagnose and fix bugs

Start with the exact symptom: expected and actual behavior, inputs, environment, version and available output. For a nontrivial or recurring failure, read [diagnosing-bugs](vendor/matt-pocock/diagnosing-bugs/INSTRUCTIONS.md); local rules replace its mandatory external interviews and agent procedures.

1. Obtain a reproducible signal: test, HTTP request, CLI fixture, browser scenario or measurement. Preserve the original result, removing secrets. Minimize the example when that accelerates diagnosis. For flaky/performance bugs, record conditions, frequency and baseline measurement.
2. Rank hypotheses using the evidence. Find and test an observation that distinguishes likely causes. Change one material variable per iteration. The symptom and risk determine the investigation's scale.
3. Repair/recheck transition: see [WORKFLOW, step 6](../../workflow/WORKFLOW.md#work-route). For significant recurring regressions add protection through dev-verify.
4. Distinguish environment failures from application defects. Further iterations: see WORKFLOW, step 6.

When dynamic reproduction is unavailable, perform useful static analysis and label hypotheses and unperformed checks. Request only the minimum missing signal/access; continue independent parts.

Deliver an evidenced cause and verification or a precise blocker with eliminated hypotheses. Action scope: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries). Check visual changes through [ui-review](../ui-review/SKILL.md).

Source revision and license: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
