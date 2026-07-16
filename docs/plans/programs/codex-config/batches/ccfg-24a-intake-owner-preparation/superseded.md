# CCFG-24A Blocked Attempt Supersession

The 2026-07-16 CCFG-24A execution attempt remains historical evidence at:

- `execution-report.md`
- `blocked-dispatch.md`
- `blocked-runway.md`

Those artifacts describe a real Slice 1 stop before implementation and must not
be resumed. They are superseded as executable planning by the current
`dispatch.md` and `runway.md` in this directory.

The blocker was resolved by the accepted contract clarification at
`../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`: DEC-037 binds
the exact prepared apply request, while `add-to-ledger/v1` owns upstream source
semantics and derives the store key internally. `ledger-store/v1` remains
unchanged.

Planning State may point only to the current `runway.md`. Any direct request to
execute `blocked-runway.md`, reuse its three-slice ledger, or restart its
decision slice must block and redirect to the current runway.
