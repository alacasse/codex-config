# Project Values Required

Resolve these values before creating or executing a spec:

- `planning_state_diagnostic`: compact facts from `planning-state` for
  ledger-driven work: planning root, current and validate status, active
  programs, selected dispatch, queued batch, active runway, blockers, warnings,
  and project policy.
- `planning_location`: where local runway specs belong.
- `planning_artifact_layout`: whether the project uses a flat local planning
  location or Planning Artifact Layout v1.
- `program_root`: durable workstream directory when the spec belongs to a
  long-lived program.
- `selected_batch_directory`: directory that should co-locate `dispatch.md`,
  `runway.md`, `closeout.md`, and completed-slice archives, when available.
- `program_archive_root`: where inactive planning docs for the current program
  belong.
- `run_artifact_root`: where runner-owned JSON state, receipts, manifests, and
  telemetry belong.
- `output_root`: where generated tool outputs belong.
- `validation_profiles`: named validation profiles available in this repo.
- `focused_validation_commands`: focused tests, linters, or checks.
- `integration_harness`: project-specific sandbox, integration harness, or
  end-to-end validation command.
- `harness_output`: where generated validation artifacts should be written.
- `summary_artifact`: command or file that must be read before reporting a
  harness result.
- `index_refresh`: graph, search index, generated docs, or metadata refresh
  required after edits.
- `commit_requirements`: trailers, signing, branch rules, or commit-message
  conventions.
- `dirty_file_constraints`: files or directories that are expected dirty,
  generated, ignored, or forbidden to touch.
- `cross_checkout_context`: complete `cross-checkout-context/v1` payload when
  the selected work explicitly spans separate toolchain, canonical-planning,
  and implementation roots; otherwise not applicable.
- `canonical_planning_root`: explicit planning write root paired with an
  applicable cross-checkout context. Do not infer it from cwd.

Stop instead of guessing when:

- ledger-driven work needs current planning state but the planning root cannot
  be resolved for the `planning-state` diagnostic
- the Planning State Diagnostic reports blockers that make the selected
  dispatch, queued batch, active runway, or target policy unsafe to consume
- no planning location is discoverable in `create-spec` mode
- project instructions require Planning Artifact Layout v1 but the program root
  or selected batch directory cannot be resolved for a selected batch
- a spec references a validation profile not defined by the spec, repository
  instructions, or local overlay
- a required harness command, output path, or summary artifact is named but not
  concretely specified
- focused validation targets cannot be identified safely from the slice scope
- explicitly cross-checkout work is missing its complete context payload or
  canonical planning root, or the installed helper rejects either one
- project instructions conflict and the priority order is not clear

When stopping, report the missing project value and the exact source checked.
