# Phase Runner Business Logic Contract

## Purpose

Extract the current architecture-program runner's business logic as
implementation-neutral contracts before creating a separate `phase-runner`
module or repository.

This is contract work, not a file-by-file port. The target runtime and package
format are intentionally unspecified here, except that the long-term direction
is an external OSS Go project. A later runway must choose package basics before
moving code or creating a public repository boundary.

## Source Scope

Current behavior evidence:

- Glossary and concept boundaries: `CONTEXT.md`
- Active program ledger:
  `docs/plans/programs/codex-config/LEDGER.md` (CCFG-1, sourced from APR-26)
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

## Contract Boundary Catalog

The target boundary is a set of implementation-neutral contracts, not a list of
future source files or package destinations. The generic core owns control-plane
rules; the `codex-config` adapter owns current architecture-program language and
dogfooding behavior.

| Contract | Generic core owns | `codex-config` adapter owns |
|---|---|---|
| **Workflow Contract** | Workflow identity, phase ordering or graph, transition constraints, run bounds, stop conditions, and artifact policy. | The architecture-program phase names and order, Program Ledger and Dispatch Packet interpretation, Batch Runway obligations, and local workflow command language. |
| **Run State Contract** | Versioned durable state, resume validation, active phase/work-unit facts, latest receipt facts, stop reason, artifact references, and completed count. | Current state-path defaults, structured run artifact locations, facade-compatible resume behavior, and migration behavior for dogfooding runs. |
| **Phase Result Contract** | Strict worker-returned control object with status, phase, next phase, work-unit identity, evidence paths, validation summary, and review summary. | Current architecture-program field names, dispatch/spec/closeout path vocabulary, phase-specific summaries, and compatibility with the existing phase-result schema. |
| **Phase Receipt Contract** | Receipt-path expectation, JSON-object loading, exact result equality, and rejection of malformed, missing, mismatched, or wrong-path receipts. | Current receipt path layout, dogfooding error language, and any compatibility translation for existing receipt artifacts. |
| **Worker Adapter Contract** | Provider-neutral phase execution interface and uniform post-worker validation, receipt checks, state transitions, artifact writes, and stop handling. | Codex prompt construction, `codex exec` command details, sandbox/model flags, skill references, shell-proof adapter wiring, and provider observation attribution. |
| **Run/Batch Artifact Contract** | Versioned run/work-unit manifests, indexes, input-inventory links, telemetry locations, receipt references, validation/review summaries, and final-summary facts. | Current architecture-program artifact tree, Program Ledger links, generated runway/closeout evidence, and local planning-policy compatibility. |

The generic core must not absorb architecture-program prompts, Batch Runway
execution rules, Program Ledger semantics, GitHub issue policy, repo-owned
Codex configuration checks, personal overlays, or Graphify-specific validation
policy. Those are integration adapter responsibilities even when the current
Python runner contains them near generic-looking control-plane code.

## Extraction Readiness Evidence

A later implementation runway may begin only after these proofs are explicit:

- contract tests or golden fixtures for workflow advancement, run-state resume,
  phase-result strictness, receipt equality, worker-adapter post-processing,
  artifact manifests, input inventory, telemetry separation, and stop
  conditions;
- facade compatibility evidence for current architecture-program CLI defaults,
  dry-run behavior, resume behavior, receipt paths, final summary shape, and
  focused `tests/test_architecture_program_runner*.py` coverage;
- planning-state interop evidence showing command/file/schema boundaries
  without importing or mirroring `scripts/planning_state.py` internals;
- a named adapter boundary for Codex prompts, `codex exec` arguments,
  sandbox/model flags, Batch Runway obligations, Program Ledger vocabulary, and
  local planning policy;
- an explicit package/runtime decision for any future target before runner code
  is moved or scaffolded.

These are preparation gates, not extraction evidence. Passing this contract
batch does not mean the runner has been extracted, packaged, or made ready for
repository creation.

## Extraction Stop Gates And Non-Goals

Stop before implementation whenever extraction work would require any of these
decisions or actions before they are explicitly selected in a later batch:

- moving `scripts/architecture_program_runner*.py` or translating the current
  Python file split into target packages;
- creating a repository, repo skeleton, package scaffold, Go module, CI
  scaffold, or public release surface;
- choosing target language/runtime, package manager, repository name, module
  path, public CLI/API name, compatibility promise, or extraction location;
- making `scripts/planning_state.py` a hidden internal dependency of the
  generic runner instead of using explicit command/file/schema interop;
- moving Codex prompts, Batch Runway rules, Program Ledger vocabulary, GitHub
  issue policy, personal overlays, Graphify validation policy, or repo-local
  planning policy into a generic runner core;
- selecting CCFG-2 through CCFG-5 or treating branch isolation, contract-drift
  review, adapter-authoring support, or Baton diagnostics as part of CCFG-1;
- scanning archived APR/PST ledgers for new scope beyond the APR-26 evidence
  already named by the canonical CCFG-1 row.

CCFG-1 can close only as contract/fixture preparation. Its closeout must show
implementation-neutral contracts, planning-state interop fixture expectations,
and facade compatibility checks. It must not claim extraction implementation,
package selection, repository creation, or adapter implementation is complete.

## Unresolved Extraction Decisions

The following decisions remain deliberately open after CCFG-1 preparation:

- target language/runtime, package manager, and test/lint toolchain;
- repository/module/package boundaries and whether extraction starts in-repo or
  directly in a separate OSS repository;
- public CLI/API name and compatibility promise;
- whether current JSON field names are public compatibility or adapter
  translation details;
- exact planning-state interop command, JSON schema, and exit-code contract;
- migration location and sequence for preserving current dogfooding behavior.

## Facade Compatibility Gates

The existing `scripts/architecture_program_runner.py` facade is the
dogfooding compatibility surface. Extraction may change internal ownership or
translate to neutral generic-core concepts, but it must keep these facade
expectations executable until a migration plan deliberately changes them:

- CLI defaults and bounds stay stable: direct invocation defaults to one
  completed closeout, `--all-batches` is the only unbounded mode, numeric and
  unbounded bounds conflict, and `--stop-after-phase` remains phase-bounded.
- Direct script execution remains supported from the `scripts/` directory as
  well as module-style imports from tests and callers.
- Dry runs print the planned command and prompt without writing runner state,
  receipts, manifests, or telemetry, and env override values remain hidden.
- Resume discovery prefers the latest structured run state and keeps legacy
  flat state compatible while rejecting state that contradicts CLI project,
  ledger, bound, or execution intent.
- Phase results stay strict: the facade-visible schema rejects missing or
  unknown control fields, invalid phase/status transitions, wrong active
  phase, and non-string evidence paths.
- Receipts remain the persisted phase result: expected structured receipt
  paths must match, receipt JSON must be an object, and loaded receipt content
  must equal the returned phase result.
- Structured artifacts keep facade-visible project-relative paths for run
  state, receipts, input inventories, manifests, telemetry, and batch
  subdirectories unless an explicit compatibility plan says otherwise.
- Input inventory linkage remains control-plane evidence: structured execute
  receipts must include the runner-provided inventory path in `evidence_paths`,
  and the inventory file must validate before transition or manifest writes.
- Final summaries keep their compact machine-readable shape: state path,
  artifact root, run and phase telemetry paths, latest receipt, stop reason,
  completed count, active work unit, dispatch/spec paths, commit range,
  validation summary, and review summary.

These are public facade expectations. How a later generic core names,
normalizes, or translates equivalent facts is an internal adapter detail and
must not leak architecture-program prompts, Batch Runway semantics, Program
Ledger vocabulary, branch-per-batch behavior, or repo-local planning policy
into the generic core.

## Separation And Interoperability Direction

The target should stay separate from `codex-config` while remaining
interoperable with it.

- The external Go runner owns the generic control plane: workflow execution,
  state, transitions, result/receipt validation, artifact registration,
  telemetry hooks, worker adapters, and stop conditions.
- `codex-config` owns the dogfooding integration: architecture-program phase
  names, prompts, skills, planning policy, Graphify fixture policy, and
  repo-local validation commands.
- `scripts/planning_state.py` owns read-only Planning Artifact Layout v1
  diagnostics and future planning-state transitions. It is not part of the
  runner core.
- Interop should happen through versioned schemas, file artifacts, command
  invocations, exit codes, and golden fixtures that both implementations can
  validate.

Do not couple the projects by sharing private helpers, importing Python modules
from Go, shelling out to `planning_state` as an implicit hidden dependency, or
copying the Python `scripts/architecture_program_runner*.py` file split into Go
packages. If the Go runner needs planning-state facts, define a small explicit
protocol: input root, output JSON, warning/error shape, and exit-code meaning.

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

### PBC-15. Planning-State Interop

- Status: fixture-backed contract expectation.
- Source evidence: `scripts/planning_state.py`,
  `tests/test_planning_state.py`, `docs/plans/planning-state-tooling-plan.md`,
  and `docs/plans/generic-phase-runner-workflow-contract.md`.
- Contract: planning-state discovery and validation are separate from runner
  execution. A runner may receive planning-state facts as explicit inputs or
  call a documented planning-state command, but it must not infer active work
  from historical filenames when Layout v1 `CURRENT.md` files exist.
- Protocol shape: the interop boundary is command/file/schema based. The
  caller supplies a planning root and optionally an explicit state fixture path
  or projection target. The command returns either text for humans or the
  `planning-state-facts` JSON protocol for machines, including root facts,
  program facts, warnings, blockers, validation messages, and exit facts.
- Exit semantics: code `0` means the command completed without fatal blockers,
  code `1` means validation completed and found blockers, and code `2` means
  unsupported invocation or protocol usage. Warnings remain warning-only unless
  they are also represented as blockers.
- Active-work facts: `selected_dispatch`, `queued_batch`, and
  `active_runway` come only from Layout v1 `CURRENT.md` files or explicit
  fixture state. Historical flat runways, dispatches, redirect ledgers, pickup
  notes, and archived files may appear as warnings or compatibility evidence,
  but they must not become selected work.
- Fixture expectation: `current --format json` and `validate --format json`
  must agree on Layout v1 root, program, warning, blocker, selected dispatch,
  queued runway, and active runway facts for the same fixture. Test-generated
  or temporary fixtures are preferred; durable JSON state is allowed only when
  project policy declares the exact target.
- Target implication: the Go runner should define planning-state integration as
  an adapter or preflight protocol, not as a built-in dependency on
  `codex-config` Markdown conventions. The first interoperable shape should be
  command/file based and fixture-tested.
- Validation: target tests must include golden Planning Artifact Layout v1
  fixtures where `current` and `validate` agree with the runner's selected work
  input, and where stale historical files produce warnings without becoming
  selected work. Ordinary planning-state interop must not require projection
  reporting or runner artifact projection.

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

- **Protocol Boundary**: versioned schemas and fixture contracts shared between
  the Python dogfooding runner, the future Go runner, and planning-state
  diagnostics. Satisfies PBC-4, PBC-5, PBC-10, PBC-12, PBC-14, and PBC-15.
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
- **Planning-State Adapter**: explicit command/file bridge for Layout v1
  planning-state facts. Satisfies PBC-15 without making planning-state
  diagnostics part of the runner core.

## Port Runway Handoff

Next useful batch: replace the current APR-26 repo-skeleton plan with a
contract-first business-logic extraction batch.

Suggested slices:

1. Define package/runtime basics and name the target module or repository.
   Acceptance: the decision names Go module/repository boundaries, CLI/API
   surface, test command, lint/type command, CI stance, license posture, and
   whether extraction starts in this repo first or directly in a new OSS repo.
2. Build the target's state/result/receipt/transition contracts with tests
   using fake or shell workers. Acceptance: PBC-1 through PBC-7 pass without
   Codex prompt construction.
3. Add artifact, telemetry, input inventory, and change-allowance contracts.
   Acceptance: PBC-8 through PBC-13 pass with provider-neutral fixtures.
4. Add planning-state interop fixtures and command/file protocol tests.
   Acceptance: PBC-15 passes without importing `planning_state` into the
   runner core.
5. Add the `codex-config` adapter/facade compatibility layer. Acceptance:
   current runner CLI behavior, phase-result schema, receipts, dry-run smoke,
   final summary, and focused runner tests remain green.

Guardrails:

- Do not directly translate the current Python file split into target packages.
- Do not make the Go project depend on `codex-config` private helpers.
- Do not make `planning_state` an internal runner dependency; use an explicit
  adapter/protocol if planning facts are needed.
- Do not move Codex prompts, Batch Runway rules, or Program Ledger semantics
  into the generic core.
- Do not move runtime behavior before package basics and compatibility tests
  are explicit.
- Do not change the existing Runner Facade behavior without a migration plan.

Validation ladder for the first implementation runway:

- Focused target contract tests for each PBC group.
- Existing focused runner tests in `tests/test_architecture_program_runner*.py`.
- Dry-run smoke against
  `docs/plans/programs/codex-config/LEDGER.md`.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts tests`
  while the source remains Python.
- `git diff --check`.

Open questions before implementation:

- Target language/runtime and package manager.
- Separate repository now, extraction branch, or in-repo generic package first.
- Public CLI/API name and compatibility promise.
- Whether the current JSON field names are public compatibility or adapter
  translation details.
- Exact planning-state interop protocol: command invocation, JSON shape, and
  exit-code semantics.
