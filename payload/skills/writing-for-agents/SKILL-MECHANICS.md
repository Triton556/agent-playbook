# Skill mechanics in local Codex

Keep a precise description that identifies the task and the branches that should load the skill. Keep detailed references out of the always-loaded pointer. Pick implicit invocation only when the skill should be reached automatically for that task.

Codex expresses explicit-only invocation in `agents/openai.yaml` with `policy.allow_implicit_invocation: false`. This local adaptation removes upstream Claude `disable-model-invocation`/`argument-hint` fields from installed frontmatter. Do not assume Codex removes descriptions from context or that a Claude Skill tool exists. An explicitly selected router may direct the agent to read the relevant installed dependency files.

Avoid building a new router or loading all skills unless the user actually needs it. Split distinct stages when useful and preserve the shared writing principles in [SKILL.md](SKILL.md).
