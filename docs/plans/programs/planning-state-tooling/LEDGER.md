# Planning-State Tooling Program Ledger

## Purpose

Track the planning-state tooling workstream so future agents can create concrete
Batch Runway specs without replaying the full brainstorming thread. This ledger
is planning-only; it does not implement code.

## Current Direction

- Shift active-state resolution, path allocation, artifact registration,
  cross-batch obligation tracking, and closeout validation into code.
- Keep Markdown and JSON canonical, readable, diffable, and repairable.
- Keep SQLite optional and rebuildable as a reporting projection.
- Make declared projections operationally useful for history/reporting workflows
  when project policy permits, while keeping active-state correctness independent
  of SQLite.
- Keep agents at the workflow command level; agents should not write SQL or
  mutate backing stores directly.
- Move the main user workflow surface toward command-owner skills:
  `add-to-ledger`, `plan-batch`, and `work-batch`.
- Keep generic tooling project-neutral. Project-specific paths, validation
  commands, and overlays belong in project instructions or active specs.
- Keep planning-state tooling separate from the future OSS Go runner. Interop
  belongs in explicit command/file protocols, schemas, and golden fixtures, not
  Python imports or duplicated Markdown heuristics.

## Source Context

- Decision note: `docs/plans/planning-state-tooling-plan.md`
- Planning Artifact Layout v1:
  `skills/planning-artifacts/SKILL.md`
- Command-owner skill decision:
  `docs/adr/0002-human-facing-command-owner-skills.md`
- Architecture Program Runway:
  `skills/architecture-program-runway/SKILL.md`
- First real fixture: Graphify local planning root at
  `/home/alacasse/projects/graphify/my-docs/plans/`
- Related GitHub issues: #8, #10, #12, #22
- Current runner concept owners: `scripts/architecture_program_runner*.py`

## GitHub Issue Reconciliation (2026-07-06)

Fetched open issues from `alacasse/codex-config` and reconciled them against
current repo artifacts and active program ledgers. This table records planning
state only; it does not update or close GitHub issues.

| Issue | Current repo disposition | Still to do? | Ledger action |
|---|---|---|---|
| #1. Integrate test-quality-review into batch-runway review workflow | Implemented by `skills/batch-runway/references/test-quality-review.md` and the trigger-based review path in Batch Runway references | No; closed on GitHub 2026-07-06 | No new finding |
| #2. Support full-audit mode with ADR candidate generation | Implemented in `skills/test-quality-review/SKILL.md` with full-audit additions and limits | No; closed on GitHub 2026-07-06 | No new finding |
| #3. Add finding disposition model for test-quality-review | Partially covered by compact test-quality output, but no explicit `blocking` / `fix_in_scope` / `issue_candidate` / `note_only` disposition model is present | Yes | Keep as future test-quality-review backlog |
| #4. Define workflow for issue candidates emitted by test-quality-review | Partially covered by the Batch Runway rule not to auto-create issues, but issue-candidate output is not fully specified | Yes | Keep as future test-quality-review backlog |
| #5. Expand test-quality-review design signal analysis | Implemented in `skills/test-quality-review/SKILL.md` under fixture complexity and design signals | No; closed on GitHub 2026-07-06 | No new finding |
| #7. Make batch-runway commit receipts avoid self-referential hash churn | Partially mitigated by historical `slice commit` wording, but `execution-contract-v1.md` still asks for commit hashes without the same-commit caveat | Yes | Future Batch Runway guidance fix |
| #8. Explore SQLite operational index for architecture program runner | Planning-state projection work closed the generic optional projection path; a dedicated runner-index script/report remains a distinct decision | Maybe, only if runner-specific indexing is still desired | Covered by PST-6 for generic projection; see runner program before reviving |
| #9. Batch Runway should guard prompt-obligation cleanup during test topology slices | Evidence exists in archived phase-contract anomalies, but reusable Batch Runway guidance does not yet state the protected-prompt cleanup rule | Yes | Future Batch Runway guidance fix |
| #10. Explore extracting a generic phase runner product | Generic workflow/product notes exist; extraction remains gated by APR-26 | Yes | Tracked in architecture-runner APR-26 |
| #11. Add branch-per-batch support for local architecture runner | No branch-per-batch mode found | Yes | Added to architecture-runner ledger as APR-27 |
| #12. Evaluate early repo split for phase-runner dogfooding | Decision note says split is premature until contract-first extraction evidence improves | Yes, reassess after APR-26 | Tracked in architecture-runner APR-26 |
| #13. Add a port-by-contract skill for implementation-neutral rewrites | Implemented under `skills/port-by-contract/` with manifest/changelog evidence | No; closed on GitHub 2026-07-06 | No new finding |
| #14. Add contract-drift-review skill | Skill does not exist | Yes | Added to architecture-runner ledger as APR-28 |
| #15. Add skill-slimmer skill | Skill does not exist | Yes | Keep as future skill-cleanup backlog |
| #16. Add runner-adapter-authoring skill | Worker adapter seam exists, but the requested authoring skill does not | Yes | Added to architecture-runner ledger as APR-29 |
| #17. Add baton-context-map CLI | CLI does not exist | Yes | Added to architecture-runner ledger as APR-30 |
| #18. Add baton-doctor CLI | CLI does not exist | Yes | Added to architecture-runner ledger as APR-30 |
| #19. Add baton-receipt-inspector CLI | CLI does not exist | Yes | Added to architecture-runner ledger as APR-30 |
| #20. Add trigger-based specialized review routing for Batch Runway | Implemented by `agents/import_topology_reviewer.toml`, `agents/runway_reviewer.toml`, and Batch Runway review routing docs | No; closed on GitHub 2026-07-06 | No new finding |
| #21. Define generic planning artifact layout and naming conventions | Implemented by Planning Artifact Layout v1 and closed PST-21 adoption guidance | No; closed on GitHub 2026-07-06 | Covered by closed PST-21 |
| #22. Explore tool-owned planning state behind workflow-level commands | Implemented across PST-1 through PST-21 with `scripts/planning_state.py` and `skills/planning-state/` | No; closed on GitHub 2026-07-06 | Covered by closed PST-1..PST-21 |
| #23. Prune batch-runway hot path | `batch-runway` has been split into references, but the issue's explicit pruning pass is not evidenced as complete | Yes | Keep as future skill-cleanup backlog |
| #24. Deduplicate ledger and dispatch rules across skills | Partially addressed by `planning-artifacts`, `planning-state`, and consumer routing; a focused dedupe pass remains | Yes | Keep as future skill-cleanup backlog |
| #25. Shorten skill frontmatter descriptions | Not done consistently; some descriptions remain long and dense | Yes | Keep as future skill-cleanup backlog |
| #26. Codify leading words for each skill | No consistent steering-vocabulary sections found | Yes | Keep as future skill-cleanup backlog |
| #27. Run deletion tests for skill no-ops and sediment | No focused deletion-test audit found | Yes | Keep as future skill-cleanup backlog |

## Planning Layout

- Layout version: Planning Artifact Layout v1.
- Planning root: `docs/plans/`
- Program root: `docs/plans/programs/planning-state-tooling/`
- Program ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Program current state: `docs/plans/programs/planning-state-tooling/CURRENT.md`
- Program archive root: `docs/plans/archive/`
- Run artifact root: not selected for this planning-only ledger.
- Output root: not selected for this planning-only ledger.
- Active closeout batch directory: `None`
- Queued batch directory: `None`
- Latest completed batch directory:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/`

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| PST-1. Planning state is inferred from Markdown and filenames | Closed | `planning-state-readonly-core` | Use read-only diagnostics before broad planning tree scans | Slice 3 evidence is clean for `current` and `validate` against codex-config and Graphify planning roots. The implemented commands report active root/program `CURRENT.md` state and stale-context warnings without writes or SQLite. |
| PST-2. Batch/artifact paths are manually allocated by agents | Closed | `planning-state-write-transitions` | Use allocation and registration commands for future batch setup | Depends on PST-1 state discovery. Slice 2 added canonical path allocation and explicit artifact registration. |
| PST-3. Cross-batch obligations are not first-class state | Closed | `planning-state-write-transitions` | Feed explicit obligations into future closeout contracts | Enables fourth-batch cleanup without archaeology. Slice 4 added obligation records and validation. |
| PST-4. Batch closeout lacks a bounded evidence-index contract | Closed | `planning-state-closeout-contract` | Require bounded pointer-first closeout evidence before batch closure | Closed by closeout contract, validation, rendering, and handoff docs. Completed-batch closeout must point to validation, review, completed-slices, commits, obligations, receipts when present, and cleanup residue evidence instead of embedding logs. |
| PST-5. Existing planning roots need migration without losing human readability | Closed | `planning-state-migration-pilot` | Use bootstrap and migrated-fixture validation before any future runner/reporting layer consumes planning state | Closed by the migration-pilot closeout. `bootstrap-state` generates companion v1 JSON state from Layout v1 Markdown, preserves active-first pickup, registers co-located artifacts, and keeps Markdown as human-readable coordination state. `current`/`validate --state-file` reject drift, malformed obligations, artifact collisions, and unregistered active pointers. |
| PST-6. Operational queries are awkward from files alone | Closed | `planning-state-sqlite-projection` | Use `rebuild-projection` and `report-projection` for bounded operational reports when a caller provides a policy-compatible database target | Closed by optional SQLite projection rebuild, report commands, runner-artifact report coverage, validation, review, and pointer-first closeout evidence. SQLite is delete-safe and remains behind command/report interfaces. |
| PST-7. Runner interoperability protocol is undefined | Closed | `planning-state-write-transitions` | Use command/file outputs as the runner boundary | Depends on PST-1 and informed PST-2/PST-3. Slice 1 defined JSON facts, Slice 3 added transition receipts, and Slice 4 added obligation facts without runner imports of planning-state internals. |
| PST-8. Project planning-state ownership policy is implicit | Closed | `planning-state-project-policy` | Use resolved project policy for durable state/projection writes and SQLite work | Closed with validation, review, and closeout evidence. codex-config committed planning docs and ignored-local overlay examples are documented without becoming universal defaults; write-target preflights reject policy-incompatible durable JSON or SQLite outputs. |
| PST-9. Planning-state operations have no reusable skill interface | Closed | `planning-state-skill-interface` | Use the repo-owned `planning-state` skill before wiring consumers | Closed by the `planning-state` skill entrypoint, install metadata, validation, review, and pointer-first closeout evidence. Fresh agents now have a compact routine interface for discovery, validation, optional state bootstrap, optional projection rebuild/reporting, and closeout evidence. |
| PST-10. Planning-state operational details are split between layout guidance and historical plan prose | Closed | `planning-state-skill-interface` | Use progressive skill references for optional state/projection/closeout details | Closed by the entrypoint plus focused references for state fixtures, target policy, projection reporting, closeout evidence, and runner artifacts. `planning-artifacts` remains the Layout v1 placement owner. |
| PST-11. Project policy target selection is not packaged as an agent-facing adapter | Closed | `planning-state-skill-interface` | Resolve or refuse state/projection targets through the planning-state skill | Closed by target-policy guidance covering stdout, `/tmp`, generated-only, committed, ignored-local, external, and none policies without embedding project-specific paths as generic defaults. |
| PST-12. Ledger-dependent skills duplicate active-state pickup and projection setup | Closed | `planning-state-consumer-integration` | Use the shared planning-state diagnostic interface before consumer-owned decisions | Closed by slices 1-3: `batch-runway`, `architecture-program-runway`, and `legacy-removal` now consume compact Planning State Diagnostic facts before Layout v1 pickup while preserving their own semantic decisions. |
| PST-13. Feature dependency metadata cannot express operational planning-state reuse | Closed | `planning-state-consumer-integration` | Install `planning-state` before consumers that invoke it | Closed by slice 4: `codex-features.json` keeps `planning-artifacts` and adds `planning-state` dependencies for the rewired consumers, with manifest tests covering expansion order and no cycle. |
| PST-14. Projection routing is implemented but not part of the routine interface | Closed | `planning-state-projection-routing` | Use projection-aware Planning State Diagnostic facts for history/reporting questions before broad historical scans when policy permits | Closed by the projection-routing batch. The `planning-state` skill now routes history/reporting questions through policy-compatible projection reports, while `current` and `validate` remain SQLite-independent active-state checks. |
| PST-15. Projection target policy does not express expected projection usage | Closed | `planning-state-projection-routing` | Use explicit `projection_usage` and `projection_rebuild_authority` policy before rebuilding or reporting projections | Closed by the projection-routing batch. Project policy now distinguishes allowed projection targets from expected projection usage and rebuild authority without introducing downstream project paths or durable default databases. |
| PST-16. Consumer skills consume active-state diagnostics but not projection reports | Closed | `planning-state-projection-consumers` | Use projection-report routing in Batch Runway, Architecture Program Runway, and Legacy Removal for supported history/reporting questions | Closed by the projection-consumers batch. Batch Runway, Architecture Program Runway, and Legacy Removal now route supported history/reporting questions through policy-compatible projection reports before broad historical scans while preserving consumer-owned decisions. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/closeout.md`. |
| PST-17. Tests protect projection commands but not workflow obligations | Closed | `planning-state-projection-consumers` | Keep focused consumer-obligation tests aligned with workflow-skill behavior changes | Closed by `tests/test_planning_state_consumer_projection_routing.py`, manifest checks, final validation, and clean review. The regression surface protects the consumer-facing projection-report routing obligation and dependency assumptions. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/closeout.md`. |
| PST-18. Batch Runway create-spec writes session-local mode into durable overrides | Closed | `batch-runway-create-spec-output-contract` | Use the closed batch closeout as the durable evidence pointer | Closed by Batch Runway create-spec guidance, focused regression coverage, bounded active/future runway scan evidence, and pointer-first closeout. Remaining scan matches are closed historical runway specs intentionally retained as evidence, not active/future artifacts or reusable guidance. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/closeout.md`. |
| PST-19. Findings lack a Pending status for cut or active batch work | Closed | `planning-state-finding-pending-status` | Use the closed batch closeout as the durable evidence pointer | Closed by reusable Architecture Program Runway `Pending` vocabulary, Pending source-scope update rules, focused status-vocabulary tests, manifest validation, final planning-state diagnostics, clean review, and pointer-first closeout evidence. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/closeout.md`. |
| PST-20. Agent-facing SQLite language still makes normal projection reporting sound optional | Closed | `planning-state-projection-language-and-migration` | Use the closed batch closeout as the durable evidence pointer | Closed by workflow-skill language that describes projection-backed reporting as the policy-gated normal route for supported history/reporting questions while preserving SQLite-independent active-state pickup, canonical Markdown/JSON, command/report-only access, and no generic durable database default. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/closeout.md`. |
| PST-21. Existing ledger workflows need a reusable projection-reporting adoption migration | Closed | `planning-state-projection-language-and-migration` | Use the closed batch closeout as the durable evidence pointer | Closed by reusable Layout v1 adoption guidance covering root/program `CURRENT.md` files, ledgers, batch queues, redirect ledgers, consumer skills, installed-skill state, generated-only temp targets, ignored-local declared projection paths, downstream overlays, and fixture proof without hard-coding downstream project paths into generic skills. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/closeout.md`. |
| PST-22. Workflow skills repeat the planning pickup interface | Closed | `workflow-skill-interface-deepening` | Use the closed batch closeout as the durable evidence pointer | Closed by consumer skill guidance that routes Layout v1 pickup through Planning State Diagnostic-First Pickup while preserving consumer-owned semantic decisions. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/closeout.md`. |
| PST-23. Layout placement and operational pickup share a fuzzy seam | Closed | `workflow-skill-interface-deepening` | Use the closed batch closeout as the durable evidence pointer | Closed by Planning Artifacts/Planning State guidance that keeps placement, naming, file shape, archives, and roots separate from operational pickup, validation, target-policy checks, and projection routing. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/closeout.md`. |
| PST-24. Program ledger updates and concrete runway ledger updates are easy to conflate | Closed | `workflow-skill-interface-deepening` | Use the closed batch closeout as the durable evidence pointer | Closed by Architecture Program Runway and Batch Runway handoff guidance that separates program findings, selected dispatch, queue state, and closeout reconciliation from concrete runway ledgers, validation/review routing, commits, and completed-slice archives. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/closeout.md`. |
| PST-25. Specialized discovery skills can become parallel planning systems | Closed | `workflow-skill-interface-deepening` | Use the closed batch closeout as the durable evidence pointer | Closed by Legacy Removal role guidance and Dead Surface Audit evidence-only guidance: discovery skills can produce evidence and dispatch handoff material without creating program queue or selected-batch state by default. Closeout evidence: `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/closeout.md`. |
| PST-26. Human-facing workflow commands are hidden behind opaque runtime skill names | Closed | `command-owner-skill-migration` | Use `add-to-ledger`, `plan-batch`, `work-batch`, and `port-by-contract` as the direct command set | Closed by installed command-owner skills with stop conditions, manifest metadata, README catalog roles, validation, and closeout evidence. Closeout: `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`. |
| PST-27. In-place renaming would disrupt active workflow skills | Closed | `command-owner-skill-migration` | Keep old runtime contracts available as agent-facing support behind command owners | Closed by command-owner migration that preserves `architecture-program-runway`, `batch-runway`, `legacy-removal`, and `dead-surface-audit` as support dependencies while demoting their metadata and UI prompts away from direct command recommendations. Closeout: `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`. |
| PST-28. Command-owner skills need narrow support-skill boundaries | Closed | `command-owner-skill-migration` | Keep support skills narrow and agent-facing behind command owners | Closed by support-boundary wording and focused regression checks for planning, review, evidence, and validation lenses. Closeout: `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`. |
| PST-29. Legacy and test-quality concerns need agent-facing placement | Closed | `command-owner-skill-migration` | Treat test-quality review as review support and preventive legacy control as a normal workflow obligation | Closed by wording and tests that keep test-quality review agent-facing support while preventing unsupported legacy preservation during implementation/review instead of advertising a normal cleanup command. Closeout: `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`. |

## Batch Queue

| Batch | Findings | Status | Why grouped | Depends on | Validation class | Dispatch | Spec |
|---|---|---|---|---|---|---|---|
| planning-state-readonly-core | PST-1 | Completed | Establishes active-state precedence, stale-context warnings, and the safe tool boundary before any state writes | None | Focused Python unit tests and dry-run CLI checks against codex-config fixtures and the Graphify planning-root fixture | `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/runway.md` |
| planning-state-write-transitions | PST-2, PST-3, PST-7 | Completed | Moves allocation, registration, selection, obligations, and runner-facing interop facts into commands | planning-state-readonly-core | Focused state/CLI tests, interop fixture tests, and Markdown round-trip checks | `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/runway.md` |
| planning-state-closeout-contract | PST-4 | Completed | Makes completed-batch evidence bounded and validateable | planning-state-write-transitions | Focused rendering/validation tests plus current/validate diagnostics | `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/runway.md` |
| planning-state-migration-pilot | PST-5 | Completed | Bootstraps tool state from existing planning roots without hiding Markdown | planning-state-readonly-core; preferably planning-state-closeout-contract | Fixture migration tests, current/validate diagnostics, review, and closeout evidence | `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/runway.md` |
| planning-state-project-policy | PST-8 | Completed | Makes state-file and projection ownership explicit per project before SQLite chooses targets | planning-state-migration-pilot | Project-policy parsing/validation tests, temp committed and ignored-local fixtures, current/validate diagnostics, and closeout evidence | `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/runway.md` |
| planning-state-sqlite-projection | PST-6 | Completed | Adds fast operational reporting after canonical files and project policy are stable while keeping SQLite optional and rebuildable | planning-state-project-policy closed by `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/closeout.md` | SQLite rebuild/report tests, report CLI checks, current/validate diagnostics, review, and closeout evidence | `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/runway.md` |
| planning-state-skill-interface | PST-9, PST-10, PST-11 | Completed | Creates the deep skill interface that centralizes planning-state operations before consumers depend on it | planning-state-sqlite-projection | Skill validation, current/validate CLI smoke, generated-only `/tmp` state/projection smoke, manifest/changelog alignment, and grep checks for project-specific hard-coding | `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/runway.md` |
| planning-state-consumer-integration | PST-12, PST-13 | Completed | Wires ledger-dependent skills and install metadata to the shared planning-state skill after the interface exists | planning-state-skill-interface | Skill validation, dependency-manifest JSON check, focused wording checks across consumer skills, current/validate diagnostics, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/runway.md` |
| planning-state-projection-routing | PST-14, PST-15 | Completed | Deepens the Planning State Diagnostic interface so declared projections become useful for history/reporting without becoming canonical active state | planning-state-consumer-integration | Skill/reference tests, project-policy parsing checks, current/validate/projection smoke tests against generated-only and ignored-local fixtures, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/runway.md` |
| planning-state-projection-consumers | PST-16, PST-17 | Completed | Wires consumer skills and regression checks so projection reports are tried before broad historical scans when policy permits | planning-state-projection-routing | Skill wording tests, manifest/dependency checks, focused grep checks across consumer skills, current/validate diagnostics, review evidence, closeout evidence, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/runway.md` |
| batch-runway-create-spec-output-contract | PST-18 | Completed | Keeps session-local create-spec history out of durable Batch Runway execution contracts | planning-state-projection-consumers closed, unless explicitly amended into the active runway | Batch Runway skill/reference wording tests, regression check for durable `Overrides`, focused grep across active templates/specs, current/validate diagnostics, closeout evidence, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/runway.md` |
| planning-state-finding-pending-status | PST-19 | Completed | Makes cut-but-not-closed finding state explicit so source ledgers stop being edited as raw intake once a dispatch/runway exists | `batch-runway-create-spec-output-contract` closed PST-18; baseline `current` and `validate` diagnostics pass | Workflow-skill wording tests, ledger/template status-vocabulary checks, current/validate diagnostics, manifest/changelog alignment, clean review, closeout evidence, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/runway.md`; closeout: `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/closeout.md`; completed slices: `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/completed-slices.md` |
| planning-state-projection-language-and-migration | PST-20, PST-21 | Completed | Pair the wording fix with the reusable adoption migration because the ambiguity and the migration gap reinforce each other | planning-state-projection-consumers and planning-state-finding-pending-status closed; baseline `current` and `validate` diagnostics pass | Skill wording tests, consumer-skill obligation tests, project-policy fixture tests for generated-only and ignored-local projection routing, migration checklist/readback validation against codex-config plus a non-codex-config Layout v1 root shape, installed-skill ownership check, changelog/manifest alignment, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/runway.md`; closeout: `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/closeout.md`; completed slices: `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/completed-slices.md` |
| workflow-skill-interface-deepening | PST-22, PST-23, PST-24, PST-25 | Completed | Deepens the workflow-skill seams so agents have one pickup Interface and do not confuse layout, planning-state diagnostics, program selection, batch execution, or specialized evidence classification | `planning-state-projection-language-and-migration` closed; baseline `current` and `validate` diagnostics pass | Skill wording tests proving one pickup owner, consumer-owned semantic decisions, explicit program-vs-runway ledger handoff, discovery role boundaries, current/validate diagnostics, manifest/changelog alignment, closeout evidence, and `git diff --check` | `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/runway.md`; closeout: `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/closeout.md`; completed slices: `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/completed-slices.md` |
| command-owner-skill-migration | PST-26, PST-27, PST-28, PST-29 | Completed | Introduces the accepted human-facing command-owner skill surface while keeping the migration copy-first and support skills narrow | `workflow-skill-interface-deepening` closed; ADR 0002 accepted; baseline `current` and `validate` diagnostics pass | Skill validation, manifest/dependency checks, focused wording tests, planning-state current/validate diagnostics, `git diff --check`, and pointer-first closeout evidence | `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/dispatch.md` | `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/runway.md`; closeout: `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`; completed slices: `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/completed-slices.md` |

## Queued Batch Brief

Queued batch: `None`.

- Status: no successor planning-state-tooling batch is selected.
- Notes: select a successor only when explicitly requested.

## Latest Batch Brief

Latest completed batch:

- Batch: `command-owner-skill-migration`
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/dispatch.md`
- Status: `Completed`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/completed-slices.md`
- Covers: PST-26, PST-27, PST-28, and PST-29.
- Goal: add the accepted user-facing command-owner skills through copy-first
  migration while keeping support skills narrow and agent-facing.
- Notes: PST-26 through PST-29 are closed with command-owner skills, support
  boundary wording, README/catalog and manifest alignment, validation, and
  closeout pointers.

Previous completed batch:

- Batch: `workflow-skill-interface-deepening`
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/dispatch.md`
- Status: `Completed`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/completed-slices.md`
- Covers: PST-22, PST-23, PST-24, and PST-25.
- Goal: deepen reusable workflow-skill seams so agents have one pickup
  Interface, one placement owner, explicit program-vs-runway ledger ownership,
  and clear specialized-discovery skill roles.
- Notes: PST-22 through PST-25 are closed with workflow wording tests,
  metadata alignment, validation, clean review evidence for implementation
  slices, and closeout pointers.

Previous completed batch:

- Batch: `planning-state-projection-language-and-migration`
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/dispatch.md`
- Status: `Completed`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/completed-slices.md`
- Covers: PST-20 and PST-21.
- Goal: make projection-backed reporting read as the policy-gated normal route
  for supported history/reporting questions and document reusable Layout v1
  adoption guidance.
- Notes: PST-20 and PST-21 are closed with workflow wording tests, portable
  fixture coverage, metadata alignment, validation, clean review evidence for
  implementation slices, and closeout pointers.

Previous completed batch:

- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/completed-slices.md`
- Covers: PST-19.
- Goal: define and enforce a Pending finding lifecycle status for cut or active
  batch work.
- Notes: PST-19 is closed with vocabulary, source-scope update guidance,
  regression tests, metadata evidence, validation, review, and closeout
  pointers.

Earlier completed batch:

- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/completed-slices.md`
- Covers: PST-18.
- Goal: keep session-local create-spec history out of durable Batch Runway
  execution `Overrides`.
- Notes: PST-18 is closed with final validation pointers, bounded scan evidence,
  and pointer-first closeout evidence.

Earlier completed batch:

- Batch: `planning-state-projection-consumers`
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/dispatch.md`
- Status: `Completed`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/closeout.md`
- Notes: PST-16 and PST-17 are closed. Consumer projection-report routing,
  manifest alignment, final validation, clean review, and closeout evidence are
  complete.

## Recommended Work Order

1. No successor planning-state-tooling batch is selected.
2. Select a successor only when explicitly requested.
3. Start future pickup from `docs/plans/CURRENT.md`, then this program
   `CURRENT.md`, before reading historical ledgers or archived batches.
4. For projection reporting, rebuild only to explicit temp or
   policy-compatible database targets and keep Markdown/JSON canonical.

## Closeout Rules

- Mark PST-1 `Closed` only after `current` and `validate` work against Graphify
  root/program `CURRENT.md` fixtures, Graphify redirect/stale-note fixtures, and
  codex-config `docs/plans/` root/program `CURRENT.md` plus redirect examples
  without mutating tracked files.
- Mark PST-2 `Closed` only after agents can register dispatch, runway, closeout,
  receipt, and output paths through commands instead of hand-allocating them.
- Mark PST-3 `Closed` only after open obligations have IDs, owners, close
  conditions, and validation that prevents silent loss.
- Mark PST-4 `Closed` only after completed batches require a bounded
  pointer-first `closeout.md` or an explicit documented exception.
- Mark PST-5 `Closed` only after migration can bootstrap state from existing
  Markdown while preserving human-readable artifacts and redirects, and after
  the migration-pilot batch has validation, review, and closeout evidence.
- Mark PST-6 `Closed` only after SQLite can be deleted and rebuilt from
  canonical artifacts and resolved project policy, with agents still using
  command/report interfaces.
- Mark PST-7 `Closed` only after planning-state facts have an explicit
  command/file protocol with JSON shape, warning/error shape, exit-code meaning,
  and golden fixtures that a future Go runner can consume without scraping
  Markdown heuristics.
- Mark PST-8 `Closed` only after project policy can represent committed,
  ignored-local, external, generated-only, and no durable state/projection
  layouts without hard-coding a downstream project path, and after write-target
  preflights reject policy-incompatible durable JSON or SQLite outputs.
- Mark PST-9 `Closed` only after a repo-owned `planning-state` skill gives
  fresh agents a compact interface for discovery, validation, optional
  state-fixture bootstrapping, optional SQLite projection rebuild, and
  projection reporting.
- Mark PST-10 `Closed` only after the planning-state skill uses progressive
  discovery: the entrypoint covers the routine hot path, and references cover
  state fixtures, projection reporting, runner artifacts, closeout, and
  target-policy details only when needed.
- Mark PST-11 `Closed` only after the skill tells agents how to resolve or
  refuse state/projection targets from project policy without embedding
  project-specific paths as generic defaults.
- Mark PST-12 `Closed` only after the ledger-dependent consumer skills use the
  shared planning-state interface before making their own semantic decisions.
- Mark PST-13 `Closed` only after feature metadata installs the new skill and
  declares consumer dependencies that distinguish layout convention from
  operational planning-state diagnostics.
- Mark PST-14 `Closed` only after the `planning-state` skill gives agents an
  explicit projection-aware routing rule for history/reporting questions, while
  preserving `current` and `validate` as SQLite-independent active-state checks.
- Mark PST-15 `Closed` only after project policy distinguishes allowed
  projection targets from expected projection usage and rebuild authority without
  hard-coding a downstream project path.
- Mark PST-16 `Closed` only after Batch Runway, Architecture Program Runway, and
  Legacy Removal try projection reports for supported history/reporting
  questions before broad historical scans when project policy permits.
- Mark PST-17 `Closed` only after regression checks protect the consumer-facing
  projection-report routing obligation, not just the underlying
  `rebuild-projection` and `report-projection` command behavior.
- Mark PST-18 `Closed` only after Batch Runway create-spec guidance prevents
  session-local mode claims from being written as durable runway `Overrides`,
  focused regression coverage protects that write-side invariant, and affected
  active/future runway artifacts are patched deliberately rather than through a
  source-ledger scope edit.
- Mark PST-19 `Closed` only after the findings ledger vocabulary defines
  `Pending` for cut or active batch work, future batch selection/update guidance
  tells agents not to mutate Pending finding scope except through an explicit
  batch amendment or follow-up item, and validation or docs-as-code checks cover
  the status transition if the tooling consumes finding status.
- Mark PST-20 `Closed` only after agent-facing wording consistently describes
  projection-backed reporting as policy-gated normal workflow for supported
  history/reporting questions, while explicitly preserving SQLite-independent
  active-state pickup, canonical Markdown/JSON, command/report-only access, and
  no generic durable database default.
- Mark PST-21 `Closed` only after a documented migration/adoption checklist
  is reusable for any project already using the current ledger/batching setup
  and covers root/program `CURRENT.md` files, program ledgers, batch queues,
  redirect ledgers, consumer skills, installed-skill state, generated-only temp
  projection targets, ignored-local projection targets, downstream project
  overlays, and fixture/dry-run evidence for at least one non-codex-config
  Layout v1 root shape without hard-coding downstream project paths into generic
  skills.
- Mark PST-22 `Closed` only after consumer skills no longer duplicate the
  planning pickup algorithm beyond invoking `planning-state` and naming the
  compact facts they consume.
- Mark PST-23 `Closed` only after `planning-artifacts` clearly owns placement
  and shape while operational pickup order is delegated to `planning-state`.
- Mark PST-24 `Closed` only after `architecture-program-runway` and
  `batch-runway` distinguish Program Ledger updates from concrete runway/spec
  execution ledger updates with a testable handoff or docs-as-code check.
- Mark PST-25 `Closed` only after specialized discovery skills state whether
  they are evidence producers, selected program owners, or dispatch handoff
  sources, and stop short of becoming parallel planning systems by default.
- Mark PST-26 `Closed` only after `add-to-ledger`, `plan-batch`, and
  `work-batch` are installed command-owner skills with clear direct-user
  ownership and stop conditions.
- Mark PST-27 `Closed` only after the migration proves the new command-owner
  surface beside existing runtime skills without removing, renaming, or
  depending on permanent wrapper compatibility as the target architecture.
- Mark PST-28 `Closed` only after support skills behind command owners have
  narrow reusable jobs and tests or wording checks prevent vague historical
  mega-skills from becoming hidden permanent owners.
- Mark PST-29 `Closed` only after test-quality review is positioned as
  agent-facing review support and preventive legacy control is enforced as a
  normal workflow obligation rather than a user-facing cleanup command.

## Planning Rules

- Create one concrete Batch Runway spec at a time.
- Start with read-only behavior; do not mix validation with write transitions.
- Keep this ledger compact. Put detailed design in
  `docs/plans/planning-state-tooling-plan.md` or future dispatch/spec files.
- Future agents should start with `docs/plans/CURRENT.md`, then consume this
  program's `CURRENT.md` and selected dispatch before reading full
  brainstorming history.
- Do not update GitHub issues as part of docs-only planning unless explicitly
  requested.
