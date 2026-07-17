# CCFG-34 Stable Runway Dogfooding Bootstrap Dispatch

## Selection

- Batch ID: `ccfg-34-stable-runway-dogfooding-bootstrap`
- Selection outcome: `selected`
- Queue target: exactly one `queued` runway
- Covers: CCFG-34 only
- Source ledger: `../../LEDGER.md`
- Source finding:
  `../../findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`
- Expected runway: `runway.md`
- Planning layout: Planning Artifact Layout v1
- Planning root: `../../../..`
- Implementation repository: `/home/alacasse/projects/codex-config`
- Execution context: ordinary single-root; neither
  `cross-checkout-context/v1` nor `cross-checkout-precreation/v1` applies
- Batch kind: `migration`
- Density: `full-runway`
- Validation profile: `project-harness-production`

Planning State `current` and `validate` reported an idle, valid program with no
selected dispatch, queued batch, active runway, or blocker. CCFG-34 is the sole
`Ready` finding. CCFG-26 remains blocked, its prior dispatch/review/runway remain
superseded historical evidence, and CCFG-27 through CCFG-29 remain unselected.

## Authoritative Sources

- CCFG-34 in `../../LEDGER.md`.
- GitHub issue #62 as ingested into
  `../../findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`.
- Active program state in `../../CURRENT.md`.
- Repository instructions in `../../../../../../.codex/AGENTS.md` and
  `../../../../../../AGENTS.md`.
- Domain language in `../../../../../../CONTEXT.md`.
- Command-owner decision in
  `../../../../../adr/0002-human-facing-command-owner-skills.md`.

The current code graph and focused source investigation are secondary
implementation-seam evidence only. They identify the existing runner facade,
phase workers, state/receipt helpers, validation, artifacts/telemetry, phase
observation, and registered `codebase_investigator` as the owners to extend.
They do not authorize a second runner framework or widen the ledger finding.

## Goal

Add the smallest temporary stable-generation support needed to execute CCFG-26
through CCFG-29 with the operational benefits of GitHub issues #59, #60, and
#61 before the permanent candidate behavior exists:

1. one project-owned vertical and context-bounded planning policy, loaded
   automatically from the repository-local instruction chain;
2. one fresh coordinator process per slice, same-slice recovery, finalization,
   and closeout unit while reusing current runner state, receipts, phase
   identities, and telemetry; and
3. at most one fresh read-only recovery assessment before avoidable escalation,
   without transferring recovery authority to the advisor.

CCFG-34 must self-dogfood the same process discipline and must leave a mechanical
CCFG-29 removal gate tied to candidate parity.

## Existing Owner Seams

- `scripts/architecture_program_runner_workers.py`: `PhaseWorker`,
  `CodexExecWorker`, and `execute_phase_with_worker` own fresh process launch.
- `scripts/architecture_program_runner.py`: `run` remains the sole runner
  coordinator and persistence loop.
- `scripts/architecture_program_runner_state.py`: atomic state, receipt paths,
  and resumable run facts.
- `scripts/architecture_program_runner_validation.py`: public phase-result,
  state, and receipt contradiction rejection; a temporary unit result must be
  validated separately rather than widening the public phase-result schema.
- `scripts/architecture_program_runner_artifacts.py` and
  `scripts/architecture_program_runner_phase_observation.py`: existing phase
  telemetry, session attribution, token summaries when available, and run
  aggregation.
- `agents/codebase_investigator.toml`: existing read-only advisory role. Do not
  add a second advisor role.

## Migration Matrix

```yaml
migration_matrix:
  stable_planning_for_ccfg_26_through_ccfg_29:
    current_owner: issue #62 plus manual runway-specific prose
    future_owner: candidate plan-batch, batch_planner, and batch_plan_reviewer behavior from issue #60
    status: pending
    removal_slice_or_condition: CCFG-29 after candidate #60 parity and equivalent regression proof
  stable_slice_coordinator_flights:
    current_owner: one long-lived stable execute coordinator
    future_owner: candidate work-batch launcher behavior from issue #61
    status: pending
    removal_slice_or_condition: CCFG-29 after candidate #61 parity
  stable_finalization_and_closeout_flights:
    current_owner: shared execute and closeout coordinator context
    future_owner: candidate work-batch and runner lifecycle behavior from issue #61
    status: pending
    removal_slice_or_condition: CCFG-29 after finalization, closeout, and no-successor parity
  stable_blocker_assessment:
    current_owner: immediate escalation or ad hoc diagnosis
    future_owner: candidate registered advisor and bounded authority envelope from issue #59
    status: pending
    removal_slice_or_condition: CCFG-29 after candidate #59 parity
  serialized_phase_identities:
    current_owner: stable architecture program runner
    future_owner: CCFG-27 migration or retention decision
    status: pending
    removal_slice_or_condition: preserve select-dispatch, create-spec, execute, and closeout until CCFG-27 decides; physical cleanup no later than CCFG-29
  superseded_ccfg_26_plan:
    current_owner: historical planning evidence only
    future_owner: a fresh post-CCFG-34 plan-batch invocation
    status: pending
    removal_slice_or_condition: never resume the superseded runway; preserve it as non-executable evidence
```

## Semantic Slice Shape

The batch starts from one possible slice and adds three boundaries because each
creates a valid, independently reviewable intermediate state:

1. **Temporary project policy**: future stable planning automatically consumes
   one project-owned contract before runner behavior changes.
2. **Representative slice flight**: one pending slice can complete through a
   fresh coordinator and durable continuation without finalization or closeout
   changes.
3. **Finalization and closeout flights**: the valid slice-only seam extends to
   distinct transition and no-successor boundaries.
4. **Recovery assessment**: normal successful continuation remains usable while
   blocker diagnosis adds a separate advisory role and authority-classification
   risk.

Adjacent-boundary rationale:

- `1 -> 2`: different owner seams and validation profiles; the policy is an
  independently usable planning result consumed by the launcher work.
- `2 -> 3`: a committed slice and durable same-batch continuation are a valid
  rollback point; finalization/closeout add transition and reconciliation risk.
- `3 -> 4`: successful continuation is complete without blocker recovery;
  recovery introduces a separate read-only role, evidence packet, and authority
  envelope.

Merge Slices 2 and 3 only if implementation proves that the existing runner
cannot expose a valid slice-only continuation state. Split a slice again if one
fresh coordinator cannot implement, validate, review, commit, and archive it
without compaction.

## Proportionality

The advisory warning thresholds apply per slice: about 12 changed files, 1,000
changed lines, 3 primary production surfaces, 2 ownership boundaries, 2
migration kinds, or 3 specialist review lenses.

- Slice 1 is expected to remain below the warnings.
- Slices 2 and 3 may reach the production-surface warning because a vertical
  runner path necessarily crosses existing worker, state, validation, and
  telemetry owners. The smaller single-file alternative is rejected because it
  would duplicate or bypass those owners.
- Slice 4 may reach the review-lens warning. The smaller alternative is to reuse
  `codebase_investigator` unchanged; a new agent or recursive debate loop is
  forbidden.

Every flight must record observed changed-file count, line delta, validation
breadth, review lenses, duration, token usage when attributable, and coordinator
compaction occurrence. A warning requires a written smaller-alternative check;
compaction or materially wider scope requires re-slicing or a reviewed amendment.

## Dependencies And Execution Preconditions

- CCFG-25 is closed and CCFG-34 is the only eligible row.
- The issue #62 intake and superseded CCFG-26 notice are intentional dirty-file
  inputs; execution must preserve them and must not absorb unrelated changes.
- Runner JSON, receipts, and telemetry require one explicit fresh,
  caller-owned batch run-artifact root under `/tmp`, created before the first
  execution flight and reused by every CCFG-34 flight. Each unit keeps distinct
  receipts and telemetry within that root. Do not invent a reusable default and
  do not write operational JSON under `docs/plans/`.
- Focused stable baseline: 139 runner/investigator/semantic-slice tests and 66
  subtests pass; focused Ruff is green.
- Full repository pytest is a known-red baseline: 16 failures, 481 passes, and
  707 subtests pass. It is diagnostic until a named slice owns every failure.
- Broad runner BasedPyright is a known-red baseline with 72 errors. It is not a
  CCFG-34 acceptance gate and must not trigger unrelated typing cleanup.
- `./install.sh --status` and `./install.sh --dry-run` confirm installed links
  but report pre-existing manifest-version drift. They are diagnostic evidence,
  not permission to mutate runtime Codex state.

## Self-Dogfooding Flight Contract

- This planning session stops after queueing and performs no implementation.
- Execute Slice 1 and Slice 2 in separate fresh coordinator processes using the
  active runway's manual flight override because the temporary launcher does not
  exist yet.
- After Slice 2 proves the launcher, use that launcher for Slice 3, Slice 4,
  finalization, and closeout.
- Stop the coordinator after every clean slice commit and receipt. Resume only
  from durable canonical state and the next incomplete execution-ledger row.
- A same-slice correction or recovery uses a fresh process and the same slice ID.
- Each flight loads only current Planning State, the active runway/unit and
  ledger row, selected validation profile, exact worktree state, immediately
  relevant prior receipt, unresolved anomalies, and an applicable current lease.
  It must not reload completed chronology, raw transcripts, or accepted review
  detail.
- Before escalating an eligible blocker, obtain exactly one fresh read-only
  assessment. The advisor cannot edit, approve, commit, delegate, select work,
  amend the runway, or approve its own recommendation.

## Non-Goals

- No CCFG-26 implementation, COR-009 closeout, candidate integration,
  stable-home rebind, default-generation switch, merge, or bridge deletion.
- No permanent implementation of #59, #60, or #61 candidate behavior.
- No second complete runner, CLI, daemon, execution store, phase enum,
  transition engine, worker hierarchy, telemetry tree, or lifecycle framework.
- No public widening of the existing phase-result protocol and no new public
  serialized phase identity.
- No project-specific CCFG behavior in reusable generic skills.
- No recursive advisor loop, general replanning, silent validation
  reclassification, safety weakening, scope expansion, destructive work, or
  successor selection.

## Stop Conditions

- Stop if the temporary policy cannot be loaded through repository-local
  instructions without changing generic skills or global instructions.
- Stop if implementation creates a second runner framework rather than reusing
  the existing facade, worker, state, validation, receipt, and telemetry seams.
- Stop if a unit result becomes a permanent public runner protocol or persistent
  execution store.
- Stop if the next unit is inferred from Git, ancestry, filenames, timestamps,
  transcripts, or accepted-review chronology instead of durable canonical state.
- Stop if a completed unit, finalization, or closeout can select or prepare a
  successor.
- Stop if the advisor gains write, approval, amendment, delegation, selection,
  or authority-expansion capability.
- Stop if any temporary surface lacks a caller, reason, current owner, future
  owner, and CCFG-29 removal condition.
- Stop if work mutates runtime Codex state, the default generation, candidate
  code, the superseded CCFG-26 artifacts, or unrelated dirty files.
