# CCFG-35 Master Planner And Independent Review Hardening Dispatch

## Selection

- Batch ID: `CCFG-35`.
- Batch slug: `ccfg-35-master-planner-review-hardening`.
- Source ledger:
  `docs/plans/programs/codex-config/LEDGER.md`.
- Source finding:
  `docs/plans/programs/codex-config/findings/planning-and-independent-review-hardening.md`.
- Superseded predecessor:
  `docs/plans/programs/codex-config/batches/ccfg-35-planning-independent-review-hardening/superseded.md`.
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-35-master-planner-review-hardening/runway.md`.
- Bounded proof-lane amendment:
  `docs/plans/programs/codex-config/batches/ccfg-35-master-planner-review-hardening/amendment.md`.
- Authoritative amendment review:
  `docs/plans/programs/codex-config/batches/ccfg-35-master-planner-review-hardening/amendment-review.md`.
- Selection authority: the user's explicit 2026-07-20 instruction to supersede
  the queued candidate-targeted plan, restore CCFG-35 to `Open`, amend the
  finding with master-only implementation authority, and replan from the
  planner actually used on master.
- Implementation started: `false`.

No other finding is selected, prepared, implemented, or closed by this batch.

## Supersession And Lifecycle Transition

The predecessor dispatch/runway/review is historical and non-executable. Its
candidate-targeted clean review cannot authorize replacement queue mutation.
CCFG-35 returned to `Open` after supersession and before this replacement
dispatch was created. If this exact replacement dispatch/runway receives a
fresh clean review, canonical program state may mark CCFG-35 `Pending` and queue
only the replacement runway.

## Exact Planning Basis

- Canonical repository and sole implementation root:
  `/home/alacasse/projects/codex-config`.
- Required implementation branch: `master`.
- Master revision inspected for this plan:
  `a701a5a9d8810e67ad193f2955eea24a4886007b`.
- Stable Codex home: `/home/alacasse/.codex`.
- Candidate evidence-only repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign` at
  `5c5ec9d52dd9033daa45f3a200031c152363b62c` on
  `implementation/command-owner-redesign`.

This is an ordinary single-root implementation batch. The candidate identity is
recorded only to prevent accidental reuse of the superseded target. The runway
must not carry `cross-checkout-context/v1`, candidate-home installation, or
candidate write authority.

## Actual Master Planner Route

The currently observed planner used by the stable session is:

```text
/home/alacasse/.codex/skills/plan-batch
  -> /home/alacasse/projects/codex-config/skills/plan-batch
  -> public plan-batch command contract
  -> Architecture Program Runway selection, dispatch, and queue ownership
  -> Batch Runway create-spec semantic planning
  -> queue mutation under coordinator practice
```

The current reusable master contract does not yet require evidence-backed
independent planning review before queue mutation. The accepted target route
adds, between create-spec and queue mutation, one separate read-only planning
reviewer that independently reconstructs facts, binds them to the exact drafts,
and returns `approve`, `revise`, or `block`. Only `approve` with planner=`plan`,
valid exact binding, matching hashes, and required evidence may map to
`queue_decision: authorized`. The aggregate exact planning review separately
returns `clean`, `correction_required`, or `blocked`.

At the planning basis:

- `skills/plan-batch/SKILL.md` is the installed public owner;
- `skills/architecture-program-runway/SKILL.md` owns dispatch and queue state;
- `skills/batch-runway/references/create-spec.md` is the semantic create-spec
  procedure;
- `codex-features.json` installs the `plan-batch` skill directory and its
  existing support dependencies;
- no master `batch_planner`, `batch_plan_reviewer`, `scripts/plan_batch.py`,
  `scripts/planning_contract.py`, or planning schema family exists; and
- `runway_reviewer` remains the implementation-diff reviewer and must not be
  repurposed as the planning reviewer.

## Goal

Harden the actual master planning route so a semantically incomplete plan
cannot enter the queue through an evidence-free reviewer `approve`, while ordinary
small non-substitutive plans remain proportionate. Require accepted closeout
evidence that independently proves the resulting planner is the one installed
from master.

## Batch Kind And Risk

- Batch kind: `mixed-risk`.
- Slice 1 risk: `contract-narrowing`; it makes an exact evidence-backed
  independent planning review a precondition for queue authorization.
- Slice 2 risk: `contract-narrowing`; it makes applicable replacement,
  failure-path, consumer, counterfactual, feasibility, and proportionality
  omissions correct-or-block conditions.
- Approval gate for both slices: the user's later explicit `work-batch` while
  this exact master-only runway plus its reviewed amendment is the sole queue
  entry, master identity still matches, the prior slice is green where
  applicable, and the independent reviewer has accepted the exact preceding
  basis. That invocation authorizes Slice 1 only. Slice 2 additionally requires
  the measured smoke receipt, a separate clean cost-gate review, and explicit
  user approval of the recorded final-lane estimate.

## Included Scope

- The public master `plan-batch` command contract.
- The master create-spec semantic planning procedure.
- Architecture Program Runway's pre-queue acceptance boundary.
- A reusable planning-review handoff/result contract implemented within the
  installed master planner surface, without adding a registered agent role.
- Exact draft binding and mechanically representable evidence-reference checks.
- Applicable semantic replacement, failure-path, current-consumer,
  counterfactual, feasibility, slice-alternative, and proportionality duties.
- Focused master-route regression evidence, including nine negative scenarios
  and one valid ordinary-small-plan control.
- One batched planner invocation and one different batched reviewer invocation
  over those ten isolated packets, followed by ten separately applied and
  verified queue decisions; no per-scenario live invocation.
- One two-packet batched smoke after Slice 1, with actual duration, call/input
  size, retry, model/effort/token availability, and final-lane extrapolation
  recorded before Slice 2 may be authorized.
- Exact-commit validation receipts reusable by later reviewers until their
  commit, command, input, dependency, configuration, or environment identity
  changes.
- Directly associated workflow/routing documentation, manifest version,
  changelog, and tests.
- Final installed-master and accepted-closeout provenance proof.

## Explicitly Excluded

- All implementation writes in
  `/home/alacasse/projects/codex-config-command-owner-redesign`.
- All writes or installs in `/home/alacasse/.codex-command-owner-redesign`.
- Candidate-only `agents/batch_planner.toml`,
  `agents/batch_plan_reviewer.toml`, `scripts/plan_batch.py`,
  `scripts/planning_contract.py`, planning schemas, planning transactions,
  scenario adapters, and candidate-only tests.
- A new registered agent role, top-level schema family, persistent state store,
  queue owner, planning command, or compatibility wrapper.
- A permanent live-evaluation service, ordinary-workflow live-model gate, or
  one live planner/reviewer pair per scenario.
- Repurposing `agents/runway_reviewer.toml` as the planning reviewer.
- Project-, ledger-, branch-, checkout-, or Graphify-specific behavior in
  reusable skills.
- Deterministic claims about semantic completeness, usefulness, feasibility
  quality, slice preference, or cost acceptability.
- CCFG-26 or any other finding, execution/finalization redesign, and successor
  selection.

## Required Closeout Proof

Closeout is not acceptable merely because source files, tests, or manifest text
changed. The final independent review must reconstruct and record:

1. the exact accepted commit range on `master`;
2. the changed master route from public `plan-batch` through create-spec,
   independent planning review, and queue authorization;
3. behavioral evidence that applicable bad plans correct or block,
   evidence-free reviewer `approve` cannot queue, and the valid small plan still
   queues, using one planner batch, one independent reviewer batch, and ten
   separately verified isolated queue decisions;
4. a counterfactual showing removal or bypass of the new master gate fails;
5. `codex_owner.py` ownership for every changed installed route feature;
6. `readlink -f`, accepted-commit blob hashes, installed-content hashes, and
   installer status/dry-run proving every changed installed route file resolves
   to the exact accepted master commit rather than only the mutable worktree;
7. absence of candidate implementation or candidate-home installation; and
8. exact smoke and final-lane cost receipts, including the independent
   cost-gate decision and explicit user approval before Slice 2;
9. the canonical planner/reviewer/queue verdict mapping and evidence that every
   non-positive or missing input fails closed; and
10. exact closeout evidence consumed by same-batch reconciliation.

## Slice Shape

Use two vertical slices:

1. establish the evidence-backed independent planning-review gate on the actual
   master queue path;
2. use that gate to harden applicable semantic planning and prove the complete
   scenario set plus installed-master provenance.

`1 -> 2` is a valid producer/consumer boundary: after Slice 1, exact evidence-
backed review is already required before queueing; Slice 2 adds the broader
semantic facts and behavioral falsification that the gate consumes. Combining
both would make one review boundary span queue authority, semantic planning,
scenario proof, documentation, and installation provenance.

## Stop Conditions

Stop before runway creation or execution if:

- master is not the sole implementation branch/root;
- the installed stable planner does not resolve to this master repository;
- the replacement plan reuses candidate-only machinery or strict cross-checkout
  execution;
- the actual planning-review handoff and queue decision cannot be identified;
- the design adds a new agent role, top-level schema/state family, queue owner,
  compatibility route, or deterministic semantic authority;
- an evidence-free reviewer `approve` can still authorize queue mutation;
- the accepted closeout can pass without proving the changed planner is the
  stable installed master planner;
- behavior evidence consists only of string, manifest, schema, or fixture-
  self-attestation checks;
- the proof lane requires more than one planner plus one distinct reviewer
  invocation for the smoke or final ten-packet batch, except a recorded single
  transport-only retry;
- Slice 2 lacks the measured smoke receipt, independent clean cost-gate review,
  or explicit user approval of its final-lane estimate;
- verdict vocabularies do not map unambiguously to one fail-closed queue
  authorization result;
- a same-commit validation gate is rerun without an invalidated receipt or
  material reason;
- reusable rules receive project-specific paths, identities, topology, or
  Graphify assumptions; or
- any unrelated finding is selected, prepared, implemented, or closed.
