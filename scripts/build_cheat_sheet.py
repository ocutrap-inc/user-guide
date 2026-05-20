#!/usr/bin/env python3
"""
Build the OcuTrap R1 Operation Cheat Sheet — a one-page, letter-size,
print-ready PDF aimed at users not yet familiar with the device.

Source of truth for content: docs.ocutrap.com (canonical knowledge base)
LED/button reference graphic: pdf-docs/printed/inside_sticker.png

Usage:
    pip install reportlab Pillow
    python scripts/build_cheat_sheet.py

Output: .gitbook/assets/R1_Operation_Cheat_Sheet.pdf
        (served as a download via {% file %} from the Downloads page)
"""

import os
import sys

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDF_DOCS = os.path.join(REPO_ROOT, "pdf-docs")
STICKER = os.path.join(PDF_DOCS, "printed", "inside_sticker.png")
LOGO = os.path.join(REPO_ROOT, ".gitbook", "assets", "Removed Background logo.png")
OUTPUT = os.path.join(REPO_ROOT, ".gitbook", "assets", "R1_Operation_Cheat_Sheet.pdf")

# OcuTrap brand palette (from shopify-theme settings_schema.json)
BRAND_GREEN = HexColor("#3A6B35")
BRAND_DARK = HexColor("#1E3B1B")
BRAND_ACCENT = HexColor("#C07B2A")
BRAND_CREAM = HexColor("#F6F4EF")
INK = HexColor("#1A1A1A")
MUTED = HexColor("#555555")
RULE = HexColor("#CFCFCF")

PAGE_W, PAGE_H = letter
MARGIN = 0.4 * inch

styles = getSampleStyleSheet()

sTitle = ParagraphStyle(
    "Title", parent=styles["Title"],
    fontName="Helvetica-Bold", fontSize=22, leading=24,
    textColor=white, alignment=TA_LEFT, spaceAfter=0,
)
sSubtitle = ParagraphStyle(
    "Subtitle", parent=styles["Normal"],
    fontName="Helvetica", fontSize=10, leading=12,
    textColor=HexColor("#E8E8E8"), alignment=TA_LEFT,
)
sSection = ParagraphStyle(
    "Section", parent=styles["Heading2"],
    fontName="Helvetica-Bold", fontSize=11, leading=13,
    textColor=white, alignment=TA_LEFT,
    spaceBefore=0, spaceAfter=0,
)
sBody = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontName="Helvetica", fontSize=8.5, leading=11,
    textColor=INK, alignment=TA_LEFT, spaceAfter=2,
)
sBodyTight = ParagraphStyle(
    "BodyTight", parent=sBody, fontSize=8, leading=10, spaceAfter=1,
)
sBullet = ParagraphStyle(
    "Bullet", parent=sBody,
    leftIndent=10, bulletIndent=0, spaceAfter=1,
)
sFooter = ParagraphStyle(
    "Footer", parent=styles["Normal"],
    fontName="Helvetica", fontSize=7.5, leading=9,
    textColor=MUTED, alignment=TA_CENTER,
)
sCaption = ParagraphStyle(
    "Caption", parent=styles["Normal"],
    fontName="Helvetica-Oblique", fontSize=7.5, leading=9,
    textColor=MUTED, alignment=TA_CENTER,
)


def header_flowable(width):
    """Dark green branded header bar: logo + title + subtitle."""
    logo_cell = ""
    if os.path.exists(LOGO):
        img = Image(LOGO, width=0.7 * inch, height=0.7 * inch, kind="proportional")
        logo_cell = img

    title_block = [
        Paragraph("OcuTrap R1 &nbsp;&middot;&nbsp; Operation Cheat Sheet", sTitle),
        Paragraph("Buttons, LEDs &amp; device states — keep near the trap.", sSubtitle),
    ]

    tbl = Table(
        [[logo_cell, title_block]],
        colWidths=[0.9 * inch, width - 0.9 * inch],
        rowHeights=[0.85 * inch],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 10),
        ("RIGHTPADDING", (0, 0), (0, 0), 6),
        ("LEFTPADDING", (1, 0), (1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return tbl


def section_header(text, width):
    """A single-row band that acts as a section header."""
    tbl = Table(
        [[Paragraph(text.upper(), sSection)]],
        colWidths=[width],
        rowHeights=[0.22 * inch],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_GREEN),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl


def boxed(flowables, width, pad=6):
    """Wrap content in a subtle rule box."""
    inner = Table(
        [[flowables]], colWidths=[width - 2],
    )
    inner.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("BACKGROUND", (0, 0), (-1, -1), white),
    ]))
    return inner


def first_time_callout(width):
    """Point new users at the Quick Start guide for setup."""
    msg = (
        "<b>First time setting up?</b> &nbsp;"
        "Follow the <b>R1 Quick Start</b> card (in the box) for battery, assembly, "
        "and app pairing. This cheat sheet is for day-to-day operation."
    )
    tbl = Table(
        [[Paragraph(msg, sBodyTight)]],
        colWidths=[width],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_CREAM),
        ("BOX", (0, 0), (-1, -1), 0.5, BRAND_ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tbl


def battery_callout(width):
    """Pack sizes, chargers, and opposite XT30 genders."""
    msg = (
        "<b>Battery (XT30):</b> &nbsp;5200 mAh &mdash; male XT30, <b>1A</b> charger. "
        "&nbsp;10,000 mAh (111 Wh) &mdash; female XT30, <b>2A</b> charger. "
        "Genders are opposite&mdash;do not force. Need the other pack? "
        "Email <b>support@ocutrap.com</b> for PCB/holder swap."
    )
    tbl = Table([[Paragraph(msg, sBodyTight)]], colWidths=[width])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), white),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return tbl


def system_led_table(width):
    """System LED patterns — what the top-of-POD LED is telling you."""
    rows = [
        ("Breathing cyan", "Connected to cloud — operational."),
        ("Fast blinking cyan", "Connecting to the cloud."),
        ("Blinking green", "Searching for cellular signal."),
        ("Blinking magenta", "Firmware update in progress."),
        ("Rapid red SOS", "Firmware crash — contact support if >10 blinks."),
        ("Solid red at boot", "Battery too low (<9.6V). Charge and retry."),
        ("No light", "Off or hibernating. Press Power to wake."),
    ]
    header = [
        Paragraph("<b>Pattern</b>", sBodyTight),
        Paragraph("<b>Meaning</b>", sBodyTight),
    ]
    body = [[Paragraph(f"<b>{p}</b>", sBodyTight), Paragraph(m, sBodyTight)] for p, m in rows]
    data = [header] + body
    tbl = Table(data, colWidths=[1.25 * inch, width - 1.25 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_CREAM),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, RULE),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
    ]))
    return tbl


def buttons_table(width):
    rows = [
        ["Arm", "User Button, then Power Button", "Door must be set open"],
        ["Unarm", "User Button, then Power Button", "From armed state"],
        ["Open door", "User Button, release, then hold 5s", "Blue flashes"],
        ["Close door", "User Button, release, then hold 5s", "Green flashes"],
        ["Power off", "Hold Power Button 3s", "Red blink → solid red → off"],
        ["Reset", "Press Reset once", "Reboots; state preserved"],
    ]
    header = [
        Paragraph("<b>Action</b>", sBodyTight),
        Paragraph("<b>How</b>", sBodyTight),
        Paragraph("<b>Result</b>", sBodyTight),
    ]
    body = [[Paragraph(a, sBodyTight), Paragraph(h, sBodyTight), Paragraph(r, sBodyTight)] for a, h, r in rows]
    data = [header] + body
    tbl = Table(data, colWidths=[0.8 * inch, width - 2.3 * inch, 1.5 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_CREAM),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, RULE),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
    ]))
    return tbl


def status_table(width):
    """Armed-state colors. The color chip shows the real LED color."""
    rows = [
        ("Unarmed & Open", HexColor("#2563EB"), "Solid blue"),
        ("Unarmed & Closed", HexColor("#22C55E"), "Solid green"),
        ("Scouting (app)", HexColor("#2563EB"), "Door open; Scout in app&mdash;no capture"),
        ("Armed", HexColor("#EAB308"), "Solid yellow"),
        ("Armed & Captured", HexColor("#D946EF"), "Solid magenta (animal captured)"),
    ]
    data = [[Paragraph(f"<b>{label}</b>", sBodyTight), "", Paragraph(desc, sBodyTight)] for label, _, desc in rows]
    tbl = Table(data, colWidths=[1.4 * inch, 0.45 * inch, width - 1.85 * inch])
    style = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, RULE),
    ]
    for i, (_, color, _) in enumerate(rows):
        style.append(("BACKGROUND", (1, i), (1, i), color))
    tbl.setStyle(TableStyle(style))
    return tbl


def safety_list():
    items = [
        "Keep fingers clear of the door and motor at all times.",
        "Power off and disconnect the battery before any maintenance.",
        "Wear gloves when approaching a captured animal.",
        "Do not submerge. Avoid freezing conditions (door may stick).",
        "Use only the supplied charger (1A or 2A&mdash;match your pack).",
    ]
    return [Paragraph(f"&bull; {t}", sBodyTight) for t in items]


def build():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    doc = BaseDocTemplate(
        OUTPUT, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="OcuTrap R1 Cheat Sheet",
        author="OcuTrap, Inc.",
    )

    usable_w = PAGE_W - 2 * MARGIN
    usable_h = PAGE_H - 2 * MARGIN

    frame = Frame(
        MARGIN, MARGIN, usable_w, usable_h,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        id="main",
    )
    doc.addPageTemplates([PageTemplate(id="one", frames=[frame])])

    story = []

    story.append(header_flowable(usable_w))
    story.append(Spacer(1, 6))

    # Two-column body: left column (quick start + buttons + safety), right column (sticker + states)
    left_w = usable_w * 0.60
    right_w = usable_w * 0.38
    gutter = usable_w * 0.02

    # --- LEFT COLUMN ---
    left_story = []
    left_story.append(first_time_callout(left_w))
    left_story.append(Spacer(1, 4))
    left_story.append(battery_callout(left_w))
    left_story.append(Spacer(1, 6))

    left_story.append(section_header("System LED (top of POD)", left_w))
    left_story.append(Spacer(1, 3))
    left_story.append(system_led_table(left_w))
    left_story.append(Spacer(1, 6))

    left_story.append(section_header("Buttons &amp; Controls", left_w))
    left_story.append(Spacer(1, 3))
    left_story.append(buttons_table(left_w))
    left_story.append(Spacer(1, 6))

    left_story.append(section_header("Safety", left_w))
    left_story.append(Spacer(1, 3))
    for f in safety_list():
        left_story.append(f)

    # --- RIGHT COLUMN ---
    right_story = []
    right_story.append(section_header("LED Patterns (Inside Sticker)", right_w))
    right_story.append(Spacer(1, 3))
    if os.path.exists(STICKER):
        # Sticker is ~1005x1200 (aspect ~0.84). Scale to fit column width.
        img = Image(STICKER, width=right_w - 4, height=(right_w - 4) * (1200.0 / 1005.0), kind="proportional")
        right_story.append(img)
        right_story.append(Spacer(1, 2))
        right_story.append(Paragraph("Matches the sticker inside every POD.", sCaption))
    else:
        right_story.append(Paragraph("(inside_sticker.png not found)", sCaption))

    right_story.append(Spacer(1, 6))
    right_story.append(section_header("Device State (Solid Colors)", right_w))
    right_story.append(Spacer(1, 3))
    right_story.append(status_table(right_w))

    # Compose columns side by side
    cols = Table(
        [[left_story, "", right_story]],
        colWidths=[left_w, gutter, right_w],
    )
    cols.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(cols)

    story.append(Spacer(1, 8))

    # Footer
    footer_txt = (
        "Docs &amp; videos: <b>docs.ocutrap.com</b> &nbsp; | &nbsp; "
        "Dashboard: <b>base.ocutrap.com</b> &nbsp; | &nbsp; "
        "Support: <b>support@ocutrap.com</b>"
    )
    story.append(Paragraph(footer_txt, sFooter))
    story.append(Paragraph(
        "&copy; OcuTrap, Inc. &middot; 5900 Balcones Drive, Suite 100, Austin, TX 78732 &middot; U.S. Patent No. 12,010,984",
        sFooter,
    ))

    doc.build(story)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"Wrote {OUTPUT} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    build()
