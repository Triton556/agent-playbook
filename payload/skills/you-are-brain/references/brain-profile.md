# Brain profile

A profile records reusable choices, not execution history or permissions. Read it for first setup of a task; restore a continuing task from its own record, including task-only overrides.

## Where profiles live

- Global: `~/.agent-playbook/brain-profile.md`, only when the user selected reuse across projects on this machine.
- Project: `.agent-playbook/brain-profile.md`, only when the user selected this project. Keep the file outside publication using the project's ignored local storage.
- Task-only: the existing task record; no permanent profile file.

Read global then project; a project section replaces the same global section. The current user's task instruction overrides the corresponding saved choice. Store no keys, tokens or credentials.

## Format

```markdown
# Brain profile
Updated: <YYYY-MM-DD>

## Execution
Route: native | adapter:<name>
Host: <client>
Allowed clients/models: <actual user selections>
Effort: <explicit level or delegated choice>
Access: <authorized mode; actual enforcement checked at launch>

## Routing
Mode: Auto | Rules | Ask

| Task type | Client / route | Model |
| --- | --- | --- |
| <type> | <selected client/route> | <selected model> |
| Anything else | <explicit fallback, if selected> | <model or Auto> |

## Brain does itself
- <selected responsibilities>

## Notes
- <task-relevant user choices>
```

The table is used only in Rules mode. Keep available model names and supported settings tied to the actual host/adapter, not fictional defaults from an example.

## Routing modes

- **Rules:** match the task type, then its explicit fallback. Without a match or fallback, ask for that choice.
- **Auto:** choose within the clients/models and cost/access scope delegated by the user.
- **Ask:** obtain the user's model selection before launching that assignment; reuse an answer that explicitly covers several workers.

A mixed task can use its main type or be split into independent outputs. Record the choice; splitting is not mandatory merely because a UI task includes tests.

## Current task state

Record route, host, selected model/effort/access, worker/run/thread IDs, briefs, latest reports and pending questions in the existing task record. A saved profile does not prove a worker is running. A continuation keeps the same IDs and assignment unless the user changes the scope or the runtime reports that the worker cannot continue.

External adapter capability checks and launch: [session guide](../../agent-sessions/references/session-guide.md). Native status and continuation use the selected host's tools.
