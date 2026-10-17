---
name: product-debugging
description: Diagnose and fix observed software failures, regressions, crashes, build errors, flaky tests, or performance symptoms. Use when behavior is wrong or a check fails and the cause needs evidence. A request for new behavior starts with implementation; aesthetic redesign starts with product-ui-design.
---

# Diagnose and fix bugs

Start with the exact symptom: expected and actual behavior, inputs, environment, version and available output. For a nontrivial or recurring failure, read [diagnosing-bugs](vendor/matt-pocock/diagnosing-bugs/INSTRUCTIONS.md); local rules replace its mandatory external interviews and agent procedures.

1. Obtain a reproducible signal: test, HTTP request, CLI fixture, browser scenario or measurement. Preserve the original result, removing secrets. Minimize the example when that accelerates diagnosis. For flaky/performance bugs, record conditions, frequency and baseline measurement.
2. Rank hypotheses using the evidence. Find and test an observation that distinguishes likely causes. Change one material variable per iteration. The symptom and risk determine the investigation's scale.
3. Fix the confirmed cause within scope. Check the original scenario with the same input, then nearby affected cases. When a significant regression could recur, add targeted protection through [product-testing](../product-testing/SKILL.md).
4. If a hypothesis is rejected, preserve the result and choose the next justified route. Do not repeat an action without a new hypothesis or changed conditions. Distinguish environment failures from application defects.

When dynamic reproduction is unavailable, perform useful static analysis and label hypotheses and unperformed checks. Request only the minimum missing signal/access; continue independent parts.

Deliver an evidenced cause, fix and check of the original symptom, or a precise external blocker with eliminated hypotheses. A diagnosis-only request does not authorize implementation. Also check visual changes through [product-ui-review](../product-ui-review/SKILL.md).

Source revision and license: [sources.json](sources.json), [LICENSE](licenses/mattpocock--skills-LICENSE).
