# CCFG-26 Slice 1 Execution Retrospective: What Did Not Go Well

## Purpose

This report records what failed during the first `work-batch` execution of
`ccfg-26-execution-state-foundation`, why several apparently green iterations
did not produce an acceptable Slice, where the plan and review process were
insufficient, and what must change before implementation resumes.

The evidence comes from the accepted dispatch, runway, amendment, design
contract, ADR, coordinator-observed validation and review results, the final
execution report, the stable planning history, and the preserved candidate
worktree. The execution runner did not persist exact model-token consumption or
a trustworthy end-to-end command timeline. This report therefore quantifies
implementation passes, review results, findings, test progression, changed
lines, and durable outcomes without inventing token or elapsed-time totals.

## Executive Summary

- Slice 1 did not complete. It ended blocked during final independent review,
  with no accepted candidate commit, no completed-Slice receipt, no real Batch
  Execution State, no closeout, and no successor selection.
- The candidate contains 4,268 inserted lines across ten paths: 4,225 lines in
  eight untracked implementation/test/workflow/schema files and 43 additions to
  `README.md` and `CHANGELOG.md`. All of it remains uncommitted.
- Execution required four code-producing passes—initial implementation plus
  three correction passes—and then a fifth, design-only pass that correctly
  stopped without editing. Coordinator validation progressed from 36 to 43 to
  55 to 60 passing tests, each with 6 passing subtests.
- Eight specialist or independent review results produced twelve actionable
  findings: nine high severity and three medium severity. The final high
  finding invalidated the storage confinement strategy after the preceding
  local tests, static gates, import review, and test-quality review were green.
- The decisive defect is a final-effect time-of-check/time-of-use gap. Path
  validation immediately before path-based `open`, `link`, or `replace` cannot
  prevent namespace substitution inside those operations. Locks, receipts, or
  canonical state can therefore be redirected outside the accepted batch
  namespace.
- The blocker is architectural, not one more bounded patch. POSIX has a viable
  descriptor-relative `O_NOFOLLOW` design, but the project's Python 3.11
  baseline does not expose an equivalent standard-library contract for the
  required Windows open/link/replace effects. The current runway does not
  authorize a cross-platform anchored-filesystem dependency, while a native
  Win32/NT backend was never designed, bounded, or given a credible validation
  path.
- Before implementation, the original clean planning review also missed a
  self-hosting bootstrap contradiction: candidate state initialized for Slice 2
  would have had no record of the stable controller's completed Slice 1 and
  would have selected Slice 1 again. A later amendment had to keep the stable
  controller authoritative and withdraw the planner-created runtime root.
- The plan was reviewed as executable even though it specified fail-closed,
  atomic, cross-platform outcomes without selecting or proving the filesystem
  mechanism needed to make those outcomes true. This feasibility question
  should have been resolved before a 4,268-line production Slice was built.
- Review routing found many real defects, but the adversarial filesystem effect
  boundary was tested and reviewed too late. Earlier green gates repeatedly
  proved the current model rather than the full safety claim.

## Exact Outcome And Preserved State

| Fact | Observed result |
|---|---|
| Stable execution basis | `e989c724e40588511afb7da4a266e9898d05d381` |
| Stable blocker-recording commit | `c91896a6571cb08b63794835add813c335edb69a` |
| Candidate branch | `implementation/command-owner-redesign` |
| Candidate baseline and current HEAD | `5c5ec9d52dd9033daa45f3a200031c152363b62c` |
| Candidate implementation commit | None |
| Candidate worktree | Dirty in ten reviewed paths |
| Real Batch Execution State | Absent |
| Withdrawn planner-created root | `/tmp/tmp.nAyp7HeqwO`; historical residue, verified empty and forbidden from use |
| Exact-platform workflow evidence | Not run; no accepted exact commit existed |
| Slice 2 | Not started |
| Batch closeout | None |
| Successor | None selected |

The strict stable/candidate startup preflight was ready, and each worker or
reviewer handoff used refreshed identity and scope evidence. The failure was
not caused by checkout confusion, stale candidate HEAD, candidate control of
canonical planning, or accidental creation of real runtime state.

## Execution And Review Slow Path

| Stage | Local gate | Review result | Consequence |
|---|---|---|---|
| Initial implementation | 36 tests, 6 subtests; Ruff and new-module BasedPyright green | Import review: 1 high. Test-quality review: 2 high, 3 medium | First correction pass required |
| Correction pass 1 | 43 tests, 6 subtests; static gates green | Repeat import and test-quality reviews clean | Advanced to independent runway review |
| Independent runway review 1 | Prior gate remained green | 3 high findings | Second correction pass required |
| Correction pass 2 | 55 tests, 6 subtests; static gates green | Delta-only test-quality review: 2 high findings | Third correction pass required |
| Correction pass 3 | 60 tests, 6 subtests; all coordinator gates green | Repeat test-quality review clean | Advanced to decisive runway re-review |
| Independent runway re-review | Prior gate remained green | 1 high final-effect confinement finding | Slice rejected |
| Final worker design pass | No code changes | Cross-platform standard-library feasibility failed under current scope | Execution stopped blocked |

This was four code-producing passes, one blocked design pass, four complete
coordinator focused-gate sets, and eight review results. The loop was costly
because each repair expanded the proof surface, but none reached the missing
mechanism decision until the final independent review.

## Complete Finding Inventory

| # | Severity | Source | What was wrong |
|---:|---|---|---|
| 1 | High | Import topology | `ModuleNotFoundError` fallbacks could create competing identities for project-local modules, while process tests exercised a file-path CLI instead of the canonical module entrypoint. |
| 2 | High | Test quality | Initialization could persist state whose batch identity did not match the state path, then reject only after the unreadable state existed. |
| 3 | Medium | Test quality | Attempt/candidate resolution coverage left incorrect-target and ordering gaps. |
| 4 | Medium | Test quality | Crash coverage omitted material checkpoints in the promised initialization-to-projection lifecycle. |
| 5 | High | Test quality | A lock-release failure after a successful commit could falsely report `state_changed: false` and the old revision. |
| 6 | Medium | Test quality | Contention proof mocked the lock backend instead of proving behavior between real processes. |
| 7 | High | Independent runway review | A failure while rereading after compare-and-swap could report that no state changed even though canonical state was already committed. |
| 8 | High | Independent runway review | New transitions trusted referenced prior receipt/result identifiers without verifying that the evidence existed and matched. |
| 9 | High | Independent runway review | Symlinked state, lock, receipt, or derived paths could fork or escape the accepted namespace. |
| 10 | High | Test quality | Prior-evidence tests did not prove normalized rejection, preservation of existing bytes, and correct replay ordering. |
| 11 | High | Test quality | Symlink tests inserted links only before an operation; they did not substitute namespace entries at the final effect boundary. |
| 12 | High | Independent runway re-review | Even after pre-effect checks, substitution inside the final path-based `Path.open`, `os.link`, and `os.replace` calls could redirect lock creation, receipt publication, or canonical-state replacement outside the namespace. |

The first eleven findings were corrected or given stronger tests. The twelfth
showed that those corrections still depended on a check-then-use strategy that
cannot establish the promised confinement guarantee.

## Technical Failures

### 1. Path validation was mistaken for effect confinement

The implementation increasingly validated parents, leaf types, symlinks, and
derived targets. Those checks narrowed ordinary misuse, but the final write
operations still resolved pathnames after the checks. An attacker or
deterministic test hook could replace a namespace entry between validation and
the kernel effect.

The required invariant is stronger: every lock, temporary file, receipt,
canonical state, manifest, and Markdown effect must remain anchored to the
already-validated batch directory at the moment the effect occurs. Rechecking
the same pathname more often does not provide that invariant.

### 2. Commit-truth reporting was initially unreliable

Several error paths treated an exception as proof that no mutation occurred.
That is false after atomic replacement or another durable step. The first
implementation could therefore report stale revision and `state_changed`
values after state had changed. Later corrections improved this, but the
repeated findings show that durable commit points and normalized outcome truth
were not designed as one explicit state machine before coding began.

### 3. Evidence integrity was incomplete

The store initially accepted references to prior results and receipts without
proving that those artifacts existed and agreed. The correction then needed a
second review because the tests did not fully assert rejection shape, byte
preservation, and replay ordering. The design named immutable evidence, but
implementation and tests reached the exact integrity contract incrementally.

### 4. Concurrency and crash proof started too abstractly

One contention test mocked the backend even though the acceptance contract was
explicitly about real processes and killed holders. Crash checkpoints also
lagged the promised lifecycle. These tests were later strengthened, but the
initial proof strategy was weaker than the runway's observable behavior.

### 5. Cross-platform feasibility was unresolved

The final design pass found a credible POSIX standard-library path based on
directory descriptors, `O_NOFOLLOW`, and descriptor-relative operations. The
same public primitives at the project's Python 3.11 baseline are not available
for Windows link and replace confinement. A correct Windows implementation
needs either a mature
cross-platform anchored-filesystem abstraction or a separately designed native
Win32/NT handle-relative backend. The dependency was outside the accepted
allowance; the native backend had not been designed or bounded and could not be
validated honestly from the Linux execution host.

## Planning And Design Failures

### 1. The original plan contained a self-hosting bootstrap contradiction

The first clean planning review accepted a design in which the candidate
machinery produced by Slice 1 would control development of the real Slice 2.
Candidate state initialization has an empty completed prefix and no event for
importing stable Batch Runway history. It would therefore have selected Slice 1
again after the stable controller had already completed it.

The bootstrap amendment correctly made the stable controller authoritative for
both real implementation Slices and limited candidate execution state to
disposable acceptance fixtures. It also withdrew `/tmp/tmp.nAyp7HeqwO` with a
`must_not_be_created_or_consumed` disposition. Needing that amendment shows the
original plan and independent review did not prove progression ownership before
declaring the runway executable.

### 2. The contract specified outcomes without the decisive primitive

ADR 0003 and the design contract require atomic replacement, fail-closed
storage, and Windows/macOS/Linux support. The runway adds generic “path safety”
tests. None of the accepted artifacts made final-effect, no-follow, anchored
namespace operations an explicit implementation and feasibility contract.

The design review therefore called the boundary clean while leaving the exact
primitive that makes the safety claim true undecided. “Atomic replacement” and
“path safety” were too broad to expose the platform gap during planning.

### 3. The dependency allowance addressed the lock, not all filesystem effects

The runway permitted at most one mature internal lock dependency and allowed
`pyproject.toml`/`uv.lock` changes only for that lock choice. The final blocker
is broader: lock creation, immutable receipt publication, and canonical state
replacement all need final-effect confinement. A lock package cannot by itself
solve anchored open/link/replace semantics.

This created an authorization mismatch. The batch required a security property
whose likely implementation would expand the dependency or native-backend
boundary beyond what the batch allowed.

### 4. Feasibility was deferred into production implementation

Rejecting separate reducer/schema/lock/store commits avoided horizontal
scaffolding, but it did not justify skipping a bounded pre-implementation
feasibility proof. A small disposable proof of anchored create/link/replace on
POSIX and Windows could have answered the platform question before the full
deep module, schemas, CLI, projections, workflow, and three test modules were
built.

The problem was not necessarily the two-Slice vertical product shape. The
problem was declaring Slice 1 executable before its most consequential
cross-platform implementation assumption had evidence.

### 5. Slice 1 carried too much unresolved risk at once

One acceptance boundary combined the reducer, schema, imports, identity
validation, process lock, compare-and-swap, crash truth, replay, prior-evidence
integrity, receipts, projections, CLI, real-process tests, three-platform
workflow, and documentation. The result was 4,268 inserted lines before an
acceptable commit boundary.

That large surface multiplied correction and rereview cost. It also made the
final architectural rejection more expensive because the preserved WIP now
mixes reusable domain logic with a rejected storage-effect strategy.

### 6. Platform proof was positioned too late

The plan required real Ubuntu, macOS, and Windows evidence only against the
exact accepted candidate commit. No commit could be accepted until local review
was clean, but local review could not prove the missing Windows primitive. The
plan needed an earlier disposable Windows feasibility gate, separate from final
exact-commit acceptance.

## Execution And Review Process Failures

### 1. Specialist routing did not target the highest-risk boundary early

Early import-topology and test-quality reviews found important problems, but no
early review was framed specifically around adversarial filesystem namespace
confinement. The independent runway reviewer eventually found the effect-boundary
issue, after three correction passes. The reviewer brief mentioned path safety
only indirectly through crash/CAS/replay and platform honesty.

### 2. Green tests repeatedly overstated confidence

The 36-, 43-, 55-, and 60-test gates were all useful, but each proved the test
model available at that moment. The strongest pre-final symlink tests changed
paths before the operation, so they could not falsify check-then-use code. The
final deterministic injection inside the effect call was the first test shape
that matched the actual guarantee.

The process treated growing green test counts as convergence when the threat
model itself was still incomplete.

### 3. Review became defect discovery by serial escalation

Each review layer exposed a deeper class only after the previous correction was
implemented and fully revalidated: imports, domain truth, evidence integrity,
pre-operation namespace safety, and finally effect-boundary safety. The review
sequence was not front-loaded around the highest-cost invalidating assumptions.

### 4. The one-commit Slice boundary amplified recovery cost

The policy correctly prevented an unsafe partial Slice from being accepted,
but the implementation accumulated as uncommitted work. There is no immutable
candidate checkpoint tying the 60-test state to an exact commit, and the final
three-platform workflow could not run against an accepted SHA. Preserving the
worktree is necessary, but resumption now requires careful diff recovery rather
than a normal commit-based continuation.

## Avoidable Tooling And Orchestration Friction

These problems were not the final blocker, but they consumed time and context:

| Friction | Effect | Correction |
|---|---|---|
| Python 3.14 dynamic helper loading omitted `sys.modules` registration | Initial preflight failed before semantic work | Register the module before dataclass execution |
| `dataclasses.asdict` attempted to deepcopy `mappingproxy` during context refresh reporting | Helper-result serialization failed | Use an explicit serializer for immutable mappings |
| Coordinator inspected workflow job `process-tests` instead of the actual `process-lock` key | Workflow check failed for the wrong reason | Inspect the declared job name |
| Broad import grep matched intentional platform `ImportError` handling for `fcntl`/`msvcrt` | False-positive import concern | Narrow the check to project-local fallback imports |
| Stable Git staging hit the sandbox's read-only `.git/index.lock` boundary | Documentation commit was delayed | Rerun exact `git add`/`git commit` with approved escalation |

## Consequences

- No part of Slice 1 is accepted, despite substantial implementation and test
  work.
- The candidate has a large dirty worktree that must be preserved and audited.
- Slice 2 cannot start because its public state-owner dependency is unaccepted.
- Parent CCFG-26 remains pending, so CCFG-27 through CCFG-29 remain blocked by
  their existing dependency order.
- The real Windows/macOS/Linux workflow has no exact commit to validate.
- Stable planning needed a separate blocker-recording commit and durable report
  instead of a Slice 1 completed-Slice receipt. Batch closeout remained
  unavailable until Slice 2 and the later whole-batch gates regardless.
- Exact time and token cost cannot be reconstructed because the execution path
  did not persist that telemetry. Any numeric claim beyond the evidenced
  passes, findings, tests, and changed lines would be speculative.

## Required Changes Before Retry

### 1. Make one explicit mechanism decision

A reviewed amendment or superseding replan must authorize exactly one of:

- a mature cross-platform anchored-filesystem dependency whose observable
  contract covers no-follow/handle-relative lock creation, temporary creation,
  immutable publication, and atomic replacement on Windows, macOS, and Linux;
  or
- a native split backend with an explicit POSIX descriptor-relative design and
  an explicit Win32/NT handle-relative design, including ownership, allowed
  files, error normalization, and maintenance boundary.

The retry must not begin with “choose while implementing.”

### 2. Write the final-effect confinement contract first

The amended contract must state how each effect remains under one validated
batch-directory handle or equivalent capability at the instant it occurs. It
must cover the lock, temporary files, canonical state, receipts, results,
manifests, and Markdown projections; define behavior under late namespace
substitution; and distinguish pre-commit from post-commit error truth.

### 3. Prove Windows feasibility before production resumption

Run a disposable, minimal proof on a real Windows runner before authorizing the
preserved production diff. The proof must exercise late substitution at the
actual open/link/replace boundary, killed-holder reacquisition, and atomic
replacement behavior. A Linux mock or platform-conditional inference is not
enough.

### 4. Re-review the preserved diff against the new contract

Do not simply patch the final finding on top of the current worktree. Classify
the 4,268 inserted lines into reusable domain/model logic, storage code coupled
to the rejected path strategy, tests that encode incomplete assumptions, and
unchanged public/docs behavior. Preserve only what the new mechanism actually
supports.

### 5. Move invalidating reviews earlier

Before rebuilding the full Slice, require an adversarial storage/effect review
of the mechanism and a focused test-quality review of effect-boundary fault
injection. Import, domain, and evidence reviews still matter, but they should
not precede the only review capable of invalidating the storage architecture.

### 6. Add exact adversarial acceptance cases

At minimum, tests must substitute the lock target, temporary/receipt target,
and canonical state target inside the final effect call; prove no external
write; prove truthful post-commit outcomes; prove old bytes remain unchanged on
pre-commit rejection; and run real process contention and killed-holder cases.

## Follow-Up Process Improvement

Persisting execution telemetry is not a precondition for the bounded Slice 1
retry, but it should be tracked separately as a workflow improvement.

Future work-batch execution should retain command start/end/result summaries,
review finding counts, correction-pass identity, and—when the platform exposes
it—token usage. That evidence is needed to distinguish design cost, validation
cost, review cost, and orchestration waste in later retrospectives.

## Next Safe Action

Keep the existing batch queued and blocked. Preserve the candidate worktree.
Create a reviewed planning amendment or superseding replan that resolves the
cross-platform final-effect mechanism and Windows proof path. Only after that
decision may the stable controller refresh the strict live lease, authorize a
bounded Slice 1 correction, rerun all focused validation and specialist
reviews, and request a new exact-diff independent runway review.

Do not apply a POSIX-only patch, weaken the platform matrix, accept another
check-then-use path strategy, start Slice 2, create real batch state, close the
batch, or select a successor.
