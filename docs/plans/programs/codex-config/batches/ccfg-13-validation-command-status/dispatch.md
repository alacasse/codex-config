# Validation Command Status Dispatch

```yaml
batch_id: ccfg-13-validation-command-status
status: queued
source_program_ledger: docs/plans/programs/codex-config/LEDGER.md
included_findings:
  - id: CCFG-13
    title: Validation command status classification
excluded_findings:
  - id: CCFG-2
    title: Branch-per-batch runner isolation mode
    reason: Runner workflow feature work; validation-command status classification is a Batch Runway create-spec contract fix.
  - id: CCFG-3
    title: Contract-drift review skill
    reason: Separate support-skill creation candidate; not needed to classify generated validation commands.
  - id: CCFG-4
    title: Runner adapter authoring skill
    reason: Separate adapter guidance candidate; not needed for the create-spec validation gate.
  - id: CCFG-5
    title: Baton dogfood diagnostics
    reason: Separate diagnostics feature set; this batch must not build new runner diagnostics.
  - id: CCFG-6
    title: Skill-slimmer support
    reason: Skill-cleanup backlog; keep separate from Batch Runway validation-contract work.
  - id: CCFG-9
    title: Short skill frontmatter descriptions
    reason: Catalog wording cleanup; not needed to fix validation-command status ambiguity.
  - id: CCFG-10
    title: Skill steering vocabulary
    reason: Separate vocabulary cleanup; not needed for validation-command status classes.
  - id: CCFG-11
    title: Skill deletion tests
    reason: Reopened and displaced from the active queue by explicit user request; CCFG-13 must handle the validation-gate root cause before CCFG-11 is planned or executed again.
goal: Add durable Batch Runway create-spec guidance and regression coverage so generated runway validation commands declare status classes before they become execution gates.
owner_seam: Batch Runway create-spec guidance owns validation-command status classification; concrete runways consume those classes when declaring focused validation gates.
validation_class: Docs and focused contract-test update with planning-state diagnostics, create-spec contract tests, and explicit known-red/future-created command handling.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `planning_state.py current` reports this CCFG-13 runway as the queued codex-config batch.
    - Batch Runway create-spec guidance requires a validation status class for each generated command.
    - Contract tests reject known-red and future-created commands being silently treated as required-green gates.
source_evidence:
  - docs/plans/programs/codex-config/LEDGER.md
  - docs/plans/programs/codex-config/findings/github-issue-29-validation-command-status.md
  - docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/runway.md
  - skills/batch-runway/references/create-spec.md
  - tests/test_batch_runway_create_spec_contract.py
current_command_evidence:
  - command: python scripts/planning_state.py current --root docs/plans
    status_class: required-green
    observed: passed during CCFG-13 planning
  - command: python scripts/planning_state.py validate --root docs/plans
    status_class: required-green
    observed: passed during CCFG-13 planning
  - command: python -m pytest tests/test_batch_runway_create_spec_contract.py -q
    status_class: required-green
    observed: passed during CCFG-13 planning
  - command: python -m pytest tests/test_codex_features_manifest.py -q
    status_class: known-red-baseline
    observed: 3 failures during CCFG-13 planning
  - command: python -m pytest tests/test_skill_deletion_surfaces.py -q
    status_class: implementation-created
    observed: file not found during CCFG-13 planning; this belongs to CCFG-11, not this batch
required_guardrails:
  - Do not execute the displaced CCFG-11 runway during this batch.
  - Do not fix CCFG-11 by deleting one failing validation command from its old runway.
  - Do not weaken validation globally; classify gates before execution instead.
  - Do not make known-red or missing future-created commands required-green without remediation or a named creating slice.
  - Keep reusable Batch Runway guidance project-neutral.
dependencies_satisfied:
  - Planning Artifact Layout v1 is active under `docs/plans/`.
  - CCFG-13 exists in the canonical codex-config ledger with source evidence.
  - The CCFG-11 queued runway exposes the ambiguous validation-gate examples.
dependencies_blocking:
  - None for CCFG-13 planning.
suggested_slices:
  - Add validation-command status classes to Batch Runway create-spec guidance.
  - Add focused contract tests for required-green, known-red-baseline, implementation-created, conditional, and diagnostic-only command handling.
  - Reconcile the displaced CCFG-11 validation-gate evidence so future CCFG-11 planning cannot reuse unclassified gates.
stop_conditions:
  - The work would execute CCFG-11 or treat its old runway as still queued.
  - The work would require project-specific downstream validation commands in reusable Batch Runway guidance.
  - The work cannot preserve a current-green path for create-spec contract tests.
expected_spec_path: docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md
```
