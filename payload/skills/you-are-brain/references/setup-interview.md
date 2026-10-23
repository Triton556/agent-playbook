# Setup interview

Open when no applicable task/profile choice exists, or the user changes it. On continuation, restore the task record instead. Ask only the row whose answer is missing; an existing answer is not an invitation to repeat the interview.

| Missing choice / event | Inspect or ask | Record |
| --- | --- | --- |
| Execution route is unset | Inspect the host's declared native agent tools. If the user requests a CLI/client, inspect that adapter with `node <agent-sessions>/adapters/<agent>.mjs --describe` and check the named CLI exists. Explain the actual available routes, then resolve the user's route choice. | `native` or the named external adapter; host and supported settings. No worker is started by this inspection. |
| Worker model selection is unset | Ask for models and Rules, Auto or Ask routing. | Explicit selections, or delegated selection within named clients/models. |
| Rules has an unmatched task type | Use its agreed fallback; if none exists, ask what should handle that task type. | The selected row or fallback. Do not silently turn Rules into Auto. |
| Responsibility split is unset | Propose brain: breakdown, briefs, integration and acceptance; workers: assigned deliverables. Let the user change that split. | Brain/worker responsibilities. |
| An external adapter is unverified or absent | State the missing capability/evidence. Offer to leave that client out or prepare a separately authorized adapter/check. | The agreed choice; do not launch a paid model probe as part of setup by default. |
| Persistence scope is unset | Keep choices for this task. Ask about saving only when the user requests future reuse but the project/global scope is unclear. | Task record, or the explicitly selected profile location. |

Show the resulting choices and any unresolved launch blocker. User authorization to start a task or project covers its worker assignments within those choices; it does not cover new providers, access, costs or work outside that scope. Native permissions and adapter readiness are separate from profile preferences.

Profile layout and override rules: [brain profile](brain-profile.md). External execution: [session guide](../../agent-sessions/references/session-guide.md).
