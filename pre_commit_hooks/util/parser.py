import argparse
import logging
from pathlib import Path
from typing import Any

import colorlog


class ArgumentParser(argparse.ArgumentParser):  # noqa: D101
    def __init__(self, *args: Any, **kwargs: Any):  # noqa: D107
        super().__init__(*args, **kwargs)

        self.add_argument(
            "-v",
            "--verbose",
            help="Enable verbose output",
            action="store_true",
        )

    def add_argument(self, *args: Any, **kwargs: Any) -> argparse.Action:  # noqa: D102
        # Auto add default to help
        if "default" in kwargs and "help" in kwargs and "--help" not in args:
            help_ = kwargs["help"]
            default = kwargs["default"]

            # Format some types in compact format
            if isinstance(default, Path):
                default = default.relative_to(Path.cwd())

            kwargs["help"] = f"{help_!s} (defaults to {default!s})"

        return super().add_argument(*args, **kwargs)

    def parse_args(self, *args: Any, **kwargs: Any) -> Any:  # noqa: D102
        parsed_args = super().parse_args(*args, **kwargs)

        # Configure logger
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(asctime)s %(log_color)s%(levelname)-8s %(reset)s%(module)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            ),
        )
        log_level = logging.DEBUG if parsed_args.verbose else logging.INFO
        logging.basicConfig(level=log_level, handlers=[handler])

        return parsed_args
