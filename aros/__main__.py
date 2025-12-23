from __future__ import annotations

import argparse
from pathlib import Path

from .checks import exit_code_from_results, format_report, run_checks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run environment checks for Agent Runtime OS")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root to scan for documentation and other assets",
    )
    return parser


def main(args: list[str] | None = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args=args)

    results = run_checks(base_dir=parsed.project_root)
    print(format_report(results))
    return exit_code_from_results(results)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
