# pre-commit-hooks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/lasuillard/pre-commit-hooks/graph/badge.svg?token=I646XXfAud)](https://codecov.io/gh/lasuillard/pre-commit-hooks)
![GitHub Release](https://img.shields.io/github/v/release/lasuillard/pre-commit-hooks)

Personal pre-commit hooks for common developer tasks.

## 🪝 Available hooks

See the [.pre-commit-hooks.yaml](./.pre-commit-hooks.yaml) file for available hooks.

An example `.pre-commit-config.yaml` would look like:

```yaml
repos:
  ...

  - repo: https://github.com/lasuillard/pre-commit-hooks
    rev: v0.4.3
    hooks:
      - id: alloy-format

  ...
```

### `preferred-suffix`

Checks whether a file uses the preferred suffix when multiple suffix variants are available.

```bash
$ TYPER_USE_RICH=0 uv run preferred-suffix --help
Usage: preferred-suffix [OPTIONS] FILES...

  Check filenames to use a single preferred suffix over other possible variants.

Arguments:
  FILES...  Files to check.  [required]

Options:
  --mapping TEXT            List of suffix mappings, each in the format of
                            `suffix1,suffix2,... -> preferred-suffix`.
                            [default: yml -> yaml]
  --extend-mapping TEXT     List of suffix mappings to extend the default
                            mapping.
  --rename / --no-rename    Whether to rename files with the preferred suffix
                            automatically.  [default: no-rename]
  --dry-run / --no-dry-run  Skip some operations to prevent changes.
                            [default: no-dry-run]
  --install-completion      Install completion for the current shell.
  --show-completion         Show completion for the current shell, to copy it
                            or customize the installation.
  --help                    Show this message and exit.
```

### `alloy-format`

> [!NOTE]
> This hook is a convenience shortcut for invoking the [Alloy](https://github.com/grafana/alloy) CLI. It does **NOT** install `alloy`.

Reformats `.alloy` files using `alloy fmt`. See `alloy fmt --help` for available options.

## 🧑‍💻 Development

See the [CONTRIBUTING.md](./CONTRIBUTING.md) file for development instructions.
