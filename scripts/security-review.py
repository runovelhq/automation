#!/usr/bin/env python3
"""Detect high-risk workflow constructs without matching comments or shell guards."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml


def walk(value, path=""):
    if isinstance(value, dict):
        for key, child in value.items():
            current = f"{path}.{key}" if path else str(key)
            if str(key) in {"pull_request_target", "workflow_run"}:
                yield f"unsafe trigger at {current}"
            if str(key) == "secrets" and child == "inherit":
                yield f"hidden secret inheritance at {current}"
            yield from walk(child, current)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")


def main() -> int:
    errors = []
    for file in sorted(Path(".github/workflows").glob("*.yml")):
        document = yaml.safe_load(file.read_text(encoding="utf-8"))
        errors.extend(f"{file}: {error}" for error in walk(document))
        if "permissions" not in document:
            errors.append(f"{file}: missing top-level permissions")
    for error in errors:
        print(f"::error title=Workflow security::{error}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
