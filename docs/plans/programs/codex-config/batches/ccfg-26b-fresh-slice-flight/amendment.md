# CCFG-26B Fresh Slice Flight Bounded Planning Amendment

## Status And Precedence

- Status: bounded planning amendment; it controls execution only when
  amendment-review.md records a clean verdict for its exact SHA-256.
- Applies to: the already queued ccfg-26b-fresh-slice-flight batch.
- Scope: planning correction only; implementation has not started.
- Precedence: when this document conflicts with dispatch.md or runway.md, this
  amendment controls. Unchanged original requirements remain in force.
- Queue effect: none. The queued path remains runway.md in this directory.
- Successor effect: none. CCFG-26C through CCFG-26E and CCFG-27 through
  CCFG-29 remain unselected and unprepared.

The existing dispatch, queued runway, and original review are immutable
historical evidence. This amendment does not rewrite, replace, or reinterpret
their bytes:

~~~yaml
original_evidence:
  dispatch:
    path: docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/dispatch.md
    sha256: 8b29b566fd743af4ecdbe555f1cf66bb29871b081bc25f7aa0fc9780ce1069d8
  queued_runway:
    path: docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/runway.md
    sha256: 8da8e0d1b0cd18d75289a1a0954b33078dd17ef6a328d2bb6a46a9404076b5ca
  original_review:
    path: docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/review.md
    sha256: e37e0678c663a44c99b642454fa4fc6b840bc59174c8df6727d10bb02ad2f45f
  original_reviewed_draft_runway_sha256: d3d3cac9136cdd2aa84ac92daa92d893c2ebc2d75acdfc33737b72db21717ee2
immutable_planning_snapshot:
  toolchain_commit: 8aec9c2bcf87f619012b6dfc748ef46387515298
  canonical_planning_commit_before: 8aec9c2bcf87f619012b6dfc748ef46387515298
  implementation_commit_before: 5c5ec9d52dd9033daa45f3a200031c152363b62c
amendment_authoring_observation:
  canonical_planning_head: 9b5b9d4cd9279424c6b75ffc8b28670832d8cc2f
  implementation_head: 5c5ec9d52dd9033daa45f3a200031c152363b62c
  note: current authoring evidence only; it does not replace the immutable planning snapshot
~~~

The selected finding, batch identity, source evidence, candidate baseline,
canonical planning baseline, and deferred child boundaries are unchanged.
Before implementation, work-batch must consume dispatch.md, runway.md,
review.md, this amendment, and the clean amendment-review.md as one execution
basis, then obtain a fresh live lease through the unchanged strict preflight.

## Amended Batch Shape

CCFG-26B contains exactly two implementation slices:

1. transfer one successful implementation-slice flight to work-batch and stop
   durably with manual continuation available; and
2. consume the first flight's continue_same_batch action to automate a fresh
   same-batch process, retain ordered evidence, and stop durably at
   finalize_same_batch after the last implementation slice.

Final-range validation, candidate installation, stable-home comparison,
exact-commit acceptance, final test-quality review, final independent review,
and same-batch closeout remain batch gates. They are not a third implementation
slice.

~~~yaml
shape:
  selected: vertical
  override_reason: null
slice_shape:
  initial_count: 1
  final_count: 2
  boundaries:
    - edge: 1 -> 2
      split_condition: Slice 2 consumes the durable continue_same_batch receipt produced by Slice 1 and adds a distinct process-launch, ordered-retention, and rollback boundary
      valid_intermediate_state: after Slice 1, one complete flight is durable, the runner has stopped without relaunch, and a later manual invocation can resume from canonical state and the receipt without chat history
  rejected_splits:
    - schema declaration alone is inert because it has no real producer and consumer
    - final validation or convergence is a batch gate rather than an implementation slice
~~~

The temporary stable one-implementation-slice-per-invocation policy still
governs execution of this amended runway. Slice 1 and Slice 2 therefore require
separate explicit stable work-batch invocations. The target candidate behavior
implemented by Slice 2 may automatically launch a later fresh same-batch
coordinator only inside its focused behavioral proof; it does not cause stable
execution of this amendment to start the next planning slice automatically.

## Source Audit And Semantic Replacement

The current candidate at
5c5ec9d52dd9033daa45f3a200031c152363b62c establishes these old rules:

- skills/work-batch/SKILL.md routes normal execution to Batch Runway
  execute-spec and describes completion after that support returns;
- scripts/architecture_program_runner_phase_contract.py routes serialized
  execute directly to Batch Runway execute-spec;
- architecture_program_runner_validation.py maps a completed execute result to
  closeout, while architecture_program_runner_transition.py and the runner loop
  apply that phase result;
- architecture_program_runner_state.py allocates one phase-keyed execute
  receipt, and architecture_program_runner_artifacts.py retains receipts and
  inventories in phase-keyed maps;
- docs/skill-routing-contract.md names Batch Runway as the owner of execution
  for an already queued or active runway and routes work-batch through
  Batch Runway execute-spec.

This amendment requires a semantic substitution, not a literal-string-only
edit:

~~~yaml
semantic_replacement:
  old_rules:
    - public work-batch routes the complete runway to batch-runway execute-spec
    - the serialized runner execute phase invokes batch-runway execute-spec
    - the routing contract names Batch Runway as the happy-path execution lifecycle owner
    - runner validation infers completed execute means closeout
  new_authority:
    - public work-batch owns one successful implementation-slice lifecycle and authors its exact durable next action
    - the runner owns fresh process launch, bounded persistence, validation, and mechanical transition only
  superseded_surfaces:
    - path: skills/work-batch/SKILL.md
      disposition: replaced
      requirement: remove the direct happy-path execute-spec route and define one-slice lifecycle authorship
    - path: scripts/architecture_program_runner_phase_contract.py
      disposition: replaced
      requirement: serialized execute launches public work-batch
    - path: scripts/architecture_program_runner_validation.py
      disposition: replaced
      requirement: validate the work-batch-authored flight result and action without inferring completion or correction
    - path: scripts/architecture_program_runner_transition.py
      disposition: conditioned_on_new_authority
      requirement: apply only the exact validated action
    - path: scripts/architecture_program_runner.py
      disposition: conditioned_on_new_authority
      requirement: persist and stop or relaunch mechanically; never choose the action
    - path: skills/architecture-program-runway/references/local-runner-v1.md
      disposition: replaced
      requirement: describe execute as a public work-batch flight and condition later closeout on retained support
    - path: docs/skill-routing-contract.md
      disposition: replaced
      requirement: name work-batch as happy-path lifecycle owner and Batch Runway as bounded temporary support
  retained_overlays:
    - surface: Batch Runway recovery support
      owner: CCFG-26C
      removal_condition: CCFG-26C replacement exists and CCFG-26E performs final displaced-owner narrowing
    - surface: Batch Runway final validation and finalization support
      owner: CCFG-26D
      removal_condition: CCFG-26D replacement exists and CCFG-26E performs final displaced-owner narrowing
    - surface: Architecture Program Runway closeout reconciliation support
      owner: CCFG-26E
      removal_condition: CCFG-26E closeout ownership cutover
    - surface: temporary stable vertical and one-slice execution policy
      owner: CCFG-29 integration
      removal_condition: CCFG-29 proves equivalent candidate behavior and removes the policy hook
  forbidden_residue:
    - any active happy-path caller that directly invokes batch-runway execute-spec
    - any runner rule that infers slice acceptance or next action
    - any public routing rule that names Batch Runway as the happy-path lifecycle decision owner
    - any silent fallback from work-batch to the former happy-path owner
  counterfactuals:
    - restoring runner execute routing to batch-runway execute-spec must fail
    - restoring Batch Runway happy-path ownership in the routing contract must fail
    - removing the work-batch-authored next action must block before persistence or transition
~~~

Batch Runway and Architecture Program Runway skill semantics remain read-only
in CCFG-26B. Their still-needed recovery, finalization, and closeout procedures
are bounded support, not alternate happy-path decision owners.

### Mechanism Classification

| Candidate surface | Classification | Boundary |
|---|---|---|
| architecture_program_runner_environment.py | conditioned on new authority | select the work-batch-owned result schema for execute; retain the generic phase schema for other labels |
| local-runner-phase-result.schema.json | intentionally retained support | unchanged for select-dispatch, create-spec, and closeout unless a focused dispatch test proves a minimal conditioning edit |
| architecture_program_runner_state.py | conditioned on new authority | Slice 1 retains one resumable flight; Slice 2 adds ordered unique execute-flight identity |
| architecture_program_runner_artifacts.py | conditioned on new authority | persist exact flight evidence in Slice 1, then retain multiple ordered entries without overwrite in Slice 2 |
| architecture_program_runner_input_inventory.py | conditioned on new authority | Slice 2 rejects forbidden prior-context material; no new execution store |
| architecture_program_runner_workers.py | intentionally retained mechanism | existing fresh CodexExecWorker boundary is reused unless a failing identity test proves a minimal change |
| architecture_program_runner_phase_observation.py | intentionally retained read-only mechanism | existing post-subprocess Codex session discovery is the observation source; runner/artifact/state consumers use it without editing the observer |
| architecture_program_runner_command.py | intentionally retained mechanism | existing phase-contract renderer is reused unless a focused prompt test fails |
| runway_worker.toml and runway_reviewer.toml | intentionally retained authority | roles and separation do not change; only an identity-echo failure may permit a minimal edit |
| command-owner behavioral scenarios | conditioned on new authority | add producer-to-consumer and no-successor proof without manufacturing terminal runner state |
| Batch Runway skill | deferred bounded support | no happy-path caller after Slice 1; recovery and finalization support expire through CCFG-26C, CCFG-26D, and final narrowing in CCFG-26E |
| Architecture Program Runway skill | deferred bounded support | closeout support expires in CCFG-26E |

### Guidance Audit

| Surface at candidate baseline | Classification | CCFG-26B action |
|---|---|---|
| docs/skill-routing-contract.md owner split and routing table | replaced; active contradiction | required Slice 1 edit and counterfactual ownership test |
| skills/work-batch/SKILL.md happy-path execute-spec route | replaced; active contradiction | required Slice 1 edit |
| docs/workflow-guide.md | conditioned on the new authority; its unqualified Batch Runway execution-support wording is an active ambiguity | required Slice 1 edit limited to successful-slice ownership versus retained recovery/finalization support |
| README.md command-owner and support tables | conditioned on the new authority; its unqualified behind-work-batch wording is an active ambiguity | required Slice 1 edit limited to the same owner/support split |
| codex-features.json work-batch and Batch Runway descriptions | happy-path slice-execution claim replaced; dependency retained as conditioned support | required Slice 1 edit: describe work-batch as successful-slice owner, describe Batch Runway only as temporary CCFG-26C recovery and CCFG-26D finalization support, retain the dependency through those replacements, and update feature versions/tests |
| docs/design/command-owner-redesign/README.md, decisions.md, 04-migration-program.md, 06-deletion-conditions.md, and 07-implementation-ledger-intake.md | intentionally retained authority | unchanged; they already name work-batch as the permanent execution owner and the runner as process-lifecycle mechanism |
| skills/batch-runway/** | deferred bounded support | read-only; CCFG-26C and CCFG-26D replace remaining behavior and CCFG-26E narrows displaced ownership |
| skills/architecture-program-runway/SKILL.md | deferred bounded support | read-only; CCFG-26E replaces closeout reconciliation |

## Corrected Flight Result Contract

Slice 1 creates the minimum real producer and consumer for
batch-execution-flight/v1. The contract is owned under
skills/work-batch/references/batch-execution-flight-v1.schema.json and contains
only values with a CCFG-26B producer, validator, persistence behavior, and
deterministic stop or transition.

~~~yaml
interface: batch-execution-flight/v1
phase: execute
receipt_path: string
input_inventory_path: string
telemetry_path: string
flight_id: string
program_ledger: string
dispatch_path: string
spec_path: string
batch_id: string
slice_id: string | null
status: completed | blocked | failed
stop_reason: string | null
candidate_before: full-git-sha
candidate_after: full-git-sha
validation_summary: string | null
review_summary: string | null
commit_receipt: string | null
orchestration_anomalies: []
bounded_inputs:
  flight_identity: {flight_id: string, receipt_path: string, input_inventory_path: string, telemetry_path: string}
  planning_state_diagnostic: {path: string, sha256: string}
  active_runway: {path: string, sha256: string, slice_id: string | null}
  amendment: {path: string, sha256: string}
  amendment_review: {path: string, sha256: string}
  validation_profile: {path: string, sha256: string}
  candidate_head: full-git-sha
  candidate_worktree_status: string
  prior_flight_receipt: {path: string, sha256: string} | null
  unresolved_orchestration_anomalies: []
  retained_migration_facts: []
  strict_execution_lease: {interface: cross-checkout-context/v1, sha256: string}
work_metrics:
  files_changed: integer
  lines_added: integer
  lines_removed: integer
  validation_command_count: integer
  validation_command_breadth: []
  support_agents: []
  review_lenses: []
  blocker_recovery_transitions: []
next_action:
  kind: continue_same_batch | finalize_same_batch | require_user
  next_slice_id: string | null
~~~

There is no closeout action in this version. A later child may evolve or
version the contract when it has a real producer and consumer; CCFG-26B does
not reserve an unowned placeholder.

The runner preallocates flight_id and the three artifact paths, places them in
bounded_inputs.flight_identity, and requires work-batch to echo them exactly.
They are correlation identifiers known before launch, not claims about the
eventual Codex session. The Codex-compatible JSON Schema layer must encode the exact field set, enums,
types, requiredness, and structural nullability without oneOf, anyOf, if, then,
else, or another unsupported output-schema keyword. The deterministic runner
validator owns the cross-field contract: it must accept exactly the following
four combinations, validate receipt/state/action consistency, and reject every
other structurally valid combination before persistence or transition.
Focused tests must exercise both the structural schema layer and the
deterministic combination layer:

| Produced result | Author | Validator | Durable persistence | Mechanical behavior | Forbidden behavior |
|---|---|---|---|---|---|
| completed plus continue_same_batch and exact non-null next slice | work-batch after worker, focused validation, independent review, commit, ledger update, and archive are accepted | runner validates schema, exact receipt equality, echoed flight identity, current batch/slice/revision, and action consistency | work-batch atomically writes the exact receipt; after subprocess exit the runner writes its separate observation telemetry and persists both exact paths, the observed session identity, inventory, and accepted commit in ordered manifests | Slice 1 stops with execute still resumable by a later manual invocation; Slice 2 relaunches one fresh same-batch coordinator | no second slice in the same coordinator; no successor selection; no inferred action |
| completed plus finalize_same_batch and null next slice | work-batch after the last implementation slice is fully accepted | runner validates last-slice identity and exact action | same ownership and ordered retention | stop durably at the handoff to CCFG-26D | no final validation, installation, finalization, closeout, or relaunch |
| blocked plus require_user and null next slice | work-batch when an authorized stop condition prevents completion | runner validates exact state, receipt equality, and action consistency | same ownership and ordered retention | persist, surface the reason, and stop | no retry, recovery, amendment, correction, relaunch, or transition |
| failed plus require_user and null next slice | work-batch when the coordinator can still author a truthful terminal result after failure | runner validates exact state, receipt equality, and action consistency | same ownership and ordered retention | persist, surface the reason, and stop | no retry, recovery, amendment, correction, relaunch, or transition |

For blocked or failed results, candidate_after is the exact observed candidate
HEAD. commit_receipt is non-null if and only if a commit was already accepted;
otherwise candidate_after equals candidate_before and commit_receipt is null.
The summaries and telemetry truthfully describe only gates reached. Completed
results require a non-null slice, validation, review, and commit receipt, an
accepted candidate movement, and a null stop_reason. Terminal results require a
non-empty stop_reason and require_user.

If failure occurs before work-batch can produce a schema-valid result, the
runner may report its own validation or launch failure, but it still may not
manufacture a work-batch action or recover autonomously.

### Runner-Owned Observation Telemetry

The byte-equal work-batch receipt contains only values available to work-batch
before it exits. The runner must not mutate or enrich that receipt. After the
subprocess exits and receipt equality is validated, the existing runner phase
telemetry mechanism writes a separate flight-keyed observation record at the
preallocated telemetry_path:

~~~yaml
flight_id: string
receipt_path: string
receipt_sha256: sha256
input_inventory_path: string
observed_codex_session_id: string | null
observed_codex_session_path: string | null
input_tokens: integer | null
output_tokens: integer | null
compaction_count: integer | null
duration_seconds: number
exit_code: integer
~~~

The runner is the sole author of these observations because the actual session
ID, process exit, session-file token events, compactions, and full duration are
available only after the work-batch subprocess exits. A completed flight
requires a non-null runner-observed session ID before transition. Terminal
results persist any observation available and stop. Slice 2 compares distinct
runner-observed session IDs and strict leases across the two flights; two
self-reported or merely echoed IDs cannot satisfy that proof. The ordered batch
manifest links the immutable work-batch receipt and runner-owned observation
without creating a second execution store.

### Bounded Fresh Inputs

A later coordinator may consume only the exact bounded_inputs object, the
current slice section it identifies, Planning State's current diagnostic, and
the fresh strict live lease. The runner must reject a manifest that contains
prior raw logs, chat transcripts, full chronology, prior worker transcripts,
or already accepted review detail. It may retain hashes and compact summaries
named by the contract. Every unavailable runner observation is explicit null
where allowed; work-metric arrays are present even when empty.

## Amended Write-Path Ceiling

### Canonical Planning Paths

The original canonical planning ceiling remains in force, with exactly these
two amendment artifacts added:

- docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/amendment.md
- docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/amendment-review.md

CURRENT.md and LEDGER.md may change only to bind the exact accepted amendment
and review to the already queued runway. dispatch.md, runway.md, and review.md
are read-only historical evidence. No queue path, batch ID, finding, baseline,
or successor state may change.

### Slice 1 Required Candidate Paths

- skills/work-batch/SKILL.md
- skills/work-batch/references/batch-execution-flight-v1.schema.json
- skills/architecture-program-runway/references/local-runner-v1.md
- scripts/architecture_program_runner.py
- scripts/architecture_program_runner_artifacts.py
- scripts/architecture_program_runner_environment.py
- scripts/architecture_program_runner_phase_contract.py
- scripts/architecture_program_runner_state.py
- scripts/architecture_program_runner_validation.py
- scripts/architecture_program_runner_transition.py
- docs/skill-routing-contract.md
- docs/workflow-guide.md
- README.md
- tests/test_work_batch_flight_contract.py
- tests/test_architecture_program_runner_artifacts.py
- tests/test_architecture_program_runner_environment.py
- tests/test_architecture_program_runner_phase_contract.py
- tests/test_architecture_program_runner_run_loop.py
- tests/test_architecture_program_runner_state.py
- tests/test_architecture_program_runner_validation.py
- tests/test_architecture_program_runner_transition.py
- tests/test_skill_routing_rule_ownership.py
- tests/test_command_owner_behavioral_scenarios.py
- tests/fixtures/command-owner-scenarios/**
- tests/test_codex_features_manifest.py
- codex-features.json
- CHANGELOG.md

### Slice 2 Required Candidate Paths

- skills/work-batch/references/batch-execution-flight-v1.schema.json
- scripts/architecture_program_runner.py
- scripts/architecture_program_runner_artifacts.py
- scripts/architecture_program_runner_environment.py
- scripts/architecture_program_runner_input_inventory.py
- scripts/architecture_program_runner_state.py
- scripts/architecture_program_runner_transition.py
- scripts/architecture_program_runner_validation.py
- tests/architecture_program_runner_test_support.py
- tests/test_work_batch_flight_contract.py
- tests/test_architecture_program_runner_artifacts.py
- tests/test_architecture_program_runner_environment.py
- tests/test_architecture_program_runner_run_loop.py
- tests/test_architecture_program_runner_state.py
- tests/test_architecture_program_runner_transition.py
- tests/test_architecture_program_runner_validation.py
- codex-features.json
- CHANGELOG.md

The original validated implementation ceiling already contains every path
above except architecture_program_runner_input_inventory.py. That file is
added to the amended ceiling only for Slice 2 bounded-input enforcement. The
fresh amendment review must bind and validate the complete amended path list.

### Conditional Or Read-Only Candidate Paths

- scripts/architecture_program_runner_command.py and its test are conditional
  only if a failing phase-contract test proves prompt rendering cannot remain
  behind architecture_program_runner_phase_contract.py.
- skills/architecture-program-runway/references/local-runner-phase-result.schema.json
  remains the generic result contract for non-execute phases and is read-only
  unless a focused schema-dispatch test proves a minimal conditioning change is
  required. Execute must use the work-batch-owned flight schema, not widen the
  generic schema with reserved combinations.
- scripts/architecture_program_runner_workers.py is conditional only if the
  deterministic two-flight test proves the existing fresh CodexExecWorker
  process boundary cannot perform the mechanical relaunch.
- scripts/architecture_program_runner_phase_observation.py is outside the
  amended write ceiling and remains read-only. It already discovers the actual
  Codex session only after subprocess exit; widening that observer requires a
  separate reviewed amendment.
- agents/runway_worker.toml, agents/runway_reviewer.toml, and
  tests/test_custom_agent_contracts.py are conditional only if a focused
  failing identity-echo test proves the registered roles cannot preserve the
  new flight identity. Their authority must not change.
- tests/test_batch_lifecycle_guards.py is conditional only when a changed
  lifecycle guard directly protects the no-finalization, no-closeout, or
  no-successor boundary.
- skills/batch-runway/** and skills/architecture-program-runway/SKILL.md remain
  read-only.
- All other candidate paths remain forbidden.

## Authoritative Migration Evidence Representation

At the candidate baseline, schemas/planning-runway-v1.schema.json and
scripts/plan_batch.py require exactly migration_evidence plus migration_matrix
for a migration-risk slice. They do not define vertical_slice. This amendment
therefore uses migration_evidence as the only live candidate representation.

The temporary stable dogfooding policy's vertical_slice block is an external
compatibility overlay through CCFG-29, not a second candidate contract. Stable
execution projects these fields directly from each slice's authoritative
migration_evidence:

| Stable overlay field | Authoritative source |
|---|---|
| starting_scenario through temporary_residue | same-named migration_evidence field |
| owner_before and owner_after | same-named migration_evidence field |
| migrated_callers and focused_validation | same-named migration_evidence field |
| independently_usable_state and rollback_boundary | same-named migration_evidence field |

The overlay adds no alternate value, schema, author, or persistence format.
ownership_coexistence and migration_matrix remain candidate migration
protection. CCFG-29 removes the stable overlay after equivalent candidate
behavior is proven.

## Amended Execution Ledger

| Slice | Status | Risk | Shape | Depends on | Commit | Validation | Review |
|---|---|---|---|---|---|---|---|
| 1. Transfer one successful flight and stop durably | pending | migration | vertical | CCFG-26A and slice-shape correction closeouts | pending | pending | pending |
| 2. Automate fresh same-batch continuation | pending | migration | vertical | accepted Slice 1 commit and durable continue_same_batch receipt | pending | pending | pending |

Completed slice details move to completed-slices.md during execution. The
active ledger retains pending or active rows only.

## Slice 1 — Transfer One Successful Flight And Stop Durably

### Migration Evidence

~~~yaml
risk: migration
shape:
  selected: vertical
  override_reason: null
migration_evidence:
  starting_scenario: Planning State identifies the exact queued CCFG-26B runway, while public work-batch and serialized execute still route the full runway to Batch Runway execute-spec and the runner infers execute completion means closeout
  durable_result: one fresh public work-batch coordinator owns and completes exactly one successful implementation-slice lifecycle, writes one exact unique flight receipt with continue_same_batch, and ends after the runner validates and durably records it without automatic relaunch
  owner_before: Batch Runway execute-spec owns the happy-path slice lifecycle behind public work-batch, and the runner owns a phase-derived execute-to-closeout rule
  owner_after: work-batch owns currentness, one-slice selection, delegation, focused validation acceptance, independent review acceptance, commit, ledger update, completed-slice archive, terminal reporting, and the exact next action; the runner launches, validates, persists, and stops mechanically
  migrated_callers:
    - public work-batch queued-or-active runway route
    - serialized runner execute phase contract
    - runner execute result and receipt validator
    - runner execute transition and stop caller
    - public skill routing contract
  focused_validation:
    - one real work-batch-produced successful flight through runner validation and durable receipt equality
    - manual resume from canonical Planning State and prior receipt without chat history
    - terminal blocked and failed require_user receipts stop without recovery
    - counterfactual direct Batch Runway routing, old ownership prose, and missing authored action failures
  independently_usable_state: one successful slice can finish with exact durable evidence and a safe manual continuation point; no schema-only or caller-only half-state remains
  rollback_boundary: revert the focused Slice 1 candidate commit to 5c5ec9d52dd9033daa45f3a200031c152363b62c; the old execute-spec route and original one-slot runner behavior return together
  temporary_residue:
    - manual relaunch is required until Slice 2
    - ordered multi-flight retention and automatic continuation remain pending in Slice 2
    - Batch Runway recovery and finalization support remain for CCFG-26C and CCFG-26D
    - Architecture Program Runway closeout support remains for CCFG-26E
    - stable one-slice execution overlay and strict bridge remain through CCFG-29
  ownership_coexistence: temporary
migration_matrix:
  public_work_batch_happy_path:
    current_owner: Batch Runway execute-spec behind public work-batch
    future_owner: work-batch one-successful-slice lifecycle
    reason: the public command must own every semantic decision and exact next action
    status: pending
    removal_slice_or_condition: Slice 1 producer-to-runner proof and no-fallback counterfactual are green
  serialized_execute_route:
    current_owner: runner phase contract directly names Batch Runway execute-spec
    future_owner: runner launches public work-batch once
    reason: the launcher may choose a process target but not a semantic lifecycle owner
    status: pending
    removal_slice_or_condition: Slice 1 phase-contract and restored-old-route counterfactual tests are green
  runner_execute_completion:
    current_owner: runner validation maps every completed execute result to closeout
    future_owner: work-batch authors continue_same_batch, finalize_same_batch, or require_user and the runner validates exactly
    reason: phase identity cannot infer slice acceptance or next action
    status: pending
    removal_slice_or_condition: Slice 1 action-consistency and missing-action rejection tests are green
  public_routing_contract:
    current_owner: routing prose names Batch Runway as execution owner
    future_owner: routing prose names work-batch as happy-path lifecycle owner and Batch Runway as bounded support
    reason: public documentation must agree with executable routing
    status: pending
    removal_slice_or_condition: Slice 1 ownership-contract counterfactual test is green
  flight_result_and_terminal_receipts:
    current_owner: no work-batch-owned result with a real runner consumer
    future_owner: work-batch authors and writes; runner validates, persists, surfaces, and stops
    reason: one flight requires an exact durable producer-consumer boundary
    status: pending
    removal_slice_or_condition: Slice 1 successful, blocked, and failed producer-consumer tests are green
  recovery_support:
    current_owner: stable work-batch plus Batch Runway recovery contracts
    future_owner: CCFG-26C work-batch bounded recovery
    reason: recovery starts from a different terminal state and is outside the happy path
    status: pending
    removal_slice_or_condition: CCFG-26C closeout and CCFG-26E final narrowing
  finalization_support:
    current_owner: Batch Runway final validation and finalization
    future_owner: CCFG-26D work-batch finalization flight
    reason: finalization starts after all implementation slices and has broader gates
    status: pending
    removal_slice_or_condition: CCFG-26D closeout and CCFG-26E final narrowing
  closeout_support:
    current_owner: Architecture Program Runway same-batch reconciliation behind work-batch
    future_owner: CCFG-26E work-batch closeout flight
    reason: closeout is deliberately deferred
    status: pending
    removal_slice_or_condition: CCFG-26E closeout
~~~

### Scope And Acceptance

Slice 1 must implement the full producer-to-persistence path:

1. Planning State current and validate confirm the exact queued or active scope.
2. The serialized execute phase starts one fresh public work-batch coordinator.
3. work-batch selects exactly one pending implementation slice.
4. The existing runway_worker implements and the separate runway_reviewer
   independently accepts the exact diff.
5. work-batch accepts focused validation and the commit, updates the execution
   ledger and archive, then authors and writes one exact flight result.
6. The runner validates the same parsed object and its expected unique path,
   persists the exact receipt reference, inventory, telemetry, session, and
   commit evidence, and stops.
7. A later manual invocation resumes from canonical state and the receipt with
   a fresh Planning State diagnostic and live lease, without chat history.

At the Slice 1 boundary, continue_same_batch is durable but does not trigger an
automatic process launch. Runner state must retain execute as the resumable
same-batch phase and record a manual-continuation stop reason. No direct
happy-path caller may reach Batch Runway execute-spec.

Slice 1 also requires truthful blocked and failed results with require_user
whenever work-batch can author a terminal receipt. The runner only persists,
surfaces, and stops.

### Slice 1 Counterfactual Proof

- restore phase_skill_instruction for execute to Batch Runway execute-spec and
  the focused phase-contract test fails;
- restore Batch Runway happy-path ownership or the execute-spec routing row in
  docs/skill-routing-contract.md and the ownership-contract test fails;
- remove or contradict the work-batch-authored next_action and validation fails
  before persistence or transition;
- manufacture only a final runner state without invoking the work-batch result
  producer and the producer-consumer test fails;
- add a fallback from work-batch to Batch Runway and the no-fallback test fails.

### Slice 1 Validation

Selected profile: project-harness-production, with the original final-only
installation and exact-acceptance override.

1. implementation-created, then required-green: one focused pytest command over
   test_work_batch_flight_contract.py, test_architecture_program_runner_phase_contract.py,
   test_architecture_program_runner_artifacts.py,
   test_architecture_program_runner_environment.py,
   test_architecture_program_runner_run_loop.py,
   test_architecture_program_runner_state.py,
   test_architecture_program_runner_validation.py,
   test_architecture_program_runner_transition.py,
   test_skill_routing_rule_ownership.py, and directly changed behavioral
   scenario tests;
2. required-green: command_owner_scenarios.py validate over the 82-scenario
   catalog;
3. diagnostic baseline with no new failure: the original exact two-test
   known-red command;
4. conditional required-green: Ruff over exact changed Python files;
5. conditional required-green: configured BasedPyright over exact changed
   production Python files;
6. required-green: git diff --check;
7. required review gate: delta-only test-quality-review, followed by an
   independent runway_reviewer on the exact diff basis.

The expanded pre-change Slice 1 subset covered
test_skill_routing_rule_ownership.py plus the artifact, environment,
phase-contract, run-loop, state, validation, and transition runner tests. It
passed 70 tests and 38 subtests in 0.25 seconds (0.41 seconds wall) on
2026-07-18. The scenario catalog validated 82 scenarios in 0.25 seconds wall.
Forecast post-change focused pytest runtime is 0.5 to 2.0 seconds, excluding
agent review and final installation gates.

### Slice 1 Proportionality Forecast

~~~yaml
expected_production_and_contract_files: 10 to 13
expected_test_and_fixture_files: 10 to 13
expected_owner_boundaries:
  count: 4
  names:
    - work-batch lifecycle and result author
    - runner phase, validation, persistence, and stop consumer
    - Planning State and strict lease inputs, consumed read-only
    - public routing and installed-feature metadata
expected_subprocess_boundaries:
  count: 3
  names:
    - runner to fresh work-batch coordinator
    - work-batch to runway_worker
    - work-batch to independent runway_reviewer
validation_commands:
  always: 4
  conditional: 2
  diagnostic: 1
validation_breadth: focused flight contract, phase routing, validation, transition, ownership contract, behavioral catalog, and no-new-known-red regression
review_lenses:
  - producer-consumer behavioral confidence and counterfactual strength
  - semantic owner replacement and no fallback
  - exact worker-reviewer-commit separation
  - scope and deferred-child boundary
support_agent_lenses:
  - delta-only test-quality-review
  - independent exact-diff runway review
approximate_changed_lines: 500 to 900
target_behavior_coordinator_processes: 1
stable_implementation_invocation_coordinator_processes: 1
~~~

Commit message: feat(work-batch): own one durable slice flight

### Slice 1 Stop Conditions

- stop if the candidate baseline has moved before the first handoff;
- stop if one complete successful producer-to-persistence flight cannot exist
  without automatic continuation;
- stop if Batch Runway or the runner retains happy-path decision authority;
- stop if terminal reporting requires autonomous recovery;
- stop if the exact required routing contract path is omitted;
- stop for another reviewed amendment if production/contract files exceed 16,
  test/fixture files exceed 16, changed lines exceed 1125, more than four owner
  boundaries or three subprocess boundary types are required, or more than two
  unforecast validation commands become necessary;
- stop on any batch-level stop condition below.

## Slice 2 — Automate Fresh Same-Batch Continuation

### Migration Evidence

~~~yaml
risk: migration
shape:
  selected: vertical
  override_reason: null
migration_evidence:
  starting_scenario: Slice 1 has durably persisted one completed flight with continue_same_batch, retained execute as resumable state, and stopped for a later manual invocation
  durable_result: the runner consumes the exact continue_same_batch action, launches one new same-batch work-batch coordinator with a fresh Planning State diagnostic and strict lease, retains ordered non-overwriting evidence for both flights, and stops at the last slice's finalize_same_batch handoff
  owner_before: a human must manually relaunch the resumable same-batch execute state after each durable flight
  owner_after: the runner mechanically relaunches exactly one fresh same-batch coordinator from the authored action while work-batch retains every lifecycle and next-action decision
  migrated_callers:
    - runner run loop after validated continue_same_batch
    - execute-flight receipt and input-inventory path allocation
    - batch manifest and telemetry retention
    - fresh work-batch process environment, echoed flight ID, and runner-observed session identity
    - last-implementation-slice finalize_same_batch stop
  focused_validation:
    - deterministic two-slice producer-to-consumer scenario with two distinct coordinator identities and fresh strict leases
    - ordered receipt, inventory, manifest, telemetry, session, and accepted-commit retention with no overwrite
    - bounded-input rejection of raw logs, transcripts, full chronology, and accepted review detail
    - continue_same_batch same-batch-only and no-successor counterfactuals
    - finalize_same_batch durable stop with no finalization or closeout
  independently_usable_state: multiple successful implementation slices can progress in separate fresh coordinators from canonical durable state, while the last slice stops safely for later CCFG-26D finalization
  rollback_boundary: revert only the Slice 2 candidate commit to the accepted Slice 1 commit; one-flight ownership and manual resume remain usable
  temporary_residue:
    - Batch Runway recovery and finalization support remain for CCFG-26C and CCFG-26D
    - Architecture Program Runway closeout support remains for CCFG-26E
    - finalize_same_batch is a stop-only handoff until CCFG-26D
    - stable one-slice execution overlay and strict bridge remain through CCFG-29
  ownership_coexistence: temporary
migration_matrix:
  continue_same_batch_consumption:
    current_owner: manual relaunch from the Slice 1 durable stop
    future_owner: runner mechanical fresh-process relaunch for the same batch only
    reason: a new coordinator must start from durable state without transferring semantic choice to the runner
    status: pending
    removal_slice_or_condition: Slice 2 two-flight fresh-process test is green
  execute_flight_receipt_paths:
    current_owner: one phase-keyed execute receipt path
    future_owner: ordered unique per-flight paths
    reason: repeated flights must not overwrite accepted evidence
    status: pending
    removal_slice_or_condition: Slice 2 no-overwrite test is green
  manifests_and_inventories:
    current_owner: phase-keyed receipt and inventory maps
    future_owner: ordered flight-keyed retention with exact session and commit identity
    reason: canonical resume requires all accepted flight evidence
    status: pending
    removal_slice_or_condition: Slice 2 two-flight manifest test is green
  bounded_fresh_context:
    current_owner: manual resume can still depend on caller discipline
    future_owner: runner validates the exact bounded input manifest before launch
    reason: process freshness is insufficient if prior chronology can silently re-enter
    status: pending
    removal_slice_or_condition: Slice 2 forbidden-input counterfactuals are green
  final_implementation_slice:
    current_owner: no candidate automatic-continuation path reaches a durable last-slice handoff
    future_owner: work-batch authors finalize_same_batch and the runner persists and stops
    reason: CCFG-26D needs a durable start state without CCFG-26B performing finalization
    status: pending
    removal_slice_or_condition: Slice 2 finalize stop test is green
  recovery_support:
    current_owner: stable work-batch plus Batch Runway recovery contracts
    future_owner: CCFG-26C work-batch bounded recovery
    reason: no recovery behavior is added by automatic happy-path continuation
    status: pending
    removal_slice_or_condition: CCFG-26C closeout and CCFG-26E final narrowing
  finalization_support:
    current_owner: Batch Runway final validation and finalization
    future_owner: CCFG-26D work-batch finalization flight
    reason: finalize_same_batch remains only a durable stop
    status: pending
    removal_slice_or_condition: CCFG-26D closeout and CCFG-26E final narrowing
  closeout_support:
    current_owner: Architecture Program Runway same-batch reconciliation behind work-batch
    future_owner: CCFG-26E work-batch closeout flight
    reason: closeout remains outside CCFG-26B
    status: pending
    removal_slice_or_condition: CCFG-26E closeout
~~~

### Scope And Acceptance

Starting only from a validated Slice 1 receipt with continue_same_batch:

1. the runner preserves the first flight's exact receipt, inventory, telemetry,
   runner-observed session identity, accepted commit, and manifest entry;
2. it mechanically launches one fresh work-batch coordinator for the same batch
   and exact next slice;
3. the new process obtains fresh Planning State and strict lease evidence and
   receives only the bounded manifest;
4. the second work-batch flight completes through the unchanged Slice 1 owner;
5. distinct paths and identities are retained in deterministic order; and
6. the last implementation slice authors finalize_same_batch, which the runner
   persists and surfaces before stopping.

continue_same_batch must never clear the current batch, read the backlog,
select or prepare a successor, or invoke plan-batch. finalize_same_batch must
not run final validation, installation, exact acceptance, Batch Runway
finalization, Architecture Program Runway closeout, or any later child.

### Slice 2 Counterfactual Proof

- reuse either runner-observed Codex session ID or strict lease and the two-flight test
  fails;
- reuse a receipt, inventory, telemetry, manifest entry, or accepted-commit slot
  and the no-overwrite test fails;
- add raw logs, transcript text, full chronology, or accepted prior review
  detail to bounded inputs and validation fails before launch;
- change the batch or select a successor on continue_same_batch and validation
  fails;
- invoke finalization or closeout on finalize_same_batch and the durable-stop
  test fails;
- directly manufacture the final runner state without producing both
  work-batch receipts and the producer-consumer scenario fails.

### Slice 2 Validation

1. implementation-created, then required-green: one focused pytest command over
   test_work_batch_flight_contract.py, runner state, validation, transition,
   run-loop, artifact, environment, and directly changed command tests;
2. required-green: command_owner_scenarios.py validate over the 82-scenario
   catalog;
3. diagnostic baseline with no new failure: the original exact two-test
   known-red command;
4. conditional required-green: Ruff over exact changed Python files;
5. conditional required-green: configured BasedPyright over exact changed
   production Python files;
6. required-green: git diff --check;
7. required review gate: delta-only test-quality-review, followed by an
   independent runway_reviewer on the exact Slice 2 diff basis.

The pre-change Slice 2 runner subset passed 62 tests and 2 subtests in 0.22
seconds (0.38 seconds wall) on 2026-07-18. The scenario catalog validated 82
scenarios in 0.25 seconds wall. Forecast post-change focused pytest runtime is
0.7 to 3.0 seconds, excluding agent review and final installation gates.

### Slice 2 Proportionality Forecast

~~~yaml
expected_production_and_contract_files: 8 to 11
expected_test_and_fixture_files: 6 to 9
expected_owner_boundaries:
  count: 4
  names:
    - unchanged work-batch lifecycle and action author
    - runner process launch and action consumer
    - runner ordered state, artifacts, inventories, and telemetry
    - Planning State and fresh strict lease inputs, consumed read-only
expected_subprocess_boundaries:
  count: 3
  names:
    - first runner launch to first work-batch coordinator
    - mechanical relaunch to second work-batch coordinator
    - each work-batch coordinator to its worker and independent reviewer roles
validation_commands:
  always: 4
  conditional: 2
  diagnostic: 1
validation_breadth: two-flight run loop, fresh identity and lease, ordered artifacts, bounded inputs, same-batch-only continuation, finalization stop, catalog, and no-new-known-red regression
review_lenses:
  - fresh-process and bounded-context proof
  - ordered immutable evidence and no overwrite
  - mechanical runner with no lifecycle inference
  - no finalization, closeout, recovery, or successor expansion
support_agent_lenses:
  - delta-only test-quality-review
  - independent exact-diff runway review
approximate_changed_lines: 450 to 800
target_behavior_coordinator_processes: 2
stable_implementation_invocation_coordinator_processes: 1
~~~

Commit message: feat(runner): continue same batch in fresh flights

### Slice 2 Stop Conditions

- stop if Slice 1's commit and continue_same_batch receipt are not exact and
  durable;
- stop if automatic continuation requires shared chat or process memory;
- stop if any ordered evidence can be overwritten;
- stop if the runner must infer batch identity, slice identity, acceptance, or
  action;
- stop if finalize_same_batch requires finalization or closeout behavior;
- stop for another reviewed amendment if production/contract files exceed 14,
  test/fixture files exceed 12, changed lines exceed 1000, more than four owner
  boundaries or three subprocess boundary types are required, or more than two
  unforecast validation commands become necessary;
- stop on any batch-level stop condition below.

## Counterfactual Validation Matrix

Every row is required focused proof. Final-state-only fixtures are insufficient;
use the strongest available public producer-to-consumer path.

| # | Required proof | Assigned gate |
|---|---|---|
| 1 | after Slice 1 no active happy-path caller reaches Batch Runway execute-spec | Slice 1 phase, routing, and behavioral tests |
| 2 | work-batch, runner phase caller, routing contract, deterministic validation, and persisted receipt agree on the new authority | Slice 1 producer-consumer scenario |
| 3 | restoring direct runner-to-Batch-Runway execution fails | Slice 1 phase-contract counterfactual |
| 4 | restoring old routing ownership fails | Slice 1 ownership-contract counterfactual |
| 5 | missing, malformed, stale, mismatched, contradictory, or unauthored next action is rejected | Slice 1 schema and validator parameterization |
| 6 | Slice 1 stops and resumes manually from canonical state and receipt without chat history | Slice 1 stop-and-resume scenario |
| 7 | Slice 2 uses distinct runner-observed coordinator identities, strict leases, receipt paths, and accepted commits | Slice 2 two-flight scenario |
| 8 | repeated flights cannot overwrite receipts, inventories, manifests, telemetry, runner-observed session identity, or commit evidence | Slice 2 artifact/state parameterization |
| 9 | continue_same_batch cannot select or prepare successor work | Slice 2 same-batch-only scenario and behavioral catalog |
| 10 | finalize_same_batch stops without invoking finalization or closeout | Slice 2 last-slice stop scenario |
| 11 | terminal blocked or failed results stop without autonomous recovery | Slice 1 terminal producer-consumer scenarios |
| 12 | recovery, finalization, closeout, phase-label migration, bridge changes, and successor selection are absent from the candidate diff | per-slice reviewer and final range review |

## Final Validation And Closeout Gates

After both implementation slices have clean focused commits and durable flight
receipts, a later explicit stable work-batch invocation runs the original
runway's final validation commands with these amendments:

- every reference to the completed implementation slice means both Slice 1 and
  Slice 2 and their exact commit range;
- the focused suite must include both manual-resume and automatic two-flight
  producer-consumer scenarios plus all twelve counterfactuals above;
- the 82-scenario catalog, unchanged known-red baseline, triggered Ruff and
  BasedPyright, and git diff check retain their original status classes;
- candidate installation, stable-home byte comparison, fresh exact-commit
  acceptance outputs, final delta-only test-quality review, and final
  independent review remain required-green batch gates;
- final validation and same-batch closeout retain the current stable support
  owners only for this batch gate; the candidate finalize_same_batch action
  remains a stop and does not invoke them.

Final validation is not an implementation slice. Closeout may reconcile only
CCFG-26B, keep parent CCFG-26 pending, clear only this queued batch after exact
closeout evidence exists, and stop without selecting or preparing any
successor.

## Actuals Required After Each Slice

The completed-slice entry must record:

- exact changed production, test, fixture, doc, and metadata file counts;
- exact lines added and removed;
- owner and subprocess boundaries actually crossed;
- validation command count, exact commands, breadth, and durations;
- worker, reviewer, and support-agent identities and review lenses;
- coordinator process count, echoed flight IDs, and distinct runner-observed
  session identities;
- for Slice 1, the accepted candidate commit, exact receipt path and SHA-256,
  continue_same_batch action and exact next-slice identity, observation
  telemetry path and SHA-256, and exact runner state, batch manifest, input
  inventory, and telemetry paths and SHA-256 values required for canonical
  manual resume;
- for Slice 2, the equivalent ordered evidence for both flights, including both
  accepted candidate commits, actions, next-slice identities, runner-observed
  sessions, and every non-overwritten receipt, state, manifest, inventory, and
  telemetry path and digest;
- input/output tokens and compaction count when available, otherwise explicit
  null;
- duration and blocker/recovery transitions; and
- comparison to this forecast.

Any substantial expansion requires a new bounded amendment and fresh review
before implementation continues. Expansion is substantial when it introduces
recovery, finalization, closeout, phase-label migration, unrelated runner
architecture, a second runner or execution store, a generic lifecycle
framework, an unforecast semantic owner or subprocess type, or exceeds a
slice-specific numeric stop threshold.

## Execution And Review Boundary

Before the first implementation handoff, work-batch must:

1. confirm Planning State still identifies this exact queued runway and no
   active or successor batch;
2. verify the original three SHA-256 values, this amendment SHA-256, and the
   clean amendment-review SHA-256;
3. verify the candidate remains at the immutable planned baseline before Slice
   1, or stop for an explicit reviewed rebase decision;
4. obtain a fresh strict live lease and separately validate the amended write
   scope;
5. execute exactly the next pending implementation slice under the stable
   one-slice policy; and
6. stop after that slice's commit, receipt, ledger update, archive, and actuals.

The independent amendment review must evaluate the complete two-slice design,
not only Markdown syntax. A non-clean verdict blocks implementation.

## Batch Stop Conditions

- stop if any original historical artifact changes;
- stop if the queued path, batch identity, finding, source evidence, immutable
  baseline, or deferred child boundary changes;
- stop if docs/skill-routing-contract.md is not a required Slice 1 path;
- stop if closeout_same_batch or another unowned placeholder appears in the
  current flight contract;
- stop if migration evidence is duplicated as both vertical_slice and
  migration_evidence in the live candidate representation;
- stop if a final-state-only fixture substitutes for the public
  producer-to-consumer path;
- stop if any slice is not independently testable, reviewable, committable, and
  useful at its durable intermediate state;
- stop if recovery, finalization, closeout, reconciliation, successor
  selection, phase-label migration, physical deletion, bridge removal, default
  generation changes, a second runner/store, or a generic lifecycle framework
  enters implementation;
- stop if the fresh independent amendment review is not clean.
