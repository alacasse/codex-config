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

The currently executing phase-runner extraction-prep runway spec and dispatch
packet remain under `plans/` until that batch closes, because moving them
mid-execution would make coordinator recovery ambiguous. They are the only
intentional active-planning compatibility exception.

Runtime runner artifacts, cache files, sessions, logs, ignored local artifacts,
and `architecture-program-runs/` are not planning documents and must not be
moved into the Planning Root or Plan Archive.

## Consequences

- The active Program Ledger is
  `docs/plans/codex-config-architecture-program-runner-findings.md`.
- Future architecture-program runner invocations should use `docs/plans/`
  paths for active planning inputs.
- Completed and superseded material can be archived mechanically without
  rewriting its historical content unless path/readability updates are needed.
- The old `plans/` root is a temporary compatibility location for the active
  extraction-prep spec and dispatch only, not the future active Planning Root.
