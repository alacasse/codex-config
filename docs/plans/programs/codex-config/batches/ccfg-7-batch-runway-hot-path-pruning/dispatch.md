# Batch Runway Hot-Path Pruning Dispatch

```yaml
batch_id: ccfg-7-batch-runway-hot-path-pruning
status: queued
source_program_ledger: docs/plans/programs/codex-config/LEDGER.md
included_findings:
  - id: CCFG-7
    title: Batch Runway hot-path pruning
excluded_findings:
  - id: CCFG-6
    title: Skill-slimmer support
    reason: Separate support-skill candidate; this batch only prunes the existing Batch Runway routine execution path.
  - id: CCFG-8
    title: Ledger and dispatch rule dedupe
    reason: Adjacent skill-boundary cleanup; this batch may remove Batch Runway duplication but must not rewrite planning/dispatch ownership across skills.
  - id: CCFG-9
    title: Short skill frontmatter descriptions
    reason: Catalog wording cleanup; not needed to reduce Batch Runway execution context load.
  - id: CCFG-10
    title: Skill steering vocabulary
    reason: Separate vocabulary cleanup; this batch may clarify Batch Runway routing terms only where it removes routine load.
  - id: CCFG-11
    title: Skill deletion tests
    reason: Broader audit; this batch should add only focused regression checks for Batch Runway hot-path load and semantics.
goal: Reduce routine Batch Runway execution/context load by pruning duplicated or non-routine guidance from the normal path while preserving current runtime semantics.
owner_seam: `batch-runway` owns concrete runway spec mechanics and execution orchestration. The hot path should keep routine execution on `SKILL.md`, `references/execute-slice-core-v1.md`, and one selected validation profile, loading recovery, finalization, reporting, subagent, or specialist guidance only when triggered.
validation_class: Docs and workflow-contract cleanup with focused text regression tests, planning-state current/validate diagnostics, and git diff checks.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `planning_state.py current` reports this batch as the queued codex-config runway after this dispatch/runway pair is selected.
    - Routine Batch Runway execution guidance is shorter or less duplicated.
    - Existing execution semantics remain intact: coordinator/worker/reviewer roles, per-slice validation/review/commit, recovery triggers, ledger retention, and finalization rules still point to the same owners.
source_evidence:
  - docs/plans/programs/codex-config/LEDGER.md
  - skills/batch-runway/SKILL.md
  - skills/batch-runway/references/execute-slice-core-v1.md
  - skills/batch-runway/references/execute-spec.md
  - skills/batch-runway/references/reporting-contracts-v1.md
  - skills/batch-runway/references/subagent-briefs.md
  - skills/batch-runway/references/ledger-retention-v1.md
  - skills/batch-runway/references/validation-profiles.md
required_guardrails:
  - Do not change runtime semantics or execution obligations.
  - Do not weaken coordinator-only implementation boundaries, worker non-delegation, reviewer separation, per-slice commits, validation, or recovery triggers.
  - Do not broaden into `plan-batch`, `work-batch`, `architecture-program-runway`, or planning-state dedupe except for references needed to keep Batch Runway links correct.
  - Do not add project-specific downstream paths, validation commands, cache locations, or local planning layouts to reusable skills.
  - Do not run nested Codex sessions or implement source code changes outside skill docs/tests.
dependencies_satisfied:
  - Planning Artifact Layout v1 is active under `docs/plans/`.
  - CCFG-7 exists in the canonical codex-config ledger.
  - No selected dispatch, queued batch, or active runway existed before this batch was selected.
dependencies_blocking:
  - None for CCFG-7.
suggested_slices:
  - Establish a small hot-path inventory and regression guard for the routine read contract.
  - Prune duplicated routine execution guidance from the Batch Runway entrypoint and execute-spec routing text.
  - Prune or relocate non-routine detail from `execute-slice-core-v1.md` while keeping trigger references explicit.
  - Align compact reporting/ledger references and closeout evidence only as needed.
stop_conditions:
  - The work would alter execution semantics instead of text/load shape.
  - The work would require changing runtime code, installer behavior, or downstream project validation.
  - The work would select or execute any other CCFG row.
  - The work cannot prove that the routine hot path remains discoverable after pruning.
expected_spec_path: docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/runway.md
```
