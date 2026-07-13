from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import cast
from unittest import mock

from scripts import cross_checkout_context as context_owner


class CrossCheckoutPrecreationTests(unittest.TestCase):
    repository_identity = "example/codex-config"
    repository_remote = "https://github.com/example/codex-config.git"
    implementation_branch = "command-owner-redesign"

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name).resolve()
        self.stable_root = self.root / "stable"
        self._git_init(self.stable_root)
        self._git(self.stable_root, "remote", "add", "origin", self.repository_remote)
        self._commit_file(self.stable_root, "identity.txt", "stable\n", "Initial")

        self._git(self.stable_root, "switch", "-c", "accepted-design")
        self.accepted_design_snapshot = self._commit_file(
            self.stable_root,
            "accepted-design.txt",
            "accepted design\n",
            "Accepted design",
        )
        self._git(self.stable_root, "switch", "master")
        self.stable_commit = self._commit_file(
            self.stable_root,
            "authoritative-base.txt",
            "authoritative master\n",
            "Authoritative base",
        )

        self.planning_root = self.stable_root / "docs" / "plans"
        self.planning_root.mkdir(parents=True)
        self.stable_codex_home = self.root / "stable-codex-home"
        self.stable_codex_home.mkdir()
        self.implementation_target = self.root / "candidate"
        self.candidate_codex_home = self.root / "candidate-codex-home"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _git_init(self, root: Path) -> None:
        root.mkdir()
        self._git(root, "init", "--quiet", "--initial-branch=master")
        self._git(root, "config", "user.email", "tests@example.invalid")
        self._git(root, "config", "user.name", "Precreation Tests")

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

    def _commit_file(
        self,
        root: Path,
        name: str,
        content: str,
        message: str,
    ) -> str:
        (root / name).write_text(content, encoding="utf-8")
        self._git(root, "add", name)
        self._git(root, "commit", "--quiet", "-m", message)
        return self._git(root, "rev-parse", "HEAD")

    def _payload(self) -> dict[str, object]:
        return {
            "interface": context_owner.PRECREATION_INTERFACE,
            "stable_control": {
                "toolchain_source_root": str(self.stable_root),
                "toolchain_commit": self.stable_commit,
                "canonical_planning_repository_root": str(self.stable_root),
                "canonical_planning_commit_before": self.stable_commit,
                "canonical_planning_root": str(self.planning_root),
                "codex_home": str(self.stable_codex_home),
                "generation_role": "stable",
                "canonical_state_mutation_allowed": True,
            },
            "candidate_intent": {
                "implementation_target_root": str(self.implementation_target),
                "expected_repository_state": "absent",
                "candidate_codex_home": str(self.candidate_codex_home),
                "expected_codex_home_state": "absent",
                "base_repository": self.repository_identity,
                "base_commit": self.stable_commit,
                "implementation_branch": self.implementation_branch,
                "accepted_design_snapshot": self.accepted_design_snapshot,
            },
            "creation_authority": {
                "repository_creation_allowed": True,
                "candidate_codex_home_creation_allowed": True,
                "allowed_creation_roots": [
                    str(self.implementation_target),
                    str(self.candidate_codex_home),
                ],
            },
        }

    def _stable_payload(self, payload: dict[str, object]) -> dict[str, object]:
        return cast(dict[str, object], payload["stable_control"])

    def _candidate_payload(self, payload: dict[str, object]) -> dict[str, object]:
        return cast(dict[str, object], payload["candidate_intent"])

    def _authority_payload(self, payload: dict[str, object]) -> dict[str, object]:
        return cast(dict[str, object], payload["creation_authority"])

    def _replace_candidate_path(
        self,
        payload: dict[str, object],
        *,
        field: str,
        value: Path | str,
    ) -> None:
        candidate = self._candidate_payload(payload)
        candidate[field] = str(value)
        authority = self._authority_payload(payload)
        authority["allowed_creation_roots"] = [
            candidate["implementation_target_root"],
            candidate["candidate_codex_home"],
        ]

    def _move_stable_head(self) -> None:
        self._commit_file(
            self.stable_root,
            "stable-drift.txt",
            "drift\n",
            "Move stable HEAD",
        )

    def _create_candidate(
        self,
        *,
        branch: str | None = None,
        start_revision: str | None = None,
        merge_design: bool = True,
        create_home: bool = True,
        remote: str | None = None,
    ) -> str:
        subprocess.run(
            [
                "git",
                "clone",
                "--quiet",
                str(self.stable_root),
                str(self.implementation_target),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self._git(
            self.implementation_target,
            "remote",
            "set-url",
            "origin",
            remote or self.repository_remote,
        )
        self._git(
            self.implementation_target,
            "config",
            "user.email",
            "tests@example.invalid",
        )
        self._git(
            self.implementation_target,
            "config",
            "user.name",
            "Precreation Tests",
        )
        switch_args = ["switch", "-c", branch or self.implementation_branch]
        if start_revision is not None:
            switch_args.append(start_revision)
        self._git(self.implementation_target, *switch_args)
        if merge_design:
            self._git(
                self.implementation_target,
                "merge",
                "--quiet",
                "--no-ff",
                "-m",
                "Merge accepted design",
                self.accepted_design_snapshot,
            )
        if create_home:
            self.candidate_codex_home.mkdir()
        return self._git(self.implementation_target, "rev-parse", "HEAD")

    def _strict_payload(
        self,
        candidate_commit: str,
        *,
        generation_role: str = "candidate",
        codex_home: Path | None = None,
    ) -> dict[str, object]:
        if generation_role == "candidate":
            toolchain_root = self.implementation_target
            toolchain_commit = candidate_commit
            selected_home = codex_home or self.candidate_codex_home
            mutation_allowed = False
        else:
            toolchain_root = self.stable_root
            toolchain_commit = self.stable_commit
            selected_home = codex_home or self.stable_codex_home
            mutation_allowed = True
        return {
            "interface": context_owner.INTERFACE,
            "execution_context": {
                "toolchain_source_root": str(toolchain_root),
                "toolchain_commit": toolchain_commit,
                "canonical_planning_repository_root": str(self.stable_root),
                "canonical_planning_commit_before": self.stable_commit,
                "implementation_target_root": str(self.implementation_target),
                "implementation_commit_before": candidate_commit,
                "codex_home": str(selected_home),
                "generation_role": generation_role,
                "canonical_state_mutation_allowed": mutation_allowed,
            },
        }

    def _invoke_after_authorization(
        self,
        context: context_owner.CrossCheckoutPrecreationContext,
        hook: mock.Mock,
        *targets: Path,
    ) -> None:
        scope = context_owner.validate_precreation_creation_targets(
            context,
            creation_targets=targets,
        )
        hook(scope)

    def _invoke_after_transition(
        self,
        precreation: context_owner.CrossCheckoutPrecreationContext,
        strict: context_owner.CrossCheckoutContext,
        hook: mock.Mock,
    ) -> None:
        receipt = context_owner.build_cross_checkout_transition_receipt(
            precreation,
            strict,
        )
        hook(receipt)

    def test_parses_and_round_trips_the_exact_three_part_shape(self) -> None:
        payload = self._payload()

        context = context_owner.parse_cross_checkout_precreation(payload)

        self.assertEqual(context.interface, "cross-checkout-precreation/v1")
        self.assertEqual(
            context.creation_authority.allowed_creation_roots,
            (self.implementation_target, self.candidate_codex_home),
        )
        self.assertEqual(
            context_owner.cross_checkout_precreation_to_dict(context),
            payload,
        )

    def test_rejects_missing_extra_and_mistyped_shape_fields(self) -> None:
        cases: list[tuple[str, dict[str, object]]] = []

        missing_top = self._payload()
        del missing_top["stable_control"]
        cases.append(("missing top-level", missing_top))

        extra_top = self._payload()
        extra_top["workflow_authority"] = True
        cases.append(("extra top-level", extra_top))

        missing_nested = self._payload()
        del self._candidate_payload(missing_nested)["base_commit"]
        cases.append(("missing nested", missing_nested))

        extra_nested = self._payload()
        self._authority_payload(extra_nested)["parent_creation_allowed"] = True
        cases.append(("extra nested", extra_nested))

        mistyped_part = self._payload()
        mistyped_part["stable_control"] = "stable"
        cases.append(("mistyped part", mistyped_part))

        mistyped_roots = self._payload()
        self._authority_payload(mistyped_roots)["allowed_creation_roots"] = tuple(
            cast(
                list[object],
                self._authority_payload(mistyped_roots)["allowed_creation_roots"],
            )
        )
        cases.append(("mistyped roots", mistyped_roots))

        for label, payload in cases:
            with self.subTest(case=label):
                with self.assertRaises(context_owner.CrossCheckoutContextError):
                    context_owner.parse_cross_checkout_precreation(payload)

    def test_rejects_non_exact_interface_states_and_authority(self) -> None:
        mutations = (
            ("interface", None, "cross-checkout-precreation/v2"),
            ("generation", "generation_role", "candidate"),
            ("mutation", "canonical_state_mutation_allowed", False),
            ("repository state", "expected_repository_state", "empty"),
            ("home state", "expected_codex_home_state", "empty"),
            ("repository authority", "repository_creation_allowed", False),
            (
                "home authority",
                "candidate_codex_home_creation_allowed",
                False,
            ),
        )
        for label, field, value in mutations:
            payload = self._payload()
            if label == "interface":
                payload["interface"] = value
            elif label in {"generation", "mutation"}:
                self._stable_payload(payload)[cast(str, field)] = value
            elif label in {"repository state", "home state"}:
                self._candidate_payload(payload)[cast(str, field)] = value
            else:
                self._authority_payload(payload)[cast(str, field)] = value
            with self.subTest(case=label):
                with self.assertRaises(context_owner.CrossCheckoutContextError):
                    context_owner.parse_cross_checkout_precreation(payload)

    def test_rejects_relative_duplicate_and_broadened_declared_targets(self) -> None:
        relative = self._payload()
        self._replace_candidate_path(
            relative,
            field="implementation_target_root",
            value="relative-candidate",
        )

        duplicate = self._payload()
        self._replace_candidate_path(
            duplicate,
            field="candidate_codex_home",
            value=self.implementation_target,
        )

        broadened = self._payload()
        authority = self._authority_payload(broadened)
        authority["allowed_creation_roots"] = [
            str(self.implementation_target.parent),
            str(self.candidate_codex_home),
        ]

        for label, payload in (
            ("relative", relative),
            ("duplicate", duplicate),
            ("broadened", broadened),
        ):
            with self.subTest(case=label):
                with self.assertRaises(context_owner.CrossCheckoutContextError):
                    context_owner.parse_cross_checkout_precreation(payload)

    def test_rejects_existing_candidate_paths_even_when_empty(self) -> None:
        for field, path in (
            ("implementation_target_root", self.implementation_target),
            ("candidate_codex_home", self.candidate_codex_home),
        ):
            with self.subTest(field=field):
                path.mkdir()
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    "must be absent",
                ):
                    context_owner.parse_cross_checkout_precreation(self._payload())
                path.rmdir()

    def test_rejects_broken_symlink_as_existing_candidate_state(self) -> None:
        self.implementation_target.symlink_to(self.root / "missing-target")

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "must be absent",
        ):
            context_owner.parse_cross_checkout_precreation(self._payload())

    def test_rejects_candidate_overlap_with_protected_and_candidate_roots(self) -> None:
        protected = self._payload()
        self._replace_candidate_path(
            protected,
            field="implementation_target_root",
            value=self.stable_root / "candidate",
        )

        candidate_overlap = self._payload()
        self._replace_candidate_path(
            candidate_overlap,
            field="candidate_codex_home",
            value=self.implementation_target / "codex-home",
        )

        for label, payload in (
            ("protected", protected),
            ("candidate", candidate_overlap),
        ):
            with self.subTest(case=label):
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    "overlap",
                ):
                    context_owner.parse_cross_checkout_precreation(payload)

    def test_rejects_stable_generation_and_planning_root_mismatches(self) -> None:
        commit_mismatch = self._payload()
        self._stable_payload(commit_mismatch)["toolchain_commit"] = (
            self.accepted_design_snapshot
        )

        outside_planning = self.root / "outside-planning"
        outside_planning.mkdir()
        planning_mismatch = self._payload()
        self._stable_payload(planning_mismatch)["canonical_planning_root"] = str(
            outside_planning
        )

        for label, payload in (
            ("generation commit", commit_mismatch),
            ("planning root", planning_mismatch),
        ):
            with self.subTest(case=label):
                with self.assertRaises(context_owner.CrossCheckoutContextError):
                    context_owner.parse_cross_checkout_precreation(payload)

    def test_rejects_invalid_repository_revision_branch_and_design_identity(
        self,
    ) -> None:
        remote_mismatch = self._payload()
        self._candidate_payload(remote_mismatch)["base_repository"] = "other/repo"

        short_base = self._payload()
        self._candidate_payload(short_base)["base_commit"] = self.stable_commit[:12]

        stale_base = self._payload()
        self._candidate_payload(stale_base)["base_commit"] = (
            self.accepted_design_snapshot
        )

        invalid_branch = self._payload()
        self._candidate_payload(invalid_branch)["implementation_branch"] = "bad..branch"

        missing_snapshot = self._payload()
        self._candidate_payload(missing_snapshot)["accepted_design_snapshot"] = "f" * 40

        for label, payload in (
            ("remote", remote_mismatch),
            ("short base", short_base),
            ("stale base", stale_base),
            ("branch", invalid_branch),
            ("snapshot", missing_snapshot),
        ):
            with self.subTest(case=label):
                with self.assertRaises(context_owner.CrossCheckoutContextError):
                    context_owner.parse_cross_checkout_precreation(payload)

    def test_rejects_ambiguous_relative_origin_identity(self) -> None:
        self._git(
            self.stable_root,
            "remote",
            "set-url",
            "origin",
            self.repository_identity,
        )

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "unambiguous repository identity",
        ):
            context_owner.parse_cross_checkout_precreation(self._payload())

    def test_rejects_multiple_origin_urls_as_ambiguous_identity(self) -> None:
        self._git(
            self.stable_root,
            "remote",
            "set-url",
            "--add",
            "origin",
            "git@github.com:example/codex-config.git",
        )

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "exactly one repository URL",
        ):
            context_owner.parse_cross_checkout_precreation(self._payload())

    def test_authorizes_only_exact_declared_targets(self) -> None:
        context = context_owner.parse_cross_checkout_precreation(self._payload())

        both = context_owner.validate_precreation_creation_targets(
            context,
            creation_targets=(
                self.implementation_target,
                self.candidate_codex_home,
            ),
        )
        repository_only = context_owner.validate_precreation_creation_targets(
            context,
            creation_targets=(self.implementation_target,),
        )

        self.assertEqual(
            both.creation_roots,
            (self.implementation_target, self.candidate_codex_home),
        )
        self.assertEqual(repository_only.creation_roots, (self.implementation_target,))

        unauthorized = (
            self.implementation_target.parent,
            self.root / "candidate-sibling",
            self.implementation_target / "descendant",
            self.root / "undeclared",
        )
        for target in unauthorized:
            with self.subTest(target=target):
                hook = mock.Mock()
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    "not an exact authorized root",
                ):
                    self._invoke_after_authorization(context, hook, target)
                hook.assert_not_called()

    def test_rejects_duplicate_or_relative_requested_targets_before_hook(self) -> None:
        context = context_owner.parse_cross_checkout_precreation(self._payload())
        cases: tuple[tuple[object, ...], ...] = (
            (self.implementation_target, self.implementation_target),
            (Path("relative-candidate"),),
        )
        for targets in cases:
            with self.subTest(targets=targets):
                hook = mock.Mock()
                with self.assertRaises(context_owner.CrossCheckoutContextError):
                    scope = context_owner.validate_precreation_creation_targets(
                        context,
                        creation_targets=cast(tuple[Path, ...], targets),
                    )
                    hook(scope)
                hook.assert_not_called()

    def test_rejects_aliased_requested_target_before_hook(self) -> None:
        context = context_owner.parse_cross_checkout_precreation(self._payload())
        alias = self.root / "candidate-alias"
        alias.symlink_to(self.implementation_target)
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "not an alias",
        ):
            self._invoke_after_authorization(context, hook, alias)
        hook.assert_not_called()

    def test_rejects_lexical_and_symlink_parent_candidate_intent_aliases(
        self,
    ) -> None:
        alias_parent = self.root / "candidate-parent-alias"
        alias_parent.symlink_to(self.root, target_is_directory=True)

        lexical_payload = self._payload()
        self._replace_candidate_path(
            lexical_payload,
            field="implementation_target_root",
            value=self.root / "unused-parent" / ".." / "candidate",
        )
        symlink_payload = self._payload()
        self._replace_candidate_path(
            symlink_payload,
            field="implementation_target_root",
            value=alias_parent / "candidate",
        )

        for label, payload in (
            ("lexical", lexical_payload),
            ("symlink parent", symlink_payload),
        ):
            with self.subTest(case=label):
                authorization_hook = mock.Mock()
                transition_hook = mock.Mock()
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    "must equal its resolved absolute path",
                ):
                    context = context_owner.parse_cross_checkout_precreation(payload)
                    authorization_hook(context)
                    transition_hook(context)
                authorization_hook.assert_not_called()
                transition_hook.assert_not_called()

    def test_rejects_lexical_and_symlink_parent_creation_authority_aliases(
        self,
    ) -> None:
        alias_parent = self.root / "authority-parent-alias"
        alias_parent.symlink_to(self.root, target_is_directory=True)

        lexical_payload = self._payload()
        lexical_authority = self._authority_payload(lexical_payload)
        lexical_authority["allowed_creation_roots"] = [
            str(self.root / "unused-parent" / ".." / "candidate"),
            str(self.candidate_codex_home),
        ]
        symlink_payload = self._payload()
        symlink_authority = self._authority_payload(symlink_payload)
        symlink_authority["allowed_creation_roots"] = [
            str(alias_parent / "candidate"),
            str(self.candidate_codex_home),
        ]

        for label, payload in (
            ("lexical", lexical_payload),
            ("symlink parent", symlink_payload),
        ):
            with self.subTest(case=label):
                authorization_hook = mock.Mock()
                transition_hook = mock.Mock()
                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    "must equal its resolved absolute path",
                ):
                    context = context_owner.parse_cross_checkout_precreation(payload)
                    authorization_hook(context)
                    transition_hook(context)
                authorization_hook.assert_not_called()
                transition_hook.assert_not_called()

    def test_revalidates_stable_revision_before_creation_hook(self) -> None:
        context = context_owner.parse_cross_checkout_precreation(self._payload())
        self._move_stable_head()
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "does not match HEAD",
        ):
            self._invoke_after_authorization(
                context,
                hook,
                self.implementation_target,
            )
        hook.assert_not_called()

    def test_revalidates_stable_directories_before_creation_hook(self) -> None:
        context = context_owner.parse_cross_checkout_precreation(self._payload())
        self.planning_root.rmdir()
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "no longer resolves to an existing directory",
        ):
            self._invoke_after_authorization(
                context,
                hook,
                self.implementation_target,
            )
        hook.assert_not_called()

    def test_rejects_candidate_state_created_after_parse_before_hook(self) -> None:
        for path in (self.implementation_target, self.candidate_codex_home):
            with self.subTest(path=path):
                context = context_owner.parse_cross_checkout_precreation(
                    self._payload()
                )
                path.mkdir()
                hook = mock.Mock()

                with self.assertRaisesRegex(
                    context_owner.CrossCheckoutContextError,
                    "must remain absent",
                ):
                    self._invoke_after_authorization(context, hook, path)
                hook.assert_not_called()
                path.rmdir()

    def test_builds_versioned_transition_evidence_bound_to_both_contexts(self) -> None:
        payload = self._payload()
        precreation = context_owner.parse_cross_checkout_precreation(payload)
        candidate_commit = self._create_candidate()
        strict_payload = self._strict_payload(candidate_commit)
        strict = context_owner.parse_cross_checkout_context(strict_payload)

        receipt = context_owner.build_cross_checkout_transition_receipt(
            precreation,
            strict,
        )
        evidence = context_owner.cross_checkout_transition_receipt_to_dict(receipt)

        self.assertEqual(
            evidence,
            {
                "interface": "cross-checkout-transition-receipt/v1",
                "precreation_context": payload,
                "created_candidate_identity": {
                    "implementation_target_root": str(self.implementation_target),
                    "implementation_commit": candidate_commit,
                    "implementation_branch": self.implementation_branch,
                    "candidate_codex_home": str(self.candidate_codex_home),
                    "base_repository": self.repository_identity,
                    "base_commit": self.stable_commit,
                    "accepted_design_snapshot": self.accepted_design_snapshot,
                },
                "strict_context": strict_payload,
                "deletion_condition": "CCFG-29 final integration",
            },
        )
        self.assertEqual(
            set(evidence),
            {
                "interface",
                "precreation_context",
                "created_candidate_identity",
                "strict_context",
                "deletion_condition",
            },
        )
        self.assertNotIn("accepted", evidence)
        self.assertNotIn("closeout", evidence)

    def test_transition_accepts_stable_strict_generation_binding(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate()
        strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit, generation_role="stable")
        )

        receipt = context_owner.build_cross_checkout_transition_receipt(
            precreation,
            strict,
        )

        self.assertEqual(
            receipt.strict_context.execution_context.generation_role,
            "stable",
        )
        self.assertEqual(
            receipt.created_candidate_identity.candidate_codex_home,
            self.candidate_codex_home,
        )

    def test_rejects_transition_with_non_strict_interface_before_hook(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate()
        parsed_strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit)
        )
        non_strict = context_owner.CrossCheckoutContext(
            interface="cross-checkout-context/v2",
            execution_context=parsed_strict.execution_context,
        )
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "strict_context.interface must be exactly",
        ):
            self._invoke_after_transition(precreation, non_strict, hook)
        hook.assert_not_called()

    def test_rejects_transition_with_wrong_candidate_remote_before_hook(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate(
            remote="https://github.com/other/repo.git"
        )
        strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit)
        )
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "origin identity does not match",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()

    def test_rejects_transition_without_declared_branch_before_hook(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate(branch="other-branch")
        strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit)
        )
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "branch does not match",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()

    def test_rejects_transition_without_design_ancestry_before_hook(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate(merge_design=False)
        strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit)
        )
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "accepted_design_snapshot is not an ancestor",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()

    def test_rejects_transition_without_exact_created_candidate_home(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate(create_home=False)
        strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit, generation_role="stable")
        )
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "candidate CODEX_HOME does not exist",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()

    def test_rejects_transition_after_candidate_head_drift_before_hook(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate()
        strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit, generation_role="stable")
        )
        self._commit_file(
            self.implementation_target,
            "candidate-drift.txt",
            "drift\n",
            "Move candidate HEAD",
        )
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "implementation_commit_before does not match HEAD",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()

    def test_rejects_valid_strict_target_mismatch_before_hook(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        other_target = self.root / "other-candidate"
        subprocess.run(
            ["git", "clone", "--quiet", str(self.stable_root), str(other_target)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        other_commit = self._git(other_target, "rev-parse", "HEAD")
        strict_payload = self._strict_payload(
            other_commit,
            generation_role="stable",
        )
        strict_execution = cast(dict[str, object], strict_payload["execution_context"])
        strict_execution["implementation_target_root"] = str(other_target)
        strict = context_owner.parse_cross_checkout_context(strict_payload)
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "implementation target does not match pre-creation intent",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()

    def test_rejects_valid_strict_codex_home_mismatch_before_hook(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate()
        other_codex_home = self.root / "other-codex-home"
        other_codex_home.mkdir()
        strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit, codex_home=other_codex_home)
        )
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "generation identity does not match",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()

    def test_rejects_second_canonical_repository_and_revision_before_hook(
        self,
    ) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate()
        other_canonical_root = self.root / "other-canonical"
        self._git_init(other_canonical_root)
        other_canonical_commit = self._commit_file(
            other_canonical_root,
            "identity.txt",
            "other canonical planning repository\n",
            "Initialize other canonical repository",
        )
        strict_payload = self._strict_payload(
            candidate_commit,
            generation_role="stable",
        )
        strict_execution = cast(dict[str, object], strict_payload["execution_context"])
        strict_execution.update(
            {
                "toolchain_source_root": str(other_canonical_root),
                "toolchain_commit": other_canonical_commit,
                "canonical_planning_repository_root": str(other_canonical_root),
                "canonical_planning_commit_before": other_canonical_commit,
            }
        )
        strict = context_owner.parse_cross_checkout_context(strict_payload)
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "canonical planning repository does not match",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()

    def test_rejects_design_snapshot_without_declared_base_ancestry(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate(
            start_revision=self.accepted_design_snapshot,
            merge_design=False,
        )
        strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit)
        )
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "base_commit is not an ancestor",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()

    def test_rejects_transition_after_stable_revision_drift_before_hook(self) -> None:
        precreation = context_owner.parse_cross_checkout_precreation(self._payload())
        candidate_commit = self._create_candidate()
        strict = context_owner.parse_cross_checkout_context(
            self._strict_payload(candidate_commit)
        )
        self._move_stable_head()
        hook = mock.Mock()

        with self.assertRaisesRegex(
            context_owner.CrossCheckoutContextError,
            "does not match HEAD",
        ):
            self._invoke_after_transition(precreation, strict, hook)
        hook.assert_not_called()


if __name__ == "__main__":
    unittest.main()
