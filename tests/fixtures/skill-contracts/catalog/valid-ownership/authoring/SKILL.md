# Catalog Authoring

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: catalog-authoring
  audience: authoring-support
producer:
  toolchain_generation: candidate
  toolchain_commit: "1111111111111111111111111111111111111111"
  schema_version: skill-contract/v1
purpose: Author structured contracts without extra audience restrictions.
owns:
  decisions:
    - contract_structure_design
  durable_facts:
    - authoring_rules
reads:
  required: []
  conditional: []
writes:
  - authored_contract
requires:
  mechanisms: []
  evidence_skills: []
delegates: []
forbids: []
outputs:
  one_of:
    - authored_result
stops_when: []
references: []
```
