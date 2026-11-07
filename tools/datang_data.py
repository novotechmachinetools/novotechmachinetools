#!/usr/bin/env python3
"""Welding positioners, turning rolls and column & boom manipulators of the NovoTech value line, built in China by Wuxi Datang
(the owner, Nov 7 2026: only these three kinds; the maker's name stays off the site).  Figures from the maker's product pages
(wuxidatang.com, read Nov 7 2026 — the owner found them more exact than the brochure), every row of every table, imperial
first with the maker's metric value in brackets; where the maker lists two motors for one model (HBJ20, HBT50, HBT100, DSK60,
DSK80) both are given in one column.  Photos: tools/datang_photos.py.

The welding automation pages (tools/welding_pages.py) merge these families with the positioners, turning rolls, stands and
tables already on the site.
"""
from ttmc_conv import KG, KW, auto_spec, dec, num, table

BRAND = "novotech"
P_POS, P_ROLL, P_CAB = "welding-positioners", "welding-turning-rolls", "column-and-boom-welding-manipulators"
NOTE = ("Metric values in brackets are the manufacturer's figures. Loads are the rated load of the machine (per set of drive and "
        "idler sections on turning rolls). Motors are three-phase, rotation speed set by variable-frequency drive (VFD) unless noted.")
NOTE_ORDER = ("Built to order: load, size and height are designed for the part — send us a drawing or photo of the work, its "
              "weight and the welds.")


# ------------------------------------------------------------------------------------------------ helpers
def D(mm):
    """a diameter in decimal inches: Ø23.6″ (600 mm)"""
    return f"Ø{dec(mm)} ({mm:,} mm)"


def DR(a, b):
    """a diameter range: Ø9.8 – 90.6″ (250 – 2,300 mm)"""
    return f"Ø{num(a / 25.4, 1)} – {dec(b)} ({a:,} – {b:,} mm)"


def T(t):
    """metric tons → lb (kg)"""
    return KG(t * 1000)


def KW2(kw):
    """two motors: 2 × 1/4 HP (2 × 0.18 kW)"""
    return f"2 × {KW(kw).split(' (')[0]} (2 × {kw:g} kW)"


def WIDTH(w, n=1):
    return f"{dec(w)} ({w:,} mm)" if n == 1 else f"2 × {dec(w)} (2 × {w:,} mm)"


def FTM(m):
    """a travel speed in ft/min to one decimal: 3.3 ft/min (1 m/min)"""
    return f"{num(m * 3.2808, 1)} ft/min ({m:g} m/min)"


def MH():
    """the turning rolls' linear (surface) speed, 6 – 60 m/h"""
    return "3.9 – 39.4 in/min (6 – 60 m/h)"


def F(fid, page, group, name, short, tables, summary, features, images, headline, cap=None, note=NOTE, optional=(), models_label=None):
    models = [m for t in tables for m in t["models"]]
    label = models_label or ((" · ".join(models) if len(models) <= 3 else f"{models[0]} – {models[-1]}") + f" · {len(models)} model{'s' if len(models) > 1 else ''}")
    return dict(id=fid, page=page, group=group, brand=BRAND, name=name, short=short, models_label=label, summary=summary,
                features=list(features), optional=list(optional), images=list(images), videos=[], headline=headline,
                specs=auto_spec(tables, note, cap=cap), manual=False, no_pdf=True)


# ================================================================================================ positioners
T_HB_LIGHT = table("HB01 · HB05 · HB1", "Light welding positioners, 22 – 220 lb", ["HB01", "HB05", "HB1"], [
    ("*Rated load", "KG", [10, 50, 100]),
    ("*Worktable diameter", "TXT", [D(180), D(320), D(360)]),
    ("*Tilt", "TXT", "0 – 90°"),
    ("*Rotation speed", "TXT", ["1 – 8 rpm", "1 – 15 rpm", "0.2 – 5 rpm"]),
    ("*Rotation motor", "TXT", ["15 W", "100 W", "120 W"]),
    ("Speed control", "TXT", "DC"),
])

HB = {  # model: load kg, eccentric mm, gravity mm, table Ø, tilt, rpm, rot kW, tilt rpm, tilt kW
    "HB3": (300, 100, 150, 600, "0 – 90°", "0.1 – 1", 0.18, None, None),
    "HB6": (600, 100, 200, 1000, "0 – 90°", "0.1 – 1", 0.75, 0.8, 0.75),
    "HB12": (1200, 100, 200, 1200, "0 – 120°", "0.05 – 0.5", 0.75, 0.5, 1.1),
    "HB30": (3000, 200, 300, 1400, "0 – 120°", "0.05 – 0.5", 1.5, 0.3, 2.2),
    "HB50": (5000, 200, 300, 1500, "0 – 120°", "0.05 – 0.5", 2.2, 0.14, 3.0),
    "HB100": (10000, 200, 400, 1800, "0 – 120°", "0.05 – 0.5", 3.0, 0.14, 4.0),
    "HB150": (15000, 250, 500, 2000, "0 – 120°", "0.03 – 0.3", 4.0, 0.14, 5.5),
    "HB200": (20000, 250, 600, 2200, "0 – 120°", "0.03 – 0.3", 5.5, 0.14, 7.5),
}


def hb_table(models, title, sub):
    v = [HB[m] for m in models]
    return table(title, sub, models, [
        ("*Rated load", "KG", [x[0] for x in v]),
        ("Eccentric distance, max", "centre of gravity off the table axis", "L", [x[1] for x in v]),
        ("Centre of gravity distance, max", "above the worktable", "L", [x[2] for x in v]),
        ("*Worktable diameter", "TXT", [D(x[3]) for x in v]),
        ("*Tilt", "TXT", [x[4] for x in v]),
        ("*Rotation speed", "TXT", [f"{x[5]} rpm, VFD" for x in v]),
        ("*Rotation motor", "KW", [x[6] for x in v]),
        ("Tilting speed", "constant", "TXT", [f"{x[7]:g} rpm" if x[7] else "—" for x in v]),
        ("Tilting motor", "TXT", [KW(x[8]) if x[8] else "—" for x in v]),
    ])


T_HB = hb_table(["HB3", "HB6", "HB12"], "HB3 · HB6 · HB12", "Tilting welding positioners, 661 – 2,646 lb")
T_HB_HEAVY = hb_table(["HB30", "HB50", "HB100", "HB150", "HB200"], "HB30 – HB200", "Heavy welding positioners, 6,614 – 44,092 lb")

T_HBT = table("HBT3 – HBT200", "Rotary welding tables, 661 – 44,092 lb", ["HBT3", "HBT5", "HBT10", "HBT20", "HBT30", "HBT50", "HBT100", "HBT200"], [
    ("*Rated load", "KG", [300, 500, 1000, 2000, 3000, 5000, 10000, 20000]),
    ("*Worktable diameter", "TXT", [D(x) for x in (600, 800, 1000, 1200, 1400, 1500, 1800, 2000)]),
    ("Eccentric distance, max", "centre of gravity off the table axis", "L", [100, 100, 200, 200, 200, 200, 200, 200]),
    ("*Rotation speed", "TXT", ["0.1 – 1 rpm"] * 2 + ["0.05 – 0.5 rpm"] * 6),
    ("*Rotation motor", "TXT", [KW(0.18), KW(0.37), KW(0.75), KW(0.75), KW(0.75), f"{KW(0.75)} or {KW(1.1)}", f"{KW(1.1)} or {KW(1.5)}", KW(1.5)]),
    ("Speed control", "TXT", "Rotation speed by VFD"),
    ("Power supply", "TXT", "3-phase, 600 V 60 Hz in Canada (factory standard 380 V 50 Hz; other voltages to order)"),
])

T_HBJ = table("HBJ10 – HBJ200", "Lift welding positioners, 2,205 – 44,092 lb", ["HBJ10", "HBJ20", "HBJ40", "HBJ60", "HBJ80", "HBJ100", "HBJ150", "HBJ200"], [
    ("*Rated load", "TXT", [T(t) for t in (1, 2, 4, 6, 8, 10, 15, 20)]),
    ("Eccentric distance, max", "centre of gravity off the table axis", "L", [150, 150, 150, 150, 200, 200, 200, 200]),
    ("Centre of gravity distance, max", "above the worktable", "L", [250, 300, 300, 300, 400, 400, 400, 400]),
    ("*Worktable diameter", "TXT", [D(x) for x in (900, 1200, 1400, 1500, 1600, 1800, 1800, 2000)]),
    ("*Tilt", "TXT", ["0 – 135°"] * 2 + ["0 – 120°"] * 6),
    ("*Rotation speed", "TXT", ["0.12 – 1.2 rpm"] + ["0.05 – 0.5 rpm"] * 3 + ["0.02 – 0.2 rpm"] * 4),
    ("*Rotation motor", "TXT", [KW(1.1), f"{KW(1.1)} or {KW(1.5)}", KW(1.5), KW(2.2), KW(2.2), KW(3.0), KW(3.0), KW(4.0)]),
    ("Tilting speed", "TXT", ["0.67 rpm", "0.23 rpm", "0.23 rpm", "0.14 rpm", "0.14 rpm", "0.14 rpm", "0.1 rpm", "0.1 rpm"]),
    ("Tilting motor", "TXT", [KW(1.5), f"{KW(1.5)} or {KW(2.2)}", KW(2.2), KW(3.0), KW(4.0), KW(5.5), KW(5.5), KW(7.5)]),
    ("Height adjustment", "TXT", "Manual elevating"),
])

T_HEADTAIL = table("Headstock and tailstock positioners", "Built to order",
                   ["Headstock positioner", "Head & tail lifting positioner", "Fixed head & tail positioner"], [
    ("*Type", "TXT", ["Fixed height or elevating; chuck optional on the fixed-height type",
                      "Headstock and tailstock that lift; the worktable height is lowered after rotating, for easy operation",
                      "Both fixed to the floor, or the headstock fixed and the tailstock moving on rails to suit the part length"]),
    ("*Load and height", "TXT", ["Load and centre height built to order"] * 3),
])

T_SPECIAL = table("L-type, hydraulic and special positioners", "Built to order",
                  ["L-type positioner", "Hydraulic 3-axis positioner", "Special positioner"], [
    ("*Movements", "TXT", ["Worktable tilted by motor; rotation by VFD", "Lift, rotation and tilt, all hydraulic",
                           "Designed to the customer's requirement"]),
    ("*Notes", "TXT", ["Designed for the customer's part; tilting positions the work accurately and reliably",
                       "Smaller, lighter and more compact than a motor-driven positioner of the same power",
                       "Example: positioner with a centre hole and a three-jaw welding chuck"]),
])

POSITIONERS = [
    F("dt-hb-light", P_POS, "vl-light", "HB01 · HB05 · HB1 light welding positioners, 22 – 220 lb", "HB light positioners", [T_HB_LIGHT],
      "Small tilting positioners for the bench and the cell: a worktable of Ø7.1 to 14.2″ that rotates on a DC motor with stepless speed "
      "and tilts from 0 to 90°, so flanges, small pipe spools and fittings are welded in the flat position, by hand or with a torch in a "
      "holder.",
      ["Loads 22 lb (HB01), 110 lb (HB05) and 220 lb (HB1)", "Worktables Ø7.1″, Ø12.6″ and Ø14.2″ (180 / 320 / 360 mm)",
       "Rotation 1 – 8, 1 – 15 and 0.2 – 5 rpm; DC speed control", "Tilt 0 – 90°"],
      ["dt-hb-light"], "22 – 220 lb", cap="[Rated load]"),
    F("dt-hb", P_POS, "vl-tilt", "HB3 · HB6 · HB12 tilting welding positioners, 661 – 2,646 lb", "HB tilting positioners", [T_HB],
      "Geared tilting positioners: the worktable turns at a speed set by VFD for the welding travel speed and tilts by gear sector — "
      "by motor at a constant speed on the HB6 and HB12 — to bring the joint to the flat position. Rated with the part's centre of "
      "gravity up to 3.9″ from the table axis and 5.9 – 7.9″ above the table; long parts and parts with a high centre of gravity "
      "take the next size up. Foot switch, welding chuck and wireless control are options.",
      ["661 / 1,323 / 2,646 lb (300 / 600 / 1,200 kg)", "Worktables Ø23.6″, Ø39.4″ and Ø47.2″ with T-slots",
       "Rotation 0.1 – 1 rpm (HB3, HB6) and 0.05 – 0.5 rpm (HB12), set by VFD", "Tilt 0 – 90° (HB3, HB6) and 0 – 120° (HB12); motorized tilt on the HB6 and HB12",
       "Options: single or double foot switch, welding chuck, wireless controller"],
      ["dt-hb-site", "dt-hb-2"], "661 – 2,646 lb", cap="[Rated load]",
      optional=["Foot switch, single or double pedal", "Welding chuck", "Wireless controller"]),
    F("dt-hb-heavy", P_POS, "vl-heavy", "HB30 – HB200 heavy welding positioners, 6,614 – 44,092 lb", "HB heavy positioners", [T_HB_HEAVY],
      "Heavy tilting positioners for pressure vessels, tank heads, large flanges and weldments: worktables of Ø55.1 to 86.6″ turn at "
      "0.05 – 0.5 or 0.03 – 0.3 rpm by VFD and tilt to 120° by motor through a gear sector, with the load's centre of gravity up to "
      "7.9 – 9.8″ off the axis and 11.8 – 23.6″ above the table.",
      ["6,614 – 44,092 lb (3 – 20 t)", "Worktables Ø55.1″ to Ø86.6″ (1,400 – 2,200 mm)",
       "Rotation 0.05 – 0.5 rpm (HB30 – HB100) and 0.03 – 0.3 rpm (HB150, HB200), VFD", "Motorized tilt 0 – 120°, constant speed",
       "Options: single or double foot switch, welding chuck, wireless controller"],
      ["dt-hb", "dt-hb-big"], "6,614 – 44,092 lb", cap="[Rated load]",
      optional=["Foot switch, single or double pedal", "Welding chuck", "Wireless controller"]),
    F("dt-hbt", P_POS, "vl-tables", "HBT3 – HBT200 rotary welding tables, 661 – 44,092 lb", "HBT rotary welding tables", [T_HBT],
      "A horizontal turntable for circumferential welds on parts that stand upright — tanks, drums, rings, hubs and flanges — with the "
      "rotation speed set by VFD for the welding travel speed. Eight sizes from 661 lb on a Ø23.6″ table to 44,092 lb on Ø78.7″.",
      ["661 – 44,092 lb (300 kg – 20 t)", "Worktables Ø23.6″ to Ø78.7″ (600 – 2,000 mm)", "Rotation 0.1 – 1 rpm (HBT3, HBT5), 0.05 – 0.5 rpm (HBT10 – HBT200), VFD",
       "Eccentric distance to 3.9″ (HBT3, HBT5) or 7.9″"],
      ["dt-hbt"], "661 – 44,092 lb", cap="[Rated load]"),
    F("dt-hbj", P_POS, "vl-tables", "HBJ10 – HBJ200 lift welding positioners, 2,205 – 44,092 lb", "HBJ lift positioners", [T_HBJ],
      "Positioners that tilt, rotate and adjust in height: the worktable is raised or lowered by hand to put the work at the right "
      "height for the welder or the welding head, then tilts to 120 or 135° and turns by VFD. For pressure vessels, metallurgy, power "
      "plant, chemical machinery and steel structures, with manual or automatic welding.",
      ["2,205 – 44,092 lb (1 – 20 t)", "Worktables Ø35.4″ to Ø78.7″ (900 – 2,000 mm)", "Tilt 0 – 135° (HBJ10, HBJ20) or 0 – 120°",
       "Rotation 0.12 – 1.2 rpm (HBJ10), 0.05 – 0.5 rpm (HBJ20 – HBJ60), 0.02 – 0.2 rpm (HBJ80 – HBJ200)", "Manual height adjustment"],
      ["dt-hbj"], "2,205 – 44,092 lb", cap="[Rated load]"),
    F("dt-headtail", P_POS, "vl-order", "Headstock and tailstock positioners, built to order", "Headstock & tailstock positioners", [T_HEADTAIL],
      "Positioners that turn long parts — beams, columns, frames, shafts and vessels — about their own length between a headstock and "
      "a tailstock: a headstock on its own, fixed height or elevating (chuck optional); a head and tail pair that lifts, so the work "
      "comes down to a comfortable height after turning; and a fixed pair, both units anchored to the floor or the tailstock moving on "
      "rails to suit the part length. Load and centre height are built to the part.",
      ["Headstock positioner: fixed height or elevating; chuck optional", "Head & tail lifting positioner: lowers the work after rotating",
       "Fixed head & tail positioner: both fixed, or the tailstock on rails for different lengths", "Load and centre height built to order"],
      ["dt-headstock", "dt-head-tail", "dt-head-tail-fixed"], "Built to order", cap="[Type]", note=NOTE_ORDER,
      models_label="Headstock · head & tail lifting · fixed head & tail"),
    F("dt-special-pos", P_POS, "vl-order", "L-type, hydraulic 3-axis and special welding positioners, built to order", "L-type & hydraulic positioners", [T_SPECIAL],
      "Positioners designed around the part: the L-type, whose worktable is tilted by motor and turned by VFD; the hydraulic 3-axis "
      "positioner, which lifts, rotates and tilts the work hydraulically — smaller, lighter and more compact than a motor-driven "
      "positioner of the same power; and special positioners, such as one with a centre hole and a three-jaw welding chuck.",
      ["L-type: motorized tilt, VFD rotation", "Hydraulic 3-axis: lift, rotation and tilt", "Special: centre hole, three-jaw welding chuck — or as your part needs"],
      ["dt-l-type", "dt-hydraulic", "dt-special"], "Built to order", cap="[Movements]", note=NOTE_ORDER,
      models_label="L-type · hydraulic 3-axis · special"),
]

# ================================================================================================ turning rolls
T_DZG_LIGHT = table("DZG1 · DZG3", "Light welding turning rolls, 2,205 – 6,614 lb", ["DZG1", "DZG3"], [
    ("*Rated load", "KG", [1000, 3000]),
    ("*Rotation speed", "surface speed", "TXT", ["3.1 – 43.3 in/min (80 – 1,100 mm/min)", "3.9 – 74.8 in/min (100 – 1,900 mm/min)"]),
    ("*Work diameter", "TXT", [DR(20, 800), DR(30, 1200)]),
    ("*Motor", "TXT", ["120 W, 220 V", "370 W (1/2 HP), 220 V"]),
    ("Wheels", "Ø × width", "TXT", ["Ø9.8 × 2″ (250 × 50 mm)", "Ø7.9 × 2″ (200 × 50 mm)"]),
    ("Drive roller, size", "TXT", ["19.7 × 11.8 × 15.7″ (500 × 300 × 400 mm)", "33.5 × 13 × 17.7″ (850 × 330 × 450 mm)"]),
    ("Idler roller, size", "TXT", ["19.7 × 7.9 × 15.7″ (500 × 200 × 400 mm)", "33.5 × 13 × 17.7″ (850 × 330 × 450 mm)"]),
    ("Power supply", "TXT", "AC 220 V, 50 / 60 Hz"),
    ("Set", "TXT", "1 drive roller, 1 idler roller, electrical system and foot switch"),
])

ADJ_DIA = [(150, 1800), (250, 2300), (320, 2800), (500, 3500), (600, 4200), (750, 4800), (850, 5000), (1000, 5500)]
ADJ_WHEEL = [200, 250, 300, 350, 400, 450, 500, 550]
ADJ_WIDTH = [WIDTH(80), WIDTH(140), WIDTH(170), WIDTH(200), WIDTH(200), WIDTH(180, 2), WIDTH(200, 2), WIDTH(220, 2)]


def adj_table(models, title, sub, motors):
    return table(title, sub, models, [
        ("*Rated load", "per set", "TXT", [T(t) for t in (2, 5, 10, 20, 40, 60, 80, 100)]),
        ("*Work diameter", "TXT", [DR(a, b) for a, b in ADJ_DIA]),
        ("Polyurethane wheel diameter", "TXT", [D(x) for x in ADJ_WHEEL]),
        ("Polyurethane wheel width", "TXT", ADJ_WIDTH),
        ("*Linear speed", "surface speed", "TXT", MH()),
        ("*Motor", "TXT", motors),
        ("Speed control", "TXT", "VFD"),
    ])


T_DKG = adj_table(["DKG2", "DKG5", "DKG10", "DKG20", "DKG40", "DKG60", "DKG80", "DKG100"], "DKG2 – DKG100",
                  "Bolt-adjustable welding turning rolls, 4,409 – 220,462 lb",
                  [KW2(k) for k in (0.18, 0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3.0)])
T_DSK = adj_table(["DSK2", "DSK5", "DSK10", "DSK20", "DSK40", "DSK60", "DSK80", "DSK100"], "DSK2 – DSK100",
                  "Lead-screw adjustable welding turning rolls, 4,409 – 220,462 lb",
                  [KW2(0.18), KW2(0.37), KW2(0.55), KW2(0.75), KW2(1.1), f"{KW2(1.5)} or {KW2(2.2)}", f"{KW2(2.2)} or {KW2(3.0)}", KW2(3.0)])

T_DZG = table("DZG-5 – DZG-100", "Self-aligning welding turning rolls, 11,023 – 220,462 lb",
              ["DZG-5", "DZG-10", "DZG-20", "DZG-40", "DZG-60", "DZG-80", "DZG-100"], [
    ("*Rated load", "per set", "TXT", [T(t) for t in (5, 10, 20, 40, 60, 80, 100)]),
    ("*Work diameter", "TXT", [DR(a, b) for a, b in ((250, 2300), (320, 2800), (500, 3500), (600, 4200), (750, 4800), (850, 5000), (1000, 5500))]),
    ("Polyurethane wheel diameter", "TXT", [D(x) for x in (250, 300, 350, 400, 450, 500, 500)]),
    ("Polyurethane wheel width", "TXT", [WIDTH(100), WIDTH(120), WIDTH(150), WIDTH(160), WIDTH(180), WIDTH(180, 2), WIDTH(180, 2)]),
    ("*Linear speed", "surface speed", "TXT", MH()),
    ("*Motor", "KW", [0.75, 1.1, 1.5, 3.0, 4.0, 4.0, 5.5]),
    ("Speed control", "TXT", "VFD"),
])

T_PIPE_ROT = table("Pipe and fit-up rotators", "Built to order", ["GGLJ pinch-type pipe rotator", "Hydraulic fit-up rotator"], [
    ("*Use", "TXT", ["Turns pipe around and over within an angle, for joining pipe segments and welding flanges",
                     "Brings two shell sections into line for the joint, then turns them for welding"]),
    ("*Rolls", "TXT", ["The lower roll drives; an upper roll pinches the pipe",
                       "1 drive roller, 2 idler rollers and 2 hydraulic swing-arm lifting rollers"]),
    ("*Speed", "TXT", [f"{MH()}, stepless by VFD", "From the drive roller"]),
    ("Adjustment", "TXT", ["—", "All rollers move on rails — the drive roller electrically, the others by hand — to suit the diameter; the lifting "
                                "rollers rise and fall by hydraulic pump with small left and right adjustment"]),
    ("Welding", "TXT", ["Manual and automatic welding", "—"]),
])

ROLLS = [
    F("dt-dzg-light", P_ROLL, "vl-light-rolls", "DZG1 · DZG3 light welding turning rolls, 2,205 – 6,614 lb", "DZG light turning rolls", [T_DZG_LIGHT],
      "Light turning rolls for pipe and small vessels from Ø0.8 to 47.2″: a set is one drive roller and one idler roller with the "
      "electrical system and a foot switch, running on 220 V single-phase power at a variable surface speed.",
      ["2,205 lb (DZG1) and 6,614 lb (DZG3) per set", "Work Ø0.8 – 31.5″ (DZG1) and Ø1.2 – 47.2″ (DZG3)",
       "Surface speed 3.1 – 43.3 and 3.9 – 74.8 in/min", "120 W and 370 W motors, 220 V single-phase", "Drive roller, idler roller, electrics and foot switch"],
      ["dt-dzg-light"], "2,205 – 6,614 lb", cap="[Rated load] per set"),
    F("dt-dkg", P_ROLL, "vl-adjust", "DKG2 – DKG100 bolt-adjustable welding turning rolls, 4,409 – 220,462 lb", "DKG bolt-adjustable rolls", [T_DKG],
      "Conventional turning rolls whose wheel spacing is changed by moving the wheel blocks on bolt positions along the frame, for "
      "work from Ø5.9 to 216.5″; both wheels of the drive section are driven, under AC frequency-converter control with a wide speed "
      "range. Special turning rolls are designed to the customer's requirement.",
      ["4,409 – 220,462 lb (2 – 100 t) per set", "Work Ø5.9 – 70.9″ (DKG2) to Ø39.4 – 216.5″ (DKG100)", "Polyurethane wheels Ø7.9 – 21.7″",
       "Surface speed 3.9 – 39.4 in/min (6 – 60 m/h), VFD", "Two drive motors, 2 × 1/4 HP to 2 × 4 HP"],
      ["dt-dkg", "dt-dkg-2"], "4,409 – 220,462 lb", cap="[Rated load] per set"),
    F("dt-dsk", P_ROLL, "vl-adjust", "DSK2 – DSK100 lead-screw adjustable welding turning rolls, 4,409 – 220,462 lb", "DSK lead-screw rolls", [T_DSK],
      "The same range as the bolt-adjustable rolls, with the wheel spacing set by a lead screw and hand wheel instead of bolt positions, "
      "so the rolls are changed over to a new diameter quickly; AC frequency-converter control. Special turning rolls are designed to "
      "the customer's requirement.",
      ["4,409 – 220,462 lb (2 – 100 t) per set", "Wheel spacing set by lead screw and hand wheel", "Work Ø5.9 – 70.9″ (DSK2) to Ø39.4 – 216.5″ (DSK100)",
       "Surface speed 3.9 – 39.4 in/min (6 – 60 m/h), VFD", "Two drive motors, 2 × 1/4 HP to 2 × 4 HP"],
      ["dt-dsk", "dt-dsk-2"], "4,409 – 220,462 lb", cap="[Rated load] per set"),
    F("dt-dzg", P_ROLL, "vl-self", "DZG-5 – DZG-100 self-aligning welding turning rolls, 11,023 – 220,462 lb", "DZG self-aligning rolls", [T_DZG],
      "Self-aligning turning rolls: the wheel pairs swing on their bogies and set their angle to the vessel's diameter by themselves, "
      "so one set carries work from Ø9.8 to 216.5″ without resetting — the turning rolls of pressure vessel and pipeline makers, for "
      "handling and for automatic welding. Quiet, gentle turning with the speed set by VFD.",
      ["11,023 – 220,462 lb (5 – 100 t) per set", "Work Ø9.8 – 90.6″ (DZG-5) to Ø39.4 – 216.5″ (DZG-100)", "Polyurethane wheels Ø9.8 – 19.7″; twin wheels on the DZG-80 and DZG-100",
       "Surface speed 3.9 – 39.4 in/min (6 – 60 m/h), VFD", "1 – 7.5 HP (0.75 – 5.5 kW)"],
      ["dt-dzg", "dt-dzg-2"], "11,023 – 220,462 lb", cap="[Rated load] per set"),
    F("dt-pipe-rot", P_ROLL, "vl-pipe", "GGLJ pinch-type pipe rotators and hydraulic fit-up rotators, built to order", "Pipe & fit-up rotators", [T_PIPE_ROT],
      "Two rotators for jobs plain turning rolls do not do. The GGLJ pinch-type rotator holds a pipe between a driven lower roll and an "
      "upper roll and turns it around and over within an angle, for joining pipe segments and welding flanges, at 3.9 – 39.4 in/min "
      "set by VFD, for manual or automatic welding. The hydraulic fit-up rotator lines up two shell sections for the joint: two "
      "hydraulic swing-arm lifting rollers raise, lower and shift each section slightly until the seam is aligned, then the drive "
      "roller turns both for welding.",
      ["GGLJ: pinch rolls for pipe, elbows and flanges; 3.9 – 39.4 in/min (6 – 60 m/h), VFD",
       "Fit-up: 1 drive, 2 idler and 2 hydraulic lifting rollers on rails; the drive roller travels electrically",
       "Roller positions changed to suit the diameter; built to order"],
      ["dt-gglj", "dt-fitup"], "Built to order", cap="[Use]", note=NOTE_ORDER, models_label="GGLJ pinch-type · hydraulic fit-up"),
]

# ================================================================================================ column & boom manipulators
CAB_ROWS = {  # model: vertical mm, boom mm, rotation rpm, trolley m/min, rail span mm
    "DLH0810": (800, 1000, None, None, 1000), "DLH1015": (1000, 1500, None, None, 1000), "DLH1520": (1500, 2000, None, None, 1000),
    "DLH2020": (2000, 2000, None, None, 1000),
    "DLH2030": (2000, 3000, 0.3, 2.5, 1800), "DLH3040": (3000, 4000, 0.3, 2.5, 1800), "DLH4050": (4000, 5000, 0.3, 2.5, 1800),
    "DLH5060": (5000, 6000, 0.3, 2.0, 2000), "DLH6070": (6000, 7000, 0.3, 2.0, 2000), "DLH7080": (7000, 8000, 0.3, 2.0, 2000),
}


def cab_table(models, title, sub):
    v = [CAB_ROWS[m] for m in models]
    return table(title, sub, models, [
        ("*Vertical travel", "boom elevation stroke", "L", [x[0] for x in v]),
        ("*Boom travel", "horizontal stroke", "L", [x[1] for x in v]),
        ("Column rotation", "TXT", "±180°"),
        ("*Column rotation speed", "TXT", [f"{x[2]:g} rpm" if x[2] else "Manual" for x in v]),
        ("Boom elevating speed", "TXT", FTM(1)),
        ("*Boom feed speed", "welding speed", "TXT", "4.7 – 47.2 in/min (0.12 – 1.2 m/min)"),
        ("Carriage travel speed", "TXT", [FTM(x[3]) if x[3] else "Manual" for x in v]),
        ("Rail gauge", "trolley", "L", [x[4] for x in v]),
    ])


T_CAB_S = cab_table(["DLH0810", "DLH1015", "DLH1520", "DLH2020"], "DLH0810 – DLH2020", "Small column and boom manipulators")
T_CAB_M = cab_table(["DLH2030", "DLH3040", "DLH4050"], "DLH2030 · DLH3040 · DLH4050", "Medium column and boom manipulators")
T_CAB_H = cab_table(["DLH5060", "DLH6070", "DLH7080"], "DLH5060 · DLH6070 · DLH7080", "Heavy column and boom manipulators")

CAB_OPT = ["Arc auto-tracking", "TV monitor", "Flux recovery and conveying system"]
CAB_COMMON = ("Fixed, fixed with rotation or travelling with rotation; the boom welds inside and outside seams of small tanks and the "
              "longitudinal and circumferential seams of large ones.")
MANIPULATORS = [
    F("dt-dlh-small", P_CAB, "vl-cab", "DLH0810 – DLH2020 small column and boom manipulators, 31.5 – 78.7″ lift", "DLH small manipulators", [T_CAB_S],
      "Small column and boom manipulators carry the welding head on a boom that rises 31.5 to 78.7″ up the column and reaches out 39.4 "
      "to 78.7″, feeding at the welding speed of 4.7 – 47.2 in/min; the column turns ±180° by hand and the trolley is moved by hand. "
      + CAB_COMMON,
      ["Vertical travel 31.5 – 78.7″ (800 – 2,000 mm); boom travel 39.4 – 78.7″ (1,000 – 2,000 mm)", "Boom feed 4.7 – 47.2 in/min (0.12 – 1.2 m/min); elevating 3.3 ft/min (1 m/min)",
       "Column rotation ±180°, by hand; trolley moved by hand on a 39.4″ (1,000 mm) gauge", "Options: arc auto-tracking, TV monitor, flux recovery"],
      ["dt-dlh-small", "dt-dlh-small-2"], "Lift 31.5 – 78.7″", cap="[Vertical travel] lift × [Boom travel] boom", optional=CAB_OPT),
    F("dt-dlh-medium", P_CAB, "vl-cab", "DLH2030 · DLH3040 · DLH4050 medium column and boom manipulators, 78.7 – 157.5″ lift", "DLH medium manipulators", [T_CAB_M],
      "Medium column and boom manipulators for tanks and pressure vessels: the boom rises 78.7 to 157.5″ and reaches 118.1 to 196.9″, "
      "the column turns ±180° at 0.3 rpm and the carriage travels its rails at 8.2 ft/min. " + CAB_COMMON,
      ["Vertical travel 78.7 – 157.5″ (2,000 – 4,000 mm); boom travel 118.1 – 196.9″ (3,000 – 5,000 mm)", "Boom feed 4.7 – 47.2 in/min; elevating 3.3 ft/min",
       "Motorized column rotation ±180°, 0.3 rpm; carriage 8.2 ft/min (2.5 m/min) on a 70.9″ (1,800 mm) gauge", "Options: arc auto-tracking, TV monitor, flux recovery"],
      ["dt-dlh-medium"], "Lift 78.7 – 157.5″", cap="[Vertical travel] lift × [Boom travel] boom", optional=CAB_OPT),
    F("dt-dlh-heavy", P_CAB, "vl-cab", "DLH5060 · DLH6070 · DLH7080 heavy column and boom manipulators, 196.9 – 275.6″ lift", "DLH heavy manipulators", [T_CAB_H],
      "Heavy column and boom manipulators for large vessels, wind towers and big tanks: the boom rises 196.9 to 275.6″ and reaches "
      "236.2 to 315″, the column turns ±180° at 0.3 rpm and the carriage travels at 6.6 ft/min on a 78.7″ gauge. " + CAB_COMMON,
      ["Vertical travel 196.9 – 275.6″ (5,000 – 7,000 mm); boom travel 236.2 – 315″ (6,000 – 8,000 mm)", "Boom feed 4.7 – 47.2 in/min; elevating 3.3 ft/min",
       "Motorized column rotation ±180°, 0.3 rpm; carriage 6.6 ft/min (2 m/min) on a 78.7″ (2,000 mm) gauge", "Options: arc auto-tracking, TV monitor, flux recovery"],
      ["dt-dlh-heavy"], "Lift 196.9 – 275.6″", cap="[Vertical travel] lift × [Boom travel] boom", optional=CAB_OPT),
]

FAMILIES = POSITIONERS + ROLLS + MANIPULATORS
