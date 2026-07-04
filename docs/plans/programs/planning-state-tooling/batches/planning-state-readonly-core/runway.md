# Planning-State Read-Only Core Runway

## Purpose

Add a read-only `planning-state` diagnostic that reports active Planning
Artifact Layout v1 state and validates existing coordination artifacts without
mutating Markdown, JSON state, SQLite, or downstream project files.

This spec executes the `planning-state-readonly-core` batch selected by
`docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md`.

## Current Baseline

- Baseline commit: `1dd9bf8`.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md`.
- Included finding: PST-1.
- Owner seam: `scripts/planning_state.py` as the first planning-state facade.
- Existing runner concept owners: `scripts/architecture_program_runner*.py`.
- Existing active-state contract:
  `/home/alacasse/projects/codex-config/skills/planning-artifacts/SKILL.md`.
- Primary real fixture: `/home/alacasse/projects/graphify/my-docs/plans/`.
- Secondary fixture: this repo's `docs/plans/` Planning Artifact Layout v1
  migration state.

## Assumptions

- Markdown and JSON remain canonical. This batch only reads and reports.
- The first implementation can use Python stdlib only.
- `planning-state current` and `planning-state validate` may start as direct
  script subcommands under `scripts/planning_state.py`; packaging or install
  wiring is out of scope unless a later batch explicitly selects it.
- Graphify is fixture data for project-neutral behavior. Generic code must not
  contain Graphify-specific branches, cache paths, validation commands, or local
  overlay assumptions.
- Layout v1 active-state precedence is: project instructions, root
  `CURRENT.md`, listed program `CURRENT.md` files, then targeted ledgers or
  selected batch artifacts. Historical filenames and redirects are evidence,
  not active selection by themselves.

## Non-Goals

- Do not write canonical state, render Markdown, update ledgers automatically,
  or close batches.
- Do not add SQLite or a database abstraction.
- Do not implement path allocation, artifact registration, cross-batch
  obligations, closeout rendering, or migration bootstrap.
- Do not change Batch Runway, Architecture Program Runway, or existing runner
  execution semantics.
- Do not classify entire historical archives recursively.
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
- Treat this file creation session as `create-spec`; implementation starts in a
  later `execute-spec` session from the first pending active-ledger row.
- Use lean-runway density with explicit read-only and project-neutral guardrails.
- Workers may read the Graphify fixture path for validation but must not write
  to it.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/project-harness-production.md`

Focused validation commands:
- For production/test slices, run:
  `python -m pytest tests/test_planning_state.py -q`
- If touched files include existing runner surfaces, add the directly affected
  `tests/test_architecture_program_runner*.py` subset.
- For docs-only Slice 4, run `git diff --check` and the focused tests only if
  docs examples or command names changed from the implemented CLI contract.
- Use the repo-proven lint path on touched Python files:
  `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check <touched production/test files>`
- Always run `git diff --check`.

Integration harness:
- Dry-run CLI checks, no nested Codex, no writes:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `python scripts/planning_state.py current --root /home/alacasse/projects/graphify/my-docs/plans`
  `python scripts/planning_state.py validate --root /home/alacasse/projects/graphify/my-docs/plans`

Harness output:
- The CLI checks should write no files. If tests need fixture output, keep it in
  test temp directories.

Summary artifact:
- No generated summary artifact is required. Report compact stdout/stderr
  signals from the CLI checks.

Index refresh:
- None required for this repo after these Python/test/docs edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Existing uncommitted planning-layout changes under `docs/plans/` are assumed
  to be user-owned baseline context for this batch.
- Do not revert or commit unrelated user changes outside the active slice.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 3. Add `planning-state validate` | pending | | | | Document fallback workflow | Detects missing current files, bad redirects, selected batch directory problems, and stale active-state contradictions. |
| 4. Document read-only workflow | pending | | | | Final validation and closeout | Updates repo guidance without introducing write transitions or SQLite. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Define read-only state model | Slice 1 commit | success | `python -m pytest tests/test_planning_state.py -q`; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py`; `git diff --check`; reviewer clean |
| 2. Add `planning-state current` | Slice 2 commit | success | `python -m pytest tests/test_planning_state.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py current --root /home/alacasse/projects/graphify/my-docs/plans`; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py`; `git diff --check`; reviewer clean after warning-output fix |

## Slice 1. Define Read-Only State Model

Scope:
- Introduce the read-only planning-state owner seam, expected at
  `scripts/planning_state.py`.
- Define small structured types or dictionaries for root state, program state,
  selected/queued/active batch pointers, redirect evidence, warnings, and
  validation messages.
- Add fixture-driven tests for Layout v1 root `CURRENT.md`, listed program
  `CURRENT.md` files, redirect ledgers, historical files, and stale pickup
  contradictions.
- Keep the first owner API project-neutral; fixture builders may model Graphify
  and codex-config layouts, but production code must not special-case either.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- This spec ledger/archive rows

Non-goals:
- Do not add CLI subcommands yet except minimal `main` scaffolding if required
  for direct import safety.
- Do not write files or render Markdown.
- Do not add SQLite, path allocation, artifact registration, or closeout logic.
- Do not modify existing architecture-program runner modules.

Acceptance criteria:
- `tests/test_planning_state.py` proves the model can represent root and
  program `CURRENT.md` state for codex-config and Graphify-style fixtures.
- Tests prove redirect ledgers are followed or reported as redirects without
  treating old flat ledger paths as active sources.
- Tests prove historical dispatch/runway filenames and stale pickup notes can
  produce warnings without overriding root/program `CURRENT.md`.
- `scripts/planning_state.py` exposes one owner API that later slices consume;
  downstream slices must not duplicate parsing or state-precedence logic.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Define planning state read-only model`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, model ownership, fixture coverage, and absence of
  write behavior or project-specific production branches.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if reliable Layout v1 parsing requires a broader Markdown parser or
  canonical state schema decision not captured by the dispatch.
- Stop if Graphify fixture expectations conflict with Planning Artifact Layout
  v1 active-state precedence.

## Slice 2. Add `planning-state current`

Scope:
- Add a direct script CLI for `planning-state current`, likely:
  `python scripts/planning_state.py current --root <planning-root>`.
- Report layout version, planning root, active programs, selected dispatch,
  queued batch, active runway, latest closeout, next safe action, blockers, and
  warnings in compact agent-facing text or JSON-like output.
- Consume the Slice 1 owner API for all parsing and precedence logic.
- Add tests for codex-config and Graphify-style roots, including root
  `CURRENT.md` first and only listed program `CURRENT.md` files before ledgers.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- This spec ledger/archive rows

Non-goals:
- Do not add write commands.
- Do not add `validate` beyond helper functions needed by `current`.
- Do not scan archives or historical filenames to choose active work.
- Do not expose SQL or backing-store concepts.

Acceptance criteria:
- `current --root docs/plans` reports both active programs named by this repo's
  root `CURRENT.md`.
- `current --root /home/alacasse/projects/graphify/my-docs/plans` reports
  Graphify active programs from root/program `CURRENT.md` files and does not
  select old flat dispatch/runway filenames as active work.
- Output includes redirect/stale-context warnings when present, but active
  selection still comes from root/program `CURRENT.md`.
- Direct script execution works from the repo root.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py current --root /home/alacasse/projects/graphify/my-docs/plans`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Add planning state current command`

Coding subagent brief:
- Implement only Slice 2 from this spec and consume the Slice 1 owner API.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, CLI output contract, active-state precedence, and
  absence of archive-driven active selection.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if CLI output needs a durable schema that should be specified before
  implementation.
- Stop if the Graphify fixture is unavailable; do not replace it with
  hard-coded Graphify behavior in generic code.

## Slice 3. Add `planning-state validate`

Scope:
- Add `planning-state validate --root <planning-root>` using the same owner API.
- Validate root `CURRENT.md`, listed program `CURRENT.md` files, program
  ledgers, redirect ledgers, selected batch directories, queued runway paths,
  and stale active-state contradictions.
- Return non-zero only for structural errors that should block pickup; warnings
  should be explicit but not fatal unless they contradict active state.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- This spec ledger/archive rows

Non-goals:
- Do not auto-repair Markdown.
- Do not render `CURRENT.md` or `LEDGER.md`.
- Do not validate full archive history or bulk migration inventories.
- Do not add obligation or closeout evidence contracts.

Acceptance criteria:
- Validation passes for this repo's active `docs/plans/` state.
- Validation passes or reports only expected warnings for the Graphify fixture
  when root/program `CURRENT.md` files declare no selected dispatch, active
  runway, or queued batch.
- Tests cover fatal errors for missing root `CURRENT.md`, missing listed program
  `CURRENT.md`, invalid selected dispatch path, invalid queued runway path, and
  redirect ledgers that do not name a target.
- Tests cover warning-only stale pickup notes or historical compatibility files
  that do not override active state.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py validate --root docs/plans`
  `python scripts/planning_state.py validate --root /home/alacasse/projects/graphify/my-docs/plans`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Add planning state validation command`

Coding subagent brief:
- Implement only Slice 3 from this spec and consume the existing planning-state
  owner API.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, error versus warning boundaries, no-write
  behavior, and validation coverage for redirect and stale-context cases.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if validation needs write transitions, migration repair, or closeout
  evidence contracts to be useful.
- Stop if fatal/warning semantics conflict with Planning Artifact Layout v1.

## Slice 4. Document Read-Only Workflow

Scope:
- Document the read-only `planning-state current` and `planning-state validate`
  workflow in the active planning guidance.
- Update changelog only if the executed implementation makes a meaningful
  workflow behavior change.
- Keep write transitions, artifact registration, closeout validation, migration,
  and SQLite explicitly deferred to later ledger rows.

Allowed files/areas:
- `docs/plans/README.md`
- `docs/plans/planning-state-tooling-plan.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `CHANGELOG.md` only if implementation changed user-facing workflow behavior
- This spec ledger/archive rows

Non-goals:
- Do not update GitHub issues or comments.
- Do not rewrite the broader planning-state roadmap.
- Do not edit Graphify files.
- Do not add new selected batches.

Acceptance criteria:
- Docs tell future agents to run read-only diagnostics before broad planning
  tree scans when Layout v1 active-state files exist.
- Docs preserve the rule that Markdown and JSON are canonical and SQLite is
  deferred.
- Program ledger marks PST-1 closed only after Slice 3 validation evidence is
  clean; otherwise it records the exact remaining blocker.
- Current-state files point to the next safe action after this batch.

Validation:
- Use the selected project-harness-production profile for final validation.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `python scripts/planning_state.py current --root /home/alacasse/projects/graphify/my-docs/plans`
  `python scripts/planning_state.py validate --root /home/alacasse/projects/graphify/my-docs/plans`
- Run ruff through `uvx` on touched Python files if Python files changed in the
  final slice.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Document planning state diagnostics`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, docs accuracy against implemented commands, and
  deferral of write transitions and SQLite.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if documentation would need to promise write behavior that this batch did
  not implement.
- Stop if final validation reveals Graphify-specific assumptions in generic
  code.

## Final Validation

After the last slice:

- `python -m pytest tests/test_planning_state.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python scripts/planning_state.py current --root /home/alacasse/projects/graphify/my-docs/plans`
- `python scripts/planning_state.py validate --root /home/alacasse/projects/graphify/my-docs/plans`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py`
- `git diff --check`

No integration harness, nested Codex run, generated-doc refresh, index refresh,
GitHub update, or SQLite rebuild is required for this batch.

## Stop Conditions

- Stop if the batch would need to write canonical state, render Markdown, add
  SQLite, or migrate artifacts.
- Stop if generic code would need Graphify-specific branches, cache paths,
  validation commands, or local overlay assumptions.
- Stop if active-state rules conflict with Planning Artifact Layout v1.
- Stop if the Graphify fixture is unavailable in the execution environment and
  cannot be replaced by a project-neutral fixture plus explicit deferred live
  validation.
- Stop on dirty-file conflict, missing subagent support, scope drift, or
  unresolved validation/review failure under the standard Batch Runway contract.
