# CCFG-19 Source Contract Decisions Completed Slices

## Slice 1: Join Contract, Owner, Scenario, And Test Evidence

- Candidate commit: `db0f37dc5a62205c3e33df9dbb82ded05fc04b47`.
- Candidate files:
  `docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`
  and `docs/design/command-owner-redesign/README.md`.
- Joined evidence: all 31 contracts have defensible source evidence, one target
  owner, resolved scenario evidence, source/target classification, and test
  disposition evidence; `blocking_ownership_conflicts: 0` is derived from the
  joined rows.
- Scenario catalog: all 16 absent references are defined or remapped, including
  the directly discovered `validation-classification` gap.
- Test inventory: all 28 current modules and 465 test methods are classified;
  253 methods use the primary classification and 212 use ordered exception
  selectors, with zero unassigned or multiply assigned methods.
- Review correction: the first independent review rejected incomplete
  mixed-module selectors, conflicting current evidence for
  `legacy-evidence-no-state-writes`, and an overstatement of direct source
  evidence. The worker re-audited every test method and corrected only the
  candidate record. Repeat independent review was clean.
- Validation: tracked and explicit no-index `git diff --check` passed; the
  implementation-created record exists; no final pytest or integration harness
  was assigned to this docs-only slice.
- Behavior changed: no runtime behavior and no accepted decision changed.
- Decision gate: schema evolution, `ledger-store`, runner protocol, and
  OPEN-003 remain unaccepted pending explicit user approval before Slice 2.

### Cross-Repository Receipts

Exact helper-produced `cross_repository_receipt_to_dict` results:

```json
{
  "candidate_implementation_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-19 Slice 1 joined contract evidence",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [],
      "implementation_paths": [
        "/home/alacasse/projects/codex-config-command-owner-redesign/docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/docs/design/command-owner-redesign/README.md"
      ]
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "bb5701fdb50e1ec921a07df36a5d3461341a092c",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "bb5701fdb50e1ec921a07df36a5d3461341a092c",
      "canonical_planning_commit_before": "bb5701fdb50e1ec921a07df36a5d3461341a092c",
      "implementation_commit_before": "db0f37dc5a62205c3e33df9dbb82ded05fc04b47"
    },
    "deletion_condition": "CCFG-29 final integration"
  },
  "stable_planning_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-19 Slice 1 stable planning receipt",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/completed-slices.md",
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md"
      ],
      "implementation_paths": []
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "bb5701fdb50e1ec921a07df36a5d3461341a092c",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "bb5701fdb50e1ec921a07df36a5d3461341a092c",
      "canonical_planning_commit_before": "bb5701fdb50e1ec921a07df36a5d3461341a092c",
      "implementation_commit_before": "db0f37dc5a62205c3e33df9dbb82ded05fc04b47"
    },
    "deletion_condition": "CCFG-29 final integration"
  }
}
```

## Slice 2: Accept Schema-Evolution And Ledger-Store Boundaries

- Candidate commit: `07c5d41882b6df83bc8298854a83d59a3006b555`.
- Accepted decisions: DEC-036 fixes the closed-world v1 schema-evolution rule;
  DEC-037 fixes the apply-only `ledger-store/v1` boundary.
- Approval evidence: exact user approval `Approve all four`, recorded in stable
  commit `19e0746cdc7f681ebe4e6b0ab0be62640097ea6f` before the Slice 2 worker
  handoff.
- Schema result: unknown versions block; unknown v1 fields reject unless a
  named bounded allowlist applies; optional additions require an accepted
  compatibility decision and reader-before-writer rollout; required-field and
  semantic ownership changes require a new version.
- Store result: whole-ledger CAS, touched-finding revisions, exact idempotent
  replay, key/payload mismatch rejection, deterministic rendering, atomic
  replacement, and ledger-written/receipt-missing recovery are mechanical;
  command owners retain all workflow semantics.
- Current strict validators and permissive compatibility examples remain
  contrasting evidence rather than a silently standardized current policy.
- Validation: `git diff --check` passed; DEC-036 and DEC-037 fenced YAML parsed;
  Markdown fences balanced; independent strict-context review was clean.
- Implementation: none. CCFG-20, CCFG-21, and CCFG-24 remain deferred.

### Cross-Repository Receipts

Exact helper-produced `cross_repository_receipt_to_dict` results:

```json
{
  "candidate_implementation_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-19 Slice 2 schema and ledger boundary decisions",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [],
      "implementation_paths": [
        "/home/alacasse/projects/codex-config-command-owner-redesign/docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/docs/design/command-owner-redesign/decisions.md"
      ]
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "19e0746cdc7f681ebe4e6b0ab0be62640097ea6f",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "19e0746cdc7f681ebe4e6b0ab0be62640097ea6f",
      "canonical_planning_commit_before": "19e0746cdc7f681ebe4e6b0ab0be62640097ea6f",
      "implementation_commit_before": "07c5d41882b6df83bc8298854a83d59a3006b555"
    },
    "deletion_condition": "CCFG-29 final integration"
  },
  "stable_planning_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-19 Slice 2 stable planning receipt",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/completed-slices.md",
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md"
      ],
      "implementation_paths": []
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "19e0746cdc7f681ebe4e6b0ab0be62640097ea6f",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "19e0746cdc7f681ebe4e6b0ab0be62640097ea6f",
      "canonical_planning_commit_before": "19e0746cdc7f681ebe4e6b0ab0be62640097ea6f",
      "implementation_commit_before": "07c5d41882b6df83bc8298854a83d59a3006b555"
    },
    "deletion_condition": "CCFG-29 final integration"
  }
}
```

## Slice 3: Accept Runner Boundary And Verify Generation Topology

- Candidate commit: `baeef7a736c1b1874b8bfd47a59343e3711907a6`.
- Accepted decision: DEC-017 preserves the runner's process lifecycle,
  environment and sandbox selection, telemetry, receipts, result validation,
  and stop-policy responsibilities while adding the approved public-command
  sequence, explicit loop bounds, fresh `plan-batch` iteration, and prohibition
  on successor-readiness semantics.
- Current direct APR/Batch Runway phase routing, closeout readiness,
  closeout-to-select behavior, and topology-only tests are classified as later
  rewrite/delete targets, not supported target contracts.
- Topology evidence: corrected CCFG-18 closeout and completed-slice evidence at
  `968f41d1ad752e817af518b12fb8f96273b76e0d` proves roots, generation
  identities, lineage, branch, isolated installation, canonical-write
  rejection, rollback, and unchanged default generation; fixture receipt
  `34202189a20313cbb3420e03507dd0165c0df2b6` is linked.
- Review correction: initial review rejected accidental narrowing of accepted
  runner responsibilities. The worker restored all seven responsibilities;
  repeat independent strict-context review was clean.
- Validation: DEC-017 and Slice 3 YAML parsed; Markdown fences balanced;
  candidate ancestry checks and `git diff --check` passed.
- Implementation: none. No runner, installer, manifest, agent, test, generation,
  or bridge behavior changed.

### Orchestration Anomaly

```yaml
- slice: 3
  severity: low
  category: worker_project_check_outside_handoff
  observed: The worker ran read-only install.sh --status once in each checkout before recognizing that the docs-only handoff did not authorize project-level checks.
  impact: Both commands exited zero and reported no changes; their output was excluded from Slice 3 acceptance evidence.
  action_taken: Directed the worker to stop project-level checks, relied only on durable CCFG-18 evidence, disclosed the deviation to the reviewer, and repeated clean review after the in-scope correction.
  follow_up: Keep worker handoffs explicit that read-only installer status is still a coordinator-owned project check unless assigned.
```

### Cross-Repository Receipts

Exact helper-produced `cross_repository_receipt_to_dict` results:

```json
{
  "candidate_implementation_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-19 Slice 3 runner and topology decisions",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [],
      "implementation_paths": [
        "/home/alacasse/projects/codex-config-command-owner-redesign/docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/docs/design/command-owner-redesign/decisions.md"
      ]
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "a0fdef399955f17a778c7d8b61ea56a4fca49e76",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "a0fdef399955f17a778c7d8b61ea56a4fca49e76",
      "canonical_planning_commit_before": "a0fdef399955f17a778c7d8b61ea56a4fca49e76",
      "implementation_commit_before": "baeef7a736c1b1874b8bfd47a59343e3711907a6"
    },
    "deletion_condition": "CCFG-29 final integration"
  },
  "stable_planning_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-19 Slice 3 stable planning receipt",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/completed-slices.md",
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md"
      ],
      "implementation_paths": []
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "a0fdef399955f17a778c7d8b61ea56a4fca49e76",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "a0fdef399955f17a778c7d8b61ea56a4fca49e76",
      "canonical_planning_commit_before": "a0fdef399955f17a778c7d8b61ea56a4fca49e76",
      "implementation_commit_before": "baeef7a736c1b1874b8bfd47a59343e3711907a6"
    },
    "deletion_condition": "CCFG-29 final integration"
  }
}
```
