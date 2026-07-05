# Planning-State Consumer Integration Runway

## Purpose

Wire the shared `planning-state` skill into ledger-dependent consumer workflows
so agents use one operational interface for current-state diagnostics,
validation, target-policy checks, optional projection reporting, and closeout
evidence before each workflow makes its own semantic decisions.

This spec executes the `planning-state-consumer-integration` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/dispatch.md`.

## Current Baseline

- Baseline state: `python scripts/planning_state.py current --root docs/plans`
  and `python scripts/planning_state.py validate --root docs/plans` pass with
  only existing architecture-runner redirect warnings.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/dispatch.md`.
- Included findings: PST-12 and PST-13.
- Shared operational seam: `skills/planning-state/SKILL.md`.
- Layout seam: `skills/planning-artifacts/SKILL.md`.
- Consumer skills in scope:
  `skills/batch-runway/SKILL.md`,
  `skills/architecture-program-runway/SKILL.md`, and
  `skills/legacy-removal/SKILL.md`.
- Feature metadata in scope: `codex-features.json`.

## Assumptions

- `planning-state` owns operational diagnostics and target-policy guidance.
- `planning-artifacts` remains the owner for Layout v1 placement and naming.
- Consumer skills should consume Planning State Diagnostic facts, then make
  their own semantic decisions about batching, execution, grouping, legacy
  classification, and closeout.
- Feature dependencies should distinguish layout placement from operational
  planning-state diagnostics.
- The batch does not need new planning-state command behavior.

## Non-Goals

- Do not change `scripts/planning_state.py` command semantics.
- Do not change Batch Runway execution delegation or commit rules.
- Do not move Layout v1 placement rules out of `planning-artifacts`.
- Do not remove consumer-owned semantic decisions from `batch-runway`,
  `architecture-program-runway`, or `legacy-removal`.
- Do not create committed durable JSON state, SQLite projection files, runner
  receipts, generated reports, or downstream project planning files.
- Do not add downstream project-specific paths, cache paths, validation
  commands, issue policy, or local overlay details to reusable skills.
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
- Treat this session as `create-spec`; implementation starts in a later
  `execute-spec` session from the first pending active-ledger row.
- Use `full-runway` density because this batch changes reusable workflow
  instructions and install dependency behavior.
- Workers must not write to downstream project planning roots.
- Workers must not create committed durable JSON state or SQLite projection
  files.
- Workers must keep project-specific paths, validation commands, cache paths,
  and local overlays out of reusable consumer skills.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/project-harness-production.md`

Focused validation commands:
- For planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For feature metadata changes:
  `python -m json.tool codex-features.json`
  `python -m pytest tests/test_codex_features_manifest.py tests/test_codex_owner.py -q`
- For consumer wording checks, adapt to the final diff:
  `rg -n "planning-state|Planning State Diagnostic|current --root|validate --root" skills/batch-runway skills/architecture-program-runway skills/legacy-removal codex-features.json`
- For generic-skill hard-coding checks, the final diff should not introduce
  matches:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/batch-runway skills/architecture-program-runway skills/legacy-removal codex-features.json`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No package install is required unless feature-install behavior changes in a
  way manifest tests cannot cover.

Harness output:
- Existing `current` and `validate` checks should write no live planning files.
- Any optional generated proof output must use an explicit `/tmp` path.

Summary artifact:
- No generated summary artifact is required. Report compact stdout/stderr
  signals from validation commands.

Index refresh:
- None required for this repo after these skill/docs/manifest edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use concise imperative subjects listed in the slice sections.
- Commit only files in the slice scope plus this spec ledger/archive updates.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Do not revert or commit unrelated user changes outside the active slice.
- Do not write to downstream project planning roots.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| None | complete |  |  |  | Coordinator final validation and review before commit | All planned slices are archived below. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Wire batch-runway diagnostics | `7289956` | success; `batch-runway` now consumes Planning State Diagnostic facts before Layout v1 active-state pickup while preserving Batch Runway-owned decisions | `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `rg` wording/hard-coding checks; `test -f skills/batch-runway/references/../../planning-state/SKILL.md`; `git diff --check`; reviewer approved current diff |
| 2. Wire architecture-program diagnostics | `da97ac5` | success; `architecture-program-runway` now uses Planning State Diagnostic facts before Layout v1 pickup and closeout expansion while preserving program-owned decisions | `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `rg` wording check; diff-only hard-coding check; `git diff --check`; reviewer approved current diff |
| 3. Wire legacy-removal diagnostics | `2984eb7` | success; `legacy-removal` now uses Planning State Diagnostic facts before Layout v1 ledger/dispatch intake while preserving evidence-based legacy decisions | `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `rg` wording/hard-coding checks; `git diff --check`; reviewer approved current diff |
| 4. Align feature dependencies and close queue | final closeout commit | success; consumer feature metadata now installs `planning-state` after `planning-artifacts`, focused manifest tests assert dependency expansion, and program state points at the batch closeout with no queued planning-state-tooling batch | `python -m json.tool codex-features.json`; `python -m pytest tests/test_codex_features_manifest.py tests/test_codex_owner.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `rg -n "planning-state" codex-features.json skills/batch-runway skills/architecture-program-runway skills/legacy-removal`; `git diff --check`; runway_reviewer approved current diff |

## Slice 1. Wire Batch-Runway Diagnostics

Scope:
- Update `skills/batch-runway/SKILL.md` and focused references so `create-spec`
  and `execute-spec` flows use the `planning-state` skill before consuming
  Layout v1 active-state files, selected dispatches, queued specs, or target
  policy.
- Define the handoff as compact Planning State Diagnostic facts: root,
  current/validate status, active programs, selected dispatch, queued batch,
  active runway, blockers, warnings, and project policy.
- Keep `batch-runway` responsible for concrete 3-5 slice spec creation,
  execution orchestration, validation selection, subagent routing, ledger
  updates, and commits.

Allowed files/areas:
- `skills/batch-runway/SKILL.md`
- Focused `skills/batch-runway/references/*.md` files needed for create-spec,
  execution pickup, or project values
- This spec ledger/archive rows
- `CHANGELOG.md` if the user-facing workflow surface changes

Non-goals:
- Do not change Batch Runway delegation, review, or commit semantics.
- Do not move Layout v1 placement rules into `batch-runway`.
- Do not add new planning-state command behavior.
- Do not update feature metadata in this slice unless needed to keep tests
  coherent.

Acceptance criteria:
- A fresh `batch-runway` agent knows to use `planning-state` for current and
  validate diagnostics before broad Layout v1 scans.
- The guidance names what diagnostic facts are passed into `batch-runway`.
- `batch-runway` still owns its own semantic decisions after the diagnostic
  handoff.
- No downstream project path, validation command, cache path, or local overlay
  becomes a reusable default.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `rg -n "planning-state|Planning State Diagnostic|current --root|validate --root" skills/batch-runway`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/batch-runway` should produce no matches from the slice diff.
  `git diff --check`

Test quality review:
- None; this is a workflow-doc slice.

Commit message:
- `Route batch runway through planning state`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, diagnostic handoff clarity, preserved
  `batch-runway` ownership, and absence of project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if `batch-runway` would need to duplicate planning-state target-policy
  or projection setup.
- Stop if the change would weaken the standard execution contract.

## Slice 2. Wire Architecture-Program Diagnostics

Scope:
- Update `skills/architecture-program-runway/SKILL.md` and focused references
  so active-state pickup starts with `planning-state` diagnostics when Layout
  v1 is active.
- Keep `architecture-program-runway` responsible for program selection,
  grouping, queue state, selected dispatch packets, closeout reconciliation,
  and handoff to `batch-runway`.
- Clarify that diagnostics prevent stale historical scans, but do not replace
  program-ledger semantics.

Allowed files/areas:
- `skills/architecture-program-runway/SKILL.md`
- Focused `skills/architecture-program-runway/references/*.md` files needed by
  active-state pickup or closeout
- This spec ledger/archive rows
- `CHANGELOG.md` if the user-facing workflow surface changes

Non-goals:
- Do not change the architecture-program runner command behavior.
- Do not change `batch-runway` contracts in this slice.
- Do not create a new program ledger template unless the existing text cannot
  express the handoff.

Acceptance criteria:
- A fresh architecture-program agent uses `planning-state` current/validate
  facts before reading historical plans or broad generated outputs.
- The skill still owns grouping, sequencing, selected dispatch packets, and
  closeout reconciliation after diagnostics are collected.
- The text keeps `planning-artifacts` as the placement owner.
- No downstream project path, validation command, cache path, or local overlay
  becomes a reusable default.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `rg -n "planning-state|Planning State Diagnostic|current --root|validate --root" skills/architecture-program-runway`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/architecture-program-runway` should produce no matches from the slice diff.
  `git diff --check`

Test quality review:
- None; this is a workflow-doc slice.

Commit message:
- `Route architecture runway through planning state`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, active-state handoff clarity, preserved
  architecture-program ownership, and absence of project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if diagnostics would replace the program ledger as semantic authority.
- Stop if the change would make the local runner depend on undocumented
  planning-state internals.

## Slice 3. Wire Legacy-Removal Diagnostics

Scope:
- Update `skills/legacy-removal/SKILL.md` and focused references so Layout v1
  ledger or selected-dispatch work uses `planning-state` diagnostics before
  creating, consuming, or validating active planning state.
- Preserve `legacy-removal` ownership over old/canonical model definition,
  evidence inventory, compatibility decisions, cleanup-residue classification,
  and handoff to `architecture-program-runway` or `batch-runway`.
- Clarify that `planning-state` target-policy and projection guidance is used
  only when the task needs durable/generated state or reports.

Allowed files/areas:
- `skills/legacy-removal/SKILL.md`
- Focused `skills/legacy-removal/references/*.md` files if needed
- This spec ledger/archive rows
- `CHANGELOG.md` if the user-facing workflow surface changes

Non-goals:
- Do not change legacy-removal classification vocabulary unless needed for the
  handoff.
- Do not load or modify `dead-surface-audit` guidance unless required by the
  final wording.
- Do not create or update downstream legacy ledgers.

Acceptance criteria:
- A fresh legacy-removal agent knows when to use `planning-state` before Layout
  v1 ledger/dispatch work.
- The skill still treats tests as evidence and preserves its compatibility and
  cleanup-residue decision rules.
- The guidance does not imply that diagnostics decide what legacy code to keep
  or remove.
- No downstream project path, validation command, cache path, or local overlay
  becomes a reusable default.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `rg -n "planning-state|Planning State Diagnostic|current --root|validate --root" skills/legacy-removal`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/legacy-removal` should produce no matches from the slice diff.
  `git diff --check`

Test quality review:
- None; this is a workflow-doc slice.

Commit message:
- `Route legacy removal through planning state`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, planning-state handoff clarity, preserved
  legacy-removal ownership, and absence of project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if diagnostics would replace evidence-based legacy classification.
- Stop if the change would make legacy-removal depend on SQL or Python
  internals.

## Slice 4. Align Feature Dependencies and Close Queue

Scope:
- Update `codex-features.json` so consumer features that now call the shared
  diagnostics require `planning-state` while keeping `planning-artifacts` where
  they still consume placement rules directly.
- Update focused manifest tests if dependency expectations are asserted.
- Update `CHANGELOG.md` for the user-facing workflow dependency change.
- Update this planning-state program `CURRENT.md` and `LEDGER.md` during
  closeout execution to mark PST-12 and PST-13 closed only after validation and
  review evidence exists.

Allowed files/areas:
- `codex-features.json`
- `tests/test_codex_features_manifest.py`
- `tests/test_codex_owner.py` only if existing owner/dependency tests require
  alignment
- `CHANGELOG.md`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/closeout.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/completed-slices.md`

Non-goals:
- Do not remove `planning-artifacts` from a consumer that still reads placement
  conventions directly.
- Do not add optional downstream-only features as default dependencies.
- Do not create runner JSON state or SQLite projection artifacts.

Acceptance criteria:
- Feature metadata installs `planning-state` before consumers that invoke it.
- Manifest JSON remains valid and focused tests pass.
- PST-12 and PST-13 are closed only with evidence from completed slices,
  validation, review, and closeout.
- Program `CURRENT.md` clears selected/queued state after closeout, not before.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m json.tool codex-features.json`
  `python -m pytest tests/test_codex_features_manifest.py tests/test_codex_owner.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `rg -n "planning-state" codex-features.json skills/batch-runway skills/architecture-program-runway skills/legacy-removal`
  `git diff --check`

Test quality review:
- Required if tests are changed; review whether assertions protect install
  dependency behavior rather than only formatting.

Commit message:
- `Declare planning state consumer dependencies`

Coding subagent brief:
- Implement only Slice 4 from this spec after Slices 1-3 are committed.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, dependency ordering, test assertion value,
  changelog alignment, and closeout state consistency.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if feature dependency metadata cannot express the required ordering
  without creating a dependency cycle.
- Stop if the closeout would mark PST-12 or PST-13 closed without completed
  implementation evidence.

## Final Validation

Run after all slices are complete:

- `python -m json.tool codex-features.json`
- `python -m pytest tests/test_codex_features_manifest.py tests/test_codex_owner.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `rg -n "planning-state|Planning State Diagnostic|current --root|validate --root" skills/batch-runway skills/architecture-program-runway skills/legacy-removal codex-features.json`
- `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/batch-runway skills/architecture-program-runway skills/legacy-removal codex-features.json` should produce no matches from the final diff.
- `git diff --check`

## Stop Conditions

- Stop if any consumer skill would need to duplicate planning-state command,
  target-policy, projection, or closeout setup.
- Stop if the batch would remove consumer-owned semantic responsibilities.
- Stop if a universal durable JSON state or SQLite projection target is needed.
- Stop if downstream project-specific paths, validation commands, cache paths,
  issue policy, or local overlays would become reusable defaults.
- Stop if validation or review finds a dependency cycle or install metadata
  inconsistency.
- Stop if work would write to downstream project planning roots.
