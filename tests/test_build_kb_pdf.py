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
