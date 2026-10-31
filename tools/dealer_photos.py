#!/usr/bin/env python3
"""Machine and accessory photos from the Polish Dener / Şahinler / Bekamak distributor's website (Dener: dn-*, the NovoTech premium
line built by Şahinler: shd-*), used with the
distributor's permission (the owner, Oct 31 2026: machine photos and accessory close-ups only — no photos taken at
customers' plants — and the distributor's marks removed).

The chosen files were downloaded once through the owner's browser and copied under their site keys to
/home/claude/dealer-pl/<key>.<ext>.  The distributor's name plates on the machines, the badge on the sample-part photos
and on-screen marks are filled with LaMa (tools/lama_inpaint.py); renders on white are cut out later by
tools/make_images.py (BiRefNet), accessory close-ups keep their background.

    python3 tools/dealer_photos.py [key …]     → tools/src-images/dealer-pl/<key>.jpg and the tools/image_map.json entries
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/dealer-pl/"
DST = os.path.join(ROOT, "tools", "src-images", "dealer-pl")
BIG = 1800

PLATE_DDM = [(424, 109, 486, 158)]


def P(alt, boxes=(), cut=True, section="dener", clone=(), crop=None, polys=(), strokes=(), plates=()):
    return dict(alt=alt, boxes=list(boxes), cut=cut, section=section, clone=list(clone), crop=crop, polys=list(polys),
                strokes=list(strokes), plates=list(plates))


def S(alt, boxes=(), cut=True, **kw):    # NovoTech premium line (Şahinler-built): the maker's name and the distributor's marks go
    return P(alt, boxes, cut=cut, section="sahinler", **kw)


# key: alt / caption, boxes (x0, y0, x1, y1 in source pixels) filled by LaMa, cut = BiRefNet cut-out (False: keep the scene);
# clone (x0, y0, x1, y1, dx, dy): a plate on a plain panel is covered with the panel next to it (offset dx, dy), feathered —
# for spots where LaMa invents a badge from the logo above
PHOTOS = {
    # ---- Dener XL hydraulic press brakes and tandem
    "dn-xl-4000x600": P("Dener XL 4000 × 600: 661 US tons (600 t) × 13 ft hydraulic CNC press brake, with the CNC control on its swing arm "
                        "and the foot pedal", [(550, 348, 590, 380)]),
    "dn-xl-4000x320": P("Dener XL 4000 × 320: 353 US tons (320 t) × 13 ft, front view with the front sheet supports, the foot pedal and "
                        "the CNC control on its swing arm", [(634, 362, 697, 412)]),
    "dn-tandem-6000x600": P("Tandem of two XL 6000 × 600 press brakes: 40 ft and 1,323 US tons (1,200 t) bent from one control",
                            [(402, 342, 434, 364), (1050, 337, 1083, 357)]),
    "dn-xl-wila": P("Wila New Standard upper tool holder on the ram — Wila mechanical or hydraulic tool clamping is optional on the XL",
                    cut=False),
    # the owner's set (sent in the chat, Oct 31 2026): the distributor's plate on each ram and its logo on the control screens filled
    "dn-xl-3000x220": P("Dener XL 3000 × 220: 243 US tons (220 t) × 10 ft hydraulic CNC press brake, with the CNC control on its swing arm, "
                        "the front sheet supports and the foot pedal", [(432, 251, 480, 290)]),
    "dn-xl-tandem-3000x320": P("Tandem of two XL 3000 × 320 press brakes: 20 ft and 706 US tons (640 t) bent from one control, or each "
                               "machine on its own", [(424, 271, 471, 307), (122, 441, 155, 455), (1305, 443, 1338, 456)],
                               clone=[(1015, 268, 1076, 316, 70, 0)]),
    "dn-xl-tandem-4000x320": P("Tandem of two XL 4000 × 320 press brakes: 26 ft and 706 US tons (640 t) bent from one control, with a CNC "
                               "control at each end", [(1405, 397, 1434, 411)],
                               clone=[(403, 317, 454, 358, 60, 0), (1007, 317, 1057, 358, 60, 0)]),
    "dn-xl-tandem-4000x320-shop": P("Tandem XL 4000 × 320 press brakes in the shop: two 13 ft machines that bend 26 ft parts together or work "
                                    "apart", cut=False, clone=[(247, 317, 278, 346, 40, 0), (611, 310, 649, 343, 45, 0)]),
    "dn-xl-throat-frames": P("Deep throats in the XL side frames, seen along the machine: tall flanges on long parts pass into the frames",
                             cut=False),
    "dn-xl-bg-fingers": P("Back gauge fingers of the XL, sliding along the beam on its linear guide", cut=False),
    "dn-sheet-followers": P("Two CNC sheet followers in front of a Dener press brake: they rise with the sheet through the bend, so large, "
                            "thin sheets do not sag or whip back", [(580, 82, 642, 125)], cut=False),
    # ---- Dener DDM servo-electric and DDS ball-screw press brakes
    "dn-ddm-5020": P("Dener DDM 5020 servo-electric press brake: 55 US tons (50 t) × 6.7 ft, front view", PLATE_DDM),
    "dn-ddm-5020-side": P("Dener DDM 5020 servo-electric press brake — three-quarter view with the front supports and the foot pedal",
                          [(670, 176, 719, 231)]),
    "dn-dds-4013": P("Dener DDS 4013 ball-screw electric press brake: 44 US tons (40 t) × 4.3 ft, with the CNC control on its swing arm "
                     "and the foot pedal", [(462, 180, 514, 222)]),
    "dn-dds-ballscrew": P("DDS ram drive: the servo motor turns a ball screw that moves the ram — no cylinders, no hydraulic oil", cut=False),
    # ---- Dener DAS guillotine and BS swing beam shears
    "dn-das-3006": P("Dener DAS 3006 CNC hydraulic guillotine shear: 1/4″ (6 mm) × 10 ft, with the CNC control on its arm"),
    "dn-das-6006": P("Dener DAS 6006 CNC hydraulic guillotine shear: 1/4″ (6 mm) × 20 ft, with the front support arms",
                     [(482, 288, 515, 321)]),
    "dn-bs-3013": P("Dener BS 3013 hydraulic swing beam shear: 1/2″ (13 mm) × 10 ft, with the NC control and the foot pedal",
                    [(572, 138, 616, 176)]),
    "dn-bs-3010": P("Dener BS 3010 hydraulic swing beam shear: 3/8″ (10 mm) × 10 ft", [(624, 178, 653, 213)]),
    "dn-bs-3006": P("Dener BS 3006 hydraulic swing beam shear: 1/4″ (6 mm) × 10 ft, with the rear guard fence", [(569, 263, 629, 318)]),
    "dn-bs-panel": P("HT 071 NC control on the BS: back gauge position, programs and stroke counter, with the mode switches below",
                     cut=False),
    # ---- Dener GFL fiber laser
    "dn-gfl-3015": P("Dener GFL 3015 fiber laser cutting machine: 5 × 10 ft table, enclosed cabin and pallet changer"),
    "dn-gfl-6020": P("Dener GFL 6020 fiber laser cutting machine: 6.6 × 20 ft table with the pallet changer",
                     clone=[(254, 238, 292, 272, 0, 44)]),
    "dn-gfl-open": P("GFL with the cabin door open: the cutting head on the gantry, and the CNC control on its arm"),
    "dn-gfl-frame": P("GFL frame: stress-relieved welded bed, the gantry with the cutting head, and the pallet changer"),
    "dn-gfl-head": P("GFL cutting head on the Z axis, with the status light strips", cut=False),
    "dn-gfl-part": P("Sample part cut from thick steel plate on a GFL fiber laser", [(455, 695, 545, 730)], cut=False),
    "dn-gfl-sheet": P("Sample nest: S-shaped parts cut from one steel sheet on a GFL fiber laser", [(455, 695, 545, 730)], cut=False),

    # ---- NovoTech premium line (Şahinler-built): machine and detail photos from the distributor's product pages (the owner, Oct 31
    # 2026) — the maker's name plates and logos, the distributor's plates and the Polish-language labels are filled; photos with
    # people, with another maker's machine in the background or with Polish screens are left out, and so are the roll diagrams
    # (the owner prefers real photos to drawings). cut=True: a render on white, cut out by make_images.
    # 4-roll heavy-duty 4R HSS
    "shd-4rhss-render": S("4R HSS heavy-duty 4-roll plate roll with the overhead support, the side supports and the NC console",
                          [(706, 458, 755, 485)]),
    "shd-4rhss-40-550": S("4R HSS 40-550 NC: 13.5 ft heavy-duty 4-roll plate roll at its NC console", cut=False),
    "shd-4rhss-30-350": S("4R HSS 30-350 set in a pit, with the overhead support and the hydraulic side supports", cut=False),
    "shd-4rhss-cone": S("Rolling a cone on a 4R HSS: the overhead crane holds the shell while it rolls", [(259, 558, 292, 618)], cut=False),
    "shd-4rhss-shell": S("Shell rolled on a 4R HSS", cut=False),
    # 4R HS orbital
    "shd-4rhs-render": S("4R HS hydraulic 4-roll plate roll with the overhead support and the mobile console", [(818, 578, 872, 609)]),
    "shd-4rhs-25-260": S("4R HS 20-260: 6.7 ft hydraulic 4-roll plate roll", [(818, 88, 858, 115), (750, 25, 795, 75)], cut=False),
    "shd-4rhs-25-260-b": S("4R HS 25-260 NC, 8.4 ft, with both side supports raised", [(275, 150, 312, 178)], cut=False),
    "shd-4rhs-cone-part": S("Cone rolled on a 4R HS", cut=False),
    # 4R HS-L linear
    "shd-4rhsl-render": S("4R HS-L linear 4-roll plate roll with the NC console", [(182, 76, 224, 105), (82, 133, 122, 172)]),
    "shd-4rhsl-650-110": S("4R HS-L NC with its electrical cabinet", [(410, 192, 472, 230), (262, 322, 348, 386)], cut=False),
    "shd-4rhsl-rolls": S("4R HS-L from above: the top roll, the pinch roll and the two side rolls, with the pinch pressure regulator",
                         strokes=[([(828, 731), (888, 731), (888, 766), (828, 766)], "dark")], cut=False),
    "shd-4rhsl-guides": S("Linear guides of the side rolls on the 4R HS-L", cut=False),
    "shd-4rhsl-lube": S("Central lubrication pump on the 4R HS-L", crop=(0, 0, 540, 1000), cut=False),
    "shd-4rhsl-parts": S("Tubes rolled on a 4R HS-L", cut=False),
    # 4R HC conical
    "shd-4rhc-render": S("4R HC 10-155 conical 4-roll plate roll with its console", [(354, 280, 430, 331)]),
    "shd-4rhc-render-b": S("4R HC from the roll end: the conical rolls between the feed tables", [(353, 553, 396, 600)],
                           strokes=[([(686, 560), (714, 560), (714, 582), (686, 582)], "dark")]),
    "shd-4rhc-console": S("4R HC 10-185 with its console: digital read-outs for every roll", [(786, 130, 832, 174), (150, 328, 186, 398)],
                          cut=False),
    "shd-4rhc-cone": S("Rolling a cone on the 4R HC", cut=False),
    "shd-4rhc-parts": S("Cones rolled on the 4R HC", cut=False),
    # 4RH cassette
    "shd-4rh-render": S("4RH 10-75 NC cassette-type 4-roll plate roll with the feed table and the NC console",
                        [(356, 306, 400, 354), (327, 311, 357, 326)]),
    "shd-4rh-top": S("4RH 10-75 NC from above: the rolls in their cassette frame and the feed table", cut=False),
    "shd-4rh-table": S("4RH from the drop end: the pressure gauges and the feed table", [(223, 318, 252, 331)], cut=False),
    "shd-4rh-rolled": S("Sheet rolled on the 4RH, with the pinch pressure regulator in front",
                        strokes=[([(518, 822), (572, 822), (572, 852), (518, 852)], "dark")], cut=False),
    # 3R HS
    "shd-3rhs-render": S("3R HS 20-240 3-roll hydraulic plate roll with its console", [(90, 54, 147, 81)]),
    # HPK section benders
    "shd-hpk40-render": S("HPK 40 NC hydraulic section and pipe bender with the NC console", [(466, 398, 542, 535)]),
    "shd-hpk40-rolls": S("HPK 40 rolls with the side guide rolls", crop=(0, 130, 1000, 720), cut=False),
    "shd-hpk40-horizontal": S("HPK 40 tipped over to bend horizontally", [(567, 436, 596, 471), (404, 44, 464, 64)], cut=False),
    "shd-hpk50-render": S("HPK 50 hydraulic section and pipe bender with the foot pedal", [(91, 461, 183, 512)]),
    "shd-hpk50-render-b": S("HPK 50 NC with the NC console", [(468, 545, 548, 735)]),
    "shd-hpk60-render": S("HPK 60 NC with the NC console", [(138, 604, 264, 812), (402, 718, 432, 760)]),
    "shd-hpk60-cylinder": S("HPK 60 from above: the hydraulic cylinder of the top roll", [(618, 252, 730, 442)], cut=False),
    "shd-hpk60-guides": S("HPK 60 rolls and the side guide roll", cut=False),
    "shd-hpk50-nc": S("NC control of the HPK 50 and 60: the roll positions on the touch screen", [(384, 159, 444, 181)], cut=False),
    "shd-hpk65-horizontal": S("HPK 65 NC set up to bend horizontally, with the NC console", [(498, 490, 525, 528)],
                              polys=[[(652, 110), (678, 95), (776, 95), (776, 133), (738, 148), (684, 148), (652, 137)]]),
    "shd-hpk80-render": S("HPK 80 NC hydraulic section and pipe bender with the NC console", [(354, 606, 508, 688), (48, 88, 76, 188)]),
    "shd-hpk65-poly-rolls": S("HPK 65 with polyamide rolls, for stainless and aluminum profiles that must not be marked",
                              [(505, 590, 752, 738), (852, 372, 1000, 428)],
                              polys=[[(0, 115), (162, 115), (312, 150), (312, 228), (110, 228), (0, 198)]], cut=False),
    "shd-hpk65-spiral": S("Spiral rolled from bar on the HPK 65", crop=(0, 0, 1000, 870), cut=False),
    "shd-hpk80-rolls-h": S("HPK 80 rolls bending horizontally, with the side guide roll", cut=False),
    "shd-hpk100-render": S("HPK 100 NC with the NC console", [(505, 455, 575, 548)]),
    "shd-hpk120-render": S("HPK 120 with its hydraulic side guides and the console", [(313, 497, 388, 565), (530, 532, 614, 604)]),
    "shd-hpk120-render-b": S("HPK 120 from the side, with the console", [(74, 120, 158, 192), (420, 500, 480, 582)]),
    "shd-hpk120-rear": S("HPK 120 from the rear: the electrical cabinet and the hydraulic unit", [(366, 61, 534, 161)]),
    "shd-hpk120-guide": S("Hydraulic side guide of the HPK 120", [(574, 600, 642, 708)], cut=False),
    "shd-hpk160-horizontal": S("HPK 160 bending horizontally, with the oil cooler and the console",
                               strokes=[([(694, 259), (750, 259), (750, 305), (694, 305)], "light")]),
    "shd-hpk160-render": S("HPK 160 bending an I-beam vertically between its hydraulic side guides", [(510, 554, 614, 621)]),
    "shd-hpk200-render": S("HPK 200 heavy-duty section and beam bender", [(811, 309, 886, 364)]),
    "shd-hpk240-render": S("HPK 240 DP heavy-duty section and beam bender with the console", [(280, 270, 401, 350), (818, 171, 888, 236)]),
    "shd-hpk360-render": S("HPK 360 heavy-duty section and beam bender", [(745, 285, 886, 360)]),
    "shd-hpk160-rolls": S("HPK 160 from above: the three rolls and the hydraulic side guides", cut=False),
    # TC-42 NC tube coiler
    "shd-tc42-render": S("TC-42 NC tube coiling machine with a coil, the NC console and the coil support", plates=[(360, 568, 610, 692)]),
    "shd-tc42-render-b": S("TC-42 NC from the side", plates=[(470, 450, 655, 615)]),
    "shd-tc42-coil": S("Tube coil on the TC-42 NC", cut=False),
    "shd-tc42-control": S("TC-42 NC console", [(150, 212, 218, 274), (340, 216, 396, 248)], cut=False),
    "shd-tc42-rolls": S("TC-42 rolls and the side supports", cut=False),
    "shd-tc42-bending-rolls": S("Bending rolls of the TC-42", cut=False),
    # DK-S straightening presses
    "shd-dks-render": S("DK-S 300 3-axis moving straightening press", [(311, 208, 331, 221), (779, 334, 816, 357)],
                        strokes=[([(498, 213), (597, 213), (597, 268), (498, 268)], "light")]),
    "shd-dks300-render": S("DK-S 300 from the front, with the pendant control", [(230, 180, 258, 195), (649, 290, 670, 303)],
                           strokes=[([(457, 195), (539, 195), (539, 243), (457, 243)], "light")]),
    "shd-dks-side": S("DK-S from the side: the press head travels over the table", cut=False),
    "shd-dks-table": S("DK-S grid table under the press head", cut=False),
    "shd-dks-piston": S("DK-S pressing tool", cut=False),
    # SDK circle cutting and flanging
    "shd-sdk8-render": S("SDK 8 circular sheet cutting and flanging machine", [(310, 170, 336, 196)]),
    "shd-sdk8-rolls": S("SDK 8 cutting and flanging rolls", [(700, 2, 750, 78), (742, 104, 771, 139)], cut=False),
    "shd-sdk8-panel": S("SDK 8 control panel with the touch screen and the pendant", [(468, 132, 498, 147), (770, 164, 834, 216),
                                                                                      (786, 213, 821, 235)], cut=False),
    "shd-sdk8-part": S("Dished head flanged on the SDK 8", cut=False),
    "shd-sdk8-edge": S("Flanged edge of a dished head made on the SDK 8", cut=False),
    "shd-sdk8-head": S("Dished head on the SDK 8", cut=False),
    # EFM elliptical cutting and flanging
    "shd-efm6-render": S("EFM 6 elliptical cutting and flanging machine",
                         strokes=[([(113, 375), (223, 348), (225, 377), (116, 408)], "light")]),
    "shd-efm6-render-b": S("EFM 6 with a sheet held on the vacuum cups",
                           strokes=[([(200, 258), (254, 258), (254, 274), (200, 274)], "light")], cut=False),
    "shd-efm6-bending-rolls": S("EFM 6 flanging head", crop=(240, 60, 1000, 786), cut=False),
    "shd-efm6-cutting-rolls": S("EFM 6 cutting head", [(514, 483, 611, 561)], cut=False),
    "shd-efm6-clamping": S("Vacuum cups of the EFM 6 holding the sheet", cut=False),
    "shd-efm6-part": S("Elliptical head cut and flanged on the EFM 6", cut=False),
}


def flat_fill(rgb, x0, y0, x1, y1, ring=5, seed=7):
    """A plate on a plain painted panel: fit a plane (per channel) to a ring of panel pixels around the box, rejecting outliers
    (the edge of a neighbouring label, a cable), and fill the box with it plus grain of the same strength, feathered by 2 px.
    LaMa tends to invent textures or a new badge on a large plain area; this does not."""
    import numpy as np
    H, W = rgb.shape[:2]
    X0, Y0, X1, Y1 = max(0, x0 - ring), max(0, y0 - ring), min(W, x1 + ring), min(H, y1 + ring)
    yy, xx = np.mgrid[Y0:Y1, X0:X1]
    sel = ~((xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1))
    px, py = xx[sel].astype(float), yy[sel].astype(float)
    val = rgb[Y0:Y1, X0:X1][sel].astype(float)
    A = np.stack([np.ones_like(px), px - x0, py - y0], 1)
    keep = np.ones(len(px), bool)
    for _ in range(3):
        coef, *_ = np.linalg.lstsq(A[keep], val[keep], rcond=None)
        res = np.abs(val - A @ coef).max(1)
        mad = np.median(res[keep]) + 1e-6
        keep = res < max(6.0, 3.0 * mad)
    resid = (val - A @ coef)[keep]
    noise = resid.std(0) * 0.8
    gy, gx = np.mgrid[y0:y1, x0:x1]
    fill = coef[0] + (gx - x0)[..., None] * coef[1] + (gy - y0)[..., None] * coef[2]
    rng = np.random.default_rng(seed)
    import cv2
    grain = cv2.GaussianBlur(rng.normal(0, 1, fill.shape).astype(np.float32), (0, 0), 0.7) * noise
    fill = np.clip(fill + grain, 0, 255)
    m = np.zeros((y1 - y0, x1 - x0), np.float32); m[2:-2, 2:-2] = 1
    m = cv2.GaussianBlur(m, (0, 0), 1.2)[..., None]
    region = rgb[y0:y1, x0:x1].astype(float)
    rgb[y0:y1, x0:x1] = np.clip(region * (1 - m) + fill * m, 0, 255).astype(np.uint8)
    # the 2 px border keeps a blend of the old pixels: overwrite it with the fill where the old pixel was far from the panel
    return rgb


def fill_boxes(im, boxes):
    """One box at a time: LaMa (lama_inpaint works on a window around the whole mask, so boxes far apart — the plates on two
    machines of a tandem — would share one big, downscaled window), or "flat" (flat_fill) for a plate on a plain panel."""
    import numpy as np
    from lama_inpaint import inpaint
    rgb = np.asarray(im.convert("RGB")).copy()
    for b in boxes:
        x0, y0, x1, y1 = b[:4]
        if len(b) > 4 and b[4] == "flat":
            rgb = flat_fill(rgb, x0, y0, x1, y1)
            continue
        mask = np.zeros(rgb.shape[:2], np.uint8)
        mask[y0:y1, x0:x1] = 255
        rgb = inpaint(rgb, mask)
    return Image.fromarray(rgb)


def fill_masks(im, p):
    """Polygons (LaMa; {"pts": [...], "keep": "dark" | "yellow"} leaves the cables or a yellow guard bar crossing the plate out of
    the mask), text strokes inside a polygon (mode "dark": letters darker than their label, "light": lighter than their plate —
    the label or plate itself stays; filled by OpenCV TELEA, which leaves no ghost letters on a plain plate) and cream plates
    (the letters inside the largest cream area of a box: the octagonal name plate of the TC-42, TELEA as well)."""
    import cv2
    import numpy as np
    from PIL import ImageDraw
    from lama_inpaint import inpaint
    rgb = np.asarray(im.convert("RGB")).copy()
    H, W = rgb.shape[:2]

    def poly_mask(pts):
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon([tuple(q) for q in pts], fill=255)
        return np.asarray(m) > 0

    for poly in p.get("polys", []):
        pts, keep = (poly["pts"], poly.get("keep")) if isinstance(poly, dict) else (poly, None)
        m = poly_mask(pts)
        if keep == "dark":
            m &= cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY) > 90
        elif keep == "yellow":
            r, g, b = rgb[..., 0].astype(int), rgb[..., 1].astype(int), rgb[..., 2].astype(int)
            m &= ~((r > 150) & (g > 120) & (b < 110) & (r - b > 80))
        m = cv2.dilate(m.astype(np.uint8) * 255, np.ones((3, 3), np.uint8))
        if m.any():
            rgb = inpaint(rgb, m)
    for poly, mode in p.get("strokes", []):
        inside = poly_mask(poly)
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(int)
        med = int(np.median(gray[inside]))
        sel = gray < med - 28 if mode == "dark" else gray > med + 28
        m = (inside & sel).astype(np.uint8) * 255
        m = cv2.dilate(m, np.ones((5, 5), np.uint8)) & (inside.astype(np.uint8) * 255)
        if m.any():
            rgb = cv2.inpaint(rgb, m, 4, cv2.INPAINT_TELEA)
    for x0, y0, x1, y1 in p.get("plates", []):
        sub = rgb[y0:y1, x0:x1].astype(int)
        cream = (((sub.max(2) - sub.min(2)) < 45) & (sub.max(2) > 150)).astype(np.uint8) * 255
        cream = cv2.morphologyEx(cream, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
        n, lab, stats, _ = cv2.connectedComponentsWithStats(cream)
        comp = (lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
        cnts, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hm = np.zeros_like(comp); cv2.fillConvexPoly(hm, cv2.convexHull(np.vstack(cnts)), 1)
        hm = cv2.erode(hm, np.ones((7, 7), np.uint8))
        gray = cv2.cvtColor(sub.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        text = cv2.dilate(((hm > 0) & (gray < 130)).astype(np.uint8) * 255, np.ones((7, 7), np.uint8)) & (hm * 255)
        m = np.zeros((H, W), np.uint8); m[y0:y1, x0:x1] = text
        if m.any():
            rgb = cv2.inpaint(rgb, m, 5, cv2.INPAINT_TELEA)
    return Image.fromarray(rgb)


def trim(im, thr=242, pad=14):
    g = im.convert("L").point(lambda v: 255 if v < thr else 0)
    bb = g.getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def source(key):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if os.path.exists(SRC + key + ext):
            return SRC + key + ext
    raise SystemExit(f"no source for {key} in {SRC}")


def process(key):
    p = PHOTOS[key]
    im = Image.open(source(key))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im)
    im = im.convert("RGB")
    for x0, y0, x1, y1, dx, dy in p.get("clone", []):
        from PIL import ImageFilter
        patch = im.crop((x0 + dx, y0 + dy, x1 + dx, y1 + dy))
        mask = Image.new("L", patch.size, 0)
        mask.paste(255, (3, 3, patch.width - 3, patch.height - 3))
        im.paste(patch, (x0, y0), mask.filter(ImageFilter.GaussianBlur(2)))
    if p["boxes"]:
        im = fill_boxes(im, p["boxes"])
    if p.get("polys") or p.get("strokes") or p.get("plates"):
        im = fill_masks(im, p)
    if p.get("crop"):
        im = im.crop(p["crop"])
    if p["cut"]:
        im = trim(im)
    if max(im.size) > BIG:
        f = BIG / max(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    os.makedirs(DST, exist_ok=True)
    im.save(os.path.join(DST, key + ".jpg"), quality=92)
    return im.size


def register(keys):
    path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(path, encoding="utf-8"))
    for k in keys:
        p = PHOTOS[k]
        imap[k] = {"src": f"tools/src-images/dealer-pl/{k}.jpg", "alt": p["alt"], "section": p["section"], "trim": p["cut"],
                   "quality": 82, "cutout": p["cut"], "cut_size": 1024}
    json.dump(imap, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for k in keys:
        print(f"{k:22s} {process(k)}")
    register(keys)


if __name__ == "__main__":
    main()
