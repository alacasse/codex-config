# Planning Current State

## Layout

- Layout: Planning Artifact Layout v1
- Planning root: `docs/plans/`
- Run artifact root: `<program-root>/architecture-program-runs/` when a program
  uses the architecture-program runner; otherwise `None selected`
- Output root: `None selected`
- One-shot intake: `None`
- Program archive root: `docs/plans/archive/`

## Active Programs

| Program | Current state |
|---|---|
| `architecture-program-runner` | `docs/plans/programs/architecture-program-runner/CURRENT.md` |
| `planning-state-tooling` | `docs/plans/programs/planning-state-tooling/CURRENT.md` |

## Compatibility Notes

- Flat active ledgers under `docs/plans/*.md` are retired for pickup. The old
  active ledger paths now contain redirects to program-local `LEDGER.md` files.
- Historical files under `docs/plans/archive/` retain their original references
  and are not active coordination state.
- `plans/codex-config-phase-runner-extraction-prep-runway.md` and
  `plans/dispatch/phase-runner-extraction-prep-dispatch.md` are historical
  compatibility artifacts from the closed extraction-prep batch.

## Next Safe Action

Use the relevant program `CURRENT.md` before reading ledgers, historical plans,
or source files. Do not infer selected work from old flat filenames or archive
contents.
