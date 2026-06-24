---
name: test-quality-review
description: Review the quality of project tests for behavioral confidence, regression protection, assertion strength, mocking and fixture friction, maintainability, and production design signals revealed by tests. Use when asked to review changed tests, audit a test file/module/feature/bug fix, evaluate whether tests meaningfully protect behavior, or identify test friction that may indicate design issues; do not optimize for coverage percentages.
---

# Test Quality Review

Evaluate whether tests create confidence in important behavior. Do not optimize
for coverage percentages. Treat hard-to-write or hard-to-read tests as evidence:
the issue may be in test code, production design, or both.

This skill is independent from `batch-runway`. It may be used by reviewers,
architects, implementation agents, or future automation.

## Mode Selection

Infer the mode from the request unless the user names it.

- `delta-only`: review only tests changed by the current change set. Prevent new
  weak tests, missing regression coverage, and newly introduced design friction.
  Do not audit unrelated historical tests.
- `focused`: review a named module, bug fix, feature, or test file. Analyze the
  requested area more deeply, including adjacent production behavior when needed.
- `full-audit`: review a larger test-suite area. Prioritize recurring smells,
  high-impact behavioral gaps, architectural friction, and remediation tracks.
  Do not attempt exhaustive reporting.

If scope is unclear, choose the narrowest useful mode and state the assumption.

## Review Workflow

1. Identify the behavior under test. Read the test names, assertions, fixtures,
   and relevant production code or public contract. Focus on externally
   observable outcomes, not implementation coverage.
2. Map important behavior to protection. Look for critical success paths, edge
   cases, failure paths, known bug risks, data boundaries, and cross-module
   contracts.
3. Evaluate assertion quality. Check whether assertions prove the behavior named
   by the test and would fail if the important behavior regressed.
4. Evaluate mocking and fixtures. Decide whether setup increases clarity or hides
   the real behavior. Distinguish poor test design from production coupling.
5. Look for regression gaps. For each fragile or historically risky behavior,
   prefer a focused test that would have failed for the bug.
6. Extract design signals. Explain whether friction appears to originate from
   tests, production code, or both.
7. Report only actionable findings. Prefer concrete examples and suggested
   stronger assertions or test cases.

## Finding Criteria

### Assertion Quality

Flag weak-confidence tests, including:

- assertions that only verify success status, absence of exceptions, or non-null
  results
- assertions that inspect implementation details instead of observable behavior
- assertions that do not validate what the test name claims
- tests where the core logic could be broken while the test still passes

For each finding, explain why confidence is weak, suggest stronger assertions,
and classify risk as `low`, `medium`, or `high`.

### Behavioral Protection

Identify important behavior that is unprotected, protected only indirectly, or
missing edge/failure-path checks. Focus on contracts, user-visible outcomes,
persisted state, emitted events, API responses, CLI output, file effects, and
other externally observable behavior.

### Regression Protection

For missing regression tests, describe:

- the behavior that should be protected
- why the behavior is historically or structurally risky
- a concrete regression test that would fail if the bug returned

Do not demand regression tests for every code path. Prioritize known bugs,
fragile seams, recent fixes, and behavior with high user or operational impact.

### Mocking Quality

Classify mocking findings as:

- `low concern`: mocks are mostly local and clarify a boundary
- `medium concern`: mocks obscure some behavior or duplicate implementation
  structure
- `high concern`: tests mostly validate mock wiring, mock chains, or details
  that could pass while core behavior is broken

Prefer real collaborators, fakes, contract tests, or narrower seams when they
would materially improve confidence without making tests brittle.

### Fixture Complexity

Flag excessive setup such as large object graphs, many mocks or patches,
repeated setup patterns, and fixtures that are difficult to understand. For each
case, classify the likely source as:

- poor test design
- missing fixture tooling
- production design complexity
- legitimate integration complexity

### Design Signals

Use test friction as design evidence, not automatic blame. Look for:

- too many responsibilities in one class or function
- hidden dependencies
- tight coupling
- global state
- poor architectural boundaries
- missing seams for testing meaningful behavior

State whether the friction appears to originate from test code, production code,
or both.

## Output Format

For automation or reviewer workflows that request compact output, return YAML:

```yaml
test_quality:
  mode: delta-only
  status: clean
  findings: []
```

Use `status: findings` and populate `findings` only when actionable test-quality
issues exist. Keep findings compact but include file path, test name when
applicable, risk level, why it matters, and suggested action.

For standalone reviews, use this structure:

```markdown
# Test Quality Review

## Verdict

## High-Risk Behavioral Gaps

## Weak or Misleading Tests

## Regression Coverage Findings

## Mocking and Fixture Friction

## Design Signals Revealed by Tests

## Recommended Actions
```

Each finding must include:

- file path
- test name, if applicable
- risk level
- why it matters
- suggested action

If a section has no findings, say `No findings.` Do not pad the report with
speculation.

## Full-Audit Additions

For `full-audit`, append:

```markdown
## ADR Candidates

## Refactoring Opportunities

## Suggested Remediation Tracks
```

Limit full-audit output to the top 5 high-impact findings, top 3 ADR candidates,
and top 3 remediation tracks. Generate ADR candidates only when findings imply a
long-lived design decision; do not propose ADRs for isolated test issues.

## Non-Goals

- Do not optimize for coverage percentages.
- Do not rewrite the entire test suite.
- Do not force architectural rewrites.
- Do not create large cleanup backlogs.
- Do not expand scope beyond the selected mode.
