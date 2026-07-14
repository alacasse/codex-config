# CCFG-20 Skill Contract Schema Completed Slices

## Slice 1: Establish Closed-World Schema And Interface

- Candidate commit: `2f8f7a8fedcac925016867596158251564470d88`.
- Candidate files: `schemas/skill-contract-v1.schema.json`,
  `scripts/skill_contract.py`, `tests/test_skill_contract_schema.py`, the two
  schema fixture catalogs, `pyproject.toml`, and `uv.lock`.
- Contract result: one Draft-07 schema owns the accepted closed-world
  `skill-contract/v1` shape, including producer identity; one deep Python
  interface owns extraction, YAML loading, schema application, deterministic
  diagnostics, and CLI adaptation.
- Fail-closed result: duplicate YAML keys reject at every mapping depth,
  Contract examples inside Markdown fences are ignored, directory catalogs
  discover only `SKILL.md`, and empty catalogs reject.
- Validation: 17 schema tests passed; Ruff passed; basedpyright reported zero
  errors; the valid CLI catalog exited 0; the invalid unknown-field catalog
  exited 1 under a successful expected-failure harness; `git diff --check`
  passed.
- Review correction: the first independent review found duplicate-key,
  fenced-example, and empty/non-skill catalog gaps. The worker added regression
  coverage and repeat independent review was clean over the full seven-file
  task-scoped diff.
- Behavior changed: yes, the candidate now exposes the repo-local schema and
  validator contract. No current skill, installed feature, manifest entry, or
  later finding changed.
- Cleanup residue: none.

### Orchestration Anomaly

```yaml
- slice: 1
  severity: low
  category: unexpected_head_change
  observed: Stable HEAD moved from 7c1c027 to 9833e92 during preflight because the queued CCFG-20 planning artifacts were committed concurrently.
  impact: The first strict-context payload became stale before delegation; no candidate write had started.
  action_taken: Frozen delegation, inspected the commit, regenerated the payload from the clean current heads, and revalidated every Slice 1 handoff.
  follow_up: Treat the reconciled 9833e92 planning commit as the stable baseline for subsequent slice receipts.
```

### Cross-Repository Receipts

Exact helper-produced `cross_repository_receipt_to_dict` results:

```json
{
  "candidate_implementation_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 1 skill contract schema and interface",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [],
      "implementation_paths": [
        "/home/alacasse/projects/codex-config-command-owner-redesign/schemas/skill-contract-v1.schema.json",
        "/home/alacasse/projects/codex-config-command-owner-redesign/scripts/skill_contract.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_contract_schema.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/schema/valid/example/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/schema/invalid-unknown-field/example/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/pyproject.toml",
        "/home/alacasse/projects/codex-config-command-owner-redesign/uv.lock"
      ]
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "canonical_planning_commit_before": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "implementation_commit_before": "2f8f7a8fedcac925016867596158251564470d88"
    },
    "deletion_condition": "CCFG-29 final integration"
  },
  "stable_planning_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 1 stable planning receipt",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/completed-slices.md"
      ],
      "implementation_paths": []
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "canonical_planning_commit_before": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "implementation_commit_before": "2f8f7a8fedcac925016867596158251564470d88"
    },
    "deletion_condition": "CCFG-29 final integration"
  }
}
```
