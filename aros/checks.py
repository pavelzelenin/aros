from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    details: str

    def __post_init__(self) -> None:
        if self.status not in {"ok", "warn", "error"}:
            raise ValueError(f"Unsupported status '{self.status}' for check '{self.name}'")


def python_version_check() -> CheckResult:
    version = sys.version_info
    minimum = (3, 10)
    if version < minimum:
        return CheckResult(
            name="python-version",
            status="error",
            details=f"Python {version.major}.{version.minor} is below required {minimum[0]}.{minimum[1]}",
        )
    return CheckResult(
        name="python-version",
        status="ok",
        details=f"Python {version.major}.{version.minor} detected",
    )


def readme_check(base_dir: os.PathLike[str] | str = ".") -> CheckResult:
    readme_path = Path(base_dir) / "README.md"
    if not readme_path.exists():
        return CheckResult(
            name="readme-present",
            status="warn",
            details="README.md is missing; add one to describe the project",
        )
    return CheckResult(
        name="readme-present",
        status="ok",
        details="README.md detected",
    )


def tmp_write_check() -> CheckResult:
    tmp_dir = Path("/tmp")
    if not tmp_dir.exists():
        return CheckResult(
            name="tmp-writeable",
            status="warn",
            details="/tmp is missing; cannot verify temporary file writes",
        )

    probe_path = tmp_dir / "aros_tmp_probe.txt"
    try:
        probe_path.write_text("ok", encoding="utf-8")
        probe_path.unlink()
    except OSError as exc:  # pragma: no cover - defensive
        return CheckResult(
            name="tmp-writeable",
            status="error",
            details=f"Failed to write to /tmp: {exc}",
        )

    return CheckResult(name="tmp-writeable", status="ok", details="Temporary directory is writeable")


def run_checks(base_dir: os.PathLike[str] | str = ".") -> List[CheckResult]:
    checks: Iterable[CheckResult] = (
        python_version_check(),
        readme_check(base_dir=base_dir),
        tmp_write_check(),
    )
    return list(checks)


def format_report(results: Iterable[CheckResult]) -> str:
    lines = []
    status_emojis = {"ok": "✅", "warn": "⚠️", "error": "❌"}

    for result in results:
        emoji = status_emojis.get(result.status, "❓")
        lines.append(f"{emoji} {result.name}: {result.details}")

    return "\n".join(lines)


def exit_code_from_results(results: Iterable[CheckResult]) -> int:
    has_error = any(result.status == "error" for result in results)
    return 1 if has_error else 0
