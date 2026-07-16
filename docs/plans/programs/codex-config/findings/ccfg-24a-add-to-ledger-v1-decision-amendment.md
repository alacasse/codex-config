# CCFG-24A `add-to-ledger/v1` Decision Amendment

## Status And Authority

- Status: accepted CCFG-24A implementation decision.
- Finding: CCFG-24 remains one `Pending` finding.
- Refines: DEC-037 without changing `ledger-store/v1`.
- Resolves: the CCFG-24A Slice 1 blocker recorded on 2026-07-16.
- Scope: the preparation batch only. CCFG-24B and CCFG-25 remain unselected.

The earlier attempt correctly proved that `ledger-store/v1` cannot distinguish
different upstream intake requests that collapse to the same apply request. The
planning error was requiring the apply-only store to make that distinction.
DEC-037 binds idempotency to the exact mechanical apply request received by the
store; it does not require the store to persist or interpret the complete raw
intake request.

The human-facing command accepts source material or a reference to work. It
does not accept a SHA-256 digest, idempotency key, request ID, replay token, or
equivalent retry identity.

## Command Boundary

`add-to-ledger/v1` owns this sequence:

1. validate the invocation authority and path containment;
2. read one complete canonical ledger snapshot;
3. canonicalize every supported source;
4. normalize proposed finding content;
5. decide `create`, `update`, `merge`, `no-op`, or `block`;
6. allocate all new IDs from the same snapshot;
7. prepare one exact atomic `ledger-store/v1` apply request;
8. derive the internal idempotency key from that prepared request;
9. call the unchanged apply-only store once, retrying only the same prepared
   request when recovery is required;
10. return a command receipt and stop without planning downstream work.

The store continues to own mechanical schema checks, whole-ledger CAS, touched
finding revisions, deterministic rendering, atomic replacement, exact apply
replay, and its durable receipt. The command owner continues to own every
semantic intake decision.

## Skill-To-Script Transport And Result

The installed `SKILL.md` owns human-language interaction and source collection.
It invokes the installed script through this private process boundary:

```text
<installed-python> <installed-add-to-ledger-root>/scripts/add_to_ledger.py apply --request-json -
```

Stdin contains exactly one UTF-8 JSON object matching the request portion of
the invocation fields below. The skill constructs the authority and source
fields; the script appends the observed ledger revision and file hash after its
read. The human does not write JSON or supply mechanical hashes or retry
identity. The process reads no request fields from environment variables.
Stdout contains exactly one UTF-8 JSON result object; progress and diagnostics
use stderr. This private transport is part of the command owner and does not
create a public intake schema or reusable ingestion framework.

The result shape is:

```yaml
interface: add-to-ledger-result/v1
outcome: completed | blocked | protocol_error
semantic_decisions:
  - source_identity: string
    input_positions: [non-negative-integer]
    action: create | update | merge | no-op | block
    finding_id: string | null
ledger_before:
  revision: integer | null
  file_hash: sha256 | null
prepared_operation_digest: sha256 | null
store:
  called: true | false
  action: create | update | merge | no-op | reconcile | null
  outcome: applied | exact_replay | rejected | null
  receipt: object | null
wrote_ledger: true | false
blocker:
  code: string | null
  message: string | null
```

Exit `0` means `completed` with a validated store receipt. Exit `1` means a
semantic, authority, unsupported-source, ambiguity, stale-CAS, or store
rejection block; it must report a blocker and no accepted ledger write. Exit
`2` means malformed internal transport or an unavailable required mechanism;
it returns `protocol_error` when serialization is still possible. Results never
echo the complete raw source envelope.

If any per-source decision is `block`, the entire atomic intake blocks and the
store is not called. Otherwise the store action is the common semantic action
when every source has the same action. A mixture of supported non-blocking
actions uses the store's mechanical `reconcile` action while the command receipt
retains every per-source semantic decision. No-op sources contribute no finding
mutation or touched revision.

Before ID allocation, the command resolves every canonical source identity and
coalesces the invocation deterministically:

- retain input position only for receipt correlation; input position does not
  affect source identity, semantic decisions, mutations, or the internal key;
- collapse repeated occurrences of one source identity only when canonical
  source material, normalized proposal, and explicit target are identical, and
  map every collapsed input position to the one receipt decision;
- block the whole invocation when repeated occurrences of one source identity
  disagree on revision material, proposal, or explicit target;
- require every explicit target to exist in the snapshot; a source cannot
  target a finding allocated by the same invocation;
- group decisions by existing target. A group containing more than one
  substantive `update`, or an `update` plus any other source, blocks. Multiple
  distinct sources may merge into one target only when their normalized title,
  scope, and next action all equal the existing finding; combine their
  effective evidence contributions into one sorted, deduplicated, append-only
  mutation and one touched-revision increment. A group of semantic no-ops emits
  no mutation;
- sort the resulting target groups by finding ID, then allocate IDs for
  remaining creates from the complete snapshot in canonical source-identity
  order. Distinct target groups become one atomic store request.

These rules make duplicate inputs, incompatible overlap, and multi-source
aggregation explicit. The command blocks rather than choosing a winner when a
group cannot satisfy them.

## Invocation And Canonical Mutation Authority

The command authority envelope binds generation, repository, root, path, and
mutation authorization before any canonical read. After the read, the command
adds the observed revision and file hash and freezes the complete internal
invocation before it makes or applies a mutation decision:

```yaml
interface: add-to-ledger/v1
toolchain_generation: stable | candidate
toolchain_commit: full-git-sha
canonical_planning_repository_root: absolute-path
canonical_planning_repository_commit: full-git-sha
planning_root: absolute-path
ledger_path: absolute-path
operation_root_kind: canonical | temporary | fixture
expected_ledger_revision: non-negative-integer
expected_ledger_file_hash: sha256
canonical_state_mutation_allowed: true | false
finding_namespace: optional-uppercase-prefix
sources:
  - source: supported-adapter-input
    proposal:
      title: string
      scope:
        summary: string
        included: [string]
        excluded: [string]
      evidence_pointers: [string]
      next_action:
        command: string
        condition: string
    explicit_target_finding_id: string | null
```

`expected_ledger_revision` and `expected_ledger_file_hash` are internal
script-appended fields and are absent from stdin. The command, not the skill or
human, obtains them from the snapshot it reads. The prepared apply request must
carry those exact facts.

Before applying:

- resolve roots and the ledger path without following an escape outside the
  declared roots;
- require `ledger_path` to resolve under `planning_root`;
- require the validated toolchain generation and commit to match the invocation;
- when canonical mutation is true, require `planning_root` to resolve under
  `canonical_planning_repository_root`, require `operation_root_kind` to be
  `canonical`, and require the canonical planning repository commit to match
  the authorized context used for the read;
- when canonical mutation is false, require `operation_root_kind` to be
  `temporary` or `fixture` and treat the bound `planning_root` itself as the
  complete authorized noncanonical root; it and `ledger_path` must resolve
  outside the canonical planning repository;
- reject every canonical read-for-mutation or write unless
  `canonical_state_mutation_allowed` is true;
- reject any snapshot whose observed revision or SHA-256 file hash differs from
  the bound values.

The authorization flag is an input from the controlling generation and
cross-checkout policy; the command owner does not grant it to itself. During
CCFG-24A, candidate workers and the candidate-installed command use only
temporary or fixture planning roots and ledgers with canonical mutation false.
They must not read for mutation or write the canonical planning ledger. Final
product-command mutation of canonical planning state remains cutover work
outside CCFG-24A; this does not prohibit the stable coordinator from writing
the same-batch execution ledger and closeout artifacts under the controlling
`work-batch` contract.

The installed skill constructs each `proposal` from the supplied source
material before invoking the script. This is the command owner's explicit
semantic input, not source identity. The script never invents title, scope,
evidence, next action, or target identity from a content hash. It normalizes and
validates the proposal, rejects destructive or lifecycle implications outside
intake ownership, and applies the exact decision rules below. Issue/ticket
proposals use the canonical source title as `proposal.title`; other adapters
require the skill to provide a title. The human may name a target in natural
language, but the skill resolves it to `explicit_target_finding_id`; absence is
JSON `null`.

## Internal Idempotency

### Prepared apply operation

The command creates this key material after all semantic decisions and ID
allocation are complete:

```yaml
store_interface: ledger-store/v1
operation: apply_ledger_decision
ledger_path: canonical-path-relative-to-planning-root
expected_revision: snapshot-logical-revision
expected_file_hash: snapshot-sha256
action: create | update | merge | no-op | reconcile
finding_mutations: canonical-list-sorted-by-finding-id
touched_finding_revisions: canonical-map-sorted-by-finding-id
```

Canonical encoding is UTF-8 JSON with mapping keys sorted, no insignificant
whitespace, JSON strings preserved after the normalization rules below, and
arrays preserved in their already canonical order. The internal key is:

```text
add-to-ledger/v1:<sha256-lowercase-hex-of-canonical-key-material>
```

The idempotency key itself is excluded from its derivation. Raw human wording,
transport metadata, wall-clock time, process IDs, temporary paths, invocation
UUIDs, request IDs, replay tokens, command-receipt fields, and any upstream
fields not present in the prepared apply operation are also excluded.

Because expected revision, expected file hash, action, mutations, and touched
revisions are included, an interrupted retry that still owns the same prepared
apply operation derives the same key and resubmits byte-for-byte equivalent
store inputs. The store then returns its durable `exact_replay` receipt without
reapplying the mutation.

If the process loses the prepared operation, a later human invocation is a new
semantic evaluation. It reads the current ledger and may prepare a new `no-op`
with a new snapshot-bound key and command receipt. It does not reconstruct or
pretend to replay the earlier raw intake request. No public retry identity,
sidecar replay database, second store, fake finding touch, or artificial
finding mutation is permitted.

### Two distinct meanings

- Semantic duplicate detection asks whether canonical source identity and
  normalized finding content map to existing work. `add-to-ledger/v1` owns it.
- Mechanical exact replay asks whether one internal key is already bound to the
  exact prepared apply request. `ledger-store/v1` owns it under DEC-037.

Different upstream sources may legitimately produce the same mechanical no-op
shape. The store is not required to distinguish their raw envelopes. The
command receipt still reports the current semantic decision and source identity.

## Supported V1 Source Adapters

All source text is Unicode NFC. Text decoding must be explicit UTF-8; invalid
input blocks. Line endings become LF, a leading BOM is removed, trailing ASCII
space and tab are removed per line, and leading or trailing blank lines are
removed. Internal paragraph whitespace otherwise remains significant.

Each raw adapter input is converted first to this canonical source material,
which deliberately excludes all derived revision fields:

```yaml
adapter: one-of-the-names-below
source_identity: stable-adapter-specific-string
source_location: canonical-url-or-label
content_sha256: 64-lowercase-hex
title: normalized-text | null
body: normalized-text
adapter_metadata: adapter-specific-canonical-object
```

Canonical encoding is UTF-8 JSON with mapping keys sorted, no insignificant
whitespace, lowercase hexadecimal digests, and adapter metadata fields named
below. Optional fields are omitted rather than emitted as empty values. For
non-Git adapters, `source_revision_token` is the first 40 lowercase hexadecimal
characters of SHA-256 over this canonical material. The token is appended only
after hashing, so it is never part of its own input. `git_file` instead uses the
verified exact Git commit.

`content_sha256` is computed before the canonical material is assembled. For
issue/ticket sources it hashes canonical JSON containing normalized title,
body, and any retained timestamps. For `plain_text` it hashes normalized text
UTF-8 bytes. For both file adapters it hashes the exact bytes read or decoded
before text normalization; those bytes must also decode as UTF-8 for v1.

`planning-finding/v1` maps these values as follows:

- `provenance.source_id`: `source_identity`;
- `provenance.source_commit`: an exact Git commit for `git_file`; otherwise the
  derived `source_revision_token`. For non-Git adapters this is a schema-constrained source
  revision token, not a claim of Git provenance;
- `provenance.source_section`: `source_location`;
- `evidence.pointers`: the canonical source location, full content SHA-256
  pointer, normalized `proposal.evidence_pointers`, and any controlled
  secondary source-reference pointers;
- `producer`: the invocation's toolchain generation and commit.

The full digest pointer is exactly `sha256:<content_sha256>`. A source's
effective evidence contribution is the sorted, deduplicated union of that
digest pointer, its canonical source location, and its normalized proposal
evidence. A controlled merge also contributes the `source-ref/v1` pointer
defined below. Evidence is append-only under this owner: create writes the
effective contribution, while update and merge union it with existing evidence
and never remove an existing pointer. Existing evidence being a strict superset
of the incoming contribution is not itself a semantic change.

### `github_issue`

Raw input fields are `owner`, `repository`, positive integer `issue_number`,
title, body, and optional `created_at` and `updated_at`. Canonical
`adapter_metadata` contains `provider=github`, lowercase owner/repository, the
integer issue number, and normalized timestamps when present. Identity is
`github-issue:github.com/<owner>/<repository>#<issue_number>`. The canonical URL
is `https://github.com/<owner>/<repository>/issues/<issue_number>` with no query
or fragment.

### `external_ticket`

Raw input fields are provider token, provider-instance hostname,
provider-specific stable external ID, HTTPS URL, title, body, and optional
`created_at` and `updated_at`. Canonical `adapter_metadata` contains the
normalized provider, instance, external ID, and timestamps. The provider token must match
`[a-z][a-z0-9-]{0,31}`; the external ID is trimmed NFC text with case
preserved. Identity is the exact tuple
`ticket:<provider>:<provider-instance>:<percent-encoded-external-id>`. A missing
stable external ID, non-HTTPS location, or URL host that disagrees with the
provider instance blocks. V1 accepts this already structured envelope only; it
does not scrape provider pages or infer identifiers from arbitrary text.

For URLs, lowercase scheme and host, remove default port, remove dot segments,
normalize percent-encoding of unreserved characters, discard fragments, and
retain only adapter-declared identity query parameters in sorted order. URL and
timestamps do not participate in source identity. If timestamps are retained
in the canonical envelope, require an RFC 3339 offset, convert to UTC, emit
`YYYY-MM-DDTHH:MM:SS[.fraction]Z`, and trim trailing fractional zeroes. They
participate only in the source revision token.

### `plain_text`

Raw input fields are `text` and optional `display_title`; canonical
`adapter_metadata` contains only the normalized display title when present.
Identity
is `text:sha256:<content-sha256>`, location is `inline-text`, and the command
computes both digests internally. The human supplies no hash. A text change is
a different source identity unless an explicit compatible target is supplied.

### `git_file`

Raw input fields are absolute `repository_root`, canonical repository identity,
exact 40-character commit, POSIX repository-relative path, and optional
section. Canonical `adapter_metadata` contains the repository identity, exact
commit, normalized path, optional section, and exact-byte SHA-256. The command
verifies that the repository root's configured identity matches the bound
identity, then reads content from the object database at that commit and path.
Reject absolute source paths, `..`, symlink
escapes, missing objects, abbreviated commits, or a worktree read used as a
substitute. Verify the content with the repository object database before
normalization. Identity is `git-file:<repository-identity>:<path>`;
`source_revision_token` is the exact Git commit; location is `<path>` plus the
optional section.

### `file_snapshot`

Raw input fields are RFC 4648 standard padded `content_base64` and an optional
path label. Reject invalid base64 or decoded non-UTF-8 bytes. Canonical
`adapter_metadata` contains only the normalized label when present and the
exact-byte SHA-256. Identity is `file-snapshot:sha256:<content-sha256>` and location is
the label or `standalone-file`. The label is descriptive and excluded from
identity. This adapter records no repository identity or Git commit and never
claims that the bytes came from Git.

## Finding Normalization

The semantic comparison object contains only intake-owned fields:

- canonical source identity, revision token, and location;
- `title`;
- `scope.summary`, `scope.included`, and `scope.excluded`;
- `evidence.pointers`;
- `next_action.command` and `next_action.condition`.

Finding ID, finding revision, producer identity, existing lifecycle status, and
existing dependencies are excluded from semantic equality. On update or merge,
the command preserves lifecycle and dependencies exactly.

Normalize single-line values by converting to NFC, trimming leading/trailing
whitespace, and collapsing runs of ASCII space, tab, CR, or LF to one space.
Normalize every compared list item by the same rule, reject empty items, remove
exact duplicates, and sort by Unicode code-point order. List order is therefore
not semantic for `scope.included`, `scope.excluded`, or `evidence.pointers`.
No other field receives fuzzy, stemming, title-similarity, or embedding-based
normalization.

For evidence, the semantic test is contribution containment rather than whole
list equality: the existing finding must contain every pointer in the incoming
effective evidence contribution. Extra existing pointers are preserved and do
not force an update. A missing incoming pointer is added by update or merge;
omission from a later proposal never requests deletion.

New findings use lifecycle `Open`, empty dependencies, and revision 1. An
update or merge may change only the intake-owned fields above and the required
revision/producer mechanics. A source that implies lifecycle, dependency,
destructive, migration, demotion, or contract-narrowing changes blocks unless a
later explicitly authorized workflow owns that decision.

## Duplicate, Update, And Merge Matrix

Build one exact source index from every finding's primary
`provenance.source_id` and controlled source-reference pointers. Never match by
title or semantic similarity.

- Same canonical source identity, one target, unchanged source revision and
  location, equal normalized title/scope/next action, and existing evidence a
  superset of the incoming effective contribution: `no-op` with no finding
  mutations or touched revisions.
- Same canonical source identity, one target, changed source revision,
  location, title, scope, or next action, or missing incoming evidence, with no
  change outside intake-owned fields: `update` that unions evidence and
  increments that finding revision once.
- Explicit target supplied, incoming identity maps to no other finding, target
  is not closed/completed/superseded, and normalized title, scope, and next
  action already equal: controlled `merge`. Preserve the target's primary
  provenance, lifecycle, and dependencies; union the incoming effective
  evidence contribution and canonical source-reference pointer; increment
  once.
- Different source identity and no explicit target: `create`, even when titles
  look alike.
- Exact source identity mapped to multiple findings, explicit target conflict,
  incompatible merge content, unsupported source, or ambiguous change:
  `block` without calling the store.

A controlled secondary source pointer has the exact form:

```text
source-ref/v1|<percent-encoded-source-identity>|<revision-token>|<percent-encoded-location>
```

Percent encoding uses UTF-8, uppercase hexadecimal, and RFC 3986 unreserved
characters only. These pointers participate in exact source-index lookup.

## Finding ID Allocation

All allocation uses the complete snapshot already bound by ledger revision and
file hash.

1. Accept IDs only in the form `<PREFIX>-<positive-base10-integer>`, where the
   prefix matches `[A-Z][A-Z0-9]*`, the integer has no leading zero, and every
   existing finding uses one identical prefix.
2. A malformed ID, mixed prefix, duplicate numeric slot, zero, or negative
   value blocks the whole intake.
3. On a non-empty ledger, derive the namespace from all existing IDs. If an
   invocation also binds `finding_namespace`, it must match.
4. On an empty ledger, require an explicit project-authorized
   `finding_namespace`; absence or ambiguity blocks. The reusable owner does not
   invent a project prefix.
5. Resolve all semantic decisions before allocation. Sort new creates by
   canonical source identity and then by SHA-256 of the normalized comparison
   object. Conflicting duplicate sort keys block.
6. Allocate consecutive IDs beginning at `max(existing numeric suffix) + 1`;
   do not fill gaps. Multiple creates remain in one atomic store request.

The store CAS rejects a concurrent or stale snapshot without writing any item.
A caller may start a new semantic evaluation from a fresh snapshot; it must not
reuse the stale prepared request with changed facts.

## Command Receipt And Stop Boundary

The returned command receipt names the canonical source identities, semantic
decision per source, target or allocated finding IDs, bound ledger revision and
file hash, internal prepared-operation digest, store outcome and receipt, and
whether the result wrote the ledger. It may summarize but does not durably store
the complete raw source envelope.

After `applied`, `exact_replay`, semantic `block`, or an unsupported case, the
command stops. It must not select work, create a dispatch or runway, execute a
slice, close a finding, or select successor work.

## Consequences For CCFG-24A

- `ledger-store/v1`, DEC-037, and `scripts/planning_contract.py` remain unchanged.
- The original blocker is resolved as a contract-layer clarification, not a
  store widening.
- The replacement runway can begin directly with owner implementation.
- Candidate validation uses only temporary or fixture ledgers.
- CCFG-24 may become `Prepared` after this batch; only a later separately
  planned CCFG-24B cutover may close it.
