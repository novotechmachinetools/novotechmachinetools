#!/usr/bin/env python3
"""Remove supplier logos / nameplates from machine photos by inpainting rough boxes.

    from delogo import delogo
    delogo(img_pil, [(x0,y0,x1,y1), ...]) -> PIL image

Each box is a rough rectangle (source pixels) that contains the logo plus some clean background around it.
Inside the box the background colour is taken from the box border (median); every pixel that differs from
it by more than `thr` (plus a dilation) is inpainted (OpenCV Telea) and a little noise matching the border
texture is added so the patch does not look airbrushed.  `mode="all"` inpaints the whole box (for plates
sitting on a textured panel).
"""
import numpy as np
import cv2
from PIL import Image


def find_logo(rgb, box, margin=10):
    """Locate a printed logo / nameplate near a rough box: the connected blob of strong edges (text has a very high
    edge density compared with a painted panel) that is closest to the box centre, searched in a window twice the
    box size.  Returns a tight (x0, y0, x1, y1) with a margin, or None."""
    H, W = rgb.shape[:2]
    x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
    X0, Y0, X1, Y1 = max(0, x0 - bw), max(0, y0 - bh), min(W, x1 + bw), min(H, y1 + bh)
    g = cv2.cvtColor(rgb[Y0:Y1, X0:X1], cv2.COLOR_RGB2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.GaussianBlur(np.sqrt(gx * gx + gy * gy), (0, 0), 2.0)
    thr = max(40.0, float(np.percentile(mag, 97)) * 0.5)
    m = (mag > thr).astype(np.uint8)
    k = max(9, int(min(bw, bh) * 0.12)) | 1
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))
    n, lab, stats, cents = cv2.connectedComponentsWithStats(m, 8)
    cx, cy = (x0 + x1) / 2 - X0, (y0 + y1) / 2 - Y0
    best, best_score = None, None
    for i in range(1, n):
        lx, ly, lw, lh, la = stats[i]
        if la < 0.02 * bw * bh or lw > 2.5 * bw or lh > 2.5 * bh or lw < 8 or lh < 6:
            continue
        ccx, ccy = cents[i]
        dist = ((ccx - cx) / max(bw, 1)) ** 2 + ((ccy - cy) / max(bh, 1)) ** 2
        density = float(mag[lab == i].mean())
        score = dist - 0.002 * density
        if best is None or score < best_score:
            best, best_score = (lx, ly, lw, lh), score
    if best is None:
        return None
    lx, ly, lw, lh = best
    return (max(0, X0 + lx - margin), max(0, Y0 + ly - margin), min(W, X0 + lx + lw + margin), min(H, Y0 + ly + lh + margin))


def neighbour_fill(rgb, mask, origin, max_err=30.0, force=None):
    """Fill the bounding rectangle of `mask` (a patch-local mask; `origin` is the patch's position in rgb) with the
    neighbouring strip of the image of the same size - left, right, above or below, whichever continues the
    rectangle's surroundings best (lowest mean colour difference along the shared border).  Returns the patch
    (float32 RGB) with the rectangle replaced, or None when every neighbour differs too much (an edge, a feature)."""
    ys, xs = np.where(mask > 0)
    if len(ys) == 0:
        return None
    H, W = rgb.shape[:2]
    ox, oy = origin
    ry0, ry1, rx0, rx1 = ys.min() + oy, ys.max() + 1 + oy, xs.min() + ox, xs.max() + 1 + ox
    rh, rw = ry1 - ry0, rx1 - rx0
    g = 3  # gap between the rectangle and the source strip (the badge's own shadow / drop-shadow)
    cands = []
    for name, (sx0, sy0) in (("L", (rx0 - rw - g, ry0)), ("R", (rx1 + g, ry0)), ("U", (rx0, ry0 - rh - g)), ("D", (rx0, ry1 + g))):
        if force and name != force:
            continue
        sx1, sy1 = sx0 + rw, sy0 + rh
        if sx0 < 0 or sy0 < 0 or sx1 > W or sy1 > H:
            continue
        src = rgb[sy0:sy1, sx0:sx1].astype(np.float32)
        # compare the strip's outer border with the rectangle's outer border (ring of 3 px just outside both)
        def ring(x0, y0, x1, y1):
            parts = []
            if y0 - 3 >= 0: parts.append(rgb[y0 - 3:y0, max(0, x0):min(W, x1)].reshape(-1, 3))
            if y1 + 3 <= H: parts.append(rgb[y1:y1 + 3, max(0, x0):min(W, x1)].reshape(-1, 3))
            if x0 - 3 >= 0: parts.append(rgb[max(0, y0):min(H, y1), x0 - 3:x0].reshape(-1, 3))
            if x1 + 3 <= W: parts.append(rgb[max(0, y0):min(H, y1), x1:x1 + 3].reshape(-1, 3))
            return np.concatenate(parts).astype(np.float32) if parts else None
        rr, sr = ring(rx0, ry0, rx1, ry1), ring(sx0, sy0, sx1, sy1)
        if rr is None or sr is None:
            continue
        # the strip itself must be "plain": its own interior should look like the rectangle's ring
        err = float(np.abs(np.median(rr, axis=0) - np.median(sr, axis=0)).mean()) + 0.5 * float(np.abs(np.median(src.reshape(-1, 3), axis=0) - np.median(rr, axis=0)).mean())
        tex = float(src.std(axis=(0, 1)).mean())
        cands.append((err + 0.15 * max(0.0, tex - rr.std(axis=0).mean()), name, src))
    if not cands:
        return None
    cands.sort(key=lambda c: c[0])
    err, name, src = cands[0]
    if err > max_err:
        return None
    ph, pw = mask.shape
    patch = rgb[oy:oy + ph, ox:ox + pw].copy()
    # Poisson-blend the strip into place so a slight colour / lighting offset does not leave a ghost rectangle
    m = np.zeros((ph, pw), np.uint8); m[ry0 - oy:ry1 - oy, rx0 - ox:rx1 - ox] = 255
    canvas = np.zeros_like(patch); canvas[ry0 - oy:ry1 - oy, rx0 - ox:rx1 - ox] = src.astype(np.uint8)
    centre = ((rx0 + rx1) // 2 - ox, (ry0 + ry1) // 2 - oy)
    try:
        out = cv2.seamlessClone(cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR), cv2.cvtColor(patch, cv2.COLOR_RGB2BGR), m, centre, cv2.NORMAL_CLONE)
        return cv2.cvtColor(out, cv2.COLOR_BGR2RGB).astype(np.float32)
    except cv2.error:
        patch = patch.astype(np.float32); patch[ry0 - oy:ry1 - oy, rx0 - ox:rx1 - ox] = src
        return patch


def find_plate(rgb, box):
    """The badge / plate blob inside and around a rough box: pixels that differ from the surrounding panel colour
    (median of a ring around the box), closed, largest component overlapping the box.  Returns its bbox with a
    margin, or None when nothing plausible is found."""
    H, W = rgb.shape[:2]
    x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
    pad = int(max(24, 0.3 * max(bw, bh)))
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)
    patch = rgb[Y0:Y1, X0:X1]
    ring = np.ones(patch.shape[:2], bool); ring[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = False
    if not ring.any():
        return None
    border = patch[ring].astype(np.float32)
    bg = np.median(border, axis=0)
    dist = np.abs(patch.astype(np.float32) - bg).max(axis=2)
    m = (dist > max(12.0, 2.5 * float(border.std(axis=0).max()))).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    cx0, cy0, cx1, cy1 = x0 - X0, y0 - Y0, x1 - X0, y1 - Y0
    best = None
    for i in range(1, n):
        lx, ly, lw, lh, la = stats[i]
        ox = max(0, min(lx + lw, cx1) - max(lx, cx0)); oy = max(0, min(ly + lh, cy1) - max(ly, cy0))
        if la >= 0.02 * bw * bh and ox * oy >= 0.4 * min(la, lw * lh) and lw <= 1.6 * bw + 20 and lh <= 1.6 * bh + 20:
            if best is None or la > best[4]:
                best = (lx, ly, lw, lh, la)
    if best is None:
        return None
    lx, ly, lw, lh, _ = best; mg = max(6, int(0.06 * max(lw, lh)))
    return (max(0, X0 + lx - mg), max(0, Y0 + ly - mg), min(W, X0 + lx + lw + mg), min(H, Y0 + ly + lh + mg))


def delogo(im, boxes, thr=26, dilate=5, radius=7, mode="auto", report=None):
    rgb = np.asarray(im.convert("RGB")).copy()
    H, W = rgb.shape[:2]
    for b in boxes:
        x0, y0, x1, y1 = [int(round(v)) for v in b[:4]]
        bmode = b[4] if len(b) > 4 else mode
        x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(W, x1), min(H, y1)
        if x1 - x0 < 4 or y1 - y0 < 4:
            continue
        pad = int(max(radius * 2, 24, 0.3 * max(x1 - x0, y1 - y0)))
        X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)
        patch = rgb[Y0:Y1, X0:X1].copy()
        box = patch[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0]
        # background colour / texture from the ring between the box and the padded patch edge
        ring = np.ones(patch.shape[:2], bool); ring[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = False
        border = patch[ring] if ring.any() else box.reshape(-1, 3)
        bg = np.median(border, axis=0)
        noise_std = float(border.astype(np.float32).std(axis=0).mean())
        mask = np.zeros(patch.shape[:2], np.uint8)
        if bmode == "lama":
            # mask = the rough box grown 6 %, united with the badge blob found inside it (when one is found), then
            # filled by LaMa (tools/lama_inpaint.py) - handles hammertone paint, louvres and edges far better than
            # Telea or a copied strip
            from lama_inpaint import inpaint
            bw_, bh_ = x1 - x0, y1 - y0
            gx, gy = int(0.06 * bw_) + 4, int(0.06 * bh_) + 4
            mx0, my0, mx1, my1 = max(0, x0 - gx), max(0, y0 - gy), min(W, x1 + gx), min(H, y1 + gy)
            blob = find_plate(rgb, (x0, y0, x1, y1))
            if blob is not None:
                bx0, by0, bx1, by1 = blob
                mx0, my0, mx1, my1 = min(mx0, bx0), min(my0, by0), max(mx1, bx1), max(my1, by1)
            full = np.zeros((H, W), np.uint8); full[my0:my1, mx0:mx1] = 255
            rgb = inpaint(rgb, full)
            if report is not None: report.append((mx0, my0, mx1, my1))
            continue
        if bmode in ("L", "R", "U", "D"):
            mask[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = 255
            if report is not None: report.append((x0, y0, x1, y1))
            out = neighbour_fill(rgb, mask, (X0, Y0), max_err=1e9, force=bmode)
            if out is None:
                continue
            soft = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (0, 0), 2.0)[..., None]
            patch = np.clip(patch.astype(np.float32) * (1 - soft) + out * soft, 0, 255).astype(np.uint8)
            rgb[Y0:Y1, X0:X1] = patch
            continue
        if bmode == "find":
            # the rough box is only approximate: look for the text-like blob (high edge density) nearest the box centre
            # in a window twice the box size, and fill that blob's bounding rectangle
            nb = find_logo(rgb, (x0, y0, x1, y1))
            if nb is None:
                continue
            x0, y0, x1, y1 = nb
            pad = int(max(radius * 2, 24, 0.3 * max(x1 - x0, y1 - y0)))
            X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)
            patch = rgb[Y0:Y1, X0:X1].copy()
            ring = np.ones(patch.shape[:2], bool); ring[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = False
            border = patch[ring] if ring.any() else patch.reshape(-1, 3)
            noise_std = float(border.astype(np.float32).std(axis=0).mean())
            mask = np.zeros(patch.shape[:2], np.uint8)
            mask[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = 255
            mask[:2, :] = 0; mask[-2:, :] = 0; mask[:, :2] = 0; mask[:, -2:] = 0
        elif bmode == "all":
            mask[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = 255
            if report is not None: report.append((x0, y0, x1, y1))
        elif bmode == "plate":
            # grow the rough box a little (boxes come from a small preview) - the blob search below covers the padded patch anyway
            # find the plate/badge as the blob of non-background pixels around the box centre, then fill its
            # whole bounding rectangle (rough boxes from a small preview are often 20-60 px off)
            dist = np.abs(patch.astype(np.float32) - bg).max(axis=2)
            m = (dist > max(12.0, 2.5 * float(border.astype(np.float32).std(axis=0).max()))).astype(np.uint8)
            m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
            n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
            cx0, cy0, cx1, cy1 = x0 - X0, y0 - Y0, x1 - X0, y1 - Y0
            best = None
            barea = (cx1 - cx0) * (cy1 - cy0)
            for i in range(1, n):
                lx, ly, lw, lh, la = stats[i]
                ox = max(0, min(lx + lw, cx1) - max(lx, cx0)); oy = max(0, min(ly + lh, cy1) - max(ly, cy0))
                inside = ox * oy
                if la >= 0.02 * barea and inside >= 0.4 * min(la, lw * lh) and lw <= 1.8 * (cx1 - cx0) + 20 and lh <= 1.8 * (cy1 - cy0) + 20:
                    if best is None or la > best[4]:
                        best = (lx, ly, lw, lh, la)
            if best is None or (best[2] >= patch.shape[1] - 2 and best[3] >= patch.shape[0] - 2):
                mask[cy0:cy1, cx0:cx1] = 255
                if report is not None: report.append((x0, y0, x1, y1))
            else:
                lx, ly, lw, lh, _ = best; mg = max(6, int(0.06 * max(lw, lh)))
                fy0, fy1 = max(0, ly - mg), min(patch.shape[0], ly + lh + mg); fx0, fx1 = max(0, lx - mg), min(patch.shape[1], lx + lw + mg)
                mask[fy0:fy1, fx0:fx1] = 255
                if report is not None: report.append((X0 + fx0, Y0 + fy0, X0 + fx1, Y0 + fy1))
            # never mask the whole patch - the inpainter needs a ring of real pixels to work from
            mask[:2, :] = 0; mask[-2:, :] = 0; mask[:, :2] = 0; mask[:, -2:] = 0
        else:
            dist = np.abs(box.astype(np.float32) - bg).max(axis=2)
            m = (dist > thr).astype(np.uint8) * 255
            m = cv2.dilate(m, np.ones((2 * dilate + 1, 2 * dilate + 1), np.uint8))
            mask[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = m
        if not mask.any():
            continue
        # 1) try to fill the masked rectangle with a copy of the neighbouring panel (same texture, same gradient);
        #    2) fall back to Telea inpainting when no neighbour matches the rectangle's surroundings
        out = neighbour_fill(rgb, mask, (X0, Y0))
        if out is None:
            out = cv2.inpaint(cv2.cvtColor(patch, cv2.COLOR_RGB2BGR), mask, radius, cv2.INPAINT_TELEA)
            out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB).astype(np.float32)
        else:
            noise_std = 0.0
        if noise_std > 0.5:
            rng = np.random.default_rng(1)
            n = rng.normal(0, min(noise_std, 6.0), out.shape).astype(np.float32)
            n = cv2.GaussianBlur(n, (3, 3), 0)
            sel = mask > 0
            out[sel] = np.clip(out[sel] + n[sel], 0, 255)
        # feather the edge of the filled area so it does not show as a hard rectangle
        soft = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (0, 0), 2.0)[..., None]
        patch = np.clip(patch.astype(np.float32) * (1 - soft) + out * soft, 0, 255).astype(np.uint8)
        rgb[Y0:Y1, X0:X1] = patch
    res = Image.fromarray(rgb)
    if im.mode == "RGBA":
        res.putalpha(im.getchannel("A"))
    return res
