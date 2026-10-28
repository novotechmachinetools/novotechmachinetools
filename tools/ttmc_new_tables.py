#!/usr/bin/env python3
"""Specification tables of the NovoTech value-line machines from TTMC's 2026 new-item sheets and catalogues (sold under
NovoTech's name with TTMC model codes, no supplier brand) — the items that are not in the Vol. 23 catalogue
(tools/ttmc_more_tables.py):

  sources (the owner's attachments, Oct 27 2026), /home/claude/ttmc-new/:
    new_items_rar/            2026 new items: bending (W2.0x2540H, HW2.0x2540H, BSM3150, EFMS-2540X1.5L, HBV-1250), C-type and
                              HP-F1/PLC presses, KSM-850, MGM-300, X6336, QCS-500A, RB365x3000D, SRB-320X2000D, MRT-15, WP-30T, WP-50
    brochure_rar/             TFM3100x2E / TFMS3100X2E folding machines, PS-1220x1.5GT slitter, CD-24 coil dispenser, positioner sheets
    pdf_a/a.pdf               "Welding positioners and welding supports" (14 pages)
    pdf_b/b.pdf               "Wood working machinery" (12 pages)

Metric values are the manufacturer's; the site shows imperial first with the metric value in brackets (tools/ttmc_conv.py).
Manual machines are not sold (see the scope note in tools/ttmc_more_data.py): the hand-turned WP30M / WP300SM / WP300M
positioners, hand tools (welding clamps, copper welder helpers) and the autobody tools are not listed.
"""
from ttmc_conv import table

TAB = {}

# =============================================================================================== sheet metal brakes
TAB["tt-pb-heavy2"] = [
    table("W2.0×1320H · W2.0×2540H", "Heavy pan and box brakes with extended fingers and digital angle gauge, 14 ga × 52″ and 100″",
          ["W2.0×1320H", "W2.0×2540H"], [
        ("*Bending length", "TXT", ["52″ (1,320 mm)", "100″ (2,540 mm)"]),
        ("*Capacity, mild steel", "T", 2.0),
        ("*Box depth / fingers", "TXT", ["Boxes and pans to 9″ (230 mm) deep; fingers 12″ × 1, 6″ × 2, 5″ × 2, 4″ × 3, 3″ × 2",
                                          "Boxes and pans to 9″ (230 mm) deep; fingers 12″ × 4, 6″ × 4, 5″ × 2, 4″ × 3, 3″ × 2"]),
        ("Back gauge", "L", 1125),
        ("Bending angle", "TXT", "0 – 120°; digital angle gauge"),
        ("Packing size L × W × H", "PK", [(193, 75, 172), (315, 75, 172)]),
        ("*Weight", "KG", [905, 1385]),
    ]),
]
TAB["tt-hw-h"] = [
    table("HW2.0×1320H · HW2.0×2540H", "Hydraulic pan and box brakes with NC angle control, 14 ga × 52″ and 100″", ["HW2.0×1320H", "HW2.0×2540H"], [
        ("*Bending length", "TXT", ["52″ (1,320 mm)", "100″ (2,540 mm)"]),
        ("*Capacity", "TXT", "14 ga (2 mm) mild steel"),
        ("Bending angle", "TXT", "0 – 120°"),
        ("*Box depth, max", "L", 230),
        ("Fingers", "TXT", ["12″ × 1, 6″ × 2, 5″ × 2, 4″ × 3, 3″ × 2", "12″ × 4, 6″ × 4, 5″ × 2, 4″ × 3, 3″ × 2"]),
        ("Back gauge", "L", 1125),
        ("Control", "TXT", "Single-program NC with programmable angle readout; foot pedal"),
        ("*Motor", "KW", [2.2, 3.0]),
        ("Packing size L × W × H", "PK", [(208, 73, 157), (330, 73, 172)]),
        ("*Weight", "KG", [1120, 1580]),
    ]),
]
TAB["tt-efms-l"] = [
    table("EFMS-2540×1.5L", "Electric folding machine with segmented beams and motorized clamping, 16 ga × 100″", ["EFMS-2540×1.5L"], [
        ("*Bending length", "TXT", "100″ (2,540 mm)"),
        ("*Capacity, mild steel", "T", 1.5),
        ("Bending angle", "TXT", "0 – 120°, set on a dial; limit switches"),
        ("Opening height", "TXT", "3-1/8″ (80 mm) clamping bar lift"),
        ("Blade", "TXT", "10 segments, 10″ (254 mm) wide"),
        ("*Motors", "TXT", "2 HP (1.5 kW) clamping, 3 HP (2.2 kW) folding"),
        ("Packing size L × W × H", "PK", (370, 90, 135)),
        ("*Weight", "KG", 1100),
    ]),
]
TAB["tt-tfm"] = [
    table("TFM 3100×2E · TFM 3680×2E · TFMS 3100×2E · TFMS 3680×2E",
          "CNC electric folding machines, 14 ga × 122″ and 145″ — TFMS with segmented upper beam",
          ["TFM 3100×2E", "TFM 3680×2E", "TFMS 3100×2E", "TFMS 3680×2E"], [
        ("*Bending length", "TXT", ["122″ (3,100 mm)", "144-7/8″ (3,680 mm)"] * 2),
        ("*Capacity", "TXT", "14 ga (2 mm) mild steel, 18 ga (1.2 mm) stainless"),
        ("Bending angle", "TXT", "0 – 135°, programmable"),
        ("Clamping opening", "TXT", "4-7/8″ (125 mm)"),
        ("Min. reverse bend", "TXT", "1/2″ (12.7 mm)"),
        ("*Back gauge", "TXT", "CNC, 1/2 – 48-3/8″ (12.7 – 1,228 mm), repeatability ±0.004″ (0.1 mm)"),
        ("Back gauge table height", "TXT", "35-3/4″ (910 mm)"),
        ("Upper beam", "TXT", ["One-piece"] * 2 + ["Segments 2″ × 7, 3″ × 2, 4″ × 4, 5″ × 10, 6″ × 6 — boxes 4″ (100 mm) deep; "
                                                  "10.5 and 25 mm one-piece beams also supplied"] * 2),
        ("*Motors", "TXT", ["4 HP (3 kW) main, 2 HP (1.5 kW) back gauge servo, 1-1/2 HP (1.1 kW) clamping",
                            "5-1/2 HP (4 kW) main, 2 HP (1.5 kW) back gauge servo, 2 HP (1.5 kW) clamping"] * 2),
        ("Control", "TXT", "Touch screen: 2,000 programs, 99 bends per program, profile library with graphics, radius bending and angle correction"),
        ("Packing size L × W × H", "PK", [(434, 201, 160), (496, 210, 150), (434, 201, 160), (496, 210, 150)]),
        ("*Weight", "KG", [4280, 5280, 4280, 5280]),
    ]),
]
TAB["tt-bsm-sb"] = [
    table("BSM1550 · BSM3150", "Shear and brake machines on a mobile stand, 22 ga × 61″ and 124″", ["BSM1550", "BSM3150"], [
        ("*Working length", "TXT", ["Bending 61″ (1,550 mm), shearing 59″ (1,500 mm)", "Bending 124″ (3,150 mm), shearing 122″ (3,100 mm)"]),
        ("*Bending and shearing capacity, mild steel", "T", 0.8),
        ("Bending angle", "TXT", "0 – 135°"),
        ("Stand", "TXT", "Mobile stand on casters; gas springs lift the bending beam and move the slitter head"),
        ("Packing size L × W × H", "PK", [(203, 87, 50), (363, 89, 52)]),
        ("*Weight", "KG", [195, 425]),
    ]),
]
TAB["tt-cd24"] = [
    table("CD-24", "Coil dispenser for trim coil on the job site", ["CD-24"], [
        ("*Coil width", "TXT", "To 24″ (610 mm)"),
        ("*Rolls", "TXT", "Two non-marring bottom rollers and a quick-release tension roller"),
        ("Stand", "TXT", "Folding support stand"),
        ("Cutting", "TXT", "Works with the cutter of the portable brake; roller cutter optional"),
        ("Packing size L × W × H", "PK", (102, 64, 18)),
        ("*Weight", "KG", 16),
    ]),
]
TAB["tt-hbv-l"] = [
    table("HBV-1250 · HBV-2540", "Hydraulic press brakes with two cylinders, 35 US tons, 49″ and 100″", ["HBV-1250", "HBV-2540"], [
        ("*Force", "TON", 32),
        ("*Bending width × thickness", "TXT", ["49-1/4″ (1,250 mm) × 3/16″ (5 mm)", "100″ (2,540 mm) × 1/8″ (3 mm)"]),
        ("Stroke", "L", 130),
        ("Open height, max", "L", 210),
        ("Speed, working and return", "TXT", "0.39 in/s (10 mm/s)"),
        ("Back gauge", "TXT", "24-3/8″ (620 mm), hand wheel with counter"),
        ("*Motor", "KW", 3.0),
        ("Packing size L × W × H", "PK", [(238, 142, 160), (367, 142, 160)]),
        ("*Weight", "KG", [1200, 1750]),
    ]),
]

# =============================================================================================== shears, saws, stands
TAB["tt-ps1220"] = [
    table("PS-1220×1.5GT", "Coil slitting and cut-to-length machine with decoiler and outfeed table, 16 ga × 48″", ["PS-1220×1.5GT"], [
        ("*Capacity", "TXT", "16 ga (1.5 mm) mild steel"),
        ("*Length", "TXT", "48″ (1,220 mm) slitting and shearing width"),
        ("Slitting", "TXT", "Up to 2 strips in 16 ga (1.5 mm), 3 in 20 ga (1 mm), 4 in 0.9 mm, 5 in 22 ga (0.8 mm), 6 in 0.7 mm, "
                            "7 in 0.6 – 0.5 mm"),
        ("*Strokes", "TXT", "35 strokes/min"),
        ("Feed speed", "TXT", "0 – 56 ft/min (0 – 17 m/min), automatic feed"),
        ("Decoiler", "TXT", "For 20″ (480 – 510 mm) coil ID, 48.4″ (1,230 mm) wide, 4,409 lb (2,000 kg)"),
        ("Outfeed table", "TXT", "120 × 49 × 30″ (306 × 125 × 76 cm)"),
        ("*Motor", "TXT", "3 HP (2.2 kW) slitter + 3 HP (2.2 kW) shear"),
        ("Packing size L × W × H", "PK", [[("machine", (172, 170, 145)), ("decoiler", (187, 88, 134)), ("table", (310, 30, 25))]]),
        ("*Weight", "KG", 2100),
    ]),
]
TAB["tt-qcs500a"] = [
    table("QCS-500A", "Aluminum cut-off saw with 20″ blade swivelling 0 – 180°, pneumatic clamping and descent", ["QCS-500A"], [
        ("*Blade diameter, max", "L", 500),
        ("*Round, 90° and 45°", "D", 170),
        ("*Rectangular, 90° and 45° left and right", "TXT", "10-1/4 × 5-1/8″ (260 × 130 mm) at 90°, 9-1/2 × 4″ (240 × 100 mm) at 45°"),
        ("*Blade speed", "RPM", 2800),
        ("*Motor", "KW", 2.2),
        ("Blade swivel", "TXT", "0 – 180°"),
        ("Drive", "TXT", "Belt"),
        ("Packing size L × W × H", "PK", (107, 107, 164)),
        ("*Weight", "KG", 340),
    ]),
]
TAB["tt-stand2"] = [
    table("RB365×3000D · SRB-320×1000D · SRB-320×2000D", "Roller conveyor with digital length stop and roller stands with side rollers",
          ["RB365×3000D", "SRB-320×1000D", "SRB-320×2000D"], [
        ("*Type", "TXT", ["Roller conveyor 120″ (3,050 mm) with digital length stop", "Roller stand 39″ (1,000 mm) with vertical side rollers",
                          "Roller stand 79″ (2,000 mm) with vertical side rollers"]),
        ("*Height", "TXT", ["29.9 – 41.7″ (760 – 1,060 mm)", "25.8 – 29.3″ (655 – 745 mm)", "25.8 – 29.3″ (655 – 745 mm)"]),
        ("Roller width", "TXT", ["14.4″ (365 mm)", "12.6″ (320 mm)", "12.6″ (320 mm)"]),
        ("*Load, max", "KG", [400, 600, 600]),
        ("Feed system", "TXT", ["Length stop moved by hand, with a digital readout; closed steel frame", "—", "—"]),
        ("Side rollers", "TXT", ["—", "Adjustable vertical side rollers guide the bar", "Adjustable vertical side rollers guide the bar"]),
        ("*Weight", "KG", [115, 80, 123]),
    ]),
]

# =============================================================================================== deburring, milling, presses
TAB["tt-mgm300"] = [
    table("MGM-300", "Finishing and deburring machine, 12″ working width", ["MGM-300"], [
        ("*Working width, max", "TXT", "12″ (300 mm)"),
        ("*Workpiece thickness", "TXT", "0.04 – 7-7/8″ (1 – 200 mm)"),
        ("Abrasive belt", "TXT", "12 × 41″ (310 × 1,040 mm); electric-eye belt tracking"),
        ("*Feed speed", "TXT", "4.9 – 23 ft/min (1.5 – 7 m/min), variable"),
        ("Contact roller", "TXT", "Rubber, Ø4-1/4 × 12-1/2″ (110 × 320 mm)"),
        ("Table height", "TXT", "Digital, mm / inch; four synchronized lifting posts"),
        ("Dust extraction", "TXT", "4″ (Ø100 mm) vacuum hose connection"),
        ("*Main motor", "KW", 4.0),
        ("Packing size L × W × H", "PK", (100, 160, 178)),
        ("*Weight", "KG", 540),
    ]),
]
TAB["tt-ksm850"] = [
    table("KSM-850", "Cylinder head and block resurfacing machine", ["KSM-850"], [
        ("*Workpiece, max L × W × H", "TXT", "33.5 × 13 × 6.3 – 17.3″ (850 × 330 × 160 – 440 mm)"),
        ("*Table travel", "L", 1115),
        ("*Cutter head, max", "TXT", "Ø13″ (330 mm), 1/2″ CBN / PCD insert and holder standard"),
        ("Head speed", "TXT", "300 – 1,200 rpm, variable"),
        ("Table feed", "TXT", "0 – 23.6 in/min (0 – 600 mm/min), variable, ball screw"),
        ("Cycle", "TXT", "Manual or continuous working cycle programs"),
        ("*Motors", "TXT", "2 HP (1.5 kW) head, 1 HP (0.75 kW) table"),
        ("Machine size L × W × H", "TXT", "64 × 43 × 66″ (163 × 110 × 168 cm)"),
        ("*Weight", "KG", 850),
    ]),
]
TAB["tt-hp-f1plc"] = [
    table("HP-100F1/PLC – HP-315F1/PLC", "Four-column hydraulic presses with PLC touch-screen control, 110 – 347 US tons",
          ["HP-100F1/PLC", "HP-150F1/PLC", "HP-200F1/PLC", "HP-250F1/PLC", "HP-315F1/PLC"], [
        ("*Force", "TXT", ["110 US tons (1,000 kN)", "165 US tons (1,500 kN)", "220 US tons (2,000 kN)", "276 US tons (2,500 kN)", "347 US tons (3,150 kN)"]),
        ("Pressure", "MPA", 31),
        ("*Stroke", "L", 300),
        ("Daylight, max", "L", [650, 650, 700, 700, 800]),
        ("*Table", "TXT", ["23.6 × 23.6″ (600 × 600 mm)", "23.6 × 23.6″ (600 × 600 mm)", "27.6 × 27.6″ (700 × 700 mm)",
                           "27.6 × 27.6″ (700 × 700 mm)", "31.5 × 31.5″ (800 × 800 mm)"]),
        ("Control", "TXT", "PLC touch-screen cabinet, foot pedal; separate hydraulic station"),
        ("Dimensions L × W × H", "TXT", ["43 × 31 × 93″ (110 × 80 × 235 cm)", "43 × 31 × 93″ (110 × 80 × 235 cm)", "102 × 35 × 55″ (260 × 90 × 140 cm)",
                                          "106 × 35 × 59″ (270 × 90 × 150 cm)", "118 × 39 × 83″ (300 × 100 × 210 cm)"]),
        ("Hydraulic station L × W × H", "TXT", ["39 × 35 × 55″ (100 × 90 × 140 cm)"] * 4 + ["43 × 39 × 59″ (110 × 100 × 150 cm)"]),
        ("*Weight", "KG", [1640, 1840, 2400, 2840, 3770]),
    ]),
]

# =============================================================================================== welding positioners and supports (pdf_a + 2026 sheets)
TAB["tt-wp-bench"] = [
    table("MRT-15 · WP-50 · WP-30T", "Benchtop welding positioners and rotary table, 33 – 110 lb", ["MRT-15", "WP-50", "WP-30T"], [
        ("*Load, horizontal / vertical", "TXT", ["33 / 22 lb (15 / 10 kg)", "110 / 66 lb (50 / 30 kg)", "66 / 44 lb (30 / 20 kg)"]),
        ("*Table / chuck", "TXT", ["4″ (100 mm) 3-jaw chuck, clamps Ø5/64 – 3-1/2″ (2 – 90 mm)",
                                   "Ø8″ (200 mm) table with 3-jaw chuck, clamps Ø5/64 – 3-1/2″ (2 – 90 mm)",
                                   "Ø12-3/8″ (315 mm) table, Ø2-9/16″ (65 mm) hollow bore"]),
        ("Table height", "TXT", ["—", "11-1/2″ (295 mm)", "15.4″ (390 mm)"]),
        ("*Rotation speed", "TXT", ["0 – 18 rpm", "0 – 6 rpm, digital display", "0 – 6.5 rpm"]),
        ("*Tilt", "TXT", ["0 – 90°, by hand", "0 – 90°, by hand", "0 – 90°, hand wheel"]),
        ("Motor", "TXT", ["150 W", "100 W", "80 W"]),
        ("Features", "TXT", ["Foot pedal; works horizontal or vertical for welding, grinding and cutting",
                             "Foot pedal; gas purge through the centre (Ø5/16″ / 8 mm hole, Ø3/8″ / 10 mm port)",
                             "Foot pedal; torch holder and chuck optional"]),
        ("Packing size L × W × H", "PK", [(37, 37, 32), (50, 30, 49), (52, 48, 51)]),
        ("*Weight", "KG", [17, 22, 35]),
    ]),
    table("WP-100T · WP-110 · WP-110T", "Chuck welding positioners for tube and pipe, 220 – 247 lb", ["WP-100T", "WP-110", "WP-110T"], [
        ("*Load, horizontal / vertical", "TXT", ["220 / 110 lb (100 / 50 kg)", "247 / 121 lb (112 / 55 kg)", "247 / 121 lb (112 / 55 kg)"]),
        ("*Table / chuck", "TXT", ["8″ (200 mm) 3-jaw chuck; Ø2-3/8″ (60 mm) hollow bore with reducer", "8″ (200 mm) 3-jaw chuck",
                                   "8″ (200 mm) 3-jaw chuck; Ø2-9/16″ (65 mm) hollow bore"]),
        ("Table height", "TXT", ["16.5″", "—", "—"]),
        ("*Rotation speed", "TXT", ["0 – 6 rpm", "0 – 8 rpm", "0 – 8 rpm"]),
        ("*Tilt", "TXT", ["0 – 90°, by hand", "0°, 30°, 60° or 90°, pin-locked", "0°, 30°, 60° or 90°, pin-locked"]),
        ("Motor", "TXT", ["120 W variable-speed AC", "125 W", "125 W"]),
        ("Features", "TXT", ["Benchtop; foot pedal", "Foot pedal; forward / reverse; auto mode", "Foot pedal; forward / reverse; auto mode"]),
        ("Packing size L × W × H", "PK", [(70, 55, 45), (50, 53, 58), (50, 53, 58)]),
        ("*Weight", "KG", [110, 65, 65]),
    ]),
]
TAB["tt-wp-tilt"] = [
    table("WP-220 · WP-350 · WP-500 · WP-500T", "Tilting welding positioners, 485 – 1,102 lb", ["WP-220", "WP-350", "WP-500", "WP-500T"], [
        ("*Load, horizontal / vertical", "TXT", ["485 / 220 lb (220 / 100 kg)", "772 / 265 lb (350 / 120 kg)", "1,102 / 551 lb (500 / 250 kg)",
                                                 "1,102 / 551 lb (500 / 250 kg)"]),
        ("*Table / chuck", "TXT", ["Ø13″ (330 mm) table", "Ø13″ (330 mm) table", "Ø21.7″ (550 mm) table", "Ø21.7″ (550 mm) table, Ø6-11/16″ (170 mm) hollow chuck"]),
        ("Table height", "L", [450, 480, 660, 660]),
        ("*Rotation speed", "TXT", "0 – 5 rpm, variable"),
        ("*Tilt", "TXT", ["0 – 135°, by hand", "0 – 135°, by hand", "0 – 135°, motorized", "0 – 135°, motorized"]),
        ("Motor", "TXT", ["125 W", "125 W", "400 W rotation; tilt motor", "400 W rotation; tilt motor"]),
        ("Packing size L × W × H", "PK", [(64, 49, 63), (64, 44, 63), (82, 73, 71), (82, 73, 71)]),
        ("*Weight", "KG", [34, 38, 220, 230]),
    ]),
]
TAB["tt-wp-heavy"] = [
    table("WP-1000 · WP-2000 · WP-3000", "Heavy welding positioners with power tilt, 3,307 – 8,818 lb", ["WP-1000", "WP-2000", "WP-3000"], [
        ("*Load, horizontal / vertical", "TXT", ["3,307 / 2,205 lb (1,500 / 1,000 kg)", "5,512 / 4,409 lb (2,500 / 2,000 kg)", "8,818 / 5,952 lb (4,000 / 2,700 kg)"]),
        ("*Table / chuck", "TXT", ["Ø39.4″ (1,000 mm) table", "Ø43.3″ (1,100 mm) table", "Ø47.2″ (1,200 mm) table"]),
        ("Table height", "L", [1059, 1118, 1213]),
        ("Load centre of gravity, max", "TXT", "12″ from the table centre and 12″ from the table face"),
        ("*Rotation speed", "TXT", "0.1 – 1.2 rpm"),
        ("*Tilt", "TXT", "0 – 135°, motorized — 135° in 57 s"),
        ("Motor", "KW", [0.75, 1.5, 1.5]),
        ("Control", "TXT", "Hand pendant and foot pedal; high-frequency protected"),
        ("Packing size L × W × H", "PK", [(170, 130, 130), (190, 150, 130), (200, 150, 140)]),
        ("*Weight", "KG", [1170, 1550, 1790]),
    ]),
]
TAB["tt-wp-acc"] = [
    table("WPC-200 · WPC-300 · WPC-400", "Self-centring 3-jaw welding chucks for the positioners", ["WPC-200", "WPC-300", "WPC-400"], [
        ("*Clamping, outside", "TXT", ["Ø4.3 – 8.3″ (110 – 210 mm)", "Ø6.7 – 11.8″ (170 – 300 mm)", "Ø9.8 – 15″ (250 – 380 mm)"]),
        ("*Clamping, inside", "TXT", ["Ø0.4 – 5.1″ (10 – 130 mm)", "Ø3.1 – 7.5″ (80 – 190 mm)", "Ø4.7 – 9.8″ (120 – 250 mm)"]),
        ("Centre hole", "TXT", ["Ø3.1″ (80 mm)", "Ø3.9″ (100 mm)", "Ø6.7″ (170 mm)"]),
        ("Clamping force", "KG", [200, 250, 350]),
        ("*Load, max", "KG", [30, 120, 240]),
    ]),
    table("WGS215 · WGS370 · WGS540", "Adjustable welding torch holders", ["WGS215", "WGS370", "WGS540"], [
        ("*Horizontal arm", "TXT", ["8.5″ (215 mm)", "14.6″ (370 mm)", "21.3″ (540 mm)"]),
        ("*Vertical post", "TXT", "11.8, 23.6, 39.4, 47.2 or 59″ (300, 600, 1,000, 1,200 or 1,500 mm)"),
    ]),
]
TAB["tt-trs"] = [
    table("TRS1000 · TRS1200 · TRS2200 · TRS5000", "Welding turning rolls (rotators), one drive and one idler per set, 2,205 – 11,023 lb",
          ["TRS1000", "TRS1200", "TRS2200", "TRS5000"], [
        ("*Load per set", "KG", [1000, 1200, 2200, 5000]),
        ("*Work diameter", "TXT", ["Ø1-1/2 – 24″ (38 – 609 mm)", "Ø7.9 – 31.5″ (200 – 800 mm)", "Ø4 – 60″ (101 – 1,524 mm)", "Ø12 – 96″ (304 – 2,438 mm)"]),
        ("*Surface speed", "TXT", ["0 – 78 in/min (0 – 1,978 mm/min)", "0 – 56 in/min (0 – 1,413 mm/min)", "0 – 143 in/min (0 – 3,641 mm/min)",
                                   "0 – 69 in/min (0 – 1,745 mm/min)"]),
        ("Wheels", "TXT", ["Ø8 × 2-9/16″ (203 × 65 mm)", "Ø8 × 2-9/16″ (203 × 65 mm)", "Ø10 × 3″ (254 × 76 mm)", "Ø12 × 4″ (305 × 100 mm)"]),
        ("Motor", "TXT", ["150 W", "250 W", "500 W", "500 W"]),
        ("Packing size L × W × H", "PK", [(65, 57, 50), (63, 66, 48), (102, 82, 50), (150, 105, 70)]),
        ("*Weight", "KG", [90, 86, 220, 325]),
    ]),
]
TAB["tt-wtr"] = [
    table("WTR450 · WTR2250 · WTR4500", "Outboard support stands with screw height adjustment", ["WTR450", "WTR2250", "WTR4500"], [
        ("*Load, max", "KG", [450, 2250, 4500]),
        ("*Work diameter", "TXT", ["Ø2 – 36″ (50 – 915 mm)", "Ø2 – 36″ (50 – 916 mm)", "Ø10 – 48″ (254 – 1,219 mm)"]),
        ("Wheels", "TXT", ["Ø8 × 2-9/16″ (203 × 65 mm)", "Ø8 × 2-9/16″ (203 × 65 mm)", "Ø12 × 4″ (305 × 100 mm)"]),
        ("*Height", "TXT", ["25.7″ (652 mm) min., screw travel 8″ (205 mm)", "28″ (712 mm) min., screw travel 8″ (205 mm)",
                            "34.9″ (887 mm) min., screw travel 8″ (205 mm)"]),
        ("Packing size L × W × H", "PK", [(77, 54, 79), (80, 54, 85), (116, 68, 100)]),
        ("*Weight", "KG", [55, 65, 250]),
    ]),
    table("MR3000 · MR3000A · MR5000 · MR7000D · MH5500 · MH9000", "Pipe stands and pipe supports, 6,600 – 19,800 lb",
          ["MR3000", "MR3000A", "MR5000", "MR7000D", "MH5500", "MH9000"], [
        ("*Load, max", "TXT", ["6,600 lb (3,000 kg)", "6,600 lb (3,000 kg)", "11,000 lb (5,000 kg)", "15,400 lb (7,000 kg)", "12,100 lb (5,500 kg)",
                               "19,800 lb (9,000 kg)"]),
        ("*Work diameter", "TXT", ["Ø4 – 48″ (101 – 1,219 mm)", "Ø4 – 48″ (101 – 1,219 mm)", "Ø4 – 60″ (101 – 1,524 mm)", "Ø4 – 60″ (101 – 1,524 mm)",
                                   "60″ (1,524 mm) wide", "72″ (1,830 mm) wide"]),
        ("Wheels", "TXT", ["Ø8″ (203 mm), polyurethane-covered steel", "Ø8″ (203 mm), polyurethane-covered steel", "Ø12″ (304 mm), polyurethane-covered steel",
                           "Ø12″ (304 mm), polyurethane-covered steel", "—", "—"]),
        ("*Height", "TXT", ["34 – 42″ (865 – 1,070 mm)", "41 – 49″ (1,054 – 1,259 mm), double height adjustment", "31 – 44″ (800 – 1,122 mm)",
                            "34 – 47″ (876 – 1,192 mm), three-point legs", "36″ (915 mm)", "18″ (460 mm)"]),
        ("Packing size L × W × H", "PK", [(137, 100, 96), (137, 100, 115), (163, 100, 100), (177, 100, 107), (163, 98, 107), (194, 71, 61)]),
        ("*Weight", "KG", [120, 145, 230, 390, 90, 127]),
    ]),
    table("PJV-1100 · PJV-450B · PJ-450SW · PTR-185 · PTR-610 · PTR-800 · PTR-1090A", "Folding pipe jacks and pipe roller stands",
          ["PJV-1100", "PJV-450B", "PJ-450SW", "PTR-185", "PTR-610", "PTR-800", "PTR-1090A"], [
        ("*Head", "TXT", ["V-head", "Ball-transfer head", "Roller head with steel wheels", "Two rollers", "Two rollers", "Two rollers", "Two rollers"]),
        ("*Load, max", "TXT", ["2,400 lb (1,100 kg)", "1,000 lb (450 kg)", "1,000 lb (450 kg)", "1,100 lb (500 kg)", "1,100 lb (500 kg)", "1,100 lb (500 kg)",
                               "1,100 lb (500 kg)"]),
        ("*Height", "TXT", ["28 – 51″ (710 – 1,300 mm)", "28 – 51″ (710 – 1,300 mm)", "28 – 51″ (710 – 1,300 mm)", "7-1/4″ (185 mm)", "24″ (610 mm)",
                            "31″ (800 mm)", "29 – 43″ (740 – 1,090 mm)"]),
        ("Pipe size", "TXT", ["—", "—", "—", "Ø1/2 – 36″ (12 – 910 mm)", "Ø1/2 – 36″ (12 – 910 mm)", "Ø1/2 – 36″ (12 – 910 mm)", "Ø1/2 – 36″ (12 – 910 mm)"]),
        ("Packing size L × W × H", "PK", [(80, 25, 20), (80, 25, 20), (80, 25, 20), "—", "—", "—", "—"]),
        ("*Weight", "KG", [14, 15, 14, 21, 32, 33, 33]),
    ]),
]
TAB["tt-wtable"] = [
    table("WT-36X24", "Mobile welding table with CNC hole pattern", ["WT-36X24"], [
        ("*Table top", "TXT", "36 × 24 × 5/8″ (910 × 610 × 16 mm), flat to 0.006″ (0.15 mm), reversible, nitrided black-oxide finish"),
        ("*Holes", "TXT", "216 × Ø5/8″ (16 mm) on a 2″ (50 mm) grid"),
        ("*Load, max", "KG", 680),
        ("Standard", "TXT", "Tube and pipe notcher, drop-down working tray, shelves, leveling feet and casters"),
        ("Packing size L × W × H", "PK", (102, 72, 108)),
        ("*Weight", "KG", 170),
    ]),
    table("MDT-4840 · MDT-6137 · MDT-6022", "Metalworking downdraft tables for grinding, sanding and welding fumes", ["MDT-4840", "MDT-6137", "MDT-6022"], [
        ("*Table", "TXT", ["46 × 38.7″ (1,168 × 982 mm)", "61 × 36.8″ (1,550 × 935 mm)", "61-3/16 × 20″ (1,555 × 510 mm)"]),
        ("*Air flow", "TXT", ["1,350 CFM at the base", "1,350 CFM at the base", "3,700 CFM (2 × 1,850 CFM)"]),
        ("*Filtration", "TXT", ["3 stages: aluminum pre-filter (G2), cartridge (F7), HEPA (H13)", "3 stages: aluminum pre-filter (G2), cartridge (F7), HEPA (H13)",
                                "4 panel filters 19 × 15 × 1″, 300 micron"]),
        ("Motor", "KW", [1.5, 3.0, 0.55]),
        ("Table load, max", "KG", [700, 700, 200]),
        ("Table height", "L", [985, 985, 750]),
        ("Other", "TXT", ["Compressed air 60 – 90 psi (4.1 – 6.2 bar) for filter cleaning", "—", "1/8″ steel table inserts, two swarf trays, ≤78 dB"]),
        ("Packing size L × W × H", "PK", [(156, 117, 208), (201, 117, 203), (178, 75, 100)]),
        ("*Weight", "KG", [355, 470, 150]),
    ]),
]

# =============================================================================================== woodworking (pdf_b)
TAB["tt-wm"] = [
    table("WM2000 · WM2200 · WM2200R · WM2500E", "Multifunction woodworking machines — planing, sawing, milling and drilling",
          ["WM2000", "WM2200", "WM2200R", "WM2500E"], [
        ("*Planing width", "TXT", ["7.9″ (200 mm)", "9.8″ (250 mm)", "9.8″ (250 mm)", "9.8″ (250 mm)"]),
        ("Planing depth per pass", "TXT", ["0 – 1/8″ (0 – 3 mm)", "0 – 9/64″ (0 – 3.5 mm)", "0 – 9/64″ (0 – 3.5 mm)", "0 – 9/64″ (0 – 3.5 mm)"]),
        ("*Saw blade / depth of cut", "TXT", ["Ø8-1/4″ (210 mm) / 2-3/4″ (70 mm)", "Ø9-7/8″ (250 mm) / 3-3/8″ (85 mm)", "Ø9-7/8″ (250 mm) / 3-3/8″ (85 mm)",
                                              "Ø11″ (280 mm) / 4″ (100 mm)"]),
        ("Saw table L × W", "TXT", ["28 × 19.7″ (710 × 500 mm)", "29.5 × 20.1″ (750 × 510 mm)", "29.5 × 20.1″ (750 × 510 mm)", "29.5 × 20.1″ (750 × 510 mm)"]),
        ("Planer tables L × W", "TXT", ["27.6 × 8.7″ (700 × 220 mm)", "34.7 × 12.5″ (882 × 318 mm)", "39.4 × 12.5″ (1,000 × 318 mm)", "34.7 × 12.5″ (882 × 318 mm)"]),
        ("Milling and drilling table", "TXT", ["—", "14.6 × 7.9″ (370 × 200 mm)", "14.6 × 7.9″ (370 × 200 mm)", "14.6 × 7.9″ (370 × 200 mm)"]),
        ("Thicknessing", "TXT", ["—", "—", "9.8 × 6.3″ (250 × 160 mm); table 22.8 × 9.8″ (580 × 250 mm)", "—"]),
        ("Cutting and planing angles", "TXT", "0 – 45° with the devices"),
        ("Knives", "TXT", ["2 × 7.9″ (200 mm), regrindable", "2 × 9.8″ (250 mm), regrindable", "2 × 9.8″ (250 mm), regrindable", "2 × 9.8″ (250 mm), regrindable"]),
        ("*Motor", "TXT", ["2.7 HP (2 kW), 5,500 rpm", "3 HP (2.2 kW), 5,500 rpm", "3 HP (2.2 kW), 5,500 rpm", "3.4 HP (2.5 kW), 5,500 rpm; starts at 160 V"]),
        ("Packing size L × W × H", "PK", [(86, 52, 25), (92, 58.5, 30), (104, 52.5, 53.5), (92, 58.5, 33)]),
        ("*Weight", "KG", [43, 59, 78, 60]),
    ]),
]
TAB["tt-wj"] = [
    table("WJ-6x55 · WJ-8x76", "Jointers with spiral cutterhead, 6″ and 8″", ["WJ-6x55", "WJ-8x76"], [
        ("*Cutting width", "TXT", ["6″ (153 mm)", "8″ (200 mm)"]),
        ("Cutting depth, max", "TXT", "1/8″ (3 mm)"),
        ("Stock, min", "TXT", ["8″ (200 mm) long, 1/2″ (12 mm) thick", "10″ (254 mm) long, 1/2″ (12 mm) thick"]),
        ("*Cutterhead", "TXT", ["Spiral, 15 × 15 × 2.5 mm indexable carbide inserts, 4,800 rpm", "Spiral, 14 × 14 × 2 mm indexable carbide inserts, 4,800 rpm"]),
        ("Fence", "TXT", "36 × 5″ (915 × 127 mm), tilts 45 – 135° with stops at 45°, 90° and 135°"),
        ("*Tables L × W", "TXT", ["55-1/2 × 6″ (1,410 × 153 mm)", "76 × 8″ (1,930 × 203 mm)"]),
        ("Packing size L × W × H", "PK", [[("stand", (83, 50, 82)), ("body", (170, 57, 34))], [("stand", (103, 54, 82)), ("body", (206, 62, 34))]]),
        ("*Weight", "KG", [180, 230]),
    ]),
    table("WJ10X40", "Surface planer, 10″", ["WJ10X40"], [
        ("*Cutting width", "TXT", "10″ (260 mm)"),
        ("Cutting depth, max", "TXT", "3/16″ (5 mm)"),
        ("*Cutterhead", "TXT", "Straight, 3 knives, 6,500 rpm"),
        ("Fence", "TXT", "Tilts 0 – 45°"),
        ("*Tables L × W", "TXT", "41-5/16″ (1,050 mm) long"),
        ("Motor", "KW", 2.2),
        ("Packing size L × W × H", "PK", (113, 55, 93)),
        ("*Weight", "KG", 158),
    ]),
]
TAB["tt-tdm"] = [
    table("TDM-260 · TDM-320 · TDM-410", "Surface planer and thicknesser combinations, 10 – 16″", ["TDM-260", "TDM-320", "TDM-410"], [
        ("*Planing width", "TXT", ["10.2″ (260 mm)", "12.6″ (320 mm)", "16.1″ (410 mm)"]),
        ("Table length", "TXT", ["41.3″ (1,050 mm)", "59″ (1,500 mm)", "70.9″ (1,800 mm)"]),
        ("Cutting depth, max", "TXT", ["1/8″ (3 mm)", "3/16″ (5 mm)", "3/16″ (5 mm)"]),
        ("*Thicknessing height", "TXT", ["0.12 – 6.3″ (3 – 160 mm)", "0.12 – 9.1″ (3 – 230 mm)", "0.12 – 8.9″ (3 – 225 mm)"]),
        ("Feed speed", "MMIN", 6),
        ("Fence", "TXT", ["Tilts 90 – 45°", "43 × 6″ (1,100 × 150 mm), tilts 90 – 45°", "Tilts 90 – 45°"]),
        ("*Motor", "KW", [2.2, 2.2, 3.0]),
        ("Packing size L × W × H", "PK", [(118, 59, 95), (160, 62, 98), (183, 67, 98)]),
        ("*Weight", "KG", [198, 285, 420]),
    ]),
]
TAB["tt-wjp"] = [
    table("WJP-15B · WJP-15 · WJP-20", "Thickness planers with spiral cutterhead, 15″ and 20″", ["WJP-15B", "WJP-15", "WJP-20"], [
        ("*Cutting width", "TXT", ["15″ (381 mm)", "15″ (381 mm)", "20″ (500 mm)"]),
        ("*Stock thickness", "TXT", ["1/4 – 8-1/4″ (6.35 – 210 mm)", "3/16 – 8″ (5 – 203 mm)", "3/16 – 8″ (5 – 200 mm)"]),
        ("Cutting depth, max", "TXT", "1/8″ (3 mm)"),
        ("*Cutterhead", "TXT", ["Spiral, 15 × 15 × 2.5 mm carbide inserts, 5,000 rpm", "Spiral, 15 × 15 × 2.5 mm carbide inserts, 4,750 rpm",
                                "Spiral, 14 × 14 × 2 mm carbide inserts, 4,800 rpm"]),
        ("Feed", "TXT", "Two feed speeds"),
        ("Table with extensions", "TXT", ["20-1/4 × 15″ (515 × 381 mm)", "42-1/8 × 15″ (1,072 × 381 mm)", "55-1/2 × 20″ (1,410 × 508 mm)"]),
        ("Type", "TXT", ["Benchtop, 3 HP", "Floor model with mobile base", "Floor model with mobile base"]),
        ("Packing size L × W × H", "PK", [(94, 64, 72), (92, 73, 130), (109, 87, 125)]),
        ("*Weight", "KG", [145, 273, 380]),
    ]),
]
TAB["tt-wts"] = [
    table("WTS10-30 · WTS10-50 · WTS10-30S · WTS10-50S", "10″ cabinet table saws — S models with touch-screen blade height and angle",
          ["WTS10-30", "WTS10-50", "WTS10-30S", "WTS10-50S"], [
        ("*Blade", "TXT", "10″ (254 mm), 3,550 rpm; dado 8″ (203 mm) to 13/16″ (20.6 mm) wide"),
        ("*Depth of cut, 90° / 45°", "TXT", "3-3/8 / 2-1/4″ (80 / 55 mm)"),
        ("*Rip capacity, right / left of blade", "TXT", ["30 / 20″ (760 / 520 mm)", "52 / 20″ (1,320 / 520 mm)", "30 / 20″ (760 / 520 mm)", "52 / 20″ (1,320 / 520 mm)"]),
        ("Cast-iron table", "TXT", "40 × 27″ (1,025 × 690 mm)"),
        ("Blade tilt", "TXT", "45° left"),
        ("Blade height and angle", "TXT", ["Hand wheels", "Hand wheels", "Touch screen with digital display", "Touch screen with digital display"]),
        ("*Motor", "KW", 2.2),
        ("Dust port", "TXT", "4″ (100 mm)"),
        ("Overall size L × W × H", "TXT", ["64 × 37 × 41″ (1,630 × 930 × 1,040 mm)", "84 × 37 × 41″ (2,138 × 930 × 1,040 mm)", "64 × 38 × 41″ (1,630 × 970 × 1,040 mm)",
                                            "84 × 38 × 41″ (2,138 × 970 × 1,040 mm)"]),
        ("*Weight", "KG", [211, 225, 234, 248]),
    ]),
]
TAB["tt-tbs"] = [
    table("TBS-356 · TBS-457", "14″ and 18″ deluxe band saws for wood", ["TBS-356", "TBS-457"], [
        ("*Resaw height", "TXT", ["13″ (330 mm)", "12″ (305 mm)"]),
        ("*Throat", "TXT", ["13.6″ (346 mm)", "18.4″ (467 mm)"]),
        ("Blade", "TXT", ["1/8 – 3/4″ (3 – 19 mm) wide, 111″ (2,819 mm) long", "1/4 – 1-1/4″ (6 – 32 mm) wide, 142″ (3,607 mm) long"]),
        ("Table", "TXT", ["16 × 21.5″ (406 × 546 mm), tilts 10° left and 45° right", "21 × 19″ (533 × 483 mm), tilts 10° left and 45° right"]),
        ("Blade speeds", "TXT", ["2 speeds: 1,250 / 2,620 ft/min (380 / 800 m/min)", "2 speeds: 1,510 / 3,215 ft/min (460 / 980 m/min)"]),
        ("*Motor", "TXT", ["1.5 HP (1.1 kW), 115 / 230 V", "3 HP (2.2 kW)"]),
        ("Size H × W × D", "TXT", ["73 × 30 × 25″ (1,850 × 762 × 635 mm)", "76 × 38 × 27″ (1,930 × 969 × 694 mm)"]),
        ("Packing size L × W × H", "PK", [(139, 48, 60), (201, 60, 103)]),
        ("*Weight", "KG", [121, 176]),
    ]),
]
TAB["tt-tl406"] = [
    table("TL-406", "12 × 16″ wood lathe", ["TL-406"], [
        ("*Swing over bed", "TXT", "12″ (305 mm); 9.5″ (241 mm) over the tool rest base"),
        ("*Between centres", "TXT", "16″ (406 mm)"),
        ("Speeds", "TXT", "6"),
        ("Headstock and tailstock", "TXT", "Spindle nose 1″ × 8 TPI, MT-2 / MT-2; 2-1/2″ (63 mm) ram travel; self-ejecting tailstock"),
        ("Index head", "TXT", "12 positions; spindle lock"),
        ("*Motor", "TXT", "1/2 HP (0.37 kW), 6.6 A"),
        ("Size H × W × D", "TXT", "32 × 10.5 × 19″ (813 × 267 × 483 mm)"),
        ("Packing size L × W × H", "PK", (86, 46, 29)),
        ("*Weight", "KG", 40),
    ]),
]
TAB["tt-mortise"] = [
    table("MS 3-8 · MS 4-8", "Benchtop hollow-chisel mortisers", ["MS 3-8", "MS 4-8"], [
        ("*Chisel and chuck", "TXT", ["3/8″ (10 mm) chuck, 5/8″ (16 mm) collar; chisels 1/4, 5/16, 3/8 and 1/2″ included",
                                      "1/2″ (12.7 mm) chuck, 5/8″ and 3/4″ (16, 19 mm) collars"]),
        ("*Stock, max width × thickness", "TXT", ["8-1/2 × 6″ (216 × 153 mm) with the riser block", "8 × 7-3/8″ (203 × 187 mm)"]),
        ("*Mortise depth, max", "TXT", ["3″ (76 mm)", "4-1/2″ (114 mm)"]),
        ("Chisel travel", "TXT", ["4-5/8″ (118 mm)", "4-3/4″ (120 mm)"]),
        ("Spindle", "TXT", ["JT #2, 1,725 rpm at 60 Hz", "JT #2, 3,450 rpm at 60 Hz"]),
        ("*Motor", "TXT", ["1/2 HP (0.37 kW)", "3/4 HP (0.56 kW)"]),
        ("Packing size L × W × H", "PK", [(35, 74, 82), [("machine", (66, 43, 36)), ("base", (33, 41, 15))]]),
        ("*Weight", "TXT", ["71 lb (32 kg)", "88 lb (40 kg) with the base, shipping weight"]),
    ]),
]
TAB["tt-slotbore"] = [
    table("MGX16 · MGX20R · WM-01", "Slot boring machines and horizontal boring machine", ["MGX16", "MGX20R", "WM-01"], [
        ("*Drill chuck", "TXT", ["5/8″ (16 mm)", "3/4″ (20 mm)", "1/2″ (13 mm)"]),
        ("Table", "TXT", ["21.5 × 10.4″ (545 × 265 mm)", "23.4 × 12.4″ (595 × 316 mm), work table fixed, motor table moves", "8.3 – 14.2″ (210 – 360 mm)"]),
        ("*Travel, cross / longitudinal / vertical", "TXT", ["6.7 / 8.7 / 5.9″ (170 / 220 / 150 mm)", "8.5 / 10.2 / 5.7″ (215 / 260 / 145 mm)", "3.3 / 3.1″ (85 / 80 mm)"]),
        ("Spindle speed", "TXT", ["2,800 rpm", "1,400 / 2,800 rpm", "3,450 rpm at 60 Hz"]),
        ("Head swivel", "TXT", ["—", "±60°", "—"]),
        ("*Motor", "TXT", ["3 HP (2.2 kW)", "2 / 2.5 HP (1.5 / 1.9 kW), two speeds", "1 HP (0.75 kW)"]),
        ("Packing size L × W × H", "PK", [(86, 66, 133), (106, 88, 133), (93, 57, 56)]),
        ("*Weight", "KG", [172, 240, 82]),
    ]),
]
TAB["tt-wood-dust"] = [
    table("WS25-200", "Belt and disc combination sander, 1 × 42″ belt and 8″ disc", ["WS25-200"], [
        ("*Belt", "TXT", "1 × 42″ (25 × 1,067 mm), 3,000 ft/min"),
        ("*Disc", "TXT", "8″ (203 mm), 1,725 rpm at 60 Hz"),
        ("Tables", "TXT", "Cast iron with miter slots, both tilt 0 – 45°: belt 6 × 7″ (153 × 178 mm), disc 4 × 10″ (102 × 254 mm)"),
        ("Dust ports", "TXT", "1-1/2″ (38 mm)"),
        ("*Motor", "TXT", "1/3 HP (0.25 kW)"),
        ("Packing size L × W × H", "PK", (64, 38, 50)),
        ("*Weight", "KG", 26),
    ]),
    table("DC900", "Dust collector for woodworking machines", ["DC900"], [
        ("*Air flow", "TXT", "940 CFM (1,600 m³/h); 4.8″ water (1,200 Pa)"),
        ("Inlets", "TXT", "Two Ø4″ (100 mm) ports; 4″ hose, 8.5 ft (2,600 mm)"),
        ("Bag", "TXT", "11.7 cu ft (0.33 m³) collection bag; 30-micron filter"),
        ("*Motor", "TXT", "1.8 HP (1,350 W)"),
        ("Packing size L × W × H", "PK", (90, 49, 46)),
        ("*Weight", "KG", 49),
    ]),
]
