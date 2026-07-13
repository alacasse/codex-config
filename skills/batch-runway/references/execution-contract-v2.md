# Standard Execution Contract v2

Use this contract for new specs unless the spec explicitly selects another
version. Existing specs that name `Standard Execution Contract v1` keep the v1
interpretation.

Rules:

- An explicitly pre-creation runway must carry a complete validated
  `cross-checkout-precreation/v1` payload and installed helper path. The
  coordinator must follow `cross-checkout-precreation-v1.md`, revalidate the
  payload and exact intended creation targets before applicable delegations,
  propagate the mechanical context, and reject a missing, null, or mismatched
  `verified_cross_checkout_precreation` field. Before implementation beyond
  repository and environment establishment, it must require the versioned
  helper-produced transition receipt and a validated strict context. A
  pre-creation result cannot satisfy strict verification, and neither field
  grants lifecycle authority.
- A runway that explicitly names `cross-checkout-context/v1` or explicitly
  declares separate existing toolchain, canonical-planning, and implementation
  repository roots must carry a complete validated strict payload and canonical
  planning root. The coordinator must follow `cross-checkout-context-v1.md`,
  revalidate before every worker and reviewer delegation, propagate the
  mechanical context, and reject missing, null, or mismatched verified identity
  in either agent result. A `cross-checkout-precreation/v1` runway remains
  outside this strict branch with `verified_cross_checkout_context` null until a
  validated helper-produced transition receipt plus green strict context
  exists. This validation grants no lifecycle authority.
- These delegation rules bind the coordinator, not spawned workers or reviewers.
  A spawned `runway_worker` is already the required coding subagent for its
  assigned slice; it must implement that slice directly and must not spawn,
  delegate to, or wait on additional coding or review agents.
- The coordinator owns validation, review delegation, concrete
  execution-ledger updates, completed-slice archive movement, commits, and
  subagent lifecycle unless a spec explicitly says otherwise.
- The main agent is coordinator only.
- The main agent must not implement code changes directly except for updating
  the concrete execution ledger and making commits.
- Each slice implementation must be delegated to a coding subagent.
- Each completed slice must be reviewed by a separate review subagent before
  commit.
- Use `runway_worker` for coding subagents and `runway_reviewer` for review
  subagents when available.
- If subagent tooling is unavailable, stop and report that execution cannot
  proceed under this workflow.
- Do not fall back to main-agent implementation.
- Commit after each clean, focused slice.
- Ordinary slice commits record exact commit hashes in the concrete execution
  ledger and completed-slice archive after the commit exists.
- A self-referential final closeout commit records `this closeout commit` in
  final closeout artifacts because the hash does not exist before that commit
  is created.
- Do not leave unresolved operational placeholders for coordinator commits,
  commit-pending states, commit receipt placeholders, or pending coordinator
  reviews in active batch artifacts.
- After each commit, report a commit receipt with:
  - commit hash and subject
  - files changed
  - validation result
  - sandbox result, when applicable
  - review result
  - exact inspection commands, usually `git show --stat <hash>` and
    `git show <hash>`
- Update the concrete execution ledger after each ordinary slice with status,
  commit hash, focused validation, review result, review commands, and notes.
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

- `Registered Agent Result Contract v2`
- `Compact Report Contract v1` for coordinator receipts
- `Compact Convergence Assessment v1`
- `Standard Ledger Retention v1`
