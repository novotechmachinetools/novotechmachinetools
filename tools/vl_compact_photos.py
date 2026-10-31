#!/usr/bin/env python3
"""Photos of the value-line compact press brakes — WAD-50T/1300, WAD-50T/1600 (CNC) and WC67K-30T/1600 (NC) — from the
supplier's web shop product pages (Oct 28 2026) and its WADE quotation document: the supplier's name on the machine and on
labels is painted out with LaMa (tools/lama_inpaint.py), because the machines are sold under NovoTech's name; the three
machine photos are cut out by BiRefNet in tools/make_images.py, the detail photos stay rectangular.

    python3 tools/vl_compact_photos.py [key …]        → tools/src-images/value-compact/<key>.jpg + image_map entries
    python3 tools/make_images.py --only $(cat tools/vl_compact_keys.txt)
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "tools", "src-images", "value-compact")
SRC = os.path.join(D, "src")
SECTION = "value-compact"

# key: dict(src, alt, boxes=[(x0, y0, x1, y1)] painted out, cutout=True for BiRefNet)
PHOTOS = {
    # ---- WAD-50T/1600 (shop photos 1,099 px)
    "vl-cp-wad1600": dict(src="ZHUTU-3.webp", cutout=True, boxes=[(355, 112, 475, 165)], alt="NovoTech WAD-50T/1600 compact CNC press brake, 55 US tons × 5.2 ft, with Delem control"),
    "vl-cp-clamps": dict(src="2-4.webp", alt="Segmented top-tool holders with the quick-release clamps of the compact CNC press brake"),
    "vl-cp-backgauge": dict(src="3-4.webp", alt="X-R back gauge of the compact CNC press brake on linear guides and ball screw, with the cable chain"),
    "vl-cp-laser": dict(src="4-3.webp", boxes=[(505, 935, 615, 1010)], alt="DSP laser finger-protection receiver on the compact CNC press brake"),
    "vl-cp-servo": dict(src="5-3.webp", alt="Servo motor of the back gauge axis"),
    "vl-cp-fingers": dict(src="6-3.webp", alt="Back gauge fingers on linear guides with the four-step stops"),
    "vl-cp-pump-motor": dict(src="7-1.webp", alt="Servo main motor on the pump — the pump turns only while the ram moves"),
    "vl-cp-hawe": dict(src="8-1.webp", alt="Proportional valve regulation in the electrical cabinet"),
    "vl-cp-valve": dict(src="9-2.webp", alt="Hydraulic valve block with pressure gauge"),
    # ---- WAD-50T/1300
    "vl-cp-wad1300": dict(src="ZHUTU-2.webp", cutout=True, alt="NovoTech WAD-50T/1300 compact CNC press brake, 55 US tons × 4.3 ft"),
    "vl-cp-clamps-2": dict(src="1-3.webp", alt="Top-tool holders along the ram of the compact CNC press brake"),
    "vl-cp-rear": dict(src="3-3.webp", alt="Compact CNC press brake from the rear: enclosed rear guard, electrical cabinet and hydraulic unit"),
    "vl-cp-hydraulics": dict(src="4-2.webp", alt="Hydraulic unit with filter and pump motor of the compact CNC press brake"),
    "vl-cp-finger-drive": dict(src="5-2.webp", alt="Back gauge drive with servo motor, ball screw and cable chain"),
    "vl-cp-fingers-2": dict(src="6-2.webp", alt="Two back gauge fingers on the linear guide of the compact CNC press brake"),
    # ---- WC67K-30T/1600 (NC)
    "vl-cp-wc67k": dict(src="ZHUTU-24.webp", cutout=True, alt="NovoTech WC67K-30T/1600 compact NC torsion-bar press brake, 33 US tons × 5.2 ft"),
    "vl-cp-e21": dict(src="1-28.webp", alt="Estun E21PS NC control of the WC67K compact press brake"),
    "vl-cp-nc-screw": dict(src="2-29.webp", alt="Back gauge lead screw and hand wheel of the WC67K NC press brake"),
    "vl-cp-nc-valve": dict(src="3-27.webp", alt="Hydraulic valve block with pressure gauge and overload valve of the WC67K"),
    # ---- from the WADE quotation document (800 × 600)
    "vl-cp-front-supports": dict(src="wade-front-supports.png", alt="Front support arms on the linear rail of the compact CNC press brake"),
    "vl-cp-rear-gauge": dict(src="wade-rear-gauge.png", alt="Back gauge beam and fingers seen from the rear of the compact CNC press brake"),
    "vl-cp-cabinet": dict(src="wade-cabinet.png", alt="Electrical cabinet with Schneider components of the compact CNC press brake"),
}


def process(key):
    from lama_inpaint import inpaint
    p = PHOTOS[key]
    im = Image.open(os.path.join(SRC, p["src"])).convert("RGB")
    if p.get("boxes"):
        rgb = np.asarray(im).copy()
        mask = np.zeros(rgb.shape[:2], np.uint8)
        for x0, y0, x1, y1 in p["boxes"]:
            mask[y0:y1, x0:x1] = 255
        im = Image.fromarray(inpaint(rgb, mask))
    if max(im.size) < 900:
        from esrgan import upscale
        im = upscale(im)
    os.makedirs(D, exist_ok=True)
    path = os.path.join(D, key + ".jpg")
    im.save(path, quality=92)
    return path, im.size


def register():
    """image_map entries for every exported photo (section value-compact) and the key list for make_images"""
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    for key, p in PHOTOS.items():
        if not os.path.exists(os.path.join(D, key + ".jpg")):
            print("!! missing export for", key)
            continue
        imap[key] = {"src": f"tools/src-images/{SECTION}/{key}.jpg", "alt": p["alt"], "section": SECTION, "trim": False, "quality": 82, "cutout": bool(p.get("cutout"))}
        if os.path.exists(os.path.join(ROOT, "tools", "cutout-specs", "birefnet", key + ".json")):   # keep / drop polygons for a cut BiRefNet gets wrong
            imap[key]["cut_spec"] = f"tools/cutout-specs/birefnet/{key}.json"
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "vl_compact_keys.txt"), "w").write(",".join(keys))
    return keys


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--register" not in sys.argv:
        for k in keys or list(PHOTOS):
            path, size = process(k)
            print(f"{k:24s} {size} -> {os.path.relpath(path, ROOT)}")
    print("registered:", len(register()))


if __name__ == "__main__":
    main()
