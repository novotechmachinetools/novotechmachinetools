#!/usr/bin/env python3
"""High-resolution supplier photos of the NovoTech value-line saws (the owner's WeTransfer "photo for band saw", Oct 28 2026,
kept in /home/claude/ttmc-new/band_saw_2026-10-28/).  They replace the catalogue crops of tools/ttmc_more_photos.py for the
cold saws and supply the vertical band saws (VS series) of tools/value_line_data.py.

Nameplates and the supplier's logo are removed with LaMa (tools/lama_inpaint.py); the white margin is trimmed; a photo
under 700 px is upscaled 2x with Real-ESRGAN (tools/esrgan.py).  Product photos are cut out later by tools/make_images.py
(BiRefNet) unless the source already carries its own alpha.

    python3 tools/ttmc_hires_photos.py [key …]
        tm-* keys  → tools/src-images/ttmc-more/<key>.jpg   (registered by tools/ttmc_more_pages.py)
        nt-* keys  → tools/src-images/value-line/<key>.png  (registered by tools/value_line_data.py)
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/ttmc-new/band_saw_2026-10-28/"
DST_TM = os.path.join(ROOT, "tools", "src-images", "ttmc-more")
DST_NT = os.path.join(ROOT, "tools", "src-images", "value-line")
SMALL = 700          # px, longest side of the machine: below it the photo is upscaled 2x

# key: dict(src, alt, boxes=[(x0, y0, x1, y1) in source pixels — nameplates / logo, filled by LaMa], detail=False)
# NB: the supplier named two files the wrong way round — "VS-500.jpg" carries the VS-400 nameplate and is the catalogue's VS-400
# photo (blue, with the lamp); "VS400.jpg" is the grey machine the catalogue shows as the VS-500.
PHOTOS = {
    # ---------------------------------------------------------------- cold saws (tools/ttmc_more_data.py, tt-cs / tt-pds400 / tt-tv / tt-qcs400)
    "tm-cs": dict(src="CS-315-350.jpg", alt="CS-315 cold saw on stand with two-speed motor and double vise"),
    "tm-cs-225": dict(src="CS-225.jpg", alt="CS-225 bench cold saw, 9″ blade, with double vise and length stop"),
    "tm-cs-250": dict(src="CS-250.jpg", alt="CS-250 / CS-275 cold saw on cabinet stand, 10 – 11″ blade"),
    "tm-pds400": dict(src="PDS400.jpg", alt="PDS-400 heavy-duty cold saw for 16″ blades on cabinet stand"),
    "tm-tv": dict(src="TV300 -350-400.jpg", alt="TV-300 / TV-350 / TV-400 abrasive cut-off saw on stand"),
    "tm-qcs400a": dict(src="QCS400A.png", alt="QCS-400A aluminum cut-off saw with pneumatic clamping and safety hood", boxes=[(606, 726, 707, 784)]),
    # ---------------------------------------------------------------- vertical band saws (tools/value_line_data.py, novotech-vs)
    "nt-vs300-1": dict(src="VS300.png", alt="NovoTech VS-300 vertical metal band saw with blade welder, 12″ throat"),
    "nt-vs400-1": dict(src="VS-500.jpg", alt="NovoTech VS-400 vertical metal band saw with work light and table gauge, 15-3/4″ throat",
                       boxes=[(1648, 364, 1897, 512), (1578, 664, 1972, 902)]),
    "nt-vs500-1": dict(src="VS400.jpg", alt="NovoTech VS-500 vertical metal band saw, 19-3/4″ throat", boxes=[(396, 187, 476, 244)]),
    # ---------------------------------------------------------------- CNC double column saw (the catalogue crop had white blotches — Oct 28 2026)
    "nt-a14-1": dict(src="BS-500G-500GT.jpg", alt="NovoTech BS-500G / BS-500GT CNC automatic band saw", boxes=[(664, 430, 733, 468)], up=True),
}


def trim(im, thr=240, pad=12):
    """crop the white (or transparent) margin, keeping a small pad"""
    if im.mode == "RGBA":
        bb = im.getchannel("A").getbbox()
    else:
        g = im.convert("L").point(lambda v: 255 if v < thr else 0)
        bb = g.getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def fill_boxes(im, boxes):
    from lama_inpaint import inpaint
    rgba = im.mode == "RGBA"
    rgb = np.asarray(im.convert("RGB")).copy()
    mask = np.zeros(rgb.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes:
        mask[y0:y1, x0:x1] = 255
    out = Image.fromarray(inpaint(rgb, mask))
    if rgba:
        out.putalpha(im.getchannel("A"))
    return out


def process(key):
    p = PHOTOS[key]
    im = Image.open(SRC + p["src"])
    im = im.convert("RGBA") if im.mode == "RGBA" else im.convert("RGB")
    if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] == 255:
        im = im.convert("RGB")
    if p.get("boxes"):
        im = fill_boxes(im, p["boxes"])
    im = trim(im)
    if max(im.size) < SMALL or p.get("up"):
        from esrgan import upscale
        im = upscale(im.convert("RGB"))
    if key.startswith("tm-"):
        os.makedirs(DST_TM, exist_ok=True)
        im.convert("RGB").save(os.path.join(DST_TM, key + ".jpg"), quality=92)
    else:
        os.makedirs(DST_NT, exist_ok=True)
        im.save(os.path.join(DST_NT, key + ".png"), optimize=True)
    return im.size


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for k in keys:
        print(f"{k:14s} {process(k)}")


if __name__ == "__main__":
    main()
