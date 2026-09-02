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
# GitBook syntax transforms + frontmatter handling
# ============================================================================

_FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n+', re.DOTALL)
_HIDDEN_RE = re.compile(r'^\s*hidden\s*:\s*true\s*$', re.MULTILINE | re.IGNORECASE)
_PDF_EXCLUDE_RE = re.compile(r'^\s*pdf-exclude\s*:\s*true\s*$', re.MULTILINE | re.IGNORECASE)

_HINT_RE = re.compile(
    r'\{%\s*hint\s+style="([^"]+)"\s*%\}\n(.*?)\n\{%\s*endhint\s*%\}',
    re.DOTALL,
)
_EMBED_RE = re.compile(r'\{%\s*embed\s+url="([^"]+)"\s*%\}')
_CONTENT_REF_RE = re.compile(
    r'\{%\s*content-ref\s+url="([^"]+)"\s*%\}\s*(.*?)\s*\{%\s*endcontent-ref\s*%\}',
    re.DOTALL,
)
_FILE_RE = re.compile(r'\{%\s*file\s+src="([^"]+)"\s*%\}')
_TABS_RE = re.compile(r'\{%\s*tabs\s*%\}\s*(.*?)\s*\{%\s*endtabs\s*%\}', re.DOTALL)
_TAB_RE = re.compile(
    r'\{%\s*tab\s+title="([^"]+)"\s*%\}\s*(.*?)\s*\{%\s*endtab\s*%\}',
    re.DOTALL,
)
# Bare GitBook-hosted video URLs that pandoc would auto-link as ugly raw text.
_BARE_VIDEO_URL_RE = re.compile(
    r'(?<![("\[])(https://files\.gitbook\.com/[^\s)<\]]+\.(?:mp4|mov|webm)[^\s)<\]]*)',
    re.IGNORECASE,
)

_KNOWN_HINT_STYLES = {"info", "danger", "warning", "success"}
_VIDEO_EXTS = (".mp4", ".mov", ".webm", ".m4v", ".avi")
_VIDEO_HOSTS = ("youtube.com", "youtu.be", "vimeo.com")


def strip_frontmatter(text: str) -> tuple[str, dict[str, bool]]:
    """Remove leading YAML frontmatter; return (cleaned_text, flags).

    `flags` exposes the booleans we care about:
      - `hidden`      — page is hidden from BOTH the website and the PDF
      - `pdf-exclude` — page is on the website but skipped from the PDF
                        (use for press/marketing pages that aren't part
                        of the customer manual)

    Frontmatter is content between two `---` markers at the very top of
    the file. GitBook-authored markdown commonly puts `description:` and
    `hidden:` here; without stripping, pandoc renders these lines as
    visible body text.
    """
    flags: dict[str, bool] = {"hidden": False, "pdf-exclude": False}
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return text, flags
    block = m.group(1)
    if _HIDDEN_RE.search(block):
        flags["hidden"] = True
    if _PDF_EXCLUDE_RE.search(block):
        flags["pdf-exclude"] = True
    return text[m.end():], flags


def _is_video_url(url: str) -> bool:
    u = url.lower().split("?", 1)[0]
    if any(u.endswith(ext) for ext in _VIDEO_EXTS):
        return True
    return any(host in url.lower() for host in _VIDEO_HOSTS)


def _video_callout(url: str) -> str:
    """Render a video reference as a styled callout block.

    Print can't play videos and the GitBook-hosted URLs are ~200 characters
    of opaque tokens — useless in print. So we just point customers to the
    online docs and skip the URL entirely.
    """
    return (
        f'<div class="video-link">\n\n'
        f'**▶ This page has a video.** Watch it online at '
        f'<a href="{url}">docs.ocutrap.com</a>.\n\n'
        f'</div>'
    )


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
    """Convert {% embed url=X %} to a link, with friendly callout for videos."""
    def repl(m: re.Match) -> str:
        url = m.group(1)
        if _is_video_url(url):
            return _video_callout(url)
        return f"[{url}]({url})"
    return _EMBED_RE.sub(repl, text)


def transform_content_refs(text: str) -> str:
    """Drop the {% content-ref %} wrapper. The body usually contains the link
    already; if not, leave nothing — the SUMMARY-driven assembly already
    provides cross-page navigation via the TOC."""
    def repl(m: re.Match) -> str:
        body = m.group(2).strip()
        return body if body else ""
    return _CONTENT_REF_RE.sub(repl, text)


def transform_files(text: str) -> str:
    """Render {% file src="X" %} as a download callout. The PDF reader can
    follow the link if the relative path resolves on the live site."""
    def repl(m: re.Match) -> str:
        src = m.group(1)
        # Friendly label: just the filename
        name = src.rsplit("/", 1)[-1]
        return (
            f'<div class="file-link">\n\n'
            f'**📎 Download:** [{name}]({src})\n\n'
            f'</div>'
        )
    return _FILE_RE.sub(repl, text)


def transform_tabs(text: str) -> str:
    """Flatten {% tabs %}...{% endtabs %} into sequential subsections.

    Tabs are interactive on the website but make no sense in a PDF. Each
    tab becomes a labeled chunk of content rendered in document order.
    """
    def tabs_repl(m: re.Match) -> str:
        body = m.group(1)
        out: list[str] = []
        for tm in _TAB_RE.finditer(body):
            title, content = tm.group(1), tm.group(2).strip()
            out.append(f'**{title}:**\n\n{content}')
        return "\n\n".join(out) if out else ""
    return _TABS_RE.sub(tabs_repl, text)


def transform_bare_video_urls(text: str) -> str:
    """Wrap bare GitBook-hosted video URLs in a friendly callout.

    Some pages reference the long `https://files.gitbook.com/...mp4` URL
    directly without the `{% embed %}` wrapper. Pandoc would auto-link
    these as ugly multi-line raw URLs in the PDF.
    """
    return _BARE_VIDEO_URL_RE.sub(lambda m: _video_callout(m.group(1)), text)


# GitBook's "mention" link: `[some-file.md](some-file.md "mention")` — a
# card-style cross-reference that renders as a styled tile on the website.
# In the PDF this just shows up as a raw filename link. The SUMMARY-driven
# TOC already provides cross-page navigation, so drop these entirely.
_MENTION_LINK_RE = re.compile(
    r'\[([^\]]+)\]\(([^)]+\.md(?:#[^)]*)?)\s+"mention"\)'
)


def transform_mention_links(text: str) -> str:
    """Strip GitBook 'mention' links — they look like raw filenames in print."""
    return _MENTION_LINK_RE.sub("", text)


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
    """Run all source-level transforms in the right order.

    Order matters: tabs first (they may contain hints), then hints (they may
    contain embeds), then content-refs and files, then embeds + bare video
    URLs, then image rewriting last (it converts paths to file:// URIs).
    """
    text = transform_tabs(text)
    text = transform_hints(text)
    text = transform_content_refs(text)
    text = transform_files(text)
    text = transform_embeds(text)
    text = transform_bare_video_urls(text)
    text = transform_mention_links(text)
    text = rewrite_images(text, source_md=source_md, ctx=ctx)
    return text


def build_cover_html(logo_uri: str | None) -> str:
    """Return raw HTML for the cover page.

    Goes into pandoc via --include-before-body so it appears before the
    auto-generated table of contents (a markdown-injected cover ends up
    AFTER the TOC, which isn't what we want).
    """
    logo_html = (
        f'<img class="cover-logo" src="{logo_uri}" alt="OcuTrap"/>'
        if logo_uri
        else ""
    )
    return f"""<div class="cover-page">
{logo_html}
<h1 class="cover-title">OcuTrap Knowledge Base</h1>
<p class="cover-subtitle">Complete user guide for the OcuTrap R2 and R1 smart wildlife traps.</p>
<p class="cover-contact">
Online docs: <strong>docs.ocutrap.com</strong><br/>
Support: <strong>support@ocutrap.com</strong>
</p>
</div>
"""


def assemble_document(entries: list[SummaryEntry], *, ctx: BuildContext) -> str:
    """Concatenate SUMMARY entries into one big markdown doc.

    Heading-level mapping:
      - chapter entries → H1 divider (forces page break via CSS)
      - pages under a chapter → original H1 demoted to H2, then by depth
      - pages with no chapter → original H1 stays H1

    Pages with `hidden: true` in their YAML frontmatter are skipped
    entirely — they exist on the GitBook site (sometimes as utility
    pages) but should not appear in the printable PDF.

    Note: the cover page is NOT included here — it's injected by
    render_pdf via pandoc's --include-before-body, so it lands before
    the auto-generated TOC.
    """
    # Build a per-chapter list of page parts so we can drop chapters that
    # end up empty (e.g. when every page in the chapter is pdf-excluded).
    pages_processed = 0
    pages_hidden = 0
    pages_pdf_excluded = 0

    chapters: list[tuple[str | None, list[str]]] = [(None, [])]  # (chapter_title, page_parts)

    for entry in entries:
        if entry.kind == "chapter":
            chapters.append((entry.title, []))
            continue
        if entry.path is None or not entry.path.exists():
            print(f"  WARN: page missing on disk: {entry.title} ({entry.path})")
            continue
        raw = entry.path.read_text(encoding="utf-8")
        body, flags = strip_frontmatter(raw)
        if flags.get("hidden"):
            pages_hidden += 1
            print(f"  skip (hidden:true): {entry.title} ({entry.path.name})")
            continue
        if flags.get("pdf-exclude"):
            pages_pdf_excluded += 1
            print(f"  skip (pdf-exclude:true): {entry.title} ({entry.path.name})")
            continue
        body = _preprocess_page(body, source_md=entry.path, ctx=ctx)
        # Shift: +1 if under any chapter, +depth for nesting
        shift = (1 if entry.chapter else 0) + entry.depth
        body = _shift_headings(body, shift)
        chapters[-1][1].append(body)
        pages_processed += 1

    parts: list[str] = []
    for chapter_title, page_parts in chapters:
        if not page_parts:
            if chapter_title:
                print(f"  skip empty chapter: {chapter_title}")
            continue
        if chapter_title:
            parts.append(f"# {chapter_title}\n")
        parts.extend(page_parts)

    ctx.pages_processed = pages_processed  # type: ignore[attr-defined]
    ctx.pages_hidden = pages_hidden  # type: ignore[attr-defined]
    ctx.pages_pdf_excluded = pages_pdf_excluded  # type: ignore[attr-defined]
    return "\n\n".join(parts) + "\n"


# ============================================================================
# Render: markdown → HTML → PDF
# ============================================================================

import subprocess

from weasyprint import HTML, CSS as WeasyCSS
from pypdf import PdfReader


def _markdown_to_html(markdown: str, *, cover_html: str | None = None) -> str:
    """Run pandoc to turn the assembled markdown into a standalone HTML doc.

    If `cover_html` is given, write it to a temp file and pass via
    --include-before-body so the cover lands BEFORE pandoc's auto-generated
    table of contents.
    """
    import tempfile

    cmd = [
        "pandoc",
        "--from=gfm+raw_html+pipe_tables+definition_lists",
        "--to=html5",
        "--standalone",
        "--toc",
        "--toc-depth=3",
        # No --metadata=title:... on purpose: the cover page (injected via
        # --include-before-body below) is the title. Adding a metadata title
        # here would also render a redundant <h1> above the TOC.
    ]

    cover_file = None
    try:
        if cover_html:
            cover_file = tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", delete=False, encoding="utf-8",
            )
            cover_file.write(cover_html)
            cover_file.close()
            cmd.append(f"--include-before-body={cover_file.name}")

        proc = subprocess.run(
            cmd, input=markdown, capture_output=True, text=True,
        )
    finally:
        if cover_file:
            Path(cover_file.name).unlink(missing_ok=True)

    if proc.returncode != 0:
        raise RuntimeError(f"pandoc failed:\n{proc.stderr}")
    return proc.stdout


def render_pdf(markdown: str, *, css_path: Path, output: Path,
               cover_html: str | None = None) -> int:
    """Render assembled markdown to a PDF. Returns page count."""
    html = _markdown_to_html(markdown, cover_html=cover_html)
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
DEFAULT_OUTPUT  = REPO_ROOT / ".gitbook" / "assets" / "OcuTrap_Knowledge_Base.pdf"
DEFAULT_CSS     = REPO_ROOT / "scripts" / "kb_pdf_style.css"
DEFAULT_CACHE   = REPO_ROOT / ".cache" / "kb-pdf"
DEFAULT_LOGO    = REPO_ROOT / ".gitbook" / "assets" / "OcuTrap_4228 × 1045_300dpi.png"


# Source-hash logic lives in source_hash.py so CI's verify step can run
# without pulling in this file's heavy imports (weasyprint, pillow, etc.).
from source_hash import write_sidecar as write_sources_sidecar  # noqa: E402


def _print_summary(ctx: BuildContext, output: Path, page_count: int) -> None:
    pages_processed = getattr(ctx, "pages_processed", 0)
    pages_hidden = getattr(ctx, "pages_hidden", 0)
    pages_pdf_excluded = getattr(ctx, "pages_pdf_excluded", 0)
    size_mb = output.stat().st_size / (1024 * 1024)
    print()
    print("─" * 60)
    print(f"Markdown files processed: {pages_processed} "
          f"({pages_hidden} hidden, {pages_pdf_excluded} pdf-excluded)")
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
    p.add_argument("--cover-logo", type=Path, default=DEFAULT_LOGO,
                   help="PNG/JPG used on the cover page; pass an empty path to omit.")
    p.add_argument("--min-pages", type=int, default=50)
    p.add_argument("--max-pages", type=int, default=1000)
    p.add_argument("--max-size-mb", type=int, default=100)
    args = p.parse_args(argv)

    ctx = BuildContext(cache_dir=args.cache_dir)
    entries = parse_summary(args.summary)
    print(f"Parsed {len(entries)} SUMMARY entries from {args.summary}")
    # Cover logo path may use Unicode whitespace variants in the on-disk
    # filename (e.g. U+200A hair space around ×); fall back to the same
    # space-normalized fuzzy lookup we use for body images.
    cover_logo = None
    if args.cover_logo:
        if args.cover_logo.exists():
            cover_logo = args.cover_logo
        else:
            cover_logo = resolve_image_path(args.cover_logo.name, args.cover_logo)
        if cover_logo is None:
            print(f"  WARN: cover logo not found at {args.cover_logo} — cover page will be text-only")
    assembled = assemble_document(entries, ctx=ctx)
    cover_html = build_cover_html(cover_logo.as_uri() if cover_logo else None)
    page_count = render_pdf(assembled, css_path=args.css, output=args.output,
                            cover_html=cover_html)
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

    sidecar = write_sources_sidecar(args.output, args.summary, Path(__file__), args.css)
    print(f"Wrote source-hash sidecar: {sidecar}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
