# Planning Current State

## Layout

- Layout: Planning Artifact Layout v1
- Planning root: `docs/plans/`
- Run artifact root: `None selected`; selected runner batches may declare
  program-local run artifacts before execution
- Output root: `None selected`
- One-shot intake: `None`
- Program archive root: `docs/plans/archive/`

## Active Programs

| Program | Current state |
|---|---|
| `codex-config` | `docs/plans/programs/codex-config/CURRENT.md` |

## Compatibility Notes

- `docs/plans/programs/codex-config/LEDGER.md` is the only active program
  ledger for codex-config pickup.
- The old `architecture-program-runner` and `planning-state-tooling` program
  ledgers are archived under `docs/plans/archive/program-ledgers/` and must not
  be used as active pickup sources.
- Flat compatibility ledgers under `docs/plans/*.md` are retired for pickup and
  redirect to the canonical codex-config ledger.
- Historical files under `docs/plans/archive/` and old program batch
  directories retain their original references and are not active coordination
  state.
- Repository-root `plans/` is retired. Do not create or use it for active,
  semi-active, or compatibility planning.
- The closed extraction-prep compatibility artifacts now live under
  `docs/plans/archive/compatibility/root-plans/`.

## Next Safe Action

Use `docs/plans/programs/codex-config/CURRENT.md` before reading the canonical
ledger. Do not infer selected work from old flat filenames, old APR/PST program
directories, archived ledgers, retired planning paths, or archive contents.
