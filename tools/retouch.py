#!/usr/bin/env python3
"""Photo retouching helpers for the product pipeline."""
import cv2
import numpy as np
from PIL import Image


def clean_patch(img, polygon, ring=10, feather=1.2, tol=38):
    """Remove a label from a flat painted panel: fill the polygon with a smooth colour plane
    fitted to the ring of panel pixels around it (outliers such as handles, edges and shadows are
    ignored), add the panel's own grain and feather the edge. RGB or RGBA in, same mode out."""
    mode = img.mode
    arr = np.asarray(img.convert("RGBA")).astype(np.float32)
    H, W = arr.shape[:2]
    mask = np.zeros((H, W), np.uint8)
    cv2.fillPoly(mask, [np.array(polygon, np.int32)], 255)
    k = np.ones((ring * 2 + 1, ring * 2 + 1), np.uint8)
    ringmask = (cv2.dilate(mask, k) > 0) & (mask == 0) & (arr[..., 3] > 200)
    ys, xs = np.nonzero(ringmask)
    if len(ys) < 20:
        return img
    cols = arr[ys, xs, :3]
    lum = cols.mean(1)
    med = np.median(lum)
    sat = cols.max(1) - cols.min(1)
    keep = (np.abs(lum - med) < tol) & (sat <= np.median(sat) + 25)   # drop coloured pixels (red labels etc.) around a grey panel
    if keep.sum() < 20:
        keep = np.abs(lum - med) < tol * 2
    ys, xs, cols = ys[keep], xs[keep], cols[keep]
    A = np.stack([np.ones_like(xs, np.float32), xs.astype(np.float32), ys.astype(np.float32)], 1)
    coef, *_ = np.linalg.lstsq(A, cols, rcond=None)          # 3 x 3 (a, bx, by per channel)
    resid = cols - A @ coef
    noise = float(np.clip(resid.std(), 0.6, 4.0))
    my, mx = np.nonzero(mask)
    Am = np.stack([np.ones_like(mx, np.float32), mx.astype(np.float32), my.astype(np.float32)], 1)
    fill = Am @ coef
    rng = np.random.default_rng(3)
    fill = fill + rng.normal(0, noise, fill.shape).astype(np.float32)
    patch = arr[..., :3].copy()
    patch[my, mx] = np.clip(fill, 0, 255)
    patch = cv2.GaussianBlur(patch, (0, 0), 0.6)              # match photo softness inside the patch
    soft = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (0, 0), feather)[..., None]
    out = arr.copy()
    out[..., :3] = arr[..., :3] * (1 - soft) + patch * soft
    res = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
    return res if mode == "RGBA" else res.convert(mode)
