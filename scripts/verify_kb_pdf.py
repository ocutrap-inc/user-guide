#!/usr/bin/env python3
"""Verify the committed Knowledge Base PDF is up-to-date with the docs.

Compares the source hash recorded in the committed `<pdf>.sources.sha`
sidecar to a hash freshly computed from the current docs. If they match,
the committed PDF was generated from the current sources and is in sync.

Stdlib-only — no pandoc, weasyprint, or pypdf needed in CI. The hash is
deterministic across environments (no PDF rendering involved), so this
gate doesn't false-fail on macOS-vs-Ubuntu layout differences.

Usage:
    python3 scripts/verify_kb_pdf.py [<pdf-path>]

Defaults to .gitbook/assets/OcuTrap_Knowledge_Base.pdf if no path given.
Exit 0 on match, 1 on drift, 2 on missing inputs.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from source_hash import (  # noqa: E402  — sys.path tweak above is intentional
    OUTPUT_PDF,
    compute_source_hash,
)


DRIFT_INSTRUCTIONS = """
::error::Committed Knowledge Base PDF is out of date with the docs.

The source hash recorded in {sidecar} does not match the current docs.
Someone changed a markdown file, the build script, or the stylesheet
without regenerating the PDF.

To fix (from the repo root):

  1. python3 scripts/build_kb_pdf.py
  2. git add {pdf} {sidecar}
  3. Commit and push.

See pdf-docs/README.md ("If you change the docs") for the full workflow.
"""


def main(argv: list[str]) -> int:
    pdf_path = Path(argv[1]) if len(argv) > 1 else OUTPUT_PDF
    sidecar = pdf_path.with_suffix(pdf_path.suffix + ".sources.sha")

    if not sidecar.exists():
        print(f"::error::No source-hash sidecar at {sidecar}.", file=sys.stderr)
        print(DRIFT_INSTRUCTIONS.format(sidecar=sidecar, pdf=pdf_path), file=sys.stderr)
        return 2

    committed_hash = sidecar.read_text().strip()
    current_hash = compute_source_hash()

    if committed_hash != current_hash:
        print("::error::Source hash mismatch.", file=sys.stderr)
        print(f"  committed:  {committed_hash}", file=sys.stderr)
        print(f"  current:    {current_hash}", file=sys.stderr)
        print(DRIFT_INSTRUCTIONS.format(sidecar=sidecar, pdf=pdf_path), file=sys.stderr)
        return 1

    print(f"PDF is up-to-date with docs (source hash {committed_hash[:12]}…). ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
