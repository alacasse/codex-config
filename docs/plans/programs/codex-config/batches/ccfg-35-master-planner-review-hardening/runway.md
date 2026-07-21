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
  -> only an exact evidence-backed clean result permits queue mutation
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
- Approval gate: a later explicit user `work-batch` while this exact runway is
  the sole queue entry, master identity is unchanged except for accepted batch
  commits, the previous slice is accepted, and no stop condition is active.

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
- No universal thresholds, mandatory telemetry, routine live-model evaluation
  in ordinary `plan-batch`, or permanent scenario service. This batch's bounded
  disposable final acceptance lane is explicitly required and is not reusable
  runtime infrastructure.
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

## Disposable Actual-Master Behavioral Proof Lane

Final acceptance requires bounded live planner and reviewer invocations because
master's semantic planner is instruction-driven Markdown and no executable
semantic planner exists. Static wording tests, candidate adapters, deterministic
semantic classifiers, and fixtures that state their own conclusions cannot
substitute for this lane. If the required fresh invocations are unavailable,
stop before final acceptance and closeout.

For each of the ten scenarios:

1. Create one fresh temporary directory with `mktemp -d`. Under it, create a
   minimal isolated Planning Artifact Layout v1 root containing only the
   scenario's `CURRENT.md`, program `CURRENT.md`, `LEDGER.md`, source finding,
   pinned repository-evidence packet, and empty batch target. Do not point any
   fixture at canonical planning state.
2. Record SHA-256 values for every scenario input and the exact accepted master
   planner/support files used by the invocation.
3. Launch one fresh bounded planner subagent with the installed
   `/home/alacasse/.codex/skills/plan-batch/SKILL.md`, its accepted master
   support references, the isolated planning root, and permission to write only
   inside that scenario root. Require the coarse disposition `plan`, `correct`,
   or `block`, exact draft hashes when produced, and cited evidence identifiers.
4. Launch a different fresh read-only reviewer subagent with the accepted
   plan-batch planning-review handoff/result reference produced by Slice 1, the
   pinned inputs, and any exact draft. Require `approve`, `revise`, or `block`,
   independently reconstructed facts/evidence, and exact draft hashes. It must
   not reuse planner prose as evidence.
5. Apply the accepted master Architecture Program Runway queue decision only to
   that isolated root. A negative scenario must record correct/block or
   revise/block and `queue_outcome: not_queued`. The positive control must
   record a compact plan, evidence-backed approval, and exactly one isolated
   queued runway.
6. For the review-gate counterfactual, present an evidence-free clean result,
   a changed draft after review, and a missing review result to the accepted
   queue boundary. Each must record `queue_outcome: not_queued` without editing
   the installed source.
7. Record a compact durable table in this batch's closeout with scenario ID,
   input hash, planner disposition, reviewer disposition, dispatch/runway
   hashes, evidence identifiers, queue outcome, and temporary root deletion
   result. Do not copy transcripts or generated prose into planning state.

The coordinator owns fixture construction, isolation, hash capture, queue-
outcome verification, and summary acceptance. The planner and reviewer remain
separate. Temporary scenario roots are proof environments, never canonical
state, reusable caches, or candidate-home inputs.

## Slice Shape Rationale

- `1 -> 2`: Slice 1 creates a complete exact-review/queue-authorization gate
  already consumed by the public master planning route. Slice 2 extends the
  semantic evidence that gate consumes and adds broader falsification and
  installed-master closeout proof. This is a valid producer/consumer boundary;
  either commit can be reviewed and rolled back independently.
- Slice 1 is useful without Slice 2 because evidence-free clean review can no
  longer queue any plan.
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
- A clean result records reconstructed facts plus non-empty evidence references;
  bare semantic passes or copied planner claims are invalid.
- Changed drafts invalidate the result; correction/blocked outcomes leave
  CCFG-35 unqueued and return control to the public planner.
- Architecture Program Runway queues only after consuming the exact accepted
  clean result; it does not absorb semantic review ownership.
- Planning State remains structural and create-spec remains semantic draft
  owner.
- A behavioral queue-gate counterfactual proves removing/bypassing the review
  result prevents authorization; string/manifest presence alone is not enough.
- The two slice-owned baseline failures become green without weakening their
  command-owner assertions.

### Focused Validation

- `required-green after slice-owned remediation`: the two exact plan-batch
  manifest contract tests listed above.
- `required-green`: focused new/updated tests covering exact draft binding,
  evidence-free clean rejection, correction/blocked no-queue behavior, and the
  queue-gate bypass counterfactual.
- `required-green`: `python -m pytest -p no:cacheprovider -q tests/test_skill_routing_rule_ownership.py tests/test_batch_runway_create_spec_contract.py`.
- `conditional`: `python -m pytest -p no:cacheprovider -q tests/test_codex_features_manifest.py`
  only if the slice deliberately fixes or quarantines the unrelated known-red
  test; otherwise run the focused plan-batch tests and preserve the unrelated
  failure explicitly.
- `required-green`: Ruff on touched Python and `git diff --check`.
- `conditional`: `./install.sh --feature plan-batch --dry-run` when the manifest
  version changes; do not install during worker execution.
- `implementation-created`: one isolated positive smoke scenario using the
  disposable proof lane after Slice 1 creates the review handoff; this becomes
  required-green before Slice 2 and must show exactly one isolated queue entry.

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
Program Runway queue mutation. Attempt evidence-free clean approval, changed-
draft reuse, and review-gate bypass. Verify no candidate machinery, new agent
role, or deterministic semantic authority appeared. Echo the exact diff basis
and keep cross-checkout fields null.

### Slice Stop Conditions

Stop if the actual master planner route remains unchanged; if a disconnected
reference/test is the only change; if the queue owner can proceed without the
exact clean review; if the reviewer can self-author evidence; if Planning State
gains semantic authority; or if a new agent role/script/schema/state family is
required.

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

- `required-green`: all Slice 1 gates.
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
- `required-green`: all ten bounded live scenarios through `Disposable Actual-
  Master Behavioral Proof Lane`; unavailable planner/reviewer invocation is a
  stop, not a skipped or xfailed gate.

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
checks do not claim semantic truth, and every changed surface participates in
the actual master route. Echo the exact diff basis and keep cross-checkout
fields null.

### Slice Stop Conditions

Stop if scenario results are manufactured by fixtures; if a string/schema test
is the only behavior proof; if applicability becomes universal; if the review
cannot falsify planner self-attestation; if the widest-slice alternative is
omitted; or if master provenance is deferred to candidate-home evidence.

## Final Validation

After both accepted slice commits, from the canonical master checkout:

1. Re-run every required-green focused command from both slices.
2. Run all CCFG-35-relevant cases in `tests/test_codex_features_manifest.py` and
   preserve the exact unrelated `work-batch` known red if still present.
3. Run broader affected planning-skill tests when practical; any new or CCFG-35-
   related failure blocks acceptance.
4. Run Ruff on all touched Python and `git diff --check`.
5. Run `./install.sh --feature plan-batch --dry-run` and inspect dependency-
   expanded actions before any stable-home write.
6. With coordinator authority, install the changed `plan-batch` feature into
   `/home/alacasse/.codex` when needed to reconcile a changed manifest version;
   do not install any candidate-home feature.
7. Enumerate every changed installed-route file in the accepted master range,
   including public `plan-batch`, Architecture Program Runway, Batch Runway
   create-spec, and any new plan-batch reference. For each owning installed
   feature, run `python scripts/codex_owner.py` and `readlink -f`. Hash the
   installed file and the exact accepted commit blob from `git show
   <accepted-commit>:<repo-path>` and require equality. Worktree-only `cmp` or
   hash equality is insufficient.
8. Run `./install.sh --status` plus the relevant feature dry-runs; reconcile
   directly changed manifest versions and distinguish unrelated pre-existing
   version lag.
9. Verify `git branch --show-current` is `master`; record the exact accepted
   commits and prove every changed planner/review surface is present in the
   accepted master commit range. Reject uncommitted-only content as proof.
10. Verify the candidate checkout and candidate Codex home received no CCFG-35
   writes or installs.
11. Run `test-quality-review` on changed behavior tests.
12. Delegate one final independent exact-range review with the required proof
    below. Do not accept a generic clean diff verdict that omits installed-master
    provenance.

## Required Accepted-Closeout Proof

The final independent reviewer and closeout must record, from fresh evidence:

- exact accepted master commit range and `master` branch identity;
- exact public route: installed `plan-batch` -> repo public owner -> Planning
  State -> Architecture Program Runway dispatch/queue -> Batch Runway
  create-spec -> independent planning review -> queue decision;
- which accepted changes alter that route and why disconnected test/docs-only
  changes are insufficient;
- ten-row behavioral results, evidence references, and bypass/removal
  counterfactual;
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
- Evidence-free clean planning review cannot authorize queue mutation.
- Applicable semantic omissions correct or block for the intended reason.
- The valid ordinary small-plan control remains compact and queueable.
- Exact draft binding and Planning State structural authority remain intact.
- No new agent role, top-level schema/state family, queue owner, candidate port,
  deterministic semantic authority, or project-specific reusable rule exists.
- Candidate checkout/home remain unchanged by CCFG-35.
- All CCFG-35 gates are green; unrelated known-red evidence is explicit.
- CCFG-35 alone is closed and no successor is selected.

## Batch Stop Conditions

Stop if master identity or installed-link ownership is missing or ambiguous; if
candidate-only paths enter implementation; if any handoff uses strict cross-
checkout context; if a clean review can remain evidence-free; if changed drafts
reuse an old verdict; if queue mutation can bypass the independent review; if
scenario evidence is only wording/schema/fixture self-attestation; if semantic
judgment moves into Planning State or a deterministic helper; if a new role,
schema/state family, queue owner, compatibility wrapper, universal threshold,
mandatory telemetry, or permanent live-model service is required; if reusable
rules gain project-specific facts or Graphify authority; if unrelated known-red
tests are silently repaired; or if any other finding is selected or changed.

## Closeout Boundary

After implementation, validation, stable installation evidence, test-quality
review, final independent exact-range review, accepted commits, and required
closeout proof are complete, reconcile CCFG-35 only. Clear its selected/queued/
active state, point latest closeout at this replacement batch, mark the finding
closed only from accepted evidence, and stop with no successor selected.
