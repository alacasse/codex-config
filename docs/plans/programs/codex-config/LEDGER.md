# Codex Config Program Ledger

## Purpose

Track active and candidate codex-config workflow work in one canonical program
ledger. This ledger is the only active executable backlog source under
`docs/plans/` for `add-to-ledger`, `plan-batch`, and `work-batch`.

## Current Direction

- Keep repo-owned workflow skills project-neutral.
- Keep Planning Artifact Layout v1 pickup rooted at `docs/plans/CURRENT.md`.
- Keep Markdown and JSON readable, diffable, and repairable.
- Keep SQLite optional and rebuildable as a reporting projection.
- Keep all codex-config workflow and skill-cleanup work in this ledger.
- Do not create a dispatch or runway until one row is explicitly selected by
  `plan-batch`.

## Source Context

- Root current state: `docs/plans/CURRENT.md`
- Program current state: `docs/plans/programs/codex-config/CURRENT.md`
- Workflow guide: `docs/workflow-guide.md`
- Skill routing contract: `docs/skill-routing-contract.md`
- Live command-owner redesign intake:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md`
- Live CCFG-25 planning-quality amendment:
  `docs/plans/programs/codex-config/findings/ccfg-25-planning-quality-amendment.md`
- Live planning and execution carry-forward amendment:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-planning-execution-carry-forward.md`
- Live bootstrap decisions:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-bootstrap-decisions.md`
- Accepted immutable command-owner redesign snapshot:
  `https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md`
- Original pre-review design snapshot:
  `b3f31c44a1fc3287c33dd2955489f194afef66f6`
- Mutable redesign branch links are navigation only.
- Planning Artifact Layout v1: `skills/planning-artifacts/SKILL.md`
- Planning State Diagnostic: `skills/planning-state/SKILL.md`
- Archived APR ledger snapshot:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST ledger snapshot:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Closed History

Closed APR and PST history remains preserved in archive snapshots, not copied
row-by-row here.

| Historical source | Archive pointer | Active pickup status |
|---|---|---|
| APR-1 through APR-25, plus historical runner batches | `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md` | Archived evidence only |
| PST-1 through PST-30, plus historical planning-state batches | `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md` | Archived evidence only |

## Findings Ledger

| Finding | Status | Source | Area | Next action | Notes |
|---|---|---|---|---|---|
| CCFG-1. Contract-first runner business-logic extraction | Completed | APR-26 | Runner extraction | None | Closed as contract/fixture preparation only; no extraction implementation was completed. |
| CCFG-2. Branch-per-batch runner isolation mode | Open | APR-27; GitHub issue #11 | Runner workflow | Design after CCFG-1 clarifies the generic runner boundary | Preserve branch-mode parsing, deterministic naming, state/receipt metadata, and closeout commit-range evidence. |
| CCFG-3. Contract-drift review skill | Open | APR-28; GitHub issue #14 | Runner support skill | Create only when extraction work starts to drift | Compare extraction changes against accepted contracts without duplicating them. |
| CCFG-4. Runner adapter authoring skill | Open | APR-29; GitHub issue #16 | Runner support skill | Create after generic worker/runtime boundary is stable | Keep provider quirks out of generic runner core. |
| CCFG-5. Baton dogfood diagnostics | Open | APR-30; GitHub issues #17, #18, #19 | Runner diagnostics | Sequence after CCFG-1 unless blocking | Diagnostics read durable artifacts rather than chat transcripts. |
| CCFG-6. Skill-slimmer support | Backlog | PST issue reconciliation #15 | Skill cleanup | Decide whether to add bounded workflow | No existing skill was found. |
| CCFG-7. Batch Runway hot-path pruning | Completed | PST issue reconciliation #23 | Skill cleanup | None | Closed with compact read path and unchanged runtime semantics. |
| CCFG-8. Ledger and dispatch rule dedupe | Completed | PST issue reconciliation #24 | Skill cleanup | None | Closed with owner map and prose dedupe; runtime unchanged. |
| CCFG-9. Short skill frontmatter descriptions | Backlog | PST issue reconciliation #25 | Skill cleanup | Shorten descriptions without losing trigger accuracy | Not consistently done. |
| CCFG-10. Skill steering vocabulary | Backlog | PST issue reconciliation #26 | Skill cleanup | Codify only where useful | No consistent vocabulary exists. |
| CCFG-11. Skill deletion tests | Open | PST issue reconciliation #27 | Skill cleanup | Future explicit `plan-batch` may regenerate, split, block, or narrow only after applying CCFG-13 through CCFG-16 guards | The displaced runway is superseded planning evidence, not executable active state. |
| CCFG-12. Plan-batch command-owner deepening | Completed | `docs/plans/programs/codex-config/notes/command-owner-deepening-review.md` | Skill cleanup | None | Closed as human-facing contract deepening while broad runtime owners remained. |
| CCFG-13. Validation command status classification | Completed | GitHub issue #29 | Batch Runway create-spec | None | Closed with validation status guidance and tests. |
| CCFG-14. Batch kind and destructive-slice risk gates | Completed | GitHub issue #30 | Batch Runway create-spec | None | Closed with batch kind, risk classes, and approval gates. |
| CCFG-15. Vague ledger row splitting before runway expansion | Completed | GitHub issue #33 | Planning guard | None | Closed with split, block, or narrow guard. |
| CCFG-16. Deletion-test vocabulary ownership | Completed | GitHub issue #31 | Skill cleanup | None | Closed with canonical evidence vocabulary ownership. |
| CCFG-17. Absolute runway reference paths | Completed | GitHub issue #32 | Batch Runway create-spec | None | Closed with repo-relative reusable references and active-artifact guard. |
| CCFG-18. Establish Stable and Candidate Generations | Closed | [COR-001](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-001--ccfg-18--establish-stable-and-candidate-generations) plus live pre-creation amendment in `findings/command-owner-redesign-implementation-intake.md` | Command-owner redesign / control-plane isolation | None | Closed by `batches/ccfg-18-candidate-generation/closeout.md`: authoritative and accepted-design lineage, strict transition, isolated candidate installation, fixture-only operation, canonical-write rejection, quiescence, and unchanged-default stable rollback are proven. CCFG-19 remains unselected. |
| CCFG-19. Verify Source Contracts and Resolve Blocking Decisions | Closed | [COR-002](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-002--ccfg-19--verify-source-contracts-and-resolve-blocking-decisions) | Command-owner redesign / contracts | None | Closed by `batches/ccfg-19-source-contract-decisions/closeout.md`: all 31 contracts are joined, all seven acceptance keys are evidenced, DEC-036/037/017/038 are accepted, and OPEN-003 is resolved. CCFG-20 closed separately; CCFG-21 through CCFG-29 remain unselected. |
| CCFG-20. Implement `skill-contract/v1` Schema and Validators | Closed | [COR-003](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-003--ccfg-20--implement-skill-contractv1-schema-and-validators) | Command-owner redesign / skill contracts | None | Closed by `batches/ccfg-20-skill-contract-schema/closeout.md`: all five COR-003 keys are green in candidate range `13d7f63..3e54155`; current skills, manifest registration, installation, and CCFG-21+ remain excluded. |
| CCFG-21. Implement Planning Artifact Schemas and Validators | Closed | [COR-004](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-004--ccfg-21--implement-planning-artifact-schemas-and-validators) | Command-owner redesign / planning contracts | None | Closed by `batches/ccfg-21-planning-artifact-contracts/closeout.md`: all six COR-004 keys, detailed migration gates, 13 fault checkpoints, and exact-range review are green in candidate range `3e54155..596fc7e`; live planning migration and CCFG-22+ remain excluded. |
| CCFG-22. Finalize and Validate `skill-authoring` v1 | Closed | [COR-005](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-005--ccfg-22--finalize-and-validate-skill-authoring-v1) | Command-owner redesign / authoring | None | Closed by `batches/ccfg-22-skill-authoring-v1/closeout.md`: all nine COR-005 keys and aggregate migration gates are green in candidate range `596fc7e..2f39950`; candidate-only installation is proven, command owners remain dependency-free, and CCFG-23+ remain excluded. |
| CCFG-23. Build the Topology-Independent Behavioral Scenario Harness | Closed | [COR-006](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-006--ccfg-23--build-the-topology-independent-behavioral-harness) plus live harness scenarios in `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / behavioral harness | None | Closed by `batches/ccfg-23-behavioral-scenario-harness/closeout.md`: all six COR-006 keys and six aliases are green across 69 observed scenarios, 31 immutable contracts, and 17 required families in candidate range `2f39950..e8d07a7`; production ownership transfer, real cutover, installed-feature changes, and bridge deletion remain excluded. |
| CCFG-24. Transfer Intake Ownership to `add-to-ledger` | Open | [COR-007](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-007--ccfg-24--transfer-intake-ownership-to-add-to-ledger) | Command-owner redesign / intake ownership | Wait for CCFG-33 | Transfer intake and ledger-mutation semantics; remove APR intake, the legacy-removal escape hatch, and replaced CCFG-23 intake adapters/tests in the same work. Coordinate migration of `test_executable_work_source_boundary_is_explicit` with CCFG-25 rather than deleting it in CCFG-33. Unselected. |
| CCFG-25. Transfer Planning Ownership to `plan-batch` | Open | [COR-008](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-008--ccfg-25--transfer-planning-ownership-to-plan-batch), `findings/ccfg-25-planning-quality-amendment.md`, and `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / planning ownership | Wait for CCFG-24; consume completed CCFG-21 planning contracts and transaction owner | Implement #51, #52, and #54 semantics through the only queue mutator, direct independent planner/reviewer orchestration, proportionality evidence, semantic slice boundaries, and non-executable blocked drafts; remove APR planning, Batch Runway create-spec ownership, and replaced CCFG-23 fixture planning logic/tests in the same work. Migrate or delete `test_executable_work_source_boundary_is_explicit` and `test_plan_batch_command_owner_runtime_boundaries_are_explicit` only when the real owner supplies the named behavior. Unselected. |
| CCFG-26. Transfer Execution and Closeout Ownership to `work-batch` | Open | [COR-009](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-009--ccfg-26--transfer-execution-and-closeout-ownership-to-work-batch) plus live execution boundary in `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / execution ownership | Wait for CCFG-25 | Make Planning State the sole semantic currentness gate and Git material-integrity evidence only; transfer all execution/closeout decisions; remove APR/Batch Runway ownership and duplicate CCFG-23 worker/validator/reviewer/committer/recovery/closeout fixtures and tests in the same work. Migrate or delete `test_work_batch_reconciles_same_batch_closeout` only when the real `work-batch` owner supplies the observable closeout behavior. Unselected. |
| CCFG-27. Prepare and Rehearse Candidate Cutover | Open | [COR-010](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-010--ccfg-27--prepare-and-rehearse-candidate-cutover) plus live bridge-readiness gate in `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / cutover preparation | Wait for CCFG-26 | Prove candidate-installed temporary bridge parity and replace synthetic CCFG-23 readiness/cutover paths where real candidate behavior becomes authoritative; retain only fixtures that still prove a named fault boundary. Master remains canonical planning authority. Unselected. |
| CCFG-28. Remove Legacy Owners and Commit Final Cutover | Open | [COR-011](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-011--ccfg-28--remove-legacy-owners-and-commit-final-cutover) plus live switch gate in `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / deletion and final switch | Wait for CCFG-27 bridge parity and rehearsal proof | Delete legacy owners, prove and commit the clean switch, and delete CCFG-23 cutover fixtures superseded by real behavior or reduce them to named fault boundaries. Close under the pinned stable controller and stop. Unselected; distinct from CCFG-11. |
| CCFG-29. Contract-First Convergence and Final Integration | Open | [COR-012](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-012--ccfg-29--contract-first-convergence-and-final-integration) plus live convergence obligations in `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / convergence and final integration | Wait for CCFG-28 | Merge candidate into latest authoritative master, preserve target behavior, delete the complete temporary bridge and every remaining CCFG-23 migration-retention adapter/model/wrapper/test, then rebind default Codex home to master. Unselected. |
| CCFG-30. Separate Planning Snapshots from Live Execution Leases | Closed | `notes/cross-flight-execution-baseline-plan.md`; `batches/ccfg-30-cross-flight-execution-leases/dispatch.md` | Batch Runway / cross-checkout execution lifecycle | None | Closed by `batches/ccfg-30-cross-flight-execution-leases/closeout.md`: all ten regression scenarios, exact live-lease validation, joined lifecycle proof, linked-state checks, and clean exact-range review are green. No successor was selected. |
| CCFG-31. Narrow ready/blocked live-lease preflight | Closed | GitHub issue #53; `findings/github-issue-53-narrow-live-lease-preflight.md` | Batch Runway / cross-checkout execution lifecycle | None | Closed by `batches/ccfg-31-narrow-live-lease-preflight/closeout.md`: exact queue-transaction proof, ready/blocked behavior, preserved strict per-handoff safety, broad-protocol deletion, final validation, and clean exact-range review are complete. CCFG-29 remains the sole bridge-removal owner; no successor was selected. |
| CCFG-32. Make Planning State authoritative for queue currentness | Closed | GitHub issue #55; `findings/github-issue-55-planning-state-queue-currentness.md`; `batches/ccfg-32-planning-state-queue-currentness/closeout.md` | Cross-checkout startup / planning-currentness ownership | None | Closed by `batches/ccfg-32-planning-state-queue-currentness/closeout.md`: Git-derived queue paths, history inference, planning fingerprints, and topology-preserving tests are removed; material first-handoff and later lease safety remain behaviorally protected. CCFG-21, CCFG-25, and CCFG-29 remain separate and unselected. |
| CCFG-33. Simplify CCFG-23 acceptance execution | Pending | `batches/ccfg-23-behavioral-scenario-harness/execution-retrospective.md` | Command-owner redesign / behavioral-harness execution | Execute `batches/ccfg-33-acceptance-execution-simplification/runway.md` | Queued as one migration slice limited to the scenario-harness execution model: one evidence-pytest process, process-local evaluation reuse, pure reporting, removal of per-function source-hash authority, semantic fast/acceptance gates, and before/after cost evidence. The three known-red manifest tests remain deferred diagnostics for CCFG-24 through CCFG-26. CCFG-23 remains closed. |

## Batch Queue

Queued batch:
`docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/runway.md`.

| Batch | Status | Dispatch | Spec | Covers | Notes |
|---|---|---|---|---|---|
| `ccfg-1-runner-contract-fixtures` | completed | `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md` | CCFG-1 | Contract/fixture preparation only. |
| `ccfg-8-ledger-dispatch-rule-dedupe` | completed | `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/runway.md` | CCFG-8 | Runtime unchanged. |
| `ccfg-7-batch-runway-hot-path-pruning` | completed | `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/runway.md` | CCFG-7 | Closed. |
| `ccfg-12-plan-batch-deepening` | completed | `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/runway.md` | CCFG-12 | Closed. |
| `ccfg-11-skill-deletion-tests` | superseded | `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/runway.md` | CCFG-11 | Planning evidence only; must be replanned. |
| `ccfg-13-validation-command-status` | completed | `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md` | CCFG-13 | Closed. |
| `ccfg-14-batch-kind-slice-risk` | completed | `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/runway.md` | CCFG-14 | Closed. |
| `ccfg-15-vague-ledger-row-splitting` | completed | `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/runway.md` | CCFG-15 | Closed. |
| `ccfg-16-deletion-test-vocabulary-ownership` | completed | `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/runway.md` | CCFG-16 | Closed. |
| `ccfg-17-absolute-runway-reference-paths` | completed | `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/runway.md` | CCFG-17 | Closed. |
| `ccfg-18-stable-control-bootstrap` | completed | `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/runway.md` | CCFG-18 | Stable bootstrap completed with a `Prepared` result; the later pre-creation circularity left the finding `Blocked` before the support batch. Candidate-generation remainder stayed under CCFG-18. |
| `ccfg-18-stable-precreation-support` | completed | `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/runway.md` | CCFG-18 | Stable support completed in `e012d93..314fbcb` and left CCFG-18 blocked on installation/fresh-session reload; the current queued batch records that gate as satisfied. Candidate paths remain absent. |
| `ccfg-18-candidate-generation` | completed | `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/runway.md` | CCFG-18 | Completed in candidate range `da5b971..9027bd1` and stable planning range `da5b971..968f41d`; corrected closeout proves lineage, strict transition, generation isolation, fixture-only operation, quiescence, and unchanged-default rollback through the primary shell CLI. CCFG-19 remains unselected. |
| `ccfg-19-source-contract-decisions` | completed | `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md` | CCFG-19 | Completed in candidate range `9027bd1..13d7f63`; all seven exit keys are evidenced and OPEN-003 is resolved. Same-batch closeout selected no successor. |
| `ccfg-20-skill-contract-schema` | completed | `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/runway.md` | CCFG-20 | Completed in candidate range `13d7f63..3e54155`; all five COR-003 keys are green, final range review is clean, and same-batch closeout selected no successor. |
| `ccfg-21-planning-artifact-contracts` | completed | `docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/runway.md` | CCFG-21 | Completed in candidate range `3e54155..596fc7e`; all COR-004 keys, final validation, and exact-range review are green; same-batch closeout selected no successor. |
| `ccfg-22-skill-authoring-v1` | completed | `docs/plans/programs/codex-config/batches/ccfg-22-skill-authoring-v1/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-22-skill-authoring-v1/runway.md` | CCFG-22 | Completed in candidate range `596fc7e..2f39950`; all nine COR-005 keys, candidate-only installation, final validation, exact-range test-quality review, and independent final review are green. Same-batch closeout selected no successor. |
| `ccfg-23-behavioral-scenario-harness` | completed | `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/runway.md` | CCFG-23 | Completed in candidate range `2f39950..e8d07a7`; all six COR-006 keys and aliases, final validation, installer isolation, exact-range test-quality review, and independent final review are green. Same-batch closeout selected no successor. |
| `ccfg-30-cross-flight-execution-leases` | completed | `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/runway.md` | CCFG-30 | Completed in stable range `d8f3952^..7917ace`; all ten regression scenarios and final range review are green; same-batch closeout selected no successor. |
| `ccfg-31-narrow-live-lease-preflight` | completed | `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/runway.md` | CCFG-31 | Completed in stable range `cdcb05e^..401a468`; the normal result is only ready/blocked, preserved safety is behaviorally proven, broad protocol topology is deleted, and same-batch closeout selected no successor. |
| `ccfg-32-planning-state-queue-currentness` | completed | `docs/plans/programs/codex-config/batches/ccfg-32-planning-state-queue-currentness/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-32-planning-state-queue-currentness/runway.md` | CCFG-32 | Completed in stable range `6ede5b2..7ef07dc`; Planning State owns semantic currentness, material handoff safety remains green, and same-batch closeout selected no successor. |
| `ccfg-33-acceptance-execution-simplification` | pending | `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/runway.md` | CCFG-33 | Queued as one bounded migration slice; unrelated manifest known-red tests remain deferred diagnostics. |

## Recommended Work Order

1. Start pickup from root and program `CURRENT.md`.
2. CCFG-18 through CCFG-23 and CCFG-30 through CCFG-32 are closed.
3. CCFG-33 is the only queued batch. Execute it only through a later explicit
   `work-batch` request; do not replace it or select another batch.
4. CCFG-24 waits for CCFG-33 closeout. Keep CCFG-24 through CCFG-29 and all
   older open rows unselected until separately requested.
5. Do not revive archived APR/PST ledgers as pickup sources.
6. Keep CCFG-11 open but do not execute its displaced runway.

## Closeout Rules

- Close CCFG-18 through CCFG-29 and CCFG-33 only from the acceptance evidence
  and stop boundaries in the ledger, local intake files, live amendments, and
  immutable accepted design snapshot.
- A redesign closeout must record controlling generation, planning root,
  implementation root, relevant revisions, temporary bridges, and legacy
  ownership removed.
- CCFG-18 closed through
  `batches/ccfg-18-candidate-generation/closeout.md` without selecting CCFG-19.
- CCFG-19 closed through
  `batches/ccfg-19-source-contract-decisions/closeout.md` with all seven
  COR-002 acceptance keys evidenced and OPEN-003 resolved. Its closeout cleared
  queued state and selected no successor.
- CCFG-20 closed through
  `batches/ccfg-20-skill-contract-schema/closeout.md` with all five COR-003
  acceptance keys green. Its closeout cleared same-batch state and selected no
  successor.
- CCFG-21 closed through
  `batches/ccfg-21-planning-artifact-contracts/closeout.md` with all six COR-004
  acceptance keys, detailed migration gates, fault injection, and clean exact-
  range review green. Its closeout cleared same-batch state and selected no
  successor.
- CCFG-22 closed through `batches/ccfg-22-skill-authoring-v1/closeout.md` with
  all nine COR-005 keys, candidate-only installation, exact known-red baseline,
  final validation, and clean exact-range reviews green. Its closeout cleared
  same-batch state and selected no successor.
- CCFG-23 closed through
  `batches/ccfg-23-behavioral-scenario-harness/closeout.md` with all six COR-006
  keys and aliases, 31-contract coverage, final validation, installer
  isolation, and clean exact-range reviews green. Its closeout cleared
  same-batch state and selected no successor.
- CCFG-31 closed through
  `batches/ccfg-31-narrow-live-lease-preflight/closeout.md` with ready/blocked
  behavior, preserved per-handoff safety, deletion evidence, final validation,
  and clean exact-range review. Its closeout cleared same-batch state and
  selected no successor.
- CCFG-30 closed through
  `batches/ccfg-30-cross-flight-execution-leases/closeout.md` with all ten
  cross-flight regression scenarios, linked-state checks, and exact-range
  review green. Its closeout cleared same-batch state and selected no successor.
- CCFG-32 closed through
  `batches/ccfg-32-planning-state-queue-currentness/closeout.md` with semantic
  currentness owned by Planning State, material live-handoff safety preserved,
  deletion evidence, final validation, and clean exact-range review. Its
  closeout cleared same-batch state and selected no successor.
- CCFG-33 may close only if COR-006 behavior remains green, reporter-owned
  nested pytest is removed, one evidence-pytest process owns exact-commit
  acceptance, evaluation reuse is process-local and input-bound, JSON/text
  reporting is pure, per-function source-hash authority and its preserving tests
  are removed or demoted, the exact known-red manifest diagnostic is unchanged,
  and before/after cost evidence is recorded. Its closeout selects no successor.
- The `ccfg-18-stable-control-bootstrap` closeout marks CCFG-18 `Prepared`, not
  `Closed`, records the changed stable commit and fresh-session handoff, and
  preserves all candidate-generation remainder under the same finding identity.
- The stable pre-creation gate, candidate lineage, strict transition,
  generation identity, fixture isolation, quiescence, and rollback are proven;
  `ccfg-18-candidate-generation` is completed.
- CCFG-24 through CCFG-29 must delete CCFG-23 adapters, duplicate workflow
  models, and preserving tests as the corresponding real owner becomes
  authoritative. Any temporary retention must name a caller, reason, owner,
  and removal condition.
- The three existing known-red manifest tests are not CCFG-33 cleanup: source
  boundary migration belongs to CCFG-24/25, planning runtime-boundary migration
  belongs to CCFG-25, and same-batch closeout migration belongs to CCFG-26.
- CCFG-27 does not switch the default generation.
- CCFG-28 switches only after legacy-owner deletion, clean-install proof, and
  CCFG-27 temporary bridge parity/rehearsal proof. The candidate installation
  retains the minimum bridge needed to reach CCFG-29, then CCFG-28 closes under
  the pinned stable controller and stops.
- CCFG-29 merges candidate into latest authoritative `master`, removes the
  complete temporary cross-checkout bridge and both retained live-context APIs,
  and restores integrated `master` as the default Codex-home toolchain source.
