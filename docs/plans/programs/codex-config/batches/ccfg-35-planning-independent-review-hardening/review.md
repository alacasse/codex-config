# CCFG-35 Independent Planning Review

## Role And Boundary

- Reviewer role: independent read-only planning review.
- Stable basis:
  `/home/alacasse/projects/codex-config` at
  `f09e2eca6767ac11f6b5d05fd66933001667d0ea`.
- Candidate basis:
  `/home/alacasse/projects/codex-config-command-owner-redesign` at
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`.
- Implementation started: `false`.
- Planning-state or queue mutation by reviewer: none.

## Initial Review

- Dispatch SHA-256:
  `74591c5ba3f9b8703adbf25c66f7b8fb5c613d77306f55fac10f13643de3267e`
- Initial runway SHA-256:
  `9f81887b1746bc4c8e71596610e984f2a7faee160593dc3b4a9ad30b947a3fa5`
- Verdict: `correction_required`.

Corrections were limited to:

1. add the exact retained-route/failure-path disposition, observable result,
   consumer, removal owner, and terminal condition;
2. identify the widest slice and its best smaller independently useful
   alternative plus rejection reason; and
3. correct the source scenario count to nine negative cases and one positive
   ordinary-small-plan control, with an explicit row-by-row mapping.

No scope expansion, different finding, new owner, new state family, or
implementation work was requested.

## Final Exact Review Basis

- Dispatch SHA-256:
  `74591c5ba3f9b8703adbf25c66f7b8fb5c613d77306f55fac10f13643de3267e`
- Corrected runway SHA-256:
  `bdb2350c2dc8494b1403792d70bbec546a1c4fef90d3898906c63c8c93b47094`
- Verdict: `clean`.
- Corrections: none.
- Blockers: none.
- Implementation started: `false`.

## Evidence-Backed Findings

### Selection And Ownership

The exact drafts select only CCFG-35, exclude every other finding, and forbid
successor selection. Candidate public `plan-batch` remains the semantic command
owner; the registered planner and planning reviewer remain separate; installed
`scripts/plan_batch.py` remains the mechanical pre-queue boundary; the DEC-038
store remains apply-only; and Planning State remains structural.

Evidence:

- `dispatch.md`, Selection, Excluded And Deferred, and Stop Conditions.
- `runway.md`, Current Baseline, Retained Route And Failure-Path Matrix, and
  Batch Non-Goals.
- Candidate `skills/plan-batch/SKILL.md` and `scripts/plan_batch.py` at the pinned
  candidate basis.

### Retained Routes And Failure Paths

The corrected matrix records every relevant direct or compatibility caller,
current/future owner, disposition/reason, forbidden fallback, observable failure
result, exact consumer, removal owner, and terminal condition. Serialized
`select-dispatch` invokes public `plan-batch`; serialized `create-spec` remains
observation-only; CCFG-27 owns their migrate/remove decision and CCFG-29 remains
the terminal cleanup boundary. Planner, reviewer, deterministic validation,
transaction interruption/retry, and stale diagnostics all fail closed without
fallback to a displaced semantic owner.

Evidence:

- `runway.md`, Retained Route And Failure-Path Matrix.
- Candidate `docs/skill-routing-contract.md`, compatibility phase boundary.
- Candidate `scripts/plan_batch.py`, review validation and blocked-result path.

### Slice Usefulness And Proportionality

Each vertical slice has a real current consumer and leaves a usable state.
Slice 2 is correctly named as widest. Its smaller alternative—separating
success-path caller classification from failure ownership, exact consumers, and
counterfactuals—is rejected because that intermediate could still return to the
displaced owner and therefore is not independently useful. Focused per-slice
validation and heavier final-range gates avoid duplicating the measured 52- and
74-second suites.

Evidence:

- `runway.md`, Proportionality And Cost Record, Slice Shape Rationale, and the
  Current Consumer And Useful State subsection for every slice.
- Candidate focused-test measurements recorded in the runway.

### Semantic Versus Mechanical Authority

The planner and reviewer retain semantic completeness, usefulness, feasibility,
shape, and proportionality judgments. Deterministic validation is restricted to
representable shape, binding, identifiers, references, and alignment. Planning
State remains responsible only for canonical structural state. The valid small
non-migration control remains compact and accepted.

Evidence:

- `runway.md`, Planning Evidence And Applicability and Final Acceptance.
- The explicit nine-negative/one-positive scenario mapping in `runway.md`.

### Cross-Checkout And Stop Boundary

The strict planning snapshot matches the observed stable/candidate revisions,
keeps stable planning writes separate from candidate implementation writes,
requires fresh live leases for execution handoffs, prohibits stable-home
mutation, and stops without implementation or successor selection.

Evidence:

- `runway.md`, Planning Snapshot, Execution Contract, Final Validation, Batch
  Stop Conditions, and Closeout Boundary.

## Authorization Result

The exact dispatch and corrected runway above are independently reviewed clean
and may be recorded as the sole queued CCFG-35 plan. Any change to either draft
invalidates this result and requires a fresh independent planning review before
queue mutation.
