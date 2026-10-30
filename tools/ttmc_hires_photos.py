#!/usr/bin/env python3
"""High-resolution supplier photos of the NovoTech value-line saws (the owner's WeTransfer "photo for band saw", Oct 28 2026,
kept in /home/claude/ttmc-new/band_saw_2026-10-28/).  They replace the catalogue crops of tools/ttmc_more_photos.py for the
cold saws and supply the vertical band saws (VS series) of tools/value_line_data.py.

Nameplates and the supplier's logo are removed with LaMa (tools/lama_inpaint.py); the white margin is trimmed; a photo
under 700 px is upscaled 2x with Real-ESRGAN (tools/esrgan.py).  Product photos are cut out later by tools/make_images.py
(BiRefNet) unless the source already carries its own alpha.

    python3 tools/ttmc_hires_photos.py [key …]
        tm-* keys  → tools/src-images/ttmc-more/<key>.jpg   (registered by tools/ttmc_more_pages.py)
        nt-* keys  → tools/src-images/value-line/<key>.png  (registered by tools/value_line_data.py)
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/ttmc-new/band_saw_2026-10-28/"
DST_TM = os.path.join(ROOT, "tools", "src-images", "ttmc-more")
DST_NT = os.path.join(ROOT, "tools", "src-images", "value-line")
SMALL = 700          # px, longest side of the machine: below it the photo is upscaled 2x

# key: dict(src, alt, boxes=[(x0, y0, x1, y1) in source pixels — nameplates / logo, filled by LaMa], detail=False)
# NB: the supplier named two files the wrong way round — "VS-500.jpg" carries the VS-400 nameplate and is the catalogue's VS-400
# photo (blue, with the lamp); "VS400.jpg" is the grey machine the catalogue shows as the VS-500.
PHOTOS = {
    # ---------------------------------------------------------------- cold saws (tools/ttmc_more_data.py, tt-cs / tt-pds400 / tt-tv / tt-qcs400)
    "tm-cs": dict(src="CS-315-350.jpg", alt="CS-315 cold saw on stand with two-speed motor and double vise"),
    "tm-cs-225": dict(src="CS-225.jpg", alt="CS-225 bench cold saw, 9″ blade, with double vise and length stop"),
    "tm-cs-250": dict(src="CS-250.jpg", alt="CS-250 / CS-275 cold saw on cabinet stand, 10 – 11″ blade"),
    "tm-pds400": dict(src="PDS400.jpg", alt="PDS-400 heavy-duty cold saw for 16″ blades on cabinet stand"),
    "tm-tv": dict(src="TV300 -350-400.jpg", alt="TV-300 / TV-350 / TV-400 abrasive cut-off saw on stand"),
    "tm-qcs400a": dict(src="QCS400A.png", alt="QCS-400A aluminum cut-off saw with pneumatic clamping and safety hood", boxes=[(606, 726, 707, 784)]),
    # ---------------------------------------------------------------- vertical band saws (tools/value_line_data.py, novotech-vs)
    "nt-vs300-1": dict(src="VS300.png", alt="NovoTech VS-300 vertical metal band saw with blade welder, 12″ throat"),
    "nt-vs400-1": dict(src="VS-500.jpg", alt="NovoTech VS-400 vertical metal band saw with work light and table gauge, 15-3/4″ throat",
                       boxes=[(1648, 364, 1897, 512), (1578, 664, 1972, 902)]),
    "nt-vs500-1": dict(src="VS400.jpg", alt="NovoTech VS-500 vertical metal band saw, 19-3/4″ throat", boxes=[(396, 187, 476, 244)]),
    # ---------------------------------------------------------------- CNC double column saw (the catalogue crop had white blotches — Oct 28 2026)
    "nt-a14-1": dict(src="BS-500G-500GT.jpg", alt="NovoTech BS-500G / BS-500GT CNC automatic band saw", boxes=[(664, 430, 733, 468)], up=True),
}

# ---------------------------------------------------------------- the owner's second and third sets (Oct 29 2026): slip rolls and ring / profile
# rollers (RAR "Slip roll and Round bending machine") and the belt grinders, disc sanders, chamfering machines and dust collectors (WeTransfer
# "pictures for belt grinder").  Only models already on the site; the manual slip rolls (W01, SJ) and the manual RBM10 stay out.
ROLLS = "/home/claude/ttmc-new/rolls_2026-10-29/"
GRIND = "/home/claude/ttmc-new/belt_grinder_2026-10-29/"
PHOTOS.update({
    # ---- ESR electric slip rolls (tt-esr)
    "tm-esr": dict(dir=ROLLS, src="ESR-1300x2.5.jpg", alt="ESR-1300×2.5 electric slip roll with wire grooves, cone rolling and foot pedal"),
    "tm-esr1300e": dict(dir=ROLLS, src="ESR-1300X4.5E.jpg", alt="ESR-1300×4.5E electric slip roll with digital rear-roll readout on the pedestal control"),
    "tm-esr1020": dict(dir=ROLLS, src="ESR-1300X1.5.jpg", alt="ESR-1300×1.5 electric slip roll, 16 ga × 51″, with foot pedal"),
    "tm-esr1300-15e": dict(dir=ROLLS, src="ESR-1300X1.5E.jpg", alt="ESR-1300×1.5E motorized slip roll, European design, with foot pedal"),
    "tm-esr1300-45": dict(dir=ROLLS, src="ESR-1300x4.5.jpg", alt="ESR-1300×4.5 electric slip roll, 3/16″ × 51″"),
    "tm-esr1550": dict(dir=ROLLS, src="ESR-1550x3.5.jpg", alt="ESR-1550×3.5 electric slip roll, 10 ga × 61″"),
    "tm-esr2550e": dict(dir=ROLLS, src="ESR-2550X2.5E  ESR-2550X3.5E.jpg", alt="ESR-2550×2.5E / ESR-2550×3.5E electric slip rolls, 100″ long, with the E-series control pedestal"),
    # ---- HER hydraulic slip rolls (tt-her)
    "tm-her": dict(dir=ROLLS, src="HER-1300X6.5.jpg", alt="HER-1300×6.5 hydraulic slip roll with digital rear-roll readout on the control pedestal"),
    "tm-her2070": dict(dir=ROLLS, src="HER-2070x6.5.png", alt="HER-2070×6.5 hydraulic slip roll, 1/4″ × 81″"),
    # ---- RBM / HRBM profile benders (tt-rbm)
    "tm-hrbm50": dict(dir=ROLLS, src="HRBM50HV.jpg", alt="HRBM50HV profile bender with hydraulic top roll and pedestal control"),
    "tm-rbm40": dict(dir=ROLLS, src="RBM-40HV.jpg", alt="RBM40HV profile bender, horizontal and vertical, with foot pedal"),
    "tm-hrbm65": dict(dir=ROLLS, src="HRBM65.JPG", alt="HRBM65 hydraulic profile bender with Ø2-1/2″ shafts and mobile control panel", boxes=[(302, 545, 362, 584)]),
    "tm-hrbm40": dict(dir=ROLLS, src="HRBM40HV.jpg", alt="HRBM40HV profile bender with hydraulic top roll and pressure gauge"),
    "tm-rbm50": dict(dir=ROLLS, src="RBM-50HV.jpg", alt="RBM50HV profile bender with Ø2″ shafts and foot pedal"),
    "tm-hrbm-work": dict(dir=ROLLS, src="HRBM.jpg", alt="Rolling a ring of round tube on the HRBM profile bender — the three rolls and the top-roll screw", detail=True),
    # ---- ERBM / RBM ring rollers (tt-rbm-small)
    "tm-rbm30hv": dict(dir=ROLLS, src="RBM30HV.jpg", alt="RBM30HV ring roller, horizontal and vertical, with pedestal control"),
    "tm-rbm20": dict(dir=ROLLS, src="RBM20.png", alt="RBM20 ring roller with LED top-roll readout and foot pedal"),
    "tm-erbm10": dict(dir=ROLLS, src="ERBM10HV.png", alt="ERBM10HV motorized ring roller, horizontal and vertical, with foot pedal"),
    "tm-rbm30": dict(dir=ROLLS, src="RBM30.jpg", alt="RBM30 motorized ring roller with foot pedal"),
    # ---- CRB-76 (tt-tr)
    "tm-crb76": dict(dir=ROLLS, src="CRB76.jpg", alt="CRB-76 decorative ring roller for tube and flat bar", boxes=[(530, 532, 632, 602)]),
    # ---- belt grinders
    "tm-s75": dict(dir=GRIND, src="S-75 S-150A.jpg", alt="S-75 / S-150A heavy-duty belt grinder on pedestal, 3″ and 6″ × 79″ belt"),
    "tm-s75l": dict(dir=GRIND, src="S-75L S-150L.png", alt="S-75L / S-150L light-type belt grinder on pedestal"),
    "tm-s75h": dict(dir=GRIND, src="S-75HA S-150HA.jpg", alt="S-75HA / S-150HA heavy-duty belt grinder with dust drawer in the base"),
    "tm-s75hb": dict(dir=GRIND, src="S-75HB S-150HB.png", alt="S-75HB / S-150HB heavy-duty belt grinder with the built-in dust collector"),
    "tm-s100": dict(dir=GRIND, src="S-100.png", alt="S-100 belt grinder with 4″ belt on pedestal"),
    "tm-s220": dict(dir=GRIND, src="S-220.jpg", alt="S-220 wide-belt radius grinder and surface sander with 8″ belt", up=True),
    "tm-s75f": dict(dir=GRIND, src="S-75F.png", alt="S-75F mobile floor belt grinder for weld seams"),
    "tm-s50": dict(dir=GRIND, src="S-50.png", alt="S-50 combination belt grinder and disc sander"),
    "tm-s50b": dict(dir=GRIND, src="S-50B.png", alt="S-50B compact 3″ belt grinder", up=True),
    "tm-s50v": dict(dir=GRIND, src="S-50V  S-75V.png", alt="S-50V / S-75V vertical column belt grinder"),
    "tm-sdd75": dict(dir=GRIND, src="SDD75.jpg", alt="SDD75 multi-purpose belt grinder — flat, contact wheel and tube notching on one arm"),
    "tm-bgm50": dict(dir=GRIND, src="BGM-50HV.png", alt="BGM-50HV 2″ belt grinder for knives and tools, horizontal and vertical"),
    "tm-bgm50b": dict(dir=GRIND, src="BGM-50.png", alt="BGM-50 variable-speed belt grinder with inverter"),
    "tm-sp6": dict(dir=GRIND, src="SP-6.png", alt="SP-6 belt grinder and 20″ disc sander combination with dust ports", boxes=[(812, 978, 972, 1065)]),
    "tm-sp2": dict(dir=GRIND, src="SP-2.jpg", alt="SP-2 variable-speed grinding and polishing machine with belt and disc"),
    "tm-sp3": dict(dir=GRIND, src="SP-3.png", alt="SP-3 belt grinder, grinding wheel and polishing wheel on one motor"),
    "tm-btm250": dict(dir=GRIND, src="BTM250.png", alt="BTM250 6″ belt and 10″ disc sander on cabinet stand"),
    "tm-bkm250": dict(dir=GRIND, src="BKM250.jpg", alt="BKM-250 belt sander and edge beveller"),
    "tm-ds20": dict(dir=GRIND, src="DS20.png", alt="DS-20 20″ disc sander for metal on pedestal"),
    "tm-ds20a": dict(dir=GRIND, src="DS-20A.png", alt="DS-20A 20″ disc sander — the table rides up and down the column"),
    "tm-ds20v": dict(dir=GRIND, src="DS-20V.png", alt="DS-20V variable-speed 20″ disc sander on cabinet base", boxes=[(570, 905, 705, 995)]),
    "tm-tsm300": dict(dir=GRIND, src="TSM300.png", alt="TSM300 12″ disc sander on cabinet stand"),
    "tm-ds12": dict(dir=GRIND, src="DS12A.jpg", alt="DS12A 12″ disc sander with two tables"),
    "tm-ds12b": dict(dir=GRIND, src="DS12B.jpg", alt="DS12B 12″ bench disc sander with tilting table"),
    "tm-bg": dict(dir=GRIND, src="BG-8.png", alt="BG-8 8″ bench grinder with eye shields", boxes=[(985, 780, 1275, 960)]),
    "tm-bg60": dict(dir=GRIND, src="BG-60.png", alt="BG-60 wire-wheel deburring and polishing machine", boxes=[(1095, 658, 1232, 818)]),
    "tm-bg60a": dict(dir=GRIND, src="BG-60A.png", alt="BG-60A 3 HP wire-wheel deburring machine"),
    "tm-cmd": dict(dir=GRIND, src="CMD80.jpg", alt="CMD-80 edge chamfering machine for 15 – 45° weld preps"),
    "tm-cmd4": dict(dir=GRIND, src="CMD-4.jpg", alt="CMD-4 bench chamfering machine"),
    "tm-dm5": dict(dir=GRIND, src="DM5.jpg", alt="DM5 compact chamfering unit, 3/16″ at 45°"),
    "tm-dm5a": dict(dir=GRIND, src="DM5A.jpg", alt="DM5A compact chamfering unit with the table set for 45°"),
    "tm-md380": dict(dir=GRIND, src="MD380A MD380B.png", alt="MD-380A / MD-380B end-surface grinding machine"),
    "tm-dc650": dict(dir=GRIND, src="DC650.png", alt="DC650 metal dust collector with three-stage filtration and dust drawer"),
    "tm-dvs14": dict(dir=GRIND, src="DVS14.png", alt="DVS14 metal dust collector with cyclone separation"),
    "tm-prs": dict(dir=GRIND, src="PRS-76C.jpg", alt="PRS-76C tube and profile end grinder with two-speed motor, forward and reverse"),
    "tm-prs76": dict(dir=GRIND, src="PRS-76.jpg", alt="PRS-76 tube end grinder with 4″ belt"),
    "tm-prs76a": dict(dir=GRIND, src="PRS-76A.jpg", alt="PRS-76A tube end grinder with the tube clamp swung out", up=True),
    "tm-prs150": dict(dir=GRIND, src="PRS-150.png", alt="PRS-150 tube end grinder with 6″ belt for tube up to 5-3/4″"),
    "tm-bfm2560": dict(dir=GRIND, src="BFM-2560.jpg", alt="BFM-2560 wide-belt finishing and deburring machine, 24″ working width"),
    "tm-wd1800": dict(dir=GRIND, src="WD-1800.png", alt="WD-1800 stainless-steel wet dust collector for metal grinding dust", boxes=[(557, 445, 656, 508)]),
})
# ---------------------------------------------------------------- the owner's fourth set (Oct 30 2026): drill presses and milling machines
# (WeTransfer "pictures for drilling and milling").  A photo replaces the catalogue crop where it is larger or cleaner (the crops of the
# T-32, T-25B and TX530A still carried catalogue text) and photos are added for models on the site that had none.  Not used: T-40.png,
# WTZ-16JF.jpg and TX-20.png (the same pictures as the crops on the site, at the same or a smaller size) and "T25BC.png" (byte for byte
# the same file as "T25 T26.png").  boxes: the TTMC logo, and other model names on the badges (S28M on the T-28, S35ME on the T-35, T32
# on the T-30, T5025-3A on the T5025-1A, TBH24 / SBH28 on the TB column drills) so no badge contradicts the caption.
DRILLMILL = "/home/claude/ttmc-new/drill_mill_2026-10-30/"
PHOTOS.update({
    # ---- T-25 – T-40 gear-head drill presses (tt-t25)
    "tm-t25": dict(dir=DRILLMILL, src="T25 T26.png", alt="T-25 / T-26 gear-head drill press, floor model, with spindle guard"),
    "tm-t25a": dict(dir=DRILLMILL, src="T25A.png", alt="T-25A gear-head drill press with the control box on the front"),
    "tm-t25b": dict(dir=DRILLMILL, src="T-25B T26B.png", alt="T-25B / T-26B bench gear-head drill press"),
    "tm-t25c": dict(dir=DRILLMILL, src="T-25C.jpg", alt="T-25C gear-head drill press with 24 V control and spindle guard switch"),
    "tm-t25ch": dict(dir=DRILLMILL, src="T25C-H.png", alt="T-25C-H gear-head drill press with digital depth readout and wire spindle guard",
                     boxes=[(594, 162, 695, 206)]),
    "tm-t28": dict(dir=DRILLMILL, src="T-28.jpg", alt="T-28 gear-head drill press with mechanical power feed", boxes=[(782, 222, 838, 252)]),
    "tm-t30": dict(dir=DRILLMILL, src="T-30.png", alt="T-30 gear-head drill press with round swivelling table", boxes=[(449, 172, 483, 202)]),
    "tm-t32": dict(dir=DRILLMILL, src="T32 T-35.jpg", alt="T-32 / T-35 gear-head drill press with power feed", boxes=[(464, 112, 528, 140)]),
    # ---- T5025 / T4025 (tt-t5025)
    "tm-t5025-1a": dict(dir=DRILLMILL, src="T5025-1A.jpg", alt="T5025-1A gear-head drill press with round table", boxes=[(790, 298, 836, 325)]),
    "tm-t5025-3a": dict(dir=DRILLMILL, src="T5025-3A.png", alt="T5025-3A gear-head drill press with ±50° tilting table"),
    "tm-t4025": dict(dir=DRILLMILL, src="T4025.png", alt="T4025 gear-head drill press with box column base"),
    # ---- T-50 / TX530 (tt-t50)
    "tm-t50": dict(dir=DRILLMILL, src="T-50.jpg", alt="T-50 heavy-duty gear-head drill press, 2″ in steel, 12 speeds and power feed"),
    "tm-t50e": dict(dir=DRILLMILL, src="T-50E.png", alt="T-50E heavy-duty drill press with 400 mm throat and swivelling table", boxes=[(641, 283, 720, 320)]),
    "tm-tx530": dict(dir=DRILLMILL, src="TX530A.png", alt="TX530A inverter-drive drill press with power feed, work light and coolant", boxes=[(275, 298, 297, 316)]),
    "tm-tx530m": dict(dir=DRILLMILL, src="TX530.jpg", alt="TX530 inverter-drive drill press with two-range gearbox and coolant"),
    # ---- TB column drills (tt-tb)
    "tm-tb": dict(dir=DRILLMILL, src="TB36.png", alt="TB36 belt-drive industrial column drill"),
    "tm-tbv": dict(dir=DRILLMILL, src="TB36V.png", alt="TB36V inverter-drive column drill with coolant"),
    "tm-tb24": dict(dir=DRILLMILL, src="TB24.png", alt="TB24 belt-drive column drill with work light", boxes=[(364, 185, 406, 203)]),
    "tm-tb28": dict(dir=DRILLMILL, src="TB28.png", alt="TB28 belt-drive column drill", boxes=[(356, 93, 399, 111)]),
    "tm-tb24v": dict(dir=DRILLMILL, src="TB24V.png", alt="TB24V inverter-drive column drill with digital speed display", boxes=[(572, 340, 684, 366)]),
    "tm-tb28v": dict(dir=DRILLMILL, src="TB28V.png", alt="TB28V inverter-drive column drill with coolant", boxes=[(382, 114, 428, 129)]),
    # ---- WTZ variable-speed drill presses (tt-wtz)
    "tm-wtz13j": dict(dir=DRILLMILL, src="WTZ-13J.png", alt="WTZ-13J variable-speed bench drill press, 1/2″"),
    "tm-wtz16j": dict(dir=DRILLMILL, src="WTZ-16J.png", alt="WTZ-16J variable-speed bench drill press with round table, 5/8″"),
    "tm-wtz16q": dict(dir=DRILLMILL, src="WTZ-16Q.png", alt="WTZ-16Q bench drill press with variable speed"),
    "tm-wtz16t": dict(dir=DRILLMILL, src="WTZ-16T.png", alt="WTZ-16T drilling and tapping press with automatic reverse"),
    # ---- turret mills (tt-mill-turret)
    "tm-x6332": dict(dir=DRILLMILL, src="X6332WA.png", alt="X6332WA vertical and horizontal turret milling machine"),
    "tm-x6325": dict(dir=DRILLMILL, src="X6325W.png", alt="X6325W turret milling machine with horizontal spindle"),
    "tm-x6336": dict(dir=DRILLMILL, src="X6336.png", alt="X6336 turret milling machine with horizontal spindle and power feed"),
    "tm-x6336wa": dict(dir=DRILLMILL, src="X6336WA.png", alt="X6336WA turret milling machine with horizontal ram, power feed and DRO"),
    # ---- universal mills (tt-mill-univ, tt-mill-heavy)
    "tm-xq6226": dict(dir=DRILLMILL, src="XQ6226A.png", alt="XQ6226A universal milling machine with swivel head"),
    "tm-xq6226b": dict(dir=DRILLMILL, src="XQ6226B.png", alt="XQ6226B universal milling machine with power feed"),
    "tm-xq6226w": dict(dir=DRILLMILL, src="XQ6226W.png", alt="XQ6226W universal milling machine"),
    "tm-lm1450": dict(dir=DRILLMILL, src="LM-1450A.jpg", alt="LM-1450A universal milling machine, ISO50, with DRO"),
    "tm-lm1450b": dict(dir=DRILLMILL, src="LM-1450B.jpg", alt="LM-1450B universal milling machine with servo feed"),
    "tm-lm1450c": dict(dir=DRILLMILL, src="LM-1450C.jpg", alt="LM-1450C universal milling machine with DRO"),
    "tm-lm1450d": dict(dir=DRILLMILL, src="LM-1450D.jpg", alt="LM-1450D universal milling machine for production work"),
    "tm-x5750": dict(dir=DRILLMILL, src="X5750 X5750A.jpg", alt="X5750 / X5750A universal milling machine with ball screws and three servo motors"),
    # ---- drill-mills (tt-zx, tt-mill-small)
    "tm-zx5325": dict(dir=DRILLMILL, src="ZX5325C.jpg", alt="ZX5325C gear-head drilling and milling machine with DRO"),
    "tm-zx7550": dict(dir=DRILLMILL, src="ZX7550CW.png", alt="ZX7550CW drilling and milling machine with vertical and horizontal spindles"),
    "tm-zx7550c": dict(dir=DRILLMILL, src="ZX7550C.png", alt="ZX7550C drilling and milling machine"),
    "tm-zx6350": dict(dir=DRILLMILL, src="ZX6350C.png", alt="ZX6350C drilling and milling machine with vertical and horizontal spindles"),
    "tm-dm20": dict(dir=DRILLMILL, src="DM-20.png", alt="DM-20 radial drill-mill with cross table and box table"),
    # ---- keyseater and slotter (tt-slot)
    "tm-b5013": dict(dir=DRILLMILL, src="B5013.png", alt="B5013 slotting machine with swivel head for keyways and splines", boxes=[(3425, 1612, 3825, 1797)]),
    "tm-b5012": dict(dir=DRILLMILL, src="B5012.tif", alt="B5012 keyseater for keyways in single and small-batch work"),
})
BIG = 1800           # px: a source bigger than this is scaled down before the cut-out


def trim(im, thr=240, pad=12):
    """crop the white (or transparent) margin, keeping a small pad"""
    if im.mode == "RGBA":
        bb = im.getchannel("A").getbbox()
    else:
        g = im.convert("L").point(lambda v: 255 if v < thr else 0)
        bb = g.getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def fill_boxes(im, boxes):
    from lama_inpaint import inpaint
    rgba = im.mode == "RGBA"
    rgb = np.asarray(im.convert("RGB")).copy()
    mask = np.zeros(rgb.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes:
        mask[y0:y1, x0:x1] = 255
    out = Image.fromarray(inpaint(rgb, mask))
    if rgba:
        out.putalpha(im.getchannel("A"))
    return out


def process(key):
    p = PHOTOS[key]
    im = Image.open(p.get("dir", SRC) + p["src"])
    if im.mode == "CMYK" and im.info.get("icc_profile"):     # print files (B5012.tif): through their own profile, not the naive formula
        import io
        from PIL import ImageCms
        src_prof = ImageCms.ImageCmsProfile(io.BytesIO(im.info["icc_profile"]))
        im = ImageCms.profileToProfile(im, src_prof, ImageCms.createProfile("sRGB"), outputMode="RGB")
    im = im.convert("RGBA") if im.mode == "RGBA" else im.convert("RGB")
    if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] == 255:
        im = im.convert("RGB")
    elif im.mode == "RGBA" and key.startswith("tm-"):
        # a supplier cut-out: the pixels under the transparent area are the old studio background (grey wall, floor
        # shadow), which a plain RGB conversion would bring back — composite on white so BiRefNet sees a clean photo
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im).convert("RGB")
    if p.get("boxes"):
        im = fill_boxes(im, p["boxes"])
    im = trim(im)
    if max(im.size) < SMALL or p.get("up"):
        from esrgan import upscale
        im = upscale(im.convert("RGB"))
    if max(im.size) > BIG:
        im = im.resize((round(im.width * BIG / max(im.size)), round(im.height * BIG / max(im.size))), Image.LANCZOS)
    if key.startswith("tm-"):
        os.makedirs(DST_TM, exist_ok=True)
        im.convert("RGB").save(os.path.join(DST_TM, key + ".jpg"), quality=92)
    else:
        os.makedirs(DST_NT, exist_ok=True)
        im.save(os.path.join(DST_NT, key + ".png"), optimize=True)
    return im.size


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for k in keys:
        print(f"{k:14s} {process(k)}")


if __name__ == "__main__":
    main()
