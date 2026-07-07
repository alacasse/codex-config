# Command Owner Skill Migration Completed Slices

## Slice 1. Add Command-Owner Skill Surfaces

Status: completed; commit `fdaf2cf`.

Files:
- `skills/add-to-ledger/`
- `skills/plan-batch/`
- `skills/work-batch/`
- `codex-features.json`
- `tests/test_codex_features_manifest.py`

Validation:
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python -m pytest tests/test_codex_features_manifest.py -q`
- `git diff --check`

Review: approved by `runway_reviewer`; no required fixes.

Notes:
- The new command-owner skills are direct user-facing surfaces.
- Existing runtime skills remain available.
- Copy-first bridge wording is intentionally bounded for later migration.

## Slice 2. Tighten Support-Skill Boundaries

Status: completed; commit `43118fc`.

Files:
- `skills/test-quality-review/SKILL.md`
- `skills/work-batch/SKILL.md`
- `skills/legacy-removal/SKILL.md`
- `skills/dead-surface-audit/SKILL.md`
- `skills/batch-runway/references/subagent-briefs.md`
- `tests/test_planning_state_consumer_projection_routing.py`

Validation:
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q`
- `git diff --check`

Review: approved by `runway_reviewer`; no required fixes.

Support review:
- `test-quality-review` delta-only support was clean after whitespace-tolerant
  wording assertions replaced brittle Markdown line-wrap checks.

Notes:
- Test-quality review is explicitly review support, while still directly
  requestable for focused audits.
- Preventive legacy control is a normal implementation/review obligation.
- Legacy/dead-surface support remains available for exceptional residue
  investigations without adding a human-facing cleanup command.

## Slice 3. Reconcile Catalog And Migration State

Status: completed; commit `0e45abe`.

Files:
- `README.md`
- `CHANGELOG.md`
- `codex-features.json`
- `tests/test_codex_features_manifest.py`
- `docs/plans/programs/planning-state-tooling/CURRENT.md`
- `docs/plans/programs/planning-state-tooling/LEDGER.md`
- `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/runway.md`
- `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/completed-slices.md`
- `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`

Validation:
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python -m pytest tests/test_codex_features_manifest.py -q`
- `git diff --check`

Review: approved by `runway_reviewer`; no required fixes.

Notes:
- README and manifest metadata now distinguish the direct command-owner skills
  from agent-facing support and current runtime workflow surfaces.
- PST-26 through PST-29 are closed in the program ledger.
- No successor planning-state-tooling batch is selected.
