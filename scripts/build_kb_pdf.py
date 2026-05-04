#!/usr/bin/env python3
"""Build OcuTrap_Knowledge_Base.pdf from the GitBook docs.

See pdf-docs/specs/2026-05-04-kb-pdf-compiler-design.md for design.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


# ============================================================================
# SUMMARY.md parser
# ============================================================================

@dataclass(frozen=True)
class SummaryEntry:
    kind: Literal["chapter", "page"]
    depth: int                # nesting depth of bullet (0 = top level)
    title: str
    path: Path | None         # None for chapter headers
    chapter: str | None       # the enclosing "## Chapter" or None for pre-chapter pages


# ---------------------------------------------------------------------------
# SUMMARY.md grammar (subset)
#
#   * [Title](path/to/file.md)         ← page entry
#     * [Sub-title](path/to/sub.md)    ← child page (2-space indent per level)
#   ## Chapter Heading                 ← chapter divider
#
# Constraints:
#   - Indentation: 2 spaces per nesting level (tabs not supported).
#   - Title text cannot contain `]`. Paths cannot contain `)`.
#   - Only `.md` paths are matched. External URLs and anchor-only links
#     are silently skipped.
#   - Lines that match neither pattern (e.g. `# Table of contents`, `***`,
#     `<details>`) are silently skipped.
# ---------------------------------------------------------------------------
_PAGE_RE = re.compile(r'^(\s*)\* \[([^\]]+)\]\(([^)]+\.md)\)')
_CHAPTER_RE = re.compile(r'^## (.+?)\s*$')


def parse_summary(summary_path: Path) -> list[SummaryEntry]:
    """Walk a GitBook SUMMARY.md in document order.

    Bullet indentation of 2 spaces = depth 1, 4 = depth 2, etc.
    `## Heading` lines become chapter entries (no path) and set the chapter
    label for subsequent page entries.
    """
    base = summary_path.parent
    entries: list[SummaryEntry] = []
    current_chapter: str | None = None

    for line in summary_path.read_text(encoding="utf-8").splitlines():
        ch = _CHAPTER_RE.match(line)
        if ch:
            current_chapter = ch.group(1)
            entries.append(SummaryEntry(
                kind="chapter", depth=0, title=current_chapter,
                path=None, chapter=current_chapter,
            ))
            continue
        pg = _PAGE_RE.match(line)
        if pg:
            indent, title, ref = pg.groups()
            depth = len(indent) // 2
            entries.append(SummaryEntry(
                kind="page", depth=depth, title=title,
                path=base / ref, chapter=current_chapter,
            ))
    return entries
