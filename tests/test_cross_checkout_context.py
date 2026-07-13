from __future__ import annotations

import copy
import dataclasses
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import cast

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

        self.assertEqual(
            context_owner.__all__,
            [
                "INTERFACE",
                "GenerationRole",
                "CrossCheckoutContextError",
                "ExecutionContext",
                "CrossCheckoutContext",
                "parse_cross_checkout_context",
            ],
        )
        self.assertEqual(
            [field.name for field in dataclasses.fields(context)],
            ["interface", "execution_context"],
        )
        self.assertEqual(
            [
                field.name
                for field in dataclasses.fields(context.execution_context)
            ],
            [
                "toolchain_source_root",
                "toolchain_commit",
                "canonical_planning_repository_root",
                "canonical_planning_commit_before",
                "implementation_target_root",
                "implementation_commit_before",
                "codex_home",
                "generation_role",
                "canonical_state_mutation_allowed",
            ],
        )
        self.assertEqual(
            {name for name in dir(context) if not name.startswith("_")},
            {"interface", "execution_context"},
        )
        self.assertEqual(
            {
                name
                for name in dir(context.execution_context)
                if not name.startswith("_")
            },
            {
                "toolchain_source_root",
                "toolchain_commit",
                "canonical_planning_repository_root",
                "canonical_planning_commit_before",
                "implementation_target_root",
                "implementation_commit_before",
                "codex_home",
                "generation_role",
                "canonical_state_mutation_allowed",
            },
        )
        with self.assertRaises(dataclasses.FrozenInstanceError):
            setattr(context, "interface", "cross-checkout-context/v2")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            setattr(context.execution_context, "generation_role", "candidate")


if __name__ == "__main__":
    unittest.main()
