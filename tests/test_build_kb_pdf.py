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
