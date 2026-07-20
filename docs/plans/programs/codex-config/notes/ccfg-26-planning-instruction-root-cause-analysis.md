# CCFG-26 Planning Instruction Root-Cause Analysis

## Executive Finding

CCFG-26 was correctly controlled and queued by the stable controller, although
the plan it produced had the documented quality gaps. Under ADR 0004, stable is
the only generation permitted to plan or control the candidate branch through
CCFG-29. Candidate planning code was not eligible to intervene, and its non-use
is not a failure.

The exact planning and queue facts are:

- Stable controller and canonical planning checkout:
  `/home/alacasse/projects/codex-config`, branch `master`.
- Stable planning basis:
  `6b575614983e72456a25875264ebab7e39ea0a72`.
- Candidate implementation checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`.
- Candidate inspection basis:
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`.
- Queue commit:
  `27c2ada4ce095ac42b102592d4d16237527c931d`.
- Exact queued dispatch and runway hashes:
  `02805a6bff0e3ad135d52d27b7c192584309ce3bfbf1736313b22b79e3c1d5cc`
  and
  `7e2512a8897a7207481908ec6788c529e97fc57338d41d34a5415dd1fea790d4`.

The primary root cause is an incomplete semantic-planning and independent-review
contract inside the stable reusable planning system:

1. The stable `plan-batch` command that controlled CCFG-26 was the authoritative
   bridge in `skills/plan-batch/SKILL.md`. It delegated selection to Architecture
   Program Runway and Markdown spec creation to Batch Runway.
2. The principal agent authored the dispatch and runway after an advisory
   `codebase_investigator` pass. A newly spawned agent named
   `batch_plan_reviewer` then performed the independent review. Stable
   instructions supplied no reusable evidence-reconstruction method or result
   contract for that review.
3. The resulting `review.md` correctly bound the dispatch and runway hashes but
   recorded bare semantic `pass` conclusions without an independently derived
   problem statement, caller set, failure-state analysis, feasibility basis,
   counterfactual, cost basis, or smaller-slice alternative.
4. Stable Planning State validation then proved path, pointer, and state
   consistency. It did not and could not prove the plan's semantic claims.

The stable pipeline was therefore the right pipeline with an insufficient
contract. Its reusable create-spec instructions and temporary project policy
required useful vertical slices, caller mapping, no silent fallback, and
smaller-alternative analysis, but did not make exact semantic replacement,
failure-path closure, decisive-primitive proof, counterfactual validation, cost
measurement, or independent evidence reconstruction enforceable.

The candidate planning implementation was inspected only because the
investigation requires comparison where generations differ and because the same
semantic weaknesses must not survive the eventual post-CCFG-29 merge. It is not
an alternative current controller and is not a proposed dependency. Its future
contracts also need hardening before they become authoritative, but that fact is
separate from the cause of the stable CCFG-26 planning failure.

The earliest reusable prevention boundary is therefore two-part:

- the stable ownership-transfer planner must perform an exact semantic
  replacement audit before choosing slices, with an independent reviewer
  reconstructing the same audit from pinned repository evidence rather than
  accepting runway claims; and
- stable review instructions must require a recorded evidence basis for every
  semantic approval before queue mutation trusts a clean verdict.

No omission should be dismissed as merely “the model missed it.” Only the
current Slice 4 smaller-alternative duty meets the narrow standard for
`model_execution_failure_despite_sufficient_contract`: the loaded temporary
policy explicitly says, at
`stable-runway-dogfooding-policy.md:47-50`, that slice count follows independent
usefulness and rollback boundaries and that a clearly oversized slice requires
a smaller-alternative analysis. The plan and review did perform an analysis but
accepted an invalid rationale. That exact failure needs enforcement and a
regression scenario, not more wording alone. Every other material omission had
an absent, abstract, self-attested, or evidence-starved stable contract.

## Planning Pipeline

### Reconstructed actual pipeline

```text
user request: $plan-batch CCFG-26
  -> stable skills/plan-batch/SKILL.md
  -> Planning State current/validate + ledger/dispatch source resolution
  -> principal agent + advisory codebase_investigator
  -> principal-authored dispatch.md and runway.md
  -> structural Planning State / policy / repository validation
  -> independent spawned batch_plan_reviewer
  -> free-form clean verdict converted to review.md
  -> principal-agent CURRENT.md / LEDGER.md / queue mutation
  -> commit 27c2ada and canonical queued state
```

The candidate pipeline is not a missing stage in this reconstruction. It could
not be used and no prevention recommendation in this report requires stable to
import, invoke, or share state with it. Candidate planning implementation is
considered later only as a non-controlling post-merge regression check.

### Stage contracts and trust flow

| Stage | Actual owner | Inputs and required evidence | Decision and output | Blocking versus advisory | Who trusted it |
| --- | --- | --- | --- | --- | --- |
| User request | User and stable `plan-batch` command | Explicit CCFG-26 selection request | Select at most one existing ledger item and stop before implementation | Missing or unsuitable ledger work blocks | Stable command owner |
| Command owner instructions | Stable `skills/plan-batch/SKILL.md:34-63,108-121`; routing in `docs/skill-routing-contract.md:53-84` | Current Planning State and canonical ledger | Route selection to Architecture Program Runway and spec creation to Batch Runway | Existing queued/active work, missing ledger row, or invalid state blocks; planning-quality method is delegated | Principal agent and support skills |
| Source resolution | Root `AGENTS.md`, Planning State, dispatch author, strict cross-checkout helpers | Canonical CURRENT/LEDGER, COR-009, ADR 0004, carry-forward, slice policy, temporary dogfood policy, candidate source | Pin stable/candidate roots and revisions and identify target seam | Identity mismatch blocks; historical failure selection was discretionary | Planner/principal agent |
| Planner handoff | Stable command owner; principal agent used an advisory `codebase_investigator` | Candidate source and the sources selected by the principal agent | Investigator proposed a four-slice shape; principal agent correctly retained planning authority | Investigator advice was non-binding and could not approve or block | Principal agent |
| Planner output | Principal agent using stable `batch-runway/references/create-spec.md` and temporary dogfood prose | Selected sources plus candidate inspection | Free-form `dispatch.md` and `runway.md` | Required fields and obvious policy conflicts could block; truth of caller, feasibility, counterfactual, and cost claims was model judgment | Validators and reviewer |
| Deterministic validation | Stable `scripts/planning_state.py`, cross-checkout helpers, focused policy/tests | Artifact paths, pointer state, hashes, checkout identities, textual policy/test fixtures | Valid state/path result and green test commands | Malformed paths/state and failed commands block; semantic completeness is outside the gate | Principal agent and reviewer |
| Independent reviewer handoff | Stable principal agent delegated to an independent read-only reviewer | Drafts and a broad set of repository reads chosen during the review | Free-form `clean` verdict with checks, corrections, blockers, and residual risk | Reviewer corrections could block in practice; no stable reusable contract required an independent semantic reconstruction or evidence basis | Principal agent |
| Reviewer output | `batches/ccfg-26-work-batch-owner-transfer/review.md` | Dispatch/runway hashes and reviewer conclusions | Approval bound to two exact draft hashes | Draft hash mismatch would block; bare semantic `pass` claims were trusted | Queueing principal agent |
| Queue transaction | Principal agent plus stable Planning State artifact registration/validation | Dispatch, runway, review, CURRENT, LEDGER | Write queue pointers and ledger status, then commit | State/path invalidity blocks; semantic review quality was trusted rather than deterministically enforceable | Canonical Planning State consumers |
| Canonical state | `CURRENT.md` and `LEDGER.md` at `27c2ada` | Queued artifacts and state mutation | CCFG-26 becomes the one queued batch | Canonical state now treats the review as sufficient authorization | Later `work-batch` pickup |

### Trust discontinuities

The pipeline contained four unearned trust transitions:

1. The principal agent treated an advisory source investigation as sufficient
   planner analysis.
2. structural validation trusted planner-authored semantic fields as facts;
3. the reviewer verified the runway's framing instead of independently deriving
   the caller set, failure states, feasibility constraints, and smaller
   alternative; and
4. the queue mutation treated the stable free-form clean review as sufficient
   semantic authorization even though the stable system did not define the
   evidence needed for those conclusions.

The queue commit contains `CURRENT.md`, `LEDGER.md`, `dispatch.md`, `runway.md`,
and `review.md`. Those are the correct stable artifacts. The missing assurance
is not a candidate receipt; it is a stable review record that reconstructs and
supports the semantic conclusions the queue is asked to trust.

## Gap-To-Cause Traceability Matrix

| Gap | Earliest prevention stage | Existing instruction | Why it failed | Root-cause class | Recommended target | Test |
| --- | ------------------------- | -------------------- | ------------- | ---------------- | ------------------ | ---- |
| No production `work-batch/v1` request/result/progress contract or implemented owner existed | Source resolution, before slice decomposition | General proportionality and stop-on-new-public-command prose in the dispatch and create-spec procedure | No loaded rule made proof of a decisive new owner interface a prerequisite; fixture behavior was allowed to stand in for the production primitive | `instruction_absent`; `planner_evidence_missing`; `historical_failure_not_routed`; `test_coverage_missing` | Planner contract and ownership-transfer planning reference | A plan whose decisive interface exists only in fixtures must block for a bounded feasibility proof |
| Green baselines exercised fixture owners and fixture-local execution state, not the installed owner | Planner evidence contract | Planner was expected to use repository evidence and record required-green baselines | The contract did not distinguish proof of target behavior from proof of the actual installed owner; planner-authored labels were sufficient | `planner_evidence_missing`; `instruction_allows_self_attestation`; `counterfactual_not_required` | Planner evidence rules and reviewer reconstruction | Reviewer receives green fixture evidence plus an absent production caller and must return corrections |
| Slice 1 transferred the clean path without a fail-closed validation/review/receipt/interruption result bridge | Semantic replacement audit, before accepting Slice 1 | Dogfood policy requires independently usable state, residue, rollback, and no silent fallback | “Scenario” and “independently usable” were too abstract; reachable failure paths and the exact next owner were not enumerated | `instruction_too_abstract`; `semantic_replacement_audit_not_required`; `slice_boundary_rule_too_weak`; `counterfactual_not_required` | Planner migration rules and reviewer failure-path reconstruction | A clean-path migration with retries/recovery still owned by the old system must be rejected |
| Artifact-only next-slice progression, resume, and candidate lease preparation were asserted but not demonstrated | Feasibility gate before implementation slices | Runway described artifacts as authority and rejected a new state store | No rule required a disposable proof that the existing artifacts support fresh-process selection, lease preparation, and resume | `instruction_absent`; `planner_evidence_missing`; `historical_failure_not_routed` | Conditional planner feasibility rule | A plan relying on an unproven artifact-selection primitive must block; a plan using an already-tested primitive must not |
| Slice 3 named APR as the temporary reconciliation caller even though APR's contract forbids the necessary queue mutation | Slice-boundary planning | Dogfood policy requires owner before/after, caller mapping, and independent usability | The named next caller was not checked against its live contract; “APR applies reconciliation” repeated an architectural label instead of proving a callable route | `planner_evidence_missing`; `reviewer_evidence_missing`; `reviewer_repeats_planner_claim`; `slice_boundary_rule_too_weak` | Planner exact-next-caller rule and reviewer direct-source check | An intermediate state with no coherent production consumer must be rejected |
| Slice 4 promised atomic same-batch reconciliation across two independently atomic CURRENT and LEDGER CAS operations | Feasibility and failure-state analysis before accepting Slice 4 | Planning contracts exposed narrow CAS mechanisms and the runway asserted ordered recovery | No loaded rule required an ordering, partial-apply state table, restart derivation, or proof of a compound receipt before claiming atomicity | `instruction_absent`; `planner_evidence_missing`; `counterfactual_not_required`; `deterministic_gate_is_structural_only`; `historical_failure_not_routed` | Conditional feasibility/counterfactual rule | Fault injection between the two writes must force correction unless every intermediate state and recovery owner is defined |
| Slice 4 combined reconciliation, partial-reconciliation recovery, dependency removal, runner/goal-runner cutover, docs, and broad tests | Planner boundary selection | Loaded dogfood policy requires independent usefulness and a smaller alternative for a clearly oversized slice | The model accepted “common rollback boundary” as sufficient even though S4A public reconciliation and S4B installed-caller cutover are independently usable; reviewer repeated it | `model_execution_failure_despite_sufficient_contract`; `slice_boundary_rule_too_weak`; `reviewer_repeats_planner_claim`; `test_coverage_missing` | Reviewer contract and regression scenario; retain current planner wording but clarify common rollback is not dispositive | A wide final slice justified only by common rollback must be split or supported by evidence that neither smaller state is usable |
| Migration matrix named capabilities or scenarios rather than the exact installed callers | Semantic replacement audit | Dogfood policy says every affected “scenario or caller” and every retained route must be mapped | The disjunction permits capability labels; schema keys are arbitrary strings and no completeness set is derived from source | `migration_matrix_schema_too_weak`; `semantic_replacement_audit_not_required`; `instruction_too_abstract`; `test_coverage_missing` | Planner/reviewer exact-caller rules; minimally strengthen existing migration evidence | A matrix with “closeout callers” but an omitted cron/goal-runner/direct skill caller must fail review |
| Direct skill entrypoints, goal-runner, v1 agents, installed dependencies, and documentation callers lacked explicit terminal dispositions | Source resolution and replacement audit | Dogfood policy requires retained caller, reason, future owner, and removal condition | The planner never constructed the full old-entrypoint set; the reviewer accepted the supplied matrix rather than comparing it with source | `semantic_replacement_audit_not_required`; `planner_evidence_missing`; `reviewer_evidence_missing`; `instruction_allows_self_attestation` | Planner source-resolution checklist and reviewer caller-set comparison | Old routes discovered in pinned manifest/skill/runner/agent sources but absent from the matrix force correction |
| No required-green counterfactual could fail on accidental Batch Runway or APR invocation | Acceptance design before queue review | Create-spec asks for fail-on-bypass/duplication/reimplementation validation in general terms | It did not require one ownership-transfer counterfactual tied to every forbidden fallback; topology and wording checks were treated as behavioral proof | `counterfactual_not_required`; `instruction_too_abstract`; `test_coverage_missing` | Planner/reviewer migration acceptance rules | Poison the legacy route while keeping it installed; acceptance must fail if any normal caller reaches it |
| Decisive filesystem, commit/receipt, lease, and reconciliation primitives were not proved before large slices | Conditional feasibility gate | General block-on-new-store/protocol wording and known mechanisms | The rule recognized scope expansion, not feasibility risk in composing existing primitives; prior foundation failure was not routed | `instruction_absent`; `planner_evidence_missing`; `historical_failure_not_routed` | Planner conditional feasibility rule and source resolver | A cross-platform filesystem confinement or two-store recovery claim must carry disposable proof before queueing |
| Per-slice expected cost, review/install cadence, and duplicated final validation multipliers were absent | Proportionality analysis | Planner records observed problem, minimum viable change, alternatives, and qualitative proportionality | No rule requests nearest-analogue file/line/runtime evidence or repeated-gate multipliers | `cost_measurement_not_required`; `historical_failure_not_routed`; `instruction_absent` | Planner proportionality contract and reviewer cost heuristic | A migration with repeated 60-second acceptance gates and four slices must expose the multiplier or justify unknowns |
| “Independently usable” intermediate states had no exact current production consumer or complete failure-path owner | Planner slice boundary, then reviewer | Dogfood policy and create-spec both require independently useful/testable boundaries | The term was satisfied by prose; neither contract defines usability as a reachable caller plus owned normal and failure outcomes | `instruction_too_abstract`; `slice_boundary_rule_too_weak`; `instruction_allows_self_attestation` | Reusable slice-boundary rule | Producer-only state with no current consumer must fail; a state used by one exact caller and safely recoverable must pass |
| Independent review returned clean without independent evidence reconstruction | Reviewer handoff | Stable process required an independent review in practice, but no reusable stable instruction defined the reconstruction and evidence duties | Output permitted bare conclusions and the review followed the planner's framing instead of deriving exact caller, failure, feasibility, counterfactual, and cost facts | `instruction_absent`; `reviewer_evidence_missing`; `reviewer_repeats_planner_claim`; `instruction_allows_self_attestation`; `temporary_policy_leak` | Stable plan-batch/review handoff and review evidence contract | A reviewer that submits passes with no evidence references/reconstruction must be rejected before queueing |

## Why The Planner Missed The Gaps

### The stable planner contract left semantic ownership implicit

The principal agent correctly owned planning under the stable command owner and
authored the Markdown plan after a bounded `codebase_investigator` supplied
source findings and a candidate slice shape. Stable does not require a
registered planner role, and the absence of candidate planner machinery is not
a defect.

The defect is that the loaded stable command/create-spec instructions did not
explicitly assign these necessary planning decisions to the principal agent or
define their evidence standard:

- minimum-change selection;
- semantic replacement completeness;
- exact caller-set derivation;
- proof that intermediate states had current production consumers;
- counterfactual acceptance design;
- feasibility proof selection;
- cost estimation; and
- the minimum recorded evidence a later reviewer must independently verify.

The stable create-spec contract contains useful semantic split guidance, but it
is a prose authoring procedure. It asks for independently testable slices,
producer/consumer seams, adjacent-pair rationale, and failure on bypass or
reimplementation. It does not define the evidence necessary to prove those
claims for an ownership transfer.

### The source packet omitted the nearest negative evidence

The dispatch's authoritative sources include COR-009, ADR 0004, the carry-
forward finding, the slice-shape policy and correction, the temporary dogfood
policy, and candidate source. It labels the rejected CCFG-26 execution-state
foundation and CCFG-26B as historical evidence, but does not route the following
as required planning-risk evidence:

- CCFG-25's closeout size and command-runtime evidence;
- CCFG-25's repeated validation-command and caller-inventory amendments;
- CCFG-25's execution anomalies;
- the rejected CCFG-26 foundation retrospective;
- the foundation's late filesystem feasibility blocker;
- the self-hosting contradiction and fresh-process attempt barrier; and
- the post-closeout slice-policy correction's explicit old/new authority and
  forbidden-residue counterfactual.

Historical artifacts should not prescribe target architecture. That valid
authority rule was over-applied: non-authoritative history was also not treated
as mandatory negative evidence. As a result, the planner repeated failure modes
whose exact shape was already documented.

### The loaded policy allowed semantic self-attestation

The temporary dogfood policy is materially better than the old fixed-slice
policy. It requires owner before/after, migrated callers, focused validation,
independently usable state, rollback, temporary residue, a migration matrix, no
silent fallback, retained-route dispositions, and smaller alternatives.

Its enforcement vocabulary is still too weak:

- `scenario_or_caller` permits a capability label instead of an exact callable
  entrypoint;
- “independently usable” has no required exact next consumer or failure-path
  owner;
- “no silent fallback” has no required counterfactual;
- “clearly oversized” lets the planner decide whether the stronger duty applies;
- “smaller-alternative analysis” does not require the reviewer to construct its
  own alternative; and
- no cost or feasibility evidence is required.

The planner could therefore satisfy every visible field with its own
conclusions. The plan's four vertical blocks looked complete while the exact
production mechanisms remained unproved.

### Historical examples biased shape rather than semantics

The immediately preceding work focused on repairing horizontal decomposition
and the stale one-slice-per-invocation policy. That correction made “vertical,”
“durable,” and “common rollback boundary” salient. It did not make exact caller
replacement, failure-path ownership, counterfactuals, feasibility, or cost
equally salient.

The current policy no longer requires one slice per invocation, so the stale
policy did not directly constrain the current four-slice plan. Its residue was
the framing: planning quality was treated primarily as a slice-shape question.
The temporary policy carried that narrow framing into the stable generation.

## Why Deterministic Validation Missed The Gaps

### Stable validation was structurally correct and semantically incapable

The stable queue flight used Planning State and related checks. In
`scripts/planning_state.py`, artifact registration and queue mutation validate
placement, registered paths, active-pointer cardinality, and state consistency.
Those are appropriate deterministic responsibilities. None evaluates whether:

- a caller label names a real installed entrypoint;
- the caller inventory is complete;
- an old fallback is reachable;
- an intermediate state has a production consumer;
- a two-write reconciliation claim is safe;
- a counterfactual can expose legacy invocation;
- a new filesystem or Git primitive is feasible; or
- repeated validation makes the plan disproportionately costly.

The stable policy tests also passed because
`tests/test_stable_runway_dogfooding_policy.py` checks that the policy is loaded
and contains expected terms. It does not present a bad plan to a planner or
reviewer and require rejection.

### Non-controlling candidate gate comparison

The candidate gate did not and could not participate in CCFG-26 planning. It was
inspected only to determine whether the same omissions would survive the
eventual post-CCFG-29 merge.

The candidate schema and `scripts/plan_batch.py` would have caught:

- missing required result fields;
- malformed enums and empty required strings/lists;
- a missing migration matrix;
- absent or mismatched draft/evidence digests;
- an unclean reviewer verdict;
- a required review check not marked `pass`; and
- queue-state and lineage inconsistencies.

They would not have caught the reported gaps. The candidate migration matrix
uses arbitrary non-empty keys and values. Reviewer checks are pass/fail labels.
The tests construct generic values such as “fixture planning caller,” manufacture
all review checks as `pass`, and verify rejection mainly for missing fields,
empty values, bad hashes, or a planner that self-declares over-specification.
This is a future-integration concern, not a cause of the current failure.

The forensic audit of the actual stable flight instead shows the relevant
stable boundary:

```text
GREEN stable_controller_authority
GREEN planning_state_structure
RED semantic_replacement_audit
RED independent_review_evidence_basis
RED legacy_counterfactual
```

The green checks confirm that the correct generation controlled the flight and
that canonical state was structurally valid. The red checks ask whether the
stable plan/review recorded the source-derived replacement audit, evidence for
semantic review conclusions, and a counterfactual capable of detecting legacy
invocation. They did not.

### What belongs where

The proposed `semantic_replacement` block in the investigation prompt contains
useful information, but a new top-level persisted schema is not the first or
smallest prevention point.

| Concern | Smallest appropriate owner |
| --- | --- |
| Derive observed problem and minimum viable change | Planner reasoning; reviewer independently reconstructs |
| Derive complete old/new caller and entrypoint sets | Planner reasoning from pinned source; concise persisted migration evidence for executor terminal conditions |
| Decide why a legacy route is retained | Persisted runway evidence because execution and closeout must know its removal condition |
| Identify forbidden fallbacks | Persisted acceptance/validation text; optionally a compact existing migration-evidence field |
| Design counterfactuals | Planner reasoning and persisted required-green acceptance commands |
| Prove semantic completeness | Reviewer reasoning from pinned evidence, not deterministic validation |
| Check caller identifiers are non-empty, unique, and aligned across existing fields | Deterministic validation |
| Check feasibility of a new primitive | Conditional planner proof and reviewer inspection; a focused fixture when mechanically reproducible |
| Estimate cost | Planner proportionality reasoning and reviewer heuristic; no universal schema requirement |

Deterministic validation should remain conservative. It may validate that an
explicit fact exists, is well formed, is uniquely identified, and is referenced
consistently. It must not convert planner-authored strings into proof that the
fact is true.

## Why The Independent Reviewer Returned Clean

### Stable supplied an independent agent but not an independent method

The review says “independent read-only `batch_plan_reviewer`,” and the actual
review was performed by a separate read-only agent as intended. Stable does not
require that agent to use the candidate `batch-plan-review/v1` role, and it
would have been wrong to load candidate runtime instructions.

The stable failure is narrower: no loaded stable instruction defined the
reviewer's independent reconstruction steps, minimum evidence packet, or
evidence-bearing result shape. The reviewer was independent in agent identity
but was free to use the runway's framing as its method.

The actual review read substantial repository evidence, including candidate
source. The failure was not lack of effort. It was that no loaded contract
required the reviewer to reconstruct the decisive facts or show its work.

### Non-controlling candidate review comparison

The future candidate contract was not eligible to control this flight and is not a
remedy before CCFG-29. It was inspected only to avoid carrying the same weakness
through the eventual merge. It improves role separation and binds four digests,
but it also
limits the reviewer to the evidence packet supplied by `plan-batch`, forbidding
additional repository exploration. It asks for independent judgment, but its
result contains pass/fail checks, corrections, blockers, and residual risks—no
required evidence references or reconstructed problem, caller set, fallback
set, counterfactual, feasibility premise, or cost calculation.

After future integration, a planner-selected packet could omit the evidence needed to contradict the
planner, and the reviewer can mark a check `pass` without recording the basis.
Digest binding would prove what was reviewed, not that the packet was sufficient.
This does not explain the current stable review; it identifies a separate gap to
fix before the candidate implementation becomes authoritative.

### Required reconstructions were absent

The actual stable review instructions did not require the reviewer to
independently reconstruct any complete set of the following:

- the observed production problem;
- the minimum viable change;
- the semantic replacement audit;
- exact old and new callers and entrypoints;
- forbidden legacy residue and retained-route terminal conditions;
- required-green counterfactuals;
- per-slice expected cost and repeated validation multipliers;
- feasibility assumptions for decisive primitives;
- the widest slice's best smaller alternative; and
- exact production consumers and failure owners proving intermediate states are
  independently usable.

The actual reviewer therefore followed the planner's four-slice frame. It
checked whether the runway contained the expected headings and claims, not
whether a fresh reconstruction produced the same plan.

### Review conclusions without sufficient recorded evidence

The following `review.md` conclusions are unsupported or under-supported by the
recorded analysis:

| Review line | Conclusion | Missing recorded support |
| --- | --- | --- |
| 39 | COR-009 purpose, removal boundary, and acceptance coverage passed | Exact old/new entrypoint set, retained-route terminal conditions, forbidden fallback set |
| 42 | Four vertical, independently usable slices passed | Exact production consumer and complete normal/failure outcomes after each slice |
| 43 | Adjacent-boundary and per-slice smaller-alternative analysis passed | Reviewer's own S4A/S4B alternative and evidence that it was not independently usable |
| 44 | Migration evidence and temporary ownership matrix passed | Source-derived complete caller set and exact set comparison with the matrix |
| 45 | Rollback points passed | Post-first-CAS partial reconciliation states and durable recovery ordering |
| 46 | Artifact-only startup, recovery, review, and closeout passed | Production implementation/prototype and fresh-process evidence |
| 47 | Required-green and known-red statuses passed | Counterfactual capable of failing on old-owner invocation; proof that fixture greens exercise the installed owner |
| 49 | No new execution state, runtime protocol, or self-hosting passed | Proof that artifact-only progression and lease preparation are sufficient without hidden state |
| 60-63 | Wide Slice 4 risk is bounded by common rollback and focused review | Cost evidence, partial-apply recovery, exact caller breadth, and independent S4A/S4B analysis |

Planning State currentness, one-batch selection, exact checkout identity, no
successor, and stop-before-implementation were directly supportable. The
problem is not that every review line was false; it is that semantic conclusions
were recorded in the same unqualified `pass` form as mechanically proven facts.

## Instruction Loading And Priority Problems

### Instruction surface inspected

The investigation did not assume that `skills/plan-batch` was the complete
surface. It traced the instructions and executable checks actually reachable in
both generations:

- stable root `AGENTS.md` and candidate root and `.codex/AGENTS.md` files;
- stable and candidate `skills/plan-batch/**`, including command metadata;
- stable Architecture Program Runway selection/queue instructions and Batch
  Runway `create-spec` references, including cross-checkout, validation,
  reviewer, recovery, and fallback guidance loaded by those skills;
- candidate `agents/batch_planner.toml` and
  `agents/batch_plan_reviewer.toml`, their exact YAML result contracts, and the
  registered-agent entries in `codex-features.json`;
- stable `scripts/planning_state.py` queue/artifact/state checks and candidate
  `scripts/plan_batch.py` planner, review, evidence, and transaction checks;
- Planning State and Planning Artifacts skill contracts and references used to
  locate, register, validate, and project Layout v1 state;
- stable temporary dogfood policy, its focused test, the completed slice-shape
  correction, and the earlier fixed-slice policy history;
- `docs/workflow-guide.md`, `docs/skill-routing-contract.md`, ADRs 0002–0004,
  and the command-owner planning-quality finding;
- stable and candidate planning/reviewer unit tests, schema tests, custom-agent
  contract tests, scenario catalogs/adapters, and behavior fixtures; and
- CCFG-25 plans, reviews, amendments, closeout, cost/anomaly evidence; rejected
  CCFG-26B and execution-state foundation artifacts; and the foundation
  retrospective and post-closeout corrections.

No hidden template, example, fallback reference, or nested instruction loaded by
the actual stable flight supplied the missing semantic audit. Candidate-only
instructions were inspected as target-generation evidence but were not treated
as stable runtime authority.

### Stable authority was correct and its quality contract was incomplete

ADR 0004 makes stable/candidate separation a development integrity boundary.
The stable controller must control CCFG-26; the candidate must not control its
own implementation. Therefore the correct fix is not for stable to import or
invoke the candidate runtime.

At planning basis `6b575614...`, the authoritative stable flow was exactly the
expected one:

- stable `skills/plan-batch/SKILL.md:57-63` routed to Planning State, Planning
  Artifacts, Architecture Program Runway, and Batch Runway create-spec;
- `docs/workflow-guide.md` and `docs/skill-routing-contract.md` described the
  same stable bridge.

Nothing in those facts indicates a loading error. The gap is that the stable
bridge and create-spec/review instructions did not own the necessary semantic
analysis or define how independent review must prove it.

The candidate at `5c5ec9d...` was available for product-source and future-
integration inspection only. Its registered roles and transaction machinery
were correctly absent from the stable execution path.

### The temporary policy narrowed stable attention to slice shape

The temporary stable dogfood overlay correctly repaired the stale slice-shape
policy. It did not claim to replace the whole stable planning system. However,
the stable planning flight treated compliance with that focused policy as strong
evidence of overall planning quality even though no stable reusable rule also
required:

- semantic replacement reconstruction;
- independent review evidence;
- feasibility or counterfactual requirements;
- cost analysis; or
- semantic behavioral regression tests.

This is the relevant `temporary_policy_leak`: a narrow project-local slice-shape
policy was allowed to stand in for broader stable planning assurance. It is not
a claim that candidate machinery should have been copied or invoked.

### No priority conflict excuses the omissions

The project policy did not override a stronger loaded reusable rule. The loaded
stable instructions were mutually consistent but collectively incomplete. The
root instructions correctly required both checkouts to be inspected, and that
occurred. Candidate source inspection supplied product evidence; it did not and
could not supply stable planning authority.

The only material historical priority conflict was the old one-slice-per-
invocation policy. It had already been removed before the current CCFG-26 plan.
It explains earlier CCFG-26B/foundation shape failures, not the current plan's
semantic omissions.

## Repeated Failure Patterns Across Prior Batches

### CCFG-25

CCFG-25 demonstrated the same gaps before CCFG-26 was planned:

- Its final closeout covered 38 files and roughly 5,223 insertions / 1,602
  deletions; exact acceptance evidence took about 39–62 seconds per run.
- The execution report found sibling runner owners and four support-skill callers
  after the original plan/review had missed them.
- Validation commands and type-check scope required bounded amendments.
- Installation and isolated acceptance were valuable, but multiplied execution
  cost.
- Its strongest review was adversarial because it reconstructed contradictory
  green/red evidence, install executability, sole-owner feasibility, vocabulary
  proxies, preservation coverage, and proportionality. That strength was not
  encoded into the reusable reviewer contract.

Repeated causes: `historical_failure_not_routed`,
`semantic_replacement_audit_not_required`, `cost_measurement_not_required`, and
`reviewer_repeats_planner_claim` when the review method is not explicit.

### Rejected CCFG-26 execution-state foundation

The superseded foundation required four code passes and eight reviews. Its first
slice inserted more than 4,000 lines while decisive filesystem confinement was
proved only after the commit. It asserted atomic/fail-closed behavior before the
underlying primitive made those claims true.

The later self-hosting amendment exposed that an empty candidate execution state
would reselect Slice 1 even though stable had already completed it. The progress
and attempt-barrier corrections similarly found that durable artifacts did not
yet imply a deterministic fresh-process selection rule.

Repeated causes: `planner_evidence_missing`, `counterfactual_not_required`,
`historical_failure_not_routed`, `slice_boundary_rule_too_weak`, and
`deterministic_gate_is_structural_only`.

### Slice-shape correction

The completed slice-shape correction found that competing old and new policies
survived despite green validation. Its effective correction named:

- exact old and new authority;
- forbidden residue;
- the terminal condition for the old rule; and
- a counterfactual in which the old horizontal default remained reachable.

That is the closest prior example of the semantic replacement audit missing
from CCFG-26. It was treated as a one-off policy correction rather than promoted
to a reusable migration-planning rule.

### Common pattern

Across all cases, the system validated the artifact it had been given rather
than forcing the planner and reviewer to disprove the most dangerous alternative
interpretation. Green structure and exact hashes consistently arrived before:

- exact caller completeness;
- negative reachability proof;
- fresh-process/failure-state proof;
- decisive primitive feasibility; and
- realistic execution cost.

This is a reusable planning-system failure, not a CCFG-26 topology accident.

## Missing Reusable Planning Rules

### 1. Semantic replacement audit for ownership transfers

Before slice selection, the planner must derive from pinned evidence:

- the decision being transferred;
- old owner and exact old entrypoints;
- new owner and exact new entrypoints;
- every normal caller;
- every retained route with reason, removal owner, and removal condition;
- forbidden fallbacks; and
- at least one counterfactual that exposes continued old-owner reachability.

This belongs in planner reasoning, with concise terminal facts persisted in the
existing migration evidence. It does not require a new schema family.

General example: when moving authentication from a framework session middleware
to an identity service, an environment-variable fallback and a background token
refresh worker must be classified even if the browser login path is migrated.

### 2. Failure-path ownership before clean-path cutover

A slice may not make a new clean path reachable while validation, review,
receipt, retry, interruption, or recovery can silently fall back to the old
owner. Every reachable outcome after the slice must have an explicit owner and
durable result.

General example: a payment adapter cannot move successful charges to a new
provider while retry and idempotency-conflict handling still re-enter the old
provider without an explicit compatibility contract.

### 3. Exact production consumer for every intermediate state

“Independently usable” means that at least one exact current production caller
can consume the state end to end and that all reachable failure outcomes are
owned. A future caller or a fixture is insufficient.

General example: a new event schema plus producer is not independently usable
when no deployed consumer can read it and failed deliveries still use an
unclassified legacy queue.

### 4. Conditional decisive-primitive feasibility proof

When the plan depends on a new public/deterministic boundary, cross-platform
filesystem behavior, multi-artifact atomicity/recovery, locking, or another
unproved primitive, the planner must either cite existing production proof or
place a bounded disposable proof before implementation slices. This is
conditional, not a universal prototype requirement.

General examples include transactional DDL in a database migration, browser
sandbox file access, cross-platform file locking, and conditional writes across
two cloud records.

### 5. Ownership counterfactuals

Every semantic ownership transfer needs at least one required-green test that
would fail if a forbidden old owner were invoked. Presence, manifest, and
wording assertions are not substitutes.

General example: leave an old CLI handler physically installed but poison its
execution; the new dispatch acceptance must stay green only if no normal route
reaches it.

### 6. Bounded cost evidence for high-multiplier plans

For migrations or plans with repeated expensive gates, proportionality must
record the nearest analogue or explicitly state unknowns for:

- likely files/surfaces and rough change range;
- focused command runtimes;
- install/fresh-home cadence;
- worker, reviewer, and specialist passes; and
- duplicated final gates.

No hard universal line or runtime threshold is warranted.

General example: a small logging adapter may still require dozens of caller
rewrites and repeated integration environments; semantic size alone understates
execution cost.

### 7. Historical negative evidence routing

The source resolver must include the nearest analogous blocker, retrospective,
post-closeout correction, and cost evidence when they share the same risk. Such
evidence is explicitly non-authoritative for target design but mandatory for
risk questions.

General example: a prior database migration's lock-timeout retrospective does
not dictate the next schema, but it must be routed when the new plan depends on
the same online-DDL primitive.

## Missing Reviewer Rules

The reviewer must independently reconstruct, from pinned evidence:

1. the observed problem and minimum viable change;
2. the exact old/new owner, entrypoint, and caller sets;
3. retained routes, removal terminal conditions, and forbidden fallbacks;
4. normal and failure-path ownership after each slice;
5. the exact production consumer proving each intermediate state is useful;
6. at least one legacy-invocation counterfactual;
7. decisive feasibility premises;
8. the widest slice's best smaller alternative; and
9. cost multipliers for migrations or expensive repeated gates.

For the semantic checks, a `pass` must cite concise evidence identifiers or
paths and state the reconstructed fact. The reviewer must return a blocker when
the supplied evidence packet is insufficient. If the reviewer is restricted to
a packet, the packet must contain the pinned source excerpts needed for this
reconstruction; alternatively, the independent reviewer may perform bounded
read-only inspection at those exact revisions.

The reviewer should not re-author the plan, prescribe universal slice counts,
or force migration fields onto a small non-migration plan. Its job is to falsify
the planner's claims at the seams most likely to hide duplicate authority.

## Missing Deterministic Enforcement

Deterministic enforcement should be added only where the fact is mechanical:

- bind the stable review to the exact dispatch and runway drafts;
- require evidence references for semantic review checks;
- require non-empty, unique exact caller identifiers for migration rows;
- validate set alignment between migrated callers, retained routes, and
  acceptance references when those facts are persisted;
- require at least one counterfactual reference for an ownership-transfer batch;
- reject a clean verdict containing missing/empty evidence references; and
- preserve existing queue/path/currentness/lineage validation.

The stable Markdown pipeline may not expose every item above as a parseable
field. In that case, the smallest current enforcement surface is the stable
planner/reviewer instruction plus a behavioral regression, not a new parser or
schema. Exact request/result interface validation becomes relevant only after
the candidate implementation is merged and authoritative.

It should not attempt to decide whether the caller set is complete, whether a
smaller slice is truly usable, whether a feasibility proof is persuasive, or
whether the cost is acceptable. Those require planner/reviewer reasoning and
focused behavioral scenarios.

The complete proposed `semantic_replacement` YAML block is therefore not P0.
The existing migration evidence and matrix should first be strengthened with
exact identities and terminal conditions. A compact persisted extension is
justified only for facts the executor or deterministic gate must consume.

## Missing Regression Scenarios

Across the inspected stable and candidate generations, current tests prove
policy text, field presence, hash binding, role separation where applicable,
and structural queue behavior. The authoritative stable tests do not prove that
the planner or independent reviewer rejects a semantically misleading but
well-formed plan.

The missing scenarios must run at the planner/reviewer behavior boundary using
small pinned evidence packets. They should deliberately make the planner's
prose plausible while embedding one contradictory source fact. The expected
failure is a planner blocker/correction or an independent reviewer correction,
not a schema parse failure.

The scenario suite must also contain a valid small plan so the stronger rules do
not turn every change into a migration audit.

## Project-Local Versus Reusable Changes

| Change | Placement | Reason |
| --- | --- | --- |
| Semantic replacement, failure-path, caller, counterfactual, conditional feasibility, and high-multiplier cost rules | Reusable planner/reviewer contracts | They apply to ownership transfers and migrations in any repository |
| Independent-review reconstruction and evidence binding | Reusable stable `plan-batch` / create-spec review handoff | Evidence-backed review is generic and does not require a new role |
| Exact stable/candidate roots, ADR 0004 generation boundary, CCFG-26 through CCFG-29 source rules | Project-local root instructions and temporary dogfood policy | They describe this repository's bootstrap topology |
| Temporary CCFG-26-through-29 trigger for the strengthened stable rules | Project-local dogfood policy | It selects when general ownership-transfer duties apply without importing candidate behavior |
| CCFG-25/foundation/slice-correction evidence routing | Project-local CCFG-26 source packet | The artifacts are specific; the rule to route nearest analogous failures is reusable |
| Planning State pointer/path/hash checks | Reusable Planning State | They are correctly generic and should stay structural |
| Cost thresholds, telemetry, or mandatory coordinator flights | Nowhere | They are overfitted or outside planning-quality prevention |

The temporary project policy must not become a generic Codex-config topology in
reusable skills. Conversely, project policy should not be the only home of
general semantic replacement and counterfactual rules.

## Recommended Changes By File

| Target | Responsibility to add or strengthen | Layer | Prevents | Why current rule is insufficient | Scope | Smallest test | Cost/risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `skills/plan-batch/SKILL.md` | Make the stable review handoff require an independent reconstruction, pinned evidence basis, corrections/blockers, and exact-draft binding before queue mutation | Command owner | Bare semantic passes and planner-framed review | Current stable bridge delegates spec creation but does not define review evidence duties | Reusable | Evidence-free clean review cannot authorize queue | Moderate review cost only for plans that require independent review |
| `skills/batch-runway/references/create-spec.md` | Add semantic replacement, failure-path owner, exact consumer, counterfactual, conditional feasibility, and high-multiplier cost duties for legacy stable planning | Planner support | Current stable omissions before cutover | Existing semantic split guidance is qualitative | Reusable | Ownership migration fixture with old retry fallback is rejected | Moderate planning tokens only for migration/risk triggers |
| Candidate `agents/batch_planner.toml` and `agents/batch_plan_reviewer.toml` | After CCFG-29 and merge, mirror the strengthened stable semantic/review duties so integration does not regress them | Future planner/reviewer | Reintroduction of the same omissions after cutover | Current candidate contracts still accept self-attested semantic passes | Reusable after merge; non-controlling now | Post-merge scenarios produce the same verdicts as stable | No current CCFG-26 prevention; explicitly deferred |
| Candidate `scripts/plan_batch.py` and `schemas/planning-runway-v1.schema.json` | After CCFG-29 and merge, validate only mechanical evidence references, exact caller identity/uniqueness/alignment, and counterfactual presence | Future deterministic gate | Structurally incomplete future evidence | Current candidate gate accepts non-empty prose and bare passes | Reusable after merge; non-controlling now | Post-merge mutation tests for missing refs, duplicate callers, and missing counterfactual | No current dependency; avoid semantic false confidence |
| `docs/plans/programs/codex-config/notes/stable-runway-dogfooding-policy.md` | Temporarily trigger the strengthened stable semantic replacement, counterfactual, feasibility, and independent-evidence duties for CCFG-26 through CCFG-29 | Project policy | Recurrence before cutover | Current policy focuses on slice shape and caller fields | Project-local and temporary | Focused CCFG-26-like scenario must fail under stable procedure | Temporary routing only; reusable rules stay outside this file |
| `docs/workflow-guide.md` | Document that queue validity is not semantic plan approval and define the stable independent-review evidence boundary | Workflow documentation | Misinterpretation of green Planning State | Current guide explains lifecycle, not quality assurance | Reusable explanation | Documentation consistency test only | No runtime prevention by itself |
| `docs/skill-routing-contract.md` | Clarify which stable command/support instruction owns independent planning review and its stop condition | Routing documentation | Diffuse review ownership | Current table ends at support skills | Reusable | Documentation consistency test only | Low; secondary enforcement |
| Post-merge `tests/test_plan_batch.py`, custom-agent tests, and scenario adapters | Mirror stable semantic regressions after candidate integration and stop manufacturing every semantic check as `pass` | Future tests | Post-cutover structural self-attestation | Current candidate fixtures primarily prove fields/hashes | Reusable after merge | Missing evidence/counterfactual/caller alignment rejects | Deferred until authoritative integration |
| `tests/test_stable_runway_dogfooding_policy.py` | Replace or supplement string-presence proof with a bad-plan rejection scenario | Project-policy test | Temporary overlay appearing effective when only loaded | Current test proves wording only | Project-local temporary | Stable review rejects a fallback-survival plan | Temporary maintenance until CCFG-29 |

## P0 Changes

1. **Give the stable independent review an explicit reusable method.** The
   stable command owner must require reconstruction of the decisive semantic
   facts, concise repository evidence, exact-draft binding, and corrections or
   blockers before a clean review can authorize queue mutation. This strengthens
   the existing independent handoff; it does not add or import an agent role.
2. **Require a semantic replacement audit for ownership transfers.** Exact old
   and new entrypoints, all normal callers, retained routes, terminal conditions,
   and forbidden fallbacks must be derived before slices are selected.
3. **Require failure-path ownership before clean-path cutover.** Validation,
   review, commit/receipt, interruption, retry, and recovery cannot silently
   return to the old owner.
4. **Require at least one legacy-invocation counterfactual.** It must be
   required-green and capable of detecting the old route while the old physical
   code may still exist.
5. **Require conditional feasibility proof for decisive unproved primitives.**
   New deterministic boundaries and multi-artifact atomic/recovery claims must
   be proved or block planning.
6. **Make the reviewer reconstruct rather than confirm.** It must derive the
   problem, minimum change, caller/residue sets, failure states, production
   consumers, counterfactuals, decisive primitives, and widest smaller
   alternative from pinned evidence, and cite a concise basis.
7. **Define independent usability operationally.** Every intermediate state
   needs an exact current production consumer and owned reachable failures.
   Common rollback alone cannot reject a smaller independently useful split.
8. **Make the temporary project policy trigger these stable reusable checks for
   CCFG-26 through CCFG-29.** Candidate planning code remains completely outside
   the controlling path.

These are required before another ownership-transfer plan is trusted because
they prevent duplicate semantic authority, unreachable intermediate states, and
unproved recovery behavior—the risks that can invalidate the whole slice
sequence.

## P1 Changes

1. Route the nearest analogous blocker, retrospective, post-closeout correction,
   and cost evidence into the planner packet as non-authoritative negative
   evidence.
2. Require bounded cost evidence for migration/high-multiplier plans: expected
   surfaces, rough change range or explicit unknown, sampled command runtimes,
   install/review cadence, and duplicate final gates.
3. Add mechanical deterministic checks for exact caller identifiers,
   uniqueness, cross-field alignment, counterfactual references, and review
   evidence references only where the stable representation supports them;
   otherwise use focused behavioral tests until post-merge tooling is
   authoritative.
4. Add the focused behavioral scenarios below at the planner and reviewer
   contract boundaries.
5. Update workflow/routing documentation so green Planning State and exact
   hashes are never described as semantic plan approval.

These materially improve planning quality but are secondary to caller,
failure-path, feasibility, and review reconstruction.

## P2 Changes

1. After observing the strengthened contracts, consider a compact persisted
   semantic-replacement subsection only if the executor or deterministic gate
   repeatedly needs facts that cannot fit the existing migration evidence.
2. Consider a reusable nearest-analogue selector if manual historical routing
   remains inconsistent. Start with an explicit bounded source list rather than
   an automated history crawler.
3. Consider calibrated cost bands after several batches produce comparable
   evidence. Do not establish thresholds from CCFG-25 and CCFG-26 alone.

## Rejected Overengineering

- **Reject a new top-level schema family or persistent planning state.** The
  first failure was reasoning, review, and evidence enforcement, not absence
  of another store.
- **Reject persisting every useful review question.** Problem reconstruction,
  alternative generation, and feasibility judgment belong primarily to planner
  and reviewer reasoning.
- **Reject universal numeric line, file, token, slice, or runtime thresholds.**
  They would create false blockers and invite gaming.
- **Reject a new agent role.** The existing stable principal-agent planning and
  independent-review handoff are adequate seams; their instructions need
  strengthening.
- **Reject requiring telemetry or fresh coordinator flights as CCFG-26
  prerequisites.** Existing repository evidence is sufficient to estimate cost
  and design bounded counterfactuals.
- **Reject importing or invoking the candidate controller from stable.** That
  would violate ADR 0004's single-generation boundary.
- **Reject putting CCFG-26 paths or topology into reusable skills.** Exact roots
  and historical artifacts belong in project-local evidence and policy.
- **Reject reopening GitHub issues #59 or #61.** Nothing in this analysis needs
  those rejected issue surfaces.
- **Reject making all historical artifacts authoritative.** Route analogous
  failures as negative evidence; do not let superseded designs prescribe the
  target architecture.

## Proposed Regression Test Matrix

| Scenario | Expected planner result | Expected reviewer result | Expected deterministic gate behavior |
| --- | --- | --- | --- |
| New owner added while old semantic fallback survives | Return correction/blocker until fallback is classified and counterfactually excluded | Independently discover reachable fallback and reject clean verdict | Reject only if required fallback/counterfactual facts or refs are absent/malformed; cannot decide reachability itself |
| Migration matrix names capabilities but not exact callers | Require exact source-derived caller identifiers | Compare pinned caller set to matrix and return missing callers | Reject generic/missing caller identity or duplicate IDs once the field is explicit; cannot prove source completeness |
| Clean path transferred before failure-path ownership is defined | Refuse slice as not independently usable | Reconstruct validation/review/retry/interruption outcomes and reject | Structural gate passes only after required failure-outcome references exist; semantics remain reviewer-owned |
| Large final slice justified only by common rollback boundary | Produce the best smaller usable checkpoint or evidence neither checkpoint is usable | Independently propose the smaller split and reject unsupported common-rollback rationale | No slice-size decision; validate that required alternative evidence is present |
| No counterfactual capable of detecting legacy invocation | Add a required-green poison/tripwire test or block | Reject wording/topology-only acceptance | Reject ownership-transfer plan with no counterfactual reference; cannot judge its strength |
| Decisive implementation primitive is unproven | Add bounded disposable proof before implementation or block | Inspect proof/known production evidence and reject assertion-only feasibility | Require proof reference for conditionally flagged primitive; cannot assess proof quality |
| Final validation repeatedly duplicates expensive gates | Record cadence and cost multiplier; consolidate or justify | Check nearest-analogue/runtime evidence and challenge disproportionate repetition | Do not enforce cost threshold; at most validate required cost record for triggered batch kind |
| Reviewer accepts planner self-attestation without independent evidence | Planner output may be valid, but cannot authorize queue alone | Bare `pass` result is invalid; return evidence-backed reconstruction or correction | Reject clean review with absent evidence refs or bad exact-draft bindings where mechanically represented |
| Valid small non-migration plan | Produce one cohesive slice without migration-only ceremony | Confirm scope, acceptance, rollback, and proportionality; do not demand caller audit | Accept without migration-only caller/counterfactual/cost fields |
| Fixture green while installed production owner is absent | Mark baseline as target-behavior evidence only and block production slice on missing primitive | Detect mismatch between fixture owner and installed entrypoint | Structural gate cannot infer mismatch; may require evidence-type labels |
| Producer exists but no current consumer uses intermediate state | Merge/reorder slice or name a real consumer | Reject “independently usable” claim | No semantic rejection; validate explicit consumer identity if persisted |
| Two independently atomic stores are claimed as one atomic reconciliation | Require ordering, partial-state table, restart owner, and fault proof | Inject/check failure between writes and reject incomplete recovery | Validate presence of referenced fault scenario/receipt fields, not atomicity truth |

Tests should use deliberately small repositories or evidence packets. The
assertion should be the coarse disposition—plan, correct, or block—not exact
prose. This limits model-eval brittleness and token cost.

## Minimum Safe Implementation Sequence

This sequence changes the reusable planning system without amending or executing
CCFG-26 as part of the investigation:

1. Add failing stable regression scenarios for missing exact callers, fallback
   survival, absent counterfactual, unproved decisive primitive,
   unsupported wide-slice rationale, shallow review evidence, and a valid small
   plan.
2. Strengthen the stable command/create-spec and independent-review instructions
   until those semantic scenarios produce the expected corrections/blockers.
3. Add the minimal stable deterministic checks for exact-draft binding,
   evidence references, exact caller identity/uniqueness/alignment, and
   counterfactual presence where the current artifact shape supports them.
4. Make the temporary dogfood policy trigger the stable reusable rules for
   CCFG-26 through CCFG-29.
5. Add bounded historical negative-evidence routing and cost analysis.
6. Update workflow and routing documentation to describe the resulting assurance
   boundary.
7. Re-run both negative scenarios and the valid-small-plan control before using
   the stronger system to reconsider any queued ownership-transfer plan.
8. Only after CCFG-29 and branch integration, mirror the proven stable duties and
   regressions into the now-authoritative candidate-derived pipeline.

The stop condition is a planning pipeline that can demonstrate both: (a) each
requested bad plan is corrected or blocked for the intended reason, and (b) the
valid small plan still queues without migration-only burden. This sequence does
not select, amend, execute, or requeue CCFG-26.

## Open Questions Requiring User Direction

1. **Stable enforcement timing:** should another CCFG-26-through-29
   ownership-transfer planning flight be prohibited until the stable reusable
   semantic-review rules and regressions are strengthened, or may the current
   stable process use the explicit checklist manually first?
2. **Persisted minimum:** should exact caller identities, retained-route terminal
   conditions, and counterfactual references extend the existing migration
   evidence, or should some remain reviewer-only? The recommendation is to
   persist only facts needed by execution/closeout and keep reconstruction in
   planner/reviewer reasoning.
3. **Historical routing policy:** should the planner receive an explicit
   project-curated list of nearest analogous failures, or should source
   resolution select the nearest blocker/retrospective by risk tag? The former
   is safer and smaller initially.
4. **Reviewer evidence access:** should the stable independent reviewer receive
   a complete bounded evidence packet, or perform bounded read-only access to
   pinned revisions when the packet is insufficient? Either can work; bare
   semantic passes without a recorded basis cannot.

No other user decision is needed to establish the root cause. Telemetry, a new
coordinator flight, new persistent state, successor selection, and reopening
rejected issues are not prerequisites.
