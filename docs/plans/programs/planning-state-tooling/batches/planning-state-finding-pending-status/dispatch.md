# Planning-State Finding Pending Status Dispatch

```yaml
batch_id: planning-state-finding-pending-status
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-19
    title: Findings lack a Pending status for cut or active batch work
excluded_findings:
  - id: PST-18
    title: Batch Runway create-spec writes session-local mode into durable overrides
    reason: Closed by the previous batch; do not reopen closed override-contract work.
goal: Define and enforce a Pending finding status for work that has been cut into a dispatch or concrete runway but is not yet closed, superseded, abandoned, or explicitly amended.
owner_seam: Architecture Program Runway owns finding lifecycle vocabulary and source-ledger update rules; Batch Runway consumes selected dispatch/runway artifacts without widening finding scope; Planning State reports selected, queued, and active artifacts without owning finding semantics.
validation_class: Workflow-skill wording tests, ledger/template status-vocabulary checks, current/validate diagnostics, manifest/changelog alignment when workflow behavior changes, and git diff --check.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `current` and `validate` report this batch as the queued planning-state-tooling batch.
    - PST-19 is no longer raw `Open` intake once the dispatch/runway pair exists.
    - The queued shape uses only `queued_batch`; selected dispatch and active runway stay `None`.
secondary_fixture:
  project: Architecture Program Runway reusable skill
  expected_resolution:
    - Finding status vocabulary includes `Pending` as cut-or-active batch work controlled by batch artifacts.
    - Selection and closeout guidance forbids silent source-ledger scope edits for Pending findings.
    - Explicit amendments or follow-up findings remain allowed and visible.
pending_status_contract:
  - `Open` means a real finding that is not yet assigned to a selected, queued, or active runway.
  - `Pending` means a finding is controlled by selected, queued, or active batch artifacts and should not be widened by source-ledger edits.
  - Pending findings can move to `Closed`, `Prepared`, `Open`, `Split`, `Superseded`, `Abandoned`, or remain `Pending` only through closeout evidence, explicit abandonment, supersession, split, or a named amendment/follow-up.
  - Batch queue state remains separate from finding status; use `selected`, `queued`, `active`, and `completed` for batch artifacts.
guardrails:
  - Do not make Planning State commands own Architecture Program Runway finding semantics.
  - Do not introduce project-specific paths, validation commands, cache paths, or downstream planning roots into generic skills or tests.
  - Do not reopen PST-18 or edit closed historical runways except as bounded evidence if a regression test needs a fixture.
  - Do not silently mutate a Pending finding's source scope; use an explicit amendment note or a new finding.
dependencies_satisfied:
  - `batch-runway-create-spec-output-contract` is completed and closed PST-18.
  - Baseline `current` and `validate` diagnostics pass for `docs/plans/`.
dependencies_blocking:
  - None for PST-19.
suggested_slices:
  - Define Pending finding lifecycle vocabulary in Architecture Program Runway guidance and the program ledger template.
  - Add focused docs-as-code regression coverage and align workflow metadata for the new reusable skill behavior.
  - Reconcile planning-state-tooling ledger/current state, validate the queued/closed transitions, and close PST-19 with pointer-first evidence.
stop_conditions:
  - The work would make Pending a Planning State command-owned status instead of an Architecture Program Runway finding lifecycle status.
  - The work would collapse batch artifact state and finding lifecycle state into one vocabulary.
  - The work would silently broaden the source scope of a Pending finding instead of recording an amendment or follow-up.
  - The work would add downstream project-specific paths or validation commands to reusable guidance or tests.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/runway.md
```
