# Planning-State Skill Interface Dispatch

```yaml
batch_id: planning-state-skill-interface
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-9
    title: Planning-state operations have no reusable skill interface
  - id: PST-10
    title: Planning-state operational details are split between layout guidance and historical plan prose
  - id: PST-11
    title: Project policy target selection is not packaged as an agent-facing adapter
excluded_findings:
  - id: PST-12
    reason: Consumer skills should not be rewired until the shared planning-state skill exists.
  - id: PST-13
    reason: Consumer dependency metadata should be changed with the consumer-integration batch after the operational skill is available.
goal: Create a repo-owned `planning-state` skill that gives fresh agents one compact, progressive interface for planning-state discovery, validation, optional state bootstrap, optional projection rebuild/reporting, closeout evidence checks, and target-policy refusal.
owner_seam: The agent-facing interface is `skills/planning-state/SKILL.md`; command behavior remains behind `python scripts/planning_state.py ...`; layout placement remains owned by `skills/planning-artifacts/SKILL.md`.
validation_class: skill entrypoint/reference validation, manifest/install metadata checks, planning-state CLI smoke, generated-only `/tmp` state/projection smoke, and grep checks for project-specific hard-coding.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - Read root and program CURRENT.md before ledgers, historical plans, generated reports, or source scans.
    - Run `current` and `validate` diagnostics before broad planning-state work.
    - Resolve generated-only state/projection policy without committing JSON state or SQLite files.
    - Treat this dispatch/runway pair as the queued planning-state batch until execution closes it.
secondary_fixture:
  project: project-neutral Layout v1 temp root
  expected_resolution:
    - Bootstrap explicit JSON state only to caller-provided temporary or policy-compatible targets.
    - Rebuild optional SQLite projections only to caller-provided temporary or policy-compatible targets.
    - Keep downstream project names, paths, cache locations, validation commands, and local overlays out of generic skill instructions.
skill_contract:
  - The `planning-state` skill entrypoint covers the routine hot path: discover project policy, run current/validate, inspect selected or queued state, and stop on missing policy for durable writes.
  - Optional references cover state fixtures, target-policy resolution, projection reporting, closeout evidence, runner artifacts, and command protocol details.
  - Agents use the `planning_state.py` command/file protocol rather than importing Python helpers, scraping historical filenames, or querying SQLite directly.
  - The skill delegates artifact placement to `planning-artifacts`; it must not duplicate Layout v1 as a second source of truth.
  - The skill explains safe target choices for stdout, `/tmp`, generated-only, committed, ignored-local, external, and none policies.
guardrails:
  - Do not update `architecture-program-runway`, `batch-runway`, or `legacy-removal` consumers in this batch.
  - Do not make `codex-config` docs paths, Graphify local overlay paths, cache paths, or validation commands generic defaults.
  - Do not change `scripts/planning_state.py` command semantics unless a tiny test/validation hook is required for skill validation.
  - Do not add durable JSON state or SQLite files to the repository.
  - Do not update GitHub issues or comments as part of this planning batch.
dependencies_satisfied:
  - PST-1 current and validate diagnostics exist.
  - PST-2 artifact allocation and registration commands exist.
  - PST-3 obligations are explicit state facts.
  - PST-4 closeout evidence validation/rendering exists.
  - PST-5 bootstrap-state can generate companion JSON state from Layout v1 Markdown.
  - PST-6 optional SQLite rebuild/report commands exist.
  - PST-7 command/file protocol boundary exists for runner interop.
  - PST-8 project policy discovery and target preflight exists.
dependencies_blocking:
  - None for creating the shared skill interface.
suggested_slices:
  - Create the `planning-state` skill entrypoint and routine hot-path contract.
  - Add state-fixture and target-policy references.
  - Add projection, closeout, and runner-artifact references.
  - Wire manifest/install metadata, skill validation tests, docs, changelog, and close PST-9 through PST-11.
stop_conditions:
  - The batch would need consumer-skill rewiring before the shared skill exists.
  - The batch would need a project-specific path, validation command, cache path, or local overlay in generic skill instructions.
  - The batch would need to choose a durable JSON state or SQLite projection target without resolved project policy.
  - The batch would need to make SQLite or JSON state canonical over Markdown planning artifacts.
  - The batch would need to modify downstream project planning roots.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/runway.md
```
