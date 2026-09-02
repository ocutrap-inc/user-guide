#!/usr/bin/env python3
"""
Build the OcuTrap in-box printed manuals (R1 and R2).

Physical format
---------------
The booklet unit is a **half-letter page, 5.5 x 8.5 in portrait**. Graham
prints on US letter, duplex, short-edge flip, at "1 page per sheet" using the
`_print-2up` file, then folds each sheet in half. One letter sheet therefore
carries four booklet pages.

    R2 = 8 booklet pages = 2 letter sheets
    R1 = 8 booklet pages = 2 letter sheets
    (sheet 2 nests inside sheet 1)

Two outputs per model:

    pdf-docs/printed/<MODEL>_Manual.pdf            half-letter, reading order
                                                   (also the docs download)
    pdf-docs/printed/<MODEL>_Manual_print-2up.pdf  letter landscape, imposed
                                                   for saddle folding

Imposition for n booklet pages (n a multiple of 4), sheets k = 0..n/4-1, with
1-indexed page numbers:

    sheet k front = [ page n-2k   | page 2k+1   ]
    sheet k back  = [ page 2k+2   | page n-2k-1 ]

Margins are 0.4 in, with an inner-edge allowance so nothing sits closer than
0.5 in to the fold. The fold edge is the LEFT edge of odd reading-order pages
and the RIGHT edge of even pages.

Type scale. This is a legibility floor: never go below it to make something
fit, give the content another page instead.

    body        11 pt on 14.5 pt leading
    step title  12 pt bold
    headings    16 pt
    table cells 10 pt (9.5 pt only on the R1 buttons+lights page, which
                carries both reference tables)
    captions    9 pt
    legal       8.5 pt
    footer      8.5 pt

Source of truth for content: docs.ocutrap.com (canonical knowledge base)
References: getting-started/setting-up.md, getting-started/setting-up-r2.md

Usage:
    pip install -r scripts/requirements.txt
    python3 scripts/build_box_manual.py --model all
"""

import argparse
import glob
import os
import sys
import tempfile

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
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
MANUAL_IMAGES = os.path.join(REPO_ROOT, "pdf-docs", "manual-images")
OUT_DIR = os.path.join(REPO_ROOT, "pdf-docs", "printed")
LOGO = os.path.join(ASSETS, "LogoMakr-1uMIUJ-300dpi (2).png")

DOCS_URL = "https://docs.ocutrap.com"
APP_URL = "https://app.ocutrap.com"
SUPPORT_EMAIL = "support@ocutrap.com"

# ---------------------------------------------------------------- palette ---
NAVY = HexColor("#1f3c6b")
GOLD = HexColor("#d9b772")
INK = HexColor("#211f1d")
MUTED = HexColor("#6f6c65")
PANEL = HexColor("#f6f5f2")
BORDER = HexColor("#e5e3de")
WARN_RED = HexColor("#9B2318")
WARN_FILL = HexColor("#FBEEEC")

# ------------------------------------------------------------ page geometry -
PAGE_W = 5.5 * inch
PAGE_H = 8.5 * inch
MARGIN = 0.4 * inch
FOLD_MARGIN = 0.5 * inch          # inner-edge allowance next to the fold
FOOTER_H = 0.34 * inch
COVER_BAND_H = 1.0 * inch

FRAME_W = PAGE_W - MARGIN - FOLD_MARGIN          # 4.6 in on every page
FRAME_H = PAGE_H - MARGIN - MARGIN - FOOTER_H

SHEET_W = 11 * inch
SHEET_H = 8.5 * inch

# ---------------------------------------------------------------- styles ----
_ss = getSampleStyleSheet()

sBody = ParagraphStyle(
    "Body", parent=_ss["Normal"], fontName="Helvetica",
    fontSize=11, leading=14.5, textColor=INK, alignment=TA_LEFT, spaceAfter=0,
)
sBodyBold = ParagraphStyle("BodyBold", parent=sBody, fontName="Helvetica-Bold")
sLead = ParagraphStyle("Lead", parent=sBody, fontSize=12, leading=15.5)
sStepTitle = ParagraphStyle(
    "StepTitle", parent=sBody, fontName="Helvetica-Bold",
    fontSize=12, leading=15, textColor=NAVY, spaceAfter=0,
)
sH1 = ParagraphStyle(
    "H1", parent=_ss["Heading1"], fontName="Helvetica-Bold",
    fontSize=16, leading=18.5, textColor=NAVY, spaceBefore=0, spaceAfter=2,
)
sH2 = ParagraphStyle(
    "H2", parent=_ss["Heading2"], fontName="Helvetica-Bold",
    fontSize=12, leading=15, textColor=NAVY, spaceBefore=0, spaceAfter=1,
)
sKicker = ParagraphStyle(
    "Kicker", parent=sBody, fontName="Helvetica-Bold", fontSize=8.5,
    leading=10.5, textColor=GOLD,
)
sSmall = ParagraphStyle("Small", parent=sBody, fontSize=9.5, leading=12.5,
                        textColor=MUTED)
sTiny = ParagraphStyle("Tiny", parent=sBody, fontSize=8.5, leading=10.8,
                       textColor=MUTED)
sLegal = ParagraphStyle("Legal", parent=sBody, fontSize=8.5, leading=10.8,
                        textColor=INK)
sLegalHead = ParagraphStyle("LegalHead", parent=sBody,
                            fontName="Helvetica-Bold",
                            fontSize=9.5, leading=11.5, textColor=NAVY)
sTable = ParagraphStyle("Tbl", parent=sBody, fontSize=10, leading=12.4)
# The R1 buttons+lights page carries both reference tables, so it keeps the
# old 9.5 pt cells rather than spilling onto a ninth page.
sTableSm = ParagraphStyle("TblSm", parent=sTable, fontSize=9.5, leading=11.6)
sTableBold = ParagraphStyle("TblB", parent=sTable, fontName="Helvetica-Bold")
sTableHead = ParagraphStyle("TblH", parent=sTable, fontName="Helvetica-Bold",
                            textColor=NAVY)
sTableSmBold = ParagraphStyle("TblSmB", parent=sTableSm,
                              fontName="Helvetica-Bold")
sTableSmHead = ParagraphStyle("TblSmH", parent=sTableSm,
                              fontName="Helvetica-Bold", textColor=NAVY)
sWarn = ParagraphStyle("Warn", parent=sBody, fontSize=11, leading=14,
                       textColor=WARN_RED)
sCaption = ParagraphStyle("Caption", parent=sBody,
                          fontName="Helvetica-Oblique",
                          fontSize=9, leading=11, textColor=MUTED,
                          alignment=TA_CENTER)
sCoverTitle = ParagraphStyle(
    "CoverTitle", parent=sBody, fontName="Helvetica-Bold",
    fontSize=30, leading=33, textColor=NAVY,
)
sCoverSub = ParagraphStyle(
    "CoverSub", parent=sBody, fontSize=12.5, leading=15.5, textColor=MUTED,
)
sCoverLine = ParagraphStyle("CoverLine", parent=sBody, fontSize=10.5,
                            leading=14.5, textColor=INK)
sQRUrl = ParagraphStyle("QRUrl", parent=sBody, fontSize=8.5, leading=10.5,
                        textColor=MUTED, alignment=TA_CENTER)
sQRLabel = ParagraphStyle("QRLabel", parent=sBody, fontName="Helvetica-Bold",
                          fontSize=9.5, leading=11.5, textColor=NAVY,
                          alignment=TA_CENTER)

_TMP_FILES = []

NO_PAD = [
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]


# --------------------------------------------------------------- helpers ----
def asset(*names):
    """First existing path from .gitbook/assets, then pdf-docs/manual-images.
    Names may be glob patterns: macOS screenshot filenames carry a narrow
    no-break space that is easy to get wrong when typed literally."""
    for n in names:
        for root in (ASSETS, MANUAL_IMAGES):
            p = os.path.join(root, n)
            if os.path.exists(p):
                return p
        hits = sorted(glob.glob(os.path.join(ASSETS, n)))
        if hits:
            return hits[0]
    return None


def trim_white(path, tol=8):
    """Crop a uniform near-white border off line art and renders so the
    drawing fills the space it is given. Photos are left alone (their border
    is not white, so the bounding box comes back unchanged)."""
    try:
        from PIL import Image as PILImage, ImageChops
        with PILImage.open(path) as im:
            rgb = im.convert("RGBA")
            bg = PILImage.new("RGBA", rgb.size, (255, 255, 255, 255))
            bg.alpha_composite(rgb)
            flat = bg.convert("RGB")
            ref = PILImage.new("RGB", flat.size, (255, 255, 255))
            diff = ImageChops.difference(flat, ref).convert("L")
            box = diff.point(lambda v: 255 if v > tol else 0).getbbox()
            if not box:
                return path
            pad = 4
            box = (max(0, box[0] - pad), max(0, box[1] - pad),
                   min(flat.size[0], box[2] + pad),
                   min(flat.size[1], box[3] + pad))
            if box == (0, 0, flat.size[0], flat.size[1]):
                return path
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            flat.crop(box).save(tmp.name, "PNG")
            _TMP_FILES.append(tmp.name)
            return tmp.name
    except Exception as e:  # pragma: no cover - defensive
        print(f"  warn: trim {path}: {e}")
        return path


def fit_image(path, max_w, max_h, target_dpi=200, trim=False):
    """Fit-and-downsample: return a reportlab Image whose embedded pixels are
    no larger than needed at `target_dpi` for the drawn size. Keeps PDF size
    sane when source photos are 4k+."""
    if not path or not os.path.exists(path):
        return None
    if trim:
        path = trim_white(path)
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
                if mode in ("RGBA", "LA", "P"):
                    # Flatten transparency onto white. Converting straight to
                    # RGB turns transparent pixels black.
                    im = im.convert("RGBA")
                    bg = PILImage.new("RGBA", im.size, (255, 255, 255, 255))
                    bg.alpha_composite(im)
                    im = bg.convert("RGB")
                im.thumbnail((target_px_w, target_px_h), PILImage.LANCZOS)
                tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                im.save(tmp.name, "JPEG", quality=82, optimize=True)
                _TMP_FILES.append(tmp.name)
                return Image(tmp.name, width=iw, height=ih)

            return Image(path, width=iw, height=ih)
    except Exception as e:  # pragma: no cover - defensive
        print(f"  warn: {path}: {e}")
        return None


def reversed_logo(max_w, max_h):
    """White silhouette of the logo, composited on navy, for the cover band."""
    if not os.path.exists(LOGO):
        return None
    try:
        from PIL import Image as PILImage
        with PILImage.open(LOGO) as im:
            im = im.convert("RGBA")
            alpha = im.split()[3]
            solid = PILImage.new("RGBA", im.size, (255, 255, 255, 255))
            solid.putalpha(alpha)
            navy = PILImage.new("RGBA", im.size, (31, 60, 107, 255))
            navy.alpha_composite(solid)
            out = navy.convert("RGB")
            out.thumbnail(
                (int((max_w / inch) * 300), int((max_h / inch) * 300)),
                PILImage.LANCZOS)
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            out.save(tmp.name, "PNG")
            _TMP_FILES.append(tmp.name)
            w, h = out.size
            aspect = w / h
            iw, ih = max_w, max_w / aspect
            if ih > max_h:
                ih, iw = max_h, max_h * aspect
            return Image(tmp.name, width=iw, height=ih)
    except Exception as e:  # pragma: no cover - defensive
        print(f"  warn: logo: {e}")
        return None


def make_qr(url, size_px=600):
    """Navy-on-white QR PNG at a temp path. Error correction M."""
    try:
        import qrcode
    except ImportError:
        print("  warn: qrcode not installed. pip install 'qrcode[pil]'")
        return None
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1f3c6b", back_color="white").convert("RGB")
    img = img.resize((size_px, size_px))
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name, "PNG")
    _TMP_FILES.append(tmp.name)
    return tmp.name


def qr_block(url, display_url, size, label=None, width=None):
    """QR code with the URL printed underneath, optional label above."""
    width = width or max(size, 1.6 * inch)
    path = make_qr(url)
    img = fit_image(path, size, size) if path else None
    rows = []
    if label:
        rows.append([Paragraph(label, sQRLabel)])
    rows.append([img if img else Paragraph("", sBody)])
    rows.append([Paragraph(display_url, sQRUrl)])
    t = Table(rows, colWidths=[width])
    t.setStyle(TableStyle(NO_PAD + [
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


class PushToBottom(Flowable):
    """Eats the frame's remaining height minus the room `tail` needs, so the
    tail block lands flush with the bottom of the page."""

    def __init__(self, tail, width):
        Flowable.__init__(self)
        self.tail = tail
        self._w = width
        self._h = 0

    def wrap(self, aw, ah):
        _, th = self.tail.wrap(self._w, 1e6)
        self._h = max(0, ah - th)
        return 0, self._h

    def draw(self):
        pass


class CircleNum(Flowable):
    """A 14 pt gold disc with a navy numeral, used as the step bullet."""

    def __init__(self, num, diameter=14):
        Flowable.__init__(self)
        self.num = str(num)
        self.d = diameter
        self.width = diameter
        self.height = diameter

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        r = self.d / 2.0
        c.setFillColor(GOLD)
        c.setStrokeColor(GOLD)
        c.circle(r, r, r, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(r, r - 3.2, self.num)


STEP_NUM_W = 0.3 * inch
STEP_TEXT_W = FRAME_W - STEP_NUM_W


def image_row(items, width, gap=10, height=1.7 * inch, trim=True):
    """items: list of (path, caption). Skips anything missing."""
    live = [(p, c) for p, c in items if p and os.path.exists(p)]
    if not live:
        return None
    n = len(live)
    cw = (width - gap * (n - 1)) / n
    cells, caps, col_widths = [], [], []
    for i, (p, c) in enumerate(live):
        if i:
            col_widths.append(gap)
            cells.append("")
            caps.append("")
        col_widths.append(cw)
        img = fit_image(p, cw, height, trim=trim)
        cells.append(img if img else Paragraph("", sBody))
        caps.append(Paragraph(c, sCaption) if c else Paragraph("", sCaption))
    t = Table([cells, caps], colWidths=col_widths)
    t.setStyle(TableStyle(NO_PAD + [
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ("TOPPADDING", (0, 1), (-1, 1), 3),
    ]))
    return t


def step(num, title, body, image=None, caption=None, img_h=1.7 * inch,
         images=None):
    """One numbered step: gold circled numeral, 11 pt bold title, 10 pt body,
    and an optional photo (never smaller than 1.6 in of height)."""
    inner = []
    if title:
        inner.append(Paragraph(title, sStepTitle))
        inner.append(Spacer(1, 1.5))
    if body:
        inner.append(Paragraph(body, sBody))
    pics = images if images is not None else (
        [(image, caption)] if image else [])
    if pics:
        row = image_row(pics, STEP_TEXT_W, height=max(img_h, 1.6 * inch),
                        trim=True)
        if row:
            inner.append(Spacer(1, 7))
            inner.append(row)
    t = Table([[CircleNum(num), inner]],
              colWidths=[STEP_NUM_W, STEP_TEXT_W])
    t.setStyle(TableStyle(NO_PAD + [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (1, 0), (1, 0), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    return t


def steps_stack(items, gap=12):
    out = []
    for i, kw in enumerate(items):
        if i:
            out.append(Spacer(1, gap))
        out.append(step(**kw))
    return out


def numbered_list(items, width, gap=7):
    """Plain numbered list (no bold title), for the R1 assembly sub-steps."""
    rows = [[CircleNum(i), Paragraph(t, sBody)]
            for i, t in enumerate(items, 1)]
    t = Table(rows, colWidths=[STEP_NUM_W, width - STEP_NUM_W])
    t.setStyle(TableStyle(NO_PAD + [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (1, 0), (1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -2), gap),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    return t


def data_table(header, rows, col_widths, small=False):
    """Header row on panel fill, 0.5 pt horizontal rules, no vertical rules."""
    head = sTableSmHead if small else sTableHead
    bold = sTableSmBold if small else sTableBold
    cell = sTableSm if small else sTable
    data = [[Paragraph(h, head) for h in header]]
    for r in rows:
        data.append([Paragraph(c, bold if j == 0 else cell)
                     for j, c in enumerate(r)])
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PANEL),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, BORDER),
        ("LINEABOVE", (0, 0), (-1, 0), 0.5, NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
    ]))
    return t


def panel_box(flowables, width, fill=PANEL, border=BORDER, pad=7):
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("BOX", (0, 0), (-1, -1), 0.5, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def warn_box(text, width):
    t = Table([[Paragraph(text, sWarn)]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WARN_FILL),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, WARN_RED),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def heading(text, kicker=None):
    rows = []
    if kicker:
        rows.append([Paragraph(kicker.upper(), sKicker)])
    rows.append([Paragraph(text, sH1)])
    t = Table(rows, colWidths=[FRAME_W])
    t.setStyle(TableStyle(NO_PAD + [
        ("LINEBELOW", (0, -1), (-1, -1), 1.0, NAVY),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 3),
    ]))
    return t


def bullet_list(items, width, style=None, gap=3):
    style = style or sBody
    rows = [[Paragraph("&bull;", style), Paragraph(t, style)] for t in items]
    t = Table(rows, colWidths=[11, width - 11])
    t.setStyle(TableStyle(NO_PAD + [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), gap),
    ]))
    return t


# ------------------------------------------------------------ doc template --
class BookletDoc(BaseDocTemplate):
    def __init__(self, path, model_label):
        BaseDocTemplate.__init__(
            self, path, pagesize=(PAGE_W, PAGE_H),
            leftMargin=MARGIN, rightMargin=MARGIN,
            topMargin=MARGIN, bottomMargin=MARGIN + FOOTER_H,
            title=f"OcuTrap {model_label} Manual",
            author="OcuTrap, Inc.",
            subject="Setup and quick reference",
        )
        self.model_label = model_label
        self.page_no = 0

        odd_frame = Frame(FOLD_MARGIN, MARGIN + FOOTER_H, FRAME_W, FRAME_H,
                          leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0, id="odd")
        even_frame = Frame(MARGIN, MARGIN + FOOTER_H, FRAME_W, FRAME_H,
                           leftPadding=0, rightPadding=0,
                           topPadding=0, bottomPadding=0, id="even")
        cover_frame = Frame(
            FOLD_MARGIN, MARGIN, FRAME_W,
            PAGE_H - COVER_BAND_H - 0.30 * inch - MARGIN,
            leftPadding=0, rightPadding=0,
            topPadding=0, bottomPadding=0, id="cover")

        self.addPageTemplates([
            PageTemplate(id="cover", frames=[cover_frame],
                         onPage=self._on_cover),
            PageTemplate(id="odd", frames=[odd_frame], onPage=self._on_body),
            PageTemplate(id="even", frames=[even_frame], onPage=self._on_body),
        ])

    def _on_cover(self, canv, doc):
        self.page_no += 1
        canv.saveState()
        canv.setFillColor(NAVY)
        canv.rect(0, PAGE_H - COVER_BAND_H, PAGE_W, COVER_BAND_H,
                  stroke=0, fill=1)
        canv.setFillColor(GOLD)
        canv.rect(0, PAGE_H - COVER_BAND_H - 3, PAGE_W, 3, stroke=0, fill=1)
        canv.restoreState()

    def _on_body(self, canv, doc):
        self.page_no += 1
        n = self.page_no
        x0 = FOLD_MARGIN if n % 2 == 1 else MARGIN
        x1 = x0 + FRAME_W
        y = MARGIN + 0.10 * inch
        canv.saveState()
        canv.setStrokeColor(BORDER)
        canv.setLineWidth(0.5)
        canv.line(x0, y + 11, x1, y + 11)
        canv.setFont("Helvetica", 8.5)
        canv.setFillColor(MUTED)
        canv.drawString(x0, y, f"OcuTrap {self.model_label}")
        canv.drawRightString(x1, y, str(n))
        canv.restoreState()


# ---------------------------------------------------------------- content ---
BUTTON_ROWS = [
    ("Check status", "Press User once",
     "Shows the state color for 5 seconds"),
    ("Open or close the door",
     "Press User once, then within 5 seconds press and hold User",
     "Blue flashes while opening, green while closing"),
    ("Arm", "Press User once, then within 5 seconds press Power once",
     "Yellow flashes, then yellow"),
    ("Unarm", "Same as Arm", "White flashes, then white"),
    ("Power off", "Hold Power about 3 seconds",
     "Red flashes, then solid red, then off"),
]

LIGHT_ROWS = [
    ("Breathing cyan", "Connected to the cloud (on external power)"),
    ("Blinking green", "Searching for cellular"),
    ("Blue flash every 10 s", "Unarmed, door open"),
    ("Green flash every 10 s", "Unarmed, door closed"),
    ("Yellow flash every 3 s", "Armed"),
    ("Yellow and blue alternating", "Scouting"),
    ("Magenta flash every 3 s", "Animal captured"),
    ("Blinking magenta (steady)", "Firmware update, leave powered on"),
    ("Solid red for 2 s after arming",
     "Arming blocked: clear the capture zone or clean the sensor window"),
    ("Solid red, staying on", "Battery critically low or trap shut down"),
    ("No light at all", "Off, hibernating, or failed boot"),
]

R2_BATTERY_TEXT = (
    "5,200 mAh pack (R2 default). Low alert at 20%, critical at 10%, auto "
    "power-off at 9.6 V. Charge at room temperature. Runtime is about 3 "
    "weeks on the 5,200 mAh pack and 40 days or more on the 10,000 mAh pack.")

R1_BATTERY_TEXT = (
    "US R1 units ship with the 10,000 mAh pack; some R1 units have the 5,200 "
    "mAh pack. In the app, set Battery Type to the pack you have so the "
    "low-battery alerts are right. Low alert at 20%, critical at 10%, auto "
    "power-off at 9.6 V. Charge at room temperature. Runtime is 40 days or "
    "more on the 10,000 mAh pack, about 3 weeks on the 5,200 mAh pack.")

CARE_ITEMS = [
    "Wipe the camera and sensor window with a soft lint-free cloth.",
    "Wipe the exterior.",
    "Clear debris from the door track.",
    "Check the battery terminals.",
    "Test open and close.",
]

CHARGE_STEP = ("Charge the battery.",
               "Use the included charger until its light turns green. About "
               "5 to 6 hours.")

ZIPTIE_STEP = ("Cut the motor zip tie.",
               "The motor is tied to the cage for shipping. Cut the tie only, "
               "never a wire. Keep fingers clear of the door. It can swing "
               "once the tie is cut.")

POD_STEP = ("Mount the POD.",
            "Slide it down the rails on the back of the cage. Snap the top "
            "clip. Screw the motor cable into the locking connector on the "
            "POD.")

BATTERY_STEP = ("Insert the battery.",
                "Open the POD latch, seat the battery in the bottom bracket, "
                "push the yellow connectors straight in, tuck the cables "
                "clear of the door, close the latch fully.")

POWER_STEP = ("Power on.",
              "Press the Power button. Breathing cyan means connected. First "
              "cellular connection can take up to 10 minutes.")

APP_STEP = ("Add the trap in the app.",
            "Go to app.ocutrap.com (or the mobile app), sign in, choose Add "
            "trap, and enter the Trap ID from the sticker on the cage and the "
            "Device ID from the sticker inside the POD. Pick Monthly or "
            "Annual. Your 30-day free trial starts when you set up billing.")

PLACE_STEP = ("Place it and arm it.",
              "Level ground, door facing the animal's path, bait behind the "
              "sensor line. Open the door, then set the arm mode to Armed in "
              "the app.")

POD_CLIP_IMG = "Screenshot 2025-12-17 at 10.26*.png"


def in_the_box(items, width):
    return panel_box([
        Paragraph("In the box", sH2),
        Spacer(1, 3),
        bullet_list(items, width - 14),
        Spacer(1, 3),
        Paragraph(
            f"Missing or damaged? Stop and email <b>{SUPPORT_EMAIL}</b> with "
            "your Trap ID.", sSmall),
    ], width)


# ------------------------------------------------------------ shared pages --
def cover_page(model, setup_url):
    """Page 1. The navy band is drawn by the cover page template."""
    story = []
    logo = reversed_logo(2.0 * inch, 0.42 * inch)
    if logo:
        band = Table([[logo]], colWidths=[FRAME_W],
                     rowHeights=[COVER_BAND_H - 0.30 * inch])
        band.setStyle(TableStyle(NO_PAD + [
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ]))
        story.append(Spacer(1, -(COVER_BAND_H - 0.30 * inch) - 0.30 * inch))
        story.append(band)
        story.append(Spacer(1, 0.34 * inch))
    else:
        story.append(Spacer(1, 0.10 * inch))

    story.append(Paragraph(f"OcuTrap {model}", sCoverTitle))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Setup and quick reference", sCoverSub))

    # TODO: swap for R2 photo. No R2 product photo exists in the repo yet, so
    # both models currently use the assembled-R1 hero shot on the cover.
    photo = fit_image(asset("DSC03816.JPG"), FRAME_W, 3.4 * inch)
    if photo:
        story.append(Spacer(1, 14))
        story.append(photo)
        story.append(Spacer(1, 22))

    lines = Table(
        [[Paragraph("<b>Read this before first use.</b>", sCoverLine)],
         [Paragraph("Full guide and videos: <b>docs.ocutrap.com</b>",
                    sCoverLine)],
         [Paragraph("App: <b>app.ocutrap.com</b>", sCoverLine)]],
        colWidths=[FRAME_W - 1.5 * inch],
    )
    lines.setStyle(TableStyle(
        NO_PAD + [("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))

    qr = qr_block(setup_url, "docs.ocutrap.com", 0.9 * inch,
                  label="Scan to set up", width=1.5 * inch)

    row = Table([[lines, qr]], colWidths=[FRAME_W - 1.5 * inch, 1.5 * inch])
    row.setStyle(TableStyle(NO_PAD + [
        ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
        ("VALIGN", (1, 0), (1, 0), "TOP"),
    ]))
    story.append(row)
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Support: {SUPPORT_EMAIL}", sSmall))
    return story


def buttons_page(with_photo=True):
    story = [heading("Buttons on the POD", kicker="Everyday use")]
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The Power button is on the left. The User button is on the right.",
        sLead))
    story.append(Spacer(1, 9))
    story.append(data_table(
        ["Action", "Steps", "Light"],
        BUTTON_ROWS,
        [1.15 * inch, 1.95 * inch, 1.50 * inch],
    ))
    story.append(Spacer(1, 11))
    if with_photo:
        row = image_row([(asset("pod-panel.png"), "The POD control panel")],
                        FRAME_W, height=2.0 * inch)
        if row:
            story.append(row)
            story.append(Spacer(1, 11))
    story.append(panel_box([
        Paragraph("Every button press also works in the app", sH2),
        Spacer(1, 3),
        Paragraph(
            "Open, close, arm, and unarm all work from app.ocutrap.com and "
            "from the mobile app. Use the buttons when you are standing at "
            "the trap.", sBody),
    ], FRAME_W))
    return story


def status_light_page():
    story = [heading("Status light", kicker="What the colors mean")]
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "On battery the light stays dark between short flashes. That is "
        "normal.", sLead))
    story.append(Spacer(1, 9))
    story.append(data_table(
        ["Light", "Meaning"],
        LIGHT_ROWS,
        [1.75 * inch, 2.85 * inch],
    ))
    story.append(Spacer(1, 16))
    story.append(Paragraph("After a capture", sH2))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "The door stays closed until you open it. The trap never releases on "
        "its own. In the app, tap Open to release. This also returns the trap "
        "to Unarmed.", sBody))
    story.append(Spacer(1, 10))
    story.append(warn_box(
        "Keep hands clear of the door. It closes in about 0.75 seconds and "
        "can pinch.", FRAME_W))
    return story


def buttons_and_lights_page():
    """Both reference tables on one page (R1 page 6)."""
    story = [heading("Buttons and lights", kicker="Everyday use")]
    story.append(Spacer(1, 5))

    story.append(Paragraph("Buttons on the POD", sH2))
    story.append(Paragraph(
        "Power button on the left, User button on the right.", sSmall))
    story.append(Spacer(1, 3))
    story.append(data_table(
        ["Action", "Steps", "Light"],
        BUTTON_ROWS,
        [1.15 * inch, 1.90 * inch, 1.55 * inch], small=True,
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Status light", sH2))
    story.append(Paragraph(
        "On battery the light stays dark between short flashes. That is "
        "normal.", sSmall))
    story.append(Spacer(1, 3))
    story.append(data_table(
        ["Light", "Meaning"],
        LIGHT_ROWS,
        [1.75 * inch, 2.85 * inch], small=True,
    ))
    return story


def battery_weather_care_page(with_after_capture, battery_text):
    story = [heading("Battery, weather, care", kicker="Keep it running")]
    story.append(Spacer(1, 5))

    if with_after_capture:
        story.append(Paragraph("After a capture", sH2))
        story.append(Spacer(1, 3))
        story.append(Paragraph(
            "The door stays closed until you open it. The trap never releases "
            "on its own. In the app, tap Open to release. This also returns "
            "the trap to Unarmed. Keep hands clear of the door: it closes in "
            "about 0.75 seconds and can pinch.", sBody))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Battery", sH2))
    story.append(Spacer(1, 3))
    story.append(Paragraph(battery_text, sBody))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Weather", sH2))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "Rated 0 &deg;C to 40 &deg;C (32 &deg;F to 104 &deg;F). Do not "
        "submerge. In freezing weather the door can ice. Check it before "
        "arming.", sBody))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Care after every capture and after harsh weather",
                           sH2))
    story.append(Spacer(1, 3))
    story.append(bullet_list(CARE_ITEMS, FRAME_W, gap=1))
    story.append(Spacer(1, 7))
    story.append(warn_box(
        "<b>Power off and unplug the battery before any maintenance.</b> Hold "
        "Power about 3 seconds, wait for the light to go out, then disconnect "
        "the yellow connectors.", FRAME_W))
    story.append(Spacer(1, 7))
    story.append(panel_box([
        Paragraph("Something not right?", sH2),
        Spacer(1, 2),
        Paragraph(
            "Troubleshooting and videos are at <b>docs.ocutrap.com</b>. Still "
            f"stuck? Email <b>{SUPPORT_EMAIL}</b> with your Trap ID and what "
            "the status light is doing.", sBody),
    ], FRAME_W, fill=white, pad=6))
    return story


def safety_page():
    story = [heading("Safety, compliance, warranty", kicker="Read and keep")]
    story.append(Spacer(1, 9))

    story.append(warn_box(
        "<b>Pinch hazard.</b> Keep hands, fingers, and face out of the door "
        "path at all times. Keep children and pets away from an armed trap.",
        FRAME_W))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Safety", sLegalHead))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "Power off before maintenance. Wear gloves when handling a captured "
        "animal. Do not touch the animal. Release it as soon as possible and "
        "follow local wildlife law. Battery: use only the included charger, "
        "do not expose it to fire, water, or heat, do not puncture or short "
        "the terminals, and dispose of it per local rules.", sLegal))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Use restrictions", sLegalHead))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "Do not use OcuTrap as a substitute for life safety or medical "
        "devices, for medical monitoring or life-sustaining applications, or "
        "in any way that breaks federal, state, local, or administrative law, "
        "including wildlife, animal welfare, health and safety, data privacy, "
        "and security law. Do not use it for criminal or illegal activity. Do "
        "not place it near life safety devices, medical monitoring equipment, "
        "or other sensitive devices it could interfere with. OcuTrap is not "
        "responsible for injury during use.", sLegal))
    story.append(Spacer(1, 8))

    story.append(Paragraph("FCC compliance", sLegalHead))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "This device complies with Part 15 of the FCC Rules. Operation is "
        "subject to the following two conditions: (1) This device may not "
        "cause harmful interference. (2) This device must accept any "
        "interference received, including interference that may cause "
        "undesired operation.", sLegal))
    story.append(Spacer(1, 4))
    story.append(Paragraph("FCC ID: 2AEMI-B404X", sLegal))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Changes or modifications not expressly approved by Particle "
        "Industries, Inc. could void the user's authority to operate the "
        "equipment. This equipment complies with FCC radiation exposure "
        "limits set forth for an uncontrolled environment. To maintain "
        "compliance, install and operate this device with a minimum distance "
        "of 20 centimeters between the radiator and your body.", sLegal))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Laser safety", sLegalHead))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "Class 1 laser product per IEC 60825-1:2014. Do not increase the "
        "laser output power by any means and do not use any optics to focus "
        "the laser beam.", sLegal))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Warranty", sLegalHead))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "12-month limited hardware warranty from the original purchase date. "
        "Full terms: ocutrap.com/pages/warranty", sLegal))

    footer = Table([[Paragraph(
        "OcuTrap, Inc. &middot; 5900 Balcones Drive, Suite 100, Austin, Texas "
        "78732, USA &middot; ocutrap.com &middot; support@ocutrap.com "
        "&middot; U.S. Patent No. 12,010,984 &middot; Manual v3, "
        "September 2026", sTiny)]], colWidths=[FRAME_W])
    footer.setStyle(TableStyle(NO_PAD + [
        ("LINEABOVE", (0, 0), (-1, 0), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
    ]))
    footer.hAlign = "LEFT"
    story.append(PushToBottom(footer, FRAME_W))
    story.append(footer)
    return story


def app_and_arm_page(app_step_num, place_step_num):
    story = [heading("Add the trap and arm it", kicker="Set up, continued")]
    story.append(Spacer(1, 9))
    story.append(step(app_step_num, APP_STEP[0], APP_STEP[1]))
    story.append(Spacer(1, 8))
    story.append(panel_box([
        Paragraph("Where the IDs are", sH2),
        Spacer(1, 3),
        Paragraph(
            "The <b>Trap ID</b> is on the sticker on the cage. The "
            "<b>Device ID</b> is on the sticker inside the POD.", sBody),
    ], FRAME_W))
    story.append(Spacer(1, 14))
    story.append(step(place_step_num, PLACE_STEP[0], PLACE_STEP[1]))
    story.append(Spacer(1, 20))
    story.append(qr_block(APP_URL, "app.ocutrap.com", 1.35 * inch,
                          label="Open the app", width=FRAME_W))
    story.append(Spacer(1, 20))
    story.append(panel_box([
        Paragraph("Bait it, then arm it", sH2),
        Spacer(1, 3),
        Paragraph(
            "Arming is blocked while something sits in the capture zone. If "
            "the light goes solid red for 2 seconds when you arm, clear the "
            "zone or clean the sensor window and try again.", sBody),
    ], FRAME_W))
    return story


# --------------------------------------------------------------- R2 pages --
def r2_page2():
    story = [heading("Set up your R2", kicker="About 10 minutes, no tools")]
    story.append(Spacer(1, 9))
    story.append(Paragraph(
        "The R2 ships with the door and motor installed.", sLead))
    story.append(Spacer(1, 9))
    story.append(in_the_box([
        "Cage with door and motor",
        "POD (camera, sensor, electronics)",
        "Battery (5,200 mAh) and charger",
        "This guide",
    ], FRAME_W))
    story.append(Spacer(1, 14))
    story.extend(steps_stack([
        dict(num=1, title=CHARGE_STEP[0], body=CHARGE_STEP[1],
             image=asset("setup-charging-battery.png"),
             caption="The charger light turns green when the pack is full",
             img_h=1.95 * inch),
        dict(num=2, title=ZIPTIE_STEP[0], body=ZIPTIE_STEP[1]),
    ], gap=14))
    return story


def r2_page3():
    story = [heading("Mount the POD", kicker="Set up, continued")]
    story.append(Spacer(1, 9))
    story.extend(steps_stack([
        dict(num=3, title=POD_STEP[0], body=POD_STEP[1],
             images=[(asset("image.png"), "The POD"),
                     (asset(POD_CLIP_IMG), "Snap the top clip")],
             img_h=2.45 * inch),
        dict(num=4, title=BATTERY_STEP[0], body=BATTERY_STEP[1]),
        dict(num=5, title=POWER_STEP[0], body=POWER_STEP[1]),
    ], gap=14))
    return story


# --------------------------------------------------------------- R1 pages --
def r1_page2():
    story = [heading("Set up your R1", kicker="About 30 minutes")]
    story.append(Spacer(1, 9))
    story.append(Paragraph(
        "The R1 ships as a kit. Assembly takes about 30 minutes with the "
        "included nut driver.", sLead))
    story.append(Spacer(1, 9))
    story.append(in_the_box([
        "Cage",
        "Parts box: door, rod, brackets, motor, handle kit, POD, battery "
        "(10,000 mAh in the US), charger, nut driver, nut assembly tool",
    ], FRAME_W))
    story.append(Spacer(1, 14))
    story.append(step(1, CHARGE_STEP[0],
                      CHARGE_STEP[1] + " Start it now so the pack is ready "
                      "when assembly is done."))
    story.append(Spacer(1, 14))

    imgs = image_row([
        (asset("cage.png"), "Cage"),
        (asset("parts-box.png"), "Parts box"),
        (asset("charger.png"), "Charger"),
    ], FRAME_W, height=1.6 * inch)
    if imgs:
        story.append(imgs)
        story.append(Spacer(1, 16))

    story.append(Paragraph("Assembly order", sH2))
    story.append(Spacer(1, 5))
    cell = ParagraphStyle("Ord", parent=sBody, alignment=TA_CENTER)
    order = Table([[
        Paragraph("<b>Door</b><br/><font size=8 color='#6f6c65'>page 3</font>",
                  cell),
        Paragraph("<b>Motor</b><br/><font size=8 color='#6f6c65'>page 4</font>",
                  cell),
        Paragraph(
            "<b>Handle</b><br/><font size=8 color='#6f6c65'>page 4</font>",
            cell),
        Paragraph("<b>POD</b><br/><font size=8 color='#6f6c65'>page 5</font>",
                  cell),
    ]], colWidths=[FRAME_W / 4.0] * 4)
    order.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PANEL),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(order)
    story.append(Spacer(1, 9))
    story.append(Paragraph(
        "Follow the sections in order. Full assembly videos are at "
        "<b>docs.ocutrap.com</b>.", sSmall))
    return story


def r1_page3():
    story = [heading("1. Door", kicker="Section 1, steps 1 and 2")]
    story.append(Spacer(1, 9))

    story.append(Paragraph("Step 1: Components needed for setup", sH2))
    story.append(Spacer(1, 5))
    story.append(panel_box([
        Paragraph(
            "<b>Door:</b> 2x brackets (top locking mechanism), 2x black "
            "spacers, 2x black capped nuts, 1x metal door, 1x 12&rdquo; rod, "
            "1x nut driver, 1x nut assembly tool", sBody),
        Spacer(1, 5),
        Paragraph("<b>Motor:</b> 1x motor, 2x pins, 2x clevises", sBody),
    ], FRAME_W))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Step 2: Set up the door mechanism", sH2))
    story.append(Spacer(1, 6))
    story.append(numbered_list([
        "Align the metal door inside the trap.",
        "Thread the metal rod through the oval slot in the metal bracket "
        "attached to the top of the solid metal trap door.",
        "On each end of the rod, place a black spacer, then secure it with a "
        "black capped nut on both sides. Use the nut assembly tool and the "
        "nut driver on each end to tighten the nut until snug.",
    ], FRAME_W))
    story.append(Spacer(1, 14))

    # The two source filenames are swapped relative to what they draw:
    # nut-tool.png is the rod/spacer/nut assembly, door-rod-diagram.png is the
    # nut going into the assembly tool. Caption by content, not by filename.
    imgs = image_row([
        (asset("nut-tool.png"), "Rod, spacers, and capped nuts"),
        (asset("door-rod-diagram.png"), "Nut assembly tool"),
    ], FRAME_W, height=1.6 * inch)
    if imgs:
        story.append(imgs)
        story.append(Spacer(1, 14))

    story.append(panel_box([
        Paragraph("Hardware note", sH2),
        Spacer(1, 3),
        Paragraph(
            "Some assembly videos show an earlier door rod with white washers "
            "and springs. Current R1 units ship with <b>black spacers and "
            "black capped nuts</b>. Follow the written steps here, which "
            "match the parts in your box.", sBody),
    ], FRAME_W))
    return story


def r1_page4():
    story = [heading("2. Motor and handle",
                     kicker="Section 1 step 3, and section 2")]
    story.append(Spacer(1, 9))

    story.append(Paragraph("Step 3: Set up the motor", sH2))
    story.append(Spacer(1, 6))
    story.append(numbered_list([
        "Install the top bracket with washers and bolts. Tighten with the "
        "nut driver.",
        "Use the pins and clevises to secure the motor to the door at both "
        "the top and bottom attachment points.",
        "Feed the cable through the metal handle.",
        "Verify that all components are securely fastened.",
        "Check that the door moves smoothly and is properly aligned.",
    ], FRAME_W, gap=6))
    story.append(Spacer(1, 13))

    story.append(Paragraph("Handle: gather your components", sH2))
    story.append(Spacer(1, 5))
    story.append(panel_box([
        Paragraph(
            "4x 3&rdquo; bolt, 1x handle guard, 1x tube, 4x washers, 2x top "
            "handle metal bracket, 2x upper tube plastic spacer, 2x lower "
            "tube plastic handle spacer, 2x internal trap bracket with "
            "press-fit nut, 1x nut driver", sBody),
    ], FRAME_W))
    story.append(Spacer(1, 13))

    story.append(Paragraph("Handle: screw in the handle", sH2))
    story.append(Spacer(1, 6))
    story.append(numbered_list([
        "Center the handle guard on the trap.",
        "Insert the two top handle pieces into the holes in the handle guard.",
        "Slide the tube between the two handle guards and make sure it is "
        "centered.",
        "Place the bracket (with the press-fit nut) inside the trap and "
        "hand-tighten the bolts.",
    ], FRAME_W, gap=6))
    story.append(Spacer(1, 13))
    story.append(warn_box(
        "Do not fully tighten the bolts until the motor connector is fully "
        "through the tube.", FRAME_W))
    return story


def r1_page5():
    """POD, battery, power on, then the app and arming. All of section 3."""
    story = [heading("3. POD, power, app", kicker="Section 3")]
    story.append(Spacer(1, 7))
    story.append(step(
        1, POD_STEP[0],
        POD_STEP[1] + " Now fully tighten all the bolts, including the handle "
        "bolts you hand-tightened earlier."))
    story.append(Spacer(1, 9))
    story.append(step(2, BATTERY_STEP[0], BATTERY_STEP[1]))
    story.append(Spacer(1, 5))
    story.append(panel_box([
        Paragraph(
            "US R1 units ship with the 10,000 mAh pack. In the app, set "
            "<b>Battery Type</b> to the pack you have so the low-battery "
            "alerts are right.", sBody),
    ], FRAME_W))
    story.append(Spacer(1, 9))
    story.append(step(3, POWER_STEP[0], POWER_STEP[1]))
    story.append(Spacer(1, 9))
    story.append(step(4, APP_STEP[0], APP_STEP[1]))
    story.append(Spacer(1, 9))
    story.append(step(5, PLACE_STEP[0], PLACE_STEP[1]))
    return story


# ---------------------------------------------------------------- builders --
MODELS = {
    "r2": {
        "label": "R2",
        "pages": 8,
        "setup_url": "https://docs.ocutrap.com/getting-started/setting-up-r2",
    },
    "r1": {
        "label": "R1",
        "pages": 8,
        "setup_url": "https://docs.ocutrap.com/getting-started/setting-up",
    },
}


def r2_pages(cfg):
    return [
        cover_page("R2", cfg["setup_url"]),   # 1 cover
        r2_page2(),                           # 2 in the box, charge, zip tie
        r2_page3(),                           # 3 POD, battery, power on
        app_and_arm_page(6, 7),               # 4 add the trap, place and arm
        buttons_page(with_photo=True),        # 5 buttons on the POD
        status_light_page(),                  # 6 status light, after a capture
        battery_weather_care_page(False, R2_BATTERY_TEXT),
                                              # 7 battery, weather, care
        safety_page(),                        # 8 safety and legal
    ]


def r1_pages(cfg):
    return [
        cover_page("R1", cfg["setup_url"]),   # 1 cover
        r1_page2(),                           # 2 in the box, charge, order
        r1_page3(),                           # 3 door
        r1_page4(),                           # 4 motor and handle
        r1_page5(),                           # 5 POD, power, app, arm
        buttons_and_lights_page(),            # 6 buttons + status light
        battery_weather_care_page(True, R1_BATTERY_TEXT),
                                              # 7 after a capture, battery,
                                              #   weather, care
        safety_page(),                        # 8 safety and legal
    ]


def build_reading_order(model_key):
    cfg = MODELS[model_key]
    label = cfg["label"]
    out = os.path.join(OUT_DIR, f"{label}_Manual.pdf")
    os.makedirs(OUT_DIR, exist_ok=True)

    pages = r2_pages(cfg) if model_key == "r2" else r1_pages(cfg)

    story = []
    for i, page in enumerate(pages):
        if i > 0:
            story.append(
                NextPageTemplate("odd" if (i + 1) % 2 == 1 else "even"))
            story.append(PageBreak())
        story.extend(page)

    doc = BookletDoc(out, label)
    doc.build(story)
    return out, cfg["pages"]


def _fold_line_overlay():
    """A letter-landscape page carrying only the faint dashed fold line."""
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    _TMP_FILES.append(tmp.name)
    c = pdfcanvas.Canvas(tmp.name, pagesize=(SHEET_W, SHEET_H))
    c.setStrokeColor(HexColor("#b8b5ae"))
    c.setLineWidth(0.3)
    c.setDash(3, 3)
    c.line(SHEET_W / 2.0, 0.2 * inch, SHEET_W / 2.0, SHEET_H - 0.2 * inch)
    c.showPage()
    c.save()
    return tmp.name


def build_2up(src, dst):
    """Impose the half-letter reading-order PDF onto letter-landscape sheets."""
    from pypdf import PdfReader, PdfWriter, PageObject, Transformation

    reader = PdfReader(src)
    n = len(reader.pages)
    if n % 4 != 0:
        raise SystemExit(f"{src}: {n} pages is not a multiple of 4")

    fold_page = PdfReader(_fold_line_overlay()).pages[0]

    writer = PdfWriter()
    for k in range(n // 4):
        for left_no, right_no in ((n - 2 * k, 2 * k + 1),
                                  (2 * k + 2, n - 2 * k - 1)):
            sheet = PageObject.create_blank_page(width=SHEET_W, height=SHEET_H)
            sheet.merge_transformed_page(reader.pages[left_no - 1],
                                         Transformation())
            sheet.merge_transformed_page(reader.pages[right_no - 1],
                                         Transformation().translate(PAGE_W, 0))
            sheet.merge_page(fold_page)
            writer.add_page(sheet)

    with open(dst, "wb") as fh:
        writer.write(fh)
    return dst, len(writer.pages)


def cleanup():
    for p in _TMP_FILES:
        try:
            os.unlink(p)
        except OSError:
            pass


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", choices=["r1", "r2", "all"], default="all")
    args = ap.parse_args()

    keys = ["r2", "r1"] if args.model == "all" else [args.model]
    failed = False
    for key in keys:
        out, expected = build_reading_order(key)
        from pypdf import PdfReader
        got = len(PdfReader(out).pages)
        ok = got == expected
        print(f"  {out}  {got} pages  "
              f"({'ok' if ok else 'WRONG PAGE COUNT'}, expected {expected})")
        if not ok:
            failed = True
            continue
        two_up = out.replace(".pdf", "_print-2up.pdf")
        _, sheets = build_2up(out, two_up)
        print(f"  {two_up}  {sheets} sheet sides")

    cleanup()
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
