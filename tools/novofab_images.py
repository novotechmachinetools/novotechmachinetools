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
from plate import apply_plate, clean_patch, face_quad, rect_quad, render_plate  # noqa: E402

SRC = "/home/claude/nf-src/cut"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "src-images", "novofab")
MOUNT_PLATES = False   # True = composite the NovoFab nameplate on each product photo

R = lambda **k: ("rect", k)            # rect_quad(cx, cy, w, h, angle_deg)
F = lambda face, uv: ("face", face, uv)  # face_quad(face, u0, u1, v0, v1)

JOBS = {
    # ---------------------------------------------------------------- manual pivot saws
    "nf-m10-1": dict(src="p10-057",
                      inpaint=[[(796, 226), (874, 228), (878, 302), (800, 300)]],
                      plate=F([(255, 500), (865, 458), (870, 692), (265, 765)], (0.25, 0.5, 0.3, 0.6))),
    "nf-m10d-1": dict(src="p10-059",
                      inpaint=[[(150, 70), (250, 70), (250, 185), (150, 185)], [(780, 245), (940, 245), (940, 356), (780, 356)]],
                      plate=F([(160, 110), (245, 118), (240, 178), (157, 170)], (0, 1, 0.08, 0.92))),
    "nf-m10s-1": dict(src="p11-063",
                       inpaint=[[(172, 60), (265, 60), (265, 178), (172, 178)]],
                       plate=F([(183, 118), (262, 122), (260, 182), (182, 178)], (0, 1, 0.1, 0.9))),
    "nf-m10t-1": dict(src="p12-069",
                       inpaint=[[(745, 236), (885, 236), (885, 310), (745, 310)]],
                       plate=R(cx=815, cy=275, w=120, h=75, angle_deg=-5)),
    "nf-m16-1": dict(src="p13-075",
                      inpaint=[[(140, 482), (205, 482), (205, 520), (140, 520)]],
                      plate=R(cx=450, cy=590, w=140, h=88, angle_deg=0)),
    # ---------------------------------------------------------------- semi-automatic
    "nf-h10s-1": dict(src="p11-065",
                       inpaint=[[(168, 174), (258, 178), (258, 250), (168, 246)]],
                       plate=R(cx=211, cy=211, w=104, h=65, angle_deg=2.5)),
    "nf-h10t-1": dict(src="p12-071",
                       inpaint=[[(280, 84), (358, 94), (356, 147), (278, 138)]],
                       plate=F([(288, 91), (350, 100), (348, 140), (285, 132)], (0, 1, 0.1, 0.9))),
    "nf-h13-1": dict(src="p30-203",
                      plate=F([(400, 740), (1040, 705), (1050, 1000), (420, 1160)], (0.22, 0.52, 0.33, 0.63))),
    "nf-h13c-1": dict(src="p29-196",
                       plate=R(cx=950, cy=800, w=190, h=118, angle_deg=0)),
    "nf-h16-1": dict(src="p13-077", plate=R(cx=520, cy=640, w=150, h=94, angle_deg=0)),
    "nf-h12sc-1": dict(src="p14-086",
                        plate=F([(660, 730), (1110, 660), (1115, 900), (665, 1050)], (0.2, 0.55, 0.3, 0.62))),
    "nf-h12sc-2": dict(src="p14-081"),
    "nf-h12sc-3": dict(src="p14-082"),
    "nf-h12sc-4": dict(src="p14-083"),
    "nf-h18-1": dict(src="p36-234", plate=R(cx=1345, cy=970, w=170, h=106, angle_deg=0)),
    "nf-h18-2": dict(src="p36-231"),
    # ---------------------------------------------------------------- automatic
    "nf-a12-1": dict(src="p31-209", plate=R(cx=1030, cy=1080, w=190, h=118, angle_deg=-1)),
    "nf-a12-2": dict(src="p31-205"),
    "nf-a12-3": dict(src="p31-206"),
    "nf-a12t-1": dict(src="p32-213", plate=R(cx=1120, cy=1120, w=190, h=118, angle_deg=0)),
    "nf-a12t-2": dict(src="p32-210"),
    "nf-a12sc-1": dict(src="p15-093",
                        inpaint=[[(148, 210), (263, 210), (263, 260), (148, 260)]],
                        plate=R(cx=200, cy=300, w=140, h=88, angle_deg=0)),
    "nf-a12sc-2": dict(src="p15-088"),
    "nf-a12sc-3": dict(src="p15-089"),
    "nf-a12sc-4": dict(src="p15-090"),
    "nf-a13-1": dict(src="p33-220", clear=[(70, 740, 540, 817)], plate=R(cx=300, cy=520, w=90, h=56, angle_deg=0)),
    "nf-a13-2": dict(src="p33-214"),
    "nf-a13-3": dict(src="p33-216"),
    "nf-a14-1": dict(src="p34-224", plate=R(cx=1270, cy=1000, w=190, h=118, angle_deg=0)),
    "nf-a18-1": dict(src="p35-229",
                      inpaint=[[(1003, 213), (1070, 213), (1070, 278), (1003, 278)]],
                      plate=R(cx=1120, cy=310, w=96, h=60, angle_deg=32)),
    "nf-a18-2": dict(src="p35-226"),
    "nf-a24-1": dict(src="p37-241", plate=R(cx=1250, cy=870, w=180, h=112, angle_deg=-2)),
    # ---------------------------------------------------------------- double column
    "nf-dc11-1": dict(src="p17-109",
                       inpaint=[[(995, 212), (1105, 212), (1105, 268), (995, 268)]],
                       plate=R(cx=1030, cy=1000, w=200, h=125, angle_deg=0)),
    "nf-dc11t-1": dict(src="p18-116",
                        inpaint=[[(1010, 188), (1070, 188), (1070, 222), (1010, 222)]],
                        plate=R(cx=920, cy=930, w=190, h=118, angle_deg=0)),
    "nf-dc11t-2": dict(src="p18-111"),
    "nf-dc11t-3": dict(src="p18-112"),
    "nf-dc11a-1": dict(src="p19-125",
                        inpaint=[[(858, 203), (937, 201), (935, 247), (858, 249)]],
                        plate=F([(340, 800), (990, 700), (1000, 1060), (350, 1230)], (0.45, 0.75, 0.3, 0.6))),
    "nf-dc11av-1": dict(src="p20-134",
                         inpaint=[[(176, 236), (290, 236), (290, 302), (176, 302)]],
                         plate=F([(185, 244), (283, 246), (283, 296), (185, 294)], (0.05, 0.95, -0.05, 1.05))),
    "nf-dc11av-2": dict(src="p20-129"),
    "nf-dc11av-3": dict(src="p20-130"),
    "nf-dc11av-4": dict(src="p20-131"),
    "nf-dc11-stand": dict(src="p20-127"),
    "nf-dc14-1": dict(src="p21-139", plate=R(cx=222, cy=322, w=150, h=94, angle_deg=0)),
    "nf-dc14-2": dict(src="p21-135"),
    "nf-dc14-3": dict(src="p21-136"),
    "nf-dc20-1": dict(src="p22-145",
                       inpaint=[[(62, 345), (310, 345), (310, 415), (62, 415)]],
                       plate=R(cx=186, cy=400, w=150, h=94, angle_deg=0)),
    "nf-dc24-1": dict(src="p23-149",
                       inpaint=[[(118, 330), (382, 330), (382, 402), (118, 402)]],
                       plate=R(cx=250, cy=400, w=170, h=106, angle_deg=0)),
    "nf-dc24-2": dict(src="p23-146"),
}


def quad_of(spec):
    if spec[0] == "rect":
        return rect_quad(**spec[1])
    face, (u0, u1, v0, v1) = spec[1], spec[2]
    return face_quad(face, u0, u1, v0, v1)


def process(key, job, plate):
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
    if MOUNT_PLATES and job.get("plate"):
        im = apply_plate(im, quad_of(job["plate"]), plate, soft=job.get("soft", 0.7))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    keys = [k for k in sys.argv[1:] if not k.startswith("--")] or list(JOBS)
    plate = render_plate("alu") if MOUNT_PLATES else None
    for k in keys:
        im = process(k, JOBS[k], plate).convert("RGB")
        im.save(os.path.join(OUT, k + ".png"), optimize=True)
        print(k, im.size, im.mode)


if __name__ == "__main__":
    main()
