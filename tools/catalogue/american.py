"""NovoTech's American-style section for the catalogue edition (pages 272 – 278): EUROSTAMP's American-style punches
and dies (.500″ tang), laid out like the rest of the catalogue — opener, overview, two pages of punches, two of dies —
and the Z1 intermediate that takes American-style punches.

The drawings are EUROSTAMP's own vector drawings (dimensions in decimal inches), placed as they are; the millimetre
value of every dimension is added beside it in the catalogue's metric blue.  Specifications and part numbers are
EUROSTAMP's (see tools/eurostamp_pages.py for the same data on the website).

    python3 tools/catalogue/american.py      → tools/cache/edition/american.pdf
"""
import os
import re
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import page6 as P6                       # noqa: E402  (Ink, fonts)
import placer as PL                      # noqa: E402
import textmodel as TM                   # noqa: E402
from logo import place_logo              # noqa: E402
from fonts import font                   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = "/home/claude/eurostamp/pdf"
PUN = os.path.join(SRC, "american_punches.pdf")
DIE = os.path.join(SRC, "american_dies.pdf")
OUT = os.path.join(ROOT, "tools", "cache", "edition", "american.pdf")
HERO = os.path.join(ROOT, "src", "img", "tooling", "es-am-hero-1200.webp")
W, H = 595.276, 841.89
FIRST = 272                                      # page numbers go on from EUROSTAMP's last page (271)

GREEN = (0.180, 0.545, 0.341)                    # the section's colour (EUROSTAMP: red, blue, purple, orange, grey)
BLUE = (0.0, 0.337, 0.533)                       # EUROSTAMP's codes and metric dimensions
INK = (0.137, 0.122, 0.125)
GREY = (0.35, 0.35, 0.36)
RULE = (0.82, 0.826, 0.832)
FRAME = (0.584, 0.661, 0.795)
WHITE = (1, 1, 1)
F = dict(P6.F, BI=os.path.join(P6.FD, "Roboto-BlackItalic.ttf"), I=os.path.join(P6.FD, "Roboto-Italic.ttf"),
         LI=os.path.join(P6.FD, "Roboto-LightItalic.ttf"), SX=os.path.join(P6.FD, "RobotoSlab-ExtraBold.ttf"))
P6.F.update(F)

STD = "std"                                      # 36″, 18″ and 35.75″ sectioned, each with its part number
PUNCHES = [
    dict(code="S28932", model="EP2-88", kind="straight punch", a=88, h=(3.779, 95.98), r=(.059, 1.5), clip=(508, 10, 645, 268)),
    dict(code="S28881", model="EGPC 88", kind="gooseneck punch", a=88, h=(3.779, 95.99), r=(.031, 0.8), clip=(158, 12, 322, 270)),
    dict(code="S28880", model="EGPC 85", kind="gooseneck punch", a=85, h=(3.779, 95.99), r=(.031, 0.8), clip=(342, 12, 494, 270)),
    dict(code="S28974", model="EGP-7A-88", kind="straight punch", a=88, h=(3.778, 95.97), r=(.031, 0.8), clip=None),
    dict(code="S29083", model="EP30", kind="acute punch", a=30, h=(3.780, 96.0), r=(.059, 1.5), clip=(314, 296, 472, 556)),
    dict(code="S29252", model=None, kind="acute punch", a=28, h=(3.780, 96.01), r=(.031, 0.8), clip=(166, 296, 320, 550),
         lengths="request"),
    dict(code="S29084", model="EGP28", kind="acute gooseneck punch", a=28, h=(5.125, 130.18), r=(.031, 0.8),
         clip=(518, 268, 686, 576)),
]
DIES = [
    dict(code="S28946", model="ELD88-3/8", kind="1V die", a=88, v=(.375, 9.53), r=(.045, 1.14), w=(1.000, 25.4), clip=(18, 84, 212, 288)),
    dict(code="S29269", model=None, kind="1V die", a=88, v=(.500, 12.70), r=(.039, 0.99), w=(1.000, 25.4), clip=(230, 96, 404, 282),
         lengths="request"),
    dict(code="S29145", model="ELD88-5/8", kind="1V die", a=88, v=(.626, 15.90), r=(.075, 1.91), w=(1.000, 25.4), clip=(432, 98, 610, 292)),
    dict(code="S28947", model="ELD88-3/4", kind="1V die", a=88, v=(.750, 19.05), r=(.150, 3.81), w=(1.500, 38.1), clip=(610, 98, 808, 292)),
    dict(code="S29142", model="ELD30-3/8", kind="acute 1V die", a=30, v=(.375, 9.53), r=(.045, 1.14), w=(1.000, 25.4), clip=(14, 302, 207, 492)),
    dict(code="S29141", model="ELD30-1/2", kind="acute 1V die", a=30, v=(.500, 12.70), r=(.045, 1.14), w=(1.000, 25.4), clip=(230, 302, 420, 494)),
    dict(code="S29143", model="ELD30-5/8", kind="acute 1V die", a=30, v=(.635, 16.13), r=(.059, 1.50), w=(1.500, 38.1), clip=(420, 316, 611, 494)),
    dict(code="S29144", model="ELD34-7/8", kind="acute 1V die", a=34, v=(.875, 22.23), r=(.091, 2.31), w=(2.000, 50.8), clip=(612, 316, 824, 497)),
]
LENGTHS = [("36″", "914.4 mm", "", "091401"), ("18″", "457.2 mm", "", "045701"), ("35.75″", "908 mm", "SECTIONED", "090801")]
SET = [(4, "4″", "horn"), (.5, "½″", ""), (3, "3″", ""), (2, "2″", ""), (1, "1″", ""), (8, "8″", ""), (.75, "¾″", ""),
       (12, "12″", ""), (.5, "½″", ""), (4, "4″", "horn")]


def inch(v):
    s = f"{v:.3f}"
    return s[1:] if s.startswith("0.") else s


def mm_txt(v):
    v = round(v + 1e-9, 2 if v < 10 else 1)                  # 9.525 → 9.53 (half up, as EUROSTAMP rounds)
    s = f"{v:.2f}" if v < 10 else f"{v:.1f}"
    s = s.rstrip("0").rstrip(".")
    return s


# ------------------------------------------------------------------------------------------------------- sources
_SRC = {}


def source(path):
    """the drawing sheet with its code call-outs ('S28881 →') taken out: the catalogue sets the code as a heading"""
    if path in _SRC:
        return _SRC[path]
    doc = fitz.open(path)
    p = doc[0]
    for w in p.get_text("words"):
        if not re.fullmatch(r"S2\d{4}", w[4]):
            continue
        cy = (w[1] + w[3]) / 2
        lead = [d["rect"] for d in p.get_drawings()
                if abs((d["rect"].y0 + d["rect"].y1) / 2 - cy) < 3 and w[2] - 1 <= d["rect"].x0 < w[2] + 30 and d["rect"].height < 5]
        tip = max([r.x1 for r in lead] + [w[2]])
        p.add_redact_annot(fitz.Rect(w[0] - 1, cy - 2.6, tip + 0.4, cy + 2.6), fill=False)
    p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                       text=fitz.PDF_REDACT_TEXT_REMOVE)
    _SRC[path] = doc
    return doc


def one_drawing(path, clip):
    """the sheet with everything outside `clip` taken out — the text too, which a clipped placement would still carry
    (invisible, but there for text extraction and for the inch / mm pairing)"""
    clip = fitz.Rect(clip)
    doc = fitz.open()
    doc.insert_pdf(source(path))
    p = doc[0]
    R = p.rect
    for r in (fitz.Rect(R.x0, R.y0, R.x1, clip.y0), fitz.Rect(R.x0, clip.y1, R.x1, R.y1),
              fitz.Rect(R.x0, clip.y0, clip.x0, clip.y1), fitz.Rect(clip.x1, clip.y0, R.x1, clip.y1)):
        if r.width > 0 and r.height > 0:
            p.add_redact_annot(r, fill=False)
    p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                       text=fitz.PDF_REDACT_TEXT_REMOVE)
    return doc


def place_drawing(page, path, clip, box, max_scale=1.05):
    """the drawing `clip` of the sheet, as large as fits `box` (centred across, top-aligned); returns where it went"""
    clip = fitz.Rect(clip)
    s = min(box.width / clip.width, box.height / clip.height, max_scale)
    w, h = clip.width * s, clip.height * s
    r = fitz.Rect(box.x0 + (box.width - w) / 2, box.y0, box.x0 + (box.width + w) / 2, box.y0 + h)
    page.show_pdf_page(r, one_drawing(path, clip), 0, clip=clip)
    return r


# ------------------------------------------------------------------------------------------------------- page parts
def chrome(page, num, title=None):
    """title bar, style tab (odd pages), page number, NovoTech logo"""
    ink = P6.Ink(page)
    if title:
        w = ink.width(title, 13, "SL")
        sh = page.new_shape()
        sh.draw_rect(fitz.Rect(0, 28.4, max(317.0, 34 + w + 24), 47.4))
        sh.finish(color=None, fill=GREEN, width=0)
        sh.commit()
        ink.put(34.0, 42.4, title, 13, "SL", WHITE)
    if num % 2:
        sh = page.new_shape()
        sh.draw_rect(fitz.Rect(567.0, 0, W, 177.0))
        sh.finish(color=None, fill=GREEN, width=0)
        sh.commit()
        ink.put(538.5, 811.7, str(num), 18, "T", GREEN, "right")
    else:
        ink.put(51.5, 811.7, str(num), 18, "T", GREEN)
    ink.flush()
    if num % 2:
        tab = "AMERICAN STYLE"
        fo = font(F["B"])
        tw = fitz.TextWriter(page.rect)
        y = 88.5 + fo.text_length(tab, 11) / 2
        tw.append(fitz.Point(584.5, y), tab, font=fo, fontsize=11)
        tw.write_text(page, color=WHITE, morph=(fitz.Point(584.5, y), fitz.Matrix(90)))
    place_logo(page)


def heading(ink, x, y, item):
    """'S28881' in the catalogue's code style, the model and type under it"""
    ink.put(x, y, item["code"], 20, "BI", BLUE)
    sub = (item["model"] + " · " if item["model"] else "") + item["kind"]
    ink.put(x, y + 13.5, sub, 9, "M", BLUE)


def spec_block(page, ink, x, y, lines, width=150.0):
    """the tool data lines ('H = 3.779″ (95.99 mm)'), framed on top and right like EUROSTAMP's"""
    lh = 13.4
    for k, (lab, val) in enumerate(lines):
        yy = y + 11 + k * lh
        xx = x + ink.put(x, yy, lab, 10.5, "R", INK)
        ink.put(xx, yy, " = " + val, 10.5, "L", INK)
    bot = y + 14 + (len(lines) - 1) * lh + 4
    sh = page.new_shape()
    sh.draw_line(fitz.Point(x - 3, y - 1), fitz.Point(x + width, y - 1))
    sh.draw_line(fitz.Point(x + width, y - 1), fitz.Point(x + width, bot))
    sh.finish(color=RULE, width=0.6, closePath=False)
    sh.commit()
    return bot


def pn_box(page, ink, x, y, item, width=150.0):
    """lengths and EUROSTAMP part numbers: 36″, 18″ and the 35.75″ sectioned set"""
    if item.get("lengths") == "request":
        ink.put(x, y + 8, "Lengths and part numbers on request.", 7.2, "LI", INK)
        return y + 12
    rh, mid = 11.2, x + width * 0.5
    sh = page.new_shape()
    sh.draw_rect(fitz.Rect(x, y, x + width, y + 3 * rh))
    sh.finish(color=FRAME, fill=WHITE, width=0.4)
    for k in range(1, 3):
        sh.draw_line(fitz.Point(x, y + k * rh), fitz.Point(x + width, y + k * rh))
    sh.draw_line(fitz.Point(mid, y), fitz.Point(mid, y + 3 * rh))
    sh.finish(color=FRAME, width=0.4)
    sh.commit()
    for k, (a, b, tag, suf) in enumerate(LENGTHS):
        yy = y + k * rh + 7.7
        xx = x + 2.4 + ink.put(x + 2.4, yy, a, 6.6, "R", INK)
        xx += ink.put(xx, yy, " " + b, 6.0, "L", INK)
        if tag:
            ink.put(xx + 2.0, yy, tag, 4.3, "L", INK)
        ink.put(x + width - 2.4, yy, item["code"] + suf, 6.6, "L", INK, "right")
    return y + 3 * rh


DIM_RE = re.compile(r"^(R\s?)?(\d*\.\d{3})$")


def mm_values(page, areas, mm_of=None, order=("after", "below", "before", "above")):
    """the millimetres of every inch dimension inside `areas` (the drawings), beside or under it in metric blue.
    `mm_of`: the millimetres to write for an inch text, where the drawing was made in millimetres (the intermediate)"""
    runs = TM.runs(page, None)
    cv = PL.Canvas(page, runs)
    polys = {id(r): r.outline() for r in runs}
    n, miss = 0, []
    reach = [fitz.Rect(a) for a in areas]                  # each drawing with the millimetres written round it
    for r in runs:
        m = DIM_RE.match(r.t)
        if not m or not any(a.contains(r.origin) for a in areas):
            continue
        k = next(j for j, a in enumerate(areas) if a.contains(r.origin))
        v = float(m.group(2)) * 25.4
        t = ("R " if m.group(1) else "") + (mm_of[r.t] if mm_of else mm_txt(v)) + " mm"
        others = [polys[id(o)] for o in runs if o is not r]
        res = PL.place(cv, r, (f"({t})", t), others, order=list(order), weight="light",
                       color=BLUE, stages=[("clean", 0.78), ("clean", 0.68), ("light", 0.68), ("clean", 0.6),
                                           ("knock", 0.68), ("knock", 0.6)])
        if res:
            n += 1
            x0, y0, x1, y1 = res["poly"].bounds
            reach[k] |= fitz.Rect(x0, y0, x1, y1)
        else:
            miss.append(r.t)
    return n, miss, reach


# ------------------------------------------------------------------------------------------------------- pages
def opener(doc, num):
    page = doc.new_page(width=W, height=H)
    sh = page.new_shape()
    sh.draw_rect(page.rect)
    sh.finish(color=None, fill=GREEN, width=0)
    sh.commit()
    # the profiles, large, in the lower half
    png = os.path.join(os.path.dirname(OUT), "am-hero.png")
    if not os.path.exists(png):
        from PIL import Image
        Image.open(HERO).save(png)                               # MuPDF reads no WebP
    page.insert_image(fitz.Rect(-20, 470, W + 20, 470 + (W + 40) * 599 / 1200), filename=png, keep_proportion=True)
    # EUROSTAMP's white logo from the Bystronic opener
    cat = fitz.open(P6.CAT)
    tmp = fitz.open()
    tmp.insert_pdf(cat, from_page=169, to_page=169)
    tp = tmp[0]
    tp.add_redact_annot(tp.rect, fill=False)                 # the logo's vectors only: no photo, no text
    tp.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                        text=fitz.PDF_REDACT_TEXT_REMOVE)
    page.show_pdf_page(fitz.Rect(137.0, 174.0, 357.0, 223.0), tmp, 0, clip=fitz.Rect(137.0, 174.0, 357.0, 223.0))
    ink = P6.Ink(page)
    ink.put(356.0, 294.0, "AMERICAN", 44, "SX", WHITE, "right")
    ink.put(356.0, 347.0, "STYLE", 44, "SX", WHITE, "right")
    ink.flush()
    html = ('<p class="r w bo" style="font-size:10px; margin-bottom:9px">The upper and lower tools in this section fit press '
            "brakes with American-style clamping: a .500″ (12.7 mm) tang held by the upper and lower clamps.</p>"
            '<p class="r w" style="font-size:10px; margin-bottom:9px">Punches and dies in 36″ (914.4 mm) full lengths, '
            "18″ (457.2 mm) half lengths and 35.75″ (908 mm) sectioned sets, each with its own EUROSTAMP part number.</p>"
            '<p class="r w" style="font-size:10px">Every dimension is given in decimal inches with the millimetres '
            "beside it.</p>")
    import textflow as TF
    page.insert_htmlbox(fitz.Rect(80, 387.5, 357.5, 470), html, css=TF.CSS, archive=TF.ARCHIVE)
    ink = P6.Ink(page)
    ink.put(51.5, 811.7, str(num), 18, "T", WHITE)
    ink.flush()
    place_logo(page)
    return page


def overview(doc, num):
    import textflow as TF
    page = doc.new_page(width=W, height=H)
    ink = P6.Ink(page)
    html = ('<p class="t" style="margin-bottom:8px">AMERICAN-STYLE PUNCHES AND DIES — TANG .500″ (12.7 MM)</p>'
            "<p>EUROSTAMP’s American-style tools fit press brakes with American-style clamping, where a .500″ (12.7 mm) "
            "tang is held in the upper and lower clamps. The punches have the safety lip that keeps them from falling "
            "out when the clamp is opened; all the dies share one working height, 1.937″ (49.2 mm), so a punch stays in "
            "step with every die in the range.</p>"
            "<p>Every profile comes in three lengths, each with its own part number: 36″ (914.4 mm) full lengths, "
            "18″ (457.2 mm) half lengths and 35.75″ (908 mm) sectioned sets. Like the rest of this catalogue, the tools "
            "are made in Italy by EUROSTAMP and supplied in Canada by NovoTech.</p>")
    page.insert_htmlbox(fitz.Rect(34, 70, 561, 190), html, css=TF.CSS, archive=TF.ARCHIVE)
    # two panels: punch tang, die tang and heights
    panels = [(34, "PUNCH TANG", [("Tang width", ".500″ (12.70 mm)"), ("Tang with safety lip", ".626″ (15.90 mm)"),
                                  ("Safety groove", ".220″ (5.59 mm)"), ("Tang height", ".752″ (19.10 mm)"),
                                  ("Punch heights", "3.779″ (96 mm) · 5.125″ (130.18 mm)")]),
              (304, "DIE TANG AND HEIGHTS", [("Tang width", ".500″ (12.70 mm)"), ("Working height", "1.937″ (49.20 mm)"),
                                            ("Overall height", "2.563″ (65.10 mm)"),
                                            ("Body widths", "1.000″ · 1.500″ · 2.000″"),
                                            ("", "(25.4 · 38.1 · 50.8 mm)")])]
    for x0, title, rows in panels:
        y0 = 200
        sh = page.new_shape()
        sh.draw_rect(fitz.Rect(x0, y0, x0 + 257, y0 + 22))
        sh.finish(color=None, fill=GREEN, width=0)
        sh.draw_rect(fitz.Rect(x0, y0 + 22, x0 + 257, y0 + 22 + len(rows) * 17 + 8))
        sh.finish(color=None, fill=(0.94, 0.95, 0.95), width=0)
        sh.commit()
        ink.put(x0 + 10, y0 + 15.2, title, 10, "M", WHITE)
        for k, (a, b) in enumerate(rows):
            yy = y0 + 22 + 16 + k * 17
            ink.put(x0 + 10, yy, a, 9, "L", INK)
            ink.put(x0 + 247, yy, b, 9, "R", INK, "right")
    # part numbers
    y0 = 360
    ink.put(34, y0, "PART NUMBERS", 10, "M", BLUE)
    cols = [(34, "Length"), (230, "Part number ends in"), (390, "Example: S28881 gooseneck punch")]
    sh = page.new_shape()
    sh.draw_rect(fitz.Rect(34, y0 + 8, 561, y0 + 26))
    sh.finish(color=None, fill=BLUE, width=0)
    sh.commit()
    for x, t in cols:
        ink.put(x + 6, y0 + 20.5, t, 8.5, "M", WHITE)
    rows = [("36″ (914.4 mm) full length", "091401", "S28881091401"), ("18″ (457.2 mm) half length", "045701", "S28881045701"),
            ("35.75″ (908 mm) sectioned set", "090801", "S28881090801")]
    for k, row in enumerate(rows):
        yy = y0 + 26 + k * 17
        sh = page.new_shape()
        sh.draw_line(fitz.Point(34, yy + 17), fitz.Point(561, yy + 17))
        sh.finish(color=RULE, width=0.5)
        sh.commit()
        for (x, _), t in zip(cols, row):
            ink.put(x + 6, yy + 11.8, t, 9, "L", INK)
    # the sectioned sets
    y0 = 470
    ink.put(34, y0, "SECTIONED SETS — 35.75″ (908 MM)", 10, "M", BLUE)
    total = sum(s for s, _, _ in SET)
    x0, x1 = 40.0, 555.0
    k_in = (x1 - x0) / total
    for row, (label, horn) in enumerate((("PUNCH", True), ("DIE", False))):
        top = y0 + 22 + row * 120
        ink.put(34, top - 6, label, 8.5, "M", INK)
        bh = 30.0 if horn else 26.0
        sh = page.new_shape()
        x = x0
        for k, (s, t, note) in enumerate(SET):
            w = s * k_in
            a, b = x, x + w
            if horn and k == 0:
                pts = [fitz.Point(a + 9, top), fitz.Point(b, top), fitz.Point(b, top + bh), fitz.Point(a, top + bh),
                       fitz.Point(a, top + bh - 9)]
                sh.draw_polyline(pts + [pts[0]])
            elif horn and k == len(SET) - 1:
                pts = [fitz.Point(a, top), fitz.Point(b - 22, top), fitz.Point(b, top + bh - 10), fitz.Point(b, top + bh),
                       fitz.Point(a, top + bh)]
                sh.draw_polyline(pts + [pts[0]])
            else:
                sh.draw_rect(fitz.Rect(a + 0.8, top, b - 0.8, top + bh))
            x = b
        sh.finish(color=(0.2, 0.2, 0.22), fill=(0.885, 0.894, 0.91), width=0.8)
        sh.commit()
        x = x0
        for k, (s, t, note) in enumerate(SET):
            w = s * k_in
            cx = x + w / 2
            ink.put(cx, top + bh + 13, t, 10, "B", INK, "center")
            ink.put(cx, top + bh + 23, mm_txt(s * 25.4), 7.5, "L", GREY, "center")
            if note and horn:
                ink.put(cx, top + bh + 33, note, 7.5, "LI", GREY, "center")
            x += w
    ink.put(34, y0 + 262, "Section lengths in inches, millimetres under them. The sectioned set is 35.75″ (908 mm) in all; "
            "the punch set has a horn at each end.", 7.5, "L", GREY)
    ink.put(34, 780, "Safety: it is the user’s responsibility to make sure that point-of-operation guarding meets all "
            "applicable safety standards.", 7.5, "LI", GREY)
    ink.flush()
    chrome(page, num, "AMERICAN STYLE TOOLING")
    return page


def punch_specs(it):
    return [("H", f"{inch(it['h'][0])}″ ({mm_txt(it['h'][1])} mm)"), ("R", f"{inch(it['r'][0])}″ ({mm_txt(it['r'][1])} mm)"),
            ("α", f"{it['a']}°")]


def die_specs(it):
    return [("V", f"{inch(it['v'][0])}″ ({mm_txt(it['v'][1])} mm)"), ("R", f"{inch(it['r'][0])}″ ({mm_txt(it['r'][1])} mm)"),
            ("α", f"{it['a']}°"), ("W", f"{it['w'][0]:.3f}″ ({mm_txt(it['w'][1])} mm)")]


def punch_page(doc, num, title, items, extra=None):
    page = doc.new_page(width=W, height=H)
    ink = P6.Ink(page)
    areas = []
    xs = [30.0, 210.0, 390.0]
    for x, it in zip(xs, items):
        r = place_drawing(page, PUN, it["clip"], fitz.Rect(x, 64, x + 172, 362), max_scale=1.12)
        areas.append(r)
        heading(ink, x + 6, 400, it)
        bot = spec_block(page, ink, x + 6, 428, punch_specs(it), width=158)
        pn_box(page, ink, x + 6, bot + 10, it, width=158)
    if extra:
        it = extra
        y = 600
        heading(ink, 36, y, it)
        ink.put(36, y + 30, "Drawing on request.", 8.5, "LI", INK)
        bot = spec_block(page, ink, 36, y + 44, punch_specs(it), width=158)
        pn_box(page, ink, 36, bot + 10, it, width=158)
    ink.put(34, 784, "Drawings in decimal inches, millimetres in blue. Tang .500″ (12.7 mm) with safety lip. "
            "H = height, R = tip radius, α = angle.", 6.8, "L", GREY)
    ink.flush()
    n, miss, reach = mm_values(page, areas)
    CROPS.update({it["code"]: (page.number, tuple(r)) for it, r in zip(items, reach)})
    chrome(page, num, title)
    return page, n, miss


def die_page(doc, num, title, items):
    page = doc.new_page(width=W, height=H)
    ink = P6.Ink(page)
    areas = []
    cells = [(30.0, 62.0), (300.0, 62.0), (30.0, 428.0), (300.0, 428.0)]
    for (x, y), it in zip(cells, items):
        r = place_drawing(page, DIE, it["clip"], fitz.Rect(x, y, x + 262, y + 212), max_scale=1.12)
        areas.append(r)
        heading(ink, x + 8, y + 238, it)
        bot = spec_block(page, ink, x + 8, y + 262, die_specs(it), width=128)
        pn_box(page, ink, x + 144, y + 262, it, width=118)
    ink.put(34, 784, "Drawings in decimal inches, millimetres in blue. All dies: tang .500″ (12.7 mm), working height "
            "1.937″ (49.2 mm), 2.563″ (65.1 mm) overall.", 6.6, "L", GREY)
    ink.put(34, 793, "V = V opening, R = shoulder radius, α = angle, W = body width.", 6.6, "L", GREY)
    ink.flush()
    n, miss, reach = mm_values(page, areas)
    CROPS.update({it["code"]: (page.number, tuple(r)) for it, r in zip(items, reach)})
    chrome(page, num, title)
    return page, n, miss


INT = os.path.join(SRC, "american_intermediate.pdf")          # EUROSTAMP's drawing 'INTERMEDIO AMERICAN STYLE' (mm)
INT_A = fitz.Rect(92, 64, 312, 350)                           # the intermediate on its own, and with a punch in it
INT_B = fitz.Rect(90, 360, 172, 470)                          # the punch tang it takes
INT_ROWS = [("Height", "3.937″ (100 mm)"), ("Upper tang", "1.181″ (30 mm)"), ("Body depth", "1.063″ (27 mm)"),
            ("Axis from tang face", ".276″ (7 mm)"), ("Punch tang slot", ".500″ (12.7 mm)"),
            ("Safety-lip pocket", ".650″ (16.5 mm)")]


def _int_source():
    """the sheet without its text (the dimensions are set again: decimal inches, the millimetres in blue), and the
    dimension texts with where they were"""
    doc = fitz.open(INT)
    p = doc[0]
    labels = []
    for b in p.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for s in ln["spans"]:
                t = s["text"].strip()
                if re.fullmatch(r"\d+(,\d+)?", t):
                    labels.append((t.replace(",", "."), fitz.Rect(s["bbox"]), tuple(ln["dir"]), s["size"]))
    p.add_redact_annot(p.rect, fill=False)
    p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                       text=fitz.PDF_REDACT_TEXT_REMOVE)
    return doc, labels


def intermediate_page(doc, num):
    """EUROSTAMP's Z1 intermediate that takes American-style punches: no part number yet, so 'on request'"""
    import textflow as TF
    page = doc.new_page(width=W, height=H)
    ink = P6.Ink(page)
    ink.put(36.0, 92.0, "Z1 intermediate", 20, "BI", BLUE)
    ink.put(36.0, 105.5, "for American-style punches · .500″ tang", 9, "M", BLUE)
    ink.flush()
    html = ("<p>This intermediate puts American-style punches on press brakes built for Z1 intermediates (Amada-Promecam "
            "European style). Its body is a standard Z1 — 3.937″ (100 mm) high under a 1.181″ (30 mm) upper tang, "
            "1.063″ (27 mm) deep, with the bending axis .276″ (7 mm) from the tang face — so it lines up with the "
            "machine’s other Z1 intermediates.</p>"
            "<p>The lower slot takes the punch’s .500″ (12.7 mm) tang, with a .650″ (16.5 mm) pocket for its safety "
            "lip, which holds the punch while the clamp is open. The clamp is drawn dashed: on the left the "
            "intermediate on its own, next to it with a punch in place.</p>")
    page.insert_htmlbox(fitz.Rect(36, 116, 561, 190), html, css=TF.CSS, archive=TF.ARCHIVE)
    src, labels = _int_source()
    uprights = [(it[1].x, min(it[1].y, it[2].y), max(it[1].y, it[2].y)) for dr in src[0].get_drawings()
                if (dr.get("width") or 1) < 0.42                  # thin: extension lines, not the centre lines
                for it in dr["items"] if it[0] == "l" and abs(it[1].x - it[2].x) < 0.05
                and abs(it[1].y - it[2].y) > 4]                    # (not the arrowheads' bases)
    s = 1.55
    areas, mm_of = [], {}
    for clip, (x0, y0) in ((INT_A, (36.0, 200.0)), (INT_B, (414.0, 412.0))):
        r = fitz.Rect(x0, y0, x0 + clip.width * s, y0 + clip.height * s)
        page.show_pdf_page(r, src, 0, clip=clip)
        areas.append(r)
        for t, bb, d, size in labels:
            if not clip.contains(bb):
                continue
            txt = inch(float(t) / 25.4)
            mm_of[txt] = t
            fs = 8.6
            w = PL.FONT["light"].text_length(txt, fs)
            if d[0] > 0.5:                                    # across: centred where the number was, on its line
                mid, yb = (bb.x0 + bb.x1) / 2, bb.y1 - 0.5           # the extension lines reach the dimension line
                xl = max([x for x, a, b in uprights if x < mid and a <= yb <= b] or [mid - 99])
                xr = min([x for x, a, b in uprights if x > mid and a <= yb <= b] or [mid + 99])
                room = (min(mid - xl, xr - mid) * 2) * s - 1.6  # between the extension lines either side
                if w > room:                                  # the 7 between the tang face and the axis
                    fs *= room / w
                    w = room
                cx = x0 + (mid - clip.x0) * s
                base = y0 + (bb.y1 - 0.21 * size - clip.y0) * s
                PL.put_text(page, fitz.Point(cx - w / 2, base), (1, 0), (0, -1), txt, fs, "light", (0, 0, 0))
            else:                                             # upright, reading bottom to top
                cy = y0 + ((bb.y0 + bb.y1) / 2 - clip.y0) * s
                base = x0 + (bb.x1 - 0.21 * size - clip.x0) * s
                PL.put_text(page, fitz.Point(base, cy + w / 2), (0, -1), (-1, 0), txt, fs, "light", (0, 0, 0))
    ink = P6.Ink(page)
    # the data, right of the drawing
    x0, y0, wd, rh = 398.0, 210.0, 163.0, 17.0
    sh = page.new_shape()
    sh.draw_rect(fitz.Rect(x0, y0, x0 + wd, y0 + 20))
    sh.finish(color=None, fill=GREEN, width=0)
    sh.draw_rect(fitz.Rect(x0, y0 + 20, x0 + wd, y0 + 20 + len(INT_ROWS) * rh + 8))
    sh.finish(color=None, fill=(0.94, 0.95, 0.95), width=0)
    sh.commit()
    ink.put(x0 + 8, y0 + 13.6, "DIMENSIONS", 9, "M", WHITE)
    for k, (a, b) in enumerate(INT_ROWS):
        yy = y0 + 20 + 15 + k * rh
        ink.put(x0 + 8, yy, a, 8.2, "L", INK)
        ink.put(x0 + wd - 8, yy, b, 8.6, "R", INK, "right")
    bot = y0 + 20 + len(INT_ROWS) * rh + 8
    ink.put(x0, bot + 16, "Part number, lengths and price on request.", 7.6, "LI", INK)
    ink.put(414.0, 400.0, "AMERICAN-STYLE PUNCH TANG", 8, "M", BLUE)
    ink.put(34, 784, "Drawing after EUROSTAMP’s, which is in millimetres: decimal inches, the millimetres in blue.",
            6.8, "L", GREY)
    ink.flush()
    n, miss, reach = mm_values(page, areas, mm_of, order=["above", "after", "before", "below", "below-far"])
    CROPS["intermediate"] = (page.number, tuple(reach[0]))
    CROPS["intermediate-tang"] = (page.number, tuple(reach[1]))
    chrome(page, num, "AMERICAN STYLE INTERMEDIATE")
    return page, n, miss


CROPS = {}                                                  # code → (page index, drawing with its labels)


def web_drawings(pdf=OUT, out_dir=None, dpi=300):
    """the drawings as they are in the catalogue — inches with the millimetres added — for the website's
    American-style pages (tools/src-images/eurostamp/es-am-<code>.png)"""
    out_dir = out_dir or os.path.join(ROOT, "tools", "src-images", "eurostamp")
    doc = fitz.open(pdf)
    paths = []
    for code, (pno, r) in CROPS.items():
        R = fitz.Rect(r) + (-6, -6, 6, 6)
        path = os.path.join(out_dir, f"es-am-{code.lower()}.png")
        doc[pno].get_pixmap(dpi=dpi, clip=R).save(path)
        paths.append(path)
    return paths


def build(out=OUT):
    doc = fitz.open()
    report = []
    opener(doc, FIRST)
    overview(doc, FIRST + 1)
    P = {it["code"]: it for it in PUNCHES}
    D = {it["code"]: it for it in DIES}
    for args in ((FIRST + 2, "AMERICAN STYLE PUNCHES - 88° / 85°", [P["S28932"], P["S28881"], P["S28880"]], P["S28974"]),
                 (FIRST + 3, "AMERICAN STYLE PUNCHES - 30° / 28°", [P["S29083"], P["S29252"], P["S29084"]], None)):
        _, n, miss = punch_page(doc, *args)
        report.append((args[0], n, miss))
    for args in ((FIRST + 4, "AMERICAN STYLE DIES - 88°", [D["S28946"], D["S29269"], D["S29145"], D["S28947"]]),
                 (FIRST + 5, "AMERICAN STYLE DIES - 30° / 34°", [D["S29142"], D["S29141"], D["S29143"], D["S29144"]])):
        _, n, miss = die_page(doc, *args)
        report.append((args[0], n, miss))
    _, n, miss = intermediate_page(doc, FIRST + 6)
    report.append((FIRST + 6, n, miss))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc.save(out, garbage=3, deflate=True)
    return out, report


if __name__ == "__main__":
    o, rep = build()
    print(o)
    for r in rep:
        print(r)
    if "--web" in sys.argv:
        for p in web_drawings(o):
            print(p)
