#!/usr/bin/env python3
"""Şahinler photos: pick the source files, erase the supplier's logos / nameplates (tools/delogo.py) and write
clean, downscaled copies to tools/src-images/sahinler/<key>.{png,jpg}.  The site pipeline (tools/make_images.py)
then cuts them out (BiRefNet) and makes the WebP variants.

Sources (not in the repo): the hi-res photos the customer received from Şahinler —
  /home/claude/sahinler/photos/dekupaj/   "DEKUPAJLI YENİ FOTOLAR" (new cut-out photos on white, 6720 px)
  /home/claude/sahinler/photos/cat/       "Catalogue photos" folder, converted to PNG
  /home/claude/sahinler/orig/img/         photos extracted from the manufacturer's catalogue PDF (grey page bg)

    python3 tools/sahinler_photos.py [key ...]      (no keys = all)   then  python3 tools/make_images.py --only ...

Boxes are (x0, y0, x1, y1, mode) in source pixels; "all" fills the whole box from its surroundings.  Every box
was placed from a gridded preview and checked on a contact sheet (tools/sahinler_photos.py --check).
"""
import json
import os
import sys

from PIL import Image, PngImagePlugin

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delogo import delogo  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
PngImagePlugin.MAX_TEXT_CHUNK = 64 * 1024 * 1024

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "tools", "src-images", "sahinler")
D = "/home/claude/sahinler/photos/dekupaj/"
C = "/home/claude/sahinler/photos/cat/"
P = "/home/claude/sahinler/orig/img/"
MAX_SIDE = 2600

A = "lama"
# key: dict(src, boxes=[...], crop=(x0,y0,x1,y1), alt, cutout=True|False|None(auto), hero=False)
PHOTOS = {
    # ---- plate rolls ---------------------------------------------------------------------------------------
    "sh-4rhss-30-380-nc": dict(src=C + "4RHSS-30-380-NC.png", boxes=[(4225, 990, 4385, 1070, A)],
                               alt="Şahinler 4R HSS 30-380 NC hydraulic heavy-duty 4-roll plate roll, 10 ft, with the NC console"),
    "sh-4rhss-heavy": dict(src=C + "4rhss-new.png", boxes=[(2946, 504, 3206, 664, A), (2516, 464, 2756, 574, A), (2180, 950, 2405, 1045, A)],
                           alt="4R HSS heavy-duty 4-roll plate roll with hydraulic drop-end and mobile control console"),
    "sh-4rhss-crane": dict(src=C + "4R-HSS-UST-vinc.png", alt="4R HSS — optional overhead crane for large diameters"),
    "sh-4rhss-side-supports": dict(src=C + "4R-HSS-yan-dayama.png", alt="4R HSS — optional hydraulic side supports and overhead crane"),
    "sh-4rhss-dro": dict(src=C + "4RHSS-3-dijital-g-sterge.png", alt="4R HSS — three digital readouts on the mobile control panel", cutout=False),
    "sh-4rhss-cone": dict(src=C + "4RHSS-Konik-k-v-rma-aparat.png", alt="4R HSS — cone-bending device on the roll end", cutout=False),
    "sh-4rhs-25-245": dict(src=D + "p15-4R-HS-25-245.jpg", boxes=[(1140, 1505, 1265, 1580, A)],
                           alt="Şahinler 4R HS 25-245 hydraulic 4-roll plate roll, 8.4 ft, with the mobile control console"),
    "sh-4rhs-30-190": dict(src=C + "4R-HS-30-190.png", boxes=[(470, 578, 635, 660, A)],
                           alt="4R HS 30-190 hydraulic 4-roll plate roll, 10 ft"),
    "sh-4rhs-20-260-crane": dict(src=C + "4R-HS-20-260.png", boxes=[(406, 1358, 576, 1438, A)],
                                 alt="4R HS 20-260 with the optional overhead crane and side supports"),
    "sh-4rhs-cone-device": dict(src=C + "4R-HS-Konik-aparat.png", alt="4R HS — cone-bending device", cutout=False),
    "sh-4rh-10-90-nc": dict(src=D + "p18-4RH-10-90-NC.jpg", alt="Şahinler 4RH 10-90 NC cassette-type hydraulic 4-roll plate roll with NC console"),
    "sh-4rh-10-90-detail": dict(src=D + "p18-4RH-10-90-NC-DETAY-3.jpg", boxes=[(942, 3490, 1662, 4380, A)],
                                alt="4RH — the four rolls move in a cassette-type frame; hydraulic drop-end and feeding table"),
    "sh-4rh-10-90-side": dict(src=D + "p18-4RH-10-90-NC-detay.jpg", boxes=[(1325, 2300, 1425, 2375, A)],
                              alt="4RH 10-90 NC — feeding table and drop-end side"),
    "sh-4rh-10-130-nc": dict(src=C + "4RH-10-130-NC.png", boxes=[(540, 312, 645, 368, A)], alt="4RH 10-130 NC with the NC control console"),
    "sh-3ruhs-30-550": dict(src=P + "p18-001.png", boxes=[(410, 18, 530, 76, A), (975, 295, 1110, 385, A), (1250, 285, 1395, 375, A)],
                            cutout=True, alt="Şahinler 3R UHS 30-550 hydraulic translating heavy-duty 3-roll plate roll, 10 ft"),
    "sh-3rhs-20-210": dict(src=D + "p22-3R-HS-20-210.jpg", boxes=[(862, 1360, 1202, 1550, A)],
                           alt="Şahinler 3R HS 20-210 hydraulic 3-roll plate roll, 6.7 ft, with the mobile control console"),
    "sh-3rhs-detail": dict(src=D + "p22-3R-HS-20-210-detay.jpg", alt="3R HS — hydraulic drop-end and roll ends with extended shafts"),
    "sh-3rhs-drop-end": dict(src=D + "p23-8Q9A0926.jpg", alt="3R HS — drop-end side with the hydraulic system and pressure gauges"),
    "sh-4rhc-10-155": dict(src=C + "4R-HC-2018.png", boxes=[(1852, 1292, 2192, 1422, A)],
                           alt="Şahinler 4R HC 10-155 hydraulic 4-roll conical plate roll with cone-machined rolls"),
    # ---- section & pipe bending -----------------------------------------------------------------------------
    "sh-bt114s": dict(src=C + "BT-114-S.png", alt="Şahinler BT 114-S automatic pipe polishing and sanding machine with the mobile control pendant"),
    "sh-bt114s-rail": dict(src=C + "bt114-s-pipes.png", cutout=False, alt="Stainless handrail tube polished on the BT 114-S"),
    "sh-bt114s-tube": dict(src=C + "BT-114-uygulama.png", cutout=False, alt="BT 114-S — satin-finished stainless tube"),
    # the p69 photos are of the SDK circle cutting & flanging machine (verified visually)
    "sh-sdk6-b": dict(src=D + "p69-8Q9A5018.jpg", boxes=[(4995, 945, 5270, 1095, A)], alt="Şahinler SDK 6 circular cutting and flanging machine — part carrier, flanging head and control box"),
    "sh-sdk-rolls": dict(src=D + "p69-20230306-15144-.jpg", alt="SDK — top and bottom flanging rolls"),
    "sh-sdk-control": dict(src=D + "p69-8Q9A5009.jpg", alt="SDK — control box with touchscreen and pendant"),
    "sh-spb60": dict(src=C + "SPB-60-N.png", alt="Şahinler SPB 60 NC pipe draw bender"),
    "sh-spb76": dict(src=C + "SPB-76-N.png", alt="Şahinler SPB 76 NC pipe draw bender with a bent tube in the tooling"),
    "sh-spb-handrail": dict(src=C + "spb-60-uyg-1.png", alt="SPB — stainless handrail bent on the SPB 60", cutout=False),
    "sh-pk30": dict(src=C + "PK-30-2018.png", alt="Şahinler PK 30 motorized section and pipe bender"),
    "sh-pk35": dict(src=C + "PK-35F.png", boxes=[(1230, 1212, 1510, 1332, A)], alt="Şahinler PK 35 motorized section and pipe bender"),
    "sh-pk35-b": dict(src=D + "p31-PK-35psd.jpg", boxes=[(2172, 2450, 2642, 2670, A), (2907, 2255, 3137, 2565, A)],
                      alt="PK 35 with the foot pedal and the adjustable guide rolls"),
    "sh-hpk40": dict(src=C + "HPK-40-Yeni2.png", boxes=[(1827, 2272, 2162, 2437, A), (2372, 1907, 2507, 2087, A)],
                     alt="Şahinler HPK 40 hydraulic section and pipe bender with the mobile control panel"),
    "sh-hpk40-coil": dict(src=C + "HPK-40-uyg-9.png", alt="HPK 40 — spiral bending with the optional crane", cutout=False),
    "sh-hpk50": dict(src=D + "p33-HPK-50.jpg", boxes=[(2622, 2310, 3042, 2530, A), (3212, 2180, 3352, 2370, A)],
                     alt="Şahinler HPK 50 hydraulic section and pipe bender, 8 t hydraulic force"),
    "sh-hpk60": dict(src=D + "p34-HPK-60.jpg", boxes=[(1902, 2570, 2492, 2860, A), (2972, 2430, 3162, 2660, A)],
                     alt="Şahinler HPK 60 hydraulic section and pipe bender, 16 t hydraulic force"),
    "sh-hpk65": dict(src=D + "p35-HPK-65.jpg", boxes=[(1690, 2770, 2315, 3018, A), (2802, 2150, 2992, 2400, A)],
                     alt="Şahinler HPK 65 hydraulic section and pipe bender with the control console"),
    "sh-hpk80": dict(src=D + "p35-HPK-80.jpg", boxes=[(1342, 2880, 1902, 3160, A), (2602, 2170, 2802, 2410, A)],
                     alt="Şahinler HPK 80 hydraulic section and pipe bender with the control console"),
    "sh-hpk65-horizontal": dict(src=D + "p35-HPK-65-DETAY.jpg", boxes=[(1294, 1135, 1574, 1305, A), (1629, 1600, 1864, 1800, A)],
                                alt="HPK 65 in the horizontal working position"),
    "sh-hpk-guide-detail": dict(src=D + "p35-8Q9A0813.JPG", crop=(0, 0, 4480, 5300), alt="HPK — hydraulic lateral guide roll with scale"),
    "sh-hpk-console": dict(src=D + "p35-ekran.jpg", alt="HPK — mobile control console with two digital readouts"),
    "sh-hpk100": dict(src=D + "p37-HPK-100.jpg", boxes=[(2422, 2750, 3042, 3070, A)],
                      alt="Şahinler HPK 100 hydraulic section and pipe bender with the control console"),
    "sh-hpk100-rolls": dict(src=D + "p37-8Q9A0985.jpg", alt="HPK 100 — three driven rolls and hydraulic lateral guides"),
    "sh-hpk100-guide": dict(src=D + "p37-8Q9A067.jpg", crop=(0, 700, 4480, 4650), alt="HPK 100 — hydraulic lateral guide roll"),
    "sh-hpk100-handwheel": dict(src=D + "p37-8Q9A0763.JPG", crop=(0, 1100, 4480, 5950), alt="HPK 100 — manual lateral guide and hand wheel"),
    "sh-hpk100-horizontal": dict(src=D + "p37-8Q9A0786.jpg", alt="HPK 100 in the horizontal working position"),
    "sh-hpk120nc": dict(src=D + "p38-HPK-120-NC.jpg", boxes=[(1572, 2590, 2292, 2940, A)],
                        alt="Şahinler HPK 120 NC hydraulic section and pipe bender with hydraulic lateral guides and NC console"),
    "sh-hpk120-panel": dict(src=D + "p38-HPK-120-NC-detay.jpg", alt="HPK 120 — hydraulic speed and pressure adjustment valves"),
    "sh-hpk160dp": dict(src=C + "HPK-160-DP-NC.png", boxes=[(3505, 1375, 3815, 1575, A)],
                        alt="Şahinler HPK 160 DP NC heavy-duty section and beam bender with the NC console"),
    "sh-hpk240dp": dict(src=C + "HPK-240-DP.png", boxes=[(1482, 1507, 2042, 1842, A), (3465, 745, 3805, 1075, A)],
                        alt="Şahinler HPK 240 DP heavy-duty section and beam bender"),
    "sh-hpkdp-top": dict(src=C + "A26A8896.png", alt="HPK DP — rolls and hydraulic lateral guide rolls seen from above"),
    "sh-hpk-halfpipe": dict(src=C + "HPK-yar-m-boru-k-v-rma-aparat.png", alt="HPK — optional half-pipe bending attachment", cutout=False),
    "sh-ipn-attachment": dict(src=C + "IPN-Bending-Attachment.png", alt="HPK DP — IPN / UPN beam bending attachment"),
    "sh-tc42": dict(src=C + "A26A9019.png", cutout=False, alt="Şahinler TC-42 NC tube coiling machine rolling a spiral coil between the hydraulic lateral supports"),
    "sh-tc42-coil": dict(src=C + "TC-42-Ugulama-1.png", alt="TC-42 NC — variable-pitch spiral coil"),
    # ---- ironworkers & punching -----------------------------------------------------------------------------
    "sh-hkm40": dict(src=D + "p52-HKM-40.jpg", boxes=[(3302, 2170, 3822, 2410, A), (4022, 1760, 4292, 2040, A), (2562, 1700, 2722, 1930, A)],
                     alt="Şahinler HKM 40 single-piston hydraulic steelworker, 44 US tons"),
    "sh-hkm40-rear": dict(src=D + "p52-HKM-40-DETAY.jpg", alt="HKM 40 — bar shear and angle shear side"),
    "sh-hkm60": dict(src=D + "p53-HKM-60.jpg", boxes=[(3802, 2670, 4242, 2920, A), (3992, 1980, 4262, 2240, A), (2452, 1700, 2642, 1950, A)],
                     alt="Şahinler HKM 60 single-piston hydraulic steelworker with five work stations"),
    "sh-hkm65v": dict(src=C + "HKM-65-V.png", boxes=[(1945, 1099, 2535, 1279, A)], alt="Şahinler HKM 65 V vertical single-piston steelworker"),
    "sh-hkm55": dict(src=D + "p55-HKM-55.jpg", boxes=[(1915, 2625, 2375, 2910, A), (925, 1950, 1005, 2250, A)],
                     alt="Şahinler HKM 55 double-piston hydraulic steelworker with two foot pedals"),
    "sh-hkm65": dict(src=D + "p55-HKM-65.jpg", boxes=[(2902, 2950, 3392, 3200, A), (1782, 2320, 1952, 2630, A)],
                     alt="Şahinler HKM 65 double-piston hydraulic steelworker, 72 US tons"),
    "sh-hkm85": dict(src=D + "p55-HKM-85.jpg", boxes=[(3072, 2870, 3572, 3130, A), (1922, 2230, 2092, 2550, A)],
                     alt="Şahinler HKM 85 double-piston hydraulic steelworker, 94 US tons"),
    "sh-hkm-lube": dict(src=D + "p55-8Q9A5298.JPG", alt="HKM — central lubrication pump"),
    "sh-hkm115": dict(src=D + "p56-HKM-115.jpg", boxes=[(2825, 2822, 3325, 3052, A), (1965, 2272, 2115, 2582, A)],
                      alt="Şahinler HKM 115 double-piston hydraulic steelworker, 127 US tons"),
    "sh-hkm115-detail": dict(src=D + "p56-HKM-115-DETAY.jpg", boxes=[(1102, 4090, 1602, 4390, A)],
                             alt="HKM 115 — punching station and angle shear with LED lighting"),
    "sh-hkm175": dict(src=D + "p57-8Q9A3971.jpg", boxes=[(3382, 920, 3892, 1150, A), (2222, 2620, 2402, 2930, A)],
                      alt="Şahinler HKM 175 double-piston hydraulic steelworker, 193 US tons"),
    "sh-hkm175-operators": dict(src=D + "p57-hkm-175.jpg", boxes=[(1573, 375, 1863, 485, A), (373, 730, 498, 800, A), (823, 1525, 913, 1685, A)],
                                alt="HKM 175 — two operators working at the same time on the punching and shearing stations"),
    "sh-hkm175-backgauge": dict(src=D + "p57-8Q9A4081.JPG", boxes=[(5112, 1470, 5282, 1730, A)], alt="HKM 175 — electrical back gauge on the shear station"),
    "sh-hkm-tool-brake": dict(src=C + "HKM-abkant.png", alt="HKM optional press-brake tool"),
    "sh-hkm-tool-stripper": dict(src=C + "HKM-hidrolik-siyirici.png", alt="HKM optional hydraulic stripper"),
    "sh-hkm-tool-notch": dict(src=C + "HKM-u-centik.png", alt="HKM rectangular notching tool"),
    "sh-hkm-tool-radius": dict(src=C + "HKM-lama-radius.png", alt="HKM flat-bar radius tool"),
    "sh-hkm-tool-punches": dict(src=C + "HKM-Z-mba.png", alt="HKM punches and dies"),
    "sh-hpm65": dict(src=D + "p60-HPM-65.jpg", boxes=[(4512, 540, 4782, 860, A)], alt="Şahinler HPM 65 hydraulic punching machine, 72 US tons"),
    "sh-hpm-station": dict(src=D + "p60-8Q9A5464.jpg", alt="HPM — punching station with stripper and table"),
    "sh-hpm-punch": dict(src=D + "p60-8Q9A5432-copy.jpg", alt="HPM — punch and die"),
    "sh-hpm30": dict(src=C + "hpm30-render.png", alt="Şahinler HPM 30 hydraulic punching machine"),
    "sh-hpm115": dict(src=C + "hpm-115-new.png", boxes=[(879, 185, 1254, 315, A)], alt="Şahinler HPM 115 hydraulic punching machine, 127 US tons"),
    "sh-hpm85dp": dict(src=C + "hpm-85-dublepunch.png", boxes=[(1690, 1415, 2000, 1525, A)], alt="Şahinler HPM 85 DP double-head hydraulic punching machine"),
    "sh-hpm85nc": dict(src=C + "HPM-85-NC-TABLE.png", boxes=[(711, 654, 886, 719, A)], alt="Şahinler HPM 85 NC punching line with NC table and control console"),
    "sh-hpm115cnc": dict(src=C + "HPM115CNC.png", boxes=[(1669, 900, 1909, 1015, A)], alt="Şahinler HPM 115 CNC punching machine with CNC table and Siemens control"),
    # ---- circle cutting & flanging ---------------------------------------------------------------------------
    "sh-sdk6": dict(src=C + "SDK-6.png", boxes=[(1880, 262, 2000, 300, A)], alt="Şahinler SDK 6 circular sheet cutting and flanging machine, Ø12.5 ft"),
    "sh-sdk8": dict(src=C + "sdk-8.png", boxes=[(1655, 282, 1790, 352, A)], alt="Şahinler SDK 8 circular sheet cutting and flanging machine, Ø15 ft"),
    "sh-sdk8-head": dict(src=P + "p61-000.png", crop=(0, 0, 2420, 2472), boxes=[(1470, 565, 1670, 668, A)], cutout=True,
                         alt="SDK 8 — flanging head, part carrier and control panel"),
    "sh-sdk8-lcd": dict(src=C + "SDK-8-LCD-ektran.png", alt="SDK — LCD touchscreen operator panel", cutout=False),
    "sh-efm6": dict(src=P + "p63-000.png", crop=(130, 0, 2535, 2545), cutout=True, alt="Şahinler EFM 6 elliptical cutting and flanging machine"),
    "sh-efm-vacuum": dict(src=C + "efm-vakumlu.png", alt="EFM 6 — flanging head with the optional vacuum system", cutout=False),
    # ---- presses & corner notchers -------------------------------------------------------------------------
    "sh-dks200": dict(src=C + "dk-s.png", boxes=[(1214, 496, 1454, 586, A), (494, 691, 564, 781, A)],
                      alt="Şahinler DK-S 200 3-axis moving straightening press with safety rails"),
    "sh-dks400": dict(src=C + "DK-S-400.png", boxes=[(1767, 952, 2227, 1142, A), (1927, 1172, 2057, 1272, A)],
                      alt="Şahinler DK-S 400 3-axis moving straightening press, 441 US tons"),
    "sh-dks-remote": dict(src=C + "DKS-uzaktan-kumanda.png", alt="DK-S — optional remote control", cutout=False),
    "sh-dpm": dict(src=P + "p68-001.png", boxes=[(606, 221, 871, 371, A)], cutout=True, alt="Şahinler DPM hydraulic shop press"),
    "sh-dpmk": dict(src=P + "p69-001.png", crop=(0, 0, 1410, 1563), boxes=[(363, 144, 563, 256, A)], cutout=True,
                    alt="Şahinler DPM-K hydraulic shop press with mobile cylinder"),
    "sh-dk": dict(src=P + "p70-000.png", boxes=[(697, 200, 857, 302, A)], cutout=True, alt="Şahinler DK hydraulic shop press with mobile cylinder and hand wheel"),
    "sh-dpm200": dict(src=P + "p70-002.png", crop=(0, 0, 1229, 1520), boxes=[(374, 362, 534, 462, A)], cutout=True, alt="Şahinler DPM 200 t hydraulic shop press"),
    "sh-at": dict(src=P + "p72-003.png", crop=(507, 0, 1690, 1497), boxes=[(315, 190, 485, 255, A)], cutout=True, alt="Şahinler AT universal T-slot hydraulic press"),
    "sh-ap": dict(src=P + "p73-001.png", crop=(350, 0, 1810, 1694), boxes=[(612, 232, 820, 350, A)], cutout=True, alt="Şahinler AP garage-type hydraulic press brake"),
    "sh-hnm6v": dict(src=P + "p74-001.png", boxes=[(1084, 641, 1249, 714, A)], cutout=True, alt="Şahinler HNM 6V variable-angle hydraulic corner notcher"),
    "sh-hnm6f": dict(src=P + "p75-000.png", boxes=[(513, 311, 686, 399, A)], cutout=True, alt="Şahinler HNM 6F fixed 90° hydraulic corner notcher"),
}


def process(key, spec):
    im = Image.open(spec["src"])
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
    if spec.get("crop"):
        im = im.crop(spec["crop"])
    boxes = spec.get("boxes") or []
    if boxes:
        im = delogo(im, boxes)
    s = MAX_SIDE / max(im.size)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    os.makedirs(DST, exist_ok=True)
    if im.mode == "RGBA":
        out = os.path.join(DST, key + ".png"); im.save(out, optimize=True)
    else:
        out = os.path.join(DST, key + ".jpg"); im.save(out, quality=92)
    return out, im.size, s


def check_sheet(keys):
    """contact sheet: for every box, the source crop with the rough box (red) and the found logo box (green), and
    the cleaned crop next to it; the key is written inside the tile"""
    from PIL import ImageDraw
    from delogo import find_logo
    import numpy as np
    tiles = []
    for key in keys:
        spec = PHOTOS[key]
        if not spec.get("boxes"):
            continue
        src = Image.open(spec["src"]); src = src.convert("RGBA") if src.mode in ("RGBA", "LA", "P") else src.convert("RGB")
        if spec.get("crop"):
            src = src.crop(spec["crop"])
        rep = []
        cleaned = delogo(src, spec["boxes"], report=rep)
        rgb = np.asarray(src.convert("RGB"))
        for bi, b in enumerate(spec["boxes"]):
            x0, y0, x1, y1 = b[:4]; mx, my = (x1 - x0) + 20, (y1 - y0) + 20
            box = (max(0, x0 - mx), max(0, y0 - my), min(src.width, x1 + mx), min(src.height, y1 + my))
            found = rep[bi] if bi < len(rep) else None
            a = src.crop(box).convert("RGB"); d = ImageDraw.Draw(a)
            d.rectangle([x0 - box[0], y0 - box[1], x1 - box[0], y1 - box[1]], outline=(255, 0, 0), width=3)
            if found:
                d.rectangle([found[0] - box[0], found[1] - box[1], found[2] - box[0], found[3] - box[1]], outline=(0, 220, 0), width=3)
            c = cleaned.crop(box).convert("RGB")
            for t in (a, c):
                t.thumbnail((300, 300))
            ImageDraw.Draw(a).text((4, 4), key, fill=(255, 255, 0)); ImageDraw.Draw(c).text((4, 4), "cleaned", fill=(255, 255, 0))
            tiles += [a, c]
    cols = 8; W = 300
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (W + 4), rows * (W + 4)), (40, 40, 40))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * (W + 4) + 2, (i // cols) * (W + 4) + 2))
    out = "/home/claude/sahinler/photos/work/check-boxes.jpg"; sheet.save(out, quality=82); print(out, sheet.size)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keys = args or list(PHOTOS)
    if "--check" in sys.argv:
        check_sheet(keys); return
    for key in keys:
        out, size, s = process(key, PHOTOS[key])
        print(f"{key:26s} {size} scale {s:.2f} boxes={len(PHOTOS[key].get('boxes') or [])} -> {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
