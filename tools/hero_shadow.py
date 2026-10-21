#!/usr/bin/env python3
"""Hero cut-out with a clean drawn shadow, for machines shown on the orange hero band.

The photographed floor shadow in a manufacturer's white-background photo is a grey smear once the
white is removed; on the orange band it looks dirty (NovoTech, Oct 2026).  This tool cuts the machine
out of the full-size photo with that shadow dropped and draws a new one: a short, dark contact shadow
right under the feet plus a soft, wide ground shadow, in a warm near-black that sits naturally on
orange.  The photo is upscaled 2× before the cut (clean anti-aliased edge, enough pixels for the
1200 px hero variant).

    python3 tools/hero_shadow.py <out-key> <source-key> [--max 1600] [--strength 1.0] [--no-shadow]
        keys from tools/image_map.json; writes tools/src-images/cutouts/<out-key>.png
        then: python3 tools/make_images.py --only <out-key>
    python3 tools/hero_shadow.py --file <photo.jpg> <out.png>      ad-hoc use
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cutout2 import auto_cutout, is_white_background  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "src-images", "cutouts")
SHADOW_RGB = (30, 22, 10)       # warm near-black


def draw_shadow(cut, strength=1.0):
    """Compose a contact + ground shadow under a transparent cut-out. Returns a new RGBA image
    (a little taller than the cut-out so the ground shadow has room)."""
    a = np.asarray(cut.getchannel("A")).astype(np.float32) / 255.0
    H, W = a.shape
    extra = int(round(H * 0.07))
    CH = H + extra
    solid = a > 0.5
    rows = solid.sum(1)
    if not rows.any():
        return cut
    # floor line: lowest row that still carries real mass (ignores a stray pixel)
    foot_y = int(np.where(rows > max(4, W * 0.01))[0].max())
    # footprint: columns the machine occupies in the band just above the floor (feet, base, castors)
    band = solid[max(0, foot_y - int(H * 0.04)):foot_y + 1]
    cols = np.where(band.any(0))[0]
    x0, x1 = int(cols.min()), int(cols.max())
    cx, half = (x0 + x1) / 2.0, max(8.0, (x1 - x0) / 2.0 * 1.06)
    yy, xx = np.mgrid[0:CH, 0:W].astype(np.float32)
    # 1) wide, soft ground shadow: a flattened ellipse centred a little below the floor line
    ry = max(10.0, W * 0.025)
    ell = ((xx - cx) / half) ** 2 + ((yy - (foot_y + ry * 0.35)) / ry) ** 2
    ground = np.clip(1 - ell, 0, 1) ** 0.8
    ground = ndimage.gaussian_filter(ground, W * 0.016) * 0.70
    # 2) tight contact shadow along the floor line, where the feet / base meet the ground
    contact = np.zeros((CH, W), np.float32)
    contact[max(0, foot_y - 3):foot_y + 5, x0 + 4:max(x0 + 5, x1 - 4)] = 1
    contact = ndimage.gaussian_filter(contact, max(3.0, W * 0.006)) * 0.60
    shadow = np.clip((ground + contact) * strength, 0, 1)
    sh = np.zeros((CH, W, 4), np.uint8)
    sh[..., :3] = SHADOW_RGB
    sh[..., 3] = (shadow * 255).round().astype(np.uint8)
    canvas = Image.fromarray(sh, "RGBA")
    canvas.alpha_composite(cut, (0, 0))
    return canvas


def hero_from_photo(src_path, max_w=1600, strength=1.0, shadow=True, shadow_thr=140):
    src = ImageOps.exif_transpose(Image.open(src_path)).convert("RGB")
    white, level = is_white_background(src)
    if not white:
        raise SystemExit(f"{src_path}: not a white-background photo — cut it out with rembg_cutout.py instead")
    big = src.resize((src.width * 2, src.height * 2), Image.LANCZOS)
    big = big.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    # shadow_thr lower than the gallery default: the whole grey floor shadow goes, including its darker core
    # right under the base (a drawn shadow replaces it)
    cut = auto_cutout(big, level, shadow_thr=shadow_thr, drop_shadow=True)
    if shadow:
        cut = draw_shadow(cut, strength)
    bbox = cut.getchannel("A").point(lambda v: 255 if v > 4 else 0).getbbox()
    if bbox:
        cut = cut.crop(bbox)
    if cut.width > max_w:
        cut = cut.resize((max_w, round(cut.height * max_w / cut.width)), Image.LANCZOS)
    return cut


def main():
    args = sys.argv[1:]
    opts = {}
    for flag in ("--max", "--strength"):
        if flag in args:
            i = args.index(flag); opts[flag] = float(args[i + 1]); del args[i:i + 2]
    shadow = "--no-shadow" not in args
    args = [a for a in args if a != "--no-shadow"]
    if args and args[0] == "--file":
        src, out = args[1], args[2]
        key = os.path.splitext(os.path.basename(out))[0]
    else:
        key, source = args[0], args[1]
        image_map = json.load(open(os.path.join(ROOT, "tools", "image_map.json")))
        spec = image_map[source]
        src = spec["src"] if os.path.isabs(spec["src"]) else os.path.join(ROOT, spec["src"])
        out = os.path.join(OUT, key + ".png")
    cut = hero_from_photo(src, int(opts.get("--max", 1600)), opts.get("--strength", 1.0), shadow)
    cut.save(out, "PNG", optimize=True)
    print(key, cut.size, "<-", os.path.basename(src))


if __name__ == "__main__":
    main()
