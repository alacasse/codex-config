# Reporting Contracts v1

## Contents

- Compact Convergence Assessment v1
- Compact Report Contract v1
- Information Lifetime Rules

## Compact Convergence Assessment v1

Use compact convergence for routine slice reports, commit receipts, ledger
updates, and status reporting. Progress is not the same as convergence, but the
routine convergence signal should be small enough to carry forward across many
slices.

Routine output format:

```yaml
convergence:
  phase: convergence
  scope_trend: shrinking
  new_unknowns: []
  blockers: []
  next_proof: "Validate ownership resolution in sandbox"
```

Fields:

- `phase`: `discovery | convergence | closure`
- `scope_trend`: `shrinking | stable | expanding`
- `new_unknowns`: compact list of newly discovered unknowns, or `[]`
- `blockers`: compact list of blockers, or `[]`
- `next_proof`: the next concrete proof needed to increase confidence

Use the expanded convergence template only when scope is expanding, significant
uncertainty exists, blockers are present, or final batch reporting is being
produced.

Expanded output format:

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

Definitions:

- `discovery`: the runway is still revealing new scope, hidden coupling, unclear
  behavior, missing test coverage, or architectural uncertainty. Do not forecast
  completion.
- `convergence`: the direction is stable, new discoveries are decreasing,
  uncertainty is localized, and slices are reducing the unknown space.
- `closure`: remaining work is explicitly bounded, mostly known, and expected to
  close known items rather than reveal major new ones.
- `shrinking`: the slice closed more uncertainty than it introduced.
- `stable`: the slice made progress, but open uncertainty stayed roughly the
  same.
- `expanding`: the slice discovered more unknowns, blockers, or required
  follow-ups than it closed.

Forecastability rules:

- Use `completion forecastable: no` if the runway is in `discovery`.
- Use `completion forecastable: no` if remaining work is not bounded.
- Use `completion forecastable: no` if new unknowns are appearing faster than
  they are being closed.
- Use `completion forecastable: yes` only when remaining work can be enumerated
  as bounded slices.
- Forecast remaining work in bounded slices, not calendar time.
- Do not say or imply that work is almost done unless remaining work is
  explicitly enumerated, no major new unknowns were introduced in the latest
  slice, temporary compatibility logic is removed or intentionally documented,
  follow-up work is separated from blocking work, and the next slice is expected
  to close known items rather than discover new ones.

## Compact Report Contract v1

Use this shared contract for `runway_worker`, `runway_reviewer`, and coordinator
commit receipts. Optimize reports for machine consumption, future recovery, and
long-term retention. Prefer YAML whenever possible.

Global rules:

- Return structured results only.
- Do not return implementation history.
- Do not narrate reasoning.
- Do not explain chronological work performed.
- Do not paste command transcripts or long logs.
- Clean worker reports should be 12 lines or fewer.
- Clean reviewer reports should be 10 lines or fewer.
- Expanded output is allowed only when findings exist, blockers exist,
  validation failed, or escalation is required.

Worker report:

```yaml
status: success
files_changed:
  - path/to/file.py
behavior_changed: false
validation:
  passed:
    - pytest: "75 passed"
risks: []
follow_up: []
notes_for_next_slice: []
```

Reviewer report:

```yaml
status: clean
findings: []
residual_risks: []
required_fixes: []
```

If a slice requests test quality review, include the compact YAML findings from
`$test-quality-review` in the reviewer report.

Commit receipt:

```yaml
slice: 2
commit: abc1234
subject: Extract module owner
status: committed
files_changed:
  - src/module_owner.py
validation: "pytest 75 passed; ruff passed; harness PASS 48 passed"
review: clean
convergence:
  phase: convergence
  scope_trend: shrinking
  new_unknowns: []
  blockers: []
  next_proof: "Move runtime entrypoint off compatibility facade imports"
inspect:
  - git show --stat abc1234
  - git show abc1234
```

## Information Lifetime Rules

Classify information before carrying it forward.

Permanent:

- commits
- durable architecture decisions
- unresolved risks
- ADR-worthy decisions
- compatibility paths that remain after the batch

Batch-scoped:

- remaining slices
- stop conditions
- active validation strategy
- active dirty-file constraints
- unresolved review or validation findings
- current convergence phase and next proof

Slice-scoped:

- implementation notes
- review findings
- validation details
- failure/recovery loops
- sandbox output paths for the current slice

Disposable after task completion:

- implementation chronology
- repeated clean-review prose
- command transcripts
- repetitive validation details
- repeated explanations of already-closed slices
