#!/usr/bin/env python3
"""High-resolution supplier photos of the NovoTech value-line saws (the owner's WeTransfer "photo for band saw", Oct 28 2026,
kept in /home/claude/ttmc-new/band_saw_2026-10-28/).  They replace the catalogue crops of tools/ttmc_more_photos.py for the
cold saws and supply the vertical band saws (VS series) of tools/value_line_data.py.

Nameplates and the supplier's logo are removed with LaMa (tools/lama_inpaint.py); the white margin is trimmed; a photo
under 700 px is upscaled 2x with Real-ESRGAN (tools/esrgan.py).  Product photos are cut out later by tools/make_images.py
(BiRefNet) unless the source already carries its own alpha.

    python3 tools/ttmc_hires_photos.py [key …]
        tm-* keys  → tools/src-images/ttmc-more/<key>.jpg   (registered by tools/ttmc_more_pages.py)
        tt-* keys  → tools/src-images/ttmc-hires/<key>.jpg  (registered by tools/ttmc_pages.py; they replace the catalogue crops
                     of tools/ttmc_photos.py, which stay in tools/src-images/ttmc)
        nt-* keys  → tools/src-images/value-line/<key>.png  (registered by tools/value_line_data.py)
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/ttmc-new/band_saw_2026-10-28/"
DST_TM = os.path.join(ROOT, "tools", "src-images", "ttmc-more")
DST_TT = os.path.join(ROOT, "tools", "src-images", "ttmc-hires")
DST_NT = os.path.join(ROOT, "tools", "src-images", "value-line")
SMALL = 700          # px, longest side of the machine: below it the photo is upscaled 2x

# key: dict(src, alt, boxes=[(x0, y0, x1, y1) in source pixels — nameplates / logo, filled by LaMa], white=[… painted white], detail=False)
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

# the owner's WeTransfer "pictures for shearing machine" (Oct 31 2026): only the photos sharper than the site's catalogue crops,
# and photos of models that had none; the red TTMC logo on the Q11-3x1250A top guard and the HNM-6 nameplate are filled by LaMa
SHEAR = "/home/claude/ttmc-new/shear_2026-10-31/"
PHOTOS.update({
    # ---- bench machines (tt-3in1, tt-ebq01 …) — tools/ttmc_more_data*.py
    "tm-3in1-1016": dict(dir=SHEAR, src="3 IN1 1016 1067 1320.jpg", alt="3-IN-1/1016, 1067 and 1320 shear, brake and roll machine with segmented fingers and two crank handles"),
    "tm-3in1-610": dict(dir=SHEAR, src="3-IN-1 610 760.png", alt="3-IN-1/610 and 760 shear, brake and roll machine on cast side frames", up=True),
    "tm-3in1-305": dict(dir=SHEAR, src="3-IN-1 200 305.jpg", alt="3-IN-1/200 and 305 bench shear, brake and slip roll with crank handle"),
    "tm-ebq01": dict(dir=SHEAR, src="EBQ01-1.25X650 EBQ01-1.0X1050.png", alt="EBQ01 motorized bench shear with rear safety cage and foot switch"),
    "tm-mcs1250e": dict(dir=SHEAR, src="MCS-1250E.jpg", alt="MCS-1250E motorized circle shear with pneumatic blank clamping, pedestal control and foot pedal"),
    "tm-ecs": dict(dir=SHEAR, src="ECS10-10.jpg", alt="ECS10/10 two-speed electric circle shear and flanging machine on stand, with pedestal control and foot pedal", up=True),
    "tm-hnm6": dict(dir=SHEAR, src="HNM-6.jpg", alt="HNM-6 hydraulic 90° corner notcher with emergency-stop pedestal and foot pedal", boxes=[(756, 766, 817, 828)]),
    "tm-hnm6a": dict(dir=SHEAR, src="HNM-6A.png", alt="HNM-6A hydraulic adjustable-angle notcher, 30 – 135°, with control pedestal and foot pedal"),
    "tm-pnm": dict(dir=SHEAR, src="PNM-130 PNM-150.png", alt="PNM-130 / PNM-150 pneumatic 90° corner notcher on stand with foot pedal"),
    # ---- shears (tt-q11, tt-q11nc, tt-hq01, tt-hq11) — tools/ttmc_data.py; the PS pneumatic shear is not sold (Nov 7 2026)
    "tt-q11a": dict(dir=SHEAR, src="Q11-3x1250A.png", alt="Q11-3x1250A electric shear, 49″ × 1/8″, with front support arms, side control box and the mobile foot pedal",
                    boxes=[(1727, 371, 2130, 533)]),
    "tt-q11nc-4x1300": dict(dir=SHEAR, src="386103 Q11-4X1300NC.png", alt="Q11-4x1300NC electric shear with PLC control and motorised back gauge, 51″ × 5/32″", up=True),
    "tt-hq01-2500": dict(dir=SHEAR, src="HQ01-1.6X2500B.jpg", alt="HQ01-1.6x2500B light hydraulic shear, 98″ × 16 ga, with front sheet supports and side guards"),
    "tt-hq11-1300": dict(dir=SHEAR, src="HQ11-1300X6.5.jpg", alt="HQ11-6.5x1300 hydraulic shear, 51″ × 1/4″, with hold-downs, beam-mounted controls and the foot pedal"),
})

# the owner's WeTransfer "tube bender" (Nov 2 2026): only models already on the site, where the photo is larger or cleaner than the
# catalogue crop (the HTB-1000 and ETR-50 crops were print scans, the ETR-50 with a callout line across the pedal), and the TB-3A, on the
# site with no photo.  Not used: YP-9, YP-38, MY22, W-1/2, SBG30, SBG-40, UB-70/100, UB-100A, PBS-3, PR-3, TR-40/50/60, HB-8, HB-10,
# HB-12/16 and the plain TB-3 (not on the site).  boxes: the KAKA importer logo on the HTB-2000 control box; the JTB-40 panel's maker
# code "JGWG-40BZ" and its "Metalcraft Pipe Bender" line, so no name contradicts the caption.
TUBE = "/home/claude/ttmc-new/tube_bender_2026-11-02/"
PHOTOS.update({
    # ---- JTB hydraulic PLC tube benders (tt-jtb)
    "tm-jtb40": dict(dir=TUBE, src="JTB-40.jpg", alt="JTB-40 hydraulic tube bender with foot pedal", boxes=[(825, 525, 875, 541), (799, 631, 888, 644)]),
    "tm-jtb50": dict(dir=TUBE, src="JTB-50.jpg", alt="JTB-50 hydraulic PLC tube bender"),
    "tm-jtb80": dict(dir=TUBE, src="JTB-80.jpg", alt="JTB-80 hydraulic PLC tube bender for 3-1/8″ tube"),
    # ---- TB-3 / HTB-1000 pipe benders (tt-tb3)
    "tm-htb1000": dict(dir=TUBE, src="HTB1000.jpg", alt="HTB-1000 electric-hydraulic pipe bender on caster stand"),
    "tm-tb3a": dict(dir=TUBE, src="TB-3A.png", alt="TB-3A pipe bender with 10-ton hydraulic jack on a floor pedestal"),
    "tm-tb3b": dict(dir=TUBE, src="TB-3B.png", alt="TB-3B air-hydraulic pipe bender on caster stand with the foot-operated air pump"),
    "tm-tb3c": dict(dir=TUBE, src="TB-3C.png", alt="TB-3C electric-hydraulic pipe bender on caster stand with power pack and foot switch"),
    # ---- HTB-2000 exhaust bender (tt-exhaust), EHB-10 (tt-hb-pipe), ETR-50 (tt-tr)
    "tm-htb2000": dict(dir=TUBE, src="HTB-2000.jpg", alt="HTB-2000 hydraulic exhaust tube bender with tooling package", boxes=[(113, 522, 148, 551)]),
    "tm-ehb10": dict(dir=TUBE, src="EHB-10.png", alt="EHB-10 electric-hydraulic pipe bender"),
    "tm-etr50": dict(dir=TUBE, src="ETR-50.png", alt="ETR-50 electric tube roller with foot pedal"),
})

# the owner's RAR "Bending brakes" (Nov 2 2026): brakes, folders, lock formers, beading machines, roller stands.  As for the tube benders:
# a photo replaces the catalogue crop where it is larger or cleaner (the BP-1648H and BSM3150 crops had cut-out holes in the white blades),
# and models on the site with no photo get theirs.  Kept on the site (its photo is as large or larger, or the new one is not a product
# shot): ALB, EFMS, HW1830, MFS, TFS, TSB2060, TSBS, W1.2×1500, W2.5×2540A, W2.0×2040, W2.5×1220, PBB2020 (an outdoor photo on a pallet),
# WF and W1.2×1010 (TTMC advertising frames), ZWJ (text printed over the photo).  Not on the site, left out: RS018, CB24, CHB-24, RM-A,
# RM-B, RM08, RM18, RM24HM, RM24M, TB12.  boxes: the TTMC logo on the M55, the HW2040E apron plate and touch-screen start page and the
# WU2.0×2500 beam; the KAKA importer plate on the EB2500.  The BSM2540 photo is the supplier's BSM2540A — the same machine, grey.
BRAKE = "/home/claude/ttmc-new/brakes_2026-11-02/"
PHOTOS.update({
    # ---- replacements (tools/ttmc_more_data.py, ttmc_more_data2.py)
    "tm-pf16g": dict(dir=BRAKE, src="373903 PF16G.png", alt="PF16G lock former for Pittsburgh locks, double seams, drive cleats and Z shapes"),
    "tm-lq15": dict(dir=BRAKE, src="373930 LQ-15.png", alt="LQ15 power slitting and bending machine for duct"),
    "tm-stand-rv": dict(dir=BRAKE, src="378201 RV1100.JPG", alt="RV1100 V-roller stand"),
    "tm-bp1648h": dict(dir=BRAKE, src="BP-1648H.png", alt="BP-1648H pan and box brake on stand"),
    "tm-bp1650": dict(dir=BRAKE, src="BP-1650.jpg", alt="BP-1650 pan and box brake, 16 ga × 50″"),
    "tm-bsm1016": dict(dir=BRAKE, src="BSM1016.png", alt="BSM1016 folding brake with slitter on folding stand"),
    "tm-bsm2540": dict(dir=BRAKE, src="BSM2540A.png", alt="BSM2540 folding brake with slitter, 100″"),
    "tm-bsm3150": dict(dir=BRAKE, src="BSM3150X0.8.png", alt="BSM3150 shear and brake machine on its mobile stand"),
    "tm-eb1250": dict(dir=BRAKE, src="EB1000 RB1250.png", alt="EB1250 magnetic sheet metal brake, 4 ft × 16 ga, with foot switch"),
    "tm-eb2500": dict(dir=BRAKE, src="EB2000 EB2500 EB3200.jpg", alt="EB2500 magnetic sheet metal brake, 8 ft × 16 ga", boxes=[(837, 766, 878, 802)]),
    "tm-efm": dict(dir=BRAKE, src="EFM2020 EFM2520 EFM3020.jpg", alt="EFM 3020 electric folding machine, 10 ft"),
    "tm-etb12": dict(dir=BRAKE, src="ETB12.png", alt="ETB-12 motorized beading machine with foot pedal"),
    "tm-etb25": dict(dir=BRAKE, src="ETB25 ETB40.png", alt="ETB-25 beading machine, 12 ga, with brake motor and foot pedal"),
    "tm-hb2248": dict(dir=BRAKE, src="HB-2248.png", alt="HB-2248 all-steel hand brake on folding stand"),
    "tm-hb2250": dict(dir=BRAKE, src="HB-2250.png", alt="HB-2250 hand brake on stand, 50″"),
    "tm-hwe": dict(dir=BRAKE, src="HW2040X4.5E HW2540X4.5E HW3050X3.5E.jpg",
                   alt="HW2040×4.5E hydraulic folding machine with touch screen, servo back gauge and light curtains",
                   boxes=[(1172, 1306, 1248, 1339), (1985, 906, 2032, 919)]),
    "tm-hw2440": dict(dir=BRAKE, src="HW2440X3.5 HW3050X3.5.jpg", alt="HW2440×3.5 hydraulic folding machine"),
    "tm-m55": dict(dir=BRAKE, src="M55 M60.png", alt="M55 compact single-cylinder ironworker with punch, shear and notcher", boxes=[(569, 73, 699, 128)]),
    "tm-pbb1020": dict(dir=BRAKE, src="PBB1020 2.5 PBB1270 2 PBB15201.5.jpg", alt="PBB1020/2.5 folding machine with foot clamping"),
    "tm-pbb3sh": dict(dir=BRAKE, src="PBB1020 3SH PBB1270 3SH PBB2050 3SH.jpg", alt="PBB1020/3SH folding machine with quick-release clamp segments"),
    "tm-stand-rb365": dict(dir=BRAKE, src="RB365.JPG", alt="RB365 roller conveyor"),
    "tm-rm36": dict(dir=BRAKE, src="RM-24 RM-36 RM-42.jpg", alt="RM24 · RM36 · RM42 power-drive bead roller with variable-speed foot pedal"),
    "tm-rm18e": dict(dir=BRAKE, src="RM18E.jpg", alt="RM18E power beading machine for round duct"),
    "tm-rm42h": dict(dir=BRAKE, src="RM24H RM36H RM42H.JPG", alt="RM-24H · RM-36H · RM-42H high-throat variable-speed bead roller"),
    "tm-w1220": dict(dir=BRAKE, src="W1.2X1220.jpg", alt="W1.2×1220 bench hand brake"),
    "tm-w1500h": dict(dir=BRAKE, src="W1.2X1500H.png", alt="W1.2×1500H pan and box brake with 125 mm fingers"),
    "tm-pb1220z": dict(dir=BRAKE, src="W1.5X1220Z.psd", alt="W1.5×1220Z heavy-duty pan and box brake"),
    "tm-w2540h": dict(dir=BRAKE, src="W1.5X2540H.png", alt="W1.5×2540H heavy pan and box brake for pans to 5-1/8″ deep"),
    "tm-w1050": dict(dir=BRAKE, src="W1.5x1050.psd", alt="W1.5×1050 floor brake with sliding segments"),
    "tm-pb1220": dict(dir=BRAKE, src="W1.5x1220.png", alt="W1.5×1220 pan and box brake with removable fingers"),
    "tm-w1830p": dict(dir=BRAKE, src="W1830X1.5P.png", alt="W1830×1.5P pan and box brake, 72″ × 16 ga"),
    "tm-wb14": dict(dir=BRAKE, src="WB-14.png", alt="WB-14 bench hand brake"),
    "tm-wu": dict(dir=BRAKE, src="WU2.0X2500.psd", alt="WU2.0×2500 pan and box brake with two counterweights", boxes=[(1768, 553, 1968, 648)]),
    # ---- models on the site that had no photo
    "tm-eb625": dict(dir=BRAKE, src="EB625.jpg", alt="EB625 magnetic sheet metal brake on pedestal stand with foot switch"),
    "tm-hb1650": dict(dir=BRAKE, src="HB-1650.png", alt="HB-1650 hand brake on stand"),
    "tm-bsm1220": dict(dir=BRAKE, src="BSM1220.png", alt="BSM1220 folding brake with slitter on stand"),
    "tm-w305a": dict(dir=BRAKE, src="W1.0X305A,W1.0X610A W1.0X915A.png", alt="W1.0×305A / W1.0×610A / W1.0×915A bench pan and box brake"),
    "tm-w610": dict(dir=BRAKE, src="W1.0x610.png", alt="W1.0×610 bench hand brake, 24″"),
    "tm-w460": dict(dir=BRAKE, src="W1.2X460 W1.2X760.png", alt="W1.2×460 / W1.2×760 bench hand brake"),
    "tm-w610b": dict(dir=BRAKE, src="W1.2X610.png", alt="W1.2×610 bench brake with toggle clamps"),
    "tm-pbb1020a": dict(dir=BRAKE, src="1020 2A PBB1270 2A PBB1520 1.5A.jpg", alt="PBB1020/2A · PBB1270/2A · PBB1520/1.5A folding machine with foot clamping"),
    "tm-pbb1020-1a": dict(dir=BRAKE, src="PBB1020 1A  PBB1250 1A.jpg", alt="PBB1020/1A · PBB1250/1A folding machine on stand"),
    "tm-tsb2020": dict(dir=BRAKE, src="TSB2020 2.jpg", alt="TSB 2020/2 manual folding machine"),
    "tm-mf3020": dict(dir=BRAKE, src="MF3020.jpg", alt="MF 3020 folding machine, 10 ft"),
    "tm-brake36": dict(dir=BRAKE, src="36  40 48 72 inch.jpg", alt="36″, 40″, 48″ and 72″ manual bending brake on stand"),
    "tm-w1220n": dict(dir=BRAKE, src="W2.5X1220N.png", alt="W2.5×1220N floor brake with counterweights"),
    "tm-w1060": dict(dir=BRAKE, src="W1.2x1060.jpg", alt="W1.2×1060 hand brake on stand"),
    "tm-w1050f": dict(dir=BRAKE, src="W1.5x1050F.jpg", alt="W1.5×1050F floor brake"),
    "tm-rb1100": dict(dir=BRAKE, src="RB1100.JPG", alt="RB1100 roller stand"),
    "tm-rb1000": dict(dir=BRAKE, src="RB1000.jpg", alt="RB1000 roller stand with tripod base"),
})

# the owner's WeTransfer "pictures for English wheel" (Nov 6 2026): of its 24 photos only the planishing hammers and the notchers are on the
# site — the English wheels (F-series), shrinker-stretchers (SS-, FSM-16, SM-16B), SG18 and RS018 are not, so they are left out.  The
# PPH500, on the site with no photo, gets its photo.  white: the "Optional stand" note and its arrow printed on the UFP-2 photo; boxes: the
# arrow tip where it touches the stand.
WHEEL = "/home/claude/ttmc-new/english_wheel_2026-11-06/"
PHOTOS.update({
    "tm-pph610": dict(dir=WHEEL, src="PPH610.psd", alt="PPH-610 pneumatic planishing hammer, 24″ throat, 16 ga"),
    "tm-pph500": dict(dir=WHEEL, src="PPH500.png", alt="PPH500 pneumatic planishing hammer, 19-5/8″ throat, on stand"),
    "tm-ufp2": dict(dir=WHEEL, src="UFP-2.png", alt="UFP-2 planishing hammer and English wheel in one",
                    white=[(806, 944, 1116, 1003), (940, 990, 1446, 1058)], boxes=[(797, 950, 808, 978)]),
    "tm-ptn30": dict(dir=WHEEL, src="PTN-30.png", alt="PTN-30 motorized tube and pipe notcher with hole saw and degree wheel"),
    "tm-ptn12u": dict(dir=WHEEL, src="PTN-12U.png", alt="PTN-12U electric pipe notcher"),
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
    elif im.mode == "RGBA" and key.startswith(("tm-", "tt-")):
        # a supplier cut-out: the pixels under the transparent area are the old studio background (grey wall, floor
        # shadow), which a plain RGB conversion would bring back — composite on white so BiRefNet sees a clean photo
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im).convert("RGB")
    if p.get("white"):         # a note or arrow printed on the white background: painted white, so no red is left for LaMa to spread
        from PIL import ImageDraw
        draw = ImageDraw.Draw(im)
        for box in p["white"]:
            draw.rectangle((box[0], box[1], box[2] - 1, box[3] - 1), fill=(255, 255, 255, 255) if im.mode == "RGBA" else (255, 255, 255))
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
    elif key.startswith("tt-"):
        os.makedirs(DST_TT, exist_ok=True)
        im.convert("RGB").save(os.path.join(DST_TT, key + ".jpg"), quality=92)
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
