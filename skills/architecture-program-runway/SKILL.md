---
name: architecture-program-runway
description: Agent-facing same-batch program closeout reconciliation used by work-batch after concrete execution evidence exists.
---

# Architecture Program Runway

Agent-facing support for `work-batch` same-batch closeout reconciliation. This
skill does not plan batches. The public `plan-batch` command owns finding
selection, proportional scope, dispatch and runway creation, independent
planning review, approvals, validation-profile selection, and the DEC-038 queue
transaction.

Use `../planning-artifacts/SKILL.md` for Planning Artifact Layout v1 placement
and `../planning-state/SKILL.md` for Diagnostic-First Pickup, current/validate
ordering, target-policy checks, and projection routing. Those support skills
provide layout and read-only operational facts; they do not grant this skill
planning or queue authority.

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: architecture-program-runway
  audience: support-mechanism
producer:
  toolchain_generation: candidate
  toolchain_commit: 5cb0e6cfccc2aba6f18a011651619157c637af28
  schema_version: skill-contract/v1
purpose: >-
  Reconcile one just-completed batch into its existing program ledger from
  concrete execution, validation, review, commit, and closeout evidence.
owns:
  decisions:
    - same_batch_closeout_disposition
    - program_lifecycle_reconciliation
  durable_facts:
    - finding_lifecycle_state
    - completed_batch_reconciliation
reads:
  required:
    - planning_state_diagnostic
    - existing_program_ledger
    - completed_batch_evidence
  conditional:
    - completed_slice_archive
    - validation_and_review_evidence
    - commit_receipts
writes:
  - program_lifecycle_mutation
  - same_batch_closeout_reconciliation
requires:
  mechanisms:
    - planning-artifacts
    - planning-state
  evidence_skills: []
delegates: []
forbids:
  - finding_intake
  - source_canonicalization
  - finding_normalization
  - atomic_planning_finding_mutation
  - finding_grouping
  - finding_prioritization
  - finding_sequencing
  - batch_selection
  - selected_dispatch_mutation
  - queue_state_mutation
  - runway_creation
  - successor_selection
  - implementation
outputs:
  one_of:
    - same_batch_reconciliation_result
    - closeout_blocker
stops_when:
  - completed_batch_evidence_is_missing
  - planning_state_is_ambiguous
  - requested_change_exceeds_same_batch_closeout
  - successor_work_would_be_selected
references: []
```

## Boundary

This skill consumes only an existing, just-completed batch. It may reconcile
that batch's existing ledger row and covered findings from concrete evidence.
It must not group open findings, rank work, choose a next batch, create or
refresh a selected dispatch, prepare a queue transaction, create a runway, or
alter successor state.

When closeout reveals genuinely new work, stop and route the finding through
`add-to-ledger`. When successor planning is requested, stop and invoke public
`plan-batch` in a later command. Neither route may be hidden inside closeout.

## Required First Steps

1. Read applicable repository instructions and local overlays.
2. Use Planning State Diagnostic-First Pickup for the declared planning root;
   require `current` and `validate` to identify the same active or just-completed
   batch and safe reconciliation target.
3. Use Planning Artifacts to resolve the existing program ledger, batch
   directory, closeout location, and archive paths. Do not invent a planning
   layout.
4. Read only compact evidence for the just-completed batch: completed-slice
   archive, commit receipts, validation result, implementation review, closeout
   artifact, and unresolved follow-ups.
5. Check the worktree and preserve unrelated files.
6. Run only `closeout-runway` mode.

For missing closeout evidence, runner summaries, or bounded history questions,
read `../planning-state/references/projection-reporting.md` and use
policy-compatible `report-projection` command output as the normal route before
broad historical scans when `projection_usage` and
`projection_rebuild_authority` allow it. Missing or incompatible policy needs
an explicit fallback decision before scanning. Do not query SQLite directly.
Projection output is read-only context; it must not select batches, replace
program ledgers, create dispatches or runways, or close findings by itself.

## Mode

`closeout-runway` reconciles the just-completed batch only. It may:

- record the exact batch, dispatch, runway, commit range, validation result,
  implementation review, and closeout evidence;
- mark covered findings `Closed`, `Prepared`, `Open`, `Pending`, `Split`, or
  `Superseded` when that disposition is supported by completed evidence;
- update the existing batch row to its completed or explicitly unresolved
  closeout disposition; and
- preserve unresolved or deferred work without selecting it.

It must not clear a queued or active batch before execution, treat a
dispatch/runway pair as closeout evidence, or mutate selected/queued/successor
state. When invoked from `work-batch`, it is part of that command's closeout and
must return control to `work-batch` after same-batch reconciliation.

## CCFG-26 Execution Preservation

This narrowing does not own or remove execution behavior. Preserve the current
`work-batch` and Batch Runway surfaces for:

- proceed and stop decisions;
- worker and reviewer delegation;
- recovery and resume;
- validation execution and acceptance;
- implementation review coordination;
- commits and commit receipts;
- execution-ledger state and per-slice evidence;
- finalization and closeout artifact production;
- same-batch reconciliation and no-successor enforcement; and
- strict cross-checkout execution safety.

This skill consumes their completed evidence. It does not duplicate or weaken
those responsibilities.

## Ledger Dispositions

Keep finding lifecycle status separate from selected, queued, active, and
completed batch artifact state:

- `Open`: real finding not controlled by the completed batch.
- `Ready`: existing near-term work that closeout must not select.
- `Pending`: existing work still controlled by an unresolved current batch.
- `Blocked`: waiting on a named decision or dependency.
- `Prepared`: evidence or seams improved, but production work remains.
- `In runway`: still covered by an active concrete runway.
- `Closed`: implementation, validation, review, and closeout are complete.
- `Superseded`: made irrelevant by another accepted change.
- `Split`: decomposed through an explicit authorized lifecycle decision.

Do not mark a finding `Closed` merely because a spec or commit exists. Require
the full completion evidence. Do not widen a `Pending` finding during closeout.
New scope goes through `add-to-ledger`; successor selection goes through a later
public `plan-batch` invocation.

## Closeout Procedure

1. Confirm the same batch identity across Planning State, dispatch, runway,
   closeout, completed-slice archive, and receipts.
2. Confirm implementation, validation acceptance, independent review, commits,
   finalization, and closeout evidence are complete.
3. Reconcile each covered finding only from that evidence. Preserve blockers,
   prepared work, and unresolved cleanup residue explicitly.
4. Update only the existing program ledger/current facts needed to record the
   just-completed batch. Do not prepare a successor.
5. For legacy-removal work, record removed, retained, and deferred surfaces,
   including concrete reasons and removal conditions. Consume canonical
   deletion-test evidence statuses owned by `dead-surface-audit`; do not invent
   unsupported labels as approval, cleanup, migration, or contract-narrowing
   decisions.
6. Return a compact reconciliation result to `work-batch` and stop.

## Runner Compatibility

The local runner keeps the serialized phases `select-dispatch`, `create-spec`,
`execute`, and `closeout`, their receipts, and their transition graph. During
this compatibility period, `select-dispatch` invokes public `plan-batch` once
for the complete planning flight. `create-spec` only observes that completed
result and advances compatibility state; it performs no planning. `execute`
uses Batch Runway execution support. `closeout` uses this skill.

The two planning labels are temporary serialized compatibility labels. CCFG-27
owns their migration or removal decision; final physical cleanup is required by
CCFG-29 if CCFG-27 retains them. This skill must not reintroduce the old
planning modes behind either label.

For runner details, read `references/local-runner-v1.md`. For bounded goal
orchestration compatibility, read `references/goal-runner-v1.md`.

## Program Ledger Shape

Use `references/program-ledger-template.md` only to interpret or reconcile an
existing program ledger. The template records layout, findings, existing batch
artifact links, compact closeout evidence, and runner receipts. It does not
authorize this skill to plan or mutate queue state.

## Stops

- Stop if evidence does not identify one just-completed batch.
- Stop if implementation, validation, review, commit, finalization, or closeout
  evidence is missing or contradictory.
- Stop before selection, grouping, prioritization, dispatch/runway creation,
  queue mutation, successor preparation, or implementation.
- Stop if reconciliation would remove or alter a CCFG-26 execution surface.
- Stop if a new finding is needed; route it through `add-to-ledger`.
- Stop if successor planning is requested; route it through public
  `plan-batch` after closeout finishes.
