#!/usr/bin/env python3
"""Small, deterministic repository syntax and hygiene checks."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


def main() -> int:
    errors: list[str] = []
    for path in Path(".").rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"{path}:{number}: trailing whitespace")
        try:
            if path.suffix in {".yml", ".yaml"}:
                yaml.safe_load(text)
            elif path.suffix == ".json":
                json.loads(text)
        except (yaml.YAMLError, json.JSONDecodeError) as error:
            errors.append(f"{path}: syntax error: {error}")
        if path.suffix == ".md":
            fences = len(re.findall(r"^```", text, re.MULTILINE))
            if fences % 2:
                errors.append(f"{path}: unclosed Markdown code fence")
    for error in errors:
        print(f"::error::{error}")
    if errors:
        return 1
    print("YAML, JSON, Markdown, and whitespace validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
