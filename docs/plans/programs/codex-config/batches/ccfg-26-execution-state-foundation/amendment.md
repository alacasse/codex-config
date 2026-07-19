# CCFG-26 Execution-State Foundation Bootstrap Amendment

## Status And Precedence

- Status: bounded planning correction; implementation has not started.
- Applies to: the already queued
  `ccfg-26-execution-state-foundation` batch.
- Batch identity and queue path: unchanged.
- Slice count: unchanged at two implementation Slices.
- Precedence: when this amendment conflicts with `dispatch.md`, `runway.md`, or
  `review.md`, this amendment controls.
- Execution gate: this amendment authorizes no execution until
  `amendment-review.md` records a clean verdict for its exact SHA-256.
- Successor effect: none. CCFG-26 remains partially open and CCFG-26C through
  CCFG-26E and CCFG-27 through CCFG-29 remain unselected.

The original artifacts remain immutable historical planning evidence:

```yaml
original_evidence:
  dispatch:
    path: docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/dispatch.md
    sha256: f6b9b04c153ad24f301e6e2b324accaf887f5e394c9a7a64d5c9196fd0e5e65d
  queued_runway:
    path: docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/runway.md
    sha256: d39864d65fa92314aff890a280f605a165c1d0195ab07244ef2a655755537736
  original_review:
    path: docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/review.md
    sha256: d5d4cf2318482634aae2aa5233499f11621965a50c47eaee5e56ba9fe3d4512b
    disposition: historical_only
    reason: the clean verdict did not detect the self-hosting bootstrap contradiction and cannot authorize execution by itself
immutable_planning_snapshot:
  toolchain_commit: 93fa9109e35719d4f36dd75edc97bf0df584c1da
  canonical_planning_commit_before: 93fa9109e35719d4f36dd75edc97bf0df584c1da
  implementation_commit_before: 5c5ec9d52dd9033daa45f3a200031c152363b62c
```

`work-batch` must consume the original dispatch, runway, and review together
with this amendment and its clean exact review. The original planning snapshot
remains historical evidence; a later execution invocation must obtain a fresh
ready live lease before any write-bearing handoff.

## Correction Reason

The original plan incorrectly made the candidate machinery produced by Slice 1
the execution authority for developing Slice 2 of the same real batch.

The temporary stable-runway policy produces this real sequence:

```text
stable work-batch invocation 1 -> completes implementation Slice 1 -> stops
stable work-batch invocation 2 -> develops implementation Slice 2
```

The original Slice 2 instead initialized a new Batch Execution State from the
real two-Slice runway and reserved its first incomplete Slice. Version 1
initialization creates an empty completed prefix and has no event that imports a
legacy completed prefix. It would therefore select Slice 1 again even though the
stable controller had already completed it.

Do not add `initialize_from_legacy_completed_prefix`, another migration event,
or another evidence owner to repair this contradiction. That would recreate
dual authority and an unnecessary legacy-state migration protocol.

## Corrected Control-Plane Seam

Slice 1's execution-state module is a code dependency of Slice 2. It is not the
controller that chooses, develops, accepts, commits, or archives the real Slice
2 implementation.

| Scenario | Execution authority | Candidate machinery role | Durable real-batch state |
|---|---|---|---|
| Develop real implementation Slice 1 | stable `work-batch` plus its existing stable Batch Runway support | code under construction and fixture-tested only | existing stable runway ledger and completed-slice evidence |
| Develop real implementation Slice 2 | stable `work-batch` plus its existing stable Batch Runway support | code dependency and fixture-tested target only | existing stable runway ledger and completed-slice evidence |
| Prove the candidate one-flight seam | explicit acceptance driver over disposable fixture roots | real candidate runner, public `work-batch`, and execution-state module exercise their production interfaces | disposable fixture Batch Execution State only |
| Real candidate runtime after cutover | later CCFG-26/27/28/29 evidence and cutover decision | future runtime authority | later configured persistent run-artifact root |

Required invariants:

- The stable controller remains the sole controller of the real
  `ccfg-26-execution-state-foundation` implementation batch.
- No candidate process may reserve, launch, resolve, or derive the next real
  implementation Slice for this batch.
- Stable code must not import or load candidate code as runtime authority.
- Candidate production interfaces may be exercised only against disposable
  fixtures until the later cutover gate explicitly transfers authority.
- No compatibility path may copy the stable completed prefix into candidate
  Batch Execution State.

## Runtime Artifact Correction

The following original values are withdrawn from the executable plan:

```yaml
withdrawn_runtime_input:
  root: /tmp/tmp.nAyp7HeqwO
  canonical_state_path: /tmp/tmp.nAyp7HeqwO/batch-executions/codex-config/ccfg-26-execution-state-foundation/execution-state.json
  disposition: must_not_be_created_or_consumed
```

Corrected project values:

```yaml
run_artifact_root: null
run_artifact_location_for_real_batch: null
state_file_policy: generated-only
fixture_root_policy:
  allocation: each test or bounded acceptance scenario uses the host platform temporary-directory facility at execution time
  lifetime: one self-contained fixture scenario only
  persistence: never recorded as the real batch run-artifact location
  portability: reusable code and fixtures receive the path explicitly and embed no platform-specific default
```

Slice 1 allocates independent temporary roots for public-interface,
multi-process, crash, lock, replay, receipt, and projection tests. Slice 2
allocates one fresh scenario root that contains its disposable planning fixture,
implementation target, Batch Execution State, receipts, and generated reports.
The scenario may keep that exact root across its two explicitly launched test
processes, then deletes it when the bounded acceptance ends.

No `/tmp` path, host-specific path, or planner-created temporary directory is a
durable prerequisite for executing or closing the real implementation batch.

## Corrected Slice Contracts

### Slice 1: Canonical Execution-State Module

The original Slice 1 module/interface, persistence, CAS, replay, lock,
receipt/projection, process-test, and cross-platform workflow scope remains in
force with these corrections:

- every consumer is a generated-only public module CLI or test fixture;
- every fixture creates its own host-native temporary root at test time;
- no real CCFG-26 batch state or durable run-artifact location is created;
- no production runner or public `work-batch` caller becomes real-batch
  authority; and
- after the stable controller commits Slice 1, it stops and leaves Slice 2 to a
  later explicit stable `work-batch` invocation.

Slice 1's independently useful result is the deep module through its public
interface and executable fixture acceptance. It is not a self-hosted execution
controller.

### Slice 2: Fixture-Only Real Caller Tracer

Risk class: `migration`.

```yaml
vertical_slice:
  starting_scenario: the stable controller has already completed real implementation Slice 1; no real Batch Execution State exists; a disposable planning fixture with two ordered fixture Slices and a disposable implementation target are allocated at execution time
  durable_result: candidate production interfaces prove one completed Execution Flight and one exact fresh manual resume against fixture-only state while the stable controller remains the sole controller of the real implementation batch
  owner_before: candidate runner execute routes semantic execution through Batch Runway public support
  owner_after: candidate public work-batch owns proceed, reserve, authorize, accept, resolve, and stop decisions only inside the tested target seam; runner owns process lifecycle; execution-state module owns fixture progression
  migrated_callers:
    - candidate serialized execute phase contract exercised through the executable runner fixture
    - public candidate work-batch fixture route
    - command-owner behavioral acceptance fixture
  focused_validation:
    - real candidate runner and public work-batch production interfaces execute against disposable planning and implementation targets
    - fixture flight 1 completes only fixture-slice-1 and derives continue_same_batch
    - the first candidate coordinator process exits
    - an explicitly launched fresh process uses the same fixture state and selects only fixture-slice-2 without repeating fixture-slice-1
    - no real CCFG-26 state, target edit, finalization, closeout, automatic continuation, or successor exists
  independently_usable_state: the candidate seam is proven end to end without becoming authority for the batch that implements it
  rollback_boundary: revert only the Slice 2 candidate commit; Slice 1 remains usable and all fixture roots are disposable
  temporary_residue:
    - real implementation execution stays under the stable controller until later cutover
    - automatic continuation, recovery, finalization, closeout, and remaining Batch Runway callers remain later reviewed work
```

#### Fixture Topology

The Slice 2 acceptance driver allocates, within one host-native temporary
scenario root:

- a Planning Artifact Layout fixture with one queued fixture runway;
- a unique fixture program and batch identity that cannot equal
  `codex-config/ccfg-26-execution-state-foundation`;
- a two-Slice fixture runway with deterministic, harmless fixture edits;
- a disposable Git implementation target seeded from the exact candidate
  baseline needed by the test;
- a fixture Batch Execution State path; and
- fixture result, receipt, projection, and report paths.

The acceptance uses the real candidate runner entrypoint, public `work-batch`
route, execution-state module, schemas, validation, and transition derivation.
Dependency injection may substitute deterministic fixture worker/reviewer
adapters at their existing seams; it must not bypass the public runner or
execution-state interfaces being migrated.

The acceptance driver explicitly launches two separate candidate processes:

1. flight 1 completes only `fixture-slice-1`, persists its exact result and
   receipt, derives `continue_same_batch`, returns the compatible stopped Phase
   Result, and exits;
2. the test driver, not an automatic runner loop, launches a fresh process;
   flight 2 loads the same fixture state, selects only `fixture-slice-2`, and
   proves `fixture-slice-1` cannot be repeated. It may complete the harmless
   second fixture Slice so the scenario can validate a complete prefix.

This is explicit manual-resume acceptance. It does not implement Automatic
Same-Batch Continuation.

#### Forbidden Slice 2 Behavior

- Do not initialize Batch Execution State for the real implementation batch.
- Do not pass the real queued CCFG-26 runway to the candidate coordinator.
- Do not use candidate state to decide which real implementation Slice the
  stable controller should execute.
- Do not import the stable completion archive into candidate state.
- Do not add a legacy-prefix initialization or migration event.
- Do not write to the canonical stable planning root from the candidate
  acceptance process.
- Do not use an in-repo or planner-created persistent fixture root.
- Do not implement automatic continuation, recovery, finalization, target
  closeout, successor selection, or a generation switch.

## Exact Baseline Commands And Failure Disposition

All commands below run from
`/home/alacasse/projects/codex-config-command-owner-redesign` at candidate
baseline `5c5ec9d52dd9033daa45f3a200031c152363b62c`.

### Affected Runner And Manifest Pytest Baseline

Exact argv:

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_architecture_program_runner.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_validation.py tests/test_custom_agent_contracts.py tests/test_codex_features_manifest.py
```

Observed baseline:

```yaml
status: known-red-baseline
passed: 124
failed: 2
subtests_passed: 443
failed_nodes:
  - tests/test_architecture_program_runner_protocol.py::ArchitectureProgramRunnerProtocolTests::test_skill_points_local_runner_usage_to_protocol
  - tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_work_batch_reconciles_same_batch_closeout
```

Failure disposition:

| Node | Classification | Preserve | Required outcome | Forbidden remediation |
|---|---|---|---|---|
| `test_skill_points_local_runner_usage_to_protocol` | topology/prose assertion left stale by the candidate narrowing of Architecture Program Runway | the local runner reference remains discoverable where a live caller actually needs it | rewrite or remove the stale assertion according to the accepted owner interface; the exact affected command must become green by Slice 2 closeout | restoring removed planning behavior or adding unused prose solely to satisfy `assertIn` |
| `test_work_batch_reconciles_same_batch_closeout` | compatibility-retention assertion over exact prose | existing stable same-batch closeout remains callable for the real implementation batch and no successor is selected | replace exact-string assertions with the narrow retained behavior/owner contract, or remove redundant assertions; the exact affected command must become green by Slice 2 closeout | pulling target closeout into Slice 2, restoring exact wording only for the test, or treating Architecture Program Runway as the target happy-path execution owner |

Both nodes are Slice 2-owned test disposition work because Slice 2 changes the
adjacent routing/owner contracts. They are not evidence that target closeout or
removed Architecture Program Runway planning behavior belongs in this batch.
Before Slice 2 they remain diagnostic known-red evidence. After the dispositions
and target behavior are implemented, rerun the exact argv and promote it to
`required-green` only with zero failed nodes.

### Runner BasedPyright Baseline

Exact argv:

```text
.venv/bin/basedpyright --outputjson scripts/architecture_program_runner.py scripts/architecture_program_runner_artifacts.py scripts/architecture_program_runner_command.py scripts/architecture_program_runner_environment.py scripts/architecture_program_runner_phase_contract.py scripts/architecture_program_runner_state.py scripts/architecture_program_runner_transition.py scripts/architecture_program_runner_validation.py scripts/architecture_program_runner_workers.py
```

Observed normalized baseline:

```yaml
status: known-red-baseline
files_analyzed: 9
errors: 56
warnings: 0
information: 0
diagnostic_files:
  - scripts/architecture_program_runner_artifacts.py
  - scripts/architecture_program_runner_state.py
  - scripts/architecture_program_runner_validation.py
  - scripts/architecture_program_runner_workers.py
normalization: relative file, severity, message, rule, and range serialized as sorted-key compact JSON in tool output order
normalized_diagnostics_sha256: f13d6aceae19246213a8189a2c678edeaac241f3bf58b58bd021e29f8fbae861
```

Execution must rerun this exact JSON command, apply the same normalization, and
reject any new or changed diagnostic outside an explicitly fixed baseline
diagnostic. New execution-state and execution-flight modules remain
`required-green` with zero diagnostics.

### Other Reproducible Gates

```yaml
commands:
  - environment: {PYTHONDONTWRITEBYTECODE: "1"}
    argv: [.venv/bin/python, scripts/command_owner_scenarios.py, validate, tests/fixtures/command-owner-scenarios]
    status: required-green
    planning_baseline: 82 scenarios passed
  - argv: [.venv/bin/python, scripts/skill_contract.py, validate, --toolchain-root, ., skills/work-batch/SKILL.md]
    status: known-red-baseline
    planning_baseline: "contract.block_count: expected exactly one ## Contract YAML block; found 0"
    remediation_owner: Slice 2 adds and validates the target public work-batch command-owner contract before promotion to required-green
  - argv: [./install.sh, --codex-home, /home/alacasse/.codex-command-owner-redesign, --status]
    status: required-green
  - argv: [./install.sh, --codex-home, /home/alacasse/.codex-command-owner-redesign, --all, --dry-run]
    status: required-green
```

Ruff and pytest commands over implementation-created files must name their
exact paths after those paths exist. A generic phrase such as “focused subset”
is not a validation receipt.

## Cross-Platform Gate

The focused Ubuntu, macOS, and Windows real-process/lock workflow remains an
implementation-created Slice 1 artifact. Local syntax and command inspection
become required-green after creation. Green jobs against the exact candidate
commit remain mandatory before the implementation batch can close.

The workflow itself uses host-native temporary directories. It must not refer
to the withdrawn Linux path or claim to exercise the real CCFG-26 batch.

## Final Validation Corrections

After both real implementation Slices have been completed by separate stable
`work-batch` invocations:

1. verify Planning State still identifies this same batch and no successor;
2. obtain a fresh strict live lease and validate the exact candidate range;
3. run the exact pytest and BasedPyright baselines above with their corrected
   green/non-regression expectations;
4. run all implementation-created state and fixture-flight tests;
5. run exact command-owner scenario validation and acceptance with fresh
   host-native temporary output roots allocated for that validation only;
6. validate reports before deleting or releasing their temporary scenario
   roots;
7. verify candidate installation convergence and unchanged stable-home content;
8. require exact Ubuntu/macOS/Windows workflow evidence;
9. run delta-only test-quality review, independent runway review, and
   import-topology review only if its trigger is met; and
10. close only this implementation batch through the existing stable
    mechanisms, leave parent CCFG-26 partially open, and select no successor.

No final validation step creates or reads real Batch Execution State for this
implementation batch.

## Amended Strict Scope

The original immutable planning snapshot and its 42 implementation paths remain
the selected candidate scope. This amendment adds only two planning paths:

```yaml
planning_path_additions:
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/amendment.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/amendment-review.md
planning_path_removals: []
implementation_path_additions: []
implementation_path_removals: []
```

Plan-time amendment validation used the installed helper resolving to
`/home/alacasse/projects/codex-config/scripts/cross_checkout_context.py` and the
following live authoring observation:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: da2422b81cb9f73248cfb2a26e634bc0d2e6843e
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: da2422b81cb9f73248cfb2a26e634bc0d2e6843e
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 5c5ec9d52dd9033daa45f3a200031c152363b62c
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Helper validation result:

```yaml
interface: cross-checkout-receipt/v1
caller: plan-batch
reason: CCFG-26 fixture-only bootstrap correction amendment
planning_path_count: 7
implementation_path_count: 42
canonical_path_manifest_sha256: 4d39c96c4d12bfb76809e8b5c9693ae51eff5412cc22efa026c8466604dd6778
deletion_condition: CCFG-29 final integration
```

This authoring observation does not replace the original immutable planning
snapshot or act as a live execution lease. Before every future worker or
reviewer handoff, the stable coordinator must confirm the amended queue basis,
prepare a fresh strict lease from live facts, and validate the exact
write-bearing paths separately.

## Queue And State Binding

After a clean exact amendment review:

- `CURRENT.md` and `LEDGER.md` keep `runway.md` as the sole queued path;
- they bind `amendment.md` and `amendment-review.md` as required execution
  inputs;
- the original review is labeled historical and insufficient by itself;
- real-batch Run artifact location is `None`;
- the next safe action is a later explicit stable `work-batch` executing only
  real implementation Slice 1 through existing stable mechanisms; and
- no implementation, closeout, successor selection, or queue replacement
  occurs during this correction.

## Amendment Review Gate

The fresh independent reviewer must evaluate the complete amended plan, not
only this document's shape. At minimum it must verify:

- the real implementation batch is never self-hosted by candidate machinery;
- stable `work-batch` remains the sole real-batch controller for both Slices;
- the Slice 2 candidate tracer uses only disposable planning, implementation,
  state, receipt, and report fixtures;
- no legacy completed-prefix import or new migration event is introduced;
- no durable temporary path remains in executable planning state;
- the two failed baseline tests have explicit semantic dispositions and cannot
  pull deferred behavior into scope;
- every custom baseline has exact reproducible argv and honest status;
- the two-Slice producer/consumer code dependency remains valid without
  becoming an execution-authority dependency;
- automatic continuation and later CCFG-26 concerns remain deferred;
- CCFG-26 remains partial and no successor is selected; and
- the exact amendment SHA-256, original artifact hashes, stable/candidate
  identities, and amended strict path scope are bound in
  `amendment-review.md`.

Stop before implementation unless that exact review is clean.
