# Planning And Independent Review Hardening

## Status And Intended Ledger Identity

- Status: amended after explicit supersession; no implementation has started.
- Lifecycle history: the candidate-targeted CCFG-35 dispatch/runway/review was
  superseded before implementation on 2026-07-20, and CCFG-35 was restored to
  `Open` before replacement planning began. Canonical `LEDGER.md` owns the
  current lifecycle state after a replacement plan is accepted.
- Intended ledger identity: `CCFG-35`, allocated as the next valid unused
  canonical identity after this document was created and before its ledger row
  was added.
- Planning state at amendment: unselected, undispatched, unqueued, and inactive;
  a later replacement `plan-batch` may return the row to `Pending` only after a
  master-based dispatch/runway receives a fresh independent clean review.
- Intended title: **Harden Planning And Independent Review**.
- Area: reusable planning and independent review.

This document is the complete durable source for the future ledger task. It
defines a generic reusable planning-system improvement, not a project-specific
exception, temporary overlay, or amendment to another task.

## Master-Only Implementation Authority Amendment

This section is project coordination authority for CCFG-35, not a reusable
branch-specific planning rule.

- The only implementation repository is
  `/home/alacasse/projects/codex-config` on branch `master`.
- Replacement planning must inspect and change the planner actually used from
  master: the installed `plan-batch` skill and its existing master support route
  through Architecture Program Runway and Batch Runway create-spec.
- `/home/alacasse/projects/codex-config-command-owner-redesign` and
  `/home/alacasse/.codex-command-owner-redesign` are evidence-only for CCFG-35.
  They are forbidden implementation, validation-install, and closeout targets.
- Candidate-only `batch_planner` / `batch_plan_reviewer` roles,
  `scripts/plan_batch.py`, `scripts/planning_contract.py`, planning schema
  families, transaction machinery, and candidate scenario adapters are not
  CCFG-35 implementation surfaces.
- The replacement plan is ordinary single-root work. It must not carry a
  strict cross-checkout planning snapshot or require candidate live leases.

An accepted CCFG-35 closeout must prove that the accepted implementation
changed the planner used on master. The final independent reviewer must verify,
from the exact accepted commit range and fresh local evidence, all of the
following:

1. implementation commits are on `master` in the canonical repository;
2. the accepted diff changes the public master `plan-batch` route or the exact
   master create-spec / independent-review handoff it consumes, rather than
   only adding disconnected tests, schemas, scripts, prompts, or documents;
3. `/home/alacasse/.codex/skills/plan-batch` remains owned by this repository
   and resolves to the accepted master `skills/plan-batch` source;
4. installed planner content matches the accepted master source, with installer
   status or dry-run evidence reconciled when manifest versions change; and
5. the behavioral counterfactual would fail if the accepted master planning or
   review gate were removed or bypassed.

Planner self-attestation, candidate-home evidence, manifest presence alone, or
a closeout statement without independently reconstructed path and revision
evidence cannot satisfy this authority amendment.

## Bounded Acceptance-Evaluation Authority Amendment

This section is CCFG-35 coordination authority, not a reusable requirement for
ordinary `plan-batch` use. The user's 2026-07-20 correction explicitly rejects
the prior mandatory per-scenario live-evaluation lane and authorizes only the
following bounded, one-time acceptance evidence:

- after Slice 1, one planner invocation may process one batched smoke input and
  one different reviewer invocation may review all smoke results;
- after Slice 2, one planner invocation may process the ten isolated evidence
  packets and one different reviewer invocation may review all ten results;
- every packet keeps its own root, hashes, evidence identifiers, disposition,
  and queue decision even though the semantic invocations are batched; and
- the normal call budget is therefore four live semantic invocations for the
  whole batch: two smoke calls and two final calls, excluding implementation
  workers and implementation/test-quality reviewers.

This authority does not permit one planner/reviewer pair per scenario, a
permanent evaluation service, routine live-model evaluation in `plan-batch`, or
silent expansion after a semantic correction. At most one transport-only retry
per batched invocation is allowed; it must be recorded and cannot disguise a
semantic `correct`, `revise`, or `block` result as infrastructure failure.

The smoke must record wall time, retry count, input and output byte counts, and
the model, effort, and token counts when the host exposes them. Unexposed values
must be recorded as `unavailable`, never guessed. It must compare the batched
shape with the rejected twenty-call per-scenario alternative and extrapolate
the final two-call lane. Slice 2 is not authorized until a separate read-only
cost-gate reviewer accepts that exact smoke receipt and the user explicitly
approves the measured estimate.

Green mechanical or behavioral validation receipts may be reused across later
same-commit reviewers when the exact commit, command, input hashes, environment
identity, result, duration, and output digest match. A material code, test,
command, dependency, configuration, input, or environment change invalidates
the receipt and requires rerun; reviewer preference alone does not.

## Observed Problem

The reusable planning pipeline can accept a plan that is structurally valid but
semantically incomplete. Exact artifact paths, hashes, pointers, and queue state
can all be correct while the plan has not proved who owns the relevant decision,
which callers still reach an old owner, who owns reachable failure paths, whether
an intermediate state has a real consumer, or whether a decisive implementation
primitive is feasible.

The corresponding aggregate independent review can return `clean` by confirming
planner-authored claims instead of reconstructing the decisive facts from pinned
repository evidence. A list of semantic `pass` statements without a recorded
evidence basis can therefore authorize queue mutation even though the review did
not independently establish the facts the queue is being asked to trust.

On the current reusable surfaces, `plan-batch` owns the human-facing planning
decision, Architecture Program Runway owns selection and dispatch state, and
Batch Runway create-spec owns semantic slice construction. Planning State
correctly validates structural state and queue mechanics. The reusable stable
pipeline does not currently own an evidence-backed independent planning-review
method and result boundary between draft creation and queue authorization.

This is a planning and review assurance defect. It is not evidence that Planning
State should decide semantic quality, and it is not solved by adding another
persistent state model.

## Current Planning And Review Pipeline

The current reusable flow is materially:

```text
explicit plan-batch request
  -> Planning State current and validate
  -> canonical ledger selection and dispatch
  -> Batch Runway create-spec semantic planning
  -> structural and focused validation
  -> independently delegated planning review where the workflow supplies one
  -> queue mutation based on an aggregate `clean` review and valid canonical state
```

The relevant trust boundaries are:

1. `skills/plan-batch/SKILL.md` owns the caller-visible selection, one-spec, and
   stop-before-implementation contract but does not define the reusable evidence
   duties of independent planning review.
2. `skills/batch-runway/references/create-spec.md` owns semantic slice shape,
   batch kind, risk, validation status, and execution handoffs. Its current
   qualitative requirements can be satisfied without an exact consumer,
   complete replacement analysis, failure-path owner, counterfactual, decisive
   feasibility proof, or bounded cost evidence.
3. The current stable planning-review practice can bind a verdict to exact
   dispatch and runway drafts, but the reusable system does not require each
   reviewer `approve` disposition to cite an independently reconstructed evidence
   basis.
4. `scripts/planning_state.py` correctly validates mechanically decidable
   planning-root, pointer, path, registration, lineage, selected-state, and
   queue-transition facts. It does not and should not infer whether a caller set
   is complete or a slice is useful.
5. The existing `runway_reviewer` is an implementation-diff reviewer, not the
   planning-review boundary. This task strengthens the actual planning-review
   handoff and result seam without adding a new agent role.

The future planner must inspect these seams directly rather than assuming this
snapshot still describes their exact line-level implementation.

## Required Outcome

Strengthen the reusable planning and independent-review system so a
semantically incomplete but structurally valid plan cannot receive a clean
review and enter the queue.

The strengthened duties must be triggered by applicable planning semantics,
including ownership transfer, migration, replacement of an existing authority,
or dependence on an unproved decisive primitive. They must not depend on a
specific ledger identity, program, repository, branch, checkout topology, or
temporary policy.

The resulting system must:

- require evidence-backed independent reconstruction of decisive semantic
  facts before a clean planning review can authorize queue mutation;
- require semantic replacement analysis before selecting slices for
  substitutive work;
- make reachable failure-path ownership part of independent usability;
- require a behavioral counterfactual for each semantic ownership transfer;
- conditionally require a bounded feasibility proof when a decisive mechanism
  is not already demonstrated;
- define intermediate usefulness through an exact current consumer and complete
  end-to-end behavior, not independent committability alone;
- record available proportionality and execution-cost evidence for work with
  significant multipliers; and
- keep semantic planner/reviewer judgments separate from deterministic
  mechanical enforcement.

## Included Scope

- Reusable planner responsibilities for semantic replacement, failure paths,
  ownership counterfactuals, conditional feasibility, intermediate-state
  usefulness, and proportionality.
- The actual independent planning-review handoff, instructions, evidence basis,
  result contract, and exact-draft binding used before queue mutation.
- Focused behavior-level planner and reviewer regression scenarios using small
  pinned evidence packets and coarse dispositions.
- Minimal deterministic checks for mechanically representable review binding,
  required evidence references, caller identifiers and alignment, and
  counterfactual references.
- Preservation of Planning State's canonical structural responsibilities.
- Workflow and routing documentation needed to make the strengthened assurance
  boundary and ownership explicit.
- Directly associated contract, glossary, manifest, or changelog documentation
  only when the current implementation seam requires it.

## Explicit Non-Goals

- Project-specific planning rules.
- Ledger-identity-specific behavior.
- Branch-specific or checkout-specific behavior.
- Temporary activation policies.
- A new top-level planning schema family.
- New persistent planning or execution state.
- A new agent role.
- Universal numeric file, line, slice, token, or runtime thresholds.
- Mandatory execution telemetry.
- Mandatory fresh coordinator processes.
- Per-scenario live planner or reviewer invocation, or any live-model
  evaluation beyond the bounded acceptance authority above.
- Persisting every useful review question.
- Turning semantic review judgments into deterministic validator claims.
- Changing unrelated execution, finalization, reconciliation, or closeout
  behavior.
- Planning or implementing another ledger task as part of this work.

## Planner Responsibilities

Before slice selection, the planner must reconstruct the decisive semantic facts
from pinned repository evidence rather than treating source prose or a proposed
runway as proof. The applicable record must include:

- the observed problem and minimum viable change;
- the decision whose ownership or behavior changes;
- the current and future semantic owners;
- the exact current and future entrypoints;
- every normal caller relevant to the transferred or replaced decision;
- retained routes, why each remains, its removal owner, and its terminal
  condition;
- every forbidden fallback;
- ownership of reachable normal and failure outcomes;
- the exact current production consumer for each intermediate result;
- at least one ownership-transfer counterfactual;
- each decisive feasibility assumption;
- the widest slice's best smaller usable alternative; and
- significant execution and validation cost multipliers.

For substitutive work, every material existing decision surface and caller must
be classified as exactly one of:

- replaced;
- conditioned on the new authority;
- intentionally retained, with reason and terminal condition;
- removed; or
- deferred, with a concrete owner and reason.

Unclassified material surfaces or callers must block planning or require
correction. Physical source-file presence is not equivalent to semantic
authority: an old implementation may remain during migration only when normal
callers are proven unable to reach its forbidden decision behavior.

A migrated success path is not independently usable when validation failure,
review failure, stale evidence, interruption, retry, commit or receipt failure,
or recovery can silently return to the displaced owner. Every reachable failure
path must have one defined owner, one observable blocked or recovery result, an
exact current consumer, and no undocumented legacy fallback.

Every semantic ownership transfer must require at least one required-green
scenario that would fail if a forbidden old owner were invoked. String,
prompt-wording, manifest, and schema presence are insufficient by themselves.
Fixtures that manufacture the expected ownership conclusion are also
insufficient by themselves.

When a plan depends on a decisive behavior that is not already demonstrated,
the planner must either cite applicable production evidence or require a bounded
disposable feasibility proof before implementation slices are approved. This is
conditional, not a mandatory prototype phase for ordinary work. Applicable
mechanisms include a new public or deterministic interface, coordinated updates
across multiple durable artifacts, partial-apply or replay behavior, locking or
concurrency guarantees, cross-platform filesystem behavior, or another premise
whose absence would invalidate the planned architecture. Assertion-only
feasibility cannot authorize execution.

Every intermediate slice result must identify:

- the exact current production consumer;
- the end-to-end behavior available to that consumer;
- ownership of all reachable failure paths;
- retained decision authority;
- terminal conditions for temporary coexistence; and
- the rollback boundary.

Being independently committable is not sufficient. A common rollback boundary
alone is not evidence that a larger slice cannot be split into two useful states.

For migration, ownership-transfer, or other high-multiplier work, the planner's
proportionality record must include available evidence or explicit unknowns for
likely production surfaces, rough scope or change range, focused validation
runtime, repeated validation between slices, installation or isolated-
environment cadence, worker and reviewer invocations, specialist reviews, and
duplicated final gates. The system must not impose universal numeric limits.

## Independent Reviewer Responsibilities

The independent reviewer must reconstruct the decisive facts from pinned
repository evidence rather than merely confirm the planner's framing. The
reviewer must record concise supporting evidence for each applicable fact:

- observed problem and minimum viable change;
- current and future semantic owners;
- exact active entrypoints and normal callers;
- retained routes, reasons, removal owners, and terminal conditions;
- forbidden fallbacks;
- ownership of every reachable failure path;
- the real consumer of every intermediate state;
- ownership-transfer counterfactuals;
- decisive feasibility assumptions and the evidence or bounded proof supporting
  them;
- the widest slice's best smaller usable alternative; and
- significant execution and validation cost multipliers.

For a reviewer `approve` result, each applicable semantic conclusion must state the
reconstructed fact and cite concise evidence identifiers, paths, or pinned
source references. Bare semantic `pass` statements must not authorize queue
mutation.

The reviewer must remain bound to the exact dispatch and runway drafts it
approves. A changed draft invalidates the prior `approve` result. If the bounded
evidence packet is insufficient, the reviewer must either perform permitted
bounded read-only inspection at the pinned basis or return a blocker. It must
not fill evidence gaps by repeating planner self-attestation.

The reviewer should falsify the plan at likely duplicate-authority and
unsupported-assumption seams. It must not re-author the plan, prescribe a
universal slice count, force migration-specific ceremony onto ordinary small
work, mutate planning state, or queue the batch. The existing independent
planning-review role boundary should be strengthened; no new agent role is
required.

## Deterministic Validation Responsibilities

Deterministic validation should enforce only mechanically decidable facts. As
supported by the current artifact representation, appropriate checks include:

- exact review binding to the dispatch and runway drafts;
- required evidence references for a reviewer `approve` disposition;
- refusal of `approve` with absent or empty required evidence references;
- non-empty and unique caller identifiers when persisted;
- alignment between persisted migrated callers, retained routes, and acceptance
  references;
- presence of a counterfactual reference for applicable ownership-transfer
  work; and
- preservation of existing path, pointer, registration, lineage, selected-
  state, queue, and currentness validation.

Deterministic validation must not claim to decide:

- whether the complete caller set was discovered;
- whether an intermediate state is genuinely useful;
- whether a smaller slice is preferable;
- whether a feasibility proof is persuasive; or
- whether estimated cost is acceptable.

Those remain planner and independent-review judgments, exercised through
behavior-level scenarios. Where the current Markdown representation cannot
support a mechanical check without a new schema or state family, use the
planner/reviewer instruction boundary and focused behavior regression instead
of inventing deterministic semantic authority.

Planning State must remain the structurally focused owner of canonical planning
paths, pointers, registration, lineage, queue state, and currentness.

## Regression Scenarios

Add behavior-level coverage for at least these cases:

| Scenario | Expected planner disposition | Expected reviewer disposition |
|---|---|---|
| A replacement owner is added while an old semantic fallback remains reachable. | Correct or block until the fallback is classified and excluded. | Reconstruct reachability and reject unsupported approval. |
| Migration evidence names capabilities but omits exact callers. | Correct the caller inventory or block. | Compare pinned callers with the plan and require revision. |
| A success path is transferred while failure paths remain owned by the displaced system. | Block the slice as not independently usable. | Reject after reconstructing failure ownership. |
| A large slice is justified only by a shared rollback boundary. | Produce the best smaller usable alternative or evidence that none exists. | Revise when common rollback is the only rationale. |
| No counterfactual can detect invocation of the old authority. | Add a required-green behavioral counterfactual or block. | Reject wording, topology, or presence evidence alone. |
| A decisive primitive is asserted without evidence. | Require applicable production evidence or a bounded disposable proof. | Reject assertion-only feasibility. |
| An intermediate producer state has no current consumer. | Merge, reorder, or name a real current consumer. | Reject the independent-usability claim. |
| Two independently atomic durable writes are described as one atomic operation without ordering and recovery proof. | Require ordering, partial-state behavior, recovery owner, and fault proof. | Reject the compound atomicity claim. |
| An independent reviewer accepts planner self-attestation without reconstructing evidence. | The plan remains unauthorized for queue mutation. | Return `revise` or `block`; an evidence-free `approve` result is invalid. |
| A valid small non-migration plan is submitted. | Plan it without migration-specific ceremony. | Approve when its ordinary scope, validation, rollback, and proportionality are supported. |

Tests should assert coarse dispositions such as `plan`, `correct`, `block`,
`approve`, or `revise`. They should use small pinned evidence packets and avoid
brittle assertions against exact generated prose.

The negative cases should fail for semantic planner or reviewer reasons, not
merely because a schema parser rejects the fixture. Mechanical validation may
separately reject missing or malformed evidence fields where representation
supports that check.

## Acceptance Criteria

- The negative regression scenarios expose the current weaknesses before
  correction, or are otherwise shown to represent the previous behavior
  accurately.
- The strengthened planner corrects or blocks each applicable bad plan for the
  intended reason.
- The strengthened independent reviewer rejects unsupported semantic approval
  and records an evidence-backed reconstruction for an `approve` result.
- Mechanical validation rejects missing or malformed required evidence
  references where the current artifact representation supports them.
- Exact review binding to the approved dispatch and runway drafts is preserved.
- The valid small-plan control remains accepted without migration-specific
  ceremony.
- The rules are triggered by applicable planning semantics rather than a
  specific task or project identity.
- Generic reusable instructions contain no hard-coded project paths, ledger
  IDs, branch names, checkout topology, temporary policies, or optional
  exploration-tool requirements.
- Planning State path, pointer, registration, lineage, currentness, and queue
  validation remains structurally focused.
- Deterministic validation does not claim semantic completeness, usefulness,
  feasibility quality, slice preference, or cost acceptability.
- No implementation work outside the planning and review system is introduced.
- No new top-level schema family, persistent planning/execution state, or agent
  role is introduced.
- The ten behavioral cases are evaluated as ten isolated packets through one
  batched planner and one different batched reviewer, with ten independently
  applied queue decisions.
- Slice 2 cannot start before the two-packet Slice 1 smoke records actual cost,
  an independent cost-gate review accepts the estimate, and the user approves
  it.
- Planner, reviewer, and queue vocabularies have one explicit fail-closed
  mapping; no synonymous positive term may authorize queue mutation.

## Expected Changed Surfaces

Future planning must inspect the current seams before prescribing edits. The
implementation is expected to inspect and may need to change:

- `skills/plan-batch/SKILL.md`;
- `skills/batch-runway/references/create-spec.md`;
- the actual independent planning-review handoff, instruction, and result
  boundary used before queue mutation;
- focused behavior-level planning and independent-review scenarios;
- existing related contract tests, including the semantic slice-shape,
  create-spec, and routing-ownership surfaces where applicable;
- the minimal deterministic planning validation used before queue mutation;
- `docs/workflow-guide.md`;
- `docs/skill-routing-contract.md`; and
- directly associated contract, glossary, manifest, or changelog documentation
  only where the inspected implementation requires alignment.

This list is an inspection boundary, not a prescribed edit list. In particular,
the implementation must not repurpose the implementation-time
`runway_reviewer` as the planning reviewer merely because that agent already
exists.

## Cost And Proportionality Expectations

The strengthened workflow should add review depth only when the work's semantics
trigger it. Ordinary small non-migration plans must remain compact.

For migration, ownership transfer, replacement, or other high-multiplier work,
the planner and reviewer must use available repository evidence or explicitly
record unknowns for:

- likely changed production surfaces and rough scope or change range;
- focused validation runtime;
- repeated validation between slices;
- installation, fresh-home, or isolated-environment cadence;
- worker and reviewer invocations;
- triggered specialist review passes; and
- duplicated final gates.

The record should support a judgment about whether the proposed shape is
proportionate and whether the widest slice has a smaller usable alternative. It
must not introduce universal hard limits for files, lines, slices, tokens, or
runtime. Missing telemetry does not itself block planning when bounded existing
evidence or explicit unknowns are sufficient.

CCFG-35 must also apply the repository's CCFG-23 execution-retrospective
evidence: the prior 123-test scenario suite took 814.32 seconds and implied
about 41,125 subprocess executions, while unchanged reruns multiplied that cost
directly. Its exact-commit receipt-reuse recommendation is therefore a required
batch-local constraint for CCFG-35 rather than optional background reading.

Implementation and test design should remain focused. Prefer small pinned
evidence packets and coarse outcomes over broad generated-prose snapshots or a
new permanent evaluation infrastructure.

## Dependencies And Sequencing

- This work depends on the current reusable `plan-batch`, create-spec,
  independent planning-review, and pre-queue validation seams being inspected
  as they exist when planning begins.
- It preserves the accepted human-facing command-owner boundary: `plan-batch`
  remains the planning command, while narrowly scoped support owns internal
  mechanics.
- It preserves the distinction between Ledger Intake, Batch Planning, Batch
  Spec Creation, and implementation execution.
- It does not depend on a particular project task, branch topology, migration
  program, or temporary policy.
- A later explicit `plan-batch` invocation must plan only this ledger task and
  derive implementation slices from independently usable behavior and
  regression boundaries.
- No dispatch, runway, queue entry, active batch, or implementation work is
  created by this intake.

## Stop Conditions

Stop planning or implementation if:

- the proposed reusable rule depends on a specific ledger identity, program,
  repository path, branch, checkout topology, temporary policy, or optional
  exploration product;
- the actual independent planning-review handoff and result boundary cannot be
  identified from current code and instructions;
- an aggregate `clean` review can still be represented by unsupported semantic `pass`
  statements;
- an ownership-transfer plan can still omit callers, retained-route terminal
  conditions, forbidden fallbacks, reachable failure owners, or a behavioral
  counterfactual without correction or a blocker;
- a decisive unproved primitive can still authorize implementation through
  assertion alone;
- deterministic validation is made responsible for semantic completeness,
  usefulness, feasibility quality, slice preference, or cost acceptability;
- Planning State's structural path, pointer, registration, lineage,
  currentness, or queue responsibilities are weakened or replaced;
- the implementation requires a new top-level schema family, persistent
  planning/execution state, agent role, universal numeric threshold, mandatory
  telemetry, or mandatory fresh coordinator process;
- migration-specific ceremony becomes mandatory for a valid small ordinary
  plan;
- behavior tests are replaced only by string, prompt, manifest, schema, or
  fixture-self-attestation checks;
- scope expands into unrelated execution, finalization, reconciliation, or
  closeout behavior; or
- planning selects, prepares, or implements any unrelated ledger work.

## Planning Handoff

A later explicit `plan-batch` invocation must:

1. plan only this generic planning and independent-review hardening task;
2. inspect the current reusable planning, review, and deterministic pre-queue
   pipeline directly;
3. derive slices from independently usable behavior and the regression
   boundaries in this document;
4. keep semantic planner/reviewer reasoning separate from mechanical
   validation;
5. preserve existing canonical Planning State responsibilities;
6. keep all reusable rules independent of project identity, local topology, and
   temporary policy;
7. create and independently review at most one bounded dispatch/runway for this
   task; and
8. stop before implementation without selecting or preparing unrelated work.

## Source Evidence

Primary historical analyses:

- `docs/plans/programs/codex-config/notes/ccfg-26-planning-instruction-root-cause-analysis.md`
- `docs/plans/programs/codex-config/notes/ccfg-26-plan-gap-interrogation.md`

Current reusable surfaces inspected at intake revision
`540e2c933eb4697fdb108f428f93bad5c4214e99`:

- `skills/plan-batch/SKILL.md`
- `skills/architecture-program-runway/SKILL.md`
- `skills/batch-runway/references/create-spec.md`
- `scripts/planning_state.py`
- `docs/workflow-guide.md`
- `docs/skill-routing-contract.md`
- `CONTEXT.md`
- `docs/adr/0001-planning-root-and-plan-archive.md`
- `docs/adr/0002-human-facing-command-owner-skills.md`
- `tests/test_semantic_slice_shape_contract.py`
- `tests/test_batch_runway_create_spec_contract.py`
- `tests/test_skill_routing_rule_ownership.py`
- `tests/test_planning_state.py`
- `tests/test_ccfg_26_development_boundary.py`

Historical planning-review artifacts were inspected only to establish the
generic failure pattern: exact draft binding and aggregate `clean` review can coexist with
unsupported semantic conclusions. Their ledger identities, project topology,
batch decomposition, and sequencing are not requirements for this task.

The historical analyses and current source inspection are evidence for the
reusable defect. Future planning must refresh the current seams and must not
treat the intake revision or historical reports as a live implementation
snapshot.
