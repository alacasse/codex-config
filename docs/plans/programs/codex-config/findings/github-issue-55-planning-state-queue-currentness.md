# GitHub Issue 55: Planning State Queue Currentness Authority

## Source

- GitHub issue: https://github.com/alacasse/codex-config/issues/55
- Title: Make Planning State authoritative for queue currentness and remove Git
  transaction inference
- State when ingested: open
- Labels when ingested: `ready-for-agent`
- Created: 2026-07-14
- Updated when ingested: 2026-07-14
- Source identity: GitHub issue #55, authored by `alacasse`

## Summary

CCFG-31 replaced the broad CCFG-30 startup protocol with a narrow mechanical
`ready`/`blocked` preflight, but its remaining implementation still asks Git to
infer a semantic planning fact: whether canonical-planning repository movement
is the exact transaction that established the current queue.

The current path accepts caller-declared queue transaction paths, walks the
commit range from the planning snapshot to live `HEAD`, combines committed and
workspace paths, and fingerprints planning files during preparation. This is a
remaining ownership leak, not a reason to build a stronger Git archaeology
protocol.

This finding is a deletion-oriented correction after closed CCFG-31. It does
not reopen CCFG-31 or authorize a new planning-transaction schema.

## Ownership Decision

### Planning State owns semantic currentness

Before cross-checkout startup invokes its mechanical helper, `work-batch` must
use Planning State `current` and `validate` as the sole authority for:

- selected or queued batch identity;
- current dispatch, runway, and source scope;
- amendment, replacement, supersession, abandonment, or replanning state; and
- whether execution may consume that planning state.

If Planning State cannot prove those facts, `work-batch` stops before helper
invocation. Cross-checkout code must not reconstruct or second-guess them from
Git history.

Transaction IDs, runway digests, amendment identity, or stronger same-path
mutation detection remain future Planning State and planning-artifact contract
work under CCFG-21 and CCFG-25, not additions to this finding.

### Git owns material execution integrity

After Planning State is green, the helper may verify only mechanical facts
needed for an exact live handoff:

- repository roots and Git repository identity;
- generation, active helper, and `CODEX_HOME` binding;
- the implementation repository's expected accepted baseline;
- current live toolchain and canonical-planning revisions;
- unchanged strict parsing of the refreshed context;
- absence of relevant repository movement during preparation; and
- later handoff identity against the last accepted implementation commit and
  exact reviewed diff.

Git remains appropriate for worker and reviewer diff bases, accepted slice
commits, rollback, and material movement after lease preparation. It is not a
second batch lifecycle authority.

Branch and dirty-file checks remain ordinary target-policy and scope-conflict
concerns. They must not become queue identity or new cross-checkout payload
fields.

## Required Deletion

Remove from the normal cross-checkout startup path:

- the `queue_transaction_paths` input;
- commit-range path collection used to explain planning movement;
- `_capture_queue_transaction_paths(...)`;
- queue-state file fingerprinting;
- helper-only Git path/status utilities and imports that become unused;
- workflow prose requiring exact queue-path supply or Git interpretation of
  queue establishment; and
- tests whose only purpose is committed, uncommitted, or combined queue-path
  classification.

The narrow helper may remain `ready`/`blocked`, but its result concerns only
material live-context preparation. Prefer folding it into
`prepare_cross_checkout_context_refresh(...)` when that removes more topology;
retain both APIs only for a named current caller with a removal condition.

## Preserved Behavior

- Green Planning State plus an unchanged implementation baseline may produce a
  fresh strict context even when the stable toolchain or canonical-planning
  `HEAD` advanced after the historical planning snapshot.
- Implementation movement without an accepted prior action remains blocked.
- Root, generation, helper, active `CODEX_HOME`, strict-context, and movement
  mismatches remain blocked.
- Movement during live-context preparation remains blocked.
- Fresh per-handoff leases, strict parsing, write-scope validation, verified
  result echo, accepted-action receipts, and exact reviewer diff bases remain
  protected.
- Unrelated dirty files remain preserved and outside queue semantics.

## Scope And Planning Constraints

- Expected shape: one cohesive deletion-oriented slice. A second slice needs an
  independent owner, risk, validation, or rollback boundary plus user approval
  before planning.
- Add no agent, lifecycle state, planning artifact, planning schema,
  transaction ID, digest format, movement taxonomy, compatibility engine,
  repository scanner, public command, or parallel bridge version.
- Do not add branch fields to `cross-checkout-context/v1`.
- Do not modify historical CCFG-30 or CCFG-31 planning artifacts.
- Do not modify the command-owner redesign candidate or absorb CCFG-21 through
  CCFG-29.
- CCFG-29 remains the sole bridge-removal owner.
- Combined production helper and reusable workflow-contract code must have a
  negative line delta unless the user explicitly approves a named exception.
- Any retained queue-transaction helper or test must name a current caller and
  a removal condition.
- Issue #54 already permits the expected one-slice runway.

## Intake Decision

- Ledger identity: `CCFG-32`.
- Finding status: `Open`.
- Dependencies: none.
- No batch is selected, queued, or active by this intake.
- A future explicit `plan-batch` request owns selection and must preserve the
  Planning State/Git ownership split, deletion goal, one-slice shape, and
  material handoff-integrity checks above.
