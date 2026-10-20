#!/usr/bin/env python3
"""Prepare the NovoTech value-line (NT series) product photos.

Source photos are the cut-outs extracted from the NovoTech sawing catalogue PDF
(/home/claude/nf-src/cut/*.png, RGBA). For every photo the OEM nameplates / model
labels are removed (inpainting). Label areas are filled with the panel colour (tools/retouch.py); the photos are otherwise untouched.
Output: tools/src-images/value-line/<key>.png

    python3 tools/value_line_images.py            # all
    python3 tools/value_line_images.py nt-h13-1   # one key
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retouch import clean_patch  # noqa: E402

SRC = "/home/claude/nf-src/cut"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "src-images", "value-line")


JOBS = {
    # ---------------------------------------------------------------- semi-automatic
    "nt-h10f-1": dict(src="p28-188", inpaint=[[(1188, 850), (1428, 850), (1428, 948), (1188, 948)]]),
    "nt-h10f-2": dict(src="p28-185"),
    "nt-h10f-3": dict(src="p29-191"),
    "nt-h10s-1": dict(src="p11-065",
                       inpaint=[[(168, 174), (258, 178), (258, 250), (168, 246)]]),
    "nt-h10t-1": dict(src="p12-071",
                       inpaint=[[(280, 84), (358, 94), (356, 147), (278, 138)]]),
    "nt-h13-1": dict(src="p30-203"),
    "nt-h13c-1": dict(src="p29-196"),
    "nt-h16-1": dict(src="p13-077"),
    "nt-h12sc-1": dict(src="p14-086"),
    "nt-h12sc-2": dict(src="p14-081"),
    "nt-h12sc-3": dict(src="p14-082"),
    "nt-h12sc-4": dict(src="p14-083"),
    "nt-h18-1": dict(src="p36-234"),
    "nt-h18-2": dict(src="p36-231"),
    # ---------------------------------------------------------------- automatic
    "nt-a12-1": dict(src="p31-209"),
    "nt-a12-2": dict(src="p31-205"),
    "nt-a12-3": dict(src="p31-206"),
    "nt-a12t-1": dict(src="p32-213"),
    "nt-a12t-2": dict(src="p32-210"),
    "nt-a12sc-1": dict(src="p15-093",
                        inpaint=[[(148, 210), (263, 210), (263, 260), (148, 260)]]),
    "nt-a12sc-2": dict(src="p15-088"),
    "nt-a12sc-3": dict(src="p15-089"),
    "nt-a12sc-4": dict(src="p15-090"),
    "nt-a13-1": dict(src="p33-220", clear=[(70, 740, 540, 817)]),
    "nt-a13-2": dict(src="p33-214"),
    "nt-a13-3": dict(src="p33-216"),
    "nt-a14-1": dict(src="p34-224"),
    "nt-a18-1": dict(src="p35-229",
                      inpaint=[[(1003, 213), (1070, 213), (1070, 278), (1003, 278)]]),
    "nt-a18-2": dict(src="p35-226"),
    "nt-a24-1": dict(src="p37-241"),
    # ---------------------------------------------------------------- double column
    "nt-dc11-1": dict(src="p17-109",
                       inpaint=[[(995, 212), (1105, 212), (1105, 268), (995, 268)]]),
    "nt-dc11t-1": dict(src="p18-116",
                        inpaint=[[(1010, 188), (1070, 188), (1070, 222), (1010, 222)]]),
    "nt-dc11t-2": dict(src="p18-111"),
    "nt-dc11t-3": dict(src="p18-112"),
    "nt-dc11a-1": dict(src="p19-125",
                        inpaint=[[(858, 203), (937, 201), (935, 247), (858, 249)]]),
    "nt-dc11av-1": dict(src="p20-134",
                         inpaint=[[(176, 236), (290, 236), (290, 302), (176, 302)]]),
    "nt-dc11av-2": dict(src="p20-129"),
    "nt-dc11av-3": dict(src="p20-130"),
    "nt-dc11av-4": dict(src="p20-131"),
    "nt-dc11-stand": dict(src="p20-127"),
    "nt-dc14-1": dict(src="p21-139"),
    "nt-dc14-2": dict(src="p21-135"),
    "nt-dc14-3": dict(src="p21-136"),
    "nt-dc20-1": dict(src="p22-145",
                       inpaint=[[(62, 345), (310, 345), (310, 415), (62, 415)]]),
    "nt-dc24-1": dict(src="p23-149",
                       inpaint=[[(118, 330), (382, 330), (382, 402), (118, 402)]]),
    "nt-dc24-2": dict(src="p23-146"),
}


def process(key, job):
    im = Image.open(os.path.join(SRC, job["src"] + ".png")).convert("RGBA")
    # the PDF soft masks have holes inside white panels: flatten onto the white studio background
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    im = Image.alpha_composite(bg, im)
    for (x0, y0, x1, y1) in job.get("clear", []):
        a = np.asarray(im).copy()
        a[y0:y1, x0:x1, :3] = 255
        im = Image.fromarray(a, "RGBA")
    for poly in job.get("inpaint", []):
        im = clean_patch(im, poly, ring=14, feather=2.2)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    keys = [k for k in sys.argv[1:] if not k.startswith("--")] or list(JOBS)
    for k in keys:
        im = process(k, JOBS[k]).convert("RGB")
        im.save(os.path.join(OUT, k + ".png"), optimize=True)
        print(k, im.size, im.mode)


if __name__ == "__main__":
    main()
