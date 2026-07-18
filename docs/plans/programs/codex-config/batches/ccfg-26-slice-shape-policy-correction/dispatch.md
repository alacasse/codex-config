# CCFG-26 Slice-Shape Policy Correction Dispatch

## Selection

- Batch ID: `ccfg-26-slice-shape-policy-correction`
- Selection outcome: `selected for exact planning review`
- Queue target: exactly one `queued` runway after a clean independent review
- Covered finding: CCFG-26 corrective preparation from GitHub issue #66
- Finding state entering the batch: `Prepared`
- Source program ledger: `../../LEDGER.md`
- Source direction: `../../findings/slice-shape-policy-direction.md`
- Expected runway path: `runway.md`
- Planning root: `../../../..`
- Implementation target:
  `/home/alacasse/projects/codex-config-command-owner-redesign`

Planning State `current` and `validate` reported an idle, valid program with no
selected dispatch, queued batch, active runway, blocker, or obligation. This
explicit `plan-batch` request selects only the issue #66 correction. CCFG-26A
remains completed historical evidence; CCFG-26B through CCFG-26E remain
unselected.

## Authoritative Sources

- CCFG-26 and the candidate batch row in `../../LEDGER.md`.
- `../../findings/slice-shape-policy-direction.md`.
- `../../notes/stable-runway-dogfooding-policy.md`.
- CCFG-26A closeout at
  `../ccfg-26a-permanent-vertical-runway-contract/closeout.md`.
- COR-009 at accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.

The completed CCFG-26A dispatch, runway, review, and closeout are historical
evidence only. They must not be reopened, rewritten, executed, or treated as
the current representation contract.

## Goal

Correct the candidate planning contract before CCFG-26B by producing one
complete planning scenario:

```text
project-owned slice-shape-policy/v1
  -> plan-batch resolves one exact policy
  -> batch_planner selects the default vertical shape
  -> batch_plan_reviewer checks the same policy independently
  -> deterministic validation proves policy consistency
  -> planning-runway/v1 persists each slice's selected shape
  -> a justified horizontal override is accepted
  -> disabled or unjustified overrides are rejected
  -> migration evidence remains independently risk-gated
```

The exact project-owned policy instance belongs at
`../../notes/slice-shape-policy.md` and is referenced from the active program
`../../CURRENT.md`. Reusable workflow owners consume the resolved policy; they
must not hard-code the codex-config path or expand Planning State into a new
configuration owner.

Minimum policy payload:

```yaml
schema: slice-shape-policy/v1
default_shape: vertical
allow_override: true
require_override_reason: true
```

Every new runway slice persists:

```yaml
shape:
  selected: vertical | horizontal
  override_reason: null | non-empty string
```

Migration-specific ownership evidence moves beside `shape` under
`migration_evidence` and remains conditional on `risk: migration`. The
extension preserves exactly `starting_scenario`, `durable_result`,
`owner_before`, `owner_after`, `migrated_callers`, `focused_validation`,
`independently_usable_state`, `rollback_boundary`, `temporary_residue`, and
`ownership_coexistence`; the separate `migration_matrix` remains
coexistence-consistent. Selected shape never depends on risk.

## Batch Kind, Slice Risk, And Approval

- Batch kind: `mixed-risk`.
- Slice 1 risk: `contract-narrowing`.
- Selected shape: `vertical`; no override is used.
- Approval gate: GitHub issue #66, the amended CCFG-26 ledger row, the accepted
  direction note, and this explicit `plan-batch` request authorize replacing
  the current migration-coupled `planning-runway/v1` slice representation
  directly, without a historical compatibility reader or archived-runway
  migration.
- The gate does not authorize a second artifact identity, a generic
  configuration framework, execution-owner work, issue #59/#61 behavior,
  bridge changes, stable-home changes, or successor selection.

## One-Slice Decision

Policy resolution, planner authoring, independent review, deterministic
enforcement, schema persistence, and focused proof form one planning
transaction. Splitting policy declaration from its consumers would leave an
inert or contradictory intermediate contract that another owner could not
author, validate, or review. Final-range validation remains a batch gate, not a
second implementation slice.

## Scope Ceiling

Canonical planning surfaces:

- `../../CURRENT.md`
- `../../LEDGER.md`
- `../../notes/slice-shape-policy.md`
- this batch's `dispatch.md`, `runway.md`, `review.md`,
  `completed-slices.md`, and `closeout.md`

Candidate implementation surfaces:

- `skills/plan-batch/**`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `scripts/plan_batch.py`
- `schemas/slice-shape-policy-v1.schema.json`
- `schemas/planning-runway-v1.schema.json`
- focused plan-batch, planning-contract, registered-agent, manifest, and
  behavioral-scenario tests
- associated planning-contract and command-owner fixtures
- `codex-features.json`
- `CHANGELOG.md`

`scripts/planning_contract.py` is conditional and may change only when a
focused failing contract test proves the existing artifact validator must
consume the new current-runway fields. Exact allowed paths are an upper ceiling,
not a requirement to touch every file.

## Validation Class

Use `project-harness-production`. Per-slice validation stays focused on the
single planning scenario. Exact-commit command-owner acceptance, candidate
installation, stable-home comparison, and final independent review remain
final batch gates.

## Stop Conditions

- Stop if any owner hard-codes a default instead of consuming the one resolved
  policy.
- Stop if deterministic validation attempts to judge whether an override reason
  is persuasive.
- Stop if migration evidence is weakened, remains named as the shape selector,
  or still determines shape.
- Stop if historical compatibility, archived-runway migration, a second
  dialect, or a generic configuration framework is introduced.
- Stop if the work needs `work-batch` execution, recovery, finalization,
  closeout, reconciliation, runner, bridge, or default-generation changes.
- Stop if CCFG-26A is reopened or CCFG-26B through CCFG-26E are selected,
  prepared, queued, or begun.
- Stop if final validation becomes an implementation slice.
- Stop on any path outside the exact planning or candidate ceiling, any stable
  default-home mutation, or any failed strict cross-checkout check.
