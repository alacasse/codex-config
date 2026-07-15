# CCFG-21 Planning Artifact Contracts Dispatch

## Batch Identity

- Batch ID: `ccfg-21-planning-artifact-contracts`
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-21, Implement Planning Artifact Schemas and
  Validators
- Dispatch state: queued through the co-located concrete runway
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/runway.md`
- Successor selected: no

## Selection Decision

Select the user-requested CCFG-21 row now. CCFG-19 and CCFG-20 are closed,
DEC-036, DEC-037, and DEC-038 are accepted, and OPEN-003 is resolved. COR-004
therefore has no unresolved dependency or planning-transaction decision.

The vague-row guard passes. The accepted contracts define one planning-contract
owner seam, six exit keys, a closed-world schema policy, the apply-only
`ledger-store/v1` boundary, the exact four-stage selection saga, and explicit
fault-recovery rules. This batch may add fixture-driven planning schemas, one
deep repo-local validator/store module, deterministic tests, and a changelog
entry in the candidate checkout. It may not migrate live planning files,
integrate command owners, install a feature, or begin CCFG-22 through CCFG-29.

CCFG-2 through CCFG-6 and CCFG-9 through CCFG-11 remain deferred because the
user requested CCFG-21 and those rows are conditional or require fresh
replanning. CCFG-22 through CCFG-29 remain separate command-owner redesign
findings with their recorded dependency chain.

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
  commit: b2a04a32d5871c96ebb5e93ccf4056a32f2db07b
  codex_home: /home/alacasse/.codex
  worktree_before_planning: clean
  install_status: passed_with_manifest_version_drift
  install_dry_run: passed_without_writes
candidate_generation:
  repository_root: /home/alacasse/projects/codex-config-command-owner-redesign
  branch: implementation/command-owner-redesign
  commit: 3e54155964e92d3a4dced8268cc683baaab9be1c
  upstream_ahead_behind: 0/0
  worktree_before_planning: clean
accepted_lineage:
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
  ccfg_19_status: closed
  ccfg_20_status: closed
  schema_evolution_decision: DEC-036
  ledger_store_decision: DEC-037
  planning_transaction_decision: DEC-038
  planning_transaction_open_question: resolved
strict_context:
  interface: cross-checkout-context/v1
  installed_helper: /home/alacasse/.codex/scripts/cross_checkout_context.py
  helper_resolves_to: /home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
  payload_validation: passed
  canonical_planning_write_scope_validation: passed
  intended_implementation_write_scope_validation: passed
focused_baseline:
  planning_state_transition_subset: 8_passed
  planning_state_broader_contract_subset: 33_passed_145_deselected
  skill_contract_suite: 42_passed
  cross_checkout_and_agent_contracts: 33_passed_187_subtests
  manifest_schema_subset: 3_passed_18_deselected_31_subtests
  full_manifest: known_red_3_failed_18_passed
```

## Batch Kind And Risk

- Batch kind: `migration`.
- Slices 1 through 4 risk: `migration`.
- Authorized migration: add the target closed-world planning contract layer,
  fixture-only compatibility readers, revisioned stores, lineage checks, and
  the DEC-038 transaction prototype.
- Live planning-artifact migration: forbidden.
- Command-owner integration or ownership transfer: forbidden.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Destructive or contract-narrowing approval gates: none, because no such slice
  is authorized.
- Candidate-checkout write access remains subject to execution-time filesystem
  approval. Approval does not widen the allowed files or finding scope.

## Goal

Implement one deep, repo-local planning contract seam that:

- validates closed-world `planning-current/v1`, `planning-finding/v1`,
  `planning-dispatch/v1`, `planning-runway/v1`, and `planning-closeout/v1`
  blocks with deterministic diagnostics;
- reads explicitly selected active old-format Markdown without allowing legacy
  writes or prose inference;
- applies expected revision and file-hash compare-and-swap, adjacent atomic
  replacement, reread validation, idempotency, and recoverable receipts;
- implements the apply-only `ledger-store/v1` mechanics while leaving all
  semantic decisions with command owners;
- confirms the accepted per-finding ledger default through a deterministic
  comparison with one global block;
- validates artifact lineage and producer generation identity; and
- prototypes DEC-038's append-only four-stage selection saga with exact replay,
  receipt recovery, mismatch blocking, visible partial evidence, and the full
  fault model.

## Owner Seam And Validation Class

- Module seam: `scripts/planning_contract.py`.
- Structural schema owners:
  - `schemas/planning-current-v1.schema.json`
  - `schemas/planning-finding-v1.schema.json`
  - `schemas/planning-dispatch-v1.schema.json`
  - `schemas/planning-runway-v1.schema.json`
  - `schemas/planning-closeout-v1.schema.json`
  - `schemas/planning-selection-transaction-v1.schema.json`
- Public surface: one validation entry point plus narrow current, ledger,
  artifact-write, and selection-saga operations in the same module. Parsing,
  JSON Schema loading, deterministic rendering, atomic persistence, receipt
  construction, fault injection, and CLI adaptation remain private.
- CLI: a thin adapter over the same public operations for validation, ledger
  representation comparison, and fixture-only selection-saga simulation.
- Existing dependencies: reuse the candidate's locked PyYAML and jsonschema;
  do not add another parser, schema library, or dependency lock change.
- Installed surface: none in CCFG-21. `codex-features.json` remains unchanged.
- Validation profile: `project-harness-production` with repo-local fixture CLI
  runs as the integration harness.
- Runway density: `full-runway` because the work adds versioned YAML schemas,
  atomic state writes, public CLI behavior, and fault-recovery semantics.
- Run artifact root: `None`.
- Output root: `None`.
- Test quality review: `delta-only` for every slice.

## Included Source Scope

- COR-004 / CCFG-21 in accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Accepted planning formats and canonicality rules in
  `docs/design/command-owner-redesign/03-contract-first-formats.md`.
- CCFG-21 entry and exit gates in
  `docs/design/command-owner-redesign/04-migration-program.md`.
- DEC-036 closed-world schema evolution, DEC-037 apply-only ledger storage, and
  DEC-038 staged planning transaction in
  `docs/design/command-owner-redesign/decisions.md`.
- Joined CCFG-19 transaction and fault-model evidence in
  `docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`.
- Existing candidate `skill_contract.py` and `planning_state.py` behavior as
  implementation evidence only, not as accidental target topology.

## Deferred And Excluded

- Migrating stable or candidate `CURRENT.md`, `LEDGER.md`, dispatch, runway, or
  closeout documents to the new blocks.
- Integrating the new module into `planning_state.py`, `add-to-ledger`,
  `plan-batch`, `work-batch`, APR, Batch Runway, or the local program runner.
- Implementing CCFG-22 authoring guidance, CCFG-23 behavioral harnesses, or
  CCFG-24 through CCFG-29 ownership transfer and cutover work.
- Registering an installed feature, editing `codex-features.json`, installing
  the candidate, or switching the default generation.
- A global-ledger default, compatibility writer, prose-semantic fallback,
  canonical SQLite state, historical archive migration, or permanent legacy
  reader.
- Broad typing cleanup in `scripts/planning_state.py`.

## Suggested Slice Shape

1. Add all five planning artifact schemas, closed-world parsing/validation, and
   explicit read-only old-format compatibility.
2. Add revisioned CURRENT and ledger stores, `ledger-store/v1`, derived-index
   validation, receipts, and the per-finding-versus-global prototype.
3. Add revisioned dispatch/runway/closeout writes with immutable lineage and
   generation validation.
4. Add the selection-transaction schema, DEC-038 saga, full fault matrix, and
   changelog evidence.

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

Complete validated planning snapshot payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: b2a04a32d5871c96ebb5e93ccf4056a32f2db07b
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: b2a04a32d5871c96ebb5e93ccf4056a32f2db07b
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 3e54155964e92d3a4dced8268cc683baaab9be1c
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

The installed stable helper parsed the payload and validated the exact four
canonical planning paths plus the thirteen intended candidate paths and file
areas named by the runway. Planning performed no candidate write.

## Stop Conditions

- Stop if the selected CCFG-21 scope no longer matches this dispatch.
- Stop if the first execution-flight ready/blocked preflight does not return a
  fresh strict context for this selected scope.
- Stop if the candidate worktree is not clean before Slice 1 or contains changes
  outside the active slice allowlist.
- Stop if implementation duplicates structural facts between JSON Schema and
  procedural code or creates a second planning-contract owner module.
- Stop if `ledger-store/v1` chooses semantic intake, selection, merge, closeout,
  or successor outcomes instead of applying a caller decision.
- Stop if the per-finding prototype cannot preserve atomicity and projection
  equality; record a blocker rather than silently selecting a global block.
- Stop if any compatibility path can write old-format state, infer facts from
  prose, or read archived state as current.
- Stop if any slice mutates live planning artifacts, `planning_state.py`,
  command-owner skills, the manifest, installed Codex state, or a CCFG-22+
  owner surface.
- Stop closeout before selecting, refreshing, dispatching, or preparing a
  successor batch.
