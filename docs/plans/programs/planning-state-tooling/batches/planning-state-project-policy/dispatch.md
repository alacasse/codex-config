# Planning-State Project Policy Dispatch

```yaml
batch_id: planning-state-project-policy
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-8
    title: Project planning-state ownership policy is implicit
excluded_findings:
  - id: PST-6
    reason: SQLite projection should consume project policy; it should not choose state-file or database ownership rules.
goal: Define and implement project-owned planning-state policy discovery so codex-config, ignored local overlays such as Graphify my-docs, and future projects can declare where durable planning state, generated state, run artifacts, and projections belong.
owner_seam: scripts/planning_state.py remains the workflow facade; shared project-policy vocabulary belongs in reusable planning-artifact guidance, while project-specific values stay in project instructions, CURRENT.md, local overlays, or active specs.
validation_class: focused project-policy parsing/validation tests, planning-state CLI checks, temp Layout v1 fixtures for committed and ignored-local policies, and ruff on touched Python files.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - Read root and program CURRENT.md before ledgers or historical plans.
    - Resolve this repo's project policy without making it a generic default for other projects.
    - Keep docs/plans human-readable and repo-owned while refusing to commit SQLite databases or runtime cache files.
secondary_fixture:
  project: Graphify-style ignored local overlay
  planning_root: my-docs/plans/
  expected_resolution:
    - Policy can represent ignored-local planning roots and ignored run/state/output roots.
    - No Graphify-specific production path, validation command, cache path, or overlay rule is hard-coded into generic code.
    - A missing policy stops durable state writes while still allowing stdout or /tmp bootstrap proof.
policy_contract:
  - Project policy is a discovered project value, not a reusable-skill hard-code.
  - Policy names planning_root, run_artifact_root, output_root, state_file_policy, state_file_path when selected, projection_policy, projection_path when selected, and update authority.
  - state_file_policy values are generated-only, committed, ignored-local, external, or none.
  - projection_policy values are generated-only, ignored-local, external, or none unless a project explicitly allows a committed projection.
  - Markdown planning artifacts remain human-readable coordination state.
  - JSON state may be a committed or local companion only when project policy says so.
  - SQLite remains optional, rebuildable, and never canonical.
guardrails:
  - Do not make codex-config's committed docs/plans layout the generic answer for Graphify or future projects.
  - Do not write durable JSON state or SQLite files unless policy explicitly selects a target.
  - Do not require state files for current/validate on Markdown-only projects.
  - Do not add Graphify-specific branches to production code.
  - Do not update GitHub issues or comments as part of this planning-state policy batch.
dependencies_satisfied:
  - PST-1 read-only current and validate diagnostics exist.
  - PST-2 artifact allocation and registration commands exist.
  - PST-3 obligations are explicit state facts.
  - PST-4 closeout evidence is bounded and validateable.
  - PST-5 bootstrap-state can generate companion JSON state from Layout v1 Markdown.
  - PST-7 command/file protocol boundary exists for runner interop.
dependencies_blocking:
  - None for defining and validating project-state policy before SQLite.
suggested_slices:
  - Define the project-state policy vocabulary and discovery contract.
  - Add planning-state policy reporting and validation to current/validate.
  - Enforce state-file and projection target policy in write/preflight commands.
  - Document codex-config and ignored-local policy examples, then unblock SQLite.
stop_conditions:
  - The batch would need to pick one universal state-file path for every project.
  - The batch would need to commit ignored/local overlay artifacts.
  - The batch would need to write durable JSON state or SQLite files without an explicit project policy.
  - The batch would need Graphify-specific production paths, cache paths, validation commands, or overlays.
  - The policy model conflicts with Planning Artifact Layout v1 root discovery.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/runway.md
```
