# Connect Jam Board MCP

Use this only to guide a missing connection. The following configuration/command section is copied verbatim from the app's `docs/mcp.md` (v2.1 contract), including placeholder paths and tokens. For Codex, these entries belong in `~/.codex/config.toml`. Let the user choose stdio or HTTP. Do not edit global client configuration or install/build anything unless explicitly authorized. Do not run these commands merely because this reference was loaded.

### Codex: stdio (installed application)

```toml
[mcp_servers.jam-board]
command = "C:\\Users\\<you>\\AppData\\Local\\Jam Board\\jam-board-mcp.exe"
env = { JAM_AGENT_NAME = "Codex" }
```

### Codex: HTTP (desktop must be open)

```toml
[mcp_servers.jam-board-http]
url = "http://127.0.0.1:47321/mcp"
bearer_token_env_var = "JAM_BOARD_TOKEN"
http_headers = { "X-Jam-Agent" = "Codex" }
```

Set `JAM_BOARD_TOKEN` in the environment inherited by the client to the token copied explicitly from Settings ? MCP. Do not commit the token. `bearer_token_env_var` and `http_headers` are supported by the [official Codex MCP configuration documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

### Claude Code: stdio

```powershell
claude mcp add jam-board --env JAM_AGENT_NAME=Claude -- '<path-to-installed-jam-board-mcp.exe>'
```

### Claude Code: HTTP

```powershell
claude mcp add --transport http jam-board http://127.0.0.1:47321/mcp --header "Authorization: Bearer <token>" --header "X-Jam-Agent: Claude"
```

The name-before-`--env` stdio form and HTTP header form follow the [official Claude Code MCP guide](https://code.claude.com/docs/en/mcp). Replace `<token>` locally; if the default port is occupied, use the actual port stored in `settings.mcp_http_port`. These are instructions for the user, not commands that this implementation runs against real agent configuration.

Replace the executable path with the absolute path shown in Settings ? MCP. TOML does not expand %LOCALAPPDATA%; the example is a placeholder, not a literal path to paste unchanged. Installed stdio needs no data override. For development, add JAM_BOARD_DATA_DIR pointing at <checkout>/.dev-data. The default data folder is %APPDATA%\dev.triton556.jamboard.

## Confirm the connection

After the user configures the chosen transport, reload/restart the client session as needed and inspect its connected tools. Call the Jam Board `get_board` tool with `{}`. A successful structured board response confirms access to that project; verify its identity before mutations. If tools are absent, report the missing connection and show the relevant example above. If a tool returns an error, report its actual code/message; do not claim success.

For stdio, use the executable path displayed in the application's MCP settings and the intended database. Development database lookup is `--db <path>` (file), then `JAM_BOARD_DB`, then `JAM_BOARD_DATA_DIR/jam.db`, then `%APPDATA%/dev.triton556.jamboard/jam.db`. Do not use `--seed-demo` for normal work: it creates a new demo project. Installed stdio normally needs no data override. HTTP requires the desktop open and the actual configured port/token. Never copy a token into a brief, report, committed file or tool output.

Return to the [skill](../SKILL.md) once connected. The skill is maintained in [agent-playbook](https://github.com/Triton556/agent-playbook); the application is [Jam Board](https://github.com/Triton556/jam-board).
