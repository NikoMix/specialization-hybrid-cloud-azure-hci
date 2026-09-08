#!/usr/bin/env python3
"""Assert that every internal link in the built site resolves to a real file.

This exists because of a specific, silent failure mode. The theme's `card` and
`button` shortcodes pass their href through Hugo's `relURL`, and — verified on
Hugo 0.165 with baseURL `https://example.com/sub/`:

    relURL "/templates/x"  ->  /templates/x       (project sub-path dropped)
    relURL "templates/x"   ->  /sub/templates/x   (correct)

A leading slash therefore produces a link that works on a user/org Pages site
and 404s on a project Pages site — invisible in local preview, broken only once
published.

The parser matters. The deploy workflow builds with `--minify`, which strips
quotes from attribute values (`href=/docs/foo/`), so a regex looking for
`href="..."` matches nothing and the check passes having verified nothing.
`html.parser` tokenises attributes regardless of quoting. `--min-links` is the
backstop: a run that inspects almost nothing is a failure, not a pass.

Usage:
    hugo --gc --minify --baseURL "https://example.com/repo/"
    python scripts/check-links.py
"""
from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

EXTERNAL = ("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:")
LINK_ATTRS = {"href", "src"}


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.canonical: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "link" and values.get("rel") == "canonical" and values.get("href"):
            self.canonical = values["href"]
        for name, value in attrs:
            if name in LINK_ATTRS and value:
                self.links.append(value)


def collect(html: str) -> LinkCollector:
    parser = LinkCollector()
    parser.feed(html)
    parser.close()
    return parser


def resolves(target: Path) -> bool:
    return target.is_file() or (target / "index.html").is_file()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", default="public", type=Path)
    parser.add_argument(
        "--base-path",
        default=None,
        help="URL path prefix of the deployment, e.g. /my-repo/. "
        "Defaults to the path of the canonical URL Hugo wrote into the home page.",
    )
    parser.add_argument(
        "--min-links",
        type=int,
        default=500,
        help="Fail if fewer than this many internal links were inspected. Guards "
        "against a parser change silently turning this check into a no-op.",
    )
    args = parser.parse_args()

    if not args.public.is_dir():
        print(f"::error::{args.public} not found — run `hugo` before this script")
        return 2

    home = args.public / "index.html"
    if not home.is_file():
        print(f"::error::{home} not found — the build produced no home page")
        return 2

    base = args.base_path
    if base is None:
        canonical = collect(home.read_text(encoding="utf-8")).canonical
        if canonical is None:
            print("::error::no <link rel=canonical> on the home page — pass --base-path")
            return 2
        base = urlparse(canonical).path
    base = "/" + base.strip("/") + "/" if base.strip("/") else "/"

    broken: list[str] = []
    checked = 0
    pages = sorted(args.public.rglob("*.html"))

    for page in pages:
        for raw in collect(page.read_text(encoding="utf-8")).links:
            if raw.startswith(EXTERNAL) or raw.startswith("#"):
                continue
            path = unquote(urlparse(raw).path)
            if not path:
                continue
            checked += 1
            where = page.relative_to(args.public).as_posix()

            if path.startswith("/"):
                if not path.startswith(base):
                    broken.append(
                        f"{where}: {raw} is missing the deployment base path "
                        f"{base!r} — it will 404 once published"
                    )
                    continue
                target = args.public / path[len(base) :].lstrip("/")
            else:
                target = (page.parent / path).resolve()

            if not resolves(target):
                broken.append(f"{where}: {raw} does not resolve")

    print(f"Checked {checked} internal links across {len(pages)} pages (base path {base!r}).")

    for item in sorted(set(broken)):
        print(f"::error::{item}")
    if broken:
        print(f"\nFAIL: {len(set(broken))} broken internal link(s).")
        return 1

    if checked < args.min_links:
        print(
            f"::error::only {checked} internal links inspected, expected at least "
            f"{args.min_links} — this check is not actually checking anything"
        )
        return 1

    print("PASS: every internal link resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
