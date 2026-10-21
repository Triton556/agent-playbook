# Brain profile

A brain profile is a short Markdown file with the user's choices: which clients and models exist, how tasks are routed, and what the brain does itself.

A profile is not the execution log. Keep the current task's selected adapter route, host-readiness evidence, run/thread IDs and assignment references in its existing task basis/session log, including task-only choices. Restore that state on continuation; absence of a permanent profile does not cancel a task's explicit choices. Profile files never grant permissions or establish current host readiness.

## Where profiles live

- **Global:** `~/.agent-playbook/brain-profile.md`, for all projects on this machine.
- **Project override:** `.agent-playbook/brain-profile.md` in the project root, for one project. Make sure the folder is ignored by git (add it to `.gitignore`, or to `.git/info/exclude` if the user does not want `.gitignore` changed). Never commit or publish a profile.

When both exist, read the global one first, then apply the project file on top: a section present in the project file replaces the same section of the global one; sections it does not have stay global.

## Format

```markdown
# Brain profile

Updated: <YYYY-MM-DD>

## Clients
| Client | Adapter | Verified | Models |
|--------|---------|----------|--------|
| codex | codex | yes | gpt-6.1-sol, gpt-6-astra |
| claude-code | claude-code | no | <models> |
| <other> | none | no | <models> |

## Routing
Mode: Auto | Rules | Ask

| Task type | Client | Model |
|-----------|--------|-------|
| Requirements and planning | brain | - |
| Math, formulas, algorithms | codex | gpt-6-astra |
| Code implementation | codex | gpt-6.1-sol |
| UI and design system | codex | gpt-6.1-sol |
| Design review | <client> | <model> |
| Code review | <client> | <model> |
| Tests and QA | codex | gpt-6.1-sol |
| Writing and documentation | codex | gpt-6.1-sol |
| Research | codex | gpt-6-astra |
| Anything else | Auto | Auto |

## Brain does itself
- Requirements, splitting, briefs, checking results, integration, small fixes.

## Notes
- <anything the user added, for example "never send client code to <client>">
```

The routing table is filled only in Rules mode. In Auto and Ask modes, keep the `Mode:` line and leave the table out.

## Routing modes

The `Mode:` line decides who picks the client and model for each session:

- **Rules:** take them from the routing table. For a task type the table does not cover, use the "Anything else" row.
- **Auto:** choose them yourself among the clients and models listed in the profile.
- **Ask:** do not choose; leave the model cell as a question in the approval summary and wait for the user's answer.

In every mode the approval summary shows the client and model of each session, and the user can change them there before anything starts.

## Reading the routing table

- Match the task to the closest task type. If a task spans two types (a UI feature with its own tests), split it into two sessions or use the type of its main part, and say which in the approval summary.
- "Anything else" covers task types not in the table.
- "brain" as the client means you do that work yourself.
- Adapter readiness: see [agent-sessions, step 2](../../agent-sessions/SKILL.md#2-split-the-work).
