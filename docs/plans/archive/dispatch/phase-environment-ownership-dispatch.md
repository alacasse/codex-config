batch_id: phase-environment-ownership
source_program_ledger: plans/codex-config-architecture-program-runner-findings.md
included_findings:
  - id: APR-16
    title: Phase Environment lacks a concept owner
excluded_findings:
  - id: APR-17
    reason: Phase Transition should wait until phase launch and prompt context are named behind a stable owner.
  - id: APR-18
    reason: Change Allowance is path-policy work and should follow the environment owner unless it proves small enough to combine later.
  - id: APR-19
    reason: Phase Contract catalog work should use the Phase Environment owner but keep normative obligations separate.
  - id: APR-20
    reason: Phase Observation attribution depends on clearer phase environment and contract boundaries.
  - id: APR-21
    reason: Input Inventory contract enforcement is intentionally out of scope for this environment-owner batch.
  - id: APR-22
    reason: Planning Root and Plan Archive migration is documentation/filesystem migration work, separate from runner behavior refactoring.
goal: Create a clear Phase Environment concept owner for runner-supplied launch and prompt context while preserving Runner Facade behavior.
concept_owner_seam: scripts/architecture_program_runner_environment.py as the single owner for Phase Environment facts consumed by prompt, command, dry-run, sandbox, env override, and launch helpers.
validation_class: mechanical production refactor; focused command/environment/run-loop tests plus dry-run smoke; no live nested Codex required.
guardrails:
  - Preserve current CLI arguments, defaults, direct script execution, and importlib-based tests.
  - Preserve phase-result schema, required receipt path behavior, final Run Summary, and structured artifact paths.
  - Preserve env override secrecy: display keys only, never values.
  - Keep Phase Contract obligations separate from Phase Environment facts; do not create a contract catalog in this batch.
  - Do not implement Input Inventory schema validation or Phase Observation session attribution in this batch.
dependencies_satisfied:
  - Runner boundary split created focused concept-owner files and tests.
  - CONTEXT.md defines Phase Environment as runner-supplied launch and prompt context.
  - Current command tests cover prompt guardrails, expected receipt/inventory paths, env override key display, execute-only sandbox behavior, command flags, and dry-run display.
dependencies_blocking:
  - None for spec creation.
suggested_slices:
  - Characterize the current Phase Environment facts in focused tests before moving ownership.
  - Introduce a Phase Environment concept owner that produces structured launch and prompt context from RunnerConfig, Run State, and Phase.
  - Route command, prompt, sandbox, env override, and dry-run helpers through the Phase Environment owner.
  - Narrow tests so environment-owner tests assert environment facts and command/facade tests assert rendering and behavior preservation.
stop_conditions:
  - Stop if the refactor changes CLI arguments, command flags, prompt obligations, receipt path strings, artifact path strings, or dry-run output semantics.
  - Stop if real or user-provided env override values appear in prompt, dry-run output, command display, or generated artifacts.
  - Stop if Phase Contract obligations are moved into the Phase Environment owner instead of remaining rendered obligations.
  - Stop if the batch starts implementing exact Codex session JSONL discovery, Input Inventory validation, or Planning Root migration.
  - Stop if validation requires a live nested Codex run; use focused tests and dry-run smoke.
expected_spec_path: plans/codex-config-architecture-program-runner-phase-environment-runway.md
