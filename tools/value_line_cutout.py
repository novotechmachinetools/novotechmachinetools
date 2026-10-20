#!/usr/bin/env python3
"""Cut-outs of the NovoTech value-line product photos for the orange hero band.

The catalogue PDF cut-outs carry a soft mask with holes punched through the white/cream panels
(wherever the panel was nearly white). This repairs those holes — an enclosed transparent region
whose surroundings are light is a panel, a region surrounded by dark machine parts is a real
see-through hole — then runs the generic clean-up (tools/cutout2.py) for soft edges and shadows.

    python3 tools/value_line_cutout.py <key> [<key> ...]   e.g. nt-h13-1 → tools/src-images/cutouts/nt-h13-1-cut.png
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cutout2 import cutout  # noqa: E402
from value_line_images import JOBS, SRC  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "src-images", "cutouts")
NF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "src-images", "value-line")


def repair_holes(rgba_pdf, rgb_clean, light=215, ring=6):
    """rgba_pdf: the PDF cut-out (RGBA); rgb_clean: the flattened, label-free photo (RGB, same size)."""
    a = np.asarray(rgba_pdf)[..., 3]
    rgb = np.asarray(rgb_clean.convert("RGB")).astype(np.float32)
    H, W = a.shape
    transp = (a < 8).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(transp, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    alpha = a.astype(np.float32).copy()
    mn = rgb.min(-1)
    k = np.ones((ring * 2 + 1, ring * 2 + 1), np.uint8)
    for i in range(1, n):
        if i in border:
            continue
        comp = (lab == i).astype(np.uint8)
        ringmask = (cv2.dilate(comp, k) > 0) & (comp == 0) & (a > 200)
        if ringmask.sum() < 10:
            continue
        if np.median(mn[ringmask]) >= light:      # surrounded by a light panel → it is the panel
            alpha[comp > 0] = 255
    out = np.dstack([rgb, alpha]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def main():
    os.makedirs(OUT, exist_ok=True)
    for key in sys.argv[1:]:
        job = JOBS[key]
        pdf = Image.open(os.path.join(SRC, job["src"] + ".png")).convert("RGBA")
        clean = Image.open(os.path.join(NF, key + ".png"))
        fixed = repair_holes(pdf, clean)
        res = cutout(fixed, shadow_thr=None, keep_alpha=True)
        res.save(os.path.join(OUT, key + "-cut.png"))
        print(key, res.size)


if __name__ == "__main__":
    main()
