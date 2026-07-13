# Live CCFG-18 Pre-Creation Amendment

## Amendment Boundary

This document records the live CCFG-18 pre-creation amendment after the accepted
design snapshot was imported into the candidate branch. It extends the live
candidate design; it does not alter the accepted snapshot or rewrite its
history.

```yaml
lineage:
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
  authoritative_base_commit: da5b97165eb8d8c9f809a64937bcc9d753032ee7
  ancestry_preserving_merge_commit: b044e3c348922663aa074638227aae8d2633cfe3
  candidate_branch: implementation/command-owner-redesign
controller:
  generation_role: stable
  toolchain_source_root: /home/alacasse/projects/codex-config
  codex_home: /home/alacasse/.codex
  canonical_state_mutation_allowed: true
  revision_binding: refreshed by validated strict execution context
roles:
  stable_repository:
    path: /home/alacasse/projects/codex-config
    role: stable toolchain source and canonical planning repository
  stable_planning_root:
    path: /home/alacasse/projects/codex-config/docs/plans
    role: only canonical planning mutation root
  candidate_repository:
    path: /home/alacasse/projects/codex-config-command-owner-redesign
    role: candidate design and implementation target
  candidate_codex_home:
    path: /home/alacasse/.codex-command-owner-redesign
    role: isolated candidate installation and fixture-only session home
temporary_cross_checkout_bridge:
  caller: stable plan and work control
  reason: create and control a separate candidate generation during self-hosted migration
  precreation_interface: cross-checkout-precreation/v1
  postcreation_interface: cross-checkout-context/v1
  allowed_scope: root, revision, generation, and write-scope enforcement only
  lifecycle_authority: none
  deletion_condition: CCFG-29 final integration
```

## Live Amendment

Strict `cross-checkout-context/v1` remains a post-creation contract: it requires
the candidate repository to exist at the declared implementation revision. It
must not be weakened or reinterpreted to authorize creation.

Before candidate creation, the stable controller uses the separate temporary
`cross-checkout-precreation/v1` interface. That interface binds the stable
generation and canonical planning revision to absent candidate paths, the
authoritative base, the implementation branch, the accepted design snapshot,
and the exact permitted creation roots. It grants no finding selection,
execution acceptance, review acceptance, commit, closeout, or successor
authority.

After the candidate repository and candidate `CODEX_HOME` are established,
execution must produce the versioned transition receipt and validate strict
`cross-checkout-context/v1` before any further candidate amendment or
implementation. Subsequent stable-controlled worker and reviewer handoffs use
fresh strict context and may write only within their explicitly validated
candidate scope.

The bridge remains temporary. CCFG-29 final integration owns its deletion after
the candidate is merged into authoritative `master`, the default toolchain is
rebound to that checkout, and no bridge caller remains.
