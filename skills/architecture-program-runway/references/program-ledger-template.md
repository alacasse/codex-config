# Program Ledger Reconciliation Template

Use this template to interpret or reconcile an existing program ledger after a
concrete batch finishes. Public `plan-batch` owns all grouping, prioritization,
selection, dispatch, runway, approval, validation-profile, and queue decisions.
This template grants no planning or lifecycle authority before closeout.

````markdown
# <Area> Program Ledger

## Purpose

Keep durable findings and completed-batch evidence visible across executions.

## Current Direction

- <Guardrail or target direction>
- <Boundary that remains stable>
- <Public contract that needs explicit reclassification before change>

## Source Context

- Review source: `<path or summary>`
- Completed runways: `<paths>` or `None`
- Current baseline: `<commit or date>`
- Related ADRs/docs: `<paths>`

## Planning Layout

- Layout version: `Planning Artifact Layout v1` or `<project-specific value>`
- Planning root: `<path>`
- Program root: `<path>`
- Program current file: `<path to CURRENT.md or None>`
- Program archive root: `<path>`
- Run artifact root: `<path>`
- Output root: `<path>`

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| <id> | Open | None | <existing next action> | <compact evidence> |

## Existing Batch Artifacts

| Batch | Findings | State | Dispatch | Runway | Closeout |
|---|---|---|---|---|---|
| <batch-id> | <ids> | <selected, queued, active, completed, or blocked> | <path> | <path> | <path or None> |

This table observes existing artifacts. Only public `plan-batch` may select,
dispatch, create a runway, choose a validation profile, or apply the queue
transaction. Same-batch closeout may update only the just-completed row from
concrete evidence and must not prepare a successor.

## Completed Batch Evidence

- Batch: `<batch-id>`
- Dispatch: `<path>`
- Runway: `<path>`
- Closeout: `<path>`
- Commit range: `<range>`
- Validation: `<summary path or compact result>`
- Implementation review: `<result>`
- Completed slices: `<archive path>`
- Unresolved follow-ups: `<ids or None>`

## Legacy Removal Evidence

```yaml
legacy_surfaces:
  - surface: "<surface>"
    status: keep | delete-now | migrate-tests-first | keep-thin-entrypoint | human-contract-decision
    reason: "<caller, contract, or test evidence>"
    removal_condition: "<required for temporary retention or None>"
```

Consume the canonical deletion-test evidence statuses owned by
`dead-surface-audit`. If a project needs local non-canonical labels, define them
inline as labels only. They must not make unsupported generated terms behave as
approval gates, cleanup decisions, migration decisions, or contract-narrowing
decisions.

## Goal Run Evaluations

```yaml
- run_id: <stable-id>
  runner: </goal | automation | local-runner | manual>
  bounds:
    max_batches: <number>
  batches:
    observed:
      - <batch-id>
    completed: <number>
  stop_reason: <completed-bound | blocked | validation-failed | review-failed | dirty-file-conflict | permission-issue | user-stop | other>
  source_of_truth_check:
    planning_receipt_linked: <yes | no | partial>
    ledger_updated: <yes | no | partial>
    validation_evidence_linked: <yes | no | partial>
    review_result_linked: <yes | no | partial>
    commit_receipts_linked: <yes | no | partial>
  responsibility_check:
    plan_batch_owned_planning: <yes | no | partial>
    batch_runway_owned_execution: <yes | no | partial>
    architecture_program_runway_owned_same_batch_closeout_only: <yes | no | partial>
    implementation_review_delegation_unchanged: <yes | no | partial>
```

## Closeout Rules

- Run Planning State `current` and `validate` for the declared planning root.
- Read only the just-completed batch's completed-slice archive, commits,
  validation result, implementation review, and closeout evidence.
- Reconcile covered findings as `Closed`, `Prepared`, `Open`, `Pending`,
  `Split`, or `Superseded` only when the evidence supports that disposition.
- Record compact evidence links rather than logs or transcripts.
- Preserve unclassified legacy residue, deferred work, and blockers.
- Do not group, prioritize, select, dispatch, create or reshape a runway,
  mutate queue state, or prepare a successor.
- Route genuinely new findings through `add-to-ledger`.
- Require a later explicit public `plan-batch` invocation for successor work.
````

## Closeout Checklist

1. Run or consume Planning State `current` and `validate` diagnostics for the
   declared planning root.
2. For missing closeout evidence, runner summaries, or bounded history, read
   `../../planning-state/references/projection-reporting.md`. Use a
   policy-compatible `report-projection` command output as the normal route
   before broad historical scans when `projection_usage` and
   `projection_rebuild_authority` allow it. Record fallback decisions before scanning
   when policy is unavailable. Do not query SQLite directly.
3. Confirm the exact batch across dispatch, runway, closeout, archive, and
   receipts.
4. Confirm implementation, validation acceptance, independent review, commits,
   finalization, and closeout evidence.
5. Reconcile only the just-completed row and covered findings.
6. Preserve unresolved findings and cleanup residue without selecting them.
7. Stop before successor preparation or selection.
