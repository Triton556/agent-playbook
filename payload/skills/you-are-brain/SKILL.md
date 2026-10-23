---
name: you-are-brain
description: Coordinate a user-selected task or project through worker agents. Restore the saved route and assignments; set up a profile only when choices are missing or changed.
---

# You are the brain

Own the task breakdown, worker briefs, integration and acceptance. Use the user's current scope and saved choices; a profile or a skill does not grant tool access. Native agents and external CLI adapters are different execution routes, not interchangeable names.

## Event routes

| Event | Action | Observable output / next step |
| --- | --- | --- |
| Continuing a task or recovering context | Read its existing task record: route, model choices, worker IDs, pending questions and last results. Inspect each pending worker with that route's status tool. | Continue the same worker or consume its completed result; no setup interview and no replacement worker solely because context was compacted. |
| First task with an applicable saved profile | Read [brain profile](references/brain-profile.md); apply current task overrides. | Selected route, routing mode and brain/worker responsibilities are recorded in the task. Resolve only a missing choice that blocks the next launch. |
| First setup, or the user changes client/model/route | Use [setup questions](references/setup-interview.md) for the specific missing choices. | A task-only configuration, or a profile saved in the scope the user selected. |
| User authorizes work on a task or project | Identify deliverables, dependencies and checks. Do tightly coupled work yourself; assign independent deliverables to workers under the authorized route and model choices. | Briefs and a worker/status table in the existing task record. Covered worker launches do not require a new approval ceremony. |
| Preparing the first worker brief or changing its scope/audience | Read [brief writing](../agent-sessions/references/brief-writing.md). Assign concrete output, permitted files/actions, acceptance scenario and report recipient. | A brief the worker can execute without the original conversation; external adapters also receive the checked assignment. |
| Launching a native worker | Use the host's available native launch tool and supported settings. Record the returned ID and the actual model/settings it exposes. | A native worker ID; continue/status/wait through the same host tools. Do not load external-adapter commands for this route. |
| Launching or resuming an external CLI worker | Read [session guide](../agent-sessions/references/session-guide.md), then the named client's command reference. | Actual run/thread ID and settings, or a reported startup blocker; a requested launch is not a running worker. |
| Worker reports completion | Inspect the delivered changes and reported observations against its acceptance scenario. For UI, verify the changed user steps and reached states. | Accept/integrate, or return the specific failed step and expected result to the same worker. A test count or exit code alone is not acceptance. |
| Requested action exceeds assigned scope, model routing, access or cost authorization | State the concrete new choice and ask before that action; continue independent covered work. | User decision recorded without expanding permissions from a profile or worker report. |
| Agreed outputs and their checks are complete | Report the result, executed checks, remaining limitations and unresolved questions. | Finished task; additional work requires a new change, failed scenario or named unresolved criterion. |

## Model routing and recovery

Rules uses the saved table and its explicit fallback; Auto delegates selection within the allowed clients/models; Ask waits for the user's selection. If a Rules table has no match or fallback, ask rather than invent one. Preserve the selected mechanism across continuation; changing native ↔ adapter route is a concrete setup change, not an automatic recovery action.

Load a reference for the event named in the table, not merely because another file links to it. Keep run records and reports in the existing local task record; report actual progress when a worker starts, blocks or returns. A separate independent reviewer remains a separately selected role, not an automatic extra worker.
