# Batch Kind And Destructive-Slice Risk Gates Runway

## Purpose

Add durable Batch Runway create-spec guidance and focused regression coverage so
generated dispatch/runway artifacts declare batch kind, classify risky slices,
and gate destructive or contract-narrowing work before execution.

This spec executes the `ccfg-14-batch-kind-slice-risk` batch described by
`docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/dispatch.md`.
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
  `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/dispatch.md`.
- Included finding: CCFG-14.
- CCFG-13 is complete and already requires validation-command status classes in
  Batch Runway create-spec guidance.
- CCFG-11 remains open, but its displaced dispatch/runway pair is superseded
  planning evidence and must not be executed as active state.

## Batch Kind And Risk Metadata

Generated dispatch/runway artifacts should declare one batch kind before
execution. Initial portable kinds for this batch to define are:

- `characterization`: evidence collection or test characterization without
  cleanup, deletion, narrowing, or migration.
- `decision`: evaluates keep/remove/migrate outcomes and records a decision, but
  does not perform destructive cleanup in the same slice unless mixed-risk gates
  are present.
- `migration`: moves or rewires behavior while preserving the supported public
  contract.
- `destructive-cleanup`: deletes, narrows, demotes, or intentionally removes an
  existing surface.
- `mixed-risk`: combines evidence, decision, migration, or destructive cleanup
  work and therefore must name the risky slices and their approval gates.

Generated slices should declare a risk class when the slice could delete,
narrow, demote, migrate, or otherwise contract an existing surface. Initial
portable risk classes for this batch to define are:

- `none`: no deletion, narrowing, migration, or contract change.
- `evidence-only`: gathers evidence without changing supported surfaces.
- `decision-only`: records a keep/remove/migrate decision without performing
  destructive cleanup.
- `migration`: changes topology or ownership while preserving supported
  behavior.
- `contract-narrowing`: removes or narrows an exposed or depended-on surface.
- `destructive-cleanup`: deletes, disables, or demotes an existing surface.

Destructive or contract-narrowing slices require an explicit approval gate
before execution. Evidence-only or characterization batches must not include
destructive cleanup slices unless the artifact is explicitly `mixed-risk` and
names the gate.

## Assumptions

- This is a create-spec contract fix, not execution of CCFG-11.
- The reusable guidance should define portable metadata and gate semantics, not
  codex-config-specific examples.
- Existing create-spec contract tests are the narrowest regression home unless
  execution finds a more precise owner.
- The CCFG-11 displaced runway is useful evidence, but future CCFG-11 work must
  be regenerated or amended after this batch closes.

## Non-Goals

- Do not implement any slice during spec creation.
- Do not execute, regenerate, or implement CCFG-11.
- Do not fix this only by removing or rewriting CCFG-11 Slice 3.
- Do not add downstream-project paths, commands, cache locations, or local
  planning layouts to reusable Batch Runway guidance.
- Do not create a broad workflow-runner taxonomy outside Batch Runway
  create-spec metadata.

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
- Use `lean-runway` density because this batch changes reusable workflow
  guidance, focused contract tests, and planning reconciliation only.
- Workers must preserve project-neutral Batch Runway guidance; repository-local
  examples belong in tests, fixtures, or this planning batch only.
- Destructive or contract-narrowing changes are not allowed in this batch except
  for documentation updates to the displaced CCFG-11 planning evidence.

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
- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  - status: `required-green`
  - scope: Batch Runway create-spec contract guidance and tests
- `python -m pytest tests/test_codex_features_manifest.py -q`
  - status: `known-red-baseline`
  - scope: diagnostic only unless a slice explicitly remediates existing
    manifest failures
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
| 1. Define Batch Kind And Slice Risk Contract | Pending |  |  |  | Focused contract guidance and planning-state diagnostics |  |
| 2. Test Destructive-Slice Gates | Pending |  |  |  | Focused create-spec contract tests and planning-state diagnostics |  |
| 3. Reconcile CCFG-11 Risk Evidence | Pending |  |  |  | Planning-state diagnostics and `git diff --check` |  |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|

## Slice 1. Define Batch Kind And Slice Risk Contract

Scope:
- Update Batch Runway create-spec guidance so generated artifacts declare a
  batch kind.
- Define portable slice risk classes for evidence-only, decision-only,
  migration, contract-narrowing, and destructive-cleanup work.
- Require explicit approval gates for destructive or contract-narrowing slices.

Allowed files/areas:
- `skills/batch-runway/references/create-spec.md`
- `skills/batch-runway/SKILL.md` only if create-spec entrypoint wording needs a
  short pointer to the new contract.
- `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/`

Non-goals:
- Do not edit CCFG-11 artifacts in this slice.
- Do not change execution semantics outside create-spec output requirements.
- Do not add codex-config-specific command examples to reusable guidance.

Acceptance criteria:
- Create-spec guidance requires generated artifacts to declare one batch kind.
- Create-spec guidance requires risky slices to declare a risk class.
- Destructive or contract-narrowing slices require an explicit approval gate
  before execution.
- Evidence-only or characterization batches cannot include destructive cleanup
  slices unless the artifact is explicitly mixed-risk and approval-gated.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Not required unless tests change in this slice.

Commit message:
- `Define batch kind risk gates`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep reusable Batch Runway guidance project-neutral.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope and guidance clarity.
- Confirm the guidance requires batch kind, slice risk class, and approval gates
  without adding project-specific examples.
- Echo the coordinator-provided `diff_basis` in compact YAML output.

Stop conditions:
- The guidance cannot express portable risk semantics without a broader runner
  rewrite.
- The change weakens validation-command status classes from CCFG-13.

## Slice 2. Test Destructive-Slice Gates

Scope:
- Add focused contract tests proving create-spec guidance requires batch kind,
  risk class, and approval-gate semantics.
- Test that evidence-only or characterization batches cannot include
  destructive cleanup slices without mixed-risk metadata and approval gates.
- Keep tests local to reusable Batch Runway create-spec contract guidance.

Allowed files/areas:
- `tests/test_batch_runway_create_spec_contract.py`
- `skills/batch-runway/references/create-spec.md` only for wording adjustments
  needed to satisfy precise contract tests.
- `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/`

Non-goals:
- Do not create CCFG-11 deletion-surface tests.
- Do not touch manifest ownership or command-owner manifest tests.
- Do not add broad parsing infrastructure unless the existing text-contract
  style cannot express the required gate.

Acceptance criteria:
- Contract tests assert the generated-spec checklist requires batch kind.
- Contract tests assert destructive, contract-narrowing, migration, and
  decision/evidence risk classes are named.
- Contract tests assert destructive cleanup in an evidence-only or
  characterization batch requires explicit mixed-risk metadata and an approval
  gate.
- Existing validation-command status contract tests remain green.

Validation:
- Use the selected docs-only profile plus:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Required because this slice changes contract tests. Ask the reviewer to check
  that assertions protect behavior and are not brittle wording trivia.

Commit message:
- `Test destructive slice gates`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Preserve the existing text-contract test style unless a small helper reduces
  real duplication.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, including test quality.
- Confirm the tests fail for missing batch kind, risk class, or destructive
  approval-gate guidance.
- Echo the coordinator-provided `diff_basis` in compact YAML output.

Stop conditions:
- Tests require a broad parser or fixture format change outside the focused
  create-spec contract test module.
- The new tests couple reusable guidance to codex-config-specific paths or
  commands.

## Slice 3. Reconcile CCFG-11 Risk Evidence

Scope:
- Amend displaced CCFG-11 planning evidence only enough to record that future
  CCFG-11 planning must declare batch kind, slice risk classes, and approval
  gates before execution.
- Keep CCFG-11 open in the program ledger.
- Update this spec ledger/archive for Slice 3 execution evidence.

Allowed files/areas:
- `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/`
- `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/`

Non-goals:
- Do not execute or regenerate CCFG-11.
- Do not change reusable Batch Runway guidance or tests in this slice except
  for emergency correction of a Slice 1 or Slice 2 regression.
- Do not remove the displaced CCFG-11 planning evidence.

Acceptance criteria:
- The displaced CCFG-11 artifact remains clearly superseded planning evidence,
  not active queue state.
- Future CCFG-11 execution is blocked unless a regenerated or amended runway
  includes batch kind, slice risk classes, and required approval gates.
- Program state still points to CCFG-14 as the queued batch until closeout.

Validation:
- Use the selected docs-only profile plus:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Not required unless tests change in this slice.

Commit message:
- `Reconcile CCFG-11 risk evidence`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- Keep this to planning-evidence reconciliation; do not execute or regenerate
  CCFG-11.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope and active-state safety.
- Confirm CCFG-11 remains superseded evidence and CCFG-14 remains the queued
  batch.
- Echo the coordinator-provided `diff_basis` in compact YAML output.

Stop conditions:
- The change would turn CCFG-11 back into active, queued, or executable state.
- The reconciliation reveals that CCFG-14's reusable guidance or tests are
  incomplete; stop and route back to the affected earlier slice.

## Final Validation

- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `git diff --check`

## Stop Conditions

- Stop if work would execute, regenerate, or implement CCFG-11 before CCFG-14
  closes.
- Stop if reusable guidance would need project-specific paths, validation
  commands, cache locations, or local planning layouts.
- Stop if destructive or contract-narrowing execution work appears in this
  batch beyond planning-evidence documentation.
- Stop if `planning_state.py current` or `validate` reports multiple active
  artifacts, stale queued state, or an active runway that conflicts with this
  queued batch.
