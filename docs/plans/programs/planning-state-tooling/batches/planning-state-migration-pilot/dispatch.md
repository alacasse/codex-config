# Planning-State Migration Pilot Dispatch

```yaml
batch_id: planning-state-migration-pilot
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-5
    title: Existing planning roots need migration without losing human readability
excluded_findings:
  - id: PST-6
    reason: SQLite remains deferred until canonical Markdown plus explicit JSON state migration is proven.
goal: Add a project-neutral migration pilot that can bootstrap explicit planning-state JSON from existing Layout v1 Markdown roots while preserving human-readable CURRENT, LEDGER, dispatch, runway, closeout, and completed-slices artifacts.
owner_seam: scripts/planning_state.py remains the workflow facade; split small owner helpers only when migration parsing, state rendering, or validation would otherwise make the facade hard to review.
validation_class: focused migration/bootstrap tests, planning-state CLI checks, Markdown fixture round-trip checks, and ruff on touched Python files.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - Read root and program CURRENT.md before ledgers or historical plans.
    - Preserve redirect ledgers as warnings, not active state sources.
    - Bootstrap registered artifact facts from co-located batch directories and ledger rows without rewriting live Markdown.
    - Treat this dispatch/runway pair as the queued planning-state batch.
secondary_fixture:
  project: Graphify-style Layout v1 fixture
  planning_root: test temp root
  expected_resolution:
    - Use project-neutral Layout v1 paths and fixture data.
    - Preserve active-first pickup over stale flat files, redirect ledgers, and historical dispatch/runway filenames.
    - Do not require Graphify-specific production branches, cache paths, validation commands, or local overlays.
migration_contract:
  - Markdown remains human-readable and canonical for planning artifacts.
  - Explicit JSON state is a tool-owned companion state that can be regenerated from Markdown and receipts.
  - Migration writes only to an explicit caller-provided state/receipt target; dry-run output writes nothing.
  - Generated state must validate through the existing planning-state fixture schema and current/validate state-file checks.
  - Migration must not rewrite CURRENT.md, LEDGER.md, dispatch.md, runway.md, closeout.md, or completed-slices.md.
  - Historical flat files and redirects may produce warnings but must not become selected or queued work.
guardrails:
  - SQLite is out of scope.
  - No live planning Markdown is rendered or rewritten from tool state.
  - No Graphify-specific paths or validation commands are hard-coded into generic code.
  - Existing Markdown-only roots keep working when no planning-state JSON exists.
  - Migration output stays bounded; logs, transcripts, and broad archive inventories belong outside the state fixture.
dependencies_satisfied:
  - PST-1 read-only current and validate diagnostics exist.
  - PST-2 path allocation and artifact registration commands exist.
  - PST-3 obligation facts exist in explicit state fixtures and transition receipts.
  - PST-4 closeout validation/rendering and bounded closeout evidence are available.
  - PST-7 command/file protocol boundary exists for runner interop.
dependencies_blocking:
  - None for a migration pilot based on explicit state files and fixtures.
suggested_slices:
  - Define the migration bootstrap contract and fixture expectations.
  - Add dry-run and explicit-target bootstrap state generation.
  - Validate migrated state against codex-config and Graphify-style Layout v1 fixtures.
  - Document the migration pilot workflow and update active planning state after execution.
stop_conditions:
  - The batch would need SQLite or a durable query database.
  - The batch would need to rewrite Markdown planning artifacts from generated state.
  - The batch would need to infer active state from historical flat filenames instead of CURRENT.md and explicit ledger rows.
  - The batch would need Graphify-specific production paths, validation commands, cache paths, or overlays.
  - A durable state-file location for real migration output is required but not explicitly provided by the caller or spec.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/runway.md
```
