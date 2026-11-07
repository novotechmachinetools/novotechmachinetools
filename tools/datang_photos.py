#!/usr/bin/env python3
"""Photos of the welding positioners, turning rolls and column & boom manipulators sold in the NovoTech value line (built in
China by Wuxi Datang; the owner, Nov 7 2026: the maker's marks, Chinese text and watermarks come off every photo).

Two sources, copied once to /home/claude/datang-src/:
  - the maker's site (downloaded through the owner's browser): 640 px product photos on white, each with the maker's logo in the
    top right corner and a semi-transparent bold italic 'DATANG' watermark somewhere across the machine;
  - the maker's specification document (SPECIFICATION WITH PHOTOS.doc): larger photos without the watermark, some with a date
    stamp or the maker's Chinese name on the machine.

The watermark is the same word on every site photo: it is found by matching a rendered template (FreeSans Bold Oblique matches
its letters), removed by undoing its 29 % white overlay, and the thin outline the letters leave is filled with LaMa
(tools/lama_inpaint.py), as are the corner logo, the stamps, stickers and name plates listed per photo.

    python3 tools/datang_photos.py [key …]            → tools/src-images/datang/<key>.jpg and the tools/image_map.json entries
    python3 tools/datang_photos.py --preview DIR [key …]  → cleaned photos in DIR only
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lama_inpaint import inpaint  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/datang-src/"
DST = os.path.join(ROOT, "tools", "src-images", "datang")
FONT = "/usr/share/fonts/truetype/freefont/FreeSansBoldOblique.ttf"
ALPHA = 0.292            # the watermark's white overlay, measured on 13 photos (median of (I - J) / (255 - J) inside the letters)
WM_SIZE = (204, 36)      # its letters on a 640 px photo, w × h
LOGO_640 = (400, 4, 636, 90)   # the maker's logo, top right of every 640 px site photo


def P(src, alt, boxes=(), cut=True, wm=True, logo=True, crop=None, scale=1.0, wm_box=None, logo_box=None, wm_fill=False):
    """src: file in SRC; boxes: (x0, y0, x1, y1) areas in source pixels to fill with LaMa (stamps, stickers, Chinese text),
    or ("flat", x0, y0, x1, y1) for a smooth fill on a plain painted surface;
    wm: a site photo with the watermark; scale: the photo's size over 640 px (the watermark and logo scale with it);
    wm_box: where to look for the watermark when the default search (the middle of the photo) misses it;
    logo_box: the maker's corner logo when it is not where it sits on the 640 px photos; wm_fill: fill the watermark's letters
    with LaMa instead of undoing the overlay (plain surfaces, where the overlay leaves a faint trace)."""
    return dict(src=src, alt=alt, boxes=list(boxes), cut=cut, wm=wm, logo=logo, crop=crop, scale=scale, wm_box=wm_box,
                logo_box=logo_box, wm_fill=wm_fill)


def D(src, alt, boxes=(), cut=False, crop=None):        # a photo from the specification document
    return P(src, alt, boxes, cut=cut, wm=False, logo=False, crop=crop)


PHOTOS = {
    # positioners
    "dt-hb-light": P("light-positioner.png", "Light welding positioner with its control box, 10 – 100 kg worktable load",
                     boxes=[(98, 243, 174, 300), (190, 435, 264, 454)]),
    "dt-hb": D("doc-image1.jpg", "HB welding positioner — tilting worktable with T-slots, rotation gearbox and control box",
               boxes=[(1440, 55, 1600, 122)], cut=True),
    "dt-hb-site": P("hb-positioner.png", "HB welding positioner with geared tilting and the pendant control box",
                    boxes=[(503, 333, 558, 428)]),
    "dt-hb-2": D("doc-image2.jpg", "HB welding positioner — the tilting sector gear and the worktable",
                 boxes=[(1390, 355, 1720, 548)], cut=True),
    "dt-hb-big": D("doc-image3.jpg", "Heavy HB welding positioners in final assembly", boxes=[(425, 790, 590, 1095)]),
    "dt-hbt": P("rotary-table.png", "HBT rotary welding table — a horizontal turntable with VFD speed control",
                boxes=[(448, 452, 502, 507)]),
    "dt-hbj": P("lift-positioner.png", "HBJ lift welding positioner — the worktable rises, tilts and turns",
                boxes=[(126, 248, 164, 300)]),
    "dt-headstock": P("headstock-positioner.png", "Headstock welding positioner with a vertical faceplate", wm_fill=True),
    "dt-head-tail": P("head-tail-lifting-positioner.png", "Headstock and tailstock lifting positioner pair",
                      boxes=[(146, 370, 200, 426)]),
    "dt-head-tail-fixed": P("head-tail-fixed-positioner.png", "Fixed-height headstock and tailstock positioners",
                            boxes=[(126, 346, 174, 434)], wm_box=(190, 340, 450, 420)),
    "dt-l-type": P("l-type-positioner.png", "L-type welding positioner — motor-tilted arm and a turning worktable", wm_fill=True),
    "dt-hydraulic": P("hydraulic-positioner.png", "Three-axis hydraulic welding positioner — lift, tilt and rotation"),
    "dt-special": P("special-positioner.png", "Special welding positioner with a three-jaw welding chuck"),
    # turning rolls
    "dt-dzg-light": P("light-rotator.png", "Light welding turning rolls — one drive roll, one idler roll and a foot switch",
                      boxes=[(70, 430, 122, 448)]),
    "dt-dzg": P("self-aligning-rotator.png", "DZG self-aligning welding turning rolls — the wheel pairs swing to the vessel diameter"),
    "dt-dzg-2": D("doc-image4.jpg", "DZG self-aligning turning rolls with their control boxes", boxes=[(2950, 3075, 4240, 3235)]),
    "dt-dkg": P("bolt-adjustable-rotator.png", "DKG bolt-adjustable welding turning rolls — drive and idler sections"),
    "dt-dkg-2": D("doc-image5.png", "DKG bolt-adjustable turning rolls, drive section", boxes=[(510, 458, 750, 502)]),
    "dt-dsk": P("lead-screw-rotator.png", "DSK lead-screw-adjustable welding turning rolls with hand wheels"),
    "dt-dsk-2": D("doc-image6.jpg", "DSK lead-screw-adjustable turning rolls — the roll pairs move on the screw", cut=True),
    "dt-gglj": P("pinch-rotator.png", "GGLJ pinch-type pipe rotator turning an elbow for flange and segment welding",
                 boxes=[("flat", 400, 412, 440, 469), ("flat", 410, 382, 432, 406)]),
    "dt-fitup": P("fit-up-rotator.png", "Hydraulic fit-up turning rolls — the lifting rolls align two shell sections"),
    # column and boom manipulators
    "dt-dlh-small": P("manipulator-small.png", "Small column and boom welding manipulator", wm_box=(300, 330, 700, 470),
                      boxes=[(303, 368, 508, 432)], logo_box=(480, 0, 800, 115)),
    "dt-dlh-small-2": D("doc-image7.jpg", "Small column and boom manipulator with a welding head",
                        boxes=[(320, 302, 502, 368), (326, 100, 396, 172)]),
    "dt-dlh-medium": P("manipulator-medium.png", "Medium column and boom welding manipulator with flux recovery",
                       boxes=[(180, 316, 226, 344)]),
    "dt-dlh-heavy": P("manipulator-heavy.png", "Heavy column and boom welding manipulator on a travelling carriage"),
}


def template(scale=1.0):
    w, h = int(round(WM_SIZE[0] * scale)), int(round(WM_SIZE[1] * scale))
    f = ImageFont.truetype(FONT, 100)
    bb = f.getbbox("DATANG")
    im = Image.new("L", (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), 0)
    ImageDraw.Draw(im).text((10 - bb[0], 10 - bb[1]), "DATANG", font=f, fill=255)
    a = np.array(im)
    ys, xs = np.where(a > 0)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return cv2.resize(a.astype(np.float32) / 255, (w, h), interpolation=cv2.INTER_AREA)


def excess(bgr):
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    return g - cv2.morphologyEx(g, cv2.MORPH_OPEN, np.ones((19, 19), np.uint8))


def find_watermark(bgr, T, box=None):
    """the watermark's top-left corner: best match of the template on the bright-stroke map, in the middle half of the photo"""
    H, W = bgr.shape[:2]
    x0, y0, x1, y1 = box or (int(W * 0.15), int(H * 0.25), int(W * 0.85), int(H * 0.85))
    win = np.clip(excess(bgr)[y0:y1, x0:x1], 0, None)
    r = cv2.matchTemplate(win, T, cv2.TM_CCORR_NORMED)
    _, score, _, loc = cv2.minMaxLoc(r)
    return x0 + loc[0], y0 + loc[1], score


def photo_alpha(bgr, T, x, y):
    """the overlay's strength on this photo: (I - J) / (255 - J) inside the letters, J filled in from around them; the
    measured 29 % when the letters sit on too little dark background to tell"""
    h, w = T.shape
    full = np.zeros(bgr.shape[:2], np.float32)
    full[y:y + h, x:x + w] = T
    J = cv2.inpaint(bgr, cv2.dilate((full > 0.05).astype(np.uint8), np.ones((5, 5), np.uint8)), 7, cv2.INPAINT_TELEA).astype(np.float32)
    I = bgr.astype(np.float32)
    num, den = (I - J).mean(2), (255 - J).mean(2)
    sel = (full > 0.6) & (den > 70)
    if sel.sum() < 300:
        return ALPHA
    return float(np.clip(np.median(num[sel] / den[sel]), 0.2, 0.35))


def remove_watermark(bgr, T, box=None, fill=False):
    """undo the overlay (fill=False) or, on a plain surface where that leaves a trace, fill the letters with LaMa"""
    x, y, score = find_watermark(bgr, T, box)
    h, w = T.shape
    pad = 6
    if fill:
        full = np.zeros(bgr.shape[:2], np.float32)
        full[y:y + h, x:x + w] = T
        return bgr.copy(), cv2.dilate((full > 0.02).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=3) * 255, score
    alpha = photo_alpha(bgr, T, x, y)
    g = bgr.astype(np.float32)
    best = None
    for dy in np.arange(-1.5, 1.51, 0.25):             # sub-pixel fit: the shift that leaves the flattest letter outline
        for dx in np.arange(-1.5, 1.51, 0.25):
            t = cv2.warpAffine(np.pad(T, pad), np.float32([[1, 0, dx], [0, 1, dy]]), (w + 2 * pad, h + 2 * pad))
            a = (alpha * t)[..., None]
            c = g[y - pad:y + h + pad, x - pad:x + w + pad]
            J = np.clip((c - a * 255) / (1 - a), 0, 255)
            lap = np.abs(cv2.Laplacian(cv2.cvtColor(J.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32), cv2.CV_32F))
            band = cv2.dilate((t > 0.05).astype(np.uint8), np.ones((3, 3), np.uint8)) - cv2.erode((t > 0.95).astype(np.uint8), np.ones((3, 3), np.uint8))
            s = float((lap * band).sum())
            if best is None or s < best[0]:
                best = (s, t, J)
    _, t, J = best
    out = g.copy()
    out[y - pad:y + h + pad, x - pad:x + w + pad] = J
    full = np.zeros(bgr.shape[:2], np.float32)
    full[y - pad:y + h + pad, x - pad:x + w + pad] = t
    outer = cv2.dilate((full > 0.02).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2)
    inner = cv2.erode((full > 0.98).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1)
    band = np.clip(outer.astype(np.int16) - inner, 0, 1).astype(np.uint8) * 255
    return out.astype(np.uint8), band, score


def clean(key):
    p = PHOTOS[key]
    bgr = cv2.imread(SRC + p["src"], cv2.IMREAD_COLOR)
    H, W = bgr.shape[:2]
    mask = np.zeros((H, W), np.uint8)
    if p["wm"]:
        bgr, band, score = remove_watermark(bgr, template(p["scale"]), p["wm_box"], p["wm_fill"])
        if score < 0.3:
            print(f"!! {key}: watermark match only {score:.2f}")
        mask |= band
    if p["logo"]:
        x0, y0, x1, y1 = p["logo_box"] or LOGO_640
        ring = np.concatenate([bgr[y1:y1 + 6, x0:x1].reshape(-1, 3), bgr[y0:y1, max(0, x0 - 6):x0].reshape(-1, 3)])
        if np.median(ring) >= 250:          # the logo sits on the white background: paint it white
            bgr[y0:y1, x0:x1] = 255
        else:
            mask[y0:y1, x0:x1] = 255
    flat = np.zeros((H, W), np.uint8)       # boxes on a plain painted surface: a smooth fill (LaMa can smear colour in from the edges)
    for bx in ([] if os.environ.get("NOBOX") else p["boxes"]):
        if bx[0] == "flat":
            x0, y0, x1, y1 = bx[1:]
            flat[y0:y1, x0:x1] = 255
        else:
            x0, y0, x1, y1 = bx
            mask[y0:y1, x0:x1] = 255
    if flat.any():
        bgr = cv2.inpaint(bgr, flat, 5, cv2.INPAINT_TELEA)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    if mask.any():
        # fill the parts one at a time so each gets its own context window
        n, lab = cv2.connectedComponents(cv2.dilate(mask, np.ones((9, 9), np.uint8)))
        for i in range(1, n):
            part = ((lab == i) & (mask > 0)).astype(np.uint8) * 255
            rgb = inpaint(rgb, part)
    im = Image.fromarray(rgb)
    if p["crop"]:
        im = im.crop(p["crop"])
    if max(im.size) > 2000:                 # the document's camera photos: 2000 px is plenty for the site's largest image
        im.thumbnail((2000, 2000), Image.LANCZOS)
    return im


def register(keys):
    path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(path, encoding="utf-8"))
    for k in keys:
        old = imap.get(k, {}).get("cutout")
        imap[k] = {"src": f"tools/src-images/datang/{k}.jpg", "alt": PHOTOS[k]["alt"], "section": "datang", "trim": False, "quality": 82,
                   "cutout": old if isinstance(old, str) else PHOTOS[k]["cut"]}
    json.dump(imap, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def main():
    args = sys.argv[1:]
    out = DST
    if args[:1] == ["--preview"]:
        out, args = args[1], args[2:]
    keys = args or list(PHOTOS)
    os.makedirs(out, exist_ok=True)
    for k in keys:
        im = clean(k)
        im.convert("RGB").save(os.path.join(out, k + ".jpg"), quality=93)
        print(k, im.size)
    if out == DST:
        register(keys)


if __name__ == "__main__":
    main()
