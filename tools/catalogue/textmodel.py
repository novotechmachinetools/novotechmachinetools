"""The text of a catalogue page as runs of glyphs with their full placement: baseline direction, the slant of the
upright strokes (isometric labels are sheared, not rotated), size, font, colour and the outline each one covers.

PyMuPDF gives the characters, their origins and the baseline direction; pdfplumber gives the text matrix of each
character, whose second column is the direction of the glyphs' upright strokes.  Page coordinates throughout (y down).
"""
import math
import os
import re

import fitz
from shapely.geometry import Polygon

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTDIR = os.path.join(ROOT, "tools", "fonts")
TTF = {"reg": os.path.join(FONTDIR, "Roboto-Regular.ttf"), "light": os.path.join(FONTDIR, "Roboto-Light.ttf"),
       "med": os.path.join(FONTDIR, "Roboto-Medium.ttf"), "bold": os.path.join(FONTDIR, "Roboto-Bold.ttf")}
FONT = {k: fitz.Font(fontfile=v) for k, v in TTF.items()}
ITALIC_SLANT = 0.21                                    # Roboto Italic leans about 12°


def weight_of(fontname):
    f = fontname or ""
    if "Black" in f or "Bold" in f:
        return "bold"
    if "Medium" in f:
        return "med"
    if "Light" in f or "Thin" in f:
        return "light"
    return "reg"


class Run:
    """a run of characters on one baseline with no wide gap: a word, a number, 'R 0,5', 'Max T/m'"""

    def __init__(self, chars, line_dir, size, font, color, matrix=None):
        self.chars = chars                              # [(c, origin Point, bbox Rect, font, size)]
        self.text = "".join(c[0] for c in chars)
        self.t = self.text.strip()
        ux, uy = line_dir
        n = math.hypot(ux, uy) or 1.0
        self.u = (ux / n, uy / n)
        if matrix is not None:
            a, b, c, d = matrix[:4]
            s = math.hypot(a, b) or 1.0
            self.v = (c / s, -d / s)                   # the glyphs' 'up' in page coordinates
        else:
            self.v = (self.u[1], -self.u[0])           # unsheared: perpendicular, pointing up
        self.size = size
        self.font = font
        self.weight = weight_of(font)
        self.italic = "Italic" in (font or "") or "Oblique" in (font or "")
        self.color = color
        first = next((c for c in chars if c[0].strip()), chars[0])
        self.origin = fitz.Point(first[1])
        last = [c for c in chars if c[0].strip()][-1] if self.t else chars[-1]
        self.adv = self.along(last[1]) + FONT[self.weight].text_length(last[0], last[4])
        self.bbox = fitz.Rect(chars[0][2])
        for c in chars:
            self.bbox |= c[2]

    # frame helpers ------------------------------------------------------------------------------------------------
    def along(self, p):
        return (p[0] - self.origin.x) * self.u[0] + (p[1] - self.origin.y) * self.u[1]

    def point(self, x, y, size=None):
        """page point at x along the baseline and y (in sizes) up the glyphs"""
        s = self.size if size is None else size
        return fitz.Point(self.origin.x + x * self.u[0] + y * s * self.v[0], self.origin.y + x * self.u[1] + y * s * self.v[1])

    @property
    def upright(self):
        return abs(self.u[1]) < 0.01 and self.u[0] > 0 and abs(self.v[0]) < 0.01

    @property
    def vertical(self):
        return abs(self.u[0]) < 0.01 and self.u[1] < 0 and abs(self.v[1]) < 0.01

    def outline(self, lo=None, hi=None):
        """the polygon the glyphs cover: baseline (or descender) to cap height, origin to advance"""
        if lo is None:
            lo = -0.2 if re.search(r"[,;()gjpqy]", self.t) else -0.03
        if hi is None:
            hi = 0.74 if re.search(r"[A-Z0-9(]", self.t) or not self.t.islower() else 0.55
        pts = [self.point(0, lo), self.point(self.adv, lo), self.point(self.adv, hi), self.point(0, hi)]
        return Polygon([(p.x, p.y) for p in pts])

    def __repr__(self):
        return f"Run({self.t!r} @{self.origin.x:.1f},{self.origin.y:.1f} u={self.u[0]:.2f},{self.u[1]:.2f} v={self.v[0]:.2f},{self.v[1]:.2f} s={self.size:.1f})"


def _plumber_index(ppage):
    idx = {}
    if ppage is None:
        return idx
    for ch in ppage.chars:
        if ch["text"].strip():
            idx.setdefault(ch["text"], []).append(ch)
    return idx


def _matrix_for(idx, c, bbox):
    best, bd = None, 3.0
    for ch in idx.get(c, []):
        d = abs(ch["x0"] - bbox.x0) + abs(ch["top"] - bbox.y0)
        if d < bd:
            best, bd = ch, d
    return best["matrix"] if best is not None else None


def runs(page, ppage=None, gap=0.55):
    """every run of text on the page.  `ppage`: the same page opened with pdfplumber (for the slant of the glyphs)."""
    idx = _plumber_index(ppage)
    result = []
    raw = page.get_text("rawdict", flags=fitz.TEXT_PRESERVE_WHITESPACE | fitz.TEXT_PRESERVE_LIGATURES)
    for b in raw["blocks"]:
        for l in b.get("lines", []):
            u = tuple(l["dir"])
            groups, cur, end = [], [], None
            for s in l["spans"]:
                for ch in s["chars"]:
                    c = ch["c"]
                    org, box = fitz.Point(ch["origin"]), fitz.Rect(ch["bbox"])
                    if cur and c.strip():
                        o = cur[0][1]
                        along = (org.x - o.x) * u[0] + (org.y - o.y) * u[1]
                        if end is not None and along - end > gap * s["size"]:
                            groups.append(cur)
                            cur, end = [], None
                    if not cur and not c.strip():
                        continue
                    cur.append((c, org, box, s["font"], s["size"], s["color"]))
                    if c.strip():
                        o = cur[0][1]
                        end = (org.x - o.x) * u[0] + (org.y - o.y) * u[1] + FONT[weight_of(s["font"])].text_length(c, s["size"])
            if cur:
                groups.append(cur)
            for grp in groups:
                while grp and not grp[-1][0].strip():
                    grp = grp[:-1]
                if not grp:
                    continue
                first = next(g for g in grp if g[0].strip())
                main = max((g for g in grp if g[0].strip()), key=lambda g: g[4])
                m = _matrix_for(idx, first[0], first[2])
                result.append(Run([g[:5] for g in grp], u, main[4], main[3], main[5], m))
    return result
