#!/usr/bin/env python3
"""Fetch every external Microsoft Learn URL cited in the content and report status.

The audit value of the reference-architecture page depends on the cited
Microsoft articles actually existing — a rotted link is a defect an auditor
will find. This is deliberately NOT part of the deploy workflow: it needs
network access to a third party and would make the build flaky. Run it before
an audit submission, or on a schedule.

Usage:
    python scripts/check-external-links.py
    python scripts/check-external-links.py --host learn.microsoft.com
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

URL = re.compile(r"https://[^\s)>\"'\]]+")
FENCE = re.compile(r"^\s*(```|~~~).*?^\s*\1", re.M | re.S)
CODE_SPAN = re.compile(r"`[^`\n]*`")
UA = "Mozilla/5.0 (compatible; link-check/1.0; +https://github.com/NikoMix)"


def citations(text: str) -> list[str]:
    """URLs a reader is meant to follow — code samples are illustrative, not cited.

    Without this, a placeholder such as
    `https://learn.microsoft.com/en-us/users/[username]/transcript/[id]`
    is checked as if it were a real citation.
    """
    text = FENCE.sub("", text)
    text = CODE_SPAN.sub("", text)
    return [url.rstrip(".,;") for url in URL.findall(text)]


def check(url: str, timeout: int) -> tuple[int | str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        return exc.code, url
    except Exception as exc:  # noqa: BLE001 — report any transport failure verbatim
        return type(exc).__name__, url


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", default="content", type=Path)
    parser.add_argument("--host", default="learn.microsoft.com")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    found: dict[str, list[str]] = {}
    for path in sorted(args.content.rglob("*.md")):
        for url in citations(path.read_text(encoding="utf-8")):
            if urlparse(url).hostname == args.host:
                found.setdefault(url, []).append(path.as_posix())

    if not found:
        print(f"::error::no {args.host} URLs found under {args.content} — nothing was checked")
        return 1

    print(f"Checking {len(found)} unique {args.host} URLs...\n")
    failures = []
    for url in sorted(found):
        status, final = check(url, args.timeout)
        redirected = final != url and urlparse(final).path != urlparse(url).path
        flag = "OK " if status == 200 else "FAIL"
        note = f"  -> {final}" if redirected else ""
        print(f"  [{flag}] {status}  {url}{note}")
        if status != 200:
            failures.append(f"{url} returned {status} (cited in {', '.join(found[url])})")

    print()
    for item in failures:
        print(f"::error::{item}")
    if failures:
        print(f"FAIL: {len(failures)} of {len(found)} URLs did not return 200.")
        return 1

    print(f"PASS: all {len(found)} {args.host} URLs return 200.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
