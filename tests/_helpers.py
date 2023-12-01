from collections.abc import Iterable
from pathlib import Path


def populate_dir(base_dir: Path, *, file_or_dirs: Iterable[str]) -> list[Path]:
    """Test helper for populating temporary directory with files.

    Args:
        base_dir: Base directory to populate.
        file_or_dirs: Iterable of file or directory path relative to base directory.
            If ends with slash(/), will be directory.

    Returns:
        List of path for created items.
    """
    results = []
    for relative_path in file_or_dirs:
        path = base_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative_path.endswith("/"):
            path.mkdir()
        else:
            path.touch()

        results.append(path)

    return results
