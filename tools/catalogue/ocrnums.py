"""Numbers that are drawn, not typed: some drawings carry their dimensions as outlined glyphs (vector shapes), which no
text extraction sees.  The page's graphics (its text taken out) are rendered, small glyph-sized shapes are grouped into
words (across, or up the page for vertical dimensions), and each word is read with Tesseract in its orientation.

found(page) → [{"text", "value", "rect" (page pt), "u", "v", "size"}]
"""
import re
import subprocess
import tempfile
import os

import cv2
import fitz
import numpy as np

Z = 8.0                                         # px per pt
NUM_RE = re.compile(r"^(R\s?)?(\d{1,4}(?:[.,]\d{1,2})?)$")


def graphics_render(page):
    tmp = fitz.open()
    tmp.insert_pdf(page.parent, from_page=page.number, to_page=page.number)
    tp = tmp[0]
    tp.add_redact_annot(tp.rect, fill=False)
    tp.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE, graphics=0, text=0)
    pix = tp.get_pixmap(matrix=fitz.Matrix(Z, Z), alpha=False)
    rgb = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3)
    return rgb


def components(rgb):
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    ink = (g < 150).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(ink, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        hp, wp = h / Z, w / Z
        long_side, short_side = max(hp, wp), min(hp, wp)
        if not (2.2 <= long_side <= 9.0 and 0.25 <= short_side <= 7.5):
            continue
        if a / float(w * h) > 0.85 and short_side > 1.0:      # solid blobs (arrowheads are triangles ~0.5)
            continue
        out.append((x, y, w, h, i))
    return out, lab


def words(comps, vertical=False):
    """chain glyph boxes into words: same line (centre within ±25 % of height), gaps under 0.7 heights"""
    comps = [c[:4] for c in comps]
    if vertical:
        comps = [(y, x, h, w) for x, y, w, h in comps]       # swap axes
    comps = sorted(comps, key=lambda c: (c[0]))
    used = [False] * len(comps)
    res = []
    for i, c in enumerate(comps):
        if used[i]:
            continue
        grp = [c]
        used[i] = True
        changed = True
        while changed:
            changed = False
            x1 = max(g[0] + g[2] for g in grp)
            cy = np.mean([g[1] + g[3] / 2 for g in grp])
            hh = np.median([g[3] for g in grp])
            for j, d in enumerate(comps):
                if used[j]:
                    continue
                if abs((d[1] + d[3] / 2) - cy) < 0.3 * hh and 0.6 < d[3] / hh < 1.6 and -0.2 * hh < d[0] - x1 < 0.75 * hh:
                    grp.append(d)
                    used[j] = True
                    changed = True
        x0 = min(g[0] for g in grp)
        y0 = min(g[1] for g in grp)
        x1 = max(g[0] + g[2] for g in grp)
        y1 = max(g[1] + g[3] for g in grp)
        if vertical:
            res.append((y0, x0, y1 - y0, x1 - x0, len(grp)))
        else:
            res.append((x0, y0, x1 - x0, y1 - y0, len(grp)))
    return res


def read(img):
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "w.png")
        cv2.imwrite(p, img)
        r = subprocess.run(["tesseract", p, "stdout", "--psm", "7", "-c", "tessedit_char_whitelist=0123456789R.,", "tsv"],
                           capture_output=True, text=True)
    best = None
    for line in r.stdout.splitlines()[1:]:
        q = line.split("\t")
        if len(q) == 12 and q[11].strip():
            t, conf = q[11].strip(), float(q[10])
            best = (t, conf) if best is None else (best[0] + " " + t, min(best[1], conf))
    return best


def found(page, min_conf=80):
    rgb = graphics_render(page)
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    comps, lab = components(rgb)
    ink = g < 150
    out = []
    for vertical in (False, True):
        for x, y, w, h, n in words(comps, vertical):
            if n > 6:
                continue
            pad = int(0.6 * min(w, h)) + 6
            crop = g[max(0, y - pad):y + h + pad, max(0, x - pad):x + w + pad]
            if crop.size == 0:
                continue
            crop = cv2.copyMakeBorder(crop, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
            tries = [(crop, (1, 0), (0, -1))] if not vertical else \
                [(cv2.rotate(crop, cv2.ROTATE_90_CLOCKWISE), (0, -1), (-1, 0)),
                 (cv2.rotate(crop, cv2.ROTATE_90_COUNTERCLOCKWISE), (0, 1), (1, 0))]
            for img, u, v in tries:
                r = read(img)
                if not r:
                    continue
                t, conf = r
                t = t.replace(" ", "")
                m = NUM_RE.match(t)
                digits = len(re.sub(r"[^0-9R]", "", t))
                if n > digits + 1 or (digits == 1 and conf < 92):
                    continue                                   # part of a longer word ('3,5 kg', '2x150') or a stray shape
                px = rgb[y:y + h, x:x + w][ink[y:y + h, x:x + w]]
                if len(px) and not (px[:, 2].mean() - px[:, 0].mean() > 35):
                    continue                                   # dimensions are blue
                if m and conf >= min_conf:
                    val = float(m.group(2).replace(",", "."))
                    size = (w if vertical else h) / Z / 0.72
                    out.append({"text": t, "value": val, "rect": fitz.Rect(x / Z, y / Z, (x + w) / Z, (y + h) / Z),
                                "u": u, "v": v, "size": size, "conf": conf})
                    break
    return out


if __name__ == "__main__":
    import sys
    doc = fitz.open("/home/claude/eurostamp/pdf/cat.pdf")
    for a in sys.argv[1:]:
        p = int(a)
        for f in found(doc[p - 1]):
            print(p, f["text"], round(f["conf"]), f["rect"], f["u"], round(f["size"], 1))
