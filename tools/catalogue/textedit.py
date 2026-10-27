"""Editing the text of a catalogue page glyph by glyph: lines with every character's origin, font, size and colour; taking
characters out (redaction of the glyphs only, graphics and images untouched); setting characters again — moved along or
across their line, or new text — in the same Roboto / Roboto Slab files the catalogue uses, in the line's own direction
and slant.

Coordinates are page coordinates (y down).  A line has a baseline direction u and an 'up' direction v (the direction of
the upright strokes: perpendicular to u unless the label is sheared, as on the isometric drawings).
"""
import math
import re

import fitz

import fonts as F

SEP_RE = re.compile(r"\s+/\s*|\s*/\s+")                 # 'IT / EN': a slash with a space on at least one side


class Ch:
    __slots__ = ("c", "o", "bbox", "font", "size", "color", "line")

    def __init__(self, c, o, bbox, font, size, color):
        self.c, self.o, self.bbox, self.font, self.size, self.color = c, o, bbox, font, size, color
        self.line = None

    @property
    def path(self):
        return F.ttf(self.font)

    def adv(self):
        return F.font(self.path).text_length(F.char_for(self.c, self.font), self.size)

    def __repr__(self):
        return f"{self.c!r}@{self.o.x:.1f},{self.o.y:.1f}"


class Line:
    def __init__(self, chars, u, v, block, idx):
        self.chars = chars
        for c in chars:
            c.line = self
        self.u, self.v = u, v
        self.block, self.idx = block, idx
        self.text = "".join(c.c for c in chars)
        self.t = self.text.strip()
        ink = [c for c in chars if c.c.strip()] or chars
        self.ink = ink
        self.size = max(c.size for c in ink)
        self.O = fitz.Point(ink[0].o)
        self.bbox = fitz.Rect(ink[0].bbox)
        for c in ink:
            self.bbox |= c.bbox
        self.removed = False

    # frame ---------------------------------------------------------------------------------------------------------
    def along(self, p):
        return (p.x - self.O.x) * self.u[0] + (p.y - self.O.y) * self.u[1]

    def coords(self, p):
        """(x along the baseline, y up the glyphs) of page point p in the line's frame (O + x·u + y·v = p)"""
        dx, dy = p.x - self.O.x, p.y - self.O.y
        n = (-self.u[1], self.u[0])
        vn = self.v[0] * n[0] + self.v[1] * n[1]
        y = (dx * n[0] + dy * n[1]) / vn if abs(vn) > 1e-6 else 0.0
        x = dx * self.u[0] + dy * self.u[1] - y * (self.v[0] * self.u[0] + self.v[1] * self.u[1])
        return x, y

    def up(self, p):
        return self.coords(p)[1]

    def point(self, x, y=0.0):
        """page point at x along the baseline and y (pt) up the glyphs"""
        return fitz.Point(self.O.x + x * self.u[0] + y * self.v[0], self.O.y + x * self.u[1] + y * self.v[1])

    @property
    def start(self):
        return 0.0

    @property
    def end(self):
        last = self.ink[-1]
        return self.along(last.o) + last.adv()

    @property
    def upright(self):
        return abs(self.u[1]) < 0.01 and self.u[0] > 0 and abs(self.v[0]) < 0.02

    @property
    def main_font(self):
        from collections import Counter
        return Counter(c.font for c in self.ink).most_common(1)[0][0]

    @property
    def color(self):
        from collections import Counter
        return Counter(c.color for c in self.ink).most_common(1)[0][0]

    def parts(self):
        """[(chars, text)] split at ' / ' separators (the separators dropped)"""
        out, last = [], 0
        for m in SEP_RE.finditer(self.text):
            seg = self.chars[last:m.start()]
            out.append(seg)
            last = m.end()
        out.append(self.chars[last:])
        res = []
        for seg in out:
            while seg and not seg[0].c.strip():
                seg = seg[1:]
            while seg and not seg[-1].c.strip():
                seg = seg[:-1]
            res.append((seg, "".join(c.c for c in seg)))
        return res

    def __repr__(self):
        return f"Line({self.t!r} @{self.O.x:.1f},{self.O.y:.1f} s={self.size:.1f})"


# ------------------------------------------------------------------------------------------------------------- reading
def _plumber_index(ppage):
    idx = {}
    if ppage is None:
        return idx
    for ch in ppage.chars:
        if ch["text"].strip():
            idx.setdefault(ch["text"], []).append(ch)
    return idx


def _up_vector(idx, c, bbox, u):
    best, bd = None, 3.0
    for ch in idx.get(c, []):
        d = abs(ch["x0"] - bbox.x0) + abs(ch["top"] - bbox.y0)
        if d < bd:
            best, bd = ch, d
    if best is not None:
        a, b, cc, dd = best["matrix"][:4]
        s = math.hypot(a, b) or 1.0
        v = (cc / s, -dd / s)
        n = math.hypot(*v) or 1.0
        if n > 0.5:
            return (v[0] / n * min(n, 1.2), v[1] / n * min(n, 1.2)) if n > 1.2 else v
    return (u[1], -u[0])


def page_lines(page, ppage=None):
    idx = _plumber_index(ppage)
    out = []
    raw = page.get_text("rawdict", flags=fitz.TEXT_PRESERVE_WHITESPACE | fitz.TEXT_PRESERVE_LIGATURES)
    k = 0
    for b in raw["blocks"]:
        for l in b.get("lines", []):
            chars = []
            for s in l["spans"]:
                for ch in s["chars"]:
                    chars.append(Ch(ch["c"], fitz.Point(ch["origin"]), fitz.Rect(ch["bbox"]), s["font"], s["size"], s["color"]))
            if not "".join(c.c for c in chars).strip():
                continue
            u = tuple(l["dir"])
            n = math.hypot(*u) or 1.0
            u = (u[0] / n, u[1] / n)
            first = next(c for c in chars if c.c.strip())
            v = _up_vector(idx, first.c, first.bbox, u) if idx else (u[1], -u[0])
            out.append(Line(chars, u, v, b["number"], k))
            k += 1
    return out


# ------------------------------------------------------------------------------------------------------------- editing
def frame_matrix(u, v):
    """morph matrix (PyMuPDF's convention: applied with y up) laying text along u with its upright strokes along v"""
    return fitz.Matrix(u[0], -u[1], v[0], -v[1], 0, 0)


def _is_identity_frame(u, v):
    return abs(u[0] - 1) < 1e-3 and abs(u[1]) < 1e-3 and abs(v[0]) < 1e-3 and abs(v[1] + 1) < 1e-3


class Editor:
    """collects removals and additions for one page, then applies them in one redaction pass"""

    def __init__(self, page, lines):
        self.page = page
        self.lines = lines
        self.gone = []                                   # Ch to remove
        self.adds = []                                   # (u, v, pivot, [(local x, local y, text, fontpath, size)], color)
        self.log = []

    # removal -------------------------------------------------------------------------------------------------------
    def drop(self, chars):
        for c in chars:
            if c.c.strip():
                self.gone.append(c)

    def drop_line(self, line):
        line.removed = True
        self.drop(line.chars)

    # additions -----------------------------------------------------------------------------------------------------
    def put_chars(self, line, chars, dx=0.0, dy=0.0, font=None, size=None, color=None):
        """set `chars` of `line` again, moved dx along the baseline and dy (pt) up the glyphs; the originals are dropped"""
        self.drop(chars)
        items = []
        for c in chars:
            if not c.c.strip():
                continue
            x, y = line.coords(c.o)
            x += dx
            y += dy
            path = F.ttf(font or c.font)
            items.append((x, y, F.char_for(c.c, c.font), path, size or c.size, color if color is not None else c.color))
        self._add(line, items)

    def put_text(self, line, x, txt, font, size, color=None, dy=0.0, tracking=0.0):
        """new text on `line`'s baseline frame starting x along it (dy up); tracking: extra pt between characters"""
        path = F.ttf(font) if not font.endswith(".ttf") else font
        fo = F.font(path)
        items, cx = [], x
        for ch in txt:
            if ch.strip():
                items.append((cx, dy, ch, path, size, color if color is not None else line.color))
            cx += fo.text_length(ch, size) + tracking
        self._add(line, items)
        return cx - tracking

    def _add(self, line, items):
        by_col = {}
        for it in items:
            by_col.setdefault(it[5], []).append(it[:5])
        for col, its in by_col.items():
            self.adds.append((line.u, line.v, fitz.Point(line.O), its, col))

    # apply ---------------------------------------------------------------------------------------------------------
    def apply(self):
        page = self.page
        if self.gone:
            for c in self.gone:
                ln = c.line
                w = c.adv() or (c.bbox.width or c.size * 0.5)
                x0, y0 = ln.coords(c.o)
                ctr = ln.point(x0 + w / 2, y0 + 0.32 * c.size)
                r = max(0.25, min(w, c.size) * 0.16)
                page.add_redact_annot(fitz.Rect(ctr.x - r, ctr.y - r, ctr.x + r, ctr.y + r), fill=False)
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                                  text=fitz.PDF_REDACT_TEXT_REMOVE)
        for u, v, piv, items, col in self.adds:
            tw = fitz.TextWriter(page.rect)
            ident = _is_identity_frame(u, v)
            for x, y, ch, path, size in items:
                # laid out upright round the pivot (y down), then morphed into the line's frame
                tw.append(fitz.Point(piv.x + x, piv.y - y), ch, font=F.font(path), fontsize=size)
            color = fitz.sRGB_to_pdf(col) if isinstance(col, int) else col
            if ident:
                tw.write_text(page, color=color)
            else:
                tw.write_text(page, color=color, morph=(piv, frame_matrix(u, v)))
        self.gone, self.adds = [], []
