#!/usr/bin/env python3
"""Dener photos → tools/src-images/dener/<key>.(png|jpg).

Sources (staged from the user's laptop, …\\DENER\\): `render/` — Dener's 2026 product renders, PNG with a real alpha channel
(no cut-out needed, `trim` only); `video/` — frames from Dener's videos (rectangular, cutout=False); `web/` — the product
photos Dener used on its website.  Renders above 2,800 px are downscaled on export.  Dener is shown under its own brand, so
its logo stays on the machines.

    python3 tools/dener_photos.py        export
"""
import os
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/dener/"
OUT = os.path.join(ROOT, "tools", "src-images", "dener")


def R(name, alt, **kw):          # render with alpha
    return dict(src="render/" + name, alt=alt, cutout=False, trim=True, **kw)


def V(name, alt, **kw):          # video frame / photo, rectangular
    return dict(src="video/" + name, alt=alt, cutout=False, trim=False, **kw)


def W(name, alt, **kw):          # website photo
    return dict(src="web/" + name, alt=alt, cutout=False, trim=False, **kw)


PHOTOS = {
    # XL hydraulic
    "dn-xl-1": R("XL-1.png", "Dener XL hydraulic CNC press brake — front view with the ESA control on its swing arm"),
    "dn-xl-2": R("XL-2.png", "Dener XL hydraulic CNC press brake — three-quarter view"),
    "dn-xl-3": R("XL-3.png", "Dener XL hydraulic press brake, long bed — three-quarter view"),
    # the six detail photos of Dener's XL page (denerusa.com) with Dener's captions — the owner, Oct 30 2026
    "dn-xl-throat": W("puma-xl-2-1.jpg", "More throat depth and stroke: with the XL's high daylight, long stroke and deep throat, large and small parts of every size bend easily"),
    "dn-xl-xr-gauge": W("puma-xl-1.jpg", "X, R axis back gauge — the element that decides the accuracy of precise parts: single or multi-step parts on up to 6 axes, ±0.03 mm (±0.001″) on the X axis"),
    "dn-xl-esa-screen": W("puma-xl-6-1.jpg", "ESA control: the part is drawn on the screen, and the automatic bend sequence lets the operator follow every bend and finds the fastest way to bend the part"),
    "dn-xl-ram-slide": W("puma-xl-4-1.jpg", "Strong ram slide system: the slides on the frame guide the upper beam for a steadier, more precise stroke"),
    "dn-xl-front-arms": W("puma-xl-5-1.jpg", "Heavy-type front support arms on linear slides, on the XL of 193 US tons (175 t) and up"),
    "dn-xl-euro-tooling": W("puma-xl-7.jpg", "European-type punch and die systems — tooling for bending thick material, chosen for the customer's work"),
    "dn-xl-control": R("XL-4.png", "Dener XL — ESA S875 W 21.5″ 3D CNC control on the swing arm"),
    "dn-xf-1": R("XF-1.png", "Dener XL 1560 / 2060 compact hydraulic press brake, 5 – 6.7 ft"),
    "dn-xf-2": R("XF-2.png", "Dener XL hydraulic press brake — front view"),
    "dn-xf-3": R("XF-3.png", "Dener XL — control arm and front support"),
    "dn-xl-video-1": V("Hydraulic Press Brake - Puma XL 175x3000_Moment32.jpg", "Dener XL 30175 — 10 ft × 193 US tons hydraulic press brake bending"),
    "dn-xl-video-2": V("PUMA XL 30175 - 7 Axis Hydraulic Press Brake_Moment47.jpg", "Dener XL 30175 with 7-axis back gauge"),
    "dn-xl-backgauge": V("Dener ATF 6 Axis Back Gauge_Moment2.jpg", "Dener ATF 6-axis back gauge — X1, X2, R1, R2, Z1, Z2"),
    "dn-xl-follower": V("CNC Sheet Follower for Press Brakes_Moment12.jpg", "CNC sheet follower supporting a large sheet during the bend"),
    # XH hybrid
    "dn-xh-1": R("XH-1.png", "Dener XH full hybrid press brake — front view"),
    "dn-xh-2": R("XH-2.png", "Dener XH full hybrid press brake — three-quarter view"),
    "dn-xh-3": R("XH-3.png", "Dener XH full hybrid — the CNC control on its swing arm"),
    "dn-xh-4": R("XH-4.png", "Dener press brake — European-style segmented punch and die with hydraulic clamping"),
    "dn-xh-video": V("Hibrit Abkant Pres_Moment28.jpg", "Dener hybrid press brake in production"),
    # DDM servo-electric
    "dn-ddm-1": R("DDM-1.png", "Dener DDM servo-electric CNC press brake — front view with ESA S875 W control"),
    "dn-ddm-2": R("DDM-2 copy.png", "Dener DDM servo-electric press brake — three-quarter view"),
    "dn-ddm-3": R("DDM-2.png", "Dener DDM servo-electric press brake, 13 ft — side view"),
    "dn-ddm-control": R("DDM-3.png", "Dener DDM — ESA S875 W 21.5″ 3D touchscreen control"),
    "dn-ddm-video-1": V("DENER SERVO BRAKE 3 MT. 150 TON_Moment17.jpg", "Dener DDM 15030 — 10 ft × 165 US tons servo-electric press brake"),
    "dn-ddm-video-2": V("Dener Servo Brake 200x40_Moment22.jpg", "Dener DDM 4015 servo-electric press brake bending"),
    "dn-ddm-web-1": W("Servo Brake 4015 + ESA675 + KUKA Robot.png", "Dener DDM 4015 servo-electric press brake in a KUKA robot bending cell"),
    "dn-ddm-web-2": W("Servo 10030 Front BG.JPG", "Dener DDM 10030 servo-electric press brake with the back gauge — front view"),
    # DDS ball-screw
    "dn-dds-1": R("DDS-1.png", "Dener DDS ball-screw electric press brake — three-quarter view"),
    "dn-dds-2": R("DDS-2.png", "Dener DDS 2090 ball-screw press brake — compact front view"),
    "dn-dds-3": R("DDS-3.png", "Dener DDS — ball-screw drive and back gauge"),
    "dn-dds-4": R("DDS-4.png", "Dener DDS — ESA S840 15.6″ touch-screen control pendant"),
    "dn-dds-video": V("Ball Screw Press Brake DDS-4013_Moment3.jpg", "Dener DDS 4013 ball-screw press brake bending a bracket"),
    # shears
    "dn-bs-1": R("BS-1.png", "Dener BS hydraulic swing beam shear — front view"),
    "dn-bs-2": R("BS-2.png", "Dener BS hydraulic swing beam shear — three-quarter view with the NC control"),
    "dn-bs-3": R("BS-3.png", "Dener BS swing beam shear — rear three-quarter view"),
    "dn-das-1": R("DAS-1.png", "Dener DAS CNC hydraulic guillotine shear — front view"),
    "dn-das-2": R("DAS-2.png", "Dener DAS CNC guillotine shear with the ESA 630 control arm"),
    "dn-das-3": R("DAS-3.png", "Dener DAS CNC guillotine shear — three-quarter view"),
    "dn-shear-video-1": V("Shearing Machines - DENER MACHINERY_Moment 15.jpg", "Dener shear cutting plate — the sheet on the slider table"),
    "dn-shear-video-2": V("Hidrolik  Giyotin Makas_2_Moment2.jpg", "Dener hydraulic guillotine shear in production"),
    "dn-shear-web": W("Makas AS-3006 (1).JPG", "Dener AS 3006 CNC hydraulic shear — 10 ft × 1/4″"),
    # GFL
    "dn-gfl-1": R("GFL-ELO PANEL 2.png", "Dener GFL fiber laser cutting machine — closed cabin, front-left view"),
    "dn-gfl-2": R("GFL-ELO PANEL 3.png", "Dener GFL fiber laser — pallet changer with the second table out"),
    "dn-gfl-3": R("GFL-ELO PANEL 4.png", "Dener GFL fiber laser cutting machine — three-quarter view"),
    "dn-gfl-4": R("GFL-ELO PANEL 5.png", "Dener GFL fiber laser with the pallet changer — right view"),
    "dn-gfl-5": R("GFL-ELO PANEL 6.png", "Dener GFL fiber laser — control side"),
    "dn-gfl-control": R("GFL-ELO PANEL 1.png", "Dener GFL — CNC control and remote handset"),
    "dn-gfl-video-1": V("Dener FL Series Fiber Laser Technology_Moment3.jpg", "Dener fiber laser cutting head at work"),
    "dn-gfl-video-2": V("Fiber Laser FL-6020-6KW - New Features for High Speed and Performance_Moment4.jpg", "Dener 6 kW fiber laser cutting mild steel"),
    "dn-laser-web": W("Lazer (1).JPG", "Dener fiber laser cutting machine on the shop floor"),
    # Smart
    "dn-smart-1": R("smart etiketli.png", "Dener Smart Laser 6020 fiber laser cutting machine — closed type with exchange table"),
    "dn-smart-2": R("smart arka.png", "Dener Smart fiber laser — exchange table out, rear view"),
    # tube lasers
    "dn-tube-1": R("6025.png", "Dener E-FTL tube and profile fiber laser — chucks and following supports"),
    "dn-tube-2": R("6025G.png", "Dener E-FTL tube laser with the automatic bundle loader"),
    "dn-tube-3": R("6025 (3).png", "Dener E-FTL tube laser — loading side"),
    "dn-tube-4": R("12036.png", "Dener FTL tube and profile fiber laser, 12 m — full line"),
    "dn-tube-5": R("12036 (2).png", "Dener FTL 12 m tube laser — loader and cutting cell"),
    "dn-tube-6": R("12036t.png", "Dener FTL tube laser — three-quarter view"),
    "dn-tube-7": R("6025G (4).png", "Dener tube laser — bundle loader detail"),
    # panel bender
    "dn-panel-1": R("2.png", "Dener CNC panel bender — three-quarter view"),
    "dn-panel-2": R("1.png", "Dener CNC panel bender — front view with the manipulator"),
    "dn-panel-3": R("4.png", "Dener CNC panel bender — right view"),
    "dn-panel-4": R("5.png", "Dener CNC panel bender — left view"),
    "dn-panel-5": R("10.png", "Dener panel bender — bending blades and blank-holder"),
    "dn-panel-6": R("6.png", "Dener panel bender — bending unit detail"),
    "dn-panel-7": R("9.png", "Dener CNC panel bender — rear three-quarter view"),
}


def export(keys=None):
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for k in keys or PHOTOS:
        p = PHOTOS[k]
        src = SRC + p["src"]
        ext = ".png" if p["src"].lower().endswith(".png") else ".jpg"
        dst = os.path.join(OUT, k + ext)
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            continue
        im = Image.open(src)
        if ext == ".png":
            im = im.convert("RGBA")
            if im.width > 2800:
                im = im.resize((2800, round(im.height * 2800 / im.width)), Image.LANCZOS)
            im.save(dst, optimize=True)
        else:
            im = im.convert("RGB")
            if im.width > 2400:
                im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
            im.save(dst, quality=92)
        n += 1
    print(f"dener photos: {n} exported, {len(PHOTOS)} total in {OUT}")


if __name__ == "__main__":
    export(sys.argv[1:] or None)
