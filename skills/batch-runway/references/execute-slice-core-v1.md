# Execute Slice Core v1

Use this reference for routine execution of one normal slice. It is a hot-path
projection of the canonical Batch Runway contracts, not an independent contract.

## Contents

- Source Map
- Routine Preconditions
- Coordinator Invariants
- Normal Slice Loop
- Worker Handoff
- Reviewer Handoff
- Commit Receipt
- Ledger Update
- Orchestration Anomalies
- Compact Convergence Fields
- Escalation Pointers

## Source Map

Coordinator invariants:

- `execution-contract-v2.md` for current specs
- `execution-contract-v1.md` only for existing specs that name v1

Reporting contracts:

- `agent-result-contract-v2.md` for current agent results
- `reporting-contracts-v1.md`

Ledger rules:

- `ledger-retention-v1.md`

Worker/reviewer handoffs:

- `subagent-briefs.md`

Cross-checkout controls:

- `cross-checkout-precreation-v1.md` for explicit absent-target creation work
- `cross-checkout-context-v1.md` for explicit strict post-creation work

Full contracts remain canonical. Make semantic changes in the canonical
references first, then update this projection to match.

## Routine Preconditions

Use this core only when the slice is routine:

- normal coding slice
- normal reviewer
- no active blocker
- no failed validation
- no reviewer-requested fix loop yet
- no explicit or triggered specialist review that needs a full review brief
- no escalation
- no final batch closeout

If any condition is false, read `execute-recovery-v1.md`,
`subagent-briefs.md`, `test-quality-review.md`, or `finalize-batch-v1.md` as
appropriate.

## Coordinator Invariants

- Keep the main agent coordinator-only.
- Do not implement code directly except concrete execution-ledger updates and
  commits.
- Delegate implementation to `runway_worker`.
- Delegate review to a separate `runway_reviewer`.
- Run triggered specialist support reviewers only when the task-scoped diff
  matches a review route; keep `runway_reviewer` as the final gate.
- Keep coordinator reads limited to orchestration state for routine slices.
- Delegate broad read-only investigation to the registered
  `codebase_investigator` and carry forward only its compact findings.
- Prefer one batch-scoped `codebase_investigator` investigation for related
  adjacent slices; use multiple investigators only for genuinely independent
  questions where parallel speedup is worth duplicated read context.
- Do not pass live support-agent handles to workers or reviewers. The
  coordinator owns support-agent lifecycle and passes only compact findings,
  selected per-slice notes, or artifact paths.
- For an explicitly `cross-checkout-precreation/v1` runway, apply
  `cross-checkout-precreation-v1.md` before every applicable worker and reviewer
  delegation, reject missing, null, or mismatched
  `verified_cross_checkout_precreation` facts, and require the helper-produced
  transition receipt plus strict context before later implementation. This
  invariant adds no step for ordinary single-root or strict cross-checkout
  handoffs.
- For a runway that explicitly names `cross-checkout-context/v1` or explicitly
  declares separate existing toolchain, canonical-planning, and implementation
  repository roots, require the `work-batch` ready/blocked preflight before the
  first strict handoff. Apply `cross-checkout-context-v1.md` by using the ready
  live context for that immediate first handoff, preparing a new exact live
  execution lease before every later worker and reviewer delegation, validating
  write scope separately, and rejecting missing, null, or mismatched verified
  identity in their v2 results. A
  `cross-checkout-precreation/v1` runway stays outside this strict branch with
  `verified_cross_checkout_context` null until a validated helper-produced
  transition receipt plus green strict context exists. Pre-creation
  verification cannot satisfy this strict invariant. This invariant adds no
  step for ordinary single-root handoffs.
- Preserve unrelated dirty files.
- Do not revert or commit files outside the slice scope.
- Commit after the slice is clean, validated, and reviewed.

## Normal Slice Loop

1. Read the active spec, current ledger, selected slice, dirty-file constraints,
   allowed files, stop conditions, commit strategy, selected validation
   profile, and named execution/result contract versions. Default new work to
   v2; preserve v1 only when the existing spec names it.
2. For Layout v1 or ledger-driven specs, read `../../planning-state/SKILL.md`, run
   its current and validate hot path, and keep compact Planning State Diagnostic
   facts before consuming active-state files, selected dispatches, queued specs,
   active runways, blockers, or target policy. Batch Runway still owns
   pending-row selection, validation, subagent routing, concrete
   execution-ledger updates, completed-slice archives, and commits.
3. If broad read-only investigation would otherwise be needed in coordinator
   context, use the `codebase_investigator` trigger in `subagent-briefs.md` and
   retain only compact findings.
4. For explicit pre-creation work, revalidate the complete payload, installed
   helper identity, stable revisions, absent targets, and exact creation scope.
   Stop before delegation on any missing or mismatched fact.
5. For work that explicitly names `cross-checkout-context/v1` or explicitly
   declares separate existing toolchain, canonical-planning, and implementation
   repository roots, require the `work-batch` ready/blocked preflight before the
   first strict handoff. Planning State must prove the same runway is current
   and safe to consume before the helper receives only the immutable planning
   snapshot. Require a ready non-null live context; blocked or ambiguous
   evidence stops before delegation. Before later worker
   handoffs, verify any repository movement since the prior accepted action
   against the exact accepted coordinator commit and intended changed paths,
   then call `prepare_cross_checkout_context_refresh(...)` against the immutable
   planning snapshot. Use its strictly parsed refreshed payload as a new live
   execution lease, and validate the canonical planning root and intended write
   scope separately. Stop before delegation on any missing or mismatched fact.
   Pre-creation work does not use this branch before its validated transition
   receipt plus green strict context.
6. Spawn `runway_worker` with the compact coding handoff below.
7. Require compact YAML from the worker. For explicit pre-creation work, reject
   a missing, null, or mismatched `verified_cross_checkout_precreation` and
   require `verified_cross_checkout_context` to remain `null`. For work that
   explicitly names `cross-checkout-context/v1` or explicitly declares separate
   existing toolchain, canonical-planning, and implementation repository roots,
   reject a missing, null, or mismatched `verified_cross_checkout_context`.
8. If a creation-bearing worker establishes either candidate root, use the
   retained validated pre-creation context and installed helper to build and
   serialize the versioned transition receipt with a newly validated strict
   context. Stop before further implementation or review when either proof is
   missing or mismatched. After this point, use only strict handoffs; do not
   re-run absent-state validation. Require `verified_cross_checkout_context`
   and require `verified_cross_checkout_precreation` to remain `null`.
9. Run or verify focused validation and selected-profile validation.
10. Classify the task-scoped diff for review triggers. If specialist support is
   needed, use `subagent-briefs.md` and retain only compact YAML findings.
11. Revalidate pre-creation facts when the declared roots remain absent. For a
   strict handoff, including one after a validated transition, call
   `prepare_cross_checkout_context_refresh(...)` again immediately before
   reviewer delegation and validate the reviewer scope separately. If an
   accepted coordinator action advanced a repository, first verify the exact
   accepted commit and intended changed paths. Movement between preparation and
   delegation, or movement not explained by an accepted coordinator action,
   enters `execute-recovery-v1.md`. Then spawn `runway_reviewer` with the compact
   review handoff below.
12. Require compact YAML from the reviewer. For a pre-creation handoff while
    roots remain absent, reject a missing, null, or mismatched
    `verified_cross_checkout_precreation` and require
    `verified_cross_checkout_context` to remain `null`. For a handoff that
    explicitly names `cross-checkout-context/v1`, explicitly declares separate
    existing toolchain, canonical-planning, and implementation repository roots,
    or follows the validated transition, reject a missing, null, or mismatched
    `verified_cross_checkout_context`.
13. Commit only the intended slice files once validation and review are clean.
14. Record any orchestration anomalies using the compact log below.
15. Report the compact commit receipt.
16. Update the active ledger with only remaining-work state. Ordinary slice
    entries record exact commit hashes after commit; final self-referential
    closeout entries use `this closeout commit` under `finalize-batch-v1.md`.
17. Move completed-slice audit references to the completed archive.
18. Close completed subagents.
19. Continue to the next pending slice unless a stop condition remains active or
    the user explicitly asks to stop.

## Worker Handoff

The registered `runway_worker` TOML owns the v2 result schema and completion
standard; `reporting-contracts-v1.md` owns the legacy v1 schema. This handoff
owns slice-specific inputs, explicit result-version selection, and coordinator
lifecycle.

```text
Use agent_type="runway_worker".

Implement slice <N> from <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Allowed files/areas: <slice allowed files>.
Dirty-file constraints: <constraints>.
Validation profile: <selected profile path or expanded profile>.
Result contract: <Registered Agent Result Contract v2, or Compact Report Contract v1 when the existing spec names v1>.
Cross-checkout pre-creation: <exact payload, installed helper path, intended creation targets, and handoff mode, or not applicable>.
Cross-checkout context: <fresh live execution lease payload, canonical planning root, and installed helper path, or not applicable>.
Cross-checkout mode: <write-bearing, read-only, or not applicable>.
You are already the required coding subagent for this slice. Do not spawn,
delegate to, or wait on additional subagents. Implement only this slice.
The coordinator handles validation, review delegation, concrete execution-ledger
updates, completed-slice archives, and commits.
Do not run project-level integration harnesses, index/search/graph refreshes,
generated-doc refreshes, final validation, or cleanup commands unless this handoff
explicitly assigns them.
Read the full slice in the spec. Return YAML only.
Use exactly the result contract selected above. Stop if it conflicts with the
spec.
For a handoff that explicitly names `cross-checkout-context/v1` or explicitly
declares separate existing toolchain, canonical-planning, and implementation
repository roots, independently validate the supplied live execution lease
before editing and populate the registered v2 strict identity field. Do not
substitute the planning snapshot. Stop on missing or mismatched context. A
handoff naming `cross-checkout-precreation/v1` does not
use this strict branch until it carries a validated helper-produced transition
receipt plus green strict context; before then its strict field remains null.
For an explicit pre-creation handoff, independently validate the complete
payload and applicable exact creation targets with the installed helper before
editing and populate `verified_cross_checkout_precreation`. Leave
`verified_cross_checkout_context` null until a validated transition selects the
strict contract. Stop on missing or mismatched facts.
No implementation history, reasoning narrative, or chronological work log.
```

## Reviewer Handoff

The registered `runway_reviewer` TOML owns the v2 result schema, review lenses,
severity values, and clean-verdict standard;
`reporting-contracts-v1.md` owns the legacy v1 schema. This handoff owns the
exact review basis, result-version selection, and slice-specific evidence.

```text
Use agent_type="runway_reviewer".

Review slice <N> against <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Diff basis: <commit hash or task-scoped worktree diff paths>.
Result contract: <Registered Agent Result Contract v2, or Compact Report Contract v1 when the existing spec names v1>.
Cross-checkout pre-creation: <exact payload, installed helper path, intended creation targets, and handoff mode, or not applicable>.
Cross-checkout context: <fresh live execution lease payload, canonical planning root, and installed helper path, or not applicable>.
Cross-checkout mode: <read-only or not applicable>.
Inspect only the task-scoped diff and relevant files.
Check scope, acceptance criteria, validation evidence, dirty-file leakage, and behavior preservation.
Flag new or remaining cleanup residue that lacks a concrete reason, removal condition, or follow-up owner.
Classify review lenses before the verdict and include `lenses_applied`.
Include compact specialist-review findings already gathered by the coordinator.
For a handoff that explicitly names `cross-checkout-context/v1` or explicitly
declares separate existing toolchain, canonical-planning, and implementation
repository roots, independently validate the supplied live execution lease and
populate the registered v2 strict identity field. Do not substitute the
planning snapshot. Stop on missing or mismatched context. A handoff naming
`cross-checkout-precreation/v1` does not use this
strict branch until it carries a validated helper-produced transition receipt
plus green strict context; before then its strict field remains null.
For an explicit pre-creation handoff, independently validate the complete
payload and applicable exact creation targets with the installed helper and
populate `verified_cross_checkout_precreation`. Leave
`verified_cross_checkout_context` null until a validated transition selects the
strict contract. Stop on missing or mismatched facts.
Return YAML only using exactly the result contract selected above. Stop if it
conflicts with the spec. Do not modify files.
```

## Triggered Specialist Review

Do not force multiple reviewers for every slice. Use specialist support only
when the task-scoped diff triggers a lens, then pass compact findings into the
final `runway_reviewer` handoff. Read `subagent-briefs.md` for triggered
specialist-review routing and `test-quality-review.md` when tests trigger that
review.

Use `subagent-briefs.md` for optional `codebase_investigator` support
investigations. Support output must follow the compact YAML contract owned by
the registered agent role.

## Commit Receipt

Routine commit receipts should stay compact. Read `reporting-contracts-v1.md`
for full receipt variants or non-routine reporting.

```yaml
slice: 3
commit: abc1234
subject: Slim execute core
status: committed
files_changed:
  - skills/batch-runway/references/execute-slice-core-v1.md
validation: "git diff --check; focused test passed"
review: clean
convergence:
  phase: convergence
  scope_trend: shrinking
  new_unknowns: []
  blockers: []
  next_proof: "Validate next boundary"
inspect:
  - git show --stat abc1234
```

For strict cross-checkout work, pair each accepted worker or reviewer action
with an execution receipt that identifies the newly prepared live execution
lease and separately validated scope used by that handoff. Keep the receipt
compact while preserving the exact helper-owned revision and identity facts;
never fill it from the planning snapshot. Keep the one preflight result compact
rather than duplicating it in every slice receipt.

## Ledger Update

- Keep active ledger state limited to remaining-work facts.
- Summarize validation; do not paste logs or transcripts.
- Keep unresolved orchestration anomalies in the active ledger only while they
  may affect remaining execution.
- Move completed rows to the completed slice archive after commit.
- Archive only commit hash, outcome, and audit references.
- Keep unresolved risks, blockers, compatibility paths, and next proof in the
  active ledger until resolved.

## Orchestration Anomalies

Use `orchestration_anomalies` for suspicious coordinator or subagent-lifecycle
behavior that may need later workflow fixes. Do not record routine command
output, normal validation logs, clean reviews, or implementation chronology.

Examples include accidental extra spawns, wrong roles, unusable support output,
malformed reports, confusing wait/resume/approval controls, ambiguous or flaky
validation, near role-contract violations, unexpected `HEAD` or diff movement,
and stale reviewer evidence.

Compact YAML:

```yaml
orchestration_anomalies:
  - slice: 1
    severity: low
    category: accidental_agent_spawn
    observed: "Extra read-only no-op explorer spawned while looking for wait control."
    impact: "No write scope, no artifact used, no lifecycle effect."
    action_taken: "Ignored; continued waiting on actual worker and support explorer."
    follow_up: "Consider UI or process note if repeated."
```

## Compact Convergence Fields

Use compact convergence for routine receipts and ledger notes:

```yaml
convergence:
  phase: convergence
  scope_trend: shrinking
  new_unknowns: []
  blockers: []
  next_proof: "Validate next boundary"
```

Allowed values:

- `phase`: `discovery | convergence | closure`
- `scope_trend`: `shrinking | stable | expanding`

## Escalation Pointers

- Validation failed: read `execute-recovery-v1.md`.
- Review found issues: read `execute-recovery-v1.md`.
- Blocker, ambiguity, dirty-file conflict, or approval issue: read
  `execute-recovery-v1.md`.
- Explicit or triggered test-quality-review: read `test-quality-review.md`.
- Last slice completed or final report requested: read `finalize-batch-v1.md`.
