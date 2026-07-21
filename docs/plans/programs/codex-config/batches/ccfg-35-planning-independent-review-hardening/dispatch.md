# CCFG-35 Planning And Independent Review Hardening Dispatch

## Selection

- Batch ID: `ccfg-35-planning-independent-review-hardening`
- Included finding: `CCFG-35. Harden Planning And Independent Review`
- Source ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Source finding:
  `docs/plans/programs/codex-config/findings/planning-and-independent-review-hardening.md`
- Intended artifact state: one exact independently reviewed dispatch/runway pair,
  queued only after the review binds both drafts and reports clean.
- Implementation started: `false`
- Successor selection: forbidden.

## Goal

Harden the reusable public `plan-batch` pipeline so a structurally valid but
semantically unsupported plan cannot receive a clean independent planning
review and reach DEC-038 queue mutation. Preserve Planning State as the owner of
structural currentness and keep semantic judgment with the planner and the
independent planning reviewer.

## Current Basis

- Canonical planning and controlling stable generation:
  `/home/alacasse/projects/codex-config` at
  `f09e2eca6767ac11f6b5d05fd66933001667d0ea` on `master`.
- Candidate implementation generation:
  `/home/alacasse/projects/codex-config-command-owner-redesign` at
  `5c5ec9d52dd9033daa45f3a200031c152363b62c` on
  `implementation/command-owner-redesign`.
- Stable Codex home: `/home/alacasse/.codex`.
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`.
- Installed strict-context helper:
  `/home/alacasse/.codex/scripts/cross_checkout_context.py`, resolving to the
  stable checkout.
- Planning State at selection: `current` and `validate` passed; selected
  dispatch, queued batch, and active runway were all `None`.
- Project slice-shape policy:
  `docs/plans/programs/codex-config/notes/slice-shape-policy.yaml`, with
  `default_shape: vertical`, overrides allowed, and an override reason required.

## Batch Contract

- Batch kind: `mixed-risk` because the batch intentionally narrows which
  planning-review results may authorize queue mutation.
- Validation class: `project-harness-production` with focused planning-owner
  tests per slice and one final command-owner acceptance pass.
- Required execution contract: Batch Runway Standard Execution Contract v2 and
  Registered Agent Result Contract v2.
- Required environment: explicit `cross-checkout-context/v1` using the planning
  snapshot in the runway.
- Canonical planning writes remain in the stable checkout; implementation,
  tests, docs, and candidate installation remain candidate-only.
- Graphify is suspended and is neither an input nor an acceptance requirement.

## Owner Seam

The candidate public `plan-batch` command remains the sole planning owner. It
directly invokes `batch_planner`, independently supplies evidence to
`batch_plan_reviewer`, and calls installed `scripts/plan_batch.py` only after a
clean exact-draft review. `scripts/plan_batch.py` remains the mechanical
pre-queue gate and DEC-038 apply boundary. Planning State remains structural;
Batch Runway remains execution-only; compatibility `create-spec` remains
observation-only.

## Semantic Shape

Use three vertical slices:

1. Establish an evidence-bearing clean-review result and fail closed before
   DEC-038 when applicable semantic conclusions lack bound evidence.
2. Consume that result boundary to enforce substitutive ownership, caller,
   retained-route, forbidden-fallback, failure-path, consumer, terminal-
   condition, and counterfactual assurance.
3. Consume the same boundary for conditional feasibility, compound durable-
   write, intermediate usefulness, smaller-alternative, and execution-cost
   proportionality assurance, then align public docs and installed metadata.

Each slice is a complete planner -> independent reviewer -> deterministic gate
-> behavioral regression path. Do not split role prose from its result consumer
or deterministic tests.

## Approval Gates

Each slice has risk `contract-narrowing` because it makes formerly acceptable
evidence-free or assertion-only planning results non-executable.

- Approval authority: the user.
- Approval action: a later explicit `work-batch` invocation while this exact
  reviewed runway remains queued.
- Required evidence: Planning State is still current and valid, the strict
  live-lease preflight is ready, and any preceding slice is committed, green,
  and reviewed.
- Approval does not authorize unrelated planning-system redesign, a new state
  family, a new agent role, stable-home mutation, or successor selection.

## Included File Areas

Candidate implementation may touch only the minimum necessary subset of:

- `skills/plan-batch/`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `scripts/plan_batch.py`
- existing planning-contract code/schema surfaces only if the accepted record
  must persist in an existing artifact
- focused planning-owner, agent-contract, manifest, schema, and command-owner
  scenario tests and fixtures
- `docs/workflow-guide.md`, `docs/skill-routing-contract.md`, `CONTEXT.md`,
  `README.md`, `codex-features.json`, and `CHANGELOG.md` only where behavior or
  installed versions require alignment.

## Excluded And Deferred

- All findings other than CCFG-35 are excluded.
- CCFG-26 and both descriptive CCFG-26 child candidates remain unselected.
- CCFG-27 through CCFG-29 remain dependency-blocked and unselected.
- No `runway_reviewer` repurposing, no new agent role, and no live-model eval
  infrastructure.
- No APR/Batch Runway planning authority, alternate queue route, runner phase
  redesign, Planning State semantic judgment, new top-level schema family, or
  persistent planning/execution state.
- No Graphify requirement or generated graph authority.

## Stop Conditions

Stop if the current independent planning-review handoff/result boundary cannot
be identified, if a clean review can still be represented by bare semantic
`pass` values without evidence, if deterministic validation is asked to decide
semantic completeness or persuasiveness, if migration-specific ceremony becomes
mandatory for ordinary small plans, if a new state family or agent role is
required, if stable and candidate begin sharing runtime state, or if work
expands into execution/closeout ownership or another ledger finding.

## Expected Runway

`docs/plans/programs/codex-config/batches/ccfg-35-planning-independent-review-hardening/runway.md`
