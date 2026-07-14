# CCFG-19 Contract Verification and Decisions

## Amendment Boundary

This is the live CCFG-19 candidate amendment to the accepted command-owner
design. Slice 1 records joined evidence. Slice 2 records only the approved
schema and ledger-store outcomes. Slice 3 records only the approved runner
boundary and verifies the retained stable/candidate topology. Slice 4 resolves
OPEN-003 and audits the seven-key CCFG-19 exit gate. These slices do not
implement the boundaries or make the current APR, Batch Runway, runner-phase,
import, file, or test topology a target contract.

```yaml
ccfg_19_record:
  evidence_snapshot:
    candidate_commit: 9027bd1ea35e66e263dfced02a2b9f91835c1bd9
    stable_controller_commit: bb5701fdb50e1ec921a07df36a5d3461341a092c
    accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
    current_test_modules: 28
  slice_1:
    contract_records: 31
    contract_to_owner_map_complete: true
    contract_to_scenario_map_complete: true
    blocking_ownership_conflicts: 0
    accepted_decisions_changed: false
  slice_2:
    user_response: Approve all four
    stable_approval_receipt_commit: 19e0746cdc7f681ebe4e6b0ab0be62640097ea6f
    candidate_base_commit: db0f37dc5a62205c3e33df9dbb82ded05fc04b47
    accepted_decisions:
      - DEC-036
      - DEC-037
  slice_3:
    user_response: Approve all four
    stable_approval_receipt_commit: a0fdef399955f17a778c7d8b61ea56a4fca49e76
    candidate_base_commit: 07c5d41882b6df83bc8298854a83d59a3006b555
    accepted_decision: DEC-017
    ccfg_18_topology_evidence_commit: 968f41d1ad752e817af518b12fb8f96273b76e0d
  slice_4:
    user_response: Approve all four
    stable_approval_receipt_commit: 4b3695d8628361649aab1f9d2a8defedd6e738cb
    candidate_base_commit: baeef7a736c1b1874b8bfd47a59343e3711907a6
    accepted_decision: DEC-038
    resolved_question: OPEN-003
  acceptance_keys:
    contract_to_owner_map_complete: true
    contract_to_scenario_map_complete: true
    blocking_ownership_conflicts: 0
    schema_evolution_policy_accepted: true
    ledger_store_boundary_accepted: true
    runner_target_protocol_accepted: true
    planning_transaction_ready_or_explicitly_blocked: true
```

The candidate checkout supplies the source and test evidence below. The stable
checkout supplies the controlling cross-checkout helper and the canonical
planning authority; its planning artifacts are not copied into this record.
The contract text remains owned by
[`01-source-behavior-contracts.md`](01-source-behavior-contracts.md), the target
seams by [`02-target-ownership-model.md`](02-target-ownership-model.md), and the
accepted decisions by [`decisions.md`](decisions.md).

## Evidence Classification

The joined matrix uses three classifications:

- **supported source behavior**: current source states the externally meaningful
  rule. Legacy skill names, modes, imports, headings, and file splits cited as
  evidence remain accidental structure.
- **supported behavior with a target mechanism gap**: current behavior or
  durable evidence supports the rule, but the target CAS, idempotency, receipt,
  or schema mechanism still belongs to a later accepted decision and
  implementation finding.
- **accepted target decision**: the rule is target-only and already supported by
  an accepted decision. Slice 1 does not broaden it.

`replace` in a test disposition means replace topology- or prose-coupled proof
with a scenario against the target public contract. `delete-after-migration`
applies only after the named caller or legacy surface is gone and its deletion
conditions pass.

## Scenario Resolution Addendum

The accepted contract file referenced 16 IDs absent from the scenario catalog.
The first 15 are the gaps named by the CCFG-19 runway; direct comparison also
found `validation-classification`. The following remaps and definitions make
every contract reference resolvable without inventing behavior.

| Referenced ID | Resolution | Justification and proof |
|---|---|---|
| `current-state-diagnostic` | Define: a fresh `planning-state current` result reports the planning root, active program, canonical ledger, selected/queued/active pointers, blockers, warnings, policy, latest closeout, and next safe action from current files. | `scripts/planning_state.py`; `tests/test_planning_state.py::test_current_and_validate_json_agree_on_layout_v1_active_work_fields`. |
| `duplicate-machine-fact-owner` | Define: validation rejects or reports two canonical structured owners for the same active machine fact; prose and projections remain derived. | DEC-010, DEC-032, and DEC-033; target proof belongs to CCFG-20/21. |
| `historical-artifact-does-not-override-current` | Remap to `archived-artifact-not-pickup-authority`. | Same observable rule; current proof is `tests/test_planning_state.py::test_historical_batch_artifacts_warn_without_overriding_current_state`. |
| `illegal-state-transition` | Define: a transition whose current state, artifact lineage, program, or finding identity does not match is rejected before mutation and receipt status is not `applied`. | `scripts/planning_state.py::select_batch`, `queue_batch`; rejection tests beginning at `test_select_batch_rejects_active_conflicts_before_state_mutation`. |
| `invalid-planning-state` | Define: contradictory or structurally invalid selected, queued, or active facts block command-owner action before delegation or mutation. | `tests/test_planning_state.py::test_validate_reports_markdown_active_state_conflict_without_json_state`; `invalid-multiple-active-state` remains its execution-specific case. |
| `legal-state-transitions` | Define: an explicit transition with matching current state and registered lineage writes the new state and a validated receipt. | `tests/test_planning_state.py::test_select_batch_updates_explicit_state_and_writes_receipt` and `test_queue_batch_requires_selected_registered_dispatch_and_runway`. |
| `missing-current-file` | Define: a listed program without `CURRENT.md` is a fatal diagnostic blocker and historical filenames are not scanned as a replacement. | `tests/test_planning_state.py::test_reports_missing_program_current_without_scanning_historical_files`. |
| `partial-execution` | Define: completed-slice evidence survives while the active runway identifies the next incomplete slice; completed work is not replayed. | Current procedure: `skills/batch-runway/references/execute-recovery-v1.md`; target behavioral proof belongs to CCFG-23. |
| `resume-after-interruption` | Remap to `resume-active-batch`. | Same command-level behavior; interruption is one cause of active-batch pickup. |
| `stale-placeholder-closeout` | Define: unresolved commit/review placeholders block closeout; the self-referential final commit uses only `this closeout commit`. | `tests/test_batch_lifecycle_guards.py::test_active_batch_artifacts_do_not_keep_unresolved_commit_placeholders` and `test_batch_runway_documents_final_closeout_commit_placeholder_policy`. |
| `stale-state-revision` | Define: an expected state or artifact revision mismatch rejects mutation before write and emits stable blocker evidence. | Existing artifact-lineage checks in `scripts/planning_state.py`; DEC-037 accepts whole-ledger CAS and CCFG-21 owns implementation proof. |
| `structured-prose-contradiction` | Remap to `current-prose-does-not-own-pointers`. | Both assert that structured canonical pointers win and contradictory prose cannot redefine them. |
| `legacy-evidence-no-state-writes` | Define: `legacy-removal` may classify and hand off evidence but may not select, queue, execute, reconcile, or write lifecycle state. | DEC-019 is the target authority. Current `skills/legacy-removal/SKILL.md` and `tests/test_planning_state_consumer_projection_routing.py` methods that preserve legacy-removal program authority are conflicting migration evidence, not proof of the prohibition; CCFG-24/25 must rewrite them. |
| `deletion-evidence-no-state-writes` | Define: `dead-surface-audit` returns deletion-test evidence vocabulary only and cannot approve or execute deletion or mutate planning state. | `skills/dead-surface-audit/SKILL.md`; `tests/test_deletion_test_vocabulary_ownership.py::test_dead_surface_audit_owns_only_deletion_test_evidence_vocabulary`. |
| `test-quality-review-no-state-writes` | Define: `test-quality-review` reports bounded review evidence and cannot implement, select, queue, accept, or transition lifecycle state. | `skills/test-quality-review/SKILL.md`; `tests/test_planning_state_consumer_projection_routing.py::test_test_quality_review_is_review_support_not_primary_planning_command`. |
| `validation-classification` | Define: every command is classified as required-green, conditional, diagnostic, known-red baseline, or future; only declared required-green failures gate acceptance. | `skills/batch-runway/references/create-spec.md`; `tests/test_batch_runway_create_spec_contract.py::test_create_spec_validation_commands_require_status_classes` and the three following status-gate tests. |

## Joined Contract Evidence

Test IDs refer to the complete inventory in the next section. An explicit gap is
a disposition, not a claim that an existing topology test proves the contract.

| Contract | Current source evidence | One target owner | Scenario evidence | Classification | Test evidence and disposition |
|---|---|---|---|---|---|
| `INTAKE-SOURCE-001` | `skills/add-to-ledger/SKILL.md` purpose and Stops; `docs/skill-routing-contract.md` Executable Work Source | `add-to-ledger` | `fresh-finding-intake`, `requested-missing-finding` | supported source behavior | T20 `test_executable_work_source_boundary_is_explicit`; T28 command-owner routing assertions. Replace text coupling with CCFG-23 command behavior. |
| `INTAKE-IDENTITY-002` | `skills/add-to-ledger/SKILL.md` source intake boundary; `docs/workflow-guide.md` external-source pipeline | `add-to-ledger` | `fresh-finding-intake`, `duplicate-finding-intake` | supported source behavior | No direct behavioral test. Replace the gap with CCFG-23 fresh/duplicate intake scenarios. |
| `INTAKE-NORMALIZE-003` | `skills/add-to-ledger/SKILL.md`; APR Vague Row Selection Guard | `add-to-ledger` | `fresh-finding-intake`, `vague-mixed-risk-finding` | supported source behavior | T16 vague-row methods and T28 `test_plan_batch_blocks_direct_planning_from_ccfg11_like_vague_rows`; replace with target intake/planning boundary proof. |
| `INTAKE-MUTATE-004` | canonical `docs/plans/programs/codex-config/LEDGER.md`; `docs/workflow-guide.md` pipeline | `add-to-ledger` | `fresh-finding-intake`, `duplicate-finding-intake`, `stale-ledger-revision` | supported behavior with a target mechanism gap | No current intake CAS/idempotency test. Add CCFG-21 store fixtures and CCFG-23 intake scenarios against DEC-037. |
| `INTAKE-STOP-005` | `skills/add-to-ledger/SKILL.md` Stops | `add-to-ledger` | `intake-stops-before-planning` | supported source behavior | T20 command-input/source-boundary methods. Replace prose assertions with no-dispatch/no-runway file-effect proof. |
| `PLAN-SOURCE-001` | `skills/plan-batch/SKILL.md`; `docs/skill-routing-contract.md` Command Input Contract | `plan-batch` | `empty-ledger`, `one-eligible-finding`, `requested-missing-finding` | supported source behavior | T20 source-boundary methods and T28 command-owner routing methods; replace with target interface scenarios. |
| `PLAN-ACTIVE-002` | `skills/plan-batch/SKILL.md`; `skills/planning-state/SKILL.md` Diagnostic-First Pickup | `plan-batch` | `selected-dispatch-exists`, `queued-runway-exists`, `active-runway-exists` | supported source behavior | T17 `test_work_batch_preserves_queued_plan_batch_output_without_closeout`; T26 current/validate active-field methods. Retain diagnostics, replace prose coupling. |
| `PLAN-SELECT-003` | `skills/plan-batch/SKILL.md`; APR Active-State Handoff and Vague Row Selection Guard | `plan-batch` | `one-eligible-finding`, `multiple-eligible-findings`, `explicitly-requested-finding` | supported source behavior | T16 selected-dispatch methods and T28 routing methods. Replace APR ownership/topology proof with CCFG-23 plan-batch scenarios. |
| `PLAN-SCOPE-004` | `skills/plan-batch/SKILL.md`; APR Vague Row Selection Guard | `plan-batch` | `vague-mixed-risk-finding`, `destructive-work-without-approval` | supported source behavior | T16 `test_selected_dispatch_requires_split_block_or_narrow_rationale` and vague-row method; T18 destructive/evidence risk methods. Rewrite against target owner. |
| `PLAN-DISPATCH-005` | APR Selected Batch Brief; `skills/planning-artifacts/SKILL.md` placement contract | `plan-batch` | `one-eligible-finding`, `selected-dispatch-exists` | supported source behavior | T16 selected-dispatch shape checks. Replace APR name/mode assertions with durable dispatch schema/behavior proof in CCFG-21/23. |
| `PLAN-RUNWAY-006` | `skills/batch-runway/references/create-spec.md`; Batch Runway create-spec mode | `plan-batch` | `exactly-one-runway` | supported source behavior | T18 create-spec, scope, and status-class methods. Rewrite schema-relevant cases in CCFG-21 and behavior in CCFG-23; delete old mode-name checks after migration. |
| `PLAN-RISK-007` | `skills/batch-runway/references/create-spec.md` batch-kind, risk, approval, and validation sections | `plan-batch` | `destructive-work-without-approval`, `validation-classification` | supported source behavior | T18 `test_create_spec_validation_commands_require_status_classes` through `test_destructive_cleanup_in_evidence_or_characterization_work_is_gated`. Retain rules, rewrite owner/topology. |
| `PLAN-STOP-008` | `skills/plan-batch/SKILL.md` stop boundary; `docs/workflow-guide.md` Rules | `plan-batch` | `planning-stops-before-implementation`, `queued-runway-exists` | supported source behavior | T17 queued-state routing and T20 command-boundary assertions. Replace with file-effect scenario proving no worker/code/commit. |
| `EXEC-CURRENT-001` | `skills/work-batch/SKILL.md`; Batch Runway Execute Slice Core current-row selection | `work-batch` | `start-queued-batch`, `resume-active-batch`, `invalid-multiple-active-state` | supported source behavior | T17 queued-state preservation; T26 active-state validation. Replace bridge prose with target work-batch scenarios. |
| `EXEC-RESUME-002` | Batch Runway recovery reference and active execution ledger | `work-batch` | `partial-execution`, `resume-active-batch` | supported source behavior | T11 resume artifact tests and T12 legacy resume tests are current evidence. Replace with topology-independent completed-slice/restart proof; delete legacy flat-state cases after expiration. |
| `EXEC-WORKER-003` | `agents/runway_worker.toml`; Execute Slice Core Worker Handoff | `work-batch` | `successful-slice`, `worker-scope-violation` | supported source behavior | T24 `test_worker_owns_slice_scope_lifecycle_and_failure_contract`; T15 worktree scope tests. Rewrite exact TOML prose into registered-contract and behavioral scope proof. |
| `EXEC-VALIDATE-004` | Batch Runway create-spec status classes and Execute Slice Core validation gate | `work-batch` | `validation-failure`, `validation-classification` | supported source behavior | T18 status-class methods; T11 validation-blocker stop. Retain the classification rule and replace legacy phase/runway coupling. |
| `EXEC-REVIEW-005` | `agents/runway_reviewer.toml`; Execute Slice Core Reviewer Handoff | `work-batch` | `review-failure`, `stale-review-basis`, `successful-slice` | supported source behavior | T24 reviewer-current-evidence and handoff-schema methods. Add CCFG-23 stale-basis behavior; rewrite exact prose assertions. |
| `EXEC-COMMIT-006` | Batch Runway Standard Execution Contract and Execute Slice Core Commit Receipt | `work-batch` | `successful-slice`, `dirty-file-conflict` | supported source behavior | T17 exact/final commit placeholder guards; T15 dirty-worktree behavior. Replace old owner names while retaining focused-commit and unrelated-dirty-file proof. |
| `EXEC-RECOVER-007` | `skills/batch-runway/references/execute-recovery-v1.md` | `work-batch` | `validation-failure`, `review-failure`, `dirty-file-conflict`, `unexpected-head-movement` | supported source behavior | T11 failure/head/artifact-state methods and T15 worktree methods. Replace runner-phase recovery topology with target work-batch recovery scenarios. |
| `EXEC-STOP-008` | Batch Runway global stop conditions and recovery stop report | `work-batch` | `invalid-planning-state`, `validation-failure`, `missing-agent-support` | supported source behavior | T11 missing receipt/inventory and validation blocker methods; T26 invalid-state blockers. Retain blocker behavior, replace topology. |
| `CLOSE-FINAL-001` | `skills/batch-runway/references/finalize-batch-v1.md` | `work-batch` | `successful-closeout`, `missing-closeout-evidence`, `stale-placeholder-closeout` | supported source behavior | T17 placeholder and closeout-evidence guards; T26 closeout validator/render methods. Retain behavior/schema proof, rewrite legacy owner prose. |
| `CLOSE-RECONCILE-002` | `skills/work-batch/SKILL.md`; APR closeout-runway boundary | `work-batch` | `same-batch-reconciliation`, `closeout-without-execution-evidence` | supported source behavior | T17 closeout evidence rejection; T20 `test_work_batch_reconciles_same_batch_closeout`; T26 closeout evidence validation. Replace APR mode with target command behavior. |
| `CLOSE-NEXT-003` | `skills/work-batch/SKILL.md`; `docs/workflow-guide.md` same-batch stop rule | `work-batch` | `no-successor-selection` | supported source behavior | T11's `next_batch_ready` methods prove conflicting accidental runner protocol, not this target contract; T17/T20 prove the command stop in prose. Replace all with CCFG-23/27 public-command behavior after Slice 3. |
| `STATE-DIAG-001` | `skills/planning-state/SKILL.md`; `scripts/planning_state.py` `current` and `validate` commands | `planning-state` | `current-state-diagnostic`, `missing-current-file`, `archived-artifact-not-pickup-authority` | supported source behavior | T26 current/validate, missing-current, warning, and historical-precedence methods. Retain behavioral diagnostics; rewrite only format-specific cases under CCFG-21. |
| `STATE-TRANSITION-002` | `scripts/planning_state.py::select_batch`, `queue_batch`, `_transition_receipt` | `planning-state` | `legal-state-transitions`, `illegal-state-transition`, `stale-state-revision` | supported behavior with a target mechanism gap | T26 select/queue/receipt and conflict methods. Retain current characterization; CCFG-21 adds DEC-037 whole-ledger revision and fault proof. |
| `STATE-CANONICAL-003` | DEC-010, DEC-032, DEC-033; planning-state canonical/projection validators | `planning-state` (cross-artifact canonicality; `ledger-store` may validate applied finding records but does not redefine the ownership rule) | `duplicate-machine-fact-owner`, `current-prose-does-not-own-pointers` | accepted target decision | T26 canonical/projection schema methods and T27 single-owner/noncanonical-projection methods. Rewrite to accepted CCFG-20/21 schemas; no current file topology is preserved. |
| `STATE-HISTORY-004` | `scripts/planning_state.py` active-first loading; Planning State Diagnostic-First Pickup | `planning-state` | `archived-artifact-not-pickup-authority` | supported source behavior | T26 historical-artifact, redirect, stale-warning, and missing-current methods. Retain behavior; delete only expired compatibility readers after migration evidence. |
| `EVIDENCE-LEGACY-001` | DEC-019; current `skills/legacy-removal/SKILL.md` is conflicting migration evidence because it retains broader program authority | `legacy-removal` (classification only) | `legacy-evidence-no-state-writes` | accepted target decision | T27 legacy-removal owner/handoff methods conflict with the target prohibition rather than proving it. Rewrite to evidence-only authority during CCFG-24/25; delete obsolete program-owner exception proof. |
| `EVIDENCE-DEAD-002` | `skills/dead-surface-audit/SKILL.md` evidence-producer boundary | `dead-surface-audit` (deletion-test evidence only) | `deletion-evidence-no-state-writes` | supported source behavior | T25 vocabulary-owner and generated-label methods. Retain evidence vocabulary behavior; rewrite references to deleted consumers after migration. |
| `EVIDENCE-TEST-003` | `skills/test-quality-review/SKILL.md` mode, output, and non-goals | `test-quality-review` (review evidence only) | `test-quality-review-no-state-writes` | supported source behavior | T27 `test_test_quality_review_is_review_support_not_primary_planning_command`. Replace text-only proof with a bounded result/no-write scenario in CCFG-23. |

## Ownership Conflict Computation

The count is derived from the 31 rows, not asserted from the target diagram:

```yaml
ownership_conflict_computation:
  joined_contracts: 31
  contracts_with_zero_target_owners: 0
  contracts_with_multiple_target_decision_owners: 0
  blocking_ownership_conflicts: 0
```

The following apparent overlaps are not hidden by that count:

| Evidence overlap | Why it is not a blocking target-owner conflict | Required disposition |
|---|---|---|
| Current APR and Batch Runway procedures make planning, execution, and closeout decisions also assigned to command owners. | DEC-001, DEC-005, DEC-006, and DEC-014 already select one target command owner; the old locations are migration topology, not co-owners. | CCFG-24 through CCFG-28 transfer behavior and remove the old decision paths. |
| Command owners decide lifecycle intent while `planning-state` applies transitions. | DEC-003 and the target ownership matrix separate semantic choice from validation/serialization. | CCFG-21 implements explicit transition requests; no selection logic moves into `planning-state`. |
| `add-to-ledger`/`work-batch` decide ledger meaning while `ledger-store` applies mutations. | DEC-037 accepts whole-ledger CAS, exact replay, and receipt recovery while preserving command-owner semantics. | CCFG-21 implements the store; CCFG-24/26 integrate it without moving semantic decisions. |
| Evidence skills classify legacy, deletion, or test quality while plan/work owners act. | DEC-019 and the evidence contracts make those skills evidence producers only. | CCFG-24/25 remove the remaining legacy-removal program-owner exception. |
| The current runner reads `next_batch_ready` while `work-batch` must not select a successor. | This is a protocol/behavior conflict in accidental runner topology, not two accepted target selection owners: `plan-batch` alone selects, and the runner owns only loop/process lifecycle. | Slice 3 records the approved public-command protocol; CCFG-27/28 replace the current runner paths/tests. |

The Slice 1 computation found no target-owner ambiguity. DEC-036 and DEC-037
resolve the schema and store detail. DEC-017 now records the approved runner
protocol without preserving current phase topology. OPEN-003 remains the
separate approved outcome for Slice 4.

## Current Test Module Classification

This inventory is the complete sorted set of current `tests/test_*.py` modules
at the candidate evidence commit. Primary classes use the CCFG-19 vocabulary.
For every row, the primary class applies to every method not matched by an
exception selector. Exception selectors are exhaustive exact names, exact-name
prefixes, or an explicit complement; ordered selectors use first-match order so
one method cannot receive two primary classes. Dispositions do not authorize
test edits in CCFG-19.

```yaml
method_inventory_audit:
  modules_observed: 28
  test_methods_observed: 465
  methods_assigned_by_primary_default: 253
  methods_assigned_by_exception_selector: 212
  unassigned_methods: 0
  multiply_assigned_methods: 0
```

| ID | Module | Primary class | Method-level exceptions | Disposition |
|---|---|---|---|---|
| T01 | `tests/test_agent_done_notify.py` | integration | 2/5 exceptions: topology = `test_manifest_feature_is_opt_in`, `test_installed_hook_config_only_registers_principal_agent_stop`. | Retain; unrelated notification topology is not a command-owner legacy contract. |
| T02 | `tests/test_architecture_program_runner.py` | integration | 2/16 exceptions: topology = `test_runner_facade_reexports_public_helpers_for_compatibility`, `test_execute_codex_phase_routes_through_worker_adapter`. | Replace runner behavior with public-command scenarios in CCFG-23/27; delete facade/adapter topology tests after migration. |
| T03 | `tests/test_architecture_program_runner_artifacts.py` | integration | 6/8 exceptions: schema = `test_batch_manifest_records_receipts_and_telemetry`, `test_token_summaries_cover_missing_and_context_pressure`, and every method whose exact name starts `test_phase_telemetry_` or `test_run_telemetry_`. | Rewrite retained receipt/telemetry behavior against the target runner protocol; delete old phase artifact topology after CCFG-28. |
| T04 | `tests/test_architecture_program_runner_change_allowance.py` | behavioral | 1/7 exception: topology = `test_change_allowance_owner_exposes_named_path_api`. | Rewrite path-scope behavior at the target command/runner seam; delete named owner API proof. |
| T05 | `tests/test_architecture_program_runner_command.py` | integration | 7/9 exceptions: text-contract = every method whose exact name starts `test_prompt_`, `test_structured_prompt_`, `test_dry_run_`, or `test_display_quoting_`. | Replace with public-command invocation/result behavior in CCFG-27; delete old phase prompt topology. |
| T06 | `tests/test_architecture_program_runner_environment.py` | integration | 2/6 exceptions: schema = `test_current_state_supplies_expected_receipt_and_input_inventory_paths`; text-contract = `test_prompt_artifact_environment_facts_are_derived_from_current_state`. | Rewrite only target environment/generation behavior; delete old phase environment shape after migration. |
| T07 | `tests/test_architecture_program_runner_input_inventory.py` | schema | 9/18 exceptions: integration = every method whose exact name starts `test_input_inventory_evidence_` or `test_input_inventory_file_loader_`, plus `test_input_inventory_expected_path_helper`; topology = `test_input_inventory_path_is_phase_environment_fact_and_prompt_guidance`, `test_phase_observation_lists_input_inventory_as_artifact_size_candidate`, `test_input_inventory_owner_direct_script_import_fallback`. | Retain or rewrite bounded inventory schema if the target protocol uses it; delete import fallback and phase routing after CCFG-28. |
| T08 | `tests/test_architecture_program_runner_phase_contract.py` | schema | 2/9 exceptions: topology/text-contract = `test_phase_contract_routes_skills_for_all_fixed_phases`, `test_prompts_render_contract_obligations_for_all_fixed_phases`. | Replace required result obligations with public command schemas; delete fixed-phase routing topology. |
| T09 | `tests/test_architecture_program_runner_phase_observation.py` | integration | 3/11 exceptions: schema = `test_phase_observation_owner_builds_execution_metadata_with_exact_session_path`; topology = `test_runner_routes_execution_metadata_through_phase_observation_owner`; text-contract = `test_phase_observation_is_launch_session_metadata_not_environment_or_contract`. | Rewrite target observation/secret-redaction behavior; delete named phase-owner topology. |
| T10 | `tests/test_architecture_program_runner_protocol.py` | text-contract | None. | Replace local runner prose assertions with executable public-command protocol tests in CCFG-27. |
| T11 | `tests/test_architecture_program_runner_run_loop.py` | integration | 6/15 exceptions: schema = `test_final_summary_shape_is_facade_compatibility_contract`; topology (obsolete successor-readiness semantics) = `test_unbounded_mode_stops_when_closeout_reports_no_next_batch`, `test_unbounded_mode_continues_after_closeout_when_next_batch_ready`; migration-retention = every method whose exact name starts `test_resume_`. | Rewrite stop/resume/failure behavior; replace successor-readiness with fresh `plan-batch`; delete old artifact compatibility after expiry. |
| T12 | `tests/test_architecture_program_runner_state.py` | migration-retention | 2/6 exceptions: schema = `test_state_write_load_round_trips_validated_json`; topology = `test_runner_reexports_owner_path_and_state_helpers`. | Replace target run-state schema as needed; delete legacy flat resume and facade topology after CCFG-28. |
| T13 | `tests/test_architecture_program_runner_transition.py` | integration | 3/7 exceptions: topology = `test_runner_facade_delegates_phase_transition_api_to_owner`, `test_closeout_next_batch_resets_active_batch_paths` (obsolete successor-readiness topology); text-contract = `test_phase_transition_owner_does_not_own_validation_or_receipts`. | Replace with public command transitions and no-successor-readiness protocol; delete named phase topology. |
| T14 | `tests/test_architecture_program_runner_validation.py` | schema | 5/11 exceptions: integration = `test_receipt_content_must_match_phase_result` and every method whose exact name starts `test_structured_receipt_`. | Replace phase-result schemas with target command-result schemas; retain receipt mismatch behavior where applicable. |
| T15 | `tests/test_architecture_program_runner_worktree.py` | behavioral | None. | Rewrite against the target runner/command write allowance; retain unrelated-dirty-file protection. |
| T16 | `tests/test_architecture_program_runway_status_vocabulary.py` | text-contract | 2/5 exceptions: behavioral = `test_selected_dispatch_requires_split_block_or_narrow_rationale`, `test_vague_row_guard_names_ccfg11_like_mixed_risk_expansion`. | Replace behavioral exceptions in the plan-batch harness; delete APR wording/status topology after transfer. |
| T17 | `tests/test_batch_lifecycle_guards.py` | text-contract | 3/5 exceptions: behavioral = `test_active_batch_artifacts_do_not_keep_unresolved_commit_placeholders`, `test_work_batch_preserves_queued_plan_batch_output_without_closeout`, `test_architecture_program_closeout_rejects_dispatch_runway_only_evidence`. | Rewrite behavior against target schemas/commands; delete exact Batch Runway/APR prose assertions after migration. |
| T18 | `tests/test_batch_runway_create_spec_contract.py` | text-contract | 7/16 exceptions: schema = `test_create_spec_validation_commands_require_status_classes`, `test_generated_spec_checklist_requires_batch_kind`, `test_create_spec_guidance_names_batch_kinds_and_slice_risk_classes`; behavioral = `test_required_green_requires_evidence_or_slice_owned_remediation`, `test_non_green_statuses_require_explicit_gating_context`, `test_diagnostic_and_future_commands_cannot_be_silent_required_gates`, `test_destructive_cleanup_in_evidence_or_characterization_work_is_gated`. | Replace exceptions with target schema/scenario tests; delete old create-spec mode and prose topology after CCFG-25/28. |
| T19 | `tests/test_codebase_investigator_contract.py` | text-contract | 4/5 exceptions: topology = `test_registered_agent_has_expected_identity_and_model`, `test_manifest_registers_only_the_new_agent_path`, `test_active_configuration_and_documentation_use_only_the_new_name`, `test_batch_runway_keeps_orchestration_ownership` (obsolete owner topology). | Retain bounded investigator result contract; rewrite inventory checks as needed and delete old Batch Runway ownership proof after migration. |
| T20 | `tests/test_codex_features_manifest.py` | topology | 13/21 exceptions: schema = `test_manifest_feature_requirements_are_valid`, `test_manifest_catalog_distinguishes_user_and_agent_facing_skills`, `test_custom_agent_toml_files_are_valid`; text-contract = `test_cross_checkout_generic_surfaces_remain_project_neutral`, `test_command_owner_input_contracts_are_explicit`, `test_work_batch_reconciles_same_batch_closeout`, `test_plan_batch_command_owner_runtime_boundaries_are_explicit`, `test_executable_work_source_boundary_is_explicit`, `test_external_skill_lock_blocks_implement_skill`, `test_port_by_contract_is_not_general_rewrite_shortcut`, `test_direct_request_prompts_preserve_command_owner_boundary`, `test_agent_facing_support_skills_are_not_ui_commands`, `test_global_instructions_include_default_agent_delegation`. | Retain manifest integrity generally; replace behavioral prose with scenarios and delete old owner dependency/helper topology when CCFG-28/29 conditions pass. |
| T21 | `tests/test_codex_owner.py` | integration | None. | Retain; installer ownership inspection is independent of the command-owner source contract. |
| T22 | `tests/test_cross_checkout_context.py` | schema | 12/21 exceptions: integration = `test_allows_toolchain_to_share_the_implementation_repository`, `test_rejects_generation_role_root_mismatch_before_caller_hook`, every method whose exact name starts `test_rechecks_`, `test_validates_planning_and_implementation_write_scopes`, `test_rejects_out_of_scope_writes_before_caller_hook`, `test_rejects_caller_supplied_planning_root_outside_repository`, `test_read_only_generations_allow_implementation_only_scope`, `test_rejects_invalid_and_mismatched_revisions`, `test_rejects_non_repository_and_nested_repository_roots`; text-contract = `test_public_api_is_data_only_and_has_no_workflow_authority`. | Retain through cross-checkout migration; delete after CCFG-29 final integration satisfies the bridge deletion condition. |
| T23 | `tests/test_cross_checkout_precreation.py` | schema | 27/32 exceptions: integration = every method except `test_parses_and_round_trips_the_exact_three_part_shape`, `test_rejects_missing_extra_and_mistyped_shape_fields`, `test_rejects_non_exact_interface_states_and_authority`, `test_rejects_relative_duplicate_and_broadened_declared_targets`, `test_rejects_candidate_overlap_with_protected_and_candidate_roots`. | Retain through bootstrap/cutover proof; delete after CCFG-29 bridge removal. |
| T24 | `tests/test_custom_agent_contracts.py` | text-contract | 7/12 exceptions: topology = `test_active_agent_inventory_and_models_are_intentional`, `test_manifest_registers_the_complete_inventory`; migration-retention = `test_worker_and_reviewer_report_verified_cross_checkout_identity`, `test_worker_and_reviewer_distinguish_precreation_verification`, `test_precreation_contract_requires_installed_owner_and_strict_transition`; schema = `test_v1_contracts_remain_compatible_and_v2_owns_current_results`, `test_worker_and_reviewer_handoffs_select_v1_or_v2_schemas`. | Retain worker/reviewer authority boundaries, rewrite exact prose/schema coupling, and delete temporary bridge fields only after CCFG-29. |
| T25 | `tests/test_deletion_test_vocabulary_ownership.py` | text-contract | 3/6 exceptions: behavioral = every method whose exact name starts `test_ccfg_like_generated_text_`. | Retain evidence-vocabulary behavior; rewrite references to APR/Batch Runway consumers after their deletion. |
| T26 | `tests/test_planning_state.py` | integration | 81/178 ordered exceptions: first, migration-retention = every method whose exact name contains `bootstrap` or `migrated_artifact` (19); second, historical = `test_redirect_ledgers_are_evidence_not_active_sources`, `test_historical_batch_artifacts_warn_without_overriding_current_state`, `test_reports_missing_program_current_without_scanning_historical_files`, `test_current_command_reports_graphify_current_without_historical_selection`, `test_current_command_reports_missing_current_blocker_without_old_runway_pickup`, `test_current_and_validate_json_keep_stale_historical_files_warning_only`, `test_validate_reports_redirect_without_target_as_fatal`, `test_validate_keeps_stale_pickup_notes_warning_only` (8); third, schema = every method whose exact name starts `test_current_json_protocol_`, `test_json_protocol_`, `test_protocol_formatter_`, `test_state_fixture_schema_`, `test_project_policy_contract_`, `test_sqlite_projection_contract_`, `test_receipt_fixture_schema_`, or `test_closeout_evidence_index_` (54 after earlier selectors). | Retain diagnostic/transition behavior and historical precedence; rewrite schema cases under CCFG-21; delete only expired compatibility fixtures after migration. |
| T27 | `tests/test_planning_state_consumer_projection_routing.py` | text-contract | 3/18 exceptions: topology = `test_batch_runway_feature_depends_on_planning_state`, `test_architecture_program_feature_depends_on_planning_state`, `test_legacy_removal_feature_depends_on_planning_state`. | Replace old consumer/owner prose with accepted target seams; retain noncanonical projection and evidence-only boundaries as behavioral/schema proof. |
| T28 | `tests/test_skill_routing_rule_ownership.py` | text-contract | None. | Replace transitional routing-owner prose with end-to-end command-owner contract tests; delete old runtime split assertions after CCFG-24 through CCFG-26. |

## Slice 1 Evidence Exit

All 31 contracts now have defensible source evidence (including explicit
inference and target-mechanism gaps, or an explicit target-only
decision source), one target owner, resolved scenarios, a source/target
classification, and test disposition evidence. All 28 current test modules have
one primary classification, and the exhaustive mixed-module selectors assign
all 465 current test methods exactly once.

Slice 1 left these decision gates for the user approval packet:

- schema evolution and explicit v1 exception policy;
- whole-ledger CAS and the exact apply-only `ledger-store/v1` boundary;
- the runner public-command protocol and removal of `next_batch_ready`;
- OPEN-003 transaction staging, partial evidence, receipt recovery, and retry.

## Slice 2 Approved Boundaries

The stable planning receipt at commit
`19e0746cdc7f681ebe4e6b0ab0be62640097ea6f` records the user's exact response
`Approve all four`. Slice 2 consumes only the schema-evolution and ledger-store
parts of that approval as DEC-036 and DEC-037.

### Closed-world schema evolution

DEC-036 accepts this behavior for every v1 contract and planning-artifact
schema:

| Concern | Accepted behavior |
|---|---|
| Writer version | While v1 is active, writers emit v1. |
| Unknown version | Block; do not fall back to prose or a permissive reader. |
| Unknown v1 field | Reject unless that schema has an explicit accepted allowlist exception for the named field. |
| Optional addition | Requires an accepted compatibility decision. Readers deploy support before writers emit the field. |
| Required-field change | Requires a new schema version; it cannot ship as a v1 exception. |
| Semantic ownership change | Requires a new schema version and an accepted architecture decision. |
| Deprecation | v1 readers retain support until the named migration condition passes; silent v1 removal is forbidden. |
| Producer identity | Emitted active contracts retain `toolchain_generation`, `toolchain_commit`, and `schema_version`. |
| Per-schema exception | Names the schema, allowed fields, accepted decision, bounded scope, and removal condition; it cannot waive the unknown-version or new-version rules. |

The deprecation and producer-identity rows preserve the already accepted
[`03-contract-first-formats.md`](03-contract-first-formats.md) contract. They do
not add an unapproved compatibility path.

Current strict validators in `scripts/cross_checkout_context.py`, runner result
schemas, and `tests/test_cross_checkout_context.py::test_rejects_missing_and_unsupported_fields`
demonstrate fail-closed validation techniques. Current `scripts/planning_state.py`
fixtures, legacy readers, `test_json_protocol_normalizes_wrapped_live_style_fields`,
and `test_bootstrap_contract_represents_graphify_compatibility_evidence`
demonstrate migration and compatibility constraints. Neither family is silently
standardized: DEC-036 is the policy, and CCFG-20/21 must implement it separately
for each declared schema.

### Apply-only `ledger-store/v1`

DEC-037 accepts one storage boundary:

```yaml
ledger_store_v1:
  read:
    inputs: [ledger_path]
    outputs: [parsed_findings, file_revision]
  apply:
    inputs:
      - ledger_path
      - expected_file_revision
      - caller_decision:
          action: create | update | merge | no-op | reconcile
          finding_mutations: []
          touched_finding_revisions: {}
          idempotency_key: string
    outputs:
      - outcome: applied | exact_replay
      - before_revision
      - after_revision
      - touched_finding_ids
      - receipt
  whole_ledger_cas:
    file_revision_mismatch: reject_without_write
    touched_finding_revision_mismatch: reject_without_write
  idempotency:
    evaluation_order:
      - reject_existing_key_payload_mismatch
      - return_existing_exact_key_payload_result
      - validate_cas_for_new_key
    exact_key_and_payload_replay: return_same_result_without_reapplying
    same_key_different_payload: reject
  persistence:
    deterministic_rendering: required
    atomic_replacement: required
    reread_and_validate: required
  receipt_recovery:
    ledger_written_receipt_missing: recover_from_durable_exact_replay_evidence
    second_application: forbidden
    missing_or_ambiguous_evidence: block
```

The store may mechanically check schema and identity uniqueness, file and
touched-finding revisions, caller payload shape, dependency references, exact
idempotency replay, and deterministic rendering. It may not decide semantic
duplicates, merge meaning, selection, scope, closeout, or successors.
`add-to-ledger` owns intake mutation meaning; `work-batch` owns same-batch
reconciliation meaning.

### Evidence, conflicts, and deferred implementation

| Boundary | Source or accepted evidence | Conflict disposition | Deferred implementation owners |
|---|---|---|---|
| Schema evolution | `03-contract-first-formats.md`; DEC-008, DEC-010, DEC-031; strict validators and permissive planning-state examples as contrasting evidence | Per-schema DEC-036 rules replace any inference that one current parser's strictness or permissiveness is universal. | CCFG-20 skill schema; CCFG-21 planning schemas; CCFG-23 scenarios. |
| Ledger storage | `02-target-ownership-model.md`; DEC-002, DEC-003, DEC-033; current whole-file ledger and planning-state revision evidence | DEC-037 assigns only apply mechanics to the store; semantic decisions remain with command owners, so no duplicate target owner is created. | CCFG-21 store/fault injection; CCFG-24 intake integration; CCFG-26 closeout integration. |

```yaml
slice_2_acceptance:
  approval:
    exact_response: Approve all four
    stable_receipt_commit: 19e0746cdc7f681ebe4e6b0ab0be62640097ea6f
  schema_evolution_policy_accepted:
    value: true
    decision: DEC-036
  ledger_store_boundary_accepted:
    value: true
    decision: DEC-037
  implementation_started: false
```

At the Slice 2 exit, the approved runner boundary remained for Slice 3 and the
approved OPEN-003 transaction remained for Slice 4. CCFG-20 through CCFG-29
remain deferred implementation owners; this record selects none of them.

## Slice 3 Approved Runner And Topology Boundaries

The stable planning receipt at commit
`a0fdef399955f17a778c7d8b61ea56a4fca49e76` retains the user's exact response
`Approve all four` and the complete approved runner outcome. Slice 3 records
that outcome under the existing single runner decision owner, DEC-017. DEC-018
continues to own the distinct rule that `work-batch` closes only its current
batch and stops.

### Public-command runner protocol

```yaml
runner_target_protocol:
  decision_owner: DEC-017
  command_sequence:
    - invoke_public_plan_batch
    - validate_plan_batch_result
    - invoke_public_work_batch_when_plan_batch_returns_executable_work
    - validate_work_batch_result
  loop:
    bound: explicit
    later_iteration_starts_with: fresh_plan_batch_invocation
    closeout_readiness_interpretation: forbidden
  child_process_lifecycle:
    owner: runner
    responsibilities:
      - launch
      - observe
      - collect_result
      - terminate_or_wait_on_stop
  retained_runner_responsibilities:
    - process_lifecycle
    - environment_selection
    - sandbox_selection
    - telemetry
    - receipts
    - command_result_validation
    - stop_policy
  target_result_and_transition_semantics:
    may_report:
      - invoked_public_command
      - validated_command_result
      - child_process_outcome
      - loop_count_and_bound
      - selected_environment_and_sandbox
      - telemetry_and_receipt_evidence
    successor_readiness_present: false
    forbidden_fields_or_meanings:
      - next_batch_ready
      - successor_ready
      - closeout_derived_successor_readiness
      - selected_successor_identity
  semantic_authority_retained_by_commands:
    plan_batch:
      - finding_selection
      - successor_planning
      - dispatch_and_runway_design
    work_batch:
      - execution_acceptance
      - same_batch_closeout_meaning
```

An explicit loop bound authorizes only another iteration. It does not make a
closed batch evidence that a successor exists or is ready. Every later
iteration starts by invoking `plan-batch` as a fresh public command; that
command alone may select and prepare later work. The runner validates public
command results and retains process lifecycle, environment and sandbox
selection, telemetry and receipt handling, and stop-policy responsibility. It
neither reconstructs APR or Batch Runway phases nor derives a successor
transition from closeout.

### Current topology is migration evidence

The current implementation still routes directly through APR and Batch Runway
phases and exposes closeout-derived `next_batch_ready` behavior. Those surfaces
characterize the migration source; they do not define the accepted protocol.
The existing findings already own their rewrite and deletion:

| Current surface | Disposition | Existing finding owner |
|---|---|---|
| APR planning phases and Batch Runway create-spec routing | Move selection, scope, dispatch, runway, risk, approval, and validation-profile behavior behind public `plan-batch`; remove the old decision path. | CCFG-25; final legacy deletion in CCFG-28. |
| Batch Runway execute/recovery/finalize phases and APR closeout routing | Move execution through same-batch reconciliation behind public `work-batch`; remove closeout interpretation from APR. | CCFG-26; final legacy deletion in CCFG-28. |
| Runner fixed-phase dispatch, phase prompts, phase observations, and facade/import topology | Rewrite against public command invocation, result validation, explicit loop bounds, and process lifecycle. | CCFG-27; delete remaining legacy topology in CCFG-28. |
| `next_batch_ready`, closeout-readiness checks, and closeout-to-select transitions in T11 and T13 | Replace with a fresh `plan-batch` invocation on a later bounded iteration; delete the closeout-derived successor protocol. | CCFG-27; deletion completion in CCFG-28. |
| Topology-only assertions across T02, T05, T08-T13, T16-T20, T27, and T28 | Replace only behavior that survives at the public command seam; delete assertions whose only subject is APR, Batch Runway, a fixed phase, facade/import location, or dependency topology. | CCFG-23 owns topology-independent scenarios; CCFG-25 through CCFG-27 supply migrated behavior; CCFG-28 removes obsolete tests. |

This disposition does not authorize test, runner, installer, manifest, agent,
or source changes in CCFG-19.

### CCFG-18 durable generation evidence

The canonical CCFG-18
[`closeout.md`](https://github.com/alacasse/codex-config/blob/968f41d1ad752e817af518b12fb8f96273b76e0d/docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/closeout.md)
and
[`completed-slices.md`](https://github.com/alacasse/codex-config/blob/968f41d1ad752e817af518b12fb8f96273b76e0d/docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/completed-slices.md)
at corrected durable closeout commit
`968f41d1ad752e817af518b12fb8f96273b76e0d` are the topology record. The
fixture-isolation and rollback ledger receipt within that record is
`34202189a20313cbb3420e03507dd0165c0df2b6`.
They establish these facts:

| Fact | Durable evidence |
|---|---|
| Roots and generations | Stable repository `/home/alacasse/projects/codex-config` with `/home/alacasse/.codex` and canonical-write authority; candidate repository `/home/alacasse/projects/codex-config-command-owner-redesign` with `/home/alacasse/.codex-command-owner-redesign` and no canonical-write authority. |
| Authoritative base and accepted snapshot | `da5b97165eb8d8c9f809a64937bcc9d753032ee7` and `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c` are both ancestors of the ancestry-preserving merge `b044e3c348922663aa074638227aae8d2633cfe3`. |
| Candidate branch and established head | Branch `implementation/command-owner-redesign`; CCFG-18 candidate evidence head `9027bd1ea35e66e263dfced02a2b9f91835c1bd9`. The Slice 3 base `07c5d41882b6df83bc8298854a83d59a3006b555` remains on that branch with both lineage commits as ancestors. |
| Isolated installation | Stable and candidate status checks passed, all 25 candidate links resolved only to the candidate repository, stable links did not resolve to the candidate, and candidate `auth.json` remained absent. |
| Canonical-write rejection | The candidate strict context mechanically rejected a canonical-planning write request; the fixture session wrote only below its fixture root. |
| Quiescence and rollback | Selected, queued, active, and resumable fixture state were all absent; stable default-path rollback passed through the normal shell Codex CLI. |
| Default generation | `default_generation_switched: false`; stable links and the stable default generation remained unchanged. Slice 3 remains controlled by the stable helper and stable `CODEX_HOME`. |

```yaml
slice_3_acceptance:
  approval:
    exact_response: Approve all four
    stable_receipt_commit: a0fdef399955f17a778c7d8b61ea56a4fca49e76
  runner_target_protocol_accepted:
    value: true
    decision: DEC-017
  topology_verification:
    value: true
    durable_ccfg_18_closeout_commit: 968f41d1ad752e817af518b12fb8f96273b76e0d
    fixture_evidence_receipt_commit: 34202189a20313cbb3420e03507dd0165c0df2b6
    current_candidate_branch: implementation/command-owner-redesign
    current_candidate_head: 07c5d41882b6df83bc8298854a83d59a3006b555
  successor_readiness_in_target_semantics: false
  implementation_started: false
  default_generation_switched: false
```

The approved OPEN-003 planning transaction remains for Slice 4. CCFG-20
through CCFG-29 remain deferred and unselected; Slice 3 performs no generation
switch, bridge removal, implementation, or successor selection.

## Slice 4 Planning Transaction And Exit Audit

The stable planning receipt at commit
`4b3695d8628361649aab1f9d2a8defedd6e738cb` retains the user's exact response
`Approve all four` and the approved OPEN-003 staged saga. DEC-038 resolves
OPEN-003 without implementing a transaction, changing a schema, or transferring
planning ownership.

### Idempotent four-stage saga

| Stage | Operation | Required binding or CAS inputs | Durable result |
|---|---|---|---|
| 1 | Write and validate dispatch. | Before the write, the append-only record binds the transaction ID, program/finding/batch, exact initial ledger/state revision and idle expectation, dispatch path and payload/hash, intended runway path, command-owner/schema versions, and four-stage plan. | Append the observed dispatch revision and validation result. |
| 2 | CAS idle to selected, then persist the selected transition receipt. | Before the CAS, append its exact input using the initial state revision and observed Stage 1 dispatch revision. | Append the observed selected-state revision, receipt revision, and validation result. |
| 3 | Write and validate runway. | After Stage 2 and before the write, append the now-computable exact runway payload/hash bound to the observed dispatch revision and expected selected-state revision. The extension must persist first. | Append the observed runway revision and validation result. |
| 4 | CAS selected to queued, then persist the queued transition receipt. | Before the CAS, append its exact input using the observed selected state, dispatch revision, and runway revision. | Append the observed queued-state revision, receipt revision, and validation result. |

The transaction ID is also the idempotency key for one append-only transaction
record. Initial intent contains only values known before Stage 1; it explicitly
does not claim a future runway payload/revision or transition/receipt output
revision. Prior fields are immutable. Every later input is appended before its
corresponding effect, and every observed artifact, state, receipt revision, and
validation result is appended immediately afterward.

An extension is legal only in the exact next saga state with all prior receipts
and revisions matching. Before any retry write or CAS, the caller must match
every immutable binding established so far. Exact retry returns or reconstructs
the same completed-stage result and resumes at the first incomplete stage.
Reusing the ID with different payload, batch, state, or artifact lineage blocks;
ambiguous partial evidence also blocks.

For a CAS applied before its receipt is appended, recovery consults the durable
pre-effect transaction-record input and observed state, then reconstructs and
appends the same receipt without reapplying the transition. This is the narrow
receipt-recovery requirement, not permission for `planning-state` or a store to
choose a batch or interpret planning semantics.

### Full fault model

| Failure checkpoint | Required recovery |
|---|---|
| Before dispatch write | Require the immutable initial-intent record to match, then retry Stage 1. |
| During or after dispatch write, before validation/output append | Atomic persistence leaves the dispatch missing or present. Retry an absent exact write; validate a present artifact and append its observed revision/result; block on mismatch. |
| After dispatch observation append | Append the exact selected-CAS input for the next saga state, then resume Stage 2. |
| Before idle-to-selected CAS | Require the exact selected-CAS input extension and all prior bindings to match. |
| After idle-to-selected CAS, before selected receipt/output append | Do not reapply the CAS. Consult the pre-effect record and observed state, recover the same receipt, and append observed state/receipt revisions and validation; block on ambiguity. |
| After selected output append | Exact replay returns the same receipt, then atomically append the now-computable runway input before Stage 3. |
| Before runway write | Require the persisted exact runway payload/hash, observed dispatch-revision binding, expected selected-state revision, and all prior bindings to match. |
| During or after runway write, before validation/output append | Atomic persistence leaves the runway missing or present. Retry an absent exact write; validate a present artifact and append its observed revision/result; block on mismatch. |
| After runway observation append | Append the exact queued-CAS input for the next saga state, then resume Stage 4. |
| Before selected-to-queued CAS | Require the exact queued-CAS input extension and all prior bindings to match. |
| After selected-to-queued CAS, before queued receipt/output append | Do not reapply the CAS. Consult the pre-effect record and observed state, recover the same receipt, and append observed state/receipt revisions and validation; block on ambiguity. |
| After queued output append | Exact replay returns the completed saga result without rewriting artifacts or transitions. |

At every checkpoint, the append-only transaction record and every durably
written dispatch, selected transition, selected receipt, runway, queued
transition, or queued receipt remain visible. Rollback may append a blocker or
recovery state, but deletion must not erase or hide any of those facts. CCFG-21
owns the transaction-record schema, prototype, atomicity, and fault-injection
implementation. CCFG-25 owns integration into `plan-batch` and the planning
ownership transfer.

### Remaining open decisions

No direct CCFG-19 evidence makes OPEN-004 through OPEN-008 necessary for one of
the seven exit keys. They remain open, explicitly non-blocking, and deferred:

| Question | CCFG-19 status | Deferred decision point |
|---|---|---|
| OPEN-004 universal versus overrideable per-slice commit profile | Non-blocking | CCFG-26 execution/commit ownership. |
| OPEN-005 exact slice-count rule | Non-blocking | CCFG-25 planning ownership. |
| OPEN-006 final Python module split | Non-blocking | CCFG-21 implementation seams. |
| OPEN-007 worker/reviewer renaming | Non-blocking | CCFG-26 or CCFG-28 after ownership transfer and deletion shape are known. |
| OPEN-008 prototype-directory retention | Non-blocking | CCFG-21 only if a reviewable comparison requires it. |

### Seven-key exit audit

| Acceptance key | Required value | Traceable evidence | Audit result |
|---|---:|---|---|
| `contract_to_owner_map_complete` | `true` | All 31 rows in Joined Contract Evidence name one target owner; `ownership_conflict_computation` reports zero missing owners. | Satisfied. |
| `contract_to_scenario_map_complete` | `true` | Scenario Resolution Addendum resolves all 16 referenced gaps, and all 31 joined rows name resolved scenarios. | Satisfied. |
| `blocking_ownership_conflicts` | `0` | `ownership_conflict_computation` reports zero contracts with zero or multiple target decision owners and records the apparent-overlap dispositions. | Satisfied. |
| `schema_evolution_policy_accepted` | `true` | DEC-036 and `slice_2_acceptance`, authorized by the exact approval response. | Satisfied. |
| `ledger_store_boundary_accepted` | `true` | DEC-037 and `slice_2_acceptance`, authorized by the exact approval response. | Satisfied. |
| `runner_target_protocol_accepted` | `true` | DEC-017 and `slice_3_acceptance`, including retained runner responsibilities and absent successor readiness. | Satisfied. |
| `planning_transaction_ready_or_explicitly_blocked` | `true` | DEC-038 resolves OPEN-003 with one append-only transaction record, known-value initial intent, state-gated input/output extensions, ordered stages, exact CAS inputs, idempotency, mismatch blocking, visible partial evidence, receipt recovery, and deletion prohibition. | Satisfied. |

```yaml
ccfg_19_exit_audit:
  acceptance_keys:
    contract_to_owner_map_complete: true
    contract_to_scenario_map_complete: true
    blocking_ownership_conflicts: 0
    schema_evolution_policy_accepted: true
    ledger_store_boundary_accepted: true
    runner_target_protocol_accepted: true
    planning_transaction_ready_or_explicitly_blocked: true
  keys_audited: 7
  keys_satisfied: 7
  blocking_decisions_remaining: 0
  open_003:
    status: resolved
    decision: DEC-038
    transaction_record: append_only
    initial_intent_binds_future_values: false
    later_bindings: exact_next_state_extensions_before_effects
  non_blocking_open_decisions:
    - OPEN-004
    - OPEN-005
    - OPEN-006
    - OPEN-007
    - OPEN-008
  record_status: decision_complete_pending_stable_same_batch_closeout
  implementation_started: false
  successor_selected: null
```

### Deferred implementation remains unselected

```yaml
deferred_implementation:
  CCFG-20: skill-contract-v1 schema and validators
  CCFG-21: planning schemas, append-only transaction record, saga prototype, atomicity, and fault injection
  CCFG-22: skill-authoring-v1 completion and validation
  CCFG-23: topology-independent behavioral scenario harness
  CCFG-24: add-to-ledger intake ownership transfer
  CCFG-25: plan-batch ownership transfer and DEC-038 integration
  CCFG-26: work-batch execution and closeout ownership transfer
  CCFG-27: candidate cutover preparation and rehearsal
  CCFG-28: legacy-owner deletion and final candidate cutover
  CCFG-29: contract-first convergence and final integration
selected_findings: []
```

The candidate CCFG-19 decision record satisfies all seven acceptance keys and
is ready for coordinator-owned review, candidate commit, and stable same-batch
closeout. It does not close CCFG-19 itself, select a successor, or authorize any
deferred implementation.
