#!/usr/bin/env python3
"""Hidroliksan production-press photos → logo-free sources in tools/src-images/hidroliksan/.

The supplier's lettering ("HiDROLiKSAN" with its bar icon, sometimes "HALİM USTA" under it) is boxed by hand per photo
(source pixels, located on grid views) and filled with LaMa (tools/delogo.py, mode "lama"); `ocr=True` on a photo adds
tesseract hits (unreliable — kept for first passes). `--check` writes
/home/claude/hidroliksan/work/check-<key>.jpg with the filled rectangles drawn for review.

    python3 tools/hidroliksan_photos.py [keys]          export
    python3 tools/hidroliksan_photos.py --check [keys]  contact sheets only
"""
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delogo import delogo  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/hidroliksan/catalogue/"
WORK = "/home/claude/hidroliksan/work/"
OUT = os.path.join(ROOT, "tools", "src-images", "premium-presses")
MAX_SIDE = 2600
OCR_SIDE = 3000
A = "lama"
WORD = re.compile(r"H[iI1l]?D|ROL|[iI1l]KSAN|KSAN|HIDROL|DROLIK", re.I)

# key: source file, alt, extra boxes (source px), cutout False for scene photos
PHOTOS = {
    "hk-hdd": dict(src="hdd.jpg", boxes=[(500, 1290, 1300, 1560)], alt="H-frame double action deep drawing press, HDD series — NovoTech premium line, with die cushion and pendant control"),
    "hk-hdd-2": dict(src="hdd-2.jpg", boxes=[(700, 1095, 1450, 1330)], alt="HDD double action deep drawing press — side view with the control pendant"),
    "hk-hdd-3": dict(src="hdd-3.jpg", boxes=[(880, 1120, 1710, 1420)], alt="HDD deep drawing press with the enclosed work area and side control panel"),
    "hk-hsa": dict(src="hsa.jpg", boxes=[(650, 1120, 1440, 1345)], alt="H-frame single action hydraulic press, HSA series — NovoTech premium line, with die support arms"),
    "hk-hsa-2": dict(src="hsa-2.jpg", boxes=[(185, 365, 335, 428)], alt="HSA single action press with separate electrical cabinet"),
    "hk-hsa-3": dict(src="hsa-3.jpg", boxes=[(870, 1350, 1560, 1650)], alt="HSA single action press — front view with light barriers"),
    "hk-hcfp": dict(src="HCFP-Yeni.jpg", boxes=[(1900, 980, 3680, 1600)], alt="Column frame single / double action press, HCFP series — NovoTech premium line, enclosed column frame"),
    "hk-hcfp-2": dict(src="COLOUMN FRAME PRESSES.jpg", boxes=[(640, 455, 905, 530)], alt="HCFP four-column press with die support arms"),
    "hk-cfss": dict(src="cfss.jpg", boxes=[(980, 600, 1570, 800)], alt="Enclosed C-frame single action press, CFSS series — NovoTech premium line, with two-hand control station"),
    "hk-cfss-2": dict(src="cfss-2.jpg", boxes=[(800, 890, 1410, 1095)], alt="CFSS enclosed C-frame press with HMI touchscreen panel"),
    "hk-cfss-3": dict(src="cfss-3.jpg", boxes=[(540, 1095, 1300, 1370)], alt="CFSS enclosed C-frame press — light barriers and two-hand control"),
    "hk-cfss-4": dict(src="cfss-4.jpg", boxes=[(485, 380, 760, 495)], alt="CFSS 150 – 250 enclosed C-frame press with pendant control"),
    "hk-cfs": dict(src="MODEL CFS.jpg", boxes=[(160, 335, 318, 418), (336, 335, 410, 418)], alt="C-frame single action press, CFS series — NovoTech premium line, guarded work area"),
    "hk-cfdd": dict(src="cfdd150-200-250.jpg", boxes=[(1010, 965, 1710, 1250)], alt="C-frame deep drawing press, CFDD series — NovoTech premium line, with die cushion and two-hand control"),
    "hk-cfdd-100": dict(src="CFDD100 - 1.jpg", boxes=[(420, 330, 890, 495)], alt="CFDD 100 C-frame deep drawing press"),
    "hk-smc": dict(src="smc.jpg", boxes=[(935, 1090, 1700, 1440)], alt="SMC composite moulding press with heated platens, HHRP series — NovoTech premium line"),
    "hk-smc-2": dict(src="smc-2.jpg", boxes=[(760, 1080, 1440, 1300)], alt="SMC / HHRP hot plate press — front view with safety fencing"),
    "hk-smc-2500": dict(src="SMC-2500.jpg", boxes=[(960, 790, 1640, 1120)], alt="SMC 2500 hot plate hydraulic press"),
    "hk-smc-detail": dict(src="smc detail.jpg", cutout=False, alt="SMC press — T-slotted heated platen with insulation"),
    "hk-smc-detail-2": dict(src="smc detail 2.jpg", cutout=False, alt="SMC press — platen guide and safety light curtain"),
    "hk-hsps": dict(src="hsps.jpg", boxes=[(1400, 650, 2420, 930)], alt="Hydraulic portal straightening press, HSPS series — NovoTech premium line, gantry with safety rails"),
    "hk-hsps-300": dict(src="HSPS300.jpg", boxes=[(1200, 320, 2000, 580)], alt="HSPS 300 portal straightening press with side control cabinet"),
    "hk-hsps-100": dict(src="hsps100-T.jpg", boxes=[(810, 570, 1510, 790)], alt="HSPS 100 compact portal straightening press"),
    "hk-hsps-detail": dict(src="hsps detail.jpg", cutout=False, alt="HSPS — rack drive for the gantry travel"),
    "hk-hdt": dict(src="hdt.jpg", boxes=[(990, 915, 1830, 1200)], alt="H-frame hydraulic press, Eco model HDT series — NovoTech premium line, with T-slotted table"),
}


def ocr_words(im, side):
    s = side / max(im.size)
    small = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS) if s < 1 else im
    tmp = os.path.join(WORK, "_ocr.png")
    small.save(tmp)
    r = subprocess.run(["tesseract", tmp, "-", "--psm", "11", "tsv"], capture_output=True, text=True)
    words = []
    for l in r.stdout.split("\n")[1:]:
        p = l.split("\t")
        if len(p) == 12 and p[11].strip():
            try:
                conf = float(p[10])
            except ValueError:
                continue
            x, y, w, h = (int(v) for v in p[6:10])
            if conf > 25 and WORD.search(p[11]) and h > 8:
                words.append((x / s, y / s, (x + w) / s, (y + h) / s))
    return words


def ocr_boxes(im):
    """Boxes (source px) of the supplier lettering: tesseract on several downscaled copies, hits merged."""
    words = []
    for side in (1400, 2000, 2600, 3200):
        words += ocr_words(im, side)
    boxes = []
    for b in sorted(words):
        for q in boxes:
            h = max(q[3] - q[1], b[3] - b[1])
            if abs((q[1] + q[3]) / 2 - (b[1] + b[3]) / 2) < h and b[0] - q[2] < 3 * h and q[0] - b[2] < 3 * h:
                q[0], q[1], q[2], q[3] = min(q[0], b[0]), min(q[1], b[1]), max(q[2], b[2]), max(q[3], b[3])
                break
        else:
            boxes.append(list(b))
    out = []
    for x0, y0, x1, y1 in boxes:
        h = y1 - y0
        x0 -= 1.6 * h          # the bar icon sits left of the lettering
        y0 -= 0.35 * h; y1 += 0.35 * h; x1 += 0.3 * h
        out.append((max(0, int(x0)), max(0, int(y0)), int(x1), int(y1)))
    return out


def process(key, check_only=False):
    p = PHOTOS[key]
    im = Image.open(SRC + p["src"]).convert("RGB")
    boxes = (ocr_boxes(im) if p.get("ocr") else []) + [tuple(b) for b in p.get("boxes", [])]
    boxes = [(x0, y0, x1, y1, A) for x0, y0, x1, y1 in boxes]
    s = min(1.0, MAX_SIDE / max(im.size))
    if check_only:
        d = ImageDraw.Draw(im)
        for x0, y0, x1, y1, _ in boxes:
            d.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=max(3, int(im.width / 400)))
        sm = im.resize((int(im.width * s * 0.6), int(im.height * s * 0.6)))
        sm.save(WORK + f"check-{key}.jpg", quality=80)
        print(f"{key:18s} {im.size} boxes={boxes}")
        return
    report = []
    if boxes:
        im = delogo(im, boxes, report=report)
    if s < 1:
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, key + ".jpg")
    im.save(out, quality=92)
    print(f"{key:18s} {im.size} boxes={len(boxes)} -> {out}")


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keys = args or list(PHOTOS)
    for k in keys:
        process(k, check_only="--check" in sys.argv)
