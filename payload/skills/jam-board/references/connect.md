# Connect Jam Board MCP

Use this only to guide a missing connection. The following configuration/command section is copied with repository-relative links resolved from the app's `docs/mcp.md` (source commit cf2e8fd03d5753a9ea316c9408e6da9f74f0cbc7, checked 2026-10-22), including placeholder paths and tokens. For Codex, these entries belong in `~/.codex/config.toml`. Let the user choose stdio or HTTP. Do not edit global client configuration or install/build anything unless explicitly authorized. Do not run these commands merely because this reference was loaded.

### Codex: stdio (installed application)

```toml
[mcp_servers.jam-board]
command = "C:\\Users\\<you>\\AppData\\Local\\Jam Board\\jam-board-mcp.exe"
env = { JAM_AGENT_NAME = "Codex", JAM_BOARD_PROJECT = "<project-id>" }
```

### Codex: HTTP (desktop must be open)

```toml
[mcp_servers.jam-board-http]
url = "http://127.0.0.1:47321/mcp"
bearer_token_env_var = "JAM_BOARD_TOKEN"
http_headers = { "X-Jam-Agent" = "Codex", "X-Jam-Project" = "<project-id>" }
```

Set `JAM_BOARD_TOKEN` in the environment inherited by the client to the token copied explicitly from Settings → Agents. Do not commit the token. `bearer_token_env_var` and `http_headers` are supported by the [official Codex MCP configuration documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

### Claude Code: stdio

```powershell
claude mcp add jam-board --env JAM_AGENT_NAME=Claude --env JAM_BOARD_PROJECT=<project-id> -- '<path-to-installed-jam-board-mcp.exe>'
```

### Claude Code: HTTP

```powershell
claude mcp add --transport http jam-board http://127.0.0.1:47321/mcp --header "Authorization: Bearer <token>" --header "X-Jam-Agent: Claude" --header "X-Jam-Project: <project-id>"
```

The name-before-`--env` stdio form and HTTP header form follow the [official Claude Code MCP guide](https://code.claude.com/docs/en/mcp). Replace `<token>` locally; if the default port is occupied, use the actual port stored in `settings.mcp_http_port`. These are instructions for the user, not commands that this implementation runs against real agent configuration.

Replace the executable path with the absolute path shown in Settings → Agents. TOML does not expand %LOCALAPPDATA%; the example is a placeholder, not a literal path to paste unchanged. Installed stdio needs no data override. For development, add JAM_BOARD_DATA_DIR pointing at <checkout>/.dev-data. The default data folder is %APPDATA%\dev.triton556.jamboard.

### Connect, appoint, then authorize

1. Choose the intended project in **Projects**, then open **Settings → Agents**.
   Its displayed name and key identify the configuration you are about to copy.
2. Choose one transport, apply the configuration in your agent client yourself,
   and restart/reconnect that session. Snippets share a connection name: replace
   the old entry intentionally, or keep different boards in separate client
   configurations/sessions; do not paste duplicate TOML entries.
3. Copy the project's read-only check. It calls `get_session_context` first and
   verifies the exact project ID/key prefix before `get_project`/`get_board`.
   Copying a prompt or configuration is not proof that a connection succeeded.
4. In **Plan**, open an epic and choose its **Brain**. The connected agent appears
   after its first board call. Appoint it separately for each epic it coordinates.
   When there is no epic yet, draft one with the agent first. An agent may use
   `become_brain` for an unassigned epic only after the human appoints it; it must
   not overwrite another brain's appointment.
5. Prepare a planning prompt; refine questions, stories and tasks together. Brain
   appointment, Active plan status and Ready tasks do not grant execution. Start
   the chosen Story/Epic explicitly in Plan, or approve the brain's typed Inbox
   request. The board never launches an operating-system agent process for you.

Switching the app's board only changes the UI; existing MCP sessions remain pinned.
To connect another project, repeat steps 1–3 with that project's configuration.
After a version upgrade, refresh cached tools and reread task/report evidence before
new actions. Never repair a rejected stale payload by silently filling new tokens.

The [optional playbook compatibility note](https://github.com/Triton556/jam-board/blob/cf2e8fd03d5753a9ea316c9408e6da9f74f0cbc7/docs/agent-playbook-compatibility.md) separates
workflow instructions from this version's calling contract. Installing that skill
is not required for MCP, does not configure the connection, and cannot certify that
older examples match the live tool schemas.

After the user configures the chosen transport, reload/restart the client session as needed and inspect its connected tools. Call the Jam Board `get_board` tool with `{}`. A successful structured board response confirms access to that project; verify its identity before mutations. If tools are absent, report the missing connection and show the relevant example above. If a tool returns an error, report its actual code/message; do not claim success.

For stdio, use the executable path displayed in the application's MCP settings and the intended database. Development database lookup is `--db <path>` (file), then `JAM_BOARD_DB`, then `JAM_BOARD_DATA_DIR/jam.db`, then `%APPDATA%/dev.triton556.jamboard/jam.db`. Do not use `--seed-demo` for normal work: it creates a new demo project. Installed stdio normally needs no data override. HTTP requires the desktop open and the actual configured port/token. Never copy a token into a brief, report, committed file or tool output.

Return to the [skill](../SKILL.md) once connected. The skill is maintained in [agent-playbook](https://github.com/Triton556/agent-playbook); the application is [Jam Board](https://github.com/Triton556/jam-board).
