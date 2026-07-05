# Planning-State Projection Routing Runway

## Purpose

Make projection reporting a first-class part of the `planning-state` agent
interface for history/reporting questions. The batch should let agents know
when to try projection reports before broad Markdown archaeology while keeping
`current` and `validate` independent of SQLite for active-state correctness.

This spec executes the `planning-state-projection-routing` batch described by
`docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/dispatch.md`.

## Current Baseline

- Baseline state: `python scripts/planning_state.py current --root docs/plans`
  and `python scripts/planning_state.py validate --root docs/plans` pass with
  only existing architecture-runner redirect warnings.
- Planning root: `docs/plans/`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/dispatch.md`.
- Included findings: PST-14 and PST-15.
- Existing owner seam: `scripts/planning_state.py`.
- Agent interface seam: `skills/planning-state/SKILL.md` plus focused
  references under `skills/planning-state/references/`.
- Existing focused tests: `tests/test_planning_state.py`.
- Existing commands can rebuild explicit SQLite projections and report pending
  batches, missing closeout evidence, batch evidence, and runner-artifact
  summaries when callers provide policy-compatible targets.

## Assumptions

- Active-state pickup remains file-first: `current` and `validate` read Layout
  v1 Markdown and explicit JSON state without requiring SQLite.
- Projection reports are appropriate for history/reporting questions only when
  project policy declares compatible projection usage and rebuild authority.
- Project policy needs vocabulary for expected projection use, not only where a
  database may be written.
- Agents should consume compact command output and skill routing rules. They
  should not query SQLite directly, infer stale projection state manually, or
  scrape historical planning filenames as a default workflow.
- Fixture coverage should stay project-neutral. Downstream paths, cache
  locations, package commands, and local overlays must not become reusable
  defaults.

## Non-Goals

- Do not make SQLite required for `current`, `validate`, `bootstrap-state`,
  `select-batch`, `queue-batch`, `validate-closeout`, or `render-closeout`.
- Do not store full Markdown prose, dispatch/runway bodies, prompts,
  transcripts, long logs, or raw telemetry blobs in SQLite.
- Do not render or rewrite `CURRENT.md`, `LEDGER.md`, `dispatch.md`,
  `runway.md`, `closeout.md`, or `completed-slices.md` from SQLite.
- Do not rewire Batch Runway, Architecture Program Runway, or Legacy Removal
  consumers in this batch; that is `planning-state-projection-consumers`.
- Do not create a durable projection database for this repo.
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
- Use `full-runway` density because this batch changes policy vocabulary,
  command-facing diagnostic semantics, and reusable skill routing.
- Workers must use temp fixtures for projection-policy tests unless a slice
  explicitly updates this batch's planning docs for ledger closeout.
- Workers must not write to downstream project planning roots.
- Workers must not create a committed durable SQLite database.
- Workers must not rewire consumer skills in this batch.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/project-harness-production.md`

Focused validation commands:
- For production/test slices:
  `python -m pytest tests/test_planning_state.py -q`
- For skill/reference slices:
  `rg -n "projection|projection usage|rebuild authority|report-projection|Planning State Diagnostic" skills/planning-state scripts/planning_state.py tests/test_planning_state.py`
- For hard-coding checks, the final diff should not introduce matches:
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/planning-state scripts/planning_state.py tests/test_planning_state.py`
- For repo diagnostics:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
- Run ruff on touched Python files when production or test Python changes:
  `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check <touched production/test files>`
- Always run `git diff --check`.

Integration harness:
- No nested Codex runs.
- No live downstream project validation.
- Projection smoke tests must use explicit `/tmp` or test temp targets unless a
  fixture declares another policy-compatible target.
- Include CLI smoke for projection reports only after a projection has been
  rebuilt from a compatible state fixture.

Harness output:
- Existing `current` and `validate` checks should write no live planning files.
- Projection tests should write SQLite databases only to test temp directories
  or explicit caller-provided paths allowed by resolved project policy.

Summary artifact:
- No generated summary artifact is required. Report compact stdout/stderr
  signals from validation commands and any temp projection paths used.

Index refresh:
- None required for this repo after these Python/test/docs edits.

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
| None | Archived |  |  |  | None | All intended slices are archived below; no pending active rows remain. |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Add projection usage policy | `bdc070a` | success; project policy now exposes projection usage and rebuild authority separately from projection target ownership while preserving backward-compatible defaults | `python -m pytest tests/test_planning_state.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py`; `git diff --check`; runway_reviewer approved current diff |
| 2. Route planning-state projection guidance | `0e5bab9` | success; planning-state skill guidance now routes supported history/reporting questions through policy-compatible projection reports while keeping `current` and `validate` SQLite-free | `rg` projection wording check; hard-coding `rg` check; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `git diff --check`; runway_reviewer approved current diff |
| 3. Surface projection-routing diagnostics | `f55d013` | success; `current` and `validate` now surface additive `projection_routing` facts without requiring SQLite, and disabled projection usage keeps projection targets blocked | `python -m pytest tests/test_planning_state.py -q`; `python scripts/planning_state.py current --root docs/plans`; `python scripts/planning_state.py validate --root docs/plans`; `python scripts/planning_state.py current --root docs/plans --format json`; `/tmp` rebuild/report projection smoke; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py`; `git diff --check`; runway_reviewer approved fixed diff |
| 4. Close projection-routing batch | pending commit | success; PST-14 and PST-15 are closed, the program queue is cleared, latest closeout points to this batch, and PST-16/PST-17 remain open for `planning-state-projection-consumers` | Final validation evidence: `current` and `validate` passed with existing redirect warning and `projection_routing`; `python -m pytest tests/test_planning_state.py -q` passed 174; `uvx ruff check scripts/planning_state.py tests/test_planning_state.py` passed with existing Python symlink warning; closed-state `/tmp` rebuild/report projection smoke passed with no pending rows; `git diff --check` clean | coordinator review pending | Commit this docs-only closeout slice | No GitHub updates; no next batch created. |

## Slice 1. Add Projection Usage Policy

Scope:
- Extend project-policy parsing and validation with explicit projection usage
  and rebuild-authority vocabulary.
- Keep existing `projection_policy` and `projection_path` semantics for write
  target ownership.
- Add tests for generated-only, ignored-local, external, and none-style policy
  combinations that prove usage expectations are separate from target paths.
- Prefer compact names such as `projection_usage` and
  `projection_rebuild_authority` if they fit existing policy shape.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- Focused planning-state protocol docs if needed
- This spec ledger/archive rows
- `CHANGELOG.md` if user-facing command behavior changes

Non-goals:
- Do not add consumer-skill rules in this slice.
- Do not change projection table schema unless policy metadata requires a small
  source-identity field.
- Do not create or commit a durable database.

Acceptance criteria:
- Policy parsing exposes whether projection reports are expected, optional,
  disabled, or caller-directed.
- Rebuild authority is explicit enough to distinguish no rebuild, ask-first,
  command-authorized, and external-owner cases.
- Invalid combinations produce stable validation errors or blockers.
- Existing roots without the new fields remain compatible through clear
  defaults that do not imply a durable projection target.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`
- Run ruff on touched Python files.

Test quality review:
- Route to test quality review only if the slice adds broad fixture builders or
  heavy mocking around policy parsing.

Commit message:
- `Add planning state projection usage policy`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, policy vocabulary clarity, backward
  compatibility, invalid-combination handling, and absence of durable target
  defaults.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the policy vocabulary cannot preserve existing generated-only roots.
- Stop if the change would choose a project-specific projection path.

## Slice 2. Route Planning-State Projection Guidance

Scope:
- Update `skills/planning-state/SKILL.md` and focused references so agents know
  when history/reporting questions should use projection reports before broad
  historical scans.
- Clarify that `current` and `validate` remain the routine active-state hot
  path and never require SQLite.
- Update target-policy or projection-reporting references to describe the new
  usage/rebuild-authority fields.
- Keep `planning-artifacts` as the owner for Layout v1 placement.

Allowed files/areas:
- `skills/planning-state/SKILL.md`
- `skills/planning-state/references/target-policy.md`
- `skills/planning-state/references/projection-reporting.md`
- This spec ledger/archive rows
- `CHANGELOG.md` if the workflow surface changes

Non-goals:
- Do not update Batch Runway, Architecture Program Runway, or Legacy Removal
  consumer rules in this slice.
- Do not repeat the full projection schema in the skill entrypoint.
- Do not add downstream project examples as generic defaults.

Acceptance criteria:
- A fresh planning-state agent can distinguish active-state pickup from
  projection-backed history/reporting.
- The guidance names policy-compatible projection usage and rebuild authority
  as prerequisites before rebuilding or reporting.
- Missing or incompatible projection policy causes a bounded stop/blocker, not
  a silent broad scan.
- The entrypoint remains compact and uses progressive disclosure.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `rg -n "projection|report-projection|rebuild-projection|projection_usage|projection_rebuild" skills/planning-state`
  `rg -n "/home/alacasse/projects/graphify|my-docs/plans|codex-config-uv-cache|Graphify-specific|project-specific validation" skills/planning-state` should produce no matches from the slice diff.
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `git diff --check`

Test quality review:
- None; this is a workflow-doc slice unless production tests change.

Commit message:
- `Document projection-aware planning state routing`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, active-state versus projection routing clarity,
  progressive disclosure, and absence of project-specific hard-coding.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if the skill would imply SQLite is required for active-state pickup.
- Stop if the guidance would duplicate consumer-owned semantic decisions.

## Slice 3. Surface Projection-Routing Diagnostics

Scope:
- Expose compact projection-routing facts, warnings, or blockers through the
  planning-state diagnostic surface or a focused policy-check path.
- Ensure agents can see whether projection reports are unavailable, optional,
  expected, stale, or policy-incompatible before falling back to broader reads.
- Add CLI smoke coverage for generated-only and ignored-local/temp projection
  scenarios.
- Keep projection rebuild/report commands behind explicit caller-provided
  targets.

Allowed files/areas:
- `scripts/planning_state.py`
- `tests/test_planning_state.py`
- `skills/planning-state/references/projection-reporting.md` if command output
  needs documentation
- This spec ledger/archive rows
- `CHANGELOG.md` if command output changes

Non-goals:
- Do not make `current` or `validate` rebuild projections automatically.
- Do not query SQL from agents or expose raw SQL as the routine interface.
- Do not add project-specific fixture paths.

Acceptance criteria:
- `current`/`validate` remain usable without projection state.
- Projection-aware output gives bounded facts or blockers for history/reporting
  workflows.
- Stale or mismatched projections are rejected before reports are trusted.
- Tests cover policy-compatible and policy-incompatible routing without writing
  durable repo databases.

Validation:
- Use the selected project-harness-production profile.
- Focused commands:
  `python -m pytest tests/test_planning_state.py -q`
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  Temp-fixture `rebuild-projection` plus `report-projection` smoke for at least
  one supported report.
  `git diff --check`
- Run ruff on touched Python files.

Test quality review:
- Route to test quality review if projection-routing fixtures become broad or
  assertion-light.

Commit message:
- `Surface projection routing diagnostics`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, diagnostic output stability, projection routing
  safety, stale-projection rejection, and no automatic rebuild side effects.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if routing diagnostics require automatic projection rebuilds.
- Stop if output shape would break existing `current --format json` or
  `validate --format json` consumers without a compatibility plan.

## Slice 4. Close Projection-Routing Batch

Scope:
- Update `docs/plans/programs/planning-state-tooling/LEDGER.md` to close
  PST-14 and PST-15 when prior slices have validation and review evidence.
- Update `docs/plans/programs/planning-state-tooling/CURRENT.md` so no
  planning-state-tooling batch remains selected, active, or queued after
  closeout.
- Create bounded pointer-first closeout evidence at
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/closeout.md`.
- Update `CHANGELOG.md` and feature metadata only if earlier slices changed
  user-facing workflow behavior or install dependencies.

Allowed files/areas:
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/closeout.md`
- `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/runway.md`
- `CHANGELOG.md` if needed
- `codex-features.json` only if dependency metadata changes

Non-goals:
- Do not close PST-16 or PST-17 in this batch.
- Do not create the next consumer batch.
- Do not update GitHub issues or comments.

Acceptance criteria:
- Closeout evidence points to commits, validation, reviews, policy behavior,
  projection smoke, and cleanup residue status without embedding long logs.
- PST-14 and PST-15 are closed only if the new interface and policy behavior
  are implemented and reviewed.
- The next ledger recommendation remains
  `planning-state-projection-consumers`.
- Planning state diagnostics pass after queue closure.

Validation:
- Use the selected project-harness-production profile.
- Final commands:
  `python scripts/planning_state.py current --root docs/plans`
  `python scripts/planning_state.py validate --root docs/plans`
  `python -m pytest tests/test_planning_state.py -q`
  Projection rebuild/report smoke using explicit `/tmp` targets.
  `git diff --check`
- Run ruff on touched Python files if any Python changed in the closeout commit.

Test quality review:
- None for docs-only closeout unless tests change in this slice.

Commit message:
- `Close planning state projection routing`

Coding subagent brief:
- Implement only Slice 4 from this spec after Slices 1-3 are committed.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, closeout evidence completeness, ledger accuracy,
  and final active-state consistency.
- Echo the coordinator-provided `diff_basis` in compact YAML output.
- Do not modify files.

Stop conditions:
- Stop if any prior slice lacks validation or review evidence.
- Stop if closeout would need to mark PST-16/PST-17 closed before consumer
  rewiring exists.

## Final Validation

Run after the last implementation slice and before final closeout:

- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python -m pytest tests/test_planning_state.py -q`
- Projection rebuild/report smoke using explicit `/tmp` targets and a
  policy-compatible fixture.
- `git diff --check`
- Ruff on touched Python files.

## Stop Conditions

- Stop if projection routing would make SQLite canonical or required for
  active-state correctness.
- Stop if a universal durable projection path is required.
- Stop if the batch would need downstream project-specific paths, validation
  commands, cache paths, issue policy, or local overlays in reusable code.
- Stop if consumer skill projection rewiring is needed before the planning-state
  interface is explicit.
- Stop if a selected dispatch, active runway, or queued batch appears outside
  this batch before execution begins.
