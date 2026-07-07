# Human-Facing Command Owner Skills

Use human-facing command-owner skills for the main ledger and batch workflows:
`add-to-ledger`, `plan-batch`, and `work-batch`. The existing
`architecture-program-runway` and `batch-runway` skill names describe internal
workflow history more than user intent, so new command-owner skills will be
created copy-first beside the current skills, proven through normal workflow
use, and only then used to retire or demote the old runtime names.

## Status

Accepted.

## Consequences

- The user-facing command set is intentionally small: `add-to-ledger`,
  `plan-batch`, `work-batch`, and `port-by-contract`.
- `planning-state`, `planning-artifacts`, test-quality review, and legacy
  prevention remain agent-facing support or default workflow obligations unless
  the user explicitly asks for a focused investigation.
- The migration should avoid permanent wrapper layers. Thin routing is allowed
  while the new commands are being proven, but the target is command-owner
  skills with narrow support skills behind them.
