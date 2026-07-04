# Planning-State Tooling Program Ledger

## Purpose

Track the planning-state tooling workstream so future agents can create concrete
Batch Runway specs without replaying the full brainstorming thread. This ledger
is planning-only; it does not implement code.

## Current Direction

- Shift active-state resolution, path allocation, artifact registration,
  cross-batch obligation tracking, and closeout validation into code.
- Keep Markdown and JSON canonical, readable, diffable, and repairable.
- Keep SQLite optional and rebuildable as a reporting projection.
- Keep agents at the workflow command level; agents should not write SQL or
  mutate backing stores directly.
- Keep generic tooling project-neutral. Project-specific paths, validation
  commands, and overlays belong in project instructions or active specs.

## Source Context

- Decision note: `docs/plans/planning-state-tooling-plan.md`
- Planning Artifact Layout v1:
  `skills/planning-artifacts/SKILL.md`
- Architecture Program Runway:
  `skills/architecture-program-runway/SKILL.md`
- First real fixture: Graphify local planning root at
  `/home/alacasse/projects/graphify/my-docs/plans/`
- Related GitHub issues: #8, #10, #12, #22
- Current runner concept owners: `scripts/architecture_program_runner*.py`

## Planning Layout

- Layout version: Planning Artifact Layout v1.
- Planning root: `docs/plans/`
- Program root: `docs/plans/programs/planning-state-tooling/`
- Program ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Program current state: `docs/plans/programs/planning-state-tooling/CURRENT.md`
- Program archive root: `docs/plans/archive/`
- Run artifact root: not selected for this planning-only ledger.
- Output root: not selected for this planning-only ledger.
- Latest completed batch directory:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/`

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| PST-1. Planning state is inferred from Markdown and filenames | Closed | `planning-state-readonly-core` | Use read-only diagnostics before broad planning tree scans | Slice 3 evidence is clean for `current` and `validate` against codex-config and Graphify planning roots. The implemented commands report active root/program `CURRENT.md` state and stale-context warnings without writes or SQLite. |
| PST-2. Batch/artifact paths are manually allocated by agents | Candidate | None | Add tool-owned path allocation and artifact registration | Depends on PST-1 state discovery. |
| PST-3. Cross-batch obligations are not first-class state | Candidate | None | Add obligation IDs, owners, and close conditions | Enables fourth-batch cleanup without archaeology. |
| PST-4. Batch closeout lacks a bounded evidence-index contract | Candidate | None | Add `closeout.md` rendering and validation | Should stay compact and pointer-first. |
| PST-5. Existing planning roots need migration without losing human readability | Candidate | None | Add migration inventory and state bootstrap | Pilot after read-only validation is reliable. |
| PST-6. Operational queries are awkward from files alone | Deferred | None | Add optional SQLite projection and report commands | Do only after canonical state and rendering are stable. |

## Batch Queue

| Batch | Findings | Status | Why grouped | Depends on | Validation class | Dispatch | Spec |
|---|---|---|---|---|---|---|---|
| planning-state-readonly-core | PST-1 | Completed | Establishes active-state precedence, stale-context warnings, and the safe tool boundary before any state writes | None | Focused Python unit tests and dry-run CLI checks against codex-config fixtures and the Graphify planning-root fixture | `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/runway.md` |
| planning-state-write-transitions | PST-2, PST-3 | Candidate | Moves allocation, registration, selection, and obligations into commands | planning-state-readonly-core | Focused state/CLI tests plus Markdown round-trip checks | TBD | TBD |
| planning-state-closeout-contract | PST-4 | Candidate | Makes completed-batch evidence bounded and validateable | planning-state-write-transitions | Focused rendering/validation tests | TBD | TBD |
| planning-state-migration-pilot | PST-5 | Candidate | Bootstraps tool state from existing planning roots without hiding Markdown | planning-state-readonly-core; preferably planning-state-closeout-contract | Fixture migration tests and docs-only readback | TBD | TBD |
| planning-state-sqlite-projection | PST-6 | Deferred | Adds fast operational reporting after canonical files are stable | planning-state-write-transitions; migration pilot evidence | SQLite rebuild/report tests | TBD | TBD |

## Latest Batch Brief

Latest completed batch:

- Batch: `planning-state-readonly-core`
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md`
- Status: `Completed`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/runway.md`
- Notes: Read-only `current` and `validate` diagnostics are available. Write
  transitions, artifact registration, closeout validation, migration, and
  SQLite remain deferred to later rows.

### Dispatch Packet

Promoted to
`docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md`.

## Recommended Work Order

1. `planning-state-write-transitions`: move selection, path allocation,
   registration, and cross-batch obligations behind commands.
2. `planning-state-closeout-contract`: render and validate bounded closeout
   evidence indexes.
3. `planning-state-migration-pilot`: bootstrap state from existing `docs/plans/`
   and one Graphify planning root.
4. `planning-state-sqlite-projection`: add rebuildable operational reporting
   only after canonical state is stable.

## Closeout Rules

- Mark PST-1 `Closed` only after `current` and `validate` work against Graphify
  root/program `CURRENT.md` fixtures, Graphify redirect/stale-note fixtures, and
  codex-config `docs/plans/` root/program `CURRENT.md` plus redirect examples
  without mutating tracked files.
- Mark PST-2 `Closed` only after agents can register dispatch, runway, closeout,
  receipt, and output paths through commands instead of hand-allocating them.
- Mark PST-3 `Closed` only after open obligations have IDs, owners, close
  conditions, and validation that prevents silent loss.
- Mark PST-4 `Closed` only after completed batches require a bounded
  pointer-first `closeout.md` or an explicit documented exception.
- Mark PST-5 `Closed` only after migration can bootstrap state from existing
  Markdown while preserving human-readable artifacts and redirects.
- Mark PST-6 `Closed` only after SQLite can be deleted and rebuilt from
  canonical artifacts, with agents still using command/report interfaces.

## Planning Rules

- Create one concrete Batch Runway spec at a time.
- Start with read-only behavior; do not mix validation with write transitions.
- Keep this ledger compact. Put detailed design in
  `docs/plans/planning-state-tooling-plan.md` or future dispatch/spec files.
- Future agents should start with `docs/plans/CURRENT.md`, then consume this
  program's `CURRENT.md` and selected dispatch before reading full
  brainstorming history.
- Do not update GitHub issues as part of docs-only planning unless explicitly
  requested.
