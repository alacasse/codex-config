batch_id: phase-transition-change-allowance
source_program_ledger: plans/codex-config-architecture-program-runner-findings.md
included_findings:
  - id: APR-17
    title: Phase Transition is expressed as run-loop state-key mutation
  - id: APR-18
    title: Change Allowance is still encoded as dirty-path helpers in the Runner Facade
excluded_findings:
  - id: APR-19
    reason: Phase Contract catalog work should consume the clarified Phase Environment and later transition seams but stay separate from state advancement and path allowance.
  - id: APR-20
    reason: Phase Observation attribution should wait until transition and contract ownership are clearer.
  - id: APR-21
    reason: Input Inventory contract enforcement is evidence-shape work, not run-state transition or changed-path classification.
  - id: APR-22
    reason: Planning Root and Plan Archive migration is documentation/filesystem migration work, separate from runner behavior refactoring.
goal: Give Phase Transition and Change Allowance clear concept owners while preserving Runner Facade behavior and conservative dirty-path protection.
concept_owner_seam: Introduce small concept owners for transition and allowance decisions; expected homes are scripts/architecture_program_runner_transition.py and scripts/architecture_program_runner_change_allowance.py unless current code shape shows clearer names.
validation_class: mechanical production refactor; focused run-loop/worktree/state/validation tests plus dry-run smoke; no live nested Codex required.
guardrails:
  - Preserve current CLI arguments, defaults, direct script execution, dry-run output, and final Run Summary shape.
  - Preserve phase-result validation and receipt equality in the validation concept owner.
  - Phase Transition may consume an already valid Phase Result and update Run State, but must not own schema validation, receipt reading, worktree checks, phase launch, or Phase Observation writing.
  - Change Allowance may classify changed paths for a phase, but must not weaken rejection of unrelated project files.
  - Preserve stopped-phase evidence path allowance and execute-to-closeout post-check behavior.
  - Do not implement Phase Contract catalog, Phase Observation attribution, Input Inventory validation, or Planning Root migration in this batch.
dependencies_satisfied:
  - Phase Environment ownership is closed and supplies launch/prompt context separately from transition and allowance decisions.
  - Runner boundary split created focused state, validation, command, artifact, worktree, and run-loop tests.
  - CONTEXT.md defines Phase Transition and Change Allowance language.
dependencies_blocking:
  - None for spec creation.
suggested_slices:
  - Characterize current Phase Transition and Change Allowance behavior in focused tests before moving production ownership.
  - Introduce a Phase Transition owner for applying valid phase results, terminal-state checks, and closeout batch reset semantics.
  - Introduce a Change Allowance owner for dirty-path classification and worktree rejection.
  - Route the Runner Facade through the new owners and tighten facade compatibility tests around behavior that must not move.
stop_conditions:
  - Stop if phase-result schema validation, expected next-phase validation, or receipt equality starts moving into Phase Transition.
  - Stop if Change Allowance permits unrelated project files or drops stopped-phase evidence path allowances.
  - Stop if execute-phase post-check no longer rejects unexpected changes before closeout.
  - Stop if the refactor changes CLI flags, phase sequence, artifact paths, receipt paths, dry-run semantics, or Run Summary fields.
  - Stop if the batch starts implementing Phase Contract catalog, Phase Observation attribution, Input Inventory validation, or Planning Root migration.
  - Stop if validation requires a live nested Codex run; use focused tests and dry-run smoke.
expected_spec_path: plans/codex-config-architecture-program-runner-phase-transition-change-allowance-runway.md
