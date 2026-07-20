#!/usr/bin/env python3
"""Resolve and render pages from the scanned circuit-analysis textbook."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

KNOWN_SHA256 = "24C6AE612A3969F9A4032B1CCEE6ED0333B672A042DC6441650CC05A57E6C62E"
BOOK_TO_PDF_OFFSET = 9


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", part)
        if not match:
            raise ValueError(f"Invalid page expression: {part}")
        first = int(match.group(1))
        last = int(match.group(2) or first)
        if first < 1 or last < first:
            raise ValueError(f"Invalid page range: {part}")
        pages.update(range(first, last + 1))
    if not pages:
        raise ValueError("No pages requested")
    return sorted(pages)


def find_pdf(explicit: str | None) -> Path:
    if explicit:
        candidates = [Path(explicit)]
    elif os.environ.get("CIRCUIT_TEXTBOOK_PDF"):
        candidates = [Path(os.environ["CIRCUIT_TEXTBOOK_PDF"])]
    else:
        candidates = list(Path.cwd().glob("*电路分析基础*第2版*.pdf"))
    candidates = [path.expanduser().resolve() for path in candidates if path.is_file()]
    if len(candidates) != 1:
        raise RuntimeError(f"Expected exactly one textbook PDF, found {len(candidates)}")
    return candidates[0]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def page_count(pdf: Path) -> int | None:
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        return None
    result = subprocess.run([pdfinfo, str(pdf)], check=True, capture_output=True, text=True,
                            errors="replace")
    match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.MULTILINE)
    return int(match.group(1)) if match else None


def render(pdf: Path, pages: list[int], output: Path, dpi: int) -> list[dict[str, object]]:
    renderer = shutil.which("pdftoppm")
    if not renderer:
        raise RuntimeError("pdftoppm is required (install Poppler or use the bundled PDF runtime)")
    output.mkdir(parents=True, exist_ok=True)
    records = []
    for pdf_page in pages:
        prefix = output / f"pdf-{pdf_page:03d}"
        subprocess.run([renderer, "-f", str(pdf_page), "-l", str(pdf_page), "-r", str(dpi),
                        "-singlefile", "-png", str(pdf), str(prefix)], check=True)
        records.append({
            "pdf_page": pdf_page,
            "book_page": pdf_page - BOOK_TO_PDF_OFFSET if pdf_page > BOOK_TO_PDF_OFFSET else None,
            "image": str(prefix.with_suffix(".png").resolve()),
        })
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--book-pages")
    group.add_argument("--pdf-pages")
    parser.add_argument("--output", type=Path, default=Path("tmp/textbook"))
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--info", action="store_true")
    args = parser.parse_args()
    try:
        pdf = find_pdf(args.pdf)
        digest = sha256(pdf)
        count = page_count(pdf)
        info = {"pdf": str(pdf), "pages": count, "sha256": digest,
                "known_edition": digest == KNOWN_SHA256, "book_to_pdf_offset": BOOK_TO_PDF_OFFSET}
        if args.info:
            print(json.dumps(info, ensure_ascii=False, indent=2))
            return 0
        if not args.book_pages and not args.pdf_pages:
            parser.error("one of --book-pages or --pdf-pages is required unless --info is used")
        requested = parse_pages(args.book_pages or args.pdf_pages)
        pdf_pages = [page + BOOK_TO_PDF_OFFSET for page in requested] if args.book_pages else requested
        if count and max(pdf_pages) > count:
            raise ValueError(f"Requested PDF page exceeds the {count}-page scan")
        if args.dpi < 72 or args.dpi > 600:
            raise ValueError("DPI must be between 72 and 600")
        info["rendered"] = render(pdf, pdf_pages, args.output, args.dpi)
        manifest = args.output / "manifest.json"
        manifest.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
        print(manifest.resolve())
        return 0
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
