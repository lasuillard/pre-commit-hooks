# pre-commit-hooks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/lasuillard/pre-commit-hooks/actions/workflows/ci.yaml/badge.svg)](https://github.com/lasuillard/pre-commit-hooks/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/lasuillard/pre-commit-hooks/graph/badge.svg?token=I646XXfAud)](https://codecov.io/gh/lasuillard/pre-commit-hooks)
![GitHub Release](https://img.shields.io/github/v/release/lasuillard/pre-commit-hooks)

Personal pre-commit hooks to handle grunt tasks.

## 🪝 Available hooks

See [.pre-commit-hooks-.yaml](./.pre-commit-hooks.yaml) file for available hooks.

### check-file-pair

Check file in source directory have its pair in target directory.

### source-matching-test

Check Python source (`src/`) file has matching test file in (`tests/`) directory.

### test-matching-source

Check Python test (`tests/`) file has matching source file in (`src/`) directory.

### preferred-suffix

Check file has preferred suffix if there are multiple available suffixes.

### alloy-format

> [!IMPORTANT]
> This hook is just a convenience shortcut to invoke [Alloy](https://github.com/grafana/alloy) CLI. It does **NOT** install `alloy`.

Reformat `.alloy` files using `alloy fmt`.
