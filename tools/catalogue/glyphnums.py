"""Numbers that are drawn, not typed: some drawings carry their dimensions as outlined glyphs (filled vector paths), which
no text extraction sees.  The small filled paths of a page are grouped into words, each word is drawn alone (black on
white, nothing touching it) and read with Tesseract along its own direction — across, up the page, or slanted like the
'R 25' of a 45° radius.  Only words that read as a plain number ('67', '2.5', 'R 25') are kept.

found(page) → [{"text", "value", "prefix", "origin", "u", "v", "adv", "size", "color", "rect"}]   (page coordinates, y down;
u = baseline direction, v = the glyphs' up direction)
"""
import math
import os
import re
import subprocess
import tempfile

import cv2
import fitz
import numpy as np

Z = 10.0                                         # px per pt for the OCR renders
NUM_RE = re.compile(r"^(R\s?)?(\d{1,4}(?:[.,]\d{1,3})?)$")


def _is_white(c):
    return c is not None and min(c[:3]) > 0.9


def glyph_paths(page):
    """filled paths the size of a glyph (not white): candidates for outlined characters"""
    out = []
    for d in page.get_drawings():
        f = d.get("fill")
        if not f or _is_white(f) or d.get("type") not in ("f", "fs"):
            continue
        R = d["rect"]
        big, small = max(R.width, R.height), min(R.width, R.height)
        if not (1.2 <= big <= 11.5 and small >= 0.25):
            continue
        out.append(d)
    return out


def has_outlined_text(page):
    """True when the page has outlined characters (several glyph-like paths with curves) that are not white"""
    n = 0
    for d in glyph_paths(page):
        items = d["items"]
        if len(items) >= 8 and sum(1 for it in items if it[0] == "c") >= 3:
            n += 1
    return n >= 1


def words(paths):
    """group glyph paths into words: bboxes closer than 0.55 × the larger glyph's height, chained"""
    rects = [d["rect"] for d in paths]
    n = len(rects)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for i in range(n):
        for j in range(i + 1, n):
            a, b = rects[i], rects[j]
            h = max(max(a.width, a.height), max(b.width, b.height))
            ha, hb = max(a.width, a.height), max(b.width, b.height)
            if min(ha, hb) < 0.35 * max(ha, hb) and min(ha, hb) > 1.6:
                continue                                  # very different sizes: not one word (a '.' is small but tiny)
            gx = max(0.0, max(a.x0, b.x0) - min(a.x1, b.x1))
            gy = max(0.0, max(a.y0, b.y0) - min(a.y1, b.y1))
            if math.hypot(gx, gy) < 0.55 * h:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(paths[i])
    return list(groups.values())


def _draw(page, ds):
    for d in ds:
        sh = page.new_shape()
        for it in d["items"]:
            k = it[0]
            if k == "l":
                sh.draw_line(it[1], it[2])
            elif k == "re":
                sh.draw_rect(it[1])
            elif k == "qu":
                sh.draw_quad(it[1])
            elif k == "c":
                sh.draw_bezier(it[1], it[2], it[3], it[4])
        sh.finish(color=None, fill=(0, 0, 0), even_odd=bool(d.get("even_odd")), closePath=True, width=0)
        sh.commit()


def render_word(ds, pad=3.0):
    """the word's paths alone, black on white: (gray image, page rect it covers)"""
    R = fitz.Rect(ds[0]["rect"])
    for d in ds:
        R |= d["rect"]
    R = fitz.Rect(R.x0 - pad, R.y0 - pad, R.x1 + pad, R.y1 + pad)
    doc = fitz.open()
    p = doc.new_page(width=max(R.x1 + 5, 50), height=max(R.y1 + 5, 50))
    _draw(p, ds)
    pix = p.get_pixmap(matrix=fitz.Matrix(Z, Z), clip=R, colorspace=fitz.csGRAY, alpha=False)
    img = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width).copy()
    return img, R


def ocr(img, whitelist=None):
    img = cv2.copyMakeBorder(img, 24, 24, 24, 24, cv2.BORDER_CONSTANT, value=255)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "w.png")
        cv2.imwrite(p, img)
        cmd = ["tesseract", p, "stdout", "--psm", "7"]
        if whitelist:
            cmd += ["-c", f"tessedit_char_whitelist={whitelist}"]
        r = subprocess.run(cmd + ["tsv"], capture_output=True, text=True)
    toks, conf = [], 100.0
    for line in r.stdout.splitlines()[1:]:
        q = line.split("\t")
        if len(q) == 12 and q[11].strip():
            toks.append(q[11].strip())
            conf = min(conf, float(q[10]))
    return (" ".join(toks), conf) if toks else (None, 0.0)


def rotate(img, deg):
    """rotate counter-clockwise by deg, canvas grown to fit, white ground"""
    h, w = img.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), deg, 1.0)
    c, s = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * s + w * c), int(h * c + w * s)
    M[0, 2] += nw / 2 - w / 2
    M[1, 2] += nh / 2 - h / 2
    return cv2.warpAffine(img, M, (nw, nh), flags=cv2.INTER_LINEAR, borderValue=255)


def _axis(ds):
    """direction of the word's glyph centres (unit vector, x right / y down), or None for a single glyph"""
    pts = np.array([[(d["rect"].x0 + d["rect"].x1) / 2, (d["rect"].y0 + d["rect"].y1) / 2] for d in ds])
    if len(pts) < 2:
        return None
    pts = pts - pts.mean(axis=0)
    _, _, vt = np.linalg.svd(pts)
    ux, uy = vt[0]
    if ux < -1e-6 or (abs(ux) < 1e-6 and uy > 0):
        ux, uy = -ux, -uy                              # read left to right, or bottom to top
    return ux, uy


# ------------------------------------------------------------------------------------------------ glyph templates
TPL_FONTS = [os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", "roboto", f"Roboto-{s}.ttf")
             for s in ("Light", "Regular", "Medium", "Bold", "Italic", "LightItalic")] + [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"]
TPL_CHARS = "0123456789R"
NORM = 40
_TPL = []


def _norm(ink):
    """a binary glyph image cropped to its ink, scaled to NORM px high and centred in a NORM × NORM square; (img, w/h)"""
    ys, xs = np.nonzero(ink)
    if len(xs) == 0:
        return None, 0.0
    g = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.uint8) * 255
    h, w = g.shape
    ar = w / h
    nw = max(1, min(NORM, int(round(NORM * ar))))
    g = cv2.resize(g, (nw, NORM), interpolation=cv2.INTER_AREA)
    out = np.zeros((NORM, NORM), np.uint8)
    x0 = (NORM - nw) // 2
    out[:, x0:x0 + nw] = g
    return cv2.GaussianBlur(out, (5, 5), 0).astype(np.float32) / 255.0, ar


def templates():
    if _TPL:
        return _TPL
    for path in TPL_FONTS:
        if not os.path.exists(path):
            continue
        fo = fitz.Font(fontfile=path)
        for ch in TPL_CHARS:
            doc = fitz.open()
            p = doc.new_page(width=200, height=200)
            tw = fitz.TextWriter(p.rect)
            tw.append((40, 150), ch, font=fo, fontsize=120)
            tw.write_text(p)
            pix = p.get_pixmap(colorspace=fitz.csGRAY, alpha=False)
            img = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width) < 128
            n, ar = _norm(img)
            if n is not None:
                _TPL.append((ch, n, ar))
    return _TPL


def classify(ink):
    """(char, score) for one glyph image (True = ink), the best template by correlation, aspect ratio counted"""
    n, ar = _norm(ink)
    if n is None:
        return None, 0.0
    best = {}
    for ch, t, tar in templates():
        num = float((n * t).sum())
        den = math.sqrt(float((n * n).sum()) * float((t * t).sum())) or 1.0
        sc = num / den * (1.0 - min(0.5, abs(ar - tar) / max(ar, tar)))
        if sc > best.get(ch, 0.0):
            best[ch] = sc
    ranked = sorted(best.items(), key=lambda kv: -kv[1])
    if not ranked:
        return None, 0.0
    (c1, s1), (c2, s2) = ranked[0], (ranked[1] if len(ranked) > 1 else ("", 0.0))
    return c1, s1 - 0.5 * max(0.0, s2 - (s1 - 0.08))      # a near tie lowers the score


def _glyph_ink(d, deg):
    """one glyph path drawn alone, turned upright (deg: the word's angle, counter-clockwise), as a boolean image"""
    img, _ = render_word([d], pad=2.0)
    if deg:
        img = rotate(img, -deg)
    return img < 128


def read_by_shape(ds, deg, u):
    """the word read glyph by glyph against the font templates: (text, score) or None"""
    # reading order: along u
    def along(d):
        r = d["rect"]
        return ((r.x0 + r.x1) / 2) * u[0] + ((r.y0 + r.y1) / 2) * u[1]
    ds = sorted(ds, key=along)
    hs = []
    for d in ds:
        r = d["rect"]
        hs.append(abs(r.width * u[1]) + abs(r.height * u[0]) if abs(u[0]) > 0.99 or abs(u[1]) > 0.99 else max(r.width, r.height))
    H = max(hs)
    out, low = "", 1.0
    for d, h in zip(ds, hs):
        if h < 0.4 * H:
            out += "."                                   # a decimal point (or comma) between the digits
            continue
        ch, sc = classify(_glyph_ink(d, deg))
        if ch is None or sc < 0.80:
            return None
        out += ch
        low = min(low, sc)
    return out, low


def read_word(ds):
    """(text, conf, u, v) of a word of outlined glyphs, or None"""
    ds = [d for d in ds if len(d["items"]) >= 4                      # arrowheads (two or three segments) and
          and min(d["rect"].width, d["rect"].height) > 0.15 * max(d["rect"].width, d["rect"].height)]   # thin marks
    if not ds:
        return None
    ax = _axis(ds)
    if ax is None:
        r = ds[0]["rect"]
        tries = [(90, (0.0, -1.0))] if r.width > r.height * 1.15 else [(0, (1.0, 0.0))]
    else:
        ang = math.degrees(math.atan2(-ax[1], ax[0]))
        if abs(ang) < 8:
            tries = [(0, (1.0, 0.0))]
        elif abs(abs(ang) - 90) < 8:
            tries = [(90, (0.0, -1.0))]
        else:
            tries = [(ang, (ax[0], ax[1]))]
    for deg, u in tries:
        res = read_by_shape(ds, deg, u)
        if not res:
            continue
        t, sc = res
        t = t.strip(".")
        if NUM_RE.match(t) and t.count(".") <= 1:
            n = math.hypot(*u)
            u = (float(u[0] / n), float(u[1] / n))
            return t, round(sc * 100, 1), u, (u[1], -u[0]), ds
    return None


def read_word_tesseract(ds):
    """(text, conf, u, v) of a word of outlined glyphs, or None"""
    img, R = render_word(ds)
    ax = _axis(ds)
    tries = []
    if ax is None:
        r = ds[0]["rect"]
        if r.width > r.height * 1.15:                  # a digit lying on its side: up the page
            tries = [(90, (0.0, -1.0)), (-90, (0.0, 1.0))]
        else:
            tries = [(0, (1.0, 0.0))]
    else:
        ang = math.degrees(math.atan2(-ax[1], ax[0]))  # counter-clockwise from the x axis, y up
        if abs(ang) < 8:
            tries = [(0, (1.0, 0.0))]
        elif abs(abs(ang) - 90) < 8:
            tries = [(90, (0.0, -1.0)), (-90, (0.0, 1.0))]
        else:
            tries = [(ang, (ax[0], ax[1]))]
    for deg, u in tries:
        im = rotate(img, -deg) if deg else img
        t, conf = ocr(im)
        if not t:
            continue
        t2 = t.replace(" ", "").replace("O", "0").replace("o", "0")
        if not NUM_RE.match(t2):
            continue                                    # not a number (a word, 'kg', '2x150' …)
        tw, cw = ocr(im, "0123456789R.,")
        if tw and tw.replace(" ", "") == t2 and min(conf, cw) >= 70:
            n = math.hypot(*u)
            u = (u[0] / n, u[1] / n)
            return t2, min(conf, cw), u, (u[1], -u[0])
    return None


def found(page):
    out = []
    paths = [d for d in glyph_paths(page) if len(d["items"]) >= 4]     # not the arrowheads
    for ds in words(paths):
        if len(ds) > 7:
            continue
        col = ds[0].get("fill")
        if col and max(col[:3]) < 0.35 and max(col[:3]) - min(col[:3]) < 0.08:
            continue                                    # black outlines are weights ('3,5 kg'), not dimensions
        res = read_word(ds)
        if not res:
            continue
        t, conf, u, v, ds = res
        m = NUM_RE.match(t)
        val = float(m.group(2).replace(",", "."))
        # extent along u and v
        pts = []
        for d in ds:
            r = d["rect"]
            pts += [(r.x0, r.y0), (r.x1, r.y0), (r.x0, r.y1), (r.x1, r.y1)]
        al = [x * u[0] + y * u[1] for x, y in pts]
        up = [x * v[0] + y * v[1] for x, y in pts]
        a0, a1, b0, b1 = min(al), max(al), min(up), max(up)
        size = (b1 - b0) / 0.72
        o = fitz.Point(a0 * u[0] + b0 * v[0], a0 * u[1] + b0 * v[1])
        R = fitz.Rect(ds[0]["rect"])
        for d in ds:
            R |= d["rect"]
        out.append({"text": t, "value": val, "prefix": m.group(1) or "", "origin": o, "u": u, "v": v, "adv": a1 - a0,
                    "size": size, "conf": conf, "rect": R,
                    "color": int(col[0] * 255) << 16 | int(col[1] * 255) << 8 | int(col[2] * 255)})
    return out


if __name__ == "__main__":
    import sys
    doc = fitz.open("/home/claude/eurostamp/pdf/cat.pdf")
    for a in sys.argv[1:]:
        p = int(a)
        pg = doc[p - 1]
        print(p, "outlined:", has_outlined_text(pg))
        for f in found(pg):
            print("  ", f["text"], round(f["conf"]), f["rect"], tuple(round(x, 2) for x in f["u"]), round(f["size"], 1), hex(f["color"]))
