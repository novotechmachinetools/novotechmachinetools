#!/usr/bin/env python3
"""Cut a machine out of a photo with a real background (showroom render, factory floor) using the
rembg / IS-Net segmentation model, for the house rule that no product photo is shown as a rectangle
on a coloured surface (docs/images.md).  White-background studio photos do not need this — the
image pipeline cuts those out by itself (tools/make_images.py).

    python3 tools/rembg_cutout.py <key> [<key> ...]      keys from tools/image_map.json
    → tools/src-images/cutouts/<key>-cut.png  (then point the key's "src" at that file, "trim": true)

Needs:  pip install "rembg[cpu]"   (model ~180 MB, downloaded on first use)
"""
import json
import os
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "src-images", "cutouts")


def main():
    from rembg import new_session, remove
    keys = [k for k in sys.argv[1:] if not k.startswith("--")]
    image_map = json.load(open(os.path.join(ROOT, "tools", "image_map.json")))
    session = new_session("isnet-general-use")
    os.makedirs(OUT, exist_ok=True)
    for key in keys:
        spec = image_map[key]
        src = spec["src"] if os.path.isabs(spec["src"]) else os.path.join(ROOT, spec["src"])
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        if spec.get("crop"):
            im = im.crop(tuple(spec["crop"]))
        res = remove(im, session=session, post_process_mask=True)
        out = os.path.join(OUT, key + "-cut.png")
        res.save(out)
        print(key, res.size, "->", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
