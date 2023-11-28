from pathlib import Path

from pre_commit_hooks.check_directory_structure import check_directory_structure


def test_empty_dir(temp_git_dir: Path) -> None:
    assert (
        check_directory_structure(
            source=temp_git_dir / "src",
            target=temp_git_dir / "tests",
        )
        == 0
    )


def test_only_src_dir_populated(temp_git_dir: Path) -> None:
    filenames = [
        "src/__init__.py",
        "src/main.py",
        "src/util/logger.py",
        "src/util/telemetry/traces.py",
    ]
    for filename in filenames:
        file = temp_git_dir / filename
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()

    assert (
        check_directory_structure(
            source=temp_git_dir / "src",
            target=temp_git_dir / "tests",
        )
        == 1
    )


def test_dir_fully_populated(temp_git_dir: Path) -> None:
    filenames = [
        "src/__init__.py",
        "src/main.py",
        "src/util/logger.py",
        "src/util/telemetry/traces.py",
        "tests/test_main.py",
        "tests/util/test_logger.py",
        "tests/util/telemetry/test_traces.py",
    ]
    for filename in filenames:
        file = temp_git_dir / filename
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()

    assert (
        check_directory_structure(
            source=temp_git_dir / "src",
            target=temp_git_dir / "tests",
        )
        == 0
    )
