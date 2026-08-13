# codex-config Development Instructions

This repository owns the source-controlled part of the user's Codex
configuration. Keep it small, reviewable, and independent from Codex's native
planner and child-agent runtime.

## Native runtime boundary

- Do not introduce a repository-owned planner, scheduler, worker/reviewer loop,
  task ledger, or transient agent-result protocol.

## Reusable configuration

- Treat `skills/`, `agents/`, hooks, and installer metadata as
  production configuration.
- Keep reusable skills project-neutral. Resolve project paths, commands, issue
  policy, and local document placement from the target project's instructions.
- Repository exploration must work with normal reads and search. Optional
  indexing tools may help when explicitly enabled, but must not become semantic
  authority or a portability requirement.
- Do not commit secrets, auth files, runtime databases, logs, sessions, caches,
  or generated installation homes.
- Update `CHANGELOG.md` for meaningful behavior changes.

## Installer and ownership development

Use the repository source when developing or testing ownership inspection:

```bash
./scripts/codex_owner.py <path>
```

Never run this repository's installer against the active Codex home during
tests; use `--codex-home` with an isolated temporary directory.

## Repository configuration

- Issues are tracked in GitHub; see `docs/agents/issue-tracker.md`.
- Use the five-label triage vocabulary in `docs/agents/triage-labels.md`.
