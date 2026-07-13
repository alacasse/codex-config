# Deletion Conditions

## Purpose

This document defines measurable conditions for deleting
`architecture-program-runway`, `batch-runway`, expired compatibility, stale
installation routes, and the temporary cross-checkout bridge.

Deletion is not established by document intent or repository search alone. It
requires source, installation, direct-invocation, behavior, and historical
classification evidence.

## General Rules

- Physical deletion follows completed ownership transfer.
- A temporary bridge with a live caller blocks deletion.
- Historical references may remain only under classified archive roots.
- A clean generation-specific `CODEX_HOME` is the installation source of truth.
- Omitted features must be absent, not retained from prior installed state.
- The default generation does not switch until candidate deletion proof passes.
- Same-batch closeout after the switch is controlled by the already-loaded stable
  controller and stops before successor selection.

## Reproducible Active-Surface Report

Every deletion decision produces:

```yaml
deletion_report:
  repository_commit: full-sha
  candidate_generation_commit: full-sha
  codex_home: absolute-path
  active_file_roots: []
  historical_file_roots: []
  searched_identifiers: []
  active_matches: []
  allowed_historical_matches: []
  unresolved_matches: []
  installed_links: []
  stale_installed_links: []
  direct_invocation_results: []
  clean_install_result: passed | failed
  target_scenario_result: passed | failed
  full_test_result: passed | failed
```

Allowed historical roots include clearly archived planning artifacts and closed
reports. Active roots include skills, agents, manifests, scripts, current docs,
prompts, tests, fixtures used by current runtime, and installed `CODEX_HOME`
links.

Unclassified matches block deletion.

## Architecture Program Runway Deletion Conditions

All must be true:

```yaml
architecture_program_runway:
  intake_callers: 0
  selection_callers: 0
  dispatch_callers: 0
  queue_callers: 0
  closeout_callers: 0
  runner_mode_callers: 0
  command_owner_dependencies: 0
  installed_feature_routes: 0
  installed_symlinks: 0
  active_schema_or_result_contract_dependencies: 0
  active_old_format_artifacts_requiring_skill: 0
  resumable_runs_requiring_skill: 0
  tests_requiring_presence: 0
  direct_invocation_available: false
  target_behavioral_scenarios_green: true
```

Surviving responsibilities must already belong to:

- `add-to-ledger` for intake;
- `plan-batch` for selection, shaping, dispatch, and queue preparation;
- `work-batch` for same-batch closeout interpretation;
- narrow state/artifact/ledger mechanisms for applying explicit decisions;
- independent runner for process lifecycle only.

## Batch Runway Deletion Conditions

All must be true:

```yaml
batch_runway:
  create_spec_callers: 0
  execute_spec_callers: 0
  recovery_callers: 0
  finalization_callers: 0
  command_owner_dependencies: 0
  worker_contract_dependencies: 0
  reviewer_contract_dependencies: 0
  result_schema_dependencies: 0
  installed_feature_routes: 0
  installed_symlinks: 0
  active_old_format_artifacts_requiring_skill: 0
  resumable_runs_requiring_skill: 0
  tests_requiring_presence: 0
  direct_invocation_available: false
  target_behavioral_scenarios_green: true
```

Surviving planning references live under `plan-batch`; execution, recovery,
finalization, retention, and closeout references live under `work-batch` or a
narrow neutral mechanism.

## Mode and Routing Deletion

Remove active references to:

```text
intake-findings
group-batches
select-next-batch
create-next-runway
closeout-runway
create-spec
execute-spec
```

The words may remain in historical evidence only when classified as such.

Current command metadata, runner prompts, manifests, agents, and active docs must
use public command protocols.

## Installer and Clean-Generation Conditions

Before final switch:

```yaml
clean_generation:
  built_from_empty_directory: true
  one_candidate_source_commit: true
  all_links_resolve_under_candidate_source_root: true
  manifest_digest_recorded: true
  contract_hashes_recorded: true
  omitted_features_absent: true
  stale_links: 0
  APR_routes: 0
  Batch_Runway_routes: 0
  direct_old_commands_callable: false
```

The installer must not expose a partially replaced generation. A failed install
leaves the previous default binding unchanged.

## Test and Fixture Deletion

Delete or rewrite tests that only require:

- old directories;
- old mode names;
- old dependency lists;
- exact old ownership prose;
- aliases or wrappers with no supported caller.

Retain behavior tests for:

- intake and one-batch planning;
- active-state precedence;
- risk and approval gates;
- execution, recovery, and resume;
- independent review and focused commits;
- closeout and no successor selection;
- root and generation isolation;
- installation and rollback;
- historical artifacts not becoming active.

Expired migration fixtures and legacy parsers are removed when no active or
resumable state requires them.

## Historical Artifact Policy

Archived artifacts may preserve old names and structures when:

- their archive root is classified;
- they are read-only evidence;
- they cannot become active through normal pickup;
- no installed old skill is required merely to read them;
- active state and new artifacts use current schemas.

## CCFG-27 Cutover-Preparation Conditions

CCFG-27 closes only when:

```yaml
CCFG_27:
  default_generation_switched: false
  command_owner_legacy_dependencies: 0
  runner_old_modes: 0
  runner_successor_readiness_decisions: 0
  agent_legacy_path_dependencies: 0
  clean_candidate_install_rehearsal: passed
  legacy_routes_installed_in_rehearsal: 0
  atomic_switch_rehearsal: passed
  rollback_rehearsal: passed
  fresh_candidate_fixture_workflow: passed
  canonical_candidate_writes: 0
  quiescence_protocol: passed
```

Legacy source directories may still exist after CCFG-27, but they are no longer
normal routes and are not installed in the rehearsal generation.

## CCFG-28 Final Deletion and Cutover Conditions

Immediately before the switch:

```yaml
pre_switch:
  CCFG_27_closed: true
  candidate_commit_pinned: true
  stable_controller_generation_pinned: true
  selected: null
  queued: null
  active: null
  resumable_stable_runs: false
  concurrent_canonical_writers: 0
  rollback_checkpoint_valid: true
```

Candidate source and clean installation:

```yaml
candidate_source:
  architecture_program_runway_directory_exists: false
  batch_runway_directory_exists: false
  active_old_mode_references: 0
  topology_tests_requiring_presence: 0
  active_legacy_parsers: 0
clean_install:
  legacy_features_installed: 0
  legacy_symlinks_present: 0
  direct_legacy_commands_callable: false
  worker_reviewer_contracts_resolve: true
  runner_public_protocols_only: true
```

Validation:

```yaml
validation:
  schema_and_dependency_validation: green
  target_behavioral_scenarios: green
  root_and_generation_scenarios: green
  full_repository_tests: green
  controlled_end_to_end_fixture: green
  archived_history_readability: green
  archived_history_active_pickup: false
```

Switch transaction:

```yaml
cutover:
  atomic_default_switch: green
  fresh_candidate_read_only_diagnostic: green
  stable_controller_generation_unchanged: true
  stable_controller_reloaded_default_skills: false
  candidate_canonical_write_before_new_batch: false
  CCFG_28_same_batch_closeout_complete: true
  stable_controller_stopped: true
resulting_state:
  default_generation: candidate
  selected: null
  queued: null
  active: null
  resumable_stable_run: false
```

Failure before stable closeout restores the previous default binding. Candidate
canonical work is not allowed until a new post-cutover batch starts.

## CCFG-29 Bootstrap Bridge Deletion

The temporary cross-checkout bridge may be deleted only when:

```yaml
CCFG_29:
  implementation_branch_merged_into_latest_master: true
  target_toolchain_content_verified: true
  default_toolchain_rebound_to_master: true
  fresh_master_bound_session_green: true
  canonical_planning_root_is_master: true
  implementation_target_root_is_master_for_future_work: true
  temporary_cross_checkout_callers: 0
  bridge_installed_routes: 0
  bridge_source_deleted: true
  candidate_branch_retired_or_frozen: true
```

## Final Deletion Test

The final proof is:

```text
physically delete old owners and expired bridges
-> build clean candidate generation from empty directory
-> prove old commands unavailable
-> run target behavior and full repository tests
-> perform controlled cutover
-> close CCFG-28 without successor selection
-> later integrate candidate into master under CCFG-29
-> remove cross-checkout bridge
-> run fresh master-bound smoke test
```

A compatibility wrapper that makes the old command work does not satisfy the
proof.
