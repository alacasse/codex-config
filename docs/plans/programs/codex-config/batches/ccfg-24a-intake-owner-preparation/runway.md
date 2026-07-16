# CCFG-24A Intake Owner Preparation Runway

## Purpose

Create and candidate-install a real `add-to-ledger/v1` owner, close the bounded
v1 intake decisions needed to implement it deterministically, bind the stable
intake scenarios to that installed owner, and produce compact cost and retained-
surface evidence for a later separately planned ownership-cutover batch.

This batch implements only the preparation half of CCFG-24. It must not remove
APR or `legacy-removal` authority, delete migration fixtures, close CCFG-24, or
prepare CCFG-25.

## Source And Authority

- Finding: CCFG-24
- Accepted source: COR-007 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Dispatch: `dispatch.md`
- Live split amendment:
  `../../findings/ccfg-24-two-batch-execution-amendment.md`
- Superseded five-slice evidence:
  `../ccfg-24-intake-ownership-transfer/`

The split amendment controls batch boundaries. COR-007 and DEC-037 remain the
behavior and store authorities.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`
- Slice 1, Define the bounded v1 intake owner contract: `decision-only`
- Slice 2, Implement and candidate-install the target owner: `migration`
- Slice 3, Bind production scenarios and produce reassessment evidence:
  `migration`

No destructive-cleanup or contract-narrowing slice is authorized.

`slice_shape`: three slices.

- `1 -> 2`: Slice 1 produces the accepted semantic contract consumed by the
  coding slice; implementation is blocked while policy remains unresolved.
- `2 -> 3`: Slice 2 produces an installed candidate owner; Slice 3 consumes that
  exact owner from the behavioral harness and measures real integration cost.

Cleanup remains outside this batch because it has a different risk, review, and
rollback boundary.

## Current Baseline And Assumptions

- Stable planning checkout: `/home/alacasse/projects/codex-config`, branch
  `master`.
- Candidate checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`.
- Stable Codex home: `/home/alacasse/.codex`.
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`.
- Candidate baseline from completed CCFG-33:
  `b38570bcd97b2584f3828abcd395b0f45ed91e58`.
- `add-to-ledger` remains a transitional owner routed through APR.
- Disposable CCFG-23 fixture helpers still own executable intake observations.
- `scripts/planning_contract.py` already supplies apply-only
  `ledger-store/v1` mechanics.
- CCFG-33 supplies the practical exact-commit scenario acceptance owner.

Execution must refresh all live revisions and write scopes. These are source
facts, not a live lease.

## Batch Non-Goals

- No APR intake or mutation-route removal.
- No `legacy-removal` authority narrowing.
- No fixture/helper deletion.
- No final source-boundary migration guard.
- No stable-home install, refresh, unlink, rebind, or default switch.
- No canonical planning write from candidate processes.
- No public general intake framework, public request schema, durable intake
  queue, second store, or second ledger.
- No CCFG-24B dispatch/runway and no CCFG-25 work.

## Allowed Candidate Areas

- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
- `codex-features.json`
- focused installation metadata for `add-to-ledger` and `planning-contracts`
- `tests/test_add_to_ledger.py`
- focused skill-contract migration fixtures/tests
- intake-only CCFG-23 catalog, workflow-case, adapter, and scenario test surfaces
- `CHANGELOG.md`
- one candidate implementation decision record under the existing command-owner
  redesign design area

## Read-Only Unless A Focused Blocking Gap Is Proven

- `scripts/planning_contract.py`
- `schemas/planning-*-v1.schema.json`
- `scripts/skill_contract.py`
- `schemas/skill-contract-v1.schema.json`
- `scripts/planning_state.py`
- `skills/architecture-program-runway/**`
- `skills/legacy-removal/**`
- `skills/plan-batch/**`
- `skills/work-batch/**`
- `skills/batch-runway/**`

A semantic change to a read-only owner requires stop and replan.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2. Registered agent TOMLs
own worker, reviewer, specialist, investigator, and Spark result schemas.
Use Batch Runway Compact Report Contract v1 only for coordinator receipts and
its other non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for suspicious coordinator or
subagent-lifecycle behavior.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/test-quality-review/SKILL.md`

Workers implement one slice only and do not delegate. Candidate installation is
coordinator-owned after source validation and review. Every test-changing slice
receives independent review followed by delta-only test-quality review.

## Required Planning Snapshot

Interface: `cross-checkout-context/v1`.

Installed helper used by the immediately superseded validated planning flight:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Canonical planning root:

```text
/home/alacasse/projects/codex-config/docs/plans
```

Inherited complete validated plan-time payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: d739bd5660165fe321981ae0219a61c56667560b
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: d739bd5660165fe321981ae0219a61c56667560b
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: b38570bcd97b2584f3828abcd395b0f45ed91e58
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

This payload is retained verbatim because the replacement preserves the same
finding scope, roots, generation role, and candidate baseline. It is historical
evidence only. At startup, `work-batch` must confirm this replacement queued
scope through Planning State, obtain a fresh ready preflight, and validate the
current exact write scope before every delegated handoff. Do not hand-edit the
historical revisions above.

## Context Control

The execute coordinator should read, in order:

1. current Planning State facts;
2. this dispatch and runway;
3. the active slice section;
4. compact prior-slice receipts and reviews;
5. only source files required for a named unanswered question.

Do not replay the full superseded runway after startup or paste worker/reviewer
transcripts into coordinator context. Record broad and large-file reads in the
runner input inventory when available.

- Soft execute budget: 120,000 input tokens.
- Hard warning: 180,000 input tokens.
- Above 85% of the model context window: stop recommended unless only compact
  validation/closeout remains and no semantic choice is unresolved.

## Validation Profile And Status Classes

- Runway density: `full-runway`.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Existing planning-store, skill-contract, behavioral/catalog, routing,
  cross-checkout, installer status/dry-run, Ruff, BasedPyright, and whitespace
  baselines used by the active candidate are `required-green`.
- Slice 1 decision-record validation is implementation-created
  `required-green` before Slice 2.
- Slice 2 direct owner tests and candidate installation checks are
  implementation-created `required-green`.
- Slice 3 migrated intake scenarios, caller inventory, cost evidence, and
  exact-commit acceptance are implementation-created `required-green`.
- The full manifest diagnostic remains `known-red-baseline`: only the previously
  assigned CCFG-24/25, CCFG-25, and CCFG-26 identities may remain red.
- Existing stable-interpreter dependency collection failures remain
  `diagnostic-only`; they do not authorize package installation.

Every concrete command must be recorded with its status class before it gates a
slice or closeout.

## Execution Ledger

| Slice | Status | Risk | Commit | Focused validation | Review | Notes |
|---|---|---|---|---|---|---|
| 1. Define bounded v1 decisions | Blocked | decision-only | None | Decision record drafted; store-contract investigation complete | Findings | Required metadata-only no-op idempotency cannot be represented by the accepted apply-only store request; stop and replan before implementation |
| 2. Implement and install target owner | Pending | migration | None | Not run | Pending | Candidate owner over apply-only store; old routes unchanged |
| 3. Bind scenarios and measure | Pending | migration | None | Not run | Pending | Prove installed behavior and classify retained surfaces |

Accepted results move to `completed-slices.md`.

## Execution Blocker

Slice 1 stopped on 2026-07-16 before any commit or production change.
Independent review and a focused `ledger-store/v1` code-path investigation
proved that the required same-key/different-complete-caller-payload behavior
cannot be implemented for a metadata-only no-op through the accepted store API:

- DEC-037 hashes the apply request, not the upstream intake request;
- a valid no-op has empty finding mutations and therefore must also have empty
  touched-finding revisions;
- the request exposes no existing metadata carrier for source/proposal identity;
- fake touches are rejected, and an unchanged finding mutation must increment
  its revision.

Distinct no-op intake payloads using the same `request_id` can therefore
collapse to one store payload and return `exact_replay` instead of the required
`idempotency_mismatch`. Encoding the missing identity requires a store request
or semantic change, which this runway classifies as read-only and names as a
Slice 1 stop condition.

The other review findings remain decision-record work: canonical mutation
authority, create-ID allocation from the CAS-bound snapshot, URL/timestamp
canonicalization, file-at-commit verification, and semantic-overlap
normalization. They do not make Slice 2 safe while the store gap remains.

Next safe action: preserve this queued runway and use a later explicit planning
request to amend or replace it with an authorized store-contract decision and
corresponding execution scope. Do not start Slice 2, weaken the required
idempotency matrix, close CCFG-24, or select successor work.

## Slice 1: Define Bounded V1 Decisions

### Scope

Produce one durable candidate decision record defining:

- the `SKILL.md -> scripts/add_to_ledger.py` invocation boundary;
- supported v1 source types and exact mapping to `planning-finding/v1`;
- meanings of `source_id`, `source_commit`, `source_section`, and evidence
  pointers for each supported source type;
- create/update/merge/no-op/block behavior;
- field-level update/merge behavior, or explicit blocking where ambiguous;
- idempotency construction and separation from semantic duplicates;
- success, exact-replay, and blocked results;
- unsupported cases and no-downstream-work behavior.

The decision matrix must cover new work, exact replay, same key/different
payload, changed same-source payload, different-source semantic overlap,
in-request identity conflict, stale whole-ledger CAS, stale finding revision,
unsupported source type, and ambiguous update/merge.

### Acceptance And Gate

- A coding worker can implement v1 without choosing policy.
- No planning schema or store semantic change is required.
- Ambiguous cases fail closed instead of generalizing.
- No production or installed file changes occur.
- Independent review accepts the record before Slice 2.

### Validation

Decision-record link/reference checks: `required-green`.
No test-quality review unless tests change.

### Commit

`docs: define bounded add-to-ledger v1 decisions`

### Stop Conditions

- Stop on schema conflict, unresolved user decision, or coupling to CCFG-25.

## Slice 2: Implement And Candidate-Install The Target Owner

### Approval Gate

Slice 1 is committed, independently accepted, and contains no unresolved
implementation-semantic choice.

### Scope

- Migrate `skills/add-to-ledger/SKILL.md` to one contract-first owner.
- Add `scripts/add_to_ledger.py` implementing only accepted v1 decisions.
- Keep semantic decisions in the command owner and consume
  `read_ledger_document`/`apply_ledger_decision` as apply-only mechanics.
- Register neutral `planning-contracts` and target `add-to-ledger` links.
- Add focused direct tests against temporary schema-valid ledgers.
- After clean source reviews, install/update only the candidate Codex home and
  verify exact links.

Do not remove or narrow old routes. Any transitional dependency retained in the
manifest must name Batch B as its removal owner and final CCFG-24 cutover as its
removal condition.

### Acceptance Criteria

- Candidate-installed command invokes the real owner.
- Supported fresh/multi intake is atomic.
- Exact replay does not reapply.
- Same-key/different-payload, stale CAS, source conflict, unsupported, and
  ambiguous cases write nothing.
- Intake creates no selected/queued/active/closeout/successor state.
- Store remains apply-only; stable home remains unchanged.

### Focused Validation

The following are implementation-created `required-green` gates:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/add-to-ledger/SKILL.md
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py
.venv/bin/basedpyright scripts/add_to_ledger.py
git diff --check
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
```

### Reviews

- Independent ownership/store/failure-path review.
- `import_topology_reviewer` for one owner and neutral store imports.
- Delta-only test-quality review for real effects and negative paths.

### Commit

`feat: prepare installed add-to-ledger owner`

### Stop Conditions

- Stop on required store/schema semantic change, stable-home mutation, hidden APR
  semantic dependency, or pressure to generalize unsupported policy.

## Slice 3: Bind Scenarios And Produce Reassessment Evidence

### Approval Gate

Slice 2 direct gates, candidate links, independent review, import-topology
review, and test-quality review are clean.

### Scope

- Rebind the four stable intake scenarios to the installed production owner.
- Add focused conflict, replay, stale, recovery, unsupported/ambiguous, and
  no-state-effect coverage where direct tests are insufficient.
- Keep old helpers physically present, but ensure migrated scenarios no longer
  depend on them.
- Inventory every remaining intake-helper caller and APR/`legacy-removal` route.
- Record caller, reason, owner, and removal condition for each retained surface.
- Record changed files, line delta, direct-suite duration, behavioral-suite
  duration, exact-acceptance duration, installation duration when observable,
  and coordinator context telemetry when available.
- Produce compact Batch B reassessment evidence, not a dispatch or runway.

### Acceptance Criteria

- Stable intake scenarios exercise the installed owner.
- Intake contracts are green without legacy topology or disposable helper logic.
- Old helpers are not acceptance owners and have a complete caller inventory.
- All retained surfaces have explicit later removal ownership.
- Exact acceptance preserves all 69 scenarios, 31 contracts, 17 families, six
  keys, and six aliases.
- No legacy authority or CCFG-25 behavior changes.

### Focused Validation

The following are implementation-created `required-green` gates:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/fixtures/command-owner-scenarios/workflow_adapters.py
git diff --check
```

Run the CCFG-33 exact-commit acceptance owner once from a clean candidate commit
with fresh `/tmp/ccfg-24a-*` outputs.

### Reviews

- Independent scenario/behavior review.
- `dead-surface-audit` for caller/retention classification only.
- Delta-only test-quality review.
- Final exact-range independent, import-topology, dead-surface, and test-quality
  reviews.

### Commit

`test: bind intake scenarios to installed owner`

### Stop Conditions

- Stop if scenarios bypass the production owner, inventory is incomplete,
  cleanup is required to turn green, or non-intake acceptance regresses.

## Final Validation

1. Confirm Planning State identifies only this batch and no successor.
2. Obtain a fresh strict read-only review lease for the exact final range.
3. Run required-green owner, store, skill-contract, behavioral/catalog,
   routing/manifest mechanics, Ruff, BasedPyright, whitespace, and candidate
   installer status/dry-run gates.
4. Reproduce the exact known-red manifest identities without a new failure.
5. Run the CCFG-33 exact-commit acceptance owner once and validate its artifacts.
6. Verify candidate links are candidate-owned and stable links remain stable-
   owned without a stable write.
7. Record range, files, line delta, durations, context telemetry when available,
   and retained-surface inventory.
8. Obtain clean final reviews.
9. Write `completed-slices.md` and `closeout.md`; mark CCFG-24 `Prepared`; clear
   same-batch state; stop without selecting Batch B or CCFG-25.

## Closeout Result Contract

Successful closeout means the target owner is candidate-installed and exercised
by stable intake scenarios, direct and aggregate behavior is green, old paths
remain only as classified migration surfaces, CCFG-24 is `Prepared`, final
COR-007 acceptance remains open, and no successor is selected.

The closeout must be compact enough for a future planner to design the smallest
Batch B without rereading this complete runway by default.

## Batch Stop Conditions

- Stop on Planning State mismatch, another queued/active batch, failed strict
  context, repository movement, or dirty-file conflict.
- Stop on candidate canonical planning writes or stable-home mutation.
- Stop if semantic decisions move into the store or another support skill.
- Stop if Slice 1 leaves unresolved policy.
- Stop if Slice 2 cannot produce an isolated candidate-installed owner.
- Stop if Slice 3 does not exercise that owner end to end.
- Stop if work removes APR, `legacy-removal`, or fixture surfaces.
- Stop if CCFG-24 would be `Closed`.
- Stop if Batch B or CCFG-25 is selected, dispatched, queued, or prepared.
- Stop after same-batch closeout with CCFG-24 `Prepared`.
