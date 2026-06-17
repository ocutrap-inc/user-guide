#!/usr/bin/env python3
"""
Build the OcuTrap R1 Installation & User Manual — letter-size, print-ready PDF.

Replaces the Google Docs "Manual v2" (half-letter, 24 pages) with a branded,
letter-portrait manual that prints normally (one page per sheet, no 2-up).
Content parity with Manual v2: unboxing, assembly, app setup, POD operation,
weather, maintenance, LED reference, battery safety, finger/animal safety,
use restrictions, warranty, FCC, and laser safety.

Source of truth for content: docs.ocutrap.com (canonical knowledge base)
Images:                      pdf-docs/manual-images/ (plain git blobs)

Usage:
    pip install reportlab Pillow qrcode
    python scripts/build_manual.py

Output: pdf-docs/printed/R1_Manual.pdf
"""

import os
import tempfile

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(REPO_ROOT, ".gitbook", "assets")
IMAGES = os.path.join(REPO_ROOT, "pdf-docs", "manual-images")
OUT_DIR = os.path.join(REPO_ROOT, "pdf-docs", "printed")
OUTPUT = os.path.join(OUT_DIR, "R1_Manual.pdf")
LOGO = os.path.join(ASSETS, "LogoMakr-1uMIUJ-300dpi (2).png")

DOCS_URL = "https://docs.ocutrap.com"
SIGNUP_URL = "https://base.ocutrap.com/signuplogin"
IOS_URL = "https://apps.apple.com/us/app/ocutrap/id1539244938"
ANDROID_URL = "https://play.google.com/store/apps/details?id=com.ocutrap.ocutrap"

LAST_UPDATED = "June 2026"

# Brand palette (matches quick start / cheat sheet)
BRAND_GREEN = HexColor("#3A6B35")
BRAND_DARK = HexColor("#1E3B1B")
BRAND_ACCENT = HexColor("#C07B2A")
BRAND_CREAM = HexColor("#F6F4EF")
INK = HexColor("#1A1A1A")
MUTED = HexColor("#555555")
RULE = HexColor("#CFCFCF")
WARN_RED = HexColor("#9B2318")
WARN_BG = HexColor("#FBEEEC")
NOTE_BG = HexColor("#EFF3EE")
TBL_HEAD = HexColor("#E4EAE2")

PAGE_W, PAGE_H = letter
MARGIN = 0.75 * inch
USABLE_W = PAGE_W - 2 * MARGIN

styles = getSampleStyleSheet()

sH1 = ParagraphStyle(
    "H1", parent=styles["Heading1"],
    fontName="Helvetica-Bold", fontSize=20, leading=24,
    textColor=BRAND_DARK, spaceBefore=0, spaceAfter=4,
)
sH2 = ParagraphStyle(
    "H2", parent=styles["Heading2"],
    fontName="Helvetica-Bold", fontSize=13.5, leading=16,
    textColor=BRAND_GREEN, spaceBefore=10, spaceAfter=4,
)
sH3 = ParagraphStyle(
    "H3", parent=styles["Heading3"],
    fontName="Helvetica-Bold", fontSize=11, leading=13,
    textColor=INK, spaceBefore=8, spaceAfter=3,
)
sBody = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontName="Helvetica", fontSize=10, leading=13.5,
    textColor=INK, spaceAfter=5,
)
sBodySmall = ParagraphStyle(
    "BodySmall", parent=sBody, fontSize=9, leading=12, textColor=MUTED,
)
sCell = ParagraphStyle(
    "Cell", parent=sBody, fontSize=9.5, leading=12, spaceAfter=0,
)
sCellHead = ParagraphStyle(
    "CellHead", parent=sCell, fontName="Helvetica-Bold", textColor=BRAND_DARK,
)
sCaption = ParagraphStyle(
    "Caption", parent=styles["Normal"],
    fontName="Helvetica-Oblique", fontSize=8.5, leading=10.5,
    textColor=MUTED, alignment=TA_CENTER, spaceAfter=0, spaceBefore=2,
)
sWarnTitle = ParagraphStyle(
    "WarnTitle", parent=sBody, fontName="Helvetica-Bold",
    textColor=WARN_RED, fontSize=10.5, leading=13, spaceAfter=2,
)
sTOC = ParagraphStyle(
    "TOC", parent=sBody, fontSize=11, leading=20, spaceAfter=0,
)

_TMP = []


def _tmp_png(pil_img):
    t = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    pil_img.save(t.name, "PNG")
    _TMP.append(t.name)
    return t.name


def flatten_on_white(path):
    """Composite RGBA/P images onto white so transparency never turns black
    when downstream conversion drops the alpha channel."""
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = PILImage.new("RGBA", im.size, (255, 255, 255, 255))
            bg.alpha_composite(im)
            return _tmp_png(bg.convert("RGB"))
    return path


def fit_image(path, max_w, max_h, target_dpi=200):
    """Fit-and-downsample an image, preserving aspect ratio. RGBA art is
    flattened onto white first (fixes the black-box logo bug)."""
    if not path or not os.path.exists(path):
        print(f"  warn: missing image {path}")
        return None
    from PIL import Image as PILImage
    path = flatten_on_white(path)
    with PILImage.open(path) as im:
        w, h = im.size
        aspect = w / h
        iw, ih = max_w, max_w / aspect
        if ih > max_h:
            ih, iw = max_h, max_h * aspect
        target_px_w = int((iw / inch) * target_dpi)
        if w > target_px_w * 1.25:
            im = im.convert("RGB")
            im.thumbnail((target_px_w, int(target_px_w / aspect)),
                         PILImage.LANCZOS)
            t = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            im.save(t.name, "JPEG", quality=85, optimize=True)
            _TMP.append(t.name)
            return Image(t.name, width=iw, height=ih)
    return Image(path, width=iw, height=ih)


def img(name, max_w, max_h):
    return fit_image(os.path.join(IMAGES, name), max_w, max_h)


def make_qr(url, size_px=400):
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    pil = qr.make_image(fill_color="black",
                        back_color="white").convert("RGB").resize(
                            (size_px, size_px))
    return _tmp_png(pil)


def qr_block(url, label, size=1.1 * inch):
    """QR code with a caption beneath it."""
    q = fit_image(make_qr(url), size, size)
    tbl = Table([[q], [Paragraph(label, sCaption)]], colWidths=[size + 8])
    tbl.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return tbl


def callout(title, body_items, kind="warning"):
    """Boxed safety/notice callout with a colored left band."""
    if kind == "warning":
        band, bg, tstyle = WARN_RED, WARN_BG, sWarnTitle
    else:
        band, bg, tstyle = BRAND_GREEN, NOTE_BG, ParagraphStyle(
            "NoteTitle", parent=sWarnTitle, textColor=BRAND_DARK)
    rows = [[Paragraph(title, tstyle)]]
    for item in body_items:
        rows.append([Paragraph(item, sCell)])
    inner = Table(rows, colWidths=[USABLE_W - 0.22 * inch])
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    outer = Table([["", inner]], colWidths=[0.08 * inch,
                                            USABLE_W - 0.08 * inch])
    outer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), band),
        ("BACKGROUND", (1, 0), (1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (1, 0), (1, -1), 5),
        ("BOTTOMPADDING", (1, 0), (1, -1), 5),
    ]))
    return outer


def data_table(head, rows, col_widths):
    """Striped reference table with brand-tinted header row."""
    data = [[Paragraph(h, sCellHead) for h in head]]
    for r in rows:
        data.append([Paragraph(c, sCell) for c in r])
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), TBL_HEAD),
        ("LINEBELOW", (0, 0), (-1, 0), 1, BRAND_GREEN),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(2, len(data), 2):
        style.append(("BACKGROUND", (0, i), (-1, i), BRAND_CREAM))
    tbl.setStyle(TableStyle(style))
    return tbl


def bullets(items, bold_first=False):
    out = []
    for it in items:
        out.append(Paragraph(f"&bull;&nbsp;&nbsp;{it}", ParagraphStyle(
            "Bullet", parent=sBody, leftIndent=14, firstLineIndent=-10,
            spaceAfter=3)))
    return out


def numbered(items):
    out = []
    for i, it in enumerate(items, 1):
        out.append(Paragraph(
            f'<font color="#C07B2A"><b>{i}.</b></font>&nbsp;&nbsp;{it}',
            ParagraphStyle("Num", parent=sBody, leftIndent=16,
                           firstLineIndent=-16, spaceAfter=3)))
    return out


def section_heading(text):
    """Page-level section heading with accent rule."""
    tbl = Table([[Paragraph(text, sH1)]], colWidths=[USABLE_W])
    tbl.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 1.5, BRAND_GREEN),
    ]))
    return tbl


def img_row(cells, total_w, caption_under=True):
    """Lay images (name, caption, max_h) side by side, centered."""
    col_w = total_w / len(cells)
    imgs, caps = [], []
    for name, cap, max_h in cells:
        imgs.append(img(name, col_w - 0.25 * inch, max_h) or "")
        caps.append(Paragraph(cap, sCaption) if cap else "")
    rows = [imgs]
    if caption_under and any(c != "" for c in caps):
        rows.append(caps)
    tbl = Table(rows, colWidths=[col_w] * len(cells))
    tbl.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return tbl


# ---------------------------------------------------------------- page chrome

def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BRAND_GREEN)
    canvas.rect(0, 0, PAGE_W, 0.35 * inch, stroke=0, fill=1)
    canvas.setFillColor(BRAND_ACCENT)
    canvas.rect(0, 0.35 * inch, PAGE_W, 0.06 * inch, stroke=0, fill=1)
    canvas.restoreState()


def on_page(canvas, doc):
    canvas.saveState()
    # header rule + wordmark
    canvas.setStrokeColor(BRAND_GREEN)
    canvas.setLineWidth(1)
    canvas.line(MARGIN, PAGE_H - 0.55 * inch, PAGE_W - MARGIN,
                PAGE_H - 0.55 * inch)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(BRAND_DARK)
    canvas.drawString(MARGIN, PAGE_H - 0.48 * inch,
                      "OcuTrap R1 — Installation & User Manual")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.48 * inch, DOCS_URL)
    # footer
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 0.6 * inch, PAGE_W - MARGIN, 0.6 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 0.45 * inch, "© OcuTrap, Inc.")
    canvas.drawRightString(PAGE_W - MARGIN, 0.45 * inch,
                           f"Page {doc.page}")
    canvas.restoreState()


# ------------------------------------------------------------------- sections

def cover(story):
    story.append(Spacer(1, 0.7 * inch))
    logo = fit_image(LOGO, 3.4 * inch, 0.9 * inch)
    if logo:
        logo.hAlign = "CENTER"
        story.append(logo)
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        "OcuTrap R1",
        ParagraphStyle("CT1", parent=sH1, fontSize=34, leading=38,
                       alignment=TA_CENTER, textColor=BRAND_DARK)))
    story.append(Paragraph(
        "Installation &amp; User Manual",
        ParagraphStyle("CT2", parent=sH1, fontSize=22, leading=28,
                       alignment=TA_CENTER, textColor=BRAND_GREEN)))
    story.append(Spacer(1, 0.35 * inch))
    hero = img("cage.png", 4.6 * inch, 2.6 * inch)
    if hero:
        hero.hAlign = "CENTER"
        story.append(hero)
    story.append(Spacer(1, 0.45 * inch))
    notice = Table([[Paragraph(
        "<b>Please read this manual fully before assembling or operating "
        "your OcuTrap R1.</b>",
        ParagraphStyle("CN", parent=sBody, alignment=TA_CENTER,
                       fontSize=11, leading=14, spaceAfter=0))]],
        colWidths=[5.4 * inch])
    notice.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, BRAND_GREEN),
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_CREAM),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    notice.hAlign = "CENTER"
    story.append(notice)
    story.append(Spacer(1, 0.5 * inch))
    qr = qr_block(DOCS_URL, "Online docs &amp; video guides<br/>"
                            "<b>docs.ocutrap.com</b>", size=1.3 * inch)
    qr.hAlign = "CENTER"
    story.append(qr)
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())


def contents_and_unboxing(story):
    story.append(section_heading("Contents"))
    story.append(Spacer(1, 6))
    # NOTE: page numbers below must match the built PDF (footer numbering).
    # After layout changes, rebuild and verify with scripts in pdf-docs/.
    toc = [
        ("Unboxing and Initial Inspection", "3"),
        ("Hardware Setup", "3"),
        ("Section 1 — Handle Assembly", "4"),
        ("Section 2 — Door Assembly", "5"),
        ("Section 3 — Motor &amp; POD Assembly", "7"),
        ("Section 4 — App Setup", "7"),
        ("Operating the POD", "8"),
        ("Weather", "11"),
        ("Routine Maintenance", "11"),
        ("LED Indicator Reference", "12"),
        ("Battery Safety Precautions", "13"),
        ("Safety Warnings — Moving Parts &amp; Animal Handling", "15"),
        ("Safety Information, Restrictions, and Notices", "15"),
        ("OcuTrap R1 Hardware Warranty", "16"),
        ("FCC Compliance and Laser Safety", "18"),
    ]
    rows = [[Paragraph(t, sTOC),
             Paragraph(p, ParagraphStyle("TP", parent=sTOC,
                                         alignment=TA_CENTER))]
            for t, p in toc]
    tbl = Table(rows, colWidths=[USABLE_W - 0.6 * inch, 0.6 * inch])
    tbl.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(tbl)
    story.append(PageBreak())

    story.append(section_heading("Unboxing and Initial Inspection"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Carefully unpack your OcuTrap R1 and check that all components "
        "are included:", sBody))
    story.append(Spacer(1, 6))
    story.append(img_row([
        ("cage.png", "Cage", 2.2 * inch),
        ("parts-box.png", "Parts box", 2.2 * inch),
    ], USABLE_W))
    story.append(Spacer(1, 8))
    story.append(callout("Before you continue", [
        "Examine each item for any visible damage. If anything is missing "
        "or appears damaged, halt installation and contact OcuTrap Support "
        "at <b>support@ocutrap.com</b> with your trap ID.",
    ], kind="note"))
    story.append(Spacer(1, 14))


def hardware_setup(story):
    story.append(section_heading("Hardware Setup"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Charge the Battery", sH2))
    half = (USABLE_W - 0.3 * inch) / 2
    charge_text = [
        Paragraph(
            "Fully charge the blue battery <b>before assembly</b> using the "
            "charger found in the small white box. The charger light is "
            "<b>red</b> while charging and <b>green</b> when full. A full "
            "charge takes 4&ndash;5 hours.", sBody),
        Spacer(1, 4),
        Paragraph(
            "If anything appears damaged, contact "
            "<b>support@ocutrap.com</b> for assistance.", sBody),
    ]
    charger = img("charger.png", half - 0.1 * inch, 1.6 * inch) or ""
    row = Table([[charge_text, charger]], colWidths=[half + 0.3 * inch, half])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(row)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Assembly is divided into four sections. Carefully follow each step "
        "to ensure your OcuTrap functions correctly and efficiently:", sBody))
    story.extend(numbered([
        "<b>Handle Assembly</b>",
        "<b>Door Assembly</b>",
        "<b>Motor &amp; POD Assembly</b>",
        "<b>App Setup</b>",
    ]))
    story.append(PageBreak())

    # ---- Section 1: Handle
    story.append(Paragraph("Section 1 — Handle Assembly", sH2))
    story.append(Paragraph("Step 1: Gather your components", sH3))
    parts_col = bullets([
        "4&times; 3&rdquo; bolt", "1&times; handle guard", "1&times; tube",
        "4&times; washer", "2&times; upper tube plastic spacer",
        "2&times; lower tube plastic handle spacer",
        "2&times; in-trap bracket with press-fit nut",
        "2&times; top metal bracket", "1&times; nut driver",
    ])
    handle = img("handle-render.png", half - 0.1 * inch, 1.9 * inch) or ""
    row = Table([[parts_col, handle]], colWidths=[half, half + 0.3 * inch])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(row)
    story.append(Paragraph("Step 2: Assemble the handle", sH3))
    story.extend(numbered([
        "Center the handle guard on the trap.",
        "Insert the two top handle assembly pieces into the holes in the "
        "handle guard.",
        "Slide the tube between the two handle guards and ensure it is "
        "centered.",
        "Place the bracket (with the press-fit nut) inside the trap and "
        "hand-tighten the bolts.",
        "Use the nut driver to fully tighten the bolts from the top, "
        "ensuring the handle remains secure.",
    ]))
    story.append(Spacer(1, 6))
    story.append(img_row([
        ("handle-installed.png", "Handle installed (top view)", 2.0 * inch),
        ("handle-in-trap.png", "In-trap view", 2.0 * inch),
    ], USABLE_W))
    story.append(PageBreak())

    # ---- Section 2: Door
    story.append(Paragraph("Section 2 — Door Assembly", sH2))
    story.append(Paragraph("Step 1: Gather your components", sH3))
    door_parts = bullets([
        "2&times; brackets (top locking mechanism)", "2&times; black spacers",
        "2&times; black capped nuts", "1&times; metal door",
        "1&times; 12&rdquo; rod", "1&times; nut driver",
        "1&times; nut assembly tool <i>(figure right)</i>",
    ])
    motor_parts = bullets([
        "1&times; motor", "2&times; pins", "2&times; clevises",
        "1&times; top motor bracket", "2&times; washers",
        "2&times; 1&rdquo; bolt",
    ])
    nut_tool = img("nut-tool.png", 1.7 * inch, 1.3 * inch) or ""
    third = USABLE_W / 3
    row = Table(
        [[[Paragraph("<b>Door</b>", sCellHead)] + door_parts,
          [Paragraph("<b>Motor</b>", sCellHead)] + motor_parts,
          nut_tool]],
        colWidths=[third + 0.4 * inch, third - 0.2 * inch, third - 0.2 * inch])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (2, 0), (2, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(row)
    story.append(Paragraph("Step 2: Assemble the door mechanism", sH3))
    story.append(Paragraph("Align the metal door inside the trap.", sBody))
    story.extend(numbered([
        "Thread the metal rod through the oval slot in the metal bracket "
        "attached to the top of the solid metal trap door.",
        "On each end of the rod: place the black spacer, secure it with "
        "the black capped nut, then use the nut assembly tool and nut "
        "driver on each end to tighten the nut until snug.",
    ]))
    story.append(Spacer(1, 4))
    diagram = img("door-rod-diagram.png", 5.6 * inch, 1.7 * inch)
    if diagram:
        diagram.hAlign = "CENTER"
        story.append(diagram)
        story.append(Paragraph("Door rod, spacers, and capped nuts",
                               sCaption))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Step 3: Assemble the motor", sH3))
    motor_steps = numbered([
        "Install the top bracket with washers and bolts. Tighten with the "
        "nut driver.",
        "Use the pins and clevises to secure the motor to the door at both "
        "the top and bottom attachment points.",
        "Feed the cable through the metal handle.",
        "Verify that all components are securely fastened.",
        "Check that the door moves smoothly and is properly aligned.",
    ])
    bracket = img("motor-bracket.png", half - 0.2 * inch, 1.7 * inch) or ""
    row = Table([[motor_steps, bracket]], colWidths=[half + 0.3 * inch, half])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(row)
    story.append(Spacer(1, 4))
    motor_img = img("motor-in-trap.png", 3.4 * inch, 2.5 * inch)
    if motor_img:
        motor_img.hAlign = "CENTER"
        story.append(motor_img)
        story.append(Paragraph(
            "Motor secured to the door with pins and clevises", sCaption))
    story.append(PageBreak())

    # ---- Section 3: POD
    story.append(Paragraph("Section 3 — Motor &amp; POD Assembly", sH2))
    story.append(Paragraph("Step 1: Prepare the battery", sH3))
    story.append(Paragraph(
        "Ensure the battery is fully charged. Charging can take "
        "4&ndash;5 hours.", sBody))
    story.append(Paragraph("Step 2: Connect the wire to the POD", sH3))
    story.extend(numbered([
        "Slide the POD down the rails on the trap until it is in place.",
        "Attach the motor&rsquo;s wire to the POD using the locking screw "
        "connector, ensuring a secure connection.",
        "Use the top latch to secure the POD in place.",
    ]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "At this point, your hardware setup is complete.", sBody))
    story.append(Spacer(1, 10))

    # ---- Section 4: App setup
    story.append(Paragraph("Section 4 — App Setup", sH2))
    story.append(Paragraph("Step 1: Create an account", sH3))
    acct = Paragraph(
        "Go to <b>base.ocutrap.com</b> (or scan the QR code on the right) "
        "and create an account.", sBody)
    row = Table([[acct, qr_block(SIGNUP_URL, "Create an account")]],
                colWidths=[USABLE_W - 1.6 * inch, 1.6 * inch])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(row)
    story.append(Spacer(1, 6))
    story.append(Paragraph("Step 2: Download the mobile app", sH3))
    qr_row = Table(
        [[qr_block(IOS_URL, "<b>iOS</b> download", size=1.25 * inch),
          qr_block(ANDROID_URL, "<b>Android</b> download", size=1.25 * inch)]],
        colWidths=[USABLE_W / 2] * 2)
    qr_row.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(qr_row)
    story.append(Spacer(1, 6))
    story.append(Paragraph("Step 3: Activate the trap through the app", sH3))
    act_steps = numbered([
        "Create an account on the app.",
        "Locate the POD for the OcuTrap you wish to register, open it, and "
        "find the serial number on the top of the device.",
        "In the app, go to <b>Account</b> (top right of the dashboard), "
        "then tap <b>Add Trap</b> at the bottom of the page.",
        "Enter the serial number when prompted.",
        "Follow the in-app prompts to enable your subscription.",
        "Once complete, the new trap will appear in your dashboard.",
    ])
    screens = img_row([
        ("app-account.png", "Account page &mdash; scroll down", 2.5 * inch),
        ("app-add-trap.png", "Tap &ldquo;Add Trap&rdquo;", 2.5 * inch),
    ], 3.4 * inch)
    row = Table([[act_steps, screens]],
                colWidths=[USABLE_W - 3.4 * inch, 3.4 * inch])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(row)
    story.append(Spacer(1, 6))
    story.append(Paragraph("Initial hardware checkout", sH3))
    story.extend(numbered([
        "<b>Power on:</b> connect the fully charged battery.",
        "<b>Connectivity check:</b> ensure the trap is within network "
        "range. Check the indicator light for a stable connection "
        "(breathing cyan). It may take up to 10 minutes to connect to "
        "cellular networks.",
        "<b>Open the control panel:</b> open the OcuTrap app.",
        "<b>Engage the trap:</b> select <b>Arm</b> in the app to initiate "
        "trap readiness. Ensure cameras, sensors, and mechanisms respond "
        "correctly.",
    ]))
    story.append(Spacer(1, 14))


def pod_operation(story):
    story.append(section_heading("Operating the POD"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Buttons on the POD", sH2))
    half = (USABLE_W - 0.3 * inch) / 2
    btn_tbl = data_table(
        ["Label", "Button"],
        [["1", "Power"], ["2", "Mode"], ["3", "Reset"], ["4", "User"],
         ["5", "LED Indicator"], ["6", "Battery Port"]],
        [0.7 * inch, half - 0.7 * inch])
    panel = img("pod-panel.png", half - 0.1 * inch, 1.8 * inch) or ""
    row = Table([[btn_tbl, panel]], colWidths=[half, half + 0.3 * inch])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(row)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Arming / Unarming", sH2))
    story.append(Paragraph(
        "Use the <b>User Button</b> and <b>Power Button</b> together to "
        "toggle between <b>Armed</b> and <b>Unarmed</b> states.", sBody))
    story.append(data_table(
        ["Action", "Steps", "Indicator"],
        [["<b>Arm</b> the device",
          "1. Press the <b>User Button</b>.<br/>"
          "2. Immediately press the <b>Power Button</b>.<br/>"
          "3. Ensure the door is <b>set to open</b> before arming.",
          "Flashing <b>yellow</b> (arming)"],
         ["<b>Unarm</b> the device",
          "1. Press the <b>User Button</b>.<br/>"
          "2. Immediately press the <b>Power Button</b> again.",
          "Flashing <b>white</b> (unarmed)"]],
        [1.3 * inch, USABLE_W - 2.9 * inch, 1.6 * inch]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Reset", sH2))
    story.append(Paragraph(
        "Restarts the device <b>without changing its configuration</b>.",
        sBody))
    story.append(data_table(
        ["Action", "Steps", "Indicator"],
        [["<b>Reset</b> the device",
          "1. Press the <b>Reset Button</b> once.<br/>"
          "2. The device will reboot and retain its current state.",
          "No LED indicator"]],
        [1.3 * inch, USABLE_W - 2.9 * inch, 1.6 * inch]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Door Functionality", sH2))
    story.append(data_table(
        ["Action", "Steps", "Indicator", "Description"],
        [["Open door",
          "1. Press the <b>User Button</b>.<br/>"
          "2. Release, then <b>press and hold</b> for 5 seconds.",
          "<b>Blue</b> flashes", "Door opens"],
         ["Close door",
          "1. Press the <b>User Button</b>.<br/>"
          "2. Release, then <b>press and hold</b> for 5 seconds.",
          "<b>Green</b> flashes", "Door closes"],
         ["Arm / Unarm",
          "Follow the Arming / Unarming steps above.",
          "See above", "Toggles <b>Armed / Unarmed</b>"]],
        [1.1 * inch, USABLE_W - 4.0 * inch, 1.3 * inch, 1.6 * inch]))
    story.append(PageBreak())

    story.append(Paragraph("Device Status Indicators", sH2))
    story.append(data_table(
        ["Mode", "Color / Pattern", "Description"],
        [["Unarmed &amp; Open", "Solid Blue",
          "The device is <b>unarmed</b>, and the <b>door is open</b>."],
         ["Unarmed &amp; Closed", "Solid Green",
          "The device is <b>unarmed</b>, and the <b>door is closed</b>."],
         ["Armed Mode", "Solid Yellow", "The device is <b>armed</b>."],
         ["Armed &amp; Captured", "Solid Magenta",
          "The device is <b>armed</b>, and a <b>capture event</b> has "
          "occurred."]],
        [1.6 * inch, 1.5 * inch, USABLE_W - 3.1 * inch]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Shut-down Operation", sH2))
    story.append(data_table(
        ["Steps", "Indicator"],
        [["<b>Power off:</b> hold down the <b>PWR</b> button for 3 seconds",
          "Blinking Red"],
         ["<b>Shutting down</b> (takes about 10 seconds)",
          "Solid Red and other lights"],
         ["<b>Fully powered off</b>", "No LED"]],
        [USABLE_W - 2.0 * inch, 2.0 * inch]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Unarmed Hibernation Control", sH2))
    story.append(Paragraph(
        "Each trap&rsquo;s Unarmed Sleep Mode is configured separately. "
        "In the app, go to <b>Settings &rarr; More Settings &rarr; Unarmed "
        "Sleep Mode</b> to adjust it.", sBody))
    story.append(data_table(
        ["Setting", "Behavior"],
        [["<b>Yes</b> (default)", "The trap hibernates when unarmed."],
         ["<b>No</b>", "The trap stays fully powered when unarmed."]],
        [1.6 * inch, USABLE_W - 1.6 * inch]))
    story.append(Spacer(1, 4))
    story.append(callout("Note", [
        "Disabling hibernation by selecting &ldquo;No&rdquo; will lead to "
        "higher battery consumption."], kind="note"))
    story.append(PageBreak())


def weather_and_maintenance(story):
    story.append(section_heading("Weather"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "OcuTrap is designed to withstand various outdoor conditions, "
        "including rain, wind, and moderate environmental challenges. While "
        "the enclosure is weatherproof, internal electronics should never "
        "be submerged in water. The trap is built for durability, but users "
        "should take precautions during extreme weather to prevent "
        "potential damage. For optimal performance, OcuTrap operates best "
        "between 0&deg;C (32&deg;F) and 40&deg;C (104&deg;F). Prolonged "
        "exposure to temperatures outside this range may affect performance "
        "and battery longevity. The lithium-ion battery should be charged "
        "at room temperature to maintain efficiency and lifespan.", sBody))
    story.append(Paragraph(
        "Extreme heat and cold can reduce performance and battery life, "
        "while freezing conditions may cause the door mechanism to become "
        "stuck and the motor to not operate properly. To prevent icing, "
        "avoid operating the trap in environments where freezing is likely. "
        "Although the enclosure is weatherproof, heavy rain or flooding "
        "could compromise internal electronics, so relocating or protecting "
        "the trap is advised. To maximize battery longevity, follow the "
        "recommended temperature guidelines and avoid prolonged exposure to "
        "extreme conditions. No additional maintenance is required.", sBody))
    story.append(Spacer(1, 10))

    story.append(section_heading("Routine Maintenance"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Run this checklist after every capture, and after harsh weather.",
        sBody))
    story.append(Paragraph("1. Cleaning", sH3))
    story.append(data_table(
        ["Item", "Action"],
        [["Camera and sensor lens",
          "Wipe with a soft, lint-free cloth until clear."],
         ["Exterior", "Wipe with a damp cloth."],
         ["Interior parts (door, motor area)",
          "Remove any debris, wipe if needed."]],
        [2.6 * inch, USABLE_W - 2.6 * inch]))
    story.append(Paragraph("2. Battery", sH3))
    story.append(data_table(
        ["Task", "Action"],
        [["Charge", "Fully charge before use, top off as needed."],
         ["Terminals", "Check for corrosion or wear, wipe dry if dirty."]],
        [2.6 * inch, USABLE_W - 2.6 * inch]))
    story.append(Paragraph("3. Quick Function Check", sH3))
    story.append(data_table(
        ["System", "Action"],
        [["Door", "Test open and close, fix any sticking."],
         ["Motor and sensors", "Confirm motor runs and sensors respond."]],
        [2.6 * inch, USABLE_W - 2.6 * inch]))
    story.append(Paragraph("4. Weatherproofing", sH3))
    story.append(data_table(
        ["Area", "Action"],
        [["Seals, enclosures", "Check for cracks or looseness."],
         ["After bad weather",
          "Look for moisture or debris inside, dry out if needed."]],
        [2.6 * inch, USABLE_W - 2.6 * inch]))
    story.append(Paragraph("5. Log", sH3))
    story.append(Paragraph(
        "Keep a simple note of cleanings, checks, and repairs.", sBody))
    story.append(Spacer(1, 4))
    story.append(callout("Safety", [
        "Power off the trap and unplug the battery before maintenance."]))
    story.append(Spacer(1, 14))


def led_reference(story):
    story.append(section_heading("LED Indicator Reference"))
    story.append(Spacer(1, 6))
    story.append(data_table(
        ["Status", "Color / Pattern", "Description"],
        [["Connected", "Solid Cyan",
          "Device is successfully connected to the cloud."],
         ["Connecting", "Blinking Cyan",
          "Device is establishing cloud connection."],
         ["Firmware Update", "Blinking Magenta",
          "Device is performing an OTA update."],
         ["Internet Search", "Blinking Green",
          "Device is searching for internet connection."],
         ["SOS Alert", "Flashing Red (&bull;&bull;&bull; &mdash;&mdash;&mdash;)",
          "Device requires immediate attention."],
         ["Low Power", "Blinking Red",
          "Battery level too low for operation."],
         ["Error State", "Solid Red", "System error detected."],
         ["No Power", "No Light",
          "Device is either powered off, in ultra-low power mode, in armed "
          "low power mode, or requires power source check/reset."]],
        [1.5 * inch, 2.1 * inch, USABLE_W - 3.6 * inch]))
    story.append(PageBreak())


def battery_safety(story):
    story.append(section_heading("Battery Safety Precautions"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The OcuTrap uses sealed lithium-ion batteries. <b>Dispose of used "
        "batteries according to all applicable federal, state, and local "
        "regulations.</b>", sBody))
    story.append(callout("General Safety Warnings", [
        "&bull;&nbsp; Do not expose the battery to fire, water, or "
        "excessive heat.",
        "&bull;&nbsp; Avoid short-circuiting the terminals.",
        "&bull;&nbsp; Use only the provided charger to prevent overcharging "
        "or damage.",
        "&bull;&nbsp; Handle the battery carefully to prevent punctures or "
        "impacts.",
        "&bull;&nbsp; Keep out of reach of children.",
    ]))
    story.append(Paragraph("Base Battery", sH2))
    story.append(Paragraph(
        "The KBT 12V Rechargeable Li-ion Battery is a versatile power "
        "source for 12V devices. Designed for reliability and long-term "
        "use, it is equipped with essential safety features and a durable "
        "build.", sBody))
    story.append(Paragraph("Specifications", sH3))
    story.extend(bullets([
        "Voltage: 12V", "Battery type: Lithium-ion",
        "Charging cycles: over 800 cycles",
    ]))
    story.append(Paragraph("Charging Instructions", sH3))
    story.extend(numbered([
        "Use the provided 12V charger for optimal performance.",
        "Connect the barrel connector securely to the charger&rsquo;s "
        "barrel connector.",
        "Charge the battery in a cool, dry place.",
        "Avoid leaving the battery connected to the charger once fully "
        "charged.",
    ]))
    story.append(Paragraph("Battery Installation in the POD", sH3))
    story.extend(numbered([
        "Open the POD latch.",
        "Place the battery in the bracket at the bottom of the POD.",
        "Plug the battery into the POD using the yellow connectors. Push "
        "straight in until fully seated.",
        "Make sure the cables are tucked out of the way of the door "
        "closing points, along the edge of the enclosure, so the wires do "
        "not get squished.",
        "Close the latch fully to maintain waterproofness.",
    ]))
    story.append(PageBreak())
    story.append(Paragraph("Maintenance &amp; Storage", sH3))
    story.extend(bullets([
        "Store the battery in a cool, dry place away from direct sunlight "
        "or heat sources.",
        "For long-term storage, keep the battery partially charged (around "
        "40&ndash;60%) to preserve its health.",
        "Clean the terminals periodically to maintain proper conductivity.",
        "Avoid exposing the battery to moisture or corrosive materials.",
    ]))
    story.append(Paragraph("Troubleshooting FAQs", sH3))
    story.append(Paragraph(
        "<b>Q: What should I do if the battery doesn&rsquo;t charge?</b><br/>"
        "A: Verify the charger is functioning properly and ensure secure "
        "connections to the terminals.", sBody))
    story.append(Paragraph(
        "<b>Q: Why is the battery overheating?</b><br/>"
        "A: Stop usage immediately and check for device compatibility or "
        "possible overcharging.", sBody))
    story.append(Paragraph(
        "<b>Q: How can I extend the battery life?</b><br/>"
        "A: Avoid fully depleting the battery before recharging and store "
        "it properly when not in use.", sBody))
    story.append(Spacer(1, 4))
    story.append(callout("Cautions", [
        "&bull;&nbsp; Do not attempt to open or modify the battery.",
        "&bull;&nbsp; Avoid charging the battery in extreme temperatures "
        "(&lt;0&deg;C or &gt;40&deg;C).",
        "&bull;&nbsp; Do not connect the battery to devices exceeding its "
        "voltage or capacity limits.",
        "&bull;&nbsp; Dispose of the battery properly according to local "
        "regulations when it reaches the end of its lifespan.",
    ]))
    story.append(PageBreak())


def safety_warnings(story):
    story.append(section_heading(
        "Safety Warnings — Moving Parts &amp; Animal Handling"))
    story.append(Spacer(1, 4))
    story.append(callout("⚠ Caution: Risk of Finger Injury", [
        "The OcuTrap&rsquo;s moving parts, including the motorized door and "
        "spring mechanism, can cause serious injury if fingers are placed "
        "in or near the trap&rsquo;s assembly while in operation.",
        "&bull;&nbsp; Keep hands and fingers clear of the trap door and "
        "motorized components at all times.",
        "&bull;&nbsp; Ensure the trap is powered off before performing "
        "maintenance or adjustments.",
        "&bull;&nbsp; Always use the provided assembly tools to adjust or "
        "interact with components.",
        "&bull;&nbsp; Do not allow children to operate or handle the trap.",
        "<b>Failure to follow these safety precautions can result in "
        "serious injury.</b>",
    ]))
    story.append(Paragraph("Animal Handling Safety", sH2))
    story.extend(bullets([
        "<b>Approach the trap cautiously</b> when an animal is captured, "
        "and wear protective gloves to prevent injury.",
        "<b>Avoid direct contact with animals</b>, especially if aggressive "
        "or frightened.",
    ]))
    story.append(Spacer(1, 10))

    story.append(section_heading(
        "Safety Information, Restrictions, and Notices"))
    story.append(Spacer(1, 4))
    story.append(callout("Safety and Use Restrictions — DO NOT USE OCUTRAP:", [
        "&bull;&nbsp; AS A SUBSTITUTE FOR LIFE SAFETY OR MEDICAL DEVICES.",
        "&bull;&nbsp; FOR ANY TYPE OF MEDICAL MONITORING OR LIFE-SUSTAINING "
        "APPLICATION.",
        "&bull;&nbsp; IN ANY WAY THAT VIOLATES FEDERAL, STATE, LOCAL, OR "
        "ADMINISTRATIVE LAWS, REGULATIONS, OR ORDINANCES. This includes, "
        "but is not limited to, laws governing wildlife and animal "
        "welfare, health and safety, data privacy, and security.",
        "&bull;&nbsp; IN A MANNER THAT INVOLVES CRIMINAL OR ILLEGAL "
        "ACTIVITIES.",
    ]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>OcuTrap is not responsible for injury during use.</b>", sBody))
    story.append(Paragraph(
        "<b>DO NOT ATTACH OCUTRAP TO OR PLACE IT NEAR LIFE SAFETY DEVICES, "
        "MEDICAL MONITORING EQUIPMENT, OR OTHER SENSITIVE DEVICES</b> where "
        "it could interfere with the operation, safety, or functionality "
        "of such equipment.", sBody))
    story.append(PageBreak())


def warranty(story):
    story.append(section_heading("OcuTrap R1 Hardware Warranty"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("1. Warranty Coverage", sH2))
    story.append(Paragraph(
        "OcuTrap, Inc. (&ldquo;Company&rdquo;) warrants that the "
        "&ldquo;OcuTrap R1&rdquo; hardware will be free from defects in "
        "materials and workmanship under normal use and conditions for a "
        "period of 12 months from the date of original purchase by the end "
        "user (&ldquo;Warranty Period&rdquo;).", sBody))
    story.append(Paragraph("2. Warranty Conditions", sH2))
    story.append(Paragraph(
        "During the Warranty Period, the Company will repair or replace, "
        "at its discretion, any defective components or product covered by "
        "this warranty. Replacement parts or products may be new or "
        "reconditioned at the Company&rsquo;s discretion and will be "
        "warranted for the remainder of the original Warranty Period or 90 "
        "days from the date of repair or replacement, whichever is longer.",
        sBody))
    story.append(Paragraph("3. Limitations and Exclusions", sH2))
    story.append(Paragraph("This warranty does not cover the following:",
                           sBody))
    story.extend(bullets([
        "<b>Improper Installation:</b> damage caused by incorrect "
        "installation not in accordance with the Company&rsquo;s "
        "installation guidelines.",
        "<b>Misuse or Neglect:</b> issues arising from misuse, neglect, or "
        "improper maintenance.",
        "<b>Third-party Modifications:</b> defects caused by unauthorized "
        "modifications, adjustments, or repairs by the user or a third "
        "party.",
        "<b>Environmental Factors:</b> damage due to power failures, power "
        "surges, extreme weather conditions, or other environmental "
        "factors beyond the Company&rsquo;s control.",
        "<b>Normal Wear and Tear:</b> cosmetic damage or normal wear and "
        "tear not affecting the functionality of the OcuTrap R1.",
        "<b>Non-OcuTrap Parts or Accessories:</b> damage caused by the use "
        "of parts or accessories not authorized by OcuTrap, Inc.",
    ]))
    story.append(Paragraph("4. Warranty Claims Process", sH2))
    story.append(Paragraph(
        "To make a claim under this warranty, the customer must:", sBody))
    story.extend(numbered([
        "Contact OcuTrap Support at <b>support@ocutrap.com</b> with proof "
        "of purchase.",
        "Provide a description of the issue, including any relevant photos "
        "or details to help diagnose the problem.",
        "Ship the product to an authorized repair facility or return "
        "address if requested by the Company, with shipping label provided "
        "by OcuTrap.",
    ]))
    story.append(Paragraph("5. Liability Limitation", sH2))
    story.append(Paragraph(
        "The Company&rsquo;s liability under this warranty is limited "
        "solely to the repair or replacement of the defective product or "
        "parts at its discretion. The Company is not liable for any "
        "indirect, incidental, or consequential damages arising from the "
        "use of, or inability to use, the OcuTrap R1, including any loss "
        "of profits, business interruption, or damage to other property.",
        sBody))
    story.append(Paragraph("6. Governing Law", sH2))
    story.append(Paragraph(
        "This warranty is governed by the laws of Texas without regard to "
        "its conflict of laws principles. Any disputes arising from this "
        "warranty will be subject to the exclusive jurisdiction of the "
        "courts located in the state of Texas.", sBody))
    story.append(Paragraph("7. Warranty Modifications", sH2))
    story.append(Paragraph(
        "OcuTrap, Inc. reserves the right to modify the terms and "
        "conditions of this warranty at any time, with any such changes "
        "not applying retroactively to products purchased before the "
        "modification date.", sBody))
    story.append(Paragraph("8. Contact Information", sH2))
    story.append(Paragraph(
        "For any questions or concerns regarding this warranty, please "
        "contact: <b>support@ocutrap.com</b>", sBody))
    story.append(PageBreak())


def fcc_and_laser(story):
    story.append(section_heading("FCC Compliance and Laser Safety"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("FCC Compliance Statement", sH2))
    story.append(Paragraph(
        "This device complies with Part 15 of the FCC Rules. Operation is "
        "subject to the following two conditions:", sBody))
    story.extend(bullets([
        "This device may not cause harmful interference.",
        "This device must accept any interference received, including "
        "interference that may cause undesired operation.",
    ]))
    story.append(Paragraph("FCC ID", sH3))
    story.append(Paragraph(
        "The FCC Identifier for this device is: <b>FCC ID: "
        "2AEMI-B404X</b>", sBody))
    story.append(Paragraph("Modifications Warning", sH3))
    story.append(Paragraph(
        "Changes or modifications not expressly approved by Particle "
        "Industries, Inc. could void the user&rsquo;s authority to operate "
        "the equipment.", sBody))
    story.append(Paragraph("RF Exposure Information", sH3))
    story.append(Paragraph(
        "This equipment complies with FCC radiation exposure limits set "
        "forth for an uncontrolled environment. To maintain compliance, "
        "this device should be installed and operated with a minimum "
        "distance of 20 centimeters between the radiator and your body.",
        sBody))
    story.append(Paragraph("Antenna Information", sH3))
    story.append(Paragraph(
        "The B404X SoM is designed to be used with external antennas. "
        "Ensure that the antennas used are of the same type and have equal "
        "or lesser gain than those tested to comply with FCC regulations.",
        sBody))
    story.append(Paragraph("Responsible Party Information", sH3))
    story.append(Paragraph(
        "For compliance inquiries, please contact: Particle Industries, "
        "Inc., 325 9th St, San Francisco, CA 94103 USA", sBody))
    story.append(Paragraph("Additional Resources", sH3))
    story.append(Paragraph(
        "For more detailed information, including test reports and "
        "certifications, please refer to the official FCC documentation "
        "for this device: https://fccid.io/2AEMI-B404X", sBody))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Laser Safety Information", sH2))
    laser_text = [
        Paragraph(
            "This product contains a laser emitter and corresponding drive "
            "circuitry. The laser output is designed to meet Class 1 laser "
            "safety limits under all reasonably foreseeable conditions, "
            "including single faults, in compliance with <b>IEC "
            "60825-1:2014</b>.", sBody),
    ]
    label = img("laser-label.png", 1.8 * inch, 1.0 * inch) or ""
    row = Table([[laser_text, label]],
                colWidths=[USABLE_W - 2.1 * inch, 2.1 * inch])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(row)
    story.append(Spacer(1, 4))
    story.append(callout("Important Safety Instructions", [
        "&bull;&nbsp; <b>Do not increase the laser output power by any "
        "means.</b>",
        "&bull;&nbsp; <b>Do not use any optics to focus the laser beam.</b>",
        "&bull;&nbsp; <b>Caution:</b> use of controls or adjustments, or "
        "performance of procedures other than those specified herein, may "
        "result in hazardous radiation exposure.",
    ]))
    story.append(Paragraph("Compliance Information", sH3))
    story.append(Paragraph(
        "This product complies with the following standards:", sBody))
    story.extend(bullets([
        "<b>IEC 60825-1:2014</b>",
        "<b>21 CFR 1040.10 and 1040.11</b>, except for conformance with "
        "IEC 60825-1:2014 as described in the Laser Notice Number 56, "
        "dated May 8, 2019.",
        "<b>EN 60825-1:2014</b>, including <b>EN 60825-1:2014/A11:2021</b>",
        "<b>This product is not intended for children.</b>",
    ]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "OcuTrap relies on a third-party wireless service using radio "
        "technology, which is subject to transmission and service area "
        "limitations. This may include <b>interruptions or dropped "
        "connections</b> due to atmospheric, topographical, or "
        "environmental factors, cell site availability, cellular network "
        "equipment or installation, government regulations, system "
        "limitations, maintenance, or other conditions affecting wireless "
        "service functionality. Wireless service and features may not be "
        "available in all areas.", sBodySmall))
    story.append(NextPageTemplate("cover"))
    story.append(PageBreak())


def back_cover(story):
    story.append(Spacer(1, 1.6 * inch))
    logo = fit_image(LOGO, 3.2 * inch, 0.85 * inch)
    if logo:
        logo.hAlign = "CENTER"
        story.append(logo)
    story.append(Spacer(1, 0.6 * inch))
    center = ParagraphStyle("BC", parent=sBody, alignment=TA_CENTER,
                            fontSize=10.5, leading=15)
    story.append(Paragraph("<b>OcuTrap, Inc.</b>", center))
    story.append(Paragraph(
        "5900 Balcones Drive, Suite 100<br/>Austin, Texas 78732, USA",
        center))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>OcuTrap.com</b>", center))
    story.append(Spacer(1, 0.3 * inch))
    qr = qr_block(DOCS_URL, "docs.ocutrap.com", size=1.2 * inch)
    qr.hAlign = "CENTER"
    story.append(qr)
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("<i>U.S. Patent No. 12,010,984</i>", center))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("support@ocutrap.com", center))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(f"Last updated: {LAST_UPDATED}", center))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("&copy; OcuTrap, Inc. All Rights Reserved.",
                           center))


# ------------------------------------------------------------------ assembly

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = BaseDocTemplate(
        OUTPUT, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="OcuTrap R1 Installation & User Manual",
        author="OcuTrap, Inc.",
    )
    cover_frame = Frame(MARGIN, 0.6 * inch, USABLE_W,
                        PAGE_H - 1.2 * inch, id="cover")
    body_frame = Frame(MARGIN, 0.75 * inch, USABLE_W,
                       PAGE_H - 0.75 * inch - 0.75 * inch, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover),
        PageTemplate(id="body", frames=[body_frame], onPage=on_page),
    ])

    story = []
    cover(story)
    contents_and_unboxing(story)
    hardware_setup(story)
    pod_operation(story)
    weather_and_maintenance(story)
    led_reference(story)
    battery_safety(story)
    safety_warnings(story)
    warranty(story)
    fcc_and_laser(story)
    back_cover(story)

    doc.build(story)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"Wrote {OUTPUT} ({size_kb:.0f} KB)")
    for t in _TMP:
        try:
            os.unlink(t)
        except OSError:
            pass


if __name__ == "__main__":
    main()
