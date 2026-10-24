"""Bekamak products that are not in the band-saw catalogue extractions (/home/claude/bekamak/data): the
GANTRY 2200XS, the vertical band saws and the BMDO circular saws.  Specs typed from the NovoTech
Bekamak catalogue 2025/2026 (bekamak-2025.txt) and bekamak.com (/home/claude/bekamak/site/extra/products-extra.json,
Oct 2026).  Imported by tools/bandsaw_data.py (gantry + vertical families, band-saw spec kind) and by
tools/isitan_pipe_end_saws.py (BMDO circular-saw families on the cold saw page, table spec kind).
Videos are NovoTech's own YouTube uploads (tools/novotech-bandsaw-videos.tsv) — never the supplier's channel.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from isitan_lib import manual_table, manual_spec  # noqa: E402


def model(name, caps, motor, speed, band, weight, *, hyd=None, cool=None, wh=None, dims=None, feed=None, other=None, notes="", inch_labels=None):
    return {"name": name, "capacity_mm": caps, "main_motor_kw": motor, "hydraulic_motor_kw": hyd,
            "coolant_pump_kw": cool, "blade_speed_m_min": speed, "band_mm": band, "working_height_mm": wh,
            "weight_kg": weight, "dims_mm": dims, "feed_length_mm": feed, "feed_type": None, "other": other or {}, "notes": notes,
            **({"inch_labels": inch_labels} if inch_labels else {})}


# ---- band-saw models (spec kind "bandsaw") --------------------------------------------------------
EXTRA_MODELS = {
    "GANTRY 2200XS": model("GANTRY 2200XS", {"0": {"round": 2200, "rect": [2400, 2200], "square": 2200}}, 30, "15-80", [17940, 80, 1.6], 92140,
                           hyd=11, cool=1.1, wh=935, dims=[15000, 9400, 6215],
                           other={"Feed servo motors": "2 × 2.7 HP (2 × 2 kW)", "Bow servo motors": "2 × 4 HP (2 × 3 kW)", "Hydraulic coolant pump": "1,5 kW", "Hydraulic chip-brush pump": "1,5 kW",
                                  "Coolant fan": "0,55 kW", "Chip conveyor motor": "0,55 kW", "Spiral chip conveyor": "0,25 kW",
                                  "Material feed stroke": "8400 mm", "Material range": "Ø19-3/4″ – 87″ (500 – 2200 mm), up to 23 ft (7 m) long, 110,000 lb (50,000 kg)"},
                           inch_labels={"2200": "87″"}),
    "VB 0814-8": model("VB 0814-8", {"0": {"rect": [1400, 820]}}, 15, "15-120", [8930, 67, 1.6], 51000,
                       hyd=7.5, cool=0.2, wh=1785, dims=[12700, 4850, 4100],
                       other={"Chip conveyor motor": "0,25 kW", "Maximum cutting length": "8000 mm", "Outer table": "2000 mm", "Inner table": "1400 mm", "Block weight on the table": "40,000 kg"}),
    "BMSY 613VT": model("BMSY 613VT", {"0": {"rect": [600, 600], "square": 600}}, 7.5, "15-120", [6185, 54, 1.6], 4470,
                        hyd=1.1, cool=0.2, wh=1314, dims=[3000, 1950, 3000],
                        other={"Cutting-feed servo motor": "1,5 kW", "Servo feed speed": ".004 – 39-3/8 in/min (0.1 – 999 mm/min)", "Chip conveyor motor": "0,25 kW", "Maximum cutting length": "1300 mm", "Weight with chip conveyor": "4720 kg"}),
    "BMSY 460VG": model("BMSY 460VG", {"0": {"round": 460, "rect": [710, 460], "square": 460}, "+30": {"round": 460, "rect": [590, 460], "square": 460},
                                       "+45": {"round": 460, "rect": [460, 460], "square": 460}, "+60": {"round": 275, "rect": [460, 275], "square": 275},
                                       "-30": {"round": 460, "rect": [590, 460], "square": 460}, "-45": {"round": 460, "rect": [480, 460], "square": 460},
                                       "-60": {"round": 325, "rect": [325, 325], "square": 325}},
                        4, "15-120", [6000, 34, 1.1], 2800, hyd=2.2, cool=0.2, wh=1160, dims=[3250, 2150, 2800],
                        other={"Frame-rotation motor": "0,37 kW", "Chip conveyor motor": "0,25 kW"}),
    "CROSS 0626VT": model("CROSS 0626VT", {"0": {"rect": [2600, 600], "square": 400}}, 7.5, "15-75", [12035, 54, 1.6], 33500,
                          hyd=2.2, cool=1.1, wh=1876, dims=[5920, 9972, 3870],
                          other={"Feeder motor": "2 kW", "Feed servo motor": "2 kW", "Chip brush motor": "0,18 kW", "Chip conveyor motor": "0,25 kW",
                                 "Vise capacity": "400 × 2600 mm", "Minimum cutting length": "20 mm (30 mm automatic)"}),
}


def vid(i, title, dur):
    return {"id": i, "title": title, "duration": dur, "thumb": "video-" + i}   # thumb registered by tools/yt_thumbs.py


# NovoTech's own YouTube uploads (tools/novotech-bandsaw-videos.tsv)
V_2200XS = [vid("d-fA0iRrYCs", "Biggest dual-column band saw from Bekamak: GANTRY 2200XS", "PT2M29S"), vid("vQO2VaY0SPw", "87″ band saw GANTRY 2200XS", "PT2M29S")]
V_613VT = [vid("UL2sziRylX4", "613 VT vertical metal cutting band saw", "PT1M50S")]
V_VB = [vid("qGbmGP5CwRE", "32″ × 55″ vertical metal cutting band saw — plate sawing machine VB 0814-8", "PT1M21S")]
V_460VG = [vid("w5-5lcb_gvA", "BMSY 460VG semi-automatic double-mitring tilting-frame vertical band saw", "PT2M")]
V_CROSS = [vid("SfTZWsSaZNU", "102″ × 23″ fully automatic vertical band saw machine CROSS 0626VT", "PT54S")]
V_BMDO_XS = [vid("CV27CVffJ1s", "BMDO 100 XS high-speed carbide cold saw", "PT2M"), vid("OP3ktYgA7aw", "High-speed carbide saw BMDO 100XS", "PT2M36S"), vid("_Gfo4BerI70", "High-speed carbide saw BMDO 100 XS CNC", "PT1M27S")]
V_BMDO_CS = [vid("FDPXXawic4o", "High-speed carbide cold saw BMDO 80CS CNC", "PT51S")]

# ---- families for content/families/bandsaw.json (brand bekamak) -----------------------------------
BANDSAW_FAMILIES = [
    dict(id="bekamak-gantry-2200xs", group="double-column", name="GANTRY 2200XS gantry band saw, 87″", short="GANTRY 2200XS", models=["GANTRY 2200XS"],
         summary="The largest saw Bekamak builds: a gantry-type double-column band saw that takes rounds from Ø20″ to Ø87″ (500–2200 mm) and blocks "
                 "up to 94-1/2″ × 87″ (2400 × 2200 mm), pieces up to 23 ft (7 m) long and 50,000 kg, and cuts them to length automatically. A 40 HP "
                 "main motor drives a 3-1/8″ (80 mm) band at 50–260 ft/min, servo motors feed the bow and the material, and the MES production software "
                 "optimises the cutting speed from sensors on the blade, logs every cut and controls the vises so a cut slab is released without tipping.",
         features=["Ø20″ – Ø87″ (500 – 2200 mm) rounds, 94-1/2″ × 87″ (2400 × 2200 mm) rectangles, up to 23 ft (7 m) and 50,000 kg on the table",
                   "Gantry double-column design; two 4 HP (3 kW) servo motors on the bow feed and two 2.7 HP (2 kW) on the material feed, with a 27-1/2 ft (8.4 m) feed stroke",
                   "40 HP (30 kW) main motor, 3-1/8″ × .063″ (80 × 1.6 mm) band, 50 – 260 ft/min (15 – 80 m/min) stepless",
                   "MES production-management software: cutting speed optimised from blade sensors, machine data monitored and reported",
                   "Safe unloading: the vises hold the cut piece so it cannot tip; hydraulic chip brush, spiral and bottom chip conveyors, coolant radiator"],
         videos=V_2200XS, headline="Rounds Ø20″ to Ø87″ (500 – 2200 mm) · blocks 94-1/2″ × 87″ · 23 ft long · 50,000 kg"),
    dict(id="bekamak-bmsy-460vg", group="vertical", subgroup="semi", name="BMSY 460VG semi-automatic double-miter vertical band saw, 18″", short="BMSY 460VG", models=["BMSY 460VG"],
         summary="A vertical band saw with a tilting frame that swings 60° both ways, so the blade comes down square or at a miter on plate, blocks, beams "
                 "and large profiles up to 28″ × 18″ (710 × 460 mm). Semi-automatic cycle with a hydraulic vise and automatic return, an inverter for "
                 "stepless blade speed, hydro-mechanical blade tension and a 5° inclined blade for faster cuts through flats; a frame-rotation motor sets "
                 "the angle from the panel.",
         features=["Double miter: the tilting frame rotates +60° / −60° under power; angle set on the control panel", "Ø18″ (460 mm) round, 28″ × 18″ (710 × 460 mm) rectangular at 0°",
                   "Semi-automatic cycle: hydraulic vise, controlled cutting pressure, automatic bow return", "Inverter blade speed 50 – 395 ft/min (15 – 120 m/min); 1-1/4″ (34 mm) band; hydro-mechanical blade tension with safety switch",
                   "Linear-way guidance, optical height adjustment, cutting-width adjustment lever, 5° inclined blade, blade brush, coolant pump, heavy-duty gearbox",
                   "Options: servo feeder, chip conveyor, hydraulic top clamping, micro-spray lubrication, laser line pointer"],
         videos=V_460VG, headline="Ø18″ (460 mm) round · 28″ × 18″ rectangular · tilting frame ±60°"),
    dict(id="bekamak-bmsy-613vt", group="vertical", subgroup="semi", name="BMSY 613VT vertical plate and block band saw, 23-5/8″", short="BMSY 613VT", models=["BMSY 613VT"],
         summary="A vertical band saw for slicing rolled blocks and plates lengthwise: the vertical blade travels across the workpiece on a servo-driven "
                 "cutting feed, so square or flat sections of any size up to 23-5/8″ × 23-5/8″ (600 × 600 mm) and 51″ (1300 mm) long come off a block in "
                 "one pass. Hydraulic blade tension, planetary reducer and an inverter for stepless blade speed; an optional chip conveyor clears the swarf.",
         features=["23-5/8″ × 23-5/8″ (600 × 600 mm) section, cutting length up to 51″ (1300 mm) — long-cut method for blocks and plates",
                   "Servo cutting feed 0.1 – 999 mm/min on a 2 HP servo motor; 10 HP (7.5 kW) main motor", "2-1/8″ × .063″ (54 × 1.6 mm) band, 50 – 395 ft/min (15 – 120 m/min) inverter blade speed",
                   "Hydraulic blade tension; planetary reducer; coolant pump", "Option: chip conveyor"],
         videos=V_613VT, headline="23-5/8″ × 23-5/8″ (600 × 600 mm) sections · cuts up to 51″ (1300 mm) long"),
    dict(id="bekamak-vb-0814-8", group="vertical", subgroup="semi", name="VB 0814-8 vertical block-cutting band saw, 32″ × 55″", short="VB 0814-8", models=["VB 0814-8"],
         summary="A block-cutting machine for forging shops and steel service centres: blocks up to 32″ high and 55″ wide (820 × 1400 mm) weighing up to "
                 "40,000 kg sit on the table and the vertical blade slices them from the length, up to 26 ft (8 m) of cutting travel, each cut to length "
                 "with high precision. A 20 HP main motor drives a 2-5/8″ (67 mm) band, and the MES production software optimises the cutting speed "
                 "from blade sensors and reports the machine's working data.",
         features=["32″ × 55″ (820 × 1400 mm) block section; maximum cutting length 26 ft (8000 mm)", "Table rated 40,000 kg; outer table 79″ (2000 mm), inner table 55″ (1400 mm)",
                   "20 HP (15 kW) main motor, 10 HP hydraulic unit; 2-5/8″ × .063″ (67 × 1.6 mm) band at 50 – 395 ft/min", "MES production-management software: speed optimisation from blade sensors, monitoring and reporting",
                   "Chip conveyor and coolant system"],
         videos=V_VB, headline="Blocks 32″ × 55″ (820 × 1400 mm) · cutting length to 26 ft (8 m) · 40,000 kg"),
    dict(id="bekamak-cross-0626vt", group="vertical", subgroup="auto", name="CROSS 0626VT fully automatic vertical plate band saw, 23-5/8″ × 102″", short="CROSS 0626VT", models=["CROSS 0626VT"],
         summary="A fully automated plate band saw: the vertical blade moves parallel to the table and an automatic feed positions billets, plates and "
                 "flat material up to 23-5/8″ thick and 102″ wide (600 × 2600 mm) for each cut. Built for hard-to-cut stock — tool steels, titanium, "
                 "Hastelloy and Inconel — with a 10 HP main motor, 2-1/8″ (54 mm) band and hydraulic vises over the full 102″ width.",
         features=["23-5/8″ × 102″ (600 × 2600 mm) plate and billet capacity; vise capacity 15-3/4″ × 102″ (400 × 2600 mm)", "Fully automatic: feeder motor and servo positioning, programmed lengths, minimum cut 3/4″ (20 mm) — 1-3/16″ (30 mm) in automatic mode",
                   "10 HP (7.5 kW) main motor; 2-1/8″ × .063″ (54 × 1.6 mm) band at 50 – 245 ft/min (15 – 75 m/min)", "For tool steel, titanium, Hastelloy and Inconel; chip brush and chip conveyor; 1.5 HP coolant pump"],
         videos=V_CROSS, headline="Plates and billets 23-5/8″ × 102″ (600 × 2600 mm) · automatic feed"),
]

# ---- BMDO circular saws (spec kind "table"), on the circular cold saw page -------------------------
GK_CIRC = ["blade", "round", "square", "main_motor", "weight"]


def t_bmdo_xs():
    models = ["BMDO 75XS", "BMDO 100XS", "BMDO 130XS", "BMDO 150XS"]
    rows = [
        ("Cutting capacity — round", "solid bar", ["Ø3/8″ – 3-1/8″ (10 – 80 mm)", "Ø3/4″ – 4-1/8″ (20 – 105 mm)", "Ø3/4″ – 5-1/8″ (20 – 130 mm)", "Ø3/4″ – 6-1/4″ (20 – 160 mm)"]),
        ("Cutting capacity — square", ["3/8″ – 2″ (10 – 50 mm)", "3/4″ – 2-3/4″ (20 – 70 mm)", "3/4″ – 3-1/2″ (20 – 90 mm)", "1-3/4″ – 4-3/8″ (45 – 110 mm)"]),
        ("Blade Ø × T", "TCT carbide", ["Ø11-1/4″ × .079″ (285 × 2.0 mm)", "Ø14-1/8″ × .102″ (360 × 2.6 mm)", "Ø14-1/8″ / 16-3/4″ × .102″ (360 / 425 × 2.6 mm)", "Ø18-1/8″ × .106″ (460 × 2.7 mm)"]),
        ("Blade bore / pin holes", ["32 mm / 2-11-63, 2-12-90, 2-15-80", "40 mm / 2-11-63, 2-12-90, 2-15-80", "40 mm / 2-11-63, 2-12-90, 2-15-80", "40 mm / 2-11-63, 2-12-90, 2-15-80"]),
        ("Blade speed", "stepless", ["130 – 920 ft/min (40 – 280 m/min)", "130 – 655 ft/min (40 – 200 m/min)", "130 – 655 ft/min (40 – 200 m/min)", "130 – 655 ft/min (40 – 200 m/min)"]),
        ("Main motor", ["10 HP (7.5 kW)", "20 HP (15 kW)", "20 HP (15 kW)", "20 HP (15 kW)"]),
        ("Saw-head feed / material feed", "servo", ["2.7 HP (2 kW) / 2.7 HP (2 kW)", "2.7 HP (2 kW) / 2.7 HP (2 kW)", "2.7 HP (2 kW) / 2.7 HP (2 kW)", "2.7 HP (2 kW) / 2.7 HP (2 kW)"]),
        ("Hydraulic motor", ["3 HP (2.2 kW)", "3 HP (2.2 kW)", "3 HP (2.2 kW)", "3 HP (2.2 kW)"]),
        ("Coolant pump / chip conveyor", ["0.27 HP / 0.33 HP (0.2 / 0.25 kW)", "0.27 HP / 0.33 HP (0.2 / 0.25 kW)", "0.27 HP / 0.33 HP (0.2 / 0.25 kW)", "0.27 HP / 0.33 HP (0.2 / 0.25 kW)"]),
        ("Installed power", ["19.6 HP (14.6 kW)", "29.7 HP (22.1 kW)", "29.7 HP (22.1 kW)", "29.7 HP (22.1 kW)"]),
        ("Material feed", "AC servo and ball screw", ["31-1/2″ (800 mm) stroke · 3/8″ – 394″ (10 – 9999 mm) lengths · 0 – 30 in/s (750 mm/s)"] * 4),
        ("Vise opening", ["3-1/8″ (80 mm)", "4-1/8″ (105 mm)", "5-5/16″ (135 mm)", "7-1/8″ (180 mm)"]),
        ("End-trim / remnant length", ["3/8″ / 2-3/8″ (10 / 60 mm)"] * 4),
        ("Magazine loader", "bundle of 20 ft bars", ["17 × Ø3-1/8″ (80 mm) bars", "10 × Ø4″ (100 mm) bars", "7 × Ø5-1/8″ (130 mm) bars", "6 × Ø6″ (150 mm) bars"]),
        ("Loader dimensions L × W × H", ["221 × 65 × 49″ (5620 × 1660 × 1240 mm)", "243 × 85 × 49″ (6175 × 2170 × 1245 mm)", "243 × 73 × 50″ (6180 × 1860 × 1280 mm)", "247 × 85 × 63″ (6280 × 2170 × 1600 mm)"]),
        ("Compressed air", ["73 psi (5 bar), 8.7 cfm (245 l/min)"] * 4),
        ("Hydraulic tank / oil-mist tank", ["18.5 gal / 0.4 gal (70 / 1.5 l)"] * 4),
        ("Table height", ["35-1/2″ (900 mm)"] * 4),
        ("Dimensions W × L × H", ["121 × 105 × 101″ (3070 × 2675 × 2575 mm)", "134 × 105 × 106″ (3400 × 2660 × 2680 mm)", "134 × 105 × 106″ (3400 × 2660 × 2680 mm)", "134 × 105 × 106″ (3400 × 2660 × 2680 mm)"]),
        ("Weight", ["6,768 lb (3,070 kg)", "7,937 lb (3,600 kg)", "8,014 lb (3,635 kg)", "8,113 lb (3,680 kg)"]),
    ]
    t = manual_table("BMDO XS — automatic TCT circular saws", "Carbide (TCT) blades for solid bar · servo feeding · magazine loader", models, rows, key_labels=("Cutting capacity", "Blade Ø"))
    glance = {"BMDO 75XS": ["Ø11-1/4″ TCT", "Ø3/8″ – 3-1/8″", "3/8″ – 2″", "10 HP", "6,768 lb"],
              "BMDO 100XS": ["Ø14-1/8″ TCT", "Ø3/4″ – 4-1/8″", "3/4″ – 2-3/4″", "20 HP", "7,937 lb"],
              "BMDO 130XS": ["Ø14-1/8″ / 16-3/4″ TCT", "Ø3/4″ – 5-1/8″", "3/4″ – 3-1/2″", "20 HP", "8,014 lb"],
              "BMDO 150XS": ["Ø18-1/8″ TCT", "Ø3/4″ – 6-1/4″", "1-3/4″ – 4-3/8″", "20 HP", "8,113 lb"]}
    caps = {"BMDO 75XS": "Automatic TCT circular saw · solid bar to Ø3-1/8″", "BMDO 100XS": "Automatic TCT circular saw · solid bar to Ø4-1/8″",
            "BMDO 130XS": "Automatic TCT circular saw · solid bar to Ø5-1/8″", "BMDO 150XS": "Automatic TCT circular saw · solid bar to Ø6-1/4″"}
    return manual_spec([t], GK_CIRC, glance, caps, "Capacities are for solid steel bar with a TCT blade; HSS blades for tube are available. Supplied for 600 V 3-phase with a CSA-approved panel (208 / 240 / 480 V on request).")


def t_bmdo_cs():
    models = ["BMDO 80CS", "BMDO 100CS"]
    rows = [
        ("Cutting capacity — round", "tube and solid bar", ["Ø3/4″ – 3-1/8″ (20 – 80 mm)", "Ø3/4″ – 4″ (20 – 100 mm)"]),
        ("Blade Ø × T", "HSS", ["Ø10-1/4″ – 13-3/4″ × .079 – .118″ (260 – 350 × 2.0 – 3.0 mm)", "Ø10-1/4″ – 14-1/8″ × .079 – .118″ (260 – 360 × 2.0 – 3.0 mm)"]),
        ("Blade speed", "stepless, inverter", ["72 – 425 ft/min (22 – 130 m/min)", "72 – 425 ft/min (22 – 130 m/min)"]),
        ("Main motor", ["7.5 HP (5.5 kW)", "7.5 HP (5.5 kW)"]),
        ("Saw-head servo / feeder servo", ["2.7 HP / 1.3 HP (2 / 1 kW)", "2.7 HP / 1.3 HP (2 / 1 kW)"]),
        ("Hydraulic motor", ["2 HP (1.5 kW)", "2 HP (1.5 kW)"]),
        ("Coolant pump / chip conveyor", ["0.27 HP / 0.33 HP (0.2 / 0.25 kW)", "0.27 HP / 0.33 HP (0.2 / 0.25 kW)"]),
        ("Clamp opening", ["3-3/8″ (85 mm)", "4-5/16″ (110 mm)"]),
        ("Feed stroke", "servo gripper feed", ["19-3/4″ (500 mm)", "39-3/8″ (1000 mm)"]),
        ("Feed accuracy", ["±.002 – .004″ (±0.05 – 0.1 mm) per stroke", "±.002 – .004″ (±0.05 – 0.1 mm) per stroke"]),
        ("Loader (option)", "6 m roller magazine", ["203 × 30 × 4″ (5150 × 750 × 110 mm)", "203 × 30 × 4″ (5150 × 750 × 110 mm)"]),
        ("Working height", ["35-1/2″ (900 mm)", "35-1/2″ (900 mm)"]),
        ("Dimensions L × W × H", ["63 × 67 × 83″ (1600 × 1700 × 2100 mm)", "85 × 79 × 83″ (2150 × 2000 × 2100 mm)"]),
        ("Weight", ["3,142 lb (1,425 kg)", "3,968 lb (1,800 kg)"]),
    ]
    t = manual_table("BMDO CS — automatic HSS circular saws", "HSS blades for tube and bar · servo gripper feed · touch-screen control", models, rows, key_labels=("Cutting capacity", "Blade Ø"))
    glance = {"BMDO 80CS": ["Ø10-1/4″ – 13-3/4″ HSS", "Ø3/4″ – 3-1/8″", "—", "7.5 HP", "3,142 lb"],
              "BMDO 100CS": ["Ø10-1/4″ – 14-1/8″ HSS", "Ø3/4″ – 4″", "—", "7.5 HP", "3,968 lb"]}
    caps = {"BMDO 80CS": "Automatic HSS circular saw · tube and bar to Ø3-1/8″", "BMDO 100CS": "Automatic HSS circular saw · tube and bar to Ø4″"}
    return manual_spec([t], GK_CIRC, glance, caps, "Capacities are for mild steel tube and bar with an HSS blade. Supplied for 600 V 3-phase with a CSA-approved panel (208 / 240 / 480 V on request).")


CIRCULAR_FAMILIES = [
    dict(id="bekamak-bmdo-xs", group="bekamak-circular", brand="bekamak",
         name="BMDO 75XS · 100XS · 130XS · 150XS — automatic TCT carbide circular saws, Ø3-1/8″ to Ø6-1/4″",
         short="BMDO XS carbide saws", models_label="BMDO 75XS · 100XS · 130XS · 150XS",
         summary="High-speed carbide cold saws for mass production of cut-off pieces from solid steel and non-ferrous bar: a TCT circular blade at "
                 "130 – 920 ft/min, a servo saw-head feed and a servo material feed with a 31-1/2″ stroke, a hydraulic vise with top clamping, micro-spray "
                 "lubrication and a 20 ft magazine loader. Load a bundle of bars, program the lengths and quantities on the control and the saw cuts "
                 "unattended, to ±.004″, from Ø3-1/8″ bar on the BMDO 75XS up to Ø6-1/4″ on the BMDO 150XS. HSS blades fit the same machines for tube.",
         features=["TCT carbide circular blades Ø11-1/4″ to Ø18-1/8″ for high-speed cutting of solid bar; HSS blades for tube",
                   "Servo saw-head feed and AC-servo ball-screw material feed, 31-1/2″ (800 mm) stroke, lengths 3/8″ to 394″ — cuts to ±.004″",
                   "Hydraulic vise and hydraulic top clamping; heavy-duty gearbox; inverter-driven blade speed 130 – 655 ft/min (920 on the 75XS)",
                   "20 ft (6 m) magazine loader for 6 to 17 bars; chip conveyor; ILC micro-spray coolant; blade brush; cover safety switch",
                   "Options: 20 ft (6 m) material roller table, air filter"],
         optional=["20 ft (6 m) material roller table", "Air filter", "HSS circular blades for tube", "208 / 240 / 480 V 3-phase"],
         images=["bk-bmdo-150xs-1", "bk-bmdo-100xs-1", "bk-bmdo-75xs-1", "bk-bmdo-130xs-1", "bk-bmdo-150xs-2", "bk-bmdo-75xs-2", "bk-bmdo-150xs-3", "bk-bmdo-100xs-2", "bk-bmdo-75xs-3"],
         videos=V_BMDO_XS, specs=t_bmdo_xs(),
         headline="Solid bar Ø3/8″ to Ø6-1/4″ (10 – 160 mm) · TCT blades · servo feed · magazine loader"),
    dict(id="bekamak-bmdo-cs", group="bekamak-circular", brand="bekamak",
         name="BMDO 80CS · 100CS — automatic HSS circular saws, Ø3-1/8″ and Ø4″",
         short="BMDO CS HSS saws", models_label="BMDO 80CS · BMDO 100CS",
         summary="Automatic HSS cold saws for tube and bar up to Ø4″: a vertical-slide saw head with a cemented and ground helical-gear drive for a "
                 "vibration-free cut, an inverter for stepless blade speed and electric servo feeding with a flexible gripper and floating carriage "
                 "that holds ±.002 – .004″ per stroke even in bar that is not perfectly straight. Several cutting lengths per bar are programmed on the "
                 "touch screen; safety covers enclose the cut.",
         features=["HSS circular blades Ø10-1/4″ to 14-1/8″; tube and solid bar Ø3/4″ to 3-1/8″ (80CS) or 4″ (100CS)",
                   "Vertical-slide saw head for rigidity; helical-gear head without worm screw — no play or vibration at the blade",
                   "Electric servo feeding with flexible gripper and floating carriage: ±.002 – .004″ (0.05 – 0.1 mm) per stroke; 19-3/4″ or 39-3/8″ feed stroke",
                   "Touch-screen control with several cutting lengths per bar; inverter blade speed 72 – 425 ft/min", "Hydraulic vise, heavy-duty gearbox, blade brush, chip conveyor, safety covers and switch",
                   "Options: micro-spray coolant, 20 ft (6 m) feed roller table"],
         optional=["Micro-spray coolant", "20 ft (6 m) feed roller table", "208 / 240 / 480 V 3-phase"],
         images=["bk-bmdo-80cs-1", "bk-bmdo-100cs-1", "bk-bmdo-80cs-2", "bk-bmdo-100cs-2", "bk-bmdo-80cs-3"],
         videos=V_BMDO_CS, specs=t_bmdo_cs(),
         headline="Tube and bar Ø3/4″ to Ø4″ (20 – 100 mm) · HSS blades · servo gripper feed · touch screen"),
]

# bekamak.com photos for the circular saws: key -> file in /home/claude/bekamak/site/img
CIRCULAR_IMAGES = {
    "bk-bmdo-75xs-1": ("bekamak-bmdo-75-xs-117_17754.jpg", "Bekamak BMDO 75XS automatic TCT carbide circular saw, solid bar to Ø3-1/8″"),
    "bk-bmdo-75xs-2": ("bekamak-bmdo-75-xs-117_17755.jpg", "BMDO 75XS — cabin open: TCT circular blade, saw head and hydraulic vise"),
    "bk-bmdo-75xs-3": ("bekamak-bmdo-75-xs-117_17756.jpg", "BMDO 75XS with the 20 ft magazine loader"),
    "bk-bmdo-100xs-1": ("bekamak-bmdo-100-xs-82_17519.jpg", "Bekamak BMDO 100XS automatic carbide circular saw, solid bar to Ø4-1/8″"),
    "bk-bmdo-100xs-2": ("bekamak-bmdo-100-xs-82_17521.jpg", "BMDO 100XS with the 20 ft magazine loader"),
    "bk-bmdo-130xs-1": ("bekamak-bmdo-120-xs-110_17523.jpg", "Bekamak BMDO 130XS automatic carbide circular saw, solid bar to Ø5-1/8″"),
    "bk-bmdo-150xs-1": ("bekamak-bmdo-150xs-113_17492.jpg", "Bekamak BMDO 150XS automatic carbide circular saw with magazine loader, solid bar to Ø6-1/4″"),
    "bk-bmdo-150xs-2": ("bekamak-bmdo-150xs-113_17495.jpg", "BMDO 150XS — cabin open: Ø18-1/8″ TCT blade, servo saw head and hydraulic clamping"),
    "bk-bmdo-150xs-3": ("bekamak-bmdo-150xs-113_17496.jpg", "BMDO 150XS — 20 ft magazine loader for bundles of bar"),
    "bk-bmdo-80cs-1": ("bekamak-bmdo-80-cs-81_17409.jpg", "Bekamak BMDO 80CS automatic HSS circular saw with roller table, tube and bar to Ø3-1/8″"),
    "bk-bmdo-80cs-2": ("bekamak-bmdo-80-cs-81_17516.jpg", "BMDO 80CS with the 20 ft feed roller table"),
    "bk-bmdo-80cs-3": ("bekamak-bmdo-80-cs-81_17421.jpg", "BMDO 80CS — 20 ft roller magazine for bar and tube"),
    "bk-bmdo-100cs-1": ("bekamak-bmdo-100cs-112_17450.jpg", "Bekamak BMDO 100CS automatic HSS circular saw with roller table, tube and bar to Ø4″"),
    "bk-bmdo-100cs-2": ("bekamak-bmdo-100cs-112_17451.jpg", "BMDO 100CS — front view with the feed roller table"),
}

# photos of the new band-saw models that are not on a white background: cut them out with BiRefNet
IMG_OPTS = {"GANTRY 2200XS": {"cutout": True}, "VB 0814-8": {"cutout": True}}
