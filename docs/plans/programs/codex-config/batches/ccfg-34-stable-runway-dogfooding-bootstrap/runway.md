# CCFG-34 Stable Runway Dogfooding Bootstrap Runway

## Purpose

Execute CCFG-34 as one temporary stable-generation migration batch. Establish a
project-owned vertical planning policy, reuse the existing architecture-program
runner for fresh coordinator execution units, add bounded read-only recovery
advice, self-dogfood those boundaries, and leave a mechanically testable
CCFG-29 removal gate. Stop before CCFG-26 selection or implementation.

## Batch Contract

- Covers: CCFG-34 only.
- Source dispatch: `dispatch.md`.
- Batch kind: `migration`.
- Slice risk class: `migration` for all four slices.
- Density: `full-runway` because runner lifecycle, public CLI behavior, state,
  receipts, sandbox boundaries, and temporary migration coexistence are high
  risk.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Execution context: ordinary single-root in
  `/home/alacasse/projects/codex-config`; no cross-checkout planning snapshot or
  pre-creation payload applies to CCFG-34.
- Completed-slice archive: `completed-slices.md`.
- Closeout artifact: `closeout.md`.
- Independent planning review: `review.md`.

## Current Baseline And Assumptions

- Planning Artifact Layout v1 is active under `docs/plans/`.
- Planning State `current` and `validate` pass with CCFG-34 as the sole `Ready`
  finding and no selected, queued, or active batch before this queue transition.
- Canonical stable repository `master` is at `580389fcf3f97900b234082808658090a62eecc3`
  before the planning artifacts and intentional issue #62 intake edits are
  committed. This is a planning baseline, not a future live lease.
- The issue #62 intake edits in program `CURRENT.md`, program `LEDGER.md`, its
  finding note, and the CCFG-26 `superseded.md` notice are intentional inputs.
  Preserve them; do not absorb unrelated dirty files into implementation commits.
- CCFG-26 remains blocked and its prior dispatch, review, and runway remain
  superseded, non-executable historical evidence.
- The default stable Codex home links runner and skill paths to this repository.
  CCFG-34 must not rebind the stable home or install candidate code.
- Focused baseline: 139 relevant tests and 66 subtests pass in 0.39 seconds;
  focused Ruff passes.
- Full repository pytest is `known-red-baseline`: 16 failures, 481 passes, and
  707 subtests pass. CCFG-34 does not own unrelated failures.
- Broad runner BasedPyright is `known-red-baseline`: 72 errors. CCFG-34 does not
  own broad typing cleanup.
- Operational runner JSON, receipts, and telemetry must use one explicit fresh,
  caller-owned batch run-artifact root under `/tmp`, created before the first
  flight and reused across every CCFG-34 flight with distinct unit paths.
  Generated acceptance output uses its own explicit fresh caller-owned root.
  Neither root may live under `docs/plans/` or become a reusable project default.

## Project Values

```yaml
planning_location: docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap
planning_artifact_layout: Planning Artifact Layout v1
program_root: docs/plans/programs/codex-config
selected_batch_directory: docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap
program_archive_root: docs/plans/programs/codex-config/archive
run_artifact_root: one caller-supplied fresh /tmp/ccfg-34-run.XXXXXX batch directory reused by every flight with distinct unit paths
output_root: caller-supplied fresh /tmp/ccfg-34-acceptance.XXXXXX directory for final deterministic proof
state_file_policy: generated-only
projection_policy: generated-only
update_authority: command
integration_harness: deterministic architecture-program runner pytest plus self-dogfood unit receipts
summary_artifact: fresh run telemetry and execution-unit receipts from the caller-supplied run directory
index_refresh: none
commit_requirements: one clean focused commit per slice; final planning closeout is separate
dirty_file_constraints: preserve the issue #62 intake and CCFG-26 supersession edits plus unrelated user changes
cross_checkout_context: not applicable
canonical_planning_root: not applicable for this ordinary single-root batch
```

Before the first execution flight, create and record explicit roots without
persisting them as project defaults:

```sh
ccfg34_run_artifact_root="$(mktemp -d /tmp/ccfg-34-run.XXXXXX)"
ccfg34_acceptance_root="$(mktemp -d /tmp/ccfg-34-acceptance.XXXXXX)"
```

The recorded `ccfg34_run_artifact_root` is immutable for this batch. Every
slice, recovery, finalization, and closeout process must receive that same root
explicitly and must write to a distinct execution-unit path beneath it.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2. Registered agent TOMLs
own worker, reviewer, specialist, investigator, and Spark result schemas.
Use Batch Runway Compact Report Contract v1 only for coordinator receipts and
its other non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for suspicious coordinator or
subagent-lifecycle behavior.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for slice-local worker, validation,
review, ledger, archive, and commit mechanics except for the flight override
below.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/execute-recovery-v1.md`
- `skills/batch-runway/references/finalize-batch-v1.md`

### CCFG-34 Flight Override

Issue #62 overrides the standard same-process continuation rule for this batch:

- One fresh coordinator process owns exactly one slice, one same-slice recovery
  attempt, finalization, or closeout unit.
- After each clean slice commit, receipt, execution-ledger update, and archive
  update, stop the coordinator instead of continuing to the next slice.
- A fresh process resumes from Planning State, this runway, the next incomplete
  execution-ledger row, exact worktree state, immediately relevant prior receipt,
  unresolved anomalies, validation profile, and any current strict lease.
- The new process must not reload completed chronology, raw transcripts, or
  accepted review detail.
- Slice 1 and Slice 2 use this override manually because the temporary launcher
  does not exist yet. After Slice 2 proves the launcher, Slice 3, Slice 4,
  finalization, and closeout must use it.
- A correction or recovery flight keeps the same slice ID and cannot advance
  another slice.
- This override does not change worker/reviewer separation: each implementation
  slice still uses a `runway_worker`, a separate `runway_reviewer`, and triggered
  specialist review before commit.

The override is temporary CCFG-34 behavior, not a general Batch Runway contract
change. CCFG-29 owns its removal after candidate parity.

## Temporary Execution-Unit Result

Prefer an internal `legacy-execution-unit/v1`-equivalent result validated by a
private stable-runner path. Do not widen the public phase-result schema or add a
serialized phase identity.

```yaml
interface: legacy-execution-unit/v1
status: completed | blocked | failed
unit: slice | finalization | closeout
slice_id: string | null
commit: string | null
next_action: continue_same_batch | resume_same_slice | finalize | closeout | require_user
```

The result may carry only the minimum facts the existing runner needs to choose
the next same-batch unit safely. Existing Planning State, runner state, phase
results, receipts, manifests, and telemetry remain authoritative. Missing,
contradictory, stale, or receipt-mismatched unit facts fail closed.

## Slice Shape

```yaml
slice_shape:
  count: 4
  adjacent_boundaries:
    1_to_2:
      condition: different owner seams and validation profiles
      valid_intermediate_state: future stable planning automatically consumes one canonical temporary policy before runner behavior changes
    2_to_3:
      condition: independent commit, rollback, and transition-risk boundary
      valid_intermediate_state: one pending slice completes in a fresh process and continues the same batch from durable state without finalization or closeout changes
    3_to_4:
      condition: separate recovery authority and support-role boundary
      valid_intermediate_state: normal slice, finalization, and closeout continuation works without advisor behavior
  merge_rule: merge Slices 2 and 3 only if the existing runner cannot expose a valid slice-only continuation state
  split_rule: re-slice if one fresh coordinator cannot implement, validate, review, commit, and archive the slice without compaction
```

There is no target slice count. Four is the output of the vertical owner,
transition, validation, and authority boundaries above.

## Migration Matrix

Use the complete migration matrix in `dispatch.md`. Every temporary surface
created by a slice must also record its exact caller, reason, current owner,
future owner, and CCFG-29 removal condition in code comments, project policy,
tests, or the execution ledger as appropriate. Silent fallback to the prior
owner is forbidden.

## Validation Status

| Command or evidence | Status class | Current or promotion rule |
|---|---|---|
| Focused runner, investigator, semantic-slice, and create-spec pytest | `required-green` | Current focused baseline is green. |
| Slice-created execution-unit, policy, or recovery tests | `implementation-created` | Each becomes `required-green` in the slice that creates it. |
| Focused Ruff for touched production and test files | `required-green` | Current focused baseline is green. |
| `git diff --check` | `required-green` | Current planning diff is green. |
| Full repository pytest | `known-red-baseline` | 16 failures, 481 passes, 707 subtests; diagnostic until a named slice owns all failures. |
| Broad runner BasedPyright | `known-red-baseline` | 72 errors; do not broaden CCFG-34 into runner typing cleanup. |
| BasedPyright for a new isolated temporary-result module | `conditional` | Run only if a new Python module is created; it must be green before that module can commit. |
| `./install.sh --status` and `./install.sh --dry-run` | `diagnostic-only` | Verify owned links and record existing manifest-version drift; do not mutate runtime state. |
| Planning State `current` and `validate` | `required-green` | Must remain one valid queued/active CCFG-34 batch through execution and idle after closeout. |

Do not promote a known-red command by narrative. Promotion requires a named
slice-owned remediation and green evidence.

## Execution Ledger

| Slice | Status | Commit | Validation | Review | Notes |
|---|---|---|---|---|---|
| 1. Install the temporary vertical planning policy | Pending | — | Pending | Pending | Manual fresh coordinator flight. |
| 2. Prove one representative fresh slice flight | Pending | — | Pending | Pending | Manual fresh coordinator flight; creates the temporary launcher path. |
| 3. Continue through finalization and closeout flights | Pending | — | Pending | Pending | Must use the Slice 2 launcher. |
| 4. Add one bounded read-only recovery assessment | Pending | — | Pending | Pending | Must use the Slice 2 launcher. |

Move completed row detail to `completed-slices.md` after every committed slice.
Keep only pending rows and compact convergence facts active here.

## Per-Flight Evidence

For each slice, recovery, finalization, and closeout flight, record:

```yaml
flight_evidence:
  unit: slice | finalization | closeout
  slice_id: string | null
  coordinator_process: string
  started_at: string | null
  elapsed_seconds: number | null
  token_usage:
    status: observed | missing
    value: number | null
  compaction_occurred: bool | null
  changed_files: number
  additions: number
  deletions: number
  validation_breadth: string
  support_roles: []
  review_roles: []
  blocker_transition: string | null
  smaller_alternative: string | null
  receipt_path: string
```

Use `missing`, not estimates, when token or compaction data is not attributable.

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

Record only suspicious coordinator or subagent-lifecycle behavior, not ordinary
validation or implementation chronology.

## Slice 1 — Install The Temporary Vertical Planning Policy

### Vertical Slice

```yaml
vertical_slice:
  starting_scenario: a stable plan-batch invocation plans CCFG-34 or later CCFG-26 through CCFG-29
  durable_result: repository-local instructions automatically require one project-owned policy containing vertical slice, migration coexistence, proportionality, telemetry, and CCFG-29 removal rules
  owner_before: issue #62 prose and runway-by-runway manual copying
  owner_after: a codex-config-owned temporary policy referenced by .codex/AGENTS.md
  migrated_callers:
    - CCFG-34 self-dogfooding planning
    - later stable planning for CCFG-26 through CCFG-29
  focused_validation:
    - policy contract test
    - semantic slice and create-spec contract tests
    - focused Ruff
    - git diff --check
  independently_usable_state: future stable planning consumes one canonical policy without runner changes
  rollback_boundary: revert the policy, repository-local instruction hook, tests, changelog, and feature metadata as one commit
  temporary_residue:
    - .codex/AGENTS.md policy hook removed by CCFG-29 after issue #60 parity
    - project policy document removed by CCFG-29 after issue #60 parity
    - policy regression test removed only after equivalent candidate scenarios pass
```

### Scope And Allowed Files

- Add a temporary policy under
  `docs/plans/programs/codex-config/notes/` with the issue #62 vertical fields,
  migration matrix, proportionality warnings, evidence requirements, fresh
  flight rules, and CCFG-29 removal gate.
- Reference it from `.codex/AGENTS.md`, the repository-local project overlay.
  Do not add codex-config-specific policy to global `AGENTS.md` or reusable
  skills.
- Add one focused policy contract test.
- Update `CHANGELOG.md` and only metadata actually required by the changed
  repository-owned feature.

Allowed areas:

- `.codex/AGENTS.md`
- `docs/plans/programs/codex-config/notes/`
- `tests/test_stable_runway_dogfooding_policy.py`
- `CHANGELOG.md`
- `codex-features.json` only if the installed feature contract actually changes

### Non-Goals

- No runner code, candidate code, generic skill, global instruction, or runtime
  state change.
- No policy text copied independently into future runways.

### Acceptance Criteria

- A stable planning agent entering this repository is mechanically instructed to
  load the one temporary project policy for CCFG-26 through CCFG-29.
- The policy contains every issue #62 vertical field, coexistence field,
  advisory warning, evidence field, self-dogfood rule, authority limit, and
  CCFG-29 removal prerequisite.
- Contract tests prove the hook and reject a missing policy, missing required
  field, arbitrary fixed slice count, permanent candidate wording, or missing
  removal condition.
- No generic skill or global instruction gains a codex-config-specific branch.

### Validation

- `implementation-created` then `required-green`:
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_stable_runway_dogfooding_policy.py`
- `required-green`:
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_semantic_slice_shape_contract.py tests/test_batch_runway_create_spec_contract.py`
- `required-green`: `.venv/bin/ruff check --no-cache tests/test_stable_runway_dogfooding_policy.py`
- `required-green`: `git diff --check`
- Trigger `test-quality-review` in delta-only mode because tests change.

### Commit

`feat: add temporary stable runway planning policy`

### Worker Brief

You are the registered `runway_worker` and already the required coding subagent
for Slice 1. Implement only the project-local policy, its `.codex/AGENTS.md`
hook, focused contract test, changelog, and strictly necessary metadata. Do not
spawn, delegate to, or wait on another agent. Do not edit global instructions,
generic skills, runner code, runtime Codex state, or candidate code. Leave
validation, review, ledger/archive updates, and commit to the coordinator.

### Reviewer Brief

Independently review the exact task-scoped diff basis supplied by the
coordinator and echo `diff_basis`. Verify automatic project-local loading,
complete vertical/migration/proportionality/removal policy, no generic or global
contamination, and focused behavioral tests. Do not edit or spawn agents.

### Slice Stop Conditions

- Stop if automatic loading requires changing a generic skill or global
  `AGENTS.md`.
- Stop if policy requirements are duplicated into individual runways instead of
  referenced from one project-owned document.
- Stop after commit, receipt, execution-ledger update, and archive update.
  Resume Slice 2 in a fresh coordinator process.

## Slice 2 — Prove One Representative Fresh Slice Flight

### Vertical Slice

```yaml
vertical_slice:
  starting_scenario: an active runway has one pending slice and durable canonical state
  durable_result: the stable runner launches one fresh coordinator that completes exactly that slice through worker, validation, review, commit, archive, receipt, and a same-batch next action
  owner_before: one long-lived execute-phase coordinator
  owner_after: temporary execution-unit orchestration behind the existing runner facade and PhaseWorker seam
  migrated_callers:
    - later CCFG-34 slice flights
    - stable CCFG-26 through CCFG-29 slice execution
  focused_validation:
    - fresh Codex process launch
    - multi-slice continuation
    - same-slice resume result
    - contradictory state or receipt rejection
    - existing telemetry capture
  independently_usable_state: one committed slice advances the same batch from durable state without shared model context
  rollback_boundary: revert temporary unit launch and continuation without changing the four serialized phase identities
  temporary_residue:
    - private legacy-execution-unit/v1-equivalent validator removed by CCFG-29 after issue #61 parity
    - temporary unit state and receipt fields removed by CCFG-29 after issue #61 parity
    - unit telemetry fields and regression scenarios removed after candidate parity
```

### Scope And Allowed Files

- Reuse `CodexExecWorker`, `PhaseWorker`, and `execute_phase_with_worker` for the
  fresh process.
- Keep `run` as the sole coordinator/persistence loop.
- Add only the minimum current-unit, prior-unit-receipt, and continuation facts
  to existing atomic state.
- Validate the temporary unit result separately; preserve the public phase-result
  schema and phase identities.
- Add optional unit facts to existing phase telemetry and session attribution.
- Add focused deterministic execution-unit tests. Prefer one new test module if
  it keeps this owner-level behavior coherent.

Allowed areas:

- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_workers.py`
- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner_state.py`
- `scripts/architecture_program_runner_transition.py`
- `scripts/architecture_program_runner_validation.py`
- `scripts/architecture_program_runner_artifacts.py`
- `scripts/architecture_program_runner_phase_observation.py`
- `tests/test_architecture_program_runner_execution_units.py`
- `tests/test_architecture_program_runner_transition.py`
- directly related existing `tests/test_architecture_program_runner*.py`
- `CHANGELOG.md`
- `codex-features.json` only for the owning feature version/link contract

### Non-Goals

- No second CLI, runner, state store, phase enum, transition engine, telemetry
  tree, public phase protocol, or successor selection.
- No finalization, closeout, or advisor behavior; those belong to later slices.

### Acceptance Criteria

- Every representative slice flight launches a distinct `codex exec` process
  through the existing worker/observation path.
- The flight completes exactly one slice cycle, persists the unit result and
  receipt, and chooses only `continue_same_batch`, `resume_same_slice`, or
  `finalize` from validated durable state.
- Multi-slice continuation starts a new process and cannot skip or duplicate a
  ledger row.
- Execute-to-execute continuation remains owned by the existing transition
  engine and is covered by its focused transition tests.
- Missing, contradictory, stale, or receipt-mismatched state stops before the
  next launch.
- Existing phase identities, phase results, receipt equality, manifests,
  worktree allowance, and telemetry remain authoritative.
- Unit telemetry records duration, session/token evidence when available,
  changed-file/line counts, validation breadth, review roles, blocker transition,
  and compaction status without a second telemetry subsystem.

### Proportionality And Smaller Alternative

This slice is expected to reach the three-production-surface warning. A
single-file launcher is smaller in file count but invalid because it would
duplicate or bypass worker, state, receipt, validation, and telemetry ownership.
Keep the vertical path across those owners; do not pull finalization, closeout,
or advisor behavior into this diff.

### Validation

- `implementation-created` then `required-green`:
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_architecture_program_runner_execution_units.py`
- `required-green`:
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_architecture_program_runner.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_phase_observation.py tests/test_architecture_program_runner_change_allowance.py`
- `required-green`: `.venv/bin/ruff check --no-cache <touched Python files>`
- `conditional`: `.venv/bin/basedpyright <new isolated Python modules>` only
  when this slice creates such a module; it must be green before commit.
- `known-red-baseline`: broad runner BasedPyright, 72 errors.
- `required-green`: `git diff --check`
- Trigger `test-quality-review` in delta-only mode.
- Trigger `import_topology_reviewer` if a new module or project-local import
  topology is introduced.

### Commit

`feat: launch stable runway slices in fresh coordinators`

### Worker Brief

You are the registered `runway_worker` and already the required coding subagent
for Slice 2. Implement only the representative slice flight behind existing
runner owners. Do not spawn, delegate to, or wait on another agent. Preserve
public phase identities and schemas. Do not add finalization, closeout, advisor,
candidate, installer, or successor behavior. Leave validation, reviews,
ledger/archive updates, and commit to the coordinator.

### Reviewer Brief

Independently review the exact diff basis and echo it. Verify one fresh process,
one slice only, durable same-batch continuation, strict state/receipt rejection,
telemetry reuse, no public protocol widening, and no second runner framework.
Do not edit or spawn agents.

### Slice Stop Conditions

- Stop if the valid intermediate state cannot execute and persist one slice
  without finalization/closeout behavior; re-slice only through a reviewed
  amendment.
- Stop if next-unit selection depends on Git, path discovery, timestamps,
  transcripts, or accepted-review chronology.
- Stop if the change approaches 12 files, 1,000 lines, two migration kinds,
  three specialist lenses, or coordinator compaction without a smaller-
  alternative analysis and re-slicing decision.
- Stop after commit, receipt, execution-ledger update, and archive update.
  Resume Slice 3 with the new launcher in a fresh coordinator process.

## Slice 3 — Continue Through Fresh Finalization And Closeout Flights

### Vertical Slice

```yaml
vertical_slice:
  starting_scenario: the last implementation slice is committed and durable state requests finalization
  durable_result: distinct fresh finalization and closeout coordinators validate the full range, finalize evidence, reconcile only CCFG-34, clear active state, and stop without a successor
  owner_before: final validation and closeout share live execution context or reload broad chronology
  owner_after: temporary unit continuation preserves execute and closeout phase identities while giving each boundary a fresh process
  migrated_callers:
    - CCFG-34 finalization and closeout
    - stable CCFG-26 through CCFG-29 finalization and closeout
  focused_validation:
    - final slice to finalization transition
    - finalization to closeout transition
    - contradictory finalization or closeout state rejection
    - same-batch reconciliation and no successor selection
  independently_usable_state: successful batches finalize and reconcile from durable state with no shared live context
  rollback_boundary: revert finalization and closeout unit support while retaining Slice 2 slice-only continuation
  temporary_residue:
    - finalization and closeout unit state removed by CCFG-29 after issue #61 parity
    - no-successor guard retained until equivalent candidate closeout proof
    - transition regression scenarios removed only after candidate parity
```

### Scope And Allowed Files

- Extend the Slice 2 unit seam to finalization and closeout without creating new
  public phases.
- Reuse existing runner transition, validation, receipt, artifact, and telemetry
  owners.
- Require finalization to consume the final exact slice range and current
  execution ledger without broad chronology.
- Require closeout to reconcile CCFG-34 only and return terminal same-batch state.

Allowed areas:

- Slice 2 runner owner files only where required
- `scripts/architecture_program_runner_transition.py`
- `tests/test_architecture_program_runner_execution_units.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `tests/test_architecture_program_runner_transition.py`
- `tests/test_architecture_program_runner_validation.py`
- `CHANGELOG.md`
- `codex-features.json` only for the owning feature version/link contract

### Non-Goals

- No CCFG-26 planning, selection, dispatch, runway, candidate work, or COR-009
  acceptance.
- No physical cleanup, phase migration, or public lifecycle change.

### Acceptance Criteria

- The last completed slice advances to a fresh finalization process, not directly
  to shared-context closeout.
- Finalization runs the full selected validation and review range, writes its
  receipt/telemetry, and advances only to closeout.
- Closeout runs in another fresh process, reconciles only CCFG-34, clears
  selected/queued/active state, and selects or prepares no successor.
- Missing, contradictory, stale, or mismatched finalization/closeout state fails
  closed.
- Repeated resume does not duplicate finalization, closeout, receipts, or
  reconciliation.

### Proportionality And Smaller Alternative

This slice may reach the three-production-surface warning. Keeping it separate
from Slice 2 preserves a valid slice-only rollback point and isolates the
distinct no-successor and program-reconciliation risk. A separate closeout
framework is forbidden.

### Validation

- `required-green`:
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_architecture_program_runner_execution_units.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py`
- `required-green`: `.venv/bin/ruff check --no-cache <touched Python files>`
- `conditional`: `.venv/bin/basedpyright <new isolated Python modules>` only
  when new modules exist; they must be green.
- `known-red-baseline`: broad runner BasedPyright, 72 errors.
- `required-green`: `git diff --check`
- Trigger `test-quality-review` in delta-only mode.
- Trigger `import_topology_reviewer` only if import topology changes.

### Commit

`feat: continue stable finalization and closeout in fresh flights`

### Worker Brief

You are the registered `runway_worker` and already the required coding subagent
for Slice 3. Extend only the Slice 2 continuation seam through fresh
finalization and same-batch closeout. Do not spawn, delegate to, or wait on
another agent. Do not add recovery advice, public phases, successor selection,
candidate work, or cleanup. Leave validation, reviews, ledger/archive updates,
and commit to the coordinator.

### Reviewer Brief

Independently review the exact diff basis and echo it. Verify distinct fresh
finalization/closeout processes, receipt/state idempotence, exact-range
validation, CCFG-34-only reconciliation, and no successor action. Do not edit or
spawn agents.

### Slice Stop Conditions

- Stop if closeout can return `select-dispatch`, queue, prepare, or otherwise
  make CCFG-26 current.
- Stop if finalization or closeout needs completed chronology, transcripts, or
  accepted review detail rather than compact current evidence.
- Stop after commit, receipt, execution-ledger update, and archive update.
  Resume Slice 4 with the launcher in a fresh coordinator process.

## Slice 4 — Add One Bounded Read-Only Recovery Assessment

### Vertical Slice

```yaml
vertical_slice:
  starting_scenario: a slice flight reaches an eligible blocker before user escalation
  durable_result: exactly one fresh codebase_investigator assessment receives a compact evidence packet, reports issue #62 recovery distinctions, and remains advisory while the coordinator enforces existing authority
  owner_before: immediate escalation or ad hoc diagnosis
  owner_after: existing codebase_investigator owns read-only evidence while the stable coordinator retains every recovery and escalation decision
  migrated_callers:
    - same-slice recovery for CCFG-34
    - stable CCFG-26 through CCFG-29 blocker handling
  focused_validation:
    - recover, retry_environment, and require_user classifications
    - at-most-one assessment for one material blocker
    - same-slice resume in a fresh process
    - authority-expansion, safety-weakening, and missing-evidence rejection
  independently_usable_state: eligible invocation, environment, cache, diff-basis, and already-authorized in-slice recoveries receive one assessment before escalation
  rollback_boundary: remove the advisor adapter and classifier without affecting normal slice, finalization, or closeout continuation
  temporary_residue:
    - recovery packet and assessment receipt removed by CCFG-29 after issue #59 parity
    - temporary authority classifier removed after candidate bounded-authority proof
    - recovery regression scenarios retained until equivalent candidate scenarios pass
```

### Scope And Allowed Files

- Reuse `agents/codebase_investigator.toml` unchanged unless a reviewed amendment
  proves its current result contract cannot express the bounded notes safely.
- Build one compact evidence packet with the active runway/slice, exact stop
  condition, failing command/tool scope, validation status, baseline/candidate
  results, exact diff basis, repository/worktree state, and smallest proposed
  recovery.
- Require the assessment to report root cause, smallest tested recovery, current
  scope, semantic change, authority expansion, safety weakening, missing
  evidence, and `recover`, `retry_environment`, or `require_user`.
- Keep all proceed/stop and recovery decisions in the stable coordinator.

Allowed areas:

- Slice 2 runner owner files only where required
- `tests/test_architecture_program_runner_recovery.py`
- `tests/test_codebase_investigator_contract.py`
- `tests/test_custom_agent_contracts.py`
- `CHANGELOG.md`
- `codex-features.json` only for the owning feature version/link contract

`agents/codebase_investigator.toml` is not an allowed edit without a reviewed
amendment. Its existing role is the intended smaller alternative.

### Non-Goals

- No new advisor agent, recursive debate, automatic amendment, approval,
  delegation, selection, write scope, destructive work, validation
  reclassification, semantic expansion, or safety weakening.

### Acceptance Criteria

- An eligible blocker receives zero assessments if no assessment is needed, or
  exactly one fresh read-only assessment before user escalation.
- The advisor cannot edit, approve, commit, delegate, select, amend the runway,
  widen authority, or approve its own recommendation.
- Only invocation correction, exact retry, local environment/cache repair,
  refreshed diff/review basis, or an already-authorized in-slice code/test repair
  may proceed without the user, and only when existing recovery authority allows.
- Write-scope expansion, validation reclassification, semantic expansion,
  safety weakening, new protocols/lifecycle surfaces, destructive work,
  multiple material choices, or insufficient evidence return `require_user`.
- Recovery resumes the same slice in a fresh process and cannot advance another
  slice or choose successor work.

### Proportionality And Smaller Alternative

The recovery authority, support-role, safety, and state/receipt lenses reach the
review-lens warning. Reusing `codebase_investigator` unchanged is the accepted
smaller alternative. Do not add a specialized permanent advisor or debate loop.

### Validation

- `implementation-created` then `required-green`:
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_architecture_program_runner_recovery.py`
- `required-green`:
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codebase_investigator_contract.py tests/test_custom_agent_contracts.py tests/test_architecture_program_runner_execution_units.py`
- `required-green`: `.venv/bin/ruff check --no-cache <touched Python files>`
- `conditional`: `.venv/bin/basedpyright <new isolated Python modules>` only
  when new modules exist; they must be green.
- `known-red-baseline`: broad runner BasedPyright, 72 errors.
- `required-green`: `git diff --check`
- Trigger `test-quality-review` in delta-only mode.
- Trigger `import_topology_reviewer` only if import topology changes.

### Commit

`feat: add bounded read-only runway recovery assessment`

### Worker Brief

You are the registered `runway_worker` and already the required coding subagent
for Slice 4. Add only the one-assessment evidence packet, advisory invocation,
authority classification, state/receipt proof, and focused tests. Do not spawn,
delegate to, or wait on another agent. Do not edit the agent role without an
approved amendment. Leave validation, reviews, ledger/archive updates, and
commit to the coordinator.

### Reviewer Brief

Independently review the exact diff basis and echo it. Verify at-most-one fresh
read-only assessment, complete evidence/classification fields, same-slice
resume, preserved coordinator authority, and fail-closed user gates. Do not edit
or spawn agents.

### Slice Stop Conditions

- Stop if the existing investigator role cannot express the required bounded
  assessment without a role change; request a reviewed amendment instead.
- Stop if the advisor can edit, approve, commit, delegate, select, amend, widen
  work, or approve its own result.
- Stop for user direction on semantic or write-scope expansion, validation
  reclassification, destructive work, safety weakening, multiple material
  choices, or missing evidence.
- Stop after commit, receipt, execution-ledger update, and archive update.
  Begin finalization in a fresh coordinator process.

## Final Validation And Finalization Flight

Run finalization in a fresh process through the Slice 2/3 launcher. The
coordinator owns validation and reads the fresh run telemetry and unit receipts
before reporting.

Required-green focused validation:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_stable_runway_dogfooding_policy.py \
  tests/test_architecture_program_runner_execution_units.py \
  tests/test_architecture_program_runner_recovery.py \
  tests/test_architecture_program_runner.py \
  tests/test_architecture_program_runner_run_loop.py \
  tests/test_architecture_program_runner_state.py \
  tests/test_architecture_program_runner_validation.py \
  tests/test_architecture_program_runner_artifacts.py \
  tests/test_architecture_program_runner_phase_observation.py \
  tests/test_architecture_program_runner_transition.py \
  tests/test_architecture_program_runner_change_allowance.py \
  tests/test_codebase_investigator_contract.py \
  tests/test_custom_agent_contracts.py \
  tests/test_semantic_slice_shape_contract.py \
  tests/test_batch_runway_create_spec_contract.py
.venv/bin/ruff check --no-cache scripts tests
git diff --check
python scripts/planning_state.py current --root docs/plans
python scripts/planning_state.py validate --root docs/plans
```

Known-red diagnostic baselines:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider
.venv/bin/basedpyright \
  scripts/architecture_program_runner.py \
  scripts/architecture_program_runner_artifacts.py \
  scripts/architecture_program_runner_change_allowance.py \
  scripts/architecture_program_runner_command.py \
  scripts/architecture_program_runner_environment.py \
  scripts/architecture_program_runner_input_inventory.py \
  scripts/architecture_program_runner_phase_contract.py \
  scripts/architecture_program_runner_phase_observation.py \
  scripts/architecture_program_runner_state.py \
  scripts/architecture_program_runner_transition.py \
  scripts/architecture_program_runner_validation.py \
  scripts/architecture_program_runner_workers.py
```

Do not report these diagnostic commands as green gates unless a reviewed
amendment names and closes every baseline failure/error.

Diagnostic installed-state evidence:

```sh
./install.sh --status
./install.sh --dry-run
```

Require deterministic proof of:

- multi-slice continuation with one fresh coordinator per slice;
- blocker-to-same-slice resume after at most one read-only assessment;
- last-slice to fresh finalization to fresh closeout;
- contradictory or stale state/receipt rejection;
- no successor selection;
- all three recovery recommendation classes and authority gates;
- per-unit telemetry sufficient to assess proportionality and context pressure;
- the CCFG-29 removal inventory and candidate parity prerequisites.

Final exact-range review must use a supplied commit range. Run the final
`runway_reviewer`, delta-only `test-quality-review`, and conditional
`import_topology_reviewer` if project-local topology changed. Do not create an
unregistered security reviewer; the final reviewer owns authority/safety review.

## Fresh Closeout Flight

After finalization is green, start a separate fresh closeout coordinator. It may:

- create `closeout.md` from complete implementation, validation, review,
  receipt, telemetry, and finalization evidence;
- mark CCFG-34 `Closed`;
- return CCFG-26 from dependency-blocked to `Open` while leaving it unselected,
  undispatched, unqueued, and without a runway;
- clear CCFG-34 selected, queued, and active state;
- update program `CURRENT.md` and `LEDGER.md` only to close CCFG-34 and record
  the resulting CCFG-26 dependency transition from `Blocked` to `Open`, while
  leaving CCFG-26 unselected, undispatched, unqueued, and without a runway; and
- preserve the superseded CCFG-26 dispatch, review, runway, and notice as
  non-executable history.

It must stop without selecting, dispatching, queueing, refreshing, or preparing
CCFG-26. A later explicit `plan-batch` invocation owns its fresh replan and must
consume permanent candidate requirements #59, #60, and #61.

## CCFG-29 Removal Gate

Remove CCFG-34 mechanisms only during or after CCFG-29 when all of these are
true:

1. candidate integration is authoritative;
2. permanent #59, #60, and #61 behavior is active and validated;
3. equivalent CCFG-34 policy, fresh-flight, recovery, contradiction, telemetry,
   and no-successor scenarios pass through the candidate;
4. removal restores neither a legacy route nor unreadable planning evidence;
5. every temporary surface below has been reconciled:
   - `.codex/AGENTS.md` policy hook and project policy document;
   - private execution-unit result validator and state/receipt fields;
   - temporary recovery packet and authority classifier;
   - temporary telemetry fields and regression tests;
   - feature version/link metadata changed by the bootstrap.

CCFG-29 must stop if any parity, proof, ownership, or evidence prerequisite is
incomplete.

## Batch Stop Conditions

- Stop on scope drift, unrelated dirty-file overlap, missing required custom
  agents, or a fresh-coordinator boundary that cannot be enforced.
- Stop if one flight approaches a proportionality warning without recorded
  smaller-alternative analysis; re-slice on compaction.
- Stop if implementation creates or exposes a permanent public unit protocol,
  second runner/store/transition engine, or new serialized phase identity.
- Stop if public phase-result compatibility, receipt equality, state atomicity,
  worktree allowance, telemetry attribution, or no-successor behavior weakens.
- Stop if CCFG-26, candidate code, stable-home bindings, default generation,
  bridge state, or generic reusable skills would change.
- Stop if the advisor gains authority or if a recovery outside the active
  runway/recovery contract would proceed without the user.
- Stop if a temporary surface lacks exact ownership and a CCFG-29 removal gate.
