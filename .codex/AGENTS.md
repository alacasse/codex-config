# Codex Config Repository Instructions

This repository defines the user's personal Codex configuration.

## Rules

- Treat `skills/`, `agents/`, `rules/`, and `AGENTS.md` as production workflow code.
- Keep repo-owned skills reusable. Do not add single-project branches or hard-code one project's paths, validation commands, cache locations, issue policy, or planning layout into a generic skill; resolve those values from project instructions, local overlays, active specs, or repo-owned reference docs instead.
- Do not edit runtime Codex state from this repository.
- Never add secrets, auth files, SQLite databases, logs, sessions, cache files, or machine-local runtime state.
- Update `CHANGELOG.md` for every meaningful workflow change.
- The changelog should explain the problem, decision, and expected effect.
- Prefer small commits focused on one workflow responsibility.
- Preserve compatibility with the live `~/.codex` layout unless explicitly changing the install/sync process.
- `codex-features.json` lists only features owned by this repository. Vendor-owned skills, rules, agents, and runtime state should not be added here.
- Repo-owned features must install as symlinks so editing the corresponding `~/.codex` path edits this repository.
- If changing a skill, include a short note about how the change affects agent behavior.
- If changing an agent, include a short note about the role boundary.
