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


def is_white_background(im, thr=228, neutral=18, ring_frac=0.012):
    """Does this photo sit on a plain white studio background?  Judged from a thin ring along the
    border: most of it must be near-white and neutral, and at least three corners white.  Returns
    (yes, level) where level is the median brightness of the white border — the thresholds of
    cutout() are set relative to it.  Photos with a real scene (factory floor, showroom) come back
    False; a studio photo whose machine touches the frame can be forced with "cutout": true in
    tools/image_map.json."""
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    H, W = a.shape[:2]
    r = max(2, int(round(min(H, W) * ring_frac)))
    mn, mx = a.min(-1), a.max(-1)
    white = (mn >= thr) & ((mx - mn) <= neutral)
    ring = np.zeros((H, W), bool)
    ring[:r] = True; ring[-r:] = True; ring[:, :r] = True; ring[:, -r:] = True
    frac = float(white[ring].mean())
    level = int(np.median(mn[ring & white])) if (ring & white).any() else 255
    corners = sum(float(white[ys, xs].mean()) >= 0.7 for ys, xs in [
        (slice(0, r), slice(0, r)), (slice(0, r), slice(-r, None)),
        (slice(-r, None), slice(0, r)), (slice(-r, None), slice(-r, None))])
    return (frac >= 0.6 and corners >= 3), level


def light_edge_fraction(rgba):
    """Share of the cut-out's edge pixels (inside, next to the transparent area) that are light and
    neutral.  Dark or coloured machines score near 0; a machine with white / cream covers that the
    normal thresholds have started to eat scores well above 0.05."""
    a = np.asarray(rgba.convert("RGBA")).astype(np.int16)
    al, rgb = a[..., 3], a[..., :3]
    opaque, transp = (al > 200), (al < 30).astype(np.uint8)
    band = opaque & (cv2.dilate(transp, np.ones((9, 9), np.uint8)) > 0)
    if not band.any():
        return 0.0
    mn, mx = rgb.min(-1), rgb.max(-1)
    light = (mn >= 210) & ((mx - mn) <= 20)
    return float(light[band].mean())


def auto_cutout(im, level=255, shadow_thr=205, light_limit=0.05, drop_shadow=False):
    """Cut-out with thresholds relative to the measured background brightness; the floor shadow
    is kept as translucent black so the machine still 'stands' on a coloured background.
    Machines with white or cream covers are detected after a first pass (light_edge_fraction) and
    cut again with strict thresholds that only remove the real background (background within
    4 levels of pure white), so the covers keep their edges."""
    res = cutout(im, border_thr=min(232, level - 8), hole_thr=min(247, level + 4), hole_area=200, shadow_thr=shadow_thr,
                 drop_shadow=drop_shadow)
    if light_edge_fraction(res) > light_limit:
        res = cutout(im, border_thr=level - 4, hole_thr=level - 1, hole_area=400, neutral=12, shadow_thr=None,
                     edge_hi=level - 2, edge_lo=level - 14, band_light=level - 6, drop_shadow=drop_shadow)
        res.info["strict"] = True
    return res


def cutout(im, border_thr=232, hole_thr=247, hole_area=200, neutral=16, keep_alpha=True, margin=6, shadow_thr=None,
           edge_hi=252.0, edge_lo=190.0, band_light=200, drop_shadow=False):
    """drop_shadow=True removes the photographed floor shadow completely (for heroes on the orange band,
    which get a drawn shadow from tools/hero_shadow.py instead of the grey smear)."""
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
    light_neutral = neutral_mask & (mn > band_light)
    shadow |= band & light_neutral          # light grey edge pixels are background + shadow, not machine
    edge = band & ~shadow
    alpha[edge] = np.clip((edge_hi - mn[edge]) / (edge_hi - edge_lo), 0, 1)
    alpha[shadow] = 0.0 if drop_shadow else np.clip((255.0 - mn[shadow]) / 255.0 * 1.15, 0, 1)
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
