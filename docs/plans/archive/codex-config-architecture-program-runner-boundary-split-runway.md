# Architecture Program Runner Boundary Split Runway

## Purpose

Split `scripts/architecture_program_runner.py` and its broad test suite into
smaller owner seams while preserving the public runner CLI, phase protocol,
receipt schema, artifact layout, and single-level phase model.

This spec executes the `runner-boundary-split` batch selected by
`plans/dispatch/runner-boundary-split-dispatch.md`.

## Current Baseline

- Baseline commit: `bad11cf Add telemetry support for structured runs in architecture program runner`.
- Source program ledger: `plans/codex-config-architecture-program-runner-findings.md`.
- Included findings: APR-11, APR-12, APR-13.
- Primary production entrypoint: `scripts/architecture_program_runner.py`.
- Primary test file: `tests/test_architecture_program_runner.py`.
- Focused baseline validation from the dispatch packet:
  `python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`.
- `python -m ruff --version` currently fails in this environment with
  `/usr/bin/python: No module named ruff`; execution should record that as a
  validation limitation instead of silently skipping lint.

## Assumptions

- `plans/` is the local planning location for this repo.
- The runner must remain executable as `python scripts/architecture_program_runner.py`.
- The runner must remain importable by the existing `importlib.util.spec_from_file_location`
  test harness.
- New helper modules must preserve both direct-script and test-import execution
  modes. Stop if a proposed import path works in only one mode.
- No live nested Codex run is required for this refactor batch.
- The integration harness is a dry-run runner smoke that exercises CLI parsing,
  prompt construction, and command display without launching nested Codex.

## Non-Goals

- Do not change CLI arguments or defaults.
- Do not change the phase-result schema, required receipt fields, or receipt
  path behavior.
- Do not change structured artifact paths under
  `architecture-program-runs/<ledger-stem>/<run-id>/`.
- Do not change the single-level phase model or execute-only sandbox override
  behavior.
- Do not add Graphify-specific validation, cache, or ledger parsing logic.
- Do not implement exact Codex session JSONL discovery or an input-inventory
  schema in this batch.
- Do not refactor `scripts/codex_owner.py`; it is outside this batch.

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
  later `execute-spec` session from the first pending ledger row.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/mechanical-production-refactor.md`

Focused validation commands:
- `python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- For split tests, run the new focused test module plus the remaining broad
  runner tests that cover the moved behavior.
- `python -m ruff check <touched production/test files>` when ruff is available;
  if unavailable, record the exact missing-tool output.
- `git diff --check`

Integration harness:
- Dry-run smoke, no nested Codex:
  `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`

Harness output:
- The dry-run smoke writes no expected project artifact. If a slice introduces a
  temporary state or artifact path for tests, it must be inside the test temp
  directory or an ignored generated path and must be removed or intentionally
  excluded from commits.

Summary artifact:
- No generated summary artifact is required for the dry-run smoke. Report the
  command status and any concise stderr/stdout signal needed to prove the smoke.

Index refresh:
- None required for this repo after these Python/test edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use a concise imperative subject. No special trailers are required.
- Commit only files in the slice scope and the ledger/spec update for that
  slice.

Dirty-file constraints:
- Preserve unrelated dirty files.
- At batch start, `plans/codex-config-architecture-program-runner-findings.md`
  and `plans/dispatch/` may be untracked local planning files.
- Do not revert or commit unrelated user changes outside the active slice.

## Execution Ledger

| Slice | Status | Commit | Focused validation | Review | Notes |
|---|---|---|---|---|---|
| 1. Path and state owner seam | Completed | `df92bda` | `70 passed`; dry-run smoke passed; `git diff --check` passed; ruff unavailable: `/usr/bin/python: No module named ruff` | Process-blocked review accepted after ledger recording; no code findings | Creates the first reusable owner API for path/state helpers. |
| 2. Phase result and receipt validation seam | Completed | `7cf3873` | `71 passed`; dry-run smoke passed; `git diff --check` passed; ruff unavailable: `/usr/bin/python: No module named ruff` | Process-blocked review accepted after ledger recording; no code findings | Consumes Slice 1 path/state APIs where applicable. |
| 3. Prompt, command, and env construction seam | Completed | `025d5a1` | `71 passed`; dry-run smoke passed; ruff via `uvx` passed; `git diff --check` passed | Clean | Preserved exact prompt guardrails and command flags. |
| 4. Artifact manifest and telemetry owner seams | Completed | `e96c71e` | `89 passed`; dry-run smoke passed; ruff via `uvx` passed; `git diff --check` passed | Clean after fix loop | APR-13 closed: structured failure paths refresh manifests and telemetry through active batch state. |
| 5. Test topology split and thin CLI integration suite | Completed | `63c1be7` | `71 passed`; dry-run smoke passed; ruff via `uvx` passed; `git diff --check` passed | Clean after coverage fix loops | Mirrored new owner seams and preserved broad regression coverage. |

## Completed Slice Archive

- Slice 1. Path and state owner seam:
  - Outcome: extracted path/state helpers to
    `scripts/architecture_program_runner_state.py` while keeping compatibility
    re-exports in `scripts/architecture_program_runner.py`.
  - Commit: `df92bda`.
  - Validation: `python -m pytest tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
    passed with 70 tests; dry-run runner smoke passed; `git diff --check`
    passed; ruff blocked because `/usr/bin/python` has no `ruff` module.
  - Review: separate `runway_reviewer` found no code findings. The reviewer
    required explicit recording of the ruff validation gap and intentional
    handling of coordinator-owned untracked planning files; both are recorded
    here.
- Slice 2. Phase result and receipt validation seam:
  - Outcome: extracted phase-result, receipt, and schema-subset validation to
    `scripts/architecture_program_runner_validation.py` while keeping
    compatibility re-exports in `scripts/architecture_program_runner.py`.
  - Commit: `7cf3873`.
  - Validation: `python -m pytest tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
    passed with 71 tests; dry-run runner smoke passed; `git diff --check`
    passed; ruff blocked because `/usr/bin/python` has no `ruff` module.
  - Review: separate `runway_reviewer` found no scope, dirty-file, or behavior
    findings. The reviewer required ruff in an environment where it is
    available; this environment gap is recorded here per the spec's validation
    limitation handling.
- Slice 3. Prompt, command, and env construction seam:
  - Outcome: extracted prompt, command, sandbox, env override, dry-run display,
    and command quoting helpers to `scripts/architecture_program_runner_command.py`
    while keeping compatibility re-exports in
    `scripts/architecture_program_runner.py`.
  - Commit: `025d5a1`.
  - Validation: `python -m pytest tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
    passed with 71 tests; dry-run runner smoke passed; `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check ...`
    passed with a non-fatal Python symlink warning; `git diff --check` passed.
  - Review: separate `runway_reviewer` returned clean with no findings or
    residual risks.
- Slice 4. Artifact manifest and telemetry owner seams:
  - Outcome: extracted artifact manifests, batch indexes, phase/run telemetry,
    token summaries, execution metadata, and artifact-size helpers to
    `scripts/architecture_program_runner_artifacts.py`.
  - APR-13: closed by refreshing manifests on structured `RunnerError` paths
    when active batch state exists, and by adding malformed-result regression
    coverage that preserves the validation error, writes state, and attributes
    phase telemetry/manifests through `active_batch_id`.
  - Commit: `e96c71e`.
  - Validation: `python -m pytest tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
    passed with 89 tests; dry-run runner smoke passed; `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check ...`
    passed with a non-fatal Python symlink warning; `git diff --check` passed.
  - Review: initial review found malformed-result failure-path attribution
    gaps; after two worker fix loops, final `runway_reviewer` pass returned
    clean with no findings.
- Slice 5. Test topology split and thin CLI integration suite:
  - Outcome: split the remaining broad runner tests into shared support,
    run-loop, worktree, protocol, and thin CLI/integration modules while keeping
    the owner-module focused tests from Slices 1-4.
  - Commit: `63c1be7`.
  - Validation: `python -m pytest tests/test_architecture_program_runner.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_codex_owner.py -q`
    passed with 71 tests; dry-run runner smoke passed; `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check ...`
    passed with a non-fatal Python symlink warning; `git diff --check` passed.
  - Review: reviewer found and workers restored missing coverage for numeric
    `--max-batches`, execute-sandbox subprocess command construction, env
    override prompt guidance, and all-batches prompt label; final
    `runway_reviewer` verification returned clean.

## Slice 1. Path and State Owner Seam

Scope:
- Extract pure path, slug, run-id, timestamp, state load/write, and structured
  artifact path helpers from `scripts/architecture_program_runner.py` into one
  owner module.
- Add focused tests for that owner seam.
- Keep `scripts/architecture_program_runner.py` as the installed CLI entrypoint
  and compatibility surface for existing tests during the transition.

Allowed files/areas:
- `scripts/architecture_program_runner.py`
- New runner helper module under `scripts/`
- `tests/test_architecture_program_runner.py`
- New focused test module under `tests/`

Non-goals:
- Do not move CLI parsing, subprocess execution, prompt construction, receipt
  validation, dirty-worktree policy, manifests, or telemetry.
- Do not change state JSON shape or artifact path strings.

Acceptance criteria:
- The new owner module is the single owner for path/state helper logic.
- Existing public helper names remain available from
  `scripts/architecture_program_runner.py` unless deliberately moved with tests
  updated in the same slice.
- Direct script execution and the importlib-based tests both still work.
- No downstream helper duplicates path, slug, run-id, or state serialization
  logic outside the owner module.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include path/state tests plus:
  `python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`.
- Run the dry-run smoke because the runner entrypoint/import behavior is touched.

Test quality review:
- None.

Commit message:
- `Extract architecture runner path state helpers`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, acceptance criteria, focused validation evidence,
  import-mode compatibility, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if helper imports only work for direct script execution or only for the
  importlib test harness.
- Stop if old flat-state resume compatibility becomes ambiguous.

## Slice 2. Phase Result and Receipt Validation Seam

Scope:
- Extract phase-result validation, expected next-phase rules, receipt path
  validation, and schema-adjacent helper checks into one owner module.
- Add focused tests for valid, invalid, nullable, and state-dependent result
  paths.
- Consume the Slice 1 path/state owner API for project path resolution where
  applicable.

Allowed files/areas:
- `scripts/architecture_program_runner.py`
- Runner validation helper module under `scripts/`
- Slice 1 helper module only as needed for imports/API use
- `tests/test_architecture_program_runner.py`
- New focused test module under `tests/`

Non-goals:
- Do not change the phase-result schema file.
- Do not change required result fields, summary string/null shape, terminal
  states, receipt equality rules, or next-phase semantics.
- Do not touch prompt text except to follow moved function imports if necessary.

Acceptance criteria:
- The new validation module is the single owner for phase result and receipt
  validation logic.
- Validation tests cover the existing supported Codex output-schema subset
  checks, nullable stopped results, invalid status/next-phase combinations,
  required fields, summary shape, and receipt path matching.
- `scripts/architecture_program_runner.py` delegates validation to the owner
  module without changing public behavior.
- Downstream slices must call this owner module instead of reimplementing
  receipt or phase-result checks.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include validation tests plus:
  `python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`.
- Run the dry-run smoke if imports in the entrypoint change.

Test quality review:
- None.

Commit message:
- `Extract architecture runner result validation`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, acceptance criteria, validation behavior
  preservation, import-mode compatibility, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if preserving the current schema subset checks requires changing the
  schema contract.
- Stop if receipt validation becomes split across multiple owner modules.

## Slice 3. Prompt, Command, and Env Construction Seam

Scope:
- Extract prompt construction, phase skill instruction lookup, Codex command
  construction, sandbox selection, env override handling, dry-run display, and
  command-display quoting into one owner module.
- Add focused tests for prompt guardrails, env key display without values,
  execute-only sandbox behavior, command flags, and dry-run output.
- Consume Slice 1 and Slice 2 owner APIs instead of duplicating path or
  validation logic.

Allowed files/areas:
- `scripts/architecture_program_runner.py`
- Runner prompt/command helper module under `scripts/`
- Existing runner helper modules only as API consumers
- `tests/test_architecture_program_runner.py`
- New focused test module under `tests/`
- `skills/architecture-program-runway/references/local-runner-v1.md` only if a
  moved prompt test needs to preserve an existing reference assertion without
  changing semantics

Non-goals:
- Do not change prompt contracts, local-runner protocol text, nested-Codex
  prohibitions, coordinator-shell env probe instructions, or command-line flags.
- Do not execute nested Codex.

Acceptance criteria:
- The new owner module is the single owner for prompt and command construction.
- Prompt tests still prove all phase contracts, expected receipt paths, input
  inventory path guidance, nested-Codex prohibition, closeout telemetry wording,
  and all-batches limit wording.
- Command tests still prove `--execute-sandbox` applies only to execute and env
  override values are not displayed in dry-run text.
- Direct script execution and importlib-based tests both still work.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include prompt/command tests plus:
  `python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`.
- Run the dry-run smoke.

Test quality review:
- None.

Commit message:
- `Extract architecture runner prompt command helpers`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, prompt/command behavior preservation, validation
  evidence, import-mode compatibility, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if prompt wording changes beyond import/path-driven mechanical edits.
- Stop if command construction begins depending on live runtime state that was
  previously pure configuration/state input.

## Slice 4. Artifact Manifest and Telemetry Owner Seams

Scope:
- Extract artifact batch recording, run/batch manifest generation, batch index
  rendering, execution metadata handling, phase telemetry, run telemetry, token
  summary parsing, and artifact size entries into owner module(s).
- Decide APR-13 inside the slice:
  - Prefer a small behavior-preserving-compatible fix that refreshes manifests
    on structured failure paths when enough state exists; or
  - If that is not mechanically safe, document in the slice ledger why manifests
    remain success-only and leave APR-13 open.
- Add focused tests for manifest paths, batch manifests, telemetry summaries,
  missing token summaries, context pressure, artifact size entries, and failure
  path manifest behavior or the documented no-change decision.
- Consume Slice 1 owner APIs for path/state behavior and Slice 2 owner APIs for
  result assumptions where applicable.

Allowed files/areas:
- `scripts/architecture_program_runner.py`
- Runner artifact/telemetry helper module(s) under `scripts/`
- Existing runner helper modules only as API consumers
- `tests/test_architecture_program_runner.py`
- New focused test module under `tests/`
- This spec ledger row for APR-13 outcome notes

Non-goals:
- Do not implement exact Codex session JSONL discovery unless already supplied
  by existing metadata.
- Do not add an input-inventory schema or enforcement path.
- Do not change artifact directory layout or receipt names.

Acceptance criteria:
- Artifact and telemetry writing have clear owner module(s) and no duplicated
  manifest-building logic remains in the runner entrypoint.
- Existing structured artifact layout tests continue to pass.
- Existing telemetry tests continue to pass.
- APR-13 has either a focused passing test for failure-path manifest refresh or
  a documented explicit decision that the success-only manifest behavior remains
  for a later, narrower batch.
- The runner still writes run telemetry on `RunnerError` as before.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include artifact/telemetry tests plus:
  `python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`.
- Run the dry-run smoke if entrypoint imports or artifact path display changes.

Test quality review:
- None.

Commit message:
- `Extract architecture runner artifact telemetry helpers`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, APR-13 outcome, artifact/telemetry behavior
  preservation, validation evidence, import-mode compatibility, and dirty-file
  leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if refreshing manifests on failure would require changing receipt schema,
  artifact paths, phase sequencing, or live Codex execution behavior.
- Stop if telemetry attribution work expands into exact session JSONL discovery.

## Slice 5. Test Topology Split and Thin CLI Integration Suite

Scope:
- Split remaining broad tests from `tests/test_architecture_program_runner.py`
  into focused modules that mirror the owner seams created in Slices 1-4.
- Keep a thin integration suite for CLI parsing, direct runner smoke, run-loop
  phase progression, dirty-worktree policy, and import compatibility.
- Remove duplicated helper setup only when the replacement makes ownership
  clearer without hiding behavior.

Allowed files/areas:
- `tests/test_architecture_program_runner.py`
- New focused test modules under `tests/`
- `scripts/architecture_program_runner.py` only for compatibility exports or
  import fixes required by the split tests
- Existing runner helper modules only for test imports
- This spec ledger/archive rows

Non-goals:
- Do not introduce broad test fixtures that obscure the phase protocol.
- Do not delete regression coverage for CLI defaults, env overrides, artifact
  layout, dirty-worktree checks, stopped-state resume, or unbounded mode.
- Do not change production behavior except tiny compatibility exports required
  by the split.

Acceptance criteria:
- The large test file no longer owns unrelated behavior that now has focused
  owner-seam modules.
- Focused tests can be run by owner module.
- A thin CLI/integration test path remains and covers direct script/import
  compatibility.
- `python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
  and the new focused test modules pass together.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include all runner test modules and
  `tests/test_codex_owner.py`.
- Run the dry-run smoke.

Test quality review:
- None.

Commit message:
- `Split architecture runner tests by owner seam`

Coding subagent brief:
- Implement only Slice 5 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 5 scope, test coverage preservation, validation evidence,
  import-mode compatibility, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if coverage for a previously fixed APR regression would be deleted
  rather than moved.
- Stop if the split requires changing production behavior outside compatibility
  exports/import fixes.

## Final Validation

Run after the last slice:

- `python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- All new focused runner test modules under `tests/`
- `python -m ruff check scripts/architecture_program_runner.py scripts/<new-runner-helper-modules>.py tests/test_architecture_program_runner.py tests/<new-runner-test-modules>.py` when ruff is available; otherwise record the missing-tool output.
- `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`
- `git diff --check`

Closeout expectations:
- APR-11 may close when runner internals are split into owner seams and the CLI
  remains runnable from `scripts/architecture_program_runner.py`.
- APR-12 may close only when the large test file no longer owns unrelated runner
  behavior.
- APR-13 may close only if failure-path manifests are refreshed with tests, or
  remain open with a documented decision.
- APR-9 and APR-10 must remain open.

## Stop Conditions

- Stop if the refactor changes CLI arguments, final summary fields, phase-result
  schema, receipt path behavior, or artifact layout.
- Stop if old flat-state resume compatibility becomes ambiguous.
- Stop if direct script execution and importlib-based tests cannot both be
  preserved.
- Stop if the batch starts implementing exact session JSONL discovery or input
  inventory schema work.
- Stop if validation requires a live nested Codex run.
- Stop if required subagent support is unavailable in execution mode.
- Stop on dirty-file conflicts with user-owned planning files or unrelated
  edits.

## Orchestration Anomalies

None recorded yet.
