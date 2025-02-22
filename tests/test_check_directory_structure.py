from pathlib import Path

from typer.testing import CliRunner

from pre_commit_hooks.check_directory_structure import app
from tests._helpers import populate_dir

runner = CliRunner()


def test_empty_dir(temp_git_dir: Path) -> None:
    result = runner.invoke(
        app,
        [
            "--source",
            str(temp_git_dir / "src"),
            "--target",
            str(temp_git_dir / "tests"),
            "--format",
            "test_{file.stem}{file.suffix}",
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == ""


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
    result = runner.invoke(
        app,
        [
            "--source",
            str(temp_git_dir / "src"),
            "--target",
            str(temp_git_dir / "tests"),
            "--format",
            "test_{file.stem}{file.suffix}",
        ],
    )

    # Assert
    assert result.exit_code == 1


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
    result = runner.invoke(
        app,
        [
            "--source",
            str(temp_git_dir / "tests"),
            "--target",
            str(temp_git_dir / "src"),
            "--eval",
            'file.stem.removeprefix("test_") + file.suffix',
        ],
    )

    # Assert
    assert result.exit_code == 1


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
    result = runner.invoke(
        app,
        [
            "--source",
            str(temp_git_dir / "src"),
            "--target",
            str(temp_git_dir / "tests"),
            "--format",
            "test_{file.stem}{file.suffix}",
            "--extend-exclude",
            "**/migrations/*.py",
        ],
    )

    # Assert
    assert result.exit_code == 0


def test_format_or_eval_not_provided(temp_git_dir: Path) -> None:
    result = runner.invoke(
        app,
        [
            "--source",
            str(temp_git_dir / "src"),
            "--target",
            str(temp_git_dir / "tests"),
            "--format",
            "",
            "--eval",
            "",
        ],
    )

    assert result.exit_code == 1


def test_mutually_exclusive_arguments() -> None:
    result = runner.invoke(
        app,
        [
            "--format",
            "test_{file.stem}{file.suffix}",
            "--eval",
            'file.stem.removeprefix("test_") + file.suffix',
        ],
    )

    assert result.exit_code == 2


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
    result = runner.invoke(
        app,
        [
            "--source",
            str(temp_git_dir / "src"),
            "--target",
            str(temp_git_dir / "tests"),
            "--format",
            "test_{file.stem}{file.suffix}",
            "--create-if-not-exists",
        ],
    )

    # Assert
    assert result.exit_code == 1
    assert (temp_git_dir / "tests/util/telemetry/test_traces.py").exists()
