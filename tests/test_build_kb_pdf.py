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
