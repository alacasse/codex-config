# Vague Ledger Row Splitting Dispatch

```yaml
batch_id: ccfg-15-vague-ledger-row-splitting
status: queued
batch_kind: mixed-risk
mixed_risk_reason: Guidance work narrows the planning contract for vague or mixed-risk ledger rows before selected dispatch and runway creation; tests and planning evidence are non-destructive.
risky_slices:
  - slice: 1
    risk_class: contract-narrowing
    approval_gate: The CCFG-15 ledger row and this dispatch authorize narrowing `plan-batch` / `architecture-program-runway` behavior only for vague or mixed-risk row expansion. Stop for user approval if execution would block precise bounded rows, change runner execution semantics, or add project-specific planning rules.
source_program_ledger: docs/plans/programs/codex-config/LEDGER.md
included_findings:
  - id: CCFG-15
    title: Vague ledger row splitting before runway expansion
excluded_findings:
  - id: CCFG-2
    title: Branch-per-batch runner isolation mode
    reason: Runner workflow feature work; not needed for vague-row planning guards.
  - id: CCFG-3
    title: Contract-drift review skill
    reason: Separate support-skill creation candidate; not needed for selected-dispatch row splitting.
  - id: CCFG-4
    title: Runner adapter authoring skill
    reason: Separate adapter guidance candidate; not needed for program-runway planning guards.
  - id: CCFG-5
    title: Baton dogfood diagnostics
    reason: Separate diagnostics feature set; this batch must not build runner diagnostics.
  - id: CCFG-6
    title: Skill-slimmer support
    reason: Skill-cleanup backlog; keep separate from generic vague-row planning guards.
  - id: CCFG-9
    title: Short skill frontmatter descriptions
    reason: Catalog wording cleanup; not needed for row-splitting behavior.
  - id: CCFG-10
    title: Skill steering vocabulary
    reason: Separate vocabulary cleanup; not needed for vague-row split/block/narrow rules.
  - id: CCFG-11
    title: Skill deletion tests
    reason: Visible CCFG-15 fixture and future consumer only; do not execute or regenerate CCFG-11 from its displaced runway during this batch.
goal: Add durable `plan-batch` / `architecture-program-runway` guidance and focused tests so vague or mixed-risk ledger rows are split, blocked, or narrowed before selected dispatch and concrete runway creation.
owner_seam: `plan-batch` owns the human command and ledger-source decision; `architecture-program-runway` owns bounded program selection, selected dispatch shaping, and split/block/narrow rationale before `batch-runway create-spec` consumes a dispatch.
validation_class: Reusable workflow guidance plus focused text-contract tests, planning-state diagnostics, and no project-level integration harness.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - A CCFG-11-like vague deletion-test row cannot expand directly into a mixed evidence, decision, and destructive-cleanup runway.
    - Selected dispatches created from vague or mixed-risk rows record split, block, or narrow-scope rationale before `runway.md` exists.
    - Destructive cleanup, migration, demotion, or contract-narrowing discoveries during planning become explicit follow-up findings unless the source row already authorizes that risk.
source_evidence:
  - docs/plans/programs/codex-config/LEDGER.md
  - docs/plans/programs/codex-config/findings/github-issue-33-vague-ledger-row-splitting.md
  - docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/dispatch.md
  - docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/runway.md
  - docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/closeout.md
  - skills/plan-batch/SKILL.md
  - skills/architecture-program-runway/SKILL.md
  - tests/test_skill_routing_rule_ownership.py
  - tests/test_architecture_program_runway_status_vocabulary.py
current_command_evidence:
  - command: python scripts/planning_state.py current --root docs/plans
    status_class: required-green
    observed: passed during CCFG-15 planning
  - command: python scripts/planning_state.py validate --root docs/plans
    status_class: required-green
    observed: passed during CCFG-15 planning
  - command: python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py -q
    status_class: required-green
    observed: 7 passed during CCFG-15 planning
  - command: python -m pytest tests/test_batch_runway_create_spec_contract.py -q
    status_class: required-green
    observed: 13 passed during CCFG-15 planning
  - command: python -m pytest tests/test_codex_features_manifest.py -q
    status_class: known-red-baseline
    observed: 3 failures during CCFG-15 planning; diagnostic only unless a slice explicitly remediates existing manifest contract drift
  - command: git diff --check
    status_class: required-green
    observed: passed after CCFG-15 planning artifact creation
required_guardrails:
  - Do not execute, regenerate, or amend CCFG-11 as implementation work during this batch.
  - Do not fix the issue only by editing the displaced CCFG-11 runway.
  - Keep reusable `plan-batch` and `architecture-program-runway` guidance project-neutral.
  - Do not add project-specific paths, validation commands, cache locations, issue policies, or local planning layouts to generic skills.
  - Do not let vague rows that mention deletion, demotion, migration, cleanup, or narrowing expand directly into mixed-risk implementation runways.
  - Do not create fresh ledger findings from source text during `plan-batch`; if follow-up findings are required, route through the ledger workflow.
dependencies_satisfied:
  - Planning Artifact Layout v1 is active under `docs/plans/`.
  - CCFG-15 exists in the canonical codex-config ledger with source evidence.
  - CCFG-13 and CCFG-14 are complete and provide validation-command status, batch-kind, slice-risk, and approval-gate prerequisites.
  - No selected dispatch, queued batch, or active runway existed before this batch was selected.
dependencies_blocking:
  - None for CCFG-15 planning.
suggested_slices:
  - Add split/block/narrow rules to `plan-batch` and `architecture-program-runway` before selected dispatch creation.
  - Add focused contract tests that prove CCFG-11-like vague rows cannot produce mixed-risk runways without prior split, block, or narrow rationale.
  - Reconcile CCFG-11 planning evidence and CHANGELOG/closeout notes so future CCFG-11 planning uses the new guard instead of the displaced runway.
stop_conditions:
  - The work would execute, regenerate, or implement CCFG-11.
  - The work would require broad runner rewrites, a new planner engine, or project-specific downstream behavior in reusable skills.
  - The guard cannot be expressed without making precise bounded ledger rows impossible to select.
  - Focused tests cannot prove the split/block/narrow behavior without brittle snapshots of whole skill files.
expected_spec_path: docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/runway.md
```
