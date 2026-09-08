#!/usr/bin/env python3
"""Assert that every Markdown table in `content/` reaches the built HTML.

The Astro/Starlight version of this site silently swallowed tables: MDX parsed a
table indented four or more spaces (for example inside a `<TabItem>`) as an
indented code block, so an evidence checklist shipped as grey preformatted text
instead of a table. This guard makes that class of defect a build failure.

Two independent checks run:

  1. Static — no table row may be indented. An indented row is the exact defect
     that broke the Astro build and it is invisible in a rendered diff.
  2. Differential — the number of tables found in `content/**/*.md` must equal
     the number of `<table>` elements in `public/**/*.html`, counting only the
     canonical page for each source file.

Usage:
    hugo --gc
    python scripts/check-tables.py            # checks content/ against public/
    python scripts/check-tables.py --content-only
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\|.*\|\s*$")
DELIMITER = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
INDENTED_ROW = re.compile(r"^[ \t]+\|.*\|\s*$")
INDENTED_DELIMITER = re.compile(r"^[ \t]+\|(\s*:?-+:?\s*\|)+\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
HTML_TABLE = re.compile(r"<table[\s>]")


def strip_front_matter(lines: list[str]) -> list[str]:
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[i + 1 :]
    return lines


def scan(path: Path) -> tuple[int, list[str]]:
    """Return (table count, indentation problems) for one Markdown file."""
    lines = strip_front_matter(path.read_text(encoding="utf-8").splitlines())
    tables, problems, in_fence = 0, [], False

    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if DELIMITER.match(line) and i > 0 and ROW.match(lines[i - 1]):
            tables += 1
        elif INDENTED_DELIMITER.match(line) and i > 0 and INDENTED_ROW.match(lines[i - 1]):
            problems.append(
                f"{path.as_posix()}:{i}: table is indented "
                f"{len(line) - len(line.lstrip())} spaces — Markdown will render it as a "
                f"code block. Move it to column 0."
            )

    return tables, problems


def html_for(source: Path, content_root: Path, public_root: Path) -> Path | None:
    """Map a content file to the single HTML page Hugo generates from it."""
    rel = source.relative_to(content_root)
    stem = rel.parent if rel.name == "_index.md" else rel.with_suffix("")
    candidate = public_root / stem / "index.html"
    return candidate if candidate.is_file() else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", default="content", type=Path)
    parser.add_argument("--public", default="public", type=Path)
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument(
        "--min-tables",
        type=int,
        default=80,
        help="Fail if fewer than this many source tables were found. A source "
        "glob that matches nothing would otherwise compare 0 against 0 and pass.",
    )
    args = parser.parse_args()

    if not args.content.is_dir():
        print(f"::error::{args.content} not found — run from the repository root")
        return 2

    sources = sorted(args.content.rglob("*.md"))
    expected, problems, per_file = 0, [], {}

    for source in sources:
        count, found = scan(source)
        expected += count
        problems += found
        if count:
            per_file[source] = count

    print(f"Scanned {len(sources)} Markdown files — {expected} tables in {len(per_file)} of them.")

    if expected < args.min_tables:
        print(
            f"::error::only {expected} source tables found, expected at least "
            f"{args.min_tables} — this check is not actually checking anything"
        )
        return 1

    for problem in problems:
        print(f"::error::{problem}")
    if problems:
        print(f"\nFAIL: {len(problems)} indented table(s).")
        return 1

    if args.content_only:
        print("PASS: no indented tables (HTML comparison skipped).")
        return 0

    if not args.public.is_dir():
        print(f"::error::{args.public} not found — run `hugo` before this script")
        return 2

    rendered, missing = 0, []
    for source, count in per_file.items():
        page = html_for(source, args.content, args.public)
        if page is None:
            missing.append(f"{source.as_posix()}: no built HTML page found")
            continue
        found = len(HTML_TABLE.findall(page.read_text(encoding="utf-8")))
        rendered += found
        if found != count:
            missing.append(
                f"{source.as_posix()}: {count} table(s) in source but "
                f"{found} <table> element(s) in {page.as_posix()}"
            )

    print(f"Rendered {rendered} <table> element(s) across {len(per_file)} page(s).")

    for problem in missing:
        print(f"::error::{problem}")
    if missing or rendered != expected:
        print(f"\nFAIL: expected {expected} rendered tables, found {rendered}.")
        return 1

    print(f"PASS: all {expected} source tables render as HTML tables.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
