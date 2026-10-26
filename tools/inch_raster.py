#!/usr/bin/env python3
"""Inch values next to the millimetre numbers of a raster drawing (EUROSTAMP's web-shop drawings and diagrams).

The drawings are pictures, so the numbers are found first.  Long thin lines are taken out (a centre line through the 0 of
a V opening would otherwise swallow it), dark glyph-sized blobs are grouped into runs of text — upright glyphs side by
side on one baseline, turned glyphs in one column, slanted ones close together, so that the labels stacked along a scale
grid stay apart — and each glyph is matched against rendered Roboto digits (Tesseract when a match is unsure).  A small
blob between two digits is the decimal comma, one raised after the last digit a degree sign (an angle: no inch value).
The colour says what a number is: blue-grey dimensions, or black scale-grid labels when the drawing has a grid (in a
drawing printed all in black the black numbers are its dimensions).  A dimension is only annotated when its value is
one the catalogue prints for that tool (`expect`), a grid label only when it is a multiple of the grid step, and a lone
'1' or an unsure lone glyph never — a number that cannot be read for sure is left alone rather than given a wrong value.

Each number then gets '(x.xx″)' in its own colour where the paper is empty and where it reads as that number's: after
it, else stacked above / below it, else a little further along, else before it — never nearer to another number than to
its own.  The scale grid is annotated label by label in one size; when most labels have no room, every other label (20,
40, 60 …) or every 50, and when not even those fit, none.

    annotate(rgb, expect=None) -> (image, not placed, numbers)
    python3 tools/inch_raster.py in.png out.png [expected values, ';' separated]
"""
import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(ROOT, "tools", "fonts", "Roboto-Regular.ttf")


def inch(mm, places=None):
    v = mm / 25.4
    p = places if places is not None else (2 if v >= 1 else 3)
    s = f"{v:.{p}f}"
    return (s[1:] if s.startswith("0.") else s) + "″"


def on_white(im):
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    return im.convert("RGB")


_TEMPL = None


def _norm(mask):
    """a glyph mask → (zero-mean unit vector at 20×28, aspect ratio)"""
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None, 1.0
    m = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = m.shape
    im = Image.fromarray((m > 0).astype(np.uint8) * 255).resize((20, 28), Image.BILINEAR)
    v = np.asarray(im, np.float32) / 255
    v -= v.mean()
    return v / (np.linalg.norm(v) + 1e-6), w / h


def _templates():
    """the digits, R and Ø of Roboto in three weights, upright and slanted 12° like the italic labels of the length
    diagrams — an italic 1 must not pass for a 7"""
    global _TEMPL
    if _TEMPL is None:
        _TEMPL = []
        for fn in ("Roboto-Regular.ttf", "Roboto-Light.ttf", "Roboto-Medium.ttf"):
            font = ImageFont.truetype(os.path.join(ROOT, "tools", "fonts", fn), 90)
            for ch in "0123456789RØ":
                im = Image.new("L", (160, 120), 0)
                ImageDraw.Draw(im).text((30, 0), ch, font=font, fill=255)
                for shear in (0.0, 0.21):
                    g = im if not shear else im.transform(im.size, Image.AFFINE, (1, shear, -shear * 120, 0, 1, 0), Image.BILINEAR)
                    v, ar = _norm(np.asarray(g) > 127)
                    _TEMPL.append((ch, v, ar))
    return _TEMPL


def _classify(mask):
    """the digit (or R) a glyph mask shows: best match against the rendered Roboto glyphs, width/height ratio included →
    (character, lead over the runner-up, score).  A printed digit scores 0.7 – 0.9, an arrow tip or a line end below 0.3."""
    v, ar = _norm(mask)
    if v is None:
        return None, 0, 0
    best = {}
    for ch, t, tar in _templates():
        sc = float((v * t).sum()) - 0.9 * abs(math.log(max(ar, 0.05) / tar))
        best[ch] = max(best.get(ch, -9), sc)
    order = sorted(best.items(), key=lambda kv: -kv[1])
    return order[0][0], order[0][1] - order[1][1], order[0][1]


def _ocr(bw):
    import pytesseract
    big = bw.resize((bw.width * 3, bw.height * 3), Image.LANCZOS)
    big = Image.fromarray(np.pad(np.asarray(big), 24, constant_values=255))
    out = []
    for psm in (7, 8):
        t = pytesseract.image_to_string(big, config=f"--psm {psm} -c tessedit_char_whitelist=0123456789R").strip().replace(" ", "")
        out.append(t)
    return out


def _components(lab):
    objs = ndimage.find_objects(lab)
    areas = np.bincount(lab.ravel())
    comps = []
    for i, sl in enumerate(objs, 1):
        if sl is None:
            continue
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        comps.append({"i": i, "x0": sl[1].start, "y0": sl[0].start, "x1": sl[1].stop, "y1": sl[0].stop, "h": h, "w": w,
                      "area": int(areas[i]), "cx": (sl[1].start + sl[1].stop) / 2, "cy": (sl[0].start + sl[0].stop) / 2})
    return comps


def _cap(comps):
    """digit size: the commonest height of upright digit-like blobs (a callout lettered large, 'R 3' alone on a detail
    drawing, when there are none of the usual size)"""
    for lo, hi in ((9, 48), (49, 140)):
        cand = [c for c in comps if lo <= c["h"] <= hi and 1.15 * c["w"] < c["h"] < 3.4 * c["w"] and c["area"] > 0.12 * c["h"] * c["w"]]
        if cand:
            hist = np.bincount([c["h"] for c in cand])
            return int(np.argmax(np.convolve(hist, [1, 1, 1], "same")))
    return 0


def text_size(rgb):
    """the height of the drawing's digits in px (0 when it has none)"""
    dark = np.asarray(rgb.convert("RGB")).astype(np.int16).mean(axis=2) < 150
    lab, _ = ndimage.label(dark, structure=np.ones((3, 3)))
    return _cap(_components(lab))


def _dash_dot(dark, thin, cap):
    """the thin pixels of dash-dot and dashed centre lines running down a column: dashes (and dots) a few pixels apart.  A
    dash may be shorter than a long line, yet it is the one that crosses the 0 of a V-opening dimension on the axis."""
    lab, n = ndimage.label(dark, structure=[[0, 1, 0], [0, 1, 0], [0, 1, 0]])
    cols = {}
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is not None:
            cols.setdefault(sl[1].start, []).append((sl[0].start, sl[0].stop, i))
    mark = np.zeros(n + 1, bool)
    dot, dash, step = max(3, 0.2 * cap), 0.5 * cap, max(8, int(0.45 * cap))
    for rs in cols.values():
        rs.sort()
        chain = []
        for r in rs + [None]:
            if r is not None and (not chain or r[0] - chain[-1][1] <= step):
                chain.append(r)
                continue
            if chain and chain[-1][1] - chain[0][0] >= 4 * cap:
                lens = [b - a for a, b, _ in chain]
                dashes = [L for L in lens if L >= dash]
                regular = False
                if len(lens) >= 6 and chain[-1][1] - chain[0][0] >= 6 * cap:
                    md = float(np.median(lens))             # a plain dashed line: dashes of one length (one of them
                    regular = md >= max(6, 0.25 * cap) and sum(0.7 * md <= L <= 1.3 * md for L in lens) >= 0.8 * len(lens)
                if (sum(L <= dot for L in lens) >= 3 and len(dashes) >= 3) or regular:
                    for _, _, k in chain:
                        mark[k] = True
            chain = [r] if r is not None else []
    return mark[lab] & thin


def _line_pixels(dark, cap):
    """the pixels of long thin vertical and horizontal lines — extension lines, centre lines — except where a glyph stroke
    crosses them: a centre line through the 0 of a V-opening dimension would otherwise make the 0 part of the line"""
    L = max(12, int(round(1.4 * cap)))
    T = max(3, int(round(0.14 * cap)))
    vl, _ = ndimage.label(dark, structure=[[0, 1, 0], [0, 1, 0], [0, 1, 0]])
    hl, _ = ndimage.label(dark, structure=[[0, 0, 0], [1, 1, 1], [0, 0, 0]])
    vlen = np.bincount(vl.ravel())[vl]                  # how far each pixel's stroke runs down / across
    hlen = np.bincount(hl.ravel())[hl]
    lines = dark & (((vlen >= L) & (hlen <= T)) | ((hlen >= L) & (vlen <= T)))
    lines |= _dash_dot(dark, dark & (hlen <= T), cap)
    lines |= _dash_dot(dark.T, (dark & (vlen <= T)).T, cap).T
    return lines


def _orient(c):
    if c["h"] >= 1.22 * c["w"]:
        return "up"                                     # an upright digit is taller than wide
    if c["w"] >= 1.22 * c["h"]:
        return "lie"                                    # … and one turned 90° wider than tall
    return "slant"


def _linked(a, b, cap):
    """two glyphs of one run of text: upright glyphs side by side on one baseline, turned glyphs one above the other in
    one column, slanted glyphs close together.  Upright labels stacked diagonally (the scale grid) stay apart."""
    oa, ob = _orient(a), _orient(b)
    if oa == ob == "up":
        gap = max(a["x0"], b["x0"]) - min(a["x1"], b["x1"])
        return abs(a["cy"] - b["cy"]) <= 0.3 * cap and abs(a["h"] - b["h"]) <= 0.35 * cap and gap <= 0.6 * cap
    if oa == ob == "lie":
        gap = max(a["y0"], b["y0"]) - min(a["y1"], b["y1"])
        return abs(a["cx"] - b["cx"]) <= 0.3 * cap and abs(a["w"] - b["w"]) <= 0.35 * cap and gap <= 0.6 * cap
    if {oa, ob} == {"up", "lie"}:
        return False
    return math.hypot(a["cx"] - b["cx"], a["cy"] - b["cy"]) <= 1.3 * cap


def find_numbers(rgb, expect=None, grid_step=10, texts=None, thr=150):
    """the numbers of a drawing.  `texts`, a list, receives the box of every run of text found, read or not."""
    a = np.asarray(rgb).astype(np.int16)
    lum = a.mean(axis=2)
    dark = lum < thr
    lab, _ = ndimage.label(dark, structure=np.ones((3, 3)))
    cap = _cap(_components(lab))
    if not cap:
        return []
    lab, _ = ndimage.label(dark & ~_line_pixels(dark, cap), structure=np.ones((3, 3)))
    comps = _components(lab)
    cap2 = _cap(comps)
    if cap2 and abs(cap2 - cap) <= 0.25 * cap:          # freed from the lines they touched, the digits may show their size better;
        cap = cap2                                      # but line ends and hatching left behind must not set it
    glyphs = [c for c in comps if 0.5 * cap <= max(c["h"], c["w"]) <= 1.45 * cap and min(c["h"], c["w"]) >= 0.12 * cap
              and c["area"] > 0.1 * c["h"] * c["w"]]
    small = [c for c in comps if max(c["h"], c["w"]) < 0.45 * cap and c["area"] >= 3]
    # runs of text
    parent = list(range(len(glyphs)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i in range(len(glyphs)):
        for j in range(i + 1, len(glyphs)):
            gi, gj = glyphs[i], glyphs[j]
            if abs(gi["cx"] - gj["cx"]) <= 1.5 * cap and abs(gi["cy"] - gj["cy"]) <= 1.5 * cap and _linked(gi, gj, cap):
                parent[find(i)] = find(j)
    groups = {}
    for i in range(len(glyphs)):
        groups.setdefault(find(i), []).append(glyphs[i])
    if texts is not None:
        # every run of text — a lone blob only when it looks like a glyph: arrow tips and corners of the drawing are not text
        for G in groups.values():
            if len(G) == 1:
                g = G[0]
                m_ = lab[g["y0"]:g["y1"], g["x0"]:g["x1"]] == g["i"]
                if g["w"] > 1.15 * g["h"]:
                    m_ = np.asarray(Image.fromarray(m_.astype(np.uint8) * 255).rotate(-90, expand=True)) > 127
                if _classify(m_)[2] < 0.5:
                    continue
            texts.append((min(g["x0"] for g in G), min(g["y0"] for g in G), max(g["x1"] for g in G), max(g["y1"] for g in G)))
    out = []
    for G in groups.values():
        if len(G) > 6:
            continue
        if len(G) >= 2:                                 # text direction from the glyph centres
            xs = np.array([g["cx"] for g in G])
            ys = np.array([g["cy"] for g in G])
            ev, evec = np.linalg.eigh(np.cov(np.vstack([xs, ys])))
            dx, dy = evec[:, 1]
            ang = math.degrees(math.atan2(-dy, dx))      # counter-clockwise from +x (image y points down)
            if ang > 90:
                ang -= 180
            if ang <= -90:
                ang += 180
            if abs(ang) < 8:
                ang = 0.0
            elif abs(abs(ang) - 90) < 8:
                ang = 90.0                               # EUROSTAMP's vertical dimensions read bottom to top
        else:
            g = G[0]
            ang = 90.0 if g["w"] > 1.15 * g["h"] else 0.0
        x0, y0 = min(g["x0"] for g in G), min(g["y0"] for g in G)
        x1, y1 = max(g["x1"] for g in G), max(g["y1"] for g in G)
        ids = [g["i"] for g in G]
        # decimal commas: small blobs between the first and the last glyph along the line, close to it (they hang low)
        u0 = (math.cos(math.radians(ang)), -math.sin(math.radians(ang)))
        along_g = [g["cx"] * u0[0] + g["cy"] * u0[1] for g in G]
        base_n = np.mean([-g["cx"] * u0[1] + g["cy"] * u0[0] for g in G])
        seps = [c for c in small if min(along_g) < c["cx"] * u0[0] + c["cy"] * u0[1] < max(along_g)
                and abs((-c["cx"] * u0[1] + c["cy"] * u0[0]) - base_n) < 0.75 * cap]
        pad = max(4, cap // 3)
        X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(rgb.width, x1 + pad), min(rgb.height, y1 + pad)
        keep = np.isin(lab[Y0:Y1, X0:X1], ids + [c["i"] for c in seps])
        bw = Image.fromarray(np.where(keep, 0, 255).astype(np.uint8))
        if ang:
            bw = bw.rotate(-ang, expand=True, fillcolor=255)
        u = (math.cos(math.radians(ang)), -math.sin(math.radians(ang)))
        seq = sorted([("g", g["cx"] * u[0] + g["cy"] * u[1], g) for g in G] + [("s", c["cx"] * u[0] + c["cy"] * u[1], c) for c in seps],
                     key=lambda e: e[1])
        n_g = len(G)
        # a small blob just past the last glyph and above the baseline: a degree sign — angles get no inch value
        end = max(along_g)
        if any(end < c["cx"] * u0[0] + c["cy"] * u0[1] < end + 1.1 * cap
               and base_n - 0.8 * cap < (-c["cx"] * u0[1] + c["cy"] * u0[0]) < base_n - 0.2 * cap for c in small):
            continue
        txt, weak, low, low_score = "", False, 9.0, 9.0
        for kd, _, g in seq:
            if kd != "g":
                continue
            m_ = (lab[g["y0"]:g["y1"], g["x0"]:g["x1"]] == g["i"])
            if ang:
                m_ = np.asarray(Image.fromarray(m_.astype(np.uint8) * 255).rotate(-ang, expand=True)) > 127
            ch, margin, score = _classify(m_)
            weak |= margin < 0.04 or score < 0.45
            low = min(low, margin)
            low_score = min(low_score, score)
            txt += ch or "?"
        if n_g == 1 and (txt == "1" or low < 0.1 or low_score < 0.5):
            continue                                      # a lone bar or an unsure lone glyph: an arrow tip as often as a 1
        if not re.fullmatch(r"[RØ]?\d+", txt) or weak:
            reads = _ocr(bw)                              # an unsure glyph: ask Tesseract, use it only if it agrees on the count
            alt = next((r for r in reads if re.fullmatch(r"R?\d+", r) and len(r) == n_g), None)
            if alt is None or not re.fullmatch(r"[RØ]?\d+", txt):
                txt = alt
            if txt is None:
                continue
        chars, k = [], 0
        for kind, _, obj in seq:
            if kind == "g":
                chars.append(txt[k])
                k += 1
            elif chars and chars[-1].isdigit() and k < n_g:
                chars.append(",")                          # a small blob between two digits: the decimal comma
        s = "".join(chars)
        if re.fullmatch(r"[RØ]?0\d+", s):                     # 06 cannot be a length in mm: the comma was too faint to see
            i0 = 2 if s[0] in "RØ" else 1
            s = s[:i0] + "," + s[i0:]
        m = re.fullmatch(r"([RØ])?(\d+(?:,\d+)?)", s)
        if not m:
            continue
        v = float(m.group(2).replace(",", "."))
        px = a[y0:y1, x0:x1][np.isin(lab[y0:y1, x0:x1], ids)]
        col = tuple(int(c) for c in px.mean(axis=0)) if len(px) else (60, 60, 60)
        kind = "dim" if (col[2] - col[0] > 8) else "grid"
        out.append({"text": s, "value": v, "is_r": bool(m.group(1)), "prefix": m.group(1) or "", "box": (x0, y0, x1, y1), "angle": ang,
                    "cap": cap, "color": col, "kind": kind, "n": n_g, "_glyphs": [obj for kd, _, obj in seq if kd == "g"]})
    # black numbers are scale-grid labels only when the drawing has a grid: round black numbers standing in evenly
    # spaced rows; in a drawing printed all in black they are its dimensions.  A round black number that fits no row of
    # a grid drawing is dropped (a grid label misread, most likely), any other black number is a dimension.
    round_ = [N for N in out if N["kind"] == "grid" and N["value"] % grid_step == 0 and N["value"] <= 600]
    rows = _grid_checked(round_)
    if len(rows) < 3:
        for N in out:
            N["kind"] = "dim"
    else:
        keep = {id(N) for N in rows}
        out = [N for N in out if not (N["kind"] == "grid" and id(N) not in keep and N in round_)]
        for N in out:
            if N["kind"] == "grid" and id(N) not in keep:
                N["kind"] = "dim"
    # a lone glyph on the baseline of other text close by is a piece of a longer number whose other glyphs touch a line
    if texts is not None:
        keep = []
        for N in out:
            if N["n"] == 1 and not N["is_r"]:
                x0, y0, x1, y1 = N["box"]
                vert = N["angle"] == 90
                near = False
                for B in texts:
                    if tuple(B) == (x0, y0, x1, y1):
                        continue
                    if not vert and abs((B[1] + B[3]) / 2 - (y0 + y1) / 2) < 0.25 * cap \
                            and max(B[0], x0) - min(B[2], x1) < 2.2 * cap:
                        near = True
                    if vert and abs((B[0] + B[2]) / 2 - (x0 + x1) / 2) < 0.25 * cap \
                            and max(B[1], y0) - min(B[3], y1) < 2.2 * cap:
                        near = True
                if near:
                    continue
            keep.append(N)
        out = keep
    trusted = []
    for N in out:
        if N["kind"] == "dim":
            if expect is not None and not any(abs(N["value"] - e) < 1e-6 for e in expect):
                # a comma the drawing has but the reading lost (65 → 6,5): only where the two digits stand a comma's width
                # apart — '1,75' whose 1 merged with a leader line reads 75, and must not become 7,5 — and only when
                # exactly one placing of the comma is expected
                digits = re.sub(r"\D", "", N["text"])
                if "," in N["text"] or len(N.get("_glyphs") or []) != len(N["text"]):
                    continue
                gl = N["_glyphs"][len(N["prefix"]):]
                u = (math.cos(math.radians(N["angle"])), -math.sin(math.radians(N["angle"])))

                def gap_after(i):
                    a, b = gl[i - 1], gl[i]
                    ea = max(a["x0"] * u[0] + a["y0"] * u[1], a["x1"] * u[0] + a["y1"] * u[1], a["x0"] * u[0] + a["y1"] * u[1],
                             a["x1"] * u[0] + a["y0"] * u[1])
                    sb = min(b["x0"] * u[0] + b["y0"] * u[1], b["x1"] * u[0] + b["y1"] * u[1], b["x0"] * u[0] + b["y1"] * u[1],
                             b["x1"] * u[0] + b["y0"] * u[1])
                    return sb - ea
                hit = {float(digits[:i] + "." + digits[i:]) for i in range(1, len(digits)) if gap_after(i) >= 0.22 * N["cap"]}
                hit = [x for x in hit if any(abs(x - e) < 1e-6 for e in expect)]
                if len(hit) != 1:
                    continue
                N["value"], N["fixed"] = hit[0], True
                N["text"] = N["prefix"] + f"{hit[0]:g}".replace(".", ",")
            trusted.append(N)
        else:
            trusted.append(N)
    return trusted


def _bitmap(lab, objs, i, ang):
    sl = objs[i - 1]
    m = (lab[sl] == i).astype(np.uint8) * 255
    im = Image.fromarray(m)
    if ang:
        im = im.rotate(-ang, expand=True)
    v = np.asarray(im.resize((18, 26), Image.BILINEAR), np.float32) / 255
    v -= v.mean()
    return v / (np.linalg.norm(v) + 1e-6)


def _verify_grid(nums, lab, objs):
    """Tesseract now and then reads a 5 as a 9.  The scale-grid labels repeat the same few digits many times in one font:
    each glyph is matched against the average of every other glyph read as the same digit (leave-one-out), and a clearly
    better match with another digit replaces the reading"""
    data = []
    for N in nums:
        if N["kind"] != "grid" or N["is_r"] or "," in N["text"]:
            continue
        gl = N.get("_glyphs") or []
        if len(gl) != len(N["text"]):
            continue
        data.append((N, list(N["text"]), [_bitmap(lab, objs, g["i"], N["angle"]) for g in gl]))
    for _ in range(2):
        sums, cnt = {}, {}
        for N, chars, bms in data:
            for ch, b in zip(chars, bms):
                sums[ch] = sums.get(ch, 0) + b
                cnt[ch] = cnt.get(ch, 0) + 1
        if len(sums) < 3:
            return
        changed = False
        for N, chars, bms in data:
            for k, (ch, b) in enumerate(zip(chars, bms)):
                scores = {}
                for c in sums:
                    if c == ch:
                        if cnt[c] < 2:
                            continue
                        t = (sums[c] - b) / (cnt[c] - 1)
                    else:
                        if cnt[c] < 2:
                            continue
                        t = sums[c] / cnt[c]
                    scores[c] = float((b * t).sum() / (np.linalg.norm(t) + 1e-6))
                if not scores:
                    continue
                best = max(scores, key=scores.get)
                if best != ch and (ch not in scores or scores[best] > scores[ch] + 0.06):
                    chars[k] = best
                    changed = True
            t = "".join(chars)
            if t != N["text"]:
                N["text"], N["value"], N["fixed"] = t, float(t), True
        if not changed:
            break


class Paper:
    def __init__(self, rgb, f=1):
        """the ink of `rgb`; with f > 1, of `rgb` drawn f times larger (pixel for pixel: an enlarged picture's ringing
        round each line is not ink)"""
        g = np.asarray(rgb.convert("L"))
        self.m = g < 236
        self.md = g < 165
        if f > 1:
            self.m = np.repeat(np.repeat(self.m, f, axis=0), f, axis=1)
            self.md = np.repeat(np.repeat(self.md, f, axis=0), f, axis=1)
        self.h, self.w = self.m.shape

    def clear(self, box, ignore=None, pad=2, dark_only=False):
        x0, y0, x1, y1 = [int(round(v)) for v in box]
        x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
        if x0 < 4 or y0 < 4 or x1 > self.w - 4 or y1 > self.h - 4:
            return False
        sub = (self.md if dark_only else self.m)[y0:y1, x0:x1]
        if ignore is not None and sub.any():
            sub = sub.copy()
            ix0, iy0, ix1, iy1 = ignore
            sub[max(0, iy0 - y0):max(0, iy1 - y0), max(0, ix0 - x0):max(0, ix1 - x0)] = False
        return not sub.any()

    def clear_pixels(self, px, py, alpha, ignore=None, dark_only=False, grow=3):
        """True when no ink lies under the text's own pixels (grown by `grow`) at (px, py) — exact for slanted text"""
        x0, y0 = int(round(px)), int(round(py))
        h, w = alpha.shape
        if x0 < 4 or y0 < 4 or x0 + w > self.w - 4 or y0 + h > self.h - 4:
            return False
        sub = (self.md if dark_only else self.m)[y0:y0 + h, x0:x0 + w].copy()
        if ignore is not None:
            ix0, iy0, ix1, iy1 = ignore
            sub[max(0, iy0 - y0):max(0, iy1 - y0), max(0, ix0 - x0):max(0, ix1 - x0)] = False
        a = ndimage.binary_dilation(alpha > 40, iterations=grow)
        return not (sub & a).any()

    def take_pixels(self, px, py, alpha, grow=4):
        x0, y0 = int(round(px)), int(round(py))
        h, w = alpha.shape
        a = ndimage.binary_dilation(alpha > 40, iterations=grow)
        for m in (self.m, self.md):
            m[y0:y0 + h, x0:x0 + w] |= a

    def take(self, box, pad=3):
        x0, y0, x1, y1 = [int(round(v)) for v in box]
        for m in (self.m, self.md):
            m[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad] = True


def _text_img(txt, font, color, ang):
    l, t, r, b = font.getbbox(txt)
    im = Image.new("RGBA", (r - l + 2, b - t + 2), (255, 255, 255, 0))
    ImageDraw.Draw(im).text((1 - l, 1 - t), txt, font=font, fill=tuple(color) + (255,))
    if ang:
        im = im.rotate(ang, expand=True, resample=Image.BICUBIC)
    return im


ORDER = {"dim": ["after", "above", "below", "after>", "before", "before<"],
         "grid": ["below", "above", "after", "before", "after>", "before<"]}


def _spots(N, tw, th):
    x0, y0, x1, y1 = N["box"]
    gap = max(3, int(0.3 * N["cap"]))
    far = range(2, max(4, int(N["cap"])) + 1, 2)          # a little further on, past an arrow tip or a line end — never far
    ang = N["angle"]
    if ang == 0:
        cy = (y0 + y1) / 2
        return {"after": [(x1 + gap, cy - th / 2)], "before": [(x0 - gap - tw, cy - th / 2)],
                "above": [((x0 + x1 - tw) / 2, y0 - gap - th)], "below": [((x0 + x1 - tw) / 2, y1 + gap)],
                "after>": [(x1 + gap + k, cy - th / 2) for k in far],
                "before<": [(x0 - gap - tw - k, cy - th / 2) for k in far]}
    if ang == 90:                                      # running upward: 'after' is above it, 'above' is to its left
        cx = (x0 + x1) / 2
        return {"after": [(cx - tw / 2, y0 - gap - th)], "before": [(cx - tw / 2, y1 + gap)],
                "above": [(x0 - gap - tw, (y0 + y1 - th) / 2)], "below": [(x1 + gap, (y0 + y1 - th) / 2)],
                "after>": [(cx - tw / 2, y0 - gap - th - k) for k in far],
                "before<": [(cx - tw / 2, y1 + gap + k) for k in far]}
    # slanted text: along its own direction only
    u = (math.cos(math.radians(ang)), -math.sin(math.radians(ang)))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    run = abs(u[0]) * (x1 - x0) + abs(u[1]) * (y1 - y0)
    w_ext = abs(u[0]) * tw + abs(u[1]) * th
    out = {"above": [], "below": []}
    for name, sgn, ks in (("after", 1, [0]), ("after>", 1, far), ("before", -1, [0]), ("before<", -1, far)):
        out[name] = []
        for k in ks:
            d = 0.5 * run * 0.8 + gap + 0.15 * N["cap"] + k + 0.5 * w_ext * 0.8
            px, py = cx + sgn * u[0] * d, cy + sgn * u[1] * d
            out[name].append((px - tw / 2, py - th / 2))
    return out


def _gap(a, b):
    """the distance between two boxes, 0 when they overlap"""
    dx = max(0, max(a[0], b[0]) - min(a[2], b[2]))
    dy = max(0, max(a[1], b[1]) - min(a[3], b[3]))
    return math.hypot(dx, dy)


def _reads_as_own(R, own, others, N):
    """True when text at R reads as belonging to the number at `own`: next to it on its line (and no other number
    nearer on that line), or else clearly nearer to it than to any other number"""
    cap = N["cap"]
    ax = 1 if N["angle"] == 90 else 0                       # the axis across the line of text: y for level text, x for upright
    lo, hi = (1, 3) if ax == 0 else (0, 2)

    def across_overlap(A, B):
        return min(A[hi], B[hi]) - max(A[lo], B[lo])
    d_own = _gap(R, own)
    if N["angle"] in (0, 90) and across_overlap(R, own) >= 0.6 * min(R[hi] - R[lo], own[hi] - own[lo]):
        for B in others:
            d = _gap(R, B)
            if d < d_own + 0.1 * cap and across_overlap(R, B) > 0.3 * min(R[hi] - R[lo], B[hi] - B[lo]):
                return False                                # another number on the same line, as near
            if d < 0.5 * d_own:
                return False
        return True
    return all(_gap(R, B) >= d_own + 0.15 * cap for B in others)


def _fit(N, paper, texts, dark_only, scales, grow=3):
    """the first free spot for N's inch value that reads as N's: (text image, x, y) or None.  A spot nearer to another
    number than to N would be read as that number's inch value, so it is not used."""
    extra = f"({inch(N['value'], 2 if N['kind'] == 'grid' else None)})"
    own = tuple(N["box"])
    others = [B for B in texts if tuple(B) != own]
    for scale in scales:
        font = ImageFont.truetype(FONT_PATH, max(8, int(round(N["cap"] / 0.711 * scale))))
        tim = _text_img(extra, font, N["color"], N["angle"])
        tw, th = tim.size
        sp = _spots(N, tw, th)
        alpha = np.asarray(tim.getchannel("A"))
        for spot in ORDER[N["kind"]]:
            for (px, py) in sp.get(spot, []):
                R = (px, py, px + tw, py + th)
                if not _reads_as_own(R, own, others, N):
                    continue
                if paper.clear_pixels(px, py, alpha, ignore=own, dark_only=dark_only, grow=grow):
                    return tim, px, py, alpha
    return None


def _grid_checked(grid):
    """the scale-grid labels whose value fits their row: the labels stand evenly spaced along the edges of the grid, so
    each one is the mean of its two neighbours on either side, or one step on from a neighbour that is.  A grey 2 read
    as a 9 fits nowhere and is dropped."""
    if len(grid) < 3:
        return []
    cen = [((N["box"][0] + N["box"][2]) / 2, (N["box"][1] + N["box"][3]) / 2) for N in grid]
    near = []
    for i, c in enumerate(cen):
        d = sorted((math.hypot(c[0] - e[0], c[1] - e[1]), j) for j, e in enumerate(cen) if j != i)
        near.append(d[0][0] if d else 0)
    s = float(np.median(near))
    nb = {i: [j for j, e in enumerate(cen) if j != i and 0.6 * s <= math.hypot(cen[i][0] - e[0], cen[i][1] - e[1]) <= 1.7 * s]
          for i in range(len(grid))}

    def opposite(i, j, k):
        a = (cen[j][0] - cen[i][0], cen[j][1] - cen[i][1])
        b = (cen[k][0] - cen[i][0], cen[k][1] - cen[i][1])
        la, lb = math.hypot(*a), math.hypot(*b)
        return la and lb and (a[0] * b[0] + a[1] * b[1]) / (la * lb) < -0.87 and 0.7 <= la / lb <= 1.4
    v = [N["value"] for N in grid]
    ok = set()
    for i in range(len(grid)):
        for j in nb[i]:
            for k in nb[i]:
                if j < k and opposite(i, j, k) and abs(v[j] + v[k] - 2 * v[i]) < 1e-6 and v[j] != v[k]:
                    ok.add(i)
    changed = True
    while changed:
        changed = False
        for i in range(len(grid)):
            if i in ok:
                continue
            for j in nb[i]:
                if j not in ok:
                    continue
                for k in nb[j]:                         # i, j, k in a row, j and k checked: i is one more step
                    if k in ok and k != i and opposite(j, i, k) and abs(v[i] - (2 * v[j] - v[k])) < 1e-6 and v[j] != v[k]:
                        ok.add(i)
                        changed = True
                        break
                if i in ok:
                    break
    return [grid[i] for i in sorted(ok)]


def _overlap(a, b):
    ix = min(a[2], b[2]) - max(a[0], b[0])
    iy = min(a[3], b[3]) - max(a[1], b[1])
    if ix <= 0 or iy <= 0:
        return 0.0
    return ix * iy / min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))


def find_twice(rgb, expect=None, grid_step=10):
    """small lettering, read twice — as drawn, and at twice the size at a lighter threshold (thin grey strokes) — in the
    coordinates of the drawing at twice the size: (numbers, text boxes)"""
    rgb = rgb.convert("RGB")
    big = rgb.resize((rgb.width * 2, rgb.height * 2), Image.LANCZOS)
    t1, t2 = [], []
    n1 = find_numbers(rgb, expect=expect, grid_step=grid_step, texts=t1)
    n2 = find_numbers(big, expect=expect, grid_step=grid_step, texts=t2, thr=185)
    nums = list(n2)
    for N in n1:
        N = dict(N, box=tuple(2 * v for v in N["box"]), cap=2 * N["cap"])
        if not any(_overlap(N["box"], M["box"]) > 0.3 for M in nums):
            nums.append(N)
    texts = list(t2) + [tuple(2 * v for v in B) for B in t1 if not any(_overlap(tuple(2 * v for v in B), C) > 0.3 for C in t2)]
    return nums, texts


def annotate(rgb, expect=None, grid_step=10, thr=150, found=None, small=None):
    """write the inch values onto a copy of `rgb`; returns (image, not-placed list, numbers found).  `found`: the
    (numbers, text boxes) of the drawing when read already (find_twice); `small`: the drawing at half the size of `rgb`,
    whose ink tells where the paper is free"""
    rgb = rgb.convert("RGB")
    if found:
        nums, texts = found
    else:
        texts = []
        nums = find_numbers(rgb, expect=expect, grid_step=grid_step, texts=texts, thr=thr)
    out = rgb.copy()
    paper = Paper(small, 2) if small is not None else Paper(rgb)
    report = []
    # dimensions first, the longest numbers first; a second pass may write over the light grey of a tool body
    todo = sorted([N for N in nums if N["value"] != 0 and N["kind"] == "dim"], key=lambda N: -N["n"])
    for dark_only in (False, True):
        left = []
        for N in todo:
            hit = _fit(N, paper, texts, dark_only, (0.84, 0.7))
            if hit:
                tim, px, py, alpha = hit
                out.paste(tim, (int(round(px)), int(round(py))), tim)
                paper.take_pixels(px, py, alpha)
            else:
                left.append(N)
        todo = left
    report += [N["text"] for N in todo]
    # the scale grid, all in one size and packed a little closer: every label, else every other one (20, 40, 60 …), else
    # every 50 — and when not even those fit, none, rather than a grid with inch values here and there
    grid = [N for N in _grid_checked([N for N in nums if N["kind"] == "grid"]) if N["value"] != 0]
    tiers = [grid, [N for N in grid if N["value"] % (2 * grid_step) == 0], [N for N in grid if N["value"] % 50 == 0]]
    chosen = None
    for tier in tiers:
        if len(tier) < 3:
            continue
        trial = Paper.__new__(Paper)
        trial.m, trial.md, trial.h, trial.w = paper.m.copy(), paper.md.copy(), paper.h, paper.w
        done = []
        for N in sorted(tier, key=lambda N: -N["value"]):
            hit = _fit(N, trial, texts, False, (0.7,), grow=2)
            if hit:
                trial.take_pixels(hit[1], hit[2], hit[3], grow=2)
                done.append(hit)
        if len(done) >= 0.85 * len(tier):
            chosen = (tier, done, trial)
            break
    if chosen:
        tier, done, paper = chosen
        for tim, px, py, alpha in done:
            out.paste(tim, (int(round(px)), int(round(py))), tim)
        report += [f"grid: {len(done)} of {len(tier)} (of {len(grid)})"]
    elif grid:
        report += [f"grid: none of {len(grid)}"]
    return out, report, nums


if __name__ == "__main__":
    exp = {float(x.replace(",", ".")) for x in sys.argv[3].split(";")} if len(sys.argv) > 3 else None
    out, rep, nums = annotate(on_white(Image.open(sys.argv[1])), expect=exp)
    out.save(sys.argv[2])
    print(len(nums), "numbers:", " ".join(f"{n['text']}@{n['angle']:.0f}/{n['kind'][0]}{'*' if n.get('fixed') else ''}" for n in nums))
    print("not placed:", rep)
