#!/usr/bin/env python3
"""Blue paint → NovoTech grey on the TTMC value-line photos (the owner, Nov 10 2026: "every TTMC photo that is blue and white
becomes grey and white, the grey of the RBM 50").

The blue paint is found by hue (about 190 – 235°, fading out to 175 / 250°), saturation and brightness, softly, so painted
edges blend.  Each blue pixel keeps its own light and shade: its brightness relative to the average brightness of the
paint in that photo is applied to the target grey (sampled from the RBM 50 photo), so a highlight stays a highlight and
a shadow a shadow.  The white covers, black rolls, yellow pedals and red buttons are not touched; a faint blue cast left
on a highlight or a reflection (low saturation) loses its colour but keeps its brightness.  A cut-out (RGBA) is
recoloured inside its outline only; a detail photo with a background is recoloured whole.

    tools/make_images.py applies it to every key with "recolor": "grey" in tools/image_map.json.
    python3 tools/recolor_grey.py IN OUT [IN OUT …]       (a quick test on single files)
"""
import sys

import numpy as np
from PIL import Image

TARGET = np.array([68.0, 70.0, 74.0])                     # RBM 50 base grey (tm-rbm50, sampled Nov 10 2026)
LUMA = np.array([0.299, 0.587, 0.114])
TL = float(TARGET @ LUMA)


def _hsv(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1)
    d = np.maximum(mx - mn, 1e-6)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return hue, sat, mx


def paint_weight(rgb):
    """0 – 1: how much a pixel is blue paint (rgb in 0 – 1)."""
    hue, sat, val = _hsv(rgb)
    hw = np.clip(np.minimum((hue - 175) / 15, (250 - hue) / 15), 0, 1)
    sw = np.clip((sat - 0.20) / 0.22, 0, 1)
    vw = np.clip((val - 0.10) / 0.10, 0, 1)                # near-black pixels: hue is noise, nothing to change
    return hw * sw * vw, hw, sat


def blue_share(im):
    """share of the (opaque) photo that is blue paint — used to pick the photos"""
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    w, _, _ = paint_weight(a[..., :3] / 255)
    op = a[..., 3] > 128
    return float((w > 0.5)[op].mean()) if op.any() else 0.0


def blue_to_grey(im, min_pixels=150):
    """the photo with its blue paint turned into the RBM 50 grey (same mode as given)"""
    mode = im.mode
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb = a[..., :3] / 255
    inside = a[..., 3] > 0
    w, hw, sat = paint_weight(rgb)
    w = w * inside
    lum = (a[..., :3] @ LUMA)
    core = (w > 0.85)
    if core.sum() < min_pixels:
        return im
    lmean = float(lum[core].mean())
    grey = (lum * (TL / lmean))[..., None] * (TARGET / TL)[None, None, :]
    out = a[..., :3] * (1 - w[..., None]) + np.clip(grey, 0, 255) * w[..., None]
    # what is left of a blue cast (highlights, reflections, blended edges): keep the brightness, drop the colour
    rest = hw * np.clip((sat - 0.04) / 0.10, 0, 1) * (1 - w) * inside
    if rest.any():
        l2 = out @ LUMA
        out = out * (1 - rest[..., None]) + l2[..., None] * rest[..., None]
    a[..., :3] = np.clip(out, 0, 255)
    res = Image.fromarray(a.round().astype(np.uint8), "RGBA")
    return res if mode == "RGBA" else res.convert(mode if mode in ("RGB", "L") else "RGB")


if __name__ == "__main__":
    args = sys.argv[1:]
    for src, dst in zip(args[0::2], args[1::2]):
        im = Image.open(src)
        print(dst, f"blue {blue_share(im):.3f}")
        blue_to_grey(im).save(dst)
