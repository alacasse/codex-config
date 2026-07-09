# Batch Kind And Destructive-Slice Risk Gates Dispatch

```yaml
batch_id: ccfg-14-batch-kind-slice-risk
status: queued
source_program_ledger: docs/plans/programs/codex-config/LEDGER.md
included_findings:
  - id: CCFG-14
    title: Batch kind and destructive-slice risk gates
excluded_findings:
  - id: CCFG-2
    title: Branch-per-batch runner isolation mode
    reason: Runner workflow feature work; not needed for Batch Runway create-spec risk metadata.
  - id: CCFG-3
    title: Contract-drift review skill
    reason: Separate support-skill creation candidate; not needed for generated runway batch-kind gates.
  - id: CCFG-4
    title: Runner adapter authoring skill
    reason: Separate adapter guidance candidate; not needed for create-spec risk classification.
  - id: CCFG-5
    title: Baton dogfood diagnostics
    reason: Separate diagnostics feature set; this batch must not build new runner diagnostics.
  - id: CCFG-6
    title: Skill-slimmer support
    reason: Skill-cleanup backlog; keep separate from Batch Runway metadata and approval-gate work.
  - id: CCFG-9
    title: Short skill frontmatter descriptions
    reason: Catalog wording cleanup; not needed to fix destructive-slice risk gates.
  - id: CCFG-10
    title: Skill steering vocabulary
    reason: Separate vocabulary cleanup; not needed for batch-kind or risk-class metadata.
  - id: CCFG-11
    title: Skill deletion tests
    reason: Visible symptom and future consumer of this fix; do not regenerate or execute CCFG-11 until CCFG-14 closes.
goal: Add durable Batch Runway create-spec guidance and regression coverage so generated dispatch/runway artifacts declare batch kind, classify risky slices, and gate destructive or contract-narrowing work before execution.
owner_seam: Batch Runway create-spec guidance owns portable batch-kind, slice-risk, and approval-gate semantics; concrete dispatch/runway artifacts consume those fields.
validation_class: Reusable workflow guidance plus focused contract tests, with planning-state diagnostics and no project-level integration harness.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - Batch Runway create-spec guidance requires generated artifacts to declare batch kind.
    - Generated slices that can delete, narrow, demote, migrate, or otherwise contract a surface declare a risk class.
    - Evidence-only or characterization batches cannot carry destructive cleanup slices unless explicitly mixed-risk and approval-gated.
source_evidence:
  - docs/plans/programs/codex-config/LEDGER.md
  - docs/plans/programs/codex-config/findings/github-issue-30-batch-kind-slice-risk.md
  - docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/runway.md
  - skills/batch-runway/references/create-spec.md
  - tests/test_batch_runway_create_spec_contract.py
current_command_evidence:
  - command: python scripts/planning_state.py current --root docs/plans
    status_class: required-green
    observed: passed during CCFG-14 planning
  - command: python scripts/planning_state.py validate --root docs/plans
    status_class: required-green
    observed: passed during CCFG-14 planning
  - command: python -m pytest tests/test_batch_runway_create_spec_contract.py -q
    status_class: required-green
    observed: passed during CCFG-14 planning
  - command: python -m pytest tests/test_codex_features_manifest.py -q
    status_class: known-red-baseline
    observed: known red from CCFG-13 planning evidence; not a CCFG-14 gate unless a slice explicitly remediates it
  - command: git diff --check
    status_class: required-green
    observed: passed during CCFG-14 planning
required_guardrails:
  - Do not execute the displaced CCFG-11 runway during this batch.
  - Do not fix the issue only by removing or rewriting CCFG-11 Slice 3.
  - Do not make reusable Batch Runway guidance codex-config-specific.
  - Do not allow evidence-only or characterization batches to include destructive cleanup slices without explicit mixed-risk metadata and approval gates.
dependencies_satisfied:
  - Planning Artifact Layout v1 is active under `docs/plans/`.
  - CCFG-14 exists in the canonical codex-config ledger with source evidence.
  - CCFG-13 already added validation-command status classification, so this batch can build on the create-spec contract tests.
dependencies_blocking:
  - None for CCFG-14 planning.
suggested_slices:
  - Add portable batch-kind, slice-risk, and approval-gate semantics to Batch Runway create-spec guidance.
  - Add focused contract tests that reject destructive cleanup slices in evidence-only batches without mixed-risk metadata and approval gates.
  - Reconcile CCFG-11 planning evidence so future CCFG-11 regeneration must use the new metadata instead of reviving the displaced runway.
stop_conditions:
  - Work would execute, regenerate, or amend CCFG-11 as implementation work before CCFG-14 closes.
  - Work would add project-specific paths, validation commands, or local planning layouts to reusable Batch Runway guidance.
  - Contract tests cannot express the batch-kind and destructive-slice gate without broad runner or workflow rewrites.
expected_spec_path: docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/runway.md
```
