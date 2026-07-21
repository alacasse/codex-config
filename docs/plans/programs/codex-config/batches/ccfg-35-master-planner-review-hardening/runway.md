# CCFG-35 Master Planner And Independent Review Hardening Runway

## Purpose

Execute one master-only CCFG-35 batch that hardens the planner actually used by
the stable Codex session. The accepted implementation must make evidence-backed
independent planning review a real pre-queue gate, strengthen applicable
semantic planning duties, preserve ordinary small-plan proportionality, and
leave independently verified closeout proof that the changed planner is the
installed planner sourced from master.

This runway supersedes no finding other than the historical CCFG-35 plan named
in its dispatch. Implementation has not started.

## Source And Status

- Covered finding: `CCFG-35` only.
- Source finding:
  `docs/plans/programs/codex-config/findings/planning-and-independent-review-hardening.md`.
- Dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-35-master-planner-review-hardening/dispatch.md`.
- Bounded proof-lane amendment:
  `docs/plans/programs/codex-config/batches/ccfg-35-master-planner-review-hardening/amendment.md`.
- Authoritative amendment review:
  `docs/plans/programs/codex-config/batches/ccfg-35-master-planner-review-hardening/amendment-review.md`.
- Superseded predecessor:
  `docs/plans/programs/codex-config/batches/ccfg-35-planning-independent-review-hardening/superseded.md`.
- Concrete status at queue time: `queued`; all execution rows remain `Pending`.
- Selected dispatch: `None` after queue transition.
- Active runway: `None` until a later explicit `work-batch` begins.
- Successor: `None`.

## Master-Only Implementation Authority

- Sole repository root: `/home/alacasse/projects/codex-config`.
- Sole implementation branch: `master`.
- Plan-time master basis:
  `a701a5a9d8810e67ad193f2955eea24a4886007b`.
- Stable Codex home: `/home/alacasse/.codex`.
- Canonical planning root:
  `/home/alacasse/projects/codex-config/docs/plans`.
- Candidate evidence-only identity:
  `/home/alacasse/projects/codex-config-command-owner-redesign` at
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`.

This is ordinary single-root work. Do not invoke the cross-checkout helper,
acquire candidate live leases, mutate the candidate checkout, or install into
the candidate Codex home. Before every worker or reviewer handoff, the
coordinator must verify that the implementation root is still on `master`, the
observed movement is explained by accepted batch commits, and the handoff path
set is wholly inside the canonical repository. The ordinary v2 result fields
`verified_cross_checkout_precreation` and `verified_cross_checkout_context`
remain `null`.

## Current Master Baseline

The actual stable planning route at the plan-time basis is:

```text
installed /home/alacasse/.codex/skills/plan-batch
  -> repo skills/plan-batch/SKILL.md
  -> Planning State current/validate
  -> Architecture Program Runway selection and dispatch
  -> Batch Runway create-spec semantic planning
  -> independently delegated planning review when the coordinator supplies one
  -> Architecture Program Runway queue mutation
```

Observed facts:

- `scripts/codex_owner.py /home/alacasse/.codex/skills/plan-batch` reports
  `owner: codex-config`, source feature `plan-batch 1.0.7`, and the master repo
  skill directory.
- `readlink -f /home/alacasse/.codex/skills/plan-batch/SKILL.md` resolves to the
  master source, and the installed/repo SHA-256 values are both
  `3d042d0af3deba2ffbb2f49f3d9062cfa22999139206e97cb87b2a71c1a9cdff`.
- The public master `plan-batch` skill owns caller-visible planning decisions
  and routes to existing support skills.
- Architecture Program Runway owns selected dispatch and queue mutation.
- `skills/batch-runway/references/create-spec.md` owns semantic slice creation.
- Master has no candidate planner/reviewer TOMLs, deterministic plan-batch
  script, planning contract script, planning schema family, or candidate
  transaction store.
- `agents/runway_reviewer.toml` is an implementation-diff reviewer and is not
  the independent planning-review role.
- Stable installed feature-state versions lag current manifest versions for
  several already-linked skills. The live symlink content is authoritative
  evidence for which planner is used; final installation/status evidence must
  distinguish pre-existing version-state drift from CCFG-35 changes.

## Required End-To-End Route

The accepted implementation must leave exactly this semantic route:

```text
public plan-batch request
  -> canonical current/validate
  -> one bounded ledger selection and dispatch
  -> create-spec reconstructs applicable semantic evidence and writes one draft
  -> a separate read-only planning reviewer independently reconstructs facts
  -> exact dispatch/runway hashes and evidence references bind the result
  -> correction or blocker returns to plan-batch without queue mutation
  -> only planner=plan + reviewer=approve + binding=valid permits queue mutation
  -> plan-batch stops before implementation
```

### Ownership Matrix

| Decision or artifact | Current master owner | Accepted owner | Forbidden alternative |
|---|---|---|---|
| Human planning intent and stop point | `skills/plan-batch/SKILL.md` | same, deepened | candidate planner script or support skill acting as public owner |
| Canonical currentness and structure | Planning State CLI | unchanged | semantic completeness in Planning State |
| Selection, dispatch, queue mutation | Architecture Program Runway | unchanged, with clean-review gate | reviewer or deterministic helper mutating queue |
| Semantic draft and slice shape | Batch Runway create-spec | unchanged, strengthened | schema/parser deciding semantic truth |
| Independent planning review | currently practice-only | reusable handoff/result contract consumed by public `plan-batch` | new registered agent role or implementation-time `runway_reviewer` |
| Mechanical exactness | existing path/hash/pointer checks | exact draft/evidence binding only | caller completeness, usefulness, feasibility, or cost judgment |
| Implementation slice review | `runway_reviewer` | unchanged | planning review responsibilities |
| Installed planner provenance | master manifest/link plus repo source | same, verified at closeout | candidate home or manifest text without link/content evidence |

## Planning Evidence Applicability

The deeper semantic record is conditional. It applies when a plan transfers or
replaces semantic ownership, migrates a supported route, depends on an unproved
decisive primitive, creates an intermediate whose usefulness is disputed, or
has material execution/review multipliers. Ordinary small non-migration work
keeps its current compact scope, validation, rollback, and proportionality
record.

For applicable work, the planner and independent reviewer must cover:

- observed problem and minimum viable change;
- current/future semantic owners and exact entrypoints;
- normal callers and retained/deferred route dispositions;
- forbidden fallbacks and every reachable failure-path owner/result/consumer;
- exact current consumer and end-to-end behavior for every intermediate;
- at least one required-green old-owner behavioral counterfactual;
- decisive feasibility assumptions and production evidence or bounded proof;
- the widest slice's best smaller usable alternative and rejection reason; and
- available or explicitly unknown production, validation, install, worker,
  reviewer, specialist, and duplicated-final-gate cost multipliers.

Bare passes, copied planner claims, physical source presence, schema presence,
or fixture-authored conclusions cannot authorize queue mutation.

## Batch Kind And Slice Risk

- Batch kind: `mixed-risk`.
- Slice 1: `contract-narrowing`.
- Slice 2: `contract-narrowing`.
- Approval gate: a later explicit user `work-batch` while this exact runway and
  its reviewed amendment are the sole queue entry, master identity is unchanged
  except for accepted batch commits, the previous slice is accepted, and no
  stop condition is active. That authorization releases Slice 1 only. Slice 2
  requires a later explicit user approval of the measured smoke estimate under
  `Slice 1 Cost Gate`.

## Batch Non-Goals

- No candidate checkout or candidate-home writes.
- No strict cross-checkout runtime.
- No new registered planner or reviewer agent.
- No repurposing of `runway_reviewer`.
- No candidate script/schema/transaction port.
- No top-level schema family, persistent planning state, queue owner, public
  command, or compatibility wrapper.
- No deterministic semantic completeness, usefulness, feasibility, shape, or
  cost authority.
- No universal thresholds, mandatory product telemetry, routine live-model
  evaluation in ordinary `plan-batch`, permanent scenario service, or one live
  planner/reviewer pair per scenario. The only live semantic evaluation
  authority is the four-call batch-local budget below.
- No project-specific identities, paths, branches, policies, or Graphify
  dependencies inside reusable workflow contracts.
- No execution, finalization, reconciliation, or unrelated finding changes.

## Execution Contract

Use Batch Runway Standard Execution Contract v2 and Registered Agent Result
Contract v2. Use Compact Report Contract v1 only for coordinator receipts,
Compact Convergence Assessment v1 for routine reports, Orchestration Anomaly
Log v1 for suspicious coordination behavior, Standard Ledger Retention v1, and
Execute Slice Core v1.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/validation-profiles/project-harness-production.md`

Overrides:

- Single-root master identity and accepted-movement checks replace all
  cross-checkout verification for this batch.
- Each independent implementation review must additionally verify the changed
  behavior remains on the actual master planner route.
- Final review and closeout must satisfy `Required Accepted-Closeout Proof`
  below; a generic clean diff review alone is insufficient.

## Validation Profile And Baseline

Validation profile: `project-harness-production`, because the work changes a
user-facing installed workflow skill, queue authorization, review behavior, and
installer-visible content.

### Current Required-Green Baseline

- `required-green`: `python -m pytest -p no:cacheprovider -q tests/test_skill_routing_rule_ownership.py tests/test_batch_runway_create_spec_contract.py tests/test_semantic_slice_shape_contract.py`
- Measured on 2026-07-20 at master commit
  `e31256758f3d7b1d01309332c2e23e24e7dd7392`: 28 passed in 0.07 seconds of
  pytest time; `/usr/bin/time` recorded 0.29 seconds wall, 0.25 seconds user,
  0.04 seconds system, and 38,368 KiB maximum RSS.
- `required-green`: `git diff --check`.
- `required-green`: owner/link/content commands recorded in `Current Master
  Baseline` currently pass.

### Slice-Owned Remediation Baseline

The following two manifest contract tests currently fail because master skill
word wrapping and runtime-owner phrasing drifted from their assertions. Slice 1
owns aligning behavior and robust tests, after which both become
`required-green`:

```text
tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_executable_work_source_boundary_is_explicit
tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_plan_batch_command_owner_runtime_boundaries_are_explicit
```

Measured together on 2026-07-20 at the same commit: two expected failures in
0.04 seconds of pytest time; `/usr/bin/time` recorded 0.23 seconds wall, 0.20
seconds user, 0.02 seconds system, and 41,824 KiB maximum RSS.

### Known-Red And Diagnostic Baseline

- `known-red-baseline`:
  `tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_work_batch_reconciles_same_batch_closeout`
  fails on pre-existing unrelated `work-batch` successor wording. CCFG-35 must
  not silently fix or absorb it.
- `diagnostic-only` while CCFG-35 is queued:
  `tests/test_ccfg_26_development_boundary.py::Ccfg26DevelopmentBoundaryTests::test_current_state_has_an_empty_queue_and_hardening_next_action`
  hard-codes the pre-queue state. Do not treat its transient state assertion as
  planner implementation behavior.
- `diagnostic-only`: `./install.sh --status` records pre-existing installed
  feature-state version lag. It becomes a CCFG-35 gate only for feature versions
  directly changed by the batch.

### Historical Cost Warning

`../ccfg-23-behavioral-scenario-harness/execution-retrospective.md` records a
123-test acceptance suite at 814.32 seconds, 35 whole-catalog evaluations, and
an estimated 41,125 subprocess executions. It also records that two unchanged
reruns would cost 27:08 and recommends combined execution plus reusable
exact-commit receipts. CCFG-35 must treat that evidence as a constraint: batch
semantic evaluations, do not repeat unchanged gates by reviewer role, and
measure before expanding beyond Slice 1.

## Live Evaluation Authority And Call Budget

Master's semantic planner is instruction-driven Markdown, so final behavioral
acceptance may use live semantic evaluation. The user's 2026-07-20 correction
authorizes it only as a bounded batch-local closeout technique. It does not
authorize routine `plan-batch` evaluation infrastructure or one invocation per
scenario.

The normal execution budget is:

| Phase | Agent purpose | Normal invocations | Retry rule |
|---|---|---:|---|
| Slice 1 implementation | `runway_worker` | 1 | semantic correction returns to the same slice; record every repeat |
| Slice 1 implementation review | `runway_reviewer` | 1 | repeat only after a material correction |
| Slice 1 batched smoke | planner plus different planning reviewer | 2 | at most one transport-only retry per invocation |
| Slice 1 cost-gate review | separate read-only reviewer | 1 | no silent retry after `revise` or `block` |
| Slice 2 implementation | `runway_worker` | 1 | semantic correction returns to the same slice; record every repeat |
| Slice 2 implementation review | `runway_reviewer` | 1 | repeat only after a material correction |
| Final ten-packet lane | planner plus different planning reviewer | 2 | at most one transport-only retry per invocation |
| Changed-test quality review | `test-quality-review` | 1 | repeat only after a material test correction |
| Final exact-range review | separate independent reviewer | 1 | repeat only after a material correction |

The base orchestration shape is therefore eleven agent invocations, of which
exactly four are live planner/planning-reviewer semantic evaluations. The
rejected design used twenty final semantic calls plus two smoke calls before
the worker and review calls. A semantic `correct`, `revise`, or `block` result
is not a transport failure and must never be retried merely to obtain a more
favorable answer. Any transport retry records its reason, duration, and partial
usage separately.

Model and effort must be held constant between the two smoke invocations and
their corresponding final invocations when the orchestration surface supports
selection. The receipt records the actual model and effort when exposed and
`unavailable` otherwise; it must not infer or invent them. No token budget was
specified for this batch. Token counts are recorded when exposed, and
`unavailable` otherwise.

## Slice 1 Cost Gate

After Slice 1 implementation and implementation review, but before Slice 2:

1. Create two isolated packets: one valid ordinary-small-plan control and one
   negative exact-review packet with an evidence-free or draft-mismatched
   approval that must not authorize queue mutation.
2. Send both packets together to one planner invocation. Send both pinned
   inputs and both planner results together to one different read-only planning
   reviewer invocation. Apply and verify the two queue decisions separately.
3. Persist `smoke-cost-receipt.md` with exact accepted Slice 1 commit, source and
   packet hashes, invocation start/end timestamps and wall seconds, retry count
   and reason, serialized input/output bytes, output digest, queue outcomes,
   and model, effort, input/output/total tokens when exposed. Use `unavailable`
   for host-hidden fields.
4. Record the rejected alternative as twenty final semantic calls versus two
   final batched calls. Extrapolate the ten-packet lane from actual final packet
   byte counts when available; before the packets exist, use the conservative
   formula `smoke wall seconds * max(1, projected final input bytes / smoke
   input bytes)` for each role. Record assumptions and a range rather than
   presenting the estimate as a measured final duration.
5. Delegate a separate read-only cost-gate review bound to the exact smoke
   receipt and accepted Slice 1 commit. It must compare the per-scenario and
   batched shapes, assess the historical CCFG-23 multiplier evidence, verify
   the retry and receipt-reuse rules, and return `clean`,
   `correction_required`, or `blocked`.
6. Stop and report the measured receipt, estimate, and cost-gate verdict. Slice
   2 remains unauthorized until the verdict is `clean` and the user explicitly
   approves that measured estimate. A `work-batch` request made before the
   receipt exists does not pre-approve an unknown estimate.

The cost gate is a progression boundary, not a new implementation slice. A
correction to measurement or evidence does not authorize production changes
beyond Slice 1.

## Canonical Verdict And Queue Mapping

These are the only accepted values:

| Boundary | Values | Queue meaning |
|---|---|---|
| Planner disposition | `plan`, `correct`, `block` | only `plan` can continue to review |
| Planning-reviewer disposition | `approve`, `revise`, `block` | only `approve` can continue to mechanical authorization |
| Mechanical review binding | `valid`, `invalid` | only `valid` can continue |
| Queue decision | `authorized`, `not_authorized` | the only queue-facing result |
| Aggregate acceptance review | `clean`, `correction_required`, `blocked` | describes the complete expected scenario set; it never substitutes for a per-packet queue decision |

`queue_decision: authorized` is legal if and only if planner=`plan`,
reviewer=`approve`, binding=`valid`, all required evidence references are
present, and the draft/input hashes match. Every other combination, missing
value, unknown synonym, changed draft, stale evidence reference, or absent
review maps to `not_authorized`.

For the aggregate lane, `blocked` takes precedence when an invocation or
required fact is unavailable or contradictory. Otherwise any unexpected but
correctable disposition, binding, or queue result yields
`correction_required`. `clean` requires all nine negative packets to be
`not_authorized` for their intended reason and the positive control alone to be
`authorized`. Thus a negative packet's expected `correct`, `revise`, or `block`
does not make the aggregate review non-clean.

The aliases `clean`, `approve`, and `plan` are not interchangeable. Only the
full conjunction above authorizes one packet's queue mutation.

## Batched Actual-Master Behavioral Proof Lane

Final acceptance uses one batched planner invocation and one different batched
planning-reviewer invocation for all ten scenarios. If either invocation is
unavailable after its single allowed transport retry, stop before final
acceptance and closeout.

1. Create ten fresh temporary directories with `mktemp -d`. In each, create a
   minimal isolated Planning Artifact Layout v1 root containing only that
   scenario's `CURRENT.md`, program `CURRENT.md`, `LEDGER.md`, source finding,
   pinned repository-evidence packet, and empty batch target. Never point a
   fixture at canonical planning state.
2. Build a ten-entry manifest with unique scenario ID, root, expected result,
   SHA-256 for every input, and hashes of the exact accepted master
   planner/support files. Hash the serialized manifest and ordered packet
   bundle.
3. Launch one bounded planner subagent with the installed
   `/home/alacasse/.codex/skills/plan-batch/SKILL.md`, accepted master support
   references, and all ten isolated packets. Permit writes only inside the ten
   listed roots. Require ten separately indexed `plan`, `correct`, or `block`
   results, exact draft hashes when produced, and evidence identifiers. One
   packet's prose or evidence must not be cited for another packet.
4. Launch one different read-only reviewer subagent once, with the accepted
   Slice 1 planning-review contract, ten pinned inputs, the exact ordered
   planner output, and every produced draft. Require ten separately indexed
   `approve`, `revise`, or `block` results with independently reconstructed
   evidence and exact draft hashes. The reviewer must detect missing, duplicate,
   reordered, or cross-contaminated packet results and fail closed.
5. Apply the accepted master Architecture Program Runway decision separately
   to each root using the canonical mapping above. The nine negative packets
   must be `not_authorized`; the positive control must create exactly one
   queued runway in its own root. No batch-level approval may queue all roots.
6. Present an evidence-free approval, a changed draft after review, and a
   missing review result to the accepted queue boundary. Each must remain
   `not_authorized` without editing installed source.
7. Persist one final-lane receipt with source/packet/bundle/output hashes,
   per-invocation cost fields from the smoke schema, ten per-packet
   dispositions and queue outcomes, and temporary-root deletion results. Keep
   transcripts and generated prose out of canonical planning state.

The coordinator owns fixture construction, isolation, hashes, separate queue
application, telemetry capture, and summary acceptance. Batching shares calls,
not evidence or queue authority.

## Exact-Commit Validation Receipt Reuse

Every reusable validation receipt must include command, exact accepted commit,
changed-source hashes, input-manifest hash where applicable, relevant
dependency/configuration and environment identity, exit/result, wall duration,
and output digest. Later workers, implementation reviewers, test-quality
reviewers, and the final reviewer consume the receipt instead of rerunning the
same green gate against the same immutable inputs.

Rerun only when the commit, relevant source/test blob, command/selector,
dependency lock or installed feature version, configuration, environment,
scenario input, or expected behavior materially changes, or when the receipt
is missing or malformed. Record the invalidating fact. A fresh reviewer still
reconstructs semantic conclusions; receipt reuse avoids duplicate mechanical
execution and does not permit planner self-attestation.

## Slice Shape Rationale

- `1 -> 2`: Slice 1 creates a complete exact-review/queue-authorization gate
  already consumed by the public master planning route. Slice 2 extends the
  semantic evidence that gate consumes and adds broader falsification and
  installed-master closeout proof. This is a valid producer/consumer boundary;
  either commit can be reviewed and rolled back independently.
- Slice 1 is useful without Slice 2 because evidence-free reviewer `approve`
  can no longer queue any plan.
- Slice 2 is separately useful because substitutive and high-assumption plans
  can no longer omit the source finding's decisive facts while ordinary plans
  stay compact.
- Slice 2 is the widest slice. Its best smaller alternative is to split
  ownership/failure/counterfactual duties from feasibility/proportionality.
  Reject that split because both are conditional fields in the same create-spec
  evidence record and the same independent reviewer must assess their
  applicability before one queue decision; neither yields a distinct master
  route, validation environment, or independently consumed intermediate.

## Execution Ledger

| Slice | Title | Risk | Status | Commit | Validation | Review |
|---|---|---|---|---|---|---|
| 1 | Evidence-backed master planning-review gate | contract-narrowing | Pending | None | Pending | Pending |
| 2 | Applicable semantic assurance and master closeout provenance | contract-narrowing | Pending | None | Pending | Pending |

## Slice 1: Evidence-Backed Master Planning-Review Gate

### Scope

Deepen the actual installed public `plan-batch` owner and its existing master
queue route. Define one reusable, bounded, read-only planning-review handoff and
result contract inside the installed plan-batch skill surface. Require exact
dispatch/runway binding, independently reconstructed facts with evidence
references, and correction/blocked outcomes before Architecture Program Runway
may mutate the queue. Keep create-spec as semantic draft owner and Planning
State as structural owner.

### Allowed Files Or Areas

- `skills/plan-batch/SKILL.md`
- optional focused references below `skills/plan-batch/references/`
- `skills/architecture-program-runway/SKILL.md`
- `skills/batch-runway/references/create-spec.md` only for the produced review
  input/evidence boundary required by this slice
- focused tests for the public command route, exact review binding, evidence-
  free clean rejection, and queue authorization
- `codex-features.json` and `CHANGELOG.md` for the actual changed installed
  feature
- `docs/workflow-guide.md` and `docs/skill-routing-contract.md` only where the
  owner/handoff boundary changes.

### Non-Goals

- No broad replacement/feasibility/proportionality rules yet.
- No registered agent TOML, implementation-review changes, executable semantic
  planner, schema family, transaction store, or candidate port.
- No queue mutation by the reviewer.

### Acceptance Criteria

- Public `plan-batch` explicitly owns obtaining one independent planning review
  of the exact dispatch/runway before queue mutation.
- The review handoff gives a separate read-only reviewer pinned repository
  evidence, exact draft identities, applicability questions, and permission for
  bounded read-only reconstruction.
- A reviewer `approve` result records reconstructed facts plus non-empty
  evidence references; bare semantic passes or copied planner claims are
  invalid.
- Changed drafts invalidate the result; `revise`/`block` outcomes leave
  CCFG-35 unqueued and return control to the public planner.
- Architecture Program Runway queues only after consuming planner=`plan`,
  reviewer=`approve`, and binding=`valid`; it does not absorb semantic review
  ownership.
- Planning State remains structural and create-spec remains semantic draft
  owner.
- A behavioral queue-gate counterfactual proves removing/bypassing the review
  result prevents authorization; string/manifest presence alone is not enough.
- The two slice-owned baseline failures become green without weakening their
  command-owner assertions.
- Planner, reviewer, binding, aggregate-review, and queue vocabularies implement
  the exact fail-closed mapping above; no alias authorizes queue mutation.
- Same-commit validation produces reusable receipts with explicit invalidation
  conditions rather than forcing every later reviewer to rerun the gate.

### Focused Validation

- `required-green after slice-owned remediation`: the two exact plan-batch
  manifest contract tests listed above.
- `required-green`: focused new/updated tests covering exact draft binding,
  evidence-free `approve` rejection, `revise`/`block` no-queue behavior, and the
  queue-gate bypass counterfactual.
- `required-green`: `python -m pytest -p no:cacheprovider -q tests/test_skill_routing_rule_ownership.py tests/test_batch_runway_create_spec_contract.py`.
- `conditional`: `python -m pytest -p no:cacheprovider -q tests/test_codex_features_manifest.py`
  only if the slice deliberately fixes or quarantines the unrelated known-red
  test; otherwise run the focused plan-batch tests and preserve the unrelated
  failure explicitly.
- `required-green`: Ruff on touched Python and `git diff --check`.
- `conditional`: `./install.sh --feature plan-batch --dry-run` when the manifest
  version changes; do not install during worker execution.
- `implementation-created`: the two-packet batched smoke under `Slice 1 Cost
  Gate`, using one planner and one different reviewer invocation. It must leave
  the negative packet unauthorized and the positive packet alone queued.
- `progression-gate`: record `smoke-cost-receipt.md`, obtain a clean separate
  cost-gate review, report the measured/extrapolated cost to the user, and stop.
  Slice 2 remains unauthorized until explicit user approval.

### Worker Brief

The `runway_worker` is the required coding subagent. Implement only Slice 1 on
master. Read the exact dispatch/runway and inspect the current installed
plan-batch route. Do not spawn or delegate. Keep the new review contract within
the installed `plan-batch` feature, use a separate generic read-only review
handoff rather than a new registered role, and do not touch candidate paths.
Return the exact task-scoped diff and focused validation; coordinator owns
review, commits, ledger, and installation.

### Review Brief

Review the exact Slice 1 commit/diff and independently trace the public master
route from `skills/plan-batch` through create-spec, review, and Architecture
Program Runway queue mutation. Attempt evidence-free `approve`, changed-
draft reuse, and review-gate bypass. Verify no candidate machinery, new agent
role, or deterministic semantic authority appeared. Verify the canonical
verdict mapping and exact-commit receipt schema. Echo the exact diff basis and
keep cross-checkout fields null. This implementation review is not the later
cost-gate reviewer.

### Slice Stop Conditions

Stop if the actual master planner route remains unchanged; if a disconnected
reference/test is the only change; if the queue owner can proceed without the
exact planner=`plan` + reviewer=`approve` + binding=`valid` conjunction; if the
reviewer can self-author evidence; if Planning State gains semantic authority;
if the two-packet smoke exceeds one planner and one
reviewer invocation except a recorded transport retry; if its metrics or
independent cost-gate review are missing; if Slice 2 would proceed without the
user's measured-cost approval; or if a new agent role/script/schema/state
family is required.

## Slice 2: Applicable Semantic Assurance And Master Closeout Provenance

### Scope

Use Slice 1's accepted gate to strengthen the existing master create-spec and
planning-review semantics for applicable replacement, migration, decisive-
primitive, intermediate-usefulness, and high-multiplier plans. Add bounded
scenario evidence for all nine negative cases and the valid small-plan control.
Align only directly affected documentation/manifest/changelog surfaces, then
produce final master-install and accepted-closeout proof.

### Allowed Files Or Areas

- Slice 1's accepted master planner/review surfaces
- `skills/batch-runway/references/create-spec.md`
- focused master-route scenario fixtures/tests/evidence owned by existing test
  areas; no candidate scenario adapter or permanent live-model service
- `tests/test_semantic_slice_shape_contract.py`
- `tests/test_batch_runway_create_spec_contract.py`
- `tests/test_skill_routing_rule_ownership.py`
- focused new planning-review contract tests
- `docs/workflow-guide.md`, `docs/skill-routing-contract.md`, `CONTEXT.md`,
  `codex-features.json`, `CHANGELOG.md`, and `README.md` only for direct
  behavior, vocabulary, or installation alignment
- this batch's completed-slice and closeout artifacts through coordinator-owned
  finalization.

### Non-Goals

- No hard-coded CCFG-35 or master topology in reusable rules.
- No mandatory migration ceremony for ordinary plans.
- No universal numeric thresholds, mandatory telemetry, or permanent live-
  model evaluation infrastructure.
- No per-scenario semantic invocation or expansion beyond the reviewed
  four-call batch-local semantic budget.
- No CCFG-26/test cleanup, work-batch wording repair, or candidate changes.

### Scenario Acceptance Matrix

| Scenario | Class | Required actual-master disposition |
|---|---|---|
| replacement owner leaves old fallback reachable | negative | planner corrects/blocks; independent reviewer rejects unsupported approval |
| capabilities named but exact callers omitted | negative | planner corrects/blocks; reviewer reconstructs callers and requires revision |
| success moves but failure remains with displaced owner | negative | planner blocks independent usability; reviewer rejects |
| widest slice justified only by common rollback | negative | planner supplies smaller usable alternative or evidence; reviewer revises otherwise |
| no old-owner behavioral counterfactual | negative | planner adds required-green counterfactual or blocks; reviewer rejects presence-only evidence |
| decisive primitive asserted without proof | negative | planner requires production evidence or bounded proof; reviewer rejects assertion-only feasibility |
| intermediate producer has no current consumer | negative | planner merges/reorders/names consumer; reviewer rejects claimed usefulness |
| two durable writes called one atomic operation without ordering/recovery | negative | planner requires partial-state/recovery/fault evidence; reviewer rejects compound-atomicity claim |
| reviewer accepts planner self-attestation | negative | queue remains unauthorized; result is revise/blocked |
| valid small non-migration plan | positive | compact plan and evidence-backed approval may queue without migration ceremony |

### Acceptance Criteria

- Applicable planner and reviewer records cover all semantic facts under
  `Planning Evidence Applicability` with concise evidence references.
- Every caller/route is classified once; retained/deferred routes name reason,
  owner, and terminal condition; failure paths cannot fall back to a displaced
  owner.
- Every intermediate has an exact current consumer and complete end-to-end
  behavior; every transfer has a behavioral old-owner counterfactual.
- Decisive unproved primitives require production evidence or a bounded
  disposable proof; compound writes cover ordering, partial state, recovery,
  and fault evidence.
- The widest slice records its best smaller usable alternative; common rollback
  alone is insufficient.
- Cost multipliers use available evidence or explicit unknowns without hard
  thresholds.
- The exact Slice 1 smoke receipt, clean cost-gate review, and explicit user
  approval authorize this slice; their model/effort availability, retries,
  bytes, duration, tokens when exposed, and final estimate remain traceable.
- All nine negative scenarios reach the intended correct/block/revise outcome,
  and the positive plan remains compact and queueable.
- Scenario evidence exercises the actual installed master planning/review route
  and includes a bypass/removal counterfactual. It is not solely a string,
  manifest, schema, or fixture-self-attestation test.
- Mechanical checks remain limited to exact binding, non-empty references,
  identifiers, and alignment; semantic judgments remain planner/reviewer-owned.
- Generic rules remain project-neutral and Graphify-independent.
- Stable installation and final review satisfy the proof below; candidate
  paths remain unchanged.

### Focused Validation

- `required-green`: all Slice 1 gates, the exact smoke cost receipt, clean
  cost-gate review, and recorded explicit user approval of the estimate.
- `required-green`: focused master-route scenario tests/evidence for the ten-row
  matrix and the review-gate bypass counterfactual.
- `required-green`: `python -m pytest -p no:cacheprovider -q tests/test_semantic_slice_shape_contract.py tests/test_batch_runway_create_spec_contract.py tests/test_skill_routing_rule_ownership.py`.
- `required-green`: focused plan-batch manifest contract tests.
- `required-green`: Ruff on touched Python and `git diff --check`.
- `conditional`: full `tests/test_codex_features_manifest.py` only if unrelated
  baseline is repaired under separately authorized scope; otherwise retain its
  exact unrelated known red and run all CCFG-35-relevant cases.
- `required-green`: `./install.sh --feature plan-batch --dry-run` after manifest
  changes and before coordinator installation.
- `required-green`: all ten isolated packets through `Batched Actual-Master
  Behavioral Proof Lane` using one planner and one different reviewer
  invocation, followed by ten separate queue decisions. Unavailable invocation
  after one transport retry is a stop, not a skipped or xfailed gate.

### Worker Brief

The `runway_worker` is the required coding subagent. Implement only Slice 2 on
top of accepted Slice 1. Exercise the master skill/support route and keep
semantic judgments in planner/reviewer instructions, with only mechanical
binding in deterministic checks. Do not spawn or delegate, touch candidate
paths, add a registered role, or solve unrelated known-red tests. Coordinator
owns final installation, independent review, commits, and closeout.

### Review Brief

Review the exact Slice 2 commit/diff. Independently reconstruct the ten scenario
facts and attempt to falsify each expected disposition, including removal or
bypass of the new gate. Verify ordinary small work stays compact, deterministic
checks do not claim semantic truth, the final lane is two batched calls rather
than twenty calls, exact-commit receipts are reused unless invalidated, and
every changed surface participates in the actual master route. Echo the exact
diff basis and keep cross-checkout fields null.

### Slice Stop Conditions

Stop if scenario results are manufactured by fixtures; if a string/schema test
is the only behavior proof; if applicability becomes universal; if the review
cannot falsify planner self-attestation; if the widest-slice alternative is
omitted; if the final lane exceeds one planner and one reviewer call except a
recorded transport retry; if a same-commit gate is rerun without recorded
invalidation; or if master provenance is deferred to candidate-home evidence.

## Final Validation

After both accepted slice commits, from the canonical master checkout:

1. Inventory every focused validation receipt from both slices. Reuse a green
   receipt when its exact commit and all receipt-key inputs still match. Rerun
   only missing, malformed, or explicitly invalidated gates, and record the
   invalidating fact.
2. Ensure the reusable receipt set covers all CCFG-35-relevant cases in
   `tests/test_codex_features_manifest.py`, preserving the exact unrelated
   `work-batch` known red if still present.
3. Run broader affected planning-skill tests only when their receipt is absent
   or a material affected input changed; any new CCFG-35-related failure blocks
   acceptance.
4. Run or reuse exact-commit receipts for Ruff on touched Python and `git diff
   --check`.
5. Execute the final ten-packet lane with one planner and one different reviewer
   invocation, then apply ten separate queue decisions. Persist its actual cost
   fields and compare them with the Slice 1 estimate; unexplained material
   divergence requires correction or block, not extra semantic reruns.
6. Run `./install.sh --feature plan-batch --dry-run` and inspect dependency-
   expanded actions before any stable-home write.
7. With coordinator authority, install the changed `plan-batch` feature into
   `/home/alacasse/.codex` when needed to reconcile a changed manifest version;
   do not install any candidate-home feature.
8. Enumerate every changed installed-route file in the accepted master range,
   including public `plan-batch`, Architecture Program Runway, Batch Runway
   create-spec, and any new plan-batch reference. For each owning installed
   feature, run `python scripts/codex_owner.py` and `readlink -f`. Hash the
   installed file and the exact accepted commit blob from `git show
   <accepted-commit>:<repo-path>` and require equality. Worktree-only `cmp` or
   hash equality is insufficient.
9. Run `./install.sh --status` plus the relevant feature dry-runs; reconcile
   directly changed manifest versions and distinguish unrelated pre-existing
   version lag.
10. Verify `git branch --show-current` is `master`; record the exact accepted
   commits and prove every changed planner/review surface is present in the
   accepted master commit range. Reject uncommitted-only content as proof.
11. Verify the candidate checkout and candidate Codex home received no CCFG-35
   writes or installs.
12. Run `test-quality-review` on changed behavior tests, consuming valid
    same-commit test receipts instead of rerunning unchanged gates.
13. Delegate one final independent exact-range review with the required proof
    below. Do not accept a generic clean diff verdict that omits installed-master
    provenance, the measured batched-lane comparison, or receipt-reuse audit.

## Required Accepted-Closeout Proof

The final independent reviewer and closeout must reconstruct the semantic and
provenance conclusions independently, using fresh reads plus reusable
exact-commit validation receipts where their keys remain valid:

- exact accepted master commit range and `master` branch identity;
- exact public route: installed `plan-batch` -> repo public owner -> Planning
  State -> Architecture Program Runway dispatch/queue -> Batch Runway
  create-spec -> independent planning review -> queue decision;
- which accepted changes alter that route and why disconnected test/docs-only
  changes are insufficient;
- ten-row behavioral results from one planner batch and one independent
  reviewer batch, ten separately applied queue decisions, evidence references,
  canonical verdict mappings, and bypass/removal counterfactual;
- exact smoke and final semantic-call counts, wall durations, retries,
  input/output bytes, output digests, model/effort/token availability, projected
  versus actual cost, the clean cost-gate review, and the explicit user approval
  that released Slice 2;
- the validation receipt inventory, every reuse, every invalidation and rerun,
  and proof that no unchanged expensive gate was repeated merely because a new
  reviewer consumed it;
- per-file accepted-commit blob hashes plus installed-content hashes, exact
  `codex_owner.py`, `readlink -f`, installer dry-run/status, and manifest-version
  facts for every changed installed route feature; mutable worktree comparison
  alone is invalid;
- proof candidate checkout/home were not implementation or installation targets;
- test-quality review and final exact-range review results; and
- same-batch closeout path/state with CCFG-35 reconciled and no successor.

The independent reviewer must reconstruct these facts itself. Planner, worker,
or closeout self-attestation; candidate-home evidence; manifest presence alone;
or an unbound clean verdict is a blocker.

## Final Acceptance

- The actual installed master planner route changed and is proven by exact
  source, commit, owner, link, content, and behavioral evidence.
- Evidence-free reviewer=`approve` cannot authorize queue mutation.
- Applicable semantic omissions correct or block for the intended reason.
- The valid ordinary small-plan control remains compact and queueable.
- The final ten-packet lane used exactly one planner and one different reviewer
  invocation in the normal path, with ten isolated queue results and measured
  cost reconciled against the accepted Slice 1 estimate.
- Every queue result follows the canonical fail-closed verdict mapping.
- Exact-commit receipts were reused until a recorded material invalidation.
- Exact draft binding and Planning State structural authority remain intact.
- No new agent role, top-level schema/state family, queue owner, candidate port,
  deterministic semantic authority, or project-specific reusable rule exists.
- Candidate checkout/home remain unchanged by CCFG-35.
- All CCFG-35 gates are green; unrelated known-red evidence is explicit.
- CCFG-35 alone is closed and no successor is selected.

## Batch Stop Conditions

Stop if master identity or installed-link ownership is missing or ambiguous; if
candidate-only paths enter implementation; if any handoff uses strict cross-
checkout context; if reviewer=`approve` can remain evidence-free; if changed
drafts reuse an old verdict; if queue mutation can bypass the independent review; if
scenario evidence is only wording/schema/fixture self-attestation; if semantic
judgment moves into Planning State or a deterministic helper; if a new role,
schema/state family, queue owner, compatibility wrapper, universal threshold,
mandatory product telemetry, per-scenario live lane, or permanent live-model
service is required; if the four-call semantic budget is exceeded except a
recorded transport retry; if Slice 2 lacks measured-cost approval; if verdict
mapping is ambiguous; if unchanged validation is rerun without invalidation;
if reusable rules gain project-specific facts or Graphify authority; if
unrelated known-red tests are silently repaired; or if any other finding is
selected or changed.

## Closeout Boundary

After implementation, validation, stable installation evidence, test-quality
review, final independent exact-range review, accepted commits, and required
closeout proof are complete, reconcile CCFG-35 only. Clear its selected/queued/
active state, point latest closeout at this replacement batch, mark the finding
closed only from accepted evidence, and stop with no successor selected.
