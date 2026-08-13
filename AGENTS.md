# codex-config Development Instructions

This repository owns the source-controlled configuration installed into the
user's Codex environment. Its production surfaces are global instructions,
reusable skills and agents, hooks, the manifest-driven installer, ownership
tooling, and repository-local tracker adapters. Keep them small and reviewable.

This repository configures Codex. It does not implement a task-execution
runtime.

## Repository-owned configuration

- Treat `global/AGENTS.md`, `skills/`, `agents/`, hooks, installer metadata,
  ownership tooling, and tracker adapters as production configuration.
- Keep reusable skills project-neutral. Resolve project paths, commands, issue
  policy, and local document placement from the target project's instructions.
- Repository exploration must work with normal reads and search. Optional
  indexes may help, but must not become semantic authority or a portability
  requirement.
- Keep `codex-features.json` limited to features owned by this repository;
  vendor-owned skills, agents, and runtime state do not belong in the manifest.
- Do not commit secrets, auth files, runtime databases, logs, sessions, caches,
  or generated installation homes.
- For meaningful behavior changes, update `CHANGELOG.md` with the problem,
  decision, and expected effect.

## Installer and ownership development

Manifest-managed targets must be symlinks to their declared repository sources.
Installer changes must preserve safe upgrades, conflict handling, dry runs,
pruning, and installed-state accuracy.

Use the repository source when developing or testing ownership inspection:

```bash
./scripts/codex_owner.py <path>
```

Never run this repository's installer against the active Codex home during
tests; use `--codex-home` with an isolated temporary directory.

## Repository configuration

- Issues are tracked in GitHub; see `docs/agents/issue-tracker.md`.
- Use the five-label triage vocabulary in `docs/agents/triage-labels.md`.
- Verify required tracker labels with `scripts/setup_github_labels.py`; applying
  missing labels changes external state and requires explicit approval.
