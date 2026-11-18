#!/usr/bin/env python3
"""Validate local links, images, SVG files and duplicate assets.

Run from the repository root:  python scripts/validate_assets.py
Exit code 1 if any error is found. Uses only the Python standard library.
Remote (http/https) URLs are not fetched; check them in a browser.
"""
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", ".venv"}
IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_ATTR = re.compile(r"""(?:src|href|srcset)\s*=\s*["']([^"']+)["']""", re.I)
COMMENT = re.compile(r"<!--.*?-->", re.S)


def files(pattern):
    for p in ROOT.rglob(pattern):
        if not SKIP_DIRS.intersection(p.parts):
            yield p


def is_local(target):
    return not re.match(r"^(https?:|mailto:|tel:|#|data:)", target, re.I)


def check_markdown(errors):
    for md in files("*.md"):
        text = COMMENT.sub("", md.read_text(encoding="utf-8"))
        targets = MD_LINK.findall(text) + HTML_ATTR.findall(text)
        for t in targets:
            if not is_local(t):
                continue
            path = t.split("#")[0].split("?")[0]
            if not path:
                continue
            if not (md.parent / path).resolve().exists():
                errors.append(f"{md.relative_to(ROOT)}: missing local file '{t}'")


def check_svgs(errors):
    for svg in files("*.svg"):
        try:
            ET.parse(svg)
        except ET.ParseError as exc:
            errors.append(f"{svg.relative_to(ROOT)}: invalid SVG ({exc})")


def check_duplicates(errors):
    seen = {}
    for p in (ROOT / "assets").rglob("*"):
        if p.is_file() and p.suffix.lower() in IMG_EXT:
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            if digest in seen:
                errors.append(
                    f"duplicate assets: {seen[digest].relative_to(ROOT)} and {p.relative_to(ROOT)}"
                )
            else:
                seen[digest] = p


MAGIC = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8\xff", ".jpeg": b"\xff\xd8\xff", ".gif": b"GIF8", ".webp": b"RIFF"}


def check_image_headers(errors):
    for p in (ROOT / "assets").rglob("*"):
        magic = MAGIC.get(p.suffix.lower())
        if p.is_file() and magic and not p.read_bytes().startswith(magic):
            errors.append(f"{p.relative_to(ROOT)}: content does not match its file extension")


def main():
    errors = []
    check_markdown(errors)
    check_svgs(errors)
    check_duplicates(errors)
    check_image_headers(errors)
    if errors:
        print(f"{len(errors)} problem(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
