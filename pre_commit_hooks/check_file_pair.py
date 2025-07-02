# flake8: noqa: B008, UP045
from __future__ import annotations

from enum import Enum
from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING, NoReturn, Optional, Protocol

import typer
from rich import print  # noqa: A004

from pre_commit_hooks.utils.debugger import input_as_args

if TYPE_CHECKING:
    from collections.abc import Iterable


app = typer.Typer()


class ExitCode(Enum):  # noqa: D101
    Ok = 0
    Error = 1


class Transform(Protocol):  # noqa: D101 # pragma: no cover
    def __call__(self, file: Path, *, source: Path, target: Path) -> str: ...  # noqa: D102


def check_file_pair(  # noqa: D103, PLR0913
    *,
    source: Path,
    target: Path,
    transform: Transform,
    exclude: Iterable[str],
    create_if_not_exists: bool,
    dry_run: bool,
) -> ExitCode:
    py_files = set(source.glob("**/*.py"))
    for f in exclude:
        py_files -= set(source.glob(f))

    missing_pairs: list[Path] = []
    for file in py_files:
        pair_name = transform(file, source=source, target=target)
        pair = target.joinpath(file.relative_to(source)).with_name(pair_name)
        if not pair.exists():
            print(f"❗ Expecting [yellow]{pair!s}[/yellow] to exist for [yellow]{file!s}[/yellow] but not exists.")
            missing_pairs.append(pair)

    if missing_pairs:
        print(f"❌ Found {len(missing_pairs)} missing pair(s).")
        if create_if_not_exists:
            for pair in missing_pairs:
                if not dry_run:
                    pair.parent.mkdir(parents=True, exist_ok=True)
                    pair.touch()

                # ? Space after this emoji is too narrow, so gave 2 spaces; is it happening in my terminal only?
                print(f"⚠️ Created [yellow]{pair!s}[/yellow].")

        return ExitCode.Error

    return ExitCode.Ok


# ? Annotated version not working as documented (currently using Python 3.9)
@app.command()
def main(  # noqa: PLR0913
    *,
    source: Path = typer.Option(
        ...,
        show_default=False,
        help="Source directory.",
    ),
    target: Path = typer.Option(
        ...,
        show_default=False,
        help="Target directory.",
    ),
    format_: Optional[str] = typer.Option(
        None,
        "--format",
        help="Format string for target file. Cannot be used with `--eval`.",
    ),
    eval_: Optional[str] = typer.Option(
        None,
        "--eval",
        help="Format string for target file using `eval()`. Cannot be used with `--format`.",
    ),
    exclude: list[str] = typer.Option(
        ["**/__*.py"],
        help="Glob patterns to exclude from check.",
    ),
    extend_exclude: list[str] = typer.Option(
        ["**/_*.py", "**/conftest.py"],
        help="Additional glob patterns to exclude from check.",
    ),
    create_if_not_exists: bool = typer.Option(
        False,  # noqa: FBT003
        help="Create expected file if not exists.",
    ),
    dry_run: bool = typer.Option(
        False,  # noqa: FBT003
        help="Skip some operations to prevent changes.",
    ),
) -> NoReturn:
    """Check file in source directory have its pair in target directory."""
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

    exit_code = check_file_pair(
        source=source,
        target=target,
        transform=transform,
        exclude=exclude + extend_exclude,
        create_if_not_exists=create_if_not_exists,
        dry_run=dry_run,
    )

    raise typer.Exit(exit_code.value)


def entrypoint() -> None:  # noqa: D103  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    with input_as_args():
        entrypoint()
