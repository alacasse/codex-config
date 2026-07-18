# CCFG-26A Permanent Vertical Runway Contract Dispatch

## Selection

- Batch ID: `ccfg-26a-permanent-vertical-runway-contract`
- Selection outcome: `selected`
- Queue target: exactly one `queued` runway
- Covered finding: CCFG-26, preparation for execution and closeout ownership
  transfer to `work-batch`
- Finding state entering the batch: `Open`
- Source program ledger: `../../LEDGER.md`
- Expected runway path: `runway.md`
- Planning root: `../../../..`
- Implementation target:
  `/home/alacasse/projects/codex-config-command-owner-redesign`

Planning State `current` and `validate` reported an idle, valid program with no
selected dispatch, queued batch, active runway, blocker, or obligation. The
explicit `plan-batch` invocation selects only CCFG-26A. CCFG-26B through
CCFG-26E remain deferred and unselected.

## Authoritative Sources

- CCFG-26 in `../../LEDGER.md`.
- COR-009 at accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- `../../findings/command-owner-redesign-planning-execution-carry-forward.md`.
- `../../findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`.
- GitHub issues #59, #60, and #61.
- `../../notes/stable-runway-dogfooding-policy.md`.
- The superseded CCFG-26 package in
  `../ccfg-26-execution-closeout-ownership-transfer/` as historical evidence
  only.

## Review And Split Decision

The superseded three-slice CCFG-26 runway is not repairable in place. It groups
complete owner construction, broad old-owner removal, and repository-wide
convergence into horizontal slices. It has no permanent vertical-slice,
migration-matrix, recovery-advisor, or fresh-flight contract and is explicitly
non-executable.

CCFG-26 is therefore split into vertical child batches while retaining the one
CCFG-26 finding and COR-009 identity:

1. CCFG-26A: permanent vertical-runway planning contract;
2. CCFG-26B: queued slice through a fresh coordinator flight and durable commit
   receipt;
3. CCFG-26C: bounded recovery advisor and fresh same-slice resume;
4. CCFG-26D: last-slice receipt through a separate finalization flight; and
5. CCFG-26E: finalization receipt through same-batch closeout, reconciliation,
   no-successor proof, and final displaced-owner narrowing.

Only CCFG-26A is selected or queued by this planning flight. A later explicit
`plan-batch` invocation owns each later child batch.

## Goal

Make the permanent candidate `plan-batch`, `batch_planner`, and
`batch_plan_reviewer` enforce the vertical planning behavior required by issue
#60 before execution ownership begins moving:

- every migration or ownership-transfer implementation slice names one starting
  scenario and one durable result;
- every temporary coexistence route is caller-mapped with current owner, future
  owner, retention reason, status, and removal condition;
- slice count follows independently useful behavior, validation, ownership,
  review, and rollback boundaries;
- an oversized boundary requires a smaller-alternative analysis rather than an
  arbitrary numeric rejection; and
- focused per-slice validation remains separate from final-range validation.

## Vertical Slice

```yaml
vertical_slice:
  starting_scenario: candidate plan-batch receives one migration or ownership-transfer finding
  durable_result: the queued plan is mechanically bound to vertical slice fields, caller migration ownership, focused validation, rollback-safe intermediate state, and independent proportionality review
  owner_before: candidate plan-batch semantic-slice and proportionality rules plus temporary stable repository policy
  owner_after: permanent candidate plan-batch command with batch_planner authoring and batch_plan_reviewer enforcement
  migrated_callers:
    - candidate plan-batch draft validation
    - registered batch_planner
    - registered batch_plan_reviewer
    - planning-runway/v1 artifact validation
  focused_validation:
    - focused plan-batch and planning-contract tests
    - registered-agent contract tests
    - vertical planning behavioral scenarios
    - command-owner scenario catalog validation
    - delta-only test-quality review
    - independent exact-diff runway review
  independently_usable_state: candidate planning rejects ambiguous horizontal ownership-transfer runways before any work-batch execution owner changes
  rollback_boundary: one candidate commit restores the exact CCFG-25 candidate baseline without touching stable planning or the default Codex home
  temporary_residue:
    - stable CCFG-34 policy and root instruction hook remain until CCFG-29
    - execution telemetry remains owned by the later CCFG-26B through CCFG-26E sequence
    - work-batch, Batch Runway, and APR execution/closeout ownership remains unchanged
```

## Migration Matrix

```yaml
migration_matrix:
  migration_plan_draft:
    current_owner: batch_planner semantic slice rationale
    future_owner: batch_planner vertical_slice and migration_matrix contract
    reason: the planner must author the complete vertical evidence before independent review
    status: pending
    removal_slice_or_condition: CCFG-26A only slice passes focused review
  independent_planning_review:
    current_owner: batch_plan_reviewer semantic_slices and proportionality checks
    future_owner: batch_plan_reviewer vertical boundary, caller ownership, residue, and smaller-alternative checks
    reason: the reviewer must reject ambiguous ownership and oversized horizontal phases independently
    status: pending
    removal_slice_or_condition: CCFG-26A only slice passes focused review
  plan_batch_command_contract:
    current_owner: plan-batch generated-plan checklist and command stop boundary
    future_owner: plan-batch permanent vertical migration-plan requirement
    reason: the human-facing command must require and route the vertical contract before deterministic queue mutation
    status: pending
    removal_slice_or_condition: CCFG-26A only slice passes focused review
  deterministic_queue_gate:
    current_owner: plan-batch and scripts/plan_batch.py semantic rationale validation
    future_owner: plan-batch and scripts/plan_batch.py permanent vertical contract validation
    reason: malformed or incomplete vertical evidence must fail mechanically before queue mutation
    status: pending
    removal_slice_or_condition: CCFG-26A exact acceptance is green
  planning_runway_artifact:
    current_owner: planning-runway/v1 generic slice fields
    future_owner: planning-runway/v1 vertical_slice fields and caller migration matrix
    reason: the durable queued artifact must preserve the evidence later execution and review consume
    status: pending
    removal_slice_or_condition: CCFG-26A exact acceptance is green
  per_flight_execution_telemetry:
    current_owner: no permanent candidate owner
    future_owner: CCFG-26B through CCFG-26E work-batch flight contracts
    reason: execution metrics require the later durable flight owner and are outside this planning-only batch
    status: pending
    removal_slice_or_condition: final CCFG-26 closeout
```

## Batch Kind And Approval

- Batch kind: `mixed-risk`.
- Implementation slice risk: `contract-narrowing`.
- Approval gate: the CCFG-26 ledger row, issue #60, and the user's explicit
  request to redo CCFG-26 under the new planning approach authorize the
  candidate planning contract to reject migration or ownership-transfer plans
  that omit the required vertical fields or leave caller ownership ambiguous.
- The gate does not authorize execution ownership transfer, new execution
  state, recovery-advisor implementation, runner protocol changes, bridge
  changes, legacy deletion, or default-generation changes.

## Scope Ceiling

Primary candidate surfaces:

- `skills/plan-batch/**`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `scripts/plan_batch.py`
- `schemas/planning-runway-v1.schema.json`
- focused planning, agent-contract, scenario, schema, and manifest tests
- associated scenario fixtures, `codex-features.json`, and `CHANGELOG.md`

`scripts/planning_contract.py` is conditional and may change only when the
existing planning-runway validator must consume the new required fields. No
other candidate path is authorized.

## Non-Goals

- No `work-batch`, Batch Runway, APR, runner, worker, reviewer, strict-context,
  recovery, finalization, closeout, or reconciliation ownership change.
- No recovery-advisor agent or result contract.
- No execution-flight schema, launcher, process boundary, state, receipt, or
  telemetry implementation.
- No serialized phase identity change; CCFG-27 owns that decision.
- No physical legacy deletion; CCFG-28 owns it.
- No bridge change, merge, default-home switch, or temporary-policy removal;
  CCFG-29 owns them.
- No stable planning or candidate implementation outside the validated roots.

## Validation Class

Use `project-harness-production`. Per-slice validation stays focused on the
candidate planning scenario. Exact-commit command-owner acceptance, clean
candidate installation, stable-home comparison, and final independent reviews
remain final gates rather than a standalone implementation slice.

## Stop Conditions

- Stop if the slice cannot leave one independently usable candidate planning
  state.
- Stop if the change needs execution-owner, runner, recovery-advisor,
  finalization, closeout, or reconciliation work.
- Stop if the planning artifact identity must change from
  `planning-runway/v1` rather than evolve compatibly under its existing owner.
- Stop if the proposed slice is clearly oversized without a recorded smaller
  alternative and independent review of the accepted boundary.
- Stop if any retained route lacks a caller, current owner, reason, future
  owner, status, or removal
  condition.
- Stop on candidate code outside the exact runway ceiling, stable-home writes,
  canonical candidate writes, default-generation change, or successor
  selection.
