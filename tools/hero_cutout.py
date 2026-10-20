#!/usr/bin/env python3
"""High-resolution hero cut-out from a white-background product photo.

Page heroes are shown at 520 CSS px (1040 px on a 2× display), larger than most manufacturer photos
once the machine is cropped out of them.  To keep the edge clean the photo is upscaled 2× (Lanczos +
light unsharp mask) before the automatic cut-out, so the edge is anti-aliased at twice the
resolution, and the result is brought back to at most 1600 px wide — enough for a 1200 px variant.

    python3 tools/hero_cutout.py <hero-key> <source-key>     keys from tools/image_map.json
    → tools/src-images/cutouts/<hero-key>.png   (then: python3 tools/make_images.py --only <hero-key>)
"""
import json
import os
import sys

from PIL import Image, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cutout2 import auto_cutout, is_white_background  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "src-images", "cutouts")


def hero_cutout(src_path, max_w=1600):
    src = ImageOps.exif_transpose(Image.open(src_path)).convert("RGB")
    white, level = is_white_background(src)
    if not white:
        raise SystemExit(f"{src_path}: not a white-background photo — cut it out with rembg_cutout.py instead")
    big = src.resize((src.width * 2, src.height * 2), Image.LANCZOS)
    big = big.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    cut = auto_cutout(big, level)
    if cut.width > max_w:
        cut = cut.resize((max_w, round(cut.height * max_w / cut.width)), Image.LANCZOS)
    return cut


def main():
    hero, source = sys.argv[1], sys.argv[2]
    image_map = json.load(open(os.path.join(ROOT, "tools", "image_map.json")))
    spec = image_map[source]
    src = spec["src"] if os.path.isabs(spec["src"]) else os.path.join(ROOT, spec["src"])
    cut = hero_cutout(src)
    out = os.path.join(OUT, hero + ".png")
    cut.save(out)
    print(hero, cut.size, "<-", source)


if __name__ == "__main__":
    main()
