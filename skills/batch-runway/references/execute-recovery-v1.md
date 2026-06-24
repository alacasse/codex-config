# Execute Recovery v1

Use this reference only when routine slice execution leaves the normal path.

## Load Triggers

- focused validation fails
- selected-profile validation fails
- review finds issues
- a blocker appears
- scope drift or ambiguity appears
- dirty-file conflict appears
- approval, permission, or infrastructure issue interrupts execution
- subagent tooling or custom agents are unavailable
- a compact handoff was insufficient

## Validation Failure Handling

1. Inspect the failure enough to classify it.
2. If the fix is within slice scope and does not require a human decision,
   delegate a follow-up fix to `runway_worker`.
3. Re-run failed validation after the fix.
4. Stop when the failure is ambiguous, out of scope, repeatedly unresolved, or
   indicates a dirty-file conflict.
5. Record unresolved validation findings in the active ledger.

Do not widen the slice to chase unrelated failures.

## Reviewer Fix Loop

1. If review finds required fixes, classify each finding as in-scope,
   ledger-only, commit-message-only, or out-of-scope.
2. Delegate in-scope code fixes to `runway_worker`.
3. Make ledger-only or commit-message-only adjustments directly as coordinator.
4. Re-run focused validation after code fixes.
5. Re-run review or ask the reviewer to verify the fix when the finding affects
   behavior, scope, tests, or validation evidence.
6. Stop on unresolved disagreement, ambiguity, or out-of-scope requested changes.

## Blockers And Escalation

Stop and report when:

- subagent support is missing
- required project values are missing
- approval or sandbox permissions are required and unresolved
- validation remains repeatedly unresolved
- dirty files conflict with slice ownership
- project instructions conflict and priority order is unclear
- scope drift would require changing the spec

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
