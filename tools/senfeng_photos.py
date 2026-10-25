#!/usr/bin/env python3
"""Senfeng photos → tools/src-images/senfeng/<key>.(png|jpg).

Sources (outside the repository, /home/claude/senfeng/): `pdfimg/` — the renders embedded in Senfeng's series leaflets and
brochures (extracted with pdfimages; most come as an RGB image plus a separate soft mask, which `M()` combines into an RGBA
cut-out — the mask's floor shadow is dropped by thresholding the alpha, so only the machine is left), and `img/` — the
800 px renders and photos from senfenglaserusa.com (renders on a light-grey studio background are cut out by BiRefNet
with `cutout=True`, scene photos and diagrams stay photos).  Senfeng is sold under its own brand, so the logo stays.

    python3 tools/senfeng_photos.py        export
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/senfeng/"
OUT = os.path.join(ROOT, "tools", "src-images", "senfeng")
P = "pdfimg/"


def M(dir_, img, mask, alt, **kw):      # brochure render + soft mask → RGBA (no floor shadow)
    return dict(src=f"{P}{dir_}/{img}", mask=f"{P}{dir_}/{mask}", alt=alt, cutout=False, trim=True, **kw)


def R(name, alt, **kw):                 # website render on a studio background → BiRefNet
    return dict(src="img/" + name, alt=alt, cutout=True, trim=False, **kw)


def W(name, alt, **kw):                 # photo / diagram, kept as it is
    return dict(src="img/" + name, alt=alt, **{"cutout": False, "trim": False, **kw})


def PP(dir_, img, alt, **kw):           # brochure photo without a mask
    return dict(src=f"{P}{dir_}/{img}", alt=alt, cutout=False, trim=False, **kw)


# Extra keys on any entry: up=True — the 800 px website render is doubled with Real-ESRGAN (tools/esrgan.py) because Senfeng
# publishes nothing larger (both websites serve 600 – 800 px product images; the brochures are the only high-resolution
# source); delabel=True — the navy caption pill the website renders carry in the top-right corner ("Optional", "Robot", …)
# is found by colour and filled by LaMa; crop=(x0, y0, x1, y1) and rotate=deg are applied first.
def caption_pills(im):
    """Boxes of the navy rounded caption labels in the top-right quarter of a Senfeng website render."""
    import cv2
    rgb = np.asarray(im.convert("RGB")); H_, W_ = rgb.shape[:2]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
    m = ((h >= 95) & (h <= 130) & (s >= 60) & (v >= 30) & (v <= 170)).astype(np.uint8)
    m[int(H_ * 0.25):] = 0; m[:, :int(W_ * 0.35)] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 15), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    out = []
    for i in range(1, n):
        x, y, w, hh, a = st[i]
        if 0.08 * W_ <= w <= 0.5 * W_ and 0.03 * H_ <= hh <= 0.14 * H_ and a > 0.5 * w * hh and w > 2.2 * hh:
            out.append((int(x), int(y), int(x + w), int(y + hh)))
    return out


def delabel(im):
    boxes = caption_pills(im)
    if not boxes:
        print("   (no caption pill found)")
        return im
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from lama_inpaint import inpaint
    rgb = np.asarray(im.convert("RGB")).copy()
    mask = np.zeros(rgb.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes:
        mask[max(0, y0 - 6):y1 + 6, max(0, x0 - 6):x1 + 6] = 255
    out = Image.fromarray(inpaint(rgb, mask))
    if im.mode == "RGBA":
        out.putalpha(im.getchannel("A"))
    return out


def upscale2x(im):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from esrgan import upscale
    return upscale(im)


H = "High-Power-Fiber-Laser-Cutting-Machine-H"
HC = "Space-Saver-Fiber-Laser-Cutter-SF3015H"
NP = "Metal-Sheet-Laser-Cutter-SF3015NP"
G13 = "Metal-Sheet-Laser-Cutter-SF1313G"
TUBE = "Tube-Laser-Cutting-Machines-brochure"
PB = "Panel-Benders-brochure"
HWM = "Handheld-Welder-HWM-Series"
HW = "Handheld-Welder-HW-Series"
LW = "Laser-Welding-Machines-brochure"

PHOTOS = {
    # ---------------------------------------------------------------- sheet lasers
    "sf-h-1": M(H, "i-001-000.png", "i-001-001.png", "Senfeng SF3015H4 enclosed fiber laser cutting machine with pallet changer — 5 × 10 ft, 6 – 30 kW"),
    "sf-h-2": M(HC, "i-001-000.png", "i-001-001.png", "Senfeng SF3015H space-saver enclosed fiber laser — 5 × 10 ft, 1.5 – 12 kW"),
    "sf-h-tower": R("H4-Laser-Cutter-2-1.png", "H4 fiber laser with the optional loading / unloading tower and sheet storage", delabel=True, up=True),
    "sf-h-loader": PP("3015H-Automatic-Loading-Unloading", "i-001-000.png", "SF3015H with the automatic loading and unloading gantry", crop=(1270, 860, 2516, 1510)),
    "sf-h-line": PP("Automation-Machines-brochure", "i-003-003.png", "Automated laser line — gantry loader and sorting robot behind the laser"),
    "sf-h5": R("H5-01.png", "SF3015H5 heavy-load fiber laser for 40 – 80 kW sources", up=True),
    "sf-np-1": M(NP, "i-001-000.png", "i-001-001.png", "Senfeng SF3015NP open-type single-table fiber laser — 5 × 10 ft, 3 – 12 kW"),
    "sf-np-2": R("NP-2.webp", "NP series open-type laser — the table seen from the loading side", up=True),
    "sf-np-3": R("NP-5.webp", "NP series laser with the optional servo swing-arm loading manipulator", delabel=True, up=True),
    "sf-np-4": R("NP-6.webp", "NP series laser with the optional loading and unloading unit", delabel=True, up=True),
    "sf-np-scene": PP("Metal-Sheet-Fiber-Laser-Cutter-3015NP", "i-002-019.png", "NP series open-type laser on the shop floor"),
    "sf-1313g": dict(src=f"{P}{G13}/i-002-008.png", alt="Senfeng SF1313G compact fiber laser — 4 × 4 ft table, 1.5 – 3 kW", cutout=True, trim=False),
    "sf-1530g": R("1530G-1-1.webp", "Senfeng SF1530G enclosed fiber laser — 5 × 10 ft, 1.5 – 4 kW", up=True),
    "sf-1530n": R("1530N-1-1.webp", "Senfeng SF1530N enclosed fiber laser with pull-out single table — 5 × 10 ft, 1.5 – 12 kW", up=True),
    "sf-1530n-table": R("1530N-4.webp", "SF1530N — the single table pulled out for loading", up=True),
    "sf-1530np": R("1530NP-1.webp", "Senfeng SF1530NP fully enclosed compact fiber laser with electric lifting door — 5 × 10 ft, 1.5 – 6 kW", up=True),
    "sf-1530np-2": R("1530NP-4.webp", "SF1530NP — pull-out platform with integrated leg supports", up=True),
    "sf-1530np-head": W("1530NP-6.webp", "SF1530NP — autofocus cutting head over the slat table", up=True),
    "sf-sfp": R("P600-1.png", "Senfeng SFP600 high-precision fiber laser for small parts — 24 × 24″ table", up=True),
    "sf-hm-1": R("HM-01.webp", "Senfeng SF3015HM enclosed sheet and tube fiber laser — 5 × 10 ft table plus Ø8.6″ × 20 ft tube attachment", up=True),
    "sf-hm-2": R("HM-02.webp", "SF3015HM — the tube attachment on the side of the enclosure", up=True),
    "sf-hm-3": R("HM-03.webp", "SF3015HM — rear view with the tube support", up=True),
    "sf-hm-4": R("HM-05.webp", "Sheet and tube laser — enclosure doors open", up=True),
    "sf-r-1": R("R-1.webp", "Senfeng R series ultra-large plate laser — 10 ft wide table to 164 ft long, 6 – 60 kW", up=True),
    "sf-r-2": R("R-2.webp", "R series plate laser — gantry over the long table", up=True),
    "sf-tx-1": R("TX-1.webp", "Senfeng TX series plate laser with ±45° bevel head — 10 × 20 ft to 10 × 164 ft", up=True),
    "sf-tx-2": R("TX-2.webp", "TX series bevel plate laser — three-quarter view", up=True),
    "sf-txp": R("TXP-01.png", "Senfeng SF12030TXP laser and flame hybrid plate cutter — 20 kW laser plus oxy-fuel to 4″", up=True),
    "sf-r-cut": W("2026013016.webp", "R series laser cutting 4″ (100 mm) plate"),
    "sf-tx-flame": W("2026013058.webp", "TXP — laser and flame hybrid cutting of 4″ carbon steel plate with bevels"),
    "sf-3d-1": R("3015TD-1-1.webp", "Senfeng SF3015TD five-axis 3D fiber laser — 5 × 10 ft travel, 3 – 20 kW", up=True),
    "sf-3d-2": R("3015TD-3.webp", "SF3015TD — the enclosed five-axis cell", up=True),
    "sf-3d-head": PP("3d-5axis-laser", "i-001-000.png", "Five-axis head trimming a formed part"),
    "sf-3d-cut": PP("3d-5axis-laser", "i-003-001.png", "3D laser cutting a hot-stamped automotive part"),
    "sf-rc-1": R("2.webp", "Senfeng RC series robot fiber laser cutting cell — 6-axis robot with a 1.5 – 6 kW source"),
    "sf-rc-2": R("RC-Series.webp", "RC series robot laser cutting system"),
    "sf-coil-1": M("Coil-Laser-Cutting-Machine-SF1503CH", "i-001-000.png", "i-001-001.png", "Senfeng SF1503CH coil-fed fiber laser cutting line — decoiler, leveller and 5 × 10 ft laser, 3 – 6 kW"),
    "sf-coil-2": M("Coil-Laser-Cutting-Machine-SF2012CH", "i-001-000.png", "i-001-001.png", "Senfeng SF2012CH coil-fed laser line for 5/16″ – 9/16″ (8 – 14 mm) coil, 12 – 80 kW"),
    "sf-coil-3": M("Coil-Laser-Cutting-Machine-SF15015C", "i-001-000.png", "i-001-001.png", "Senfeng SF15015C open-type thin-sheet coil-fed laser — 0.031 – 0.047″ coil"),
    "sf-coil-top": M("Flexible-Metal-Processing-Line-TOP-Serie", "i-001-000.png", "i-001-001.png", "Senfeng TOP series automated line — coil, laser cutting, robot sorting, panel bending and welding"),
    "sf-coil-parts": W("samples-1400x584-1.webp", "Parts cut straight from coil"),
    "sf-coil-scene": M("Full-range-of-product-brochures", "i-015-159.png", "i-015-160.png", "Coil-fed laser line — decoiler, leveller, laser and sorting robot"),
    # ---------------------------------------------------------------- tube lasers
    "sf-t-1": M("Tube-Laser-Cutter-T-Series", "i-001-000.png", "i-001-001.png", "Senfeng SF6024T two-chuck tube fiber laser — Ø0.7 – 9″ tube, 20 ft, 1.5 – 6 kW"),
    "sf-t-2": M("54-Tube-Laser-Cutter-T-Series", "i-002-025.png", "i-002-026.png", "Senfeng SF6024T two-chuck tube laser — side view along the 20 ft bed"),
    "sf-t-3": M(TUBE, "i-006-008.png", "i-006-009.png", "T series tube laser with the optional automatic bundle loader"),
    "sf-t-4": M(TUBE, "i-016-060.png", "i-016-061.png", "T series tube laser — loader and unloading conveyor"),
    "sf-t-head": PP(TUBE, "i-001-000.png", "Tube laser cutting head with the following support"),
    "sf-t-chuck": PP(TUBE, "i-004-002.png", "Pneumatic chuck and cutting head on a round tube"),
    "sf-t-cutting": PP(TUBE, "i-005-004.png", "Tube laser cutting a perforated square tube"),
    "sf-t-profiles": PP(TUBE, "i-005-006.png", "Round, square, rectangular, angle and channel profiles cut on the tube laser"),
    "sf-t-thickness": W("T-tube-cutting-thickness-scaled.jpg", "Tube wall thickness capacity by laser power — stainless, carbon steel, aluminum"),
    "sf-plus-1": M("High-speed-High-precision-Tube-Laser-Cut", "i-001-000.png", "i-001-001.png", "Senfeng SF6024PLUS high-speed tube laser — Ø0.7 – 9.4″, 20 ft, 3 – 6 kW"),
    "sf-gplus-1": M("Two-chuck-Bevel-Tube-Laser-Cutter-GPLUS-", "i-001-000.png", "i-001-001.png", "Senfeng SF6012GPLUS bevel tube laser — Ø0.6 – 4.7″ at 240 rpm"),
    "sf-gt-1": M("Beveling-Tube-Laser-Cutter-GT-Series", "i-001-000.png", "i-001-001.png", "Senfeng SF6024GT bevel tube laser with loader — Ø2.3 – 9″, 45° bevels"),
    "sf-gt-2": R("6035GT-01.webp", "Senfeng SF6035GT bevel tube laser — Ø3.1 – 14.1″", up=True),
    "sf-plus-parts-1": W("9-640-640-2.jpg", "Bevel-cut square tubes joined without a gap", up=True),
    "sf-plus-parts-2": W("7-640-640.jpg", "Rectangular tube with laser-cut holes and bevelled ends", up=True),
    "sf-plus-parts-3": W("6-640-640-1.jpg", "Round tube with a 45° bevel cut", up=True),
    "sf-nt-1": M("Three-Chucks-0-Tailing-Tube-Laser-Cutter", "i-001-000.png", "i-001-001.png", "Senfeng SF6035NT three-chuck zero-tailing tube laser — Ø0.7 – 14″, 20 ft, 3 – 12 kW"),
    "sf-st-1": M("Three-Chucks-Heavy-duty-Tube-Laser-Cutte", "i-001-000.png", "i-001-001.png", "Senfeng ST series three-chuck heavy-duty tube laser — Ø1.9 – 25″, 29 – 39 ft, 6 – 20 kW"),
    "sf-ht-1": M("Four-chuck-Ultra-Heavy-Tube-Laser-Cutter", "i-001-000.png", "i-001-001.png", "Senfeng HT series four-chuck tube laser — Ø1.9 – 25″, 39 – 49 ft tubes to 6,600 lb"),
    "sf-ch-1": M("Large-H-shaped-Steel-Laser-Cutter-SF1500", "i-001-000.png", "i-001-001.png", "Senfeng SF1500CH profile laser line for H-beams, channels and angles — 12 – 30 kW"),
    "sf-nt-chucks": PP(TUBE, "i-004-003.png", "Cutting a square tube in the chuck — sparks at the cut"),
    "sf-ht-tube": PP(TUBE, "i-005-005.png", "Heavy-wall tube held in the chuck under the cutting head"),
    "sf-ch-scan": W("CH-05.webp", "Optional visual scanning of the H-beam before cutting", up=True),
    "sf-ch-render": W("features4.jpg", "H-beam laser line — the gantry cutting a beam", up=True),
    # ---------------------------------------------------------------- welding & cladding
    "sf-hwm-1": M(HWM, "i-007-046.png", "i-007-047.png", "Senfeng HWM series handheld fiber laser welder — 1.5, 2 or 3 kW, welds to 9/32″"),
    "sf-hwm-gun": M(HWM, "i-005-029.png", "i-005-030.png", "Handheld laser welding gun — under 1.5 lb, wire feeder and air-cooled head"),
    "sf-hwm-2": M(LW, "i-016-041.png", "i-016-042.png", "HWM series laser welder with the wire feeder", up=True),
    "sf-hw-1": M(HW, "i-005-037.png", "i-005-038.png", "Senfeng S series portable air-cooled laser welder with wire feeder — 0.8 – 1.5 kW"),
    "sf-hw-gun": M(HW, "i-005-039.png", "i-005-040.png", "S series air-cooled welding gun"),
    "sf-hw-weld": PP(HW, "i-004-027.png", "Handheld laser welding a stainless corner — no filler, no grinding"),
    "sf-hwm-weld": PP(HWM, "i-004-025.png", "Handheld laser welding with filler wire"),
    "sf-hwm-weld-2": PP(HWM, "i-005-028.png", "Handheld laser welding a stainless sheet"),
    "sf-hw-safety": PP(HWM, "i-005-027.png", "Operator in laser-resistant clothing, gloves and face shield welding with the handheld gun", rotate=90),
    "sf-hw-booth": PP(HWM, "i-003-015.png", "Senfeng's laser welding centre — handheld and robotic welding stations"),
    "sf-rw-1": M(LW, "i-011-017.png", "i-011-018.png", "Senfeng RW series robotic fiber laser welding cell — 6-axis robot with a 1.5 – 20 kW source"),
    "sf-rw-2": R("RW-01.webp", "RW series robot laser welder with positioner", up=True),
    "sf-rw-positioner": M(LW, "i-006-005.png", "i-006-006.png", "Robotic laser welding cell with the horizontal positioner for tanks and tubes"),
    "sf-rw-cell": M(LW, "i-008-011.png", "i-008-012.png", "Fully enclosed robotic laser welding workstation"),
    "sf-rmw-1": R("RMW-01.webp", "Senfeng RMW series teaching-free robotic arc welding machine — 500 A MIG/MAG", up=True),
    "sf-cmw-1": R("CMW-01.webp", "Senfeng CMW series collaborative robotic arc welder on a mobile cart — 350 / 500 A", up=True),
    "sf-cmw-2": R("CMW-02.webp", "CMW collaborative welder — the cobot arm and torch", up=True),
    "sf-weld-samples": W("robot-welding.jpg", "Laser-welded seams on stainless, aluminum and carbon steel"),
    "sf-clad-1": R("SFR6063-02.webp", "Senfeng SFR6063 robot laser cladding machine — 6 / 12 kW, workpieces to 20 ft and 15 t", delabel=True, up=True),
    "sf-clad-2": R("SFHS3050-2.webp", "Senfeng SFHS3050 laser cladding machine for shafts to 10 ft", up=True),
    "sf-clad-3": R("SFMR02-2.webp", "Senfeng SFMR02 portable laser cladding system for on-site repair", up=True),
    "sf-clad-robot": R("Laser-Cladding-Robot.webp", "KUKA / FANUC robot of the cladding cell", delabel=True, up=True),
    "sf-clad-positioner": R("Laser-Cladding-Dual-axis-Positioner.webp", "Dual-axis positioner for cladding", delabel=True, up=True),
    "sf-clad-head": W("High-speed-Laser-Cladding-Head.webp", "High-speed laser cladding head with powder feed", delabel=True, up=True, cutout=True),
    "sf-clad-bore": W("Laser-Inner-bore-Head.webp", "Inner-bore cladding head", delabel=True, up=True, cutout=True),
    # ---------------------------------------------------------------- panel benders
    "sf-bdc-1": M(PB, "i-007-026.png", "i-007-027.png", "Senfeng BDC2000 push-down automatic panel bender — 79″ bend width, 13 servo axes"),
    "sf-bdc-2": M(PB, "i-011-055.png", "i-011-056.png", "Senfeng BDC2000 panel bender — three-quarter view with the control cabinet"),
    "sf-bdc-3": PP("BDC-Series", "i-001-000.png", "Senfeng BDC2500 push-down panel bender — 98″ bend width"),
    "sf-bdc-suction": R("Suction-cup-Automatic-Panel-Bender-01.webp", "Senfeng BDC1500 suction-cup panel bender — 59″ bend width, 10 axes", up=True),
    "sf-bdc-robot": R("Loading-and-Unloading-Panel-Bender-01.webp", "BDC panel bender with robot loading and unloading", up=True),
    "sf-bdc-robot-2": PP("BDC-Series", "i-002-019.png", "BDC2000 panel bender in production — the operator at the control"),
    "sf-bdc-tool": PP(PB, "i-003-001.png", "Bending blades and blank-holder of the BDC panel bender"),
    "sf-bdc-clamps": R("Push-down-BDC2500-05.webp", "Optional clamps of the BDC panel bender", delabel=True, up=True),
    "sf-bdc-bends": W("440x280-6.jpg", "Bend up, bend down, press the edge and bend arc", up=True),
    "sf-bdc-parts": W("yangpin.jpg", "Panels, boxes and hems bent on the BDC", up=True),
    "sf-bdc-parts-2": W("daoju.jpg", "Door panel bent on the suction-cup panel bender", up=True),
}


def export(keys=None):
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for k in keys or PHOTOS:
        p = PHOTOS[k]
        src = SRC + p["src"]
        is_png = "mask" in p or p["src"].lower().endswith(".png") and Image.open(src).mode == "RGBA"
        ext = ".png" if is_png else ".jpg"
        dst = os.path.join(OUT, k + ext)
        srcs = [src] + ([SRC + p["mask"]] if "mask" in p else [])
        if os.path.exists(dst) and os.path.getmtime(dst) >= max(os.path.getmtime(s) for s in srcs):
            continue
        im = Image.open(src)
        if "mask" in p:
            m = Image.open(SRC + p["mask"]).convert("L")
            if m.size != im.size:
                m = m.resize(im.size, Image.LANCZOS)
            a = np.asarray(m).astype(np.float32)
            a = np.clip((a - 110) * 4, 0, 255).astype(np.uint8)       # drop the soft floor shadow, keep the machine's edge
            m = Image.fromarray(a).filter(ImageFilter.GaussianBlur(0.6))
            im = im.convert("RGBA")
            im.putalpha(m)
            if im.width > 3000:
                im = im.resize((3000, round(im.height * 3000 / im.width)), Image.LANCZOS)
        elif ext == ".png":
            im = im.convert("RGBA")
        else:
            im = im.convert("RGB")
        if p.get("crop"):
            im = im.crop(p["crop"])
        if p.get("rotate"):
            im = im.rotate(p["rotate"], expand=True)
        if p.get("delabel"):
            print(f"   delabel {k}")
            im = delabel(im)
        if p.get("up"):
            print(f"   upscale {k} {im.size}")
            im = upscale2x(im)
        if ext == ".png":
            im.save(dst, optimize=True)
        else:
            im.save(dst, quality=92)
        n += 1
    print(f"senfeng photos: {n} exported, {len(PHOTOS)} total in {OUT}")


if __name__ == "__main__":
    export(sys.argv[1:] or None)
