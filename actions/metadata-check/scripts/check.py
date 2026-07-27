#!/usr/bin/env python3
"""Offline repository metadata validation with GitHub annotations."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

OBSOLETE_NAMESPACES = ("Alireza" + "Sayyari/", "alireza" + "sayyari/")
INVALID_IMAGE_NAMESPACES = tuple("ghcr.io/" + value for value in OBSOLETE_NAMESPACES)


def validate(root: Path, require_changelog: bool, require_contributing: bool) -> list[str]:
    errors: list[str] = []
    required = ["README.md", "LICENSE", "SECURITY.md"]
    if require_contributing:
        required.append("CONTRIBUTING.md")
    if require_changelog:
        required.append("CHANGELOG.md")
    for name in required:
        if not (root / name).is_file():
            errors.append(f"missing required file: {name}")

    readme = (root / "README.md")
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        if not re.search(r"(?im)^#+\s+.*version", text):
            errors.append("README.md must document the versioning model")

    license_file = root / "LICENSE"
    if license_file.is_file() and "Apache License" not in license_file.read_text(encoding="utf-8"):
        errors.append("LICENSE must contain recognizable license text")

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for namespace in OBSOLETE_NAMESPACES:
            if namespace in text:
                errors.append(f"{path.relative_to(root)} uses obsolete personal namespace {namespace}")
        for namespace in INVALID_IMAGE_NAMESPACES:
            if namespace in text:
                errors.append(f"{path.relative_to(root)} uses invalid image namespace {namespace}")
        if path.name in {"Dockerfile", "Containerfile"}:
            for line_no, line in enumerate(text.splitlines(), 1):
                if line.startswith("FROM ") and " AS " not in line.upper() and "@sha256:" not in line:
                    errors.append(f"{path.relative_to(root)}:{line_no} base image lacks digest or named stage")
                if line.startswith("LABEL ") and "org.opencontainers.image.licenses=" in line and "Apache-2.0" not in line:
                    errors.append(f"{path.relative_to(root)}:{line_no} has unexpected SPDX license label")
    return sorted(set(errors))


def main() -> int:
    root = Path(os.environ.get("INPUT_WORKING_DIRECTORY", ".")).resolve()
    errors = validate(
        root,
        os.environ.get("INPUT_REQUIRE_CHANGELOG", "false").lower() == "true",
        os.environ.get("INPUT_REQUIRE_CONTRIBUTING", "true").lower() == "true",
    )
    for error in errors:
        print(f"::error title=Repository metadata::{error}")
    if errors:
        print(f"metadata check failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("repository metadata is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
