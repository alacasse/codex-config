# Registered Agent Result Contract v2

Use this contract with `Standard Execution Contract v2`. It changes only agent
result ownership and presentation semantics; coordinator receipts, convergence,
orchestration anomalies, and ledger retention keep their existing named
contracts.

## Canonical Owners

Each registered agent TOML owns that role's exact status values, fields, field
semantics, completion standard, and stable authority boundary:

- `agents/runway_worker.toml`: worker result schema
- `agents/runway_reviewer.toml`: final-review result schema
- `agents/import_topology_reviewer.toml`: specialist result schema
- `agents/codebase_investigator.toml`: investigation result schema
- `agents/spark.toml`: lightweight support result schema

Workflow and skill documents own invocation conditions, task-specific handoffs,
coordinator lifecycle, triggered review routing, and local acceptance criteria.
They request the registered role contract instead of copying agent schemas into
prompts or examples.

The worker and final-reviewer TOMLs also own their nullable
`verified_cross_checkout_context` fields. For an explicitly cross-checkout
handoff, each role independently validates and reports mechanical repository
and generation identity. The field stays `null` otherwise. It never transfers
selection, execution acceptance, review acceptance, closeout, or successor
authority from the coordinator.

The coordinator must put the selected result contract in every worker and final
reviewer handoff. Use `Registered Agent Result Contract v2` for new v2 specs and
`Compact Report Contract v1` only when an existing spec names v1. The registered
worker and final reviewer use that handoff value to select the compatible schema
and stop when the handoff conflicts with the spec.

For v2 execution, these registered schemas supersede only the worker and
reviewer examples in `Compact Report Contract v1`. The v1 coordinator receipt,
convergence, anomaly-log, and information-lifetime rules remain applicable.
Existing specs that name only `Standard Execution Contract v1` and `Compact
Report Contract v1` keep the v1 worker and reviewer schemas.

## Presentation Rules

- Return structured results only when the role contract requires them.
- Concision governs presentation, not coverage. Include every material change,
  finding, blocker, failed or unavailable validation, uncertainty, and
  escalation that affects the next workflow decision.
- Omit duplicated evidence, raw logs, command transcripts, reasoning narration,
  and chronology.
- Expand output whenever the canonical agent schema needs to represent
  findings, blockers, failed validation, uncertainty, or escalation. No line
  limit may suppress a material result.
