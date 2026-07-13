from __future__ import annotations

import copy
import dataclasses
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import cast
from unittest import mock

from scripts import cross_checkout_context as context_owner


class CrossCheckoutContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.stable_root, self.stable_commit = self._create_repository("stable")
        self.implementation_root, self.implementation_commit = (
            self._create_repository("implementation")
        )
        self.codex_home = self.root / "codex-home"
        self.codex_home.mkdir()
        self.planning_root = self.stable_root / "docs" / "plans"
        self.planning_root.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _create_repository(self, name: str) -> tuple[Path, str]:
        root = self.root / name
        root.mkdir()
        self._git(root, "init", "--quiet")
        self._git(root, "config", "user.email", "tests@example.invalid")
        self._git(root, "config", "user.name", "Cross Checkout Tests")
        (root / "identity.txt").write_text(f"{name}\n", encoding="utf-8")
        self._git(root, "add", "identity.txt")
        self._git(root, "commit", "--quiet", "-m", f"Initialize {name}")
        return root.resolve(), self._git(root, "rev-parse", "HEAD")

    def _git(self, root: Path, *args: str) -> str:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return completed.stdout.strip()

    def _move_head(self, root: Path, label: str) -> None:
        changed_path = root / f"changed-{label}.txt"
        changed_path.write_text(f"move {label} HEAD\n", encoding="utf-8")
        self._git(root, "add", changed_path.name)
        self._git(root, "commit", "--quiet", "-m", f"Move {label} HEAD")

    def _payload(self) -> dict[str, object]:
        return {
            "interface": context_owner.INTERFACE,
            "execution_context": {
                "toolchain_source_root": str(self.stable_root),
                "toolchain_commit": self.stable_commit,
                "canonical_planning_repository_root": str(self.stable_root),
                "canonical_planning_commit_before": self.stable_commit,
                "implementation_target_root": str(self.implementation_root),
                "implementation_commit_before": self.implementation_commit,
                "codex_home": str(self.codex_home),
                "generation_role": "stable",
                "canonical_state_mutation_allowed": True,
            },
        }

    def _execution_payload(self, payload: dict[str, object]) -> dict[str, object]:
        return cast(dict[str, object], payload["execution_context"])

    def _invoke_after_receipt_validation(
        self,
        payload: dict[str, object],
        hook: mock.Mock,
        *,
        planning_paths: tuple[Path, ...] = (),
        implementation_paths: tuple[Path, ...] = (),
    ) -> None:
        context = context_owner.parse_cross_checkout_context(payload)
        receipt = context_owner.build_cross_repository_receipt(
            context,
            caller="runway-worker",
            reason="test guarded action",
            canonical_planning_root=self.planning_root,
            planning_paths=planning_paths,
            implementation_paths=implementation_paths,
        )
        hook(receipt)

    def test_parses_the_exact_versioned_context(self) -> None:
        context = context_owner.parse_cross_checkout_context(self._payload())

        self.assertEqual(context.interface, "cross-checkout-context/v1")
        self.assertEqual(
            context.execution_context,
            context_owner.ExecutionContext(
                toolchain_source_root=self.stable_root,
                toolchain_commit=self.stable_commit,
                canonical_planning_repository_root=self.stable_root,
                canonical_planning_commit_before=self.stable_commit,
                implementation_target_root=self.implementation_root,
                implementation_commit_before=self.implementation_commit,
                codex_home=self.codex_home.resolve(),
                generation_role="stable",
                canonical_state_mutation_allowed=True,
            ),
        )

    def test_allows_toolchain_to_share_the_implementation_repository(self) -> None:
        payload = self._payload()
        execution = self._execution_payload(payload)
        execution["toolchain_source_root"] = str(self.implementation_root)
        execution["toolchain_commit"] = self.implementation_commit
        execution["generation_role"] = "candidate"
        execution["canonical_state_mutation_allowed"] = False

        context = context_owner.parse_cross_checkout_context(payload)

        self.assertEqual(
            context.execution_context,
            context_owner.ExecutionContext(
                toolchain_source_root=self.implementation_root,
                toolchain_commit=self.implementation_commit,
                canonical_planning_repository_root=self.stable_root,
                canonical_planning_commit_before=self.stable_commit,
                implementation_target_root=self.implementation_root,
                implementation_commit_before=self.implementation_commit,
                codex_home=self.codex_home.resolve(),
                generation_role="candidate",
                canonical_state_mutation_allowed=False,
            ),
        )
        self.assertEqual(
            context_owner.capture_generation_identity(context),
            context_owner.GenerationIdentity(
                generation_role="candidate",
                toolchain_source_root=self.implementation_root,
                toolchain_commit=self.implementation_commit,
                codex_home=self.codex_home.resolve(),
                canonical_state_mutation_allowed=False,
            ),
        )

    def test_rejects_generation_role_root_mismatch_before_caller_hook(self) -> None:
        stable_mismatch = self._payload()
        stable_execution = self._execution_payload(stable_mismatch)
        stable_execution["toolchain_source_root"] = str(self.implementation_root)
        stable_execution["toolchain_commit"] = self.implementation_commit

        candidate_mismatch = self._payload()
        candidate_execution = self._execution_payload(candidate_mismatch)
        candidate_execution["generation_role"] = "candidate"
        candidate_execution["canonical_state_mutation_allowed"] = False

        for payload, role, expected_root_field in (
            (
                stable_mismatch,
                "stable",
                "canonical_planning_repository_root",
            ),
            (candidate_mismatch, "candidate", "implementation_target_root"),
        ):
            with self.subTest(role=role):
                hook = mock.Mock()
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    rf"generation_role '{role}' requires toolchain_source_root to "
                    rf"equal {expected_root_field}",
                ):
                    self._invoke_after_receipt_validation(payload, hook)
                hook.assert_not_called()

    def test_rechecks_toolchain_revision_before_caller_hook(self) -> None:
        context = context_owner.parse_cross_checkout_context(self._payload())
        self._move_head(self.stable_root, "toolchain")
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "toolchain_commit does not match HEAD for toolchain_source_root",
        ):
            receipt = context_owner.build_cross_repository_receipt(
                context,
                caller="runway-worker",
                reason="test stale toolchain rejection",
                canonical_planning_root=self.planning_root,
            )
            hook(receipt)
        hook.assert_not_called()

    def test_rechecks_canonical_planning_revision_before_caller_hook(self) -> None:
        payload = self._payload()
        execution = self._execution_payload(payload)
        execution["toolchain_source_root"] = str(self.implementation_root)
        execution["toolchain_commit"] = self.implementation_commit
        execution["generation_role"] = "candidate"
        execution["canonical_state_mutation_allowed"] = False
        context = context_owner.parse_cross_checkout_context(payload)
        self._move_head(self.stable_root, "canonical-planning")
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "canonical_planning_commit_before does not match HEAD for "
            "canonical_planning_repository_root",
        ):
            receipt = context_owner.build_cross_repository_receipt(
                context,
                caller="runway-worker",
                reason="test stale planning rejection",
                canonical_planning_root=self.planning_root,
            )
            hook(receipt)
        hook.assert_not_called()

    def test_rechecks_implementation_revision_before_caller_hook(self) -> None:
        context = context_owner.parse_cross_checkout_context(self._payload())
        self._move_head(self.implementation_root, "implementation")
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "implementation_commit_before does not match HEAD for "
            "implementation_target_root",
        ):
            receipt = context_owner.build_cross_repository_receipt(
                context,
                caller="runway-worker",
                reason="test stale implementation rejection",
                canonical_planning_root=self.planning_root,
            )
            hook(receipt)
        hook.assert_not_called()

    def test_validates_planning_and_implementation_write_scopes(self) -> None:
        context = context_owner.parse_cross_checkout_context(self._payload())
        planning_path = self.planning_root / "LEDGER.md"
        implementation_path = (
            self.implementation_root / "skills" / "work-batch" / "SKILL.md"
        )

        scope = context_owner.validate_write_scope(
            context,
            canonical_planning_root=self.planning_root,
            planning_paths=(planning_path,),
            implementation_paths=(implementation_path,),
        )

        self.assertEqual(
            scope,
            context_owner.AllowedWriteScope(
                canonical_planning_repository_root=self.stable_root,
                canonical_planning_root=self.planning_root,
                implementation_target_root=self.implementation_root,
                planning_paths=(planning_path.resolve(),),
                implementation_paths=(implementation_path.resolve(),),
            ),
        )

    def test_rejects_out_of_scope_writes_before_caller_hook(self) -> None:
        outside_root = self.root / "outside"
        outside_root.mkdir()
        escape_link = self.planning_root / "escape"
        escape_link.symlink_to(outside_root, target_is_directory=True)

        for scope_field, planning_paths, implementation_paths, error in (
            (
                "planning",
                (self.stable_root / "not-planning.md",),
                (),
                "planning_paths\\[0\\] must stay within "
                "canonical_planning_root=",
            ),
            (
                "implementation",
                (),
                (self.stable_root / "not-implementation.py",),
                "implementation_paths\\[0\\] must stay within "
                "implementation_target_root=",
            ),
            (
                "planning symlink escape",
                (escape_link / "escaped.md",),
                (),
                "planning_paths\\[0\\] must stay within "
                "canonical_planning_root=",
            ),
        ):
            with self.subTest(scope=scope_field):
                hook = mock.Mock()
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    error,
                ):
                    self._invoke_after_receipt_validation(
                        self._payload(),
                        hook,
                        planning_paths=planning_paths,
                        implementation_paths=implementation_paths,
                    )
                hook.assert_not_called()

    def test_rejects_caller_supplied_planning_root_outside_repository(self) -> None:
        context = context_owner.parse_cross_checkout_context(self._payload())
        outside_planning_root = self.root / "outside-planning"
        outside_planning_root.mkdir()
        proposed_path = outside_planning_root / "LEDGER.md"
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "canonical_planning_root must stay within "
            "canonical_planning_repository_root=",
        ):
            receipt = context_owner.build_cross_repository_receipt(
                context,
                caller="runway-worker",
                reason="test outside planning root rejection",
                canonical_planning_root=outside_planning_root,
                planning_paths=(proposed_path,),
            )
            hook(receipt)
        hook.assert_not_called()

    def test_rejects_canonical_writes_when_mutation_permission_is_false(self) -> None:
        candidate_payload = self._payload()
        candidate_execution = self._execution_payload(candidate_payload)
        candidate_execution["toolchain_source_root"] = str(self.implementation_root)
        candidate_execution["toolchain_commit"] = self.implementation_commit
        candidate_execution["generation_role"] = "candidate"
        candidate_execution["canonical_state_mutation_allowed"] = False

        stable_read_only_payload = self._payload()
        self._execution_payload(stable_read_only_payload)[
            "canonical_state_mutation_allowed"
        ] = False

        for payload, role in (
            (candidate_payload, "candidate"),
            (stable_read_only_payload, "stable"),
        ):
            with self.subTest(role=role):
                hook = mock.Mock()
                with (
                    mock.patch.object(
                        context_owner,
                        "AllowedWriteScope",
                        wraps=context_owner.AllowedWriteScope,
                    ) as scope_constructor,
                    mock.patch.object(
                        context_owner,
                        "CrossRepositoryReceipt",
                        wraps=context_owner.CrossRepositoryReceipt,
                    ) as receipt_constructor,
                    self.assertRaisesRegex(
                        context_owner.CrossCheckoutContextError,
                        "planning_paths require "
                        "canonical_state_mutation_allowed=true; "
                        rf"generation_role '{role}' declared false",
                    ),
                ):
                    self._invoke_after_receipt_validation(
                        payload,
                        hook,
                        planning_paths=(self.planning_root / "LEDGER.md",),
                    )
                scope_constructor.assert_not_called()
                receipt_constructor.assert_not_called()
                hook.assert_not_called()

    def test_read_only_generations_allow_implementation_only_scope(self) -> None:
        candidate_payload = self._payload()
        candidate_execution = self._execution_payload(candidate_payload)
        candidate_execution["toolchain_source_root"] = str(self.implementation_root)
        candidate_execution["toolchain_commit"] = self.implementation_commit
        candidate_execution["generation_role"] = "candidate"
        candidate_execution["canonical_state_mutation_allowed"] = False

        stable_read_only_payload = self._payload()
        self._execution_payload(stable_read_only_payload)[
            "canonical_state_mutation_allowed"
        ] = False
        implementation_path = self.implementation_root / "scripts" / "feature.py"

        for payload, role in (
            (candidate_payload, "candidate"),
            (stable_read_only_payload, "stable"),
        ):
            with self.subTest(role=role):
                context = context_owner.parse_cross_checkout_context(payload)
                receipt = context_owner.build_cross_repository_receipt(
                    context,
                    caller="runway-worker",
                    reason="test implementation-only scope",
                    canonical_planning_root=self.planning_root,
                    implementation_paths=(implementation_path,),
                )

                self.assertEqual(receipt.allowed_scope.planning_paths, ())
                self.assertEqual(
                    receipt.allowed_scope.implementation_paths,
                    (implementation_path.resolve(),),
                )

    def test_builds_exact_versioned_cross_repository_receipt(self) -> None:
        context = context_owner.parse_cross_checkout_context(self._payload())
        planning_path = self.planning_root / "LEDGER.md"
        implementation_path = self.implementation_root / "scripts" / "feature.py"

        receipt = context_owner.build_cross_repository_receipt(
            context,
            caller="work-batch",
            reason="implement the selected migration slice",
            canonical_planning_root=self.planning_root,
            planning_paths=(planning_path,),
            implementation_paths=(implementation_path,),
        )

        self.assertEqual(
            context_owner.cross_repository_receipt_to_dict(receipt),
            {
                "interface": "cross-checkout-receipt/v1",
                "caller": "work-batch",
                "reason": "implement the selected migration slice",
                "allowed_scope": {
                    "canonical_planning_repository_root": str(self.stable_root),
                    "canonical_planning_root": str(self.planning_root),
                    "implementation_target_root": str(self.implementation_root),
                    "planning_paths": [str(planning_path.resolve())],
                    "implementation_paths": [str(implementation_path.resolve())],
                },
                "generation_identity": {
                    "generation_role": "stable",
                    "toolchain_source_root": str(self.stable_root),
                    "toolchain_commit": self.stable_commit,
                    "codex_home": str(self.codex_home.resolve()),
                    "canonical_state_mutation_allowed": True,
                },
                "repository_revisions": {
                    "toolchain_commit": self.stable_commit,
                    "canonical_planning_commit_before": self.stable_commit,
                    "implementation_commit_before": self.implementation_commit,
                },
                "deletion_condition": "CCFG-29 final integration",
            },
        )
        self.assertEqual(
            [field.name for field in dataclasses.fields(receipt.repository_revisions)],
            [
                "toolchain_commit",
                "canonical_planning_commit_before",
                "implementation_commit_before",
            ],
        )

    def test_receipt_requires_caller_and_reason(self) -> None:
        context = context_owner.parse_cross_checkout_context(self._payload())

        for field, caller, reason in (
            ("caller", "", "reason"),
            ("reason", "caller", "   "),
        ):
            with self.subTest(field=field):
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    rf"receipt {field} must be a non-empty string",
                ):
                    context_owner.build_cross_repository_receipt(
                        context,
                        caller=caller,
                        reason=reason,
                        canonical_planning_root=self.planning_root,
                    )

    def test_rejects_missing_and_unsupported_fields(self) -> None:
        missing = self._payload()
        del self._execution_payload(missing)["implementation_commit_before"]
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "missing required fields: implementation_commit_before",
        ):
            context_owner.parse_cross_checkout_context(missing)

        unsupported = self._payload()
        self._execution_payload(unsupported)["select_next_batch"] = True
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "contains unsupported fields: select_next_batch",
        ):
            context_owner.parse_cross_checkout_context(unsupported)

        non_string_field = self._payload()
        untyped_execution = cast(
            dict[object, object], self._execution_payload(non_string_field)
        )
        untyped_execution[7] = True
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "contains non-string field names: 7",
        ):
            context_owner.parse_cross_checkout_context(non_string_field)

    def test_rejects_an_unsupported_interface(self) -> None:
        payload = self._payload()
        payload["interface"] = "cross-checkout-context/v2"

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "must be exactly 'cross-checkout-context/v1'",
        ):
            context_owner.parse_cross_checkout_context(payload)

    def test_rejects_relative_and_missing_roots(self) -> None:
        for field in (
            "toolchain_source_root",
            "canonical_planning_repository_root",
            "implementation_target_root",
            "codex_home",
        ):
            with self.subTest(field=field, problem="relative"):
                payload = self._payload()
                self._execution_payload(payload)[field] = "relative/path"
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    rf"{field} must be an absolute path",
                ):
                    context_owner.parse_cross_checkout_context(payload)

            with self.subTest(field=field, problem="missing"):
                payload = self._payload()
                self._execution_payload(payload)[field] = str(self.root / f"missing-{field}")
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    rf"{field} does not resolve to an existing path",
                ):
                    context_owner.parse_cross_checkout_context(payload)

    def test_rejects_overlapping_planning_implementation_and_home_roots(self) -> None:
        payload = self._payload()
        nested_implementation = self.stable_root / "candidate"
        nested_implementation.mkdir()
        self._execution_payload(payload)["implementation_target_root"] = str(
            nested_implementation
        )
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "root roles overlap: canonical_planning_repository_root=",
        ):
            context_owner.parse_cross_checkout_context(payload)

        payload = self._payload()
        nested_home = self.implementation_root / "codex-home"
        nested_home.mkdir()
        self._execution_payload(payload)["codex_home"] = str(nested_home)
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "root roles overlap: implementation_target_root=",
        ):
            context_owner.parse_cross_checkout_context(payload)

    def test_rejects_invalid_and_mismatched_revisions(self) -> None:
        for field in (
            "toolchain_commit",
            "canonical_planning_commit_before",
            "implementation_commit_before",
        ):
            with self.subTest(field=field, problem="not full length"):
                payload = self._payload()
                self._execution_payload(payload)[field] = "abc1234"
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    rf"{field} must be a full 40-character lowercase Git SHA",
                ):
                    context_owner.parse_cross_checkout_context(payload)

        for revision_field, root_field in (
            ("toolchain_commit", "toolchain_source_root"),
            (
                "canonical_planning_commit_before",
                "canonical_planning_repository_root",
            ),
            ("implementation_commit_before", "implementation_target_root"),
        ):
            with self.subTest(field=revision_field, problem="mismatched HEAD"):
                payload = self._payload()
                self._execution_payload(payload)[revision_field] = "0" * 40
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    rf"{revision_field} does not match HEAD for {root_field}",
                ):
                    context_owner.parse_cross_checkout_context(payload)

    def test_rejects_non_repository_and_nested_repository_roots(self) -> None:
        non_repository = self.root / "not-a-repository"
        non_repository.mkdir()
        payload = self._payload()
        execution = self._execution_payload(payload)
        execution["implementation_target_root"] = str(non_repository)
        execution["implementation_commit_before"] = "0" * 40
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "implementation_target_root is not a readable Git repository root",
        ):
            context_owner.parse_cross_checkout_context(payload)

        nested_root = self.implementation_root / "nested"
        nested_root.mkdir()
        payload = self._payload()
        self._execution_payload(payload)["implementation_target_root"] = str(nested_root)
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "implementation_target_root must be the Git repository root",
        ):
            context_owner.parse_cross_checkout_context(payload)

    def test_rejects_invalid_generation_and_mutation_permission(self) -> None:
        invalid_role = self._payload()
        self._execution_payload(invalid_role)["generation_role"] = "preview"
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "generation_role must be 'stable' or 'candidate'",
        ):
            context_owner.parse_cross_checkout_context(invalid_role)

        invalid_type = self._payload()
        self._execution_payload(invalid_type)["canonical_state_mutation_allowed"] = 1
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "canonical_state_mutation_allowed must be a boolean",
        ):
            context_owner.parse_cross_checkout_context(invalid_type)

        candidate_write = copy.deepcopy(self._payload())
        execution = self._execution_payload(candidate_write)
        execution["generation_role"] = "candidate"
        execution["canonical_state_mutation_allowed"] = True
        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "must be false for generation_role 'candidate'",
        ):
            context_owner.parse_cross_checkout_context(candidate_write)

    def test_public_api_is_data_only_and_has_no_workflow_authority(self) -> None:
        context = context_owner.parse_cross_checkout_context(self._payload())
        generation_identity = context_owner.capture_generation_identity(context)
        receipt = context_owner.build_cross_repository_receipt(
            context,
            caller="test",
            reason="assert public authority boundary",
            canonical_planning_root=self.planning_root,
        )

        self.assertEqual(
            context_owner.__all__,
            [
                "INTERFACE",
                "RECEIPT_INTERFACE",
                "DELETION_CONDITION",
                "GenerationRole",
                "CrossCheckoutContextError",
                "ExecutionContext",
                "CrossCheckoutContext",
                "GenerationIdentity",
                "AllowedWriteScope",
                "RepositoryRevisions",
                "CrossRepositoryReceipt",
                "parse_cross_checkout_context",
                "capture_generation_identity",
                "validate_write_scope",
                "build_cross_repository_receipt",
                "cross_repository_receipt_to_dict",
            ],
        )
        data_contracts = (
            (context, ("interface", "execution_context")),
            (
                context.execution_context,
                (
                    "toolchain_source_root",
                    "toolchain_commit",
                    "canonical_planning_repository_root",
                    "canonical_planning_commit_before",
                    "implementation_target_root",
                    "implementation_commit_before",
                    "codex_home",
                    "generation_role",
                    "canonical_state_mutation_allowed",
                ),
            ),
            (
                generation_identity,
                (
                    "generation_role",
                    "toolchain_source_root",
                    "toolchain_commit",
                    "codex_home",
                    "canonical_state_mutation_allowed",
                ),
            ),
            (
                receipt.allowed_scope,
                (
                    "canonical_planning_repository_root",
                    "canonical_planning_root",
                    "implementation_target_root",
                    "planning_paths",
                    "implementation_paths",
                ),
            ),
            (
                receipt.repository_revisions,
                (
                    "toolchain_commit",
                    "canonical_planning_commit_before",
                    "implementation_commit_before",
                ),
            ),
            (
                receipt,
                (
                    "interface",
                    "caller",
                    "reason",
                    "allowed_scope",
                    "generation_identity",
                    "repository_revisions",
                    "deletion_condition",
                ),
            ),
        )
        for value, expected_fields in data_contracts:
            with self.subTest(data_type=type(value).__name__):
                self.assertEqual(
                    tuple(field.name for field in dataclasses.fields(value)),
                    expected_fields,
                )
                self.assertEqual(
                    {name for name in dir(value) if not name.startswith("_")},
                    set(expected_fields),
                )
                with self.assertRaises(dataclasses.FrozenInstanceError):
                    setattr(value, expected_fields[0], object())


if __name__ == "__main__":
    unittest.main()
