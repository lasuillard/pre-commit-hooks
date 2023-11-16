FROM python:3.11-slim-bookworm AS workspace

USER root:root

SHELL ["/bin/bash", "-c"]

# Core deps
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    git \
    gnupg2 \
    make \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

ARG WORKSPACE="/workspace"

WORKDIR "${WORKSPACE}"

# Dev tools
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Deps
COPY poetry.lock poetry.toml pyproject.toml ./
RUN poetry install --verbose --no-ansi --no-interaction --no-root --sync --with dev

VOLUME ["${WORKSPACE}/.venv"]

RUN git config --system --add safe.directory "${WORKSPACE}"

# Python control variables
ENV PYTHONUNBUFFERED="1"

HEALTHCHECK NONE
