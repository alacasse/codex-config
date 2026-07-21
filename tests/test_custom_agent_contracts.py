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


def test_import_topology_reviewer_reports_findings_without_a_result_schema() -> None:
    text = instructions("import_topology_reviewer")
    for guidance in (
        "Lead with whether the exact diff is clean",
        "Order actionable findings by severity",
        "cite precise files and lines",
        "State the exact diff basis used",
    ):
        assert guidance in text
    assert "Return YAML only" not in text
    assert "exactly these top-level fields" not in text
