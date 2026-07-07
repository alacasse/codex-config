# Command Owner Skill Migration Runway

## Purpose

Create the first copy-first migration batch for the human-facing command-owner
skill surface accepted in ADR 0002. This batch should add `add-to-ledger`,
`plan-batch`, and `work-batch` beside the existing runtime skills, prove the
new names through validation and docs, and keep agent-facing support skills
narrow.

This spec executes the `command-owner-skill-migration` batch described by
`docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/dispatch.md`.

## Current Baseline

- Baseline diagnostics pass:
  `python scripts/planning_state.py current --root docs/plans`
  and
  `python scripts/planning_state.py validate --root docs/plans`.
- Decision record:
  `docs/adr/0002-human-facing-command-owner-skills.md`.
- Source program ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Dispatch packet:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/dispatch.md`.
- Included findings: PST-26, PST-27, PST-28, and PST-29.
- Existing runtime skills remain installed and must not be removed in this
  batch.

## Assumptions

- The user-facing command set is `add-to-ledger`, `plan-batch`, `work-batch`,
  and `port-by-contract`.
- `add-to-ledger` owns ledger intake.
- `plan-batch` owns selecting bounded ledger work when needed and writing one
  concrete batch spec.
- `work-batch` owns executing the current planned batch.
- Support skills are allowed behind these commands only when they have narrow,
  reusable jobs.
- Preventive legacy control is a default implementation/review obligation, not
  a normal human-facing cleanup command.
- Test-quality review is primarily agent-facing review support, while still
  directly requestable for focused audits.

## Non-Goals

- Do not remove, rename, or archive `architecture-program-runway`,
  `batch-runway`, `legacy-removal`, or `dead-surface-audit` in this first batch.
- Do not create GitHub issues or comments.
- Do not add durable JSON state, SQLite projections, runner artifacts, or
  generated reports.
- Do not run downstream project validation.

## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execute-slice-core-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execution-contract-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/reporting-contracts-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/ledger-retention-v1.md`

Overrides:
- Use `lean-runway` density.
- Keep implementation copy-first: add new command-owner skills beside existing
  runtime skills before changing or retiring old names.
- Do not preserve old runtime names inside the new command-owner skill bodies
  except where temporary migration routing is explicit and bounded.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/docs-only.md`

Focused validation commands:
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python -m pytest tests/test_codex_features_manifest.py -q` when manifest
  metadata changes.
- Focused skill wording tests for command-owner names, support-skill
  boundaries, and absence of user-facing legacy cleanup commands.
- `git diff --check`

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1. Add command-owner skill surfaces | Completed | `fdaf2cf` | `current` passed; `validate` passed; manifest tests passed; `git diff --check` passed | Approved; no required fixes | Slice archived in `completed-slices.md`. |
| 2. Tighten support-skill boundaries | Completed | `43118fc` | `current` passed; `validate` passed; wording tests passed; `git diff --check` passed | Approved; no required fixes | Slice archived in `completed-slices.md`. |
| 3. Reconcile catalog and migration state | Completed | `0e45abe` | `current` passed; `validate` passed; manifest tests passed; `git diff --check` passed | Approved; no required fixes | Slice archived in `completed-slices.md`; batch closeout written. |

## Slice 1. Add Command-Owner Skill Surfaces

Scope:
- Add new repo-owned skills for `add-to-ledger`, `plan-batch`, and
  `work-batch`.
- Keep each `SKILL.md` short, verb-led, and focused on direct user intent.
- Add install metadata and UI metadata when required by the repo's current
  feature model.
- Route to existing runtime procedures only as an explicit copy-first migration
  bridge.

Allowed files/areas:
- `skills/add-to-ledger/`
- `skills/plan-batch/`
- `skills/work-batch/`
- `codex-features.json`
- Skill metadata/tests required for manifest validation
- This spec active-ledger/archive rows

Acceptance criteria:
- The three new skill names are directly invokable by the user.
- The new skill bodies state what they own and where they stop.
- Existing runtime skills remain available.

Validation:
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python -m pytest tests/test_codex_features_manifest.py -q`
- `git diff --check`

Commit message:
- `Add command-owner skill surfaces`

## Slice 2. Tighten Support-Skill Boundaries

Scope:
- Clarify test-quality review as review support rather than a primary human
  planning command.
- Clarify preventive legacy control as a default workflow obligation in normal
  implementation/review paths.
- Keep existing legacy cleanup and dead-surface evidence machinery available
  for exceptional residue investigations without advertising a normal cleanup
  ritual.

Allowed files/areas:
- `skills/test-quality-review/`
- `skills/batch-runway/`
- `skills/legacy-removal/`
- `skills/dead-surface-audit/`
- New command-owner skills when their support-boundary wording needs alignment
- Focused wording tests
- This spec active-ledger/archive rows

Acceptance criteria:
- Changed-test workflows route test-quality checks through review support.
- Work-batch/review guidance rejects unsupported legacy preservation by
  default.
- No new human-facing legacy cleanup command is introduced.

Validation:
- Focused wording tests for the support-skill obligations.
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `git diff --check`

Commit message:
- `Clarify support skill boundaries`

## Slice 3. Reconcile Catalog And Migration State

Scope:
- Update README/catalog language so the user-facing command set is clear.
- Keep old runtime skill names described as current migration internals or
  existing workflow surfaces, not the target user interface.
- Update `CHANGELOG.md`, manifest tests, planning-state ledger/current state,
  closeout, and completed-slices evidence.

Allowed files/areas:
- `README.md`
- `CHANGELOG.md`
- `codex-features.json`
- `tests/`
- `docs/plans/programs/planning-state-tooling/`
- This spec active-ledger/archive rows

Acceptance criteria:
- The repo explains which skills are user-facing and which are agent-facing.
- The queued batch closes with pointer-first evidence.
- No successor batch is selected unless explicitly requested.

Validation:
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python -m pytest tests/test_codex_features_manifest.py -q`
- `git diff --check`

Commit message:
- `Reconcile command skill migration`
