# PDF Maintenance — what's stale and what to update

**As of 2026-05-04**, `OcuTrap_Knowledge_Base.pdf` is auto-generated from
`SUMMARY.md` by `scripts/build_kb_pdf.py` and rebuilt on every push to `main`
via GitHub Actions. The "Pending updates" tracker now only applies to the
hand-coded scripts (`build_quick_start.py`, `build_cheat_sheet.py`).

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
| `pdf-docs/printed/R1_Quick_Start.pdf` | `scripts/build_quick_start.py` (hardcoded ReportLab) | Hand-edit Python → rerun script. **Does not** read any markdown. |
| `.gitbook/assets/R1_Operation_Cheat_Sheet.pdf` | `scripts/build_cheat_sheet.py` (hardcoded ReportLab) | Hand-edit Python → rerun script. **Does not** read any markdown. |
| `.gitbook/assets/OcuTrap_Knowledge_Base.pdf` | `scripts/build_kb_pdf.py` (auto-compiled from `SUMMARY.md`) | Edit GitBook markdown → CI rebuild on push to `main`. |
| `pdf-docs/printed/inside_sticker.png` | Hardware team | New sticker design → replace PNG. |

The Quick Start and Cheat Sheet have a narrow, intentional scope and don't need
to mirror every doc page. The Knowledge Base PDF is now a real compilation of
the GitBook docs.

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

- [x] **Quick Start — “view images”** (not “view captures”) — `build_quick_start.py` + regenerated PDF, 2026-05-20.
- [x] **Quick Start — battery / XT30 / chargers** — 5200 mAh (1A, male XT30) vs 10k mAh (2A, female XT30); charge via black connector only — script + PDF, 2026-05-20.
- [x] **Cheat Sheet — battery / XT30 callout** + Scout row in device states — script + PDF, 2026-05-20.
- [ ] **Cold weather guidance** — confirm whether the Cheat Sheet and Quick
  Start should include cold-weather guidance, or whether deferring to the
  GitBook docs (now fully captured in the auto-built Knowledge Base PDF) is
  intentional.

**Terminology:** “Hibernating” = powered off / deep sleep (still used on Cheat Sheet).
“Unarmed hibernation” = removed product setting (not in printed PDFs).

---

## Workflow when adding a new GitBook page

The Knowledge Base PDF picks up GitBook markdown changes automatically on the
next CI rebuild. Only the hand-coded shorter PDFs need a review:

1. Does this page describe a **firmware-gated feature**, **safety behaviour**,
   **LED/button pattern**, or **hardware step** that should also live in the
   Cheat Sheet or Quick Start? If yes → add a checkbox under "Pending updates"
   above with the date and the page path.
2. When you next regenerate the Cheat Sheet or Quick Start, work through the
   relevant checkboxes and tick them off in the same commit.
