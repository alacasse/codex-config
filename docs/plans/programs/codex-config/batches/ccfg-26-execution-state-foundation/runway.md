# CCFG-26 Execution-State Foundation Runway

## Purpose

Implement the first bounded CCFG-26 execution foundation in the candidate
generation. The batch creates one deep canonical Batch Execution State owner,
then integrates one fresh public `work-batch` Execution Flight through the real
candidate runner `execute` caller. It ends at the deliberately manual one-flight
acceptance milestone and leaves automatic continuation, recovery,
finalization, closeout, and successor selection outside this runway.

## Source Contract

- Selected dispatch: `dispatch.md`
- Program ledger: `../../LEDGER.md`, CCFG-26 only
- Accepted architecture decision:
  `../../../../../adr/0003-canonical-batch-execution-state.md`
- Accepted detailed design:
  `../../notes/ccfg-26-execution-state-design-contract.md`
- Clean design review:
  `../../notes/ccfg-26-execution-state-design-review.md`
- Replan provenance:
  `../../notes/ccfg-26-replan-analysis-and-chatgpt-pro-handoff.md`
- Direction amendment:
  `../../findings/ccfg-26-execution-state-authority-direction.md`
- Temporary execution policy:
  `../../notes/stable-runway-dogfooding-policy.md`
- Slice-shape policy: `../../notes/slice-shape-policy.yaml`
- Superseded CCFG-26B evidence only: `../ccfg-26b-fresh-slice-flight/`

This runway covers only the first CCFG-26 execution-foundation batch. CCFG-26
must remain open after closeout. CCFG-26C through CCFG-26E and CCFG-27 through
CCFG-29 remain unselected.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`
- Density: `full-runway`
- Slice 1 risk: `migration`
- Slice 2 risk: `migration`
- Approval gate: CCFG-26/COR-009, ADR 0003, the accepted design contract, the
  clean design review, the temporary stable-runway policy, and this explicit
  `plan-batch` request authorize the two exact ownership migrations below.
- No contract narrowing, destructive cleanup, recovery authority, finalization,
  closeout, successor selection, stable implementation edit, or generation
  switch is approved.

## Current Baseline And Assumptions

- Canonical stable planning/toolchain checkout:
  `/home/alacasse/projects/codex-config`
- Stable branch/revision:
  `master` / `93fa9109e35719d4f36dd75edc97bf0df584c1da`
- Candidate implementation checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Candidate branch/revision: `implementation/command-owner-redesign` /
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`
- Stable and candidate worktrees were clean at planning pickup.
- Stable and candidate installed `work-batch` links resolve to their matching
  source roots.
- The installed strict helper resolves to the stable toolchain helper.
- Candidate installation status and dry-run were converged at the candidate
  baseline.
- Planning State `current` and `validate` passed before selection with no
  selected dispatch, queued batch, active runway, blocker, or obligation.
- A narrow candidate runner/workflow baseline passed 64 tests and 22 subtests.
- The complete affected runner/manifest baseline passed 124 tests and 443
  subtests with exactly two known failures owned by Slice 2:
  `test_skill_points_local_runner_usage_to_protocol` and
  `test_work_batch_reconciles_same_batch_closeout`.
- Command-owner scenario catalog validation passed for 82 scenarios.
- Touched-path Ruff baseline passed.
- The exact affected runner BasedPyright subset is a known-red baseline of
  56 errors, zero warnings, and zero notes. New execution-state code must be
  clean; the existing subset must not gain a diagnostic.
- Stable installed feature inventory reports version metadata drift while all
  managed links, including the strict helper, resolve to the stable checkout.
  This planning batch does not install or mutate the stable home.

## Explicit Runtime Input

- Run-artifact root: `/tmp/tmp.nAyp7HeqwO`
- Root source: exact generated-only input allocated once through the host
  temporary-directory facility during planning.
- Program slug: `codex-config`
- Batch ID: `ccfg-26-execution-state-foundation`
- Canonical state path:
  `/tmp/tmp.nAyp7HeqwO/batch-executions/codex-config/ccfg-26-execution-state-foundation/execution-state.json`

The root is not project policy and does not become a reusable default. The
executor passes the exact value to every target Execution Flight. The canonical
state path must be absent before Slice 2 initializes the real tracer. Slice 1
tests and executable acceptance use distinct fresh caller-supplied fixture
roots and must not create the batch's canonical path. Reusable code and fixtures
must accept an explicit path and allocate their own host-platform temporary
roots; they must not embed `/tmp` or copy this planning value as a default.

## Whole-Batch Non-Goals

- No automatic same-batch continuation.
- No ambiguous-attempt recovery, cancellation, or automatic relaunch.
- No final validation/finalization state transition.
- No target closeout, ledger reconciliation, Planning State completion, or
  no-successor transition.
- No CCFG-26C/D/E selection or revival of the superseded CCFG-26B sequence.
- No serialized phase identity change; CCFG-27 retains that decision.
- No physical legacy-owner deletion or default switch; CCFG-28 retains it.
- No candidate/stable integration or bridge removal; CCFG-29 retains it.
- No stable runner source edit, stable install, candidate control of canonical
  planning, or stable loading of candidate code.
- No planner compaction, FSM library, shared/network filesystem, multi-host
  lease, fencing, or power-loss durability guarantee.

## Planning Snapshot

Interface: `cross-checkout-context/v1`.

Installed helper:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Resolved helper:

```text
/home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
```

Canonical planning root:

```text
/home/alacasse/projects/codex-config/docs/plans
```

Complete validated plan-time payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 93fa9109e35719d4f36dd75edc97bf0df584c1da
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 93fa9109e35719d4f36dd75edc97bf0df584c1da
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 5c5ec9d52dd9033daa45f3a200031c152363b62c
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Plan-time validation receipt:

```yaml
interface: cross-checkout-receipt/v1
caller: plan-batch
reason: CCFG-26 execution-state foundation selection and queue transition
allowed_scope:
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_root: /home/alacasse/projects/codex-config/docs/plans
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  planning_paths:
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/CURRENT.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/LEDGER.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/dispatch.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/runway.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/review.md
  implementation_paths:
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/batch_execution_state.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/batch_execution_state_model.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/batch_execution_state_store.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_artifacts.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_command.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_environment.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_execution.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_phase_contract.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_state.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_transition.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_validation.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_workers.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/work-batch/references/batch-execution-state-v1.schema.json
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/work-batch/references/execution-flight-result-v1.schema.json
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/work-batch
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/architecture-program-runway/references/local-runner-v1.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_batch_execution_state.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_batch_execution_state_store.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_batch_execution_state_process.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_work_batch_flight_contract.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_artifacts.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_phase_contract.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_command.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_environment.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_protocol.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_validation.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_transition.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_run_loop.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_state.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_behavioral_scenarios.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_scenario_catalog.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_codex_features_manifest.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/codex-features.json
    - /home/alacasse/projects/codex-config-command-owner-redesign/pyproject.toml
    - /home/alacasse/projects/codex-config-command-owner-redesign/uv.lock
    - /home/alacasse/projects/codex-config-command-owner-redesign/.github/workflows/batch-execution-state.yml
    - /home/alacasse/projects/codex-config-command-owner-redesign/docs/skill-routing-contract.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/docs/workflow-guide.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/README.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/CHANGELOG.md
generation_identity:
  generation_role: stable
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 93fa9109e35719d4f36dd75edc97bf0df584c1da
  codex_home: /home/alacasse/.codex
  canonical_state_mutation_allowed: true
repository_revisions:
  toolchain_commit: 93fa9109e35719d4f36dd75edc97bf0df584c1da
  canonical_planning_commit_before: 93fa9109e35719d4f36dd75edc97bf0df584c1da
  implementation_commit_before: 5c5ec9d52dd9033daa45f3a200031c152363b62c
deletion_condition: CCFG-29 final integration
```

The snapshot is immutable historical plan-time evidence, not a live execution
lease. Do not rewrite it to chase `HEAD` or embed the containing planning
commit. Before each worker/reviewer handoff, `work-batch` must confirm the same
selected scope through Planning State, acquire a fresh ready live lease, and
validate the exact write-bearing paths separately.

## Project Values

- Planning Artifact Layout: Planning Artifact Layout v1.
- Planning location: this batch directory.
- Program root: `docs/plans/programs/codex-config`.
- Program archive root: `docs/plans/archive/`.
- Project-policy run artifact root: `None`.
- Explicit batch execution input: `/tmp/tmp.nAyp7HeqwO`.
- Output root: generated-only subpaths beneath the explicit batch root.
- Slice 1 fixture roots: separate fresh caller-supplied temporary roots; the
  exact batch root and canonical state path are reserved for Slice 2 and final
  batch evidence.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Integration harness: candidate `scripts/command_owner_scenarios.py accept`
  over the exact candidate commit with explicit generated outputs.
- Summary artifacts: exact acceptance result JSON, JSON report, and text report.
- Index refresh: none.
- Candidate commits: one focused commit per Slice after local validation,
  delta-only test-quality review, and independent runway review.
- Cross-platform matrix: final exact candidate commit on Ubuntu, macOS, and
  Windows; external green evidence is required before batch closeout.
- Stable planning receipts and same-batch reconciliation are separate stable
  commits. Self-referential closeout fields use `this closeout commit`.
- Preserve unrelated dirt and stop on overlap.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2; registered agent TOMLs
own worker and reviewer result schemas.
Use Batch Runway Compact Report Contract v1 for coordinator receipts.
Use Batch Runway Compact Convergence Assessment v1 for routine status and
receipt summaries.
Use Batch Runway Orchestration Anomaly Log v1 only for suspicious coordination
behavior.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine implementation.
Use strict `cross-checkout-context/v1` for every delegated handoff.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`

Overrides:

- The temporary stable-runway dogfooding policy limits one `work-batch`
  invocation to exactly the next incomplete implementation Slice, including
  implementation, focused validation, review, commit, receipt, and archive.
- The stable controller may orchestrate through existing mechanisms but may not
  load candidate code as runtime authority.
- Final cross-platform evidence may require an external authorized action after
  candidate commits exist. If unavailable, stop with the same batch active; do
  not mark it complete or select another batch.

## Execution Ledger

| Slice | Status | Commit | Review | Durable result |
|---|---|---|---|---|
| 1. Canonical execution-state owner | Blocked | — | Findings | Uncommitted candidate implementation; final-effect path confinement requires a reviewed cross-platform mechanism amendment; see `execution-report.md` and `execution-retrospective.md` |
| 2. One-flight public `work-batch` tracer | Pending | — | Pending | Real candidate runner advances one Slice, derives `continue_same_batch`, stops compatibly, and supports exact fresh resume |

## Slice Shape

Two slices are required by semantic ownership and rollback boundaries.

- `1 -> 2`: Slice 1 produces the accepted public state interface and durable
  generated-only artifacts. Slice 2 consumes that exact interface through the
  real runner/public command seam. The intermediate state is executable and
  testable, and Slice 2 can roll back without discarding the state module.
- The smaller Slice 1 alternative—separate reducer, schema, lock, persistence,
  receipt, and projection commits—was rejected because it exposes internal
  coordination and creates horizontal scaffolding without the accepted public
  behavior.
- The smaller Slice 2 alternative—separate skill, runner launch, result-schema,
  or stopped-result commits—was rejected because any intermediate state would
  leave duplicate semantic ownership or a silent public fallback.
- Automatic continuation is not a third Slice in this batch. Its outer loop,
  one-final-Phase-Result rule, crash-between-flights contract, validation, and
  rollback are independently reviewable and materially broader than proving
  one fresh resumable flight.

## Migration Matrix

| Scenario or caller | Owner before | Owner after this batch | Status before | Removal condition |
|---|---|---|---|---|
| Generated-only execution-state acceptance | no canonical Batch Execution State owner | candidate execution-state deep module | pending | Slice 1 acceptance and commit |
| Candidate runner first-tracer `execute` caller | Batch Runway public execution route | runner process lifecycle plus public `work-batch`; execution-state module owns progression | pending | Slice 2 acceptance and commit |
| Public candidate `work-batch` first-tracer decisions | Batch Runway support route | `work-batch` | pending | Slice 2 acceptance and commit |
| Automatic successful continuation | no accepted outer loop | later CCFG-26 milestone | pending | Required before CCFG-26 normal use/closeout; later explicit `plan-batch` |
| Ambiguous recovery | fail-closed stop only | later reviewed recovery owner | pending | Later explicit CCFG-26 planning |
| Finalization and target closeout | stable bridge owners | later candidate `work-batch` milestones | pending | Later explicit CCFG-26 planning |
| Unmigrated Batch Runway support callers | Batch Runway | later `work-batch` migration | pending | Each retained caller must name reason, future owner, and removal condition; CCFG-26 cannot close while forbidden dependency remains |

## Validation Contract

All commands run in the candidate checkout unless explicitly marked stable.
Use `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` for pytest. Slice 1
test and acceptance artifacts use distinct fresh caller-supplied roots. Slice 2
and final exact acceptance use generated-only subpaths beneath the explicit
batch root. Reusable commands do not embed a platform temporary directory.

Baseline gates:

- Focused runner/workflow pytest subset: `required-green`; the narrow planning
  baseline passed 64 tests and 22 subtests.
- Complete affected runner/manifest subset: `known-red-baseline`; 124 tests and
  443 subtests passed with exactly the two Slice 2-owned failures named above.
  Slice 2 must promote both nodes to required-green without adding a failure.
- `scripts/command_owner_scenarios.py validate
  tests/fixtures/command-owner-scenarios`: `required-green`; baseline 82
  scenarios.
- Touched-path Ruff with `--no-cache`: `required-green`; baseline passed.
- Existing runner BasedPyright subset: `known-red-baseline`; 56 errors, zero
  warnings, zero notes. The batch must add no diagnostic.
- New `scripts/batch_execution_state*.py` BasedPyright gate:
  `implementation-created` by Slice 1, then `required-green`.
- Candidate install status and dry-run: `required-green`; planning baseline
  converged.
- Stable Planning State `current` and `validate`: `required-green` at pickup,
  after queue mutation, and at same-batch closeout.

Implementation-created gates:

- `tests/test_batch_execution_state.py`,
  `tests/test_batch_execution_state_store.py`, and
  `tests/test_batch_execution_state_process.py`: Slice 1.
- `.github/workflows/batch-execution-state.yml`: Slice 1; exact
  Ubuntu/macOS/Windows green run required at final acceptance.
- `tests/test_work_batch_flight_contract.py`: Slice 2.
- `skills/work-batch/references/batch-execution-state-v1.schema.json`: Slice 1.
- `skills/work-batch/references/execution-flight-result-v1.schema.json`: Slice 2.
- New command-owner scenario rows/aliases proving one-flight ownership and
  forbidden Batch Runway fallback: Slice 2.

Every test-changing Slice requires a delta-only `test-quality-review` before
the independent runway review.

## Slice 1: Canonical Execution-State Owner

Risk class: `migration`.

### Vertical Slice

```yaml
vertical_slice:
  starting_scenario: no Batch Execution State exists for an accepted batch and an explicit generated-only root is supplied
  durable_result: one public apply/query interface atomically owns initialization, attempts, resolutions, exact replay, receipts, and projections at the batch-stable path
  owner_before: no canonical structured batch execution owner; Markdown, manifests, and per-run state are non-authoritative observations
  owner_after: candidate Batch Execution State deep module
  migrated_callers:
    - generated-only execution-state acceptance fixture and public module CLI
  focused_validation:
    - deterministic reducer and schema behavior
    - real-process initialization, writer, lock, replay, crash, and killed-holder tests
    - receipt, result, manifest, and Markdown projection ordering
    - path safety, corruption, orphan, and no-next-action tests
  independently_usable_state: callers can initialize and advance one batch through the accepted interface without coordinating schema, lock, replacement, receipt, or projection internals
  rollback_boundary: revert the Slice 1 candidate commit and remove only generated acceptance artifacts before any real candidate runtime state is retained
  temporary_residue:
    - real runner and public work-batch are not integrated until Slice 2
    - automatic continuation, recovery, finalization, and closeout remain unimplemented
```

### Scope

- Add one cohesive candidate execution-state owner with a small typed
  `apply(state_path, event, expected_state)`-style public seam and an exact
  query/derivation operation. Use separate internal model/store modules when
  that keeps the facade deep and the implementation cohesive; file count is not
  an acceptance metric.
- Hide schema validation, domain parsing, inter-process lock backend, pure
  reduction, expected-state CAS, idempotency, atomic replacement, reread
  validation, immutable result/receipt handling, and projection repair.
- Implement `batch-execution-state/v1` and the accepted event vocabulary:
  initialize, reserve, authorize launch, and resolve completed/blocked/failed.
- Use exact event ID plus canonical request digest replay before current-revision
  rejection. Compare initialization against absence.
- Keep the lock short-lived and outside external effects. Fail closed on
  timeout, unsupported storage, backend failure, or weak fallback.
- Perform a bounded dependency comparison. Add at most one mature internal lock
  dependency only if it satisfies the observable cross-platform contract; do
  not leak its API or errors through the public seam.
- Persist canonical state first, then exact receipt, then derived manifest and
  Markdown. Orphans do not advance state.
- Add a focused cross-platform workflow and executable local acceptance tests.

### Allowed Candidate Files Or Areas

- `scripts/batch_execution_state.py` (new public facade/CLI)
- `scripts/batch_execution_state_model.py` (new pure typed reducer)
- `scripts/batch_execution_state_store.py` (new persistence/lock owner)
- `skills/work-batch/references/batch-execution-state-v1.schema.json` (new)
- `tests/test_batch_execution_state.py` (new public behavior)
- `tests/test_batch_execution_state_store.py` (new persistence behavior)
- `tests/test_batch_execution_state_process.py` (new real-process behavior)
- `.github/workflows/batch-execution-state.yml` (new)
- `pyproject.toml` and `uv.lock` only if one lock dependency is accepted
- `README.md` and `CHANGELOG.md` only for the public execution-state contract,
  explicit root input, and validation guidance

No stable implementation file is write-bearing.

### Non-Goals

- No runner `execute` integration or `work-batch` behavior change.
- No agent launch or external work inside the lock.
- No automatic continuation, recovery event, finalization, closeout, queue
  currentness, or successor behavior.
- No platform-specific lock primitive in the public API.
- No per-run state path, latest-run lookup, Git authority, or mutable
  `next_action` field.

### Acceptance Criteria

- The public interface is deep: callers provide the exact state path, one typed
  event, and tagged expected state; they receive one normalized outcome.
- Revision 0 is created exclusively from absence; concurrent initialization has
  one winner, exact replay, and no overwrite.
- Completed Slices remain a contiguous prefix and only the first incomplete
  Slice can be reserved.
- `reserved -> in_flight` is explicit; completed/blocked/failed resolution is
  exact, idempotent, and retains its immutable result reference.
- `next_action` is absent from mutable state and agent inputs; code derives it.
- Same event ID/request/expected-state returns the exact recorded outcome;
  collisions and stale new events fail without writes.
- Killed lock holders release ownership and a later process can validate the old
  or atomically replaced state.
- Fault checkpoints cover initialization, reservation, launch, result,
  resolution CAS, receipt, and projections in fresh processes.
- New module tests and BasedPyright are green. Local real-process tests pass.
- The matrix workflow runs the real process/lock subset on Ubuntu, macOS, and
  Windows for the exact candidate commit before final batch acceptance.
- No production runner caller is claimed until Slice 2.

### Focused Validation

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider
  tests/test_batch_execution_state.py tests/test_batch_execution_state_store.py
  tests/test_batch_execution_state_process.py`: `implementation-created`, then
  `required-green`.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/ruff check --no-cache
  scripts/batch_execution_state.py scripts/batch_execution_state_model.py
  scripts/batch_execution_state_store.py tests/test_batch_execution_state.py
  tests/test_batch_execution_state_store.py
  tests/test_batch_execution_state_process.py`:
  `implementation-created`, then `required-green`.
- `.venv/bin/basedpyright scripts/batch_execution_state.py
  scripts/batch_execution_state_model.py scripts/batch_execution_state_store.py`:
  `implementation-created`, then
  `required-green`.
- `python -m json.tool
  skills/work-batch/references/batch-execution-state-v1.schema.json`:
  `implementation-created`, then `required-green`.
- Workflow syntax and exact test-command inspection: `implementation-created`,
  then `required-green`; real three-platform workflow result: `conditional`
  until the exact commit is publishable, then required before final batch
  acceptance.
- `git diff --check`: `required-green`.

### Test Quality Review

Required, delta-only. Review behavioral confidence through the public
interface, real process isolation, crash/replay assertions, assertion strength,
fixture friction, and accidental topology coupling. Coverage percentage is not
an acceptance criterion.

### Commit

`feat(work-batch): add canonical batch execution state`

### Worker Brief

The spawned `runway_worker` is the coding subagent. Implement only Slice 1 in
the candidate checkout. Read the runway, accepted design contract, ADR, and
fresh strict live lease. Do not spawn, delegate to, or wait on other agents.
Do not touch stable planning, integrate the runner, change `work-batch`, run
project-wide exact acceptance, publish the workflow, or implement later CCFG-26
semantics. Return exact changed paths, focused validation, dependency choice
evidence, and verified strict context.

### Reviewer Brief

The independent `runway_reviewer` receives the exact task-scoped diff basis,
runway path, accepted design/ADR, focused validation, test-quality result, and a
fresh read-only live lease. Verify deep-module quality, public-interface
behavior, crash/CAS/replay correctness, platform-gate honesty, scope, and absence
of horizontal scaffolding. Echo `diff_basis` and return `clean` or
`correction_required`.

### Stop Conditions

- Stop if the public interface exposes the schema, lock backend, replacement
  protocol, receipt repair, or projection ordering to callers.
- Stop if a smaller split would leave uncalled internal scaffolding.
- Stop if state writes occur outside the exact batch-stable path or an orphan
  advances progress.
- Stop if any transition relies on Git, Markdown, Run State, a manifest, or
  agent-authored action.
- Stop if the lock library requires a weak fallback, leaves stale ownership
  after process death, or lacks a credible real-platform test path.
- Stop if runner/work-batch integration, automatic continuation, recovery,
  finalization, closeout, or successor logic enters the diff.

## Slice 2: One-Flight Public `work-batch` Tracer

Risk class: `migration`.

### Vertical Slice

```yaml
vertical_slice:
  starting_scenario: Planning State identifies one queued runway with at least two fixture Slices, the explicit root is supplied, and no Batch Execution State exists
  durable_result: the real candidate runner launches one fresh public work-batch coordinator, one Slice resolves completed through canonical state, continue_same_batch is derived, and the existing execute phase stops compatibly for manual continuation
  owner_before: candidate runner execute routes semantic execution through Batch Runway public support
  owner_after: public work-batch owns the one-flight proceed, reserve, authorize, accept, resolve, and stop decisions; runner owns process lifecycle; execution-state module owns progression
  migrated_callers:
    - candidate serialized execute phase contract and command path
    - public candidate work-batch first-tracer route
    - command-owner behavioral acceptance fixture
  focused_validation:
    - exact public work-batch launch and no Batch Runway public fallback
    - action-free execution-flight-result validation against state and receipt
    - one worker, reviewer, commit, completed Slice, and continue_same_batch
    - compatible stopped Phase Result and exact fresh manual resume
    - no finalization, closeout, automatic second flight, or successor
  independently_usable_state: a later fresh invocation deterministically receives the exact next Slice without chat history and cannot repeat or overlap the completed Slice
  rollback_boundary: revert only the Slice 2 candidate commit; Slice 1 state owner and generated-only tests remain usable, and remove any tracer fixture state created under the explicit root
  temporary_residue:
    - manual relaunch remains required until the separate automatic-continuation milestone
    - unmigrated recovery, finalization, closeout, and Batch Runway support callers retain exact later removal conditions
```

### Scope

- Make public candidate `work-batch` the semantic owner for exactly the first
  one-flight tracer.
- Pass the exact run-artifact root and accepted runway identity into one fresh
  coordinator.
- Confirm Planning State currentness, initialize canonical state if absent,
  reserve the first incomplete Slice, and persist `in_flight` immediately before
  the effectful worker launch.
- Preserve worker, focused validation, independent reviewer, commit, receipt,
  execution-ledger, and completed-slice obligations for exactly one Slice.
- Write and validate one immutable result, resolve it under expected-revision
  CAS, and return strict `execution-flight-result/v1` without `next_action`.
- Make the runner reload the exact state and receipt, derive
  `continue_same_batch`, and map this first milestone to the existing compatible
  stopped execute Phase Result without changing the serialized phase identity.
- Prove a later exact resume launches a fresh coordinator against the same
  state path and selects the next incomplete Slice without re-executing the
  first.
- Update candidate installation and exact command-owner scenario evidence.

### Allowed Candidate Files Or Areas

- `skills/work-batch/`
- `scripts/batch_execution_state.py` only for integration corrections required
  by its accepted public interface
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_artifacts.py` only for non-authoritative
  Execution Flight observation links
- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner_environment.py`
- `scripts/architecture_program_runner_execution.py` (new flight-result and
  one-flight lifecycle owner)
- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_state.py`
- `scripts/architecture_program_runner_transition.py` only if a focused failing
  compatibility test proves a change is required; stopped results already
  preserve the active `execute` phase
- `scripts/architecture_program_runner_validation.py`
- `scripts/architecture_program_runner_workers.py`
- `skills/work-batch/references/execution-flight-result-v1.schema.json` (new)
- `skills/architecture-program-runway/references/local-runner-v1.md`
- `tests/test_work_batch_flight_contract.py` (new)
- Focused `tests/test_architecture_program_runner_*.py` modules named in the
  planning snapshot
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/fixtures/command-owner-scenarios/`
- `tests/test_codex_features_manifest.py`
- `codex-features.json`, `README.md`, and `CHANGELOG.md`
- `docs/skill-routing-contract.md` and `docs/workflow-guide.md` only for the
  target happy-path owner/support distinction

No stable implementation file is write-bearing.

### Non-Goals

- No automatic launch of a second Execution Flight.
- No ambiguous-attempt recovery or relaunch.
- No finalization or closeout transition.
- No change to `PHASES = (select-dispatch, create-spec, execute, closeout)`.
- No migration/removal decision for `select-dispatch` or `create-spec`.
- No removal of Batch Runway support for exact unmigrated callers, but the new
  tracer may not expose or silently fall back to it.
- No stable-home install, stable runner edit, target queue mutation, or
  successor selection.

### Acceptance Criteria

- Candidate runner `execute` launches the public `work-batch` first-tracer
  route exactly once; `$batch-runway execute-spec` is not the public target
  instruction for that route.
- One fresh coordinator may advance at most one Slice.
- Reservation and launch authorization occur inside that coordinator after
  Planning State/currentness checks and immediately before the effectful worker.
- One worker, focused validation, independent reviewer, candidate commit,
  immutable result, resolution, transition receipt, and completed-slice
  projection are observed.
- The strict Execution Flight Result contains only status, batch, Slice,
  attempt, exact state path, resolved revision, and receipt path. Unknown fields
  and `next_action` are rejected.
- Runner code reloads canonical state, validates the exact receipt and
  identities, and derives `continue_same_batch` without reading generic
  `evidence_paths`, Markdown progress, or Git topology.
- The first milestone returns the compatible stopped Phase Result with active
  phase still `execute` and exact reason `manual_continuation_required`.
- No second coordinator, automatic continuation, finalization, closeout, or
  successor is started.
- Exact resume uses the same state path and candidate baseline, starts a new
  coordinator, and binds only the next incomplete Slice. A concurrent or
  unresolved attempt fails closed.
- Every retained Batch Runway route names its exact caller, reason, future
  owner, and removal condition. There is no target fallback.
- Candidate `work-batch` and impacted feature versions/install links converge;
  stable-home content remains unchanged.

### Focused Validation

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider
  tests/test_work_batch_flight_contract.py`: `implementation-created`, then
  `required-green`.
- Focused runner/workflow subset used at planning baseline plus Slice 1 tests:
  `required-green`.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider
  tests/test_codex_features_manifest.py`: `required-green` for the filtered
  work-batch/runner ownership nodes; any unrelated known-red node remains
  diagnostic and must not regress.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python
  scripts/command_owner_scenarios.py validate
  tests/fixtures/command-owner-scenarios`: `required-green`.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/ruff check --no-cache` over touched
  production/tests: `required-green`.
- `.venv/bin/basedpyright scripts/batch_execution_state.py`: `required-green`.
- Existing runner BasedPyright subset: `known-red-baseline` at 56 errors; no new
  diagnostic is accepted.
- `.venv/bin/python scripts/skill_contract.py validate --toolchain-root .
  skills/work-batch/SKILL.md`: `required-green`.
- `python -m json.tool
  skills/work-batch/references/execution-flight-result-v1.schema.json`:
  `implementation-created`, then `required-green`.
- Candidate install status/dry-run: `required-green`.
- `git diff --check`: `required-green`.

### Test Quality Review

Required, delta-only. Review the one-flight tests for observable public behavior,
exact identity/result/receipt assertions, fresh-process proof, negative fallback
coverage, non-overlap, and absence of mock-heavy topology assertions.

### Commit

`feat(work-batch): prove one canonical execution flight`

### Worker Brief

The spawned `runway_worker` is the coding subagent. Implement only Slice 2 in
the candidate checkout using the accepted Slice 1 public interface and a fresh
strict live lease. Do not spawn, delegate to, or wait on other agents. Do not
edit stable planning, implement automatic continuation/recovery/finalization/
closeout, change serialized phase identities, remove broad legacy owners, run
final exact acceptance, publish the matrix workflow, or select a successor.
Return exact changed paths, focused validation, retained-caller matrix, and
verified strict context.

### Reviewer Brief

The independent `runway_reviewer` receives the exact task-scoped diff basis,
runway path, design/ADR, Slice 1 interface/receipt, focused validation,
delta-only test-quality result, and a fresh read-only live lease. Verify the
real public caller, one-flight boundary, reservation timing, action-free result,
code-derived continuation, stopped compatibility, exact resume, forbidden
fallback, retained-caller evidence, and absence of later semantics. Echo
`diff_basis` and return `clean` or `correction_required`.

### Stop Conditions

- Stop if the runner, not `work-batch`, chooses a Slice, accepts an attempt
  result, mutates execution state semantically, or owns recovery.
- Stop if `work-batch` launches a worker before `in_flight` is durable.
- Stop if a result includes `next_action`, if the runner trusts generic evidence
  paths, or if progression is inferred from Markdown, Run State, manifests, or
  Git.
- Stop if the target tracer invokes Batch Runway as its public/semantic owner or
  silently falls back to it.
- Stop if more than one Slice or coordinator runs in one Execution Flight.
- Stop if automatic continuation, recovery, finalization, closeout, successor
  selection, phase-label change, or stable implementation enters the diff.
- Stop if exact fresh resume cannot identify the next Slice from artifacts and
  code alone.

## Final Validation And Acceptance

After both Slice commits exist:

1. Re-run stable Planning State `current` and `validate`; confirm the same batch
   remains current and no successor is selected.
2. Refresh the strict live context and verify the exact candidate range. Reject
   unexplained stable or candidate movement.
3. Run focused execution-state and one-flight tests plus the relevant existing
   runner/workflow subset with no pytest cache and no bytecode writes.
4. Run the complete command-owner scenario catalog validation and exact
   acceptance against the exact candidate commit. Store result JSON, report
   JSON, and text report under explicit generated-only subpaths beneath
   `/tmp/tmp.nAyp7HeqwO`; read the text report and validate both JSON documents
   before reporting success.
5. Run touched-path Ruff, new-module BasedPyright, the exact 56-error runner
   BasedPyright non-regression comparison, schema validation, skill-contract
   validation, manifest tests, and `git diff --check`.
6. Install only into `/home/alacasse/.codex-command-owner-redesign`, verify
   status and dry-run convergence, and prove stable-home state is unchanged.
7. Run the focused Ubuntu/macOS/Windows workflow against the exact candidate
   commit. Green evidence is required. If publishing/running it is outside the
   current authority, stop with the batch active and report that single
   external gate; do not weaken or simulate it.
8. Run final exact-range delta-only test-quality review, independent runway
   review, and import-topology review if local import topology changed.
9. Finalize and close only this implementation batch through existing stable
   execution/closeout mechanisms. Reconcile parent CCFG-26 to `Prepared` or
   equivalent partial status, not `Closed`.
10. Record that Automatic Same-Batch Continuation, recovery, finalization,
    target closeout, and displaced-owner narrowing remain. Select no successor.

## Batch Stop Conditions

- Stop on scope drift, dirty-file overlap, missing subagent role, missing fresh
  live lease, changed selected scope, or unexpected repository movement.
- Stop if the explicit runtime root or canonical state path is missing,
  ambiguous, reused by another batch, or pre-populated before initialization.
- Stop if stable source, canonical planning outside this batch transaction, or
  candidate-local planning is written.
- Stop if CCFG-26B is treated as current or CCFG-26C through CCFG-26E are
  selected.
- Stop if cross-platform evidence is unavailable; preserve the same active
  batch and exact next action.
- Stop if the real tracer requires automatic continuation, recovery,
  finalization, closeout, a new phase label, or a stable/candidate switch to be
  useful.
- Stop if any unsupported compatibility, alias, facade, fallback, or topology
  assertion is added without a named caller, reason, future owner, and removal
  condition.
- Stop if Graphify is invoked or its output is treated as authority.

## Closeout Handoff

Closeout evidence must identify:

- exact stable planning and candidate implementation revisions;
- exact generated-only runtime root and canonical state path;
- both Slice commits and exact independent review bases;
- local focused validation and exact scenario acceptance;
- real Ubuntu/macOS/Windows matrix evidence for the exact candidate commit;
- candidate install convergence and unchanged stable home;
- completed one-flight behavior and exact manual-resume proof;
- remaining Automatic Same-Batch Continuation, recovery, finalization, target
  closeout, and owner-narrowing work; and
- `successor_selected: false`.

This `plan-batch` invocation stops after queueing and validation. It implements
no Slice.
