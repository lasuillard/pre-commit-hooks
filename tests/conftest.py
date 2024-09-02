from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from _pytest._py.path import LocalPath


# https://github.com/pre-commit/pre-commit-hooks/blob/main/tests/conftest.py
@pytest.fixture
def temp_git_dir(tmpdir: LocalPath) -> Path:
    git_dir = Path(tmpdir) / "git"
    subprocess.Popen(["git", "init", "--", str(git_dir)])  # noqa: S603, S607
    return git_dir
