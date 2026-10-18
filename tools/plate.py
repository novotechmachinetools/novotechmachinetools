#!/usr/bin/env python3
"""Composite a NovoFab nameplate onto a product photo so that it looks like a real
metal plate riveted to the machine (perspective, surface shading, relief edge,
photo softness and noise).

    from plate import render_plate, apply_plate, rect_quad
    plate = render_plate("alu")                       # high-res RGBA plate
    out   = apply_plate(img_rgba, quad, plate)        # quad = [TL, TR, BR, BL] in image px

Styles: "alu" (brushed aluminium plate, dark logo) and "dark" (charcoal badge, light logo).
"""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "novofab", "novofab-logo-1420.png")
FONT_BOLD = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FONT_REG = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"


# ----------------------------------------------------------------------------- plate art
def _logo(light=False):
    im = Image.open(LOGO).convert("RGBA")
    if not light:
        return im
    # light version for dark plates: grey parts -> near-white, orange untouched
    arr = np.asarray(im).astype(np.float32)
    rgb, a = arr[..., :3], arr[..., 3:]
    mx, mn = rgb.max(-1, keepdims=True), rgb.min(-1, keepdims=True)
    sat = (mx - mn) / np.maximum(mx, 1)
    grey = (sat < 0.22).astype(np.float32)
    light_rgb = np.full_like(rgb, 236.0)
    rgb = rgb * (1 - grey) + light_rgb * grey
    return Image.fromarray(np.concatenate([rgb, a], -1).astype(np.uint8), "RGBA")


def _brushed(w, h, base=(214, 216, 219), strength=5, seed=1):
    rng = np.random.default_rng(seed)
    rows = rng.normal(0, 1, (h, 1)).astype(np.float32)
    fine = rng.normal(0, 1, (h, w)).astype(np.float32)
    fine = cv2.GaussianBlur(fine, (0, 0), sigmaX=max(w / 60, 3), sigmaY=0.6)
    fine /= max(fine.std(), 1e-6)
    tex = rows * 0.6 + fine * 0.8
    # soft diagonal sheen
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sheen = ((xx / w) * 0.55 + (yy / h) * 0.45)
    sheen = 1.0 + 0.06 * np.cos(sheen * math.pi * 1.6 + 0.4)
    img = np.zeros((h, w, 3), np.float32)
    for c in range(3):
        img[..., c] = (base[c] + tex * strength) * sheen
    return np.clip(img, 0, 255).astype(np.uint8)


def _rounded_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return m


def _rivet(draw, cx, cy, r, dark=False):
    # countersunk screw head: outer ring, domed face, slot highlight
    ring = (70, 72, 76) if not dark else (16, 16, 18)
    face = (176, 178, 182) if not dark else (96, 98, 102)
    hi = (236, 238, 240) if not dark else (170, 172, 176)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ring)
    draw.ellipse([cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78], fill=face)
    draw.ellipse([cx - r * 0.5, cy - r * 0.62, cx + r * 0.1, cy - r * 0.05], fill=hi)
    draw.line([cx - r * 0.55, cy + r * 0.1, cx + r * 0.55, cy - r * 0.1], fill=ring, width=max(1, int(r * 0.22)))


def render_plate(style="alu", w=1400, ratio=1.6, text_lines=None, rivets=True, seed=1):
    """High-resolution RGBA nameplate. ratio = width / height."""
    h = int(round(w / ratio))
    r = int(h * 0.06)
    if style == "alu":
        base = Image.fromarray(_brushed(w, h, seed=seed), "RGB").convert("RGBA")
        logo = _logo(light=False)
        text_col = (58, 60, 64)
        line_col = (120, 122, 126)
        inset_col = (150, 152, 156)
    else:
        arr = _brushed(w, h, base=(44, 46, 50), strength=4, seed=seed).astype(np.float32)
        # glossy vertical gradient
        yy = np.linspace(1.18, 0.86, h, dtype=np.float32)[:, None, None]
        base = Image.fromarray(np.clip(arr * yy, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
        logo = _logo(light=True)
        text_col = (205, 207, 210)
        line_col = (120, 122, 126)
        inset_col = (90, 92, 96)
    d = ImageDraw.Draw(base)
    # thin inset border line
    ins = int(h * 0.045)
    d.rounded_rectangle([ins, ins, w - ins - 1, h - ins - 1], radius=max(2, r - ins), outline=inset_col, width=max(2, w // 500))
    # logo
    lw = int(w * 0.74)
    lg = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    lines = text_lines or ["NovoFab Machinery Inc.",
                           "Supplied by NovoTech Machine Tools · Mississauga, Ontario, Canada"]
    fs = int(h * 0.046)
    f1 = ImageFont.truetype(FONT_BOLD, fs)
    f2 = ImageFont.truetype(FONT_REG, fs)
    block = lg.height + int(h * 0.09) + int(fs * 1.35) * len(lines)
    ly = (h - block) // 2 + int(h * 0.01)
    base.alpha_composite(lg, ((w - lw) // 2, ly))
    y = ly + lg.height + int(h * 0.09)
    d.line([int(w * 0.14), y - int(h * 0.04), int(w * 0.86), y - int(h * 0.04)], fill=line_col, width=max(1, w // 700))
    for i, t in enumerate(lines):
        f = f1 if i == 0 else f2
        tw = d.textlength(t, font=f)
        while tw > w * 0.84 and f.size > 8:
            f = ImageFont.truetype(f.path, f.size - 1)
            tw = d.textlength(t, font=f)
        d.text(((w - tw) / 2, y), t, font=f, fill=text_col)
        y += int(fs * 1.35)
    if rivets:
        rr = int(h * 0.045)
        for cx, cy in [(ins + rr * 1.3, ins + rr * 1.3), (w - ins - rr * 1.3, ins + rr * 1.3),
                       (ins + rr * 1.3, h - ins - rr * 1.3), (w - ins - rr * 1.3, h - ins - rr * 1.3)]:
            _rivet(d, cx, cy, rr, dark=(style != "alu"))
    mask = _rounded_mask(w, h, r)
    base.putalpha(mask)
    return base


# ----------------------------------------------------------------------------- geometry
def rect_quad(cx, cy, w, h, angle_deg=0.0, skew=0.0):
    """Rectangle centred at (cx, cy), long axis rotated by angle_deg (clockwise on screen).
    skew > 0 makes the right edge shorter (plate turning away to the right)."""
    a = math.radians(angle_deg)
    u = (math.cos(a), math.sin(a))
    v = (-math.sin(a), math.cos(a))
    hw, hh = w / 2, h / 2
    pts = []
    for sx, sy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
        f = 1 - skew * (sx + 1) / 2
        x = cx + sx * hw * u[0] + sy * hh * f * v[0]
        y = cy + sx * hw * u[1] + sy * hh * f * v[1]
        pts.append((x, y))
    return pts


# ----------------------------------------------------------------------------- compositing
def apply_plate(img, quad, plate, soft=0.6, shade=1.0, shadow=0.5, relief=1.0, noise=None, ss=4):
    """img: PIL RGBA photo. quad: 4 (x, y) image points TL, TR, BR, BL. plate: RGBA from render_plate.
    Returns a new PIL RGBA image."""
    img = img.convert("RGBA")
    src = np.asarray(img).astype(np.float32)
    H, W = src.shape[:2]
    q = np.array(quad, np.float32)
    m = 8
    x0, y0 = max(int(np.floor(q[:, 0].min())) - m, 0), max(int(np.floor(q[:, 1].min())) - m, 0)
    x1, y1 = min(int(np.ceil(q[:, 0].max())) + m, W), min(int(np.ceil(q[:, 1].max())) + m, H)
    bw, bh = x1 - x0, y1 - y0
    region = src[y0:y1, x0:x1]

    # --- warp plate into a supersampled canvas of the bbox
    qw = float(np.linalg.norm(q[1] - q[0]))
    target_w = int(qw * ss * 1.15)
    pl = plate
    if pl.width > target_w:
        pl = pl.resize((target_w, int(target_w * pl.height / pl.width)), Image.LANCZOS)
    pa = np.asarray(pl).astype(np.float32)
    ph, pw = pa.shape[:2]
    srcpts = np.array([[0, 0], [pw, 0], [pw, ph], [0, ph]], np.float32)
    dst = (q - np.array([x0, y0], np.float32)) * ss
    Hm = cv2.getPerspectiveTransform(srcpts, dst)
    canvas = cv2.warpPerspective(pa, Hm, (bw * ss, bh * ss), flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    small = cv2.resize(canvas, (bw, bh), interpolation=cv2.INTER_AREA)
    prgb, palpha = small[..., :3], small[..., 3] / 255.0

    # --- inherit the surface shading of the photo under the plate
    if shade > 0:
        lum = region[..., :3].mean(-1)
        sig = max(bw, bh) / 5.0
        lum_b = cv2.GaussianBlur(lum, (0, 0), sig)
        inside = palpha > 0.5
        ref = lum_b[inside].mean() if inside.any() else lum_b.mean()
        sh = np.clip(lum_b / max(ref, 1.0), 0.55, 1.45)
        sh = 1 + (sh - 1) * shade
        prgb = prgb * sh[..., None]

    # --- relief: 1 px light edge top-left, dark edge bottom-right, drop shadow
    a8 = (palpha * 255).astype(np.uint8)
    k = np.ones((3, 3), np.uint8)
    er = cv2.erode(a8, k, iterations=1).astype(np.float32) / 255.0
    edge = palpha - er
    shifted = np.roll(np.roll(palpha, 1, 0), 1, 1)      # plate moved down-right
    hi = np.clip(edge - shifted, 0, 1)                  # top/left rim
    lo = np.clip(edge - np.roll(np.roll(palpha, -1, 0), -1, 1), 0, 1)
    prgb = prgb + (hi[..., None] * 70 - lo[..., None] * 60) * relief

    out = region.copy()
    if shadow > 0:
        sh_a = cv2.GaussianBlur(np.roll(np.roll(palpha, 2, 0), 1, 1), (0, 0), 1.6) * shadow
        sh_a = np.clip(sh_a - palpha, 0, 1)
        out[..., :3] = out[..., :3] * (1 - sh_a[..., None] * 0.9)

    # --- match photo softness and grain
    if soft > 0:
        prgb = cv2.GaussianBlur(prgb, (0, 0), soft)
        palpha = cv2.GaussianBlur(palpha, (0, 0), soft * 0.8)
    if noise is None:
        g = region[..., :3].mean(-1)
        hp = g - cv2.GaussianBlur(g, (0, 0), 1.0)
        noise = float(np.clip(np.median(np.abs(hp)) * 1.4826 * 1.2, 0.8, 6.0))
    rng = np.random.default_rng(7)
    prgb = prgb + rng.normal(0, noise, prgb.shape).astype(np.float32)

    # keep the plate inside the machine silhouette
    palpha = palpha * (region[..., 3] / 255.0)
    a3 = palpha[..., None]
    out[..., :3] = out[..., :3] * (1 - a3) + np.clip(prgb, 0, 255) * a3
    res = src.copy()
    res[y0:y1, x0:x1] = out
    return Image.fromarray(np.clip(res, 0, 255).astype(np.uint8), "RGBA")


def inpaint(img, polygon, radius=6, feather=2):
    """Remove a label: fill polygon from its surroundings (Telea inpainting), RGBA in/out."""
    img = img.convert("RGBA")
    arr = np.asarray(img).copy()
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).polygon([tuple(p) for p in polygon], fill=255)
    if feather:
        mask = mask.filter(ImageFilter.MaxFilter(feather * 2 + 1))
    m = np.asarray(mask)
    rgb = cv2.inpaint(arr[..., :3], m, radius, cv2.INPAINT_TELEA)
    arr[..., :3] = rgb
    return Image.fromarray(arr, "RGBA")


def flatten(img, bg=(255, 255, 255)):
    bgim = Image.new("RGBA", img.size, bg + (255,))
    return Image.alpha_composite(bgim, img.convert("RGBA")).convert("RGB")


def face_quad(face, u0, u1, v0, v1):
    """Sub-rectangle (u, v in 0..1) of a planar face given by its 4 image corners TL, TR, BR, BL —
    mapped with the face's perspective, so a plate placed with it recedes like the panel it sits on."""
    src = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], np.float32)
    dst = np.array(face, np.float32)
    Hm = cv2.getPerspectiveTransform(src, dst)
    pts = np.array([[[u0, v0], [u1, v0], [u1, v1], [u0, v1]]], np.float32)
    out = cv2.perspectiveTransform(pts, Hm)[0]
    return [(float(x), float(y)) for x, y in out]
