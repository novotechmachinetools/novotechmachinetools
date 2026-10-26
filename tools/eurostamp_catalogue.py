#!/usr/bin/env python3
"""The EUROSTAMP catalogue in inches as well — NovoTech's edition of the IT-EN tooling catalogue.

EUROSTAMP draws every tool in millimetres.  This keeps every page exactly as it is and writes the inch value next to each
metric number, in the catalogue's own font, size and colour:

  dimensions   the blue numbers on the drawings (26, 105, R 0,5 …)               → 105 (4.13″), R 0,5 (.020″)
  scale grid   the grey numbers round the squared diamond under each tool         → 20 (.79″), 40 (1.57″) …
  spec lines   H = 105.00, R = 0.5, V = 8                                         → H = 105.00 (4.134″), R = 0.5 (.020″) …
  length box   the ruled box of lengths and weights (835 mm | 12,6 kg …)          → a twin box with the same rows (32.87″ | 27.8 lb)
                                                                                   where every box of the page has room, else both
                                                                                   units inside each cell (835 mm / 32.87″)

Every addition goes where the paper is empty: after the number, else stacked above or below it, else further along the
line past an extension line, else before it.  The page is rendered to an ink mask; each placement is checked against it
and against what was already added.  Numbers that find no free spot are reported (and checked by eye).

    python3 tools/eurostamp_catalogue.py [--pages 36,116] [--out file.pdf] [--png dir]
"""
import argparse
import math
import os
import re

import fitz
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = "/home/claude/eurostamp/pdf/cat.pdf"
FONTS = {"reg": os.path.join(ROOT, "tools", "fonts", "Roboto-Regular.ttf"),
         "light": os.path.join(ROOT, "tools", "fonts", "Roboto-Light.ttf"),
         "med": os.path.join(ROOT, "tools", "fonts", "Roboto-Medium.ttf")}
FONT = {k: fitz.Font(fontfile=v) for k, v in FONTS.items()}
BLACK = 0x231F20
S = 4                                   # ink-mask resolution, px per pt
US_T_FT = 0.3048 * 1.10231              # t/m → US tons per foot
LONG_DIMS = {1000, 1050, 1100, 1200, 1250, 2000, 2050, 2400, 2550, 3000, 3050, 4050}     # blue numbers ≥ 1 m that are lengths
DIM_RE = re.compile(r"^(R\s?|Ø\s?)?(\d{1,4}(?:\s?[.,]\s?\d{1,2})?)$")
SPEC_RE = re.compile(r"^(H|R|V|B|L)\s*=\s*(\d+(?:[.,]\d+)?)$")     # lengths only: Max T/m is converted in the edition's table


def rgb(c):
    return ((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255


def is_blue(c):
    r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
    return b >= 100 and b - r >= 60 and b >= g and r + g + b < 450


def is_grey(c):
    r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
    return abs(r - g) < 16 and abs(g - b) < 16 and 70 <= r <= 175


def num(t):
    t = re.sub(r"\s+", "", t).replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def inch(mm, places=None):
    """decimal inches, leading zero dropped: 2 places from 1″ up and 3 below unless `places` is given — '4.13″', '.315″'"""
    v = mm / 25.4
    p = places if places is not None else (2 if v >= 1 else 3)
    s = f"{v:.{p}f}"
    return (s[1:] if s.startswith("0.") else s) + "″"


# ------------------------------------------------------------------------------------------------ page reading
def spans(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].strip():
                    out.append({"t": s["text"], "bbox": fitz.Rect(s["bbox"]), "size": s["size"], "font": s["font"],
                                "color": s["color"], "dir": (round(l["dir"][0], 3), round(l["dir"][1], 3)),
                                "origin": fitz.Point(s["origin"])})
    return out


def along(p, u):
    return p.x * u[0] + p.y * u[1]


def across(p, u):
    return p.x * (-u[1]) + p.y * u[0]


def extent(s):
    """length of a span along its direction"""
    u = s["dir"]
    if abs(u[0]) > 0.999 or abs(u[1]) > 0.999:
        b = s["bbox"]
        return abs(b.x1 - b.x0) * abs(u[0]) + abs(b.y1 - b.y0) * abs(u[1])
    return FONT["reg"].text_length(s["t"], s["size"])


def lines(sp):
    """spans that sit on one baseline and follow each other → one run of text ('R' + '0,4', 'Max T/m ' + '= ' + '100')"""
    out = []
    for s in sorted(sp, key=lambda s: (s["dir"], round(across(s["origin"], s["dir"]), 0), along(s["origin"], s["dir"]))):
        u = s["dir"]
        a0 = along(s["origin"], u)
        for L in out:
            if L["dir"] == u and abs(L["base"] - across(s["origin"], u)) < 0.3 * s["size"] and -1.5 < a0 - L["end"] < 0.7 * s["size"]:
                gap = a0 - L["end"]
                L["text"] += (" " if gap > 0.18 * s["size"] and not L["text"].endswith(" ") and not s["t"].startswith(" ") else "") + s["t"]
                L["spans"].append(s)
                L["end"] = a0 + extent(s)
                L["bbox"] |= s["bbox"]
                L["size"] = max(L["size"], s["size"])
                L["color"], L["font"] = s["color"], s["font"]
                break
        else:
            out.append({"dir": u, "base": across(s["origin"], u), "start": a0, "end": a0 + extent(s), "text": s["t"],
                        "spans": [s], "bbox": fitz.Rect(s["bbox"]), "size": s["size"], "color": s["color"], "font": s["font"],
                        "origin": s["origin"]})
    for L in out:
        L["t"] = L["text"].strip()
        L["adv"] = L["end"] - L["start"]
    return out


def ink_mask(page):
    pix = page.get_pixmap(matrix=fitz.Matrix(S, S), alpha=False, colorspace=fitz.csGRAY)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width) < 238


class Canvas:
    """the page's ink plus everything added so far; placements must land on empty paper inside the page margins"""

    def __init__(self, page):
        self.page = page
        pix = page.get_pixmap(matrix=fitz.Matrix(S, S), alpha=False, colorspace=fitz.csGRAY)
        g = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width)
        self.m = g < 238                                # any ink
        self.md = g < 165                               # dark ink only: text, outlines, dimension lines — not the grey tool bodies
        self.h, self.w = self.m.shape
        self.free_rect = fitz.Rect(14, 50, page.rect.width - 14, page.rect.height - 38)

    def _ix(self, r):
        return (max(0, int(r.x0 * S)), max(0, int(r.y0 * S)), min(self.w, int(math.ceil(r.x1 * S))), min(self.h, int(math.ceil(r.y1 * S))))

    def clear(self, r, pad=0.6, ignore=None, dark_only=False, mask=None, margin=None):
        r = fitz.Rect(r.x0 - pad, r.y0 - pad, r.x1 + pad, r.y1 + pad)
        fr = self.free_rect if margin is None else fitz.Rect(margin, self.free_rect.y0, self.page.rect.width - margin, self.free_rect.y1)
        if not fr.contains(r):
            return False
        x0, y0, x1, y1 = self._ix(r)
        sub = (mask if mask is not None else (self.md if dark_only else self.m))[y0:y1, x0:x1]
        if ignore is not None and sub.any():
            sub = sub.copy()
            ix0, iy0, ix1, iy1 = self._ix(ignore)
            sub[max(0, iy0 - y0):max(0, iy1 - y0), max(0, ix0 - x0):max(0, ix1 - x0)] = False
        return not sub.any()

    def take(self, r, pad=0.8, mask=None):
        x0, y0, x1, y1 = self._ix(fitz.Rect(r.x0 - pad, r.y0 - pad, r.x1 + pad, r.y1 + pad))
        if mask is not None:
            mask[y0:y1, x0:x1] = True
            return
        self.m[y0:y1, x0:x1] = True
        self.md[y0:y1, x0:x1] = True


# ------------------------------------------------------------------------------------------------ text geometry
def text_box(origin, u, txt, font, fs):
    """axis-aligned box of a text run whose baseline starts at `origin` and runs along u (page coords, y down)"""
    L = FONT[font].text_length(txt, fs)
    up = (u[1], -u[0])
    pts = [(origin.x + u[0] * a + up[0] * b, origin.y + u[1] * a + up[1] * b) for a in (0, L) for b in (-0.23 * fs, 0.78 * fs)]
    return fitz.Rect(min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def put_text(page, origin, u, txt, font, fs, color):
    ang = math.degrees(math.atan2(-u[1], u[0]))     # counter-clockwise, PDF sense
    kw = dict(fontsize=fs, fontname="rob" + font, fontfile=FONTS[font], color=rgb(color))
    if abs(ang) < 0.3:
        page.insert_text(origin, txt, **kw)
    elif abs(ang - 90) < 0.3:
        page.insert_text(origin, txt, rotate=90, **kw)
    else:
        page.insert_text(origin, txt, morph=(origin, fitz.Matrix(-ang)), **kw)


def ink_box(L):
    """the box of a run's digits — baseline to cap height — rather than the font's line box"""
    u, O, adv, h = L["dir"], L["origin"], L["adv"], 0.72 * L["size"]
    up = (u[1], -u[0])
    pts = [(O.x + u[0] * a + up[0] * b, O.y + u[1] * a + up[1] * b) for a in (0, adv) for b in (0, h)]
    return fitz.Rect(min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def gap(a, b):
    """the distance between two rectangles, 0 when they overlap"""
    dx = max(0.0, max(a.x0, b.x0) - min(a.x1, b.x1))
    dy = max(0.0, max(a.y0, b.y0) - min(a.y1, b.y1))
    return math.hypot(dx, dy)


def reads_as_own(r, L, others, same_line):
    """True when text at r reads as belonging to the run L: on L's own line with no other text on that line as near,
    or stacked above / below L and clearly nearer to it than to any other text of the page"""
    own = ink_box(L)
    d_own = gap(r, own)
    sz = L["size"]
    if same_line:
        vertical = abs(L["dir"][1]) > 0.7
        for B in others:
            d = gap(r, B)
            if d < 0.5 * d_own:
                return False
            ov = (min(r.x1, B.x1) - max(r.x0, B.x0)) if vertical else (min(r.y1, B.y1) - max(r.y0, B.y0))
            span = min(r.width, B.width) if vertical else min(r.height, B.height)
            if d < d_own + 0.1 * sz and ov > 0.3 * span:
                return False
        return True
    return all(gap(r, B) >= d_own + 0.15 * sz for B in others)


def place(cv, L, extra, font, fs, order, color=None, dark_only=False, others=()):
    """write `extra` next to the text run L at the first free spot of `order` where it reads as L's (`others`: the ink
    boxes of the page's other text); returns the spot or None"""
    u = L["dir"]
    up = (u[1], -u[0])
    O = L["origin"]
    adv = L["adv"]
    Le = FONT[font].text_length(extra, fs)
    gap_ = 0.22 * L["size"]
    color = L["color"] if color is None else color
    far = [k * 0.5 for k in range(1, max(2, int(2 * L["size"])) + 1)]    # a little further on — at most one text height
    for spot in order:
        cands = []
        if spot == "after":
            cands = [adv + gap_]
        elif spot == "after+":
            cands = [("lift", adv + gap_)]
        elif spot == "after>":                          # past an arrow tip or a line end on the same baseline
            cands = [adv + gap_ + k for k in far]
        elif spot == "before":
            cands = [-(Le + gap_)]
        elif spot == "before<":
            cands = [-(Le + gap_) - k for k in far]
        for c in cands:
            lift = 0.0
            if isinstance(c, tuple):
                c, lift = c[1], 0.26 * fs
            o = fitz.Point(O.x + u[0] * c + up[0] * lift, O.y + u[1] * c + up[1] * lift)
            r = text_box(o, u, extra, font, fs)
            if cv.clear(r, ignore=L["bbox"], dark_only=dark_only) and reads_as_own(r, L, others, True):
                put_text(cv.page, o, u, extra, font, fs, color)
                cv.take(r)
                return spot
        if spot in ("above", "below"):
            # stacked: clear of the number's cap height (above) or of its baseline (below) by ~0.7 pt, centred on it
            k = (0.72 * L["size"] + 0.7 + 0.23 * fs) if spot == "above" else -(0.74 * fs + 0.9)
            c = (adv - Le) / 2
            o = fitz.Point(O.x + u[0] * c + up[0] * k, O.y + u[1] * c + up[1] * k)
            r = text_box(o, u, extra, font, fs)
            if cv.clear(r, ignore=L["bbox"], dark_only=dark_only) and reads_as_own(r, L, others, False):
                put_text(cv.page, o, u, extra, font, fs, color)
                cv.take(r)
                return spot
    return None


# ------------------------------------------------------------------------------------------------ the length / weight boxes
LEN_RE = re.compile(r"^\s*(\d{2,4})\s*mm\s*$")
KG_RE = re.compile(r"^\s*(\d+(?:[.,]\d+)?)\s*kg\s*$", re.I)
BOTH_RE = re.compile(r"^\s*(\d{2,4})\s*mm\s+(\d+(?:[.,]\d+)?)\s*kg\s*$", re.I)


def boxes(sp):
    """rows of the ruled length boxes: [{rows:[{mm, kg, L (span), K (span or None)}]}]"""
    lens = [s for s in sp if (LEN_RE.match(s["t"]) or BOTH_RE.match(s["t"])) and s["dir"] == (1.0, 0.0) and s["size"] < 10]
    kgs = [s for s in sp if KG_RE.match(s["t"]) and s["dir"] == (1.0, 0.0) and s["size"] < 10]
    rows = []
    for L in lens:
        cy = (L["bbox"].y0 + L["bbox"].y1) / 2
        both = BOTH_RE.match(L["t"])
        if both:
            rows.append({"mm": int(both.group(1)), "kg": num(both.group(2)), "L": L, "K": None})
            continue
        cand = [K for K in kgs if -2 < K["bbox"].x0 - L["bbox"].x1 < 45 and abs((K["bbox"].y0 + K["bbox"].y1) / 2 - cy) < 7]
        K = min(cand, key=lambda K: abs((K["bbox"].y0 + K["bbox"].y1) / 2 - cy)) if cand else None
        rows.append({"mm": int(LEN_RE.match(L["t"]).group(1)), "kg": num(KG_RE.match(K["t"]).group(1)) if K else None, "L": L, "K": K})
    rows.sort(key=lambda r: (round(r["L"]["bbox"].x0), r["L"]["bbox"].y0))
    out = []
    for r in rows:
        for b in out:
            last = b["rows"][-1]
            if abs(last["L"]["bbox"].x0 - r["L"]["bbox"].x0) < 3 and 0 < r["L"]["bbox"].y0 - last["L"]["bbox"].y0 < 24:
                b["rows"].append(r)
                break
        else:
            out.append({"rows": [r]})
    return out


def box_lines(drawings, rect):
    """the ruled lines of a length box: stroke colour and width, horizontal rules [(y, x0, x1)], vertical rules [(x, y0, y1)]"""
    hs, vs, col, wid = [], [], None, 0.5
    big = fitz.Rect(rect.x0 - 12, rect.y0 - 9, rect.x1 + 12, rect.y1 + 12)
    for d in drawings:
        if not d.get("color") or d["type"] not in ("s", "fs"):
            continue
        for it in d["items"]:
            if it[0] == "l":
                p, q = it[1], it[2]
                if not (big.contains(p) and big.contains(q)):
                    continue
                if abs(p.y - q.y) < 0.3 and abs(p.x - q.x) > 8:
                    hs.append((p.y, min(p.x, q.x), max(p.x, q.x)))
                elif abs(p.x - q.x) < 0.3 and abs(p.y - q.y) > 4:
                    vs.append((p.x, min(p.y, q.y), max(p.y, q.y)))
                else:
                    continue
                col, wid = d["color"], d.get("width") or 0.5
            elif it[0] == "re":
                R = it[1]
                if not big.contains(R) or R.width < 8:
                    continue
                hs += [(R.y0, R.x0, R.x1), (R.y1, R.x0, R.x1)]
                vs += [(R.x0, R.y0, R.y1), (R.x1, R.y0, R.y1)]
                col, wid = d["color"], d.get("width") or 0.5
    return col, wid, hs, vs


def lb_text(kg):
    v = kg * 2.20462
    return f"{v:.1f} lb" if v < 100 else f"{v:,.0f} lb"


def box_geometry(drawings, b):
    """outer edges, full-width rules, the column divider and the gaps of a length box"""
    rows = b["rows"]
    tight = fitz.Rect(min(r["L"]["bbox"].x0 for r in rows), min(r["L"]["bbox"].y0 for r in rows),
                      max((r["K"] or r["L"])["bbox"].x1 for r in rows), max(r["L"]["bbox"].y1 for r in rows))
    col, wid, hs, vs = box_lines(drawings, tight)
    lefts = [v[0] for v in vs if v[0] <= tight.x0 + 2]
    rights = [v[0] for v in vs if v[0] >= tight.x1 - 2]
    X0 = min(lefts) if lefts else tight.x0 - 4
    X1 = max(rights) if rights else tight.x1 + 4
    Y0 = min([h[0] for h in hs] + [tight.y0 - 2])
    Y1 = max([h[0] for h in hs] + [tight.y1 + 3])
    full = sorted(set(round(h[0], 2) for h in hs if h[2] - h[1] > 0.6 * (X1 - X0)))
    mids = sorted(v[0] for v in vs if X0 + 3 < v[0] < X1 - 3)
    gaps = []                                          # Trumpf boxes come as two boxes one under the other
    outer = sorted((v[1], v[2]) for v in vs if abs(v[0] - X0) < 1.5)
    for (a1, b1), (a2, b2) in zip(outer, outer[1:]):
        if a2 - b1 > 1.5:
            gaps.append((b1, a2))
    return {"X0": X0, "X1": X1, "Y0": Y0, "Y1": Y1, "full": full, "mid": mids[0] if mids else None, "gaps": gaps,
            "col": col or (0.584, 0.661, 0.795), "wid": wid}


def twin_plan(cv, geo, b, mask):
    """where the imperial twin of a box fits (same rows, inches and pounds): attached on the right, else on the left, else
    under or over it.  Reserves the spot in `mask`; returns the plan or None"""
    rows = b["rows"]
    X0, X1, Y0, Y1 = geo["X0"], geo["X1"], geo["Y0"], geo["Y1"]
    fs0 = rows[0]["L"]["size"]
    ins = [inch(r["mm"], 2) for r in rows]
    lbs = [lb_text(r["kg"]) if r["kg"] is not None else "" for r in rows]
    H = Y1 - Y0
    for f in (fs0, fs0 * 0.9, fs0 * 0.82, fs0 * 0.75):
        pad = 0.44 * f
        wi = max(FONT["light"].text_length(t, f) for t in ins) + 2 * pad
        wl = (max(FONT["light"].text_length(t, f) for t in lbs if t) + 2 * pad) if any(lbs) else 0
        W = wi + wl
        spots = [("right", fitz.Rect(X1, Y0, X1 + W, Y1)), ("left", fitz.Rect(X0 - W, Y0, X0, Y1))]
        for g in (3, 6):
            Wb = max(W, X1 - X0)
            spots += [("below", fitz.Rect(X0, Y1 + g, X0 + Wb, Y1 + g + H)), ("below", fitz.Rect(X1 - Wb, Y1 + g, X1, Y1 + g + H)),
                      ("above", fitz.Rect(X0, Y0 - g - H, X0 + Wb, Y0 - g)), ("above", fitz.Rect(X1 - Wb, Y0 - g - H, X1, Y0 - g))]
        for spot, R in spots:
            test = fitz.Rect(R.x0 + (1.8 if spot == "right" else 0), R.y0 + (1.2 if spot in ("right", "left") else 0),
                             R.x1 - (1.8 if spot == "left" else 0), R.y1 - (1.2 if spot in ("right", "left") else 0))
            if cv.clear(test, pad=0.8, mask=mask, margin=7):
                cv.take(R, pad=1, mask=mask)
                return {"spot": spot, "R": R, "f": f, "pad": pad, "wi": wi if spot in ("right", "left") else R.width * wi / W,
                        "wl": wl, "ins": ins, "lbs": lbs, "dy": R.y0 - Y0}
    return None


def twin_draw(cv, geo, b, plan):
    page = cv.page
    R, dy, f, pad = plan["R"], plan["dy"], plan["f"], plan["pad"]
    col, wid = geo["col"], geo["wid"]
    shape = page.new_shape()
    shape.draw_rect(R)
    shape.finish(color=col, fill=(1, 1, 1), width=wid)
    for y in geo["full"]:
        if R.y0 + 0.5 < y + dy < R.y1 - 0.5:
            shape.draw_line(fitz.Point(R.x0, y + dy), fitz.Point(R.x1, y + dy))
    if plan["wl"]:
        shape.draw_line(fitz.Point(R.x0 + plan["wi"], R.y0), fitz.Point(R.x0 + plan["wi"], R.y1))
    shape.finish(color=col, width=wid)
    for g0, g1 in geo["gaps"]:                         # blank the gap between the two boxes, like the original
        shape.draw_rect(fitz.Rect(R.x0 - 0.4, g0 + dy + 0.35, R.x1 + 0.4, g1 + dy - 0.35))
        shape.finish(color=None, fill=(1, 1, 1), width=0)
    shape.commit()
    for r, ti, tl in zip(b["rows"], plan["ins"], plan["lbs"]):
        put_text(page, fitz.Point(R.x0 + pad, r["L"]["origin"].y + dy), (1, 0), ti, "light", f, BLACK)
        if tl:
            yk = (r["K"]["origin"].y if r["K"] else r["L"]["origin"].y) + dy
            put_text(page, fitz.Point(R.x1 - pad - FONT["light"].text_length(tl, f), yk), (1, 0), tl, "light", f, BLACK)
    cv.take(R, pad=1)


def dual_plan(geo, b, sp):
    """the length box itself in both units: each cell keeps its metric value and gets the imperial one under it, one
    smaller size for the whole box so two lines fit a row (835 mm / 32.87″ · 12,6 kg / 27.8 lb).  The ruled lines stay;
    returns (rects to redact, texts to write)"""
    rows = b["rows"]
    X0, X1, ys = geo["X0"], geo["X1"], geo["full"]
    tags = [s for s in sp if s["size"] <= 6.5 and re.search(r"FRAZ|SECT|SEZ|HORN|SHORT", s["t"].upper())]
    cells = []
    for r in rows:
        cy = (r["L"]["bbox"].y0 + r["L"]["bbox"].y1) / 2
        top = max([y for y in ys if y <= cy + 0.5] or [r["L"]["bbox"].y0 - 2])
        bot = min([y for y in ys if y > cy + 0.5] or [r["L"]["bbox"].y1 + 3])
        T = [t for t in tags if -3.5 <= t["bbox"].y0 - r["L"]["bbox"].y1 < 5 and abs(t["bbox"].x0 - r["L"]["bbox"].x0) < 8]
        cells.append((r, top, bot, T))
    plain = [bot - top for r, top, bot, T in cells if not T] or [min(bot - top for r, top, bot, T in cells) - 5]
    fs = max(4.4, min(rows[0]["L"]["size"] * 0.8, (min(plain) - 1.0) / 1.88))
    red, wr = [], []
    for r, top, bot, T in cells:
        for sx in [r["L"]] + ([r["K"]] if r["K"] else []) + T:
            red.append(fitz.Rect(sx["bbox"].x0 + 0.15, sx["bbox"].y0 + 0.6, sx["bbox"].x1 - 0.15, sx["bbox"].y1 - 0.6))
        h = bot - top
        block = 1.88 * fs + (0.95 * min(T[0]["size"], 4.6) + 0.3 if T else 0)
        b1 = top + (h - block) / 2 + 0.72 * fs
        b2 = b1 + 1.0 * fs + 0.2
        pad = 0.44 * rows[0]["L"]["size"]
        wr.append((fitz.Point(X0 + pad, b1), f"{r['mm']} mm", fs))
        wr.append((fitz.Point(X0 + pad, b2), inch(r["mm"], 2), fs))
        if T:
            tfs = min(T[0]["size"], 4.6)
            wr.append((fitz.Point(X0 + pad, b2 + 0.23 * fs + 0.74 * tfs + 0.3), T[0]["t"].strip(), tfs))
        if r["kg"] is not None:
            kg_txt = (f"{r['kg']:.1f}" if r["kg"] < 100 else f"{r['kg']:.0f}").replace(".", ",") + " kg"
            k1 = top + (h - 1.88 * fs) / 2 + 0.72 * fs
            for y, t in ((k1, kg_txt), (k1 + 1.0 * fs + 0.2, lb_text(r["kg"]))):
                wr.append((fitz.Point(X1 - pad - FONT["light"].text_length(t, fs), y), t, fs))
    return red, wr


# ------------------------------------------------------------------------------------------------ one page
DIM_ORDER = ["after", "above", "below", "after+", "after>", "before", "before<"]
GRID_ORDER = ["below", "above", "after", "before", "after>", "before<"]


def piece_labels(sp):
    """'1 X 200' piece counts and lengths stacked inside the small tool icons of the segmentation pages: not dimensions"""
    xs = [s for s in sp if s["t"].strip() in ("X", "x") and is_blue(s["color"])]
    skip = set()
    for s in sp:
        for x in xs:
            if abs((s["bbox"].x0 + s["bbox"].x1) / 2 - (x["bbox"].x0 + x["bbox"].x1) / 2) < 6 and (
                    -1 <= s["bbox"].y0 - x["bbox"].y1 < 4 or -1 <= x["bbox"].y0 - s["bbox"].y1 < 4):
                skip.add(id(s))
    return skip


def annotate_page(page, report, box_mode="auto"):
    cv = Canvas(page)
    sp = spans(page)
    ls = lines(sp)
    inks = [(id(L), ink_box(L)) for L in ls]

    def others(L):
        return [b for k, b in inks if k != id(L)]
    drawings = page.get_drawings()
    n = {"dim": 0, "grid": 0, "spec": 0, "box": 0}
    # 1 · spec lines, black: 'H = 105.00', 'R = 0.5', 'V = 8'
    for L in ls:
        m = SPEC_RE.match(re.sub(r"\s+", " ", L["t"]))
        if not m or is_blue(L["color"]) or is_grey(L["color"]):
            continue
        v = num(m.group(2))
        if not v:
            continue
        lab = m.group(1)
        extra = f"({v * US_T_FT:.1f} US t/ft)" if lab.startswith("Max") else (f"({v / 25.4:.3f}″)" if v >= 25.4 else f"({inch(v)})")
        fnt = "light" if "Light" in L["font"] else "reg"
        if place(cv, L, extra, fnt, L["size"] * 0.82, ["after", "after>"], others=others(L)) or \
                place(cv, L, extra, fnt, L["size"] * 0.68, ["after", "after>"], others=others(L)):
            n["spec"] += 1
        else:
            report.append(("spec", page.number + 1, L["t"]))
    # 2 · dimensions on the drawings (blue), longest first — they have the least room
    skip = piece_labels(sp)
    dims = []
    for L in ls:
        if not is_blue(L["color"]) or L["size"] >= 14 or "Black" in L["font"] or "Bold" in L["font"] or "Italic" in L["font"]:
            continue
        if any(id(x) in skip for x in L["spans"]):
            continue
        m = DIM_RE.match(L["t"])
        if not m:
            continue
        v = num(m.group(2))
        if v is None or v == 0 or (v >= 1000 and v not in LONG_DIMS):
            continue
        dims.append((L, v))
    left = []
    for L, v in sorted(dims, key=lambda d: -len(d[0]["t"])):
        extra = f"({inch(v)})"
        if any(place(cv, L, extra, "reg", L["size"] * k, DIM_ORDER, others=others(L)) for k in (0.88, 0.72, 0.6)):
            n["dim"] += 1
        else:
            left.append((L, v))
    # 3 · the length boxes: imperial twins if every box of the page has room for one, else both units inside each box
    bxs = boxes(sp)
    geos = [box_geometry(drawings, b) for b in bxs]
    plans = None
    if bxs and box_mode in ("auto", "twin"):
        trial = cv.m.copy()
        plans = [twin_plan(cv, g, b, trial) for g, b in zip(geos, bxs)]
        if box_mode == "auto" and not all(plans):
            plans = None
    if plans:
        for g, b, pl in zip(geos, bxs, plans):
            if pl:
                twin_draw(cv, g, b, pl)
                n["box"] += 1
    elif bxs:
        red, wr = [], []
        for g, b in zip(geos, bxs):
            r_, w_ = dual_plan(g, b, sp)
            red += r_
            wr += w_
        for r in red:
            page.add_redact_annot(r, fill=False)
        page.apply_redactions(images=0, graphics=0, text=0)
        for o, t, fs in wr:
            put_text(page, o, (1, 0), t, "light", fs, BLACK)
        n["box"] += len(bxs)
    # 4 · the scale grid (grey integers; 0 needs nothing)
    for L in ls:
        if not is_grey(L["color"]) or not re.fullmatch(r"\d{1,3}", L["t"]) or not 6 <= L["size"] <= 11:
            continue
        v = int(L["t"])
        if v == 0:
            continue
        extra = f"({inch(v, 2)})"
        if place(cv, L, extra, "reg", L["size"] * 0.78, GRID_ORDER, others=others(L)) or \
                place(cv, L, extra, "reg", L["size"] * 0.66, GRID_ORDER, others=others(L)):
            n["grid"] += 1
        else:
            report.append(("grid", page.number + 1, L["t"]))
    # 5 · dimensions still without a spot: allowed over the light grey of a tool body (never over text or lines)
    for L, v in left:
        extra = f"({inch(v)})"
        if any(place(cv, L, extra, "reg", L["size"] * k, DIM_ORDER, dark_only=True, others=others(L)) for k in (0.88, 0.72, 0.6)):
            n["dim"] += 1
        else:
            report.append(("dim", page.number + 1, L["t"]))
    return n


def catalogue_codes(doc):
    """the tool codes printed as block titles (Roboto-BlackItalic) through the catalogue"""
    out = set()
    for page in doc:
        for s in spans(page):
            t = s["t"].strip()
            if "Italic" in s["font"] and ("Black" in s["font"] or "Bold" in s["font"]) and s["size"] >= 14 and re.fullmatch(r"\d{4}(S|PN|/\d+)?", t):
                out.add(t)
    return out


def page_dims(doc_or_path=CAT):
    """{page number: set of the dimension values (mm) printed in blue on it} — what a drawing of a tool on that page may show"""
    doc = fitz.open(doc_or_path) if isinstance(doc_or_path, str) else doc_or_path
    out = {}
    for pno in range(13, doc.page_count):
        vals = set()
        for L in lines(spans(doc[pno])):
            if not is_blue(L["color"]) or L["size"] >= 14 or any(k in L["font"] for k in ("Black", "Bold", "Italic", "Thin")):
                continue
            if L["bbox"].y0 > doc[pno].rect.height - 50:      # the folio
                continue
            m = DIM_RE.match(L["t"])
            if m:
                v = num(m.group(2))
                if v and (v < 1000 or v in LONG_DIMS):
                    vals.add(v)
        out[pno + 1] = vals
    return out


def code_pages(doc_or_path=CAT):
    """{code: [pages where its block title is printed]}"""
    doc = fitz.open(doc_or_path) if isinstance(doc_or_path, str) else doc_or_path
    out = {}
    for pno in range(doc.page_count):
        for s in spans(doc[pno]):
            t = s["t"].strip()
            if "Italic" in s["font"] and ("Black" in s["font"] or "Bold" in s["font"]) and s["size"] >= 10:
                for c in re.findall(r"\d{4}(?:S|PN)?", t):
                    out.setdefault(c, [])
                    if pno + 1 not in out[c]:
                        out[c].append(pno + 1)
    return out


def annotate(src=CAT, pages=None, first=14):
    doc = fitz.open(src)
    report, tot = [], {"dim": 0, "grid": 0, "spec": 0, "box": 0}
    for pno in range(doc.page_count):
        if (pages and pno + 1 not in pages) or pno + 1 < first:
            continue
        n = annotate_page(doc[pno], report)
        for k in tot:
            tot[k] += n[k]
    return doc, tot, report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--png", default="")
    ap.add_argument("--report", default="")
    a = ap.parse_args()
    pages = {int(x) for x in a.pages.split(",") if x} or None
    doc, tot, report = annotate(pages=pages)
    print(tot, len(report), "not placed")
    if a.report:
        import json
        json.dump(report, open(a.report, "w"))
    for r in report[:120]:
        print("  ", r)
    if a.png:
        os.makedirs(a.png, exist_ok=True)
        for p in sorted(pages or []):
            doc[p - 1].get_pixmap(dpi=130).save(os.path.join(a.png, f"a{p:03d}.png"))
    if a.out:
        doc.subset_fonts()
        doc.save(a.out, garbage=3, deflate=True, encryption=fitz.PDF_ENCRYPT_NONE)
        print("saved", a.out, os.path.getsize(a.out) // 1024, "KB")
