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
