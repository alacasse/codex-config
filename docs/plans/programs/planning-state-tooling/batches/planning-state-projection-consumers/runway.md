# Planning-State Projection Consumers Runway

## Purpose

Make projection-report routing operational for the consumer workflows that
already use the Planning State Diagnostic. The batch should teach Batch Runway,
Architecture Program Runway, and Legacy Removal when to try policy-compatible
projection reports for supported history/reporting questions before broad
historical scans, while keeping their active-state pickup and semantic decisions
unchanged.

This spec executes the `planning-state-projection-consumers` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/dispatch.md`.

## Current Baseline

- Baseline state: `python scripts/planning_state.py current --root docs/plans
  --format json` and `python scripts/planning_state.py validate --root
  docs/plans --format json` pass with no blockers and existing redirect
  warnings only.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/dispatch.md`.
- Included findings: PST-16 and PST-17.
- `skills/planning-state/SKILL.md` already owns the projection-backed reporting
  hot path and points to
  `skills/planning-state/references/projection-reporting.md`.
- `skills/batch-runway/SKILL.md`,
  `skills/architecture-program-runway/SKILL.md`, and
  `skills/legacy-removal/SKILL.md` already consume active-state diagnostics but
  do not yet require projection reports for supported history/reporting
  workflows before broad scans.
- `tests/test_codex_features_manifest.py` already protects consumer feature
  dependencies on `planning-artifacts` and `planning-state`; a focused
  consumer-obligation test surface is still missing.

## Assumptions

- Active-state pickup remains file-first through `planning-state current` and
  `validate`; consumer workflows must not require SQLite for normal pickup.
- Projection reports are useful only for supported history/reporting questions,
  such as pending-batch inventory, missing closeout evidence, batch evidence,
  runner summaries, or bounded backlog/history reports.
- Projection report use depends on compatible `projection_usage`,
  `projection_rebuild_authority`, and target policy.
- Consumer skills should consume command output and planning-state references,
  not query SQLite directly or duplicate projection policy logic.
- Workflow doc edits are behavior changes for repo-owned skills, so
  `CHANGELOG.md` and `codex-features.json` must stay aligned when the consumer
  skill surfaces change.

## Non-Goals

- Do not change `scripts/planning_state.py` projection behavior unless a
  consumer test exposes a real missing command fact.
- Do not make SQLite or projection rebuilds required for active-state pickup,
  create-spec, execute-spec, batch selection, closeout reconciliation, or
  legacy classification.
- Do not store raw logs, prompts, transcripts, full Markdown bodies, or SQL
  query details in consumer guidance.
- Do not add project-specific validation commands, cache paths, downstream
  planning roots, or local overlays to generic skills.
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
- Use `lean-runway` density because this batch is mostly workflow-doc and
  regression-test wiring.
- Workers must not write to downstream project planning roots.
- Workers must not create a committed durable SQLite database.
- Workers must not change planning-state command behavior unless a focused
  consumer regression test proves the existing command surface is insufficient.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- For consumer obligation tests:
  `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`
- For manifest or version dependency checks:
  `python -m pytest tests/test_codex_features_manifest.py -q`
- For planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- For projection-routing wording:
  `rg -n "projection|report-projection|projection_usage|projection_rebuild_authority|historical scan|history/reporting" skills/batch-runway skills/architecture-program-runway skills/legacy-removal tests/test_planning_state_consumer_projection_routing.py`
- For hard-coding checks, the final diff should not introduce matches:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/batch-runway skills/architecture-program-runway skills/legacy-removal tests/test_planning_state_consumer_projection_routing.py`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No projection database is required unless a slice deliberately adds a
  temporary proof command; use `/tmp` only for such proof.

Harness output:
- Existing `current` and `validate` checks should write no live planning files.
- No generated summary artifact is required.

Index refresh:
- None required for this repo after these workflow-doc and test edits.

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
| 1. Route Batch Runway projection reports | Closed | this commit | `tests/test_planning_state_consumer_projection_routing.py` passed 3; manifest tests passed 6; `current`/`validate` passed with existing redirect warnings only; `git diff --check` passed | `runway_reviewer` clean | Consumer routing test for Architecture Program Runway passes | Batch Runway now routes supported history/reporting questions through policy-compatible projection reports while keeping active pickup on `current`/`validate`. |
| 2. Route Architecture Program projection reports | Pending |  |  |  | Consumer routing test for Architecture Program Runway passes |  |
| 3. Route Legacy Removal projection reports | Pending |  |  |  | Consumer routing test for Legacy Removal passes |  |
| 4. Align metadata and close consumer obligations | Pending |  |  |  | Manifest, changelog, diagnostics, and final hard-coding checks pass |  |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Route Batch Runway projection reports | this commit | success; Batch Runway now names projection-reporting guidance and `report-projection` for supported history/reporting questions without making SQLite part of active-state pickup | Validation: `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`, `python -m pytest tests/test_codex_features_manifest.py -q`, `python scripts/planning_state.py current --root docs/plans`, `python scripts/planning_state.py validate --root docs/plans`, `git diff --check`; review: clean `runway_reviewer` result against the Slice 1 diff. |

## Slice 1. Route Batch Runway Projection Reports

Scope:
- Update Batch Runway guidance so supported history/reporting questions try
  planning-state projection reports before broad historical scans when project
  policy permits.
- Keep create-spec and execute-spec active-state pickup on `current` and
  `validate`.
- Add or extend focused tests that assert Batch Runway names the projection
  reporting obligation and still depends on `planning-state`.
- Update `CHANGELOG.md` and the `batch-runway` feature version if the skill
  behavior surface changes.

Allowed files/areas:
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/create-spec.md`
- `skills/batch-runway/references/execute-spec.md`
- `skills/batch-runway/references/finalize-batch-v1.md`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_codex_features_manifest.py` if dependency/version checks need a
  small extension
- `codex-features.json`
- `CHANGELOG.md`
- This spec ledger/archive rows

Non-goals:
- Do not change Batch Runway slice execution ownership, subagent requirements,
  or commit rules.
- Do not make projection reports decide slice scope, validation profile,
  subagent routing, ledger updates, or commit readiness.
- Do not make projection reporting mandatory for ordinary active-state pickup.

Acceptance criteria:
- Batch Runway still starts Layout v1 pickup with Planning State Diagnostic
  facts.
- Batch Runway tells agents to read planning-state projection-reporting guidance
  and use policy-compatible reports before broad history/reporting scans.
- Missing or incompatible projection policy remains a bounded blocker or
  explicit fallback decision, not silent Markdown archaeology.
- Regression tests protect the Batch Runway obligation.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless the slice adds assertion-light or broad fixture tests.

Commit message:
- `Route batch runway projection reporting`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, Batch Runway ownership boundaries, projection
  fallback clarity, dependency/version/changelog alignment, and absence of
  project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if Batch Runway wording implies SQLite is required for active-state
  pickup.
- Stop if projection reports would choose Batch Runway slice semantics.

## Slice 2. Route Architecture Program Projection Reports

Scope:
- Update Architecture Program Runway guidance so program history/reporting,
  pending-batch inventory, missing closeout evidence, runner summary, or
  backlog-report questions try policy-compatible projection reports before
  broad historical scans.
- Preserve Architecture Program ownership of grouping, sequencing, dispatch
  selection, closeout reconciliation, and handoff to Batch Runway.
- Add or extend focused tests that assert Architecture Program Runway names the
  projection reporting obligation and still depends on `planning-state`.
- Update `CHANGELOG.md` and the `architecture-program-runway` feature version
  if the skill behavior surface changes.

Allowed files/areas:
- `skills/architecture-program-runway/SKILL.md`
- `skills/architecture-program-runway/references/program-ledger-template.md`
- `skills/architecture-program-runway/references/goal-runner-v1.md`
- `skills/architecture-program-runway/references/local-runner-v1.md`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_architecture_program_runner_protocol.py` if protocol-specific
  assertions are more appropriate
- `tests/test_codex_features_manifest.py` if dependency/version checks need a
  small extension
- `codex-features.json`
- `CHANGELOG.md`
- This spec ledger/archive rows

Non-goals:
- Do not change local runner command behavior.
- Do not make projection reports select architecture batches or close findings.
- Do not replace selected dispatch packets or program ledgers with projection
  output.

Acceptance criteria:
- Architecture Program Runway still uses Planning State Diagnostic facts before
  active-state reads.
- The skill routes supported history/reporting questions through projection
  reports when policy permits before broad historical scans.
- Projection report failures are explicit blockers, warnings, or fallback
  decisions.
- Regression tests protect the Architecture Program Runway obligation.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`
  `python -m pytest tests/test_architecture_program_runner_protocol.py -q`
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless tests become broad or assertion-light.

Commit message:
- `Route architecture program projection reporting`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, Architecture Program ownership boundaries,
  runner/projection distinction, dependency/version/changelog alignment, and
  absence of project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if projection reports would replace program ledger or selected dispatch
  authority.
- Stop if the wording changes local runner execution semantics.

## Slice 3. Route Legacy Removal Projection Reports

Scope:
- Update Legacy Removal guidance so supported planning history/reporting
  questions try policy-compatible planning-state projection reports before
  broad historical scans.
- Preserve Legacy Removal ownership of old/canonical model definition,
  evidence inventory, compatibility decisions, cleanup-residue classification,
  and handoff decisions.
- Add or extend focused tests that assert Legacy Removal names the projection
  reporting obligation and still depends on `planning-state`.
- Update `CHANGELOG.md` and the `legacy-removal` feature version if the skill
  behavior surface changes.

Allowed files/areas:
- `skills/legacy-removal/SKILL.md`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_codex_features_manifest.py` if dependency/version checks need a
  small extension
- `codex-features.json`
- `CHANGELOG.md`
- This spec ledger/archive rows

Non-goals:
- Do not change legacy-removal evidence standards, test-classification rules,
  compatibility decisions, or cleanup-residue semantics.
- Do not make projection reports decide whether a surface is legacy, removable,
  public, or deferred.
- Do not require SQLite for ordinary Markdown ledger or dispatch work.

Acceptance criteria:
- Legacy Removal still uses Planning State Diagnostic facts for Layout v1
  active-state intake.
- The skill routes supported history/reporting questions through projection
  reports when policy permits before broad historical scans.
- Projection report output is treated as planning-state context only, not
  evidence that decides legacy classification.
- Regression tests protect the Legacy Removal obligation.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`
  `python -m pytest tests/test_codex_features_manifest.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless tests become broad or assertion-light.

Commit message:
- `Route legacy removal projection reporting`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, Legacy Removal evidence boundaries,
  projection-report fallback clarity, dependency/version/changelog alignment,
  and absence of project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if projection reports are treated as proof that a legacy surface is live
  or dead.
- Stop if the guidance weakens named-reason requirements for keeping
  compatibility.

## Slice 4. Align Metadata And Close Consumer Obligations

Scope:
- Audit the three consumer skill updates as a set and make sure the projection
  reporting obligation is consistent but not copy-pasted into misleading
  contexts.
- Ensure `CHANGELOG.md`, `codex-features.json`, and focused tests are aligned
  with all behavior-changing workflow doc edits.
- Update the active ledger and completed-slice archive for this runway closeout.
- Prepare the planning-state program ledger to close PST-16 and PST-17 only
  after validation, review, and closeout evidence exist.

Allowed files/areas:
- `skills/batch-runway/**`
- `skills/architecture-program-runway/**`
- `skills/legacy-removal/**`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_codex_features_manifest.py`
- `codex-features.json`
- `CHANGELOG.md`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/closeout.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/completed-slices.md`
- This spec ledger/archive rows

Non-goals:
- Do not create the next batch during this closeout slice.
- Do not update GitHub issues or comments unless explicitly requested.
- Do not run live downstream project validations.

Acceptance criteria:
- All three consumer skills route supported history/reporting questions through
  planning-state projection reports before broad historical scans when policy
  permits.
- Tests protect the consumer-facing obligation and dependency assumptions.
- Feature versions and changelog entries are aligned with touched workflow
  surfaces.
- Final hard-coding checks find no downstream project defaults introduced by
  this batch.
- PST-16 and PST-17 are closed only with completed validation, review, and
  closeout evidence.

Validation:
- Use the selected docs-only profile plus final commands:
  `python -m pytest tests/test_planning_state_consumer_projection_routing.py tests/test_codex_features_manifest.py tests/test_architecture_program_runner_protocol.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/batch-runway skills/architecture-program-runway skills/legacy-removal tests/test_planning_state_consumer_projection_routing.py` should report no new matches from the batch.
  `git diff --check`

Test quality review:
- Route to test quality review only if the new tests are broad enough that
  assertion strength is uncertain.

Commit message:
- `Close planning state projection consumers`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, cross-consumer consistency, final metadata
  alignment, closeout evidence pointers, and no premature next-batch selection.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if a consumer skill lacks projection-report routing after earlier
  slices.
- Stop if version/changelog metadata cannot be aligned with the touched
  workflow behavior.
- Stop if closeout evidence is missing or points to unreviewed work.
