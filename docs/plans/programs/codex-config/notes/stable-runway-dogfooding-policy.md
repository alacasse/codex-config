# Temporary Stable-Runway Dogfooding Policy

## Scope

This repository-local policy applies only when the stable generation plans or
executes CCFG-26 through CCFG-29. It is a temporary bridge to the integrated
candidate, not a reusable workflow contract.

Manual relaunch between implementation slices is an accepted tradeoff. This
policy does not promise automatic continuation or a fresh process at each
lifecycle boundary. Final range validation, finalization, and same-batch
closeout retain their existing stable behavior; this policy neither requires
nor creates separate finalization or closeout processes.

## Vertical Planning

Every migration or ownership-transfer implementation slice must describe one
starting scenario and the durable state produced for that scenario:

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

When ownership coexists temporarily, the plan must also map every affected
scenario or caller:

```yaml
migration_matrix:
  scenario_or_caller:
    current_owner: string
    future_owner: string
    status: pending | migrated
    removal_slice_or_condition: string
```

Do not leave caller ownership ambiguous or add a silent fallback. Every
retained legacy route must name its caller, reason, future owner, and removal
condition. Keep validation and independent review focused on the scenario owned
by the slice; final range validation remains separate.

Derive slice count from independently useful ownership, behavior, validation,
and rollback boundaries. Never choose a fixed slice count in advance. When a
slice is clearly oversized, record a smaller-alternative analysis before
accepting the larger boundary.

## One Implementation Slice Per Invocation

For CCFG-26 through CCFG-29, one `work-batch` invocation must:

1. consume the current queued or active runway and its existing durable state;
2. execute exactly the next incomplete implementation slice;
3. complete worker implementation, focused validation, independent review,
   any already-authorized correction, commit, receipt, execution-ledger update,
   and completed-slice archive for that slice;
4. stop before beginning another implementation slice; and
5. leave the next incomplete ledger row for a later explicit `work-batch`
   invocation, which resumes from the existing durable state.

Progress across those explicit invocations is established from existing
planning artifacts, receipts, execution-ledger records, and Git evidence. It
adds no candidate runtime state, and it creates no runtime communication,
synchronization, or shared execution state between stable and candidate.

This is an instruction boundary only. It adds no launcher, automatic
continuation, execution-unit protocol, state field, transition, receipt type, or
telemetry. Existing final validation, finalization, same-batch closeout, and the
no-successor-selection rule retain their current owners and behavior.

## Bounded Read-Only Recovery Advice

Before escalating an ambiguous blocker that appears mechanical, the coordinator
may consult the existing read-only `codebase_investigator` exactly once. The
investigator remains unchanged and advisory.

The bounded question may include only the active slice, stop condition, failing
command or evidence, current diff and worktree facts, and the proposed smallest
recovery. The coordinator may continue only when the suggested recovery is
already authorized by the active runway and existing recovery contract, such as
a command invocation correction, exact retry, environment or cache repair,
refreshed diff or review basis, or already-authorized in-slice repair.

Stop for user direction or a reviewed amendment when recovery would expand
scope, reclassify validation, change semantics, weaken safety, perform
destructive work, add a lifecycle surface, choose among multiple material
options, or proceed without enough evidence.

The investigator cannot edit, approve, commit, delegate, select, amend, or grant
recovery authority. The coordinator retains every proceed, stop, recovery,
acceptance, commit, closeout, and successor decision.

## Removal Condition

CCFG-29 must remove this policy and its root `AGENTS.md` hook only after the
integrated candidate proves equivalent vertical planning, one-slice execution,
bounded recovery escalation, and no-successor behavior. Remove the focused
regression test only after equivalent candidate scenarios pass.
