from pathlib import Path

from pre_commit_hooks.check_directory_structure import check_directory_structure
from tests._helpers import populate_dir


def test_empty_dir(temp_git_dir: Path) -> None:
    exit_code = check_directory_structure(
        source=temp_git_dir / "src",
        target=temp_git_dir / "tests",
    )
    assert exit_code == 0


def test_only_src_dir_populated(temp_git_dir: Path) -> None:
    populate_dir(
        temp_git_dir,
        file_or_dirs=[
            "src/__init__.py",
            "src/main.py",
            "src/util/logger.py",
            "src/util/telemetry/traces.py",
        ],
    )
    exit_code = check_directory_structure(
        source=temp_git_dir / "src",
        target=temp_git_dir / "tests",
    )
    assert exit_code == 1


def test_dir_fully_populated(temp_git_dir: Path) -> None:
    populate_dir(
        temp_git_dir,
        file_or_dirs=[
            "src/__init__.py",
            "src/main.py",
            "src/util/logger.py",
            "src/util/telemetry/traces.py",
            "tests/test_main.py",
            "tests/util/test_logger.py",
            "tests/util/telemetry/test_traces.py",
        ],
    )
    exit_code = check_directory_structure(
        source=temp_git_dir / "src",
        target=temp_git_dir / "tests",
    )
    assert exit_code == 0
