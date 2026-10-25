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
    return dict(src="img/" + name, alt=alt, cutout=False, trim=False, **kw)


def PP(dir_, img, alt, **kw):           # brochure photo without a mask
    return dict(src=f"{P}{dir_}/{img}", alt=alt, cutout=False, trim=False, **kw)


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
    "sf-h-tower": R("H4-Laser-Cutter-2-1.png", "H4 fiber laser with the optional loading / unloading tower and sheet storage"),
    "sf-h-loader": R("H4-Laser-Cutter-3-1.png", "H4 fiber laser with the optional loading and unloading arm"),
    "sf-h-line": R("HC-2.webp", "Space-saver H series lasers in a line with a shared storage tower"),
    "sf-h5": R("H5-01.png", "SF3015H5 heavy-load fiber laser for 40 – 80 kW sources"),
    "sf-h-container": W("3015HC-1.jpg", "The compact H series ships in one container without teardown"),
    "sf-h-head": W("advantage01-H5-rkl2sp0k2sgf63w15egdoyphpo2fqsexkjwzmwoqig.webp", "Cutting head with the 7.9″ (200 mm) Z-axis travel for thick plate"),
    "sf-h-bevel": W("advantage02-H5-rkl2z72dcjcth0g26pmhftn9mm0tzf83gqcw4t1ph4.webp", "Optional 45° bevel cutting head"),
    "sf-np-1": M(NP, "i-001-000.png", "i-001-001.png", "Senfeng SF3015NP open-type single-table fiber laser — 5 × 10 ft, 3 – 12 kW"),
    "sf-np-2": R("NP-2.webp", "NP series open-type laser — the table seen from the loading side"),
    "sf-np-3": R("NP-5.webp", "NP series laser with the optional servo swing-arm loading manipulator"),
    "sf-np-4": R("NP-6.webp", "NP series laser with the optional loading and unloading unit"),
    "sf-np-scene": W("advantage1.jpg", "NP series laser cutting a sheet"),
    "sf-np-container": W("advantage2.jpg", "Six 3015NP machines fit in one 40 ft container"),
    "sf-1313g": dict(src=f"{P}{G13}/i-002-008.png", alt="Senfeng SF1313G compact fiber laser — 4 × 4 ft table, 1.5 – 3 kW", cutout=True, trim=False),
    "sf-1530g": R("1530G-1-1.webp", "Senfeng SF1530G enclosed fiber laser — 5 × 10 ft, 1.5 – 4 kW"),
    "sf-1530n": R("1530N-1-1.webp", "Senfeng SF1530N enclosed fiber laser with pull-out single table — 5 × 10 ft, 1.5 – 12 kW"),
    "sf-1530n-table": R("1530N-4.webp", "SF1530N — the single table pulled out for loading"),
    "sf-1530np": R("1530NP-1.webp", "Senfeng SF1530NP fully enclosed compact fiber laser with electric lifting door — 5 × 10 ft, 1.5 – 6 kW"),
    "sf-1530np-2": R("1530NP-4.webp", "SF1530NP — pull-out platform with integrated leg supports"),
    "sf-1530np-head": W("1530NP-6.webp", "SF1530NP — autofocus cutting head over the slat table"),
    "sf-sfp": R("P600-1.png", "Senfeng SFP600 high-precision fiber laser for small parts — 24 × 24″ table"),
    "sf-hm-1": R("HM-01.webp", "Senfeng SF3015HM enclosed sheet and tube fiber laser — 5 × 10 ft table plus Ø8.6″ × 20 ft tube attachment"),
    "sf-hm-2": R("HM-02.webp", "SF3015HM — the tube attachment on the side of the enclosure"),
    "sf-hm-3": R("HM-03.webp", "SF3015HM — rear view with the tube support"),
    "sf-hm-4": R("HM-05.webp", "Sheet and tube laser — enclosure doors open"),
    "sf-r-1": R("R-1.webp", "Senfeng R series ultra-large plate laser — 10 ft wide table to 164 ft long, 6 – 60 kW"),
    "sf-r-2": R("R-2.webp", "R series plate laser — gantry over the long table"),
    "sf-tx-1": R("TX-1.webp", "Senfeng TX series plate laser with ±45° bevel head — 10 × 20 ft to 10 × 164 ft"),
    "sf-tx-2": R("TX-2.webp", "TX series bevel plate laser — three-quarter view"),
    "sf-txp": R("TXP-01.png", "Senfeng SF12030TXP laser and flame hybrid plate cutter — 20 kW laser plus oxy-fuel to 4″"),
    "sf-r-curtain": W("R-4.webp", "R series — protective curtain and the beam with its protective chamber"),
    "sf-r-bevel": W("R-5.webp", "Bevel cutting in one step — K, V, X and Y weld preparations"),
    "sf-r-dust": W("R-6.webp", "Blow-suction dust collection under the slat table"),
    "sf-r-cut": W("2026013016.webp", "R series laser cutting 4″ (100 mm) plate"),
    "sf-tx-flame": W("2026013058.webp", "TXP — laser and flame hybrid cutting of 4″ carbon steel plate with bevels"),
    "sf-3d-1": R("3015TD-1-1.webp", "Senfeng SF3015TD five-axis 3D fiber laser — 5 × 10 ft travel, 3 – 20 kW"),
    "sf-3d-2": R("3015TD-3.webp", "SF3015TD — the enclosed five-axis cell"),
    "sf-3d-head": PP("3d-5axis-laser", "i-001-000.png", "Five-axis head trimming a formed part"),
    "sf-3d-cut": PP("3d-5axis-laser", "i-003-001.png", "3D laser cutting a hot-stamped automotive part"),
    "sf-rc-1": R("2.webp", "Senfeng RC series robot fiber laser cutting cell — 6-axis robot with a 1.5 – 6 kW source"),
    "sf-rc-2": R("RC-Series.webp", "RC series robot laser cutting system"),
    "sf-coil-1": M("Coil-Laser-Cutting-Machine-SF1503CH", "i-001-000.png", "i-001-001.png", "Senfeng SF1503CH coil-fed fiber laser cutting line — decoiler, leveller and 5 × 10 ft laser, 3 – 6 kW"),
    "sf-coil-2": M("Coil-Laser-Cutting-Machine-SF2012CH", "i-001-000.png", "i-001-001.png", "Senfeng SF2012CH coil-fed laser line for 5/16″ – 9/16″ (8 – 14 mm) coil, 12 – 80 kW"),
    "sf-coil-3": M("Coil-Laser-Cutting-Machine-SF15015C", "i-001-000.png", "i-001-001.png", "Senfeng SF15015C open-type thin-sheet coil-fed laser — 0.031 – 0.047″ coil"),
    "sf-coil-top": M("Flexible-Metal-Processing-Line-TOP-Serie", "i-001-000.png", "i-001-001.png", "Senfeng TOP series automated line — coil, laser cutting, robot sorting, panel bending and welding"),
    "sf-coil-parts": W("samples-1400x584-1.webp", "Parts cut straight from coil"),
    "sf-coil-scene": W("1503CH-05.webp", "Coil-fed laser line — the leveller feeding the cutting table"),
    # ---------------------------------------------------------------- tube lasers
    "sf-t-1": M("Tube-Laser-Cutter-T-Series", "i-001-000.png", "i-001-001.png", "Senfeng SF6024T two-chuck tube fiber laser — Ø0.7 – 9″ tube, 20 ft, 1.5 – 6 kW"),
    "sf-t-2": R("7524T-1.webp", "Senfeng SF7524T two-chuck tube laser for 24.6 ft tubes with the safety fence"),
    "sf-t-3": R("6024T-02.webp", "T series tube laser with the optional automatic bundle loader"),
    "sf-t-4": R("6024T-03.webp", "T series tube laser — loader and unloading conveyor"),
    "sf-t-head": PP(TUBE, "i-001-000.png", "Tube laser cutting head with the following support"),
    "sf-t-chuck": PP(TUBE, "i-004-002.png", "Pneumatic chuck and cutting head on a round tube"),
    "sf-t-cutting": PP(TUBE, "i-005-004.png", "Tube laser cutting a perforated square tube"),
    "sf-t-profiles": PP(TUBE, "i-005-006.png", "Round, square, rectangular, angle and channel profiles cut on the tube laser"),
    "sf-t-thickness": W("T-tube-cutting-thickness-scaled.jpg", "Tube wall thickness capacity by laser power — stainless, carbon steel, aluminum"),
    "sf-plus-1": M("High-speed-High-precision-Tube-Laser-Cut", "i-001-000.png", "i-001-001.png", "Senfeng SF6024PLUS high-speed tube laser — Ø0.7 – 9.4″, 20 ft, 3 – 6 kW"),
    "sf-gplus-1": M("Two-chuck-Bevel-Tube-Laser-Cutter-GPLUS-", "i-001-000.png", "i-001-001.png", "Senfeng SF6012GPLUS bevel tube laser — Ø0.6 – 4.7″ at 240 rpm"),
    "sf-gt-1": M("Beveling-Tube-Laser-Cutter-GT-Series", "i-001-000.png", "i-001-001.png", "Senfeng SF6024GT bevel tube laser with loader — Ø2.3 – 9″, 45° bevels"),
    "sf-gt-2": R("6035GT-01.webp", "Senfeng SF6035GT bevel tube laser — Ø3.1 – 14.1″"),
    "sf-plus-bevel": W("advantege-2-rg4w62iba61gpcu85krchb4juxqr3ksei55kgbc2ew.jpg", "45° bevel cutting head on the GPLUS"),
    "sf-plus-small": W("advantege-1-rg4w62iba61gpcu85krchb4juxqr3ksei55kgbc2ew.jpg", "Cutting small tubes at high speed — minimum Ø0.6″"),
    "sf-plus-chuck": W("advantage03-PLUS-rkl176a3urpqp5fw11d9lz911tktpl29buqbebz1a0.webp", "Self-centering pneumatic chuck of the PLUS series"),
    "sf-plus-parts-1": W("9-640-640-2.jpg", "Bevel-cut square tubes joined without a gap"),
    "sf-plus-parts-2": W("7-640-640.jpg", "Rectangular tube with laser-cut holes and bevelled ends"),
    "sf-plus-parts-3": W("6-640-640-1.jpg", "Round tube with a 45° bevel cut"),
    "sf-nt-1": M("Three-Chucks-0-Tailing-Tube-Laser-Cutter", "i-001-000.png", "i-001-001.png", "Senfeng SF6035NT three-chuck zero-tailing tube laser — Ø0.7 – 14″, 20 ft, 3 – 12 kW"),
    "sf-st-1": M("Three-Chucks-Heavy-duty-Tube-Laser-Cutte", "i-001-000.png", "i-001-001.png", "Senfeng ST series three-chuck heavy-duty tube laser — Ø1.9 – 25″, 29 – 39 ft, 6 – 20 kW"),
    "sf-ht-1": M("Four-chuck-Ultra-Heavy-Tube-Laser-Cutter", "i-001-000.png", "i-001-001.png", "Senfeng HT series four-chuck tube laser — Ø1.9 – 25″, 39 – 49 ft tubes to 6,600 lb"),
    "sf-ch-1": M("Large-H-shaped-Steel-Laser-Cutter-SF1500", "i-001-000.png", "i-001-001.png", "Senfeng SF1500CH profile laser line for H-beams, channels and angles — 12 – 30 kW"),
    "sf-nt-chucks": W("NT-adv-1.png", "The three chucks of the NT series — the middle chuck feeds the last piece so there is no tailing"),
    "sf-ht-tube": W("advantage01-HT-rkmdmmbe78cz3izmj5guwiyqnecvqzf4p3v5bky69k.webp", "Four-chuck tube laser carrying a heavy large-diameter tube"),
    "sf-ht-bevel": W("advantage02-HT-rkmdn0ez1qw9xof58tk9fxenk6fdyfz3r1nfiqd9o8.webp", "45° bevel cutting on heavy tube"),
    "sf-ch-scan": W("CH-05.webp", "Optional visual scanning of the H-beam before cutting"),
    "sf-ch-render": W("features4.jpg", "H-beam laser line — the gantry cutting a beam"),
    # ---------------------------------------------------------------- welding & cladding
    "sf-hwm-1": M(HWM, "i-007-046.png", "i-007-047.png", "Senfeng HWM series handheld fiber laser welder — 1.5, 2 or 3 kW, welds to 9/32″"),
    "sf-hwm-gun": M(HWM, "i-005-029.png", "i-005-030.png", "Handheld laser welding gun — under 1.5 lb, wire feeder and air-cooled head"),
    "sf-hwm-2": R("HWM-02.webp", "HWM series laser welder with the wire feeder on top"),
    "sf-hw-1": M(HW, "i-005-037.png", "i-005-038.png", "Senfeng S series portable air-cooled laser welder with wire feeder — 0.8 – 1.5 kW"),
    "sf-hw-gun": M(HW, "i-005-039.png", "i-005-040.png", "S series air-cooled welding gun"),
    "sf-hw-weld": PP(HW, "i-004-027.png", "Handheld laser welding a stainless corner — no filler, no grinding"),
    "sf-hwm-weld": PP(HWM, "i-004-025.png", "Handheld laser welding with filler wire"),
    "sf-hwm-weld-2": PP(HWM, "i-005-028.png", "Handheld laser welding a stainless sheet"),
    "sf-hw-safety": W("laser-welder-S-Series-04.webp", "Operator protection for laser welding — CE face shield, laser-resistant clothing and gloves"),
    "sf-hw-booth": R("laser-welder-S-Series-05.webp", "Optional laser welding booth with protective glass"),
    "sf-rw-1": M(LW, "i-011-017.png", "i-011-018.png", "Senfeng RW series robotic fiber laser welding cell — 6-axis robot with a 1.5 – 20 kW source"),
    "sf-rw-2": R("RW-01.webp", "RW series robot laser welder with positioner"),
    "sf-rw-positioner": R("RW-03.webp", "Horizontal positioner for welding tanks and tubes"),
    "sf-rw-cell": R("RMW-02.webp", "Robotic welding cell with safety fencing — 7-axis configuration"),
    "sf-rmw-1": R("RMW-01.webp", "Senfeng RMW series teaching-free robotic arc welding machine — 500 A MIG/MAG"),
    "sf-rmw-weld": W("RMW-adv3-rg4w61kh3c06dqvlb2cpwtd39jvdvvoo60i2z1dgl4.png", "Robotic arc welding on a 3D fixture table"),
    "sf-cmw-1": R("CMW-01.webp", "Senfeng CMW series collaborative robotic arc welder on a mobile cart — 350 / 500 A"),
    "sf-cmw-2": R("CMW-02.webp", "CMW collaborative welder — the cobot arm and torch"),
    "sf-cmw-weld": W("CMW-adv2-rg4w61kh3c06dqvlb2cpwtd39jvdvvoo60i2z1dgl4.png", "Collaborative arc welding on the 3D flexible table"),
    "sf-weld-samples": W("robot-welding.jpg", "Laser-welded seams on stainless, aluminum and carbon steel"),
    "sf-clad-1": R("SFR6063-02.webp", "Senfeng SFR6063 robot laser cladding machine — 6 / 12 kW, workpieces to 20 ft and 15 t"),
    "sf-clad-2": R("SFHS3050-2.webp", "Senfeng SFHS3050 laser cladding machine for shafts to 10 ft"),
    "sf-clad-3": R("SFMR02-2.webp", "Senfeng SFMR02 portable laser cladding system for on-site repair"),
    "sf-clad-robot": R("Laser-Cladding-Robot.webp", "KUKA / FANUC robot of the cladding cell"),
    "sf-clad-positioner": R("Laser-Cladding-Dual-axis-Positioner.webp", "Dual-axis positioner for cladding"),
    "sf-clad-head": W("High-speed-Laser-Cladding-Head.webp", "High-speed laser cladding head with powder feed"),
    "sf-clad-bore": W("Laser-Inner-bore-Head.webp", "Inner-bore cladding head"),
    # ---------------------------------------------------------------- panel benders
    "sf-bdc-1": M(PB, "i-007-026.png", "i-007-027.png", "Senfeng BDC2000 push-down automatic panel bender — 79″ bend width, 13 servo axes"),
    "sf-bdc-2": R("Push-down-BDC2500-02.webp", "BDC series panel bender — three-quarter view from the manipulator side"),
    "sf-bdc-3": R("Push-down-BDC2500-01.webp", "Senfeng BDC2500 push-down panel bender — 98″ bend width"),
    "sf-bdc-suction": R("Suction-cup-Automatic-Panel-Bender-01.webp", "Senfeng BDC1500 suction-cup panel bender — 59″ bend width, 10 axes"),
    "sf-bdc-robot": R("Loading-and-Unloading-Panel-Bender-01.webp", "BDC panel bender with robot loading and unloading"),
    "sf-bdc-robot-2": R("Loading-and-Unloading-Panel-Bender-02.webp", "Robot loading cell of the BDC panel bender — rear view"),
    "sf-bdc-tool": R("Push-down-BDC2500-04.webp", "Optional auxiliary bending tool of the BDC"),
    "sf-bdc-clamps": R("Push-down-BDC2500-05.webp", "Optional clamps of the BDC panel bender"),
    "sf-bdc-blades": W("440x280-1.jpg", "Bending blades and blank-holder of the panel bender"),
    "sf-bdc-bends": W("440x280-6.jpg", "Bend up, bend down, press the edge and bend arc"),
    "sf-bdc-parts": W("yangpin.jpg", "Panels, boxes and hems bent on the BDC"),
    "sf-bdc-parts-2": W("daoju.jpg", "Door panel bent on the suction-cup panel bender"),
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
            im.save(dst, optimize=True)
        elif ext == ".png":
            im.convert("RGBA").save(dst, optimize=True)
        else:
            im.convert("RGB").save(dst, quality=92)
        n += 1
    print(f"senfeng photos: {n} exported, {len(PHOTOS)} total in {OUT}")


if __name__ == "__main__":
    export(sys.argv[1:] or None)
