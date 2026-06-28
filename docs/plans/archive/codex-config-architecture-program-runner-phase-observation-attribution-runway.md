# Architecture Program Runner Phase Observation Attribution Runway

## Purpose

Give **Phase Observation** exact runner-launched session attribution without
broad transcript reconstruction while preserving existing telemetry, manifest,
CLI, and receipt behavior.

This spec executes the `phase-observation-attribution` batch selected by
`plans/dispatch/phase-observation-attribution-dispatch.md`.

## Current Baseline

- Baseline commit: `11fa04b Close architecture runner phase contract batch`.
- Source program ledger:
  `plans/codex-config-architecture-program-runner-findings.md`.
- Dispatch packet:
  `plans/dispatch/phase-observation-attribution-dispatch.md`.
- Included finding: APR-20.
- Primary concept language: `CONTEXT.md`.
- Runner Facade: `scripts/architecture_program_runner.py`.
- Current artifact and telemetry owner:
  `scripts/architecture_program_runner_artifacts.py`.
- Current runner state owner:
  `scripts/architecture_program_runner_state.py`.
- Current focused tests:
  - `tests/test_architecture_program_runner_artifacts.py`
  - `tests/test_architecture_program_runner_run_loop.py`
  - `tests/test_architecture_program_runner_command.py`
  - `tests/test_architecture_program_runner_environment.py`
  - `tests/test_architecture_program_runner_phase_contract.py`
  - `tests/test_architecture_program_runner.py`
  - `tests/test_codex_owner.py`

## Assumptions

- `plans/` is the current planning location until APR-22 migrates the
  **Planning Root**.
- The new concept owner should likely live at
  `scripts/architecture_program_runner_phase_observation.py`, unless the worker
  finds a smaller name that better matches `CONTEXT.md`.
- **Phase Observation** means runner-recorded facts about launching and
  monitoring one phase: subprocess exit code, stdout/stderr byte counts, exact
  Codex session id, exact Codex session JSONL path when discoverable, and the
  metadata handed to telemetry writers.
- The current artifact telemetry path already records direct runner
  measurements and parses token_count events when `codex_session_path` is
  supplied. This batch should feed that path with exact attribution, not replace
  manifest or telemetry persistence.
- No live nested Codex run is required for this batch. Use synthetic subprocess
  output and synthetic session JSONL files in tests.

## Non-Goals

- Do not change CLI arguments, defaults, command flags, model handling,
  sandbox defaults, execute-only sandbox behavior, env override parsing,
  dry-run semantics, or final Run Summary shape.
- Do not change phase-result schema, required receipt fields, receipt equality,
  expected receipt paths, expected input inventory paths, or artifact layout.
- Do not move **Phase Environment** launch/prompt facts into the observation
  owner.
- Do not move **Phase Contract** obligations into the observation owner.
- Do not make missing session attribution fatal.
- Do not infer sessions by prompt text search, newest session file selection,
  broad session-log reconstruction, or copied prompt matching.
- Do not implement **Input Inventory** schema validation for APR-21.
- Do not implement worker/reviewer session attribution from execute-phase
  subagents.
- Do not promote context warnings into hard stop conditions.
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
- Use lean-runway density with explicit attribution guardrails because the
  intended change is behavior-preserving concept ownership and telemetry
  enrichment, not public runner behavior redesign.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/mechanical-production-refactor.md`

Focused validation commands:
- For each slice, run the new or touched focused test modules plus the runner
  integration tests that cover the moved behavior.
- Expected focused runner subset as the batch grows:
  `python -m pytest tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- For slices before `tests/test_architecture_program_runner_phase_observation.py`
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
  temporary state, session logs, or artifact paths, keep them inside test temp
  directories or ignored generated paths.

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
| 1. Characterize Phase Observation attribution | completed | slice commit | `pytest` 30 passed; `uvx ruff` passed; `git diff --check` passed | clean | Introduce observation owner from characterized facts | Characterization coverage added without production behavior changes. |
| 2. Introduce Phase Observation owner | completed | slice commit | `pytest` 29 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean after planning-artifact staging fix | Route runner execution through owner | Added `PhaseExecutionObservation` owner, exact session id parsing, and unique session JSONL path discovery without routing execution yet. |
| 3. Route execution metadata through observation owner | completed | slice commit | `pytest` 48 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean after env-secrecy and filesystem-error recovery | Tighten telemetry/facade compatibility | `execute_codex_phase` records observation-owner metadata; override-derived CODEX_HOME paths are not persisted. |
| 4. Tighten telemetry and compatibility tests | completed | slice commit | `pytest` 89 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean after changelog scope recovery | Final validation and closeout | Artifact tests now own telemetry persistence/token summaries, observation tests own attribution, APR-20 is marked closed, and repo-required changelog coverage is included. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Characterize Phase Observation attribution | slice commit | Added characterization coverage for exact session id parsing, non-fatal missing attribution, and synthetic token summaries from exact session JSONL paths; no production behavior changed. | Worker: success; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check tests/test_architecture_program_runner_phase_observation.py`, `git diff --check` |
| 2. Introduce Phase Observation owner | slice commit | Added `scripts/architecture_program_runner_phase_observation.py`; runner facade reexports the owner API while execution routing remains unchanged for Slice 3. | Worker: success; reviewer: clean after planning-artifact staging fix; validation: `python -m pytest tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, dry-run smoke, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/architecture_program_runner_phase_observation.py scripts/architecture_program_runner.py tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner.py`, `git diff --check` |
| 3. Route execution metadata through observation owner | slice commit | Routed subprocess execution metadata through `PhaseExecutionObservation`, added exact session path routing from non-override Codex home, and kept override values and discovery failures non-fatal. | Worker: success; reviewer: clean after env-secrecy and filesystem-error recovery; validation: `python -m pytest tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, dry-run smoke, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/architecture_program_runner.py scripts/architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_phase_observation.py`, `git diff --check` |
| 4. Tighten telemetry and compatibility tests | slice commit | Moved telemetry persistence/token-summary assertions to artifact tests, kept attribution/discovery assertions in observation tests, closed APR-20 in the program ledger, and added the repo-required changelog note. | Worker: success; reviewer: clean after changelog scope recovery; validation: `python -m pytest tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, dry-run smoke, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/architecture_program_runner.py scripts/architecture_program_runner_artifacts.py scripts/architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner.py`, `git diff --check` |

## Slice 1. Characterize Phase Observation Attribution

Scope:
- Add focused characterization coverage for current **Phase Observation**
  attribution boundaries before moving production ownership.
- Characterize exact Codex session id parsing from subprocess stdout/stderr.
- Characterize that telemetry remains useful and non-fatal when session
  attribution is missing.
- Characterize token summaries from a synthetic exact session JSONL path.

Allowed files/areas:
- `tests/test_architecture_program_runner_phase_observation.py`
- `tests/test_architecture_program_runner_artifacts.py`
- `tests/test_architecture_program_runner.py`
- `tests/architecture_program_runner_test_support.py`
- This spec ledger/archive rows

Non-goals:
- Do not change production code in this slice unless a tiny test-support import
  compatibility fix is required.
- Do not change prompt wording, command construction, dry-run output, telemetry
  file shape, or manifest file shape.
- Do not introduce the observation owner API yet unless characterization tests
  cannot be written without a named test helper.

Acceptance criteria:
- Tests prove exact UUID parsing works from synthetic `codex exec` stdout,
  stderr, or combined output.
- Tests prove missing session id/path leaves `codex_session_id` and
  `codex_session_path` null and keeps `token_summary.status=missing`.
- Tests prove a supplied exact synthetic session JSONL path produces
  `token_summary.status=ok`, max input tokens, context percentage, and context
  pressure as expected.
- Tests name **Phase Observation** as runner-observed launch/session metadata,
  separate from **Phase Environment** and **Phase Contract** facts.
- Tests do not assert prompt-text searches, newest-file selection, or broad
  transcript reconstruction.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run ruff through `uvx` on touched tests.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Characterize architecture runner phase observation`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, observation/environment/contract separation,
  exact-attribution guardrails, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if characterization requires a live nested Codex run.
- Stop if tests encode prompt-text search, newest-session heuristics, or any
  attribution that is not exact.

## Slice 2. Introduce Phase Observation Owner

Scope:
- Introduce a **Phase Observation** concept owner, expected at
  `scripts/architecture_program_runner_phase_observation.py`.
- Define a small structured API for observed execution metadata. Suggested
  names are `PhaseExecutionObservation` and `build_phase_execution_observation`,
  but the worker may choose clearer local names if the concept stays explicit.
- Move exact session id parsing behind this owner.
- Add exact session JSONL path discovery by UUID under the effective Codex home:
  prefer `CODEX_HOME` from the subprocess environment when present, otherwise
  default to the current user's Codex home. Discovery must return a path only
  when exactly one matching session JSONL path is found.
- Keep compatibility imports or wrappers in existing modules when needed for
  current tests and users.

Allowed files/areas:
- `scripts/architecture_program_runner_phase_observation.py`
- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner_phase_observation.py`
- `tests/test_architecture_program_runner.py`
- This spec ledger/archive rows

Non-goals:
- Do not route `execute_codex_phase` through the owner yet unless required for
  compatibility tests.
- Do not read session JSONL contents in the observation owner; token parsing
  remains in artifact telemetry helpers.
- Do not move manifest or telemetry writing out of the artifact owner.
- Do not change subprocess env construction ownership.

Acceptance criteria:
- A single observation-owner API can produce exit code, stdout bytes,
  stderr bytes, exact session id, and exact session path when uniquely
  discoverable.
- Exact session path discovery works with synthetic Codex home layouts such as
  `sessions/YYYY/MM/DD/rollout-...-<uuid>.jsonl`.
- Discovery returns `None` when no file matches or more than one file matches.
- The owner does not parse prompt text or choose newest files.
- Direct script execution and importlib-based tests both still work.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run ruff through `uvx` on touched production and test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Add architecture runner phase observation owner`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, owner/API clarity, exact-attribution behavior,
  direct-script compatibility, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if path discovery needs broad transcript scanning or prompt matching.
- Stop if ambiguity in session files is silently resolved by guessing.
- Stop if the owner starts owning telemetry persistence, **Phase Environment**
  facts, or **Phase Contract** obligations.

## Slice 3. Route Execution Metadata Through Observation Owner

Scope:
- Update `execute_codex_phase` to build subprocess env once, run `codex exec`
  with that env, and record `_phase_execution_meta` from the **Phase
  Observation** owner.
- Preserve output-last-message handling and return-value parsing.
- Preserve failure behavior while enriching telemetry with exact
  `codex_session_path` when the owner can discover it.
- Keep `last_codex_session` updates tied to exact observed session ids only.

Allowed files/areas:
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_phase_observation.py`
- `tests/test_architecture_program_runner_phase_observation.py`
- `tests/test_architecture_program_runner_artifacts.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `tests/test_architecture_program_runner.py`
- This spec ledger/archive rows

Non-goals:
- Do not change `build_codex_command` output, prompt text, dry-run output, or
  CLI parsing.
- Do not write env override values to observation metadata or telemetry.
- Do not make missing or ambiguous session paths fatal.
- Do not add worker/reviewer attribution.

Acceptance criteria:
- `execute_codex_phase` records the same exit/stdout/stderr byte fields as
  before.
- When synthetic subprocess output includes an exact session id and the
  effective Codex home has one matching JSONL path, telemetry receives both id
  and path.
- When attribution is missing or ambiguous, the runner still writes phase
  telemetry with missing token summary.
- Existing env override behavior is preserved and values are not recorded in
  telemetry or prompts.
- Existing command flags, output-last-message behavior, and result parsing are
  unchanged.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run the dry-run smoke because the runner entrypoint and command path are
  touched.
- Run ruff through `uvx` on touched production and test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Route architecture runner execution observations`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, behavior preservation, exact-attribution routing,
  env-value secrecy, failure telemetry, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if `execute_codex_phase` starts constructing a different `codex exec`
  command or changes result-file parsing.
- Stop if env override values can appear in observation metadata, telemetry,
  prompts, dry-run output, or tests.
- Stop if missing attribution changes successful or failed phase control flow.

## Slice 4. Tighten Telemetry And Compatibility Tests

Scope:
- Tighten focused tests so **Phase Observation** tests own execution/session
  attribution, artifact tests own telemetry/manifest persistence, and facade
  tests own compatibility exports.
- Add or adjust tests proving run telemetry aggregates exact session ids and
  token summaries from synthetic session JSONL paths.
- Update the Program Ledger closeout evidence for APR-20 after implementation
  finishes.

Allowed files/areas:
- `tests/test_architecture_program_runner_phase_observation.py`
- `tests/test_architecture_program_runner_artifacts.py`
- `tests/test_architecture_program_runner.py`
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_artifacts.py` only for small
  compatibility/export adjustments if tests reveal a genuine boundary issue
- `plans/codex-config-architecture-program-runner-findings.md`
- `CHANGELOG.md` for the repo-required workflow-change note
- This spec ledger/archive rows

Non-goals:
- Do not broaden into **Input Inventory** schema validation.
- Do not add hard context-stop behavior.
- Do not add worker/reviewer attribution.
- Do not migrate planning files.

Acceptance criteria:
- Observation tests are the only tests asserting exact session id/path
  discovery rules.
- Artifact tests assert that telemetry consumes supplied observation metadata
  and records path/token summaries without owning discovery.
- Facade compatibility tests expose any intentionally preserved API aliases.
- Final validation includes the focused runner subset, dry-run smoke, `uvx ruff`
  on touched files, and `git diff --check`.
- Program Ledger marks APR-20 closed only if exact session/path attribution is
  implemented or explicitly records a narrowed residual gap.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run the dry-run smoke.
- Run ruff through `uvx` on touched production and test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Tighten architecture runner observation tests`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, test ownership boundaries, final closeout evidence,
  behavior preservation, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if final tests require live nested Codex execution.
- Stop if APR-20 cannot be honestly closed because exact path attribution still
  depends on guessing or broad reconstruction.

## Final Validation

After the last slice and review pass, run:

- `python -m pytest tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts/architecture_program_runner.py scripts/architecture_program_runner_artifacts.py scripts/architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner.py`
- `git diff --check`

## Batch Stop Conditions

- Stop if implementation requires live nested Codex execution for validation.
- Stop if session attribution depends on prompt text search, newest-file
  heuristics, broad transcript reconstruction, or copied prompt matching.
- Stop if missing or ambiguous attribution becomes fatal.
- Stop if env override values are exposed in observation metadata, telemetry,
  manifests, prompts, dry-run output, or test snapshots.
- Stop if **Phase Observation** starts owning **Phase Environment**, **Phase
  Contract**, manifest persistence, or phase-result validation responsibilities.
- Stop if CLI behavior, command flags, receipt contract, phase-result schema,
  artifact layout, dry-run output semantics, or final Run Summary shape changes.

## Closeout Requirements

- Update `plans/codex-config-architecture-program-runner-findings.md` so APR-20
  records the final status, evidence commits, validation, and any residual
  attribution limitations.
- Keep APR-21 and APR-22 visible as remaining candidates unless separately
  superseded by implementation evidence.
- Archive detailed execution history in this spec's completed slice archive,
  not in the program ledger.
