# CCFG-19 Source Contract Decisions Dispatch

## Batch Identity

- Batch ID: `ccfg-19-source-contract-decisions`
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-19, Verify Source Contracts and Resolve Blocking
  Decisions
- Dispatch state: queued through the co-located concrete runway
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md`
- Successor selected: no

## Selection Decision

Select CCFG-19 now because CCFG-18 is closed, its strict candidate-generation
handoff is proven, and CCFG-20 through CCFG-29 depend directly or transitively
on decisions owned by CCFG-19.

The source row mixes evidence gathering, test classification, protocol
decisions, and topology verification. It is therefore not suitable for broad
direct expansion. This dispatch narrows it to one design-only candidate
amendment batch with four bounded slices. The batch may verify source and tests
read-only and may update only the candidate design record; it may not implement
schemas, `ledger-store`, planning transactions, runner changes, command-owner
transfers, installer changes, or production behavior.

## Gate Evidence

```yaml
planning_state:
  root: /home/alacasse/projects/codex-config/docs/plans
  current: passed
  validate: passed
  selected_dispatch: null
  queued_runway: null
  active_runway: null
  blockers: []
  warnings:
    - two known redirect-ledger warnings
stable_control:
  repository_root: /home/alacasse/projects/codex-config
  branch: master
  commit: e1946ad41df24190c0938ffa171426a34c027c0e
  codex_home: /home/alacasse/.codex
  worktree_before_planning: clean
  install_status: passed
  install_dry_run: passed
candidate_generation:
  repository_root: /home/alacasse/projects/codex-config-command-owner-redesign
  branch: implementation/command-owner-redesign
  commit: 9027bd1ea35e66e263dfced02a2b9f91835c1bd9
  codex_home: /home/alacasse/.codex-command-owner-redesign
  worktree_before_planning: clean
  install_status: passed
  install_dry_run: passed
accepted_lineage:
  authoritative_base: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
  ancestry_preserving_merge: b044e3c348922663aa074638227aae8d2633cfe3
strict_context:
  interface: cross-checkout-context/v1
  installed_helper: /home/alacasse/.codex/scripts/cross_checkout_context.py
  helper_resolves_to: /home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
  payload_validation: passed
  canonical_planning_write_scope_validation: passed
focused_baseline:
  source_and_topology_tests: 285_passed
  cross_checkout_manifest_subset: 3_passed_18_deselected
  workflow_boundary_tests: 31_passed
  full_manifest: known_red_3_failed_18_passed
```

The full manifest failures are the unchanged exact-wording baseline documented
by the CCFG-18 closeout. They are diagnostic only and are not part of this
design-only batch.

## Batch Kind And Risk

- Batch kind: `mixed-risk`.
- Slice 1 risk: `evidence-only`.
- Slices 2 through 4 risk: `decision-only`.
- Migration: forbidden.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Destructive, contract-narrowing, and migration approval gates: none, because
  no such slice is authorized.
- Decision approval gate: after accepted Slice 1 evidence and before Slice 2,
  the execution coordinator must present one compact recommendation packet for
  schema evolution, `ledger-store`, the runner protocol, and OPEN-003 to the
  user. Slices 2 through 4 may record only the user's approved or amended
  decisions. Silence is not approval.
- Candidate-checkout write access remains subject to execution-time filesystem
  approval. Approval does not widen the allowed files or finding scope.

## Goal

Produce one joined, auditable CCFG-19 verification and decision record that:

- maps every current behavior contract to source evidence, target owner,
  scenarios, and test classification;
- closes the schema-evolution and unknown-field policy;
- closes the narrow apply-only `ledger-store` boundary;
- closes the runner public-command and no-successor-readiness boundary;
- verifies the accepted generation and branch topology;
- resolves OPEN-003 with a recoverable planning-transaction protocol or records
  one explicit blocker; and
- records remaining non-blocking user decisions without guessing them.

## Owner Seam And Validation Class

- Decision owner: the command-owner redesign candidate design record.
- Controlling generation: stable.
- Canonical planning owner:
  `/home/alacasse/projects/codex-config/docs/plans`.
- Candidate amendment owner:
  `/home/alacasse/projects/codex-config-command-owner-redesign`.
- Candidate output:
  `docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`.
- Supporting candidate files: `docs/design/command-owner-redesign/decisions.md`
  and `docs/design/command-owner-redesign/README.md`.
- Validation profile: `docs-only` with focused source-characterization tests
  assigned only at final validation.
- Run artifact root: `None`.
- Output root: `None`.
- Integration harness: not required.

## Existing Gaps To Resolve

- The accepted design contains 31 behavior contracts but no joined
  contract-to-source-to-owner-to-scenario matrix.
- Fifteen scenario IDs referenced by the contracts are absent from the current
  behavioral scenario catalog.
- The current test inventory has no durable classification by behavioral,
  schema, integration, migration-retention, topology, text-contract, or
  historical role.
- Schema documents state a closed-world policy, but current validators are not
  uniform about unknown object keys; the target rule and exceptions need one
  accepted boundary.
- No `ledger-store` implementation exists, so CCFG-19 must accept its apply-only
  contract without beginning CCFG-24 implementation.
- The current runner still routes old APR and Batch Runway modes and interprets
  successor readiness; CCFG-19 records the target protocol and rewrite/delete
  dispositions without changing runner code.
- OPEN-003, the multi-artifact planning transaction, remains unresolved.

## Included Source Scope

- Immutable CCFG-19 intake at accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Candidate design files `01-source-behavior-contracts.md`,
  `02-target-ownership-model.md`, `03-contract-first-formats.md`,
  `04-migration-program.md`, `05-behavioral-test-matrix.md`, `decisions.md`,
  and `09-live-precreation-amendment.md` as read-only evidence except for the
  three explicitly allowed output files above.
- Current source and tests named by the contracts as read-only evidence.
- CCFG-18 closeout and completed-slice evidence for generation and lineage.

## Deferred And Excluded

- CCFG-20 schema and validator implementation.
- CCFG-21 planning-artifact schemas and transaction prototype.
- CCFG-22 skill-authoring finalization.
- CCFG-23 topology-independent behavioral harness.
- CCFG-24 `ledger-store` implementation and intake ownership transfer.
- CCFG-25 through CCFG-29 ownership transfer, execution transfer, cutover,
  deletion, and convergence.
- Changes to stable source files outside this batch's canonical planning
  artifacts.
- Changes to candidate production code, tests, skills, scripts, manifests,
  agents, installer surfaces, or generated artifacts.

## Suggested Slice Shape

1. Join source, owner, scenario, and test-classification evidence.
2. Accept schema-evolution and apply-only `ledger-store` boundaries.
3. Accept the runner public-command boundary and verify generation/branch
   topology.
4. Resolve OPEN-003 and audit the complete CCFG-19 exit gate.

## Required Strict Execution Context

Mode: explicit `cross-checkout-context/v1`.

Installed helper used for planning validation:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Canonical planning root:

```text
/home/alacasse/projects/codex-config/docs/plans
```

Complete validated payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: e1946ad41df24190c0938ffa171426a34c027c0e
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: e1946ad41df24190c0938ffa171426a34c027c0e
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 9027bd1ea35e66e263dfced02a2b9f91835c1bd9
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

The installed stable helper parsed this payload and validated the exact four
canonical planning paths for `CURRENT.md`, `LEDGER.md`, this dispatch, and the
co-located runway. Planning performed no candidate write.

## Stop Conditions

- Stop if the strict context, canonical planning root, installed helper, stable
  revision, candidate revision, generation, or root identity does not validate.
- Stop if the candidate worktree is not clean before Slice 1 or contains changes
  outside the allowed candidate design files.
- Stop if any slice would implement a deferred CCFG-20 through CCFG-29 surface.
- Stop if evidence cannot eliminate an ownership conflict; record the exact
  conflict and leave CCFG-19 blocked.
- Stop before Slice 2 until the user explicitly approves or amends the compact
  decision packet produced from Slice 1 evidence.
- Stop if OPEN-003 cannot be accepted safely; record one explicit blocker and
  leave CCFG-19 blocked rather than guessing.
- Stop if a slice proposes migration, contract narrowing, destructive cleanup,
  or changes to supported runtime behavior.
- Stop closeout before selecting, refreshing, dispatching, or preparing
  CCFG-20 or any other successor.
