# CCFG-23 Execution Retrospective

## Purpose

This report explains why `ccfg-23-behavioral-scenario-harness` consumed many
hours and substantial model context. It records the implementation timeline,
review/fix loops, orchestration and tooling retries, validation cost, and the
specific design that makes the final focused test suite take more than 13
minutes.

The evidence comes from the batch dispatch, runway, completed-slice receipts,
closeout, stable and candidate Git history, coordinator-observed command
results, and a post-closeout read-only timing investigation. Exact model-token
usage was not persisted by the batch runner, so this report does not invent a
token total.

## Executive Summary

- The evidenced implementation window ran from the first candidate commit at
  10:50:55 to stable closeout at 17:29:25 on 2026-07-15: **6 hours, 38 minutes,
  30 seconds**.
- The candidate range added **9,154 lines across 16 files**. The main harness,
  catalog, adapters, and four test modules total 8,364 lines at closeout.
- The durable batch artifacts themselves total 1,799 lines: 284-line dispatch,
  981-line runway, 354-line completed-slice archive, and 180-line closeout.
- Four semantic slices each went through worker, validation, test-quality, and
  independent-review loops. Slices 2 and 4 required same-slice runway
  amendments before execution could proceed honestly.
- The final four-module scenario suite passed **123 tests in 814.32 seconds
  (13:34)**. This is not ordinary pytest overhead. The suite starts nested
  pytest to prove that its own acceptance-evidence tests passed.
- One observed report launches 13 separate pytest processes and then evaluates
  all 69 scenarios again. A representative observed report measured **92.20
  seconds wall time**.
- One CLI determinism test starts the observed report four times. Together with
  the final report test and final CLI report test, those six report builds
  account for roughly **9:13**, about 68% of the full 13:34 suite.
- The suite performs **35 complete catalog evaluations**. One instrumented
  evaluation launched 1,175 subprocesses, implying roughly **41,125 process
  executions** per focused run—approximately 39,795 Git commands and 1,330
  candidate-Python commands.
- The remaining time comes primarily from repeated full-catalog evaluation,
  disposable Git repositories, Planning State commands, child Python
  processes, installer/switch/rollback fixtures, and negative-runtime tests.
- Final closeout was correct: CCFG-23 is closed, both checkouts were clean, and
  no successor was selected. The cost problem is test and orchestration shape,
  not a failed outcome.

## Scope And Outcome

The batch produced a non-installed, topology-independent scenario harness that
proves 69 scenarios across 31 immutable contracts and 17 required families. It
emits the six COR-006 keys and six migration aliases from observed runtime
evidence while keeping production ownership transfer, real cutover, default
generation switching, and bridge deletion out of scope.

Candidate commits:

| Time | Commit | Outcome |
|---|---|---|
| 10:50:55 | `a5971ca` | Scenario schema, catalog contract, harness owner, and Slice 1 tests |
| 12:05:13 | `58cdf2d` | Workflow and planning-quality scenario bindings |
| 13:18:32 | `a2f3aa2` | Planning currentness and protected-handoff evidence |
| 17:00:40 | `0c1844c` | Disposable cutover and aggregate evidence |
| 17:22:27 | `e8d07a7` | One-line deferred-import lint annotation |

Stable planning commits:

| Time | Commit | Outcome |
|---|---|---|
| 10:53:25 | `43ec4c4` | Slice 1 receipt |
| 11:14:34 | `a32457f` | Slice 2 progression-aware test-boundary amendment |
| 12:06:51 | `2e18d76` | Slice 2 receipt |
| 13:20:27 | `db1a517` | Slice 3 receipt |
| 13:23:49 | `47b2045` | Slice 4 aggregate-report capability amendment |
| 13:27:32 | `6cc8bb0` | Slice 4 progression-gate amendment |
| 13:43:01 | `1fa0fbb` | Slice 4 prior-slice-gate amendment |
| 17:29:25 | `3580d78` | Same-batch closeout and program reconciliation |

The longest interval was the final slice: 3 hours 17 minutes 39 seconds from
the last required runway amendment to the Slice 4 implementation commit. That
interval contained the largest implementation surface, repeated acceptance
review, and the newly expensive report/test path.

## What Happened In Each Slice

### Slice 1: Contract And Harness

The first slice introduced the closed-world schema, the catalog validator,
adapter loading, deterministic reports, and honest unavailable bindings.

Review/fix loop:

- Test-quality review found nondeterministic CLI behavior and observation-input
  purity gaps.
- Independent review found a nested expectation-mutation false green and a
  forbidden-topology separator bypass.
- The worker fixed the bounded findings; repeat test-quality and runway review
  were clean.

Orchestration retry:

- The coordinator and worker each initially loaded the Python 3.14 dataclass
  helper dynamically without registering the module in `sys.modules`.
- Both attempts failed before validation, writes, or accepted delegation.
- The loader was corrected, and strict generation/root identity then matched.

### Slice 2: Workflow And Planning Quality

The second slice bound intake, planning, execution, recovery, closeout, and
planning-quality scenarios through fixture-owned collaborators.

Runway amendment:

- The first focused validation showed that Slice 1's intentionally transitional
  “all live bindings unavailable” assertion could not remain true after Slice 2
  legitimately bound scenarios.
- The stable runway was amended to use progression-aware honesty checks rather
  than weakening the acceptance boundary.

Review/fix loop:

- Test-quality review found self-certified planning/execution evidence.
- Final review found generic role labels that did not prove the required
  independent planner/reviewer ownership.
- The fixes introduced separately injected `batch_planner` and
  `batch_plan_reviewer` behavior and artifact-backed evidence.
- Repeat test-quality, import-topology, and runway reviews were clean.

Support-result retry:

- The first test-quality result nested strict identity under
  `execution_context` instead of returning the required flat result shape.
- The coordinator rejected it, renewed the live lease, and accepted only the
  corrected result. No code or acceptance decision used the malformed result.

### Slice 3: Currentness And Protected Handoffs

The third slice added Planning State currentness, material Git integrity, fresh
worker/reviewer leases, exact scopes, receipts, commit ranges, reconciliation,
and workspace-write evidence.

Review/fix loop:

- Test-quality review found four false-green classes: movement-boundary
  confusion, self-certification, incomplete exact-write evidence, and copied
  checkpoint labels.
- Independent review found worker-lease reuse at the reviewer handoff and a
  missing schema-valid but semantically stale Planning State case.
- Bounded fixes and repeat test-quality, import-topology, and runway reviews
  were clean.

### Slice 4: Disposable Cutover And Aggregate Evidence

Slice 4 was the largest and slowest slice. It added synthetic generation
lineage, installer failure behavior, atomic switch/rollback, quiescence,
synthetic bridge absence, historical-state non-authority, and runtime-backed
aggregate evidence.

Pre-edit stops and amendments:

- The implementation correctly stopped when the original runway did not
  authorize a generic aggregate-evidence report capability.
- A second amendment made the final progression gate explicit.
- A third amendment allowed only the minimum prior-slice assertion changes
  needed for final all-green state.
- These were committed as three stable planning changes before implementation
  continued.

Validation/review:

- Slice review, import-topology review, delta-only test-quality review, final
  exact-range review, and final exact-range test-quality review were clean.
- The final 123-test scenario run took 814.32 seconds.
- The worker's final packaging/handoff was slow enough to appear stuck. The
  coordinator interrupted it once and took over the remaining gates; the
  committed implementation was intact.

Final-gate retries:

- A parallel validation tool result exceeded the context/output limit. The
  coordinator reran smaller commands individually to recover exact evidence.
- The first focused-manifest filter matched no tests (`21 deselected`, pytest
  exit 5). The exact runway-owned `-k` selector was restored and passed 4 tests
  plus 34 subtests.
- Ruff first failed while trying to write `.ruff_cache` in the read-only
  candidate checkout. Re-running with `--no-cache` exposed the real lint result.
- Ruff then found `E402` on the deliberate deferred import after fixture-local
  path bootstrapping. A worker added one local `# noqa: E402`, Ruff and import
  sanity passed, independent review was clean, and `e8d07a7` recorded the fix.
- The first closeout receipt payload used an incorrectly guessed full SHA for
  `e8d07a7`. The strict helper failed closed with the observed HEAD. The payload
  was regenerated with the exact SHA and passed.

Closeout editing retries:

- Initial reference commands used the wrong CCFG-22 batch-directory name and
  a program-level `completed-slices.md` path that does not exist. Repository
  search recovered the canonical locations.
- The first completed-slices patch matched a repeated JSON-fence boundary and
  inserted Slice 4 before Slice 2. A second move placed it before Slice 3, and
  one subsequent patch failed verification because its context was stale.
- The final patch used the unique Slice 3 commit receipt as its anchor. The
  archive then had the correct Slice 1→4 order.
- Planning State `current` and `validate`, independent closeout review, tracked
  and untracked whitespace checks, and both worktree status checks were clean
  before commit.

## Error And Retry Inventory

| Class | Count/evidence | Effect | Resolution |
|---|---|---|---|
| Dynamic helper import bootstrap | 2 failed attempts | No writes; delayed Slice 1 handoff | Register dynamic module before dataclass execution |
| Same-slice runway amendments | 1 for Slice 2, 3 for Slice 4 | Added planning/review cycles but preserved honest scope | Commit narrow amendments before further implementation |
| Actionable review loops | Every slice; multiple findings in Slices 1–3 | Rework and repeated context/test/review cost | Bounded worker fixes followed by clean repeat reviews |
| Malformed support result | 1 | Result rejected; lease renewed | Require exact result-contract identity shape |
| Slow worker handoff | 1 interruption | Coordinator wait and context recovery | Coordinator took over final gates |
| Tool-output truncation | 1 material final-validation occurrence | Exact command results unavailable | Rerun smaller commands independently |
| Wrong pytest selector | 1 | No tests collected; exit 5 | Use exact runway selector |
| Ruff cache write failure | 1 | Lint did not run | Use `ruff --no-cache` in read-only checkout |
| Actual Ruff defect | 1 | Blocked closeout | One-line local suppression plus review and commit |
| Incorrect receipt SHA | 1 | Strict context rejected payload | Use helper-reported exact HEAD |
| Closeout patch placement/verification | 2 wrong placements, 1 rejected patch | Documentation-only rework | Anchor on unique Slice 3 receipt |
| Known-red manifest | 3 expected failures | Diagnostic only; no scope expansion | Verify exact same failures, 18 passes, 202 subtests |

The review findings were valuable defects, not wasted retries: they prevented
several plausible false-green acceptance paths. The avoidable waste came from
re-reading/re-sending large context, rerunning unchanged slow evidence, command
selection/cache mistakes, output truncation, and brittle repeated-text patch
anchors.

## Validation Performed

| Gate | Result | Approximate wall time |
|---|---|---:|
| Four focused scenario modules | 123 passed | 814.32s |
| Catalog validate CLI | 69 scenarios valid | Included in final gate; individually fast relative to observed report |
| Observed report CLI | 69 scenarios, 31 contracts, 17 families, 6 keys and 6 aliases green | Approximately 92s per invocation |
| Planning/state/strict-context/agent baseline | 309 passed, 187 subtests | 48.00s |
| Pre-creation isolation | 32 passed, 39 subtests | 2.16s |
| Focused manifest subset | 4 passed, 34 subtests | 0.02s |
| Full manifest known-red diagnostic | 3 expected failures, 18 passed, 202 subtests | 0.09s |
| Ruff, BasedPyright, diff checks | Green; 0 type errors, 5 environment warnings | Seconds |
| Stable/candidate installer status and dry-run | Read-only and generation-owned | Seconds |

The comparison matters: the 309-test baseline takes 48 seconds, while the 123
new scenario tests take 814 seconds. Test count is not the cause. The scenario
suite is expensive because individual tests repeatedly execute the entire
scenario catalog and launch nested selected pytest evidence nodes.
Collection-only for the 123 tests took 0.17 seconds, confirming that discovery
is negligible.

## Why The New Tests Are Slow

### Runtime Call Graph

```text
top-level scenario tests and report CLI tests
├── build_report(catalog)
│   └── evaluate_catalog(catalog)
│       └── execute 69 fixture adapters
│           ├── temporary files and directories
│           ├── disposable Git repositories and commits
│           ├── Planning State subprocesses
│           ├── child Python/import provenance checks
│           └── installer/switch/rollback/quiescence simulations
└── build_observed_report(catalog)
    ├── probe candidate .venv interpreter provenance
    ├── launch 13 separate pytest processes, one per evidence node
    │   └── 3 evidence nodes call build_report/evaluate_catalog again
    └── build_report(catalog) once more for the final aggregate report
```

An observed report therefore performs four complete catalog evaluations: three
inside selected evidence tests and one for its own final report.

### Measured Cost Centers

A post-closeout read-only timing run selected the 13 unique aggregate-evidence
nodes together. Parameterization expanded them to 25 test cases:

- 25 evidence cases: **69.61s** in one pytest process.
- `test_planning_quality_scenarios_cover_semantic_scope_approval_and_drafts`:
  **18.91s**.
- `test_contract_coverage_evidence_is_exact_and_green`: **18.81s**.
- `test_workflow_catalog_keeps_slice_two_families_green`: **18.65s**.
- A direct `validate_catalog` + `build_report` over the live catalog:
  **19.44s** (`17.24s` user CPU, `2.11s` system CPU).
- A representative direct observed-report test:
  **91.93s call time / 92.20s wall time**.

Those three 18–19 second evidence tests each rebuild/evaluate the complete
69-scenario report. The production observed-report path runs the 13 evidence
nodes as **13 separate processes**, not the one combined process used by the
timing probe, and then performs another full report evaluation. The measured
92.20-second observed report includes that process/collection overhead.

Instrumenting one whole-catalog evaluation recorded **1,175 subprocess calls**:

- 1,137 Git commands and 38 candidate-Python commands;
- 516 `git rev-parse HEAD` and 279 `git rev-parse --show-toplevel` calls;
- 74 commits, 42 repository initializations, 49 name/email configuration pairs,
  42 `git add identity.txt`, and 27 `git add .` calls;
- 26 Planning State `validate` commands and 10 `current` commands;
- 16 diffs and 8 status reads.

Every whole-catalog evaluation runs 32 workflow, 21 currentness, and 16 cutover
adapters. Currentness repeatedly seeds two real disposable Git repositories and
observes revisions, commits, diffs, status, scopes, and Planning State. Cutover
adds disposable lineage repositories, a child Python process, installer
fixtures, atomic symlink switch/rollback/quiescence, and historical Planning
State subprocesses. The installer work is real, but Git/process multiplication
is the dominant cost.

### Multiplication Inside The 123-Test Suite

The largest multiplier is not the number of scenarios. It is repeated observed
report construction:

- `test_cli_validate_and_json_report_are_deterministic` launches the report CLI
  four times: JSON twice and text twice. Inferred cost from the measured report:
  about **368s (6:08)**.
- `test_final_report_emits_exact_green_keys_aliases_contracts_and_families`
  builds one observed report. Measured cost: about **92s**.
- `test_report_cli_emits_the_same_exact_aggregate_evidence` launches one more
  observed report CLI. Inferred cost: about **92s**.

Those six report builds alone account for approximately **553s (9:13)**,
about 68% of the measured 814.32-second suite. The repetition count is exact;
the CLI durations are inferred from the representative 92.20-second direct
measurement.

The suite performs 24 whole-catalog evaluations inside those six observed
reports and 11 additional whole-catalog evaluations in ordinary tests: **35 in
total**. At 1,175 subprocesses per evaluation, that estimates 41,125 process
executions for equivalent live-catalog passes: roughly 39,795 Git and
1,330 Python processes. Mutated negative catalogs can skip a small amount of
work, so treat these as scale estimates rather than exact process totals. The
same multiplication implies roughly 2,415 disposable scenario workspaces and
1,470 repository-initialization commands.

The measured whole-catalog cost is approximately 18.5–19.4 seconds. Multiplying
the instrumented 18.53-second run by 35 yields 648.6 seconds, about 80% of the
full suite. Selected-node orchestration, catalog validation, negative tests,
CLI serialization, filesystem work, and pytest overhead explain the remainder.
Negative runtime-observation coverage alone adds another 17 child-process
starts across skip/xfail/xpass/collection/deselection/failure/error and
interpreter-provenance cases.

### Why Repeated Batch Validation Became So Expensive

The final suite was appropriately rerun after material fixes, but each full
rerun now costs 13:34. Two unchanged reruns cost 27:08; three cost 40:42. Worker
validation, coordinator final validation, and any reviewer that independently
reruns the same gate multiply that cost directly.

Git history proves the final 13:34 run and the long Slice 4 interval, but it does
not persist every intermediate command duration. The exact number of earlier
full-suite reruns cannot be reconstructed honestly from commits alone.

## What Consumed Model Context And Tokens

No exact token counter was written to the runway or receipts. The material
drivers are nevertheless visible:

1. **Large implementation surface.** The candidate added 9,154 lines. Agents
   repeatedly had to inspect a 1,354-line harness, 1,466-line catalog, roughly
   3,100 lines of adapters, and roughly 2,450 lines of focused tests.
2. **Large planning surface.** Dispatch, runway, receipts, and closeout total
   1,799 lines. The 981-line runway was repeatedly consulted after findings and
   three final-slice amendments.
3. **Strict cross-checkout handoffs.** Every worker and reviewer handoff carried
   full stable/candidate roots, revisions, generation identity, write scopes,
   and result-contract requirements. This was correct for safety but expensive
   to repeat verbatim.
4. **Multiple independent review lenses.** Each test-changing slice required a
   worker, test-quality review, independent runway review, and often
   import-topology review. Findings triggered new worker/reviewer turns.
5. **False-green hardening.** Many tests were added specifically to mutate
   expectations, collection controls, result shapes, leases, receipts, commit
   ranges, and workspace writes. These increased both code volume and review
   context, but materially improved confidence.
6. **Repeated long validation.** Agent turns remained open while 13-minute
   tests ran, then had to ingest large reports and continue with renewed live
   context.
7. **Output recovery.** Truncated parallel output and incorrect command/cache
   invocations caused additional tool calls and repeated context.
8. **Documentation duplication.** Full receipt payloads are repeated in the
   runway, completed-slice archive, and closeout. This improves standalone
   auditability but increases reading and generation cost.

## Necessary Cost Versus Avoidable Cost

Necessary or valuable:

- strict stable/candidate identity validation;
- independent worker/reviewer ownership;
- same-slice stop-and-amend behavior when the runway lacked authority;
- test-quality findings that removed self-certification and false greens;
- runtime proof that skip, xfail/xpass, collection manipulation, assertion
  failure, and setup error cannot count as acceptance;
- disposable Git/install/cutover behavior instead of real external mutation;
- exact same-batch closeout with no successor selection.

Avoidable or reducible:

- executing 13 evidence nodes in 13 pytest processes;
- rebuilding all 69 scenarios inside several evidence nodes;
- running the expensive observed report four times merely to prove output
  determinism;
- repeating unchanged expensive validation in multiple agent roles;
- late discovery that the all-changed-file Ruff command needed `--no-cache`;
- final-gate command batching that truncated output;
- large verbatim handoff/receipt repetition where a validated immutable receipt
  reference could suffice;
- patching repeated Markdown/JSON boundaries without unique anchors.

## Recommendations

### Priority 0: Remove The Nested Test Multiplier

1. **Run all evidence nodes in one pytest process.** Pass all 13 nodes to one
   invocation, emit JUnit once, and map each testcase back to its declared node.
   Preserve rejection of skips, xfails, xpasses, errors, deselection, and zero
   tests. This removes 12 process startups per observed report.
2. **Evaluate the catalog once per immutable input.** Add an internal or
   test-session cache keyed by candidate HEAD, catalog content hash, adapter
   source hashes, and evidence-test source hashes. Do not expose a public
   caller-controlled `observed_test_outcomes` argument; the anti-self-
   certification boundary must remain.
3. **Make evidence-node tests narrow.** The three slowest evidence nodes each
   evaluate all 69 scenarios. Have them assert their declared scenario subset
   against a shared immutable evaluation result instead of rebuilding the whole
   catalog.
4. **Separate CLI formatting determinism from acceptance execution.** Keep one
   end-to-end observed CLI test. Test repeated JSON/text formatting against one
   captured immutable report object, not four fresh executions of the evidence
   harness. This is the highest-value isolated change and should save roughly
   4.5 minutes per focused run.

### Priority 1: Make Slow Gates Explicit And Reusable

5. **Split fast and acceptance suites semantically.** Keep schema, mapping,
   pure comparison, and negative-shape tests in a fast gate. Mark runtime
   evidence, disposable Git/install behavior, and end-to-end observed reporting
   as an acceptance gate. The distinction should follow behavior and external
   cost, not an arbitrary test-count threshold.
6. **Persist validation receipts by exact commit.** Record command, candidate
   SHA, environment identity, result, duration, and output digest. Reviewers may
   reuse a green receipt for the same immutable commit instead of rerunning an
   unchanged 13-minute gate.
7. **Always collect duration evidence.** Use pytest duration reporting for the
   acceptance gate and compare its slowest nodes with the prior committed
   baseline. Flag material regressions by cause and ratio rather than a fixed
   universal timeout.
8. **Run the full acceptance gate once after the slice stabilizes.** During
   implementation, use the smallest behaviorally complete affected subset.
   Rerun the full gate only after a material code/test change or at final exact-
   commit validation.

### Priority 2: Reduce Orchestration And Context Overhead

9. **Introduce immutable lease/receipt references.** After full mechanical
   validation, allow later same-commit read-only handoffs to cite a durable
   receipt digest plus exact SHAs while retaining fail-closed revalidation on
   repository movement.
10. **Preflight final commands before the long run.** Validate selectors, Ruff
    cache policy, writable temp roots, output-size strategy, and exact changed
    paths before spending 13 minutes on the acceptance gate.
11. **Keep long command outputs separate.** Run slow tests, type/lint checks,
    installers, and known-red diagnostics as individually receipted commands so
    one large result cannot truncate all evidence.
12. **Add runner telemetry.** Future Batch Runway receipts should persist agent
    count, retry reason, command wall time, and model token usage when the host
   exposes it. This would replace retrospective inference with exact cost data.
13. **Reduce Git observation churn without faking Git.** Pre-seed a disposable
    repository template and cache root/revision observations within one atomic
    boundary. Retain fresh observations specifically at movement, race, and
    reviewer-handoff boundaries.
14. **Use Planning State's public Python API for most scenario checks.** Keep
    one CLI contract path, but avoid starting 36 Planning State processes per
    whole-catalog evaluation when the scenario is proving semantic behavior
    rather than shell invocation.

## Suggested Follow-Up Work

A bounded follow-up should optimize only the scenario-harness execution model,
without changing the 69 scenario semantics or weakening runtime evidence:

- baseline and profile the current acceptance gate;
- batch the 13 pytest evidence nodes;
- share immutable catalog evaluation within a test session;
- reduce the four CLI determinism executions to one end-to-end execution plus
  pure formatting checks;
- preserve every negative-runtime and provenance assertion;
- demonstrate the same six keys, six aliases, 31 contracts, and 17 families;
- compare old/new exact-commit durations and record the result.

This work should be planned separately. CCFG-23 remains closed, and this report
does not select or prepare a successor batch.

## Evidence Index

- `dispatch.md`: selected scope and non-goals.
- `runway.md`: execution contract, amendments, review routing, and final gates.
- `completed-slices.md`: slice outcomes, receipts, review loops, and durable
  orchestration anomalies.
- `closeout.md`: final acceptance, validation, repository identity, and
  same-batch reconciliation.
- Candidate range
  `2f3995060a309b27ba22d8d7e80f7d07d0b4a34f..e8d07a785581e26ffb202b13ae43a0a83173205b`:
  exact implementation and test surface.
- Stable range
  `3fbec1ba80884e4f35bd10c3fdf4f90578358011..3580d7844a3e95a8e5a1e652f496d904e232676e`:
  receipts, amendments, and closeout.
