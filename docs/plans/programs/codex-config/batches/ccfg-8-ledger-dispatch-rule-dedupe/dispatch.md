# Ledger Dispatch Rule Dedupe Dispatch

```yaml
batch_id: ccfg-8-ledger-dispatch-rule-dedupe
status: queued
source_program_ledger: docs/plans/programs/codex-config/LEDGER.md
included_findings:
  - id: CCFG-8
    title: Ledger and dispatch rule dedupe
excluded_findings:
  - id: CCFG-2
    title: Branch-per-batch runner isolation mode
    reason: Runner workflow work depends on the runner boundary and is not part of skill-maintainability dedupe.
  - id: CCFG-3
    title: Contract-drift review skill
    reason: Separate runner support-skill candidate; this batch changes no runner extraction contracts.
  - id: CCFG-4
    title: Runner adapter authoring skill
    reason: Separate runner support-skill candidate.
  - id: CCFG-5
    title: Baton dogfood diagnostics
    reason: Separate runner diagnostics candidate.
  - id: CCFG-6
    title: Skill-slimmer support
    reason: Adjacent cleanup backlog, but this batch deduplicates existing rules rather than creating a new slimming workflow.
  - id: CCFG-7
    title: Batch Runway hot-path pruning
    reason: Completed; closeout evidence only.
  - id: CCFG-9
    title: Short skill frontmatter descriptions
    reason: Separate catalog cleanup; do not combine with ownership-rule dedupe.
  - id: CCFG-10
    title: Skill steering vocabulary
    reason: Separate vocabulary cleanup; this batch may only adjust wording needed for rule ownership.
  - id: CCFG-11
    title: Skill deletion tests
    reason: Separate audit; this batch may add focused ownership-boundary tests only.
  - id: CCFG-12
    title: Plan-batch command-owner deepening
    reason: Completed; closeout evidence only.
goal: Reduce facade-like skill layering and duplicated routing rules across ledger, dispatch, active-state, closeout, and external-source guidance without changing runtime behavior.
owner_seam: Command-owner skills own human-facing routing decisions and stop points. Runtime/support skills own procedures and mechanics. This batch assigns repeated rules to one owner, then replaces safe duplicates with short references.
validation_class: Skill-maintainability docs and focused text-contract tests, with planning-state current/validate diagnostics and git diff checks. No integration harness or runtime behavior validation is required unless tests reveal a behavior-facing contract change.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `planning_state.py current` reports this runway as the queued codex-config batch after dispatch/runway creation.
    - Command-owner skills still own user intent and stopping decisions.
    - Runtime/support skills still own procedures, mechanics, active-state diagnostics, artifact layout, program queue mechanics, concrete runway execution, and closeout reconciliation.
source_evidence:
  - docs/plans/programs/codex-config/LEDGER.md
  - skills/add-to-ledger/SKILL.md
  - skills/plan-batch/SKILL.md
  - skills/work-batch/SKILL.md
  - skills/architecture-program-runway/SKILL.md
  - skills/batch-runway/SKILL.md
  - skills/planning-state/SKILL.md
  - skills/planning-artifacts/SKILL.md
  - docs/skill-routing-contract.md
  - docs/workflow-guide.md
required_guardrails:
  - Do not touch CCFG-1 runner extraction work.
  - Do not select CCFG-2 through CCFG-5.
  - Do not implement Go runner work.
  - Do not create a new command-owner skill.
  - Do not rewrite all skills.
  - Do not change runtime behavior.
  - Do not reconcile current program data beyond this batch's selected/queued planning state and eventual same-batch closeout.
  - Do not add project-specific downstream paths, validation commands, cache locations, or local planning layouts to generic skills.
  - Do not delete necessary command-owner rules merely because similar wording exists in support skills.
dependencies_satisfied:
  - Planning Artifact Layout v1 is active under `docs/plans/`.
  - CCFG-8 exists in the canonical codex-config ledger.
  - CCFG-1 has been closed and live state has no selected, queued, or active batch before this selection.
  - CCFG-12 clarified the `plan-batch` command-owner contract, which this batch can preserve while deduplicating overlapping support wording.
dependencies_blocking:
  - None for the planning-only dedupe batch.
suggested_slices:
  - Inventory repeated ledger, dispatch, selected/queued/active, closeout, and external-source rules across the named skill and docs surfaces; assign one owner for each repeated rule.
  - Replace safe duplicate command-owner and docs prose with short references while preserving user-facing routing decisions.
  - Replace safe duplicate runtime/support prose with references to the owning support skill where mechanics are already centralized.
  - Add or adjust focused tests that protect the ownership map and prevent future facade-like duplication.
closeout_gates:
  - A compact owner map exists in the implementation diff, tests, or closeout evidence.
  - Duplicated prose is reduced on the targeted surfaces where safe.
  - Tests fail if command-owner skills lose human-facing routing ownership or if runtime/support skills lose procedure/mechanics ownership.
  - Planning-state current/validate diagnostics pass after closeout.
stop_conditions:
  - The worker would need to redesign the command-owner architecture instead of assigning ownership for repeated existing rules.
  - The work would require changing `scripts/planning_state.py` behavior, runner behavior, Batch Runway execution semantics, or install/runtime behavior.
  - The work would require selecting CCFG-2 through CCFG-5, CCFG-6, CCFG-9, CCFG-10, or CCFG-11.
  - The work cannot identify a single owner for a repeated rule without a user decision.
expected_spec_path: docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/runway.md
```
