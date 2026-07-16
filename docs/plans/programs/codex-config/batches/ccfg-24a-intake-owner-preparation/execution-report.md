# CCFG-24A Failed Execution Report

## Status

- Attempt date: 2026-07-16
- Final attempt state: `blocked`
- Stopped in: the original Slice 1 decision step
- Accepted slice commits: none
- Candidate implementation commits: none
- Candidate install: not performed
- Stable install: untouched
- Closeout: none

This report is historical evidence. The failed attempt must not be resumed.
Current executable planning is `dispatch.md` and `runway.md` in this directory.

## What Happened

Planning State `current` and `validate` were green, CCFG-24A was the only queued
batch, and strict `cross-checkout-context/v1` startup validation returned
`ready`.

A worker drafted an uncommitted `add-to-ledger/v1` decision record in the
candidate checkout. No production code, tests, schemas, installed links, or
store code changed.

Independent review found that the draft treated one upstream intake `request_id`
as if `ledger-store/v1` had to distinguish complete raw intake payloads. A
focused store investigation confirmed that DEC-037 durably binds the exact
mechanical apply request received by the store, not the complete upstream source
envelope.

For a metadata-only semantic no-op, two different upstream requests can collapse
to the same mechanical store request. The draft therefore could not make the
store return an upstream-payload mismatch without widening the store contract.
That widening was outside the runway and correctly triggered a stop.

The reviewer also identified bounded decision work for mutation authority,
complete-snapshot ID allocation, source canonicalization, and exact duplicate
rules.

## Stop And Cleanup

Execution stopped before implementation. The uncommitted draft was removed and
the candidate checkout returned clean at:

```text
b38570bcd97b2584f3828abcd395b0f45ed91e58
```

The stable planning checkout recorded the blocker in commit:

```text
c0870240c5a7de5f37a6dc1a8a314c3eeed60647
```

The full report was added in commit:

```text
199f4a9cd86edf7e80a13b174b162ce6798c18af
```

The pre-attempt queued planning is recoverable from commit:

```text
33f7adfd1a5948f9176f8b2d1ddc47040cebb6e3
```

Git history is the authoritative copy of the old dispatch and runway. Duplicate
`blocked-dispatch.md` and `blocked-runway.md` files are not required.

## Final Attempt State

| State | Result |
|---|---|
| CCFG-24 | `Pending` |
| Original CCFG-24A attempt | Blocked before implementation |
| Candidate checkout | Clean at `b38570b` |
| Candidate install | Not performed |
| Stable install | Untouched |
| CCFG-24B | Not selected or created |
| CCFG-25 | Not selected or prepared |

## Resolution

The blocker was resolved as a command/store boundary clarification, not a store
change:

- the human supplies source material, not a hash or replay identity;
- `add-to-ledger/v1` reevaluates source semantics against the current ledger;
- the command owner prepares one exact store request;
- the command owner derives the private idempotency key from that request;
- `ledger-store/v1` remains unchanged and owns exact mechanical replay only.

The accepted resolution is recorded at:

```text
../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md
```

The current CCFG-24A v1 is intentionally bounded to `plain_text` and
`github_issue`. Generic tickets, file ingestion, cross-source merge, and fuzzy
duplicate matching are deferred.

## Current Safe Action

A later explicit `work-batch` request may execute only the current two-slice
`runway.md`. It must use fresh Planning State and strict cross-checkout
validation, temporary or fixture ledgers for candidate execution, and the
accepted decision amendment.

Do not reconstruct or resume the old decision slice from Git history.
