#!/usr/bin/env python3
"""Prepare the NovoFab (value line) product photos.

Source photos are the cut-outs extracted from the NovoTech sawing catalogue PDF
(/home/claude/nf-src/cut/*.png, RGBA). For every photo the OEM nameplates / model
labels are removed (inpainting). The NovoFab nameplate overlay (tools/plate.py) is kept
as an option but switched off (MOUNT_PLATES = False) — the photos are used as they are.
Output: tools/src-images/novofab/<key>.png

    python3 tools/novofab_images.py            # all
    python3 tools/novofab_images.py nf-h330-1  # one key
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plate import apply_plate, face_quad, inpaint, rect_quad, render_plate  # noqa: E402

SRC = "/home/claude/nf-src/cut"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "src-images", "novofab")
MOUNT_PLATES = False   # True = composite the NovoFab nameplate on each product photo

R = lambda **k: ("rect", k)            # rect_quad(cx, cy, w, h, angle_deg)
F = lambda face, uv: ("face", face, uv)  # face_quad(face, u0, u1, v0, v1)

JOBS = {
    # ---------------------------------------------------------------- manual pivot saws
    "nf-m250-1": dict(src="p10-057",
                      inpaint=[[(800, 243), (878, 243), (878, 312), (800, 312)], [(330, 430), (420, 430), (420, 466), (330, 466)]],
                      plate=F([(255, 500), (865, 458), (870, 692), (265, 765)], (0.25, 0.5, 0.3, 0.6))),
    "nf-m260-1": dict(src="p10-059",
                      inpaint=[[(150, 70), (250, 70), (250, 185), (150, 185)], [(788, 253), (935, 253), (935, 352), (788, 352)]],
                      plate=F([(160, 110), (245, 118), (240, 178), (157, 170)], (0, 1, 0.08, 0.92))),
    "nf-m250s-1": dict(src="p11-063",
                       inpaint=[[(175, 62), (270, 62), (270, 188), (175, 188)], [(670, 175), (808, 175), (808, 258), (670, 258)]],
                       plate=F([(183, 118), (262, 122), (260, 182), (182, 178)], (0, 1, 0.1, 0.9))),
    "nf-m260t-1": dict(src="p12-069",
                       inpaint=[[(738, 226), (892, 222), (892, 326), (738, 330)]],
                       plate=R(cx=815, cy=275, w=120, h=75, angle_deg=-5)),
    "nf-m400-1": dict(src="p13-075",
                      inpaint=[[(140, 482), (205, 482), (205, 520), (140, 520)]],
                      plate=R(cx=450, cy=590, w=140, h=88, angle_deg=0)),
    # ---------------------------------------------------------------- semi-automatic
    "nf-h250s-1": dict(src="p11-065",
                       inpaint=[[(164, 172), (258, 176), (258, 250), (164, 246)], [(675, 165), (795, 165), (795, 245), (675, 245)]],
                       plate=R(cx=211, cy=211, w=104, h=65, angle_deg=2.5)),
    "nf-h260t-1": dict(src="p12-071",
                       inpaint=[[(280, 84), (358, 94), (356, 147), (278, 138)]],
                       plate=F([(288, 91), (350, 100), (348, 140), (285, 132)], (0, 1, 0.1, 0.9))),
    "nf-h330-1": dict(src="p30-203",
                      plate=F([(400, 740), (1040, 705), (1050, 1000), (420, 1160)], (0.22, 0.52, 0.33, 0.63))),
    "nf-h330c-1": dict(src="p29-196",
                       inpaint=[[(240, 620), (325, 620), (325, 660), (240, 660)]],
                       plate=R(cx=950, cy=800, w=190, h=118, angle_deg=0)),
    "nf-h400-1": dict(src="p13-077", plate=R(cx=520, cy=640, w=150, h=94, angle_deg=0)),
    "nf-h300sc-1": dict(src="p14-086",
                        plate=F([(660, 730), (1110, 660), (1115, 900), (665, 1050)], (0.2, 0.55, 0.3, 0.62))),
    "nf-h300sc-2": dict(src="p14-081"),
    "nf-h300sc-3": dict(src="p14-082"),
    "nf-h300sc-4": dict(src="p14-083"),
    "nf-h460-1": dict(src="p36-234", plate=R(cx=1345, cy=970, w=170, h=106, angle_deg=0)),
    "nf-h460-2": dict(src="p36-231"),
    # ---------------------------------------------------------------- automatic
    "nf-a300-1": dict(src="p31-209", plate=R(cx=1030, cy=1080, w=190, h=118, angle_deg=-1)),
    "nf-a300-2": dict(src="p31-205"),
    "nf-a300-3": dict(src="p31-206"),
    "nf-a300t-1": dict(src="p32-213", plate=R(cx=1120, cy=1120, w=190, h=118, angle_deg=0)),
    "nf-a300t-2": dict(src="p32-210"),
    "nf-a300sc-1": dict(src="p15-093",
                        inpaint=[[(150, 205), (258, 205), (258, 264), (150, 264)], [(60, 170), (130, 170), (130, 210), (60, 210)],
                                 [(650, 160), (790, 160), (790, 210), (650, 210)]],
                        plate=R(cx=200, cy=300, w=140, h=88, angle_deg=0)),
    "nf-a300sc-2": dict(src="p15-088"),
    "nf-a300sc-3": dict(src="p15-089"),
    "nf-a300sc-4": dict(src="p15-090"),
    "nf-a330-1": dict(src="p33-220", clear=[(70, 740, 540, 817)], plate=R(cx=300, cy=520, w=90, h=56, angle_deg=0)),
    "nf-a330-2": dict(src="p33-214"),
    "nf-a330-3": dict(src="p33-216", inpaint=[[(78, 38), (150, 38), (150, 63), (78, 63)]]),
    "nf-a350-1": dict(src="p34-224", plate=R(cx=1270, cy=1000, w=190, h=118, angle_deg=0)),
    "nf-a460-1": dict(src="p35-229",
                      inpaint=[[(995, 205), (1065, 205), (1065, 275), (995, 275)]],
                      plate=R(cx=1120, cy=310, w=96, h=60, angle_deg=32)),
    "nf-a460-2": dict(src="p35-226"),
    "nf-a600-1": dict(src="p37-241", plate=R(cx=1250, cy=870, w=180, h=112, angle_deg=-2)),
    # ---------------------------------------------------------------- double column
    "nf-dc280-1": dict(src="p17-109",
                       inpaint=[[(995, 212), (1105, 212), (1105, 268), (995, 268)]],
                       plate=R(cx=1030, cy=1000, w=200, h=125, angle_deg=0)),
    "nf-dc280t-1": dict(src="p18-116",
                        inpaint=[[(995, 208), (1085, 208), (1085, 265), (995, 265)]],
                        plate=R(cx=920, cy=930, w=190, h=118, angle_deg=0)),
    "nf-dc280t-2": dict(src="p18-111"),
    "nf-dc280t-3": dict(src="p18-112"),
    "nf-dc280a-1": dict(src="p19-125",
                        inpaint=[[(845, 218), (940, 218), (940, 276), (845, 276)]],
                        plate=F([(340, 800), (990, 700), (1000, 1060), (350, 1230)], (0.45, 0.75, 0.3, 0.6))),
    "nf-dc280av-1": dict(src="p20-134",
                         inpaint=[[(176, 236), (290, 236), (290, 302), (176, 302)]],
                         plate=F([(185, 244), (283, 246), (283, 296), (185, 294)], (0.05, 0.95, -0.05, 1.05))),
    "nf-dc280av-2": dict(src="p20-129"),
    "nf-dc280av-3": dict(src="p20-130"),
    "nf-dc280av-4": dict(src="p20-131"),
    "nf-dc280-stand": dict(src="p20-127"),
    "nf-dc350-1": dict(src="p21-139", plate=R(cx=222, cy=322, w=150, h=94, angle_deg=0)),
    "nf-dc350-2": dict(src="p21-135"),
    "nf-dc350-3": dict(src="p21-136"),
    "nf-dc500-1": dict(src="p22-145",
                       inpaint=[[(62, 345), (310, 345), (310, 415), (62, 415)]],
                       plate=R(cx=186, cy=400, w=150, h=94, angle_deg=0)),
    "nf-dc600-1": dict(src="p23-149",
                       inpaint=[[(118, 330), (382, 330), (382, 402), (118, 402)]],
                       plate=R(cx=250, cy=400, w=170, h=106, angle_deg=0)),
    "nf-dc600-2": dict(src="p23-146"),
}


def quad_of(spec):
    if spec[0] == "rect":
        return rect_quad(**spec[1])
    face, (u0, u1, v0, v1) = spec[1], spec[2]
    return face_quad(face, u0, u1, v0, v1)


def process(key, job, plate):
    im = Image.open(os.path.join(SRC, job["src"] + ".png")).convert("RGBA")
    for poly in job.get("inpaint", []):
        im = inpaint(im, poly, radius=8, feather=3)
    for (x0, y0, x1, y1) in job.get("clear", []):
        a = np.asarray(im).copy()
        a[y0:y1, x0:x1, 3] = 0
        im = Image.fromarray(a, "RGBA")
    if MOUNT_PLATES and job.get("plate"):
        im = apply_plate(im, quad_of(job["plate"]), plate, soft=job.get("soft", 0.7))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    keys = [k for k in sys.argv[1:] if not k.startswith("--")] or list(JOBS)
    plate = render_plate("alu") if MOUNT_PLATES else None
    for k in keys:
        im = process(k, JOBS[k], plate)
        # keep RGB-only sources as RGB (smaller webp), cut-outs as RGBA
        if np.asarray(im)[..., 3].min() == 255:
            im = im.convert("RGB")
        im.save(os.path.join(OUT, k + ".png"), optimize=True)
        print(k, im.size, im.mode)


if __name__ == "__main__":
    main()
