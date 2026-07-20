# CCFG-26 Execution-State Foundation Superseded

## Status

Superseded by explicit user direction on 2026-07-19.

This batch is not executable, resumable, amendable, closable, or authoritative
for a replacement Slice sequence.

## Reason

The batch was planned from the wrong architectural boundary. It mixed the future
extractable product with codex-config's temporary installation and dogfooding
mechanics, required a separate runtime root without a user need, and expanded the
filesystem threat model beyond the intended trusted-local product.

The failed Slice 1 review later exposed the cost of that expansion: the plan
required cross-platform protection against hostile same-user namespace
substitution without having selected or proven the Windows implementation
primitive. The replacement direction deliberately removes that requirement
rather than continuing to patch toward it.

## Durable Outcome

- No Slice was accepted.
- No candidate CCFG-26 implementation commit exists.
- No real Batch Execution State exists.
- Slice 2 never started.
- No closeout or successor exists.
- The dispatch, runway, reviews, amendment, execution report, and retrospective
  remain historical evidence only.

## Candidate Worktree

The uncommitted candidate files are preserved under the user's control. This
supersession does not delete, reset, commit, modify, or authorize reuse of those
files.

Agents must not read the preserved worktree as the replacement specification or
continue editing it unless the user later gives explicit authority. Any future
execution that overlaps those paths must stop until the user has isolated or
resolved the worktree.

## Replacement Authority

Future CCFG-26 planning must use:

- `docs/adr/0004-extraction-first-batch-local-execution.md`;
- `docs/plans/programs/codex-config/findings/ccfg-26-product-dogfood-reset.md`;
- COR-009's original user-visible execution and closeout outcome;
- the permanent product/dogfood, threat-model, and feasibility planning gates.

ADR 0003 and the detailed execution-state contract remain provenance for the
failed approach, not live architecture authority.

## Queue Disposition

The queue is cleared. CCFG-26 returns to planning-ready state only; no replacement
batch or successor is selected by this notice.
