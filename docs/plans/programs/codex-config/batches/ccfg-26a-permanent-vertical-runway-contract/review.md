# CCFG-26A Independent Planning Review

## Result

```yaml
interface: batch-plan-review/v1
verdict: clean
review_basis:
  selected_dispatch_sha256: e5ff62acc1c4ab81c5d4fabf544083d592e5bcb9de795be578287fdc33fc9327
  draft_sha256: aeec378e0c3261a01c616a7694af4a060680e27dae52399aeac37e9946bc05a5
  approvals_sha256: 054510f293c4076a7c165f65b006e8452e505e94d628cdfd6bd8751bf0347504
  evidence_packet_sha256: cc624cc536b72da0591dd3aabaf33e56b18ca25df4f98ba200f4175bdd2824c0
checks:
  currentness: pass
  selection: pass
  scope: pass
  proportionality: pass
  lineage: pass
  approval_scope: pass
  semantic_slices: pass
  vertical_slice: pass
  migration_matrix: pass
  validation_statuses: pass
  strict_context: pass
  stop_boundary: pass
corrections: []
blockers: []
implementation_started: false
```

The independent reviewer was invoked directly by the `plan-batch` command
owner as `/root/ccfg26a_exact_review`. It did not edit, select, queue, implement,
delegate, or run tests.

## Correction History

The first exact review returned `correction_required` for two related defects:

- retained migration routes did not mechanically require the retention reason;
  and
- the declared migrated `plan-batch` command and `planning-runway/v1` artifact
  callers had no dedicated migration-matrix rows.

The command owner corrected only those omissions without changing the finding,
selected batch, vertical sequence, implementation slice, approval scope,
validation profile, strict planning snapshot, or stop boundary. The reviewer
then re-read the corrected exact files and returned `clean`.

## Review Findings

- The superseded CCFG-26 runway is correctly retained as non-executable
  historical evidence rather than repaired or resumed.
- Splitting CCFG-26 into CCFG-26A through CCFG-26E is proportional because
  permanent planning, fresh execution flights, bounded recovery, finalization,
  and closeout have distinct owners, risks, validation, and rollback boundaries.
- CCFG-26A has one complete vertical scenario and one durable candidate result.
- Every declared migrated or retained caller has current owner, future owner,
  retention reason, status, and removal condition.
- The contract-narrowing approval is limited to permanent candidate vertical
  planning behavior from issue #60.
- Issues #59 and #61, COR-009 execution/closeout transfer, runner protocol
  decisions, physical deletion, bridge removal, and generation switching remain
  outside CCFG-26A.
- Focused validation and known-red statuses are explicit and final-range
  acceptance is not disguised as an implementation slice.
- Only CCFG-26A may queue. CCFG-26B through CCFG-26E remain unselected and a
  later explicit `plan-batch` invocation owns each successor decision.

## Mechanical Context

- Planning State before queue mutation: idle and valid; selected dispatch,
  queued batch, and active runway were `None`.
- Stable toolchain and canonical planning revision:
  `0ff5dea39cc80c5a313c5f70076d22b3d0973f62`.
- Candidate implementation revision:
  `89671eceb9103039e7e6660e73837827c167a3a1`.
- Installed helper:
  `/home/alacasse/.codex/scripts/cross_checkout_context.py`.
- Strict parse and exact planning/implementation upper write-scope validation:
  passed.
- Canonical planning root:
  `/home/alacasse/projects/codex-config/docs/plans`.

This review authorizes queue mutation for the exact dispatch, runway, approval,
and evidence hashes above only. Any later edit to `dispatch.md`, `runway.md`, or
the approval basis invalidates this review and requires a fresh independent
review before execution.

## Bounded Planning Amendment Review Inputs

The original clean review, its hashes, and its correction history above remain
unaltered pre-amendment planning evidence at stable commit
`db56018c96286f2a6d0363cd9c2a0d7e1468ded3`. They do not cover the amended
dispatch or runway. The following exact inputs require a fresh independent
review before execution.

<!-- bounded-amendment-approval-basis:start -->
```yaml
approval_basis:
  finding: CCFG-26
  contract: COR-009
  selected_batch: ccfg-26a-permanent-vertical-runway-contract
  authority:
    - GitHub issue #60
    - CCFG-26 canonical ledger row
    - explicit bounded planning amendment request
  approved_behavior: candidate planning permanently enforces and proves the exact migration-slice vertical contract for eventual integration
  slice_risk: migration
  approval_scope_unchanged: true
  excluded:
    - canonical planning authority before CCFG-29
    - issue #59 or issue #61 implementation
    - execution, recovery, finalization, closeout, or reconciliation ownership
    - new artifact identity, queue path, transaction, store, wrapper, or persistent draft
    - candidate implementation during this amendment
    - successor selection or planning
```
<!-- bounded-amendment-approval-basis:end -->

<!-- bounded-amendment-evidence-packet:start -->
```yaml
evidence_packet:
  pre_amendment_planning_commit: db56018c96286f2a6d0363cd9c2a0d7e1468ded3
  pre_amendment_dispatch_sha256: e5ff62acc1c4ab81c5d4fabf544083d592e5bcb9de795be578287fdc33fc9327
  pre_amendment_runway_sha256: aeec378e0c3261a01c616a7694af4a060680e27dae52399aeac37e9946bc05a5
  pre_amendment_review_sha256: 928bf180f85a5d88d85d6101f4305033e02471c2369712a5203a51e12f196d86
  canonical_state:
    selected_dispatch: null
    queued_batch: docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/runway.md
    active_runway: null
    later_children: unselected
  immutable_planning_snapshot:
    toolchain_commit: 0ff5dea39cc80c5a313c5f70076d22b3d0973f62
    canonical_planning_commit_before: 0ff5dea39cc80c5a313c5f70076d22b3d0973f62
    implementation_commit_before: 89671eceb9103039e7e6660e73837827c167a3a1
  canonical_planning_path_until_integration: stable plan-batch plus temporary CCFG-34 repository policy
  candidate_authority_before_ccfg_29: false
  implementation_started: false
```
<!-- bounded-amendment-evidence-packet:end -->

## Bounded Planning Amendment Review Result

The fresh independent amendment review first returned `correction_required` on
dispatch SHA-256
`bc42f71ba8802313ce9ae8db3cab92a1c1a5fc65add53599938feee65040364a`,
runway SHA-256
`ee9ed6128f921c93991885b029db20157495c434368ec3677d7af94ce06af921`,
and ledger SHA-256
`09aad0e5734057721564fdfd73bacadd72f85e42eaa23478b0828ab93fb1033c`.
It found one stale immediate-post-CCFG-34 ledger sentence and required the
`ownership_coexistence` value domain to be exhaustive in both planning
artifacts. Only those findings were corrected; the approval basis, evidence
packet, `CURRENT.md`, selected batch, slice, scope, validation, baseline, and
stop boundaries did not change.

The same read-only reviewer then independently recomputed and reviewed the
corrected exact bytes:

```yaml
interface: batch-plan-review/v1
verdict: clean
review_basis:
  dispatch_sha256: 77fa4f57ee48275ffceade3485cc16d1798ebcd1e6a428266fa1ab5ac6cdea88
  runway_sha256: e1e06bb3a14cab30b9bc49ae7ca339302eed75042b3717e4873207a0d8765e9f
  approval_basis_sha256: d055e4baa5c29b1d2a3dd430d340ce63971d4dd3a228e9eae17c9a3994e1f613
  evidence_packet_sha256: 728c9219298ec5e6e4a5b4bdd1607a5bddd58967569c2d0ed23cc3c6fd00a4a4
  current_sha256: 6b1e20b6b1d50800bb8e5e11124457a0e27edc45c3d807d40d9ef4fc855c0081
  ledger_sha256: fa2ff2e5add000d1f899ffc857bbecbee00f3ecaef11e665d2e3b249e32765d1
checks:
  currentness: pass
  selection: pass
  scope: pass
  proportionality: pass
  lineage: pass
  approval_scope: pass
  authority_boundary: pass
  applicability_predicate: pass
  vertical_slice: pass
  migration_matrix: pass
  future_test_scenarios: pass
  validation_statuses: pass
  strict_context: pass
  stop_boundary: pass
  prior_review_preservation: pass
implementation_started: false
corrections: []
blockers: []
```

The independent reviewer was invoked as `/root/ccfg26a_amendment_review`. It
did not edit, select, queue, implement, invoke `work-batch`, commit, or delegate.
The clean result covers only this bounded amendment and authorizes no successor
selection or candidate implementation outside the unchanged CCFG-26A runway.
