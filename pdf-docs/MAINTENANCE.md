# PDF Maintenance — what's stale and what to update

**As of 2026-05-04**, `OcuTrap_Knowledge_Base.pdf` is auto-generated from
`SUMMARY.md` by `scripts/build_kb_pdf.py` and rebuilt on every push to `main`
via GitHub Actions. The "Pending updates" tracker now only applies to the
hand-coded scripts (`build_quick_start.py`, `build_cheat_sheet.py`).

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
| `online/OcuTrap_Knowledge_Base.pdf` | `scripts/build_kb_pdf.py` (auto-compiled from `SUMMARY.md`) | Edit GitBook markdown → CI rebuild on push to `main`. |
| `printed/inside_sticker.png` | Hardware team | New sticker design → replace PNG. |

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

- [ ] **Cold weather guidance** — confirm whether the Cheat Sheet and Quick
  Start should include cold-weather guidance, or whether deferring to the
  GitBook docs (now fully captured in the auto-built Knowledge Base PDF) is
  intentional.

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
