# Planning-State Projection Language And Migration Runway

## Purpose

Clarify that projection-backed reporting is the policy-gated normal workflow for
supported planning history/reporting questions, then provide a reusable adoption
checklist for existing Layout v1 ledger roots. The batch should remove wording
that makes SQLite reporting sound merely theoretical or "not yet", without
changing the real architecture: Markdown and JSON remain canonical, SQLite is
rebuildable, active-state pickup stays SQLite-independent, and agents consume
commands rather than SQL.

This spec executes the
`planning-state-projection-language-and-migration` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/dispatch.md`.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans --format json`
  and
  `python scripts/planning_state.py validate --root docs/plans --format json`.
- Planning root: `docs/plans/`.
- Program: `planning-state-tooling`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/dispatch.md`.
- Included findings: PST-20 and PST-21.
- No planning-state-tooling batch was selected, queued, or active before this
  batch was materialized.
- Project policy currently resolves to `state_file_policy: generated-only`,
  `projection_policy: generated-only`, `projection_usage: caller-directed`, and
  `projection_rebuild_authority: command`; generated-only projection reporting
  therefore needs an explicit caller-provided temporary target.
- The implementation already exposes `rebuild-projection` and
  `report-projection`, forbids direct SQLite querying in workflow guidance, and
  keeps `current` and `validate` independent of SQLite.
- The remaining gap is agent-facing adoption: some language still describes
  projection reporting as "optional" in a way that fresh agents can interpret
  as "not part of the normal workflow", and there is no reusable migration
  checklist for existing ledger roots.

## Assumptions

- Planning State owns projection policy, projection command/report guidance,
  target-policy checks, and reusable migration/adoption docs.
- Consumer workflow skills own their semantic decisions, but should use
  policy-compatible projection reports before broad historical scans for
  supported report types.
- Project instructions or overlays own durable projection paths and downstream
  validation commands.
- Workflow doc and skill behavior changes should keep `CHANGELOG.md` and
  `codex-features.json` aligned when installed surfaces change.

## Non-Goals

- Do not make SQLite canonical planning state.
- Do not require SQLite for `current`, `validate`, active-state pickup, batch
  allocation, transition commands, or closeout validation.
- Do not add a committed or reusable default database path.
- Do not expose SQL, table names, or direct SQLite queries as an agent workflow
  contract.
- Do not rewrite project-specific downstream overlays or planning roots.
- Do not run live downstream project validation unless a slice explicitly
  assigns a bounded fixture or dry-run proof.
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
- Use `lean-runway` density because this batch is workflow wording,
  docs-as-code, fixture, and planning-migration guidance.
- Workers must not write durable JSON planning state, durable SQLite
  projections, runner artifacts, downstream project planning roots, or installed
  `~/.codex` paths.
- Any temporary projection smoke must use an explicit `/tmp` target supplied by
  the execution coordinator and must be removed or left as disposable temp
  evidence only.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- Projection wording and consumer obligations:
  `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`
- Planning-state command/policy behavior, if fixture tests are changed:
  `python -m pytest tests/test_planning_state.py -q`
- Manifest checks, if feature metadata changes:
  `python -m pytest tests/test_codex_features_manifest.py -q`
- Planning-state diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Optional generated-only projection smoke when a slice changes projection
  routing or adoption guidance:
  `python scripts/planning_state.py rebuild-projection --root docs/plans --database /tmp/planning-state-projection-language-and-migration.sqlite`
  `python scripts/planning_state.py report-projection --root docs/plans --database /tmp/planning-state-projection-language-and-migration.sqlite --report pending-batches`
- Hard-coding check:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/planning-state skills/batch-runway skills/architecture-program-runway skills/legacy-removal tests docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- No committed SQLite database or durable JSON state file is required.

Harness output:
- `current` and `validate` checks should write no live planning files.
- Projection smoke, when used, writes only to an explicit `/tmp` database.
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
| 1. Tighten projection language | Closed | this commit | `consumer_projection_routing.py` 11 passed; `current`; `validate`; `git diff --check` | Clean review after stale-block fix loop | Checklist and fixture adoption proof remain. | Projection reporting is now described as the policy-gated normal route for supported reports while preserving SQLite-independent active-state pickup. |
| 2. Add adoption checklist and fixtures | Closed | this commit | `test_planning_state.py` 176 passed; `current`; `validate`; `git diff --check` | Clean review | Metadata, changelog, current/ledger, closeout evidence remain. | Adoption checklist and portable Layout v1 fixture tests cover generated-only temp targets and ignored-local declared projection paths without downstream defaults. |
| 3. Reconcile metadata and closeout evidence | Pending |  |  |  | Manifest/changelog/current/ledger state is aligned and closeout is pointer-first. | Do not select a successor batch. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Tighten projection language | this commit | Planning State, Batch Runway, Architecture Program Runway, and Legacy Removal now route supported history/reporting questions through policy-compatible `report-projection` command output as the normal pre-scan route, with explicit fallback/blocker handling and direct-SQL guards. | Validation: `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`, `python scripts/planning_state.py current --root docs/plans`, `python scripts/planning_state.py validate --root docs/plans`, `git diff --check`; review: clean `runway_reviewer` result after required stale-block fixes. |
| 2. Add adoption checklist and fixtures | this commit | Added a reusable Layout v1 projection-reporting adoption checklist plus portable command-level fixture coverage for generated-only and ignored-local projection policy routing. | Validation: `python -m pytest tests/test_planning_state.py -q`, `python scripts/planning_state.py current --root docs/plans`, `python scripts/planning_state.py validate --root docs/plans`, `git diff --check`; review: clean `runway_reviewer` result against the Slice 2 diff. |

## Slice 1. Tighten Projection Language

Scope:
- Update Planning State and consumer workflow guidance so supported
  history/reporting questions use policy-compatible projection reports as the
  normal route before broad historical scans.
- Replace ambiguous "optional" wording only where it implies projection reports
  are not operationally expected when `projection_usage` and
  `projection_rebuild_authority` allow them.
- Preserve explicit guardrails: SQLite is rebuildable, not canonical, not
  directly queried, not a generic durable default, and not required for
  active-state pickup.
- Add or adjust focused wording tests for these obligations.

Allowed files/areas:
- `skills/planning-state/SKILL.md`
- `skills/planning-state/references/projection-reporting.md`
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/create-spec.md`
- `skills/batch-runway/references/execute-spec.md`
- `skills/batch-runway/references/finalize-batch-v1.md`
- `skills/architecture-program-runway/SKILL.md`
- `skills/architecture-program-runway/references/program-ledger-template.md`
- `skills/architecture-program-runway/references/goal-runner-v1.md`
- `skills/architecture-program-runway/references/local-runner-v1.md`
- `skills/legacy-removal/SKILL.md`
- `tests/test_planning_state_consumer_projection_routing.py`
- This spec active-ledger/archive rows

Non-goals:
- Do not change `scripts/planning_state.py` command semantics in this slice.
- Do not introduce SQL/table-name guidance.
- Do not add downstream project paths or validation commands.

Acceptance criteria:
- `current` and `validate` remain documented as the active-state hot path and
  do not require SQLite.
- Projection-backed reporting is described as the policy-gated normal route for
  supported history/reporting questions before broad historical scans.
- Workflow guidance tells agents to consume command output, not SQLite directly.
- Tests fail if the consumer guidance loses `projection_usage`,
  `projection_rebuild_authority`, `report-projection`, or the broad-scan
  fallback guard.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None unless tests become broad snapshots or assertion-light wording scans.

Commit message:
- `Clarify projection reporting language`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, the projection-reporting wording boundary, and
  absence of direct SQL guidance or project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the wording makes SQLite canonical or required for active-state
  pickup.
- Stop if the wording makes broad historical scans impossible when projection
  policy is missing, stale, or incompatible and an explicit fallback decision is
  recorded.

## Slice 2. Add Adoption Checklist And Fixtures

Scope:
- Add a reusable migration/adoption checklist for projects already using Layout
  v1 ledger/batching workflows.
- Cover root/program `CURRENT.md` files, program ledgers, batch queues,
  redirect ledgers, consumer skills, installed-skill state, project overlays,
  generated-only temp targets, ignored-local projection targets, and command-only
  rebuild/report usage.
- Add or extend fixture coverage so at least one non-codex-config Layout v1
  root shape proves generated-only and ignored-local projection routing without
  hard-coded downstream paths.

Allowed files/areas:
- `skills/planning-state/references/projection-reporting.md`
- `skills/planning-state/references/target-policy.md`
- `skills/planning-state/references/state-fixtures.md`
- `tests/test_planning_state.py`
- `tests/fixtures/` or existing planning-state fixture areas, if present
- This spec active-ledger/archive rows

Non-goals:
- Do not migrate a live downstream project.
- Do not commit generated projection databases.
- Do not add project-specific validation commands to reusable skills.

Acceptance criteria:
- The checklist is usable by any Layout v1 project that declares planning root
  and projection policy.
- Generated-only projects require explicit temp projection targets.
- Ignored-local projects can declare durable local projection paths through
  project policy or overlays.
- Fixture tests prove policy routing without using downstream project paths.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- Request test-quality review if fixture additions become broad or duplicate
  production parser behavior.

Commit message:
- `Document projection adoption migration`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, fixture portability, and absence of downstream path
  hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the checklist requires a live downstream root to validate.
- Stop if ignored-local examples become generic defaults.
- Stop if generated-only policy silently chooses a durable database path.

## Slice 3. Reconcile Metadata And Closeout Evidence

Scope:
- Align `CHANGELOG.md` and `codex-features.json` for meaningful workflow/skill
  behavior changes from Slices 1 and 2.
- Reconcile `docs/plans/programs/planning-state-tooling/CURRENT.md` and
  `LEDGER.md` for queued/active/completed state during execution.
- Create pointer-first closeout evidence and completed-slice archive when the
  batch completes.
- Run a generated-only `/tmp` rebuild/report smoke if projection guidance or
  fixture changes need end-to-end proof.

Allowed files/areas:
- `CHANGELOG.md`
- `codex-features.json`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/`
- Test files touched by earlier slices only for targeted reconciliation

Non-goals:
- Do not select a successor batch.
- Do not write durable JSON state or committed SQLite projection files.
- Do not edit GitHub issues or comments.

Acceptance criteria:
- Feature metadata and changelog reflect behavior-changing reusable skill edits.
- Planning diagnostics pass with no active-state contradictions.
- Closeout evidence is pointer-first and bounded.
- Final hard-coding and `git diff --check` validations pass.

Validation:
- Use the selected docs-only profile plus focused commands:
  `python -m pytest tests/test_planning_state_consumer_projection_routing.py tests/test_planning_state.py tests/test_codex_features_manifest.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  optional `/tmp` rebuild/report smoke if projection behavior changed
  `git diff --check`

Test quality review:
- None unless this slice materially changes test structure.

Commit message:
- `Close projection language migration batch`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, closeout evidence, metadata alignment, and absence
  of selected successor batch.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if final validation needs a live downstream project.
- Stop if the closeout would include long logs instead of bounded pointers.
- Stop if the batch would leave multiple active artifacts in `CURRENT.md`.

## Final Validation

Run:

```bash
python -m pytest tests/test_planning_state_consumer_projection_routing.py tests/test_planning_state.py tests/test_codex_features_manifest.py -q
python scripts/planning_state.py current --root docs/plans
python scripts/planning_state.py validate --root docs/plans
git diff --check
```

Run the generated-only `/tmp` projection smoke when the final diff changes
projection behavior or adoption guidance in a way that needs command-level
proof:

```bash
python scripts/planning_state.py rebuild-projection --root docs/plans --database /tmp/planning-state-projection-language-and-migration.sqlite
python scripts/planning_state.py report-projection --root docs/plans --database /tmp/planning-state-projection-language-and-migration.sqlite --report pending-batches
```

## Stop Conditions

- Stop if any slice would make SQLite canonical planning state.
- Stop if any slice would make active-state pickup depend on SQLite.
- Stop if any slice would expose direct SQL/table names as workflow guidance.
- Stop if any slice would choose a durable projection path without explicit
  project policy.
- Stop if any slice would hard-code downstream project paths, cache locations,
  validation commands, or overlays into reusable skills.
- Stop if `current` or `validate` reports multiple active artifacts.
