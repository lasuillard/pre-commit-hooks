from pathlib import Path

from typer.testing import CliRunner

from pre_commit_hooks.check_file_pair import app
from tests._helpers import populate_dir

runner = CliRunner()

# TODO(lasuillard): Enrich assertions (command outputs)


def test_empty_dir(temp_git_dir: Path) -> None:
    """It should exit silently on empty directory."""
    # Arrange
    # ...

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
    assert result.exit_code == 0
    assert result.stdout == ""


def test_forward_match(temp_git_dir: Path) -> None:
    """Test forward matching using `--format` option."""
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


def test_reverse_match(temp_git_dir: Path) -> None:
    """Test reverse matching using `--eval` option."""
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
    """If both source and target directories are fully populated with all matching pairs, it should exit OK."""
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


def test_format_or_eval_must_provided(temp_git_dir: Path) -> None:
    # Arrange
    # ...

    # Act
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

    # Assert
    assert result.exit_code == 1


def test_format_and_eval_mutually_exclusive(temp_git_dir: Path) -> None:
    # Arrange
    # ...

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
            "--eval",
            'file.stem.removeprefix("test_") + file.suffix',
        ],
    )

    # Assert
    assert result.exit_code == 1


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


def test_create_if_not_exists_dry_run(temp_git_dir: Path) -> None:
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
            "--dry-run",
        ],
    )

    # Assert
    assert result.exit_code == 1
    assert not (temp_git_dir / "tests/util/telemetry/test_traces.py").exists()
