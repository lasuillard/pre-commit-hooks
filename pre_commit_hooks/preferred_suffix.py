# flake8: noqa: B008
from __future__ import annotations

from enum import Enum
from pathlib import Path  # noqa: TC003
from typing import NoReturn

import typer
from rich import print  # noqa: A004
from rich.table import Table

from pre_commit_hooks.utils.debugger import input_as_args

app = typer.Typer()


class ExitCode(Enum):  # noqa: D101
    Ok = 0
    Error = 1


def preferred_suffix(*files: Path, mapping: dict[str, str], rename: bool, dry_run: bool) -> ExitCode:  # noqa: D103
    violations: list[Path] = []
    for file in files:
        preferred = mapping.get(file.suffix)
        if preferred is None:
            continue

        print(f"❗ File [yellow]{file!s}[/yellow] has suffix {file.suffix!r} where preferred suffix is {preferred!r}.")
        violations.append(file)

    if violations:
        print(f"❌ Found {len(violations)} file(s) with non-preferred suffix.")
        if rename:
            for file in violations:
                preferred = mapping[file.suffix]
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
    mapping: list[str] = typer.Option(
        ["yml -> yaml"],
        help="List of suffix mapping, each in format of `suffix1,suffix2,... -> preferred-suffix`.",
    ),
    extend_mapping: list[str] = typer.Option(
        [],
        help="List of suffix mapping to extend the default mapping.",
    ),
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
    mapping_dict = _parse_mapping(mapping + extend_mapping)
    print("📝 Mapping of suffixes to preferred suffix:")
    _print_mapping(mapping_dict)

    exit_code = preferred_suffix(
        *files,
        mapping=mapping_dict,
        rename=rename,
        dry_run=dry_run,
    )

    raise typer.Exit(exit_code.value)


def _parse_mapping(mapping: list[str]) -> dict[str, str]:
    """Parse list of mapping string (`"suffix1,suffix2,... -> suffix"`) to dictionary of suffix to preferred suffix."""
    result = {}
    for item in mapping:
        suffix_csv, preferred = item.split("->")
        suffix_list = [f".{suffix.strip()}" for suffix in suffix_csv.split(",")]
        preferred = f".{preferred.strip()}"
        for suffix in suffix_list:
            result[suffix] = preferred

    return result


def _print_mapping(mapping: dict[str, str]) -> None:
    # Group suffixes to preferred suffix
    match: dict[str, list[str]] = {}
    for suffix, preferred in mapping.items():
        match.setdefault(preferred, []).append(suffix)

    # Print table in pretty format
    table = Table("Preferred", "Suffixes")
    for preferred, suffixes in match.items():
        table.add_row(preferred, ", ".join(suffixes))

    print(table)


def entrypoint() -> None:  # noqa: D103  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    with input_as_args():
        entrypoint()
