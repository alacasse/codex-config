# Runner Contract Fixtures Dispatch

```yaml
batch_id: ccfg-1-runner-contract-fixtures
status: queued
source_program_ledger: docs/plans/programs/codex-config/LEDGER.md
included_findings:
  - id: CCFG-1
    title: Contract-first runner business-logic extraction
excluded_findings:
  - id: CCFG-2
    title: Branch-per-batch runner isolation mode
    reason: Depends on the generic runner contract boundary being explicit first.
  - id: CCFG-3
    title: Contract-drift review skill
    reason: Follow-up support skill; this batch prepares the contract sources it would review.
  - id: CCFG-4
    title: Runner adapter authoring skill
    reason: Depends on the worker/runtime boundary defined by this batch.
  - id: CCFG-5
    title: Baton dogfood diagnostics
    reason: Diagnostics should read stable runner/planning artifacts after CCFG-1 clarifies them.
  - id: CCFG-6
    title: Skill-slimmer support
    reason: Separate skill-cleanup backlog, unrelated to runner extraction preparation.
  - id: CCFG-7
    title: Batch Runway hot-path pruning
    reason: Completed; closeout evidence only.
  - id: CCFG-8
    title: Ledger and dispatch rule dedupe
    reason: Separate skill-cleanup backlog.
  - id: CCFG-9
    title: Short skill frontmatter descriptions
    reason: Separate skill-cleanup backlog.
  - id: CCFG-10
    title: Skill steering vocabulary
    reason: Separate skill-cleanup backlog.
  - id: CCFG-11
    title: Skill deletion tests
    reason: Separate skill-cleanup backlog.
  - id: CCFG-12
    title: Plan-batch command-owner deepening
    reason: Completed; closeout evidence only.
goal: Prepare runner business-logic extraction with implementation-neutral contracts and validation fixtures before any code move, repository creation, repo skeleton, or extraction implementation.
owner_seam: CCFG-1 is a contract-preparation batch. It clarifies generic runner control-plane contracts, planning-state interop expectations, and codex-config facade compatibility while keeping current Python runner behavior in place.
validation_class: Contract and fixture preparation with focused runner/planning-state tests, planning-state current/validate diagnostics, and git diff checks. No integration harness or nested Codex execution is required.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - `planning_state.py current` reports this runway as the queued codex-config batch after dispatch/runway creation.
    - Planning-state interop expectations are explicit enough for later extraction tests without making `planning_state.py` an internal runner dependency.
    - Facade compatibility expectations preserve current runner CLI, direct-script, phase-result, receipt, artifact, and final-summary behavior before extraction.
source_evidence:
  - docs/plans/programs/codex-config/LEDGER.md
  - docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md#APR-26
  - docs/plans/phase-runner-business-logic-contract.md
  - docs/plans/generic-phase-runner-workflow-contract.md
  - docs/plans/phase-runner-repo-split-issue-12-plan.md
  - skills/planning-state/references/state-fixtures.md
  - skills/planning-state/references/runner-artifacts.md
required_guardrails:
  - Do not move runner code.
  - Do not create a new repository.
  - Do not create a repo skeleton.
  - Do not create package, module, or CI scaffolding.
  - Do not implement runner extraction.
  - Do not choose package/runtime basics beyond documenting what remains undecided.
  - Do not make `planning_state.py` a hidden runner-core dependency.
  - Do not move Codex prompts, Batch Runway rules, Program Ledger semantics, GitHub policy, or local planning policy into the generic runner core.
  - Do not scan archived APR/PST ledgers except for the APR-26 evidence already named by CCFG-1.
dependencies_satisfied:
  - Planning Artifact Layout v1 is active under `docs/plans/`.
  - CCFG-1 exists in the canonical codex-config ledger and points to APR-26 evidence.
  - The implementation-neutral business-logic contract artifact already exists.
  - No selected dispatch, active runway, or queued batch existed before this batch was selected.
dependencies_blocking:
  - None for contract/fixture preparation.
suggested_slices:
  - Clarify workflow/state/result/receipt/worker/artifact contract boundaries in implementation-neutral terms.
  - Define planning-state interop fixture expectations using explicit command/file/JSON/exit-code boundaries and generated-only fixture rules.
  - Define facade compatibility expectations and focused validation coverage for the existing runner facade.
  - Harden non-goals, stop conditions, and closeout criteria so later extraction cannot begin until contracts and fixtures are explicit.
closeout_gates:
  - Implementation-neutral workflow, state, result, receipt, worker, artifact, and stop-condition contracts are explicit.
  - Planning-state interop fixture expectations are command/file/schema based and do not make `planning_state.py` a runner-core dependency.
  - Facade compatibility expectations preserve current runner CLI, dry-run, direct-script, phase-result, receipt, artifact, and final-summary behavior.
  - Remaining target language, package/repository, public CLI/API, compatibility promise, and extraction-location decisions are recorded as unresolved.
  - Closeout does not claim extraction implementation, repository creation, package scaffolding, adapter implementation, or CCFG-2 through CCFG-5 completion.
stop_conditions:
  - The work requires moving code or changing runtime behavior.
  - The work creates a new repository, repo skeleton, package scaffold, Go module, or CI scaffold.
  - The work starts choosing branch isolation, adapter-authoring, or dogfood diagnostics scope from CCFG-2 through CCFG-5.
  - The work needs archived APR/PST scans beyond APR-26 evidence already named by CCFG-1.
  - The work cannot express planning-state interop without coupling the runner core to `planning_state.py` internals.
unresolved_extraction_decisions:
  - Target language/runtime and package manager.
  - Repository/module/package boundary and extraction location.
  - Public CLI/API name and compatibility promise.
  - Whether current JSON field names are public compatibility or adapter translation details.
  - Exact planning-state interop command, JSON shape, and exit-code contract.
expected_spec_path: docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md
```
