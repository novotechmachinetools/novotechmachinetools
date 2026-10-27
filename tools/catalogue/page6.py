"""Catalogue page 6, the air-bending page, in two versions:

  * imperial (a new page that goes in front of page 6): every value in inches, the force in US tons per foot, the
    tensile strengths in ksi, the formula for inches — drawn on a copy of EUROSTAMP's page so it looks the same;
  * metric (EUROSTAMP's page 6 itself): the tables untouched, the Italian taken out and the English set again as one
    clean line per row.

EUROSTAMP's stainless table prints 208 t/m for V 50 / 8 mm; the formula and the cells around it give 128 (208 is the
value of V 200 / 20 mm), so both versions show 128.

    python3 tools/catalogue/page6.py        → tools/cache/edition/imperial6.pdf (the imperial page)
"""
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bending_chart as BC                         # noqa: E402
from fonts import font                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
CAT = "/home/claude/eurostamp/pdf/cat.pdf"
OUT = os.path.join(ROOT, "tools", "cache", "edition", "imperial6.pdf")
FD = os.path.join(ROOT, "tools", "fonts", "roboto")
F = {k: os.path.join(FD, f"{v}.ttf") for k, v in dict(T="Roboto-Thin", L="Roboto-Light", R="Roboto-Regular",
                                                       M="Roboto-Medium", B="Roboto-Bold", SR="RobotoSlab-Regular",
                                                       SL="RobotoSlab-Light", SB="RobotoSlab-Bold").items()}
INK = (0.137, 0.122, 0.125)
DARK = (0.157, 0.173, 0.180)
BLACK = (0, 0, 0)
WHITE = (1, 1, 1)
BLUE = (0.0, 0.336, 0.534)
TITLE_BLUE = (0.0, 0.337, 0.533)
LABEL = (0.833, 0.838, 0.844)
CELL = (0.904, 0.906, 0.901)
GRID = (0.833, 0.838, 0.844)
NOTE = (0.35, 0.35, 0.36)
US = 0.3048 * 1.10231                              # t/m → US tons per foot
KSI = 1.42233                                      # kg/mm² → ksi
TYPO = {("stainless", 50.0, 8.0): (208, 128)}


def inch(mm):
    v = mm / 25.4
    s = f"{v:.2f}" if v >= 1 else f"{v:.3f}"
    return s[1:] if s.startswith("0.") else s


def tons(tm):
    v = tm * US
    return f"{v:.1f}" if v < 9.95 else f"{v:.0f}"


class Ink:
    """text collected per colour and written with one TextWriter each"""

    def __init__(self, page):
        self.page, self.by = page, {}

    def put(self, x, y, t, size, key="L", color=INK, align="left"):
        fo = font(F[key])
        w = fo.text_length(t, size)
        if align == "center":
            x -= w / 2
        elif align == "right":
            x -= w
        tw = self.by.get(color)
        if tw is None:
            tw = self.by[color] = fitz.TextWriter(self.page.rect)
        tw.append(fitz.Point(x, y), t, font=fo, fontsize=size)
        return w

    def width(self, t, size, key="L"):
        return font(F[key]).text_length(t, size)

    def flush(self):
        for col, tw in self.by.items():
            tw.write_text(self.page, color=col)
        self.by = {}


def redact(page, rects, graphics=False):
    for r in rects:
        page.add_redact_annot(fitz.Rect(r), fill=False)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                          graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED if graphics else fitz.PDF_REDACT_LINE_ART_NONE,
                          text=fitz.PDF_REDACT_TEXT_REMOVE)


# the text that is set again on both versions: the two title bars, the legend, the ratio table, the table titles
TEXT_RECTS = [(30, 31, 340, 62), (30, 288, 432, 318), (206, 90, 348, 194), (390, 90, 532, 194), (78, 349, 180, 401),
              (184, 348, 337, 397), (30, 429, 282, 452), (288, 429, 530, 452)]
FORMULA_RECTS = [(220, 210, 300, 258), (303, 220, 392, 242)]
ROWS = (102.8, 129.8, 156.8, 183.8)                # the legend rows' centre lines (cells 87.5 – 196.6, 27 pt each)


def bar_title(ink, page, y, text, bar):
    """a title in a blue bar, the bar lengthened when the title needs it"""
    x0 = 34.0
    w = ink.width(text, 13, "SL")
    if x0 + w + 22 > bar.x1:
        sh = page.new_shape()
        sh.draw_rect(fitz.Rect(bar.x1 - 1, bar.y0, x0 + w + 24, bar.y1))
        sh.finish(color=None, fill=BLUE, width=0)
        sh.commit()
    ink.put(x0, y, text, 13, "SL", WHITE)


def set_text(page, units):
    """the English text of either version (units 'mm' or 'in')"""
    redact(page, TEXT_RECTS + (FORMULA_RECTS if units == "in" else []))
    ink = Ink(page)
    if units == "in":
        bar_title(ink, page, 51.4, "AIR BENDING FORCE CALCULATION – INCH", fitz.Rect(0, 29.1, 346.8, 64.6))
        bar_title(ink, page, 308.0, "SHEET THICKNESS / V OPENING RATIO – INCH", fitz.Rect(0, 285.8, 439.4, 321.3))
        left = ("Sheet thickness (in)", "V opening (in)", "Force (US tons per foot)", "Shortest flange (in)")
        right = ("Inside radius (in)", f"Aluminum: {20 * KSI:.0f} – {25 * KSI:.0f} ksi",
                 f"Mild steel: {40 * KSI:.0f} – {45 * KSI:.0f} ksi", f"Stainless steel: {65 * KSI:.0f} – {70 * KSI:.0f} ksi")
    else:
        bar_title(ink, page, 51.4, "AIR BENDING FORCE CALCULATION – METRIC", fitz.Rect(0, 29.1, 346.8, 64.6))
        bar_title(ink, page, 308.0, "SHEET THICKNESS / V OPENING RATIO – METRIC", fitz.Rect(0, 285.8, 439.4, 321.3))
        left = ("Sheet thickness (mm)", "V opening (mm)", "Force (metric tons per meter)", "Shortest flange (mm)")
        right = ("Inside radius (mm)", "Aluminum: 20 – 25 kg/mm²", "Mild steel: 40 – 45 kg/mm²",
                 "Stainless steel: 65 – 70 kg/mm²")
    for y, a, b in zip(ROWS, left, right):
        ink.put(208.1, y + 2.9, a, 8.2, "L")
        ink.put(392.0, y + 2.9, b, 8.2, "L")
    if units == "in":
        # F = S² × 12 × R / (1.4 × V) in US tons per foot, S and V in inches, R in ksi
        parts = [("S", 15.98, 0), ("2", 9.13, 9.2), (" × ", 10.27, 3.5), ("12", 15.98, 0), (" × ", 10.27, 3.5),
                 ("R", 15.98, 0)]
        w = sum(ink.width(t, s) for t, s, _ in parts)
        x = 255.6 - w / 2
        for t, s, rise in parts:
            x += ink.put(x, 229.4 - rise, t, s, "L", BLACK)
        parts = [("1.4", 15.98, 0), (" × ", 10.27, 3.5), ("V", 15.98, 0)]
        w = sum(ink.width(t, s) for t, s, _ in parts)
        x = 255.6 - w / 2
        for t, s, rise in parts:
            x += ink.put(x, 251.6 - rise, t, s, "L", BLACK)
        x = 305.4 + ink.put(305.4, 235.3, "= ", 10.27, "L", BLACK)
        x += ink.put(x, 234.2, ".......", 11.41, "L", BLACK)
        ink.put(x + 3, 235.3, "US tons/ft", 13.5, "L", BLACK)
        ink.put(305.4, 249.5, "S and V in inches, R in ksi", 6.8, "L", NOTE)
    # thickness / V opening ratio
    ink.put(80.0, 365.0, "Sheet thickness (in)" if units == "in" else "Sheet thickness (mm)", 7.7, "L", INK)
    ink.put(80.0, 395.0, "V opening", 7.7, "L", INK)
    if units == "in":
        top = ((196.0, ".020 – .098"), (236.0, ".118 – .315"), (276.0, ".354 – .394"),
               (316.0, ".472 and up"))
        sz = 7.0
    else:
        top = ((200.9, "0.5 – 2.5"), (236.6, "3 – 8"), (269.4, "9 – 10"), (311.8, "12 and up"))
        sz = 9.0
    for x, t in top:
        ink.put(x, 365.6, t, sz, "L", INK, "center")
    xs = [x for x, _ in top]
    for x, t in zip(xs, ("6 S", "8 S", "10 S", "12 S")):
        ink.put(x, 395.6, t, 9.0, "L", INK, "center")
    # table titles
    ink.put(34.3, 449.0, "AIR BENDING TABLE – MILD STEEL", 10, "M", TITLE_BLUE)
    ink.put(291.5 if units == "mm" else 300.0, 449.0, "AIR BENDING TABLE – STAINLESS STEEL", 10, "M", TITLE_BLUE)
    ink.flush()


def fix_typo(page):
    """EUROSTAMP's 208 in the stainless table (V 50, 8 mm) → 128"""
    row = next(r for r in BC.charts()["stainless"]["rows"] if r["V"] == 50.0)
    for w in page.get_text("words"):
        cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
        if w[4] == "208" and 285 < cx < 530 and abs(cy - row["y"]) < 4:
            r = fitz.Rect(w[:4])
            raw = page.get_text("rawdict", clip=r + (-0.5, -0.5, 0.5, 0.5))
            for b in raw["blocks"]:
                for ln in b.get("lines", []):
                    for sp in ln["spans"]:
                        for ch in sp["chars"]:
                            q = fitz.Rect(ch["bbox"])
                            if ch["c"].strip() and r.contains(fitz.Point((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2)):
                                m = fitz.Point((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2)
                                page.add_redact_annot(fitz.Rect(m.x - 0.5, m.y - 0.5, m.x + 0.5, m.y + 0.5), fill=False)
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                                  text=fitz.PDF_REDACT_TEXT_REMOVE)
            ink = Ink(page)
            ink.put(cx, r.y1 - 1.25, "128", 5.59, "L", INK, "center")
            ink.flush()
            return True
    return False


def metric_handler(page, ppage, ctx):
    set_text(page, "mm")
    fix_typo(page)


# ------------------------------------------------------------------------------------------------- imperial tables
def table(page, ink, x0, chart, name):
    """one air-bending table in inches: the label columns V, B, Ri; a column per thickness; F in US tons per foot.
    The same rows (13.93 pt) and grid colours as EUROSTAMP's."""
    y0, rh = 472.5, 13.93
    lw, uw, cw = 20.0, 8.0, 9.5
    cols = chart["S"]
    rows = chart["rows"]
    x_s = x0 + 3 * lw + uw
    x_end = x_s + len(cols) * cw
    yf = y0 + (len(rows) + 1) * rh
    shade = {tuple(k): v for k, v in chart["shade"]}
    sh = page.new_shape()
    sh.draw_rect(fitz.Rect(x0 - 4, y0 - 10, x_end + 6, yf + rh + 12))
    sh.finish(color=None, fill=WHITE, width=0)
    sh.commit()
    sh = page.new_shape()
    sh.draw_rect(fitz.Rect(x0, y0, x0 + 3 * lw, y0 + rh))                      # the S box
    sh.finish(color=None, fill=BLUE, width=0)
    for i in range(len(rows) + 1):                                             # V, B, Ri cells and the footer
        y = y0 + (i + 1) * rh
        for j in range(3):
            sh.draw_rect(fitz.Rect(x0 + j * lw, y, x0 + (j + 1) * lw, y + rh))
    sh.finish(color=WHITE, fill=LABEL, width=0.47)
    sh.commit()
    sh = page.new_shape()
    for i, r in enumerate(rows):
        y = y0 + (i + 1) * rh
        for k, s in enumerate(cols):
            st = shade.get((r["V"], s))
            if st and s in r["F"]:
                sh.draw_rect(fitz.Rect(x_s + k * cw, y, x_s + (k + 1) * cw, y + rh))
                sh.finish(color=None, fill=BLUE if st == "rec" else CELL, width=0)
    fx = x_end - 2 * cw
    sh.draw_rect(fitz.Rect(fx, yf, x_end, yf + rh))
    sh.finish(color=None, fill=BLUE, width=0)
    sh.commit()
    # grid: rows across the thickness columns, one line per column
    sh = page.new_shape()
    for i in range(len(rows) + 2):
        y = y0 + i * rh
        sh.draw_line(fitz.Point(x0 + 3 * lw, y), fitz.Point(x_end, y))
    for k in range(len(cols) + 1):
        x = x_s + k * cw
        sh.draw_line(fitz.Point(x, y0), fitz.Point(x, yf if k >= len(cols) - 1 else yf + rh))
    sh.draw_line(fitz.Point(x0 + 3 * lw, y0), fitz.Point(x0 + 3 * lw, yf + rh))
    sh.draw_line(fitz.Point(x0 + 3 * lw, yf + rh), fitz.Point(fx, yf + rh))
    sh.finish(color=GRID, width=0.47, closePath=False)
    sh.commit()
    # text
    ink.put(x0 + 1.5 * lw, y0 + 11.0, "S", 11.18, "SB", WHITE, "center")
    ink.put(x0 + 3 * lw + uw / 2, y0 + 8.6, "in", 4.4, "L", INK, "center")
    for k, s in enumerate(cols):
        ink.put(x_s + (k + 0.5) * cw, y0 + 8.6, inch(s), 4.25, "R", INK, "center")
    for i, r in enumerate(rows):
        y = y0 + (i + 1) * rh
        for j, v in enumerate((r["V"], r["B"], r["Ri"])):
            ink.put(x0 + (j + 0.5) * lw, y + 8.9, inch(v), 5.3, "L", INK, "center")
        for k, s in enumerate(cols):
            if s not in r["F"]:
                continue
            f = r["F"][s]
            fixed = TYPO.get((name, r["V"], s))
            if fixed and f == fixed[0]:
                f = fixed[1]
            dark = shade.get((r["V"], s)) == "rec"
            ink.put(x_s + (k + 0.5) * cw, y + 8.9, tons(f), 5.3, "L", WHITE if dark else INK, "center")
    for j, t in enumerate(("V", "B", "Ri")):
        ink.put(x0 + (j + 0.5) * lw, yf + 8.9, t, 5.59, "L", INK, "center")
    ink.put(fx + cw, yf + 11.4, "F", 11.18, "SB", WHITE, "center")
    ink.put(x_end, yf + rh + 6.4, "US tons/ft", 4.97, "L", DARK, "right")
    return x_end


def build(out=OUT):
    from logo import place_logo
    src = fitz.open(CAT)
    doc = fitz.open()
    doc.insert_pdf(src, from_page=5, to_page=5)
    page = doc[0]
    set_text(page, "in")
    redact(page, [(22, 458, 572, 778)], graphics=True)          # the two metric tables
    charts = BC.charts()
    ink = Ink(page)
    table(page, ink, 34.0, charts["mild"], "mild")
    table(page, ink, 300.0, charts["stainless"], "stainless")
    ink.put(34.0, 789.0, "S, V, B and Ri in inches; F in US tons per foot of bend length.  Converted from EUROSTAMP’s "
            "metric chart on the next page (1 mm = .03937 in, 1 metric t/m = 0.336 US t/ft).", 6.2, "L", NOTE)
    ink.flush()
    place_logo(page)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc.save(out, garbage=3, deflate=True)
    return out


if __name__ == "__main__":
    print(build())
