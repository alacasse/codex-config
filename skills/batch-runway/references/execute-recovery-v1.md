# Execute Recovery v1

Use this reference only when routine slice execution leaves the normal path.

## Load Triggers

- focused validation fails
- selected-profile validation fails
- review finds issues
- a blocker appears
- scope drift or ambiguity appears
- dirty-file conflict appears
- HEAD, the index, or the task-scoped diff changes unexpectedly
- review evidence appears stale or does not match the current diff
- approval, permission, or infrastructure issue interrupts execution
- subagent tooling or custom agents are unavailable
- a compact handoff was insufficient

## Cross-Checkout Movement Boundary

A queued `cross-checkout-context/v1` planning snapshot that no longer equals
live repository revisions is not, by itself, a recovery trigger. First route
through the normal `work-batch` ready/blocked preflight defined by the canonical
`cross-checkout-context-v1.md` bridge. A ready result supplies the first
strictly parsed live context without an orchestration anomaly. A
blocked result, null context, helper failure, or ambiguous queue-transaction
evidence freezes delegation. Preserve the diagnostic evidence and report any
amendment or replanning blocker without reinterpreting the helper's reason.
Recovery cannot accept the movement or replace the queued runway.

After startup, a live execution lease remains exact for one handoff. An exact
coordinator commit following an accepted action may advance a repository; verify
that commit and its intended paths, then prepare a fresh lease through the
normal slice loop. Freeze delegation and use workspace reconciliation when a
repository moves between lease preparation and handoff, when movement is not
explained by an accepted coordinator action, or when strict revalidation fails.
No post-lease movement may reach delegation on the old lease.

## Validation Failure Handling

1. Inspect the failure enough to classify it.
2. If the fix is within slice scope and does not require a human decision,
   delegate a follow-up fix to `runway_worker`.
3. Re-run failed validation after the fix.
4. Stop when the failure is ambiguous, out of scope, repeatedly unresolved, or
   indicates a dirty-file conflict.
5. Record unresolved validation findings in the active ledger.

Do not widen the slice to chase unrelated failures.

## Workspace Reconciliation

Use this lane when the worktree, index, or `HEAD` does not match the
coordinator's expected slice state.

1. Freeze staging, commits, and review acceptance until the state is reconciled.
2. Snapshot `HEAD`, status, staged files, unstaged files, and the task-scoped
   diff basis that will be validated or reviewed.
3. Classify every changed path as current-slice, previous-slice evidence,
   next-slice drift, unrelated dirty work, generated validation output, or
   unknown.
4. If `HEAD` moved unexpectedly, verify the commit contents before continuing.
   Treat unexpected commits as orchestration anomalies; do not amend, revert, or
   replace them unless the user explicitly asks.
5. If reconciliation requires changing tracked source, test, spec, or generated
   content, delegate that cleanup to `runway_worker` or stop for user direction.
   The coordinator may inspect diffs, update concrete execution ledgers, stage
   intended files, and make commits, but must not hand-edit or reverse-patch
   tracked content as implementation cleanup.
6. If the drift can be isolated without content edits, preserve it outside the
   commit path and document the dirty-file constraint.
7. After reconciliation, re-run the focused validation affected by the changed
   paths and re-request review with the exact commit hash or diff basis.

Stop instead of improvising when path ownership is unclear, a cleanup would
discard user work, or current-slice validation cannot run without unrelated
dirty changes.

## Reviewer Fix Loop

1. If review finds required fixes, classify each finding as in-scope,
   ledger-only, commit-message-only, or out-of-scope.
2. Delegate in-scope code fixes to `runway_worker`.
3. Make ledger-only or commit-message-only adjustments directly as coordinator.
4. Re-run focused validation after code fixes.
5. Re-run review or ask the reviewer to verify the fix when the finding affects
   behavior, scope, tests, or validation evidence.
6. Stop on unresolved disagreement, ambiguity, or out-of-scope requested changes.

## Stale Review Or Diff Mismatch

If reviewer findings cite code that is absent from the current task-scoped diff,
or the reviewer appears to have inspected a stale checkout:

1. Do not accept the review as clean or actionable yet.
2. Re-snapshot `HEAD`, status, and the task-scoped diff basis.
3. Ask the reviewer to verify against the exact commit hash or attached diff
   basis, or spawn a fresh `runway_reviewer` if the first review cannot be
   trusted.
4. Record a compact orchestration anomaly if the mismatch suggests tooling,
   checkout, or lifecycle confusion.
5. Continue only after review evidence matches the reconciled diff basis.

## Blockers And Escalation

Stop and report when:

- subagent support is missing
- required project values are missing
- approval or sandbox permissions are required and unresolved
- validation remains repeatedly unresolved
- dirty files conflict with slice ownership
- project instructions conflict and priority order is unclear
- scope drift would require changing the spec
- workspace reconciliation would require coordinator-authored code or test edits
- review evidence cannot be matched to the current commit or diff basis

When stopping, report:

- blocker
- exact source checked
- current slice
- files touched
- validation/review state
- next safe action

## Resume Behavior

After a resolved interruption, approval, permission issue, context transition, or
clarification, resume the same runway at the next incomplete ledger row.

Do not stop after a successful slice commit merely because a commit receipt was
reported.

## Expanded Output

Use expanded worker/reviewer/coordinator output only when findings, blockers,
failed validation, or escalation require details. Do not paste long transcripts;
reference artifacts, commands, commits, or logs by path.
