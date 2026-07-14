# Catalog Evidence

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: catalog-evidence
  audience: evidence-skill
producer:
  toolchain_generation: candidate
  toolchain_commit: "1111111111111111111111111111111111111111"
  schema_version: skill-contract/v1
purpose: Produce bounded review evidence.
owns:
  decisions:
    - evidence_classification
  durable_facts:
    - review_findings
reads:
  required: []
  conditional: []
writes:
  - review_report
requires:
  mechanisms: []
  evidence_skills: []
delegates: []
forbids:
  - execution_acceptance
outputs:
  one_of:
    - evidence_report
stops_when: []
references: []
```
