# Planning-State Projection Consumers Dispatch

```yaml
batch_id: planning-state-projection-consumers
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-16
    title: Consumer skills consume active-state diagnostics but not projection reports
  - id: PST-17
    title: Tests protect projection commands but not workflow obligations
excluded_findings: []
goal: Wire Batch Runway, Architecture Program Runway, and Legacy Removal so supported history/reporting workflows try policy-compatible planning-state projection reports before broad historical scans, and add focused regression checks for that consumer-facing obligation.
owner_seam: `skills/planning-state/SKILL.md` and `skills/planning-state/references/projection-reporting.md` own projection-report policy; consumer skills own when their workflow needs history/reporting context and how they preserve their own semantic decisions.
validation_class: consumer skill wording tests, feature metadata/version checks when workflow docs change, focused grep checks across consumer skills, planning-state current/validate diagnostics, and `git diff --check`.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `current` and `validate` remain the first active-state pickup commands.
    - This dispatch/runway pair is treated as the queued planning-state batch until execution closes it.
    - Projection reports remain advisory history/reporting inputs, not active-state authority.
secondary_fixture:
  project: consumer skill documentation fixtures
  expected_resolution:
    - Batch Runway, Architecture Program Runway, and Legacy Removal each name projection-report routing for supported history/reporting questions.
    - Regression tests fail if a consumer keeps only active-state diagnostic guidance and omits projection-report obligations.
projection_consumer_contract:
  - Active-state pickup still starts with `planning-state current` and `validate`.
  - Before broad historical Markdown scans, old flat planning-file scans, generated report reads, knowledge-graph queries, or source archaeology for supported history/reporting questions, consumers should check whether projection reports are policy-compatible.
  - Consumers read the planning-state projection-reporting reference before rebuilding or reporting projections.
  - Consumers use `rebuild-projection` and `report-projection` command output, not SQL or direct database mutation.
  - Missing, disabled, stale, external-owner, or policy-incompatible projections produce bounded blockers, warnings, or explicit fallback decisions.
  - Projection reports do not decide consumer-owned semantics such as slice scope, architecture grouping, legacy classification, compatibility decisions, validation routing, or commits.
guardrails:
  - Do not make SQLite required for active-state pickup, spec creation, batch selection, legacy classification, or closeout reconciliation.
  - Do not add a durable projection path as a generic default.
  - Do not add Graphify-specific paths, validation commands, cache paths, or local overlays to reusable skills or tests.
  - Do not modify downstream project planning roots.
  - Do not update GitHub issues or comments as part of this planning batch.
dependencies_satisfied:
  - `planning-state-projection-routing` added projection-aware diagnostic facts and policy vocabulary.
  - `planning-state` now documents projection-report routing and target policy.
  - Consumer features already depend on `planning-artifacts` and `planning-state`.
dependencies_blocking:
  - None for consumer routing.
suggested_slices:
  - Update Batch Runway projection-report routing for history/reporting questions and protect it with focused tests.
  - Update Architecture Program Runway projection-report routing for program history/reporting and closeout evidence questions and protect it with focused tests.
  - Update Legacy Removal projection-report routing for planning history/reporting questions while preserving evidence-based legacy decisions and protect it with focused tests.
  - Align workflow metadata, changelog entries, and final regression checks so PST-16 and PST-17 can close together.
stop_conditions:
  - The batch would make projection data canonical over Markdown or explicit JSON state.
  - The batch would require consumer workflows to rebuild SQLite for ordinary active-state pickup.
  - The batch would blur ownership by letting planning-state choose Batch Runway slices, architecture grouping, or legacy-removal compatibility decisions.
  - The batch would need downstream project-specific paths or validation commands in generic code.
  - The batch would mutate downstream project planning roots.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/runway.md
```
