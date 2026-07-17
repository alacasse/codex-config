# CCFG-34 First Plan Superseded

The original CCFG-34 dispatch, runway, and independent review were committed at
`a6e2a40493577e9e670d3c41b081f71ca66f0a31`.

That plan proposed a temporary execution-unit architecture spanning the stable
runner loop, workers, state, transitions, receipts, validation, artifacts,
telemetry, finalization, closeout, and recovery classification.

It is preserved in Git history as planning evidence but is not executable.

## Reason

The implementation cost and risk were disproportionate to a temporary bootstrap
that exists only until CCFG-29. The user explicitly accepts manual relaunch
between slices and some remaining recovery friction to avoid changing stable
runner architecture.

## Replacement Boundary

The replacement plan is limited to:

- one repository-local temporary policy;
- one pending implementation slice per `work-batch` invocation;
- optional one-time use of the existing read-only investigator before avoidable
  escalation;
- no runner, state, transition, receipt, telemetry, launcher, or agent-contract
  changes.

Only the replacement `dispatch.md`, `runway.md`, and current `review.md` may be
treated as active CCFG-34 planning.
