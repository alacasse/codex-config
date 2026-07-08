# 0001: Planning Root And Plan Archive

## Status

Accepted.

## Context

Architecture-program runner planning had accumulated under `plans/`, mixing
active coordination material with completed runways, block reports, and other
historical notes. Future runner invocations need a stable documentation root
that agents can follow without replaying superseded plans.

## Decision

Use `docs/plans/` as the project **Planning Root** for active program ledgers,
dispatch packets, runway specs, and planning reports.

Use `docs/plans/archive/` as the **Plan Archive** for completed or superseded
planning documents that should remain readable but should not be treated as
active instructions.

The historical phase-runner extraction-prep runway spec and dispatch packet are
archived under `docs/plans/archive/compatibility/root-plans/`. Use
`docs/plans/CURRENT.md` for active planning-root policy.

Runtime runner artifacts, cache files, sessions, logs, ignored local artifacts,
and `architecture-program-runs/` are not planning documents and must not be
moved into the Planning Root or Plan Archive.

## Consequences

- As of the 2026-07-08 consolidation, the active codex-config Program Ledger is
  `docs/plans/programs/codex-config/LEDGER.md`. Earlier architecture-program
  runner and planning-state-tooling ledger snapshots are archive evidence, not
  active pickup sources.
- Future architecture-program runner invocations should use `docs/plans/`
  paths for active planning inputs.
- Completed and superseded material can be archived mechanically without
  rewriting its historical content unless path/readability updates are needed.
- Use `docs/plans/CURRENT.md` for active planning-root policy.
