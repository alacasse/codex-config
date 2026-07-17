---
name: batch-runway
description: Agent-facing execution support used by work-batch for per-slice validation, commits, ledgers, recovery, finalization, and implementation/review delegation.
---

# Batch Runway

Agent-facing execution support for `work-batch`. Do not present this as the
normal human command for ledger-driven execution; use the command owner first,
then apply this workflow to an already queued or active runway. Keep the main
agent as coordinator; delegate implementation and review.

Public `plan-batch` owns selection, dispatch and runway creation, planning
review, proportionality, approvals, validation-profile selection, and the
DEC-038 queue transaction. Batch Runway must not plan, create, reshape, select,
or queue a runway.

## Mode

`execute-spec` executes one existing runway one slice at a time. Planning,
spec-creation, or next-batch requests must return to public `plan-batch`; they
must not be inferred as a Batch Runway mode.

## Existing Runway Density

- `lean-runway`: token-efficient. Specs reference standard contracts,
  validation profiles, and compact subagent briefs.
- `full-runway`: maximum explicitness. Specs may include full contracts, full
  commands, and full subagent briefs.

Consume the density already selected by the queued runway. Do not use execution
to change slice shape, risk classification, or planning detail.

## Progressive Disclosure

Read only the reference files needed for the current mode. Do not load every
reference file by default.

- `references/project-values.md`: read before executing a spec.
- `../planning-state/SKILL.md`: read before consuming Layout v1 active-state
  files, selected dispatches, queued specs, active runways, blockers, target
  policy, or projection-backed reports. Carry forward only Planning State
  Diagnostic facts; Batch Runway still owns execution orchestration,
  validation acceptance, subagent routing,
  execution-ledger updates, completed-slice archives, and commits.
- `../planning-state/references/projection-reporting.md`: read before broad
  history/reporting scans; follow Planning State's projection routing.
- `../planning-artifacts/SKILL.md`: read when resolving the existing runway,
  batch directory, closeout, archive, or when project instructions name
  Planning Artifact Layout v1.
- `references/execute-slice-core-v1.md`: read for routine `execute-spec` slice
  execution. This is the hot-path projection of the full canonical contracts.
- `references/execution-contract-v2.md`: read when executing current
  full-runway specs or changing current execution-contract semantics.
- `references/execution-contract-v1.md`: read only when executing or auditing an
  existing spec that names v1.
- `references/agent-result-contract-v2.md`: read when changing current agent
  result ownership or shared agent presentation semantics. Registered agent
  TOMLs own their exact v2 result schemas.
- `references/reporting-contracts-v1.md`: read for v1 compatibility and before
  requesting coordinator commit-receipt, convergence, anomaly, or ledger-update
  output outside the routine core path.
- `references/ledger-retention-v1.md`: read before creating a new ledger or
  changing canonical ledger semantics. Routine ledger updates are covered by the
  execution core.
- `references/validation-profiles.md`: read when the runway's selected profile
  is unknown. During routine execution, read only the selected file under
  `references/validation-profiles/`.
- `references/execute-spec.md`: read for execution routing, compatibility
  questions, or non-routine execution. Routine slices can use the execution core
  directly.
- `references/execute-recovery-v1.md`: read only when validation fails, review
  finds issues, blockers appear, workspace state or review evidence stops
  matching the expected diff, escalation is required, or execution deviates from
  the normal path.
- `references/finalize-batch-v1.md`: read only when closing a batch or producing
  a final report.
- `references/subagent-briefs.md`: read only when full brief variants,
  support-agent guidance, triggered specialist review routing, or non-routine
  subagent prompting is needed. Routine handoffs are covered by the execution
  core.
- `references/test-quality-review.md`: read only when a slice explicitly asks for
  test quality review or when changed tests trigger test-review routing.
- `references/cross-checkout-precreation-v1.md`: read only when a selected
  dispatch, runway, or handoff explicitly names
  `cross-checkout-precreation/v1`.
- `references/cross-checkout-context-v1.md`: read only when a selected dispatch,
  runway, or handoff explicitly names `cross-checkout-context/v1` or explicitly
  declares separate existing toolchain, canonical-planning, and implementation
  repository roots.

When a subagent receives only a spec path, make sure the spec contains enough
contract detail for that subagent to act safely, or include a short contract
capsule and the relevant Batch Runway reference path in the subagent prompt.

## Required First Steps

1. Read applicable project instructions and local overlays.
2. Resolve execution values from repository instructions, local overlays, the
   active spec, or explicit user direction. See
   `references/project-values.md`.
3. When the work uses a ledger-driven planning root, use `planning-state`
   Diagnostic-First Pickup and projection-reporting guidance for operational
   state facts before broader exploration.
   Treat the Planning State Diagnostic as read-only current/validate evidence.
4. Use `planning-artifacts` to interpret the existing Layout v1 active-state
   shape, batch directory, archive, and run/output roots.
5. Check the worktree and preserve unrelated dirty files.
6. Require an existing queued or active runway and use `execute-spec`.
7. Consume the runway's recorded density and validation profile unchanged.

For supported execution-history, missing-closeout-evidence, runner-summary, or
bounded reporting questions, read
`../planning-state/references/projection-reporting.md`. Use policy-compatible
`report-projection` command output as the normal route before broad historical
scans when `projection_usage` and `projection_rebuild_authority` allow it.
Record an explicit fallback decision before scanning when policy is unavailable
or incompatible, and do not query SQLite directly.

For explicit pre-creation work, complete
`references/cross-checkout-precreation-v1.md` before delegating a worker or
reviewer, then require its transition before switching to the strict contract.
For work that explicitly names
`cross-checkout-context/v1` or explicitly declares separate existing toolchain,
canonical-planning, and implementation repository roots, complete
`references/cross-checkout-context-v1.md`. A pre-creation runway does not use
that strict branch until it has a validated helper-produced transition receipt
plus green strict context. Ordinary single-root work uses neither bridge.

Stop instead of guessing when a required execution value, validation command,
harness command, output path, summary artifact, existing runway location, or
instruction priority order is missing.

## Core Contract

Use Batch Runway Standard Execution Contract v2 for new work. Honor an existing
spec's named contract version; do not reinterpret v1 as v2.

Non-negotiable execution rules:

- For an explicitly pre-creation runway, validate the complete
  `cross-checkout-precreation/v1` payload and exact intended creation targets
  with the installed helper before applicable delegations, propagate them, and
  reject missing, null, or mismatched
  `verified_cross_checkout_precreation` facts. Before later implementation,
  require the helper-produced transition receipt and validated strict context;
  pre-creation verification cannot satisfy the strict result field. The strict
  field remains `null` for a pre-creation handoff; after transition, the
  pre-creation field remains `null` for strict handoffs. Both remain `null` and
  this rule adds no step for ordinary single-root work.
- For a runway that explicitly names `cross-checkout-context/v1` or explicitly
  declares separate existing toolchain, canonical-planning, and implementation
  repository roots, validate the complete strict payload and canonical planning
  root with the installed helper before delegation, propagate them in worker and
  reviewer handoffs, and reject missing or mismatched verified identity in
  either agent result. A `cross-checkout-precreation/v1` runway stays outside
  this branch with `verified_cross_checkout_context` null until a validated
  helper-produced transition receipt plus green strict context exists. Do not
  infer roots from cwd.
- These delegation rules bind the coordinator, not spawned workers or reviewers.
  A spawned `runway_worker` is already the required coding subagent for its
  assigned slice; it must implement that slice directly and must not spawn,
  delegate to, or wait on additional coding or review agents.
- The coordinator owns validation, project-level refresh/harness decisions,
  review delegation, concrete execution-ledger updates, completed-slice
  archives, commits, and subagent lifecycle unless a spec explicitly says
  otherwise.
- The main agent is coordinator only.
- The main agent must not implement code changes directly except for updating
  the concrete execution ledger and making commits.
- Each slice implementation must be delegated to a coding subagent.
- Each completed slice must be reviewed by a separate review subagent before
  commit.
- Use `runway_worker` for coding subagents and `runway_reviewer` for review
  subagents when available.
- If required subagent tooling or custom agents are unavailable, stop and report
  that execution cannot proceed under this workflow.
- Do not fall back to main-agent implementation.
- Commit after each clean, focused slice.
- Preserve unrelated dirty files.
- Do not revert or commit files outside the slice scope.
- If workspace reconciliation requires changing tracked source, test, spec, or
  generated content, delegate that cleanup to `runway_worker` or stop for user
  direction; coordinator-authored reverse patches are not allowed as
  implementation cleanup.
- Workers must not run project-level integration harnesses, index/search/graph
  refreshes, generated-doc refreshes, final validation, package installs, or
  cleanup commands unless their handoff explicitly assigns that work.
- Continue to the next pending slice after a commit receipt unless the user
  explicitly asks to stop or a stop condition remains active.
- After an interruption, approval, permission issue, context transition, or
  clarification, resume the same runway at the next incomplete ledger row.

## Context Discipline

Keep live orchestration context small enough for long batches.

- The coordinator should orchestrate. Workers, reviewers, and support agents
  should investigate.
- In routine `execute-spec` mode, coordinator reads should stay limited to
  orchestration state: active spec/slice, active ledger state, dirty-file state,
  selected validation profile, compact validation outputs, compact subagent
  reports, commit receipts, and required summary artifacts.
- Delegate broad read-only technical investigation to the registered
  `codebase_investigator` instead of loading it into coordinator context. Give
  it a bounded, decision-oriented question. Prefer one batch-scoped
  investigation for related adjacent slices; use multiple investigators only
  when questions are genuinely independent and the parallel speedup is worth
  duplicated read context.
- The coordinator owns support-agent lifecycle. Do not pass live support-agent
  handles to workers or reviewers; pass only compact findings, selected
  per-slice notes, or artifact paths.
- `codebase_investigator` output should reduce coordinator and worker search
  cost, not become retained raw investigation context. Require the compact,
  file-referenced YAML contract owned by the registered agent role.
- Prefer lean specs and compact subagent briefs when they preserve safety.
- Do not paste full slice text into subagent prompts unless the subagent cannot
  reliably read the spec, the boundary is subtle, or the work is high risk.
- Broad coordinator exploration is allowed for recovery, blocker analysis,
  finalization, stale or ambiguous specs, subagent-report
  verification, or uncertainty that prevents safe delegation.
- Do not retain implementation chronology, command transcripts, repeated
  clean-review prose, repetitive validation detail, or repeated explanations of
  already-closed slices.
- Keep a compact `orchestration_anomalies` log for suspicious coordinator or
  subagent-lifecycle behavior that may need later workflow fixes, such as
  accidental extra agent spawns, wrong agent roles, unusable support output,
  malformed subagent reports, confusing controls, ambiguous validation, flaky
  commands, escalation friction, unexpected `HEAD` or diff movement, stale
  review evidence, or near contract violations. Do not use it for routine
  command output, normal validation logs, clean reviews, or implementation
  chronology.
- Use compact YAML for routine worker results, reviewer results, commit
  receipts, convergence, and concrete execution-ledger updates.
- Move completed slice details out of the active ledger and into the completed
  slice archive.
- Store detailed commands, logs, transcripts, and generated reports in commits
  or artifacts, then reference them.

## Architecture Program Handoff

Public `plan-batch` supplies the complete selected dispatch, independently
reviewed runway, validation profile, and queue transaction. Batch Runway
consumes that already queued or active runway and owns concrete execution
state: pending slice rows, validation execution and acceptance, review routing,
commit receipts, orchestration anomalies, execution-ledger updates, and
completed-slice archive movement.

Do not use Batch Runway execution to reselect work, reshape the runway, create
planning artifacts, mutate finding lifecycle state, or close program findings
directly. At finalization, preserve compact evidence so
`architecture-program-runway closeout-runway` can reconcile the just-completed
batch only. That reconciliation must not select or prepare a successor.

## Execute-Spec Summary

In `execute-spec` mode:

1. Read the full active spec.
2. Read `references/project-values.md`.
3. For an explicitly pre-creation runway, read and apply
   `references/cross-checkout-precreation-v1.md` before applicable worker or
   reviewer delegation and until its validated strict transition.
4. For a runway that explicitly names `cross-checkout-context/v1` or explicitly
   declares separate existing toolchain, canonical-planning, and implementation
   repository roots, read and apply `references/cross-checkout-context-v1.md`
   before any worker or reviewer delegation. Pre-creation work does not use
   this strict branch before its validated transition receipt plus green strict
   context.
5. For Layout v1 or ledger-driven specs, use `planning-state`
   Diagnostic-First Pickup first and carry only its compact facts before
   broader exploration.
6. For routine slice execution, read `references/execute-slice-core-v1.md` and
   only the selected validation profile file under
   `references/validation-profiles/`.
7. Identify the active validation profile, pending ledger rows, stop conditions,
   commit strategy, density mode, convergence state, active ledger rows, and
   completed slice archive.
8. Execute from the next incomplete ledger row.
9. For routine slices, follow `references/execute-slice-core-v1.md`; it owns
   the worker/reviewer handoffs, validation/review loop, commit receipt,
   ledger/archive update, anomaly logging, and continuation.
10. If validation fails, review finds issues, blockers appear, or escalation is
   needed, read `references/execute-recovery-v1.md`.
11. After the last slice, read `references/finalize-batch-v1.md`; it owns final
   validation, required refreshes, closeout evidence, cleanup residues,
   `orchestration_anomalies`, and expanded convergence reporting.

## Stop Conditions

Stop on scope drift, unresolved ambiguity, repeatedly unresolved validation
failure, dirty-file conflict, missing subagent support, missing project values,
or a stop condition from the active spec.

Do not say work is almost done or completion is forecastable unless remaining
work is bounded, known, explicitly enumerated, and supported by the latest
convergence evidence.
