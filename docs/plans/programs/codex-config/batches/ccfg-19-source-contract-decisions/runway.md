# CCFG-19 Source Contract Decisions Runway

## Purpose

Verify the accepted command-owner source contracts against current source and
tests, then record the blocking target decisions needed by later redesign
findings. The implementation result is one candidate-owned design record plus
accepted decision-register updates; no runtime implementation occurs.

This runway covers CCFG-19 only. Closeout may mark CCFG-19 `Closed` only when
every acceptance key is evidenced and OPEN-003 is resolved. If one blocking
decision remains unresolved, close the batch with explicit evidence, leave
CCFG-19 `Blocked`, and stop without selecting a successor.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`.
- Slice 1 risk: `evidence-only`.
- Slices 2, 3, and 4 risk: `decision-only`.
- Migration: forbidden.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Destructive, contract-narrowing, and migration approval gates: none, because
  no such slice is authorized.
- User decision gate: required after Slice 1 review and before Slice 2. The
  coordinator must present a compact evidence-backed recommendation packet for
  schema evolution, `ledger-store`, the runner protocol, and OPEN-003. Slices 2
  through 4 may record only the user's explicitly approved or amended
  decisions. Silence is not approval.
- Candidate-checkout filesystem approval may be required at execution time.
  That approval authorizes access only; it does not widen the allowed files,
  finding scope, or lifecycle authority.

## Current Baseline And Assumptions

- Planning Artifact Layout v1 is active at
  `/home/alacasse/projects/codex-config/docs/plans`.
- Program root:
  `/home/alacasse/projects/codex-config/docs/plans/programs/codex-config`.
- Planning-state `current` and `validate` pass with no blockers and only the two
  known redirect-ledger warnings.
- Selected dispatch, queued runway, and active runway were all `None` before
  this planning pass.
- Stable checkout:
  `/home/alacasse/projects/codex-config`, branch `master`, exact `HEAD`
  `e1946ad41df24190c0938ffa171426a34c027c0e`.
- Candidate checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`, exact `HEAD`
  `9027bd1ea35e66e263dfced02a2b9f91835c1bd9`.
- Both worktrees were clean before planning. Planning performs no candidate
  write.
- Stable and candidate installer status and dry-run checks pass and keep every
  managed link bound to its declared generation.
- Accepted immutable design snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- CCFG-18 durable evidence proves authoritative base
  `da5b97165eb8d8c9f809a64937bcc9d753032ee7`, ancestry-preserving merge
  `b044e3c348922663aa074638227aae8d2633cfe3`, candidate head `9027bd1`,
  isolated candidate installation, and unchanged stable default generation.
- The accepted design has 31 behavior contracts. It lacks one joined
  source/owner/scenario matrix, references 15 scenario IDs absent from the
  scenario catalog, and has no durable classification for the 28 current
  `tests/test_*.py` modules.
- OPEN-003 remains the only planning-transaction blocker owned by CCFG-19.
- Baseline focused validation is green: 285 source/topology tests, 3 focused
  cross-checkout manifest tests, and 31 workflow-boundary tests pass.
- Full `tests/test_codex_features_manifest.py` remains at the documented
  known-red baseline of 3 failures and 18 passes in unrelated exact-wording
  assertions.

The queued planning artifacts in the stable checkout are expected dirty
coordination state. Do not copy them into the candidate checkout or include
them in candidate implementation commits. If either repository `HEAD` moves,
regenerate and revalidate the complete strict context before delegation; do not
edit revision fields by inspection.

## Batch Non-Goals

- Do not implement `skill-contract/v1` or any planning-artifact schema.
- Do not create a `ledger-store` module, API, fixture, or test.
- Do not change `planning-state`, runner, command-owner, worker, reviewer,
  installer, manifest, or agent behavior.
- Do not transfer ownership from APR or Batch Runway.
- Do not rewrite, delete, or preserve source topology through new tests.
- Do not add compatibility aliases, fallback paths, parallel skill catalogs,
  or versioned command names.
- Do not modify accepted immutable history; evolve only the live candidate
  design record.
- Do not select, dispatch, queue, or prepare CCFG-20 or any later finding.

## Required Strict Execution Context

Mode: explicit `cross-checkout-context/v1`.

Installed helper path used for planning validation:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Canonical planning root:

```text
/home/alacasse/projects/codex-config/docs/plans
```

Complete validated payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: e1946ad41df24190c0938ffa171426a34c027c0e
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: e1946ad41df24190c0938ffa171426a34c027c0e
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 9027bd1ea35e66e263dfced02a2b9f91835c1bd9
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Planning loaded the installed stable helper, verified that it resolves under
the declared toolchain root, parsed the complete payload, and called
`validate_write_scope` with the explicit canonical planning root and the exact
four planning paths for program `CURRENT.md`, `LEDGER.md`, `dispatch.md`, and
`runway.md`. Validation passed.

Before every worker or reviewer delegation, the execution coordinator must
follow `skills/batch-runway/references/cross-checkout-context-v1.md`, revalidate
the exact then-current payload and intended paths, and pass the payload,
canonical planning root, absolute helper path, and write-bearing/read-only mode.
Every explicit cross-checkout agent result must carry matching non-null
`verified_cross_checkout_context` evidence.

## Project Values

- Planning location:
  `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/`.
- Planning artifact layout: Planning Artifact Layout v1.
- Program root: `docs/plans/programs/codex-config/`.
- Selected batch directory:
  `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`.
- Output root: `None`.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/docs-only.md`.
- Integration harness: not required.
- Harness output: `None`.
- Summary artifact: this runway, `completed-slices.md`, and `closeout.md`.
- Index refresh: none.
- Commit requirements: one focused candidate commit per accepted slice plus a
  separate stable planning-ledger receipt after the candidate hash exists.
- Dirty-file constraints: candidate starts clean and may change only the files
  named by the active slice; stable changes are limited to this batch's
  canonical planning artifacts and same-batch reconciliation.
- Test quality review: not requested.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2. Registered agent TOMLs
own worker, reviewer, specialist, investigator, and Spark result schemas.
Use Batch Runway Compact Report Contract v1 only for coordinator receipts and
its other non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about
suspicious coordinator or subagent-lifecycle behavior.
Use the expanded convergence template only when scope is expanding,
significant uncertainty exists, blockers are present, or final batch reporting
is being produced.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`

Overrides:

- Candidate design commits and stable planning-ledger receipt commits are
  distinct cross-repository commits. Record both hashes per slice.
- No project integration harness runs because the batch changes design docs
  only. Focused source-characterization tests run at final validation from the
  candidate checkout.

## Validation Profile And Status Classes

Profile: `docs-only`.

Per-slice required-green command:

- `git diff --check`

Run it from the candidate checkout for candidate changes and from the stable
checkout for coordinator-owned planning changes.

Per-slice diagnostic command:

- `git status --short`
  - The command's exit code is not a green gate. The coordinator must compare
    its exact output against the active slice's allowed candidate files and the
    canonical stable planning allowlist. Any unexpected path stops the batch.

Final required-green commands, run from the candidate checkout unless the
command uses an absolute stable path:

- `python -m pytest tests/test_planning_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_run_loop.py tests/test_cross_checkout_context.py tests/test_cross_checkout_precreation.py tests/test_custom_agent_contracts.py -q`
- `python -m pytest tests/test_codex_features_manifest.py -q -k 'cross_checkout_helper_is_installed_only_by_batch_runway or cross_checkout_consumers_share_the_temporary_runtime_contract or cross_checkout_generic_surfaces_remain_project_neutral'`
- `python -m pytest tests/test_skill_routing_rule_ownership.py tests/test_architecture_program_runway_status_vocabulary.py tests/test_batch_runway_create_spec_contract.py tests/test_batch_lifecycle_guards.py -q`
- `git merge-base --is-ancestor caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c HEAD`
- `git merge-base --is-ancestor da5b97165eb8d8c9f809a64937bcc9d753032ee7 HEAD`
- `git diff --check 9027bd1ea35e66e263dfced02a2b9f91835c1bd9..HEAD`
- `python /home/alacasse/projects/codex-config/scripts/planning_state.py current --root /home/alacasse/projects/codex-config/docs/plans`
- `python /home/alacasse/projects/codex-config/scripts/planning_state.py validate --root /home/alacasse/projects/codex-config/docs/plans`

Known-red-baseline command:

- `python -m pytest tests/test_codex_features_manifest.py -q`
  - Baseline: 3 failed, 18 passed.
  - Role: diagnostic only; this batch does not edit the asserted command-owner
    prose and must not claim to remediate or promote this command.

Implementation-created command:

- `test -f docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`
  - Created by Slice 1 and promoted to required-green after that slice.

Conditional commands:

- Stable and candidate `./install.sh --status` and `./install.sh --dry-run` run
  only if an allowed diff unexpectedly touches installed-feature metadata or a
  managed link. Such a diff is otherwise a scope violation and stops the batch.

No per-slice worker may run project-level integration harnesses, graph/index
refreshes, generated-doc refreshes, package installs, or final validation.

## Shared Worker And Reviewer Briefs

Worker brief for every slice:

- You are the already-required `runway_worker`; implement only the active slice
  from this runway and do not spawn, delegate to, or wait on another agent.
- Independently validate the strict cross-checkout context before reading or
  writing, then write only inside the candidate checkout and only to the active
  slice's allowed files.
- Treat source, tests, accepted history, CCFG-18 evidence, and all other design
  files as read-only evidence.
- Do not implement code, tests, schemas, validators, stores, transactions,
  runner behavior, ownership transfer, or cleanup.
- Return the registered v2 worker result with exact changed files, validation,
  residual risks, and matching `verified_cross_checkout_context`.

Reviewer brief for every slice:

- The coordinator supplies the exact candidate commit hash or task-scoped
  candidate worktree diff basis. Echo it as `diff_basis` in the registered v2
  reviewer result.
- Independently validate the strict cross-checkout context before review.
- Verify factual source links, complete acceptance evidence, lack of duplicate
  decision ownership, and absence of implementation or deferred-scope changes.
- Reject evidence-free booleans, invented scenario mappings, prose that treats
  accidental topology as a supported contract, and decisions that silently
  absorb CCFG-20 through CCFG-29.
- Return matching `verified_cross_checkout_context` and a clear accept/fix/block
  verdict.

## User Decision Approval Gate

Timing: after Slice 1 has an accepted candidate commit and stable receipt, and
before any Slice 2 worker handoff.

Approval authority: the user.

The coordinator must present one compact packet containing:

- Slice 1's joined evidence and any blocking ownership conflicts;
- the proposed closed-world v1 schema-evolution rule and explicit-exception
  mechanism;
- the proposed whole-ledger CAS and apply-only `ledger-store/v1` boundary;
- the proposed runner public-command and no-successor-readiness boundary;
- the proposed idempotent staged saga for OPEN-003, including visible partial
  evidence and retry rules; and
- any source contradiction, alternative, or residual risk that could change a
  decision.

Record the user's exact approval or amendments in the stable runway ledger
before Slice 2. Propagate only those approved outcomes to Slices 2 through 4.
If the user does not approve a complete decision set, stop with the queued or
active batch intact. If the user explicitly decides that a blocking item cannot
be resolved in this batch, record that decision and close the batch with
CCFG-19 `Blocked`; do not guess or select a successor.

## Execution Ledger

| Slice | Risk | Status | Candidate commit | Stable receipt | Focused validation | Review | Notes |
|---|---|---|---|---|---|---|---|
| 1. Join contract evidence | evidence-only | Pending | None | None | Pending | Pending | Creates the joined record and README link. |
| 2. Accept schema and ledger boundaries | decision-only | Pending | None | None | Pending | Pending | No schema or store implementation. |
| 3. Accept runner boundary and verify topology | decision-only | Pending | None | None | Pending | Pending | No runner or installer implementation. |
| 4. Resolve OPEN-003 and audit exit gate | decision-only | Pending | None | None | Pending | Pending | Close or explicitly block CCFG-19; no successor. |

Completed slice details move to `completed-slices.md` after each accepted stable
receipt. Keep only active rows and compact evidence here.

## Slice 1: Join Contract, Owner, Scenario, And Test Evidence

Risk: `evidence-only`.

Scope:

- Create
  `docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`
  in the candidate checkout.
- Join all 31 accepted behavior contract IDs to current source evidence, one
  target decision owner, behavioral scenario IDs, and a source-versus-accidental
  classification.
- Define or explicitly remap these currently absent scenario IDs:
  `current-state-diagnostic`, `duplicate-machine-fact-owner`,
  `historical-artifact-does-not-override-current`, `illegal-state-transition`,
  `invalid-planning-state`, `legal-state-transitions`, `missing-current-file`,
  `partial-execution`, `resume-after-interruption`,
  `stale-placeholder-closeout`, `stale-state-revision`,
  `structured-prose-contradiction`, `legacy-evidence-no-state-writes`,
  `deletion-evidence-no-state-writes`, and
  `test-quality-review-no-state-writes`.
- Classify every current `tests/test_*.py` module as behavioral, schema,
  integration, migration-retention, topology, text-contract, or historical.
  Mixed modules must name method-level exceptions and a retain, rewrite,
  replace, or delete-after-migration disposition.
- Link the new record from the candidate design README.

Allowed files:

- `docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`
- `docs/design/command-owner-redesign/README.md`

Non-goals:

- No accepted decision changes.
- No source or test changes.
- No inference that current file topology is a target contract.

Acceptance criteria:

- All 31 contract IDs have source, target owner, scenario, classification, and
  test-disposition evidence.
- Every referenced scenario ID exists in the catalog or has one explicit,
  justified remapping.
- Every current test module has a primary classification; mixed cases have
  method-level exceptions.
- `blocking_ownership_conflicts` is computed from the joined evidence, not
  asserted without support.
- The README links the new record as the live CCFG-19 candidate amendment.

Validation: `docs-only`; per-slice required-green commands only.

Test quality review: not requested.

Commit message: `docs: map CCFG-19 contract evidence`.

Subagent briefs: use the shared worker and reviewer briefs above. The reviewer
must sample every contract family and inspect every claimed ownership conflict.

Stop conditions:

- Stop if a contract has no defensible source evidence or one target owner.
- Stop if the matrix requires changing source or tests to make evidence fit.
- Stop if a missing scenario cannot be defined without inventing behavior.

## Slice 2: Accept Schema-Evolution And Ledger-Store Boundaries

Risk: `decision-only`.

Scope:

- After the user decision gate, record the approved schema-evolution decision.
  The recommended decision is: writers emit v1; unknown
  versions block; unknown fields within v1 are rejected unless an explicit
  schema allowlist accepts them; optional additions require an accepted
  compatibility decision and coordinated reader-before-writer rollout;
  required-field or semantic ownership changes require a new version; explicit
  per-schema exceptions are named and bounded.
- After the same gate, record the approved apply-only `ledger-store/v1`
  boundary. The recommended decision is: whole-ledger CAS,
  touched-finding revisions, exact idempotency-key replay, key/payload mismatch
  rejection, deterministic rendering, atomic replacement, and recoverable
  ledger-written/receipt-missing evidence.
- Preserve semantic duplicate, selection, scope, closeout, and successor
  decisions in command owners rather than `ledger-store`.
- Update the joined record with source evidence, conflicts, acceptance keys,
  and deferred implementation owner IDs.

Allowed files:

- `docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`
- `docs/design/command-owner-redesign/decisions.md`

Non-goals:

- No schema, parser, validator, store, mutation API, receipt writer, fixture, or
  test implementation.
- No changes to existing command-owner or planning-state behavior.

Acceptance criteria:

- Unknown-version, unknown-field, optional-addition, required-change,
  semantic-change, deprecation, producer-generation, and explicit-exception
  behavior is unambiguous.
- The `ledger-store` read/apply inputs, outputs, allowed mechanical checks,
  forbidden semantic decisions, CAS, idempotency, atomicity, deterministic
  rendering, and receipt-recovery semantics are unambiguous.
- Existing strict validators and permissive planning-state examples are
  classified as evidence, not silently standardized by this slice.
- `schema_evolution_policy_accepted: true` and
  `ledger_store_boundary_accepted: true` are supported by user-approved
  decision IDs and the stable approval receipt.

Validation: `docs-only`; per-slice required-green commands only.

Test quality review: not requested.

Commit message: `docs: decide CCFG-19 schema and ledger boundaries`.

Subagent briefs: use the shared worker and reviewer briefs above. The reviewer
must reject any decision that grants `ledger-store` semantic workflow authority.

Stop conditions:

- Stop before writing accepted decisions if the user gate is absent, partial,
  or ambiguous.
- Stop if the policy creates incompatible v1 readers without an explicit
  rollout rule.
- Stop if idempotency or receipt recovery cannot distinguish exact replay from
  a different mutation using the same key.
- Stop if the decision begins CCFG-20, CCFG-21, or CCFG-24 implementation.

## Slice 3: Accept Runner Boundary And Verify Generation Topology

Risk: `decision-only`.

Scope:

- After the user decision gate, record the approved target runner protocol.
  The recommended protocol is: invoke public `plan-batch` and
  `work-batch` command protocols, validate their results, own explicit loop
  bounds and child-process lifecycle, and start a fresh `plan-batch` invocation
  for a later successor without interpreting closeout readiness.
- Mark current direct APR/Batch Runway phase routing, closeout readiness,
  closeout-to-select transition behavior, and topology-only tests as future
  rewrite/delete targets under their existing later findings.
- Verify and link CCFG-18 evidence for stable/candidate roots, generation
  identities, authoritative base, accepted snapshot, ancestry merge, candidate
  branch/head, isolated candidate install, canonical-write rejection, and
  unchanged default generation.
- Update the joined record and accepted decision register only.

Allowed files:

- `docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`
- `docs/design/command-owner-redesign/decisions.md`

Non-goals:

- No runner, transition, validation, CLI, installer, manifest, agent, or test
  changes.
- No default-generation switch or cross-checkout bridge removal.

Acceptance criteria:

- The runner public-command protocol and explicit loop-bound behavior have one
  accepted decision owner.
- Successor readiness is absent from the target runner result and transition
  semantics.
- Current conflicting runner paths and tests have explicit later-finding
  dispositions rather than being treated as target contracts.
- CCFG-18 root, generation, lineage, branch, installation, quiescence, and
  rollback facts link to durable evidence.
- `runner_target_protocol_accepted: true` and topology verification are
  supported by the record, the user-approved decision ID, and the stable
  approval receipt.

Validation: `docs-only`; per-slice required-green commands only.

Test quality review: not requested.

Commit message: `docs: decide CCFG-19 runner and topology boundaries`.

Subagent briefs: use the shared worker and reviewer briefs above. The reviewer
must distinguish supported runner behavior from accidental phase topology.

Stop conditions:

- Stop before recording the target protocol if the user gate is absent,
  partial, or ambiguous.
- Stop if the target protocol preserves successor-readiness interpretation.
- Stop if lineage or generation evidence contradicts the strict context.
- Stop if the slice changes candidate runtime or installation behavior.

## Slice 4: Resolve OPEN-003 And Audit The CCFG-19 Exit Gate

Risk: `decision-only`.

Scope:

- After the user decision gate, resolve OPEN-003 with the approved planning
  transaction. The recommended decision is an idempotent staged saga:
  1. write and validate the dispatch;
  2. CAS idle to selected and persist a transition receipt;
  3. write and validate a runway bound to the dispatch revision;
  4. CAS selected to queued and persist a transition receipt.
- Bind all four stages to one transaction/idempotency ID. Retry may resume only
  the same batch and exact artifact lineage; key/payload or lineage mismatch
  blocks. Partial evidence remains visible; rollback deletion must not hide a
  dispatch, transition, runway, or receipt that was durably written.
- Record the fault model for failures before and after each artifact write,
  transition, and receipt, while leaving implementation/prototyping to CCFG-21
  and ownership transfer to CCFG-25.
- Audit every CCFG-19 acceptance key against the joined record and accepted
  decision IDs.
- Keep OPEN-004 through OPEN-008 explicitly non-blocking and deferred unless
  source evidence proves one is required for a CCFG-19 acceptance key.
- Update the README if final record naming or status changed.

Allowed files:

- `docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`
- `docs/design/command-owner-redesign/decisions.md`
- `docs/design/command-owner-redesign/README.md`

Non-goals:

- No planning transaction implementation, prototype, schema, fixture, or fault
  injection test.
- No universal resolution of commit profile, exact slice count, final module
  split, worker/reviewer names, or prototype retention.

Acceptance criteria:

- OPEN-003 is resolved by one accepted decision with stage order, CAS inputs,
  transaction identity, idempotent retry, mismatch rejection, visible partial
  evidence, receipt recovery, and deletion prohibition, and the accepted
  decision matches the user's approval receipt.
- The joined record evidences:
  `contract_to_owner_map_complete: true`,
  `contract_to_scenario_map_complete: true`,
  `blocking_ownership_conflicts: 0`,
  `schema_evolution_policy_accepted: true`,
  `ledger_store_boundary_accepted: true`,
  `runner_target_protocol_accepted: true`, and
  `planning_transaction_ready_or_explicitly_blocked: true`.
- If any other acceptance key cannot be true, the exact blocker is named and
  CCFG-19 remains `Blocked`; do not soften or omit the failed key.
- The final record names CCFG-20 through CCFG-29 as deferred implementation and
  selects none of them.

Validation: `docs-only`; per-slice required-green commands plus all final
required-green commands.

Test quality review: not requested.

Commit message: `docs: resolve CCFG-19 planning transaction`.

Subagent briefs: use the shared worker and reviewer briefs above. Final review
must inspect the exact candidate range from `9027bd1` through the Slice 4 commit
and the stable planning range through same-batch closeout.

Stop conditions:

- Stop before resolving OPEN-003 if the user gate is absent, partial, or
  ambiguous.
- Stop with CCFG-19 `Blocked` if the staged saga conflicts with verified source
  or cannot define idempotent recovery without guessing.
- Stop if any acceptance key is asserted without traceable evidence.
- Stop before implementation or successor selection.

## Final Validation And Closeout

1. Revalidate strict context and exact candidate/stable paths.
2. Run the three required-green focused pytest commands in the candidate
   checkout. Pytest cache warnings caused solely by a read-only sandbox cache
   path do not change a green exit result.
3. Re-run both ancestry checks and the candidate-range `git diff --check`.
4. Write `completed-slices.md` and `closeout.md` beside this runway.
5. Reconcile only CCFG-19 in program `CURRENT.md` and `LEDGER.md`:
   - mark `Closed` only if all seven acceptance keys are evidenced and OPEN-003
     is resolved;
   - otherwise mark `Blocked` with the exact remaining decision and dependency
     impact.
6. Clear selected, queued, and active state for this batch; point
   `latest_closeout` at the CCFG-19 closeout.
7. Run stable planning-state `current` and `validate`.
8. Obtain independent final review with matching strict identity over the exact
   candidate commit range and the task-scoped stable planning diff through
   completed slices, closeout, `CURRENT.md`, and `LEDGER.md`. If review finds a
   defect, delegate correction and repeat focused validation and final review.
9. Create the self-referential final stable closeout commit using
   `this closeout commit`, then verify the commit receipt and planning state.
10. Stop without selecting, dispatching, queuing, refreshing, or preparing
   CCFG-20 or any other successor.

## Global Stop Conditions

- Stop on any strict context, helper, revision, root, generation, or write-scope
  mismatch.
- Stop on unrelated candidate or stable dirty files that overlap the active
  slice or planning updates.
- Stop if required subagent support is unavailable.
- Stop if a worker or reviewer lacks matching non-null strict identity.
- Stop on source/test changes, schema/store/transaction/runner implementation,
  ownership transfer, migration, contract narrowing, or destructive cleanup.
- Stop if full manifest known-red failures change count or identity; investigate
  the drift before accepting final validation.
- Stop if any slice absorbs work owned by CCFG-20 through CCFG-29.
- Stop after same-batch closeout with no successor selected.

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

Record only suspicious coordinator or subagent-lifecycle behavior here. Routine
validation output, clean reviews, commit chronology, and expected cross-checkout
approval prompts do not belong in this log.

## Convergence Assessment

- Phase: planning complete; execution not started.
- Scope trend: bounded to one design-only CCFG-19 amendment.
- Closed in this planning pass: none.
- Remaining slices: four.
- Blockers: none at planning time.
- Completion forecastable: yes, subject to the explicit OPEN-003 evidence gate.
- Successor selected: no.
