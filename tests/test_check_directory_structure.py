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
            "--format",
            "test_{file.stem}{file.suffix}",
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
            "--format",
            "test_{file.stem}{file.suffix}",
        ],
    ):
        exit_code = main()

    # Assert
    assert exit_code == 1


def test_only_tests_dir_populated(temp_git_dir: Path) -> None:
    # Arrange
    populate_dir(
        temp_git_dir,
        file_or_dirs=[
            "src/__init__.py",
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
            str(temp_git_dir / "tests"),
            "--target",
            str(temp_git_dir / "src"),
            "--eval",
            'file.stem.removeprefix("test_") + file.suffix',
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
            "--format",
            "test_{file.stem}{file.suffix}",
            "--extend-exclude",
            "**/migrations/*.py",
        ],
    ):
        exit_code = main()

    # Assert
    assert exit_code == 0


def test_format_or_eval_not_provided(temp_git_dir: Path) -> None:
    with patch.object(
        sys,
        "argv",
        [
            "check-directory-structure",
            "--source",
            str(temp_git_dir / "src"),
            "--target",
            str(temp_git_dir / "tests"),
            "--format",
            "",
            "--eval",
            "",
        ],
    ):
        exit_code = main()

    assert exit_code == 1


def test_mutually_exclusive_arguments() -> None:
    with patch.object(
        sys,
        "argv",
        [
            "check-directory-structure",
            "--format",
            "test_{file.stem}{file.suffix}",
            "--eval",
            'file.stem.removeprefix("test_") + file.suffix',
        ],
    ):
        exit_code = main()

    assert exit_code == 1


def test_create_if_not_exists(temp_git_dir: Path) -> None:
    # Arrange
    populate_dir(
        temp_git_dir,
        file_or_dirs=[
            "src/__init__.py",
            "src/main.py",
            "src/util/logger.py",
            "src/util/telemetry/traces.py",
            "tests/test_main.py",
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
            "--format",
            "test_{file.stem}{file.suffix}",
            "--create-if-not-exists",
        ],
    ):
        exit_code = main()

    # Assert
    assert exit_code == 1
    assert (temp_git_dir / "tests/util/telemetry/test_traces.py").exists()
