---
name: batch-runway
description: Create and execute multi-slice runway specs with per-slice scope, validation, ledger updates, commits, and mandatory coding/review subagent delegation. Use when the user asks to create a batch runway spec, execute a runway spec, streamline sequential slices, work from my-docs/plans, commit after each slice, or keep the main agent as coordinator only while subagents implement and review.
---

# Batch Runway

Use this skill for a controlled sequence of small, independently committable slices.

Modes:

- `create-spec`: write a runway spec for a future execution session.
- `execute-spec`: execute an existing runway spec one slice at a time.

Spec density modes:

- `full-runway`: maximum explicitness. Specs may include full contracts, full commands, and full subagent briefs.
- `lean-runway`: token-efficient. Specs reference standard contracts, validation profiles, and compact subagent briefs.

Default to `lean-runway` for mechanical refactors, test topology splits, import cleanup, docs-local planning, compatibility facade cleanup, and behavior-preserving module moves.

Default to `full-runway` for production behavior changes, installer lifecycle changes, YAML schema changes, sandbox execution behavior, public CLI behavior, risky migrations, or ambiguous ownership boundaries.

If the user does not name a mode, infer it from the request. "Create", "spec", "plan", "next runway", or "upcoming work" means `create-spec`. "Execute", "run", "implement", "work through", or a specific spec path means `execute-spec`.

## Standard Execution Contract v1

Use this contract unless the spec explicitly overrides it. Treat named standard contracts as versioned and stable: do not reinterpret an existing spec's `Standard Execution Contract v1` reference using later contract semantics. If this contract needs incompatible changes, create `Standard Execution Contract v2` and keep v1 available for older specs.

- The main agent is coordinator only.
- The main agent must not implement code changes directly except for updating the ledger and making commits.
- Each slice implementation must be delegated to a coding subagent.
- Each completed slice must be reviewed by a separate review subagent before commit.
- Use `runway_worker` for coding subagents and `runway_reviewer` for review subagents when available.
- If subagent tooling is unavailable, stop and report that execution cannot proceed under this workflow.
- Do not fall back to main-agent implementation.
- Commit after each clean, focused slice.
- After each commit, report a commit receipt with:
  - commit hash and subject
  - files changed
  - validation result
  - sandbox result, when applicable
  - review result
  - exact inspection commands, usually `git show --stat <hash>` and `git show <hash>`
- Update the ledger after each slice with status, commit hash, focused validation, review result, review commands, and notes.
- After reporting a commit receipt, continue to the next pending slice unless the user explicitly asks to stop or a stop condition remains active.
- If execution is interrupted by an approval request, permission issue, transient infrastructure blocker, context transition, or user clarification, resume from the next incomplete ledger row as soon as the blocker is resolved.
- Do not stop after a successful slice commit merely because a commit receipt was reported.
- Preserve unrelated dirty files.
- Do not revert or commit files outside the slice scope.
- Stop on scope drift, unresolved ambiguity, repeatedly unresolved validation failure, dirty-file conflict, missing subagent support, or a stop condition from the spec.

## Standard Ledger v1

Use this ledger shape unless the spec explicitly overrides it.

```md
## Execution Ledger

| Slice | Status | Commit | Focused validation | Review | Review commands | Notes |
|---|---|---|---|---|---|---|
| 1 | pending | | | | | |
| 2 | pending | | | | | |
| 3 | pending | | | | | |
```

## Validation Profiles

Specs should reference validation profiles instead of repeating long command blocks when practical. Slice-specific commands and overrides still belong in the spec when the profile is not precise enough.

### `docs-only`

Use for local plans, docs-only edits, and non-code artifacts.

Per-slice validation:

- `git diff --check`
- project-specific doc checks only when the touched docs require them

Do not run pytest, ruff, Docker sandbox, or `graphify update .` unless the spec explicitly requires them.

### `test-only-topology`

Use for moving, splitting, or reorganizing tests without production code changes.

Per-slice validation:

- focused pytest for touched test modules
- ruff on touched test modules
- `git diff --check`

Final validation:

- full relevant test subset
- broader pytest if the spec requires it
- Docker-backed sandbox only at final validation unless the slice changes sandbox execution behavior, direct-runner coverage, runtime import/path assumptions, or the spec requires earlier sandbox validation
- `graphify update .` only if project instructions require it after test topology changes

### `mechanical-production-refactor`

Use for behavior-preserving production module moves, facade slimming, import cleanup, and ownership extraction.

Per-slice validation:

- focused pytest covering touched behavior
- ruff on touched production and test files
- `git diff --check`
- `graphify update .` when project instructions require it

Sandbox policy:

- Run Docker-backed install sandbox per slice if the touched code can affect installer sandbox execution.
- Treat module moves, runtime import cleanup, compatibility facade changes, report or summary generation changes, runtime path handling, artifact-shape handling, and changes to code imported by `tools/install_sandbox/run.py`, `sandbox_runner`, or `agent_summary` as sandbox-affecting even when the intended behavior is preserving.
- Otherwise run Docker-backed sandbox at final validation.

### `install-sandbox-production`

Use for installer sandbox production behavior, lifecycle, target selection, harness policy, YAML normalization, report/summary output, public CLI behavior, or sandbox artifact behavior.

Per-slice validation:

- focused pytest
- ruff
- Docker-backed `tools/install_sandbox/run.py` with an explicit fresh `--output tools/install_sandbox/out/<fresh-dir>`
- `python -m tools.install_sandbox.agent_summary tools/install_sandbox/out/<fresh-dir> --write`
- `graphify update .` when required
- `git diff --check`

Final validation:

- full install-sandbox test subset
- broader project tests when practical
- Docker-backed sandbox with an explicit fresh `--output tools/install_sandbox/out/<fresh-dir>`
- read generated `agent-summary.md` before reporting the final sandbox result

## Create-Spec Mode

Write one local plan file. Do not implement code.

1. Read applicable project instructions and local overlays first.
2. Inspect the current goal, existing local plans, recent commits, current ledger state, and the last completed task enough to identify the next related work.
3. Pick 3-5 tightly related slices that can execute sequentially.
4. Keep each slice independently testable and committable.
5. Store the spec in the project's local planning location. For Graphify, use `my-docs/plans/`.
6. Prefer `lean-runway` unless the work touches high-risk production behavior.

The spec must include:

- title and purpose
- current baseline and assumptions
- non-goals for the whole batch
- execution contract reference
- validation profile
- execution ledger
- 3-5 slice sections
- final validation
- stop conditions

For lean specs, do not paste the full standard execution contract. Reference it:

```md
## Execution Contract

Use Batch Runway Standard Execution Contract v1.

Overrides:
- <only list deviations from the standard contract>
```

For lean specs, do not repeat full command blocks in every slice if a validation profile covers them. Reference the profile and list only slice-specific commands or overrides.

Each slice must include:

- scope
- allowed files or file areas
- non-goals
- acceptance criteria
- validation profile or focused validation overrides
- commit message
- coding subagent brief reference or compact brief
- review subagent brief reference or compact brief
- stop conditions

### Lean Coding Brief Format

Use this compact brief when the subagent can read the spec file directly:

```text
Use agent_type="runway_worker".

Implement slice <N> from <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Read the full slice and applicable execution contract in the spec.
Use the standard runway_worker return format.
Allowed files/areas: <repeat exact allowed files if needed for safety>.
Dirty-file constraints: preserve unrelated dirty files; do not touch generated output except allowed validation output.
Return only: files changed, behavior changed, tests run, risks, follow-up needed.
```

Only paste the full slice content into the subagent brief when the subagent cannot reliably read the spec path or when the slice is unusually risky.

### Lean Review Brief Format

Use this compact brief when the reviewer can read the spec file directly:

```text
Use agent_type="runway_reviewer".

Review slice <N> against <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Inspect only the task-scoped diff and relevant files.
Check scope, acceptance criteria, validation evidence, dirty-file leakage, and behavior preservation.
Return findings first, then residual risks. Do not modify files.
```

Only paste full acceptance criteria when the reviewer cannot reliably read the spec path or when the review boundary is subtle.

## Execute-Spec Mode

Enforce the spec. Do not create a new plan unless the spec is ambiguous, stale, or missing required execution details.

Coordinator preflight:

1. Read project instructions, local overlays, and the full spec.
2. Check the worktree and identify dirty-file risks.
3. Identify:
   - active validation profile
   - pending ledger rows
   - stop conditions
   - commit strategy
   - whether this is `lean-runway` or `full-runway`
4. Confirm subagent tooling is available.
5. Prefer `runway_worker` for coding and `runway_reviewer` for review.
6. If required custom agents are unavailable because Codex has not reloaded configuration yet, stop and ask for a restart or new thread rather than falling back to main-agent implementation.

For each slice:

1. Spawn a coding subagent with `agent_type="runway_worker"`.
2. In lean mode, pass the absolute spec path, repo cwd, slice number, slice anchor, allowed files, dirty-file constraints, and slice-specific overrides. Do not paste the full slice unless needed.
3. Require the coding result to include: files changed, behavior changed, tests run, risks, and follow-up needed.
4. Run or verify focused validation from the coordinator session when practical.
5. Apply the active validation profile.
6. If the slice is test-only and uses `test-only-topology`, do not run the Docker-backed sandbox per slice unless the slice changes sandbox execution behavior, direct-runner coverage, runtime import/path assumptions, or the spec requires it.
7. If the slice touches installer-sandbox production code or behavior, run the installer sandbox for that slice before review and before commit unless the validation profile explicitly defers it.
8. Treat module moves, runtime import cleanup, compatibility facade changes, report or summary generation changes, runtime path handling, artifact-shape handling, and changes to code imported by `tools/install_sandbox/run.py`, `sandbox_runner`, or `agent_summary` as sandbox-affecting.
9. Use an explicit fresh sandbox output directory: `--output tools/install_sandbox/out/<fresh-dir>`.
10. If focused validation fails, inspect the failure and delegate a follow-up fix to a coding subagent when the fix is within slice scope and does not require a human decision.
11. Re-run validation after in-scope fixes.
12. Stop only when the failure is ambiguous, out of scope, repeatedly unresolved, or indicates a dirty-file conflict.
13. Spawn a separate review subagent with `agent_type="runway_reviewer"`.
14. In lean mode, pass the absolute spec path, repo cwd, slice number, slice anchor, task-scoped diff context, and review focus. Do not paste the full slice unless needed.
15. If review finds issues, delegate follow-up fixes to a coding subagent unless the fix is only a ledger or commit-message adjustment.
16. Commit only the files intentionally changed for that slice once validation and review are clean.
17. Immediately report a commit receipt with hash, subject, files changed, validation result, sandbox result when applicable, review result, and inspection commands.
18. Update the ledger with status, commit hash, focused validation result, review result, review commands, and notes.
19. Close completed subagents before continuing to avoid thread-limit failures.
20. Continue directly to the next pending ledger row.

After the last completed slice:

1. Run the spec's final validation.
2. Run any project-required graph or index refresh after code changes.
3. Report completed commits, validation results, skipped slices, and remaining risks.
4. If final validation uses the Docker-backed sandbox, read `agent-summary.md` before reporting the final sandbox result.

## Hard Rules

- Do not let the main agent become the implementer in `execute-spec` mode.
- Stop if the next slice depends on unresolved failures from the prior slice.
- After a resolved interruption, approval, permission issue, context transition, or clarification, resume the same runway at the next incomplete ledger row.
- Do not stop after a successful slice commit merely because a commit receipt was reported.
- Try to resolve validation or review failures by delegating in-scope follow-up fixes before stopping.
- Stop on scope drift, ambiguity, repeatedly unresolved validation failure, dirty-file conflict, or missing subagent support.
- Preserve unrelated dirty files.
- Do not revert or commit files outside the slice scope.
- Keep commits aligned to one slice and one ownership boundary.
- Prefer focused tests after each slice and broad validation once at the end.
- Use lean specs and lean subagent briefs when they preserve safety.
- Use full explicit specs when risk, ambiguity, or missing subagent file access makes compact references unsafe.

## Subagent Brief Rules

Coding subagent briefs should include only the context needed for that slice.

Prefer compact briefs:

```text
Use agent_type="runway_worker".

Implement slice <N> from <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Read the full slice and applicable execution contract in the spec.
Allowed files/areas: ...
Dirty-file constraints: ...
Return only: files changed, behavior changed, tests run, risks, follow-up needed.
```

Use full briefs only when:

- the subagent may not be able to read the spec file
- the slice has subtle non-goals
- the slice has unusual stop conditions
- the work touches high-risk production behavior
- previous attempts showed the compact brief was insufficient

Review subagent briefs should be independent but compact:

```text
Use agent_type="runway_reviewer".

Review slice <N> against <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Inspect only the task-scoped diff and relevant files.
Check: scope, acceptance criteria, validation evidence, behavior changes, dirty-file leakage.
Return findings first, then residual risks. Do not modify files.
```

## Support-Only Custom Agents

- Use `fast_explorer` only for read-only side investigations that do not replace required coding or review subagents.
- Use `spark` only for lightweight, low-risk iteration.
- Do not use `spark` for required Batch Runway review, security review, broad refactors, or ambiguous installer-sandbox failure recovery.

## Graphify Defaults

When used in `/home/alacasse/projects/graphify`:

- Read committed `AGENTS.md`, then `my-docs/AGENTS.md`.
- Put local runway specs under `my-docs/plans/`.
- Use `uv run --frozen pytest ...` for validation unless dependencies or packaging metadata are intentionally changed.
- For installer-sandbox changes, follow local installer validation guidance in `my-docs/AGENTS.md`.
- When executing install-sandbox production slices, run the Docker-backed `tools/install_sandbox/run.py` validation after each slice before committing unless the slice is documentation-only, test-only, or explicitly cannot affect sandbox execution.
- Treat production module moves, runtime import cleanup, facade changes, summary/report changes, path handling, artifact-shape handling, and code imported by `tools/install_sandbox/run.py`, `sandbox_runner`, or `agent_summary` as sandbox-affecting.
- For test-only topology slices, prefer focused pytest and ruff per slice, then run Docker-backed sandbox at final validation unless the spec requires earlier sandbox validation.
- Always pass an explicit fresh `--output tools/install_sandbox/out/<fresh-dir>` to `tools/install_sandbox/run.py`.
- If the Docker-backed sandbox fails with `permission denied` for `/var/run/docker.sock`, request escalation and rerun the same sandbox command. Treat this as a host Docker permission issue, not a code failure.
- After code edits, run `graphify update .` if project instructions require it.
- If graph queries are too broad for runway planning, prefer the completed ledger, recent commits, current module shape, and local plans.
