#!/usr/bin/env python3
"""NovoFab Machinery (value line) band saw families.

Technical data transcribed from the manufacturer's catalogue (metric, as printed),
cross-checked against NovoTech's imperial sawing catalogue (NovoTech_Sawing_Machines_2026.pdf). Model codes are NovoFab's own: NF-<series> <round
capacity in mm at 0°> <variant>:
    M  = manual pivot saw (gravity / hydraulic-damped descent, manual vise)
    H  = hydraulic semi-automatic (hydraulic descent + hydraulic vise, auto cycle)
    A  = automatic (NC / PLC feeding and cutting)
    DC = double column
    S = swivel bow, T = twin-mitre (swivels both ways), C = movable control panel,
    SC = single column, V = variable blade speed, AV = automatic + variable speed.

Writes the families into content/families/bandsaw.json (brand "novofab", line "value").
    python3 tools/novofab_data.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAM = os.path.join(ROOT, "content", "families", "bandsaw.json")


def cap(round_, rect, square=None):
    d = {"round": round_, "rect": rect, "square": square}
    return d


def model(name, caps, motor, speed, band, weight, *, hyd=None, cool=None, wh=None, dims=None, feed=None, other=None, notes=""):
    return {"name": name, "capacity_mm": caps, "main_motor_kw": motor, "hydraulic_motor_kw": hyd,
            "coolant_pump_kw": cool, "blade_speed_m_min": speed, "band_mm": band, "working_height_mm": wh,
            "weight_kg": weight, "dims_mm": dims, "feed_length_mm": feed, "other": other or {}, "notes": notes}


V = "600 V 3-phase (208/240/480 V on request)"
PACK = "Packing size"
GROSS = "Gross weight"

FAMILIES = [
    # ================================================================ MANUAL
    dict(id="novofab-nf-m250", group="manual",
         name="NF-M 250 series manual pivot band saws",
         short="NF-M 250 manual saws",
         models_label="NF-M 250 · NF-M 250 S · NF-M 260 · NF-M 260 T",
         summary="Four 10-inch gravity-feed pivot saws for the maintenance shop and light fabrication. The bow descends on a hydraulic damper with adjustable feed, a four-speed belt drive matches blade speed to the material, and every model ships with a coolant system and a repeat-cut stop rod. Pick the mitre arrangement you need: mitre vise (NF-M 250), swivel bow 45°–90° (NF-M 250 S), larger-capacity frame (NF-M 260) or a twin-mitre bow that swings 60° both ways (NF-M 260 T).",
         features=[
             "Descent controlled by a hydraulic cylinder — adjustable, repeatable feed pressure",
             "Four blade speeds on a belt drive (up to 130 m/min on the NF-M 260 / 260 T)",
             "27 × 0.9 mm bi-metal blade, coolant pump and stop rod included",
             "NF-M 250 S: bow swivels 45°–90° for mitre cuts without moving the stock",
             "NF-M 260 T: bow swivels both ways — 45° left and right, 60° right",
             "2 HP (1.5 kW) three-phase motor; 600 V with CSA-approved panel",
         ],
         optional=["Roller stand with length stop", "Extra blades"],
         images=["nf-m250-1", "nf-m250s-1", "nf-m260-1", "nf-m260t-1"],
         videos=[],
         models=[
             model("NF-M 250", {"0": cap(254, [457, 127]), "+45": cap(150, [190, 150])},
                   1.5, "35/60/88/115", [3280, 27, 0.9], 310,
                   other={"Mitre cutting": "Mitre vise, 45°", "Drive": "V-belt, 4 speeds", PACK: "1820 × 830 × 1160 mm", GROSS: "392 kg"},
                   notes="Angle cuts via the mitre vise (the frame does not swivel)."),
             model("NF-M 250 S", {"0": cap(254, [406, 160]), "+45": cap(170, [190, 160])},
                   1.5, "35/60/88/115", [3215, 27, 0.9], 340,
                   other={"Mitre cutting": "Swivel bow, 45°–90°", "Drive": "V-belt, 4 speeds", PACK: "1820 × 780 × 1340 mm", GROSS: "440 kg"}),
             model("NF-M 260", {"0": cap(260, [460, 125], 260), "+45": cap(230, [230, 220], 220)},
                   1.5, "28/62/93/130", [3660, 27, 0.9], 320,
                   other={"Mitre cutting": "Swivel bow, 45°", "Drive": "Belt, 4 speeds", PACK: "2130 × 870 × 1250 mm", GROSS: "440 kg"}),
             model("NF-M 260 T", {"0": cap(260, [430, 260]), "+45": cap(260, [300, 200]), "+60": cap(155, [125, 125]), "-45": cap(260, [260, 130])},
                   1.5, "28/62/93/130", [3660, 27, 0.9], 466,
                   other={"Mitre cutting": "Swivel bow, 45° left / 45° and 60° right", "Drive": "Belt, 4 speeds", PACK: "2120 × 1080 × 1220 mm", GROSS: "520 kg"}),
         ]),
    dict(id="novofab-nf-m400", group="manual",
         name="NF-M 400 manual band saw, Ø400 mm",
         short="NF-M 400",
         models_label="NF-M 400",
         summary="A big 15¾-inch pivot saw with a gear-driven two-speed motor and sintered-carbide blade guides, for shops that cut heavy sections but do not need an automatic cycle. The bow swivels for mitre cuts up to 60°, the sliding vise has a quick clamp for fast workpiece changes, and the heavy welded base keeps the cut square on 550 × 360 mm stock.",
         features=[
             "Ø400 mm round / 550 × 360 mm rectangular at 0°; mitre cuts up to 60°",
             "Gear-driven two-speed motor, 2.2/2.8 kW — no belts to tension",
             "Blade guides with sintered-carbide inserts for straight cuts in series production",
             "Sliding vise with quick clamp; powerful coolant pump",
             "34 × 1.1 × 4405 mm blade",
         ],
         optional=["Roller stand with length stop", "Hydraulic version — see NF-H 400"],
         images=["nf-m400-1"],
         videos=[],
         models=[
             model("NF-M 400", {"0": cap(400, [550, 360]), "+45": cap(340, [400, 340]), "+60": cap(150, [250, 200])},
                   "2.2-2.8", "48/70", [4405, 34, 1.1], 580,
                   other={"Drive": "Gear, 2 speeds", PACK: "2300 × 830 × 1580 mm", GROSS: "710 kg"}),
         ]),
    # ================================================================ SEMI-AUTOMATIC
    dict(id="novofab-nf-h250", group="semi-automatic",
         name="NF-H 250 series hydraulic band saws",
         short="NF-H 250 hydraulic saws",
         models_label="NF-H 250 S · NF-H 260 T",
         summary="The hydraulic versions of the 10-inch pivot saws: a hydraulic cylinder lowers the bow at a dialled-in rate, the bow lifts automatically at the end of the cut and the machine shuts off — the operator only loads, clamps and starts. The NF-H 250 S adds a hydraulic clamping vise and a swivel bow for 45° mitres; the NF-H 260 T swings both ways for 45°/60° cuts and comes with a movable control panel.",
         features=[
             "Hydraulic descent with variable feed speed; automatic bow return and shut-off",
             "NF-H 250 S: hydraulic clamping vise, swivel bow 45°–90°, manual or auto-cut cycle",
             "NF-H 260 T: twin-mitre bow (45° left, 45°/60° right), quick-clamp vise, movable control panel",
             "Four-speed belt drive, 2 HP (1.5 kW) three-phase motor",
             "Coolant system and stop rod included",
         ],
         optional=["Roller stand with length stop"],
         images=["nf-h250s-1", "nf-h260t-1"],
         videos=[],
         models=[
             model("NF-H 250 S", {"0": cap(254, [406, 160]), "+45": cap(170, [190, 160])},
                   1.5, "35/60/88/115", [3215, 27, 0.9], 420,
                   other={"Mitre cutting": "Swivel bow, 45°–90°", "Vise": "Hydraulic", "Drive": "V-belt, 4 speeds", PACK: "1890 × 780 × 1430 mm", GROSS: "533 kg"}),
             model("NF-H 260 T", {"0": cap(260, [430, 260]), "+45": cap(260, [300, 200]), "+60": cap(155, [125, 125]), "-45": cap(260, [260, 130])},
                   1.5, "28/62/93/130", [3660, 27, 0.9], 515,
                   other={"Mitre cutting": "Swivel bow, 45° left / 45° and 60° right", "Vise": "Quick-clamp, manual", "Drive": "Belt, 4 speeds", PACK: "2120 × 1310 × 1220 mm", GROSS: "653 kg"}),
         ]),
    dict(id="novofab-nf-h330", group="semi-automatic",
         name="NF-H 330 twin-mitre hydraulic band saws",
         short="NF-H 330 saws",
         models_label="NF-H 330 · NF-H 330 C",
         summary="A 13-inch gear-driven semi-automatic saw whose bow swivels both ways — 45° left and right, 60° right — with a quick lock at every angle. Hydraulic vise, hydraulic descent and a two-speed gear motor make it the workhorse for structural steel, tube and profile cutting. The NF-H 330 C is the same machine with a movable control panel on an arm. PLC control and servo feed can be added to turn it into an automatic.",
         features=[
             "Ø330 mm round / 460 × 250 mm at 0°; Ø305 mm at 45° both sides, Ø205 mm at 60°",
             "Hydraulic clamping vise and hydraulic bow descent",
             "Bow swivels left and right with quick lock",
             "Gear drive, two-speed 1.5/2.2 kW motor (48/96 m/min at 60 Hz)",
             "NF-H 330 C: movable control panel",
         ],
         optional=["PLC control", "Servo motor (variable blade speed)", "Roller stands"],
         images=["nf-h330-1", "nf-h330c-1"],
         videos=[],
         models=[
             model("NF-H 330", {"0": cap(330, [460, 250]), "+45": cap(305, [305, 250]), "-45": cap(305, [305, 250]), "+60": cap(205, [205, 250])},
                   "1.5-2.2", "48/96", [3960, 27, 0.9], 900,
                   other={"Vise": "Hydraulic", "Drive": "Gear, 2 speeds", PACK: "2300 × 1050 × 1630 mm", GROSS: "1060 kg"}),
             model("NF-H 330 C", {"0": cap(330, [460, 250]), "+45": cap(305, [305, 250]), "-45": cap(305, [305, 250]), "+60": cap(205, [205, 250])},
                   "1.5-2.2", "48/96", [3960, 27, 0.9], 900,
                   other={"Vise": "Hydraulic", "Drive": "Gear, 2 speeds", "Control panel": "Movable, on arm", PACK: "2300 × 1050 × 1630 mm", GROSS: "1060 kg"}),
         ]),
    dict(id="novofab-nf-h400", group="semi-automatic",
         name="NF-H 400 hydraulic band saw, Ø400 mm",
         short="NF-H 400",
         models_label="NF-H 400",
         summary="The hydraulic version of the NF-M 400: the saw frame descends and rises automatically, so one operator can clamp, start and walk away. Gear-driven two-speed motor, sintered-carbide guides, quick-clamp sliding vise and mitre cuts up to 60° on stock up to 550 × 360 mm.",
         features=[
             "Ø400 mm round / 550 × 360 mm rectangular at 0°; mitre cuts up to 60°",
             "Automatic bow descent and return on a hydraulic cylinder",
             "Gear-driven two-speed motor, 2.2/2.8 kW",
             "Sintered-carbide blade guides, quick-clamp sliding vise",
             "Powerful coolant pump; 34 × 1.1 × 4405 mm blade",
         ],
         optional=["Roller stand with length stop"],
         images=["nf-h400-1"],
         videos=[],
         models=[
             model("NF-H 400", {"0": cap(400, [550, 360]), "+45": cap(340, [400, 340]), "+60": cap(150, [250, 200])},
                   "2.2-2.8", "48/70", [4405, 34, 1.1], 630,
                   other={"Drive": "Gear, 2 speeds", PACK: "2300 × 830 × 1580 mm", GROSS: "760 kg"}),
         ]),
    dict(id="novofab-nf-h300sc", group="semi-automatic",
         name="NF-H 300 SC single-column band saw with touch screen",
         short="NF-H 300 SC",
         models_label="NF-H 300 SC",
         summary="A single-column saw for straight cuts up to Ø300 mm / 500 × 300 mm with a PLC and finger-touch screen, hydraulic jaw vise, variable hydraulic down-feed and blade overload protection. The column guides the bow vertically for square, repeatable cuts; bearing and carbide double guides extend blade life. Ideal as a production saw for bar and plate where a feeder is not needed — its automatic sister is the NF-A 300 SC.",
         features=[
             "Ø300 mm round / 500 × 300 mm rectangular (straight cut)",
             "PLC control with graphical finger-touch screen; work light",
             "Hydraulic jaw clamping vise, variable hydraulic down-feed",
             "Blade overload protection; bearing + carbide double guides",
             "Four blade speeds, 3 kW motor, 34 × 1.1 × 4180 mm blade",
         ],
         optional=["Roller stands", "Automatic feeding — see NF-A 300 SC"],
         images=["nf-h300sc-1", "nf-h300sc-2", "nf-h300sc-3", "nf-h300sc-4"],
         videos=[],
         models=[
             model("NF-H 300 SC", {"0": cap(300, [500, 300])},
                   3.0, "30/50/75/90", [4180, 34, 1.1], 1085,
                   other={"Vise": "Hydraulic jaw", "Control": "PLC, touch screen", "Max. hydraulic pressure": "2.2 MPa", "Drive": "V-belt, 4 speeds", PACK: "2270 × 1320 × 1710 mm", GROSS: "1175 kg"}),
         ]),
    dict(id="novofab-nf-h460", group="semi-automatic",
         name="NF-H 460 hydraulic band saw, Ø460 mm",
         short="NF-H 460",
         models_label="NF-H 460",
         summary="An 18-inch swivel-head saw with automatic cutting and manual feeding: hydraulic vise, variable-frequency drive for stepless blade speed, a digital read-out for the feed position and a movable control panel. The bow swivels 45° to both sides and 60° to the right, and the gear-driven 5.5 kW motor handles 650 × 350 mm sections. Same frame as the automatic NF-A 460 without the feeder.",
         features=[
             "Ø460 mm round / 650 × 350 mm at 0°; Ø460 mm at 45° both sides, Ø310 mm at 60°",
             "Automatic cutting cycle; material fed by hand on the roller table",
             "Hydraulic clamping vise, digital read-out of the feed position",
             "Variable blade speed 0–95 m/min (inverter); 5.5 kW gear-driven motor",
             "Movable control panel; 41 × 1.3 × 5220 mm blade",
         ],
         optional=["Roller conveyors", "Automatic feeding — see NF-A 460"],
         images=["nf-h460-1", "nf-h460-2"],
         videos=[],
         models=[
             model("NF-H 460", {"0": cap(460, [650, 350]), "+45": cap(460, [460, 350]), "-45": cap(460, [460, 350]), "+60": cap(310, [310, 350])},
                   5.5, "0-95", [5220, 41, 1.3], 1640,
                   other={"Vise": "Hydraulic", "Drive": "Gear, inverter", "Control panel": "Movable", PACK: "2950 × 1480 × 2120 mm", GROSS: "1880 kg"}),
         ]),
    # ================================================================ AUTOMATIC
    dict(id="novofab-nf-a300", group="automatic",
         name="NF-A 300 automatic band saws with roller feed",
         short="NF-A 300 automatic saws",
         models_label="NF-A 300 · NF-A 300 T",
         summary="Compact automatic saws for batch cutting of bar, tube and profile up to Ø300 mm: a powered roller feed advances the stock, the hydraulic vise clamps, the bow cuts and returns, and the cycle repeats for the programmed count. Stepless blade speed from an inverter, gear drive and a 3 HP motor. The NF-A 300 T adds an automatic mitre head for angle cuts of 30°, 45° and 60°.",
         features=[
             "Ø300 mm round / 370 × 280 mm rectangular at 0°",
             "Roller feeding with automatic cycle; piece counter",
             "Hydraulic clamping vise; inverter-driven blade speed 0–113 m/min",
             "Gear drive, 2.2 kW main motor, 0.25 kW feed motor",
             "NF-A 300 T: mitre cutting 0°–60° (Ø280 mm at 30°, Ø230 mm at 45°, Ø130 mm at 60°)",
         ],
         optional=["Roller conveyors", "Extra blades"],
         images=["nf-a300-1", "nf-a300-2", "nf-a300-3", "nf-a300t-1", "nf-a300t-2"],
         videos=[],
         models=[
             model("NF-A 300", {"0": cap(300, [370, 280])},
                   2.2, "0-113", [3820, 27, 0.9], 800, wh=730,
                   other={"Feed motor": "0.25 kW", "Feeding": "Roller feed, automatic cycle", "Vise": "Hydraulic", "Drive": "Gear, inverter", PACK: "2140 × 1320 × 1500 mm", GROSS: "950 kg"}),
             model("NF-A 300 T", {"0": cap(300, [370, 280]), "+30": cap(280, [280, 280]), "+45": cap(230, [230, 250]), "+60": cap(130, [130, 150])},
                   2.2, "0-113", [3820, 27, 0.9], 940, wh=730,
                   other={"Feed motor": "0.25 kW", "Feeding": "Roller feed, automatic cycle", "Vise": "Hydraulic", "Drive": "Gear, inverter", PACK: "2140 × 1320 × 1500 mm", GROSS: "1090 kg"}),
         ]),
    dict(id="novofab-nf-a300sc", group="automatic",
         name="NF-A 300 SC single-column automatic band saw",
         short="NF-A 300 SC",
         models_label="NF-A 300 SC",
         summary="The automatic version of the single-column saw: a hydraulic shuttle vise feeds up to 500 mm per stroke, a batch clamping device holds bundles, and an automatic chip conveyor clears the swarf. PLC control with touch screen, hydraulic jaw vise, variable hydraulic down-feed, rapid descent until the blade touches the work and blade overload protection.",
         features=[
             "Ø300 mm round / 500 × 300 mm rectangular (straight cut)",
             "Hydraulic shuttle-vise feeding, up to 500 mm per stroke; batch clamping device",
             "PLC with finger-touch screen; rapid approach, then controlled feed",
             "Automatic chip conveyor, work light, coolant system",
             "Four blade speeds, 3 kW motor, 34 × 1.1 × 4180 mm blade",
         ],
         optional=["Roller conveyors"],
         images=["nf-a300sc-1", "nf-a300sc-2", "nf-a300sc-3", "nf-a300sc-4"],
         videos=[],
         models=[
             model("NF-A 300 SC", {"0": cap(300, [500, 300])},
                   3.0, "30/50/75/90", [4180, 34, 1.1], 1550,
                   other={"Feeding": "Hydraulic shuttle vise", "Feed length per stroke": "500 mm", "Vise": "Hydraulic jaw", "Control": "PLC, touch screen", "Max. hydraulic pressure": "2.5 MPa", "Drive": "V-belt, 4 speeds", PACK: "2260 × 2130 × 1780 mm", GROSS: "1720 kg"}),
         ]),
    dict(id="novofab-nf-a330", group="automatic",
         name="NF-A 330 automatic twin-mitre band saw with 6 m stand",
         short="NF-A 330",
         models_label="NF-A 330",
         summary="The automatic version of the NF-H 330: PLC-controlled feeding and clamping with a shuttle vise (500 mm per stroke), feed length selectable in metric or inch, and a 6 m material stand (3 m feed, 3 m return) delivered with the machine. The bow still swivels to both sides for mitre cuts, and a guard net protects the operator. Gear drive with a two-speed motor; blade 34 × 1.1 × 3960 mm.",
         features=[
             "Ø330 mm round / 460 × 250 mm at 0°; Ø305 mm at 45° both sides, Ø205 mm at 60°",
             "Automatic feeding and clamping, max. 500 mm per stroke; standard PLC",
             "6 m material stand included (feeder width 460 mm, height 850 mm)",
             "Bow swivels left and right; safety guard net",
             "Gear drive, 1.5/2.2 kW two-speed motor",
         ],
         optional=["Extra stands and supports", "Servo motor (variable blade speed)"],
         images=["nf-a330-1", "nf-a330-2", "nf-a330-3"],
         videos=[],
         models=[
             model("NF-A 330", {"0": cap(330, [460, 250]), "+45": cap(305, [305, 250]), "-45": cap(305, [305, 250]), "+60": cap(205, [205, 250])},
                   "1.5-2.2", "48/96", [3960, 34, 1.1], 1520,
                   other={"Feeding": "Shuttle vise, PLC", "Feed length per stroke": "500 mm", "Vise": "Hydraulic", "Drive": "Gear, 2 speeds", PACK: "2500 × 2300 × 1630 mm", GROSS: "1655 kg"}),
         ]),
    dict(id="novofab-nf-a-cnc", group="automatic",
         name="NF-A 350–600 CNC automatic band saws",
         short="NF-A CNC saws",
         models_label="NF-A 350 · NF-A 415 · NF-A 460 · NF-A 600",
         summary="Production saws with CNC feeding and cutting: a servo-driven feeder positions the stock, hydraulic vises clamp it, the servo blade drive sets a stepless cutting speed and the PLC runs the batch. The NF-A 350 and NF-A 415 have an automatic rotary bow (45°) and chip extraction; the NF-A 460 feeds up to 650 mm per stroke with a linear scale on the feed and a swivelling control panel; the NF-A 600 cuts 850 × 600 mm sections with a hydraulic feeder as standard.",
         features=[
             "Round capacity from Ø350 mm to Ø600 mm; mitre cuts to 45° (NF-A 460: 60°)",
             "CNC / PLC automatic feeding and clamping, hydraulic vises",
             "Servo motor for stepless blade speed; industrial gearbox (NF-A 460)",
             "Feed per stroke: 500 mm (NF-A 350/415), 650 mm (NF-A 460), 600 mm (NF-A 600)",
             "Work light, chip extraction and coolant system included",
         ],
         optional=["Material supports and roller conveyors"],
         images=["nf-a350-1", "nf-a460-1", "nf-a460-2", "nf-a600-1"],
         videos=[],
         models=[
             model("NF-A 350", {"0": cap(350, [500, 350]), "+45": cap(330, [330, 350])},
                   3.7, None, [4180, 34, 1.1], 2700,
                   other={"Blade drive": "Servo motor, stepless speed", "Feeding": "CNC, hydraulic clamping", "Feed length per stroke": "500 mm", "Bow swivel": "Automatic, to 45°", PACK: "2230 × 2220 × 1700 mm", GROSS: "2900 kg"}),
             model("NF-A 415", {"0": cap(415, [500, 415]), "+45": cap(335, [265, 415])},
                   3.7, None, [4555, 34, 1.1], 2780,
                   other={"Blade drive": "Servo motor, stepless speed", "Feeding": "CNC, hydraulic clamping", "Feed length per stroke": "500 mm", "Bow swivel": "Automatic, to 45°", PACK: "2250 × 2350 × 1750 mm", GROSS: "3000 kg"}),
             model("NF-A 460", {"0": cap(460, [650, 350]), "+45": cap(460, [460, 350]), "+60": cap(310, [310, 350])},
                   5.5, "23-95", [5220, 41, 1.3], 2430,
                   other={"Blade drive": "Servo motor + industrial gearbox", "Feeding": "NC, automatic clamping", "Feed length per stroke": "650 mm", "Bow swivel": "Automatic, to 60° right", PACK: "3030 × 2280 × 2220 mm", GROSS: "2730 kg"}),
             model("NF-A 600", {"0": cap(600, [850, 600]), "+45": cap(400, [400, 600])},
                   5.5, "0-119", [6685, 54, 1.6], 3945,
                   other={"Blade drive": "Servo motor, stepless speed", "Feeding": "Hydraulic feeder, CNC", "Feed length per stroke": "600 mm", "Bow swivel": "To 45°", PACK: "3550 × 2120 × 2660 mm (body), 1790 × 1720 × 1490 mm (feeder)", GROSS: "4235 kg"}),
         ]),
    # ================================================================ DOUBLE COLUMN
    dict(id="novofab-nf-dc280", group="double-column",
         name="NF-DC 280 series double column band saws",
         short="NF-DC 280 saws",
         models_label="NF-DC 280 · NF-DC 280 T · NF-DC 280 A · NF-DC 280 AV",
         summary="Twin-column saws for Ø280 mm / 280 × 280 mm stock: the bow travels vertically on two columns, so the cut stays square whatever the feed pressure. Hydraulic down-feed with variable speed, hydraulic clamping and automatic shut-off on every model. Choose the base machine with hand-wheel feed (NF-DC 280), the mitre version that cuts at 30° and 45° (NF-DC 280 T), the automatic with a 3-position shuttle vise (NF-DC 280 A) or the automatic with stepless blade speed, chip conveyor and the new vise design (NF-DC 280 AV).",
         features=[
             "Ø280 mm round / 280 × 280 mm square; NF-DC 280 T: Ø260 mm at 30°, Ø170 mm at 45°",
             "Double column — vertical, rigid bow travel",
             "Hydraulic variable down-feed, hydraulic clamping, auto shut-off",
             "NF-DC 280 A / AV: automatic feed and cut, 3-position vise for bundle cutting, feed length by limit switch",
             "NF-DC 280 AV: variable blade speed 0–61 m/min, automatic chip conveyor",
             "Belt drive, 3 kW motor; work light, coolant and material stand included",
         ],
         optional=["Roller stand", "Extra blades"],
         images=["nf-dc280-1", "nf-dc280t-1", "nf-dc280t-2", "nf-dc280t-3", "nf-dc280a-1", "nf-dc280av-1", "nf-dc280av-2", "nf-dc280av-3", "nf-dc280av-4", "nf-dc280-stand"],
         videos=[],
         models=[
             model("NF-DC 280", {"0": cap(280, [280, 280], 280)},
                   3.0, "27/45/69", [3505, 27, 0.9], 695, hyd=0.55, dims=[2180, 1310, 1610],
                   other={"Feeding": "Manual hand wheel", "Vise": "Hydraulic", "Blade tensioning": "Mechanical", "Drive": "V-belt, 3 speeds", GROSS: "834 kg"}),
             model("NF-DC 280 T", {"0": cap(280, [280, 280], 280), "+30": cap(260, [260, 280]), "+45": cap(170, [170, 280])},
                   3.0, "27/45/69", [3625, 27, 0.9], 820, hyd=0.55, dims=[2180, 1300, 1600],
                   other={"Feeding": "Manual", "Mitre cutting": "0°–45°", "Vise": "Hydraulic", "Blade tensioning": "Mechanical", "Drive": "V-belt, 3 speeds", GROSS: "965 kg"}),
             model("NF-DC 280 A", {"0": cap(280, [280, 280], 280)},
                   3.0, "27/45/69", [3505, 27, 0.9], 990, hyd=0.55, dims=[2250, 2010, 1640],
                   other={"Feeding": "Automatic, 3-position shuttle vise", "Vise": "Hydraulic", "Blade tensioning": "Mechanical", "Drive": "V-belt, 3 speeds", GROSS: "1160 kg"}),
             model("NF-DC 280 AV", {"0": cap(280, [280, 280], 280)},
                   3.0, "0-61", [3505, 27, 0.9], 990, hyd=0.55, dims=[2250, 2010, 1640],
                   other={"Feeding": "Automatic, shuttle vise", "Vise": "Hydraulic, new clamp design", "Blade tensioning": "Mechanical", "Drive": "V-belt, inverter", "Chip conveyor": "Automatic", GROSS: "1160 kg"}),
         ]),
    dict(id="novofab-nf-dc350", group="double-column",
         name="NF-DC 350 and NF-DC 400 gear-driven double column saws",
         short="NF-DC 350 / 400",
         models_label="NF-DC 350 · NF-DC 400",
         summary="Heavier twin-column saws with a gear-driven two-speed motor, hydraulic blade tensioning and hydraulic clamping. Vertical lifting on two columns keeps the blade square in Ø350 mm and Ø400 mm solids; the cutting feed is hydraulically controlled and stepless. A three-position hydraulic clamping vise for bundles is optional.",
         features=[
             "NF-DC 350: Ø350 mm / 350 × 350 mm · NF-DC 400: Ø400 mm / 400 × 400 mm",
             "Double column structure, vertical lifting, high stability",
             "Hydraulic variable down-feed, hydraulic clamping, hydraulic blade tensioning",
             "Gear drive with two-speed motor (2.2/2.8 kW or 3.0/4.0 kW)",
             "Work light, coolant pump and material stand included",
         ],
         optional=["Three-position hydraulic clamping vise", "Roller stands"],
         images=["nf-dc350-1", "nf-dc350-2", "nf-dc350-3"],
         videos=[],
         models=[
             model("NF-DC 350", {"0": cap(350, [350, 350], 350)},
                   "2.2-2.8", "45/69", [4115, 34, 1.1], 880, hyd=0.55, cool=0.04, dims=[2410, 1150, 1500],
                   other={"Vise": "Hydraulic", "Blade tensioning": "Hydraulic", "Drive": "Gear, 2 speeds", GROSS: "990 kg"}),
             model("NF-DC 400", {"0": cap(400, [400, 400], 400)},
                   "3.0-4.0", "36/56", [5000, 41, 1.3], 1325, hyd=0.75, cool=0.9, dims=[2700, 1350, 2150],
                   other={"Vise": "Hydraulic", "Blade tensioning": "Hydraulic", "Drive": "Gear, 2 speeds", GROSS: "1585 kg"}),
         ]),
    dict(id="novofab-nf-dc500", group="double-column",
         name="NF-DC 500 and NF-DC 600 gantry double column saws",
         short="NF-DC 500 / 600",
         models_label="NF-DC 500 · NF-DC 600",
         summary="Gantry-type double column saws for heavy plate, blocks, bundles and large tube: Ø500 mm / 700 × 500 mm on the NF-DC 500 and Ø600 mm / 1200 × 600 mm on the NF-DC 600. Hydraulic clamping, stepless blade speed and a powered roller table; the NF-DC 600 adds hydraulic blade tensioning and an 11 kW motor for the 67 mm blade.",
         features=[
             "NF-DC 500: Ø500 mm / 700 × 500 mm · NF-DC 600: Ø600 mm / 1200 × 600 mm",
             "Double column gantry structure for batch sawing of tubes, bars, profiles and plates",
             "Hydraulic clamping; variable blade speed (40–80 and 20–80 m/min)",
             "NF-DC 500: 5.5 kW, 41 × 1.3 mm blade · NF-DC 600: 11 kW, 67 × 1.3 × 8800 mm blade, hydraulic tensioning",
             "Powered roller table with chain drive",
         ],
         optional=["Roller conveyors", "Bundle clamping"],
         images=["nf-dc500-1", "nf-dc600-1", "nf-dc600-2"],
         videos=[],
         models=[
             model("NF-DC 500", {"0": cap(500, [700, 500])},
                   5.5, "40-80", [None, 41, 1.3], 2590, hyd=1.5, cool=0.09,
                   other={"Vise": "Hydraulic", "Blade tensioning": "Manual", "Drive": "Belt", PACK: "3550 × 1500 × 2180 mm", GROSS: "2960 kg"},
                   notes="Blade length not printed in the catalogue."),
             model("NF-DC 600", {"0": cap(600, [1200, 600])},
                   11.0, "20-80", [8800, 67, 1.3], 5060, hyd=2.2, cool=0.12,
                   other={"Vise": "Hydraulic", "Blade tensioning": "Hydraulic", PACK: "4250 × 1750 × 2370 mm", GROSS: "5320 kg"}),
         ]),
]


def main():
    data = json.load(open(FAM, encoding="utf-8"))
    fams = data["families"]
    order = [k for k in data["order"] if not k.startswith("novofab-")]
    for f in FAMILIES:
        rec = {
            "id": f["id"], "brand": "novofab", "line": "value", "group": f["group"],
            "name": f["name"], "short": f["short"], "models_label": f["models_label"],
            "summary": f["summary"], "features": f["features"], "optional": f["optional"],
            "images": f["images"], "videos": f["videos"],
            "specs": {"kind": "bandsaw", "voltage": V, "models": f["models"]},
        }
        fams[f["id"]] = rec
        order.append(f["id"])
    data["order"] = order
    json.dump(data, open(FAM, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("families:", len(fams), "novofab:", len(FAMILIES))


if __name__ == "__main__":
    main()
