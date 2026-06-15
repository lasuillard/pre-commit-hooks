# 👥 Development guide

This is a personal project. Although it is public and open-source, contributions are not accepted. This document describes how to develop and test pre-commit hooks locally.

## 🛠️ Tech stack

This project uses the following tech stack:

- [Python](https://www.python.org) 3.10
- [uv](https://docs.astral.sh/uv/) for dependency management and packaging
- [Ruff](https://docs.astral.sh/ruff/) to lint and format Python code, and [mypy](https://mypy-lang.org/) for type checking
- [pytest](https://docs.pytest.org/en/latest) for testing

## 📂 Key directory structure

- `.devcontainer.example/`: Development environment configuration
- `.vscode.example/`: Project-specific VS Code configuration example
- `pre_commit_hooks/`: The project's source code
- `tests/`: Project tests
- `flake.nix`: Flake configuration for the development environment
- `Justfile`: Commands for development
- `pyproject.toml`: Project dependencies and configuration

## 🔧 Set up the development environment

To work on this project, you must have the following tools installed:

### ❄️ Tools managed via Nix Flakes

This repository uses [Nix Flakes](https://nix.dev/concepts/flakes.html) to manage tools. The following tools will be automatically installed (requires `nix` to be installed):

- `git`
- `pre-commit`
- `just`
- `uv`
- Tools required by the pre-commit hook (not needed for development): `alloy`

Simply run `nix develop` to start the development environment, then run `just install` to install dependencies.

If you prefer using a [Dev Container](https://containers.dev), a configuration file ([devcontainer.json](./.devcontainer.example/devcontainer.json)) is provided with Nix pre-installed.

## ⌨️ Developing pre-commit hooks

This project provides pre-commit hooks as small, self-contained CLI programs. The `pyproject.toml` file contains the following configuration:

```toml
[project.scripts]
preferred-suffix = "pre_commit_hooks.preferred_suffix:entrypoint"
```

You can examine the source code at [`pre_commit_hooks/preferred_suffix.py`](./pre_commit_hooks/preferred_suffix.py) as an example.

When you add a hook, include a new entry in `.pre-commit-hooks.yaml`. Then test the hook locally using `pre-commit try-repo`.

Let's use the `alloy-format` hook as an example:

```bash
$ pre-commit try-repo . alloy-format
[WARNING] Creating temporary repo with uncommitted changes...
===============================================================================
Using config:
===============================================================================
repos:
-   repo: /tmp/tmpukfbfrjl/shadow-repo
    rev: 5c072fdaa9e679ecd2558558ef4eebc01e6176ca
    hooks:
    -   id: alloy-format
===============================================================================
[WARNING] Unstaged files detected.
[INFO] Stashing unstaged files to /tmp/tmpukfbfrjl/patch1781346949-237959.
[INFO] Initializing environment for /tmp/tmpukfbfrjl/shadow-repo.
alloy-format.........................................(no files to check)Skipped
[INFO] Restored changes from /tmp/tmpukfbfrjl/patch1781346949-237959.
```

## ✅ Verifying changes

Before pushing changes, verify they adhere to the project's coding standards. Run `just ci` to execute all necessary linters, formatters, and tests. Alternatively, you can let the `pre-commit` hooks handle this automatically.

## 🚀 Publishing pre-commit hooks

> [!NOTE]
> This project is not published to PyPI because pre-commit natively supports Git repositories.

This project is published via GitHub Releases. Pushing a new Git tag automatically creates a corresponding release.
