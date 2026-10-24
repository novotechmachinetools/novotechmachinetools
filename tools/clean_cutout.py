#!/usr/bin/env python3
"""Cut-out for catalogue photos whose white covers are the same pure white as the background, where a
threshold cut (tools/cutout2.py) and a raw IS-Net mask both bite into the covers.

IS-Net gives the silhouette; every enclosed hole in it is filled (a hole inside a machine is never
background), notches on the outline are healed with a morphological closing, and any clearly non-white
pixel next to the mask is kept.  Result: the machine with nothing eaten, nothing of the background kept.

    python3 tools/clean_cutout.py <key> [<key> ...]     keys from tools/image_map.json; the white source is
                                                        tools/src-images/value-line/<key>.png
    → tools/src-images/cutouts/<key>-cut.png;  tools/cutout-specs/<key>.json may add {"keep": [[x,y],...]} polygons
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "src-images", "cutouts")


def clean_cut(im, session, close=25, nonwhite=235, keep_polys=()):
    from rembg import remove
    from PIL import ImageDraw
    out = remove(im, session=session, post_process_mask=False)
    a = (np.asarray(out.getchannel("A")) > 100).astype(np.uint8)
    h, w = a.shape
    for poly in keep_polys:                                # parts the model cannot see (a white box on white): traced by hand
        km = Image.new("L", (w, h), 0); ImageDraw.Draw(km).polygon([tuple(p) for p in poly], fill=255)
        a = np.maximum(a, (np.asarray(km) > 0).astype(np.uint8))
    inv = (1 - a).copy()
    m = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(inv, m, (0, 0), 2)                       # background reachable from the corner
    filled = (inv != 2).astype(np.uint8)                   # everything else is machine (holes filled)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close, close))
    closed = cv2.morphologyEx(filled, cv2.MORPH_CLOSE, k)
    rgb = np.asarray(im).astype(int)
    keep = (rgb.min(-1) < nonwhite) & (cv2.dilate(closed, k) > 0)
    closed = np.maximum(closed, keep.astype(np.uint8))
    alpha = np.clip(cv2.GaussianBlur(closed.astype(np.float32), (0, 0), 1.0), 0, 1)
    res = Image.fromarray(np.dstack([np.asarray(im), (alpha * 255).astype(np.uint8)]), "RGBA")
    bbox = res.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    return res.crop(bbox) if bbox else res


def main():
    from rembg import new_session
    session = new_session("isnet-general-use")
    os.makedirs(OUT, exist_ok=True)
    for key in [k for k in sys.argv[1:] if not k.startswith("--")]:
        src = os.path.join(ROOT, "tools", "src-images", "value-line", key + ".png")
        spec = os.path.join(ROOT, "tools", "cutout-specs", key + ".json")   # optional {"keep": [[poly], ...]}
        keep = json.load(open(spec)).get("keep", []) if os.path.exists(spec) else []
        res = clean_cut(Image.open(src).convert("RGB"), session, keep_polys=keep)
        out = os.path.join(OUT, key + "-cut.png")
        res.save(out)
        print(key, res.size, "->", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
