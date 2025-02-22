from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Mapping, Sequence, cast

from pre_commit_hooks.helpers.debugger import input_as_args
from pre_commit_hooks.util.parser_ import ArgumentParser

logger = logging.getLogger(__name__)

# TODO(lasuillard): Find possible references of filenames from other files

suffixes_to_preferred: Mapping[Sequence[str], str] = {
    (".yml",): ".yaml",
}


def preferred_suffix(*files: Path, rename: bool) -> int:  # noqa: D103
    exit_code = 0
    for file in files:
        logger.debug("Checking %r", file)
        for suffixes, preferred in suffixes_to_preferred.items():
            for suffix in suffixes:
                if file.name.endswith(suffix):
                    exit_code = 1
                    if rename:
                        logger.warning(
                            "File %r has suffix %r where preferred suffix is %r.",
                            file,
                            suffix,
                            preferred,
                        )
                        file_renamed = file.with_name(file.name[: file.name.rfind(suffix)] + preferred)
                        file.rename(file_renamed)
                        logger.warning("Renamed file %r to %r because `rename` option is set.", file, file_renamed)
                    else:
                        logger.warning(
                            "File %r has suffix %r while preferred suffix is %r."
                            " To rename suffixes automatically, provide `rename` option.",
                            file,
                            suffix,
                            preferred,
                        )

                    # If anything caught, escape abnormally to trigger upper loop escape (`for else` syntax)
                    break
            else:
                continue
            break

    return exit_code


def main() -> int:  # noqa: D103
    parser = ArgumentParser(
        prog="preferred-suffix",
        description="Check filenames to use single preferred suffix over other possible variants.",
    )
    parser.add_argument(
        "--rename",
        action="store_true",
        help="Whether to rename files with preferred suffix automatically.",
    )
    parser.add_argument("files", type=Path, nargs="+", help="Path of files.")

    # Type annotate args
    args = parser.parse_args()
    files: list[Path] = [f.absolute() for f in cast(Sequence[Path], args.files)]
    rename: bool = args.rename

    return preferred_suffix(*files, rename=rename)


if __name__ == "__main__":  # pragma: no cover
    with input_as_args():
        sys.exit(main())
