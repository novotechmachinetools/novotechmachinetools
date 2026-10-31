#!/usr/bin/env python3
"""NC torsion-bar press brake (value line): the supplier's factory photos of a 200/3200 NC press brake with the optional
Estun E315PS control, sent by the owner on Oct 31 2026 as side photos for the NC gallery — kept as photos, no cut-outs.

The originals (2,576 × 1,717) sit in /home/claude/nc-photos/<key>.jpg.  The value line is sold under NovoTech's name, so
the supplier's logo on the ram and the supplier's ring logos on the wrapped machines in the background are filled with
LaMa (tools/lama_inpaint.py), one box at a time.

    python3 tools/nc_photos.py [key …]     → tools/src-images/value-nc/<key>.jpg and the tools/image_map.json entries
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/nc-photos/"
DST = os.path.join(ROOT, "tools", "src-images", "value-nc")
BIG = 1800


def P(alt, boxes=()):
    return dict(alt=alt, boxes=list(boxes))


PHOTOS = {
    "vl-nc-front": P("NC hydraulic press brake 200/3200: 220 US tons (200 t) × 10.5 ft, with the optional Estun E315PS touch control on its "
                     "swing arm, the front support arms and the foot pedal", [(808, 176, 984, 251)]),
    "vl-nc-34": P("The 200/3200 NC press brake from the right: the side guards, the front support arms and the Estun E315PS control",
                  [(806, 270, 942, 347)]),
    "vl-nc-34b": P("The 200/3200 NC press brake from the left, with the tool clamps along the ram and the foot pedal on its stand",
                   [(864, 320, 988, 396)]),
    "vl-nc-34c": P("The 200/3200 NC press brake from the front, with the right side guard open", [(1060, 153, 1228, 239)]),
    "vl-nc-rear": P("From the rear: the main motor and pump on top of the frame, the electrical cabinet and the rear guard doors",
                    [(316, 650, 374, 724), (484, 650, 554, 732)]),
    "vl-nc-crowning": P("Manual crowning: the hand crank and chain at the end of the table set the crowning wedges under the die holder"),
}


def process(key):
    from lama_inpaint import inpaint
    p = PHOTOS[key]
    rgb = np.asarray(Image.open(SRC + key + ".jpg").convert("RGB")).copy()
    for x0, y0, x1, y1 in p["boxes"]:
        m = np.zeros(rgb.shape[:2], np.uint8)
        m[y0:y1, x0:x1] = 255
        rgb = inpaint(rgb, m)
    im = Image.fromarray(rgb)
    if max(im.size) > BIG:
        f = BIG / max(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    os.makedirs(DST, exist_ok=True)
    im.save(os.path.join(DST, key + ".jpg"), quality=92)
    return im.size


def register(keys):
    path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(path, encoding="utf-8"))
    for k in keys:
        imap[k] = {"src": f"tools/src-images/value-nc/{k}.jpg", "alt": PHOTOS[k]["alt"], "section": "value-sheet", "trim": False,
                   "quality": 82, "cutout": False}
    json.dump(imap, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for k in keys:
        print(f"{k:16s} {process(k)}", flush=True)
    register(keys)


if __name__ == "__main__":
    main()
