from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from pre_commit_hooks.preferred_suffix import app
from tests._helpers import populate_dir

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_all_using_preferred_suffixes(temp_git_dir: Path) -> None:
    """If all files already have preferred suffixes, it should exit silently."""
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
    result = runner.invoke(app, [*map(str, paths)])

    # Assert
    assert result.exit_code == 0
    for path in paths:
        assert path.exists()


def test_prefer_yaml_over_yml(temp_git_dir: Path) -> None:
    """Test preferring `yaml` over `yml`."""
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
    result = runner.invoke(app, [*map(str, paths)])

    # Assert
    assert result.exit_code == 1
    for path in paths:
        assert path.exists()
        assert not path.with_suffix(".yaml").exists()


def test_prefer_yaml_over_yml_rename(temp_git_dir: Path) -> None:
    """Test preferring `yaml` over `yml` with auto-renaming."""
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
    result = runner.invoke(app, ["--rename", *map(str, paths)])

    # Assert
    assert result.exit_code == 1
    for path in paths:
        assert not path.exists()
        assert path.with_suffix(".yaml").exists()


def test_prefer_yaml_over_yml_rename_dry_run(temp_git_dir: Path) -> None:
    """Test preferring `yaml` over `yml` with auto-renaming in dry-run mode."""
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
    result = runner.invoke(app, ["--rename", "--dry-run", *map(str, paths)])

    # Assert
    assert result.exit_code == 1
    for path in paths:
        assert path.exists()
        assert not path.with_suffix(".yaml").exists()
