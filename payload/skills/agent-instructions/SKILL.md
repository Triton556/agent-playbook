---
name: agent-instructions
description: Edit agent-facing instructions and their routing. Use when a rule, skill instruction or workflow document is being changed.
---

# Writing instructions for agents

## Edit the existing instruction

| Change requested or found | Action | Check before finishing |
| --- | --- | --- |
| Change a rule's behavior | Locate its existing owner and write the requested outcome plus the event that triggers it | The text distinguishes a real triggering case from a case that should continue unchanged |
| Two files prescribe the same behavior or disagree | Choose one owner; replace other copies with a pointer naming when to open it | Callers agree with the owner; removing a copy does not reintroduce it through a mandatory reading chain |
| Move or remove an instruction | Find its incoming links and catalog/installation callers, then update them together | Destinations and anchors resolve; removed entrypoints are not still selected by profiles |
| A procedure says only “as needed”, “enough” or “do it well” | Name the input event, action and observable result, or remove the sentence if it adds no decision | The next action can be selected from an actual request, change, failure or unresolved choice |
| Create/package a new native skill | Use the selected client's available skill-creator for metadata and packaging | The client can discover the skill; prose review is not another separate authoring cycle |
| Executable behavior changes | Run the affected operation and its failure/preservation cases | Report what ran and what did not; file hashes alone do not prove behavior |
| Compare two workflows is explicitly requested | Read [workflow-pilot](../dev-flow/references/workflow-pilot.md) | Comparable inputs and measured outcomes; do not start a model experiment just to edit prose |

Keep agent-facing instructions in English unless the user requests a different language. A past example or defect does not automatically become a universal rule. Preserve the user's named invariants and actual scope; do not invent a new approval gate while shortening text.

## Pointers and authority

An entrypoint states which request selects it and which output it produces. A reference pointer names its triggering question or operation. Keep one owner for each meaning, with its exceptions beside it; put domain detail in the corresponding reference. Do not copy commands or client capabilities that can be inspected directly into several guides.

[WORKFLOW](../../workflow/WORKFLOW.md) holds the short event-to-action route. A specialist supplies its domain method rather than copying that route. When a link, rule or executable changes, check that changed surface; unrelated references are not required reading.
