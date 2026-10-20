# Setup interview

Question procedure: see [requirements-interview, Delegation-specific additions](../../agent-sessions/references/requirements-interview.md#delegation-specific-additions); language: see [AGENTS, Goal, communication and boundaries]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries).

## Before asking: find the clients

Check what is available on this machine and say what you found. These checks start no sessions and change nothing, so run them without asking:

- `node <agent-sessions>/adapters/<agent>.mjs --describe` for every adapter in `agent-sessions/adapters/`: whether it is verified, its effort levels and access modes.
- Whether each client's command exists (`codex`, `claude`, and any client the user names).

## Round 1

**Q1 - Clients and models:** "I found: <list with verified / unverified>. Which clients and models do you want to use? You can also name others, for example 'z.ai GLM 5.3' or 'DeepSeek harness'."
➡️ Recommended: the verified clients you found, with the models the user already uses.

**Q2 - Routing:** "How should I decide which model gets which task?
- Auto: I choose for each session; you see and can change it in the approval table.
- Rules: you tell me once which task types go to which model; I follow that, and choose myself for anything the rules do not cover.
- Ask each time: I ask you for every session in the approval table."
➡️ Recommended: Rules if the user mentioned preferences such as "math to Astra"; otherwise Auto.

**Q3 - What I do myself:** "By default I do requirements, splitting, briefs, checking and integration, plus small fixes; everything else goes to sessions. Change that?"
➡️ Recommended: the default.

## Round 2 (only what applies)

**Q4 - Routing table** (only in Rules mode): show the table of task types from [the profile format](brain-profile.md), filled with your proposal based on the user's answers so far. The user corrects only what they want different. A one-line answer such as "math and research to astra, reviews to glm, the rest sol" is enough: fill the table from it and show it.
➡️ Recommended: your filled table.

**Q5 - Clients without an adapter** (only if the user named one): "<client> has no verified adapter yet. Write and check one now on a tiny task, or leave it out for now?"
➡️ Recommended: leave it out until it is needed, unless the routing table sends tasks to it.

**Q6 - Scope:** "Apply these choices to all future sessions, or only to the current task? If all: for every project, or only this one?"
➡️ Recommended: all future sessions, for every project; a project can override later.

## Finish

Show the resulting profile card and save only explicitly settled setup choices at the location chosen in Q6. Playback and unresolved decisions follow [task brief and acceptance, sections 3–4](../../dev-flow/references/task-brief-and-acceptance.md#3-ask-only-what-changes-the-work); session launch follows agent-sessions, step 5.

## Notes on specific clients

- **Codex:** adapter `codex`, sessions visible in the Codex app. Driver operation: see [agent-sessions-codex, step 6](../../agent-sessions-codex/SKILL.md#6-run-and-check).
- **Claude Code:** adapter `claude-code`, headless sessions; needs a CLI that is logged in on its own.
- **z.ai GLM and similar API providers:** they usually run inside an existing coding client (for example Claude Code pointed at the provider's API) rather than as a separate program. Find out from the user how they run it; it may need an adapter variant with its own settings. Not checked yet: treat it as unverified.
- **DeepSeek harness and other CLIs:** adapter readiness follows [agent-sessions, step 2](../../agent-sessions/SKILL.md#2-split-the-work).
