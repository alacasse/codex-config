# Finalize Batch v1

Use this reference only after all intended slices are complete or the user asks
for final batch reporting.

## Final Validation

1. Run the spec's final validation.
2. Run project-required graph, search index, generated docs, or metadata refresh
   after code changes.
3. If final validation uses a project-specific integration harness, use an
   explicit fresh output path when the harness writes artifacts.
4. Read the required summary artifact before reporting the final harness result.
5. Report skipped validation clearly when a command cannot run.

## Final Report

Report:

- completed commits
- validation results
- skipped slices
- remaining risks
- compatibility paths that remain
- audit artifacts or summary paths
- `orchestration_anomalies`
- final inspection commands
- expanded final convergence assessment

Always print an `Orchestration Anomalies` section in the final report. Use a
compact YAML block and print `orchestration_anomalies: []` when no anomalies
were recorded. Include resolved/no-impact anomalies when they suggest future
workflow fixes, but do not include routine command output, normal validation
logs, clean reviews, or implementation chronology.

## Expanded Convergence

Use the expanded convergence template for final batch reports:

```md
## Convergence Assessment

### Phase
`discovery | convergence | closure`

### Scope trend
`shrinking | stable | expanding`

### Closed this slice
- ...

### Newly discovered
- ...

### Deferred out of scope
- ...

### Remaining unknowns
- ...

### Temporary compatibility paths
- ...

### Blockers
- ...

### Completion forecastable
`yes | no`

### Forecast
- ...

### Evidence
- ...

### Next proof required
- ...
```

## Completion Rules

- Do not mark `closure` while major unknowns remain.
- Do not mark completion forecastable while scope is still expanding.
- Do not say work is almost done unless remaining work is bounded, known,
  explicitly enumerated, and supported by the latest convergence evidence.
- Forecast remaining work in bounded slices, not calendar time.
