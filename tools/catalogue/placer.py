"""Where an inch value can go on a catalogue page, and writing it there.

The page is rendered to masks at S px per pt:
  ink    anything printed
  dark   dark ink only (a light grey tool body or shading is not dark)
  hard   what must never be covered: text, fills, shading — everything but the thin blue / black dimension, extension and
         leader lines
An inch value is tried at a few spots round its number (after it, stacked above or below it, before it, a little further
along), in the number's own direction and slant, at a few sizes, first on clean paper, then over light shading, and last
across a thin line with a white patch under it.  It is accepted only where it reads as that number's: nearer to it than
to any other number.
"""
import math

import fitz
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from shapely.geometry import Point as SPoint, Polygon, LineString

from textmodel import FONT, TTF, ITALIC_SLANT

S = 4                                                   # mask resolution, px per pt
PAD = 0.45                                              # pt of paper kept round an addition


def inch(mm, places=None):
    """decimal inches, leading zero dropped: 2 places from 1″ up and 3 below unless `places` is given — '4.13″', '.315″'"""
    v = mm / 25.4
    p = places if places is not None else (2 if v >= 1 else 3)
    s = f"{v:.{p}f}"
    return (s[1:] if s.startswith("0.") else s) + "″"


def lb_text(kg):
    v = kg * 2.20462
    return f"{v:.1f} lb" if v < 100 else f"{v:,.0f} lb"


def _render(page, clip=None):
    pix = page.get_pixmap(matrix=fitz.Matrix(S, S), colorspace=fitz.csGRAY, alpha=False)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width)


def _is_grey(col):
    if not col:
        return False
    r, g, b = col[:3]
    return abs(r - g) < 0.07 and abs(g - b) < 0.07 and 0.3 < r < 0.9


def _bezier(p0, p1, p2, p3, n=12):
    out = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        out.append((mt ** 3 * p0.x + 3 * mt * mt * t * p1.x + 3 * mt * t * t * p2.x + t ** 3 * p3.x,
                    mt ** 3 * p0.y + 3 * mt * mt * t * p1.y + 3 * mt * t * t * p2.y + t ** 3 * p3.y))
    return out


class Canvas:
    def __init__(self, page, runs):
        self.page = page
        g = _render(page)
        self.h, self.w = g.shape
        self.ink = g < 238
        self.dark = g < 165
        # the page without its text: what the graphics alone cover
        tmp = fitz.open()
        tmp.insert_pdf(page.parent, from_page=page.number, to_page=page.number)
        tp = tmp[0]
        tp.add_redact_annot(tp.rect, fill=False)
        tp.apply_redactions(images=0, graphics=0, text=0)
        gink = _render(tp) < 238
        # thin stroked lines in blue or black (dimension, extension and leader lines; not the grey scale grids)
        im = Image.new("L", (self.w, self.h), 0)
        dr = ImageDraw.Draw(im)
        for d in page.get_drawings():
            if "s" not in (d.get("type") or "") or d.get("fill") is not None:
                continue
            wid = d.get("width") or 0.5
            col = d.get("color")
            if wid > 1.05 or col is None or _is_grey(col):
                continue
            lw = max(2, int(round(wid * S)) + 2)
            for it in d["items"]:
                if it[0] == "l":
                    dr.line([(it[1].x * S, it[1].y * S), (it[2].x * S, it[2].y * S)], fill=255, width=lw)
                elif it[0] == "c":
                    dr.line([(x * S, y * S) for x, y in _bezier(*it[1:5])], fill=255, width=lw)
                elif it[0] == "re":
                    R = it[1]
                    dr.rectangle([R.x0 * S, R.y0 * S, R.x1 * S, R.y1 * S], outline=255, width=lw)
                elif it[0] == "qu":
                    q = it[1]
                    dr.line([(p.x * S, p.y * S) for p in (q.ul, q.ur, q.lr, q.ll, q.ul)], fill=255, width=lw)
        thin = np.asarray(im) > 0
        soft = gink & thin
        text = self._polys_mask([r.outline() for r in runs], grow=0.25)
        self.text = text
        self.hard = (gink & ~soft) | text
        self.knock = []                                 # white patches to draw under additions

    # masks ---------------------------------------------------------------------------------------------------------
    def _poly_local(self, poly, grow):
        p = poly.buffer(grow, join_style=2) if grow else poly
        x0, y0, x1, y1 = p.bounds
        X0, Y0 = int(math.floor(x0 * S)) - 1, int(math.floor(y0 * S)) - 1
        X1, Y1 = int(math.ceil(x1 * S)) + 1, int(math.ceil(y1 * S)) + 1
        im = Image.new("L", (max(1, X1 - X0), max(1, Y1 - Y0)), 0)
        geoms = getattr(p, "geoms", [p])
        for gm in geoms:
            ImageDraw.Draw(im).polygon([(x * S - X0, y * S - Y0) for x, y in gm.exterior.coords], fill=255)
        return X0, Y0, np.asarray(im) > 0

    def _polys_mask(self, polys, grow=0.0):
        m = np.zeros((self.h, self.w), bool)
        for p in polys:
            X0, Y0, loc = self._poly_local(p, grow)
            self._or(m, X0, Y0, loc)
        return m

    def _or(self, m, X0, Y0, loc):
        h, w = loc.shape
        x0, y0 = max(0, X0), max(0, Y0)
        x1, y1 = min(self.w, X0 + w), min(self.h, Y0 + h)
        if x1 > x0 and y1 > y0:
            m[y0:y1, x0:x1] |= loc[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0]

    def free(self, poly, mode="clean", margin=10):
        """True when `poly` (grown by PAD) lies on the page inside the margin and on paper allowed in `mode`:
        clean: no ink · light: no dark ink and no text · knock: nothing hard (thin lines will get a white patch)"""
        x0, y0, x1, y1 = poly.bounds
        pr = self.page.rect
        if x0 < margin or y0 < margin or x1 > pr.width - margin or y1 > pr.height - margin:
            return False
        X0, Y0, loc = self._poly_local(poly, PAD)
        h, w = loc.shape
        if X0 < 0 or Y0 < 0 or X0 + w > self.w or Y0 + h > self.h:
            return False
        if mode == "clean":
            m = self.ink
        elif mode == "light":
            m = self.dark | self.text
        elif mode == "force":
            m = self.text                              # anything but text: a white patch goes under the value
        else:
            m = self.hard
        return not (m[Y0:Y0 + h, X0:X0 + w] & loc).any()

    def take(self, poly, grow=PAD):
        X0, Y0, loc = self._poly_local(poly, grow)
        for m in (self.ink, self.dark, self.hard, self.text):
            self._or(m, X0, Y0, loc)

    def take_rect(self, r, pad=0.8):
        self.take(Polygon([(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]), grow=pad)


# --------------------------------------------------------------------------------------------------------------- text
def frame_matrix(u, v, italic=False):
    """fitz morph matrix that lays text along u with its upright strokes along v (page coordinates, v pointing up)"""
    vx, vy = v
    if italic:
        vx, vy = vx + ITALIC_SLANT * u[0], vy + ITALIC_SLANT * u[1]
    # PyMuPDF applies a morph matrix with y pointing up: the page-space matrix (u, -v) goes in with b and c negated
    return fitz.Matrix(u[0], -u[1], vx, -vy, 0, 0)


def text_outline(origin, u, v, txt, fs, weight="reg", lo=-0.22, hi=0.80):
    w = FONT[weight].text_length(txt, fs)
    pts = []
    for x, y in ((0, lo), (w, lo), (w, hi), (0, hi)):
        pts.append((origin.x + x * u[0] + y * fs * v[0], origin.y + x * u[1] + y * fs * v[1]))
    return Polygon(pts), w


def put_text(page, origin, u, v, txt, fs, weight, color, italic=False):
    name = {"reg": "robReg", "light": "robLight", "med": "robMed", "bold": "robBold"}[weight]
    kw = dict(fontsize=fs, fontname=name, fontfile=TTF[weight], color=color)
    if abs(u[0] - 1) < 1e-4 and abs(u[1]) < 1e-4 and abs(v[0]) < 1e-4 and abs(v[1] + 1) < 1e-4 and not italic:
        page.insert_text(origin, txt, **kw)
    else:
        page.insert_text(origin, txt, morph=(origin, frame_matrix(u, v, italic)), **kw)


def rgb(c):
    if isinstance(c, (tuple, list)):
        return tuple(c[:3])
    return ((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255


# --------------------------------------------------------------------------------------------------------------- spots
DIM_ORDER = ["below", "above", "after", "before", "after>", "before<"]
SLANT_ORDER = ["below", "above", "after", "before", "below-l", "below-r", "after>", "before<"]
GRID_ORDER = ["below", "above", "after", "before", "after>", "before<"]
STAGES = [("clean", 0.88), ("clean", 0.75), ("light", 0.88), ("light", 0.75), ("clean", 0.62), ("light", 0.62),
          ("knock", 0.75), ("knock", 0.62), ("clean", 0.52), ("light", 0.52), ("knock", 0.52), ("clean", 0.44),
          ("light", 0.44), ("knock", 0.44)]


def _spots(label, w, fs, name, lo_l, hi_l):
    s = label.size
    g1, g2 = 0.25 * s, 0.10 * s + 0.4
    adv = label.adv
    if name == "after":
        return [(adv + g1, 0)]
    if name == "before":
        return [(-(w + g1), 0)]
    if name == "after>":
        return [(adv + g1 + k * s, 0) for k in (0.25, 0.5, 0.75, 1.0, 1.4, 1.8)]
    if name == "before<":
        return [(-(w + g1) - k * s, 0) for k in (0.25, 0.5, 0.75, 1.0, 1.4, 1.8)]
    below = lo_l * s - g2 - 0.80 * fs
    above = hi_l * s + g2 + 0.22 * fs
    if name == "below":
        return [((adv - w) / 2, below)]
    if name == "above":
        return [((adv - w) / 2, above)]
    if name == "below-l":
        return [(0, below)]
    if name == "below-r":
        return [(adv - w, below)]
    if name == "below-v":                               # under the value of a 'H = 66.65' line
        x0 = getattr(label, "num_x", 0.0)
        return [(x0, below)]
    if name == "below-far":                             # further down: under the tile a piece label sits in
        return [((adv - w) / 2, below - k * s) for k in (0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.2, 2.6)]
    return []


def _reads_as_own(poly, own, others, same_line, label, band):
    d_own = poly.distance(own)
    if same_line:
        for B in others:
            d = poly.distance(B)
            if d < 0.5 * d_own:
                return False
            if d < d_own + 0.1 * label.size and band.intersects(B):
                return False
        return True
    c = poly.centroid
    dc = c.distance(own)
    for B in others:
        if poly.distance(B) < 0.25 * label.size and c.distance(B) < 1.25 * dc + 0.1:
            return False
        if c.distance(B) < 1.4 * dc:                    # clearly nearer to its own number than to any other
            return False
    return True


ROW_SCALES = (0.88, 0.8, 0.72, 0.66, 0.6, 0.54, 0.48, 0.44, 0.4, 0.36)


def place_row(cv, members, texts, weight="reg", color=None, min_share=0.6):
    """values for a row of numbers set close together on one baseline (the piece lengths of a segmentation diagram:
    '100 25 25 30 35 40 45 50'): every value centred under its own number — or all of them over — at one size small
    enough that neighbouring values keep apart.  Where the numbers are too close for a readable size the values are
    staggered: every other one a line lower, still centred under its number.  Members whose spot is not free are left
    out (returned as None).  Returns [result or None] in the order of `members`."""
    n = len(members)
    r0 = members[0]
    s = sorted(m.size for m in members)[n // 2]
    fo = FONT[weight]
    centres = [r0.along(m.origin) + m.adv / 2 for m in members]
    unit = [fo.text_length(t, 1.0) for t in texts]
    gap = 0.3 * s

    def fit(step):
        lim = [(centres[i + step] - centres[i] - gap) / ((unit[i] + unit[i + step]) / 2) for i in range(n - step)]
        return min(lim) if lim else 9e9
    fit1, fit2 = fit(1), fit(2)
    layouts = []
    for sc in ROW_SCALES:
        fs = s * sc
        if fs < 3.3:
            continue
        if fs <= fit1:
            layouts.append(("one", fs))
        elif fs <= fit2 and n >= 3:
            layouts.append(("two", fs))
    best = None
    for kind, fs in layouts:
        for pos in ("below", "above"):
            res = []
            for k, (m, t) in enumerate(zip(members, texts)):
                w = fo.text_length(t, fs)
                lo_l = -0.2 if "," in m.t else -0.03
                g2 = 0.10 * m.size + 0.4
                level = (k % 2) if kind == "two" else 0
                if pos == "below":
                    dy = lo_l * m.size - g2 - 0.80 * fs - level * 1.02 * fs
                else:
                    dy = 0.74 * m.size + g2 + 0.22 * fs + level * 1.02 * fs
                o = m.point((m.adv - w) / 2, 0)
                o = fitz.Point(o.x + dy * m.v[0], o.y + dy * m.v[1])
                poly, _ = text_outline(o, m.u, m.v, t, fs, weight)
                mode = next((md for md in ("clean", "light", "knock") if cv.free(poly, md)), None)
                res.append((o, poly, mode, fs, t))
            cnt = sum(1 for x in res if x[2])
            # every value placed matters most; then a single line over two, a larger size, below over above
            key = (cnt == n, cnt, fs >= 0.55 * s and kind == "one", fs, pos == "below")
            if best is None or key > best[0]:
                best = (key, res)
    if best is None or best[0][1] < max(2, min_share * n):
        return [None] * n
    out = []
    for m, (o, poly, mode, fs, t) in zip(members, best[1]):
        if not mode:
            out.append(None)
            continue
        if mode == "knock":
            patch = poly.buffer(0.35, join_style=2)
            sh = cv.page.new_shape()
            sh.draw_polyline([fitz.Point(x, y) for x, y in patch.exterior.coords])
            sh.finish(color=None, fill=(1, 1, 1), closePath=True, width=0)
            sh.commit()
        put_text(cv.page, o, m.u, m.v, t, fs, weight, rgb(color if color is not None else m.color), italic=m.italic)
        cv.take(poly)
        out.append({"spot": "row", "mode": mode, "fs": fs, "poly": poly})
    return out


def place(cv, label, txt, others, order=None, stages=STAGES, color=None, weight=None, min_fs=3.4, base=1.0,
          dry=False):
    """write `txt` by the run `label` at the first spot that is free and reads as the label's; returns a dict or None.
    `txt` may be a pair (text on the same line, text stacked above / below): '(32.87″)' beside a number, '32.87″' under it"""
    t_inline, t_stacked = txt if isinstance(txt, tuple) else (txt, txt)
    if order is None:
        order = DIM_ORDER if (label.upright or label.vertical) else SLANT_ORDER
    weight = weight or ("light" if label.weight == "light" else "reg")
    color = rgb(color if color is not None else label.color)
    own = label.outline()
    lo_l = -0.2 if "," in label.t else -0.03
    hi_l = 0.74
    u, v = label.u, label.v
    # the band of the label's own line (mid-glyph height, ± 0.3 sizes) for the same-line test: neighbours on the line
    # count, the lines above and below do not
    a = label.point(-60, 0.35)
    b = label.point(label.adv + 60, 0.35)
    band = LineString([(a.x, a.y), (b.x, b.y)]).buffer(0.3 * label.size)
    for mode, sc in stages:
        fs = label.size * sc * base
        if fs < min_fs:
            continue
        for spot in order:
            txt = t_inline if spot in ("after", "before", "after>", "before<") else t_stacked
            w = FONT[weight].text_length(txt, fs)
            for dx, dy in _spots(label, w, fs, spot, lo_l, hi_l):
                o = label.point(dx, 0)
                o = fitz.Point(o.x + dy * v[0], o.y + dy * v[1])
                poly, _ = text_outline(o, u, v, txt, fs, weight)
                if not cv.free(poly, mode):
                    continue
                if not _reads_as_own(poly, own, others, spot in ("after", "before", "after>", "before<"), label, band):
                    continue
                if not dry:
                    if mode in ("knock", "force"):
                        patch = poly.buffer(0.35, join_style=2)
                        sh = cv.page.new_shape()
                        sh.draw_polyline([fitz.Point(x, y) for x, y in patch.exterior.coords])
                        sh.finish(color=None, fill=(1, 1, 1), closePath=True, width=0)
                        sh.commit()
                    put_text(cv.page, o, u, v, txt, fs, weight, color, italic=label.italic)
                cv.take(poly)
                return {"spot": spot, "mode": mode, "fs": fs, "poly": poly}
    return None
