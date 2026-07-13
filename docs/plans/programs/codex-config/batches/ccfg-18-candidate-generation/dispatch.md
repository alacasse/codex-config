# CCFG-18 Candidate Generation Dispatch

## Batch Identity

- Batch ID: `ccfg-18-candidate-generation`
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-18, Establish Stable and Candidate Generations
- Dispatch state: queued through the co-located concrete runway
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/runway.md`
- Successor selected: no

## Selection Decision

Select the remaining candidate-generation scope of CCFG-18 now that the stable
pre-creation feature set is committed, installed, linked to the authoritative
stable checkout, and loaded for a fresh planning pass.

The row is suitable for one bounded batch because the live amendment now names
the exact absent roots, stable controller, authoritative base revision, accepted
design snapshot, implementation branch, transition contract, acceptance
evidence, and stop boundaries. The batch combines two migration slices with one
evidence-only isolation and rollback slice; it does not absorb CCFG-19.

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
stable_control:
  checkout: /home/alacasse/projects/codex-config
  branch: master
  commit: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  origin_master: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  worktree: clean
  codex_home: /home/alacasse/.codex
  installed_versions_match: true
  installed_links_resolve_to_stable_checkout: true
candidate_intent:
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_target_state: absent
  candidate_codex_home: /home/alacasse/.codex-command-owner-redesign
  candidate_codex_home_state: absent
  base_repository: alacasse/codex-config
  base_commit: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  implementation_branch: implementation/command-owner-redesign
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
installed_helper: /home/alacasse/.codex/scripts/cross_checkout_context.py
precreation_payload_validation: passed
authorized_creation_targets_validation: passed
```

The stable helper resolved to
`/home/alacasse/projects/codex-config/scripts/cross_checkout_context.py` before
validation. Planning created neither candidate root.

## Batch Kind And Risk

- Batch kind: `mixed-risk`.
- Migration slices: Slice 1 and Slice 2.
- Evidence-only slice: Slice 3.
- Destructive cleanup: forbidden.
- Contract narrowing: forbidden.
- Destructive or contract-narrowing approval gates: none, because neither risk
  class is authorized.
- Runtime authority: creation is limited to the two exact roots accepted by
  `cross-checkout-precreation/v1`. Network, filesystem, and cost-bearing fresh
  session approvals remain subject to the execution environment.

## Goal

Establish a separate candidate repository and candidate `CODEX_HOME` under the
installed stable pre-creation contract, preserve authoritative master and
accepted-design ancestry on `implementation/command-owner-redesign`, transition
immediately to strict `cross-checkout-context/v1`, install and fingerprint the
candidate generation, then prove fixture-only candidate behavior, canonical
planning write rejection, quiescence, and pre-cutover rollback.

## Owner Seam And Validation Class

- Owner seam: stable cross-checkout control over candidate repository and
  generation establishment.
- Controlling generation before cutover: stable.
- Canonical planning owner: stable repository at
  `/home/alacasse/projects/codex-config/docs/plans`.
- Implementation owner after creation: candidate repository at
  `/home/alacasse/projects/codex-config-command-owner-redesign`.
- Validation profile: `project-harness-production` with explicit operational
  cross-checkout and fresh-session overrides in the runway.
- Density: `full-runway`; repository creation, installer lifecycle, strict
  identity transition, sandbox boundaries, and real session validation make a
  lean handoff unsafe.

## Covered Work

- Revalidate the complete `cross-checkout-precreation/v1` payload with the
  installed stable helper before creation.
- Pre-review the deterministic master-plus-design merge result while both
  candidate roots remain absent.
- Create only the exact candidate repository and candidate `CODEX_HOME` roots.
- Create `implementation/command-owner-redesign` from authoritative master at
  `da5b97165eb8d8c9f809a64937bcc9d753032ee7`.
- Merge the accepted design history ending at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c` with preserved ancestry and verify
  the imported design tree before live amendments.
- Build and preserve the helper-produced transition receipt, then validate
  strict `cross-checkout-context/v1` before any further implementation.
- Apply the live pre-creation amendment explicitly to the candidate design tree
  without rewriting the frozen accepted snapshot.
- Install all manifest-owned features into the separate candidate `CODEX_HOME`
  from the candidate repository and fingerprint candidate links and identity.
- Prove stable workers and reviewers remain stable-controlled while candidate
  trials use the candidate generation.
- Run a fresh candidate fixture-only session, reject canonical planning
  mutation, inventory old selected/queued/active/resumable state, and prove
  pre-cutover return to the untouched stable generation.
- Close CCFG-18 only from complete evidence and stop without selecting CCFG-19.

## Deferred And Excluded

- CCFG-19 through CCFG-29 remain unselected.
- No command-owner ownership transfer or implementation begins.
- No `skill-contract/v1`, planning schema, or behavioral harness program work.
- No APR or Batch Runway deletion.
- No default `CODEX_HOME` switch.
- No candidate-controlled canonical planning write.
- No candidate session controls a real batch before cutover.
- No design history rewrite, branch deletion, or candidate retirement.
- No permanent cross-checkout owner; CCFG-29 remains the deletion condition.

## Suggested Slice Shape

1. Establish the exact candidate roots, authoritative branch lineage, accepted
   design merge, and validated pre-creation-to-strict transition.
2. Apply the live amendment, install the candidate feature set, and prove
   stable/candidate generation fingerprints and strict cross-repository scope.
3. Prove fresh candidate fixture-only behavior, canonical-write rejection,
   old-generation quiescence, and pre-cutover stable rollback; then close only
   CCFG-18.

## Stop Conditions

- Stop if either candidate root exists before Slice 1 creation authority is
  revalidated.
- Stop if stable `HEAD`, `origin/master`, installed versions, installed links,
  active `CODEX_HOME`, or the complete payload differs from the gate evidence.
- Stop if stable planning artifacts are committed before the fixed pre-creation
  payload and transition are validated; that would stale the pinned revision.
- Stop if the merge result cannot preserve both authoritative master and
  accepted-design ancestry or cannot be reviewed before the merge commit.
- Stop after candidate creation unless the helper produces a green transition
  receipt and strict context.
- Stop if any worker, reviewer, helper, schema, or reference resolves from the
  wrong generation.
- Stop if candidate execution can write canonical planning state.
- Stop if credentials for a fresh candidate session would require copying or
  linking secrets without explicit user authorization.
- Stop if the sandbox cannot distinguish canonical planning and candidate
  implementation roots or cannot confine fixture writes.
- Stop if execution would switch the default generation, start CCFG-19, or
  broaden into command-owner migration.
