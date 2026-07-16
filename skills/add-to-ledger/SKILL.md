---
name: add-to-ledger
description: Add plain-text findings or GitHub issues to a project planning ledger without selecting, planning, or executing a batch. Use for fresh work requests, review findings, bugs, and cleanup needs that must become durable ledger state first.
---

# Add To Ledger

Treat this skill as the human-facing owner of ledger intake. Support only
`plain_text` and `github_issue` sources. Collect human-language proposals,
invoke the installed deterministic owner once, report its compact result, and
stop before downstream planning.

This explicit ingestion boundary accepts fresh user-provided work/finding text
and GitHub issues. Unsupported external tickets and every other source type
block in v1 without a ledger write.

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: add-to-ledger
  audience: human-command-owner
producer:
  toolchain_generation: candidate
  toolchain_commit: b38570bcd97b2584f3828abcd395b0f45ed91e58
  schema_version: skill-contract/v1
purpose: >-
  Convert supported human or GitHub intake into one atomic, provenance-bound
  planning-ledger decision without exposing mechanical store identity.
owns:
  decisions:
    - intake_eligibility
    - source_canonicalization
    - source_identity
    - finding_normalization
    - duplicate_decision
    - finding_id_allocation
    - store_request_preparation
    - private_operation_identity
  durable_facts:
    - finding_source_provenance
reads:
  required:
    - controlling_generation
    - canonical_planning_repository
    - planning_root
    - planning_ledger
    - explicit_source_request
  conditional:
    - project_authorized_finding_namespace
writes:
  - atomic_planning_finding_mutation
requires:
  mechanisms:
    - planning_contract_store
  evidence_skills: []
delegates:
  - responsibility: atomic_ledger_application
    target: planning_contract_store
forbids:
  - public_idempotency_identity
  - unsupported_source_adapter
  - cross_source_merge
  - lifecycle_or_dependency_change
  - batch_selection
  - dispatch_creation
  - runway_creation
  - implementation
  - finding_closeout
outputs:
  one_of:
    - applied_intake_result
    - no_op_intake_result
    - blocked_intake_result
stops_when:
  - unsupported_or_ambiguous_input
  - unauthorized_mutation_root
  - malformed_finding_namespace
  - stale_ledger_snapshot
  - compact_result_returned
references: []
```

## Procedure

1. Resolve the active toolchain generation and source commit, canonical
   planning repository and commit, project planning root, target ledger, and
   mutation authorization from the controlling session and project
   instructions. Never infer authorization from the request text.
2. Collect one or more independent `plain_text` or `github_issue` sources. For
   each source, draft only a title, scope summary, included and excluded items,
   evidence pointers, and next-action command and condition.
3. Block before invocation when the request is unsupported or ambiguous, asks
   for a cross-source merge, or implies lifecycle, dependency, destructive,
   migration, demotion, or contract-narrowing changes.
4. Send one complete private JSON request on stdin to the installed
   `scripts/add_to_ledger.py`. Set `interface` to `add-to-ledger/v1` and include
   the exact context and input fields below. Do not generate or request a
   digest, idempotency key, request ID, replay token, ledger revision, or file
   hash.
5. Return the script's compact result. Summarize source evidence if useful, but
   do not echo or durably store complete raw input outside the finding. Stop
   regardless of whether the result is applied, an exact replay, a no-op, or a
   block.

## Private Transport

The `context` object contains exactly:

- `toolchain_generation`, `toolchain_commit`, and absolute `toolchain_root`;
- absolute `canonical_planning_repository_root` and its current
  `canonical_planning_commit`;
- absolute `planning_root` and `ledger_path`;
- `operation_root_kind`: `canonical`, `temporary`, or `fixture`;
- `canonical_state_mutation_allowed` from the controlling generation; and
- `project_namespace`, which is null unless controlling project configuration
  authorizes a namespace needed by an empty ledger.

Each `inputs` item contains exactly:

- `source`: either `{type: plain_text, text: ...}` or
  `{type: github_issue, owner: ..., repository: ..., number: ..., title: ...,
  body: ...}`;
- `title`;
- `scope`: `summary`, `included`, and `excluded`;
- `evidence_pointers`;
- `next_action`: `command` and `condition`;
- `explicit_target_finding_id`, normally null; and
- `non_intake_changes`, normally empty and populated only to force a safe
  block on a detected non-intake request.

This transport is an installed skill-to-script mechanism, not a public user
interface or reusable intake schema. The script reads one complete valid
ledger snapshot, derives source identities and CAS facts internally, resolves
all decisions and allocations together, derives a private key from the exact
prepared store request, and invokes the unchanged ledger store atomically.

## Decision Boundary

Create when the exact source identity is absent. Update only the single finding
with the same source identity and only for intake-owned fields. Return a no-op
when normalized intake content is unchanged; existing evidence that is already
a superset is unchanged. Block duplicate source mappings, conflicting repeated
inputs, unsupported adapters, malformed or mixed namespaces, stale CAS,
unauthorized roots, and every explicit-target cross-source merge.

Similar titles from different source identities remain independent findings.
Never perform fuzzy matching. Never select a batch, create a dispatch or
runway, execute implementation, close the finding, or choose successor work.
