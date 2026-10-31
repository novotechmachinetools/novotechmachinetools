#!/usr/bin/env python3
"""NovoTech value-line sheet-metal machines (CNC / NC / electric press brakes, hydraulic shears, V-grooving, panel benders,
ironworker) — supplier renders and photos → logo-free sources in tools/src-images/value-sheet/.

Sources (outside the repository): the supplier's website renders (`/home/claude/value-sheet-src/img/`, 1,600 px WebP, most with a real
alpha channel) and the hi-res factory photos staged from the user's laptop (`/home/claude/value-sheet-src/hires/`).  The machines are sold under NovoTech's name, so every supplier badge and model label that carries the supplier's
name is boxed by hand (source pixels, located on 100 px grid views) and filled with LaMa (tools/delogo.py, mode "lama");
Chinese warning stickers on the renders are filled the same way.  Renders on an opaque white background get an alpha
channel by flood-filling the background from the border (`white_alpha`), so no BiRefNet pass is needed for them.

    python3 tools/vl_sheet_photos.py [keys]          export
    python3 tools/vl_sheet_photos.py --check [keys]  contact sheet with the boxes drawn (/home/claude/value-sheet-src/work/)
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delogo import delogo  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/value-sheet-src/img/"
HI = "/home/claude/value-sheet-src/hires/"
WORK = "/home/claude/value-sheet-src/work/"
OUT = os.path.join(ROOT, "tools", "src-images", "value-sheet")
MAX_SIDE = 2600
A = "lama"
Image.MAX_IMAGE_PIXELS = None


def R(name, alt, boxes=(), **kw):      # website render / photo (1,600 px)
    return dict(src=SRC + name, alt=alt, boxes=list(boxes), **kw)


def H(path, alt, **kw):                # hi-res factory photo (detail, kept as a photo)
    return dict(src=HI + path, alt=alt, boxes=[], cutout=False, **kw)


PB_CNC = "PRESS BRAKE/CNC/WAD-110T-3200-DA53T-4+1蓝白新款/"
PB_NC = "PRESS BRAKE/NC/WC67E-200T-3200-E315PS(手动补偿）/"
SH_G = "SHEARING MACHINE/GUILLOTINE/8x3200/"
SH_S = "SHEARING MACHINE/SWING BEAM/QC12K-4×2500-E21S/"

PHOTOS = {
    # ---------------------------------------------------------------- CNC hydraulic press brakes (WAD)
    "vl-wad-1": R("WAD-electro-hydraulic-servo-CNC-press-brake.png", "NovoTech WAD 100T/3200 CNC hydraulic press brake — 10 ft × 110 US tons, front view with the Delem control on its swing arm",
                  boxes=[(600, 140, 775, 290)]),
    "vl-wad-2": R("hero-4-16.9_w1600.webp", "WAD 100T/3200 CNC hydraulic press brake — front view with front support arms", boxes=[(520, 135, 690, 275)], cutout=True),
    "vl-wade-1": R("WADE-electro-hydraulic-servo-CNC-press-brake.png", "WAD 110T/3200 CNC hydraulic press brake with the 2D graphic touchscreen control",
                   boxes=[(470, 140, 620, 280), (200, 650, 265, 685), (1280, 650, 1340, 685)]),
    "vl-wad-heavy": R("%E5%A4%A7%E5%9E%8B-%E9%80%8F%E6%98%8E_w1600.webp", "Heavy-duty CNC press brake with twin sheet followers — 30 ft bending length", boxes=[(985, 345, 1165, 415)]),
    "vl-wad-tandem": R("hero16.9_w1600.webp", "Tandem CNC press brake — two 300 t × 13 ft machines on one control with sheet followers",
                       boxes=[(330, 240, 400, 270), (795, 205, 855, 235), (205, 590, 275, 620), (495, 595, 565, 625), (790, 600, 860, 630), (1055, 605, 1125, 635)], cutout=True),
    "vl-wad-tandem-2": R("01_w1600-7.webp", "Tandem press brake with CNC sheet followers for long, heavy plate"),
    "vl-wad-follower": R("05_w1600-11.webp", "Heavy-duty CNC press brake with a CNC sheet follower table", boxes=[(800, 205, 885, 290), (610, 340, 665, 360)]),
    "vl-wad-robot": R("44.05_w1600.webp", "WAD 110T/3200 CNC press brake in a robot bending cell", boxes=[(800, 110, 890, 195)], cutout=False),
    "vl-pb-backgauge": R("03_w1600-8.webp", ("4-axis CNC back gauge X-R-Z1-Z2, option: the fingers move in depth (X) and height (R), and each finger tower travels along "
                         "the beam on its own (Z1, Z2) — ball screws, linear guides and servo drives"), cutout=False),
    "vl-pb-clamps": R("04_w1600-17.webp", "European-style tool clamping along the ram with the light curtain at the side", cutout=False),
    "vl-pb-quickclamp": R("04_w1600-18.webp", "Quick-release tool clamps — the punch changes without tools", boxes=[(980, 275, 1180, 355), (585, 365, 705, 425)], cutout=False),
    "vl-pb-clamp-open": R("%E6%B8%85%E7%90%86_w1600.webp", "Quick clamp opened for a punch change", cutout=False),
    "vl-pb-cylinders": R("02_w1600-38.webp", "Y1 and Y2 ram cylinders with the hydraulic blocks on top of the frame", cutout=False),
    "vl-pb-da53": R("01_w1600-11.webp", "Delem DA-53Tx touchscreen control — standard on the CNC press brakes", cutout=False),
    "vl-pb-da58": R("02_w1600-10.webp", "Delem DA-58Tx 18.5″ 2D graphic control with automatic bend sequence calculation", cutout=False),
    "vl-pb-da66": R("04_w1600-6.webp", "Delem DA-66T control (discontinued — replaced by the DA-66S; photo no longer used on the site)", cutout=False),
    "vl-pb-fingers": R("03_w1600-15.webp", "Back gauge stop fingers on the X-R beam", cutout=False),
    "vl-pb-hydclamp": R("05_w1600-12.webp", "Hydraulic tool clamping — one lever locks the whole ram", cutout=False),
    "vl-pb-dsp": R("04_w1600_w1600.webp", "DSP laser finger protection under the punch", cutout=False),
    "vl-pb-crowning": R("04_w1600-3-1.webp", "CNC crowning cylinders under the table compensate deflection along the bend", cutout=False),
    "vl-pb-servo-bg": R("03_w1600-10.webp", "CNC motorised crowning: the motor and gearbox at the end of the table drive the "
                       "crowning wedges under the die holder, and the control sets the crowning for every bend, for the same "
                       "angle along the whole part", cutout=False),   # a crowning unit, not the back gauge (the owner, Oct 31 2026)
    "vl-pb-follower-detail": R("03_w1600-6.webp", "CNC sheet follower supporting a large blank through the bend", cutout=False),
    # ---------------------------------------------------------------- NC press brakes (WC67K / E)
    "vl-nc-1": R("nc-16.9_w1600.webp", "NovoTech WC67E 100T/3200 NC hydraulic press brake — 10 ft × 110 US tons, torsion-bar synchronised, with the Estun control",
                 boxes=[(545, 165, 665, 245), (265, 380, 320, 690), (1275, 380, 1330, 690)], cutout=True),
    "vl-nc-backgauge": R("wc67k-backgauge.webp", "Torsion bar and the motorised X back gauge seen from the rear", cutout=False),
    "vl-nc-torsion": R("%E6%89%AD%E8%BD%B4%E5%90%8C%E6%AD%A5_w1600.webp", "Torsion-bar synchronisation of the ram — the mechanical link between the two cylinders", cutout=False),
    "vl-nc-bg-motor": R("04.1_w1600.webp", "Back gauge drive motor and ball screw on the NC press brake", cutout=False),
    "vl-nc-photo-1": H(PB_NC + "DSC02590.JPG", "NC press brake — back gauge beam with the stop fingers and linear scale"),
    "vl-nc-photo-2": H(PB_NC + "DSC02592.JPG", "NC press brake — European-style punch clamping on the ram"),
    "vl-nc-photo-3": H(PB_NC + "DSC02594.JPG", "NC press brake — ram cylinder and the mechanical depth stop"),
    # ---------------------------------------------------------------- electric press brakes (WADG)
    "vl-wadg-1": R("hero_w1600-21.webp", "NovoTech WADG 100T/3200 electric servo press brake — 10 ft × 110 US tons, dual ball-screw drive, no hydraulics",
                   boxes=[(440, 140, 580, 275)], white=True),
    "vl-wadg-robot": R("hero-16.9_w1600_5.webp", "WADG 40T/1600 electric press brake in a robot bending cell with an Estun robot", boxes=[(575, 115, 690, 235)], cutout=True),
    "vl-wadg-motors": R("Y1-Y2_w1600.webp", "Y1 and Y2 servo motors on top of the electric press brake frame", cutout=False),
    "vl-wadg-ram": R("02_w1600-40.webp", "Servo motors, belts and ball screws driving the ram of the electric press brake", cutout=False),
    "vl-wadg-drawing": R("02_w1600-34.webp", "Electric press brake — frame, dual lead screws and ram", cutout=False),
    "vl-wadg-support": R("04_w1600-12.webp", "Front support arms on linear rails", cutout=False),
    "vl-wadg-tooling": R("50.05_w1600.webp", "Standard punches and dies supplied with the press brakes", cutout=False),
    "vl-wadg-parts": R("68.05_w1600.webp", "Typical parts bent on the electric press brake — brackets, channels and boxes", cutout=False),
    # ---------------------------------------------------------------- swing beam shears (QC12K / E)
    "vl-qc12k-1": R("%E5%89%AA%E6%9D%BF%E6%9C%BA3_w1600_w1600.webp", "NovoTech QC12K hydraulic swing beam shear — 10 ft × 1/4″ with the Estun E21S control", boxes=[(895, 250, 1030, 325)]),
    "vl-qc12k-2": R("%E5%89%AA%E6%9D%BF%E6%9C%BA-16.9_w1600.webp", "Hydraulic swing beam shear with the control on a swing arm and front ball-transfer tables", boxes=[(775, 265, 900, 345)], cutout=True),
    "vl-qc12k-rear": R("04_w1600-1.webp", "Swing beam shear from the rear — back gauge beam, hydraulic cylinders and the light-barrier guard"),
    "vl-sh-backgauge": R("%E5%90%8E%E6%8C%A1%E6%96%99_w1600.webp", "Motorised back gauge on ball screws with the sheet support fingers", cutout=False),
    "vl-sh-holddowns": R("02_w1600-1.webp", "Hydraulic hold-down cylinders along the cutting line", cutout=False),
    "vl-sh-holddowns-2": R("06_w1600-3-1.webp", "Hold-downs and blade gap seen from the operator side", cutout=False),
    "vl-sh-e21s": R("03_w1600.webp", "Estun E21S and E200PS NC shear controls — back gauge, cutting angle and blade clearance", cutout=False),
    "vl-sh-roller": R("11_w1600-1-1.webp", "Roller sheet support in the front table", cutout=False),
    "vl-sh-photo-1": H(SH_S + "DSC02656.JPG", "Swing beam shear — hydraulic cylinder and back gauge drive"),
    "vl-sh-photo-2": H(SH_S + "DSC02658.JPG", "Swing beam shear — main motor and pump on top of the oil tank"),
    "vl-sh-photo-3": H(SH_S + "DSC02659.JPG", "Swing beam shear — blade gap adjustment and hold-down manifold"),
    # ---------------------------------------------------------------- guillotine shears (Q11K / E)
    "vl-q11k-1": R("%E9%97%B8%E5%BC%8F%E5%89%AA%E6%9D%BF%E6%9C%BA-%E9%80%8F%E6%98%8E_w1600-1.webp", "NovoTech Q11K 6×2500 hydraulic guillotine shear — 8 ft × 1/4″ with the Estun control and ball-transfer tables",
                  boxes=[(995, 255, 1175, 370), (1010, 375, 1175, 465)]),
    "vl-q11k-rear": R("%E9%97%B8%E5%BC%8F%E5%89%AA%E6%9D%BF%E6%9C%BA-%E5%90%8E%E6%8C%A1%E6%96%99_w1600.webp", "Guillotine shear from the rear — the ball-screw back gauge and sheet support"),
    "vl-q11k-rear-2": R("%E9%97%B8%E5%BC%8F%E5%89%AA%E6%9D%BF%E6%9C%BA-01_w1600.webp", "Guillotine shear — rear view with the electrical cabinet and the back gauge motor"),
    "vl-q11k-controls": R("%E9%97%B8%E5%BC%8F%E5%89%AA%E6%9D%BF%E6%9C%BA-05_w1600.webp", "Estun E21S NC control and the optional Delem DAC-360T", cutout=False),
    "vl-q11k-valve": R("%E9%97%B8%E5%BC%8F%E5%89%AA%E6%9D%BF%E6%9C%BA-03_w1600.webp", "hydraulic valve block with pressure gauge", cutout=False),
    "vl-q11k-measure": R("%E9%97%B8%E5%BC%8F%E5%89%AA%E6%9D%BF%E6%9C%BA-06_w1600.webp", "Checking the cut strip — straight, burr-free edges", cutout=False),
    "vl-q11k-feed": R("q11k-feed-opening.webp", "Feed opening with the hold-down cylinders and the roller table", cutout=False),
    "vl-q11k-rexroth": R("01.1_w1600.webp", "Directional valve of the hydraulic system", cutout=False),
    "vl-q11k-holddown": R("01_w1600-1.webp", "Hydraulic hold-down cylinders of the guillotine shear", cutout=False),
    "vl-g-photo-1": H(SH_G + "REI00065.JPG", "Guillotine shear — rake angle cylinders behind the blade beam"),
    "vl-g-photo-2": H(SH_G + "REI00082.JPG", "Guillotine shear — pressure gauge and manual valves"),
    "vl-g-photo-3": H(SH_G + "REI00088.JPG", "Guillotine shear — NC control panel"),
    "vl-g-photo-4": H(SH_G + "REI00092.JPG", "Guillotine shear — top of the frame with the main cylinder"),
    "vl-g-photo-5": H(SH_G + "REI00098.JPG", "Guillotine shear — back gauge screw and support"),
    # ---------------------------------------------------------------- ironworker (Q35Y)
    "vl-q35y-1": R("%E5%86%B2%E5%89%AA%E6%9C%BA-%E9%80%8F%E6%98%8E-%E8%93%9D_w1600.webp", "NovoTech Q35Y hydraulic ironworker — punching, flat bar, angle, round and square bar shearing and notching stations",
                   boxes=[(470, 140, 510, 275), (625, 180, 770, 220)]),
    "vl-iw-punch": R("01_w1600-27.webp", "Punching station with the hold-down and the adjustable stripper", cutout=False),
    "vl-iw-notch": R("02_w1600-32.webp", "Rectangular notching station", cutout=False),
    "vl-iw-angle": R("02_w1600-33.webp", "Angle shearing station with the guard open", cutout=False),
    "vl-iw-flat": R("03_w1600-27.webp", "Flat bar shearing station with the ruler and hold-down", cutout=False),
    "vl-iw-notch-die": R("03_w1600-28.webp", "Notching die and the opened guard", cutout=False),
    "vl-iw-tooling": R("%E6%A0%B7%E6%9C%BA_w1600-1.webp", "Punches, dies and notching tools supplied with the ironworker", cutout=False),
    "vl-iw-valve": R("%E6%B6%B2%E5%8E%8B_w1600-1.webp", "Hydraulic valve block of the ironworker", cutout=False),
    "vl-iw-motor": R("03_w1600-1-3.webp", "Main motor and pump unit", cutout=False),
    "vl-iw-gauge": R("%E6%B5%8B%E8%AF%95_w1600.webp", "Checking the angle on a sheared and bent sample", cutout=False),
    # ---------------------------------------------------------------- V-grooving (horizontal / vertical)
    "vl-vg-h-1": R("%E5%8D%A7%E5%BC%8F%E5%BC%80%E6%A7%BD%E6%9C%BA-%E9%80%8F%E6%98%8E_w1600-2.webp", "NovoTech horizontal CNC V-grooving machine — 13 ft × 4 ft table with the four-tool grooving head",
                   boxes=[(195, 590, 405, 700), (915, 290, 975, 310), (1245, 445, 1335, 490), (520, 600, 605, 675), (1150, 440, 1195, 490)]),
    "vl-vg-v-1": R("%E5%BC%80%E6%A7%BD%E6%9C%BA_w1600.webp", "NovoTech vertical CNC V-grooving machine — the sheet stands against the clamps, 13 ft grooving length",
                   boxes=[(315, 315, 395, 350), (700, 340, 840, 390), (140, 425, 340, 460)]),
    "vl-vg-v-scene": R("01_w1600-1-3.webp", "Vertical V-grooving machine on the shop floor", boxes=[(290, 315, 385, 350), (700, 345, 865, 395), (120, 455, 350, 490), (540, 530, 585, 555)], cutout=False),
    "vl-vg-head": R("vg-h-four-tool.webp", "Four-tool grooving head of the horizontal machine", cutout=False),
    "vl-vg-cutters": R("vg-v-cutters.webp", "Grooving cutters of the vertical machine", cutout=False),
    "vl-vg-trial": R("GROOVE-TRIAL-%E8%AF%95%E5%8A%A0%E5%B7%A5_w1600.webp", "V-groove cut into stainless sheet before bending", cutout=False),
    "vl-vg-clamps": R("%E5%A4%B9%E7%B4%A7_w1600.webp", "Pneumatic sheet clamps along the table", cutout=False),
    "vl-vg-corner": R("%E5%A4%B9%E8%A7%92_w1600.webp", "Sharp outside corner bent after V-grooving", cutout=False),
    "vl-vg-table": R("01_w1600-26.webp", "Horizontal V-grooving machine — table and gantry", cutout=False),
    "vl-vg-beam": R("03_w1600-31.webp", "Vertical machine — grooving beam and clamping bar", cutout=False),
    "vl-vg-control": R("04_w1600-13.webp", "Touchscreen CNC control of the V-grooving machine", cutout=False),
    "vl-vg-control-2": R("03_w1600-26.webp", "Control pendant with the CNC screen and push buttons", cutout=False),
    "vl-vg-ruler": R("05_w1600-1-1.webp", "Scale along the clamping bar for positioning the sheet", cutout=False),
    "vl-vg-parts": R("%E6%A0%B7%E6%9C%BA02_w1600-1.webp", "Grooved and bent stainless sample — zero-radius corner", cutout=False),
    "vl-vg-parts-2": R("%E6%A0%B7%E6%9C%BA03_w1600-1.webp", "Octagonal column bent from a V-grooved sheet", cutout=False),
    # ---------------------------------------------------------------- panel benders (PB-M, PB-A)
    # PB-M = press-arm type (the tall cabinet with the swinging press arm, the supplier's "P" render); PB-A = automatic tool
    # change (the machine with the tool-magazine columns on top, the "PC" render) — the supplier's file names are the other
    # way round, which is how the two were swapped at first (fixed Oct 2026).
    "vl-pbm-1": R("pb-p_w1600.webp", "NovoTech PB-M press-arm CNC panel bender — the press arm feeds and turns the blank, 63 – 165″ bend widths", boxes=[(305, 270, 370, 330), (770, 160, 845, 235)]),
    "vl-pbm-bend": R("01_w1600-5.webp", "PB-M bending unit forming a flange — upper and lower blades and the blank-holder", cutout=False),
    "vl-pbm-holder": R("03_w1600-2.webp", "Blank-holder and bending blade of the PB-M over the ball-transfer table", cutout=False),
    "vl-pbm-bending": R("%E6%8A%98%E5%BC%AF_w1600.webp", "PB-M press arm holding the blank in the bending unit", cutout=False),
    "vl-pbm-profiles": R("06_w1600-3.webp", "Profiles, hems and channels bent on the PB-M", cutout=False),
    "vl-pba-1": R("PB-M-16.9_w1600.webp", "NovoTech PB-A CNC panel bender with automatic tool change — tool magazine on top, 98″ bend width", boxes=[(455, 205, 545, 260)], cutout=True),
    "vl-pba-head": R("%E5%AE%9A%E8%BD%B4_w1600-1.webp", "Automatic tool changer of the PB-A placing a tool segment", cutout=False),
    "vl-pb-robot-cell": R("%E5%9C%B0%E6%8E%A5_w1600.webp", "PB-A panel bender loaded and unloaded by two robots", boxes=[(510, 150, 605, 210)], crop=(0, 60, 1600, 1065), cutout=False),
    "vl-pb-operator": R("05_w1600-23.webp", "Operator at the tool magazine of the automatic tool-change panel bender", boxes=[(920, 170, 1080, 245)], cutout=False),
    "vl-pb-unit": R("01_w1600-32.webp", "Bending unit — upper and lower blades, blank-holder and the sheet manipulator", cutout=False),
    "vl-pb-tools": R("%E7%BB%B4%E6%8A%A4_w1600_2.webp", "Automatic tool-change magazine of the PB-A", cutout=False),
    "vl-pb-blades": R("02_w1600-4.webp", "Bending blades forming a flange upward", cutout=False),
    "vl-pb-frame": R("05_w1600-5.webp", "High-grade cast body of the PB-M panel bender", cutout=False),
    "vl-pb-tool-diagram": R("26-28_w1600-1.webp", "Tool-change diagram of the PB-A bending unit", cutout=False),
}


def white_alpha(im, tol=14):
    """Alpha channel for a render on an opaque white background: flood-fill the near-white background from the border
    (OpenCV), the rest of the picture is the machine.  Soft shadows on the floor are near-white and go with the
    background, which is what the site rule wants (only the machine in a cut-out)."""
    import cv2
    rgb = np.asarray(im.convert("RGB"))
    h, w = rgb.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    flags = 4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8)
    work = rgb.copy()
    for x, y in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (0, h // 2), (w - 1, h // 2), (w // 2, h - 1)]:
        if (255 - rgb[y, x].astype(int)).max() <= tol * 2:
            cv2.floodFill(work, mask, (x, y), (0, 0, 0), (tol,) * 3, (tol,) * 3, flags)
    bg = mask[1:-1, 1:-1] > 0
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.8)
    out = im.convert("RGBA")
    out.putalpha(Image.fromarray(alpha))
    return out


def process(key, check_only=False):
    p = PHOTOS[key]
    im = Image.open(p["src"])
    if p.get("crop"):
        im = im.crop(p["crop"])
    has_alpha = im.mode in ("RGBA", "LA", "P") and (im.mode != "P" or "transparency" in im.info)
    im = im.convert("RGBA") if has_alpha else im.convert("RGB")
    if has_alpha and (np.asarray(im.getchannel("A")) < 128).mean() < 0.005:   # WebP alpha noise, not a real cut-out
        has_alpha = False
        im = im.convert("RGB")
    boxes = [(x0, y0, x1, y1, A) for x0, y0, x1, y1 in p.get("boxes", [])]
    if check_only:
        d = ImageDraw.Draw(im)
        for x0, y0, x1, y1, _ in boxes:
            d.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=3)
        im.convert("RGB").save(WORK + f"check-{key}.jpg", quality=80)
        print(f"{key:20s} {im.size} alpha={has_alpha} boxes={boxes}")
        return
    if boxes:
        im = delogo(im, boxes)
    if p.get("white") and not has_alpha:
        im = white_alpha(im)
        has_alpha = True
    s = min(1.0, MAX_SIDE / max(im.size))
    if s < 1:
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.startswith(key + "."):
            os.remove(os.path.join(OUT, old))
    if has_alpha:
        out = os.path.join(OUT, key + ".png")
        im.save(out, optimize=True)
    else:
        out = os.path.join(OUT, key + ".jpg")
        im.convert("RGB").save(out, quality=92)
    print(f"{key:20s} {im.size} boxes={len(boxes)} -> {os.path.basename(out)}")


def export_kind(key):
    """(ext, cutout) for image_map: alpha PNGs are used as they are; photos stay photos unless cutout=True."""
    p = PHOTOS[key]
    f = [x for x in os.listdir(OUT) if x.startswith(key + ".")]
    ext = os.path.splitext(f[0])[1] if f else ".jpg"
    cut = p.get("cutout")
    if cut is None:
        cut = ext != ".png" and not p["src"].startswith(HI)
    return ext, bool(cut) and ext != ".png"


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keys = args or list(PHOTOS)
    for k in keys:
        process(k, check_only="--check" in sys.argv)
