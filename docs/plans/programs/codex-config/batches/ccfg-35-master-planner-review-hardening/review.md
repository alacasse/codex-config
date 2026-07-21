# CCFG-35 Master Planner Replacement Planning Review

## Role And Boundary

- Reviewer: separate read-only planning reviewer.
- Canonical master basis:
  `/home/alacasse/projects/codex-config` on `master` at
  `a701a5a9d8810e67ad193f2955eea24a4886007b`.
- Candidate evidence-only basis:
  `/home/alacasse/projects/codex-config-command-owner-redesign` at
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`.
- Planning State at review: replacement dispatch selected; queue and active
  runway empty; validation passed.
- Planning-state or queue mutation by reviewer: none.
- Implementation started: `false`.

## Initial Exact Review

- Dispatch SHA-256:
  `293fe59e63b739f7a15323502af37992e39e9bdfbd916b59e01fe5bf41b667bb`.
- Runway SHA-256:
  `80cbcc87656098e4e16914f917fd0437da01fadf7ea1b46fecf722d40ca3ca53`.
- Verdict: `correction_required`.
- Blockers: none.

Required corrections:

1. define an executable disposable proof lane that sends all ten scenarios
   through the installed master planner/create-spec/reviewer instructions and
   observes the real isolated queue decision;
2. prove every changed installed route file against exact accepted master
   commit objects rather than only the mutable worktree; and
3. distinguish the current master route from the target evidence-backed review
   gate in the dispatch.

## Final Exact Review

- Dispatch SHA-256:
  `f8f5e8535608f9d50521dd205d1ae726183738ae3e27af30b31701b316881aed`.
- Runway SHA-256:
  `3acef09e943c9aa1d73cf5027859379d8f7bef1be6757d7785aed8ccb216379a`.
- Verdict: `clean`.
- Corrections: none.
- Blockers: none.
- Implementation started: `false`.

Any later draft change invalidates this review and requires another exact-draft
review before queue mutation.

## Independently Reconstructed Facts

### Canonical State And Supersession

The candidate-targeted predecessor is superseded before implementation. The
source finding records the explicit transition through `Open` and master-only
authority. At review time, canonical state selected only the replacement
dispatch and left the queue/active runway empty.

Evidence:

- `../ccfg-35-planning-independent-review-hardening/superseded.md`
- `../../findings/planning-and-independent-review-hardening.md`
- canonical program `CURRENT.md` and `LEDGER.md`
- passing Planning State `current` and `validate` output.

### Actual Installed Master Planner

The stable installed public planner is the repo-owned master
`skills/plan-batch` symlink. Master routes planning through Planning State,
Architecture Program Runway selection/queue ownership, and Batch Runway
create-spec. Evidence-backed independent planning review is the missing target
gate, not an observed current guarantee.

Evidence:

- `skills/plan-batch/SKILL.md`
- `skills/architecture-program-runway/SKILL.md`
- `skills/batch-runway/references/create-spec.md`
- `codex-features.json`
- `scripts/codex_owner.py` and installed `readlink -f` evidence
- matching plan-time installed/repo skill SHA-256
  `3d042d0af3deba2ffbb2f49f3d9062cfa22999139206e97cb87b2a71c1a9cdff`.

### Master-Only Scope

The replacement writes only the master planner/support route. Candidate-only
planner/reviewer roles, deterministic planning scripts, schemas, transactions,
tests, and candidate-home installation are explicit stop conditions. The batch
uses ordinary single-root v2 handoffs with cross-checkout fields null.

Evidence:

- final dispatch, Exact Planning Basis and Explicitly Excluded
- final runway, Master-Only Implementation Authority and Batch Non-Goals.

### Slice Shape And Semantic Authority

Slice 1 is independently useful because it prevents evidence-free review from
authorizing any queue mutation. Slice 2 uses that gate for conditional semantic
replacement, failure-path, current-consumer, counterfactual, feasibility,
alternative-shape, and proportionality evidence. Mechanical enforcement remains
limited to binding, references, identifiers, and alignment.

Evidence:

- final runway, Ownership Matrix, Planning Evidence Applicability, Slice Shape
  Rationale, and both slice acceptance sections.

### Executable Behavior And Closeout Proof

The corrected runway requires exactly nine negative scenarios and one positive
control in isolated temporary Planning State roots. Fresh separate planner and
reviewer invocations must record input/draft hashes, evidence-backed coarse
dispositions, and observed queue outcomes. Missing live invocation blocks
acceptance. Evidence-free clean, changed-draft, and missing-review
counterfactuals must all remain unqueued.

Final provenance enumerates every changed installed-route file and owning
feature. The reviewer must compare installed hashes to exact accepted master
commit blobs, confirm owner/link/installer/branch/range facts, and reject
worktree-only or candidate-home evidence.

Evidence:

- final runway, Disposable Actual-Master Behavioral Proof Lane
- final runway, Scenario Acceptance Matrix
- final runway, Final Validation and Required Accepted-Closeout Proof.

## Authorization Result

The exact final dispatch/runway above may be recorded as the sole queued
CCFG-35 replacement. This clean planning review authorizes only queue mutation;
it does not authorize implementation, candidate work, successor selection, or
closeout.
