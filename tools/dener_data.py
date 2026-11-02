#!/usr/bin/env python3
"""Dener Makina (Kayseri, Turkey) — press brakes, shears, sheet and tube fiber lasers, panel bender.

Metric data from Dener's 2026 brochures (HYDRAULIC_EN, SERVO_EN, SHEARING_EN, SMART_EN, GFL_EN, TUBE_EN, PANEL BENDER_EN,
"Mild hybrid presentation") and NovoTech's own Dener brochures; shown as imperial (metric) like the rest of the site.
Model numbers are Dener's: metric bending length × metric tonnage (hydraulic / servo), cutting length × capacity (shears),
table size (lasers).

Pages fed from here: dener-cnc-press-brakes (hydraulic XL, hybrid XH, servo-electric DDM, ball-screw DDS), dener-shears (DAS CNC
guillotine, BS / BSY swing beam — under the shear-cutting hub; the family set 'shears' is written by tools/saymak_pages.py), dener-fiber-lasers (GFL + Smart sheet lasers, under the
laser-cutting-machine hub), dener-tube-lasers (FTL, E-FTL, under the tube-laser-cutting-machine hub) and panel-bender.
"""
BRAND = "dener"
P_PB = "dener-cnc-press-brakes"      # under the press-brake hub (Oct 2026); press-brake.html is the hub of the three press-brake pages
P_SHEAR = "dener-shears"
P_LASER = "dener-fiber-lasers"
P_TUBE = "dener-tube-lasers"
P_PANEL = "panel-bender"

US_PER_T = 1.10231


def fmt(v, nd=0):
    return f"{v:,.{nd}f}"


def inch(mm, nd=1):
    return f"{mm / 25.4:,.{nd}f}″ ({mm:,} mm)"


def feet(mm):
    f = mm / 304.8
    if round(f, 1) == 9.9:              # the 3,020 mm machines are 10 ft machines (the owner, Oct 31 2026): never "9.9 ft"
        return "10 ft"
    return f"{f:.0f} ft" if abs(f - round(f)) < 0.06 else f"{f:.1f} ft"


def length(mm):
    if feet(mm) == "10 ft" and round(mm / 25.4) < 120:
        return f"10 ft · 120″ ({mm:,} mm)"          # and 120″ with it, not 118.9″ (the owner, Oct 31 2026)
    return f"{feet(mm)} · {mm / 25.4:.1f}″ ({mm:,} mm)"


def tons(t):
    return f"{round(t * US_PER_T):,} US tons ({t:g} t)"


def hp(kw):
    return f"{kw * 1.341:.1f} HP ({kw:g} kW)"


def speed(mms):
    return f"{mms / 25.4:.2f} in/s ({mms:g} mm/s)"


def weight(kg):
    return f"{round(kg * 2.20462):,} lb ({kg:,} kg)"


def dims(l, w, h):
    return f"{l / 25.4:.0f} × {w / 25.4:.0f} × {h / 25.4:.0f}″ ({l:,} × {w:,} × {h:,} mm)"


def gal(lt):
    return f"{lt / 3.785:.0f} US gal ({lt} L)"


def mmin(v):
    return f"{v * 3.281:,.0f} ft/min ({v:g} m/min)"


def table(title, sub, models, rows, key_labels=("Bending force", "Bending length", "Cutting capacity", "Cutting length", "Working area", "Tube")):
    out = []
    for r in rows:
        label, s, cells = (r[0], r[1], r[2]) if len(r) == 3 else (r[0], "", r[1])
        cells = [cells] * len(models) if isinstance(cells, str) else list(cells)
        out.append({"label": label, "sub": s, "cells": cells, "key": any(label.startswith(k) for k in key_labels)})
    return {"title": title, "sub": sub, "models": list(models), "rows": out}


def spec(tables, gk, g_from, note):
    models = []
    for t in tables:
        rr = {r["label"]: r["cells"] for r in t["rows"]}
        for i, m in enumerate(t["models"]):
            models.append({"name": m, "glance": [rr[l][i] if l in rr else "" for l in g_from]})
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": gk, "caps": {}, "note": note}


# Shorts are not on the channel's Videos tab (tools/novotech-youtube-videos.tsv): their lengths here, their publish dates in
# tools/video_dates.json (build.py places them by date)
SHORTS = {"xv_iM-ZcEWw": "0:42", "rjqRtcExlmU": "0:44"}


def vids(*ids_titles):
    from sahinler_lib import vids as _vids, vid, yt_dur      # NovoTech's own channel: id → video dict with thumb
    out = []
    for it in ids_titles:
        i = it if isinstance(it, str) else it[0]
        out += [vid(i, it[1], yt_dur(SHORTS[i]))] if i in SHORTS else _vids(it)
    return out


# ------------------------------------------------------------------------------------------------ press brakes
# (model, length mm, t, approach, bend, return mm/s, stroke, daylight, throat, between frames, L, W, W no supports, H, table h, pit, kW, oil L, kg)
XL = [("XL 1560", 1550, 60, 180, 10, 160, 220, 410, 400, 1250, 2445, 2200, 1635, 2390, 900, 0, 7.5, 100, 4300),
      ("XL 2060", 2050, 60, 180, 10, 160, 220, 410, 400, 1650, 2845, 2200, 1635, 2390, 900, 0, 7.5, 100, 4900),
      ("XL 26100", 2600, 100, 160, 10, 150, 300, 530, 450, 2150, 3320, 2260, 1710, 2780, 900, 0, 11, 190, 7700),
      ("XL 30100", 3020, 100, 160, 10, 150, 300, 530, 450, 2555, 3725, 2260, 1690, 2780, 900, 0, 11, 190, 8700),
      ("XL 30135", 3020, 135, 160, 10, 130, 320, 550, 450, 2555, 3745, 2280, 1720, 2835, 900, 0, 15, 190, 9600),
      ("XL 30175", 3020, 175, 150, 10, 130, 350, 600, 450, 2555, 3745, 2280, 1720, 3030, 900, 0, 22, 300, 11600),
      ("XL 30220", 3020, 220, 140, 10, 130, 350, 600, 450, 2555, 3745, 2290, 1720, 3055, 920, 0, 22, 300, 11800),
      ("XL 30320", 3020, 320, 125, 10, 120, 400, 650, 450, 2555, 3785, 2290, 1755, 3100, 920, 0, 30, 400, 14800),
      ("XL 36175", 3650, 175, 150, 10, 130, 350, 600, 450, 3100, 4290, 2290, 1720, 3030, 920, 0, 22, 300, 12500),
      ("XL 36220", 3650, 220, 140, 10, 130, 350, 600, 450, 3100, 4290, 2290, 1730, 3055, 920, 0, 22, 300, 12700),
      ("XL 40175", 4050, 175, 150, 10, 130, 350, 600, 450, 3550, 4740, 2290, 1720, 3030, 920, 0, 22, 300, 14200),
      ("XL 40220", 4050, 220, 140, 10, 130, 350, 600, 450, 3550, 4740, 2290, 1730, 3050, 920, 0, 22, 300, 14300),
      ("XL 40320", 4050, 320, 125, 10, 120, 400, 650, 450, 3550, 4780, 2290, 1760, 3100, 920, 0, 30, 400, 17500),
      ("XL 40400", 4050, 400, 80, 10, 80, 400, 650, 600, 3550, 5000, 2770, 2290, 3560, 1095, 0, 37, 400, 25000),
      ("XL 60220", 6050, 220, 100, 10, 100, 350, 600, 450, 5100, 6825, 2300, 1760, 3010, 920, 0, 22, 300, 19000),
      ("XL 60320", 6050, 320, 80, 10, 80, 350, 650, 450, 5100, 6865, 2280, 1760, 3110, 920, 0, 30, 400, 23100),
      ("XL 60400", 6050, 400, 60, 10, 60, 400, 650, 600, 5100, 6905, 2780, 2330, 3615, 1095, 0, 37, 400, 32000),
      ("XL 60600", 6050, 600, 60, 8, 60, 450, 680, 600, 5100, 7145, 3275, 2800, 3910, 1000, 1030, 45, 600, 51700)]
XL_SMALL, XL_LARGE = XL[:8], XL[8:]


def pb_rows(data):
    return [("Bending force", [tons(r[2]) for r in data]),
            ("Bending length", [length(r[1]) for r in data]),
            ("Distance between frames", [inch(r[9]) for r in data]),
            ("Stroke", [inch(r[6]) for r in data]),
            ("Daylight", "open height", [inch(r[7]) for r in data]),
            ("Throat depth", [inch(r[8]) for r in data]),
            ("Approach speed", [speed(r[3]) for r in data]),
            ("Bending speed", [speed(r[4]) for r in data]),
            ("Return speed", [speed(r[5]) for r in data]),
            ("Table height", [inch(r[14]) for r in data]),
            ("Main motor", [hp(r[16]) for r in data]),
            ("Hydraulic oil tank", [gal(r[17]) for r in data]),
            ("Dimensions L × W × H", [dims(r[10], r[11], r[13]) for r in data]),
            ("Width without front supports", [inch(r[12]) for r in data]),
            ("Weight", [weight(r[18]) for r in data])]


PB_GK = ["bending_force", "bending_length", "stroke", "daylight", "weight"]
PB_G_FROM = ["Bending force", "Bending length", "Stroke", "Daylight", "Weight"]
NOTE_PB = ("Bending force in US tons (metric tons in brackets); the model number is Dener's — metric bending length × metric tonnage. "
           "Capacities vary with the V-die opening, material and sheet length: check the bending chart or ask us for the tonnage your part needs. "
           "Dimensions are overall L (along the bed) × W × H with the standard front supports.")

T_XL_SMALL = table("XL hydraulic press brakes · 5 – 10 ft", "8 models · 66 – 353 US tons", [r[0] for r in XL_SMALL], pb_rows(XL_SMALL))
T_XL_1560 = table("XL 1560 compact CNC press brake", "1 model · 66 US tons × 5 ft", [XL[0][0]], pb_rows(XL[:1]))
T_XL_LARGE = table("XL hydraulic press brakes · 12 – 20 ft", "10 models · 193 – 661 US tons", [r[0] for r in XL_LARGE], pb_rows(XL_LARGE))
T_XL = table("XL hydraulic CNC press brakes · 5 – 20 ft", "18 models · 66 – 661 US tons", [r[0] for r in XL], pb_rows(XL))

# mild hybrid option on the XL — Dener's SVP packages (Mild hybrid presentation, Dener 2026): (package, t, approach, bend, return, kW,
# energy saving %); frame, stroke, daylight and dimensions stay those of the XL of the same tonnage.  The XH is a different machine:
# Dener's full hybrid series (the owner, Oct 29 2026) — no SVP data belongs to it.
# the XF model is not sold (the owner, Oct 30 2026): its SVP 80 XF and SVP 125 XF packages are left out
XH = [("SVP 60", 60, 120, 10, 160, 5, None), ("SVP 100", 100, 200, 10, 200, 8.7, 45),
      ("SVP 135", 135, 170, 10, 160, 10.8, 42), ("SVP 175", 175, 170, 10, 150, 13.2, 45),
      ("SVP 220", 220, 175, 10, 160, 16.7, 51), ("SVP 320", 320, 130, 10, 150, 21.4, 55), ("SVP 400", 400, 100, 10, 100, 26.9, 58)]
XL_BY_T = {r[2]: r for r in XL}


def xh_rows():
    return [("Bending force", [tons(r[1]) for r in XH]),
            ("Bending length", "on request to 13 ft", ["up to 13 ft (4,050 mm) · 20 ft (6,050 mm) on request"] * len(XH)),
            ("Approach speed", [speed(r[2]) for r in XH]),
            ("Bending speed", [speed(r[3]) for r in XH]),
            ("Return speed", [speed(r[4]) for r in XH]),
            ("Servo motor", [hp(r[5]) for r in XH]),
            ("Energy saving vs. the standard XL", [f"about {r[6]} %" if r[6] else "—" for r in XH]),
            ("Frame, stroke, daylight", ["as the XL press brake of the same tonnage"] * len(XH))]


T_SVP = table("Mild hybrid option on the XL · Dener SVP packages", "servo motor and servo pump in the XL hydraulic circuit · 66 – 441 US tons",
              [r[0] for r in XH], xh_rows())
NOTE_SVP = ("Mild hybrid option: the SVP package replaces the XL's AC motor and fixed pump with a servo motor and servo pump; packages to 441 US "
            "tons (400 t) fit XL machines to 13 ft (4 m) bending length, longer machines on request. Frame, stroke, daylight, throat and "
            "dimensions stay those of the XL of the same tonnage and length.")

# servo-electric DDM: (model, length, t, approach, bend, return, stroke, daylight, L, W, H, kW, kg)
DDM = [("DDM 4015", 1530, 40, 180, 20, 180, 300, 590, 2670, 2280, 2530, 11, 4600), ("DDM 5020", 2040, 50, 150, 20, 150, 300, 590, 3180, 2280, 2530, 11, 5200),
       ("DDM 6525", 2550, 65, 130, 20, 130, 300, 590, 3680, 2280, 2530, 11, 5900), ("DDM 8025", 2550, 80, 100, 20, 100, 300, 590, 3680, 2280, 2530, 11, 6000),
       ("DDM 10030", 3050, 100, 75, 20, 75, 300, 590, 4220, 2260, 2530, 11, 6800), ("DDM 13030", 3050, 130, 80, 20, 80, 300, 590, 4230, 2300, 2660, 12.5, 8300),
       ("DDM 15030", 3050, 150, 100, 20, 100, 300, 590, 4770, 2480, 2820, 22, 12500), ("DDM 17535", 3570, 175, 85, 20, 85, 300, 590, 5370, 2480, 2820, 22, 14000),
       ("DDM 20040", 4080, 200, 75, 20, 75, 300, 590, 5760, 2480, 2820, 22, 15500)]
T_DDM = table("DDM servo-electric press brakes", "9 models · 44 – 220 US tons · 5 – 13.4 ft", [r[0] for r in DDM], [
    ("Bending force", [tons(r[2]) for r in DDM]),
    ("Bending length", [length(r[1]) for r in DDM]),
    ("Stroke", [inch(r[6]) for r in DDM]),
    ("Daylight", "open height", [inch(r[7]) for r in DDM]),
    ("Approach speed", [speed(r[3]) for r in DDM]),
    ("Bending speed", [speed(r[4]) for r in DDM]),
    ("Return speed", [speed(r[5]) for r in DDM]),
    ("Servo motor power", [hp(r[11]) for r in DDM]),
    ("Dimensions L × W × H", [dims(r[8], r[9], r[10]) for r in DDM]),
    ("Weight", [weight(r[12]) for r in DDM])])
NOTE_DDM = ("Bending force in US tons (metric tons in brackets); the model number is Dener's — metric tonnage × metric bending length. "
            "Servo-electric drive: no hydraulic oil, 20 mm/s bending speed on every model, power drawn only while the ram moves.")

# ball-screw DDS
T_DDS = table("DDS ball-screw electric press brakes", "2 models · 22 and 44 US tons · 3 – 4.3 ft", ["DDS 4013", "DDS 2090"], [
    ("Bending force", ["44 US tons (40 t)", "22 US tons (20 t)"]),
    ("Bending length", ["4.3 ft · 51.2″ (1,300 mm)", "3 ft · 35.4″ (900 mm)"]),
    ("Daylight", "open height", ["14.8″ (376 mm)", "14.8″ (376 mm)"]),
    ("Stroke", ["5.9″ (150 mm)", "5.9″ (150 mm)"]),
    ("Approach speed", ["4.72 in/s (120 mm/s)", "4.72 in/s (120 mm/s)"]),
    ("Bending speed", ["0.39 in/s (10 mm/s)", "0.39 in/s (10 mm/s)"]),
    ("Return speed", ["4.72 in/s (120 mm/s)", "4.72 in/s (120 mm/s)"]),
    ("Servo motor power", ["2 × 5.1 HP (2 × 3.8 kW)", "5.1 HP (3.8 kW)"]),
    ("Dimensions W × D × H", ["95.9 × 74.0 × 91.3″ (2,436 × 1,880 × 2,319 mm)", "69.3 × 50.4 × 86.2″ (1,760 × 1,280 × 2,189 mm)"]),
    ("Weight", ["7,496 lb (3,400 kg)", "4,409 lb (2,000 kg)"])])
NOTE_DDS = ("Bending force in US tons (metric tons in brackets). Ball-screw drive with Lenze servo technology — no hydraulic oil or cylinders; "
            "a compact machine for small parts, boxes and brackets.")

# The XL standard equipment: NovoTech's own list for the XL series (the owner's quote, Oct 30 2026) combined with the items from
# Dener's brochure, as plain text (the owner, Oct 30 2026: no links in this list).  The DSP-AP laser guard is standard now, so it
# left the XL options.
# The S840 has a 15.6″ screen and the S875 W a 21.5″ one (the owner, Oct 30 2026; ESA's data) — never "15″" / "21″".
PB_STD_XL = ["ESA S840 15.6″ 2D graphic touch-screen CNC control (Italy)",
             "2D offline programming software for the CNC control",
             "Heavy-duty X-axis back gauge on servo motor, ball screw and linear guides, with 2 finger stops adjustable by hand in height and lateral position",
             "Y1, Y2 ram axes on linear scales",
             "DSP-AP laser finger protection with MCS safety PLC",
             "2 front supports: sliding arms on linear rail with manual height adjustment",
             "European (Promecam) tool clamping with segmented punch and die holders",
             "EUROSTAMP 1281 punch (Italy)",
             "EUROSTAMP 2067 4-V die (Italy)",
             "Side and rear safety covers with safety interlocks", "Heavy-duty ram guideways", "Proportional servo-valve hydraulic system; constant pressure",
             "Anti-panic foot pedal with emergency stop button", "Large daylight and throat depth",
             "CSA-approved electrical panel; 600 V 3-phase transformer included", "Aluminum-foil waterproof overseas packaging",
             "Made in Turkey with European components"]
# the XH full hybrid keeps the brochure list (the owner's list above is for the XL series)
PB_STD_XH = ["X back gauge axis on ball screw and linear guides; Y1, Y2 ram axes", "15.6″ ESA S840 2D graphic touch-screen CNC control",
             "European-style segmented punch and die with European-style holders",
             "Anti-panic foot pedal with emergency stop", "Front support arms on linear rail", "Side and rear safety guards", "CSA-approved electrical panel, 600 V 3-phase standard"]
_PB_OPT_ALL = ["Mild hybrid drive (Dener SVP package): a servo motor and servo pump replace the AC motor and pump — the pump stops while the machine "
               "waits or is loaded and unloaded: 42 – 58 % less energy, faster approach and return, cooler oil, less noise and wear; on machines up to 441 US tons (400 t) and 13 ft",
               "21.5″ ESA S875 W 3D CNC control; Delem DA-66S or DA-69S 3D control", "CE-certified light barrier (DSP laser finger protection)",
               "X-R, X-R-Z1-Z2, X1-X2-R-Z1-Z2 or ATF X1-X2-R1-R2-Z1-Z2 back gauge (6 axes)", "Manual or CNC motorised crowning", "Automatic angle measurement (bending accuracy 0.05°)",
               "Sheet follower support", "Hydraulic oil cooler; electrical panel cooler; automatic lubrication", "Quick, pneumatic or Wila mechanical / hydraulic tool clamping",
               "Tandem configuration to 60 ft and 1,800 US tons", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
# the XL options: NovoTech's list for the XL series (the owner, Oct 30 2026) with the mild hybrid, angle measurement, tandem and
# voltage items of Dener's brochure; the XH keeps the brochure list (PB_OPT_XH)
PB_OPT_XL = [_PB_OPT_ALL[0],
             "21.5″ ESA S875 W 3D CNC control", "Delem DA-66S 2D CNC control", "Delem DA-69S 3D CNC control",
             "X-R back gauge", "X-R-Z1-Z2 back gauge", "X1-X2-R-Z1-Z2 back gauge", "ATF X1-X2-R1-R2-Z1-Z2 back gauge",
             "Bar-type X1-X2-R1-R2-Z1-Z2 back gauge", "Sheet followers", "Hydraulic oil cooling system", "Electrical panel cooling system",
             "Automatic lubrication system", "CNC motorised or manual crowning", "Quick punch clamping", "Pneumatic punch and die clamping",
             "Wila mechanical upper and lower tool clamping", "Wila hydraulic upper and lower tool clamping",
             "Automatic angle measurement (bending accuracy 0.05°)", "Tandem configuration to 60 ft and 1,800 US tons",
             "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
PB_OPT_XH = _PB_OPT_ALL[1:]
# DDM and DDS standard and optional equipment as Dener USA lists it on denerusa.com (the owner, Oct 31 2026), shown in the
# "Standard equipment / Optional equipment" tabs of the family
PB_STD_DDM = ["European-type segmented upper punch holder", "European-type segmented lower die holder", "21.5″ ESA S875 W 3D CNC control",
              "4 axes: Y1, Y2, X, R",
              "X-R back gauge: ball-screw X axis on two linear guides, 29.5″ (750 mm) X and 9.8″ (250 mm) R stroke, 2 manual fingers, "
              "± 0.03 mm positioning and repeatability",
              "DSP front laser finger protection", "Side and rear safety guards", "Anti-panic foot pedal with emergency stop",
              "Electrical cabinet cooling system", "600 V 3-phase, 60 Hz, CSA-approved electrical panel"]
PB_OPT_DDM = ["Delem DA-66S or DA-69S 3D control", "ATF X1-X2-R1-R2-Z1-Z2 back gauge", "X1-X2-R-Z1-Z2 back gauge", "X-R-Z1-Z2 back gauge",
              "X-Prime back gauge", "Fiessler AKAS 2 M(P) laser safety barrier", "CE-standard light barrier", "Manual or automatic (CNC) crowning",
              "Sheet followers", "Automatic angle measurement", "Pneumatic punch and die clamping",
              "Wila mechanical upper and lower tool clamping", "Wila hydraulic upper and lower tool clamping", "Robot bending cell",
              "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
# the DDS control is the 15″ ESA S640 (Dener USA and NovoTech's own servo brochure), not the S840 of the XL
PB_STD_DDS = ["European-type segmented upper punch holder", "European-type segmented lower die holder", "15″ ESA S640 2D colour touch-screen CNC control",
              "4 axes: Y1, Y2, X, R — 2-axis back gauge (X, R)", "DSP front laser finger protection", "Side and rear safety guards",
              "Foot pedal with emergency stop", "Electrical cabinet cooling system", "600 V 3-phase, 60 Hz, CSA-approved electrical panel"]
PB_OPT_DDS = ["21.5″ ESA S875 W 3D control", "Delem DA-66S or DA-69S 3D control", "5-axis back gauge (X, R, Z1, Z2, X-Prime) with the ESA S660 control",
              "Fiessler AKAS 2 M(P) laser safety barrier", "CE-standard light barrier", "Pneumatic punch and die clamping",
              "Wila mechanical upper and lower tool clamping", "Wila hydraulic upper and lower tool clamping", "Double-wedge adjustable European punch holder",
              "Foldable, height-adjustable work table", "Punches and dies", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]

# the controls Dener fits — a short note under every press brake (the buying guide on press-brake.html explains them)
CTL_XL = {"title": "ESA S840 2D as standard; ESA S875 W, Delem DA-66S or DA-69S as options",
          "text": "Every XL comes with the 15.6″ ESA S840 touch screen: numeric and 2D graphic programming, automatic calculation of tonnage, "
                  "bend sequence and back-gauge positions, tool library, up to 6 axes, USB and network. For shops that program from CAD or run "
                  "many different parts, Dener fits the 21.5″ ESA S875 W (3D programming and simulation, DXF / STEP import, EsaBend 3D), "
                  "the 24″ Delem DA-66S (2D graphic programming with a 3D machine view, Profile-S2D offline) or the 24″ Delem DA-69S "
                  "(full 3D programming and simulation, Profile-S3D) — the same four controls on every Dener press brake. All four have "
                  "collision control: once the part is drawn or imported, the control simulates the bend sequence and checks the part against "
                  "the punch, the die and the machine before the first bend.",
          "images": ["ctl-esa-s840-card", "ctl-esa-s875w-card", "ctl-delem-da66s", "ctl-delem-da69s"]}
CTL_DDM = {"title": "ESA S875 W 3D as standard; Delem DA-66S or DA-69S as options",
           "text": "The DDM is delivered with the 21.5″ ESA S875 W: 3D programming and simulation, automatic bend sequence, DXF / STEP import "
                   "and EsaBend 3D offline software on a Windows PC. The 24″ Delem DA-66S (2D graphic, 3D machine view) and DA-69S (3D) are "
                   "the alternatives for shops standardised on Delem. All three have collision control: the control simulates the bend "
                   "sequence and checks the part against the punch, the die and the machine before the first bend.",
           "images": ["ctl-esa-s875w-card", "dn-det-esabend-3d", "ctl-delem-da66s", "ctl-delem-da69s"]}
CTL_DDS = {"title": "ESA S640 2D as standard; ESA S875 W, Delem DA-66S or DA-69S as options",
           "text": "The small DDS carries the 15″ ESA S640 2D colour touch-screen control — numeric and 2D graphic programming with automatic "
                   "tonnage and sequence calculation. It can be ordered with the 21.5″ ESA S875 W 3D control, the Delem DA-66S or DA-69S, or "
                   "the ESA S660 with a 5-axis back gauge. The graphic controls check the drawn part against the punch, the die and the "
                   "machine before the first bend.",
           "images": ["ctl-esa-s875w-card", "ctl-delem-da66s", "ctl-delem-da69s"]}

PB_FAMILIES = [
    dict(id="dn-xl", control=CTL_XL, show_optional=True, layout="stacked",   # trial: gallery and videos across the page (owner, Oct 31 2026)
         group="pb-hydraulic", page=P_PB, brand=BRAND,
         name="XL hydraulic CNC press brakes, 66 – 661 US tons × 5 – 20 ft",
         short="XL hydraulic press brakes",
         models_label="XL 1560 – XL 60600 · 18 models",
         summary="The Dener XL is the hydraulic press brake most Canadian shops buy from us: a stress-relieved monoblock frame, servo-valve hydraulics "
                 "at constant pressure, Y1-Y2 ram axes and an X back gauge on ball screw and linear guides, driven from a 15.6″ ESA S840 2D "
                 "graphic control — the operator draws the part and the control works out the sequence, tonnage and back-gauge positions. "
                 "Eighteen models from 66 US tons × 5 ft to 661 US tons × 20 ft on the same frame design: the 5 to 10 ft machines to 353 US tons "
                 "for job-shop sheet work, the 12, 13 and 20 ft machines to 661 US tons with up to 26.8″ daylight, 17.7″ stroke and a 23.6″ throat "
                 "on the 400 and 600-ton sizes for deep boxes and large profiles (the 60600 sits in a pit). European-style tooling and front "
                 "supports come with every machine; the options run from CNC crowning and 6-axis back gauges to angle measurement, sheet "
                 "followers and robot cells, and for longer work Dener builds tandem machines — two XLs on one control bending to 60 ft and "
                 "1,800 US tons.",
         features=["Monoblock welded frame, stress-relieved and machined in one setting",
                   "5 to 20 ft bending lengths, 66 to 661 US tons; 23.6″ (600 mm) throat on the 400 and 600 t machines"] + PB_STD_XL,
         optional=PB_OPT_XL,
         # no XF photos (the owner, Oct 30 2026: the XF model is out of the gallery and the tables)
         # Dener's six XL detail photos with their captions (denerusa.com, the owner, Oct 30 2026); the blurry video frame of the
         # punch holders and the ATF back-gauge frame are out (the owner, Oct 30 2026)
         # + the detail photos of NovoTech's XL quote and the owner's own photos of a delivered XL (DSP-AP laser, CNC crowning, die
         # holder channel) with their standard / option status (the owner, Oct 30 2026); dn-xh-4, the
         # blurry tooling photo, is out (the owner, Oct 30 2026)
         # dn-xl-2 (three-quarter render), dn-xl-esa-screen (an ESA S660 W, not the XL's S840) and dn-xl-front-arms (the same
         # front supports as dn-xl-q-front-supports) and dn-xl-q-rear-gates out — the owner, Oct 30 2026; the 1281 punch and 2067 die
         # are EUROSTAMP's drawings with the inch values added (tools/eurostamp_photos.drawing), the laser angle measurement the owner's
         # picture, and the CNC crowning photo his second picture; the front support arms of the XL under 175 t and the manual
         # crowning (option) his pictures too, upscaled 4x in one Real-ESRGAN x4plus pass (tools/esrgan4.py), his photo of the back safety covers (standard) and of the sheet followers
         # with extended parking (option) (Oct 30 2026)
         # gallery order (the owner, Oct 31 2026): single machines, then the tandems on white, then the tandems in the shop, then the
         # details — the owner's own set of XL singles, tandems, throat, fingers and sheet followers added the same day
         images=["dn-xl-1", "dn-xl-3", "dn-xl-3000x220", "dn-xl-4000x320", "dn-xl-4000x600", "dn-xl-tandem-3000x320", "dn-xl-tandem-4000x320",
                 "dn-tandem-6000x600", "dn-xl-tandem-4000x320-shop", "dn-xl-p-tandem-9200", "dn-xl-throat", "dn-xl-throat-frames",
                 "dn-xl-xr-gauge", "dn-xl-bg-fingers", "dn-xl-servo-pump", "dn-xl-p-front-arms-std", "dn-xl-q-front-supports", "dn-xl-p-dsp-laser",
                 "dn-xl-p-back-covers", "dn-xl-es-1281", "dn-xl-es-2067", "dn-xl-p-crowning", "dn-xl-p-manual-crowning", "dn-xl-p-laser-angle",
                 "dn-xl-video-2", "dn-xl-follower", "dn-xl-p-follower-parking", "dn-sheet-followers", "dn-xl-control", "dn-xl-g-esa-s840",
                 "dn-xl-g-esa-s875w", "dn-xl-g-delem-da66s", "dn-xl-g-delem-da69s", "dn-det-bg-2axis", "dn-det-bg-4axis", "dn-det-bg-5axis",
                 "dn-det-bg-6axis-atf", "dn-xl-euro-tooling", "dn-xl-q-cylinder", "dn-xl-q-finger", "dn-xl-ram-slide", "dn-xl-p-die-channel",
                 "dn-xl-wila", "dn-xl-q-quick-release", "dn-xl-q-euro-american", "dn-xl-q-es-clamp", "dn-xl-q-es-clamp-2"],
         # the last nine photos at the end of the gallery, in the owner's order (Oct 31 2026)
         videos=vids(("0pvdG-DYO-E", "DENER XL 3100 × 100 — 10 ft × 110 US tons CNC press brake"), ("CFkFmrRCaFc", "DENER PUMA XL 10 ft × 135 ton 6-axis CNC press brake"),
                     ("qUb8fUZr0A4", "DENER XL 5 ft × 160 ton press brake"), ("pRxr7CB2pDQ", "XL 13 ft × 220 ton with laser angle measurement and sheet follower"),
                     ("dXorm3f4fBY", "DENER XL 13 ft × 320 ton CNC hydraulic press brake"), ("_rdb1prKsxc", "20 ft × 600 ton DENER Puma XL heavy-duty press brake"),
                     ("MkaKtgulHKw", "Heavy-duty CNC hydraulic press brake PUMA XL 20 ft × 600 ton with sheet follower"),
                     ("FpHkRYeceyA", "20 ft × 1,000 ton 9-axis CNC heavy-duty press brake"), ("AGifmIGQOso", "DENER 60 ft × 1,800 ton tandem press brake with auto feeder"),
                     ("jMqwk_yyCBo", "DENER 1,600 ton × 40 ft tandem press brake installation time-lapse"), ("dsZ8f7BKP84", "Tandem press brake PUMA XL 2 × 20 ft × 320 ton"),
                     ("fG6TQ8TseSo", "Hydraulic press brake with ATF 6-axis back gauge"), ("BUFzeYAAE_Y", "Laser angle measurement system on the XL press brake"),
                     ("VGd39pN2zBM", "CNC press brake instruction with the ESA control"),
                     # XLs with the mild hybrid option (the owner: the hybrid on the XL is the mild hybrid; the XH is the full hybrid)
                     ("vIWys546tWY", "DENER XL 10 ft × 220 ton mild hybrid CNC press brake"), ("nKbuxZGSjdQ", "DENER XL 12 ft × 175 ton mild hybrid press brake"),
                     ("-tAymdJwXjU", "DENER XL 13 ft × 220 ton mild hybrid press brake"), ("Msy6YHM5dIU", "DENER XL mild hybrid press brake"),
                     ("Ymz5qW36zTs", "DENER tandem 60 ft × 1,764 US tons (1,600 t) mild hybrid press brake with sheet following support")),
         # the SVP table sits under the XL table; the model list (compare, all models) stays the 18 XL machines
         specs=dict(spec([T_XL], PB_GK, PB_G_FROM, NOTE_PB), tables=[T_XL, T_SVP], note=NOTE_PB + " " + NOTE_SVP)),
    dict(id="dn-xl-1560", control=CTL_XL, show_optional=True, group="pb-compact-dener", page=P_PB, brand=BRAND,
         name="XL 1560 compact CNC press brake, 66 US tons × 5 ft",
         short="XL 1560 compact press brake",
         models_label="XL 1560 · 1 model",
         summary="The smallest XL is the compact press brake of the premium line: 60 metric tons (66 US tons) over 1,550 mm (5 ft), "
                 "49″ between the frames, a 15.7″ throat and 16.1″ of daylight, on a 96 × 87″ footprint (64″ wide without the front supports) that goes through a shop door and "
                 "weighs 9,480 lb — the same stress-relieved monoblock frame, servo-valve hydraulics, Y1-Y2 ram with linear scales and ball-screw X "
                 "back gauge as the big XLs, with the 15.6″ ESA S840 2D control, front supports on linear rail and a sectioned EUROSTAMP punch "
                 "1281 with the 4-way die 2067 in the crate. 7.5 kW, 600 V with a CSA panel. For HVAC fittings, enclosures, brackets, "
                 "signage and job-shop sheet work up to 5 ft where a 100-ton machine is more than you need — and a real CNC press brake, "
                 "not a bending brake: the control calculates tonnage, sequence and gauge positions, the DSP-AP laser finger guard comes as "
                 "standard, and 4- to 6-axis back gauges, CNC crowning and Wila clamping are the same options as on the 10 ft machines.",
         headline="66 US tons × 5 ft · 15.7″ throat · ESA S840 2D · 9,480 lb · EUROSTAMP 1281 / 2067 tooling included",
         features=["60 t × 1,550 mm — 16 ga to 3/16″ mild steel over the full 5 ft, 1/4″ over 4 ft (V = 8 × thickness)",
                   "Monoblock welded frame, stress-relieved and machined in one setting; 49.2″ (1,250 mm) between the frames",
                   "8.7″ (220 mm) stroke, 16.1″ (410 mm) daylight, 15.7″ (400 mm) throat for boxes and deep flanges",
                   "Ball-screw X back gauge with 25.6″ (650 mm) travel, fingers with manual R and Z adjustment and micro vernier"] + PB_STD_XL,
         optional=[x for x in PB_OPT_XL if not x.startswith("Tandem")],     # a 5 ft machine is not built in tandem
         images=["dn-xl1560-studio", "dn-xl1560-photo-left", "dn-xl1560-photo-front", "dn-xl1560-photo-right", "dn-xl1560-control",
                 "dn-xl1560-tooling", "dn-xl1560-tooling-2", "dn-xl1560-backgauge", "dn-xl1560-backgauge-2",
                 "dn-xl-es-1281", "dn-xl-es-2067"],   # the inch drawings of the standard tools (the owner, Oct 31 2026)
         videos=vids(("qUb8fUZr0A4", "DENER XL 5 ft × 160 ton press brake — the same 5 ft frame class"), ("5FWxGB6hoJI", "XL series hydraulic CNC press brakes"),
                     ("VGd39pN2zBM", "CNC press brake instruction with the ESA control")),
         specs=spec([T_XL_1560], PB_GK, PB_G_FROM, NOTE_PB)),
    dict(id="dn-xh", group="pb-hybrid", page=P_PB, brand=BRAND,   # no control box on the XH (the owner, Oct 31 2026)
         name="XH full hybrid press brakes — Dener's hybrid series",
         short="XH full hybrid press brakes",
         models_label="XH full hybrid series",
         summary="The XH is Dener's full hybrid press brake: a series designed around its servo-driven hydraulics, built for low energy use, "
                 "quiet operation and low running costs, with its own frame and covers (the XH design won a Bronze International Design Award). "
                 "It is a different machine from the XL with the mild hybrid option, where only the XL's main motor and pump are replaced by a "
                 "servo motor and servo pump — that option is listed with the XL. The XH takes the same controls and options as the XL; "
                 "tonnage, length and speeds are confirmed per machine, so ask us for the XH data in your size.",
         features=["Full hybrid: the servo-driven hydraulic system is designed into the machine, not added to an XL",
                   "The pumps turn only while the ram moves — low energy use, quiet operation and cool oil",
                   "Its own frame and covers — the XH design won a Bronze International Design Award"] + PB_STD_XH,
         optional=PB_OPT_XH,
         images=["dn-xh-1", "dn-xh-2", "dn-xh-3"],
         videos=[],
         specs=None),
    dict(id="dn-ddm", control=CTL_DDM, show_optional=True, group="pb-servo", page=P_PB, brand=BRAND,
         name="DDM servo-electric CNC press brakes, 44 – 220 US tons × 5 – 13.4 ft",
         short="DDM servo-electric press brakes",
         models_label="DDM 4015 – DDM 20040 · 9 models",
         summary="A full-electric press brake with no hydraulic oil: servo motors drive the ram through belts and pulleys, bending at 20 mm/s on "
                 "every model — twice the speed of a hydraulic — with 0.01 mm ram repeatability and power drawn only while the ram moves. Nine "
                 "models from 44 US tons × 5 ft to 220 US tons × 13.4 ft, all with the 21.5″ ESA S875 W 3D control, four axes (Y1, Y2, X, R) and "
                 "European tooling as standard; robot cells, 6-axis back gauges and angle measurement as options. Quiet, clean and "
                 "fast — the machine for a job shop that bends all day.",
         features=["Servo-electric ram drive — 0.79 in/s bending speed on every model, 0.01 mm repeatability", "No hydraulic oil, pump or valves; 50 – 70 % less energy than a hydraulic brake"] + PB_STD_DDM,
         optional=PB_OPT_DDM,
         images=["dn-ddm-2", "dn-ddm-1", "dn-ddm-5020", "dn-ddm-5020-side",
                 "dn-det-ddm-rear", "dn-det-ddm-motors", "dn-det-ddm-springs",
                 "dn-ddm-control", "dn-det-ddm-esa", "dn-det-esabend-3d", "dn-det-ddm-delem",
                 "dn-det-quick-release-plate", "dn-det-ddm-eurostamp", "dn-det-ddm-die-change", "dn-det-wila-tools",
                 "dn-ddm-video-1", "dn-det-bg-2axis-ddm", "dn-det-bg-6axis-atf",
                 "dn-det-front-support-single", "dn-det-cabinet-cooling",
                 "dn-det-crowning-motor"],
         videos=vids(("_Aqyyfk97KI", "DENER DDM 4015 — 5 ft × 40 ton servo-electric CNC press brake"), ("dlmcihzfRuI", "DENER DDM 5020 — 7 ft × 50 ton servo-electric press brake"),
                     ("ZujRJUhckG4", "DENER DDM 10030 — 10 ft × 100 ton servo-electric CNC press brake"), ("qLRQDobmnXQ", "DENER DDM servo-electric press brake robot cell"),
                     ("xv_iM-ZcEWw", "DENER DDM 5020 — 7 ft × 50 ton servo-electric press brake with the ESA 3D control and a 4-axis back gauge"),
                     ("rjqRtcExlmU", "DENER DDM 4015 — 5 ft × 40 ton servo-electric press brake on its way to a shop in Canada"),
                     ("7CzWdd1uY9w", "DENER DDM — 10 ft × 100 ton servo-electric press brake"),
                     ("30squAhhy_o", "CNC hydraulic press brake vs. servo-electric press brake")),
         specs=spec([T_DDM], PB_GK, PB_G_FROM, NOTE_DDM)),
    dict(id="dn-dds", control=CTL_DDS, show_optional=True, group="pb-servo", page=P_PB, brand=BRAND,
         name="DDS ball-screw electric press brakes, 22 and 44 US tons × 3 – 4.3 ft",
         short="DDS ball-screw press brakes",
         models_label="DDS 2090 · DDS 4013 · 2 models",
         summary="The small electric press brake: Lenze servo motors on ball screws move the ram — no oil, no cylinders — in a compact "
                 "monoblock frame with a small throat for precise bends on brackets, boxes, enclosures and pans. 22 US tons × 3 ft or 44 US "
                 "tons × 4.3 ft, 14.8″ daylight, the 15″ ESA S640 control, a 2-axis back gauge and a DSP laser finger guard as standard; a 5-axis gauge, Delem controls, "
                 "pneumatic or Wila clamping and a Fiessler AKAS laser guard as options. Plugs into a standard panel and goes through a normal door.",
         features=["Ball-screw ram drive with Lenze servo technology; up to 50 % energy saving", "Monoblock frame, small throat, 14.8″ daylight for box bending"] + PB_STD_DDS,
         optional=PB_OPT_DDS,
         images=["dn-dds-1", "dn-dds-2", "dn-dds-4013", "dn-dds-video", "dn-dds-3", "dn-dds-4", "dn-dds-ballscrew"],
         videos=vids(("GptvkfBO9GQ", "DENER DDS 40130 — 4 ft × 30 ton ball-screw servo-electric press brake"),
                     ("JVG9kw1nIGk", "DENER DDS 4 ft × 30 ton ball-screw electric press brake"), ("R5D3JCTN-Ww", "Small press brake — DDS 4013 ball-screw press brake"),
                     ("Myd9TVSUFj8", "DENER DDS 2050 — 1.6 ft × 20 ton ball-screw servo-electric press brake"), ("sq1YPi0sQTU", "Bending a water-sealed pan on the DDS ball-screw press brake"),
                     ("nlCZhY7olZ8", "DDS 4013 — 100 % electric ball-screw press brake")),
         specs=spec([T_DDS], PB_GK, PB_G_FROM, NOTE_DDS)),
]
PB_FAMILIES = [f for f in PB_FAMILIES if f["id"] != "dn-xh"]   # the XH full hybrid is off the site (the owner, Oct 31 2026)

# ------------------------------------------------------------------------------------------------ shears
# DAS: (model, length, ms, ss, al, angle, holddowns, kW, cuts/min, oil, L, throat, W no support, W, H, kg)
DAS = [("DAS 3006", 3080, 6, 4, 8, "0.5 – 2°", 16, 11, "25 / 12", 180, 3900, 350, 2150, 3380, 2165, 8000),
       ("DAS 4006", 4050, 6, 4, 8, "0.5 – 2°", 22, 11, "20 / 10", 180, 4940, 350, 2180, 3380, 2225, 11000),
       ("DAS 3010", 3080, 10, 7, 13, "0.5 – 2°", 16, 22, "22 / 10", 200, 3920, 350, 2230, 3440, 2290, 10000),
       ("DAS 3013", 3080, 13, 10, 18, "0.5 – 3°", 16, 30, "16 / 7", 400, 3900, 350, 2235, 3520, 2590, 13800),
       ("DAS 4013", 4050, 13, 10, 18, "0.5 – 3°", 22, 30, "15 / 6", 400, 4900, 350, 2270, 3500, 2650, 16700),
       ("DAS 3016", 3080, 16, 12, 22, "0.5 – 3°", 16, 30, "14 / 6", 400, 3900, 350, 2240, 3650, 2635, 16400),
       ("DAS 4016", 4050, 16, 12, 22, "0.5 – 3°", 22, 30, "13 / 5", 400, 4950, 350, 2250, 3660, 2700, 21500),
       ("DAS 3020", 3080, 20, 14, 26, "0.5 – 3°", 16, 37, "12 / 5", 750, 3950, 350, 2340, 3750, 2650, 19250),
       ("DAS 4020", 4050, 20, 14, 26, "0.5 – 3°", 22, 37, "11 / 4", 750, 5050, 350, 2350, 3755, 2740, 28500),
       ("DAS 6006", 6100, 6, 4, 8, "0.5 – 2.5°", 33, 11, "18 / 6.5", 200, 7035, 350, 2720, 4000, 2580, 27500),
       ("DAS 6013", 6110, 13, 9, 16, "0.5 – 2.5°", 31, 37, "11.5 / 5.3", 400, 7090, 350, 2775, 4055, 2730, 37500),
       ("DAS 6016", 6140, 16, 12, 22, "0.5 – 2.5°", 31, 45, "6.1 / 3.9", 750, 7200, 350, 3100, 4400, 2780, 49500),
       ("DAS 6020", 6140, 20, 14, 26, "0.5 – 2.5°", 31, 45, "6 / 3.5", 750, 7200, 350, 3150, 4450, 2780, 55000)]
# BS/BSY: (model, ms, ss, al, length, spm, angle, oil, kW, L, throat, W no support, W, H, kg)
BS = [("BSY 2006", 6, 4, 8, 2080, 22, 1.39, 200, 11, 2830, 150, 2115, 3640, 1860, 4800),
      ("BSY 2606", 6, 4, 8, 2620, 20, 1.39, 200, 11, 3380, 150, 2115, 3645, 1860, 5500),
      ("BSY 3006", 6, 4, 8, 3070, 18, 1.39, 200, 11, 3880, 150, 2110, 3495, 1750, 6500),
      ("BS 3006", 6, 4, 8, 3065, 18, 1.39, 200, 11, 3880, 150, 2140, 3700, 2150, 8000),
      ("BS 4006", 6, 4, 8, 4110, 14, 1.33, 200, 11, 4955, 150, 2160, 3695, 2140, 10400),
      ("BS 3010", 10, 7, 13, 3070, 12, 2, 200, 22, 3900, 150, 2305, 3770, 2430, 12000),
      ("BS 4010", 10, 7, 13, 4110, 8, 2, 200, 22, 4950, 150, 2305, 3830, 2415, 15000),
      ("BS 3013", 13, 10, 18, 3070, 12, 2.5, 300, 30, 3920, 150, 2308, 3840, 2520, 14000),
      ("BS 4013", 13, 10, 18, 4110, 8, 2, 400, 30, 4970, 150, 2308, 3840, 2508, 16850),
      ("BS 3016", 16, 12, 22, 3070, 12, 2.5, 400, 30, 3940, 150, 2235, 3865, 2500, 16120),
      ("BS 4016", 16, 12, 22, 4110, 8, 2, 400, 30, 4970, 150, 2320, 3865, 2508, 18400)]
CAPS = {6: "1/4″", 10: "3/8″", 13: "1/2″", 16: "5/8″", 20: "3/4″", 4: "5/32″", 7: "9/32″", 12: "15/32″", 14: "9/16″", 8: "5/16″", 18: "11/16″", 22: "7/8″", 26: "1″", 9: "11/32″"}


def cap(mm):
    return f"{CAPS[mm]} ({mm} mm)"


T_DAS = table("DAS CNC hydraulic guillotine shears", "13 models · 1/4″ – 3/4″ × 10 – 20 ft", [r[0] for r in DAS], [
    ("Cutting capacity, mild steel", "42 kg/mm² · 60,000 psi", [cap(r[2]) for r in DAS]),
    ("Cutting capacity, stainless steel", "70 kg/mm² · 100,000 psi", [cap(r[3]) for r in DAS]),
    ("Cutting capacity, aluminum", "20 kg/mm²", [cap(r[4]) for r in DAS]),
    ("Cutting length", [length(r[1]) for r in DAS]),
    ("Cutting angle", "variable", [r[5] for r in DAS]),
    ("Hold-down cylinders", [str(r[6]) for r in DAS]),
    ("Cuts per minute", "at min / max angle", [r[8] for r in DAS]),
    ("Main motor", [hp(r[7]) for r in DAS]),
    ("Hydraulic oil tank", [gal(r[9]) for r in DAS]),
    ("Throat depth", [inch(r[11]) for r in DAS]),
    ("Dimensions L × W × H", [dims(r[10], r[13], r[14]) for r in DAS]),
    ("Width without front supports", [inch(r[12]) for r in DAS]),
    ("Weight", [weight(r[15]) for r in DAS])])
T_BS = table("BS / BSY hydraulic swing beam shears", "11 models · 1/4″ – 5/8″ × 6.8 – 13.5 ft", [r[0] for r in BS], [
    ("Cutting capacity, mild steel", "42 kg/mm² · 60,000 psi", [cap(r[1]) for r in BS]),
    ("Cutting capacity, stainless steel", "70 kg/mm² · 100,000 psi", [cap(r[2]) for r in BS]),
    ("Cutting capacity, aluminum", "20 kg/mm²", [cap(r[3]) for r in BS]),
    ("Cutting length", [length(r[4]) for r in BS]),
    ("Strokes per minute", [str(r[5]) for r in BS]),
    ("Swing beam angle", [f"{r[6]:g}°" for r in BS]),
    ("Main motor", [hp(r[8]) for r in BS]),
    ("Hydraulic oil tank", [gal(r[7]) for r in BS]),
    ("Throat depth", [inch(r[10]) for r in BS]),
    ("Dimensions L × W × H", [dims(r[9], r[12], r[13]) for r in BS]),
    ("Width without front supports", [inch(r[11]) for r in BS]),
    ("Weight", [weight(r[14]) for r in BS])])
SH_GK = ["capacity", "length", "strokes", "motor", "weight"]
SH_G_FROM = ["Cutting capacity, mild steel", "Cutting length", "Cuts per minute", "Main motor", "Weight"]
SH_G_FROM_BS = ["Cutting capacity, mild steel", "Cutting length", "Strokes per minute", "Main motor", "Weight"]
NOTE_SH = ("Capacities are Dener's ratings over the full blade length for mild steel of 60,000 psi (42 kg/mm²), stainless of 100,000 psi "
           "(70 kg/mm²) and aluminum; the model number is the metric cutting length × capacity. Dimensions are overall L (along the blade) × W × H "
           "with the standard front supports.")
SH_STD_DAS = ["ESA 630 CNC control, 10″ touchscreen: back gauge, blade gap and cutting angle set by the control from the thickness and material; 100-step programs",
              "Motorised ball-screw back gauge, 0.1 mm accuracy, 39.4″ (1,000 mm) stroke", "Variable cutting angle and automatic blade-gap adjustment",
              "Hydraulic hold-downs; front protection frame with photocell; sheet slider table and squaring arm", "Remote foot pedal with emergency stop",
              "Welded steel frame, cutting beam on rollers — rigid against torsion over the full length", "CSA-approved electrical panel, 600 V 3-phase standard"]
SH_OPT_DAS = ["Longer front support arms, 6.6 or 9.8 ft (2 / 3 m)", "Pneumatic sheet support system (return of the cut piece)", "Shadow-line laser cutting line; light curtain",
              "Hydraulic oil cooler", "Spare blade set", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
SH_STD_BS = ["HT 071 NC control: back gauge, retract, stroke counter, 99 programs × 20 steps", "Motorised ball-screw back gauge, 0.1 mm accuracy, 39.4″ (1,000 mm) stroke",
             "Single-point manual blade-gap adjustment; cutting-length adjustment by timer", "Hydraulic hold-downs; 1 m flip-up front guard; sheet support arms and squaring arm",
             "Sheet slider table and back slider; remote foot pedal with emergency stop", "Welded steel frame proven on thousands of machines", "CSA-approved electrical panel, 600 V 3-phase standard"]
SH_OPT_BS = ["Longer front support arms, 6.6 or 9.8 ft (2 / 3 m)", "Pneumatic sheet support system", "Motorised blade-clearance adjustment from a CNC control (ESA 630)",
             "Shadow-line laser cutting line; light curtain", "Hydraulic oil cooler", "Spare blade set", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]

SHEAR_FAMILIES = [
    dict(id="dn-bs", group="shear-swing", page=P_SHEAR, brand=BRAND,
         name="BS / BSY hydraulic swing beam shears, 1/4″ – 5/8″ × 6.8 – 13.5 ft",
         short="BS swing beam shears",
         models_label="BSY 2006 – BS 4016 · 11 models",
         summary="The hydraulic shear for plate from 1/4″ to 5/8″: a swing beam on two cylinders cuts the full length in one stroke, 8 to 22 "
                 "strokes a minute, with an NC back gauge, hydraulic hold-downs and a welded frame that thousands of shops run every day. The "
                 "light BSY 2006 – 3006 cut 1/4″ over 6.8 – 10 ft; the BS 3006 – 4016 go to 5/8″ (16 mm) mild steel over 10 and 13.5 ft. "
                 "Single-point blade-gap adjustment, sheet slider table and squaring arm are standard.",
         features=["1/4″ to 5/8″ (6 – 16 mm) mild steel; 5/32″ to 15/32″ stainless; 5/16″ to 7/8″ aluminum"] + SH_STD_BS,
         optional=SH_OPT_BS,
         images=["dn-bs-2", "dn-bs-1", "dn-bs-3", "dn-bs-3013", "dn-bs-3010", "dn-bs-3006", "dn-bs-panel", "dn-shear-video-2"],
         videos=vids(("dla5MjevgT0", "DENER BS 3006 — 10 ft × 1/4″ swing beam shear with NC control"), ("3zHK_2sp3U0", "DENER BS 3006 — 10 ft × 1/4″ hydraulic shear"),
                     ("hnrRt3WFhqw", "DENER BS 3006 NC shear — 10 ft × 1/4″"), ("54vb6tx96aI", "NC / CNC hydraulic shears — DENER AS and BS series"),
                     ("WhowsXg9Z84", "NC hydraulic shear with pneumatic sheet support")),
         specs=spec([T_BS], SH_GK, SH_G_FROM_BS, NOTE_SH)),
    dict(id="dn-das", group="shear-cnc", page=P_SHEAR, brand=BRAND,
         name="DAS CNC hydraulic guillotine shears, 1/4″ – 3/4″ × 10 – 20 ft",
         short="DAS CNC guillotine shears",
         models_label="DAS 3006 – DAS 6020 · 13 models",
         summary="The production shear: a guillotine beam on linear rollers with a variable cutting angle, so thin sheet is cut fast and flat at "
                 "0.5° and 3/4″ plate at 3° with less distortion. The ESA 630 CNC sets back gauge, blade gap and angle from the thickness and "
                 "material the operator keys in; 16 – 33 hydraulic hold-downs, a 1 m ball-screw back gauge and the front photocell guard are "
                 "standard. Thirteen models: 1/4″ to 3/4″ (6 – 20 mm) mild steel over 10, 13 and 20 ft, from 8,000 to 55,000 kg.",
         features=["1/4″ to 3/4″ (6 – 20 mm) mild steel, 5/32″ to 9/16″ stainless, over 10 – 20 ft; up to 25 cuts a minute"] + SH_STD_DAS,
         optional=SH_OPT_DAS,
         images=["dn-das-3", "dn-das-1", "dn-das-2", "dn-das-3006", "dn-das-6006", "dn-shear-web", "dn-shear-video-1"],
         videos=vids(("wtCPgw_5GaY", "DENER DAS 3006 — 10 ft × 1/4″ CNC hydraulic shear with pneumatic back support"), ("eQ7NqRHVSvM", "CNC hydraulic metal shear AS 3006 DENER"),
                     ("54vb6tx96aI", "NC / CNC hydraulic shears — DENER AS and BS series")),
         specs=spec([T_DAS], SH_GK, SH_G_FROM, NOTE_SH)),
]

# ------------------------------------------------------------------------------------------------ sheet lasers
POWERS = "3 / 6 / 12 / 20 / 30 / 40 kW"


def nom_ft(mm):
    """a table dimension in nominal feet (the owner, Nov 1 2026: "10 × 5 ft", not "9.8 ft × 4.9 ft · 118 × 59″"): whole feet when
    within 2 %, otherwise one decimal — 3,000 → 10, 1,500 → 5, 2,000 → 6.6, 2,500 → 8.2, 12,500 → 41"""
    f = mm / 304.8
    r = round(f)
    if r and abs(f - r) / r <= 0.02:
        return f"{r}"
    return f"{f:.1f}".rstrip("0").rstrip(".")


def area(code):
    l, w = int(code[:-2]) * 100, int(code[-2:]) * 100
    return f"{nom_ft(l)} × {nom_ft(w)} ft ({l:,} × {w:,} mm)"


def laser_table(title, sub, prefix, codes, power, precision, speed_mmin, accel, worktable, extra=()):
    models = [f"{prefix} {c}" for c in codes]
    rows = [("Working area L × W", "nominal", [area(c) for c in codes]),
            ("Worktable", worktable),
            ("Laser source power", "options", power),
            ("Positioning accuracy", precision),
            ("Max. axis speed", mmin(speed_mmin)),
            ("Max. acceleration", accel)] + list(extra) + [("Voltage", "380 V 50/60 Hz · 600 V with transformer")]
    return table(title, sub, models, rows)


# GFL — the "Pro DC" gantry fiber laser on dener.com. Where Dener's GFL catalogue (GFL_EN, Oct 2026) and the PRO offer
# (PRO Laser 3015 6 & 12 kW) disagree, the catalogue's figure is used (the owner, Nov 1 2026: 1.5 G, 350 mm Z travel), checked
# against en.dener.com/urun/5/gantry-fiber-lazer (X-Y 1.5 G, Z 1 G, Z travel 350 mm, positioning 0.05, repeatability 0.03 mm,
# pallet change 16 / 22 / 30 s); details only the PRO offer gives (net cutting size, Z speed, drives, gases, weights, the
# cutting chart and the power consumption) are added from it.
GFL = [("GFL 3015", 3050, 1530, 16, 8500), ("GFL 4020", 4050, 2040, 22, 10200), ("GFL 6020", 6050, 2040, 30, 12600)]
GFL_KW = [3, 4, 6, 8, 12, 15, 20]
GFL_CUT = {"Mild steel": [18, 20, 25, 30, 35, 40, 50], "Stainless steel": [8, 10, 15, 25, 30, 35, 50],
           "Aluminum": [6, 8, 15, 25, 30, 35, 40], "Copper": [4, 6, 8, 10, 12, 12, 12], "Brass": [4, 6, 10, 12, 15, 18, 20]}
GFL_KWH = ["35.8", "39.7", "46.4", "51.45", "64", "80", "96"]
GFL_CORE = [50, 50, 50, 100, 100, 100, 100]


def frac_in(mm):
    """plate thickness in the nearest 1/16″ (denominators 2, 4, 8, 16 only): 18 → 11/16, 35 → 1-3/8, 50 → 1-15/16"""
    from fractions import Fraction
    n = round(mm / 25.4 * 16)
    w, r = divmod(n, 16)
    f = Fraction(r, 16)
    if not r:
        return f"{w}″"
    return (f"{w}-" if w else "") + f"{f.numerator}/{f.denominator}″"


T_GFL = table("GFL fiber laser cutting machines", "3 table sizes · 3 – 40 kW · shuttle table", [g[0] for g in GFL], [
    ("Working area L × W", "nominal · net cutting size", [f"{nom_ft(int(m[-4:-2]) * 100)} × {nom_ft(int(m[-2:]) * 100)} ft ({l:,} × {w:,} mm)"
                                                          for m, l, w, _, _ in GFL]),
    ("Worktable", "shuttle table, 2 tables"),
    ("Table change time", [f"{t} s" for *_, t, _ in GFL]),
    ("Laser source power", "options", "3 / 6 / 12 / 20 / 30 / 40 kW"),
    ("Laser source", "Raycus · IPG optional"),
    ("Cutting head", "Boji BLT autofocus · Precitec optional"),
    ("CNC control", "FSCUT · CypCut / HypCut · Fanuc optional"),
    ("Positioning accuracy", "±0.002″ (±0.05 mm)"),
    ("Repeatability", "±0.0012″ (±0.03 mm)"),
    ("Max. axis speed", "X, Y", mmin(120)),
    ("Max. Z-axis speed", mmin(50)),
    ("Max. acceleration", "X, Y", "1.5 G"),
    ("Z-axis acceleration", "1 G"),
    ("Z-axis stroke", inch(350)),
    ("Axis drives", "X, Y rack and pinion · Z ball screw"),
    ("Drive components", "Framo Morat · Yaskawa · THK"),
    ("Assist gas", "oxygen, nitrogen, air"),
    ("Weight", "approx.", [weight(kg) for *_, kg in GFL]),
    ("Voltage", "380 V 50/60 Hz · 600 V with transformer")])
T_GFL_CUT = table("GFL maximum cutting thickness by laser source power", "Dener cutting chart · 3 – 20 kW",
                  [f"{k} kW" for k in GFL_KW], [(m, [f"{frac_in(v)} ({v} mm)" for v in vals]) for m, vals in GFL_CUT.items()])
T_GFL_CUT["corner"] = "Material"
T_GFL_POWER = table("GFL electrical consumption by laser source power", "machine total, kW", [f"{k} kW" for k in GFL_KW],
                    [("Power consumption", [f"{v} kW" for v in GFL_KWH]), ("Fiber core diameter", [f"{v} µm" for v in GFL_CORE])])
T_GFL_POWER["corner"] = "Laser source"
NOTE_GFL = ("Working area: the nominal table size (3015 = 10 × 5 ft) and Dener's net cutting size in mm. Every table size is available with "
            "any of the listed laser sources; the maximum cutting thickness for 3 to 20 kW sources is in the cutting chart below — "
            "thickness varies with material quality, operator settings and cutting speed.")
T_SMART_C = laser_table("Smart fiber lasers with shuttle table", "6 table sizes · 3 – 40 kW", "Smart", ["3015", "4020", "6020", "6025", "8025", "12526"], POWERS,
                        "±0.03 mm (±0.0012″)", 140, "1 G", "shuttle table")
T_SMART_S = laser_table("Smart semi-closed fiber lasers · single table", "7 table sizes · 3 – 40 kW", "Smart", ["6025", "8025", "12525", "14035", "16045", "25031", "25040"],
                        POWERS, "±0.01 mm (±0.0004″)", 75, "0.6 G", "single table, semi-closed cabin")
LS_GK = ["working_area", "power", "speed", "accel", "worktable"]
LS_G_FROM = ["Working area L × W", "Laser source power", "Max. axis speed", "Max. acceleration", "Worktable"]
NOTE_LS = ("The model number gives the nominal working area (3015 = 3,000 × 1,500 mm); every table size is available with any of the listed "
           "laser sources. Cutting thickness depends on the source: as a guide, 6 kW cuts 3/4″ mild steel, 12 kW 1″ and 20 kW 1-1/2″ — ask us "
           "for the cutting chart for your material.")
LS_STD = ["Fiber laser source (IPG, Raycus or nLIGHT), Precitec or Raytools cutting head with autofocus", "Stress-relieved welded frame; space-frame bridge for high acceleration",
          "Shuttle table / pallet changer so loading overlaps cutting", "Pneumatic fume-extraction compartments and scrap boxes on wheels; prepared for a dust collector",
          "CNC control with nesting software, cutting database and production reports; remote diagnostics", "Laser-safe viewing glass; CE safety",
          "Chiller, air/nitrogen/oxygen assist-gas system", "CSA-approved electrical panel; 600 V with transformer"]
LS_OPT = ["Automatic loading / unloading tower", "Sheet storage automation", "Bevel cutting head", "Film-removal and marking functions", "Dust collector", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
GFL_STD = ["X, Y 394 ft/min (120 m/min) at 1.5 G; Z axis 1 G with a 13.8″ (350 mm) stroke; ±0.05 mm positioning, ±0.03 mm repeatability",
           "Shuttle table: two exchangeable tables, changed in 16 s (3015), 22 s (4020) or 30 s (6020) while the next sheet is loaded",
           "Raycus fiber laser source (IPG optional); Boji BLT autofocus cutting head — BLT 421S for 3 – 8 kW, BLT 643H for 12 – 15 kW, BLT 662H for 20 kW — "
           "with capacitive height sensing and a quick-change optics drawer: lens change in 2 minutes",
           "FSCUT 4000 (3 – 8 kW) or FSCUT 8000 (12 – 20 kW) EtherCAT control with CypCut or HypCut, CypNest nesting, a camera view of the working "
           "area and air cutting",
           "Stress-relieved one-piece welded frame finish-machined on a 5-axis portal mill; space-geometry bridge for high acceleration",
           "Framo Morat rack and pinion with planetary gearboxes, THK linear guides, Yaskawa servo drives, central automatic lubrication",
           "Six pneumatic extraction compartments switched by cutting position; six scrap boxes on wheels",
           "S&A dual-circuit chiller; proportional cutting-gas pressure control for oxygen, nitrogen and air",
           "Light curtain, emergency stops and status buzzer; front sliding door with laser-safe glass, rear pneumatic door",
           "Automatic nozzle cleaning and calibration on the sheet; starting kit of nozzles, ceramics and protective windows",
           "CSA-approved electrical panel; 600 V with transformer"]
GFL_OPT = ["Precitec ProCutter 2.0 cutting head", "IPG YLS fiber laser source", "Fanuc CNC control", "Air conditioner for the electrical cabinet",
           "Chemical air dryer", "Metalix cncKad CAD/CAM software", "CNC-controlled scrap conveyor", "Fume extraction filter", "UPS",
           "Voltage stabilizer"] + [o for o in LS_OPT if o != "Dust collector"]
SMART_STD = ["Raycus RFL series fiber laser source; BLT series autofocus cutting head with a quick-change optics drawer — lens change in 2 minutes",
             "FSCUT control with CypNest nesting software; handwheel for fine axis moves; resume cutting from any point after an alarm",
             "Inovance servo motors and drives, Techmech reducers, TWEBOLUN rack and pinion, SMC gas pressure regulators",
             "S&A CWFL dual-circuit chiller", "Stress-relieved welded frame; space-geometry bridge for high acceleration",
             "Six pneumatic fume-extraction compartments and six scrap boxes on wheels; prepared for a fume extraction system",
             "Light safety barriers, emergency stops and status buzzer; the head stops before it hits a part or the pallet",
             "Air, nitrogen and oxygen assist gas", "CSA-approved electrical panel; 600 V with transformer"]

LASER_FAMILIES = [
    dict(id="dn-gfl", group="laser-gfl", page=P_LASER, brand=BRAND,
         name="GFL fiber laser cutting machines, 5 × 10 to 6.6 × 20 ft, 3 – 40 kW",
         short="GFL fiber lasers",
         models_label="GFL 3015 · 4020 · 6020 · 3 – 40 kW",
         summary="The GFL is Dener's production sheet laser: a gantry on a stress-relieved, one-piece welded frame that moves at 394 ft/min "
                 "with 1.5 G acceleration, and a shuttle table whose two tables change in 16 to 30 seconds, so the next sheet is loaded while "
                 "the first is cut. Three table sizes — 10 × 5, 13 × 6.6 and 20 × 6.6 ft — with fiber sources from 3 to 40 kW (Raycus, IPG "
                 "optional), a Boji BLT autofocus head, the FSCUT control with CypCut and CypNest nesting, six pneumatic extraction "
                 "compartments and six scrap boxes on wheels. The machine for a job shop that cuts all day.",
         features=GFL_STD, optional=GFL_OPT,
         # the detail photos after dn-gfl-control come from Dener's GFL catalogue and the PRO offer (the owner, Nov 1 2026)
         images=["dn-gfl-1", "dn-gfl-3", "dn-gfl-2", "dn-gfl-3015", "dn-gfl-6020", "dn-gfl-open", "dn-gfl-frame", "dn-gfl-head", "dn-gfl-control",
                 "dn-gfl-cutting", "dn-gfl-blt-head", "dn-gfl-tables", "dn-gfl-zaxis", "dn-gfl-scrap", "dn-gfl-lube", "dn-gfl-pneumatic",
                 "dn-gfl-cypnest", "dn-gfl-fanuc", "dn-gfl-part", "dn-gfl-sheet"],
         videos=vids(("P3ynLUu2VYU", "DENER GFL 10 × 5 ft 6 kW laser cutting machine"), ("VjuvZWb_O_g", "DENER GFL laser cutting machine"),
                     ("0Cz5xYoNVec", "DENER GFL laser cutting machine"), ("NxTq4uw3n5k", "DENER GFL laser cutting machine"),
                     ("L9fTrifVFiA", "DENER 6 kW / 4 kW / 2 kW fiber laser cutting comparison"), ("C0mG6rJkHdU", "6 kW fiber laser cutting 15 mm mild steel")),
         # the "Intelligent air cutting" film (EFTY5a-Ri1Q) is Senfeng's, not Dener's — off the GFL (the owner, Nov 1 2026)
         pdf=dict(file="files/NovoTech-Dener-GFL-Fiber-Laser-2026.pdf", label="Download the GFL brochure", size="PDF · 2.5 MB · imperial units"),
         pdf_cta="Download GFL brochure",
         spec_pdf=dict(file="files/NovoTech-Dener-GFL-Fiber-Laser-Technical-Specification-2026.pdf", label="Download the GFL full technical specification",
                       size="PDF · 3.5 MB · imperial units", cta="Download full technical specification"),
         specs=dict(spec([T_GFL], LS_GK, LS_G_FROM, NOTE_GFL), tables=[T_GFL, T_GFL_CUT, T_GFL_POWER])),
    dict(id="dn-smart-closed", group="laser-smart", page=P_LASER, brand=BRAND,
         name="Smart fiber lasers with shuttle table, 5 × 10 to 8.5 × 41 ft, 3 – 40 kW",
         short="Smart lasers with shuttle table",
         models_label="Smart 3015 – 12526 · 6 table sizes · 3 – 40 kW",
         summary="The Smart series is the economy sheet laser from the same Turkish factory: a cabin with laser-safe glass, a "
                 "shuttle table and 459 ft/min at 1 G, in six table sizes from 5 × 10 ft to a 41 ft long bed. The same fiber sources, cutting "
                 "heads and software as the GFL, built to a lower price with a lighter frame and simpler cabin. Open front for the cutting "
                 "area, control and remote handset.",
         features=["Cabin with laser-safe viewing glass; shuttle table so loading overlaps cutting", "1 G acceleration, 459 ft/min (140 m/min) axis speed, ±0.03 mm precision"] + SMART_STD,
         optional=LS_OPT,
         # the Legend shop-floor photo (dn-laser-web) and videos zDGupa7NevE, 9J_m5e1Z7-M, oM9GCeSY9EI are off the Smart (the owner, Nov 1 2026)
         images=["dn-smart-1", "dn-smart-2", "dn-smart-open-front", "dn-smart-cutting"],
         pdf=dict(file="files/NovoTech-Dener-Smart-Fiber-Laser-2026.pdf", label="Download the Smart fiber laser brochure", size="PDF · 2.7 MB · imperial units"),
         videos=vids(("4Yp6X9tP6J8", "DENER SMART series laser cutting machine")),
         specs=spec([T_SMART_C], LS_GK, LS_G_FROM, NOTE_LS)),
    dict(id="dn-smart-semi", group="laser-smart", page=P_LASER, brand=BRAND,
         name="Smart semi-closed fiber lasers with single table, 8.2 × 20 to 13 × 82 ft, 3 – 40 kW",
         short="Smart semi-closed lasers",
         models_label="Smart 6025 – 25040 · 7 table sizes · 3 – 40 kW",
         summary="The large-format Smart: a single table from 8.2 × 20 ft to 13 × 82 ft with a semi-closed cabin that travels with the gantry "
                 "over the cut, for long plates, beams and parts that do not fit a standard sheet. ±0.01 mm positioning, 246 ft/min and 3 to 40 kW sources — the 20 – 40 kW machines "
                 "cut 1-1/2″ plate and thicker.",
         features=["Single table to 13 × 82 ft (4 × 25 m); semi-closed cabin on the gantry, loading from any side", "±0.01 mm precision, 246 ft/min (75 m/min), 0.6 G"] + SMART_STD,
         optional=LS_OPT,
         images=["dn-smart-semi-1", "dn-smart-semi-2", "dn-smart-semi-close"],
         pdf=dict(file="files/NovoTech-Dener-Smart-Fiber-Laser-2026.pdf", label="Download the Smart fiber laser brochure", size="PDF · 2.7 MB · imperial units"),
         videos=[],
         specs=spec([T_SMART_S], LS_GK, LS_G_FROM, NOTE_LS)),
]

# ------------------------------------------------------------------------------------------------ tube lasers
# Main tables: Dener's English tube catalogue (TUBE_EN 2026), by chuck size.  Model lists: Dener's Turkish tube catalogue
# (dener_borulazer.pdf), by model — length code × chuck (6025 = 6 m bed, Ø250 chuck); only the rows that do not contradict the
# English catalogue (the owner, Nov 1 2026: add the extra details and photos) — components as the English catalogue names them.  The 12,000 kg on the 12 m FTL 250 in TUBE_EN is a
# typing error for 1,200 kg (the Turkish model list: FTL 12025, 12,300 mm, 1,200 kg).
TL_POWERS = "3 / 6 / 12 / 20 kW"
T_FTL = table("FTL tube and profile fiber lasers", "4 chuck sizes · Ø0.6″ – 25.2″ · 3 – 20 kW", ["FTL 250", "FTL 350", "FTL 500", "FTL 640"], [
    ("Tube diameter", "round", ["Ø0.6 – 9.8″ (Ø15 – 250 mm)", "Ø1.2 – 13.8″ (Ø30 – 350 mm)", "Ø1.2 – 19.7″ (Ø30 – 500 mm)", "Ø4.7 – 25.2″ (Ø120 – 640 mm)"]),
    ("Profile size", "square / rectangular", ["0.6 – 9.8″ (15 – 250 mm)", "1.2 – 13.8″ (30 – 350 mm)", "1.2 – 19.7″ (30 – 500 mm)", "4.7 – 25.2″ (120 – 640 mm)"]),
    ("Laser source power", "options", TL_POWERS),
    ("Max. tube length and weight", ["20 ft, 1,323 lb (6 m, 600 kg) · 40 ft, 2,646 lb (12 m, 1,200 kg)", "30 ft, 2,205 lb (9 m, 1,000 kg) · 40 ft, 3,086 lb (12 m, 1,400 kg)",
                                     "40 ft, 4,630 lb (12 m, 2,100 kg)", "40 ft, 5,732 lb (12 m, 2,600 kg)"]),
    ("Max. speed", [mmin(80), mmin(54), mmin(25), mmin(25)]),
    ("Max. acceleration", "0.6 G"),
    ("Repeatability", ["±0.05 mm (±0.002″)", "±0.05 mm (±0.002″)", "±0.1 mm (±0.004″)", "±0.1 mm (±0.004″)"]),
    ("Chucks", "3 moving chucks · zero remnant"),
    ("Voltage", "380 V 50/60 Hz · 600 V with transformer")])
T_EFTL = table("E-FTL tube and profile fiber lasers", "4 chuck sizes · Ø0.3″ – 13.8″ · 3 – 20 kW · 1 G", ["E-FTL 120", "E-FTL 180", "E-FTL 250", "E-FTL 350"], [
    ("Tube diameter", "round", ["Ø0.3 – 4.7″ (Ø8 – 120 mm)", "Ø0.4 – 7.1″ (Ø10 – 180 mm)", "Ø0.6 – 9.8″ (Ø15 – 250 mm)", "Ø1.2 – 13.8″ (Ø30 – 350 mm)"]),
    ("Profile size", "square / rectangular", ["0.3 – 4.7″ (8 – 120 mm)", "0.4 – 7.1″ (10 – 180 mm)", "0.6 – 9.8″ (15 – 250 mm)", "1.2 – 13.8″ (30 – 350 mm)"]),
    ("Laser source power", "options", TL_POWERS),
    ("Max. tube length and weight", ["23 ft, 265 lb (7 m, 120 kg)", "23 ft, 529 lb (7 m, 240 kg)", "23 ft, 661 lb · 30 ft, 970 lb · 40 ft, 2,646 lb (7 / 9 / 12 m, 300 / 440 / 1,200 kg)",
                                     "23 ft, 1,323 lb · 30 ft, 2,646 lb · 40 ft, 3,968 lb (7 / 9 / 12 m, 600 / 1,200 / 1,800 kg)"]),
    ("Max. speed", [mmin(120), mmin(120), mmin(80), mmin(54)]),
    ("Max. acceleration", "1 G"),
    ("Repeatability", "±0.05 mm (±0.002″)"),
    ("Chucks", "2 moving chucks · remnant ≥1.4″ (35 mm)"),
    ("Voltage", "380 V 50/60 Hz · 600 V with transformer")])


_NOM_FT = {2: "6.6", 6: "20", 7: "23", 9: "30", 12: "40"}       # bed and table lengths in nominal feet (6 / 9 / 12 m → 20 / 30 / 40 ft)


def _ft_m(mm):
    m = mm / 1000
    f = _NOM_FT.get(m) if m == int(m) else None
    return f"{f or f'{mm / 304.8:.1f}'} ft ({m:g} m)"


def _mm3(x, y, z):
    return f"{x / 25.4:.1f} · {y / 25.4:,.0f} · {z / 25.4:.1f}″ ({x:,} · {y:,} · {z:,} mm)"


def _rpm(v):
    return f"{v} rpm"


def _lu(a, b):
    return f"{_NOM_FT[a]} + {_NOM_FT[b]} ft ({a} + {b} m)"


# E-FTL models: (model, chuck mm, bar length mm, X, Y, Z travel mm, tube feed m/min, chuck rpm, (L, W, H) mm, loading + unloading m)
EFTL_M = [("E-FTL 6012", 120, 7000, 290, 7850, 450, 131, 200, (11850, 2720, 2200), (7, 2)),
          ("E-FTL 6018", 180, 7000, 290, 7850, 450, 94, 180, (12150, 2720, 2200), (7, 2)),
          ("E-FTL 6025", 250, 7000, 860, 7800, 380, 115, 85, (12200, 2800, 3100), (7, 2)),
          ("E-FTL 6035", 350, 7000, 750, 7800, 460, 81, 54, (13200, 3450, 3600), (7, 2)),
          ("E-FTL 9025", 250, 9300, 860, 10300, 380, 115, 85, (14700, 2800, 3100), (9, 2)),
          ("E-FTL 9035", 350, 9300, 750, 10300, 460, 81, 54, (15800, 3450, 3600), (9, 2))]
FTL_M = [("FTL 6018", 180, 6200, 900, 7000, 250, 104, 180, (16100, 2800, 3000), (6, 6)),
         ("FTL 6025", 250, 6200, 850, 7200, 300, 92, 85, (16100, 2800, 3000), (6, 6)),
         ("FTL 6035", 350, 6200, 900, 7500, 300, 81, 54, (16100, 2800, 3000), (6, 6)),
         ("FTL 9025", 250, 9300, 850, 10000, 300, 92, 85, (19000, 2800, 3000), (9, 9)),
         ("FTL 9035", 350, 9300, 850, 10100, 300, 81, 54, (19000, 2800, 3000), (9, 9)),
         ("FTL 12025", 250, 12300, 850, 13100, 300, 92, 85, (28200, 2800, 2800), (12, 12)),
         ("FTL 12035", 350, 12300, 760, 13000, 460, 81, 54, (29100, 3400, 3400), (12, 12)),
         ("FTL 12050", 500, 12300, 1200, 13500, 540, 50, 25, (30500, 3950, 3750), (12, 12)),
         ("FTL 12064", 640, 12300, 1300, 13400, 540, 50, 25, (30500, 3900, 3400), (12, 12))]


def _model_rows(ms, extra):
    return [("Chuck", "max. tube Ø", [f"Ø{m[1] / 25.4:.1f}″ (Ø{m[1]} mm)" for m in ms]),
            ("Max. tube length", [_ft_m(m[2]) for m in ms])] + extra(ms) + [
            ("Axis travel", "X · Y · Z", [_mm3(m[3], m[4], m[5]) for m in ms]),
            ("Tube feed speed", [mmin(m[6]) for m in ms]),
            ("Chuck rotation", [_rpm(m[7]) for m in ms]),
            ("Loading + unloading length", [_lu(*m[9]) for m in ms]),
            ("Machine size", "L × W × H", [dims(*m[8]) for m in ms])]


T_EFTL_M = table("E-FTL models", "6 models · 23 and 30.5 ft (7 and 9.3 m) bars · Ø4.7″ to 13.8″ chucks", [m[0] for m in EFTL_M], _model_rows(EFTL_M, lambda ms: [
    ("Bevel cutting", "option"),
    ("Loading system", "option", ["Semi-automatic or fully automatic"] * 2 + ["Fully automatic bundle loader"] * 4),
    ("Cutting head", "BOCI, by source power", ["≤3 kW BLT310T · 6 kW BLT421TS"] * 2 + ["≤3 kW BLT310T · 6 kW BLT421TS · 12 kW BLT442T"] * 4),
    ("Unloading length", "6.6 ft (2 m)")]))
T_FTL_M = table("FTL models", "9 models · 20.3, 30.5 and 40.4 ft (6.2, 9.3 and 12.3 m) bars · Ø7.1″ to 25.2″ chucks", [m[0] for m in FTL_M], _model_rows(FTL_M, lambda ms: [
    ("Bevel cutting", ["option"] * 6 + ["standard"] * 3),
    ("Loading system", "option", "Semi-automatic loader"),
    ("Cutting head", "BOCI, by source power", "≤3 kW BLT310T · 6 kW BLT421TS · 12 kW BLT442T · 20 kW BLT560H"),
    ("Unloading length", [_ft_m(m[9][1] * 1000) for m in ms])]))
TL_GK = ["tube", "profile", "power", "speed", "length"]
TL_G_FROM = ["Tube diameter", "Profile size", "Laser source power", "Max. speed", "Max. tube length and weight"]
NOTE_TL = ("Chuck size is the model number (250 = Ø250 mm); every chuck size is available with any of the listed laser sources. In the "
           "model lists the model number is bed length × chuck (6025 = 6 m bed, Ø250 chuck). Ask us for the cutting chart for your "
           "tube wall and material.")
_TL_STD_ALL = ["Maxphotonics fiber laser source; BOCI BLT autofocus tube cutting head, chosen by source power",
               "Servo-driven supports that follow the tube as it turns; automatic lubrication",
               "TubePro operator interface; imports IGS and SAT files of the tube parts",
               "TWEBOLUN rack and pinion, Techmech gearboxes, Inovance servo motors and drives; SMC gas regulator; S&A CWFL chiller",
               "Fume extraction through the tube; chip and slug collection", "CE safety enclosure", "CSA-approved electrical panel; 600 V with transformer"]
EFTL_STD = ["Two moving pneumatic chucks with automatic centring; remnant from 1.4″ (35 mm)",
            "FSCUT3000 control; TubeST nesting software, small-tube version",
            "6.6 ft (2 m) unloading table"] + _TL_STD_ALL
FTL_STD = ["Three moving chucks: the third takes over the bar so the last part is cut with zero remnant",
           "FSCUT5000A control; TubeST nesting software, professional version",
           "Unloading table as long as the bar: 20, 30 or 40 ft (6, 9 or 12 m)",
           "Bevel (3D) cutting head standard on the FTL 12035, 12050 and 12064"] + _TL_STD_ALL
EFTL_OPT = ["Fully automatic bundle loader; on the 120 and 180 chucks a semi-automatic or fully automatic loader", "Bevel (3D) cutting head",
            "Seam detection; tapping and drilling attachments", "Dust collector", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
FTL_OPT = ["Semi-automatic loader", "Bevel (3D) cutting head (FTL 6018 to 12025)",
           "Seam detection; tapping and drilling attachments", "Dust collector", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
TL_STD = EFTL_STD           # kept for older callers
TL_OPT = EFTL_OPT

TUBE_FAMILIES = [
    dict(id="dn-eftl", group="tube-eftl", page=P_TUBE, brand=BRAND,
         name="E-FTL tube and profile laser cutters, Ø0.3″ – 13.8″, 3 – 20 kW",
         short="E-FTL tube lasers",
         models_label="E-FTL 120 · 180 · 250 · 350",
         summary="The fast tube laser: servo axes accelerating at 1 G move two chucks at up to 394 ft/min, cutting round, square, "
                 "rectangular and open profiles from Ø0.3″ to 13.8″ in 7, 9 or 12 m lengths with ±0.05 mm repeatability. Four chuck "
                 "sizes and 3 to 20 kW sources; servo supports follow the tube, TubeST nests the parts along the bar and a fully "
                 "automatic bundle loader can be added (on the 120 and 180 chucks a semi-automatic one as well).",
         features=["Ø0.3 – 13.8″ (8 – 350 mm) round and profile; 1 G, 394 ft/min (120 m/min)", "Tube length 23, 30 or 40 ft (7, 9 or 12 m)"] + EFTL_STD,
         optional=EFTL_OPT,
         images=["dn-tube-2", "dn-tube-1", "dn-tube-3", "dn-tube-eftl-side", "dn-tube-eftl-rear", "dn-tube-cabin", "dn-tube-tubest"],
         videos=vids(("n4gFLrlC-es", "DENER E-FTL tube laser cutting machine with auto loader"), ("6_UQ6NBUUO4", "DENER E-FTL tube laser cutting machine")),
         specs=spec([T_EFTL, T_EFTL_M], TL_GK, TL_G_FROM, NOTE_TL)),
    dict(id="dn-ftl", group="tube-ftl", page=P_TUBE, brand=BRAND,
         name="FTL tube and profile laser cutters, Ø0.6″ – 25.2″, 3 – 20 kW",
         short="FTL tube lasers",
         models_label="FTL 250 · 350 · 500 · 640",
         summary="The heavy tube laser: three moving chucks hold the bar to the last part, so it is cut with zero remnant, and carry "
                 "structural tube, pipe and beams to 25.2″ across and 40 ft (12 m) long — up to 2,600 kg per bar on the 640 chuck. 3 to "
                 "20 kW sources; the bevel head cuts weld preparations and is standard on the 12 m 350, 500 and 640 machines. For "
                 "steel-construction, trailer, agricultural and equipment builders.",
         features=["Ø0.6 – 25.2″ (15 – 640 mm) round and profile; bars to 40 ft (12 m) and 5,732 lb", "3 to 20 kW sources; BOCI heads to the 20 kW BLT560H"] + FTL_STD,
         optional=FTL_OPT,
         images=["dn-tube-6", "dn-tube-4", "dn-tube-5", "dn-tube-7", "dn-tube-cutting", "dn-tube-head-cut", "dn-tube-head"],
         videos=vids(("zPexjUvz7jg", "DENER FTL tube laser cutting machine")),
         specs=spec([T_FTL, T_FTL_M], TL_GK, TL_G_FROM, NOTE_TL)),
]

# ------------------------------------------------------------------------------------------------ panel bender
T_PANEL = table("CNC panel bender", "1 model · 79″ × 49″ blank · 1/8″ aluminum, 14 ga mild steel, 16 ga stainless", ["Panel bender DB 2017"], [
    ("Max. bending width", ["78.7″ (2,000 mm)"]),
    ("Max. blank size L × W", ["78.7 × 49.2″ (2,000 × 1,250 mm)"]),
    ("Max. bending height", ["6.7″ (170 mm) · 11.8″ (300 mm) on request"]),
    ("Max. thickness, mild steel", "410 N/mm²", ["14 ga (2.0 mm)"]),
    ("Max. thickness, stainless steel", "515 N/mm²", ["16 ga (1.5 mm)"]),
    ("Max. thickness, aluminum", "265 N/mm²", ["1/8″ (3.0 mm)"]),
    ("Min. bend radius", ["0.04″ (1 mm)"]),
    ("Min. four-side box, inside", ["5.5 × 7.5″ (140 × 190 mm)"]),
    ("Min. two-side box, inside", ["5.5″ (140 mm)"]),
    ("Bending speed", ["0.2 s per bend"]),
    ("Feeding speed", ["295 ft/min (90 m/min)"]),
    ("Positioning accuracy", ["0.001 mm"]),
    ("Servo axes", ["15"]),
    ("Installed / average power", ["106 HP (79 kW) installed · about 2.8 kW average"]),
    ("Noise", ["about 50 dB"]),
    ("Dimensions L × W × H", ["201 × 104 × 130″ (5,100 × 2,650 × 3,300 mm)"]),
    ("Weight", ["about 35,000 lb (16 t)"])])
PN_GK = ["bending_width", "thickness", "bending_height", "speed", "weight"]
PN_G_FROM = ["Max. bending width", "Max. thickness, mild steel", "Max. bending height", "Bending speed", "Weight"]
NOTE_PN = "Capacities are Dener's ratings for the stated tensile strengths; longer bending widths and a 300 mm bending height on request."

PANEL_FAMILIES = [
    dict(id="dn-panel", group="panel", page=P_PANEL, brand=BRAND,
         name="CNC panel bender, 79″ × 49″ blanks, 14 ga mild steel — 15 servo axes",
         short="CNC panel bender",
         models_label="DB 2017 · 1 model",
         summary="A panel bender folds all four sides of a blank — up, down, hems, boxes — in one setup, holding the sheet with a blank-holder "
                 "while the bending blades form each flange in 0.2 s; the manipulator rotates the part between sides. No tooling changes, no "
                 "operator skill, 1 mm radius bends and ±0.001 mm positioning on 15 servo axes: enclosures, doors, panels, HVAC and appliance "
                 "parts that would take a press brake a dozen handlings. 100 % electric, 2.8 kW average draw, 50 dB. Automatic loading and "
                 "unloading arms are available.",
         features=["Four-side bending of blanks to 78.7 × 49.2″ (2,000 × 1,250 mm) in one setup; flanges to 6.7″ (11.8″ on request)",
                   "15 servo axes, 0.001 mm positioning, 0.2 s per bend, 295 ft/min feeding", "14 ga mild steel, 16 ga stainless, 1/8″ aluminum; 1 mm minimum radius",
                   "High-strength cast frame; servo manipulator with brush table and pressing arm", "3D CNC with offline programming, 3D simulation and bending compensation",
                   "100 % electric — no hydraulics; about 2.8 kW average consumption, 50 dB", "CE safety; CSA-approved electrical panel"],
         optional=["Automatic loading and unloading arms", "Longer bending widths; 300 mm bending height", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"],
         images=["dn-panel-1", "dn-panel-2", "dn-panel-3", "dn-panel-7", "dn-panel-5", "dn-panel-6"],
         videos=vids(("KrQ5S2YMDlk", "DENER CNC panel bender"), ("_f6ZcqTYmNg", "DENER CNC panel bender with auto loading and unloading arms"), ("LIDHOoM8Abk", "DENER panel bender")),
         specs=spec([T_PANEL], PN_GK, PN_G_FROM, NOTE_PN)),
]
