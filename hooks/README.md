# Codex Hooks

## Agent completion notifications

`agent_done_notify.py` sends a compact notification when the principal Codex
agent finishes a turn and the `Stop` hook fires. The script reads Codex hook
JSON from stdin and derives the active project from the hook `cwd`, so it works
even when installed as a symlink from this repo into a different project's Codex
session.

The alert includes:

- hook event (`Stop`)
- project/repository name
- branch and short commit
- dirty tracked/untracked file count
- session cwd relative to the repository root
- host name
- model and permission mode
- short session and turn ids
- final assistant message excerpt
- UTC timestamp

Install the script:

```bash
./install.sh --feature agent-notifications
```

This feature installs `~/.codex/hooks.json` as a symlink to the repo-owned
`hooks/agent_done_hooks.json`. Review and trust the hook with `/hooks` in
Codex after installing.

If you already have an unmanaged `~/.codex/hooks.json`, the installer stops
instead of overwriting it. In that case, merge the event entries from
`~/.codex/hooks/agent_done_hooks.example.json` into the existing file.

Configure one backend with environment variables. Do not commit tokens or
topics if they identify a private notification channel.

You can also use an untracked local config file at
`~/.codex/agent-notifications.json`. Environment variables override config file
values.

```json
{
  "ntfy_topic": "codex-long-random-private-topic",
  "ntfy_server": "https://ntfy.sh",
  "priority": "default"
}
```

### ntfy

```bash
export CODEX_AGENT_NOTIFY_NTFY_TOPIC="codex-$(openssl rand -hex 12)"
```

Subscribe to the same topic in the ntfy mobile app. For a self-hosted or Pro
server:

```bash
export CODEX_AGENT_NOTIFY_NTFY_SERVER="https://ntfy.example.com"
export CODEX_AGENT_NOTIFY_NTFY_TOKEN="tk_..."
```

You can also set the full URL directly:

```bash
export CODEX_AGENT_NOTIFY_NTFY_URL="https://ntfy.sh/my-random-topic"
```

### Pushover

```bash
export CODEX_AGENT_NOTIFY_PUSHOVER_TOKEN="app-token"
export CODEX_AGENT_NOTIFY_PUSHOVER_USER="user-key"
```

### Apprise

Install `apprise`, then provide any supported Apprise target URL:

```bash
export CODEX_AGENT_NOTIFY_APPRISE_URL="pover://user-key@app-token"
```

Optional:

```bash
export CODEX_AGENT_NOTIFY_PRIORITY="default"
export CODEX_AGENT_NOTIFY_LOG="/tmp/codex-agent-notify.log"
```
