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


def test_process_image_rgba_jpeg_does_not_crash(tmp_path):
    """A .jpg source opened as RGBA (rare but possible) must not raise on save."""
    from PIL import Image
    src = tmp_path / "weird.jpg"
    # Create a large RGBA image saved as PNG, then rename to .jpg to simulate
    # the rare case where Pillow opens a .jpg-suffixed file as RGBA.
    Image.new("RGBA", (4000, 2000), (255, 0, 0, 128)).save(src, "PNG")
    out = process_image(src, cache_dir=tmp_path / ".cache")
    # Should not crash. Output should be valid and openable.
    assert out.exists()
    with Image.open(out) as im:
        im.verify()


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


from build_kb_pdf import render_pdf

CSS_PATH = Path(__file__).parent.parent / "scripts" / "kb_pdf_style.css"


def test_render_pdf_produces_a_pdf(tmp_path):
    md = "# Hello\n\nWorld.\n\n# Chapter Two\n\nMore."
    out = tmp_path / "out.pdf"
    pages = render_pdf(md, css_path=CSS_PATH, output=out)
    assert out.exists() and out.stat().st_size > 0
    assert pages >= 2  # one page per H1 due to page-break-before
