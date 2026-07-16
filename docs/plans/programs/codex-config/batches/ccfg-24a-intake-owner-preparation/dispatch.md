# CCFG-24A Intake Owner Preparation Dispatch

## Selection

- Batch ID: `ccfg-24a-intake-owner-preparation`
- Batch state: `queued`
- Source finding: CCFG-24, Transfer Intake Ownership to `add-to-ledger`
- Accepted source: COR-007 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Two-batch boundary:
  `../../findings/ccfg-24-two-batch-execution-amendment.md`
- Accepted implementation decisions:
  `../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`
- Historical failed attempt: `execution-report.md` and stable commits
  `33f7adf`, `c087024`, and `199f4a9`
- Current runway: `runway.md`

## Goal

Prepare and prove one bounded candidate `add-to-ledger/v1` owner that:

- accepts plain user text and GitHub issues without public digest or replay fields;
- owns exact source identity, normalization, create/update/no-op/block decisions,
  complete-snapshot ID allocation, and private store-key derivation;
- calls the unchanged apply-only `ledger-store/v1`;
- is candidate-installed and tested only against temporary or fixture ledgers;
- becomes the primary acceptance path for the relevant intake scenarios;
- leaves compact cost and retained-surface evidence for later cutover planning.

Successful closeout leaves CCFG-24 `Prepared`, not `Closed`.

## Included Work

1. Implement the real owner for only `plain_text` and `github_issue`.
2. Prove create, atomic multi-create, same-source no-op, same-source update,
   unsupported/ambiguous block, stale CAS, and exact prepared-operation retry.
3. Register and candidate-install only `add-to-ledger` and the neutral
   `planning-contracts` mechanism after clean review.
4. Bind the relevant CCFG-23 intake scenarios to the installed owner.
5. Inventory every retained APR, `legacy-removal`, and CCFG-23 intake surface
   with caller, reason, removal owner, and removal condition.
6. Record duration, context when available, test-process count, changed-file
   count, line delta, and diff size.

## Explicitly Deferred

- Generic external-ticket, Git-file, and standalone-file adapters.
- Cross-source merge and secondary-source provenance.
- Universal URL/timestamp canonicalization and fuzzy duplicate matching.
- Fixture/helper deletion.
- APR or `legacy-removal` narrowing.
- Canonical planning mutation by candidate code or candidate-installed tests.
- Stable-home installation or default-generation changes.
- Final CCFG-24 cutover, any CCFG-24B artifact, and any CCFG-25 work.

## Batch Kind And Slice Shape

- Batch kind: `migration`.
- Slice 1: implement, directly prove, register, and candidate-install the bounded
  owner over the unchanged store.
- Slice 2: bind the installed owner to intake scenarios and collect preparation
  and retained-surface evidence.

`1 -> 2`: Slice 1 produces a reviewed installed owner that works against
non-canonical ledgers. Slice 2 consumes that exact owner in the broader harness.
Old intake paths remain unchanged, so the intermediate state is rollback-safe.

## Owner And Store Boundary

- `add-to-ledger/v1` owns source semantics and mutation preparation.
- `ledger-store/v1` owns only exact apply replay, CAS, revision checks,
  deterministic rendering, atomic replacement, and its receipt.
- `scripts/planning_contract.py`, planning schemas, APR, `legacy-removal`,
  `plan-batch`, `work-batch`, and Batch Runway support remain semantically
  unchanged.
- No public SHA-256, idempotency key, request ID, or replay token is permitted.

## Cross-Checkout Guardrails

- Stable toolchain and canonical planning repository:
  `/home/alacasse/projects/codex-config`
- Candidate implementation repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Stable Codex home: `/home/alacasse/.codex`
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`
- Interface: `cross-checkout-context/v1`

Every execution startup and handoff requires fresh Planning State and strict
cross-checkout validation. Candidate code and installed validation use only
`temporary` or `fixture` ledgers with canonical mutation disabled.

## Validation And Review

- Runway density: `full-runway` because the batch changes a human-facing command
  owner and installs it into the candidate home.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`
- Every test-changing slice receives independent review and delta-only
  `test-quality-review`.
- Slice 1 and the final range receive `import_topology_reviewer`.
- Slice 2 receives `dead-surface-audit` only for retained-surface inventory;
  deletion is forbidden.

## Closeout Contract

Closeout must record the accepted decision path, candidate commit range,
installed links, direct and scenario validation, measured cost, and complete
retained-surface inventory. It marks CCFG-24 `Prepared`, clears same-batch state,
and stops without selecting CCFG-24B or CCFG-25.

## Stop Conditions

- Stop if implementation requires a public caller-supplied replay identity.
- Stop if DEC-037, `ledger-store/v1`, or a planning schema must change.
- Stop if work expands beyond `plain_text` and `github_issue`.
- Stop if a cross-source merge is required instead of blocking.
- Stop if candidate code can mutate canonical planning state.
- Stop on stable-home mutation, strict-context mismatch, or repository movement.
- Stop if old intake paths must be deleted or narrowed to turn validation green.
- Stop if work enters CCFG-24B or CCFG-25.
- Stop after same-batch closeout with CCFG-24 `Prepared`.
