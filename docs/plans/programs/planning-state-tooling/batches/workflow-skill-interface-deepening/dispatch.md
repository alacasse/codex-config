# Workflow Skill Interface Deepening Dispatch

```yaml
batch_id: workflow-skill-interface-deepening
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-22
    title: Workflow skills repeat the planning pickup interface
  - id: PST-23
    title: Layout placement and operational pickup share a fuzzy seam
  - id: PST-24
    title: Program ledger updates and concrete runway ledger updates are easy to conflate
  - id: PST-25
    title: Specialized discovery skills can become parallel planning systems
excluded_findings:
  - id: PST-20
    title: Agent-facing SQLite language still makes normal projection reporting sound optional
    reason: Already closed by the projection language and migration batch.
  - id: PST-21
    title: Existing ledger workflows need a reusable projection-reporting adoption migration
    reason: Already closed by the projection language and migration batch.
goal: Deepen the reusable workflow-skill seams so agents have one planning pickup Interface, one artifact-placement owner, explicit program-vs-runway ledger ownership, and clear roles for specialized discovery skills.
owner_seam: Planning State owns operational pickup facts, target policy, validation, and projection-reporting routing; Planning Artifacts owns Layout v1 placement and artifact shape; Architecture Program Runway owns program finding selection and queue state; Batch Runway owns concrete slice execution state; specialized discovery skills own domain evidence and handoff packets unless explicitly named as the selected program owner.
validation_class: Workflow-skill wording tests or focused grep checks, planning-state current/validate diagnostics, manifest/changelog alignment when reusable skill behavior changes, and git diff --check.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `current` and `validate` report this batch as the queued planning-state-tooling batch.
    - Consumer workflow skills invoke Planning State for active-state pickup instead of restating competing pickup algorithms.
    - Layout placement guidance does not become a second operational pickup procedure.
secondary_fixture:
  project: reusable Layout v1 root shape
  expected_resolution:
    - Skill guidance remains project-neutral and does not hard-code downstream paths, cache locations, validation commands, or local overlays.
    - Specialized discovery skills can produce evidence or dispatch handoff artifacts without owning program queue state by default.
guardrails:
  - Do not move Planning Artifact Layout v1 placement rules into Planning State.
  - Do not move operational pickup, validation, target policy, or projection routing back into consumer skills.
  - Do not let specialized discovery skills create parallel durable ledgers unless they are explicitly the owning program.
  - Do not weaken Batch Runway coordinator/worker/reviewer boundaries.
  - Do not add downstream-specific paths, validation commands, cache locations, issue policy, or planning roots to generic skills.
  - Do not edit installed `~/.codex` paths directly unless ownership is checked and repo-owned changes are made through this repo.
dependencies_satisfied:
  - `planning-state-projection-language-and-migration` is closed.
  - PST-20 and PST-21 are closed with projection-backed reporting and reusable Layout v1 adoption guidance.
  - Baseline `current` and `validate` diagnostics pass for `docs/plans/`.
dependencies_blocking:
  - None for PST-22 through PST-25.
suggested_slices:
  - Make Planning State the single operational pickup Interface and shrink duplicated consumer pickup prose.
  - Re-separate Planning Artifacts placement guidance from Planning State operational pickup guidance.
  - Clarify the Architecture Program Runway and Batch Runway ledger handoff.
  - Define specialized discovery skill roles and reconcile metadata, planning state, and closeout evidence.
stop_conditions:
  - The work would create a second planning pickup algorithm outside Planning State.
  - The work would make Planning Artifacts responsible for operational validation or projection routing.
  - The work would blur program selection and concrete runway execution state.
  - The work would hard-code downstream project behavior into reusable workflow skills.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/runway.md
```
