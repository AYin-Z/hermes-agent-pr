"""Decide whether an installed runtime meets this checkout's Python floor."""
from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path


def needs_migration(installed: str, requirement: str) -> bool:
    # Fail explicitly if the project changes its version policy; do not guess
    # and accidentally bypass either the migration or the direct-update test.
    floor = re.fullmatch(r">=\s*(\d+)\.(\d+)(?:\.(\d+))?", requirement.strip())
    version = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", installed.strip())
    if floor is None or version is None:
        raise ValueError(f"Unsupported Python versions: {installed!r}, {requirement!r}")
    return tuple(map(int, version.groups())) < tuple(int(p or 0) for p in floor.groups())


if __name__ == "__main__":
    project = tomllib.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    print("true" if needs_migration(sys.argv[1], project["project"]["requires-python"]) else "false")
