# Writing an adapter

Write an adapter when the user wants a client without one as a worker: OpenCode, a DeepSeek harness, Aider, a client running GLM or Kimi models, or a custom agent. The result is one script, `adapters/<agent>.mjs`, that satisfies the [contract](contract.md). Start from `adapters/claude-code.mjs` (a CLI that streams JSON) or `adapters/codex.mjs` (a JSON-RPC server); both are short.

Tell the user before you start that this is new code which runs another agent on their machine, and get their agreement for the live checks at the end.

## 1. Find out how the client runs headless

Read the client's own help and documentation. Do not guess flags. You need answers to:

- **One turn without a person.** A print or run mode (`-p`, `run`, `exec`), a local server with an API, or an SDK.
- **The session ID.** Where it appears in the output, or whether you can set it yourself on start.
- **Continuing.** How to send the next turn to the same session (`--resume <id>`, an API call with the session ID).
- **The final answer.** Which event or field holds it, and how errors are reported. Some clients report failures, such as a missing login, as an ordinary answer.
- **Restrictions.** What the client can enforce: an OS sandbox, permission modes, allowed-tool lists, or nothing.
- **Approvals.** How to make anything that would ask a person fail instead of waiting forever.
- **Visibility.** Whether sessions started this way appear where the user works: the app, a session list, a web UI.
- **Login and settings.** Whether a separate start uses the user's own login and settings.

## 2. Map the access modes honestly

For each of `read-only`, `workspace-write`, `danger-full-access`, decide which client setting gives it, and write in `--describe` what that setting really enforces. If the client cannot stop file writes, it has no `read-only`. Leave the mode out, and the adapter refuses it with exit code 4. A weaker mode under the stronger name is worse than no mode: the user chooses based on it.

## 3. Implement

- Parse the contract's options; reject unknown access modes and missing folders with exit code 4 before starting anything.
- Find the executable: an environment variable (`<AGENT>_BIN`), then PATH, then the client's usual install locations.
- Start the client in `--cwd` with the brief on stdin or in a file. Do not put the brief on the command line, where length limits and quoting break it.
- Stream events to `--log`, show commands and tool calls as short stderr lines, collect the final answer.
- Decline every approval request and question. Never auto-approve.
- Print the result JSON as the last stdout line and use the contract's exit codes. A failed start that created no session is exit code 3.
- If the orchestrator itself may be a session of the same client, check for environment variables that make the child think it is nested, and clear them.

## 4. Check it live

Run these on a tiny task in an empty test folder, with the user's agreement:

1. `--describe` prints valid JSON, and an unknown `--sandbox` value exits with 4.
2. A new session completes the task. Check the file yourself, not the answer.
3. `--thread <id>` continues the same session: the worker remembers the first turn, and the change lands in the same place.
4. Each access mode you claim behaves as described: `read-only` refuses to write a file, and `workspace-write` cannot write outside `--cwd` if you claim that.
5. The user confirms the session is visible where `visible_in` says.

Record which checks passed, and on which client version, in the adapter's header comment. A check you did not run is not a check that passed.
