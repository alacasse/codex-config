# Codex Config Program Ledger

## Purpose

Track active and candidate codex-config workflow work in one canonical program
ledger. This ledger is the only active executable backlog source under
`docs/plans/` for `add-to-ledger`, `plan-batch`, and `work-batch`.

## Current Direction

- Keep repo-owned workflow skills project-neutral and extraction-ready.
- Keep Planning Artifact Layout v1 pickup rooted at `docs/plans/CURRENT.md`.
- Start reusable work from the user-visible product, not the current
  codex-config installer or dogfood topology.
- Keep the planning root user-selected and keep one batch's small runtime state
  under that batch directory by default.
- Treat `CODEX_HOME`, symlinks, stable/candidate checkouts, cross-checkout
  bridges, and developer paths as temporary dogfood mechanics unless the user
  explicitly promotes one into the product.
- Require Product Boundary, Dogfood Boundary, Threat Model, and Guarantee
  Feasibility in architecture, migration, extraction, runner, storage, and
  installation plans.
- Do not begin large production work while its decisive implementation primitive
  is unknown.
- Keep Markdown and JSON readable, diffable, and repairable.
- Keep SQLite optional and rebuildable as a reporting projection.
- Keep all codex-config workflow and skill-cleanup work in this ledger.
- Create a dispatch or runway only when one row is explicitly chosen by
  `plan-batch`. CCFG-26A and the issue #66 slice-shape policy correction are
  completed and reconciled. CCFG-26B and
  `ccfg-26-execution-state-foundation` are superseded. The queue is empty, no
  implementation Slice is accepted, the candidate WIP remains under user
  control, CCFG-26 is Ready for fresh extraction-first planning after that WIP
  is isolated from the future write scope, and no successor is selected.

## Source Context

- Root current state: `docs/plans/CURRENT.md`
- Program current state: `docs/plans/programs/codex-config/CURRENT.md`
- Workflow guide: `docs/workflow-guide.md`
- Skill routing contract: `docs/skill-routing-contract.md`
- Live command-owner redesign intake:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md`
- Live CCFG-24 two-batch execution amendment:
  `docs/plans/programs/codex-config/findings/ccfg-24-two-batch-execution-amendment.md`
- Accepted CCFG-24A `add-to-ledger/v1` decision amendment:
  `docs/plans/programs/codex-config/findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`
- CCFG-24A closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/closeout.md`
- CCFG-24B closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-24b-intake-ownership-cutover/closeout.md`
- Live CCFG-25 planning-quality amendment:
  `docs/plans/programs/codex-config/findings/ccfg-25-planning-quality-amendment.md`
- Live CCFG-34 intake and CCFG-26 replanning amendment:
  `docs/plans/programs/codex-config/findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`
- CCFG-26 slice-shape policy direction from GitHub issue #66:
  `docs/plans/programs/codex-config/findings/slice-shape-policy-direction.md`
- CCFG-26 slice-shape policy post-closeout correction evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/post-closeout-correction.md`
- Active extraction-first architecture:
  `docs/adr/0004-extraction-first-batch-local-execution.md`
- Active CCFG-26 product/dogfood reset:
  `docs/plans/programs/codex-config/findings/ccfg-26-product-dogfood-reset.md`
- CCFG-26 execution-state foundation supersession notice:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/superseded.md`
- Historical CCFG-26 execution-state direction amendment:
  `docs/plans/programs/codex-config/findings/ccfg-26-execution-state-authority-direction.md`
- Historical CCFG-26 replan analysis and ChatGPT Pro handoff:
  `docs/plans/programs/codex-config/notes/ccfg-26-replan-analysis-and-chatgpt-pro-handoff.md`
- Historical CCFG-26 execution-state design contract:
  `docs/plans/programs/codex-config/notes/ccfg-26-execution-state-design-contract.md`
- Historical CCFG-26 execution-state design review:
  `docs/plans/programs/codex-config/notes/ccfg-26-execution-state-design-review.md`
- Historical CCFG-26 execution-state foundation dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/dispatch.md`
- Historical CCFG-26 execution-state foundation runway:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/runway.md`
- Historical CCFG-26 execution-state foundation planning review:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/review.md`
- Historical CCFG-26 execution-state foundation bootstrap amendment:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/amendment.md`
- Historical CCFG-26 execution-state foundation bootstrap amendment review:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/amendment-review.md`
- Blocked CCFG-26 execution-state foundation Slice 1 report:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/execution-report.md`
- CCFG-26 execution-state foundation Slice 1 failure retrospective:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/execution-retrospective.md`
- Superseded canonical batch execution-state ADR:
  `docs/adr/0003-canonical-batch-execution-state.md`
- CCFG-26B supersession notice:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/superseded.md`
- Historical CCFG-26B progression-authority correction:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/progression-authority-correction.md`
- Historical CCFG-26B progression-authority review:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/progression-authority-review.md`
- Historical CCFG-26B unresolved-attempt barrier correction, exact SHA-256
  `94388b089bd1da22d570576735c567f08bb994cf7ddba809f0c2f013f445a3ad`:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/progression-attempt-barrier-correction.md`
- Historical CCFG-26B unresolved-attempt barrier review, exact SHA-256
  `386694d7c06db5c6bb1f55018dc623be2d0bfcf40d733972ab826ac6ba5ac433`:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/progression-attempt-barrier-review.md`
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
| CCFG-18. Establish Stable and Candidate Generations | Closed | [COR-001](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-001--ccfg-18--establish-stable-and-candidate-generations) plus live pre-creation amendment in `findings/command-owner-redesign-implementation-intake.md` | Command-owner redesign / control-plane isolation | None | Closed by `batches/ccfg-18-candidate-generation/closeout.md`: authoritative and accepted-design lineage, strict transition, isolated candidate installation, fixture-only operation, canonical-write rejection, quiescence, and unchanged-default rollback are proven. CCFG-19 remains unselected. The stable/candidate topology is dogfood infrastructure, not product architecture. |
| CCFG-19. Verify Source Contracts and Resolve Blocking Decisions | Closed | [COR-002](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-002--ccfg-19--verify-source-contracts-and-resolve-blocking-decisions) | Command-owner redesign / contracts | None | Closed by `batches/ccfg-19-source-contract-decisions/closeout.md`: all 31 contracts are joined, all seven acceptance keys are evidenced, DEC-036/037/017/038 are accepted, and OPEN-003 is resolved. CCFG-20 closed separately. |
| CCFG-20. Implement `skill-contract/v1` Schema and Validators | Closed | [COR-003](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-003--ccfg-20--implement-skill-contractv1-schema-and-validators) | Command-owner redesign / skill contracts | None | Closed by `batches/ccfg-20-skill-contract-schema/closeout.md`: all five COR-003 keys are green in candidate range `13d7f63..3e54155`. |
| CCFG-21. Implement Planning Artifact Schemas and Validators | Closed | [COR-004](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-004--ccfg-21--implement-planning-artifact-schemas-and-validators) | Command-owner redesign / planning contracts | None | Closed by `batches/ccfg-21-planning-artifact-contracts/closeout.md`: all six COR-004 keys, migration gates, fault checkpoints, and exact-range review are green. |
| CCFG-22. Finalize and Validate `skill-authoring` v1 | Closed | [COR-005](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-005--ccfg-22--finalize-and-validate-skill-authoring-v1) | Command-owner redesign / authoring | None | Closed by `batches/ccfg-22-skill-authoring-v1/closeout.md`: all nine COR-005 keys and candidate-only installation are proven. |
| CCFG-23. Build the Topology-Independent Behavioral Scenario Harness | Closed | [COR-006](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-006--ccfg-23--build-the-topology-independent-behavioral-harness) plus live harness scenarios in `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / behavioral harness | None | Closed by `batches/ccfg-23-behavioral-scenario-harness/closeout.md`: all six COR-006 keys and six aliases are green across 69 scenarios, 31 contracts, and 17 families. |
| CCFG-24. Transfer Intake Ownership to `add-to-ledger` | Closed | [COR-007](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-007--ccfg-24--transfer-intake-ownership-to-add-to-ledger), `findings/ccfg-24-two-batch-execution-amendment.md`, and `findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md` | Command-owner redesign / intake ownership | None | Closed by `batches/ccfg-24b-intake-ownership-cutover/closeout.md`: `add-to-ledger/v1` is the sole intake and normal mutation-decision owner; APR intake and legacy state-owner routes are absent; candidate range `3b0941a..91179e8`, isolated installation, exact acceptance, and final reviews are green. CCFG-25 remains unselected. |
| CCFG-25. Transfer Planning Ownership to `plan-batch` | Closed | [COR-008](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-008--ccfg-25--transfer-planning-ownership-to-plan-batch), `findings/ccfg-25-planning-quality-amendment.md`, and `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / planning ownership | None | Closed by `batches/ccfg-25-planning-ownership-transfer/closeout.md`: one complete `plan-batch` invocation owns selection, independent planning review, proportionality, and the DEC-038 transaction; displaced planning owners are removed; candidate range `91179e8..89671ec`, real installations, exact acceptance, and final reviews are green. The closeout selected no successor; later CCFG-26 planning was superseded. |
| CCFG-26. Transfer Execution and Closeout Ownership to `work-batch` | Ready | [COR-009](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-009--ccfg-26--transfer-execution-and-closeout-ownership-to-work-batch), `docs/adr/0004-extraction-first-batch-local-execution.md`, `findings/ccfg-26-product-dogfood-reset.md`, GitHub issue #66, `findings/slice-shape-policy-direction.md`, `findings/command-owner-redesign-planning-execution-carry-forward.md`, and `findings/github-issue-62-stable-runway-dogfooding-bootstrap.md` | Command-owner redesign / execution ownership | After the user isolates the preserved candidate WIP from future write scope, run a fresh explicit `plan-batch CCFG-26` | CCFG-26 and COR-009 remain open. The replacement must start from the extraction-ready product, use batch-local state, keep codex-config installation mechanics in a dogfood adapter, and limit v1 to accidental concurrency and process-crash safety on trusted local filesystems. No implementation Slice is accepted and no successor is selected. |
| CCFG-27. Prepare and Rehearse Candidate Cutover | Open | [COR-010](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-010--ccfg-27--prepare-and-rehearse-candidate-cutover) plus live bridge-readiness gate in `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / cutover preparation | Wait for CCFG-26 | Prove candidate-installed bridge parity and rehearse cutover without changing the default generation. Own the runner public-protocol decision to migrate or remove the temporary serialized `select-dispatch` and `create-spec` labels and old runner modes. Unselected. |
| CCFG-28. Remove Legacy Owners and Commit Final Cutover | Open | [COR-011](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-011--ccfg-28--remove-legacy-owners-and-commit-final-cutover) plus live switch gate in `findings/command-owner-redesign-planning-execution-carry-forward.md` | Command-owner redesign / deletion and final switch | Wait for CCFG-27 | Delete remaining legacy owners and switch only after rehearsal proof. Unselected. |
| CCFG-29. Contract-First Convergence and Final Integration | Open | [COR-012](https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-012--ccfg-29--contract-first-convergence-and-final-integration), `findings/command-owner-redesign-planning-execution-carry-forward.md`, and `findings/github-issue-62-stable-runway-dogfooding-bootstrap.md` | Command-owner redesign / convergence and final integration | Wait for CCFG-28 | Merge candidate into authoritative master, remove the temporary bridge, restore integrated master as default, and remove the CCFG-34 policy and hook only after permanent #59/#60/#61 parity and equivalent regression proof. Stop if parity is incomplete. Unselected. |
| CCFG-30. Separate Planning Snapshots from Live Execution Leases | Closed | `notes/cross-flight-execution-baseline-plan.md`; `batches/ccfg-30-cross-flight-execution-leases/dispatch.md` | Batch Runway / cross-checkout execution lifecycle | None | Closed with exact live-lease validation and linked lifecycle proof. |
| CCFG-31. Narrow ready/blocked live-lease preflight | Closed | GitHub issue #53; `findings/github-issue-53-narrow-live-lease-preflight.md` | Batch Runway / cross-checkout execution lifecycle | None | Closed with ready/blocked behavior and preserved handoff safety. |
| CCFG-32. Make Planning State authoritative for queue currentness | Closed | GitHub issue #55; `findings/github-issue-55-planning-state-queue-currentness.md`; `batches/ccfg-32-planning-state-queue-currentness/closeout.md` | Cross-checkout startup / planning-currentness ownership | None | Closed with semantic currentness owned by Planning State and material handoff safety preserved. |
| CCFG-33. Simplify CCFG-23 acceptance execution | Closed | `batches/ccfg-23-behavioral-scenario-harness/execution-retrospective.md`; `batches/ccfg-33-acceptance-execution-simplification/closeout.md` | Command-owner redesign / behavioral-harness execution | None | Closed with one exact-commit evidence-pytest process and preserved COR-006 behavior. |
| CCFG-34. Bootstrap minimal stable runway dogfooding before CCFG-26 | Closed | GitHub issue #62; `findings/github-issue-62-stable-runway-dogfooding-bootstrap.md` | Stable runway / temporary dogfooding bootstrap | None | Closed by `batches/ccfg-34-stable-runway-dogfooding-bootstrap/closeout.md` and implementation commit `ba1e941`: root `AGENTS.md` loads the temporary policy, the focused contract gate and reviews are green, and no runner, generic skill, agent contract, candidate, runtime state, or successor changed. |

## Batch Queue

Active batch: `None`.
Selected dispatch and active runway are `None`.
Queued batch: `None`.

| Batch | Status | Dispatch | Spec | Covers | Notes |
|---|---|---|---|---|---|
| `ccfg-1-runner-contract-fixtures` | completed | `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md` | CCFG-1 | Contract/fixture preparation only. |
| `ccfg-7-batch-runway-hot-path-pruning` | completed | `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/runway.md` | CCFG-7 | Closed. |
| `ccfg-8-ledger-dispatch-rule-dedupe` | completed | `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/runway.md` | CCFG-8 | Runtime unchanged. |
| `ccfg-11-skill-deletion-tests` | superseded | `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/runway.md` | CCFG-11 | Planning evidence only; must be replanned. |
| `ccfg-12-plan-batch-deepening` | completed | `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/runway.md` | CCFG-12 | Closed. |
| `ccfg-13-validation-command-status` | completed | `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md` | CCFG-13 | Closed. |
| `ccfg-14-batch-kind-slice-risk` | completed | `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/runway.md` | CCFG-14 | Closed. |
| `ccfg-15-vague-ledger-row-splitting` | completed | `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/runway.md` | CCFG-15 | Closed. |
| `ccfg-16-deletion-test-vocabulary-ownership` | completed | `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-16-deletion-test-vocabulary-ownership/runway.md` | CCFG-16 | Closed. |
| `ccfg-17-absolute-runway-reference-paths` | completed | `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/runway.md` | CCFG-17 | Closed. |
| `ccfg-18-stable-control-bootstrap` | completed | `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/runway.md` | CCFG-18 | Historical bootstrap phase. |
| `ccfg-18-stable-precreation-support` | completed | `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/runway.md` | CCFG-18 | Historical support phase. |
| `ccfg-18-candidate-generation` | completed | `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/runway.md` | CCFG-18 | Candidate generation closed; dogfood infrastructure only. |
| `ccfg-19-source-contract-decisions` | completed | `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md` | CCFG-19 | Closed. |
| `ccfg-20-skill-contract-schema` | completed | `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/runway.md` | CCFG-20 | Closed. |
| `ccfg-21-planning-artifact-contracts` | completed | `docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/runway.md` | CCFG-21 | Closed. |
| `ccfg-22-skill-authoring-v1` | completed | `docs/plans/programs/codex-config/batches/ccfg-22-skill-authoring-v1/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-22-skill-authoring-v1/runway.md` | CCFG-22 | Closed. |
| `ccfg-23-behavioral-scenario-harness` | completed | `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/runway.md` | CCFG-23 | Closed. |
| `ccfg-30-cross-flight-execution-leases` | completed | `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/runway.md` | CCFG-30 | Closed. |
| `ccfg-31-narrow-live-lease-preflight` | completed | `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/runway.md` | CCFG-31 | Closed. |
| `ccfg-32-planning-state-queue-currentness` | completed | `docs/plans/programs/codex-config/batches/ccfg-32-planning-state-queue-currentness/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-32-planning-state-queue-currentness/runway.md` | CCFG-32 | Closed. |
| `ccfg-33-acceptance-execution-simplification` | completed | `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/runway.md` | CCFG-33 | Closed. |
| `ccfg-24-intake-ownership-transfer` | superseded | `docs/plans/programs/codex-config/batches/ccfg-24-intake-ownership-transfer/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-24-intake-ownership-transfer/runway.md` | CCFG-24 | Superseded historical source analysis. |
| `ccfg-24a-intake-owner-preparation` | completed | `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/runway.md` | CCFG-24 | Completed in candidate range `b38570b..3b0941a`; CCFG-24 became `Prepared`. |
| `ccfg-24b-intake-ownership-cutover` | completed | `docs/plans/programs/codex-config/batches/ccfg-24b-intake-ownership-cutover/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-24b-intake-ownership-cutover/runway.md` | CCFG-24 | Completed in candidate range `3b0941a..91179e8`; COR-007 closed with converged isolated installation, exact acceptance, and no stable-home mutation. |
| `ccfg-25-planning-ownership-transfer` | completed | `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/runway.md` | CCFG-25 | Closed in candidate range `91179e8..89671ec`; configured-project validation, fresh and isolated installation, stable-home comparison, exact acceptance, and all final reviews are green. No successor was selected. |
| `ccfg-26-execution-closeout-ownership-transfer` | superseded | `docs/plans/programs/codex-config/batches/ccfg-26-execution-closeout-ownership-transfer/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-26-execution-closeout-ownership-transfer/runway.md` | CCFG-26 | Preserved historical planning evidence only; see `batches/ccfg-26-execution-closeout-ownership-transfer/superseded.md`. Do not execute or resume. |
| `ccfg-26a-permanent-vertical-runway-contract` | completed | `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/runway.md` | CCFG-26 | Closed by `batches/ccfg-26a-permanent-vertical-runway-contract/closeout.md` at candidate commit `a0835f1`: issue #60 vertical planning behavior, installation, exact acceptance, and final reviews are green; no successor was selected. |
| `ccfg-26-slice-shape-policy-correction` | completed | `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/runway.md` | CCFG-26 | Original closeout remains historical at candidate commit `8a93319` and stable evidence commits `f5cb753` / `66cb6d4`. `batches/ccfg-26-slice-shape-policy-correction/post-closeout-correction.md` records the semantic-authority correction at candidate commit `5c5ec9d`; no successor was selected or prepared. |
| `ccfg-26-execution-state-foundation` | superseded | `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/runway.md` | CCFG-26 | No Slice was accepted and no candidate implementation commit exists. The uncommitted WIP remains under user control and is not planning authority. See `superseded.md`, `execution-report.md`, and `execution-retrospective.md`. |
| `ccfg-26b-fresh-slice-flight` | superseded | `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/runway.md` | CCFG-26 | Superseded by explicit user cancellation before implementation; see `batches/ccfg-26b-fresh-slice-flight/superseded.md`. All nine prior planning and review artifacts remain historical evidence. Do not execute, resume, amend, close, or infer queue/currentness from them. No successor was selected. |
| `ccfg-26c-bounded-recovery` | candidate | None | None | CCFG-26 | Unselected conceptual evidence only. Its owner, prerequisite, and boundary must be re-derived from fresh extraction-first planning rather than any superseded sequence. |
| `ccfg-26d-finalization-flight` | candidate | None | None | CCFG-26 | Unselected conceptual evidence only. Its prerequisite and boundary must be re-derived after accepted execution behavior exists. |
| `ccfg-26e-closeout-ownership-cutover` | candidate | None | None | CCFG-26 | Unselected conceptual evidence only. Closeout/reconciliation/no-successor proof and displaced-owner narrowing remain concerns, not an accepted order. |
| `ccfg-34-stable-runway-dogfooding-bootstrap` | completed | `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/dispatch.md` | `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/runway.md` | CCFG-34 | Closed by implementation commit `ba1e941` with clean focused validation, delta-only test-quality review, final independent review, and no successor selection. |

## Recommended Work Order

1. Start pickup from root and program `CURRENT.md`.
2. CCFG-18 through CCFG-25 and CCFG-30 through CCFG-34 are closed.
3. Parent CCFG-26 is `Ready`; CCFG-26B and
   `ccfg-26-execution-state-foundation` are superseded historical evidence.
4. Keep the queue empty. The user decides how to isolate or preserve the dirty
   candidate WIP; no workflow edits it.
5. A later explicit `plan-batch CCFG-26` creates one fresh extraction-first
   runway from ADR 0004 and the product/dogfood reset. It starts from the OSS
   product, uses batch-local runtime state, limits v1 to trusted-local accidental
   concurrency and process-crash safety, identifies material primitives before
   coding, and keeps codex-config installation mechanics in a removable dogfood
   adapter.
6. Do not execute or amend CCFG-26B, resume the superseded foundation, or infer a
   successor from either historical design.
7. Keep CCFG-26C through CCFG-26E, CCFG-27 through CCFG-29, and all older open
   rows unselected until an explicit future command chooses one under proven
   dependency edges.
8. Do not revive archived APR/PST ledgers as pickup sources.
9. Keep CCFG-11 open but do not execute its displaced runway.

## Closeout Rules

- Close findings only from implementation, validation, review, and same-batch
  reconciliation evidence; a dispatch or runway is not closeout evidence.
- A redesign closeout records controlling generation, all roots and commits,
  candidate installation, removed and preserved temporary surfaces, validation,
  reviews, and no-successor state.
- CCFG-24B closed CCFG-24 only after proving:
  - `add-to-ledger/v1` is the sole intake and normal ledger-mutation decision owner;
  - `ledger-store/v1` remains apply-only;
  - APR intake, normalization, normal mutation authority, and every fallback route
    are absent;
  - APR responsibilities reserved for CCFG-25/26 remain explicit and tested;
  - `legacy-removal` has no state-owner escape hatch and remains a valid evidence
    and classification producer;
  - CCFG-23 zero-caller/topology-only residue is removed or any retention has a
    current caller, reason, owner, and removal condition;
  - replacement scenarios and complete COR-007 acceptance are green;
  - candidate installation converges and stable/default ownership is unchanged;
  - only the three named CCFG-25/26 manifest diagnostics remain red;
  - same-batch closeout clears selected/queued/active state and selects no successor.
- CCFG-25 is closed by
  `batches/ccfg-25-planning-ownership-transfer/closeout.md` in exact candidate
  range `91179e84c7cfed666be224575db7000ca0ea01b3..89671eceb9103039e7e6660e73837827c167a3a1`.
- CCFG-25 owns APR planning/selection/queue and Batch Runway create-spec transfer.
- CCFG-25 must preserve all proceed/stop, delegation, recovery, validation,
  implementation review, commit, receipt, execution-ledger, finalization,
  closeout, same-batch reconciliation, and strict execution-safety
  responsibilities reserved for CCFG-26.
- CCFG-26 owns the later APR and Batch Runway execution/closeout transfer.
- The prior CCFG-26 dispatch, review, and runway are superseded by the issue #62
  intake amendment and cannot be executed or resumed.
- The later CCFG-26B dispatch, runway, amendment, and correction bundle was
  superseded by explicit user cancellation on 2026-07-19 before implementation.
  `batches/ccfg-26b-fresh-slice-flight/superseded.md` preserves the historical
  evidence boundary.
- The later `ccfg-26-execution-state-foundation` dispatch, runway, amendment,
  reviews, and attempted Slice 1 are superseded by the extraction-first reset.
  No part is accepted implementation. The uncommitted WIP remains under the
  user's control.
- ADR 0004 and `findings/ccfg-26-product-dogfood-reset.md` are the live CCFG-26
  architecture and reset authority. ADR 0003 and its detailed design documents
  remain historical only.
- CCFG-34 closed before any fresh CCFG-26 planning. Replacement planning must
  preserve CCFG-26 and COR-009 identity and consume the permanent candidate
  requirements from issues #59, #60, and #61 without letting dogfood topology
  shape the product.
- GitHub issue #66 and `findings/slice-shape-policy-direction.md` amend CCFG-26
  after CCFG-26A without reopening it. The bounded corrective preparation batch
  kept migration evidence independent from the externally resolved slice-shape
  policy and added no historical compatibility.
- The issue #66 post-closeout correction replaces only the reusable semantic
  shape authority claim. It preserves the original closeout as historical
  evidence, the stable temporary vertical overlay, and the no-successor state.
- CCFG-34 closeout stopped without selecting CCFG-26. The reset also selects no
  successor and leaves the queue empty.
- CCFG-34 is closed by
  `batches/ccfg-34-stable-runway-dogfooding-bootstrap/closeout.md`; its closeout
  selected no successor and leaves CCFG-26 open but unselected.
- CCFG-27 does not switch the default generation.
- CCFG-27 owns the migration/removal decision for the temporary serialized
  `select-dispatch` and `create-spec` labels and old runner modes; CCFG-29 is the
  final physical-cleanup deadline if CCFG-27 retains them.
- CCFG-28 switches only after CCFG-27 rehearsal proof and stops under the pinned
  stable controller.
- CCFG-29 merges candidate into latest authoritative master, removes the
  temporary cross-checkout bridge, removes the CCFG-34 policy and hook only after
  candidate #59/#60/#61 parity is proven, and restores integrated master as the
  default toolchain. It stops if parity is incomplete.
- Future architecture, migration, extraction, runner, storage, or installation
  closeout must show that temporary dogfood mechanics did not enter the product
  API, schemas, state layout, or terminology without explicit user approval.
- A material guarantee cannot be closed from tests alone when its implementation
  primitive or required platform proof was never established.
