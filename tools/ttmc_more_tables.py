#!/usr/bin/env python3
"""Spec tables of the NovoTech value-line machines built by TTMC — transcribed from the supplier's Vol. 23 catalogue
(/mnt/user-data/uploads/Catalog_TTMC_Vol23.pdf; PDF page N holds catalogue pages 2N-5 and 2N-4).  Metric as printed,
converted by tools/ttmc_conv.py.  TAB[family id] = [table, …]; CAT[family id] = the catalogue's feature bullets (source notes
for the copy in tools/ttmc_more_data.py, not shown on the site as they are).
"""
from ttmc_conv import D, F, L, R, table


def A(fn, *vals):
    """one cell with several angles: A(D, 120, 115, 95) -> 'Ø4-3/4″ (120 mm) / Ø4-1/2″ (115 mm) / …'"""
    return " / ".join(fn(v) for v in vals)

TAB, CAT = {}, {}
NOTE_50HZ = "rated at 50 Hz"

# ------------------------------------------------------------------------------------------------ circular & abrasive saws
# PDF p18 (catalogue 031 – 032)
TAB["tt-cs"] = [
    table("CS-225 · CS-250 · CS-275", "Bench and stand cold saws, 9 – 11″ blade", ["CS-225", "CS-250", "CS-275"], [
        ("*Blade diameter, max", "L", [225, 250, 275]),
        ("*Round, 90°", "D", [60, 60, 70]),
        ("Rectangular, 90°", "R", [(50, 50), (75, 45), (90, 45)]),
        ("Round, 45°", "D", [52, 55, 65]),
        ("Rectangular, 45°", "R", [(50, 50), (55, 45), (70, 45)]),
        ("*Blade speed", NOTE_50HZ, "RPM", [46, 42, 42]),
        ("Vise opening", "L", [70, 100, 100]),
        ("*Motor", "KW", [0.75, 1.1, 1.1]),
        ("Drive", "TXT", "Gear"),
        ("Packing size L × W × H", "PK", [(71, 50, 62), [("body", (86, 58, 77)), ("stand", (78, 47, 33))], [("body", (86, 58, 78)), ("stand", (78, 47, 33))]]),
        ("*Weight", "KG", [63, 143, 148]),
    ]),
    table("CS-315 · CS-350", "Cold saws on stand, 12 – 14″ blade, two speeds", ["CS-315", "CS-350"], [
        ("*Blade diameter, max", "L", [315, 350]),
        ("*Round, 90°", "D", [100, 120]),
        ("Rectangular, 90°", "R", [(140, 90), (140, 100)]),
        ("Round, 45°", "D", [90, 105]),
        ("Rectangular, 45°", "R", [(100, 90), (100, 100)]),
        ("*Blade speed", NOTE_50HZ, "RPM", [(18, 36), (18, 36)]),
        ("Vise opening", "L", [145, 145]),
        ("*Motor", "TXT", "1 / 1.7 HP (0.75 / 1.3 kW) two-speed, 3-phase · 1.5 HP (1.1 kW) 1-phase"),
        ("Drive", "TXT", "Gear"),
        ("Packing size L × W × H", "PK", [[("body", (98, 62, 93)), ("stand", (78, 60, 50))], [("body", (98, 62, 95)), ("stand", (78, 60, 50))]]),
        ("*Weight", "KG", [227, 236]),
    ]),
]
CAT["tt-cs"] = ["CS-225/250/275: vice with anti-burr device; 24 V low-voltage hold-to-run control knob; head swivels 45° right and left; reduction unit in oil bath",
                "CS-315/350: easy manual press; quick-adjusting vise, the saw frame swivels for angle cuts; two blade speeds; double vise"]

# PDF p19 (033 – 034)
TAB["tt-pds315h"] = [
    table("PDS-315H", "Semi-automatic hydraulic cold saw, 12-1/2″ blade", ["PDS-315H"], [
        ("*Blade diameter, max", "L", [315]),
        ("*Round pipe, 90° / 45°", "TXT", [A(D, 90, 80)]),
        ("Rectangular pipe, 90° / 45°", "TXT", [A(R, (80, 80), (60, 60))]),
        ("*Motor", "TXT", ["3 / 4 HP (2.2 / 3 kW), two-speed"]),
        ("*Blade speed", NOTE_50HZ, "RPM", [(60, 120)]),
        ("Feed cylinder stroke", "TXT", [L(130) + ", max. 1,450 psi (10 MPa)"]),
        ("Clamping cylinder stroke", "L", [10]),
        ("Hydraulic power unit", "TXT", ["1 HP (750 W), 24 V DC control, 435 psi (3 MPa)"]),
        ("Drive", "TXT", "Gear"),
        ("Packing size L × W × H", "PK", [(146, 75, 166)]),
        ("*Weight", "KG", [460]),
    ]),
]
CAT["tt-pds315h"] = ["max blade 315 mm; saw frame swivels ±45°; coolant system; two blade speeds; double vise; auto cutting, hydraulic clamping"]

TAB["tt-pds400"] = [
    table("PDS-400", "Heavy-duty cold saw, 16″ blade", ["PDS-400"], [
        ("*Blade diameter, max", "L", [400]),
        ("*Round pipe, 90° / 45° / 60°", "TXT", [A(D, 120, 115, 95)]),
        ("Rectangular pipe, 90° / 45° / 60°", "TXT", [A(R, (110, 110), (105, 105), (75, 75))]),
        ("Channel, 90° / 45° / 60°", "TXT", [A(R, (150, 75), (100, 50), (75, 40))]),
        ("Angle, 90° / 45° / 60°", "TXT", [A(R, (115, 115), (100, 100), (70, 70))]),
        ("Round bar, 90° / 45° / 60°", "TXT", [A(D, 65, 65, 55)]),
        ("Flat bar, 90° / 45° / 60°", "TXT", [A(R, (150, 75), (100, 50), (70, 50))]),
        ("*Motor", "TXT", ["3 / 3.75 HP (2.2 / 2.8 kW), two-speed"]),
        ("*Blade speed", NOTE_50HZ, "RPM", [(20, 40)]),
        ("Drive", "TXT", "Gear"),
        ("Packing size L × W × H", "PK", [(110, 91, 162)]),
        ("*Weight", "KG", [362]),
    ]),
]
CAT["tt-pds400"] = ["heavy duty; compact design, easy operation; max blade 400 mm; electric power control; manual vise feeding; two blade speeds; head swivels right 60°, left 45°"]

# PDF p20 (035 – 036)
TAB["tt-qcs400"] = [
    table("QCS-400 · QCS-400A", "Aluminum saws with pneumatic clamping and feed, 16″ blade", ["QCS-400", "QCS-400A"], [
        ("*Blade diameter, max", "L", [400, 400]),
        ("*Round, 90° and 45°", "D", [105, 105]),
        ("*Rectangular, 90° and 45° left and right", "R", [(200, 80), (200, 80)]),
        ("*Blade speed", NOTE_50HZ, "RPM", [2800, 2800]),
        ("*Motor", "KW", [1.1, 1.1]),
        ("Drive", "TXT", "Belt"),
        ("Packing size L × W × H", "PK", [(86, 78, 141), (97, 97, 150)]),
        ("*Weight", "KG", [130, 252]),
    ]),
]
CAT["tt-qcs400"] = ["blade swivels ±45°; fast pneumatic clamping vise; pneumatic cylinder for controlled descent; for cutting aluminum alloy"]

TAB["tt-tv"] = [
    table("TV-300 · TV-350 · TV-400", "Abrasive cut-off saws on stand, 12 – 16″ wheel", ["TV-300", "TV-350", "TV-400"], [
        ("*Wheel diameter, max", "L", [300, 350, 400]),
        ("*Round, 90°", "D", [100, 120, 140]),
        ("Rectangular, 90°", "R", [(70, 120), (80, 120), (90, 120)]),
        ("Round, 45°", "D", [90, 105, 120]),
        ("Rectangular, 45°", "R", [(70, 90), (90, 100), (90, 110)]),
        ("*Wheel speed", NOTE_50HZ, "RPM", [5400, 4300, 3200]),
        ("Vise opening", "L", [190, 190, 220]),
        ("*Motor", "KW", [4.0, 4.0, 5.5]),
        ("Drive", "TXT", "Belt"),
        ("Packing size L × W × H", "PK", [[("body", (87, 57, 86)), ("stand", (60, 50, 77))], [("body", (86, 64, 92)), ("stand", (60, 50, 77))],
                                          [("body", (112, 76, 103)), ("stand", (80, 64, 57))]]),
        ("*Weight", "KG", [140, 145, 162]),
    ]),
    table("SQ-40-1", "Portable abrasive cut-off saw, 16″ wheel", ["SQ-40-1"], [
        ("*Wheel diameter, max", "TXT", ["16″ × 1/8″ × 1″ bore (405 × 3 × 25.4 / 32 mm)"]),
        ("*Round, 90°", "D", [140]),
        ("*Wheel speed", "RPM", [2242]),
        ("*Motor", "KW", [2.2]),
        ("Packing size L × W × H", "PK", [(90, 52, 70)]),
        ("*Weight", "KG", [90]),
    ]),
]
CAT["tt-tv"] = ["TV: vise with anti-burr device; 24 V low-voltage hold-to-run control knob; abrasive cutting wheel; for round, special pipe, angle and flat steel — construction, metal, petrochemical, plumbing and electrical installation",
                "SQ-40-1: portable, on wheels; 2242 rpm; 405 mm wheel"]

# ------------------------------------------------------------------------------------------------ belt grinders
# PDF p21 (037 – 038)
TAB["tt-s50"] = [
    table("S-50 · S-50B", "Compact belt grinders, 2″ and 3″ belt", ["S-50", "S-50B"], [
        ("*Motor", "KW", [0.75, 0.75]),
        ("Contact wheel", "WHEEL", [(75, 50), (100, 75)]),
        ("*Belt size", "BELT", [(1000, 50), (1750, 75)]),
        ("*Belt speed", "MS", [22, 13]),
        ("Packing size L × W × H", "PK", [(54, 44, 42), (80, 50, 58)]),
        ("*Weight", "KG", [25, 50]),
    ]),
]
CAT["tt-s50"] = ["S-50: belt grinder and disc sander in one; small and easy to carry", "S-50B: compact machine with great working potential — grinds, cleans, brushes and deburrs the edges of all kinds of parts; optional stand"]

TAB["tt-s75"] = [
    table("S-75 · S-150 · S-150A", "Heavy-duty belt grinders on pedestal, 3″ and 6″ belt", ["S-75", "S-150", "S-150A"], [
        ("*Motor", "TXT", ["4 HP (3 kW) output", "3 / 3.75 HP (2.2 / 2.8 kW), two-speed", "4 HP (3 kW) output"]),
        ("Contact wheel", "WHEEL", [(200, 75), (250, 150), (200, 150)]),
        ("*Belt size", "BELT", [(2000, 75), (2000, 150), (2000, 150)]),
        ("*Belt speed", "MS", [34, (17, 34), 34]),
        ("Packing size L × W × H", "PK", [(115, 56, 54), (114, 63, 65), (114, 63, 65)]),
        ("*Weight", "KG", [85, 107, 107]),
    ]),
    table("S-75L · S-150L", "Light-type belt grinders on pedestal, 3″ and 6″ belt", ["S-75L", "S-150L"], [
        ("*Motor", "TXT", ["4 HP (3 kW) input", "4 HP (3 kW) input"]),
        ("Contact wheel", "WHEEL", [(200, 75), (200, 150)]),
        ("*Belt size", "BELT", [(2000, 75), (2000, 150)]),
        ("*Belt speed", "MS", [29, 29]),
        ("Packing size L × W × H", "PK", [(117, 57, 70), (122, 77, 72)]),
        ("*Weight", "KG", [72, 82]),
    ]),
]
CAT["tt-s75"] = ["S-150 heavy duty: high belt speed; vibration-free operation; quick-adjusting belt angle; large sanding surface", "S-75 / S-150A heavy duty; S-75L / S-150L light type"]

TAB["tt-s75f"] = [
    table("S-75F", "Mobile floor belt grinder for weld seams, 3″ belt", ["S-75F"], [
        ("*Motor", "KW", [3.0]),
        ("Contact wheel", "WHEEL", [(200, 75)]),
        ("*Belt size", "BELT", [(2000, 75)]),
        ("*Belt speed", "MS", [34]),
        ("Packing size L × W × H", "PK", [(105, 70, 95)]),
        ("*Weight", "KG", [75]),
    ]),
]
CAT["tt-s75f"] = ["adjustable depth stop; easy and comfortable operation; grinds/polishes workpieces that cannot be moved without major effort; grinding and polishing weld seams on the floor; on wheels with handle"]

# PDF p22 (039 – 040)
TAB["tt-s75h"] = [
    table("S-75HA · S-75HB · S-150HA · S-150HB", "Heavy-duty belt grinders, 5.5 HP, 3″ and 6″ belt — HB with dust collector", ["S-75HA", "S-75HB", "S-150HA", "S-150HB"], [
        ("*Motor", "TXT", "5.5 HP (4 kW), 2,800 rpm"),
        ("Dust collector motor", "TXT", ["—", "3/4 HP (0.55 kW)", "—", "3/4 HP (0.55 kW)"]),
        ("Contact wheel", "WHEEL", [(200, 75), (200, 75), (200, 150), (200, 150)]),
        ("Drive wheel", "WHEEL", [(225, 75), (225, 75), (225, 150), (225, 150)]),
        ("Flat grinding length", "L", [530, 530, 530, 530]),
        ("*Belt size", "BELT", [(2000, 75), (2000, 75), (2000, 150), (2000, 150)]),
        ("*Belt speed", "MS", [33, 33, 33, 33]),
        ("Packing size L × W × H", "PK", [(110, 70, 132)] * 4),
        ("*Weight", "KG", [102, 107, 128, 135]),
    ]),
]
CAT["tt-s75h"] = ["strong, rigid welded steel base; grinding angle adjustable with lock; 4 kW motor output; large flat grinding area for big parts; HB: 0.5 kW dust collector built in; adjustable height; dust drawer on S-75HA"]

TAB["tt-s100"] = [
    table("S-100 · S-220", "Wide-belt grinders: 4″ belt, and 8″ belt for radius grinding and flat sanding", ["S-100", "S-220"], [
        ("*Motor", "KW", [1.1, 3.0]),
        ("Drive wheel", "WHEEL", [(130, 100), (200, 220)]),
        ("Contact wheel", "WHEEL", [(130, 100), (200, 220)]),
        ("*Belt size", "BELT", [(1220, 100), (2000, 200)]),
        ("*Belt speed", "MS", [19, 29]),
        ("Graphite platen pad", "TXT", ["11.8 × 4.7 × 0.06″ (300 × 120 × 1.5 mm)", "19.7 × 8.7 × 0.06″ (500 × 220 × 1.5 mm)"]),
        ("Packing size L × W × H", "PK", [(102, 57, 60), (122, 77, 72)]),
        ("*Weight", "KG", [45, 118]),
    ]),
]
CAT["tt-s100"] = ["S-100: quick-adjusting belt angle; vibration-free operation; high belt speed; large flat sanding area", "S-220: radius grinder and surface sander in one; adjustable working position"]

# PDF p23 (041 – 042) — tube and profile end grinders (pipe notching belt grinders)
ROLLERS = "Contact rollers for 1/2, 3/4, 1, 1-1/4, 1-1/2, 2 and 2-1/2″ pipe (Ø20 – 76 mm)"
TAB["tt-prs"] = [
    table("PRS-76A · PRS-76C · PRS-76", "Tube and profile end grinders, 4″ belt — notch tube ends Ø3/4 – 3″ at 30 – 90°", ["PRS-76A", "PRS-76C", "PRS-76"], [
        ("*Motor", "TXT", ["3 / 3.75 HP (2.2 / 2.8 kW), two-speed", "3 / 3.75 HP (2.2 / 2.8 kW), two-speed, forward and reverse", "4 HP (3 kW)"]),
        ("*Belt size", "BELT", [(2000, 100)] * 3),
        ("*Belt speed", "MS", [(15, 30), (15, 30), 30]),
        ("*Notching angle", "TXT", "30 – 90°"),
        ("Tube diameter", "TXT", ["Ø3/4 – 3″ (20 – 76 mm) with the optional rollers", "Ø3/4 – 3″ (20 – 76 mm) with the optional rollers", "Ø3/4 – 3″ (20 – 76 mm)"]),
        ("Adjustable slide", "R", [(160, 70)] * 3),
        ("Standard contact roller", "D", [28, 28, 28]),
        ("Drive wheel", "D", ["—", "—", 198]),
        ("Graphite platen pad", "TXT", ["—", "—", "15 × 3.9″ (380 × 100 mm)"]),
        ("Packing size L × W × H", "PK", [(137, 62, 66), (137, 62, 66), (130, 56, 46)]),
        ("*Weight", "KG", [160, 158, 168]),
    ]),
    table("PRS-150", "Tube end grinder, 6″ belt — notch tube ends Ø1-3/8 – 5-3/4″, grind flat and on the contact wheel", ["PRS-150"], [
        ("*Motor", "TXT", ["7.5 HP (5.5 kW), two-speed 1,400 / 2,800 rpm, forward and reverse"]),
        ("*Belt size", "BELT", [(2000, 150)]),
        ("*Belt speed", "MS", [(15, 30)]),
        ("*Notching angle", "TXT", ["30 – 90°"]),
        ("Tube diameter", "TXT", ["Ø1-3/8 – 5-3/4″ (35 – 145 mm)"]),
        ("Adjustable slide, horizontal × cross", "R", [(175, 150)]),
        ("Standard contact rollers", "TXT", ["Ø1-1/2″ and Ø4″"]),
        ("Drive wheel", "D", [200]),
        ("Contact wheel", "TXT", ["Ø1-3/8 – 5-3/4″ (35 – 145 mm)"]),
        ("Graphite platen pad", "TXT", ["15.7 × 6.3″ (400 × 160 mm)"]),
        ("Packing size L × W × H", "PK", [(165, 88, 152)]),
        ("*Weight", "KG", [310]),
    ]),
]
CAT["tt-prs"] = ["PRS-76C: vertical and horizontal operation; two-speed motor, forward and reverse; grinds at any angle 30 – 90°; dust collector connection; standard roller Ø28 mm; also sands flat and on the back",
                 "PRS-76A: steady three-leg stand with 8 roller holder sets; two speeds; standard roller Ø28 mm",
                 "PRS-76: easy operation, rotating design; any angle 30 – 90°; any diameter 20 – 76 mm; all major materials; tubes and profiles; standard roller Ø28",
                 "PRS-150: any angle 30 – 90°; any diameter 35 – 145 mm; dust collector connection; standard rollers 1-1/2″ and 4″; tube grinding, surface grinding and wheel grinding in one; two-speed, forward and reverse",
                 "optional special rollers Ø20 (1/2″), 26 (3/4″), 32 (1″), 42 (1-1/4″), 48 (1-1/2″), 60 (2″), 76 mm (2-1/2″)"]

# PDF p24 (043 – 044)
TAB["tt-sdd75"] = [
    table("SDD75", "Multi-purpose belt grinder — flat, contact wheel and tube notching on one arm, 3″ belt", ["SDD75"], [
        ("*Motor", "TXT", ["2 / 3 HP (1.5 / 2.2 kW), two-speed"]),
        ("*Belt size", "BELT", [(2000, 75)]),
        ("*Belt speed", "MS", [(15, 30)]),
        ("*Tube notching", "TXT", ["Ø3/4 – 3″ (20 – 76 mm) with the optional vise and Ø28 mm roller"]),
        ("Packing size L × W × H", "PK", [(81, 74, 102)]),
        ("*Weight", "KG", [110]),
    ]),
]
CAT["tt-sdd75"] = ["three kinds of grinding with one working arm and one belt — change the wheel for the job; easy belt change; standard rubber contact wheel as on a normal belt grinder and adjustable wheel for grinding knives; optional vise with Ø28 mm roller for tube notching (as PRS-76, Ø20 – 76 mm)"]

TAB["tt-bgm50"] = [
    table("BGM-50HV · BGM-50", "2″ and 1-1/2″ belt grinders for knives, tools and pipe notching", ["BGM-50HV", "BGM-50"], [
        ("*Motor", "KW", [1.5, 1.1]),
        ("Contact wheel", "WHEEL", [(87, 50), (180, 38)]),
        ("*Belt size", "BELT", [(1220, 50), (1520, 38)]),
        ("*Belt speed", "TXT", ["Variable, up to 3,543 ft/min (18 m/s)", "Variable (inverter)"]),
        ("Working position", "TXT", ["Horizontal and vertical", "Vertical"]),
        ("Packing size L × W × H", "PK", [(142, 52, 63), (68, 58, 80)]),
        ("*Weight", "KG", [50, 46]),
    ]),
]
CAT["tt-bgm50"] = ["BGM-50HV: fully sealed bearings; sanding disc available; horizontal and vertical working position; five contact wheels 3/4, 1, 1-1/2, 3-1/2 and 8″; polyurethane wheels ground flat for precision finishing; tilts on its side as a bobbin grinder, also great for pipe notching; belts P80 / P100",
                   "BGM-50: variable speed by inverter; cast frame; precision-machined components; belt guard; quick belt change and tracking; cord and switch included; belt P60"]

# PDF p25 (045 – 046)
TAB["tt-s50v"] = [
    table("S-50V · S-75V", "Vertical column belt grinders, 2″ and 3″ belt", ["S-50V", "S-75V"], [
        ("*Motor", "KW", [0.75, 1.1]),
        ("Motor speed", "RPM", [2800, 2800]),
        ("*Belt size", "BELT", [(2000, 50), (2000, 75)]),
        ("*Belt speed", "MS", [22, 26]),
        ("Packing size L × W × H", "PK", [(48, 40, 120), (48, 40, 120)]),
        ("*Weight", "KG", [40, 45]),
    ]),
]
CAT["tt-s50v"] = ["compact belt grinder for metalworking, the economical choice for the workshop; 2/3 less floor space than conventional machines; ready to use, no assembly; quick belt changes; sparks directed for safe work"]

TAB["tt-cmd"] = [
    table("CMD-4 · CMD-80 · DM5 · DM5A", "Edge chamfering machines for 15 – 45° weld preps and deburring", ["CMD-4", "CMD-80", "DM5", "DM5A"], [
        ("*Chamfer size", "TXT", ["0 – 5/32″ (0 – 4 mm)", "0 – 1/4″ (0 – 6 mm)", "0 – 3/16″ (0 – 5 mm)", "0 – 3/16″ (0 – 5 mm)"]),
        ("*Chamfer angle", "TXT", ["15 – 45°", "15 – 45°", "45°", "45°"]),
        ("*Motor", "TXT", ["1/2 HP (0.375 kW)", "1.5 HP (1.1 kW)", "1/2 HP (370 W)", "1/3 HP (250 W)"]),
        ("Motor speed", "TXT", ["2,800 rpm", "2,800 rpm", "0 – 4,300 rpm", "2,800 rpm"]),
        ("Packing size L × W × H", "PK", [(56, 40, 48), (59, 48, 58), (34, 34, 23), (34, 34, 23)]),
        ("*Weight", "KG", [28, 66, 9, 9]),
    ]),
]

TAB["tt-ds12"] = [
    table("DS12 · DS12A · DS12B", "12″ disc sanders", ["DS12", "DS12A", "DS12B"], [
        ("*Disc diameter", "L", [304, 304, 304]),
        ("*Table size", "TXT", ["17.6 × 6.1″ (446 × 156 mm)", "15.7 × 8.9″ (400 × 225 mm), two tables", "15.7 × 8.9″ (400 × 225 mm)"]),
        ("*Motor", "TXT", ["3/4 HP (550 W)", "1 HP (750 W)", "1 HP (750 W)"]),
        ("*Disc speed", "TXT", "1,725 rpm at 60 Hz (1,450 rpm at 50 Hz)"),
        ("Packing size L × W × H", "PK", [(46, 43, 43), (66, 47, 44), (51, 47, 44)]),
        ("*Weight", "KG", [34, 38, 30]),
    ]),
]

# PDF p26 (047 – 048) — disc sanders
TAB["tt-ds20"] = [
    table("TSM300", "12″ disc sander on cabinet stand", ["TSM300"], [
        ("*Disc diameter", "L", [300]),
        ("*Disc speed", "RPM", [1960]),
        ("*Table size", "TXT", ["12 × 16.3″ (305 × 415 mm), tilting, with miter stop"]),
        ("*Motor", "KW", [1.1]),
        ("Packing size L × W × H", "PK", [(52, 54, 127)]),
        ("*Weight", "KG", [90]),
    ]),
    table("DS-20 · DS-20A · DS-20V", "20″ disc sanders for metal: deburr, chamfer weld edges, clean castings", ["DS-20", "DS-20A", "DS-20V"], [
        ("*Disc diameter", "L", [508, 508, 508]),
        ("*Disc speed", "TXT", ["1,100 rpm at 60 Hz (900 rpm at 50 Hz)", "1,100 rpm at 60 Hz (900 rpm at 50 Hz)", "Variable, 500 – 1,800 rpm at 60 Hz (500 – 1,500 rpm at 50 Hz)"]),
        ("*Table tilt", "TXT", ["30° up, 45° down, hand wheel", "30° up, 45° down, hand wheel; table raised and lowered on the column", "45° down"]),
        ("Table size", "TXT", ["—", "—", "25 × 12″ (636 × 305 mm)"]),
        ("Base size", "TXT", ["22 × 22″ (558 × 558 mm)", "22 × 22″ (558 × 558 mm)", "22.8 × 20.5″ (580 × 520 mm)"]),
        ("*Motor", "KW", [1.5, 1.5, 1.5]),
        ("Packing size L × W × H", "PK", [(77, 71, 138), (77, 71, 138), (78, 72, 136)]),
        ("*Weight", "KG", [165, 165, 135]),
    ]),
]
CAT["tt-ds20"] = ["TSM300: optimum speed for wood and metal; balanced disc, vibration-free; rigid steel base; large table with angle adjustment and miter stop (9.5 × 19 mm slot); optional exhaust connector",
                  "DS-20: smooths burrs on metal, chamfers edges for welding, cleans up castings; hand-wheel chamfer adjustment to 45°; heavy-duty column",
                  "DS-20A: whole table moves up and down the column by hand wheel; dust port for any shop vacuum; cast-iron base and table",
                  "DS-20V: variable speed; hand-wheel chamfer to 45°; dust port; stable cabinet base"]

# PDF p27 (049 – 050)
TAB["tt-btm250"] = [
    table("BTM250 · BKM-250", "6″ belt and 10″ disc sander · 6″ belt sander and edge beveller", ["BTM250", "BKM-250"], [
        ("*Belt size", "BELT", [(1220, 150), (1220, 150)]),
        ("*Belt speed", "MS", [8.4, 14.5]),
        ("Belt table", "TXT", ["6 × 10.5″ (152 × 267 mm), tilts to 45°", "7.4 × 14.8″ (188 × 375 mm), tilts 70 – 135°"]),
        ("*Disc", "TXT", ["Ø10″ (250 mm), 2,100 rpm, table 7.5 × 13″ (190 × 330 mm)", "—"]),
        ("*Bevel", "TXT", ["15°", "15 – 45°: max. 1/4″ (6 mm) at 45°, 3/16″ (4.5 mm) at 15°"]),
        ("Min. workpiece length", "TXT", ["—", "3.5″ (90 mm)"]),
        ("*Motor", "KW", [1.1, 1.1]),
        ("Packing size L × W × H", "PK", [(79, 51, 114), (85, 63, 114)]),
        ("*Weight", "KG", [90, 118]),
    ]),
]
CAT["tt-btm250"] = ["BTM250: support tables for disc and belt; quick-lock belt change; belt works horizontal and vertical; dust plates for belt and disc; optional exhaust connector",
                    "BKM-250: bevels ferrous and non-ferrous material; bevel 45° to 15°, easy depth adjustment; removable top cover for sanding contours; optional exhaust connector; miter stop"]

TAB["tt-bg"] = [
    table("BG-8 · BG-10", "Bench grinders, 8″ and 10″", ["BG-8", "BG-10"], [
        ("*Wheel size", "TXT", ["8 × 1″ (200 × 25 mm)", "10 × 1″ (250 × 25 mm)"]),
        ("*Motor", "TXT", ["3/4 HP (550 W)", "1 HP"]),
        ("Arbor", "TXT", ["5/8″ (15.88 mm)", "0.7″ (18 mm)"]),
        ("*Wheel grit", "TXT", ["36 / 60", "46 / 60"]),
        ("Packing size L × W × H", "PK", [(48, 37, 37), (37, 35, 48)]),
        ("*Weight", "KG", [29, 33]),
    ]),
    table("BG-60 · BG-60A", "Wire-wheel deburring and polishing machines, 10″ wheel", ["BG-60", "BG-60A"], [
        ("*Wheel size", "TXT", ["Ø10 × 2-3/8″ (250 × 60 mm), 2″ (50 mm) bore"] * 2),
        ("Steel wire diameter", "TXT", ["0.012″ (0.3 mm)"] * 2),
        ("*Wheel speed", "TXT", ["1,680 / 3,400 rpm at 60 Hz (1,400 / 2,800 at 50 Hz)", "1,680 rpm at 60 Hz (1,400 at 50 Hz)"]),
        ("*Motor", "TXT", ["2 / 3 HP (1.5 / 2.2 kW), two-speed", "3 HP (2.2 kW)"]),
        ("Packing size L × W × H", "PK", [(45, 51, 61), (44, 41, 41)]),
        ("*Weight", "KG", [38, 37]),
    ]),
]
CAT["tt-bg"] = ["BG-8/10: economical; easy operation; heavy-duty cast-iron construction"]

# PDF p28 – p29 (051 – 054)
TAB["tt-sp"] = [
    table("SP-2 · SP-3 · SP-6", "Grinding and polishing machines — belt, disc and wheel on one motor", ["SP-2", "SP-3", "SP-6"], [
        ("*Motor", "TXT", ["3 HP (2.2 kW), variable 200 – 2,800 rpm", "1.5 / 2 HP (1.1 / 1.5 kW), 1,400 / 2,800 rpm", "3 HP (2.2 kW), variable 400 – 2,800 rpm"]),
        ("*Belt size", "BELT", [(2000, 50), (1500, 75), (2000, 50)]),
        ("Belt angle", "TXT", ["—", "0 – 90°", "0 – 90°"]),
        ("*Second station", "TXT", ["Disc Ø10 – 12-5/8″ (250 – 320 mm); Ø6″ (150 mm) disc with the belt",
                                   "Grinding wheel Ø10 × 1-1/4″ (250 × 32 mm) or cup wheel; polishing wheel Ø8″ (200 mm)",
                                   "Disc sander Ø20″ (508 mm), table 25 × 12″ (636 × 305 mm), tilts 45° down"]),
        ("Belt speed", "MS", ["—", (14.7, 29), "—"]),
        ("Packing size L × W × H", "PK", [(123, 69, 150), (83, 63, 128), (118, 87, 145)]),
        ("*Weight", "KG", [145, 75, 195]),
    ]),
]
CAT["tt-sp"] = ["SP-2: variable speed; two working ends; for all kinds of polishing work; safety cover rotates 360°; many kinds of discs; accessories: polishing mandrel, keyless chuck, Velcro sanding disc, clamping arbors A and B",
                "SP-6: belt grinder for surface grinding, bevelling, deburring or contact grinding; disc sander for smoothing burrs, chamfering edges for welding and cleaning castings",
                "SP-3: high power; versatile; balanced, low vibration, low noise; combination machine for finishing and sharpening; belt 0 – 90°; grinding wheel and cup grinding wheel for heavy-duty grinding and deburring; polishing wheel"]

TAB["tt-dc"] = [
    table("DVS14 · DC650", "Metal dust collectors for grinders and sanders", ["DVS14", "DC650"], [
        ("*Airflow", "TXT", ["494 CFM (14 m³/min)", "650 CFM"]),
        ("*Filtration", "TXT", ["Panel filter 12 × 16 × 1″ (305 × 405 × 25 mm); cyclone separation", "Three stages: 30-micron stainless steel, 5-micron activated carbon, 1-micron pleated filter"]),
        ("*Inlets", "TXT", ["One hose 3 × 59″ (75 × 1,500 mm)", "Two Ø4″ (100 mm) — two machines at a time"]),
        ("*Motor", "TXT", ["3/4 HP (0.55 kW)", "1.5 HP (1.1 kW), single-phase"]),
        ("Dust drawer", "TXT", ["Pull-out tray", "1.06 cu ft (30 L)"]),
        ("Sound level", "TXT", ["—", "82 dB"]),
        ("Packing size L × W × H", "PK", [(92, 59, 85), (81, 62, 116)]),
        ("*Weight", "KG", [67, 90]),
    ]),
]
CAT["tt-dc"] = ["DVS14: fan blades and enclosure of aluminum; pull-out tray for easy waste disposal; simple filter change; cyclone technology, quiet and effective",
                "DC650: cuts airborne dust in the shop; 4″ adapter inlets; casters; NOT for wood dust; grinding dust and chips drop into a removable clean-out drawer; two machines at once"]

# PDF p30 (055 – 056)
TAB["tt-bfm2560"] = [
    table("BFM-2560", "Wide-belt finishing and deburring machine, 24″ working width", ["BFM-2560"], [
        ("*Working width, max", "TXT", ["24″ (600 mm)"]),
        ("*Workpiece thickness", "TXT", ["0.04 – 6″ (1 – 156 mm)"]),
        ("Workpiece length, min", "TXT", ["12″ (300 mm)"]),
        ("Abrasive belt", "TXT", ["25 × 60″ (635 × 1,520 mm)"]),
        ("*Feed speed", "MMIN", [(2, 9)]),
        ("Dust extraction air flow", "TXT", ["1,766 CFM (3,000 m³/h); 6″ (Ø152 mm) hood outlet"]),
        ("*Main motor", "KW", [7.5]),
        ("Packing size L × W × H", "PK", [(177, 150, 204)]),
        ("*Weight", "KG", [955]),
    ]),
    table("WD-1800", "Stainless-steel wet dust collector for metal grinding dust", ["WD-1800"], [
        ("*Air flow", "TXT", ["2,100 CFM"]),
        ("*Motor", "TXT", ["5 HP (3.7 kW)"]),
        ("Packing size L × W × H", "PK", [(122, 100, 210)]),
        ("*Weight", "KG", [260]),
    ]),
]
CAT["tt-bfm2560"] = ["BFM-2560: table height by digital control (mm / inch); conveyor with variable speed; push-button control; four-post synchronous lifting; heat-resistant rubber conveyor belt; electric-eye belt tracking; emergency stop at mid-rack; 6″ dust hood outlet; rubber roller 645 mm long",
                     "WD-1800: stainless-steel wet scrubber: draws dust through a filter, keeps metal dust from becoming a combustible-dust fire hazard; sludge drains into a water pan accessible from the front"]

TAB["tt-md380"] = [
    table("MD-380A · MD-380B", "End-surface grinding machines — fixed table or Ø16″ rotary table", ["MD-380A", "MD-380B"], [
        ("*Table", "TXT", ["Fixed, 15.2 × 7″ (386 × 177 mm)", "Rotary, Ø15.7″ (400 mm)"]),
        ("*Grinding height, max", "L", [280, 280]),
        ("Vertical increment", "TXT", "0.0004″ (0.01 mm)"),
        ("Grinding wheel", "TXT", "Ø7-7/8 × 3-1/16″, 3-1/16″ bore (200 × 78 × 78 mm), 2,800 rpm"),
        ("*Spindle motor", "TXT", "4 HP electro-spindle"),
        ("Coolant", "TXT", "0.12 HP pump, 5.3 US gal (20 L) tank"),
        ("Noise level, max", "TXT", "68 dB"),
        ("Machine size L × W × H", "TXT", "49 × 37 × 71″ (1,250 × 950 × 1,800 mm)"),
        ("Packing size L × W × H", "PK", [(143, 107, 191), (156, 106, 191)]),
        ("*Weight", "KG", [690, 770]),
    ]),
]
CAT["tt-md380"] = ["Italian design; easy operation with high precision; small footprint; fixed table (A) or rotary table (B), magnetic chuck optional"]

# PDF p31 (057 – 058) — vises and welding angle clamps
TAB["tt-vise"] = [
    table("BSM · TSL · TMS", "Drill press vises", ["BSM75N", "BSM100N", "BSM125N", "BSM150N", "BSM100", "BSM125", "TSL-100", "TSL-100Q", "TSL-140", "TSL-140Q", "TSL-200", "TSL-200Q", "TMS135", "TMS180"], [
        ("*Jaw width", "F", [80, 105, 125, 150, 105, 125, 100, 100, 140, 140, 200, 200, 135, 180]),
        ("*Jaw opening", "F", [55, 95, 115, 135, 100, 125, 100, 100, 140, 140, 200, 200, 145, 260]),
        ("Jaw height", "F", [27, 27, 39, 39, 30, 49, 40, 37, 50, 50, 64, 58, "—", "—"]),
        ("*Weight", "KG", [2.1, 3.2, 4.5, 6.2, 5, 12, 9, 6, 15, 12, 36, 25, 15, 32]),
    ]),
    table("TQ", "Tilting and swivelling precision vises (inch)", ["TQC4″", "TQC5″", "TQC6″", "TQB6″", "TQA6″"], [
        ("*Jaw width", "TXT", ["4″", "5″", "6″", "6″", "6″"]),
        ("Jaw depth", "TXT", ["1-1/2″", "1-3/4″", "2″", "1-3/4″", "2″"]),
        ("*Jaw opening", "TXT", ["4″", "5″", "6″", "9″", "6″"]),
        ("Height", "TXT", ["4-9/16″", "5-1/2″", "6″", "6-1/4″", "7-1/4″"]),
        ("Base size", "TXT", ["7-3/4 × 5-3/4″", "10-1/2 × 7-1/2″", "11-1/2 × 8-7/16″", "12-3/4 × 11-3/4″", "9 × 11-1/2″"]),
        ("*Weight", "KG", [14, 28, 39, 48, 51]),
    ]),
    table("AC", "Welding angle clamps", ["AC-60", "AC-100", "AC-100H"], [
        ("*Jaw opening", "F", [60, 100, 100]),
        ("Jaw width", "F", [60, 90, "—"]),
        ("Jaw height", "TXT", ["1-3/8″ (35 mm)", "2-3/8″ (60 mm)", "2-3/8″ (60 mm) bottom clamp, 7-1/2″ (190 mm) with the top clamp"]),
        ("*Weight", "KG", [5, 14, 24]),
    ]),
]
CAT["tt-vise"] = ["BSM-N: changeable prismatic jaws; pin for powerful clamping; smooth running with exact jaw guides even at high axial load", "BSM100/125: easy operation; hardened fixing plate",
                  "TSL-Q: quick lock", "TMS: changeable prismatic jaws; pin for clamping; exact jaw guides; slots in the base for mounting and clamping",
                  "TQ: TQA tilting, TQB swivel, TQC compound (catalogue photos)", "AC-100H: for box and round tubing, box tubing and angle iron, small vee clamp; small and large clamp attachments"]

# ------------------------------------------------------------------------------------------------ drilling
# PDF p32 (059 – 060)
TAB["tt-wtz"] = [
    table("WTZ-13J · WTZ-16J · WTZ-16Q · WTZ-16JF", "Variable-speed drill presses with digital speed display", ["WTZ-13J", "WTZ-16J", "WTZ-16Q", "WTZ-16JF"], [
        ("*Drilling capacity in steel", "F", [13, 16, 16, 16]),
        ("Chuck", "TXT", ["1 – 13 mm (0.04 – 1/2″)", "3 – 16 mm (1/8 – 5/8″)", "3 – 16 mm (1/8 – 5/8″)", "3 – 16 mm (1/8 – 5/8″)"]),
        ("Spindle taper", "TXT", "MT2"),
        ("*Spindle travel", "F", [50, 80, 60, 80]),
        ("*Spindle speeds", "TXT", "Variable, 500 – 2,600 rpm"),
        ("Throat (spindle to column)", "F", [114, 182, 152, 182]),
        ("Table size", "TXT", ["6-1/2 × 6-1/2″ (165 × 165 mm)", "Ø11-3/4″ (300 mm)", "Ø11-3/4″ (300 mm)", "Ø11-3/4″ (300 mm)"]),
        ("Table travel", "F", [140, 360, 360, 600]),
        ("Column diameter", "F", [48, 72, 72, 72]),
        ("Mounting", "TXT", ["Bench", "Bench", "Bench", "Floor"]),
        ("*Motor", "TXT", ["0.6 HP (450 W)", "3/4 HP (550 W)", "0.6 HP (450 W)", "3/4 HP (550 W)"]),
        ("Packing size L × W × H", "PK", [(50, 43, 28), (78, 52, 29), (63, 49, 30), (141, 56, 24)]),
        ("*Weight", "KG", [30, 55, 47, 65]),
    ]),
    table("WTZ-16T", "Drilling and tapping press — drills 5/8″, taps M12 with automatic reverse", ["WTZ-16T"], [
        ("*Drilling capacity in steel", "F", [16]),
        ("*Tapping capacity", "TXT", ["M12 (1/2″)"]),
        ("Chuck", "TXT", ["1 – 16 mm (0.04 – 5/8″) on B18 taper"]),
        ("*Spindle travel", "F", [85]),
        ("*Spindle speeds", "TXT", ["Variable, 260 – 1,800 rpm"]),
        ("Throat (spindle to column)", "F", [185]),
        ("Spindle to table / to base", "TXT", ["13″ (330 mm) / 20″ (510 mm)"]),
        ("Table size", "TXT", ["11 × 11″ (280 × 280 mm)"]),
        ("Base size", "TXT", ["11.2 × 9.4″ (285 × 240 mm)"]),
        ("Column diameter", "F", [72]),
        ("*Motor", "TXT", ["1 HP (750 W)"]),
        ("Packing size L × W × H", "PK", [(95, 59, 35)]),
        ("*Weight", "KG", [57]),
    ]),
]
CAT["tt-wtz"] = ["WTZ-13J/16J/16Q/16JF: digital speed display; variable speed",
                 "WTZ-16T: spindle runout under 0.01 mm; rigid head body for long quill life; variable spindle speed; energy-saving (no idle running); drilling / tapping switch rated 100,000 cycles; laser cross-hair positioning; digital depth readout mm / inch; switching to tapping: spindle brake in 0.2 s, reverses to back the tap out and protect it"]

# PDF p33 – p34 (061 – 064) — gear-head drill presses
SPEED8_25 = "8 speeds, 130 – 3,200 rpm at 60 Hz (105 – 2,900 rpm at 50 Hz)"
SPEED8_28 = "8 speeds, 90 – 3,610 rpm at 60 Hz (75 – 3,010 rpm at 50 Hz)"
TAB["tt-t25"] = [
    table("T-25 · T-26", "Gear-head drill presses, 1″ capacity, floor and bench", ["T-25 / T-25A", "T-25C / T-25AC", "T-25C-H", "T-26", "T-26C / T-26AC", "T-25B / T-25BC", "T-26B / T-26BC"], [
        ("*Drilling capacity in steel", "F", [25, 25, 25, 26, 26, 25, 26]),
        ("Tapping capacity, steel / cast iron", "TXT", "M10 / M16 (optional tapping)"),
        ("Spindle taper", "TXT", "MT3"),
        ("*Spindle travel", "F", [125] * 7),
        ("*Spindle speeds", "TXT", SPEED8_25),
        ("*Motor", "TXT", ["0.9 / 1.2 HP (0.65 / 0.9 kW), two-speed"] * 3 + ["1.2 / 1.5 HP (0.9 / 1.1 kW), two-speed"] * 2 + ["0.9 / 1.2 HP (0.65 / 0.9 kW), two-speed", "1.2 / 1.5 HP (0.9 / 1.1 kW), two-speed"]),
        ("Controls", "TXT", ["Standard (A: frame with scale for down feed)", "24 V control, spindle guard micro-switch", "24 V control, depth readout", "Standard", "24 V control, spindle guard micro-switch",
                             "Bench model (BC: 24 V control)", "Bench model (BC: 24 V control)"]),
        ("Mounting", "TXT", ["Floor"] * 5 + ["Bench"] * 2),
        ("Packing size L × W × H", "PK", [(167, 56, 72), (167, 57, 72), (167, 57, 72), (167, 56, 72), (167, 57, 72), (94, 48, 73), (94, 48, 73)]),
        ("*Weight", "KG", [190, 190, 210, 192, 192, 136, 138]),
    ]),
    table("T-28 · T-30 · T-32 · T-35 · T-40", "Gear-head drill presses, 1-1/8 to 1-9/16″, with power feed", ["T-28", "T-28B", "T-30", "T-30B", "T-32", "T-35", "T-40"], [
        ("*Drilling capacity in steel", "F", [28, 28, 30, 30, 32, 35, 40]),
        ("Tapping capacity, steel / cast iron", "TXT", ["M12 / M16"] * 5 + ["M14 / M18", "M18 / M22"]),
        ("Spindle taper", "TXT", ["MT3"] * 4 + ["MT4"] * 3),
        ("*Spindle travel", "F", [150] * 6 + [190]),
        ("*Spindle speeds", "TXT", [SPEED8_28] * 6 + ["8 speeds, 108 – 1,800 rpm at 60 Hz (90 – 1,500 rpm at 50 Hz)"]),
        ("*Feed", "TXT", ["Mechanical, 0.004 – 0.013″/rev (0.1 – 0.33 mm/rev)", "Mechanical, 0.004 – 0.013″/rev (0.1 – 0.33 mm/rev)", "Manual", "Manual",
                          "Electric, 0.004 – 0.013″/rev (0.1 – 0.33 mm/rev)", "Electric, 0.004 – 0.013″/rev (0.1 – 0.33 mm/rev)", "Mechanical, 0.004 – 0.013″/rev (0.1 – 0.33 mm/rev)"]),
        ("Table", "TXT", ["Rectangular", "Rectangular (bench)", "Round", "Round (bench)", "Round, rotary", "Rectangular", "Rectangular"]),
        ("*Motor", "TXT", ["1.2 / 1.6 HP (0.9 / 1.2 kW), two-speed", "1.2 / 1.6 HP (0.9 / 1.2 kW), two-speed", "1.5 / 1.7 HP (1.1 / 1.3 kW), two-speed", "1.5 / 1.7 HP (1.1 / 1.3 kW), two-speed",
                           "1.7 / 2 HP (1.3 / 1.5 kW), two-speed", "2 / 2.4 HP (1.5 / 1.8 kW), two-speed", "3 HP (2.2 kW)"]),
        ("Packing size L × W × H", "PK", [(174, 67, 88), (74, 48, 118), (174, 67, 88), (74, 48, 135), (174, 67, 88), (174, 67, 88), (217, 57, 93)]),
        ("*Weight", "KG", [265, 195, 255, 200, 295, 307, 345]),
    ]),
]
CAT["tt-t25"] = ["T-25/26: drilling head and table both move up and down; table swivels; safety spindle guard; 8 speeds; steady and quiet; A: frame with scale for down feed; tapping optional on T-25/25A/25B/26/26B; C: 24 V control and spindle guard micro-switch; C-H: depth reader",
                 "T-28/30: solid drilling table, precisely machined; solid base plate with T-slots; T-28 mechanical feed; tapping optional on T-28B/30/30B",
                 "T-32/35/40: easy operation; continuously rated motor; 8 speeds; T-32 round rotary table; T-32/35 electric automatic feed; T-40 mechanical feed"]

# PDF p35 (065 – 066)
TAB["tt-t50"] = [
    table("T-50 · T-50E", "Heavy-duty gear-head drill presses, 2″ in steel, 12 speeds and power feed", ["T-50", "T-50E"], [
        ("*Drilling capacity", "TXT", "2″ (50 mm) in steel, 2-1/4″ (58 mm) in cast iron"),
        ("*Tapping capacity", "TXT", "M30 in steel, M38 in cast iron"),
        ("*Throat (spindle to column)", "F", [275, 400]),
        ("Spindle nose to table", "TXT", ["1-1/8 – 29-3/4″ (30 – 755 mm)", "1-1/8 – 24″ (30 – 610 mm)"]),
        ("Spindle nose to base", "TXT", "36 – 44-3/4″ (915 – 1,135 mm)"),
        ("Spindle stroke", "TXT", "7-1/8″ (180 mm) power feed, 8-5/8″ (220 mm) by hand"),
        ("Spindle taper", "TXT", "MT4"),
        ("*Spindle speeds", "TXT", "12 speeds, 75 – 1,525 rpm at 60 Hz (60 – 1,270 rpm at 50 Hz)"),
        ("Power feed", "TXT", "3 steps, 0.004 / 0.008 / 0.012″/rev (0.1 / 0.2 / 0.3 mm/rev)"),
        ("*Motor", "TXT", "3 HP, 4-pole"),
        ("Table", "TXT", ["Ø20″ (510 mm), 16 mm T-slots", "23.6 × 21.7″ (600 × 550 mm), swivels left and right, 18 mm T-slots"]),
        ("Table (knee) travel", "F", [500, 395]),
        ("Base size", "TXT", ["19.7 × 35.4″ (500 × 900 mm)", "23.6 × 41.7″ (600 × 1,060 mm)"]),
        ("Overall height", "L", [2200, 2245]),
        ("Coolant", "TXT", ["Separate coolant unit", "Built into the base"]),
        ("Packing size L × W × H", "PK", [(113, 70, 240), (125, 75, 245)]),
        ("*Weight", "KG", [660, 860]),
    ]),
    table("TX530 · TX530A", "Inverter-drive drill presses with two-range gearbox — drill and tap, forward and reverse", ["TX530", "TX530A"], [
        ("*Drilling capacity in steel", "F", [32, 40]),
        ("*Tapping capacity", "F", [19, 25]),
        ("Swing", "L", [323, 323]),
        ("Spindle taper", "TXT", ["MT3", "MT4"]),
        ("*Spindle travel", "F", [150, 150]),
        ("*Spindle speeds", "TXT", "Variable (inverter): high range 245 – 2,000 rpm, low range 65 – 540 rpm"),
        ("Feed", "TXT", ["Manual", "Mechanical power feed"]),
        ("Spindle nose to table / base", "TXT", ["20.9″ (530 mm) / 46.5″ (1,180 mm)", "23.8″ (605 mm) / 45.3″ (1,150 mm)"]),
        ("Quill / column diameter", "TXT", "Ø3″ (75 mm) / Ø4-1/2″ (115 mm)"),
        ("Table size", "TXT", "22 × 18.7″ (560 × 475 mm), 16 mm T-slots"),
        ("Base size", "TXT", "27.1 × 19.1″ (688 × 486 mm), T-slotted, with coolant return"),
        ("*Motor", "KW", [2.2, 2.2]),
        ("Packing size L × W × H", "PK", [(95, 64, 200), (96, 65, 229)]),
        ("*Weight", "KG", [340, 382]),
    ]),
]
CAT["tt-t50"] = ["T-50/50E: upgraded cast iron; high-precision bearings; high-precision spindle, all gears hardened; 12 spindle speeds; T-50E: new control panel, 400 mm deep throat, 600 × 550 mm table that turns left / right, built-in coolant (separate unit on T-50)",
                 "TX530/530A: variable spindle speed by frequency inverter; high-low gearbox for high torque; large drilling and tapping capacity; cast-iron structure; coolant standard; safety guard with micro-switch; T-slotted base with coolant return; forward / reverse tapping standard; TX530A mechanical power feed"]

# PDF p36 (067 – 068)
SPEED8_T5 = "8 speeds, 120 – 3,480 rpm at 60 Hz (100 – 2,900 rpm at 50 Hz)"
TAB["tt-t5025"] = [
    table("T5025 · T4025", "Gear-head drill presses, 1″ capacity — forward / reverse, preset depth", ["T5025-1A", "T5025-3A", "T5025H", "T4025", "T4025H"], [
        ("*Drilling capacity in steel", "F", [25] * 5),
        ("Spindle taper", "TXT", "MT3"),
        ("*Spindle travel", "F", [140] * 5),
        ("*Spindle speeds", "TXT", SPEED8_T5),
        ("*Throat (spindle to column)", "F", [225, 225, 315, 225, 315]),
        ("Spindle nose to table / base", "TXT", ["24.4″ (620 mm) / 42.3″ (1,075 mm)", "23.6″ (600 mm) / 42.3″ (1,075 mm)", "26″ (660 mm) / 47.2″ (1,200 mm)", "— / 17.5″ (445 mm)", "— / 17.5″ (445 mm)"]),
        ("Table", "TXT", ["Ø15.4″ (390 mm), round", "12.4 × 10.8″ (315 × 275 mm), tilts ±50°", "12.4 × 16.3″ (315 × 415 mm), tilts ±50°", "Base 12 × 11.7″ (305 × 297 mm)", "18.7 × 15.7″ (475 × 400 mm) on the base"]),
        ("Mounting", "TXT", ["Floor", "Floor", "Floor", "Bench", "Bench"]),
        ("*Motor", "TXT", "3/4 / 1 HP (0.55 / 0.75 kW), two-speed"),
        ("Packing size L × W × H", "PK", [(166, 60, 46), (166, 60, 46), (190, 59, 96), (108, 50, 77), (108, 50, 90)]),
        ("*Weight", "KG", [247, 249, 338, 175, 220]),
    ]),
]
CAT["tt-t5025"] = ["gear-driven head with 8 speeds; head and table lift with fast locking device; rigid base with T-slots for large parts; ±50° tilting table (T5025-3A, T5025H); forward / reverse switch; preset drilling depth; spindle cover with micro-switch"]

# PDF p37 (069 – 070)
TAB["tt-tb"] = [
    table("TB24 · TB28 · TB36", "Belt-drive industrial column drills, 3-phase", ["TB24", "TB28", "TB36"], [
        ("*Drilling capacity in steel", "F", [24, 28, 34]),
        ("*Spindle travel", "F", [85, 105, 160]),
        ("Spindle taper", "TXT", ["MT2", "MT3", "MT4"]),
        ("*Spindle speeds", "TXT", ["7 speeds, 360 – 4,200 rpm", "16 speeds, 120 – 4,250 rpm", "9 speeds, 130 – 4,940 rpm"]),
        ("Throat (spindle to column)", "F", [165, 200, 285]),
        ("Table size", "TXT", ["11 × 11.8″ (280 × 300 mm)", "13.4 × 14.2″ (340 × 360 mm)", "15.7 × 19.7″ (400 × 500 mm)"]),
        ("Spindle to table / base, max", "TXT", ["20.3″ (515 mm) / 26.8″ (681 mm)", "33.8″ (858 mm) / 50″ (1,270 mm)", "31.1″ (790 mm) / 50″ (1,270 mm)"]),
        ("Column diameter", "F", [80, 92, 115]),
        ("*Motor", "TXT", ["1 HP (750 W), 3-phase", "1.1 HP (850 W), 3-phase", "2 / 3 HP (1.5 / 2.2 kW), 3-phase"]),
        ("Overall height", "L", [1170, 1750, 1930]),
        ("Packing size L × W × H", "PK", [(83, 43, 132), (101, 65, 192), (110, 67, 210)]),
        ("*Weight", "KG", [120, 200, 360]),
    ]),
    table("TB24V · TB28V · TB36V", "Inverter-drive industrial column drills, stepless speed, 1-phase", ["TB24V", "TB28V", "TB36V"], [
        ("*Drilling capacity in steel", "F", [24, 28, 34]),
        ("*Spindle travel", "F", [85, 105, 160]),
        ("Spindle taper", "TXT", ["MT2", "MT3", "MT4"]),
        ("*Spindle speeds", "TXT", ["Stepless, 100 – 4,400 rpm", "Stepless, 35 – 6,100 rpm", "Stepless, 40 – 6,500 rpm"]),
        ("Throat (spindle to column)", "F", [165, 200, 285]),
        ("Table size", "TXT", ["11 × 11.8″ (280 × 300 mm)", "13.4 × 14.2″ (340 × 360 mm)", "15.7 × 19.7″ (400 × 500 mm)"]),
        ("Spindle to table / base, max", "TXT", ["19.5″ (495 mm) / 26.8″ (681 mm)", "30.1″ (765 mm) / 47.2″ (1,200 mm)", "31.1″ (790 mm) / 50″ (1,270 mm)"]),
        ("Column diameter", "F", [80, 92, 115]),
        ("Coolant", "TXT", ["—", "Standard", "Standard"]),
        ("*Motor", "TXT", ["2 HP (1.5 kW), 1-phase", "2 HP (1.5 kW), 1-phase", "3 HP (2.2 kW), 1-phase"]),
        ("Overall height", "L", [1170, 1750, 1930]),
        ("Packing size L × W × H", "PK", [(83, 43, 132), (101, 65, 192), (110, 67, 210)]),
        ("*Weight", "KG", [120, 200, 360]),
    ]),
]
CAT["tt-tb"] = ["high-precision industrial column drill; V-belt drive, high torque; quality servo motor; digital LED speed display; forward / reverse switch; precisely finished table with cross T-slots 14 mm; easy tool change device; large finished base plate; adjustable chuck guard; work light; V: stepless speed by frequency converter, coolant on TB28V / TB36V"]

# ------------------------------------------------------------------------------------------------ milling & slotting
# PDF p38 (071 – 072)
TAB["tt-slot"] = [
    table("B5012 · B5013", "Keyseaters and slotting machines for keyways and splines", ["B5012", "B5013"], [
        ("*Stroke, max", "F", [120, 125]),
        ("*Workpiece capacity", "TXT", ["Ø16-1/2″ (420 mm) × 4-3/4″ (120 mm) high on the table; not limited by the column for large parts", "—"]),
        ("Strokes per minute", "TXT", ["—", "60 – 350, 6 steps"]),
        ("Table size", "TXT", ["7.9 × 15.7″ (200 × 400 mm)", "23.6 × 9.4″ (600 × 240 mm), 14 mm T-slots"]),
        ("Table travel, longitudinal × cross", "TXT", ["4.7 × 9.4″ (120 × 240 mm)", "5.1 × 13.4″ (130 × 340 mm)"]),
        ("Head swivel", "TXT", ["—", "90° left and right"]),
        ("*Motor", "TXT", ["1.5 HP (1.1 kW)", "1/3 HP (0.25 kW)"]),
        ("Packing size L × W × H", "PK", [(96, 54, 91), (83, 76, 109)]),
        ("*Weight", "KG", [185, 240]),
    ]),
]
CAT["tt-slot"] = ["B5012: keyways and spline joints in single and small-batch production, especially keyways in blind holes; the column does not limit the size of the part — flexible for keyways in large parts",
                  "B5013: heavy-duty cast iron; swivel head tilts 90° left and right; 0 – 125 mm stroke range; 60 – 350 strokes/min in 6 steps"]

TAB["tt-mill-small"] = [
    table("TX-20 · DM-20", "Mini mill-drill and radial drill-mill, 3/4″ drilling", ["TX-20", "DM-20"], [
        ("*Drilling capacity", "F", [20, 20]),
        ("*Milling capacity", "TXT", ["—", "End mill 5/8″ (16 mm), face mill 2-1/2″ (63 mm)"]),
        ("Spindle taper", "TXT", ["MT2", "MT3 / R8"]),
        ("*Spindle speeds", "TXT", ["Variable, 50 – 2,250 rpm", "5 speeds, 210 – 2,000 rpm"]),
        ("Spindle travel", "TXT", ["—", "3.5″ (90 mm)"]),
        ("Table", "TXT", ["27.6 × 7.1″ (700 × 180 mm); X 11″ (280 mm), Y 6.9″ (175 mm)", "Cross table and box table"]),
        ("Throat / reach", "TXT", ["6.7″ (170 mm) spindle to column; head travel 15″ (380 mm)", "Arm reach 19.7″ (500 mm); arm rise and fall 14.6″ (370 mm)"]),
        ("*Motor", "TXT", ["0.8 HP (0.6 kW)", "1 HP (750 W)"]),
        ("Packing size L × W × H", "PK", [(138, 72, 105), (93, 51, 117)]),
        ("*Weight", "KG", [105, 354]),
    ]),
]
CAT["tt-mill-small"] = ["TX-20: X-Y table and spindle — recessing, surface milling, end milling, circular grooving, angled drilling, grooving with an indexer; variable speed",
                        "DM-20: easy to operate; cross table and box table; double column lock; standard draw bar, 1 – 13 mm drill chuck, MT3/B16 arbor; optional vise, coolant pump, milling chuck set, halogen lamp, end mills 10/12/16"]

# PDF p39 (073 – 074)
TAB["tt-zx"] = [
    table("ZX5325 · ZX5325C · ZX7550C · ZX7550CW", "Drilling and milling machines, 2″ drilling", ["ZX5325", "ZX5325C", "ZX7550C", "ZX7550CW"], [
        ("*Drilling capacity", "F", [50, 50, 50, 50]),
        ("*Milling capacity, face / end", "TXT", ["Ø4″ (100 mm) / Ø1-1/4″ (32 mm)", "Ø4″ (100 mm) / Ø1-1/4″ (32 mm)", "Ø4″ (100 mm) / Ø1″ (25 mm)", "Ø4″ (100 mm) / Ø1″ (25 mm)"]),
        ("Tapping capacity", "TXT", "M16"),
        ("Spindle taper", "TXT", ["MT4 (ISO30, ISO40, R8 optional)", "MT4 (ISO30, ISO40, R8 optional)", "—", "—"]),
        ("Spindle nose to table", "TXT", ["—", "—", "2-3/4 – 16-1/2″ (70 – 420 mm)", "2-3/4 – 16-1/2″ (70 – 420 mm)"]),
        ("*Spindle speeds", "TXT", ["270 – 2,400 rpm", "115 – 1,750 rpm", "110 – 1,760 rpm", "Vertical 110 – 1,760 rpm, horizontal 38 – 1,335 rpm"]),
        ("Spindle travel", "F", [125, 125, 120, 120]),
        ("*Table", "TXT", ["10.2 × 39.4″ (260 × 1,000 mm)", "10.2 × 39.4″ (260 × 1,000 mm)", "31.5 × 9.4″ (800 × 240 mm)", "31.5 × 9.4″ (800 × 240 mm)"]),
        ("Travel X × Y × Z", "TXT", ["17.7 × 11 × 15″ (450 × 280 × 380 mm)", "17.7 × 11 × 15″ (450 × 280 × 380 mm)", "15.7 × 9.1″ (400 × 230 mm)", "15.7 × 9.1″ (400 × 230 mm)"]),
        ("Head drive", "TXT", ["Belt", "Gear", "Gear", "Gear"]),
        ("*Motor", "TXT", ["2 HP (1.5 kW)", "1.1 / 2 HP (0.85 / 1.5 kW)", "1.1 / 2 HP (0.85 / 1.5 kW)", "1.1 / 2 HP (0.85 / 1.5 kW) vertical, 3 HP (2.2 kW) horizontal"]),
        ("Packing size L × W × H", "PK", [(114, 145, 210), (114, 114, 222), (114, 110, 222), (114, 122, 222)]),
        ("*Weight", "KG", [850, 870, 630, 850]),
    ]),
    table("ZX6350C · ZX6350Z", "Drilling and milling machines with vertical and horizontal spindles", ["ZX6350C", "ZX6350Z"], [
        ("*Drilling capacity", "F", [50, 50]),
        ("*Milling capacity, face / end", "TXT", ["Ø4″ (100 mm) / Ø1″ (25 mm)", "Ø5″ (125 mm) / Ø1″ (25 mm)"]),
        ("Tapping capacity", "TXT", "M16"),
        ("Spindle nose to table", "TXT", ["3.5 – 15.7″ (90 – 400 mm)", "3.5 – 14.6″ (90 – 370 mm)"]),
        ("*Spindle speeds", "TXT", ["Vertical 110 – 1,760 rpm, horizontal 38 – 1,310 rpm", "Vertical 90 – 2,000 rpm (8), horizontal 40 – 1,300 rpm (12)"]),
        ("Spindle travel", "F", [120, 120]),
        ("*Table", "TXT", ["44.1 × 11″ (1,120 × 280 mm)", "49.2 × 12.6″ (1,250 × 320 mm)"]),
        ("Travel X × Y", "TXT", ["23.6 × 9.1″ (600 × 230 mm)", "23.6 × 11.8″ (600 × 300 mm)"]),
        ("*Motor", "TXT", ["1.1 / 2 HP (0.85 / 1.5 kW) vertical, 3 HP (2.2 kW) horizontal", "3 HP (2.2 kW)"]),
        ("Packing size L × W × H", "PK", [(160, 140, 222), (160, 140, 222)]),
        ("*Weight", "KG", [1120, 1120]),
    ]),
]
CAT["tt-zx"] = ["ZX5325/C: rotary milling head; table swivels ±45°; ZX5325 belt-drive head, ZX5325C gear-drive head; power feed on Y, Z and DRO at extra cost", "ZX7550C: power feed on X, Y, Z at extra cost; optional DRO"]

# PDF p39 – p42 (074 – 080) — turret and universal milling machines
TAB["tt-mill"] = [
    table("4H · X6325W · X6332WA · X6336 · X6336WA", "Turret milling machines; the W models with a horizontal spindle too", ["4H", "X6325W", "X6332WA", "X6336", "X6336WA"], [
        # X6336: the owner's 2026 sheet (vertical head only, power feed and rapid on X, Y, Z) replaces the catalogue's X6336
        ("Spindle taper", "TXT", ["—", "NT30, R8", "ISO40", "NT40; head swivels 90°", "ISO40 vertical, ISO50 horizontal"]),
        ("*Spindle speeds", "TXT", ["—", "Vertical 80 – 5,440 rpm, horizontal 40 – 1,300 rpm", "Vertical 80 – 5,440 rpm, horizontal 40 – 1,300 rpm",
                                    "Vertical 60 – 3,600 rpm, rated at 50 Hz", "Vertical 70 – 7,200 rpm, horizontal 60 – 1,800 rpm"]),
        ("Quill travel", "F", [127, 127, 127, "—", 127]),
        ("Spindle nose to table", "TXT", ["0 – 18.1″ (0 – 460 mm)", "3.9 – 19.3″ (100 – 490 mm)", "3.9 – 19.7″ (100 – 500 mm)", "1.6 – 19.3″ (40 – 490 mm)", "5.3 – 19.1″ (135 – 485 mm)"]),
        ("Spindle to column", "TXT", ["—", "3.9 – 22″ (100 – 560 mm)", "3.9 – 22″ (100 – 560 mm)", "6.3 – 26″ (160 – 660 mm)", "5.9 – 29.5″ (150 – 750 mm)"]),
        ("*Table", "TXT", ["50 × 10″ (1,270 × 254 mm)", "50 × 10.2″ (1,270 × 260 mm)", "49.2 × 12.6″ (1,250 × 320 mm), swivels ±45°",
                           "63 × 14.2″ (1,600 × 360 mm); 3 T-slots; 772 lb (350 kg) load", "64.2 × 14.2″ (1,630 × 360 mm), swivels ±45°"]),
        ("*Travel X × Y (× Z)", "TXT", ["33.5 × 15.7″ (850 × 400 mm)", "27.6 × 11″ (700 × 280 mm)", "23.6 × 13.4″ (600 × 340 mm)", "51.2 × 12.6 × 17.7″ (1,300 × 320 × 450 mm)", "39.4 × 12.6 × 15.9″ (1,000 × 320 × 405 mm)"]),
        ("Feeds", "TXT", ["Ask for the configuration", "Power feed X, Y; motorized Z", "Power feed X, Y; motorized Z",
                          "Power feed X, Y 1 – 31.5 in/min (25 – 800 mm/min), Z 1.2 – 10.5 in/min (30 – 267 mm/min); rapid 39.4 / 39.4 / 13.2 in/min (1,000 / 1,000 / 335 mm/min)",
                          "Power feed X, Y, Z"]),
        ("*Motor", "TXT", ["3 HP (2.2 kW)", "3 HP (2.2 kW) vertical, 4 HP (3 kW) horizontal", "3 HP (2.2 kW) vertical, 4 HP (3 kW) horizontal",
                           "—", "5 / 2.7 HP (3.7 / 2 kW) vertical, 5.5 HP (4 kW) horizontal"]),
        ("Packing size L × W × H", "PK", [(170, 160, 215), (150, 167, 210), (152, 163, 220), (267, 222, 240), (200, 200, 225)]),
        ("*Weight", "KG", [1200, 1600, 1550, 3200, 2650]),
    ]),
    table("XQ6226A · XQ6226B · XQ6226W · X6436", "Universal milling machines, ISO40 – ISO50, swivel head ±360°", ["XQ6226A", "XQ6226B", "XQ6226W", "X6436"], [
        ("Spindle taper", "TXT", ["ISO40", "ISO40", "ISO40", "ISO40 vertical, ISO50 horizontal"]),
        ("*Milling capacity", "TXT", ["Horizontal Ø5″ (125 mm), vertical Ø1″ (25 mm)", "Horizontal Ø5″ (125 mm), vertical Ø1″ (25 mm)", "Horizontal Ø5″ (125 mm), vertical Ø1-1/8″ (28 mm)", "—"]),
        ("*Spindle speeds", "TXT", ["Vertical 40 – 1,600 rpm", "Vertical 40 – 1,600 rpm, horizontal 40 – 1,300 rpm", "Vertical 40 – 1,600 rpm, horizontal 40 – 1,300 rpm", "Vertical 60 – 1,750 rpm, horizontal 60 – 1,800 rpm"]),
        ("Spindle nose to table", "TXT", ["3.1 – 19.7″ (80 – 500 mm)", "3.1 – 19.7″ (80 – 500 mm)", "3.1 – 22″ (80 – 560 mm)", "5.9 – 23.6″ (150 – 600 mm)"]),
        ("*Table", "TXT", ["44.1 × 10.2″ (1,120 × 260 mm)", "44.1 × 10.2″ (1,120 × 260 mm)", "50 × 10.2″ (1,270 × 260 mm)", "52.2 × 14.2″ (1,325 × 360 mm); 63″ (1,600 mm) option"]),
        ("*Travel X × Y (× Z)", "TXT", ["23.6 × 10.6″ (600 × 270 mm)", "23.6 × 10.6″ (600 × 270 mm)", "29.5 × 11.8″ (750 × 300 mm)", "43.3 (51.2) × 12.6 × 17.7″ (1,100 (1,300) × 320 × 450 mm)"]),
        ("Feeds", "TXT", ["Power feed X, Y (Z optional)", "Power feed X, Y; motorized Z", "Power feed X, Y (Z optional)", "Servo feed and rapid X, Y, Z"]),
        ("*Motor", "TXT", ["3 HP (2.2 kW)", "3 HP (2.2 kW)", "4 HP (3 kW) horizontal, 4 HP (3 kW) vertical", "5.5 HP (4 kW) vertical, 7.5 HP (5.5 kW) horizontal"]),
        ("Packing size L × W × H", "PK", [(145, 165, 210), (145, 165, 210), (150, 167, 210), (180, 210, 200)]),
        ("*Weight", "KG", [1500, 1550, 1650, 2650]),
    ]),
    table("LM-1450A · B · C · D · X5750 · X5750A", "Heavy universal milling machines, ISO50", ["LM-1450A", "LM-1450B", "LM-1450C", "LM-1450D", "X5750", "X5750A"], [
        ("Spindle taper", "TXT", "ISO50"),
        ("*Spindle speeds", "TXT", ["Horizontal 60 – 1,800 rpm (12), vertical 60 – 1,700 rpm (12)", "Horizontal 60 – 1,800 rpm (12), vertical 60 – 1,700 rpm (12)",
                                    "Horizontal 30 – 1,500 rpm (18), vertical 60 – 1,700 rpm (12)", "Horizontal 30 – 1,500 rpm (18), vertical 60 – 1,700 rpm (12)",
                                    "30 – 2,050 rpm (27 speeds)", "30 – 2,050 rpm (27 speeds)"]),
        ("Spindle nose to table", "TXT", ["5.9 – 21.7″ (150 – 550 mm)", "5.9 – 21.7″ (150 – 550 mm)", "5.9 – 22.4″ (150 – 570 mm)", "5.9 – 22.4″ (150 – 570 mm)", "2 – 21.7″ (50 – 550 mm)", "2 – 21.7″ (50 – 550 mm)"]),
        ("*Table", "TXT", ["64.2 × 14.2″ (1,630 × 360 mm)", "64.2 × 14.2″ (1,630 × 360 mm)", "64.2 × 12.6″ (1,630 × 320 mm)", "78.7 × 15.7″ (2,000 × 400 mm)", "63 × 19.7″ (1,600 × 500 mm)", "78.7 × 19.7″ (2,000 × 500 mm)"]),
        ("*Travel X × Y × Z", "TXT", ["39.4 × 12.6 × 15.9″ (1,000 × 320 × 405 mm)", "47.2 × 11.8 × 15.4″ (1,200 × 300 × 390 mm)", "31.5 × 12.2 × 16.5″ (800 × 310 × 420 mm)",
                                     "47.2 × 12.4 × 15.2″ (1,200 × 315 × 385 mm)", "47.2 × 27.6 × 19.7″ (1,200 × 700 × 500 mm)", "55.1 × 27.6 × 19.7″ (1,400 × 700 × 500 mm)"]),
        ("T-slots (number / width / spacing)", "TXT", ["3 / 18 / 80 mm", "3 / 18 / 80 mm", "3 / 18 / 70 mm", "3 / 18 / 90 mm", "5 / 18 / 80 mm", "5 / 18 / 80 mm"]),
        ("Table swivel", "TXT", ["±45°", "±45°", "±45°", "±45° optional", "—", "—"]),
        ("Feeds", "TXT", ["Power feed and rapid X, Y, Z", "Servo power feed (variable) and rapid X, Y, Z", "Power feed and rapid X, Y, Z", "Power feed and rapid X, Y, Z",
                          "Three servo motors, ball screws on X, Y, Z", "Three servo motors, ball screws on X, Y, Z"]),
        ("*Motor", "TXT", ["5.5 HP (4 kW) vertical, 5.5 HP (4 kW) horizontal", "5.5 HP (4 kW) vertical, 6.7 HP (5 kW) horizontal", "5.5 HP (4 kW) vertical, 10 HP (7.5 kW) horizontal",
                           "5.5 HP (4 kW) vertical, 15 HP (11 kW) horizontal", "10 HP (7.5 kW)", "10 HP (7.5 kW)"]),
        ("Packing size L × W × H", "PK", [(200, 210, 225), (210, 210, 225), (223, 210, 225), (286, 220, 210), (263, 246, 208), (263, 286, 208)]),
        ("*Weight", "KG", [2650, 2650, 3500, 3950, 4300, 4500]),
    ]),
]
CAT["tt-mill"] = ["X6325W/X6332WA: automatic feed X, Y; motorized Z; head swivels ±45° front/back and ±90° left/right; manual lubrication; X6332WA table swivel ±45°",
                    "X6336/X6336WA: high-speed milling head made in Taiwan; automatic feeds X, Y, Z; hardened square guideways; manual lubrication; X6336WA table swivel ±45°; vertical spindle 70 – 7,200 rpm",
                    "XQ6226: hardened guideways; ISO40 spindle; manual lubrication; X, Y auto feed standard, Z optional; cutter head swivels ±360°; XQ6226B hardened and finish-ground table, auto feed X, Y, motorized table lift Z",
                    "LM-1450A/B/C/D: auto feed and rapid X, Y, Z; head ±360°; three axes hardened; hardened and ground table; DRO at extra cost; B: servo feed motor; C/D: for production work",
                    "X6436: servo drive; auto and rapid feed X, Y, Z",
                    "X5750/A: ball screws on 3 axes; 3 separate servo feed motors; mechanical speed change in the head; extra table support column; mills any angle in the front half-sphere with the swivel head; central lubrication"]

# ------------------------------------------------------------------------------------------------ CNC machine tools
# PDF p43 – p46 (081 – 088)
CNC_CTRL = "Mitsubishi, Fanuc or Siemens (to order)"
TAB["tt-cnc-lathe"] = [
    table("CTK6416", "Slant-bed CNC lathe with gang tooling", ["CTK6416"], [
        ("*Swing over bed", "L", [300]),
        ("Swing over cross slide", "L", [150]),
        ("*Travel X / Z", "TXT", ["11.8 / 11.8″ (300 / 300 mm)"]),
        ("Rapid traverse X / Z", "IPM", [12]),
        ("*Spindle speed, max", "RPM", [3000]),
        ("Spindle taper", "TXT", ["MT5"]),
        ("*Motor", "TXT", ["7.5 HP (5.5 kW) spindle, AC servo axes"]),
        ("Minimum increment", "TXT", ["0.00004″ (0.001 mm)"]),
        ("CNC control", "TXT", ["Mitsubishi or Fanuc (to order)"]),
        ("Packing size L × W × H", "TXT", ["75 × 51 × 59″ (1,900 × 1,300 × 1,500 mm)"]),
        ("*Weight", "KG", [1800]),
    ]),
]
CAT["tt-cnc-lathe"] = ["linear guides — accurate, high precision; gang (parallel) tooling for efficiency; one-piece bed and base, steady and reliable; 45° slant bed for chip clearing; easy to run, small footprint"]

TAB["tt-vmc"] = [
    table("VMC8046 · VMC10562", "Vertical machining centres, BT40, 8,000 rpm", ["VMC8046", "VMC10562"], [
        ("*Table", "TXT", ["39.4 × 21.7″ (1,000 × 550 mm), 1,764 lb (800 kg) load"] * 2),
        ("*Travel X × Y × Z", "TXT", ["31.5 (41.3 optional) × 17.3 × 19.7″ (800 (1,050) × 440 × 500 mm)", "41.3 × 24.4 × 24″ (1,050 × 620 × 610 mm)"]),
        ("Spindle taper", "TXT", "BT40"),
        ("*Spindle speed", "TXT", ["200 – 8,000 rpm", "500 – 8,000 rpm"]),
        ("*Spindle motor", "TXT", ["7.5 / 10 HP (5.5 / 7.5 kW)", "15 HP (11 kW)"]),
        ("Rapid traverse X / Y / Z", "IPM", [12, 24]),
        ("Cutting feed", "TXT", ["X, Y 0.04 – 126 ipm (1 – 3,200 mm/min); Z 0.04 – 79 ipm (1 – 2,000 mm/min)", "X, Y 0.24 – 126 ipm (6 – 3,200 mm/min); Z 0.04 – 315 ipm (1 – 8,000 mm/min)"]),
        ("Positioning / repeatability", "TXT", ["±0.0006″ / ±0.0002″ (±0.015 / ±0.005 mm)", "±0.0006″ per 12″ / ±0.0001″ (±0.015 per 300 / ±0.003 mm)"]),
        ("*Tool changer", "TXT", ["16 tools", "24 tools"]),
        ("CNC control", "TXT", CNC_CTRL),
        ("Machine size L × W × H", "TXT", ["98 × 91 × 106″ (2,500 × 2,300 × 2,700 mm)", "110 × 110 × 112″ (2,800 × 2,800 × 2,850 mm)"]),
        ("*Weight", "KG", [4500, 8000]),
    ]),
    table("CNC100 · CNC120", "CNC slot machining centres for grooving quartz and glass with saw discs", ["CNC100", "CNC120"], [
        ("*Table", "TXT", ["39.4 × 19.7″ (1,000 × 500 mm), 5 T-slots 18 mm at 100 mm", "47.2 × 23.6″ (1,200 × 600 mm), 5 T-slots 18 mm at 125 mm"]),
        ("*Cutting disc", "TXT", "Ø4 – 7″ (100 – 180 mm)"),
        ("*Travel X × Y × Z", "TXT", ["31.5 / 40.2 × 18.1 × 19.7″ (800 / 1,020 × 460 × 500 mm)", "31.5 / 40.2 × 23.6 × 19.7″ (800 / 1,020 × 600 × 500 mm)"]),
        ("Spindle speed", "TXT", "200 – 4,500 rpm"),
        ("*Spindle motor", "TXT", ["3 HP (2.2 kW)", "3 / 4 HP (2.2 / 3 kW)"]),
        ("Rapid traverse", "IPM", [18, 18]),
        ("Positioning / repeatability", "TXT", "±0.0006″ / ±0.0002″ (±0.015 / ±0.005 mm)"),
        ("CNC control", "TXT", "Mitsubishi or Fanuc (to order)"),
        ("Machine size L × W × H", "TXT", ["98 × 91 × 106″ (2,500 × 2,300 × 2,700 mm)", "118 × 98 × 106″ (3,000 × 2,500 × 2,700 mm)"]),
        ("*Weight", "KG", [4300, 5350]),
    ]),
]
CAT["tt-vmc"] = ["VMC8046: stable design; resin-sand cast body; rolling guideways on X, Y; rectangular hardened sliding guideways on Z; high-quality linear guideways",
                 "VMC10562: wide bed, heavy column; roller-type linear guideways on all 3 axes (load, rigidity, damping); floating-cushion tool unclamping that protects the spindle bearings; oil separation keeps coolant clean; 24-tool changer",
                 "CNC100/120: optoelectronics and photovoltaic industry — grooving quartz; patented spindle structure; outboard chip / slurry collection"]

TAB["tt-boring"] = [
    table("TXK68 · TXK160 · TXK160B · TXK160D · TH-800", "CNC boring and milling machines, BT50 / MT5", ["TXK68", "TXK160", "TXK160B", "TXK160D", "TH-800"], [
        ("*Table", "TXT", ["36.2 × 32.3″ (920 × 820 mm), worm-gear dividing", "51.2 × 23.6″ (1,300 × 600 mm)", "51.2 × 23.6″ (1,300 × 600 mm), rotary", "51.2 × 23.6″ (1,300 × 600 mm); optional rotary 4th axis 23.6 × 19.7″ (600 × 500 mm)", "31.5 × 31.5″ (800 × 800 mm), B axis 360°"]),
        ("*Travel X × Y × Z", "TXT", ["31.5 × 23.6 × 39.4″ (800 × 600 × 1,000 mm)", "41.3 (59.1 optional) × 31.5 × 19.7″ (1,050 (1,500) × 800 × 500 mm)", "41.3 (59.1 optional) × 31.5 × 19.7″ (1,050 (1,500) × 800 × 500 mm)",
                                     "41.3 × 63 × 19.7″ (1,050 × 1,600 × 500 mm)", "X 47.2″ (1,200 mm), Z 39.4″ (1,000 mm)"]),
        ("Spindle taper", "TXT", ["MT5 or BT50", "BT50", "BT50", "BT50", "BT50"]),
        ("*Spindle speed", "TXT", ["25 – 760 rpm, 9 speeds", "Up to 3,000 rpm", "Up to 3,000 rpm", "Up to 3,000 rpm", "—"]),
        ("*Spindle motor", "TXT", ["7.5 HP (5.5 kW)", "7.5 / 10 HP (5.5 / 7.5 kW)", "7.5 / 10 HP (5.5 / 7.5 kW)", "7.5 / 10 HP (5.5 / 7.5 kW)", "7.5 / 10 HP (5.5 / 7.5 kW)"]),
        ("Rapid traverse", "TXT", ["472 ipm (12 m/min)", "709 ipm (18 m/min)", "709 ipm (18 m/min)", "709 ipm (18 m/min)", "472 ipm (12 m/min) X, Z; 394 ipm (10 m/min) Y"]),
        ("Positioning / repeatability", "TXT", ["±0.0006″ / ±0.0002″ (±0.015 / ±0.005 mm)"] * 4 + ["0.0004″ / 0.0002″ (0.01 / 0.005 mm)"]),
        ("Tool changer", "TXT", ["—", "—", "—", "Optional tool magazine", "40-tool chain magazine, 13 s change"]),
        ("CNC control", "TXT", "Mitsubishi E60 / M64AS or Fanuc (to order)"),
        ("Machine size L × W × H", "TXT", ["136 × 83 × 113″ (3,450 × 2,100 × 2,880 mm)", "104 × 118 × 98″ (2,650 × 3,000 × 2,500 mm)", "104 × 118 × 98″ (2,650 × 3,000 × 2,500 mm)",
                                            "104 × 118 × 98″ (2,650 × 3,000 × 2,500 mm)", "236 × 228 × 138″ (6,000 × 5,800 × 3,500 mm)"]),
        ("*Weight", "KG", [6000, 6800, 7000, 6800, 16500]),
    ]),
]
CAT["tt-boring"] = ["TXK68: 4-axis CNC boring and milling — steps, arcs and curved surfaces; boring, milling, drilling, tapping for small and medium parts; hardened rectangular guideways; table on double guides with worm-gear dividing; multi-face machining in one set-up",
                    "TXK160/B: fixed column — drilling, reaming, tapping, milling, boring; large table, long cross travel; heavy linear guideways on X, Y, hardened box ways on Z; B axis (4th) with 360° division",
                    "TXK160D: fixed-column horizontal type, simultaneous X/Y/Z; heavy linear guides and servo drives; HT300-type box castings; optional B axis and tool magazine",
                    "TH-800: roller-type guideways; 4-axis simultaneous; double-pitch worm and gear for the rotary table; 40-tool chain ATC, 13 s"]

# ------------------------------------------------------------------------------------------------ sheet metal: combination machines, circle shears
# PDF p47 (089 – 090)
TAB["tt-3in1"] = [
    table("Mini shear brake 8″ · 3-IN-1/200 – 760", "Bench shear, brake and slip roll machines, 8 – 30″", ["Mini shear brake 8″", "3-IN-1/200", "3-IN-1/305", "3-IN-1/610", "3-IN-1/760"], [
        ("*Working width", "L", [200, 200, 305, 610, 760]),
        ("*Shear / brake / roll capacity, mild steel", "TXT", ["20 ga (1 mm) copper and brass, 18 ga (1.2 mm) aluminum — shear and brake", "20 ga (1 mm)", "20 ga (1 mm)", "20 ga (1 mm)", "20 ga (1 mm)"]),
        ("Bending angle, max", "TXT", "90°"),
        ("*Min. rolling diameter", "TXT", ["—", "Ø1-1/8″ (29 mm)", "Ø1-1/2″ (39 mm)", "Ø1-1/2″ (39 mm)", "Ø1-1/2″ (39 mm)"]),
        ("Packing size L × W × H", "PK", [(50, 32, 17), (36, 25, 30), (50, 40, 35), (84, 41, 66), (100, 45, 72)]),
        ("*Weight", "KG", [13, 17, 43, 112, 136]),
    ]),
    table("3-IN-1/1016 – 1320", "Floor shear, brake and slip roll machines, 40 – 52″", ["3-IN-1/1016", "3-IN-1/1067", "3-IN-1/1320", "3-IN-1/1067×1.5", "3-IN-1/1320×1.5"], [
        ("*Working width", "L", [1016, 1067, 1320, 1067, 1320]),
        ("*Shear / brake / roll capacity, mild steel", "T", [1.0, 1.0, 1.0, 1.5, 1.5]),
        ("Bending angle, max", "TXT", "90°"),
        ("*Min. rolling diameter", "D", [40, 42, 50, 60, 70]),
        ("Packing size L × W × H", "PK", [(135, 45, 72), (139, 54, 78), (168, 54, 78), (150, 59, 93), (179, 59, 94)]),
        ("*Weight", "KG", [195, 276, 349, 390, 470]),
    ]),
]
CAT["tt-3in1"] = ["mini shear brake 8″: bends and shears in one compact tool; copper and brass 1 mm, aluminum 1.2 mm (18 ga); blade 200 mm; mounting base 230 × 125 mm; bends to 90°",
                  "3-IN-1/305: combination machine for sheet to 305 mm and 1 mm; rolls from Ø39 mm; folds to 90°; adjustable rear stop",
                  "3-IN-1/1016 etc.: removable segmented upper dies (fingers) for box and pan work; back gauge standard; two handle positions; shears mild steel; slip roll with wire grooves; ×1.5 heavy-duty, 1.5 mm"]

# PDF p48 (091 – 092)
TAB["tt-e3in1"] = [
    table("E3-IN-1/1320 · E3-IN-1/2040", "Motorized shear, brake and roll machines, 1/8″ shear, 52 – 80″", ["E3-IN-1/1320", "E3-IN-1/2040"], [
        ("*Shearing capacity × width", "TXT", ["1/8″ (3 mm) × 52″ (1,320 mm)", "1/8″ (3 mm) × 80.3″ (2,040 mm)"]),
        ("Shearing angle / strokes per minute", "TXT", "2° / 30 per min"),
        ("Back gauge range", "TXT", "17.7″ (450 mm), digital readout"),
        ("*Bending capacity × width", "TXT", ["14 ga (2 mm) × 52″ (1,320 mm)", "14 ga (2 mm) × 80.3″ (2,040 mm)"]),
        ("*Rolling capacity × width", "TXT", ["12 ga (2.5 mm) × 59″ (1,500 mm)", "12 ga (2.5 mm) × 82.7″ (2,100 mm)"]),
        ("Min. rolling diameter", "D", [90, 120]),
        ("Work table height", "L", [760, 760]),
        ("*Motor", "TXT", ["4.7 HP (3.5 kW)", "5.5 HP (4 kW)"]),
        ("Packing size L × W × H", "PK", [(254, 145, 197), (320, 152, 206)]),
        ("*Weight", "KG", [2435, 3345]),
    ]),
]
CAT["tt-e3in1"] = ["combination of shear, brake and roll in a heavy structure; easy taper (cone) rolling; single stroke or continuous for shearing and bending; back gauge with digital readout for quick, exact settings; function selector brake / shear / roll; top roll quick release; back gauge hand wheel"]

TAB["tt-mcs"] = [
    table("MCS-1250E", "Motorized circle shear, Ø8 – 49″ discs", ["MCS-1250E"], [
        ("*Sheet thickness, max", "T", [3.5]),
        ("*Disc diameter", "TXT", ["Ø7-7/8 – 49-1/4″ (200 – 1,250 mm)"]),
        ("*Motors", "TXT", ["3 HP (2.2 kW) main, 1.5 HP (1.1 kW) feed"]),
        ("Packing size L × W × H", "PK", [(207, 75, 146)]),
        ("*Weight", "KG", [750]),
    ]),
]
CAT["tt-mcs"] = ["cuts metal, paper and more; solid cast-iron construction; special-steel blades in bronze bearings — hardened, adjustable and regrindable; ball-screw radius setting, high precision; encoder shows the cutting radius; pneumatic clamping of the blank"]

# PDF p49 (093 – 094) — manual circle shears, circle cutting and flanging
TAB["tt-hcs"] = [
    table("MCS1.0x1000 · HCS10/10 · ECS10/10", "Manual and motorized circle shears; HCS / ECS cut discs and flange rims", ["MCS1.0x1000", "HCS10/10", "ECS10/10"], [
        ("*Sheet thickness, max", "T", [1.0, 1.5, 1.5]),
        ("*Disc diameter", "TXT", ["Ø4 – 39-3/8″ (100 – 1,000 mm)", "Ø5-7/8 – 19-3/4″ (150 – 500 mm)", "Ø5-7/8 – 19-3/4″ (150 – 500 mm)"]),
        ("Throat depth", "TXT", ["—", "19.7″ (500 mm)", "19.7″ (500 mm)"]),
        ("Flanging height, max", "TXT", ["—", "5/16″ (8 mm)", "5/16″ (8 mm)"]),
        ("*Drive", "TXT", ["Hand crank", "Hand crank; hand-wheel infeed of the upper roll", "1/2 / 3/4 HP (0.37 / 0.55 kW) two-speed motor, foot pedal"]),
        ("Packing size L × W × H", "PK", [(115, 28, 60), (144, 47, 160), (151, 57, 160)]),
        ("*Weight", "KG", [70, 120, 165]),
    ]),
]
CAT["tt-hcs"] = ["MCS1.0x1000: manual circle shear for metal, paper and other materials; solid cast-iron construction; hardened cutters, adjustable and regrindable",
                 "HCS10/10: easy manual control; manual clamping of the blank; 2 standard roller sets: cutting and flanging; hand-wheel infeed of the upper cutting roll",
                 "ECS10/10: electric, two speeds; foot pedal; 2 roller sets: cutting and flanging; optional flanging device for outside and inside rims"]

TAB["tt-mms"] = [
    table("MMS-1 · MMS-2 · MMS-3", "Bench shears for sheet, strip and wire", ["MMS-1", "MMS-2", "MMS-3"], [
        ("*Shearing capacity, mild steel", "T", [1.5, 2.0, 3.0]),
        ("Packing size L × W × H", "PK", [(32, 10, 13), (19, 18, 24), (32, 24, 34)]),
        ("*Weight", "KG", [2, 9, 21]),
    ]),
    table("MMS-4 · MMS-5 · MMS-6", "Throatless rack-and-pinion bench shears — cut straight lines, curves and shapes", ["MMS-4", "MMS-5", "MMS-6"], [
        ("*Capacity, mild steel", "T", [2.0, 3.0, 4.0]),
        ("*Capacity, stainless steel", "T", [1.5, 2.0, 3.0]),
        ("Length of cut per stroke", "F", [70, 80, 110]),
        ("Lower blade length", "F", [105, 108, 140]),
        ("Throat", "F", [105, 116, 150]),
        ("Handle length", "F", [442, 590, 720]),
        ("Packing size L × W × H", "PK", [(51, 33, 22), (38, 26, 69), (38, 26, 82)]),
        ("*Weight", "KG", [8, 15, 26]),
    ]),
]
CAT["tt-mms"] = ["MMS-4/5/6: alloy-steel rack and pinion — great power with little effort; removable handle; alloy-steel body for rigidity; adjustable hold-down (MMS-6); top-grade blades with correct rake for clean, burr-free cuts, adjustable and quickly changed; alloy-steel pivot; 2-point lower blade adjustment; shoulder shape lets you turn the work to any shape; keyed lower blade clamp; steel base drilled for bench or stand"]

# PDF p50 – p51 (095 – 098)
TAB["tt-hs"] = [
    table("HS-5 – HS-12 · HSG-8", "Lever shears for plate, flat bar and round bar", ["HS-5", "HS-6", "HS-8", "HS-10", "HS-12", "HSG-8"], [
        ("*Blade length", "TXT", ["5″", "6″", "8″", "10″", "12″", "8″"]),
        ("*Plate, mild steel", "T", [6.0] * 6),
        ("Flat bar", "R", [(70, 6)] * 6),
        ("Round bar", "D", [11, 11, 13, 13, 13, 13]),
        ("Packing size L × W × H", "PK", [(40, 37, 17), (40, 37, 17), (42, 41, 16), (54, 48, 15), (54, 48, 15), (50, 16, 45)]),
        ("*Weight", "KG", [9, 10, 17, 21, 26, 19]),
    ]),
    table("MS-20 · MS-24 · MS-28 · MS-32", "Hand bar cutters for round, square and flat bar", ["MS-20", "MS-24", "MS-28", "MS-32"], [
        ("*Round bar", "D", [20, 24, 28, 32]),
        ("Square bar", "R", [(18, 18), (20, 20), (24, 24), (28, 28)]),
        ("Flat bar", "R", [(30, 8), (35, 12), (40, 12), (40, 14)]),
        ("Packing size L × W × H", "PK", [(41, 37, 20), (41, 37, 20), (45, 24, 45), (46, 25, 45)]),
        ("*Weight", "KG", [16, 25, 34, 46]),
    ]),
    table("PBS-8 · PBS-7 · PBS-9", "Bar and section shears — angle, T, flat, round and square; PBS-9 also punches", ["PBS-8", "PBS-7", "PBS-9"], [
        ("*Round bar", "D", [16, 22, 22]),
        ("Square bar", "R", [(16, 16), (20, 20), (20, 20)]),
        ("*Flat bar", "R", [(100, 10), (90, 14), (90, 14)]),
        ("Angle", "R", [(40, 6), (60, 7), (60, 7)]),
        ("T-section", "R", [(40, 6), (60, 7), (60, 7)]),
        ("Plate", "T", [8.0, 10.0, 10.0]),
        ("Punching", "TXT", ["—", "—", "14 ga (2 mm) sheet, throat 6.3″ (160 mm)"]),
        ("Packing size L × W × H", "PK", [(65, 24, 55), (87, 37, 62), (106, 36, 84)]),
        ("*Weight", "KG", [45, 96, 130]),
    ]),
]
CAT["tt-hs"] = ["HSG: lever arm with compensating spring; easy cutting along the whole blade; rigid cutter body",
                "MS: for plate, rod and flat bar; durable steel frame, hardened high-carbon steel blade; bolts to a bench or table; blade easily replaced; standard handle",
                "PBS: rigid, versatile cutter for sheet, flat bar, round / square / angle bar and T-sections; rigid height-adjustable hold-down; PBS-9 cuts and punches, round, square or similar punches, for the sheet-metal shop"]

TAB["tt-hs300"] = [
    table("HS-300 · HS-500 – HS-1300", "Hand guillotine shears for thin sheet and plastic, 12 – 52″", ["HS-300", "HS-500", "HS-800", "HS-1000", "HS-1300"], [
        ("*Working width", "L", [305, 500, 800, 1000, 1300]),
        ("*Capacity, mild steel", "TXT", ["20 ga (1 mm) full width, 18 ga (1.2 mm) half width", "16 ga (1.5 mm)", "16 ga (1.5 mm)", "16 ga (1.5 mm)", "16 ga (1.5 mm)"]),
        ("Back gauge", "TXT", ["0 – 7″ (0 – 180 mm)", "—", "—", "—", "—"]),
        ("Packing size L × W × H", "PK", ["18 × 17 × 26″ (46 × 44 × 67 cm) overall", (79, 27, 45), (112, 28, 54), (138, 28, 54), (170, 28, 54)]),
        ("*Weight", "KG", [21, 36, 41, 52, 70]),
    ]),
    table("GS-1000 · GS-1000I · KHS-1000 · KHS-1250 · TSC1010/1.6", "Manual lever guillotine shears on stand, 40 – 49″", ["GS-1000", "GS-1000I", "KHS-1000", "KHS-1250", "TSC1010/1.6"], [
        ("*Working width", "L", [1000, 1000, 1000, 1250, 1010]),
        ("*Capacity, mild steel", "T", [1.0, 1.0, 1.0, 1.0, 1.6]),
        ("Frame", "TXT", ["Steel plate", "Cast iron", "Steel plate", "Steel plate", "Steel plate"]),
        ("Table height", "L", [800, 760, 750, 750, 760]),
        ("Packing size L × W × H", "PK", [(155, 100, 58), (162, 102, 50), (187, 110, 69), (212, 110, 69), (150, 105, 117)]),
        ("*Weight", "KG", [238, 385, 460, 560, 335]),
    ]),
]
CAT["tt-hs300"] = ["HS-300: 12″ working width; precise cutting; rigid and compact; adjustable rear stop; hand control", "HS-500 – 1300: hand lever, simple; for thin sheet; metal and plastic sheet; max. 1.5 mm",
                   "GS/KHS/TSC: fast clamping device; back gauge set by hand wheel; counter-balance weight on the lever (spring on GS-1000)"]

# PDF p52 (099 – 100) — foot shears
TAB["tt-q01"] = [
    table("Q01 foot shears", "Foot-operated shears, 20 – 14 ga × 40 – 98″", ["Q01-1.0x1000", "Q01-2x1000", "Q01-2x1000A", "Q01-1.5x1320", "Q01-1.5x1320A", "Q01-1.6x1320B", "Q01-1.2x2500B"], [
        ("*Working width", "L", [1000, 1000, 1000, 1320, 1320, 1320, 2500]),
        ("*Capacity, mild steel", "T", [1.0, 2.0, 2.0, 1.5, 1.5, 1.6, 1.2]),
        ("*Back gauge range", "TXT", ["0 – 27.6″ (0 – 700 mm)", "0 – 27.6″ (0 – 700 mm)", "0 – 31.5″ (0 – 800 mm)", "0 – 27.6″ (0 – 700 mm)", "0 – 31.5″ (0 – 800 mm)", "31.5″ (800 mm)", "31.5″ (800 mm)"]),
        ("Frame", "TXT", ["Cast", "Cast", "Welded steel", "Cast", "Welded steel", "Welded steel, light duty", "Welded steel, light duty"]),
        ("Packing size L × W × H", "PK", [(140, 76, 115), (140, 76, 115), (140, 76, 115), (168, 76, 120), (168, 76, 115), (180, 60, 120), (300, 60, 120)]),
        ("*Weight", "KG", [365, 405, 355, 454, 430, 410, 740]),
    ]),
]
CAT["tt-q01"] = ["cast models: front and back gauge; heavy, stable; high-carbon chrome-steel blade; cast frame does not deform; for mild steel, aluminum, copper, brass, zinc, plastic and lead",
                 "A models: fully welded steel frame; strong cutting with less effort; adjustable-length foot pedal, low pedal height; back gauge standard; optional rear safety cage",
                 "B models: steel fabrication; spring-loaded hold-down beam; light duty, cost-effective; adjustable blade gap for thin material; front sheet supports and back gauge with scale"]

# PDF p53 (101 – 102)
TAB["tt-bq01"] = [
    table("BQ01 · BQF01 · EBQ01", "Bench shears — hand lever, foot pedal or motorized, 20 – 18 ga × 26 – 41″", ["BQ01-1.25x650", "BQ01-1.0x1050", "BQF01-1.25x650", "BQF01-1.0x1050", "EBQ01-1.25x650", "EBQ01-1.0x1050"], [
        ("*Working width", "L", [650, 1050, 650, 1050, 650, 1050]),
        ("*Capacity, mild steel", "T", [1.25, 1.0, 1.25, 1.0, 1.25, 1.0]),
        ("*Operation", "TXT", ["Hand lever", "Hand lever", "Foot pedal", "Foot pedal", "Motor 1 HP (0.75 kW), foot switch", "Motor 1 HP (0.75 kW), foot switch"]),
        ("Back gauge range", "TXT", "0 – 19.7″ (0 – 500 mm)"),
        ("Packing size L × W × H", "PK", [(93, 47, 58), (133, 40, 63), (92, 80, 113), (132, 80, 113), (105, 65, 63), (140, 65, 65)]),
        ("*Weight", "KG", [91, 135, 155, 175, 185, 238]),
    ]),
    table("Q01 hand shears", "Two-handle lever shears on stand, 22 – 16 ga × 41 – 98″", ["Q01-1.5x1050", "Q01-1.5x1500", "Q01-1.25x2000", "Q01-0.8x2500"], [
        ("*Working width", "L", [1050, 1500, 2000, 2500]),
        ("*Capacity, mild steel", "T", [1.5, 1.5, 1.25, 0.8]),
        ("Back gauge range", "TXT", "0 – 11.8″ (0 – 300 mm)"),
        ("Packing size L × W × H", "PK", [(161, 75, 120), (208, 75, 120), (258, 75, 120), (308, 76, 120)]),
        ("*Weight", "KG", [378, 460, 511, 557]),
    ]),
]
CAT["tt-bq01"] = ["BQ01: hand lever; working light; mild steel, aluminum, copper, brass, zinc, plastic and lead; high-carbon chrome-steel blade",
                  "BQF01: foot control; working light; back gauge standard; optional rear safety cage", "EBQ01: cutting line light, front angle stop, foot switch and adjustable back stop with scale standard; optional stand",
                  "Q01 hand shears: two hand levers; mild steel, aluminum, copper, brass, zinc, plastic and lead; high-carbon chrome-steel blade"]

# ------------------------------------------------------------------------------------------------ notchers
# PDF p54 – p55 (103 – 106)
TAB["tt-notch-hand"] = [
    table("HN-3 · HN-4 · HN-3/102 · FN1.5x80", "Hand and foot corner notchers, 90°", ["HN-3", "HN-4", "HN-3/102", "FN1.5x80"], [
        ("*Capacity, mild steel", "T", [1.5, 1.5, 3.0, 1.5]),
        ("*Notch size", "R", [(125, 125), (152, 152), (100, 100), (80, 80)]),
        ("Notch angle", "TXT", "90°"),
        ("Ram stroke", "F", [25, 20, 30, 25]),
        ("Operation", "TXT", ["Hand lever", "Hand lever (stand optional)", "Hand lever", "Foot pedal, on stand"]),
        ("Packing size L × W × H", "PK", [(43, 37, 44), (58, 53, 52), (44, 42, 78), (115, 51, 40)]),
        ("*Weight", "KG", [27, 75, 90, 74]),
    ]),
]
TAB["tt-pnm"] = [
    table("PNM-130 · PNM-150", "Pneumatic 90° corner notchers on stand", ["PNM-130", "PNM-150"], [
        ("*Notch size", "R", [(130, 130), (150, 150)]),
        ("*Capacity, mild steel", "T", [3.0, 2.0]),
        ("Table size", "TXT", "23.6 × 18.1″ (600 × 460 mm), cast iron"),
        ("Operation", "TXT", "Shop air, roving foot pedal"),
        ("*Weight", "KG", [188, 190]),
    ]),
]
CAT["tt-pnm"] = ["free-standing pneumatic notcher cuts 130 × 130 × 3 mm mild steel effortlessly; transparent blade guard lets the operator line up scribed lines quickly and accurately; adjustable stops and guides on both sides of the blade; adjustable pressure regulator and water filter trap; heavy cast-iron table; roving foot pedal"]

TAB["tt-hnm"] = [
    table("HNM-6 · HNM-6A", "Hydraulic corner notchers, 1/4″ — fixed 90° or adjustable 30 – 135°", ["HNM-6", "HNM-6A"], [
        ("*Capacity, mild steel", "T", [6.5, 6.0]),
        ("*Notch length", "TXT", ["9.8 × 9.8″ (250 × 250 mm)", "7.9″ (200 mm)"]),
        ("*Notch angle", "TXT", ["90° fixed", "30 – 135° adjustable"]),
        ("Strokes per minute", "TXT", ["24", "—"]),
        ("Punching", "TXT", ["—", "Up to Ø1-9/16″ (40 mm)"]),
        ("Table size", "TXT", ["31.9 × 29.5″ (810 × 750 mm)", "—"]),
        ("*Motor", "KW", [4.0, 4.0]),
        ("Hydraulics", "TXT", ["1,740 psi (12 MPa), 9.2 US gal (35 L) tank", "2,611 psi (18 MPa)"]),
        ("Packing size L × W × H", "PK", [(101, 85, 137), (120, 105, 142)]),
        ("*Weight", "KG", [630, 1020]),
    ]),
]
CAT["tt-hnm"] = ["HNM-6: cuts up to 6.5 mm; 250 × 250 mm notch; fixed 90°, high notching speed; compact; easy to run; automatic blade clearance; chips slide down a chute; sheet hold-down",
                 "HNM-6A: fast and precise; for many thicknesses and materials; angle 30 – 135° set by hand wheels; punching up to Ø40 mm; gauges for locating the sheet; sheet hold-down for a good cut edge; automatic blade clearance"]

# ------------------------------------------------------------------------------------------------ CNC plasma
# PDF p61 (117 – 118)
TAB["tt-plasma"] = [
    table("PC 2′×2′ · PC 2′×4′", "Compact CNC plasma tables with stepper drives", ["PC 2′×2′", "PC 2′×4′"], [
        ("*Cutting area", "TXT", ["24 × 24″ (610 × 610 mm)", "24 × 48″ (610 × 1,220 mm)"]),
        ("*Cutting thickness", "TXT", "3/8″ (10 mm) with a 40 A source, 1″ (26 mm) with 100 A"),
        ("Cutting speed", "TXT", "0 – 236 ipm (0 – 6,000 mm/min)"),
        ("Z-axis stroke", "L", [150, 150]),
        ("Accuracy", "TXT", "±0.04″ per 39″ (±1 mm per 1,000 mm)"),
        ("*Drive", "TXT", "Stepper motors, lead screws; hand-held controller with USB"),
        ("Power", "TXT", "6 / 11 kW (with the plasma source)"),
        ("Packing size L × W × H", "PK", [(117, 112, 130), (185, 115, 132)]),
        ("*Weight", "KG", [180, 255]),
    ]),
    table("PC 4′×4′ · PC 5′×10′", "CNC plasma tables with servo drives and automatic torch height control", ["PC 4′×4′", "PC 5′×10′"], [
        ("*Cutting area", "TXT", ["48 × 48″ (1,220 × 1,220 mm)", "60 × 120″ (1,524 × 3,048 mm)"]),
        ("*Cutting thickness", "TXT", "5/16″ (8 mm) at 45 A, 3/8″ (10 mm) at 65 A, 1/2″ (12 mm) at 85 A"),
        ("Z-axis stroke", "L", [150, 150]),
        ("Accuracy / repeatability", "TXT", "±0.006″ / ±0.004″ (±0.15 / ±0.1 mm)"),
        ("*Drive", "TXT", ["Servo motors, lead screws; water table", "Servo motors, rack and gear; downdraft dust collection"]),
        ("Table load", "TXT", "Plate up to 1″ (25.4 mm) mild steel"),
        ("Connected load", "TXT", "6 / 9 / 12 kW"),
        ("Packing size L × W × H", "TXT", ["83 × 81 × 64″ (210 × 205 × 162 cm) machine, 32 × 28 × 59″ (81 × 70 × 150 cm) CNC console", "154 × 87 × 61″ (392 × 221 × 155 cm) machine, 33 × 31 × 61″ (84 × 78 × 156 cm) CNC console"]),
        ("*Weight", "TXT", ["1,411 lb (640 kg) + 154 lb (70 kg) console", "3,748 lb (1,700 kg) + 220 lb (100 kg) console"]),
    ]),
]
CAT["tt-plasma"] = ["PC 2×2 / 2×4: cuts steel, aluminum, galvanized and coated sheet and other conductive metals; water-assisted cooling; fully welded frame; industrial cable track on X; hardened ground slideways with wipers on X, Y; stepper motors on X, Y; hand-held controller, plasma source and torch; USB — runs without a computer; easy programming software",
                    "PC 4×4 / 5×10: precision guides with servo motors on X and Y; Z axis with automatic height detection; welded frame carries plate up to 1″; control console with programming; 4×4 with water pans, 5×10 with downdraft dust collector; plasma source of other brands (e.g. Hypertherm) optional"]

# PDF p62 (119 – 120)
TAB["tt-pcp"] = [
    table("PCP 300×3000E · PCP 300×3000 · PCP 300×6000", "CNC plasma pipe cutting machines, Ø2 – 11-3/4″ pipe", ["PCP 300×3000E", "PCP 300×3000", "PCP 300×6000"], [
        ("*Pipe diameter", "TXT", "Ø2 – 11-3/4″ (50 – 300 mm)"),
        ("*Pipe length", "TXT", ["10 ft (3,000 mm)", "10 ft (3,000 mm)", "20 ft (6,000 mm)"]),
        ("*Wall thickness", "TXT", "0.04 – 1/2″ (1 – 12 mm)"),
        ("Pipe weight, max", "TXT", ["661 lb (300 kg)", "101 lb/ft (150 kg/m)", "101 lb/ft (150 kg/m)"]),
        ("Cutting speed", "TXT", "200 ipm (5.08 m/min)"),
        ("Travel speed / rotation", "TXT", "394 ipm (10 m/min) / up to 100 rpm"),
        ("Pipe support", "TXT", ["Chuck at both ends; removable chip tray; dust exhaust on both sides", "Gas-spring chuck supports, ball-transfer cradles", "Gas-spring chuck supports, ball-transfer cradles"]),
        ("Air supply", "TXT", "86 – 135 psi (5.9 – 9.3 bar)"),
        ("Packing size L × W × H", "PK", [(470, 110, 160), (417, 112, 140), (417, 145, 140)]),
        ("*Weight", "KG", [1250, 990, 1200]),
    ]),
]
CAT["tt-pcp"] = ["300×3000E: new European design; economical CNC plasma pipe cutting for OD 50 – 300 mm; easy programming, no special skills; modular bed extensions for longer pipe; removable chip tray; pipe held by chucks at both ends for parallelism and precision; powerful dust exhaust on both sides",
                 "300×3000 / 300×6000: adjustable gas-shock chuck supports set the chuck height for smooth, level rotation of different diameters; adjustable ball-transfer cradles load the pipe easily; modular bed extensions"]

# ------------------------------------------------------------------------------------------------ brakes (folders)
# PDF p63 (121 – 122)
TAB["tt-eb"] = [
    table("EB625 – EB3200", "Magnetic sheet metal brakes, 2 to 10 ft", ["EB625", "EB1000", "EB1250", "EB2000", "EB2500", "EB3200"], [
        ("*Capacity, length × mild steel", "TXT", ["2 ft × 16 ga (625 × 1.6 mm)", "3 ft × 16 ga (1,000 × 1.6 mm)", "4 ft × 16 ga (1,250 × 1.6 mm)", "6 ft × 16 ga (2,000 × 1.6 mm)",
                                                   "8 ft × 16 ga (2,500 × 1.6 mm)", "10 ft × 18 ga (3,200 × 1.2 mm)"]),
        ("*Clamping force", "TXT", ["3.3 US tons (3 t)", "5 US tons (4.5 t)", "6.6 US tons (6 t)", "9.9 US tons (9 t)", "13.2 US tons (12 t)", "11 US tons (10 t)"]),
        ("Bending edge length", "L", [670, 1050, 1300, 2090, 2590, 3290]),
        ("Distance between lifters", "L", [630, 1010, 1260, 2028, 2528, 3228]),
        ("Back gauge", "L", [390, 640, 640, 640, 640, 640]),
        ("Duty cycle / protection", "TXT", "30 % / thermal cut-out at 158 °F (70 °C)"),
        ("Rated current", "TXT", ["4 A", "6 A", "6 A", "12 A", "15 A", "15 A"]),
        ("Packing size L × W × H", "PK", [(83, 112, 38), (120, 112, 38), (145, 112, 38), (220, 112, 38), (270, 112, 38), (340, 112, 38)]),
        ("*Weight", "KG", [102, 142, 185, 259, 290, 381]),
    ]),
]
CAT["tt-eb"] = ["electromagnetic instead of mechanical clamping: a long electromagnet with a steel clamp bar above it clamps the sheet with 3 – 12 t; the bending beam swings the bend around the front edge of the clamp bar; four sets of clamp bars (full length, short set for boxes, narrow, slotted); foot switch standard; easy-raise clamp bar; unlimited box depth; multiple finger lengths; bending stop included; 19 mm min. return flange, 98 mm min. standard clamp bar"]

# PDF p64 (123 – 124)
TAB["tt-bsm"] = [
    table("BSM1016 · BSM1220 · BSM2540", "Folding brakes with slitter on folding stand, 40 – 100″", ["BSM1016", "BSM1220", "BSM2540"], [
        ("*Working length", "L", [1016, 1220, 2540]),
        ("*Bending and shearing capacity, mild steel", "T", [1.0, 0.8, 0.8]),
        ("Bending angle", "TXT", "0 – 135°"),
        ("Stand height", "L", [900, 900, 650]),
        ("Packing size L × W × H", "PK", [(145, 32, 24), (165, 31, 23), (300, 77, 51)]),
        ("*Weight", "KG", [62, 82, 230]),
    ]),
]
CAT["tt-bsm"] = ["works with aluminum, copper and steel; all-steel folding stand for transport and storage; the shearing (slitting) device is easy to take off"]

TAB["tt-alb"] = [
    table("ALB-2200 – ALB-3800", "Portable aluminum roofing brakes with roller slitter, 7 to 12-1/2 ft", ["ALB-2200", "ALB-2600", "ALB-2600A", "ALB-3200", "ALB-3200A", "ALB-3800"], [
        ("*Bending length", "TXT", ["7.2 ft (2,200 mm)", "8.5 ft (2,600 mm)", "8.5 ft (2,600 mm)", "10.5 ft (3,200 mm)", "10.5 ft (3,200 mm)", "12.5 ft (3,800 mm)"]),
        ("*Capacity", "TXT", "24 ga (0.7 mm) steel, 0.032″ (0.8 mm) aluminum"),
        ("Bending angle", "TXT", "0 – 180°"),
        ("*Throat (infeed depth)", "L", [580, 580, 485, 580, 485, 580]),
        ("Packing size L × W × H", "PK", [(229, 73, 28), (280, 75, 28), (280, 75, 28), (327, 77, 30), (327, 77, 30), (400, 75, 30)]),
        ("*Weight", "KG", [60, 76, 73, 89, 85, 106]),
    ]),
]
CAT["tt-alb"] = ["for profiles and sheet up to 0.7 mm — skates, sills, cornices, flashing; steel, brass, copper and other materials, including painted and coated sheet — the silicone insert in the bending beam does not mark the surface; easy thickness setting; anodized light-alloy frame — mobile and compact for the shop or the job site; set-up 10 – 15 minutes; secure blank clamping, bends to 180°; roller knife for cutting sheet"]

# PDF p65 (125 – 126)
TAB["tt-3in1a"] = [
    table("3-IN-1/760A · 1016A · 1320A", "Shear, brake and roll machines with separate bending section, 30 – 52″", ["3-IN-1/760A", "3-IN-1/1016A", "3-IN-1/1320A"], [
        ("*Working width", "L", [760, 1016, 1320]),
        ("*Shear / brake / roll capacity, mild steel", "T", [1.0, 1.0, 1.0]),
        ("Bending angle, max", "TXT", "90°"),
        ("*Min. rolling diameter", "D", [39, 40, 50]),
        ("Packing size L × W × H", "PK", [(106, 49, 51), (135, 45, 72), (167, 57, 62)]),
        ("*Weight", "KG", [128, 195, 334]),
    ]),
]
CAT["tt-3in1a"] = ["simple construction, easy operation; shears, rolls and bends; the bending section is independent and can be supplied separately; improved model — less effort when bending"]

TAB["tt-wb"] = [
    table("WB-14 · W1.2 bench brakes · ZWJ offset brakes", "Bench hand brakes and offset (jog) brakes, 14 – 40″", ["WB-14", "W1.2×460", "W1.2×610", "W1.2×760", "W1.2×1000", "ZWJ-20", "ZWJ-36"], [
        ("*Bending length", "TXT", ["14″ (356 mm)", "18″ (460 mm)", "24″ (610 mm)", "30″ (760 mm)", "39.4″ (1,000 mm)", "20″", "36″"]),
        ("*Capacity, mild steel", "TXT", ["20 ga (1 mm)", "18 ga (1.2 mm)", "18 ga (1.2 mm)", "18 ga (1.2 mm)", "18 ga (1.2 mm)", "20 ga — 1/2″ offsets to 90°; 18 ga aluminum", "20 ga"]),
        ("Bending angle", "TXT", ["0 – 90°", "0 – 90°", "0 – 135°", "0 – 90°", "0 – 135°", "90°", "90°"]),
        ("Packing size L × W × H", "PK", [(66, 24, 46), (50, 12, 6.5), (83, 21, 37), (90, 17, 12), (125, 27, 30), (72, 20, 12), (114, 19, 14)]),
        ("*Weight", "KG", [24, 4.5, 24, 14, 36, 16, 34]),
    ]),
]
CAT["tt-wb"] = ["simple construction, easy to move and use; C-clamp mounting optional (W1.2×460 / 760); up to 1.2 mm",
                "ZWJ offset brake: precision tool for offset (jog) bends; accurate 1/2″ offsets up to 90° in 20 ga steel and 18 ga aluminum up to 20″ wide; 18 ga steel in widths under 12″; bench or vise mount"]

# PDF p66 – p68 (127 – 132)
TAB["tt-hb"] = [
    table("HB-2248 · HB-2250 · HB-1650", "Hand brakes on stand, 48 – 50″", ["HB-2248", "HB-2250", "HB-1650"], [
        ("*Bending length", "TXT", ["48″ (1,220 mm)", "50″ (1,270 mm)", "50″ (1,270 mm)"]),
        ("*Capacity, mild steel", "TXT", ["22 ga (0.8 mm)", "22 ga (0.8 mm)", "16 ga (1.5 mm)"]),
        ("Beam lift, max", "TXT", ["1″ (25.4 mm)", "7/8″ (22 mm)", "1-1/4″ (32 mm)"]),
        ("Beam adjustment", "TXT", ["—", "1/8″ (3 mm)", "5/8″ (16 mm)"]),
        ("Packing size L × W × H", "PK", [(157, 67, 71), (168, 54, 71), (168, 59, 82)]),
        ("*Weight", "KG", [120, 142, 191]),
    ]),
    table("W1.0 · W1.2 straight hand brakes", "Bench and floor hand brakes with one-piece blade, 12 – 79″", ["W1.0×305", "W1.0×610", "W1.0×915", "W1.2×1220", "W1.2×1500", "W1.0×2000"], [
        ("*Bending length", "L", [305, 610, 915, 1220, 1500, 2000]),
        ("*Capacity, mild steel", "T", [1.0, 1.0, 1.0, 1.2, 1.2, 1.0]),
        ("Bending angle", "TXT", ["0 – 135°"] * 4 + ["0 – 140°"] * 2),
        ("Packing size L × W × H", "PK", [(51, 30, 35), (82, 30, 37), (116, 41, 59), (158, 39, 58), (200, 76, 125), (250, 76, 125)]),
        ("*Weight", "KG", [19, 29, 65, 90, 285, 410]),
    ]),
    table("W2.0 · W2.5 heavy hand brakes", "Floor hand brakes with one-piece blade, counterweights and stop rod, 4 – 13 ft", ["W2.5×1220N", "W2.0×2040", "W2.5×2040", "W2.0×2540", "W2.5×2540", "W2.0×3050", "W1.2×3700", "W0.8×4000"], [
        ("*Bending length", "TXT", ["48″ (1,220 mm)", "80″ (2,040 mm)", "80″ (2,040 mm)", "100″ (2,540 mm)", "100″ (2,540 mm)", "120″ (3,050 mm)", "146″ (3,700 mm)", "157″ (4,000 mm)"]),
        ("*Capacity, mild steel", "T", [2.5, 2.0, 2.5, 2.0, 2.5, 2.0, 1.2, 0.8]),
        ("Bending angle", "TXT", "0 – 135°"),
        ("Packing size L × W × H", "PK", [(171, 75, 94), (253, 75, 101), (255, 76, 100), (300, 76, 100), (300, 76, 100), (350, 77, 110), (425, 85, 120), (470, 90, 120)]),
        ("*Weight", "KG", [490, 925, 1010, 1070, 1165, 1490, 1800, 2200]),
    ]),
]
CAT["tt-hb"] = ["HB-2250/1650: for many sheet-forming jobs; precise bed and beam alignment for accurate work",
                "HB-2248: all-steel welded; adjustable truss bars and bronze bushings; removable nose bar; precise stop rod for repeat bends; folding stand standard",
                "W2.0/W2.5 heavy: one-piece blade; floor stand; stop rod and counterweights for easy folding"]

TAB["tt-pb"] = [
    table("W1.0A · W1.5 pan and box brakes", "Bench and floor pan and box brakes with removable fingers, 12 – 50″", ["W1.0×305A", "W1.0×610A", "W1.0×915A", "W1.5×1220", "W1.5×610Z", "W1.5×915Z", "W1.5×1220Z", "W1.5×1260A"], [
        ("*Bending length", "L", [305, 610, 915, 1220, 610, 915, 1220, 1260]),
        ("*Capacity, mild steel", "T", [1.0, 1.0, 1.0, 1.5, 1.5, 1.5, 1.5, 1.5]),
        ("Bending angle", "TXT", "0 – 135°"),
        ("Fingers", "TXT", ["Removable segments"] * 4 + ["Heavy-duty segments, many widths"] * 4),
        ("Packing size L × W × H", "PK", [(50, 35, 41), (82, 35, 44), (113, 35, 55), (158, 45, 66), (85, 37, 56), (117, 40, 58), (158, 45, 65), (158, 45, 65)]),
        ("*Weight", "KG", [28, 43, 80, 142, 51, 106, 166, 150]),
    ]),
    table("BP-1650 · BP-1648H", "Pan and box brakes, 16 ga × 48 – 50″, 4″ box depth", ["BP-1650", "BP-1648H"], [
        ("*Bending length", "TXT", ["50″ (1,270 mm)", "48″ (1,220 mm)"]),
        ("*Capacity, mild steel", "TXT", "16 ga (1.5 mm)"),
        ("*Box depth, max", "TXT", "4″ (100 mm)"),
        ("Finger (blade) height", "TXT", ["7-1/4″ (184 mm)", "7-3/4″ (198 mm)"]),
        ("Beam lift, max / adjustment", "TXT", ["1-1/4″ (32 mm) / 5/8″ (16 mm)", "1-1/4″ (32 mm) / 1/4″ (6.5 mm)"]),
        ("Bending angle", "TXT", "0 – 135°"),
        ("Packing size L × W × H", "PK", [(168, 59, 83), (166, 61, 72)]),
        ("*Weight", "KG", [205, 237]),
    ]),
    table("W1.5 · W1.2 · W2.0A · W2.5A floor pan and box brakes", "Floor pan and box brakes with segment blade and counterweights, 5 – 13 ft", ["W1.5×1500", "W1.2×2000", "W2.5×1220", "W2.0×2040A", "W2.5×2040A", "W2.0×2540A", "W2.5×2540A", "W2.0×3050A", "W1.2×3700A", "W0.8×4000A"], [
        ("*Bending length", "TXT", ["59″ (1,500 mm)", "79″ (2,000 mm)", "48″ (1,220 mm)", "80″ (2,040 mm)", "80″ (2,040 mm)", "100″ (2,540 mm)", "100″ (2,540 mm)", "120″ (3,050 mm)", "146″ (3,700 mm)", "157″ (4,000 mm)"]),
        ("*Capacity, mild steel", "T", [1.5, 1.2, 2.5, 2.0, 2.5, 2.0, 2.5, 2.0, 1.2, 0.8]),
        ("Bending angle", "TXT", ["0 – 140°", "0 – 140°"] + ["0 – 135°"] * 8),
        ("Packing size L × W × H", "PK", [(200, 75, 123), (250, 75, 123), (170, 75, 96), (254, 76, 102), (253, 75, 101), (300, 76, 102), (300, 76, 100), (360, 76, 102), (425, 85, 120), (470, 90, 120)]),
        ("*Weight", "KG", [445, 581, 495, 960, 1060, 1115, 1225, 1435, 2450, 2700]),
    ]),
]
CAT["tt-pb"] = ["W1.0A/W1.5: solid welded frame; removable segmented fingers; hardened steel dies repositioned for different jobs; Z: heavy duty, precise bending segments in many widths",
                "BP-1650: 184 mm fingers; sectioned fingers removed easily for boxes and special forming; with all fingers in, a full-length nose bar — a straight brake; counterweight saves effort; enlarged handle",
                "BP-1648H: 198 mm fingers; all-steel welded; adjustable truss bars, bronze bushings; removable nose bar; stop rod for repeat bends; stand standard",
                "floor pan & box: segment bending blade for box sections; segments of various widths, shiftable set-up; counterweights for easy folding"]

# PDF p69 – p70 (133 – 136)
TAB["tt-pb-heavy"] = [
    table("W1830×1.5P · W1.2×1500H · W1.5×2540H · WU2.0×2500", "Heavy pan and box brakes with counterweights, 5 – 8 ft", ["W1830×1.5P", "W1.2×1500H", "W1.5×2540H", "WU2.0×2500"], [
        ("*Bending length", "TXT", ["72″ (1,830 mm)", "59″ (1,500 mm)", "100″ (2,540 mm)", "100″ (2,500 mm)"]),
        ("*Capacity, mild steel", "T", [1.5, 1.2, 1.5, 2.0]),
        ("*Box depth / fingers", "TXT", ["Fingers 8 × 2″, 8 × 3″, 8 × 4″", "Fingers 4-7/8″ (125 mm) high", "Pans and boxes to 5-1/8″ (130 mm) deep; fingers 60 – 305 mm",
                                         "Fingers 75 mm (5) and 125 mm (17)"]),
        ("Clamping beam lift", "TXT", ["—", "2-3/8″ (60 mm)", "6-1/4″ (160 mm)", "—"]),
        ("Bending angle", "TXT", ["0 – 135°", "0 – 125°", "0 – 135°", "0 – 135°"]),
        ("Packing size L × W × H", "PK", [(243, 77, 104), (211, 75, 142), (350, 100, 184), (310, 104, 182)]),
        ("*Weight", "KG", [780, 460, 1100, 1370]),
    ]),
    table("W1.2 · W1.5 floor brakes, 40 – 51″", "Floor brakes with one-piece blade or segments", ["W1.2×1010", "W1.2×1040", "W1.2×1060", "W1.2×1300", "W1.5×1050", "W1.5×1050F"], [
        ("*Bending length", "L", [1010, 1040, 1060, 1300, 1050, 1050]),
        ("*Capacity, mild steel", "T", [1.2, 1.2, 1.2, 1.2, 1.5, 1.5]),
        ("Bending angle", "TXT", ["0 – 150°", "0 – 140°", "0 – 150°", "0 – 140°", "0 – 135°", "0 – 150°"]),
        ("Blade", "TXT", ["One-piece (segments available)", "One-piece or segments", "One-piece or segments", "Segments (one-piece available)", "Segments of various widths, sliding", "Segments of various widths, sliding"]),
        ("Packing size L × W × H", "PK", [(130, 77, 52), (141, 73, 125), (144, 77, 110), (157, 76, 52), (144, 77, 110), (145, 70, 131)]),
        ("*Weight", "KG", [118, 80, 132, 118, 185, 294]),
    ]),
    table("PBB1020/1A · PBB1250/1A · light brakes · WF1.0", "Folding machines for light sheet, 36 – 118″", ["PBB1020/1A", "PBB1250/1A", "36″ brake", "40″ brake", "48″ brake", "72″ brake", "WF1.0×2020", "WF1.0×2500", "WF1.0×3000"], [
        ("*Bending length", "L", [1020, 1250, 915, 1016, 1220, 1830, 2020, 2500, 3000]),
        ("*Capacity, mild steel", "TXT", ["20 ga (1 mm)", "20 ga (1 mm)", "Light gauge — ask us", "Light gauge — ask us", "20 ga", "22 ga", "20 ga (1 mm)", "20 ga (1 mm)", "20 ga (1 mm)"]),
        ("Bending angle", "TXT", ["0 – 135°", "0 – 135°", "0 – 120°", "0 – 120°", "0 – 120°", "0 – 120°", "0 – 135°", "0 – 135°", "0 – 135°"]),
        ("Packing size L × W × H", "PK", [(136, 52, 68), (162, 69, 45), (123, 24, 50), (134, 24, 50), (153, 24, 53), (217, 36, 64), (245, 95, 63), (307, 94, 62), (358, 94, 63)]),
        ("*Weight", "KG", [135, 115, 68, 70, 76, 145, 470, 550, 640]),
    ]),
]
CAT["tt-pb-heavy"] = ["WU2.0×2500: all-steel welded; two heavy counterweights; fingers 75 mm (5) and 125 mm (17), easy to remove; beam adjustment; stop rod",
                      "W1830×1.5P: 72″ × 16 ga; fingers 8 @ 2, 3 and 4″; counterweights for easy bending",
                      "W1.2×1500H: 125 mm high fingers; all-steel welded; counterweight stops in any position; precision angle stop",
                      "W1.5×2540H: heavy steel frame for accurate bends; extended fingers for pans and boxes to 130 mm deep; quick beam adjustment; two counterweights, stop in any position; fingers 60, 75, 95, 100, 105, 125, 145, 150, 305 mm",
                      "36/40/48/72″ brakes: floor stand; compact; for light-gauge sheet (catalogue lists 12 ga for 36/40″ — to be confirmed)"]

# PDF p71 – p73 (137 – 142)
TAB["tt-pbb"] = [
    table("PBB foot-clamp folding machines", "Manual folding machines with foot-operated clamping beam, 40 – 99″", ["PBB1020/2.5", "PBB1020/2A", "PBB1020/3SH", "PBB1270/2", "PBB1270/2A", "PBB1270/3SH", "PBB1520/1.5", "PBB1520/1.5A", "PBB2020/1.2", "PBB2050/3SH", "PBB2520/1.0"], [
        ("*Bending length", "L", [1020, 1020, 1020, 1270, 1270, 1270, 1520, 1520, 2020, 2020, 2520]),
        ("*Capacity, mild steel", "T", [2.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.2, 1.0, 1.0]),
        ("Clamping beam lift", "L", [47, 47, 45, 47, 47, 45, 47, 47, 47, 47, 47]),
        ("Bending angle", "TXT", ["0 – 135°", "0 – 135°", "0 – 150°", "0 – 135°", "0 – 135°", "0 – 150°", "0 – 135°", "0 – 135°", "0 – 135°", "0 – 135°", "0 – 135°"]),
        ("Blades", "TXT", ["One-piece", "Segmented clamp and folding blades", "Segmented, quick-release clamp segments", "One-piece", "Segmented clamp and folding blades", "Segmented, quick-release clamp segments",
                           "One-piece", "Segmented clamp and folding blades", "One-piece", "Segmented, quick-release clamp segments", "One-piece"]),
        ("Packing size L × W × H", "PK", [(146, 63, 131), (146, 64, 131), (142, 59, 142), (171, 71, 131), (171, 71, 131), (167, 66, 142), (193, 68, 133), (196, 71, 130), (246, 95, 134), (248, 97, 154), (297, 94, 132)]),
        ("*Weight", "KG", [290, 325, 360, 340, 370, 420, 390, 395, 540, 750, 590]),
    ]),
    table("TSB · TSBS · TFS · MFS · MF", "Heavy manual folding machines, 6.7 – 10 ft", ["TSB 2020/2", "TSBS 2020/2", "TSB 2060/2", "TFS 2020B", "MFS 2020", "TSBS 2540/1.5", "TSBS 3020/1.2", "MF 3020"], [
        ("*Bending length", "TXT", ["80″ (2,020 mm)", "80″ (2,020 mm)", "81″ (2,060 mm)", "80″ (2,020 mm)", "80″ (2,020 mm)", "100″ (2,540 mm)", "119″ (3,020 mm)", "119″ (3,020 mm)"]),
        ("*Capacity, mild steel", "T", [2.0, 2.0, 2.0, 1.2, 1.5, 1.5, 1.2, 1.0]),
        ("Bending angle", "TXT", "0 – 135°"),
        ("Blades / clamping", "TXT", ["One-piece blade; lever-swung beam", "Segments 25 – 400 mm; lever-swung beam", "One-piece; cast-iron frame, counterweight", "Foot clamping", "Segments 25 – 500 mm; foot clamping",
                                      "Segments 25 – 400 mm", "Segments 25 – 400 mm", "One-piece; foot clamping"]),
        ("Packing size L × W × H", "PK", [(280, 71, 150), (280, 71, 152), (310, 76, 150), (248, 97, 154), (267, 84, 147), (337, 72, 150), (385, 72, 150), (365, 84, 147)]),
        ("*Weight", "KG", [1010, 1025, 1760, 650, 815, 1250, 1385, 980]),
    ]),
    table("EFM · EFMS electric folding machines", "Motorized clamping and folding, foot pedal, 6.7 – 10 ft", ["EFM 2020", "EFMS 2020", "EFM 2520", "EFMS 2520", "EFM 3020", "EFMS 3020"], [
        ("*Bending length", "TXT", ["80″ (2,020 mm)", "80″ (2,020 mm)", "100″ (2,520 mm)", "100″ (2,520 mm)", "119″ (3,020 mm)", "119″ (3,020 mm)"]),
        ("*Capacity, mild steel", "T", [1.5, 1.5, 1.0, 1.0, 1.0, 1.0]),
        ("Bending angle", "TXT", "0 – 135°"),
        ("Opening height", "TXT", "4″ (100 mm)"),
        ("Blade", "TXT", ["One-piece", "Segments 25 – 400 mm", "One-piece", "Segments 25 – 400 mm", "One-piece", "Segments 25 – 400 mm"]),
        ("*Motors", "TXT", "1/2 HP (0.37 kW) clamping, 1 HP (0.75 kW) folding"),
        ("Packing size L × W × H", "PK", [(283, 76, 142), (283, 76, 142), (333, 76, 141), (333, 76, 141), (383, 76, 145), (383, 76, 145)]),
        ("*Weight", "KG", [925, 965, 1260, 1310, 1560, 1630]),
    ]),
]
CAT["tt-pbb"] = ["PBB: fully welded, compact, low maintenance; simple and safe; foot-operated clamping leaves both hands free; gas spring in the arm optional; A: segmented clamping and folding blades; 3SH: quick-release clamp beam segments, counterbalanced folding beam with angle stop, optional back gauge on pre-drilled points",
                 "TSB/TSBS: welded steel; rigid; TSBS segments 25, 30, 35, 40, 45, 50, 75, 100, 150, 200, 200, 270, 400, 400 mm; lever swings the bending beam; TSB one-piece blade; TSB 2060/2 cast-iron frame with counterweight; TFS 2020B welded, foot control",
                 "MFS 2020: segments 25 – 500 mm; foot control; MF 3020: one-piece blade, foot control", "EFMS: segments 25 – 400 mm; EFM one-piece blade; foot pedal operation"]

# PDF p74 – p75 (143 – 145) — hydraulic folding machines.  The WC67Y / WA67Y torsion-bar press brakes on p75 right are NOT
# listed: they are the NovoTech value-line NC press brakes (vl-nc-small / vl-nc-large on novotech-cnc-press-brakes.html).
TAB["tt-hw"] = [
    table("HW1220×3.5 – HW3050×3.5", "Hydraulic folding machines, 10 ga × 4 – 10 ft, manual back gauge", ["HW1220×3.5", "HW1830×3.5", "HW2440×3.5", "HW3050×3.5"], [
        ("*Bending length", "TXT", ["48″ (1,220 mm)", "72″ (1,830 mm)", "96″ (2,440 mm)", "120″ (3,050 mm)"]),
        ("*Capacity", "TXT", "10 ga (3.5 mm) mild steel, 12 ga (2.5 mm) stainless"),
        ("Bending angle", "TXT", "0 – 135°"),
        ("*Box depth, max", "TXT", "5.9″ (150 mm)"),
        ("Beam opening", "TXT", "3″ (75 mm); beam adjustment 0 – 1″ (0 – 25 mm) front and back"),
        ("Back gauge", "TXT", "26″ (660 mm), manual"),
        ("Hydraulics", "TXT", ["Up to 2,176 psi (15 MPa); 2 – 3.3 in/s (50 – 85 mm/s)", "Up to 2,176 psi (15 MPa); 2 – 3.3 in/s (50 – 85 mm/s)", "Up to 2,176 psi (15 MPa); 2 – 3.3 in/s (50 – 85 mm/s)", "Up to 2,176 psi (15 MPa); 2 – 3 in/s (50 – 75 mm/s)"]),
        ("Control panel", "TXT", "Type A on a movable pedestal or type B fixed; foot pedals"),
        ("*Motor", "KW", [3.7, 3.7, 5.5, 7.5]),
        ("Packing size L × W × H", "PK", [(205, 102, 170), (265, 102, 170), (325, 102, 170), (390, 102, 170)]),
        ("*Weight", "KG", [1780, 2170, 2850, 3400]),
    ]),
    table("HW2040×4.5E · HW2540×4.5E · HW3050×3.5E", "Hydraulic folding machines with touch screen and servo back gauge, to 3/16″ × 10 ft", ["HW2040×4.5E", "HW2540×4.5E", "HW3050×3.5E"], [
        ("*Bending length", "TXT", ["80″ (2,040 mm)", "100″ (2,540 mm)", "120″ (3,050 mm)"]),
        ("*Capacity", "TXT", ["3/16″ (4.5 mm) structural steel, 1/8″ (3 mm) stainless", "3/16″ (4.5 mm) structural steel, 1/8″ (3 mm) stainless", "10 ga (3.5 mm) structural steel, 14 ga (2 mm) stainless"]),
        ("Bending angle", "TXT", "0 – 135°"),
        ("*Box depth, max", "TXT", "5.9″ (150 mm)"),
        ("Opening height / lower beam adjustment", "TXT", "3.5″ (90 mm) / 1″ (25 mm)"),
        ("*Back gauge", "TXT", ["21.7″ (550 mm), servo with ball screw", "31.9″ (810 mm), servo with ball screw", "49.2″ (1,250 mm), servo with ball screw"]),
        ("Optional segment set", "TXT", ["3″ × 7, 4″ × 3, 5″ × 7, 6″ × 2", "3″ × 6, 4″ × 5, 5″ × 10, 6″ × 2", "3″ × 6, 4″ × 4, 5″ × 10, 6″ × 6"]),
        ("Table height", "L", [910, 910, 910]),
        ("*Motor", "TXT", "10 HP (7.5 kW); max. 2,321 psi (16 MPa)"),
        ("Packing size L × W × H", "PK", [(305, 188, 200), (358, 188, 200), (412, 215, 200)]),
        ("*Weight", "KG", [3350, 4250, 4600]),
    ]),
]
CAT["tt-hw"] = ["HW…×3.5: rigid welded steel frame for 3.5 mm; hand wheels set the gap between upper and lower tools; bending angle setting device 0 – 135°; foot pedal; segments for boxes; back gauge; full protective covers; hand wheel sets the upper beam position",
                "HW…E: welded steel-plate frame, stress-relieved by tempering; hydraulic cylinders drive the clamping beam, pressure set to the thickness; the bending beam swings on two hydraulic cylinders and levers; servo back gauge with ball screw; touch screen shows angle and gauge, easy programs; light curtain at the front; European design"]

# ------------------------------------------------------------------------------------------------ ironworkers, small press brakes, stands
# PDF p76 (147 – 148)
TAB["tt-hbv"] = [
    table("HBV24 · HBV48", "Hydraulic bending brakes with four-way V-block, 3/16″ × 24 – 48″", ["HBV24", "HBV48"], [
        ("*Force", "TXT", ["16.5 US tons (15 t)", "33 US tons (30 t)"]),
        ("*Bending width × thickness", "TXT", ["24″ (610 mm) × 5/32″ (4 mm)", "48″ (1,220 mm) × 5/32″ (4 mm)"]),
        ("Stroke", "L", [150, 150]),
        ("Back gauge", "TXT", "4.1 – 21.7″ (105 – 550 mm)"),
        ("Control", "TXT", "Hydraulic foot valve"),
        ("*Motor", "KW", [1.5, 3.0]),
        ("Packing size L × W × H", "PK", [(152, 92, 143), (220, 93, 146)]),
        ("*Weight", "KG", [350, 510]),
    ]),
]
CAT["tt-hbv"] = ["hydraulic brakes that bend 4 mm plate and more; 24″ and 48″; the beam unpins for closed bends and easy part removal; hydraulic foot valve for precise control; simple set-up; four-way V-block (openings about 38, 51 and 86 mm); hydraulic pull-up press beam; back gauge 105 – 550 mm"]

TAB["tt-m55"] = [
    table("M50 · M55 · M60", "Compact single-cylinder ironworkers, 50 – 60 US tons", ["M50", "M55", "M60"], [
        ("*Punching", "TXT", ["1″ hole in 5/8″ plate", "1-1/16″ hole in 5/8″ plate", "1-1/16″ hole in 5/8″ plate"]),
        ("*Flat bar shear", "TXT", ["10 × 1/2″; 4 × 3/4″", "12 × 5/8″ or 14 × 3/8″; 4 × 3/4″", "12 × 5/8″ or 14 × 3/8″; 4 × 3/4″"]),
        ("*Angle shear", "TXT", ["4 × 4 × 1/4″ or 3 × 3 × 3/8″", "4 × 4 × 1/4″ or 3 × 3 × 3/8″", "4 × 4 × 3/8″ or 3 × 3 × 1/2″"]),
        ("*Rated force", "TXT", ["50 tons", "55 tons", "60 tons"]),
        ("Throat depth", "TXT", "7-1/2″"),
        ("Open / shut height", "TXT", "8″ / 6-3/4″"),
        ("Stroke", "TXT", "1-1/4″"),
        ("*Motor", "TXT", ["5.5 HP (4 kW)", "6 HP (4.5 kW)", "7 HP (5 kW)"]),
        ("Packing size L × W × H", "PK", [(108, 113, 151), (115, 113, 152), (123, 113, 152)]),
        ("*Weight", "KG", [670, 825, 1056]),
    ]),
]
CAT["tt-m55"] = ["punch, shear, notch and brake mild steel plate, bar and angle; many accessories for rod, square bar, sheet and pipe",
                 "standard tooling: punch and die 15/16″ (Ø22 mm), flat bar shear, angle shear",
                 "optional tooling: punch and die sets 1-1/16, 13/16, 11/16, 9/16, 7/16, 5/16, 3/16″ (Ø25, 20, 18, 14, 10, 8, 5 mm); right-angle notcher; shaped punches; brake die; slot die; pipe notcher 3/4, 1, 1-1/4, 1-1/2, 2″; round pipe shear die; bar shear die (angle 2 × 2″, square 3/4″, round Ø1/4 – 3/4″, flat 6 × 5/16″); gauging table kit and fabricator's guard"]

# PDF p77 (149 – 150)
TAB["tt-stand"] = [
    table("Roller stands and conveyors", "Material supports for saws, shears and brakes", ["RV1100", "RB1100", "RB1000", "RS018", "RB365", "RB2000", "RA785"], [
        ("*Type", "TXT", ["V-roller stand", "Roller stand", "Tripod roller stand", "Adjustable stand (for the SS-18)", "Roller conveyor, 41″ (1,040 mm) — 2,000 / 3,000 mm extensions", "Roller conveyor", "Roller table with measuring feed system, 79″ (2,000 mm)"]),
        ("*Height", "TXT", ["24.4 – 43.3″ (620 – 1,100 mm)", "24.4 – 43.3″ (620 – 1,100 mm)", "23 – 38.6″ (585 – 980 mm)", "25.6 – 35.4″ (650 – 900 mm)", "23.6 – 39.4″ (600 – 1,000 mm)", "23 – 38.6″ (585 – 980 mm)", "31.5 – 39.4″ (800 – 1,000 mm)"]),
        ("Roller width", "TXT", ["8.9″ (225 mm)", "13.8″ (350 mm)", "—", "—", "14.4″ (365 mm)", "—", "18.1″ (460 mm), rollers Ø2″ (50 mm) at 11″ (280 mm)"]),
        ("*Load, max", "TXT", ["728 lb (330 kg)", "661 lb (300 kg)", "331 lb (150 kg)", "—", "1,323 lb (600 kg)", "1,543 lb (700 kg)", "336 lb/ft (500 kg/m)"]),
        ("Feed system", "TXT", ["—", "—", "—", "—", "—", "—", "40 – 140 ipm, accuracy ±0.012″ (0.3 mm)"]),
        ("*Weight", "KG", [16, 16, 8, 11, 34.5, 52, 145]),
    ]),
]

# ------------------------------------------------------------------------------------------------ slip rolls
# PDF p78 – p80 (151 – 156)
TAB["tt-slip"] = [
    table("SJ · W01-0.8 · W01-1.5 · KW01", "Manual slip rolls, 22 – 16 ga × 12 – 51″", ["SJ300", "SJ320", "W01-0.8×305", "W01-0.8×610", "W01-0.8×915", "W01-0.8×1000", "KW01-0.8×1250", "W01-0.8×1300", "W01-1.5×915", "W01-1.5×1300", "W01-1.5×1300 HD"], [
        ("*Working width", "L", [300, 320, 305, 610, 915, 1000, 1250, 1300, 915, 1300, 1300]),
        ("*Capacity, mild steel", "T", [1.0, 1.0, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1.5, 1.5, 1.5]),
        ("*Roll diameter", "D", [32, 32, 25.4, 38, 50, 50, 70, 50, 50, 75, 75]),
        ("Mounting", "TXT", ["Bench (vise optional)", "Bench", "Bench (stand A optional)", "Bench", "Bench", "Bench", "Floor stand", "Bench", "Bench", "Bench, light type", "Bench, heavy duty"]),
        ("Packing size L × W × H", "PK", [(48, 22, 18), (48, 22, 18), (54, 24, 28), (95, 26, 37), (134, 32, 50), (145, 32, 50), (155, 59, 128), (170, 45, 50), (134, 35, 50), (170, 43, 56), (175, 45, 60)]),
        ("*Weight", "KG", [13, 12, 13, 38, 80, 86, 135, 117, 100, 195, 235]),
    ]),
    table("W01-2 · W01-0.8×2050", "Floor slip rolls on stand, 14 ga × 24 – 49″ and 22 ga × 81″", ["W01-2×610", "W01-2×1000", "W01-2×1250", "W01-0.8×2050"], [
        ("*Working width", "L", [610, 1000, 1250, 2050]),
        ("*Capacity, mild steel", "T", [2.0, 2.0, 2.0, 0.8]),
        ("*Roll diameter", "D", [60, 60, 60, 60]),
        ("Drive", "TXT", "Hand crank"),
        ("Packing size L × W × H", "PK", [(110, 50, 69), (155, 51, 69), (180, 50, 69), (255, 50, 70)]),
        ("*Weight", "KG", [165, 200, 229, 290]),
    ]),
    table("ESR electric slip rolls", "Motorized 3-roll slip rolls with foot pedal, 22 ga – 1/4″ × 3.3 – 10 ft", ["ESR-1020×2", "ESR-1300×1.5", "ESR-1300×1.5E", "ESR-1300×2.5", "ESR-1300×4.5", "ESR-1300×6.5", "ESR-1550×3.5", "ESR-1550×4.5", "ESR-2020×3.5", "ESR-2070×2.5", "ESR-2070×3.5", "ESR-2500×0.8", "ESR2550×2.5E", "ESR2550×3.5E", "ESR3050×2.5E", "ESR3050×3.5E"], [
        ("*Working width", "L", [1020, 1300, 1300, 1300, 1300, 1300, 1550, 1550, 2020, 2070, 2070, 2500, 2510, 2510, 3010, 3010]),
        ("*Capacity, mild steel", "T", [2.0, 1.5, 1.5, 2.5, 4.5, 6.5, 3.5, 4.5, 3.5, 2.5, 3.5, 0.8, 2.5, 3.5, 2.5, 3.5]),
        ("*Roll diameter", "D", [60, 75, 60, 90, 120, 150, 120, 150, 127, 120, 127, 90, 140, 150, 160, 170]),
        ("Min. rolling diameter", "D", ["—", "—", "—", 100, 130, 170, 130, 230, 140, 130, 140, 100, 160, 170, 180, 190]),
        ("Roll speed at 60 Hz", "TXT", ["—", "—", "—", "10.8 rpm", "11.2 rpm", "7.8 rpm", "11.2 rpm", "7.8 rpm", "7.8 rpm", "7.8 rpm", "7.8 rpm", "10.8 rpm", "7.8 rpm", "7.8 rpm", "7.8 rpm", "7.8 rpm"]),
        ("*Motor", "TXT", ["1.5 HP (1.1 kW) 1-phase or 1 HP (0.75 kW) 3-phase"] * 3 + ["2 HP (1.5 kW)", "3 HP (2.2 kW)", "4 HP (3 kW)", "3 HP (2.2 kW)", "4 HP (3 kW)", "4 HP (3 kW)", "3 HP (2.2 kW)", "4 HP (3 kW)", "3 HP (2.2 kW)", "4 HP (3 kW)", "4 HP (3 kW)", "5.5 HP (4 kW)", "7.5 HP (5.5 kW)"]),
        ("Back roll", "TXT", ["Manual"] * 12 + ["Motorized lift, digital position readout"] * 4),
        ("Packing size L × W × H", "PK", [(174, 60, 126), (179, 59, 110), (190, 55, 108), (200, 70, 120), (200, 76, 127), (208, 80, 134), (222, 76, 127), (230, 77, 145), (270, 87, 130), (282, 87, 130), (282, 87, 130), (310, 74, 120), (342, 83, 132), (342, 83, 132), (384, 82, 142), (391, 91, 136)]),
        ("*Weight", "KG", [260, 300, 275, 545, 750, 900, 840, 1005, 1095, 1060, 1110, 780, 1508, 1529, 1696, 2182]),
    ]),
    table("HER hydraulic slip rolls", "3-roll slip rolls with hydraulic drive on all rolls, 12 ga – 1/2″ × 4 – 10 ft", ["HER-1300×6.5", "HER-1550×4.5", "HER-1550×6.5", "HER-2070×4.5", "HER-2070×6.5", "HER-2000×12", "HER-2500×8", "HER-2500×6.5", "HER-2550×2.5", "HER-2550×3.5", "HER-3050×2.5", "HER-3050×3.5"], [
        ("*Working width", "TXT", ["4′3″ (1,300 mm)", "5′1″ (1,550 mm)", "5′1″ (1,550 mm)", "6′8″ (2,070 mm)", "6′8″ (2,070 mm)", "6′7″ (2,000 mm)", "8′2″ (2,500 mm)", "8′2″ (2,500 mm)", "8′3″ (2,510 mm)", "8′3″ (2,510 mm)", "9′11″ (3,010 mm)", "9′11″ (3,010 mm)"]),
        ("*Capacity, mild steel", "T", [6.5, 4.5, 6.5, 4.5, 6.5, 12.0, 8.0, 6.5, 2.5, 3.5, 2.5, 3.5]),
        ("*Roll diameter", "D", [151, 151, 181, 181, 191, 240, 240, 200, 140, 150, 160, 170]),
        ("Min. rolling diameter", "D", [170, 170, 200, 200, 215, 420, 420, 220, 160, 170, 180, 190]),
        ("Roll speed at 60 Hz", "TXT", ["5 rpm"] * 5 + ["4 rpm", "4 rpm"] + ["5 rpm"] * 5),
        ("*Motor", "TXT", ["3 HP (2.2 kW)", "5.5 HP (4 kW)", "5.5 HP (4 kW)", "5.5 HP (4 kW)", "5.5 HP (4 kW)", "7.5 HP (5.5 kW)", "7.5 HP (5.5 kW)", "7.5 HP (5.5 kW)", "3 HP (2.2 kW)", "4 HP (3 kW)", "5.5 HP (4 kW)", "7.5 HP (5.5 kW)"]),
        ("Packing size L × W × H", "PK", [(241, 108, 144), (266, 108, 144), (267, 111, 147), (315, 109, 152), (319, 111, 148), (313, 116, 152), (355, 104, 147), (361, 111, 147), (361, 108, 154), (361, 108, 154), (411, 108, 154), (416, 111, 144)]),
        ("*Weight", "KG", [1870, 2490, 2570, 2870, 3110, 3480, 3325, 3460, 2250, 2290, 2580, 3130]),
    ]),
]
CAT["tt-slip"] = ["manual: hardened gears for long life; comfortable eccentric clamp system; precision-ground rolls of high-strength steel; top roll swings out; lower roll adjusted by lever and cam; quick-release top roll; KW01: fast rolling, light and easy to carry, on stand; optional stand type A",
                  "W01-2 / ESR-1020×2: iron frame; quick-release top roll; ESR-1020×2 motorized with foot pedal",
                  "ESR: asymmetric 3-roll with high-strength steel rolls; fixed top roll, adjustable lower and rear rolls; wire grooves standard; top roll swings out with cam lock; cone rolling feature; ESR-1300×1.5E European design; options: hand-wheel back roll adjustment, fast lower roll adjustment; ESR2550/3050 E: motorized back roll lift and digital back roll position readout",
                  "HER: all three rolls driven hydraulically; pinch roll cylinders synchronized; hydraulic pinch roll up / down with digital position counter; rolls of top-grade alloy steel hardened to HRC 55; rigid, smooth, long life; top roll swivels out to remove the finished part; removable forward / reverse foot pedal with guard; electrical cabinet"]

# ------------------------------------------------------------------------------------------------ profile benders (ring rollers)
# PDF p81 – p83 (157 – 162).  Capacity rows: the catalogue's largest section per profile with its minimum ring diameter (the
# catalogue's icons: first flat bar row = on edge (hard way), second = flat (easy way) — checked against the section moduli).
from ttmc_conv import frac as _frac, dec as _dec


def nom(mm, wall=False):
    """nominal inch size of a profile dimension: walls of 3 mm and less as decimals (0.098″), other sizes as fractions,
    snapped to the whole or half inch when within 2 % (50 mm -> 2″, 100 mm -> 4″)"""
    v = mm / 25.4
    if wall and mm <= 3:
        return f"{v:.3f}″"
    for step in (1, 2):
        n = round(v * step) / step
        if n and abs(n - v) / v <= 0.02:
            return _frac(n * 25.4, den=step)
    return _frac(mm, den=32 if v < 0.25 else None)


def P(*a):
    """profile size: P(50, 10, 600) -> '2 × 3/8″ (50 × 10 mm), min. Ø23.6″ (600 mm)'; P(30, 650) -> round bar Ø30"""
    *dims, dmin = a
    if len(dims) == 1:
        s = f"Ø{nom(dims[0])} ({dims[0]:g} mm)"
    else:
        last = len(dims) - 1
        s = " × ".join(nom(x, wall=(i == last and len(dims) == 3)).rstrip("″") for i, x in enumerate(dims)) + "″ (" + " × ".join(f"{x:g}" for x in dims) + " mm)"
    return f"{s}, min. Ø{_dec(dmin)} ({dmin:g} mm)"


PROFILE_ROWS = ["Flat bar on edge (hard way)", "Flat bar flat (easy way)", "Square bar", "T-bar, stem out", "T-bar, stem in", "Channel, flanges out", "Channel, flanges in",
                "Angle, leg out", "Angle, leg in", "Round bar", "Square tube", "Rectangular tube"]


def profile_rows(cols):
    """cols: per model a list of 12 P() cells in PROFILE_ROWS order (None -> —)"""
    return [(("*" if i in (0, 1, 9) else "") + lab, "TXT", [c[i] or "—" for c in cols]) for i, lab in enumerate(PROFILE_ROWS)]


C_RBM10 = [P(30, 10, 500), P(50, 10, 400), P(20, 20, 500), None, None, None, None, None, None, None, None, None]
C_RBM20 = [P(25, 6, 200), P(45, 10, 300), P(12, 12, 110), P(25, 25, 4, 200), P(25, 25, 4, 200), P(30, 15, 4, 250), P(30, 15, 4, 250), P(20, 20, 4, 150), P(20, 20, 4, 200),
           P(12, 120), P(20, 20, 1.5, 250), P(30, 10, 1.5, 300)]
C_RBM30 = [P(30, 10, 320), None, None, None, None, None, None, None, None, P(16, 400), P(30, 30, 1, 900), None]
C_RBM30HV = [None, P(50, 15, 350), None, P(50, 50, 5, 400), P(50, 50, 5, 400), P(50, 25, 5, 400), P(50, 25, 5, 300), P(40, 40, 5, 400), P(40, 40, 5, 400),
             P(30, 600), P(40, 40, 3, 1000), P(50, 30, 3, 1200)]
C_40 = [P(50, 10, 600), P(50, 20, 800), P(20, 20, 800), P(50, 50, 6, 600), P(50, 50, 6, 600), P(50, 37, 4.5, 600), P(50, 37, 4.5, 600), P(50, 50, 5, 500), P(50, 50, 5, 500),
        P(30, 650), P(50, 50, 2.5, 700), P(50, 25, 2.5, 800)]
C_50 = [P(60, 10, 500), P(100, 15, 920), P(25, 25, 650), P(60, 60, 7, 750), P(60, 60, 7, 750), P(65, 40, 5, 550), P(80, 45, 6, 650), P(60, 60, 5, 500), P(60, 60, 5, 700),
        P(35, 600), P(50, 50, 3, 550), P(70, 50, 3, 1200)]
C_65 = [P(80, 25, 600), P(120, 25, 600), P(35, 35, 550), P(80, 40, 7, 500), P(80, 40, 7, 400), P(100, 50, 6, 600), P(100, 50, 6, 600), P(70, 70, 6, 500), P(70, 70, 6, 600),
        P(40, 500), P(50, 50, 3, 600), P(60, 40, 3, 800)]

TAB["tt-rbm"] = [
    table("RBM10 · ERBM10HV · RBM20 · RBM30 · RBM30HV", "Ring rollers with Ø3/4 – 1-3/16″ shafts — manual and motorized", ["RBM10", "ERBM10HV", "RBM20", "RBM30", "RBM30HV"], [
        ("*Shaft diameter", "D", [30, 30, 20, 30, 30]),
        ("*Drive", "TXT", ["Hand crank", "1.5 HP (1.1 kW), 8 rpm, foot pedal", "1 HP (0.75 kW) 1-phase or 3/4 HP (0.55 kW) 3-phase, 12 rpm, two driven rolls", "1.5 HP (1.1 kW), 9 rpm, foot pedal", "1 HP (0.75 kW), 9 rpm, foot pedal"]),
        ("Working position", "TXT", ["Vertical", "Horizontal and vertical", "Vertical", "Vertical", "Horizontal and vertical"]),
        ("Top roll readout", "TXT", ["—", "—", "LED readout", "—", "—"]),
    ] + profile_rows([C_RBM10, C_RBM10, C_RBM20, C_RBM30, C_RBM30HV]) + [
        ("Round tube", "TXT", ["—", "—", "Ø3/4″ pipe, min. Ø15.7″ (400 mm); Ø1-3/16 × 0.06″ (30 × 1.5 mm), min. Ø15.7″ (400 mm)", "Ø1-3/16 × 0.04″ (30 × 1 mm), min. Ø31.5″ (800 mm)", "Ø1-3/8 – 2-3/8 × 0.08″ (35 – 60 × 2 mm), min. Ø39.4″ (1,000 mm), special rolls"]),
        ("Packing size L × W × H", "TXT", ["20 × 19 × 27″ (50 × 48 × 68 cm) + stand 23 × 14 × 34″ (59 × 35 × 86 cm)", "37 × 31 × 53″ (95 × 80 × 135 cm)", "39 × 19 × 54″ (98 × 47 × 138 cm) + base 28 × 18 × 31″ (70 × 45 × 80 cm)",
                                           "37 × 24 × 59″ (93 × 62 × 150 cm)", "46 × 30 × 50″ (116 × 75 × 127 cm)"]),
        ("*Weight", "KG", [158, 235, 120, 213, 224]),
    ]),
    table("RBM40HV · HRBM40HV · RBM50 · RBM50HV · HRBM50HV · HRBM65", "Profile benders with Ø1-9/16 – 2-9/16″ shafts — H models with hydraulic top roll", ["RBM40HV", "HRBM40HV", "RBM50", "RBM50HV", "HRBM50HV", "HRBM65"], [
        ("*Shaft diameter", "D", [40, 40, 50, 50, 50, 65]),
        ("*Motor", "TXT", ["2 HP (1.5 kW), 9.3 rpm", "2 HP (1.5 kW), 9.3 rpm", "3 HP (2.2 kW), 9 rpm", "3 HP (2.2 kW), 9 rpm", "3 HP (2.2 kW), 9 rpm", "3 HP (2.2 kW), 9.3 rpm, hydraulic drive"]),
        ("Top roll", "TXT", ["Manual", "Hydraulic", "Manual", "Manual", "Hydraulic", "Hydraulic"]),
        ("Working position", "TXT", ["Horizontal and vertical", "Horizontal and vertical", "Vertical", "Horizontal and vertical", "Horizontal and vertical", "Horizontal and vertical"]),
    ] + profile_rows([C_40, C_40, C_50, C_50, C_50, C_65]) + [
        ("Round tube (special rolls)", "TXT", ["Ø1-3/16 – 2-3/4 × 0.08″ (30 – 70 × 2 mm), min. Ø27.6″ (700 mm)", "Ø1-3/16 – 2-3/4 × 0.08″ (30 – 70 × 2 mm), min. Ø27.6″ (700 mm)",
                                               "Ø1-3/16 – 2-3/4 × 0.08″ (30 – 70 × 2 mm), min. Ø23.6″ (600 mm)", "Ø1-3/16 – 2-3/4 × 0.08″ (30 – 70 × 2 mm), min. Ø23.6″ (600 mm)",
                                               "Ø1-3/16 – 2-3/4 × 0.08″ (30 – 70 × 2 mm), min. Ø23.6″ (600 mm)", "Ø3-15/16 × 0.08″ (100 × 2 mm), min. Ø39.4″ (1,000 mm)"]),
        ("Packing size L × W × H", "PK", [(140, 95, 134), (134, 93, 185), (100, 82, 155), (100, 82, 153), (122, 82, 180), (122, 110, 188)]),
        ("*Weight", "KG", [425, 490, 450, 460, 515, 720]),
    ]),
    table("CRB-76", "Decorative ring roller for tube and flat bar — metal-craft rings and scrolls", ["CRB-76"], [
        ("*Round tube formers", "TXT", ["Ø5/8, 3/4, 7/8, 1, 1-1/4, 1-1/2, 2, 2-1/2, 3″ (Ø16, 19, 22, 25, 32, 38, 51, 63, 76 mm)"]),
        ("*Square tube formers", "TXT", ["5/8, 3/4, 7/8, 1, 1-3/16, 1-1/2, 1-9/16, 2″ (16, 19, 22, 25, 30, 38, 40, 50 mm)"]),
        ("*Wall thickness", "TXT", ["0.02 – 0.08″ (0.5 – 2 mm)"]),
        ("*Motor", "KW", [1.1]),
        ("Packing size L × W × H", "PK", [(56, 92, 120)]),
        ("*Weight", "KG", [300]),
    ]),
]
CAT["tt-rbm"] = ["RBM10: special cast frame; hardened shafts of special steel; hardened and ground rolls; gears machined from solid; optional rolls; stand included; hand crank",
                 "ERBM10HV / RBM30HV: horizontal and vertical operation; foot pedal standard; RBM30: vertical, foot pedal; combination roll set optional",
                 "RBM20: heavy steel frame; ground and heat-treated shafts; foot pedal; digital display for the top roll; gear driven; 1-phase or 3-phase; stand included; some profiles need optional tooling",
                 "RBM40HV/50HV, HRBM40HV/50HV: horizontal and vertical; H models hydraulic top roll; one standard combination roll set does all listed profiles; special rolls (also nylon) made to order",
                 "HRBM65: steel-welded frame; hydraulic motor; mobile control panel; hydraulic top roll; one combination roll set; horizontal and vertical",
                 "CRB-76: for metal craft — round or square tube and flat bar into arcs and rings of any size; rolls made to order"]

# ------------------------------------------------------------------------------------------------ HVAC and sheet-metal hand tools
# PDF p84 (163 – 164) — lock formers
TAB["tt-lock"] = [
    table("PF20G · PF16G · AX20G", "Lock formers and auxiliary roll former for HVAC duct", ["PF20G", "PF16G", "AX20G"], [
        ("*Capacity, mild steel", "TXT", ["26 – 20 ga", "25 – 16 ga", "26 – 20 ga"]),
        ("*Standard roll forms", "TXT", ["Pittsburgh lock, flange attachment, right angle", "Pittsburgh lock, flange attachment, right angle, double seam, drive cleat, Z shape",
                                         "Roll sets to order: drive cleat, Acme double seam, female and male button lock, 6-in-1 set (1/4, 3/8, 1/2 and 5/8″ right-angle flanges, 5/8″ standing seam, 5/8″ T-connect)"]),
        ("Optional roll forms", "TXT", ["Double seam, drive cleat", "—", "—"]),
        ("*Speed", "TXT", ["25 ft/min", "24 ft/min", "40 ft/min"]),
        ("*Motor", "TXT", ["1 HP (0.75 kW), 1-phase or 3-phase", "3 HP (2.2 kW), 1-phase or 3-phase", "4 HP (3 kW), 1-phase or 3-phase"]),
        ("Packing size L × W × H", "PK", [(105, 56, 135), (118, 65, 109), (157, 82, 120)]),
        ("*Weight", "KG", [160, 299, 260]),
    ]),
]
CAT["tt-lock"] = ["PF: Pittsburgh joints for HVAC duct; the flange attachment forms a flange for easier fitting of the Pittsburgh joint; uses about 1″ of material; adjustable auto-guides; all-steel forming head, hardened, ground shafts; case-hardened forming rolls with matched cut gears and needle bearings",
                  "AX20G: designed for ease of use; hinged table top and square drive shafts — a complete roll set changes in under five minutes; quick-change tooling without keys or tools; quick jam release; converts from button lock to Acme double seam and drive cleat instantly"]

# PDF p85 – p86 (165 – 168)
TAB["tt-hvac"] = [
    table("CHB · CB · SL-10 · LB-2", "HVAC duct hand tools: hand brakes, cleat benders, seam closer and letter bender", ["CHB-24", "CHB-30", "CB-24", "CB-30", "SL-10", "LB-2"], [
        ("*Job", "TXT", ["Hand brake for 1/4 – 1″ flanges, 24″ long", "Hand brake for 1/4 – 1″ flanges, 30″ long", "Drive cleat edges on duct, 24″", "Drive cleat edges on duct, 30″",
                         "Closes Pittsburgh seams, 3 stages (30°, 75°, 90°)", "Channel letter bender for sign makers — Z, S and W bends"]),
        ("*Capacity", "TXT", ["20 ga (1 mm)", "20 ga (1 mm)", "20 ga (1 mm)", "20 ga (1 mm)", "26 – 20 ga (0.5 – 1 mm); flange 0.28 – 0.35″ (7 – 9 mm)", "0.079″ (2 mm) aluminum"]),
        ("Working width / fence", "TXT", ["24″ (610 mm); fence 1/4 – 1″ (6.35 – 25.4 mm)", "30″ (760 mm); fence 1/4 – 1″ (6.35 – 25.4 mm)", "24″ (610 mm)", "30″ (760 mm); fence 0 – 1/2″ (0 – 12.7 mm)", "—", "—"]),
        ("Drive", "TXT", ["Hand levers, bench mount", "Hand levers, bench mount", "Hand levers, 3-position quick release", "Hand levers, 3-position quick release", "1,400 W motor, 120 V or 230 V, 13 – 23 ft/min (4 – 7 m/min)", "Foot pedal, depth stop"]),
        ("Packing size L × W × H", "PK", [(81, 38, 11), (98, 38, 18), (82, 27, 31), (96, 27, 30), "—", (120, 67, 40)]),
        ("*Weight", "KG", [30, 34, 26, 30, 6.6, 41]),
    ]),
]
CAT["tt-hvac"] = ["CHB: rugged tool for consistent bends quickly; two-way trunnion holds the bending apron steady; bench mounted; bends 1/4 – 7/8″ flanges 24″ long",
                  "CB: forms uniform drive-cleat edges on rectangular duct in seconds without set-up; upper handle forms the cleat, lower handle opens the tool; Torrington needle bearings; quick release with 3 handle positions",
                  "SL-10: closes Pittsburgh seams, saving labour; adjusts to the sheet thickness automatically; continuous; speed set by a wheel",
                  "LB-2: letter bender for aluminum channel letters up to 2 mm; foot pedal; depth stop"]

TAB["tt-bead"] = [
    table("RM-A · RM-B · RM08 · RM12 · RM18 · RM-8H · RM-27", "Rotary machines and bead rollers", ["RM-A", "RM-B", "RM08", "RM12", "RM18", "RM-8H", "RM-27"], [
        ("*Capacity", "TXT", ["20 ga (1 mm)", "20 ga (1 mm)", "22 ga (0.8 mm)", "18 ga (1.2 mm)", "18 ga (1.2 mm)", "18 ga (1.2 mm) mild steel, 20 ga stainless, 16 ga aluminum", "18 ga (1.2 mm) mild steel, 20 ga stainless, 16 ga aluminum"]),
        ("*Throat depth", "TXT", ["—", "4.5″ (114 mm)", "7″ (177 mm)", "12″ (305 mm)", "18″ (457 mm)", "8″ (panels up to 16″ wide)", "—"]),
        ("Dies", "TXT", ["Hardened rolls; head rotates 360°; edge finder", "Hardened rolls, tool-free adjustment, quick change", "Six sets: turning, burring, wiring, crimping, ogee bead", "—", "Fence attachment optional",
                         "3/8″ bead set and offset set; 22 mm shafts; gear drive", "Offset set standard; 1/4 and 3/8″ bead, tipping and flange sets optional"]),
        ("Mounting", "TXT", ["Bench clamp", "Bench clamp", "Bench (stand optional)", "Bench", "Bench (stand optional)", "Vise or stand", "Vise or stand"]),
        ("Packing size L × W × H", "PK", [(18, 28, 66), (15, 26, 71), (49, 46, 16), (38, 45, 16), (73, 28, 14), "—", "—"]),
        ("*Weight", "KG", [9, 9, 22, 19, 24, "—", "—"]),
    ]),
]
CAT["tt-bead"] = ["RM-A: hardened rolls; head rotates 360°; bench mounted with an edge finder", "RM-B: hardened rolls; tool-free fade adjustment; easy roll change",
                  "RM08: six sets of standard rolls for large and small turning, burring, wiring, crimping and ogee bead; optional stand", "RM18: optional stand and fence attachment",
                  "RM-8H: 8″ throat handles panels up to 16″ wide; 20 ga stainless, 18 ga mild steel, 16 ga aluminum; 22 mm shafts; gear drive for full forming power; 3/8″ bead die set and offset die set included",
                  "RM-27: one set of offset dies standard; same capacity; tool-less precise adjustment; vise or stand mount; for floor pans, firewalls, truck floors, inner fenders; optional 1/4″ and 3/8″ bead dies, tipping die, flange die set"]

TAB["tt-rtb"] = [
    table("RTB-8 · RTB-8A · RTB-8AS", "Hand rollers for forming round duct and pipe from sheet, 40 – 49″", ["RTB-8", "RTB-8A", "RTB-8AS"], [
        ("*Working length", "TXT", ["40″ (1,020 mm)", "49″ (1,250 mm)", "49″ (1,250 mm)"]),
        ("*Capacity, mild steel", "TXT", "22 ga (0.8 mm)"),
        ("Mounting", "TXT", ["Bench, portable", "Bench, portable", "On welded stand, roll height 33.5″ (850 mm)"]),
        ("Packing size L × W × H", "PK", [(136, 30, 40), (160, 30, 40), (150, 147, 38)]),
        ("*Weight", "KG", [59, 64, 93]),
    ]),
]
CAT["tt-rtb"] = ["hardened rolls; up to 1,250 mm working length; portable and compact; AS on a welded stand at an ideal working height"]

# PDF p87 – p88 (169 – 172) — bead rollers and beading machines
TAB["tt-etb"] = [
    table("TB-12 · ETB-12 · ETB-25 · ETB-40", "Beading machines with 8 – 12″ throat, 18 ga to 8 ga", ["TB-12", "ETB-12", "ETB-25", "ETB-40"], [
        ("*Capacity, mild steel", "TXT", ["18 ga (1.2 mm)", "18 ga (1.2 mm)", "12 ga (2.5 mm)", "8 ga (4 mm)"]),
        ("*Throat depth", "TXT", ["8″ (200 mm)", "8″ (200 mm)", "11″ (280 mm)", "12″ (300 mm)"]),
        ("Shaft length", "TXT", ["5-1/2″ (140 mm)", "5-1/2″ (140 mm)", "4-3/4″ (120 mm)", "6-1/2″ (165 mm)"]),
        ("*Drive", "TXT", ["Hand crank", "1 HP (0.75 kW), 32 rpm, foot pedal", "2 HP (1.5 kW), 20 rpm, brake motor, foot pedal", "3 HP (2.2 kW), 15.3 rpm, brake motor, foot pedal"]),
        ("Rolls", "TXT", "4 standard sets; 8 extra profiles to order"),
        ("Packing size L × W × H", "PK", [(67, 32, 60), (110, 48, 148), (147, 58, 135), (165, 58, 140)]),
        ("*Weight", "KG", [46, 120, 235, 341]),
    ]),
    table("RM18E · LQ15", "Power beading machine for round duct · power slitting and bending machine", ["RM18E", "LQ15"], [
        ("*Capacity, mild steel", "TXT", ["15 ga (1.8 mm)", "16 ga (1.5 mm), slits sheet up to 47″ (1,200 mm) wide"]),
        ("*Throat depth", "TXT", ["9-3/8″ (238 mm)", "4 – 24″ (100 – 600 mm); duct Ø15 – 30-3/4″ (382 – 782 mm)"]),
        ("Rolls / speed", "TXT", ["3 standard sets (single and offset beads); 3 extra sets to order", "42 – 49 in/min (1,060 – 1,253 mm/min)"]),
        ("*Motor", "KW", [1.5, 1.5]),
        ("Packing size L × W × H", "PK", [(88, 52, 123), (137, 77, 142)]),
        ("*Weight", "KG", [138, 300]),
    ]),
    table("RM24 · RM36 · RM42 · RM-24H · RM-36H · RM-42H", "Deep-throat bead rollers, 24 – 42″, 20 ga — hand crank (M) or variable-speed motor; H models with a 4″ high throat", ["RM24M", "RM24", "RM-24H", "RM-24HM", "RM36M", "RM36", "RM-36H", "RM-36HM", "RM42", "RM-42H", "RM-42HM"], [
        ("*Capacity", "TXT", "20 ga (1 mm) mild steel, 18 ga (1.2 mm) aluminum"),
        ("*Throat depth", "TXT", ["24″ (610 mm)"] * 4 + ["36″ (910 mm)"] * 4 + ["42″ (1,067 mm)"] * 3),
        ("Throat height", "TXT", ["—", "—", "4″ (102 mm)", "4″ (102 mm)", "—", "—", "4″ (102 mm)", "4″ (102 mm)", "—", "4″ (102 mm)", "4″ (102 mm)"]),
        ("*Drive", "TXT", ["Hand crank", "Variable-speed motor, foot pedal, forward / reverse", "Variable-speed motor, foot pedal, both shafts driven", "Hand crank",
                           "Hand crank", "Variable-speed motor, foot pedal, forward / reverse", "Variable-speed motor, foot pedal, both shafts driven", "Hand crank",
                           "Variable-speed motor, foot pedal, forward / reverse", "Variable-speed motor, foot pedal, both shafts driven", "Hand crank"]),
        ("Packing size L × W × H", "PK", [(117, 64, 40), (117, 64, 40), (122, 61, 129), (166, 61, 150), (120, 70, 40), (151, 72, 40), (147, 61, 143), (166, 61, 150), (157, 57, 58), (166, 61, 150), (166, 61, 150)]),
        ("*Weight", "KG", [55, 60, 66, 61, 70, 80, 84, 79, 76, 93, 88]),
    ]),
]
CAT["tt-etb"] = ["TB/ETB-12: heavy, solid cast iron; special steel adjustable bottom spindle; self-braking motor with subframe (E); foot pedal (E); 4 standard roll sets S1 – S4, extra E1 – E8",
                 "ETB-25/40: welded steel frame; adjustable idle roll; steel shafts in bronze bushings; gear motor with brake; foot pedal; stand; 4 standard roll sets",
                 "RM18E: single and offset beads on round duct; 3 standard roll sets", "LQ15: multi-function slitting and bending — slits 1.5 mm sheet up to 1,200 mm wide; for duct forming",
                 "RM24/36/42 power drive: 1 mm mild steel, 1.2 mm aluminum; heavy fabricated plate-steel frame; adjustable bead depth; variable-speed foot control, hands free; Oilite bushings; forward / reverse; heat-treated gears; 1/2″ round bead roll standard; large selection of rolls: round bead 1/8 – 1″, flat bead 1/8 – 1″, step 1/16 – 1/4″, 45° step, spoiler 1-1/4″ radius",
                 "RM-H high throat: rigid frame; 4″ high throat for clearance; copper bushings; forward / reverse; adjustable bead depth; variable-speed foot pedal; both shafts driven; profiles round 1/2″, step 1/4″, flat 1/2″, spoiler 1-1/4″",
                 "bead roller B/F 3/8″: 1/8″ beads on tube ends to hold hoses; material up to 0.028″; tube from 3/8″ diameter"]

# ------------------------------------------------------------------------------------------------ tube and pipe benders, tube rollers
# PDF p89 – p97 (173 – 190)
TAB["tt-tb-manual"] = [
    table("TB-180 · RB-1 · RB-2 · MY-22", "Hand tube benders for small tube, 1/4 – 1″", ["TB-180", "RB-1", "RB-2", "MY-22"], [
        ("*Tube size", "TXT", ["3/8 – 1″ OD, 0.049 – 0.095″ wall", "1/2 – 1″ OD, 0.03 – 0.05″ (0.8 – 1.2 mm) wall", "1/4 – 5/8″ OD", "Round 3/8 – 7/8″ OD, square 3/4 and 1″; 0.03 – 0.05″ (0.8 – 1.2 mm) wall"]),
        ("*Bend angle, max", "TXT", ["180° in one pull", "270°", "180°", "180°"]),
        ("*Standard dies", "TXT", ["3/4″ OD, 2-1/2″ CLR (20 mm, CLR 60 mm)", "1/2, 9/16, 5/8, 3/4, 7/8, 1″", "1/4, 5/16, 3/8, 1/2, 5/8″ — 3D and 5D radius", "3/8, 1/2, 9/16, 5/8, 3/4, 7/8″ round; 3/4, 1″ square, in a carry case"]),
        ("Optional dies", "TXT", ["3/8 and 1/2″ (CLR 2″), 5/8″ (2-1/2″), 7/8 and 1″ (3-1/2″); 10 – 25 mm", "—", "—", "—"]),
        ("Mounting", "TXT", ["Bench vise", "Stand", "Stand", "Bench vise"]),
        ("Packing size L × W × H", "PK", ["—", (103, 43, 35), (110, 40, 40), (62, 35, 16)]),
        ("*Weight", "KG", ["—", 56, 51, 24]),
    ]),
    table("TB-500 · TB-3 · TB-3A · TB-3B · TB-3C · HTB-1000", "Ratchet and hydraulic tube and pipe benders, to 2-1/2″ tube", ["TB-500", "TB-3", "TB-3A", "TB-3B", "TB-3C", "HTB-1000"], [
        ("*Capacity", "TXT", ["Round tube 2-1/2 × 0.120″ mild steel and aluminum, 2 × 0.120″ stainless and chromoly; solid rod 1″; min. OD 3/4″",
                              "2″ schedule 40 pipe (0.154″ wall)", "2″ schedule 40 pipe (0.154″ wall)", "2″ schedule 40 pipe (0.154″ wall)", "2″ schedule 40 pipe (0.154″ wall)", "2″ schedule 40 pipe (0.154″ wall)"]),
        ("*Drive", "TXT", ["Hand lever (ratchet)", "Hand lever", "10-ton air / hydraulic jack", "10-ton air-hydraulic cylinder, 12″ stroke", "10-ton electric-hydraulic cylinder, 12″ stroke",
                           "Electric hydraulic pump: 1 HP (0.75 kW) 1-phase or 3/4 HP (0.55 kW) 3-phase — about 3× faster than air-hydraulic"]),
        ("Centre-line radius", "TXT", ["3 – 7″ (76 – 176 mm)", "3 – 6″", "3 – 6″", "3 – 6″", "3 – 6″", "3 – 6″"]),
        ("*Standard dies", "TXT", ["1″ × 3″ CLR", "1″ × 3″, 1-1/2″ × 5″, 1-3/4″ × 6″ (120°)", "1″ × 3″, 1-1/2″ × 5″, 1-3/4″ × 6″ (120°)", "1″ × 3″, 1-1/2″ × 5″, 1-3/4″ × 6″ (120°)",
                                    "1″ × 3″, 1-1/2″ × 5″, 1-3/4″ × 6″ (120°)", "1″ × 3″, 1-1/2″ × 5″, 1-3/4″ × 6″ (120°)"]),
        ("Optional dies", "TXT", ["3/4 – 2″ round, 3 – 7″ CLR (13 sizes); 90° or 180° dies", "Round 3/4 – 2″, square 3/4 – 1-1/2″; 120°, 180° and 240° dies", "Round 3/4 – 2″, square 3/4 – 1-1/2″; 120°, 180° and 240° dies",
                                  "Round 3/4 – 2″, square 3/4 – 1-1/2″; 120°, 180° and 240° dies", "Round 3/4 – 2″, square 3/4 – 1-1/2″; 120°, 180° and 240° dies", "Round 3/4 – 2″, square 3/4 – 1-1/2″; 120°, 180° and 240° dies"]),
        ("Stand", "TXT", ["Pedestal", "Pedestal (extension handle optional)", "Pedestal", "Caster stand with die rack", "Caster stand with die rack", "Caster stand with die rack"]),
        ("Packing size L × W × H", "PK", [(90, 90, 43), (98, 34, 36), "—", "—", "—", (125, 65, 106)]),
        ("*Weight", "KG", [130, 65, "—", "—", "—", 111]),
    ]),
    table("HTB-25T · TBM-60", "25-ton hydraulic tubing bender and electric rotary-draw (top) bender", ["HTB-25T", "TBM-60"], [
        ("*Capacity", "TXT", ["Round and square tube 3/4 – 2″ OD (19 – 50 mm), wall 0.065 – 0.125″ (1.6 – 3 mm); mild steel, stainless, aluminum", "Tube, pipe, square, rectangular and solid 1/4 – 2-1/2″ OD"]),
        ("*Drive", "TXT", ["25-ton hydraulic ram, air-hydraulic foot pump", "2 HP (1.5 kW), two speeds 1.7 / 3.4 rpm, foot pedal"]),
        ("Bend angle", "TXT", ["90°", "0 – 180°"]),
        ("*Dies", "TXT", ["1″ × 4″ CLR standard; round 3/4 – 2″ (CLR 4 – 8″, 13 sets), 25 – 45 mm, square 3/4 – 2″ (CLR 4 – 8″) optional", "1″ tube kit standard; dies to order; two-axis positioner optional"]),
        ("Packing size L × W × H", "PK", ["—", (100, 60, 132)]),
        ("*Weight", "KG", ["—", 215]),
    ]),
    table("HB-8 · HB-10 · HB-12 · HB-16 · EHB-10", "Hydraulic pipe benders for 1/2 – 3″ pipe", ["HB-8", "HB-10", "EHB-10", "HB-12", "HB-16"], [
        ("*Force", "TXT", ["8.8 US tons (8 t)", "11 US tons (10 t)", "11 US tons (10 t)", "13.2 US tons (12 t)", "17.6 US tons (16 t)"]),
        ("*Pipe dies", "TXT", ["3/4, 1, 1-1/2, 1-5/8, 1-3/4″", "1/2, 3/4, 1, 1-1/4, 1-1/2, 2″", "1/2, 3/4, 1, 1-1/4, 1-1/2, 2″", "1/2, 3/4, 1, 1-1/4, 1-1/2, 2″", "1/2, 3/4, 1, 1-1/4, 1-1/2, 2, 2-1/2, 3″"]),
        ("Ram stroke", "TXT", ["4.7 + 2.4″ (120 + 60 mm)", "6.1″ (155 mm)", "6.1″ (155 mm)", "9.4″ (240 mm)", "9.4″ (240 mm)"]),
        ("*Drive", "TXT", ["Hand pump", "Hand pump", "Electric pump: 1 HP (0.75 kW) 1-phase or 3/4 HP (0.55 kW) 3-phase", "Hand pump", "Hand pump"]),
        ("Packing size L × W × H", "PK", [(74, 36, 30), (71, 59, 22), (72, 59, 50), (63, 57, 18), (82, 62, 24)]),
        ("*Weight", "KG", [46, 42, 53, 40, 85]),
    ]),
    table("JTB-40 · JTB-50 · JTB-80", "Hydraulic PLC tube benders for round, stainless and square tube", ["JTB-40", "JTB-50", "JTB-80"], [
        ("*Round tube", "TXT", ["Ø5/8 – 1-9/16″ (16 – 40 mm), wall 0.04 – 0.12″ (1 – 3 mm)", "Ø5/8 – 2″ (16 – 51 mm), wall 0.04 – 0.2″ (1 – 5 mm)", "Ø1-9/16 – 3-1/8″ (40 – 80 mm), wall 0.04 – 0.35″ (1 – 9 mm)"]),
        ("*Stainless tube", "TXT", ["—", "Ø5/8 – 1-1/2″ (16 – 38 mm)", "Ø1-1/4 – 2″ (32.2 – 50.8 mm)"]),
        ("*Square tube", "TXT", ["—", "5/8 – 2″ (16 × 16 – 50 × 50 mm)", "1-9/16 – 3-1/8″ (40 × 40 – 80 × 80 mm)"]),
        ("Bend angle / speed", "TXT", ["—", "180°, 5 rpm", "180°, 2 rpm"]),
        ("Standard dies", "TXT", ["16, 20, 25, 32, 38 mm", "25, 32, 38, 48 mm", "76 mm × 265 mm CLR, 60 mm × 210 mm CLR"]),
        ("*Motor", "TXT", ["2 HP (1.5 kW)", "3 HP (2.2 kW) + 1.5 HP (1.1 kW) hydraulic", "7.5 HP (5.5 kW) + 2 HP (1.5 kW) hydraulic"]),
        ("Packing size L × W × H", "PK", [(78, 54, 77), (145, 69, 117), (150, 91, 155)]),
        ("*Weight", "KG", [220, 550, 1300]),
    ]),
    table("HTB-2000 · HTES-3000", "Exhaust and muffler shop: hydraulic tube bender with swager / expander, and tube expander-swager", ["HTB-2000", "HTES-3000"], [
        ("*Capacity", "TXT", ["Bends tube 1 – 3″ OD; expands to 3″", "Expands 1 – 3-1/2″, swages 1 – 3″; collets for 1 – 2-1/2″ OD"]),
        ("*Force / pressure", "TXT", ["58,000 lb bending force", "3,000 psi; cylinder Ø3.5″ (90 mm), stroke 6.5″ (165 mm)"]),
        ("*Motor", "TXT", ["4 HP (3 kW) 3-phase or 5.5 HP (4 kW) 1-phase", "5.5 HP (4 kW)"]),
        ("Equipment", "TXT", ["Tooling package (radius dies 3 – 5″ for 1-1/2 – 3″ tube, back shoes, collets, ball and swage dies, flare tool); knee-pad control; depth-of-bend indicator; safety guards; casters with brakes",
                              "Portable cart with swivel casters; adjustable collar; arbor tips, reducing dies, segments, ball and swage dies optional"]),
        ("Packing size L × W × H", "PK", [(180, 85, 134), (115, 50, 100)]),
        ("*Weight", "KG", [580, 286]),
    ]),
]
CAT["tt-tb-manual"] = ["TB-500: manual bender with large capacity; dies for 90° or 180°; 180° bends without re-pinning the die; quick-change hook sleeve inserts, no U-straps",
                       "TB-180: 180° in one pull; 3/8 – 1″ OD tube, 0.049 – 0.095″ wall; standard 3/4″ OD, CLR 2.5″; vise mounted; eccentric lock roll; angle indicator",
                       "HTB-25T: 25 tons of hydraulic power; portable, no anchoring; one 1″ × 4″ die set; air-hydraulic pump; mild steel, stainless, aluminum tube and pipe; engraved reference scale; optional floor stand",
                       "TB-3 family: 2″ schedule 40 pipe; A: 10-ton air/hydraulic jack; B: air-hydraulic, 10 t, 12″ stroke cylinder, caster stand with die rack; C: electric-hydraulic",
                       "HTB-1000: portable; 2″ schedule 40 pipe; dies 120°, 180°, 240°; aluminum-bronze bushings at pivots; about 3× faster than air-hydraulic units",
                       "TBM-60: two speeds; 1/4 – 2-1/2″ OD; one 1″ tube kit standard; pipe, tube, squares, rectangles, solids and profiles; remote foot pedal; transport wheels and handle; optional two-axis positioner",
                       "JTB-50/80: hydraulic drive, PLC control; low-carbon and stainless round tube, square tube, round bar; one-touch operation for single parts and programmed batch work; easy, low power; JTB-80 movable control pedal",
                       "HTB-2000: entry-level exhaust bender; bends to 3″, built-in swager / expander for end finishing; tooling package as listed",
                       "HTES-3000: 4 kW motor, 3,000 psi; Ø90 mm cylinder, 165 mm stroke; expands 1 – 3-1/2″, swages 1 – 3″; portable cart"]

TAB["tt-tr"] = [
    table("TR-40 · TR-50 · ETR-50 · TR-60", "Tube and pipe rollers — rings and arcs in tube, pipe, square tube and flat bar", ["TR-40", "TR-50", "ETR-50", "TR-60"], [
        ("*Capacity", "TXT", ["Square tube 1-9/16 × 0.06″ (40 × 40 × 1.5 mm) mild steel, min. Ø23.6″ (600 mm); 3/4″ (20 × 20 × 1.2 mm), min. Ø17.7″ (450 mm)",
                              "Round tube 1/2 – 2″, pipe 1/4 – 1-1/2″, square tube 1/2 – 1″ with optional rolls", "Round tube 1/2 – 2″, pipe 1/4 – 1-1/2″, square tube 1/2 – 1″ with optional rolls",
                              "Round tube 2″ (min. radius 60″), pipe 1-1/2″ (20″), square tube 2″ (70″), rectangular 1 × 2″ (60″), channel 1 × 2″ (60″), flat bar 1-1/4″ (10″)"]),
        ("*Standard rolls", "TXT", ["One set for square and rectangular tube", "1-1/2″ round tube", "1-1/2″ round tube", "1-1/2″ round tube"]),
        ("*Drive", "TXT", ["Hand crank", "Hand crank", "1/2 HP (0.37 kW) motor, foot pedal, 1- or 3-phase", "Hand crank; quick-change lower roll"]),
        ("Packing size L × W × H", "PK", [(55, 25, 40), "—", "—", (63, 37, 23)]),
        ("*Weight", "KG", [20, 44, 57, 34]),
    ]),
]
CAT["tt-tr"] = ["TR-40: square and rectangular tube with one standard roll set; mild steel 20×20×1.2 – 40×40×1.5, copper and aluminum slightly thicker",
                "TR-50/ETR-50: hardened steel top plate; enlarged outrigger base; bench top or adjustable stand; CNC-machined round and square dies; ETR electric for hands-free work; optional rolls",
                "TR-60: quick-change lower roll; many optional rolls: round tube 1/2 – 2″ (12), pipe 1/4 – 1-1/2″ (7), square tube 1/2 – 2″ (7), 1×2″ rectangular, 1-1/4″ flat, 1×2″ channel; metric rolls on request"]

# p90 – p93 (175 – 182) — benders for flat bar and rod, ornamental iron tools
TAB["tt-ub"] = [
    table("UB-70 · UB-100 · UB-100A · SBG-30 · SBG-40", "Universal benders for flat bar, round, square and angle", ["UB-70", "UB-100", "UB-100A", "SBG-30", "SBG-40"], [
        ("*Flat bar", "TXT", ["2-3/4 × 3/8″ (70 × 10 mm) warm", "4 × 3/8″ (100 × 10 mm) warm", "4 × 1/4″ (100 × 7 mm) warm", "1-3/16 × 3/8″ (30 × 10 mm)", "1-3/16 × 5/16″ (30 × 8 mm)"]),
        ("*Round bar", "TXT", ["Ø3/4″ (20 mm) warm", "Ø3/4″ (20 mm) warm", "Ø7/8″ (22 mm) warm", "Ø3/8″ (10 mm)", "Ø5/8″ (15 mm)"]),
        ("Square bar", "TXT", ["11/16″ (18 mm) warm", "11/16″ (18 mm) warm", "3/4″ (20 mm) warm", "3/8″ (10 mm)", "1/2″ (13 mm)"]),
        ("Angle", "TXT", ["2-3/8 × 5/16″ (60 × 8 mm)", "2-3/8 × 5/16″ (60 × 8 mm)", "—", "—", "—"]),
        ("Bending", "TXT", ["Angles to 120°, radius bends", "Angles to 120°, radius bends", "Angles to 120°, radius bends", "Angles, rings, hoops and scrolls", "Angles, rings, hoops and scrolls"]),
        ("*Weight", "KG", [28, 29, 33, 27, 23]),
    ]),
    table("YP-9 · YP-38 · UBM-30 · PR-3 · PR-5", "Bench benders and ring rollers for flat bar and rod", ["YP-9", "YP-38", "UBM-30", "PR-3", "PR-5"], [
        ("*Capacity", "TXT", ["Flat 1-1/4 × 5/16″ (32 × 8 mm) or 2 × 1/4″ (50 × 6 mm)", "Flat 1-1/4 × 5/16″ (32 × 8 mm) or 2 × 1/4″ (50 × 6 mm)", "Flat 2 × 5/16″ (50 × 8 mm) or 2 × 1/4″ (50 × 6 mm)",
                              "Round 1/4″ (6.5 mm); flat 1 × 5/32″ (25 × 4 mm); rolls Ø1-1/4″ (32 mm)", "Flat bar 1 × 1/4″ easy way; round 1/2″ with optional rolls; min. Ø2.75″"]),
        ("*Bend", "TXT", ["0 – 200°", "0 – 200°", "0 – 200°", "Rings — hand crank", "Rings — three driven rolls, hand crank, heavy stand"]),
        ("Packing size L × W × H", "PK", [(67, 26, 13), (88, 26, 26), (88, 26, 26), (36, 20, 21), (33, 22, 24)]),
        ("*Weight", "KG", [16, 19.5, 31, 6, 14]),
    ]),
    table("W-1 · W-2 · W-10 · Mini universal bender · SBG-20 · JTR-20 · JTR-30 · CRB-style tools", "Ornamental iron and metal-craft tools", ["W-1", "W-2", "W-10", "Mini universal bender", "SBG-20", "JTR-20", "JTR-30"], [
        ("*Job", "TXT", ["Scroll former, bender, twister, shear and punch set", "Heavier scroll former, bender, twister, shear and punch set", "Rod forming tool: 180°+ bends with 1/2 – 1-1/2″ ID",
                         "Clamps, brackets, hooks, coils from wire, flat bar and tube", "Angle bending of steel strip", "Pressing (embossing) of steel strip", "Rings from flat bar, round and square tube"]),
        ("*Capacity", "TXT", ["Round or square 3/8″ in scroll former and bender; flat 1 × 3/16″; punch 3/16″ flat; shear 1.18 × 0.2″ flat, 0.236″ round or square", "—",
                              "Rod to 3/8″; flat to 1/2 × 3/16″", "Wire and rod to 1/2″", "Strip 13/16 × 0.06″ (20 × 1.5 mm)", "Strip 13/16 × 0.06″ (20 × 1.5 mm)", "Flat 1-9/16 × 3/8″ (40 × 10 mm); round tube Ø1-3/16 × 0.04″ (30 × 1 mm); square tube 1-9/16″ × 0.04″ (40 × 40 × 1 mm)"]),
        ("Packing size L × W × H", "PK", [(107, 31, 32), (107, 41, 26), "—", (32, 10, 10), (61, 20, 11), (39, 18, 20), (95, 58, 120)]),
        ("*Weight", "KG", [12, 32, "—", 2.8, 7, 12, 65]),
    ]),
    table("PBS-3", "Shear, brake and punch hanger board for on-site sheet metal work", ["PBS-3"], [
        ("*Capacity", "TXT", ["Shears and bends 16 ga (1.5 mm), punches holes to 9/32″ (7 mm)"]),
        ("Bend angle", "TXT", ["90°"]),
        ("Packing size L × W × H", "PK", [(105, 12, 19)]),
        ("*Weight", "KG", [16]),
    ]),
]
CAT["tt-ub"] = ["UB: easy, precise; wide support face for safe work; bending angles and radii by changing and turning the tools; up to 120°; capacities given for warm bending",
                "SBG-30/40: angle, roll, hoop and coil bending; grilles, gates, railings, patio furniture, wrought-iron lamps; steel, brass, copper, aluminum",
                "W-1: ornate metal work — plant hangers, candelabras, wire racks, fencing from mild steel strip; scroll former, bender, twister; 3/8″ round or square bar, 1 × 3/16″ flat strip; one tool shears and punches; 1/4″ base with four 3/8″ holes",
                "W-10: industrial rod forming tool for repeatable 180°+ bends in mild steel, stainless and aluminum rod up to 3/8″ and flat stock 1/2 × 3/16″; mounts in a vise; dies 1/2 – 1-1/2″",
                "PR-5: three driven rolls; bends on either side of the bottom roll for more radius options; compact and portable; flat bar tooling included; small circles; heavy stand; round tooling optional",
                "PBS-3: hanger board — bends, punches and cuts for on-site sheet metal installation"]

# ------------------------------------------------------------------------------------------------ metal shaping (auto body, custom fab)
# PDF p98 – p101 (191 – 198)
TAB["tt-ss"] = [
    table("SS-16 · SS-18 · SG-18 · SM-16B · SS-12P", "Shrinker-stretchers, bench and hand", ["SS-18", "SG-18", "SS-16", "SM-16B", "SS-12P"], [
        ("*Capacity", "TXT", ["18 ga (1.2 mm) mild steel", "16 ga (1.5 mm) mild steel", "16 ga (1.5 mm) mild steel", "16 ga (1.5 mm) mild steel", "18 ga (1.2 mm) mild steel, 16 ga (1.5 mm) aluminum"]),
        ("*Throat depth", "TXT", ["1″ (25.4 mm)", "2-3/4″ (70 mm)", "8″ (208 mm)", "—", "—"]),
        ("Jaws", "TXT", ["One body + shrinker and stretcher jaws (two units in the photo)", "Shrinker and stretcher jaws", "Shrinker and stretcher jaws", "Two jaws, industrial type", "Pliers type, quick-change tools"]),
        ("Packing size L × W × H", "PK", [(46, 22, 13), (46, 20, 13), (35, 17, 40), (80, 59, 132), "—"]),
        ("*Weight", "KG", [5.5, 5.4, 24, 20, "—"]),
    ]),
    table("SS-18FD · SS-16F · SG-18F · FSM-16", "Foot-operated shrinker-stretchers on stand", ["SS-18FD", "SS-16F", "SG-18F", "FSM-16"], [
        ("*Capacity", "TXT", ["18 ga (1.2 mm) mild steel", "16 ga (1.5 mm) mild steel", "18 ga (1.2 mm) mild steel", "16 ga (1.5 mm) mild steel"]),
        ("*Throat depth", "TXT", ["1″ (25.4 mm)", "8″ (208 mm)", "8″ (208 mm)", "6″ (152 mm)"]),
        ("Operation", "TXT", ["Foot pedal, two heads (shrink and stretch)", "Foot pedal", "Foot pedal", "Foot pedal; wheeled base; aluminum jaws optional"]),
        ("Packing size L × W × H", "PK", [(115, 46, 19), [("body", (36, 17, 42)), ("stand", (90, 65, 28))], "—", (118, 51, 23)]),
        ("*Weight", "KG", [29, 29, 35, 38]),
    ]),
]
CAT["tt-ss"] = ["shrinker contracts sheet for inside curves, stretcher expands it for outside curves; chamfered plate with inside and outside radius into an S-form; standard one body + two jaws",
                "pedal operation makes shrinking and stretching more effective and less labour-intensive; hands-free for better control and faster results",
                "SS-12P: light and handy, aluminum handles; wide jaw opening; quick tool change through screw locks; 1.2 mm mild steel, 1.5 mm aluminum",
                "SM-16B: two jaws; industrial; 1.5 mm; optional RS018 universal tool stand"]

TAB["tt-ph"] = [
    table("PPH-12 · PPH-24 · PPH500 · PPH-610 · UFP-2", "Pneumatic planishing hammers", ["PPH-12", "PPH-24", "PPH500", "PPH-610", "UFP-2"], [
        ("*Capacity, mild steel", "TXT", ["18 ga (1.2 mm)", "18 ga (1.2 mm)", "—", "16 ga (1.5 mm)", "22 ga (0.75 mm) with the English wheel head"]),
        ("*Throat depth", "TXT", ["12″ (305 mm)", "24″ (610 mm)", "19-5/8″ (500 mm)", "24″ (610 mm)", "20″ (500 mm)"]),
        ("Anvils", "TXT", ["9 radius anvils (3/4″ – 12″ rad. and flat) with holder", "9 radius anvils (3/4″ – 12″ rad. and flat) with holder", "1, 2 and 3″ radius; anvil-to-hammer opening 4″", "One upper and anvil die set", "1, 2, 3″ radius planishing hammer + English wheel"]),
        ("Air", "TXT", ["Foot pedal", "Foot pedal", "50 – 100 psi; 875 – 1,350 bpm", "90 – 120 psi; 3-position air flow", "Foot pedal"]),
        ("Packing size L × W × H", "PK", ["—", "—", (75, 65, 24), (173, 94, 40), (88, 44, 68)]),
        ("*Weight", "KG", [12, 15, 23, 79, 74]),
    ]),
    table("PH-20D · PH-30D · BEP", "Electric power hammers and bullseye picks", ["PH-20D", "PH-30D", "BEP-15", "BEP-20", "BEP-25", "BEP-30"], [
        ("*Capacity", "TXT", ["16 ga (1.5 mm) mild steel, 12 ga (2.5 mm) aluminum", "16 ga (1.5 mm) mild steel, 12 ga (2.5 mm) aluminum", "Dent repair on panels", "Dent repair on panels", "Dent repair on panels", "Dent repair on panels"]),
        ("*Throat depth", "TXT", ["20″ (508 mm)", "30″ (760 mm)", "15″ (380 mm)", "20″ (508 mm)", "25″ (635 mm)", "30″ (762 mm)"]),
        ("Opening height", "TXT", ["5″ (127 mm)", "6″ (152 mm)", "—", "—", "—", "—"]),
        ("*Drive", "TXT", ["2 HP (1.5 kW), variable 0 – 1,700 blows/min, foot switch, casters", "2 HP (1.5 kW), variable 0 – 1,400 blows/min, foot switch", "Spring-loaded handle; 2 and 4 mm tips (8 mm and blunt optional)",
                           "Spring-loaded handle; 2 and 4 mm tips", "Spring-loaded handle; 2 and 4 mm tips", "Spring-loaded handle; 2 and 4 mm tips"]),
        ("Packing size L × W × H", "PK", [(95, 85, 60), (118, 93, 165), "—", "—", "—", "—"]),
        ("*Weight", "KG", [170, 190, 1.3, 1.5, 1.6, 2.0]),
    ]),
]
CAT["tt-ph"] = ["PPH-12/24: 9 radius steel anvils and an anvil holder; foot pedal, hands free; anvils 3/4, 1-1/2, 2, 3, 4, 6, 8, 12″ radius and flat; stretcher die optional; floor stand optional",
                "PPH500: anvils 1, 2, 3″ radius; 875 – 1,350 rpm; 4″ opening; 50 – 100 psi", "PPH-610: smooth beads and forms mild steel up to 16 ga; quick change of upper dies; one die set; 3-position air flow regulates speed; 90 – 120 psi",
                "PH-20D/30D: steel-welded frame; variable speed; foot switch; casters on PH-20D", "BEP: straighten metal accurately; angle-picking around braces and gussets; panels, roof panels, hoods; faster than conventional methods; spring-loaded handle for repetitive light blows"]

TAB["tt-ew"] = [
    table("F0.8×450 · F1.2×560 · F1.2×560A · F1.2×710 · F1.5×700 · F1.2×1000", "English wheels, 18 – 40″ throat", ["F0.8×450", "F1.2×560", "F1.2×560A", "F1.2×710", "F1.5×700", "F1.2×1000"], [
        ("*Capacity, mild steel", "TXT", ["22 ga (0.8 mm)", "18 ga (1.2 mm)", "18 ga (1.2 mm)", "18 ga (1.2 mm)", "16 ga (1.5 mm) steel, 14 ga (2 mm) aluminum and copper", "18 ga (1.2 mm)"]),
        ("*Throat depth", "TXT", ["18″ (450 mm)", "22″ (560 mm)", "22″ (560 mm)", "28″ (710 mm)", "27-1/2″ (700 mm)", "40″ (1,040 mm)"]),
        ("Wheels", "TXT", ["Upper wheel and lower anvils", "Upper wheel and 6 lower forming wheels", "Upper wheel and 6 lower wheels; quick-change", "Upper wheel and 6 lower forming wheels",
                           "Upper wheel 7-5/8 × 3″ (195 × 75 mm); lower anvil radii 47, 55, 75, 220, 1,000 mm; hardened; 0.15 / 0.06 mm accuracy", "5 lower forming wheels; quick lever; sideways lower-wheel adjustment; foot pressure control"]),
        ("Frame", "TXT", ["Bench frame on stand", "Welded C-frame on stand", "Welded C-frame on stand", "Welded C-frame on stand", "Rigid welded C-frame, heavy stand with anvil storage", "Welded frame, professional version"]),
        ("Packing size L × W × H", "TXT", ["25 × 24 × 2″ (63 × 60 × 4.5 cm) body + 34 × 5 × 5″ (87 × 12 × 13 cm) stand", "33 × 29 × 13″ (84 × 74 × 34 cm)", "33 × 29 × 13″ (84 × 74 × 33 cm)",
                                           "35 × 31 × 11″ (89 × 80 × 27 cm)", "46 × 41 × 11″ (118 × 103 × 29 cm)", "72 × 37 × 14″ (183 × 93 × 35 cm)"]),
        ("*Weight", "KG", [17, 62, 57, 77, 110, 144]),
    ]),
]
CAT["tt-ew"] = ["F1.2 range: 6 forming wheels and the upper rolling wheel; quick-change on 560A", "F1.5×700: 700 mm throat; top anvil 195 × 75 mm; bottom anvil radius 47, 55, 75, 220, 1,000 mm; accuracy 0.15 / 0.06 mm; curved panels without heating and hammering — automotive; rigid welded C-frame; heavy stand with 4 mounting holes and anvil storage; hardened anvils",
                "F1.2×1000: professional, foot pressure control; quick lever; sideways adjustment of the lower wheels; 5 forming wheels"]

TAB["tt-dolly"] = [
    table("Dollies, mallets, clamps and body tools", "Hand tools for panel beating and auto body repair", ["Post dollies LD01 · SD01 · TD01 · HFD01", "SFD-9 · SFD-1 dolly stands", "TPD-3 · TD-3 · TCD-3 T-dollies", "BM-3 mallets",
                                                                                                                                 "WG100 – WG130 weld clamps", "NS-1 nibbler shears", "FR-120 · PFF-1 fender rollers", "DSI-1 door skin tool"], [
        ("*Job", "TXT", ["Cast-iron post dollies (loaf, shoe, teardrop, half football) — hand-held or in a vise", "Stands that hold post dollies at working height (SFD-1: 34-3/4″, 884 mm)",
                         "Tapered, T and curved T-dollies, small / medium / large", "Bossing mallets, right / middle / left", "Butt-weld panel clamps, weld grips and midget clamp sets",
                         "Cuts 22 ga stainless, 16 ga mild steel, 15 ga copper, 12 ga aluminum; 2.7 mm cut width", "Rolls the fender lip for tire clearance — hub-mounted (FR-120) or pneumatic (PFF-1)",
                         "Folds the edge of a new door skin onto the frame; 1-1/4 and 2″ nylon pads, 12″ handles"]),
    ]),
]
CAT["tt-dolly"] = ["post dollies of cast iron with an easy grip handle; SFD-1 holds any size dolly; WG: weld panel clamps for perfect butt welds, panels held edge to edge with almost no gap; NS-1 cuts with an upward action and no distortion",
                   "FR-120: for lowered vehicles and larger wheels; bolts to the hub flange (4- and 5-bolt, 4.75″ – 120.6 mm PCD); forming arm 14 – 22-3/4″; PFF-1 pneumatic fender former; DSI-1 door skin installation tool"]

# PDF p102 (199 – 200) — more English wheels and the diamond roller former
TAB["tt-ew2"] = [
    table("F1.5×1100 · F2.0×630 · F2.0×630B · F2.0×760", "Heavy English wheels, 14 – 16 ga, 24-4/5 – 45″ throat", ["F1.5×1100", "F2.0×630", "F2.0×630B", "F2.0×760"], [
        ("*Capacity, mild steel", "TXT", ["16 ga (1.5 mm)", "14 ga (2 mm)", "14 ga (2 mm)", "14 ga (2 mm)"]),
        ("*Throat depth", "TXT", ["45″ (1,145 mm)", "24-4/5″ (630 mm)", "24-4/5″ (630 mm)", "30″ (760 mm)"]),
        ("Wheels", "TXT", ["10 lower wheels and 4 upper rolling wheels; quick cam handle releases the panel", "Upper wheel Ø8″ (203.5 mm); 6 lower wheels 3″ wide: flat, 2, 4, 6, 8, 12″ radius",
                           "Upper wheel Ø8″ (203.5 mm); roll holder for anvil storage", "Upper wheel Ø8″ (203.5 mm); quick-release lower anvil support with locking cam"]),
        ("Size L × W × H", "TXT", ["67 × 60 × 16″ (170 × 152 × 40 cm) crate", "39 × 31 × 64″ (100 × 80 × 162 cm) machine", "39 × 20 × 39″ (100 × 50 × 98 cm) machine",
                                    "46 × 39 × 67″ (118 × 100 × 170 cm) machine"]),
        ("*Weight", "KG", [209, 166, 129, 298]),
    ]),
    table("PIC50", "Roller former that embosses a diamond pattern into sheet, 50″", ["PIC50"], [
        ("*Capacity", "TXT", ["20 ga mild steel × 50″ (1,270 mm)"]),
        ("*Pattern", "TXT", ["Diamonds 2-3/4 × 2-3/4″ (70 × 70 mm)"]),
        ("Speed", "TXT", ["9 – 16 rpm, adjustable"]),
        ("*Motor", "TXT", ["1 HP (750 W)"]),
        ("Packing size L × W × H", "PK", [(161, 140, 134)]),
        ("*Weight", "KG", [520]),
    ]),
]
CAT["tt-ew2"] = ["F1.5×1100: 45″ deep throat for large panels; rolls beads and forms mild steel to 1.5 mm; 10 lower and 4 upper wheels; quick cam release",
                 "F2.0 range: 2 mm mild steel; easy adjustment; triangular base for stability; F2.0×630B with roll holder", "PIC50: steel-welded frame; 20 ga × 50″; 1 HP; converts 1,270 mm sheet into a 70 × 70 mm diamond pattern"]

# ------------------------------------------------------------------------------------------------ pipe notchers and small punches
# PDF p103 – p104 (201 – 204)
TAB["tt-notcher"] = [
    table("PTN-30 · UTN40 · UTN40V · PTN-12U", "Motorized tube and pipe notchers", ["PTN-30", "UTN40", "UTN40V", "PTN-12U"], [
        ("*Capacity", "TXT", ["Tube 1/2 – 3″ OD, pipe 1/2 – 2-1/2″ schedule 40 (5/8 – 3″ OD)", "Tube 1/2 – 2″", "Tube 1/2 – 2″", "Pipe 1/4 – 2″ (inside diameter)"]),
        ("*Notch angle", "TXT", ["0 – 90°, large degree wheel", "Swivel vise, 1° steps", "Swivel vise, 1° steps", "—"]),
        ("*Cutter", "TXT", ["Bi-metal hole saws (1/2″-20 and 5/8″-18 arbors)", "End mill — no coolant, no dust", "End mill — no coolant, no dust", "Hole saws"]),
        ("*Motor / speed", "TXT", ["3/4 HP (0.55 kW); 230 rpm at 60 Hz (186 at 50 Hz)", "1.5 HP AC motor, 280 rpm", "1 HP DC motor, variable 75 – 250 rpm", "Electric"]),
        ("Packing size L × W × H", "PK", [(90, 63, 45), "—", "—", (82, 45, 48)]),
        ("*Weight", "KG", [65, 140, 120, 98]),
    ]),
    table("PNM 1-1/2 · PN-1/2 · RA · RAB", "Hole-saw pipe notchers for the drill press and hand drill, and hand tube notchers", ["PNM 1-1/2", "PN-1/2A", "PN-1/2S", "PN-1/2H", "RA-1 – RA-3", "RA-4 – RA-10", "RAB"], [
        ("*Capacity", "TXT", ["Tube 3/4 – 3″ OD; offset notches up to 1-1/2″", "Tube to 2″", "Tube to 2″", "Tube to 2″", "Pipe 1/4 – 2″ (inside diameter)", "Tube Ø22 – 50 mm (sizes per model)", "Vent notcher, wall to 0.155″"]),
        ("*Angle", "TXT", ["Up to 50°", "0 – 45°", "0 – 60°", "0 – 50°", "90°", "90°", "—"]),
        ("Drive", "TXT", ["Ordinary 1/2″ hand drill; bi-metal hole saws", "Drill press, 3/4″ spindle, 1/2 – 5/8″ adapter", "Drill press, 3/4″ spindle, 1/2 – 5/8″ adapter", "Drill press, 1″ spindle, 1/2 – 5/8″ adapter", "Hand lever", "Hand lever", "Hand lever"]),
        ("Frame", "TXT", ["CNC-machined, 1-1/4″ steel frame; 2-axis clamp; 1″ stainless shaft", "Aluminum", "Steel", "Aluminum", "Steel", "Steel", "Steel"]),
        ("*Weight", "KG", [9.5, 2.8, 4.5, 4, "13 – 31 lb (6 – 14 kg)", "24 – 37 lb (11 – 17 kg)", 6]),
    ]),
    table("FB-4 · BDS · HP-20", "Form bender, vise brake dies and hand punch", ["FB-4", "BDS-4", "BDS-5", "BDS-6", "BDS-8", "HP-20"], [
        ("*Job", "TXT", ["Cold forming of steel: bends, closed forms; stencil for roll bending", "Vise-mount brake dies, 4″ (100 mm)", "Vise-mount brake dies, 5″ (125 mm)", "Vise-mount brake dies, 6″ (150 mm)", "Vise-mount brake dies, 8″ (200 mm)",
                         "Hand lever punch for round, square and similar holes"]),
        ("*Capacity", "TXT", ["—", "14 ga (2 mm)", "14 ga (2 mm)", "14 ga (2 mm)", "14 ga (2 mm)", "14 ga (2 mm); throat 6.3″ (160 mm); dies 1/8 – 5/8″ or 3 – 20 mm"]),
        ("*Weight", "KG", [8.5, 1.1, 1.5, 2.1, 2.6, 81]),
    ]),
]
CAT["tt-notcher"] = ["PTN-30: notches 0.5 – 3″ tube and 0.5 – 2.5″ schedule 40 pipe; quick-release cam vise and solid taper lock for notch angles; large degree wheel; turn on, grab the hand wheel and rotate toward the material; two arbor threads (1/2″-20, 5/8″-18) for all optional hole saws",
                     "UTN40/40V: end mill for fast metal removal; V-block for quick set-up; swivel vise in 1° steps; no coolant; no dust or excessive noise; portable",
                     "PNM 1-1/2: 3/4 – 3″ OD; angles to 50°; CNC machined; 1-1/4″ steel frame; 2-axis clamp; offset notch to 1-1/2″; 1″ ground stainless shaft; bolt or clamp in a vise; inexpensive bi-metal hole saws; 1/2″ hand drill",
                     "PN-1/2: precision notcher for the drill press — round cuts in pipe and tubing at any angle; sturdy frame; base swivels and rotates for compound angles; PN-1/2H and A aluminum, S steel",
                     "HP-20: deep-hole round and square stamps; quick die change; stencil 34 × 34 × 16 mm; standard die 16 mm or 5/8″; metric 3 – 20 mm and inch 1/8 – 5/8″ die series at extra cost"]

# ------------------------------------------------------------------------------------------------ presses
# PDF p105 – p106 (205 – 208) — arbor presses, turret punches, bench presses
TAB["tt-arbor"] = [
    table("AP-1/2 – AP-8", "Arbor presses, 1/2 to 8 tons", ["AP-1/2", "AP-1", "AP-2", "AP-3", "AP-5", "AP-6", "AP-8"], [
        ("*Capacity", "TXT", ["1/2 ton", "1 ton", "2 tons", "3 tons", "5 tons", "6 tons", "8 tons"]),
        ("*Max. work height × diameter", "TXT", ["3.5 × 3.1″ (90 × 80 mm)", "4.3 × 3.9″ (110 × 100 mm)", "7.1 × 4.8″ (180 × 123 mm)", "11.2 × 6.4″ (285 × 163 mm)", "15.7 × 8.9″ (400 × 226 mm)",
                                                 "17.7 × 10.2″ (450 × 260 mm)", "17.7 × 10″ (450 × 255 mm)"]),
        ("Largest arbor", "F", [26, 29, 40, 44, 70, 65, 65]),
        ("Table", "D", [95, 120, 155, 185, 255, 260, 255]),
        ("Ram", "TXT", ["3/4″ (19 mm) square", "1″ (25 mm) square", "1-1/4″ (32 mm) square", "1-1/2″ (38 mm) square", "2″ (50 mm) square", "2″ (50 mm) square", "2-3/8 × 2-1/8″ (60 × 55 mm)"]),
        ("Overall height", "L", [280, 355, 445, 615, 815, 645, 650]),
        ("Base size", "TXT", ["9.4 × 6.7″ (240 × 170 mm)", "10.6 × 7.5″ (268 × 190 mm)", "17 × 10.2″ (432 × 260 mm)", "17.9 × 11.8″ (455 × 300 mm)", "25.4 × 6.9″ (645 × 176 mm)", "26 × 11″ (660 × 280 mm)", "25.2 × 10″ (640 × 255 mm)"]),
        ("*Weight", "KG", [7, 11, 30, 45, 118, 120, 130]),
    ]),
    table("AP-1S · AP-2S · MP-1 · RAP-2 · RAP-3 · MP-800", "Rack-and-pinion and ratchet presses, hand presses for small parts", ["AP-1S", "AP-2S", "MP-1", "RAP-2", "RAP-3", "MP-800"], [
        ("*Capacity", "TXT", ["2,248 lbf (10 kN)", "4,496 lbf (20 kN)", "2,248 lbf (10 kN)", "2 tons, ratchet", "3 tons, ratchet", "0.8 ton, flywheel"]),
        ("*Travel / opening", "TXT", ["Travel 5.9 + 2.4″ (150 + 60 mm)", "Travel 7.9 + 3.1″ (200 + 80 mm)", "Travel 4.7″ (120 mm); max. height 10.2″ (260 mm), dia. 7.9″ (200 mm)", "Opening 7.1″ (180 mm)", "Opening 15″ (380 mm)",
                                        "Stroke 0.08″ (2 mm); shut height 5.5″ (140 mm)"]),
        ("Table", "TXT", ["5.3 × 4.3″ (135 × 110 mm)", "6.1 × 4.7″ (155 × 120 mm)", "Ø9.3″ (235 mm)", "—", "—", "—"]),
        ("*Weight", "KG", [11, 16, 25, 44, 60, 38]),
    ]),
]
CAT["tt-arbor"] = ["AP: high-quality steel body; press-fitting and pulling bearings; 4-position plate"]

TAB["tt-tpunch"] = [
    table("TP-12A · TP-12B · TP-24A · TP-24B", "Manual turret punch presses, 12 stations, 6.6 US tons", ["TP-12A", "TP-12B", "TP-24A", "TP-24B"], [
        ("*Punching force", "TXT", "6.6 US tons (6,000 kg)"),
        ("*Throat depth", "TXT", ["12″ (305 mm)", "12″ (305 mm)", "24″ (608 mm)", "24″ (608 mm)"]),
        ("*Capacity", "TXT", "1/4″ (6 mm) — 3 ga mild steel; holes to 1-1/4″"),
        ("Stations", "TXT", "12 round punches: 3/16, 1/4, 5/16, 3/8, 1/2, 9/16, 5/8, 3/4, 7/8, 1, 1-1/8, 1-1/4″ (metric 5 – 32 mm)"),
        ("Stripper clearance / ram stroke", "TXT", "7/16″ (11 mm) / 21/32″ (17 mm)"),
        ("Stand", "TXT", ["Open stand (A)", "Cabinet stand with table (B)", "Open stand (A)", "Cabinet stand with table (B)"]),
        ("Packing size L × W × H", "PK", [(76, 53, 81), (81, 81, 157), (112, 45, 85), (120, 80, 160)]),
        ("*Weight", "KG", [270, 390, 455, 690]),
    ]),
]
CAT["tt-tpunch"] = ["two stands A and B; manual punching via hand lever; accurate and lower-cost machine; dies up to 2-1/4″ on special request; delivered with 12 round punches; square, oval, rectangular and other shaped punches and dies on request"]

TAB["tt-bench-press"] = [
    table("BP-3T · EBP-10T · BP3-F", "Bench presses for punch, flare, bead, louver and bend tooling", ["BP-3T", "EBP-10T", "BP3-F"], [
        ("*Capacity", "TXT", ["3 tons, hand lever", "10 tons, hydraulic, 4″ stroke", "Four hand stations"]),
        ("*Throat depth", "TXT", ["12″", "25″", "Two 12″ and two 3″ throats"]),
        ("Tool opening", "TXT", ["—", "6″", "—"]),
        ("*Tooling", "TXT", ["Industry-standard punches and dies for round, square and oblong holes; punch & flare and punch & bead tools; louver press tooling", "All BP-3T bench and louver press tooling; adaptor and die plate included",
                             "90° bend kit (3/8″ mild steel), stretcher (1.5 mm), corner punch (16 ga, 1 × 1″ cut), shrinker (1.5 mm) — four tools mounted at once"]),
        ("Packing size L × W × H", "PK", [(68, 38, 72), (135, 115, 63), (111, 88, 165)]),
        ("*Weight", "KG", [67, 335, 280]),
    ]),
]
CAT["tt-bench-press"] = ["BP-3T: punch & flare and punch & bead tools; round, square and oblong holes; rugged welded plate; bronze bushings; also a standard arbor press; all bench press and louver press tooling; 12″ throat",
                         "EBP-10T: 10-ton hydraulic bench press; accepts all BP-3T tooling; 6″ tool opening; 4″ stroke; 25″ extra deep throat",
                         "optional tooling: shear kit 16 ga; 90° bend kit 3/8″; corner punch 16 ga, 1 × 1″; louver punches 3/8″ in 1 – 5″; corner radius punch 1/4 – 1″ radius 16 ga; punch & flare kit 1 – 3″; punch & bead kit 1 – 3″; universal tool stand",
                         "BP3-F: rugged 5/16″ welded plate; four tools at once; production use; two 12″ throats (1, 3) and two 3″ throats (2, 4); optional stand"]

# PDF p107 (209 – 210)
TAB["tt-hb-horizontal"] = [
    table("HB-10T · HB-25T · HB-40T", "Hydraulic horizontal benders for flat bar, pipe and bar", ["HB-10T", "HB-25T", "HB-40T"], [
        ("*Bending force", "TXT", ["11 US tons (10 t)", "27.6 US tons (25 t)", "44 US tons (40 t)"]),
        ("*Flat bar", "R", [(115, 8), (120, 12), (160, 12)]),
        ("Vee bending die", "R", [(115, 105), (120, 80), (160, 80)]),
        ("Stroke", "L", [200, 250, 250]),
        ("Table", "TXT", ["38.2 × 9.8″ (970 × 250 mm)", "41.3 × 24.4″ (1,050 × 620 mm)", "41.3 × 24.4″ (1,050 × 620 mm)"]),
        ("Speed", "TXT", ["Bend / return 0.38 / 0.43 in/s (9.7 / 11 mm/s)", "Approach 0.79 in/s (20 mm/s), bend 0.11 in/s (2.8 mm/s)", "Approach 0.85 in/s (21.5 mm/s), bend 0.11 in/s (2.8 mm/s)"]),
        ("*Control", "TXT", ["Hand lever valve; mobile on casters", "Foot pedal; PLC touch screen; 33.5″ (850 mm) manual back gauge", "Foot pedal; PLC touch screen; 33.5″ (850 mm) manual back gauge"]),
        ("*Motor", "KW", [1.5, 1.1, 1.5]),
        ("Packing size L × W × H", "PK", [(134, 50, 125), (153, 80, 136), (155, 80, 136)]),
        ("*Weight", "KG", [150, 620, 635]),
    ]),
]
CAT["tt-hb-horizontal"] = ["HB-10T: hand control; adjustable pressure dial with gauge; bending / release speed 9.7 / 11 mm/s; 1.5 kW motor; mobile",
                           "HB-25T/40T: easy stroke adjustment at the front; feed speed by valve; massive ground-steel table; manual slide adjustment; foot pedal; adjustable pressure dial with gauge; 850 mm manual back gauge; forward up to 21.5 / 20 mm/s; bending 2.8 mm/s; PLC touch screen",
                           "special tools for pipe and flat bar at required angles made to order; uses: hooks, U-bolts, loops, eyes, brackets, clamps"]

# PDF p108 – p112 (211 – 220)
TAB["tt-riveter"] = [
    table("XM-5 – XM-30", "Hydraulic orbital (rolling) riveters, rivets Ø3/16 – 1-3/16″", ["XM-5", "XM-8", "XM-10", "XM-16", "XM-20", "XM-30"], [
        ("*Rivet diameter, max", "F", [5, 8, 10, 16, 20, 30]),
        ("*Force", "TXT", ["1,911 lbf (8.5 kN)", "2,923 lbf (13 kN)", "4,271 lbf (19 kN)", "7,644 lbf (34 kN)", "14,613 lbf (65 kN)", "22,481 lbf (100 kN)"]),
        ("Spindle travel", "L", [20, 30, 30, 50, 30, 30]),
        ("Head to table, max", "L", [120, 275, 275, 220, 250, 300]),
        ("Table", "TXT", ["Ø4.7″ (120 mm)", "9.8 × 7.9″ (250 × 200 mm)", "9.8 × 7.9″ (250 × 200 mm)", "13.8 × 9.8″ (350 × 250 mm)", "16.5 × 11.8″ (420 × 300 mm)", "19.7 × 14″ (500 × 355 mm)"]),
        ("Machine size L × W × H", "TXT", ["17 × 13 × 32″ (440 × 320 × 822 mm)", "33 × 24 × 69″ (850 × 600 × 1,750 mm)", "28 × 20 × 59″ (700 × 500 × 1,500 mm)", "31 × 23 × 73″ (800 × 585 × 1,850 mm)",
                                           "42 × 20 × 76″ (1,070 × 500 × 1,930 mm)", "51 × 23 × 87″ (1,300 × 580 × 2,200 mm)"]),
    ]),
]
CAT["tt-riveter"] = ["cold rolling riveting: the part keeps its fit without deformation; forming pressure only 1/10 of punch riveting; smooth, neat rivet heads; no vibration, low noise, low energy; efficient and low cost; safe and easy; replaces hammering, punching and hot riveting in auto, motorcycle, light industry, appliance and hardware work; with optional tools it works as a normal press; 11 rivet head forms"]

TAB["tt-shop-press"] = [
    table("HP-12N · HP-24N", "Press brakes for the shop press: 12 – 20 tons, 12 – 24″", ["HP-12N", "HP-24N"], [
        ("*Force", "TXT", ["12 tons (hydraulic ram and hand pump, removable for other pressing jobs)", "20 tons hydraulic"]),
        ("*Bending width × thickness", "TXT", ["12″ (305 mm) × 3/16″ (5 mm, 6 ga) mild steel", "24″ (610 mm): 14 ga (2 mm) mild steel half width, 16 ga (1.5 mm) full width, 12 ga (2.5 mm) aluminum, 18 ga (1.2 mm) stainless"]),
        ("Bending range", "TXT", "0 – 90°"),
        ("Min. reverse bend", "TXT", ["7/8″ (23 mm)", "5/8″ (16 mm)"]),
        ("Ram stroke", "L", [130, 260]),
        ("Packing size L × W × H", "PK", [(74, 58, 19), (77, 54, 18)]),
        ("*Weight", "KG", [52, 59]),
    ]),
    table("H-frame shop presses, 10 – 30 tons", "Hand-pump shop presses for the garage and maintenance shop", ["10 t bench (382101)", "12 t (382102)", "10 t (382103)", "20 t (382105)", "30 t (382106)"], [
        ("*Capacity", "TXT", ["10 tons", "12 tons", "10 tons", "20 tons", "30 tons"]),
        ("*Overall height", "L", [713, 1283, 1276, 1562, 1710]),
        ("Width", "L", [596, 514.4, 516.9, 670, 760]),
        ("Working space", "TXT", ["—", "2.6 – 39″ (66.7 – 990 mm)", "5.7 – 36.3″ (146 – 922 mm)", "5.7 – 36.3″ (146 – 922 mm)", "0.25 – 24.2″ (6.4 – 615 mm)"]),
        ("*Weight", "KG", [80, 54, 65, 116, 200]),
    ]),
    table("BP-16T · EBP-25T", "Workshop presses with V-blocks — hand pump or motorized pump", ["BP-16T", "EBP-25T"], [
        ("*Force", "TXT", ["18 US tons (160 kN)", "28 US tons (250 kN)"]),
        ("Stroke", "L", [160, 200]),
        ("*Pump", "TXT", ["Hand pump, low and high pressure: 0.16 / 0.03″ (4 / 0.8 mm) per stroke", "Motorized pump, infinitely variable pressure and speed: 0.35 in/s (8.8 mm/s)"]),
        ("Return speed", "TXT", ["0.59 in/s (15 mm/s)", "0.49 in/s (12.5 mm/s)"]),
        ("Oil reservoir", "LIT", [2.5, 5]),
        ("Packing size L × W × H", "PK", [(85, 70, 117), (98, 96, 108)]),
        ("*Weight", "KG", [215, 242]),
    ]),
    table("HP-20S – HP-100S · HP-20S-A – HP-100S-A", "H-frame workshop presses 22 – 110 US tons — S European design, S-A standard design", ["HP-20S", "HP-30S", "HP-50S", "HP-80S", "HP-100S"], [
        ("*Force", "TXT", ["22 US tons (200 kN)", "33 US tons (300 kN)", "55 US tons (500 kN)", "88 US tons (800 kN)", "110 US tons (1,000 kN)"]),
        ("Pressure", "MPA", [50, 60, 60, 40, 40]),
        ("*Travel", "TXT", ["7.9 + 17.7″ (200 + 450 mm)", "7.9 + 17.7″ (200 + 450 mm)", "9.8 + 17.7″ (250 + 450 mm)", "11.8″ (300 mm)", "11.8″ (300 mm)"]),
        ("Table", "TXT", ["7.9 × 11.8″ (200 × 300 mm)", "11.8 × 15.7″ (300 × 400 mm)", "14.2 × 19.7″ (360 × 500 mm)", "19.7 × 15.7″ (500 × 400 mm)", "31.5 × 15.7″ (800 × 400 mm)"]),
        ("*Weight", "KG", [290, 320, 460, 820, 960]),
    ]),
    table("HPP-60 · HPP-100 · HPP-160", "Motorized workshop presses with moving cylinder, 66 – 176 US tons", ["HPP-60", "HPP-100", "HPP-160"], [
        ("*Force", "TXT", ["66 US tons (600 kN)", "110 US tons (1,000 kN)", "176 US tons (1,600 kN)"]),
        ("Pressure, max", "MPA", [23.5, 27, 31]),
        ("*Stroke", "L", [410, 410, 410]),
        ("*Working width, max", "L", [750, 920, 1100]),
        ("Speeds: approach / press / return", "TXT", ["0.36 / 0.09 / 0.5 in/s (9.2 / 2.2 / 12.7 mm/s)", "0.36 / 0.11 / 0.48 in/s (9.2 / 2.7 / 12.3 mm/s)", "0.36 / 0.09 / 0.47 in/s (9.2 / 2.3 / 12 mm/s)"]),
        ("*Motor", "KW", [2.2, 3.0, 3.0]),
        ("Oil tank", "LIT", [30, 30, 30]),
        ("Packing size L × W × H", "PK", [(170, 100, 210), (187, 100, 248), (215, 120, 258)]),
        ("*Weight", "KG", [840, 1340, 1900]),
    ]),
]
CAT["tt-shop-press"] = ["HP-12N: H-frame; two V-blocks; high-strength steel; base with four wheels; the 12-ton ram and hand pump come off for other pressing jobs; ram can be lifted for more height",
                        "HP-24N: compact, powerful bending brake; 20 tons of hydraulic force; 14 ga, 0 – 90°; return springs bring the bending bar back every time",
                        "H-frame 10 – 30 t: rigid weldment; accurate hydraulics; pressing and clamping; straightening beams, shafts and sections",
                        "BP-16T / EBP-25T: functional design, simple operation; versatile press for service and repair shops; hand pump with low / high pressure (BP-16T); motorized pump with infinite pressure and speed regulation (EBP-25T); 2 V-blocks for straightening; pressure gauge",
                        "HPP: mobile cylinder; motorized drive; 2-step hydraulic unit; V-block table; hand pump with double operation; repair and assembly work",
                        "HP-S: European design (S) and standard design (S-A); packing sizes in the catalogue look wrong for HP-20S/30S (500×350×130 cm) — not shown"]

TAB["tt-hp"] = [
    table("HP-30 – HP-500", "Motorized H-frame hydraulic presses, 33 – 551 US tons", ["HP-30", "HP-50", "HP-63", "HP-80", "HP-100", "HP-150", "HP-200", "HP-300", "HP-400", "HP-500"], [
        ("*Force", "TXT", ["33 US tons (300 kN)", "55 US tons (500 kN)", "69 US tons (630 kN)", "88 US tons (800 kN)", "110 US tons (1,000 kN)", "165 US tons (1,500 kN)", "220 US tons (2,000 kN)", "331 US tons (3,000 kN)",
                           "441 US tons (4,000 kN)", "551 US tons (5,000 kN)"]),
        ("Pressure", "MPA", [25, 25, 25, 30, 30, 30, 31.5, 31.5, 31.5, 31.5]),
        ("*Piston travel + table travel", "TXT", ["7.9 + 10.6″ (200 + 270 mm)", "8.7 + 15.9″ (220 + 405 mm)", "8.7 + 15.9″ (220 + 405 mm)", "10.2 + 25.6″ (260 + 650 mm)", "9.8 + 15.9″ (250 + 405 mm)",
                                                  "9.8 + 15.9″ (250 + 405 mm)", "11.8 + 15.9″ (300 + 405 mm)", "11.8 + 15.9″ (300 + 405 mm)", "11.8 + 15.9″ (300 + 405 mm)", "11.8 + 15.9″ (300 + 405 mm)"]),
        ("*Table", "TXT", ["11.8 × 15.7″ (300 × 400 mm)", "13.8 × 18.9″ (350 × 480 mm)", "13.8 × 18.9″ (350 × 480 mm)", "15.7 × 30.7″ (400 × 780 mm)", "18.1 × 38.6″ (460 × 980 mm)", "18.1 × 38.6″ (460 × 980 mm)",
                           "19.7 × 39.4″ (500 × 1,000 mm)", "27.6 × 47.2″ (700 × 1,200 mm)", "31.5 × 47.2″ (800 × 1,200 mm)", "35.4 × 47.2″ (900 × 1,200 mm)"]),
        ("Machine size L × W × H", "PK", [(123, 55, 168), (148, 64, 200), (150, 65, 195), (170, 65, 200), (175, 75, 220), (179, 72, 220), (194, 80, 225), (210, 95, 270), (230, 100, 290), (230, 100, 290)]),
        ("Hydraulic station", "TXT", ["Built on", "Built on", "Built on", "Built on", "Separate, 29 × 25 × 38″ (73 × 63 × 96 cm)", "Separate, 29 × 25 × 38″ (73 × 63 × 96 cm)", "Separate, 35 × 31 × 42″ (90 × 80 × 106 cm)",
                                      "Separate, 43 × 47 × 53″ (110 × 120 × 135 cm)", "Separate, 43 × 47 × 53″ (110 × 120 × 135 cm)", "Separate, 43 × 47 × 53″ (110 × 120 × 135 cm)"]),
        ("*Weight", "KG", [420, 520, 620, 995, 1020, 1360, 1734, 4200, 5500, 6500]),
    ]),
    table("HPB-580 – HPB-2000 · HPB-580D – HPB-3000D", "H-frame presses with brake function — single cylinder or two cylinders (D) for wide bending", ["HPB-580", "HPB-790", "HPB-1010", "HPB-1500", "HPB-2000", "HPB-580D", "HPB-790D", "HPB-1000D", "HPB-1500D", "HPB-2000D", "HPB-3000D"], [
        ("*Force", "TXT", ["33 US tons (300 kN)", "55 US tons (500 kN)", "110 US tons (1,000 kN)", "165 US tons (1,500 kN)", "220 US tons (2,000 kN)", "33 US tons (300 kN)", "55 US tons (500 kN)", "110 US tons (1,000 kN)",
                           "165 US tons (1,500 kN)", "220 US tons (2,000 kN)", "331 US tons (3,000 kN)"]),
        ("Pressure", "MPA", [25, 25, 30, 30, 30, 25, 25, 31.5, 31.5, 31.5, 31.5]),
        ("*Travel", "TXT", ["11.8 + 10.6″ (300 + 270 mm)", "8.7 + 15.9″ (220 + 405 mm)", "9.8 + 15.9″ (250 + 405 mm)", "9.8 + 15.9″ (250 + 405 mm)", "11.8 + 15.9″ (300 + 405 mm)",
                            "8.7″ (220 mm)", "8.7″ (220 mm)", "9.8″ (250 mm)", "9.8″ (250 mm)", "11.8″ (300 mm)", "11.8″ (300 mm)"]),
        ("*Table", "TXT", ["11.8 × 15.7″ (300 × 400 mm)", "15.7 × 31.5″ (400 × 800 mm)", "18.1 × 38.6″ (460 × 980 mm)", "18.1 × 38.6″ (460 × 980 mm)", "19.7 × 39.4″ (500 × 1,000 mm)",
                           "47.2 × 11.8″ (1,200 × 300 mm)", "51.2 × 14.2″ (1,300 × 360 mm)", "59.1 × 17.3″ (1,500 × 440 mm)", "59.1 × 17.3″ (1,500 × 440 mm)", "63 × 19.7″ (1,600 × 500 mm)", "70.9 × 27.6″ (1,800 × 700 mm)"]),
        ("Machine size L × W × H", "PK", [(120, 55, 168), (143, 65, 197), (175, 75, 220), (175, 72, 220), (184, 80, 225), (186, 55, 170), (200, 64, 200), (240, 75, 220), (240, 75, 220), (270, 85, 220), (295, 110, 250)]),
        ("*Weight", "KG", [283, 578, 1278, 1540, 2032, 760, 1100, 1710, 1950, 2600, 4120]),
    ]),
    table("HP-20M1 – HP-200M1", "Presses with a sliding table, 22 – 220 US tons", ["HP-20M1", "HP-40M1", "HP-63M1", "HP-100M1", "HP-150M1", "HP-200M1"], [
        ("*Force", "TXT", ["22 US tons (200 kN)", "44 US tons (400 kN)", "69 US tons (630 kN)", "110 US tons (1,000 kN)", "165 US tons (1,500 kN)", "220 US tons (2,000 kN)"]),
        ("Pressure", "MPA", [25, 25, 25, 30, 30, 30]),
        ("*Stroke", "L", [300, 300, 300, 400, 400, 400]),
        ("Daylight, max", "L", [700, 700, 800, 900, 900, 1100]),
        ("*Table / table travel", "TXT", ["19.7 × 19.7″ (500 × 500 mm) / 23.6″ (600 mm)", "19.7 × 19.7″ (500 × 500 mm) / 23.6″ (600 mm)", "27.6 × 23.6″ (700 × 600 mm) / 23.6″ (600 mm)",
                                          "31.5 × 27.6″ (800 × 700 mm) / 23.6″ (600 mm)", "31.5 × 27.6″ (800 × 700 mm) / 23.6″ (600 mm)", "31.5 × 27.6″ (800 × 700 mm) / 23.6″ (600 mm)"]),
        ("Packing size L × W × H", "PK", [(140, 120, 200), (150, 140, 210), (160, 160, 220), (170, 170, 235), (170, 170, 235), (260, 190, 180)]),
        ("*Weight", "KG", [650, 980, 1020, 1520, 1750, 2260]),
    ]),
    table("HP-20C – HP-100C", "C-frame hydraulic presses, open on three sides, 22 – 110 US tons", ["HP-20C", "HP-30C", "HP-50C", "HP-63C", "HP-100C"], [
        ("*Force", "TXT", ["22 US tons (200 kN)", "33 US tons (300 kN)", "55 US tons (500 kN)", "69 US tons (630 kN)", "110 US tons (1,000 kN)"]),
        ("Pressure", "MPA", [25, 25, 31.5, 31.5, 31.5]),
        ("*Stroke", "L", [300, 300, 300, 300, 400]),
        ("*Table", "TXT", ["15.7 × 11.8″ (400 × 300 mm)", "15.7 × 11.8″ (400 × 300 mm)", "23.6 × 15.7″ (600 × 400 mm)", "27.6 × 19.7″ (700 × 500 mm)", "31.5 × 23.6″ (800 × 600 mm)"]),
        ("Machine size L × W × H", "PK", [(100, 60, 160), (110, 60, 160), (140, 80, 200), (150, 80, 220), (190, 100, 250)]),
        ("*Weight", "KG", [660, 1160, 2800, 3200, 4800]),
    ]),
    table("HP-50F – HP-315FK", "Four-column hydraulic presses, 55 – 347 US tons", ["HP-50F", "HP-100F", "HP-150F", "HP-200F", "HP-150F1", "HP-200F1", "HP-315F1", "HP-315FK"], [
        ("*Force", "TXT", ["55 US tons (500 kN)", "110 US tons (1,000 kN)", "165 US tons (1,500 kN)", "220 US tons (2,000 kN)", "165 US tons (1,500 kN)", "220 US tons (2,000 kN)", "347 US tons (3,150 kN)", "347 US tons (3,150 kN)"]),
        ("Pressure", "MPA", [50, 50, 60, 60, 31.5, 31.5, 32, 32]),
        ("*Stroke", "L", [300, 300, 300, 300, 300, 300, 400, 400]),
        ("*Table", "TXT", ["15.7 × 23.6″ (400 × 600 mm)", "19.7 × 27.6″ (500 × 700 mm)", "21.7 × 33.5″ (550 × 850 mm)", "21.7 × 33.5″ (550 × 850 mm)", "34.3 × 26.4″ (870 × 670 mm)", "38.2 × 27.6″ (970 × 700 mm)",
                           "42.9 × 31.5″ (1,090 × 800 mm)", "42.9 × 31.5″ (1,090 × 800 mm)"]),
        ("Control", "TXT", ["Separate pump unit"] * 4 + ["Separate pump unit"] * 3 + ["PLC touch-screen cabinet and pump unit"]),
        ("*Weight", "KG", [980, 1220, 1600, 1960, 3200, 4200, 8600, 8900]),
    ]),
]
CAT["tt-hp"] = ["HP: optional at extra cost: CE standard, complete protection, foot pedal switch, travel limit switch; lift device optional for HP-30/50/63/80",
                "HPB: with brake function; adjustable worktable; torsion-proof steel weldment; accurate hydraulics; replaceable top tools, V-block and support table with stops; table lifted by a chain driven by the main cylinder; HP-80M: mobile cylinder, manual and electric hydraulic station, fast-lifting table frame",
                "HPB-D: larger bending width; synchronizing device optional; angle micro-adjustment; saves energy",
                "M1: improved from the two-column press; the table moves out lengthwise — for press-fitting or dismantling large, heavy parts; simple and cost-effective; N.W./G.W. in the catalogue are swapped — the smaller figure is shown",
                "C: open C-type with three-side access; assembling and dismantling complex structures and large parts", "F: four-column sliding presses; F1 traditional model, rational structure, long life, for large plants"]

# PDF p113 (221 – 222)
TAB["tt-hammer"] = [
    table("C41-16KG – C41-75KG", "Self-contained pneumatic forging (air) hammers, 35 – 165 lb ram", ["C41-16KG", "C41-20KG", "C41-25KG", "C41-40KG", "C41-75KG"], [
        ("*Ram (falling) weight", "TXT", ["35 lb (16 kg)", "44 lb (20 kg)", "55 lb (25 kg)", "88 lb (40 kg)", "165 lb (75 kg)"]),
        ("*Blow energy", "TXT", ["133 ft·lbf (180 J)", "162 ft·lbf (220 J)", "199 ft·lbf (270 J)", "391 ft·lbf (530 J)", "664 ft·lbf (900 J)"]),
        ("Blows per minute", "TXT", ["258", "270", "250", "245", "210"]),
        ("Working height", "L", [180, 200, 240, 245, 300]),
        ("*Max. stock, square / round", "TXT", ["3/4″ (20 mm) / Ø3/4″ (20 mm)", "1-3/16″ (30 mm) / Ø1-3/8″ (35 mm)", "1-9/16″ (40 mm) / Ø1-3/4″ (45 mm)", "2″ (52 mm) / Ø2-5/8″ (68 mm)", "2-1/2″ (65 mm) / Ø3-3/8″ (85 mm)"]),
        ("*Motor", "TXT", ["2 HP (1.5 kW)", "3 HP (2.2 kW)", "3 HP (2.2 kW)", "5.5 HP (4 kW)", "9.4 HP (7 kW)"]),
        ("Anvil block", "TXT", ["—", "441 lb (200 kg)", "551 lb (250 kg)", "882 lb (400 kg)", "1,874 lb (850 kg)"]),
        ("Packing size L × W × H", "PK", [(116, 59, 107), (67, 37, 105), (80, 41, 121), (108, 60, 139), (160, 95, 195)]),
        ("*Weight", "KG", [240, 500, 760, 1350, 2800]),
    ]),
]
CAT["tt-hammer"] = ["general forging: drawing out, upsetting, punching, chiselling, forge welding, bending and twisting; also forging in bolster dies; catalogue 'beat capacity (kgf·m)' read as joules (C41-40: 0.53 kJ)"]
