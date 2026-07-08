# Human-Facing Command Owner Skills

Use human-facing command-owner skills for the main ledger and batch workflows:
`add-to-ledger`, `plan-batch`, and `work-batch`. The existing
`architecture-program-runway` and `batch-runway` skill names describe internal
workflow history more than user intent, so the normal user-facing commands are
the command-owner skills. The old runtime names may remain installed only as
agent-facing support dependencies behind those commands.

## Status

Accepted.

## Consequences

- The user-facing command set is intentionally small: `add-to-ledger`,
  `plan-batch`, `work-batch`, and `port-by-contract`.
- `planning-state`, `planning-artifacts`, `test-quality-review`,
  `legacy-removal`, and `dead-surface-audit` remain agent-facing support or
  default workflow obligations unless the user explicitly asks for a focused
  investigation; they are not part of the normal user-facing cleanup command
  set.
- The migration should avoid permanent wrapper layers. The target is
  command-owner skills with narrow support skills behind them; old runtime
  metadata must not advertise those internals as preferred direct commands.
