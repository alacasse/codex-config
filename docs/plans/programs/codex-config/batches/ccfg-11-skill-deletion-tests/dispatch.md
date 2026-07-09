# Skill Deletion Tests Dispatch

```yaml
batch_id: ccfg-11-skill-deletion-tests
status: superseded
source_program_ledger: docs/plans/programs/codex-config/LEDGER.md
included_findings:
  - id: CCFG-11
    title: Skill deletion tests
excluded_findings:
  - id: CCFG-2
    title: Branch-per-batch runner isolation mode
    reason: Runner workflow feature work; this batch is skill cleanup evidence only.
  - id: CCFG-3
    title: Contract-drift review skill
    reason: Separate support-skill creation candidate; deletion evidence should not create new runner review skills.
  - id: CCFG-4
    title: Runner adapter authoring skill
    reason: Separate adapter guidance candidate; not needed for deletion-test audit.
  - id: CCFG-5
    title: Baton dogfood diagnostics
    reason: Separate diagnostics feature set; this batch must not build new runner diagnostics.
  - id: CCFG-6
    title: Skill-slimmer support
    reason: Related but broader workflow candidate; deletion evidence should be produced before deciding whether another support skill is needed.
  - id: CCFG-9
    title: Short skill frontmatter descriptions
    reason: Catalog wording cleanup; not needed to prove no-op, sediment, or obsolete skill surfaces.
  - id: CCFG-10
    title: Skill steering vocabulary
    reason: Separate vocabulary cleanup; this batch may note steering gaps only as evidence for deletion-test decisions.
goal: Produce focused, test-backed deletion evidence for no-op, sediment, and obsolete skill surfaces without deleting or demoting any skill unless the evidence and tests support that exact action.
owner_seam: `dead-surface-audit` owns evidence classification for apparently live surfaces; `legacy-removal` owns exceptional obsolete-surface scoping; command-owner skills own human-facing workflow commands; installed skill metadata owns direct invocation and dependency visibility.
validation_class: Skill/test audit with focused pytest coverage, docs-only planning updates, planning-state current/validate diagnostics, manifest/install checks when metadata changes, and git diff checks.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `planning_state.py current` reports this batch as the queued codex-config runway after this dispatch/runway pair is selected.
    - Focused tests or fixtures distinguish no-op skills, sediment surfaces, obsolete internals, support-only skills, and necessary command-owner entrypoints.
    - Closeout for CCFG-11 records deletion-test evidence even if the right outcome is "keep with justification" rather than deletion.
source_evidence:
  - docs/plans/programs/codex-config/LEDGER.md
  - docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md#L75
  - skills/dead-surface-audit/SKILL.md
  - skills/legacy-removal/SKILL.md
  - docs/plans/programs/codex-config/notes/command-owner-deepening-review.md
  - docs/skill-routing-contract.md
required_guardrails:
  - Do not delete, demote, or rename skills during spec creation.
  - Do not delete runtime/support skills merely because a command-owner skill exists.
  - Do not preserve obsolete surfaces only because tests assert imports, aliases, topology, or compatibility shape.
  - Do not add project-specific downstream paths, validation commands, cache locations, or local planning layouts to generic skills.
  - Do not revive archived APR/PST ledgers as active pickup sources; use the archived PST row only as CCFG-11 source evidence.
  - Do not select or execute any other CCFG row.
dependencies_satisfied:
  - Planning Artifact Layout v1 is active under `docs/plans/`.
  - CCFG-11 exists in the canonical codex-config ledger.
  - No selected dispatch, queued batch, or active runway existed before this batch was selected.
  - `dead-surface-audit` and `legacy-removal` already provide narrow evidence vocabulary that this batch can test against.
dependencies_blocking:
  - CCFG-13 must handle validation-command status classification before this
    batch is planned or executed again.
  - CCFG-14 must handle batch-kind and destructive-slice risk gates before this
    batch is planned or executed again.
supersession:
  replacement_batch: ccfg-13-validation-command-status
  replacement_dispatch: docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/dispatch.md
  replacement_spec: docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md
  reason: The original CCFG-11 runway listed known-red and implementation-created validation commands without status classes.
risk_gate_supersession:
  status: blocked-before-future-execution
  prerequisite_batch: ccfg-14-batch-kind-slice-risk
  required_before_execution:
    - declare one batch kind for the regenerated or amended CCFG-11 batch
    - declare a risk class for every slice that could migrate, narrow, demote, or delete a skill surface
    - include explicit approval gates before destructive-cleanup or contract-narrowing slices execute
  note: This displaced dispatch remains superseded planning evidence and is not active queue state.
suggested_slices:
  - Add a focused deletion-test inventory over installed/user-facing/support skill metadata and existing evidence vocabulary.
  - Add regression coverage that classifies command-owner, support-only, no-op, sediment, and obsolete-surface cases without broad Markdown snapshots.
  - Apply the evidence to one narrow skill-surface cleanup decision, or record "keep with justification" where deletion is unsafe.
  - Align docs, changelog, ledger state, and closeout evidence only as needed.
stop_conditions:
  - The work would delete or demote a human-facing command-owner skill without explicit user approval and focused test evidence.
  - The work would require broad skill-system redesign instead of deletion-test evidence.
  - The work would turn archived PST issue #27 into an active ledger source instead of evidence for CCFG-11.
  - The work cannot name the observable contract a candidate skill or surface still satisfies.
expected_spec_path: docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/runway.md
```
