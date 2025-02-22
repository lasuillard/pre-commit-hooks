from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

from pre_commit_hooks.helpers.debugger import input_as_args
from pre_commit_hooks.util.parser_ import ArgumentParser

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = logging.getLogger(__name__)

# List of glob patterns to exclude from check
_exclude_base = [
    "**/__init__.py",
]


class Transform(Protocol):  # noqa: D101
    def __call__(self, file: Path, *, source: Path, target: Path) -> str: ...  # noqa: D102


def check_directory_structure(  # noqa: D103
    *,
    source: Path,
    target: Path,
    transform: Transform,
    extend_exclude: Iterable[str],
    create_if_not_exists: bool,
) -> int:
    exit_code = 0
    py_files = set(source.glob("**/*.py"))
    exclude = _exclude_base + list(extend_exclude)
    for f in exclude:
        py_files -= set(source.glob(f))

    # NOTE: `Path.walk` available since 3.12
    for file in py_files:
        mirror = target.joinpath(file.relative_to(source)).with_name(
            transform(file, source=source, target=target),
        )
        if not mirror.exists():
            logger.warning(
                "Expecting %s to exist for %s but not exists",
                mirror,
                file,
            )
            if create_if_not_exists:
                mirror.parent.mkdir(parents=True, exist_ok=True)
                mirror.touch()
                logger.info("Created %s", mirror)

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
        "--format",
        type=str,
        default=None,  # e.g. "test_{file.stem}{file.suffix}",
        help="Format string for target file. Cannot be used with `--eval`.",
    )
    parser.add_argument(
        "--eval",
        type=str,
        default=None,  # e.g. "file.stem.removeprefix('test_')",
        help="Format string for target file using `eval()`. Cannot be used with `--format`.",
    )
    parser.add_argument(
        "--extend-exclude",
        type=str,
        nargs="*",
        default=[],
        help="Additional glob patterns to exclude from check",
    )
    parser.add_argument(
        "--create-if-not-exists",
        action="store_true",
        default=False,
        help="Create expected file if not exists",
    )

    args = parser.parse_args()
    source: Path = args.source
    target: Path = args.target
    format_: str = args.format
    eval_: str = args.eval
    extend_exclude: list[str] = args.extend_exclude
    create_if_not_exists: bool = args.create_if_not_exists

    if format_ and eval_:
        msg = "Cannot use `--format` and `--eval` together"
        raise ValueError(msg)

    if format_:

        def transform(file: Path, *, source: Path, target: Path) -> str:
            return format_.format(file=file, source=source, target=target)

    elif eval_:

        def transform(file: Path, *, source: Path, target: Path) -> str:
            namespace = {
                "file": file,
                "source": source,
                "target": target,
            }
            result = eval(eval_, {"__builtins__": None}, namespace)  # noqa: S307
            return str(result)

    else:
        msg = "Either `--format` or `--eval` must be provided"
        raise ValueError(msg)

    return check_directory_structure(
        source=source,
        target=target,
        transform=transform,
        extend_exclude=extend_exclude,
        create_if_not_exists=create_if_not_exists,
    )


if __name__ == "__main__":  # pragma: no cover
    with input_as_args():
        sys.exit(main())
