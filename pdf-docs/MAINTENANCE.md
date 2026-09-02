# PDF Maintenance — what's stale and what to update

**As of 2026-05-04**, `OcuTrap_Knowledge_Base.pdf` is auto-generated from
`SUMMARY.md` by `scripts/build_kb_pdf.py` and rebuilt on every push to `main`
via GitHub Actions. The "Pending updates" tracker now only applies to the
hand-coded scripts (`build_box_manual.py`, `build_cheat_sheet.py`).

**As of 2026-09-02**, the in-box paper is a single **half-letter booklet,
5.5 x 8.5 in portrait, 8 pages**, one per model, built by
`scripts/build_box_manual.py`. It replaced the old 20-page (R1) / 17-page (R2)
letter manuals and the 2-page quick starts, and their scripts
(`build_manual.py`, `build_manual_r2.py`, `build_quick_start.py`,
`build_quick_start_r2.py`) are gone.

Customer-downloadable PDFs live in `.gitbook/assets/` so GitBook can serve
them via the `{% file %}` syntax (linked from
`appendix-and-resources/downloads.md`). They are **not** all auto-compiled
from the GitBook docs — only the Knowledge Base PDF is. The Cheat Sheet
remains a hand-maintained ReportLab document.

This file tracks the current drift. Update each item when the PDF is rebuilt.

---

## How each PDF is actually maintained

| PDF | Source of truth | How updates propagate |
| --- | --- | --- |
| `pdf-docs/printed/R2_Quick_Start_Guide.pdf` (+ `.gitbook/assets/R2_Quick_Start_Guide.pdf`) | `scripts/build_box_manual.py` (hardcoded ReportLab) | Hand-edit Python → `python3 scripts/build_box_manual.py --model r2` → copy to `.gitbook/assets/`. **Does not** read any markdown. |
| `pdf-docs/printed/R2_Quick_Start_Guide_print-2up.pdf` | derived from `R2_Quick_Start_Guide.pdf` by the same script (pypdf imposition) | Never hand-edited. Rebuilt automatically with the reading-order file. |
| `pdf-docs/printed/R1_Quick_Start_Guide.pdf` (+ `.gitbook/assets/R1_Quick_Start_Guide.pdf`) | `scripts/build_box_manual.py` | Hand-edit Python → `python3 scripts/build_box_manual.py --model r1` → copy to `.gitbook/assets/`. |
| `pdf-docs/printed/R1_Quick_Start_Guide_print-2up.pdf` | derived from `R1_Quick_Start_Guide.pdf` by the same script | Never hand-edited. |
| `.gitbook/assets/R1_Operation_Cheat_Sheet.pdf` | `scripts/build_cheat_sheet.py` (hardcoded ReportLab) | Hand-edit Python → rerun script. **Does not** read any markdown. |
| `.gitbook/assets/OcuTrap_Knowledge_Base.pdf` | `scripts/build_kb_pdf.py` (auto-compiled from `SUMMARY.md`) | Edit GitBook markdown → CI rebuild on push to `main`. |
| `pdf-docs/printed/inside_sticker.png` | Hardware team | New sticker design → replace PNG. |

The booklet and the Cheat Sheet have a narrow, intentional scope and don't
need to mirror every doc page. The Knowledge Base PDF is a real compilation of
the GitBook docs.

### Two flavors, one script

| Flavor | Page size | What it is for |
| --- | --- | --- |
| `<MODEL>_Quick_Start_Guide.pdf` | half-letter 5.5 x 8.5 in portrait, 8 pages | Reading order. This is the docs download and the file you read on screen. |
| `<MODEL>_Quick_Start_Guide_print-2up.pdf` | letter landscape 11 x 8.5 in, 4 sheet sides | Imposed for saddle folding. This is the file you send to the printer. |

**Print recipe:** print the `_print-2up` file on US letter, **duplex**,
**flip on the short edge**, at **1 page per sheet** (do not let the driver
shrink to fit). Fold each of the 2 sheets in half, then nest **sheet 2 inside
sheet 1**. Pages then read 1 through 8.

**Rebuild:**

```bash
python3 scripts/build_box_manual.py --model all
cp pdf-docs/printed/R2_Quick_Start_Guide.pdf .gitbook/assets/R2_Quick_Start_Guide.pdf
cp pdf-docs/printed/R1_Quick_Start_Guide.pdf .gitbook/assets/R1_Quick_Start_Guide.pdf
```

The script exits non-zero if a booklet is not exactly 8 pages (the imposition
needs a multiple of 4). If content spills, add a page and keep the total a
multiple of 4. Do not shrink the type: the scale in the script docstring
(body 11 pt on 14.5 pt, step titles 12 pt, headings 16 pt, table cells 10 pt,
captions 9 pt, legal 8.5 pt, footer 8.5 pt) is a legibility floor. The one
exception is the R1 buttons+lights page, which carries both reference tables
and keeps 9.5 pt cells.

---

## Pending updates

### Critical (customer-facing docs say something the PDFs don't)

- [x] **Monitoring Mode page** — added to GitBook on 2026-05-04 at
  `getting-started/app/monitoring-mode.md` with a full firmware-version table
  (v598 / v633 / v644 / v672 / v675 / v700–v706). Resolved by new compiler —
  auto-included as of `d5c1712`.
- [x] **Lightning-bolt fast image request (firmware v550+)** — documented on
  GitBook 2026-05-04. Resolved by new compiler — auto-included as of
  `d5c1712`.
- [x] **v675+ periodic photo heartbeat (`monImgInt`)** — documented on GitBook
  2026-05-04. Resolved by new compiler — auto-included as of `d5c1712`.
- [x] **v700–v706 firmware feature notes** — documented on GitBook
  2026-05-04. Resolved by new compiler — auto-included as of `d5c1712`.

### Non-critical (housekeeping)

- [x] **Quick Start — “view images”** (not “view captures”) — landed in the retired `build_quick_start.py`, 2026-05-20; superseded by the booklet 2026-09-02.
- [ ] **Booklet — battery / XT30 / chargers detail** — the retired quick start called out 5200 mAh (1A, male XT30) vs 10k mAh (2A, female XT30) and "charge via the black connector only". The booklet's charge step does not repeat the connector detail. Decide whether to add it back to `build_box_manual.py`.
- [x] **Cheat Sheet — battery / XT30 callout** + Scout row in device states — script + PDF, 2026-05-20.
- [x] **Cold weather guidance** — the booklet's Weather block carries the
  0 °C to 40 °C rating and the "door can ice, check it before arming" line,
  2026-09-02.
- [ ] **R2 cover photo** — the cover of both booklets uses the assembled-R1
  hero shot (`.gitbook/assets/DSC03816.JPG`) because no R2 product photo
  exists in the repo. Swap it in `cover_page()` when one lands (DOC-23).
- [ ] **R2 setup photos** — the R2 set-up pages reuse R1 photos (POD, top
  clip, charger). Replace with R2 shots when available (DOC-23).

**Terminology:** “Hibernating” = powered off / deep sleep (still used on the
Cheat Sheet and in the booklet's status light table).
“Unarmed hibernation” = removed product setting (not in printed PDFs).

---

## Workflow when adding a new GitBook page

The Knowledge Base PDF picks up GitBook markdown changes automatically on the
next CI rebuild. Only the hand-coded shorter PDFs need a review:

1. Does this page describe a **firmware-gated feature**, **safety behaviour**,
   **LED/button pattern**, or **hardware step** that should also live in the
   Cheat Sheet or the in-box booklet? If yes → add a checkbox under "Pending
   updates" above with the date and the page path.
2. When you next regenerate the Cheat Sheet or the booklet, work through the
   relevant checkboxes and tick them off in the same commit.
