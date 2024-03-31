#!/usr/bin/env -S make -f

MAKEFLAGS += --warn-undefined-variable
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --silent

-include Makefile.*

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.DEFAULT_GOAL := help

help: Makefile  ## Show help
	for makefile in $(MAKEFILE_LIST)
	do
		@echo "$${makefile}"
		@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' "$${makefile}" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
	done


# =============================================================================
# Common
# =============================================================================
install:  ## Install the app locally
	poetry install
	pre-commit install --install-hooks
.PHONY: install

update:  ## Update deps and tools
	poetry update
	pre-commit autoupdate
.PHONY: update


# =============================================================================
# CI
# =============================================================================
ci: lint test  ## Run CI tasks
.PHONY: ci

format:  ## Run autoformatters
	poetry run ruff check --fix .
.PHONY: format

lint:  ## Run all linters
	poetry run ruff check .
	poetry run mypy --show-error-codes --pretty .
.PHONY: lint

test:  ## Run tests
	poetry run pytest
.PHONY: test

build:  ## Build application
	poetry build
.PHONY: build


# =============================================================================
# Handy Scripts
# =============================================================================
clean:  ## Remove temporary files
	rm -rf .mypy_cache/ .pytest_cache/ .ruff_cache/ build/ dist/ htmlcov/ .coverage coverage.xml report.xml
	find . -path '*/__pycache__*' -delete
	find . -path "*.log*" -delete
.PHONY: clean
