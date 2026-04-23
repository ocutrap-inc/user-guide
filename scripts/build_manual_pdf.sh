#!/usr/bin/env bash
# Convert printed/R1_Manual_v2.docx to printed/R1_Manual_v2.pdf
# Pipeline: docx -> HTML (pandoc, media extracted) -> PDF (Chrome headless)
#
# Requirements:
#   brew install pandoc
#   Google Chrome installed at /Applications/Google Chrome.app
#
# Run from the repo root (user-guide/).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DOCX="${REPO_ROOT}/printed/R1_Manual_v2.docx"
OUT_PDF="${REPO_ROOT}/printed/R1_Manual_v2.pdf"
WORK_DIR="$(mktemp -d)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [[ ! -f "${SRC_DOCX}" ]]; then
  echo "Source docx not found: ${SRC_DOCX}" >&2
  exit 1
fi
if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not found. Install with: brew install pandoc" >&2
  exit 1
fi
if [[ ! -x "${CHROME}" ]]; then
  echo "Google Chrome not found at ${CHROME}" >&2
  exit 1
fi

echo "Extracting docx -> HTML (work dir: ${WORK_DIR})"
pandoc "${SRC_DOCX}" \
  --extract-media="${WORK_DIR}" \
  --standalone \
  -o "${WORK_DIR}/manual.html"

echo "Rendering HTML -> PDF"
"${CHROME}" \
  --headless \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="${OUT_PDF}" \
  "file://${WORK_DIR}/manual.html"

echo "Wrote ${OUT_PDF} ($(du -h "${OUT_PDF}" | cut -f1))"
rm -rf "${WORK_DIR}"
