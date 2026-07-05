# Planning-State Migration Pilot Runway

## Purpose

Add a safe migration pilot for bootstrapping explicit planning-state JSON from
existing Planning Artifact Layout v1 Markdown roots. The batch should prove
that tool-owned state can be generated, validated, and consumed without hiding
or rewriting human-readable planning artifacts.

This spec executes the `planning-state-migration-pilot` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/dispatch.md`.

## Current Baseline

- Baseline state: `python scripts/planning_state.py current --root docs/plans`
  and `python scripts/planning_state.py validate --root docs/plans` pass with
  only existing redirect warnings.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/dispatch.md`.
- Included finding: PST-5.
- Existing owner seam: `scripts/planning_state.py`.
- Existing focused tests: `tests/test_planning_state.py`.
- Existing commands can report current state, validate state, allocate batch
  paths, register artifacts, select/queue batches in explicit state fixtures,
  and validate/render bounded closeout evidence.
- Latest completed closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/closeout.md`.

## Assumptions

- Markdown remains the human-readable planning surface and stays usable without
  a state fixture.
- Explicit JSON state is a companion tool-state artifact, not a replacement for
  `CURRENT.md`, `LEDGER.md`, dispatches, runways, closeouts, or completed-slice
  archives.
- Bootstrap generation should be dry-run by default or write only to an
  explicit caller-provided target.
- A real durable state-file location is not selected for this program. If the
  implementation needs to commit a generated state file, stop and get an
  explicit project value first.
- Graphify-style behavior belongs in temp fixtures that model Layout v1 roots;
  production code must not contain Graphify-specific paths, cache locations,
  validation commands, or overlay rules.

## Non-Goals

- Do not implement SQLite or a database abstraction.
- Do not render or rewrite `CURRENT.md`, `LEDGER.md`, `dispatch.md`,
  `runway.md`, `closeout.md`, or `completed-slices.md` from tool state.
- Do not change Batch Runway execution semantics.
- Do not change architecture-program runner phase execution.
- Do not update GitHub issues or comments.
- Do not create, move, or mutate downstream project planning roots.
- Do not close PST-6 or add operational reporting queries.

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
- Use `full-runway` density because this batch defines migration/bootstrap
  command behavior and explicit state-file safety.
- Workers must use temp fixtures for write-target tests unless a slice
  explicitly targets this batch's planning docs for ledger closeout.
- Workers must not write to `/home/alacasse/projects/graphify`.

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
- For slices that add migration/bootstrap commands, include focused
  temp-fixture CLI checks for valid dry-run output, explicit target writes,
  stale historical files, redirects, and invalid target paths.
- Do not require live Graphify validation for this batch; use Graphify-style
  temp fixtures when project-neutral behavior needs coverage.

Harness output:
- Existing `current` and `validate` checks should write no files.
- Migration/bootstrap tests should write only to test temp directories or
  stdout unless the slice deliberately updates this batch's planning docs.

Summary artifact:
- No generated summary artifact is required. Report compact stdout/stderr
  signals from CLI checks and the paths of any temp migration fixtures created
  by tests.

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
| 4. Document migration pilot handoff | Pending | | | | | |

## Orchestration Anomalies

orchestration_anomalies:
  - slice: 1
    severity: low
    category: validation_escalation
    observed: "`uvx ruff check` could not resolve PyPI inside the sandbox until rerun with approved network access."
    impact: "No validation gap remained; ruff passed after approval."
    action_taken: "Recorded the approval-dependent validation path for the slice receipt."
    follow_up: "None unless repeated uncached ruff fetches become noisy."

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Define migration bootstrap contract | this commit | Added the Layout v1 bootstrap contract metadata for `planning-state-tool-state` version 1, tightened validation to require the complete contract field/code sets, and documented which Markdown facts remain human-owned versus safe JSON state. | Validation: `python -m pytest tests/test_planning_state.py -q` (102 passed), `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py` (passed with existing `/usr/bin/python3.14` symlink warning after approved network access), `git diff --check` (passed). Review: `runway_reviewer` approved the recovered diff against `HEAD 6a7f8fc` scoped to `CHANGELOG.md`, `docs/plans/planning-state-tooling-plan.md`, `scripts/planning_state.py`, and `tests/test_planning_state.py`. |
| 2. Add explicit bootstrap state generation | this commit | Added `bootstrap-state` to generate validated v1 planning-state fixtures from Layout v1 Markdown, print by default, write only to explicit JSON targets outside the planning root, atomically replace target files, and register existing co-located batch artifacts including ID-only queued batches. | Validation: `python -m pytest tests/test_planning_state.py -q` (107 passed), `python scripts/planning_state.py current --root docs/plans` (passed with existing redirect warnings), `python scripts/planning_state.py validate --root docs/plans` (passed with existing redirect warnings), `python scripts/planning_state.py bootstrap-state --root docs/plans --program planning-state-tooling --format json` (passed), `python scripts/planning_state.py bootstrap-state --root docs/plans --program planning-state-tooling --state-file /tmp/codex-config-bootstrap-state-slice2.json --format json` (passed), `python scripts/planning_state.py validate --root docs/plans --state-file /tmp/codex-config-bootstrap-state-slice2.json --format json` (passed), `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py` (passed with existing `/usr/bin/python3.14` symlink warning), `git diff --check` (passed). Review: `runway_reviewer` approved the recovered diff against `HEAD bf8ba95` scoped to `CHANGELOG.md`, `scripts/planning_state.py`, and `tests/test_planning_state.py`. |
| 3. Validate migrated state fixtures | this commit | Added migrated state-file consistency validation for active Markdown facts, registered active pointers, duplicate/colliding artifacts, active-state conflicts, root mismatches, and malformed obligations; generated codex-config and Graphify-style fixtures now round-trip through `current`/`validate --state-file`, including ID-only queued batch normalization. | Validation: `python -m pytest tests/test_planning_state.py -q` (117 passed), `python scripts/planning_state.py current --root docs/plans` (passed with existing redirect warnings), `python scripts/planning_state.py validate --root docs/plans` (passed with existing redirect warnings), `python scripts/planning_state.py bootstrap-state --root docs/plans --program planning-state-tooling --state-file /tmp/codex-config-bootstrap-state-slice3.json --format json` (passed), `python scripts/planning_state.py validate --root docs/plans --state-file /tmp/codex-config-bootstrap-state-slice3.json --format json` (passed), `python scripts/planning_state.py current --root docs/plans --state-file /tmp/codex-config-bootstrap-state-slice3.json --format json` (passed), `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py` (passed with existing `/usr/bin/python3.14` symlink warning), `git diff --check` (passed). Review: `runway_reviewer` approved the recovered diff against `HEAD bf659dc` scoped to `CHANGELOG.md`, `scripts/planning_state.py`, and `tests/test_planning_state.py`. |

## Slice 1. Define Migration Bootstrap Contract

Scope:
- Define the migration bootstrap contract for converting existing Layout v1
  Markdown facts into explicit planning-state fixture data.
- Cover root/program `CURRENT.md`, program ledgers, known batch rows,
  co-located batch artifacts, redirects, latest closeout pointers, selected or
  queued state, and obligations when present.
- Add tests or helper fixtures for codex-config and Graphify-style planning
  roots that prove active-first pickup and redirect/historical-file handling.
- Keep the contract compatible with existing `planning-state-tool-state`
  version `1` unless the slice finds a concrete missing field that requires a
  versioned extension.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Optional focused note under
  `docs/plans/programs/planning-state-tooling/notes/`
- `docs/plans/planning-state-tooling-plan.md`
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command or contract behavior changes

Non-goals:
- Do not add a write command yet unless a tiny parser hook is needed for tests.
- Do not render or rewrite live planning Markdown.
- Do not write a durable state fixture for `docs/plans/`.
- Do not add SQLite or runner execution behavior.

Acceptance criteria:
- Tests define which Markdown facts become fixture fields and registered
  artifact facts.
- Historical flat files and redirect ledgers are represented as warnings or
  compatibility evidence, not selected or queued state.
- The contract can represent the current `planning-state-migration-pilot`
  queued batch without hand-written path inference by future agents.
- The contract explicitly states what is left to Markdown and what is safe for
  JSON state.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless fixture builders become broad or heavily mocked.

Commit message:
- `Define planning state migration contract`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, contract clarity, active-first migration behavior,
  and absence of implicit Markdown writes or project-specific branches.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if migration requires a durable state-file location not supplied by the
  spec or user.
- Stop if the contract requires scanning broad archives or parsing execution
  transcripts.

## Slice 2. Add Explicit Bootstrap State Generation

Scope:
- Add migration/bootstrap behavior that reads an existing Layout v1 planning
  root and produces an explicit planning-state fixture document.
- Prefer a command shape such as:
  `python scripts/planning_state.py bootstrap-state --root <planning-root> [--program <slug>] [--state-file <state.json>] [--format json]`.
- Without `--state-file`, print the generated fixture or receipt to stdout and
  write nothing.
- With `--state-file`, write only that explicit target after validating the
  target path and generated fixture.
- Include artifact registrations for co-located batch `dispatch.md`,
  `runway.md`, `closeout.md`, and `completed-slices.md` when those files exist.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Protocol/plan docs directly tied to the bootstrap command
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not rewrite `CURRENT.md`, ledgers, dispatches, runways, closeouts, or
  completed-slices archives.
- Do not select, queue, close, or supersede batches as a side effect.
- Do not infer active state from historical flat filenames.
- Do not commit generated live state for `docs/plans/`.

Acceptance criteria:
- Dry-run/bootstrap output validates as `planning-state-tool-state` version `1`
  or a deliberately versioned compatible extension.
- Explicit target writes are atomic enough to avoid partial corrupt state
  fixtures on validation failure.
- Invalid state targets, path escapes, malformed program slugs, and existing
  active-state contradictions produce stable blockers or usage errors.
- Existing `current`, `validate`, `allocate-batch`, `register-artifact`,
  `select-batch`, `queue-batch`, `validate-closeout`, and `render-closeout`
  behavior remains compatible.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Add temp-fixture bootstrap CLI checks for stdout and explicit state-file
  writes.
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless migration parsing gets complex enough to risk false confidence.

Commit message:
- `Bootstrap planning state fixtures`

Coding subagent brief:
- Implement only Slice 2 from this spec and consume the Slice 1 migration
  contract owner.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, target-write safety, generated fixture validity,
  and preservation of existing command behavior.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if target writes need a project-level durable state location that has
  not been selected.
- Stop if generation would need to rewrite Markdown to become correct.

## Slice 3. Validate Migrated State Fixtures

Scope:
- Add validation coverage that consumes generated state fixtures with existing
  `current` and `validate --state-file` behavior.
- Prove generated codex-config and Graphify-style temp fixtures preserve
  active-first pickup, redirect warnings, historical-file warnings, registered
  artifact facts, queued batch state, latest closeout pointers, and obligation
  facts when present.
- Add focused CLI checks that bootstrap a temp state file and immediately
  validate it.
- Ensure malformed migrated fixtures produce actionable blockers without
  traceback output.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Focused protocol/plan docs for validation semantics
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing validation behavior changes

Non-goals:
- Do not add SQLite projection or query commands.
- Do not require live Graphify file access.
- Do not use migration validation to close or queue batches.
- Do not update GitHub issues.

Acceptance criteria:
- Bootstrap-plus-validate passes for codex-config and Graphify-style temp
  fixtures.
- Validation rejects mismatched root, duplicate artifacts, malformed
  obligation records, active-state contradictions, and unregistered active
  batch pointers with stable message codes.
- Current/validate output remains compact and usable by future runner preflight
  adapters.
- Markdown-only roots still work when no state file is supplied.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless tests rely on large golden JSON snapshots.

Commit message:
- `Validate migrated planning state`

Coding subagent brief:
- Implement only Slice 3 from this spec and consume the Slice 1/2 contract and
  bootstrap owners.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, migration validation completeness, blocker
  specificity, and absence of live downstream project mutation.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if validation depends on broad archive scans or Git history inference.
- Stop if generated state cannot be validated without choosing a new canonical
  state-file version.

## Slice 4. Document Migration Pilot Handoff

Scope:
- Document the migration/bootstrap workflow in the planning-state plan or a
  focused program note.
- Update `CHANGELOG.md` with the migration pilot problem, decision, and
  expected effect.
- Update this program ledger and `CURRENT.md` after execution so future agents
  see PST-5 closed or partially closed with explicit evidence.
- Keep PST-6 deferred unless the completed migration evidence directly changes
  the SQLite-projection preconditions.
- Render or validate this batch's `closeout.md` only through explicit
  closeout command targets added by the previous completed batch.

Allowed files/areas:
- `docs/plans/planning-state-tooling-plan.md`
- Optional focused note under
  `docs/plans/programs/planning-state-tooling/notes/`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- This batch `closeout.md` and `completed-slices.md` if created by explicit
  closeout rendering
- `CHANGELOG.md`
- Tests only if docs examples are executable

Non-goals:
- Do not update GitHub issues or comments.
- Do not start PST-6 SQLite projection work.
- Do not add permanent generated state under `docs/plans/` unless a durable
  state-file location has been explicitly selected.

Acceptance criteria:
- Docs explain that migration bootstraps explicit state while preserving
  Markdown as human-readable coordination state.
- The planning-state program points at the next safe action after this batch.
- PST-5 is marked closed only with validation, review, and closeout evidence.
- Existing planning-state diagnostics still pass with only known redirect
  warnings.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`
- Run focused tests only if docs examples or command names changed after
  implementation.

Test quality review:
- None.

Commit message:
- `Document planning state migration pilot`

Coding subagent brief:
- Implement only Slice 4 from this spec after Slices 1-3 are complete.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, documentation accuracy, ledger/current-state
  consistency, closeout evidence, and absence of premature PST-6 work.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if migration evidence from earlier slices is incomplete.
- Stop if the next recommended batch depends on unresolved PST-5 behavior.

## Final Validation

Run after the last slice:

- `python -m pytest tests/test_planning_state.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- Bootstrap/migration CLI checks added by this batch against temp fixtures.
- Closeout validation/render CLI checks for this batch if closeout is rendered.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py`
- `git diff --check`

## Final Reporting

Report:
- commits by slice;
- validation commands and results;
- review outcomes;
- bootstrap state target behavior;
- closeout artifact path if rendered;
- open or deferred obligations;
- cleanup residue classification;
- remaining PST-6 risks;
- `orchestration_anomalies`.

## Batch Stop Conditions

- Stop if the implementation needs SQLite or a durable query database.
- Stop if generated state must rewrite Markdown planning artifacts.
- Stop if active state must be inferred from transcripts, historical filenames,
  or broad archive scans.
- Stop if a durable state-file location is required but not explicitly
  selected by project instructions, active spec, or user direction.
- Stop if production code needs Graphify-specific paths, validation commands,
  cache locations, or overlay rules.
