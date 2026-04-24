#!/usr/bin/env python3
"""Fail if the public ClawHub skill drifts into platform-control wording."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skill" / "random-coffee-best-fit-outreach"
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".txt"}

RISK_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("named social platform", re.compile(r"\b(?:linkedin|discord|telegram)\b", re.IGNORECASE)),
    ("platform-control tool", re.compile(r"\b(?:openclaw|computer use|browser|gui)\b", re.IGNORECASE)),
    ("message delivery wording", re.compile(r"\b(?:send|sent|sending|dm|dms)\b", re.IGNORECASE)),
    ("abuse-adjacent wording", re.compile(r"\b(?:selfbot|scrap(?:e|er|ing)|automate[ds]?)\b", re.IGNORECASE)),
)


def iter_skill_text_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and (path.name == "SKILL.md" or path.suffix.lower() in TEXT_SUFFIXES)
    )


def collect_issues(root: Path = SKILL_ROOT) -> list[str]:
    issues: list[str] = []
    for path in iter_skill_text_files(root):
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in RISK_PATTERNS:
                if pattern.search(line):
                    relative = path.relative_to(root)
                    issues.append(f"{relative}:{line_number}: {label}: {line.strip()}")
    return issues


def main() -> int:
    if not SKILL_ROOT.exists():
        print(f"missing skill root: {SKILL_ROOT}")
        return 1

    issues = collect_issues(SKILL_ROOT)
    if issues:
        print("ClawHub skill surface check failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("ClawHub skill surface check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
