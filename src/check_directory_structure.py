import logging
import sys
from pathlib import Path

from src.util.parser import ArgumentParser

logger = logging.getLogger(__name__)

# TODO(lasuillard): Regex support
# TODO(lasuillard): Customizable options to support languages other than Python

# List of glob patterns to exclude from check
filters = [
    "__init__.py",
]


def check_directory_structure(*, source: Path, target: Path) -> int:  # noqa: D103
    exit_code = 0
    py_files = set(source.glob("**/*.py"))
    for f in filters:
        py_files -= set(source.glob(f))

    # NOTE: `Path.walk` available since 3.12
    for file in py_files:
        mirror = target.joinpath(file.relative_to(source)).with_stem(f"test_{file.stem}")
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

    args = parser.parse_args()

    return check_directory_structure(
        source=args.source,
        target=args.target,
    )


if __name__ == "__main__":
    sys.exit(main())
