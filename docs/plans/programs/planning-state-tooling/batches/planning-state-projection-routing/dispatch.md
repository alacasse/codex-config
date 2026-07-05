# Planning-State Projection Routing Dispatch

```yaml
batch_id: planning-state-projection-routing
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-14
    title: Projection routing is implemented but not part of the routine interface
  - id: PST-15
    title: Projection target policy does not express expected projection usage
excluded_findings:
  - id: PST-16
    reason: Consumer skill rewiring should follow after the planning-state interface and policy vocabulary are explicit.
  - id: PST-17
    reason: Consumer-facing regression checks belong with the consumer rewiring batch.
goal: Make the Planning State Diagnostic projection-aware for history/reporting questions and add explicit project-policy vocabulary for projection usage and rebuild authority, without making SQLite canonical active state.
owner_seam: `skills/planning-state/SKILL.md` owns the routine agent interface; `scripts/planning_state.py` owns project-policy parsing, validation, projection rebuild/report commands, and machine-readable diagnostic facts.
validation_class: planning-state skill/reference checks, project-policy parsing tests, current/validate/projection CLI smoke tests against generated-only and ignored-local fixtures, and `git diff --check`.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `current` and `validate` remain SQLite-independent active-state checks.
    - Project policy remains generated-only for this repo unless explicit fixture state says otherwise.
    - This dispatch/runway pair is treated as the queued planning-state batch until execution closes it.
secondary_fixture:
  project: policy-compatible temp Layout v1 roots
  expected_resolution:
    - One generated-only fixture proves projection reports are advisory and require explicit temp targets.
    - One ignored-local fixture proves projection usage and rebuild authority can be declared without hard-coding downstream paths.
projection_routing_contract:
  - Active-state pickup still starts with `current` and `validate`.
  - History/reporting questions may use `rebuild-projection` and `report-projection` when project policy declares compatible projection usage and rebuild authority.
  - Agents use planning-state command output, not SQL or direct database mutation.
  - Missing, stale, policy-incompatible, or unauthorized projections must produce compact blockers or warnings, not silent fallbacks to broad historical scans.
  - Projection reports are a bounded optimization for history/reporting; Markdown planning artifacts and explicit JSON state remain canonical.
guardrails:
  - Do not make SQLite required for `current`, `validate`, active-state selection, queueing, or closeout validation.
  - Do not choose a durable projection path as a generic default.
  - Do not add Graphify-specific paths, validation commands, cache paths, or local overlays to reusable skills or code.
  - Do not modify downstream project planning roots.
  - Do not update GitHub issues or comments as part of this planning batch.
dependencies_satisfied:
  - `planning-state-sqlite-projection` added optional rebuild and report commands.
  - `planning-state-skill-interface` created progressive references for projection reporting and target policy.
  - `planning-state-consumer-integration` wired consumer skills to the shared Planning State Diagnostic handoff.
dependencies_blocking:
  - None for projection routing.
suggested_slices:
  - Add projection usage and rebuild-authority policy vocabulary with parser/validation coverage.
  - Make the planning-state skill and references projection-aware for history/reporting questions.
  - Surface compact projection-routing facts, blockers, and warnings from diagnostics or dedicated policy checks.
  - Document validation evidence, update workflow metadata, and close PST-14/PST-15.
stop_conditions:
  - The batch would make projection data canonical over Markdown or explicit JSON state.
  - The batch would need a universal durable SQLite path.
  - The batch would require consumer skill rewiring before the planning-state interface is explicit.
  - The batch would need downstream project-specific paths or validation commands in generic code.
  - The batch would mutate downstream project planning roots.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/runway.md
```
