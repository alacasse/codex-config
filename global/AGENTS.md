# Personal Codex Operating Instructions

## GitHub issues and comments

Keep GitHub bodies compact and actionable: summary, why, proposed direction,
acceptance criteria, and links to detailed repository documents. Do not paste
large designs, schemas, logs, or Markdown dumps into issue or pull-request
comments.

## Git commit attribution

When Codex materially contributes to a commit, append
`Co-authored-by: Codex <codex@openai.com>` exactly once.

## Project documentation

For questions about project status, plans, decisions, or architecture, resolve a
single documentation root before answering. Use the non-empty value of
`git config --local --get codex.docs-root` when it names an existing
repository-relative directory whose resolved path stays within the repository;
otherwise use `docs`. If the selected root contains `AGENTS.md`, read it as the
index for that documentation workstream and follow its pointers for the
question. This selection adds documentation context; the normal Codex
instruction chain continues to govern repository work.

## Codex configuration ownership

Before editing a path under the active Codex home, inspect it with the
`bin/codex-owner` executable from that same Codex home. For the default home:

```bash
~/.codex/bin/codex-owner <path>
```

When `CODEX_HOME` is set, use its `bin/codex-owner` instead. If the command
reports `owner: codex-config`, edit the reported repository source rather than
the installed runtime path. Before editing that source, read and follow the
applicable instructions in its repository.
