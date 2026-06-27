# Architecture Program Runner Input Inventory Contract Runway

## Purpose

Give **Input Inventory** an enforced runner contract for phase-consumed context
evidence while preserving the existing **Runner Facade** behavior and
phase-result schema.

This spec executes the `input-inventory-contract` batch selected by
`plans/dispatch/input-inventory-contract-dispatch.md`.

## Current Baseline

- Baseline commit: `a54d244 Tighten architecture runner observation tests`.
- Source program ledger:
  `plans/codex-config-architecture-program-runner-findings.md`.
- Dispatch packet:
  `plans/dispatch/input-inventory-contract-dispatch.md`.
- Included finding: APR-21.
- Primary concept language: `CONTEXT.md`.
- Runner Facade: `scripts/architecture_program_runner.py`.
- Existing expected inventory path owner:
  `scripts/architecture_program_runner_environment.py` via
  `scripts/architecture_program_runner_state.py`.
- Existing prompt/contract owners:
  - `scripts/architecture_program_runner_command.py`
  - `scripts/architecture_program_runner_phase_contract.py`
- Existing validation and artifact owners:
  - `scripts/architecture_program_runner_validation.py`
  - `scripts/architecture_program_runner_artifacts.py`
- Current focused tests:
  - `tests/test_architecture_program_runner_environment.py`
  - `tests/test_architecture_program_runner_command.py`
  - `tests/test_architecture_program_runner_validation.py`
  - `tests/test_architecture_program_runner_artifacts.py`
  - `tests/test_architecture_program_runner_run_loop.py`
  - `tests/test_architecture_program_runner_protocol.py`
  - `tests/test_architecture_program_runner.py`

## Assumptions

- `plans/` is the current planning location until APR-22 migrates the
  **Planning Root**.
- The new concept owner should likely live at
  `scripts/architecture_program_runner_input_inventory.py`.
- **Input Inventory** records what a phase consumed: primary inputs, broad
  source reads, large file reads, and subagent reports.
- **Input Inventory** is phase-agent reported, not runner inferred.
- The runner can enforce existence, compact JSON shape, expected path, and
  `evidence_paths` linkage. It must not infer omitted reads from transcripts,
  command logs, session JSONL, newest files, or prompt text.
- No live nested Codex run is required for this batch. Synthetic phase
  executors and dry-run smoke are enough.

## Non-Goals

- Do not change CLI arguments, defaults, direct script execution, phase order,
  dry-run semantics, or final **Run Summary** shape.
- Do not add fields to
  `skills/architecture-program-runway/references/local-runner-phase-result.schema.json`.
- Do not change phase receipt equality. The phase receipt remains exactly the
  phase result JSON object.
- Do not make Input Inventory a transcript reconstruction feature.
- Do not implement worker/reviewer session attribution, context-stop policy, or
  hard budget enforcement.
- Do not migrate the **Planning Root** or create the **Plan Archive** for
  APR-22.
- Do not add Graphify-specific validation, cache, package-manager, network, or
  ledger-parsing logic.

## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about
suspicious coordinator or subagent-lifecycle behavior.
Use the expanded convergence template only when scope is expanding, significant
uncertainty exists, blockers are present, or final batch reporting is produced.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execute-slice-core-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execution-contract-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/reporting-contracts-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/ledger-retention-v1.md`

Overrides:
- Treat this file creation session as `create-spec`; implementation starts in a
  later `execute-spec` session from the first pending active-ledger row.
- Use lean-runway density with explicit schema, receipt, and inference
  guardrails because the intended behavior change is a narrow runner contract,
  not a broad runner redesign.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/project-harness-production.md`

Focused validation commands:
- For each slice, run the new or touched focused test modules plus the runner
  integration tests that cover the changed contract.
- Expected focused runner subset as the batch grows:
  `python -m pytest tests/test_architecture_program_runner_input_inventory.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- For slices before `tests/test_architecture_program_runner_input_inventory.py`
  exists, omit that path and run touched tests plus the relevant focused runner
  subset.
- Use the repo-proven lint path:
  `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check <touched production/test files>`
- `git diff --check`

Integration harness:
- Dry-run smoke, no nested Codex:
  `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`

Harness output:
- The dry-run smoke writes no expected project artifact. If tests introduce
  temporary state or artifact paths, keep them inside test temp directories or
  ignored generated paths.

Summary artifact:
- No generated summary artifact is required for the dry-run smoke. Report the
  command status and concise stdout/stderr signal needed to prove the smoke.

Index refresh:
- None required for this repo after these Python/test/docs edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use a concise imperative subject. No special trailers are required.
- Commit only files in the slice scope and the spec ledger/archive update for
  that slice.

Dirty-file constraints:
- Preserve unrelated dirty files.
- At batch start, planning files under `plans/` may be local planning artifacts.
- Do not revert or commit unrelated user changes outside the active slice.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1. Characterize Input Inventory gap | completed | slice commit | `pytest` 48 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean after characterization coverage fix | Introduce concept owner from characterized facts | Characterization proves expected path and prompt guidance exist, artifact size telemetry lists the inventory path, and validation does not yet enforce evidence linkage, file existence, or compact shape. |
| 2. Introduce Input Inventory owner | completed | slice commit | `pytest` 44 passed; `uvx ruff` passed; `git diff --check` passed | clean after path-safety fixes | Enforce expected inventory evidence | Added project-neutral owner validation and helper exports without run-loop enforcement, schema changes, receipt changes, or transcript/session inference. |
| 3. Enforce inventory evidence linkage | completed | slice commit | `pytest` 64 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean after manifest-ordering fix | Update prompts, docs, and artifact integration | Structured runs now require expected inventory evidence before phase transition and manifest writes; legacy runs without expected inventory paths remain exempt. |
| 4. Tighten prompt, docs, and artifact integration | completed | this closeout commit | `pytest` 129 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean after artifact-content assertion fix | Final validation and closeout | Prompts, protocol docs, manifests, telemetry tests, phase-observation fixtures, and changelog now reflect the enforced **Input Inventory** contract. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Characterize Input Inventory gap | slice commit | Added focused characterization tests for current **Input Inventory** prompt/path/artifact signals and missing enforcement. | Worker: success after reviewer-requested coverage fix; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_input_inventory.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, dry-run smoke, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check tests/test_architecture_program_runner_input_inventory.py`, `git diff --check` |
| 2. Introduce Input Inventory owner | slice commit | Added `scripts/architecture_program_runner_input_inventory.py` with compact JSON shape validation, project-relative path safety, expected-path helpers, and validation-owner helper exports. | Worker: success after reviewer-requested tilde path hardening; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_input_inventory.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/architecture_program_runner_input_inventory.py scripts/architecture_program_runner_validation.py tests/test_architecture_program_runner_input_inventory.py tests/test_architecture_program_runner_validation.py`, `git diff --check` |
| 3. Enforce inventory evidence linkage | slice commit | Routed receipt validation through the **Input Inventory** owner, requiring expected inventory evidence for structured runs and suppressing artifact manifests for rejected inventory evidence. | Worker: success after reviewer-requested manifest-ordering fix; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_input_inventory.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, dry-run smoke, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/architecture_program_runner.py scripts/architecture_program_runner_input_inventory.py scripts/architecture_program_runner_validation.py tests/test_architecture_program_runner_input_inventory.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_run_loop.py`, `git diff --check` |
| 4. Tighten prompt, docs, and artifact integration | this closeout commit | Updated prompt obligations, protocol reference, manifest/telemetry path exposure, changelog, and synthetic phase-observation fixtures for the enforced **Input Inventory** contract. | Worker: success after reviewer-requested artifact-content assertion fix; reviewer: clean; validation: final focused runner subset 129 passed, dry-run smoke passed, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts tests` passed after network escalation with known Python symlink warning, `git diff --check` passed |

## Slice 1. Characterize Input Inventory Gap

Scope:
- Add focused characterization coverage for the current **Input Inventory**
  behavior before production enforcement.
- Prove that the runner provides an expected input inventory path and prompt
  guidance, but does not yet enforce file existence, compact shape, or
  `evidence_paths` linkage.
- Keep characterization names aligned with `CONTEXT.md`.

Allowed files/areas:
- `tests/test_architecture_program_runner_input_inventory.py`
- `tests/test_architecture_program_runner_command.py`
- `tests/test_architecture_program_runner_artifacts.py`
- `tests/test_architecture_program_runner_validation.py`
- `tests/architecture_program_runner_test_support.py`
- This spec ledger/archive rows

Non-goals:
- Do not change production behavior in this slice unless a tiny test-support
  import compatibility fix is required.
- Do not change prompt wording yet.
- Do not introduce the owner API yet unless characterization tests cannot be
  expressed without a named test helper.

Acceptance criteria:
- Tests show `PhaseEnvironment.expected_input_inventory_path` and rendered
  prompts name the expected inventory path.
- Tests show phase telemetry includes the expected inventory path as an
  artifact size candidate.
- Tests characterize the current missing enforcement: a schema-valid phase
  result can omit the expected inventory path from `evidence_paths` and still
  pass validation before later slices change that behavior.
- Tests distinguish **Input Inventory** from **Phase Observation** and
  **Phase Receipt** in names or local helper structure.

Validation:
- Use the selected project-harness-production profile.
- Focused commands must include touched tests and:
  `python -m pytest tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run ruff through `uvx` on touched tests.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Characterize architecture runner input inventory gap`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, characterization accuracy, concept-language
  separation, and absence of production behavior changes.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if current code already enforces Input Inventory existence, shape, and
  `evidence_paths` linkage in a way the dispatch packet did not capture.
- Stop if characterization requires changing phase-result schema or receipt
  equality.

## Slice 2. Introduce Input Inventory Owner

Scope:
- Introduce a dedicated **Input Inventory** concept owner, expected at
  `scripts/architecture_program_runner_input_inventory.py`.
- Define compact JSON shape validation for phase-reported inventories.
- Keep the owner project-neutral and free of transcript/session inference.
- Provide small helpers for expected path checks and project-relative path
  resolution that validation/artifact owners can consume.

Allowed files/areas:
- `scripts/architecture_program_runner_input_inventory.py`
- `scripts/architecture_program_runner.py` compatibility exports only if
  existing public runner tests need them
- `scripts/architecture_program_runner_validation.py` only for importing or
  preparing owner calls, not for full enforcement yet
- `tests/test_architecture_program_runner_input_inventory.py`
- `tests/test_architecture_program_runner_validation.py`
- This spec ledger/archive rows

Non-goals:
- Do not enforce the new contract in the main run loop yet.
- Do not modify `local-runner-phase-result.schema.json`.
- Do not add YAML, JSON Schema files, or project-specific inventory schemas
  unless the worker proves a Python validator is insufficient.
- Do not infer inventory content from shell commands, session logs, or
  transcripts.

Acceptance criteria:
- The owner validates a compact JSON object with:
  - `schema_version` integer
  - `phase` string matching the active phase
  - `primary_inputs` array
  - `broad_reads` array
  - `large_file_reads` array
  - `subagent_reports` array
- The owner accepts minimal empty arrays for phases that consumed no broad
  inputs.
- The owner rejects non-object JSON, unknown top-level fields, wrong phase,
  non-array sections, non-string paths/commands/reasons/roles where present,
  non-integer byte counts where present, and absolute or parent-escaping
  project paths where project-relative paths are required.
- Tests prove validation failures raise `RunnerError` messages that name the
  inventory problem without dumping inventory content.
- Direct script execution fallback imports still work.

Validation:
- Use the selected project-harness-production profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_input_inventory.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run ruff through `uvx` on touched production/test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Add architecture runner input inventory owner`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, owner boundary, JSON shape validation, path safety,
  direct-script compatibility, and absence of schema/receipt changes.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if a Python-only validator cannot express the contract without changing
  the phase-result schema.
- Stop if the owner starts reading Codex session JSONL, transcripts, command
  logs, or arbitrary source files to infer consumed inputs.

## Slice 3. Enforce Inventory Evidence Linkage

Scope:
- Route phase-result/receipt validation through the **Input Inventory** owner.
- Require the runner-provided expected inventory file to exist for structured
  phases that have an expected inventory path.
- Require the expected inventory path to appear in `evidence_paths`.
- Validate the inventory JSON shape before phase transition and before
  artifact manifests are written.

Allowed files/areas:
- `scripts/architecture_program_runner_input_inventory.py`
- `scripts/architecture_program_runner_validation.py`
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_transition.py` only if unavoidable for
  validation ordering
- `tests/test_architecture_program_runner_input_inventory.py`
- `tests/test_architecture_program_runner_validation.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `tests/test_architecture_program_runner_protocol.py`
- This spec ledger/archive rows

Non-goals:
- Do not change the phase-result schema or receipt equality.
- Do not require inventory validation for legacy flat runs without an expected
  inventory path.
- Do not make inventory validation depend on live nested Codex, Git history, or
  project-specific validation tools.
- Do not change **Change Allowance** semantics except allowing the expected
  inventory evidence file where already appropriate.

Acceptance criteria:
- A phase result missing the expected input inventory path from
  `evidence_paths` fails with a clear `RunnerError`.
- A missing expected inventory file fails before phase transition.
- A malformed expected inventory file fails before phase transition.
- A valid inventory file at the expected path and listed in `evidence_paths`
  lets the existing phase-result and receipt checks pass.
- `validate_receipt` still rejects receipt mismatches exactly as before.
- Execute-phase worktree checks continue to allow the phase receipt plus
  explicit evidence paths only; unrelated dirty files still stop the runner.
- Tests use synthetic phase executors and temp files, not live nested Codex.

Validation:
- Use the selected project-harness-production profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_input_inventory.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run the dry-run smoke after enforcement is wired.
- Run ruff through `uvx` on touched production/test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Enforce architecture runner input inventory evidence`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, validation ordering, evidence-path linkage,
  receipt equality preservation, worktree allowance behavior, and synthetic
  test realism.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if enforcing the inventory contract requires adding new phase-result
  fields.
- Stop if missing inventory enforcement breaks dry-run behavior or legacy runs
  that do not have an expected inventory path.
- Stop if validation leaks inventory content or environment override values in
  error messages.

## Slice 4. Tighten Prompt, Docs, And Artifact Integration

Scope:
- Update prompt and phase-contract wording so phase agents know the inventory
  file is required when the runner provides an expected path.
- Update `skills/architecture-program-runway/references/local-runner-v1.md` to
  document the Input Inventory contract.
- Ensure phase telemetry/artifact size entries and batch/run manifests expose
  inventory paths consistently without duplicating inventory content.
- Update `CHANGELOG.md` because this is a meaningful runner workflow behavior
  change.

Allowed files/areas:
- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_artifacts.py`
- `scripts/architecture_program_runner_input_inventory.py`
- `skills/architecture-program-runway/references/local-runner-v1.md`
- `CHANGELOG.md`
- `tests/test_architecture_program_runner_command.py`
- `tests/test_architecture_program_runner_artifacts.py`
- `tests/test_architecture_program_runner_protocol.py`
- `tests/test_architecture_program_runner.py`
- This spec ledger/archive rows

Non-goals:
- Do not paste large schemas, examples, or logs into the runner reference.
- Do not change final **Run Summary** fields.
- Do not add hard context-stop policy, worker/reviewer session attribution, or
  Planning Root migration.

Acceptance criteria:
- Prompt text names the expected inventory path as a required compact evidence
  file when the path is present, and tells phase agents to include it in
  `evidence_paths`.
- `local-runner-v1.md` documents the inventory shape, evidence-path linkage,
  and separation from receipts, observations, telemetry, and transcript
  inference.
- Telemetry/artifact size tests prove inventory paths are listed as artifacts
  without embedding inventory content.
- `CHANGELOG.md` records the problem, decision, and expected effect.
- Dry-run smoke preserves CLI, command display, and no nested Codex behavior.

Validation:
- Use the selected project-harness-production profile.
- Focused commands must include the full focused runner subset named in this
  spec.
- Run the dry-run smoke.
- Run ruff through `uvx` on touched production/test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Document architecture runner input inventory contract`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, prompt/docs accuracy, artifact integration,
  changelog completeness, and absence of unrelated runner behavior changes.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if docs or prompt wording imply transcript reconstruction, session-log
  inference, or automatic broad-read detection.
- Stop if artifact integration embeds raw inventory content into telemetry or
  manifests instead of linking paths and sizes.

## Final Validation

Run after all slices are complete:

- `python -m pytest tests/test_architecture_program_runner_input_inventory.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts tests`
- `git diff --check`

## Closeout Instructions

At batch closeout:

- Mark APR-21 `Closed` in
  `plans/codex-config-architecture-program-runner-findings.md` only after the
  owner, enforcement, prompt/docs, artifact linkage, review, and final
  validation are complete.
- Keep APR-22 open as the next remaining candidate.
- Update this spec's Active Ledger and Completed Slice Archive with commit
  hashes, validation summaries, and review results.
- Record the final commit range, validation result, and review result in the
  program ledger without pasting long logs.

## Stop Conditions

- Stop on any required phase-result schema expansion.
- Stop on receipt equality changes.
- Stop on transcript/session-log inference.
- Stop on live nested Codex requirements.
- Stop on Graphify-specific or project-specific inventory rules.
- Stop on unresolved dirty-file conflict or unrelated user changes.
- Stop if subagent tooling required by Batch Runway execution is unavailable.
