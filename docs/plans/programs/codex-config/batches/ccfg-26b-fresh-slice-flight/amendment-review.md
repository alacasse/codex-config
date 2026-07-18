# CCFG-26B Bounded Amendment Independent Planning Review

## Final Result

~~~yaml
interface: batch-plan-amendment-review/v1
reviewer: /root/ccfg26b_fresh_amendment_review
verdict: clean
reviewed_amendment:
  path: docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/amendment.md
  sha256: 2ec8981e8ac6c088d7d5f4435f2638ea94346bd921b04609938e43e29a6787d8
original_evidence:
  dispatch_sha256: 8b29b566fd743af4ecdbe555f1cf66bb29871b081bc25f7aa0fc9780ce1069d8
  queued_runway_sha256: 8da8e0d1b0cd18d75289a1a0954b33078dd17ef6a328d2bb6a46a9404076b5ca
  original_review_sha256: e37e0678c663a44c99b642454fa4fc6b840bc59174c8df6727d10bb02ad2f45f
immutable_baselines:
  toolchain_and_canonical_planning: 8aec9c2bcf87f619012b6dfc748ef46387515298
  candidate_implementation: 5c5ec9d52dd9033daa45f3a200031c152363b62c
amended_scope:
  planning_path_count: 10
  implementation_path_count: 36
  canonical_path_manifest_sha256: 54416bbd581861d54fb30c9693eae1e73cee439f8530ec01f4e24cb991868dd1
selected_slice_count: 2
correction_rounds: 4
corrections: []
blockers: []
implementation_started: false
implementation_authorized_after_state_binding: true
implementation_authorized_for_later_explicit_work_batch: true
queue_mutation_authorized: false
state_binding: complete
successor_selected: false
~~~

The fresh independent reviewer evaluated the exact amended two-slice design,
not only the amendment syntax. It did not edit files, implement code, invoke
work-batch, select or prepare a successor, mutate the queue, or delegate.

## Review Basis

The reviewer read:

- immutable dispatch.md, runway.md, and review.md in this directory;
- exact amendment.md at
  2ec8981e8ac6c088d7d5f4435f2638ea94346bd921b04609938e43e29a6787d8;
- current stable Planning State current and validate evidence;
- program CURRENT.md and LEDGER.md;
- the temporary stable-runway dogfooding policy;
- candidate source at clean exact baseline
  5c5ec9d52dd9033daa45f3a200031c152363b62c;
- current public work-batch, serialized runner phase, validation, transition,
  state, artifact, input-inventory, process-observation, routing, feature
  metadata, and focused test surfaces; and
- candidate planning-runway schema and deterministic plan-batch migration
  evidence validation.

At review time:

~~~yaml
planning_state:
  current: valid
  validate: valid
  selected_dispatch: null
  queued_batch: docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/runway.md
  active_runway: null
  blockers: []
  obligations: []
  implementation_started: false
candidate:
  head: 5c5ec9d52dd9033daa45f3a200031c152363b62c
  worktree: clean
canonical_authoring_head: 9b5b9d4cd9279424c6b75ffc8b28670832d8cc2f
canonical_authoring_note: current review evidence only; the immutable planning snapshot remains unchanged
~~~

Planning State reported only the existing redirect warnings. They are unrelated
to this amendment and are not blockers.

## Scope Binding

The installed cross-checkout helper validated a refreshed authoring context
against the current stable and unchanged candidate heads. It accepted:

- the original eight canonical planning paths plus amendment.md and
  amendment-review.md, for ten planning paths total; and
- the original thirty-five candidate implementation paths plus
  scripts/architecture_program_runner_input_inventory.py, for thirty-six
  implementation paths total.

The exact manifest is the planning_paths and implementation_paths object used
by validate_write_scope, serialized as sorted-key compact JSON. Its SHA-256 is:

~~~text
54416bbd581861d54fb30c9693eae1e73cee439f8530ec01f4e24cb991868dd1
~~~

This refreshed validation is amendment-authoring evidence, not a replacement
for the original immutable planning snapshot or a live execution lease.
Before implementation, work-batch must obtain a fresh live lease and validate
the same amended path ceiling separately.

## Correction History

The reviewer preserved the original review's historical correction record and
performed four new amendment-specific correction rounds.

### Round 1 — Proportionality Baseline

Verdict: correction_required.

The Slice 1 required source and test scope had expanded to include artifact,
environment, run-loop, and state behavior, but the amendment still quoted the
earlier smaller baseline. The corrected exact pre-change set passed:

~~~text
70 tests and 38 subtests in 0.25 seconds
0.41 seconds wall
~~~

The amendment now uses that measured set and retains the 82-scenario catalog's
0.25-second wall baseline.

### Round 2 — Feature Metadata Ownership Residue

Verdict: correction_required.

The first amendment classified the codex-features.json Batch Runway description
as retained support without requiring its unqualified slice-execution claim to
change. The corrected amendment requires:

- work-batch to be described as the successful-slice owner;
- Batch Runway to be described only as temporary CCFG-26C recovery and
  CCFG-26D finalization support;
- the dependency to remain only for those conditioned uses; and
- feature versions and focused tests to update.

### Round 3 — Output-Schema Feasibility

Verdict: correction_required.

The first contract wording required JSON Schema itself to encode all cross-field
status, action, and nullability combinations. The current Codex output-schema
subset rejects oneOf, anyOf, if, then, and else. The corrected amendment splits
ownership:

- the Codex-compatible schema validates exact fields, enums, types,
  requiredness, and structural nullability; and
- deterministic runner validation accepts exactly the four supported
  combinations, validates receipt/state/action consistency, and rejects every
  other structurally valid combination.

Focused tests must prove both layers.

### Round 4 — Truthful Session Observation And Durable Resume

Verdict: correction_required.

The first contract placed coordinator_session_id in the byte-equal work-batch
receipt even though the runner observes the real Codex session only after the
subprocess exits. It also did not bind enough durable evidence for manual
resume. The corrected amendment:

- gives work-batch only preallocated flight and artifact identifiers to echo;
- leaves the work-batch receipt immutable after byte-equality validation;
- uses the existing runner phase telemetry mechanism as a separate
  flight-keyed observation record for actual session ID, token, compaction,
  duration, and exit evidence;
- requires completed flights to have a non-null runner-observed session ID;
- compares runner-observed, not self-reported, session IDs across flights;
- keeps architecture_program_runner_phase_observation.py read-only and outside
  the amended write ceiling; and
- requires completed-slice evidence to bind exact receipt, action, next-slice,
  observation, runner state, manifest, inventory, telemetry, commit paths, and
  digests needed for manual and ordered resume.

The reviewer re-read the final exact amendment after these corrections and
returned clean.

## Substantive Checks

| Check | Result |
|---|---|
| Original dispatch, queued runway, and original review remain immutable | pass |
| Finding, batch identity, source evidence, and baselines remain unchanged | pass |
| Queue remains the same single CCFG-26B runway | pass |
| Exactly two implementation slices and no validation-only third slice | pass |
| Slice 1 is a complete producer-to-persistence flight with durable manual resume | pass |
| Slice 1 performs no automatic relaunch | pass |
| Slice 2 consumes the exact authored action in a fresh same-batch process | pass |
| Slice 2 retains ordered receipts, inventories, manifests, observations, sessions, and commits without overwrite | pass |
| work-batch is the sole successful-slice semantic lifecycle owner | pass |
| Runner is limited to launch, validation, persistence, observation, and mechanical transition | pass |
| No active happy-path Batch Runway caller or silent fallback remains | pass |
| docs/skill-routing-contract.md is required and feature/guidance contradictions are classified | pass |
| Batch Runway recovery/finalization and APR closeout remain bounded read-only support | pass |
| Flight contract contains only current CCFG-26B producers, consumers, and deterministic behavior | pass |
| No closeout action or other future placeholder is reserved | pass |
| Structural schema and cross-field deterministic validation are feasible and separately tested | pass |
| Receipt author facts and runner-observed telemetry are truthfully separated | pass |
| All twelve counterfactuals use the strongest available producer-consumer path | pass |
| Per-slice forecasts include files, lines, owners, subprocesses, commands, runtime, reviewers, agents, and coordinator counts | pass |
| Substantial expansion requires another reviewed amendment | pass |
| migration_evidence is the sole candidate representation | pass |
| Stable vertical_slice evidence is classified as a temporary external overlay | pass |
| Focused validation belongs to its slice; final gates remain batch-level | pass |
| Recovery, finalization, closeout, phase-label migration, deletion, bridge removal, default switch, and successor selection remain deferred | pass |
| CCFG-26C through CCFG-26E and CCFG-27 through CCFG-29 remain unselected | pass |
| No implementation has started | pass |

## Final Execution Basis

Implementation is permitted only through a later explicit stable work-batch
request after canonical state binds this review. The execution basis is:

1. dispatch.md at
   8b29b566fd743af4ecdbe555f1cf66bb29871b081bc25f7aa0fc9780ce1069d8;
2. runway.md at
   8da8e0d1b0cd18d75289a1a0954b33078dd17ef6a328d2bb6a46a9404076b5ca;
3. original review.md at
   e37e0678c663a44c99b642454fa4fc6b840bc59174c8df6727d10bb02ad2f45f;
4. amendment.md at
   2ec8981e8ac6c088d7d5f4435f2638ea94346bd921b04609938e43e29a6787d8;
5. this clean amendment-review.md; and
6. a fresh Planning State diagnostic and strict live lease at execution time.

The later stable invocation executes only the next pending amended
implementation slice and stops under the temporary policy. It does not select,
prepare, or begin another child or successor.

## State Binding Receipt

~~~yaml
status: bound
pre_binding:
  current_sha256: 45ec2cf7b39faa628cd3c9b4e434c01b0a3f3956226de4ae6ebb43c66881a403
  ledger_sha256: 21b6258e97c8f8f07a147d8c04308e289d53006655ab2ebca980dce5c556f5b0
post_binding:
  current_sha256: 946294fed46e18d2da2b1f0ec3e2f92ffb8ddc98a4e7569382f97f3636f6722e
  ledger_sha256: e85094ad90419c8ce1b904fa55a21547cfd450bb2f182443485ae1b9bd860fb1
planning_state:
  current_exit: 0
  validate_exit: 0
  selected_dispatch: null
  queued_batch: docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/runway.md
  active_runway: null
  blockers: []
  obligations: []
  implementation_started: false
  successor_selected: false
warnings:
  - existing redirect_ledger warning for codex-config-architecture-program-runner-findings.md
  - existing redirect_ledger warning for planning-state-tooling-ledger.md
~~~

Canonical CURRENT.md and LEDGER.md now bind this exact amendment and clean
review to the existing queued runway. The queue path did not change, no batch
became active, and no successor was selected or prepared.
