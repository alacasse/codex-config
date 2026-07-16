# CCFG-24A Intake Owner Preparation Runway

## Purpose

Create and candidate-install a real `add-to-ledger/v1` owner, close the bounded
v1 intake decisions needed to implement it deterministically, bind the stable
intake scenarios to that installed owner, and produce compact cost and cleanup
evidence for a later separately planned ownership-cutover batch.

This runway implements only the expand/preparation half of CCFG-24. It must not
remove existing APR or `legacy-removal` authority, delete migration fixtures,
close CCFG-24, or prepare CCFG-25.

## Source And Authority

- Finding: CCFG-24
- Accepted contract: COR-007 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Dispatch: `dispatch.md`
- Live split amendment:
  `../../findings/ccfg-24-two-batch-execution-amendment.md`
- Superseded five-slice evidence:
  `../ccfg-24-intake-ownership-transfer/`

The split amendment controls batch boundaries. The accepted COR-007 behavior and
DEC-037 apply-only store boundary remain unchanged.

## Batch Kind And Slice Risk

- Batch kind: `migration-with-decision-gate`
- Slice 1, Define the bounded v1 intake owner contract: `evidence-only`
- Slice 2, Implement and candidate-install the target owner: `migration`
- Slice 3, Bind production scenarios and produce reassessment evidence:
  `migration`

No destructive-cleanup or contract-narrowing slice is authorized.

## Current Baseline

- Stable planning checkout: `/home/alacasse/projects/codex-config`, branch
  `master`.
- Candidate checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`.
- Stable Codex home: `/home/alacasse/.codex`.
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`.
- Candidate baseline from completed CCFG-33:
  `b38570bcd97b2584f3828abcd395b0f45ed91e58`.
- `skills/add-to-ledger/SKILL.md` is still a transitional caller-visible owner
  that routes mechanics through APR and may involve `legacy-removal`.
- Executable intake semantics still exist in the disposable CCFG-23 fixture
  adapter.
- `scripts/planning_contract.py` already supplies the accepted apply-only
  `ledger-store/v1` mechanics.
- CCFG-33 reduced the complete scenario suite to a practical acceptance path;
  do not recreate recursive report-owned pytest.

Execution must refresh all live revisions and write scopes. The baseline above
is source context, not a live execution lease.

## Batch Non-Goals

- No APR intake or mutation-route removal.
- No `legacy-removal` authority narrowing.
- No fixture/helper deletion.
- No final migration guard claiming one sole production owner across all source
  and installed surfaces.
- No stable-home installation or default switch.
- No canonical planning write from candidate processes.
- No public general intake framework or request schema.
- No CCFG-25 planning ownership work.
- No Batch B dispatch, runway, selection, or queue state.

## Allowed Candidate Areas

- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
- `codex-features.json`
- focused candidate installation metadata required for `add-to-ledger` and
  `planning-contracts`
- `tests/test_add_to_ledger.py`
- focused skill-contract migration fixtures and tests
- intake-only CCFG-23 catalog, workflow-case, adapter, and scenario test surfaces
  needed to bind observations without deleting old helpers
- `CHANGELOG.md`
- one candidate decision record under
  `docs/design/command-owner-redesign/` or another existing candidate design
  location selected by current repo conventions

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
- stable planning artifacts outside same-batch coordination and closeout

A semantic change to a read-only owner requires stop and replan.

## Execution Contract

Use the current Batch Runway execution and registered-agent result contracts.
Workers implement one slice only and do not delegate. The coordinator owns
candidate installation after source validation and review. Every test-changing
slice receives independent review followed by delta-only test-quality review.

Use fresh Planning State pickup and strict `cross-checkout-context/v1` validation
at startup and before every worker/reviewer handoff. The superseded runway's
validated snapshot is historical evidence only.

## Context Control

The execute coordinator should read, in order:

1. current Planning State facts;
2. this dispatch and runway;
3. the active slice section;
4. compact prior-slice receipts and reviews;
5. only the source files required to resolve a named unanswered question.

Avoid replaying the full superseded runway after startup. Do not paste worker or
reviewer transcripts into coordinator context. Record broad reads and large-file
reads in the runner input inventory when available.

Context thresholds:

- soft execute budget: 120,000 input tokens;
- hard warning: 180,000 input tokens;
- above 85% of the model context window: stop recommended unless the remaining
  work is only compact validation/closeout with no unresolved semantic choice.

## Execution Ledger

| Slice | Status | Risk | Commit | Focused validation | Review | Notes |
|---|---|---|---|---|---|---|
| 1. Define the bounded v1 intake owner contract | Pending | evidence-only | None | Not run | Pending | Close command, source identity, normalization, and semantic decision rules |
| 2. Implement and candidate-install the target owner | Pending | migration | None | Not run | Pending | Produce one installed owner over the apply-only store; keep old routes unchanged |
| 3. Bind production scenarios and produce reassessment evidence | Pending | migration | None | Not run | Pending | Prove installed behavior, measure cost, classify retained migration surfaces |

Accepted results move to `completed-slices.md`. Keep only pending, active, or
blocked rows here.

## Slice 1: Define The Bounded V1 Intake Owner Contract

### Goal

Produce one durable implementation decision record sufficient for a worker to
implement the smallest deterministic v1 owner without inventing policy during
coding.

### Scope

Define:

- the internal invocation boundary between `skills/add-to-ledger/SKILL.md` and
  `scripts/add_to_ledger.py`;
- input fields and result fields;
- supported source types for v1;
- exact mapping to `planning-finding/v1`, including the meaning of `source_id`,
  `source_commit`, `source_section`, and evidence pointers for each supported
  source type;
- duplicate source identity detection within one request;
- semantic decision rules for create, update, merge, no-op, and block;
- field-level update/merge behavior or an explicit decision that ambiguous cases
  block in v1;
- idempotency-key construction and separation from semantic duplicate decisions;
- success, exact-replay, and blocked result behavior;
- unsupported cases and stop behavior;
- no-selection and no-downstream-work guarantees.

Inspect only the minimum current source, accepted decisions, schemas, store API,
fixtures, and tests needed to answer these points. Do not implement code in this
slice.

### Required Decision Matrix

The record must contain explicit rows for at least:

- new source and new semantic work;
- exact same source and same normalized payload;
- same idempotency key and different payload;
- same source with changed normalized payload;
- different source that appears to describe the same work;
- conflicting source identity inside one multi-item request;
- stale whole-ledger revision/hash;
- stale touched-finding revision;
- unsupported source type;
- ambiguous merge or update.

Each row must name the command-owner action, store action if any, write/no-write
result, returned status, and whether retry is safe.

### Acceptance Criteria

- A coding worker can implement v1 without choosing a new semantic rule.
- The record does not broaden `planning-finding/v1` or `ledger-store/v1`.
- Ambiguous behavior blocks instead of silently generalizing.
- The internal API is narrow and not presented as a public general framework.
- Source mapping is concrete for every supported v1 source type.
- No production or installed file changes occur.

### Validation And Review

- Validate links and references in the decision record.
- Independent review checks completeness, consistency with COR-007 and DEC-037,
  and absence of unnecessary framework commitments.
- No test-quality review is required unless tests change.

### Commit

`docs: define bounded add-to-ledger v1 decisions`

### Stop Conditions

- Stop if a required source mapping conflicts with the current closed schema.
- Stop if update or merge semantics require a user decision not already present.
- Stop if the smallest credible v1 cannot be separated from CCFG-25 planning
  decisions.

## Slice 2: Implement And Candidate-Install The Target Owner

### Approval Gate

Slice 1 decision record is committed, independently accepted, and contains no
open implementation-semantic decision.

### Scope

- Migrate `skills/add-to-ledger/SKILL.md` to one contract-first
  `skill-contract/v1` command owner.
- Add `scripts/add_to_ledger.py` using only the decisions accepted in Slice 1.
- Keep semantic duplicate/update/merge/no-op/block decisions in the command
  owner.
- Consume `read_ledger_document` and `apply_ledger_decision` as apply-only
  mechanics.
- Register `planning-contracts` as a neutral mechanism installing the existing
  planning store script and closed schema family.
- Register the target script/link set for `add-to-ledger`.
- Add focused direct tests against temporary schema-valid ledgers.
- After source validation and review, install/update only the candidate Codex
  home and verify exact links.

Do not remove the old APR dependency or legacy routes in this slice. Where
manifest dependency topology must preserve the transitional route, document it
as temporary with Batch B removal condition.

### Acceptance Criteria

- One candidate-installed command surface invokes the real target owner.
- Fresh and multi-item supported intake mutates a temporary ledger atomically.
- Exact replay returns the same receipt without reapplication.
- Same-key/different-payload, stale CAS, source conflicts, unsupported cases, and
  ambiguous semantic cases write nothing.
- No selected, queued, active, closeout, implementation, or successor state is
  created by intake.
- The store remains apply-only.
- Candidate links resolve only to candidate sources.
- Stable links and stable home remain unchanged.
- Old routes remain present but are not modified or used to self-certify the new
  owner.

### Focused Validation

At minimum:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/add-to-ledger/SKILL.md
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py
.venv/bin/basedpyright scripts/add_to_ledger.py
git diff --check
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
```

The coordinator owns candidate installation after clean source review. Verify
status and dry-run again after installation.

### Reviews

- Independent review: ownership, deterministic decisions, non-mutating failures,
  narrow store integration, and no public framework.
- `import_topology_reviewer`: one command owner, neutral store import, no hidden
  semantic owner.
- Delta-only test-quality review: real effects, negative paths, no
  self-certification, and realistic temporary ledgers.

### Commit

`feat: prepare installed add-to-ledger owner`

### Stop Conditions

- Stop if implementation requires semantic changes to the planning store or
  schema.
- Stop if candidate installation cannot remain isolated from stable.
- Stop if the command surface cannot invoke the owner without APR deciding
  intake meaning.
- Stop rather than adding unsupported source types or generalized merge policy.

## Slice 3: Bind Production Scenarios And Produce Reassessment Evidence

### Approval Gate

The candidate-installed owner passes Slice 2 focused validation, candidate link
verification, independent review, import-topology review, and test-quality
review.

### Scope

- Rebind the four stable intake scenarios to invoke the installed production
  owner against temporary schema-valid ledgers.
- Add focused scenario coverage for source conflict, same-key/different-payload,
  stale CAS, unsupported/ambiguous block behavior, receipt recovery, and no
  downstream state effects where not already covered directly.
- Keep old fixture helpers physically present for Batch B caller/deletion
  reassessment, but ensure migrated scenarios no longer depend on them.
- Inventory every remaining caller of intake fixture helpers and every current
  APR/`legacy-removal` intake or lifecycle route.
- Record for each retained surface: caller, reason, owner, and removal condition.
- Measure:
  - changed candidate files;
  - added/deleted lines;
  - focused direct-test duration;
  - focused behavioral-suite duration;
  - exact-commit acceptance duration;
  - candidate installation/dry-run duration when observable;
  - execute coordinator context telemetry when available.
- Produce a compact Batch B reassessment packet or closeout section. Do not
  produce a Batch B dispatch or runway.

### Acceptance Criteria

- Stable intake scenarios observe the installed production owner.
- Intake contracts are green without requiring APR/Batch Runway topology,
  exact prose, or disposable helper implementation.
- Old helpers are not acceptance owners and have a complete current caller
  inventory.
- All retained migration surfaces have an explicit removal condition owned by a
  later CCFG-24 cutover batch.
- Exact acceptance preserves all 69 scenario meanings, 31 contracts, 17
  families, six keys, and six aliases.
- No legacy authority is removed and no CCFG-25 behavior is changed.
- Cost and context evidence is compact and sufficient for fresh planning.

### Focused Validation

At minimum:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/fixtures/command-owner-scenarios/workflow_adapters.py
git diff --check
```

Run the CCFG-33 exact-commit acceptance owner once from a clean candidate commit
with fresh `/tmp/ccfg-24a-*` outputs. Do not let formatting or reporting launch
additional evidence pytest processes.

### Reviews

- Independent review: scenarios call the target owner and preserve behavior.
- `dead-surface-audit`: caller and retention classification only; no deletion
  authorization.
- Delta-only test-quality review: tests protect behavior, not new module or link
  topology.
- Final exact-range independent, import-topology, dead-surface, and delta-only
  test-quality reviews.

### Commit

`test: bind intake scenarios to installed owner`

### Stop Conditions

- Stop if scenarios can pass without invoking the production owner.
- Stop if caller inventory is incomplete.
- Stop if cleanup is required to make the target behavior green.
- Stop if exact acceptance regresses non-intake families.

## Final Validation

After all three candidate commits and candidate installation:

1. Confirm Planning State still identifies only this CCFG-24A batch and no
   successor.
2. Obtain a fresh strict read-only review lease for the exact final range.
3. Run focused direct owner, skill-contract, planning-store, behavioral/catalog,
   routing/manifest mechanics required by the changed source, Ruff,
   BasedPyright, whitespace, and candidate installer status/dry-run gates.
4. Run the full manifest diagnostic and preserve the documented deferred
   CCFG-24/25/26 failure identities. This preparation batch does not claim final
   CCFG-24 source-boundary cutover.
5. Run the CCFG-33 exact-commit acceptance owner once and validate its generated
   result/report artifacts.
6. Verify candidate links resolve only to candidate sources and stable links
   remain stable-owned without a stable write.
7. Record exact candidate range, files, line delta, test durations, acceptance
   duration, install duration when available, context telemetry when available,
   and retained-surface inventory.
8. Obtain clean final reviews.
9. Write `completed-slices.md` and `closeout.md`; mark CCFG-24 `Prepared`; clear
   same-batch active state; stop without selecting Batch B or CCFG-25.

## Closeout Result Contract

A successful closeout means:

- target owner implemented and candidate-installed;
- stable intake scenarios bound to the target owner;
- direct and aggregate behavior green;
- old paths retained only as explicitly classified migration surfaces;
- CCFG-24 status `Prepared`;
- CCFG-24 final COR-007 acceptance still open;
- no successor selected.

The closeout must give a future planner enough compact evidence to decide the
smallest Batch B without loading this complete runway by default.

## Batch Stop Conditions

- Stop on Planning State mismatch, another queued/active batch, failed strict
  context, unexpected repository movement, or dirty-file conflict.
- Stop on candidate canonical planning writes or stable-home mutation.
- Stop if semantic decisions move into the store or another support skill.
- Stop if Slice 1 leaves unresolved policy.
- Stop if Slice 2 cannot produce an isolated candidate-installed command path.
- Stop if Slice 3 does not exercise that path end to end.
- Stop if work removes APR, `legacy-removal`, or fixture surfaces.
- Stop if CCFG-24 would be marked `Closed`.
- Stop if Batch B or CCFG-25 is selected, dispatched, queued, or prepared.
- Stop after same-batch closeout with CCFG-24 `Prepared`.
