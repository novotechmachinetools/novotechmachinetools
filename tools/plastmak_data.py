#!/usr/bin/env python3
"""Plastmak (Bursa, Turkey) aluminum and PVC window and door machinery — sold under its own brand.

Sources: the 2026 Plastmak catalogue (PLASTMAK_KATALOG_2026_K___K.pdf: metric figures from each page's symbol table,
cutting-capacity charts and dimension drawings), NovoTech's Plastmak catalogue (NovoTech_Plastmak_Window_Machinery_2026.pdf,
imperial — its figures were checked against the metric ones: they agree except where noted below), plastmak.com (Oct 2026
page captures) and the 2025 price list.  Where they differ the 2026 catalogue's page text and charts win:
  - SÇ 400S: 2 × Ø500 mm blades (title, text and chart; the symbol box still says 2 × 450)
  - SÇ 4000S: 2 × Ø600 mm blades, 215 mm blade rise, ±0.5 mm (title, text and chart; the box and plastmak.com say 550)
  - motor powers as the symbol boxes give them (NovoTech's catalogue garbles a few: "2.7 × 1" for 2 × 0.75 kW and so on)
  - SÇ 100 / SÇ 101 profile height to 160 mm (plastmak.com: 150), SÇ 1000 ±0.5 mm (plastmak.com: 0.1 mm)
The screwing and sash assembly machines are only in NovoTech's catalogue, in imperial; they are shown as given there.

Shown as imperial (metric); lengths to the nearest 1/16″ (1/32″ under 1/4″).
"""
from fractions import Fraction

PLASTMAK = "plastmak"
P_SAWS = "aluminum-and-pvc-upcut-saws"
P_HUB = "pvc-aluminum-window-machines"
P_WELD = "pvc-window-welding-machines"
P_CNC = "profile-machining-centres-copy-routers"
P_ASSY = "window-assembly-machines"
P_LINES = "window-production-lines"


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


def n(v):
    return f"{v:,g}"


def one(a):
    return f"{inch(a)} ({n(a)} mm)"


def dia(a):
    return f"Ø{inch(a)} ({n(a)} mm)"


def rng(a, b):
    return f"{inch(a)} – {inch(b)} ({n(a)} – {n(b)} mm)"


def size(a, b):
    """a × b, e.g. profile height × width"""
    return f"{inch(a)[:-1]} × {inch(b)} ({n(a)} × {n(b)} mm)"


def size_rng(a, b, c, d):
    """frame a × b to c × d"""
    return f"{inch(a)[:-1]} × {inch(b)} – {inch(c)[:-1]} × {inch(d)} ({n(a)} × {n(b)} – {n(c)} × {n(d)} mm)"


def dims(l, w, h):
    return f"{l / 25.4:.0f} × {w / 25.4:.0f} × {h / 25.4:.0f}″ ({n(l)} × {n(w)} × {n(h)} mm)"


def dims2(l, w):
    return f"{l / 25.4:.0f} × {w / 25.4:.0f}″ ({n(l)} × {n(w)} mm)"


def ftin(mm):
    """long lengths as feet and inches: 9′ 10″ (3 m)"""
    t = mm / 25.4
    ft, i = int(t // 12), round(t - 12 * (t // 12))
    if i == 12:
        ft, i = ft + 1, 0
    m = f"{mm / 1000:g} m"
    return f"{ft}′ {i}″ ({m})" if i else f"{ft}′ ({m})"


def hpv(kw):
    return f"{kw / 0.7457:.1f}".rstrip("0").rstrip(".")


def hp(kw):
    return f"{hpv(kw)} HP ({n(kw)} kW)"


def hpx(k, kw):
    """k motors of kw each"""
    return f"{k} × {hpv(kw)} HP ({k} × {n(kw)} kW)"


def hpsum(*kw):
    return " + ".join(hpv(k) for k in kw) + f" HP ({' + '.join(n(k) for k in kw)} kW)"


def cfmv(lpm):
    x = lpm * 0.0353147
    return f"{x:.2f}" if x < 1 else f"{x:.1f}"


def cfm(lpm):
    return f"{cfmv(lpm)} CFM ({n(lpm)} l/min)"


def lbv(kg):
    return f"{round(kg * 2.20462):,} lb"


def lb(kg):
    return f"{lbv(kg)} ({kg:,} kg)"


def rpm(v):
    return f"{v:,} rpm"


def row(label, cells, key=False, sub=""):
    return {"label": label, "sub": sub, "cells": cells, "key": key}


def table(title, sub, models, rows):
    return {"title": title, "sub": sub, "models": models, "rows": rows}


AIR = "87 – 116 psi (6 – 8 bar)"
GK = ["capacity", "profile", "power", "air", "weight"]
NOTE = ("Metric values in brackets are the manufacturer's figures; imperial values are converted and rounded, lengths to the "
        "nearest 1/16″. Air consumption is at 87 – 116 psi (6 – 8 bar). Weights are approximate.")
NOTE_SAW = NOTE + " Cutting capacities are the largest profile, height × width, at the angle shown."
NOTE_NT = ("Figures as listed in NovoTech's Plastmak catalogue. Air supply 87 – 116 psi (6 – 8 bar). Weights are approximate.")


def spec(tbls, glance, note=NOTE, caps=None, models=None):
    """glance: {model: [capacity, profile, power, air, weight]}; models: the range-table rows (default: the first table's columns)"""
    tbls = tbls if isinstance(tbls, list) else [tbls]
    ms = models or tbls[0]["models"]
    return {"kind": "table", "tables": tbls, "models": [{"name": m, "glance": glance[m]} for m in ms],
            "glance_keys": GK, "caps": caps or {}, "note": note}


VOLT = "CSA-approved electrical panel; 600 V 3-phase with transformer (208 / 240 / 480 V on request)"
VOLT_OPT = "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"
CE = "Built to CE standards"

# ================================================================================================ saws
T_401 = table("SÇ 401", "Upcut saw, Ø450 mm blade", ["SÇ 401"], [
    row("Cutting angle", ["0° – 180°"], True, "quick stops 15°, 22.5°, 30°, 45°, 60°, 90°"),
    row("Blade", [dia(450)], True, "diamond-tipped"),
    row("Blade bore", [dia(32)]),
    row("Blade rise", [one(135)], False, "through the table"),
    row("Capacity at 90°", [size(135, 217)], True, "height × width"),
    row("Capacity at 45°", [size(135, 157)], False, "height × width"),
    row("Motor", [hp(1.1)]),
    row("Air consumption", [cfm(41)]),
    row("Conveyors", [f"{ftin(2500)} right and left"], False, "measuring and transport"),
    row("Weight", [lb(125)], True),
    row("Dimensions", [dims(660, 790, 1300)], False, "W × D × H"),
])

T_402_403 = table("SÇ 402 · SÇ 403", "Automatic upcut saws", ["SÇ 402", "SÇ 403"], [
    row("Cutting angle", ["−60° to +60°", "−60° to +60°"], True, "fixed stops 0°, ±15°, ±22.5°, ±30°, ±45°, ±60°"),
    row("Blade", [dia(550), f"{dia(600)}; {dia(650)} optional"], True, "diamond-tipped"),
    row("Blade bore", [dia(32), dia(40)]),
    row("Capacity at 90°", [size(180, 265), f"{size(208, 288)}; {size(233, 315)} with Ø650"], True, "height × width"),
    row("Capacity at 45°", [size(180, 190), f"{size(208, 205)}; {size(233, 223)} with Ø650"], False, "height × width"),
    row("Capacity at 60°", [size(180, 140), f"{size(208, 145)}; {size(233, 157)} with Ø650"], False, "height × width"),
    row("Saw motor", [hp(2.2), hp(3)]),
    row("Total power", [hp(3), hp(3)], True),
    row("Air consumption", [cfm(41), cfm(41)]),
    row("Roller conveyors", [f"{ftin(3000)} right and left"] * 2),
    row("Weight", [lb(200), lb(260)], True),
    row("Dimensions", [dims(820, 900, 1330), dims(850, 985, 1450)], False, "W × D × H"),
])

T_450 = table("SÇ 450", "Shutter box and lamella saw", ["SÇ 450"], [
    row("Blade", [dia(550)], True),
    row("Blade bore", [dia(32)]),
    row("Cutting width", [one(360)], True, "max."),
    row("Shutter box", [one(350)], True, "L-shaped, max."),
    row("Motor", [hp(3)]),
    row("Air consumption", [cfm(10)]),
    row("Roller conveyors", [f"2 × {ftin(3000)}"]),
    row("Weight", [lb(345)], True),
    row("Dimensions", [dims(840, 900, 1980)], False, "W × D × H"),
])

T_DOUBLE = table("SÇ 400S · SÇ 4000S", "Double-head miter saws", ["SÇ 400S", "SÇ 4000S"], [
    row("Cutting length", [rng(485, 3350), rng(550, 4360)], True, "min – max"),
    row("Head tilt", ["90° and 45° inward, automatic"] * 2),
    row("Cutting accuracy", ["±.039″ (±1 mm)", "±.020″ (±0.5 mm)"], True),
    row("Blades", [f"2 × {dia(500)}", f"2 × {dia(600)}"], True),
    row("Blade bore", [dia(32), dia(40)]),
    row("Blade rise", [f"{one(165)} — two 3-1/8″ (80 mm) profiles at once", f"{one(215)} — two 3-1/8″ (80 mm) profiles at once"]),
    row("Capacity at 90°", [size(282, 165), size(310, 215)], True, "height × width"),
    row("Capacity at 45°", [size(200, 165), size(222, 215)], False, "height × width"),
    row("Saw motors", [hpx(2, 2.2), hpx(2, 3)]),
    row("Total power", [hp(6), hp(8)], True),
    row("Air consumption", [cfm(30), cfm(30)]),
    row("Weight", [lb(885), lb(1085)], True),
    row("Dimensions", [dims(6398, 1010, 1580), dims(7375, 1110, 1580)], False, "L × W × H"),
])

T_BEAD = table("SÇ 301 · SÇ 301S", "Glazing bead saws", ["SÇ 301", "SÇ 301S"], [
    row("Cutting angle", ["45°", "45°"]),
    row("Bead length", [rng(300, 2550)] * 2, True, "min – max"),
    row("Bead height", [one(28.3)] * 2, True, "max."),
    row("Bead profiles", ["Universal adjustable mould", "12 on the profile wheel, no moulds; 2 beads at once"], True),
    row("Main saws", [f"2 × {dia(200)}"] * 2),
    row("Nail saws", ["Optional", f"2 × {dia(100)}"]),
    row("Blade bore", [dia(32)] * 2),
    row("Saw motors", [hpx(2, 0.75), hpx(2, 1.1)]),
    row("Total power", [hp(1.5), hp(2.2)], True),
    row("Air consumption", [cfm(10), cfm(10)]),
    row("Conveyors", [f"Measuring conveyor {ftin(2500)}", f"2 × {ftin(2500)}, right and left"]),
    row("Weight", [lb(95), lb(145)], True),
    row("Dimensions", [dims(450, 1160, 1120), dims(520, 1400, 1180)], False, "W × D × H"),
])

T_MITER = table("SÇ 431 · SÇ 441 · SÇ 451", "Overhead and bench miter saws", ["SÇ 431", "SÇ 441", "SÇ 451"], [
    row("Type", ["Overhead (top-down) miter saw on its stand, pneumatic clamping", "Bench miter saw", "Bench miter saw"], True),
    row("Blade", [dia(400), dia(300), dia(400)], True),
    row("Blade bore", [dia(32), "—", "—"]),
    row("Miter range", ["−45° to +45°"] * 3, True),
    row("Quick stops", ["90°, 75°, 60°, 45°", "0°, 15°, 22.5°, 30°, 45° left and right", "0°, 15°, 22.5°, 30°, 45° left and right"]),
    row("Capacity at 90°", [size(120, 180), "—", "—"], True, "height × width"),
    row("Capacity at 45°", [size(120, 125), "—", "—"], False, "height × width"),
    row("Cutting length", [rng(360, 3300), "—", "—"], False, "with the conveyor"),
    row("Motor", [hp(1.5), "—", "—"]),
    row("Air consumption", [cfm(2.2), "—", "—"]),
    row("Weight", [lb(120), "—", "—"], True),
    row("Dimensions", [dims(650, 800, 1340), "—", "—"], False, "W × D × H"),
])

# ================================================================================================ welding & corner cleaning
T_GOLD = table("SÇ 100 Gold Plus · Gold Plus Full", "4-corner PVC welding", ["SÇ 100 Gold Plus", "SÇ 100 Gold Plus Full"], [
    row("Machine", ["4-corner welding machine", "4-corner welding machine, carrier robot and CNC corner cleaner in one line"], True),
    row("Welding angle", ["90°", "90°"]),
    row("Profile height", [rng(40, 200)] * 2, True, "min – max"),
    row("Profile width", [one(150)] * 2, True, "max."),
    row("Frame size, min.", [f"{size(410, 495)}; {size(520, 520)} with gasket press", "—"], False, "width × length"),
    row("Frame size, max.", [f"{size(3700, 2700)}; {size(3650, 2650)} with gasket press", "—"], True, "width × length"),
    row("Weld seam", ["0.2 mm (.008″) seam possible on every profile", "0.2 mm (.008″) seam possible on every profile"]),
    row("Total power", [hp(25), hp(34)], True),
    row("Air consumption", [cfm(180), cfm(350)]),
    row("Weight", [lb(1900), lb(3750)], True),
    row("Dimensions", [dims(5280, 4670, 1670), f"{dims2(13500, 5500)} line footprint"], False, "L × W × H"),
])

T_100_101 = table("SÇ 100 · SÇ 101", "Double- and single-head PVC welding", ["SÇ 100", "SÇ 101"], [
    row("Heads", ["2 (right head moves, locked by button)", "1 (left table moves)"], True),
    row("Welding angle", ["90°", "25° – 180°"], True),
    row("Welded profile length", [rng(340, 3200), "—"], True, "min – max"),
    row("Profile height", [rng(40, 160)] * 2, True, "min – max"),
    row("Profile width", [one(165), one(200)], False, "max."),
    row("Weld seam", ["Normal or 0.2 mm (.008″) on laminated profiles", "Normal or 0.2 mm (.008″)"]),
    row("Control", ["PLC, digital heating-plate temperature"] * 2),
    row("Total power", [hp(9), hp(4)], True),
    row("Air consumption", [cfm(70), cfm(70)]),
    row("Weight", [lb(485), lb(135)], True),
    row("Dimensions", [dims(3870, 1400, 1570), dims(610, 630, 1390)], False, "W × D × H"),
])

T_6000 = table("SÇ 6000 · SÇ 6000S", "CNC corner cleaning, 2 axes", ["SÇ 6000", "SÇ 6000S"], [
    row("Control", ["PLC / NC, joystick programming, touch screen", "CNC, 19″ Windows screen, DXF import (CAM Codex)"], True),
    row("Output", ["400 – 500 frames a shift; 5 – 8 s a corner", "160 – 200 frames a shift, all surfaces and seal grooves"], True, "8-hour shift"),
    row("Cleaning tools", ["Saw, scrapers and cutters on 2 servo axes", "10 tools in separate groups"]),
    row("Frame size", [f"from {size(350, 350)}"] * 2, False, "min. A × B"),
    row("Profile width", [one(150), one(120)], True, "max. a"),
    row("Profile height", [one(200), one(150)], True, "max. h"),
    row("Saw blade", [f"{dia(250)} diamond-tipped, .079″ (2 mm) thick"] * 2),
    row("Blade bore", [dia(32)] * 2),
    row("Spindle", [f"{rpm(18000)}, 300 Hz, {hp(1.4)}", f"{rpm(18000)}, 300 Hz, {hp(1.5)}"]),
    row("Total power", [hp(3), hp(6)], True),
    row("Air consumption", [cfm(40), cfm(120)]),
    row("Weight", [lb(400), lb(750)], True),
    row("Dimensions", [dims(1030, 1400, 1570), dims(1250, 1850, 2100)], False, "W × D × H"),
])

T_601 = table("SÇ 601", "Corner cleaning machine, 3 knives", ["SÇ 601"], [
    row("Cleaning", ["Corners, top and bottom faces; frame and sash profiles told apart automatically"], True),
    row("Profile width", [one(125)], True, "max. a"),
    row("Profile height", [rng(40, 90)], True, "min – max h"),
    row("Knives", ["3"]),
    row("Cutter", [dia(210)], False, "max."),
    row("Cutter bore", [dia(32)]),
    row("Motor", [hp(1.1)]),
    row("Total power", [hp(1.5)], True),
    row("Air consumption", [cfm(10)]),
    row("Weight", [lb(180)], True),
    row("Dimensions", [dims(770, 980, 1510)], False, "W × D × H"),
])

# ================================================================================================ CNC, copy routers, end milling
T_4550 = table("SÇ 4550", "Profile machining and cutting centre, 9 axes", ["SÇ 4550"], [
    row("Axes", ["9"], True),
    row("Profile length", [f"{rng(2000, 6500)} — 6′ 7″ to 21′ 4″"], True, "min – max"),
    row("Spindles", ["10 high-speed air-cooled spindle motors for aluminum"], True),
    row("Spindle head travel", [f"{inch(300)[:-1]} / {inch(320)[:-1]} / {inch(260)} (300 / 320 / 260 mm)"], False, "X / Y / Z"),
    row("Axis speed", ["394 ft/min (120 m/min) average"]),
    row("Profile magazine", ["7 profiles"]),
    row("Cutting unit", ["Servo-controlled, 30° – 150°, ±0.1°"], True),
    row("Saw blade", [dia(550)]),
    row("Blade bore", [dia(32)]),
    row("Total power", [hp(38)], True),
    row("Air consumption", [cfm(500)]),
    row("Weight", [lb(3750)], True),
    row("Dimensions", [dims(13600, 2760, 2200)], False, "L × W × H"),
])

TRAVEL_5000 = f"{inch(390)[:-1]} / {inch(200)[:-1]} / {inch(200)} (390 / 200 / 200 mm)"
T_5000 = table("SÇ 5000 · SÇ 5000S", "3-axis CNC drilling and milling", ["SÇ 5000", "SÇ 5000S"], [
    row("Profiles", ["PVC", "Aluminum and PVC"], True),
    row("Axis travel", [TRAVEL_5000] * 2, True, "X / Y / Z"),
    row("Spindles", [f"3 motors: {hpsum(0.75, 0.55, 0.55)}, {rpm(18000)}", f"3 independent: {hpx(3, 1.4)}, {rpm(18000)}"], True),
    row("Router cutter / shank", [f"Ø{inch(5)} / Ø{inch(8)} (5 / 8 mm)"] * 2),
    row("Routing length", [one(80)] * 2, False, "min."),
    row("Control", ["Point-to-point programming, laser centring", "19″ Windows screen, DXF import (CAM Codex), simulation"]),
    row("Total power", [hp(6), hp(6)], True),
    row("Air consumption", [cfm(9), cfm(9)]),
    row("Weight", [lb(355), lb(750)], True),
    row("Dimensions", [dims(2400, 1130, 1940), dims(1330, 1670, 1900)], False, "W × D × H"),
])

TRAVEL_COPY = f"{inch(280)[:-1]} / {inch(125)[:-1]} / {inch(90)} (280 / 125 / 90 mm)"
COPY = ["SÇ 501", "SÇ 502S", "SÇ 512", "SÇ 521S", "SÇ 542"]
T_COPY = table("SÇ 501 · 502S · 512 · 521S · 542", "Copy routers", COPY, [
    row("Profiles", ["PVC", "Aluminum and PVC", "Aluminum and PVC", "PVC", "Aluminum"], True),
    row("Jobs", ["Lock places, hinge slots, handle holes, drainage slots",
                 "Lock places, hinge slots, handle holes, drainage slots",
                 "Lock places, hinge slots, handle holes",
                 "Water drainage slots, 3 routers",
                 "Handles, locks and hardware slots"], True),
    row("Router speed", [rpm(12000)] + [rpm(18000)] * 4, True),
    row("Router motor", [hpx(2, 0.9), hpsum(0.9, 0.75), hp(0.75), hpx(3, 0.75), hp(1.4)]),
    row("Router travel", [TRAVEL_COPY] * 5, False, "X / Y / Z"),
    row("Router cutter / shank", [f"Ø{inch(5)} / Ø{inch(8)} (5 / 8 mm)"] * 5),
    row("Routing length", [one(80)] * 5, False, "min."),
    row("Triple drilling unit", [f"{hp(0.75)}; drills to Ø{inch(11)} / Ø{inch(12)} (11 / 12 mm)"] * 3 + ["—", "—"]),
    row("Total power", [hp(2.5), hp(3), hp(1.5), hp(3), hp(1.4)], True),
    row("Air consumption", [cfm(9)] * 5),
    row("Conveyor", ["—", f"Right, {ftin(1000)}", f"Right, {ftin(1000)}", "Table moves right and left", f"Right, {ftin(1000)}"]),
    row("Weight", [lb(115), lb(130), lb(110), lb(140), lb(90)], True),
    row("Dimensions", [dims(650, 900, 1220), dims(710, 960, 1250), dims(650, 900, 1220), dims(740, 900, 1475),
                       dims(631, 920, 1443)], False, "W × D × H"),
])

T_211 = table("SÇ 211 · SÇ 211S", "End milling machines", ["SÇ 211", "SÇ 211S"], [
    row("Profiles", ["PVC and aluminum", "Aluminum and PVC"], True),
    row("Milling angle", ["To 30°", "−45° to +45°, mechanical stops"], True),
    row("Cutter", [dia(140), dia(160)], True, "max."),
    row("Cutter bore", [dia(30)] * 2),
    row("Cutter stack height", [one(90), f"{inch(90)} + {inch(200)} (90 + 200 mm)"], False, "max."),
    row("Cutter change", ["Series switch button (60 – 70 series)", "Whole cutter group by one button; rack for 3 groups"]),
    row("Motor", [hp(1.1)] * 2, True),
    row("Air consumption", [cfm(10)] * 2),
    row("Weight", [lb(100), lb(155)], True),
    row("Dimensions", [dims(690, 600, 1220), dims(1030, 670, 1245)], False, "W × D × H"),
])

# ================================================================================================ assembly, portable, conveyors
T_902 = table("SÇ 902", "Hydraulic corner crimping machine", ["SÇ 902"], [
    row("Profiles", ["Aluminum, 90° corners"], True),
    row("Profile height", [one(130)], True, "max. H"),
    row("Knives", ["4 right and 4 left, hydraulic"], True),
    row("Crimping force", ["2 × 3,307 lbf (2 × 1,500 kgf) at 102 psi (7 bar)"], True),
    row("Hydraulic pressure", ["1,450 psi (100 bar)"], False, "max."),
    row("Total power", [hp(2.2)], True),
    row("Air consumption", [cfm(20)]),
    row("Weight", [lb(360)], True),
    row("Dimensions", [dims(1090, 930, 1280)], False, "W × D × H"),
])

SCREW = ["Single screwing machine", "Double-head screwing machine", "Sash assembly machine"]
T_SCREW = table("Screwing and sash assembly", "Pneumatic screwing stations and a sash hardware assembly machine", SCREW, [
    row("Job", ["Screwing at one station", "Screwing with two heads at once, PVC and aluminum", "Fitting and screwing sash hardware, single and double opening"], True),
    row("Working range", ["A and B 1.6 – 4.7″", "—", "—"], False, "min – max"),
    row("Screw size", ["3.9 × 16 mm to 4.2 × 38 mm", "to 4.2 × 38 mm", "—"], True),
    row("Screwing motor", ["Pneumatic, 0.7 HP, 3,000 rpm, stall torque 5 lb·ft", "2 × pneumatic, 0.7 HP, 3,000 rpm, stall torque 5 lb·ft",
                           "Automatic screwing with laser alignment"]),
    row("Cycle", ["Foot pedal", "—", "Double opening window: 3.5 min on average"], True),
    row("Air", ["90 – 120 psi, 1/4″ inlet", "90 – 120 psi, 1/4″ inlet", "90 – 120 psi"]),
    row("Weight", ["276 lb", "463 lb", "—"], True),
    row("Dimensions", ["43 × 22 × 79″", "35 × 30 × 79″", "—"], False, "L × W × H"),
    row("Colour", ["—", "RAL 7035", "RAL 7035"]),
])

T_PORTABLE = table("SÇ 221 · SÇ 551 · stand", "Portable machines", ["SÇ 221", "SÇ 551", "Portable stand"], [
    row("Job", ["Mullion (transom) notching of aluminum and PVC profiles",
                "Lock, handle, hinge and espagnolette slots and grooves of any size",
                "Two-shelf steel stand for the portable machines"], True),
    row("Working", ["Vertical and horizontal vises", "Copy template made for your job; grooving against the stop without a template", "—"]),
    row("Motor", ["Single-phase", "—", "—"]),
    row("Options", ["Lower cabinet; pneumatic system", "Lower cabinet; pneumatic system", "—"]),
])

CONV = ["SÇ 1000", "SÇ 1001", "SÇ 1002", "SÇ 1003"]
T_CONV = table("SÇ 1000 · 1001 · 1002 · 1003", "Measuring and roller conveyors", CONV, [
    row("Type", ["Digital measuring conveyor with stop", "Aluminum roller conveyor", "Plastic roller conveyor", "Sheet-metal conveyor"], True),
    row("Measuring length", [ftin(3000), "—", "—", "—"], True),
    row("Accuracy", ["±.020″ (±0.5 mm)", "—", "—", "—"], True),
    row("Control", ["Touch screen; stop retracts at one push to free the cut piece", "—", "—", "—"]),
    row("Supply", ["220 V single-phase", "—", "—", "—"]),
    row("Legs", ["—", "Height-adjustable", "Height-adjustable", "Height-adjustable"]),
])

# ================================================================================================ production groups
# per machine: (job, capacity, kW, l/min, kg) from the tables above
M = {
    "SÇ 401": ("Upcut saw", f"Ø{inch(450)} blade, 0° – 180°", 1.1, 41, 125),
    "SÇ 400S": ("Double-head saw", f"2 × Ø{inch(500)} blades, {inch(485)} – {inch(3350)}", 6, 30, 885),
    "SÇ 4000S": ("Double-head saw", f"2 × Ø{inch(600)} blades, {inch(550)} – {inch(4360)}", 8, 30, 1085),
    "SÇ 501": ("Copy router with triple drilling", f"Travel {inch(280)[:-1]} × {inch(125)[:-1]} × {inch(90)}", 2.5, 9, 115),
    "SÇ 5000": ("3-axis CNC drilling and milling", f"Travel {inch(390)[:-1]} × {inch(200)[:-1]} × {inch(200)}", 6, 9, 355),
    "SÇ 5000S": ("3-axis CNC drilling and milling", f"Travel {inch(390)[:-1]} × {inch(200)[:-1]} × {inch(200)}", 6, 9, 750),
    "SÇ 101": ("Single-head welder", f"25° – 180°, profiles to {inch(160)} high", 4, 70, 135),
    "SÇ 100": ("Double-head welder", f"Profiles {inch(340)} – {inch(3200)} long", 9, 70, 485),
    "SÇ 301": ("Glazing bead saw", f"Beads to {inch(2550)}", 1.5, 10, 95),
    "SÇ 301S": ("Mouldless glazing bead saw", f"12 beads, to {inch(2550)}", 2.2, 10, 145),
    "SÇ 211": ("End milling machine", f"Cutters to Ø{inch(140)}", 1.1, 10, 100),
    "SÇ 211S": ("End milling machine", f"Cutters to Ø{inch(160)}, ±45°", 1.1, 10, 155),
    "SÇ 601": ("Corner cleaner, 3 knives", f"Profiles to {inch(125)} wide", 1.5, 10, 180),
    "SÇ 6000": ("CNC corner cleaner", "400 – 500 frames a shift", 3, 40, 400),
    "SÇ 902": ("Hydraulic corner crimper", f"Profiles to {inch(130)} high", 2.2, 20, 360),
    "SÇ 801": ("Air compressor", "130 gal (500 l) tank", None, None, None),
}
LINES = {
    "pm-line-pvc1": ("PVC single-head group", (40, 60), ["SÇ 401", "SÇ 501", "SÇ 101", "SÇ 301", "SÇ 211", "SÇ 601"]),
    "pm-line-pvc2": ("PVC double-head group", (80, 120), ["SÇ 400S", "SÇ 501", "SÇ 100", "SÇ 301", "SÇ 211", "SÇ 601"]),
    "pm-line-alu": ("Aluminum double-head group", (80, 120), ["SÇ 4000S", "SÇ 5000S", "SÇ 211S", "SÇ 902"]),
    "pm-line-shop": ("PVC window workshop", (200, 220), ["SÇ 801", "SÇ 400S", "SÇ 5000", "SÇ 100", "SÇ 6000", "SÇ 211S", "SÇ 301S"]),
}


def line_totals(machines):
    ms = [M[m] for m in machines if M[m][2] is not None]
    return round(sum(x[2] for x in ms), 1), sum(x[3] for x in ms), sum(x[4] for x in ms)


def line_spec(lid):
    name, (lo, hi), machines = LINES[lid]
    kw, lpm, kg = line_totals(machines)
    t1 = table(name, f"{lo} – {hi} windows in an 8-hour shift", machines, [
        row("Job", [M[m][0] for m in machines], True),
        row("Capacity", [M[m][1] for m in machines]),
        row("Power", [hp(M[m][2]) if M[m][2] else "—" for m in machines]),
        row("Air consumption", [cfm(M[m][3]) if M[m][3] else "—" for m in machines]),
        row("Weight", [lb(M[m][4]) if M[m][4] else "—" for m in machines]),
    ])
    extra = " (without the compressor)" if "SÇ 801" in machines else ""
    t2 = table(f"{name} — the whole group", "Sums of the machines above" + extra, [name], [
        row("Output", [f"{lo} – {hi} windows in an 8-hour shift"], True),
        row("Machines", [str(len(machines))]),
        row("Installed power", [hp(kw)], True),
        row("Air consumption", [cfm(lpm)]),
        row("Machine weight", [lb(kg)], True),
    ])
    glance = {name: [f"{lo} – {hi} windows a shift", "Aluminum" if "alu" in lid else "PVC", f"{hpv(kw)} HP", f"{cfmv(lpm)} CFM", lbv(kg)]}
    return spec([t1, t2], glance, NOTE + " Group figures are the sums of the machines' own figures.", models=[name])


# ================================================================================================ families
def fam(fid, group, page, name, short, models_label, summary, headline, features, optional, images, specs, videos=()):
    return dict(id=fid, group=group, page=page, brand=PLASTMAK, name=name, short=short, models_label=models_label, summary=summary,
                headline=headline, features=features, optional=optional, images=images, specs=specs, videos=list(videos))


FAMILIES = [
    # ------------------------------------------------------------------------------------------ saws
    fam("plastmak-401", "pm-upcut", P_SAWS,
        "SÇ 401 upcut saw for aluminum and PVC, Ø17-11/16″ blade, 0° – 180°", "SÇ 401", "SÇ 401 · 1 model",
        "The entry upcut saw for window shops and aluminum fabricators: the Ø17-11/16″ (450 mm) diamond-tipped blade rises from "
        "under the table through the clamped profile, so the cut is guarded and burr-light, and the turntable sets any angle from "
        "0° to 180° — with quick stops at 15°, 22.5°, 30°, 45°, 60° and 90° and a locking arm for the angles between. The blade "
        "rises 5-5/16″ (135 mm) and cuts profiles up to 5-5/16″ high and 8-9/16″ wide at 90°. Its feed slows down when the blade "
        "meets aluminum, easing the load on the motor, and 8′ 2″ (2.5 m) measuring and transport conveyors come standard on both sides.",
        "Ø17-11/16″ (450 mm) blade · 0° – 180° · cuts 5-5/16 × 8-9/16″ at 90°",
        ["Diamond-tipped Ø17-11/16″ (450 mm) blade rising 5-5/16″ (135 mm) through the table",
         "Turntable 0° – 180° with quick stops at 15°, 22.5°, 30°, 45°, 60° and 90°; locking arm for intermediate angles",
         "Blade feed slows in aluminum to reduce the load on the motor",
         "Pneumatic profile clamps; protective cover over the cutting area",
         "Measuring and transport conveyors 8′ 2″ (2.5 m), right and left, standard",
         CE, VOLT],
        ["Cooling device for aluminum cutting", "Hydro-check feed control for aluminum cutting", "Roller conveyor",
         "SÇ 1000 digital measuring conveyor", VOLT_OPT],
        ["pm-401", "pm-401-table", "pm-401-scale", "pm-401-guard"],
        spec(T_401, {"SÇ 401": [f"Ø{inch(450)} blade, 0° – 180°", f"{inch(135)[:-1]} × {inch(217)} at 90°", f"{hpv(1.1)} HP", f"{cfmv(41)} CFM", lbv(125)]},
             NOTE_SAW, caps={"SÇ 401": f"Ø{inch(450)} (450 mm) blade"})),
    fam("plastmak-402-403", "pm-upcut", P_SAWS,
        "SÇ 402 · SÇ 403 automatic upcut saws, Ø21-5/8″ to Ø25-9/16″ blades", "SÇ 402 · SÇ 403", "SÇ 402 · SÇ 403 · 2 models",
        "Fully automatic upcut saws for aluminum and PVC production: the profile is clamped pneumatically from above and from the "
        "side, the blade rises through it under hydro-pneumatic control at the speed set for the profile, and an oil spray cools "
        "the cut. The head turns to fixed stops from −60° to +60° — 0°, 15°, 22.5°, 30°, 45° and 60° either way. The SÇ 402 runs a "
        "Ø21-5/8″ (550 mm) blade and cuts profiles up to 7-1/16″ high and 10-7/16″ wide at 90°; the SÇ 403 takes a Ø23-5/8″ "
        "(600 mm) blade, or Ø25-9/16″ (650 mm) as an option, for profiles up to 9-3/16 × 12-3/8″, behind a guard that moves front "
        "to back. Both come with 9′ 10″ (3 m) roller conveyors on each side.",
        "Ø21-5/8″ – Ø25-9/16″ blades · −60° to +60° · cuts to 9-3/16 × 12-3/8″",
        ["Hydro-pneumatic blade feed with hydro-checks; cutting speed set to the profile",
         "Fixed angle stops left and right: 0°, 15°, 22.5°, 30°, 45° and 60°",
         "Pneumatic vertical and horizontal clamps with adjustable pressure; two-hand safety start",
         "SÇ 402: Ø21-5/8″ (550 mm) diamond-tipped blade, 3 HP (2.2 kW) saw motor",
         "SÇ 403: Ø23-5/8″ (600 mm) blade, Ø25-9/16″ (650 mm) optional; 4 HP (3 kW) saw motor; front-rear moving guard",
         "Oil spray cooling; roller conveyors 9′ 10″ (3 m) right and left",
         CE, VOLT],
        ["Ø25-9/16″ (650 mm) blade (SÇ 403)", "SÇ 1000 digital measuring conveyor", VOLT_OPT],
        ["pm-402", "pm-403", "pm-402-table", "pm-402-blade", "pm-403-panel", "pm-403-clamps", "pm-403-blade", "pm-403-guard"],
        spec(T_402_403, {"SÇ 402": [f"Ø{inch(550)} blade, ±60°", f"{inch(180)[:-1]} × {inch(265)} at 90°", f"{hpv(3)} HP", f"{cfmv(41)} CFM", lbv(200)],
                         "SÇ 403": [f"Ø{inch(600)} / Ø{inch(650)} blade, ±60°", f"{inch(233)[:-1]} × {inch(315)} at 90°", f"{hpv(3)} HP", f"{cfmv(41)} CFM", lbv(260)]},
             NOTE_SAW, caps={"SÇ 402": f"Ø{inch(550)} (550 mm) blade", "SÇ 403": f"Ø{inch(600)} (600 mm) blade"})),
    fam("plastmak-450", "pm-upcut", P_SAWS,
        "SÇ 450 roller-shutter box and lamella saw, Ø21-5/8″ blade, cuts 14-3/16″ wide", "SÇ 450", "SÇ 450 · 1 model",
        "A saw for roller-shutter work: it cuts packs of aluminum or PVC shutter lamellas in one stroke, shutter boxes and side "
        "posts, and monoblock shutter boxes as a set. The Ø21-5/8″ (550 mm) blade runs fast for a clean cut surface and travels "
        "on linear guides; the clamping pistons are matched to the part, L-shaped boxes up to 13-3/4″ (350 mm) fit under them, "
        "and the blade cuts 14-3/16″ (360 mm) wide. The cutting speed is adjustable, and 9′ 10″ (3 m) roller conveyors carry the "
        "profiles on both sides.",
        "Ø21-5/8″ (550 mm) blade · shutter boxes to 13-3/4″ · cuts 14-3/16″ wide",
        ["Cuts packs of shutter lamellas, shutter boxes, side posts and monoblock boxes",
         "Ø21-5/8″ (550 mm) blade at high speed for a clean cut surface; adjustable cutting speed",
         "Blade on a linear guide system for precise cuts",
         "Clamping pistons matched to the part; L-shaped boxes up to 13-3/4″ (350 mm)",
         "Roller conveyors 2 × 9′ 10″ (3 m)",
         VOLT],
        ["Cooling system", VOLT_OPT],
        ["pm-450", "pm-450-clamps", "pm-450-blade", "pm-450-roller", "pm-450-table"],
        spec(T_450, {"SÇ 450": [f"Ø{inch(550)} blade, boxes to {inch(350)}", f"Cuts {inch(360)} wide", f"{hpv(3)} HP", f"{cfmv(10)} CFM", lbv(345)]},
             NOTE_SAW, caps={"SÇ 450": f"Ø{inch(550)} (550 mm) blade"})),
    fam("plastmak-double", "pm-double", P_SAWS,
        "SÇ 400S · SÇ 4000S double-head miter saws, cutting lengths to 171-5/8″", "SÇ 400S · SÇ 4000S", "SÇ 400S · SÇ 4000S · 2 models",
        "Double-head saws cut both ends of a window or door profile in one stroke, square or mitred, to the length set on the "
        "control: the right head runs on a servo-driven carriage, both heads tilt automatically to 90° or 45° inward, and an arm "
        "supports long profiles. The SÇ 400S has two Ø19-11/16″ (500 mm) blades, cuts 19-1/8″ to 131-7/8″ (485 – 3,350 mm) long to "
        "±.039″ (±1 mm) and takes profiles up to 11-1/8″ high at 90°. The fully automatic SÇ 4000S has two Ø23-5/8″ (600 mm) "
        "blades on hydro-check-controlled feeds, cuts 21-5/8″ to 171-5/8″ (550 – 4,360 mm) to ±.020″ (±0.5 mm) and takes profiles "
        "up to 12-3/16″ high and 8-7/16″ wide. Cut lists arrive by USB; the SÇ 400S works with Ercom and Teknosoft barcode systems.",
        "2 × Ø19-11/16″ or 2 × Ø23-5/8″ blades · lengths to 171-5/8″ · ±.020″",
        ["Heads set automatically to 90° and 45° inward; automatic cutting at 90°; wedge (block) slicing",
         "Servo-driven moving head; colour touch panel (10″ on the SÇ 4000S); unlimited cut-list memory, lists by USB; remote support",
         "SÇ 400S: 2 × Ø19-11/16″ (500 mm) blades rising 6-1/2″ (165 mm) — two 3-1/8″ (80 mm) profiles at once; ±.039″ (±1 mm)",
         "SÇ 4000S: 2 × Ø23-5/8″ (600 mm) blades rising 8-7/16″ (215 mm) — two 3-1/8″ profiles at once; hydro-check saw feed; ±.020″",
         "2 vertical and 4 horizontal vises; profile supports right, left and between the heads; automatic support arm for long profiles",
         "Program for profiles longer than the bed: 19′ 8″ (6 m) on the SÇ 400S, 26′ 3″ (8 m) on the SÇ 4000S",
         "Spray blade cooling; multi-language software",
         CE, VOLT],
        ["Barcode printer (Ercom, Teknosoft)", "Hydro-check saw feed (SÇ 400S)", VOLT_OPT],
        ["pm-400s", "pm-4000s", "pm-400s-head", "pm-400s-console", "pm-400s-vise", "pm-400s-support", "pm-400s-guard",
         "pm-4000s-heads", "pm-4000s-tilt", "pm-4000s-console", "pm-4000s-conveyor", "pm-4000s-clamps", "pm-4000s-slide"],
        spec(T_DOUBLE, {"SÇ 400S": [f"Lengths {inch(485)} – {inch(3350)}", f"{inch(282)[:-1]} × {inch(165)} at 90°", f"{hpv(6)} HP", f"{cfmv(30)} CFM", lbv(885)],
                        "SÇ 4000S": [f"Lengths {inch(550)} – {inch(4360)}", f"{inch(310)[:-1]} × {inch(215)} at 90°", f"{hpv(8)} HP", f"{cfmv(30)} CFM", lbv(1085)]},
             NOTE_SAW, caps={"SÇ 400S": f"2 × Ø{inch(500)} (500 mm) blades", "SÇ 4000S": f"2 × Ø{inch(600)} (600 mm) blades"}),
        ),
    fam("plastmak-bead", "pm-bead", P_SAWS,
        "SÇ 301 · SÇ 301S glazing bead saws, beads 11-13/16″ – 100-3/8″ long", "SÇ 301 · SÇ 301S", "SÇ 301 · SÇ 301S · 2 models",
        "Glazing beads are cut at 45° on both ends to the size of the glass opening. The SÇ 301 cuts PVC beads automatically with "
        "two Ø7-7/8″ (200 mm) saws in an easily adjusted universal mould, with an 8′ 2″ (2.5 m) sheet-steel measuring conveyor for "
        "long frames. The SÇ 301S needs no moulds: a wheel holds 12 different bead profiles, two beads are cut at the same time, a "
        "nail adjustment mechanism and two nail saws finish the bead's clip, and 8′ 2″ (2.5 m) conveyors run on both sides — with a "
        "diamond saw and cooling it cuts aluminum beads too. Both take beads 11-13/16″ to 100-3/8″ (300 – 2,550 mm) long and up "
        "to 1-1/8″ (28.3 mm) high.",
        "45° bead cutting · 11-13/16″ – 100-3/8″ · 12 beads without moulds (SÇ 301S)",
        ["45° cutting of glazing beads; automatic cycle, adjustable cutting speed",
         "Pneumatic bead clamping",
         "SÇ 301: 2 × Ø7-7/8″ (200 mm) saws, universal adjustable mould, measuring conveyor 8′ 2″ (2.5 m)",
         "SÇ 301S: profile wheel for 12 beads, 2 beads at once, 2 nail saws Ø3-15/16″ (100 mm), conveyors 2 × 8′ 2″",
         CE, VOLT],
        ["Left conveyor (SÇ 301)", "Nail saw (SÇ 301)", "Diamond-tipped saw with cooling for aluminum beads (SÇ 301S)", VOLT_OPT],
        ["pm-301", "pm-301s", "pm-301-mould", "pm-301-saws", "pm-301s-wheel", "pm-301s-clamps", "pm-301s-twin", "pm-301s-top"],
        spec(T_BEAD, {"SÇ 301": [f"Beads {inch(300)} – {inch(2550)}", f"Beads to {inch(28.3)} high", f"{hpv(1.5)} HP", f"{cfmv(10)} CFM", lbv(95)],
                      "SÇ 301S": [f"Beads {inch(300)} – {inch(2550)}, 12 profiles", f"Beads to {inch(28.3)} high", f"{hpv(2.2)} HP", f"{cfmv(10)} CFM", lbv(145)]},
             NOTE_SAW, caps={"SÇ 301": "2 × Ø7-7/8″ (200 mm) saws", "SÇ 301S": "12 bead profiles, no moulds"})),
    fam("plastmak-miter", "pm-miter", P_SAWS,
        "SÇ 431 · SÇ 441 · SÇ 451 overhead and bench miter saws, Ø11-13/16″ to Ø15-3/4″ blades", "SÇ 431 · SÇ 441 · SÇ 451",
        "SÇ 431 · SÇ 441 · SÇ 451 · 3 models",
        "Top-down miter saws for aluminum and PVC profiles. The SÇ 431 stands on its own base with a pneumatic clamp and a "
        "Ø15-3/4″ (400 mm) diamond blade that leaves burr-free aluminum cuts; it miters from −45° to +45° with quick stops at 90°, "
        "75°, 60° and 45° and a locking arm between them, cuts profiles up to 4-3/4″ high and 7-1/16″ wide at 90°, and works with "
        "a 9′ 10″ (3 m) roller conveyor. The SÇ 441 (Ø11-13/16″, 300 mm) and SÇ 451 (Ø15-3/4″, 400 mm) are bench saws for the "
        "workshop or the site: double springs and a guard for safe cuts, cutting on the top table, and fixed stops at 0°, 15°, "
        "22.5°, 30° and 45° either way.",
        "Ø11-13/16″ – Ø15-3/4″ blades · −45° to +45° · cuts 4-3/4 × 7-1/16″ (SÇ 431)",
        ["SÇ 431: Ø15-3/4″ (400 mm) diamond blade, burr-free aluminum cuts; −45° to +45°, quick stops 90°, 75°, 60°, 45°",
         "SÇ 431: pneumatic profile clamp, table locking arm, roller conveyor 9′ 10″ (3 m)",
         "SÇ 441 · SÇ 451: bench miter saws, Ø11-13/16″ and Ø15-3/4″ blades, −45° to +45°",
         "SÇ 441 · SÇ 451: double spring system and saw guard; fixed stops 0°, 15°, 22.5°, 30°, 45° left and right",
         CE, VOLT],
        ["Cooling device for aluminum cutting (SÇ 431)", "Single-phase 220 V version (SÇ 431)",
         "Lower cabinet, right / left measuring system, pneumatic clamping with cooling, diamond triple-chip saw (SÇ 441 · SÇ 451)",
         "Portable stand (SÇ 441 · SÇ 451)", VOLT_OPT],
        ["pm-431", "pm-441", "pm-451", "pm-431-table", "pm-431-head"],
        spec(T_MITER, {"SÇ 431": [f"Ø{inch(400)} blade, ±45°", f"{inch(120)[:-1]} × {inch(180)} at 90°", f"{hpv(1.5)} HP", f"{cfmv(2.2)} CFM", lbv(120)],
                       "SÇ 441": [f"Ø{inch(300)} blade, ±45°", "—", "—", "—", "—"],
                       "SÇ 451": [f"Ø{inch(400)} blade, ±45°", "—", "—", "—", "—"]},
             NOTE_SAW, caps={"SÇ 431": "Ø15-3/4″ (400 mm) blade", "SÇ 441": "Ø11-13/16″ (300 mm) blade", "SÇ 451": "Ø15-3/4″ (400 mm) blade"})),

    # ------------------------------------------------------------------------------------------ welding & corner cleaning
    fam("plastmak-gold-plus", "pm-weld", P_WELD,
        "SÇ 100 Gold Plus 4-corner PVC welder and Gold Plus Full welding & cleaning line, frames to 145-11/16 × 106-5/16″",
        "SÇ 100 Gold Plus · Gold Plus Full", "SÇ 100 Gold Plus · Gold Plus Full · 2 models",
        "The fastest way to weld a PVC window frame: the SÇ 100 Gold Plus welds all four corners at 90° at the same time. Its "
        "heads ride on linear rails, driven by servo motors through planetary gearboxes, and automatic carriers bring the profiles "
        "in; frames from 16-1/8 × 19-1/2″ up to 145-11/16 × 106-5/16″ (410 × 495 to 3,700 × 2,700 mm), profiles 1-9/16″ to "
        "7-7/8″ high, with a 0.2 mm seam on every profile type. A barcode scanner and a 19″ Windows screen recall each profile's "
        "temperatures and times. The Gold Plus Full adds a high-precision carrier robot and a CNC corner cleaner that recognises "
        "each frame itself — welding and cleaning in one line, four frames on it at once, with automatic colour / white separation.",
        "4 corners at once · frames to 145-11/16 × 106-5/16″ · welding and cleaning line (Full)",
        ["Welds the four corners of a PVC frame at 90° at the same time; single-corner welding too",
         "Axes on servo motors with planetary gearboxes; linear-rail top presses; automatic carriers",
         "0.2 mm weld seam possible on every profile type; U (threshold-less door) welding",
         "Heating temperature and time set independently by PID; welding, cooling and temperature stored per profile",
         "Barcode scanner and 19″ Windows-based screen; quick mould change; roll-type Teflon changed in minutes",
         "Gold Plus Full: carrier robot arm and CNC corner cleaner that identifies each frame without the operator; 2-axis carrier "
         "arm feeding profiles; 4 frames on the line at once; automatic colour / white separation",
         CE, VOLT],
        ["Gasket press system (frames 20-1/2 × 20-1/2″ to 143-11/16 × 104-5/16″)", VOLT_OPT],
        ["pm-100gp", "pm-100gp-full", "pm-gp-head", "pm-gp-heads", "pm-gp-top", "pm-gp-press", "pm-gp-heater", "pm-gp-console",
         "pm-gp-robot", "pm-gp-cleaner", "pm-gp-corner"],
        spec(T_GOLD, {"SÇ 100 Gold Plus": [f"Frames to {inch(3700)[:-1]} × {inch(2700)}", f"h {inch(40)[:-1]} – {inch(200)} · w {inch(150)}", f"{hpv(25)} HP", f"{cfmv(180)} CFM", lbv(1900)],
                      "SÇ 100 Gold Plus Full": ["4 corners welded and cleaned", f"h {inch(40)[:-1]} – {inch(200)} · w {inch(150)}", f"{hpv(34)} HP", f"{cfmv(350)} CFM", lbv(3750)]},
             caps={"SÇ 100 Gold Plus Full": "welding and cleaning line", "SÇ 100 Gold Plus": "4-corner welder"})),
    fam("plastmak-100-101", "pm-weld", P_WELD,
        "SÇ 100 · SÇ 101 double- and single-head PVC welders, profiles to 6-5/16″ high", "SÇ 100 · SÇ 101", "SÇ 100 · SÇ 101 · 2 models",
        "The welders of most PVC window shops. The SÇ 100 welds two corners at once: its right head is moved to the profile "
        "length and locked with a button, profiles from 13-3/8″ to 126″ (340 – 3,200 mm) long and 1-9/16″ to 6-5/16″ high, with a "
        "normal or a 0.2 mm seam on laminated profiles, and top-down centring on linear guides. The SÇ 101 welds one corner at any "
        "angle from 25° to 180° — for arches, bays and odd frames — with individually clamping top pistons, a moving left table and "
        "a foot pedal. Both are PLC-controlled with thermostatic heating plates set on a digital display, store temperature, "
        "time and pressure for each profile type, and change moulds quickly.",
        "Two corners (SÇ 100) or one at 25° – 180° (SÇ 101) · profiles to 6-5/16″ high",
        ["SÇ 100: two heads, right head positioned and locked by button; profiles 13-3/8″ – 126″ (340 – 3,200 mm) long",
         "SÇ 100: normal and 0.2 mm seams on laminated profiles; single-corner welding; top-down centring; linear guides",
         "SÇ 101: any angle from 25° to 180°; individually clamping top pistons; moving left table; foot-pedal clamping",
         "PLC control; thermostatic heating plates, temperature set on a digital display; temperature, time and pressure per profile",
         "Quick mould change; power supply protected against voltage surges",
         CE, VOLT],
        [VOLT_OPT],
        ["pm-100", "pm-101", "pm-100-head", "pm-100-side", "pm-100-heater", "pm-100-panel", "pm-100-guide", "pm-101-head", "pm-101-plates"],
        spec(T_100_101, {"SÇ 100": [f"Profiles {inch(340)} – {inch(3200)} long", f"h {inch(40)[:-1]} – {inch(160)} · w {inch(165)}", f"{hpv(9)} HP", f"{cfmv(70)} CFM", lbv(485)],
                         "SÇ 101": ["One corner, 25° – 180°", f"h {inch(40)[:-1]} – {inch(160)} · w {inch(200)}", f"{hpv(4)} HP", f"{cfmv(70)} CFM", lbv(135)]},
             caps={"SÇ 100": "double-head welder", "SÇ 101": "single-head welder, 25° – 180°"}),
        vids(("w9HuC6RrHno", "SÇ 101 welding a PVC corner"))),
    fam("plastmak-6000", "pm-clean", P_WELD,
        "SÇ 6000 · SÇ 6000S CNC corner cleaners, profiles to 7-7/8″ high", "SÇ 6000 · SÇ 6000S", "SÇ 6000 · SÇ 6000S · 2 models",
        "After welding, every corner of a PVC frame carries a bead of melted plastic that has to come off. The SÇ 6000 cleans the "
        "bottom, top and outer faces of 90° corners with a Ø9-13/16″ (250 mm) diamond-tipped saw, scrapers and a high-frequency "
        "spindle on two servo axes — 5 to 8 seconds a corner, 400 to 500 frames in an 8-hour shift; programs are written with a "
        "joystick, angles and radii come from circular interpolation, and a pedal centres the frame. The SÇ 6000S is the full CNC "
        "cleaner: 10 tools in separate groups clean top and bottom faces of white and laminated profiles, the inner and outer seal "
        "grooves and angled and radiused surfaces, it recognises the profile itself, and it imports DXF drawings through CAM "
        "Codex — 160 to 200 frames a shift.",
        "2 axes · 400 – 500 frames a shift (SÇ 6000) · 10 tools, DXF (SÇ 6000S)",
        ["Ø9-13/16″ (250 mm) diamond-tipped saw and bearing-guided scrapers; high-frequency 18,000 rpm spindle",
         "SÇ 6000: 2 servo axes and 1 high-frequency motor; joystick programming of Y and Z; touch screen; foot-pedal centring",
         "SÇ 6000: 5 – 8 s a corner, 400 – 500 frames a shift; daily and monthly production report; sensor profile stop",
         "SÇ 6000S: 10 cleaning tools; seal grooves, angled and radiused surfaces; automatic profile recognition",
         "SÇ 6000S: 19″ LCD screen, own software, DXF import and drawing with CAM Codex; automatic timed lubrication; linear slides",
         "Unlimited program memory; profile carry tables with brush tops that keep the profiles from scratching",
         CE, VOLT],
        [VOLT_OPT],
        ["pm-6000", "pm-6000s", "pm-6000-panel", "pm-6000-saw", "pm-6000-head", "pm-6000-inside", "pm-6000s-tools", "pm-6000s-head",
         "pm-6000s-inside", "pm-6000s-scraper", "pm-6000s-pendant"],
        spec(T_6000, {"SÇ 6000": ["400 – 500 frames a shift", f"h {inch(200)} · w {inch(150)}", f"{hpv(3)} HP", f"{cfmv(40)} CFM", lbv(400)],
                      "SÇ 6000S": ["160 – 200 frames a shift, 10 tools", f"h {inch(150)} · w {inch(120)}", f"{hpv(6)} HP", f"{cfmv(120)} CFM", lbv(750)]},
             caps={"SÇ 6000": "semi-automatic CNC corner cleaner", "SÇ 6000S": "CNC corner cleaner, 10 tools"})),
    fam("plastmak-601", "pm-clean", P_WELD,
        "SÇ 601 corner cleaning machine with 3 knives, profiles to 4-15/16″ wide", "SÇ 601", "SÇ 601 · 1 model",
        "The PLC-controlled corner cleaner for shops that weld on an SÇ 100 or SÇ 101: the welded corner is pushed against the "
        "square, centred automatically, and three knives and bearing-guided scrapers clean the corner and its top and bottom "
        "faces in one cycle. Frame and sash profiles are told apart automatically, and on acrylic-coated profiles surface and "
        "corner cleaning can be run separately. Profiles up to 4-15/16″ (125 mm) wide and 1-9/16″ to 3-9/16″ (40 – 90 mm) high.",
        "3 knives · profiles to 4-15/16″ wide, 1-9/16″ – 3-9/16″ high",
        ["Cleans the corner and the top and bottom faces after welding",
         "3 different knives; bearing-guided scraping system",
         "Automatic squaring against the stop and automatic centring of the profile",
         "Automatic frame / sash separation; surface and corner cleaning separately for acrylic profiles",
         "Fully automatic PLC operation",
         CE, VOLT],
        [VOLT_OPT],
        ["pm-601", "pm-601-inside", "pm-601-cutter", "pm-601-scraper"],
        spec(T_601, {"SÇ 601": ["90° corners, 3 knives", f"h {inch(40)[:-1]} – {inch(90)} · w {inch(125)}", f"{hpv(1.5)} HP", f"{cfmv(10)} CFM", lbv(180)]},
             caps={"SÇ 601": "corner cleaner, 3 knives"})),

    # ------------------------------------------------------------------------------------------ CNC, copy routers, end milling
    fam("plastmak-4550", "pm-cnc", P_CNC,
        "SÇ 4550 9-axis profile machining and cutting centre, profiles to 21′ 4″", "SÇ 4550", "SÇ 4550 · 1 model",
        "A complete machining line for aluminum and PVC profiles: seven profiles wait in the magazine, the length of each is "
        "measured automatically, a 3-axis holding station clamps it, and ten high-speed air-cooled spindles groove, drill, mark "
        "and mill it before a servo-controlled Ø21-5/8″ (550 mm) saw cuts it at any angle from 30° to 150° to ±0.1°. Profiles from "
        "78-3/4″ to 255-7/8″ (2,000 – 6,500 mm), axes averaging 394 ft/min (120 m/min). Finished parts wait on a station and leave "
        "on a belt conveyor with a printed barcode label; offcuts go to the collection cart by conveyor. A 23.8″ touch screen "
        "runs Windows-based software; jobs arrive by USB, the machine can be watched online and is backed by a UPS.",
        "9 axes · 10 spindles · profiles 78-3/4″ – 255-7/8″ · saw 30° – 150°",
        ["Grooving, drilling, marking and cutting at different angles on aluminum and PVC profiles",
         "10 high-speed air-cooled spindle motors for aluminum; precision 3-axis profile holding station",
         "Profile magazine for 7 profiles; automatic profile length detection",
         "Servo-controlled Ø21-5/8″ (550 mm) cutting unit, 30° – 150°, ±0.1°",
         "Waiting station for processed profiles; outlet belt conveyor; barcode printer; automatic waste conveyor to the cart",
         "23.8″ touch screen, Windows-based software; USB data transfer; online remote monitoring and remote support; UPS",
         CE, VOLT],
        ["Compatibility with CAM programs", "Optional profile length", "Safety barrier (sensor)", VOLT_OPT],
        ["pm-4550", "pm-4550-spindles", "pm-4550-heads", "pm-4550-saw", "pm-4550-printer", "pm-4550-outfeed", "pm-4550-station"],
        spec(T_4550, {"SÇ 4550": [f"Profiles {inch(2000)} – {inch(6500)}", "9 axes, 10 spindles", f"{hpv(38)} HP", f"{cfmv(500)} CFM", lbv(3750)]},
             caps={"SÇ 4550": "9 axes, 10 spindles"})),
    fam("plastmak-5000", "pm-cnc", P_CNC,
        "SÇ 5000 · SÇ 5000S 3-axis CNC drilling and milling machines, travel 15-3/8 × 7-7/8 × 7-7/8″", "SÇ 5000 · SÇ 5000S",
        "SÇ 5000 · SÇ 5000S · 2 models",
        "Three-axis CNC machines that do the hardware work of a window on one station: lock and handle places, hinge and "
        "espagnolette slots, barrel holes, triple drilling and drainage slots, with three spindles at 18,000 rpm on servo axes "
        "travelling 15-3/8 × 7-7/8 × 7-7/8″ (390 × 200 × 200 mm). The SÇ 5000 is for PVC — door, sash and sliding work, "
        "point-to-point programming, inside drainage slots, measuring arms with stops and laser centring. The SÇ 5000S takes "
        "aluminum and PVC: three independent 1.9 HP spindles, a 19″ Windows screen with DXF import and CAM Codex, on-screen "
        "simulation, cooling for aluminum, an automatic safety cover and a wider working area; switching between aluminum and "
        "PVC on the touch screen changes every speed by itself.",
        "3 axes · 3 spindles at 18,000 rpm · travel 15-3/8 × 7-7/8 × 7-7/8″",
        ["Door, sash, handle-cylinder (barrel) and triple drilling on one station; drainage slots",
         "3 spindles at 18,000 rpm on X, Y and Z servo axes, travel 15-3/8 × 7-7/8 × 7-7/8″ (390 × 200 × 200 mm)",
         "Right and left measuring arms with stops; laser centring; unlimited memory",
         "SÇ 5000: PVC profiles, easy point-to-point programming",
         "SÇ 5000S: aluminum and PVC; 19″ Windows screen, DXF import and drawing with CAM Codex; process simulation on screen",
         "SÇ 5000S: cooling for aluminum; aluminum / PVC switch on the touch screen; linear guides; automatic lubrication; "
         "automatic safety cover; remote support",
         CE, VOLT],
        [VOLT_OPT],
        ["pm-5000", "pm-5000s", "pm-5000-screen", "pm-5000-spindles", "pm-5000-inside", "pm-5000-heads", "pm-5000s-screen",
         "pm-5000s-console", "pm-5000s-spindles", "pm-5000s-inside", "pm-5000s-clamp", "pm-5000s-table"],
        spec(T_5000, {"SÇ 5000": [f"Travel {inch(390)[:-1]} × {inch(200)[:-1]} × {inch(200)}", "PVC, 3 spindles", f"{hpv(6)} HP", f"{cfmv(9)} CFM", lbv(355)],
                      "SÇ 5000S": [f"Travel {inch(390)[:-1]} × {inch(200)[:-1]} × {inch(200)}", "Aluminum & PVC, 3 spindles", f"{hpv(6)} HP", f"{cfmv(9)} CFM", lbv(750)]},
             caps={"SÇ 5000": "3-axis CNC for PVC", "SÇ 5000S": "3-axis CNC for aluminum and PVC"})),
    fam("plastmak-copy", "pm-copy", P_CNC,
        "SÇ 501 · 502S · 512 · 521S · 542 copy routers, travel 11 × 4-15/16 × 3-9/16″", "SÇ 501 · 502S · 512 · 521S · 542",
        "SÇ 501 · 502S · 512 · 521S · 542 · 5 models",
        "A copy router follows a template with a stylus while the router cuts the same shape into the profile — the quick, "
        "simple way to make lock, handle and hinge cut-outs and drainage slots in series. On the SÇ 501 (PVC, 12,000 rpm), "
        "SÇ 502S and SÇ 512 (aluminum and PVC, 18,000 rpm) the copy head works on the vertical axis and a triple drilling unit on "
        "the horizontal one, each able to run on its own; a universal template comes with them and special templates can be made. "
        "The SÇ 521S opens water drainage slots with three independent 18,000 rpm routers that can work angled, over a table "
        "that moves right and left. The SÇ 542 is the aluminum router: an 18,000 rpm spindle, oil cooling and a template system "
        "made for aluminum handle, lock and hardware slots. All travel 11 × 4-15/16 × 3-9/16″ (280 × 125 × 90 mm).",
        "Travel 11 × 4-15/16 × 3-9/16″ · 12,000 – 18,000 rpm · triple drilling (501 · 502S · 512)",
        ["Copy head on the vertical axis, triple drilling unit on the horizontal axis (SÇ 501 · 502S · 512); each works on its own",
         "Universal template; templates made to order",
         "Water drainage slots, also angled (SÇ 501 · 502S · 521S)",
         "High-frequency 18,000 rpm routers (SÇ 502S · 512 · 521S · 542); cooling on the SÇ 512, oil cooling on the SÇ 542",
         "SÇ 521S: three routers working separately or together, pneumatic clamping, fully automatic cycle",
         "Right conveyor 3′ 3″ (1 m) on the SÇ 502S, 512 and 542; dual support system on the SÇ 502S",
         CE, VOLT],
        ["Optional templates", VOLT_OPT],
        ["pm-501", "pm-502s", "pm-512", "pm-521s", "pm-542", "pm-501-drill", "pm-501-head", "pm-502-panel", "pm-502-template",
         "pm-502-top", "pm-512-head", "pm-521s-heads", "pm-521s-table", "pm-542-spindle", "pm-542-template", "pm-542-head",
         "pm-542-clamp", "pm-542-top"],
        spec(T_COPY, {"SÇ 501": [f"Travel {inch(280)[:-1]} × {inch(125)[:-1]} × {inch(90)}", "PVC, triple drilling", f"{hpv(2.5)} HP", f"{cfmv(9)} CFM", lbv(115)],
                      "SÇ 502S": [f"Travel {inch(280)[:-1]} × {inch(125)[:-1]} × {inch(90)}", "Aluminum & PVC, triple drilling", f"{hpv(3)} HP", f"{cfmv(9)} CFM", lbv(130)],
                      "SÇ 512": [f"Travel {inch(280)[:-1]} × {inch(125)[:-1]} × {inch(90)}", "Aluminum & PVC, triple drilling", f"{hpv(1.5)} HP", f"{cfmv(9)} CFM", lbv(110)],
                      "SÇ 521S": ["3 drainage-slot routers", "PVC", f"{hpv(3)} HP", f"{cfmv(9)} CFM", lbv(140)],
                      "SÇ 542": [f"Travel {inch(280)[:-1]} × {inch(125)[:-1]} × {inch(90)}", "Aluminum", f"{hpv(1.4)} HP", f"{cfmv(9)} CFM", lbv(90)]},
             caps={"SÇ 501": "PVC copy router, triple drilling", "SÇ 502S": "18,000 rpm copy router", "SÇ 512": "3-hole copy router",
                   "SÇ 521S": "3 drainage-slot routers", "SÇ 542": "aluminum copy router"}),
        vids(("eSDM6QInOfs", "SÇ 501 copy router making hardware cut-outs"), ("phyPgKa6BxE", "SÇ 502S copy router, 3 spindles"))),
    fam("plastmak-211", "pm-endmill", P_CNC,
        "SÇ 211 · SÇ 211S end milling machines, cutters to Ø6-5/16″", "SÇ 211 · SÇ 211S", "SÇ 211 · SÇ 211S · 2 models",
        "An end milling machine shapes the end of a mullion (transom) to the contour of the frame profile it butts against, so "
        "the joint closes tight. The SÇ 211 mills PVC and aluminum mullions with a stack of cutters up to Ø5-1/2″ (140 mm) and "
        "3-9/16″ (90 mm) high: two vertical and one horizontal vise hold the profile, a pneumatic cylinder moves the milling motor, "
        "and a separator button switches between profile series. The heavier SÇ 211S mills aluminum to high quality from −45° to "
        "+45° on mechanical stops, with cutters up to Ø6-5/16″ (160 mm) and a second 7-7/8″ (200 mm) stack; a whole cutter group "
        "changes with one button and three more wait on the rack, the support adjusts to four profiles, the feed is hydro-"
        "pneumatic and a boron-oil spray cools the cut.",
        "Cutters to Ø6-5/16″ · stack to 3-9/16″ + 7-7/8″ · ±45° (SÇ 211S)",
        ["End milling of mullion (transom) connections on PVC and aluminum profiles",
         "SÇ 211: 2 vertical and 1 horizontal vise, pneumatic profile clamping; milling motor moved by a pneumatic cylinder",
         "SÇ 211: easy series change with the separator button (60 – 70 series)",
         "SÇ 211S: −45° to +45° with mechanical angle stops; cutter groups changed with a single button; rack for 3 groups",
         "SÇ 211S: support adjustable for four profiles; hydro-pneumatic cutting speed; boron-oil spray",
         CE, VOLT],
        ["Hydro-check feed (SÇ 211)", "Cooling system (SÇ 211)", VOLT_OPT],
        ["pm-211", "pm-211s", "pm-211-front", "pm-211-vises", "pm-211-cutters", "pm-211-stack", "pm-211s-change"],
        spec(T_211, {"SÇ 211": [f"Cutters to Ø{inch(140)}", "PVC & aluminum", f"{hpv(1.1)} HP", f"{cfmv(10)} CFM", lbv(100)],
                     "SÇ 211S": [f"Cutters to Ø{inch(160)}, ±45°", "Aluminum & PVC", f"{hpv(1.1)} HP", f"{cfmv(10)} CFM", lbv(155)]},
             caps={"SÇ 211": "end milling, 2 knives", "SÇ 211S": "end milling, serial blade change"})),

    # ------------------------------------------------------------------------------------------ assembly, portable, conveyors
    fam("plastmak-902", "pm-crimp", P_ASSY,
        "SÇ 902 hydraulic corner crimping machine for aluminum, profiles to 5-1/8″ high", "SÇ 902", "SÇ 902 · 1 model",
        "Aluminum window and door frames are joined at the corner with a cleat inside the profile; the corner crimper presses "
        "knives into the profile walls over the cleat and locks the 90° joint. On the SÇ 902 both knife movements are hydraulic, "
        "4 knives on the right and 4 on the left, with millimetre scales for knife height and advance, a pneumatic centring miter "
        "wedge, and a release button for fine adjustment. Two foot pedals work the hydraulic press and the profile clamp, "
        "plexiglass protects the profile faces, and arms on both sides carry the frame. Profiles up to 5-1/8″ (130 mm) high.",
        "4 + 4 hydraulic knives · profiles to 5-1/8″ high · 2 × 3,307 lbf",
        ["Hydraulic movement of both knife sets; 4 right and 4 left knives",
         "Millimetre scales for knife height and advance; release button for precise adjustment",
         "Pneumatic centring miter wedge; 2 foot pedals for the hydraulic press and the profile clamp",
         "Plexiglass sheet protects the profile faces; right and left support arms",
         CE, VOLT],
        [VOLT_OPT],
        ["pm-902", "pm-902-table", "pm-902-heads", "pm-902-knives", "pm-902-scale", "pm-902-wedge", "pm-902-cylinder"],
        spec(T_902, {"SÇ 902": ["Aluminum 90° corners", f"Profiles to {inch(130)} high", f"{hpv(2.2)} HP", f"{cfmv(20)} CFM", lbv(360)]},
             caps={"SÇ 902": "hydraulic corner crimper"})),
    fam("plastmak-screw", "pm-screw", P_ASSY,
        "Screwing machines and sash assembly machine, screws to 4.2 × 38 mm", "Screwing & sash assembly",
        "Single screwing · double-head screwing · sash assembly · 3 machines",
        "Assembly stations for the steps after the frame is welded or crimped. The single screwing machine drives screws from 3.9 "
        "× 16 mm to 4.2 × 38 mm with a pneumatic motor and stable torque control, its working range set between 1.6″ and 4.7″ and "
        "its cycle started by a foot pedal — compact enough to slot into a line, fed by an automatic screw feeder. The double-head "
        "screwing machine drives two screws at once into PVC and aluminum profiles. The sash assembly machine fits single and "
        "double opening hardware in series without moulds or templates: laser alignment, automatic measuring and screwing, a "
        "three-arm drilling unit, a hinge template and an espagnolette groove cutter — 3.5 minutes on average for a double "
        "opening window.",
        "Screws 3.9 × 16 to 4.2 × 38 mm · double-opening sash in 3.5 min",
        ["Single screwing: pneumatic screwing system with precise torque control; adjustable working range (A – B); foot pedal",
         "Single screwing: works with an automatic screw feeding unit; compact, ergonomic and easy to maintain",
         "Double-head screwing: two pneumatic screwing motors driving at the same time, PVC and aluminum profiles",
         "Sash assembly: series work on different profiles, single and double opening hardware, no moulds or templates",
         "Sash assembly: fully automatic laser-aligned screwing; automatic measuring; triple-arm drilling with support plate",
         "Sash assembly: semi-automatic hinge template; espagnolette grooving cutter; lit hardware shelf; corner-turning scissors",
         "Compressed air required; RAL 7035 grey"],
        [],
        ["pm-screw-single", "pm-screw-double", "pm-sash", "pm-screw-motor"],
        spec(T_SCREW, {"Single screwing machine": ["Working range 1.6 – 4.7″", "Screws 3.9 × 16 – 4.2 × 38 mm", "0.7 HP motor", "—", "276 lb"],
                       "Double-head screwing machine": ["Two heads", "Screws to 4.2 × 38 mm", "2 × 0.7 HP motors", "—", "463 lb"],
                       "Sash assembly machine": ["Double sash in 3.5 min", "Hardware fitting and screwing", "—", "—", "—"]},
             NOTE_NT, caps={"Single screwing machine": "pneumatic, foot pedal", "Double-head screwing machine": "two heads at once",
                            "Sash assembly machine": "laser alignment, automatic screwing"})),
    fam("plastmak-portable", "pm-portable", P_ASSY,
        "SÇ 221 · SÇ 551 portable notching and copy milling machines", "SÇ 221 · SÇ 551", "SÇ 221 · SÇ 551 · stand · 2 machines",
        "Bench machines for small shops, site work and the jobs a production line does not cover. The SÇ 221 notches the ends of "
        "aluminum and PVC mullions (transoms) to fit the frame, holding the profile in vertical and horizontal vises, with a "
        "single-phase motor. The SÇ 551 copy-mills lock, handle, hinge and espagnolette slots and grooves of any size in aluminum "
        "and PVC profiles, from a copy template made for the job — or, against its stop, grooves of many kinds without a template. "
        "A two-shelf steel stand carries them, and a lower cabinet and an air system are available for both.",
        "Mullion notching (SÇ 221) · copy milling of hardware slots (SÇ 551)",
        ["SÇ 221: mullion (transom) notching of aluminum and PVC profiles; vertical and horizontal vises; single-phase motor",
         "SÇ 551: lock, handle, hinge and espagnolette slots and grooves of any size, aluminum and PVC",
         "SÇ 551: copy device suited to your job; grooving independent of the copy template with the help of the stop",
         "Two-shelf steel stand for the portable machines"],
        ["Lower cabinet", "Pneumatic (air) system"],
        ["pm-221", "pm-551", "pm-table"],
        spec(T_PORTABLE, {"SÇ 221": ["Mullion notching", "Aluminum & PVC", "Single-phase", "—", "—"],
                          "SÇ 551": ["Copy milling of hardware slots", "Aluminum & PVC", "—", "—", "—"]},
             NOTE_NT.replace("Figures as listed in NovoTech's Plastmak catalogue. ", ""), caps={"SÇ 221": "portable notcher", "SÇ 551": "portable copy mill"},
             models=["SÇ 221", "SÇ 551"])),
    fam("plastmak-conveyor", "pm-portable", P_ASSY,
        "SÇ 1000 digital measuring conveyor, 9′ 10″, ±.020″, and SÇ 1001 – 1003 roller conveyors", "SÇ 1000 · 1001 · 1002 · 1003",
        "SÇ 1000 · 1001 · 1002 · 1003 · 4 models",
        "Conveyors carry long profiles to and from the saws and machines at table height. The SÇ 1000 is a digital measuring "
        "conveyor: 9′ 10″ (3 m) long, it sets its stop to the length entered on the touch screen to ±.020″ (±0.5 mm), retracts "
        "the stop at one push so the cut piece comes out freely, calibrates easily and fits any of the saws, on a 220 V "
        "single-phase supply. The SÇ 1001 (aluminum rollers), SÇ 1002 (plastic rollers, kind to finished profiles) and SÇ 1003 "
        "(sheet-metal track) are plain support conveyors on height-adjustable legs.",
        "Measuring length 9′ 10″ (3 m) · ±.020″ (±0.5 mm) · roller and sheet conveyors",
        ["SÇ 1000: 9′ 10″ (3 m) digital measuring conveyor, ±.020″ (±0.5 mm), touch screen",
         "SÇ 1000: stop retracts at one push to free the cut piece; easy to fit to all the machines; easy calibration",
         "SÇ 1000: works on a 220 V single-phase supply",
         "SÇ 1001: aluminum roller track · SÇ 1002: plastic roller track · SÇ 1003: sheet-metal profile track",
         "Height-adjustable legs"],
        ["Bluetooth measuring station (SÇ 1000)"],
        ["pm-1000", "pm-1000-panel", "pm-1001", "pm-1002", "pm-1003"],
        spec(T_CONV, {"SÇ 1000": [f"Measuring length {ftin(3000).split(' (')[0]}", "±.020″ (±0.5 mm)", "220 V 1-phase", "—", "—"],
                      "SÇ 1001": ["Aluminum roller conveyor", "—", "—", "—", "—"],
                      "SÇ 1002": ["Plastic roller conveyor", "—", "—", "—", "—"],
                      "SÇ 1003": ["Sheet-metal conveyor", "—", "—", "—", "—"]},
             NOTE.replace(" Air consumption is at 87 – 116 psi (6 – 8 bar). Weights are approximate.", ""),
             caps={"SÇ 1000": "digital measuring conveyor"}),
        vids(("jpJMgI3VL4w", "SÇ 1000 programmable length stop on an upcut saw"), ("DVVKKS4_RqE", "SÇ 1000 9′ 10″ NC length stop table"))),

    # ------------------------------------------------------------------------------------------ production groups
    fam("plastmak-line-pvc1", "pm-lines", P_LINES,
        "PVC single-head production group, 40 – 60 windows a shift", "PVC single-head group", "6 machines · 40 – 60 windows a shift",
        "The starting set for a PVC window shop, built around single-head machines for a continuous flow: the SÇ 401 upcut saw "
        "cuts the profiles, the SÇ 501 copy router opens lock places, handle holes and drainage slots, the SÇ 101 welds the "
        "corners one at a time, the SÇ 601 cleans them, the SÇ 211 end-mills the mullions and the SÇ 301 cuts the glazing beads. "
        "Together they make 40 to 60 windows in an 8-hour shift.",
        "6 machines · 40 – 60 windows in an 8-hour shift",
        ["Cutting: SÇ 401 upcut saw, Ø17-11/16″ (450 mm), 0° – 180°",
         "Copy routing, triple drilling and drainage slots: SÇ 501",
         "Welding: SÇ 101 single-head welder, 25° – 180° · corner cleaning: SÇ 601, 3 knives",
         "Mullion end milling: SÇ 211 · glazing beads: SÇ 301",
         "Machines can be changed or added — ask us for a layout of your shop"],
        [],
        ["pm-line-pvc1", "pm-401", "pm-501", "pm-101", "pm-301", "pm-211", "pm-601"],
        line_spec("pm-line-pvc1")),
    fam("plastmak-line-pvc2", "pm-lines", P_LINES,
        "PVC double-head production group, 80 – 120 windows a shift", "PVC double-head group", "6 machines · 80 – 120 windows a shift",
        "The same flow with double-head machines for higher volumes: the SÇ 400S double-head saw cuts both ends of each profile "
        "in one stroke and the SÇ 100 welds two corners at a time, with the SÇ 501 copy router, SÇ 601 corner cleaner, SÇ 211 "
        "end mill and SÇ 301 bead saw around them — 80 to 120 windows in an 8-hour shift.",
        "6 machines · 80 – 120 windows in an 8-hour shift",
        ["Cutting: SÇ 400S double-head saw, 2 × Ø19-11/16″ (500 mm)",
         "Copy routing, triple drilling and drainage slots: SÇ 501",
         "Welding: SÇ 100 double-head welder · corner cleaning: SÇ 601",
         "Mullion end milling: SÇ 211 · glazing beads: SÇ 301",
         "Machines can be changed or added — ask us for a layout of your shop"],
        [],
        ["pm-line-pvc2", "pm-400s", "pm-501", "pm-100", "pm-301", "pm-211", "pm-601"],
        line_spec("pm-line-pvc2")),
    fam("plastmak-line-alu", "pm-lines", P_LINES,
        "Aluminum double-head production group, 80 – 120 windows a shift", "Aluminum double-head group", "4 machines · 80 – 120 windows a shift",
        "A group for aluminum windows and doors, built around a double-head saw and a 3-axis CNC: the SÇ 4000S cuts the profiles, "
        "the SÇ 5000S drills and mills the hardware places, the SÇ 211S end-mills the mullions and the SÇ 902 crimps the corners "
        "— 80 to 120 windows in an 8-hour shift.",
        "4 machines · 80 – 120 windows in an 8-hour shift",
        ["Cutting: SÇ 4000S servo double-head saw, 2 × Ø23-5/8″ (600 mm)",
         "Drilling and milling: SÇ 5000S 3-axis CNC for aluminum and PVC",
         "Mullion end milling: SÇ 211S, ±45° · corner crimping: SÇ 902 hydraulic",
         "Machines can be changed or added — ask us for a layout of your shop"],
        [],
        ["pm-line-alu", "pm-4000s", "pm-5000s", "pm-211s", "pm-902"],
        line_spec("pm-line-alu")),
    fam("plastmak-line-shop", "pm-lines", P_LINES,
        "PVC window workshop set-up, 200 – 220 windows a shift", "PVC window workshop", "7 machines · 200 – 220 windows a shift",
        "A complete PVC window workshop laid out as a production loop: compressed air from the SÇ 801, double-head cutting on the "
        "SÇ 400S, CNC drilling and milling on the SÇ 5000, double-corner welding on the SÇ 100, CNC corner cleaning on the SÇ "
        "6000, end milling on the SÇ 211S and bead cutting on the SÇ 301S — 200 to 220 windows in an 8-hour shift.",
        "7 machines · 200 – 220 windows in an 8-hour shift",
        ["Compressed air: SÇ 801 compressor, 130 gal (500 l)",
         "Cutting: SÇ 400S double-head saw · CNC drilling and milling: SÇ 5000",
         "Welding: SÇ 100 double-head welder · corner cleaning: SÇ 6000 CNC",
         "Mullion end milling: SÇ 211S · glazing beads: SÇ 301S, 12 beads without moulds",
         "Laid out as a loop so the profiles travel the shortest way — ask us for a layout of your shop"],
        [],
        ["pm-line-shop", "pm-compressor", "pm-400s", "pm-5000", "pm-100", "pm-6000", "pm-211s", "pm-301s"],
        line_spec("pm-line-shop")),
]

# NovoTech's own videos of these machines
VIDEOS = {
    "plastmak-401": [("6_KfOwCxUwk", "SÇ 401 upcut saw for aluminum and PVC extrusions"), ("zai1zC0QZ0Q", "SÇ 401 upcut saw, Ø17-11/16″ (450 mm)")],
    "plastmak-402-403": [("F9VBp0QD91E", "SÇ 402 cutting aluminum profiles"), ("PRLhsXYBvfc", "SÇ 402 upcut saw"),
                         ("LJSwkkCeFMg", "SÇ 402 with Ø21-5/8″ (550 mm) blade"), ("ueqIxB1KMfE", "SÇ 402 automatic upcut saw at work")],
    "plastmak-double": [("4joDJ1kUi00", "SÇ 400 double-head saw with NC control"), ("DLE1zG6NJVA", "SÇ 4000S fully automatic double-head saw"),
                        ("CBYNMAwzDGw", "SÇ 4000S PLUS with Ø23-5/8″ (600 mm) blades")],
}
for _f in FAMILIES:
    if _f["id"] in VIDEOS:
        _f["videos"] = vids(*VIDEOS[_f["id"]])


def families(page=None):
    return [f for f in FAMILIES if page is None or f["page"] == page]
