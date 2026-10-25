#!/usr/bin/env python3
"""Wecotech (Switzerland) tube end forming machines — families for tube-end-forming-machines.html, below the ISITAN SFF.

Metric data transcribed from the Wecotech tube-end-forming catalogue (English, 20 May 2022; /home/claude/wecotech/cat.pdf,
pages 8 – 63) and shown as imperial (metric).  The catalogue's four lines are kept as groups: Easy (compact entry-level
expanders / reducers), Universal (modular production machines), Traditional (for the C and IO tooling that is standard
in the exhaust trade) and Weco (the CNC inner / outer formers); the tube cutting, shearing and deburring machines that
share the end-forming cell are a fifth group.  The Spiralmatic-Flex strip-wound hose machine sits in the Universal line.
"""
P_FORM = "tube-end-forming-machines"
BRAND = "wecotech"

HP = {0.25: "1/3", 4.0: "5.5", 5.5: "7.5", 7.5: "10", 11.0: "15"}


def fmt(v, nd=1):
    s = f"{v:,.{nd}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def inch(mm, nd=1):
    return f"{fmt(mm / 25.4, nd)}″ ({mm:,g} mm)"


def rng(a, b, nd=1):
    """Ø range 20 – 600 mm → '0.8 – 23.6″ (20 – 600 mm)'."""
    return f"{fmt(a / 25.4, nd)} – {fmt(b / 25.4, nd)}″ ({a:g} – {b:g} mm)"


def dia(a, b):
    return "Ø" + rng(a, b)


def tons(t):
    return f"{fmt(t * 1.10231, 0)} US tons ({t:g} t)"


def hp(kw, n=1):
    h = HP[float(kw)]
    return (f"{n} × {h} HP ({n} × {kw:g} kW)" if n > 1 else f"{h} HP ({kw:g} kW)")


def psi(bar):
    if isinstance(bar, str):      # '160/220'
        a, b = bar.split("/")
        return f"{round(float(a) * 14.5038, -1):,.0f} / {round(float(b) * 14.5038, -1):,.0f} psi ({a} / {b} bar)"
    return f"{round(bar * 14.5038, -1):,.0f} psi ({bar:g} bar)"


def gal(l):
    return f"{fmt(l * 0.264172, 0)} US gal ({l:g} L)"


def gpm(l):
    return f"{fmt(l * 0.264172, 1)} gpm ({l:g} L/min)"


def dims(l, w, h):
    return f"{l / 25.4:.0f} × {w / 25.4:.0f} × {h / 25.4:.0f}″ ({l:,} × {w:,} × {h:,} mm)"


def weight(kg):
    return f"{round(kg * 2.20462):,} lb ({kg:,} kg)"


def ftmin(a, b):
    return f"{a * 3.28084:g} – {b * 3.28084:,.0f} ft/min ({a:g} – {b:g} m/min)"


def ins(mm_s):
    return f"{mm_s / 25.4:.2f} in/s ({mm_s:g} mm/s)"


def table(title, sub, models, rows):
    """rows: [(label, [cells], key)]; a cell may be the same string for every model when a single value is given."""
    out = []
    for lab, cells, key in rows:
        if isinstance(cells, str):
            cells = [cells] * len(models)
        out.append({"label": lab, "sub": "", "cells": cells, "key": key})
    return {"title": title, "sub": sub, "models": models, "rows": out}


GK = ["tube_diameter", "forming_length", "force", "cycle", "weight"]
G_FROM = ["Tube diameter", "Max forming length", "Lifting force", "Mean cycle time", "Weight"]
NOTE = ("Working ranges marked by the maker as tool-dependent are given for the standard tooling; the forming length, the "
        "expansion or reduction per stroke and the cycle time change with the tool. Metric values in brackets are the "
        "manufacturer's nominal figures; dimensions are L × W × H. Machines are built for 400 V 50 Hz and are supplied for the "
        "Canadian supply voltage with a CSA-approved panel.")


def spec(tables, note=NOTE):
    models = []
    for t in tables:
        rr = {r["label"]: r["cells"] for r in t["rows"]}
        for i, m in enumerate(t["models"]):
            models.append({"name": m, "glance": [rr[l][i] if l in rr else "—" for l in G_FROM]})
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": GK, "caps": {}, "note": note}


HYD_EASY = [("Hydraulic tank", gal(50), False), ("Pump flow", gpm(13), False), ("Working pressure", psi(240), False), ("Motor power", hp(4), False)]
HYD_U = [("Hydraulic tank", gal(63), False), ("Pump flow", gpm(16), False), ("Working pressure", psi(300), False), ("Motor power", hp(5.5), False)]
CTRL_EASY = ["Siemens PLC; set-up mode (forming stroke while the foot switch is pressed) and production mode (one tap starts the cycle)",
             "Pre-selectable number of forming and calibrating steps", "Forward and return stroke set on a hand wheel with scale",
             "Compact housing with the electrics and hydraulics built in", "Bosch Rexroth 24 V valves; energy-saving feature; safety foot switch"]
OPT_EASY_CTRL = ["4″ colour touchscreen with position sensor: macro programming, 200 numerical programs, log-in levels, workpiece and hours counters, offset"]
CTRL_U = ["Siemens PLC with 4″ colour touchscreen on a pivot arm and position sensor: macro programming, set-up / manual / production modes, log-in levels, workpiece and hours counters, offset",
          "HW-Flex universal housing with the hydraulic unit bolted on and room in the electrical cabinet", "Bosch Rexroth 24 V valves; energy-saving feature; safety foot switch"]
OPT_U_CTRL = ["7″ colour touchscreen, 200 alphanumerical programs, USB program transfer, remote maintenance module, program protection key switch",
              "Digital I/O and Profisafe interfaces; lubricant, oil level / temperature and filter monitors", "Oil / air or oil / water heat exchanger; 15 HP (11 kW) power increase with 25 L/min pump",
              "Air-conditioned control cabinet; individually labelled cables; special electrical connection"]
VOLT_OPT = "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"

# ----------------------------------------------------------------------------------------------- Easy line
TUBEX = table("Tubex", "Compact tube end expander", ["Tubex"], [
    ("Tube diameter", dia(20, 600), True), ("Max forming length", inch(100) + " (150 mm optional)", True), ("Max tube wall thickness", inch(4, 2), False),
    ("Axial stroke", inch(100) + " · piston Ø100 mm", False), ("Lifting force", tons(19), True), ("Expansion per stroke (5° cone)", "Ø max " + inch(17, 2) + " (Ø26 mm with the 150 mm stroke)", False),
    ("Mean cycle time", "~2 s", True)] + HYD_EASY + [("Working position", "vertical (horizontal version optional)", False), ("Dimensions L × W × H", dims(1140, 530, 880), False), ("Weight", weight(400), False)])
TUBIN = table("Tubin", "Compact tube end reducer (impander)", ["Tubin 150", "Tubin 200"], [
    ("Tube diameter", [dia(10, 140), dia(10, 190)], True), ("Max forming length", inch(100), True), ("Max tube wall thickness", inch(4, 2), False),
    ("Axial stroke", inch(100) + " · piston Ø100 mm", False), ("Lifting force", tons(19), True), ("Reduction per stroke", "Ø max " + inch(14, 2), False),
    ("Mean cycle time", "~4 s", True)] + HYD_EASY + [("Working position", "vertical (horizontal version optional)", False), ("Dimensions L × W × H", dims(930, 570, 870), False), ("Weight", weight(450), False)])
TUBEPRESS = table("Tubepress", "Tube straightening press", ["Tubepress"], [
    ("Tube diameter", dia(20, 160), True), ("Max forming length", "adjustable depth stop", True), ("Axial stroke", inch(150) + " · piston Ø100 mm", False),
    ("Lifting force", tons(19), True), ("Mean cycle time", "~2 s", True)] + HYD_EASY + [("Dimensions L × W × H", dims(750, 550, 1350), False), ("Weight", weight(260), False)])
TUBEPUNCH = table("Tubepunch", "Tube end punching unit", ["Tubepunch"], [
    ("Tube diameter", "from " + inch(20, 1), True), ("Max forming length", "—", True), ("Max tube wall thickness", inch(4, 2), False), ("Punch stroke", inch(13, 2) + " · piston Ø70 mm", False),
    ("Lifting force", tons(9), True), ("Mean cycle time", "~0.3 s per punch", True)] + HYD_EASY + [("Working position", "horizontal", False), ("Dimensions L × W × H", dims(700, 500, 1200), False), ("Weight", weight(300), False)])

# ----------------------------------------------------------------------------------------------- Universal line
TUBEX_U = table("Tubex-U", "Universal production expander", ["Tubex-U"], [
    ("Tube diameter", "from " + inch(20) + " · supporting table to Ø" + inch(500), True), ("Max forming length", "100 / 150 / 200 / 300 / 400 mm standard tool lengths (3.9 – 15.7″)", True),
    ("Max tube wall thickness", inch(8, 2), False), ("Axial stroke", inch(150) + " · piston Ø100 mm", False), ("Lifting force", tons(24) + " · " + tons(34) + " with the Ø120 piston option", True),
    ("Expansion per stroke (7° cone)", "Ø max " + inch(36, 2), False), ("Mean cycle time", "~3 s", True)] + HYD_U +
    [("Working position", "vertical (horizontal version optional)", False), ("Dimensions L × W × H", dims(1200, 875, 950), False), ("Weight", weight(600), False)])
TUBIN_U = table("Tubin-U", "Universal production reducer (impander)", ["Tubin-U 150", "Tubin-U 200"], [
    ("Tube diameter", [dia(10, 140), dia(10, 190)], True), ("Max forming length", inch(100) + " (200 mm optional)", True), ("Max tube wall thickness", inch(8, 2), False),
    ("Axial stroke", inch(150) + " · piston Ø100 mm", False), ("Lifting force", tons(24) + " · 34 or 60 t pistons optional", True), ("Reduction per stroke", "Ø max " + inch(21, 2), False),
    ("Mean cycle time", "~3 s", True)] + HYD_U + [("Working position", "vertical (horizontal version optional)", False), ("Dimensions L × W × H", dims(1200, 875, 950), False), ("Weight", weight(650), False)])
TUBAX_U = table("Tubax-U", "Axial forming machine with tube clamping", ["Tubax-U 200", "Tubax-U 300"], [
    ("Tube diameter", [dia(10, 200), dia(10, 300)], True), ("Max forming length", [inch(100), inch(200)], True), ("Max clamping length", [inch(200), inch(400)], False),
    ("Max tube wall thickness", inch(4, 2), False), ("Axial stroke", inch(150), False), ("Lifting force", [tons(24) + " (Ø100 piston)", tons(34) + " (Ø120 piston)"], True),
    ("Clamping stroke / force", [inch(100) + " · " + tons(34), inch(100) + " · " + tons(68) + " (2 × Ø120)"], False), ("Mean cycle time", ["~5 s", "~8 s"], True)] + HYD_U +
    [("Working position", "horizontal", False), ("Dimensions L × W × H", dims(1200, 875, 1400), False), ("Weight", weight(600), False)])
TUBAX_ROTARY = table("Tubax-Rotary Electra", "Servo-electric rotary forming machine", ["Tubax-Rotary 200", "Tubax-Rotary 400"], [
    ("Tube diameter", [dia(40, 200), dia(40, 400)], True), ("Max forming length", "—", True), ("Max clamping length", [inch(100), inch(250)], False), ("Axial stroke", [inch(150), inch(300)], False),
    ("Clamping stroke", inch(150), False), ("Lifting force", "servo-electric axial and clamping drives", True), ("Surface quality", "< Ra 0.2 on sealing faces", False), ("Mean cycle time", ["~10 s", "~20 s"], True),
    ("Working position", "horizontal", False), ("Dimensions L × W × H", dims(1800, 550, 1880), False), ("Weight", weight(1500), False)])
TUBAX_MULTI = table("Tubax-Multi Electra", "Multi-station axial forming centre", ["Tubax-Multi"], [
    ("Tube diameter", dia(10, 160), True), ("Max forming length", "—", True), ("Max clamping length", inch(180), False), ("Axial stroke / force", inch(300) + " · " + tons(36), False),
    ("Clamping stroke / force", inch(100) + " · " + tons(36), False), ("Lifting force", tons(36), True), ("Tool stations", "5 axial mandrels or milling heads on a servo tool changer", False),
    ("Mean cycle time", "~40 s", True), ("Working position", "horizontal", False), ("Dimensions L × W × H", dims(2000, 2200, 2100), False), ("Weight", weight(4000), False)])
TUBIROLL = table("Tubiroll-2R", "Automatic beading and flanging machine", ["Tubiroll-2R 600", "Tubiroll-2R 1000"], [
    ("Tube diameter", [dia(40, 600), dia(40, 1000)], True), ("Max forming length", inch(100) + " rolling length (200 mm optional)", True), ("Max tube wall thickness", inch(2, 3), False),
    ("Max beading depth", inch(15, 2), False), ("Peripheral speed", ftmin(0, 75), False), ("Roller feed", "0 – " + ins(3) + " · rapid " + ins(12), False),
    ("Lifting force", "—", True), ("Mean cycle time", "~8 s (10 mm bead on Ø200 mm)", True), ("Hydraulic tank", gal(63), False), ("Roll drive", "0 – " + gpm(20) + " at " + psi(140), False),
    ("Motor power", hp(5.5), False), ("Compressed air", "87 psi (6 bar)", False), ("Dimensions L × W × H", dims(1250, 880, 2600), False), ("Weight", weight(500), False)])

SPIRALMATIC = table("Spiralmatic-Flex", "Strip-wound flexible hose machine", ["Spiralmatic-Flex"], [
    ("Tube diameter", "hose " + dia(50, 200), True), ("Max forming length", "—", True), ("Strip thickness", inch(0.4, 3), False), ("Strip width", inch(50), False),
    ("Strip speed", "82 ft/min (25 m/min)", False), ("Lifting force", "—", True), ("Mean cycle time", "continuous winding", True),
    ("Hemming and seaming units", "7 stations each, pitch angle adjustable; hydraulic lifting cylinders on the seaming rollers", False), ("Motor power", "2 × " + hp(4), False),
    ("Dimensions L × W × H", dims(3300, 1100, 1750), False), ("Weight", weight(1800), False)])

# ----------------------------------------------------------------------------------------------- Traditional line
TUBIMATIC_C = table("Tubimatic C", "For commercially available C-tools", ["Tubimatic C 80 UNO", "Tubimatic C 80 TRE", "Tubimatic C 160 UNO"], [
    ("Tube diameter", [dia(20, 80) + " expand · " + dia(10, 80) + " reduce", dia(20, 80) + " expand · " + dia(10, 80) + " reduce", dia(20, 160) + " expand · " + dia(10, 160) + " reduce"], True),
    ("Max forming length", [inch(90), inch(90), inch(100)], True), ("Max tube wall thickness", [inch(4, 2), inch(8, 2), inch(8, 2)], False),
    ("Axial stroke", [inch(80) + " working + " + inch(20) + " free", inch(80) + " working + " + inch(20) + " free", inch(150)], False),
    ("Lifting force", [tons(19), tons(24), tons(34)], True), ("Expansion / reduction per stroke", ["Ø ~" + inch(7, 2), "Ø ~" + inch(7, 2), "Ø " + inch(26, 2) + " / Ø " + inch(16, 2)], False),
    ("Tool stations", ["1 C-tool holder (2 with option DUE)", "3 C-tool holders", "1 C-tool holder (2 or 3 optional)"], False), ("Mean cycle time", ["~4 s", "~3 s", "~3 s"], True),
    ("Hydraulic tank", [gal(50), gal(63), gal(63)], False), ("Pump flow", [gpm(13), gpm(16), gpm(20)], False), ("Working pressure", [psi(240), psi(300), psi(300)], False),
    ("Motor power", [hp(4), hp(5.5), hp(7.5)], False), ("Working position", "horizontal", False),
    ("Dimensions L × W × H", [dims(680, 520, 1350), dims(920, 1210, 1450), dims(920, 1000, 1500)], False), ("Weight", [weight(450), weight(600), weight(500)], False)])
TUBIMATIC_IO80 = table("Tubimatic IO 80", "Inner / outer tool end formers for commercially available IO-tools", ["Tubimatic IO 80", "Tubimatic IO 80 Electra", "Tubimatic IO-US 80 Electra"], [
    ("Tube diameter", dia(20, 80) + " expand · " + dia(10, 80) + " reduce", True), ("Max forming length", inch(80), True), ("Max tube wall thickness", inch(4, 2), False),
    ("Inner axial stroke", inch(80), False), ("Outer axial stroke", inch(80) + " (110 mm to the tool-change position)", False), ("Lifting force", [tons(24) + " inner and outer", tons(25) + " inner and outer", tons(25) + " inner and outer"], True),
    ("Expansion / reduction per stroke", "Ø ~" + inch(14, 2) + " / Ø ~" + inch(10, 2), False), ("Drive", ["hydraulic: " + gal(63) + ", " + gpm(20) + ", " + psi(300) + ", " + hp(7.5), "servo-electric, Bosch Rexroth " + hp(7.5), "servo-electric, Bosch Rexroth " + hp(7.5) + "; swivelling forming unit"], False),
    ("Mean cycle time", ["~3 s", "~5 s", "~3 s"], True), ("Working position", "horizontal", False),
    ("Dimensions L × W × H", [dims(1250, 800, 1250), dims(1500, 600, 1200), dims(1500, 600, 1500)], False), ("Weight", [weight(600), weight(600), weight(1000)], False)])
TUBIMATIC_IO160 = table("Tubimatic IO 160", "Inner / outer tool end formers for commercially available IO-tools", ["Tubimatic IO 160", "Tubimatic IO 160 Electra", "Tubimatic IO-US 160 Electra"], [
    ("Tube diameter", dia(20, 160) + " expand · " + dia(10, 160) + " reduce", True), ("Max forming length", inch(100), True), ("Max tube wall thickness", [inch(8, 2), inch(4, 2), inch(4, 2)], False),
    ("Inner axial stroke", inch(150), False), ("Outer axial stroke", inch(150), False), ("Lifting force", tons(34) + " inner and outer", True),
    ("Expansion / reduction per stroke", "Ø ~" + inch(14, 2) + " / Ø ~" + inch(10, 2), False), ("Drive", ["hydraulic: " + gal(100) + ", " + gpm(25) + ", " + psi(300) + ", " + hp(11), "servo-electric, Bosch Rexroth " + hp(11), "servo-electric, Bosch Rexroth " + hp(11) + "; swivelling forming unit"], False),
    ("Mean cycle time", ["~3 s", "~5 s", "~5 s"], True), ("Working position", "horizontal", False),
    ("Dimensions L × W × H", [dims(1900, 800, 1200), dims(2500, 600, 1200), dims(2300, 800, 1550)], False), ("Weight", weight(1200), False)])

# ----------------------------------------------------------------------------------------------- Weco line
IOS_COMMON = [("Max forming length", inch(100), True), ("Max tube wall thickness", inch(4, 2), False)]
TUBEX_IOS = table("Tubex IO-S", "Combined inner / outer tube end former", ["Tubex IO-S 200", "Tubex IO-S 400", "Tubex IO-S 600"], [
    ("Tube diameter", [dia(20, 200), dia(20, 400), dia(20, 600)], True)] + IOS_COMMON + [
    ("Inner axial stroke", [inch(150), inch(200), inch(200)], False), ("Lifting force", [tons(24) + " inner (Ø100)", tons(34) + " inner (Ø120)", tons(61) + " inner (Ø160)"], True),
    ("Inner tool forming stroke", ["Ø max " + inch(36, 2), "Ø max " + inch(49, 2), "Ø max " + inch(49, 2)], False), ("Outer tool radial stroke / force", ["Ø max " + inch(60, 2) + " · 8 × " + tons(11), "Ø max " + inch(60, 2) + " · 16 × " + tons(11), "Ø max " + inch(60, 2) + " · 24 × " + tons(11)], False),
    ("Tool interface inner / outer", ["Ø150 / Ø280 mm", "Ø190 / Ø480 mm", "Ø270 / Ø680 mm"], False), ("Mean cycle time", ["~30 s", "~35 s", "~40 s"], True),
    ("Hydraulic tank", [gal(63), gal(100), gal(100)], False), ("Pump flow", [gpm(20), gpm(25), gpm(25)], False), ("Working pressure", psi(300), False), ("Motor power", [hp(7.5), hp(11), hp(11)], False),
    ("Working position", "vertical (HV head for horizontal and vertical optional)", False), ("Dimensions L × W × H", dims(1600, 850, 1100) + " (variant 200)", False), ("Weight", weight(850) + " (variant 200)", False)])
WECO_ROWS = lambda forces, inner_strokes, cycles: [("Inner axial stroke", inner_strokes, False), ("Lifting force", forces, True),
    ("Inner tool forming stroke", ["Ø max " + inch(36, 2), "Ø max " + inch(49, 2), "Ø max " + inch(49, 2)], False),
    ("Outer tool radial stroke / force", ["Ø max " + inch(60, 2) + " · 8 × " + tons(9), "Ø max " + inch(60, 2) + " · 16 × " + tons(9), "Ø max " + inch(60, 2) + " · 24 × " + tons(9)], False),
    ("Tool interface inner / outer", ["Ø150 / Ø280 mm", "Ø190 / Ø480 mm", "Ø270 / Ø680 mm"], False), ("Inner tool rotation", "programmable in 10° steps to 67.5° against the outer tool", False),
    ("Mean cycle time", cycles, True)]
WECO_F = [tons(18) + " inner (Ø100)", tons(25) + " inner (Ø120)", tons(45) + " inner (Ø160)"]
WECO_S = [inch(150), inch(200), inch(200)]
WECOMATIC_200 = table("Wecomatic IO-S 200", "CNC radial forming machine", ["Wecomatic IO-S 200"], [
    ("Tube diameter", dia(20, 200), True)] + IOS_COMMON + [("Inner axial stroke", inch(150), False), ("Lifting force", tons(18) + " inner (Ø100)", True),
    ("Inner tool forming stroke", "Ø max " + inch(36, 2), False), ("Outer tool radial stroke / force", "Ø max " + inch(60, 2) + " · 8 × " + tons(9), False), ("Tool interface inner / outer", "Ø150 / Ø280 mm", False),
    ("Inner tool rotation", "programmable in 10° steps to 67.5° against the outer tool", False), ("Mean cycle time", "~15 s", True),
    ("Hydraulic tank", gal(275), False), ("Pump flow", "max " + gpm(65), False), ("Working pressure", psi("160/220") + " (300 bar optional, +40 % force)", False), ("Motor power", hp(11), False),
    ("Working position", "vertical (HV head optional)", False), ("Dimensions L × W × H", dims(2100, 1100, 1800), False), ("Weight", weight(1500), False)])
WECOMATIC_SPEED = table("Wecomatic IO-S Speed", "CNC radial forming machines, about 30 % faster", ["IO-S Speed 200", "IO-S Speed 400", "IO-S Speed 600"], [
    ("Tube diameter", [dia(20, 200), dia(20, 400), dia(20, 600)], True)] + IOS_COMMON + WECO_ROWS(WECO_F, WECO_S, ["~12 s", "~15 s", "~16 s"]) + [
    ("Hydraulic tank", gal(365), False), ("Pump flow", "max " + gpm(130), False), ("Working pressure", psi("160/220") + " (300 bar optional)", False), ("Motor power", hp(11, 2), False),
    ("Working position", "vertical (HV head optional)", False), ("Dimensions L × W × H", dims(2500, 1100, 1800), False), ("Weight", weight(1700), False)])
WECOMATIC_HIGH = table("Wecomatic IO-S High Speed", "CNC radial forming machines, about 60 % faster", ["IO-S High Speed 200", "IO-S High Speed 400", "IO-S High Speed 600"], [
    ("Tube diameter", [dia(20, 200), dia(20, 400), dia(20, 600)], True)] + IOS_COMMON + WECO_ROWS(WECO_F, WECO_S, ["~10 s", "~12 s", "~13 s"]) + [
    ("Hydraulic tank", gal(530), False), ("Pump flow", "max " + gpm(185), False), ("Working pressure", psi("160/220") + " (300 bar optional)", False), ("Motor power", hp(11, 3), False),
    ("Working position", "vertical (HV head optional)", False), ("Dimensions L × W × H", dims(2900, 1100, 1800), False), ("Weight", weight(1900), False)])
FLANGING_CELL = table("Flanging cell", "Rotating-head flanging and beading cell", ["Flanging cell"], [
    ("Tube diameter", dia(80, 400) + " (300 – 700 mm extension optional)", True), ("Max forming length", "—", True), ("Tube wall thickness", "0.012 – 0.094″ (0.3 – 2.4 mm)", False),
    ("Clamping", "8 hydraulic clamps, pressure controlled; 8 removable flange supports", False), ("Lifting force", "—", True), ("Mean cycle time", "~30 s for Ø110 mm, handling excluded", True),
    ("Hydraulic tank", gal(100), False), ("Pump flow", gpm(25), False), ("Working pressure", psi(300), False), ("Motor power", hp(11), False),
    ("Dimensions L × W × H", dims(1700, 1100, 1800), False), ("Weight", weight(2200), False)])

# ----------------------------------------------------------------------------------------------- cutting and deburring
TUBECUT = table("Tubecut IO-S 160 Electra", "Inner / outer shearing tube cutter", ["Tubecut IO-S 160"], [
    ("Tube diameter", dia(20, 160), True), ("Max forming length", "—", True), ("Max cut-off length", inch(200) + " or " + inch(400), False), ("Max tube wall thickness", inch(3, 2), False),
    ("Inner axial stroke", inch(50) + " electric · " + tons(10), False), ("Outer blade stroke", inch(30) + " pneumatic", False), ("Inner tool rotation", "0 – 180° against the outer tool", False),
    ("Lifting force", tons(10), True), ("Mean cycle time", "~10 s", True), ("Drive", "electric inner unit, pneumatic outer unit — no hydraulics, no coolant", False),
    ("Working position", "horizontal", False), ("Dimensions L × W × H", dims(1760, 620, 1740), False), ("Weight", weight(750), False)])
TUBESHEAR = table("Tubeshear", "Tube shear for straight and bent tubes", ["Tubeshear"], [
    ("Tube diameter", dia(20, 160), True), ("Max forming length", "—", True), ("Max tube wall thickness", inch(3, 2), False), ("Cutting width", inch(3.2, 2), False),
    ("Cutting speed", "scoring knife " + ftmin(0, 2.5) + " · chopping knife " + ftmin(0, 6), False), ("Lifting force", "scoring " + tons(5.5) + " · chopping " + tons(11), True),
    ("Mean cycle time", "~13 s cut on Ø80 mm", True), ("Hydraulic tank", gal(100), False), ("Pump flow", "5 – 60 L/min (1.3 – 15.9 gpm)", False), ("Working pressure", psi(300), False), ("Motor power", hp(11), False),
    ("Dimensions L × W × H", dims(3000, 2250, 1470) + " with the working table · " + dims(1650, 1050, 1470) + " without", False)])
ROTOBRUSH = table("Rotobrush", "Tube end deburring machine", ["Rotobrush"], [
    ("Tube diameter", dia(20, 160), True), ("Max forming length", "—", True), ("Wire brush adjustment", "0 – " + inch(75), False), ("Tube centre offset", "±6° eccentric", False),
    ("Lifting force", "—", True), ("Mean cycle time", "~3 s", True), ("Motor power", hp(4) + " brush · " + hp(0.25) + " rotating frame", False),
    ("Dimensions L × W × H", dims(1050, 700, 1520), False), ("Weight", weight(300), False)])


def vids(*ids_titles):
    from sahinler_lib import vids as _vids      # NovoTech's own channel: id, title, duration → video dict with thumb
    return _vids(*ids_titles)


def fam(id_, group, name, short, models_label, summary, features, optional, images, tables, videos=()):
    return dict(id=id_, group=group, page=P_FORM, brand=BRAND, name=name, short=short, models_label=models_label, summary=summary,
                features=features, optional=optional, images=images, videos=list(videos), specs=spec(tables))


FAMILIES = [
    # Easy line
    fam("wt-tubex", "wt-easy", "Tubex compact tube end expander, Ø3/4″ to 23.6″", "Tubex expander", "Tubex · Ø20 – 600 mm",
        "The entry-level expander: a vertical hydraulic unit in a compact housing that expands, sizes and calibrates tube ends from "
        "Ø3/4″ to Ø23.6″ with a cone-driven segmented tool — 2.2 US tons of lifting force on a 3.9″ stroke, about two seconds a "
        "cycle. Rings and tubes are expanded, calibrated round after bending or welding with an oval tool, and joined. A basic "
        "expansion tool covers Ø20 – 70 mm; plastic top jaws take the range to Ø600 mm. Touchscreen programming, a longer stroke, "
        "a horizontal version and a slot punching unit are options.",
        ["Expansion and calibration of tube ends Ø3/4″ – 23.6″ (20 – 600 mm), wall to 5/32″ (4 mm)", "21 US tons (19 t) lifting force · 3.9″ (100 mm) axial stroke · ~2 s cycle",
         "Exclusive cone expansion unit with quick-change flange for the basic tool", "Hardened Ø8.3″ (210 mm) tube supporting table"] + CTRL_EASY,
        OPT_EASY_CTRL + ["5.9″ (150 mm) axial stroke with Ø26 mm expansion per stroke", "Horizontal version", "Ø18.9″ (480 mm) steel supporting table", "Slot punching unit", VOLT_OPT],
        ["wt-tubex", "wt-tubex-horizontal", "wt-tubex-table", "wt-tubex-part"], [TUBEX], videos=vids(("UZLQXynn70s", "Tubex tube end expander"), ("AM66tl7B3Yo", "Tubex expanding and pressing"))),
    fam("wt-tubin", "wt-easy", "Tubin compact tube end reducers, Ø3/8″ to 7.5″", "Tubin reducer", "Tubin 150 · Tubin 200",
        "The Tubin reduces (impands) tube ends with collet-type top jaws closed by a cone: Ø3/8″ to 5.5″ on the Tubin 150, to 7.5″ "
        "on the Tubin 200, up to 0.55″ reduction per stroke on 5/32″ wall. The same compact vertical housing, 21 US ton hydraulic "
        "unit and foot-switch control as the Tubex; calibration of bent or welded ends and ring and tube joining are its other "
        "jobs. Touchscreen control and a horizontal version are optional.",
        ["Reduction and calibration Ø3/8″ – 5.5″ (10 – 140 mm) or Ø3/8″ – 7.5″ (10 – 190 mm), wall to 5/32″ (4 mm)", "21 US tons (19 t) · 3.9″ (100 mm) stroke · ~4 s cycle",
         "Compact impanding unit with tool holder for the top jaws"] + CTRL_EASY,
        OPT_EASY_CTRL + ["Horizontal version", VOLT_OPT],
        ["wt-tubin", "wt-tubin-horizontal", "wt-tubin-part"], [TUBIN], videos=vids(("vjVnj08CB_g", "Tubin tube end reducer"))),
    fam("wt-tubepress", "wt-easy", "Tubepress tube straightening press, Ø3/4″ to 6.3″", "Tubepress", "Tubepress · Ø20 – 160 mm",
        "Bent and welded tubes go out of round; the Tubepress presses them round again between a tool housing and an adjustable "
        "depth stop so the end former's tool fits and the joint seals. Ø3/4″ to 6.3″ tube, 21 US tons on a 5.9″ stroke, about two "
        "seconds a cycle, in a compact housing with the hydraulics built in.",
        ["Straightening of non-round tube Ø3/4″ – 6.3″ (20 – 160 mm) after bending or welding", "21 US tons (19 t) · 5.9″ (150 mm) stroke · ~2 s cycle",
         "Tool housing with adjustable depth stop"] + CTRL_EASY[2:],
        ["Special electrical connection; fan in the control cabinet", VOLT_OPT],
        ["wt-tubepress", "wt-tubepress-process", "wt-tubepress-part"], [TUBEPRESS]),
    fam("wt-tubepunch", "wt-easy", "Tubepunch tube end punching unit, from Ø3/4″", "Tubepunch", "Tubepunch · from Ø20 mm",
        "A compact horizontal punching unit for tube ends: single or multiple slots — straight, Torca, parallel or perpendicular "
        "to the axis — and round holes around the circumference, with a punch-and-die interface for tooling made to the part. "
        "10 US tons on a 1/2″ punch stroke in 0.3 s, with an adjustable stop plate for the punching length; built as the auxiliary "
        "machine beside an expander or reducer.",
        ["Slots and holes in tube ends from Ø3/4″ (20 mm), wall to 5/32″ (4 mm)", "10 US tons (9 t) · 1/2″ (13 mm) punch stroke · ~0.3 s per punch",
         "Punch and die interface (tooling to the part); adjustable punching length by stop plate", "Compact housing with the electrics and hydraulics built in; foot switch"],
        ["Special electrical connection; fan in the control cabinet", VOLT_OPT],
        ["wt-tubepunch", "wt-tubepunch-unit", "wt-tubepunch-part"], [TUBEPUNCH], videos=vids(("PB9W3SniXDk", "IO forming and 8-fold punching combined"))),
    # Universal line
    fam("wt-tubex-u", "wt-universal", "Tubex-U universal production expander, from Ø3/4″", "Tubex-U", "Tubex-U · from Ø20 mm",
        "The all-purpose production expander: a modular HW-Flex housing with the hydraulic unit bolted on, 26 US tons on a 5.9″ "
        "stroke (37 US tons with the Ø120 piston), expansion tools in 100 to 400 mm lengths for wall to 5/16″ and a quick-change "
        "interface for the mandrel. A 4″ touchscreen on a pivot arm with macro programming and 2,000 program memory is standard; "
        "7″ touchscreen, remote maintenance, heat exchangers, the 15 HP pump and a horizontal version are options.",
        ["Expansion from Ø3/4″ (20 mm), supporting table to Ø19.7″ (500 mm), wall to 5/16″ (8 mm)", "26 US tons (24 t) · 5.9″ (150 mm) stroke · Ø1.42″ (36 mm) expansion per stroke · ~3 s",
         "Standard tool lengths 3.9 / 5.9 / 7.9 / 11.8 / 15.7″ (100 – 400 mm)", "Quick-change flange for the basic tool and quick-change interface for the expansion mandrel", "Hardened tube supporting table; vertical working position"] + CTRL_U,
        OPT_U_CTRL + ["Ø120 mm piston, 37 US tons (34 t)", "Horizontal version; Ø39.4″ (1,000 mm) supporting table", "Central lubrication (SKF) with air service unit (Festo); bayonet quick-change for the cone", VOLT_OPT],
        ["wt-tubex-u", "wt-tubex-u-horizontal", "wt-tubex-u-part"], [TUBEX_U]),
    fam("wt-tubin-u", "wt-universal", "Tubin-U universal production reducers, Ø3/8″ to 7.5″", "Tubin-U", "Tubin-U 150 · Tubin-U 200",
        "The production impander in the same HW-Flex housing as the Tubex-U: Ø3/8″ to 5.5″ or 7.5″ tube reduced up to 0.83″ per "
        "stroke on wall to 5/16″, 26 US tons on a 5.9″ stroke, three-second cycles, touchscreen macro programming. Ø120 and Ø160 "
        "pistons (37 and 66 US tons), a 7.9″ forming length and a horizontal version are options.",
        ["Reduction Ø3/8″ – 5.5″ (10 – 140 mm) or Ø3/8″ – 7.5″ (10 – 190 mm), wall to 5/16″ (8 mm)", "26 US tons (24 t) · 5.9″ (150 mm) stroke · Ø0.83″ (21 mm) reduction per stroke · ~3 s",
         "Impanding unit on the HW-Flex universal housing; vertical working position"] + CTRL_U,
        OPT_U_CTRL + ["Ø120 mm piston, 37 US tons (34 t), or Ø160 mm piston, 66 US tons (60 t)", "Forming length 7.9″ (200 mm); horizontal version", "Central lubrication (SKF) with air service unit (Festo)", VOLT_OPT],
        ["wt-tubin-u", "wt-tubin-u-horizontal", "wt-tubin-u-part"], [TUBIN_U], videos=vids(("fdBzBNVtMkY", "Tubin-U production reducer"))),
    fam("wt-tubax-u", "wt-universal", "Tubax-U axial forming machines with tube clamping, Ø3/8″ to 11.8″", "Tubax-U", "Tubax-U 200 · Tubax-U 300",
        "A horizontal axial former that clamps the tube in jaws and pushes a forming tool into the end: beads, flares, collars and "
        "reductions on tube to Ø7.9″ (variant 200) or Ø11.8″ (variant 300), with 26 or 37 US tons on the forming axis and 37 or 75 "
        "US tons of clamping. Built for all-purpose series production on the HW-Flex housing with a safety cover and hand-wheel "
        "stroke adjustment.",
        ["Axial forming on clamped tube Ø3/8″ – 7.9″ (10 – 200 mm) or Ø3/8″ – 11.8″ (10 – 300 mm), wall to 5/32″ (4 mm)",
         "Forming 26 / 37 US tons on a 5.9″ (150 mm) stroke · clamping 37 / 75 US tons on a 3.9″ (100 mm) stroke · ~5 / ~8 s",
         "Forming unit and clamping unit each with a tool interface; safety cover; horizontal working position", "Forward and return stroke adjustable by hand wheel"] + CTRL_U[1:],
        ["Workpiece and hours counters, remote maintenance, digital I/O and Profisafe, oil monitors", "Oil / air or oil / water heat exchanger; 15 HP (11 kW) power increase",
         "Two-hand station on a free-standing console; lubricant saving system", VOLT_OPT],
        ["wt-tubax-u", "wt-tubax-u-300", "wt-tubax-u-diagram", "wt-tubax-u-part"], [TUBAX_U], videos=vids(("gKUZYwb4TbY", "Tubax-U axial forming"))),
    fam("wt-tubax-rotary", "wt-universal", "Tubax-Rotary Electra servo rotary forming machines, Ø1.6″ to 15.7″", "Tubax-Rotary Electra", "Tubax-Rotary 200 · Tubax-Rotary 400",
        "A rotating forming tool is moved axially against the clamped tube by servo motors and gears: mirror-smooth sealing faces "
        "below Ra 0.2, roll collars, beads and flanges formed with high, precisely applied force. Tube Ø1.6″ to 7.9″ with 5.9″ "
        "axial stroke on the 200, Ø1.6″ to 15.7″ with 11.8″ stroke on the 400; all-electric, with central lubrication and tooling "
        "holders for rolling head and clamping jaws.",
        ["Rotary forming of sealing faces, collars, beads and flanges on tube Ø1.6″ – 7.9″ (40 – 200 mm) or Ø1.6″ – 15.7″ (40 – 400 mm)",
         "Servo motor and gear on the rolling unit and on the clamping unit; surface quality < Ra 0.2", "Axial stroke 5.9″ / 11.8″ (150 / 300 mm) · clamping stroke 5.9″ (150 mm) · ~10 / ~20 s",
         "Central lubrication (SKF) with air service unit (Festo); horizontal working position; HW-Flex housing"],
        ["Workpiece and hours counters, remote maintenance, program key switch, digital I/O and Profisafe", "LED status light; two-hand console; safety light curtain for short tubes; air-conditioned cabinet", VOLT_OPT],
        ["wt-tubax-rotary", "wt-tubax-rotary-400", "wt-tubax-rotary-diagram", "wt-tubax-rotary-part"], [TUBAX_ROTARY], videos=vids(("2bfMV1pC4U8", "Tubax-Rotary 200 Electra rolling"), ("AgcIvvgyU8k", "Wecomatic IO-S 400 with Tubax-Rotary Electra 400"))),
    fam("wt-tubax-multi", "wt-universal", "Tubax-Multi Electra multi-station forming centre, Ø3/8″ to 6.3″", "Tubax-Multi Electra", "Tubax-Multi · Ø10 – 160 mm",
        "Five axial mandrels or milling heads on a servo tool changer form the tube end in one clamping: expand, reduce, bead and "
        "machine without re-handling the part. 40 US tons on an 11.8″ axial stroke and 40 US tons of clamping, tube Ø3/8″ to 6.3″, "
        "clamping length to 7.1″. Milling, rolling (radial) and forming stations are configured to the part family.",
        ["Five exchangeable axial mandrels or milling heads on a servo-driven tool changer", "Tube Ø3/8″ – 6.3″ (10 – 160 mm), clamping length to 7.1″ (180 mm)",
         "Axial stroke 11.8″ (300 mm) · 40 US tons (36 t); clamping stroke 3.9″ (100 mm) · 40 US tons", "HW-Flex housing with tube clamping unit and tooling interface; horizontal working position"],
        ["Milling station with spindle, tool mount and motor", "Rolling station with radial movement, rolling spindle and drives", "Additional forming station; chip conveyor; drip pan", "LED status light; two-hand console; air-conditioned cabinet", VOLT_OPT],
        ["wt-tubax-multi", "wt-tubax-multi-part", "wt-tubax-multi-part2"], [TUBAX_MULTI], videos=vids(("9bs7p3XdY_k", "Tubax-Multi Electra"))),
    fam("wt-tubiroll", "wt-universal", "Tubiroll-2R automatic beading and flanging machines, Ø1.6″ to 39.4″", "Tubiroll-2R", "Tubiroll-2R 600 · Tubiroll-2R 1000",
        "A fully automatic beading machine for thin-wall tube and duct: two rolls bead or flange tube from Ø1.6″ to 23.6″ (variant "
        "600) or 39.4″ (variant 1000) in 0.08″ wall, beading depth to 0.6″, with hydraulic roll drive, adjustable feed and a safety "
        "guard with light curtain. The operator loads and unloads while the machine cycles — about 8 s for a 10 mm bead on Ø200 mm.",
        ["Beading and flanging of tube Ø1.6″ – 23.6″ (40 – 600 mm) or Ø1.6″ – 39.4″ (40 – 1,000 mm), wall to 0.08″ (2 mm)",
         "Rolling length 3.9″ (100 mm), beading depth to 0.6″ (15 mm); peripheral speed 0 – 246 ft/min", "Hollow tool holder for the forming rolls; safety guard with light curtain",
         "Hydraulic roll drive and feed, each manually adjustable; pneumatic service unit (Festo); Siemens PLC with rapid / feed potentiometers"],
        ["Static driving-roll support for long tubes; pneumatic centring and blocking supports for tube to 1,000 mm long and Ø1,400 mm", "Rolling length increased to 7.9″ (200 mm)",
         "Oil / air or oil / water heat exchanger; drip pan with foot plate", VOLT_OPT],
        ["wt-tubiroll", "wt-tubiroll-diagram", "wt-tubiroll-part"], [TUBIROLL], videos=vids(("bM7thm2Lq20", "Tubiroll-2R beading machine"))),
    fam("wt-spiralmatic", "wt-universal", "Spiralmatic-Flex strip-wound flexible hose machine, Ø2″ to 7.9″", "Spiralmatic-Flex", "Spiralmatic-Flex · Ø50 – 200 mm",
        "Winds and seams flexible strip-wound metal hose — the corrugated exhaust, ventilation and chimney flex — from coil: a winding unit "
        "with height-adjustable carriage sets the hose diameter from Ø2″ to 7.9″, a seven-station hemming unit folds the 2″ strip and a "
        "seven-station seaming unit with hydraulic rollers locks the seam at 82 ft/min. Coil unwinder with hand brake, strip lubrication "
        "and adjustable strip entrance on the HW-Flex housing; a 3,000 mm roller table and a laser trimming device are options.",
        ["Flexible strip-wound hose Ø2″ – 7.9″ (50 – 200 mm) from 0.016″ (0.4 mm) strip, 2″ (50 mm) wide, at 82 ft/min (25 m/min)",
         "Hemming unit and seaming unit of seven stations each with pitch-angle adjustment; free-wheel decoupling of the seaming unit", "Winding unit with height-adjustable carriage and hollow-shaft interface for the winding mandrel",
         "Hydraulic unit with seven individually controlled stations for the seaming rollers; coil unwinder with hand brake; strip lubrication", "Siemens PLC with 4″ touchscreen and speed-differential potentiometer"],
        ["7″ touchscreen, counters, remote maintenance, Profisafe, coolant monitor", "Roller table 3,000 mm; laser trimming device with pneumatic ejector", "Central lubrication; pneumatic unwinding brake; LED status light", VOLT_OPT],
        ["wt-spiralmatic", "wt-spiralmatic-table", "wt-spiralmatic-hose", "wt-spiralmatic-hose2"], [SPIRALMATIC], videos=vids(("lpqRGu6D8jc", "Spiralmatic Flex"))),
    # Traditional line
    fam("wt-tubimatic-c", "wt-traditional", "Tubimatic C end formers for standard C-tools, Ø3/8″ to 6.3″", "Tubimatic C", "C 80 UNO · C 80 TRE · C 160 UNO",
        "Expanders and reducers built around the commercially available C-tools of the exhaust and tube trade, so existing "
        "tooling carries over: the compact C 80 UNO with one tool station for Ø3/4″ – 3.1″ expansion and Ø3/8″ – 3.1″ reduction, "
        "the C 80 TRE with three stations and 26 US tons for three forming steps without a tool change, and the C 160 UNO for "
        "tube to Ø6.3″ with 37 US tons and a 5.9″ stroke. Horizontal working position; second and third tool holders, a slot "
        "punching unit and the Tubimatic-AX head are options.",
        ["Compatible with commercially available C-tools; expansion Ø3/4″ – 3.1″ / 6.3″, reduction Ø3/8″ – 3.1″ / 6.3″",
         "C 80 UNO: 1 station, 21 US tons, 3.1″ + 0.8″ free stroke · C 80 TRE: 3 stations, 26 US tons · C 160 UNO: 1 station, 37 US tons, 5.9″ stroke",
         "Horizontal working position; forward and return stroke on a hand wheel (C 80 UNO)", "C 80 TRE and C 160 UNO on the HW-Flex housing with 4″ touchscreen, macro programming and 200 programs"],
        ["Option DUE (2 tool holders) and TRE (3 tool holders) on the UNO machines; left / right / alternate forming selection", "Ø120 mm piston, 37 US tons (34 t) on the C 80 TRE; crane for tool change on the C 160",
         "Tubimatic-AX manufacturing head; slot punching unit", "7″ touchscreen, USB, remote maintenance, Profisafe; heat exchangers; 15 HP power increase", VOLT_OPT],
        ["wt-tubimatic-c160", "wt-tubimatic-c80tre", "wt-tubimatic-c80uno", "wt-tubimatic-c-diagram", "wt-tubimatic-c-part"], [TUBIMATIC_C], videos=vids(("yhqAVTbgRks", "Tubimatic C 80 DUE"), ("fCILtMmtW3c", "Tubimatic C 80 DUE programmable"))),
    fam("wt-tubimatic-io80", "wt-traditional", "Tubimatic IO 80 inner / outer end formers for standard IO-tools, Ø3/8″ to 3.1″", "Tubimatic IO 80", "IO 80 · IO 80 Electra · IO-US 80 Electra",
        "Production end formers with inner and outer tools that take the IO tooling already in the shop: the inner tool expands "
        "while the outer tool closes on the tube, so flares, double flares, beads and reductions are formed in one stroke with "
        "a quick set-up. Tube Ø3/4″ – 3.1″ expansion and Ø3/8″ – 3.1″ reduction, 3.1″ forming length, 27 US tons inner and outer. "
        "The IO 80 is hydraulic; the Electra versions are servo-electric with a 10 HP Bosch Rexroth drive, and the IO-US Electra "
        "adds a swivelling forming unit for automated cells.",
        ["Compatible with commercially available IO-tools; inner and outer forming in one stroke", "Expansion Ø3/4″ – 3.1″ (20 – 80 mm), reduction Ø3/8″ – 3.1″ (10 – 80 mm), wall to 5/32″ (4 mm)",
         "Inner stroke 3.1″ (80 mm), outer stroke 3.1″ (80 mm, 110 mm to the tool-change position); 26 – 27 US tons inner and outer", "HW-Flex housing, safety cover on the tool, horizontal working position; 4″ touchscreen with macro programming"],
        ["Option DUE: two separate forming units", "200 alphanumerical programs, counters, remote maintenance, Profisafe, lubricant and oil monitors", "IO 80: 37 US ton (34 t) inner and outer force, proportional valves, heat exchangers, 15 HP power increase",
         "Drip pan under the forming unit; central lubrication (SKF / Festo) on the IO 80", VOLT_OPT],
        ["wt-tubimatic-io80", "wt-tubimatic-io80-electra", "wt-tubimatic-ious80", "wt-tubimatic-io-diagram", "wt-tubimatic-io-part"], [TUBIMATIC_IO80], videos=vids(("o7vyBqrQsxk", "Tubimatic IO 80 Electra"), ("ufduRg-u5ao", "Tubimatic IO-US 80 Electra"), ("NnzDYdWuBKY", "Tubimatic IO-US axial forming"), ("xVXU0Qkr00U", "Tubimatic IO-US oval reduction"), ("-PmQNa17_AQ", "Batch production on the Tubimatic"))),
    fam("wt-tubimatic-io160", "wt-traditional", "Tubimatic IO 160 inner / outer end formers for standard IO-tools, Ø3/8″ to 6.3″", "Tubimatic IO 160", "IO 160 · IO 160 Electra · IO-US 160 Electra",
        "The larger IO former: tube to Ø6.3″, 3.9″ forming length, 5.9″ inner and outer strokes and 37 US tons on both tools, with "
        "the same commercially available IO tooling. The hydraulic IO 160 takes wall to 5/16″ with a 15 HP power unit; the "
        "Electra versions run a 15 HP servo drive without hydraulics, and the IO-US Electra swivels the forming unit for "
        "integration in an automated line. A crane for tool change and a second forming unit (option DUE) are available.",
        ["Compatible with commercially available IO-tools; inner and outer forming in one stroke", "Expansion Ø3/4″ – 6.3″ (20 – 160 mm), reduction Ø3/8″ – 6.3″ (10 – 160 mm)",
         "Inner and outer strokes 5.9″ (150 mm); 37 US tons (34 t) inner and outer; ~3 – 5 s cycle", "HW-Flex housing, safety cover on the tool, horizontal working position; touchscreen with macro programming"],
        ["Option DUE: two separate forming units; crane for tool change", "IO 160: power-regulated pump with proportional valves, heat exchangers", "Counters, remote maintenance, Profisafe, lubricant and oil monitors; air-conditioned cabinet", VOLT_OPT],
        ["wt-tubimatic-io160", "wt-tubimatic-io160-electra", "wt-tubimatic-ious160", "wt-tubimatic-io160-diagram", "wt-tubimatic-io160-part"], [TUBIMATIC_IO160], videos=vids(("6YL3H-D8-Bg", "Tubimatic IO 160 bicone forming"), ("MU1f1OTpU9k", "Tubimatic IO 160 Electra expanding"), ("6EyvMLDbj7o", "Tubimatic IO 160 Electra reducing"), ("TDC8dDh6gF8", "Tubimatic IO 160 high speed, high power square expanding"), ("-hY8y-_2Q80", "Tubimatic IO-US 160 Electra"), ("qkEoALNkNME", "Tubimatic IO-US 160 with Tubepunch"), ("6CnFhqsJqA4", "Automated processes on the Tubimatic IO-US"))),
    # Weco line
    fam("wt-tubex-io-s", "wt-weco", "Tubex IO-S combined inner / outer tube end formers, Ø3/4″ to 23.6″", "Tubex IO-S", "Tubex IO-S 200 · 400 · 600",
        "The combined former for high degrees of forming: an inner expansion mandrel and 8, 16 or 24 radial outer pistons work "
        "together, so expansion, reduction, beading, flaring, flanging and embossing are formed in any position on round and "
        "shaped tube — exhaust components, ventilation parts, chimney elements. Three variants from Ø7.9″ to Ø23.6″ with 26, 37 "
        "or 67 US tons on the inner tool and 12 US tons on each outer piston; 12″ touchscreen, HV head for horizontal and vertical "
        "working and a light-curtain guard are options.",
        ["Inner / outer forming on tube Ø3/4″ – 7.9″, 15.7″ or 23.6″ (20 – 200 / 400 / 600 mm), wall to 5/32″ (4 mm)",
         "Inner tool 26 / 37 / 67 US tons with Ø1.42″ or 1.93″ forming stroke; outer tool Ø2.36″ radial stroke with 8 / 16 / 24 pistons of 12 US tons",
         "Expansion, reduction, beading, flaring, flanging and embossing in every position on round and shaped tube", "Vertical working position; HW-Flex housing with the hydraulic unit bolted on"],
        ["12″ colour touchscreen, 200 alphanumerical programs, counters, remote maintenance, Profisafe, oil monitors", "HV head for horizontal and vertical working; force increase on the inner and outer tool",
         "Safety guard with light curtain and mode selector; mechanically synchronised outer tools; bayonet quick-change for the cone", "Heat exchangers; 15 HP power increase; drip pan; central lubrication", VOLT_OPT],
        ["wt-tubex-io-s", "wt-tubex-io-s-guard", "wt-tubex-io-s-diagram", "wt-tubex-io-s-part"], [TUBEX_IOS], videos=vids(("pJdVW99rkyY", "Tubex IO-S 200 — shock absorber"), ("-SlgcxWwOPs", "Tubex IO-S 200 — V bead"), ("xpPsnW_LYPk", "Tubex IO-S 200 — sphere"), ("PNGfvKXFdhc", "Tubex IO-S 200 — exhaust pipe calibrating"), ("eXFIygwl5Q4", "Tubex IO-S 200 — oval"), ("Is7NtGNsfwA", "Tubex IO-S 200 — end cap"), ("bcEB68sW0P8", "Tubex IO-S 600 double head"))),
    fam("wt-wecomatic-200", "wt-weco", "Wecomatic IO-S 200 CNC radial forming machine, Ø3/4″ to 7.9″", "Wecomatic IO-S 200", "Wecomatic IO-S 200",
        "The flagship radial forming concept: CNC-controlled inner and outer tools with a programmable rotation of the inner tool "
        "in 10° steps, so the hardest forming tasks — multi-step expansions and reductions, beads, flares and flanges on exhaust "
        "and ventilation parts to Ø7.9″ — are programmed on the machine and run in about 15 s. Free-programmable CNC axes, a "
        "287-litre power unit with heat exchanger, quick-change tool flanges and mechanically synchronised outer tools.",
        ["CNC inner / outer forming on tube Ø3/4″ – 7.9″ (20 – 200 mm), wall to 5/32″ (4 mm); inner tool rotation programmable in 10° steps to 67.5°",
         "Inner tool 20 US tons (18 t) with Ø1.42″ forming stroke; 8 outer pistons of 10 US tons with Ø2.36″ radial stroke", "Quick-change flange for basic tool and mandrel; quick-change interface for the outer top jaws; synchronised outer tools",
         "Separate low- and high-voltage cabinets; lubricant, oil level / temperature and filter monitors standard; vertical working position"],
        ["Pressure increase to 300 bar (up to +40 % force); HV head for horizontal and vertical working", "Force increase on the inner and outer tool; safety guard with light curtain",
         "Touchscreen on pivot arm; work-place lighting; LED status light; remote maintenance, Profisafe", VOLT_OPT],
        ["wt-wecomatic-200", "wt-wecomatic-200-side", "wt-wecomatic-200-part"], [WECOMATIC_200], videos=vids(("oW2llrkpsHI", "Wecomatic IO-S 200 — V beading"), ("5eX5iyaDxV4", "Wecomatic IO-S 200 — tulip"), ("U9Igfkriexs", "Wecomatic IO-S 200 — press fitting V"), ("gvP5TjbV180", "Wecomatic IO-S 200 — reducing and bending"), ("jVguuN7TJIo", "Wecomatic IO-S 200 — expanding with integrated marking"), ("tb4mq3zf6Os", "Wecomatic IO-S 200 — sphere"), ("fBtUZ4qq-DM", "Wecomatic IO-S 200 — short tube bending"), ("ZKq4S8k0NZA", "Various forming on the Wecomatic"))),
    fam("wt-wecomatic-speed", "wt-weco", "Wecomatic IO-S Speed and High Speed CNC radial formers, Ø3/4″ to 23.6″", "Wecomatic IO-S Speed", "Speed 200 · 400 · 600 · High Speed 200 · 400 · 600",
        "The same CNC inner / outer forming with programmable inner-tool rotation, in three diameter variants to Ø23.6″ and two "
        "power levels: Speed with two 15 HP pumps is about 30 % faster than the IO-S 200, High Speed with three pumps about 60 % — "
        "10 to 16 s cycles on the largest parts. 20, 28 or 50 US tons on the inner tool, 8 to 24 outer pistons, 300 bar force "
        "increase and the HV head as options.",
        ["CNC inner / outer forming on tube Ø3/4″ – 7.9″, 15.7″ or 23.6″ (20 – 200 / 400 / 600 mm); inner tool rotation in 10° steps to 67.5°",
         "Inner tool 20 / 28 / 50 US tons; 8 / 16 / 24 outer pistons of 10 US tons; Ø1.42″ – 1.93″ forming stroke", "Speed: 2 × 15 HP, 96 US gal power unit · High Speed: 3 × 15 HP, 140 US gal; oil / air heat exchanger",
         "Quick-change tool flanges, synchronised outer tools, separate low- and high-voltage cabinets; vertical working position"],
        ["Pressure increase to 300 bar (up to +40 % force); High Power force increase on inner and outer tool", "HV head for horizontal and vertical working; safety guard with light curtain and mode selector",
         "Touchscreen on pivot arm; LED status light; remote maintenance, Profisafe, air-conditioned cabinet", VOLT_OPT],
        ["wt-wecomatic-speed", "wt-wecomatic-highspeed", "wt-wecomatic-400", "wt-wecomatic-diagram", "wt-wecomatic-part"], [WECOMATIC_SPEED, WECOMATIC_HIGH], videos=vids(("nIP6jMVVZq4", "Wecomatic IO-S 400 Speed High Power — Euro 6 / China 6 parts"), ("ZEcSolFbB9k", "Wecomatic IO-S 400 — V bead expanding"), ("MKr1nnRqdkM", "Wecomatic IO-S 400 — catalytic converter housing"), ("1xgFi2E2ctE", "Wecomatic IO-S 200 High Speed — sphere forming"), ("bLvY5hZcExA", "Wecomatic IO-S 1200 × 200 High Speed"))),
    fam("wt-flanging-cell", "wt-weco", "Flanging cell for bellows, T-pieces and bent parts, Ø3.1″ to 15.7″", "Flanging cell", "Flanging cell · Ø80 – 400 mm",
        "A rotating-head cell for flanging and beading parts that cannot be formed in a static tool: T-pieces, bends and unstable "
        "workpieces such as bellows are held by eight pressure-controlled hydraulic clamps and flange supports while the rotating "
        "forming head rolls the flange — bellows can be flanged directly onto the flange with additional clamping. Clamping, "
        "rotation and forming are run from a menu-driven CNC program with short set-up; Ø3.1″ – 15.7″ tube in 0.012 – 0.094″ wall.",
        ["Flanging and beading of bellows, T-pieces and bent parts Ø3.1″ – 15.7″ (80 – 400 mm), wall 0.012 – 0.094″ (0.3 – 2.4 mm)",
         "Rotation unit with integrated axial and radial axes: electric rotating drive, hydraulic path-controlled radial and axial drives", "8 hydraulic clamps and 8 removable flange supports, positions set independently of the workpiece; inner clamping cylinder",
         "Flanging diameter set-up electrically path-controlled; safety guard with light curtain; menu-driven CNC"],
        ["Forming unit extension for Ø11.8″ – 27.6″ (300 – 700 mm) tube and Ø31.5″ (800 mm) flanges", "NC axial roller drive, absolute flanging-height set-up, radial roller position set-up, measurement display",
         "Remote maintenance, Profisafe, oil monitors; heat exchangers; touchscreen on pivot arm", VOLT_OPT],
        ["wt-flanging-cell", "wt-flanging-cell-bellows", "wt-flanging-cell-step"], [FLANGING_CELL]),
    # cutting and deburring
    fam("wt-tubecut", "wt-cutting", "Tubecut IO-S 160 Electra tube shearing cutter, Ø3/4″ to 6.3″", "Tubecut IO-S 160", "Tubecut IO-S 160 Electra",
        "Tube cut by shearing between an inner and an outer tool instead of sawing: burr-free, without lubricant or emulsion, "
        "in about 10 s, with resharpenable shearing inserts and the inner tool rotating up to 180° against the outer tool for "
        "round and shaped tube to Ø6.3″ in 1/8″ wall. Electric inner unit, pneumatic outer unit, HW-Flex housing with scrap exit "
        "and a 7″ touchscreen with free-programmable cutting software — for cutting tube from the bar or trimming after forming.",
        ["Shear cutting of round and shaped tube Ø3/4″ – 6.3″ (20 – 160 mm), wall to 1/8″ (3 mm); cut-off length to 7.9″ or 15.7″ (200 / 400 mm)",
         "Burr-free cut without lubricant or coolant; shearing inserts resharpened; inner tool rotation 0 – 180°", "Electric inner cutting unit, 11 US tons (10 t); pneumatic outer blade, 1.2″ (30 mm) stroke; ~10 s cycle",
         "7″ colour touchscreen, USB, 200 alphanumerical programs; quick-change interfaces for inner and outer tool; scrap exit; central lubrication"],
        ["Tube rod cutting with programmable electric tube stop; insertion slide (electric); supporting table with guiding nut", "Two-hand station on a free-standing console; counters, remote maintenance, Profisafe; air-conditioned cabinet", VOLT_OPT],
        ["wt-tubecut", "wt-tubecut-notable", "wt-tubecut-diagram", "wt-tubecut-part"], [TUBECUT], videos=vids(("8glqyUN6YuI", "Tubecut IO-S — oval cutting"), ("IXH9bl5-dsg", "Tubecut IO-S with integrated tube stop"), ("4SCocdlxsmQ", "Tubecut with Rotobrush"))),
    fam("wt-tubeshear", "wt-cutting", "Tubeshear for straight and bent tubes, Ø3/4″ to 6.3″", "Tubeshear", "Tubeshear · Ø20 – 160 mm",
        "Cuts tube quickly, cleanly and cheaply in series production: a scoring knife and a chopping knife shear straight, "
        "curved and serpentine tube laid flat on a table that adjusts to the tube diameter — cutting tubes into lengths, trimming "
        "bent parts or parting single pieces. A torsion-resistant machined frame takes the 12 US ton chopping force; the shear "
        "also works without the table for maximum clearance left and right of the jaws.",
        ["Shear cutting of straight, curved and serpentine tube Ø3/4″ – 6.3″ (20 – 160 mm), wall to 1/8″ (3 mm); 1/8″ (3.2 mm) cutting width",
         "Scoring knife 6 US tons, 0 – 8 ft/min · chopping knife 12 US tons, 0 – 20 ft/min · ~13 s on Ø80 mm", "Torsion-resistant machined frame; height-adjustable lifting table (removable); horizontal working position",
         "15 HP (11 kW) power unit with 5 – 60 L/min variable flow; central lubrication for the cutting oil"],
        ["Oil / air or oil / water heat exchanger; oil sump; drip pan with foot plate", "Separate workpiece and hours counters; digital I/O, Profisafe, oil and filter monitors", VOLT_OPT],
        ["wt-tubeshear", "wt-tubeshear-process", "wt-tubeshear-part"], [TUBESHEAR], videos=vids(("xoiQEzHDXdE", "Tubeshear"))),
    fam("wt-rotobrush", "wt-cutting", "Rotobrush tube end deburring machine, Ø3/4″ to 6.3″", "Rotobrush", "Rotobrush · Ø20 – 160 mm",
        "Clean, fast deburring of cut tube ends before forming: a 5.5 HP wire brush on a linear adjustment of 0 – 3″ and a rotating "
        "frame that moves the tube centre ±6° eccentrically, so the whole inner and outer edge is brushed in about 3 s. "
        "Format-dependent safety plates on the HW-Flex housing; a suction device is optional.",
        ["Deburring of tube ends Ø3/4″ – 6.3″ (20 – 160 mm) in ~3 s", "5.5 HP (4 kW) brush motor; wire brush linear adjustment 0 – 3″ (75 mm); 1/3 HP rotating frame, ±6° eccentric",
         "Format-dependent exchangeable safety plates; HW-Flex housing"],
        ["Suction device; separate hours counter; fan in the control cabinet", VOLT_OPT],
        ["wt-rotobrush", "wt-rotobrush-head", "wt-rotobrush-part"], [ROTOBRUSH], videos=vids(("nDiOKeqX9S0", "Rotobrush tube end deburring"))),
]
