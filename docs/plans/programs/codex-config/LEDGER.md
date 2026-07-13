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
- Command-owner redesign intake:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md`
- Authoritative command-owner redesign packet:
  `https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md`
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
| CCFG-1. Contract-first runner business-logic extraction | Completed | APR-26 | Runner extraction | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/closeout.md` as contract/fixture preparation only. External OSS runner remains possible, but CCFG-1 did not move code, create a repo skeleton, choose package/runtime basics, implement extraction, or complete CCFG-2 through CCFG-5 scope. |
| CCFG-2. Branch-per-batch runner isolation mode | Open | APR-27; GitHub issue #11 | Runner workflow | Design after CCFG-1 clarifies the generic runner boundary | Preserve source scope: `--batch-branch-mode none\|create\|require`, deterministic branch naming, state/receipt branch metadata, and closeout commit-range evidence remain unimplemented. |
| CCFG-3. Contract-drift review skill | Open | APR-28; GitHub issue #14 | Runner support skill | Create only when extraction work starts to drift across boundaries | The requested skill should compare extraction changes against APR/PBC contracts, facade compatibility, generic-core boundaries, and stale-plan/archive risks without duplicating the full contract text. |
| CCFG-4. Runner adapter authoring skill | Open | APR-29; GitHub issue #16 | Runner support skill | Create after CCFG-1 stabilizes the generic worker/runtime boundary | Preserve adapter guidance scope: provider quirks stay out of generic runner core; cover result, receipt, transition, artifact, observation, and input-inventory boundaries. |
| CCFG-5. Baton dogfood diagnostics | Open | APR-30; GitHub issues #17, #18, #19 | Runner diagnostics | Sequence after CCFG-1 unless a diagnostic need blocks extraction | `baton-context-map`, `baton-doctor`, and `baton-receipt-inspector` should read runner/planning artifacts and produce compact diagnostics, not reconstruct execution from chat transcripts. |
| CCFG-6. Skill-slimmer support | Backlog | PST issue reconciliation #15 | Skill cleanup | Decide whether to add a focused skill-slimmer workflow | Source issue said the `skill-slimmer` skill does not exist. Keep this as cleanup backlog until a bounded workflow and validation target are selected. |
| CCFG-7. Batch Runway hot-path pruning | Completed | PST issue reconciliation #23 | Skill cleanup | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/closeout.md`. Batch Runway routine execution now has a guarded compact read path, non-routine references remain trigger-loaded, and runtime semantics remain owned by the same Batch Runway contracts. |
| CCFG-8. Ledger and dispatch rule dedupe | Completed | PST issue reconciliation #24 | Skill cleanup | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`. The batch added a single owner map, deduplicated command-owner and support-skill rule prose, aligned cross-doc summaries, and changed no runtime behavior. |
| CCFG-9. Short skill frontmatter descriptions | Backlog | PST issue reconciliation #25 | Skill cleanup | Shorten dense skill descriptions without losing trigger accuracy | Source issue said this is not done consistently. |
| CCFG-10. Skill steering vocabulary | Backlog | PST issue reconciliation #26 | Skill cleanup | Codify leading words or steering vocabulary where useful | Source issue said no consistent steering-vocabulary sections were found. |
| CCFG-11. Skill deletion tests | Open | PST issue reconciliation #27 | Skill cleanup | Future explicit `plan-batch` request can regenerate, split, block, or narrow the displaced runway only after applying validation-command status classes, batch kind, slice risk classes, required approval gates, and the CCFG-15 vague-row guard | Source issue said no focused deletion-test audit was found. The previous queued dispatch/runway was displaced by CCFG-13 and amended by CCFG-14 and CCFG-15 as superseded planning evidence only; CCFG-11 remains open skill-cleanup work and must not execute from the displaced artifact. |
| CCFG-12. Plan-batch command-owner deepening | Completed | `docs/plans/programs/codex-config/notes/command-owner-deepening-review.md` | Skill cleanup | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/closeout.md`. `plan-batch` now owns a deeper human-facing command contract for ledger-only selection, selected/queued/active state handling, one-spec output, and stop-before-implementation behavior while `architecture-program-runway` and `batch-runway` remain runtime owners. |
| CCFG-13. Validation command status classification | Completed | GitHub issue #29; `docs/plans/programs/codex-config/findings/github-issue-29-validation-command-status.md` | Batch Runway create-spec | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/closeout.md`. Batch Runway create-spec guidance and contract tests now classify generated validation commands before execution gates, and the displaced CCFG-11 runway records required future classification/regeneration. |
| CCFG-14. Batch kind and destructive-slice risk gates | Completed | GitHub issue #30; `docs/plans/programs/codex-config/findings/github-issue-30-batch-kind-slice-risk.md` | Batch Runway create-spec | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/closeout.md`. Batch Runway create-spec guidance and focused contract tests now require generated dispatch/runway artifacts to declare batch kind, require risky slices to declare risk classes, and require destructive or contract-narrowing work to carry explicit approval gates. |
| CCFG-15. Vague ledger row splitting before runway expansion | Completed | GitHub issue #33; `docs/plans/programs/codex-config/findings/github-issue-33-vague-ledger-row-splitting.md` | Plan-batch / program runway planning guard | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/closeout.md`. `plan-batch` and `architecture-program-runway` now require vague or mixed-risk ledger rows to be split, blocked, or narrowed before selected dispatch and concrete runway creation. CCFG-11 remains open and must not resume from the displaced runway without applying this guard. |
| CCFG-16. Deletion-test vocabulary ownership | Completed | GitHub issue #31; `docs/plans/programs/codex-config/findings/github-issue-31-deletion-test-vocabulary-ownership.md` | Skill cleanup / deletion-test evidence vocabulary | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/closeout.md`. `dead-surface-audit` owns canonical deletion-test evidence vocabulary; `legacy-removal`, `architecture-program-runway`, and `batch-runway` consume canonical statuses or locally defined non-canonical labels; focused CCFG-like regression coverage prevents unsupported generated deletion categories. Runtime behavior unchanged. |
| CCFG-17. Absolute runway reference paths | Completed | GitHub issue #32; `docs/plans/programs/codex-config/findings/github-issue-32-absolute-runway-reference-paths.md` | Batch Runway create-spec | None | Closed by `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/closeout.md`. Batch Runway create-spec guidance now prefers repo-relative or skill-relative reusable skill references, focused tests guard the guidance and active generated artifacts, and completed historical runways were not rewritten. |
| CCFG-18. Establish Stable and Candidate Generations | Open | [COR-001](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-001--establish-stable-and-candidate-generations) | Command-owner redesign / isolation | A future `plan-batch` may select or narrow this dependency-free item | Source identity `COR-001`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-001). Unselected. |
| CCFG-19. Verify Source Contracts and Resolve Blocking Decisions | Open | [COR-002](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-002--verify-source-contracts-and-resolve-blocking-decisions) | Command-owner redesign / contracts | Wait for CCFG-18 (`COR-001`) | Source identity `COR-002`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-002). Unselected. |
| CCFG-20. Implement `skill-contract/v1` Schema and Validators | Open | [COR-003](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-003--implement-skill-contractv1-schema-and-validators) | Command-owner redesign / skill contracts | Wait for CCFG-19 (`COR-002`) | Source identity `COR-003`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-003). Unselected. |
| CCFG-21. Implement Planning Artifact Schemas and Validators | Open | [COR-004](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-004--implement-planning-artifact-schemas-and-validators) | Command-owner redesign / planning contracts | Wait for CCFG-19 (`COR-002`) | Source identity `COR-004`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-004). Unselected. |
| CCFG-22. Finalize and Validate `skill-authoring` v1 | Open | [COR-005](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-005--finalize-and-validate-skill-authoring-v1) | Command-owner redesign / authoring | Wait for CCFG-20 and CCFG-21 (`COR-003`, `COR-004`) | Source identity `COR-005`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-005). Unselected. |
| CCFG-23. Build the Topology-Independent Behavioral Scenario Harness | Open | [COR-006](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-006--build-the-topology-independent-behavioral-scenario-harness) | Command-owner redesign / behavioral harness | Wait for CCFG-21 and CCFG-22 (`COR-004`, `COR-005`) | Source identity `COR-006`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-006). Unselected. |
| CCFG-24. Transfer Intake Ownership to `add-to-ledger` | Open | [COR-007](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-007--transfer-intake-ownership-to-add-to-ledger) | Command-owner redesign / intake ownership | Wait for CCFG-22 and CCFG-23 (`COR-005`, `COR-006`) | Source identity `COR-007`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-007). Unselected. |
| CCFG-25. Transfer Planning Ownership to `plan-batch` | Open | [COR-008](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-008--transfer-planning-ownership-to-plan-batch) | Command-owner redesign / planning ownership | Wait for CCFG-24 (`COR-007`) | Source identity `COR-008`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-008). Unselected. |
| CCFG-26. Transfer Execution and Closeout Ownership to `work-batch` | Open | [COR-009](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-009--transfer-execution-and-closeout-ownership-to-work-batch) | Command-owner redesign / execution ownership | Wait for CCFG-25 (`COR-008`) | Source identity `COR-009`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-009). Unselected. |
| CCFG-27. Cut Over Runner, Manifest, Agents, and Installation | Open | [COR-010](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-010--cut-over-runner-manifest-agents-and-installation) | Command-owner redesign / cutover | Wait for CCFG-26 (`COR-009`) | Source identity `COR-010`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-010). Unselected. |
| CCFG-28. Delete Architecture Program Runway and Batch Runway | Open | [COR-011](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-011--delete-architecture-program-runway-and-batch-runway) | Command-owner redesign / legacy owner deletion | Wait for CCFG-27 (`COR-010`) | Source identity `COR-011`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-011). Unselected; distinct from CCFG-11 deletion-test work. |
| CCFG-29. Perform Contract-First Authoring Convergence | Open | [COR-012](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-012--perform-contract-first-authoring-convergence) | Command-owner redesign / authoring convergence | Wait for CCFG-28 (`COR-011`) | Source identity `COR-012`; [preserved intake details](findings/command-owner-redesign-implementation-intake.md#cor-012). Unselected. |

## Batch Queue

Queued batch: None.

| Batch | Status | Dispatch | Spec | Covers | Notes |
|---|---|---|---|---|---|
| `ccfg-1-runner-contract-fixtures` | completed | `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md` | CCFG-1 | Closed by `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/closeout.md`. Contract-first extraction preparation only: implementation-neutral contract boundaries, planning-state interop fixture expectations, facade compatibility checks, explicit non-goals/stop conditions, and unresolved extraction decisions before any code move, repository creation, package scaffold, hidden planning-state dependency, archived-ledger archaeology, or runner extraction. |
| `ccfg-8-ledger-dispatch-rule-dedupe` | completed | `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/runway.md` | CCFG-8 | Closed by `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`. Runtime behavior unchanged. |
| `ccfg-7-batch-runway-hot-path-pruning` | completed | `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/runway.md` | CCFG-7 | Closed by `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/closeout.md`. |
| `ccfg-12-plan-batch-deepening` | completed | `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/runway.md` | CCFG-12 | Closed by `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/closeout.md`. |
| `ccfg-11-skill-deletion-tests` | superseded | `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/runway.md` | CCFG-11 | Displaced by CCFG-13 at explicit user request. The displaced runway now records validation-command status, batch-kind/risk-gate, and vague-row guard prerequisites as planning evidence only; CCFG-11 remains open and must be regenerated, split, blocked, or narrowed before execution. |
| `ccfg-13-validation-command-status` | completed | `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md` | CCFG-13 | Closed by `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/closeout.md`. Runtime behavior unchanged. |
| `ccfg-14-batch-kind-slice-risk` | completed | `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/runway.md` | CCFG-14 | Closed by `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/closeout.md`. Runtime behavior unchanged. |
| `ccfg-15-vague-ledger-row-splitting` | completed | `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/runway.md` | CCFG-15 | Closed by `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/closeout.md`. Runtime behavior unchanged. |
| `ccfg-16-deletion-test-vocabulary-ownership` | completed | `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/runway.md` | CCFG-16 | Closed by `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/closeout.md`. Runtime behavior unchanged. |
| `ccfg-17-absolute-runway-reference-paths` | completed | `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/runway.md` | CCFG-17 | Closed by `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/closeout.md`. Runtime guidance changed for generated reference paths; historical completed runways were not rewritten. |

## Recommended Work Order

1. Start pickup from `docs/plans/CURRENT.md`, then
   `docs/plans/programs/codex-config/CURRENT.md`.
2. No batch is currently selected, queued, or active. A future explicit
   `plan-batch` request can select exactly one next batch from this ledger.
3. Treat CCFG-18 through CCFG-29 as the unselected command-owner redesign
   intake. Preserve their `COR-*` identities and dependencies; CCFG-18
   (`COR-001`) is the first dependency-free redesign item.
4. Treat CCFG-6 and CCFG-9 through CCFG-10 as skill-cleanup backlog;
   group only when a batch can stay bounded and validation can prove the
   cleanup.
5. Treat CCFG-11 as open skill-cleanup work; do not execute the displaced
   CCFG-11 runway as active state. Replan, split, block, or narrow it only with
   an explicit `plan-batch` request that applies the CCFG-13 validation-status,
   CCFG-14 risk-gate, CCFG-15 vague-row, and CCFG-16 deletion-test vocabulary
   guards.
6. Treat CCFG-17 as completed closeout evidence, not queued work.
7. Treat CCFG-1, CCFG-7, CCFG-8, and CCFG-12 through CCFG-17 as completed
   closeout evidence, not queued work.
8. Do not revive APR or PST ledgers as active pickup sources. Use their archive
   snapshots only for evidence.

## Closeout Rules

- CCFG-1 is closed only as contract/fixture preparation evidence. Its closeout
  must not be read as runner extraction, package/runtime selection, repository
  or scaffold creation, adapter implementation, or CCFG-2 through CCFG-5 scope
  completion.
- Close CCFG-2 only after branch mode parsing, deterministic create/reuse,
  require-mode refusal, state/receipt branch metadata, and closeout branch or
  commit-range evidence are covered without changing default runner behavior.
- Close CCFG-3 only after the review skill names its contract sources and
  separates generic-core drift from codex-config integration drift.
- Close CCFG-4 only after adapter authoring guidance points to current worker
  seams and contract sources, with test patterns and failure modes.
- Close CCFG-5 only after the requested diagnostics exist with fixture-backed
  CLI tests or are split with explicit rationale.
- Close CCFG-6, CCFG-9 through CCFG-11, and CCFG-16 only with focused cleanup
  evidence, validation, and archive-safe closeout pointers.
- Close CCFG-12 only after `plan-batch` owns a deeper human-facing command
  contract for ledger-only selection, selected-state handling, one-spec output,
  and stop-before-implementation behavior without duplicating runtime
  ownership from `architecture-program-runway` or `batch-runway`.
- Close CCFG-13 only after Batch Runway create-spec guidance and focused
  contract tests classify generated validation commands as required-green,
  known-red-baseline, implementation-created, conditional, or diagnostic-only,
  and prevent known-red or missing future-created tests from becoming silent
  required-green gates.
- Close CCFG-14 only after Batch Runway create-spec guidance and focused
  contract tests require generated dispatch/runway artifacts to declare batch
  kind, require risk classes for destructive or contract-narrowing slices, and
  prevent evidence-only batches from carrying destructive cleanup slices without
  explicit mixed-risk metadata and approval gates.
- Close CCFG-15 only after `plan-batch` / `architecture-program-runway`
  guidance and focused tests or fixtures require vague or mixed-risk ledger
  rows to be split, blocked, or narrowed before selected dispatch and concrete
  runway creation, with CCFG-11-like deletion-test scope covered.
- Close CCFG-16 only after canonical deletion-test vocabulary ownership is
  defined, generated dispatch/runway guidance uses canonical terms or local
  non-canonical labels explicitly, owner/consumer boundaries are aligned across
  `dead-surface-audit`, `legacy-removal`, `batch-runway`, and
  `architecture-program-runway`, and focused regression coverage prevents
  CCFG-like runways from inventing unsupported deletion categories.
- Close CCFG-17 only after Batch Runway create-spec guidance stops requiring
  local absolute paths for reusable repo-owned skill references, generated
  active runways use repo-relative or skill-relative paths for those
  references, focused tests cover both the guidance and generated-artifact
  guard, and any remaining absolute-path allowance is limited to
  project-specific values or runtime handoffs.
- Close CCFG-18 through CCFG-29 only from the acceptance evidence and
  stop/planning boundary preserved in each corresponding `COR-*` section of
  `docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md`.
