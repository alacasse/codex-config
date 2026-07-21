# Personal Codex Operating Instructions

This repository owns the source-controlled part of the user's Codex
configuration. Keep it small, reviewable, and independent from Codex's native
planner and child-agent runtime.

## GitHub issues and comments

Keep GitHub bodies compact and actionable: summary, why, proposed direction,
acceptance criteria, and links to detailed repository documents. Do not paste
large designs, schemas, logs, or Markdown dumps into issue or pull-request
comments.

## Native orchestration

- Use native Codex plans and native child-agent orchestration for task-internal
  work.
- Delegate when it improves implementation, review, exploration, or context
  management; keep each child prompt bounded.
- Do not introduce a repository-owned planner, scheduler, worker/reviewer loop,
  task ledger, or transient agent-result protocol.

## Reusable configuration

- Treat `skills/`, `agents/`, `rules/`, hooks, and installer metadata as
  production configuration.
- Keep reusable skills project-neutral. Resolve project paths, commands, issue
  policy, and local document placement from the target project's instructions.
- Repository exploration must work with normal reads and search. Optional
  indexing tools may help when explicitly enabled, but must not become semantic
  authority or a portability requirement.
- Do not commit secrets, auth files, runtime databases, logs, sessions, caches,
  or generated installation homes.
- Update `CHANGELOG.md` for meaningful behavior changes.

## Codex configuration ownership

Before editing a path under `~/.codex`, inspect it with:

```bash
/home/alacasse/src/codex-config/scripts/codex_owner.py <path>
```

If it reports `owner: codex-config`, edit the repository source, not the linked
runtime path. Never run this repository's installer against the active Codex
home during tests; use `--codex-home` with an isolated temporary directory.

## Repository configuration

- Issues are tracked in GitHub; see `docs/agents/issue-tracker.md`.
- Use the five-label triage vocabulary in `docs/agents/triage-labels.md`.
