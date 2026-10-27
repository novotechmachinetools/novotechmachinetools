"""ISITAN section: Edgebender compact hydraulic press brakes (catalogue pages 35–39) — one category page."""
from isitan_lib import *  # noqa: F401,F403

SET = "edgebender"
SECTION = "Compact press brakes"
SLUG = "compact-hydraulic-press-brakes"

IMAGES = {
    "is-eb-1240-cnc": ("cut/p35-222.png", "ISITAN Edgebender 1240 CNC 3-axis hydraulic press brake, 44 US tons × 4.2 ft"),
    "is-eb-cnc-promecam-clamps": ("cut/p35-219.png", "Edgebender 1240 CNC — quick-release Promecam top-tool clamping"),
    "is-eb-cnc-backgauge": ("cut/p35-215.png", "Edgebender 1240 CNC — CNC X-axis backgauge fingers on HIWIN linear guides"),
    "is-eb-cnc-hydraulics": ("cut/p35-217.png", "Edgebender — HAWE / Rexroth hydraulic valves and pressure gauge"),
    "is-eb-cnc-promecam": ("cut/p36-224.png", "Edgebender — Promecam punch and die installed"),
    "is-eb-cnc-supports": ("cut/p36-226.png", "Edgebender 1240 CNC — separate height setting on the front support arms"),
    "is-eb-cnc-lightguard": ("cut/p36-228.png", "Edgebender 1240 CNC — Leuze front safety light guard"),
    "is-eb-cnc-panel": ("cut/p39-262.png", "Edgebender — Siemens electrical panel"),
    # the EB photos sit on a soft grey floor glow that the auto pass keeps as a white blob — hand-set thresholds remove it
    "is-eb-2160": ("img/EB2160.jpg", "ISITAN Edgebender 2160 NC 2-axis hydraulic press brake, 66 US tons × 6.9 ft",
                   {"cut_params": {"border_thr": 226, "neutral": 4, "hole_thr": 250, "hole_area": 400, "shadow_thr": None, "edge_hi": 250, "edge_lo": 215, "band_light": 225}}),
    "is-eb-1540": ("img/EB1540.jpg", "ISITAN Edgebender 1540 NC hydraulic press brake, 44 US tons × 5.1 ft",
                   {"cut_params": {"border_thr": 240, "neutral": 6, "hole_thr": 250, "hole_area": 400, "shadow_thr": None, "edge_hi": 252, "edge_lo": 225, "band_light": 238}}),
    "is-eb-1230": ("cut/p37-234.png", "ISITAN Edgebender 1230 NC 2-axis hydraulic press brake, 33 US tons × 4.2 ft"),
    "is-eb-nc-bending": ("cut/p37-236.png", "Edgebender NC — bending a sheet behind the Leuze light guard"),
    "is-eb-nc-backgauge": ("cut/p37-238.png", "Edgebender NC — motorized X backgauge fingers on linear guides"),
    "is-eb-nc-promecam": ("cut/p37-239.png", "Edgebender 1540 / 2160 — Promecam quick-release tool clamps"),
    "is-eb-nc-lightguard": ("cut/p38-244.png", "Edgebender NC — safety light guard complying with CE"),
    "is-eb-nc-torsion": ("cut/p38-246.png", "Edgebender NC — torsion bar for sensitive bending"),
    "is-eb-nc-ballscrew": ("cut/p38-247.png", "Edgebender NC — motorized backgauge with ball screw"),
    "is-eb-nc-yaxis": ("cut/p39-255.png", "Edgebender 1230 NC — motor-controlled Y axis (angle setting)"),
    "is-eb-nc-angle": ("cut/p39-257.png", "Edgebender 1540 / 2160 NC — gearbox-driven angle adjustment"),
    "is-eb-nc-screen": ("cut/p39-253.png", "Edgebender NC — bending-force calculation on the NC control"),
    "is-eb-nc-tooling-screen": ("cut/p39-254.png", "Edgebender NC — tool selection and drawing on the NC control"),
    "is-eb-nc-interface": ("cut/p39-259.png", "Edgebender NC — X, Y and R axis display on the NC control"),
    "is-eb-nc-buttons": ("cut/p39-261.png", "Edgebender NC — control panel with emergency stop"),
}

NOTE = "Bending force in US tons (metric tons in brackets); bending capacity varies with the V-die opening and sheet length — check the bending chart. Dimensions are overall L × W × H."
GK = ["bending_force", "working_length", "control", "backgauge_travel", "weight"]


def t_cnc():
    t = manual_table("Edgebender 1240 CNC", "3 axes (Y1 + Y2 + X) · Cybelec Cybtouch 12", ["EB 1240 CNC"], [
        ("Bending force", ["44 US tons (40 t)"]),
        ("Working length", ["4.2 ft · 50.0″ (1270 mm)"]),
        ("Distance between frames", ["39.8″ (1010 mm)"]),
        ("Stroke", ["8.7″ (220 mm)"]),
        ("Throat depth", ["11.6″ (295 mm)"]),
        ("Daylight", ["16.1″ (410 mm)"]),
        ("Y free-fall speed", ["5.91 in/s (150 mm/s)"]),
        ("Y working speed", ["0.39 in/s (10 mm/s)"]),
        ("Backgauge travel", ["19.7″ (500 mm)"]),
        ("Main motor", ["5.4 HP (4 kW)"]),
        ("X-axis motor", ["0.7 HP (0.55 kW)"]),
        ("Dimensions L × W × H", ["81 × 60 × 89″ (2060 × 1520 × 2260 mm)"]),
        ("Weight", ["5,181 lb (2,350 kg)"]),
    ], key_labels=("Bending force", "Working length"))
    glance = {"EB 1240 CNC": ["44 US tons (40 t)", "4.2 ft · 50″ (1270 mm)", "Cybelec Cybtouch 12 CNC · 3 axes", "19.7″ (500 mm)", "5,181 lb"]}
    caps = {"EB 1240 CNC": "44 US tons × 4.2 ft · 3-axis CNC (Y1 + Y2 + X)"}
    return manual_spec([t], GK, glance, caps, NOTE)


def t_nc():
    t = manual_table("Edgebender NC", "2 axes (Y + X) · 3 models", ["EB 1230 NC", "EB 1540 NC", "EB 2160 NC"], [
        ("Bending force", ["33 US tons (30 t)", "44 US tons (40 t)", "66 US tons (60 t)"]),
        ("Bending capacity", "mild steel, full length", ["8 ga (4 mm)", "8 ga (4 mm)", "8 ga (4 mm)"]),
        ("Working length", ["4.2 ft · 50.0″ (1270 mm)", "5.1 ft · 61.0″ (1550 mm)", "6.9 ft · 82.7″ (2100 mm)"]),
        ("Distance between frames", ["39.8″ (1010 mm)", "49.6″ (1260 mm)", "66.9″ (1700 mm)"]),
        ("Stroke", ["5.9″ (150 mm)", "6.3″ (160 mm)", "6.3″ (160 mm)"]),
        ("Bending speed", ["0.39 in/s (10 mm/s)", "0.39 in/s (10 mm/s)", "0.39 in/s (10 mm/s)"]),
        ("Idle ram speed", ["2.76 in/s (70 mm/s)", "3.54 in/s (90 mm/s)", "3.54 in/s (90 mm/s)"]),
        ("Throat depth", ["10.0″ (255 mm)", "12.6″ (320 mm)", "12.6″ (320 mm)"]),
        ("Daylight", ["10.4″ (265 mm)", "15.0″ (380 mm)", "15.0″ (380 mm)"]),
        ("Table width", ["5.1″ (130 mm)", "3.9″ (100 mm)", "3.9″ (100 mm)"]),
        ("Lower table height", ["32.7″ (830 mm)", "33.3″ (845 mm)", "33.3″ (845 mm)"]),
        ("Backgauge travel", ["19.7″ (500 mm)", "23.6″ (600 mm)", "23.6″ (600 mm)"]),
        ("Main motor", ["4 HP (3 kW)", "7.4 HP (5.5 kW)", "10 HP (7.5 kW)"]),
        ("X-axis motor", ["0.7 HP (0.55 kW)", "1 HP (0.75 kW)", "1 HP (0.75 kW)"]),
        ("Y-axis motor", ["0.2 HP (0.18 kW)", "0.5 HP (0.37 kW)", "0.5 HP (0.37 kW)"]),
        ("R-axis motor (optional)", ["0.3 HP (0.25 kW)", "0.3 HP (0.25 kW)", "0.3 HP (0.25 kW)"]),
        ("Hydraulic oil tank", ["90 L", "120 L", "120 L"]),
        ("Dimensions L × W × H", ["69 × 54 × 85″ (1750 × 1370 × 2160 mm)", "79 × 63 × 88″ (2000 × 1600 × 2240 mm)", "96 × 63 × 88″ (2440 × 1600 × 2240 mm)"]),
        ("Weight", ["3,748 lb (1,700 kg)", "7,606 lb (3,450 kg)", "9,568 lb (4,340 kg)"]),
    ], key_labels=("Bending force", "Working length", "Bending capacity"))
    glance = {"EB 1230 NC": ["33 US tons (30 t)", "4.2 ft · 50″ (1270 mm)", "NC · 2 axes (Y + X)", "19.7″ (500 mm)", "3,748 lb"],
              "EB 1540 NC": ["44 US tons (40 t)", "5.1 ft · 61″ (1550 mm)", "NC · 2 axes (Y + X)", "23.6″ (600 mm)", "7,606 lb"],
              "EB 2160 NC": ["66 US tons (60 t)", "6.9 ft · 82.7″ (2100 mm)", "NC · 2 axes (Y + X)", "23.6″ (600 mm)", "9,568 lb"]}
    caps = {"EB 1230": "33 US tons × 4.2 ft · 2-axis NC", "EB 1540": "44 US tons × 5.1 ft · 2-axis NC", "EB 2160": "66 US tons × 6.9 ft · 2-axis NC",
            "Edgebender 1230": "33 US tons × 4.2 ft · 2-axis NC", "Edgebender 1540": "44 US tons × 5.1 ft · 2-axis NC", "Edgebender 2160": "66 US tons × 6.9 ft · 2-axis NC"}
    return manual_spec([t], GK, glance, caps, NOTE)


FAMILIES = [
    dict(id="isitan-edgebender-cnc", group="pressbrake", page=SLUG,
         name="Edgebender 1240 CNC — 3-axis (Y1 + Y2 + X) CNC hydraulic press brake",
         short="Edgebender 1240 CNC",
         models_label="Edgebender 1240 CNC · 44 US tons × 4.2 ft",
         summary="A compact 3-axis CNC press brake for the sheet-metal shop: 44 US tons over 4.2 ft with a Cybelec Cybtouch 12 touchscreen "
                 "control, independently controlled Y1 and Y2 cylinders, a CNC X-axis backgauge on HIWIN linear guides and ball screws, "
                 "and quick-release Promecam tool clamping. HAWE or Rexroth hydraulics, Siemens electrics with remote connection and a "
                 "Leuze light guard with learning mode for different part shapes — the specification of a large press brake in a "
                 "machine that fits beside a shear and a slip roll.",
         features=["Cybelec Cybtouch 12 CNC control; 3 axes Y1 + Y2 + X; GIVI magnetic linear scales", "CNC X-axis backgauge on HIWIN linear guides with ball screws, 19.7″ travel; manual R axis; programmable retract",
                   "Quick-release Promecam top-tool clamping; standard top tools and bottom die for short-edge bends; manual crowning",
                   "Double-cylinder bending system; upper beam on fibre slide bearings; balancing spindle and eccentric bearings for parallelism",
                   "Two-speed operation (free fall, bending, return); hydraulic overload safety; HAWE or Rexroth hydraulic unit at the rear top",
                   "Siemens electrics with remote-connection service; Leuze front safety barrier with learning mode; side covers with safety switch; foot pedal; height-adjustable front support arms on linear slides"],
         optional=["Motorized crowning (cambering) system", "Servo-motorized R axis; servo-motorized X axis; extended backgauge length and extra fingers", "Special bending dies; extra front support arms",
                   "Special safety systems (DSP, Fiessler)", VOLT],
         images=["is-eb-1240-cnc", "is-eb-cnc-promecam-clamps", "is-eb-cnc-backgauge", "is-eb-cnc-promecam", "is-eb-cnc-supports", "is-eb-cnc-hydraulics", "is-eb-cnc-lightguard", "is-eb-cnc-panel"],
         videos=[], specs=t_cnc(),
         headline="44 US tons (40 t) × 4.2 ft (1270 mm) · 3-axis CNC · Cybelec Cybtouch 12"),
    dict(id="isitan-edgebender-nc", group="pressbrake", page=SLUG,
         name="Edgebender 1230 / 1540 / 2160 NC — 2-axis (Y + X) NC hydraulic press brakes",
         short="Edgebender NC",
         models_label="Edgebender 1230 NC · 1540 NC · 2160 NC",
         summary="Two-axis NC press brakes from 33 to 66 US tons and 4.2 to 6.9 ft: the Y axis sets the bending angle through the NC "
                 "control (motor-driven on the 1230, gearbox-driven on the 1540 and 2160) and a high-speed motorized X backgauge on "
                 "linear guides positions the sheet to 0.008″. The NC stores 500 programs of 200 lines, calculates bending force and "
                 "draws the tool, and every machine carries HAWE or Rexroth hydraulics, Siemens / Pizzato / Balluff electrics, a Leuze "
                 "light guard and Promecam quick-release tool clamping — the compact press brake for ducting, enclosures, brackets and "
                 "job-shop bending up to 8 ga.",
         features=["NC control storing 500 programs of 200 lines; tooling selection, drawing and bending-force calculation; save and load via USB",
                   "Motor-driven Y-axis angle setting via the NC; stroke-controlled angle with mechanical stop; tonnage set by pressure switch",
                   "High-speed motorized X backgauge on linear guides: 23.6″ travel, 0.008″ accuracy; sensitive programmable retract",
                   "Quick-release Promecam upper-tool clamping; manual crowning by wedges in the upper tool holders; standard upper and lower tools",
                   "Double-cylinder bending system; two-speed operation (free fall, slow bend, fast return); hydraulic overload safety",
                   "HAWE or Rexroth hydraulic unit; Siemens, Pizzato and Balluff electrics with remote service; Leuze front safety system with learning mode; CE-compliant safety foot pedal; floating-arm control panel; front support arms on linear slides"],
         optional=["Motorized R axis with precision movement; additional backgauge length and fingers", "Manual or motorized crowning on the lower blade",
                   "Special bending dies; extra front support arm; special two-hand and foot-pedal control", "Special safety systems (DSP, Fiessler)", VOLT],
         images=["is-eb-2160", "is-eb-1540", "is-eb-1230", "is-eb-nc-bending", "is-eb-nc-backgauge", "is-eb-nc-promecam", "is-eb-nc-lightguard",
                 "is-eb-nc-torsion", "is-eb-nc-ballscrew", "is-eb-nc-yaxis", "is-eb-nc-angle", "is-eb-nc-screen", "is-eb-nc-tooling-screen", "is-eb-nc-interface", "is-eb-nc-buttons"],
         videos=[], specs=t_nc(),
         headline="33–66 US tons (30–60 t) · 4.2–6.9 ft (1270–2100 mm) · 2-axis NC"),
]

PAGE = dict(
    title="Small Hydraulic Press Brakes, 33–66 Ton NC & CNC | NovoTech",
    meta="Small hydraulic press brakes: 33, 44 and 66 ton NC models from 4.2 to 6.9 ft and a 44-ton 3-axis CNC with Cybelec control and Promecam tooling. Parts in Canada.",
    h1="Compact hydraulic press brakes",
    intro="A compact hydraulic press brake bends sheet metal between a punch and a V-die under hydraulic force — here 33 to 66 US tons over 4.2 to 6.9 ft, the size that fits a sheet-metal shop rather than a steel-fabrication plant. ISITAN's Edgebender range bends up to 8 ga over 4.2 to 6.9 ft with 33 to 66 US tons — the press brake for HVAC fittings, enclosures, brackets, signage and job-shop work where a 100-ton machine is more than you need. The NC models set the angle and backgauge from a stored program; the Edgebender 1240 CNC adds independent Y1 / Y2 cylinders and a Cybelec Cybtouch 12 touchscreen. European hydraulics, electrics and safety light guards on every machine, with CSA-approved panels and support from Mississauga, ON, Canada. For larger machines see the Dener CNC press brakes and NovoTech's value-line CNC press brakes.",
    points=["33, 44 and 66 US tons · 4.2, 5.1 and 6.9 ft (1270–2100 mm)", "2-axis NC or 3-axis CNC (Y1 + Y2 + X) with Cybelec control", "Promecam tooling, HAWE / Rexroth hydraulics, Leuze light guard"],
    hero="is-eb-1240-cnc", minis=["is-eb-2160", "is-eb-1230"],
    groups=[("pressbrake", "Edgebender press brakes line-up", "The 3-axis CNC Edgebender 1240 and the 2-axis NC 1230, 1540 and 2160.")],
    faq=[{"q": "What tonnage do I need?", "a": "Bending force depends on the sheet thickness, the bend length and the V-die opening: in mild steel about 575 × t² ÷ V US tons per foot, with t and V in inches. In a V of 8 × the thickness, a 4 ft bend takes about 16 US tons in 16 ga, 39 tons in 10 ga and 47 tons in 8 ga (0.16″); a wider die lowers the force — 8 ga in a 2″ V takes about 31 tons over 4 ft — at the cost of a larger inside radius. The NC control calculates the exact force for the tool and material you enter; send us your thickest and longest bend and we will size the machine."},
         {"q": "NC or CNC?", "a": "The 2-axis NC Edgebender sets the bending angle (Y) and the backgauge (X) from a program — enough for most job-shop bending. The 3-axis CNC Edgebender 1240 controls the two cylinders independently (Y1, Y2), so the beam can be tilted for compensation and the Cybelec Cybtouch 12 gives graphic programming, angle correction and tool libraries like a full-size CNC press brake."},
         {"q": "Which tooling fits?", "a": "The Edgebenders use Promecam-style (European) quick-release clamping, the most common tooling standard in Canada, with a standard top tool and bottom die included. Segmented punches, gooseneck tools and special dies are available — see our Eurostamp press brake tooling page."},
         {"q": "Are they safe to run without a separate guarding system?", "a": "Every Edgebender carries a Leuze front light guard with learning mode, side covers with safety switches, a programmable backgauge retract and a CE-compliant foot pedal with emergency stop; DSP and Fiessler laser systems are available as options."},
         VOLT_FAQ_GENERIC],
)


def build():
    write_families(SET, FAMILIES)
    import press_brake_nav as PBN
    write_category(SLUG, {**PAGE, "related_pages": [{"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}, {"href": "bead-rollers.html", "label": "Bead rollers"}]},
                   FAMILIES, SET, SECTION, hub=PBN.hub(), siblings=PBN.siblings(),
                   extra={"nav_label": "Compact hydraulic press brakes", "related_title": "More bending machinery from NovoTech"})
    return IMAGES
