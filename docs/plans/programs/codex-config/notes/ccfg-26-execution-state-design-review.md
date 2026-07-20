# CCFG-26 Execution-State Design Review

> **Historical evidence.** This review applies only to the rejected design
> superseded by
> [ADR 0004](../../../../adr/0004-single-generation-command-owner-development-boundary.md)
> and the
> [execution-state foundation supersession](../batches/ccfg-26-execution-state-foundation/superseded.md).
> It is not current planning or execution authority.

## Verdict

`clean` on 2026-07-19 after two initial bounded correction rounds, one fresh
review of the user-directed quality and continuation amendment, and one final
bounded portability and first-batch-scope review.

This is independent design-review evidence. It does not select, queue, execute,
or authorize a batch.

## Exact Basis

- stable root: `/home/alacasse/projects/codex-config`;
- stable branch/revision:
  `master` / `cc79a52544f80bcb4f59bad98e51349b441978ce`;
- candidate root:
  `/home/alacasse/projects/codex-config-command-owner-redesign`;
- candidate branch/revision: `implementation/command-owner-redesign` /
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`;
- Planning State: idle and valid, with no selected, queued, or active batch;
- reviewed ADR: `../../../../adr/0003-canonical-batch-execution-state.md`,
  SHA-256 `6ac1362467e4b32d28cc050fa314e8e825b143769114fd08a3ad08ea8a9606e8`;
- reviewed design:
  `ccfg-26-execution-state-design-contract.md`, SHA-256
  `4c846deef22c46ca14f60821c8ff623de9e70b4b8676c800f2b87e8713f582b6`;
- reviewed vocabulary: root `CONTEXT.md`, SHA-256
  `c3e698ab0f8897dfd23b3372f3ea921c5c2392c511f9708e46b8ac2168fe9163`;
- reviewed response disposition:
  `ccfg-26-replan-analysis-and-chatgpt-pro-handoff.md`, SHA-256
  `cfbf4c480c1f5a5f60076cbbaf8f73580af18fc8fb57fa614d8402a22180a34a`.

Graphify was not used. Both stable and candidate worktrees were clean before the
follow-up edits. The candidate remained clean and unchanged during review.

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

The user-directed amendment received a fresh independent `clean` verdict against
the then-current stable baseline
`357fb5b638137233fdf966be328630625435a7d4` and candidate
`5c5ec9d52dd9033daa45f3a200031c152363b62c`. The stable checkout contained only
the pending design and planning edits; the candidate checkout remained clean.
Planning State was valid and idle with no selected dispatch, queued batch, or
active runway.

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

## Follow-Up Portability And Scope Review

The final bounded review returned `clean` on the exact basis above. It
confirmed:

1. bounded generated-only implementation and acceptance roots are caller- or
   harness-supplied absolute temporary directories allocated through the host
   platform facility; no platform-specific temporary path is a contract input;
2. automatic successful continuation remains required before normal CCFG-26 use
   or closeout, but enters the first execution-foundation batch only when
   planning proves a proportionate shared semantic, validation, and rollback
   boundary;
3. the at-least-two-Slice condition belongs only to the public tracer fixture or
   acceptance runway used to observe `continue_same_batch`, not to the CCFG-26
   implementation runway;
4. the real runner caller under validation belongs to the candidate target or
   its executable fixture, while the stable controller continues to orchestrate
   through existing mechanisms without loading candidate code as runtime
   authority; and
5. `CURRENT.md`, `LEDGER.md`, the direction finding, ADR, design contract,
   handoff, and changelog agree that the program remains idle and that no
   dispatch, runway, implementation, or successor was created.

The temporary stable-runway dogfooding policy remains intact: one
`work-batch` invocation still advances at most one implementation Slice, and an
automatic continuation loop may only launch a later fresh invocation.

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
`plan-batch` may select the first bounded execution-foundation batch. It must end
in one independently useful state through the real candidate
runner/`work-batch` seam, and automatic continuation belongs to it only if the
planner proves the combined boundary proportionate. The planner must derive the
Slice count from semantic interface, behavior, test, and rollback boundaries,
refresh strict identities, and resolve the exact run-artifact root from
authorized policy or execution input. This review selects no work and starts no
implementation.
