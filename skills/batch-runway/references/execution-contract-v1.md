# Standard Execution Contract v1

Use this contract unless the spec explicitly overrides it.

Treat named standard contracts as versioned and stable. Do not reinterpret an
existing spec's `Standard Execution Contract v1` reference using later contract
semantics. If this contract needs incompatible changes, create
`Standard Execution Contract v2` and keep v1 available for older specs.

Rules:

- These delegation rules bind the coordinator, not spawned workers or reviewers.
  A spawned `runway_worker` is already the required coding subagent for its
  assigned slice; it must implement that slice directly and must not spawn,
  delegate to, or wait on additional coding or review agents.
- The coordinator owns validation, review delegation, ledger updates, commits,
  and subagent lifecycle unless a spec explicitly says otherwise.
- The main agent is coordinator only.
- The main agent must not implement code changes directly except for updating
  the ledger and making commits.
- Each slice implementation must be delegated to a coding subagent.
- Each completed slice must be reviewed by a separate review subagent before
  commit.
- Use `runway_worker` for coding subagents and `runway_reviewer` for review
  subagents when available.
- If subagent tooling is unavailable, stop and report that execution cannot
  proceed under this workflow.
- Do not fall back to main-agent implementation.
- Commit after each clean, focused slice.
- After each commit, report a commit receipt with:
  - commit hash and subject
  - files changed
  - validation result
  - sandbox result, when applicable
  - review result
  - exact inspection commands, usually `git show --stat <hash>` and
    `git show <hash>`
- Update the ledger after each slice with status, commit hash, focused
  validation, review result, review commands, and notes.
- After reporting a commit receipt, continue to the next pending slice unless
  the user explicitly asks to stop or a stop condition remains active.
- If execution is interrupted by an approval request, permission issue,
  transient infrastructure blocker, context transition, or user clarification,
  resume from the next incomplete ledger row as soon as the blocker is resolved.
- Do not stop after a successful slice commit merely because a commit receipt
  was reported.
- Preserve unrelated dirty files.
- Do not revert or commit files outside the slice scope.
- Stop on scope drift, unresolved ambiguity, repeatedly unresolved validation
  failure, dirty-file conflict, missing subagent support, or a stop condition
  from the spec.

New specs should pair this execution contract with:

- `Compact Report Contract v1`
- `Compact Convergence Assessment v1`
- `Standard Ledger Retention v1`
