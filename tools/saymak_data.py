#!/usr/bin/env python3
"""Direct-gear motorised guillotine shears — NovoTech premium line, made in Turkey (novotech-mechanical-shears.html, under the shear-cutting hub).

Metric data from the maker's 2025 catalogue, pages 8 – 21 (SRGM, SRGM-H, SRGM-FR, SRGM-HFR, SRGM-CL, SRGM-HCL), shown as
imperial (metric) like the rest of the site.  Columns per model: capacity mm, max shearing length mm, strokes/min, kW,
table height mm, table width mm, overall width (depth) mm, length (along the blade) mm, height mm, kg.
"""
P_SHEAR = "novotech-mechanical-shears"
BRAND = "novotech-premium"
PREMIUM = "NovoTech premium line"

# mild-steel capacity label per mm — the fraction / gauge the trade quotes for that sheet
CAP = {6.0: "1/4″", 5.0: "3/16″", 4.0: "5/32″", 3.0: "1/8″", 2.5: "12 ga"}
HP = {3.0: "4", 4.0: "5.5", 7.5: "10", 11.0: "15"}


def fmt(v):
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.1f}"


def cap(mm):
    return f"{CAP[mm]} ({mm:g} mm)"


def inch(mm, nd=1):
    return f"{mm / 25.4:,.{nd}f}″ ({mm:,} mm)"


def feet(mm):
    f = mm / 304.8
    return f"{f:.0f} ft" if abs(f - round(f)) < 0.06 else f"{f:.1f} ft"


def motor(kw):
    return f"{HP[kw]} HP ({kw:g} kW)"


def dims(w, l, h):
    return f"{l / 25.4:.0f} × {w / 25.4:.0f} × {h / 25.4:.0f}″ ({l:,} × {w:,} × {h:,} mm)"


def weight(kg):
    return f"{round(kg * 2.20462):,} lb ({kg:,} kg)"


# (model, cap mm, length mm, strokes, kW, table h, table w, width, length, height, kg)
SRGM = [("SRGM 1100", 6.0, 1100, 31, 7.5, 800, 455, 2250, 1750, 1400, 2000), ("SRGM 1360", 6.0, 1360, 31, 7.5, 800, 455, 2250, 2050, 1400, 2300),
        ("SRGM 1560", 5.0, 1560, 31, 7.5, 800, 455, 2250, 2250, 1400, 2500), ("SRGM 2060", 4.0, 2060, 31, 7.5, 800, 455, 2250, 2700, 1400, 3000),
        ("SRGM 2560", 4.0, 2560, 31, 7.5, 800, 455, 2250, 3200, 1400, 3500), ("SRGM 3060", 4.0, 3060, 31, 11.0, 800, 455, 2250, 3700, 1400, 4000),
        ("SRGM 3200", 4.0, 3200, 31, 11.0, 800, 455, 2250, 4300, 1400, 4400), ("SRGM 4200", 3.0, 4200, 31, 11.0, 800, 455, 2250, 5300, 1400, 5300)]
SRGM_H = [("SRGM-H 1100", 3.0, 1100, 35, 3.0, 810, 390, 2100, 1720, 1260, 1100), ("SRGM-H 1360", 3.0, 1360, 35, 3.0, 810, 390, 2100, 1920, 1260, 1250),
          ("SRGM-H 1560", 3.0, 1560, 35, 3.0, 810, 390, 2100, 2100, 1260, 1500), ("SRGM-H 2060", 3.0, 2060, 35, 4.0, 810, 390, 2100, 2650, 1260, 1750),
          ("SRGM-H 2560", 2.5, 2560, 35, 4.0, 810, 390, 2100, 3150, 1260, 1950), ("SRGM-H 3060", 3.0, 3060, 35, 7.5, 810, 455, 2100, 3650, 1260, 3000)]
SRGM_FR = [("SRGM-FR 1100", 6.0, 1100, 31, 7.5, 880, 455, 2250, 1750, 1400, 2050), ("SRGM-FR 1360", 6.0, 1360, 31, 7.5, 880, 455, 2250, 2050, 1400, 2350),
           ("SRGM-FR 1560", 5.0, 1560, 31, 7.5, 880, 455, 2250, 2250, 1400, 2550), ("SRGM-FR 2060", 4.0, 2060, 31, 7.5, 880, 455, 2250, 2700, 1400, 3100),
           ("SRGM-FR 2560", 4.0, 2560, 31, 7.5, 880, 455, 2250, 3200, 1400, 3600), ("SRGM-FR 3060", 4.0, 3060, 31, 11.0, 880, 455, 2250, 3700, 1400, 4100),
           ("SRGM-FR 3200", 4.0, 3200, 31, 11.0, 880, 455, 2250, 4300, 1400, 4500), ("SRGM-FR 4200", 3.0, 4200, 31, 11.0, 880, 455, 2250, 5300, 1400, 5400)]
SRGM_HFR = [("SRGM-HFR 1320", 3.0, 1320, 35, 3.0, 880, 390, 2100, 1920, 1330, 1400), ("SRGM-HFR 1520", 3.0, 1520, 35, 3.0, 880, 390, 2100, 2100, 1330, 1700),
            ("SRGM-HFR 2020", 3.0, 2020, 35, 4.0, 880, 390, 2100, 2650, 1330, 2000), ("SRGM-HFR 2520", 2.5, 2520, 35, 4.0, 880, 390, 2100, 3150, 1330, 2200),
            ("SRGM-HFR 3020", 3.0, 3020, 35, 7.5, 880, 455, 2100, 3650, 1330, 3100)]
SRGM_CL = [("SRGM-CL 1100", 6.0, 1100, 31, 7.5, 800, 455, 1250, 1750, 1400, 1900), ("SRGM-CL 1360", 6.0, 1360, 31, 7.5, 800, 455, 1250, 2050, 1400, 2200),
           ("SRGM-CL 1560", 5.0, 1560, 31, 7.5, 800, 455, 1250, 2250, 1400, 2400), ("SRGM-CL 2060", 4.0, 2060, 31, 7.5, 800, 455, 1250, 2700, 1400, 2900)]
SRGM_HCL = [("SRGM-HCL 1100", 3.0, 1100, 35, 3.0, 810, 390, 1300, 1720, 1260, 1050), ("SRGM-HCL 1360", 3.0, 1360, 35, 3.0, 810, 390, 1300, 1920, 1260, 1200),
            ("SRGM-HCL 1560", 3.0, 1560, 35, 3.0, 810, 390, 1300, 2100, 1260, 1450), ("SRGM-HCL 2060", 3.0, 2060, 35, 4.0, 810, 390, 1300, 2650, 1260, 1700)]

ROWS = [("Shearing capacity, mild steel", lambda r: cap(r[1]), True), ("Max shearing length", lambda r: inch(r[2]), True),
        ("Strokes per minute", lambda r: f"{r[3]} strokes/min", True), ("Motor power", lambda r: motor(r[4]), False),
        ("Table height", lambda r: inch(r[5]), False), ("Table width", lambda r: inch(r[6]), False),
        ("Dimensions L × W × H", lambda r: dims(r[7], r[8], r[9]), False), ("Weight", lambda r: weight(r[10]), False)]
GK = ["capacity", "length", "strokes", "motor", "weight"]
G_FROM = ["Shearing capacity, mild steel", "Max shearing length", "Strokes per minute", "Motor power", "Weight"]
NOTE = ("Capacities are the manufacturer's ratings for mild steel over the full blade length; count on about 60 % of the thickness in "
        "stainless steel. Metric values in brackets are the manufacturer's nominal figures; dimensions are overall L (along the blade) × W × H.")


def table(data, title, sub):
    rows = [{"label": lab, "sub": "", "cells": [fn(r) for r in data], "key": key} for lab, fn, key in ROWS]
    return {"title": title, "sub": sub, "models": [r[0] for r in data], "rows": rows}


def spec(tables, note=NOTE):
    models = []
    for t in tables:
        rr = {r["label"]: r["cells"] for r in t["rows"]}
        for i, m in enumerate(t["models"]):
            models.append({"name": m, "glance": [rr[l][i] for l in G_FROM]})
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": GK, "caps": {}, "note": note}


def span(data):
    """'3.6 – 13.8 ft' from the shearing lengths of a series."""
    return f"{feet(data[0][2])} – {feet(data[-1][2])}"


def vids(*ids_titles):
    from sahinler_lib import vids as _vids      # NovoTech's own channel: id, title, duration → video dict with thumb
    return _vids(*ids_titles)


STD_SRGM = ["NC-controlled back gauge with 29.5″ (750 mm) stroke", "Squaring arm with T-slot, stopper and ruler", "Front sheet holding arms; finger protection guard",
            "Rear protection cages with photocell", "Table with ball transfers; cutting line illumination with shadow wire", "Foot pedal and cutting counter",
            "Easy blade-gap adjustment from the front; mechanical sheet clamping", "High-carbon, high-chrome blades: two-edged top blade, four-edged bottom blade"]
OPT_SRGM = ["NC back gauge with 39.4″ (1,000 mm) stroke", "Pneumatic sheet support with return-to-rear", "Rear protection cages with light barrier",
            "0 – 180° angular cutting device", "ELGO P40T or FUJI Monitouch touch-screen NC control", "Longer squaring arm and front holding arms to 118″ (3,000 mm)",
            "Front-operated manual back gauge with ball screw", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]
STD_H = ["Manual back gauge with 29.5″ (750 mm) stroke", "Squaring arm with ruler; front sheet holding arms; finger protection guard",
         "Rear protection cages with photocell", "Cutting line illumination with shadow wire", "Foot pedal and cutting counter",
         "Mechanical sheet clamping; high-carbon, high-chrome two-edged top and four-edged bottom blades"]
OPT_H = ["NC-controlled back gauge with 29.5″ or 39.4″ (750 / 1,000 mm) stroke", "Pneumatic sheet support with return-to-rear", "Rear protection cages with light barrier",
         "0 – 180° angular cutting device", "ELGO P40T or FUJI Monitouch touch-screen NC control", "Longer squaring arm and front holding arms to 118″ (3,000 mm)",
         "Front-operated manual back gauge with ball screw", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]
STD_FR = ["NC-controlled back gauge with 29.5″ (750 mm) stroke", "Manual return-to-sender: the cut piece comes back to the operator",
          "Squaring arm with T-slot, stopper and ruler", "Front sheet holding arms; finger protection guard", "Rear protection cages with photocell",
          "Table with ball transfers; cutting line illumination with shadow wire", "Foot pedal and cutting counter", "Easy blade-gap adjustment from the front; mechanical sheet clamping"]
OPT_FR = ["NC back gauge with 39.4″ (1,000 mm) stroke", "Pneumatic sheet support with return-to-sender and return-to-rear", "Rear protection cages with light barrier",
          "0 – 180° angular cutting device", "ELGO P40T or FUJI Monitouch touch-screen NC control", "Longer squaring arm and front holding arms to 118″ (3,000 mm)",
          "Front-operated manual back gauge with ball screw", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]
STD_CL = ["Built to be integrated into a cut-to-length line: the sheet feeds straight through from the rear", "Squaring arm with T-slot, stopper and ruler",
          "Front sheet holding arms; finger protection guard", "Table with ball transfers; cutting line illumination with shadow wire",
          "Mechanical sheet clamping; high-carbon, high-chrome two-edged top and four-edged bottom blades"]
OPT_CL = ["Electrical cabinet (when the shear is not run from the line control)", "Rear protection cages with photocell or light barrier", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]

FAMILIES = [
    dict(id="nt-shear-srgm-h", group="shear-standard", page=P_SHEAR, brand=BRAND,
         name=f"SRGM-H light type mechanical guillotine shears, 1/8″ × {span(SRGM_H)}",
         short="SRGM-H light shears",
         models_label="SRGM-H 1100 – SRGM-H 3060 · 6 models",
         summary="The light-type direct-gear guillotine for sheet-metal shops, HVAC and signage: 1/8″ (3 mm) mild steel over 43″ to 10 ft in "
                 "35 strokes a minute from a 4 to 10 HP motor, with a manual back gauge, squaring arm, front holding arms and photocell rear "
                 "guard as standard. The same welded frame, teflon slideways and four-edged blades as the SRGM, in a lighter machine from "
                 "2,425 lb. An NC back gauge, pneumatic sheet support and a touch-screen control are options.",
         features=["1/8″ (3 mm) mild steel; 12 ga on the 2560; 35 strokes per minute"] + STD_H,
         optional=OPT_H,
         images=["sm-srgm-h", "sm-srgm-h-panel", "sm-srgm-h-rear", "sm-srgm-h-gauge"],
         videos=[],
         specs=spec([table(SRGM_H, "SRGM-H", "Light type direct-gear motorised guillotines")])),
    dict(id="nt-shear-srgm", group="shear-standard", page=P_SHEAR, brand=BRAND,
         name=f"SRGM mechanical guillotine shears, 1/4″ × {span(SRGM)}",
         short="SRGM shears",
         models_label="SRGM 1100 – SRGM 4200 · 8 models",
         summary="The standard direct-gear motorised guillotine: a 10 or 15 HP motor drives the cutting beam through a gearbox — no hydraulics, "
                 "no flywheel clutch — for 31 clean strokes a minute in 1/4″ (6 mm) mild steel over 43″ to 1/8″ over 13.8 ft. Welded steel "
                 "frame, cutting beam in teflon slideways, blade gap set from the front, mechanical hold-downs and an NC back gauge with 29.5″ "
                 "stroke, squaring arm, ball-transfer table, shadow-line light and photocell rear guard as standard.",
         features=["1/4″ (6 mm) mild steel on the 1100 and 1360, 3/16″ to 5/32″ on the 1560 – 3200, 1/8″ on the 4200; 31 strokes per minute"] + STD_SRGM,
         optional=OPT_SRGM,
         images=["sm-srgm", "sm-srgm-table", "sm-srgm-rear", "sm-elgo-p40t"],
         videos=vids(("MQNV9oMWMNQ", "SRGM mechanical shear"), ("6gRA2_DOkFs", "SRGM 1360 mechanical shear")),
         specs=spec([table(SRGM, "SRGM", "Direct-gear motorised guillotines")])),
    dict(id="nt-shear-srgm-hfr", group="shear-return", page=P_SHEAR, brand=BRAND,
         name=f"SRGM-HFR light type guillotine shears with return-to-sender, 1/8″ × {span(SRGM_HFR)}",
         short="SRGM-HFR shears",
         models_label="SRGM-HFR 1320 – SRGM-HFR 3020 · 5 models",
         summary="The light-type shear with the return-to-sender sheet support: after the cut the strip is carried back to the front of the "
                 "machine, so one operator cuts blanks and strips without walking round to the rear. 1/8″ (3 mm) mild steel over 4.3 to 9.9 ft, "
                 "35 strokes a minute, NC back gauge with 29.5″ stroke as standard; pneumatic return-to-sender and return-to-rear optional.",
         features=["1/8″ (3 mm) mild steel; 12 ga on the 2520; 35 strokes per minute"] + STD_FR,
         optional=OPT_FR,
         images=["sm-srgm-hfr", "sm-srgm-hfr-blade", "sm-srgm-fr-rear"],
         videos=vids(("hF92ADE0DMA", "SRGM HFR guillotine shear with return-to-front and return-to-rear")),
         specs=spec([table(SRGM_HFR, "SRGM-HFR", "Light type direct-gear motorised guillotines with return-to-sender")])),
    dict(id="nt-shear-srgm-fr", group="shear-return", page=P_SHEAR, brand=BRAND,
         name=f"SRGM-FR mechanical guillotine shears with return-to-sender, 1/4″ × {span(SRGM_FR)}",
         short="SRGM-FR shears",
         models_label="SRGM-FR 1100 – SRGM-FR 4200 · 8 models",
         summary="The SRGM with the return-to-sender sheet support behind the blade: the cut piece is returned to the operator at the front, "
                 "the off-cut drops to the rear — blanking and strip cutting by one person. Same 1/4″ (6 mm) capacity, 31 strokes a minute, "
                 "NC back gauge, squaring arm and ball-transfer table as the SRGM, with the table 3″ higher for the return conveyor.",
         features=["1/4″ (6 mm) mild steel on the 1100 and 1360, 3/16″ to 5/32″ on the 1560 – 3200, 1/8″ on the 4200; 31 strokes per minute"] + STD_FR,
         optional=OPT_FR,
         images=["sm-srgm-fr", "sm-srgm-fr-panel", "sm-srgm-fr-rear", "sm-srgm-fr-open"],
         videos=vids(("Cc6JwtRAidg", "SRGM FR guillotine shear with return-to-front and return-to-rear"), ("5Kv4G4OqOy4", "SRGM FR NC mechanical shear")),
         specs=spec([table(SRGM_FR, "SRGM-FR", "Direct-gear motorised guillotines with return-to-sender")])),
    dict(id="nt-shear-srgm-hcl", group="shear-line", page=P_SHEAR, brand=BRAND,
         name=f"SRGM-HCL light type shears for cut-to-length lines, 1/8″ × {span(SRGM_HCL)}",
         short="SRGM-HCL line shears",
         models_label="SRGM-HCL 1100 – SRGM-HCL 2060 · 4 models",
         summary="The light-type guillotine built into a decoiler, straightener and feeder line: open at the rear so the coil strip runs straight "
                 "through, 1/8″ (3 mm) mild steel over 43″ to 6.8 ft at 35 strokes a minute, with the line's control or an optional electrical "
                 "cabinet of its own. From 2,315 lb.",
         features=["1/8″ (3 mm) mild steel; 35 strokes per minute; 51″ (1,300 mm) deep"] + STD_CL,
         optional=OPT_CL,
         images=["sm-srgm-hcl", "sm-srgm-hcl-rear"],
         videos=[],
         specs=spec([table(SRGM_HCL, "SRGM-HCL", "Light type direct-gear motorised guillotines for cut-to-length lines")])),
    dict(id="nt-shear-srgm-cl", group="shear-line", page=P_SHEAR, brand=BRAND,
         name=f"SRGM-CL mechanical shears for cut-to-length lines, 1/4″ × {span(SRGM_CL)}",
         short="SRGM-CL line shears",
         models_label="SRGM-CL 1100 – SRGM-CL 2060 · 4 models",
         summary="The SRGM for coil lines: the same 10 HP direct-gear drive, 1/4″ (6 mm) capacity and 31 strokes a minute in a frame only 49″ "
                 "deep that the straightened strip feeds through from the rear, cut to length by the line control. Squaring arm, front holding "
                 "arms, ball-transfer table and shadow-line light as standard; electrical cabinet and rear guards optional.",
         features=["1/4″ (6 mm) mild steel on the 1100 and 1360, 3/16″ on the 1560, 5/32″ on the 2060; 31 strokes per minute; 49″ (1,250 mm) deep"] + STD_CL,
         optional=OPT_CL,
         images=["sm-srgm-cl"],
         videos=[],
         specs=spec([table(SRGM_CL, "SRGM-CL", "Direct-gear motorised guillotines for cut-to-length lines")])),
]
