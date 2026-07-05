# Runner Artifacts

Use this reference only when a workflow has explicit compact runner output to
include in a projection. Runner artifacts are optional projection inputs, not a
requirement for ordinary planning reports.

## Projection Inputs

Pass runner inputs only to `rebuild-projection`:

```bash
python scripts/planning_state.py rebuild-projection --root <planning-root> --database <projection.sqlite> --runner-artifact <artifact.json>
python scripts/planning_state.py rebuild-projection --root <planning-root> --database <projection.sqlite> --runner-artifact-manifest <manifest.json>
```

Combine these with `--state-file` and `--program` only when those same values
are part of the desired projection identity.

## Artifact Contract

A runner artifact is compact JSON using the `planning-runner-artifact` protocol.
It should contain a program slug, run id, status, optional timestamps or summary,
and a bounded list of phase summaries. Phase entries may include status, reason,
message, severity, duration, and compact context-pressure values.

A runner artifact manifest uses the `planning-runner-artifact-manifest`
protocol and lists artifact paths. Manifest entries may be strings or objects
with a `path` field.

Do not store raw telemetry, full logs, prompts, transcripts, or high-cardinality
event streams in runner artifacts meant for projection.

## Reporting Behavior

Projection source identity includes each runner artifact and manifest supplied
during rebuild. Later `report-projection` calls will refuse stale or mismatched
projection data when those files change or disappear.

Runner-specific reports are:

- `runner-latest-run`
- `runner-failed-phases`
- `runner-context-pressure`

When no runner artifacts were projected, runner reports return an absent
summary row. Non-runner reports such as `pending-batches`,
`missing-closeout-evidence`, and `batch-evidence` should remain usable without
runner inputs.
