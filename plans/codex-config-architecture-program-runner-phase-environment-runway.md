# Architecture Program Runner Phase Environment Runway

## Purpose

Create a clear **Phase Environment** concept owner for runner-supplied launch
and prompt context while preserving the public **Runner Facade** behavior.

This spec executes the `phase-environment-ownership` batch selected by
`plans/dispatch/phase-environment-ownership-dispatch.md`.

## Current Baseline

- Baseline commit: `18afdf0 Refactor Codex Config Architecture Program Runner findings into a structured Program Ledger`.
- Source program ledger:
  `plans/codex-config-architecture-program-runner-findings.md`.
- Dispatch packet:
  `plans/dispatch/phase-environment-ownership-dispatch.md`.
- Included finding: APR-16.
- Primary concept language: `CONTEXT.md`.
- Runner Facade: `scripts/architecture_program_runner.py`.
- Current prompt/command owner:
  `scripts/architecture_program_runner_command.py`.
- Current focused command tests:
  `tests/test_architecture_program_runner_command.py`.
- Existing owner tests and thin integration tests:
  - `tests/test_architecture_program_runner.py`
  - `tests/test_architecture_program_runner_run_loop.py`
  - `tests/test_architecture_program_runner_protocol.py`
  - `tests/test_architecture_program_runner_state.py`
  - `tests/test_architecture_program_runner_validation.py`
  - `tests/test_architecture_program_runner_artifacts.py`
  - `tests/test_architecture_program_runner_worktree.py`
  - `tests/test_codex_owner.py`

## Assumptions

- `plans/` is the current planning location until APR-22 migrates the Planning
  Root.
- The new concept owner should likely live at
  `scripts/architecture_program_runner_environment.py`, unless the worker finds
  a smaller name that better matches `CONTEXT.md`.
- **Phase Environment** means runner-supplied launch and prompt context:
  project path, program ledger, state path, active phase, batch bound, schema
  and reference paths, expected receipt and input inventory paths, active
  artifact paths, sandbox/model choices, env override key labels, subprocess
  env application, and dry-run launch display facts.
- **Phase Contract** obligations remain separate. For example, "Do not run
  codex exec" and per-phase requirements are contract/rendering facts, not
  environment facts.
- No live nested Codex run is required for this batch.
- The integration harness is the dry-run runner smoke that exercises CLI
  parsing, prompt construction, command display, and direct script execution
  without launching nested Codex.

## Non-Goals

- Do not change CLI arguments, defaults, command flags, model handling,
  sandbox defaults, execute-only sandbox behavior, env override parsing, or
  dry-run semantics.
- Do not change phase-result schema, required receipt fields, receipt equality,
  expected receipt paths, expected input inventory paths, or artifact layout.
- Do not create the **Phase Contract** catalog for APR-19.
- Do not implement exact Codex session JSONL discovery for APR-20.
- Do not implement **Input Inventory** schema validation for APR-21.
- Do not migrate the Planning Root or Plan Archive for APR-22.
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
- Use lean-runway density with explicit prompt, CLI, env-secrecy, and artifact
  guardrails because the intended change is behavior-preserving concept
  ownership, not public behavior redesign.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/mechanical-production-refactor.md`

Focused validation commands:
- For each slice, run the new or touched focused test modules plus the runner
  integration tests that cover the moved behavior.
- Expected focused runner subset as the batch grows:
  `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- For slices before `tests/test_architecture_program_runner_environment.py`
  exists, omit that path and run the touched tests plus the remaining focused
  runner subset.
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
- At batch start, planning files under `plans/` may be local planning artifacts.
- Do not revert or commit unrelated user changes outside the active slice.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1. Characterize Phase Environment facts | completed | slice commit | `pytest` 36 passed; `uvx ruff` passed; `git diff --check` passed | clean | Introduce owner from characterized facts | Characterization coverage added without production behavior changes. |
| 2. Introduce Phase Environment owner | completed | slice commit | `pytest` 38 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean after staging-scope fix | Route launch helpers through owner | Added `PhaseEnvironment` owner and compatibility wrappers without behavior changes. |
| 3. Route prompt and command context through owner | completed | slice commit | `pytest` 55 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean | Narrow tests around owner/rendering split | Prompt, command, dry-run, and subprocess env paths reuse owner-produced environment facts. |
| 4. Tighten test topology and facade compatibility | completed | slice commit | `pytest` 78 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean | Final validation and closeout | Environment tests now own environment facts, command tests own rendering, and facade tests own compatibility exports. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Characterize Phase Environment facts | slice commit | Added environment and launch fact characterization tests; no production behavior changed. | Worker: success; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py`, `git diff --check` |
| 2. Introduce Phase Environment owner | slice commit | Added `scripts/architecture_program_runner_environment.py`; command helpers delegate to the owner while prompt rendering remains in command owner. | Worker: success; reviewer: clean after staged-file separation; validation: `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, dry-run smoke, `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts/architecture_program_runner_environment.py scripts/architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py`, `git diff --check` |
| 3. Route prompt and command context through owner | slice commit | Routed runner execution, command construction, dry-run display, and env application through owner-produced `PhaseEnvironment`; updated changelog per repo instructions. | Worker: success; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, dry-run smoke, `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts/architecture_program_runner.py scripts/architecture_program_runner_environment.py scripts/architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py`, `git diff --check` |
| 4. Tighten test topology and facade compatibility | slice commit | Moved environment fact assertions to environment tests, command rendering assertions to command tests, and facade compatibility assertions to integration tests. | Worker: success; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, dry-run smoke, `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts/architecture_program_runner.py scripts/architecture_program_runner_environment.py scripts/architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner.py`, `git diff --check` |

## Slice 1. Characterize Phase Environment Facts

Scope:
- Add focused characterization coverage for current **Phase Environment** facts
  before moving production ownership.
- Identify which facts are environment facts versus rendered **Phase Contract**
  obligations in test names, assertions, and local helper structure.
- Prefer adding `tests/test_architecture_program_runner_environment.py` now if
  the characterization reads naturally there; otherwise add narrowly named
  tests in `tests/test_architecture_program_runner_command.py` and move them in
  Slice 2.

Allowed files/areas:
- `tests/test_architecture_program_runner_environment.py`
- `tests/test_architecture_program_runner_command.py`
- `tests/architecture_program_runner_test_support.py`
- This spec ledger/archive rows

Non-goals:
- Do not change production code in this slice unless a tiny test-support import
  compatibility fix is required.
- Do not change prompt wording or dry-run output.
- Do not introduce the owner API yet unless characterization tests cannot be
  written without a named test helper.

Acceptance criteria:
- Tests characterize expected receipt path and input inventory path facts from
  current state.
- Tests characterize artifact path facts used in prompts:
  `active_batch_id`, `artifact_root`, `active_batch_artifact_root`,
  `dispatch_path`, `spec_path`, `last_receipt_path`, `run_manifest_path`, and
  `batch_manifest_path`.
- Tests characterize launch facts: batch-limit label, sandbox selection,
  execute-only sandbox behavior, optional model flag, output-last-message path,
  and subprocess env override application.
- Tests prove env override values are not included in prompt or dry-run display.
- Tests keep **Phase Contract** obligations as rendered prompt assertions, not
  environment-owner assertions.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include touched test modules and:
  `python -m pytest tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run ruff through `uvx` on touched tests.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Characterize architecture runner phase environment`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, characterization coverage, env-value secrecy,
  contract/environment separation, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if the current behavior cannot be characterized without changing prompt
  text, command flags, or dry-run output.
- Stop if env override values appear in expected rendered output, snapshots, or
  generated output. Synthetic test sentinel values may be used only as inputs
  that assertions prove absent from rendered output.

## Slice 2. Introduce Phase Environment Owner

Scope:
- Introduce a **Phase Environment** concept owner, expected at
  `scripts/architecture_program_runner_environment.py`.
- Define a small structured API for deriving environment facts from
  `RunnerConfig`, **Run State**, and **Phase**. Suggested names are
  `PhaseEnvironment` and `build_phase_environment`, but the worker may choose a
  clearer local name if it keeps the concept explicit.
- Move pure environment helpers behind this owner: expected receipt/input
  inventory paths, batch-limit label, env override key label, sandbox selection,
  subprocess env application, schema/reference paths, and artifact path facts.
- Keep compatibility imports or wrappers in existing modules when needed for
  current tests and users.

Allowed files/areas:
- `scripts/architecture_program_runner_environment.py`
- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_state.py` only for consuming existing
  state/path APIs, not for moving state ownership
- `tests/test_architecture_program_runner_environment.py`
- `tests/test_architecture_program_runner_command.py`
- This spec ledger/archive rows

Non-goals:
- Do not move prompt rendering obligations into the environment owner.
- Do not change CLI parsing, `RunnerConfig` fields, env override parsing, or
  state JSON shape.
- Do not change artifact path construction ownership in
  `architecture_program_runner_state.py`; the environment owner should consume
  those APIs.

Acceptance criteria:
- A single environment-owner API can produce all launch and prompt context facts
  characterized in Slice 1.
- Existing command-owner helpers either delegate to the new owner or remain as
  compatibility wrappers with tests proving the owner is authoritative.
- Direct script execution and importlib-based tests both still work.
- Env override values remain absent from prompt and dry-run display.
- The owner consumes existing state/path APIs instead of duplicating artifact
  path or receipt path construction.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run the dry-run smoke because runner entrypoint imports and dry-run display
  may be touched.
- Run ruff through `uvx` on touched production and test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Add architecture runner phase environment owner`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, owner/API clarity, behavior preservation,
  import-mode compatibility, env-value secrecy, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if the owner would need to own **Phase Contract** obligations to satisfy
  tests.
- Stop if compatibility wrappers obscure which API owns Phase Environment
  facts.
- Stop if direct script execution and importlib-based tests cannot both be
  preserved.

## Slice 3. Route Prompt And Command Context Through Owner

Scope:
- Update prompt building, command construction, dry-run display, sandbox
  selection, and subprocess env construction to consume the **Phase
  Environment** owner API.
- Keep prompt wording and command lists behavior-preserving except for purely
  mechanical ordering that existing tests already allow.
- Remove duplicated environment fact derivation from
  `scripts/architecture_program_runner_command.py` after callers use the owner.

Allowed files/areas:
- `scripts/architecture_program_runner_environment.py`
- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner_environment.py`
- `tests/test_architecture_program_runner_command.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `tests/test_architecture_program_runner_protocol.py`
- This spec ledger/archive rows

Non-goals:
- Do not change phase-specific prompt obligations.
- Do not move **Phase Contract** wording into the owner.
- Do not change `codex exec` command flags or subprocess execution behavior.
- Do not add live nested Codex probes or CODEX_HOME workarounds.

Acceptance criteria:
- Prompt and command code consume one owner-produced environment object or
  equivalent owner API for environment facts.
- Command tests still prove phase skill instructions, nested-Codex prohibition,
  schema path, expected receipt path, expected input inventory path, env probe
  guidance, all-batches label, execute-only sandbox, optional model flag, and
  shell display quoting.
- Run-loop tests still pass without changing phase-result or receipt behavior.
- Env override values remain secret in prompt and dry-run display while still
  being applied to the subprocess env.
- The dry-run smoke output remains behaviorally equivalent and does not write
  runner state.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run the dry-run smoke.
- Run ruff through `uvx` on touched production and test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Route architecture runner command context through environment`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, prompt/command behavior preservation, owner API
  consumption, validation evidence, import-mode compatibility, and dirty-file
  leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if prompt wording changes beyond mechanical owner/API routing.
- Stop if command construction begins depending on mutable state not already
  provided by config/state/phase.
- Stop if environment ownership starts replacing validation, state, artifact,
  or contract ownership.

## Slice 4. Tighten Test Topology And Facade Compatibility

Scope:
- Move or narrow tests so the environment-owner tests assert **Phase
  Environment** facts and command tests assert prompt/command rendering.
- Keep thin Runner Facade compatibility assertions for public helper reexports
  that remain intentionally supported.
- Remove duplicated environment fact tests from command/run-loop suites when
  owner tests cover the same behavior more directly.
- Update local planning ledger rows only as coordinator-owned closeout work, not
  as worker implementation scope.

Allowed files/areas:
- `scripts/architecture_program_runner_environment.py`
- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner_environment.py`
- `tests/test_architecture_program_runner_command.py`
- `tests/test_architecture_program_runner.py`
- Other focused runner test modules only when moving duplicate assertions
- This spec ledger/archive rows

Non-goals:
- Do not delete regression coverage for env override secrecy, execute-only
  sandbox, optional model flag, output schema path, output-last-message path,
  expected receipt path, expected input inventory path, direct script execution,
  import compatibility, or dry-run display.
- Do not change production behavior except compatibility exports/import fixes
  required by the tightened tests.
- Do not close APR-16 in the program ledger inside worker scope; closeout is a
  separate architecture-program-runway responsibility after execution evidence
  exists.

Acceptance criteria:
- Test ownership mirrors concept ownership:
  environment tests cover environment facts, command tests cover rendering and
  launch command behavior, and facade tests cover user-visible compatibility.
- No broad test file regains responsibility for unrelated owner behavior.
- Public compatibility exports that remain are intentional and tested.
- The batch has enough final evidence to close APR-16 during later program
  closeout if all validation and review steps pass.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include the full runner subset:
  `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run the dry-run smoke.
- Run ruff through `uvx` on touched production and test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Align architecture runner environment tests`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, test ownership, compatibility coverage, validation
  evidence, import-mode compatibility, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if coverage for a previously fixed APR regression would be deleted
  rather than moved.
- Stop if test cleanup requires changing behavior outside compatibility
  exports/import fixes.

## Final Validation

Run after the last slice:

- `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts/architecture_program_runner.py scripts/architecture_program_runner_environment.py scripts/architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py`
- `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`
- `git diff --check`

Closeout expectations:
- APR-16 may close only after a concept owner owns both launch context and
  prompt context facts, focused tests pass, dry-run smoke passes, review is
  clean, and Runner Facade behavior is unchanged.
- APR-17, APR-18, APR-19, APR-20, APR-21, and APR-22 must remain open or
  candidate unless separate later evidence closes them.

## Final Batch Report

Completed commits:
- `950ddf9` Characterize architecture runner phase environment
- `82e8c8e` Add architecture runner phase environment owner
- `556b6bd` Route architecture runner command context through environment
- `e00f667` Align architecture runner environment tests

Final validation:
- `python -m pytest tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`: 78 passed.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts/architecture_program_runner.py scripts/architecture_program_runner_environment.py scripts/architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py`: passed with the known non-fatal `/usr/bin/python3.14` symlink warning.
- `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`: passed.
- `git diff --check`: passed.

Skipped slices:
- None.

Remaining risks:
- APR-17, APR-18, APR-19, APR-20, APR-21, and APR-22 remain deferred; this
  batch intentionally did not implement phase transitions, change allowance,
  phase contract cataloging, phase observation attribution, input inventory
  enforcement, or planning-root migration.
- `uvx ruff` continues to emit the known non-fatal base-Python symlink warning.

Compatibility paths that remain:
- The Runner Facade still reexports public command and environment helpers for
  direct-script and import compatibility.
- Command-owner wrappers remain for prompt and command rendering while
  environment facts are owned by `scripts/architecture_program_runner_environment.py`.

Orchestration anomalies:

```yaml
orchestration_anomalies: []
```

Inspection commands:
- `git show --stat 950ddf9`
- `git show --stat 82e8c8e`
- `git show --stat 556b6bd`
- `git show --stat e00f667`

## Convergence Assessment

### Phase
`closure`

### Scope trend
`shrinking`

### Closed this slice
- APR-16, **Phase Environment** concept ownership.

### Newly discovered
- None.

### Deferred out of scope
- APR-17 **Phase Transition**
- APR-18 **Change Allowance**
- APR-19 **Phase Contract**
- APR-20 **Phase Observation**
- APR-21 **Input Inventory**
- APR-22 **Planning Root** and **Plan Archive**

### Remaining unknowns
- None for the Phase Environment ownership batch.

### Temporary compatibility paths
- Runner Facade helper reexports remain intentionally supported and tested.

### Blockers
- None.

### Completion forecastable
`yes`

### Forecast
- The selected `phase-environment-ownership` batch is complete. Remaining work
  is represented by separate candidate batches in the program ledger.

### Evidence
- Four reviewed slice commits, final focused validation, dry-run smoke, ruff,
  and whitespace audit.

### Next proof required
- Select a future batch from the remaining program ledger candidates before
  opening another concrete runway.

## Stop Conditions

- Stop if the refactor changes CLI arguments, command flags, final summary
  fields, phase-result schema, receipt path behavior, expected input inventory
  path behavior, artifact layout, or dry-run state-writing behavior.
- Stop if real or user-provided env override values appear in prompt output,
  dry-run output, command display, or generated artifacts. Synthetic test
  sentinel values may be used only as inputs that assertions prove absent from
  rendered output.
- Stop if direct script execution and importlib-based tests cannot both be
  preserved.
- Stop if **Phase Contract** obligations are moved into the **Phase
  Environment** owner.
- Stop if the batch starts implementing exact session JSONL discovery, Input
  Inventory schema enforcement, or Planning Root migration.
- Stop if validation requires a live nested Codex run.
- Stop if required subagent support is unavailable in execution mode.
- Stop on dirty-file conflicts with unrelated user edits.
