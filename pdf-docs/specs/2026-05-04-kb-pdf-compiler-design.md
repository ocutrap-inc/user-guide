# Knowledge Base PDF Compiler — Design

**Date:** 2026-05-04
**Status:** Approved
**Owner:** Graham Patterson
**Replaces:** `scripts/build_pdf.py` (1,372-line hand-coded ReportLab document)

## Goal

Produce `pdf-docs/online/OcuTrap_Knowledge_Base.pdf` as a faithful, print-quality
PDF rendering of the GitBook docs at `docs.ocutrap.com`. The PDF must:

1. **Stay in sync with the markdown** — generated, not hand-maintained. Adding a
   page to `SUMMARY.md` makes it appear in the PDF on the next CI run.
2. **Print well on letter portrait paper** — proper page breaks, real numbered
   TOC, page numbers, running chapter headers, controlled image sizing.
3. **Embed all images** — no broken references, no missing assets.

## Non-goals

- Custom branding / multi-page cover beyond a simple title page.
- Per-chapter or per-section PDFs. Single mega-PDF only.
- A mechanism to mark pages as "GitBook only, exclude from PDF." If a page
  shouldn't be in the PDF, remove it from `SUMMARY.md` and it disappears from
  docs.ocutrap.com too.
- Replacing `R1_Quick_Start.pdf` or `R1_Operation_Cheat_Sheet.pdf`. Those have
  intentionally narrow scope (single-page printed reference cards) and stay on
  their hand-coded ReportLab scripts.
- Translating GitBook syntax 1:1 into PDF visuals beyond what's listed in the
  Preprocessing rules table. Edge-case GitBook constructs not in the table get
  passed through as raw HTML and pandoc handles whatever it can.

## Architecture

```
SUMMARY.md ──┐
             │
markdown ────┼──> preprocess  ──> assembled.md ──> pandoc ──> kb.html ──┐
             │   (GitBook → CommonMark,            (with style.css)     │
.gitbook/    │    image path resolution,                                │
assets/  ────┘    HEIC→JPEG, max-dim cap)                               │
                                                                        v
                                                                  weasyprint
                                                                        │
                                                                        v
                                            pdf-docs/online/OcuTrap_Knowledge_Base.pdf
```

One Python script orchestrates the pipeline. Single command:

```bash
python3 scripts/build_kb_pdf.py
```

## File layout

### Add

- `scripts/build_kb_pdf.py` — orchestrator (~250 lines).
- `scripts/kb_pdf_style.css` — CSS Paged Media stylesheet.
- `.github/workflows/build-kb-pdf.yml` — CI auto-rebuild workflow.

### Delete

- `scripts/build_pdf.py` — the parallel hand-coded ReportLab document. The new
  compiler replaces it.
- `pdf-docs/online/R1_Manual_v2.pdf` — the Word-derived manual. The new
  compiler IS the manual; one source of truth (the GitBook markdown).
- `scripts/build_manual_pdf.sh` — only consumer was the deleted manual.

### Modify

- `pdf-docs/README.md` — update the `OcuTrap_Knowledge_Base.pdf` row to describe
  the new compiler honestly. Drop the `R1_Manual_v2.pdf` row.
- `pdf-docs/MAINTENANCE.md` — close the four "Pending updates" items the new
  compiler resolves (Monitoring Mode page, lightning-bolt request, v675+
  heartbeat, v700–v706 notes). Remove the architectural-debt section (debt
  paid). The Quick Start / Cheat Sheet rows stay since they remain hand-coded.

## Preprocessing rules

The Python orchestrator walks `SUMMARY.md` to determine document order and
chapter structure, reads each linked markdown file, and applies these
transforms before passing the assembled document to pandoc.

| GitBook construct | Transform |
| --- | --- |
| `{% hint style="info\|danger\|warning" %}…{% endhint %}` | `<div class="hint hint-{style}">…</div>` |
| `{% embed url="X" %}` | Plain markdown link `[X](X)` |
| `![](path)` and `<img src="path">` with relative paths | Resolve to absolute `file://` URL using the source markdown's location |
| `<figure><img …><figcaption>…</figcaption></figure>` | Pass through unchanged (pandoc handles raw HTML) |
| `.HEIC` images | Convert to JPEG via Pillow, cache in `.cache/kb-pdf/` |
| Any image reference with an `http://` or `https://` URL | Download once, cache in `.cache/kb-pdf/` keyed by URL hash, rewrite reference to local file |
| Images > 1600px wide | Downscale via Pillow to 1600px max width (preserve aspect ratio); save JPEGs at quality 82 |
| Filenames with spaces / `<>`-wrapped paths | Normalize before path resolution |
| `.gif` images | Use the first frame only (PDF has no animation) |
| Image at `path` not found on disk | Log warning, drop the `<img>` tag, continue |

Heading levels are rewritten so SUMMARY chapters become H1, sections H2,
sub-sections H3 — regardless of how the source markdown numbered itself. This
keeps the PDF's TOC consistent with `SUMMARY.md`.

The `.cache/kb-pdf/` directory is gitignored. CI uses an actions/cache step
keyed on the hashes of `SUMMARY.md` + `.gitbook/assets/` to avoid re-downloading
external images on every run.

## Print CSS

WeasyPrint implements the CSS Paged Media specification, so the styling is
plain CSS:

```css
@page {
  size: letter portrait;
  margin: 0.75in;
  @bottom-center { content: counter(page); }
  @top-right    { content: string(chapter-title); }
}

h1 {
  string-set: chapter-title content();
  page-break-before: always;
}

h2, h3 { page-break-after: avoid; }

img {
  max-width: 100%;
  max-height: 8in;
  page-break-inside: avoid;
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

table {
  border-collapse: collapse;
  page-break-inside: avoid;
  width: 100%;
}
th, td { border: 1px solid #ccc; padding: 0.4em 0.6em; }

code {
  font-family: ui-monospace, "JetBrains Mono", monospace;
  font-size: 0.9em;
  background: #f6f8fa;
  padding: 0.1em 0.3em;
  border-radius: 3px;
}

pre { page-break-inside: avoid; }
```

WeasyPrint generates a real numbered TOC from heading levels (`<nav
role="doc-toc">`) with page numbers, plus running chapter title in the page
header.

## GitHub Action

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
  workflow_dispatch:

concurrency:
  group: build-kb-pdf
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: sudo apt-get update && sudo apt-get install -y pandoc
      - run: pip install weasyprint pillow requests
      - uses: actions/cache@v4
        with:
          path: .cache/kb-pdf
          key: kb-pdf-${{ hashFiles('SUMMARY.md', '.gitbook/assets/**') }}
      - run: python3 scripts/build_kb_pdf.py
      - name: Commit if PDF changed
        run: |
          if ! git diff --quiet pdf-docs/online/OcuTrap_Knowledge_Base.pdf; then
            git config user.name 'github-actions[bot]'
            git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
            git add pdf-docs/online/OcuTrap_Knowledge_Base.pdf
            git commit -m "chore(kb-pdf): regenerate from docs [skip ci]"
            git push
          fi
```

The `[skip ci]` tag and the `paths:` filter together prevent infinite rebuild
loops. Concurrency group cancels in-flight builds when a new push lands so
queued runs don't pile up.

## Verification / smoke tests

The build script prints a summary to stdout:

```
Markdown files processed: 79
Images embedded:          312 (8 converted from HEIC, 14 downloaded externally,
                               3 skipped — see warnings)
Final PDF: 24.8 MB, 287 pages
```

Hard-fail thresholds (non-zero exit, no PDF written):

- Final page count outside `[50, 1000]` (heuristic; tune after first successful
  build. Out-of-range likely means SUMMARY parse broke or image scaling
  regressed).
- Final size > 100 MB (image scaling almost certainly regressed).
- Any image with a relative path referenced in SUMMARY-walked markdown is
  missing on disk (typo / asset deletion not yet propagated). External-URL
  image fetch failures are warnings, not failures, since the network is
  flaky and the cache should normally cover them.

Soft warnings (non-blocking):

- Animated GIF stripped to first frame.
- External URL fetched (slowest path; flagged so we know if a doc starts
  pulling lots of external images).

## Open questions

None at design time. If WeasyPrint output reveals issues with specific GitBook
markdown patterns we don't currently use, the preprocessing rules table is
where to extend.

## References

- Existing toolchain pattern: `scripts/build_manual_pdf.sh` (pandoc + Chrome
  headless, currently for the soon-to-be-deleted Word manual).
- Drift tracker: `pdf-docs/MAINTENANCE.md` — this design is option 1 from the
  "Architectural debt" section.
- The reorg PR that exposed the architectural problem: PR #2 (merged
  2026-05-04, commit `66b8da4`).
- Asset path quirks (Unicode space variants in filenames) historically handled
  by `scripts/build_pdf.py`'s `img_path` helper. Port the same normalization
  into the new compiler's image resolver.
