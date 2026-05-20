#!/usr/bin/env python3
"""
Build the OcuTrap R1 Quick Start — a 2-page, letter-size, print-ready PDF.

Print single sheet, double-sided (flip on long edge). Folded in half for
shipping; read unfolded. Focus: bare-minimum hardware setup + a push to the
video guides at docs.ocutrap.com.

Source of truth for content: docs.ocutrap.com (canonical knowledge base)
Reference:                   getting-started/setting-up.md

Usage:
    pip install reportlab Pillow qrcode
    python scripts/build_quick_start.py

Output: pdf-docs/printed/R1_Quick_Start.pdf
"""

import io
import os
import sys
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
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(REPO_ROOT, ".gitbook", "assets")
OUT_DIR = os.path.join(REPO_ROOT, "pdf-docs", "printed")
OUTPUT = os.path.join(OUT_DIR, "R1_Quick_Start.pdf")
LOGO = os.path.join(ASSETS, "LogoMakr-1uMIUJ-300dpi (2).png")

DOCS_URL = "https://docs.ocutrap.com"
DASHBOARD_URL = "https://base.ocutrap.com"

# Brand palette (matches cheat sheet)
BRAND_GREEN = HexColor("#3A6B35")
BRAND_DARK = HexColor("#1E3B1B")
BRAND_ACCENT = HexColor("#C07B2A")
BRAND_CREAM = HexColor("#F6F4EF")
INK = HexColor("#1A1A1A")
MUTED = HexColor("#555555")
RULE = HexColor("#CFCFCF")

PAGE_W, PAGE_H = letter
MARGIN = 0.4 * inch
# The sheet is folded vertically down the middle for shipping. Keep content
# off the fold by using a generous gutter between the two panels.
FOLD_GUTTER = 0.4 * inch
FOLD_X = PAGE_W / 2  # absolute X of the fold line in PDF coords

styles = getSampleStyleSheet()

sTitle = ParagraphStyle(
    "Title", parent=styles["Title"],
    fontName="Helvetica-Bold", fontSize=26, leading=28,
    textColor=white, alignment=TA_LEFT, spaceAfter=0,
)
sSubtitle = ParagraphStyle(
    "Subtitle", parent=styles["Normal"],
    fontName="Helvetica", fontSize=11, leading=13,
    textColor=HexColor("#E8E8E8"), alignment=TA_LEFT,
)
sStepNum = ParagraphStyle(
    "StepNum", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=28, leading=30,
    textColor=BRAND_ACCENT, alignment=TA_CENTER, spaceAfter=0,
)
sStepTitle = ParagraphStyle(
    "StepTitle", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=12, leading=14,
    textColor=BRAND_DARK, alignment=TA_CENTER, spaceAfter=3,
)
sStepBody = ParagraphStyle(
    "StepBody", parent=styles["Normal"],
    fontName="Helvetica", fontSize=9.5, leading=12,
    textColor=INK, alignment=TA_CENTER, spaceAfter=0,
)
sSection = ParagraphStyle(
    "Section", parent=styles["Heading2"],
    fontName="Helvetica-Bold", fontSize=13, leading=15,
    textColor=white, alignment=TA_LEFT,
    spaceBefore=0, spaceAfter=0,
)
sBody = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontName="Helvetica", fontSize=10, leading=13,
    textColor=INK, alignment=TA_LEFT, spaceAfter=3,
)
sBodyBold = ParagraphStyle(
    "BodyBold", parent=sBody, fontName="Helvetica-Bold",
)
sSmall = ParagraphStyle(
    "Small", parent=styles["Normal"],
    fontName="Helvetica", fontSize=8.5, leading=11,
    textColor=MUTED, alignment=TA_LEFT, spaceAfter=2,
)
sCaption = ParagraphStyle(
    "Caption", parent=styles["Normal"],
    fontName="Helvetica-Oblique", fontSize=8, leading=10,
    textColor=MUTED, alignment=TA_CENTER, spaceAfter=0,
)
sQRLabel = ParagraphStyle(
    "QRLabel", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=9, leading=11,
    textColor=white, alignment=TA_CENTER,
)
sFooter = ParagraphStyle(
    "Footer", parent=styles["Normal"],
    fontName="Helvetica", fontSize=8, leading=10,
    textColor=MUTED, alignment=TA_CENTER,
)
sWarn = ParagraphStyle(
    "Warn", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=9.5, leading=12,
    textColor=HexColor("#7B241C"), alignment=TA_LEFT, spaceAfter=2,
)


def make_qr(url, size_px=400):
    """Generate a QR code PNG at a temp path; returns the path."""
    try:
        import qrcode
    except ImportError:
        print("  warn: qrcode not installed — skipping QR. pip install qrcode[pil]")
        return None
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size_px, size_px))
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name, "PNG")
    return tmp.name


_TMP_IMAGES = []


def fit_image(path, max_w, max_h, target_dpi=200):
    """Fit-and-downsample: return a reportlab Image whose embedded pixels are no
    larger than needed at `target_dpi` for the drawn size. Keeps PDF size sane
    when source photos are 4k+."""
    if not path or not os.path.exists(path):
        return None
    try:
        from PIL import Image as PILImage
        with PILImage.open(path) as im:
            w, h = im.size
            mode = im.mode
            aspect = w / h
            iw, ih = max_w, max_w / aspect
            if ih > max_h:
                ih, iw = max_h, max_h * aspect

            target_px_w = int((iw / inch) * target_dpi)
            target_px_h = int((ih / inch) * target_dpi)

            if w > target_px_w * 1.25 or h > target_px_h * 1.25:
                if mode in ("RGBA", "P"):
                    im = im.convert("RGB")
                im.thumbnail((target_px_w, target_px_h), PILImage.LANCZOS)
                tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                im.save(tmp.name, "JPEG", quality=82, optimize=True)
                _TMP_IMAGES.append(tmp.name)
                return Image(tmp.name, width=iw, height=ih)

            return Image(path, width=iw, height=ih)
    except Exception as e:
        print(f"  warn: {path}: {e}")
        return None


def asset(*names):
    """Return the first existing asset path from the list of names."""
    for n in names:
        p = os.path.join(ASSETS, n)
        if os.path.exists(p):
            return p
    return None


# ---------- Page 1: Setup ----------

def two_panel_header(panel_w, page_label):
    """Left half of the header: logo on top, large dark-green title, small
    subtitle, thin accent rule below. Stays entirely inside the left panel."""
    title_style = ParagraphStyle(
        "HT", parent=sTitle, fontSize=22, leading=24, textColor=BRAND_DARK,
    )
    subtitle_style = ParagraphStyle(
        "HS", parent=sSubtitle, fontSize=10, leading=12, textColor=MUTED,
    )

    logo = fit_image(LOGO, 1.8 * inch, 0.42 * inch)
    left_cells = []
    if logo:
        left_cells.append([logo])
        left_cells.append([Spacer(1, 4)])
    left_cells.append([Paragraph("OcuTrap R1 Quick Start", title_style)])
    left_cells.append([Spacer(1, 1)])
    left_cells.append([Paragraph(page_label, subtitle_style)])
    left_half = Table(left_cells, colWidths=[panel_w])
    left_half.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEBELOW", (0, -1), (-1, -1), 1.25, BRAND_GREEN),
    ]))
    return left_half


def side1_right_header(panel_w, qr_docs):
    """Right panel of the front header: QR + short video push."""
    qr_size = 1.15 * inch
    qr_img = fit_image(qr_docs, qr_size, qr_size) if qr_docs else None
    qr_cell = Table([[qr_img if qr_img else ""]], colWidths=[qr_size],
                    rowHeights=[qr_size])
    qr_cell.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    headline = ParagraphStyle(
        "VidHead", parent=sBodyBold, fontSize=12, leading=14,
        textColor=BRAND_DARK,
    )
    body = ParagraphStyle(
        "VidBody", parent=sSmall, fontSize=9, leading=11.5, textColor=INK,
    )
    text_cells = [
        [Paragraph("Scan for setup videos", headline)],
        [Spacer(1, 2)],
        [Paragraph("Full step-by-step videos &amp; knowledge base at "
                   "<b>docs.ocutrap.com</b>. This card covers the essentials.",
                   body)],
    ]
    text_tbl = Table(text_cells, colWidths=[panel_w - qr_size - 0.2 * inch])
    text_tbl.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    tbl = Table(
        [[qr_cell, text_tbl]],
        colWidths=[qr_size + 0.05 * inch, panel_w - qr_size - 0.05 * inch],
    )
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, -1), (-1, -1), 1.25, BRAND_GREEN),
    ]))
    return tbl


def side2_right_header(panel_w, qr_docs):
    """Right panel of the back header. Same shape as side 1 for registration."""
    return side1_right_header(panel_w, qr_docs)


def two_panel_row(left_flow, right_flow, panel_w):
    """Place two flowables (or lists of flowables) in side-by-side panels
    with a fold gutter between them. Nothing crosses the fold."""
    tbl = Table(
        [[left_flow, "", right_flow]],
        colWidths=[panel_w, FOLD_GUTTER, panel_w],
    )
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return tbl


def step_card(num, title, body, image_path, card_w, card_h):
    """Numbered step card with a numbered badge in the top-left, image
    centered, and title/body below. Clean, restrained, print-friendly."""
    # Compact number badge (orange circle-feel with bold numeral).
    badge_style = ParagraphStyle(
        "Badge", parent=sBody,
        fontName="Helvetica-Bold", fontSize=13, leading=15,
        textColor=white, alignment=TA_CENTER, spaceAfter=0,
    )
    badge = Table(
        [[Paragraph(f"<b>{num}</b>", badge_style)]],
        colWidths=[0.32 * inch], rowHeights=[0.32 * inch],
    )
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_ACCENT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    title_row = Table(
        [[badge, Paragraph(f"<b>{title}</b>",
                           ParagraphStyle("ST", parent=sStepTitle,
                                          alignment=TA_LEFT, spaceAfter=0))]],
        colWidths=[0.42 * inch, card_w - 0.42 * inch - 0.2 * inch],
    )
    title_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    img_h = card_h * 0.58
    img = fit_image(image_path, card_w - 0.3 * inch, img_h) if image_path else None
    img_cell = img if img else Paragraph("", sBody)

    body_style = ParagraphStyle(
        "CardBody", parent=sBody,
        fontSize=9.5, leading=12, alignment=TA_LEFT, textColor=INK,
    )

    inner = Table(
        [
            [title_row],
            [img_cell],
            [Paragraph(body, body_style)],
        ],
        colWidths=[card_w - 0.2 * inch],
    )
    inner.setStyle(TableStyle([
        ("ALIGN", (0, 1), (0, 1), "CENTER"),
        ("VALIGN", (0, 0), (0, 0), "TOP"),
        ("VALIGN", (0, 1), (0, 1), "MIDDLE"),
        ("VALIGN", (0, 2), (0, 2), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))

    outer = Table([[inner]], colWidths=[card_w], rowHeights=[card_h])
    outer.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("LINEABOVE", (0, 0), (-1, 0), 1.5, BRAND_GREEN),
        ("BACKGROUND", (0, 0), (-1, -1), white),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return outer


def panel_width(usable_w):
    return (usable_w - FOLD_GUTTER) / 2


def build_page_1(story, usable_w, qr_docs):
    panel_w = panel_width(usable_w)

    header = two_panel_row(
        two_panel_header(panel_w, "Setup &mdash; read this side first"),
        side1_right_header(panel_w, qr_docs),
        panel_w,
    )
    story.append(header)
    story.append(Spacer(1, 10))

    steps = [
        (
            "1", "Charge the battery",
            "Plug the blue battery into the supplied charger. "
            "Light is <b>red</b> while charging, <b>green</b> when full. 4&ndash;5 hrs.",
            asset("DSC03816.JPG"),
        ),
        (
            "2", "Assemble the handle",
            "Center the handle guard. Insert the tube and bolts. "
            "Place the internal bracket inside the trap; hand-tighten.",
            asset("unknown (5).png", "image (25).png"),
        ),
        (
            "3", "Attach door &amp; motor",
            "Thread the metal rod through the door bracket. "
            "Pin the motor to the door and feed its cable through the handle tube.",
            asset("image (28).png",
                  "Use the nut driver to mount the top motor bracket with the bolt and washer.png"),
        ),
        (
            "4", "Slide in the POD",
            "Slide the POD down the rails. Connect the motor wire. "
            "Close the top latch firmly for waterproofing.",
            asset("image.png", "unknown (7).png"),
        ),
    ]

    card_h = 3.3 * inch

    # Build each half-panel as a vertical stack of two cards so the fold
    # falls between the columns (not through a card).
    left_cards = [
        step_card(*steps[0], card_w=panel_w, card_h=card_h),
        Spacer(1, 8),
        step_card(*steps[2], card_w=panel_w, card_h=card_h),
    ]
    right_cards = [
        step_card(*steps[1], card_w=panel_w, card_h=card_h),
        Spacer(1, 8),
        step_card(*steps[3], card_w=panel_w, card_h=card_h),
    ]
    story.append(two_panel_row(left_cards, right_cards, panel_w))

    story.append(Spacer(1, 8))

    # Right-panel flip hint rendered as a subtle outlined pill so it reads
    # as a call-to-action without heavy ink coverage.
    flip_style = ParagraphStyle(
        "FlipHint", parent=sBody, alignment=TA_CENTER,
        fontName="Helvetica-Bold", textColor=BRAND_DARK, fontSize=10.5,
        spaceAfter=0,
    )
    pill = Table(
        [[Paragraph("Flip over for app setup &amp; arming  &rarr;",
                    flip_style)]],
        colWidths=[panel_w - 0.8 * inch],
    )
    pill.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, BRAND_GREEN),
        ("BACKGROUND", (0, 0), (-1, -1), white),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    right_hint_wrap = Table(
        [[pill]], colWidths=[panel_w],
    )
    right_hint_wrap.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    left_hint = Paragraph("", sSmall)
    story.append(two_panel_row(left_hint, right_hint_wrap, panel_w))


# ---------- Page 2: Activate & Arm ----------

def section_band(text, width):
    """Ink-light section heading: dark green text with a thin underline."""
    style = ParagraphStyle(
        "SectionLite", parent=styles["Heading2"],
        fontName="Helvetica-Bold", fontSize=12, leading=14,
        textColor=BRAND_DARK, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=0,
    )
    # Escape ampersands AFTER upper() so Paragraph XML stays valid.
    safe = text.upper().replace("&", "&amp;")
    tbl = Table(
        [[Paragraph(safe, style)]],
        colWidths=[width],
    )
    tbl.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -1), 0.75, BRAND_GREEN),
    ]))
    return tbl


def numbered_list(items, col_w):
    data = []
    for i, (title, body) in enumerate(items, 1):
        num = Paragraph(
            f'<font color="#C07B2A" size="16"><b>{i}</b></font>',
            ParagraphStyle("N", parent=sBody, leading=16),
        )
        text = Paragraph(f"<b>{title}</b><br/>{body}", sBody)
        data.append([num, text])
    tbl = Table(data, colWidths=[0.35 * inch, col_w - 0.35 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, RULE),
    ]))
    return tbl


def led_strip(width):
    """Tiny LED legend — enough to recognize the happy-path states on page 2."""
    rows = [
        ("Breathing cyan", HexColor("#06B6D4"), "Connected — ready to arm"),
        ("Solid yellow", HexColor("#EAB308"), "Armed, door open, waiting"),
        ("Solid magenta", HexColor("#D946EF"), "Capture detected"),
    ]
    data = []
    for label, color, desc in rows:
        chip = Table([[""]], colWidths=[0.3 * inch], rowHeights=[0.2 * inch])
        chip.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("BOX", (0, 0), (-1, -1), 0.3, RULE),
        ]))
        data.append([chip, Paragraph(f"<b>{label}</b> — {desc}", sBody)])
    tbl = Table(data, colWidths=[0.35 * inch, width - 0.35 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return tbl


def safety_panel(items, panel_w, show_header):
    """A single safety panel (half of the fold-split safety section).
    Only the left half draws the 'Safety' header so the two halves read
    as one warning block when the sheet is unfolded."""
    warn_style = ParagraphStyle(
        "SafetyHead", parent=sWarn, fontSize=11, leading=13,
        textColor=HexColor("#7B241C"),
    )
    item_style = ParagraphStyle(
        "SafetyItem", parent=sBody, fontSize=9.5, leading=12.5,
        textColor=INK, spaceAfter=1,
    )

    cells = []
    if show_header:
        cells.append([Paragraph("&#9888;&nbsp; Safety", warn_style)])
    else:
        # Blank spacer on right panel to keep vertical alignment with left.
        cells.append([Paragraph("&nbsp;", warn_style)])
    for t in items:
        cells.append([Paragraph(f"&bull;&nbsp;&nbsp;{t}", item_style)])

    tbl = Table(cells, colWidths=[panel_w])
    tbl.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (0, 0), 4),
        ("TOPPADDING", (0, 1), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, HexColor("#C0392B")),
    ]))
    return tbl


def support_left(qr_dash, panel_w):
    """Left half: 'Need help?' heading, bordered QR + side text, docs URL."""
    qr_size = 1.15 * inch
    qr_img = fit_image(qr_dash, qr_size, qr_size) if qr_dash else None
    qr_cell = Table([[qr_img if qr_img else ""]], colWidths=[qr_size],
                    rowHeights=[qr_size])
    qr_cell.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    heading = ParagraphStyle(
        "HelpHead", parent=sBodyBold, fontSize=12, leading=14,
        textColor=BRAND_DARK,
    )
    body = ParagraphStyle(
        "HelpBody", parent=sSmall, fontSize=9, leading=11.5, textColor=INK,
    )
    right_text = Table(
        [
            [Paragraph("Need help?", heading)],
            [Spacer(1, 2)],
            [Paragraph("Scan for the full knowledge base, videos, and "
                       "troubleshooting guides.", body)],
            [Spacer(1, 3)],
            [Paragraph("<b>docs.ocutrap.com</b>", sBody)],
        ],
        colWidths=[panel_w - qr_size - 0.2 * inch],
    )
    right_text.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    tbl = Table(
        [[qr_cell, right_text]],
        colWidths=[qr_size + 0.05 * inch, panel_w - qr_size - 0.05 * inch],
    )
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return tbl


def support_right(panel_w):
    """Right half: dashboard / support / related docs, consistent hierarchy."""
    lbl = ParagraphStyle(
        "SupLbl", parent=sSmall, fontName="Helvetica-Bold",
        fontSize=8.5, leading=10, textColor=BRAND_GREEN,
        spaceAfter=0,
    )
    val = ParagraphStyle(
        "SupVal", parent=sBody, fontSize=10, leading=12.5, textColor=INK,
        spaceAfter=0,
    )
    note = ParagraphStyle(
        "SupNote", parent=sSmall, fontSize=8.5, leading=11, textColor=MUTED,
        spaceAfter=0,
    )

    rows = [
        [Paragraph("DASHBOARD", lbl)],
        [Paragraph("<b>base.ocutrap.com</b>", val)],
        [Paragraph("Manage your traps &amp; view images", note)],
        [Spacer(1, 5)],
        [Paragraph("SUPPORT", lbl)],
        [Paragraph("<b>support@ocutrap.com</b>", val)],
        [Paragraph("Include your trap ID in the subject", note)],
        [Spacer(1, 5)],
        [Paragraph("ALSO ONLINE", lbl)],
        [Paragraph("Full manual &amp; operation cheat sheet at "
                   "<b>docs.ocutrap.com</b>", note)],
    ]
    tbl = Table(rows, colWidths=[panel_w])
    tbl.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return tbl


def build_page_2(story, usable_w, qr_docs, qr_dash):
    panel_w = panel_width(usable_w)

    story.append(two_panel_row(
        two_panel_header(panel_w, "Activate &amp; arm &mdash; after hardware is built"),
        side2_right_header(panel_w, qr_docs),
        panel_w,
    ))
    story.append(Spacer(1, 10))

    app_items = [
        ("Create an account",
         "Go to <b>base.ocutrap.com</b> or download the mobile app, then sign up."),
        ("Add your trap",
         "In the app: <b>Account &rarr; Add Trap</b>. Scan the QR inside the POD "
         "or type the serial number."),
        ("Activate subscription",
         "Follow the in-app prompts. Your trap appears on the dashboard."),
    ]
    arm_items = [
        ("Power on",
         "Install the charged battery and close the POD latch. The trap boots automatically."),
        ("Wait for breathing cyan",
         "Up to ~10 minutes to find cellular. A breathing cyan LED means connected."),
        ("Arm in the app",
         "Door must be <b>open</b>. Tap <b>Arm</b> in the app &mdash; the state LED turns yellow."),
    ]

    left_col = [
        section_band("5 · Set up the app", panel_w),
        Spacer(1, 6),
        numbered_list(app_items, panel_w),
    ]
    right_col = [
        section_band("6 · Power on & arm", panel_w),
        Spacer(1, 6),
        numbered_list(arm_items, panel_w),
        Spacer(1, 8),
        Paragraph("What the LED is telling you:", sBodyBold),
        Spacer(1, 2),
        led_strip(panel_w),
    ]

    story.append(two_panel_row(left_col, right_col, panel_w))

    story.append(Spacer(1, 12))

    safety_left = [
        "<b>Finger injury risk.</b> Keep hands clear of the door and motor at all times.",
        "<b>Power off</b> and disconnect the battery before any maintenance.",
    ]
    safety_right = [
        "Use only the supplied charger. Do not submerge or expose to fire.",
        "Do not let children operate the trap. Wear gloves near captured animals.",
    ]
    story.append(two_panel_row(
        safety_panel(safety_left, panel_w, show_header=True),
        safety_panel(safety_right, panel_w, show_header=False),
        panel_w,
    ))

    story.append(Spacer(1, 12))

    story.append(two_panel_row(
        support_left(qr_dash, panel_w),
        support_right(panel_w),
        panel_w,
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "&copy; OcuTrap, Inc. &middot; 5900 Balcones Drive, Suite 100, Austin, TX 78732 "
        "&middot; U.S. Patent No. 12,010,984",
        sFooter,
    ))


# ---------- Build ----------

SIDE_LABELS = {
    1: "Side 1 of 2 · Setup",
    2: "Side 2 of 2 · Activate & Arm",
}


def draw_side_footer(canv, doc):
    """Bottom-center side indicator + thin fold-line registration marks."""
    label = SIDE_LABELS.get(doc.page, f"Page {doc.page}")
    canv.saveState()
    canv.setFont("Helvetica", 7.5)
    canv.setFillColor(MUTED)
    canv.drawCentredString(PAGE_W / 2, 0.22 * inch, label)

    # Subtle fold tick marks at top and bottom of the center fold line.
    canv.setStrokeColor(MUTED)
    canv.setLineWidth(0.4)
    tick = 0.12 * inch
    canv.line(FOLD_X, PAGE_H, FOLD_X, PAGE_H - tick)
    canv.line(FOLD_X, 0, FOLD_X, tick)
    canv.restoreState()


def build():
    os.makedirs(OUT_DIR, exist_ok=True)

    qr_docs = make_qr(DOCS_URL)
    qr_dash = make_qr(DASHBOARD_URL)

    doc = BaseDocTemplate(
        OUTPUT, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="OcuTrap R1 Quick Start",
        author="OcuTrap, Inc.",
    )
    usable_w = PAGE_W - 2 * MARGIN
    usable_h = PAGE_H - 2 * MARGIN

    frame = Frame(
        MARGIN, MARGIN, usable_w, usable_h,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        id="main",
    )
    doc.addPageTemplates([PageTemplate(id="pg", frames=[frame], onPage=draw_side_footer)])

    story = []
    build_page_1(story, usable_w, qr_docs)
    story.append(PageBreak())
    build_page_2(story, usable_w, qr_docs, qr_dash)

    doc.build(story)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"Wrote {OUTPUT} ({size_kb:.0f} KB)")

    for p in (qr_docs, qr_dash, *_TMP_IMAGES):
        if p and os.path.exists(p):
            try:
                os.unlink(p)
            except OSError:
                pass


if __name__ == "__main__":
    build()
