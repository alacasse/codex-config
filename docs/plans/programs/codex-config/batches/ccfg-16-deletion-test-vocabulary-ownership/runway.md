# CCFG-16 Runway: Deletion-Test Vocabulary Ownership

## Purpose

Define one project-neutral deletion-test evidence vocabulary owner and align the
consumer skills that generate or execute dispatch/runway artifacts. The outcome
should let future CCFG-11 planning avoid ambiguous deletion-test labels without
performing deletion cleanup in this batch.

## Batch Kind And Slice Risk Contract

- Batch kind: `decision`
- Risk posture: no destructive cleanup, migration, demotion, deletion, or
  contract narrowing is authorized.
- Risky slices: none.
- Approval gates: none required because every slice is `decision-only` or
  `none`; if implementation discovers a need for deletion, demotion, migration,
  or contract narrowing, stop and create explicit follow-up ledger work.

## Current Baseline And Assumptions

- Planning root: `docs/plans/`
- Program root: `docs/plans/programs/codex-config/`
- Selected dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/dispatch.md`
- Queued runway:
  `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/runway.md`
- `planning_state.py current --root docs/plans` reported no selected, queued,
  or active batch before this spec was created.
- `planning_state.py validate --root docs/plans` passed with redirect-ledger
  warnings only.
- Existing focused contract subset passed:
  `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py tests/test_batch_runway_create_spec_contract.py -q`
  produced `23 passed`.
- Broader consumer-projection subset is currently a known-red baseline:
  `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py tests/test_batch_runway_create_spec_contract.py tests/test_planning_state_consumer_projection_routing.py -q`
  produced `34 passed, 7 failed`, with failures in
  `tests/test_planning_state_consumer_projection_routing.py`.
- `python -m ruff --version` currently fails with `No module named ruff`.

## Non-Goals

- Do not execute, regenerate, or amend CCFG-11 beyond naming its future
  dependency on this batch.
- Do not perform deletion-test cleanup.
- Do not delete, narrow, demote, or migrate any skill surface.
- Do not make `dead-surface-audit` responsible for program selection, dispatch
  state, runway creation, commits, or closeout.
- Do not add codex-config-specific paths or validation commands to reusable
  skill guidance.

## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about
suspicious coordinator or subagent-lifecycle behavior.
Use the expanded convergence template only when scope is expanding, significant
uncertainty exists, blockers are present, or final batch reporting is being
produced.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v1.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`

Overrides:

- None.

## Validation Profile

Selected profile: `test-only-topology`

Profile reference:
`skills/batch-runway/references/validation-profiles/test-only-topology.md`

Focused validation commands:

- `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py tests/test_batch_runway_create_spec_contract.py -q`
  - Status class: `required-green`
  - Baseline: passed with `23 passed`.
- `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`
  - Status class: `known-red-baseline`
  - Baseline: currently has unrelated existing failures; this command can be
    used diagnostically if touched, but must not block this batch unless a slice
    explicitly remediates and promotes it.
- `python -m pytest tests/test_deletion_test_vocabulary_ownership.py -q`
  - Status class: `implementation-created`
  - Created by: Slice 1 if a new focused test file is used.
- `python -m ruff check tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py tests/test_batch_runway_create_spec_contract.py`
  - Status class: `known-red-baseline`
  - Baseline: `python -m ruff --version` fails because `ruff` is not installed.
    Use an available project-approved ruff runner only if the executor can do so
    without installing dependencies.
- `git diff --check`
  - Status class: `required-green`
  - Baseline: passed.

## Execution Ledger

| Slice | Status | Risk class | Commit | Validation | Review | Notes |
|---|---|---|---|---|---|---|
| 1. Evidence vocabulary owner | Completed | decision-only | `056a576` | `tests/test_deletion_test_vocabulary_ownership.py` passed; selected profile subset passed; `git diff --check` passed | clean | Archived in `completed-slices.md`. |
| 2. Legacy-removal consumer boundary | Completed | decision-only | `7070f88` | `tests/test_deletion_test_vocabulary_ownership.py` passed; selected profile subset passed; `git diff --check` passed | clean | Archived in `completed-slices.md`. |
| 3. Generated artifact consumer rules | Completed | decision-only | `2dc852e` | `tests/test_deletion_test_vocabulary_ownership.py` passed; selected profile subset passed; `git diff --check` passed | clean | Archived in `completed-slices.md`. |
| 4. CCFG-like regression guard | Completed | decision-only | `921dc0a` | `tests/test_deletion_test_vocabulary_ownership.py` passed; selected profile subset passed; `git diff --check` passed | clean | Archived in `completed-slices.md`. |

## Slice 1: Evidence Vocabulary Owner

Risk class: `decision-only`

Scope:

- Define `dead-surface-audit` as the canonical owner for deletion-test evidence
  vocabulary.
- Keep the existing evidence statuses project-neutral, including `keep`,
  `delete-now`, `migrate-tests-first`, `keep-thin-entrypoint`, and
  `human-contract-decision`.
- State that labels such as `no-op`, `sediment`, `obsolete skill surface`, and
  `deletion-safe evidence` are not canonical deletion-test evidence categories
  unless locally defined as non-canonical labels in a specific artifact.

Allowed files or areas:

- `skills/dead-surface-audit/SKILL.md`
- Focused test files under `tests/`

Non-goals:

- Do not add program queue, selected dispatch, concrete runway, commit, or
  closeout ownership to `dead-surface-audit`.
- Do not rename or remove existing evidence statuses.

Acceptance criteria:

- The owner skill explicitly names canonical deletion-test evidence statuses.
- The owner skill rejects or scopes non-canonical generated labels.
- Focused tests prove `dead-surface-audit` remains an evidence producer and
  vocabulary owner only.

Validation:

- Run the selected `test-only-topology` profile.
- Run the focused pytest command covering the touched test module.
- Run `git diff --check`.

Commit message:

`Define deletion-test evidence vocabulary owner`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only Slice 1, do not spawn or wait on additional subagents, and
do not touch CCFG-11 execution artifacts except as read-only context.

Review subagent brief:

Review the exact task-scoped diff basis provided by the coordinator. Confirm the
owner boundary is project-neutral, preserves `dead-surface-audit` as evidence
producer only, and does not authorize deletion cleanup.

Stop conditions:

- Stop if the owner cannot be expressed without making `dead-surface-audit` the
  planning or execution owner.

## Slice 2: Legacy-Removal Consumer Boundary

Risk class: `decision-only`

Scope:

- Clarify that `legacy-removal` consumes canonical deletion-test evidence
  statuses and owns compatibility/cleanup-residue decisions.
- Prevent `legacy-removal` from silently redefining deletion-test evidence
  categories while preserving its existing decision authority.

Allowed files or areas:

- `skills/legacy-removal/SKILL.md`
- Focused test files under `tests/`

Non-goals:

- Do not make `legacy-removal` the selected program owner for this codex-config
  batch.
- Do not create a parallel legacy-removal ledger.

Acceptance criteria:

- `legacy-removal` distinguishes evidence vocabulary ownership from legacy
  compatibility decision ownership.
- Tests cover the consumer boundary without changing runtime behavior.

Validation:

- Run the selected `test-only-topology` profile.
- Run focused pytest for the touched tests.
- Run `git diff --check`.

Commit message:

`Align legacy-removal deletion-test vocabulary consumption`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only Slice 2 and do not delegate. Preserve project-neutral
language and avoid queue-state changes outside the concrete execution ledger.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm `legacy-removal` consumes
evidence terms, owns compatibility decisions, and does not redefine canonical
deletion-test categories.

Stop conditions:

- Stop if this slice starts selecting, dispatching, or executing legacy-removal
  work outside the current batch.

## Slice 3: Generated Artifact Consumer Rules

Risk class: `decision-only`

Scope:

- Clarify that `architecture-program-runway` selected dispatches and
  `batch-runway` generated runways must use canonical deletion-test evidence
  statuses or locally define non-canonical labels.
- State that generated artifacts must not make unsupported terms behave like
  evidence categories, approval gates, or cleanup decisions.

Allowed files or areas:

- `skills/architecture-program-runway/SKILL.md`
- `skills/batch-runway/references/create-spec.md`
- Focused test files under `tests/`

Non-goals:

- Do not duplicate the full dead-surface-audit vocabulary in every consumer
  skill; point to the owner and specify consumer obligations.
- Do not change Batch Runway execution semantics.

Acceptance criteria:

- `architecture-program-runway` selected-dispatch guidance preserves canonical
  vocabulary or local label definitions.
- `batch-runway` create-spec guidance prevents generated runways from inventing
  deletion-test evidence categories.
- Tests cover both consumer surfaces.

Validation:

- Run the selected `test-only-topology` profile.
- Run focused pytest for the touched tests.
- Run `git diff --check`.

Commit message:

`Require canonical deletion-test labels in generated artifacts`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only Slice 3, do not spawn other agents, and keep
Batch Runway create-spec guidance project-neutral.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm generated artifact guidance
uses canonical terms or local definitions and does not authorize destructive or
contract-narrowing work.

Stop conditions:

- Stop if the slice would add destructive cleanup, migration, or approval-gate
  semantics instead of vocabulary-consumption rules.

## Slice 4: CCFG-Like Regression Guard

Risk class: `decision-only`

Scope:

- Add or extend focused regression coverage for CCFG-11-like generated dispatch
  and runway text.
- Reject unsupported deletion categories such as ambiguous `no-op`, `sediment`,
  `obsolete skill surface`, and `deletion-safe evidence` unless they are
  explicitly local, non-canonical labels with definitions.
- Preserve future CCFG-11 replanning safety without replanning CCFG-11 now.

Allowed files or areas:

- Focused test files under `tests/`
- Minimal skill/reference wording touched by the tests if a previous slice left
  a gap
- Program ledger/current closeout updates only when finalizing the batch

Non-goals:

- Do not rewrite the superseded CCFG-11 runway into an executable plan.
- Do not execute deletion cleanup.

Acceptance criteria:

- A CCFG-like fixture or assertion fails if generated text invents unsupported
  deletion-test evidence categories.
- Future CCFG-11 planning can consume the owner/consumer contract without using
  ambiguous deletion-test terminology.
- Final closeout can mark CCFG-16 closed only with validation and review
  evidence.

Validation:

- Run the selected `test-only-topology` profile.
- Run focused pytest for the touched tests.
- Run `git diff --check`.

Commit message:

`Guard generated deletion-test vocabulary`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only Slice 4 and do not use the superseded CCFG-11 runway as an
active execution source.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm the regression is
project-neutral, catches invented generated labels, and does not replan or
execute CCFG-11.

Stop conditions:

- Stop if regression coverage requires broad CCFG-11 cleanup or destructive
  work to pass.

## Final Validation

Required:

- `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py tests/test_batch_runway_create_spec_contract.py -q`
- Focused pytest for any new or renamed deletion-test vocabulary test module.
- `git diff --check`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`

Conditional:

- Run `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`
  only if the batch changes that file or remediates its known-red baseline.
- Run ruff through an available project-approved runner only if available
  without dependency installation.

## Stop Conditions

- Stop if work would execute, regenerate, or broaden CCFG-11.
- Stop if work would delete, demote, narrow, migrate, or clean up a skill
  surface.
- Stop if work would make evidence vocabulary labels act as approval gates.
- Stop if work would put project-specific paths, validation commands, cache
  locations, or local planning layouts into reusable skill guidance.
- Stop if subagent tooling required by Batch Runway execution is unavailable.

## Handoff

Execute with `work-batch`. The execution coordinator should start at Slice 1,
delegate each slice to `runway_worker`, review each completed slice with
`runway_reviewer`, commit after each clean slice, and update this ledger plus
completed-slice archive as required by Batch Runway Standard Execution Contract
v1.
