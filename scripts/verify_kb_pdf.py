#!/usr/bin/env python3
"""Verify two PDFs are content-equivalent (same page count + same extracted text).

Used by .github/workflows/build-kb-pdf.yml to confirm the committed
KB PDF matches what `build_kb_pdf.py` produces from the current docs.

WeasyPrint output is non-deterministic at the byte level (creation
timestamps and object IDs vary between runs), so a binary diff would
always fire. Comparing extracted text catches real docs drift while
ignoring cosmetic binary churn.

Usage:
    python3 scripts/verify_kb_pdf.py <committed.pdf> <built.pdf>

Exit code 0 if content matches, 1 if it drifted (with a clear
contributor message pointing at pdf-docs/README.md).
"""

from __future__ import annotations

import sys
from pathlib import Path

from pypdf import PdfReader


DRIFT_INSTRUCTIONS = """
::error::Committed Knowledge Base PDF is out of date with the docs.

The KB PDF in .gitbook/assets/OcuTrap_Knowledge_Base.pdf does not match what
scripts/build_kb_pdf.py produces from the current SUMMARY.md and markdown.

To fix (from the repo root):

  1. python3 scripts/build_kb_pdf.py
  2. git add .gitbook/assets/OcuTrap_Knowledge_Base.pdf
  3. Commit and push.

See pdf-docs/README.md ("If you change the docs") for the full workflow.
"""


def _pages_text(path: Path) -> list[str]:
    return [p.extract_text() for p in PdfReader(str(path)).pages]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"usage: {argv[0]} <committed.pdf> <built.pdf>", file=sys.stderr)
        return 2

    committed = Path(argv[1])
    built = Path(argv[2])

    if not committed.exists():
        print(f"committed PDF not found: {committed}", file=sys.stderr)
        return 2
    if not built.exists():
        print(f"built PDF not found: {built}", file=sys.stderr)
        return 2

    committed_pages = _pages_text(committed)
    built_pages = _pages_text(built)

    if len(committed_pages) != len(built_pages):
        print(
            f"::error::Page count drift: committed has {len(committed_pages)} pages, "
            f"built has {len(built_pages)} pages.",
            file=sys.stderr,
        )
        print(DRIFT_INSTRUCTIONS, file=sys.stderr)
        return 1

    for i, (c, b) in enumerate(zip(committed_pages, built_pages), start=1):
        if c != b:
            print(f"::error::Page {i} text differs from what the docs produce.", file=sys.stderr)
            print(DRIFT_INSTRUCTIONS, file=sys.stderr)
            return 1

    print(f"Committed PDF matches docs ({len(built_pages)} pages, content equivalent). ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
