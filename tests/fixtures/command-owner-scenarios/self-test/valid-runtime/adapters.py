from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path


def waiting_observation(
    _scenario: Mapping[str, object],
    _fixture_root: Path,
) -> None:
    return None


def matching_observation(
    _scenario: Mapping[str, object],
    _fixture_root: Path,
) -> Mapping[str, object]:
    return {
        "transition": "observed",
        "writes": ["results/evidence.json"],
        "forbidden_writes": ["outside/forbidden.txt"],
        "stop_reason": None,
        "generation_and_roots": {
            "generation": "candidate",
            "roots": [{"role": "fixture", "path": "roots/fixture"}],
        },
        "validation": ["focused.green"],
    }


def mismatching_observation(
    scenario: Mapping[str, object],
    fixture_root: Path,
) -> Mapping[str, object]:
    observation = dict(matching_observation(scenario, fixture_root))
    observation["writes"] = ["results/wrong.json"]
    return observation
