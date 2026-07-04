# Phase Runner Business Logic Contract

## Purpose

Extract the current architecture-program runner's business logic as
implementation-neutral contracts before creating a separate `phase-runner`
module or repository.

This is contract work, not a file-by-file port. The target runtime and package
format are intentionally unspecified here. A later runway must choose package
basics before moving code.

## Source Scope

Current behavior evidence:

- Glossary and concept boundaries: `CONTEXT.md`
- Active program ledger:
  `docs/plans/programs/architecture-program-runner/LEDGER.md`
- Generic workflow boundary:
  `docs/plans/generic-phase-runner-workflow-contract.md`
- Repo split decision:
  `docs/plans/phase-runner-repo-split-issue-12-plan.md`
- Runner facade and concept owners:
  `scripts/architecture_program_runner*.py`
- Runner protocol and phase-result schema:
  `skills/architecture-program-runway/references/local-runner-v1.md`
  and
  `skills/architecture-program-runway/references/local-runner-phase-result.schema.json`
- Focused runner tests:
  `tests/test_architecture_program_runner*.py`

Prefer current code and tests over older archived runway specs when they
disagree.

## Source Architecture Map

The runner currently has three layers:

1. **Runner Facade**: the user-facing CLI in
   `scripts/architecture_program_runner.py`. It preserves invocation behavior,
   direct script execution, dry-run output, resume behavior, and final summary
   shape.
2. **Generic-looking control plane**: state, phase result validation, receipt
   equality, transition rules, worker execution seam, run/batch artifacts,
   telemetry, and input inventory validation.
3. **Codex-config integration**: architecture-program phase names, Program
   Ledger and Dispatch Packet semantics, Codex prompt construction, Batch
   Runway obligations, skill references, sandbox/model flags, and local
   planning policy.

The extraction target is the control-plane business logic. The current
architecture-program workflow should become the first integration adapter or
dogfooding workflow, not the generic runner itself.

## Contracts

### PBC-1. Workflow Phase Sequence

- Status: current for `codex-config`, generic as one valid workflow instance.
- Source evidence: `CONTEXT.md`, `local-runner-v1.md`,
  `scripts/architecture_program_runner_state.py`, and
  `tests/test_architecture_program_runner_run_loop.py`.
- Contract: a workflow has ordered phases and only advances through validated
  phase results. The current dogfooding workflow order is
  `select-dispatch -> create-spec -> execute -> closeout`.
- Target implication: the generic core must support declared phase order and
  transition constraints without hard-coding architecture-program semantics as
  the only possible workflow.
- Validation: target tests must prove normal advancement, stopped/failed
  terminal states, max-batch stop, and unbounded continuation.

### PBC-2. Runner Invocation Bounds

- Status: current.
- Source evidence: `parse_args()` and `config_from_args()` in
  `scripts/architecture_program_runner.py`;
  `test_cli_defaults_and_state_path`,
  `test_all_batches_cli_sets_unbounded_mode`, and
  `test_all_batches_conflicts_with_numeric_max`.
- Contract: an invocation chooses project, workflow ledger/config, batch bound,
  execution intent, resume state, sandbox/model intent, env overrides, dry-run,
  and optional stop-after-phase. Direct CLI defaults to one completed closeout
  unless an unbounded mode is explicit.
- Target implication: a generic runner must make run bounds explicit and reject
  contradictory bounds. The architecture-program CLI vocabulary may stay in
  `codex-config`.
- Validation: target CLI/API tests must cover default bound, numeric bound,
  unbounded mode, conflict rejection, and stop-after-phase.

### PBC-3. Durable Run State

- Status: current.
- Source evidence: `initial_state()`, `validate_state()`,
  `resolve_state_path()`, and `discover_resume_state_path()` in
  `scripts/architecture_program_runner_state.py`;
  `tests/test_architecture_program_runner_state.py`.
- Contract: each run has a durable JSON state object with schema version,
  runner version, project/workflow identity, active phase, active batch/work
  unit, artifact paths, last receipt, last phase status, stop reason, and
  completed count. Resume must load and validate this state before executing.
- Target implication: the target owns a versioned state schema and resume
  discovery policy. The exact current path names may change only with a
  compatibility plan.
- Validation: target tests must cover state creation, atomic write/read,
  validation failures, latest structured resume, and legacy/compatibility
  behavior if preserved.

### PBC-4. Phase Result Schema

- Status: current.
- Source evidence:
  `skills/architecture-program-runway/references/local-runner-phase-result.schema.json`
  and `validate_phase_result()` in
  `scripts/architecture_program_runner_validation.py`.
- Contract: every worker returns a compact JSON object with exactly these
  control fields: status, phase, next phase, stop reason, workflow ledger/config
  identity, work-unit id, dispatch/config path, spec/plan path, receipt path,
  commit range, validation summary, review summary, and evidence paths.
  Unknown fields are rejected.
- Target implication: the generic core should define its own neutral result
  names, but it must preserve the same strictness: required fields, no
  accidental extras, typed nullable summaries, and evidence paths as strings.
- Validation: target schema tests must reject missing fields, extra fields,
  invalid status/next-phase combinations, and active-phase mismatches.

### PBC-5. Receipt Equality

- Status: current.
- Source evidence: `validate_receipt()` and
  `validate_expected_receipt_path()` in
  `scripts/architecture_program_runner_validation.py`;
  `test_receipt_content_must_match_phase_result` and
  `test_structured_receipt_path_must_match_runner_expected_path`.
- Contract: the receipt is the persisted phase result. The runner rejects a
  result when the receipt is missing, malformed, at the wrong expected path, or
  not JSON-object equivalent after loading.
- Target implication: receipts are control-plane evidence, not transcripts,
  logs, telemetry, or summaries.
- Validation: target tests must cover missing receipt, mismatched receipt,
  wrong expected path, malformed JSON, and successful equality.

### PBC-6. Phase Transition

- Status: current.
- Source evidence: `apply_phase_transition()` in
  `scripts/architecture_program_runner_transition.py` and
  `tests/test_architecture_program_runner_transition.py`.
- Contract: transition consumes only a schema-valid, receipt-verified phase
  result. It records latest result facts, sets active work-unit paths, records
  artifact batch membership, advances to the next phase, increments completed
  count on closeout, and resets work-unit paths when another work unit begins.
- Target implication: transition must not own worker execution, result
  validation, receipt loading, or telemetry writing.
- Validation: target tests must prove execute-to-closeout, closeout-to-done,
  closeout-to-next-work-unit, stopped/failed non-advancement, and terminal
  state detection.

### PBC-7. Worker Adapter Boundary

- Status: current seam, target-critical.
- Source evidence: `PhaseWorker`, `CodexExecWorker`,
  `ShellCommandWorker`, and `execute_phase_with_worker()` in
  `scripts/architecture_program_runner_workers.py`; worker tests in
  `tests/test_architecture_program_runner.py`.
- Contract: a worker runs one phase and returns a phase result object or raises
  a runner error. Workers may differ by provider, but the runner validates
  results, receipts, state transition, and artifact behavior uniformly after
  worker return.
- Target implication: `codex exec` is one adapter, not the generic core. Shell
  command execution proves the boundary must not require prompt rendering.
- Validation: target tests must include at least two worker adapters or one
  adapter plus a fake worker proving the same post-worker control path.

### PBC-8. Environment And Provider Intent

- Status: current, partly integration-specific.
- Source evidence: `PhaseEnvironment` and `build_phase_environment()` in
  `scripts/architecture_program_runner_environment.py`;
  `tests/test_architecture_program_runner_environment.py`.
- Contract: each phase receives runner-supplied facts: expected receipt path,
  expected input inventory path, artifact facts, sandbox choice, env override
  keys, and batch/run limit label. Env override values may be applied to
  subprocesses but must not be displayed in diagnostics or persisted in
  telemetry.
- Target implication: the generic core should expose provider-neutral launch
  context. Codex schema paths, skill references, and prompt labels stay in the
  Codex-config integration.
- Validation: target tests must cover execute-only sandbox override, env
  override pass-through, key-only display, and no env value persistence.

### PBC-9. Change Allowance

- Status: current.
- Source evidence: `check_change_allowance()` and
  `expected_change_allowance_paths()` in
  `scripts/architecture_program_runner_change_allowance.py`;
  `tests/test_architecture_program_runner_change_allowance.py` and
  `tests/test_architecture_program_runner_worktree.py`.
- Contract: before each phase and after execute, the runner rejects unrelated
  dirty project paths. Allowed changes are the state path, structured artifact
  root, expected run/batch manifests, current dispatch/spec paths, latest
  receipt, stopped-phase evidence paths, closeout ledger updates, and
  phase-specific extra evidence.
- Target implication: this is a generic "change allowance" policy over an
  observed workspace, not inherently a Git feature. Git porcelain is the
  current observer.
- Validation: target tests must cover clean workspaces, expected artifact
  changes, rename path parsing if Git is used, sibling-prefix rejection, and
  unrelated file rejection.

### PBC-10. Artifact Layout

- Status: current.
- Source evidence: `local-runner-v1.md`,
  `scripts/architecture_program_runner_state.py`, and
  `scripts/architecture_program_runner_artifacts.py`;
  `tests/test_architecture_program_runner_artifacts.py`.
- Contract: structured runs write operational evidence under a run artifact
  root beside the workflow ledger/config. Run artifacts include state,
  manifests, telemetry, run-scoped selection receipts, and batch/work-unit
  subdirectories. Batch/work-unit artifacts include manifest, index, receipts,
  input inventory links, telemetry links, commit range, validation summary, and
  review summary.
- Target implication: the exact tree can be redesigned only if the facade or
  migration layer preserves current dogfooding behavior.
- Validation: target tests must cover run manifest content, batch manifest
  content, index backlinks, structured receipt paths, and failure manifest
  refresh where appropriate.

### PBC-11. Telemetry And Observation

- Status: current.
- Source evidence: `PhaseExecutionObservation` in
  `scripts/architecture_program_runner_phase_observation.py` and telemetry
  builders in `scripts/architecture_program_runner_artifacts.py`;
  `tests/test_architecture_program_runner_phase_observation.py` and
  `tests/test_architecture_program_runner_artifacts.py`.
- Contract: phase observation records runner-observed launch metadata such as
  exit code, stdout/stderr byte counts, prompt bytes, and provider session id
  when exactly attributable. Telemetry is separate from receipts and may record
  elapsed time, sandbox/model, token summaries, context pressure, artifact
  sizes, and missing-attribution status. Missing or ambiguous provider session
  paths are non-fatal.
- Target implication: provider-specific attribution belongs in adapters or
  observation plugins; receipt semantics must remain independent of telemetry.
- Validation: target tests must cover exact attribution, missing attribution,
  ambiguous attribution, filesystem errors, no env-value leakage, token summary
  aggregation, and non-fatal telemetry gaps.

### PBC-12. Input Inventory

- Status: current.
- Source evidence: `scripts/architecture_program_runner_input_inventory.py`,
  `local-runner-v1.md`, and
  `tests/test_architecture_program_runner_input_inventory.py`.
- Contract: each structured phase must write a compact input inventory at the
  runner-provided path and include that path in evidence paths. The inventory
  records phase, schema version, primary inputs, broad reads, large file reads,
  and subagent reports. It must use project-relative paths that do not escape
  the project. The runner validates shape and path before transition and
  manifest writes.
- Target implication: input inventory is consumed-context evidence. The runner
  must not reconstruct it from transcripts, logs, prompts, or newest files.
- Validation: target tests must cover minimal empty inventory, compact entries,
  wrong phase, unsupported fields, path escape attempts, non-integer byte
  counts, missing expected file, and evidence-path omission.

### PBC-13. Stop Conditions And Recovery

- Status: current.
- Source evidence: `run()` in `scripts/architecture_program_runner.py`,
  validation tests, and run-loop tests.
- Contract: the runner stops safely on invalid state, missing required
  dispatch/spec artifacts, dirty unrelated paths, worker failure, invalid
  phase result, missing or mismatched receipt, missing or malformed input
  inventory, execute post-check failures, configured max-batch completion,
  explicit stopped/failed phase results, and explicit stop-after-phase.
- Target implication: stop reasons must be durable in state and final summary.
  The runner should not infer domain correctness or repair project plans.
- Validation: target tests must cover each stop class and prove state is
  persisted when a phase fails after state initialization.

### PBC-14. Final Summary

- Status: current.
- Source evidence: `build_final_summary()` and `print_final_summary()` in
  `scripts/architecture_program_runner.py`;
  `test_final_summary_uses_state_and_last_receipt`.
- Contract: every invocation ends with a compact machine-readable summary of
  state path, artifact root, run telemetry path, latest phase telemetry, latest
  receipt, stop reason, completed count, active work unit, dispatch/spec paths,
  commit range, validation summary, and review summary.
- Target implication: the invoking agent should report from this summary and
  artifacts, not reconstruct execution from chat.
- Validation: target tests must cover summaries with and without readable
  latest receipts.

## Integration-Specific Behavior To Keep Out Of The Core

These behaviors are current and important, but they belong to the
`codex-config` integration rather than the generic business-logic core:

- architecture-program phase names as the only workflow;
- Program Ledger, Dispatch Packet, and Batch Runway semantics;
- `architecture-program-runway` and `batch-runway` skill instructions;
- Codex prompt text, output-schema subset quirks, model flags, sandbox flag
  names, and `codex exec` command construction;
- GitHub issue/comment conventions;
- personal planning overlays and Graphify validation policy;
- the Python file split under `scripts/architecture_program_runner*.py`.

## Source Details That Must Not Become Target Constraints

- The target does not need to preserve Python helper/function names unless they
  are part of the facade compatibility surface.
- The target does not need one module per current concept owner.
- The target does not need to store telemetry in the exact current JSON shape
  unless dogfooding compatibility requires it.
- The target does not need to use Git as the only change observer, though the
  current `codex-config` integration does.
- The target does not need to use Codex, prompts, or session JSONL files to run
  phases.

## Target Architecture Notes

A generic target should name owners by durable contracts, not source files:

- **Workflow Definition**: phase order, allowed next phases, phase metadata,
  and stop policy. Satisfies PBC-1, PBC-2, PBC-6, PBC-13.
- **State Store**: versioned state, atomic persistence, resume discovery, and
  final-summary source facts. Satisfies PBC-3 and PBC-14.
- **Result And Receipt Validator**: strict result schema, state consistency,
  expected receipt path, receipt equality, and input inventory linkage.
  Satisfies PBC-4, PBC-5, PBC-12.
- **Worker Runtime**: provider adapter interface plus shell/Codex or fake
  adapter implementations. Satisfies PBC-7 and PBC-8.
- **Artifact Store**: run/work-unit manifests, indexes, receipt locations,
  telemetry locations, and artifact-size metadata. Satisfies PBC-10 and
  PBC-11.
- **Workspace Guard**: observed changed-path policy and phase-specific change
  allowance. Satisfies PBC-9 and PBC-13.
- **Codex-Config Adapter**: architecture-program phases, Program Ledger
  vocabulary, Batch Runway prompts, Codex command construction, and current
  facade compatibility. Satisfies integration behavior without polluting the
  generic core.

## Port Runway Handoff

Next useful batch: replace the current APR-26 repo-skeleton plan with a
contract-first business-logic extraction batch.

Suggested slices:

1. Define package/runtime basics and name the target module or repository.
   Acceptance: the decision names language/runtime, CLI/API surface, test
   command, lint/type command, CI stance, and whether extraction happens in
   this repo first or a new repo.
2. Build the target's state/result/receipt/transition contracts with tests
   using fake or shell workers. Acceptance: PBC-1 through PBC-7 pass without
   Codex prompt construction.
3. Add artifact, telemetry, input inventory, and change-allowance contracts.
   Acceptance: PBC-8 through PBC-13 pass with provider-neutral fixtures.
4. Add the `codex-config` adapter/facade compatibility layer. Acceptance:
   current runner CLI behavior, phase-result schema, receipts, dry-run smoke,
   final summary, and focused runner tests remain green.

Guardrails:

- Do not directly translate the current Python file split into target packages.
- Do not move Codex prompts, Batch Runway rules, or Program Ledger semantics
  into the generic core.
- Do not move runtime behavior before package basics and compatibility tests
  are explicit.
- Do not change the existing Runner Facade behavior without a migration plan.

Validation ladder for the first implementation runway:

- Focused target contract tests for each PBC group.
- Existing focused runner tests in `tests/test_architecture_program_runner*.py`.
- Dry-run smoke against
  `docs/plans/programs/architecture-program-runner/LEDGER.md`.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts tests`
  while the source remains Python.
- `git diff --check`.

Open questions before implementation:

- Target language/runtime and package manager.
- Separate repository now, extraction branch, or in-repo generic package first.
- Public CLI/API name and compatibility promise.
- Whether the current JSON field names are public compatibility or adapter
  translation details.
