# Planning-State Projection Language And Migration Closeout

## Status

- Batch: `planning-state-projection-language-and-migration`
- Status: completed
- Findings closed: PST-20, PST-21
- Dispatch: `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/dispatch.md`
- Runway: `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/runway.md`
- Completed slices: `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/completed-slices.md`

## Evidence Pointers

- Slice 1 commit: `5471b4a` (`Clarify projection reporting language`)
- Slice 2 commit: `b6d01cb` (`Document projection adoption migration`)
- Slice 3 commit: this closeout commit
- Slice 1 validation: `python -m pytest tests/test_planning_state_consumer_projection_routing.py -q` passed with 11 tests; `current`; `validate`; `git diff --check`
- Slice 2 validation: `python -m pytest tests/test_planning_state.py -q` passed with 176 tests; `current`; `validate`; `git diff --check`
- Pre-closeout final validation: `python -m pytest tests/test_planning_state_consumer_projection_routing.py tests/test_planning_state.py tests/test_codex_features_manifest.py -q` passed with 193 tests; `current`; `validate`; `git diff --check`
- Pre-closeout generated-only projection smoke: `rebuild-projection --root docs/plans --database /tmp/planning-state-projection-language-and-migration.sqlite` passed; `report-projection --report pending-batches` passed with 1 row for this queued batch before closeout.
- Post-closeout generated-only projection smoke: after `CURRENT.md` and `LEDGER.md` closeout reconciliation, `report-projection --root docs/plans --database /tmp/planning-state-projection-language-and-migration.sqlite --report pending-batches` passed with 0 rows.

## Outcome

- Projection-backed reporting is described as the policy-gated normal route for supported history/reporting questions when `projection_usage` and `projection_rebuild_authority` allow it.
- `current` and `validate` remain SQLite-independent active-state checks.
- Agents consume `rebuild-projection` and `report-projection` command output, not direct SQL or table names.
- Layout v1 adoption guidance covers generated-only temporary targets and ignored-local declared projection paths without downstream path defaults.
- `CHANGELOG.md`, `codex-features.json`, `CURRENT.md`, and `LEDGER.md` are aligned for closeout.

## Cleanup Residue

- No durable JSON state file was written.
- No committed SQLite projection file was written.
- No successor planning-state-tooling batch was selected.
