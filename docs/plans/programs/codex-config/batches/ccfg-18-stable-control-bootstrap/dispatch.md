# CCFG-18 Dispatch: Stable Control Bootstrap

## Batch Identity

- Batch ID: `ccfg-18-stable-control-bootstrap`
- Program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding:
  `CCFG-18. Establish Stable and Candidate Generations`
- Source finding note:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md`
- Bootstrap decisions:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-bootstrap-decisions.md`
- Accepted design snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Expected runway spec:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/runway.md`

## Selection Decision

Select CCFG-18 as the only dependency-free command-owner redesign finding, but
narrow this batch to the stable cross-checkout control bootstrap.

CCFG-18 is precise enough to keep one program identity, but not to execute as
one concrete runway. The accepted migration policy requires one controlling
toolchain generation per batch and forbids a real batch from crossing
generations. The stable bridge must be committed before a fresh stable session
can load it, so candidate clone and candidate-generation work must wait for a
later explicit `plan-batch` that resumes CCFG-18.

Closeout for this batch must mark CCFG-18 `Prepared`, not `Closed`, preserve the
remaining CCFG-18 scope, and stop without selecting CCFG-19.

## Preflight Evidence

```yaml
controlling_generation:
  role: stable
  loaded_commit: c0615f63060e07e79101089b5599c8eff05f77f8
stable_checkout:
  path: /home/alacasse/projects/codex-config
  branch: master
  clean: true
  tracks: origin/master
  contains_live_intake: true
installed_generation:
  default_codex_home: /home/alacasse/.codex
  repo_owned_links_resolve_to_stable_checkout: 24
  candidate_links: 0
planning_state:
  selected_dispatch: null
  queued_runway: null
  active_runway: null
  resumable_runner_state: false
future_project_values:
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  candidate_codex_home: /home/alacasse/.codex-command-owner-redesign
  candidate_paths_exist: false
accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
```

## Scope

- Batch kind: `migration`
- Owner seam: temporary `cross-checkout-context/v1` mechanism.
- Validation profile: `project-harness-production`.
- Density: `full-runway` because the batch changes stable control, installed
  routing, worker/reviewer context, and write-scope enforcement.
- Slice risk: all implementation slices are `migration`; no destructive or
  contract-narrowing slice is authorized.
- Mandatory destructive/contract-narrowing approval gate: none.

The temporary mechanism owns only:

- root-binding validation;
- repository-identity validation;
- write-scope validation;
- generation-identity capture; and
- the cross-repository receipt format.

It must not own intake, selection, scope shaping, runway design, execution
acceptance, closeout interpretation, or successor selection. Its deletion
condition is CCFG-29 final integration.

## Covered Work

- Implement the versioned `cross-checkout-context/v1` data contract and
  fail-closed validation in the stable checkout.
- Require explicit absolute toolchain, planning, implementation, and
  `CODEX_HOME` roots plus exact repository revisions and generation role.
- Reject root overlap, wrong repository identity, planning writes outside the
  canonical stable root, and implementation writes outside the declared
  implementation root before writes or delegation.
- Capture generation identity and distinguish planning and implementation
  revisions in cross-repository receipts.
- Wire the stable command/runtime control and registered worker/reviewer
  contracts to propagate the context without transferring workflow decisions.
- Expose the mechanism through existing manifest-driven installation wiring.
- Add focused positive and negative tests, release metadata, and changelog.
- Run installation dry-run only, then stop before loading or using the changed
  stable control for real work.

## Deferred Within CCFG-18

- Do not create the candidate clone or implementation branch.
- Do not merge or verify accepted design ancestry in a candidate clone.
- Do not create or install the candidate `CODEX_HOME`.
- Do not launch candidate fixture-only sessions.
- Do not prove worker/reviewer identity across real stable and candidate roots.
- Do not produce real cross-repository operation receipts.
- Do not rehearse pre-cutover rollback.

Those remain CCFG-18 work. A later fresh stable session must verify that all
installed links resolve to the new exact master commit, rerun planning-state
diagnostics, and invoke `plan-batch` again for the remaining CCFG-18 scope.

## Excluded

- Do not select or begin CCFG-19 through CCFG-29.
- Do not implement command-owner ownership transfer, `skill-contract/v1`,
  planning-format migration, APR/Batch Runway deletion, or default-generation
  switching.
- Do not redesign the architecture-program runner protocol.
- Do not modify `scripts/planning_state.py` or planning-state schemas.
- Do not use archived planning artifacts as executable authority.

## Suggested Slice Shape

1. Establish the `cross-checkout-context/v1` contract and fail-closed root and
   repository validation with focused tests.
2. Enforce write scopes, generation identity, and distinct cross-repository
   receipts with focused negative tests.
3. Wire stable consumers, agents, and manifest-driven installation; update
   release metadata; validate; and stop before reloading changed control.

## Stop Conditions

- Stop if selected, queued, active, or resumable state appears unexpectedly.
- Stop if any installed repo-owned link resolves outside the stable master
  checkout before execution.
- Stop if the mechanism acquires a semantic workflow decision.
- Stop if a stable helper resolves from candidate source.
- Stop if validation requires creating the candidate clone or candidate
  `CODEX_HOME` in this batch.
- Stop if changed stable control would be installed, reloaded, or used for real
  coordination in the same batch.
- Stop if closeout would mark CCFG-18 `Closed` or select CCFG-19.
