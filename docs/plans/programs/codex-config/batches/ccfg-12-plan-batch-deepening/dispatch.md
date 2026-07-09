# Plan-Batch Command-Owner Deepening Dispatch

```yaml
batch_id: ccfg-12-plan-batch-deepening
status: queued
source_program_ledger: docs/plans/programs/codex-config/LEDGER.md
included_findings:
  - id: CCFG-12
    title: Plan-batch command-owner deepening
excluded_findings:
  - id: CCFG-6
    title: Skill-slimmer support
    reason: Separate skill-cleanup candidate; this batch should deepen one existing command owner, not introduce a new support workflow.
  - id: CCFG-7
    title: Batch Runway hot-path pruning
    reason: Separate runtime-procedure cleanup; this batch must keep Batch Runway as runtime owner.
  - id: CCFG-8
    title: Ledger and dispatch rule dedupe
    reason: Related but broader dedupe work; this batch may clarify plan-batch routing without rewriting every ledger/dispatch rule.
  - id: CCFG-9
    title: Short skill frontmatter descriptions
    reason: Separate catalog cleanup; not needed to deepen the plan-batch command interface.
  - id: CCFG-10
    title: Skill steering vocabulary
    reason: Separate vocabulary cleanup; this batch may add only plan-batch-specific steering when needed.
  - id: CCFG-11
    title: Skill deletion tests
    reason: Broader audit; this batch uses focused deletion-test reasoning only for plan-batch.
goal: Make `plan-batch` a deeper human-facing command-owner interface for creating one bounded batch from existing ledger work while preserving `architecture-program-runway` and `batch-runway` as runtime owners behind it.
owner_seam: The external seam is the human "plan a batch/create the next specs batch" command. `plan-batch` owns the command contract and decision table; `architecture-program-runway` owns program selection, dispatch, queue state, and closeout reconciliation; `batch-runway` owns concrete runway spec mechanics.
validation_class: Skill/documentation contract updates with focused text regression tests, manifest dependency checks when touched, planning-state current/validate diagnostics, install dry-run when feature metadata changes, and git diff --check.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `planning_state.py current` reports this batch as the queued codex-config runway after this dispatch/runway pair is selected.
    - `plan-batch` exposes a deeper command contract without copying detailed runtime procedures from support skills.
    - `work-batch` remains the execution command for the queued runway.
source_evidence:
  - docs/plans/programs/codex-config/LEDGER.md
  - docs/plans/programs/codex-config/notes/command-owner-deepening-review.md
  - docs/skill-routing-contract.md
  - docs/workflow-guide.md
  - skills/plan-batch/SKILL.md
  - skills/architecture-program-runway/SKILL.md
  - skills/batch-runway/SKILL.md
required_guardrails:
  - Do not implement broad skill-system refactors.
  - Do not deepen `work-batch` in this batch.
  - Do not delete or demote `architecture-program-runway` or `batch-runway`.
  - Do not make `plan-batch` scan external sources for new work.
  - Do not create new ledger findings from fresh user text.
  - Do not introduce project-specific downstream paths, validation commands, cache locations, or local planning layouts into generic skills.
dependencies_satisfied:
  - Planning Artifact Layout v1 is active under `docs/plans/`.
  - CCFG-12 has a source review note and an active ledger row.
  - No selected dispatch, queued batch, or active runway existed before this batch was selected.
dependencies_blocking:
  - None for CCFG-12.
suggested_slices:
  - Add a compact plan-batch command contract section and decision table to `skills/plan-batch/SKILL.md`.
  - Add focused regression coverage proving `plan-batch` owns the human command while runtime owners remain dependencies.
  - Align routing docs, metadata, changelog, and planning closeout evidence only as needed.
stop_conditions:
  - The work would copy Batch Runway execution procedure into `plan-batch`.
  - The work would move Architecture Program Runway program-state ownership into `plan-batch`.
  - The work would broaden into all command-owner skills instead of CCFG-12.
  - The work would select or execute any other CCFG row.
expected_spec_path: docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/runway.md
```
