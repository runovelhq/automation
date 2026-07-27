#!/usr/bin/env python3
"""Validate relative Markdown links without network access."""
import re
import sys
from pathlib import Path

errors = []
for document in Path(".").rglob("*.md"):
    if ".git" in document.parts:
        continue
    text = document.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = target.split("#", 1)[0]
        if path and not (document.parent / path).resolve().exists():
            errors.append(f"{document}: missing local link target {target}")
for error in errors:
    print(f"::error::{error}")
sys.exit(bool(errors))
