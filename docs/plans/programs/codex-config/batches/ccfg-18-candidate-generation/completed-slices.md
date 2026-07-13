# CCFG-18 Candidate Generation Completed Slices

## Slice 1: Candidate Roots And Strict Transition

- Candidate commit: `b044e3c348922663aa074638227aae8d2633cfe3`.
- Parents: `da5b97165eb8d8c9f809a64937bcc9d753032ee7` and
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Reviewed and committed tree:
  `36d347daa5d2c28e5894d730d4e4763067424236`.
- Accepted design subtree:
  `96f79a0996fbb8aac6358aeeac711589cb8ec308`.
- Candidate branch: `implementation/command-owner-redesign`.
- Origin identity: `alacasse/codex-config`.
- Candidate `CODEX_HOME`: `/home/alacasse/.codex-command-owner-redesign`,
  created empty with no credentials or installed content.
- Pre-creation review: clean with matching
  `verified_cross_checkout_precreation` and null strict identity.
- Creation worker: success with matching
  `verified_cross_checkout_precreation` and null strict identity.
- Post-transition review: clean with null pre-creation identity and matching
  `verified_cross_checkout_context`.
- Validation: 86 focused tests and 440 subtests passed; 3 focused manifest
  tests and 137 subtests passed; Ruff and basedpyright passed; stable installer
  status/dry-run, planning-state current/validate, manifest JSON, ancestry,
  branch, origin, tree, and diff checks passed.
- Known-red diagnostic: full manifest validation remained exactly 3 failed,
  18 passed, and 202 subtests passed in the three documented unrelated wording
  expectations.

### Transition Receipt

Exact helper-produced `cross_checkout_transition_receipt_to_dict` result:

```json
{
  "interface": "cross-checkout-transition-receipt/v1",
  "precreation_context": {
    "interface": "cross-checkout-precreation/v1",
    "stable_control": {
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "da5b97165eb8d8c9f809a64937bcc9d753032ee7",
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_commit_before": "da5b97165eb8d8c9f809a64937bcc9d753032ee7",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "codex_home": "/home/alacasse/.codex",
      "generation_role": "stable",
      "canonical_state_mutation_allowed": true
    },
    "candidate_intent": {
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "expected_repository_state": "absent",
      "candidate_codex_home": "/home/alacasse/.codex-command-owner-redesign",
      "expected_codex_home_state": "absent",
      "base_repository": "alacasse/codex-config",
      "base_commit": "da5b97165eb8d8c9f809a64937bcc9d753032ee7",
      "implementation_branch": "implementation/command-owner-redesign",
      "accepted_design_snapshot": "caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c"
    },
    "creation_authority": {
      "repository_creation_allowed": true,
      "candidate_codex_home_creation_allowed": true,
      "allowed_creation_roots": [
        "/home/alacasse/projects/codex-config-command-owner-redesign",
        "/home/alacasse/.codex-command-owner-redesign"
      ]
    }
  },
  "created_candidate_identity": {
    "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
    "implementation_commit": "b044e3c348922663aa074638227aae8d2633cfe3",
    "implementation_branch": "implementation/command-owner-redesign",
    "candidate_codex_home": "/home/alacasse/.codex-command-owner-redesign",
    "base_repository": "alacasse/codex-config",
    "base_commit": "da5b97165eb8d8c9f809a64937bcc9d753032ee7",
    "accepted_design_snapshot": "caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c"
  },
  "strict_context": {
    "interface": "cross-checkout-context/v1",
    "execution_context": {
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "da5b97165eb8d8c9f809a64937bcc9d753032ee7",
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_commit_before": "da5b97165eb8d8c9f809a64937bcc9d753032ee7",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "implementation_commit_before": "b044e3c348922663aa074638227aae8d2633cfe3",
      "codex_home": "/home/alacasse/.codex",
      "generation_role": "stable",
      "canonical_state_mutation_allowed": true
    }
  },
  "deletion_condition": "CCFG-29 final integration"
}
```

### Orchestration Anomaly

```yaml
- slice: 1
  severity: low
  category: post_creation_absent_parser_attempt
  observed: The coordinator invoked the absent-state parser once after candidate creation.
  impact: The installed helper failed closed before any write or lifecycle decision.
  action_taken: Reused the exact retained pre-creation facts with the helper transition builder and validated strict context.
  follow_up: Keep pre-creation context alive or serialize a helper-owned rehydration form across creation-bearing delegation.
```
