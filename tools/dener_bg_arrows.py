#!/usr/bin/env python3
"""Back gauge figures with their axis arrows (the owner's request of Oct 29 2026: "the arrows show which way each axis moves").

Dener's XL quotation draws the back gauge pictures as raster images and the axis arrows and letters (X, R, Z1 …) as vector
graphics and text on top.  pdfimages (tools/dener_detail_photos.py) only takes the raster, so the arrows were lost.  Here the
page is rendered twice by MuPDF around each figure — once with the figure's own picture replaced by a white image, once by a
black one, every other picture made transparent — and the two renders give the arrow / letter layer exactly:

    final = B + clean × (W − B) / 255          (W, B: the white and the black render; clean: our 2× ESRGAN picture)

so the arrows and letters sit at their original places, sharp at the new resolution, over the upscaled picture.  The
4-axis figure reuses the 2-axis picture with its own arrows, so the PDF yields four figures from three pictures.  Text or
graphics of a neighbouring figure that reach into a clip are blanked back to the picture (`foreign`).

    python3 tools/dener_bg_arrows.py          → tools/src-images/dener-detail/dn-det-bg-{2axis,4axis,5axis,6axis-atf}.jpg
    (needs the quotation PDF below — outside the repository; without it the committed images stay as they are)
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DET = os.path.join(ROOT, "tools", "src-images", "dener-detail")
PDF = "/home/claude/untrusted/dener-pc/3.6 mt 220 ton XL - NOVOTECH - 6.6.2026 - Special for Protech Welding.pdf"
MAIN = (55, 61, 79)          # the three back gauge pictures (xref 55 is placed twice: the 2-axis and the 4-axis figure)

# key: page (0-based), picture xref, which placement of it, the clean 2× picture, and the box (pt) in which the figure's own
# arrows and letters lie (anything else drawn inside the clip is a neighbour's and is blanked)
FIGS = {
    "dn-det-bg-2axis": dict(page=4, xref=55, n=0, clean="dn-det-bg-xr.jpg", own=(340, 298, 515, 440)),
    "dn-det-bg-4axis": dict(page=4, xref=55, n=1, clean="dn-det-bg-xr.jpg", own=(365, 495, 565, 600)),
    "dn-det-bg-5axis": dict(page=4, xref=61, n=0, clean="dn-det-bg-5axis-base.jpg", own=(372, 603, 565, 735),
                            prime=(513.5, 610.7)),   # the top letter is X′ (each finger's own depth axis); the PDF prints a bare X
    "dn-det-bg-6axis-atf": dict(page=5, xref=79, n=0, clean="dn-det-bg-6axis-atf-base.jpg", own=(300, 88, 590, 258)),
}


def _inside(b, box):
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return box[0] <= cx <= box[2] and box[1] <= cy <= box[3]


def _render(fig, mode, clip, zoom):
    import pymupdf as fitz
    doc = fitz.open(PDF)
    page = doc[fig["page"]]
    for x in MAIN:
        info = doc.extract_image(x)
        w, h = info["width"], info["height"]
        if x == fig["xref"]:
            pm = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w, h), False)
            pm.clear_with(255 if mode == "W" else 0)
        else:
            pm = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w, h), True)
            pm.clear_with()                     # all zero: black and fully transparent
        if any(i[0] == x for i in page.get_images(full=True)):
            page.replace_image(x, pixmap=pm)
            page = doc[fig["page"]]
    if fig.get("prime"):                        # add the prime after the letter that starts at this point
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if abs(s["bbox"][0] - fig["prime"][0]) < 0.6 and abs(s["bbox"][1] - fig["prime"][1]) < 0.6:
                        page.insert_text((s["bbox"][0] + 7.6, s["origin"][1]), "'", fontname="hebo", fontsize=s["size"])
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3].astype(np.float32)


def figure(key):
    import pymupdf as fitz
    fig = FIGS[key]
    doc = fitz.open(PDF)
    page = doc[fig["page"]]
    rect = page.get_image_rects(fig["xref"])[fig["n"]]
    own_box = fig["own"]
    # the figure's own arrows (filled polygons), letters and letter boxes
    elems, foreign = [], []
    for d in page.get_drawings():
        (elems if _inside(d["rect"], own_box) else foreign).append(tuple(d["rect"]))
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if not t:
                    continue
                label = len(t) <= 2 and t[0] in "XRZ"
                (elems if (label and _inside(s["bbox"], own_box)) else foreign).append(tuple(s["bbox"]))
    for img in page.get_images(full=True):
        if img[0] in MAIN or img[0] == 9:       # the pictures themselves, the Dener logo in the header
            continue
        for r in page.get_image_rects(img[0]):
            (elems if _inside(r, own_box) else foreign).append(tuple(r))
    x0 = min([rect.x0] + [e[0] for e in elems]) - 4
    y0 = min([rect.y0] + [e[1] for e in elems]) - 4
    x1 = max([rect.x1] + [e[2] for e in elems]) + 4
    y1 = max([rect.y1] + [e[3] for e in elems]) + 4
    clip = fitz.Rect(x0, y0, x1, y1)
    clean = Image.open(os.path.join(DET, fig["clean"])).convert("RGB")
    zoom = clean.width / rect.width
    W = _render(fig, "W", clip, zoom)
    B = _render(fig, "B", clip, zoom)
    H, Wd = W.shape[:2]
    full = Image.new("RGB", (Wd, H), (255, 255, 255))
    pw, ph = round(rect.width * zoom), round(rect.height * zoom)
    full.paste(clean.resize((pw, ph), Image.LANCZOS), (round((rect.x0 - x0) * zoom), round((rect.y0 - y0) * zoom)))
    C = np.asarray(full, np.float32)
    out = B + C * (W - B) / 255.0
    for fb in foreign:                           # a neighbour's letters or arrows reaching into the clip: back to the picture
        fx0, fy0, fx1, fy1 = fb
        if fx1 < x0 or fx0 > x1 or fy1 < y0 or fy0 > y1:
            continue
        a, b_ = max(0, int((fx0 - 1 - x0) * zoom)), max(0, int((fy0 - 1 - y0) * zoom))
        c, d = min(Wd, int((fx1 + 1 - x0) * zoom) + 1), min(H, int((fy1 + 1 - y0) * zoom) + 1)
        out[b_:d, a:c] = C[b_:d, a:c]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), len(elems)


def main():
    if not os.path.exists(PDF):
        print("!! the Dener quotation PDF is not here — the committed back gauge figures stay as they are")
        return
    # the clean pictures (tools/dener_detail_photos.py: pdfimages + 2× ESRGAN) are kept as *-base.jpg, so a re-run starts clean
    for k in ("dn-det-bg-5axis", "dn-det-bg-6axis-atf"):
        base = os.path.join(DET, k + "-base.jpg")
        if not os.path.exists(base):
            os.replace(os.path.join(DET, k + ".jpg"), base)
    for key in [a for a in sys.argv[1:] if not a.startswith("-")] or list(FIGS):
        im, n = figure(key)
        path = os.path.join(DET, key + ".jpg")
        im.save(path, quality=93)
        print(f"{key:24s} {im.size} · {n} arrow / letter elements -> {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
