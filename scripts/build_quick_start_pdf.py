#!/usr/bin/env python3
"""
Build OcuTrap Quick Start & Installation Guide as a saddle-stitch booklet PDF.

Layout: Half-letter pages (5.5" x 8.5") — 12 pages total.
Print: 3 sheets, double-sided, fold in half, staple spine.

Usage:
    pip install reportlab Pillow
    python scripts/build_quick_start_pdf.py

Run from the repo root (OcuTrap_Knowledge_Base/).
"""

import os
import sys
import unicodedata
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle, KeepTogether, HRFlowable, Frame, PageTemplate,
    BaseDocTemplate, NextPageTemplate, FrameBreak
)
from reportlab.lib.units import cm
from PIL import Image as PILImage

# --- Paths ---
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(REPO_ROOT, "docs-site", "public", "gitbook-assets")
MANUAL_MEDIA = os.path.join(REPO_ROOT, "..", "manual_unpacked", "word", "media")
# Fallback if run from sandbox
if not os.path.exists(MANUAL_MEDIA):
    MANUAL_MEDIA = ASSETS  # images were copied here with descriptive names
OUTPUT = os.path.join(REPO_ROOT, "OcuTrap_Quick_Start_Guide.pdf")

if len(sys.argv) > 1:
    OUTPUT = sys.argv[1]

VERSION = "v1.0"
HALF_LETTER_W = 5.5 * inch
HALF_LETTER_H = 8.5 * inch

# --- Helpers ---

def find_image(name, fallback_name=None):
    """Find image in ASSETS with Unicode-tolerant matching."""
    for search_name in [name, fallback_name] if fallback_name else [name]:
        if not search_name:
            continue
        direct = os.path.join(ASSETS, search_name)
        if os.path.exists(direct):
            return direct
        # Also check manual media
        direct2 = os.path.join(MANUAL_MEDIA, search_name)
        if os.path.exists(direct2):
            return direct2
        # Fuzzy match
        def norm(s):
            return ''.join(' ' if unicodedata.category(c).startswith('Z') else c for c in s)
        for folder in [ASSETS, MANUAL_MEDIA]:
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    if norm(f) == norm(search_name):
                        return os.path.join(folder, f)
    return None

def safe_image(name, max_w=3.5*inch, max_h=3*inch, fallback=None):
    path = find_image(name, fallback)
    if not path:
        print(f"  MISSING: {name}")
        return None
    try:
        pil = PILImage.open(path)
        if name.endswith('.gif'):
            return None
        w, h = pil.size
        aspect = w / h
        img_w = min(max_w, w)
        img_h = img_w / aspect
        if img_h > max_h:
            img_h = max_h
            img_w = img_h * aspect
        return Image(path, width=img_w, height=img_h)
    except Exception as e:
        print(f"  ERROR: {name}: {e}")
        return None

# --- Styles ---

def make_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'BkTitle', parent=styles['Title'],
        fontSize=22, leading=26, textColor=HexColor('#1B4F72'),
        spaceAfter=4, fontName='Helvetica-Bold', alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'BkSubtitle', parent=styles['Normal'],
        fontSize=11, leading=14, textColor=HexColor('#5D6D7E'),
        spaceAfter=12, fontName='Helvetica', alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'BkSection', parent=styles['Heading1'],
        fontSize=14, leading=18, textColor=HexColor('#1B4F72'),
        spaceBefore=10, spaceAfter=6, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'BkSubSec', parent=styles['Heading2'],
        fontSize=11, leading=14, textColor=HexColor('#2E86C1'),
        spaceBefore=8, spaceAfter=4, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'BkBody', parent=styles['Normal'],
        fontSize=8.5, leading=12, textColor=black,
        spaceAfter=4, fontName='Helvetica', alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        'BkBodyBold', parent=styles['Normal'],
        fontSize=8.5, leading=12, textColor=black,
        spaceAfter=4, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'BkBullet', parent=styles['Normal'],
        fontSize=8.5, leading=12, textColor=black,
        fontName='Helvetica', spaceAfter=2, leftIndent=15, bulletIndent=5
    ))
    styles.add(ParagraphStyle(
        'BkWarn', parent=styles['Normal'],
        fontSize=8, leading=11, textColor=HexColor('#7B241C'),
        fontName='Helvetica-Oblique', spaceAfter=4,
        leftIndent=10, borderPadding=4, backColor=HexColor('#FDEDEC')
    ))
    styles.add(ParagraphStyle(
        'BkCaption', parent=styles['Normal'],
        fontSize=7.5, leading=10, textColor=HexColor('#5D6D7E'),
        alignment=TA_CENTER, spaceAfter=6, fontName='Helvetica-Oblique'
    ))
    styles.add(ParagraphStyle(
        'BkTableH', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=white,
        fontName='Helvetica-Bold', alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'BkTableC', parent=styles['Normal'],
        fontSize=7.5, leading=10, textColor=black, fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        'BkFooter', parent=styles['Normal'],
        fontSize=7, leading=9, textColor=HexColor('#5D6D7E'),
        alignment=TA_CENTER, fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        'BkSmall', parent=styles['Normal'],
        fontSize=7, leading=9, textColor=HexColor('#5D6D7E'),
        fontName='Helvetica', spaceAfter=2
    ))
    return styles

def make_table(headers, rows, col_widths=None):
    s = make_styles()
    header_cells = [Paragraph(h, s['BkTableH']) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(str(c), s['BkTableC']) for c in row])
    if col_widths is None:
        col_widths = [4*inch / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1B4F72')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F2F4F4')]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#BDC3C7')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
    ]))
    return t

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=HexColor('#D5D8DC'), spaceAfter=6, spaceBefore=6)

def bullet(text, s):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", s['BkBullet'])

def numbered(text, n, s):
    return Paragraph(f"<b>{n}.</b> {text}", s['BkBullet'])

def add_img(story, name, caption=None, max_w=3.5*inch, max_h=2.5*inch, fallback=None):
    img = safe_image(name, max_w, max_h, fallback)
    if img:
        story.append(img)
        if caption:
            story.append(Paragraph(caption, make_styles()['BkCaption']))
        return True
    return False


# ========== BUILD DOCUMENT ==========

s = make_styles()
story = []

# ===== PAGE 1: COVER =====
story.append(Spacer(1, 1.2*inch))
add_img(story, "OcuTrap_4228 × 1045_300dpi.png", max_w=3.5*inch, max_h=0.8*inch)
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("OcuTrap R1", s['BkTitle']))
story.append(Paragraph("Installation &amp; User Manual", s['BkSubtitle']))
story.append(Spacer(1, 0.2*inch))
add_img(story, "qr-docs-video-guide.png", max_w=1.2*inch, max_h=1.5*inch)
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("Scan for online docs &amp; video guides", s['BkCaption']))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("PLEASE READ THIS MANUAL FULLY", s['BkBodyBold']))
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph(f"{VERSION}  |  docs.ocutrap.com", s['BkFooter']))
story.append(PageBreak())

# ===== PAGE 2: TABLE OF CONTENTS =====
story.append(Paragraph("Contents", s['BkSection']))
story.append(hr())
toc = [
    "1. Unboxing &amp; Initial Inspection",
    "2. Hardware Setup",
    "    Handle Assembly  |  Door Assembly  |  Motor  |  POD",
    "3. App Setup &amp; Trap Activation",
    "4. Buttons, Arming &amp; Door Control",
    "5. LED Indicators &amp; Status",
    "6. Weather &amp; Maintenance",
    "7. Safety &amp; Battery Precautions",
    "8. Warranty &amp; Compliance",
]
for item in toc:
    story.append(Paragraph(item, s['BkBody']))
story.append(Spacer(1, 0.3*inch))
add_img(story, "DSC03816.JPG", "The OcuTrap R1 fully assembled", max_w=3.5*inch, max_h=2.5*inch)
story.append(PageBreak())

# ===== PAGE 3: UNBOXING + CHARGE + HANDLE =====
story.append(Paragraph("1. Unboxing &amp; Initial Inspection", s['BkSection']))
story.append(Paragraph(
    "Carefully unpack your OcuTrap R1 and check all components are included. "
    "Examine each item for visible damage. If anything is missing or damaged, halt installation and "
    "contact <b>support@ocutrap.com</b> with your trap ID.", s['BkBody']))
add_img(story, "cage-unboxed.png", "Cage", max_w=2*inch, max_h=1.2*inch)
add_img(story, "parts-box.png", "Parts box", max_w=2*inch, max_h=1.2*inch)
story.append(hr())

story.append(Paragraph("2. Hardware Setup", s['BkSection']))
story.append(Paragraph(
    "First, fully charge the blue lithium-ion battery until the charger light turns green (4-6 hours). "
    "Use only the included charger. Assembly has four sections: <b>Handle</b>, <b>Door</b>, <b>POD</b>, and <b>App Setup</b>.", s['BkBody']))

story.append(Paragraph("Section 1: Handle Assembly", s['BkSubSec']))
story.append(Paragraph("Components needed:", s['BkBodyBold']))
for item in [
    "4x 3\" bolts, 1x handle guard, 1x tube, 4x washers",
    "2x upper plastic spacers, 2x lower handle spacers",
    "2x in-trap brackets (press-fit nut), 2x top metal brackets, 1x nut driver",
]:
    story.append(bullet(item, s))

add_img(story, "handle-assembly-parts.png", max_w=1.8*inch, max_h=1.8*inch)

story.append(Paragraph("Steps:", s['BkBodyBold']))
for i, step in enumerate([
    "Center handle guard on trap. Insert top handle pieces into guard holes.",
    "Slide tube between guards; ensure centered.",
    "Place bracket (press-fit nut) inside trap; hand-tighten bolts.",
    "Fully tighten bolts from top with nut driver.",
], 1):
    story.append(numbered(step, i, s))
story.append(PageBreak())

# ===== PAGE 5: DOOR ASSEMBLY =====
story.append(Paragraph("Section 2: Door Assembly", s['BkSubSec']))
story.append(Paragraph("<b>Door components:</b> 2x brackets, 2x black spacers, 2x black capped nuts, "
    "1x metal door, 1x 12\" rod, 1x nut driver, 1x nut assembly tool", s['BkBody']))
story.append(Paragraph("<b>Motor components:</b> 1x motor, 2x pins, 2x clevises, 1x top motor bracket, "
    "2x washers, 2x 1\" bolts", s['BkBody']))

add_img(story, "door-parts.png", "Door components", max_w=2.5*inch, max_h=1.3*inch)

story.append(Paragraph("Door Assembly:", s['BkBodyBold']))
for i, step in enumerate([
    "Thread the metal rod through the oval slot in the bracket on the door.",
    "On each end: place black spacer, secure with capped nut, tighten with nut driver.",
], 1):
    story.append(numbered(step, i, s))

add_img(story, "door-rod-assembly.png", "Rod assembly", max_w=3.2*inch, max_h=1.2*inch)

story.append(Paragraph("Motor Assembly:", s['BkBodyBold']))
for i, step in enumerate([
    "Install top bracket with washers and bolts. Tighten with nut driver.",
    "Use pins and clevises to secure motor to door at both attachment points.",
    "Feed the cable through the metal handle.",
    "Verify all components are secure; check door moves smoothly.",
], 1):
    story.append(numbered(step, i, s))

add_img(story, "motor-assembly.png", "Motor bracket installed", max_w=1.5*inch, max_h=1.5*inch)
story.append(hr())

story.append(Paragraph("Section 3: POD Assembly", s['BkSubSec']))
for i, step in enumerate([
    "Ensure battery is fully charged (4-6 hours).",
    "Slide the POD down the rails on the trap.",
    "Attach motor wire to POD using the locking screw connector.",
    "Use the top latch to secure the POD in place.",
    "Insert battery, tuck cables along edges, close latch fully for waterproofness.",
], 1):
    story.append(numbered(step, i, s))
story.append(hr())

story.append(Paragraph("3. App Setup &amp; Trap Activation", s['BkSection']))
story.append(Paragraph(
    "Go to <b>base.ocutrap.com</b> and create an account. Download the mobile app:", s['BkBody']))

story.append(Paragraph("Activation Steps:", s['BkBodyBold']))
for i, step in enumerate([
    "Create an account on the app or website.",
    "Open the POD and locate the serial number on top.",
    "In the app: Account (top right) &rarr; Add Trap.",
    "Enter the serial number or scan QR code inside POD.",
    "Follow prompts to enable your subscription.",
    "The new trap appears on your dashboard.",
], 1):
    story.append(numbered(step, i, s))

story.append(Paragraph("Initial Hardware Check:", s['BkBodyBold']))
for i, step in enumerate([
    "Connect charged battery and power on.",
    "Wait for breathing cyan LED (connected, up to 10 min).",
    "Open the app and select <b>Arm</b> to initiate readiness.",
], 1):
    story.append(numbered(step, i, s))
story.append(PageBreak())

# ===== PAGE 7: BUTTONS, ARMING, DOOR =====
story.append(Paragraph("4. Buttons, Arming &amp; Door Control", s['BkSection']))
add_img(story, "pod-buttons-diagram.png", "POD button layout", max_w=3.5*inch, max_h=1.5*inch)

story.append(Paragraph("Arming / Unarming", s['BkSubSec']))
story.append(make_table(
    ["Action", "Steps", "LED"],
    [["Arm", "Press User, then Power. Door must be open.", "Flashing Yellow"],
     ["Unarm", "Press User, then Power again.", "Flashing White"]],
    col_widths=[0.8*inch, 2.2*inch, 1*inch]
))
story.append(Spacer(1, 4))

story.append(Paragraph("Door Control", s['BkSubSec']))
story.append(make_table(
    ["Action", "Steps", "LED"],
    [["Open Door", "Press User, release, press+hold 5 sec", "Blue flashes"],
     ["Close Door", "Press User, release, press+hold 5 sec", "Green flashes"]],
    col_widths=[0.8*inch, 2.2*inch, 1*inch]
))
story.append(Spacer(1, 4))

story.append(Paragraph("Other Controls", s['BkSubSec']))
story.append(make_table(
    ["Action", "Steps"],
    [["Reset", "Press Reset button once (retains config)"],
     ["Power Off", "Hold PWR button for 3 seconds"],
     ["Wake", "Press Power button"]],
    col_widths=[1*inch, 3*inch]
))
story.append(PageBreak())

# ===== PAGE 8: LED INDICATORS + STATUS =====
story.append(Paragraph("5. LED Indicators &amp; Status", s['BkSection']))

story.append(Paragraph("System LED (top of POD)", s['BkSubSec']))
story.append(make_table(
    ["Pattern", "Meaning"],
    [["Breathing Cyan", "Connected to cloud - operational"],
     ["Blinking Cyan", "Connecting to cloud"],
     ["Blinking Magenta", "Firmware update in progress"],
     ["Blinking Green", "Searching for cellular connection"],
     ["Flashing Red SOS", "Device needs attention - contact support"],
     ["Blinking Red", "Battery too low for operation"],
     ["No LED", "Powered off, hibernation, or needs power check"]],
    col_widths=[1.2*inch, 2.8*inch]
))
story.append(Spacer(1, 6))

story.append(Paragraph("User Button LED", s['BkSubSec']))
story.append(make_table(
    ["Color", "State"],
    [["Solid Blue", "Unarmed, door open"],
     ["Solid Green", "Unarmed, door closed"],
     ["Solid Yellow", "Armed"],
     ["Solid Magenta", "Armed + captured"]],
    col_widths=[1.2*inch, 2.8*inch]
))

story.append(Spacer(1, 6))
story.append(Paragraph("Unarmed Hibernation", s['BkSubSec']))
story.append(Paragraph(
    "By default, the trap enters hibernation after ~2 hours unarmed. "
    "Adjust in Settings &rarr; More Settings &rarr; Unarmed Sleep Mode. "
    "Disabling increases battery consumption.", s['BkBody']))
story.append(PageBreak())

# ===== PAGE 9: WEATHER + MAINTENANCE =====
story.append(Paragraph("6. Weather &amp; Maintenance", s['BkSection']))
story.append(Paragraph(
    "OcuTrap operates best between 0-40C (32-104F). The enclosure is weatherproof but not submersion-rated. "
    "Extreme temperatures reduce battery life; freezing may affect the door mechanism.", s['BkBody']))

story.append(Paragraph("Routine Maintenance Checklist", s['BkSubSec']))
story.append(Paragraph("Run after every capture and after harsh weather:", s['BkBody']))

story.append(make_table(
    ["Area", "Action"],
    [["Camera/sensor lens", "Wipe with soft, lint-free cloth"],
     ["Exterior", "Wipe with damp cloth"],
     ["Interior", "Remove debris, wipe if needed"],
     ["Battery", "Full charge before use; check terminals"],
     ["Door &amp; motor", "Test open/close; confirm motor runs"],
     ["Seals", "Check for cracks; inspect after bad weather"]],
    col_widths=[1.2*inch, 2.8*inch]
))
story.append(Spacer(1, 4))
story.append(Paragraph(
    '<b>Safety:</b> Power off the trap and unplug the battery before maintenance.', s['BkWarn']))
story.append(PageBreak())

# ===== PAGE 10: SAFETY + BATTERY =====
story.append(Paragraph("7. Safety &amp; Battery Precautions", s['BkSection']))

story.append(Paragraph(
    '<b>Warning: Risk of Finger Injury.</b> The motorized door and spring mechanism can cause '
    'serious injury. Keep hands clear of the door path at all times. Power off before maintenance. '
    'Do not allow children to operate the trap.', s['BkWarn']))

story.append(Paragraph("Battery Safety", s['BkSubSec']))
for item in [
    "Do not expose to fire, water, or excessive heat.",
    "Avoid short-circuiting terminals.",
    "Use only the provided charger.",
    "Handle carefully - do not puncture or impact.",
    "Keep out of reach of children.",
    "Charge in a cool, dry place (0-40C).",
    "Store at 40-60% charge for long-term storage.",
    "Dispose per federal, state, and local regulations.",
]:
    story.append(bullet(item, s))

story.append(Paragraph(
    "<b>Battery specs:</b> 12V Li-ion, 800+ charging cycles, 3+ weeks runtime, 4-6 hour charge time.", s['BkBody']))
story.append(hr())

story.append(Paragraph("8. Warranty &amp; Compliance", s['BkSection']))

story.append(Paragraph("Hardware Warranty (12 Months)", s['BkSubSec']))
story.append(Paragraph(
    "OcuTrap warrants the R1 hardware against defects in materials and workmanship for 12 months "
    "from original purchase. Covers repair or replacement at OcuTrap's discretion.", s['BkBody']))
story.append(Paragraph("<b>Not covered:</b> improper installation, misuse, third-party modifications, "
    "environmental damage, normal wear, non-OcuTrap parts.", s['BkBody']))
story.append(Paragraph(
    "To claim: contact <b>support@ocutrap.com</b> with proof of purchase and issue description.", s['BkBody']))

story.append(Paragraph("FCC Compliance", s['BkSubSec']))
story.append(Paragraph(
    "This device complies with Part 15 of FCC Rules. FCC ID: <b>2AEMI-B404X</b>. "
    "Maintain 20cm minimum distance from body. Changes not approved by Particle Industries "
    "may void authority to operate.", s['BkBody']))

story.append(Paragraph("Laser Safety", s['BkSubSec']))
story.append(Paragraph(
    "Contains Class 1 laser (IEC 60825-1:2014). Do not increase power or focus the beam.", s['BkBody']))
add_img(story, "laser-safety-label.png", max_w=1.5*inch, max_h=0.7*inch)

story.append(Paragraph(
    "OcuTrap relies on third-party wireless service subject to transmission and coverage limitations.", s['BkSmall']))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Warranty governed by Texas law. Full terms at <b>ocutrap.com/pages/warranty</b>.", s['BkSmall']))
story.append(PageBreak())

# ===== PAGE 12: BACK COVER =====
story.append(Spacer(1, 1.5*inch))
add_img(story, "OcuTrap_4228 × 1045_300dpi.png", max_w=3*inch, max_h=0.7*inch)
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("<b>OcuTrap, Inc.</b>", ParagraphStyle(
    'BackAddr', parent=s['BkBody'], alignment=TA_CENTER, fontSize=9)))
story.append(Paragraph("5900 Balcones Drive, Suite 100<br/>Austin, Texas 78732, USA", ParagraphStyle(
    'BackAddr2', parent=s['BkBody'], alignment=TA_CENTER, fontSize=8)))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("OcuTrap.com  |  support@ocutrap.com", ParagraphStyle(
    'BackURL', parent=s['BkBody'], alignment=TA_CENTER, fontSize=9, textColor=HexColor('#2E86C1'))))
story.append(Spacer(1, 0.3*inch))
add_img(story, "qr-support.png", max_w=1*inch, max_h=1*inch)
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<i>U.S. Patent No. 12,010,984</i>", ParagraphStyle(
    'Patent', parent=s['BkBody'], alignment=TA_CENTER, fontSize=7.5, textColor=HexColor('#5D6D7E'))))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(f"{VERSION}  |  April 2026", ParagraphStyle(
    'Ver', parent=s['BkBody'], alignment=TA_CENTER, fontSize=7.5, textColor=HexColor('#5D6D7E'))))
story.append(Paragraph("&copy; OcuTrap, Inc. All Rights Reserved.", ParagraphStyle(
    'Copy', parent=s['BkBody'], alignment=TA_CENTER, fontSize=7, textColor=HexColor('#999999'))))


# ========== BUILD ==========

print("Building Quick Start Guide booklet PDF...")

def page_footer(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont('Helvetica', 6.5)
    canvas_obj.setFillColor(HexColor('#999999'))
    page_num = canvas_obj.getPageNumber()
    if page_num > 1 and page_num < 12:  # skip cover and back
        canvas_obj.drawCentredString(HALF_LETTER_W/2, 0.35*inch,
            f"OcuTrap R1 Quick Start Guide  |  {page_num}")
    canvas_obj.restoreState()

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=(HALF_LETTER_W, HALF_LETTER_H),
    rightMargin=0.5*inch,
    leftMargin=0.5*inch,
    topMargin=0.5*inch,
    bottomMargin=0.5*inch,
    title="OcuTrap R1 Quick Start Guide",
    author="OcuTrap, Inc.",
    subject="Installation & User Manual",
)

doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
print(f"PDF saved to: {OUTPUT}")
print(f"Total pages: {doc.page}")
print(f"\nPrint instructions:")
print(f"  - Print on US Letter paper, double-sided (flip on short edge)")
print(f"  - Fold all 3 sheets in half together")
print(f"  - Staple along the spine (saddle-stitch)")
print(f"  - Place in box with trap")
