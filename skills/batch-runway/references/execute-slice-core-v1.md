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
4. Spawn `runway_worker` with the compact coding handoff below.
5. Require compact YAML from the worker.
6. Run or verify focused validation and selected-profile validation.
7. Classify the task-scoped diff for review triggers. If specialist support is
   needed, use `subagent-briefs.md` and retain only compact YAML findings.
8. Spawn `runway_reviewer` with the compact review handoff below.
9. Require compact YAML from the reviewer.
10. Commit only the intended slice files once validation and review are clean.
11. Record any orchestration anomalies using the compact log below.
12. Report the compact commit receipt.
13. Update the active ledger with only remaining-work state. Ordinary slice
    entries record exact commit hashes after commit; final self-referential
    closeout entries use `this closeout commit` under `finalize-batch-v1.md`.
14. Move completed-slice audit references to the completed archive.
15. Close completed subagents.
16. Continue to the next pending slice unless a stop condition remains active or
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
Inspect only the task-scoped diff and relevant files.
Check scope, acceptance criteria, validation evidence, dirty-file leakage, and behavior preservation.
Flag new or remaining cleanup residue that lacks a concrete reason, removal condition, or follow-up owner.
Classify review lenses before the verdict and include `lenses_applied`.
Include compact specialist-review findings already gathered by the coordinator.
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
