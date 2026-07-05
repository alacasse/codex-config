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
- Make declared projections operationally useful for history/reporting workflows
  when project policy permits, while keeping active-state correctness independent
  of SQLite.
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
- Queued batch directory:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/`
- Latest completed batch directory:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/`

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| PST-1. Planning state is inferred from Markdown and filenames | Closed | `planning-state-readonly-core` | Use read-only diagnostics before broad planning tree scans | Slice 3 evidence is clean for `current` and `validate` against codex-config and Graphify planning roots. The implemented commands report active root/program `CURRENT.md` state and stale-context warnings without writes or SQLite. |
| PST-2. Batch/artifact paths are manually allocated by agents | Closed | `planning-state-write-transitions` | Use allocation and registration commands for future batch setup | Depends on PST-1 state discovery. Slice 2 added canonical path allocation and explicit artifact registration. |
| PST-3. Cross-batch obligations are not first-class state | Closed | `planning-state-write-transitions` | Feed explicit obligations into future closeout contracts | Enables fourth-batch cleanup without archaeology. Slice 4 added obligation records and validation. |
| PST-4. Batch closeout lacks a bounded evidence-index contract | Closed | `planning-state-closeout-contract` | Require bounded pointer-first closeout evidence before batch closure | Closed by closeout contract, validation, rendering, and handoff docs. Completed-batch closeout must point to validation, review, completed-slices, commits, obligations, receipts when present, and cleanup residue evidence instead of embedding logs. |
| PST-5. Existing planning roots need migration without losing human readability | Closed | `planning-state-migration-pilot` | Use bootstrap and migrated-fixture validation before any future runner/reporting layer consumes planning state | Closed by the migration-pilot closeout. `bootstrap-state` generates companion v1 JSON state from Layout v1 Markdown, preserves active-first pickup, registers co-located artifacts, and keeps Markdown as human-readable coordination state. `current`/`validate --state-file` reject drift, malformed obligations, artifact collisions, and unregistered active pointers. |
| PST-6. Operational queries are awkward from files alone | Closed | `planning-state-sqlite-projection` | Use `rebuild-projection` and `report-projection` for bounded operational reports when a caller provides a policy-compatible database target | Closed by optional SQLite projection rebuild, report commands, runner-artifact report coverage, validation, review, and pointer-first closeout evidence. SQLite is delete-safe and remains behind command/report interfaces. |
| PST-7. Runner interoperability protocol is undefined | Closed | `planning-state-write-transitions` | Use command/file outputs as the runner boundary | Depends on PST-1 and informed PST-2/PST-3. Slice 1 defined JSON facts, Slice 3 added transition receipts, and Slice 4 added obligation facts without runner imports of planning-state internals. |
| PST-8. Project planning-state ownership policy is implicit | Closed | `planning-state-project-policy` | Use resolved project policy for durable state/projection writes and SQLite work | Closed with validation, review, and closeout evidence. codex-config committed planning docs and ignored-local overlay examples are documented without becoming universal defaults; write-target preflights reject policy-incompatible durable JSON or SQLite outputs. |
| PST-9. Planning-state operations have no reusable skill interface | Closed | `planning-state-skill-interface` | Use the repo-owned `planning-state` skill before wiring consumers | Closed by the `planning-state` skill entrypoint, install metadata, validation, review, and pointer-first closeout evidence. Fresh agents now have a compact routine interface for discovery, validation, optional state bootstrap, optional projection rebuild/reporting, and closeout evidence. |
| PST-10. Planning-state operational details are split between layout guidance and historical plan prose | Closed | `planning-state-skill-interface` | Use progressive skill references for optional state/projection/closeout details | Closed by the entrypoint plus focused references for state fixtures, target policy, projection reporting, closeout evidence, and runner artifacts. `planning-artifacts` remains the Layout v1 placement owner. |
| PST-11. Project policy target selection is not packaged as an agent-facing adapter | Closed | `planning-state-skill-interface` | Resolve or refuse state/projection targets through the planning-state skill | Closed by target-policy guidance covering stdout, `/tmp`, generated-only, committed, ignored-local, external, and none policies without embedding project-specific paths as generic defaults. |
| PST-12. Ledger-dependent skills duplicate active-state pickup and projection setup | Closed | `planning-state-consumer-integration` | Use the shared planning-state diagnostic interface before consumer-owned decisions | Closed by slices 1-3: `batch-runway`, `architecture-program-runway`, and `legacy-removal` now consume compact Planning State Diagnostic facts before Layout v1 pickup while preserving their own semantic decisions. |
| PST-13. Feature dependency metadata cannot express operational planning-state reuse | Closed | `planning-state-consumer-integration` | Install `planning-state` before consumers that invoke it | Closed by slice 4: `codex-features.json` keeps `planning-artifacts` and adds `planning-state` dependencies for the rewired consumers, with manifest tests covering expansion order and no cycle. |
| PST-14. Projection routing is implemented but not part of the routine interface | Closed | `planning-state-projection-routing` | Use projection-aware Planning State Diagnostic facts for history/reporting questions before broad historical scans when policy permits | Closed by the projection-routing batch. The `planning-state` skill now routes history/reporting questions through policy-compatible projection reports, while `current` and `validate` remain SQLite-independent active-state checks. |
| PST-15. Projection target policy does not express expected projection usage | Closed | `planning-state-projection-routing` | Use explicit `projection_usage` and `projection_rebuild_authority` policy before rebuilding or reporting projections | Closed by the projection-routing batch. Project policy now distinguishes allowed projection targets from expected projection usage and rebuild authority without introducing downstream project paths or durable default databases. |
| PST-16. Consumer skills consume active-state diagnostics but not projection reports | Pending | `planning-state-projection-consumers` | Continue the active runway; do not change source finding scope while the cut batch is in flight | Consumer skills now use `planning-state` before active-state pickup, but they do not require projection reports for pending batches, missing closeout evidence, batch evidence, or runner summaries. The token-saving interface is therefore not exercised by default. |
| PST-17. Tests protect projection commands but not workflow obligations | Pending | `planning-state-projection-consumers` | Continue the active runway; do not change source finding scope while the cut batch is in flight | `tests/test_planning_state.py` covers SQLite rebuild/report behavior, but no test protects the agent-facing rule that history/reporting workflows should try projection reports before Markdown archaeology when policy permits. |
| PST-18. Batch Runway create-spec writes session-local mode into durable overrides | Open | None | Correct the Batch Runway create-spec output contract and add regression coverage after the active projection-consumers batch closes, unless explicitly amended into that runway | The stale `Treat this session as create-spec` line belongs to spec creation history, not durable execution-contract `Overrides`. Fix the write-side contract so generated runways keep only durable execution deviations in `Overrides`, patch affected active/future runways deliberately, and keep this out of `scripts/planning_state.py` because mode semantics belong to Batch Runway. |
| PST-19. Findings lack a Pending status for cut or active batch work | Open | None | Define and enforce a `Pending` finding status for work that has been cut into a queued or active batch but is not closed | `Open` currently covers both uncut intake and findings already assigned to a dispatch/runway, which invites late source-ledger scope edits after a batch is materialized. `Pending` should mean the finding is controlled by the batch artifacts until closeout, supersession, explicit abandonment, or an explicit amendment. |

## Batch Queue

| Batch | Findings | Status | Why grouped | Depends on | Validation class | Dispatch | Spec |
|---|---|---|---|---|---|---|---|
| planning-state-readonly-core | PST-1 | Completed | Establishes active-state precedence, stale-context warnings, and the safe tool boundary before any state writes | None | Focused Python unit tests and dry-run CLI checks against codex-config fixtures and the Graphify planning-root fixture | `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/runway.md` |
| planning-state-write-transitions | PST-2, PST-3, PST-7 | Completed | Moves allocation, registration, selection, obligations, and runner-facing interop facts into commands | planning-state-readonly-core | Focused state/CLI tests, interop fixture tests, and Markdown round-trip checks | `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/runway.md` |
| planning-state-closeout-contract | PST-4 | Completed | Makes completed-batch evidence bounded and validateable | planning-state-write-transitions | Focused rendering/validation tests plus current/validate diagnostics | `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/runway.md` |
| planning-state-migration-pilot | PST-5 | Completed | Bootstraps tool state from existing planning roots without hiding Markdown | planning-state-readonly-core; preferably planning-state-closeout-contract | Fixture migration tests, current/validate diagnostics, review, and closeout evidence | `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/runway.md` |
| planning-state-project-policy | PST-8 | Completed | Makes state-file and projection ownership explicit per project before SQLite chooses targets | planning-state-migration-pilot | Project-policy parsing/validation tests, temp committed and ignored-local fixtures, current/validate diagnostics, and closeout evidence | `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/runway.md` |
| planning-state-sqlite-projection | PST-6 | Completed | Adds fast operational reporting after canonical files and project policy are stable while keeping SQLite optional and rebuildable | planning-state-project-policy closed by `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/closeout.md` | SQLite rebuild/report tests, report CLI checks, current/validate diagnostics, review, and closeout evidence | `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/runway.md` |
| planning-state-skill-interface | PST-9, PST-10, PST-11 | Completed | Creates the deep skill interface that centralizes planning-state operations before consumers depend on it | planning-state-sqlite-projection | Skill validation, current/validate CLI smoke, generated-only `/tmp` state/projection smoke, manifest/changelog alignment, and grep checks for project-specific hard-coding | `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/runway.md` |
| planning-state-consumer-integration | PST-12, PST-13 | Completed | Wires ledger-dependent skills and install metadata to the shared planning-state skill after the interface exists | planning-state-skill-interface | Skill validation, dependency-manifest JSON check, focused wording checks across consumer skills, current/validate diagnostics, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/runway.md` |
| planning-state-projection-routing | PST-14, PST-15 | Completed | Deepens the Planning State Diagnostic interface so declared projections become useful for history/reporting without becoming canonical active state | planning-state-consumer-integration | Skill/reference tests, project-policy parsing checks, current/validate/projection smoke tests against generated-only and ignored-local fixtures, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/runway.md` |
| planning-state-projection-consumers | PST-16, PST-17 | Queued | Wires consumer skills and regression checks so projection reports are tried before broad historical scans when policy permits | planning-state-projection-routing | Skill wording tests, manifest/dependency checks if metadata changes, focused grep checks across consumer skills, current/validate diagnostics, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/runway.md` |
| batch-runway-create-spec-output-contract | PST-18 | Candidate | Keeps session-local create-spec history out of durable Batch Runway execution contracts | planning-state-projection-consumers closed, unless explicitly amended into the active runway | Batch Runway skill/reference wording tests, regression check for durable `Overrides`, focused grep across active templates/specs, current/validate diagnostics, and `git diff --check` | None | None |
| planning-state-finding-pending-status | PST-19 | Candidate | Makes cut-but-not-closed finding state explicit so source ledgers stop being edited as raw intake once a dispatch/runway exists | planning-state-projection-consumers closed, unless selected as an explicit active-runway amendment | Ledger/template wording checks, optional planning-state validation if status vocabulary becomes machine-checked, current/validate diagnostics, and `git diff --check` | None | None |

## Latest Batch Brief

Queued batch:

- Batch: `planning-state-projection-consumers`
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/dispatch.md`
- Status: `Queued`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/runway.md`
- Covers: PST-16 and PST-17.
- Goal: wire Batch Runway, Architecture Program Runway, and Legacy Removal so
  supported history/reporting workflows try policy-compatible projection
  reports before broad historical scans, with focused regression checks.
- Notes: execute this queued runway next. Do not create another
  planning-state-tooling batch until this runway closes, blocks, is superseded,
  or is explicitly abandoned.

Latest completed batch:

- Batch: `planning-state-projection-routing`
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/dispatch.md`
- Status: `Completed`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/closeout.md`
- Notes: PST-14 and PST-15 are closed. Projection-aware policy, skill routing,
  diagnostics, and smoke evidence are complete. PST-16 and PST-17 remain open
  for `planning-state-projection-consumers`.

## Recommended Work Order

1. Execute the queued `planning-state-projection-consumers` runway before
   selecting another planning-state-tooling batch.
2. After that batch closes, prefer `planning-state-finding-pending-status`
   before more large batches so future ledgers distinguish uncut `Open` work
   from cut or active `Pending` work.
3. Then schedule `batch-runway-create-spec-output-contract` unless it has been
   explicitly amended into the active runway.
4. For projection reporting, rebuild only to explicit temp or
   policy-compatible database targets and keep Markdown/JSON canonical.

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
- Mark PST-9 `Closed` only after a repo-owned `planning-state` skill gives
  fresh agents a compact interface for discovery, validation, optional
  state-fixture bootstrapping, optional SQLite projection rebuild, and
  projection reporting.
- Mark PST-10 `Closed` only after the planning-state skill uses progressive
  discovery: the entrypoint covers the routine hot path, and references cover
  state fixtures, projection reporting, runner artifacts, closeout, and
  target-policy details only when needed.
- Mark PST-11 `Closed` only after the skill tells agents how to resolve or
  refuse state/projection targets from project policy without embedding
  project-specific paths as generic defaults.
- Mark PST-12 `Closed` only after the ledger-dependent consumer skills use the
  shared planning-state interface before making their own semantic decisions.
- Mark PST-13 `Closed` only after feature metadata installs the new skill and
  declares consumer dependencies that distinguish layout convention from
  operational planning-state diagnostics.
- Mark PST-14 `Closed` only after the `planning-state` skill gives agents an
  explicit projection-aware routing rule for history/reporting questions, while
  preserving `current` and `validate` as SQLite-independent active-state checks.
- Mark PST-15 `Closed` only after project policy distinguishes allowed
  projection targets from expected projection usage and rebuild authority without
  hard-coding a downstream project path.
- Mark PST-16 `Closed` only after Batch Runway, Architecture Program Runway, and
  Legacy Removal try projection reports for supported history/reporting
  questions before broad historical scans when project policy permits.
- Mark PST-17 `Closed` only after regression checks protect the consumer-facing
  projection-report routing obligation, not just the underlying
  `rebuild-projection` and `report-projection` command behavior.
- Mark PST-18 `Closed` only after Batch Runway create-spec guidance prevents
  session-local mode claims from being written as durable runway `Overrides`,
  focused regression coverage protects that write-side invariant, and affected
  active/future runway artifacts are patched deliberately rather than through a
  source-ledger scope edit.
- Mark PST-19 `Closed` only after the findings ledger vocabulary defines
  `Pending` for cut or active batch work, future batch selection/update guidance
  tells agents not to mutate Pending finding scope except through an explicit
  batch amendment or follow-up item, and validation or docs-as-code checks cover
  the status transition if the tooling consumes finding status.

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
