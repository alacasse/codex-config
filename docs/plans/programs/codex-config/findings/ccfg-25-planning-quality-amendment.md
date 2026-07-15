# CCFG-25 Planning Quality Amendment

## Purpose

Amend COR-008 / CCFG-25 so the future candidate `plan-batch` owner cannot queue
an over-specified runway merely because its proposed design is complete and
internally consistent.

This amendment carries the substantive requirements from GitHub issues #51,
#52, and #54 into the canonical program source. A future CCFG-25 planner must
read this file from the ledger and must not depend on GitHub browsing to discover
those requirements.

CCFG-21 is complete. CCFG-25 must consume its resolved candidate planning
artifact contracts and selection transaction rather than treating the planning
transaction as unresolved. GitHub #54 is implemented on stable master; its
semantic slice rules remain target acceptance for CCFG-25. GitHub #51 and #52
remain open until CCFG-25 implements and validates their requirements.

The accepted command-owner redesign snapshot remains immutable. This is a live
implementation-intake amendment for CCFG-25 only.

## Required Planning Topology

The default agent remains the human-facing `plan-batch` command owner and the
only queue mutator.

```text
user
  -> default agent / plan-batch command owner
       -> batch_planner: produce a non-executable draft
       -> batch_plan_reviewer: independently challenge the draft
       -> batch_planner: revise named findings when required
       -> default agent: queue only after the gate is satisfied
```

The default agent must invoke both registered specialists directly. The planner
must not invoke, select evidence for, or approve the reviewer. The reviewer must
receive the selected dispatch, authoritative source packet, explicit user
constraints and approvals, current planning-state facts, the exact draft, and
the proportionality record from the default agent.

`batch_planner` owns draft production and correction only. It cannot queue,
mutate program finding lifecycle, approve its own complexity, implement code, or
perform review.

`batch_plan_reviewer` is read-only. It cannot edit the draft, select work, mutate
planning state, queue, implement, perform slice review, or spawn agents. It
reviews the planning decision rather than an implementation diff.

Every new or materially amended runway receives independent planning review.
Routine plans use a compact review; complexity changes review depth, not whether
the gate exists.

## Proportionality Gate

Before queue mutation, the planner must produce:

```yaml
proportionality:
  observed_failure: string
  invariants: []
  minimum_viable_change: string
  proposed_change: string
  additions_beyond_minimum: []
  simpler_alternatives_rejected: []
  verdict: proportionate | requires-user-approval | blocked
```

Every material addition beyond the minimum must name the added state, concept,
owner, artifact, schema, validation surface, test topology, or workflow
obligation; the concrete in-scope failure mode it prevents; and why the minimum
viable change cannot prevent that failure more simply.

Source findings, notes, issues, and accepted designs define authoritative
problems, invariants, user decisions, and authorized risk. Proposed mechanics are
evidence, not automatically mandatory topology. The planner must narrow or
replace over-specified source mechanics when a smaller design preserves all
authoritative invariants, unless the larger topology is itself an explicit
user-approved contract.

Routine work must satisfy this compactly. Do not create a standalone permanent
design artifact, complexity-scoring framework, or new lifecycle state merely to
hold the proportionality result.

A `requires-user-approval` or `blocked` verdict preserves the selected dispatch
and draft evidence but stops before queue mutation. User approval applies only to
the named residual complexity.

## Slice Shape

Slice count is an output of scope analysis, never an input range.

Start with one slice. Split only when a boundary is independently meaningful:

- different owner seams;
- a valid producer/consumer intermediate state;
- different risk classes or approval gates;
- different validation profiles, repositories, generations, or environments;
- a materially safer independent commit, rollback, or review boundary;
- isolation of destructive cleanup or contract narrowing;
- one combined diff would not have one coherent acceptance contract.

Merge proposed slices that share owner, risk, validation, and acceptance
boundaries and have no useful independently shippable intermediate state.

One-slice runways are valid. More than five slices are not rejected solely by
count, but every multi-slice boundary requires a compact concrete rationale. No
slice may exist solely to hold generic docs, metadata, tests, or closeout work
that naturally belongs with the behavior it validates.

## Planning Review Decision

The registered planning reviewer must return structured decisions equivalent to:

```yaml
status: clean | findings | blocked
review_basis: string
minimum_viable_alternative: string
unjustified_additions: []
slice_shape_findings: []
scope_leaks: []
user_decisions: []
required_fixes: []
```

Queue mutation is allowed only when:

- selected dispatch and source evidence remain current;
- proportionality is `proportionate`, or named residual complexity has explicit
  user approval;
- the planning reviewer returns `clean` against the exact current draft;
- no unresolved user decision remains;
- the default agent applies the queue mutation through the resolved candidate
  planning transaction.

Named findings return to `batch_planner` through the default agent. A repeated
unresolved material finding, newly expanding architecture after correction, or
need for an unrecorded user choice stops rather than looping indefinitely.

## CCFG-25 Integration Boundary

Implement these requirements in the candidate planning-owner architecture while
CCFG-25 transfers selection, scope, dispatch, runway, risk, approval, and
validation-profile ownership to `plan-batch`.

Do not add permanent planner/reviewer or proportionality infrastructure to
legacy Architecture Program Runway or Batch Runway create-spec merely to land
this amendment before CCFG-25. CCFG-25 must remove those legacy planning owners
in the same ownership transfer.

Use the planning transaction and artifact contracts resolved by CCFG-21 and
required by CCFG-25. Do not create a parallel planning store, second queue owner,
parallel command, or duplicate executable draft format.

CCFG-23 owns topology-independent behavioral proof for the planning-quality
requirements in this amendment. The canonical carry-forward amendment at
`command-owner-redesign-planning-execution-carry-forward.md` adds the related
execution-currentness and cutover obligations without changing CCFG-25's
planning ownership.

## Added CCFG-25 Acceptance

```yaml
planning_quality:
  default_agent_is_only_queue_mutator: true
  registered_batch_planner: true
  registered_batch_plan_reviewer: true
  planner_cannot_invoke_reviewer: true
  reviewer_receives_independent_source_evidence: true
  every_new_or_amended_runway_reviewed: true
  proportionality_required_before_queue: true
  source_mechanics_can_be_narrowed: true
  minimum_viable_change_recorded: true
  residual_complexity_requires_user_approval: true
  fixed_slice_count_required: false
  filler_slices_rejected: true
  stale_draft_rejected: true
  blocked_review_preserves_non_executable_draft: true
  legacy_planning_owner_dependencies: 0
```

Behavioral tests must cover:

- a cohesive one-slice plan;
- a justified producer/consumer split;
- rejection or merging of filler decomposition;
- an over-specified source proposal narrowed to the minimum viable design;
- unjustified expansion blocked before queue mutation;
- explicit approval limited to named residual complexity;
- direct default-agent invocation of planner and reviewer;
- independent reviewer evidence supply and no-self-review;
- correction routing, repeated-finding stop, stale-draft rejection, and atomic
  queue gating;
- topology-independent behavior rather than exact prompt prose or legacy paths.

## References

- GitHub issue #51: compact proportionality evidence
- GitHub issue #52: delegated planning and independent planning review
- GitHub issue #54: semantic slice boundaries instead of a fixed 3–5 range
- COR-008 / CCFG-25 in the accepted command-owner redesign snapshot
- `command-owner-redesign-planning-execution-carry-forward.md`: canonical
  behavioral, execution-currentness, and cutover carry-forward

## No Selection Performed

This amendment changes future CCFG-25 scope and acceptance only. It does not
select, dispatch, queue, activate, implement, or close CCFG-25 or any successor.
