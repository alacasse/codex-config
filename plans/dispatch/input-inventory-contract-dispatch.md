batch_id: input-inventory-contract
source_program_ledger: plans/codex-config-architecture-program-runner-findings.md
included_findings:
  - id: APR-21
    title: Input Inventory has no enforced contract
excluded_findings:
  - id: APR-22
    reason: Planning Root and Plan Archive migration is filesystem/documentation migration work and should not be mixed with runner phase-evidence enforcement.
goal: Give Input Inventory a runner-enforced contract for existence, compact JSON shape, evidence-path linkage, and artifact discoverability while preserving the existing phase-result schema.
concept_owner_seam: scripts/architecture_program_runner_input_inventory.py as the single owner for Input Inventory path expectations, JSON shape validation, and evidence linkage checks.
validation_class: project-harness production; focused validation/artifact/command/run-loop tests plus dry-run smoke; no live nested Codex required.
guardrails:
  - Preserve current CLI arguments, direct script execution, phase order, Run Summary shape, phase-result schema, receipt equality, and structured artifact layout.
  - Do not add Input Inventory fields to local-runner-phase-result.schema.json; use the existing evidence_paths array and runner-provided expected inventory path.
  - Keep Input Inventory separate from Phase Observation. Observation records what the runner observed; Input Inventory records what the phase reports it consumed.
  - Keep Input Inventory separate from Phase Receipt. The phase receipt remains the schema-valid phase result, and inventory details live in a separate compact JSON file.
  - Do not infer broad reads from transcripts, prompt text, newest files, shell logs, or Codex session JSONL.
  - Do not implement worker/reviewer session attribution, hard context-stop behavior, or Planning Root migration in this batch.
dependencies_satisfied:
  - APR-16 created Phase Environment ownership for expected input inventory paths.
  - APR-19 separated Phase Contract obligations from prompt rendering.
  - APR-20 implemented exact Phase Observation session attribution without transcript reconstruction.
  - Current prompts already name the expected input inventory path and ask phase agents to include it in evidence_paths when applicable.
dependencies_blocking:
  - None for spec creation.
suggested_slices:
  - Characterize the current Input Inventory gap with focused tests for prompt guidance, expected path generation, artifact size reporting, and missing validation.
  - Introduce an Input Inventory concept owner with compact JSON shape validation and project-relative path handling.
  - Enforce expected inventory existence, schema shape, and evidence_paths linkage during phase-result or receipt validation without changing the phase-result schema.
  - Update prompt/reference/manifest/telemetry integration so phase agents know the contract and runner artifacts expose the inventory path consistently.
stop_conditions:
  - Stop if the batch requires adding fields to the phase-result schema or changing receipt equality semantics.
  - Stop if validation depends on a live nested Codex run instead of synthetic phase results and dry-run smoke.
  - Stop if the implementation infers inventory content from transcripts, command logs, session JSONL, or broad filesystem scans.
  - Stop if Input Inventory validation starts owning Phase Observation, worker/reviewer attribution, context-budget policy, or Planning Root migration.
  - Stop if existing evidence_paths behavior is made project-specific or Graphify-specific.
expected_spec_path: plans/codex-config-architecture-program-runner-input-inventory-contract-runway.md
