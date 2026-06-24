# Test Quality Review Integration

A slice may explicitly request:

```md
Test quality review: none | delta-only | focused | full-audit
```

Default to `none` when the field is omitted. Existing behavior must remain
unchanged for specs that do not request test quality review.

If a slice requests `delta-only`, `focused`, or `full-audit`, invoke
`$test-quality-review` using the requested mode and include its compact YAML
findings in the review output.

Treat test-quality-review findings as review information only. Do not
automatically modify execution flow, create issues, update the ledger, block
execution, run full-audit orchestration, generate ADRs, or create remediation
plans unless the existing review rules or the spec already require that action.
