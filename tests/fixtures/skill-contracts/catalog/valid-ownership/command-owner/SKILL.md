# Catalog Command Owner

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: catalog-command
  audience: human-command-owner
producer:
  toolchain_generation: candidate
  toolchain_commit: "1111111111111111111111111111111111111111"
  schema_version: skill-contract/v1
purpose: Own one human workflow decision.
owns:
  decisions:
    - candidate_selection
  durable_facts:
    - selected_dispatch_content
reads:
  required: []
  conditional: []
writes:
  - selected_dispatch
requires:
  mechanisms:
    - catalog-support
  evidence_skills: []
delegates:
  - responsibility: path_resolution
    target: catalog-support
forbids: []
outputs:
  one_of:
    - selected_result
stops_when: []
references: []
```
