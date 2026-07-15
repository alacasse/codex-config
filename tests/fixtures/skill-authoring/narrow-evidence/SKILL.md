---
name: fixture-evidence-classifier
description: Fixture-only narrow evidence classification trial.
---

# Fixture Evidence Classifier

Classify an explicit observation set without selecting work, executing a
workflow, or mutating state.

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: fixture-evidence-classifier
  audience: evidence-skill
producer:
  toolchain_generation: candidate
  toolchain_commit: 23db635dba08d7d1641fccfa0652ff5d3df0d2f6
  schema_version: skill-contract/v1
purpose: >-
  Classify an explicit observation set into one bounded evidence result.
owns:
  decisions:
    - evidence_classification
  durable_facts:
    - evidence_output
reads:
  required:
    - explicit_observations
  conditional: []
writes:
  - evidence_output
requires:
  mechanisms: []
  evidence_skills: []
delegates: []
forbids:
  - planning_state_mutation
  - workflow_decisions
  - workflow_execution
outputs:
  one_of:
    - classified_evidence
    - insufficient_evidence
stops_when:
  - missing_observations
  - conflicting_observations
references: []
```

## Procedure

1. Require the caller's explicit observation set.
2. Classify only what those observations establish as `confirmed`,
   `not_confirmed`, or `insufficient_evidence`.
3. Return the classification with the observations that support it.

Stop with `insufficient_evidence` when observations are missing or conflicting.
Do not select follow-up work, execute a workflow, or write planning state.
