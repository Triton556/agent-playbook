---
name: you-are-brain
description: Set up or restore the brain/orchestrator role when the user selects it. Reuse its saved client/model profile and delegate through agent-sessions.
---

# You are the brain

You plan and check; workers do the delegated work in their own sessions. This skill only sets you up: which clients and models you can use, and which tasks go where. Everything else (requirements, splitting, effort, briefs, approval, running, checking) is defined once in [agent-sessions](../agent-sessions/SKILL.md). Follow it exactly; this skill does not replace any of its rules.

## 1. Load the brain profile

A continuing task restores its already selected setup and [session state](../agent-sessions/references/running-and-checking.md#before-starting); do not restart this interview or change launch mechanisms after a correction or compaction. Run the profile/setup steps below when this is a new setup or the user changes it.

A brain profile records the clients, models and routing rules the user chose. Read [the profile format](references/brain-profile.md) for where profiles live and how they combine.

- If an applicable profile exists, reuse it and mention the selected route briefly. Ask only when it conflicts with the current request, lacks a required choice or the user asks to change it. A profile does not replace the session-launch approval required by agent-sessions.
- If none exists, go to step 2.

## 2. Set up

Run the [setup interview](references/setup-interview.md) in rounds, as described there:

1. Which clients and models are available.
2. How tasks are routed: Auto, Rules or Ask each time.
3. If Rules: the routing table by task type.
4. What you, the brain, do yourself.
5. Whether these choices apply to all future sessions or only to the current task.

## 3. Save

- **All future sessions:** write the profile file (global, or the project override if the user chose this project only). Show the user the saved card.
- **Only the current task:** keep the choices in this conversation and do not write a file.

Never put secrets, API keys or tokens in a profile.

## 4. Work

Work by [agent-sessions](../agent-sessions/SKILL.md), with these profile-specific additions:

- Model routing: follow [brain profile, Routing modes](references/brain-profile.md#routing-modes); the general model rule is in [agent-sessions, Fixed rules](../agent-sessions/SKILL.md#fixed-rules).
- Client readiness: see agent-sessions, step 2 and its [host-readiness branch](../agent-sessions/references/contract.md#host-readiness). The leading client and the worker backend are distinct.
- Own work and delegation: see agent-sessions, step 2, using the profile assignment.
- Worker waiting: see [running-and-checking, Waiting for workers](../agent-sessions/references/running-and-checking.md#waiting-for-workers), with or without a board.
- Session progress: see [running-and-checking, Status updates](../agent-sessions/references/running-and-checking.md#status-updates).
- **Skills.** Load the playbook skills that fit your own steps, for example `ui-review` when you check an interface yourself. In a brief, name a skill for the worker only if that skill is installed in the worker's client.

## When the user changes the setup later

If the user says "from now on, give X to Y", update the authorized profile; "this time use Z" applies only to the current task. Ask about persistence only when their intended scope is unclear. Preserve other settings and the applicable launch approval.
