from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from pre_commit_hooks.helpers.debugger import input_as_args
from pre_commit_hooks.util.parser import ArgumentParser

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = logging.getLogger(__name__)

# List of glob patterns to exclude from check
_exclude_base = [
    "**/__init__.py",
]


def check_directory_structure(*, source: Path, target: Path, extend_exclude: Iterable[str]) -> int:  # noqa: D103
    exit_code = 0
    py_files = set(source.glob("**/*.py"))
    exclude = _exclude_base + list(extend_exclude)
    for f in exclude:
        py_files -= set(source.glob(f))

    # NOTE: `Path.walk` available since 3.12
    for file in py_files:
        mirror = target.joinpath(file.relative_to(source)).with_name(
            f"test_{file.stem}{file.suffix}",
        )
        if not mirror.exists():
            logger.warning(
                "Expecting %s to exist for %s but not exists",
                mirror,
                file,
            )
            exit_code = 1

    return exit_code


def main() -> int:  # noqa: D103
    parser = ArgumentParser(
        prog="check-directory-structure",
        description="Check current directory structure",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.cwd() / "src",
        help="Source directory",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd() / "tests",
        help="Target directory",
    )
    parser.add_argument(
        "--extend-exclude",
        type=str,
        nargs="*",
        help="Additional glob patterns to exclude from check",
    )

    args = parser.parse_args()
    source: Path = args.source
    target: Path = args.target
    extend_exclude: list[str] = args.extend_exclude

    return check_directory_structure(
        source=source,
        target=target,
        extend_exclude=extend_exclude,
    )


if __name__ == "__main__":
    with input_as_args():
        sys.exit(main())
