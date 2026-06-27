batch_id: phase-contract-catalog
source_program_ledger: plans/codex-config-architecture-program-runner-findings.md
included_findings:
  - id: APR-19
    title: Phase Contract facts are embedded in prompt string construction
excluded_findings:
  - id: APR-20
    reason: Phase Observation attribution should consume clearer contract language but has separate artifact/session-log ownership.
  - id: APR-21
    reason: Input Inventory enforcement should wait until contract obligations are named and should not be mixed with prompt refactoring.
  - id: APR-22
    reason: Planning Root and Plan Archive migration is documentation/filesystem migration work, separate from runner phase behavior.
goal: Separate normative Phase Contract obligations from rendered prompt text while preserving exact Runner Facade behavior.
concept_owner_seam: scripts/architecture_program_runner_phase_contract.py as the single owner for per-phase obligations, allowed outputs, phase skill routing, and shared single-level phase rules consumed by prompt rendering.
validation_class: mechanical production refactor; focused contract/command tests plus dry-run smoke; no live nested Codex required.
guardrails:
  - Preserve the fixed phase sequence select-dispatch -> create-spec -> execute -> closeout.
  - Preserve current CLI arguments, command flags, dry-run output semantics, receipt path behavior, phase-result schema expectations, and final Run Summary shape.
  - Keep Phase Environment facts in scripts/architecture_program_runner_environment.py; do not move paths, sandbox/model/env override values, artifact facts, or batch-limit labels into the contract owner.
  - Keep Phase Result schema validation, receipt equality, and expected next-phase validation in scripts/architecture_program_runner_validation.py.
  - Do not implement exact Codex session JSONL discovery, Input Inventory schema validation, or Planning Root migration in this batch.
dependencies_satisfied:
  - Phase Environment now owns runner-supplied launch and prompt facts.
  - Phase Transition and Change Allowance owners now keep run-loop state advancement and path allowances separate from prompt construction.
  - CONTEXT.md defines Phase Contract as obligations and allowed outputs, not prompt text.
dependencies_blocking:
  - None for spec creation.
suggested_slices:
  - Characterize current Phase Contract obligations in focused tests before moving production ownership.
  - Introduce a Phase Contract concept owner with a structured per-phase contract API and compatibility routing for phase skill instructions.
  - Route prompt rendering through the contract owner while keeping Phase Environment facts supplied separately.
  - Tighten tests so contract tests own obligations, command tests own rendering, and facade tests preserve compatibility exports.
stop_conditions:
  - Stop if the refactor changes prompt obligations, phase-specific next_phase requirements, command flags, receipt path strings, artifact path strings, dry-run output semantics, or CLI behavior.
  - Stop if the contract owner starts deriving Phase Environment facts such as paths, sandbox/model choices, env override key labels, or batch-limit labels.
  - Stop if schema validation, expected next-phase validation, or receipt equality moves out of the validation concept owner.
  - Stop if the batch starts implementing Phase Observation attribution, Input Inventory validation, or Planning Root migration.
  - Stop if validation requires a live nested Codex run; use focused tests and dry-run smoke.
expected_spec_path: plans/codex-config-architecture-program-runner-phase-contract-catalog-runway.md
