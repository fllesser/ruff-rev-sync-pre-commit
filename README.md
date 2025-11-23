# ruff-rev-sync-pre-commit

A pre-commit hook to automatically synchronize your [Ruff](https://github.com/astral-sh/ruff) version in `.pre-commit-config.yaml` with the version locked in `uv.lock`.

## Purpose

When managing Python dependencies with `uv`, you have a specific version of `ruff` locked in your `uv.lock` file. However, the `ruff-pre-commit` hook in your `.pre-commit-config.yaml` is often updated independently, leading to version mismatches between your local environment/CI and the pre-commit hook.

This hook solves that problem by:
1.  Reading the `ruff` version from your `uv.lock` file.
2.  Checking the `ruff-pre-commit` revision in your `.pre-commit-config.yaml`.
3.  Automatically updating the `rev` in `.pre-commit-config.yaml` to match the version in `uv.lock`.

## Usage

Add this hook to your `.pre-commit-config.yaml`. It should run *before* the main ruff hook to ensure the version is correct.

```yaml
repos:
  - repo: https://github.com/fllesser/ruff-rev-sync-pre-commit
    rev: v1.0.0
    hooks:
      - id: ruff-rev-sync
```

## How it works

The hook runs a Python script that:
1.  Locates `uv.lock` and `.pre-commit-config.yaml` in your project root.
2.  Parses `uv.lock` to find the installed version of `ruff`.
3.  Updates the `rev` field for `https://github.com/astral-sh/ruff-pre-commit` in `.pre-commit-config.yaml` to `v{version}`.

## Requirements

-   `uv` package manager (for `uv.lock`).
-   `ruff` must be present in your `uv.lock`.
