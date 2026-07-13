# Independent Review Resolution

## Scope

This note records the outcome of the independent review performed after the
command-owner redesign intake was added to `master`.

Reviewed design provenance:

```text
original snapshot: b3f31c44a1fc3287c33dd2955489f194afef66f6
live intake commit: 7356a3fd9d8d487be8562af11cad56170f300616
```

The review verdict was **go with required changes**. The intake remains valid and
must not be repeated. CCFG-18 remains the correct first item, but its live scope
must include executable two-generation control.

## Findings Resolved by Accepted Decisions

| Review concern | Resolution |
|---|---|
| Canonical planning and candidate code roots were conflated | DEC-027 defines toolchain, planning, and implementation roots. |
| Candidate branch lineage was undefined | DEC-028 starts implementation from latest master and merges accepted design history. |
| Rollback after candidate writes was undefined | DEC-029 defines pre-write and full-bundle post-write rollback. |
| Cutover and deletion ordering conflicted | DEC-030 makes CCFG-27 rehearsal-only and CCFG-28 deletion plus final switch. |
| `skill-authoring` waited for all planning schemas | DEC-031 creates complete core plus conditional planning reference. |
| Current-state representation was open | DEC-032 selects one canonical structured block in CURRENT.md. |
| Ledger representation was open | DEC-033 selects per-finding structured records with a derived index. |
| Post-cutover source authority was unclear | DEC-034 assigns final integration and rebinding to CCFG-29. |
| Cross-checkout routing risked becoming prompt convention | DEC-035 requires a narrow versioned temporary bridge. |
| Mutable branch links could change provenance | DEC-028 requires immutable authoritative URLs. |

## Findings Reduced but Requiring Implementation Proof

- stable helpers must resolve from the stable toolchain root, not candidate CWD;
- worker, reviewer, and runner child generations must be mechanically verified;
- installer must create complete generation-specific environments and switch one
  binding atomically;
- cutover checkpoint and rollback must be exercised;
- planning, commit, and closeout partial failures need idempotent recovery;
- deletion evidence needs a reproducible active/historical classifier;
- candidate sessions must be unable to mutate canonical planning state.

These are explicit CCFG-18, CCFG-23, CCFG-27, and CCFG-28 acceptance work.

## Deliberately Open for CCFG-19+

The following are not blockers to planning CCFG-18:

```text
OPEN-003  multi-artifact planning transaction
OPEN-004  one-commit-per-slice strictness
OPEN-005  exact slice-count rule
OPEN-006  final Python module split
OPEN-007  worker/reviewer naming
OPEN-008  prototype directory retention
```

Other required later decisions include:

- schema unknown-field and compatibility details;
- exact `ledger-store` idempotency and atomicity implementation;
- runner removal of successor-readiness fields and modes;
- old-format active-state completion or migration policy;
- deterministic limit of cosmetic-migration validation.

## Minimum Gate Before `plan-batch CCFG-18`

```yaml
manual:
  stable_checkout_on_master: true
  stable_checkout_clean_or_classified: true
  default_codex_home_resolves_to_stable_checkout: true
  required_skills_resolve_to_one_stable_commit: true
  selected: null
  queued: null
  active: null
  resumable_runner_state: false
  stable_checkout_path_known: true
  candidate_clone_path_known: true
  candidate_codex_home_path_known: true
  accepted_design_commit_known: true

documentary:
  CCFG_18_live_scope_amended: true
  CCFG_22_dependency_amended: true
  CCFG_27_and_CCFG_28_meanings_amended: true
  CCFG_29_final_integration_scope_amended: true
  authoritative_links_immutable: true
```

The clone, implementation branch, accepted design merge, candidate `CODEX_HOME`,
temporary bridge, mechanical fingerprints, and rollback rehearsal belong inside
CCFG-18.

## No Re-Intake Rule

The accepted amendments modify the existing CCFG-18 through CCFG-29 findings.
They do not create new findings, a second program, a batch map, dispatch, runway,
or selected batch.

## Readiness

After the live `master` amendments and local preflight, another broad architecture
review is not required before `plan-batch CCFG-18`.

A focused review is required after CCFG-18 because the root binding, generation
identity, cross-checkout receipts, and candidate write rejection will then be
observable rather than theoretical.
