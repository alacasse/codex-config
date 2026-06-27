# Architecture Program Runner Phase Transition and Change Allowance Runway

## Purpose

Give **Phase Transition** and **Change Allowance** clear concept owners while
preserving the public **Runner Facade** behavior and conservative changed-path
protection.

This spec executes the `phase-transition-change-allowance` batch selected by
`plans/dispatch/phase-transition-change-allowance-dispatch.md`.

## Current Baseline

- Baseline commit: `305ae9e Close phase environment ownership batch`.
- Source program ledger:
  `plans/codex-config-architecture-program-runner-findings.md`.
- Dispatch packet:
  `plans/dispatch/phase-transition-change-allowance-dispatch.md`.
- Included findings: APR-17 and APR-18.
- Primary concept language: `CONTEXT.md`.
- Runner Facade: `scripts/architecture_program_runner.py`.
- Existing concept owners:
  - `scripts/architecture_program_runner_state.py`
  - `scripts/architecture_program_runner_validation.py`
  - `scripts/architecture_program_runner_command.py`
  - `scripts/architecture_program_runner_artifacts.py`
  - `scripts/architecture_program_runner_environment.py`
- Current transition and allowance behavior still in the Runner Facade:
  - `apply_phase_result`
  - `is_terminal_completed_state`
  - `dirty_paths_from_status`
  - `expected_dirty_paths`
  - `check_worktree`
  - `path_is_expected`
- Current focused tests:
  - `tests/test_architecture_program_runner_run_loop.py`
  - `tests/test_architecture_program_runner_worktree.py`
  - `tests/test_architecture_program_runner_state.py`
  - `tests/test_architecture_program_runner_validation.py`
  - `tests/test_architecture_program_runner_environment.py`
  - `tests/test_architecture_program_runner_command.py`
  - `tests/test_architecture_program_runner.py`
  - `tests/test_codex_owner.py`

## Assumptions

- `plans/` is the current planning location until APR-22 migrates the
  **Planning Root**.
- **Phase Transition** consumes a schema-valid, receipt-verified
  **Phase Result** and updates **Run State**. It does not validate result
  schema, verify receipts, launch phases, classify dirty paths, or write
  observations.
- **Change Allowance** classifies which changed paths are acceptable for the
  current phase. Git status is an input observation, not the concept itself.
- Expected concept-owner homes are:
  - `scripts/architecture_program_runner_transition.py`
  - `scripts/architecture_program_runner_change_allowance.py`
  Workers may choose clearer local names only if the concept language remains
  explicit and compatibility exports are preserved.
- No live nested Codex run is required for this batch.
- The integration harness is the dry-run runner smoke that exercises CLI
  parsing, prompt construction, command display, direct script execution, and
  imports without launching nested Codex.

## Non-Goals

- Do not change CLI arguments, defaults, phase sequence, model handling,
  sandbox behavior, env override handling, or dry-run semantics.
- Do not change phase-result schema, required receipt fields, receipt equality,
  expected receipt paths, expected input inventory paths, artifact layout, or
  final Run Summary shape.
- Do not move schema validation, expected next-phase validation, or receipt
  equality out of `scripts/architecture_program_runner_validation.py`.
- Do not move path and artifact derivation out of
  `scripts/architecture_program_runner_state.py` or
  `scripts/architecture_program_runner_artifacts.py` unless a tiny import
  cleanup is required.
- Do not create the **Phase Contract** catalog for APR-19.
- Do not implement exact Codex session JSONL discovery for APR-20.
- Do not implement **Input Inventory** schema validation for APR-21.
- Do not migrate the **Planning Root** or **Plan Archive** for APR-22.
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
- Use lean-runway density with explicit state-transition and changed-path
  guardrails because the intended change is behavior-preserving concept
  ownership, not public behavior redesign.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/mechanical-production-refactor.md`

Focused validation commands:
- For each slice, run the new or touched focused test modules plus the runner
  integration tests that cover the moved behavior.
- Expected focused runner subset as the batch grows:
  `python -m pytest tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- For slices before `tests/test_architecture_program_runner_transition.py` or
  `tests/test_architecture_program_runner_change_allowance.py` exists, omit the
  missing path and run touched tests plus the remaining focused runner subset.
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
- None required for this repo after these Python/test edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use a concise imperative subject. No special trailers are required.
- Commit only files in the slice scope and the spec ledger/archive update for
  that slice.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Planning files under `plans/` may be local planning artifacts.
- Do not revert or commit unrelated user changes outside the active slice.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1. Characterize transition and allowance behavior | completed | slice commit | `pytest` 54 passed; `uvx ruff` passed; `git diff --check` passed | clean | Introduce Phase Transition owner | Characterization coverage added without production behavior changes. |
| 2. Introduce Phase Transition owner | pending |  |  |  | Introduce Change Allowance owner | Move state advancement without taking validation ownership. |
| 3. Introduce Change Allowance owner | pending |  |  |  | Route facade and tighten compatibility | Move dirty-path classification without weakening protection. |
| 4. Route facade through owners and tighten tests | pending |  |  |  | Final validation and closeout | Keep Runner Facade compatibility exports and behavior stable. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Characterize transition and allowance behavior | slice commit | Added focused transition and change allowance characterization tests; no production behavior changed. | Worker: success; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py`, `git diff --check` |

## Slice 1. Characterize Transition and Allowance Behavior

Scope:
- Add focused characterization coverage for current **Phase Transition** and
  **Change Allowance** behavior before moving production ownership.
- Separate tests by concept where practical:
  `tests/test_architecture_program_runner_transition.py` for state advancement
  and `tests/test_architecture_program_runner_change_allowance.py` for changed
  path classification.
- Keep existing run-loop and worktree tests as thin integration coverage until
  later slices narrow them.

Allowed files/areas:
- `tests/test_architecture_program_runner_transition.py`
- `tests/test_architecture_program_runner_change_allowance.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `tests/test_architecture_program_runner_worktree.py`
- `tests/architecture_program_runner_test_support.py`
- This spec ledger/archive rows

Non-goals:
- Do not change production code in this slice unless a tiny test-support import
  compatibility fix is required.
- Do not change prompt wording, phase results, receipt paths, dry-run output,
  or dirty-path behavior.
- Do not introduce the new owner APIs yet unless characterization tests cannot
  be written without a named test helper.

Acceptance criteria:
- Transition tests characterize:
  - `execute` advancing to `closeout` without incrementing completed batches.
  - `closeout` incrementing completed batches.
  - `closeout` with another selected batch resetting active batch, dispatch,
    spec, active batch artifact root, and batch manifest path.
  - terminal completed states that should not launch another phase.
  - `stop_after_phase` preserving the next active phase after the named phase
    finishes.
- Allowance tests characterize:
  - dirty status parsing, including rename paths.
  - expected state path and structured artifact root allowances.
  - stopped-phase evidence path allowances.
  - execute-to-closeout post-check rejection of unexpected project files.
  - prefix matching that allows expected directories without allowing unrelated
    siblings.
- Tests keep schema validation and expected next-phase validation in validation
  test ownership, not transition tests.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include touched tests and:
  `python -m pytest tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run ruff through `uvx` on touched tests.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Characterize architecture runner transition allowances`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, characterization coverage, concept separation,
  changed-path safety, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if current behavior cannot be characterized without changing production
  behavior.
- Stop if tests assert weaker changed-path protection than the existing
  run-loop/worktree tests.

## Slice 2. Introduce Phase Transition Owner

Scope:
- Introduce a **Phase Transition** concept owner, expected at
  `scripts/architecture_program_runner_transition.py`.
- Move state advancement decisions behind the owner:
  - applying a valid **Phase Result** to **Run State**
  - terminal completed-state detection
  - closeout completed-batch increment
  - active batch reset when closeout returns to `select-dispatch`
  - preserving stopped/failed stop reasons
- Preserve compatibility exports from the Runner Facade for existing tests and
  users when needed.

Allowed files/areas:
- `scripts/architecture_program_runner_transition.py`
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_artifacts.py` only for consuming
  existing artifact-recording helpers, not moving artifact ownership
- `tests/test_architecture_program_runner_transition.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `tests/test_architecture_program_runner.py`
- This spec ledger/archive rows

Non-goals:
- Do not move `validate_phase_result`, `expected_next_phases`,
  `validate_receipt`, or receipt equality into the transition owner.
- Do not move artifact manifest writing or phase observation writing into the
  transition owner.
- Do not change state schema or persisted field names.

Acceptance criteria:
- The transition owner exposes a small API with explicit **Phase Transition**
  naming.
- The Runner Facade delegates state advancement and terminal-state checks to
  the transition owner.
- Existing behavior for closeout, stopped/failed results, terminal done/max
  batch states, and `stop_after_phase` remains unchanged.
- Compatibility imports or wrappers keep current tests and direct script use
  working.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run dry-run smoke because the Runner Facade imports and loop are touched.
- Run ruff through `uvx` on touched production/test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Add architecture runner phase transition owner`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep validation and receipt checking outside the transition owner.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, transition ownership, validation boundary
  preservation, behavior preservation, and compatibility exports.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if the transition owner starts validating phase-result schema, expected
  next phases, or receipt equality.
- Stop if closeout batch counts, active batch reset, terminal state handling, or
  `stop_after_phase` semantics change.

## Slice 3. Introduce Change Allowance Owner

Scope:
- Introduce a **Change Allowance** concept owner, expected at
  `scripts/architecture_program_runner_change_allowance.py`.
- Move changed-path classification behind the owner:
  - porcelain status path extraction
  - expected changed-path set calculation
  - expected path prefix matching
  - worktree rejection with phase-specific error text
  - stopped-phase evidence path allowances
- Preserve compatibility exports from the Runner Facade for existing tests and
  users when needed.

Allowed files/areas:
- `scripts/architecture_program_runner_change_allowance.py`
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_state.py` only for consuming existing
  path helpers, not moving state ownership
- `tests/test_architecture_program_runner_change_allowance.py`
- `tests/test_architecture_program_runner_worktree.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `tests/test_architecture_program_runner.py`
- This spec ledger/archive rows

Non-goals:
- Do not weaken unrelated-dirty-file rejection.
- Do not move artifact path derivation ownership out of state/artifacts helpers.
- Do not change which paths are expected for each phase unless an existing bug
  is proven by tests and kept within APR-18.
- Do not change Git status invocation behavior except for import routing.

Acceptance criteria:
- The allowance owner exposes a small API with explicit **Change Allowance**
  naming.
- The Runner Facade delegates dirty-path parsing, expected-path calculation,
  prefix matching, and worktree checks to the allowance owner.
- Stopped execute evidence paths remain allowed when resuming or recovering.
- Execute-phase post-check still rejects unexpected changes before closeout.
- Compatibility imports or wrappers keep current tests and direct script use
  working.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run dry-run smoke because the Runner Facade imports are touched.
- Run ruff through `uvx` on touched production/test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Add architecture runner change allowance owner`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Preserve conservative changed-path behavior exactly unless a characterization
  test proves the intended behavior.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, changed-path safety, stopped evidence allowances,
  execute-to-closeout post-check behavior, and compatibility exports.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if unrelated changed source files become allowed.
- Stop if stopped-phase evidence paths are no longer allowed.
- Stop if execute-to-closeout post-check behavior is removed or delayed.

## Slice 4. Route Facade Through Owners and Tighten Tests

Scope:
- Finish routing the Runner Facade through the Phase Transition and Change
  Allowance owners.
- Move concept-specific assertions out of broad facade/run-loop tests where the
  new focused tests already own the behavior.
- Keep thin integration coverage in facade/run-loop tests for direct script
  execution, compatibility exports, CLI/dry-run behavior, full run-loop phase
  sequencing, and final summary behavior.
- Update `CHANGELOG.md` if the implementation meaningfully changes workflow
  code behavior or agent-facing workflow expectations.

Allowed files/areas:
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_transition.py`
- `scripts/architecture_program_runner_change_allowance.py`
- `tests/test_architecture_program_runner_transition.py`
- `tests/test_architecture_program_runner_change_allowance.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `tests/test_architecture_program_runner_worktree.py`
- `tests/test_architecture_program_runner.py`
- `CHANGELOG.md` only if required by repo instructions for meaningful workflow
  behavior changes
- This spec ledger/archive rows

Non-goals:
- Do not remove facade compatibility exports that current users or tests still
  rely on.
- Do not broaden refactoring into Phase Contract, Phase Observation, Input
  Inventory, Planning Root, command rendering, or artifact manifest ownership.
- Do not delete integration coverage just because a focused owner test exists.

Acceptance criteria:
- Runner Facade no longer owns transition or allowance rules beyond delegating
  to the concept owners and preserving compatibility exports.
- Focused owner tests carry concept behavior; run-loop/worktree/facade tests
  retain thin integration and compatibility assertions.
- Direct script execution remains covered.
- Dry-run smoke still succeeds.
- The program ledger can be closed out later with APR-17 and APR-18 evidence
  from the slice commits.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include the full runner subset:
  `python -m pytest tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run dry-run smoke:
  `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`
- Run ruff through `uvx` on touched production/test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Tighten architecture runner transition facade`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep thin integration coverage and compatibility exports where they protect
  user-visible behavior.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, facade slimming, compatibility exports, test
  topology, and accidental expansion into deferred findings.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if integration coverage for direct script execution, CLI/dry-run
  behavior, full run-loop sequencing, or final summary behavior disappears.
- Stop if the batch starts implementing APR-19, APR-20, APR-21, or APR-22.

## Final Validation

Run:
- `python -m pytest tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts/architecture_program_runner.py scripts/architecture_program_runner_transition.py scripts/architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner.py`
- `git diff --check`

Expected closeout evidence:
- APR-17 can close only after **Phase Transition** is testable as the place that
  consumes a valid **Phase Result** and updates **Run State**.
- APR-18 can close only after **Change Allowance** can be understood without
  reading Runner Facade orchestration.
- The program ledger should remain clear that APR-19, APR-20, APR-21, and
  APR-22 are still open/candidate work.

## Stop Conditions

- Stop on any dirty-file conflict outside this spec's allowed planning files or
  the active implementation slice.
- Stop if required subagent tooling is unavailable during execution.
- Stop if the refactor changes CLI arguments, phase sequence, command flags,
  dry-run semantics, phase-result schema, receipt equality, expected receipt
  paths, expected input inventory paths, artifact layout, or Run Summary shape.
- Stop if validation or receipt equality moves into Phase Transition ownership.
- Stop if unrelated changed-path rejection is weakened or stopped-phase evidence
  allowances are lost.
- Stop if implementation expands into Phase Contract catalog, Phase Observation
  attribution, Input Inventory validation, Planning Root migration, or
  Graphify-specific logic.
