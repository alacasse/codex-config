# GitHub Issue 62: Stable Runway Dogfooding Bootstrap

## Source

- GitHub issue: https://github.com/alacasse/codex-config/issues/62
- Title: Bootstrap temporary stable runway dogfooding before CCFG-26
- State when ingested: open
- Labels when ingested: none
- Created: 2026-07-17
- Updated when ingested: 2026-07-17
- Source identity: GitHub issue #62, authored by `alacasse`
- Related issues:
  - #59, Add bounded autonomous blocker recovery with a read-only advisor;
  - #60, Require vertical, context-bounded slices with controlled migration
    coexistence;
  - #61, Run each slice in a fresh coordinator flight.

## Summary

The remaining command-owner redesign batches must still be planned and executed
by the stable runway generation while the permanent candidate behavior from
#59, #60, and #61 is being built. Without a stable bootstrap, the most expensive
ownership-transfer work would run under the context, planning, and recovery
failure modes that those issues are intended to remove.

CCFG-34 adds only temporary stable-generation dogfooding support for CCFG-26
through CCFG-29. It must reuse existing durable ledgers, receipts, Planning
State, and runner state rather than implementing a second copy of the candidate
command-owner architecture.

## Intake And Queue Amendment

- Ledger identity: `CCFG-34`.
- Finding status: `Ready`; this intake does not select, dispatch, queue, or
  execute it.
- CCFG-34 is the next eligible planning candidate. A later explicit
  `plan-batch` invocation owns its selection and concrete runway.
- The currently queued CCFG-26 dispatch, independent review, and runway are
  superseded as executable planning and preserved unchanged as historical
  planning evidence.
- CCFG-26 becomes `Blocked` pending CCFG-34 closeout. It must be replanned after
  CCFG-34 and cannot resume from the superseded runway.
- CCFG-26 retains its finding identity and COR-009 acceptance boundary. Its
  future planning must absorb the permanent candidate-generation requirements
  from #59, #60, and #61 and may split preparation and ownership cutover into
  multiple batches when required for vertical, context-bounded execution.
- No batch is selected, queued, or active after this intake.

## Goal

Provide the main operational benefits of #59, #60, and #61 while the stable
runway generation still executes CCFG-26 through CCFG-29:

1. project-owned vertical and context-bounded planning requirements that are
   applied automatically;
2. one fresh coordinator process for each bounded execution unit; and
3. one bounded read-only recovery assessment before avoidable user escalation.

Every temporary mechanism requires an explicit owner and a removal condition
tied to candidate parity and CCFG-29 integration.

## Temporary Stable Scope

### Vertical planning and review policy

Stable planning must automatically consume one project-owned temporary policy
for CCFG-26 through CCFG-29. Migration and ownership-transfer slices must state:

```yaml
vertical_slice:
  starting_scenario: string
  durable_result: string
  owner_before: string
  owner_after: string
  migrated_callers: []
  focused_validation: []
  independently_usable_state: string
  rollback_boundary: string
  temporary_residue: []
```

When ownership temporarily coexists, planning must also provide an explicit
migration matrix:

```yaml
migration_matrix:
  scenario_or_caller:
    current_owner: string
    future_owner: string
    status: pending | migrated
    removal_slice_or_condition: string
```

The policy must additionally require:

- unambiguous caller ownership and no silent fallback to the prior owner;
- a named caller, reason, future owner, and removal condition for every retained
  legacy route;
- focused validation and review for the slice-owned scenario;
- final range validation as a separate boundary;
- advisory proportionality warnings around 12 changed files, 1,000 changed
  lines, 3 primary production surfaces, 2 ownership boundaries, 2 migration
  kinds, or 3 specialist review lenses;
- a smaller-alternative analysis whenever a warning is exceeded; and
- per-slice evidence for changed-file count, line delta, validation breadth,
  review lenses, duration, and coordinator compaction when observable.

The controlling criterion is that one fresh coordinator context can implement,
validate, review, commit, and archive the slice without compaction. The policy
must not impose arbitrary tiny slices or a fixed slice count.

### Fresh coordinator per execution unit

Add the smallest stable-generation launcher that can execute one bounded unit
in a fresh `codex exec` process and continue from durable canonical state. The
supported units are:

- one complete slice implementation, validation, review, commit, and receipt
  cycle;
- one same-slice recovery attempt after a blocker or approved correction;
- final validation and finalization; and
- same-batch closeout and reconciliation.

Reuse the active ledger, completed-slice archive, commit and phase receipts,
Planning State, and runner state. Add only the minimum temporary result the
outer launcher needs to choose the next unit safely. Any internal
`legacy-execution-unit/v1`-equivalent result is temporary, is not a permanent
public runner protocol, must preserve the four serialized compatibility phase
identities, and must never select successor work.

```yaml
interface: legacy-execution-unit/v1
status: completed | blocked | failed
unit: slice | finalization | closeout
slice_id: string | null
commit: string | null
next_action: continue_same_batch | resume_same_slice | finalize | closeout | require_user
```

Each fresh process loads only the current Planning State Diagnostic, active
runway and unit, active ledger row, validation profile, exact repository and
worktree state, immediately relevant prior receipt, unresolved anomalies, and
current strict lease. It must not reload completed chronology, raw transcripts,
or accepted review detail.

Record per-unit duration, token usage when available, compaction occurrence,
changed-file and line counts, validation breadth, support and review roles, and
blocker/recovery transitions.

### Read-only recovery assessment

Before escalating an eligible blocker, obtain exactly one fresh read-only
assessment through an existing support role such as `codebase_investigator`,
unless planning proves a separate temporary role is materially smaller or
safer. Give it a compact evidence packet containing the active runway and slice,
exact stop condition, failing command and tool scope, validation status,
baseline and candidate results, exact diff basis, repository/worktree state,
and smallest proposed recovery.

The result must distinguish root cause, smallest tested recovery, scope,
semantic change, authority expansion, safety weakening, missing evidence, and a
`recover`, `retry_environment`, or `require_user` recommendation.

```yaml
blocker_class: string
root_cause: string
smallest_tested_recovery: string | null
inside_current_scope: bool
semantic_change: bool
authority_expansion: bool
safety_weakened: bool
evidence_missing: []
recommendation: recover | retry_environment | require_user
```

The assessment is advisory only. It cannot edit, amend or approve the runway,
commit, delegate, select work, or approve its own recommendation. The stable
coordinator may act without the user only for recovery already authorized by
the active runway and recovery contract, such as an invocation correction, an
exact retry, a local environment/cache repair, a refreshed diff/review basis,
or an already authorized in-slice code/test repair.

Write-scope expansion, validation reclassification, semantic expansion, safety
weakening, new protocols or lifecycle surfaces, unapproved destructive work,
multiple material choices, and insufficient evidence still require user
direction or a reviewed amendment.

## CCFG-34 Self-Dogfooding

CCFG-34 cannot consume code that does not exist yet, so its own planning and
execution must manually apply the intended behavior:

- plan vertical, context-bounded slices with explicit intermediate states and
  migration residue;
- use a separate coordinator process per slice, finalization, and closeout;
- stop after each durable slice commit and resume from the next incomplete
  ledger row;
- obtain one read-only recovery assessment before escalating an avoidable
  blocker; and
- record enough evidence to judge proportionality and usefulness before CCFG-26
  consumes the bootstrap.

The final slice count comes from the actual vertical boundaries.

## Permanent Candidate Amendment

When CCFG-26 is replanned, its authoritative sources must require:

- #60 in candidate `plan-batch`, `batch_planner`, and `batch_plan_reviewer`
  behavior;
- #61 in candidate `work-batch` and runner/launcher execution boundaries; and
- #59 in candidate `work-batch` recovery through a registered read-only advisor
  and bounded authority envelope.

CCFG-34 must not implement those permanent candidate surfaces. CCFG-26 may use
multiple batches if one runway cannot preserve vertical, context-bounded
execution, but its finding identity and COR-009 acceptance remain unchanged.

## Acceptance Criteria

- CCFG-34 is implemented in the stable generation before CCFG-26 is replanned
  or executed.
- Stable planning consumes one temporary project-owned policy automatically;
  requirements are not copied into each runway.
- Ownership-transfer plans contain the vertical-slice fields, migration
  coexistence evidence, proportionality warnings, and smaller-alternative
  analysis required above.
- CCFG-34 itself follows the vertical and fresh-process discipline.
- A new coordinator process owns each slice flight, same-slice recovery flight,
  finalization flight, and closeout flight.
- Successful units continue the same batch from durable canonical state without
  shared live model context; missing, contradictory, or stale state stops.
- An eligible blocker receives at most one fresh read-only assessment, and that
  assessment cannot write, approve, commit, delegate, select, or widen work.
- Only recoveries already inside active authority proceed without the user.
- Deterministic proof covers multi-slice continuation, blocker-to-same-slice
  resume, final-slice-to-finalization-to-closeout, no successor selection,
  contradictory state/receipt rejection, and recovery authority classes.
- Telemetry is sufficient to evaluate context pressure and planning quality.
- Temporary mechanisms name CCFG-29 removal ownership and candidate-parity
  prerequisites.
- CCFG-26 durable source evidence requires the permanent candidate behavior from
  #59, #60, and #61.

## Removal Condition

Remove the CCFG-34 stable-generation mechanisms only during or after CCFG-29
when the candidate is integrated and authoritative, permanent #59/#60/#61
behavior is active and validated, equivalent CCFG-34 regression scenarios pass
through the candidate, and removal neither restores a legacy path nor makes the
remaining planning evidence unreadable. CCFG-29 must stop if parity is
incomplete.

## Non-Goals And Planning Rejection Gates

- No second complete runway or command-owner framework.
- No permanent public runner protocol, execution store, or lifecycle framework
  solely for the bootstrap.
- No CCFG-26 ownership transfer, COR-009 closeout, candidate integration,
  stable-home rebind, default-generation switch, or bridge deletion.
- No recursive advisor debate, nested coordinator hierarchy, autonomous general
  replanning, silent validation reclassification, safety weakening, scope
  expansion, destructive work, or successor selection.
- Reject planning that creates horizontal foundation slices before one
  representative path works end to end, gives the advisor amendment/approval
  authority, cannot explain CCFG-34 self-dogfooding, or lacks a mechanical and
  testable CCFG-29 removal condition.
