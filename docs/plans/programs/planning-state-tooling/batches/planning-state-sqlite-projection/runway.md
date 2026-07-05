# Planning-State SQLite Projection Runway

## Purpose

Add an optional SQLite projection for planning-state operational reports. The
batch should make common report questions fast and bounded while preserving
Markdown and JSON state as the canonical workflow record.

This spec executes the `planning-state-sqlite-projection` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/dispatch.md`.

## Current Baseline

- Baseline state: `python scripts/planning_state.py current --root docs/plans`
  and `python scripts/planning_state.py validate --root docs/plans` pass with
  only existing architecture-runner redirect warnings.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/dispatch.md`.
- Included finding: PST-6.
- Existing owner seam: `scripts/planning_state.py`.
- Existing focused tests: `tests/test_planning_state.py`.
- Existing commands can report current state, validate state, allocate batch
  paths, register artifacts, select/queue batches in explicit state fixtures,
  validate/render bounded closeout evidence, and bootstrap companion JSON state
  from Layout v1 Markdown.
- Latest completed closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/closeout.md`.

## Assumptions

- SQLite is a projection, not canonical storage. If the database is deleted,
  workflows remain understandable and recoverable from Markdown planning
  artifacts, explicit JSON state, closeout evidence, runner receipts, telemetry
  summaries, and commits.
- Projection rebuilds use explicit command targets allowed by resolved project
  policy. No durable database location is selected for this repo by default.
- Reports expose compact command output for agents. Agents and runners do not
  query SQL directly or import private Python helpers.
- Projection input is bounded: paths, compact evidence indexes, state facts,
  receipts, manifests, telemetry summaries, statuses, warning/error codes,
  timestamps, durations, hashes, and short summaries.
- Graphify-style and runner-style behavior belongs in temp fixtures.
  Production code must not contain project-specific downstream paths, cache
  locations, validation commands, or overlay rules.
- `planning-state-project-policy` is closed. This batch consumes its resolved
  state-file and projection ownership policy instead of choosing durable target
  ownership by itself.

## Non-Goals

- Do not make SQLite required for `current`, `validate`, `bootstrap-state`,
  `select-batch`, `queue-batch`, `validate-closeout`, or `render-closeout`.
- Do not store full Markdown prose, dispatch/runway bodies, prompts,
  transcripts, long logs, or raw telemetry blobs in SQLite.
- Do not render or rewrite `CURRENT.md`, `LEDGER.md`, `dispatch.md`,
  `runway.md`, `closeout.md`, or `completed-slices.md` from SQLite.
- Do not change Batch Runway execution semantics.
- Do not change architecture-program runner phase execution.
- Do not create a future OSS Go runner or make it depend on Python internals.
- Do not update GitHub issues or comments.
- Do not choose state-file or projection ownership policy; consume the policy
  established by the preceding PST-8 batch.

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
- Use `full-runway` density because this batch defines optional database
  behavior and report command semantics.
- Workers must use temp fixtures for database and runner-artifact tests unless
  a slice explicitly targets this batch's planning docs for ledger closeout.
- Workers must not write to downstream project planning roots.
- Workers must not create a committed durable SQLite database unless a later
  explicit project policy selects a location.
- Stop before Slice 1 if `planning-state-project-policy` is not completed in
  the program ledger or if resolved project policy cannot be checked before a
  durable database target is used.

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
- For slices that add projection commands, include focused temp-fixture CLI
  checks for valid rebuilds, stale database rejection, missing evidence
  reports, runner-artifact summaries, and invalid database targets.
- Do not require live Graphify validation for this batch; use project-neutral
  temp fixtures when downstream Layout v1 behavior needs coverage.

Harness output:
- Existing `current`, `validate`, and `bootstrap-state` checks should write no
  live planning files.
- Projection tests should write SQLite databases only to test temp directories
  or explicit caller-provided paths allowed by resolved project policy.

Summary artifact:
- No generated summary artifact is required. Report compact stdout/stderr
  signals from CLI checks and the paths of any temp SQLite databases created by
  tests.

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
| 5. Document projection workflow and close PST-6 | Closed | `c8f5e12` | Passed `current`, `validate`, `bootstrap-state` to `/tmp/planning-state-sqlite-projection-state.json`, 169-test pytest, `validate-closeout`, temp projection rebuild, `pending-batches --program planning-state-tooling`, `batch-evidence`, and `git diff --check`. | runway_reviewer approved corrected final closeout evidence after fix loops. | Batch closed; no selected, active, or queued planning-state-tooling batch remains. |  |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Define SQLite projection contract | `0ae6e99` | success | `python -m pytest tests/test_planning_state.py -q` 152 passed; `python scripts/planning_state.py current --root docs/plans` passed with expected redirect warnings; `python scripts/planning_state.py validate --root docs/plans` passed with expected redirect warnings; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py` passed; `git diff --check`; review approved updated diff against `ec4179f` |
| 2. Add explicit projection rebuild | `1e5f47d` | success | `python -m pytest tests/test_planning_state.py -q` 157 passed; `python scripts/planning_state.py current --root docs/plans` passed with expected redirect warnings; `python scripts/planning_state.py validate --root docs/plans` passed with expected redirect warnings; temp rebuilds passed for all programs and `--program planning-state-tooling`; policy-incompatible `docs/plans/projection.sqlite` was rejected; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py` passed; `git diff --check`; review approved updated diff against `530b1d2` |
| 3. Add planning-state report commands | `fc46c41` | success | `python -m pytest tests/test_planning_state.py -q` 165 passed; `python scripts/planning_state.py current --root docs/plans` passed with expected redirect warnings; `python scripts/planning_state.py validate --root docs/plans` passed with expected redirect warnings; temp rebuild plus pending-batches, missing-closeout-evidence, and batch-evidence reports passed; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py` passed; `git diff --check`; review approved updated diff against `4d67a03` |
| 4. Add runner-artifact report coverage | `52f0cab` | success | `python -m pytest tests/test_planning_state.py -q` 169 passed; `python -m pytest tests/test_planning_state.py -q -k runner` 5 passed; `python scripts/planning_state.py current --root docs/plans` passed with expected redirect warnings; `python scripts/planning_state.py validate --root docs/plans` passed with expected redirect warnings; temp rebuild plus runner-latest-run, runner-failed-phases, and runner-context-pressure reports passed; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py` passed; `git diff --check`; review approved updated diff against `533f6b5` |
| 5. Document projection workflow and close PST-6 | `c8f5e12` | success | `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `python scripts/planning_state.py bootstrap-state --root docs/plans --state-file /tmp/planning-state-sqlite-projection-state.json`; `python -m pytest tests/test_planning_state.py -q` 169 passed; `python scripts/planning_state.py validate-closeout --root docs/plans --program planning-state-tooling --batch-id planning-state-sqlite-projection --closeout docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/closeout.md --state-file /tmp/planning-state-sqlite-projection-state.json`; `python scripts/planning_state.py rebuild-projection --root docs/plans --database /tmp/codex-config-final-projection.sqlite --state-file /tmp/planning-state-sqlite-projection-state.json --program planning-state-tooling`; `python scripts/planning_state.py report-projection --root docs/plans --database /tmp/codex-config-final-projection.sqlite --state-file /tmp/planning-state-sqlite-projection-state.json --program planning-state-tooling --report pending-batches`; `python scripts/planning_state.py report-projection --root docs/plans --database /tmp/codex-config-final-projection.sqlite --state-file /tmp/planning-state-sqlite-projection-state.json --report batch-evidence --program planning-state-tooling --batch-id planning-state-sqlite-projection`; `git diff --check`; review approved corrected final closeout evidence |

## Slice 1. Define SQLite Projection Contract

Scope:
- Define the versioned projection contract, schema metadata, source identity
  fields, stale-database checks, and allowed report facts.
- Add tests or fixture helpers proving that projection rows are bounded
  metadata, not canonical Markdown or transcript storage.
- Define how projection metadata records planning root, state fixture identity
  when supplied, source artifact hashes or mtimes where useful, schema version,
  build command, and build timestamp.
- Keep the contract compatible with existing `planning-state-tool-state`
  version `1` inputs.
- Consume resolved project policy for state-file and projection ownership;
  do not invent target locations inside this slice.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Optional focused note under
  `docs/plans/programs/planning-state-tooling/notes/`
- `docs/plans/planning-state-tooling-plan.md`
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command or contract behavior changes

Non-goals:
- Do not add the rebuild command yet unless a tiny parser hook is needed for
  tests.
- Do not write a live database for `docs/plans/`.
- Do not expose SQL or direct database mutation as the agent workflow.
- Do not change active-state resolution or closeout validation behavior.

Acceptance criteria:
- Tests define the accepted projection metadata and bounded table content.
- Tests reject attempts to store full Markdown bodies, transcript-like content,
  prompts, or long logs in projected rows.
- The contract can represent pending batches, artifact pointers, closeout
  evidence status, obligations, and runner summary facts without becoming
  canonical.
- Stale or mismatched database detection has a stable error code or report
  blocker shape.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless fixture builders become broad or heavily mocked.

Commit message:
- `Define planning state SQLite projection contract`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, projection contract clarity, bounded-data
  behavior, stale-database semantics, and absence of canonical-state changes.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the contract requires a durable database location not supplied by the
  resolved project policy.
- Stop if the contract needs to store full Markdown prose, prompts,
  transcripts, or raw logs.

## Slice 2. Add Explicit Projection Rebuild

Scope:
- Add a projection rebuild command that reads canonical planning facts and
  writes a SQLite database only to an explicit caller-provided target.
- Prefer a command shape such as:
  `python scripts/planning_state.py rebuild-projection --root <planning-root> --database <state.db> [--state-file <state.json>] [--program <slug>] [--format json]`.
- Validate database target ownership and avoid accidental writes under the
  active planning tree unless resolved project policy allows it.
- Populate bounded tables for root/program facts, batch rows, registered
  artifacts, obligations, closeout evidence pointers, transition receipts, and
  compact runner artifact summaries when fixture inputs provide them.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Protocol/plan docs directly tied to the rebuild command
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not create or commit a durable database for `docs/plans/`.
- Do not infer active state from historical flat filenames.
- Do not render or rewrite Markdown planning artifacts.
- Do not require SQLite for existing commands.

Acceptance criteria:
- Rebuild output validates the projection schema and source identity.
- Rebuild rejects missing, directory, absolute-escape, planning-root, or
  otherwise policy-incompatible database targets with stable blockers.
- Rebuild is deterministic enough for tests to compare bounded rows while
  ignoring build timestamp noise.
- Existing `current`, `validate`, and `bootstrap-state` behavior remains
  unchanged when no database exists.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Add focused CLI checks against temp database paths.
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless database fixture setup obscures behavior or over-mocks file IO.

Commit message:
- `Add planning state projection rebuild`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, explicit-target safety, deterministic rebuild
  behavior, no live planning Markdown writes, and no canonical dependency on
  SQLite.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if rebuild requires a committed database or hidden default location.
- Stop if database writes would need to occur inside downstream project roots
  without matching project policy.

## Slice 3. Add Planning-State Report Commands

Scope:
- Add compact report commands that read a validated projection and emit
  agent-facing text plus optional JSON protocol output.
- Cover at least:
  - pending executable batches;
  - missing closeout evidence;
  - batch to dispatch/runway/closeout/completed-slices/receipt/commit evidence
    lookup.
- Reports must validate projection identity against the requested root and
  optional state file and resolved project policy before using stored rows.
- Reports should provide blockers when a projection is stale, missing, from a
  different root, or missing required schema metadata.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Protocol/plan docs directly tied to report commands
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not expose raw SQL to agents.
- Do not add broad dashboard rendering.
- Do not update GitHub issues or comments.
- Do not make reports mutate planning state.

Acceptance criteria:
- Reports answer the three required planning-state questions from projection
  rows without scanning historical filenames at report time.
- Text output is compact and actionable for agents.
- JSON output, if added, includes protocol name/version, command, root, report
  kind, rows, warnings, blockers, and exit semantics.
- Missing or stale projection blockers are stable and test-covered.
- Policy-incompatible projection blockers are stable and test-covered.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Add focused CLI checks that rebuild a temp projection and run each report.
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- Trigger test-quality review if report fixtures become snapshot-heavy or assert
  formatting without behavior.

Commit message:
- `Add planning state projection reports`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, report usefulness, stale-projection rejection, JSON
  protocol shape if present, and absence of SQL-facing agent workflow.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the report command needs unbounded Markdown parsing, long logs, or
  transcript reconstruction.
- Stop if report semantics conflict with active-first Layout v1 pickup.

## Slice 4. Add Runner-Artifact Report Coverage

Scope:
- Extend projection rebuild/report fixtures to include bounded runner-style
  artifacts when provided by explicit paths, manifests, or temp fixtures.
- Cover latest run for a program, failed phases by reason, and context pressure
  summaries by phase.
- Keep the runner interop boundary at command/file protocols and compact
  artifacts. Do not import runner internals as the report source of truth.
- Treat missing runner artifacts as an empty optional report area, not a
  blocker for planning-state reports that do not ask for runner data.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Focused fixture data under tests if needed
- Protocol/plan docs directly tied to runner-artifact reporting
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not change architecture-program runner execution.
- Do not require a run artifact root for every planning program.
- Do not store raw telemetry blobs, prompts, logs, or transcripts.
- Do not make downstream runners import planning-state internals.

Acceptance criteria:
- Temp fixtures prove latest-run, failed-phase, and context-pressure reports
  from bounded runner-style artifacts.
- Reports identify absent runner artifacts without failing unrelated planning
  reports.
- The projection stores compact metadata and evidence pointers only.
- Existing architecture-program runner tests, if touched, continue to pass.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
- Add runner-artifact report CLI checks against temp fixtures.
- If architecture-program runner code is touched, run its focused tests as well.
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- Trigger test-quality review if runner fixtures become broad, brittle, or
  overly coupled to private runner helper names.

Commit message:
- `Report planning runner artifact summaries`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, runner interop boundary, bounded artifact storage,
  optional-runner behavior, and absence of project-specific paths.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if runner artifacts require broad transcript parsing or private runner
  object imports.
- Stop if a durable run artifact root is required but not supplied.

## Slice 5. Document Projection Workflow and Close PST-6

Scope:
- Document the SQLite projection workflow, report command usage, optional
  database target rules, and rebuild/delete safety.
- Update the planning-state tooling plan and program ledger to close PST-6
  only after validation and review evidence exists.
- Add or update `completed-slices.md` and `closeout.md` for this batch with
  bounded evidence pointers.
- Keep any closeout rendering explicit and registered.

Allowed files/areas:
- `docs/plans/planning-state-tooling-plan.md`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/`
- `CHANGELOG.md` if user-facing command behavior changed in prior slices and
  has not yet been recorded
- Tests only if documentation examples need a small fixture correction

Non-goals:
- Do not start a new planning-state batch.
- Do not update GitHub issues unless explicitly requested.
- Do not create a committed SQLite database.
- Do not broaden the workflow into a runner implementation plan.

Acceptance criteria:
- PST-6 is closed with validation, review, and closeout evidence.
- Documentation states that SQLite is optional, rebuildable, delete-safe, and
  never canonical, and that target ownership comes from project policy.
- Program `CURRENT.md` has no selected, active, or queued batch unless a future
  user request creates one.
- `current` and `validate` pass for `docs/plans` after closeout with only
  expected warnings.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py validate-closeout --root docs/plans --program planning-state-tooling --batch-id planning-state-sqlite-projection --closeout docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/closeout.md --state-file <explicit temp state file>`
- Run ruff through `uvx` on touched Python files when Python or tests changed
  in the slice.
- Run `git diff --check`.

Test quality review:
- None unless tests are changed in this slice.

Commit message:
- `Document planning state projection workflow`

Coding subagent brief:
- Implement only Slice 5 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 5 scope, closeout evidence completeness, ledger/current
  consistency, and preservation of optional SQLite semantics.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if closeout evidence is missing validation or review records.
- Stop if closing PST-6 would hide unresolved optional-projection blockers.

## Final Validation

Run after all slices are complete:
- `python -m pytest tests/test_planning_state.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- A temp projection rebuild/report CLI sequence covering the implemented report
  commands.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py`
- `git diff --check`

Expected final state:
- `planning-state-sqlite-projection` is closed with bounded closeout evidence.
- PST-6 is closed in the program ledger.
- No durable SQLite database is required or committed.
- Existing Markdown and JSON state commands still work without SQLite.
- Agents have compact report commands and do not need SQL access.
- Projection writes comply with resolved project policy.

## Stop Conditions

- Stop if SQLite becomes required for canonical active-state or closeout
  behavior.
- Stop if a durable database location is required but not allowed by resolved
  project policy.
- Stop if implementation needs to store full Markdown, prompts, transcripts,
  raw telemetry, or long logs in SQLite.
- Stop if reports would need to scan historical flat filenames instead of using
  current state, registered artifacts, state fixtures, or bounded runner
  artifacts.
- Stop if scope expands into runner execution or project-specific downstream
  behavior.
