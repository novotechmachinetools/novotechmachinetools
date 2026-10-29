#!/usr/bin/env python3
"""Cut the Dener XL 1560 showroom photos out properly: Segment Anything picks the machine (prompted part by part,
so the shear next to it, the dealer's sign, the roller stand and the cable chain are never part of the mask) and
BiRefNet supplies the soft edge inside that selection.

    alpha = BiRefNet alpha inside dilate(SAM mask)   ∪   erode(SAM mask)      (+ a few hand keep/drop polygons)

Writes tools/src-images/dener-xl1560/<key>-cut.png (full-frame RGBA) and a check sheet on NovoTech orange in the
scratchpad.  tools/dener_xl1560_photos.py register() points the image_map at the PNG, so make_images uses the
alpha as it is (no second cut).

    python3 tools/xl1560_cut.py [key …]        (default: the three machine views)
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import sam_cut  # noqa: E402  (SAM ViT-B ONNX, rembg export; embeddings cached next to the photo)
from birefnet_cut import cut_rgba  # noqa: E402

SRC = os.path.join(ROOT, "tools", "src-images", "dener-xl1560")
SCRATCH = "/tmp/claude-0/-home-claude/c238f6cc-e8bd-5b1f-a645-cb18914b0540/scratchpad"


def P(*pts):
    return [list(p) for p in pts]


# SAM prompts per view, in SOURCE pixels (1600 × 1201).  "add" prompts are unioned, "sub" prompts subtracted.
# A prompt with "crop" runs SAM on that crop (higher resolution for a small part).
SPECS = {
    "dn-xl1560-right": dict(
        add=[
            dict(box=[485, 190, 1010, 1110], pos=P((750, 350), (700, 480), (760, 620), (750, 850), (620, 1000), (900, 700), (560, 300), (960, 420)),
                 neg=P((890, 150), (1450, 400), (250, 700))),
            dict(box=[398, 525, 500, 940], pos=P((450, 700), (450, 850), (440, 600)), crop=[300, 450, 650, 1000]),       # left guard door
            dict(box=[985, 365, 1160, 1095], pos=P((1070, 700), (1100, 950), (1110, 450)), neg=P((1250, 900)), crop=[900, 300, 1400, 1150]),  # right guard door
            dict(box=[1030, 150, 1325, 735], pos=P((1170, 550), (1180, 250), (1060, 330), (1120, 180), (1250, 650)),
                 neg=P((1450, 500), (1250, 900), (1400, 300))),                                                           # pendant and arm
            dict(box=[478, 440, 506, 665], pos=P((491, 550), (491, 620)), crop=[400, 400, 700, 700]),                   # left light-curtain post
            dict(box=[598, 760, 790, 930], pos=P((650, 850), (745, 860)), crop=[550, 700, 850, 950]),                  # front sheet supports
        ],
        sub=[
            dict(box=[1135, 790, 1430, 1010], pos=P((1250, 900), (1350, 960)), crop=[1100, 750, 1500, 1050]),           # cable chain on the floor
            dict(box=[1150, 690, 1600, 1000], pos=P((1450, 800), (1300, 760))),                                          # roller stand behind
            dict(box=[778, 85, 1005, 240], pos=P((890, 150))),                                                           # dealer's sign
        ],
        drop=[[[0, 0], [478, 0], [478, 540], [424, 540], [421, 560], [405, 905], [398, 930], [398, 1201], [0, 1201]],    # the shear on the left, up to the door's slanted edge
              [[1330, 0], [1600, 0], [1600, 1201], [1330, 1201]],
              [[1135, 795], [1430, 795], [1430, 1010], [1135, 1010]],
              [[1068, 300], [1090, 240], [1120, 205], [1180, 205], [1182, 398], [1068, 398]]],                      # wall inside the arm
        drop_final=[[[770, 80], [1010, 80], [1010, 241], [1002, 241], [950, 203], [942, 202], [900, 215], [840, 234], [790, 241], [770, 245]],   # sign
                    [[1068, 300], [1090, 240], [1120, 205], [1180, 205], [1182, 398], [1068, 398]],
                    [[0, 0], [478, 0], [478, 540], [424, 540], [421, 560], [405, 905], [398, 930], [398, 1201], [0, 1201]],
                    [[452, 905], [484, 905], [484, 945], [452, 945]]],                                                 # floor between door and frame
        zones_final=[dict(poly=[[452, 548], [480, 548], [480, 903], [452, 903]], lum_gt=110)],                       # door side face kept, the dark gap behind it dropped
    ),
    "dn-xl1560-left": dict(
        add=[
            dict(box=[495, 160, 1065, 1085], pos=P((780, 300), (700, 500), (800, 700), (780, 900), (600, 1000), (1000, 450), (560, 250), (950, 600)),
                 neg=P((1040, 250), (1200, 500), (1500, 400), (250, 800))),
            dict(box=[355, 478, 495, 1045], pos=P((420, 700), (420, 900), (410, 560)), crop=[300, 420, 560, 1100]),            # left guard door
            dict(box=[1065, 535, 1140, 925], pos=P((1100, 700), (1100, 850)), crop=[1000, 480, 1200, 980]),                  # right guard door
            dict(box=[1190, 468, 1376, 655], pos=P((1280, 560), (1230, 620), (1340, 500)), neg=P((1392, 600), (1280, 750)), crop=[1150, 420, 1450, 720]),  # pendant
            dict(box=[1045, 318, 1300, 485], pos=P((1150, 332), (1270, 400), (1262, 460)), neg=P((1200, 500), (1150, 450)), crop=[1000, 280, 1350, 520]),  # arm
            dict(box=[493, 365, 528, 565], pos=P((510, 450), (510, 520)), crop=[450, 330, 600, 600]),                      # left light-curtain post
            dict(box=[1038, 425, 1065, 660], pos=P((1050, 500), (1050, 600)), crop=[980, 400, 1120, 700]),                 # right light-curtain post
            dict(box=[795, 725, 925, 885], pos=P((830, 760), (900, 800), (850, 860)), crop=[750, 700, 980, 920]),          # front sheet supports
        ],
        sub=[],
        drop=[[[0, 0], [200, 0], [200, 240], [0, 240]],                                                                    # Tevmak sign top left
              [[0, 240], [358, 240], [358, 1201], [0, 1201]],                                                              # roller stand on the left
              [[1372, 0], [1600, 0], [1600, 1201], [1372, 1201]],                                                          # the XL 3000 on the right
              [[1185, 656], [1372, 656], [1372, 1201], [1185, 1201]],                                                      # its guard door below the pendant
              [[1120, 352], [1249, 352], [1249, 466], [1195, 466], [1195, 642], [1120, 642]], [[1302, 352], [1372, 352], [1372, 466], [1302, 466]]],  # dark panel behind the arm
        drop_final=[[[0, 0], [200, 0], [200, 240], [0, 240]], [[0, 240], [358, 240], [358, 1201], [0, 1201]],
                    [[1372, 0], [1600, 0], [1600, 1201], [1372, 1201]], [[1185, 656], [1372, 656], [1372, 1201], [1185, 1201]],
                    [[1120, 352], [1249, 352], [1249, 466], [1195, 466], [1195, 642], [1120, 642]], [[1302, 352], [1372, 352], [1372, 466], [1302, 466]]],
    ),
    "dn-xl1560-front": dict(
        add=[
            dict(box=[492, 228, 1075, 1095], pos=P((780, 300), (780, 500), (780, 700), (780, 900), (600, 1000), (1000, 500), (560, 400), (1000, 900)),
                 neg=P((500, 150), (1450, 150), (150, 700), (1350, 800))),
            dict(box=[330, 535, 415, 1015], pos=P((370, 700), (370, 900), (360, 600)), crop=[280, 480, 500, 1060]),          # left guard door
            dict(box=[1135, 535, 1230, 1015], pos=P((1180, 700), (1180, 900), (1190, 600)), crop=[1080, 480, 1300, 1060]),   # right guard door
            dict(box=[436, 425, 478, 690], pos=P((455, 500), (455, 600), (452, 660)), crop=[380, 380, 560, 740]),           # left light-curtain post
            dict(box=[1080, 425, 1122, 690], pos=P((1100, 500), (1100, 600)), crop=[1020, 380, 1200, 740]),                 # right light-curtain post
            dict(box=[1235, 440, 1485, 705], pos=P((1360, 560), (1300, 650), (1440, 500)), neg=P((1550, 500), (1350, 780)), crop=[1200, 400, 1520, 760]),  # pendant
            dict(box=[1070, 228, 1400, 450], pos=P((1200, 250), (1360, 300), (1365, 420), (1090, 380)), neg=P((1200, 400), (1250, 150)), crop=[1040, 200, 1420, 470]),  # arm
            dict(box=[725, 795, 865, 945], pos=P((760, 830), (830, 840), (750, 920)), crop=[680, 760, 900, 980]),          # front sheet supports
        ],
        sub=[],
        drop=[[[0, 0], [330, 0], [330, 1201], [0, 1201]], [[1485, 0], [1600, 0], [1600, 1201], [1485, 1201]],              # shear left, XL 3000 right
              [[330, 0], [496, 0], [496, 440], [330, 440]], [[1075, 0], [1600, 0], [1600, 440], [1395, 440], [1395, 262], [1378, 248], [1362, 240], [1340, 235], [1100, 306], [1075, 330]],             # signs above / beside the frame
              [[1102, 338], [1330, 262], [1343, 262], [1343, 444], [1122, 444], [1122, 428], [1102, 428]],
              [[1075, 0], [1600, 0], [1600, 440], [1395, 440], [1395, 262], [1378, 248], [1362, 240], [1340, 235], [1100, 306], [1075, 330]],                                           # wall inside the arm loop
              [[1225, 708], [1485, 708], [1485, 1201], [1225, 1201]],                                                      # roller stand behind the pendant
              [[410, 1012], [497, 1012], [497, 1201], [410, 1201]], [[1070, 1012], [1140, 1012], [1140, 1201], [1070, 1201]],    # floor beside the base
              [[412, 692], [497, 692], [497, 1012], [412, 1012]], [[1072, 692], [1138, 692], [1138, 1012], [1072, 1012]],        # wall and floor between doors and frame
              [[496, 0], [640, 0], [640, 231], [496, 231]],                                                                    # hoist above the frame
              [[1102, 338], [1330, 262], [1343, 262], [1343, 444], [1122, 444], [1122, 428], [1102, 428]]],       # wall above the arm's bend
        keep_final=[[[497, 632], [1072, 632], [1072, 702], [497, 702]], [[497, 752], [1072, 752], [1072, 795], [497, 795]]],   # tool holders and die rows (nothing behind them)
        drop_final=[[[412, 692], [497, 692], [497, 1012], [412, 1012]], [[1072, 692], [1138, 692], [1138, 1012], [1072, 1012]],
                    [[496, 0], [640, 0], [640, 231], [496, 231]], [[1102, 338], [1330, 262], [1343, 262], [1343, 444], [1122, 444], [1122, 428], [1102, 428]],
                    [[0, 0], [330, 0], [330, 1201], [0, 1201]], [[1485, 0], [1600, 0], [1600, 1201], [1485, 1201]],
                    [[330, 0], [496, 0], [496, 440], [330, 440]], [[1075, 0], [1600, 0], [1600, 440], [1395, 440], [1395, 262], [1378, 248], [1362, 240], [1340, 235], [1100, 306], [1075, 330]], [[1102, 338], [1330, 262], [1343, 262], [1343, 444], [1122, 444], [1122, 428], [1102, 428]],
                    [[1075, 0], [1600, 0], [1600, 440], [1395, 440], [1395, 262], [1378, 248], [1362, 240], [1340, 235], [1100, 306], [1075, 330]], [[1225, 708], [1485, 708], [1485, 1201], [1225, 1201]],
                    [[410, 1012], [497, 1012], [497, 1201], [410, 1201]], [[1070, 1012], [1140, 1012], [1140, 1201], [1070, 1201]]],
    ),
}


def poly_mask(poly, W, H):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=255)
    return np.asarray(m) > 0


def sam_mask(img_path, spec, W, H):
    import onnxruntime as ort
    dec = ort.InferenceSession(sam_cut.DEC, providers=["CPUExecutionProvider"])
    mask = np.zeros((H, W), bool)
    for p in spec.get("add", []):
        mask |= sam_cut.masks_for(dec, img_path, H, W, p)
    for p in spec.get("sub", []):
        mask &= ~sam_cut.masks_for(dec, img_path, H, W, p)
    for poly in spec.get("keep", []):
        mask |= poly_mask(poly, W, H)
    for poly in spec.get("drop", []):
        mask &= ~poly_mask(poly, W, H)
    # small enclosed holes inside the machine are never background (big ones — the wall inside the pendant arm — are)
    a = mask.astype(np.uint8)
    inv = (1 - a).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(inv, connectivity=4)
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if area < spec.get("fill_holes_below", 10 ** 9) and x > 0 and y > 0 and x + w < W and y + h < H:
            a[lab == i] = 1
    # stray islands away from the machine
    n, lab, stats, _ = cv2.connectedComponentsWithStats(a, connectivity=8)
    if n > 2:
        big = 1 + int(np.argmax(stats[1:, 4]))
        for i in range(1, n):
            if i != big and stats[i][4] < 4000:
                a[lab == i] = 0
    return a.astype(bool)


def combine(bire, sam, dil=14, ero=6):
    """BiRefNet's soft alpha inside the (dilated) SAM selection, the eroded SAM selection fully opaque."""
    k = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    s = sam.astype(np.uint8)
    outer = cv2.dilate(s, k(dil)).astype(bool)
    inner = cv2.erode(s, k(ero)).astype(np.float32)
    inner = cv2.GaussianBlur(inner, (0, 0), 1.0)
    alpha = np.where(outer, bire, 0.0)
    return np.clip(np.maximum(alpha, inner), 0, 1)


def run(key, show=True):
    spec = SPECS[key]
    img_path = os.path.join(SRC, key + ".jpg")
    im = Image.open(img_path).convert("RGB"); W, H = im.size
    sam = sam_mask(img_path, spec, W, H)
    bire = np.asarray(cut_rgba(im, "1536", spec=None, cache_key=key).getchannel("A")).astype(np.float32) / 255.0
    alpha = combine(bire, sam, spec.get("dil", 14), spec.get("ero", 6))
    for poly in spec.get("keep_final", []):
        alpha = np.where(poly_mask(poly, W, H), 1.0, alpha)
    lum = np.asarray(im.convert("L")).astype(np.float32)
    for z in spec.get("zones_final", []):                     # inside the polygon: a plain luminance cut (door side face vs dark gap)
        inside = poly_mask(z["poly"], W, H)
        zm = np.zeros((H, W), bool)
        if "lum_gt" in z: zm |= lum > z["lum_gt"]
        if "lum_lt" in z: zm |= lum < z["lum_lt"]
        zf = cv2.GaussianBlur(zm.astype(np.float32), (0, 0), 0.8)
        alpha = np.where(inside, zf, alpha)
    for poly in spec.get("drop_final", []):                   # drops win over everything
        alpha = np.where(poly_mask(poly, W, H), 0.0, alpha)
    out = Image.fromarray(np.dstack([np.asarray(im), (alpha * 255).astype(np.uint8)]), "RGBA")
    out.save(os.path.join(SRC, key + "-cut.png"))
    if show:
        bg = Image.new("RGBA", out.size, (242, 138, 31, 255)); bg.alpha_composite(out)
        chk = bg.convert("RGB")
        # SAM selection outline for the check sheet
        cnts, _ = cv2.findContours(sam.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        arr = np.asarray(chk).copy(); cv2.drawContours(arr, cnts, -1, (0, 90, 255), 1)
        Image.fromarray(arr).save(os.path.join(SCRATCH, key + "-samcheck.jpg"), quality=88)
        chk.save(os.path.join(SCRATCH, key + "-check.jpg"), quality=90)
    print(key, "sam px", int(sam.sum()), "alpha>0.5 px", int((alpha > 0.5).sum()))


if __name__ == "__main__":
    for k in (sys.argv[1:] or ["dn-xl1560-right", "dn-xl1560-left", "dn-xl1560-front"]):
        run(k)
