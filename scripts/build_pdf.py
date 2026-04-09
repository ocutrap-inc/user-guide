#!/usr/bin/env python3
"""
Build OcuTrap Knowledge Base PDF with images from gitbook-assets.

Usage:
    pip install reportlab Pillow
    python scripts/build_pdf.py

Run from the repo root (OcuTrap_Knowledge_Base/).
Output: OcuTrap_Knowledge_Base.pdf in the repo root.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle, KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import cm
from PIL import Image as PILImage

# Resolve paths relative to the repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(REPO_ROOT, "docs-site", "public", "gitbook-assets")
OUTPUT = os.path.join(REPO_ROOT, "OcuTrap_Knowledge_Base.pdf")

# Allow overriding output path via CLI argument
if len(sys.argv) > 1:
    OUTPUT = sys.argv[1]

VERSION = "v1.0"

# --- Helpers ---

def img_path(name):
    """Find image by name, handling Unicode space variants in filenames."""
    direct = os.path.join(ASSETS, name)
    if os.path.exists(direct):
        return direct
    # Try fuzzy matching - replace regular spaces with Unicode variants
    for f in os.listdir(ASSETS):
        # Normalize both strings by replacing all unicode spaces with regular spaces
        import unicodedata
        def normalize_spaces(s):
            return ''.join(' ' if unicodedata.category(c).startswith('Z') else c for c in s)
        if normalize_spaces(f) == normalize_spaces(name):
            return os.path.join(ASSETS, f)
    return direct  # fallback

def safe_image(name, max_width=5*inch, max_height=4*inch):
    """Return an Image flowable scaled to fit, or None if file missing/broken."""
    path = img_path(name)
    if not os.path.exists(path):
        print(f"  MISSING: {name}")
        return None
    try:
        pil = PILImage.open(path)
        w, h = pil.size
        # Skip tiny images or gifs that won't render well
        if name.endswith('.gif'):
            print(f"  SKIP GIF: {name}")
            return None
        # Convert HEIC or unsupported to JPEG for reportlab
        if name.upper().endswith('.HEIC'):
            print(f"  SKIP HEIC: {name}")
            return None
        # Calculate scale
        aspect = w / h
        img_w = min(max_width, w)
        img_h = img_w / aspect
        if img_h > max_height:
            img_h = max_height
            img_w = img_h * aspect
        return Image(path, width=img_w, height=img_h)
    except Exception as e:
        print(f"  ERROR loading {name}: {e}")
        return None

# --- Styles ---

def make_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'DocTitle', parent=styles['Title'],
        fontSize=28, leading=34, textColor=HexColor('#1B4F72'),
        spaceAfter=6, fontName='Helvetica-Bold', alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontSize=14, leading=18, textColor=HexColor('#5D6D7E'),
        spaceAfter=20, fontName='Helvetica', alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'SectionHeader', parent=styles['Heading1'],
        fontSize=22, leading=28, textColor=HexColor('#1B4F72'),
        spaceBefore=24, spaceAfter=12, fontName='Helvetica-Bold',
        borderPadding=(0, 0, 4, 0),
    ))
    styles.add(ParagraphStyle(
        'SubSection', parent=styles['Heading2'],
        fontSize=16, leading=20, textColor=HexColor('#2E86C1'),
        spaceBefore=16, spaceAfter=8, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'SubSubSection', parent=styles['Heading3'],
        fontSize=13, leading=16, textColor=HexColor('#2874A6'),
        spaceBefore=12, spaceAfter=6, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=10.5, leading=15, textColor=black,
        spaceAfter=8, fontName='Helvetica', alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        'BodyBold', parent=styles['Normal'],
        fontSize=10.5, leading=15, textColor=black,
        spaceAfter=8, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'Tip', parent=styles['Normal'],
        fontSize=10, leading=14, textColor=HexColor('#1A5276'),
        spaceAfter=8, fontName='Helvetica-Oblique',
        leftIndent=20, borderPadding=8,
        backColor=HexColor('#EBF5FB'),
    ))
    styles.add(ParagraphStyle(
        'Warning', parent=styles['Normal'],
        fontSize=10, leading=14, textColor=HexColor('#7B241C'),
        spaceAfter=8, fontName='Helvetica-Oblique',
        leftIndent=20, borderPadding=8,
        backColor=HexColor('#FDEDEC'),
    ))
    styles.add(ParagraphStyle(
        'Caption', parent=styles['Normal'],
        fontSize=9, leading=12, textColor=HexColor('#5D6D7E'),
        alignment=TA_CENTER, spaceAfter=12, fontName='Helvetica-Oblique'
    ))
    styles.add(ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontSize=10, leading=13, textColor=white,
        fontName='Helvetica-Bold', alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontSize=9.5, leading=13, textColor=black,
        fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        'BulletText', parent=styles['Normal'],
        fontSize=10.5, leading=15, textColor=black,
        fontName='Helvetica', spaceAfter=4, leftIndent=20, bulletIndent=8
    ))
    styles.add(ParagraphStyle(
        'QA_Q', parent=styles['Normal'],
        fontSize=10.5, leading=15, textColor=HexColor('#1B4F72'),
        fontName='Helvetica-Bold', spaceAfter=2, spaceBefore=8
    ))
    styles.add(ParagraphStyle(
        'QA_A', parent=styles['Normal'],
        fontSize=10.5, leading=15, textColor=black,
        fontName='Helvetica', spaceAfter=8, leftIndent=15
    ))
    return styles

def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    s = make_styles()
    header_cells = [Paragraph(h, s['TableHeader']) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(str(c), s['TableCell']) for c in row])

    if col_widths is None:
        col_widths = [6.5*inch / len(headers)] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1B4F72')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#FAFAFA')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F2F4F4')]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#BDC3C7')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    return t

def hr():
    return HRFlowable(width="100%", thickness=1, color=HexColor('#D5D8DC'), spaceAfter=12, spaceBefore=12)

def add_image(story, name, caption=None, max_w=5*inch, max_h=4*inch):
    img = safe_image(name, max_w, max_h)
    if img:
        story.append(Spacer(1, 6))
        story.append(img)
        if caption:
            story.append(Paragraph(caption, s['Caption']))
        else:
            story.append(Spacer(1, 6))
        return True
    return False

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", s['BulletText'])

def numbered(text, n):
    return Paragraph(f"<b>{n}.</b> {text}", s['BulletText'])

# --- Build Document ---

s = make_styles()
story = []

# ==================== COVER PAGE ====================
story.append(Spacer(1, 2*inch))

# Logo
logo = safe_image("OcuTrap_4228 × 1045_300dpi.png", max_width=5*inch, max_height=1.5*inch)
if logo:
    story.append(logo)
    story.append(Spacer(1, 0.5*inch))

story.append(Paragraph("OcuTrap Knowledge Base", s['DocTitle']))
story.append(Paragraph("Complete User Guide &amp; Reference &mdash; Smart Wildlife Trap System", s['DocSubtitle']))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("www.ocutrap.com", s['DocSubtitle']))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(f"{VERSION}  |  April 2026", s['DocSubtitle']))
story.append(Spacer(1, 0.5*inch))

# Product image on cover
prod_img = safe_image("DSC03816.JPG", max_width=4.5*inch, max_height=3*inch)
if prod_img:
    story.append(prod_img)

story.append(PageBreak())

# ==================== TABLE OF CONTENTS (manual) ====================
story.append(Paragraph("Table of Contents", s['SectionHeader']))
story.append(hr())

toc_items = [
    ("1. Getting Started", [
        "Introduction", "Hardware Setup", "Video Assembly Guide", "Hardware Features",
        "Technical Specifications", "The OcuTrap App", "Settings Reference",
        "Tips and Tricks", "Trap Settings", "Maintenance", "LED Guide", "Battery Overview"
    ]),
    ("2. Frequently Asked Questions", [
        "Sharing Traps", "Common Questions", "Safe Mode", "Battery FAQ",
        "Updating Firmware", "Camera &amp; Images", "GPS",
        "Weather &amp; Environmental Guidelines", "Cold Weather Guide",
        "Power Modes", "Accessory Port"
    ]),
    ("3. Troubleshooting", [
        "Common Issues", "Trap Not Sending Commands", "Motor Connection Issues",
        "Condensation on the Camera"
    ]),
    ("4. Support", [
        "Contact Us", "Bug Reporting", "Safety Information",
        "Purchases", "Nonprofit and 501(c) Program"
    ]),
    ("5. Account &amp; Billing", [
        "Billing Overview", "Changing Your Payment Method",
        "Managing Subscriptions", "Resetting Password", "Account Deletion"
    ]),
    ("6. Legal &amp; Compliance", ["Warranty Information", "Legal Disclaimers"]),
    ("7. Device Management", ["Selling or Transferring a Trap", "Deleting a Trap"]),
    ("8. Appendix &amp; Resources", [
        "Media Kit", "Testimonials", "Case Study", "Updates", "OcuTrap in the News"
    ]),
]

for section, items in toc_items:
    story.append(Paragraph(f"<b>{section}</b>", s['Body']))
    for item in items:
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&bull; {item}", ParagraphStyle(
            'TOCItem', parent=s['Body'], fontSize=10, leading=14, textColor=HexColor('#5D6D7E')
        )))

story.append(PageBreak())

# ==================== 1. GETTING STARTED ====================
story.append(Paragraph("1. Getting Started", s['SectionHeader']))
story.append(hr())

# -- Introduction --
story.append(Paragraph("Introduction", s['SubSection']))
add_image(story, "OcuTrap_4228 × 1045_300dpi.png", max_w=4*inch, max_h=1*inch)
story.append(Paragraph(
    "The OcuTrap is an innovative smart wildlife trap that transforms how traps are monitored, managed, and controlled. "
    "Whether you are a wildlife professional, pest control operator, researcher, or landowner, OcuTrap brings cutting-edge "
    "technology to humane animal management.", s['Body']))
story.append(Paragraph("<b>Key Benefits:</b>", s['Body']))
for b in [
    "Significant time and cost savings through reduced trap checks",
    "Instant mobile alerts the moment a capture occurs",
    "Smart control features for precise, species-selective animal capture",
    "Remote operation capability to minimize on-site visits and injury risks",
    "Humane design that prioritizes animal welfare"
]:
    story.append(bullet(b))
story.append(hr())

# -- Hardware Setup --
story.append(Paragraph("Hardware Setup", s['SubSection']))
story.append(Paragraph(
    '<i>Video Tutorial: A step-by-step hardware setup video is available at docs.ocutrap.com</i>', s['Tip']))

story.append(Paragraph(
    "Setting up your OcuTrap involves unboxing and assembling the cage, door mechanism, handle, and POD "
    "(the smart electronics unit). Follow these steps carefully for a successful installation.", s['Body']))

story.append(Paragraph("Step 1: Battery Preparation", s['SubSubSection']))
story.append(Paragraph(
    "Charge the blue lithium-ion battery using the included charger until the indicator light turns green. "
    "This typically takes 4-6 hours from a full drain. The charger LED shows red while charging and green when complete.", s['Body']))

story.append(Paragraph("Step 2: Door Assembly", s['SubSubSection']))
for b in [
    "Thread the metal rod through the top bracket of the cage frame",
    "Add spacers and capped nuts to secure the rod in place",
    "Install the linear motor using pins and clevises to connect the motor arm to the door",
]:
    story.append(bullet(b))
# Images for door assembly
add_image(story, "unknown (7).png", "Door assembly components", max_w=4*inch, max_h=3*inch)
story.append(Paragraph(
    '<i>Tip: If the pin and clevis don\'t fit easily into the motor connector, the motor may be fully retracted. '
    'Power on the OcuTrap and press "Close" to extend the motor, making assembly easier.</i>', s['Tip']))

story.append(Paragraph("Step 3: Handle Setup", s['SubSubSection']))
story.append(Paragraph(
    "Gather the 4 three-inch bolts, handle guard, tube, washers, 2 top metal brackets, plastic spacers, "
    "and internal trap brackets. Assemble the handle onto the top of the cage frame following the included diagram.", s['Body']))
add_image(story, "image (28).png", "Handle assembly", max_w=4*inch, max_h=3*inch)

story.append(Paragraph("Step 4: POD Installation", s['SubSubSection']))
for b in [
    "Slide the POD down the rails on top of the cage",
    "Attach the retaining clip to secure the POD",
    "Connect the motor wire using the locking screw connector",
    "Attach the door latch",
    "Insert the charged battery and close the POD enclosure",
]:
    story.append(bullet(b))
add_image(story, "Use the nut driver to mount the top motor bracket with the bolt and washer.png",
          "Motor bracket mounting", max_w=4*inch, max_h=3*inch)
add_image(story, "unknown (5).png", "POD installation", max_w=4*inch, max_h=3*inch)
add_image(story, "image (25).png", "Top view of POD", max_w=3*inch, max_h=2.5*inch)
add_image(story, "image (27).png", "Inside trap view", max_w=3*inch, max_h=2.5*inch)

story.append(Paragraph(
    '<b>Warning:</b> Ensure both latches are fully closed and the waterproof knob is tightened '
    'to protect the electronics from moisture.', s['Warning']))

story.append(Paragraph("Step 5: Software Setup", s['SubSubSection']))
for i, step in enumerate([
    "Create an account at base.ocutrap.com",
    "Locate your POD serial number printed on the top of the POD unit",
    "Go to Account &rarr; Add Trap and enter the serial number",
    "Your new trap will appear on the dashboard, ready to configure",
], 1):
    story.append(numbered(step, i))

add_image(story, "image.png", "Software setup screen", max_w=4*inch, max_h=3*inch)
add_image(story, "Screenshot 2025-12-17 at 10.26.40 AM.png", "Account setup", max_w=4*inch, max_h=3*inch)

story.append(Spacer(1, 12))
add_image(story, "DSC03816.JPG", "The OcuTrap hardware fully assembled", max_w=5*inch, max_h=3.5*inch)
story.append(hr())

# -- Video Assembly --
story.append(Paragraph("Video Assembly Guide", s['SubSection']))
story.append(Paragraph(
    '<i>Video Tutorial: A comprehensive step-by-step assembly video is available at docs.ocutrap.com</i>', s['Tip']))
story.append(Paragraph(
    "The video walkthrough covers all assembly steps: battery preparation, door assembly with rod/washers/springs/nuts, "
    "motor attachment with pins and clevises, and POD assembly with battery connection and mounting.", s['Body']))
story.append(hr())

# -- Hardware Features --
story.append(Paragraph("Hardware Features", s['SubSection']))
story.append(Paragraph(
    "The OcuTrap R1 packs a full suite of smart hardware into a rugged, field-ready enclosure.", s['Body']))

features = [
    ("<b>Connectivity:</b> 4G LTE cellular networks with nationwide multi-carrier coverage. Automatic network selection and fallback."),
    ("<b>Camera:</b> Automatic night vision with IR LEDs. Adjustable image quality across 6 resolution sizes (QVGA to UXGA). Image rotation (0, 90, 180, 270 degrees). Configurable time-lapse photography."),
    ("<b>Door:</b> Linear motor with closing speed under 0.5 seconds and opening speed under 1 second. Remote and manual control. Enhanced door closing option for secure locking."),
    ("<b>Location:</b> Integrated GPS module with satellite positioning. Battery-optimized updates every 8 hours by default. Map view in the app."),
    ("<b>Sensors:</b> Time-of-Flight (ToF) distance detection for precise triggering. Temperature and humidity monitoring. Ambient light detection for automatic day/night camera switching. Accelerometer for tilt detection."),
    ("<b>Battery:</b> 12V lithium-ion rechargeable. 10,000 mAh capacity for 3+ weeks runtime (5,000 mAh variant for Canada). Low battery alerts at 20% and 10%."),
    ("<b>Accessory Port:</b> 12V output port for external devices such as buzzers, solenoids, lure dispensers, or vaccine feeders. Configurable 0-30 second activation timer. 3.0A maximum continuous current."),
    ("<b>Smart Detection:</b> Dual-zone verification system to reduce false triggers. Rain and debris filtering. Consecutive reading requirements before capture activation. Pre-capture notification alerts."),
]
for f in features:
    story.append(bullet(f))
story.append(hr())

# -- Technical Specifications --
story.append(Paragraph("Technical Specifications", s['SubSection']))
story.append(make_table(
    ["Specification", "Details"],
    [
        ["Dimensions", "10\" W x 12\" H x 32\" L"],
        ["Weight", "24 lbs (complete unit)"],
        ["Target Species", "5-25 lb animals"],
        ["Trap Compatibility", "Tomahawk-style trap frames"],
        ["Door Close Speed", "&lt; 0.5 seconds"],
        ["Door Open Speed", "&lt; 1 second"],
        ["Battery", "KBT 12V Li-ion - 10 Ah (std) / 5 Ah (Canada)"],
        ["Operating Voltage", "7.0-15.0 V"],
        ["Runtime", "3+ weeks per charge (usage dependent)"],
        ["Connectivity", "4G LTE cellular, multi-network"],
        ["GPS Updates", "Default every 8 hours"],
        ["Sensor", "VL53L1X ToF - 0-4 m range, 250 mm default"],
        ["Camera Resolution", "QVGA to UXGA (6 sizes)"],
        ["IR LEDs", "Automatic; 0-100% brightness control"],
        ["Operating Temp", "-10C to 45C"],
        ["Environment", "Outdoor field deployment; weatherproof"],
    ],
    col_widths=[2.5*inch, 4*inch]
))
story.append(hr())

# -- The OcuTrap App --
story.append(Paragraph("The OcuTrap App", s['SubSection']))
story.append(Paragraph(
    "The OcuTrap app is your command center for managing traps, viewing captures, and configuring settings. "
    "Create your account at base.ocutrap.com/signuplogin. The mobile app is available for both iOS (App Store) "
    "and Android (Google Play).", s['Body']))

# App store badges
add_image(story, "Screenshot 2025-02-11 at 6.55.09 PM.png", "iOS App Store", max_w=1.5*inch, max_h=0.6*inch)
add_image(story, "Screenshot 2025-02-11 at 6.58.10 PM.png", "Google Play Store", max_w=1.5*inch, max_h=0.6*inch)

story.append(Paragraph("Adding a Trap to Your Account", s['SubSubSection']))
for i, step in enumerate([
    "Log into your account at OcuTrap.com",
    "Locate the serial number printed on top of your POD",
    "Navigate to Account &rarr; Add Trap",
    "Enter the serial number and complete the process",
    "Your new trap appears on the main dashboard",
], 1):
    story.append(numbered(step, i))
add_image(story, "image (2) (1).png", "Add trap screen", max_w=2.5*inch, max_h=3*inch)
add_image(story, "image (3).png", "Serial number entry", max_w=2.5*inch, max_h=3*inch)

story.append(Paragraph("Open &amp; Closed Button", s['SubSubSection']))
story.append(Paragraph(
    "The Open/Close button controls the trap door remotely. <b>Open</b> lifts the door for resetting or allowing "
    "an animal to exit. <b>Close</b> shuts and locks the door. The app always displays the latest reported door state.", s['Body']))

story.append(Paragraph("Arm &amp; Un-arm Button", s['SubSubSection']))
story.append(Paragraph("The trap operates in three distinct states:", s['Body']))
for b in [
    "<b>Armed:</b> Trap set to capture. Door must be manually opened first. Enters low-power mode with periodic updates.",
    "<b>Monitoring:</b> For scouting without closing the door. Sends pre-capture and trigger alerts but does not close the door.",
    "<b>Unarmed:</b> Standby mode. Listens for commands but is not set to capture.",
]:
    story.append(bullet(b))

story.append(Paragraph("Interface Views", s['SubSubSection']))
for b in [
    "<b>Feed View:</b> Default view showing your trap activity feed",
    "<b>Map View:</b> Shows geographical locations of all traps",
]:
    story.append(bullet(b))

story.append(Paragraph("Notification Settings", s['SubSubSection']))
story.append(Paragraph("Three notification types keep you informed:", s['Body']))
for b in [
    "<b>Error:</b> Device failures and critical issues",
    "<b>Alert:</b> Important updates (battery, temperature, connection)",
    "<b>Capture:</b> Successful capture notifications with images",
]:
    story.append(bullet(b))
story.append(Paragraph("Each type can be set to: No notification, Email only, Push notification only, or Push + Email.", s['Body']))

story.append(Paragraph("Trap Control Panel", s['SubSubSection']))
add_image(story, "image (29).png", "Trap Control Panel", max_w=4*inch, max_h=3.5*inch)
story.append(Paragraph("The control panel provides detailed device information and remote actions:", s['Body']))
for b in [
    "<b>Power:</b> Battery type and current voltage",
    "<b>Device:</b> Firmware version and temperature",
    "<b>Network:</b> Signal quality, carrier, strength, and last activity time",
    "<b>Remote Actions:</b> Request data update, send audible buzz, reboot device, enter hibernation",
]:
    story.append(bullet(b))

story.append(Paragraph("Logs", s['SubSubSection']))
story.append(Paragraph(
    "The logs section tracks the complete history of actions, events, and errors for each trap. "
    "Essential for troubleshooting issues and monitoring trap performance over time.", s['Body']))

story.append(Paragraph("Deleting an Image", s['SubSubSection']))
story.append(Paragraph(
    "Images can be deleted from the gallery. Note: this action is permanent and cannot be undone.", s['Body']))
add_image(story, "Screenshot 2025-12-28 at 3.00.32 PM.png", "Select image to delete", max_w=3.5*inch, max_h=3*inch)
add_image(story, "Screenshot 2025-12-28 at 3.00.37 PM.png", "Confirm deletion", max_w=3.5*inch, max_h=3*inch)
story.append(hr())

# -- Settings Reference --
story.append(Paragraph("Settings Reference", s['SubSection']))
add_image(story, "image (30).png", "Settings screen", max_w=4*inch, max_h=3.5*inch)

story.append(Paragraph("Capture &amp; Detection", s['SubSubSection']))
story.append(make_table(
    ["Setting", "Range / Default"],
    [["Capture Distance", "125-1000 mm (default: 250 mm)"],
     ["Pre-Capture Alerts", "On / Off (default: On)"]],
    col_widths=[3*inch, 3.5*inch]
))
story.append(Spacer(1, 8))

story.append(Paragraph("Camera", s['SubSubSection']))
story.append(make_table(
    ["Setting", "Range / Default"],
    [["Time-Lapse Interval", "0-24 hours (default: 6 hours)"],
     ["Quality", "1-6 (default: 2)"],
     ["Rotate Image", "0 / 90 / 180 / 270 degrees"],
     ["Dark Lux Threshold", "1-100 (default: 25)"],
     ["Min / Max IR Brightness", "0-100%"],
     ["Image Cropping", "Left / Right / Top / Bottom: 0-50%"]],
    col_widths=[3*inch, 3.5*inch]
))
story.append(Spacer(1, 8))

story.append(Paragraph("Battery &amp; Power", s['SubSubSection']))
story.append(make_table(
    ["Setting", "Range / Default"],
    [["Battery Type", "5 Ah / 10 Ah selection"],
     ["Battery Alerts", "On / Off"],
     ["Power-Off Voltage", "7-12 V (default: 9.6 V)"]],
    col_widths=[3*inch, 3.5*inch]
))
story.append(Spacer(1, 8))

story.append(Paragraph("Temperature", s['SubSubSection']))
story.append(make_table(
    ["Setting", "Range / Default"],
    [["Temperature Alerts", "On / Off"],
     ["High Limit", "45C"],
     ["Low Limit", "-10C"],
     ["Report Interval", "0-48 hours (default: 8 hours)"]],
    col_widths=[3*inch, 3.5*inch]
))
story.append(Spacer(1, 8))

story.append(Paragraph("Other Settings", s['SubSubSection']))
story.append(make_table(
    ["Setting", "Range / Default"],
    [["GPS Interval", "Configurable (default: 8 hours)"],
     ["Location Tracking", "On / Off"],
     ["Accessory Port", "Enable / Disable; timing 0-30,000 ms"],
     ["User Beeps", "On / Off"],
     ["Enhanced Door Closing", "On / Off (default: On)"],
     ["Units", "Metric / Imperial"]],
    col_widths=[3*inch, 3.5*inch]
))
story.append(hr())

# -- Tips and Tricks --
story.append(Paragraph("Tips and Tricks", s['SubSection']))

story.append(Paragraph("Powering Off", s['SubSubSection']))
story.append(Paragraph("Hold the power button for 3 seconds for a proper shutdown.", s['Body']))

story.append(Paragraph("Maximizing Battery Life", s['SubSubSection']))
for b in [
    "Deploy in areas with strong cellular signal (poor signal increases power consumption)",
    "Keep GPS interval at the default 8 hours, or disable GPS if not needed",
    "Set camera time-lapse to 6 hours or more",
    "Use the 10 Ah battery for extended winter deployments",
]:
    story.append(bullet(b))

story.append(Paragraph("Optimal Placement", s['SubSubSection']))
for b in [
    "Position the ToF sensor 6-10 inches inside the cage entrance",
    "Place bait behind (deeper than) the sensor",
    "Set the trap on level ground to avoid false tilt alerts",
]:
    story.append(bullet(b))

story.append(Paragraph("Detection Zones", s['SubSubSection']))
story.append(Paragraph(
    "The sensor has a 20-degree field of view. An approaching animal first enters the detection zone "
    "(approximately 300-450 mm) triggering a pre-capture alert, then enters the capture zone (0-250 mm by default) "
    "which closes the door.", s['Body']))
add_image(story, "Untitled (40 x 30 in).png", "Detection zone diagram", max_w=5.5*inch, max_h=3.5*inch)

story.append(Paragraph("Button Shortcuts", s['SubSubSection']))
add_image(story, "pod-buttons-diagram.png", "POD button layout", max_w=5*inch, max_h=2.5*inch)
story.append(make_table(
    ["Action", "Button Combination"],
    [["Check Status", "Single press of User button"],
     ["Open/Close Door", "Double-press + hold User button for 5 seconds"],
     ["Arm / Disarm", "Press User button, then Power button"],
     ["Power Off", "Hold Power button for 3 seconds"],
     ["Wake from Hibernation", "Press Power button"]],
    col_widths=[3*inch, 3.5*inch]
))

story.append(Paragraph("Pre-Deployment Checklist", s['SubSubSection']))
for b in [
    "LED breathing cyan (connected to cloud)",
    "Battery sufficiently charged",
    "Door operates smoothly via app",
    "Trap armed successfully",
    "GPS location updated",
    "Bait positioned behind sensor",
    "Trap set on level ground",
]:
    story.append(bullet(b))
story.append(hr())

# -- Trap Settings --
story.append(Paragraph("Trap Settings", s['SubSection']))
story.append(Paragraph("Enhanced Door Closing", s['SubSubSection']))
story.append(Paragraph(
    "When enabled, the door cycles open and closed after closing to ensure a secure lock. "
    "This improves door lock reliability in the field. Enabled by default.", s['Body']))

story.append(Paragraph("Pre-Capture Notification", s['SubSubSection']))
story.append(Paragraph(
    "When enabled in armed mode, the system monitors two zones: an early detection zone (approximately 6 inches "
    "before the capture distance) and the primary detection zone (at the set capture distance). When an animal approaches, "
    "a pre-capture photo and alert are sent with the measured distance. There is a 2-minute cooldown between alerts. "
    "Enabled by default.", s['Body']))
story.append(hr())

# -- Maintenance --
story.append(Paragraph("Maintenance", s['SubSection']))
story.append(Paragraph("Perform these checks at the start of every trapping session:", s['Body']))
for b in [
    "<b>Camera lens:</b> Clean with a soft, lint-free cloth",
    "<b>Door operation:</b> Test open and close via the app",
    "<b>Exterior:</b> Wipe down with a damp cloth",
    "<b>Interior:</b> Inspect for obstructions or debris",
    "<b>Battery terminals:</b> Check for corrosion or loose connections",
    "<b>Motor and sensor:</b> Test operation and inspect for damage",
    "<b>Seals and enclosures:</b> Verify POD is watertight (both latches, knob tightened)",
    "<b>Post-weather:</b> Inspect thoroughly after storms or extreme conditions",
]:
    story.append(bullet(b))
story.append(Paragraph('<i>Firmware updates are applied automatically over the air when the device is connected.</i>', s['Tip']))
story.append(hr())

# -- LED Guide --
story.append(Paragraph("LED Guide", s['SubSection']))
story.append(Paragraph("System Status LEDs", s['SubSubSection']))
story.append(make_table(
    ["LED Pattern", "Meaning"],
    [["Breathing Cyan", "Connected to internet - fully operational"],
     ["Fast Blinking Cyan", "Connecting to cloud"],
     ["Blinking Magenta", "OTA firmware update in progress"],
     ["Blinking Green", "Searching for cellular connection"],
     ["Red Flash SOS", "Firmware crash - contact support if >10 blinks"],
     ["No LED", "No power or failed to boot"],
     ["LED Off (after armed)", "Hibernation - low-power sleep mode"]],
    col_widths=[2.5*inch, 4*inch]
))
story.append(Spacer(1, 8))
story.append(Paragraph("User Button LED Patterns", s['SubSubSection']))
story.append(make_table(
    ["LED Pattern", "State"],
    [["Solid Blue", "Unarmed / Door Open"],
     ["Solid Green", "Unarmed / Door Closed"],
     ["Solid Yellow", "Armed Mode"],
     ["Solid Magenta", "Armed / Captured"],
     ["Blinking Blue", "Opening Door"],
     ["Blinking Green", "Closing Door"],
     ["Blinking Yellow", "Arming Trap"],
     ["Blinking White", "Unarming Trap"]],
    col_widths=[2.5*inch, 4*inch]
))
story.append(Paragraph(
    '<b>Low Battery Startup:</b> If the battery is critically low, the LED shows solid red during boot. '
    'The device will send a cloud error notification and automatically enter hibernation.', s['Warning']))
story.append(hr())

# -- Battery Overview --
story.append(Paragraph("Battery Overview", s['SubSection']))
story.append(make_table(
    ["Battery Model", "Capacity", "Runtime", "Charge Time", "Charger"],
    [["KBT 5000 mAh (12V)", "5,000 mAh", "~21 days", "5-6 hours", "1A charger"],
     ["KBT 10000 mAh (12V)", "10,000 mAh", "~40+ days", "5-6 hours", "2A charger"]],
    col_widths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch]
))
story.append(Paragraph("Battery Care", s['SubSubSection']))
for b in [
    "Charge in a cool, dry environment",
    "Keep firmware updated for power optimizations",
    "Deploy traps in strong cellular coverage areas to reduce power draw",
    "Disconnect from charger after fully charged for long-term battery health",
    "Never attempt to open, puncture, or modify the battery",
]:
    story.append(bullet(b))

story.append(PageBreak())

# ==================== 2. FAQs ====================
story.append(Paragraph("2. Frequently Asked Questions", s['SectionHeader']))
story.append(hr())

# -- Sharing Traps --
story.append(Paragraph("Sharing Traps", s['SubSection']))
story.append(Paragraph(
    "Both the sharer and the recipient must have OcuTrap accounts. To share a trap:", s['Body']))
for i, step in enumerate([
    "Log in and navigate to the Sharing section",
    "Select the trap you want to share",
    "Click the + icon and enter the recipient's email",
    "Confirm - access is granted based on user level",
], 1):
    story.append(numbered(step, i))

story.append(Paragraph("User Levels", s['SubSubSection']))
for b in [
    "<b>Account Owners:</b> Full account privileges including billing management",
    "<b>Managers:</b> Can view, share, and edit settings and alerts in assigned groups",
    "<b>TNR:</b> Trap-Neuter-Return users with access to shared traps for TNR operations",
]:
    story.append(bullet(b))
story.append(hr())

# -- Common Questions --
story.append(Paragraph("Common Questions", s['SubSection']))
qa_pairs = [
    ("Can I differentiate between species?", "Yes. You can review captured images and release non-target animals remotely by opening the door from the app."),
    ("What size is the OcuTrap?", "The standard unit measures 10\" x 12\" x 34\" and targets animals in the 5-25 lb range."),
    ("Is the OcuTrap humane?", "Absolutely. The system is designed with animal welfare as a priority, featuring rapid door closure, remote monitoring to minimize stress, and selective targeting."),
    ("What is the battery life?", "3+ weeks depending on usage, settings, and environmental conditions. The 10 Ah battery provides extended runtime per charge."),
    ("Is a subscription required?", "A subscription enables cloud connectivity features. Check the current plans at ocutrap.com."),
    ("Does it work in extreme weather?", "The OcuTrap operates in temperatures from -10C to 45C. The weatherproof enclosure protects electronics."),
    ("Can I use it commercially?", "Yes. OcuTrap is suitable for commercial pest control, wildlife management, and research operations."),
    ("How do I handle false triggers?", "The dual-zone detection system, consecutive reading requirements, and oscillation detection minimize false triggers. Adjusting the capture distance and keeping the sensor clean further reduces them."),
    ("Can I connect multiple traps?", "Yes. Name traps clearly, use map view for tracking, share with team members, and stagger GPS intervals."),
    ("Is it safe around children?", "The door closes rapidly and can cause injury. Always keep children away from the trap."),
    ("What app platforms are supported?", "iOS (App Store) and Android (Google Play), plus the web console at base.ocutrap.com."),
    ("Is it suitable for residential areas?", "Yes. OcuTrap is effective in urban and suburban environments."),
    ("What warranty is available?", "Warranty details are available at ocutrap.com/pages/warranty."),
    ("Can I use it for research?", "Yes. Image capture, remote access, and data logging make OcuTrap an effective research tool."),
]
for q, a in qa_pairs:
    story.append(Paragraph(f"Q: {q}", s['QA_Q']))
    story.append(Paragraph(a, s['QA_A']))
story.append(hr())

# -- Safe Mode --
story.append(Paragraph("Safe Mode", s['SubSection']))
story.append(Paragraph("Prerequisites: Sufficient battery charge.", s['Body']))
for i, step in enumerate([
    "Hold both the RESET and MODE buttons simultaneously",
    "Release only the RESET button while continuing to hold MODE",
    "Wait for the magenta LED to blink",
    "Release the MODE button",
], 1):
    story.append(numbered(step, i))
story.append(hr())

# -- Battery FAQ --
story.append(Paragraph("Battery FAQ", s['SubSection']))
story.append(Paragraph(
    "OcuTrap uses high-quality lithium-ion batteries with built-in protection boards. The yellow connector "
    "powers the device; the black connector is for charging. A full charge from empty takes 4-6 hours.", s['Body']))
story.append(make_table(
    ["Specification", "Value"],
    [["Dimensions", "70 x 55 x 40 mm"],
     ["Weight", "~295 g"],
     ["Cable Length", "90 cm"],
     ["Charge Time", "4-6 hours (from empty)"]],
    col_widths=[3*inch, 3.5*inch]
))
story.append(hr())

# -- Updating Firmware --
story.append(Paragraph("Updating Firmware", s['SubSection']))
story.append(Paragraph(
    "Firmware updates are delivered automatically over the air (OTA) when the device is connected to cellular. "
    "Updates typically take 5-15 minutes.", s['Body']))
story.append(Paragraph("<b>Requirements for successful update:</b>", s['Body']))
for b in [
    "Device powered on and connected",
    "Battery charge above 20%",
    "Remain powered throughout the update",
]:
    story.append(bullet(b))
story.append(hr())

# -- Camera & Images --
story.append(Paragraph("Camera &amp; Images", s['SubSection']))

story.append(Paragraph("Manually Taking an Image", s['SubSubSection']))
story.append(Paragraph(
    "Navigate to the console page, click the controls icon, then click the camera icon in the bottom right.", s['Body']))
add_image(story, "IMG_3965.png", "Controls icon", max_w=4*inch, max_h=3.5*inch)
add_image(story, "IMG_2529.png", "Camera capture button", max_w=4*inch, max_h=3.5*inch)

story.append(Paragraph("Seeing the Camera View", s['SubSubSection']))
story.append(Paragraph(
    "Click the downward arrow icon beneath the settings button to expand the camera and map view.", s['Body']))
add_image(story, "drop down image.png", "Expand camera view", max_w=4*inch, max_h=3*inch)

story.append(Paragraph("Image Quality Settings", s['SubSubSection']))
story.append(Paragraph(
    "Quality is adjustable from 1 (lowest) to 6 (highest). Higher quality produces more detailed images "
    "but uses more data and battery. For most deployments, quality 2-3 provides a good balance.", s['Body']))
add_image(story, "IMG_2083.png", "Image quality settings", max_w=4*inch, max_h=3.5*inch)

story.append(Paragraph("Night Vision", s['SubSubSection']))
story.append(Paragraph(
    "The camera automatically switches between color (daylight) and grayscale with IR illumination (dark conditions). "
    "The switch is controlled by the Dark Lux threshold setting (default 25). IR brightness is adjustable from 0-100%.", s['Body']))
add_image(story, "Untitled (Flat Greeting Card - Landscape (7 in x 5 in)).png",
          "Day vs. night camera comparison", max_w=5*inch, max_h=3*inch)

story.append(Paragraph("Troubleshooting Camera Issues", s['SubSubSection']))
for b in [
    "<b>Dark daytime images:</b> Lower the dark lux threshold",
    "<b>Blurry images:</b> Increase quality setting",
    "<b>Dark nighttime images:</b> Increase max IR brightness",
    "<b>Washed-out images:</b> Lower max IR brightness",
    "<b>Glare:</b> Adjust trap position or lower IR brightness",
]:
    story.append(bullet(b))
story.append(hr())

# -- GPS --
story.append(Paragraph("GPS", s['SubSection']))
story.append(Paragraph(
    "GPS is battery-optimized with strategic update intervals. By default, position updates occur every 8 hours. "
    "GPS automatically updates upon a capture event.", s['Body']))
story.append(Paragraph("Best Practices", s['SubSubSection']))
for b in [
    "Place the trap with a clear view of the sky",
    "Allow 3 minutes for initial satellite acquisition",
    "More satellites connected means better accuracy (minimum 5 required)",
    "Avoid placing under buildings, dense foliage, or metal structures",
]:
    story.append(bullet(b))
story.append(hr())

# -- Weather --
story.append(Paragraph("Weather &amp; Environmental Guidelines", s['SubSection']))
story.append(make_table(
    ["Condition", "Guideline"],
    [["Operating Temperature", "Ideal: 0C to 40C"],
     ["Charging Temperature", "Recommended: 0C to 45C"],
     ["Extreme Heat", "Shade the trap; monitor temperature alerts"],
     ["Freezing", "Bring battery indoors for charging; use 10 Ah battery"],
     ["Heavy Rain", "Weatherproof but not submersion-rated; inspect after storms"],
     ["Icing", "Door mechanism may freeze; allow natural thaw"]],
    col_widths=[2.5*inch, 4*inch]
))
story.append(hr())

# -- Cold Weather --
story.append(Paragraph("Cold Weather Guide", s['SubSection']))
story.append(Paragraph(
    "The OcuTrap operates in temperatures as low as -10C, though battery capacity is significantly reduced in cold conditions.", s['Body']))
for b in [
    "Use the 10 Ah battery for extended winter deployments",
    "Bring batteries indoors for charging below freezing",
    "Store batteries in cool, dry conditions - avoid freezing",
    "Swap batteries more frequently in winter",
    "Use silica gel packs to prevent internal condensation from temperature swings",
]:
    story.append(bullet(b))
story.append(Paragraph(
    '<i>Condensation Prevention: Morning and evening temperature swings can cause external fogging. '
    'For internal moisture, perform a deep-dry: leave the POD cracked open for 24 hours in a warm, ventilated area.</i>', s['Tip']))
story.append(hr())

# -- Power Modes --
story.append(Paragraph("Power Modes", s['SubSection']))
story.append(Paragraph("The OcuTrap has six power modes that automatically optimize battery usage:", s['Body']))
story.append(make_table(
    ["Mode", "Description", "LED"],
    [["Normal Power", "Full operation, highest power consumption", "Full brightness"],
     ["Low Power Idle", "Power-saving during inactivity", "Dimmed"],
     ["Low Power Armed", "Armed and waiting; ~300ms ToF intervals", "Dimmed"],
     ["Sleep", "Deep power-saving; most sensors disabled", "Off"],
     ["Armed Sleep Offline", "20-minute check-ins", "Flashes 3s"],
     ["Hibernation", "Lowest power; no communication", "Off"]],
    col_widths=[1.8*inch, 3.2*inch, 1.5*inch]
))

story.append(Paragraph("Unarmed Hibernation", s['SubSubSection']))
story.append(Paragraph(
    "When enabled (default), the trap enters hibernation after approximately 2 hours of unarmed inactivity, "
    "with a 15-minute warning beforehand.", s['Body']))
story.append(hr())

# -- Accessory Port --
story.append(Paragraph("Accessory Port", s['SubSection']))
story.append(Paragraph(
    "The accessory port is located on top of the POD and provides a 12V DC output for external devices.", s['Body']))
add_image(story, "2.png", "Accessory port location", max_w=4*inch, max_h=3*inch)
add_image(story, "1.png", "Accessory port detail", max_w=4*inch, max_h=3*inch)

story.append(make_table(
    ["Specification", "Value"],
    [["Voltage", "12V DC"],
     ["Max Continuous Current", "3.0 A"],
     ["Switching", "MOSFET low-side switched, 100k ohm pull-down"],
     ["Polarity", "Pin 1: Ground, Pin 2: +12V (not reversible)"],
     ["Timing", "Configurable 0-30,000 ms"]],
    col_widths=[3*inch, 3.5*inch]
))
story.append(Paragraph(
    '<b>Warning:</b> Do not use the accessory port and door motor simultaneously. Do not exceed 3.0A. '
    'Add flyback diode protection for inductive loads.', s['Warning']))

story.append(PageBreak())

# ==================== 3. TROUBLESHOOTING ====================
story.append(Paragraph("3. Troubleshooting", s['SectionHeader']))
story.append(hr())

# -- Common Issues --
story.append(Paragraph("Common Issues", s['SubSection']))

story.append(Paragraph("Trap Won't Arm", s['SubSubSection']))
for b in [
    "The door must be fully open (LED shows solid blue) before arming",
    "Clear any obstructions from the sensor or interior",
    "Verify the motor connector is securely attached",
]:
    story.append(bullet(b))

story.append(Paragraph("False Triggers", s['SubSubSection']))
story.append(Paragraph(
    "OcuTrap uses multiple safeguards: 3+ consecutive readings required, oscillation detection, and signal quality filtering.", s['Body']))
for b in [
    "Increase the capture distance setting",
    "Position the trap to minimize rain entering the sensor area",
    "Clean the sensor window",
    "Reposition the trap away from debris or moving vegetation",
]:
    story.append(bullet(b))

story.append(Paragraph("GPS Not Updating", s['SubSubSection']))
for b in [
    "Ensure GPS is enabled in settings",
    "Place the trap outdoors with clear sky visibility",
    "Allow 3 minutes for initial satellite fix",
    "Request a manual update from the app",
]:
    story.append(bullet(b))

story.append(Paragraph("Camera Issues", s['SubSubSection']))
for b in [
    "<b>Dark/black images:</b> Check the lux threshold; increase IR brightness; clean the IR window",
    "<b>Overexposed images:</b> Decrease max IR brightness; adjust image cropping; reposition trap",
    "<b>Images not sending:</b> Check signal strength; reduce quality setting; move to better coverage",
]:
    story.append(bullet(b))

story.append(Paragraph("Connectivity Issues", s['SubSubSection']))
story.append(Paragraph(
    "The device has automatic recovery after 20 minutes offline.", s['Body']))
for i, step in enumerate([
    "Check that the battery is charged and connected",
    "Inspect the LED - if no LED, verify all connections are secure",
    "Confirm the trap appears in your Main Console",
    "Verify the serial number matches the Particle chipset SN in settings",
    "If blinking green, ensure you have adequate cellular coverage",
    "Check that the gold antenna connections are pressed down and secure",
], 1):
    story.append(numbered(step, i))

story.append(Paragraph("Battery Draining Quickly", s['SubSubSection']))
for b in [
    "Poor cellular signal significantly increases power consumption",
    "Frequent GPS updates and short time-lapse intervals drain the battery faster",
    "Cold temperatures reduce effective battery capacity",
    "Deploy in good coverage areas, increase intervals, and keep firmware updated",
]:
    story.append(bullet(b))

story.append(Paragraph("Door Issues", s['SubSubSection']))
for b in [
    "<b>Won't open/close:</b> Check motor connector; ensure no obstructions; verify adequate battery",
    "<b>Slow operation:</b> Fully charge battery; check track for debris",
    "<b>Orange motor LED:</b> Motor fault detected - contact support",
]:
    story.append(bullet(b))
story.append(hr())

# -- Trap Not Sending Commands --
story.append(Paragraph("Trap Not Sending Commands", s['SubSection']))
story.append(Paragraph("Common Causes:", s['BodyBold']))
for b in [
    "Device is in hibernation mode",
    "Battery disconnected or depleted",
    "Not online (no cellular connection)",
    "Poor cellular signal in deployment area",
]:
    story.append(bullet(b))
story.append(Paragraph("Solutions:", s['BodyBold']))
for b in [
    "Press the power button to wake from hibernation",
    "Verify battery connection and charge level",
    "Check online status indicator in the app",
    "Move to an area with better cellular coverage",
    "Contact support if the issue persists",
]:
    story.append(bullet(b))
story.append(hr())

# -- Motor Connection Issues --
story.append(Paragraph("Motor Connection Issues", s['SubSection']))
story.append(Paragraph("Pin and Clevis Won't Fit", s['SubSubSection']))
add_image(story, "11B9D2D8-CDFF-4395-A167-CEF1BE76B000_1_105_c.jpeg",
          "Motor connector assembly", max_w=4*inch, max_h=3*inch)
story.append(Paragraph("If the pin and clevis don't fit into the motor connector, the motor may be fully retracted.", s['Body']))
for i, step in enumerate([
    "Power on the OcuTrap",
    'Press "Close" to extend the motor shaft',
    "Prop up the motor for clearance",
    "Let the door down completely",
    "Unplug the motor",
    "Insert the clevis and pin - they should now fit easily",
], 1):
    story.append(numbered(step, i))

add_image(story, "DE68151C-8ECC-4ED7-BDC7-857640B4E369_1_105_c (2).jpeg",
          "Motor connector detail", max_w=3*inch, max_h=2.5*inch)
add_image(story, "IMG_7064 2.jpeg", "Before assembly", max_w=3*inch, max_h=2.5*inch)
add_image(story, "IMG_7065 2 (1).jpeg", "After assembly", max_w=3*inch, max_h=2.5*inch)

story.append(Paragraph("Motor Connector Tightness", s['SubSubSection']))
add_image(story, "IMG_0998.jpeg", "Motor connector tightness check", max_w=4*inch, max_h=3*inch)
story.append(Paragraph(
    "The correct gap specification is <b>0.15-0.20 inches</b>. Less causes connection issues; "
    "more causes loose operation. Gradually tighten to the proper range.", s['Body']))
story.append(hr())

# -- Condensation --
story.append(Paragraph("Condensation on the Camera", s['SubSection']))
story.append(Paragraph("Symptoms:", s['BodyBold']))
for b in [
    "Foggy or milky images (external condensation)",
    "Persistent haze inside the lens (internal moisture)",
    "Visible droplets inside the POD (water ingress)",
]:
    story.append(bullet(b))

story.append(Paragraph("Immediate Fix:", s['BodyBold']))
for i, step in enumerate([
    "Power down and open the POD",
    "Wipe the outside glass with a clean cloth",
    "Inspect the seal for debris; clean with isopropyl alcohol",
    "Place a silica gel pack inside the POD",
], 1):
    story.append(numbered(step, i))

story.append(Paragraph("Deep-Dry Procedure:", s['BodyBold']))
story.append(Paragraph(
    "Remove the battery and leave the POD cracked open for 24 hours in a warm, ventilated area. "
    "Alternatively, seal the POD with a desiccant pack for 12-18 hours.", s['Body']))

story.append(Paragraph("Prevention:", s['BodyBold']))
for b in [
    "Coat the seal with silicone grease every 6 months",
    "Tighten antenna and accessory port caps",
    "Avoid submerging or pressure-washing the POD",
]:
    story.append(bullet(b))

story.append(Paragraph(
    '<i>If condensation persists, email photos and a description to support@ocutrap.com.</i>', s['Tip']))

story.append(PageBreak())

# ==================== 4. SUPPORT ====================
story.append(Paragraph("4. Support", s['SectionHeader']))
story.append(hr())

story.append(Paragraph("Contact Us", s['SubSection']))
story.append(make_table(
    ["Channel", "Details"],
    [["Live Chat", "Message bubble on OcuTrap.com homepage (bottom right)"],
     ["Email", "info@ocutrap.com or via the contact page"],
     ["Website Status", "ocutrap.statuspage.io"]],
    col_widths=[2*inch, 4.5*inch]
))
story.append(hr())

story.append(Paragraph("Bug Reporting", s['SubSection']))
story.append(Paragraph(
    "Report bugs promptly at base.ocutrap.com/bug_report. Include a detailed description, steps to reproduce, "
    "screenshots or photos, and expected versus actual behavior.", s['Body']))
story.append(hr())

story.append(Paragraph("Safety Information", s['SubSection']))
story.append(Paragraph(
    '<b>Warning:</b> The OcuTrap uses a depth sensor to remotely trigger a rapid door closure that can cause serious injury. '
    'Never place hands, fingers, or any body part in the door path. Keep children away at all times.', s['Warning']))
story.append(Paragraph("Injury Prevention:", s['BodyBold']))
for b in [
    "Keep clear of the door path at all times",
    "Supervise all trap operation",
    "Review the user manual before first use",
    "Perform regular maintenance checks",
]:
    story.append(bullet(b))
story.append(hr())

story.append(Paragraph("Purchases", s['SubSection']))
story.append(Paragraph("OcuTrap devices are available for purchase online only at www.ocutrap.com.", s['Body']))
story.append(hr())

story.append(Paragraph("Nonprofit and 501(c) Program", s['SubSection']))
story.append(Paragraph("OcuTrap offers special pricing and support for qualifying organizations.", s['Body']))
story.append(Paragraph("Benefits:", s['BodyBold']))
for b in [
    "Discounted hardware pricing",
    "Dedicated onboarding and training",
    "Priority support",
    "Flexible purchasing with quotes, POs, and invoicing",
    "Bulk order benefits",
]:
    story.append(bullet(b))
story.append(Paragraph("Eligibility:", s['BodyBold']))
for b in [
    "U.S. 501(c) nonprofit organizations",
    "Government agencies",
    "Accredited educational institutions",
]:
    story.append(bullet(b))

story.append(PageBreak())

# ==================== 5. ACCOUNT & BILLING ====================
story.append(Paragraph("5. Account &amp; Billing", s['SectionHeader']))
story.append(hr())

story.append(Paragraph("Billing Overview", s['SubSection']))
story.append(Paragraph(
    "Manage your billing through the OcuTrap account portal. Log in at base.ocutrap.com, navigate to Account, "
    "and scroll to the Billing section.", s['Body']))
add_image(story, "Screenshot 2025-01-30 at 10.30.00 AM (1).png", "Account billing section", max_w=5*inch, max_h=3.5*inch)
add_image(story, "Screenshot 2025-01-30 at 10.30.08 AM (1).png", "Stripe billing portal", max_w=5*inch, max_h=3.5*inch)

story.append(Paragraph("Subscription Statuses", s['SubSubSection']))
story.append(make_table(
    ["Status", "Description"],
    [["Active", "Full access to all features"],
     ["Trialing", "Free trial period; no charges until trial ends"],
     ["Canceled", "Service continues until end of current billing cycle"]],
    col_widths=[2*inch, 4.5*inch]
))
story.append(hr())

story.append(Paragraph("Changing Your Payment Method", s['SubSection']))
add_image(story, "Screenshot 2025-01-30 at 10.32.34 AM (1).png", "Payment method management", max_w=5*inch, max_h=3.5*inch)
for i, step in enumerate([
    "Sign in at OcuTrap.com and go to the Account page",
    'Scroll to "Manage Subscription"',
    "In the Stripe portal, scroll to Payment Methods",
    'Click "Add payment method"',
    "Enter your new payment information",
    "Optionally set as default under the payment method list",
], 1):
    story.append(numbered(step, i))
story.append(hr())

story.append(Paragraph("Updating Individual Trap Subscriptions", s['SubSection']))
story.append(Paragraph("Each trap requires its own active subscription.", s['Body']))
for i, step in enumerate([
    "Log into the console and find the trap",
    "Click Settings and check the Plan status in Device Info",
    'Click "Update" if the subscription needs renewal',
    "Complete the checkout process",
], 1):
    story.append(numbered(step, i))
story.append(hr())

story.append(Paragraph("Managing Your Subscription", s['SubSection']))
for i, step in enumerate([
    "Go to base.ocutrap.com and log in",
    "Click Account &rarr; Manage Subscription",
    "Select the trap to update",
], 1):
    story.append(numbered(step, i))
story.append(Paragraph(
    "From here you can switch plans (Monthly/Annual), update your payment method, or cancel your subscription. "
    "Canceled subscriptions retain access until the end of the current billing period.", s['Body']))
story.append(hr())

story.append(Paragraph("Resetting Your Password", s['SubSection']))
story.append(Paragraph("Visit base.ocutrap.com/signuplogin and select either:", s['Body']))
for b in [
    "<b>Forgot Password:</b> Standard password reset via email",
    "<b>Magic Link:</b> One-time login link sent to your email (expires after 1 hour)",
]:
    story.append(bullet(b))
story.append(hr())

story.append(Paragraph("Account Deletion", s['SubSection']))
story.append(Paragraph(
    '<b>Warning:</b> Account deletion is permanent and cannot be undone. All data, traps, and subscriptions will be removed.', s['Warning']))
for i, step in enumerate([
    "Visit base.ocutrap.com/delete-account",
    'Click "Delete Account" (log in if prompted)',
    'Type "Delete" (case sensitive) in the confirmation box',
    'Click "Delete Account" to confirm',
], 1):
    story.append(numbered(step, i))

story.append(PageBreak())

# ==================== 6. LEGAL & COMPLIANCE ====================
story.append(Paragraph("6. Legal &amp; Compliance", s['SectionHeader']))
story.append(hr())

story.append(Paragraph("Warranty Information", s['SubSection']))
story.append(Paragraph(
    "Full warranty details are available at ocutrap.com/pages/warranty. The warranty period begins from the date of first device activation.", s['Body']))
story.append(hr())

story.append(Paragraph("Legal Disclaimers &amp; Compliance", s['SubSection']))
story.append(Paragraph("The following policies govern the use of OcuTrap products and services:", s['Body']))
for b in ["Terms of Service", "Privacy Policy", "Hardware Warranty", "Software License", "Refund Policy", "Animal Recognition Policy"]:
    story.append(bullet(b))
story.append(Paragraph("Full text of all policies is available at ocutrap.com.", s['Body']))

story.append(PageBreak())

# ==================== 7. DEVICE MANAGEMENT ====================
story.append(Paragraph("7. Device Management", s['SectionHeader']))
story.append(hr())

story.append(Paragraph("Selling or Transferring a Trap", s['SubSection']))
story.append(Paragraph("Step 1: Remove the trap from your account", s['SubSubSection']))
story.append(Paragraph('Log in, locate the trap, click "Delete Trap," and confirm by typing the exact trap name.', s['Body']))
story.append(Paragraph("Step 2: New owner adds the trap", s['SubSubSection']))
story.append(Paragraph(
    "The new owner creates an OcuTrap account, navigates to Account &rarr; Add Trap, and enters the Trap ID (serial number found inside the POD).", s['Body']))
story.append(Paragraph("Step 3: Activate subscription", s['SubSubSection']))
story.append(Paragraph("The new owner activates a subscription if required.", s['Body']))
story.append(hr())

story.append(Paragraph("Deleting a Trap", s['SubSection']))
story.append(Paragraph(
    '<b>Warning:</b> Deleting a trap is permanent and cannot be undone. The associated subscription will be automatically canceled.', s['Warning']))
for i, step in enumerate([
    "Visit base.ocutrap.com/account and scroll to Devices",
    'Click "Delete Devices"',
    "Select the trap from the dropdown",
    "Type the exact trap name in the red confirmation box",
    "A confirmation email with the Trap ID will be sent",
], 1):
    story.append(numbered(step, i))

story.append(PageBreak())

# ==================== 8. APPENDIX & RESOURCES ====================
story.append(Paragraph("8. Appendix &amp; Resources", s['SectionHeader']))
story.append(hr())

story.append(Paragraph("Media Kit", s['SubSection']))
story.append(Paragraph(
    "OcuTrap provides high-quality media assets for press, partners, and promotional use. "
    "Contact info@ocutrap.com or visit the media kit page for downloads.", s['Body']))
add_image(story, "LogoMakr-1uMIUJ.png", "OcuTrap Logo", max_w=3*inch, max_h=1.5*inch)
story.append(hr())

story.append(Paragraph("Testimonials", s['SubSection']))
testimonials = [
    ('"OcuTrap has dramatically reduced the time we spend on trap checks. The real-time alerts mean we can respond immediately to captures instead of making daily rounds."',
     "Wildlife Management Professional"),
    ('"The ability to release non-target animals remotely without visiting the trap has transformed our humane pest control operations."',
     "Pest Control Operator"),
    ('"Real-time notifications let us respond to captures quickly, protecting both our livestock and the trapped animals."',
     "Farm Owner"),
    ('"The image capture and remote access capabilities provide invaluable research data without disturbing the animals or the trap site."',
     "Wildlife Researcher"),
]
for quote, author in testimonials:
    story.append(Paragraph(f'<i>{quote}</i>', s['Body']))
    story.append(Paragraph(f'<b>- {author}</b>', ParagraphStyle(
        'Author', parent=s['Body'], alignment=TA_LEFT, textColor=HexColor('#2E86C1'), spaceAfter=12
    )))
story.append(hr())

story.append(Paragraph("Case Study: Springfield Municipal Council", s['SubSection']))
story.append(Paragraph("<b>Location:</b> Springfield suburban area", s['Body']))
story.append(Paragraph("<b>Challenge:</b> High raccoon population with limited resources and humanitarian concerns.", s['Body']))
story.append(Paragraph("<b>Solution:</b> Deployed 50 OcuTrap devices with remote monitoring, smart controls, and selective targeting.", s['Body']))
story.append(Paragraph("<b>Results:</b>", s['Body']))
for b in [
    "90% reduction in manual trap checks",
    "75% increase in successful captures",
    "Zero safety incidents",
    "Positive community feedback on humane practices",
]:
    story.append(bullet(b))
story.append(hr())

story.append(Paragraph("Recent Updates", s['SubSection']))
story.append(Paragraph("April 2026 - Firmware v2.1.2-632", s['SubSubSection']))
story.append(Paragraph(
    "Introduced Monitoring Mode (in testing). This mode uses live armed detection for scouting without closing the door.", s['Body']))
story.append(Paragraph("April 2024 - Firmware v1.12.7-250", s['SubSubSection']))
story.append(Paragraph(
    "Added unarmed hibernation control setting (default enabled, configurable). General improvements including faster GPS acquisition, "
    "more accurate battery readings, sharper images, and overall stability enhancements.", s['Body']))
story.append(Paragraph("January 2023 - UI Update", s['SubSubSection']))
story.append(Paragraph("Dark mode and general user interface improvements.", s['Body']))
story.append(hr())

story.append(Paragraph("OcuTrap in the News", s['SubSection']))
story.append(Paragraph(
    "OcuTrap founders Brian Quispe '20 '22G and Graham Patterson '20 won the Joan F. and John M. Thalheimer '55 "
    "Grand Prize at the Baker Institute's annual award competitions at Lehigh University, recognizing OcuTrap's "
    "innovative approach to humane wildlife management technology.", s['Body']))

story.append(Spacer(1, 1*inch))
story.append(hr())
story.append(Paragraph("<i>OcuTrap - Smart Wildlife Management</i>", ParagraphStyle(
    'Footer', parent=s['Body'], alignment=TA_CENTER, textColor=HexColor('#5D6D7E')
)))
story.append(Paragraph("<i>www.ocutrap.com | info@ocutrap.com</i>", ParagraphStyle(
    'FooterURL', parent=s['Body'], alignment=TA_CENTER, textColor=HexColor('#2E86C1')
)))

# ==================== BUILD PDF ====================
print("Building PDF...")

def add_page_number(canvas_obj, doc):
    """Add page number footer and header line."""
    canvas_obj.saveState()
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(HexColor('#5D6D7E'))
    page_num = canvas_obj.getPageNumber()
    canvas_obj.drawCentredString(letter[0]/2, 0.5*inch, f"OcuTrap Knowledge Base {VERSION}  |  Page {page_num}")
    canvas_obj.restoreState()

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch,
    title="OcuTrap Knowledge Base",
    author="OcuTrap",
    subject="Complete User Guide & Reference - Smart Wildlife Trap System",
)

doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"PDF saved to: {OUTPUT}")
print(f"Total pages: {doc.page}")
