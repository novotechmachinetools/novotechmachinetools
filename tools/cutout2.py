#!/usr/bin/env python3
"""Clean cut-out of a product photo shot on a white studio background → PNG with alpha.

Compared with tools/cutout.py: also removes the white background seen *through* the machine
(enclosed holes), anti-aliases the edge from the real pixel whiteness and removes the white
fringe (colour decontamination), so the cut-out sits cleanly on a coloured background.

    python3 -I tools/cutout2.py <src.jpg|png> <out.png> [--border 232] [--hole 247] [--hole-area 200]
    (an RGBA source keeps its own alpha and only gets hole removal + edge clean-up)
"""
import sys

import cv2
import numpy as np
from PIL import Image


def cutout(im, border_thr=232, hole_thr=247, hole_area=200, neutral=16, keep_alpha=True, margin=6, shadow_thr=None):
    rgba = im.convert("RGBA")
    arr = np.asarray(rgba).astype(np.float32)
    rgb, a0 = arr[..., :3], arr[..., 3]
    mn, mx = rgb.min(-1), rgb.max(-1)
    neutral_mask = (mx - mn) <= neutral
    H, W = mn.shape
    # --- hard background: near-white components touching the border, plus very white enclosed components
    cand = ((mn >= border_thr) & neutral_mask).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(cand, connectivity=8)
    bg = np.zeros((H, W), bool)
    border_labels = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        comp = lab == i
        if i in border_labels:
            bg |= comp
        elif area >= hole_area and mn[comp].mean() >= hole_thr:
            bg |= comp
    if keep_alpha and a0.min() < 255:
        bg |= a0 < 8
    alpha = np.where(bg, 0.0, 1.0).astype(np.float32)
    shadow = np.zeros_like(bg)
    if shadow_thr:
        # light neutral pixels touching the background in the bottom quarter of the object = the floor
        # shadow: keep it as translucent black (opacity from its darkness) instead of an opaque grey smear
        cand2 = ((mn >= shadow_thr) & neutral_mask & ~bg).astype(np.uint8)
        ys_obj = np.where((~bg).any(1))[0]
        if len(ys_obj):
            cand2[: int(ys_obj.min() + 0.75 * (ys_obj.max() - ys_obj.min()))] = 0
        grow = cv2.dilate(bg.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        n2, lab2 = cv2.connectedComponents(cand2, connectivity=8)
        touch = set(np.unique(lab2[grow & (cand2 > 0)])) - {0}
        if touch:
            shadow = np.isin(lab2, list(touch))
    # --- soft edge in a band around the hard edge
    k = np.ones((5, 5), np.uint8)
    band = (cv2.dilate(bg.astype(np.uint8), k) > 0) & (cv2.erode(bg.astype(np.uint8), k) == 0) & ~bg
    light_neutral = neutral_mask & (mn > 200)
    shadow |= band & light_neutral          # light grey edge pixels are background + shadow, not machine
    edge = band & ~shadow
    alpha[edge] = np.clip((252.0 - mn[edge]) / (252.0 - 190.0), 0, 1)
    alpha[shadow] = np.clip((255.0 - mn[shadow]) / 255.0 * 1.15, 0, 1)
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.5)
    alpha = np.clip(alpha, 0, 1)
    # --- colours: decontaminate machine edge pixels (remove the white mixed in); shadows become black
    out = rgb.copy()
    sel = edge & (alpha > 0.02) & (alpha < 0.98)
    aa = alpha[sel][:, None]
    out[sel] = np.clip((rgb[sel] - (1 - aa) * 255.0) / np.maximum(aa, 0.05), 0, 255)
    out[shadow] = 18.0
    out[alpha <= 0.02] = 255
    res = np.dstack([out, alpha * 255]).astype(np.uint8)
    img = Image.fromarray(res, "RGBA")
    bbox = Image.fromarray((alpha * 255).astype(np.uint8)).point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox:
        img = img.crop((max(0, bbox[0] - margin), max(0, bbox[1] - margin), min(W, bbox[2] + margin), min(H, bbox[3] + margin)))
    return img


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = {sys.argv[i].lstrip("-"): float(sys.argv[i + 1]) for i in range(1, len(sys.argv) - 1) if sys.argv[i].startswith("--")}
    src, out = args[0], args[1]
    img = cutout(Image.open(src), border_thr=opts.get("border", 232), hole_thr=opts.get("hole", 247), hole_area=int(opts.get("hole-area", 200)))
    img.save(out, "PNG")
    print(out, img.size)
