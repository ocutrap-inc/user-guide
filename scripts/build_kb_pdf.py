#!/usr/bin/env python3
"""Build OcuTrap_Knowledge_Base.pdf from the GitBook docs.

See pdf-docs/specs/2026-05-04-kb-pdf-compiler-design.md for design.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

# macOS dylib quirk: WeasyPrint's CFFI loader needs help finding Pango/Cairo
# from Homebrew. Set this BEFORE any weasyprint import below.
if sys.platform == "darwin" and "DYLD_FALLBACK_LIBRARY_PATH" not in os.environ:
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = "/opt/homebrew/lib"


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


# ============================================================================
# GitBook syntax transforms
# ============================================================================

_HINT_RE = re.compile(
    r'\{%\s*hint\s+style="([^"]+)"\s*%\}\n(.*?)\n\{%\s*endhint\s*%\}',
    re.DOTALL,
)
_EMBED_RE = re.compile(r'\{%\s*embed\s+url="([^"]+)"\s*%\}')

_KNOWN_HINT_STYLES = {"info", "danger", "warning", "success"}


def transform_hints(text: str) -> str:
    def repl(m: re.Match) -> str:
        style = m.group(1)
        if style not in _KNOWN_HINT_STYLES:
            style = "info"
        body = m.group(2)
        # Blank lines around body so pandoc sees inline markdown inside the div
        return f'<div class="hint hint-{style}">\n\n{body}\n\n</div>'
    return _HINT_RE.sub(repl, text)


def transform_embeds(text: str) -> str:
    return _EMBED_RE.sub(lambda m: f"[{m.group(1)}]({m.group(1)})", text)


# ============================================================================
# Image pipeline — path normalization
# ============================================================================

import unicodedata


def _strip_angle_brackets(s: str) -> str:
    s = s.strip()
    if s.startswith("<") and s.endswith(">"):
        return s[1:-1].strip()
    return s


def _normalize_spaces(s: str) -> str:
    """Collapse all Unicode whitespace to a regular space for matching."""
    return "".join(" " if unicodedata.category(c).startswith("Z") else c for c in s)


def resolve_image_path(raw: str, source_md: Path) -> Path | None:
    """Resolve a markdown image ref to an on-disk Path, or None if missing.

    Handles `<>`-wrapped paths and Unicode-space variants in filenames.
    External http(s):// URLs are NOT handled here — see fetch_external().
    """
    raw = _strip_angle_brackets(raw)
    if raw.startswith(("http://", "https://")):
        return None  # caller must use fetch_external

    base = source_md.parent
    direct = (base / raw).resolve()
    if direct.exists():
        return direct

    # Fuzzy fallback: scan the resolved parent directory for a filename whose
    # space-normalized form matches the requested one.
    parent = direct.parent
    if not parent.exists():
        return None
    target = _normalize_spaces(direct.name)
    for candidate in parent.iterdir():
        if _normalize_spaces(candidate.name) == target:
            return candidate
    return None


# ============================================================================
# Image pipeline — conversion and downscaling
# ============================================================================

import hashlib

from PIL import Image
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

MAX_IMAGE_WIDTH = 1600
JPEG_QUALITY = 82
HEIC_EXTS = {".heic", ".heif"}
RASTER_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"} | HEIC_EXTS


def _cache_key(src: Path) -> str:
    """Stable cache key from path + mtime + transform params."""
    h = hashlib.sha256()
    h.update(str(src.resolve()).encode())
    h.update(str(src.stat().st_mtime_ns).encode())
    h.update(f"w{MAX_IMAGE_WIDTH}q{JPEG_QUALITY}".encode())
    return h.hexdigest()[:16]


def process_image(src: Path, *, cache_dir: Path) -> Path:
    """Return a path to a print-ready version of the image.

    May be the original (when no transform is needed), or a cached derivative.
    """
    if src.suffix.lower() not in RASTER_EXTS:
        return src

    needs_heic   = src.suffix.lower() in HEIC_EXTS
    needs_gif    = src.suffix.lower() == ".gif"
    needs_resize = False
    try:
        with Image.open(src) as probe:
            if probe.width > MAX_IMAGE_WIDTH:
                needs_resize = True
    except Exception:
        return src  # let WeasyPrint deal with it; we don't break the build over one image

    if not (needs_heic or needs_gif or needs_resize):
        return src

    cache_dir.mkdir(parents=True, exist_ok=True)
    key = _cache_key(src)
    out_ext = ".jpg" if needs_heic else ".png" if needs_gif else src.suffix.lower()
    out = cache_dir / f"{src.stem}.{key}{out_ext}"
    if out.exists():
        return out

    with Image.open(src) as im:
        if needs_gif and getattr(im, "n_frames", 1) > 1:
            im.seek(0)
        if im.mode not in ("RGB", "RGBA", "L"):
            im = im.convert("RGB")
        if im.width > MAX_IMAGE_WIDTH:
            ratio = MAX_IMAGE_WIDTH / im.width
            im = im.resize((MAX_IMAGE_WIDTH, int(im.height * ratio)), Image.LANCZOS)
        if needs_heic:
            im.convert("RGB").save(out, "JPEG", quality=JPEG_QUALITY, optimize=True)
        elif needs_gif:
            im.save(out, "PNG", optimize=True)
        else:
            save_kwargs = {"optimize": True}
            if out_ext in (".jpg", ".jpeg"):
                save_kwargs["quality"] = JPEG_QUALITY
                if im.mode != "RGB":
                    im = im.convert("RGB")
            im.save(out, **save_kwargs)
    return out


# ============================================================================
# Image pipeline — external URL fetcher
# ============================================================================

import requests

_CONTENT_TYPE_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/heic": ".heic",
}


def fetch_external(url: str, *, cache_dir: Path) -> Path | None:
    """Download an external image to the cache and return its local path.

    Returns None on any failure — external image errors are warnings,
    not build failures.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(url.encode()).hexdigest()[:16]

    # Check for any existing cached file with this key prefix
    for existing in cache_dir.glob(f"ext-{key}.*"):
        return existing

    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"  WARN: external fetch failed for {url}: {e}")
        return None

    ctype = r.headers.get("Content-Type", "").split(";")[0].strip().lower()
    ext = _CONTENT_TYPE_EXT.get(ctype, ".bin")
    out = cache_dir / f"ext-{key}{ext}"
    out.write_bytes(r.content)
    return out


# ============================================================================
# Image pipeline — markdown rewriting
# ============================================================================

@dataclass
class BuildContext:
    cache_dir: Path
    images_embedded: int = 0
    images_converted: int = 0
    images_downloaded: int = 0
    images_skipped: int = 0


_MD_IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+|<[^>]+>)\)')
_HTML_IMG_RE = re.compile(r'<img\s+([^>]*?)src="([^"]+)"([^>]*)/?>', re.IGNORECASE)


def _resolve_or_fetch(raw: str, source_md: Path, ctx: BuildContext) -> Path | None:
    raw = _strip_angle_brackets(raw)
    if raw.startswith(("http://", "https://")):
        out = fetch_external(raw, cache_dir=ctx.cache_dir)
        if out:
            ctx.images_downloaded += 1
        return out
    p = resolve_image_path(raw, source_md)
    if p is None:
        return None
    out = process_image(p, cache_dir=ctx.cache_dir)
    if out != p:
        ctx.images_converted += 1
    return out


def rewrite_images(text: str, *, source_md: Path, ctx: BuildContext) -> str:
    def md_repl(m: re.Match) -> str:
        alt, raw = m.group(1), m.group(2)
        out = _resolve_or_fetch(raw, source_md, ctx)
        if out is None:
            ctx.images_skipped += 1
            print(f"  WARN: skipped image {raw!r} referenced from {source_md.name}")
            return ""
        ctx.images_embedded += 1
        return f"![{alt}]({out.as_uri()})"

    def html_repl(m: re.Match) -> str:
        before, raw, after = m.group(1), m.group(2), m.group(3)
        out = _resolve_or_fetch(raw, source_md, ctx)
        if out is None:
            ctx.images_skipped += 1
            print(f"  WARN: skipped <img> {raw!r} referenced from {source_md.name}")
            return ""
        ctx.images_embedded += 1
        return f'<img {before}src="{out.as_uri()}"{after}/>'

    text = _MD_IMG_RE.sub(md_repl, text)
    text = _HTML_IMG_RE.sub(html_repl, text)
    # Tidy: collapse stray empty lines left by stripped images
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ============================================================================
# Document assembly
# ============================================================================

_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)$', re.MULTILINE)


def _shift_headings(text: str, by: int) -> str:
    """Shift all ATX headings down by `by` levels, capped at H6."""
    if by <= 0:
        return text
    def repl(m: re.Match) -> str:
        level = min(len(m.group(1)) + by, 6)
        return f"{'#' * level} {m.group(2)}"
    return _HEADING_RE.sub(repl, text)


def _preprocess_page(text: str, source_md: Path, ctx: BuildContext) -> str:
    text = transform_hints(text)
    text = transform_embeds(text)
    text = rewrite_images(text, source_md=source_md, ctx=ctx)
    return text


def assemble_document(entries: list[SummaryEntry], *, ctx: BuildContext) -> str:
    """Concatenate SUMMARY entries into one big markdown doc.

    Heading-level mapping:
      - chapter entries → H1 divider (forces page break via CSS)
      - pages under a chapter → original H1 demoted to H2, then by depth
      - pages with no chapter → original H1 stays H1
    """
    parts: list[str] = []
    pages_processed = 0
    for entry in entries:
        if entry.kind == "chapter":
            parts.append(f"# {entry.title}\n")
            continue
        if entry.path is None or not entry.path.exists():
            print(f"  WARN: page missing on disk: {entry.title} ({entry.path})")
            continue
        body = entry.path.read_text(encoding="utf-8")
        body = _preprocess_page(body, source_md=entry.path, ctx=ctx)
        # Shift: +1 if under any chapter, +depth for nesting
        shift = (1 if entry.chapter else 0) + entry.depth
        body = _shift_headings(body, shift)
        parts.append(body)
        pages_processed += 1
    ctx.pages_processed = pages_processed  # type: ignore[attr-defined]
    return "\n\n".join(parts) + "\n"


# ============================================================================
# Render: markdown → HTML → PDF
# ============================================================================

import subprocess

from weasyprint import HTML, CSS as WeasyCSS
from pypdf import PdfReader


def _markdown_to_html(markdown: str) -> str:
    """Run pandoc to turn the assembled markdown into a standalone HTML doc."""
    proc = subprocess.run(
        [
            "pandoc",
            "--from=gfm+raw_html+pipe_tables+definition_lists",
            "--to=html5",
            "--standalone",
            "--toc",
            "--toc-depth=3",
            "--metadata=title:OcuTrap Knowledge Base",
        ],
        input=markdown,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"pandoc failed:\n{proc.stderr}")
    return proc.stdout


def render_pdf(markdown: str, *, css_path: Path, output: Path) -> int:
    """Render assembled markdown to a PDF. Returns page count."""
    html = _markdown_to_html(markdown)
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(output.parent)).write_pdf(
        target=str(output),
        stylesheets=[WeasyCSS(filename=str(css_path))],
    )
    return len(PdfReader(str(output)).pages)


# ============================================================================
# CLI
# ============================================================================

import argparse

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SUMMARY = REPO_ROOT / "SUMMARY.md"
DEFAULT_OUTPUT  = REPO_ROOT / "pdf-docs" / "online" / "OcuTrap_Knowledge_Base.pdf"
DEFAULT_CSS     = REPO_ROOT / "scripts" / "kb_pdf_style.css"
DEFAULT_CACHE   = REPO_ROOT / ".cache" / "kb-pdf"


def _print_summary(ctx: BuildContext, output: Path, page_count: int) -> None:
    pages_processed = getattr(ctx, "pages_processed", 0)
    size_mb = output.stat().st_size / (1024 * 1024)
    print()
    print("─" * 60)
    print(f"Markdown files processed: {pages_processed}")
    print(f"Images embedded:          {ctx.images_embedded} "
          f"({ctx.images_converted} converted, "
          f"{ctx.images_downloaded} downloaded externally, "
          f"{ctx.images_skipped} skipped)")
    print(f"Final PDF: {size_mb:.1f} MB, {page_count} pages")
    print(f"Output:    {output}")
    print("─" * 60)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build OcuTrap_Knowledge_Base.pdf from GitBook docs")
    p.add_argument("--summary",   type=Path, default=DEFAULT_SUMMARY)
    p.add_argument("--output",    type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--css",       type=Path, default=DEFAULT_CSS)
    p.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    p.add_argument("--min-pages", type=int, default=50)
    p.add_argument("--max-pages", type=int, default=1000)
    p.add_argument("--max-size-mb", type=int, default=100)
    args = p.parse_args(argv)

    ctx = BuildContext(cache_dir=args.cache_dir)
    entries = parse_summary(args.summary)
    print(f"Parsed {len(entries)} SUMMARY entries from {args.summary}")
    assembled = assemble_document(entries, ctx=ctx)
    page_count = render_pdf(assembled, css_path=args.css, output=args.output)
    _print_summary(ctx, args.output, page_count)

    size_mb = args.output.stat().st_size / (1024 * 1024)
    if page_count < args.min_pages or page_count > args.max_pages:
        print(f"FAIL: page count {page_count} outside [{args.min_pages}, {args.max_pages}]",
              file=sys.stderr)
        args.output.unlink(missing_ok=True)
        return 2
    if size_mb > args.max_size_mb:
        print(f"FAIL: PDF size {size_mb:.1f} MB exceeds max {args.max_size_mb} MB",
              file=sys.stderr)
        args.output.unlink(missing_ok=True)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
