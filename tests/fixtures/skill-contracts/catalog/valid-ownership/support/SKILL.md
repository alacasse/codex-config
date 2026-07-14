# Catalog Support

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: catalog-support
  audience: support-mechanism
producer:
  toolchain_generation: candidate
  toolchain_commit: "1111111111111111111111111111111111111111"
  schema_version: skill-contract/v1
purpose: Apply a caller-owned path decision.
owns:
  decisions:
    - path_resolution
  durable_facts:
    - path_rules
reads:
  required: []
  conditional: []
writes: []
requires:
  mechanisms: []
  evidence_skills: []
delegates: []
forbids:
  - candidate_selection
outputs:
  one_of:
    - resolved_path
stops_when: []
references: []
```
