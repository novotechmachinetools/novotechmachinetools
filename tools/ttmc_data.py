#!/usr/bin/env python3
"""NovoTech sheet metal shears — the value-line shears for the sheet-metal shop, built in China (by TTMC) and sold under
NovoTech's name without the supplier's brand (sheet-metal-shears.html, under the shear-cutting hub).

Metric data from the supplier's Vol. 23 catalogue, pages 107 – 114: PS pneumatic shear, THS / HQ01 / HQ11 hydraulic shears,
Q11 electric shears (manual and NC) and the Q11 mechanical shears.  Shown as imperial (metric) like the rest of the site.
The supplier's QC11Y guillotine and QC12Y swing beam ranges are NOT listed — they are the same machines as the NovoTech
value-line QC12K / Q11K hydraulic shears on hydraulic-shearing-machine.html.
"""
P_SHEAR = "sheet-metal-shears"
BRAND = "novotech"

CAP = {1.5: "16 ga", 1.6: "16 ga", 2.0: "14 ga", 2.5: "12 ga", 3.0: "1/8″", 4.0: "5/32″", 4.5: "3/16″", 6.0: "1/4″", 6.5: "1/4″", 8.0: "5/16″", 10.0: "3/8″"}
HP = {2.2: "3", 3.0: "4", 4.0: "5.5", 5.5: "7.5", 7.5: "10", 11.0: "15", 15.0: "20"}


def cap(mm):
    return f"{CAP[mm]} ({mm:g} mm)"


def inch(mm, nd=1):
    return f"{mm / 25.4:,.{nd}f}″ ({mm:,} mm)"


def feet(mm):
    f = mm / 304.8
    return f"{f:.0f} ft" if abs(f - round(f)) < 0.06 else f"{f:.1f} ft"


def motor(kw):
    return f"{HP[kw]} HP ({kw:g} kW)"


def packing(cm):
    l, w, h = cm
    return f"{l / 2.54:.0f} × {w / 2.54:.0f} × {h / 2.54:.0f}″ ({l} × {w} × {h} cm)"


def weight(kg):
    return f"{round(kg * 2.20462):,} lb ({kg:,} kg)"


GK = ["capacity", "length", "strokes", "motor", "weight"]
NOTE = ("Capacities are the manufacturer's ratings for mild steel over the full blade length; count on about 60 % of the thickness in "
        "stainless steel and the full thickness and more in aluminum. Metric values in brackets are the manufacturer's nominal figures; "
        "packing size is the shipping crate L × W × H, weight is the net weight of the machine.")


def table(title, sub, models, rows):
    """rows: [(label, [cell per model], key)] — key marks the five 'at a glance' rows in GK order (capacity, length, strokes, motor, weight)."""
    return {"title": title, "sub": sub, "models": models, "rows": [{"label": lab, "sub": "", "cells": cells, "key": key} for lab, cells, key in rows]}


def spec(tables, glance_rows, note=NOTE):
    """glance_rows: the five row labels (in GK order) the glance is read from."""
    models = []
    for t in tables:
        rr = {r["label"]: r["cells"] for r in t["rows"]}
        for i, m in enumerate(t["models"]):
            models.append({"name": m, "glance": [rr[l][i] if l else "—" for l in glance_rows]})
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": GK, "caps": {}, "note": note}


# ---------------------------------------------------------------------------------------------------------- pneumatic
PS = table("PS", "Pneumatic shear", ["PS-1.5x1320"],
           [("Shearing capacity, mild steel", [cap(1.5)], True), ("Max shearing width", [inch(1320)], True),
            ("Strokes per minute", ["40 strokes/min"], True), ("Back gauge", [inch(750)], False), ("Front gauge", [inch(535)], False),
            ("Air pressure", ["85 – 100 psi (0.6 – 0.7 MPa)"], True), ("Air consumption per stroke", ["1.4 CFM"], False),
            ("Packing size L × W × H", [packing((175, 75, 123))], False), ("Weight", [weight(570)], False)])

# ---------------------------------------------------------------------------------------------------------- hydraulic
# (model, cap mm, width mm, strokes, kW, packing cm, kg)
THS = [("THS-1320X2.5", 2.5, 1320, 20, 2.2, (173, 83, 130), 640), ("THS-1320X4", 4.0, 1320, 15, 4.0, (201, 104, 158), 1270),
       ("THS-1520X4", 4.0, 1520, 15, 4.0, (223, 104, 160), 1450), ("THS-2030X4", 4.0, 2032, 15, 4.0, (273, 104, 160), 1700),
       ("THS-2540X4", 4.0, 2540, 13, 5.5, (326, 113, 170), 2590), ("THS-3050X4", 4.0, 3048, 13, 5.5, (377, 113, 170), 2900)]
T_THS = table("THS", "Hydraulic shears with front and back gauges", [r[0] for r in THS],
              [("Shearing capacity, mild steel", [cap(r[1]) for r in THS], True), ("Max shearing width", [inch(r[2]) for r in THS], True),
               ("Strokes per minute", [f"{r[3]} strokes/min" for r in THS], True), ("Motor power", [motor(r[4]) for r in THS], True),
               ("Back gauge", [inch(650) for r in THS], False), ("Front gauge", [inch(600) for r in THS], False),
               ("Packing size L × W × H", [packing(r[5]) for r in THS], False), ("Weight", [weight(r[6]) for r in THS], True)])

# (model, cap mm, width mm, kW, kg, packing)
HQ01 = [("HQ01-2x1320B", 2.0, 1320, 2.2, 550, (198, 92, 143)), ("HQ01-1.6x2500B", 1.6, 2500, 2.2, 1140, (314, 99, 143))]
T_HQ01 = table("HQ01", "Light hydraulic shears", [r[0] for r in HQ01],
               [("Shearing capacity, mild steel", [cap(r[1]) for r in HQ01], True), ("Max shearing length", [inch(r[2]) for r in HQ01], True),
                ("Motor power", [motor(r[3]) for r in HQ01], True), ("Back gauge", [inch(800) for r in HQ01], False),
                ("Work table height", [inch(880) for r in HQ01], False), ("Packing size L × W × H", [packing(r[5]) for r in HQ01], False),
                ("Weight", [weight(r[4]) for r in HQ01], True)])

# (model, cap mm, width mm, angle, strokes, kW, back gauge text, packing, kg)
HQ11 = [("HQ11-6.5x1300", 6.5, 1300, "2.5°", 20, 5.5, "24.8″ (630 mm), electric", (215, 175, 181), 2470),
        ("HQ11-4.5x2000", 4.5, 2000, "2°", 18, 7.5, "24.8″ (630 mm), manual", (285, 116, 185), 2900),
        ("HQ11-4x2500", 4.0, 2500, "1.7°", 16, 7.5, "24.8″ (630 mm), manual", (335, 116, 185), 3330),
        ("HQ11-6.5x3050", 6.5, 3050, "2°", 12, 15.0, "36.2″ (920 mm), electric", (413, 210, 190), 6095)]
T_HQ11 = table("HQ11", "Hydraulic shears with quick-set blade clearance", [r[0] for r in HQ11],
               [("Shearing capacity, mild steel", [cap(r[1]) for r in HQ11], True), ("Max shearing width", [inch(r[2]) for r in HQ11], True),
                ("Shearing angle", [r[3] for r in HQ11], False), ("Strokes per minute", [f"{r[4]} strokes/min" for r in HQ11], True),
                ("Motor power", [motor(r[5]) for r in HQ11], True), ("Back gauge", [r[6] for r in HQ11], False),
                ("Packing size L × W × H", [packing(r[7]) for r in HQ11], False), ("Weight", [weight(r[8]) for r in HQ11], True)])

# ---------------------------------------------------------------------------------------------------------- electric
# (model, cap mm, width mm, angle, strokes, kW, back gauge mm, packing, kg)
Q11 = [("Q11-3x1250", 3.0, 1250, "2°", 30, 3.0, 630, (184, 103, 131), 850), ("Q11-2x2050", 2.0, 2050, "2°", 30, 3.0, 630, (266, 116, 147), 1360),
       ("Q11-3x2050", 3.0, 2050, "2°", 30, 4.0, 630, (266, 116, 147), 1520), ("Q11-4x1250", 4.0, 1250, "2.4°", 30, 4.0, 630, (187, 115, 145), 1185),
       ("Q11-3x1250A", 3.0, 1250, "2°", 28, 4.0, 635, (184, 117, 133), 980)]
Q11NC = [("Q11-4x1300NC", 4.0, 1300, "2.4°", 30, 4.0, 630, (191, 116, 145), 1355), ("Q11-2x2550NC", 2.0, 2550, "1.6°", 30, 4.0, 630, (320, 116, 148), 1900),
         ("Q11-4x2550NC", 4.0, 2550, "1.8°", 30, 7.5, 630, (325, 116, 155), 2500)]


def t_q11(title, sub, data):
    return table(title, sub, [r[0] for r in data],
                 [("Shearing capacity, mild steel", [cap(r[1]) for r in data], True), ("Max shearing width", [inch(r[2]) for r in data], True),
                  ("Shearing angle", [r[3] for r in data], False), ("Strokes per minute", [f"{r[4]} strokes/min" for r in data], True),
                  ("Motor power", [motor(r[5]) for r in data], True), ("Back gauge", [inch(r[6]) for r in data], False),
                  ("Packing size L × W × H", [packing(r[7]) for r in data], False), ("Weight", [weight(r[8]) for r in data], True)])


# ---------------------------------------------------------------------------------------------------------- mechanical
# (model, cap mm, width mm, angle, strokes, kW, back gauge mm, packing, kg)
Q11M = [("Q11-3x1300", 3.0, 1300, "2°", 55, 3.0, 350, (220, 132, 145), 1350), ("Q11-3x1500", 3.0, 1500, "2°", 55, 3.0, 350, (240, 130, 144), 1500),
        ("Q11-4x2000", 4.0, 2000, "2°", 45, 5.5, 500, (318, 151, 149), 3000), ("Q11-4x2500", 4.0, 2500, "2°", 45, 5.5, 500, (370, 151, 149), 3600),
        ("Q11-6x2000", 6.0, 2000, "2°", 50, 7.5, 500, (328, 170, 182), 3930), ("Q11-6x2500", 6.0, 2500, "2°", 50, 11.0, 500, (378, 170, 182), 5200),
        ("Q11-8x2000", 8.0, 2000, "2°", 50, 11.0, 500, (335, 175, 182), 4500), ("Q11-8x2500", 8.0, 2500, "2°", 50, 11.0, 500, (390, 227, 244), 6800),
        ("Q11-10x1000", 10.0, 1000, "3°", 50, 11.0, 500, (240, 175, 182), 3500), ("Q11-10x1500", 10.0, 1500, "3°", 50, 15.0, 500, (290, 175, 182), 4000)]

G5 = ["Shearing capacity, mild steel", "Max shearing width", "Strokes per minute", "Motor power", "Weight"]
G5_HQ01 = ["Shearing capacity, mild steel", "Max shearing length", None, "Motor power", "Weight"]
G5_PS = ["Shearing capacity, mild steel", "Max shearing width", "Strokes per minute", "Air pressure", "Weight"]

STD_HYD = ["Mobile 24 V foot pedal switch with emergency stop", "Front gauge arms with squaring guide and back gauge, both with fine adjustment",
           "High-chromium blades with two cutting edges — turn the blade for a second life", "Steel-welded frame; hydraulic hold-downs ahead of the blade",
           "CSA-approved electrical panel; 600 V 3-phase with transformer (208 / 240 / 480 V on request)"]
OPT_HYD = ["Photoelectric rear protection", "Electric back gauge (HQ11)", "NC back gauge control (HQ11)", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]
STD_EL = ["Manual back gauge with millimetre counter, 24.8″ (630 mm) travel", "Mobile 24 V foot switch; bench angle stop; cutting line lighting",
          "Automatic rubber-coated sheet hold-down", "Two-sided shear blades", "CSA-approved electrical panel; 600 V 3-phase with transformer (208 / 240 / 480 V on request)"]
OPT_EL = ["Electric back gauge (except Q11-2x2050 and Q11-3x1250A)", "Light curtain rear guard and pneumatic sheet catcher (standard on the A model)",
          "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]
STD_NC = ["PLC control with graphical touch-screen; motorised back gauge with manual fine adjustment", "Cutting line lighting; mobile 24 V foot switch",
          "Rear guarding with interlock; sheet hold-downs with rolling balls", "Pneumatic sheet catcher", "Two-sided shear blades",
          "CSA-approved electrical panel; 600 V 3-phase with transformer (208 / 240 / 480 V on request)"]
OPT_NC = ["Front sheet pallet for stacking", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]
STD_MECH = ["Flywheel and clutch drive — one stroke per pedal press, 45 to 55 strokes a minute", "Back gauge with fine adjustment, 13.8″ or 19.7″ (350 / 500 mm) travel",
            "Mechanical hold-downs; long-life high-quality blades", "Simple, rugged construction for medium and thick steel",
            "CSA-approved electrical panel; 600 V 3-phase with transformer (208 / 240 / 480 V on request)"]
OPT_MECH = ["Rear guard with photocell", "Front sheet support arms", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]

FAMILIES = [
    dict(id="tt-ps", group="sh-light", page=P_SHEAR, brand=BRAND,
         name="PS pneumatic shear, 16 ga × 52″",
         short="PS pneumatic shear",
         models_label="PS-1.5x1320 · 1 model",
         summary="The shear for a shop that already has compressed air: a pneumatic cylinder drives the cutting beam through 16 ga (1.5 mm) mild "
                 "steel over 52″ at 40 strokes a minute, with no motor, no hydraulics and nothing to warm up. A low cutting angle cuts narrow strips "
                 "without twisting; the bed and beam are aligned at the factory for accuracy; front and back gauges with fine adjustment, a mobile "
                 "24 V foot pedal and a complete pneumatic control set are standard. 1,257 lb, runs on 85 – 100 psi shop air.",
         features=["16 ga (1.5 mm) mild steel × 52″ (1,320 mm); 40 strokes per minute on 85 – 100 psi shop air", "Pneumatic cylinder drive with filter, regulator and lubricator",
                   "Low cutting angle for narrow strips without twist; factory-aligned bed and beam", "Back gauge 29.5″ (750 mm) with indicator; front gauge 21″ (535 mm)",
                   "Mobile 24 V foot pedal switch"],
         optional=["Photoelectric rear protection", "Sheet support arms"],
         images=["tt-ps", "tt-ps-gauge", "tt-ps-control", "tt-ps-cylinder"],
         videos=[],
         specs=spec([PS], G5_PS)),
    dict(id="tt-hq01", group="sh-light", page=P_SHEAR, brand=BRAND,
         name="HQ01 light hydraulic shears, 16 – 14 ga × 52 – 98″",
         short="HQ01 light hydraulic shears",
         models_label="HQ01-2x1320B · HQ01-1.6x2500B · 2 models",
         summary="The light hydraulic shear for HVAC, ductwork and signage: a 3 HP power pack and one cylinder cut 14 ga (2 mm) over 52″ or 16 ga "
                 "over 98″ with hydraulic control, a roving foot pedal, an adjustable back gauge for repeatable widths and front sheet supports with "
                 "a squaring guide. A fenced rear guard is standard; photoelectric protection is optional. From 1,213 lb — the lowest-priced "
                 "powered shear in the range.",
         features=["14 ga (2 mm) × 52″ or 16 ga (1.6 mm) × 98″ mild steel; 3 HP hydraulic power pack", "Adjustable back gauge, 31.5″ (800 mm) travel, for precise repeatability",
                   "Roving foot pedal control; automatic and single-stroke switching", "Front sheet supports and squaring guide; rear guard fence",
                   "Work table height 34.6″ (880 mm)"],
         optional=["Photoelectric rear protection", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"],
         images=["tt-hq01", "tt-hq01-gauge", "tt-hq01-switch", "tt-hq01-photocell"],
         videos=[],
         specs=spec([T_HQ01], G5_HQ01)),
    dict(id="tt-ths", group="sh-hydraulic", page=P_SHEAR, brand=BRAND,
         name="THS hydraulic shears, 12 ga – 5/32″ × 52 – 120″",
         short="THS hydraulic shears",
         models_label="THS-1320X2.5 – THS-3050X4 · 6 models",
         summary="The steel-welded hydraulic shear for precision shearing of mild steel: 12 ga (2.5 mm) over 52″ on the 1320X2.5, and 5/32″ (4 mm) "
                 "over 52″ to 120″ on the X4 models, 13 to 20 strokes a minute from a 3 to 7.5 HP power pack. Front gauge arms and a back gauge, "
                 "both with fine adjustment, a mobile 24 V foot pedal and high-chromium two-edged blades that are turned for a second life are "
                 "standard. From 1,411 to 6,393 lb.",
         features=["12 ga (2.5 mm) or 5/32″ (4 mm) mild steel × 52 – 120″ (1,320 – 3,048 mm); 13 – 20 strokes per minute",
                   "Back gauge 25.6″ (650 mm) and front gauge 23.6″ (600 mm), both with fine adjustment"] + STD_HYD,
         optional=OPT_HYD[:1] + OPT_HYD[3:],
         images=["tt-ths", "tt-ths-gauge"],
         videos=[],
         specs=spec([T_THS], G5)),
    dict(id="tt-hq11", group="sh-hydraulic", page=P_SHEAR, brand=BRAND,
         name="HQ11 hydraulic shears, 5/32″ – 1/4″ × 51 – 120″",
         short="HQ11 hydraulic shears",
         models_label="HQ11-6.5x1300 – HQ11-6.5x3050 · 4 models",
         summary="The hydraulic shear for sheet and non-ferrous sheet metal in a production shop: 1/4″ (6.5 mm) over 51″ and 120″, 3/16″ over 79″ "
                 "and 5/32″ over 98″, 12 to 20 strokes a minute from 7.5 to 20 HP. Blade clearance is set by a quick-set device, the cutting "
                 "angle can be adjusted, and the low cutting angle and shearing direction keep bowing and twist to a minimum. Ball-transfer "
                 "table, hold-downs, lubrication pump and a mobile foot pedal are standard; the 1300 and 3050 come with an electric back gauge, "
                 "the 2000 and 2500 with a manual one; an NC back gauge is optional. 5,445 to 13,437 lb.",
         features=["5/32″ to 1/4″ (4 – 6.5 mm) mild steel × 51 – 120″ (1,300 – 3,050 mm); 12 – 20 strokes per minute", "Quick-set blade clearance and adjustable cutting angle (1.7 – 2.5°)",
                   "Ball-transfer table; hydraulic hold-downs; lubrication pump", "Back gauge 24.8″ (630 mm) manual or electric; 36.2″ (920 mm) electric on the 3050"] + STD_HYD[:1] + STD_HYD[2:],
         optional=OPT_HYD,
         images=["tt-hq11", "tt-hq11-table", "tt-hq11-egauge", "tt-hq11-mgauge", "tt-hq11-pump"],
         videos=[],
         specs=spec([T_HQ11], G5)),
    dict(id="tt-q11", group="sh-electric", page=P_SHEAR, brand=BRAND,
         name="Q11 electric shears, 14 ga – 5/32″ × 49 – 81″",
         short="Q11 electric shears",
         models_label="Q11-3x1250 – Q11-3x1250A · 5 models",
         summary="The electric shear for the sheet-metal shop: a 4 or 5.5 HP motor drives the beam through a gearbox for 28 to 30 strokes a minute "
                 "in 1/8″ (3 mm) mild steel over 49″ or 81″, 14 ga over 81″ and 5/32″ over 49″ — no hydraulics, nothing to warm up. A manual "
                 "back gauge with millimetre counter, a bench angle stop, cutting line lighting, an automatic rubber-coated hold-down and a mobile "
                 "foot switch are standard; the Q11-3x1250A adds a light-curtain rear guard and a pneumatic sheet catcher. From 1,874 lb.",
         features=["14 ga to 5/32″ (2 – 4 mm) mild steel × 49 – 81″ (1,250 – 2,050 mm); 28 – 30 strokes per minute",
                   "Q11-3x1250A: light-curtain back safety system, pneumatic sheet catcher, front sheet pallet for stacking"] + STD_EL,
         optional=OPT_EL,
         images=["tt-q11a", "tt-q11", "tt-q11a-rear", "tt-q11-gauge", "tt-q11-stop"],
         videos=[],
         specs=spec([t_q11("Q11", "Electric shears with manual back gauge", Q11)], G5)),
    dict(id="tt-q11nc", group="sh-electric", page=P_SHEAR, brand=BRAND,
         name="Q11 NC electric shears with PLC control, 14 ga – 5/32″ × 51 – 100″",
         short="Q11 NC electric shears",
         models_label="Q11-4x1300NC · Q11-2x2550NC · Q11-4x2550NC · 3 models",
         summary="The electric shear with a PLC: a graphical touch-screen control, a motorised back gauge with manual fine adjustment, cutting "
                 "line lighting, sheet hold-downs with rolling balls, an interlocked rear guard and a pneumatic sheet catcher — 5/32″ (4 mm) "
                 "over 51″ or 100″, 14 ga over 100″, 30 strokes a minute from 5.5 or 10 HP. The two-sided blades are turned for a second edge. "
                 "2,987 to 5,512 lb.",
         features=["14 ga to 5/32″ (2 – 4 mm) mild steel × 51 – 100″ (1,300 – 2,550 mm); 30 strokes per minute; cutting angle 1.6 – 2.4°"] + STD_NC,
         optional=OPT_NC,
         images=["tt-q11nc", "tt-q11nc-rear", "tt-q11nc-screen", "tt-q11nc-gauge", "tt-q11nc-balls", "tt-q11nc-light"],
         videos=[],
         specs=spec([t_q11("Q11 NC", "Electric shears with PLC control and motorised back gauge", Q11NC)], G5)),
    dict(id="tt-q11-mech", group="sh-mechanical", page=P_SHEAR, brand=BRAND,
         name="Q11 mechanical shears, 1/8″ – 3/8″ × 39 – 98″",
         short="Q11 mechanical shears",
         models_label="Q11-3x1300 – Q11-10x1500 · 10 models",
         summary="The classic flywheel shear for medium and thick steel: a 4 to 20 HP motor spins a flywheel and the clutch makes one stroke per "
                 "pedal press, 45 to 55 strokes a minute — the fastest shears in the range. Ten models from 1/8″ (3 mm) over 51″ to 1/4″ over "
                 "98″ and 3/8″ (10 mm) over 39″ and 59″, with a back gauge with fine adjustment, mechanical hold-downs and long-life blades, on a "
                 "simple welded construction with low energy consumption. 2,976 to 14,991 lb.",
         features=["1/8″ to 3/8″ (3 – 10 mm) mild steel × 39 – 98″ (1,000 – 2,500 mm); 45 – 55 strokes per minute"] + STD_MECH,
         optional=OPT_MECH,
         images=["tt-q11-6x2000", "tt-q11-4x2000", "tt-q11-3x1300"],
         videos=[],
         specs=spec([t_q11("Q11 mechanical", "Flywheel shears for medium and thick steel", Q11M)], G5)),
]
