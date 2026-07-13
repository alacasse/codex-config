# CCFG-18 Dispatch: Stable Pre-Creation Support

## Batch Identity

- Batch ID: `ccfg-18-stable-precreation-support`
- Program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding:
  `CCFG-18. Establish Stable and Candidate Generations`
- Source finding note:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md`
- Bootstrap decisions:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-bootstrap-decisions.md`
- Prior completed batch:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/closeout.md`
- Accepted design snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Expected runway spec:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/runway.md`

## Selection Decision

Select only the amended, bounded stable-support portion of CCFG-18. The prior
stable bootstrap completed `cross-checkout-context/v1`, but that strict
post-creation contract cannot validate an implementation repository that does
not exist yet. The accepted live amendment resolves the circularity with a
separate temporary `cross-checkout-precreation/v1` interface.

This batch is a single-root stable-control batch. It implements and validates
the pre-creation interface in the authoritative stable checkout, preserves the
strict post-creation contract unchanged, and stops before creating either
candidate path. CCFG-18 remains the finding identity; CCFG-19 is deferred.

## Preflight Evidence

```yaml
controlling_generation:
  role: stable
  loaded_commit: 20b792888481dd9db1e3fa4b90831500eda509f1
stable_checkout:
  path: /home/alacasse/projects/codex-config
  branch: master
  origin: https://github.com/alacasse/codex-config.git
installed_generation:
  default_codex_home: /home/alacasse/.codex
  feature_versions_match_manifest: true
  repo_owned_links_resolve_to_stable_checkout: true
planning_state:
  current: passed
  validate: passed
  selected_dispatch: null
  queued_runway: null
  active_runway: null
candidate_intent:
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_target_state: absent
  candidate_codex_home: /home/alacasse/.codex-command-owner-redesign
  candidate_codex_home_state: absent
accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
```

The worktree already contains classified, user-owned CCFG-18 amendment edits in
program `CURRENT.md`, `LEDGER.md`, and the two source finding notes. Preserve
those edits. Workers must not rewrite or stage those files; the coordinator may
update active batch state and same-batch closeout fields only.

## Scope

- Batch kind: `migration`.
- Owner seam: the temporary cross-checkout validation owner in
  `scripts/cross_checkout_context.py` plus its reusable consumer contracts.
- Validation profile: `project-harness-production`.
- Density: `full-runway` because the batch changes installed stable control,
  pre-write authority, delegated identity, and transition evidence.
- Slice risk: all implementation slices are `migration`; no destructive or
  contract-narrowing slice is authorized.
- Mandatory destructive/contract-narrowing approval gate: none.

## Covered Work

- Add a separate `cross-checkout-precreation/v1` data contract and fail-closed
  validator without weakening `cross-checkout-context/v1`.
- Bind the validated stable toolchain, canonical planning repository and
  revision, stable `CODEX_HOME`, absent intended candidate paths,
  authoritative base commit, implementation branch, accepted design snapshot,
  and exact creation authority.
- Reject relative targets, protected-root overlap, unexpected existing
  candidate state, ambiguous repository identity, revision drift, and creation
  authority broader than the two exact intended targets.
- Define versioned transition evidence that can later bind successful candidate
  lineage and environment creation to the existing strict post-creation
  context before further implementation.
- Wire `plan-batch`, `work-batch`, Batch Runway, worker, and reviewer contracts
  to consume the installed mechanical owner without acquiring workflow
  lifecycle authority.
- Add focused helper, consumer, agent-contract, manifest, and installation
  tests; update affected feature versions and `CHANGELOG.md`.
- Run installation dry-run only, then stop before installing or loading the
  changed stable generation.

## Deferred Within CCFG-18

- Do not create or clone the candidate repository.
- Do not create the candidate implementation branch or merge accepted design
  history.
- Do not create or install the candidate `CODEX_HOME`.
- Do not emit a real transition receipt against the intended candidate paths.
- Do not validate a real strict cross-checkout payload for the absent candidate.
- Do not launch candidate fixture-only sessions, prove real cross-generation
  worker/reviewer identity, or rehearse rollback.

After closeout, the changed stable feature set must be installed and loaded in
a fresh stable session. Only a later explicit `plan-batch CCFG-18` may plan the
remaining candidate-creation scope.

## Excluded

- Do not select or begin CCFG-19 through CCFG-29.
- Do not implement command-owner ownership transfer, `skill-contract/v1`,
  planning-format migration, APR/Batch Runway deletion, or cutover.
- Do not modify `scripts/planning_state.py` or planning-state schemas.
- Do not add project-specific paths, identities, commands, or cache locations
  to reusable skills or reusable reference contracts.
- Do not use archived planning artifacts as executable authority.

## Suggested Slice Shape

1. Extend the existing mechanical owner with the pre-creation contract,
   fail-closed validation, and versioned transition evidence; add focused
   behavior tests while preserving strict-context regressions.
2. Add the reusable pre-creation consumer contract and propagate it through
   command/runtime and registered-agent contracts with focused contract tests.
3. Update manifest expectations, affected feature versions, and release
   documentation; run installation dry-run and final validation, then stop.

## Stop Conditions

- Stop if implementation weakens or reinterprets strict
  `cross-checkout-context/v1` repository or revision validation.
- Stop if this batch would create or write either intended candidate path.
- Stop if the pre-creation mechanism gains intake, selection, scope, execution
  acceptance, closeout, or successor authority.
- Stop if a reusable contract hard-codes this repository's local paths or
  CCFG-specific policy.
- Stop if installer changes beyond existing manifest-driven links are needed.
- Stop if changed stable control would be installed, reloaded, or consumed for
  real coordination in this batch.
- Stop if closeout would mark CCFG-18 `Closed`, select CCFG-19, or prepare a
  successor dispatch or runway.
