# Planning-State Write Transitions Runway

## Purpose

Add explicit planning-state command/file protocols for batch path allocation,
artifact registration, batch selection, and cross-batch obligations. The batch
keeps Markdown and JSON canonical, preserves read-only diagnostics, and gives
future runners a fixture-tested interop surface instead of Markdown scraping or
Python imports.

This spec executes the `planning-state-write-transitions` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/dispatch.md`.

## Current Baseline

- Baseline state: `python scripts/planning_state.py current --root docs/plans`
  and `python scripts/planning_state.py validate --root docs/plans` pass with
  only redirect warnings.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/dispatch.md`.
- Included findings: PST-2, PST-3, PST-7.
- Existing owner seam: `scripts/planning_state.py`.
- Existing focused tests: `tests/test_planning_state.py`.
- Related interop contract:
  `docs/plans/phase-runner-business-logic-contract.md` PBC-15.

## Assumptions

- Existing `current` and `validate` behavior remains backward compatible.
- The first write-transition implementation may use Python stdlib only.
- New commands may write isolated fixture state or explicit state/receipt files
  in tests, but must not rewrite live repo Markdown as part of normal
  diagnostics or validation.
- JSON state and receipts are allowed as canonical machine-readable facts when
  explicitly named by a command. Markdown remains the human-readable planning
  surface.
- The future Go runner consumes planning-state facts through documented command
  output or file protocols. It must not import Python internals or duplicate
  codex-config Markdown heuristics.
- Graphify remains fixture data for project-neutral behavior. Production code
  must not contain Graphify-specific branches, cache paths, validation commands,
  or overlay rules.

## Non-Goals

- Do not implement SQLite or a database abstraction.
- Do not render or rewrite live `CURRENT.md`, `LEDGER.md`, `dispatch.md`,
  `runway.md`, `closeout.md`, or `completed-slices.md` from tool state.
- Do not add closeout evidence rendering; that is PST-4.
- Do not bootstrap existing planning roots into a full migration state; that is
  PST-5.
- Do not change Batch Runway or architecture-program runner execution
  semantics.
- Do not make `scripts/planning_state.py` part of the runner core.
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
- Use `full-runway` density for the interop and transition boundary because it
  defines command/file behavior that later runners may consume.
- Workers may read the Graphify fixture path for validation but must not write
  to it.
- New transition commands must be tested against temp fixture roots or explicit
  test state files before any later batch can use them on live planning docs.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/project-harness-production.md`

Focused validation commands:
- For production/test slices, run:
  `python -m pytest tests/test_planning_state.py -q`
- Add focused runner interop tests only if a slice touches runner-facing
  contract docs or runner protocol helpers.
- Use the repo-proven lint path on touched Python files:
  `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check <touched production/test files>`
- Always run `git diff --check`.

Integration harness:
- Dry-run CLI checks, no nested Codex:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `python scripts/planning_state.py current --root /home/alacasse/projects/graphify/my-docs/plans`
  `python scripts/planning_state.py validate --root /home/alacasse/projects/graphify/my-docs/plans`
- Any command that writes state, receipts, or fixtures must target a test
  temporary directory or an explicit path under the test tmp root.

Harness output:
- Existing `current` and `validate` checks should write no files.
- Write-transition tests should keep generated state, receipts, and fixture
  Markdown in test temp directories.

Summary artifact:
- No generated summary artifact is required. Report compact stdout/stderr
  signals from CLI checks and the paths of any temp fixture receipts created by
  tests.

Index refresh:
- None required for this repo after these Python/test/docs edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not write to `/home/alacasse/projects/graphify/my-docs/plans/` outside
  read-only validation commands.
- Do not revert or commit unrelated user changes outside the active slice.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Define protocol and state schema | `bb4b61c` | success | `python -m pytest tests/test_planning_state.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans --format json`; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py`; `git diff --check`; reviewer approved after wrapped-field fix |
| 2. Add path allocation and artifact registration | `0b85f6a` | success | `python -m pytest tests/test_planning_state.py -q`; `python scripts/planning_state.py validate --root docs/plans`; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py`; `git diff --check`; reviewer clean after path-component validation fix |
| 3. Add batch selection and queue transitions | `e46cb52` | success | `python -m pytest tests/test_planning_state.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py`; `git diff --check`; reviewer approved after exact ledger-batch validation fix |
| 4. Add obligation tracking and interop validation | Slice 4 commit | success | `python -m pytest tests/test_planning_state.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `python scripts/planning_state.py current --root /home/alacasse/projects/graphify/my-docs/plans`; `python scripts/planning_state.py validate --root /home/alacasse/projects/graphify/my-docs/plans`; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py`; `git diff --check`; reviewer clean after state-file root isolation fix |

## Slice 1. Define Protocol And State Schema

Scope:
- Define the versioned planning-state facts protocol used by `current` and
  `validate`, including JSON shape, warning/error shape, and exit-code meaning.
- Define the minimal explicit state/receipt schema that later transition
  commands will write in test fixture roots.
- Add tests proving text output remains compatible while JSON/protocol output is
  strict and stable enough for runner interop fixtures.
- Document the command/file boundary in
  `docs/plans/planning-state-tooling-plan.md` or a small adjacent protocol note
  if the implementation needs more detail than code comments.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- `docs/plans/planning-state-tooling-plan.md`
- Optional focused protocol note under `docs/plans/programs/planning-state-tooling/notes/`
- This spec ledger/archive rows
- `CHANGELOG.md` if behavior-facing command output changes

Non-goals:
- Do not add mutating commands yet.
- Do not render Markdown from JSON state.
- Do not change runner modules.
- Do not make JSON output the only output format for existing users.

Acceptance criteria:
- Existing text `current` and `validate` output remains accepted by current
  tests.
- A machine-readable protocol shape exposes root facts, program facts,
  warnings, blockers, validation messages, and exit-code semantics.
- Tests reject unsupported protocol versions or malformed state/receipt
  fixture objects.
- Runner interop language says consumers use command/file outputs, not Python
  imports or Markdown filename inference.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless the slice substantially rewrites fixture helpers.

Commit message:
- `Define planning state protocol schema`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, protocol clarity, backward compatibility, and the
  absence of runner imports or Graphify-specific production branches.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the protocol needs a public schema location or versioning policy that
  is not captured by the dispatch.
- Stop if JSON output would require breaking existing text output.

## Slice 2. Add Path Allocation And Artifact Registration

Scope:
- Add command behavior that computes canonical Layout v1 batch and artifact
  paths for a program/batch without agents hand-allocating paths.
- Add artifact registration semantics for dispatch, runway, closeout, receipt,
  and output paths against an explicit fixture state file or dry-run output.
- Validate path ownership, batch-directory co-location, collisions, path
  escapes, absolute-path policy, and unsupported artifact types.
- Keep dry-run output usable before a state file exists.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Protocol note or planning-state plan updates directly tied to command
  behavior
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not create real batch directories in live `docs/plans/` from the command.
- Do not render or rewrite Markdown ledgers or `CURRENT.md`.
- Do not add selection/queue state transitions beyond registration facts.
- Do not add SQLite.

Acceptance criteria:
- Tests prove the tool can compute the canonical paths for
  `dispatch.md`, `runway.md`, `closeout.md`, and `completed-slices.md` under:
  `docs/plans/programs/<program>/batches/<batch-id>/`.
- Tests prove artifact registration rejects missing program roots, batch
  collisions, unsupported artifact types, and paths outside the planning root.
- Dry-run output is sufficient for an agent to create the same co-located batch
  directory by hand when mutation is not requested.
- Existing `current` and `validate` behavior remains unchanged.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py validate --root docs/plans`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless command fixture setup becomes broad or heavily mocked.

Commit message:
- `Add planning state artifact registration`

Coding subagent brief:
- Implement only Slice 2 from this spec and consume the Slice 1 protocol/state
  owner.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, path-allocation correctness, path safety,
  co-location semantics, and preservation of read-only diagnostics.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if canonical path allocation needs project-specific roots not discoverable
  from Layout v1 state or explicit command arguments.
- Stop if registration semantics would silently rewrite live planning Markdown.

## Slice 3. Add Batch Selection And Queue Transitions

Scope:
- Add command behavior for selecting a dispatch and queueing a runway against
  explicit fixture state, with transition receipts suitable for runner
  preflight.
- Enforce that a program has at most one selected dispatch, active runway, or
  queued batch at a time.
- Validate that selected and queued artifacts exist, belong to the same batch
  directory, and match the program ledger's known batch row when the ledger row
  is available.
- Keep transition writes isolated to explicit fixture state/receipt paths in
  tests; do not render Markdown.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Protocol note or planning-state plan updates directly tied to transition
  receipts
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not implement active execution state or Batch Runway slice ledgers.
- Do not close batches.
- Do not update GitHub issues.
- Do not change architecture-program runner transition code.

Acceptance criteria:
- Tests prove selecting a dispatch and queueing a runway produce strict
  transition facts or receipts with program, batch, artifact paths, warnings,
  and blockers.
- Tests prove the command refuses multiple active artifacts, missing artifacts,
  cross-program paths, stale selected dispatches, and queue attempts that bypass
  the registered dispatch/runway pair.
- Existing `validate` still reports active-state conflicts from Markdown
  `CURRENT.md` without requiring JSON state.
- Runner-facing docs or protocol notes explain how a runner can consume the
  transition receipt without importing planning-state internals.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless fixture mutation logic starts hiding behavior behind excessive
  mocking.

Commit message:
- `Add planning state batch transitions`

Coding subagent brief:
- Implement only Slice 3 from this spec and consume the established protocol and
  registration owner from earlier slices.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, active-state conflict handling, transition receipt
  semantics, and the runner interop boundary.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if selecting or queueing requires rendering Markdown to be meaningful.
- Stop if the transition receipt would become a hidden runner dependency
  instead of an explicit command/file protocol.

## Slice 4. Add Obligation Tracking And Interop Validation

Scope:
- Add first-class obligation records with IDs, owners, source batch, target
  batch or close condition, status, and evidence path fields.
- Add validation output that reports open, closed, missing-owner, duplicate-ID,
  and orphaned-obligation states.
- Connect obligation facts to batch selection/queue receipts so later closeout
  work can require bounded evidence without archaeology.
- Add golden interop fixture coverage showing a future runner can consume
  planning-state facts without parsing Markdown prose.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- `docs/plans/planning-state-tooling-plan.md`
- Optional focused protocol note under `docs/plans/programs/planning-state-tooling/notes/`
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not render `closeout.md`.
- Do not automatically close obligations from commits, GitHub comments, or
  runner transcripts.
- Do not add SQLite projection tables.
- Do not make obligation fields architecture-program specific.

Acceptance criteria:
- Tests prove obligations have stable IDs, owners, close conditions, statuses,
  and evidence paths.
- Tests prove validation flags duplicate IDs, missing owners, missing close
  conditions, missing evidence for closed obligations, and orphaned obligations
  whose source batch no longer exists in fixture state.
- Interop fixture output includes planning facts and obligations in a shape a
  runner can consume as explicit inputs.
- Existing read-only Markdown diagnostics continue to work for roots that have
  no planning-state JSON.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `python scripts/planning_state.py current --root /home/alacasse/projects/graphify/my-docs/plans`
  `python scripts/planning_state.py validate --root /home/alacasse/projects/graphify/my-docs/plans`
- Run ruff through `uvx` on touched Python files.
- Run `git diff --check`.

Test quality review:
- None unless the obligation tests become heavily implementation-coupled.

Commit message:
- `Add planning state obligations`

Coding subagent brief:
- Implement only Slice 4 from this spec and consume the earlier protocol,
  registration, and transition owners.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, obligation semantics, interop fixture usefulness,
  and avoidance of closeout rendering or runner coupling.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if obligation closure semantics require the PST-4 closeout contract
  before IDs and validation can be represented.
- Stop if the implementation starts inferring obligations from historical prose
  instead of explicit records.

## Final Validation

After all slices are complete, run:

- `python -m pytest tests/test_planning_state.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python scripts/planning_state.py current --root /home/alacasse/projects/graphify/my-docs/plans`
- `python scripts/planning_state.py validate --root /home/alacasse/projects/graphify/my-docs/plans`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/planning_state.py tests/test_planning_state.py`
- `git diff --check`

If docs or runner contract files are touched, reread the affected sections and
confirm they still keep planning-state diagnostics separate from runner core
execution.

## Stop Conditions

- Stop if a slice needs to render or rewrite live planning Markdown from tool
  state.
- Stop if a slice needs SQLite or any database abstraction.
- Stop if a slice needs Graphify-specific production branches, cache paths,
  validation commands, or overlay assumptions.
- Stop if a slice makes an architecture-program runner module import
  `scripts.planning_state` as an internal dependency.
- Stop if the command/file protocol is not explicit enough for a future runner
  to consume without Markdown filename inference.
- Stop on dirty-file conflict, scope drift, missing subagent support,
  unresolved validation failure, or any standard Batch Runway stop condition.
