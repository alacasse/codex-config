from __future__ import annotations

import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def instructions(name: str) -> str:
    path = REPO_ROOT / "agents" / f"{name}.toml"
    return tomllib.loads(path.read_text(encoding="utf-8"))["developer_instructions"]


def test_import_topology_reviewer_has_one_narrow_review_lens() -> None:
    text = instructions("import_topology_reviewer")
    for expected in (
        "project-local imports",
        "sys.path mutation",
        "one canonical import topology",
        "Temporary compatibility needs a named caller",
        "Remain read-only",
        "Never spawn, delegate to, or wait",
    ):
        assert expected in text
    assert "Do not broaden into general architecture" in text


def test_import_topology_reviewer_returns_a_fixed_result_shape() -> None:
    text = instructions("import_topology_reviewer")
    for field in (
        "status: clean | findings | blocked",
        "diff_basis: string",
        "findings: []",
        "residual_risks: []",
        "required_fixes: []",
    ):
        assert field in text
    assert "severity, file, issue, and evidence" in text
