# Command Owner Skill Migration Completed Slices

## Slice 1. Add Command-Owner Skill Surfaces

Status: completed; commit pending.

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

Status: completed; commit pending.

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
