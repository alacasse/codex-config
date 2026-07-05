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
- Keep planning-state tooling separate from the future OSS Go runner. Interop
  belongs in explicit command/file protocols, schemas, and golden fixtures, not
  Python imports or duplicated Markdown heuristics.

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
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/`

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| PST-1. Planning state is inferred from Markdown and filenames | Closed | `planning-state-readonly-core` | Use read-only diagnostics before broad planning tree scans | Slice 3 evidence is clean for `current` and `validate` against codex-config and Graphify planning roots. The implemented commands report active root/program `CURRENT.md` state and stale-context warnings without writes or SQLite. |
| PST-2. Batch/artifact paths are manually allocated by agents | Closed | `planning-state-write-transitions` | Use allocation and registration commands for future batch setup | Depends on PST-1 state discovery. Slice 2 added canonical path allocation and explicit artifact registration. |
| PST-3. Cross-batch obligations are not first-class state | Closed | `planning-state-write-transitions` | Feed explicit obligations into future closeout contracts | Enables fourth-batch cleanup without archaeology. Slice 4 added obligation records and validation. |
| PST-4. Batch closeout lacks a bounded evidence-index contract | Closed | `planning-state-closeout-contract` | Require bounded pointer-first closeout evidence before batch closure | Closed by closeout contract, validation, rendering, and handoff docs. Completed-batch closeout must point to validation, review, completed-slices, commits, obligations, receipts when present, and cleanup residue evidence instead of embedding logs. |
| PST-5. Existing planning roots need migration without losing human readability | Closed | `planning-state-migration-pilot` | Use bootstrap and migrated-fixture validation before any future runner/reporting layer consumes planning state | Closed by the migration-pilot closeout. `bootstrap-state` generates companion v1 JSON state from Layout v1 Markdown, preserves active-first pickup, registers co-located artifacts, and keeps Markdown as human-readable coordination state. `current`/`validate --state-file` reject drift, malformed obligations, artifact collisions, and unregistered active pointers. |
| PST-6. Operational queries are awkward from files alone | Deferred | None | Add optional SQLite projection and report commands after PST-8 closes | Do only after canonical state, rendering, and project state/projection ownership policy are stable. |
| PST-7. Runner interoperability protocol is undefined | Closed | `planning-state-write-transitions` | Use command/file outputs as the runner boundary | Depends on PST-1 and informed PST-2/PST-3. Slice 1 defined JSON facts, Slice 3 added transition receipts, and Slice 4 added obligation facts without runner imports of planning-state internals. |
| PST-8. Project planning-state ownership policy is implicit | Queued | `planning-state-project-policy` | Execute the project policy batch before SQLite | codex-config can commit repo-owned planning docs; Graphify-style work may require ignored local overlays; future projects may choose committed, ignored-local, external, generated-only, or no durable state. Tooling must resolve this as project policy before durable JSON state or SQLite projections are written. |

## Batch Queue

| Batch | Findings | Status | Why grouped | Depends on | Validation class | Dispatch | Spec |
|---|---|---|---|---|---|---|---|
| planning-state-readonly-core | PST-1 | Completed | Establishes active-state precedence, stale-context warnings, and the safe tool boundary before any state writes | None | Focused Python unit tests and dry-run CLI checks against codex-config fixtures and the Graphify planning-root fixture | `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/runway.md` |
| planning-state-write-transitions | PST-2, PST-3, PST-7 | Completed | Moves allocation, registration, selection, obligations, and runner-facing interop facts into commands | planning-state-readonly-core | Focused state/CLI tests, interop fixture tests, and Markdown round-trip checks | `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/runway.md` |
| planning-state-closeout-contract | PST-4 | Completed | Makes completed-batch evidence bounded and validateable | planning-state-write-transitions | Focused rendering/validation tests plus current/validate diagnostics | `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/runway.md` |
| planning-state-migration-pilot | PST-5 | Completed | Bootstraps tool state from existing planning roots without hiding Markdown | planning-state-readonly-core; preferably planning-state-closeout-contract | Fixture migration tests, current/validate diagnostics, review, and closeout evidence | `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/runway.md` |
| planning-state-project-policy | PST-8 | Queued | Makes state-file and projection ownership explicit per project before SQLite chooses targets | planning-state-migration-pilot | Project-policy parsing/validation tests, temp committed and ignored-local fixtures, current/validate diagnostics, and closeout evidence | `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/runway.md` |
| planning-state-sqlite-projection | PST-6 | Deferred | Adds fast operational reporting after canonical files and project policy are stable while keeping SQLite optional and rebuildable | planning-state-project-policy | SQLite rebuild/report tests, report CLI checks, current/validate diagnostics, and closeout evidence | `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/runway.md` |

## Latest Batch Brief

Latest completed batch:

- Batch: `planning-state-migration-pilot`
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/dispatch.md`
- Status: `Completed`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/closeout.md`
- Notes: Migration bootstrap generation and migrated fixture validation are
  available. Bootstrap JSON is companion tool state, not a replacement for
  human-readable Markdown planning artifacts. PST-6 remains deferred optional
  reporting work.

## Queued Batch Brief

Queued batch:

- Batch: `planning-state-project-policy`
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/dispatch.md`
- Status: `Queued`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/runway.md`
- Notes: PST-8 should define project-owned state and projection policy before
  SQLite. codex-config, ignored local overlays, and future projects must be
  able to declare different ownership policies without generic workflow code
  hard-coding one repository's layout.

## Recommended Work Order

1. Execute `planning-state-project-policy` from its queued runway.
2. Queue and execute `planning-state-sqlite-projection` only after PST-8 closes.

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
  Markdown while preserving human-readable artifacts and redirects, and after
  the migration-pilot batch has validation, review, and closeout evidence.
- Mark PST-6 `Closed` only after SQLite can be deleted and rebuilt from
  canonical artifacts and resolved project policy, with agents still using
  command/report interfaces.
- Mark PST-7 `Closed` only after planning-state facts have an explicit
  command/file protocol with JSON shape, warning/error shape, exit-code meaning,
  and golden fixtures that a future Go runner can consume without scraping
  Markdown heuristics.
- Mark PST-8 `Closed` only after project policy can represent committed,
  ignored-local, external, generated-only, and no durable state/projection
  layouts without hard-coding a downstream project path, and after write-target
  preflights reject policy-incompatible durable JSON or SQLite outputs.

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
