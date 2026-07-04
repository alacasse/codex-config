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
- Related GitHub issues: #8, #10, #12, #22
- Current runner concept owners: `scripts/architecture_program_runner*.py`

## Planning Layout

- Layout version: current `docs/plans/` planning root with a temporary flat
  planning-file convention.
- Planning root: `docs/plans/`
- Program root: flat file convention for this planning pass.
- Program ledger: `docs/plans/planning-state-tooling-ledger.md`
- Program archive root: `docs/plans/archive/`
- Run artifact root: not selected for this planning-only ledger.
- Output root: not selected for this planning-only ledger.
- Compatibility exception: this repo has not fully moved its own planning docs
  into `programs/<slug>/`; keep these artifacts flat under `docs/plans/`.

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| PST-1. Planning state is inferred from Markdown and filenames | Ready | None | Build read-only `planning-state current` and `planning-state validate` | Start with discovery and validation only; no writes, no SQLite. |
| PST-2. Batch/artifact paths are manually allocated by agents | Candidate | None | Add tool-owned path allocation and artifact registration | Depends on PST-1 state discovery. |
| PST-3. Cross-batch obligations are not first-class state | Candidate | None | Add obligation IDs, owners, and close conditions | Enables fourth-batch cleanup without archaeology. |
| PST-4. Batch closeout lacks a bounded evidence-index contract | Candidate | None | Add `closeout.md` rendering and validation | Should stay compact and pointer-first. |
| PST-5. Existing planning roots need migration without losing human readability | Candidate | None | Add migration inventory and state bootstrap | Pilot after read-only validation is reliable. |
| PST-6. Operational queries are awkward from files alone | Deferred | None | Add optional SQLite projection and report commands | Do only after canonical state and rendering are stable. |

## Batch Queue

| Batch | Findings | Status | Why grouped | Depends on | Validation class | Dispatch | Spec |
|---|---|---|---|---|---|---|---|
| planning-state-readonly-core | PST-1 | Ready | Establishes the safe tool boundary before any state writes | None | Focused Python unit tests and dry-run CLI checks | TBD | TBD |
| planning-state-write-transitions | PST-2, PST-3 | Candidate | Moves allocation, registration, selection, and obligations into commands | planning-state-readonly-core | Focused state/CLI tests plus Markdown round-trip checks | TBD | TBD |
| planning-state-closeout-contract | PST-4 | Candidate | Makes completed-batch evidence bounded and validateable | planning-state-write-transitions | Focused rendering/validation tests | TBD | TBD |
| planning-state-migration-pilot | PST-5 | Candidate | Bootstraps tool state from existing planning roots without hiding Markdown | planning-state-readonly-core; preferably planning-state-closeout-contract | Fixture migration tests and docs-only readback | TBD | TBD |
| planning-state-sqlite-projection | PST-6 | Deferred | Adds fast operational reporting after canonical files are stable | planning-state-write-transitions; migration pilot evidence | SQLite rebuild/report tests | TBD | TBD |

## Selected Batch Brief

Current dispatch:

- Batch: `planning-state-readonly-core`
- Dispatch: `TBD`
- Status: `Ready`
- Notes: Create a dispatch/spec for read-only state discovery and validation
  before implementing write transitions.

### Dispatch Packet Draft

```yaml
batch_id: planning-state-readonly-core
source_program_ledger: docs/plans/planning-state-tooling-ledger.md
included_findings:
  - id: PST-1
    title: Planning state is inferred from Markdown and filenames
excluded_findings:
  - id: PST-2
    reason: Write transitions must wait until read-only state discovery is stable.
  - id: PST-3
    reason: Obligation mutation depends on the state model introduced by PST-1/PST-2.
  - id: PST-4
    reason: Closeout rendering should consume the read-only model first.
  - id: PST-5
    reason: Migration should wait until validation can prove source artifacts.
  - id: PST-6
    reason: SQLite is a projection and should wait until canonical state is stable.
goal: Add a read-only planning-state tool that reports active planning state and validates existing artifacts.
owner_seam: scripts/planning_state.py as the first planning-state facade, with small owner modules only if the first slice proves they are needed.
validation_class: focused Python unit tests plus dry-run CLI checks; no GitHub or network access.
guardrails:
  - Markdown and JSON remain canonical.
  - SQLite is out of scope.
  - Tool output is semantic and agent-facing; no SQL or backing-store details.
  - No Graphify-specific paths or validation commands in generic code.
  - Existing Markdown-only workflows remain valid when no tool state exists.
dependencies_satisfied:
  - Planning Artifact Layout v1 exists.
  - Architecture Program Runway active-state fast path exists.
  - Runner already has JSON state, receipts, manifests, telemetry, and input inventory owners.
dependencies_blocking:
  - None for read-only validation.
suggested_slices:
  - Define the read-only state model and fixture set from `docs/plans/`.
  - Implement `planning-state current` for active programs, selected batch, queued runway, latest closeout, and allowed next actions.
  - Implement `planning-state validate` for `CURRENT.md`, ledgers, batch directories, runner artifacts, and generated-output placement.
  - Document fallback behavior for Markdown-only roots and update user-facing workflow guidance.
stop_conditions:
  - The batch would need to write canonical state or rendered Markdown.
  - The batch would need SQLite.
  - The batch would need Graphify-specific path rules in generic code.
  - Active-state rules conflict with Planning Artifact Layout v1.
expected_spec_path: docs/plans/planning-state-readonly-core-runway.md
```

## Recommended Work Order

1. `planning-state-readonly-core`: prove the tool can answer and validate
   current state without mutating anything.
2. `planning-state-write-transitions`: move selection, path allocation,
   registration, and cross-batch obligations behind commands.
3. `planning-state-closeout-contract`: render and validate bounded closeout
   evidence indexes.
4. `planning-state-migration-pilot`: bootstrap state from existing `docs/plans/`
   and one Graphify planning root.
5. `planning-state-sqlite-projection`: add rebuildable operational reporting
   only after canonical state is stable.

## Closeout Rules

- Mark PST-1 `Closed` only after `current` and `validate` work against fixtures
  and existing `docs/plans/` examples without mutating tracked files.
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
- Future agents should consume the selected batch brief above before reading
  the full brainstorming history.
- Do not update GitHub issues as part of docs-only planning unless explicitly
  requested.
