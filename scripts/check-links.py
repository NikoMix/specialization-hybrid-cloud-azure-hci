#!/usr/bin/env python3
"""Assert that every internal link in the built site resolves to a real file.

This exists because of a specific, silent failure mode. The theme's `card` and
`button` shortcodes pass their href through Hugo's `relURL`, and — verified on
Hugo 0.165 with baseURL `https://example.com/sub/`:

    relURL "/templates/x"  ->  /templates/x       (project sub-path dropped)
    relURL "templates/x"   ->  /sub/templates/x   (correct)

A leading slash therefore produces a link that works on a user/org Pages site
and 404s on a project Pages site — invisible in local preview, broken only once
published. Rather than trusting a convention, this checks the built output.

Usage:
    hugo --gc --baseURL "https://example.com/repo/"
    python scripts/check-links.py --base-path /repo/
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ATTR = re.compile(r'(?:href|src)="([^"]*)"')
EXTERNAL = ("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:")


def resolve(target: Path) -> bool:
    return target.is_file() or (target / "index.html").is_file()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", default="public", type=Path)
    parser.add_argument(
        "--base-path",
        default=None,
        help="URL path prefix of the deployment, e.g. /my-repo/. "
        "Defaults to the baseURL path Hugo wrote into the site.",
    )
    args = parser.parse_args()

    if not args.public.is_dir():
        print(f"::error::{args.public} not found — run `hugo` before this script")
        return 2

    pages = sorted(args.public.rglob("*.html"))
    base = args.base_path
    if base is None:
        # Recover the deployed sub-path from the canonical link Hugo emits.
        home = args.public / "index.html"
        found = re.search(r'<link rel="canonical" href="([^"]+)"', home.read_text(encoding="utf-8"))
        base = urlparse(found.group(1)).path if found else "/"
    base = "/" + base.strip("/") + "/" if base.strip("/") else "/"

    broken: list[str] = []
    checked = 0

    for page in pages:
        html = page.read_text(encoding="utf-8")
        for raw in ATTR.findall(html):
            if not raw or raw.startswith(EXTERNAL) or raw.startswith("#"):
                continue
            path = unquote(urlparse(raw).path)
            if not path:
                continue
            checked += 1

            if path.startswith("/"):
                if not path.startswith(base):
                    broken.append(
                        f"{page.relative_to(args.public).as_posix()}: {raw} is missing the "
                        f"deployment base path {base!r} — it will 404 once published"
                    )
                    continue
                target = args.public / path[len(base) :].lstrip("/")
            else:
                target = (page.parent / path).resolve()

            if not resolve(target):
                broken.append(f"{page.relative_to(args.public).as_posix()}: {raw} does not resolve")

    print(f"Checked {checked} internal links across {len(pages)} pages (base path {base!r}).")

    for item in sorted(set(broken)):
        print(f"::error::{item}")
    if broken:
        print(f"\nFAIL: {len(set(broken))} broken internal link(s).")
        return 1

    print("PASS: every internal link resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
