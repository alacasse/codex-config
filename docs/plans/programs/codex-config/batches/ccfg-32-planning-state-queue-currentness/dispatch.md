# CCFG-32 Planning-State Queue Currentness Dispatch

## Selection

- Batch ID: `ccfg-32-planning-state-queue-currentness`
- Source ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-32, Make Planning State authoritative for queue
  currentness.
- Source packet:
  `docs/plans/programs/codex-config/findings/github-issue-55-planning-state-queue-currentness.md`
- Authoritative external evidence at intake: GitHub issue #55, authored by the
  repository owner and labeled `ready-for-agent` on 2026-07-14.
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-32-planning-state-queue-currentness/runway.md`

## Goal And Owner Seam

Make Planning State `current` and `validate` the sole authority for selected or
queued batch currentness. Delete Git-derived queue-transaction paths, commit-
range archaeology, worktree classification, and planning-file fingerprints
from the temporary cross-checkout bridge.

Retain `preflight_cross_checkout_live_lease(...)` only as the named
`work-batch` first-handoff check for material repository identity, expected
implementation baseline, strict parsing, generation/Codex-home binding, and
movement during preparation. Retain
`prepare_cross_checkout_context_refresh(...)` for later handoffs after accepted
coordinator commits. Both APIs remain temporary until CCFG-29 final integration.

## Batch Boundary

- Batch kind: `destructive-cleanup`.
- Slice 1 risk: `contract-narrowing`; remove the queue-currentness API input,
  helper machinery, workflow obligations, and tests that preserve Git-derived
  planning semantics.
- Approval gate: the repo-owner-authored issue #55 and its ingested
  `ready-for-agent` state authorize this narrowing. Before execution, Planning
  State must still report this exact runway as the sole queued or active batch,
  CCFG-32 must remain `Pending`, and no amendment, supersession, abandonment,
  or source change may have withdrawn the authorization.
- Dependencies: none.
- Validation class: `project-harness-production` using temporary Git repository
  behavior tests, lifecycle ownership guards, manifest/installation routing
  checks, Ruff, basedpyright, and `git diff --check`.
- Execution topology: ordinary single-root work in this repository. Editing the
  temporary cross-checkout bridge does not make this batch a strict cross-
  checkout handoff and does not require a planning snapshot.

## Slice Shape

`slice_shape`: one slice. Helper deletion, workflow-contract narrowing,
behavioral test migration, release metadata, and changelog share one owner,
risk, validation, rollback, and acceptance boundary. Splitting them would leave
an invalid intermediate in which installed workflow prose and the helper API
disagree.

## Included Surfaces

- `scripts/cross_checkout_context.py`
- `skills/work-batch/SKILL.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/execute-spec.md`
- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execute-recovery-v1.md`
- `tests/test_cross_checkout_context.py`
- `tests/test_batch_lifecycle_guards.py`
- `tests/test_codex_features_manifest.py`
- `codex-features.json`
- `CHANGELOG.md`

## Guardrails

- Planning State alone decides selected/queued identity, current dispatch and
  runway scope, amendment/replacement/supersession/abandonment, and whether
  execution may consume the plan.
- Delete `queue_transaction_paths`, canonical-planning path classification,
  planning-snapshot-to-live commit-range path collection, worktree path
  combination, file fingerprints, and helpers/imports used only by them.
- Preserve the three-field `ready | blocked` result and fail-closed mechanical
  preparation; it no longer expresses queue or batch lifecycle currentness.
- Preserve strict parsing, exact roots, generation and active `CODEX_HOME`,
  expected implementation baseline, current toolchain/planning revisions,
  movement-during-preparation rejection, per-handoff leases, write-scope
  validation, verified result echo, accepted-action receipts, and reviewer diff
  bases.
- Name `work-batch` as the current startup caller and CCFG-29 final integration
  as the removal condition for both retained temporary helper APIs.
- Combined production-helper and reusable workflow-contract code must have a
  negative line delta.
- Do not add transaction IDs, digests, branch fields, planning schemas,
  movement taxonomies, scanners, compatibility versions, lifecycle states,
  agents, public commands, or durable artifacts.
- Preserve unrelated dirty files and exclude them from staging, cleanup,
  rewrites, and commits.

## Deferred Findings

- CCFG-21 owns future planning-artifact schema and validator work.
- CCFG-25 owns future planning-command and planning-transaction redesign.
- CCFG-29 alone owns deletion of the complete temporary cross-checkout bridge.
- CCFG-2 through CCFG-6, CCFG-9 through CCFG-11, and CCFG-22 through CCFG-28
  remain open or backlog work outside this batch.
- Historical CCFG-30 and CCFG-31 artifacts remain immutable evidence.

## Stop Conditions

Stop before implementation if Planning State cannot prove this exact queued
scope; the deletion authorization is withdrawn; a preserved material handoff
check would weaken; implementation movement without an accepted prior action
could become ready; the complete bridge would be deleted; a new planning-
currentness schema or compatibility path becomes necessary; the combined
production/contract line delta is not negative without explicit user approval;
or historical, candidate, installed-runtime, or out-of-scope paths would need
modification.
