#!/usr/bin/env python3
"""Cevisa (CEVISA S.A., Vitoria, Spain — plate bevelling machines since 1969, ISO 9001 / AENOR) — sold under its own brand on
plate-beveler.html (the old site's URL), small → large: standard shearing (CHP 7, CHP 12, CHP 12 INV), adjustable shearing
(CHP 12G, CHP 21G, CHP 21G INV), reversible shearing (CHP 12G REV, CHP 21G REV) and milling bevellers (CHP 30G, CHP 60G,
CHP 60G INV, CHP 100G).

Technical data from the Cevisa catalogue (CATALOGO_CEVISA_EN-ES.pdf, the user's source for technical data) and, for the CHP
100G, which the catalogue predates, the Cevisa CHP-100G data sheet; minimum plate width and disc Ø (not in the catalogue)
from cevisa.net.  Where cevisa.net differs from the catalogue (CHP 12 bevel in several runs 17 mm, CHP 12G 135 kg, CHP 21G INV
450 kg, CHP 21G REV 635 kg, CHP 60G 800 kg and 500 mm/min, CHP 21G tube Ø 100 mm) the catalogue figure is used.
Shown as imperial (metric); bevel lengths and thicknesses to the nearest 1/16″ (1/32″ below 1/4″).
"""
from fractions import Fraction

BRAND = "cevisa"
P_BEVEL = "plate-beveler"


def vids(*ids_titles):
    from sahinler_lib import vids as _vids      # NovoTech's own channel only
    return _vids(*ids_titles)


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


def mm(v):
    return f"{v:,g}"


def pair(a, b):
    """one run / several runs: 1/2″ / 11/16″ (12 / 18 mm)"""
    return f"{inch(a)} / {inch(b)} ({mm(a)} / {mm(b)} mm)"


def rng(a, b):
    return f"{inch(a)} – {inch(b)} ({mm(a)} – {mm(b)} mm)"


def one(a):
    return f"{inch(a)} ({mm(a)} mm)"


def dia(a):
    return f"Ø{inch(a)} ({mm(a)} mm)"


def hp(h, kw):
    return f"{h:g} HP ({kw:g} kW)"


def lb(kg):
    return f"{round(kg * 2.20462):,} lb ({kg:,} kg)"


def m_min(v):
    return f"{v * 3.28084:.1f} ft/min ({v:g} m/min)"


def mm_min(v):
    return f"{v / 25.4:.1f} in/min ({v:,} mm/min)"


def row(label, cells, key=False, sub=""):
    return {"label": label, "sub": sub, "cells": cells, "key": key}


VOLT = "CSA-approved electrical panel; 600 V 3-phase with transformer (208 / 240 / 480 V on request)"
VOLT_OPT = "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"
ANGLES_STD = "22.5° – 45° with angle devices"
ANGLES_ADJ = "20° – 45°, adjustable"
ANGLES_MILL = "15° – 70°, adjustable"
GK = ["bevel", "thickness", "angle", "motor", "weight"]
NOTE_SHEAR = ("Bevel length is the width of the bevel face; its depth is the length × cos (bevel angle) — an 11/16″ bevel at 30° is "
              "about 5/8″ deep. Capacities for mild steel of 58 ksi (400 MPa) tensile strength; stainless steel as given. Metric values in "
              "brackets are the manufacturer's figures.")
NOTE_MILL = ("Bevel length is the width of the bevel face; the milling bevellers have the same capacity in every material, from mild "
             "steel to Hardox. Metric values in brackets are the manufacturer's figures.")

# (model, one run, several runs, stainless one / several, rec. max, t min, t max, speed m/min, angle, HP, kW, tube Ø in, kg)
SHEAR = {
    "CHP 7": (6, 10, 4, 8, 8, 3, 16, 1.6, ANGLES_STD, 0.75, 0.55, 100, 45),
    "CHP 12": (12, 18, 8, 16, 20, 6, 40, 2.6, ANGLES_STD, 3, 2.2, 100, 65),
    "CHP 12 INV": (12, 18, 8, 16, 20, 6, 40, 2.6, ANGLES_STD, 3, 2.2, 100, 65),
    "CHP 12G": (12, 18, 8, 16, 20, 6, 30, 2.6, ANGLES_ADJ, 3, 2.2, 100, 110),
    "CHP 21G": (20, 28, 13, 23, 40, 9, 50, 1.7, ANGLES_ADJ, 4, 3, 150, 450),
    "CHP 21G INV": (20, 28, 13, 23, 40, 9, 50, 1.7, ANGLES_ADJ, 4, 3, 150, 485),
    "CHP 12G REV": (12, 18, 8, 16, 20, 6, 30, 2.6, ANGLES_ADJ, 3, 2.2, 100, 235),
    "CHP 21G REV": (20, 28, 13, 23, 40, 9, 50, 1.7, ANGLES_ADJ, 4, 3, 150, 628),
}
# (model, one run, several runs, rec. max, t min, t max, speed mm/min, HP, kW, kg)
MILL = {
    "CHP 30G": (25, 35, 50, 3, 50, 800, 3, 2.2, 620),
    "CHP 60G": (40, 60, 70, 10, 70, 670, 5, 3.8, 810),
    "CHP 60G INV": (40, 60, 70, 10, 70, 670, 5, 3.8, 810),
    "CHP 100G": (88, 100, 120, 10, 120, 550, 15, 11, 3650),
}


def shear_table(title, sub, models):
    d = [SHEAR[m] for m in models]
    return {"title": title, "sub": sub, "models": models, "rows": [
        row("Max. bevel length, mild steel", [pair(r[0], r[1]) for r in d], True, "one run / several runs"),
        row("Max. bevel length, stainless", [pair(r[2], r[3]) for r in d], False, "one run / several runs"),
        row("Plate & tube thickness", [rng(r[5], r[6]) for r in d], True, "nominal range"),
        row("Max. recommended thickness", [one(r[4]) for r in d]),
        row("Bevel angle", [r[8] for r in d], True),
        row("Bevel speed", [m_min(r[7]) for r in d]),
        row("Min. tube Ø", [dia(r[11]) for r in d], False, "inside"),
        row("Motor power", [hp(r[9], r[10]) for r in d], True),
        row("Weight", [lb(r[12]) for r in d], True)]}


def mill_table(title, sub, models):
    d = [MILL[m] for m in models]
    thick = [rng(r[3], r[4]) + (" · to 3-15/16″ (100 mm) in special configuration" if m.startswith("CHP 60G") else "") for m, r in zip(models, d)]
    return {"title": title, "sub": sub, "models": models, "rows": [
        row("Max. bevel length, any material", [pair(r[0], r[1]) for r in d], True, "one run / several runs"),
        row("Plate thickness", thick, True, "nominal range"),
        row("Max. recommended thickness", [one(r[2]) for r in d]),
        row("Bevel angle", [ANGLES_MILL] * len(d), True),
        row("Bevel speed", [mm_min(r[5]) for r in d]),
        row("Motor power", [hp(r[6], r[7]) for r in d], True),
        row("Weight", [lb(r[8]) for r in d], True)]}


def spec(table, note):
    """glance: bevel (several runs) · thickness range · angle · motor · weight"""
    rr = {r["label"]: r["cells"] for r in table["rows"]}
    bevel = rr.get("Max. bevel length, mild steel") or rr["Max. bevel length, any material"]
    thick = rr.get("Plate & tube thickness") or rr["Plate thickness"]
    models = [{"name": m, "glance": [bevel[i].split(" / ")[1].split(" (")[0] + " bevel", thick[i].split(" (")[0], rr["Bevel angle"][i],
                                     rr["Motor power"][i], rr["Weight"][i]]} for i, m in enumerate(table["models"])]
    return {"kind": "table", "tables": [table], "models": models, "glance_keys": GK, "caps": {}, "note": note}


STD = ["CHP 7", "CHP 12", "CHP 12 INV"]
ADJ = ["CHP 12G", "CHP 21G", "CHP 21G INV"]
REV = ["CHP 12G REV", "CHP 21G REV"]
MIL = ["CHP 30G", "CHP 60G", "CHP 60G INV", "CHP 100G"]
SHEAR_OPT = ["Cutters for mild steel, stainless steel and aluminum", "Plastic rollers that do not mark the material", VOLT_OPT]

FAMILIES = [
    dict(id="cevisa-std", group="cevisa-shear", page=P_BEVEL, brand=BRAND,
         name="CHP 7 · CHP 12 · CHP 12 INV standard shearing bevellers, bevel to 11/16″",
         short="CHP 7 · CHP 12 · CHP 12 INV",
         models_label="CHP 7 · CHP 12 · CHP 12 INV · 3 models",
         summary="The portable bevellers that do most of a fabrication shop's weld preparation: the machine sits on the plate edge, a "
                 "shear cutter takes the bevel off cold in one or several runs, and the machine feeds itself along the edge — on the "
                 "CHP 12 a 20 ft plate is bevelled in under three minutes. The 99 lb CHP 7 bevels plate, tube and aluminum from 1/8″ to "
                 "5/8″ thick to a 3/8″ bevel; the CHP 12, Cevisa's best-known machine since 1972, takes 1/4″ to 1-9/16″ plate to an "
                 "11/16″ bevel at 8.5 ft/min; the CHP 12 INV is the same machine working upside down on the lower edge, so an X bevel "
                 "needs no plate turning. V, X, K and Y bevels at 22.5° to 45°; tube from Ø3-15/16″ inside, bevelled inside or out.",
         headline="Plate & tube 1/8″ – 1-9/16″ · bevel to 11/16″ · 22.5° – 45° · self-feeding",
         features=["Self-feeding along the plate edge — no pushing and no supervision while it bevels",
                   "Cold shear cutting: no heat-affected zone, no slag, no grinding; cutters last about 3,300 ft (1,000 m) and are resharpened",
                   "V, X, K and Y bevels on plate, on tube from Ø3-15/16″ (100 mm) inside — inside or outside — and on discs from Ø13-3/4″ (350 mm)",
                   "Angle devices 22.5° – 45°; supplied with 3 cutters (1 on the machine), a 30° device, a tube device and spanners",
                   "On the bench, on casters or on a crane hook; reversing switch, thermal-magnetic trip and emergency stop",
                   "CHP 12 INV works upside down for lower bevels — under a CHP 12 it cuts the other half of an X bevel in the same pass",
                   VOLT],
         optional=["Angle devices 22.5° – 45°; other angles on request", "Parts for narrow plates, down to 13/16″ (20 mm) wide", "Trolley"] + SHEAR_OPT,
         images=["cv-chp12", "cv-chp7", "cv-chp12-inv", "cv-bevel-samples", "cv-chp12-plate", "cv-chp7-shell", "cv-chp12-bench", "cv-chp12-crane", "cv-cutters"],
         videos=vids(("LB_jeV9aHm4", "CHP 12 plate beveller"), ("3mBwPe_QHyQ", "CHP 7 plate beveller"), ("wX0wgBJT-QU", "CHP 12 INV — lower bevels"),
                     ("ZPAYNjHysmk", "CHP 12 bevelling tube"), ("jWqVIYxWY2k", "CHP 12 — internal bevel"), ("DdeSJH7Fj6I", "CHP 12 bevelling a disc"),
                     ("pViAntAKHzI", "CHP 12 bevelling checker plate"), ("yU2twl3M-FI", "CHP 12 on long plates")),
         specs=spec(shear_table("CHP 7 · CHP 12 · CHP 12 INV", "Standard shearing bevellers", STD), NOTE_SHEAR)),
    dict(id="cevisa-adj", group="cevisa-shear", page=P_BEVEL, brand=BRAND,
         name="CHP 12G · CHP 21G · CHP 21G INV adjustable-angle bevellers, bevel to 1-1/8″",
         short="CHP 12G · CHP 21G · CHP 21G INV",
         models_label="CHP 12G · CHP 21G · CHP 21G INV · 3 models",
         summary="Adjustable-angle bevellers for production weld preparation: the bevel angle is set anywhere from 20° to 45° on the "
                 "machine itself, and the trolley holds machine and plate in the best working position, which steadies the cut and "
                 "lengthens cutter life. The CHP 12G is the adjustable CHP 12 — 1/4″ to 1-3/16″ plate, an 11/16″ bevel at 8.5 ft/min. "
                 "The CHP 21G is built for round-the-clock work: 3/8″ to 1-15/16″ plate and a 1-1/8″ bevel in several runs (13/16″ in "
                 "one) on a built-in trolley. The CHP 21G INV bevels the lower edge of heavy plate without turning it over, and side by "
                 "side with a CHP 21G one operator bevels both edges.",
         headline="Plate 1/4″ – 1-15/16″ · bevel to 1-1/8″ · angle 20° – 45° on the machine",
         features=["Bevel angle adjustable from 20° to 45° on the machine — no angle devices to change",
                   "Self-feeding at 8.5 ft/min (CHP 12G) or 5.6 ft/min (CHP 21G); V, X, K and Y bevels on plate and tube",
                   "Trolley for a stable plate / machine position and longer cutter life — built in on the CHP 21G and 21G INV, working height 33-1/2″ – 34-5/8″ (850 – 880 mm)",
                   "CHP 21G: heavy-duty frame for 24-hour production; plates from 2-3/4″ (70 mm) wide",
                   "CHP 21G INV: lower bevels on heavy plate without turning it; works in pair with a CHP 21G",
                   "Electric box with reversing switch, thermal-magnetic trip and emergency stop; 3 cutters supplied (1 on the machine)",
                   VOLT],
         optional=["Universal cutter for every material (CHP 21G, 21G INV)"] + SHEAR_OPT,
         images=["cv-chp21g", "cv-chp12g", "cv-chp21g-inv", "cv-bevel-sample-v", "cv-bevel-cutting", "cv-chp21g-inv-yard"],
         videos=vids(("WbrDnYep26k", "CHP 21G heavy-duty beveller"), ("t263mnC4Fws", "CHP 12G adjustable-angle beveller"),
                     ("YHTVPUcQHGg", "CHP 12G on small plates"), ("NcKvH2zlEA8", "CHP 21G INV — lower bevels")),
         specs=spec(shear_table("CHP 12G · CHP 21G · CHP 21G INV", "Adjustable-angle shearing bevellers", ADJ), NOTE_SHEAR)),
    dict(id="cevisa-rev", group="cevisa-shear", page=P_BEVEL, brand=BRAND,
         name="CHP 12G REV · CHP 21G REV reversible bevellers, bevel to 1-1/8″",
         short="CHP 12G REV · CHP 21G REV",
         models_label="CHP 12G REV · CHP 21G REV · 2 models",
         summary="Two bevellers in one: the head turns over on its frame in under a minute, so the same machine cuts the upper bevel "
                 "and then the lower one without anyone turning the plate — X, K, V and Y bevels on large and heavy plate with one "
                 "machine and one operator, and no crane work to flip the plate. The CHP 12G REV bevels 1/4″ to 1-3/16″ plate to an "
                 "11/16″ bevel at 8.5 ft/min; the CHP 21G REV combines a CHP 21G and a CHP 21G INV for 3/8″ to 1-15/16″ plate and a "
                 "1-1/8″ bevel. Bevel angle adjustable from 20° to 45° on both.",
         headline="Upper and lower bevels with one machine · plate to 1-15/16″ · bevel to 1-1/8″",
         features=["Turns over on its frame in under a minute for upper and lower bevels — the plate stays where it is",
                   "Bevel angle adjustable 20° – 45°; self-feeding; no supervision needed while it bevels",
                   "CHP 12G REV: 8.5 ft/min, 518 lb · CHP 21G REV: 5.6 ft/min, 1,385 lb, built-in trolley, working height 33-1/2″ – 34-5/8″",
                   "Plate and tube bevelling; electric box with reversing switch, thermal-magnetic trip and emergency stop",
                   VOLT],
         optional=["Universal cutter for every material (CHP 21G REV)"] + SHEAR_OPT,
         images=["cv-chp21g-rev", "cv-chp12g-rev", "cv-chp21g-rev-turned", "cv-chp21g-rev-plate", "cv-chp12g-rev-detail"],
         videos=vids(("cTYLvwywiXg", "CHP 21G REV turning over"), ("-fUkdjHz-Tw", "CHP 21G REV on long plates"),
                     ("NevxcSie6nw", "CHP 12G REV reversible beveller"), ("v6nlThzN-GA", "CHP 12G REV on long plates")),
         specs=spec(shear_table("CHP 12G REV · CHP 21G REV", "Reversible shearing bevellers", REV), NOTE_SHEAR)),
    dict(id="cevisa-mill", group="cevisa-mill", page=P_BEVEL, brand=BRAND,
         name="CHP 30G · CHP 60G · CHP 60G INV · CHP 100G milling bevellers, bevel to 3-15/16″",
         short="CHP 30G · CHP 60G · CHP 100G",
         models_label="CHP 30G · CHP 60G · CHP 60G INV · CHP 100G · 4 models",
         summary="Portable milling machines that bevel: an insert milling head machines the bevel while feed rollers carry the machine "
                 "along the plate and pneumatic clamps hold it down — a machined face with no heat and no grinding, in any material "
                 "from mild steel to Hardox and duplex at the same capacity, at 15° to 70°, with transition and J bevels. CHP 30G: plate "
                 "1/8″ – 1-15/16″, bevel to 1-3/8″. CHP 60G: plate 3/8″ – 2-3/4″ (3-15/16″ in special configuration), bevel to 2-3/8″, "
                 "and the CHP 60G INV for lower bevels. CHP 100G: plate to 4-3/4″, bevel to 3-15/16″.",
         headline="Plate 1/8″ – 4-3/4″ · bevel to 3-15/16″ · 15° – 70° · any material, machined finish",
         features=["Machined bevel face from an insert milling head — no grinding before welding and no change to the steel",
                   "The same capacity in every material: mild and stainless steel, Hardox, Armox, duplex, super duplex, aluminum",
                   "Bevel angle 15° – 70°; electronic display of bevel width; adjustable feed and spindle speed",
                   "V, X, K, Y, transition (slope) and slope + bevel; J bevels with the J-bevel device (CHP 60G)",
                   "Pneumatic clamping and feed rollers for a vibration-free cut; shop air 7 CFM (200 l/min)",
                   "Built-in trolley; pneumatic working height 29-7/8″ – 37″ (CHP 60G); control pendant; chip drawer",
                   "CHP 60G INV bevels the lower edge and works in parallel with a CHP 60G",
                   VOLT],
         optional=["Indexable inserts", "J-bevel device, 15° – 30° (CHP 60G)", "Pneumatic working-height adjustment (CHP 30G)",
                   "Plate to 3-15/16″ (100 mm) in special configuration (CHP 60G)", "Plastic rollers that do not mark the material", VOLT_OPT],
         images=["cv-chp60g", "cv-chp30g", "cv-chp60g-inv", "cv-chp100g", "cv-milled-bevel", "cv-chp30g-plate", "cv-chp100g-chips",
                 "cv-chp60g-pendant", "cv-chp100g-panel", "cv-milling-head"],
         videos=vids(("Wp_bL9Zlzr0", "CHP 60G milling beveller"), ("8onvK9FJcXM", "CHP 30G milling beveller"),
                     ("IzTptXDUixA", "CHP 60G and CHP 60G INV working together"), ("paMtzykm12c", "CHP 60G bevelling Hardox plate"),
                     ("oCw91LfFeac", "CHP 60G — J bevel"), ("TEyll5YizoE", "CHP 60G at 70° on checker plate"),
                     ("XSt1uJQeK04", "CHP 60G on curved plate"), ("mbuJygnX5o4", "CHP 60G and CHP 21G compared"),
                     ("JlbdjfEDiGk", "CHP 60G tutorial")),
         specs=spec(mill_table("CHP 30G · CHP 60G · CHP 60G INV · CHP 100G", "Milling bevellers", MIL), NOTE_MILL)),
]


def families(page=None):
    return [f for f in FAMILIES if page is None or f["page"] == page]
