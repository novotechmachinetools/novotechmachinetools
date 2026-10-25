"""Hidroliksan production presses — sold as NovoTech's premium line of production hydraulic presses (made in Turkey).
The supplier's name is not used on the site; the data comes from the imperial NovoTech brochure text
(/home/claude/hidroliksan/novotech-2026.txt, extracted from NovoTech_Hidroliksan_Hydraulic_Presses_2026.pdf).
Families are appended below the premium-line group on hydraulic-press.html (tools/sahinler_pages.py)."""
import re

from sahinler_lib import dims, inch, ins, motor, tons, weight  # noqa: F401

TXT = open("/home/claude/hidroliksan/novotech-2026.txt", encoding="utf-8").read()
P_PRESS = "hydraulic-press"
NUM = re.compile(r"^[\d.,+]+$")
UNITS = ("in", "cc", "HP", "in/s", "lb", "US", "tons", "metric")


def page(n):
    m = re.search(rf"=== page {n} ===\n(.*?)(?==== page|\Z)", TXT, re.S)
    return m.group(1)


def parse_table(n):
    """The TECHNICAL SPECIFICATIONS block of brochure page n → (models, {label: [cells]})."""
    t = page(n)
    t = t[t.index("TECHNICAL SPECIFICATIONS"):]
    rows, models = {}, []
    pending_us = False
    for line in t.split("\n")[1:]:
        if line.startswith(("Larger model", "Custom voltage", "Made in", "INCLUDED", "NOVOTECH", "1-year", "NovoTech", "1365", "Die cushion")) or not line.strip():
            if line.startswith(("Larger", "Custom", "Made in", "INCLUDED")):
                break
            continue
        if line.strip() in ("metric", "tons", "US"):
            pending_us = line.strip() == "US"
            continue
        tk = line.split()
        if tk[0] == "Model":
            # "Model HDD 100 HDD 200 …" → pairs
            rest = tk[1:]
            models = [" ".join(rest[i:i + 2]) for i in range(0, len(rest), 2)]
            continue
        # find where the numbers start
        i = 0
        while i < len(tk) and not NUM.match(tk[i]):
            i += 1
        label = " ".join(w for w in tk[:i] if w not in UNITS).strip()
        unit = " ".join(w for w in tk[:i] if w in UNITS)
        vals = tk[i:]
        cells, cur = [], []
        for v in vals:
            if v in ("×", "–"):
                cur.append(v)
            elif cur and cur[-1] in ("×", "–"):
                cur.append(v)
            else:
                if cur:
                    cells.append(" ".join(cur))
                cur = [v]
        if cur:
            cells.append(" ".join(cur))
        key = label + (" (US)" if ("US" in unit or pending_us) else "")
        pending_us = False
        rows[key] = cells
    return models, rows


KW = {"4": 3, "5.4": 4, "7.4": 5.5, "10": 7.5, "15": 11, "20": 15, "25": 18.5, "40": 30, "50": 37, "74": 55}


def hp(c):
    return f"{c} HP ({KW.get(c, round(float(c) / 1.341, 1)):g} kW)"


def spd(c):
    """in/s → mm/s: '4.33' → '4.33 in/s (110 mm/s)'; '0.12 – 0.63' → '0.12 – 0.63 in/s (3 – 16 mm/s)'."""
    parts = [p.strip() for p in c.split("–")]
    mm = [f"{round(float(p) * 25.4):g}" for p in parts]
    return f"{c} in/s ({' – '.join(mm)} mm/s)"


def table_size(c):
    a, b = [float(x) for x in c.split("×")]
    return f"{a:g} × {b:g}″ ({round(a * 25.4 / 10) * 10:,} × {round(b * 25.4 / 10) * 10:,} mm)"


def in10(c):
    v = float(c)
    return f"{v:g}″ ({round(v * 25.4 / 10) * 10:,} mm)"


def cc(c):
    return f"{c} cc/rev"


ROW_MAP = [("Capacity", "Press force", "", None, True), ("Table size", "Table size", "", table_size, True), ("Stroke", "Stroke", "", in10, True),
           ("Daylight", "Daylight", "", in10, False), ("Throat depth", "Throat depth", "", lambda c: inch(c), False), ("Cylinder diameter", "Cylinder Ø", "", lambda c: inch(c), False),
           ("Cushion capacity", "Die cushion force", "", None, False), ("Cushion stroke", "Die cushion stroke", "", in10, False),
           ("Pump displacement", "Pump displacement", "", cc, False), ("Motor power", "Motor power", "", hp, False),
           ("Advance speed", "Advance speed", "", spd, False), ("Working speed", "Pressing speed", "", spd, False), ("Return speed", "Return speed", "", spd, False),
           ("Dimensions", "Dimensions L × W × H", "", dims, False), ("Weight", "Weight", "", weight, False)]


def press_table(n, title, sub):
    models, R = parse_table(n)
    rows = []
    for pref, new, s, conv, key in ROW_MAP:
        src = next((k for k in R if k.startswith(pref) and "(US)" not in k), None)
        if src is None:
            continue
        if pref in ("Capacity", "Cushion capacity"):
            us = R.get(src + " (US)")
            cells = [tons(m, u) for m, u in zip(R[src], us)] if us else R[src]
        else:
            cells = [conv(c) if conv else c for c in R[src]]
        rows.append({"label": new, "sub": s, "cells": cells, "key": key})
    for (lab, model), val in FIX.items():
        for r in rows:
            if r["label"] == lab and model in models:
                r["cells"][models.index(model)] = val
    return {"title": title, "sub": sub, "models": models, "rows": rows}


# Source figures that cannot be right, shown as "on request" until the maker confirms them:
# the brochure (and the maker's own catalogue) give the HDD 200 a 300 t die cushion on a 200 t press.
FIX = {("Die cushion force", "HDD 200"): "on request"}


GK = ["force", "table", "stroke", "motor", "weight"]
G_FROM = ["Press force", "Table size", "Stroke", "Motor power", "Weight"]
NOTE = ("Standard sizes shown; every series is also built to the customer's table size, stroke, daylight and tonnage. Larger models to 3,000 metric tons "
        "(3,307 US tons) are built to order. Metric values in brackets are the manufacturer's nominal figures; dimensions are overall L × W × H.")


def spec(tables, note=NOTE):
    models = []
    for t in tables:
        rr = {r["label"]: r["cells"] for r in t["rows"]}
        for i, m in enumerate(t["models"]):
            models.append({"name": m, "glance": [rr[l][i] if l in rr and i < len(rr[l]) else "—" for l in G_FROM]})
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": GK, "caps": {}, "note": note}


STD_H = ["Welded and machined monoblock steel frame; precision-machined frame and T-slotted working table", "Chrome-plated and hardened cylinder; automatic lubrication for the guides",
         "Hydraulic block to EN standards; adjustable speed and pressure; load check valve", "Siemens S7 PLC with HMI touchscreen and remote access via internet",
         "Front and rear light barriers, two-hand control, reset and emergency-stop buttons; CE certificate", "Air cooling or heat exchanger for the hydraulic oil"]
OPT_H = ["Quick die change system", "Die, built and supplied with the press", "Ejector cylinder in the lower table"]
VOLT3 = "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"
PREMIUM = "NovoTech premium line"

FAMILIES = [
    dict(id="nt-press-hdd", group="novotech-production", page=P_PRESS, brand="novotech-premium",
         name="HDD H-frame double action deep drawing presses, 110 – 661 US tons",
         short="HDD deep drawing",
         models_label="HDD 100 – HDD 600 · to HDD 3000 built to order",
         summary="Double action deep drawing presses on a welded, machined monoblock H-frame: a main cylinder and a die cushion in the "
                 "lower table draw cups, pans, housings and tank ends in one stroke, and the ejector in the table lifts the finished "
                 "part out. Standard sizes from 110 to 661 US tons with 39.4″ stroke and daylight; larger presses to 3,307 US tons and "
                 "custom table sizes are built to order, with the die supplied by the press maker if required. Siemens S7 PLC with "
                 "HMI touchscreen, remote access, light barriers and two-hand control are standard.",
         features=["Double action: main cylinder plus die cushion (44 – 276 US tons) with 11.8″ cushion stroke"] + STD_H,
         optional=OPT_H + ["Die loading system or other die installation solutions", VOLT3],
         images=["hk-hdd", "hk-hdd-2", "hk-hdd-3"], videos=[],
         specs=spec([press_table(5, "HDD", "H-frame double action deep drawing presses")]),
         headline="110 – 661 US tons standard (to 3,307 to order) · 39.4″ stroke · die cushion to 331 US tons"),
    dict(id="nt-press-hsa", group="novotech-production", page=P_PRESS, brand="novotech-premium",
         name="HSA H-frame single action presses, 110 – 661 US tons",
         short="HSA single action",
         models_label="HSA 100 – HSA 600 · to HSA 3000 built to order",
         summary="The general-purpose production press: a single-action H-frame for bending, forming, hole punching, cutting and "
                 "straightening with whatever die is bolted to its T-slotted tables. Standard sizes from 110 to 661 US tons with "
                 "39.4″ stroke and daylight, built to 3,307 US tons and to the customer's table size on request. Chrome-plated "
                 "hardened cylinder, automatic guide lubrication, adjustable speed and pressure, safety PLC with light barriers and "
                 "a Siemens HMI with remote access.",
         features=["Single action press for bending, forming, punching, cutting and straightening dies", "Safety PLC"] + STD_H,
         optional=OPT_H + ["Die loading devices or other die installation solutions", VOLT3],
         images=["hk-hsa", "hk-hsa-3", "hk-hsa-2"], videos=[],
         specs=spec([press_table(7, "HSA", "H-frame single action presses")]),
         headline="110 – 661 US tons standard (to 3,307 to order) · 39.4″ stroke and daylight · T-slotted tables"),
    dict(id="nt-press-hcfp", group="novotech-production", page=P_PRESS, brand="novotech-premium",
         name="HCFP column frame single / double action presses, 110 – 1,102 US tons",
         short="HCFP column frame",
         models_label="HCFP 100 – HCFP 600 · HCFP 1000 built to order",
         summary="Four-column presses with the same hydraulics, Siemens control and safety equipment as the H-frame range, for shops "
                 "that need access to the die from all four sides or a die-cushion option on a column frame. Standard sizes from "
                 "110 to 661 US tons with 39.4″ stroke; the 1,102 US ton HCFP 1000 and custom table sizes are built to order, and "
                 "die support arms or a die loading system are available for heavy tooling.",
         features=["Column (four-post) frame, open on all sides; single or double action", "Central lubrication for the guides; safety PLC"] + STD_H[:1] + STD_H[2:],
         optional=OPT_H + ["Die cushion on all models", "Die support arms; die loading system", VOLT3],
         images=["hk-hcfp", "hk-hcfp-2"], videos=[],
         specs=spec([press_table(9, "HCFP", "column frame single / double action presses")]),
         headline="110 – 661 US tons standard (1,102 to order) · four-column frame · die cushion optional"),
    dict(id="nt-press-cfss", group="novotech-production", page=P_PRESS, brand="novotech-premium",
         name="CFSS enclosed C-frame single action presses, 33 – 276 US tons",
         short="CFSS enclosed C-frame",
         models_label="CFSS 30 · 60 · 100 · 150 · 200 · 250",
         summary="C-frame presses with the work area enclosed by guards and a light barrier, for bending, punching, cutting and "
                 "straightening with smaller dies: the frame is open on three sides so dies are mounted and removed easily, and "
                 "the press takes up less floor space than an H-frame. From 33 to 276 US tons with 15.7″ stroke, 11″ – 14.6″ "
                 "throat, Siemens S7 PLC with HMI touchscreen and remote access; an ejector cylinder and speed adjustment are optional.",
         features=["Enclosed work area with light barrier and safety PLC; frame open on three sides for quick die changes", "Throat depth 11″ to 14.6″; 15.7″ stroke"] + STD_H[:1] + STD_H[2:4] + STD_H[5:],
         optional=["Ejector cylinder", "Speed adjustment", VOLT3],
         images=["hk-cfss", "hk-cfss-2", "hk-cfss-3", "hk-cfss-4"], videos=[],
         specs=spec([press_table(10, "CFSS", "enclosed C-frame single action presses")]),
         headline="33 – 276 US tons · 15.7″ stroke · throat 11″ – 14.6″ · enclosed work area"),
    dict(id="nt-press-cfs", group="novotech-production", page=P_PRESS, brand="novotech-premium",
         name="CFS C-frame single action presses, 33 – 276 US tons",
         short="CFS C-frame",
         models_label="CFS 30 · 60 · 100 · 150 · 200 · 250",
         summary="The simpler C-frame press: the same welded monoblock frame, chrome-plated cylinder and T-slotted table as the CFSS "
                 "with a pressure transmitter, light barrier, two-hand control and emergency stop, and the HMI touchscreen as an "
                 "option. A manual production press for bending, punching and straightening with small dies, from 33 to 276 US tons.",
         features=["C-frame open on three sides; T-slotted working table", "Pressure transmitter; light barrier; two-hand button control; emergency stop; CE certificate",
                   "Welded and machined monoblock steel frame; chrome-plated and hardened cylinder; hydraulic block to EN standards"],
         optional=["HMI touchscreen control panel", "Air cooling for the hydraulic oil", "Quick die change system; die; ejector", VOLT3],
         images=["hk-cfs"], videos=[],
         specs=spec([press_table(12, "CFS", "C-frame single action presses")]),
         headline="33 – 276 US tons · 15.7″ stroke · 19.7″ daylight · two-hand control"),
    dict(id="nt-press-cfdd", group="novotech-production", page=P_PRESS, brand="novotech-premium",
         name="CFDD C-frame deep drawing presses, 33 – 276 US tons",
         short="CFDD deep drawing",
         models_label="CFDD 30 · 60 · 100 · 150 · 200 · 250",
         summary="Deep drawing on a C-frame: a die cushion of 11 to 110 US tons with 5.9″ stroke in the lower table and an ejector "
                 "that lifts the drawn part out, for small dies where a C-frame saves floor space. Table sizes are limited by the "
                 "C-shaped frame — beyond them the HDD H-frame press takes over. 33 to 276 US tons, 15.7″ stroke, 23.6″ daylight, "
                 "Siemens S7 PLC with HMI touchscreen and remote access.",
         features=["Die cushion 11 – 110 US tons with 5.9″ stroke; ejector in the lower table", "C-frame open on three sides; throat 11″ – 14.6″", "Pressure transmitter; light barrier; safety PLC"] + STD_H[:1] + STD_H[2:4] + STD_H[5:],
         optional=OPT_H + [VOLT3],
         images=["hk-cfdd", "hk-cfdd-100"], videos=[],
         specs=spec([press_table(14, "CFDD", "C-frame deep drawing presses")]),
         headline="33 – 276 US tons · die cushion 11 – 110 US tons · 15.7″ stroke · 23.6″ daylight"),
    dict(id="nt-press-hhrp", group="novotech-production", page=P_PRESS, brand="novotech-premium",
         name="SMC / HHRP composite moulding and hot plate presses, 110 – 661 US tons",
         short="SMC / HHRP hot plate",
         models_label="HHRP 100 – HHRP 600 · to HHRP 3000 built to order",
         summary="H-frame presses with heated (or cold) platens for SMC / BMC composite moulding, rubber, laminates and every part "
                 "that needs heat and pressure together. Insulation between the heated platens and the frame is standard, the "
                 "press software is written for the customer's moulding cycle and the press is built in the size and capacity "
                 "required — standard sizes from 110 to 661 US tons, to 3,307 US tons on request. Safety light curtains, "
                 "T-slotted platens, Siemens S7 PLC and HMI with remote access.",
         features=["Hot or cold T-slotted platens with insulation between plates and frame", "Press software written for the customer's moulding process", "Safety light curtains and safety PLC"] + STD_H,
         optional=OPT_H + [VOLT3],
         images=["hk-smc", "hk-smc-2", "hk-smc-2500", "hk-smc-detail", "hk-smc-detail-2"], videos=[],
         specs=spec([press_table(16, "HHRP", "SMC & hot plate hydraulic presses")]),
         headline="110 – 661 US tons standard (to 3,307 to order) · heated platens · composite, rubber and laminate moulding"),
    dict(id="nt-press-hsps", group="novotech-production", page=P_PRESS, brand="novotech-premium",
         name="HSPS hydraulic portal straightening presses, 110 – 441 US tons",
         short="HSPS portal straightening",
         models_label="HSPS 100 · 200 · 300 · 400",
         summary="Gantry (portal) presses for straightening long beams, plates, pipes and shafts: the cylinder travels along the "
                 "gantry on a rack drive and the gantry along the bed, so the press works in three axes from a pendant and the "
                 "workpiece stays on the threaded-hole table. Built in the size and tonnage requested — standard beds from 39.4 × "
                 "78.7″ to 59.1 × 137.8″ — with a safety rope, pressure transmitter and optional radio remote control.",
         features=["X, Y, Z axes by pendant control; rack drive for the gantry travel", "Working table with threaded holes; chrome-plated and hardened cylinder",
                   "Pressure transmitter; safety rope; reset and emergency-stop buttons; CE certificate", "Welded and machined monoblock steel frame; hydraulic block to EN standards"],
         optional=["Radio remote control", "Safety rails and fencing", VOLT3],
         images=["hk-hsps", "hk-hsps-300", "hk-hsps-100", "hk-hsps-detail"], videos=[],
         specs=spec([press_table(18, "HSPS", "hydraulic portal straightening presses")]),
         headline="110 – 441 US tons · beds to 59.1 × 137.8″ · cylinder moves on 3 axes"),
    dict(id="nt-press-hdt", group="novotech-production", page=P_PRESS, brand="novotech-premium",
         name="HDT H-frame hydraulic presses — Eco model, 110 – 276 US tons",
         short="HDT Eco H-frame",
         models_label="HDT 100 · 150 · 200 · 250",
         summary="A workshop-type H-frame press built to production standards: welded, machined monoblock frame, T-slotted table, "
                 "chrome-plated hardened cylinder, pressure transmitter and two-hand control, at a lower price than the HSA. "
                 "110 to 276 US tons with 15.7″ stroke and 23.6″ daylight, for the repair, maintenance and small fabrication "
                 "shop; quick die change, ejector, radio remote and oil cooling are optional.",
         features=["T-slotted working table; 15.7″ stroke, 23.6″ daylight", "Pressure transmitter; two-hand button control; emergency stop; CE certificate",
                   "Welded and machined monoblock steel frame; chrome-plated and hardened cylinder; hydraulic block to EN standards"],
         optional=["Quick die change system; die; ejector", "Radio remote control", "Air cooling or heat exchanger for the hydraulic oil", VOLT3],
         images=["hk-hdt"], videos=[],
         specs=spec([press_table(19, "HDT", "H-frame hydraulic presses — Eco model")]),
         headline="110 – 276 US tons · 15.7″ stroke · 23.6″ daylight · T-slotted table"),
]
