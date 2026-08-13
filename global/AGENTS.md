# Personal Codex Operating Instructions

## GitHub issues and comments

Keep GitHub bodies compact and actionable: summary, why, proposed direction,
acceptance criteria, and links to detailed repository documents. Do not paste
large designs, schemas, logs, or Markdown dumps into issue or pull-request
comments.

## Git commit attribution

When Codex materially contributes to a commit, append
`Co-authored-by: Codex <codex@openai.com>` exactly once.

## Native orchestration

- Use native Codex plans and native child-agent orchestration for task-internal
  work.
- Delegate when it improves implementation, review, exploration, or context
  management; keep each child prompt bounded.

## Codex configuration ownership

Before editing a path under the active Codex home, inspect it with the
`bin/codex-owner` executable from that same Codex home. For the default home:

```bash
~/.codex/bin/codex-owner <path>
```

When `CODEX_HOME` is set, use its `bin/codex-owner` instead. If the command
reports `owner: codex-config`, edit the reported repository source rather than
the installed runtime path.
