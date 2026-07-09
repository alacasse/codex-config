# Runner Contract Fixtures Runway

## Purpose

Prepare CCFG-1 runner business-logic extraction with implementation-neutral
contracts and validation fixtures before any extraction implementation begins.

This spec executes the `ccfg-1-runner-contract-fixtures` batch described by
`docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/dispatch.md`.
The batch is intentionally preparatory: it must clarify contracts and fixture
expectations, not move runner code, create a repository, create a repo skeleton,
or implement extraction.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/dispatch.md`.
- Included finding: CCFG-1.
- CCFG-1 source evidence: APR-26 in
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`.
- Existing contract artifact:
  `docs/plans/phase-runner-business-logic-contract.md`.
- Planning-state fixture guidance:
  `skills/planning-state/references/state-fixtures.md`.
- Runner artifact projection guidance:
  `skills/planning-state/references/runner-artifacts.md`.
- The current runner facade and tests remain the behavior source for existing
  CLI, phase-result, receipt, artifact, and final-summary compatibility.

## Assumptions

- The next safe CCFG-1 step is contract/fixture preparation, not package
  selection or implementation.
- Implementation-neutral contracts can be added or sharpened in planning docs
  and focused tests without changing runtime behavior.
- Planning-state interop should be command/file/schema based. If a later runner
  needs planning facts, it must consume explicit inputs or documented command
  outputs rather than import or mirror `scripts/planning_state.py` internals.
- Durable JSON planning-state fixtures must respect generated-only policy:
  prefer temporary/generated fixtures or test-owned builders unless project
  policy explicitly declares a durable fixture target.
- Facade compatibility expectations should preserve current dogfooding behavior
  while allowing a later generic core to use neutral names internally.

## Non-Goals

- Do not move runner code.
- Do not create a new repository.
- Do not create a repo skeleton.
- Do not implement runner extraction.
- Do not choose the final Go module name, repository name, package layout, CI
  layout, or public CLI/API beyond recording that those remain open.
- Do not implement branch-per-batch isolation, contract-drift review,
  runner-adapter authoring, or Baton dogfood diagnostics.
- Do not make `planning_state.py` part of the runner core.
- Do not move architecture-program phase prompts, Batch Runway contracts,
  Program Ledger semantics, GitHub issue policy, personal planning overlays, or
  Graphify-specific validation into a generic runner contract.
- Do not scan archived APR/PST ledgers beyond the APR-26 evidence named by the
  canonical CCFG-1 row.

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
- Use `lean-runway` density because this batch is contract, fixture, and
  compatibility-preparation work.
- Workers must not move runner source files, create a new repository, create a
  repo skeleton, or implement extraction.
- Workers must not write durable JSON planning state, SQLite projections, or
  runner artifacts unless a slice explicitly assigns a generated-only proof
  under `/tmp`.
- Workers must keep any static fixture examples portable and implementation
  neutral; test-generated fixtures are preferred for planning-state interop.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/test-only-topology.md`

Focused validation commands:
- For planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For planning-state interop fixture work:
  `python -m pytest tests/test_planning_state.py -q`
- For runner facade compatibility work:
  `python -m pytest tests/test_architecture_program_runner*.py -q`
- For contract-only slices that touch no tests:
  `git diff --check`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No new repository, package scaffold, or external runner harness.
- No durable SQLite database or JSON planning-state file is required.

Harness output:
- Existing `current` and `validate` checks should not write live planning files.
- If a slice needs generated fixture proof, write it to `/tmp` and record only
  the command/result in the worker report or committed test.

Index refresh:
- None required for this repo after these docs, test, and fixture-preparation
  edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.
- Treat the CCFG-1 ledger row, APR-26 evidence, and
  `phase-runner-business-logic-contract.md` as baseline planning context unless
  execution finds a direct contradiction.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 4. Non-goals and extraction stop gates | pending | | | | Confirm extraction cannot start from this batch alone | |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Contract boundary catalog | `03a6fae` | success; clarified implementation-neutral workflow, state, result, receipt, worker-adapter, and artifact boundaries while keeping codex-config runner behavior adapter-owned | `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`; reviewer `runway_reviewer` clean |
| 2. Planning-state interop fixture expectations | `409742d` | success; documented planning-state command/file/schema boundaries and added Layout v1 current/validate fixture expectations for selected, queued, active, and stale historical cases | `python -m pytest tests/test_planning_state.py -q`; `uvx ruff check tests/test_planning_state.py`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`; test-quality review clean after fix; reviewer `runway_reviewer` clean |
| 3. Facade compatibility expectations | `1f25a59` | success; documented runner facade compatibility gates and added focused checks for direct-script dry-run behavior and final-summary shape | `python -m pytest tests/test_architecture_program_runner*.py -q`; `uvx ruff check tests/test_architecture_program_runner.py tests/test_architecture_program_runner_run_loop.py`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`; test-quality review clean after fix; reviewer `runway_reviewer` clean |

## Slice 1. Contract Boundary Catalog

Scope:
- Sharpen implementation-neutral runner control-plane boundaries for workflow,
  run state, phase result, phase receipt, worker adapter, and run/batch
  artifact contracts.
- Prefer updating `docs/plans/phase-runner-business-logic-contract.md` or a
  nearby planning note over creating runtime code.
- Make generic concepts distinct from codex-config integration concepts:
  architecture-program phase names, Codex prompts, Batch Runway obligations,
  Program Ledger vocabulary, GitHub policy, and local planning policy stay out
  of the generic core.

Allowed files/areas:
- `docs/plans/phase-runner-business-logic-contract.md`
- `docs/plans/generic-phase-runner-workflow-contract.md`
- `docs/plans/programs/codex-config/notes/`
- This spec active-ledger/archive rows

Non-goals:
- Do not move or split `scripts/architecture_program_runner*.py`.
- Do not create target package files, Go module files, repository metadata, or
  CI files.
- Do not decide final package/runtime basics.

Acceptance criteria:
- Workflow, state, result, receipt, worker, and artifact boundaries are named
  as contracts rather than source-file destinations.
- The contract text states which current codex-config behaviors are integration
  adapter responsibilities, not generic runner-core responsibilities.
- The contract text identifies the validation evidence expected before a later
  extraction implementation can begin.

Validation:
- Use the selected profile plus:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless tests are changed in this slice.

Commit message:
- `Clarify runner contract boundaries`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep changes implementation neutral and documentation-focused.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope and contract-boundary clarity.
- Confirm the diff does not create code movement, package scaffolding, or
  hidden extraction implementation.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if boundary clarification requires source-file movement.
- Stop if the slice starts choosing target package/repository basics.

## Slice 2. Planning-State Interop Fixture Expectations

Scope:
- Define planning-state interop expectations for a future generic runner using
  explicit command, file, JSON, warning/error, and exit-code boundaries.
- Capture fixture expectations for Layout v1 `current` and `validate` cases:
  selected dispatch, queued runway, active runway, stale historical files, and
  warnings that must not become selected work.
- Prefer test-generated or temporary fixtures over committed JSON planning
  state unless project policy explicitly declares a durable fixture target.

Allowed files/areas:
- `docs/plans/phase-runner-business-logic-contract.md`
- `docs/plans/generic-phase-runner-workflow-contract.md`
- `docs/plans/programs/codex-config/notes/`
- `tests/test_planning_state.py`
- Existing planning-state test fixture helpers only if needed
- This spec active-ledger/archive rows

Non-goals:
- Do not import `scripts.planning_state` internals into runner tests.
- Do not add a durable project-tree JSON state file unless policy explicitly
  supports that exact target.
- Do not make projection reporting or runner artifact projection mandatory for
  ordinary planning-state interop.

Acceptance criteria:
- The interop contract says how a runner receives planning facts without
  inferring active work from historical filenames.
- Fixture expectations cover agreement between `current` and `validate` for
  Layout v1 roots and warning-only stale historical files.
- Tests or test-fixture builders make the expectations executable enough for a
  later extraction batch to consume.

Validation:
- Use the selected profile plus:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required if this slice adds or changes tests. Review should focus on whether
  fixtures protect behavior without freezing incidental Markdown wording.

Commit message:
- `Define planning-state interop fixtures`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep planning-state interop explicit and fixture-driven; do not couple a
  future runner core to `planning_state.py` internals.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, fixture behavior, and planning-state boundary
  clarity.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if fixture proof requires durable JSON state in an undeclared project
  location.
- Stop if the runner contract starts depending on planning-state private
  Python helpers.

## Slice 3. Facade Compatibility Expectations

Scope:
- Define compatibility expectations for the existing runner facade before any
  later extraction implementation can change internals.
- Cover current CLI/default bounds, direct script execution, phase-result
  schema strictness, receipt equality, structured artifact paths, input
  inventory linkage, dry-run behavior, resume behavior, and final summary
  shape.
- Add or tighten focused tests only where current expectations are not already
  executable.

Allowed files/areas:
- `docs/plans/phase-runner-business-logic-contract.md`
- `docs/plans/programs/codex-config/notes/`
- `tests/test_architecture_program_runner*.py`
- This spec active-ledger/archive rows

Non-goals:
- Do not alter the runner facade behavior.
- Do not move callers off the facade.
- Do not implement a compatibility adapter.
- Do not add branch-per-batch behavior.

Acceptance criteria:
- The compatibility contract distinguishes public facade behavior from
  internal generic-core translation details.
- Focused tests fail if current facade behavior needed for dogfooding is lost
  before extraction.
- Any compatibility gaps discovered are recorded as follow-up or stop-gate
  notes, not silently implemented as extraction work.

Validation:
- Use the selected profile plus:
  `python -m pytest tests/test_architecture_program_runner*.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required if this slice adds or changes tests. Review should focus on whether
  tests protect observable facade behavior without overfitting implementation
  internals.

Commit message:
- `Define runner facade compatibility gates`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Preserve runtime behavior; compatibility expectations and focused tests are
  the only intended outputs.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, facade compatibility coverage, and behavior
  preservation.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if compatibility proof requires changing current runner behavior.
- Stop if the slice starts implementing an adapter or generic core.

## Slice 4. Non-Goals And Extraction Stop Gates

Scope:
- Harden explicit non-goals, stop conditions, and closeout criteria for CCFG-1
  so later extraction cannot begin from ambiguous preparation text.
- Ensure the program ledger, dispatch, and contract artifacts agree that this
  batch prepares contracts and fixtures only.
- Record unresolved decisions that remain after this batch: target language,
  package/repository basics, public CLI/API name, compatibility promise, and
  extraction location.

Allowed files/areas:
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/`
- `docs/plans/phase-runner-business-logic-contract.md`
- `docs/plans/programs/codex-config/notes/`
- This spec active-ledger/archive rows

Non-goals:
- Do not close CCFG-1 until implementation, validation, review, and closeout
  evidence prove the contract/fixture preparation is complete.
- Do not select CCFG-2 through CCFG-5.
- Do not create a follow-up batch unless the user explicitly asks for
  `plan-batch` after this batch closes.

Acceptance criteria:
- CCFG-1 closeout criteria explicitly require implementation-neutral contracts,
  planning-state interop fixture expectations, and facade compatibility checks
  before extraction work can start.
- Stop conditions mention code moves, new repositories, repo skeletons,
  package scaffolds, hidden planning-state dependencies, and archived-ledger
  archaeology.
- Remaining extraction decisions are visible as unresolved follow-up decisions,
  not implied by this preparation batch.

Validation:
- Use the selected profile plus:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless tests are changed in this slice.

Commit message:
- `Harden runner extraction stop gates`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep finalization limited to preparation criteria and queued-batch evidence.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, stop-gate clarity, and planning-state consistency.
- Confirm no extraction implementation, repo skeleton, or package scaffold was
  introduced.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if finalization requires selecting or planning another CCFG row.
- Stop if the closeout text would imply extraction implementation is complete.

## Final Validation

Before closeout, run:

- `python -m pytest tests/test_planning_state.py -q`
- `python -m pytest tests/test_architecture_program_runner*.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `git diff --check`

Do not run nested Codex, create a repo, create a package skeleton, or run a
downstream project harness during this batch.

## Stop Conditions

- Stop on any attempt to move runner code.
- Stop on any attempt to create a new repository, repo skeleton, Go module,
  package scaffold, or CI scaffold.
- Stop on any attempt to implement runner extraction.
- Stop if work broadens into CCFG-2 through CCFG-5.
- Stop if planning-state interop requires importing or mirroring private
  `scripts/planning_state.py` internals in a runner core.
- Stop if durable JSON state, SQLite projections, or runner artifacts would be
  written without explicit compatible policy.
- Stop if archived APR/PST ledgers are needed beyond APR-26 evidence already
  named by CCFG-1.
- Stop on dirty-file conflicts outside the active slice scope.
