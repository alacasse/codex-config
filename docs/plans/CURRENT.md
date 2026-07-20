# Planning Current State

## Layout

- Layout: Planning Artifact Layout v1
- Planning root: `docs/plans/`
- Batch runtime policy: `batch-local`; small state owned by one batch lives under
  that batch directory, normally in `.runtime/`
- Run artifact root: `None selected`; optional only for runner-global, bulky, or
  explicitly external operational artifacts
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
- The closed extraction-prep compatibility artifacts live under
  `docs/plans/archive/compatibility/root-plans/`.
- A temporary directory may be used by a test or disposable acceptance run, but
  its generated path is not durable planning state and must not be persisted as
  the location of a real batch.

## Next Safe Action

Use `docs/plans/programs/codex-config/CURRENT.md` before reading the canonical
ledger. Do not infer selected work from old flat filenames, old APR/PST program
directories, archived ledgers, retired planning paths, or archive contents.
