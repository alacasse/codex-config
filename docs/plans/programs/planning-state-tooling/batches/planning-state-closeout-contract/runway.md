# Planning-State Closeout Contract Runway

## Purpose

Add a bounded `closeout.md` contract for completed batches. The batch makes
closeout evidence validateable and renderable from explicit planning-state
facts without making agents reconstruct history from old filenames, transcripts,
or unbounded logs.

This spec executes the `planning-state-closeout-contract` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/dispatch.md`.

## Current Baseline

- Baseline state: `python scripts/planning_state.py current --root docs/plans`
  and `python scripts/planning_state.py validate --root docs/plans` pass with
  only existing redirect warnings.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/dispatch.md`.
- Included finding: PST-4.
- Existing owner seam: `scripts/planning_state.py`.
- Existing focused tests: `tests/test_planning_state.py`.
- Existing artifact registration supports `dispatch`, `runway`, `closeout`,
  `completed-slices`, `receipt`, and `output` artifact types.
- Existing transition receipts can carry batch-relevant obligation facts.

## Assumptions

- Markdown and JSON remain canonical.
- `closeout.md` is a compact evidence index. It should point to commits,
  receipts, validation outputs, reviews, and completed-slice archives rather
  than embed transcripts or long logs.
- Closeout validation can start from explicit fixture state, registered
  artifacts, and closeout Markdown. It does not need SQLite.
- Rendering closeout Markdown is allowed only when the caller provides an
  explicit target path or asks for stdout. Rendering must not implicitly rewrite
  root/program `CURRENT.md`, program ledgers, dispatches, or runways.
- Graphify-style planning roots may be represented by temp fixtures. Production
  code must not contain Graphify-specific branches, cache paths, validation
  commands, or overlay rules.

## Non-Goals

- Do not implement SQLite or a database abstraction.
- Do not bootstrap existing planning roots into a migration state; that is
  PST-5.
- Do not change Batch Runway execution semantics.
- Do not change architecture-program runner phase execution.
- Do not close live batches automatically or update GitHub issues.
- Do not render or rewrite `CURRENT.md`, `LEDGER.md`, `dispatch.md`, or
  `runway.md` from tool state.

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
- Use `full-runway` density because this batch defines a user-facing closeout
  artifact contract and new CLI behavior.
- Workers must use temp fixtures for write/render tests unless a slice
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
- For slices that add closeout commands, include focused temp-fixture CLI checks
  for valid and invalid closeout input.
- Do not require live Graphify validation for this batch; use Graphify-style
  temp fixtures when project-neutral behavior needs coverage.

Harness output:
- Existing `current` and `validate` checks should write no files.
- Closeout render tests should write only to test temp directories or stdout.

Summary artifact:
- No generated summary artifact is required. Report compact stdout/stderr
  signals from CLI checks and the paths of any temp closeout artifacts created
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
| 4. Document closeout workflow and state handoff | Pending |  |  |  |  |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Define closeout evidence contract | this commit | Added the bounded closeout evidence-index contract helper and focused contract tests; no CLI command or Markdown rendering added. | Validation: `python -m pytest tests/test_planning_state.py -q` (79 passed), `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py` (passed with existing `/usr/bin/python3.14` symlink warning), `git diff --check` (passed). Review: `runway_reviewer` clean against final diff basis `HEAD 6ccafe0` scoped to `scripts/planning_state.py` and `tests/test_planning_state.py`. |
| 2. Add closeout validation | this commit | Added `validate-closeout` JSON preflight for registered closeout evidence indexes with compact blockers for missing evidence, path ownership, non-file closeouts, and malformed artifact pointers; no rendering or live planning Markdown mutation added. | Validation: `python -m pytest tests/test_planning_state.py -q` (92 passed), `python scripts/planning_state.py validate --root docs/plans` (passed with existing redirect warnings), `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check CHANGELOG.md scripts/planning_state.py tests/test_planning_state.py` (passed with existing `/usr/bin/python3.14` symlink warning), `git diff --check` (passed). Review: `runway_reviewer` clean against final diff basis `HEAD e332699` scoped to `CHANGELOG.md`, `scripts/planning_state.py`, and `tests/test_planning_state.py`. |
| 3. Add explicit closeout rendering | this commit | Added `render-closeout` for deterministic pointer-first Markdown from explicit registered evidence, with stdout rendering by default and writes limited to the registered closeout target. | Validation: `python -m pytest tests/test_planning_state.py -q` (96 passed), `python scripts/planning_state.py current --root docs/plans` (passed with existing redirect warnings), `python scripts/planning_state.py validate --root docs/plans` (passed with existing redirect warnings), `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check CHANGELOG.md scripts/planning_state.py tests/test_planning_state.py` (passed with existing `/usr/bin/python3.14` symlink warning), `git diff --check` (passed). Review: `runway_reviewer` clean against final diff basis `HEAD cef290f` scoped to `CHANGELOG.md`, `scripts/planning_state.py`, and `tests/test_planning_state.py`. |

## Slice 1. Define Closeout Evidence Contract

Scope:
- Define a compact closeout evidence-index contract for `closeout.md`.
- Add fixture helpers or schema-oriented owner functions that identify required
  closeout fields and bounded sections.
- Required evidence should include batch ID, status, source dispatch, runway,
  completed-slices archive, commit or commit range, validation evidence, review
  evidence, transition or runner receipts when present, closed obligations,
  open/deferred obligations, and cleanup residue classification.
- Add tests for valid closeout examples and malformed examples with missing
  required pointers, unknown batch IDs, or unbounded log sections.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Optional focused note under
  `docs/plans/programs/planning-state-tooling/notes/`
- `docs/plans/planning-state-tooling-plan.md`
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command or contract behavior changes

Non-goals:
- Do not add a CLI command yet unless a tiny parser hook is needed for tests.
- Do not render closeout Markdown.
- Do not write state fixtures or live planning Markdown.
- Do not change architecture-program runner modules.

Acceptance criteria:
- Tests define the accepted closeout evidence-index shape.
- Tests reject transcript-like or unbounded log sections in closeout examples.
- The contract can represent closed and open obligations using the existing
  obligation fields.
- The contract references registered artifacts instead of inferring paths from
  historical filenames.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless fixture helpers become broad or heavily mocked.

Commit message:
- `Define planning state closeout contract`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, contract clarity, bounded-evidence behavior, and
  absence of implicit Markdown writes or project-specific branches.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if closeout evidence needs a public schema location or versioning policy
  not captured by this dispatch.
- Stop if the contract requires parsing long execution transcripts.

## Slice 2. Add Closeout Validation

Scope:
- Add closeout validation behavior that consumes explicit state fixture facts,
  registered artifacts, obligation facts, and a named `closeout.md` path.
- Validate batch identity, closeout path ownership, required registered
  artifacts, completed-slices pointer, commit evidence, validation evidence,
  review evidence, receipt pointers when present, and obligation evidence.
- Return structured blockers and warnings in the existing planning-state
  protocol style.
- Add CLI coverage if the implementation exposes validation through a command,
  likely `python scripts/planning_state.py validate-closeout ...`.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Protocol/plan docs directly tied to the validation contract
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not render closeout Markdown.
- Do not close or queue batches.
- Do not mutate state fixtures except where an explicit test fixture setup does
  so before validation.
- Do not validate historical archive contents recursively.

Acceptance criteria:
- Valid fixture closeouts pass with no blockers.
- Invalid fixture closeouts fail with stable blocker codes for missing
  registered closeout, missing completed-slices pointer, missing validation or
  review evidence, missing closed-obligation evidence, and batch/path mismatch.
- Existing `current`, `validate`, `allocate-batch`, `register-artifact`,
  `select-batch`, and `queue-batch` behavior remains compatible.
- Validation output is compact enough for an agent or runner preflight to act
  on without reading long logs.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py validate --root docs/plans`
- Add temp-fixture closeout validation CLI checks if a command is introduced.
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless closeout parsing gets complex enough to risk false confidence.

Commit message:
- `Validate planning state closeouts`

Coding subagent brief:
- Implement only Slice 2 from this spec and consume the Slice 1 contract owner.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, validation completeness, blocker specificity, and
  preservation of existing command behavior.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if validation requires inferring evidence from commit history instead of
  explicit closeout pointers.
- Stop if the validator would need SQLite or a persistent index.

## Slice 3. Add Explicit Closeout Rendering

Scope:
- Add rendering behavior for a bounded `closeout.md` evidence index from
  explicit inputs: registered artifact facts, completed-slices summary,
  validation/review/receipt pointers, commits, obligation facts, and cleanup
  residue classification.
- Rendering should support stdout and an explicit target path. Target-path
  writes must validate that the path is the registered closeout path for the
  batch.
- Add tests proving rendering is deterministic, compact, pointer-first, and
  rejected when required evidence is missing.
- Keep live root/program state and ledgers untouched.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Focused protocol/plan docs for the rendering command
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not generate a transcript, slice chronology, or long validation log.
- Do not rewrite `CURRENT.md`, `LEDGER.md`, `dispatch.md`, or `runway.md`.
- Do not update live planning docs unless the command caller explicitly passes
  the registered closeout target path.
- Do not mark the batch completed in tool state.

Acceptance criteria:
- Rendering from a complete fixture produces a stable Markdown closeout with
  bounded sections and all required pointers.
- Rendering to a path outside the registered batch directory is rejected.
- Rendering with missing closed-obligation evidence is rejected.
- The rendered closeout validates through Slice 2 behavior.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Add temp-fixture render CLI checks for stdout and explicit target-path
  behavior if a command is introduced.
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless snapshot-style assertions become large or brittle.

Commit message:
- `Render bounded planning state closeouts`

Coding subagent brief:
- Implement only Slice 3 from this spec and consume the Slice 1/2 contract and
  validation owners.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, deterministic rendering, target-path safety, and
  absence of implicit live planning rewrites.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if deterministic rendering requires broad runner receipt parsing not
  already represented by explicit inputs.
- Stop if output length grows beyond a compact evidence index.

## Slice 4. Document Closeout Workflow And State Handoff

Scope:
- Document the closeout validation/rendering workflow in the planning-state
  plan or a focused program note.
- Update `CHANGELOG.md` with the closeout contract problem, decision, and
  expected effect.
- Update this program ledger and `CURRENT.md` after execution so future agents
  see the completed closeout-contract batch and the next recommended batch.
- Keep PST-5 and PST-6 queued/deferred according to the ledger work order.

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
- Do not start PST-5 migration work.
- Do not add SQLite projection details beyond preserving it as deferred.

Acceptance criteria:
- Docs explain that closeout Markdown is a bounded pointer-first evidence
  index.
- The planning-state program points at the next safe action after this batch.
- PST-4 is marked closed only with validation, review, and closeout evidence.
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
- `Document planning state closeout workflow`

Coding subagent brief:
- Implement only Slice 4 from this spec after Slices 1-3 are complete.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, documentation accuracy, ledger/current-state
  consistency, and absence of premature PST-5/PST-6 work.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if closeout evidence from earlier slices is incomplete.
- Stop if the next recommended batch depends on unresolved PST-4 behavior.

## Final Validation

Run after the last slice:

- `python -m pytest tests/test_planning_state.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- Closeout validation/render CLI checks added by this batch against temp
  fixtures.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py`
- `git diff --check`

## Final Reporting

Report:
- commits by slice;
- validation commands and results;
- review outcomes;
- closeout artifact path if rendered;
- open or deferred obligations;
- cleanup residue classification;
- remaining PST-5/PST-6 risks;
- `orchestration_anomalies`.

## Batch Stop Conditions

- Stop if the implementation needs SQLite or a durable query database.
- Stop if closeout evidence must be inferred from transcripts, historical
  filenames, or broad archive scans.
- Stop if a command would rewrite live root/program `CURRENT.md`, ledgers,
  dispatches, or runways from tool state.
- Stop if production code needs Graphify-specific paths, validation commands,
  cache locations, or overlay rules.
- Stop if closeout output becomes a long log dump instead of a bounded evidence
  index.
