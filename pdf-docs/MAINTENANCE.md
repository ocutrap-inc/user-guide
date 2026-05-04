# PDF Maintenance — what's stale and what to update

The PDFs in `pdf-docs/online/` are **not** auto-compiled from the GitBook docs.
Each one is hand-maintained by a different mechanism, and they drift from the
live docs at `docs.ocutrap.com` whenever the markdown changes without a
corresponding script edit.

This file tracks the current drift. Update each item when the PDF is rebuilt.

---

## How each PDF is actually maintained

| PDF | Source of truth | How updates propagate |
| --- | --- | --- |
| `printed/R1_Quick_Start.pdf` | `scripts/build_quick_start.py` (hardcoded ReportLab) | Hand-edit Python → rerun script. **Does not** read any markdown. |
| `online/R1_Operation_Cheat_Sheet.pdf` | `scripts/build_cheat_sheet.py` (hardcoded ReportLab) | Hand-edit Python → rerun script. **Does not** read any markdown. |
| `online/R1_Manual_v2.pdf` | `R1_Manual_v2.docx` (Word, **not in repo**) | Hand-edit `.docx` → export to PDF → commit PDF. The `.docx` is held by the docs author. |
| `online/OcuTrap_Knowledge_Base.pdf` | `scripts/build_pdf.py` (1,372 lines, hardcoded ReportLab) | Hand-edit Python → rerun script. **Does not** read any markdown. |
| `printed/inside_sticker.png` | Hardware team | New sticker design → replace PNG. |

The Quick Start and Cheat Sheet have a narrow, intentional scope and don't need
to mirror every doc page. The Knowledge Base PDF is the one that's
*supposed* to look like a compilation of the docs but isn't.

---

## Pending updates

### Critical (customer-facing docs say something the PDFs don't)

- [ ] **Monitoring Mode page** — added to GitBook on 2026-05-04 at
  `getting-started/app/monitoring-mode.md` with a full firmware-version table
  (v598 / v633 / v644 / v672 / v675 / v700–v706). The Knowledge Base PDF only
  mentions Monitoring Mode in passing on lines 473 and 1322 of `build_pdf.py`
  ("introduced in testing"); none of the firmware version requirements,
  `monImg` / `monImgInt` knobs, exit behaviour, or 5-min cooldown are
  documented. Cheat Sheet and Quick Start have **zero** mention of Monitoring
  Mode.
- [ ] **Lightning-bolt fast image request (firmware v550+)** — documented on
  GitBook 2026-05-04. Not in any PDF.
- [ ] **v675+ periodic photo heartbeat (`monImgInt`)** — documented on GitBook
  2026-05-04. Not in any PDF.
- [ ] **v700–v706 firmware feature notes** — documented on GitBook
  2026-05-04. Not in any PDF.

### Non-critical (housekeeping)

- [ ] **R1_Manual_v2.docx not tracked.** The README's "source of truth" for the
  manual lives outside the repo. Decide whether to commit the `.docx` (and
  accept Git tracking a binary that diffs poorly) or formally document where
  the canonical copy lives and who can edit it.
- [ ] **Cold weather guidance** — present in `build_pdf.py:874` ("Cold
  Weather Guide" section) but absent from Cheat Sheet and Quick Start. Confirm
  whether the shorter docs intentionally omit it.

---

## Architectural debt

The biggest problem is that `build_pdf.py` advertises itself as a knowledge
base compilation but is actually a parallel hand-coded document. Three ways to
resolve this — pick one and track it as a phase:

1. **Replace with a real compiler.** Walk `SUMMARY.md`, render each linked
   markdown via pandoc (already installed for `build_manual_pdf.sh`), stitch
   into one PDF. Removes 1,372 lines of drift-prone Python.
2. **Rename and rescope.** Stop calling it a knowledge base; treat it as a
   curated highlights PDF that intentionally summarizes, not mirrors. Keep the
   ReportLab approach but make the divergence intentional.
3. **Retire it.** If the GitBook site is the canonical knowledge base, the
   parallel PDF may not be earning its 50 MB. Verify customer demand before
   killing.

---

## Workflow when adding a new GitBook page

Until the architectural debt is resolved, every GitBook docs change should
trigger a checklist review:

1. Does this page describe a **firmware-gated feature**, **safety behaviour**,
   **LED/button pattern**, or **hardware step**? If yes → likely a PDF update.
2. Add a checkbox under "Pending updates" above with the date and the page
   path.
3. When you next regenerate a PDF, work through the relevant checkboxes and
   tick them off in the same commit.
