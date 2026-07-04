# Codex Hooks

## Agent completion notifications

`agent_done_notify.py` sends a compact notification when a Codex `Stop` or
`SubagentStop` hook fires. The script reads Codex hook JSON from stdin and
derives the active project from the hook `cwd`, so it works even when installed
as a symlink from this repo into a different project's Codex session.

The alert includes:

- hook event (`Stop` or `SubagentStop`)
- project/repository name
- branch and short commit
- dirty tracked/untracked file count
- session cwd relative to the repository root
- host name
- model and permission mode
- short session and turn ids
- subagent type/id for `SubagentStop`
- final assistant/subagent message excerpt
- UTC timestamp

Install the script:

```bash
./install.sh --feature agent-notifications
```

Add the hook registration from `~/.codex/hooks/agent_done_hooks.example.json`
to your global `~/.codex/hooks.json`, or merge the two event entries into an
existing global hooks file. Review and trust the hook with `/hooks` in Codex.

Configure one backend with environment variables. Do not commit tokens or
topics if they identify a private notification channel.

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
