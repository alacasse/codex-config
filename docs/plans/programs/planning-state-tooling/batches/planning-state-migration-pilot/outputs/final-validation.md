# Final Validation: planning-state-migration-pilot

Validation commands:

- `python -m pytest tests/test_planning_state.py -q`
- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`
- `python scripts/planning_state.py bootstrap-state --root docs/plans --program planning-state-tooling --state-file /tmp/codex-config-bootstrap-state-final.json --format json`
- `python scripts/planning_state.py validate --root docs/plans --state-file /tmp/codex-config-bootstrap-state-final.json --format json`
- `python scripts/planning_state.py current --root docs/plans --state-file /tmp/codex-config-bootstrap-state-final.json --format json`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check CHANGELOG.md scripts/planning_state.py tests/test_planning_state.py`
- `python scripts/planning_state.py validate-closeout --root docs/plans --program planning-state-tooling --batch-id planning-state-migration-pilot --closeout docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/closeout.md --state-file /tmp/planning-state-migration-pilot-closeout-state.json`
- `git diff --check`

Observed results:

- `python -m pytest tests/test_planning_state.py -q`: passed, `117 passed`.
- `python scripts/planning_state.py current --root docs/plans`: passed with the
  known redirect ledger warning for old flat ledger redirects.
- `python scripts/planning_state.py validate --root docs/plans`: passed with
  the known redirect ledger warning for old flat ledger redirects.
- `python scripts/planning_state.py bootstrap-state --root docs/plans --program planning-state-tooling --state-file /tmp/codex-config-bootstrap-state-final.json --format json`:
  passed and wrote only the explicit `/tmp` state-file target.
- `python scripts/planning_state.py validate --root docs/plans --state-file /tmp/codex-config-bootstrap-state-final.json --format json`:
  passed with the known redirect ledger warning.
- `python scripts/planning_state.py current --root docs/plans --state-file /tmp/codex-config-bootstrap-state-final.json --format json`:
  passed with the known redirect ledger warning.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check CHANGELOG.md scripts/planning_state.py tests/test_planning_state.py`:
  passed with the existing `/usr/bin/python3.14` symlink warning.
- `python scripts/planning_state.py validate-closeout --root docs/plans --program planning-state-tooling --batch-id planning-state-migration-pilot --closeout docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/closeout.md --state-file /tmp/planning-state-migration-pilot-closeout-state.json`:
  passed.
- `git diff --check`: passed.

Cleanup residue: none. PST-6 SQLite projection remains deferred program work,
not cleanup residue from this batch.
