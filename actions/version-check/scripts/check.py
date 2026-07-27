#!/usr/bin/env python3
"""Strict SemVer release input validation."""
from __future__ import annotations

import os
import re
import sys

SEMVER = re.compile(
    r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def parse(version: str) -> dict[str, str]:
    match = SEMVER.fullmatch(version)
    if not match:
        raise ValueError("version must match vMAJOR.MINOR.PATCH with an optional SemVer pre-release")
    major, minor, patch, suffix = match.groups()
    if suffix and any(part.isdigit() and len(part) > 1 and part.startswith("0") for part in suffix.split(".")):
        raise ValueError("numeric pre-release identifiers must not contain leading zeroes")
    normalized = f"{major}.{minor}.{patch}" + (f"-{suffix}" if suffix else "")
    return {
        "normalized_version": normalized,
        "major": major,
        "major_minor": f"{major}.{minor}",
        "prerelease": str(bool(suffix)).lower(),
    }


def main() -> int:
    try:
        values = parse(os.environ.get("INPUT_VERSION", ""))
    except ValueError as error:
        print(f"::error title=Invalid release version::{error}")
        return 1
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            for key, value in values.items():
                handle.write(f"{key}={value}\n")
    for key, value in values.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
