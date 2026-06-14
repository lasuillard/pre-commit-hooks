# 👥 Development guide

This project is personal work. Although it's shared public open source, it is not open for contributions. Here, I describe how to develop and test pre-commit hooks locally.

## 🛠️ Tech stack

This project uses the following tech stack:

- [Python](https://www.python.org) 3.10
- [uv](https://docs.astral.sh/uv/) for dependency management and packaging
- [Ruff](https://docs.astral.sh/ruff/) to lint and format Python code, and [mypy](https://mypy-lang.org/) to type check
- [pytest](https://docs.pytest.org/en/latest) for testing

## 📂 Key directory structure

- `.devcontainer.example/`: Development environment configuration
- `.vscode.example/`: Project-specific VS Code configuration example
- `packages/`: Shared packages
- `pre_commit_hooks/`: This project source code
- `flake.lock`, `flake.nix`: Flake configuration for development environment
- `Justfile`: Commands for development
- `pyproject.toml`: Project dependencies and configuration

## 🔧 Set up development environment

For development, you need to have the following tools installed:

### ❄️ Tools managed via Nix Flakes

This repository uses [Nix Flakes](https://nix.dev/concepts/flakes.html) to manage tools. Following tools will be automatically installed (you need `nix` installed, of course):

- `git`
- `pre-commit`
- `uv`
- [Just](https://just.systems/) (`just`)
- Tools that pre-commit hook requires (irrelevant for development): `alloy`

If you prefer [Dev Container](https://containers.dev/), we have configuration ([devcontainer.json](./.devcontainer.example/devcontainer.json)) for it, with Nix installed! All you need to do is to run `nix develop` to start the development environment then run `just install` to install dependencies.

## ⌨️ Developing pre-commit hooks

This project delivers pre-commit hooks as small, self-contained CLI programs. If you look at the `pyproject.toml` file, you will see the following:

```toml
[project.scripts]
preferred-suffix = "pre_commit_hooks.preferred_suffix:entrypoint"
```

You can check the source code at [`pre_commit_hooks/preferred_suffix.py`](./pre_commit_hooks/preferred_suffix.py) as an example.

Once you have implemented a hook, you should add a new hook entry in the `pre-commit-hooks.yaml` file as well. Then, you can try the hook as if you are installing it as a pre-commit hook, by running `pre-commit try-repo` command.

Let's take `alloy-format` hook as an example:

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

Before you push your code, you need to verify your code changes if it follows with the project's coding standard. You can run `just ci` to run all the necessary linters, formatters, and tests. Or, you can leave the `pre-commit` hooks do the job for you.

## 🚀 Publishing pre-commit hooks

> [!NOTE]
> This project is not published to PyPI because pre-commit support Git repositories.

This project is published as a package on GitHub Releases. If you push a tag, it will be automatically create a new release automatically.
