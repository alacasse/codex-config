batch_id: runner-boundary-split
source_program_ledger: plans/codex-config-architecture-program-runner-findings.md
included_findings:
  - id: APR-11
    title: architecture_program_runner.py concentrates too many responsibilities
  - id: APR-12
    title: tests mirror the large runner file as one broad suite
  - id: APR-13
    title: structured failure paths do not refresh manifests consistently
excluded_findings:
  - id: APR-9
    reason: telemetry attribution should wait until telemetry helpers have a clear owner seam
  - id: APR-10
    reason: input inventory validation should wait until telemetry/artifact seams are easier to extend
  - id: APR-14
    reason: planning-doc cleanup should follow functional runner seams
  - id: APR-15
    reason: codex_owner.py is not the current architecture hotspot
goal: Split architecture_program_runner internals into testable owner seams while preserving the public CLI and runner protocol.
owner_seam: scripts/architecture_program_runner.py and tests/test_architecture_program_runner.py
validation_class: stdlib unit tests plus CLI/dry-run smoke; no live nested Codex required for the refactor batch
guardrails:
  - Keep scripts/architecture_program_runner.py as the installed CLI entrypoint.
  - Preserve the phase-result schema and required receipt fields.
  - Preserve structured artifact paths under architecture-program-runs/<ledger-stem>/<run-id>/.
  - Preserve the single-level phase model and execute-only sandbox override behavior.
  - Do not add project-specific Graphify validation or cache logic.
dependencies_satisfied:
  - Current focused tests pass: python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q.
  - Current commits already closed schema, env, execute-sandbox, single-level phase, artifact-layout, and first-pass telemetry blockers.
dependencies_blocking:
  - None for spec creation.
suggested_slices:
  - Extract pure path/state helpers into a small module with focused tests.
  - Extract phase-result and receipt validation into a small module with schema-subset tests.
  - Extract prompt/command construction into a module while preserving exact prompt guardrails.
  - Extract artifact manifest and telemetry writing into modules; decide whether failure paths should refresh manifests.
  - Split tests to mirror the new owner seams and keep a thin CLI integration suite.
stop_conditions:
  - Stop if the refactor changes CLI arguments, final summary fields, phase-result schema, receipt path behavior, or artifact layout.
  - Stop if old flat-state resume compatibility becomes ambiguous.
  - Stop if the batch starts implementing exact session JSONL discovery or input inventory schema work instead of only creating seams.
  - Stop if validation requires a live nested Codex run; use mocks and dry-run smoke for this refactor batch.
expected_spec_path: plans/codex-config-architecture-program-runner-boundary-split-runway.md
