# CCFG-24 Intake Ownership Transfer Dispatch

## Selection

- Batch ID: `ccfg-24-intake-ownership-transfer`
- Source ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-24, Transfer Intake Ownership to `add-to-ledger`.
- Accepted immutable source: COR-007 at commit
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Live source packet:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md`.
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-24-intake-ownership-transfer/runway.md`.
- CCFG-22, CCFG-23, and CCFG-33 are closed. CCFG-25 through CCFG-29 remain
  open and unselected.

## Selection Decision

Select CCFG-24 as the only queued batch. Its dependencies are closed, the live
planning state is idle, and the ledger now names this explicit `plan-batch`
request as the owner of selection.

The row is one bounded ownership transfer with required same-work cleanup:

1. make `add-to-ledger/v1` the sole semantic owner of intake and canonical
   ledger-mutation decisions;
2. consume the existing apply-only `ledger-store/v1` mechanism without moving
   duplicate, merge, no-op, selection, or closeout meaning into that mechanism;
3. rebind the CCFG-23 intake scenarios to the production owner and remove the
   replaced fixture-only intake implementation;
4. remove APR intake/normalization and normal ledger-mutation authority while
   preserving its still-deferred CCFG-25 planning and CCFG-26 closeout seams;
5. make `legacy-removal` evidence-only by removing its program-owner,
   selected-dispatch, queue, execution, and closeout escape hatch; and
6. install the command owner and neutral planning-contract mechanism only in
   the candidate generation.

This is not a broad APR or Batch Runway deletion batch. Physical deletion of
those remaining owners is reserved for CCFG-28 after CCFG-25 through CCFG-27.

## Goal And Owner Seam

The human-facing `add-to-ledger` feature becomes one production owner composed
of:

- the contract-first `skills/add-to-ledger/SKILL.md` command surface; and
- an internal, installed `scripts/add_to_ledger.py` implementation of
  `add-to-ledger/v1` that owns intake eligibility, source identity,
  normalization, duplicate/update/merge/no-op decisions, and the exact caller
  decision passed to `ledger-store/v1`.

The existing `scripts/planning_contract.py` store remains a narrow apply-only
mechanism. Register it and the existing planning schema family under one new
agent-facing neutral feature named `planning-contracts`; do not place it under
APR, `legacy-removal`, or another command owner's semantic authority.

## Included Contracts

- `INTAKE-SOURCE-001`: fresh work crosses one explicit ingestion boundary.
- `INTAKE-IDENTITY-002`: source type, external identifier, title, URL or path,
  and compact evidence pointers preserve source identity.
- `INTAKE-NORMALIZE-003`: output is one or more individually addressable
  `planning-finding/v1` records without silently authorizing unsupported risk.
- `INTAKE-MUTATE-004`: create, update, merge, or no-op applies to one canonical
  ledger with revision checks, idempotence, and a compact receipt.
- `INTAKE-STOP-005`: intake creates no selection, dispatch, runway,
  implementation, closeout, or successor work.
- DEC-037: `ledger-store/v1` is whole-ledger CAS, exact-replay aware,
  deterministic, atomic, and apply-only.

## Explicitly Deferred

- CCFG-25 owns `plan-batch` selection, scope shaping, dispatch, runway, risk,
  approvals, validation profiles, and removal of APR planning plus Batch Runway
  create-spec semantics.
- CCFG-26 owns `work-batch` execution/closeout transfer and removal of APR
  reconciliation plus Batch Runway execute/finalize semantics.
- CCFG-27 owns candidate cutover preparation and rehearsal.
- CCFG-28 owns physical deletion of remaining legacy owner directories and the
  final switch.
- CCFG-29 owns convergence, merge into current master, default-home rebinding,
  and bridge removal.
- `tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_executable_work_source_boundary_is_explicit`
  retains only its CCFG-25 planning-owner remainder after the intake half is
  migrated. Do not repair its plan-batch text coupling in this batch.

## Batch Kind And Risk

- Batch kind: `mixed-risk`.
- Slice 1: `migration` — establish the real command owner and its narrow store
  integration.
- Slice 2: `destructive-cleanup` — replace and delete the CCFG-23 disposable
  intake adapter logic only after the new owner is green.
- Slice 3: `contract-narrowing` — remove APR intake and normal mutation routes
  while preserving CCFG-25/26 authority.
- Slice 4: `contract-narrowing` — remove `legacy-removal` lifecycle ownership
  while preserving its evidence vocabulary.
- Slice 5: `migration` — reconcile neutral installation, routing, docs,
  migration guards, and complete acceptance.

### Approval Gates

- Slice 2 is approved by COR-007 only after production intake scenarios are
  green and a caller inventory proves no remaining non-migration caller needs
  the disposable fixture helpers.
- Slice 3 is approved by DEC-001, DEC-005, DEC-037, and COR-007 only after the
  target intake owner is green and the remaining APR planning/closeout paths
  required by CCFG-25 and CCFG-26 are explicitly preserved.
- Slice 4 is approved by DEC-019 and COR-007 only after an
  `legacy-evidence-no-state-writes` test is green and the deletion/dead-surface
  evidence vocabulary remains available.

The execution coordinator records each gate as satisfied or stops. The gates do
not authorize broader deletion or successor work.

## Slice Shape

`slice_shape`: five slices.

- `1 -> 2`: Slice 1 produces a valid, tested production owner; Slice 2 may then
  migrate the behavioral consumer and delete only the replaced disposable
  adapter. The intermediate state is green with temporary duplicate fixture
  evidence still present.
- `2 -> 3`: Slice 2 leaves target intake behavior independent of APR. Slice 3
  can therefore narrow APR without coupling behavior migration to contract
  deletion.
- `3 -> 4`: APR and `legacy-removal` are distinct owner seams with different
  surviving responsibilities and separate rollback/review boundaries.
- `4 -> 5`: after semantic ownership and cleanup are accepted, Slice 5 can
  reconcile installation, metadata, docs, and the complete migration guard
  against one stable implementation range.

No slice exists merely to meet a target count. Each boundary has an independently
green intermediate state, separate owner seam, risk class, or approval gate.

## Required Guardrails

- Planning reads and writes remain under
  `/home/alacasse/projects/codex-config/docs/plans`.
- Candidate implementation writes remain under
  `/home/alacasse/projects/codex-config-command-owner-redesign`.
- Stable `/home/alacasse/.codex` remains installed from the stable checkout and
  must not be refreshed, installed, unlinked, or rebound.
- Candidate installation may update only
  `/home/alacasse/.codex-command-owner-redesign` after source validation and
  review.
- `scripts/planning_contract.py`, `schemas/planning-finding-v1.schema.json`,
  `scripts/skill_contract.py`, and `schemas/skill-contract-v1.schema.json` are
  read-only unless a focused test proves a mechanical gap that the owning
  contract cannot satisfy. Stop before changing their semantics.
- Do not make `skill-authoring` a runtime dependency of any command owner.
- Do not create a public general intake framework, a second planning store, a
  parallel ledger, or a candidate-controlled canonical planning write.

## Validation Class

- Runway density: `full-runway`.
- Validation profile: `project-harness-production`.
- Tests changed in every behavioral/cleanup slice require delta-only
  `test-quality-review` after normal independent review.
- Final acceptance must use the CCFG-33 exact-commit acceptance owner once from
  a clean candidate commit, with fresh `/tmp/ccfg-24-*` outputs.

## Strict Cross-Checkout Planning

Interface: `cross-checkout-context/v1`.

Installed helper used for planning validation:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Helper resolution:

```text
/home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
```

Canonical planning root:

```text
/home/alacasse/projects/codex-config/docs/plans
```

Complete validated plan-time payload:

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

The installed stable helper accepted the complete payload and the exact four
planning write paths for `CURRENT.md`, `LEDGER.md`, `dispatch.md`, and
`runway.md`. This planning snapshot is immutable historical evidence, not a live
execution lease. `work-batch` must confirm the same selected scope through
Planning State, obtain a fresh ready preflight, and validate every handoff's
exact write scope.

## Stop Conditions

- Stop if Planning State reports another selected, queued, or active batch.
- Stop if the strict context or canonical/candidate write scope fails.
- Stop if the production `add-to-ledger/v1` owner or neutral installed
  `planning-contracts` mechanism is left unnamed.
- Stop if semantic intake decisions move into `ledger-store/v1`.
- Stop if CCFG-24 changes plan selection behavior reserved for CCFG-25.
- Stop if APR cleanup disturbs planning or closeout responsibilities reserved
  for CCFG-25 or CCFG-26.
- Stop if `legacy-removal` evidence vocabulary is deleted instead of only its
  lifecycle authority.
- Stop if fixture intake logic is deleted before replacement behavior is green.
- Stop if any candidate process mutates canonical planning state.
- Stop after queueing this one runway; do not implement any slice.
