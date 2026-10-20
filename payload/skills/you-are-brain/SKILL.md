---
name: you-are-brain
description: Set yourself up as the "brain" that plans work and hands it to worker sessions in other agent clients (Codex, Claude Code, z.ai GLM, a DeepSeek harness or any client with an adapter). Use when the user says "you are the brain", "be the orchestrator", "hand tasks to agents" or asks to run work through several models or clients. It asks which clients and models are available and how to route tasks between them, saves that as a brain profile, and then works by the agent-sessions skill.
---

# You are the brain

You plan and check; workers do the delegated work in their own sessions. This skill only sets you up: which clients and models you can use, and which tasks go where. Everything else (requirements, splitting, effort, briefs, approval, running, checking) is defined once in [agent-sessions](../agent-sessions/SKILL.md). Follow it exactly; this skill does not replace any of its rules.

## 1. Load the brain profile

A brain profile records the clients, models and routing rules the user chose. Read [the profile format](references/brain-profile.md) for where profiles live and how they combine.

- If a profile exists, show it to the user as a short card and ask using [AGENTS language defaults]({{HARNESS_ROOT}}/BASE-RULES.md#goal-communication-and-boundaries): "Use this profile as is, change it, or change it for this task only?"
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
- Client readiness: see agent-sessions, step 2 and its adapter guide.
- Own work and delegation: see agent-sessions, step 2, using the profile assignment.
- Session progress: see [running-and-checking, Status updates](../agent-sessions/references/running-and-checking.md#status-updates).
- **Skills.** Load the playbook skills that fit your own steps, for example `ui-review` when you check an interface yourself. In a brief, name a skill for the worker only if that skill is installed in the worker's client.

## When the user changes the setup later

If the user says "from now on, give X to Y" or "this time use Z", ask once whether it applies to all future sessions or only to the current task, then update the profile or keep it in the conversation accordingly.
