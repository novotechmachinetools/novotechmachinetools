"""NovoTech premium line families other than plate rolls: section & pipe benders (angle rolls, SPB draw benders, TC-42 coiler), steelworkers
and punching machines, hydraulic presses, circle cutting & flanging, corner notchers and the BT 114-S pipe polisher
(catalogue pages 22–56).  Families for shared ISITAN pages are imported by the ISITAN modules; the rest by sahinler_pages.py."""
from sahinler_lib import *  # noqa: F401,F403

P_ANGLE, P_IRON, P_PUNCH, P_PRESS, P_NOTCH, P_POLISH = "angle-rolls", "ironworker-machines", "hydraulic-punching-machines", "hydraulic-press", "corner-notcher", "pipe-sanding-polishing-machines"
P_DRAW, P_CIRCLE = "rotary-draw-tube-benders", "circle-cutters-and-seamers"

# nominal metric roll / shaft sizes from the manufacturer's metric pages (inch → mm rounding would miss them by 1–3 mm)
ROLLS_MM = {("Top roll Ø", "PK 30"): [148], ("Bottom rolls Ø", "PK 30"): [118], ("Top roll Ø", "PK 35"): [155], ("Bottom rolls Ø", "PK 35"): [155],
            ("Standard roll Ø", "HPK 40"): [137], ("Top roll Ø", "HPK 50"): [192], ("Bottom rolls Ø", "HPK 50"): [162],
            ("Standard roll Ø", "HPK 65"): [180], ("Standard roll Ø", "HPK 80"): [245], ("Standard roll Ø", "TC-42 NC"): [165]}

S_INCH = lambda lab: (lab, lab, "", inch, False)            # noqa: E731
S_MOTOR = ("Motor power", "Motor power", "", motor, False)
S_SPEED = ("Rolling speed", "Rolling speed", "", speed, False)
S_DIMS = ("Dimensions", "Dimensions L × W × H", "", dims, False)
S_WT = ("Weight", "Weight", "", weight, False)


def force_row(tb, label="Hydraulic force"):
    R = rows_of(tb)
    mt = next((R[k] for k in R if k.startswith(label) and "metric" in k), None)
    us = next((R[k] for k in R if k.startswith(label) and "US" in k), None)
    if not mt or not us:
        return None
    return {"label": label, "sub": "", "cells": [tons(m, u) for m, u in zip(mt, us)], "key": True}


def bender_table(page, title, sub, shaft_rows, roll_rows, extra=()):
    tb = table(page, 0)
    spec = [S_INCH(r) for r in shaft_rows] + [S_INCH(r) for r in roll_rows] + list(extra) + [S_SPEED, S_MOTOR, S_DIMS, S_WT]
    t = spec_table(tb, title, sub, spec, ROLLS_MM)
    f = force_row(tb)
    if f:
        i = next(i for i, r in enumerate(t["rows"]) if r["label"] == "Rolling speed")
        t["rows"].insert(i, f)
    return t


GK_BENDER = ["shaft", "roll_diameter", "motor", "weight"]


def bender_spec(tables, chart_pages, note=NOTE_SIMPLE + " " + CHART_NOTE):
    """tables + the capacity-chart columns of the same machines; glance = [shaft Ø, roll Ø, motor, weight]."""
    all_tables = list(tables)
    for pg, machines, title in chart_pages:
        all_tables.append(chart_table(pg, machines, title, "largest section → minimum rolling diameter (outside)"))
    models, caps = [], {}
    for t in tables:
        rr = {r["label"]: r["cells"] for r in t["rows"]}
        shaft = rr.get("Roll shaft Ø") or rr.get("Top roll shaft Ø")
        roll = rr.get("Standard roll Ø") or rr.get("Top roll Ø")
        for i, m in enumerate(t["models"]):
            models.append({"name": m, "glance": [shaft[i] if shaft else "—", roll[i] if roll else "—", rr["Motor power"][i], rr["Weight"][i]]})
    return {"kind": "table", "tables": all_tables, "models": models, "glance_keys": GK_BENDER, "caps": caps, "note": note}


# ------------------------------------------------------------------ section & pipe benders (angle rolls)
OPT_HPK_V = VOLT
ANGLE_FAMILIES = [
    dict(id="sahinler-pk", group="sahinler-angle", page=P_ANGLE, brand="sahinler",
         name="PK 30 · PK 35 motorized section and pipe benders",
         short="PK 30 · PK 35",
         models_label="PK 30 · PK 35 · Ø1.18″ and 1.97″ shafts",
         summary="Compact motorized angle rolls for flat bar, angle, square bar, tube and pipe — the first roll bender of the railing, "
                 "furniture and ornamental shop. The PK 30 drives its two bottom rolls by gear directly from the gearbox with an idle top "
                 "roll and a two-speed motor; the PK 35 drives two rolls through a hardened gear train, runs horizontally or vertically "
                 "and takes a bar-twist or C & S scroll-forming attachment. Hardened rolls on hardened and ground special-steel shafts, "
                 "adjustable guide rolls and a standard roll set are included; pipe, angle and special profile rolls are optional.",
         features=["PK 30: two bottom rolls driven by gear system directly from the gearbox, idle top roll, two-speed motor",
                   "PK 35: two rolls direct-driven by gear system, roll shafts in bearings, horizontal and vertical working position",
                   "Hardened rolls; roll shafts of special steel, hardened and ground; steel frame", "Standard rolls and adjustable guide rolls included"],
         optional=["Pipe / tube bending rolls; angle bending rolls; special profile rolls", "Digital readout; special lateral angle guides",
                   "Bar-twist attachment and C & S forming attachment (PK 35); two-speed motor (PK 35)", VOLT],
         images=["sh-pk35", "sh-pk30", "sh-pk35-b"],
         videos=vids(("WjqJVURbZ6U", "PK 35 angle roll — 2″ tube"), ("4IdFAbpuV8s", "PK 30 ring roller"), ("ID81kR5uI8E", "PK 35 mechanical ring roller")),
         specs=bender_spec([bender_table(24, "PK 30 · PK 35", "motorized section & pipe benders", ["Roll shaft Ø"], ["Top roll Ø", "Bottom rolls Ø"])],
                           [(32, ["PK 30", "PK 35"], "PK 30 · PK 35 — section bending capacities")]),
         headline="Flat bar to 2-3/8 × 3/8″ · square bar to 1-3/8″ · pipe to NPS 2 · angle to L 2 × 2 × 1/4″"),
    dict(id="sahinler-hpk-40", group="sahinler-angle", page=P_ANGLE, brand="sahinler",
         name="HPK 40 hydraulic section and pipe bender",
         short="HPK 40",
         models_label="HPK 40 · Ø1.38″ shafts · 2 HP",
         summary="The smallest hydraulic angle roll in the range, on a stable cast-steel frame: motor-driven rolls, hydraulic up/down "
                 "bottom rolls with two digital readouts, horizontal and vertical working position and lateral side supports. Made for "
                 "tight inner radii — rings from flat bar, small-diameter tube and angle — with NC control, spiral-bending crane and "
                 "pipe rolls as options.",
         features=["Stable cast-steel frame; rolls motor-driven; special hardened and polished rolls", "Bottom rolls hydraulic up/down with two digital readouts",
                   "Horizontal and vertical working position; lateral side supports", "Brake motor for precision bending; mobile control panel"],
         optional=["NC control", "Spiral bending crane", "Pipe / tube bending rolls; special profile rolls", VOLT],
         images=["sh-hpk40", "sh-hpk40-coil"],
         videos=vids(("JGPsDq7ph8A", "HPK 40 angle roll — rolling tight rings"), ("baJdE0W_Puk", "HPK 40 roll bender — small inner radius"), ("2wLeLjYmBKo", "HPK 40 hydraulic profile bending roll")),
         specs=bender_spec([bender_table(25, "HPK 40", "hydraulic section & pipe bender", ["Top roll shaft Ø", "Bottom roll shafts Ø"], ["Standard roll Ø"])],
                           [(32, ["HPK 40"], "HPK 40 — section bending capacities")]),
         headline="Flat bar to 2 × 1/2″ · square bar to 11/16″ · pipe to NPS 1 · angle to L 1-3/8 × 1-3/8 × 3/16″"),
    dict(id="sahinler-hpk-50-60", group="sahinler-angle", page=P_ANGLE, brand="sahinler",
         name="HPK 50 · HPK 60 hydraulic section and pipe benders",
         short="HPK 50 · HPK 60",
         models_label="HPK 50 (9 US tons) · HPK 60 (18 US tons)",
         summary="The most popular NovoTech premium line angle rolls in Canada: welded steel frame, all three rolls motor-driven with a brake motor for "
                 "precise stops, hydraulic up/down top roll and horizontal or vertical working position. The HPK 50 bends with 9 US "
                 "tons of hydraulic force — angle to L 2 × 2 × 1/4″, pipe to NPS 2; the HPK 60 with 18 US tons takes L 2-3/4 × 2-3/4 × "
                 "1/4″ angle, NPS 3 pipe and 2-3/4″ square tube. Digital readout, NC control, lateral angle guides, stairway attachment "
                 "and Delrin rolls for aluminum and stainless are the usual options.",
         features=["Steel welded construction frame; all 3 rolls motor-driven; hardened shafts of special steel", "Top roll hydraulic up/down; 9 / 18 US tons hydraulic force",
                   "Horizontal and vertical working position; standard rolls and guide rolls", "Brake motor for precision bending; mobile control panel"],
         optional=["Pipe / tube bending rolls; profile rolls; angle bending rolls", "Digital readout; NC control", "Lateral angle guides; stairway bending attachment",
                   "Special Delrin rolls for aluminum and stainless steel", VOLT],
         images=["sh-hpk60", "sh-hpk50"],
         videos=vids(("gQlXmbOJOwk", "HPK 60 angle roll — 3″ pipe"), ("f1cJ_Z2jkWM", "HPK 60 angle roll with digital readout"), ("0VJxlVlf3UI", "Angle iron rolling on the HPK 50"), ("ouH4xfmGyZY", "HPK 60 NC angle roll")),
         specs=bender_spec([bender_table(26, "HPK 50 · HPK 60", "hydraulic section & pipe benders", ["Roll shaft Ø"], ["Top roll Ø", "Bottom rolls Ø"])],
                           [(32, ["HPK 50", "HPK 60"], "HPK 50 · HPK 60 — section bending capacities")]),
         headline="Angle to L 2-3/4 × 2-3/4 × 1/4″ · pipe to NPS 3 · square tube to 2-3/4″ · flat bar to 4-3/4 × 1″"),
    dict(id="sahinler-hpk-65-80", group="sahinler-angle", page=P_ANGLE, brand="sahinler",
         name="HPK 65 · HPK 80 hydraulic section and pipe benders",
         short="HPK 65 · HPK 80",
         models_label="HPK 65 · HPK 80 · Ø2.36″ and 3.15″ top shafts",
         summary="Double-pinch angle rolls with hydraulic bottom rolls and two digital readouts: all three rolls are driven, the shafts "
                 "are hardened and ground high-tensile special steel and the machine works horizontally or vertically. The HPK 65 rolls "
                 "L 2-3/8 × 2-3/8 × 1/4″ angle and NPS 2 pipe; the HPK 80 goes to L 3-1/8 × 3-1/8 × 5/16″, NPS 3 pipe and UPN 140 "
                 "channel. 2-axis hydraulic lateral guide rolls, NC control and a spiral-rolling crane are optional.",
         features=["Steel welded construction frame; all 3 rolls driven", "Hardened and ground high-tensile special-steel shafts; hardened and ground rolls",
                   "Bottom rolls hydraulic up/down; 2 digital readouts", "Horizontal and vertical working position; brake motor; mobile control panel"],
         optional=["Pipe, tube and profile bending rolls", "2-axis hydraulic lateral guide rolls", "Automation with NC control", "Crane system for spiral rolling", VOLT],
         images=["sh-hpk80", "sh-hpk65", "sh-hpk65-horizontal", "sh-hpk-guide-detail", "sh-hpk-console"],
         videos=vids(("r-EPaVtz0sA", "HPK 65 profile rolling machine with digital readout"), ("_ZMcJ7YJmTg", "HPK 80 NC roll bender — pipe"), ("l8r_5GLfvhw", "HPK 80 NC angle roll"), ("0FxGiDxlHBQ", "HPK 65 hydraulic profile bending machine")),
         specs=bender_spec([bender_table(27, "HPK 65 · HPK 80", "hydraulic section & pipe benders", ["Top roll shaft Ø", "Bottom roll shafts Ø"], ["Standard roll Ø"])],
                           [(33, ["HPK 65", "HPK 80"], "HPK 65 · HPK 80 — section bending capacities")]),
         headline="Angle to L 3-1/8 × 3-1/8 × 5/16″ · pipe to NPS 3 · channel to UPN 140 · flat bar to 4-7/8 × 1″"),
    dict(id="sahinler-hpk-100-120", group="sahinler-angle", page=P_ANGLE, brand="sahinler",
         name="HPK 100 · HPK 120 hydraulic section and pipe benders",
         short="HPK 100 · HPK 120",
         models_label="HPK 100 (10 HP) · HPK 120 (20 HP, hydraulic guides standard)",
         summary="Heavy angle rolls for the structural and tank shop. The HPK 100 drives its three rolls from a single gearbox and "
                 "hydromotor on Ø3.94″ shafts and rolls L 3-7/8 × 3-7/8 × 1/2″ angle, NPS 4 pipe and IPN 180 beams; the HPK 120 gives "
                 "each roll its own planetary gearbox and hydromotor, has hydraulic lateral angle guides and infinitely variable speed "
                 "as standard, and rolls NPS 5 pipe, UPN 220 channel and 4-3/4 × 1-5/8″ rectangular tube. Both work horizontally and "
                 "vertically; 3-axis hydraulic guides, NC control, spiral crane and the half-pipe bending attachment are optional.",
         features=["HPK 100: single gearbox with hydromotor drives 3 rolls by gear system; HPK 120: each roll driven by its own planetary gearbox and hydromotor",
                   "Hardened and ground high-tensile special-steel shafts; hardened standard rolls", "Bottom rolls hydraulic up/down; 2 digital readouts",
                   "HPK 120: hydraulic lateral angle guide rolls and infinitely variable speed standard", "Horizontal and vertical working position; mobile control panel"],
         optional=["Pipe, tube and profile bending rolls; IPN / UPN beam attachments", "3-axis hydraulic lateral guide rollers", "Infinitely variable speed (HPK 100)",
                   "Automation with NC control", "Crane system for spiral rolling", "Half-pipe bending attachment", VOLT],
         images=["sh-hpk100", "sh-hpk120nc", "sh-hpk100-rolls", "sh-hpk100-guide", "sh-hpk100-handwheel", "sh-hpk100-horizontal", "sh-hpk120-panel", "sh-hpk-halfpipe"],
         videos=vids(("eGdImYgyjZ8", "HPK 100 angle roll — 5″"), ("M2nYe99jzBM", "HPK 100 NC double-pinch angle roll"), ("2HHkR7Ld9fE", "HPK 100 NC roll bender"), ("HK-GhfJwcjI", "HPK 120 corrugated profile (guard rail) roll bender"), ("PY_GMtb1i-4", "HPK 120 U-beam roll bender")),
         specs=bender_spec([bender_table(28, "HPK 100 · HPK 120", "hydraulic section & pipe benders", ["Roll shaft Ø"], ["Standard roll Ø"])],
                           [(33, ["HPK 100", "HPK 120"], "HPK 100 · HPK 120 — section bending capacities")]),
         headline="Angle to L 4-3/4 × 4-3/4 × 1/2″ · pipe to NPS 5 · channel to UPN 220 · beams to IPN 220 / HEB 120"),
    dict(id="sahinler-hpk-dp", group="sahinler-angle", page=P_ANGLE, brand="sahinler",
         name="HPK 160 – 360 DP heavy-duty hydraulic section and beam benders",
         short="HPK DP heavy-duty",
         models_label="HPK 160 DP · 180 DP · 200 DP · 240 DP · 300 DP · 360 DP",
         summary="Heavy-duty double-pinch section benders in which each of the three rolls is driven by its own planetary gearbox and "
                 "hydromotor, on shafts from Ø6.3″ to Ø14.2″. Built for structural beams and heavy sections — from UPN 280 channel, "
                 "IPN 300 and HEB 180 beams on the HPK 160 DP up to UPN 600, IPN 600 and HEB 600 on the HPK 360 DP, pipe to NPS 16 "
                 "and angle to L 7-7/8 × 7-7/8 × 1-1/8″. Hydraulic lateral angle guide rolls, two-speed working and two digital "
                 "readouts are standard; NC control and HEB / IPN / UPN beam attachments are optional.",
         features=["Each of the 3 rolls driven by its own planetary gearbox and hydromotor", "Hardened and ground high-tensile special-steel shafts; hardened standard rolls",
                   "Hydraulic lateral angle guide rolls; lateral rolls hydraulic up/down", "Two-speed working system; 2 digital readouts standard", "Horizontal working position; steel construction welded frame"],
         optional=["All types of pipe, tube and profile rolls; HEB / IPN / UPN beam attachments", "Automation with NC control", VOLT],
         images=["sh-hpk160dp", "sh-hpk240dp", "sh-hpkdp-top", "sh-ipn-attachment"],
         videos=vids(("Q4s3okCn65Q", "HPK 300 heavy-duty structural section bending roll"), ("U0bTM5_YK9g", "HPK 160 hydraulic ring roller — angle and pipe"), ("wZJmGplhR6Y", "HPK 180 H-beam bender"), ("k3qj4i1u0_w", "HPK 200 marine T-profile roll bender")),
         specs=bender_spec([bender_table(30, "HPK DP", "heavy-duty section & beam benders", ["Roll shaft Ø"], ["Standard roll Ø"])],
                           [(34, ["HPK 160 DP", "HPK 180 DP", "HPK 200 DP", "HPK 240 DP", "HPK 300 DP", "HPK 360 DP"], "HPK DP — section and beam bending capacities")]),
         headline="Beams to HEB 600 · channel to UPN 600 · pipe to NPS 16 · angle to L 7-7/8 × 7-7/8 × 1-1/8″"),
    dict(id="sahinler-tc-42", group="sahinler-coil", page=P_ANGLE, brand="sahinler",
         name="TC-42 NC tube coiling machine",
         short="TC-42 NC coiler",
         models_label="TC-42 NC · Ø2.56″ shafts · 10 HP",
         summary="An NC-controlled coil rolling machine for heating coils, heat-exchanger and tank jackets: it rolls variable-pitch spiral "
                 "coils with straight elbows at the start and finish in a single pass by automation. Three rolls driven by one gearbox "
                 "and hydromotor, hydraulic lateral supports with rollers, hydraulic top support, infinitely variable speed and a "
                 "material support stand are standard; tube from 12 ga wall.",
         features=["NC control panel standard — variable-pitch coils with elbows at start and finish in one pass", "Single gearbox with hydromotor drives 3 rolls; rolls hardened and ground in the bore",
                   "Hydraulic lateral supports with roller; manual lateral supports; hydraulic top support", "Infinitely variable speed; bottom rolls hydraulic up/down; material support stand"],
         optional=["Pipe, tube and profile bending rolls", VOLT],
         images=["sh-tc42", "sh-tc42-coil"],
         videos=vids(("QhEGGGOO4ug", "TC 42 NC tube coil rolling machine"), ("S_Irw3iNxd8", "TC 42 NC pipe coiling machine")),
         specs=simple_spec([generic_table(31, 0, "TC-42 NC", "tube coiling machine", [S_INCH("Top roll shaft Ø"), S_INCH("Bottom roll shafts Ø"), S_INCH("Standard roll Ø"), ("Min. tube wall", "Min. tube wall", "", cap, True), S_SPEED, S_MOTOR, S_DIMS, S_WT], ROLLS_MM)],
                          GK_BENDER, ["Top roll shaft Ø", "Standard roll Ø", "Motor power", "Weight"]),
         headline="Spiral and variable-pitch tube coils · tube wall from 12 ga · NC control standard"),
]

# ------------------------------------------------------------------ SPB draw benders (rotary draw tube benders page)
SPB_FAMILIES = [
    dict(id="sahinler-spb", group="sahinler-draw", page=P_DRAW, brand="sahinler",
         name="SPB 60 · SPB 76 NC pipe draw benders",
         short="SPB 60 · SPB 76",
         models_label="SPB 60 (Ø2-3/8″) · SPB 76 (Ø3″)",
         summary="Rotary draw benders with an NC control screen and 500-program memory for handrail, furniture, fitness equipment and "
                 "exhaust work. The SPB 60 bends pipe up to Ø2-3/8″ × 8 ga, the SPB 76 up to Ø3″ × 11 ga, at a minimum radius of 3× "
                 "the tube diameter; a holder attachment supports the tube while it is clamped, free holes take special tooling and "
                 "one set of pipe-bending tooling is included. Infinitely variable speed, thermal overload protection and emergency stop.",
         features=["NC control screen with 500-program internal memory", "SPB 60: pipe to Ø2-3/8″ × 8 ga; SPB 76: pipe to Ø3″ × 11 ga; minimum bending radius 3 × tube Ø",
                   "Holder attachment supports the tube while clamped; free holes for mounting special tools", "1 set of pipe bending tooling included; infinitely variable speed",
                   "Welded steel construction frame; thermal overload / power reset; emergency stop"],
         optional=["Pipe, tube, section or bar tooling sets to required size", VOLT],
         images=["sh-spb76", "sh-spb60", "sh-spb-handrail"],
         videos=vids(("bNLJxsDqr4U", "SPB 76 pipe bender with NC controller"), ("Jbw-7lCxxqE", "SPB 76 pipe draw bender"), ("GBahTNVoke4", "SPB 60 pipe draw bender")),
         specs=simple_spec([{"title": "SPB 60 · SPB 76", "sub": "NC pipe draw benders", "models": ["SPB 60", "SPB 76"], "rows": [
             {"label": "Mild steel tube", "sub": "max. capacity", "cells": ["Ø2-3/8″ × 11 ga (60 × 3 mm)", "Ø3″ × 10 ga (76 × 3.5 mm)"], "key": True},
             {"label": "Boiler tube", "sub": "", "cells": ["Ø2-3/8″ × 12 ga (60 × 2.5 mm)", "Ø3″ × 11 ga (76 × 3 mm)"], "key": False},
             {"label": "Aluminum tube", "sub": "", "cells": ["Ø2-3/8″ × 8 ga (60 × 4 mm)", "Ø3″ × 1/4″ (76 × 6 mm)"], "key": False},
             {"label": "Round bar, mild steel", "sub": "", "cells": ["Ø1-5/8″ (40 mm)", "Ø1-3/4″ (45 mm)"], "key": False},
             {"label": "Square tube, mild steel", "sub": "", "cells": ["□1-5/8″ × 8 ga (40 × 4 mm)", "□1-5/8″ × 3/16″ (40 × 5 mm)"], "key": False},
             {"label": "Min. bending radius", "sub": "", "cells": ["R2.4″ (Ø5/8″ × 8 ga)", "R3″ (Ø5/8″ × 11 ga)"], "key": False},
             {"label": "Max. bending radius", "sub": "", "cells": ["R5.9″ (Ø2-3/8″ × 10 ga)", "R8.7″ (Ø3″ × 10 ga)"], "key": False},
             {"label": "Working speed", "sub": "", "cells": ["0 – 4.5 rpm", "0 – 4 rpm"], "key": False},
             {"label": "Motor power", "sub": "", "cells": [motor("3.0"), motor("4.0")], "key": False},
             {"label": "Dimensions L × W × H", "sub": "", "cells": [dims("33 × 30 × 47"), dims("37 × 33 × 49")], "key": False},
             {"label": "Weight", "sub": "", "cells": [weight("728"), weight("1,102")], "key": False}]}],
             ["capacity", "radius", "motor", "weight"], ["Mild steel tube", "Min. bending radius", "Motor power", "Weight"]),
         headline="Pipe to Ø3″ × 10 ga (76 × 3.5 mm) · NC control with 500 programs · 1 tooling set included"),
]

# ------------------------------------------------------------------ steelworkers (ironworkers) and punching machines
HKM_SPEC = [("Punching — Ø × max. thickness", "Punching, max. thickness", "Ø × thickness", None, True),
            ("Ø × thickness", "Punching, larger hole", "Ø × thickness", None, False),
            ("Max. Ø × thickness", "Punching, max. Ø", "Ø × thickness", None, False),
            ("Punching force", None, None, None, None),    # placeholder, replaced by force_row
            ("Stroke", "Stroke", "", lambda c: inch(c), False), ("Strokes / min", "Strokes per minute", "at 0.8″ stroke", None, False),
            ("Throat depth", "Throat depth", "", lambda c: inch(c), False),
            ("Bar shear", "Bar shear — round · square", "", None, True), ("Angle shear 90°", "Angle shear 90°", "", None, True), ("Angle shear 45°", "Angle shear 45°", "", None, False),
            ("Flat-bar shear — width", "Flat-bar shear", "width × thickness", None, True), ("Flat-bar shear (wide)", "Flat-bar shear, wide", "width × thickness", None, False),
            ("Blade length", "Blade length", "", lambda c: inch(c), False),
            ("Notching — thickness", "Notching — thickness", "", cap, False), ("Notch width × depth", "Notch width × depth", "", dims, False),
            ("Opt. UPN / IPN blades", "Optional UPN / IPN blades", "", None, False), ("Opt. Tee blades", "Optional Tee blades", "", None, False),
            ("Opt. V-notching blade", "Optional V-notching blade", "", None, False), ("Opt. press brake — bar", "Optional press-brake tool — bar", "", None, False),
            ("Opt. press brake — sheet", "Optional press-brake tool — sheet", "", None, False),
            S_MOTOR, S_DIMS, S_WT]


def tidy(c):
    return c.replace("⁄", "/")


def hkm_table(page, title, sub):
    tb = table(page, 0)
    spec = [(p, n, s, (conv or tidy), k) for p, n, s, conv, k in HKM_SPEC if n]
    t = spec_table(tb, title, sub, spec)
    f = force_row(tb, "Punching force")
    i = next(i for i, r in enumerate(t["rows"]) if r["label"] == "Stroke")
    t["rows"].insert(i, f)
    return t


GK_IRON = ["punching", "angle", "flat_bar", "force", "weight"]
NOTE_IRON = ("Capacities are for mild steel of 65,000 psi (450 N/mm²) tensile strength; thickness in gauge / common fraction. * with a special tool · "
             "** with the optional large-hole punching tool. Dimensions are overall L × W × H. All models punch Ø1/4″ up to Ø1-1/2″ as standard.")

IRON_FAMILIES = [
    dict(id="sahinler-hkm-single", group="sahinler-iron", page=P_IRON, brand="sahinler",
         name="HKM 40 · 45 · 60 · 65 V single-piston hydraulic ironworkers",
         short="HKM single-piston",
         models_label="HKM 40 (44 US tons) · HKM 45 (50) · HKM 60 (66) · HKM 65 V (72)",
         summary="Hydraulic steelworkers in which one cylinder serves every work station — compact and economical for the shop that "
                 "punches, shears and notches one job at a time. Punching, round and square bar shear, angle shear at 90° and 45°, "
                 "flat-bar shear and (except on the HKM 40) a rectangular notching station, all with LED lighting, central lubrication "
                 "and adjustable piston stroke. The HKM 65 V puts the piston vertical for vertical punching and cutting. A Ø7/8″ punch "
                 "and die and the standard blade sets are included.",
         features=["One hydraulic cylinder serves all work stations: punching, round and square bar shear, angle shear 90° / 45°, flat-bar shear, U-notching (not on HKM 40)",
                   "Adjustable piston stroke for higher productivity; central lubrication; LED lighting on all stations", "Ø7/8″ punch & die and standard punching tools; round and square bar blade set; angle blade set; U-notching blade set",
                   "HKM 65 V: vertical piston layout for vertical punching and cutting; spot lubrication", "Punches up to Ø1-1/2″ as standard — punches and dies change quickly, special punches at short notice"],
         optional=["Large-hole punching tool — Ø1-1/2″ (5/16″ thick) up to Ø4-3/8″ (1/8″ thick)", "Section punching tools for IPN, UPN, flat bar and angle", "Section blades for UPN, IPN and T; V-notching blade",
                   "Press-brake tool on the punching station; hydraulic stripper", VOLT],
         images=["sh-hkm60", "sh-hkm40", "sh-hkm65v", "sh-hkm40-rear", "sh-hkm-tool-punches", "sh-hkm-tool-notch"],
         videos=vids(("Ih_g56w46tU", "HKM 60 ironworker machine"), ("jtzBulD29sQ", "HKM 40 (44 US ton) hydraulic ironworker"), ("7i0384bLxF0", "HKM 60 (66 US ton) hydraulic ironworker"), ("n-OjAP38XNA", "HKM 65 V single-piston vertical ironworker"), ("MQrQtCYScJY", "Angle iron miter cutting on the HKM 60")),
         specs=simple_spec([hkm_table(39, "HKM single piston", "HKM 40 · 45 · 60 · 65 V")], GK_IRON, ["Punching, max. thickness", "Angle shear 90°", "Flat-bar shear", "Punching force", "Weight"], NOTE_IRON),
         headline="44 – 72 US tons · punch to Ø1-1/8 × 9/16″ · angle to L 4-3/4 × 4-3/4 × 1/2″ · 4 – 5 work stations"),
    dict(id="sahinler-hkm-double", group="sahinler-iron", page=P_IRON, brand="sahinler",
         name="HKM 55 · 65 · 85 · 115 · 175 double-piston hydraulic ironworkers",
         short="HKM double-piston",
         models_label="HKM 55 (61 US tons) · 65 (72) · 85 (94) · 115 (127) · 175 (193)",
         summary="Two separate hydraulic cylinders and two foot pedals, so two operators work at the same time — one punching, the other "
                 "shearing angle, bar or flat, or notching. Electrical back gauge, adjustable piston stroke, central lubrication and LED "
                 "lighting on every station; the HKM 115 comes with a Ø1″ punch and die and the HKM 175 with an oil cooling system. From "
                 "61 to 193 US tons: angle to L 7-7/8 × 7-7/8 × 13/16″, flat bar to 15 × 1-1/8″, round bar to Ø2-1/2″ and holes to "
                 "Ø2-1/4″ in 7/8″ plate on the HKM 175.",
         features=["2 separate hydraulic cylinders and foot pedals — 2 operators work at the same time", "Electrical back gauge; adjustable piston stroke; central lubrication; LED lighting on all work stations",
                   "Punching, round and square bar shear, angle shear 90° / 45°, flat-bar shear and U-notching stations; Ø1″ punch & die on HKM 115", "Oil cooling system on the HKM 175",
                   "Ideal for cutting all ranges of angle, I-beam and U-section with the optional section blades"],
         optional=["Large-hole punching tool — up to Ø4-7/8″ × 3/16″", "Section punching tools for IPN, UPN, flat bar and angle; section blades for UPN, IPN and T", "V-notching blade; press-brake tool; hydraulic stripper",
                   "NC feeding table on the punching station", VOLT],
         images=["sh-hkm115", "sh-hkm85", "sh-hkm65", "sh-hkm55", "sh-hkm175", "sh-hkm175-operators", "sh-hkm175-backgauge", "sh-hkm115-detail", "sh-hkm-lube", "sh-hkm-tool-brake", "sh-hkm-tool-stripper", "sh-hkm-tool-radius"],
         videos=vids(("wY5bTK1XnnE", "HKM 60, HKM 85 and HKM 115 hydraulic ironworkers — walk-around"), ("Tt33aBsxH-4", "HKM 115 ironworker machine"), ("tVxDdnI7tEI", "HKM 85 (94 US ton) hydraulic ironworker"), ("nSbf4Dwcoog", "HKM 65 (72 US ton) hydraulic ironworker"), ("jd5xdM5LENs", "HKM 175 hydraulic ironworker — all functions"), ("Qaj7a7gDubg", "HKM 115 NC steelworker — keyway punching")),
         specs=simple_spec([hkm_table(40, "HKM double piston", "HKM 55 · 65 · 85 · 115 · 175")], GK_IRON, ["Punching, max. thickness", "Angle shear 90°", "Flat-bar shear", "Punching force", "Weight"], NOTE_IRON),
         headline="61 – 193 US tons · two operators at once · angle to L 7-7/8 × 7-7/8 × 13/16″ · holes to Ø2-1/4″ × 7/8″"),
]

HPM_SPEC = [("Punching — Ø × max. thickness", "Punching, max. thickness", "Ø × thickness", tidy, True), ("Ø × thickness", "Punching, larger hole", "Ø × thickness", tidy, False),
            ("Max. Ø × thickness", "Punching, max. Ø", "Ø × thickness", tidy, False), ("Stroke", "Stroke", "", lambda c: inch(c), False),
            ("Strokes / min", "Strokes per minute", "at 0.8″ stroke", None, False), ("Throat depth", "Throat depth", "", lambda c: inch(c), True),
            ("Working height", "Working height", "", lambda c: inch(c), False), ("Opt. press brake — bar", "Optional press-brake tool — bar", "", tidy, False),
            ("Opt. press brake — sheet", "Optional press-brake tool — sheet", "", tidy, False), S_MOTOR, S_DIMS, S_WT]


def hpm_table():
    tb = table(45, 0)
    t = spec_table(tb, "HPM", "hydraulic punching machines · 6 models", [s for s in HPM_SPEC])
    i = next(i for i, r in enumerate(t["rows"]) if r["label"] == "Stroke")
    t["rows"].insert(i, force_row(tb, "Punching force"))
    return t


def hpm_dp_table():
    tb = table(42, 0)
    t = spec_table(tb, "HPM DP", "double-head punching machines", [S_DIMS, S_WT])
    t["rows"].insert(0, force_row(tb, "Punching force"))
    return t


GK_PUNCH = ["punching", "throat", "force", "weight"]
PUNCH_FAMILIES = [
    dict(id="sahinler-hpm", group="sahinler-punch", page=P_PUNCH, brand="sahinler",
         name="HPM 30 – 175 hydraulic punching machines",
         short="HPM punching machines",
         models_label="HPM 30 (33 US tons) · 40 · 65 · 85 · 115 · 175 (193 US tons)",
         summary="Single-station hydraulic punches for holes and shapes from Ø1/4″ up to Ø2-1/4″ in plate to 1-1/4″ thick: the HPM 30 "
                 "and 40 are the compact punches with an 11.8″ throat, the HPM 65 to 175 have a 24.6″ throat for punching deep into "
                 "plate, angle and flat bar. A punch holder, a Ø7/8″ (HPM 65 / 85) or Ø1″ (HPM 115 / 175) punch and die, LED light "
                 "and C-spanner are included; punches and dies interchange with the HKM steelworkers. A hydraulic stripper, press-brake "
                 "tool and NC table system are optional.",
         features=["Punch & die Ø7/8″ (HPM 65 / 85) or Ø1″ (HPM 115 / 175) included; punch holder; C-spanner", "LED light on the work station",
                   "Throat depth 11.8″ (HPM 30 / 40) or 24.6″ (HPM 65 – 175)", "Punches and dies interchangeable with the HKM steelworkers — special tools on request"],
         optional=["Punching tools from Ø1/4″ up to Ø2-1/4″ (max. 1-1/4″ thick); special tools", "Hydraulic stripper", "Press-brake tool", "NC table system", VOLT],
         images=["sh-hpm65", "sh-hpm30", "sh-hpm115", "sh-hpm-station", "sh-hpm-punch"],
         videos=vids(("sXaJHhUVtnE", "HPM 40 Ton punching machine"), ("PAxfpuBlUlY", "HPM 65 (72 US ton) hydraulic plate punching machine"), ("TNc_jYos-VA", "HPM 115 hydraulic punching machine"), ("v9mC9fqcVcE", "HPM 115 hydraulic punching machine — tools")),
         specs=simple_spec([hpm_table()], GK_PUNCH, ["Punching, max. thickness", "Throat depth", "Punching force", "Weight"], NOTE_IRON),
         headline="33 – 193 US tons · holes Ø1/4″ to Ø2-1/4″ · plate to 1-1/4″ · throat 11.8″ / 24.6″"),
    dict(id="sahinler-hpm-dp", group="sahinler-punch", page=P_PUNCH, brand="sahinler",
         name="HPM 65 – 175 DP double-head hydraulic punching machines",
         short="HPM DP double-head",
         models_label="HPM 65 DP · 85 DP · 115 DP · 175 DP · 2 × 72 to 2 × 193 US tons",
         summary="Two punching heads on one frame with double motor and double foot-pedal control: two operators punch at the same time, "
                 "or two different tools stay set up for the same part. Each head has the capacity of the single HPM of the same size — "
                 "2 × 72 to 2 × 193 US tons, holes to Ø2-1/4″ — with a hydraulic stripper as the usual option.",
         features=["Two punching heads, double motor and double foot-pedal control", "Each head with the full capacity of the single-head HPM; punch holders and punch & die included",
                   "Two operators at once, or two tools set up for the same part", "LED lights on the work stations"],
         optional=["Hydraulic stripper", "Punching tools Ø1/4″ – Ø2-1/4″; special tools", VOLT],
         images=["sh-hpm85dp"],
         videos=[],
         specs=simple_spec([hpm_dp_table()], ["force", "dimensions", "weight"], ["Punching force", "Dimensions L × W × H", "Weight"], NOTE_IRON + " Punching capacities per head as the HPM of the same size."),
         headline="2 × 72 to 2 × 193 US tons · two operators at once"),
    dict(id="sahinler-hpm-cnc", group="sahinler-punch", page=P_PUNCH, brand="sahinler",
         name="HPM 85 · 115 · 175 CNC punching machines",
         short="HPM CNC",
         models_label="HPM 85 CNC · 115 CNC · 175 CNC · Siemens control",
         summary="The HPM punch on a 120 × 20″ CNC table (X 63″ / Y 23.6″ travel, 550 lb carriage load) with Siemens control: ideal for "
                 "bolted steel-construction work where every hole must match — base plates, gussets, splice plates and flat bar from "
                 "14 ga to 1″ thick at ±0.004″ positioning accuracy. Material is held in hydraulic clamps on a divisible table, the "
                 "axes run at 79 ft/min (98 ft/min on two axes) and the free software takes manual (MDI) punching or CAM programs with "
                 "a 1-3/4″ minimum edge distance. A 3-head punching unit is optional on the 115 and 175.",
         features=["CNC table 120 × 20″ · X 63″ / Y 23.6″ travel · 550 lb max. carriage load; divisible separate table with hydraulic clamps",
                   "Material 14 ga to 1″ thick; positioning accuracy ±0.004″; 79 ft/min on one axis, 98 ft/min on two axes",
                   "Mobile CNC control panel (Siemens); free software — manual punching (MDI) and CAM program entry; min. 1-3/4″ edge distance",
                   "Punch & die Ø7/8″ (HPM 85) or Ø1″ (HPM 115 / 175); punch holder; automatic lubrication system; LED light; C-spanner"],
         optional=["3-head punching unit (HPM 115 / 175 CNC)", "Punching tools Ø1/4″ – Ø2-1/4″; special tools", "Hydraulic stripper", VOLT],
         images=["sh-hpm115cnc"],
         videos=vids(("FsofcerO5nU", "HPM 115 CNC punching machine"), ("QRqZVK4bQzA", "HPM 115 CNC hydraulic punching machine"), ("7z2Ypj10HOQ", "HPM 115 CNC punch with triple punching head")),
         specs=simple_spec([{"title": "HPM CNC", "sub": "CNC punching machines", "models": ["HPM 85 CNC", "HPM 115 CNC", "HPM 175 CNC"], "rows": [
             {"label": "Punching force", "sub": "", "cells": [tons(85, 94), tons(115, 127), tons(175, 193)], "key": True},
             {"label": "Punching, max. thickness", "sub": "Ø × thickness", "cells": ["Ø1-1/4 × 13/16″*", "Ø1-3/8 × 1″", "Ø1-5/8 × 1-1/4″"], "key": True},
             {"label": "Punching, max. Ø", "sub": "Ø × thickness", "cells": ["Ø4-3/8 × 3/16″**", "Ø4-3/8 × 3/16″**", "Ø4-7/8 × 3/16″**"], "key": False},
             {"label": "CNC table", "sub": "", "cells": ["120 × 20″ (3050 × 500 mm)"] * 3, "key": False},
             {"label": "Axis travel X / Y", "sub": "", "cells": ["63″ / 23.6″ (1600 / 600 mm)"] * 3, "key": False},
             {"label": "Material thickness", "sub": "", "cells": ["14 ga – 1″ (2 – 25 mm)"] * 3, "key": False},
             {"label": "Positioning accuracy", "sub": "", "cells": ["±0.004″ (±0.1 mm)"] * 3, "key": False},
             {"label": "Axis speed", "sub": "one axis / two axes", "cells": ["79 / 98 ft/min (24 / 30 m/min)"] * 3, "key": False},
             {"label": "Max. carriage load", "sub": "", "cells": ["550 lb (250 kg)"] * 3, "key": False},
             {"label": "Throat depth", "sub": "", "cells": [inch("24.6")] * 3, "key": False},
             {"label": "Motor power", "sub": "punch", "cells": [motor("10"), motor("15"), motor("15")], "key": False}]}],
             GK_PUNCH, ["Punching, max. thickness", "Throat depth", "Punching force", "Weight"], NOTE_IRON),
         headline="94 – 193 US tons · 120 × 20″ CNC table · ±0.004″ · 14 ga to 1″ plate"),
    dict(id="sahinler-hpm-nc-line", group="sahinler-punch", page=P_PUNCH, brand="sahinler",
         name="HPM / HKM 65 – 175 NC punching and cutting lines",
         short="HPM / HKM NC lines",
         models_label="HPM 65 · 85 · 115 · 175 NC · HKM 65 · 85 · 115 · 175 NC",
         summary="Special punching and cutting lines for angles, flat bar, IPN and UPN sections: an HPM punch or HKM steelworker with a "
                 "307 × 31″ NC table, a 201 × 16″ loading table, X travel of 244″ and mechanical holders and feeders. The NC control "
                 "copies the hole pattern along the bar — clean holes up to Ø2-1/4″ in 7/8″ material, 14 ga to 13/16″ thick at "
                 "±0.004″ — with free software, manual punching and a copy system, programmed by technical values. On the HKM NC the "
                 "shear station cuts the punched bar to length.",
         features=["NC table 307 × 31″ · loading table 201 × 16″ · X travel 244″; mechanical holders and feeders; roller conveyor",
                   "Punching of angles, flat bar, IPN and UPN sections: holes up to Ø2-1/4″ in 7/8″ material, copied by NC", "Material 14 ga – 13/16″ thick; positioning accuracy ±0.004″",
                   "Mobile NC control panel; free software — manual punching and copy system, program by technical values", "Punch & die Ø7/8″ (65 / 85) or Ø1″ (115 / 175); punch holder; divisible separate table with manual adjustment clamps; LED light"],
         optional=["Angle punching tooling; section tools", "Hydraulic stripper", VOLT],
         images=["sh-hpm85nc"],
         videos=vids(("0Wy-gydiyQg", "HPM 85 NC programmable hydraulic punch"), ("tQkcc2WAlWc", "HKM 115 NC hydraulic ironworker with material feeder on the punching station"), ("eWnYKhe64l4", "Robotic punching cell with the HPM")),
         specs=simple_spec([{"title": "HPM / HKM NC lines", "sub": "punching & cutting lines with feeding system", "models": ["HPM / HKM 65 NC", "HPM / HKM 85 NC", "HPM / HKM 115 NC", "HPM / HKM 175 NC"], "rows": [
             {"label": "Punching force", "sub": "", "cells": [tons(65, 72), tons(85, 94), tons(115, 127), tons(175, 193)], "key": True},
             {"label": "Punching, max. thickness", "sub": "Ø × thickness", "cells": ["Ø1 × 13/16″", "Ø1-1/4 × 13/16″*", "Ø1-3/8 × 1″", "Ø1-5/8 × 1-1/4″"], "key": True},
             {"label": "NC table", "sub": "", "cells": ["307 × 31″ (7800 × 800 mm)"] * 4, "key": False},
             {"label": "Loading table", "sub": "", "cells": ["201 × 16″ (5100 × 400 mm)"] * 4, "key": False},
             {"label": "X travel", "sub": "", "cells": ["244″ (6200 mm)"] * 4, "key": False},
             {"label": "Material thickness", "sub": "", "cells": ["14 ga – 13/16″ (2 – 20 mm)"] * 4, "key": False},
             {"label": "Positioning accuracy", "sub": "", "cells": ["±0.004″ (±0.1 mm)"] * 4, "key": False}]}],
             ["force", "punching", "table"], ["Punching force", "Punching, max. thickness", "NC table"], NOTE_IRON),
         headline="72 – 193 US tons · 307 × 31″ NC table · angles, flat bar, IPN and UPN · ±0.004″"),
]

# ------------------------------------------------------------------ hydraulic presses
PRESS_SPEC = [("Press force", None, None, None, None), ("Max. working pressure", "Max. working pressure", "", psi, False), ("Stroke", "Stroke", "", lambda c: inch(c), True),
              ("Daylight", "Daylight (table to table)", "", lambda c: inch(c), False), ("Bending capacity", "Bending capacity", "mild steel", cap, True),
              ("Cylinder Ø", "Cylinder Ø (bore × rod)", "", lambda c: inch(c.replace("×", "/")).replace(" / ", " × "), False),
              ("Advance / working / return", "Advance / working / return speed", "", ins, False), ("Advance speed", "Advance speed", "", ins, False), ("Working speed", "Working speed", "", ins, False),
              ("Bottom table", "Bottom table", "", dims, False), ("Table center-hole", "Table centre-hole Ø", "", lambda c: inch(c), False),
              ("Bed-hole spacing", "Bed-hole spacing (A)", "", lambda c: inch(c), False), ("Working width", "Working width (B)", "between the columns", lambda c: inch(c), True),
              ("Depth", "Depth (C)", "", lambda c: inch(c), False), S_MOTOR, S_DIMS, S_WT]


def press_table(page, idx, title, sub):
    tb = table(page, idx)
    t = spec_table(tb, title, sub, [s for s in PRESS_SPEC if s[1]])
    t["rows"].insert(0, force_row(tb, "Press force"))
    return t


GK_PRESS = ["force", "stroke", "width", "motor", "weight"]
G_PRESS = ["Press force", "Stroke", "Working width (B)", "Motor power", "Weight"]
NOTE_PRESS = "Dimensions are overall L × W × H; working width is the clear width between the columns. Metric values in brackets are the manufacturer's nominal figures."
OPT_DPM = ["Hand pump", "Foot-pedal control", "Limit switch + foot pedal", VOLT]

PRESS_FAMILIES = [
    dict(id="sahinler-dpm", group="sahinler-press", page=P_PRESS, brand="sahinler",
         name="DPM hydraulic shop presses, 33 – 220 US tons",
         short="DPM shop presses",
         models_label="DPM 775-30 – DPM 1570-200 · 9 models",
         summary="H-frame hydraulic shop presses from 33 to 220 US tons on a welded steel frame: two-speed joystick control, a pressure "
                 "gauge and relief valve against overload, height-adjustable bottom tables with a table up/down attachment and a pair "
                 "of V-blocks. The cylinder stops at any position for straightening, pressing bearings and bushings, bending and "
                 "assembly work; a hand pump, foot pedal and limit switch are optional. Model numbers give the working width in mm "
                 "and the force in metric tons — a DPM 1040-60 is 40.9″ between the columns at 66 US tons.",
         features=["Steel construction welded frame; stops at any position", "Two-speed joystick control; pressure gauge; relief valve against overload",
                   "Height-adjustable bottom tables with table up/down movement attachment", "A pair of V-blocks included; easy to operate"],
         optional=OPT_DPM,
         images=["sh-dpm", "sh-dpm200"],
         videos=vids(("C9UMkUAX9io", "DPM 1040 × 60 Ton hydraulic shop press"), ("KZV6tOhQ-6E", "DPM 1570 × 150 hydraulic shop press — double speed")),
         specs=simple_spec([press_table(51, 0, "DPM 30 – 100", "33 – 110 US tons"), press_table(52, 0, "DPM 150 – 200", "165 – 220 US tons")], GK_PRESS, G_PRESS, NOTE_PRESS),
         headline="33 – 220 US tons (30 – 200 t) · working widths 30.5″ to 61.8″ · two-speed joystick control"),
    dict(id="sahinler-dpm-k", group="sahinler-press", page=P_PRESS, brand="sahinler",
         name="DPM-K · DK hydraulic shop presses with mobile cylinder",
         short="DPM-K · DK mobile cylinder",
         models_label="DPM-K 775-30 – DPM-K 1570-150 · DK 1570-100 – DK 1900-200",
         summary="The DPM press with a cylinder head that travels across the frame — geared movement by hand wheel — so the ram is "
                 "positioned over the work instead of the work under the ram: long shafts, frames and plates are straightened without "
                 "re-clamping. DPM-K from 33 to 165 US tons with the same two-speed joystick control, pressure gauge and relief valve, "
                 "height-adjustable tables and V-blocks as the DPM; the DK series adds a wider 61.8″ – 74.8″ frame from 110 to 220 US tons.",
         features=["Cylinder head travels across the frame — geared movement by hand wheel", "Steel construction welded frame; stops at any position",
                   "Two-speed joystick control (except 220 US ton model); pressure gauge; relief valve against overload", "Height-adjustable bottom tables with up/down attachment; a pair of V-blocks included"],
         optional=OPT_DPM,
         images=["sh-dpmk", "sh-dk"],
         videos=vids(("IaLQHL62RHQ", "DPM-K and DK hydraulic shop press with sliding cylinder"), ("aQx2zab_GHM", "DPM-K 1040 × 80 Ton workshop press")),
         specs=simple_spec([press_table(53, 0, "DPM-K 30 – 100", "33 – 110 US tons"), press_table(53, 1, "DPM-K 100 – 150", "110 – 165 US tons"), press_table(53, 2, "DK 100 – 200", "110 – 220 US tons · 61.8″ – 74.8″ wide")],
                          GK_PRESS, G_PRESS, NOTE_PRESS),
         headline="33 – 220 US tons · cylinder travels across the frame · working widths 30.5″ to 74.8″"),
    dict(id="sahinler-at", group="sahinler-press", page=P_PRESS, brand="sahinler",
         name="AT universal T-slot hydraulic presses, 110 – 165 US tons",
         short="AT T-slot presses",
         models_label="AT 1020-100 · 1520-100 · 1020-150 · 1520-150",
         summary="Hydraulic presses with T-slot top and bottom tables for die work — forming, blanking, coining and assembly tooling "
                 "bolted straight to the tables. Two guide cylinders, one each side, keep the ram square; stepless stroke adjustment by "
                 "limit switch, adjustable pressure valve, pressure gauge, height-adjustable bottom table with up/down attachment and "
                 "two-hand control. 110 or 165 US tons with 40.2″ or 59.8″ between the columns and 24″ – 26.8″ daylight.",
         features=["T-slot top and bottom tables for die work; table centre hole Ø3.9″", "Two guide cylinders, one each side; stepless stroke adjustment (limit switch)",
                   "Adjustable pressure valve; pressure gauge; two-hand control", "Height-adjustable bottom table with table up/down movement attachment; steel construction welded frame"],
         optional=[VOLT],
         images=["sh-at"],
         videos=vids(("A0-KkaGnAaM", "AT hydraulic shop press with T-slot table"), ("CDDqTYn6SU0", "AT-S 1520 × 150 Ton straight-side hydraulic press with heated platen")),
         specs=simple_spec([press_table(54, 0, "AT", "universal T-slot hydraulic presses")], GK_PRESS, G_PRESS, NOTE_PRESS),
         headline="110 – 165 US tons · T-slot tables 19.7 × 40.2″ to 23.6 × 59.8″ · daylight to 26.8″"),
    dict(id="sahinler-ap", group="sahinler-press", page=P_PRESS, brand="sahinler",
         name="AP garage-type hydraulic press brakes, 110 – 165 US tons",
         short="AP press brakes",
         models_label="AP 1020-100 · 1520-100 · 1020-150 · 1520-150",
         summary="A hydraulic press fitted with press-brake tooling for heavy plate in short lengths: a 5-face prism bottom die and "
                 "hardened blades bend 1/4″ (100 t) or 3/8″ (150 t) mild steel over 40.2″ or 59.8″, with a T-slot bottom table for "
                 "other tooling. Stepless stroke adjustment, adjustable pressure valve, pressure gauge, height-adjustable bottom "
                 "attachment, a large workspace for big sheets and two-hand control — the affordable press brake of the repair and "
                 "trailer shop, with a 29.5″ or 39.4″ manual back gauge as an option.",
         features=["Hardened blades; 5-face prism bottom die; bottom table with T-slot", "Bends 1/4″ (110 US tons) or 3/8″ (165 US tons) mild steel",
                   "Stepless stroke adjustment; adjustable pressure valve; pressure gauge", "Height-adjustable bottom attachment; large workspace for big sheets; two-hand control"],
         optional=["29.5″ (750 mm) or 39.4″ (1000 mm) manual back gauge", VOLT],
         images=["sh-ap"],
         videos=vids(("3NVkGji2fEY", "AP hydraulic shop press brake — affordable press brake for small shops"), ("WVxN1BFnKsk", "AP hydraulic press with special tooling")),
         specs=simple_spec([press_table(55, 0, "AP", "garage-type hydraulic press brakes")], GK_PRESS, G_PRESS, NOTE_PRESS),
         headline="110 – 165 US tons · bends 1/4″ – 3/8″ plate · 40.2″ and 59.8″ wide"),
    dict(id="sahinler-dk-s", group="sahinler-press", page=P_PRESS, brand="sahinler",
         name="DK-S 3-axis moving straightening presses, 220 – 441 US tons",
         short="DK-S straightening presses",
         models_label="DK-S 200/2550 · 300/2550 · 400/2550",
         summary="Gantry presses whose cylinder moves on X, Y and Z axes by motorized gear drive, so a large plate, beam, profile or "
                 "round bar lies still on the bed while the ram is brought to each point that needs straightening. Pendant control, "
                 "press safety cage, pressure gauge and stops at any position are standard on all three sizes — 220, 331 and 441 US "
                 "tons with an 11.8″ stroke; a work table, material lifting system, remote control, cylinder-stroke readout, LED lights "
                 "and bridges in other widths are optional.",
         features=["X-Y-Z axis movement of the cylinder, motorized by gear drive", "For straightening large plates and profiles, beams and round steel",
                   "Pendant-style control panel; press safety cage; pressure gauge; stops at any position", "Steel welded frame; very easy to operate"],
         optional=["Table; material lifting system", "Remote control; digital readout for cylinder stroke", "Bridge and work-table options in different widths; side-tank arrangement; LED lights", VOLT],
         images=["sh-dks400", "sh-dks200", "sh-dks-remote"],
         videos=vids(("0IGVfYrBiA8", "DK-S 400 Ton 3-axis moving hydraulic straightening press"), ("l0pVqb4BCdA", "DK-S 200 × 2500 3-axis plate straightening press")),
         specs=simple_spec([generic_table(50, 0, "DK-S", "3-axis moving straightening presses", [("Max. working pressure", "Max. working pressure", "", psi, False), ("Stroke", "Stroke", "", lambda c: inch(c), True),
                                                                                                   ("Cylinder Ø", "Cylinder Ø", "", lambda c: inch(c), False), ("Advance speed", "Advance speed", "", ins, False), ("Working speed", "Working speed", "", ins, False), S_MOTOR, S_WT])],
                          ["force", "stroke", "motor", "weight"], ["Press force", "Stroke", "Motor power", "Weight"], NOTE_PRESS),
         headline="220 – 441 US tons · cylinder moves on 3 axes over a 100″ bed · 11.8″ stroke"),
]
PRESS_FAMILIES[-1]["specs"]["tables"][0]["rows"].insert(0, force_row(table(50, 0), "Press force"))
PRESS_FAMILIES[-1]["specs"]["models"] = [{"name": m, "glance": [r for r in [next(x["cells"][i] for x in PRESS_FAMILIES[-1]["specs"]["tables"][0]["rows"] if x["label"] == l) for l in ["Press force", "Stroke", "Motor power", "Weight"]]]}
                                         for i, m in enumerate(PRESS_FAMILIES[-1]["specs"]["tables"][0]["models"])]

# ------------------------------------------------------------------ circle cutting & flanging (SDK, EFM) — ISITAN page
SDK_SPEC = [("Max. flanging plate Ø", "Max. flanging plate Ø", "", lambda c: inch(c, 10), True), ("Min. flanging plate Ø", "Min. flanging plate Ø", "", lambda c: inch(c, 10), False),
            ("Min. flanging Ø with", "Min. flanging Ø with small-Ø attachment", "optional", lambda c: inch(c, 10), False),
            ("Max. cutting plate Ø", "Max. cutting plate Ø", "", lambda c: inch(c, 10), True), ("Min. cutting plate Ø", "Min. cutting plate Ø", "", lambda c: inch(c, 10), False),
            ("Min. cutting Ø with", "Min. cutting Ø with small-Ø attachment", "optional", lambda c: inch(c, 10), False),
            ("Max. flanging height", "Max. flanging height (optional rolls)", "height (flange radius)", lambda c: c.replace("(R", "″ (R").replace(") ·", "″) ·") + "″)", False),
            ("Flanging radius", "Flanging radius", "min. – max.", lambda c: c.replace(" – ", "″ – ") + "″", False),
            ("Max. plate thickness — mild", "Max. plate thickness — mild steel", "", cap, True), ("Max. plate thickness — stainless", "Max. plate thickness — stainless 304 / 316", "", cap, False),
            S_MOTOR, S_DIMS, S_WT]
EFM_SPEC = [("Max. plate cutting Ø", "Max. plate cutting Ø", "", lambda c: inch(c, 10), True), ("Min. plate cutting Ø", "Min. plate cutting Ø", "", lambda c: inch(c, 10), False),
            ("Max. flanging height", "Max. flanging height", "", lambda c: inch(c), False), ("Max. flanging radius", "Max. flanging radius", "", lambda c: inch(c), False),
            ("Plate thickness — mild", "Plate thickness — mild steel", "", lambda c: c.replace("⁄", "/"), True), ("Plate thickness — stainless", "Plate thickness — stainless 304 / 316", "", lambda c: c, False),
            S_MOTOR, S_DIMS, S_WT]
NOTE_SDK = "Mild-steel capacities are for 37,000 psi (26 kg/mm²) yield strength. Dimensions are overall L × W × H; metric values in brackets are the manufacturer's nominal figures."

CIRCLE_FAMILIES = [
    dict(id="sahinler-sdk", group="sahinler-circle", page=P_CIRCLE, brand="sahinler",
         name="SDK 6 · SDK 8 circular sheet cutting and flanging machines",
         short="SDK 6 · SDK 8",
         models_label="SDK 6 (Ø12.5 ft) · SDK 8 (Ø15 ft)",
         summary="Tank-head machines that cut a circle from plate and flange its edge on the same head: dished and flat heads from "
                 "Ø21.7″ up to Ø12.5 ft (SDK 6) or Ø15 ft (SDK 8) in mild steel to 1/4″ – 5/16″ and stainless to 8 ga – 3/16″. The "
                 "flanging rolls are driven through planetary gearboxes by electric motor (SDK 6) or hydromotor (SDK 8), the part "
                 "carrier has two speeds and hydraulic up/down adjustment, hydraulic lateral supports hold the plate and an LCD "
                 "touchscreen runs the cycle. One set of R1″ flanging rolls and one set of cutting blades are included; a Japanese-hat "
                 "(top-hat) attachment, small-diameter attachment and stainless blade set are optional.",
         features=["Cut and flange dished and flat heads up to Ø15 ft on the same head", "Bottom and top flanging rolls driven by hydromotor (SDK 8) or electric motor (SDK 6) through planetary gearbox",
                   "Two-speed part carrier, hydraulic up/down; hydraulic-cylinder lateral supports", "LCD touchscreen operator panel", "One set of flanging rolls (R1″) and one set of cutting blades included"],
         optional=["Flanging rolls in other radii", "Japanese-hat (top-hat) attachment", "Small-Ø cutting / flanging attachment (Ø15.7″ – 17.7″)", "Blade set for cutting stainless steel", VOLT],
         images=["sh-sdk8", "sh-sdk6", "sh-sdk6-b", "sh-sdk8-head", "sh-sdk-rolls", "sh-sdk-control", "sh-sdk8-lcd"],
         videos=vids(("RgQYKfC1lDU", "SDK 8 tank head flanging and circle cutting machine"), ("s5NHZ7ylf80", "SDK 8 tank dish end circular cutting and flanging machine"), ("rFdDnjtZ5zs", "SDK 6 circular cutting shear and flanging machine"), ("3_6at2kbAGo", "SDK 8 — conical flanging of a tank head")),
         specs=simple_spec([generic_table(47, 0, "SDK 6 · SDK 8", "circular sheet cutting & flanging machines", SDK_SPEC)], ["max_dia", "thickness", "motor", "weight"], ["Max. flanging plate Ø", "Max. plate thickness — mild steel", "Motor power", "Weight"], NOTE_SDK),
         headline="Heads Ø21.7″ to Ø15 ft (0.55 – 4.5 m) · plate to 5/16″ (8 mm) · cut and flange on one head"),
    dict(id="sahinler-efm", group="sahinler-circle", page=P_CIRCLE, brand="sahinler",
         name="EFM 6 elliptical cutting and flanging machine",
         short="EFM 6",
         models_label="EFM 6 · Ø29.5″ to Ø118″",
         summary="For round and elliptical tank heads: the flanging head tilts 90° to both sides and follows a moving, changeable bottom "
                 "template, so flat, crowned and elliptical bottoms are cut and flanged on the same head. Plate from 11 ga to 1/4″ "
                 "mild steel (14 ga to 8 ga stainless) up to Ø118″; one set of R3/8″ flanging rolls, one set of cutting blades and one "
                 "copy template are included, with a vacuum system optional for holding thin heads.",
         features=["Flanging head tilts 90° to both sides for elliptical flanging", "Moving, changeable bottom template for flat and elliptical sheets; copy template (1 pc.)",
                   "Round and elliptical flanging and cutting on the same head; flanges flat, crowned and elliptical bottoms", "Planetary gearbox and gear system drive",
                   "One set of flanging rolls (R3/8″) and one set of cutting blades included"],
         optional=["Vacuum system", VOLT],
         images=["sh-efm6", "sh-efm-vacuum"],
         videos=vids(("UDAOTlZ0Is8", "EFM 6 oval tank head shear cutting and flanging machine"), ("g-YYZHvy-1g", "EFM 6 tank dish elliptical cutting and flanging machine"), ("KfXlPsGZF10", "EFM 6 elliptical tank head cutting shear and flanging machine")),
         specs=simple_spec([generic_table(48, 0, "EFM 6", "elliptical cutting & flanging machine", EFM_SPEC)], ["max_dia", "thickness", "motor", "weight"], ["Max. plate cutting Ø", "Plate thickness — mild steel", "Motor power", "Weight"], NOTE_SDK),
         headline="Round and elliptical heads Ø29.5″ to Ø118″ (0.75 – 3 m) · plate 11 ga to 1/4″"),
]

# ------------------------------------------------------------------ corner notchers
HNM_SPEC = [("Cutting capacity — steel", "Cutting capacity — mild steel", "", lambda c: c.replace("⁄", "/"), True), ("Cutting capacity — stainless", "Cutting capacity — stainless steel", "", lambda c: c, True),
            ("Cutting angle", "Cutting angle", "", lambda c: c.replace("90 fixed", "90° fixed").replace("30 – 140 variable", "30° – 140° variable"), True),
            ("Table size", "Table size", "", dims, False), ("Blade length", "Blade length", "", dims, False), ("Max. cuts per minute", "Max. cuts per minute", "", None, False),
            ("Max. working pressure", "Max. working pressure", "", psi, False), ("Oil tank", "Oil tank", "", litres, False), S_MOTOR, S_DIMS, S_WT]
NOTCH_FAMILIES = [
    dict(id="sahinler-hnm-fixed", group="sahinler-notch", page=P_NOTCH, brand="sahinler",
         name="HNM 4F · HNM 6F fixed-angle hydraulic corner notchers",
         short="HNM 4F · 6F",
         models_label="HNM 4F (3/16″) · HNM 6F (1/4″) · fixed 90°",
         summary="Compact hydraulic notchers that cut a 90° corner out of sheet in one stroke — the box, pan and enclosure corner before "
                 "it goes to the press brake. Fixed 90° angle with high notching speed (20 – 25 cuts per minute), foot-pedal control "
                 "and a small footprint: the HNM 4F cuts 3/16″ mild steel or 14 ga stainless on a 7.8″ blade, the HNM 6F 1/4″ mild "
                 "steel or 11 ga stainless on a 9.8″ blade.",
         features=["Fixed 90° notching angle with high notching speed — 20 / 25 cuts per minute", "Compact structure, small footprint and convenient operation",
                   "Foot-pedal control", "HNM 4F: 3/16″ mild steel · 7.8 × 7.8″ blades; HNM 6F: 1/4″ mild steel · 9.8 × 9.8″ blades"],
         optional=[VOLT],
         images=["sh-hnm6f"],
         videos=vids(("LuQHD5rFh3A", "HNM-6 1/4″ corner notcher"), ("ADZj0MzeK7w", "HNM 4 hydraulic corner notcher")),
         specs=simple_spec([generic_table(56, 0, "HNM", "hydraulic corner notchers", HNM_SPEC)], ["capacity", "angle", "blade", "motor", "weight"], ["Cutting capacity — mild steel", "Cutting angle", "Blade length", "Motor power", "Weight"], NOTE_SIMPLE),
         headline="3/16″ and 1/4″ mild steel · fixed 90° · 7.8″ and 9.8″ blades · 20 – 25 cuts/min"),
    dict(id="sahinler-hnm-variable", group="sahinler-notch", page=P_NOTCH, brand="sahinler",
         name="HNM 6V variable-angle hydraulic corner notcher",
         short="HNM 6V variable angle",
         models_label="HNM 6V · 30° – 140° · 1/4″",
         summary="A variable-angle notcher on a statically and dynamically rigid steel table and top beam: the blades swing from 30° to "
                 "140° for V-notches, hoppers, cones and ducting corners, and the blade gap adjusts automatically so no realignment is "
                 "needed between sheet thicknesses. Four hydraulic hold-down cylinders give repeatable cuts up to 1/4″ mild steel (11 ga "
                 "stainless) at 30 cuts per minute, with a T-slot top table for precise, repeatable positioning and foot-pedal control.",
         features=["Variable notching angle 30° – 140°", "Strong frame with statically and dynamically rigid steel table and top beam; T-slot top table for precise cuts",
                   "Automatic blade-gap adjustment — no realignment for different sheet thicknesses", "4 hydraulic hold-down cylinders for repeatable cutting; foot-pedal control; max. 1/4″ cutting capacity"],
         optional=["Punching attachment (HNM 6 VP: notching and punching on one machine)", VOLT],
         images=["sh-hnm6v"],
         videos=vids(("JVWQf5gMtfY", "HNM-6A 1/4″ variable-angle corner notcher and punching machine"), ("nwNGB5PgXoo", "HNM 6 VP variable-angle corner notcher + punch"), ("m2QTUJ1ovq0", "2-in-1 corner notcher and punch (variable angle): HNM 6 VP")),
         specs={"kind": "table", "tables": [], "models": [{"name": "HNM 6V", "glance": ["1/4″ – 8 ga", "30° – 140° variable", dims("7.9 × 7.9"), motor("5.4"), weight("2,535")]}], "glance_keys": ["capacity", "angle", "blade", "motor", "weight"], "caps": {}, "note": "Specifications in the HNM table above."},
         headline="1/4″ mild steel · 30° – 140° variable angle · 4 hydraulic hold-downs · 30 cuts/min"),
]

# ------------------------------------------------------------------ BT 114-S pipe polisher
POLISH_FAMILIES = [
    dict(id="sahinler-bt-114-s", group="sahinler-polish", page=P_POLISH, brand="sahinler",
         name="BT 114-S automatic pipe polishing and sanding machine",
         short="BT 114-S",
         models_label="BT 114-S · Ø3/8″ to Ø4-1/2″ · 6.4 HP",
         summary="A belt sander for round pipe and square tube that feeds the material itself: an automatic pipe feeder with its own "
                 "motor pushes straight or bent tube (up to a 45° bend) through two 37 × 2″ abrasive belts, so the operator does not "
                 "turn or hold the material. Feeding speed and belt speed are both inverter-variable, the belt is changed through an "
                 "opening cover and a holder is provided for manual feeding. Finishing, satin-brushing and rust removal on Ø3/8″ to "
                 "Ø4-1/2″ — handrail, furniture and architectural stainless.",
         features=["Automatic pipe feeder with separate motor — delivers material without operator intervention; no need to turn the material",
                   "Pipe / tube Ø3/8″ – Ø4-1/2″ (10 – 114 mm); polishes bent pipe and tube up to a 45° bend", "Variable feeding speed and variable sanding-belt speed by inverter drive",
                   "2 abrasive belts 37 × 2″ included; opening cover for belt changes and cleaning", "Manual pipe-clamping adjustment; fixing attachment for the motor; holder for manual feeding"],
         optional=["Abrasive belts in other grits", VOLT],
         images=["sh-bt114s-photo", "sh-bt114s", "sh-bt114s-showroom", "sh-bt114s-head", "sh-bt114s-front", "sh-bt114s-top", "sh-bt114s-belt", "sh-bt114s-square", "sh-bt114s-rolls", "sh-bt114s-wheel", "sh-bt114s-belt-2", "sh-bt114s-pendant", "sh-bt114s-rail", "sh-bt114s-tube"],
         videos=vids(("j8vE5Dmc4QI", "BT 114-S pipe sander — pipe polishing machine"), ("zd5Zhu82wPo", "BT 114-S square tube sanding and polishing machine"), ("kotI1chSYnY", "Curved pipe polishing on the BT 114-S"), ("6SVmTnY_4rs", "BT 114-S — diameter adjustment"), ("o23ZQEoAvzU", "BT 114-S automatic pipe sander with feeder")),
         specs=simple_spec([{"title": "BT 114-S", "sub": "automatic pipe polishing & sanding machine", "models": ["BT 114-S"], "rows": [
             {"label": "Working capacity", "sub": "pipe / tube OD", "cells": ["Ø3/8″ – Ø4-1/2″ (10 – 114 mm)"], "key": True},
             {"label": "Abrasive-belt motors", "sub": "", "cells": [motor("4.0 + 2.0")], "key": False},
             {"label": "Feed-wheel motor", "sub": "", "cells": [motor("0.3")], "key": False},
             {"label": "Total motor power", "sub": "", "cells": ["6.4 HP (4.75 kW)"], "key": False},
             {"label": "Belt size", "sub": "2 belts included", "cells": ["37 × 2″ (940 × 50 mm)"], "key": False},
             {"label": "Feeding speed", "sub": "variable, inverter drive", "cells": [speed("9.8 – 72")], "key": False},
             {"label": "Sanding-belt speed", "sub": "", "cells": ["Variable, inverter drive"], "key": False},
             {"label": "Automatic pipe feeder", "sub": "", "cells": ["Standard"], "key": False},
             {"label": "Dimensions L × W × H", "sub": "", "cells": [dims("39 × 30 × 59")], "key": False},
             {"label": "Weight", "sub": "approx.", "cells": [weight("617")], "key": False}]}],
             ["capacity", "belt", "motor", "weight"], ["Working capacity", "Belt size", "Total motor power", "Weight"], NOTE_SIMPLE),
         headline="Pipe and tube Ø3/8″ to Ø4-1/2″ (10 – 114 mm) · automatic feeder · 2 belts 37 × 2″"),
]

ALL = ANGLE_FAMILIES + SPB_FAMILIES + IRON_FAMILIES + PUNCH_FAMILIES + PRESS_FAMILIES + CIRCLE_FAMILIES + NOTCH_FAMILIES + POLISH_FAMILIES
