#!/usr/bin/env python3
"""Extract one version's section from CHANGELOG.md, for use as release notes.

Given a tag such as ``v1.2.0``, prints everything between the ``## [1.2.0]``
heading and the next ``##`` heading. Exits non-zero when the version has no
section, so a release cannot be published without a changelog entry.

Link reference definitions (the ``[1.2.0]: https://…`` block Keep a Changelog
keeps at the bottom of the file) are stripped, so use inline links inside
section bodies.

Standard library only.

Usage::

    python3 .github/scripts/extract_changelog.py v1.2.0 [CHANGELOG.md]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HEADING = re.compile(r"^##\s+\[?(?P<version>[^\]\s]+)\]?")
LINK_DEFINITION = re.compile(r"^\[[^\]]+\]:\s*\S+\s*$")


def extract(changelog: str, version: str) -> str | None:
    lines = changelog.splitlines()
    collected: list[str] | None = None

    for line in lines:
        match = HEADING.match(line)
        if match:
            if collected is not None:
                break
            if match.group("version").lstrip("vV") == version:
                collected = []
            continue
        if collected is not None and not LINK_DEFINITION.match(line):
            collected.append(line)

    if collected is None:
        return None
    return "\n".join(collected).strip()


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(f"usage: {argv[0]} TAG [CHANGELOG.md]", file=sys.stderr)
        return 2

    version = argv[1].lstrip("vV")
    path = Path(argv[2] if len(argv) > 2 else "CHANGELOG.md")

    if not path.exists():
        print(f"{path}: not found", file=sys.stderr)
        return 1

    section = extract(path.read_text(encoding="utf-8"), version)

    if section is None:
        print(
            f"{path}: no section found for version {version!r}.\n"
            f"Add a '## [{version}] - YYYY-MM-DD' heading before tagging.",
            file=sys.stderr,
        )
        return 1

    if not section:
        print(f"{path}: section for version {version!r} is empty.", file=sys.stderr)
        return 1

    print(section)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
