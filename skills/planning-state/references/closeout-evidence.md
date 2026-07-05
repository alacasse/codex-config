# Closeout Evidence

Use this reference when a workflow needs to render or validate a completed
batch closeout. Closeout evidence is pointer-first: store compact summaries and
artifact paths, not transcripts, raw logs, or pasted review output.

## Render Closeout

`render-closeout` builds a bounded closeout evidence index from explicit inputs
and a registered closeout artifact in the state fixture.

```bash
python scripts/planning_state.py render-closeout --root <planning-root> --program <program-slug> --batch-id <batch-id> --state-file <state-file> --completed-slices-summary "<summary>" --validation-artifact <path> --validation-summary "<summary>" --review-artifact <path> --review-summary "<summary>" --cleanup-classification <classification>
```

Use `--target <closeout-path>` only when the target is the registered
`closeout.md` path and the caller has authorized writing it. Omit `--target` to
preview Markdown on stdout.

Optional evidence inputs are additive and compact:

- `--cleanup-evidence <path>` for cleanup checks or residue classifications.
- `--commit <sha>` plus optional `--commit-range-from` and
  `--commit-range-to`.
- `--transition-receipt-artifact <path>` paired with
  `--transition-receipt-summary "<summary>"`.

## Validate Closeout

Run validation against the registered closeout path and the same explicit state
fixture:

```bash
python scripts/planning_state.py validate-closeout --root <planning-root> --program <program-slug> --batch-id <batch-id> --closeout <closeout-path> --state-file <state-file>
```

Treat validation blockers as closeout blockers. Fix the pointer, registration,
or bounded summary; do not satisfy the contract by embedding long logs.

## Evidence Boundaries

- Prefer paths to committed artifacts, generated reports, validation summaries,
  review receipts, transition receipts, and cleanup classifications.
- Keep summaries short enough for a closeout index.
- Cleanup residue classifications, especially deferred residue, must point to a
  bounded artifact or compact summary that names the reason, removal condition,
  and follow-up owner.
- Do not paste command transcripts, raw telemetry, long review logs, or
  downstream project-specific directory examples into reusable closeout
  guidance.
- `validate-closeout` and `render-closeout` require explicit JSON state
  fixtures and target policy. They do not require a SQLite projection.
