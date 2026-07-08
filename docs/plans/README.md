# Planning Root

`docs/plans/` is the active **Planning Root** for repo-owned workflow planning.
Use Planning Artifact Layout v1 for active pickup.

Active planning:

- `CURRENT.md`: root active-state handoff.
- `programs/codex-config/CURRENT.md`: codex-config pickup state.
- `programs/codex-config/LEDGER.md`: the single active codex-config Program
  Ledger.
- `phase-runner-repo-split-issue-12-plan.md`: current issue #12 decision note.
- `generic-phase-runner-product-idea.md`: product idea feeding the generic
  workflow contract.
- `generic-phase-runner-workflow-contract.md`: generic workflow boundary and
  current runner mapping.

Read-only diagnostics:

- When Layout v1 active-state files exist, run diagnostics before broad planning
  tree scans or historical filename searches:
  `python scripts/planning_state.py current --root docs/plans` and
  `python scripts/planning_state.py validate --root docs/plans`.
- Treat root and codex-config program `CURRENT.md` files as active pickup
  state. Redirects, archives, old program directories, and old flat files are
  compatibility or historical evidence unless the current files point to them.
- The diagnostics are read-only. Markdown and JSON remain canonical planning
  state; SQLite remains deferred and rebuildable if added later.

Compatibility redirects:

- `codex-config-architecture-program-runner-findings.md`
- `planning-state-tooling-ledger.md`
- `plans/codex-config-phase-runner-extraction-prep-runway.md` and
  `plans/dispatch/phase-runner-extraction-prep-dispatch.md` remain historical
  compatibility artifacts from a closed batch.

Archived program-ledger snapshots:

- `archive/program-ledgers/architecture-program-runner-LEDGER.md`
- `archive/program-ledgers/planning-state-tooling-LEDGER.md`

Completed or superseded plans and reports live under `docs/plans/archive/`.
