#!/usr/bin/env python3
"""Dener machine tools (Kayseri, Turkey) — TTC / TTH CNC lathes, TMC vertical machining centres, TDC double-column machining
centres and the TGH-B 450 NC surface grinder.  The 5-axis machining centres are left out on purpose.

Metric data from Dener's 2024 catalogues (R-2404: TTC-TTH CNC Torna Tezgahı, CNC Dikey İşleme Merkezi, Çift Kolonlu İşleme
Merkezi, NC Taşlama Tezgahı) and the product pages of en.dener.com / denerusa.com, gathered in /home/claude/dener-mt/raw/.
Where the two disagree the catalogue's technical table wins (TTH swing over bed 700 mm, TMC 1000 X travel 1,020 mm), except the
TDC 2112 rapid traverse (24 / 24 / 15 m/min), which only denerusa.com gives model by model.  The lathes' Fanuc column of the
catalogue table (Fanuc 0i-TF Plus is standard on denerusa.com) gives the spindle motor and torque; the machining centres'
Mitsubishi column (M80A is standard there).  Shown as imperial (metric) like the rest of the site.

Pages: cnc-lathe, vertical-machining-center, surface-grinder — under the cnc-machine-tools hub
(tools/machine_tools_nav.py), written by tools/dener_mt_pages.py.
"""
import dener_data as D

BRAND = D.BRAND
P_LATHE = "cnc-lathe"
P_MC = "vertical-machining-center"
P_GRIND = "surface-grinder"


def i1(mm, nd=1):
    return f"{mm / 25.4:,.{nd}f}″"


def mm_s(v):
    return f"{v:,}" if isinstance(v, int) else f"{v:g}"


def inch(mm, nd=1):
    return f"{i1(mm, nd)} ({mm_s(mm)} mm)"


def dia(mm, nd=2):
    return f"Ø{i1(mm, nd)} ({mm_s(mm)} mm)"


def pair_in(a, b, nd=1):
    return f"{a / 25.4:,.{nd}f} / {b / 25.4:,.{nd}f}″ ({mm_s(a)} / {mm_s(b)} mm)"


def xyz(x, y, z):
    return f"{x / 25.4:.1f} × {y / 25.4:.1f} × {z / 25.4:.1f}″ ({x:,} × {y:,} × {z:,} mm)"


def area(a, b):
    return f"{a / 25.4:.1f} × {b / 25.4:.1f}″ ({a:,} × {b:,} mm)"


def hp2(a, b=None):
    if b is None:
        return f"{a * 1.341:.1f} HP ({a:g} kW)"
    return f"{a * 1.341:.1f} / {b * 1.341:.1f} HP ({a:g} / {b:g} kW)"


def hp3(x, y, z):
    return f"{x * 1.341:.1f} / {y * 1.341:.1f} / {z * 1.341:.1f} HP ({x:g} / {y:g} / {z:g} kW)"


def lbft(a, b=None):
    if b is None:
        return f"{a * 0.7376:,.0f} lb·ft ({a:g} N·m)"
    return f"{a * 0.7376:,.0f} / {b * 0.7376:,.0f} lb·ft ({a:g} / {b:g} N·m)"


def ipm(a, b=None):
    """m/min → in/min (machine-tool feeds and rapids)"""
    if b is None:
        return f"{a * 39.37:,.0f} in/min ({a:g} m/min)"
    return f"{a * 39.37:,.0f} – {b * 39.37:,.0f} in/min ({a:g} – {b:g} m/min)"


def tol(mm):
    """±0.004 mm → ±0.00016″ (±0.004 mm)"""
    s = f"{mm / 25.4:.5f}".rstrip("0")
    return f"±{s[1:] if s.startswith('0.') else s}″ (±{mm:g} mm)"


def dims(l, w, h):
    return f"{l / 25.4:.0f} × {w / 25.4:.0f} × {h / 25.4:.0f}″ ({l:,} × {w:,} × {h:,} mm)"


KEYS = ("Swing over bed", "Max. turning", "Chuck", "Travels", "Table", "Spindle speed", "Max. spindle speed", "Distance between columns",
        "Grinding")


def table(title, sub, models, rows):
    return D.table(title, sub, models, rows, key_labels=KEYS)


spec = D.spec
vids = D.vids

ORIGIN_NOTE = ("Dener builds its machine tools in Kayseri, Turkey, in the Taksan machine-tool plant it took over in 2016.")

# ======================================================================================================== CNC lathes
# (model, swing, max turn Ø, C-axis max Ø, max turn L, C-axis max L, chuck ″, bar Ø, nose, bore, rpm, motor cont/max kW,
#  max torque N·m, X, Z, feed max m/min, tailstock travel, MT, coolant L, kVA, L, W, H, kg)
LATHES = [("TTC-6", 560, 305, 275, 433, 362, 6, 45, "A2-5", 56, 6000, (11, 20.4), 171.6, 190, 450, 5, 450, 4, 140, 25, 4123, 1709, 1778, 3260),
          ("TTC-8", 560, 305, 275, 406, 335, 8, 52, "A2-6", 66, 4500, (11, 20.4), 195, 190, 450, 5, 450, 4, 140, 25, 4123, 1709, 1778, 3306),
          ("TTH-8", 700, 528, 438, 680, 627, 8, 52, "A2-6", 66, 4500, (15, 24.2), 231, 300, 760, 10, 650, 4, 160, 32, 4345, 1924, 2008, 5389),
          ("TTH-10", 700, 528, 438, 660, 607, 10, 75, "A2-8", 92, 3500, (11, 16.5), 315, 300, 760, 10, 650, 4, 160, 32, 4345, 1924, 2008, 5439),
          ("TTH-12", 700, 488, 373, 614, 537, 12, 95, "A2-11", 118, 2450, (15, 20.4), 815.9, 300, 760, 10, 650, 5, 160, 32, 4545, 2073, 2008, 5886)]


def lathe_rows(ms):
    return [("Swing over bed", [dia(r[1], 1) for r in ms]),
            ("Max. turning diameter", "C-axis turret in brackets", [f"Ø{i1(r[2])} ({r[2]} mm) · C: Ø{i1(r[3])}" for r in ms]),
            ("Max. turning length", "C-axis turret in brackets", [f"{i1(r[4])} ({r[4]} mm) · C: {i1(r[5])}" for r in ms]),
            ("Chuck", [f"{r[6]}″ hydraulic, soft and hard jaws" for r in ms]),
            ("Bar capacity", [dia(r[7]) for r in ms]),
            ("Spindle nose", [r[8] for r in ms]),
            ("Spindle bore", [dia(r[9]) for r in ms]),
            ("Max. spindle speed", [f"{r[10]:,} rpm" for r in ms]),
            ("Spindle motor", "Fanuc, continuous / max.", [hp2(*r[11]) for r in ms]),
            ("Max. spindle torque", [lbft(r[12]) for r in ms]),
            ("Travels X / Z", [pair_in(r[13], r[14]) for r in ms]),
            ("Rapid traverse X / Z", [ipm(30)] * len(ms)),
            ("Cutting feed", [ipm(1, r[15]) for r in ms]),
            ("Turret", ["12 stations, servo-driven, hydraulic clamping; 0.20 – 0.34 s per station"] * len(ms)),
            ("Tool shank / boring bar", ["1″ square (25 × 25 mm) / Ø1.57″ (40 mm)"] * len(ms)),
            ("C-axis turret", "option", [f"BMT55, 12 live tools to {6000 if r[0] != 'TTH-12' else 5000:,} rpm, {hp2(3.7, 8.3)}" for r in ms]),
            ("Tailstock", "hydraulic, quill Ø2.68″ (68 mm)", [f"{i1(r[16])} ({r[16]} mm) travel, MT{r[17]}" for r in ms]),
            ("Positioning accuracy X / Z", [".0003 / .00016″ (0.008 / 0.004 mm)"] * len(ms)),
            ("Repeatability X / Z", [".00016 / .00008″ (0.004 / 0.002 mm)"] * len(ms)),
            ("Coolant tank", [D.gal(r[18]) for r in ms]),
            ("Power supply", [f"{r[19]} kVA" for r in ms]),
            ("Dimensions L × W × H", [dims(r[20], r[21], r[22]) for r in ms]),
            ("Weight", [D.weight(r[23]) for r in ms])]


TTC, TTH = LATHES[:2], LATHES[2:]
T_TTC = table("TTC CNC lathes", "2 models · 6″ and 8″ chucks · 45° slant bed", [r[0] for r in TTC], lathe_rows(TTC))
T_TTH = table("TTH CNC lathes", "3 models · 8″, 10″ and 12″ chucks · 45° slant bed", [r[0] for r in TTH], lathe_rows(TTH))
LATHE_GK = ["swing_over_bed", "travel_x_z", "spindle_speed_max", "spindle_motor", "weight"]
LATHE_G_FROM = ["Swing over bed", "Travels X / Z", "Max. spindle speed", "Spindle motor", "Weight"]
NOTE_LATHE = ("Dimensions in inches with Dener's millimetres in brackets. Spindle motor and torque are those of the standard Fanuc control; "
              "with the optional Mitsubishi control the spindle motor is 11 / 18 kW. Max. turning diameter and length are given for "
              "the standard slot turret and, after 'C:', for the optional C-axis turret with live tools.")

LATHE_STD = ["Fanuc 0i-TF Plus CNC with 10.4″ colour screen (Mitsubishi M80 optional)",
             "One-piece 45° cast slant bed; roller linear guides; C1 / C3 ballscrews coupled directly to the servo motors",
             "Spindle on super-precision roller bearings; hydraulic chuck with soft and hard jaws",
             "12-station servo turret with tool holders; hydraulic tailstock moved independently of the turret",
             "Fully enclosed guarding with front-door interlock; chip conveyor, coolant system, oil skimmer, automatic lubrication",
             "Hydraulic unit, cabinet cooling, foot pedal, portable handwheel, levelling bolts and tools",
             "CSA-approved electrical panel; transformer for 600, 480, 240 or 208 V 3-phase"]
LATHE_OPT = ["Mitsubishi M80A control", "C-axis turret: BMT55, 12 live tools for drilling, tapping and milling", "Tool-setting arm and workpiece probe",
             "Automatic bar feeder; parts catcher", "Programmable tailstock", "Linear scales", "Automatic door", "Electrical cabinet air conditioner",
             "Chip cart; mist extractor"]

# ======================================================================================================== vertical machining centres
# (model, X, Y, Z, table L, W, T-slot pitch, load kg, nose-table min, max, motor kW, torque N·m, axis kW (x, y, z), chip-to-chip s,
#  guides X/Y/Z mm, accuracy mm, coolant L, kVA, L, W, H, kg)
TMC = [("TMC 850", 850, 510, 560, 1000, 500, 100, 500, 150, 710, (7.5, 18), (47.7, 115), (2.2, 2.2, 3.5), 3.1, "30 / 35 / 35", 0.004, 350, 32, 3965, 2200, 3185, 6500),
       ("TMC 1000", 1020, 510, 560, 1200, 500, 100, 500, 150, 710, (7.5, 18), (47.7, 115), (2.2, 2.2, 3.5), 3.1, "30 / 35 / 35", 0.004, 350, 32, 4300, 2200, 3185, 7500),
       ("TMC 1200", 1200, 600, 600, 1300, 600, 100, 1000, 150, 750, (7.5, 18), (47.7, 115), (3.5, 3.5, 3.5), 3.7, "35 / 45 / 45", 0.004, 400, 32, 4685, 2400, 3145, 8000),
       ("TMC 1300", 1300, 700, 700, 1450, 700, 125, 1200, 130, 830, (11, 30), (77.8, 191), (3.5, 3.5, 4.5), 3.7, "35 / 45 / 45", 0.004, 400, 43, 4945, 2370, 3280, 9500),
       ("TMC 1600", 1600, 700, 700, 1750, 700, 125, 1200, 130, 830, (11, 30), (77.8, 191), (3.5, 3.5, 4.5), 3.7, "35 / 45 / 45", 0.005, 400, 43, 5690, 2400, 3280, 10000)]
T_TMC = table("TMC vertical machining centres", "5 models · BBT40, 10,000 rpm, 24 tools · 33.5 to 63″ X travel", [r[0] for r in TMC], [
    ("Travels X × Y × Z", [xyz(r[1], r[2], r[3]) for r in TMC]),
    ("Table", [area(r[4], r[5]) for r in TMC]),
    ("T-slots", [f"5 × 18 mm at {r[6]} mm ({r[6] / 25.4:.2f}″)" for r in TMC]),
    ("Max. table load", [D.weight(r[7]) for r in TMC]),
    ("Spindle nose to table", [f"{r[8] / 25.4:.1f} – {r[9] / 25.4:.1f}″ ({r[8]} – {r[9]} mm)" for r in TMC]),
    ("Spindle", ["BBT40 (7/24 taper), direct drive, with spindle cooling"] * len(TMC)),
    ("Spindle speed", ["10,000 rpm · 12,000 or 15,000 rpm optional"] * len(TMC)),
    ("Spindle motor", "Mitsubishi, continuous / max.", [hp2(*r[10]) for r in TMC]),
    ("Spindle torque", "continuous / max.", [lbft(*r[11]) for r in TMC]),
    ("Axis motors X / Y / Z", [hp3(*r[12]) for r in TMC]),
    ("Rapid traverse X / Y / Z", [ipm(36)] * len(TMC)),
    ("Cutting feed", [ipm(1, 15)] * len(TMC)),
    ("Tool changer", ["24 tools, arm type, BBT40"] * len(TMC)),
    ("Tool change", "tool to tool / chip to chip", [f"1.3 / {r[13]:g} s" for r in TMC]),
    ("Max. tool", "Ø with free neighbours · length · weight", ["Ø3.9″ (100 mm), Ø5.9″ (150 mm) · 11.8″ (300 mm) · 15.4 lb (7 kg)"] * len(TMC)),
    ("Linear guides", "roller type, X / Y / Z", [f"{r[14]} mm" for r in TMC]),
    ("Ballscrews", ["C3 class, double nut, X / Y / Z"] * len(TMC)),
    ("Positioning accuracy", "per 11.8″ (300 mm)", [tol(r[15]) for r in TMC]),
    ("Repeatability", "per 11.8″ (300 mm)", [tol(0.002)] * len(TMC)),
    ("Coolant tank", [D.gal(r[16]) for r in TMC]),
    ("Power supply / air", [f"{r[17]} kVA · 73 – 87 psi (5 – 6 bar)" for r in TMC]),
    ("Floor space L × W × H", [dims(r[18], r[19], r[20]) for r in TMC]),
    ("Weight", [D.weight(r[21]) for r in TMC])])
MC_GK = ["table", "travel_x_y_z", "spindle_speed", "spindle_motor", "weight"]
TMC_G_FROM = ["Table", "Travels X × Y × Z", "Spindle speed", "Spindle motor", "Weight"]
NOTE_TMC = ("Dimensions in inches with Dener's millimetres in brackets. Spindle motor and torque are those of the standard Mitsubishi "
            "control; with the optional Fanuc 0i-MF control the spindle is a Fanuc motor of the same class. Floor space is Dener's figure for "
            "the machine's working area.")

TMC_STD = ["Mitsubishi M80A CNC, 15″ touchscreen, Navi-Mill conversational programming (Fanuc 0i-MF optional)",
           "Stress-relieved Meehanite cast base, column and saddle, laid out by finite-element analysis",
           "BBT40 10,000 rpm direct-drive spindle with spindle cooling; 24-tool arm-type changer; rigid tapping",
           "C3 double-nut ballscrews coupled directly to the servo motors; roller linear guides; 4th-axis ready",
           "Fully enclosed guarding with front-door interlock; coolant round the spindle, air blast, chip wash-down",
           "Steel-belt chip conveyor with cart, oil skimmer, automatic lubrication, cabinet cooling, handwheel",
           "CSA-approved electrical panel; transformer for 600, 480, 240 or 208 V 3-phase"]
TMC_OPT = ["Fanuc 0i-MF control", "12,000 or 15,000 rpm BBT40 spindle", "Through-spindle coolant, 435 psi (30 bar)", "CNC rotary table — 4th axis",
           "Tool setter and workpiece probe", "Linear scales", "Automatic door", "Electrical cabinet air conditioner", "Mist extractor"]

# ======================================================================================================== double-column machining centres
# (model, X, Y, Z, between columns, table L, W, T-slots n, load kg, rapid (x, y, z), axis kW, tools, coolant L, W, L, H, kg)
TDC = [("TDC 2112", 2100, 1220, 600, 1400, 2000, 1200, 7, 4000, (24, 24, 15), (9, 4.5, 4.5), "24 tools, arm type", 300, 3640, 5965, 3372, 21000),
       ("TDC 3116", 3100, 1600, 1020, 1700, 3000, 1500, 9, 10000, (12, 12, 12), (9, 7, 7), "40 tools, chain type", 800, 4340, 8315, 4390, 32000),
       ("TDC 4120", 4100, 2020, 1020, 2100, 4000, 1800, 9, 12000, (12, 12, 12), (9, 7, 7), "40 tools, chain type", 800, 4740, 10315, 4390, 40000)]


def rapid3(r):
    x, y, z = r
    if x == y == z:
        return ipm(x)
    return f"{x * 39.37:,.0f} / {y * 39.37:,.0f} / {z * 39.37:,.0f} in/min ({x:g} / {y:g} / {z:g} m/min)"


T_TDC = table("TDC double-column machining centres", "3 models · BBT50, 10,000 rpm · 82.7 to 161.4″ X travel", [r[0] for r in TDC], [
    ("Travels X × Y × Z", [xyz(r[1], r[2], r[3]) + (" · Z 31.5″ (800 mm) optional" if r[3] == 600 else "") for r in TDC]),
    ("Distance between columns", [inch(r[4]) for r in TDC]),
    ("Table", [area(r[5], r[6]) for r in TDC]),
    ("T-slots", [f"{r[7]} × 22 mm at 150 mm (5.91″)" for r in TDC]),
    ("Max. table load", [D.weight(r[8]) for r in TDC]),
    ("Spindle", ["BBT50, direct drive, through-spindle coolant 435 psi (30 bar)"] * len(TDC)),
    ("Spindle speed", ["10,000 rpm"] * len(TDC)),
    ("Spindle motor", "continuous / max.", [hp2(22, 26)] * len(TDC)),
    ("Axis motors X / Y / Z", [hp3(*r[10]) for r in TDC]),
    ("Rapid traverse X / Y / Z", [rapid3(r[9]) for r in TDC]),
    ("Cutting feed", [ipm(1, 10)] * len(TDC)),
    ("Tool changer", [f"{r[11]}, BBT50" for r in TDC]),
    ("Linear guides", ["roller type on X, Y and Z"] * len(TDC)),
    ("Positioning accuracy", "X / Y / Z", [tol(0.008)] * len(TDC)),
    ("Repeatability", "X / Y / Z", [tol(0.004)] * len(TDC)),
    ("Coolant tank", [D.gal(r[12]) for r in TDC]),
    ("Guarding", ["semi-enclosed"] * len(TDC)),
    ("Dimensions L × W × H", [dims(r[14], r[13], r[15]) for r in TDC]),
    ("Weight", [D.weight(r[16]) for r in TDC])])
TDC_G_FROM = ["Table", "Travels X × Y × Z", "Spindle speed", "Spindle motor", "Weight"]
NOTE_TDC = ("Dimensions in inches with Dener's millimetres in brackets. Mitsubishi M80A control standard, Fanuc 0i-MF Plus optional. "
            "The TDC 2112's rapid traverse is from Dener USA's specification; the 3116 and 4120 traverse at 12 m/min on all axes.")

TDC_STD = ["Mitsubishi M80A CNC with Navi-Mill conversational programming (Fanuc 0i-MF Plus optional)",
           "BBT50 10,000 rpm direct-drive spindle with spindle cooling and through-spindle coolant, 435 psi (30 bar)",
           "Arm-type 24-tool changer (TDC 2112) or chain-type 40-tool magazine (TDC 3116, 4120); rigid tapping",
           "C3 ballscrews; roller linear guides on X, Y and Z; 4th-axis ready",
           "Semi-enclosed guarding; coolant round the spindle, air blast, chip wash-down; steel-belt chip conveyor",
           "Oil skimmer, automatic lubrication, cabinet cooling, portable handwheel",
           "CSA-approved electrical panel; transformer for 600, 480, 240 or 208 V 3-phase"]
TDC_OPT = ["Fanuc 0i-MF Plus 15″ control", "Z travel 31.5″ (800 mm) on the TDC 2112", "CNC rotary table", "Tool setter and workpiece probe",
           "Linear scales", "Automatic door", "Electrical cabinet air conditioner", "Chip cart; mist extractor"]

# ======================================================================================================== surface grinder
T_TGH = table("TGH-B 450 NC surface grinder", "1 model · 17.7 × 35.4″ table · Mitsubishi NC on the cross and vertical axes", ["TGH-B 450"], [
    ("Table", [area(450, 900)]),
    ("Electromagnetic chuck", [area(400, 800)]),
    ("Grinding length × width", [area(900, 450)]),
    ("Spindle centre to table", ["3.0 – 21.7″ (75 – 550 mm)"]),
    ("Max. table load", [D.weight(400)]),
    ("T-slot", ["1 × 14 mm H7"]),
    ("Grinding wheel", ["Ø13.8 × Ø5.0 × 1.57″ (Ø350 × Ø127 × 40 mm)"]),
    ("Spindle speed", ["100 – 1,450 rpm, by inverter"]),
    ("Spindle motor", [hp2(4) + ", direct drive"]),
    ("Table speed", "longitudinal, hydraulic", ["16 – 82 ft/min (5 – 25 m/min)"]),
    ("Cross feed", "automatic, per stroke", ["0.002 – 0.79″ (0.05 – 20 mm)"]),
    ("Down feed", "smallest increment", ["0.00004″ (0.001 mm)"]),
    ("Rapid traverse vertical / cross", ["236 in/min (6 m/min)"]),
    ("Ballscrews vertical / cross", ["Ø25 mm, C3 / Ø25 mm, C6"]),
    ("Guideways", ["V and flat, Turcite-B coated, hand-scraped"]),
    ("Servo motors vertical / cross", [f"{hp2(0.7)} each"]),
    ("Hydraulic unit", [f"{hp2(4)}, 580 psi (40 bar), {D.gal(100)}"]),
    ("Coolant", [f"{D.gal(100)} tank with paper filter"]),
    ("Control", ["Mitsubishi FX5U NC, 10″ colour touchscreen"]),
    ("Power supply", ["22.3 kVA"]),
    ("Dimensions L × W × H", [dims(3280, 2750, 2151)]),
    ("Weight", [D.weight(3700)])])
TGH_GK = ["table", "grinding_area", "spindle_speed", "spindle_motor", "weight"]
TGH_G_FROM = ["Table", "Grinding length × width", "Spindle speed", "Spindle motor", "Weight"]
NOTE_TGH = "Dimensions in inches with Dener's millimetres in brackets."

TGH_STD = ["Mitsubishi NC on the cross and vertical axes, AC servo motors on ballscrews, 10″ touchscreen, wired handwheel",
           "Electro-hydraulic table drive; direct-drive spindle on preloaded precision bearings",
           "Stress-relieved cast base; honeycomb-ribbed column; V and flat guideways, Turcite-B coated and hand-scraped",
           "Electromagnetic chuck 15.7 × 31.5″ (400 × 800 mm) with demagnetizing unit",
           "Ø13.8″ (350 mm) wheel with flange, puller, balancing stand and arbor; table-mounted diamond dresser",
           "Coolant system with paper filter; hydraulic unit; central lubrication; table guard and door interlock",
           "CSA-approved electrical panel; transformer for 600, 480, 240 or 208 V 3-phase"]
TGH_OPT = ["Additional wheel flange", "Wheel-head-mounted diamond dresser", "Magnetic sine plate (V-S 100M) and sine bar (VS-100)",
           "Magnetic separator with paper filter for the coolant", "Precision toolmaker's vise (VMV-40)", "Workpiece demagnetizer (VDM-68)",
           "Profile grinding and dressing attachment (V-PB-BS)"]

FAMILIES = [
    dict(id="dn-ttc", group="lathe-ttc", page=P_LATHE, brand=BRAND,
         name="TTC compact CNC lathes, 6″ and 8″ chucks — 45° slant bed",
         short="TTC compact CNC lathes",
         models_label="TTC-6 · TTC-8 · 2 models, C-axis versions",
         summary="The TTC is Dener's compact slant-bed CNC lathe for shaft, flange and bushing work in series: a one-piece cast bed inclined at "
                 "45° that sheds chips into the conveyor, roller linear guides and C1 / C3 ballscrews coupled straight to the servo motors, "
                 "a spindle on super-precision bearings and a 12-station servo turret that indexes in 0.2 s. The TTC-6 turns parts to "
                 "Ø12″ (305 mm) × 17″ (433 mm) behind a 6″ hydraulic chuck at 6,000 rpm and takes 1.77″ (45 mm) bar; the TTC-8 has an 8″ "
                 "chuck, 2.05″ (52 mm) bar and 4,500 rpm. With the optional BMT55 C-axis turret and its 12 live tools the same machine "
                 "drills, taps and mills flats and slots in the one setup. Fanuc 0i-TF Plus control as standard, Mitsubishi M80 to order.",
         features=["45° one-piece cast slant bed; finite-element designed; travels X 7.5″ × Z 17.7″ (190 × 450 mm)",
                   "Swing over bed Ø22″ (560 mm); max. turning Ø12″ (305 mm)"] + LATHE_STD,
         optional=LATHE_OPT,
         images=["dn-ttc-1", "dn-ttc-2", "dn-ttc-3", "dn-ttc-4"],
         videos=vids(("dim9DA1TmoQ", "DENER TTC-8 CNC turning centre"), ("_bkvwzuOYW0", "DENER machining centre and turning centre assembly line")),
         specs=spec([T_TTC], LATHE_GK, LATHE_G_FROM, NOTE_LATHE)),
    dict(id="dn-tth", group="lathe-tth", page=P_LATHE, brand=BRAND,
         name="TTH CNC lathes, 8″, 10″ and 12″ chucks — 45° slant bed, Ø27.6″ swing",
         short="TTH CNC lathes",
         models_label="TTH-8 · TTH-10 · TTH-12 · 3 models, C-axis versions",
         summary="The TTH is the larger Dener slant-bed lathe: Ø27.6″ (700 mm) swing over the bed, X 11.8″ × Z 29.9″ (300 × 760 mm) travels and "
                 "parts to Ø20.8″ (528 mm) × 26.8″ (680 mm). Three spindles cover shaft and chuck work from 2″ to 3.7″ bar: the TTH-8 with an "
                 "8″ chuck, 2.05″ (52 mm) bar and 4,500 rpm, the TTH-10 with a 10″ chuck, 2.95″ (75 mm) bar and an A2-8 nose, and the TTH-12 "
                 "with a 12″ chuck, an A2-11 nose, a 4.65″ (118 mm) spindle bore and 602 lb·ft (816 N·m) of torque for heavy cuts in large "
                 "diameters. Same 45° cast bed, roller guides, servo turret and hydraulic tailstock as the TTC; the BMT55 C-axis turret with "
                 "12 live tools makes it a turn-mill centre.",
         features=["45° one-piece cast slant bed; travels X 11.8″ × Z 29.9″ (300 × 760 mm); tailstock travel 25.6″ (650 mm)",
                   "Swing over bed Ø27.6″ (700 mm); max. turning Ø20.8″ (528 mm)"] + LATHE_STD,
         optional=LATHE_OPT,
         images=["dn-tth-1", "dn-tth-2", "dn-tth-3", "dn-tth-5"],
         videos=vids(("XhIVx8rzqnY", "DENER TTH-10 CNC turning machine"), ("_bkvwzuOYW0", "DENER machining centre and turning centre assembly line")),
         specs=spec([T_TTH], LATHE_GK, LATHE_G_FROM, NOTE_LATHE)),
    dict(id="dn-tmc", group="mc-vertical", page=P_MC, brand=BRAND,
         name="TMC vertical machining centres, BBT40 — X 33.5 to 63″",
         short="TMC vertical machining centres",
         models_label="TMC 850 – TMC 1600 · 5 models",
         summary="Dener's TMC vertical machining centres mill, drill, bore and tap in one setup — pockets, contours, rigid tapping without a "
                 "floating holder, and shapes drawn freehand in the Navi-Mill conversational software. The base, column and saddle are "
                 "stress-relieved Meehanite castings laid out by finite-element analysis; the BBT40 spindle is direct-driven at 10,000 rpm "
                 "(12,000 or 15,000 to order) with its own cooling; the 24-tool arm changer swaps tools in 1.3 s; double-nut C3 ballscrews "
                 "and roller guides traverse at 1,417 in/min (36 m/min) and position to ±0.00016″ (±0.004 mm). Five sizes from the TMC 850 "
                 "— 33.5 × 20.1 × 22″ (850 × 510 × 560 mm) over a 39 × 20″ table — to the TMC 1600 with 63 × 27.6 × 27.6″ (1,600 × 700 × "
                 "700 mm) and a 2,646 lb (1,200 kg) table load; the 1300 and 1600 have a 40 HP (30 kW) spindle motor.",
         features=["Five sizes: X 33.5 – 63″, Y 20.1 – 27.6″, Z 22 – 27.6″ (850 – 1,600 × 510 – 700 × 560 – 700 mm)",
                   "1,417 in/min (36 m/min) rapids on all axes; ±0.00016″ (±0.004 mm) positioning, ±0.00008″ (±0.002 mm) repeatability"] + TMC_STD,
         optional=TMC_OPT,
         images=["dn-tmc-1", "dn-tmc-5", "dn-tmc-3", "dn-tmc-2", "dn-tmc-4", "dn-tmc-7", "dn-tmc-6"],
         videos=vids(("gUYhBOqIP3M", "DENER TMC 1200 vertical machining centre"), ("_bkvwzuOYW0", "DENER machining centre and turning centre assembly line")),
         specs=spec([T_TMC], MC_GK, TMC_G_FROM, NOTE_TMC)),
    dict(id="dn-tdc", group="mc-double", page=P_MC, brand=BRAND,
         name="TDC double-column machining centres, BBT50 — X 82.7 to 161.4″",
         short="TDC double-column machining centres",
         models_label="TDC 2112 · TDC 3116 · TDC 4120 · 3 models",
         summary="For parts too long, wide or heavy for a vertical machining centre — machine bases, moulds, plates, frames — the TDC "
                 "double-column (gantry) machining centre carries the spindle on a saddle across a rigid cross rail between two columns, "
                 "over a table that travels underneath. The BBT50 direct-drive spindle runs to 10,000 rpm on a 30 / 35 HP (22 / 26 kW) "
                 "motor, with through-spindle coolant at 435 psi (30 bar); roller guides on all three axes. Three sizes: the TDC 2112 "
                 "with 82.7 × 48 × 23.6″ (2,100 × 1,220 × 600 mm) travels, 55″ (1,400 mm) between the columns and a 24-tool changer, the "
                 "TDC 3116 with 122 × 63 × 40″ and the TDC 4120 with 161 × 79.5 × 40″ (4,100 × 2,020 × 1,020 mm), a 157.5 × 71″ table for "
                 "26,455 lb (12,000 kg) and a 40-tool chain magazine.",
         features=["Gantry frame: two columns and a cross rail over a travelling table; 55 – 82.7″ (1,400 – 2,100 mm) between the columns",
                   "Table loads 8,818 – 26,455 lb (4,000 – 12,000 kg); X travel 82.7 – 161.4″ (2,100 – 4,100 mm)"] + TDC_STD,
         optional=TDC_OPT,
         images=["dn-tdc-1", "dn-tdc-2", "dn-tdc-3", "dn-tdc-4", "dn-tdc-5"],
         videos=[],
         specs=spec([T_TDC], MC_GK, TDC_G_FROM, NOTE_TDC)),
    dict(id="dn-tgh", group="grind", page=P_GRIND, brand=BRAND,
         name="TGH-B 450 NC surface grinder, 17.7 × 35.4″ table",
         short="TGH-B 450 NC surface grinder",
         models_label="TGH-B 450 · 1 model",
         summary="A precision surface grinder for flat, parallel and square faces on dies, moulds, plates, gauges and machine parts in "
                 "hardened or soft steel and other materials. The table travels on scraped V and flat guideways with Turcite-B coating, "
                 "driven hydraulically at 16 – 82 ft/min (5 – 25 m/min); the cross and vertical axes run on ballscrews and AC servo motors "
                 "under a Mitsubishi NC with a 10″ touchscreen, so the operator keys in the stock to remove and the down feed — in "
                 "0.00004″ (0.001 mm) steps — and the cross feed are applied stroke by stroke. A 15.7 × 31.5″ (400 × 800 mm) "
                 "electromagnetic chuck on a 17.7 × 35.4″ (450 × 900 mm) table, a Ø13.8″ (350 mm) wheel on a direct-drive spindle and "
                 "21.7″ (550 mm) under the wheel centre.",
         features=["Grinds 35.4 × 17.7″ (900 × 450 mm) faces; 3.0 – 21.7″ (75 – 550 mm) from the wheel centre to the table",
                   "Automatic down feed in 0.00004″ (0.001 mm) steps; automatic cross feed 0.002 – 0.79″ (0.05 – 20 mm) per stroke"] + TGH_STD,
         optional=TGH_OPT,
         images=["dn-tgh-1", "dn-tgh-2", "dn-tgh-4", "dn-tgh-5", "dn-tgh-6", "dn-tgh-7"],
         videos=vids(("ofby5Vxihsc", "DENER TGH-B 450 surface grinding machine")),
         specs=spec([T_TGH], TGH_GK, TGH_G_FROM, NOTE_TGH)),
]
