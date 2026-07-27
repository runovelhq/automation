#!/usr/bin/env python3
"""Reject mutable external GitHub Action references."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

USES = re.compile(r"^\s*(?:-\s*)?uses:\s*['\"]?([^\s'\"]+)", re.MULTILINE)
SHA = re.compile(r"^[0-9a-fA-F]{40}$")
DOCUMENTED_COMPATIBILITY = re.compile(
    r"^runovelhq/automation/\.github/workflows/[^@]+@v1$"
)


def validate_reference(reference: str) -> str | None:
    if reference.startswith("./") or reference.startswith("docker://"):
        return None
    if DOCUMENTED_COMPATIBILITY.fullmatch(reference):
        return None
    if "@" not in reference:
        return "reference has no revision"
    _, revision = reference.rsplit("@", 1)
    if not SHA.fullmatch(revision):
        return "external Action must use a full 40-character commit SHA"
    return None


def scan(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        if path.is_dir():
            files = sorted(p for p in path.rglob("*") if p.suffix in {".yml", ".yaml"})
        else:
            files = [path]
        for file in files:
            text = file.read_text(encoding="utf-8")
            for reference in USES.findall(text):
                error = validate_reference(reference)
                if error:
                    errors.append(f"{file}: {reference}: {error}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, default=[Path(".github"), Path("examples")])
    errors = scan(parser.parse_args().paths)
    for error in errors:
        print(f"::error title=Mutable Action reference::{error}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
