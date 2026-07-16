# CCFG-24A Failed Attempt Supersession

The 2026-07-16 CCFG-24A attempt stopped before implementation and must not be
resumed.

Historical evidence is preserved by:

- `execution-report.md`;
- queued planning commit `33f7adfd1a5948f9176f8b2d1ddc47040cebb6e3`;
- blocker-state commit `c0870240c5a7de5f37a6dc1a8a314c3eeed60647`;
- report commit `199f4a9cd86edf7e80a13b174b162ce6798c18af`.

Git history is the authoritative copy of the failed dispatch and runway.
`blocked-dispatch.md` and `blocked-runway.md` are compact non-executable pointers,
not duplicated planning documents.

The blocker is resolved by
`../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`. Current
executable planning is `dispatch.md` and `runway.md` in this directory.

Planning State may point only to the current `runway.md`. A request to recreate
or resume the old decision slice must block.
