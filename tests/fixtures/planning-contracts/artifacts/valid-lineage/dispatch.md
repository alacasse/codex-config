# CCFG-21 Dispatch

## Operational Contract

```yaml
schema: planning-dispatch/v1
artifact:
  id: ccfg-21-artifacts
  program: codex-config
  revision: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
source:
  ledger_path: LEDGER.md
  ledger_revision: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
  finding_ids:
  - CCFG-21
selection:
  outcome: selected
  rationale_code: bounded-ready-finding
scope:
  goal: Prove revisioned artifact lineage writes.
  included_finding_ids:
  - CCFG-21
  deferred_finding_ids: []
  owner_seam: planning-contract
  batch_kind: migration
  risk_summary:
  - artifact lineage migration
approval_gates: []
dependencies:
  satisfied:
  - CCFG-20
  blocking: []
runway:
  expected_path: runway.md
execution_context:
  toolchain_source_root: /work/stable
  canonical_planning_repository_root: /work/stable
  implementation_target_root: /work/candidate
stops_when:
- lineage mismatch
producer:
  toolchain_generation: stable
  toolchain_commit: 0123456789abcdef0123456789abcdef01234567
  schema_version: planning-dispatch/v1
```
