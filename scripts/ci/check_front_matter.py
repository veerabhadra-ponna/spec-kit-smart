#!/usr/bin/env python3
"""Validate that key Markdown templates contain required YAML front matter."""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_KEYS = (
    "feature_id",
    "title",
    "status",
    "branch",
    "semver",
    "created_at",
    "source_commit",
    "generator",
    "constitution_version",
)

TEMPLATES = [
    Path("templates/spec-template.md"),
    Path("templates/plan-template.md"),
    Path("templates/tasks-template.md"),
]


def parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing opening front matter delimiter")
    try:
        end = text.index("\n---", 4)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"{path}: missing closing front matter delimiter") from exc
    header = text[4:end].strip().splitlines()
    result: dict[str, str] = {}
    for line in header:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"{path}: invalid front matter line '{line}'")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def main() -> int:
    missing: list[str] = []
    for template in TEMPLATES:
        if not template.exists():
            missing.append(f"{template}: file not found")
            continue
        try:
            data = parse_front_matter(template)
        except ValueError as exc:
            missing.append(str(exc))
            continue
        for key in REQUIRED_KEYS:
            if key not in data or not data[key]:
                missing.append(f"{template}: missing required key '{key}'")
    if missing:
        for msg in missing:
            print(msg, file=sys.stderr)
        return 1
    print("Front matter validation passed for key templates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
