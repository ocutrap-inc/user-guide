#!/usr/bin/env python3
"""Compute a hash of every input that affects the rendered KB PDF.

Standalone (stdlib-only) so CI can run it without installing the heavy
PDF tooling (pandoc, weasyprint, pillow, etc.). Imported by both
`build_kb_pdf.py` (which writes a sidecar after a successful build)
and `verify_kb_pdf.py` (which compares to the committed sidecar in CI).
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARY_PATH = REPO_ROOT / "SUMMARY.md"
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build_kb_pdf.py"
STYLE_CSS    = REPO_ROOT / "scripts" / "kb_pdf_style.css"
OUTPUT_PDF   = REPO_ROOT / ".gitbook" / "assets" / "OcuTrap_Knowledge_Base.pdf"
SIDECAR      = OUTPUT_PDF.with_suffix(OUTPUT_PDF.suffix + ".sources.sha")


# Mirror of build_kb_pdf.py's SUMMARY parser, kept stdlib-only here so
# this module can run in CI without pulling in the build script's heavy
# imports. If build_kb_pdf.py's parsing rules change, update both.
@dataclass(frozen=True)
class _Page:
    title: str
    path: Path


_PAGE_RE = re.compile(r'^(\s*)\* \[([^\]]+)\]\(([^)]+\.md)\)')


def _walk_summary(summary_path: Path) -> list[_Page]:
    base = summary_path.parent
    out: list[_Page] = []
    for line in summary_path.read_text(encoding="utf-8").splitlines():
        m = _PAGE_RE.match(line)
        if m:
            _, title, ref = m.groups()
            out.append(_Page(title=title, path=base / ref))
    return out


def compute_source_hash(summary_path: Path = SUMMARY_PATH,
                        build_script: Path = BUILD_SCRIPT,
                        style_css: Path = STYLE_CSS) -> str:
    """SHA256 of every input that affects the rendered PDF.

    Inputs hashed (in this order):
      1. SUMMARY.md content
      2. Each markdown file referenced from SUMMARY (in document order)
      3. scripts/build_kb_pdf.py content
      4. scripts/kb_pdf_style.css content

    NOT included: image content under .gitbook/assets/. If you replace an
    image with the same filename, regenerate the PDF explicitly — the source
    hash won't catch that case.
    """
    h = hashlib.sha256()

    h.update(b"--summary--\n")
    h.update(summary_path.read_bytes())

    h.update(b"\n--markdown--\n")
    for page in _walk_summary(summary_path):
        if not page.path.exists():
            continue
        rel = page.path.relative_to(summary_path.parent)
        h.update(str(rel).encode("utf-8"))
        h.update(b":")
        h.update(page.path.read_bytes())
        h.update(b"\n")

    h.update(b"\n--script--\n")
    h.update(build_script.read_bytes())

    h.update(b"\n--style--\n")
    h.update(style_css.read_bytes())

    return h.hexdigest()


def write_sidecar(pdf_path: Path = OUTPUT_PDF,
                  summary_path: Path = SUMMARY_PATH,
                  build_script: Path = BUILD_SCRIPT,
                  style_css: Path = STYLE_CSS) -> Path:
    """Write `<pdf_path>.sources.sha` containing the current source hash."""
    sidecar = pdf_path.with_suffix(pdf_path.suffix + ".sources.sha")
    sidecar.write_text(compute_source_hash(summary_path, build_script, style_css) + "\n")
    return sidecar
