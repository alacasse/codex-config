# Codex Config Program Ledger

## Purpose

Track active and candidate codex-config workflow work in one canonical program
ledger. This ledger is the only active executable backlog source under
`docs/plans/` for `add-to-ledger`, `plan-batch`, and `work-batch`.

## Current Direction

- Keep repo-owned workflow skills project-neutral.
- Keep Planning Artifact Layout v1 active-state pickup rooted at
  `docs/plans/CURRENT.md`.
- Keep Markdown and JSON canonical, readable, diffable, and repairable.
- Keep SQLite optional and rebuildable as a reporting projection.
- Keep future runner extraction contract-first; do not create a new repository,
  dispatch, or runway until a `CCFG-N` row is explicitly selected.
- Keep skill cleanup work in this same codex-config ledger instead of splitting
  it into separate active pickup ledgers.

## Source Context

- Root current state: `docs/plans/CURRENT.md`
- Program current state: `docs/plans/programs/codex-config/CURRENT.md`
- Workflow guide: `docs/workflow-guide.md`
- Skill routing contract: `docs/skill-routing-contract.md`
- Planning Artifact Layout v1: `skills/planning-artifacts/SKILL.md`
- Planning State Diagnostic: `skills/planning-state/SKILL.md`
- Archived APR ledger snapshot:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST ledger snapshot:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Closed History

Closed APR and PST history remains preserved in archive snapshots, not copied
row-by-row here.

| Historical source | Archive pointer | Active pickup status |
|---|---|---|
| APR-1 through APR-25, plus historical runner batches | `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md` | Archived evidence only |
| PST-1 through PST-30, plus historical planning-state batches | `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md` | Archived evidence only |

## Findings Ledger

| Finding | Status | Source | Area | Next action | Notes |
|---|---|---|---|---|---|
| CCFG-1. Contract-first runner business-logic extraction | Pending | APR-26 | Runner extraction | Execute queued runway `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md` when requested | Preserve the APR-26 direction: external OSS runner remains possible, but the queued batch is limited to implementation-neutral workflow/state/result/receipt/worker/artifact contract boundaries, planning-state interop fixture expectations, facade compatibility expectations, explicit non-goals, and stop conditions before moving code or creating a repo skeleton. |
| CCFG-2. Branch-per-batch runner isolation mode | Open | APR-27; GitHub issue #11 | Runner workflow | Design after CCFG-1 clarifies the generic runner boundary | Preserve source scope: `--batch-branch-mode none\|create\|require`, deterministic branch naming, state/receipt branch metadata, and closeout commit-range evidence remain unimplemented. |
| CCFG-3. Contract-drift review skill | Open | APR-28; GitHub issue #14 | Runner support skill | Create only when extraction work starts to drift across boundaries | The requested skill should compare extraction changes against APR/PBC contracts, facade compatibility, generic-core boundaries, and stale-plan/archive risks without duplicating the full contract text. |
| CCFG-4. Runner adapter authoring skill | Open | APR-29; GitHub issue #16 | Runner support skill | Create after CCFG-1 stabilizes the generic worker/runtime boundary | Preserve adapter guidance scope: provider quirks stay out of generic runner core; cover result, receipt, transition, artifact, observation, and input-inventory boundaries. |
| CCFG-5. Baton dogfood diagnostics | Open | APR-30; GitHub issues #17, #18, #19 | Runner diagnostics | Sequence after CCFG-1 unless a diagnostic need blocks extraction | `baton-context-map`, `baton-doctor`, and `baton-receipt-inspector` should read runner/planning artifacts and produce compact diagnostics, not reconstruct execution from chat transcripts. |
| CCFG-6. Skill-slimmer support | Backlog | PST issue reconciliation #15 | Skill cleanup | Decide whether to add a focused skill-slimmer workflow | Source issue said the `skill-slimmer` skill does not exist. Keep this as cleanup backlog until a bounded workflow and validation target are selected. |
| CCFG-7. Batch Runway hot-path pruning | Completed | PST issue reconciliation #23 | Skill cleanup | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/closeout.md`. Batch Runway routine execution now has a guarded compact read path, non-routine references remain trigger-loaded, and runtime semantics remain owned by the same Batch Runway contracts. |
| CCFG-8. Ledger and dispatch rule dedupe | Backlog | PST issue reconciliation #24 | Skill cleanup | Deduplicate overlap across planning, dispatch, and runway skills | Preserve the source observation that `planning-artifacts`, `planning-state`, and consumer routing partially address this, but a focused dedupe pass remains. |
| CCFG-9. Short skill frontmatter descriptions | Backlog | PST issue reconciliation #25 | Skill cleanup | Shorten dense skill descriptions without losing trigger accuracy | Source issue said this is not done consistently. |
| CCFG-10. Skill steering vocabulary | Backlog | PST issue reconciliation #26 | Skill cleanup | Codify leading words or steering vocabulary where useful | Source issue said no consistent steering-vocabulary sections were found. |
| CCFG-11. Skill deletion tests | Backlog | PST issue reconciliation #27 | Skill cleanup | Run deletion tests for no-ops, sediment, and obsolete skill surfaces | Source issue said no focused deletion-test audit was found. |
| CCFG-12. Plan-batch command-owner deepening | Completed | `docs/plans/programs/codex-config/notes/command-owner-deepening-review.md` | Skill cleanup | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/closeout.md`. `plan-batch` now owns a deeper human-facing command contract for ledger-only selection, selected/queued/active state handling, one-spec output, and stop-before-implementation behavior while `architecture-program-runway` and `batch-runway` remain runtime owners. |

## Batch Queue

Queued batch:
`docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md`.

| Batch | Status | Dispatch | Spec | Covers | Notes |
|---|---|---|---|---|---|
| `ccfg-1-runner-contract-fixtures` | queued | `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md` | CCFG-1 | Contract-first extraction preparation only: implementation-neutral contract boundaries, planning-state interop fixture expectations, facade compatibility expectations, and explicit non-goals/stop conditions before any code move, repository creation, or runner extraction. |
| `ccfg-7-batch-runway-hot-path-pruning` | completed | `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/runway.md` | CCFG-7 | Closed by `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/closeout.md`. |
| `ccfg-12-plan-batch-deepening` | completed | `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/runway.md` | CCFG-12 | Closed by `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/closeout.md`. |

## Recommended Work Order

1. Start pickup from `docs/plans/CURRENT.md`, then
   `docs/plans/programs/codex-config/CURRENT.md`.
2. Execute queued CCFG-1 before CCFG-2 through CCFG-5 because runner extraction
   contracts clarify later runner workflow, skill, and diagnostic boundaries.
3. Treat CCFG-6 through CCFG-11 as skill-cleanup backlog; group only when a
   batch can stay bounded and validation can prove the cleanup.
4. Treat CCFG-7 and CCFG-12 as completed closeout evidence, not queued work.
5. Do not revive APR or PST ledgers as active pickup sources. Use their archive
   snapshots only for evidence.

## Closeout Rules

- Close CCFG-1 only after implementation-neutral contracts, planning-state
  interop fixtures, and facade compatibility checks exist or an explicit
  decision supersedes extraction.
- Close CCFG-2 only after branch mode parsing, deterministic create/reuse,
  require-mode refusal, state/receipt branch metadata, and closeout branch or
  commit-range evidence are covered without changing default runner behavior.
- Close CCFG-3 only after the review skill names its contract sources and
  separates generic-core drift from codex-config integration drift.
- Close CCFG-4 only after adapter authoring guidance points to current worker
  seams and contract sources, with test patterns and failure modes.
- Close CCFG-5 only after the requested diagnostics exist with fixture-backed
  CLI tests or are split with explicit rationale.
- Close CCFG-6 and CCFG-8 through CCFG-11 only with focused cleanup evidence,
  validation, and archive-safe closeout pointers.
- Close CCFG-12 only after `plan-batch` owns a deeper human-facing command
  contract for ledger-only selection, selected-state handling, one-spec output,
  and stop-before-implementation behavior without duplicating runtime
  ownership from `architecture-program-runway` or `batch-runway`.
