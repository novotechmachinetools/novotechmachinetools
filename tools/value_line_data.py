#!/usr/bin/env python3
"""NovoTech value line band saw families (manufacturer's original model codes).

Technical data transcribed from the manufacturer's catalogue (metric, as printed),
cross-checked against NovoTech's imperial sawing catalogue. Model codes are the manufacturer's
original codes (BS-… pivot and single-column saws, TBK-/TGK- double column, GZ gantry saws); the
image keys (nt-…) are internal file names only.

Writes the families into content/families/bandsaw.json (brand "novotech", line "value").
    python3 tools/value_line_data.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAM = os.path.join(ROOT, "content", "families", "bandsaw.json")


def cap(round_, rect, square=None):
    return {"round": round_, "rect": rect, "square": square}


def model(name, caps, motor, speed, band, weight, *, hyd=None, cool=None, wh=None, dims=None, feed=None, other=None, notes=""):
    return {"name": name, "capacity_mm": caps, "main_motor_kw": motor, "hydraulic_motor_kw": hyd,
            "coolant_pump_kw": cool, "blade_speed_m_min": speed, "band_mm": band, "working_height_mm": wh,
            "weight_kg": weight, "dims_mm": dims, "feed_length_mm": feed, "other": other or {}, "notes": notes}


V = "600 V 3-phase (208/240/480 V on request)"
PACK = "Packing size"
GROSS = "Gross weight"

FAMILIES = [
    # ================================================================ MANUAL
    # ================================================================ SEMI-AUTOMATIC
    dict(id="novotech-bs-315gf", group="semi-automatic",
         voltage="240 V single-phase",          # the only supply this model is built for — no 3-phase or other-voltage option
         name="BS-315GF full-hydraulic double-miter band saw, 10″",
         short="BS-315GF",
         models_label="BS-315GF",
         summary="Our most popular value-line saw: a 10-inch gear-driven semi-automatic with everything hydraulic — the vise clamps hydraulically, the bow descends on a hydraulic cylinder at a dialled-in feed rate and lifts itself hydraulically at the end of the cut. The bow swivels to both sides for 30°, 45° and 60° miters with fast angle stops, the gear-driven motor runs the band at a variable blade speed set on the VFD inverter drive. One operator loads, clamps and starts; the saw does the rest.",
         features=[
             "Ø9-7/8″ (250 mm) round / 12-1/2″ × 7-1/2″ at 0°; Ø9″ at 45° both sides, Ø5-7/8″ at 60°",
             "Hydraulic clamping vise, hydraulic down-feed with variable feed rate and hydraulic bow up-lift",
             "Swivels left and right with fast angle stops at 30°, 45° and 60°",
             "Gear-driven 1.5 HP (1.1 kW) blade motor with variable blade speed by VFD inverter drive, up to 262 ft/min (80 m/min), and a separate 1 HP (0.75 kW) motor for the hydraulic pump",
             "Bow pivots on adjustable tapered bearings — no backlash; electro-mechanical blade tensioner with microswitch",
             "Safety guards on the flywheel casing and blade; electric coolant system; 1″ × .035″ × 111″ (27 × 0.9 × 2825 mm) blade",
         ],
         optional=["Roller stand with length stop", "Extra blades"],
         images=["nt-bs315gf-1", "nt-bs315gf-2", "nt-bs315gf-3", "nt-bs315gf-4", "nt-bs315gf-d7", "nt-bs315gf-d1", "nt-bs315gf-d9", "nt-bs315gf-d8", "nt-bs315gf-d3",
                 "nt-bs315gf-d4", "nt-bs315gf-d6", "nt-bs315gf-d5", "nt-bs315gf-d2", "nt-bs315gf-d10"],
         videos=[
             {"id": "yylLY38qVrM", "title": "BS-315GF 10″ semi-automatic swivel band saw with hydraulic up-lift and down-feed — miter cuts both sides", "thumb": "video-yylLY38qVrM", "duration": "PT1M15S", "upload_date": "2026-10-07"},
             {"id": "iwCyiXP3JRg", "title": "BS-315GF 10″ semi-automatic double-miter band saw with inverter drive, hydraulic up-lift and hydraulic vise", "thumb": "video-iwCyiXP3JRg", "duration": "PT3M1S", "upload_date": "2026-09-02"},
             {"id": "obbCib0YB24", "title": "BS-315GF 10″ double-miter semi-automatic band saw with hydraulic vise", "thumb": "video-obbCib0YB24", "duration": "PT1M1S"},
         ],
         models=[
             model("BS-315GF", {"0": cap(250, [315, 190]), "+45": cap(230, [210, 190]), "-45": cap(230, [210, 190]), "+60": cap(150, [130, 150])},
                   "1.1", "Variable, VFD inverter drive — up to 262 ft/min (80 m/min)", [2825, 27, 0.9], 400, hyd=0.75,
                   other={"Vise": "Hydraulic", "Bow lift": "Hydraulic", "Miter cutting": "Swivel bow, 45° left / 30°, 45° and 60° right", "Drive": "Gear, variable blade speed by VFD inverter drive", PACK: "1630 × 900 × 1550 mm", GROSS: "515 kg"}),
         ]),
    dict(id="novotech-bs-460g", group="semi-automatic",
         name="BS-460G dual-miter hydraulic band saws, 13″",
         short="BS-460G saws",
         models_label="BS-460G · BS-460G-JC",
         summary="A 13-inch gear-driven semi-automatic saw whose bow swivels both ways — 45° left and right, 60° right — with a quick lock at every angle. Hydraulic vise, hydraulic descent and a gear-driven motor with variable blade speed by VFD inverter drive make it the workhorse for structural steel, tube and profile cutting. The BS-460G-JC is the same machine with a movable control panel on an arm. PLC control and servo feed can be added to turn it into an automatic.",
         features=[
             "Ø13″ (330 mm) round / 18″ × 9-7/8″ at 0°; Ø12″ at 45° both sides, Ø8″ at 60°",
             "Hydraulic clamping vise and hydraulic bow descent",
             "Bow swivels left and right with quick lock",
             "Gear drive, 2/3 HP (1.5/2.2 kW) motor — variable blade speed by VFD inverter drive, up to 315 ft/min (96 m/min)",
             "BS-460G-JC: movable control panel",
         ],
         optional=["PLC control", "Roller stands"],
         images=["nt-h13-1", "nt-h13c-1"],
         videos=[],
         models=[
             model("BS-460G", {"0": cap(330, [460, 250]), "+45": cap(305, [305, 250]), "-45": cap(305, [305, 250]), "+60": cap(205, [205, 250])},
                   "1.5-2.2", "Variable, VFD inverter drive — up to 315 ft/min (96 m/min)", [3960, 27, 0.9], 900,
                   other={"Vise": "Hydraulic", "Drive": "Gear, variable blade speed by VFD inverter drive", PACK: "2300 × 1050 × 1630 mm", GROSS: "1060 kg"}),
             model("BS-460G-JC", {"0": cap(330, [460, 250]), "+45": cap(305, [305, 250]), "-45": cap(305, [305, 250]), "+60": cap(205, [205, 250])},
                   "1.5-2.2", "Variable, VFD inverter drive — up to 315 ft/min (96 m/min)", [3960, 27, 0.9], 900,
                   other={"Vise": "Hydraulic", "Drive": "Gear, variable blade speed by VFD inverter drive", "Control panel": "Movable, on arm", PACK: "2300 × 1050 × 1630 mm", GROSS: "1060 kg"}),
         ]),
    dict(id="novotech-bs-2114th", group="semi-automatic",
         name="BS-2114TH hydraulic band saw, 15-3/4″",
         short="BS-2114TH",
         models_label="BS-2114TH",
         summary="A 15-3/4-inch pivot saw with hydraulic descent and return: the saw frame descends and rises automatically, so one operator can clamp, start and walk away. Gear-driven motor with variable blade speed by VFD inverter drive, sintered-carbide guides, quick-clamp sliding vise and miter cuts up to 60° on stock up to 21-3/4″ × 14-1/4″.",
         features=[
             "Ø15-3/4″ (400 mm) round / 21-3/4″ × 14-1/4″ rectangular at 0°; miter cuts up to 60°",
             "Automatic bow descent and return on a hydraulic cylinder",
             "Gear-driven 3/3.8 HP (2.2/2.8 kW) motor — variable blade speed by VFD inverter drive, up to 230 ft/min (70 m/min)",
             "Sintered-carbide blade guides, quick-clamp sliding vise",
             "Powerful coolant pump; 1-3/8″ × 0.043″ × 173-1/2″ blade",
         ],
         optional=["Roller stand with length stop"],
         images=["nt-h16-1"],
         videos=[],
         models=[
             model("BS-2114TH", {"0": cap(400, [550, 360]), "+45": cap(340, [400, 340]), "+60": cap(150, [250, 200])},
                   "2.2-2.8", "Variable, VFD inverter drive — up to 230 ft/min (70 m/min)", [4405, 34, 1.1], 630,
                   other={"Drive": "Gear, variable blade speed by VFD inverter drive", PACK: "2300 × 830 × 1580 mm", GROSS: "760 kg"}),
         ]),
    dict(id="novotech-bs-5030", group="semi-automatic",
         name="BS-5030 single-column band saw with touch screen",
         short="BS-5030",
         models_label="BS-5030",
         summary="A single-column saw for straight cuts up to Ø11-3/4″ / 19-3/4″ × 11-3/4″ with a PLC and finger-touch screen, hydraulic jaw vise, variable hydraulic down-feed and blade overload protection. The column guides the bow vertically for square, repeatable cuts; bearing and carbide double guides extend blade life. Ideal as a production saw for bar and plate where a feeder is not needed — its automatic sister is the BS-5040.",
         features=[
             "Ø11-3/4″ (300 mm) round / 19-3/4″ × 11-3/4″ rectangular (straight cut)",
             "PLC control with graphical finger-touch screen; work light",
             "Hydraulic jaw clamping vise, variable hydraulic down-feed",
             "Blade overload protection; bearing + carbide double guides",
             "Four blade speeds, 4 HP (3 kW) motor, 1-3/8″ × 0.043″ × 164-1/2″ blade",
         ],
         optional=["Roller stands", "Automatic feeding — see BS-5040"],
         images=["nt-h12sc-1", "nt-h12sc-2", "nt-h12sc-3", "nt-h12sc-4"],
         videos=[],
         models=[
             model("BS-5030", {"0": cap(300, [500, 300])},
                   3.0, "30/50/75/90", [4180, 34, 1.1], 1085,
                   other={"Vise": "Hydraulic jaw", "Control": "PLC, touch screen", "Max. hydraulic pressure": "2.2 MPa", "Drive": "V-belt, 4 speeds", PACK: "2270 × 1320 × 1710 mm", GROSS: "1175 kg"}),
         ]),
    dict(id="novotech-bs-650ga", group="semi-automatic",
         name="BS-650GA hydraulic swivel-head band saw, 18″",
         short="BS-650GA",
         models_label="BS-650GA",
         summary="An 18-inch swivel-head saw with automatic cutting and manual feeding: hydraulic vise, variable-frequency drive for stepless blade speed, a digital read-out for the feed position and a movable control panel. The bow swivels 45° to both sides and 60° to the right, and the gear-driven 7.4 HP motor handles 25-1/2″ × 13-3/4″ sections. Same frame as the automatic BS-650G without the feeder.",
         features=[
             "Ø18″ (460 mm) round / 25-1/2″ × 13-3/4″ at 0°; Ø18″ at 45° both sides, Ø12-1/4″ at 60°",
             "Automatic cutting cycle; material fed by hand on the roller table",
             "Hydraulic clamping vise, digital read-out of the feed position",
             "Variable blade speed 0–312 ft/min (inverter); 7.4 HP (5.5 kW) gear-driven motor",
             "Movable control panel; 1-5/8″ × 0.051″ × 205-1/2″ blade",
         ],
         optional=["Roller conveyors", "Automatic feeding — see BS-650G"],
         images=["nt-h18-1", "nt-h18-2"],
         videos=[],
         models=[
             model("BS-650GA", {"0": cap(460, [650, 350]), "+45": cap(460, [460, 350]), "-45": cap(460, [460, 350]), "+60": cap(310, [310, 350])},
                   5.5, "0-95", [5220, 41, 1.3], 1640,
                   other={"Vise": "Hydraulic", "Drive": "Gear, inverter", "Control panel": "Movable", PACK: "2950 × 1480 × 2120 mm", GROSS: "1880 kg"}),
         ]),
    # ================================================================ AUTOMATIC
    dict(id="novotech-bs300x370", group="automatic",
         name="BS300x370 automatic band saws with roller feed, 11-3/4″",
         short="BS300x370 automatic saws",
         models_label="BS300x370 · BS300x370H",
         summary="Compact automatic saws for batch cutting of bar, tube and profile up to Ø11-3/4″: a powered roller feed advances the stock, the hydraulic vise clamps, the bow cuts and returns, and the cycle repeats for the programmed count. Stepless blade speed from an inverter, gear drive and a 3 HP motor. The BS300x370H adds an automatic miter head for angle cuts of 30°, 45° and 60°.",
         features=[
             "Ø11-3/4″ (300 mm) round / 14-1/2″ × 11″ rectangular at 0°",
             "Roller feeding with automatic cycle; piece counter",
             "Hydraulic clamping vise; inverter-driven blade speed 0–371 ft/min",
             "Gear drive, 3 HP (2.2 kW) main motor, 0.3 HP feed motor",
             "BS300x370H: miter cutting 0°–60° (Ø11″ at 30°, Ø9″ at 45°, Ø5-1/8″ at 60°)",
         ],
         optional=["Roller conveyors", "Extra blades"],
         images=["nt-a12-1", "nt-a12-2", "nt-a12-3", "nt-a12t-1", "nt-a12t-2"],
         videos=[],
         models=[
             model("BS300x370", {"0": cap(300, [370, 280])},
                   2.2, "0-113", [3820, 27, 0.9], 800, wh=730,
                   other={"Feed motor": "0.25 kW", "Feeding": "Roller feed, automatic cycle", "Vise": "Hydraulic", "Drive": "Gear, inverter", PACK: "2140 × 1320 × 1500 mm", GROSS: "950 kg"}),
             model("BS300x370H", {"0": cap(300, [370, 280]), "+30": cap(280, [280, 280]), "+45": cap(230, [230, 250]), "+60": cap(130, [130, 150])},
                   2.2, "0-113", [3820, 27, 0.9], 940, wh=730,
                   other={"Feed motor": "0.25 kW", "Feeding": "Roller feed, automatic cycle", "Vise": "Hydraulic", "Drive": "Gear, inverter", PACK: "2140 × 1320 × 1500 mm", GROSS: "1090 kg"}),
         ]),
    dict(id="novotech-bs-5040", group="automatic",
         name="BS-5040 single-column automatic band saw",
         short="BS-5040",
         models_label="BS-5040",
         summary="The automatic version of the single-column saw: a hydraulic shuttle vise feeds up to 19-3/4″ (500 mm) per stroke, a batch clamping device holds bundles, and an automatic chip conveyor clears the swarf. PLC control with touch screen, hydraulic jaw vise, variable hydraulic down-feed, rapid descent until the blade touches the work and blade overload protection.",
         features=[
             "Ø11-3/4″ (300 mm) round / 19-3/4″ × 11-3/4″ rectangular (straight cut)",
             "Hydraulic shuttle-vise feeding, up to 19-3/4″ per stroke; batch clamping device",
             "PLC with finger-touch screen; rapid approach, then controlled feed",
             "Automatic chip conveyor, work light, coolant system",
             "Four blade speeds, 4 HP (3 kW) motor, 1-3/8″ × 0.043″ × 164-1/2″ blade",
         ],
         optional=["Roller conveyors"],
         images=["nt-a12sc-1", "nt-a12sc-2", "nt-a12sc-3", "nt-a12sc-4"],
         videos=[],
         models=[
             model("BS-5040", {"0": cap(300, [500, 300])},
                   3.0, "30/50/75/90", [4180, 34, 1.1], 1550,
                   other={"Feeding": "Hydraulic shuttle vise", "Feed length per stroke": "500 mm", "Vise": "Hydraulic jaw", "Control": "PLC, touch screen", "Max. hydraulic pressure": "2.5 MPa", "Drive": "V-belt, 4 speeds", PACK: "2260 × 2130 × 1780 mm", GROSS: "1720 kg"}),
         ]),
    dict(id="novotech-bs-460gb", group="automatic",
         name="BS-460GB automatic swivel-head miter band saw with 20 ft stand",
         short="BS-460GB",
         models_label="BS-460GB",
         summary="The automatic version of the BS-460G: PLC-controlled feeding and clamping with a shuttle vise (19-3/4″ per stroke), feed length selectable in inches or millimetres, and a 20 ft (6 m) material stand — 10 ft feed and 10 ft return — delivered with the machine. The bow still swivels to both sides for miter cuts, and a guard net protects the operator. Gear drive with variable blade speed by VFD inverter drive.",
         features=[
             "Ø13″ (330 mm) round / 18″ × 9-7/8″ at 0°; Ø12″ at 45° both sides, Ø8″ at 60°",
             "Automatic feeding and clamping, max. 19-3/4″ (500 mm) per stroke; standard PLC",
             "20 ft material stand included (feeder width 18″, height 33-1/2″)",
             "Bow swivels left and right; safety guard net",
             "Gear drive, 2/3 HP (1.5/2.2 kW) motor — variable blade speed by VFD inverter drive",
         ],
         optional=["Extra stands and supports", "Servo motor (variable blade speed)"],
         images=["nt-a13-1", "nt-a13-2", "nt-a13-3"],
         videos=[],
         models=[
             model("BS-460GB", {"0": cap(330, [460, 250]), "+45": cap(305, [305, 250]), "-45": cap(305, [305, 250]), "+60": cap(205, [205, 250])},
                   "1.5-2.2", "Variable, VFD inverter drive — up to 315 ft/min (96 m/min)", [3960, 34, 1.1], 1520,
                   other={"Feeding": "Shuttle vise, PLC", "Feed length per stroke": "500 mm", "Vise": "Hydraulic", "Drive": "Gear, variable blade speed by VFD inverter drive", PACK: "2500 × 2300 × 1630 mm", GROSS: "1655 kg"}),
         ]),
    dict(id="novotech-bs-cnc", group="automatic",
         name="BS-500G to BS-850G CNC automatic band saws",
         short="BS-500G–850G CNC saws",
         models_label="BS-500G · BS-500GT · BS-650G · BS-850G",
         summary="Production saws with CNC feeding and cutting: a servo-driven feeder positions the stock, hydraulic vises clamp it, the servo blade drive sets a stepless cutting speed and the PLC runs the batch. The BS-500G and BS-500GT have an automatic rotary bow (45°) and chip extraction; the BS-650G feeds up to 25-1/2″ per stroke with a linear scale on the feed and a swivelling control panel; the BS-850G cuts 33-1/2″ × 23-5/8″ sections with a hydraulic feeder as standard.",
         features=[
             "Round capacity from Ø13-3/4″ (350 mm) to Ø23-5/8″ (600 mm); miter cuts to 45° (BS-650G: 60°)",
             "CNC / PLC automatic feeding and clamping, hydraulic vises",
             "Servo motor for stepless blade speed; industrial gearbox (BS-650G)",
             "Feed per stroke: 19-3/4″ (BS-500G/500GT), 25-1/2″ (BS-650G), 23-5/8″ (BS-850G)",
             "Work light, chip extraction and coolant system included",
         ],
         optional=["Material supports and roller conveyors"],
         images=["nt-a14-1", "nt-a18-1", "nt-a18-2", "nt-a24-1"],
         videos=[],
         models=[
             model("BS-500G", {"0": cap(350, [500, 350]), "+45": cap(330, [330, 350])},
                   3.7, None, [4180, 34, 1.1], 2700,
                   other={"Blade drive": "Servo motor, stepless speed", "Feeding": "CNC, hydraulic clamping", "Feed length per stroke": "500 mm", "Bow swivel": "Automatic, to 45°", PACK: "2230 × 2220 × 1700 mm", GROSS: "2900 kg"}),
             model("BS-500GT", {"0": cap(415, [500, 415]), "+45": cap(335, [265, 415])},
                   3.7, None, [4555, 34, 1.1], 2780,
                   other={"Blade drive": "Servo motor, stepless speed", "Feeding": "CNC, hydraulic clamping", "Feed length per stroke": "500 mm", "Bow swivel": "Automatic, to 45°", PACK: "2250 × 2350 × 1750 mm", GROSS: "3000 kg"}),
             model("BS-650G", {"0": cap(460, [650, 350]), "+45": cap(460, [460, 350]), "+60": cap(310, [310, 350])},
                   5.5, "23-95", [5220, 41, 1.3], 2430,
                   other={"Blade drive": "Servo motor + industrial gearbox", "Feeding": "NC, automatic clamping", "Feed length per stroke": "650 mm", "Bow swivel": "Automatic, to 60° right", PACK: "3030 × 2280 × 2220 mm", GROSS: "2730 kg"}),
             model("BS-850G", {"0": cap(600, [850, 600]), "+45": cap(400, [400, 600])},
                   5.5, "0-119", [6685, 54, 1.6], 3945,
                   other={"Blade drive": "Servo motor, stepless speed", "Feeding": "Hydraulic feeder, CNC", "Feed length per stroke": "600 mm", "Bow swivel": "To 45°", PACK: "3550 × 2120 × 2660 mm (body), 1790 × 1720 × 1490 mm (feeder)", GROSS: "4235 kg"}),
         ]),
    # ================================================================ DOUBLE COLUMN
    dict(id="novotech-tbk-4228", group="double-column",
         name="TBK-4228 series double column band saws, 11″",
         short="TBK-4228 saws",
         models_label="TBK-4228 · TBK-4228A · TBK-4228B · TBK-4228B (improved)",
         summary="Twin-column saws for Ø11″ / 11″ × 11″ stock: the bow travels vertically on two columns, so the cut stays square whatever the feed pressure. Hydraulic down-feed with variable speed, hydraulic clamping and automatic shut-off on every model. Choose the base machine with hand-wheel feed (TBK-4228), the miter version that cuts at 30° and 45° (TBK-4228A), the automatic with a 3-position shuttle vise (TBK-4228B) or the automatic with stepless blade speed, chip conveyor and the new vise design (TBK-4228B (improved)).",
         features=[
             "Ø11″ (280 mm) round / 11″ × 11″ square; TBK-4228A: Ø10-1/4″ at 30°, Ø6-3/4″ at 45°",
             "Double column — vertical, rigid bow travel",
             "Hydraulic variable down-feed, hydraulic clamping, auto shut-off",
             "TBK-4228B / 4228B (improved): automatic feed and cut, 3-position vise for bundle cutting, feed length by limit switch",
             "TBK-4228B (improved): variable blade speed 0–200 ft/min, automatic chip conveyor",
             "Belt drive, 4 HP (3 kW) motor; work light, coolant and material stand included",
         ],
         optional=["Roller stand", "Extra blades"],
         images=["nt-dc11-1", "nt-dc11t-1", "nt-dc11t-2", "nt-dc11t-3", "nt-dc11a-1", "nt-dc11av-1", "nt-dc11av-3", "nt-dc11av-4", "nt-dc11-stand"],
         videos=[],
         models=[
             model("TBK-4228", {"0": cap(280, [280, 280], 280)},
                   3.0, "27/45/69", [3505, 27, 0.9], 695, hyd=0.55, dims=[2180, 1310, 1610],
                   other={"Feeding": "Manual hand wheel", "Vise": "Hydraulic", "Blade tensioning": "Mechanical", "Drive": "V-belt, 3 speeds", GROSS: "834 kg"}),
             model("TBK-4228A", {"0": cap(280, [280, 280], 280), "+30": cap(260, [260, 280]), "+45": cap(170, [170, 280])},
                   3.0, "27/45/69", [3625, 27, 0.9], 820, hyd=0.55, dims=[2180, 1300, 1600],
                   other={"Feeding": "Manual", "Miter cutting": "0°–45°", "Vise": "Hydraulic", "Blade tensioning": "Mechanical", "Drive": "V-belt, 3 speeds", GROSS: "965 kg"}),
             model("TBK-4228B", {"0": cap(280, [280, 280], 280)},
                   3.0, "27/45/69", [3505, 27, 0.9], 990, hyd=0.55, dims=[2250, 2010, 1640],
                   other={"Feeding": "Automatic, 3-position shuttle vise", "Vise": "Hydraulic", "Blade tensioning": "Mechanical", "Drive": "V-belt, 3 speeds", GROSS: "1160 kg"}),
             model("TBK-4228B (improved)", {"0": cap(280, [280, 280], 280)},
                   3.0, "0-61", [3505, 27, 0.9], 990, hyd=0.55, dims=[2250, 2010, 1640],
                   other={"Feeding": "Automatic, shuttle vise", "Vise": "Hydraulic, new clamp design", "Blade tensioning": "Mechanical", "Drive": "V-belt, inverter", "Chip conveyor": "Automatic", GROSS: "1160 kg"}),
         ]),
    dict(id="novotech-tgk-4235", group="double-column",
         name="TGK-4235 and TGK-4240 gear-driven double column saws",
         short="TGK-4235 / 4240",
         models_label="TGK-4235 · TGK-4240",
         summary="Heavier twin-column saws with a gear-driven motor and variable blade speed by VFD inverter drive, hydraulic blade tensioning and hydraulic clamping. Vertical lifting on two columns keeps the blade square in Ø13-3/4″ and Ø15-3/4″ solids; the cutting feed is hydraulically controlled and stepless. A three-position hydraulic clamping vise for bundles is optional.",
         features=[
             "TGK-4235: Ø13-3/4″ / 13-3/4″ × 13-3/4″ · TGK-4240: Ø15-3/4″ / 15-3/4″ × 15-3/4″",
             "Double column structure, vertical lifting, high stability",
             "Hydraulic variable down-feed, hydraulic clamping, hydraulic blade tensioning",
             "Gear drive, 3/3.8 HP or 4/5.4 HP motor — variable blade speed by VFD inverter drive",
             "Work light, coolant pump and material stand included",
         ],
         optional=["Three-position hydraulic clamping vise", "Roller stands"],
         images=["nt-dc14-1", "nt-dc14-2", "nt-dc14-3"],
         videos=[],
         models=[
             model("TGK-4235", {"0": cap(350, [350, 350], 350)},
                   "2.2-2.8", "Variable, VFD inverter drive — up to 226 ft/min (69 m/min)", [4115, 34, 1.1], 880, hyd=0.55, cool=0.04, dims=[2410, 1150, 1500],
                   other={"Vise": "Hydraulic", "Blade tensioning": "Hydraulic", "Drive": "Gear, variable blade speed by VFD inverter drive", GROSS: "990 kg"}),
             model("TGK-4240", {"0": cap(400, [400, 400], 400)},
                   "3.0-4.0", "Variable, VFD inverter drive — up to 184 ft/min (56 m/min)", [5000, 41, 1.3], 1325, hyd=0.75, cool=0.9, dims=[2700, 1350, 2150],
                   other={"Vise": "Hydraulic", "Blade tensioning": "Hydraulic", "Drive": "Gear, variable blade speed by VFD inverter drive", GROSS: "1585 kg"}),
         ]),
    dict(id="novotech-gz4250", group="double-column",
         name="GZ4250/70 and GZ4260/120 gantry double column saws",
         short="GZ4250/70 / GZ4260/120",
         models_label="GZ4250/70 · GZ4260/120",
         summary="Gantry-type double column saws for heavy plate, blocks, bundles and large tube: Ø19-3/4″ / 27-1/2″ × 19-3/4″ on the GZ4250/70 and Ø23-5/8″ / 47-1/4″ × 23-5/8″ on the GZ4260/120. Hydraulic clamping, stepless blade speed and a powered roller table; the GZ4260/120 adds hydraulic blade tensioning and a 15 HP motor for the 2-5/8″ blade.",
         features=[
             "GZ4250/70: Ø19-3/4″ / 27-1/2″ × 19-3/4″ · GZ4260/120: Ø23-5/8″ / 47-1/4″ × 23-5/8″",
             "Double column gantry structure for batch sawing of tubes, bars, profiles and plates",
             "Hydraulic clamping; variable blade speed (131–262 and 66–262 ft/min)",
             "GZ4250/70: 7.4 HP, 1-5/8″ × 0.051″ blade · GZ4260/120: 15 HP, 2-5/8″ × 0.051″ × 346-1/2″ blade, hydraulic tensioning",
             "Powered roller table with chain drive",
         ],
         optional=["Roller conveyors", "Bundle clamping"],
         images=["nt-dc20-1", "nt-dc24-1", "nt-dc24-2"],
         videos=[],
         models=[
             model("GZ4250/70", {"0": cap(500, [700, 500])},
                   5.5, "40-80", [None, 41, 1.3], 2590, hyd=1.5, cool=0.09,
                   other={"Vise": "Hydraulic", "Blade tensioning": "Manual", "Drive": "Belt", PACK: "3550 × 1500 × 2180 mm", GROSS: "2960 kg"},
                   notes="Blade length not printed in the catalogue."),
             model("GZ4260/120", {"0": cap(600, [1200, 600])},
                   11.0, "20-80", [8800, 67, 1.3], 5060, hyd=2.2, cool=0.12,
                   other={"Vise": "Hydraulic", "Blade tensioning": "Hydraulic", PACK: "4250 × 1750 × 2370 mm", GROSS: "5320 kg"}),
         ]),
]


def main():
    data = json.load(open(FAM, encoding="utf-8"))
    fams = {k: v for k, v in data["families"].items() if not k.startswith("novotech-")}
    order = [k for k in data["order"] if not k.startswith("novotech-")]
    for f in FAMILIES:
        rec = {
            "id": f["id"], "brand": "novotech", "line": "value", "group": f["group"],
            "name": f["name"], "short": f["short"], "models_label": f["models_label"],
            "summary": f["summary"], "features": f["features"], "optional": f["optional"],
            "images": f["images"], "videos": f["videos"],
            "specs": {"kind": "bandsaw", "voltage": f.get("voltage", V), "models": f["models"]},
        }
        fams[f["id"]] = rec
        order.append(f["id"])
    data["families"] = fams
    data["order"] = order
    json.dump(data, open(FAM, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("families:", len(fams), "value line:", len(FAMILIES))


if __name__ == "__main__":
    main()
