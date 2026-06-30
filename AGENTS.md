## Project-specific local instructions

When working in `/home/alacasse/projects/graphify`, first use Codex's normal project instruction discovery, including the repo's committed `/home/alacasse/projects/graphify/AGENTS.md`. Then read `/home/alacasse/projects/graphify/my-docs/AGENTS.md` before doing project work.

Treat `my-docs/AGENTS.md` as a local additive overlay, not a replacement for the committed repo `AGENTS.md`. If the two files conflict, prefer the local `my-docs/AGENTS.md` only for personal workflow/configuration details; prefer the committed repo `AGENTS.md` for upstream project rules unless the user explicitly says otherwise. The `my-docs/` directory is intentionally ignored and should not be committed.

## GitHub issues and comments

When creating or updating GitHub issues, PR comments, or issue comments, keep the GitHub body compact and actionable. Use GitHub for the decision-oriented core: summary, why, proposed direction, acceptance criteria, and links or paths to detailed design artifacts.

Do not put long design documents, large schema sketches, long logs, or giant Markdown dumps directly into GitHub issue/comment bodies. If the design is substantial, create or update a repo-owned planning/reference document and link or name that file from the issue instead. Prefer short follow-up comments for addenda.

## Reusable workflow ownership

Repo-owned skills are reusable workflow code. Do not hard-code a single project's name, paths, validation commands, cache locations, issue policy, or local planning layout into a generic skill. If a workflow needs project-specific behavior, put those values in that project's instructions, local overlay, active spec, or a repo-owned reference document, then make the skill resolve them or stop when they are missing.

## Codex config ownership

When editing a path under `~/.codex`, first check whether it is linked from `/home/alacasse/src/codex-config`:

```bash
/home/alacasse/src/codex-config/scripts/codex_owner.py <path>
```

If the script reports `owner: codex-config`, treat the edit as work in `/home/alacasse/src/codex-config` even when the current task is happening in another project. Read `/home/alacasse/src/codex-config/.codex/AGENTS.md`, make the change through the linked file or the repo file, update `/home/alacasse/src/codex-config/CHANGELOG.md` for meaningful workflow or behavior changes, and report that repo's git status before finishing.

Vendor-owned or unmanaged `~/.codex` paths should not be copied into `/home/alacasse/src/codex-config` unless explicitly asked.
