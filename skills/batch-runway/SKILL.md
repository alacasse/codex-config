---
name: batch-runway
description: Agent-facing runtime support used by plan-batch and work-batch for multi-slice runway spec mechanics, execution contracts, per-slice validation, commits, ledger updates, and implementation/review delegation.
---

# Batch Runway

Agent-facing runtime support for `plan-batch` and `work-batch`. Do not present
this as the normal human command for ledger-driven planning or execution; use
the command-owner skill first, then apply this workflow for the controlled
sequence of small, independently committable slices. Keep the main agent as
coordinator; delegate implementation and review.

## Modes

- `create-spec`: write one runway spec for a future execution session. Do not
  implement code.
- `execute-spec`: execute an existing runway spec one slice at a time.

Infer the mode when the user does not name one:

- "create", "spec", "plan", "next runway", or "upcoming work" means
  `create-spec`.
- "execute", "run", "implement", "work through", or a specific spec path means
  `execute-spec`.

## Density

- `lean-runway`: token-efficient. Specs reference standard contracts,
  validation profiles, and compact subagent briefs.
- `full-runway`: maximum explicitness. Specs may include full contracts, full
  commands, and full subagent briefs.

Default to `lean-runway` for mechanical refactors, test topology splits, import
cleanup, docs-local planning, compatibility facade cleanup, and
behavior-preserving module moves.

Default to `full-runway` only when compact references would be unsafe: production
behavior changes, installer lifecycle changes, YAML schema changes, sandbox
execution behavior, public CLI behavior, risky migrations, ambiguous ownership
boundaries, or unreliable subagent file access.

Prefer lean specs plus explicit risk overrides before pasting whole contracts.

## Progressive Disclosure

Read only the reference files needed for the current mode. Do not load every
reference file by default.

- `references/project-values.md`: read before creating or executing a spec.
- `../planning-state/SKILL.md`: read before consuming Layout v1 active-state
  files, selected dispatches, queued specs, active runways, blockers, target
  policy, or projection-backed reports. Carry forward only Planning State
  Diagnostic facts; Batch Runway still owns concrete runway spec creation,
  execution orchestration, validation selection, subagent routing,
  execution-ledger updates, completed-slice archives, and commits.
- `../planning-state/references/projection-reporting.md`: read before broad
  history/reporting scans; follow Planning State's projection routing.
- `../planning-artifacts/SKILL.md`: read when resolving a planning location,
  creating a spec from a selected dispatch packet, reorganizing planning
  artifacts, or when project instructions name Planning Artifact Layout v1.
- `references/execute-slice-core-v1.md`: read for routine `execute-spec` slice
  execution. This is the hot-path projection of the full canonical contracts.
- `references/execution-contract-v2.md`: read when creating a new spec, executing
  current full-runway specs, or changing current contract semantics.
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
- `references/validation-profiles.md`: read when selecting a profile during
  planning or when the selected profile is unknown. During routine execution,
  read only the selected file under `references/validation-profiles/`.
- `references/create-spec.md`: read only in `create-spec` mode.
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
2. Resolve project-specific values from repository instructions, local overlays,
   the active spec, or explicit user direction. See
   `references/project-values.md`.
3. When the work uses a ledger-driven planning root, use `planning-state`
   Diagnostic-First Pickup and projection-reporting guidance for operational
   state facts before broader exploration.
4. Use `planning-artifacts` for Planning Artifact Layout v1 placement, naming,
   active-state file shape, batch directory, archive, and run/output-root
   questions.
5. Check the worktree and preserve unrelated dirty files.
6. Choose `create-spec` or `execute-spec`.
7. Choose `lean-runway` or `full-runway`.

For explicit pre-creation work, complete
`references/cross-checkout-precreation-v1.md` before writing a runway or
delegating a worker or reviewer, then require its transition before switching to
the strict contract. For work that explicitly names
`cross-checkout-context/v1` or explicitly declares separate existing toolchain,
canonical-planning, and implementation repository roots, complete
`references/cross-checkout-context-v1.md`. A pre-creation runway does not use
that strict branch until it has a validated helper-produced transition receipt
plus green strict context. Ordinary single-root work uses neither bridge.

Stop instead of guessing when a required project value, validation command,
harness command, output path, summary artifact, planning location, or
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
- Broad coordinator exploration is allowed for `create-spec`, recovery, blocker
  analysis, finalization, stale or ambiguous specs, subagent-report
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

When a runway is created from an `architecture-program-runway` selected
dispatch, treat that dispatch as the program-level selection contract. Batch
Runway consumes the dispatch and minimum program-ledger excerpt needed for
traceability, then writes one concrete `runway.md` with its own active ledger
and completed-slice archive.

Batch Runway owns concrete execution state: slice rows, validation selection,
review routing, commit receipts, orchestration anomalies, and completed-slice
archive movement. Architecture Program Runway owns program state: finding
grouping, selected dispatch, batch queue, program-level ledger updates, and
closeout reconciliation across batches.

Do not use Batch Runway routine execution to reselect the architecture program
batch, rewrite finding lifecycle statuses, or close program findings directly.
At finalization, preserve compact evidence from the concrete runway so an
`architecture-program-runway closeout-runway` pass can reconcile the program
ledger.

## Create-Spec Summary

In `create-spec` mode:

1. Read `references/create-spec.md`.
2. For explicit pre-creation work, read and apply
   `references/cross-checkout-precreation-v1.md` before writing the runway.
3. For work that explicitly names `cross-checkout-context/v1` or explicitly
   declares separate existing toolchain, canonical-planning, and implementation
   repository roots, read and apply `references/cross-checkout-context-v1.md`
   before writing the runway. Pre-creation work does not use this branch before
   its validated transition receipt plus green strict context.
4. If the project uses Planning Artifact Layout v1, use `planning-state`
   Diagnostic-First Pickup first and consume only its compact facts.
5. If a selected dispatch, active runway, or queued batch exists, do not select
   another batch. Report the queued/active path, or create the missing
   `runway.md` from the selected dispatch when that is the requested action.
6. If no batch is selected, read the relevant program ledger and only the source
   packet named by the selected ledger row before writing the spec.
7. Write one local plan file in the project planning location. If the project
   uses Planning Artifact Layout v1 and a selected batch directory exists,
   write the spec to that batch directory as `runway.md`.
8. Pick 3-5 tightly related slices that can execute sequentially.
9. Keep each slice independently testable and committable.
10. Stop before coding.

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
