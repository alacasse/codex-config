# Workflow Skill Interface Deepening Runway

## Purpose

Deepen the reusable workflow-skill boundaries after the Planning State and
projection-reporting work. The batch should make `planning-state` the single
operational pickup Interface for Layout v1 state, keep `planning-artifacts`
focused on placement and shape, clarify where program ledgers stop and concrete
runway ledgers begin, and prevent specialized discovery skills from becoming
parallel planning systems by default.

This spec executes the `workflow-skill-interface-deepening` batch described by
`docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/dispatch.md`.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans`
  and
  `python scripts/planning_state.py validate --root docs/plans`.
- Planning root: `docs/plans/`.
- Program: `planning-state-tooling`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/dispatch.md`.
- Included findings: PST-22, PST-23, PST-24, and PST-25.
- Before this batch was materialized, no planning-state-tooling batch was
  selected, queued, or active.
- Project policy resolves to `state_file_policy: generated-only`,
  `projection_policy: generated-only`, `projection_usage: caller-directed`,
  and `projection_rebuild_authority: command`.
- The latest completed planning-state batch closed PST-20 and PST-21, so
  projection-backed reporting is already the policy-gated normal route for
  supported history/reporting questions.

## Assumptions

- Planning State owns operational pickup, current/validate diagnostics, target
  policy, projection-reporting routing, and compact handoff facts.
- Planning Artifacts owns Layout v1 placement, naming, active-state file shape,
  batch directory conventions, archive placement, run artifact roots, and output
  roots.
- Architecture Program Runway owns program findings, grouping, queue state,
  selected dispatch, and closeout reconciliation.
- Batch Runway owns concrete 3-5 slice execution state, validation selection,
  worker/reviewer routing, commit receipts, and completed-slice archives.
- Specialized discovery skills can produce domain evidence and dispatch
  handoff material, but they do not own durable program selection unless the
  workflow explicitly names them as the program owner.
- Workflow doc and skill behavior changes should keep `CHANGELOG.md` and
  `codex-features.json` aligned when installed surfaces change.

## Non-Goals

- Do not change `scripts/planning_state.py` behavior unless a focused
  docs-as-code test exposes an existing mismatch that must be fixed for this
  batch's acceptance criteria.
- Do not add durable JSON state, durable SQLite projections, runner artifacts,
  or generated reports.
- Do not run live downstream project validation.
- Do not hard-code downstream project names, paths, validation commands, cache
  locations, issue policy, or local overlays into reusable skills.
- Do not update GitHub issues or comments.

## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about
suspicious coordinator or subagent-lifecycle behavior.
Use the expanded convergence template only when scope is expanding, significant
uncertainty exists, blockers are present, or final batch reporting is produced.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execute-slice-core-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execution-contract-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/reporting-contracts-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/ledger-retention-v1.md`

Overrides:
- Use `lean-runway` density because this batch is reusable workflow guidance,
  docs-as-code checks, and planning-state reconciliation.
- Workers must not write durable JSON planning state, durable SQLite
  projections, runner artifacts, downstream project planning roots, or installed
  `~/.codex` paths.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- Skill wording and ownership checks, using focused pytest if existing tests
  already cover the touched workflow-skill contract.
- Planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Manifest checks, if feature metadata changes:
  `python -m pytest tests/test_codex_features_manifest.py -q`
- Hard-coding check:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific" skills/planning-state skills/planning-artifacts skills/batch-runway skills/architecture-program-runway skills/legacy-removal skills/dead-surface-audit`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No committed SQLite database or durable JSON state file is required.

Harness output:
- `current` and `validate` checks should write no live planning files.
- No generated summary artifact is required.

Index refresh:
- None required for this repo after workflow-doc, test, and planning-doc edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Treat this batch's `CURRENT.md`, `LEDGER.md`, `dispatch.md`, and `runway.md`
  edits as coordinator-owned planning state.
- Do not revert or commit unrelated user changes outside the active slice.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1. Make pickup single-owned | Closed | this commit | `consumer_projection_routing.py` 12 passed; `current`; `validate`; `git diff --check` | Clean review | Planning Artifacts placement seam remains. | Consumer workflow skills now route Layout v1 pickup through Planning State Diagnostic-First Pickup while preserving consumer-owned semantic decisions. |
| 2. Re-separate layout and pickup | Closed | this commit | `consumer_projection_routing.py` 13 passed; `current`; `validate`; `git diff --check` | Clean review after focused phrase-wrap recovery | Program-vs-runway ledger handoff remains. | Planning Artifacts now owns placement and active-state file shape without acting as a competing pickup algorithm; Planning State is the first-use owner for pickup, validation, target policy, and projection routing. |
| 3. Clarify program/runway handoff | pending | | | | Specialized discovery role boundaries remain. | |
| 4. Define discovery roles and closeout | pending | | | | Final metadata and planning closeout. | |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Make pickup single-owned | this commit | Batch Runway, Architecture Program Runway, and Legacy Removal now invoke Planning State Diagnostic-First Pickup as the single Layout v1 operational pickup Interface while retaining their own semantic decisions; focused tests guard against reintroducing duplicate pickup guidance. | Validation: `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`, `python scripts/planning_state.py current --root docs/plans`, `python scripts/planning_state.py validate --root docs/plans`, `git diff --check`; review: clean `runway_reviewer` result against the Slice 1 diff. |
| 2. Re-separate layout and pickup | this commit | Planning Artifacts now defines placement, naming, file shape, archives, and roots while directing operational pickup through Planning State; Planning State explicitly owns pickup ordering, validation, target-policy checks, and projection routing without redefining artifact layout. | Validation: `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`, `python scripts/planning_state.py current --root docs/plans`, `python scripts/planning_state.py validate --root docs/plans`, `git diff --check`; review: clean `runway_reviewer` result after focused phrase-wrap recovery. |

## Slice 1. Make Pickup Single-Owned

Scope:
- Update consumer workflow skills so `planning-state` is the single operational
  pickup Interface for Layout v1 state.
- Shrink duplicated instructions that restate how to run `current`/`validate`,
  inspect active files, use projection reports, or avoid broad scans.
- Keep each consumer skill responsible for its semantic decision after receiving
  compact Planning State Diagnostic facts.
- Add or adjust focused wording checks if tests already protect workflow-skill
  obligations.

Allowed files/areas:
- `skills/planning-state/SKILL.md`
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/create-spec.md`
- `skills/batch-runway/references/execute-spec.md`
- `skills/architecture-program-runway/SKILL.md`
- `skills/legacy-removal/SKILL.md`
- Existing workflow-skill obligation tests, if present
- This spec active-ledger/archive rows

Non-goals:
- Do not remove consumer-owned semantic responsibilities.
- Do not change `scripts/planning_state.py` command behavior.
- Do not weaken projection-reporting fallback/blocker handling.

Acceptance criteria:
- Consumer skills invoke Planning State for active-state pickup instead of
  embedding a competing pickup algorithm.
- Consumer skills still name the compact facts they consume and the semantic
  decision they own.
- A focused check fails if the consumer guidance drops the Planning State
  Diagnostic dependency or reintroduces broad historical scans before
  `current`/`validate`.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless tests become broad snapshots or assertion-light wording scans.

Commit message:
- `Make planning pickup single-owned`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, the Planning State pickup Interface boundary, and
  absence of new project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if a consumer skill loses its own semantic decision boundary.
- Stop if the edit creates a second operational pickup procedure outside
  Planning State.

## Slice 2. Re-Separate Layout And Pickup

Scope:
- Refine `planning-artifacts` so it clearly owns placement, naming, active-state
  file shape, batch directory conventions, archives, run artifact roots, and
  output roots.
- Refine `planning-state` cross-references so operational pickup, validation,
  target policy, and projection routing stay in Planning State.
- Remove or narrow wording that makes layout guidance look like a competing
  operational pickup algorithm when Planning State is available.

Allowed files/areas:
- `skills/planning-artifacts/SKILL.md`
- `skills/planning-state/SKILL.md`
- Existing planning-artifact or planning-state wording tests, if present
- This spec active-ledger/archive rows

Non-goals:
- Do not remove Layout v1 placement details from `planning-artifacts`.
- Do not make `planning-state` redefine artifact directory layout.
- Do not add downstream project layout defaults.

Acceptance criteria:
- `planning-artifacts` remains the placement and shape owner.
- `planning-state` remains the operational pickup and validation owner.
- The guidance tells agents which skill to use first for pickup questions
  without making artifact layout guidance stale or redundant.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless tests become broad snapshots or assertion-light wording scans.

Commit message:
- `Separate layout from pickup guidance`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, the placement-vs-pickup ownership boundary, and
  absence of project-specific defaults.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if Layout v1 placement details are removed rather than narrowed.
- Stop if Planning Artifacts becomes responsible for validation or projection
  routing.

## Slice 3. Clarify Program/Runway Handoff

Scope:
- Clarify where `architecture-program-runway` owns program findings, grouping,
  selected dispatch, queue state, and closeout reconciliation.
- Clarify where `batch-runway` owns concrete runway creation, slice execution
  ledgers, validation selection, review routing, commits, and completed-slice
  archives.
- Add or adjust focused wording checks if existing tests cover these workflow
  obligations.

Allowed files/areas:
- `skills/architecture-program-runway/SKILL.md`
- `skills/architecture-program-runway/references/`
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/`
- Existing workflow-skill obligation tests, if present
- This spec active-ledger/archive rows

Non-goals:
- Do not change runner code.
- Do not change the Batch Runway worker/reviewer execution contract.
- Do not create or execute an architecture-runner batch.

Acceptance criteria:
- Program-level ledger updates are described as Architecture Program Runway
  responsibilities.
- Concrete execution-ledger updates are described as Batch Runway
  responsibilities.
- The handoff for selected dispatch -> concrete runway -> closeout
  reconciliation is explicit enough that the two skills do not read as
  competing ledger managers.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless tests become broad snapshots or assertion-light wording scans.

Commit message:
- `Clarify program and runway ledgers`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, the program-ledger vs concrete-runway ledger
  boundary, and preservation of Batch Runway execution rules.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if Batch Runway starts owning program selection.
- Stop if Architecture Program Runway starts owning concrete slice execution
  details.

## Slice 4. Define Discovery Roles And Closeout

Scope:
- Define whether specialized discovery skills are evidence producers, selected
  program owners, or handoff sources before they create durable ledgers.
- Apply the role model to `legacy-removal` and any directly related discovery
  skill whose current wording would otherwise create a parallel planning
  system.
- Align `CHANGELOG.md` and `codex-features.json` for meaningful reusable
  workflow behavior changes.
- Reconcile `docs/plans/programs/planning-state-tooling/CURRENT.md` and
  `LEDGER.md` for completed state during execution, then create pointer-first
  closeout evidence and completed-slice archive when the batch completes.

Allowed files/areas:
- `skills/legacy-removal/SKILL.md`
- Directly related discovery-skill guidance, if the Slice 4 review finds it is
  part of the same role-boundary issue
- `CHANGELOG.md`
- `codex-features.json`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/`
- Existing workflow-skill obligation tests, if present

Non-goals:
- Do not broaden into a full skill cleanup batch.
- Do not create new GitHub issues or comments.
- Do not select a successor batch.

Acceptance criteria:
- Specialized skills do not create durable program ledgers or queue state by
  default unless they are explicitly the owning program.
- The guidance supports evidence production and dispatch handoff without
  bypassing program-level selection.
- Feature metadata and changelog reflect behavior-changing reusable skill edits
  when needed.
- Final planning-state diagnostics pass with no active-state contradictions.
- Closeout evidence is pointer-first and bounded.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_codex_features_manifest.py -q` if
  `codex-features.json` changes
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  hard-coding check from the validation profile
  `git diff --check`

Test quality review:
- None unless this slice materially changes test structure.

Commit message:
- `Close workflow interface deepening batch`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, discovery-skill role boundaries, metadata
  alignment, and closeout state.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the role model requires a broad redesign of all discovery skills.
- Stop if reusable skills start hard-coding downstream project behavior.
- Stop if final diagnostics report contradictory selected, active, or queued
  planning-state artifacts.
