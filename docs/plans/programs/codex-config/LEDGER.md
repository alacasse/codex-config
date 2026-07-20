# Codex Config Program Ledger

## Purpose

Track active and candidate codex-config workflow work in one canonical program
ledger. This ledger is the only active executable backlog source under
`docs/plans/` for `add-to-ledger`, `plan-batch`, and `work-batch`.

## Current Direction

- Keep repo-owned workflow skills project-neutral and extraction-ready.
- Start from the user-visible product, not the current codex-config installer or
  dogfood topology.
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
- Keep Markdown and JSON readable, diffable, and repairable. Keep SQLite optional
  and rebuildable as a reporting projection.
- Select work only through an explicit `plan-batch`; closeout never selects a
  successor.

## Current State

- Selected dispatch: `None`
- Active runway: `None`
- Queued batch: `None`
- CCFG-26: `Ready` for fresh planning after the user-controlled candidate WIP is
  isolated from the future execution scope.
- Superseded current attempt:
  `batches/ccfg-26-execution-state-foundation/superseded.md`
- Candidate WIP: uncommitted, unaccepted, preserved under user control, and not
  planning authority.
- Successor selected: `false`

## Live Sources

- Root current state: `docs/plans/CURRENT.md`
- Program current state: `docs/plans/programs/codex-config/CURRENT.md`
- Extraction-first architecture:
  `docs/adr/0004-extraction-first-batch-local-execution.md`
- CCFG-26 reset direction:
  `findings/ccfg-26-product-dogfood-reset.md`
- CCFG-26 failed-attempt retrospective:
  `batches/ccfg-26-execution-state-foundation/execution-retrospective.md`
- Temporary stable-runway dogfood policy:
  `notes/stable-runway-dogfooding-policy.md`
- Planning Artifact Layout v1: `skills/planning-artifacts/SKILL.md`
- Planning State Diagnostic: `skills/planning-state/SKILL.md`
- Immutable command-owner redesign source:
  `https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md`
- Archived APR/PST ledgers:
  `docs/plans/archive/program-ledgers/`

ADR 0003, the detailed execution-state design contract, and all plans derived
from them are historical evidence only after ADR 0004.

## Findings Ledger

| Finding | Status | Source | Area | Next action | Notes |
|---|---|---|---|---|---|
| CCFG-1. Contract-first runner business-logic extraction | Completed | APR-26 | Runner extraction | None | Contract/fixture preparation only. |
| CCFG-2. Branch-per-batch runner isolation mode | Open | APR-27; issue #11 | Runner workflow | Re-evaluate after the extraction boundary is stable | Do not let branch mechanics shape the core product. |
| CCFG-3. Contract-drift review skill | Open | APR-28; issue #14 | Runner support | Create only when current contract drift is measured | Support only. |
| CCFG-4. Runner adapter authoring skill | Open | APR-29; issue #16 | Runner support | Wait for the generic runtime boundary | Provider quirks stay outside the core. |
| CCFG-5. Baton dogfood diagnostics | Open | APR-30; issues #17-19 | Diagnostics | Sequence after the core boundary | Dogfood diagnostics read durable artifacts. |
| CCFG-6. Skill-slimmer support | Backlog | PST reconciliation #15 | Skill cleanup | Decide later | No current skill. |
| CCFG-7. Batch Runway hot-path pruning | Completed | PST #23 | Skill cleanup | None | Closed. |
| CCFG-8. Ledger and dispatch rule dedupe | Completed | PST #24 | Skill cleanup | None | Closed. |
| CCFG-9. Short skill frontmatter descriptions | Backlog | PST #25 | Skill cleanup | Later bounded cleanup | Open. |
| CCFG-10. Skill steering vocabulary | Backlog | PST #26 | Skill cleanup | Add only where useful | Open. |
| CCFG-11. Skill deletion tests | Open | PST #27 | Skill cleanup | Replan before execution | Old runway is superseded. |
| CCFG-12. Plan-batch command-owner deepening | Completed | `notes/command-owner-deepening-review.md` | Planning command | None | Closed. |
| CCFG-13. Validation command status classification | Completed | issue #29 | Planning guard | None | Closed. |
| CCFG-14. Batch kind and destructive-slice risk gates | Completed | issue #30 | Planning guard | None | Closed. |
| CCFG-15. Vague ledger row splitting | Completed | issue #33 | Planning guard | None | Closed. |
| CCFG-16. Deletion-test vocabulary ownership | Completed | issue #31 | Planning guard | None | Closed. |
| CCFG-17. Absolute runway reference paths | Completed | issue #32 | Planning guard | None | Closed. |
| CCFG-18. Establish Stable and Candidate Generations | Closed | COR-001 | Temporary control-plane isolation | None | Dogfood infrastructure only; not product architecture. |
| CCFG-19. Verify Source Contracts and Decisions | Closed | COR-002 | Contracts | None | Closed. |
| CCFG-20. Implement `skill-contract/v1` | Closed | COR-003 | Skill contracts | None | Closed. |
| CCFG-21. Implement Planning Artifact Contracts | Closed | COR-004 | Planning contracts | None | Closed. |
| CCFG-22. Finalize `skill-authoring` v1 | Closed | COR-005 | Authoring | None | Closed. |
| CCFG-23. Behavioral Scenario Harness | Closed | COR-006 | Behavioral harness | None | Closed. |
| CCFG-24. Transfer Intake Ownership | Closed | COR-007 | Intake ownership | None | Closed by CCFG-24B. |
| CCFG-25. Transfer Planning Ownership | Closed | COR-008 | Planning ownership | None | Closed; no successor selected. |
| CCFG-26. Transfer Execution And Closeout Ownership | Ready | COR-009; ADR 0004; `findings/ccfg-26-product-dogfood-reset.md` | Execution ownership | After the user isolates preserved WIP, run a fresh `plan-batch CCFG-26` | Start from the extraction-ready product. Batch-local state; trusted-local threat model; no installer concepts in the core. |
| CCFG-27. Prepare And Rehearse Candidate Cutover | Open | COR-010 | Cutover preparation | Wait for accepted CCFG-26 completion evidence | Temporary topology only. |
| CCFG-28. Remove Legacy Owners And Switch | Open | COR-011 | Final switch | Wait for CCFG-27 | Unselected. |
| CCFG-29. Final Integration | Open | COR-012 | Integration | Wait for CCFG-28 | Remove temporary bridge and dogfood policy after parity. |
| CCFG-30. Separate Planning Snapshots From Live Leases | Closed | CCFG-30 closeout | Cross-checkout lifecycle | None | Closed. |
| CCFG-31. Narrow Ready/Blocked Preflight | Closed | issue #53 | Cross-checkout lifecycle | None | Closed. |
| CCFG-32. Planning State Queue Currentness | Closed | issue #55 | Currentness | None | Closed. |
| CCFG-33. Simplify CCFG-23 Acceptance | Closed | CCFG-33 closeout | Harness execution | None | Closed. |
| CCFG-34. Minimal Stable Runway Dogfooding | Closed | issue #62 | Temporary dogfood | None | Removed later by CCFG-29. |

## Batch Queue

Active batch: `None`.
Selected dispatch: `None`.
Active runway: `None`.
Queued batch: `None`.

| Batch | Status | Dispatch | Spec | Covers | Notes |
|---|---|---|---|---|---|
| `ccfg-1-runner-contract-fixtures` | completed | `batches/ccfg-1-runner-contract-fixtures/dispatch.md` | `batches/ccfg-1-runner-contract-fixtures/runway.md` | CCFG-1 | Historical. |
| `ccfg-7-batch-runway-hot-path-pruning` | completed | `batches/ccfg-7-batch-runway-hot-path-pruning/dispatch.md` | `batches/ccfg-7-batch-runway-hot-path-pruning/runway.md` | CCFG-7 | Closed. |
| `ccfg-8-ledger-dispatch-rule-dedupe` | completed | `batches/ccfg-8-ledger-dispatch-rule-dedupe/dispatch.md` | `batches/ccfg-8-ledger-dispatch-rule-dedupe/runway.md` | CCFG-8 | Closed. |
| `ccfg-11-skill-deletion-tests` | superseded | `batches/ccfg-11-skill-deletion-tests/dispatch.md` | `batches/ccfg-11-skill-deletion-tests/runway.md` | CCFG-11 | Replan before execution. |
| `ccfg-12-plan-batch-deepening` | completed | `batches/ccfg-12-plan-batch-deepening/dispatch.md` | `batches/ccfg-12-plan-batch-deepening/runway.md` | CCFG-12 | Closed. |
| `ccfg-13-validation-command-status` | completed | `batches/ccfg-13-validation-command-status/dispatch.md` | `batches/ccfg-13-validation-command-status/runway.md` | CCFG-13 | Closed. |
| `ccfg-14-batch-kind-slice-risk` | completed | `batches/ccfg-14-batch-kind-slice-risk/dispatch.md` | `batches/ccfg-14-batch-kind-slice-risk/runway.md` | CCFG-14 | Closed. |
| `ccfg-15-vague-ledger-row-splitting` | completed | `batches/ccfg-15-vague-ledger-row-splitting/dispatch.md` | `batches/ccfg-15-vague-ledger-row-splitting/runway.md` | CCFG-15 | Closed. |
| `ccfg-16-deletion-test-vocabulary-ownership` | completed | `batches/ccfg-16-deletion-test-vocabulary-ownership/dispatch.md` | `batches/ccfg-16-deletion-test-vocabulary-ownership/runway.md` | CCFG-16 | Closed. |
| `ccfg-17-absolute-runway-reference-paths` | completed | `batches/ccfg-17-absolute-runway-reference-paths/dispatch.md` | `batches/ccfg-17-absolute-runway-reference-paths/runway.md` | CCFG-17 | Closed. |
| `ccfg-18-stable-control-bootstrap` | completed | `batches/ccfg-18-stable-control-bootstrap/dispatch.md` | `batches/ccfg-18-stable-control-bootstrap/runway.md` | CCFG-18 | Historical dogfood bootstrap. |
| `ccfg-18-stable-precreation-support` | completed | `batches/ccfg-18-stable-precreation-support/dispatch.md` | `batches/ccfg-18-stable-precreation-support/runway.md` | CCFG-18 | Historical dogfood support. |
| `ccfg-18-candidate-generation` | completed | `batches/ccfg-18-candidate-generation/dispatch.md` | `batches/ccfg-18-candidate-generation/runway.md` | CCFG-18 | Temporary candidate generation. |
| `ccfg-19-source-contract-decisions` | completed | `batches/ccfg-19-source-contract-decisions/dispatch.md` | `batches/ccfg-19-source-contract-decisions/runway.md` | CCFG-19 | Closed. |
| `ccfg-20-skill-contract-schema` | completed | `batches/ccfg-20-skill-contract-schema/dispatch.md` | `batches/ccfg-20-skill-contract-schema/runway.md` | CCFG-20 | Closed. |
| `ccfg-21-planning-artifact-contracts` | completed | `batches/ccfg-21-planning-artifact-contracts/dispatch.md` | `batches/ccfg-21-planning-artifact-contracts/runway.md` | CCFG-21 | Closed. |
| `ccfg-22-skill-authoring-v1` | completed | `batches/ccfg-22-skill-authoring-v1/dispatch.md` | `batches/ccfg-22-skill-authoring-v1/runway.md` | CCFG-22 | Closed. |
| `ccfg-23-behavioral-scenario-harness` | completed | `batches/ccfg-23-behavioral-scenario-harness/dispatch.md` | `batches/ccfg-23-behavioral-scenario-harness/runway.md` | CCFG-23 | Closed. |
| `ccfg-24-intake-ownership-transfer` | superseded | `batches/ccfg-24-intake-ownership-transfer/dispatch.md` | `batches/ccfg-24-intake-ownership-transfer/runway.md` | CCFG-24 | Historical. |
| `ccfg-24a-intake-owner-preparation` | completed | `batches/ccfg-24a-intake-owner-preparation/dispatch.md` | `batches/ccfg-24a-intake-owner-preparation/runway.md` | CCFG-24 | Closed. |
| `ccfg-24b-intake-ownership-cutover` | completed | `batches/ccfg-24b-intake-ownership-cutover/dispatch.md` | `batches/ccfg-24b-intake-ownership-cutover/runway.md` | CCFG-24 | Closed. |
| `ccfg-25-planning-ownership-transfer` | completed | `batches/ccfg-25-planning-ownership-transfer/dispatch.md` | `batches/ccfg-25-planning-ownership-transfer/runway.md` | CCFG-25 | Closed. |
| `ccfg-26-execution-closeout-ownership-transfer` | superseded | `batches/ccfg-26-execution-closeout-ownership-transfer/dispatch.md` | `batches/ccfg-26-execution-closeout-ownership-transfer/runway.md` | CCFG-26 | Historical. |
| `ccfg-26a-permanent-vertical-runway-contract` | completed | `batches/ccfg-26a-permanent-vertical-runway-contract/dispatch.md` | `batches/ccfg-26a-permanent-vertical-runway-contract/runway.md` | CCFG-26 | Closed preparation. |
| `ccfg-26-slice-shape-policy-correction` | completed | `batches/ccfg-26-slice-shape-policy-correction/dispatch.md` | `batches/ccfg-26-slice-shape-policy-correction/runway.md` | CCFG-26 | Closed preparation. |
| `ccfg-26-execution-state-foundation` | superseded | `batches/ccfg-26-execution-state-foundation/dispatch.md` | `batches/ccfg-26-execution-state-foundation/runway.md` | CCFG-26 | No accepted Slice; WIP preserved under user control; see `superseded.md`. |
| `ccfg-26b-fresh-slice-flight` | superseded | `batches/ccfg-26b-fresh-slice-flight/dispatch.md` | `batches/ccfg-26b-fresh-slice-flight/runway.md` | CCFG-26 | Historical only. |
| `ccfg-26c-bounded-recovery` | candidate | None | None | CCFG-26 | Concept only; no accepted sequence. |
| `ccfg-26d-finalization-flight` | candidate | None | None | CCFG-26 | Concept only; no accepted sequence. |
| `ccfg-26e-closeout-ownership-cutover` | candidate | None | None | CCFG-26 | Concept only; no accepted sequence. |
| `ccfg-30-cross-flight-execution-leases` | completed | `batches/ccfg-30-cross-flight-execution-leases/dispatch.md` | `batches/ccfg-30-cross-flight-execution-leases/runway.md` | CCFG-30 | Closed. |
| `ccfg-31-narrow-live-lease-preflight` | completed | `batches/ccfg-31-narrow-live-lease-preflight/dispatch.md` | `batches/ccfg-31-narrow-live-lease-preflight/runway.md` | CCFG-31 | Closed. |
| `ccfg-32-planning-state-queue-currentness` | completed | `batches/ccfg-32-planning-state-queue-currentness/dispatch.md` | `batches/ccfg-32-planning-state-queue-currentness/runway.md` | CCFG-32 | Closed. |
| `ccfg-33-acceptance-execution-simplification` | completed | `batches/ccfg-33-acceptance-execution-simplification/dispatch.md` | `batches/ccfg-33-acceptance-execution-simplification/runway.md` | CCFG-33 | Closed. |
| `ccfg-34-stable-runway-dogfooding-bootstrap` | completed | `batches/ccfg-34-stable-runway-dogfooding-bootstrap/dispatch.md` | `batches/ccfg-34-stable-runway-dogfooding-bootstrap/runway.md` | CCFG-34 | Temporary policy retained until CCFG-29. |

## Recommended Work Order

1. Start from root and program `CURRENT.md`.
2. Keep the program idle while the preserved candidate WIP overlaps the likely
   CCFG-26 implementation paths.
3. The user decides how to isolate or retain that WIP; no agent modifies it.
4. A later explicit `plan-batch CCFG-26` creates one fresh runway from ADR 0004
   and the reset finding.
5. The replacement plan starts from the OSS product, uses batch-local runtime
   state, limits version 1 to trusted local filesystems, and keeps codex-config
   installation mechanics in a temporary adapter.
6. CCFG-27 through CCFG-29 and all other open rows remain unselected until an
   explicit command chooses them under proven dependencies.

## Closeout Rules

- Close findings only from implementation, validation, review, and same-batch
  reconciliation evidence; planning is not closeout evidence.
- Same-batch closeout clears selected, queued, and active state and selects no
  successor.
- Dogfood adapters record their removal condition and cannot become permanent
  product dependencies by inertia.
- Preserved user-owned WIP remains outside workflow authority until explicit
  user direction changes that disposition.
