#!/usr/bin/env python3
"""Tubend (Bursa, Turkey) — sold under its own brand, three product groups only (Oct 2026 brief):

  * HP 10 – HP 150 NC hydraulic horizontal presses → horizontal-press-brake.html (the old site's URL, kept: it ranks for
    "horizontal press brake" and "horizontal hydraulic press"), written by tools/tubend_pages.py;
  * WP 100 / WP 300 welding positioners → welding-positioners.html (new section), tools/tubend_pages.py;
  * TB 34 / TB 42 mandrel-less pipe benders → a group on rotary-draw-tube-benders.html under the pipe-benders hub, written by
    tools/isitan_tube_benders.py.

No other Tubend products (MHB, roller conveyors, PK / HPK section benders, SPB, TT notchers, BP polisher, AC / DK saws).
Metric data from the Tubend General Catalogue 2026 (July 2026) and tubend.com.tr; imperial as in NovoTech's own Tubend
brochure (NovoTech_Tubend_Presses_Benders_2026.pdf), widths and thicknesses to the nearest 1/16″.  HP 60: the catalogue gives
50 t (300 × 16 mm — the same width as the HP 80 at 16 instead of 20 mm), tubend.com.tr 60 t; the catalogue figure is used.
"""
BRAND = "tubend"
P_HP, P_WP = "horizontal-press-brake", "welding-positioners"
P_TB = "rotary-draw-tube-benders"          # isitan_tube_benders.P_BK


def vids(*ids_titles):
    from sahinler_lib import vids as _vids      # NovoTech's own channel only
    return _vids(*ids_titles)


def usT(t):
    return f"{round(t * 1.1023):,} US ton ({t:g} t)"


def mm_in(mm, nd=1):
    return f"{mm / 25.4:,.{nd}f}″ ({mm:,} mm)"


def hp(kw, txt=None):
    return f"{txt or f'{kw * 1.341:.1f}'.rstrip('0').rstrip('.')} HP ({kw:g} kW)"


def lb(kg):
    return f"{round(kg * 2.20462):,} lb ({kg:,} kg)"


def dims(l, w, h):
    return f"{l / 25.4:.0f} × {w / 25.4:.0f} × {h / 25.4:.0f}″ ({l:,} × {w:,} × {h:,} mm)"


def row(label, cells, key=False, sub=""):
    return {"label": label, "sub": sub, "cells": cells, "key": key}


VOLT = "CSA-approved electrical panel; 600 V 3-phase with transformer (208 / 240 / 480 V on request)"
VOLT_OPT = "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"

# ------------------------------------------------------------------------------------------------ HP 10 – HP 100
HP_MODELS = ["HP 10", "HP 20", "HP 40", "HP 60", "HP 80", "HP 100"]
HP_T = [10, 20, 40, 50, 80, 100]
HP_FLAT = ["5-7/8″ × 1/4″ (150 × 6 mm)", "7-7/8″ × 3/8″ (200 × 10 mm)", "9-7/8″ × 5/8″ (250 × 16 mm)", "11-13/16″ × 5/8″ (300 × 16 mm)",
           "11-13/16″ × 13/16″ (300 × 20 mm)", "11-13/16″ × 15/16″ (300 × 24 mm)"]
HP_STROKE = [200, 200, 300, 300, 300, 300]
HP_TOOL = [150, 200, 250, 300, 300, 300]
HP_KW = [(1.1, "1.5"), (2.2, "3"), (4, "5.4"), (5.5, "7.4"), (7.5, "10"), (11, "15")]
HP_KG = [400, 640, 1000, 1700, 2100, 2450]
HP_DIM = [(900, 450, 1160), (1200, 550, 1230), (1300, 600, 1300), (1300, 600, 1400), (1600, 850, 1600), (1600, 850, 1700)]
T_HP = {"title": "HP 10 – HP 100", "sub": "NC hydraulic horizontal presses", "models": HP_MODELS, "rows": [
    row("Max. force", [usT(t) for t in HP_T], True, "at 2,900 psi (200 bar)"),
    row("Flat bar bending capacity", HP_FLAT, True, "width × thickness, mild steel"),
    row("Maximum stroke", [mm_in(s) for s in HP_STROKE], True),
    row("Tool height", [mm_in(s) for s in HP_TOOL]),
    row("Working / return speed", ["0.39 in/s (10 mm/s)"] * 6),
    row("Motor power", [hp(k, t) for k, t in HP_KW], True),
    row("Dimensions L × W × H", [dims(*d) for d in HP_DIM]),
    row("Weight", [lb(k) for k in HP_KG], True)]}

HPH_MODELS = ["HP 120", "HP 150"]
T_HPH = {"title": "HP 120 · HP 150", "sub": "Heavy-duty horizontal presses with T-slot table and support columns", "models": HPH_MODELS, "rows": [
    row("Max. force", [usT(120), usT(150)], True, "at 3,340 psi (230 bar)"),
    row("Flat bar bending capacity", ["19-11/16″ × 1-3/16″ (500 × 30 mm)", "19-11/16″ × 1-9/16″ (500 × 40 mm)"], True, "width × thickness, mild steel"),
    row("Maximum piston stroke", [mm_in(500)] * 2, True),
    row("Tool height", [mm_in(500)] * 2),
    row("Support column diameter", ["Ø5-1/8″ (130 mm)", "Ø5-7/8″ (150 mm)"]),
    row("Working / return speed", ["0.39 in/s (10 mm/s)"] * 2),
    row("Motor power", [hp(5.5, "7.4"), hp(7.5, "10")], True),
    row("Dimensions L × W × H", [dims(2760, 1750, 1275), dims(2960, 1750, 1475)]),
    row("Weight", [lb(3600), lb(4300)], True)]}

HP_GK = ["force", "capacity", "stroke", "motor", "weight"]
HP_NOTE = ("Bending capacity is flat bar bent the hard way in mild steel with the standard V tooling; force is at the pressure "
           "given. Metric values in brackets are the manufacturer's figures; dimensions L × W × H, weight net.")


def glance_from(t, labels):
    rr = {r["label"]: r["cells"] for r in t["rows"]}
    return [{"name": m, "glance": [rr[l][i] if l else "—" for l in labels]} for i, m in enumerate(t["models"])]


def spec(tables, labels, gk, note):
    models = [m for t in tables for m in glance_from(t, labels)]
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": gk, "caps": {}, "note": note}


HP_LABELS = ["Max. force", "Flat bar bending capacity", "Maximum stroke", "Motor power", "Weight"]
HPH_LABELS = ["Max. force", "Flat bar bending capacity", "Maximum piston stroke", "Motor power", "Weight"]

TOOLS_BEND = ["Radius punch with V-die", "Press brake punch with multi-V die", "Bolt punch with multi-V die", "Narrow V-die",
              "Two-sided V-bending tool", "Spring-loaded U-bending tool", "Mandrel-less pipe bending tool", "Solid bar and thick-wall pipe bending tool",
              "Pipe end reduction and expansion tool", "Profile bending tool", "Round bar bending tool", "Pipe clamping tool"]
TOOLS_CUT = ["Pipe notching tool", "Wide-radius bending tool", "Straightening tool", "Punching tool", "Shearing tool",
             "Busbar shearing, punching, precision, vertical and Z-bending, corner notching and twisting tools"]

# ------------------------------------------------------------------------------------------------ TB 34 / TB 42
T_TB34 = {"title": "TB 34", "sub": "Electric mandrel-less pipe and tube bender", "models": ["TB 34"], "rows": [
    row("Max. bending capacity", ["1″ NPS pipe · Ø1-5/16″ × 11 ga (Ø34 × 3 mm)"], True, "OD × wall, to 180°"),
    row("Min. bending radius", ["3 × tube Ø"], True, "centreline"),
    row("Control", ["Digital angle readout with angle limit · brake motor"], True),
    row("Output speed", ["1.9 rpm"]),
    row("Motor power", [hp(0.55, "0.7")]),
    row("Dimensions L × W × H", [dims(720, 260, 460)]),
    row("Weight", [lb(90)], True)]}
T_TB42 = {"title": "TB 42", "sub": "Hydraulic mandrel-less pipe and tube bender", "models": ["TB 42"], "rows": [
    row("Max. bending capacity", ["1-1/4″ NPS pipe · Ø1-5/8″ × 11 ga (Ø42 × 3 mm)"], True, "OD × wall"),
    row("Max. force", [usT(15)], False, "at 2,900 psi (200 bar)"),
    row("Control", ["Digital readout · manual angle switch · adjustable speed"], True),
    row("Maximum stroke", [mm_in(150)]),
    row("Working speed", ["0.79 in/s (20 mm/s)"]),
    row("Oil tank", ["4 US gal (15 L)"]),
    row("Motor power", [hp(1.1, "1.5")]),
    row("Dimensions L × W × H", [dims(450, 1000, 1000)]),
    row("Weight", [lb(220)], True)]}
TB_GK = ["capacity", "min_radius", "working_length", "control", "weight"]  # the hub's CLR column is the largest radius, so the minimum stays off it
TB_NOTE = "Capacity is mild steel pipe or tube with the matching die set; one die set in the size you order is included."

# ------------------------------------------------------------------------------------------------ WP 100 / WP 300
T_WP = {"title": "WP 100 · WP 300", "sub": "Tilting welding positioners", "models": ["WP 100", "WP 300"], "rows": [
    row("Nominal load capacity", [lb(100), lb(300)], True, "table horizontal"),
    row("Load capacity, table tilted", [lb(50), lb(150)], False, "table vertical"),
    row("Table diameter", ["Ø13-3/4″ (350 mm)", "Ø18-7/8″ (480 mm)"], True),
    row("Table rotation", ["360° · 1 – 5.5 rpm, variable"] * 2, True),
    row("Tilt", ["120°, right – left", "90°, right – left"], True),
    row("Turntable motor", [hp(0.25, "0.33"), hp(0.37, "0.5")]),
    row("Power supply", ["220 V 1-phase"] * 2),
    row("T-slots", ["M10 × 12"] * 2),
    row("Dimensions L × W × H", [dims(550, 650, 370), dims(640, 740, 550)]),
    row("Weight", [lb(45), lb(95)], True)]}
WP_GK = ["capacity", "table", "rotation", "tilt", "weight"]
WP_LABELS = ["Nominal load capacity", "Table diameter", "Table rotation", "Tilt", "Weight"]
WP_NOTE = ("Nominal load is a centred part on the horizontal table; with the table tilted the WP 100 carries 110 lb and the WP 300 331 lb. "
           "Metric values in brackets are the manufacturer's figures.")

FAMILIES = [
    # -------------------------------------------------------------------------------------------- horizontal presses
    dict(id="tubend-hp", group="tubend-hp", page=P_HP, brand=BRAND,
         name="HP 10 – HP 100 NC hydraulic horizontal presses, 11 – 110 US ton",
         short="HP 10 – HP 100",
         models_label="HP 10 · HP 20 · HP 40 · HP 60 · HP 80 · HP 100 · 6 models",
         summary="A horizontal press brake lays the press on its side: a hydraulic ram pushes the tool across a heavy steel table "
                 "at bench height, so flat bar, angle, pipe, solid bar and busbar are bent, punched, sheared or straightened "
                 "with the part lying flat in front of the operator. Tubend's HP series runs from the 11-ton HP 10 for 5-7/8″ × 1/4″ "
                 "flat bar to the 110-ton HP 100 for 11-13/16″ × 15/16″, every model with an NC touch-screen on a control stand — "
                 "manual, automatic and recipe modes — a foot pedal, induction-hardened support pins and an ergonomic tool table "
                 "for quick tool changes.",
         headline="11 – 110 US ton · flat bar to 11-13/16″ × 15/16″ · NC touch-screen with recipes",
         features=["NC control stand with touch-screen: manual mode between set limits, automatic serial modes and recipe mode for multi-step parts",
                   "Hydraulic speed and pressure adjustment; ram stroke 7.9″ (HP 10, HP 20) or 11.8″ (HP 40 – HP 100)",
                   "Ergonomic tool table at bench height; easy tool change; induction-hardened support pins",
                   "Easily adjustable back stop; foot pedal", VOLT],
         optional=["Automatic back gauge — servo-driven NC with pull-back, 3.3, 6.6 or 9.8 ft (1, 2 or 3 m) long, for series parts",
                   "Bending tools: " + ", ".join(TOOLS_BEND[:6]).lower().capitalize(),
                   "Pipe and bar tools: " + ", ".join(TOOLS_BEND[6:]).lower(),
                   "Notching, punching, shearing and straightening tools; busbar shearing, punching, bending and twisting tools",
                   "Custom dies made to your part", VOLT_OPT],
         images=["tb-hp10", "tb-hp80", "tb-hp-backgauge", "tb-hp-screen-manual", "tb-hp-screen-recipe", "tb-hp-tool-vdie", "tb-hp-tool-pipe",
                 "tb-hp-tool-pipe-end", "tb-hp-tool-radius", "tb-hp-tool-busbar", "tb-hp-parts", "tb-hp-busbar-parts"],
         videos=vids(("pxJvddrvYeg", "HP 40 NC horizontal press — instruction"), ("D9CKQFKn78E", "HP multi-function horizontal press brake with NC control"),
                     ("njyMkBwLGQk", "HP horizontal press — straightening tool"), ("RgLqznLX8QI", "HP 10 horizontal press brake, 11 US ton")),
         specs=spec([T_HP], HP_LABELS, HP_GK, HP_NOTE)),
    dict(id="tubend-hp-heavy", group="tubend-hp", page=P_HP, brand=BRAND,
         name="HP 120 · HP 150 heavy-duty horizontal presses, 132 – 165 US ton",
         short="HP 120 · HP 150",
         models_label="HP 120 · HP 150 · 2 models",
         summary="The heavy horizontal presses for straightening and bending big sections: 132 and 165 US tons on a 19.7″ stroke, "
                 "hardened Ø5-1/8″ and Ø5-7/8″ support columns between which shafts, beams and heavy bar are straightened, a "
                 "T-slot clamping table with heat-treated support holes for tools and attachments, and an upper brace that keeps "
                 "the frame from flexing. 19-11/16″ × 1-9/16″ flat bar on the HP 150; NC control stand and foot pedal as on the "
                 "HP series, and dies designed and made for the job.",
         headline="132 – 165 US ton · 19.7″ stroke · flat bar to 19-11/16″ × 1-9/16″ · T-slot table",
         features=["NC control unit with control stand and foot pedal; hydraulic speed and pressure adjustment",
                   "Hardened support columns, Ø5-1/8″ (HP 120) and Ø5-7/8″ (HP 150), for straightening between columns",
                   "Multiple heat-treated support holes for straightening and for mounting tools and attachments",
                   "T-slot clamping table for securing tools and dies; upper support brace prevents flexing",
                   "Robust steel body; high-profile ergonomic design for large and long workpieces", VOLT],
         optional=["Custom die design and manufacturing for the job", "Special requests and revisions on request", VOLT_OPT],
         images=["tb-hp120", "tb-hp120-side", "tb-hp120-straighten"],
         videos=[],
         specs=spec([T_HPH], HPH_LABELS, HP_GK, HP_NOTE)),
    # -------------------------------------------------------------------------------------------- mandrel-less pipe benders
    dict(id="tubend-tb34", group="tubend-tb", page=P_TB, brand=BRAND,
         name="TB 34 electric mandrel-less pipe bender, 1″ NPS pipe",
         short="TB 34",
         models_label="TB 34 · 1 model",
         summary="A bench-size electric pipe bender for 1″ NPS pipe and Ø1-5/16″ × 11 ga tube to 180°: a gear-reduced drive turns "
                 "the bend die at 1.9 rpm, a digital readout shows the angle and stops the bend where you set it, and a brake motor "
                 "holds the angle so spring-back does not creep into the part. 198 lb with detachable carrying handles — it goes to "
                 "the work — and one die set in your pipe size is included. Street furniture, bike racks, safety barriers and "
                 "handrail parts.",
         headline="1″ NPS pipe · Ø1-5/16″ × 11 ga to 180° · digital angle readout · 198 lb",
         features=["Bends pipe and tube to Ø1-5/16″ × 11 ga (Ø34 × 3 mm) — 1″ NPS — up to 180°, minimum radius 3 × tube Ø",
                   "Digital readout; the bend angle can be limited from the readout for repeat parts",
                   "Gearbox-driven power transmission; brake motor prevents bending errors from spring-back",
                   "Durable steel body; detachable carrying handles for moving it around the shop",
                   "1 set of pipe bending dies included", VOLT],
         optional=["Pipe dies in custom sizes", VOLT_OPT],
         images=["tb-tb34", "tb-tb34-parts", "tb-tb34-barrier"],
         videos=[],
         specs=spec([T_TB34], ["Max. bending capacity", "Min. bending radius", None, "Control", "Weight"], TB_GK, TB_NOTE)),
    dict(id="tubend-tb42", group="tubend-tb", page=P_TB, brand=BRAND,
         name="TB 42 hydraulic mandrel-less pipe bender, 1-1/4″ NPS pipe",
         short="TB 42",
         models_label="TB 42 · 1 model",
         summary="A 17-ton hydraulic pipe bender in a closed steel cabinet: the cylinder pushes the former through the pipe or tube "
                 "between two wing dies on the top plate, a manual angle switch and digital readout set the bend, and the speed is "
                 "adjustable. 1-1/4″ NPS pipe and Ø1-5/8″ × 11 ga tube; free holes in the plate take special dies for section, flat "
                 "and solid bar. One set of pipe bending dies included, 485 lb.",
         headline="17 US ton hydraulic · 1-1/4″ NPS pipe · Ø1-5/8″ × 11 ga · digital readout",
         features=["Tube bending capacity to Ø1-5/8″ × 11 ga (Ø42 × 3 mm) — 1-1/4″ NPS pipe", "17 US ton (15 t) hydraulic cylinder, 5.9″ stroke, adjustable speed",
                   "Manual adjustable angle switch with digital readout", "Free holes in the top plate for special tools; steel welded frame",
                   "One set of pipe bending dies included", VOLT],
         optional=["Sets of pipe, tube, section or solid bar dies to the required size", VOLT_OPT],
         images=["tb-tb42", "tb-tb42-part", "tb-tb42-dies", "tb-tb42-panel"],
         videos=[],
         specs=spec([T_TB42], ["Max. bending capacity", None, None, "Control", "Weight"], TB_GK, TB_NOTE)),
    # -------------------------------------------------------------------------------------------- welding positioners
    dict(id="tubend-wp", group="tubend-wp", page=P_WP, brand=BRAND,
         name="WP 100 · WP 300 tilting welding positioners, 220 – 661 lb",
         short="WP 100 · WP 300",
         models_label="WP 100 · WP 300 · 2 models",
         summary="A welding positioner turns the part under the torch, so a round weld is laid in one continuous pass in the flat "
                 "position instead of being stopped and restarted around the part. Tubend's WP 100 carries 220 lb on a Ø13-3/4″ "
                 "table that tilts 120°; the WP 300 carries 661 lb on a Ø18-7/8″ table that tilts 90°. The table turns 360° at 1 to "
                 "5.5 rpm, set on the control box and run from the standard foot pedal; T-slots take clamps and fixtures, and a "
                 "Ø6-1/4″ or Ø7-7/8″ lathe chuck or a custom fixture plate (WP 300) is available. Single-phase 220 V.",
         headline="220 – 661 lb · 360° at 1 – 5.5 rpm · 90 – 120° tilt · foot pedal",
         features=["Adjustable tilt angle for easy positioning of the part — 120° (WP 100) or 90° (WP 300), right or left",
                   "Adjustable turning speed, 1 – 5.5 rpm, for a steady travel speed under the torch", "Standard foot pedal; control box with speed and direction",
                   "T-slotted turntable (M10) for clamps and fixtures", "Runs on single-phase 220 V"],
         optional=["Ø6-1/4″ (160 mm) or Ø7-7/8″ (200 mm) 3-jaw lathe chuck", "Custom work plate for welding fixtures (WP 300)"],
         volt_note="Single-phase 220 V supply — no three-phase power needed.",
         images=["tb-wp300", "tb-wp100", "tb-wp300-plate"],
         videos=[],
         specs=spec([T_WP], WP_LABELS, WP_GK, WP_NOTE)),
]


def families(page=None):
    return [f for f in FAMILIES if page is None or f["page"] == page]
