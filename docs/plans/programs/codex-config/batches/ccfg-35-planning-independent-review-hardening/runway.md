# CCFG-35 Planning And Independent Review Hardening Runway

## Purpose

Implement the CCFG-35 reusable planning-system hardening in the candidate
generation. A clean independent planning review must reconstruct applicable
semantic facts from pinned evidence, and the deterministic pre-queue gate must
reject missing or malformed evidence bindings without claiming to decide
semantic truth.

## Status

- Batch: `ccfg-35-planning-independent-review-hardening`
- Finding: `CCFG-35`
- State after exact clean planning review: `queued`
- Implementation: not started
- Density: `full-runway`
- Batch kind: `mixed-risk`
- Validation profile: `project-harness-production`
- Slice-shape policy: configured `vertical`; no override is used.
- Successor selection: forbidden.

## Planning Snapshot

This immutable snapshot was validated at plan time with the installed helper at
`/home/alacasse/.codex/scripts/cross_checkout_context.py`. It is historical
planning evidence, not a live execution lease. Do not rewrite it to chase a
later `HEAD` or to embed the commit containing this runway.

Canonical planning root:

```text
/home/alacasse/projects/codex-config/docs/plans
```

Complete `cross-checkout-context/v1` payload:

```json
{
  "execution_context": {
    "canonical_planning_commit_before": "f09e2eca6767ac11f6b5d05fd66933001667d0ea",
    "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
    "canonical_state_mutation_allowed": true,
    "codex_home": "/home/alacasse/.codex",
    "generation_role": "stable",
    "implementation_commit_before": "5c5ec9d52dd9033daa45f3a200031c152363b62c",
    "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
    "toolchain_commit": "f09e2eca6767ac11f6b5d05fd66933001667d0ea",
    "toolchain_source_root": "/home/alacasse/projects/codex-config"
  },
  "interface": "cross-checkout-context/v1"
}
```

Before the first implementation or review handoff, `work-batch` must confirm
this same selected scope through Planning State and call the installed helper's
ready/blocked preflight. Every later handoff requires a fresh strict live lease
and separately validated write scope. Stable and candidate do not import,
invoke, synchronize with, or share runtime execution state.

## Current Baseline

At candidate commit `5c5ec9d52dd9033daa45f3a200031c152363b62c`:

- `skills/plan-batch/SKILL.md` owns one-finding selection, direct planner and
  reviewer invocation, exact review, and DEC-038 queue mutation.
- `agents/batch_planner.toml` returns `batch-plan-draft/v1` with scope,
  proportionality, semantic slice rationales, and exact-risk migration evidence.
- `agents/batch_plan_reviewer.toml` returns `batch-plan-review/v1`, but its
  semantic checks are only coarse `pass | fail` values.
- `scripts/plan_batch.py::_validate_review_evidence` binds exact packet content,
  source digests, diagnostics, policy, approvals, draft, dispatch, and direct
  invocation lineage.
- `scripts/plan_batch.py::_validate_review` validates four exact review-basis
  hashes and requires every coarse check to pass, but cannot require the
  reconstructed fact or evidence references behind a clean semantic conclusion.
- DEC-038 writes only after `_prepare_plan` validates state, roles, draft,
  quality, evidence packet, review result, and transaction contracts.
- Existing migration evidence identifies owners, migrated callers, a claimed
  independently usable state, rollback, residue, and coexistence rows, but it
  does not prove exact active entrypoints, complete caller disposition, reachable
  failure owners, exact current consumers, a behavioral counterfactual, decisive
  feasibility, or material cost multipliers.
- Planning State owns structural currentness, paths, registration, lineage, and
  queue state. It must not absorb semantic review judgment.
- Candidate routing already makes Batch Runway execution-only and compatibility
  `create-spec` observation-only. Do not restore the stable finding's historical
  `create-spec.md` seam in the candidate.

## Retained Route And Failure-Path Matrix

This is the plan-time reconstruction at the pinned candidate basis. Slice 2 must
preserve or strengthen every disposition and must block if bounded inspection
finds an unclassified normal caller or reachable outcome.

| Entrypoint or caller | Current / future owner | Disposition and reason | Forbidden fallback | Observable failure result and exact consumer | Removal owner and terminal condition |
|---|---|---|---|---|---|
| Explicit human/agent `plan-batch` invocation through the installed skill | public `plan-batch` / public `plan-batch` | Intentionally retained as the sole human-facing planning command | APR or Batch Runway selection, draft, review, or queue ownership | One blocked command result with `write_status: not_written`; consumed by the invoking user/agent | Permanent command surface; no removal planned by CCFG-35 |
| Architecture runner serialized `select-dispatch` phase | public `plan-batch` / public `plan-batch` | Intentionally retained compatibility caller; it invokes public `plan-batch` once for the complete planning result | Phase-local selection, APR planning, or a second queue transaction | Blocked/stopped plan-batch result; consumed by the architecture-runner phase transition and run summary | CCFG-27 owns migrate/remove decision; physical retention ends no later than CCFG-29 final integration |
| Architecture runner serialized `create-spec` phase | public `plan-batch` result / public `plan-batch` result | Intentionally retained observation-only compatibility route so the serialized phase graph can advance | Batch Runway create-spec, a replacement draft, repeat review, or queue mutation | Missing/invalid completed planning result blocks phase advancement; consumed by the architecture-runner transition/run summary | CCFG-27 owns migrate/remove decision; physical retention ends no later than CCFG-29 final integration |
| Direct `batch_planner` invocation by public `plan-batch` | `batch_planner` draft author / same, conditioned on strengthened applicable evidence duties | Conditioned on the evidence-bearing draft contract; retained because planning authorship is separate from review | Planner approval, reviewer evidence selection, queue mutation, or alternate-finding selection | `status: blocked` or malformed draft causes plan-batch to stop without writes; consumed by public `plan-batch` | Permanent role unless a later accepted design replaces it; no CCFG-35 removal |
| Direct `batch_plan_reviewer` invocation by public `plan-batch` | independent planning reviewer / same, with reconstructed facts and evidence refs | Conditioned on the strengthened clean-result contract; retained as the semantic quality gate | Planner self-attestation, planner-selected verdict, implementation-time `runway_reviewer`, or evidence-free clean passes | `correction_required` returns to the same planner/finding/basis; `blocked` stops; malformed/evidence-free clean output is rejected; consumed by public `plan-batch` | Permanent role unless a later accepted design replaces it; no CCFG-35 removal |
| Installed `scripts/plan_batch.py` deterministic entrypoint | mechanical pre-queue validator and DEC-038 caller / same | Conditioned on new shape/reference/alignment checks; retained as the only mechanical apply boundary | Semantic completeness judgment, role invocation, direct store bypass, or a second queue path | `plan-batch-result/v1` blocked with `write_status: not_written` and a bounded next action; consumed by public `plan-batch` | Permanent mechanical boundary; no CCFG-35 removal |
| `planning_contract.simulate_selection_transaction` called by `scripts/plan_batch.py` | apply-only DEC-038 store / same | Intentionally retained; it applies an already reviewed decision and owns replay-safe transaction faults | Direct calls from planner/reviewer, semantic review, or alternate lifecycle authority | `PlanningStoreError` becomes a blocked same-transaction `resume`; consumed by `scripts/plan_batch.py` and then public `plan-batch` | Permanent apply mechanism unless separately redesigned; no CCFG-35 removal |
| Planning State `current` and `validate` diagnostics | Planning State structural authority / same | Intentionally retained for paths, pointers, registration, lineage, currentness, and queue state | Semantic completeness, usefulness, feasibility, slice preference, or cost judgment | Fatal/stale/ambiguous diagnostic stops before roles and writes; consumed by public `plan-batch` | Permanent structural owner; no CCFG-35 removal |

Reachable transaction interruption does not fall back to a legacy owner: only
the same immutable DEC-038 transaction may resume. Reviewer correction does not
reselect work: it returns only to the same planner, finding, and evidence basis.
Any discovered route that violates these statements blocks the slice and becomes
explicit follow-up evidence rather than being silently absorbed.

## Planning Evidence And Applicability

The implementation must define a machine-readable applicability trigger in the
existing draft/review boundary for substitutive work such as ownership transfer,
migration, or replacement, and for a plan that depends on an unproved decisive
primitive. Do not infer applicability only from prose. Reuse an existing result,
draft, runway, review, or transaction boundary; do not create a new top-level
schema family or persistent state store.

Applicable semantic records must support:

- observed problem and minimum viable change;
- current/future semantic owner and exact entrypoints;
- every normal caller and its replaced, conditioned, intentionally retained,
  removed, or deferred disposition;
- retained-route reason, removal owner, and terminal condition;
- forbidden fallbacks;
- reachable normal and failure outcome owners, observable result, and exact
  current consumer;
- current production consumer and end-to-end behavior for each intermediate;
- required-green ownership counterfactual references;
- decisive feasibility assumptions and production evidence or bounded
  disposable proof;
- widest-slice smaller usable alternative and rejection reason; and
- available or explicitly unknown execution/validation cost multipliers.

For a clean review, each applicable conclusion must state the independently
reconstructed fact and cite non-empty pinned evidence identifiers or paths. A
bare `pass` cannot authorize queue mutation. Mechanical validation may check
shape, non-empty/unique identifiers, reference resolution, exact binding, and
cross-record alignment; it must not claim that discovery is complete, an
intermediate is useful, proof is persuasive, a slice is preferable, or cost is
acceptable.

## Proportionality And Cost Record

- Observed failure: an exact, structurally valid planning packet can queue when
  the reviewer echoes planner conclusions as bare passes.
- Minimum viable change: make the clean-review result evidence-bearing and
  mechanically reject evidence-free clean results before DEC-038.
- Additions beyond the minimum:
  - substitutive-work assurance prevents partial owner transfer, hidden caller
    fallback, legacy-owned failure paths, and consumerless intermediates;
  - conditional feasibility and cost assurance prevents assertion-only
    architecture, compound atomicity claims, rollback-only oversized slices,
    and avoidable repeated expensive gates.
- Rejected simpler alternative: prompt-only wording without a result consumer
  or deterministic gate; it remains self-attested and cannot fail closed.
- Rejected broader alternative: a new review schema family, state store, agent
  role, live-model eval system, or Planning State semantic validator; each adds
  authority or persistence without being required by the defect.
- Likely production surfaces: the public plan-batch skill, two planning role
  contracts, the deterministic plan-batch script, focused scenario adapters,
  and directly associated docs/manifest metadata.
- Measured candidate baseline:
  - focused review/evidence/migration/proportionality plan-batch tests: 33 passed
    in about 14.7 seconds;
  - full `tests/test_plan_batch.py`: 116 passed in about 51.4 seconds;
  - focused planning behavioral scenarios: 3 passed in about 42.0 seconds;
  - full behavioral scenario file: about 74 seconds from current evidence;
  - planning-contract schema tests: 41 passed in about 1.6 seconds;
  - focused planning agent tests: 2 passed in about 0.02 seconds;
  - focused plan-batch manifest tests: 2 passed in about 0.08 seconds;
  - catalog structural validation: 82 scenarios in about 0.26 seconds.
- Known unrelated baseline: a broad five-file test command produced 170 passes
  and one existing failure in
  `test_work_batch_reconciles_same_batch_closeout` after about 128 seconds. The
  failure is outside CCFG-35 and must not be fixed or promoted to a gate by this
  batch; any new or changed failure remains blocking.
- Planner/reviewer model runtime and token cost: unknown; record as unknown, do
  not estimate or make live-model evaluation mandatory.
- Validation cadence: run the roughly 15-second focused gate per slice; reserve
  the full 52-second owner file, full behavioral file, installation, and exact
  acceptance for final range validation.

## Batch Non-Goals

- No implementation or closeout changes outside planning and independent review.
- No new planning owner, agent role, top-level schema family, transaction,
  persistent draft/review store, retry token, compatibility wrapper, or queue
  path.
- No semantic-quality responsibility in Planning State.
- No `runway_reviewer` repurposing.
- No restoration of APR or Batch Runway planning authority.
- No mandatory migration ceremony for a valid small ordinary plan.
- No universal numeric file, line, slice, token, or runtime threshold.
- No mandatory telemetry, fresh coordinator process, or live-model evaluation.
- No project-specific path, ledger identity, branch topology, temporary policy,
  or Graphify product requirement in generic reusable instructions.
- No stable Codex-home mutation and no successor selection.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2; registered agent TOMLs
own exact worker and reviewer result schemas.
Use Batch Runway Compact Report Contract v1 for coordinator receipts.
Use Batch Runway Compact Convergence Assessment v1.
Use Batch Runway Orchestration Anomaly Log v1.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.
Use the strict cross-checkout consumer contract for every delegated handoff.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/validation-profiles/project-harness-production.md`

Overrides:

- Implementation edits and commits occur only in the candidate checkout.
- Canonical planning/ledger reconciliation occurs only in the stable checkout.
- Do not run candidate installation or the full command-owner acceptance harness
  per slice; they are final-range gates.
- The known unrelated `work-batch` manifest assertion is diagnostic baseline,
  not CCFG-35 remediation scope.

## Approval Contract

All three slices are `contract-narrowing` because they reject planning results
that the current interface can represent as clean. The user is the approval
authority. A later explicit `work-batch` invocation against this exact queued
runway supplies execution approval, provided Planning State remains current,
strict preflight is ready, and previous slice evidence is green. Approval does
not broaden the allowed file areas or authorize stable-home installation.

## Execution Ledger

| Slice | Shape | Risk | Status | Current consumer | Commit |
|---|---|---|---|---|---|
| 1. Evidence-backed clean-review gate | vertical | contract-narrowing | Pending | `scripts/plan_batch.py::_validate_review` before DEC-038 | Pending |
| 2. Substitutive ownership and independent-usability assurance | vertical | contract-narrowing | Pending | public `plan-batch` planner/reviewer pipeline and Slice 1 review result boundary | Pending |
| 3. Conditional feasibility and cost proportionality | vertical | contract-narrowing | Pending | public `plan-batch` proportionality/reviewer pipeline and prior evidence boundary | Pending |

## Slice Shape Rationale

- Slice 1 produces a complete evidence-bearing independent-review result and
  fail-closed deterministic consumer. It is independently useful because an
  evidence-free clean verdict can no longer queue, while a small ordinary plan
  remains accepted.
- `1 -> 2`: producer/consumer and contract boundary. Slice 2 consumes Slice 1's
  result/evidence representation to protect substitutive ownership and every
  reachable outcome without adding a parallel review contract.
- `2 -> 3`: risk and validation boundary. Slice 2 closes ownership/caller/
  fallback/failure-path risks; Slice 3 conditionally adds mechanism feasibility
  and high-multiplier cost judgments while keeping ordinary work compact.
- Slice 2 is the widest proposed slice. Its best smaller candidate was to split
  entrypoint/caller/retained-route classification from failure-path ownership,
  exact consumers, and the ownership counterfactual. That smaller state was
  rejected because success-path classification alone would still authorize a
  transfer whose validation, review, stale-evidence, retry, or recovery path can
  return to the displaced owner; it is not independently usable under the
  finding's failure-ownership requirement.
- A one-slice batch was rejected because the resulting diff would combine a new
  result boundary, multiple ownership failure modes, conditional primitive
  proof, cost policy, scenario expansion, and documentation into one review
  surface. A prompt-only preparatory slice was also rejected because it would
  leave no mechanically consumed, independently useful state.

## Slice 1: Evidence-Backed Clean-Review Gate

### Scope

Create one end-to-end review result boundary in which each applicable clean
semantic conclusion records the reconstructed fact and non-empty pinned evidence
references. Make the existing deterministic plan-batch gate reject a clean
result whose required evidence record is absent, empty, stale, mismatched, or
unbound to the exact dispatch/runway/evidence packet.

### Allowed Candidate Areas

- `skills/plan-batch/SKILL.md`
- `agents/batch_plan_reviewer.toml`
- `scripts/plan_batch.py`
- `tests/test_plan_batch.py`
- focused planning-agent, manifest, and behavioral scenario contract tests and
  fixtures required for this exact boundary
- existing planning contract/schema surfaces only if the evidence record must
  persist in an existing artifact; do not create a new schema family.

### Current Consumer And Useful State

- Current consumer: `_validate_review` within `_prepare_plan`, immediately before
  the DEC-038 transaction contracts are accepted.
- End-to-end behavior: public `plan-batch` supplies a pinned packet to the
  independent reviewer; the reviewer returns facts plus evidence references;
  the script checks their mechanical binding; only then may queue mutation run.
- Failure owner: `batch_plan_reviewer` returns correction or blocked for
  semantic insufficiency; public `plan-batch` routes correction or stops;
  `scripts/plan_batch.py` rejects malformed/evidence-free clean output as
  `not_written`.
- Retained authority: the reviewer judges semantic support; the script checks
  only shape and binding; Planning State stays structural.
- Rollback: reverting this slice's candidate commit restores the prior exact
  review result without leaving persistent state or partial installation.

### Acceptance Criteria

- A clean review cannot be encoded only as coarse `pass` statements.
- Every applicable clean conclusion contains a concise reconstructed fact and
  non-empty evidence references resolvable against the exact packet or permitted
  pinned inspection basis.
- Changed dispatch, runway draft, approvals, packet, evidence references, or
  review basis invalidates the clean result before writes.
- Correction and blocked outcomes remain distinct and preserve the same-finding
  correction loop.
- An ordinary small non-migration plan with proportional evidence still queues
  without migration-specific fields.
- The deterministic validator does not claim semantic completeness or
  persuasiveness.
- Behavior-level tests demonstrate both evidence-free refusal and the ordinary
  clean control; prompt/string checks are supporting tests only.

### Focused Validation

- `required-green`: `python -m pytest -p no:cacheprovider -q tests/test_plan_batch.py -k 'review or evidence or roles'`
- `required-green`: focused planning-role contract tests in
  `tests/test_custom_agent_contracts.py`
- `required-green`: focused public plan-batch manifest tests in
  `tests/test_codex_features_manifest.py -k 'plan_batch'`
- `required-green`: `python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios/catalog.yaml`
- `conditional`: planning-contract schema tests only if an existing persisted
  artifact contract changes.
- `required-green`: Ruff on touched Python files and `git diff --check`.
- No per-slice install, full behavioral file, or acceptance harness.

### Worker Brief

The `runway_worker` is the required coding subagent. Implement only Slice 1 in
the candidate checkout using a fresh validated live lease. Do not spawn or wait
on other agents. Keep semantic judgment in the reviewer and mechanical binding
in the script. Do not edit stable planning files, install features, run the full
harness, or touch unrelated `work-batch` behavior.

### Review Brief

Review the exact Slice 1 commit/diff basis. Falsify the gate with an
evidence-free clean result, stale/mismatched references, and a valid small plan.
Verify no semantic judgment moved into deterministic validation and no new
state/schema family or alternate queue path appeared. Echo the exact
`diff_basis` and strict context in the registered reviewer result.

### Slice Stop Conditions

Stop if the result cannot bind exact evidence without a new state family, if
reviewer facts remain bare passes, if the script starts judging semantic truth,
or if candidate changes require stable-home mutation.

## Slice 2: Substitutive Ownership And Independent-Usability Assurance

### Scope

Use Slice 1's evidence result to require applicable planner and reviewer records
for exact entrypoints, caller disposition, retained routes and terminal
conditions, forbidden fallbacks, reachable normal/failure owners and observable
outcomes, exact current consumers, and a required-green behavioral
counterfactual. Add focused scenarios for reachable old fallbacks, omitted
callers, legacy-owned failure paths, and consumerless intermediates.

### Allowed Candidate Areas

- `skills/plan-batch/SKILL.md`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `scripts/plan_batch.py`
- `scripts/planning_contract.py` and `schemas/planning-runway-v1.schema.json`
  only if existing queued artifacts must persist the accepted record
- focused planning-contract tests, plan-batch tests, and command-owner scenario
  catalog/adapter/tests.

### Current Consumer And Useful State

- Current consumer: the independent reviewer consumes the exact planner draft
  and pinned evidence packet; `_prepare_plan` consumes both role results before
  DEC-038.
- End-to-end behavior: applicable substitutive work cannot queue until every
  material caller/route has one disposition, each reachable failure has an
  owner/result/consumer, and a counterfactual would fail if forbidden legacy
  authority were invoked.
- Failure owner: planner corrects or blocks incomplete discovery; reviewer
  reconstructs and returns correction/blocked when evidence is unsupported;
  script rejects missing, duplicate, or misaligned persisted identifiers.
- Retained authority: Planning State remains structural; the project slice-shape
  policy remains the only shape preference; compatibility runner labels and
  Batch Runway execution ownership remain unchanged.
- Rollback: revert the Slice 2 commit; Slice 1 remains a complete evidence-backed
  clean-review gate.

### Acceptance Criteria

- Every applicable normal caller is classified exactly once as replaced,
  conditioned, intentionally retained, removed, or deferred.
- Retained and deferred entries have reason, owner, and terminal condition.
- Forbidden fallbacks are explicit, and physical source presence is never
  treated as semantic authority.
- Every reachable success/failure route has one owner, an observable result,
  and an exact current consumer; no undocumented old-owner fallback remains.
- Each intermediate names a current production consumer, end-to-end behavior,
  retained authority, terminal condition, and rollback boundary.
- Each ownership transfer names at least one required-green behavioral
  counterfactual that fails on forbidden old-owner invocation.
- Mechanical validation checks only representable identifiers, uniqueness,
  references, and cross-record alignment.
- The negative scenarios fail for planner/reviewer semantic reasons, while the
  valid small-plan control remains accepted without this ceremony.

### Focused Validation

- `required-green`: `python -m pytest -p no:cacheprovider -q tests/test_plan_batch.py -k 'review or evidence or migration or roles'`
- `required-green`: focused planning behavioral scenario tests covering the new
  ownership/failure/counterfactual cases.
- `conditional`: `python -m pytest -p no:cacheprovider -q tests/test_planning_contract_schema.py` when the existing runway representation changes.
- `required-green`: focused custom-agent/manifest contract tests, Ruff on
  touched Python, and `git diff --check`.
- No per-slice install or full acceptance harness.

### Worker Brief

The `runway_worker` is the required coding subagent. Implement only Slice 2 on
top of the accepted Slice 1 commit. Reuse the Slice 1 evidence boundary; do not
add a parallel result or queue route. Do not infer applicability from prose, do
not require migration fields for ordinary small plans, and do not broaden into
execution/closeout ownership.

### Review Brief

Review the exact Slice 2 commit/diff basis and independently reconstruct the
fixture entrypoints, caller dispositions, failure routes, current consumers,
and counterfactual behavior. Verify the negative cases cannot pass by copying
planner claims and the ordinary control remains compact. Echo exact basis and
strict context.

### Slice Stop Conditions

Stop if caller completeness is asserted without reconstruction, a failure path
can return to an old owner, a counterfactual is only a string/presence check,
or schema expansion becomes a new top-level family or persistent state store.

## Slice 3: Conditional Feasibility And Cost Proportionality

### Scope

Complete the applicable semantic record with decisive feasibility assumptions,
production proof or a bounded disposable proof, compound durable-write ordering
and recovery, widest-slice smaller usable alternatives, and available/unknown
execution-cost multipliers. Cover unsupported primitives, two independently
atomic writes described as one operation, rollback-only oversized boundaries,
and the valid ordinary small-plan control. Align reusable docs and installed
feature versions only where behavior changed.

### Allowed Candidate Areas

- `skills/plan-batch/SKILL.md`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `scripts/plan_batch.py`
- focused plan-batch, role, schema, manifest, and command-owner scenario tests
  and fixtures
- `docs/workflow-guide.md`, `docs/skill-routing-contract.md`, `CONTEXT.md`,
  `README.md`, `codex-features.json`, and `CHANGELOG.md` only for direct behavior
  or installation alignment.

### Current Consumer And Useful State

- Current consumer: planner/reviewer proportionality decisions and the
  deterministic pre-queue gate, using the evidence boundary delivered by
  Slices 1 and 2.
- End-to-end behavior: a decisive unproved primitive or unsupported compound
  atomicity blocks or requires bounded proof; a wide slice records the best
  smaller usable alternative; high-multiplier work records available evidence
  or explicit unknowns without universal thresholds.
- Failure owner: planner blocks/corrects assertion-only designs; reviewer
  independently evaluates proof and proportionality; script checks required
  reference shape only.
- Retained authority: semantic feasibility and cost acceptability remain human/
  reviewer judgments; actual execution telemetry remains optional.
- Rollback: revert Slice 3; Slices 1 and 2 remain useful evidence and ownership
  gates.

### Acceptance Criteria

- An unproved decisive primitive cannot authorize implementation; applicable
  production evidence or a bounded disposable proof is required.
- Compound durable writes name ordering, partial-state behavior, recovery owner,
  and fault proof; independent atomicity is not mislabeled as compound atomicity.
- The widest slice records its best smaller usable alternative and a supported
  rejection reason; common rollback alone is insufficient.
- Significant production scope, focused/repeated validation, install cadence,
  worker/reviewer passes, specialist reviews, and duplicated final gates are
  recorded from evidence or as explicit unknowns.
- No universal numeric limits, mandatory telemetry, or live-model evaluation.
- Valid small non-migration work remains compact and accepted.
- Workflow/routing/glossary/manifest/changelog changes state the assurance
  boundary without project-specific identities or topology in reusable rules.

### Focused Validation

- `required-green`: `python -m pytest -p no:cacheprovider -q tests/test_plan_batch.py -k 'review or evidence or migration or proportionality or roles'`
- `required-green`: focused planning agent, manifest, routing, and behavioral
  scenario contract tests.
- `required-green`: `python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios/catalog.yaml`
- `conditional`: schema tests if the existing runway representation changes.
- `required-green`: Ruff on touched Python and `git diff --check`.
- Candidate install and full acceptance remain final-range gates.

### Worker Brief

The `runway_worker` is the required coding subagent. Implement only Slice 3 on
the accepted prior commits. Preserve optional/conditional applicability, keep
unknown cost facts explicit, align only directly affected docs/metadata, and do
not add evaluation infrastructure, execution changes, or project-specific
generic rules.

### Review Brief

Review the exact Slice 3 commit/diff basis. Falsify assertion-only feasibility,
compound atomicity, rollback-only large-slice rationale, and invented cost
certainty. Confirm the ordinary control stays compact and reusable rules remain
project-neutral. Echo exact basis and strict context.

### Slice Stop Conditions

Stop if feasibility proof becomes mandatory for ordinary work, cost estimates
become hard thresholds, telemetry/live-model evaluation becomes required, or
scope expands beyond planning and independent review.

## Final Validation

Run from the candidate checkout after all three accepted slice commits:

1. `python -m pytest -p no:cacheprovider -q tests/test_plan_batch.py`
2. `python -m pytest -p no:cacheprovider -q tests/test_command_owner_behavioral_scenarios.py`
3. Focused planning tests in `tests/test_custom_agent_contracts.py`,
   `tests/test_codex_features_manifest.py`, and
   `tests/test_skill_routing_rule_ownership.py`.
4. `python -m pytest -p no:cacheprovider -q tests/test_planning_contract_schema.py`
   when an existing planning schema changed.
5. Ruff on all touched Python and `git diff --check`.
6. Basedpyright on changed production and scenario-adapter Python where the
   current candidate toolchain applies it.
7. One `command_owner_scenarios.py accept` invocation for the catalog, with all
   result/JSON/text outputs under one fresh `mktemp -d` directory; read the
   resulting summary before reporting acceptance.
8. Run `install.sh --dry-run` for `plan-batch`, `custom-agents`, and
   `planning-contracts` against
   `/home/alacasse/.codex-command-owner-redesign`, then install and verify
   candidate-home status.
9. Install the same dependency-expanded feature set into one fresh temporary
   Codex home and verify the installed skill, agents, script, and schema links.
10. Record stable-home `install.sh --status` and `--dry-run` before/after and
    prove no stable-home link or version changed.
11. Run `test-quality-review` on the changed behavior tests, then a final
    independent exact-range implementation review.

The broad baseline command containing the unrelated `work-batch` manifest
failure is diagnostic only. The exact pre-existing failure may remain; any new,
changed, or CCFG-35-related failure blocks final acceptance.

## Final Acceptance

The finding's complete scenario table is mapped explicitly:

| Scenario | Control class | Required disposition |
|---|---|---|
| Replacement owner with reachable old fallback | negative | planner corrects/blocks; reviewer rejects unsupported approval |
| Capability evidence omits exact callers | negative | planner corrects/blocks; reviewer requires caller reconstruction |
| Success moves but failure paths retain displaced owner | negative | planner blocks independent usability; reviewer rejects |
| Large slice justified only by common rollback | negative | planner supplies the best smaller usable alternative or proof; reviewer revises otherwise |
| No behavioral old-owner counterfactual | negative | planner adds required-green counterfactual or blocks; reviewer rejects presence-only evidence |
| Decisive primitive asserted without proof | negative | planner requires production evidence or bounded proof; reviewer rejects assertion-only feasibility |
| Intermediate producer has no current consumer | negative | planner merges/reorders/names a real consumer; reviewer rejects claimed usefulness |
| Two durable writes called one atomic operation without ordering/recovery proof | negative | planner requires partial-state/recovery/fault evidence; reviewer rejects compound atomicity claim |
| Reviewer accepts planner self-attestation | negative | queue remains unauthorized; reviewer returns revise/blocked |
| Valid small non-migration plan | positive control | planner stays compact and reviewer approves supported ordinary scope |

- All nine negative scenarios fail for the intended planner/reviewer reason and
  the positive ordinary-small-plan control remains accepted, or equivalent
  focused coverage demonstrates the same previous weakness and corrected
  disposition.
- Clean review records independently reconstructed facts and evidence; bare
  passes or planner self-attestation cannot authorize DEC-038.
- Exact dispatch/draft/approval/evidence binding remains intact.
- Applicable owner-transfer records cover entrypoints, callers, retained routes,
  forbidden fallbacks, reachable outcomes, current consumers, terminal
  conditions, and behavioral counterfactuals.
- Conditional feasibility and proportionality are evidence-backed without
  universal thresholds or mandatory telemetry.
- Valid ordinary small plans remain accepted without migration ceremony.
- Planning State stays structural; public `plan-batch` stays sole planning
  owner; Batch Runway stays execution-only.
- Candidate installation converges, fresh installation works, and stable home
  remains unchanged.
- No implementation outside planning/review, no new top-level schema/state/role,
  and no successor selection.

## Batch Stop Conditions

Stop if strict identities or write scope mismatch; if the actual independent
planning-review seam cannot be identified; if a clean result can remain
evidence-free; if owner/caller/failure/counterfactual gaps can still queue; if
assertion-only feasibility can authorize work; if deterministic validation
claims semantic truth; if migration-specific ceremony reaches ordinary work;
if a new state family, agent role, alternate queue owner, compatibility wrapper,
or universal threshold is required; if stable and candidate share runtime state;
if stable home would change; if the known unrelated baseline is silently fixed;
or if another finding is selected, prepared, implemented, or closed.

## Closeout Boundary

After implementation, validation, installation, reviews, commits, and compact
closeout evidence are complete, reconcile CCFG-35 only. Clear its selected/
queued/active state and stop with no successor selected. CCFG-26 and every other
finding remain untouched and unselected.
