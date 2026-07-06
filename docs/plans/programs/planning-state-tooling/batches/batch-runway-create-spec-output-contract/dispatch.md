# Batch Runway Create-Spec Output Contract Dispatch

```yaml
batch_id: batch-runway-create-spec-output-contract
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-18
    title: Batch Runway create-spec writes session-local mode into durable overrides
excluded_findings:
  - id: PST-19
    title: Findings lack a Pending status for cut or active batch work
    reason: Separate lifecycle-vocabulary work; do not widen this batch into finding-state modeling.
goal: Keep session-local create-spec history out of durable Batch Runway execution-contract Overrides, add focused regression coverage, and deliberately clean or document affected active/future runway artifacts.
owner_seam: Batch Runway owns create-spec output contracts and durable runway structure; Planning State only reports selected, queued, and active artifacts and must not encode Batch Runway mode semantics.
validation_class: Batch Runway skill/reference wording tests, focused regression checks for durable Overrides, current/validate diagnostics, bounded grep for affected runways, manifest/changelog alignment when workflow behavior changes, and git diff --check.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `current` and `validate` report this batch as the queued planning-state-tooling batch after this dispatch/runway pair is selected.
    - The queued runway does not store create-spec session history in `Overrides`.
    - Planning-state diagnostics remain read-only and do not learn Batch Runway mode rules.
secondary_fixture:
  project: Batch Runway reusable skill
  expected_resolution:
    - `skills/batch-runway/references/create-spec.md` tells agents that `Overrides` is only for durable execution-contract deviations.
    - Regression coverage fails when create-spec guidance or active/future runway specs put session-local mode claims into durable `Overrides`.
durable_override_contract:
  - `Overrides` belongs to execution-time deviations from Batch Runway Standard Execution Contract v1.
  - Session mode, artifact creation history, and "implementation starts later" notes belong in baseline, handoff, or active-state context, not in durable execution `Overrides`.
  - Create-spec mode can be named in prose where it explains the current task, but not as an execution-contract override.
  - Closed historical specs may be left as historical evidence only after a bounded scan proves they are not active or future templates.
guardrails:
  - Do not change `scripts/planning_state.py` for this finding.
  - Do not introduce project-specific paths, validation commands, cache paths, or downstream planning roots into generic Batch Runway guidance.
  - Do not retroactively widen PST-18 into Pending-status lifecycle modeling; PST-19 owns that work.
  - Do not mass-edit closed historical runways unless the execution pass explicitly classifies them as reusable templates or active/future artifacts.
dependencies_satisfied:
  - `planning-state-projection-consumers` is completed and has closeout evidence.
  - The planning-state diagnostic reports no active or queued planning-state-tooling batch before this dispatch was created.
dependencies_blocking:
  - None for PST-18.
suggested_slices:
  - Tighten Batch Runway create-spec guidance so durable `Overrides` excludes session-local mode and creation-history claims.
  - Add focused regression coverage for the durable override contract and align workflow metadata/changelog if the skill behavior surface changes.
  - Audit and deliberately clean or document affected active/future runway artifacts, then close PST-18 with pointer-first evidence.
stop_conditions:
  - The work would move create-spec mode semantics into planning-state diagnostics or JSON state.
  - The work would redefine the full Batch Runway execution contract instead of tightening the create-spec output contract.
  - The work would edit PST-19 lifecycle status vocabulary or use Pending as a durable finding state without that separate batch.
  - The work would require downstream project-specific fixture paths in reusable skill guidance or tests.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/runway.md
```
