# CCFG-26 Execution-State Design Review

## Verdict

`clean` on 2026-07-19 after two initial bounded correction rounds and one fresh
review of the user-directed quality and continuation amendment.

This is independent design-review evidence. It does not select, queue, execute,
or authorize a batch.

## Exact Basis

- stable root: `/home/alacasse/projects/codex-config`;
- stable branch/revision:
  `master` / `357fb5b638137233fdf966be328630625435a7d4`;
- candidate root:
  `/home/alacasse/projects/codex-config-command-owner-redesign`;
- candidate branch/revision: `implementation/command-owner-redesign` /
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`;
- Planning State: idle and valid, with no selected, queued, or active batch;
- reviewed ADR: `../../../../adr/0003-canonical-batch-execution-state.md`;
- reviewed design:
  `ccfg-26-execution-state-design-contract.md`;
- reviewed vocabulary: root `CONTEXT.md`;
- reviewed response disposition:
  `ccfg-26-replan-analysis-and-chatgpt-pro-handoff.md`.

Graphify was not used. Both stable and candidate worktrees were clean before the
design edits.

## Corrections Required And Resolved

The first review required four material corrections:

1. move reservation and launch authorization inside the already-running public
   `work-batch` coordinator, immediately before the effectful worker launch;
2. check exact-event replay before applying current-revision CAS to a new event;
3. retain terminal result references and exact canonical receipt payloads in
   state so blocked/failed outcomes and replay remain recoverable; and
4. require a killed lock holder to release ownership so a later process can
   reacquire and inspect durable state.

The second review found one remaining gap: initialization required an explicit
compare-to-absence contract. The design now uses a tagged expected state,
serializes creation through the companion lock, handles concurrent initializers,
and defines crash/replay behavior before and after the first atomic replace.

The final review found no remaining material contradiction.

## User-Directed Amendment Review

The user-directed amendment received a fresh independent `clean` verdict on the
same stable/candidate revisions. The stable checkout contained only the pending
design and planning edits; the candidate checkout remained clean. Planning State
was valid and idle with no selected dispatch, queued batch, or active runway.

The review confirmed:

1. the execution-state owner remains a deep module with a small typed interface;
   internal classes/functions/adapters hide persistence and locking without
   creating speculative public abstractions;
2. multiple implementation slices are permitted only at semantic
   interface/behavior/test/rollback boundaries with a real consumer or
   executable acceptance path, so the amendment neither forces a monolith nor
   authorizes horizontal scaffolding;
3. `execution-flight-result/v1` is closed-world, action-free, and sufficient for
   the runner to reload canonical state, validate the exact revision/receipt,
   and derive continuation through code;
4. the outer loop lives inside the serialized `execute` phase, launches one
   fresh coordinator per Slice, and emits only one final Phase Result/receipt,
   avoiding overwrite of the current single execute-phase receipt path;
5. the temporary stable-runway policy remains intact because every individual
   `work-batch` invocation advances at most one Slice; automatic continuation
   launches a later fresh invocation rather than extending one coordinator;
6. ambiguous-attempt recovery, finalization, closeout, queue mutation, and
   successor selection remain separate and fail closed; and
7. project policy or explicit execution input resolves the run-artifact root
   once and propagates it across flights without a per-slice human prompt.

No correction was required by this amendment review.

## Clean Boundaries

- Batch Execution State is separate from run-scoped Run State and cannot become
  a second Planning State queue.
- `work-batch`, the execution-state module, `ledger-store`, Planning State, and
  the runner each have one non-overlapping semantic/mechanical role.
- The one-flight tracer has a real public caller and stops through the existing
  compatible stopped Phase Result as a deliberate acceptance milestone.
- Automatic successful continuation is a separate required CCFG-26 milestone
  with one fresh coordinator per Slice; ambiguous-attempt recovery,
  finalization, closeout, successor selection, shared/network storage, and
  multi-host coordination remain outside the initial tracer.
- The lock contract is observable across Windows, macOS, and Linux without a
  platform-specific dependency in the public interface.
- State, transition receipts, results, manifests, and Markdown have one
  canonical/derived relationship with explicit replay behavior.

## Result

The amended formal CCFG-26 design gate is satisfied. A later explicit
`plan-batch` may select one bounded execution-foundation batch whose slice count
follows semantic interface, behavior, test, and rollback boundaries, after
refreshing strict identities and resolving the exact run-artifact root from
authorized policy or execution input. This review selects no work and starts no
implementation.
