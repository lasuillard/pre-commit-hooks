# flake8: noqa: B008
from __future__ import annotations

from enum import Enum
from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING, NoReturn

import typer
from rich import print  # noqa: A004

from pre_commit_hooks.helpers.debugger import input_as_args

if TYPE_CHECKING:
    from collections.abc import Mapping

app = typer.Typer()


class ExitCode(Enum):  # noqa: D101
    Ok = 0
    Error = 1


suffixes_to_preferred: Mapping[str, str] = {
    ".yml": ".yaml",
}


def preferred_suffix(*files: Path, rename: bool, dry_run: bool) -> ExitCode:  # noqa: D103
    violations: list[Path] = []
    for file in files:
        preferred = suffixes_to_preferred.get(file.suffix)
        if preferred is None:
            continue

        print(f"❗ File [yellow]{file!s}[/yellow] has suffix {file.suffix!r} where preferred suffix is {preferred!r}.")
        violations.append(file)

    if violations:
        print(f"❌ Found {len(violations)} file(s) with non-preferred suffix.")
        if rename:
            for file in violations:
                preferred = suffixes_to_preferred[file.suffix]
                file_renamed = file.with_suffix(preferred)
                if not dry_run:
                    file.rename(file_renamed)

                print(f"⚠️  Renamed file [yellow]{file!s}[/yellow] to [yellow]{file_renamed!s}[/yellow].")

        return ExitCode.Error

    return ExitCode.Ok


@app.command()
def main(
    files: list[Path] = typer.Argument(
        ...,
        show_default=False,
        help="Files to check.",
    ),
    *,
    rename: bool = typer.Option(
        False,  # noqa: FBT003
        help="Whether to rename files with preferred suffix automatically.",
    ),
    dry_run: bool = typer.Option(
        False,  # noqa: FBT003
        help="Skip some operations to prevent changes.",
    ),
) -> NoReturn:
    """Check filenames to use single preferred suffix over other possible variants."""
    exit_code = preferred_suffix(
        *files,
        rename=rename,
        dry_run=dry_run,
    )

    raise typer.Exit(exit_code.value)


def entrypoint() -> None:  # noqa: D103
    app()


if __name__ == "__main__":  # pragma: no cover
    with input_as_args():
        entrypoint()
