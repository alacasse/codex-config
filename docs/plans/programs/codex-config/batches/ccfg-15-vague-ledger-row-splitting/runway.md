# Vague Ledger Row Splitting Runway

## Purpose

Add durable `plan-batch` / `architecture-program-runway` guidance and focused
regression coverage so vague or mixed-risk ledger rows are split, blocked, or
narrowed before selected dispatch and concrete runway creation.

This spec executes the `ccfg-15-vague-ledger-row-splitting` batch described by
`docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/dispatch.md`.
It is a prerequisite before CCFG-11 is regenerated or executed.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/dispatch.md`.
- Included finding: CCFG-15.
- CCFG-13 and CCFG-14 are complete and provide validation-command status,
  batch-kind, slice-risk, and approval-gate prerequisites.
- CCFG-11 remains open, but its displaced dispatch/runway pair is superseded
  planning evidence and must not be executed as active state.

## Batch Kind And Risk Metadata

Batch kind: `mixed-risk`.

Risk rationale:
- The batch includes normal guidance, tests, and planning-evidence updates.
- Slice 1 intentionally narrows the planning contract so vague or mixed-risk
  ledger rows cannot silently expand into mixed evidence, decision, migration,
  contract-narrowing, or destructive-cleanup runways.
- No slice may perform destructive cleanup, migration, demotion, contract
  narrowing of product behavior, or CCFG-11 execution.

Risk classes:
- Slice 1: `contract-narrowing`
- Slice 2: `none`
- Slice 3: `decision-only`

Approval gate for Slice 1:
- The CCFG-15 ledger row and dispatch authorize narrowing only the planning
  behavior for vague or mixed-risk ledger-row expansion.
- Before implementation, the coordinator must confirm the diff is limited to
  `plan-batch` / `architecture-program-runway` guidance and focused tests for
  split, block, or narrow behavior.
- Stop and ask the user if execution would block precise bounded rows, change
  runner execution semantics, create fresh ledger findings from source text, or
  add project-specific planning rules to reusable skills.

## Assumptions

- This is a planning-contract guard, not execution of CCFG-11.
- The reusable guidance should define portable selection and dispatch-shaping
  rules, not codex-config-specific row text.
- A CCFG-11-like row is evidence for the unsafe shape; it is not active work for
  this batch.
- Existing text-contract tests are acceptable for skill guidance until a
  narrower parser or fixture owner exists.

## Non-Goals

- Do not implement any slice during spec creation.
- Do not execute, regenerate, amend, or implement CCFG-11.
- Do not create new ledger findings from CCFG-15 execution notes.
- Do not make vague-row handling a codex-config-only local policy.
- Do not build a new planner engine, schema, or runner phase.
- Do not weaken CCFG-13 validation-command status or CCFG-14 batch-kind/risk
  gates.

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
- Use `full-runway` density because this batch changes a subtle planning
  contract and must preserve the `plan-batch` / `architecture-program-runway`
  owner split.
- Workers must keep reusable workflow guidance project-neutral.
- Workers must not execute, regenerate, amend, or implement CCFG-11.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- `python scripts/planning_state.py current --root docs/plans`
  - status: `required-green`
  - scope: planning-state diagnostics
- `python scripts/planning_state.py validate --root docs/plans`
  - status: `required-green`
  - scope: planning-state diagnostics
- `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py -q`
  - status: `required-green`
  - scope: command-owner and architecture-program-runway guidance contracts
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  - status: `required-green`
  - scope: CCFG-13/CCFG-14 create-spec contract guard regression
- `python -m pytest tests/test_codex_features_manifest.py -q`
  - status: `known-red-baseline`
  - scope: diagnostic only unless a slice explicitly remediates existing
    manifest contract drift
- `git diff --check`
  - status: `required-green`
  - scope: all slices

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No SQLite database or durable JSON planning-state file is required.

Harness output:
- Existing `current`, `validate`, and focused pytest checks should not write
  live planning files.
- No generated summary artifact is required.

Index refresh:
- None required for these skill, tests, and planning-doc edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 3. Reconcile CCFG-11 Planning Evidence | Pending |  |  |  | CCFG-11 remains superseded and future planning points at the new guard | Planning evidence and closeout notes only. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Guard Vague Row Selection | `4b531af` | `plan-batch` and `architecture-program-runway` now require vague or mixed-risk ledger rows to be split, blocked, or narrowed before selected dispatch and concrete runway creation. | Validation: `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`. Review: clean `runway_reviewer` pass against HEAD for `skills/plan-batch/SKILL.md` and `skills/architecture-program-runway/SKILL.md`. |
| 2. Test Split Block Narrow Contract | `0ab3ad9` | Added focused text-contract tests proving `plan-batch` rejects vague CCFG-11-like mixed-risk rows and `architecture-program-runway` requires split, block, or narrow rationale before selected dispatch creation. | Validation: `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py -q`; `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`. Review: clean `runway_reviewer` pass with delta-only test-quality review after newline-sensitive assertions were fixed. |

## Slice 1. Guard Vague Row Selection

Scope:
- Update `plan-batch` guidance so requested ledger rows are suitable only when
  they are precise enough for one bounded selected dispatch.
- Update `architecture-program-runway` selection/dispatch guidance so vague or
  mixed-risk rows are split, blocked, or narrowed before `dispatch.md` is
  created.
- Define portable signals for rows that mix evidence gathering,
  classification, decisions, destructive cleanup, migration, demotion, or
  contract narrowing without enough owner, risk, or acceptance boundaries.

Allowed files/areas:
- `skills/plan-batch/SKILL.md`
- `skills/architecture-program-runway/SKILL.md`
- `skills/architecture-program-runway/references/program-ledger-template.md`
  only if the template needs a short dispatch-shaping pointer.
- `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/`

Non-goals:
- Do not edit CCFG-11 artifacts in this slice.
- Do not change Batch Runway create-spec risk metadata from CCFG-14 unless a
  wording bug blocks this guard.
- Do not add codex-config-specific row examples to reusable guidance.

Acceptance criteria:
- `plan-batch` says existing ledger rows are not suitable for direct planning
  when they are too vague or mixed-risk for one bounded selected dispatch.
- `architecture-program-runway` says selected dispatch creation must record
  split, block, or narrow-scope rationale before handing work to Batch Runway.
- Guidance prefers characterization-only or evidence-only dispatches when a row
  mentions deletion, demotion, migration, cleanup, or narrowing but lacks
  precise owner, risk, and acceptance boundaries.
- Guidance routes newly discovered destructive, migration, demotion, or
  contract-narrowing work to explicit follow-up ledger work unless the source
  row already authorized that risk.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Not required unless tests change in this slice.

Commit message:
- `Guard vague row selection`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep reusable workflow guidance project-neutral and preserve the
  `plan-batch` / `architecture-program-runway` owner split.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope and guidance clarity.
- Confirm the guidance blocks vague mixed-risk expansion without blocking
  precise bounded ledger rows.
- Echo the coordinator-provided `diff_basis` in compact YAML output.

Stop conditions:
- The guard cannot be expressed without a broader planner or runner rewrite.
- The change would make `plan-batch` create fresh ledger findings from source
  text.
- The change weakens CCFG-13 or CCFG-14 create-spec contracts.

## Slice 2. Test Split Block Narrow Contract

Scope:
- Add focused contract tests proving `plan-batch` and
  `architecture-program-runway` require vague or mixed-risk ledger rows to be
  split, blocked, or narrowed before selected dispatch and runway creation.
- Cover a CCFG-11-like deletion-test row shape without executing or
  regenerating CCFG-11.
- Keep tests focused on reusable guidance, not whole-file snapshots.

Allowed files/areas:
- `tests/test_skill_routing_rule_ownership.py`
- `tests/test_architecture_program_runway_status_vocabulary.py`
- A new focused test module under `tests/` if that is clearer than expanding
  existing files.
- `skills/plan-batch/SKILL.md` and
  `skills/architecture-program-runway/SKILL.md` only for wording adjustments
  needed to satisfy precise contract tests.
- `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/`

Non-goals:
- Do not add broad Markdown parser infrastructure.
- Do not snapshot complete skill files.
- Do not test CCFG-11 deletion surfaces themselves.

Acceptance criteria:
- Tests fail if `plan-batch` no longer rejects direct planning from vague or
  mixed-risk ledger rows.
- Tests fail if `architecture-program-runway` no longer requires selected
  dispatches to record split/block/narrow rationale for vague rows.
- Tests name the unsafe CCFG-11-like shape: evidence gathering plus
  classification plus decision or destructive cleanup in one vague row.
- Existing CCFG-13/CCFG-14 create-spec contract tests remain green.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py -q`
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required because this slice changes contract tests. Ask the reviewer to check
  that assertions protect behavior and avoid brittle wording trivia.

Commit message:
- `Test vague row split guards`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Preserve the existing text-contract test style unless a small helper removes
  real duplication.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, including test quality.
- Confirm tests would catch direct expansion of a vague CCFG-11-like row into a
  mixed-risk runway.
- Echo the coordinator-provided `diff_basis` in compact YAML output.

Stop conditions:
- Tests require a broad parser or fixture format change outside the focused
  contract test scope.
- The tests couple reusable guidance to codex-config-only planning paths except
  as named CCFG-11-like fixture evidence.

## Slice 3. Reconcile CCFG-11 Planning Evidence

Scope:
- Amend displaced CCFG-11 planning evidence only enough to record that future
  CCFG-11 planning must be split, blocked, or narrowed under the new CCFG-15
  guard before execution.
- Update `CHANGELOG.md` for the workflow behavior change if Slice 1 changes
  reusable skill behavior.
- Keep CCFG-11 open in the program ledger.
- Update this spec ledger/archive and closeout evidence for Slice 3 execution.

Allowed files/areas:
- `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/`
- `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/CURRENT.md`
- `CHANGELOG.md`

Non-goals:
- Do not execute or regenerate CCFG-11.
- Do not remove the displaced CCFG-11 planning evidence.
- Do not select successor work after CCFG-15 closeout.

Acceptance criteria:
- The displaced CCFG-11 artifact remains clearly superseded planning evidence,
  not active queue state.
- Future CCFG-11 planning is blocked unless it is split, blocked, or narrowed
  before selected dispatch and concrete runway creation.
- Program state still points to CCFG-15 as the queued batch until closeout.
- Closeout evidence records CCFG-15 completion without selecting successor work.

Validation:
- Use the selected docs-only profile plus:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Not required unless tests change in this slice.

Commit message:
- `Reconcile CCFG-11 split guard evidence`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep this to planning-evidence reconciliation; do not execute, regenerate, or
  amend CCFG-11 as active work.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope and active-state safety.
- Confirm CCFG-11 remains superseded evidence and CCFG-15 remains the queued
  batch until closeout.
- Echo the coordinator-provided `diff_basis` in compact YAML output.

Stop conditions:
- The change would turn CCFG-11 back into active, queued, or executable state.
- The change would select successor work during CCFG-15 closeout.
- The reconciliation reveals that CCFG-15 guidance or tests are incomplete;
  stop and route back to the affected earlier slice.

## Final Validation

- `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py -q`
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `git diff --check`

Diagnostic-only:
- `python -m pytest tests/test_codex_features_manifest.py -q` is currently a
  known-red baseline unless a CCFG-15 slice explicitly remediates the existing
  manifest contract drift.

## Stop Conditions

- Stop if work would execute, regenerate, or implement CCFG-11.
- Stop if reusable guidance would need project-specific paths, validation
  commands, cache locations, issue policies, or local planning layouts.
- Stop if vague-row guards would block precise bounded ledger rows.
- Stop if `planning_state.py current` or `validate` reports multiple active
  artifacts, stale queued state, or an active runway that conflicts with this
  queued batch.
