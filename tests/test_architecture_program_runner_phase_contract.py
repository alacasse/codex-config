from __future__ import annotations

import unittest

from scripts import architecture_program_runner_command as command_owner
from scripts import architecture_program_runner_environment as environment_owner
from scripts import architecture_program_runner_phase_contract as phase_contract_owner

from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)


class ArchitectureProgramRunnerPhaseContractTests(ArchitectureProgramRunnerTestCase):
    def prompt_for_phase(self, phase: str) -> str:
        return command_owner.build_prompt(
            self.config,
            runner.initial_state(self.config),
            phase,
        )

    def test_phase_contract_names_shared_single_level_obligations_without_environment_facts(
        self,
    ) -> None:
        required_lines = (
            "- Do not run codex exec from inside this phase.",
            "- Do not launch the local architecture program runner from inside this phase.",
            "- Do not probe nested Codex availability or create temporary CODEX_HOME workarounds.",
        )

        for phase in runner.PHASES:
            with self.subTest(phase=phase):
                contract = phase_contract_owner.build_phase_contract(phase)
                for line in required_lines:
                    self.assertIn(line, contract.single_level_boundary_obligations)

    def test_phase_contract_names_shared_result_obligations_without_state_ownership(
        self,
    ) -> None:
        required_lines = (
            "Return schema-valid JSON as the final response.",
            "Write the same JSON object to a compact phase receipt file.",
            "Return the receipt path in receipt_path.",
            "Use compact strings or null for validation_summary and review_summary.",
            "Do not parse or edit runner state directly.",
        )

        for phase in runner.PHASES:
            with self.subTest(phase=phase):
                contract = phase_contract_owner.build_phase_contract(phase)
                for line in required_lines:
                    self.assertIn(line, contract.shared_result_obligations)

    def test_phase_contract_catalogs_phase_specific_obligations_and_next_phase(
        self,
    ) -> None:
        phase_requirements = {
            "select-dispatch": (
                "- Select exactly one next executable batch.",
                "- Create or refresh one compact dispatch packet.",
                "- Do not create a Batch Runway spec.",
                "- Do not execute code.",
                "- Use next_phase=create-spec when completed.",
            ),
            "create-spec": (
                "- Read the dispatch packet as primary input.",
                "- Read only minimum ledger context needed for status and evidence.",
                "- Create exactly one concrete Batch Runway spec.",
                "- Do not execute code.",
                "- Use next_phase=execute when completed.",
            ),
            "execute": (
                "- Read and execute exactly the generated Batch Runway spec.",
                "- Preserve normal runway_worker and runway_reviewer delegation.",
                "- Stop on validation, review, dirty-file conflict, or active spec stop conditions.",
                (
                    "- Run canonical validation from the execute coordinator shell; do not "
                    "treat subagent-only validation output as canonical when runner env "
                    "overrides are involved."
                ),
                (
                    "- If validation stops, summarize exact canonical command lines "
                    "attempted, whether runner env override keys were present in the "
                    "command environment, whether path-like override values were readable "
                    "without disclosing values, fallback validation attempted/passed, "
                    "likely failure class, and dirty files remaining."
                ),
                "- Use next_phase=closeout when completed.",
            ),
            "closeout": (
                "- Reconcile compact execution evidence back into the program ledger.",
                "- Do not paste execution logs into the ledger.",
                "- Write or update compact closeout telemetry as project file evidence.",
                "- Use existing state, receipt, ledger, and evidence files only.",
                "- Update telemetry without launching another Codex process.",
                "- Use next_phase=select-dispatch only when another batch is allowed and ready.",
                (
                    "- Use next_phase=select-dispatch when another safe executable batch is "
                    "ready and the batch limit permits it."
                ),
                "- Use next_phase=done when the batch limit is reached or no next batch is ready.",
            ),
        }

        for phase, expected_requirements in phase_requirements.items():
            with self.subTest(phase=phase):
                contract = phase_contract_owner.build_phase_contract(phase)
                self.assertEqual(contract.phase_requirements, expected_requirements)

    def test_phase_contract_catalogs_env_override_validation_obligations(self) -> None:
        contract = phase_contract_owner.build_phase_contract("execute")

        self.assertEqual(
            contract.env_override_validation_obligations,
            (
                "Do not disclose runner env override values.",
                (
                    "Before validation that depends on these keys, run a "
                    "coordinator-shell environment probe and record only "
                    "key-present/readable-path booleans."
                ),
            ),
        )

    def test_phase_contract_allows_create_spec_to_finish_when_execution_is_disabled(
        self,
    ) -> None:
        config = runner.RunnerConfig(
            **{**self.config.__dict__, "execute_batches": False}
        )

        contract = phase_contract_owner.build_phase_contract(
            "create-spec",
            execute_batches=config.execute_batches,
        )

        self.assertIn("- Use next_phase=done when completed.", contract.phase_requirements)

    def test_env_override_validation_contract_uses_phase_environment_inputs(
        self,
    ) -> None:
        secret_value = "secret-token"
        cache_value = "/tmp/cache-path-sentinel"
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "env_overrides": (
                    ("UV_CACHE_DIR", cache_value),
                    ("TOKEN", secret_value),
                ),
            }
        )
        environment = environment_owner.build_phase_environment(
            config,
            runner.initial_state(config),
            "execute",
        )

        prompt = command_owner.build_prompt(
            config,
            runner.initial_state(config),
            "execute",
            environment=environment,
        )

        self.assertEqual(environment.env_override_key_label, "UV_CACHE_DIR, TOKEN")
        self.assertEqual(
            environment.subprocess_env(config.env_overrides, base_env={})["TOKEN"],
            secret_value,
        )
        self.assertIn("Runner env override keys: UV_CACHE_DIR, TOKEN", prompt)
        self.assertIn("Do not disclose runner env override values.", prompt)
        self.assertIn("coordinator-shell environment probe", prompt)
        self.assertIn("key-present/readable-path booleans", prompt)
        self.assertIn("exact canonical command lines attempted", prompt)
        self.assertIn("runner env override keys were present", prompt)
        self.assertIn("path-like override values were readable without disclosing values", prompt)
        self.assertNotIn(secret_value, prompt)
        self.assertNotIn(cache_value, prompt)

    def test_phase_contract_routes_skills_for_all_fixed_phases(self) -> None:
        expected = {
            "select-dispatch": "$architecture-program-runway in select-next-batch mode",
            "create-spec": "$architecture-program-runway in create-next-runway mode",
            "execute": "$batch-runway execute-spec",
            "closeout": "$architecture-program-runway closeout-runway",
        }

        for phase, skill_instruction in expected.items():
            with self.subTest(phase=phase):
                contract = phase_contract_owner.build_phase_contract(phase)

                self.assertEqual(contract.phase, phase)
                self.assertEqual(contract.skill_instruction, skill_instruction)
                self.assertEqual(
                    command_owner.phase_skill_instruction(phase),
                    skill_instruction,
                )

    def test_phase_contract_rejects_unknown_phase(self) -> None:
        with self.assertRaisesRegex(runner.RunnerError, "unknown phase: unknown"):
            phase_contract_owner.build_phase_contract("unknown")

        with self.assertRaisesRegex(runner.RunnerError, "unknown phase: unknown"):
            command_owner.phase_skill_instruction("unknown")

    def test_prompts_render_contract_obligations_for_all_fixed_phases(self) -> None:
        for phase in runner.PHASES:
            with self.subTest(phase=phase):
                contract = phase_contract_owner.build_phase_contract(
                    phase,
                    execute_batches=self.config.execute_batches,
                )
                prompt = self.prompt_for_phase(phase)

                self.assertIn(f"Use {contract.skill_instruction}.", prompt)
                for line in contract.single_level_boundary_obligations:
                    self.assertIn(line, prompt)
                for line in contract.shared_result_obligations:
                    self.assertIn(line, prompt)
                for line in contract.phase_requirements:
                    self.assertIn(line, prompt)


if __name__ == "__main__":
    unittest.main()
