#!/usr/bin/env python3
"""List local Codex skills with frontmatter summaries."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


DEFAULT_ROOTS = [
    Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills",
    Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "plugins" / "cache",
]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    lines = text[4:end].splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if ":" not in line:
            index += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key not in {"name", "description"}:
            index += 1
            continue
        if value in {">", "|", ">-", "|-"}:
            block: list[str] = []
            index += 1
            while index < len(lines) and (lines[index].startswith(" ") or not lines[index].strip()):
                block.append(lines[index].strip())
                index += 1
            data[key] = " ".join(part for part in block if part)
            continue
        data[key] = value.strip('"').strip("'")
        index += 1
    return data


def iter_skill_files(roots: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    results: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("SKILL.md"):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            results.append(path)
    return sorted(results)


def main() -> int:
    parser = argparse.ArgumentParser(description="List local Codex skills as JSON.")
    parser.add_argument("--root", action="append", type=Path, help="Additional skill root to scan.")
    parser.add_argument("--query", help="Case-insensitive filter over name, description, and path.")
    args = parser.parse_args()

    roots = [*DEFAULT_ROOTS, *(args.root or [])]
    query = args.query.lower() if args.query else None
    skills = []
    for path in iter_skill_files(roots):
        meta = parse_frontmatter(path)
        if not meta.get("name"):
            continue
        item = {
            "name": meta.get("name", ""),
            "description": meta.get("description", ""),
            "path": str(path),
        }
        haystack = " ".join(item.values()).lower()
        if query and query not in haystack:
            continue
        skills.append(item)

    print(json.dumps(skills, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
