"""The pipe and tube bender section — hub `pipe-benders` with three pages by kind of machine (the owner, Nov 7 2026), names from
the Search Console queries and Ubersuggest volumes ("cnc tube bender" 1,000 / month in the US against 40 for "cnc mandrel bender";
"nc mandrel … bender" the most-seen NC queries; "hydraulic pipe benders" seen far more than "rotary draw"):
  cnc-tube-benders          CNC tube benders: CSM first, then ISITAN
  nc-tube-benders           NC mandrel benders: ISITAN first, then CSM
  rotary-draw-tube-benders  hydraulic and rotary draw pipe benders: ISITAN BK, the premium-line TB and SPB, the NovoTech value line
Every group runs from the smallest machine to the largest, photos too.  The CSM line page (csm-tube-benders) and the value-line
tube-bender page were merged into these (301s in src/root/.htaccess).  ISITAN catalogue pages 40–49."""
from isitan_lib import *  # noqa: F401,F403
from sahinler_families import SPB_FAMILIES  # SPB draw benders, NovoTech premium line
from sahinler_lib import premium_pdf
import csm_pages as CSM          # CSM (Taiwan) CNC, NC and symmetric benders
import tubend_pages as TB        # TB 34 / TB 42 pipe benders, NovoTech premium line
import ttmc_more_data as TT      # NovoTech value-line tube and pipe benders (written to ttmc-more too, by tools/ttmc_more_pages.py)

SET = "tube-benders"
SECTION = "Pipe & tube benders"
HUB = "pipe-benders"

IMAGES = {
    # SFB CNC
    "is-sfb-38-cnc-a5": ("cut/p40-267.png", "ISITAN SFB 38-CNC/A5 5-axis servo CNC mandrel tube bender with 21″ touchscreen control"),
    "is-sfb-38-cnc": ("img/ISITAN-SFB38-CNC-R1-ANA.jpg", "ISITAN SFB 38-CNC/A3 CNC mandrel tube bender, Ø1-1/2″ × 11 ga"),
    "is-sfb-38-cnc-rear": ("img/ISITAN-SFB38-CNC-R3.jpg", "ISITAN SFB 38-CNC — bending head, servo rotation and feed axes"),
    "is-sfb-51-cnc": ("img/ISITAN-SFB-51-CNC-R1.jpg", "ISITAN SFB 51-CNC/A3 CNC mandrel tube bender, Ø2″ × 11 ga"),
    "is-sfb-76-cnc": ("img/ISITAN-SFB-76-CNC-R1.jpg", "ISITAN SFB 76-CNC/A3 CNC mandrel pipe bender, Ø3″ × 8 ga"),
    "is-sfb-90-cnc": ("img/ISITAN-SFB90-CNC-R1-1.jpg", "ISITAN SFB 90-CNC/A3 CNC mandrel pipe bender, Ø3-1/2″ × 8 ga"),
    "is-sfb-cnc-unit": ("cut/p41-289.png", "SFB 38-CNC with the mobile 21″ touchscreen CNC control unit"),
    "is-sfb-cnc-screen": ("cut/p41-269.png", "SFB CNC control — 3D bending simulation with collision warning"),
    "is-sfb-cnc-head": ("cut/p41-271.png", "SFB CNC — safety plate behind the bending head"),
    "is-sfb-cnc-mandrel": ("cut/p41-273.png", "SFB CNC — hydraulic mandrel and collet"),
    "is-sfb-cnc-cooler": ("cut/p41-275.png", "SFB CNC — hydraulic oil cooler"),
    "is-sfb-cnc-part-sofa": ("cut/p41-279.png", "Typical CNC-bent part — seating frame"),
    "is-sfb-cnc-part-fitness": ("cut/p41-283.png", "Typical CNC-bent part — fitness equipment frame"),
    # SFB NC/C and NC
    "is-sfb-90-nc-c": ("img/ISITAN-SFB90-NC-C.jpg", "ISITAN SFB 90-NC/C NC mandrel pipe bender with servo-rotation carrier, Ø3-1/2″ × 8 ga"),
    "is-sfb-51-nc-c": ("img/ISITAN-SFB51-NC-C.jpg", "ISITAN SFB 51-NC/C NC mandrel tube bender with carrier, Ø2″ × 11 ga"),
    "is-sfb-38-nc-c": ("cut/p45-319.png", "ISITAN SFB 38-NC/C NC mandrel tube bender with carrier, Ø1-1/2″ × 11 ga"),
    "is-sfb-nc-c-carrier": ("cut/p43-295.png", "SFB NC/C — servo rotation axis and hydraulic collet on the carrier"),
    "is-sfb-nc-c-servo": ("cut/p43-297.png", "SFB NC/C — servo-motorized rotation axis, the same servo as the CNC models"),
    "is-sfb-90-nc": ("img/ISITAN-SFB-90NC.jpg", "ISITAN SFB 90-NC NC mandrel pipe bender, Ø3-1/2″ × 8 ga"),
    "is-sfb-76-nc": ("img/SFB-76NC.jpg", "ISITAN SFB 76-NC NC mandrel pipe bender, Ø3″ × 8 ga"),
    "is-sfb-65-nc": ("img/ISITAN-SFB-65NC.jpg", "ISITAN SFB 65-NC NC mandrel tube bender, Ø2-1/2″ × 11 ga"),
    "is-sfb-51-nc": ("img/ISITAN-SFB-51NC.jpg", "ISITAN SFB 51-NC NC mandrel tube bender, Ø2″ × 11 ga"),
    "is-sfb-38-nc": ("img/ISITAN-SFB-38NC-STANDART.jpg", "ISITAN SFB 38-NC NC mandrel tube bender, Ø1-1/2″ × 11 ga"),
    "is-sfb-38-nc-carrier": ("img/ISITAN-SFB-38NC-ARABALI.jpg", "ISITAN SFB 38-NC with the optional manual carrier"),
    "is-sfb-nc-reducer": ("cut/p44-309.png", "SFB 65-NC — electric bending drive with reducer and 10″ touchscreen NC"),
    "is-sfb-nc-collet": ("cut/p44-313.png", "SFB 90-NC — direct-drive reducer on the 76 and 90 models"),
    # SFB 32 and 38-NC/A
    "is-sfb-32-hd": ("img/ISITAN-SFB-32HD.jpg", "ISITAN SFB 32-HD compact PLC hydraulic mandrel tube bender, Ø1-1/4″ × 11 ga"),
    "is-sfb-32-m": ("img/ISITAN-SFB-32M.jpg", "ISITAN SFB 32-M compact motorized mandrel tube bender, Ø1-1/4″ × 11 ga"),
    "is-sfb-38-nc-a2": ("cut/p47-339.png", "ISITAN SFB 38-NC/A2 NC aluminum-profile bender with carrier"),
    "is-sfb-38-nc-a": ("img/ISITAN-SFB38-NC-A.jpg", "ISITAN SFB 38-NC/A NC aluminum-profile bender for window and door frames"),
    # BK
    "is-bk-050": ("img/ISITAN-BK050.jpg", "ISITAN BK-050 rotary draw tube bender, Ø2-3/8″ × 11 ga steel tube, NC touchscreen"),
    "is-bk-42": ("img/ISITAN-BK-42.jpg", "ISITAN BK-42 rotary draw tube bender, Ø1-5/8″ × 11 ga steel tube"),
    "is-bk-h060": ("img/ISITAN-BK-H060.jpg", "ISITAN BK-H 060 hydraulic rotary draw tube bender, 0–210°"),
    "is-bk-030": ("img/ISITAN-ISITAN-BK030.jpg", "ISITAN BK 030 (76) rotary draw pipe bender, Ø3″ × 11 ga steel tube"),
    "is-bk-screen": ("cut/p49-353.png", "BK series — touchscreen with manual, program, auto and parameter modes"),
    "is-bk-panel": ("cut/p49-354.png", "BK series — NC (PLC) control panel with digital angle display"),
    "is-bk-tooling": ("cut/p49-356.png", "Tooling sets for BK rotary draw benders — bend die, clamp die and counter die"),
    "is-bk-mandrel-tooling": ("cut/p49-358.png", "Mandrel tooling set for SFB CNC benders"),
    "is-bk-mandrel-tooling-nc": ("cut/p49-360.png", "Mandrel tooling set for SFB NC benders"),
    "is-bk-part": ("cut/p49-366.png", "Typical rotary-draw-bent part — stainless tube frame"),
}

NOTE = "Tube capacities are for mild steel tube, shown as outside diameter × wall (nearest gauge or fraction). CLR = centreline radius of the bend die. Working length is the maximum tube length fed into the bender with the standard mandrel rod. Dimensions are overall L × W × H."
GK = ["capacity", "clr", "working_length", "control", "weight"]
CLR = "9.8″ (250 mm)"


def t_cnc_a5():
    t = manual_table("SFB CNC/A5 — 5-axis", "Y + B + C servo axes plus servo roll-bending axes", ["SFB 38-CNC/A5", "SFB 51-CNC/A5", "SFB 65-CNC/A5"], [
        ("Max. tube capacity", "OD × wall, mild steel", ["Ø1-1/2″ × 11 ga (Ø38 × 3 mm)", "Ø2″ × 11 ga (Ø51 × 3 mm)", "Ø2-1/2″ × 11 ga (Ø65 × 3 mm)"]),
        ("Max. bending radius (CLR)", [CLR] * 3),
        ("Max. bending angle", ["190°"] * 3),
        ("Hydraulic pressure", ["730 – 2,900 psi (50 – 200 bar)"] * 3),
        ("Working length", ["9.8 ft · 118.1″ (3000 mm)"] * 3),
        ("Rotation tolerance", ["±0.1°"] * 3),
        ("Bending speed", ["Adjustable"] * 3),
        ("Motor power", ["20 HP (15 kW)", "30 HP (22 kW)", "30 HP (22 kW)"]),
        ("Dimensions L × W × H", ["217 × 51 × 63″ (5500 × 1300 × 1600 mm)", "250 × 55 × 63″ (6350 × 1400 × 1600 mm)", "250 × 55 × 63″ (6350 × 1400 × 1600 mm)"]),
        ("Weight", ["4,960 lb (2,250 kg)", "8,267 lb (3,750 kg)", "8,708 lb (3,950 kg)"]),
    ], key_labels=("Max. tube capacity", "Working length"))
    glance = {"SFB 38-CNC/A5": ["Ø1-1/2″ × 11 ga", CLR, "9.8 ft", "5-axis servo CNC · 21″ touchscreen", "4,960 lb"],
              "SFB 51-CNC/A5": ["Ø2″ × 11 ga", CLR, "9.8 ft", "5-axis servo CNC · 21″ touchscreen", "8,267 lb"],
              "SFB 65-CNC/A5": ["Ø2-1/2″ × 11 ga", CLR, "9.8 ft", "5-axis servo CNC · 21″ touchscreen", "8,708 lb"]}
    caps = {"SFB 38-CNC/A5": "Ø1-1/2″ × 11 ga · 5-axis servo CNC", "SFB 38-CNC": "Ø1-1/2″ × 11 ga · CNC mandrel bender"}
    return manual_spec([t], GK, glance, caps, NOTE)


def t_cnc_a3():
    t = manual_table("SFB CNC/A3 — 3-axis", "Y + B + C servo axes", ["SFB 38-CNC/A3", "SFB 51-CNC/A3", "SFB 65-CNC/A3", "SFB 76-CNC/A3", "SFB 90-CNC/A3"], [
        ("Max. tube capacity", "OD × wall, mild steel", ["Ø1-1/2″ × 11 ga (Ø38 × 3 mm)", "Ø2″ × 11 ga (Ø51 × 3 mm)", "Ø2-1/2″ × 11 ga (Ø65 × 3 mm)", "Ø3″ × 8 ga (Ø76 × 4 mm)", "Ø3-1/2″ × 8 ga (Ø90 × 4 mm)"]),
        ("Max. bending radius (CLR)", [CLR] * 5),
        ("Max. bending angle", ["190°"] * 5),
        ("Hydraulic pressure", ["730 – 2,610 psi (50 – 180 bar)"] * 5),
        ("Working length", ["9.8 ft · 118.1″ (3000 mm)"] * 3 + ["13.1 ft · 157.5″ (4000 mm)"] * 2),
        ("Rotation tolerance", ["±0.1°"] * 5),
        ("Bending speed", ["Adjustable"] * 5),
        ("Bending drive", ["Servo", "Servo", "Servo", "Geared electric", "Geared electric"]),
        ("Motor power", ["14 HP (11 kW)", "21 HP (15 kW)", "21 HP (15 kW)", "27 HP (20 kW)", "34 HP (25 kW)"]),
        ("Dimensions L × W × H", ["177 × 47 × 59″ (4500 × 1200 × 1500 mm)", "195 × 51 × 63″ (4950 × 1300 × 1600 mm)", "195 × 51 × 63″ (4950 × 1300 × 1600 mm)", "236 × 57 × 69″ (6000 × 1450 × 1750 mm)", "236 × 57 × 69″ (6000 × 1450 × 1750 mm)"]),
        ("Weight", ["2,866 lb (1,300 kg)", "3,858 lb (1,750 kg)", "4,079 lb (1,850 kg)", "6,945 lb (3,150 kg)", "7,385 lb (3,350 kg)"]),
    ], key_labels=("Max. tube capacity", "Working length"))
    c = "3-axis servo CNC · 21″ touchscreen"
    glance = {"SFB 38-CNC/A3": ["Ø1-1/2″ × 11 ga", CLR, "9.8 ft", c, "2,866 lb"],
              "SFB 51-CNC/A3": ["Ø2″ × 11 ga", CLR, "9.8 ft", c, "3,858 lb"],
              "SFB 65-CNC/A3": ["Ø2-1/2″ × 11 ga", CLR, "9.8 ft", c, "4,079 lb"],
              "SFB 76-CNC/A3": ["Ø3″ × 8 ga", CLR, "13.1 ft", c, "6,945 lb"],
              "SFB 90-CNC/A3": ["Ø3-1/2″ × 8 ga", CLR, "13.1 ft", c, "7,385 lb"]}
    caps = {"SFB 38-CNC/A3": "Ø1-1/2″ × 11 ga · 3-axis servo CNC", "SFB 51-CNC/A3": "Ø2″ × 11 ga · 3-axis servo CNC", "SFB 76-CNC/A3": "Ø3″ × 8 ga · 3-axis servo CNC",
            "SFB 90-CNC/A3": "Ø3-1/2″ × 8 ga · 3-axis servo CNC", "SFB 38-CNC": "Ø1-1/2″ × 11 ga · CNC mandrel bender", "SFB 51-CNC": "Ø2″ × 11 ga · CNC mandrel bender",
            "SFB 76-CNC": "Ø3″ × 8 ga · CNC mandrel bender", "SFB 90-CNC": "Ø3-1/2″ × 8 ga · CNC mandrel bender"}
    return manual_spec([t], GK, glance, caps, NOTE)


def t_nc_c():
    t = manual_table("SFB NC/C — with carrier", "Servo rotation axis and hydraulic collet on the carrier", ["SFB 38-NC/C", "SFB 51-NC/C", "SFB 65-NC/C", "SFB 76-NC/C"], [
        ("Max. tube capacity", "OD × wall, mild steel", ["Ø1-1/2″ × 11 ga (Ø38 × 3 mm)", "Ø2″ × 11 ga (Ø51 × 3 mm)", "Ø2-1/2″ × 11 ga (Ø65 × 3 mm)", "Ø3″ × 8 ga (Ø76 × 4 mm)"]),
        ("Max. bending radius (CLR)", [CLR] * 4),
        ("Max. bending angle", ["190°"] * 4),
        ("Hydraulic pressure", ["730 – 2,610 psi (50 – 180 bar)"] * 4),
        ("Working length", ["9.8 ft · 118.1″ (3000 mm)"] * 3 + ["13.1 ft · 157.5″ (4000 mm)"]),
        ("Bending speed", ["Adjustable"] * 4),
        ("Motor power", ["7.1 HP (5.3 kW)", "12 HP (9 kW)", "15 HP (11 kW)", "22 HP (16.5 kW)"]),
        ("Dimensions L × W × H", ["177 × 45 × 65″ (4500 × 1150 × 1650 mm)", "191 × 59 × 73″ (4850 × 1500 × 1850 mm)", "191 × 59 × 73″ (4850 × 1500 × 1850 mm)", "236 × 63 × 73″ (6000 × 1600 × 1850 mm)"]),
        ("Weight", ["2,646 lb (1,200 kg)", "3,638 lb (1,650 kg)", "3,858 lb (1,750 kg)", "6,614 lb (3,000 kg)"]),
    ], key_labels=("Max. tube capacity", "Working length"))
    c = "NC · 10″ touchscreen · servo-rotation carrier"
    glance = {"SFB 38-NC/C": ["Ø1-1/2″ × 11 ga", CLR, "9.8 ft", c, "2,646 lb"], "SFB 51-NC/C": ["Ø2″ × 11 ga", CLR, "9.8 ft", c, "3,638 lb"],
              "SFB 65-NC/C": ["Ø2-1/2″ × 11 ga", CLR, "9.8 ft", c, "3,858 lb"], "SFB 76-NC/C": ["Ø3″ × 8 ga", CLR, "13.1 ft", c, "6,614 lb"]}
    caps = {"SFB 90-NC/C": "Ø3-1/2″ × 8 ga · NC with servo-rotation carrier", "SFB 51-NC/C": "Ø2″ × 11 ga · NC with servo-rotation carrier", "SFB 38-NC/C": "Ø1-1/2″ × 11 ga · NC with servo-rotation carrier"}
    return manual_spec([t], GK, glance, caps, NOTE + " The SFB 90-NC/C carrier model is built to order.")


def t_nc():
    t = manual_table("SFB NC", "10″ touchscreen NC, hydraulic mandrel", ["SFB 38-NC", "SFB 51-NC", "SFB 65-NC", "SFB 76-NC", "SFB 90-NC"], [
        ("Max. tube capacity", "OD × wall, mild steel", ["Ø1-1/2″ × 11 ga (Ø38 × 3 mm)", "Ø2″ × 11 ga (Ø51 × 3 mm)", "Ø2-1/2″ × 11 ga (Ø65 × 3 mm)", "Ø3″ × 8 ga (Ø76 × 4 mm)", "Ø3-1/2″ × 8 ga (Ø90 × 4 mm)"]),
        ("Max. bending radius (CLR)", [CLR] * 5),
        ("Max. bending angle", ["190°"] * 5),
        ("Hydraulic pressure", ["730 – 2,610 psi (50 – 180 bar)"] * 5),
        ("Working length", ["11.8 ft · 141.7″ (3600 mm)"] * 3 + ["15.1 ft · 181.1″ (4600 mm)"] * 2),
        ("Bending speed", ["Adjustable"] * 5),
        ("Bending drive", ["Electric with reducer", "Electric with reducer", "Electric with reducer", "Direct-drive reducer", "Direct-drive reducer"]),
        ("Hydraulic oil tank", ["40 L", "70 L", "70 L", "100 L", "100 L"]),
        ("Motor power", ["7 HP (5.2 kW)", "11 HP (8 kW)", "14 HP (10.5 kW)", "20 HP (15 kW)", "25 HP (18.5 kW)"]),
        ("Dimensions L × W × H", ["177 × 45 × 55″ (4500 × 1150 × 1400 mm)", "191 × 59 × 59″ (4850 × 1500 × 1500 mm)", "191 × 59 × 59″ (4850 × 1500 × 1500 mm)", "236 × 63 × 63″ (6000 × 1600 × 1600 mm)", "236 × 63 × 63″ (6000 × 1600 × 1600 mm)"]),
        ("Weight", ["2,205 lb (1,000 kg)", "3,417 lb (1,550 kg)", "3,527 lb (1,600 kg)", "5,842 lb (2,650 kg)", "6,283 lb (2,850 kg)"]),
    ], key_labels=("Max. tube capacity", "Working length"))
    c = "NC · 10″ touchscreen · 100 programs"
    glance = {"SFB 38-NC": ["Ø1-1/2″ × 11 ga", CLR, "11.8 ft", c, "2,205 lb"], "SFB 51-NC": ["Ø2″ × 11 ga", CLR, "11.8 ft", c, "3,417 lb"],
              "SFB 65-NC": ["Ø2-1/2″ × 11 ga", CLR, "11.8 ft", c, "3,527 lb"], "SFB 76-NC": ["Ø3″ × 8 ga", CLR, "15.1 ft", c, "5,842 lb"],
              "SFB 90-NC": ["Ø3-1/2″ × 8 ga", CLR, "15.1 ft", c, "6,283 lb"]}
    caps = {"SFB 90-NC": "Ø3-1/2″ × 8 ga · NC mandrel bender", "SFB 76-NC": "Ø3″ × 8 ga · NC mandrel bender", "SFB 65-NC": "Ø2-1/2″ × 11 ga · NC mandrel bender",
            "SFB 51-NC": "Ø2″ × 11 ga · NC mandrel bender", "SFB 38-NC": "Ø1-1/2″ × 11 ga · NC mandrel bender"}
    return manual_spec([t], GK, glance, caps, NOTE)


def t_sfb32():
    t = manual_table("SFB 32 — compact mandrel benders", "PLC hydraulic and motorized", ["SFB 32-HD", "SFB 32-M"], [
        ("Max. tube capacity", "OD × wall, mild steel", ["Ø1-1/4″ × 11 ga (Ø32 × 3 mm)", "Ø1-1/4″ × 11 ga (Ø32 × 3 mm)"]),
        ("Max. bending radius (CLR)", [CLR] * 2),
        ("Max. bending angle", ["190°"] * 2),
        ("Hydraulic pressure", ["730 – 2,610 psi (50 – 180 bar)", "— (motorized)"]),
        ("Working length", ["6.9 ft · 82.7″ (2100 mm)", "4.9 ft · 59.1″ (1500 mm)"]),
        ("Control", ["PLC with 4.7″ touchscreen · 20 programs", "Manual angle scale · foot pedal"]),
        ("Clamping", ["Hydraulic", "Manual"]),
        ("Motor power", ["5 HP (3.7 kW)", "3 HP (2.2 kW)"]),
        ("Hydraulic oil tank", ["20 L", "—"]),
        ("Dimensions L × W × H", ["91 × 43 × 45″ (2300 × 1100 × 1150 mm)", "91 × 43 × 45″ (2300 × 1100 × 1150 mm)"]),
        ("Weight", ["794 lb (360 kg)", "639 lb (290 kg)"]),
    ], key_labels=("Max. tube capacity", "Working length"))
    glance = {"SFB 32-HD": ["Ø1-1/4″ × 11 ga", CLR, "6.9 ft", "PLC · 4.7″ touchscreen · hydraulic clamping", "794 lb"],
              "SFB 32-M": ["Ø1-1/4″ × 11 ga", CLR, "4.9 ft", "Motorized · manual clamping · foot pedal", "639 lb"]}
    caps = {"SFB 32-HD": "Ø1-1/4″ × 11 ga · PLC hydraulic, 6.9 ft", "SFB 32-M": "Ø1-1/4″ × 11 ga · motorized, 4.9 ft"}
    return manual_spec([t], GK, glance, caps, NOTE)


def t_nc_a():
    t = manual_table("SFB 38-NC/A2 · NC/A — aluminum-profile benders", "Special tooling for window, door and frame profiles", ["SFB 38-NC/A2", "SFB 38-NC/A"], [
        ("Profile capacity", ["Aluminum window and door profiles — quoted per profile drawing", "Aluminum window and door profiles — quoted per profile drawing"]),
        ("Max. bending radius (CLR)", [CLR] * 2),
        ("Max. bending angle", ["190°"] * 2),
        ("Hydraulic pressure", ["730 – 2,610 psi (50 – 180 bar)"] * 2),
        ("Working length", ["9.8 ft · 118.1″ (3000 mm)"] * 2),
        ("Carrier", ["Yes — rotation and feed on carrier", "No — standard feed"]),
        ("Bending speed", ["Adjustable"] * 2),
        ("Motor power", ["9.4 HP (7 kW)", "7.4 HP (5.5 kW)"]),
        ("Dimensions L × W × H", ["177 × 45 × 39″ (4500 × 1150 × 1000 mm)", "177 × 45 × 53″ (4500 × 1150 × 1350 mm)"]),
    ], key_labels=("Profile capacity", "Working length"))
    glance = {"SFB 38-NC/A2": ["Aluminum profiles (per drawing)", CLR, "9.8 ft", "NC · 10″ touchscreen · carrier", "—"],
              "SFB 38-NC/A": ["Aluminum profiles (per drawing)", CLR, "9.8 ft", "NC · 10″ touchscreen", "—"]}
    caps = {"SFB 38-NC/A2": "Aluminum-profile bender with carrier", "SFB 38-NC/A": "Aluminum-profile bender"}
    return manual_spec([t], GK, glance, caps, "Profile-bending dies are made to the customer's profile drawing; capacity depends on the profile section and alloy. " + NOTE)


def t_bk():
    models = ["BK-42", "BK-050", "BK-H 060", "BK 030 (76)"]
    t1 = manual_table("BK series — rotary draw benders (non-mandrel)", "Machine data", models, [
        ("Tube capacity", "pipe size, NPS", ["1/8″ – 1-1/4″", "1/8″ – 2″", "1/8″ – 2″", "1/8″ – 2-1/2″"]),
        ("Max. bending radius (CLR)", ["7.9″ (200 mm)"] * 4),
        ("Bending angle", ["Programmed", "Programmed", "0 – 210°", "Programmed"]),
        ("Control", ["Touchscreen NC (PLC) · 20 programs", "One-touch control · two speeds", "One-touch control · two speeds · hydraulic", "Touchscreen NC (PLC) · 20 programs"]),
        ("Motor power", ["1 HP (0.75 kW)", "3 HP (2.2 kW)", "3 HP (2.2 kW)", "3 HP (2.2 kW)"]),
        ("Hydraulic oil tank", ["—", "—", "25 L", "—"]),
        ("Dimensions L × W × H", ["22 × 18 × 41″ (560 × 460 × 1040 mm)", "30 × 22 × 43″ (760 × 560 × 1090 mm)", "30 × 22 × 43″ (760 × 560 × 1090 mm)", "30 × 22 × 43″ (760 × 560 × 1090 mm)"]),
        ("Weight", ["243 lb (110 kg)", "309 lb (140 kg)", "311 lb (141 kg)", "397 lb (180 kg)"]),
    ], key_labels=("Tube capacity",))
    t2 = manual_table("BK series — maximum bending capacities", "At maximum, with matching tooling · tube as OD × wall", models, [
        ("Gas pipe (Sch. 40)", ["1-1/4″ NPS", "2″ NPS", "—", "—"]),
        ("Steel tube", ["Ø1-5/8″ × 11 ga", "Ø2-3/8″ × 11 ga", "Ø2-3/8″ × 11 ga", "Ø3″ × 11 ga"]),
        ("Stainless steel tube (304/316)", ["Ø1-5/8″ × 14 ga", "Ø2-3/8″ × 14 ga", "Ø2-3/8″ × 12 ga", "Ø2-3/4″ × 8 ga"]),
        ("Hard copper & aluminum tube", ["Ø2-1/8″ × 14 ga", "Ø2-1/2″ × 8 ga", "Ø2-3/8″ × 3/16″", "Ø3″ × 1/4″"]),
        ("Solid round bar", ["Ø1-1/8″", "Ø1-3/8″", "Ø1-3/4″", "Ø1-3/4″"]),
        ("Solid square / rectangular bar", ["1/4″ × 1-5/8″", "3/8″ × 2-3/8″", "1-1/8″ × 2-3/8″", "3/8″ × 3-1/2″"]),
        ("Flat bar — hard way", ["1-5/8″ × 1/2″", "2-3/8″ × 5/8″", "2-3/8″ × 5/8″", "3″ × 9/16″"]),
        ("Flat bar — easy way", ["1-5/8″ × 13/16″", "2-3/8″ × 1-1/8″", "2-3/8″ × 1-1/8″", "3″ × 1-1/8″"]),
        ("Box section", ["1-5/8″ × 13/16″ × 12 ga", "2-3/8″ × 1-1/8″ × 8 ga", "2-3/8″ × 1-1/8″ × 8 ga", "2-3/4″ × 1-5/8″ × 8 ga"]),
    ], key_labels=("Steel tube",))
    glance = {"BK-42": ["Ø1-5/8″ × 11 ga steel tube · 1-1/4″ NPS", "7.9″ (200 mm)", "—", "Touchscreen NC (PLC)", "243 lb"],
              "BK-050": ["Ø2-3/8″ × 11 ga steel tube · 2″ NPS", "7.9″ (200 mm)", "—", "One-touch · two speeds", "309 lb"],
              "BK-H 060": ["Ø2-3/8″ × 11 ga steel tube", "7.9″ (200 mm)", "—", "Hydraulic · one-touch · 0–210°", "311 lb"],
              "BK 030 (76)": ["Ø3″ × 11 ga steel tube", "7.9″ (200 mm)", "—", "Touchscreen NC (PLC)", "397 lb"]}
    caps = {"BK-42": "Ø1-5/8″ × 11 ga steel tube · touchscreen NC", "BK-050": "Ø2-3/8″ × 11 ga steel tube · one-touch control", "BK-H 060": "Ø2-3/8″ × 11 ga · hydraulic, 0–210°", "BK 030": "Ø3″ × 11 ga steel tube · touchscreen NC"}
    # two tables: only the first carries the model glance rows
    sp = manual_spec([t1, t2], GK, glance, caps, "Rotary draw (non-mandrel) bending — tube is bent around a die without an internal mandrel, so wall thickness and CLR limits are tighter than on the SFB mandrel benders. Capacities are at maximum with matching tooling; one tooling set is included. Dimensions are overall L × W × H.")
    sp["models"] = [{"name": m, "glance": glance[m]} for m in models]
    return sp


P_CNC, P_NC, P_BK = "cnc-tube-benders", "nc-tube-benders", "rotary-draw-tube-benders"
P_CSM = CSM.D.P_BEND

FAMILIES = [
    dict(id="isitan-sfb-cnc-a5", group="cnc", page=P_CNC,
         name="SFB CNC/A5 — 5-axis servo CNC mandrel tube benders",
         short="SFB CNC/A5",
         models_label="SFB 38-CNC/A5 · 51-CNC/A5 · 65-CNC/A5",
         summary="Fully servo-driven CNC mandrel benders with five axes: servo feed (Y), rotation (B) and bend (C) plus two servo "
                 "roll-bending axes, so the same machine draw-bends tight radii with the mandrel and roll-bends large sweeps "
                 "without a tooling change. A mobile 21″ touchscreen CNC with 3D simulation, spring-back and hardness compensation, "
                 "X-Y-Z to Y-B-C conversion and automatic job reports — for exhaust, chassis, seating and fitness-frame production "
                 "in Ø1-1/2″ to Ø2-1/2″ tube.",
         features=["Servo-motorized feeding (Y), rotation (B) and bending (C) axes; two axes move together; rotation tolerance ±0.1°",
                   "Servo roll-bending axes for large-radius sweeps on the same machine", "Mobile CNC control unit with 21″ TFT touchscreen; 3D bending simulation with collision warning; spring-back calculation; hardness compensation",
                   "X-Y-Z to Y-B-C conversion; tube-length and bending-time calculation; daily, weekly and monthly reports e-mailed automatically; remote assistance",
                   "Hydraulic clamping, mandrel, pressure die, linear slider and collet; bending with or without mandrel; manual and automatic operation",
                   "Safety plate behind the bending head; mobile foot pedal with emergency stop; electrical cabinet cooler; lockable panel with safety interlock; overload protection; 1 die set (3 pieces) in requested size"],
         optional=["Extra die sets; ball mandrel and wiper die", "Extended mandrel length (up to 20 ft)", "Automatic mandrel lubrication (SFB 51 / 65)", "Hydraulic oil cooler and oil heater", "Safety mat 30 × 39″ or 39 × 59″", VOLT],
         images=["is-sfb-38-cnc-a5", "is-sfb-cnc-unit", "is-sfb-cnc-screen", "is-sfb-cnc-mandrel", "is-sfb-cnc-head", "is-sfb-cnc-cooler", "is-sfb-cnc-part-sofa", "is-sfb-cnc-part-fitness"],
         videos=[], specs=t_cnc_a5(),
         headline="Ø1-1/2″ – Ø2-1/2″ × 11 ga · 5 servo axes · 21″ touchscreen CNC with 3D simulation"),
    dict(id="isitan-sfb-cnc-a3", group="cnc", page=P_CNC,
         name="SFB CNC/A3 — 3-axis servo CNC mandrel tube & pipe benders",
         short="SFB CNC/A3",
         models_label="SFB 38 · 51 · 65 · 76 · 90-CNC/A3",
         summary="The production CNC mandrel bender in five sizes from Ø1-1/2″ tube to Ø3-1/2″ × 8 ga pipe. Servo feed, rotation and "
                 "bend axes on the 38, 51 and 65 (geared electric bending drive on the 76 and 90), the same 21″ touchscreen CNC "
                 "with 3D simulation as the A5, hydraulic mandrel, collet and clamping, and a standard oil cooler for shift work. "
                 "The CNC tube bender for multi-bend parts — handrails, exhaust and automotive tube, furniture and fabricated "
                 "assemblies — with 9.8 or 13.1 ft of feed.",
         features=["Servo-motorized feeding (Y) and rotation (B) axes; servo bending axis on SFB 38 / 51 / 65, geared electric bending drive on SFB 76 / 90",
                   "Mobile CNC control unit with 21″ TFT touchscreen; 3D simulation; spring-back calculation; hardness compensation; all profile types (round, square, rectangular)",
                   "X-Y-Z to Y-B-C conversion; tube-length and cycle-time estimate; job reports over the local network; remote assistance",
                   "Hydraulic clamping, mandrel, pressure die, linear slider and collet; hydraulic oil cooler standard; automatic mandrel lubrication on SFB 38-CNC/A3",
                   "Bending with or without mandrel; manual and automatic operation; mobile foot pedal with emergency stop",
                   "Safety plate behind the bending head; electrical cabinet cooler; lockable panel with safety interlock; overload protection; 1 die set (3 pieces) in requested size"],
         optional=["Extra die sets; ball mandrel and wiper die", "Extended mandrel length (up to 20 ft)", "Automatic mandrel lubrication (SFB 51 / 65 / 76 / 90)", "Hydraulic oil heater", "Safety mat 30 × 39″ or 39 × 59″", VOLT],
         images=["is-sfb-90-cnc", "is-sfb-76-cnc", "is-sfb-51-cnc", "is-sfb-38-cnc", "is-sfb-38-cnc-rear"],
         videos=[], specs=t_cnc_a3(),
         headline="Ø1-1/2″ × 11 ga to Ø3-1/2″ × 8 ga · 3 servo axes · 9.8 / 13.1 ft feed"),
    dict(id="isitan-sfb-nc-c", group="nc", page=P_NC,
         name="SFB NC/C — NC mandrel tube benders with servo-rotation carrier",
         short="SFB NC/C",
         models_label="SFB 38 · 51 · 65 · 76-NC/C",
         summary="An NC mandrel bender with a carrier: the hydraulic collet holds the tube, a servo motor — the same as on the CNC "
                 "models — rotates it between bends to very low tolerance, and the operator feeds to adjustable stops on the "
                 "carrier slide while a screen on the carrier shows feed length and rotation angle. Faster and more repeatable "
                 "than a standard NC bender for series production of furniture, lighting, metal accessories and handrail parts, "
                 "at a fraction of the price of a CNC.",
         features=["NC carrier: servo-motorized rotation axis (B), hydraulic collet, manual feeding axis (Y) with adjustable stoppers, screen on the carrier",
                   "Five hydraulic cylinders: slider support, clamping, mandrel, pressure die and collet", "NC control unit with 10″ touchscreen on a mobile panel; 100-program memory, 20 bends per program; working-status reports, error and warning messages",
                   "Electric bending axis (C) with reducer and brake motor for precise bends; bending angle measured by encoder; bending with or without mandrel",
                   "Mobile foot pedal with emergency stop; safety plate behind the bending head; overload protection; CE certified; 1 die set in requested size"],
         optional=["Motorized feeding (Y axis)", "Extra die sets; ball mandrel; wiper die", "Extended mandrel length (up to 20 ft)", VOLT],
         images=["is-sfb-90-nc-c", "is-sfb-51-nc-c", "is-sfb-38-nc-c", "is-sfb-nc-c-carrier", "is-sfb-nc-c-servo"],
         videos=[], specs=t_nc_c(),
         headline="Ø1-1/2″ × 11 ga to Ø3″ × 8 ga · servo rotation on carrier · 10″ touchscreen NC"),
    dict(id="isitan-sfb-nc", group="nc", page=P_NC,
         name="SFB NC — NC mandrel tube & pipe benders",
         short="SFB NC",
         models_label="SFB 38 · 51 · 65 · 76 · 90-NC",
         summary="ISITAN's best-selling mandrel bender: a 10″ touchscreen NC with 100 programs of 20 sequential bends, hydraulic "
                 "mandrel, clamping and pressure die, an electric bending drive with brake motor and encoder angle measurement, "
                 "and the longest feed in the range at 11.8 or 15.1 ft. Five sizes from Ø1-1/2″ × 11 ga to Ø3-1/2″ × 8 ga — "
                 "the pipe bending machine for exhaust shops, handrail and fence fabricators, trailer and chassis builders and "
                 "job shops bending with or without a mandrel.",
         features=["NC control unit with 10″ TFT touchscreen; 100-program memory, 20 sequential bends per program; working-status reports, error and warning messages",
                   "Electric bending drive with reducer (direct-drive reducer on 76 and 90 NC); brake motor for precise bends; bending angle measured by encoder",
                   "Four hydraulic cylinders: slider support, clamping, mandrel and pressure die; bending with or without mandrel",
                   "Gauge-distance bracket; mobile foot pedal with emergency stop; safety plate on the bending head",
                   "Lockable electrical panel with safety interlock; overload protection; 1 die set in requested size"],
         optional=["Manual carrier", "Extra die sets in requested size; ball mandrel; wiper die", "Extended mandrel length (up to 20 ft)", VOLT],
         images=["is-sfb-76-nc", "is-sfb-65-nc", "is-sfb-51-nc", "is-sfb-38-nc", "is-sfb-38-nc-carrier", "is-sfb-nc-reducer", "is-sfb-nc-collet"],
         videos=[], specs=t_nc(),
         headline="Ø1-1/2″ × 11 ga to Ø3-1/2″ × 8 ga · 10″ touchscreen NC · 11.8 / 15.1 ft feed"),
    dict(id="isitan-sfb-32", group="compact", page=P_NC,
         name="SFB 32-HD · SFB 32-M — compact mandrel tube benders",
         short="SFB 32",
         models_label="SFB 32-HD (PLC hydraulic) · SFB 32-M (motorized)",
         summary="Compact mandrel benders for Ø1-1/4″ × 11 ga tube in a 91″ footprint: the SFB 32-HD with PLC control, 4.7″ "
                 "touchscreen, 20 programs of 10 bends and hydraulic clamping, and the SFB 32-M, a motorized bender with manual "
                 "clamping and angle scale. Both have a direct gear-drive reducer, brake motor, square attachment and support "
                 "pulley — the entry point to mandrel bending for handrail, furniture and small-tube work.",
         features=["SFB 32-HD: PLC control with 4.7″ TFT touchscreen, 20-program memory with 10 sequential bends per program, hydraulic clamping, gauge-distance attachment, overload protection",
                   "SFB 32-M: motorized bending with manual clamping and manual angle scale, gauge-distance bracket",
                   "Bending system with special direct gear-drive reducer; brake motor for precise bends", "Square attachment and support pulley; mobile foot pedal with emergency stop",
                   "Lockable electrical panel with safety interlock; CE certified; 1 die set in requested size"],
         optional=["Extra die sets in requested size", VOLT],
         images=["is-sfb-32-hd", "is-sfb-32-m"],
         videos=[], specs=t_sfb32(),
         headline="Ø1-1/4″ × 11 ga · PLC hydraulic or motorized · 91″ footprint"),
    dict(id="isitan-sfb-38-nc-a", group="compact", page=P_NC,
         name="SFB 38-NC/A2 · SFB 38-NC/A — NC aluminum-profile bending machines",
         short="SFB 38-NC/A",
         models_label="SFB 38-NC/A2 (with carrier) · SFB 38-NC/A",
         summary="NC benders built for aluminum window, door and frame profiles: special profile dies made to your section drawing, "
                 "hydraulic support and clamping, a hydraulic tooling clamp and the 10″ touchscreen NC with 100 programs. The "
                 "NC/A2 adds a carrier with rotation and feed for arched frames and repeat work. Special production — quoted "
                 "with the profile drawing.",
         features=["1 special aluminum-profile bending die set in requested size; hydraulic tooling clamp", "Mobile NC control unit with 10″ TFT touchscreen; 100-program memory, 20 bends per program; working-status reports, error and warning messages",
                   "Electric bending drive with reducer; bending angle measured by encoder; hydraulic support and clamping",
                   "Mobile foot pedal with emergency stop; safety plate behind the bending head; gauge-distance bracket", "Lockable electrical panel with safety interlock; overload protection"],
         optional=["Additional profile die sets", VOLT],
         images=["is-sfb-38-nc-a2", "is-sfb-38-nc-a"],
         videos=[], specs=t_nc_a(),
         headline="Aluminum window & door profiles · 10″ touchscreen NC · dies to your profile drawing"),
    dict(id="isitan-bk", group="bk", page=P_BK,
         name="BK series — rotary draw tube & profile benders (non-mandrel)",
         short="BK series",
         models_label="BK-42 · BK-050 · BK-H 060 · BK 030 (76)",
         summary="Compact rotary draw benders for tube, pipe, solid bar, flat bar and box section — one tooling set included. The "
                 "BK-42 and BK 030 (76) have touchscreen NC (PLC) programming with 20 programs of 10 bends, quick-change tooling "
                 "and a digital angle display; the BK-050 and hydraulic BK-H 060 use a one-touch control any operator can "
                 "program, with two bending speeds and a foot pedal. From 1-1/4″ NPS pipe on the BK-42 to Ø3″ × 11 ga steel "
                 "tube on the BK 030 — the bench of handrail, gate, fence and furniture shops.",
         features=["BK-42 and BK 030 (76): touchscreen programming of bend angle, multilingual diagnostics, 20 programs of 10 lines with NC (PLC) control, quick-change tooling, sequential bends with high repeatability, digital display of bend angle",
                   "BK-050 and BK-H 060: one-touch control — any operator can program and store bend angles; two bending speeds; bend from the control panel or the foot pedal",
                   "BK-H 060: hydraulic, draws the tube from one direction for easier sequential bending; one-piece solid bronze counter-bend die, swiveling bend head, angle indicator, 0–210°",
                   "Foot-pedal control for hands-free operation; mobile on rollers with handle; compact design", "1 tooling set (bend die, clamp die, counter die) in requested size; CE certified"],
         optional=["Additional tooling for other diameters and profiles", VOLT],
         images=["is-bk-050", "is-bk-42", "is-bk-h060", "is-bk-030", "is-bk-screen", "is-bk-panel", "is-bk-tooling", "is-bk-part"],
         videos=[], specs=t_bk(),
         headline="1/8″ to 2-1/2″ NPS pipe · Ø3″ × 11 ga steel tube · touchscreen NC or one-touch control"),
]

VOLT_FAQ = {"q": "What voltage do the benders run on?",
            "a": "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel; 208 V, 240 V and 480 V 3-phase are available on request, and 240 V single-phase on the BK-42 and other models whose main motor is 2.2 kW (3 HP) or less — a machine with a motor above 2.2 kW must run on three-phase power and cannot be converted to 240 V single-phase."}

TOOLING_FAQ = {"q": "What do you need from me to quote tooling?",
               "a": "Six things: material type, tube or profile size, wall thickness, the smallest centreline radius (CLR) you bend, the maximum bend angle and the maximum tube length. Every bender comes with one die set in the size you request; extra sets, ball mandrels and wiper dies are quoted from the same list."}

def _faq(faqs, *questions):
    return [next(f for f in faqs if f["q"] == q) for q in questions]


CSM_FAQ = CSM.PAGE_BEND["faq"]
TT_TUBE_FAQ = [  # from the former value-line tube-bender page (tools/ttmc_more_pages.py)
    {"q": "Rotary-draw, push-type or roll bending?", "a": "A rotary-draw bender (JTB, TBM-60, HTB-25T, TB-3, HTB-1000) pulls the tube around a die with a clamp and a follower — a tight, accurate bend with little flattening, the method for roll cages, railings, frames and exhaust. A push-type hydraulic pipe bender (EHB-10) pushes the pipe into a die between two supports — simple and fast for plumbing and electrical pipe, where some ovality is acceptable. For large radii, rings and spirals, see the tube rollers on the angle rolls page."},
    {"q": "What do I need to tell you to choose the dies?", "a": "The outside diameter (or the square size), the wall thickness, the material and the centre-line radius (CLR) of the bend — usually 2 to 4 times the tube diameter. Tube and pipe sizes differ: 1-1/2″ schedule 40 pipe is 1.900″ OD, while 1-1/2″ tube is 1.500″ OD — the die must fit the OD exactly."},
]

PAGES = {
    P_CNC: dict(
        title="CNC Tube Benders for Sale in Canada — CNC Mandrel Tube & Pipe Benders to Ø8-5/8″ | NovoTech",
        meta="CNC tube benders sold, installed and supported in Canada: CSM all-electric, electric-hybrid and hydraulic CNC mandrel benders from Ø15/32″ to Ø8-5/8″, and ISITAN SFB 3- and 5-axis servo CNC mandrel benders from Ø1-1/2″ to Ø3-1/2″ with 3D simulation.",
        h1="CNC tube benders — CNC mandrel benders, all-electric, hybrid and hydraulic, Ø15/32″ to Ø8-5/8″",
        intro="A CNC tube bender feeds, rotates and bends the tube from a program, so a part with ten bends in different planes comes off "
              "the machine the same every time; a mandrel inside the tube and a wiper die keep thin walls round at tight radii. NovoTech sells "
              "two makers' CNC mandrel benders in Canada, all on this page, small to large: CSM of Tainan, Taiwan — the EMB / EMR all-electric "
              "benders that switch between left- and right-hand bending within one part, from Ø19/32″ brake and fuel line to Ø3″, and the "
              "all-electric MRE2-RBE to Ø4″; the TBRE / TMRE / TSRE / TDRE and MBE / MRE electric hybrids from Ø15/32″ to Ø6″ with one to "
              "three stacked tools and roll-bending heads; and the TSR / TDR hydraulic CNC pipe benders to Ø8-5/8″ — then ISITAN of Bursa, "
              "Turkey: the five-axis SFB CNC/A5 with servo roll-bending for large sweeps, Ø1-1/2″ to Ø2-1/2″, and the SFB CNC/A3 in five "
              "sizes from Ø1-1/2″ tube to Ø3-1/2″ × 8 ga pipe, both with a 21″ touchscreen CNC, 3D simulation and spring-back "
              "compensation. Each family below has its full specification table and photos. Every machine comes with a CSA-approved panel, "
              "tooling, installation and training, supported from Mississauga, ON, Canada. NC mandrel benders, which program the bend "
              "angles while the tube is fed by hand or by a carrier, are on the NC page.",
        points=["CSM all-electric EMB / EMR and MRE2-RBE Ø19/32″ – Ø4″ · electric hybrid TBRE / TDRE and MBE / MRE Ø15/32″ – Ø6″, 1 – 3 stacked tools",
                "CSM TSR / TDR hydraulic CNC pipe benders to Ø8-5/8″ pipe on 20 ft mandrels",
                "ISITAN SFB CNC/A5 and CNC/A3: Ø1-1/2″ × 11 ga to Ø3-1/2″ × 8 ga, 3 or 5 servo axes, 21″ touchscreen CNC with 3D simulation"],
        hero="cs-emr", minis=["cs-tsr", "is-sfb-38-cnc-a5"],
        groups=[CSM.PAGE_BEND["groups"][0], CSM.PAGE_BEND["groups"][1],
                ("cnc", "ISITAN premium line — SFB CNC mandrel benders", "Five-axis A5 with servo roll bending, and the three-axis A3 production line-up.", "isitan")],
        faq=_faq(CSM_FAQ, "All-electric, electric-hybrid or hydraulic?", "How many stacked tools do I need, and what is roll bending?", "What does a rear booster do?", "Can the bender be automated?", "How do I read a CSM model name?")
            + [{"q": "3-axis or 5-axis?", "a": "Both ISITAN CNC benders have servo feed (Y), rotation (B) and bend (C). The A5 adds two servo roll-bending axes, so one machine can draw-bend tight radii around the mandrel and roll-bend large-radius sweeps — handrail returns, roll cages, furniture arcs — without changing machines or tooling. If every bend in your parts is a tight radius, the A3 does the job."},
               {"q": "Does it bend without a mandrel too?", "a": "Yes — every SFB CNC bends with or without the mandrel, selected in the program. Thick-wall tube and generous radii bend without; thin-wall tube and tight radii need the mandrel (and often a wiper die) to stop wrinkling and collapse."},
               {"q": "Can I program from a drawing?", "a": "The CNC takes X-Y-Z coordinates from the part drawing and converts them to Y-B-C bender data (feed, rotation, bend), simulates the sequence in 3D with collision warning, and estimates the tube length and cycle time before you bend the first part."}]
            + _faq(CSM_FAQ, "CSM or ISITAN?") + [TOOLING_FAQ, VOLT_FAQ],
        faq_title="Questions we get asked about CNC tube benders",
    ),
    P_NC: dict(
        title="NC Mandrel Benders for Sale in Canada — NC Mandrel Pipe & Tube Benders to Ø8-5/8″ | NovoTech",
        meta="NC mandrel benders sold, installed and supported in Canada: ISITAN SFB NC and NC/C hydraulic mandrel benders with 10″ touchscreen NC from Ø1-1/4″ to Ø3-1/2″, compact and aluminum-profile benders, and CSM symmetric, TSRJ / TDRJ, TNCPB and TNCB NC hydraulic benders to Ø8-5/8″ pipe.",
        h1="NC mandrel benders — NC tube and pipe benders, Ø1-1/4″ to Ø8-5/8″",
        intro="An NC mandrel bender is a hydraulic bender whose bend angles are stored in a numeric control: the operator feeds and rotates "
              "the tube to a stop — or a servo carrier does it — and the machine bends each angle to the programmed value, with a mandrel "
              "inside the tube for thin walls and tight radii. NovoTech sells two makers' NC benders in Canada, all on this page, small to "
              "large: ISITAN of Bursa, Turkey — the compact SFB 32 benders for Ø1-1/4″ tube, the SFB 38-NC/A benders for aluminum window and "
              "door profiles, the SFB NC/C with a servo-rotation carrier and hydraulic collet for series production and the SFB NC in five "
              "sizes from Ø1-1/2″ × 11 ga to Ø3-1/2″ × 8 ga with 100 programs of 20 bends; then CSM of Tainan, Taiwan — the two-head F38 / "
              "F50 symmetric benders that bend both ends of a tube at once, the TSRJ / TDRJ with servo feed and rotation and the TNCPB with "
              "manual feed to Ø4″, and the single-axis TNCB NC hydraulic pipe benders to Ø8-5/8″. Each family below has its full "
              "specification table and photos. The pipe bender most exhaust, handrail, furniture and fabrication shops in Canada actually "
              "need — mandrel bending with programmed angles, without the price of a full CNC; CSA-approved panels and support from "
              "Mississauga, ON, Canada.",
        points=["ISITAN SFB 32 compact Ø1-1/4″ · SFB 38-NC/A aluminum-profile benders · SFB NC/C carrier and SFB NC Ø1-1/2″ × 11 ga to Ø3-1/2″ × 8 ga",
                "10″ touchscreen NC · 100 programs × 20 bends · hydraulic mandrel, clamping and pressure die · up to 15.1 ft feed",
                "CSM F38 / F50 symmetric benders · TSRJ / TDRJ and TNCPB NC benders to Ø4″ · TNCB NC pipe benders to Ø8-5/8″"],
        hero="is-sfb-90-nc", minis=["is-sfb-51-nc-c", "cs-tncb"],
        groups=[("compact", "ISITAN premium line — compact and aluminum-profile benders", "SFB 32 benders for Ø1-1/4″ tube and SFB 38-NC/A profile benders.", "isitan"),
                ("nc", "ISITAN premium line — SFB NC mandrel benders", "The NC/C with servo-rotation carrier and the standard SFB NC.", "isitan"),
                CSM.PAGE_BEND["groups"][3], CSM.PAGE_BEND["groups"][2]],
        faq=[{"q": "What is the difference between the SFB NC and the SFB NC/C?", "a": "On the SFB NC the operator feeds and rotates the tube by hand to the gauge bracket and the NC controls the bend angle. The NC/C adds a carrier with a hydraulic collet and a servo rotation axis: feed to the carrier's adjustable stops, the servo turns the tube to the programmed angle between bends, and the carrier screen shows feed and rotation. For parts with several bends in different planes it is faster and far more repeatable."},
             {"q": "NC or CNC?", "a": "An NC bender programs the bend angles; the operator handles feed and rotation (servo rotation on the NC/C, servo feed and rotation on the CSM TSRJ / TDRJ). A CNC bender drives all three axes with servos from a drawing. If you bend hundreds of the same multi-plane part a shift, see our CNC tube benders; for mixed work, exhaust, handrails and furniture, an NC bender pays back faster."},
             {"q": "What about the mandrel — when do I need it?", "a": "Thin-wall tube bent to a tight radius (CLR under about 2× the diameter) wrinkles on the inside and flattens on the outside without support. The mandrel supports the tube from inside; every SFB has a hydraulic mandrel and bends with or without it, and a wiper die and ball mandrel are available for the thinnest walls."},
             TOOLING_FAQ, VOLT_FAQ],
        faq_title="Questions we get asked about NC mandrel benders",
    ),
    P_BK: dict(
        title="Hydraulic Pipe Benders & Rotary Draw Benders for Sale in Canada — to Ø3-1/8″ | NovoTech",
        meta="Hydraulic and rotary draw pipe benders sold, installed and supported in Canada: ISITAN BK rotary draw benders, premium-line TB 34 / TB 42 and SPB 60 / 76 pipe benders, and NovoTech value-line hydraulic, electric and air-hydraulic tube and pipe benders to Ø3-1/8″.",
        h1="Hydraulic and rotary draw pipe benders — non-mandrel benders for pipe, tube and bar to Ø3-1/8″",
        intro="A rotary draw bender clamps the tube to a rotating bend die and draws it around the die radius without an internal mandrel, and "
              "a hydraulic pipe bender bends pipe around a die with a hydraulic ram — the simplest machines for handrail, gate, fence, "
              "furniture, plumbing, exhaust and repair bends in pipe, tube and bar. NovoTech sells three lines in Canada, all on this page: "
              "ISITAN's BK series, four rotary draw benders from the 1 HP BK-42 for 1-1/4″ pipe to the BK 030 (76) for Ø3″ × 11 ga steel "
              "tube, bending pipe, tube, solid and flat bar and box section with one included tooling set; NovoTech's premium line, built in "
              "Turkey — the TB 34 electric bench bender for 1″ NPS pipe, the 17-ton hydraulic TB 42 for 1-1/4″ NPS pipe and the SPB 60 and "
              "SPB 76 NC draw benders with a 500-program memory for Ø2-3/8″ and Ø3″ pipe; and NovoTech's value line, built in China — the "
              "EHB-10 electric hydraulic pipe bender and the TB-3 and HTB-1000 benders for 2″ schedule 40 pipe, the HTB-25T 25-ton tubing "
              "bender and the TBM-60 electric bender to 2-1/2″, the HTB-2000 exhaust bender with an expander-swager and the JTB hydraulic PLC "
              "tube benders to Ø3-1/8″. Each family below has its full specification table and photos. For thin-wall tube to a tight radius, "
              "see the NC and CNC mandrel benders.",
        points=["ISITAN BK rotary draw benders: 1/8″ to 2-1/2″ NPS pipe, Ø3″ × 11 ga steel tube, bar and box section — one tooling set included",
                "NovoTech premium line: TB 34 electric and 17-ton TB 42 hydraulic pipe benders · SPB 60 / SPB 76 NC draw benders with 500 programs",
                "NovoTech value line: EHB-10, TB-3 and HTB-1000 for 2″ pipe · HTB-25T and TBM-60 · HTB-2000 exhaust bender · JTB hydraulic PLC tube benders to Ø3-1/8″"],
        hero="is-bk-050", minis=["tm-jtb50", "tb-tb42"],
        groups=[("bk", "ISITAN premium line — BK rotary draw benders", "Four compact non-mandrel benders from 1 to 3 HP.", "isitan"),
                TB.TB_GROUP,
                ("sahinler-draw", "SPB pipe draw benders", "NC-controlled rotary draw benders for pipe to Ø3″ with a 500-program memory.", "sahinler"),
                ("tt-tube", "Tube and pipe benders · value line", "Hydraulic, electric and air-hydraulic benders for pipe and tube to Ø3-1/8″ — NovoTech value line, built in China.", "novotech")],
        faq=[{"q": "Rotary draw or mandrel bender?", "a": "A rotary draw bender clamps the tube to a bend die and draws it around; without an internal mandrel it suits thicker walls and radii of about 2× the diameter and up — handrail, gate, fence and furniture work. Thin-wall tube to a tight radius needs the mandrel support of an NC or CNC mandrel bender. The BK capacity table lists the maximum tube, bar and box section for each model."},
             {"q": "Which BK for stainless handrail?", "a": "The BK-050 bends Ø2-3/8″ × 14 ga 304/316 stainless tube and the BK-H 060 Ø2-3/8″ × 12 ga — the common 1-1/2″ and 2″ handrail sizes with room to spare. The hydraulic BK-H 060 draws from one direction, which makes sequential bends on long rails easier."},
             {"q": "Does it come with tooling?", "a": "The BK benders come with one set — bend die, clamp die and counter die — in the size you request. Additional sets for other diameters, square tube, flat bar and box section are quoted with the machine; tell us material, size, wall, CLR and angle."},
             {"q": "BK, SPB or TB?", "a": "For the occasional bend in pipe up to 1-1/4″ NPS, the premium-line TB 34 (electric, digital angle stop) or TB 42 (17-ton hydraulic) is the simplest and lowest-cost premium machine. For railing, gate and furniture work in pipe, tube, bar and box section, the ISITAN BK series with its programmable controls and capacity to Ø3″ tube. For repeated multi-bend parts in pipe to Ø2-3/8″ or Ø3″, the SPB 60 or SPB 76 with a 500-program NC. Thin-wall tube to a tight radius needs a mandrel bender."}]
            + [f for f in TT_TUBE_FAQ if f["q"] in ("Rotary-draw, push-type or roll bending?", "What do I need to tell you to choose the dies?")]
            + [VOLT_FAQ],
        faq_title="Questions we get asked about hydraulic and rotary draw pipe benders",
    ),
}

HUB_PAGE = dict(
    title="Pipe Benders & Tube Bending Machines for Sale in Canada — CNC, NC Mandrel, Hydraulic & Rotary Draw | NovoTech",
    meta="Every pipe and tube bender NovoTech sells in Canada, by kind: CNC tube benders (CSM and ISITAN) from Ø15/32″ to Ø8-5/8″, NC mandrel benders to Ø8-5/8″ pipe, and hydraulic and rotary draw pipe benders to Ø3-1/8″ — every model in one table.",
    h1="Pipe benders and tube bending machines — CNC, NC mandrel, hydraulic and rotary draw",
    intro="A pipe bender or tube bending machine draws a tube around a bend die to a set angle; a mandrel bender adds an internal mandrel so thin-wall tube bends to a tight radius without wrinkling or collapsing. NovoTech sells three kinds in Canada, each on its own page: CNC tube benders that feed, rotate and bend from a program — CSM all-electric, electric-hybrid and hydraulic CNC mandrel benders from Ø15/32″ to Ø8-5/8″ and ISITAN SFB 3- and 5-axis servo CNC benders to Ø3-1/2″; NC mandrel benders with programmed bend angles — ISITAN SFB NC, NC/C, compact and aluminum-profile benders and CSM symmetric, TSRJ / TDRJ, TNCPB and TNCB NC benders to Ø8-5/8″ pipe; and hydraulic and rotary draw pipe benders without a mandrel — ISITAN BK, the premium-line TB and SPB benders and NovoTech's value-line hydraulic, electric and air-hydraulic benders to Ø3-1/8″. From a bench bender for 1″ pipe to a 20 ft hydraulic CNC pipe bender for shipyard pipe, every machine is supplied with installation and support from Mississauga, ON, Canada. Below, each page in brief and every model in one capacity table.",
    points=[f"<a href=\"{P_CNC}\">CNC tube benders</a> — CSM all-electric, hybrid and hydraulic and ISITAN servo CNC mandrel benders, Ø15/32″ to Ø8-5/8″",
            f"<a href=\"{P_NC}\">NC mandrel benders</a> — ISITAN SFB NC and NC/C, compact and profile benders, CSM symmetric and NC benders, Ø1-1/4″ to Ø8-5/8″",
            f"<a href=\"{P_BK}\">Hydraulic and rotary draw pipe benders</a> — ISITAN BK, premium-line TB and SPB, value-line benders to Ø3-1/8″"],
    hero="is-sfb-38-cnc-a5", minis=["cs-tbre", "is-bk-050"],
    faq=[{"q": "Pipe bender, tube bender, mandrel bender — what is the difference?", "a": "\"Pipe\" is sized by nominal pipe size (NPS) and schedule, \"tube\" by outside diameter and wall, but the machines are the same: a bend die, a clamp and a pressure die draw the material around the radius. A mandrel bender adds an internal mandrel so thin-wall tube can be bent to a tight radius without wrinkling; the CNC and NC benders on these pages are mandrel benders, the BK, TB, SPB and value-line benders bend without a mandrel. Every capacity on these pages is given as OD × wall in inches and gauge."},
         {"q": "How do I choose a tube bender?", "a": "Start with the largest tube (OD × wall and material), the tightest centreline radius and the number of bends per part — that sets mandrel or not and the model size. Then the volume: a hydraulic or rotary draw bender for occasional bends, an NC mandrel bender for programmed angles with manual feed, a carrier or servo-feed NC for repeatable multi-plane parts, and a CNC when parts come from a drawing in hundreds. Send us a part drawing and we will size the machine and tooling."},
         {"q": "Which tube benders does NovoTech stock?", "a": "We keep the SFB 38-NC and 51-NC and the BK-050 in Mississauga, ON, Canada, and bring CNC models, carrier models and the larger 76 and 90 sizes in to order with their tooling. In-stock machines carry the 7-day money-back guarantee. CSM benders are quoted with the tooling for your part drawings."},
         _faq(CSM_FAQ, "CSM or ISITAN?")[0],
         {"q": "Do you install tube benders and train operators?", "a": "Yes — our technicians commission the bender anywhere in Canada, set up the first tooling, prove out your part and train operators on the NC or CNC. Remote assistance over the network is built into the CNC models, and we support every machine by video call."},
         TOOLING_FAQ, VOLT_FAQ],
    range_lead="Maximum tube (OD × wall in mild steel), centreline radius, working length, control and weight for every model. Each row links to the full specification table of its series.",
    range_cols=["Max. tube (OD × wall)", "Max. CLR", "Working length", "Control", "Weight"],
    range_caption="Tube and pipe benders supplied by NovoTech — CSM, ISITAN, the NovoTech premium line and the value line — capacities for mild steel tube",
    range_note="Tube capacities are for mild steel; stainless, aluminum, bar and box-section capacities for the BK series are on the hydraulic and rotary draw page. CLR = centreline radius (the largest die radius). Working length is the maximum feed with the standard mandrel rod (extended mandrels to 20 ft are optional on SFB models); for the CSM symmetric benders it is the span between the two bends. Weights for the CSM benders are quoted with the configuration.",
)
SUBPAGE_META = {
    P_CNC: ("CNC tube benders", "cs-emr", "CSM all-electric, electric-hybrid and hydraulic CNC mandrel benders from Ø15/32″ to Ø8-5/8″, then ISITAN SFB 3- and 5-axis servo CNC benders to Ø3-1/2″ with 3D simulation.", "CNC tube benders"),
    P_NC: ("NC mandrel benders", "is-sfb-90-nc", "ISITAN SFB NC, NC/C, compact and aluminum-profile benders with 10″ touchscreen NC, then CSM symmetric, TSRJ / TDRJ, TNCPB and TNCB NC benders to Ø8-5/8″ pipe.", "NC mandrel benders"),
    P_BK: ("Hydraulic and rotary draw pipe benders", "is-bk-050", "ISITAN BK rotary draw benders, premium-line TB 34 / TB 42 and SPB 60 / 76 pipe benders, and NovoTech value-line hydraulic, electric and air-hydraulic benders to Ø3-1/8″.", "Hydraulic & rotary draw benders"),
}
ORDER = [P_CNC, P_NC, P_BK]

# the CSM line page is gone: CNC models to the CNC page, NC and symmetric models to the NC page
CSM_PAGE = {"csm-electric": P_CNC, "csm-hydraulic": P_CNC, "csm-nc": P_NC, "csm-symmetric": P_NC}
# page order, each group from the smallest machine to the largest (the owner, Nov 7 2026)
FAMILY_ORDER = ["csm-emr", "csm-tbre", "csm-mbe", "csm-tsr", "isitan-sfb-cnc-a5", "isitan-sfb-cnc-a3",
                "isitan-sfb-32", "isitan-sfb-38-nc-a", "isitan-sfb-nc-c", "isitan-sfb-nc", "csm-f38", "csm-tsrj", "csm-tncb",
                "isitan-bk", "tubend-tb34", "tubend-tb42", "sahinler-spb", "tt-hb-pipe", "tt-tb3", "tt-tbm60", "tt-exhaust", "tt-jtb"]
# … and the photos: the smallest model first, details and parts after
IMAGE_ORDER = {
    "csm-emr": ["cs-emr-15", "cs-emr-45", "cs-emr", "cs-mre2-50", "cs-emr-75", "cs-mre2", "cs-mre2-100", "cs-emr-parts-small", "cs-emr-parts-mid",
                "cs-mre2-parts", "cs-emr-parts-large", "cs-mre2-parts-large"],
    "csm-mbe": ["cs-mbe", "cs-mbe-parts-2", "cs-mbe-parts"],
    "csm-tbre": ["cs-tbre", "cs-tdre", "cs-tdre-parts-2", "cs-tbre-parts", "cs-tbre-parts-2", "cs-tdre-parts"],
    "csm-tsr": ["cs-tsr", "cs-tsr-parts-2", "cs-tsr-parts-3", "cs-tsr-parts"],
    "csm-tncb": ["cs-tncb", "cs-tncb-parts-2", "cs-tncb-parts"],
    "csm-f38": ["cs-f38", "cs-f38h"],
    "isitan-sfb-cnc-a3": ["is-sfb-38-cnc", "is-sfb-51-cnc", "is-sfb-76-cnc", "is-sfb-90-cnc", "is-sfb-38-cnc-rear"],
    "isitan-sfb-nc-c": ["is-sfb-38-nc-c", "is-sfb-51-nc-c", "is-sfb-90-nc-c", "is-sfb-nc-c-carrier", "is-sfb-nc-c-servo"],
    "isitan-sfb-nc": ["is-sfb-38-nc", "is-sfb-51-nc", "is-sfb-65-nc", "is-sfb-76-nc", "is-sfb-38-nc-carrier", "is-sfb-nc-reducer", "is-sfb-nc-collet"],
    "isitan-bk": ["is-bk-42", "is-bk-050", "is-bk-h060", "is-bk-030", "is-bk-screen", "is-bk-panel", "is-bk-tooling", "is-bk-part"],
    "sahinler-spb": ["sh-spb60", "sh-spb76", "sh-spb-handrail"],
    "tt-jtb": ["tm-jtb40", "tm-jtb50", "tm-jtb80"],
    "tt-tbm60": ["tm-htb25t", "tm-tbm60", "tm-htb25t-stand", "tm-tbm60-pos"],
    "tt-tb3": ["tm-tb3a", "tm-tb3b", "tm-tb3c", "tm-htb1000"],
}


def all_families():
    fams = {f["id"]: f for f in FAMILIES + SPB_FAMILIES + TB.families(P_BK)}
    for f in CSM.families(P_CSM):
        fams[f["id"]] = dict(f, page=CSM_PAGE[f["group"]])
    for f in TT.TUBE:
        fams[f["id"]] = dict(f, page=P_BK, group="tt-tube")
    out = []
    for fid in FAMILY_ORDER:
        f = fams.pop(fid)
        if fid in IMAGE_ORDER:
            if sorted(IMAGE_ORDER[fid]) != sorted(f["images"]):
                raise SystemExit(f"pipe benders: the photo order of {fid} does not list its photos: {f['images']}")
            f = dict(f, images=IMAGE_ORDER[fid])
        out.append(f)
    if fams:
        raise SystemExit(f"pipe benders: families with no place in FAMILY_ORDER: {sorted(fams)}")
    return out


ALL_FAMILIES = all_families()


def build():
    write_families(SET, ALL_FAMILIES)
    sib = [(s, SUBPAGE_META[s][3], SUBPAGE_META[s][0]) for s in ORDER]
    hub = {"slug": HUB, "label": "All pipe & tube benders", "image": "is-sfb-38-cnc-a5",
           "blurb": "Every pipe and tube bender NovoTech sells in Canada — CNC, NC mandrel, hydraulic and rotary draw."}
    related = [{"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "tube-end-forming-machines.html", "label": "Tube end forming machines"}, {"href": "circular-cold-saws.html", "label": "Circular cold saws"}]
    extras = {
        P_CNC: {"catalogue_pdf": None, "catalogue_pdfs": [CSM.pdf("csm-emr"), CSM.pdf("csm-tsr"), PDF], **CSM.INTRO_VIDEO,
                "hero_brand_line": "CSM benders are made in Taiwan by Chiao Sheng Machinery and ISITAN benders in Turkey by ISITAN Makine. All sold, installed and supported in Canada by NovoTech.",
                "origin_feature": {"title": "Made in Taiwan and Turkey", "text": "CSM has built tube benders in Tainan since 1982 and CNC benders since 1989, with 24 international design patents; ISITAN has built tube and sheet-metal machinery in Bursa since 1959 — CE-certified machines, installed and supported by NovoTech in Canada."}},
        P_NC: {"catalogue_pdf": None, "catalogue_pdfs": [PDF, CSM.pdf("csm-tsr")],
               "hero_brand_line": "ISITAN benders are made in Turkey by ISITAN Makine and CSM benders in Taiwan by Chiao Sheng Machinery. All sold, installed and supported in Canada by NovoTech.",
               "origin_feature": {"title": "Made in Turkey and Taiwan", "text": "ISITAN has built tube and sheet-metal machinery in Bursa since 1959; CSM has built tube benders in Tainan since 1982 — CE-certified machines, installed and supported by NovoTech in Canada."}},
        P_BK: {"catalogue_pdf": None, "catalogue_pdfs": [p for p in (PDF, premium_pdf("premium-sheet-metal"), TB.pdf()) if p],
               "hero_brand_line": "ISITAN BK benders are made in Turkey by ISITAN Makine, since 1959; the SPB draw benders and TB pipe benders are NovoTech's premium line, built in Turkey to NovoTech's specification; NovoTech's value-line benders are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech.",
               "origin_feature": {"title": "Made in Turkey — ISITAN and the NovoTech premium line", "text": "ISITAN has built sheet-metal machinery in Bursa since 1959, and NovoTech's premium-line draw benders, pipe benders and horizontal presses are built in Turkey to our specification — CE-certified machines with European components."}},
    }
    for slug in ORDER:
        write_category(slug, {**PAGES[slug], "related_pages": related}, ALL_FAMILIES, SET, SECTION, hub=hub, siblings=sib,
                       extra={**extras[slug], "nav_label": SUBPAGE_META[slug][3]})
    write_hub(HUB, {**HUB_PAGE, "artifact_title": "Pipe Benders & Tube Bending Machines", "faq_title": "Questions we get asked about pipe benders", "nav_label": "All pipe & tube benders", "related_blurb": hub["blurb"]},
              ALL_FAMILIES, SET, SECTION, [(s, SUBPAGE_META[s][0], SUBPAGE_META[s][1], SUBPAGE_META[s][2], SUBPAGE_META[s][3]) for s in ORDER],
              extra={"catalogue_pdf": None, "catalogue_pdfs": [p for p in (CSM.pdf("csm-emr"), CSM.pdf("csm-tsr"), PDF, premium_pdf("premium-sheet-metal")) if p],
                     "range_pick": [["capacity", "round_tube", "pipe_dies"], ["clr", "radius", "min_radius"], "working_length", ["control", "drive"], "weight"],
                     "hero_brand_line": "CSM benders are made in Taiwan by Chiao Sheng Machinery and ISITAN benders in Turkey by ISITAN Makine; the SPB draw benders and TB pipe benders are NovoTech's premium line, made in Turkey, and the value-line benders are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech.",
                     "origin_feature": {"title": "Two bender makers and two NovoTech lines, one supplier", "text": "CSM (Taiwan, CNC benders since 1989), ISITAN (Turkey, since 1959) and NovoTech's premium and value lines — every machine installed and supported from Mississauga, ON, Canada."},
                     "related_pages": [{"href": f"{s}.html", "label": SUBPAGE_META[s][0]} for s in ORDER] + related + [{"href": "wire-bending-machines.html", "label": "CNC wire bending machines"}]})
    return IMAGES
