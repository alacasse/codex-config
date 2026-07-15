# Global Ledger Prototype

## Global Comparison

```yaml
interface: planning-ledger-global-comparison/v1
source_artifact: LEDGER.md
source_revision: 1
findings:
- schema: planning-finding/v1
  id: CCFG-1
  revision: 1
  title: First finding
  provenance:
    source_id: SRC-1
    source_commit: "1111111111111111111111111111111111111111"
    source_section: source.md#one
  lifecycle:
    status: open
  dependencies: []
  scope:
    summary: First scope.
    included:
    - first
    excluded: []
  evidence:
    pointers: []
  next_action:
    command: plan-batch
    condition: explicit_request
  producer:
    toolchain_generation: stable
    toolchain_commit: 0123456789abcdef0123456789abcdef01234567
    schema_version: planning-finding/v1
- schema: planning-finding/v1
  id: CCFG-1
  revision: 1
  title: Second finding
  provenance:
    source_id: SRC-2
    source_commit: "2222222222222222222222222222222222222222"
    source_section: source.md#two
  lifecycle:
    status: open
  dependencies:
  - CCFG-1
  scope:
    summary: Second scope.
    included:
    - second
    excluded: []
  evidence:
    pointers: []
  next_action:
    command: plan-batch
    condition: explicit_request
  producer:
    toolchain_generation: stable
    toolchain_commit: 0123456789abcdef0123456789abcdef01234567
    schema_version: planning-finding/v1
```
