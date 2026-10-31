#!/usr/bin/env python3
"""WAD CNC hydraulic press brake: the supplier's factory photo set of the WAD 110T/3200 (Delem DA-53T, 4+1 axes), sent by the
owner on Oct 31 2026 as side / detail photos for the WAD gallery — kept as photos, no cut-outs.

The originals (6,720 × 4,480 JPEGs, extracted outside the repository) were downscaled to 2,400 px as
/home/claude/wad-photos/<key>.jpg (source file in the comment of each entry).  The value line is sold under NovoTech's
name, so the supplier's logo on the ram, the force chart that carries it and the supplier's name on machines in the
background are filled with LaMa (tools/lama_inpaint.py), one box at a time so each fill keeps full resolution.  The
valve maker's logo on the valve label is removed from its dark strokes only (no valve maker names on value-line pages),
and the Chinese warning sticker in the valve photo is cropped off.

    python3 tools/wad_photos.py [key …]     → tools/src-images/value-wad/<key>.jpg and the tools/image_map.json entries
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/wad-photos/"
DST = os.path.join(ROOT, "tools", "src-images", "value-wad")
BIG = 1800


def P(alt, boxes=(), strokes=(), crop=None):
    return dict(alt=alt, boxes=list(boxes), strokes=list(strokes), crop=crop)


# key: alt / caption; boxes (x0, y0, x1, y1 in the 2,400 px source) filled by LaMa; strokes = polygons inside which only the
# dark text strokes are filled (a printed label keeps its blank face); crop applied after the fills
PHOTOS = {
    "vl-wad-front": P("WAD 110T/3200 CNC hydraulic press brake: 10 ft × 121 US tons, with the Delem DA-53Tx on its swing arm, the front "
                      "support arms and the foot pedal",                                                   # 101A0826
                      [(728, 158, 978, 415), (708, 622, 895, 750), (190, 564, 224, 584)]),
    "vl-wad-34": P("WAD 110T/3200 from the side: the Delem control on its swing arm, the hinged side guards and the electrical cabinet",
                   [(795, 350, 955, 548), (795, 690, 905, 800), (120, 804, 172, 832), (426, 836, 476, 862)]),   # 101A0829
    "vl-wad-side": P("Side frame of the WAD with the hinged side guard and its window",                   # 101A0832
                     [(130, 398, 210, 460), (2036, 771, 2082, 787)]),
    "vl-wad-arm": P("Front sheet support arm sliding on a linear rail along the bed"),                     # 101A0783
    "vl-wad-pedal": P("Foot pedal on a movable stand, with the emergency stop on top"),                   # 101A0791
    "vl-wad-bg-beam": P("Back gauge from the rear: the beam with a stop finger on its linear rail, and the X-axis ball screw and "
                        "linear guide that move it front to back"),                                       # 101A0846
    "vl-wad-bg-rear": P("X-axis drive behind the frame: one servo motor and a timing belt turn the ball screws on both sides "
                        "together, so the back gauge beam stays parallel"),                               # 101A0848
    "vl-wad-bg-chain": P("Back gauge from the side: the X-axis carriage on its ball screw and linear guide, with the cable chain "
                         "that follows the beam"),                                                        # 101A0849
    "vl-wad-finger": P("Back gauge stop finger: it slides along the beam on a linear rail and locks with the knob"),   # 101A0854
    "vl-wad-throat": P("Throat in the side frame: a flange can pass into it when the part is longer than the distance between "
                       "the frames"),                                                                     # 101A8022
    "vl-wad-valve-top": P("Valve block on top of a ram cylinder, inside the top cover",                   # 101A0862
                          strokes=[[(1036, 768), (1057, 758), (1093, 783), (1133, 836), (1126, 844), (1081, 833), (1038, 776)]],
                          crop=(120, 90, 2280, 1290)),
    "vl-wad-servo": P("Servo motor and pump of the mild-hybrid drive, with the oil filter: the servo motor turns the pump only while "
                     "the ram moves and stops it while the machine waits, loads or unloads — that is where the mild hybrid's "
                     "gains come from: 40 – 60 % less energy, oil 18 – 36 °F (10 – 20 °C) cooler, a quieter shop (about 60 dB, "
                     "silent while the ram waits) and longer life for the pump, seals and valves"),     # 101A0840
    "vl-wad-crown-motor": P("Crowning motor at the end of the bed: the control sets the crowning wedges for each bend"),   # 101A0792
    "vl-wad-cabinet": P("Electrical cabinet on the side of the machine, door open", [(2020, 398, 2070, 448)]),   # 101A0797
    "vl-wad-cabinet-in": P("Inside the electrical cabinet: the main switch, the two servo drives of the back gauge axes and the "
                           "drive of the main hydraulic motor"),                                          # 101A0803
}


def fill(rgb, mask):
    from lama_inpaint import inpaint
    return inpaint(rgb, mask)


def process(key):
    import cv2
    p = PHOTOS[key]
    rgb = np.asarray(Image.open(SRC + key + ".jpg").convert("RGB")).copy()
    H, W = rgb.shape[:2]
    for x0, y0, x1, y1 in p["boxes"]:
        m = np.zeros((H, W), np.uint8)
        m[y0:y1, x0:x1] = 255
        rgb = fill(rgb, m)
    for poly in p["strokes"]:
        inside = Image.new("L", (W, H), 0)
        ImageDraw.Draw(inside).polygon(poly, fill=255)
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        m = ((np.asarray(inside) > 0) & (gray < 205)).astype(np.uint8) * 255
        m = cv2.dilate(m, np.ones((5, 5), np.uint8))
        rgb = fill(rgb, m)
    im = Image.fromarray(rgb)
    if p["crop"]:
        im = im.crop(p["crop"])
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
        imap[k] = {"src": f"tools/src-images/value-wad/{k}.jpg", "alt": PHOTOS[k]["alt"], "section": "value-sheet", "trim": False,
                   "quality": 82, "cutout": False}
    json.dump(imap, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for k in keys:
        print(f"{k:20s} {process(k)}", flush=True)
    register(keys)


if __name__ == "__main__":
    main()
