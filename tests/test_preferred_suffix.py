from pathlib import Path

import pytest

from pre_commit_hooks.preferred_suffix import preferred_suffix
from tests._helpers import populate_dir


def test_no_paths() -> None:
    exit_code = preferred_suffix(rename=False)
    assert exit_code == 0


@pytest.mark.parametrize(
    "kwargs",
    [{"rename": True}, {"rename": False}],
)
def test_all_using_preferred_suffixes(temp_git_dir: Path, kwargs: dict) -> None:
    paths = populate_dir(
        temp_git_dir,
        file_or_dirs=[
            ".github/workflows/ci.yaml",
            ".github/dependabot.yaml",
            "docker-compose.yaml",
            "docker-compose.override.yaml",
        ],
    )
    exit_code = preferred_suffix(*paths, **kwargs)
    assert exit_code == 0
    for path in paths:
        assert path.exists()


def test_prefer_yaml_over_yml(temp_git_dir: Path) -> None:
    paths = populate_dir(
        temp_git_dir,
        file_or_dirs=[
            ".github/workflows/ci.yml",
            ".github/dependabot.yml",
            "docker-compose.yml",
            "docker-compose.override.yml",
        ],
    )
    exit_code = preferred_suffix(*paths, rename=True)
    assert exit_code == 1
    for path in paths:
        assert not path.exists()
        assert path.with_suffix(".yaml").exists()
