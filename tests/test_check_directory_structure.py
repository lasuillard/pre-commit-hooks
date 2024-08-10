import sys
from pathlib import Path
from unittest.mock import patch

from pre_commit_hooks.check_directory_structure import main
from tests._helpers import populate_dir


def test_empty_dir(temp_git_dir: Path) -> None:
    with patch.object(
        sys,
        "argv",
        [
            "check-directory-structure",
            "--source",
            str(temp_git_dir / "src"),
            "--target",
            str(temp_git_dir / "tests"),
        ],
    ):
        exit_code = main()

    assert exit_code == 0


def test_only_src_dir_populated(temp_git_dir: Path) -> None:
    # Arrange
    populate_dir(
        temp_git_dir,
        file_or_dirs=[
            "src/__init__.py",
            "src/main.py",
            "src/util/logger.py",
            "src/util/telemetry/traces.py",
        ],
    )

    # Act
    with patch.object(
        sys,
        "argv",
        [
            "check-directory-structure",
            "--source",
            str(temp_git_dir / "src"),
            "--target",
            str(temp_git_dir / "tests"),
        ],
    ):
        exit_code = main()

    # Assert
    assert exit_code == 1


def test_dir_fully_populated(temp_git_dir: Path) -> None:
    # Arrange
    populate_dir(
        temp_git_dir,
        file_or_dirs=[
            "src/__init__.py",
            "src/main.py",
            "src/util/logger.py",
            "src/util/telemetry/traces.py",
            "src/migrations/0001_initial.py",
            "src/migrations/__init__.py",
            "tests/test_main.py",
            "tests/util/test_logger.py",
            "tests/util/telemetry/test_traces.py",
        ],
    )

    # Act
    with patch.object(
        sys,
        "argv",
        [
            "check-directory-structure",
            "--source",
            str(temp_git_dir / "src"),
            "--target",
            str(temp_git_dir / "tests"),
            "--extend-exclude",
            "**/migrations/*.py",
        ],
    ):
        exit_code = main()

    # Assert
    assert exit_code == 0
