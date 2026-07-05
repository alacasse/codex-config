# Planning-State Project Policy Runway

## Purpose

Define and implement project-owned planning-state policy before adding SQLite
projection behavior. The batch makes state-file and projection ownership an
explicit project value so `codex-config`, ignored local overlays such as
Graphify `my-docs`, and future projects can use the same workflow tooling
without sharing one hard-coded state layout.

This spec executes the `planning-state-project-policy` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/dispatch.md`.

## Current Baseline

- Baseline state: `python scripts/planning_state.py current --root docs/plans`
  and `python scripts/planning_state.py validate --root docs/plans` pass with
  only existing architecture-runner redirect warnings.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/dispatch.md`.
- Included finding: PST-8.
- Existing owner seam: `scripts/planning_state.py`.
- Existing focused tests: `tests/test_planning_state.py`.
- Existing commands can report current state, validate state, allocate batch
  paths, register artifacts, select/queue batches in explicit state fixtures,
  validate/render bounded closeout evidence, and bootstrap companion JSON state
  from Layout v1 Markdown.
- Latest completed closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/closeout.md`.
- Existing planned SQLite batch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/runway.md`.

## Assumptions

- `codex-config` owns its workflow docs and can commit project planning docs
  under `docs/plans/`, but that does not define a generic default for other
  repositories.
- Graphify-style local planning should remain ignored/local when the upstream
  repository should not receive personal coordination artifacts.
- A future project may choose committed, ignored-local, external,
  generated-only, or no durable JSON state depending on its repository and
  ownership model.
- SQLite projection policy is separate from JSON state policy. SQLite is still
  optional, rebuildable, and never canonical.
- Reusable skills and tooling resolve project values from instructions,
  overlays, current state, active specs, or explicit user direction. They do
  not hard-code one project name, path, issue policy, cache path, or local
  planning layout.

## Non-Goals

- Do not implement SQLite projection or reporting in this batch.
- Do not migrate any downstream project planning root.
- Do not commit ignored/local Graphify artifacts.
- Do not choose a universal state-file path for all projects.
- Do not make state files mandatory for Markdown-only projects.
- Do not render or rewrite planning Markdown from generated state.
- Do not update GitHub issues or comments.

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
- Treat this session as `create-spec`; implementation starts in a later
  `execute-spec` session from the first pending active-ledger row.
- Use `full-runway` density because this batch defines project policy and
  write-target safety semantics that future SQLite/reporting work consumes.
- Workers must use temp fixtures for ignored-local and external policy tests.
- Workers must not write to downstream project planning roots.
- Workers must not create committed durable JSON state or SQLite files unless a
  slice explicitly declares that path as codex-config policy documentation or
  a test fixture.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/project-harness-production.md`

Focused validation commands:
- For production/test slices, run:
  `python -m pytest tests/test_planning_state.py -q`
- Use the repo-proven lint path on touched Python files:
  `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check <touched production/test files>`
- Always run `git diff --check`.

Integration harness:
- Dry-run CLI checks, no nested Codex:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For slices that add policy discovery or enforcement, include temp-fixture CLI
  checks for committed, ignored-local, external, generated-only, none, and
  missing-policy behavior.
- Do not require live Graphify validation for this batch; use project-neutral
  ignored-local fixtures when downstream behavior needs coverage.

Harness output:
- Existing `current`, `validate`, and `bootstrap-state` checks should write no
  live planning files.
- Policy tests should write only to test temp directories, stdout, or explicit
  caller-provided paths.

Summary artifact:
- No generated summary artifact is required. Report compact stdout/stderr
  signals from CLI checks and the paths of any temp fixtures created by tests.

Index refresh:
- None required for this repo after these Python/test/docs edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.
- Do not write to downstream project planning roots.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1. Define project policy contract | Closed | This commit | `python -m pytest tests/test_planning_state.py -q` passed (124 passed); ruff passed with existing `/usr/bin/python3.14` warning; `git diff --check` passed. | `runway_reviewer` clean after root/policy and empty-path fix loops. | Policy vocabulary and discovery contract are documented and fixture-tested. |
| 2. Report and validate project policy | Closed | This commit | `python -m pytest tests/test_planning_state.py -q` passed (137 passed); current/validate text and JSON checks passed with existing redirect warnings only; ruff passed with existing `/usr/bin/python3.14` warning; `git diff --check` passed. | `runway_reviewer` clean after discovery, source-path, queued-ID, malformed-precedence, and malformed-queued-batch fix loops. | `current`/`validate` expose project policy and stable blockers/warnings. |
| 3. Enforce state and projection target policy | Pending |  |  | Write/preflight commands refuse durable targets not allowed by policy. |  |
| 4. Document policies and unblock SQLite | Pending |  |  | codex-config and ignored-local examples are documented; SQLite batch is queued next. |  |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Define project policy contract | This commit | Closed | Contract docs and schema validation cover committed, ignored-local, external, generated-only, none, missing, unsupported, root-mismatch, and empty-path policy cases; clean final review against task-scoped diff. |
| 2. Report and validate project policy | This commit | Closed | `current`/`validate` report policy facts in text/JSON, preserve read-only Markdown behavior without policy, preflight `--require-project-policy`, discover policy from state fixtures, root/program CURRENT, instructions, and active specs, and keep malformed higher-precedence policy/queued-batch diagnostics stable; clean final review against task-scoped diff. |

## Slice 1. Define Project Policy Contract

Scope:
- Define the project-state policy vocabulary and discovery contract.
- Cover `planning_root`, `run_artifact_root`, `output_root`,
  `state_file_policy`, `state_file_path`, `projection_policy`,
  `projection_path`, and update authority.
- Define accepted `state_file_policy` values: `generated-only`, `committed`,
  `ignored-local`, `external`, and `none`.
- Define accepted `projection_policy` values: `generated-only`,
  `ignored-local`, `external`, and `none`, with committed projections allowed
  only by explicit project exception.
- Add tests or fixtures that distinguish codex-config committed planning docs
  from Graphify-style ignored local overlays without hard-coding either as a
  generic default.

Allowed files/areas:
- `skills/planning-artifacts/SKILL.md`
- `docs/plans/planning-state-tooling-plan.md`
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Optional focused note under
  `docs/plans/programs/planning-state-tooling/notes/`
- This spec ledger/archive rows
- `CHANGELOG.md` if reusable skill or command behavior changes

Non-goals:
- Do not add SQLite schema or reports.
- Do not choose actual durable state files for every project.
- Do not write state files as part of contract tests except temp fixtures.
- Do not change active-state resolution precedence.

Acceptance criteria:
- The contract says project policy is discovered, not hard-coded.
- The contract can represent committed repo planning docs, ignored local
  overlays, external state, generated-only proof, and no durable state.
- Tests or fixture examples cover missing policy and unsupported policy values.
- Reusable docs warn generic skills not to bake in codex-config or Graphify
  paths.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless policy fixtures become broad or heavily mocked.

Commit message:
- `Define planning state project policy`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, policy vocabulary clarity, generic-skill
  guardrails, and fixture coverage for committed versus ignored-local policy.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the policy contract requires one universal path for all projects.
- Stop if the contract conflicts with Planning Artifact Layout v1 root
  discovery.

## Slice 2. Report And Validate Project Policy

Scope:
- Teach `current` and `validate` to discover and report project-state policy
  when declared by root `CURRENT.md`, program `CURRENT.md`, project
  instructions, an active spec, or explicit CLI input supported by the slice.
- Add stable warnings or blockers for missing policy only when a command is
  about to write durable state or projection data.
- Preserve Markdown-only workflows: `current` and `validate` without writes
  should still work when no durable state policy is selected.
- Include JSON protocol output for project policy when `--format json` is used.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- `docs/plans/planning-state-tooling-plan.md`
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not implement state/projection writes yet.
- Do not require every project to declare a durable state file.
- Do not parse arbitrary downstream local overlays outside explicit fixture
  data or declared project instructions.

Acceptance criteria:
- `current` text output shows resolved project policy compactly when present.
- JSON output includes policy facts with stable keys and warning/blocker
  semantics.
- `validate` distinguishes "no policy needed for read-only checks" from
  "policy required before durable write."
- Missing or malformed policy produces stable diagnostics.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless assertions become snapshot-heavy rather than behavior-focused.

Commit message:
- `Report planning state project policy`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, read-only compatibility, JSON protocol shape, and
  stable malformed-policy diagnostics.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if read-only current/validate would require a durable state policy.
- Stop if policy discovery requires broad historical scans or downstream
  project-specific branches.

## Slice 3. Enforce State And Projection Target Policy

Scope:
- Enforce project policy for commands that write or preflight durable JSON state
  or projection targets.
- Apply policy to `bootstrap-state --state-file`, transition state writes,
  artifact registration with state files, closeout validation inputs, and the
  planned SQLite projection target contract where applicable.
- Ensure stdout and `/tmp` proof workflows remain available when policy is
  generated-only or missing.
- Add clear blockers when a write target conflicts with `committed`,
  `ignored-local`, `external`, `generated-only`, or `none` policy.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- `docs/plans/planning-state-tooling-plan.md`
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not implement SQLite rebuild or reports.
- Do not write actual durable state for codex-config unless a specific command
  invocation in tests uses a temp fixture path.
- Do not mutate root/program `CURRENT.md` from state policy.

Acceptance criteria:
- Durable state writes require compatible policy.
- Projection target preflights can be validated before the SQLite batch.
- Generated-only/missing policy allows stdout or explicit temp proof output but
  blocks committed/local durable writes.
- Diagnostics name the offending target, policy, and expected source of the
  project value.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Include temp-fixture CLI checks for allowed and rejected state-file targets.
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- Trigger test-quality review if target-policy fixtures become brittle or
  couple to private path helper names.

Commit message:
- `Enforce planning state project policy`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, write-target enforcement, no hidden state writes,
  and no SQLite implementation leakage.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if write-target policy requires a new durable location not declared by
  the project.
- Stop if enforcement would break existing stdout or temp proof workflows.

## Slice 4. Document Policies And Unblock SQLite

Scope:
- Document codex-config's project policy and an ignored-local example for
  Graphify-style overlays without making either universal.
- Update `docs/plans/planning-state-tooling-plan.md` to say SQLite must consume
  resolved project policy before choosing state or projection targets.
- Update program `CURRENT.md` and `LEDGER.md` to close PST-8, record evidence,
  and queue `planning-state-sqlite-projection` only after policy validation and
  review pass.
- Add or update `completed-slices.md` and `closeout.md` for this batch with
  bounded evidence pointers.

Allowed files/areas:
- `docs/plans/planning-state-tooling-plan.md`
- `docs/plans/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/`
- `CHANGELOG.md` if reusable skill or command behavior changed in prior slices
  and has not yet been recorded
- Tests only if documentation examples need a small fixture correction

Non-goals:
- Do not execute SQLite slices.
- Do not update GitHub issues unless explicitly requested.
- Do not commit downstream ignored-local artifacts.
- Do not create committed SQLite databases.

Acceptance criteria:
- PST-8 is closed with validation, review, and closeout evidence.
- SQLite batch is queued only after project policy is documented and validated.
- The SQLite dispatch/runway depends on project policy and does not choose
  state/projection ownership by itself.
- `current` and `validate` pass for `docs/plans` after closeout with only
  expected warnings.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py validate-closeout --root docs/plans --program planning-state-tooling --batch-id planning-state-project-policy --closeout docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/closeout.md --state-file <explicit temp state file>`
- Run ruff through `uvx` on touched Python files when Python or tests changed
  in the slice.
- Run `git diff --check`.

Test quality review:
- None unless tests are changed in this slice.

Commit message:
- `Document planning state project policy`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, closeout evidence completeness, ledger/current
  consistency, and SQLite dependency handoff.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if policy evidence is missing validation or review records.
- Stop if queuing SQLite would still leave project state/projection ownership
  implicit.

## Final Validation

Run after all slices are complete:
- `python -m pytest tests/test_planning_state.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- Focused project-policy CLI checks against committed, ignored-local,
  generated-only, external, none, and missing-policy temp fixtures.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py`
- `git diff --check`

Expected final state:
- PST-8 is closed in the program ledger.
- `planning-state-project-policy` is closed with bounded closeout evidence.
- `planning-state-sqlite-projection` is queued next and depends on resolved
  project policy.
- No downstream ignored-local artifacts are committed.
- No durable state file or SQLite projection is written without explicit
  project policy.

## Stop Conditions

- Stop if the implementation needs one universal state-file or projection path
  for every project.
- Stop if read-only workflows would fail without a durable policy.
- Stop if durable JSON state or SQLite files would be written without explicit
  project policy.
- Stop if scope expands into SQLite rebuild/report implementation.
- Stop if production code needs project-specific paths for Graphify or any
  other downstream project.
