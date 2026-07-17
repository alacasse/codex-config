---
name: plan-batch
description: Select one bounded ledger finding and queue one independently reviewed batch plan without executing it.
---

# Plan Batch

Use this skill when the user asks to plan the next batch, turn existing ledger
state/work into a runway, or prepare implementation slices. This command
consumes existing ledger state/work. `plan-batch` owns the
complete human-facing planning command: state branching, one-finding selection,
scope shaping, dispatch, runway, risks, approvals, validation profile, exact
review, and queue mutation. It always stops before implementation.
It must not silently create new ledger findings from fresh request text.

Executable work comes only from the canonical program ledger or the exact
selected/queued/active state reported by Planning State. External sources are
evidence only when an
existing ledger row points to them. Do not scan external sources to discover new work.
If no suitable existing
finding exists, stop and tell the user to use `add-to-ledger`.

When routing ambiguity exists, follow `../../docs/skill-routing-contract.md`.

## Command Contract

The command result is one existing-state report, one reviewed queued runway, or
one blocked result. Its stop-before-implementation boundary is unconditional.
If useful work exists outside the ledger, stop and require `add-to-ledger` to
ingest it first.

Requested ledger rows are suitable for direct planning only when the row is
precise enough for one bounded selected dispatch. A row is not suitable when it
mixes evidence gathering, classification, decisions, destructive cleanup,
migration, demotion, or contract narrowing without clear owner, risk, and
acceptance boundaries. `plan-batch` must split, block, or narrow that scope
before any concrete runway is queued.

When selected work carries deletion-test evidence, consume the canonical
deletion-test evidence statuses owned by `dead-surface-audit`. Any local
non-canonical labels must be defined inline as labels only. They must not make
unsupported terms behave like approval gates, cleanup decisions, migration
decisions, demotion decisions, or contract-narrowing decisions.

## Generated Plan Contract

### Generated Spec Checklist

Every generated reviewed plan must include:

- title, purpose, baseline, assumptions, and batch non-goals;
- batch kind and slice risk contract;
- execution and result contract references;
- one selected validation profile and focused commands with status classes;
- execution ledger, semantic slice sections, final validation, and stop
  conditions; and
- any explicitly required strict or pre-creation cross-checkout context.

### Batch Kind And Slice Risk Contract

Every generated dispatch and runway must declare exactly one batch kind:

- `characterization`: collect evidence without cleanup, deletion, narrowing,
  demotion, migration, or ownership changes;
- `decision`: evaluate and record a decision without performing destructive
  cleanup in the same slice unless the batch is `mixed-risk`;
- `migration`: change topology or ownership while preserving the supported
  public contract;
- `destructive-cleanup`: delete, disable, demote, or intentionally remove an
  existing surface; or
- `mixed-risk`: combine evidence, decision, migration, contract-narrowing, or
  destructive work while naming risky slices and approval gates.

Every generated slice that can change an existing surface, ownership boundary,
or supported contract must declare exactly one slice risk class:

- `none`;
- `evidence-only`;
- `decision-only`;
- `migration`;
- `contract-narrowing`; or
- `destructive-cleanup`.

Destructive or contract-narrowing slices require an explicit approval gate
before execution. Name who or what can approve the work and the evidence that
must exist. A `characterization` batch or an `evidence-only` slice must not
include destructive cleanup or contract narrowing. If a batch combines
evidence-only or decision-only work with destructive cleanup, contract
narrowing, or migration, declare the batch kind as `mixed-risk`, name the risky
slices, and list the approval gate for each risky slice.

### Validation Command Status Classes

Every focused validation command in a generated runway must declare exactly one
status class before execution:

- `required-green`: the command is expected to pass now, or the slice explicitly
  owns the remediation that makes it pass before it can gate later work. Use
  this only with current passing evidence, or with a named slice-owned
  remediation path and acceptance criteria that prove the command becomes
  green.
- `known-red-baseline`: the command currently fails. Retain it as diagnostic
  evidence or remediation scope, but do not let it block execution until a
  named slice fixes the failure and promotes it with green evidence.
- `implementation-created`: the command targets a test, file, fixture, tool, or
  artifact that does not exist yet. Name the slice that creates it before the
  command can become a required gate.
- `conditional`: run only when named files, artifacts, metadata, or project
  areas change. State the trigger condition precisely enough for an executor to
  decide whether to run it.
- `diagnostic-only`: use for planning, review, or risk evidence; it is not an
  execution gate unless a later slice explicitly promotes it.

Do not silently promote a known-red command, a missing future-created command,
or a diagnostic command to `required-green`. Promotion requires explicit green
evidence or an explicitly named slice-owned remediation path that makes the
command green before it gates downstream work.

## Required Installed Boundaries

This command uses only:

- `../planning-state/SKILL.md` for semantic currentness through `current` and
  `validate`;
- `../planning-artifacts/SKILL.md` for Layout v1 paths and artifact names;
- the existing installed planning contracts and DEC-038 transaction store;
- the registered `batch_planner` and `batch_plan_reviewer` roles; and
- the installed `scripts/plan_batch.py` deterministic validation/apply boundary.

The command owner directly invokes both roles. Neither role invokes the other,
mutates planning state, or implements work. Do not route planning through a
second workflow owner.

## Explicit Cross-Checkout Pre-Creation Planning

When the selected finding explicitly names `cross-checkout-precreation/v1`,
resolve the installed helper from the active Codex home. Use it to validate the
complete payload and exact intended creation targets while they are absent.
Planning must not create either candidate root. Preserve the validated payload
in the proposed runway. This conditional bridge adds no step for ordinary
single-root or strict cross-checkout batches.

## Explicit Strict Cross-Checkout Planning

When the selected finding explicitly names `cross-checkout-context/v1` or
separate existing roots, require the complete context payload and canonical
planning root, validate them with the installed helper, and preserve both
verbatim in that runway. An absent-target payload cannot satisfy this strict
post-creation contract. This conditional bridge adds no step for ordinary
single-root batches.

## Procedure

1. Resolve the explicit planning root through Planning Artifacts. Run Planning
   State `current` and `validate` against that same root. Stop on any fatal,
   stale, ambiguous, or mismatched diagnostic.
2. Branch on the semantic state before drafting:
   - Active runway: report it and stop without planning or execution.
   - Queued runway: report it and stop without replacement or execution.
   - Selected dispatch: report it and stop unless an exact durable DEC-038
     transaction proves this is recovery of that same selection.
   - Idle: continue with selection.
3. Read the current canonical ledger. Honor an explicit requested finding only
   when it exists, is open, and is precise enough for one bounded batch.
   Otherwise choose exactly one eligible finding. Do not group multiple
   findings. Stop on a missing, repeated, closed, vague, mixed-risk, or
   dependency-blocked finding.
4. Capture the exact current revision/hash, ledger path/hash, finding revision,
   roots, producer identities, and authorized paths for `CURRENT.md`, one
   dispatch, one runway, and one transaction record. Existing dispatch or
   runway paths must not be silently replaced. Canonical planning roots require
   stable generation and explicit canonical mutation authority; temporary and
   fixture roots carry no canonical mutation authority and must resolve outside
   the canonical planning repository.
5. If the selected work explicitly carries cross-checkout context, resolve
   `scripts/cross_checkout_context.py` from the active Codex home, require it to
   resolve below the declared toolchain root, validate the complete versioned
   payload and canonical planning root, and preserve the exact validated
   context in the draft. For pre-creation context, validate the exact absent
   creation targets without creating them. Stop on any mismatch. This
   mechanical step grants no selection, queue, creation, install, generation,
   implementation, or closeout authority.
6. Directly invoke registered `batch_planner` with the exact Planning State and
   ledger basis, selected finding and source evidence, user constraints,
   planning-contract schemas, root/generation context, and validation catalogs.
   Treat that catalog as opaque identifiers: do not resolve an identifier as a
   source path or import another workflow. Require exactly one selected profile
   identifier from that catalog and the complete
   proportionality record: observed failure, invariants, minimum viable change,
   proposed change, justified additions beyond minimum, rejected simpler
   alternatives, and verdict. Require `batch-plan-draft/v1`. A blocked or
   malformed result stops without queue mutation.
7. Check the draft before review:
   - one complete dispatch and one complete runway bind the same single finding,
     batch, roots, producers, and immutable source revisions;
   - the proposed change is the minimum viable change and proportional;
   - a cohesive plan may have one slice; multiple slices each need a concrete
     producer/consumer, risk, validation, migration, or contract boundary;
   - filler decomposition and unrelated expansion block;
   - approvals match, in declared order and without extras, the union of
     dispatch `approval_gates`, residual-complexity scopes, and destructive-
     action scopes; unresolved decisions and missing approvals remain blocked;
   - implementation has not started and successor selection is forbidden.
8. Assemble one canonical independent-review evidence packet in the command
   request. Include exact source contents and digests, explicit user constraints,
   Planning State current/validate diagnostic identities, proportionality,
   ordered approvals, the complete draft, selected dispatch, and both direct
   invocation records. Compute canonical SHA-256 digests of that packet, the
   dispatch, complete draft, and approval record. Supply the packet directly to
   registered `batch_plan_reviewer`; the planner must not select or frame it.
9. Require `batch-plan-review/v1` with all four exact digests. Any added,
   removed, reordered, or changed approval after review requires a fresh
   independent review before queue mutation. On
   `correction_required`, return only the corrections to `batch_planner`, keep
   the same finding and evidence basis, compute new digests, and invoke the
   reviewer independently again. Record material correction history in the
   ephemeral command request. Stop if the same correction repeats against
   an unchanged draft, scope expands, currentness moves, or evidence remains
   unresolved. `blocked` and any non-clean check remain non-executable.
10. Only after a clean exact-draft review and every exact approval gate passes,
    invoke installed `scripts/plan_batch.py` with `plan-batch/v1`. Pass the two
    direct invocation receipts, role results, approvals, immutable Planning
    State and ledger basis, authorized transaction paths, and existing
    planning-contract payloads. The script validates these gates and applies the
    existing four-stage DEC-038 transaction. Do not call the store directly.
11. If DEC-038 was interrupted, resume only the same transaction ID after every
    immutable binding and live Planning State fact matches. Preserve partial
    evidence. Exact completed replay must produce no duplicate effects.
12. Report the selected finding, dispatch, runway, and transaction result. Stop
    before worker delegation, validation execution, commits, implementation,
    closeout, or successor selection.

## Deterministic Boundary Contract

`scripts/plan_batch.py` accepts exactly `interface`, `context`,
`planning_state`, both direct role invocation records and results, `approvals`,
the independent `review_evidence` packet, caller-supplied opaque-ID
`validation_catalog`,
ephemeral `correction_history`, and `transaction`. It writes only the authorized
current, dispatch, runway, and transaction paths after all gates pass. Blocked
or stale drafts write nothing and are not visible as queued or active work.

The planner result is exactly `batch-plan-draft/v1`; the reviewer result is
exactly `batch-plan-review/v1`. The script verifies selected-dispatch, full
draft, exact approval-record, and independent-evidence-packet hashes,
one-finding lineage, the selected catalogued validation profile, semantic slice
rationales, the complete proportionality record, exact approval gates, stop
boundaries, correction history, and transaction inputs before DEC-038 can write.
Agent invocation remains in this skill; the script never invokes roles.

## Stops

- Do not create ledger findings or discover external backlog work.
- Do not select more than one finding or produce more than one runnable batch.
- Do not bypass selected, queued, or active Planning State.
- Do not queue a stale, unresolved, unapproved, unreviewed, corrected-but-not-
  rereviewed, or non-proportional draft.
- Do not add a schema, lifecycle state, persistent draft store, transaction,
  retry token, source adapter, compatibility wrapper, or alternate queue path.
- Do not implement, delegate implementation, commit, close out, reconcile, or
  select successor work.

## Agent-Facing Support

Planning State, Planning Artifacts, the two registered planning roles, existing
planning contracts, and the deterministic installed script support this command.
The command owner retains every planning and stop decision.
