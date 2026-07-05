# Planning-State SQLite Projection Dispatch

```yaml
batch_id: planning-state-sqlite-projection
status: deferred
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-6
    title: Operational queries are awkward from files alone
excluded_findings: []
goal: Add an optional, rebuildable SQLite projection and compact report commands for planning-state operational questions while preserving Markdown and JSON state as the canonical workflow record.
owner_seam: scripts/planning_state.py remains the workflow facade; split small projection/schema/report helpers only if they keep the facade reviewable and project-neutral.
validation_class: focused SQLite/report tests, planning-state CLI checks, dry-run rebuild/report checks against temp fixtures, and ruff on touched Python files.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - Read root and program CURRENT.md before ledgers or historical plans.
    - Bootstrap explicit planning-state JSON from Markdown before any projection rebuild that needs state facts.
    - Rebuild reports from canonical Markdown, JSON state, closeout evidence, receipts, and runner artifacts when provided.
    - Treat this dispatch/runway pair as the queued planning-state batch.
secondary_fixture:
  project: Layout v1 temp root with runner-style artifacts
  expected_resolution:
    - Use project-neutral fixture data for receipts, telemetry summaries, closeout evidence, selected/queued state, and missing evidence.
    - Do not hard-code Graphify paths, cache locations, validation commands, or local overlays.
    - Deleting the SQLite database must not affect current/validate behavior or canonical state recovery.
projection_contract:
  - SQLite is optional, rebuildable, and safe to delete.
  - SQLite stores only paths, metadata, compact summaries, statuses, timestamps, durations, phase names, warning/error codes, hashes, and bounded evidence pointers.
  - SQLite must not store canonical ledger prose, full dispatch/runway text, closeout decisions, prompts, transcripts, long logs, or raw telemetry payloads.
  - Agents use planning-state commands and compact report output, not SQL or direct database mutation.
  - Projection rebuild writes only to an explicit database target or an explicit temp/output target chosen by the caller or spec.
  - Report commands must reject stale or mismatched projections instead of silently trusting a database built from another planning root or state fixture.
guardrails:
  - Markdown and JSON remain canonical.
  - Do not require SQLite for active-state resolution, validation, selection, queueing, closeout validation, or bootstrap-state.
  - Do not render or rewrite CURRENT.md, LEDGER.md, dispatch.md, runway.md, closeout.md, or completed-slices.md from SQLite.
  - Do not make downstream runners import scripts.planning_state internals.
  - Do not expose SQL as the normal agent workflow interface.
  - Do not add project-specific report branches for Graphify or any other downstream project.
dependencies_satisfied:
  - PST-1 read-only current and validate diagnostics exist.
  - PST-2 artifact allocation and registration commands exist.
  - PST-3 obligations are explicit state facts.
  - PST-4 closeout evidence is bounded and validateable.
  - PST-5 bootstrap-state can generate companion JSON state from Layout v1 Markdown.
  - PST-7 command/file protocol boundary exists for runner interop.
dependencies_blocking:
  - planning-state-project-policy must close first so SQLite consumes resolved project state/projection policy instead of choosing target ownership.
suggested_slices:
  - Define the SQLite projection contract, schema metadata, stale-database checks, and allowed report facts.
  - Add an explicit projection rebuild command that writes only to a caller-provided SQLite target.
  - Add compact report commands for pending batches, missing closeout evidence, and batch artifact/evidence lookup.
  - Add runner-artifact report coverage for latest run, failed phases by reason, and context pressure summaries when runner artifacts are present.
  - Document the projection workflow and close PST-6 with bounded evidence.
stop_conditions:
  - The batch would make SQLite canonical or required for current/validate/bootstrap/closeout behavior.
  - The batch would need to store long logs, prompts, transcripts, or full Markdown prose in SQLite.
  - The batch would need to infer active state from historical flat filenames instead of CURRENT.md and explicit state facts.
  - The batch would need a durable database location not allowed by resolved project policy.
  - The batch would need to choose state-file or projection ownership before PST-8 closes.
  - The batch would need project-specific production paths, cache paths, validation commands, or local overlays.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/runway.md
```
