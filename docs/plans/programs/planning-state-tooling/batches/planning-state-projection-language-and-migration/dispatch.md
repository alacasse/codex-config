# Planning-State Projection Language And Migration Dispatch

```yaml
batch_id: planning-state-projection-language-and-migration
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-20
    title: Agent-facing SQLite language still makes normal projection reporting sound optional
  - id: PST-21
    title: Existing ledger workflows need a reusable projection-reporting adoption migration
excluded_findings:
  - id: PST-6
    title: Operational queries are awkward from files alone
    reason: Already closed by the SQLite projection command/report implementation; this batch is consumer-facing wording and migration adoption.
  - id: PST-14
    title: Projection routing is implemented but not part of the routine interface
    reason: Already closed by projection-routing facts; this batch tightens how agents and project roots adopt that route.
  - id: PST-16
    title: Consumer skills consume active-state diagnostics but not projection reports
    reason: Already closed by consumer routing; this batch fixes remaining ambiguity and adoption gaps.
goal: Make projection-backed reporting read as the policy-gated normal workflow for supported history/reporting questions, then document a reusable adoption checklist for existing Layout v1 ledger roots without making SQLite canonical or project-specific.
owner_seam: Planning State owns projection-reporting policy, command/report boundaries, and reusable adoption guidance; Batch Runway, Architecture Program Runway, and Legacy Removal consume command output without querying SQLite directly; project overlays own durable projection paths and downstream validation commands.
validation_class: Workflow-skill wording tests, consumer-obligation tests, project-policy fixture tests for generated-only and ignored-local projection routing, migration checklist/readback validation, current/validate diagnostics, changelog/manifest alignment when behavior surfaces change, and git diff --check.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `current` and `validate` report this batch as the queued planning-state-tooling batch.
    - Projection language preserves SQLite-independent active-state pickup.
    - Generated-only projection policy uses explicit caller-provided temporary targets.
secondary_fixture:
  project: reusable Layout v1 root fixture
  expected_resolution:
    - Ignored-local projection policy can declare a durable local projection path without hard-coding that path into generic skills.
    - Adoption guidance inventories CURRENT.md files, ledgers, queues, redirects, consumer skills, installed-skill state, and overlays.
    - Agents still consume `rebuild-projection` and `report-projection` command output rather than SQL or table names.
guardrails:
  - Do not make SQLite canonical planning state.
  - Do not require SQLite for `current`, `validate`, active-state pickup, batch allocation, transition commands, or closeout validation.
  - Do not add a generic durable database default.
  - Do not query SQLite directly from workflow skills or agent guidance.
  - Do not hard-code downstream project paths, validation commands, cache paths, or local planning roots into reusable skills.
  - Do not edit installed `~/.codex` paths directly unless ownership is checked and repo-owned changes are made through this repo.
dependencies_satisfied:
  - `planning-state-projection-routing` is closed.
  - `planning-state-projection-consumers` is closed.
  - `planning-state-finding-pending-status` is closed and supports Pending finding lifecycle state.
  - Baseline `current` and `validate` diagnostics pass for `docs/plans/`.
dependencies_blocking:
  - None for PST-20/PST-21.
suggested_slices:
  - Tighten projection language across Planning State and consumer skills so supported history/reporting questions use policy-compatible projection reports as the normal route while preserving active-state independence.
  - Add regression coverage for the wording and policy boundaries, including generated-only temp targets and ignored-local fixture policy.
  - Add a reusable adoption checklist for existing Layout v1 ledger roots and prove it against codex-config plus a non-codex-config fixture shape.
  - Reconcile feature metadata, changelog, and planning closeout state with pointer-first evidence.
stop_conditions:
  - The work would make SQLite a canonical backing store or required active-state dependency.
  - The work would expose SQL/table names as an agent workflow contract.
  - The work would choose a durable projection path without project policy.
  - The work would add downstream-project-specific defaults to generic reusable skills.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/runway.md
```
