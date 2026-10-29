#!/usr/bin/env python3
"""Photos of the Dener XL 1560 compact press brake (the owner's set of Oct 28 2026, 1600 × 1200, from a dealer's showroom):
the dealer's watermark across the middle of every photo, the dealer's name plate under the Dener logo, the Turkish warning
stickers and the neighbouring machines are painted out with LaMa (tools/lama_inpaint.py); the machine and the control pendant
are then cut out by BiRefNet in tools/make_images.py (`cutout`), the detail photos stay rectangular.

    python3 tools/dener_xl1560_photos.py [key …]      → tools/src-images/dener-xl1560/<key>.jpg   (raw photos in raw/)
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "tools", "src-images", "dener-xl1560")
RAW = os.path.join(D, "raw")
WM_MASK = os.path.join(D, "wm_mask.png")          # the watermark lettering, same place in every photo (from control.jpg)

# key: dict(src, alt, boxes=[(x0, y0, x1, y1)] painted out besides the watermark, cutout=True for BiRefNet)
PHOTOS = {
    "dn-xl1560-front": dict(src="front.jpg", cutout=True, alt="Dener XL 1560 compact CNC press brake, 66 US tons × 5 ft, front view with ESA S640 control",
                            boxes=[(688, 296, 786, 338), (0, 440, 250, 1000), (1480, 500, 1600, 1000)]),
    "dn-xl1560-left": dict(src="angle-left.jpg", cutout=True, alt="Dener XL 1560 press brake from the left: Y1 / Y2 ram cylinders, DSP laser guards and the ESA control pendant",
                           boxes=[(754, 273, 839, 306), (1365, 230, 1600, 930), (1340, 230, 1365, 465), (1340, 785, 1365, 930)]),
    "dn-xl1560-right": dict(src="angle-right.jpg", cutout=True, alt="Dener XL 1560 press brake from the right with the ESA S640 control on its swing arm",
                            boxes=[(642, 302, 714, 338), (0, 440, 470, 960)]),
    "dn-xl1560-control": dict(src="control.jpg", cutout=True, alt="ESA S640 15″ touch-screen control on the Dener XL 1560 — start, stop, muting lamp and general reset",
                              boxes=[(418, 852, 596, 1046)]),
    "dn-xl1560-tooling": dict(src="tooling-left.jpg", cutout=False, alt="EUROSTAMP punch 1281 in the segmented holders, 4-way die and DSP laser transmitter on the XL 1560"),
    "dn-xl1560-tooling-2": dict(src="tooling-right.jpg", cutout=False, alt="Segmented top-tool holders, EUROSTAMP tooling, front supports and the DSP laser receiver on the XL 1560"),
    "dn-xl1560-backgauge": dict(src="backgauge.jpg", cutout=False, alt="X-axis back gauge of the XL 1560 on its ball screw with two fingers and the servo drive",
                                boxes=[(975, 948, 1115, 1092)]),
    "dn-xl1560-backgauge-2": dict(src="backgauge-side.jpg", cutout=False, alt="Back gauge beam, fingers and rear sheet support of the XL 1560 seen through the side frame"),
}


def process(key):
    from lama_inpaint import inpaint
    p = PHOTOS[key]
    im = Image.open(os.path.join(RAW, p["src"])).convert("RGB")
    rgb = np.asarray(im).copy()
    mask = np.asarray(Image.open(WM_MASK).convert("L")).copy()
    for x0, y0, x1, y1 in p.get("boxes", []):
        mask[y0:y1, x0:x1] = 255
    out = Image.fromarray(inpaint(rgb, mask))
    os.makedirs(D, exist_ok=True)
    path = os.path.join(D, key + ".jpg")
    out.save(path, quality=93)
    return path, out.size


def register():
    """image_map entries (section dener-xl1560) and the key list for make_images"""
    import json
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    for key, p in PHOTOS.items():
        if not os.path.exists(os.path.join(D, key + ".jpg")):
            print("!! missing export for", key)
            continue
        imap[key] = {"src": f"tools/src-images/dener-xl1560/{key}.jpg", "alt": p["alt"], "section": "dener-xl1560", "trim": False, "quality": 82, "cutout": bool(p.get("cutout"))}
        if os.path.exists(os.path.join(ROOT, "tools", "cutout-specs", "birefnet", key + ".json")):   # keep / drop polygons for a cut BiRefNet gets wrong
            imap[key]["cut_spec"] = f"tools/cutout-specs/birefnet/{key}.json"
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "dener_xl1560_keys.txt"), "w").write(",".join(keys))
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
