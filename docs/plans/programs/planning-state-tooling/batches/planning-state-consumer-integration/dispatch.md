# Planning-State Consumer Integration Dispatch

```yaml
batch_id: planning-state-consumer-integration
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-12
    title: Ledger-dependent skills duplicate active-state pickup and projection setup
  - id: PST-13
    title: Feature dependency metadata cannot express operational planning-state reuse
excluded_findings:
  - id: none
    reason: This is the remaining planning-state-tooling candidate batch.
goal: Wire ledger-dependent consumer skills to the shared `planning-state` skill interface before they make Layout v1 pickup, target-policy, projection, or closeout decisions, then align install-time feature dependencies.
owner_seam: The shared operational seam is `skills/planning-state/SKILL.md` plus `python scripts/planning_state.py ...`; consumer skills keep their own semantic decisions after consuming compact Planning State Diagnostic facts.
validation_class: skill wording checks, dependency-manifest JSON and focused tests, current/validate diagnostics, no downstream project writes, and `git diff --check`.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `python scripts/planning_state.py current --root docs/plans` and `validate --root docs/plans` remain the first operational diagnostics.
    - This dispatch/runway pair is treated as the queued planning-state batch until execution closes it.
    - State/projection policy remains generated-only; no committed JSON state or SQLite projection is created.
consumer_contract:
  - `batch-runway` uses Planning State Diagnostic facts before consuming Layout v1 active-state files for create-spec, execute-spec pickup, or queued-batch checks.
  - `architecture-program-runway` uses Planning State Diagnostic facts at the start of active-state pickup, then preserves its responsibility for program selection, grouping, queue state, dispatch packets, and closeout reconciliation.
  - `legacy-removal` uses Planning State Diagnostic facts before creating or consuming Layout v1 ledgers and dispatch packets, while preserving legacy classification and evidence decisions inside the legacy-removal skill.
  - Consumer skills may still read `planning-artifacts` for placement rules, but they should not duplicate the operational current/validate, target-policy, projection, or closeout setup that `planning-state` owns.
dependency_contract:
  - Add `planning-state` as a feature dependency for consumer features that now invoke the shared diagnostic interface.
  - Keep `planning-artifacts` dependencies where layout placement is still consumed directly.
  - Keep `planning-state` dependent on `planning-artifacts`, not the other way around.
guardrails:
  - Do not change `scripts/planning_state.py` command semantics unless a tiny test hook is required for dependency or wording validation.
  - Do not add project-specific downstream paths, validation commands, cache paths, or local overlays to reusable consumer skills.
  - Do not create committed durable JSON state, SQLite projection files, runner receipts, or generated reports.
  - Do not write to downstream project planning roots.
  - Do not update GitHub issues or comments as part of this planning batch.
dependencies_satisfied:
  - `planning-state-skill-interface` created the shared operational skill and references.
  - `planning-state` is installable through `codex-features.json`.
  - Current planning-state diagnostics validate this program with no blockers.
dependencies_blocking:
  - None for consumer integration.
suggested_slices:
  - Wire `batch-runway` to the planning-state diagnostic handoff.
  - Wire `architecture-program-runway` to the planning-state diagnostic handoff.
  - Wire `legacy-removal` to the planning-state diagnostic handoff.
  - Align feature dependency metadata, changelog/tests, and close PST-12/PST-13.
stop_conditions:
  - The batch would need a universal durable JSON state or SQLite projection path.
  - The batch would need downstream project-specific paths or validation commands in generic skill text.
  - The batch would need to make SQLite or JSON state canonical over Markdown planning artifacts.
  - The batch would need to remove consumer-owned semantic decisions instead of only centralizing operational planning-state setup.
  - The batch would need to modify downstream project planning roots.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/runway.md
```
