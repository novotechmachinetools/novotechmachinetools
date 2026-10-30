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
    return f"{f:.0f} ft" if abs(f - round(f)) < 0.06 else f"{f:.1f} ft"


def length(mm):
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


def vids(*ids_titles):
    from sahinler_lib import vids as _vids      # NovoTech's own channel: id → video dict with thumb
    return _vids(*ids_titles)


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

# hybrid: (model, t, approach, bend, return, kW, energy saving %) — frame, stroke, daylight and dimensions as the XL of the same tonnage
XH = [("SVP 60", 60, 120, 10, 160, 5, None), ("SVP 80 XF", 80, 130, 10, 125, 8.7, None), ("SVP 100", 100, 200, 10, 200, 8.7, 45),
      ("SVP 125 XF", 125, 120, 10, 190, 10.8, None), ("SVP 135", 135, 170, 10, 160, 10.8, 42), ("SVP 175", 175, 170, 10, 150, 13.2, 45),
      ("SVP 220", 220, 175, 10, 160, 16.7, 51), ("SVP 320", 320, 130, 10, 150, 21.4, 55), ("SVP 400", 400, 100, 10, 100, 26.9, 58)]
XL_BY_T = {r[2]: r for r in XL}


def xh_rows():
    return [("Bending force", [tons(r[1]) for r in XH]),
            ("Bending length", "on request to 13 ft", ["up to 13 ft (4,050 mm) · 20 ft (6,050 mm) on request"] * len(XH)),
            ("Approach speed", [speed(r[2]) for r in XH]),
            ("Bending speed", [speed(r[3]) for r in XH]),
            ("Return speed", [speed(r[4]) for r in XH]),
            ("Servo motor", [hp(r[5]) for r in XH]),
            ("Energy saving vs. the XL hydraulic", [f"about {r[6]} %" if r[6] else "—" for r in XH]),
            ("Frame, stroke, daylight", ["as the XL press brake of the same tonnage"] * len(XH))]


T_XH = table("XH hybrid press brakes · SVP series", "9 tonnage packages · 66 – 441 US tons · servo-driven pump on the XL frame", [r[0] for r in XH], xh_rows())
NOTE_XH = ("The hybrid package replaces the XL's AC motor and fixed pump with a servo motor and inverter pump; tonnage packages up to 441 US tons "
           "(400 t) are available to 13 ft (4 m) bending length, longer machines on request. Frame, stroke, daylight, throat and dimensions "
           "are those of the XL press brake of the same tonnage and length.")

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

PB_STD_XL = ["X back gauge axis on ball screw and linear guides; Y1, Y2 ram axes", "15″ ESA S840 2D graphic touch-screen CNC control",
             "European-style segmented punch and die with European-style holders", "Hawe hydraulic system; constant pressure",
             "Anti-panic foot pedal with emergency stop", "Front support arms on linear rail", "Side and rear safety guards", "CSA-approved electrical panel, 600 V 3-phase standard"]
PB_OPT_XL = ["Mild hybrid drive: a servo motor and servo pump replace the AC motor and pump — the pump stops while the machine waits or is "
             "loaded and unloaded: 42 – 58 % less energy, faster approach and return, cooler oil, less noise and wear (to 400 t and 13 ft; the XL with it is the XH)",
             "21″ ESA S875 W 3D CNC control; Delem DA-66S or DA-69S 3D control", "CE-certified light barrier (DSP laser finger protection)",
             "X-R, X-R-Z1-Z2, X1-X2-R-Z1-Z2 or ATF X1-X2-R1-R2-Z1-Z2 back gauge (6 axes)", "Manual or CNC motorised crowning", "Automatic angle measurement (bending accuracy 0.05°)",
             "Sheet follower support", "Hydraulic oil cooler; electrical panel cooler; automatic lubrication", "Quick, pneumatic or Wila mechanical / hydraulic tool clamping",
             "Tandem configuration to 60 ft and 1,800 US tons", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
PB_STD_DDM = ["21″ ESA S875 W 3D CNC control", "4 axes: Y1, Y2, X, R", "European-type segmented punch and die clamping", "Side and rear safety guards; anti-panic emergency-stop pedal",
              "Electrical cabinet cooling; 380/600 V 3-phase, CSA-approved panel", "Servo-electric drive — no hydraulic oil, start/stop energy use"]
PB_OPT_DDM = ["Delem DA-66S or DA-69S 3D control", "X-R-Z1-Z2, X1-X2-R-Z1-Z2, ATF X1-X2-R1-R2-Z1-Z2 or X-Prime back gauge", "Fiessler AKAS 2 M(P) safety barrier or DSP front laser safety",
              "Manual or automatic crowning", "CE-standard light barrier; sheet follower", "Automatic angle measurement", "Pneumatic or Wila mechanical / hydraulic clamping",
              "Robot bending cell", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
PB_STD_DDS = ["15″ ESA S840 2D graphic touch-screen CNC control", "2-axis back gauge (X, R)", "European-type punch and die clamping", "Electrical cabinet cooling",
              "Ball-screw drive with Lenze servo technology — no hydraulic oil or cylinders"]
PB_OPT_DDS = ["ESA 875 W CNC control; 5-axis back gauge (X, R, Z1, Z2, X-Prime) with ESA S660", "Foldable, height-adjustable work table",
              "Wila mechanical / hydraulic clamping; double-wedge adjustable European punch holder", "Punches and dies", "DSP-AP laser finger protection", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]

# the controls Dener fits — a short note under every press brake (the buying guide on press-brake.html explains them)
CTL_XL = {"title": "ESA S840 2D as standard; ESA S875 W, Delem DA-66S or DA-69S as options",
          "text": "Every XL comes with the 15″ ESA S840 touch screen: numeric and 2D graphic programming, automatic calculation of tonnage, "
                  "bend sequence and back-gauge positions, tool library, up to 6 axes, USB and network. For shops that program from CAD or run "
                  "many different parts, Dener fits the 21″ ESA S875 W (3D programming and simulation, DXF / STEP import, EsaBend 3D), "
                  "the 24″ Delem DA-66S (2D graphic programming with a 3D machine view, Profile-S2D offline) or the 24″ Delem DA-69S "
                  "(full 3D programming and simulation, Profile-S3D) — the same four controls on every Dener press brake.",
          "images": ["ctl-esa-s840-card", "ctl-esa-s875w-card", "ctl-delem-da66s", "ctl-delem-da69s"]}
CTL_DDM = {"title": "ESA S875 W 3D as standard; Delem DA-66S or DA-69S as options",
           "text": "The DDM is delivered with the 21″ ESA S875 W: 3D programming and simulation, automatic bend sequence with collision "
                   "control, DXF / STEP import and EsaBend 3D offline software on a Windows PC. The 24″ Delem DA-66S (2D graphic, 3D "
                   "machine view) and DA-69S (3D) are the alternatives for shops standardised on Delem.",
           "images": ["ctl-esa-s875w-card", "dn-det-esabend-3d", "ctl-delem-da66s", "ctl-delem-da69s"]}
CTL_DDS = {"title": "ESA S840 2D as standard; ESA S875 W as an option",
           "text": "The small DDS carries the 15″ ESA S840 2D touch-screen control — numeric and 2D graphic programming with automatic tonnage and "
                   "sequence calculation — and can be ordered with the 21″ ESA S875 W 3D control and a 5-axis back gauge.",
           "images": ["ctl-esa-s840-card", "ctl-esa-s875w-card"]}

PB_FAMILIES = [
    dict(id="dn-xl", control=CTL_XL, group="pb-hydraulic", page=P_PB, brand=BRAND,
         name="XL hydraulic CNC press brakes, 66 – 661 US tons × 5 – 20 ft",
         short="XL hydraulic press brakes",
         models_label="XL 1560 – XL 60600 · 18 models",
         summary="The Dener XL is the hydraulic press brake most Canadian shops buy from us: a stress-relieved monoblock frame, Hawe hydraulics "
                 "at constant pressure, Y1-Y2 ram axes and an X back gauge on ball screw and linear guides, driven from a 15″ ESA S840 2D "
                 "graphic control — the operator draws the part and the control works out the sequence, tonnage and back-gauge positions. "
                 "Eighteen models from 66 US tons × 5 ft to 661 US tons × 20 ft on the same frame design: the 5 to 10 ft machines to 353 US tons "
                 "for job-shop sheet work, the 12, 13 and 20 ft machines to 661 US tons with up to 26.8″ daylight, 17.7″ stroke and a 23.6″ throat "
                 "on the 400 and 600-ton sizes for deep boxes and large profiles (the 60600 sits in a pit). European-style tooling and front "
                 "supports come with every machine; the options run from CNC crowning and 6-axis back gauges to angle measurement, sheet "
                 "followers and robot cells, and for longer work Dener builds tandem machines — two XLs on one control bending to 60 ft and "
                 "1,800 US tons.",
         features=["Monoblock welded frame, stress-relieved and machined in one setting; fixed upper table, 100 % free bending area between the housings",
                   "5 to 20 ft bending lengths, 66 to 661 US tons; 23.6″ (600 mm) throat on the 400 and 600 t machines"] + PB_STD_XL,
         optional=PB_OPT_XL,
         images=["dn-xl-1", "dn-xl-2", "dn-xl-3", "dn-xf-1", "dn-xf-2", "dn-xl-video-1", "dn-xl-video-2", "dn-xl-backgauge", "dn-xl-follower",
                 "dn-xh-4", "dn-xf-3", "dn-xl-control",
                 # the back gauge options with their axis arrows (tools/dener_bg_arrows.py)
                 "dn-det-bg-2axis", "dn-det-bg-4axis", "dn-det-bg-5axis", "dn-det-bg-6axis-atf"],
         videos=vids(("0pvdG-DYO-E", "DENER XL 3100 × 100 — 10 ft × 110 US tons CNC press brake"), ("CFkFmrRCaFc", "DENER PUMA XL 10 ft × 135 ton 6-axis CNC press brake"),
                     ("qUb8fUZr0A4", "DENER XL 5 ft × 160 ton press brake"), ("pRxr7CB2pDQ", "XL 13 ft × 220 ton with laser angle measurement and sheet follower"),
                     ("dXorm3f4fBY", "DENER XL 13 ft × 320 ton CNC hydraulic press brake"), ("_rdb1prKsxc", "20 ft × 600 ton DENER Puma XL heavy-duty press brake"),
                     ("MkaKtgulHKw", "Heavy-duty CNC hydraulic press brake PUMA XL 20 ft × 600 ton with sheet follower"),
                     ("FpHkRYeceyA", "20 ft × 1,000 ton 9-axis CNC heavy-duty press brake"), ("AGifmIGQOso", "DENER 60 ft × 1,800 ton tandem press brake with auto feeder"),
                     ("jMqwk_yyCBo", "DENER 1,600 ton × 40 ft tandem press brake installation time-lapse"), ("dsZ8f7BKP84", "Tandem press brake PUMA XL 2 × 20 ft × 320 ton"),
                     ("fG6TQ8TseSo", "Hydraulic press brake with ATF 6-axis back gauge"), ("BUFzeYAAE_Y", "Laser angle measurement system on the XL press brake"),
                     ("VGd39pN2zBM", "CNC press brake instruction with the ESA control")),
         specs=spec([T_XL], PB_GK, PB_G_FROM, NOTE_PB)),
    dict(id="dn-xl-1560", control=CTL_XL, group="pb-compact-dener", page=P_PB, brand=BRAND,
         name="XL 1560 compact CNC press brake, 66 US tons × 5 ft",
         short="XL 1560 compact press brake",
         models_label="XL 1560 · 1 model",
         summary="The smallest XL is the compact press brake of the premium line: 60 metric tons (66 US tons) over 1,550 mm (5 ft), "
                 "49″ between the frames, a 15.7″ throat and 16.1″ of daylight, on a 96 × 87″ footprint (64″ wide without the front supports) that goes through a shop door and "
                 "weighs 9,480 lb — the same stress-relieved monoblock frame, Hawe hydraulics, Y1-Y2 ram with linear scales and ball-screw X "
                 "back gauge as the big XLs, with the 15″ ESA S840 2D control, front supports on linear rail and a sectioned EUROSTAMP punch "
                 "1281 with the 4-way die 2067 in the crate. 7.5 kW, 600 V with a CSA panel. For HVAC fittings, enclosures, brackets, "
                 "signage and job-shop sheet work up to 5 ft where a 100-ton machine is more than you need — and a real CNC press brake, "
                 "not a bending brake: the control calculates tonnage, sequence and gauge positions, and the DSP laser guard, 4- to 6-axis "
                 "back gauges, CNC crowning and Wila clamping are the same options as on the 10 ft machines.",
         headline="66 US tons × 5 ft · 15.7″ throat · ESA S840 2D · 9,480 lb · EUROSTAMP 1281 / 2067 tooling included",
         features=["60 t × 1,550 mm — 16 ga to 3/16″ mild steel over the full 5 ft, 1/4″ over 4 ft (V = 8 × thickness)",
                   "Monoblock welded frame, stress-relieved and machined in one setting; 49.2″ (1,250 mm) between the frames",
                   "8.7″ (220 mm) stroke, 16.1″ (410 mm) daylight, 15.7″ (400 mm) throat for boxes and deep flanges",
                   "Ball-screw X back gauge with 25.6″ (650 mm) travel, fingers with manual R and Z adjustment and micro vernier"] + PB_STD_XL,
         optional=PB_OPT_XL,
         images=["dn-xl1560-studio", "dn-xl1560-photo-left", "dn-xl1560-photo-front", "dn-xl1560-photo-right", "dn-xl1560-control",
                 "dn-xl1560-tooling", "dn-xl1560-tooling-2", "dn-xl1560-backgauge", "dn-xl1560-backgauge-2", "dn-det-eurostamp-tools"],
         videos=vids(("qUb8fUZr0A4", "DENER XL 5 ft × 160 ton press brake — the same 5 ft frame class"), ("5FWxGB6hoJI", "XL series hydraulic CNC press brakes"),
                     ("VGd39pN2zBM", "CNC press brake instruction with the ESA control")),
         specs=spec([T_XL_1560], PB_GK, PB_G_FROM, NOTE_PB)),
    dict(id="dn-xh", control=CTL_XL, group="pb-hybrid", page=P_PB, brand=BRAND,
         name="XH mild hybrid press brakes, 66 – 441 US tons — servo motor and servo pump on the XL frame",
         short="XH mild hybrid press brakes",
         models_label="SVP 60 – SVP 400 · 9 tonnage packages",
         summary="The mild hybrid press brake is the XL with its AC motor and fixed-displacement pump replaced by a servo motor and servo "
                 "pump: the pump turns only when the ram moves, so the machine draws 42 – 58 % less energy, runs quieter, approaches and "
                 "returns 17 – 75 % faster and starts and stops with the pedal. Same frame, cylinders, stroke, daylight and equipment as the XL "
                 "of the same tonnage — the hybrid is an option on any XL to 13 ft, longer on request.",
         features=["Servo motor, drivers and inverter pump in the XL hydraulic circuit; single oil tank", "Start/stop: the pump runs only while the ram moves",
                   "42 – 58 % energy saving and 17 – 75 % faster approach and return than the XL of the same tonnage", "Less noise, less oil heating, lower maintenance"] + PB_STD_XL,
         optional=PB_OPT_XL[1:],
         images=["dn-xh-1", "dn-xh-2", "dn-xh-video", "dn-xh-3"],
         videos=vids(("vIWys546tWY", "DENER XL 10 ft × 220 ton hybrid CNC press brake"), ("nKbuxZGSjdQ", "DENER XL 12 ft × 175 ton hybrid press brake"),
                     ("-tAymdJwXjU", "DENER XL 13 ft × 220 ton hybrid press brake"), ("Msy6YHM5dIU", "DENER hybrid press brake"),
                     ("Ymz5qW36zTs", "DENER tandem 60 ft × 1,600 ton hybrid press brake with sheet following support")),
         specs=spec([T_XH], ["bending_force", "bending_length", "approach_speed", "servo_motor", "energy_saving"], ["Bending force", "Bending length", "Approach speed", "Servo motor", "Energy saving vs. the XL hydraulic"], NOTE_XH)),
    dict(id="dn-ddm", control=CTL_DDM, group="pb-servo", page=P_PB, brand=BRAND,
         name="DDM servo-electric CNC press brakes, 44 – 220 US tons × 5 – 13.4 ft",
         short="DDM servo-electric press brakes",
         models_label="DDM 4015 – DDM 20040 · 9 models",
         summary="A full-electric press brake with no hydraulic oil: servo motors drive the ram through belts and pulleys, bending at 20 mm/s on "
                 "every model — twice the speed of a hydraulic — with 0.01 mm ram repeatability and power drawn only while the ram moves. Nine "
                 "models from 44 US tons × 5 ft to 220 US tons × 13.4 ft, all with the 21″ ESA S875 W 3D control, four axes (Y1, Y2, X, R) and "
                 "European tooling as standard; robot cells, 6-axis back gauges and angle measurement as options. Quiet, clean and "
                 "fast — the machine for a job shop that bends all day.",
         features=["Servo-electric ram drive — 0.79 in/s bending speed on every model, 0.01 mm repeatability", "No hydraulic oil, pump or valves; 50 – 70 % less energy than a hydraulic brake"] + PB_STD_DDM,
         optional=PB_OPT_DDM,
         images=["dn-ddm-2", "dn-ddm-1", "dn-ddm-3", "dn-ddm-web-1", "dn-ddm-video-1", "dn-ddm-control"],
         videos=vids(("_Aqyyfk97KI", "DENER DDM 4015 — 5 ft × 40 ton servo-electric CNC press brake"), ("dlmcihzfRuI", "DENER DDM 5020 — 7 ft × 50 ton servo-electric press brake"),
                     ("ZujRJUhckG4", "DENER DDM 10030 — 10 ft × 100 ton servo-electric CNC press brake"), ("da7UnOripzc", "DENER DDM 15030 — 10 ft × 150 ton servo-electric press brake"),
                     ("30squAhhy_o", "CNC hydraulic press brake vs. servo-electric press brake"), ("qLRQDobmnXQ", "DENER DDM servo-electric press brake robot cell"),
                     ("2_Vz-v-rFqU", "DDM electric press brake with Wila hydraulic clamping"), ("IGgudJFrO-I", "DDM electric press brake bending demonstration")),
         specs=spec([T_DDM], PB_GK, PB_G_FROM, NOTE_DDM)),
    dict(id="dn-dds", control=CTL_DDS, group="pb-servo", page=P_PB, brand=BRAND,
         name="DDS ball-screw electric press brakes, 22 and 44 US tons × 3 – 4.3 ft",
         short="DDS ball-screw press brakes",
         models_label="DDS 2090 · DDS 4013 · 2 models",
         summary="The small electric press brake: Lenze servo motors on ball screws move the ram — no oil, no cylinders — in a compact "
                 "monoblock frame with a small throat for precise bends on brackets, boxes, enclosures and pans. 22 US tons × 3 ft or 44 US "
                 "tons × 4.3 ft, 14.8″ daylight, the 15″ ESA S840 control and a 2-axis back gauge as standard, a 5-axis gauge, Wila clamping "
                 "and a laser finger guard as options. Plugs into a standard panel and goes through a normal door.",
         features=["Ball-screw ram drive with Lenze servo technology; up to 50 % energy saving", "Monoblock frame, small throat, 14.8″ daylight for box bending"] + PB_STD_DDS,
         optional=PB_OPT_DDS,
         images=["dn-dds-1", "dn-dds-2", "dn-dds-video", "dn-dds-3", "dn-dds-4"],
         videos=vids(("JVG9kw1nIGk", "DENER DDS 4 ft × 30 ton ball-screw electric press brake"), ("R5D3JCTN-Ww", "Small press brake — DDS 4013 ball-screw press brake"),
                     ("Myd9TVSUFj8", "DENER DDS 2050 — 1.6 ft × 20 ton ball-screw servo-electric press brake"), ("sq1YPi0sQTU", "Bending a water-sealed pan on the DDS ball-screw press brake"),
                     ("nlCZhY7olZ8", "DDS 4013 — 100 % electric ball-screw press brake")),
         specs=spec([T_DDS], PB_GK, PB_G_FROM, NOTE_DDS)),
]

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
         images=["dn-bs-2", "dn-bs-1", "dn-bs-3", "dn-shear-video-2"],
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
         images=["dn-das-3", "dn-das-1", "dn-das-2", "dn-shear-web", "dn-shear-video-1"],
         videos=vids(("wtCPgw_5GaY", "DENER DAS 3006 — 10 ft × 1/4″ CNC hydraulic shear with pneumatic back support"), ("eQ7NqRHVSvM", "CNC hydraulic metal shear AS 3006 DENER"),
                     ("54vb6tx96aI", "NC / CNC hydraulic shears — DENER AS and BS series")),
         specs=spec([T_DAS], SH_GK, SH_G_FROM, NOTE_SH)),
]

# ------------------------------------------------------------------------------------------------ sheet lasers
POWERS = "3 / 6 / 12 / 20 / 30 / 40 kW"


def area(code):
    l, w = int(code[:-2]) * 100, int(code[-2:]) * 100
    return f"{feet(l)} × {feet(w)} · {l / 25.4:.0f} × {w / 25.4:.0f}″ ({l:,} × {w:,} mm)"


def laser_table(title, sub, prefix, codes, power, precision, speed_mmin, accel, worktable, extra=()):
    models = [f"{prefix} {c}" for c in codes]
    rows = [("Working area L × W", "nominal", [area(c) for c in codes]),
            ("Worktable", worktable),
            ("Laser source power", "options", power),
            ("Positioning accuracy", precision),
            ("Max. axis speed", mmin(speed_mmin)),
            ("Max. acceleration", accel)] + list(extra) + [("Voltage", "380 V 50/60 Hz · 600 V with transformer")]
    return table(title, sub, models, rows)


T_GFL = laser_table("GFL fiber laser cutting machines", "3 table sizes · 3 – 40 kW · pallet changer", "GFL", ["3015", "4020", "6020"], POWERS, "±0.03 mm (±0.0012″)", 120, "1.5 G",
                    "pallet changer, 2 tables", [("Z-axis stroke", "13.8″ (350 mm)")])
T_SMART_C = laser_table("Smart closed-type fiber lasers · double table", "6 table sizes · 3 – 40 kW", "Smart", ["3015", "4020", "6020", "6025", "8025", "12526"], POWERS,
                        "±0.03 mm (±0.0012″)", 140, "1 G", "double exchange table")
T_SMART_S = laser_table("Smart semi-closed fiber lasers · single table", "7 table sizes · 3 – 40 kW", "Smart", ["6025", "8025", "12525", "14035", "16045", "25031", "25040"],
                        POWERS, "±0.01 mm (±0.0004″)", 75, "0.6 G", "single table, semi-closed cabin")
T_SMART_O = laser_table("Smart open-type fiber lasers · single table", "3 table sizes · 3 – 6 kW", "Smart", ["3015", "4020", "6020"], "3 / 6 kW", "±0.03 mm (±0.0012″)", 110, "1 G",
                        "single table, open")
LS_GK = ["working_area", "power", "speed", "accel", "worktable"]
LS_G_FROM = ["Working area L × W", "Laser source power", "Max. axis speed", "Max. acceleration", "Worktable"]
NOTE_LS = ("The model number gives the nominal working area (3015 = 3,000 × 1,500 mm); every table size is available with any of the listed "
           "laser sources. Cutting thickness depends on the source: as a guide, 6 kW cuts 3/4″ mild steel, 12 kW 1″ and 20 kW 1-1/2″ — ask us "
           "for the cutting chart for your material.")
LS_STD = ["Fiber laser source (IPG, Raycus or nLIGHT), Precitec or Raytools cutting head with autofocus", "Stress-relieved welded frame; space-frame bridge for high acceleration",
          "Exchange table / pallet changer so loading overlaps cutting", "Pneumatic fume-extraction compartments and scrap boxes on wheels; prepared for a dust collector",
          "CNC control with nesting software, cutting database and production reports; remote diagnostics", "Laser-safe viewing glass; CE safety",
          "Chiller, air/nitrogen/oxygen assist-gas system", "CSA-approved electrical panel; 600 V with transformer"]
LS_OPT = ["Automatic loading / unloading tower", "Sheet storage automation", "Bevel cutting head", "Film-removal and marking functions", "Dust collector", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]

LASER_FAMILIES = [
    dict(id="dn-gfl", group="laser-gfl", page=P_LASER, brand=BRAND,
         name="GFL fiber laser cutting machines, 5 × 10 to 6.6 × 20 ft, 3 – 40 kW",
         short="GFL fiber lasers",
         models_label="GFL 3015 · 4020 · 6020 · 3 – 40 kW",
         summary="The GFL is Dener's production sheet laser: a gantry on a stress-relieved frame accelerating at 1.5 G to 394 ft/min, with a "
                 "pallet changer so the next sheet is loaded while the first is cut. Three table sizes — 5 × 10, 6.6 × 13 and 6.6 × 20 ft — with "
                 "fiber sources from 3 to 40 kW, a Precitec autofocus head, nesting software and production reports on the control, and the "
                 "pneumatic extraction and scrap boxes that keep the floor clean. The machine for a job shop that cuts all day.",
         features=["1.5 G acceleration, 394 ft/min (120 m/min) axis speed, ±0.03 mm positioning", "3 to 40 kW fiber sources; 6 kW cuts 3/4″ mild steel, 12 kW 1″"] + LS_STD,
         optional=LS_OPT,
         images=["dn-gfl-3", "dn-gfl-2", "dn-gfl-1", "dn-gfl-video-1", "dn-gfl-video-2", "dn-gfl-control"],
         videos=vids(("P3ynLUu2VYU", "DENER GFL 10 × 5 ft 6 kW laser cutting machine"), ("VjuvZWb_O_g", "DENER GFL laser cutting machine"),
                     ("0Cz5xYoNVec", "DENER GFL laser cutting machine"), ("NxTq4uw3n5k", "DENER GFL laser cutting machine"),
                     ("L9fTrifVFiA", "DENER 6 kW / 4 kW / 2 kW fiber laser cutting comparison"), ("C0mG6rJkHdU", "6 kW fiber laser cutting 15 mm mild steel"),
                     ("EFTY5a-Ri1Q", "Intelligent air cutting — a smarter solution beyond traditional air cutting")),
         specs=spec([T_GFL], LS_GK, LS_G_FROM, NOTE_LS)),
    dict(id="dn-smart-closed", group="laser-smart", page=P_LASER, brand=BRAND,
         name="Smart closed-type fiber lasers with double table, 5 × 10 to 8.5 × 41 ft, 3 – 40 kW",
         short="Smart closed-type lasers",
         models_label="Smart 3015 – 12526 · 6 table sizes · 3 – 40 kW",
         summary="The Smart series is the economy sheet laser from the same Turkish factory: a fully enclosed cabin with laser-safe glass, a double "
                 "exchange table and 459 ft/min at 1 G, in six table sizes from 5 × 10 ft to a 41 ft long bed. The same fiber sources, cutting "
                 "heads and software as the GFL, built to a lower price with a lighter frame and simpler cabin. Open front for the cutting "
                 "area, control and remote handset.",
         features=["Closed cabin with laser-safe viewing glass; double exchange table", "1 G acceleration, 459 ft/min (140 m/min) axis speed, ±0.03 mm positioning"] + LS_STD,
         optional=LS_OPT,
         images=["dn-smart-1", "dn-smart-2", "dn-laser-web"],
         videos=vids(("4Yp6X9tP6J8", "DENER SMART series laser cutting machine"), ("zDGupa7NevE", "Dener fiber laser cutting machine"),
                     ("9J_m5e1Z7-M", "Fiber laser FL 6020 6 kW — new features for high speed and performance"), ("oM9GCeSY9EI", "Very fast fiber laser cut steel by Dener")),
         specs=spec([T_SMART_C], LS_GK, LS_G_FROM, NOTE_LS)),
    dict(id="dn-smart-semi", group="laser-smart", page=P_LASER, brand=BRAND,
         name="Smart semi-closed fiber lasers with single table, 8.2 × 20 to 13 × 82 ft, 3 – 40 kW",
         short="Smart semi-closed lasers",
         models_label="Smart 6025 – 25040 · 7 table sizes · 3 – 40 kW",
         summary="The large-format Smart: a single table from 8.2 × 20 ft to 13 × 82 ft under a semi-closed cabin, for long plates, beams and "
                 "parts that do not fit a standard sheet. ±0.01 mm positioning, 246 ft/min and 3 to 40 kW sources — the 20 – 40 kW machines "
                 "cut 1-1/2″ plate and thicker.",
         features=["Single table to 13 × 82 ft (4 × 25 m) under a semi-closed cabin", "±0.01 mm positioning, 246 ft/min (75 m/min), 0.6 G"] + LS_STD,
         optional=LS_OPT,
         images=["dn-smart-2"],
         videos=[],
         specs=spec([T_SMART_S], LS_GK, LS_G_FROM, NOTE_LS)),
    dict(id="dn-smart-open", group="laser-smart", page=P_LASER, brand=BRAND,
         name="Smart open-type fiber lasers, 5 × 10 to 6.6 × 20 ft, 3 – 6 kW",
         short="Smart open-type lasers",
         models_label="Smart 3015 · 4020 · 6020 · 3 – 6 kW",
         summary="The entry sheet laser: an open single-table machine with a 3 or 6 kW source, 361 ft/min at 1 G, in 5 × 10, 6.6 × 13 and 6.6 × "
                 "20 ft. Maximum access to the table for odd sheets and manual loading; the lowest-cost way into fiber laser cutting from a "
                 "builder that also makes the 40 kW machines.",
         features=["Open single table — full access for loading; 3 or 6 kW source", "1 G acceleration, 361 ft/min (110 m/min), ±0.03 mm positioning"] + LS_STD[:1] + LS_STD[3:],
         optional=LS_OPT,
         images=["dn-smart-1"],
         videos=[],
         specs=spec([T_SMART_O], LS_GK, LS_G_FROM, NOTE_LS)),
]

# ------------------------------------------------------------------------------------------------ tube lasers
TL_POWERS = "3 / 6 / 12 / 20 kW"
T_FTL = table("FTL tube and profile fiber lasers", "4 chuck sizes · Ø0.6″ – 25.2″ · 3 – 20 kW", ["FTL 250", "FTL 350", "FTL 500", "FTL 640"], [
    ("Tube diameter", "round", ["Ø0.6 – 9.8″ (Ø15 – 250 mm)", "Ø1.2 – 13.8″ (Ø30 – 350 mm)", "Ø1.2 – 19.7″ (Ø30 – 500 mm)", "Ø4.7 – 25.2″ (Ø120 – 640 mm)"]),
    ("Profile size", "square / rectangular", ["0.6 – 9.8″ (15 – 250 mm)", "1.2 – 13.8″ (30 – 350 mm)", "1.2 – 19.7″ (30 – 500 mm)", "4.7 – 25.2″ (120 – 640 mm)"]),
    ("Laser source power", "options", TL_POWERS),
    ("Max. tube length and weight", ["19.7 ft, 1,323 lb (6 m, 600 kg) · 39.4 ft, 26,455 lb (12 m, 12,000 kg)", "29.5 ft, 2,205 lb (9 m, 1,000 kg) · 39.4 ft, 3,086 lb (12 m, 1,400 kg)",
                                     "39.4 ft, 4,630 lb (12 m, 2,100 kg)", "39.4 ft, 5,732 lb (12 m, 2,600 kg)"]),
    ("Max. speed", [mmin(80), mmin(54), mmin(25), mmin(25)]),
    ("Max. acceleration", "0.6 G"),
    ("Repeatability", ["±0.05 mm (±0.002″)", "±0.05 mm (±0.002″)", "±0.1 mm (±0.004″)", "±0.1 mm (±0.004″)"]),
    ("Voltage", "380 V 50/60 Hz · 600 V with transformer")])
T_EFTL = table("E-FTL tube and profile fiber lasers", "4 chuck sizes · Ø0.3″ – 13.8″ · 3 – 20 kW · 1 G", ["E-FTL 120", "E-FTL 180", "E-FTL 250", "E-FTL 350"], [
    ("Tube diameter", "round", ["Ø0.3 – 4.7″ (Ø8 – 120 mm)", "Ø0.4 – 7.1″ (Ø10 – 180 mm)", "Ø0.6 – 9.8″ (Ø15 – 250 mm)", "Ø1.2 – 13.8″ (Ø30 – 350 mm)"]),
    ("Profile size", "square / rectangular", ["0.3 – 4.7″ (8 – 120 mm)", "0.4 – 7.1″ (10 – 180 mm)", "0.6 – 9.8″ (15 – 250 mm)", "1.2 – 13.8″ (30 – 350 mm)"]),
    ("Laser source power", "options", TL_POWERS),
    ("Max. tube length and weight", ["23 ft, 265 lb (7 m, 120 kg)", "23 ft, 529 lb (7 m, 240 kg)", "23 ft, 661 lb · 29.5 ft, 970 lb · 39.4 ft, 2,646 lb (7 / 9 / 12 m, 300 / 440 / 1,200 kg)",
                                     "23 ft, 1,323 lb · 29.5 ft, 2,646 lb · 39.4 ft, 3,968 lb (7 / 9 / 12 m, 600 / 1,200 / 1,800 kg)"]),
    ("Max. speed", [mmin(120), mmin(120), mmin(80), mmin(54)]),
    ("Max. acceleration", "1 G"),
    ("Repeatability", "±0.05 mm (±0.002″)"),
    ("Voltage", "380 V 50/60 Hz · 600 V with transformer")])
TL_GK = ["tube", "profile", "power", "speed", "length"]
TL_G_FROM = ["Tube diameter", "Profile size", "Laser source power", "Max. speed", "Max. tube length and weight"]
NOTE_TL = ("Chuck size is the model number (250 = Ø250 mm); every chuck size is available with any of the listed laser sources. Loading length "
           "and bundle loader to suit the tube length; ask us for the cutting chart for your tube wall and material.")
TL_STD = ["Fiber laser source 3 – 20 kW, autofocus cutting head", "Front and rear pneumatic chucks with automatic centring; 3D cutting head for bevels and copes on the 5-axis versions",
          "Automatic loader for bundles; tube supports that follow the cut; unloading table", "CNC with tube nesting and import of STEP / IGES files; cutting database",
          "Fume extraction through the tube; chip and slug collection", "CE safety enclosure", "CSA-approved electrical panel; 600 V with transformer"]
TL_OPT = ["Bevel (3D) cutting head", "Longer loading and unloading, 29.5 and 39.4 ft (9 / 12 m)", "Seam detection; tapping and drilling attachments", "Dust collector", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]

TUBE_FAMILIES = [
    dict(id="dn-eftl", group="tube-eftl", page=P_TUBE, brand=BRAND,
         name="E-FTL tube and profile laser cutters, Ø0.3″ – 13.8″, 3 – 20 kW",
         short="E-FTL tube lasers",
         models_label="E-FTL 120 · 180 · 250 · 350",
         summary="The fast tube laser: servo axes accelerating at 1 G move the chucks at up to 394 ft/min, cutting round, square, rectangular and "
                 "open profiles from Ø0.3″ to 13.8″ in 7, 9 or 12 m lengths with ±0.05 mm repeatability. Four chuck sizes and 3 to 20 kW sources, "
                 "with the bundle loader, following supports and tube nesting software that turn a bar of tube into finished parts without an "
                 "operator at the machine.",
         features=["Ø0.3 – 13.8″ (8 – 350 mm) round and profile; 1 G, 394 ft/min (120 m/min)", "Tube length to 39.4 ft (12 m) with automatic bundle loader"] + TL_STD,
         optional=TL_OPT,
         images=["dn-tube-2", "dn-tube-1", "dn-tube-3"],
         videos=vids(("n4gFLrlC-es", "DENER E-FTL tube laser cutting machine with auto loader"), ("6_UQ6NBUUO4", "DENER E-FTL tube laser cutting machine")),
         specs=spec([T_EFTL], TL_GK, TL_G_FROM, NOTE_TL)),
    dict(id="dn-ftl", group="tube-ftl", page=P_TUBE, brand=BRAND,
         name="FTL tube and profile laser cutters, Ø0.6″ – 25.2″, 3 – 20 kW",
         short="FTL tube lasers",
         models_label="FTL 250 · 350 · 500 · 640",
         summary="The heavy tube laser: four chuck sizes from Ø250 to Ø640 mm for structural tube, pipe and beams to 25.2″ across and 12 m long, "
                 "up to 2,600 kg per bar on the 640 chuck and 12,000 kg on the long-bed 250 version. 3 to 20 kW sources cut wall thicknesses to "
                 "1″; the 5-axis head cuts bevels and weld preparations. For steel-construction, trailer, agricultural and equipment "
                 "builders.",
         features=["Ø0.6 – 25.2″ (15 – 640 mm) round and profile; bars to 39.4 ft (12 m) and 5,732 lb", "3 to 20 kW sources; 5-axis bevel head"] + TL_STD,
         optional=TL_OPT,
         images=["dn-tube-6", "dn-tube-4", "dn-tube-5", "dn-tube-7"],
         videos=vids(("zPexjUvz7jg", "DENER FTL tube laser cutting machine")),
         specs=spec([T_FTL], TL_GK, TL_G_FROM, NOTE_TL)),
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
