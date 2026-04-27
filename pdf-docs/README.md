# PDF Docs

All print-ready and online-distribution PDFs for the OcuTrap R1. Organized by
how the document reaches the customer.

```
pdf-docs/
├── printed/   Physical items that ship with the trap
└── online/    Downloadable from docs.ocutrap.com and the dashboard
```

## `printed/` — Ships with the trap

The Quick Start is the only paper document in the box. Everything else the
customer needs is pushed to `docs.ocutrap.com` via QR code.

| File | Purpose | Source of truth |
| --- | --- | --- |
| `R1_Quick_Start.pdf` | 2-page, letter-size. Printed double-sided, folded in half. Bare-minimum setup (charge → assemble → app → arm) plus a big QR code to the video guides. | `scripts/build_quick_start.py` |
| `inside_sticker.png` | LED/button reference graphic pre-applied inside the POD lid. | Hardware team |

## `online/` — Downloadable only

| File | Purpose | Source of truth |
| --- | --- | --- |
| `R1_Manual_v2.docx` | Full Installation & User Manual (Word source). Edited in Word. | Word (hand-edited) |
| `R1_Manual_v2.pdf` | PDF export of the manual. | Generated from `.docx` |
| `R1_Operation_Cheat_Sheet.pdf` | One-page letter-size reference for users unfamiliar with the device: system LEDs, buttons, device states, safety. | `scripts/build_cheat_sheet.py` |
| `OcuTrap_Knowledge_Base.pdf` | ~50 MB PDF of every KB article with images. | `scripts/build_pdf.py` |

## Rebuilding

From the repo root (`user-guide/`):

```bash
pip3 install --user reportlab Pillow qrcode

# 2-page Quick Start (shipped in box)
python3 scripts/build_quick_start.py

# 1-page Operation Cheat Sheet (online download)
python3 scripts/build_cheat_sheet.py

# Full manual — requires pandoc + Chrome
brew install pandoc   # one-time
./scripts/build_manual_pdf.sh

# Online Knowledge Base PDF
python3 scripts/build_pdf.py
```

## When to update

- **Firmware changes that add/change LED patterns or button sequences**: update
  `R1_Manual_v2.docx`, re-export the PDF, and update the LED/button tables in
  `scripts/build_cheat_sheet.py` and `scripts/build_quick_start.py`. Replace
  `inside_sticker.png` if the hardware team ships a new sticker design.
- **Hardware revision (new parts list, different assembly steps)**: update the
  `.docx`, re-export the PDF, and adjust the 4 setup cards in
  `scripts/build_quick_start.py` (text + referenced images under
  `.gitbook/assets/`).
- **Contact/URL changes** (support email, dashboard URL, docs URL): update the
  docx and the footer/support strings in both `build_quick_start.py` and
  `build_cheat_sheet.py`.
