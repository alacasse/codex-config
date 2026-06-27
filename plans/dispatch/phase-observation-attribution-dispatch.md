batch_id: phase-observation-attribution
source_program_ledger: plans/codex-config-architecture-program-runner-findings.md
included_findings:
  - id: APR-20
    title: Phase Observation attribution is incomplete
excluded_findings:
  - id: APR-21
    reason: Input Inventory existence and schema enforcement is consumed-input contract work, not runner-observed launch/session attribution.
  - id: APR-22
    reason: Planning Root and Plan Archive migration is documentation/filesystem migration work, separate from runner phase observation.
goal: Give Phase Observation exact runner-launched session attribution without broad transcript reconstruction while preserving existing telemetry, manifest, CLI, and receipt behavior.
concept_owner_seam: Introduce scripts/architecture_program_runner_phase_observation.py as the single owner for observed phase execution metadata: exit/stdout/stderr sizes, exact Codex session id parsing, exact session JSONL path discovery, and metadata handed to telemetry writers.
validation_class: mechanical production refactor; focused observation/artifact/run-loop tests with synthetic session logs plus dry-run smoke; no live nested Codex required.
guardrails:
  - Preserve current CLI arguments, command flags, phase-result schema, receipt equality, expected receipt paths, final Run Summary shape, and direct script execution.
  - Preserve Phase Environment ownership for launch/prompt facts and subprocess env construction.
  - Preserve Phase Contract ownership for prompt obligations and allowed outputs.
  - Preserve artifacts ownership for manifest and telemetry file writing; Phase Observation should supply observed metadata, not own manifest persistence.
  - Use only exact session attribution: parse an explicit session UUID or path from codex exec output and resolve a unique matching JSONL path under the effective CODEX_HOME or default Codex home.
  - Do not infer sessions by prompt text search, newest file heuristics, broad session-log reconstruction, or copied prompt matching.
  - Missing session attribution remains non-fatal and must continue to produce telemetry with token_summary.status=missing.
  - Do not implement Input Inventory schema validation, worker/reviewer attribution, hard context-stop behavior, or Planning Root migration in this batch.
dependencies_satisfied:
  - Phase Environment now supplies launch and prompt context separately from observation.
  - Phase Contract now owns per-phase obligations separately from prompt rendering.
  - Artifact telemetry already records direct runner measurements and parses token_count events when an exact session JSONL path is supplied.
  - CONTEXT.md defines Phase Observation as runner-recorded facts about launching and monitoring one Phase.
dependencies_blocking:
  - None for spec creation.
suggested_slices:
  - Characterize current Phase Observation attribution boundaries with focused tests for exact UUID parsing, missing token data, and synthetic session JSONL summaries.
  - Introduce a Phase Observation concept owner for exact execution metadata and session path discovery.
  - Route execute_codex_phase through the observation owner while preserving subprocess env, output-last-message handling, and existing telemetry writes.
  - Tighten telemetry and facade compatibility tests so artifacts consume observation metadata without broad session reconstruction.
stop_conditions:
  - Stop if implementation requires live nested Codex execution for validation.
  - Stop if attribution depends on scanning session logs for prompt text, selecting newest session files, or guessing from unrelated transcripts.
  - Stop if missing session attribution becomes fatal or suppresses phase/run telemetry artifacts.
  - Stop if env override values are written to telemetry, prompts, manifests, dry-run output, or test snapshots.
  - Stop if the phase-result schema, receipt contract, command flags, dry-run output semantics, or final Run Summary shape changes.
expected_spec_path: plans/codex-config-architecture-program-runner-phase-observation-attribution-runway.md
