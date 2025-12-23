from __future__ import annotations

from pathlib import Path

from aros import checks


def test_run_checks_returns_expected_order(tmp_path: Path) -> None:
    temp_readme = tmp_path / "README.md"
    temp_readme.write_text("Test", encoding="utf-8")

    results = checks.run_checks(base_dir=tmp_path)
    names = [result.name for result in results]

    assert names == ["python-version", "readme-present", "tmp-writeable"]
    assert results[0].status == "ok"
    assert results[1].status == "ok"
    assert results[2].status == "ok"


def test_format_report_includes_statuses(tmp_path: Path) -> None:
    readme_missing = tmp_path / "README.md"
    if readme_missing.exists():
        readme_missing.unlink()

    results = [
        checks.CheckResult(name="alpha", status="ok", details="all good"),
        checks.CheckResult(name="beta", status="warn", details="something to note"),
        checks.CheckResult(name="gamma", status="error", details="needs attention"),
    ]

    report = checks.format_report(results)
    assert "✅ alpha: all good" in report
    assert "⚠️ beta: something to note" in report
    assert "❌ gamma: needs attention" in report


def test_exit_code_from_results_identifies_errors() -> None:
    ok_results = [
        checks.CheckResult(name="alpha", status="ok", details="fine"),
        checks.CheckResult(name="beta", status="warn", details="warning"),
    ]
    error_results = ok_results + [
        checks.CheckResult(name="gamma", status="error", details="problem"),
    ]

    assert checks.exit_code_from_results(ok_results) == 0
    assert checks.exit_code_from_results(error_results) == 1
