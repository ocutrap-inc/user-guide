# KB PDF Compiler Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a real markdown→PDF compiler that produces `pdf-docs/online/OcuTrap_Knowledge_Base.pdf` from the GitBook docs, replacing the 1,372-line hand-coded ReportLab document at `scripts/build_pdf.py` and the Word-derived `R1_Manual_v2.pdf`.

**Architecture:** Python orchestrator walks `SUMMARY.md`, preprocesses each linked markdown (GitBook syntax → CommonMark, image resolution, HEIC conversion, downscaling), concatenates with depth-based heading rewriting, then pipes through pandoc → HTML → WeasyPrint → PDF. GitHub Action auto-rebuilds on push to main.

**Tech Stack:** Python 3.12, pandoc (CLI), WeasyPrint (Python API), Pillow (image conversion), pypdf (page count validation), requests (external image fetch), pytest (tests).

**Spec:** `pdf-docs/specs/2026-05-04-kb-pdf-compiler-design.md` (PR #3).

---

## File Structure

| Path | Responsibility |
| --- | --- |
| `scripts/build_kb_pdf.py` | Single-file orchestrator. Sections (SUMMARY parser, GitBook transforms, image pipeline, assembler, render, CLI) marked with banner comments for navigability. |
| `scripts/kb_pdf_style.css` | CSS Paged Media stylesheet — `@page` rules, hint/figure/table styling, image sizing. Loaded by WeasyPrint. |
| `tests/test_build_kb_pdf.py` | pytest suite — pure-transform unit tests + one end-to-end smoke test against `tests/fixtures/mini-summary/`. |
| `tests/fixtures/mini-summary/` | Tiny fixture: SUMMARY.md + 3 markdown files + 1 image, exercises every preprocessing rule. |
| `requirements-dev.txt` | `pytest`, `weasyprint`, `pillow`, `pypdf`, `requests`, `pillow-heif`. |
| `pytest.ini` | `rootdir` + test discovery. |
| `.github/workflows/build-kb-pdf.yml` | CI: triggers on docs changes, runs the script, commits regenerated PDF. |
| `.gitignore` (modify) | Add `.cache/` and `.DS_Store`. |
| `pdf-docs/README.md` (modify) | Update PDF rows to reflect the new compiler. |
| `pdf-docs/MAINTENANCE.md` (modify) | Close items resolved by the compiler; remove arch-debt section. |

**Files deleted in cleanup task:** `scripts/build_pdf.py`, `pdf-docs/online/R1_Manual_v2.pdf`, `scripts/build_manual_pdf.sh`.

---

## Task 1: Test harness setup

**Files:**
- Create: `requirements-dev.txt`
- Create: `pytest.ini`
- Create: `tests/__init__.py`
- Create: `tests/test_smoke.py`
- Modify: `.gitignore`

- [ ] **Step 1: Create requirements-dev.txt**

```
pytest>=8.0
weasyprint>=62.0
pillow>=10.0
pillow-heif>=0.18.0
pypdf>=4.0
requests>=2.31
```

- [ ] **Step 2: Create pytest.ini**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short
```

- [ ] **Step 3: Create tests/__init__.py** (empty file)

- [ ] **Step 4: Add a smoke test that proves the harness works**

`tests/test_smoke.py`:

```python
def test_pytest_runs():
    assert 1 + 1 == 2
```

- [ ] **Step 5: Update .gitignore**

Append:

```
.cache/
.DS_Store
__pycache__/
*.pyc
.pytest_cache/
```

(If `.gitignore` does not exist, create it with this content.)

- [ ] **Step 6: Install deps and run the smoke test**

```bash
pip install -r requirements-dev.txt
pytest tests/test_smoke.py
```

Expected: `1 passed`.

- [ ] **Step 7: Commit**

```bash
git add requirements-dev.txt pytest.ini tests/__init__.py tests/test_smoke.py .gitignore
git commit -m "test: add pytest harness for KB PDF compiler"
```

---

## Task 2: SUMMARY.md parser

Parses GitBook's `SUMMARY.md` into an ordered sequence of entries, each tagged with depth and the chapter group it belongs to. This drives document order and heading-level rewriting downstream.

**Files:**
- Create: `scripts/build_kb_pdf.py`
- Create: `tests/test_build_kb_pdf.py`
- Create: `tests/fixtures/mini-summary/SUMMARY.md`

- [ ] **Step 1: Write the failing test**

`tests/fixtures/mini-summary/SUMMARY.md`:

```markdown
# Table of contents

* [Welcome](README.md)

## Getting Started

* [Introduction](getting-started/introduction.md)
* [App](getting-started/app/README.md)
  * [Settings](getting-started/app/settings.md)

## FAQs

* [Common Questions](faqs/common-questions.md)
```

`tests/test_build_kb_pdf.py`:

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from build_kb_pdf import parse_summary, SummaryEntry

FIXTURE = Path(__file__).parent / "fixtures" / "mini-summary"


def test_parse_summary_extracts_chapters_and_pages():
    entries = parse_summary(FIXTURE / "SUMMARY.md")

    assert entries == [
        SummaryEntry(kind="page",    depth=0, title="Welcome",          path=FIXTURE / "README.md",                         chapter=None),
        SummaryEntry(kind="chapter", depth=0, title="Getting Started",  path=None,                                          chapter="Getting Started"),
        SummaryEntry(kind="page",    depth=0, title="Introduction",     path=FIXTURE / "getting-started/introduction.md",   chapter="Getting Started"),
        SummaryEntry(kind="page",    depth=0, title="App",              path=FIXTURE / "getting-started/app/README.md",     chapter="Getting Started"),
        SummaryEntry(kind="page",    depth=1, title="Settings",         path=FIXTURE / "getting-started/app/settings.md",   chapter="Getting Started"),
        SummaryEntry(kind="chapter", depth=0, title="FAQs",             path=None,                                          chapter="FAQs"),
        SummaryEntry(kind="page",    depth=0, title="Common Questions", path=FIXTURE / "faqs/common-questions.md",          chapter="FAQs"),
    ]
```

- [ ] **Step 2: Run the test and verify it fails**

```bash
pytest tests/test_build_kb_pdf.py::test_parse_summary_extracts_chapters_and_pages -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'build_kb_pdf'`.

- [ ] **Step 3: Write the minimal parser**

Create `scripts/build_kb_pdf.py`:

```python
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

    for line in summary_path.read_text().splitlines():
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
```

- [ ] **Step 4: Run the test and verify it passes**

```bash
pytest tests/test_build_kb_pdf.py::test_parse_summary_extracts_chapters_and_pages -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_kb_pdf.py tests/test_build_kb_pdf.py tests/fixtures/mini-summary/SUMMARY.md
git commit -m "feat(kb-pdf): SUMMARY.md parser with chapter tracking"
```

---

## Task 3: GitBook hint and embed transforms

GitBook's `{% hint %}` and `{% embed %}` syntax aren't standard CommonMark and pandoc can't parse them. Replace them before pandoc sees the document.

**Files:**
- Modify: `scripts/build_kb_pdf.py`
- Modify: `tests/test_build_kb_pdf.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_build_kb_pdf.py`:

```python
from build_kb_pdf import transform_hints, transform_embeds


def test_transform_hints_info():
    src = """before
{% hint style="info" %}
Heads up.
{% endhint %}
after"""
    expected = """before
<div class="hint hint-info">

Heads up.

</div>
after"""
    assert transform_hints(src) == expected


def test_transform_hints_danger_and_warning():
    for style in ("danger", "warning"):
        src = f'{{% hint style="{style}" %}}\nX\n{{% endhint %}}'
        out = transform_hints(src)
        assert f'class="hint hint-{style}"' in out
        assert "X" in out


def test_transform_hints_unknown_style_falls_back_to_info():
    src = '{% hint style="weird" %}\nX\n{% endhint %}'
    assert 'class="hint hint-info"' in transform_hints(src)


def test_transform_embeds_replaces_with_link():
    src = '{% embed url="https://ocutrap.statuspage.io/" %}'
    assert transform_embeds(src) == "[https://ocutrap.statuspage.io/](https://ocutrap.statuspage.io/)"


def test_transform_embeds_handles_multiple():
    src = '{% embed url="https://a" %}\nx\n{% embed url="https://b" %}'
    out = transform_embeds(src)
    assert "[https://a](https://a)" in out
    assert "[https://b](https://b)" in out
```

- [ ] **Step 2: Run tests and verify they fail**

```bash
pytest tests/test_build_kb_pdf.py -k "hint or embed" -v
```

Expected: FAIL with `ImportError`.

- [ ] **Step 3: Add the transforms**

Append to `scripts/build_kb_pdf.py`:

```python
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
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
pytest tests/test_build_kb_pdf.py -k "hint or embed" -v
```

Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_kb_pdf.py tests/test_build_kb_pdf.py
git commit -m "feat(kb-pdf): GitBook hint and embed transforms"
```

---

## Task 4: Image path normalization

GitBook image references come in several shapes — `<>`-wrapped paths, filenames with literal spaces, Unicode space variants. Normalize them to a real `Path` (or `None` if missing).

**Files:**
- Modify: `scripts/build_kb_pdf.py`
- Modify: `tests/test_build_kb_pdf.py`
- Create: `tests/fixtures/images/normal.png`
- Create: `tests/fixtures/images/has spaces.png`

- [ ] **Step 1: Create fixture images** (any small valid PNG)

```bash
python3 -c "
from PIL import Image
from pathlib import Path
d = Path('tests/fixtures/images')
d.mkdir(parents=True, exist_ok=True)
Image.new('RGB', (10, 10), 'red').save(d / 'normal.png')
Image.new('RGB', (10, 10), 'blue').save(d / 'has spaces.png')
"
```

- [ ] **Step 2: Write failing tests**

Append to `tests/test_build_kb_pdf.py`:

```python
from build_kb_pdf import resolve_image_path

IMAGES = Path(__file__).parent / "fixtures" / "images"


def test_resolve_image_path_normal():
    src = IMAGES.parent / "dummy.md"
    assert resolve_image_path("images/normal.png", src) == IMAGES / "normal.png"


def test_resolve_image_path_unwraps_angle_brackets():
    src = IMAGES.parent / "dummy.md"
    assert resolve_image_path("<images/has spaces.png>", src) == IMAGES / "has spaces.png"


def test_resolve_image_path_handles_unicode_space_variant(tmp_path):
    """The on-disk filename uses U+00A0 (NBSP) but the markdown uses a regular space."""
    target = tmp_path / "weird name.png"
    target.write_bytes(b"\x89PNG\r\n\x1a\n")
    src = tmp_path / "doc.md"
    src.write_text("")
    assert resolve_image_path("weird name.png", src) == target


def test_resolve_image_path_returns_none_when_missing(tmp_path):
    src = tmp_path / "doc.md"
    src.write_text("")
    assert resolve_image_path("nope.png", src) is None
```

- [ ] **Step 3: Run tests and verify they fail**

```bash
pytest tests/test_build_kb_pdf.py -k resolve_image_path -v
```

Expected: 4 FAIL with `ImportError`.

- [ ] **Step 4: Implement**

Append to `scripts/build_kb_pdf.py`:

```python
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
```

- [ ] **Step 5: Run tests and verify they pass**

```bash
pytest tests/test_build_kb_pdf.py -k resolve_image_path -v
```

Expected: 4 passed.

- [ ] **Step 6: Commit**

```bash
git add scripts/build_kb_pdf.py tests/test_build_kb_pdf.py tests/fixtures/images/
git commit -m "feat(kb-pdf): image path resolution with Unicode space handling"
```

---

## Task 5: Image conversion and downscaling pipeline

HEIC images need conversion to JPEG. Anything wider than 1600px gets downscaled. GIFs collapse to first frame. Cached output keyed by source mtime + transform parameters.

**Files:**
- Modify: `scripts/build_kb_pdf.py`
- Modify: `tests/test_build_kb_pdf.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_build_kb_pdf.py`:

```python
from build_kb_pdf import process_image, MAX_IMAGE_WIDTH


def _make_png(path: Path, w: int, h: int, color="red") -> Path:
    from PIL import Image
    Image.new("RGB", (w, h), color).save(path)
    return path


def test_process_image_passthrough_when_small_and_supported(tmp_path):
    src = _make_png(tmp_path / "small.png", 800, 600)
    out = process_image(src, cache_dir=tmp_path / ".cache")
    assert out == src  # no transform needed


def test_process_image_downscales_when_too_wide(tmp_path):
    from PIL import Image
    src = _make_png(tmp_path / "big.png", 4000, 2000)
    out = process_image(src, cache_dir=tmp_path / ".cache")
    assert out != src
    assert out.parent == tmp_path / ".cache"
    with Image.open(out) as im:
        assert im.width == MAX_IMAGE_WIDTH


def test_process_image_converts_heic_to_jpeg(tmp_path):
    """We can't easily synthesize a HEIC file in tests, so we use an extension
    swap on a JPEG and patch pillow-heif registration. Use a real fixture if
    available; otherwise this test is skipped."""
    import pytest
    try:
        from pillow_heif import register_heif_opener  # noqa
    except ImportError:
        pytest.skip("pillow-heif not installed")

    # Use a real HEIC fixture if present; otherwise skip
    fixture = Path(__file__).parent / "fixtures" / "images" / "sample.heic"
    if not fixture.exists():
        pytest.skip("no sample.heic fixture")
    out = process_image(fixture, cache_dir=tmp_path / ".cache")
    assert out.suffix == ".jpg"
    assert out.parent == tmp_path / ".cache"


def test_process_image_gif_first_frame(tmp_path):
    from PIL import Image
    gif = tmp_path / "anim.gif"
    Image.new("P", (100, 100), 0).save(
        gif, save_all=True,
        append_images=[Image.new("P", (100, 100), 128)],
        duration=100, loop=0,
    )
    out = process_image(gif, cache_dir=tmp_path / ".cache")
    assert out.suffix == ".png"
    with Image.open(out) as im:
        assert getattr(im, "n_frames", 1) == 1


def test_process_image_caches_repeated_calls(tmp_path):
    src = _make_png(tmp_path / "big.png", 4000, 2000)
    cache = tmp_path / ".cache"
    out1 = process_image(src, cache_dir=cache)
    mtime1 = out1.stat().st_mtime
    out2 = process_image(src, cache_dir=cache)
    assert out1 == out2
    assert out2.stat().st_mtime == mtime1  # not regenerated
```

- [ ] **Step 2: Run tests and verify they fail**

```bash
pytest tests/test_build_kb_pdf.py -k process_image -v
```

Expected: ImportError on all (or skip on HEIC if no fixture).

- [ ] **Step 3: Implement**

Append to `scripts/build_kb_pdf.py`:

```python
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
            im.save(out, **save_kwargs)
    return out
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
pytest tests/test_build_kb_pdf.py -k process_image -v
```

Expected: 4 passed, 1 skipped (HEIC if no fixture).

- [ ] **Step 5: Commit**

```bash
git add scripts/build_kb_pdf.py tests/test_build_kb_pdf.py
git commit -m "feat(kb-pdf): image conversion and downscaling pipeline"
```

---

## Task 6: External image fetcher

Some markdown pages reference Google docsz / Unsplash URLs. Download once, cache by URL hash.

**Files:**
- Modify: `scripts/build_kb_pdf.py`
- Modify: `tests/test_build_kb_pdf.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_build_kb_pdf.py`:

```python
from unittest.mock import patch, MagicMock
from build_kb_pdf import fetch_external


def test_fetch_external_downloads_and_caches(tmp_path):
    cache = tmp_path / ".cache"
    fake_response = MagicMock()
    fake_response.content = b"\x89PNG\r\n\x1a\n" + b"x" * 100
    fake_response.headers = {"Content-Type": "image/png"}
    fake_response.raise_for_status = MagicMock()
    with patch("build_kb_pdf.requests.get", return_value=fake_response) as get:
        out1 = fetch_external("https://example.com/img.png", cache_dir=cache)
        out2 = fetch_external("https://example.com/img.png", cache_dir=cache)
    assert out1 is not None
    assert out1 == out2  # same cache hit
    assert out1.read_bytes().startswith(b"\x89PNG")
    assert get.call_count == 1  # second call hit cache


def test_fetch_external_returns_none_on_failure(tmp_path):
    cache = tmp_path / ".cache"
    with patch("build_kb_pdf.requests.get", side_effect=Exception("network down")):
        assert fetch_external("https://example.com/x.png", cache_dir=cache) is None
```

- [ ] **Step 2: Run tests and verify they fail**

```bash
pytest tests/test_build_kb_pdf.py -k fetch_external -v
```

Expected: ImportError.

- [ ] **Step 3: Implement**

Append to `scripts/build_kb_pdf.py`:

```python
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
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
pytest tests/test_build_kb_pdf.py -k fetch_external -v
```

Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_kb_pdf.py tests/test_build_kb_pdf.py
git commit -m "feat(kb-pdf): external image fetcher with caching"
```

---

## Task 7: Markdown image-reference rewriting

Walks every `![](path)` and `<img src="path">` in a markdown file, runs each through the resolver / fetcher / processor, and rewrites the path to an absolute `file://` URL pointing at the cached/converted file.

**Files:**
- Modify: `scripts/build_kb_pdf.py`
- Modify: `tests/test_build_kb_pdf.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/test_build_kb_pdf.py`:

```python
from build_kb_pdf import rewrite_images, BuildContext


def test_rewrite_images_handles_markdown_and_html(tmp_path):
    img = _make_png(tmp_path / "pic.png", 100, 100)
    src = tmp_path / "doc.md"
    md = '![alt](pic.png)\n<figure><img src="pic.png" alt=""></figure>'
    ctx = BuildContext(cache_dir=tmp_path / ".cache")
    out = rewrite_images(md, source_md=src, ctx=ctx)
    file_url = (tmp_path / "pic.png").as_uri()
    assert f"![alt]({file_url})" in out
    assert f'<img src="{file_url}"' in out


def test_rewrite_images_strips_when_missing(tmp_path):
    src = tmp_path / "doc.md"
    src.parent.mkdir(parents=True, exist_ok=True)
    md = "before\n![](nope.png)\nafter\n"
    ctx = BuildContext(cache_dir=tmp_path / ".cache")
    out = rewrite_images(md, source_md=src, ctx=ctx)
    assert "nope.png" not in out
    assert "before" in out and "after" in out


def test_rewrite_images_external_url_passthrough_when_fetch_fails(tmp_path, monkeypatch):
    monkeypatch.setattr("build_kb_pdf.fetch_external", lambda url, cache_dir: None)
    src = tmp_path / "doc.md"
    md = "![](https://example.com/missing.png)"
    ctx = BuildContext(cache_dir=tmp_path / ".cache")
    out = rewrite_images(md, source_md=src, ctx=ctx)
    assert out == ""  # the only image stripped, leaving an empty doc
```

- [ ] **Step 2: Run tests and verify they fail**

```bash
pytest tests/test_build_kb_pdf.py -k rewrite_images -v
```

Expected: ImportError.

- [ ] **Step 3: Implement**

Append to `scripts/build_kb_pdf.py`:

```python
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
            return ""
        ctx.images_embedded += 1
        return f"![{alt}]({out.as_uri()})"

    def html_repl(m: re.Match) -> str:
        before, raw, after = m.group(1), m.group(2), m.group(3)
        out = _resolve_or_fetch(raw, source_md, ctx)
        if out is None:
            ctx.images_skipped += 1
            return ""
        ctx.images_embedded += 1
        return f'<img {before}src="{out.as_uri()}"{after}/>'

    text = _MD_IMG_RE.sub(md_repl, text)
    text = _HTML_IMG_RE.sub(html_repl, text)
    # Tidy: collapse stray empty lines left by stripped images
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
pytest tests/test_build_kb_pdf.py -k rewrite_images -v
```

Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_kb_pdf.py tests/test_build_kb_pdf.py
git commit -m "feat(kb-pdf): markdown image rewriting with stats tracking"
```

---

## Task 8: Document assembly with heading rewrite

Walks the parsed SUMMARY entries, applies all preprocessing, shifts each file's headings down by its depth, and emits one big assembled markdown document.

**Files:**
- Modify: `scripts/build_kb_pdf.py`
- Modify: `tests/test_build_kb_pdf.py`
- Create: `tests/fixtures/mini-summary/README.md`
- Create: `tests/fixtures/mini-summary/getting-started/introduction.md`
- Create: `tests/fixtures/mini-summary/getting-started/app/README.md`
- Create: `tests/fixtures/mini-summary/getting-started/app/settings.md`
- Create: `tests/fixtures/mini-summary/faqs/common-questions.md`

- [ ] **Step 1: Create fixture markdown files**

`tests/fixtures/mini-summary/README.md`:

```markdown
# Welcome

Welcome to the OcuTrap docs.
```

`tests/fixtures/mini-summary/getting-started/introduction.md`:

```markdown
# Introduction

What is OcuTrap.

## Background

Some background.
```

`tests/fixtures/mini-summary/getting-started/app/README.md`:

```markdown
# App

The OcuTrap app.
```

`tests/fixtures/mini-summary/getting-started/app/settings.md`:

```markdown
# Settings

{% hint style="info" %}
Read carefully.
{% endhint %}
```

`tests/fixtures/mini-summary/faqs/common-questions.md`:

```markdown
# Common Questions

Q&A.
```

- [ ] **Step 2: Write failing test**

Append to `tests/test_build_kb_pdf.py`:

```python
from build_kb_pdf import assemble_document


def test_assemble_document_orders_and_shifts_headings(tmp_path):
    ctx = BuildContext(cache_dir=tmp_path / ".cache")
    entries = parse_summary(FIXTURE / "SUMMARY.md")
    out = assemble_document(entries, ctx=ctx)

    # Chapter dividers appear in document order
    assert out.index("# Getting Started") < out.index("# FAQs")
    # Pre-chapter pages keep H1
    assert "# Welcome" in out
    # Pages under a chapter get demoted: their H1 becomes H2, etc.
    assert "## Introduction" in out
    assert "### Background" in out
    # Nested-bullet pages get further demotion
    assert "### Settings" in out
    # GitBook syntax inside a page is transformed before assembly
    assert 'class="hint hint-info"' in out
```

- [ ] **Step 3: Run test and verify it fails**

```bash
pytest tests/test_build_kb_pdf.py -k assemble_document -v
```

Expected: FAIL with ImportError.

- [ ] **Step 4: Implement**

Append to `scripts/build_kb_pdf.py`:

```python
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
        body = entry.path.read_text()
        body = _preprocess_page(body, source_md=entry.path, ctx=ctx)
        # Shift: +1 if under any chapter, +depth for nesting
        shift = (1 if entry.chapter else 0) + entry.depth
        body = _shift_headings(body, shift)
        parts.append(body)
        pages_processed += 1
    ctx.pages_processed = pages_processed  # type: ignore[attr-defined]
    return "\n\n".join(parts) + "\n"
```

(`pages_processed` is added dynamically — that's fine for now; we'll formalize Stats in Task 10.)

- [ ] **Step 5: Run test and verify it passes**

```bash
pytest tests/test_build_kb_pdf.py -k assemble_document -v
```

Expected: 1 passed.

- [ ] **Step 6: Commit**

```bash
git add scripts/build_kb_pdf.py tests/test_build_kb_pdf.py tests/fixtures/mini-summary/
git commit -m "feat(kb-pdf): document assembly with heading shift"
```

---

## Task 9: Pandoc + WeasyPrint render pipeline

Pipes the assembled markdown through pandoc to HTML, then through WeasyPrint to PDF. Returns page count.

**Files:**
- Modify: `scripts/build_kb_pdf.py`
- Modify: `tests/test_build_kb_pdf.py`
- Create: `scripts/kb_pdf_style.css`

- [ ] **Step 1: Create the stylesheet**

`scripts/kb_pdf_style.css`:

```css
@page {
  size: letter portrait;
  margin: 0.75in;
  @bottom-center { content: counter(page); font-size: 9pt; color: #666; }
  @top-right    { content: string(chapter-title); font-size: 9pt; color: #666; }
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 10.5pt;
  line-height: 1.45;
  color: #1f2328;
}

h1 {
  string-set: chapter-title content();
  page-break-before: always;
  font-size: 22pt;
  margin: 0 0 0.5em 0;
  color: #0d1117;
  border-bottom: 2px solid #1f2328;
  padding-bottom: 0.2em;
}
h2 { font-size: 16pt; margin-top: 1.2em; page-break-after: avoid; }
h3 { font-size: 13pt; margin-top: 1em;  page-break-after: avoid; }
h4 { font-size: 11pt; margin-top: 0.8em; page-break-after: avoid; }

p, ul, ol, table, pre, blockquote { margin: 0.6em 0; }

img {
  max-width: 100%;
  max-height: 8in;
  page-break-inside: avoid;
  display: block;
  margin: 0.6em auto;
}

.hint {
  padding: 0.5em 1em;
  border-left: 4px solid;
  margin: 1em 0;
  page-break-inside: avoid;
}
.hint-info    { border-color: #0969da; background: #ddf4ff; }
.hint-danger  { border-color: #cf222e; background: #ffebe9; }
.hint-warning { border-color: #9a6700; background: #fff8c5; }
.hint-success { border-color: #1a7f37; background: #dafbe1; }

table {
  border-collapse: collapse;
  page-break-inside: avoid;
  width: 100%;
  font-size: 9.5pt;
}
th, td { border: 1px solid #d0d7de; padding: 0.4em 0.6em; vertical-align: top; }
th { background: #f6f8fa; font-weight: 600; text-align: left; }

code {
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.9em;
  background: #f6f8fa;
  padding: 0.1em 0.3em;
  border-radius: 3px;
}
pre {
  background: #f6f8fa;
  padding: 0.8em 1em;
  border-radius: 4px;
  overflow-x: auto;
  page-break-inside: avoid;
  font-size: 9pt;
}
pre code { background: transparent; padding: 0; }

nav[role="doc-toc"] ol { list-style: none; padding-left: 1em; }
nav[role="doc-toc"] a { text-decoration: none; color: #1f2328; }
nav[role="doc-toc"] a::after { content: leader('.') target-counter(attr(href), page); }
```

- [ ] **Step 2: Write failing test**

Append to `tests/test_build_kb_pdf.py`:

```python
from build_kb_pdf import render_pdf

CSS_PATH = Path(__file__).parent.parent / "scripts" / "kb_pdf_style.css"


def test_render_pdf_produces_a_pdf(tmp_path):
    md = "# Hello\n\nWorld.\n\n# Chapter Two\n\nMore."
    out = tmp_path / "out.pdf"
    pages = render_pdf(md, css_path=CSS_PATH, output=out)
    assert out.exists() and out.stat().st_size > 0
    assert pages >= 2  # one page per H1 due to page-break-before
```

- [ ] **Step 3: Run test and verify it fails**

```bash
pytest tests/test_build_kb_pdf.py -k render_pdf -v
```

Expected: FAIL with ImportError.

- [ ] **Step 4: Implement**

Append to `scripts/build_kb_pdf.py`:

```python
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
```

- [ ] **Step 5: Run test and verify it passes**

```bash
pytest tests/test_build_kb_pdf.py -k render_pdf -v
```

Expected: 1 passed. (Requires `pandoc` on PATH; install via `brew install pandoc` if missing.)

- [ ] **Step 6: Commit**

```bash
git add scripts/build_kb_pdf.py scripts/kb_pdf_style.css tests/test_build_kb_pdf.py
git commit -m "feat(kb-pdf): pandoc + WeasyPrint render pipeline + print stylesheet"
```

---

## Task 10: CLI orchestrator with summary stats and thresholds

Wire everything together: `python3 scripts/build_kb_pdf.py` reads the real `SUMMARY.md`, builds the assembled doc, renders the PDF, prints a summary, and hard-fails on out-of-range thresholds.

**Files:**
- Modify: `scripts/build_kb_pdf.py`
- Modify: `tests/test_build_kb_pdf.py`

- [ ] **Step 1: Write failing end-to-end smoke test**

Append to `tests/test_build_kb_pdf.py`:

```python
import subprocess as _sp


def test_cli_end_to_end_against_fixture(tmp_path):
    """Run the script as a CLI against the mini-summary fixture and verify it
    produces a PDF and prints a sane summary."""
    output = tmp_path / "fixture.pdf"
    proc = _sp.run(
        ["python3", str(Path(__file__).parent.parent / "scripts" / "build_kb_pdf.py"),
         "--summary", str(FIXTURE / "SUMMARY.md"),
         "--output", str(output),
         "--css", str(CSS_PATH),
         "--cache-dir", str(tmp_path / ".cache"),
         "--min-pages", "1",
         "--max-pages", "100"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"stderr:\n{proc.stderr}\nstdout:\n{proc.stdout}"
    assert output.exists() and output.stat().st_size > 0
    assert "Markdown files processed:" in proc.stdout
    assert "Final PDF:" in proc.stdout


def test_cli_fails_when_below_min_pages(tmp_path):
    output = tmp_path / "fixture.pdf"
    proc = _sp.run(
        ["python3", str(Path(__file__).parent.parent / "scripts" / "build_kb_pdf.py"),
         "--summary", str(FIXTURE / "SUMMARY.md"),
         "--output", str(output),
         "--css", str(CSS_PATH),
         "--cache-dir", str(tmp_path / ".cache"),
         "--min-pages", "9999",
         "--max-pages", "10000"],
        capture_output=True, text=True,
    )
    assert proc.returncode != 0
    assert "page count" in proc.stderr.lower()
```

- [ ] **Step 2: Run tests and verify they fail**

```bash
pytest tests/test_build_kb_pdf.py -k cli_ -v
```

Expected: FAIL — script has no CLI yet.

- [ ] **Step 3: Implement CLI**

Append to `scripts/build_kb_pdf.py`:

```python
# ============================================================================
# CLI
# ============================================================================

import argparse
import sys

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
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
pytest tests/test_build_kb_pdf.py -k cli_ -v
```

Expected: 2 passed.

- [ ] **Step 5: Run the full test suite**

```bash
pytest -v
```

Expected: All previous tests still pass.

- [ ] **Step 6: Commit**

```bash
git add scripts/build_kb_pdf.py tests/test_build_kb_pdf.py
git commit -m "feat(kb-pdf): CLI orchestrator with summary stats and thresholds"
```

---

## Task 11: First production run + commit the generated PDF

Now that the pipeline is wired end-to-end, run it against the real `SUMMARY.md` and commit the regenerated PDF.

**Files:**
- Generated: `pdf-docs/online/OcuTrap_Knowledge_Base.pdf` (regenerated)

- [ ] **Step 1: Ensure pandoc is available**

```bash
which pandoc || brew install pandoc
```

Expected: a path is printed (or pandoc gets installed).

- [ ] **Step 2: Run the script against the real docs**

```bash
python3 scripts/build_kb_pdf.py
```

Expected output ends with a summary like:

```
────────────────────────────────────────────────────────────
Markdown files processed: 79
Images embedded:          ~300 (X converted, Y downloaded externally, Z skipped)
Final PDF: ~25 MB, ~280 pages
Output:    /Users/.../pdf-docs/online/OcuTrap_Knowledge_Base.pdf
────────────────────────────────────────────────────────────
```

If page count or size is wildly off, the script will exit non-zero and clean up the output. Investigate the script logs for skipped images / failed fetches.

- [ ] **Step 3: Open the PDF and spot-check it**

```bash
open pdf-docs/online/OcuTrap_Knowledge_Base.pdf
```

Verify:
- Title page renders.
- Auto-generated TOC appears with page numbers.
- Each `## Chapter` from `SUMMARY.md` starts on its own page.
- Monitoring Mode page (the recently-merged one) appears in the App section with its firmware version table.
- Image-heavy pages render without the images breaking across pages awkwardly.

If any of those fail: this is a real defect — either fix the script, the CSS, or open a follow-up. Do not accept a broken PDF.

- [ ] **Step 4: Commit the regenerated PDF**

```bash
git add pdf-docs/online/OcuTrap_Knowledge_Base.pdf
git commit -m "chore(kb-pdf): regenerate from current docs

First production run of the new compiler. Includes Monitoring Mode page,
v675+ heartbeat notes, lightning-bolt request, and v700-v706 firmware notes
that were missing from the previous hand-coded version."
```

---

## Task 12: GitHub Action for auto-rebuild

Triggers on docs changes, runs the script, commits the regenerated PDF back to main.

**Files:**
- Create: `.github/workflows/build-kb-pdf.yml`

- [ ] **Step 1: Create the workflow**

```yaml
name: build-kb-pdf

on:
  push:
    branches: [main]
    paths:
      - '**/*.md'
      - '.gitbook/assets/**'
      - 'scripts/build_kb_pdf.py'
      - 'scripts/kb_pdf_style.css'
      - '.github/workflows/build-kb-pdf.yml'
      - 'requirements-dev.txt'
  workflow_dispatch:

concurrency:
  group: build-kb-pdf
  cancel-in-progress: true

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
      - name: Install system deps
        run: |
          sudo apt-get update
          sudo apt-get install -y pandoc libpango-1.0-0 libpangoft2-1.0-0
      - name: Install Python deps
        run: pip install -r requirements-dev.txt
      - uses: actions/cache@v4
        with:
          path: .cache/kb-pdf
          key: kb-pdf-${{ hashFiles('SUMMARY.md', '.gitbook/assets/**', 'scripts/build_kb_pdf.py') }}
          restore-keys: |
            kb-pdf-
      - name: Build PDF
        run: python3 scripts/build_kb_pdf.py
      - name: Commit if PDF changed
        run: |
          if ! git diff --quiet -- pdf-docs/online/OcuTrap_Knowledge_Base.pdf; then
            git config user.name 'github-actions[bot]'
            git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
            git add pdf-docs/online/OcuTrap_Knowledge_Base.pdf
            git commit -m "chore(kb-pdf): regenerate from docs [skip ci]"
            git push
          else
            echo "PDF unchanged, skipping commit."
          fi
```

- [ ] **Step 2: Lint the YAML locally**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/build-kb-pdf.yml'))"
```

Expected: no output (valid YAML).

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/build-kb-pdf.yml
git commit -m "ci(kb-pdf): auto-rebuild PDF on docs changes"
```

(The workflow won't run until this branch is merged to main.)

---

## Task 13: Cleanup — delete superseded artifacts and update READMEs

The new compiler replaces three pieces. Clean them up now that the replacement works.

**Files:**
- Delete: `scripts/build_pdf.py`
- Delete: `scripts/build_manual_pdf.sh`
- Delete: `pdf-docs/online/R1_Manual_v2.pdf`
- Modify: `pdf-docs/README.md`
- Modify: `pdf-docs/MAINTENANCE.md`

- [ ] **Step 1: Delete superseded files**

```bash
git rm scripts/build_pdf.py scripts/build_manual_pdf.sh pdf-docs/online/R1_Manual_v2.pdf
```

- [ ] **Step 2: Update `pdf-docs/README.md`**

Replace the `online/` section with:

```markdown
## `online/` — Downloadable only

| File | Purpose | Source of truth |
| --- | --- | --- |
| `R1_Operation_Cheat_Sheet.pdf` | One-page letter-size reference for users unfamiliar with the device: system LEDs, buttons, device states, safety. Hand-coded ReportLab document. | `scripts/build_cheat_sheet.py` |
| `OcuTrap_Knowledge_Base.pdf` | Print-quality PDF rendering of the full GitBook docs. **Auto-generated** by `scripts/build_kb_pdf.py` and rebuilt on every push to `main` via `.github/workflows/build-kb-pdf.yml`. To rebuild locally: `python3 scripts/build_kb_pdf.py`. | The GitBook markdown (driven by `SUMMARY.md`) |
```

Update the "Rebuilding" section by replacing the manual / KB lines with:

```bash
# Full Knowledge Base PDF (auto-rebuilt by CI; manual rebuild only when iterating)
pip install -r requirements-dev.txt
python3 scripts/build_kb_pdf.py
```

Drop the `brew install pandoc` / `./scripts/build_manual_pdf.sh` block — that toolchain is gone.

- [ ] **Step 3: Update `pdf-docs/MAINTENANCE.md`**

Close the four "Pending updates" items the new compiler resolves (Monitoring Mode page, lightning-bolt request, v675+ heartbeat, v700–v706 notes) by adding a checkmark and a "Resolved by new compiler — auto-included as of <commit>" note.

Remove the entire **"Architectural debt"** section. The debt is paid.

Add a short note at the top under the header:

```markdown
**As of 2026-05-04**, `OcuTrap_Knowledge_Base.pdf` is auto-generated from
`SUMMARY.md` by `scripts/build_kb_pdf.py` and rebuilt on every push to `main`
via GitHub Actions. The "Pending updates" tracker now only applies to the
hand-coded scripts (`build_quick_start.py`, `build_cheat_sheet.py`).
```

- [ ] **Step 4: Run tests one more time**

```bash
pytest -v
```

Expected: all green.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_pdf.py scripts/build_manual_pdf.sh pdf-docs/online/R1_Manual_v2.pdf pdf-docs/README.md pdf-docs/MAINTENANCE.md
git commit -m "chore(kb-pdf): retire build_pdf.py + R1_Manual_v2.pdf

The new compiler at scripts/build_kb_pdf.py replaces the parallel
hand-coded ReportLab document and the Word-derived manual. Updates the
PDF README and closes the resolved drift items in MAINTENANCE.md."
```

---

## Self-Review

**Spec coverage check:**
- ✅ Pipeline (markdown → preprocess → pandoc → WeasyPrint → PDF) — Tasks 7-10
- ✅ SUMMARY-driven document order — Task 2 + Task 8
- ✅ GitBook hint / embed transforms — Task 3
- ✅ Image path resolution with Unicode space handling — Task 4
- ✅ HEIC → JPEG, GIF first-frame, downscaling — Task 5
- ✅ External URL fetcher with caching — Task 6
- ✅ Heading-level rewrite — Task 8
- ✅ CSS Paged Media stylesheet — Task 9
- ✅ Hard-fail thresholds — Task 10
- ✅ Summary stats — Task 10
- ✅ GitHub Action — Task 12
- ✅ Delete `build_pdf.py`, `R1_Manual_v2.pdf`, `build_manual_pdf.sh` — Task 13
- ✅ Update README.md + MAINTENANCE.md — Task 13

**Type / signature consistency check:**
- `BuildContext` defined in Task 7, used in Tasks 7, 8, 10. Stats fields (`images_embedded`, `images_converted`, `images_downloaded`, `images_skipped`) all referenced consistently.
- `SummaryEntry` fields (`kind`, `depth`, `title`, `path`, `chapter`) consistent across Tasks 2 and 8.
- `process_image` / `fetch_external` / `resolve_image_path` signatures consistent across Tasks 4-7.

**Task ordering note:** Task 11 (first production run) sits before Task 12 (CI workflow) so that the very first KB PDF lands as a human-authored commit, not a CI-authored one. This makes the diff easy to review. After that, CI takes over for incremental updates.

**One known soft spot:** the HEIC test in Task 5 is gated on a fixture file that doesn't exist; the test will skip until someone adds `tests/fixtures/images/sample.heic`. This is acceptable — synthesizing a HEIC programmatically is more trouble than it's worth for one test, and the conversion path will be exercised by Task 11 (first production run) against the real `.gitbook/assets/`.
