# CCFG-35 Bounded Proof-Lane Amendment

## Status And Precedence

- Status: bounded planning correction; implementation has not started.
- Applies to: queued batch `ccfg-35-master-planner-review-hardening` only.
- Batch identity, queue path, master-only target, and two-slice shape: unchanged.
- Authority: the user's 2026-07-20 request to apply the corrections from the
  independent `revise` review of the queued plan.
- Precedence: the amended source finding, dispatch, and runway plus this
  document supersede conflicting live-evaluation, cost, retry, receipt, and
  verdict language in the historical planning review.
- Execution gate: no work may begin until `amendment-review.md` records a clean
  verdict for the exact amended dispatch/runway hashes.
- Successor effect: none.

The pre-amendment planning evidence remains historical:

```yaml
pre_amendment_evidence:
  master_commit: e31256758f3d7b1d01309332c2e23e24e7dd7392
  source_finding_sha256: 02d18c478cccdd0708cbd19789e535368327e09f8f8cc6128f42a79e4cef0310
  dispatch_sha256: f8f5e8535608f9d50521dd205d1ae726183738ae3e27af30b31701b316881aed
  runway_sha256: 3acef09e943c9aa1d73cf5027859379d8f7bef1be6757d7785aed8ccb216379a
  review_sha256: c5fdd35c7fd5924d98d034e00d759bfdafa1c3a1b1a95eb2802185537e5276c3
  review_disposition: historical_only
  reason: the clean verdict required an unmeasured per-scenario live lane and cannot authorize execution after this correction
implementation_started: false
```

## Correction

The prior runway required a fresh planner and fresh reviewer for each of ten
scenarios plus a Slice 1 smoke pair: at least 22 live semantic invocations. It
did not measure that lane before making it mandatory, did not define a retry
policy, did not explain when same-commit receipts could be reused, and left
three verdict vocabularies without one canonical queue mapping.

That design is withdrawn. It is replaced by:

1. one planner invocation over two isolated smoke packets and one different
   reviewer invocation over both results after Slice 1;
2. one planner invocation over ten isolated final packets and one different
   reviewer invocation over all ten results after Slice 2;
3. separate hashes, evidence, dispositions, and queue application for every
   packet despite the batched semantic calls;
4. a measured progression gate before Slice 2; and
5. exact-commit validation receipts reused until a named material input
   invalidates them.

This reduces the normal semantic-evaluation count from 22 to 4 without reducing
the ten scenario decisions or planner/reviewer independence. It authorizes no
permanent evaluation infrastructure and changes no reusable runtime behavior by
itself.

## Measured Plan-Time Baseline

At master commit `e31256758f3d7b1d01309332c2e23e24e7dd7392` on 2026-07-20:

| Gate | Result | Pytest time | Wall | User | System | Max RSS |
|---|---|---:|---:|---:|---:|---:|
| three required-green planning contract files | 28 passed | 0.07s | 0.29s | 0.25s | 0.04s | 38,368 KiB |
| two Slice 1-owned manifest cases | 2 expected failures | 0.04s | 0.23s | 0.20s | 0.02s | 41,824 KiB |

These measurements bound current deterministic test cost; they do not estimate
model latency or tokens. The Slice 1 smoke must supply that missing evidence.

Historical proportionality evidence comes from
`../ccfg-23-behavioral-scenario-harness/execution-retrospective.md`: its final
suite took 814.32 seconds, ran 35 whole-catalog evaluations, implied about
41,125 subprocess executions, and documented direct multiplication from
unchanged reruns. Its recommendations to batch executions and reuse receipts by
exact commit are binding constraints for this amendment.

## Slice 1 Measurement And Progression Gate

After the accepted Slice 1 commit and implementation review, the coordinator
must run one two-packet planner batch and one different two-packet reviewer
batch. `smoke-cost-receipt.md` must bind:

- accepted Slice 1 commit and exact planner/support source hashes;
- ordered packet manifest hash and each packet/input hash;
- start/end timestamps, wall seconds, retries and reasons for both invocations;
- serialized input/output byte counts and output digests;
- actual model and effort plus input/output/total tokens when exposed, or
  `unavailable` when the host does not expose them;
- the two separately applied queue outcomes;
- the rejected 20-call final alternative versus the proposed 2-call final lane;
  and
- the ten-packet estimate, formula, assumptions, and range.

A separate read-only cost-gate reviewer must compare the measured batched smoke
with the rejected per-scenario shape and the CCFG-23 evidence. It returns only
`clean`, `correction_required`, or `blocked`. Slice 2 is unauthorized until that
review is clean and the user explicitly approves the reported estimate. The
initial `work-batch` request cannot pre-approve a measurement that does not yet
exist.

## Retry And Call-Budget Policy

- Normal semantic budget: four calls total, two smoke and two final.
- Maximum transport retry: one per batched semantic invocation, recorded with
  reason, duration, and partial usage.
- Semantic `correct`, `revise`, or `block` is not retryable as transport.
- Worker or reviewer correction loops must be separately counted; they do not
  expand the four-call semantic lane.
- An unavailable invocation after its transport retry blocks progression.
- Any proposed per-scenario invocation or expanded semantic budget requires a
  new explicit user-approved amendment and fresh independent review.

## Canonical Decision Mapping

```text
planner:  plan | correct | block
reviewer: approve | revise | block
binding:  valid | invalid
queue:    authorized | not_authorized
aggregate review: clean | correction_required | blocked
```

Queue authorization is the exact conjunction:

```text
planner=plan
AND reviewer=approve
AND binding=valid
AND required evidence is present
AND reviewed input/draft hashes still match
=> queue=authorized
```

Every other or missing combination maps to `not_authorized`. For aggregate
acceptance, `blocked` takes precedence for unavailable or contradictory facts;
otherwise an unexpected correctable result maps to `correction_required`.
`clean` means all nine negatives are not authorized for their intended reason
and only the positive control is authorized. No synonym or aggregate verdict
may bypass this mapping.

## Exact-Commit Receipt Reuse

A reusable validation receipt binds command, exact commit, relevant source and
test hashes, input manifest, dependency/configuration/environment identity,
result, duration, and output digest. Later same-commit reviewers consume it
instead of rerunning the gate.

Rerun is required only after a material commit/blob, command/selector,
dependency, installed version, configuration, environment, scenario input, or
expected-behavior change, or when the receipt is missing or malformed. The
invalidating fact must be recorded. Independent semantic reconstruction remains
required; mechanical receipt reuse is not planner self-attestation.

## Preserved Scope And Stop Boundary

- Both original vertical slices remain unchanged in purpose and dependency.
- Implementation and final accepted provenance remain master-only.
- Candidate checkout/home remain evidence-only and unwritable.
- All ten scenarios and all installed-master closeout proofs remain required.
- No CCFG-26 or successor work is selected.
- This is planning-only. Stop after the exact amendment receives fresh
  independent review and canonical queue references are reconciled.
