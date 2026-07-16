# CCFG-24A `add-to-ledger/v1` Decision Amendment

## Status

- Status: accepted CCFG-24A implementation decision.
- Finding: CCFG-24 remains one `Pending` finding.
- Refines DEC-037 without changing `ledger-store/v1`.
- Resolves the blocked CCFG-24A decision attempt from 2026-07-16.
- Scope: preparation only. CCFG-24B and CCFG-25 remain unselected.

## Decision Summary

The failed attempt asked the apply-only store to distinguish complete upstream
intake requests after they had collapsed to the same mechanical apply request.
That was the wrong boundary.

`add-to-ledger/v1` owns source semantics and prepares one exact store request.
It derives the store idempotency key internally from that prepared request.
`ledger-store/v1` continues to own only CAS, atomic application, durable receipt,
and exact replay of the same mechanical request.

The human-facing command never asks the user for a SHA-256 digest, idempotency
key, request ID, replay token, JSON envelope, ledger revision, or file hash.

## Bounded V1 Scope

CCFG-24A v1 supports only:

1. `plain_text`
2. `github_issue`

Deferred from CCFG-24A:

- generic external-ticket adapters;
- Git-file and standalone-file ingestion;
- universal URL or timestamp canonicalization;
- cross-source merge and secondary-source provenance;
- fuzzy, title-similarity, stemming, or embedding-based duplicate detection;
- a public intake request schema or reusable ingestion framework.

An unsupported source or requested cross-source merge blocks without writing.

## Command Boundary

`add-to-ledger/v1` performs this sequence:

1. validate the controlling generation, repository roots, planning root, ledger
   path, and mutation authorization;
2. read one complete schema-valid ledger snapshot with revision and file hash;
3. canonicalize the supported source;
4. normalize the proposed finding fields;
5. decide `create`, `update`, `no-op`, or `block`;
6. allocate all new IDs from the same snapshot;
7. prepare one exact atomic `apply_ledger_decision` request;
8. derive the private idempotency key from that prepared request;
9. call the unchanged store once, or retry only that identical prepared request;
10. return a compact command result and stop before planning downstream work.

The installed skill owns human-language collection and proposal drafting. The
installed script owns validation, canonicalization, decisions, ID allocation,
store request preparation, invocation, and machine-readable results.

A private stdin/stdout JSON transport between the installed skill and script is
allowed. It is not a public user interface or reusable schema.

## Invocation Authority

Before reading for mutation, the command must bind and validate:

- toolchain generation and commit;
- canonical planning repository root and commit;
- planning root;
- ledger path;
- operation root kind: `canonical`, `temporary`, or `fixture`;
- whether canonical-state mutation is authorized.

The ledger path must resolve under the declared planning root without an escape.
Canonical mutation requires explicit authorization supplied by the controlling
generation; the command cannot grant it to itself.

During CCFG-24A, candidate code and candidate-installed validation use only
`temporary` or `fixture` ledgers outside the canonical planning repository with
canonical mutation disabled.

The script reads the ledger and internally appends the observed revision and
file hash to the prepared operation. The human and installed skill do not supply
those values.

## Supported Sources

### `plain_text`

Input is user-provided text plus a concise title and proposal fields collected by
the skill. The command normalizes text to Unicode NFC, LF line endings, trimmed
outer blank lines, and removed trailing spaces or tabs per line.

The command computes internally:

- source identity: `text:sha256:<full-content-digest>`;
- source location: `inline-text`;
- source revision token: first 40 lowercase hexadecimal characters of the
  canonical source digest.

The token satisfies the existing `planning-finding/v1` provenance field; it is a
source revision token, not a Git commit claim.

### `github_issue`

Input contains GitHub owner, repository, positive issue number, title, and body.
Timestamps, query parameters, and fragments are excluded from v1 identity and
semantic comparison.

The command computes internally:

- source identity: `github-issue:github.com/<owner>/<repo>#<number>` with
  lowercase owner and repository;
- source location: `https://github.com/<owner>/<repo>/issues/<number>`;
- source revision token: first 40 lowercase hexadecimal characters of SHA-256
  over canonical owner, repository, issue number, normalized title, and body.

The human supplies no hash. The source revision token is not presented as a Git
commit.

## Finding Normalization

Only intake-owned fields participate in semantic comparison:

- source identity, source revision token, and source location;
- title;
- scope summary, included items, and excluded items;
- evidence pointers;
- next-action command and condition.

Single-line values are NFC-normalized, trimmed, and collapse ASCII whitespace to
one space. Compared lists reject empty items, remove exact duplicates, and sort
by Unicode code-point order. Evidence is append-only: an existing superset does
not cause an update.

Lifecycle, dependencies, finding ID, and existing finding revision are not
intake-owned. A source that implies lifecycle, dependency, destructive,
migration, demotion, or contract-narrowing changes blocks.

## Decision Matrix

Build an exact source index from `provenance.source_id`.

| Condition | Decision |
|---|---|
| Source identity is absent from the ledger | `create` |
| Source identity maps to one finding and normalized intake-owned content is unchanged | `no-op` |
| Source identity maps to one finding and only intake-owned content changed | `update` |
| Source identity maps to multiple findings | `block` |
| Different source identity names an explicit existing target | `block` in CCFG-24A v1 |
| Source type is unsupported or proposal is ambiguous | `block` |

No fuzzy matching is performed. Similar titles with different source identities
create separate findings unless a later accepted version adds a bounded merge
contract.

A `block` anywhere blocks the whole atomic intake and the store is not called.
A multi-source request may contain only independent creates, updates, and no-ops;
multiple inputs for the same source identity must be equivalent after
canonicalization or the whole request blocks.

## Finding ID Allocation

Allocation uses the complete CAS-bound snapshot.

- Existing IDs must all match one `<PREFIX>-<positive-integer>` namespace.
- Malformed IDs, mixed prefixes, duplicate numeric slots, zero, or ambiguity
  block the whole intake.
- An empty ledger requires an explicit project-authorized namespace supplied by
  controlling configuration, not invented from user text.
- Resolve all decisions before allocation.
- Sort creates by canonical source identity.
- Allocate consecutive IDs after the maximum existing suffix; do not fill gaps.
- One stale or concurrent snapshot causes the store CAS to reject the entire
  request without writing.

## Internal Idempotency

After decisions and allocation, the command derives the key from the exact
mechanical store request, excluding the key itself:

- ledger path relative to the bound planning root;
- expected ledger revision and file hash;
- action;
- canonical finding mutations sorted by finding ID;
- touched finding revisions sorted by finding ID.

Canonical encoding is UTF-8 JSON with sorted mapping keys and no insignificant
whitespace. The private key is:

```text
add-to-ledger/v1:<sha256-of-canonical-prepared-store-request>
```

An interrupted retry that retains the same prepared operation derives the same
key and reaches the store's durable `exact_replay`. If that prepared operation
is lost, a later human request is a new semantic evaluation against the current
ledger and may produce a new `no-op` receipt.

No public retry identity, sidecar replay database, second store, fake finding
touch, or artificial mutation is permitted.

## Result And Stop Boundary

The command result reports outcome, source identity and action per input,
affected finding IDs, internally observed ledger facts, private operation
digest, store outcome and receipt, write status, and any blocker.

The result may summarize source evidence but must not echo or durably store the
complete raw user input.

After any outcome, the command stops. It must not select a batch, create a
dispatch or runway, execute work, close a finding, or select successor work.

## Consequences For CCFG-24A

- `ledger-store/v1`, DEC-037, `scripts/planning_contract.py`, and planning schemas
  remain unchanged.
- Slice 1 starts directly with bounded owner implementation.
- Direct and installed validation use temporary or fixture ledgers only.
- Cross-source merge and the three deferred adapter families are not acceptance
  requirements for CCFG-24A.
- Successful CCFG-24A closeout may mark CCFG-24 `Prepared`, not `Closed`.
