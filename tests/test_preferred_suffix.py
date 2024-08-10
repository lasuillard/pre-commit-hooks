from __future__ import annotations

import sys
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from pre_commit_hooks.preferred_suffix import main
from tests._helpers import populate_dir

if TYPE_CHECKING:
    from pathlib import Path


def test_no_paths() -> None:
    with pytest.raises(SystemExit, match="2"), patch.object(sys, "argv", ["preferred-suffix"]):
        main()


@pytest.mark.parametrize(
    "args",
    [(), ("--rename")],
)
def test_all_using_preferred_suffixes(temp_git_dir: Path, args: tuple[str]) -> None:
    # Arrange
    paths = populate_dir(
        temp_git_dir,
        file_or_dirs=[
            ".github/workflows/ci.yaml",
            ".github/dependabot.yaml",
            "docker-compose.yaml",
            "docker-compose.override.yaml",
        ],
    )

    # Act
    with patch.object(sys, "argv", ["preferred-suffix", *map(str, paths), *args]):
        exit_code = main()

    # Assert
    assert exit_code == 0
    for path in paths:
        assert path.exists()


def test_prefer_yaml_over_yml(temp_git_dir: Path) -> None:
    # Arrange
    paths = populate_dir(
        temp_git_dir,
        file_or_dirs=[
            ".github/workflows/ci.yml",
            ".github/dependabot.yml",
            "docker-compose.yml",
            "docker-compose.override.yml",
        ],
    )

    # Act
    with patch.object(sys, "argv", ["preferred-suffix", "--rename", *map(str, paths)]):
        exit_code = main()

    # Assert
    assert exit_code == 1
    for path in paths:
        assert not path.exists()
        assert path.with_suffix(".yaml").exists()


def test_prefer_yaml_over_yml_leave_it(temp_git_dir: Path) -> None:
    # Arrange
    paths = populate_dir(
        temp_git_dir,
        file_or_dirs=[
            ".github/workflows/ci.yml",
            ".github/dependabot.yml",
            "docker-compose.yml",
            "docker-compose.override.yml",
        ],
    )

    # Act
    with patch.object(sys, "argv", ["preferred-suffix", *map(str, paths)]):
        exit_code = main()

    # Assert
    assert exit_code == 1
    for path in paths:
        assert path.exists()
        assert not path.with_suffix(".yaml").exists()
