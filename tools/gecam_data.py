#!/usr/bin/env python3
"""Gecam (GECAM srl, Vicofertile, Parma, Italy) deburring, edge rounding, brush, corner grinding and corner welding machines, and
the Eurofintec pipe finishing machines Gecam builds (Gecam took over Eurofintec in 2005; its belt and pipe machines carry the
Eurofintec name) — sold under their own brands.

Sources: the 2026 Gecam catalogue (Catalogo_Gecam_EN_26.pdf) for every deburring machine in it; gecam.com (Oct 25) for the GT13,
the corner grinders' belt speeds, rollers and weights, the special corner grinders and what the catalogues leave out (feed
speeds of the pipe machines, weights, motor details); the metal-box brochure (metal_box_deburring_and_grinding_machine.pdf) for
the CWS 200/300, 135, 136 and 131; the Eurofintec catalogue (pipe_and_sheet_metal_deburing_polishing_and_grinding_machines_
GECAM_EUROFINTEC.pdf) for the pipe machines.  Where gecam.com differs from a catalogue (older G65 / G135 / GE30 figures on the
site, 141 Ø10 – 76 mm, 144 Ø10 – 150 mm, CWS welding speed 0 – 20 mm/s) the catalogue figure is used.  Only the pipe polishing,
finishing and sanding machines of the Eurofintec catalogue are on the site; its ordinary belt grinders are not.

Shown as imperial (metric); lengths to the nearest 1/16″ (1/32″ below 1/4″), sheet below 1/8″ as decimal inch.
"""
from fractions import Fraction

GECAM, EURO = "gecam", "eurofintec"
P_HUB = "sheet-metal-plate-deburring-edge-rounding-finishing-grinding"
P_SHEET = "sheet-metal-deburring-machines"
P_EDGE = "edge-rounding-deslagging-machines"
P_BRUSH = "brush-deburring-machines"
P_CORNER = "corner-grinding-machines"
P_PIPE = "pipe-sanding-polishing-machines"
P_WELD = "corner-welding-machines"


def vids(*ids_titles):
    from sahinler_lib import vids as _vids      # NovoTech's own channel only
    return _vids(*ids_titles)


# ------------------------------------------------------------------------------------------------ units
def inch(mm):
    """nearest 1/16″ (1/32″ under 1/4″) as a mixed fraction: 1-3/8″"""
    x = mm / 25.4
    den = 32 if x < 0.25 else 16
    f = Fraction(round(x * den), den)
    whole, rest = divmod(f.numerator, f.denominator)
    if rest == 0:
        return f"{whole}″"
    frac = f"{rest}/{f.denominator}"
    return f"{whole}-{frac}″" if whole else f"{frac}″"


def thin(mm):
    """sheet: decimal inch below 1/8″, fractions above"""
    return f"{mm / 25.4:.3f}″".replace("0.", ".", 1) if mm < 3 else inch(mm)


def n(v):
    return f"{v:,g}"


def one(a):
    return f"{inch(a)} ({n(a)} mm)"


def dia(a):
    return f"Ø{inch(a)} ({n(a)} mm)"


def dia_rng(a, b):
    return f"Ø{inch(a)} – {inch(b)} ({n(a)} – {n(b)} mm)"


def thick(a, b):
    return f"{thin(a)} – {thin(b)} ({n(a)} – {n(b)} mm)"


def size(a, b):
    """a × b, e.g. belt width × length"""
    return f"{inch(a)[:-1]} × {inch(b)} ({n(a)} × {n(b)} mm)"


def dims(l, w, h):
    return f"{l / 25.4:.0f} × {w / 25.4:.0f} × {h / 25.4:.0f}″ ({n(l)} × {n(w)} × {n(h)} mm)"


def ftmin(v):
    x = v * 3.28084
    return f"{x:.1f}" if x < 15 else f"{x:.0f}"


def feed(a, b):
    return f"{ftmin(a)} – {ftmin(b)} ft/min ({n(a)} – {n(b)} m/min)"


def cfm(m3h):
    return f"{round(m3h * 0.588578):,} CFM ({m3h:,} m³/h)"


def fpm(ms):
    return f"{int(ms * 196.8504 + 0.5):,}"


def belt_speed(*ms):
    return " / ".join(fpm(v) for v in ms) + f" ft/min ({' / '.join(n(v) for v in ms)} m/s)"


def hp(*kw):
    return " / ".join(f"{k / 0.7457:.1f}".rstrip("0").rstrip(".") for k in kw) + f" HP ({' / '.join(n(k) for k in kw)} kW)"


def lb(kg, approx=False):
    return f"{'from ' if approx else ''}{round(kg * 2.20462):,} lb ({kg:,} kg)"


def row(label, cells, key=False, sub=""):
    return {"label": label, "sub": sub, "cells": cells, "key": key}


def table(title, sub, models, rows):
    return {"title": title, "sub": sub, "models": models, "rows": rows}


GK = ["capacity", "thickness", "feed", "tools", "weight"]
NOTE = ("Metric values in brackets are the manufacturer's figures; imperial values are converted and rounded. Weights are approximate "
        "and depend on the working groups fitted. Dimensions are overall L × W × H.")


def spec(tbl, glance, note=NOTE):
    """glance: {model: [capacity, thickness, feed, tools, weight]}"""
    return {"kind": "table", "tables": [tbl], "models": [{"name": m, "glance": glance[m]} for m in tbl["models"]],
            "glance_keys": GK, "caps": {}, "note": note}


VOLT = "CSA-approved electrical panel; 600 V 3-phase with transformer (208 / 240 / 480 V on request)"
VOLT_OPT = "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"
WIDE = "wide"

# ================================================================================================ sheet metal deburring
T_G15_G30 = table("G15 · G30", "Compact deburring machines", ["G15", "G30"], [
    row("Working width", [one(150), one(300)], True),
    row("Part thickness", [thick(1, 105), thick(0.5, 120)], True, "min – max"),
    row("Abrasive belt", [size(150, 2000), size(320, 1900)], False, "width × length"),
    row("Brushes", [f"Ø{inch(200)} (200 mm), single row (T)", f"Ø{inch(115)} (115 mm), double row of 4 (X)"]),
    row("Feed speed", [feed(1, 4), feed(1, 4)], True),
    row("Working groups", ["R · T", "R · B · b · X"], True, "configurable"),
    row("Grit set", ["—", "Manual"]),
    row("Suction hood", ["—", dia(200)]),
    row("Dust extraction required", [cfm(2000), cfm(2000)]),
    row("Dimensions L × W × H", [dims(1774, 853, 1929), dims(620, 2134, 2050)]),
    row("Weight", [lb(430, True), lb(540, True)], True)])

T_G65_G135 = table("G65 · G135", "Wide-belt deburring machines", ["G65", "G135"], [
    row("Working width", [one(650), one(1350)], True),
    row("Part thickness", [thick(0.5, 120), thick(0.5, 120)], True, "min – max"),
    row("Abrasive belt", [size(660, 2200), size(1370, 2200)], False, "width × length"),
    row("Belt contact roller", [dia(190), dia(180)], False, "55 Shore rubber"),
    row("Top brushes (X)", [f"8 × Ø{inch(115)} (115 mm)", f"20 × Ø{inch(115)} (115 mm)"], False, "double row"),
    row("Feed speed", [feed(0.6, 6), feed(0.6, 6)], True),
    row("Working groups", ["R · X · B · B4 · b", "R · X · B · b"], True, "configurable"),
    row("Touch screen · electronic grit set · variable-speed belt", ["Standard", "Standard"]),
    row("Suction hoods", [dia(150), dia(150)]),
    row("Dust extraction required", [cfm(4000), cfm(6000)]),
    row("Dimensions L × W × H", [dims(1176, 2137, 2050), dims(1876, 2137, 2070)]),
    row("Weight", [lb(1700, True), lb(1800, True)], True)])

T_GM = table("GM65 · GM110", "Single-belt deburring and satin finishing machines", ["GM65", "GM110"], [
    row("Working width", [one(650), one(1100)], True),
    row("Part thickness", [thick(0.5, 120), thick(0.5, 120)], True, "min – max"),
    row("Abrasive belt", [size(670, 2200), size(1120, 1524)], False, "width × length"),
    row("Belt contact roller", [dia(190), dia(190)], False, "55 Shore rubber"),
    row("Feed speed", [feed(0.6, 6), feed(1, 4)], True),
    row("Working group", ["R", "R"], True, "abrasive belt"),
    row("Suction hood", [dia(150), dia(150)]),
    row("Dust extraction required", [cfm(2000), cfm(2000)]),
    row("Dimensions L × W × H", [dims(980, 1386, 2000), dims(1600, 1386, 1990)]),
    row("Weight", [lb(590, True), lb(800, True)], True)])

T_WET = table("G30 WET · G65/135 WET", "Wet deburring machines", ["G30 WET", "G65/135 WET"], [
    row("Working width", [one(300), one(1300)], True),
    row("Part thickness", [f"to {one(140)}", thick(0.8, 140)], True),
    row("Abrasive belt", [size(320, 1900), size(1320, 2200)], False, "width × length"),
    row("Feed speed", [feed(5, 10), feed(0.5, 10)], True),
    row("Working groups", ["Up to 2 of R · T · B", "R · T · B · b"], True, "configurable"),
    row("Water", ["Sprayers at each tool · external sludge tank", "Sprayers at each tool · external sludge tank"]),
    row("Working height", [one(900), one(900)], False, "fixed bench"),
    row("Dimensions L × W × H", [dims(1430, 860, 2100), dims(2300, 1600, 2380)]),
    row("Weight", [lb(660, True), lb(4000)], True)])

# ================================================================================================ edge rounding & deslagging
T_RB8 = table("G135RB8", "Deburring and edge rounding machine", ["G135RB8"], [
    row("Working width", [one(1350)], True),
    row("Part thickness", [thick(0.5, 120)], True, "min – max"),
    row("Edge radius", ["to 5/64″ (2 mm)"], True, "inside holes too"),
    row("Abrasive belt", [size(1370, 2200)], False, "width × length"),
    row("Carousel brushes", [f"8 × Ø{inch(300)[:-1]} × {inch(532)} (300 × 532 mm)"], False, "B group"),
    row("Feed speed", [feed(0.2, 2)], True),
    row("Working groups", ["R · X · B (8-brush carousel)"], True, "configurable"),
    row("Touch screen · electronic grit set · variable-speed belt", ["Standard"]),
    row("Suction hoods", [dia(150)]),
    row("Dust extraction required", [cfm(6000)]),
    row("Dimensions L × W × H", [dims(2177, 4277, 2235)]),
    row("Weight", [lb(4190, True)], True)])

T_GT = table("GT06 · GT13", "Double-sided edge rounding machines", ["GT06", "GT13"], [
    row("Working width", [one(600), one(1300)], True),
    row("Part thickness", [thick(0.5, 80), thick(0.5, 90)], True, "min – max"),
    row("Groups above and below the part", ["2 transverse abrasive belts (R) + 4 strip-brush tracks (C)", "2 strip-brush belts (C), one above and one below, 75 brushes each"], True),
    row("Abrasive belts", [size(50, 2500), "—"], False, "width × length"),
    row("Strip brushes", [size(66, 32), size(60, 50)]),
    row("Brush pressure", ["0 – 1-3/8″ (0 – 35 mm), motorized, each group", "0 – 1-3/8″ (0 – 35 mm), motorized, each group"]),
    row("Feed speed", [feed(0.7, 7), feed(0.7, 6)], True, "motorized rollers"),
    row("Suction hood", [dia(150), dia(180)]),
    row("Dust extraction required", [cfm(4000), cfm(4000)]),
    row("Dimensions L × W × H", [dims(1170, 1676, 2096), dims(2550, 1250, 1950)]),
    row("Weight", [lb(2000, True), lb(2200, True)], True)])

T_DCC = table("G65DCC", "Deslagging and edge rounding machine", ["G65DCC"], [
    row("Working width", [one(600)], True),
    row("Part thickness", [thick(10, 120)], True, "min – max"),
    row("Abrasive belt (D)", [size(680, 1500)], False, "width × length"),
    row("D belt roller", [f"{dia(420)}, 20 Shore, pneumatic pressure"]),
    row("Strip brushes (C)", [f"82 on two transverse belts, {size(66, 52)}"], False, "reverse rotation, independent motors"),
    row("Feed speed", [feed(0.7, 7)], True),
    row("Working groups", ["D · C"], True),
    row("Touch screen · magnetic table", ["Standard"]),
    row("Suction hoods", [dia(150)]),
    row("Dust extraction required", [cfm(4000)]),
    row("Dimensions L × W × H", [dims(1900, 1776, 2130)]),
    row("Weight", [lb(1520, True)], True)])

# ================================================================================================ brush deburring & benches
T_CUB = table("CUB 30 · CUB 65BB · CUB 30B1B2", "Brush deburring machines", ["CUB 30", "CUB 65BB", "CUB 30B1B2"], [
    row("Working width", [one(300), one(650), one(300)], True),
    row("Part thickness", [thick(0.5, 250), thick(0.5, 120), thick(0.5, 250)], True, "min – max"),
    row("Brush Ø", [dia(180), dia(200), dia(180)], True, "cylindrical"),
    row("Feed speed", [feed(1, 7), feed(1, 7), feed(1, 7)], True, "variable"),
    row("Min. part length", [one(100), one(100), one(100)]),
    row("Dimensions L × W × H", [dims(1120, 1068, 1360), dims(1220, 1700, 1400), dims(1150, 750, 1200)]),
    row("Weight", [lb(385), lb(700), lb(450)], True)])

T_EASY = table("EASY T", "Brushing workstation", ["EASY T"], [
    row("Work table", [size(800, 1300)], True),
    row("Working height", [one(945)]),
    row("Vacuum area", [size(250, 350)]),
    row("Max. part thickness", [one(150)], True),
    row("Top brush (T)", [f"{dia(150)}, quick release"], True, "2 tools on a 180° tilting arm"),
    row("Motor", [hp(0.75)], True)])

T_GCB = table("GCB 25 · GCB 30 · GCB 40", "Double crossed-belt deburring benches", ["GCB 25", "GCB 30", "GCB 40"], [
    row("Work table", [size(2500, 800), size(3000, 800), size(4000, 800)], True),
    row("Abrasive belts", [size(120, 8000), size(120, 9000), size(120, 10935)], True, "2 crossed belts"),
    row("Table vertical stroke (Z)", [one(600)] * 3),
    row("Max. part weight on the table", [lb(100)] * 3),
    row("Max. part weight on the clamping system", [lb(8)] * 3),
    row("Max. part weight on the manipulator", [lb(37)] * 3, False, "optional"),
    row("Dimensions L × W × H", [dims(1000, 3750, 2200)] * 3),
    row("Weight", [lb(790, True)] * 3, True)])

# ================================================================================================ corner grinders
T_135 = table("135", "Automatic corner grinder", ["135"], [
    row("Max. edge length", ["31-1/2″ or 59-1/16″ (800 or 1,500 mm)"], True, "two base lengths"),
    row("Grinding heads", ["1 · 2 on the two-head version"], True),
    row("Abrasive belt", [size(150, 2000)], False, "width × length"),
    row("Belt speed", [belt_speed(24, 12)], False, "two speeds"),
    row("Contact rollers", [size(50, 150)]),
    row("Head travel", ["Automatic, speed by inverter"], True),
    row("Clamping", ["Pneumatic"]),
    row("Motor", [hp(3)]),
    row("Dimensions L × W × H", [dims(1850, 1600, 1500)], False, "one head"),
    row("Weight", [lb(480, True)], True)])

T_131 = table("131", "Hand-fed corner grinder", ["131"], [
    row("Max. corner height", [f"{one(150)}"], True),
    row("Work table", [size(600, 250)], True),
    row("Table adjustment", ["Height and inclination by handwheel · squaring guides"]),
    row("Corner radius", ["3/64″ – 3/8″ (R1 – R10 mm) or sharp"], True),
    row("Abrasive belt", [size(150, 2000)], False, "width × length"),
    row("Belt speed", [belt_speed(24, 12)], False, "two speeds"),
    row("Fork rollers", [size(50, 150)]),
    row("Motor", [hp(2.3, 1.5)], True, "two speeds"),
    row("Dimensions L × W × H", [dims(700, 1400, 1500)]),
    row("Weight", [lb(120)], True)])

T_136 = table("136", "Hand-fed corner grinder", ["136"], [
    row("Max. corner height", ["7-7/8″ or 11-13/16″ (200 / 300 mm) · 19-11/16″ (500 mm) on request"], True),
    row("Part depth", ["3-1/8″ – 19-11/16″ (80 – 500 mm)"]),
    row("Work table", [size(600, 400)], True),
    row("Table adjustment", ["Prismatic guide"]),
    row("Corner radius", ["3/64″ – 3/8″ (R1 – R10 mm) or sharp"], True),
    row("Abrasive belt", [size(150, 2000)], False, "width × length"),
    row("Belt speed", [belt_speed(24, 12)], False, "two speeds"),
    row("Fork rollers", [size(50, 150)]),
    row("Motor", [hp(2.25, 1.5)], True, "two speeds"),
    row("Dimensions L × W × H", [dims(1006, 1200, 1130)]),
    row("Weight", [lb(160)], True)])

T_SPECIAL = table("Special corner grinders", "PLC-controlled corner grinders for series work",
                  ["Upper-corner grinder", "Six-head grinder", "Tube-frame grinder"], [
    row("Workpiece", ["Boxes, working width 7-7/8″ / 23-5/8″ (200 / 600 mm)", f"Boxes up to {one(150)} high",
                      f"Square tube {inch(20)} – {inch(80)} (20 – 80 mm) · frames from {one(450)}"], True),
    row("Grinding heads", ["2, vertical, on the two top corners", "6: 4 lower in pairs at 90° + 2 upper", "4: 2 vertical + 2 horizontal"], True),
    row("Corners per cycle", ["2", "2, about 30 s per pair", "1 corner, 4 sides"]),
    row("Abrasive belt", [size(35, 1535), "—", size(150, 2000)], False, "width × length"),
    row("Belt speed", [belt_speed(24, 12), "—", belt_speed(25)]),
    row("Control", ["Touch-screen PLC: time and pressure", "PLC recipes", "Touch-screen PLC: time for each head"], True)])

# ================================================================================================ corner welders
T_CWS = table("CWS 200 · CWS 300", "Corner welding machines", ["CWS 200", "CWS 300"], [
    row("Max. corner height", [one(200), one(300)], True, "external copper unit"),
    row("Part size", ["3-15/16 × 3-15/16″ – 59-1/16 × 59-1/16″ (100 × 100 – 1,500 × 1,500 mm)"] * 2, True, "min – max"),
    row("Work table", [size(820, 820)] * 2),
    row("Welding speed", ["0 – 118 in/min (0 – 50 mm/s), variable"] * 2, True),
    row("Welding process", ["TIG or plasma"] * 2, True),
    row("Clamping", ["Pneumatic, from inside, on copper blocks"] * 2),
    row("Torch movement", ["Guided · 2-axis (X, Y) available"] * 2),
    row("Control", ["CNC touch screen, stored parameters"] * 2)])

# ================================================================================================ pipe (Eurofintec)
T_141_144 = table("141 · 144", "Orbital pipe sanders", ["141", "144"], [
    row("Tube Ø", [dia_rng(10, 80), dia_rng(15, 150)], True, "round and oval, straight and bent"),
    row("Abrasive belts", [f"2 × {size(20, 600)}", f"2 × {size(50, 1100)}"], True, "on an orbital wheel"),
    row("Belt speed", [f"{fpm(10)} – {fpm(25)} ft/min (10 – 25 m/s)"] * 2, False, "variable"),
    row("Motor", [hp(1.5), hp(3)], True),
    row("Dimensions L × W × H", [dims(620, 650, 1110), dims(1200, 650, 1250)]),
    row("Weight", [lb(185), lb(210)], True)])

T_128 = table("128 S · 128 SL", "Single-head centreless pipe and bar sanders", ["128 S", "128 SL"], [
    row("Bar and tube Ø", [dia_rng(5, 110), dia_rng(5, 150)], True),
    row("Grinding heads", ["1", "1"], True),
    row("Abrasive belt", [size(75, 2000), size(150, 2000)], True, "width × length"),
    row("Contact wheel", [size(200, 75), size(200, 150)], False, "Ø × width"),
    row("Belt speed", [belt_speed(15, 30)] * 2, False, "two speeds"),
    row("Part rotation", ["23 – 115 ft/min (7 – 35 m/min)"] * 2, False, "rubber wheel, variable"),
    row("Max. length without support", [one(1000), one(1000)]),
    row("Motor", [hp(3.3, 2.5), hp(3.3, 2.5)], True),
    row("Dimensions L × W × H", [dims(1500, 650, 1450), dims(1500, 700, 1600)]),
    row("Weight", [lb(140), "—"], True)])

T_128DL = table("128 DL", "Two-head centreless pipe and bar sander", ["128 DL"], [
    row("Bar and tube Ø", [dia_rng(10, 150)], True),
    row("Grinding heads", ["2, independent, in line"], True),
    row("Abrasive belt", [size(150, 2000)], True, "width × length, each head"),
    row("Contact wheel", [size(200, 150)], False, "Ø × width, each head"),
    row("Belt speed", [belt_speed(15, 30)], False, "two speeds"),
    row("Part rotation", ["33 – 164 ft/min (10 – 50 m/min)"], False, "rubber wheel, variable"),
    row("Work support", ["Prismatic, anti-friction lining, set by handwheel"]),
    row("Motor", [hp(6.5)], True),
    row("Dimensions L × W × H", [dims(1700, 1400, 1600)]),
    row("Weight", [lb(450)], True)])

T_228 = table("228", "Pipe sander for large pipe", ["228"], [
    row("Pipe and bar Ø", [dia_rng(10, 400)], True),
    row("Abrasive belt", [size(100, 4000)], True, "free belt, width × length"),
    row("Contact wheel", [f"{size(250, 100)}, pneumatic"], False, "Ø × width"),
    row("Feed speed", ["0 – 23 ft/min (0 – 7 m/min)"], True, "contrast roller"),
    row("Motor", [hp(3.2, 4)], True),
    row("Dimensions L × W × H", [dims(1380, 990, 2270)])])

T_728_143 = table("728 · 143", "Tube brushing and tube-end deburring machines", ["728", "143"], [
    row("Tube size", [f"Round {dia_rng(10, 150)}", f"Round {dia_rng(20, 120)} · square {inch(20)} – {inch(120)} (20 – 120 mm)"], True),
    row("Brush", [f"{dia(300)}, {one(100)} wide", f"Wire, {dia(250)}, {one(100)} wide"], True),
    row("Brush speed", ["275 – 825 rpm, 2-speed motor", "2 speeds · brush axis rotation 2 speeds"]),
    row("Work", ["Cleaning, satin finishing and polishing along the tube", "Tube ends cut at 90° and 45°, inside and outside in one cycle"]),
    row("Motor", [hp(2.5, 3.3), hp(3.3, 4.5)], True),
    row("Dimensions L × W × H", [dims(800, 1300, 1400), dims(700, 930, 1400)]),
    row("Weight", [lb(320), lb(370)], True)])

NOTE_PIPE = ("Tube capacities are outside diameters. Metric values in brackets are the manufacturer's figures; belt speeds are surface "
             "speeds. Dimensions are overall L × W × H.")
NOTE_CORNER = ("Belt speeds are surface speeds; the corner grinders run at two speeds, the higher for steel and the lower for stainless "
               "and aluminum. Metric values in brackets are the manufacturer's figures.")
NOTE_WELD = ("The CWS works with a TIG or plasma welding power source. Metric values in brackets are the manufacturer's figures.")
NOTE_SPECIAL = ("Special machines are configured for the part: send a drawing of the box or frame and the weld to be removed for a quote. "
                "Metric values in brackets are the manufacturer's figures.")


# ================================================================================================ families
def fam(fid, group, page, brand, name, short, models_label, summary, headline, features, optional, images, specs, videos=()):
    return dict(id=fid, group=group, page=page, brand=brand, name=name, short=short, models_label=models_label, summary=summary,
                headline=headline, features=features, optional=optional, images=images, specs=specs, videos=list(videos))


FAMILIES = [
    # ------------------------------------------------------------------------------------------ sheet metal deburring
    fam("gecam-g15-g30", "gc-belt", P_SHEET, GECAM,
        "G15 · G30 compact deburring machines, 5-7/8″ and 11-13/16″ wide", "G15 · G30", "G15 · G30 · 2 models",
        "The way into belt deburring for laser, punching and plasma shops: an abrasive belt on a rubber contact roller takes the burr "
        "off, the brushes behind it round the edges and leave an even satin finish, and the conveyor carries the parts through. The "
        "G15 is the smallest Gecam — 5-7/8″ wide, a belt unit and a row of rotating, oscillating top brushes, for small parts up to "
        "4-1/8″ thick. The G30 takes parts 11-13/16″ wide and .020″ to 4-3/4″ thick with the belt (R), cylindrical Scotch-Brite brush "
        "(B), external brush (b) and double-row top brush (X) groups in the combination the parts need.",
        "Working width 5-7/8″ and 11-13/16″ · parts .020″ – 4-3/4″ · belt and brush groups",
        ["Abrasive belt unit (R) on a 55 Shore rubberized contact roller with automatic belt centering",
         "G15: single row of rotating and oscillating top brushes Ø7-7/8″ (T) — deburring, satin finish and edge rounding in one pass",
         "G30: belt (R), cylindrical Scotch-Brite brush (B), external brush (b) and a double row of four top brushes Ø4-1/2″ (X), configured to your parts",
         "Conveyor feed 3.3 – 13.1 ft/min (1 – 4 m/min), rubberized pressure rollers before and after each group",
         "Manual grit set on the G30: the bench height compensates for the belt thickness",
         "Dust extraction at each group; 1,177 CFM (2,000 m³/h) required",
         VOLT],
        ["Additional infeed and outfeed rollers", "Variable speed for each working group (G30)", "Conveyor belt cleaning brush (G30)",
         "Touch screen (G30)", "Vacuum table (G30)", VOLT_OPT],
        ["gc-g15", "gc-g30", "gc-g15-infeed", "gc-g15-brushes", "gc-g30-belts", "gc-g30-rb", "gc-g30-panel", "gc-g30-rollers",
         "gc-g30-conveyor", "gc-g30-sample", "gc-sample-r"],
        spec(T_G15_G30, {"G15": ["5-7/8″ wide", ".039″ – 4-1/8″", "3.3 – 13.1 ft/min", "R · T", "948 lb"],
                         "G30": ["11-13/16″ wide", ".020″ – 4-3/4″", "3.3 – 13.1 ft/min", "R · B · b · X", "1,190 lb"]})),
    fam("gecam-g65-g135", "gc-belt", P_SHEET, GECAM,
        "G65 · G135 wide-belt deburring machines, 25-9/16″ and 53-1/8″ wide", "G65 · G135", "G65 · G135 · 2 models",
        "The production deburring machines for laser, punching and plasma shops: up to four working groups in one pass — an "
        "abrasive belt for the burr, a double row of rotating, oscillating top brushes for the edges (8 on the G65, 20 on the G135), "
        "a cylindrical Scotch-Brite brush for the finish, and on the G65 a carousel of four abrasive brushes that rounds edges inside "
        "holes and slots. Touch screen, electronic grit set and variable belt speed are standard; the motorized table lifts on four "
        "synchronized screws and sets the part thickness to ±.004″ (0.1 mm). Parts .020″ to 4-3/4″ thick, fed at 2 to 20 ft/min.",
        "Working width 25-9/16″ and 53-1/8″ · parts .020″ – 4-3/4″ · up to 4 groups · touch screen",
        ["Configurable groups: R abrasive belt on a 55 Shore contact roller (Ø7-1/2″ G65, Ø7-1/16″ G135), X double row of top brushes "
         "Ø4-1/2″ (8 or 20), B cylindrical Scotch-Brite brush Ø7-7/8″, b external brush Ø5-7/8″, B4 four-brush carousel Ø9-13/16″ (G65)",
         "Touch screen, electronic grit set with stored belt types, and variable-speed belt group as standard",
         "Independent motor for every group; dust hood at each group, directly at the point of work",
         "Motorized table on 4 synchronized trapezoidal screws — part thickness set to ±.004″ (0.1 mm)",
         "Oil-proof natural rubber conveyor belt with automatic centering; rubberized pressure rollers before and after each group",
         "Diagnostic unit with display for alarms and faults",
         VOLT],
        ["Vacuum table", "Magnetic conveyor track for small steel parts", "Conveyor belt cleaning brush", "Higher-power motors",
         "Industry 4.0 connection", "Additional infeed / outfeed rollers", "Return conveyor bringing parts back to the operator", VOLT_OPT],
        ["gc-g65", "gc-g135", "gc-g65-glass", "gc-g65-rxb4", "gc-g65-rx", "gc-g135-rxr", "gc-x-brushes", "gc-touch", "gc-grit-set",
         "gc-g135-ext-brush", "gc-g135-long-table", "gc-belt-cleaning", "gc-g135-dust", "gc-sample-rx", "gc-sample-rxx", "gc-sample-rb",
         "gc-sample-oxide"],
        spec(T_G65_G135, {"G65": ["25-9/16″ wide", ".020″ – 4-3/4″", "2.0 – 20 ft/min", "R · X · B · B4 · b", "3,748 lb"],
                          "G135": ["53-1/8″ wide", ".020″ – 4-3/4″", "2.0 – 20 ft/min", "R · X · B · b", "3,968 lb"]})),
    fam("gecam-gm", "gc-belt", P_SHEET, GECAM,
        "GM65 · GM110 single-belt deburring and satin finishing machines, 25-9/16″ and 43-5/16″ wide", "GM65 · GM110",
        "GM65 · GM110 · 2 models",
        "One abrasive belt on a Ø7-1/2″ rubber contact roller and nothing more: the simplest and lowest-cost way to take the burrs off "
        "flat parts and give stainless steel, aluminum, brass and copper an even satin grain across a 25-9/16″ or 43-5/16″ width. "
        "Parts from .020″ to 4-3/4″ thick ride through on the conveyor at 2 to 20 ft/min (GM65) or 3.3 to 13.1 ft/min (GM110), and a "
        "magnetic conveyor track holds small steel parts down.",
        "Working width 25-9/16″ and 43-5/16″ · parts .020″ – 4-3/4″ · one abrasive belt",
        ["Abrasive belt unit (R) on a 55 Shore rubberized contact roller Ø7-1/2″ (190 mm) with automatic belt centering",
         "Deburring and satin finishing of flat parts in one pass",
         "Conveyor feed 2 – 20 ft/min (GM65) or 3.3 – 13.1 ft/min (GM110)",
         "Suction hood Ø5-7/8″; 1,177 CFM (2,000 m³/h) extraction required",
         VOLT],
        ["Magnetic conveyor track", VOLT_OPT],
        ["gc-gm65", "gc-gm110", "gc-gm-belt", "gc-sample-brass", "gc-sample-plate", "gc-sample-copper", "gc-sample-hairline", "gc-sample-satin"],
        spec(T_GM, {"GM65": ["25-9/16″ wide", ".020″ – 4-3/4″", "2.0 – 20 ft/min", "R", "1,301 lb"],
                    "GM110": ["43-5/16″ wide", ".020″ – 4-3/4″", "3.3 – 13.1 ft/min", "R", "1,764 lb"]})),
    fam("gecam-wet", "gc-wet", P_SHEET, GECAM,
        "G30 WET · G65/135 WET wet deburring machines, 11-13/16″ and 51-3/16″ wide", "G30 WET · G65/135 WET",
        "G30 WET · G65/135 WET · 2 models",
        "Deburring with water, for parts that would deform from the heat of dry grinding and for shops that want no grinding dust in "
        "the air: sprayers wet the belt and the brushes right at the cut, each managed separately, the sludge drains to an external "
        "collection tank, and on the G30 WET a drying group clears the parts at the exit. The G30 WET carries up to two groups on an "
        "11-13/16″ width; the G65/135 WET takes parts 51-3/16″ wide and .031″ to 5-1/2″ thick with belt, top-brush and cylindrical-"
        "brush groups. Fixed bench at 35-7/16″ working height; feed up to 33 ft/min.",
        "Working width 11-13/16″ and 51-3/16″ · parts to 5-1/2″ · water sprayed at every tool",
        ["Water sprayers directly on each working tool, managed independently",
         "External sludge collection tank; filter paper separates the sludge (G30 WET)",
         "Groups: R abrasive belt on a Ø4-15/16″ (125 mm) contact roller, T single row of top brushes Ø4-1/2″, B cylindrical Scotch-Brite brush Ø5-7/8″; b external brush on the G65/135 WET",
         "G30 WET: up to 2 groups, feed 16 – 33 ft/min (5 – 10 m/min), drying group at the exit",
         "G65/135 WET: feed 1.6 – 33 ft/min (0.5 – 10 m/min)",
         "Fixed bench at 35-7/16″ (900 mm) working height",
         VOLT],
        ["Touch screen", "Synthetic top brushes made for wet work", VOLT_OPT],
        ["gc-g30-wet", "gc-g65-wet", "gc-g30-wet-side", "gc-wet-rr", "gc-wet-rt", "gc-sample-rbb"],
        spec(T_WET, {"G30 WET": ["11-13/16″ wide", "to 5-1/2″", "16 – 33 ft/min", "R · T · B (2)", "1,455 lb"],
                     "G65/135 WET": ["51-3/16″ wide", ".031″ – 5-1/2″", "1.6 – 33 ft/min", "R · T · B · b", "8,818 lb"]})),
    # ------------------------------------------------------------------------------------------ edge rounding & deslagging
    fam("gecam-g135rb8", "gc-round", P_EDGE, GECAM,
        "G135RB8 edge rounding machine, 53-1/8″ wide, radius to 5/64″", "G135RB8", "G135RB8 · 8-brush carousel",
        "For laser-cut parts going to paint, powder coating or hands-on assembly: an abrasive belt takes off the burr, then a "
        "carousel of eight cylindrical abrasive brushes — each turning clockwise and counter-clockwise while the carousel rotates — "
        "works every edge from every direction, inside holes and slots too, up to a 5/64″ (2 mm) radius. The brushes are staggered, "
        "so no part of an edge escapes them, and paint covers the rounded edge instead of thinning out on a sharp one. Vacuum table "
        "for small parts, quick-release brush and belt change, touch-screen control of every group. 53-1/8″ wide, parts .020″ to "
        "4-3/4″.",
        "Working width 53-1/8″ · edge radius to 5/64″ (2 mm) · belt + 8-brush carousel",
        ["Abrasive belt (R) on a 55 Shore contact roller Ø4-15/16″ (125 mm), variable speed",
         "Carousel of 8 cylindrical abrasive brushes Ø11-13/16 × 20-15/16″ (300 × 532 mm) turning both ways, staggered so every edge is reached",
         "Edge radius up to 5/64″ (2 mm), inside holes too; also for coated and surface-treated sheet",
         "Double row of 8 top brushes Ø4-1/2″ (X) as a further configurable group",
         "Feed 0.7 – 6.6 ft/min (0.2 – 2 m/min); touch screen and electronic grit set standard",
         "Vacuum table; quick-release change of brushes and belt",
         VOLT],
        [VOLT_OPT],
        ["gc-g135rb8", "gc-rb8-carousel", "gc-rb8-belt", "gc-rb8-touch", "gc-rb8-before-after", "gc-rb8-plate", "gc-sample-r2", "gc-sample-rb8"],
        spec(T_RB8, {"G135RB8": ["53-1/8″ wide", ".020″ – 4-3/4″", "0.7 – 6.6 ft/min", "R · X · 8-brush carousel", "9,237 lb"]})),
    fam("gecam-gt", "gc-round", P_EDGE, GECAM,
        "GT06 · GT13 double-sided edge rounding machines, 23-5/8″ and 51-3/16″ wide", "GT06 · GT13", "GT06 · GT13 · 2 models",
        "Both faces of the part in one pass: cross belts carrying flexible strip brushes travel across the part above and below it, "
        "rounding every edge on both sides and inside the holes, while the faces themselves are not touched — a brushed, galvanized "
        "or pre-painted surface comes out as it went in. The part rides through on motorized rollers on a fixed bench. The GT06 adds "
        "two transverse abrasive belts with a pressure pad for heavier burrs (six groups, 23-5/8″ wide, parts .020″ to 3-1/8″); the "
        "GT13 runs two strip-brush belts of 75 brushes each, one above and one below the part (51-3/16″ wide, parts to 3-9/16″). Touch screen "
        "with stored programs on both.",
        "Working width 23-5/8″ and 51-3/16″ · both sides in one pass · edges rounded inside holes",
        ["Cross belts with strip brushes above and below the part: every edge rounded on both sides in one pass, inside holes too",
         "The faces are not worked, so previous surface treatments are kept",
         "GT06: 2 transverse abrasive belts with pressure pad and self-braking motor + 4 strip-brush tracks — 6 groups above and below",
         "GT13: 2 strip-brush belts, one above and one below, 75 brushes each (150 in all), 7.4 HP (5.5 kW) per group",
         "Motorized pressure setting of each group, 0 – 1-3/8″ (0 – 35 mm); independent motor for each group",
         "Fixed bench with motorized rollers; feed 2.3 – 23 ft/min (GT06) or 2.3 – 20 ft/min (GT13)",
         "Touch screen with stored work programs and alarm self-diagnosis",
         VOLT],
        [VOLT_OPT],
        ["gc-gt06", "gc-gt13", "gc-gt13-rcs", "gc-gt06-inside", "gc-gt-strips", "gc-gt-gauge", "gc-gt-touch", "gc-sample-holes"],
        spec(T_GT, {"GT06": ["23-5/8″ wide", ".020″ – 3-1/8″", "2.3 – 23 ft/min", "2 belts + 4 strip-brush tracks", "4,409 lb"],
                    "GT13": ["51-3/16″ wide", ".020″ – 3-9/16″", "2.3 – 20 ft/min", "2 strip-brush belts, 150 brushes", "4,850 lb"]})),
    fam("gecam-g65dcc", "gc-slag", P_EDGE, GECAM,
        "G65DCC deslagging and edge rounding machine, 23-5/8″ wide, parts 3/8″ – 4-3/4″", "G65DCC", "G65DCC · deslagging",
        "Plasma and oxy-fuel cutting leave dross welded to the bottom edge of thick parts, and grinding it off by hand is slow, noisy "
        "work. The G65DCC takes it off in one pass: a D belt on a large Ø16-9/16″ soft rubber roller (20 Shore), pressed on by a "
        "pneumatic cylinder, works only the edges and breaks the slag away, then 82 strip brushes on two transverse belts, turning in "
        "opposite directions, round the edges evenly. Magnetic table and touch screen standard; parts 3/8″ to 4-3/4″ "
        "thick, 23-5/8″ wide.",
        "Working width 23-5/8″ · parts 3/8″ – 4-3/4″ · slag off and edges rounded in one pass",
        ["D group: abrasive belt on a Ø16-9/16″ (420 mm) 20 Shore roller, pressed by a pneumatic cylinder; pneumatic belt tensioning and photocell belt centering",
         "Works the edges, not the face — the slag is broken off without grinding the surface",
         "C group: 82 strip brushes on two transverse belts with reverse rotation and independent motors, for an even edge radius",
         "Magnetic table and touch screen standard",
         "Feed 2.3 – 23 ft/min (0.7 – 7 m/min); suction hoods Ø5-7/8″, 2,354 CFM (4,000 m³/h) required",
         VOLT],
        [VOLT_OPT],
        ["gc-g65dcc", "gc-dcc-inside", "gc-dcc-touch", "gc-dcc-before", "gc-dcc-after", "gc-dcc-edge", "gc-dcc-thick"],
        spec(T_DCC, {"G65DCC": ["23-5/8″ wide", "3/8″ – 4-3/4″", "2.3 – 23 ft/min", "D belt · 82 strip brushes", "3,351 lb"]})),
    # ------------------------------------------------------------------------------------------ brush deburring & benches
    fam("gecam-cub", "gc-brush", P_BRUSH, GECAM,
        "CUB 30 · CUB 65BB · CUB 30B1B2 brush deburring machines, 11-13/16″ and 25-9/16″ wide", "CUB 30 · CUB 65BB · CUB 30B1B2",
        "CUB 30 · CUB 65BB · CUB 30B1B2 · 3 models",
        "A simpler, much lower-cost alternative to a wide-belt machine for deburring and satin-finishing flat parts: cylindrical "
        "brushes over a conveyor, each with its own motor and a motorized pressure setting, and the heads open on the operator side, "
        "so parts wider than the conveyor can still be brushed. Any cylindrical brush fits — Scotch-Brite for a satin finish, "
        "abrasive or wire for burrs. The CUB 30 and CUB 30B1B2 take parts 11-13/16″ wide and up to 9-13/16″ thick, the CUB 65BB "
        "parts 25-9/16″ wide and up to 4-3/4″, all from 3-15/16″ long.",
        "Working width 11-13/16″ and 25-9/16″ · parts to 9-13/16″ · conveyor 3.3 – 23 ft/min",
        ["Cylindrical brushes Ø7-1/16″ (CUB 30, CUB 30B1B2) or Ø7-7/8″ (CUB 65BB) — Scotch-Brite, abrasive or wire",
         "Motorized, independent pressure adjustment of each brush; brush heads positioned by handwheel",
         "Conveyor at variable speed, 3.3 – 23 ft/min (1 – 7 m/min); pressure rollers with independent adjustment",
         "Independent motors; heads open on the operator side for parts wider than the conveyor",
         "Parts from 3-15/16″ (100 mm) long",
         VOLT],
        ["Variable brush speed", "Brushes for other finishes", VOLT_OPT],
        ["gc-cub", "gc-cub-cat", "gc-cub-30", "gc-cub-compact", "gc-cub-brushes", "gc-cub-heads", "gc-sample-scotch"],
        spec(T_CUB, {"CUB 30": ["11-13/16″ wide", ".020″ – 9-13/16″", "3.3 – 23 ft/min", "Brushes Ø7-1/16″", "849 lb"],
                     "CUB 65BB": ["25-9/16″ wide", ".020″ – 4-3/4″", "3.3 – 23 ft/min", "Brushes Ø7-7/8″", "1,543 lb"],
                     "CUB 30B1B2": ["11-13/16″ wide", ".020″ – 9-13/16″", "3.3 – 23 ft/min", "Brushes Ø7-1/16″", "992 lb"]})),
    fam("gecam-easy-t", "gc-bench", P_BRUSH, GECAM,
        "EASY T brushing workstation with vacuum table, 31-1/2 × 51-3/16″, parts to 5-7/8″", "EASY T", "EASY T · workstation",
        "A bench for the parts a conveyor machine cannot take — heavy, thick, shaped or one-off: the vacuum table holds the part and "
        "the operator guides a Ø5-7/8″ top brush over it on a swinging arm, deburring, rounding the edges or satin-finishing. The arm "
        "carries two tools and tilts through 180° to change from one to the other; the tool is switched on from the handlebar, and "
        "the dust is drawn off inside the table. Parts up to 5-7/8″ thick on a 31-1/2 × 51-3/16″ table.",
        "Table 31-1/2 × 51-3/16″ · parts to 5-7/8″ · two tools on a 180° tilting arm",
        ["Two tools on a swinging arm that tilts through 180° for a quick change from one to the other",
         "Vacuum table, vacuum area 9-13/16 × 13-3/4″ (250 × 350 mm)",
         "Top brush Ø5-7/8″ (150 mm) with quick release; adjustable speed; any brush type for the material and finish",
         "1 HP (0.75 kW) motor; tool buttons on the handlebar",
         "Suction hood inside the table; working height 37-3/16″ (945 mm)",
         VOLT],
        ["Brushes for deburring, edge rounding and satin finishing", VOLT_OPT],
        ["gc-easy-t", "gc-easy-t-tools", "gc-easy-t-work", "gc-easy-t-operator", "gc-easy-t-brush"],
        spec(T_EASY, {"EASY T": ["31-1/2 × 51-3/16″ table", "to 5-7/8″", "—", "Top brush Ø5-7/8″ · 2 tools", "—"]})),
    fam("gecam-gcb", "gc-bench", P_BRUSH, GECAM,
        "GCB 25 · GCB 30 · GCB 40 double crossed-belt deburring benches, tables 98-7/16″ to 157-1/2″", "GCB 25 · GCB 30 · GCB 40",
        "GCB 25 · GCB 30 · GCB 40 · 3 models",
        "A manual station for large, heavy and awkward parts: two long abrasive belts cross over a motorized table, and the operator "
        "works the part against the belt — over a rubber roller, a shoe or a brush placed wherever along the belt the job needs — "
        "so long edges, profiles and shaped parts are deburred, satin-finished and rounded without a fixture. The belts are "
        "tensioned pneumatically and run at variable speed, a single independent brush (T) rounds edges, and a suction-cup "
        "manipulator holds shaped parts in any position. Tables 98-7/16″, 118-1/8″ or 157-1/2″ long.",
        "Tables 98-7/16″, 118-1/8″ and 157-1/2″ × 31-1/2″ · two crossed belts · manipulator for shaped parts",
        ["Double crossed abrasive belt 4-3/4″ (120 mm) wide with pneumatic tensioning, variable belt speed",
         "Rubber roller, shoe or brush accessory placed at any point along the belt",
         "Motorized table with 23-5/8″ (600 mm) vertical stroke; parts up to 220 lb (100 kg) on the table",
         "Single independent brush (T group) for edge rounding",
         "Control panel in front of the working area",
         VOLT],
        ["Suction-cup manipulator for shaped parts: 360° horizontal and 360° vertical rotation, 90° tilt, parts to 82 lb (37 kg)",
         "Accessory storage rack on guided wheels", VOLT_OPT],
        ["gc-gcb", "gc-gcb-cat", "gc-gcb-work", "gc-gcb-brush", "gc-gcb-vacuum"],
        spec(T_GCB, {"GCB 25": ["98-7/16 × 31-1/2″ table", "—", "—", "2 crossed belts 4-3/4″", "1,742 lb"],
                     "GCB 30": ["118-1/8 × 31-1/2″ table", "—", "—", "2 crossed belts 4-3/4″", "1,742 lb"],
                     "GCB 40": ["157-1/2 × 31-1/2″ table", "—", "—", "2 crossed belts 4-3/4″", "1,742 lb"]})),
    # ------------------------------------------------------------------------------------------ corner grinders
    fam("gecam-131", "gc-corner", P_CORNER, GECAM,
        "131 corner grinder for box and door welds, corners to 5-7/8″ high", "131", "131 · hand-fed",
        "The compact hand-fed corner grinder for welded boxes, cabinets, doors and trays: the abrasive belt runs over a fork with "
        "two rollers, and the operator slides the corner along it on the table. The fork oscillates both in angle and about its "
        "pivot, so it grinds the weld flush and leaves a radius from 3/64″ to 3/8″ (R1 – R10 mm) or a sharp corner. The "
        "23-5/8 × 9-13/16″ table is set in height and inclination by handwheel, with squaring guides adjusted by hand, for corners "
        "up to 5-7/8″ high. Two belt speeds: the higher for steel, the lower for stainless steel and aluminum.",
        "Corners to 5-7/8″ high · radius 3/64″ – 3/8″ or sharp · table adjustable in height and inclination",
        ["Fixed head with an oscillating two-roller fork: radius 3/64″ – 3/8″ (R1 – R10 mm) or a sharp corner",
         "Abrasive belt 5-7/8 × 78-3/4″ (150 × 2,000 mm) at two speeds, 4,724 / 2,362 ft/min (24 / 12 m/s)",
         "23-5/8 × 9-13/16″ (600 × 250 mm) work table, height and inclination set by handwheel",
         "Squaring guides adjusted by hand; corners up to 5-7/8″ (150 mm) high",
         "Dust hood; electrics in a sealed box",
         VOLT],
        ["Dust collector", VOLT_OPT],
        ["gc-131", "gc-131-table", "gc-131-head", "gc-box-corner"],
        spec(T_131, {"131": ["Corners to 5-7/8″ high", "—", "Hand-fed", "Belt 5-7/8″, oscillating fork", "265 lb"]}, NOTE_CORNER)),
    fam("gecam-136", "gc-corner", P_CORNER, GECAM,
        "136 corner grinder for box and cabinet welds, corners to 11-13/16″ high", "136", "136 · hand-fed",
        "The hand-fed corner grinder for taller boxes, cabinets and enclosures: the abrasive belt runs over a fork with two rollers, "
        "and the operator slides the corner along it on a 23-5/8 × 15-3/4″ table with a prismatic guide. The fork oscillates both "
        "in angle and about its pivot, so it grinds the weld flush and leaves a radius from 3/64″ to 3/8″ (R1 – R10 mm) or a sharp "
        "corner. Corners 7-7/8″ or 11-13/16″ high — 19-11/16″ on request — on parts 3-1/8″ to 19-11/16″ deep, and it also radiuses "
        "the edges of flat parts. Two belt speeds: the higher for steel, the lower for stainless steel and aluminum.",
        "Corners to 11-13/16″ high (19-11/16″ on request) · radius 3/64″ – 3/8″ or sharp · prismatic guide",
        ["Fixed head with an oscillating two-roller fork: radius 3/64″ – 3/8″ (R1 – R10 mm) or a sharp corner",
         "Abrasive belt 5-7/8 × 78-3/4″ (150 × 2,000 mm) at two speeds, 4,724 / 2,362 ft/min (24 / 12 m/s)",
         "23-5/8 × 15-3/4″ (600 × 400 mm) work table with prismatic guide",
         "Corners 7-7/8″ or 11-13/16″ (200 / 300 mm) high; parts 3-1/8″ – 19-11/16″ (80 – 500 mm) deep",
         "Also radiuses the edges of flat parts",
         "Dust hood; electrics in a sealed box",
         VOLT],
        ["Cyclone dust collector", "Version for corners up to 19-11/16″ (500 mm) high", VOLT_OPT],
        ["gc-136", "gc-136-box", "gc-136-head", "gc-box-corner"],
        spec(T_136, {"136": ["Corners to 11-13/16″ high", "—", "Hand-fed", "Belt 5-7/8″, oscillating fork", "353 lb"]}, NOTE_CORNER)),
    fam("gecam-135", "gc-corner", P_CORNER, GECAM,
        "135 automatic corner grinder for welded boxes, edges to 59″", "135", "135 · 1 or 2 heads",
        "Grinds the weld on the outside corner of a welded box or cabinet without the operator holding anything: the box is clamped "
        "pneumatically on a large support base, the belt head comes in on a pneumatic carriage and then travels the full length of "
        "the edge on recirculating-ball guides at an inverter-set speed, stops at the end and releases the part, so the operator "
        "turns it to the next edge and starts again without returning to zero. One head as standard, a two-head version for more "
        "output, and a PLUS version with vertical, horizontal and oscillating head movement for radiusing. Edges up to 31-1/2″ or 59″.",
        "Edges to 31-1/2″ or 59″ · automatic head travel · 1 or 2 heads",
        ["Automatic head travel along the edge; head speed variable by inverter",
         "Large base with table support for the part; pneumatic clamping",
         "Abrasive belt 5-7/8 × 78-3/4″ (150 × 2,000 mm) pressed on the weld by a pad with contact rollers",
         "Belt speed 4,724 / 2,362 ft/min (24 / 12 m/s); 4 HP (3 kW)",
         "Working pressure set by bringing the head closer to the part",
         "Push-button control as standard",
         VOLT],
        ["Touch-screen control", "Two-head version", "PLUS version: vertical, horizontal and oscillating head movement for radiusing (touch-screen models)", VOLT_OPT],
        ["gc-135", "gc-135-2h", "gc-135-head", "gc-135-pad", "gc-135-guides", "gc-135-touch", "gc-135-sample"],
        spec(T_135, {"135": ["Edges to 31-1/2″ or 59″", "—", "Automatic head travel", "1 or 2 belt heads", "1,058 lb"]}, NOTE_CORNER)),
    fam("gecam-corner-special", "gc-corner-special", P_CORNER, GECAM,
        "Upper-corner, six-head and tube-frame corner grinders, boxes to 23-5/8″, tube to 3-1/8″",
        "Special corner grinders", "Upper-corner · six-head · tube-frame",
        "For corner welds in series, Gecam builds grinders that run from a stored recipe — the operator places the part and starts "
        "it. The upper-corner grinder brings two vertical heads down on the two top corners of a box at once and presses the belt on "
        "the weld with pads; time and pressure are set on the touch screen by how much weld there is to remove. The six-head grinder "
        "cleans the outside edges of boxes up to 5-7/8″ high two corners at a time, about 30 seconds a pair. The four-head tube-frame "
        "grinder removes the welds on 90° corners of square-tube frames — table legs and frames from 3/4″ to 3-1/8″ tube — on all four "
        "sides in one cycle.",
        "Recipe-controlled corner grinding · boxes and 90° tube frames · built to the part",
        ["Upper-corner grinder: 2 heads with pads press a 1-3/8″ (35 mm) belt on both top corners at once; time and pressure set on the touch screen",
         "Six-head grinder: 4 lower heads in pairs at 90° with rubber pads and 2 upper heads with oscillating rubber rollers; the heads close in pneumatically and travel along the corner",
         "Tube-frame grinder: 2 mirrored vertical heads for top and bottom and 2 horizontal heads for the sides; pneumatic belt tension; side heads travel vertically to use the whole belt",
         "PLC recipes with the data of each part; dust drawn off at the point of work",
         VOLT],
        [VOLT_OPT],
        ["gc-upper-corner", "gc-six-head", "gc-tube-corner", "gc-upper-corner-panel", "gc-six-head-heads", "gc-six-head-pads",
         "gc-tube-corner-table", "gc-tube-corner-heads", "gc-corner-before", "gc-corner-after"],
        spec(T_SPECIAL, {"Upper-corner grinder": ["Boxes 7-7/8″ / 23-5/8″ wide", "—", "PLC-timed", "2 belt heads", "—"],
                         "Six-head grinder": ["Boxes to 5-7/8″ high", "—", "~30 s per 2 corners", "6 belt heads", "—"],
                         "Tube-frame grinder": ["Tube 3/4″ – 3-1/8″ square", "—", "4 sides per cycle", "4 belt heads", "—"]}, NOTE_SPECIAL)),
    # ------------------------------------------------------------------------------------------ corner welders
    fam("gecam-cws", "gc-weld", P_WELD, GECAM,
        "CWS 200 · CWS 300 corner welding machines for bent boxes, parts to 59 × 59″", "CWS 200 · CWS 300", "CWS 200 · CWS 300 · 2 models",
        "Welds the corners of bent boxes, cabinets, trays and enclosures in mild steel, stainless and aluminum with a TIG or plasma "
        "torch moved by the machine instead of by hand. The operator places the part with its corner against the external copper "
        "guide and presses the clamp button — a pneumatic cylinder anchors it from inside against copper blocks that hold the corner "
        "and draw the heat away — then presses start: the torch goes to the start point and welds the corner at the set speed. The "
        "parameters of each part are stored on the CNC touch screen. Corners 7-7/8″ high on the CWS 200 and 11-13/16″ on the CWS "
        "300, parts from 3-15/16 × 3-15/16″ to 59 × 59″; two-axis torch movement is available.",
        "Corners 7-7/8″ and 11-13/16″ high · parts 3-15/16″ – 59″ square · TIG or plasma · CNC touch screen",
        ["Guide system for the torch; welding speed variable 0 – 118 in/min (0 – 50 mm/s)",
         "Pneumatic clamping from inside against copper blocks: the corner is held in place and kept cool",
         "Copper group: external unit 7-7/8″ or 11-13/16″ (200 / 300 mm) high and an internal unit matched to the corner height",
         "CNC with touch screen; work and torch parameters stored for repeat parts",
         "Mild steel, stainless steel and aluminum; for a TIG or plasma welding power source",
         "Work table 32-5/16 × 32-5/16″ (820 × 820 mm)",
         VOLT],
        ["Two-axis (X, Y) torch movement", "Cooling unit for the copper blocks — recommended to avoid discoloration of the weld zone", VOLT_OPT],
        ["gc-cws", "gc-cws-welding", "gc-cws-copper", "gc-cws-stop", "gc-cws-touch", "gc-cws-bent", "gc-cws-welded", "gc-cws-boxes"],
        spec(T_CWS, {"CWS 200": ["Corners to 7-7/8″ high", "Parts to 59 × 59″", "0 – 118 in/min", "TIG or plasma torch", "—"],
                     "CWS 300": ["Corners to 11-13/16″ high", "Parts to 59 × 59″", "0 – 118 in/min", "TIG or plasma torch", "—"]}, NOTE_WELD)),
    # ------------------------------------------------------------------------------------------ pipe sanding & polishing (Eurofintec)
    fam("eurofintec-141-144", "ef-orbital", P_PIPE, EURO,
        "141 · 144 orbital pipe sanders for straight and bent tube, Ø3/8″ – 5-7/8″", "141 · 144", "141 · 144 · 2 models",
        "The tube passes through the head while two abrasive belts orbit around it, so round and oval tube — straight or bent — is "
        "ground, satin-finished or cleaned all round without the operator turning it. The tube only moves along its axis, which "
        "gives an even finish and spares the operator. Belt tension and centering are electronic, belt speed is variable. The compact "
        "141 takes tube from Ø3/8″ to Ø3-1/8″ — handrail, furniture and frame tube; the 144 Ø9/16″ to Ø5-7/8″. Feeding and extraction "
        "units are available, with reverse feed that brings the tube back for a second pass.",
        "Round and oval tube Ø3/8″ – 5-7/8″ · straight and bent · two orbiting belts",
        ["Two abrasive belts on an orbital wheel inside the head — the tube is worked all round without being turned",
         "Round and elliptical tube, straight and bent",
         "Electronic belt tensioning and centering",
         "Variable belt speed, 1,969 – 4,921 ft/min (10 – 25 m/s)",
         "141: 2 belts 13/16 × 23-5/8″ (20 × 600 mm), 2 HP (1.5 kW) · 144: 2 belts 1-15/16 × 43-5/16″ (50 × 1,100 mm), 4 HP (3 kW)",
         "Connection for a dust extractor at the point of work",
         VOLT],
        ["Automatic feeding and extraction units", "Reverse feed that returns the tube for a second pass", VOLT_OPT],
        ["ef-141", "ef-144", "ef-141-bend", "ef-141-small", "ef-144-feeder", "ef-144-panel"],
        spec(T_141_144, {"141": ["Tube Ø3/8″ – 3-1/8″", "—", "Hand or automatic feed", "2 orbiting belts 13/16″", "408 lb"],
                         "144": ["Tube Ø9/16″ – 5-7/8″", "—", "Hand or automatic feed", "2 orbiting belts 1-15/16″", "463 lb"]}, NOTE_PIPE)),
    fam("eurofintec-128", "ef-centreless", P_PIPE, EURO,
        "128 S · 128 SL single-head centreless pipe and bar sanders, Ø3/16″ – 5-7/8″", "128 S · 128 SL", "128 S · 128 SL · 2 models",
        "Single-head centreless belt grinders for satin-finishing and polishing round bar and tube: the part lies on a work rest and "
        "a grooved rubber wheel turns it against the abrasive belt while it is pushed through, so the whole surface is finished evenly "
        "along its length. The rubber wheel's speed is set for each diameter and the belt runs at two speeds. The 128 S takes Ø3/16″ "
        "to Ø4-5/16″ on a 2-15/16″ belt and the 128 SL Ø3/16″ to Ø5-7/8″ on a 5-7/8″ belt, both up to 39″ long without extra "
        "supports. Dry or wet.",
        "Round bar and tube Ø3/16″ – 5-7/8″ · centreless · single head · dry or wet",
        ["Centreless group with grooved rubber wheel; part rotation set electronically for the diameter, 15 – 75 rpm",
         "Two belt speeds: 2,953 / 5,906 ft/min (15 / 30 m/s); belt tensioning and centering",
         "128 S: abrasive belt 2-15/16 × 78-3/4″ (75 × 2,000 mm) for Ø3/16″ – 4-5/16″ · 128 SL: 5-7/8 × 78-3/4″ (150 × 2,000 mm) for Ø3/16″ – 5-7/8″",
         "Contact wheel Ø7-7/8″ (200 mm)",
         "Parts up to 39-3/8″ (1 m) long without support; extra support guides for longer parts",
         "Electrics in a sealed metal box",
         VOLT],
        ["Wet version with coolant on the belt", "Extra work support guides for long parts", "Contact wheels in other diameters", VOLT_OPT],
        ["ef-128sl", "ef-128-work", "ef-128-wheel", "ef-128-wet"],
        spec(T_128, {"128 S": ["Bar & tube Ø3/16″ – 4-5/16″", "—", "Rotation 23 – 115 ft/min", "1 belt 2-15/16″", "309 lb"],
                     "128 SL": ["Bar & tube Ø3/16″ – 5-7/8″", "—", "Rotation 23 – 115 ft/min", "1 belt 5-7/8″", "—"]}, NOTE_PIPE)),
    fam("eurofintec-128dl", "ef-centreless", P_PIPE, EURO,
        "128 DL two-head centreless pipe and bar sander, Ø3/8″ – 5-7/8″", "128 DL", "128 DL · 2 heads",
        "The two-head centreless sander for production finishing of round bar and tube: two independently controlled heads in line, "
        "so two grits — roughing and finishing, or two finishing steps — work in one pass. The part lies on a prismatic work support "
        "with an anti-friction lining, set by handwheel, and a grooved rubber wheel turns it against the belts while it is pushed "
        "through, so the whole surface is finished evenly along its length. Part rotation 20 – 100 rpm, set electronically for the "
        "diameter; two belt speeds. Bar and tube Ø3/8″ to Ø5-7/8″, dry or wet.",
        "Round bar and tube Ø3/8″ – 5-7/8″ · two heads in line · two grits in one pass · dry or wet",
        ["Two independently controlled heads in line, each with a 5-7/8 × 78-3/4″ (150 × 2,000 mm) belt: two grits in one pass",
         "Centreless group with grooved rubber wheel; part rotation set electronically for the diameter, 20 – 100 rpm",
         "Two belt speeds: 2,953 / 5,906 ft/min (15 / 30 m/s); belt tensioning and centering",
         "Contact wheels Ø7-7/8″ (200 mm)",
         "Prismatic work support with anti-friction lining, set by handwheel; 3 support accessories included",
         "Electrics in a sealed metal box",
         VOLT],
        ["Wet version with coolant on the belts", "Contact wheels in other diameters", VOLT_OPT],
        ["ef-128dl", "ef-128dl-heads", "ef-128dl-guide", "ef-128-wheel", "ef-128-wet"],
        spec(T_128DL, {"128 DL": ["Bar & tube Ø3/8″ – 5-7/8″", "—", "Rotation 33 – 164 ft/min", "2 belts 5-7/8″", "992 lb"]}, NOTE_PIPE)),
    fam("eurofintec-228", "ef-centreless", P_PIPE, EURO,
        "228 pipe sander for large pipe, Ø3/8″ – 15-3/4″", "228", "228 · pipe to Ø15-3/4″",
        "For pipe too big for a centreless machine: a 3-15/16″ free belt runs over two Vulkollan rollers on a compensated fork that "
        "follows any ovality of the pipe, while a contrast group with a grooved rubber roller — set to the diameter by handwheel — "
        "turns the pipe and carries it past at up to 23 ft/min. Pneumatic contact wheel, fully enclosed belt and a circular-grinding "
        "attachment; roller stands in line with the machine carry long pipe. Pipe and round bar from Ø3/8″ to Ø15-3/4″.",
        "Pipe Ø3/8″ – 15-3/4″ · 3-15/16 × 157-1/2″ free belt · feed 0 – 23 ft/min",
        ["Free abrasive belt 3-15/16 × 157-1/2″ (100 × 4,000 mm) on two Vulkollan rollers on a compensated fork",
         "Pneumatic contact wheel Ø9-13/16 × 3-15/16″ (250 × 100 mm) on bearings, for pipe up to Ø15-3/4″",
         "Contrast group with grooved rubber roller on a guide set by handwheel to the pipe diameter; feed 0 – 23 ft/min (0 – 7 m/min)",
         "Fully enclosed belt; circular-grinding attachment included",
         "4.3 / 5.4 HP (3.2 / 4 kW)",
         VOLT],
        ["Roller stands for long and heavy pipe", VOLT_OPT],
        ["ef-228", "ef-228-rollers", "ef-228-work", "ef-228-large"],
        spec(T_228, {"228": ["Pipe Ø3/8″ – 15-3/4″", "—", "0 – 23 ft/min", "Free belt 3-15/16″", "—"]}, NOTE_PIPE)),
    fam("eurofintec-728-143", "ef-brush", P_PIPE, EURO,
        "728 tube brushing machine and 143 tube-end deburring machine, Ø3/8″ – 5-7/8″", "728 · 143", "728 · 143 · 2 machines",
        "Two brush machines for the work around a tube shop's saw and polisher. The 728 brushes round tube: a Ø11-13/16″ brush on a "
        "two-speed, self-braking motor works the tube while a grooved rubber contrast roller — tilted to feed it and pneumatically "
        "compensated — carries it past, cleaning, satin-finishing or polishing tube from Ø3/8″ to Ø5-7/8″, with handwheel adjustment "
        "as the brush wears. The 143 deburrs the cut ends of stainless tube and profiles inside and outside in one cycle: a wire brush "
        "turns while its own axis rotates, changing direction so every edge is deburred evenly, on ends cut at 90° or 45° and on bent "
        "parts — round tube Ø13/16″ to Ø4-3/4″, square 13/16″ to 4-3/4″.",
        "728: tube Ø3/8″ – 5-7/8″ · 143: tube ends Ø13/16″ – 4-3/4″, round and square",
        ["728: brush Ø11-13/16 × 3-15/16″ (300 × 100 mm), 275 – 825 rpm; two-speed motor with electronic brake, V-belt drive",
         "728: contrast group with grooved rubber roller, tilt and diameter adjustment, pneumatic position compensation with adjustable pressure; steel work rest",
         "728: column base, extraction hood, electrics in a sealed box with inverter",
         "143: wire brush Ø9-13/16 × 3-15/16″ (250 × 100 mm); two brush speeds and two speeds of brush-axis rotation",
         "143: inside and outside of the tube end in one cycle; ends cut at 90° and 45°, bent parts too; entry with adjustable central prism",
         VOLT],
        ["Self-filtering dust extraction (728)", VOLT_OPT],
        ["ef-728", "ef-143", "ef-143-front", "ef-728-brush", "ef-728-adjust", "ef-728-pneumatic", "ef-728-contrast", "ef-143-brush", "ef-143-45"],
        spec(T_728_143, {"728": ["Tube Ø3/8″ – 5-7/8″", "—", "Contrast-roller feed", "Brush Ø11-13/16″", "705 lb"],
                         "143": ["Tube ends Ø13/16″ – 4-3/4″", "—", "Hand-fed", "Wire brush Ø9-13/16″", "816 lb"]}, NOTE_PIPE)),
]


# NovoTech's own videos of these machines (G3 = G30, G6 / G60 = G65 in Gecam's older names)
VIDEOS = {
    "gecam-g15-g30": [("DS_yO-WbtSQ", "G15 RTT — the little one"), ("-uEVrOpBn2s", "G30 (G3) RB dry deburring")],
    "gecam-g65-g135": [("P6clb5uvwzo", "G65 RXB4 deburring and finishing"), ("uQ-9CMccQIs", "G65 RXB4 — edge rounding with rotating brushes"),
                       ("brMbAFpqbOw", "G65 RXR deburring and edge rounding"), ("9Lprvh8Y438", "G65 (G60) RX deburring"),
                       ("1chAwVBSWWs", "G65 (G6) RTB deburring"), ("9gJt-anlXiE", "G65 (G6) BB Scotch-Brite polishing"),
                       ("pMdmrBLEAFc", "G135 RXR deburring and finishing"), ("vYP5gY1w1Ik", "G135 XX deburring"),
                       ("7ly2JRZL-Xc", "In-depth look at the G135 RXR")],
    "gecam-wet": [("n12yiYojRjI", "G30 WET"), ("jwnr8gK3ETg", "G30 (G3) WET deburring and finishing"), ("MgZDeNLR5KY", "G65 (G6) WET")],
    "gecam-g135rb8": [("v9s8r2TJT00", "G135 RB8 deburring and edge rounding"), ("nyTW0augaGo", "G135 RB rotary brushes for edge rounding"),
                      ("a9VgU3D0vok", "Rotary brush carousel rounding edges")],
    "gecam-gt": [("owfvMKRntJ8", "GT06 — edge rounding top and bottom"), ("7GM9LWGFoEs", "GT13 double-sided cross-belt edge rounding"),
                 ("snxpgxlhbu8", "GT13 CS double-sided deburring"), ("OeZjSsXzXas", "GT13 CB — oxide removal"),
                 ("q6RLOup6bN4", "GT13 RCS cross-belt deburring"), ("Kxy4IBRUBS4", "GT13 CSB brushing, rounding and oxide removal")],
    "gecam-g65dcc": [("iicuKk_mo58", "G65 (G6) DCC deslagging and edge rounding"), ("VpVDpUHtAOM", "GE65 RCC — belt and strip-brush groups")],
    "gecam-cub": [("GIHs5vp-zQE", "CUB 30 brushing and deburring"), ("MIgzM81gJQA", "CUB 30 BB — top and bottom brushing"),
                  ("TzeAYCddrUs", "CUB 30 BB brushing and finishing")],
    "gecam-easy-t": [("oIDa5QsHTG0", "EASY T deburring, grinding and polishing")],
    "gecam-gcb": [("8wLm7uOQRnA", "GCB 25 RR cross-belt deburring"), ("8Z8EFZOkpXI", "Double crossed belt on bent plate")],
    "gecam-135": [("tOxkUm2lGZo", "135 grinding box corners"), ("J6m2o9B1Ka4", "135 on a corner weld seam"),
                  ("ZzlXT-qjUOc", "135 two-head version"), ("TTCL4SnvtKI", "135 PLUS"), ("VPEpu74z84I", "135 corner seam grinding"),
                  ("7RM52FGLZag", "135 belt change")],
    "gecam-131": [("bDsDqFoJ5l4", "131 corner grinder"), ("cnQful7fLsI", "131 with oscillating head"),
                  ("XSrlMJ_lmME", "131 box weld seam sanding"), ("pRvYJVhLOkE", "131 on a stainless box"),
                  ("y0gMB7J6F_E", "131 box seam grinding"), ("7sG_9LqdVNM", "131 on a door corner"),
                  ("eEYp5xXPNZo", "How to adjust and operate the 131")],
    "gecam-136": [("lXGO65Ghwo0", "136 on an enclosure weld seam"), ("rrpQjvD7sEE", "136 weld seam grinding")],
    "gecam-corner-special": [("J5LT42sqaRw", "Six-head corner grinder"), ("QLv9H4YqNoc", "Automatic weld seam grinder for electrical panels"),
                             ("CK-pAsAkwrg", "Weld seam grinder for electrical panels"), ("YH0_0xBvYb4", "Special weld seam corner grinder")],
    "gecam-cws": [("31eDB7VrF6I", "CWS 200 / 300 one-axis corner welding"), ("x_qoKWRnEwA", "Two-axis corner welding"),
                  ("R48m8-Np9XU", "Automatic corner welding"), ("QTZDWAw4wu0", "Corner welding system at work")],
    "eurofintec-141-144": [("bBTOXVG-XkA", "141 pipe sander"), ("Ct6iF4KiDts", "141 small tube deburring and finishing"),
                           ("Ds_wymTW1Bs", "144 orbital pipe sander"), ("qsHhvHH5IOw", "144 pipe polishing"),
                           ("reRZfVQBCF8", "144 polishing aluminum tube")],
    "eurofintec-128": [("T8fy51DykIk", "128 S centreless pipe sander"), ("ESDnM4-hkYM", "128 S centreless pipe sanding"),
                       ("UwRy5zVRRk4", "128 SL pipe sanding"), ("KJX0iCI8bYY", "128 SL centreless tube sanding"),
                       ("I-LmPF3pKe4", "128 SL pipe sanding machine"), ("QWP5ysXOv7w", "128 SL centreless pipe polisher")],
    "eurofintec-128dl": [("f3f7-lNiEH0", "128 DL dry"), ("I27PlnO8OI8", "128 DL twin, wet"),
                         ("_jHJUG1jRWE", "128 DL centreless pipe sanders")],
    "eurofintec-228": [("RF_dHAi0IEE", "228 — pipe up to Ø15-3/4″")],
    "eurofintec-728-143": [("pCPlP3ZAuyw", "728 pipe polishing and brushing"), ("3-jRbQS-rs4", "143 tube-end deburring")],
}
for _f in FAMILIES:
    _f["videos"] = vids(*VIDEOS.get(_f["id"], ()))


def families(page=None):
    return [f for f in FAMILIES if page is None or f["page"] == page]
