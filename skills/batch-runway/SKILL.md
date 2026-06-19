---
name: batch-runway
description: Create and execute multi-slice runway specs with per-slice scope, validation, ledger updates, commits, and mandatory coding/review subagent delegation. Use when the user asks to create a batch runway spec, execute a runway spec, streamline sequential slices, work from my-docs/plans, commit after each slice, or keep the main agent as coordinator only while subagents implement and review.
---

# Batch Runway

Use this skill for a controlled sequence of small, independently committable slices. It has two modes:

- `create-spec`: write a runway spec for a future execution session.
- `execute-spec`: execute an existing runway spec one slice at a time.

If the user does not name a mode, infer it from the request. "Create", "spec", "plan", "next runway", or "upcoming work" means `create-spec`. "Execute", "run", "implement", "work through", or a specific spec path means `execute-spec`.

## Create-Spec Mode

Write one local plan file. Do not implement code.

1. Read applicable project instructions and local overlays first.
2. Inspect the current goal, existing local plans, recent commits, and the last completed task enough to identify the next related work.
3. Pick 3-5 tightly related slices that can execute sequentially.
4. Keep each slice independently testable and committable.
5. Store the spec in the project's local planning location. For Graphify, use `my-docs/plans/`.

The spec must include:

- title and purpose
- current baseline and assumptions
- non-goals for the whole batch
- execution contract
- execution ledger
- 3-5 slice sections
- final validation
- stop conditions

Each slice must include:

- scope
- allowed files or file areas
- non-goals
- acceptance criteria
- focused validation commands
- commit message
- coding subagent brief
- review subagent brief
- stop conditions

Add this execution contract to every spec:

```md
## Execution Contract

The execution session must treat the main agent as coordinator only.

- The main agent must not implement code changes directly except for updating this ledger and making commits.
- Each slice implementation must be delegated to a coding subagent.
- Each completed slice must be reviewed by a separate review subagent before commit.
- Use the `runway_worker` custom agent for coding subagents and the
  `runway_reviewer` custom agent for review subagents when those agents are
  available.
- If subagent tooling is unavailable, stop and report that execution cannot proceed under this workflow.
- Do not fall back to main-agent implementation.
- Commit after each clean, focused slice.
- After each commit, report a commit receipt in chat with the commit hash,
  subject, files changed, validation/sandbox result, and review commands.
- Update the ledger after each slice with status, commit hash, focused tests,
  review result, review commands, and notes.
- After reporting a commit receipt, continue to the next pending slice unless
  the user explicitly asks to stop or a stop condition remains active.
- If execution is interrupted by an approval request, permission issue,
  transient infrastructure blocker, context transition, or user clarification,
  resume from the next incomplete ledger row as soon as the blocker is resolved.
```

Use this ledger shape:

```md
## Execution Ledger

| Slice | Status | Commit | Focused validation | Review | Review commands | Notes |
|---|---|---|---|---|---|---|
| 1 | pending | | | | | |
| 2 | pending | | | | | |
| 3 | pending | | | | | |
```

## Execute-Spec Mode

Enforce the spec. Do not create a new plan unless the spec is ambiguous, stale, or missing required execution details.

Coordinator preflight:

1. Read project instructions, local overlays, and the full spec.
2. Check the worktree and identify dirty-file risks.
3. Summarize slices, stop conditions, focused validation, and commit strategy.
4. Confirm subagent tooling is available. If unavailable, stop.
5. Prefer the personal custom agents `runway_worker` for coding and
   `runway_reviewer` for review. If those custom agents are unavailable because
   Codex has not reloaded configuration yet, stop and ask for a Codex restart
   or new thread rather than falling back to main-agent implementation.

For each slice:

1. Spawn a coding subagent with `agent_type="runway_worker"` and include the slice scope, allowed files, non-goals, acceptance criteria, focused validation, and current dirty-file constraints.
2. Wait for the coding result and require a concise summary: files changed, behavior changed, tests run, risks, and follow-up needed.
3. Run or verify the focused validation from the coordinator session when practical.
4. If the slice touches installer-sandbox code or behavior, run the installer sandbox for that slice as part of focused validation, before review and before commit. Treat the installer sandbox as an extension of unit tests, not only as end-of-batch validation.
5. If focused validation fails, inspect the failure and delegate a follow-up fix to a coding subagent when the fix is within the slice scope and does not require a human decision. Re-run validation after the fix. Stop only when the failure is ambiguous, out of scope, repeatedly unresolved, or indicates a dirty-file conflict.
6. Spawn a separate review subagent with `agent_type="runway_reviewer"` and include the task-scoped diff and slice acceptance criteria.
7. If review finds issues, delegate follow-up fixes to a coding subagent unless the fix is only a ledger or commit-message adjustment.
8. Commit only the files intentionally changed for that slice once validation and review are clean.
9. Immediately report a commit receipt in chat with:
   - commit hash and subject
   - files changed
   - focused validation and installer-sandbox result, when applicable
   - review result
   - exact commands to inspect the commit, usually `git show --stat <hash>` and `git show <hash>`
10. Update the ledger with status, commit hash, focused validation result, review result, review commands, and notes.
11. Close completed subagents before continuing to avoid thread-limit failures.
12. Continue directly to the next pending ledger row. Do not treat the commit
    receipt or a resolved approval/sandbox interruption as a stopping point
    unless the user explicitly asked to pause or a stop condition still applies.

After the last completed slice:

1. Run the spec's final validation.
2. Run any project-required graph or index refresh after code changes.
3. Report completed commits, validation results, skipped slices, and remaining risks.

## Hard Rules

- Do not let the main agent become the implementer in `execute-spec` mode.
- Stop if the next slice depends on unresolved failures from the prior slice.
- After a resolved interruption, approval, permission issue, context transition,
  or clarification, resume the same runway at the next incomplete ledger row.
- Do not stop after a successful slice commit merely because a commit receipt
  was reported; keep executing pending slices until the spec is complete or a
  stop condition applies.
- Try to resolve validation or review failures by delegating in-scope follow-up fixes before stopping.
- Stop on scope drift, ambiguity, repeatedly unresolved validation failure, dirty-file conflict, or missing subagent support.
- Preserve unrelated dirty files. Do not revert or commit files outside the slice scope.
- Keep commits aligned to one slice and one ownership boundary.
- Prefer focused tests after each slice and broad validation once at the end.

## Subagent Briefs

Coding subagent briefs should include only the context needed for that slice:

```text
Use agent_type="runway_worker".

Implement slice <N> from <spec path>.
Allowed files/areas: ...
Non-goals: ...
Acceptance criteria: ...
Focused validation: ...
Dirty-file constraints: ...
Return only: files changed, behavior changed, tests run, risks, follow-up needed.
```

Review subagent briefs should be independent:

```text
Use agent_type="runway_reviewer".

Review slice <N> against <spec path>.
Inspect only the task-scoped diff and relevant files.
Check: scope, ownership boundary, behavior changes, tests, dirty-file leakage.
Return findings first, then residual risks. Do not modify files.
```

Support-only custom agents:

- Use `fast_explorer` only for read-only side investigations that do not replace
  the required coding or review subagents.
- Use `spark` only for lightweight, low-risk iteration. Do not use it for
  required Batch Runway review, security review, broad refactors, or ambiguous
  installer-sandbox failure recovery.

## Graphify Defaults

When used in `/home/alacasse/projects/graphify`:

- Read committed `AGENTS.md`, then `my-docs/AGENTS.md`.
- Put local runway specs under `my-docs/plans/`.
- Use `uv run --frozen pytest ...` for validation unless dependencies or packaging metadata are intentionally changed.
- For installer-sandbox changes, follow the local installer validation guidance in `my-docs/AGENTS.md`.
- When executing install-sandbox slices, run the Docker-backed `tools/install_sandbox/run.py` validation after each slice, before committing, unless the slice is documentation-only and explicitly cannot affect sandbox execution.
- If the Docker-backed sandbox fails with `permission denied` for
  `/var/run/docker.sock`, request escalation and rerun the same sandbox command.
  Treat this as a host Docker permission issue, not a code failure.
- After code edits, run `graphify update .` if project instructions require it.
