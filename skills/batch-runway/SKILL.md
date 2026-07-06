---
name: batch-runway
description: Create and execute multi-slice runway specs with per-slice scope, validation, ledger updates, commits, and mandatory coding/review subagent delegation. Use when the user asks to create a batch runway spec, execute a runway spec, streamline sequential slices, work from project-local plans, commit after each slice, reduce long-running context use, or keep the main agent as coordinator only while subagents implement and review.
---

# Batch Runway

Use this skill for a controlled sequence of small, independently committable
slices. Keep the main agent as coordinator; delegate implementation and review.

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
  files, selected dispatches, queued specs, active runways, blockers, or target
  policy. Treat its output as Planning State Diagnostic facts for this
  workflow; Batch Runway still owns spec creation, execution orchestration,
  validation selection, subagent routing, ledger updates, and commits.
- `../planning-state/references/projection-reporting.md`: read before broad
  history/reporting scans for pending-batch inventory, missing closeout
  evidence, batch evidence, runner summaries, or bounded backlog/history
  reports. Treat policy-compatible `report-projection` command output as the
  normal route when `projection_usage` and `projection_rebuild_authority` allow
  it; stop on missing or incompatible policy, or record an explicit fallback
  decision, before broad historical scans. Do not query SQLite directly or
  silently scrape historical planning files.
- `../planning-artifacts/SKILL.md`: read when resolving a planning location,
  creating a spec from a selected dispatch packet, reorganizing planning
  artifacts, or when project instructions name Planning Artifact Layout v1.
- `references/execute-slice-core-v1.md`: read for routine `execute-spec` slice
  execution. This is the hot-path projection of the full canonical contracts.
- `references/execution-contract-v1.md`: read when creating a new spec, executing
  full-runway specs, auditing compatibility, or changing contract semantics.
- `references/reporting-contracts-v1.md`: read before requesting worker,
  reviewer, commit-receipt, convergence, or ledger-update output outside the
  routine core path, or when changing canonical reporting semantics.
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

When a subagent receives only a spec path, make sure the spec contains enough
contract detail for that subagent to act safely, or include a short contract
capsule and the relevant Batch Runway reference path in the subagent prompt.

## Required First Steps

1. Read applicable project instructions and local overlays.
2. Resolve project-specific values from repository instructions, local overlays,
   the active spec, or explicit user direction. See
   `references/project-values.md`.
3. When the work uses a ledger-driven planning root, run the `planning-state`
   hot path before consuming Layout v1 active-state files, selected dispatches,
   queued specs, active runways, blockers, or target policy. Carry forward only
   compact Planning State Diagnostic facts: planning root, current and validate
   status, active programs, selected dispatch, queued batch, active runway,
   blockers, warnings, and project policy.
   For next-task, next-spec, pickup, or queued-work requests, follow
   `planning-state` Diagnostic-First Pickup before broader exploration.
4. For supported history/reporting questions not answered by the active-state
   diagnostic, read the planning-state projection-reporting guidance and use
   policy-compatible `report-projection` command output as the normal route
   before broad historical scans. Missing or incompatible projection policy is a
   bounded blocker or explicit fallback decision, not permission for silent
   Markdown archaeology or direct SQLite reads.
5. Check the worktree and preserve unrelated dirty files.
6. Choose `create-spec` or `execute-spec`.
7. Choose `lean-runway` or `full-runway`.

Stop instead of guessing when a required project value, validation command,
harness command, output path, summary artifact, planning location, or
instruction priority order is missing.

## Core Contract

Use Batch Runway Standard Execution Contract v1 unless the spec explicitly
overrides it.

Non-negotiable execution rules:

- These delegation rules bind the coordinator, not spawned workers or reviewers.
  A spawned `runway_worker` is already the required coding subagent for its
  assigned slice; it must implement that slice directly and must not spawn,
  delegate to, or wait on additional coding or review agents.
- The coordinator owns validation, project-level refresh/harness decisions,
  review delegation, ledger updates, commits, and subagent lifecycle unless a
  spec explicitly says otherwise.
- The main agent is coordinator only.
- The main agent must not implement code changes directly except for updating
  the ledger and making commits.
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
- Delegate broad read-only exploration to `fast_explorer` instead of loading it
  into coordinator context. Prefer one batch-scoped investigation for related
  adjacent slices; use multiple explorers only when questions are independent
  and the parallel speedup is worth duplicated read context.
- The coordinator owns support-agent lifecycle. Do not pass live support-agent
  handles to workers or reviewers; pass only compact findings, selected
  per-slice notes, or artifact paths.
- `fast_explorer` output should reduce coordinator and worker search cost, not
  become retained raw investigation context. Require compact, file-referenced
  YAML findings.
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
  receipts, convergence, and ledger updates.
- Move completed slice details out of the active ledger and into the completed
  slice archive.
- Store detailed commands, logs, transcripts, and generated reports in commits
  or artifacts, then reference them.

## Create-Spec Summary

In `create-spec` mode:

1. Read `references/create-spec.md`.
2. If the project uses Planning Artifact Layout v1, use `planning-state` first
   to collect Planning State Diagnostic facts, then read the root `CURRENT.md`
   and relevant program `CURRENT.md` named by that diagnostic before broader
   exploration.
3. If a selected dispatch, active runway, or queued batch exists in the
   diagnostic or active-state files, do not
   select another batch. Report the queued/active path, or create the missing
   `runway.md` from the selected dispatch when that is the requested action.
4. If no batch is selected, read the relevant program ledger and only the source
   packet named by the selected ledger row before writing the spec.
5. Write one local plan file in the project planning location. If the project
   uses Planning Artifact Layout v1 and a selected batch directory exists,
   write the spec to that batch directory as `runway.md`.
6. Pick 3-5 tightly related slices that can execute sequentially.
7. Keep each slice independently testable and committable.
8. Stop before coding.

## Execute-Spec Summary

In `execute-spec` mode:

1. Read the full active spec.
2. Read `references/project-values.md`.
3. For Layout v1 or ledger-driven specs, use `planning-state` first to collect
   Planning State Diagnostic facts before reading active-state files, queued
   specs, active runways, blockers, or target policy.
4. For routine slice execution, read `references/execute-slice-core-v1.md` and
   only the selected validation profile file under
   `references/validation-profiles/`.
5. Identify the active validation profile, pending ledger rows, stop conditions,
   commit strategy, density mode, convergence state, active ledger rows, and
   completed slice archive.
6. Execute from the next incomplete ledger row.
7. For each routine slice: spawn coding subagent, validate, spawn separate review
   subagent, commit if clean, record any orchestration anomalies, report
   receipt, update ledger/archive, close subagents, continue.
8. If validation fails, review finds issues, blockers appear, or escalation is
   needed, read `references/execute-recovery-v1.md`.
9. After the last slice, read `references/finalize-batch-v1.md`, run final
   validation and project-required index refresh,
   then report commits, validation, skipped slices, remaining risks, cleanup
   residues, `orchestration_anomalies`, and expanded convergence.

## Stop Conditions

Stop on scope drift, unresolved ambiguity, repeatedly unresolved validation
failure, dirty-file conflict, missing subagent support, missing project values,
or a stop condition from the active spec.

Do not say work is almost done or completion is forecastable unless remaining
work is bounded, known, explicitly enumerated, and supported by the latest
convergence evidence.
