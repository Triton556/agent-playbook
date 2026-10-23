# Implementation

| Input event | Action | Observable output |
| --- | --- | --- |
| A software change has an agreed behavior | Read its existing code/contracts and uncommitted changes; connect the required layers | The requested operation produces the expected result with real logic/data; identify any demonstration stub |
| The change touches a human-facing flow | Execute the changed user steps, including opened surfaces and state transitions | Step-by-step user-flow observations, not implementation-derived assertions |
| An architectural or public-contract choice is unresolved | Use [dev-plan](../SKILL.md) for that decision | A resolved choice before implementing dependent code |
| Execution contradicts the contract | Use [dev-debug](../../dev-debug/SKILL.md) with the observed failure | Reproduced cause and repair |
| Code is ready for technical verification | Use [dev-verify](../../dev-verify/SKILL.md) | Independent contract expectations checked; limitations stated |

Reuse existing components and boundaries. A shared abstraction needs an actual shared use, not a speculative future feature. Complete the agreed scenario before widening scope. A unit test, build or hash is not evidence that a person can complete the UI flow.
