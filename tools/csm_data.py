#!/usr/bin/env python3
"""CSM (Chiao Sheng Machinery Co., Tainan, Taiwan — CNC tube benders since 1982, 24 patents, ISO 9001, CE) — sold under its
own brand: CNC, NC and symmetric tube benders (line page csm-tube-benders under the pipe-benders hub, written by
tools/isitan_tube_benders.py), tube end forming / grooving (a group on tube-end-forming-machines) and the CT325 circular saw (a
group on circular-cold-saws), both written by tools/isitan_pipe_end_saws.py, and the WB wire benders (wire-bending-machines,
tools/csm_pages.py).  Metric data from the supplier's electric and hydraulic catalogues and
tubebender.com.tw (Oct 2026), shown as imperial (metric).  CSM's laser cutting and riveting ranges are NOT transferred.
"""
BRAND = "csm"
P_BEND, P_FORM, P_SAW, P_WIRE = "csm-tube-benders", "tube-end-forming-machines", "circular-cold-saws", "wire-bending-machines"
P_CNC = P_NC = P_BEND        # the CSM benders have one line page under the pipe-benders hub (section rule: > 6 families → a page per line)


def vids(*ids_titles):
    from sahinler_lib import vids as _vids      # NovoTech's own channel: id, title, duration → video dict with thumb
    return _vids(*ids_titles)

GA = {1: "20 ga", 1.5: "16 ga", 1.6: "16 ga", 1.8: "15 ga", 2: "14 ga", 2.5: "12 ga", 2.8: "12 ga", 3: "11 ga", 3.5: "10 ga", 3.6: "10 ga", 3.8: "9 ga",
      4.5: "3/16″", 5.5: "7/32″", 7: "9/32″", 8: "5/16″", 9: "11/32″", 15: "19/32″"}


def od(mm):
    """Ø1-1/2″ (38.1 mm) — common tube sizes as fractions, else decimal inches"""
    frac = {12: "15/32″", 15: "19/32″", 18: "11/16″", 20: "13/16″", 25.4: "1″", 30: "1-3/16″", 32: "1-1/4″", 38: "1-1/2″", 38.1: "1-1/2″", 45: "1-3/4″",
            50: "2″", 50.8: "2″", 65: "2-1/2″", 76.2: "3″", 80: "3-1/8″", 88.9: "3-1/2″", 100: "4″", 101.6: "4″", 120: "4-3/4″", 127: "5″",
            152.4: "6″", 180: "7″", 220: "8-5/8″"}
    return f"Ø{frac.get(mm, f'{mm / 25.4:.2f}″')} ({mm:g} mm)"


def wall(mm):
    return f"{GA.get(mm, f'{mm / 25.4:.3f}″')} ({mm:g} mm)"


def clr(rng):
    a, b = rng.split("-")
    return f"{int(a) / 25.4:.1f} – {int(b) / 25.4:.1f}″ ({a} – {b} mm)"


def mm_in(mm):
    return f"{mm / 25.4:,.1f}″ ({mm:,} mm)"


def ft(mm):
    return f"{mm / 304.8:.1f} ft · {mm / 25.4:,.0f}″ ({mm:,} mm)"


def hp(kw):
    return f"{kw * 1.341:.1f} HP ({kw:g} kW)"


def lb(kg):
    return f"{round(kg * 2.20462):,} lb ({kg:,} kg)"


def dims(l, w, h):
    return f"{l / 25.4:.0f} × {w / 25.4:.0f} × {h / 25.4:.0f}″ ({l:,} × {w:,} × {h:,} mm)"


def psi(kgf):
    return f"{round(kgf * 14.223):,} psi ({kgf} kgf/cm²)"


GK = ["capacity", "clr", "working_length", "control", "weight"]
NOTE_BEND = ("Capacities are the manufacturer's ratings for round mild-steel tube, outside diameter × wall; CLR = centreline radius of the bend die. "
             "Mandrel length is the maximum tube length fed with the standard mandrel rod (the working length). Tooling capacity is the number of "
             "stacked bend dies / radii; \"roll bending\" models carry a roll-bending head for large radii; a rear booster (RBE servo, RBF / RBH / CBF "
             "hydraulic) pushes the tube from behind for thin-wall and tight-radius bends. Three-phase machines are supplied for 600 V with a CSA-approved panel.")


def bend_table(title, sub, rows, control):
    """rows: (part no, od, wt, clr, mandrel, tooling, roll, booster)"""
    models = [r[0] for r in rows]
    t = {"title": title, "sub": sub, "models": models, "rows": [
        {"label": "Max. tube capacity", "sub": "OD × wall, mild steel", "cells": [f"{od(r[1])} × {wall(r[2])}" for r in rows], "key": True},
        {"label": "Centreline radius (CLR)", "sub": "", "cells": [clr(r[3]) for r in rows], "key": True},
        {"label": "Mandrel working length", "sub": "", "cells": [ft(r[4]) for r in rows], "key": True},
        {"label": "Tooling capacity", "sub": "stacked dies / radii", "cells": [str(r[5]) for r in rows], "key": False},
        {"label": "Roll bending", "sub": "", "cells": ["Yes" if r[6] else "—" for r in rows], "key": False},
        {"label": "Rear booster", "sub": "", "cells": [{"servo": "Servo", "hydraulic": "Hydraulic"}.get(r[7], "—") for r in rows], "key": False},
    ]}
    glance = {r[0]: [f"{od(r[1]).split(' (')[0]} × {wall(r[2]).split(' (')[0]}", f"{int(r[3].split('-')[1]) / 25.4:.1f}″ ({r[3].split('-')[1]} mm)",
                     f"{r[4] / 304.8:.1f} ft", control, "—"] for r in rows}
    return t, glance


def spec(tables_glances, caps=None, note=NOTE_BEND):
    tables = [t for t, _ in tables_glances]
    glance = {}
    for _, g in tables_glances:
        glance.update(g)
    models = [{"name": m, "glance": glance.get(m, [])} for t in tables for m in t["models"]]
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": GK, "caps": caps or {}, "note": note}


# ---------------------------------------------------------------- CNC all-electric
EMB = [("15 EMB", 15, 1.5, "10-55", 1000, "3+3", False, ""), ("20 EMB", 20, 1.5, "10-80", 1500, "3+3", False, ""), ("20 EMR", 20, 1.5, "10-80", 1500, "3+3", True, ""),
       ("32 MBRE", 32, 1.8, "25-128", 3500, "3+3", True, ""), ("30 EMR", 30, 2, "15-90", 2800, "3+3", True, ""), ("45 EMR", 45, 1.6, "30-150", 3000, "3+3", True, ""),
       ("75 EMR", 76.2, 2, "40-230", 3000, "3+3", True, "servo")]
MRE2 = [("50 MRE2-RBE", 50.8, 1.8, "30-150", 2500, 3, True, "servo"), ("80 MRE2-RBE", 80, 2.5, "40-230", 3000, 3, True, "servo"), ("100 MRE2-RBE", 100, 3.6, "30-300", 3000, 3, True, "servo")]
# ---------------------------------------------------------------- CNC electric hybrid
MBE = [("18 MBE", 18, 1.6, "10-80", 1200, 3, False, ""), ("25 MBE", 25.4, 1.5, "15-120", 1500, 3, False, ""), ("30 MBE", 30, 2, "15-120", 2200, 3, False, ""),
       ("38 MBE", 38.1, 1.8, "25-150", 2200, 3, False, ""), ("50 MBE", 50.8, 2, "30-220", 2500, 3, False, ""), ("65 MBE", 65, 2.5, "35-250", 2500, 3, False, ""),
       ("80 MBE", 80, 2.5, "40-280", 3500, 3, False, ""), ("100 MBE", 100, 3, "30-300", 3500, 3, False, ""),
       ("65 MBE-RBE", 65, 2.5, "35-250", 2500, 3, False, "servo"), ("80 MBE-RBE", 80, 2.8, "40-280", 3500, 3, False, "servo"), ("100 MBE-RBE", 100, 3.6, "30-300", 3500, 3, False, "servo"),
       ("130 MBE-RBE", 127, 3.8, "80-400", 4000, 3, False, "servo")]
MRE = [("18 MRE", 18, 1.6, "10-80", 1200, 3, True, ""), ("25 MRE", 25.4, 1.5, "15-120", 1500, 3, True, ""), ("30 MRE", 30, 2, "15-120", 2200, 3, True, ""),
       ("38 MRE", 38, 1.8, "25-150", 2200, 3, True, ""), ("50 MRE", 50.8, 2, "30-220", 2500, 3, True, ""), ("65 MRE", 65, 2.5, "35-250", 2500, 3, True, ""),
       ("80 MRE", 80, 2.5, "40-280", 3500, 3, True, ""), ("65 MRE-RBE", 65, 2.5, "35-250", 2500, 3, True, "servo"), ("80 MRE-RBE", 80, 2.8, "40-280", 3500, 3, True, "servo"),
       ("100 MRE-RBE", 100, 3.6, "30-300", 3500, 3, True, "servo"), ("130 MRE-RBE", 127, 3.8, "80-400", 4000, 3, True, "servo"), ("150 MRE-RBE", 152.4, 3, "90-400", 4000, 3, True, "servo")]
TBRE = [("25 TBRE", 25.4, 1.5, "15-120", 1500, 2, True, ""), ("30 TBRE", 30, 2, "15-120", 2200, 2, True, ""), ("38 TBRE", 38.1, 1.8, "25-150", 2200, 2, True, ""),
        ("50 TBRE", 50.8, 2, "30-220", 2500, 2, True, ""), ("65 TBRE", 65, 2, "35-250", 2500, 2, True, ""), ("80 TBRE", 80, 2.5, "40-280", 3500, 2, True, ""),
        ("100 TBRE", 100, 3, "30-300", 3500, 2, True, ""), ("65 TBRE-RBE", 65, 2.5, "35-250", 2500, 2, True, "servo"), ("80 TBRE-RBE", 80, 2.8, "40-280", 3500, 2, True, "servo"),
        ("100 TBRE-RBE", 100, 3.6, "30-300", 3500, 2, True, "servo"), ("130 TBRE-RBE", 127, 3.8, "80-400", 4000, 2, True, "servo")]
TMRE = [("25 TMRE", 25.4, 1.5, "15-120", 1500, 3, True, ""), ("30 TMRE", 30, 2, "15-120", 2200, 3, True, ""), ("38 TMRE", 38.1, 1.8, "25-150", 2200, 3, True, ""),
        ("50 TMRE", 50.8, 2, "30-220", 2500, 3, True, ""), ("65 TMRE", 65, 2, "35-250", 2500, 3, True, ""), ("80 TMRE", 80, 2.5, "40-280", 3500, 3, True, ""),
        ("100 TMRE", 100, 3, "30-300", 3500, 3, True, ""), ("65 TMRE-RBE", 65, 2.5, "35-250", 2500, 3, True, "servo"), ("80 TMRE-RBE", 80, 2.8, "40-280", 3500, 3, True, "servo"),
        ("100 TMRE-RBE", 100, 3.6, "30-300", 3500, 3, True, "servo")]
TSRE = [("18 TSRE", 18, 1.6, "10-80", 1200, 1, False, ""), ("30 TSRE", 30, 2, "15-120", 2200, 1, False, ""), ("38 TSRE", 38.1, 1.8, "25-150", 2200, 1, False, ""),
        ("50 TSRE", 50.8, 2, "30-220", 2500, 1, False, ""), ("65 TSRE", 65, 2, "35-250", 2500, 1, False, ""), ("80 TSRE", 80, 2.5, "40-280", 3500, 1, False, ""),
        ("100 TSRE", 100, 3, "40-350", 3500, 1, False, ""), ("65 TSRE-RBE", 65, 2.5, "35-250", 2500, 1, False, "servo"), ("80 TSRE-RBE", 80, 2.8, "40-280", 3500, 1, False, "servo")]
TDRE = [("12 TDRE", 12, 1, "12-55", 1000, 2, False, ""), ("18 TDRE", 18, 1.6, "10-80", 1200, 2, False, ""), ("25 TDRE", 25.4, 1.5, "15-120", 1500, 2, False, ""),
        ("30 TDRE", 30, 2, "15-120", 2200, 2, False, ""), ("38 TDRE", 38.1, 1.8, "25-150", 2200, 2, False, ""), ("50 TDRE", 50.8, 2, "30-220", 2500, 2, False, ""),
        ("65 TDRE", 65, 2, "35-250", 2500, 2, False, ""), ("80 TDRE", 80, 2.5, "40-280", 3500, 2, False, ""), ("100 TDRE", 100, 3, "30-300", 3500, 2, False, ""),
        ("65 TDRE-RBE", 65, 2.5, "35-250", 2500, 2, False, "servo"), ("80 TDRE-RBE", 80, 2.8, "40-280", 3500, 2, False, "servo"), ("100 TDRE-RBE", 100, 3.6, "30-300", 3500, 2, False, "servo")]
# ---------------------------------------------------------------- CNC hydraulic
TSR = [("38 TSR", 38.1, 3, "25-150", 2200, 1, False, ""), ("50 TSR", 50.8, 3, "30-220", 2200, 1, False, ""), ("65 TSR", 65, 3, "35-250", 2500, 1, False, ""),
       ("80 TSR", 80, 4.5, "40-280", 3000, 1, False, ""), ("100 TSR", 101.6, 5.5, "60-400", 3600, 1, False, ""), ("120 TSR", 120, 5.5, "80-450", 5000, 1, False, ""),
       ("150 TSR", 152.4, 7, "90-500", 6000, 1, False, ""), ("180 TSR", 180, 9, "100-600", 6000, 1, False, ""), ("220 TSR", 220, 15, "100-800", 6000, 1, False, ""),
       ("80 TSR-RBF", 80, 5.5, "32-345", 3000, 1, False, "hydraulic"), ("100 TSR-RBF", 101.6, 5.5, "30-400", 3600, 1, False, "hydraulic"), ("120 TSR-RBF", 120, 5.5, "80-450", 5000, 1, False, "hydraulic"),
       ("50 TSR-RBH", 50.8, 3, "30-220", 2200, 1, False, "hydraulic"), ("65 TSR-RBH", 65, 3, "35-250", 2500, 1, False, "hydraulic"), ("80 TSR-RBH", 80, 4.5, "40-250", 3000, 1, False, "hydraulic"),
       ("100 TSR-RBH", 101.6, 5.5, "60-400", 3600, 1, False, "hydraulic"), ("120 TSR-RBH", 120, 5.5, "80-450", 5000, 1, False, "hydraulic"), ("150 TSR-RBH", 152.4, 7, "90-500", 6000, 1, False, "hydraulic"),
       ("180 TSR-RBH", 180, 9, "100-600", 6000, 1, False, "hydraulic")]
TDR = [("38 TDR", 38.1, 3, "25-150", 2200, 2, False, ""), ("50 TDR", 50.8, 3, "30-220", 2200, 2, False, ""), ("65 TDR", 65, 3, "35-250", 2500, 2, False, ""),
       ("80 TDR", 80, 4.5, "40-280", 3000, 2, False, ""), ("100 TDR", 101.6, 5.5, "60-400", 3600, 2, False, ""), ("120 TDR", 120, 5.5, "80-400", 5000, 2, False, ""),
       ("150 TDR", 152.4, 7, "90-500", 6000, 2, False, ""), ("100 TDR-RBH", 101.6, 5.5, "60-400", 3600, 2, False, "hydraulic"), ("150 TDR-RBH", 152.4, 7, "90-500", 6000, 2, False, "hydraulic")]
# ---------------------------------------------------------------- NC hydraulic
TSRJ = [("38 TSRJ", 38.1, 3, "25-150", 2200, 1, False, ""), ("50 TSRJ", 50.8, 3, "30-220", 2200, 1, False, ""), ("65 TSRJ", 65, 3, "35-250", 2500, 1, False, ""),
        ("80 TSRJ", 80, 4.5, "40-280", 3000, 1, False, ""), ("38 TDRJ", 38.1, 3, "25-150", 2200, 2, False, ""), ("50 TDRJ", 50.8, 3, "30-220", 2200, 2, False, ""), ("65 TDRJ", 65, 3, "35-250", 2500, 2, False, "")]
TNCPB = [("50 TNCPB", 50.8, 3, "30-220", 2100, 1, False, ""), ("75 TNCPB", 76.2, 3, "40-250", 2400, 1, False, ""), ("89 TNCPB", 88.9, 2.5, "50-300", 2600, 1, False, ""), ("100 TNCPB", 101.6, 5.5, "60-400", 3600, 1, False, "")]
TNCB = [("38 TNCB", 38.1, 3, "25-170", 1900, 1, False, ""), ("50 TNCB", 50.8, 3, "30-250", 2200, 1, False, ""), ("75 TNCB", 76.2, 3, "40-300", 2600, 1, False, ""),
        ("89 TNCB", 88.9, 2.5, "40-350", 2600, 1, False, ""), ("100 TNCB", 101.6, 5.5, "60-400", 3600, 1, False, ""), ("120 TNCB", 127, 3.5, "80-450", 5200, 1, False, ""),
        ("150 TNCB", 152.4, 7, "90-500", 6000, 1, False, ""), ("180 TNCB", 180, 9, "100-600", 6000, 1, False, ""), ("220 TNCB", 220, 8, "100-700", 6000, 1, False, ""),
        ("75 TNCB-CBF", 76.2, 3, "40-300", 2600, 1, False, "hydraulic"), ("120 TNCB-CBF", 127, 5.5, "80-400", 5200, 1, False, "hydraulic"),
        ("120 TNCB-RBF", 127, 5.5, "60-450", 5200, 1, False, "hydraulic"), ("220 TNCB-RBF", 220, 7, "100-1000", 6000, 1, False, "hydraulic")]

CTRL_IPC = "IPC CNC · touch-screen · 3D simulation"
CTRL_PLC = "PLC NC · touch-screen"

STD_CNC_CTRL = ["Industrial-PC control with touch-screen: bending simulation, 3D preview and interference detection; reads IGS / STP files",
                "Programmable speed for every servo axis; USB port for data transfer; manual / automatic mode; inch / metric; XYZ / YBC axes"]
STD_SERVO_AXES = ["Bend arm (C-axis) by servo motor through CSM's patented transmission gears — ±0.01° tolerance",
                  "Carriage (Y-axis) by servo motor with programmable speed; collet (B-axis) rotation by servo motor"]
STD_MANDREL_SERVO = "Mandrel by servo motor with automatic lubrication and anticipated retraction"
STD_MANDREL_HYD = "Mandrel by hydraulics with automatic lubrication and anticipated retraction"
VOLT = "CSA-approved electrical panel; 600 V 3-phase with transformer (208 / 240 / 480 V on request)"
OPT_BEND = ["Automatic tube loader and unloader; bundle loading", "Rear booster (servo RBE / hydraulic RBF, RBH) for thin-wall and tight-radius bending",
            "Roll-bending head for large radii", "Integrated circular saw, end-forming station and robot transfer — automated bending cells",
            "Tooling: bend dies, clamp dies, pressure dies, wiper dies and mandrels to your tube and radius", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"]

FAMILIES = [
    # ---------------------------------------------------------------- CNC page
    dict(id="csm-emr", group="csm-electric", page=P_CNC, brand=BRAND,
         name="EMB / EMR and MRE2-RBE all-electric CNC tube benders, Ø19/32″ to Ø4″",
         short="EMB / EMR all-electric",
         models_label="15 EMB – 75 EMR · 50 – 100 MRE2-RBE · 10 models",
         summary="CSM's all-electric CNC benders: every axis — bend arm, carriage, collet, clamp and pressure die, side booster, tool shift and mandrel — "
                 "is a servo motor, so there is no hydraulic unit, no oil, no warm-up and about half the energy of a hydraulic bender, with "
                 "±0.01° bend-arm accuracy. The EMB / EMR work-head rotates to bend left- and right-hand in the same part — brake and fuel lines, "
                 "air-conditioning and oil tube on the 15 and 20, furniture and health-care tube on the 30 – 45, automotive and transportation tube "
                 "on the 75 — with 3 + 3 stacked tools and a roll-bending head. The MRE2-RBE adds a servo rear booster for Ø2″ to Ø4″ tube in "
                 "thin walls and tight radii.",
         headline="All-electric · left- and right-hand bending · Ø19/32″ – Ø4″ · 3 + 3 stacked tools",
         features=["All axes by servo motor: bend arm, carriage, collet, clamp die (EMB / EMR by pneumatic), pressure die, side booster, tool shift up-down and left-right",
                   "Work-head rotation by servo motor — converts between left- and right-hand bending within one part (EMB / EMR)", STD_MANDREL_SERVO,
                   "Servo rear booster on the MRE2-RBE and 75 EMR"] + STD_CNC_CTRL + [VOLT],
         optional=OPT_BEND,
         images=["cs-emr", "cs-mre2", "cs-emr-15", "cs-emr-45", "cs-emr-75", "cs-mre2-50", "cs-mre2-100", "cs-emr-parts-small", "cs-emr-parts-mid", "cs-emr-parts-large", "cs-mre2-parts", "cs-mre2-parts-large"],
         videos=vids(("-2gkOrFzL_E", "15 EMB all-electric bender — fuel lines"), ("MDyNuwdL4NM", "20 EMB — car head-rest bars"), ("qqJaIEVVA4o", "20 EMBH with robot cell — car head rests"),
                     ("QaaLWs2v9rM", "45 EMR CNC tube bender"), ("_0lmdzh_CMo", "45 EMR — left- and right-hand bending"), ("4yCa4Psl0kY", "100 MRE2-RBE all-electric pipe bender"),
                     ("ziFviuJ280Q", "100 MRE2-RBE CNC mandrel tube bender")),
         specs=spec([bend_table("EMB / EMR", "All-electric CNC left- and right-hand benders", EMB, CTRL_IPC), bend_table("MRE2-RBE", "All-electric CNC benders with servo rear booster", MRE2, CTRL_IPC)],
                    caps={"45 EMR": "Ø1-3/4″ × 16 ga · all-electric, left / right bending", "80 MRE2-RBE": "Ø3-1/8″ × 12 ga · all-electric with servo booster"})),
    dict(id="csm-mbe", group="csm-electric", page=P_CNC, brand=BRAND,
         name="MBE / MRE electric-hybrid CNC tube benders, Ø11/16″ to Ø6″",
         short="MBE / MRE electric hybrid",
         models_label="18 MBE – 150 MRE-RBE · 24 models",
         summary="The electric-hybrid bender: servo motors on the bend arm, carriage, collet rotation and tool shift for accuracy and speed, hydraulics "
                 "on the clamp die, pressure die, side booster and mandrel for force — the combination most production shops choose. Twenty-four "
                 "models from Ø11/16″ to Ø6″ in three stacked tools; the MRE adds a roll-bending head for large radii and the -RBE versions a servo "
                 "rear booster. The work-head travels on linear guides, so the same machine bends clockwise and counter-clockwise.",
         headline="Electric hybrid · Ø11/16″ – Ø6″ · 3 stacked tools · clockwise and counter-clockwise",
         features=STD_SERVO_AXES + ["Clamp die, pressure die and side booster by hydraulics; tool / radii shift up-down and left-right by servo motor", STD_MANDREL_HYD,
                                    "Work-head on linear guides — bends clockwise and counter-clockwise on one machine (MBE / MRE)", "Roll-bending head on the MRE; servo rear booster on the -RBE models"] + STD_CNC_CTRL + [VOLT],
         optional=OPT_BEND,
         images=["cs-mbe", "cs-mbe-parts", "cs-mbe-parts-2"],
         videos=vids(("jm3NRKCkZ24", "18 MBE steel tube bender"), ("N25JS5HRfhI", "65 MBE — trunk hood hinges"), ("onuI3yw9ORo", "80 MBE-RBE with saw cutter"),
                     ("837dwPNiKq8", "90 MBE-RBE exhaust pipe bender"), ("qwCp0PyUBaY", "50 MRE — handlebars"), ("dDR4wWSnXiY", "50 MRE-RBE with robot transfer and checking fixture"),
                     ("9TQpk6FSaBM", "80 MRE aluminum profile bender"), ("AWu19COeHqU", "130 MRE-RBE chassis tube bender")),
         specs=spec([bend_table("MBE", "Electric-hybrid CNC benders", MBE, CTRL_IPC), bend_table("MRE", "Electric-hybrid CNC benders with roll-bending head", MRE, CTRL_IPC)],
                    caps={"80 MBE": "Ø3-1/8″ × 12 ga · electric hybrid"})),
    dict(id="csm-tbre", group="csm-electric", page=P_CNC, brand=BRAND,
         name="TBRE / TMRE and TSRE / TDRE electric-hybrid CNC tube benders, Ø15/32″ to Ø5″",
         short="TBRE / TMRE / TDRE electric hybrid",
         models_label="25 TBRE – 130 TBRE-RBE · 25 – 100 TMRE-RBE · 18 TSRE – 100 TDRE-RBE · 42 models",
         summary="The T series: the same servo bend arm, carriage and collet as the MBE on a fixed work-head with two (TBRE, TDRE) or three (TMRE) "
                 "stacked tools and hydraulic tool shift up-down — the economical electric-hybrid bender for a shop that bends one direction. "
                 "The TBRE / TMRE carry a roll-bending head and reach Ø5″; the TSRE (one tool) and TDRE (two tools) start at Ø15/32″ for HVAC and "
                 "fuel line and go to Ø4″; -RBE versions add the servo rear booster.",
         headline="Electric hybrid · Ø15/32″ – Ø5″ · 1 – 3 stacked tools · roll bending on TBRE / TMRE",
         features=STD_SERVO_AXES + ["Clamp die, pressure die and side booster by hydraulics; tool shift up-down by hydraulics, left-right by servo motor", STD_MANDREL_HYD,
                                    "Roll-bending head on the TBRE / TMRE; servo rear booster on the -RBE models"] + STD_CNC_CTRL + [VOLT],
         optional=OPT_BEND,
         images=["cs-tbre", "cs-tdre", "cs-tbre-parts", "cs-tbre-parts-2", "cs-tdre-parts", "cs-tdre-parts-2"],
         videos=vids(("a-IhDc2PMvg", "32 TBRE CNC tube bender"), ("8HGVF3b_hYs", "38 TMRE three-stack bender — stroller frames"), ("JM40hF49R8A", "80 TBRE-RBE with roll bender and punching unit"),
                      ("1NBAKSIfxBo", "38 TBRE with punch — oval furniture tube"), ("ESVmrPwJ-6A", "12 TDRE brake line bender"), ("2RBTDwhJG1E", "65 TDRE exhaust pipe bender"),
                      ("2mRTbtcL7os", "18 TDRE with LD020 automatic loader"), ("iEgi5kfQ2EY", "130 TBRE-RBE — driver cabin frames")),
         specs=spec([bend_table("TBRE", "Two stacked tools, roll bending", TBRE, CTRL_IPC), bend_table("TMRE", "Three stacked tools, roll bending", TMRE, CTRL_IPC),
                     bend_table("TSRE", "One tool", TSRE, CTRL_IPC), bend_table("TDRE", "Two stacked tools", TDRE, CTRL_IPC)],
                    caps={"65 TDRE": "Ø2-1/2″ × 14 ga · electric hybrid, two tools"})),
    dict(id="csm-tsr", group="csm-hydraulic", page=P_CNC, brand=BRAND,
         name="TSR / TDR hydraulic CNC pipe benders, Ø1-1/2″ to Ø8-5/8″",
         short="TSR / TDR hydraulic CNC",
         models_label="38 TSR – 220 TSR · TSR-RBF / RBH · 38 TDR – 150 TDR-RBH · 28 models",
         summary="The heavy hydraulic CNC bender for pipe and thick-wall tube: a hydraulic bend arm, clamp, pressure die and side booster with a "
                 "servo carriage and collet rotation, from Ø1-1/2″ × 11 ga to Ø8-5/8″ × 19/32″ pipe on 20 ft mandrels — boiler, construction, "
                 "shipyard, oil-rig and water-supply pipe. The TDR carries two stacked tools; the -RBF and -RBH versions add a hydraulic rear "
                 "booster for thin-wall pipe and radii down to 1 × D. Industrial-PC control with 3D simulation, or the PLC control of the NC range.",
         headline="Hydraulic CNC · Ø1-1/2″ – Ø8-5/8″ · pipe to 19/32″ wall · 1 – 2 tools",
         features=["Bend arm (C-axis), clamp die, pressure die and side booster by hydraulics", "Carriage (Y-axis) by servo motor with programmable speed; collet (B-axis) rotation by servo motor",
                   "Tool / radii shift up-down and left-right by hydraulics (TDR)", STD_MANDREL_HYD, "Hydraulic rear booster on the -RBF / -RBH models"] + STD_CNC_CTRL + [VOLT],
         optional=OPT_BEND,
         images=["cs-tsr", "cs-tsr-parts", "cs-tsr-parts-2", "cs-tsr-parts-3"],
         videos=vids(("8fi_4Ccsh00", "38 TSR CNC hydraulic pipe bender"), ("gUbyulH7I-0", "50 TSR with automatic loader"), ("N02_RPTBW2E", "65 TSR CNC pipe bender"),
                     ("QH6HAbj2Aqs", "80 TSR-RBF serpentine bender"), ("xvaNquiXaNA", "150 TSR shipyard CNC pipe bender"), ("8IKC2uQYhDk", "180 TSR CNC pipe bender"),
                     ("X-zuvXJGMfI", "38 TDR with split dies"), ("rMYecEESog4", "100 TDR-RBH exhaust pipe bender with seam detection")),
         specs=spec([bend_table("TSR", "Hydraulic CNC benders, one tool", TSR, CTRL_IPC), bend_table("TDR", "Hydraulic CNC benders, two stacked tools", TDR, CTRL_IPC)],
                    caps={"100 TSR": "Ø4″ × 7/32″ · hydraulic CNC", "220 TSR": "Ø8-5/8″ × 19/32″ · hydraulic CNC"})),
    # ---------------------------------------------------------------- NC page
    dict(id="csm-tsrj", group="csm-nc", page=P_NC, brand=BRAND,
         name="TSRJ / TDRJ and TNCPB NC hydraulic tube benders, Ø1-1/2″ to Ø4″",
         short="TSRJ / TDRJ / TNCPB NC",
         models_label="38 – 80 TSRJ · 38 – 65 TDRJ · 50 – 100 TNCPB · 11 models",
         summary="The NC hydraulic benders with a PLC touch-screen: the TSRJ (one tool) and TDRJ (two tools) feed the tube with a servo carriage "
                 "at programmable speed and rotate it with a servo collet, so multi-plane parts are bent from a stored program; the TNCPB is fed by "
                 "hand against the stop with servo rotation — the lowest-priced programmed bender for Ø2″ to Ø4″ furniture, railing and automotive "
                 "tube. Hydraulic bend arm, clamp, pressure die and side booster; mandrel with automatic lubrication and anticipated retraction.",
         headline="NC hydraulic · Ø1-1/2″ – Ø4″ · servo feed (TSRJ / TDRJ) or manual feed (TNCPB)",
         features=["Bend arm (C-axis), clamp die, pressure die and side booster by hydraulics", "Carriage (Y-axis) by servo motor with programmable speed (TSRJ / TDRJ) — manual feeding on the TNCPB",
                   "Collet (B-axis) grip by hydraulics, rotation by servo motor", STD_MANDREL_HYD, "Tool / radii shift up-down and left-right by hydraulics (TDRJ)",
                   "PLC control with touch-screen: programmable servo speeds, USB port, manual / automatic, inch / metric; XYZ / YBC axes optional", VOLT],
         optional=OPT_BEND,
         images=["cs-tsrj", "cs-tncpb", "cs-tsrj-carriage"],
         videos=vids(("uHg5_8L7djQ", "75 TNCPB NC pipe bending machine")),
         specs=spec([bend_table("TSRJ / TDRJ", "NC hydraulic benders with servo carriage", TSRJ, CTRL_PLC), bend_table("TNCPB", "NC hydraulic benders with manual feeding", TNCPB, CTRL_PLC)],
                    caps={"75 TNCPB": "Ø3″ × 11 ga · NC hydraulic, manual feed"})),
    dict(id="csm-tncb", group="csm-nc", page=P_NC, brand=BRAND,
         name="TNCB single-axis NC hydraulic pipe benders, Ø1-1/2″ to Ø8-5/8″",
         short="TNCB single-axis NC",
         models_label="38 TNCB – 220 TNCB · TNCB-CBF / RBF · 13 models",
         summary="The single-axis hydraulic bender with a mandrel: the operator positions the pipe against the mechanical stop, the PLC bends it "
                 "to the programmed angle — the simple, rugged machine for boiler, construction, shipyard and water-supply pipe from Ø1-1/2″ to "
                 "Ø8-5/8″, and for furniture and automotive tube on the small models. The -CBF and -RBF versions add a hydraulic booster for "
                 "thin-wall pipe and tight radii, the 220 TNCB-RBF bends to a 39″ centreline radius.",
         headline="Single-axis NC hydraulic · Ø1-1/2″ – Ø8-5/8″ · mandrel · mechanical stop",
         features=["Bend arm (C-axis), clamp die, pressure die and side booster by hydraulics", STD_MANDREL_HYD, "Mechanical stopper for the feed position",
                   "Hydraulic booster on the -CBF / -RBF models", "PLC control with touch-screen: programmable speeds, USB port, manual / automatic, inch / metric", VOLT],
         optional=["Automatic loader", "Hydraulic rear booster", "Tooling: bend dies, clamp dies, pressure dies, wiper dies and mandrels to your pipe and radius", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"],
         images=["cs-tncb", "cs-tncb-parts", "cs-tncb-parts-2"],
         videos=vids(("Z3eMKTBjO5A", "38 TNCB NC mandrel pipe bender"), ("bp16NSlrOXc", "38 TNCB bending square tube"), ("TU0e6UvHXLQ", "50 TNCB mandrel pipe bender"),
                      ("g-hrQ6svHn8", "75 TNCB NC pipe bender"), ("groeKSO8KBs", "100 TNCB NC hydraulic pipe bender"), ("_qmrm1RAdv8", "120 TNCB-RBF boiler pipe — 1 × D bends"),
                      ("Q7NQpY0_nvI", "220 TNCB NC mandrel bender"), ("0RuOxFGOlTA", "220 TNCB-RBF mandrel pipe bender")),
         specs=spec([bend_table("TNCB", "Single-axis NC hydraulic benders", TNCB, CTRL_PLC)], caps={"120 TNCB": "Ø5″ × 10 ga · single-axis NC"})),
    dict(id="csm-f38", group="csm-symmetric", page=P_NC, brand=BRAND,
         name="F38 / F50 symmetric tube benders — both ends of the tube bent at once, Ø1-1/2″ and Ø2″",
         short="F38 / F50 symmetric benders",
         models_label="F38 · F50 · F38-90 · F38H-4A · F38H-5A · 5 models",
         summary="Two bending heads on one bed bend both ends of a tube in the same stroke — towel rails, handles, furniture frames, U-bolts, chair "
                 "legs and headboards come off the machine finished, at twice the output of a single-head bender. The F38 and F50 are the "
                 "single-axis hydraulic machines with a head pusher for fast unloading; the F38-90 adds manual multi-plane rotation; the F38H-4A "
                 "and F38H-5A feed the tube with a servo motor and the -5A rotates it with a servo collet for automatic multi-plane parts. Stacked "
                 "tools for Ø3/4″, Ø1″, Ø1-1/4″ and Ø1-1/2″.",
         headline="Two heads · Ø1-1/2″ and Ø2″ × 12 ga · 1 to 3 axes · stacked tools",
         features=["Two bending heads bend both tube ends in one cycle; bending, clamp die and pressure die by hydraulics", "Head pusher for fast unloading (single-axis models)",
                   "Feeding by servo motor (F38H-4A / 5A); grip by hydraulics with servo rotation for multi-plane bends (F38H-5A)",
                   "Stacked tooling: up to 3 – 4 dies for Ø3/4″, 2 – 3 for Ø1″, 1 – 2 for Ø1-1/4″, 1 for Ø1-1/2″", VOLT],
         optional=["Tooling to your tube and radius", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"],
         images=["cs-f38h", "cs-f38"],
         videos=vids(("NUlZbZ6Pv8c", "F38H-4A double-head bender — bed frames in square tube"), ("4lOXCjcIoK4", "F38 dual-head symmetric bender with punch")),
         specs={"kind": "table", "glance_keys": GK, "caps": {}, "note": "Capacities for round mild-steel tube; the working distance is the range of centre-to-centre spacing between the two bends; tools stack = number of dies stacked for that tube size.",
                "tables": [{"title": "F series", "sub": "Symmetric benders", "models": ["F38", "F50", "F38-90", "F38H-4A", "F38H-5A"], "rows": [
                    {"label": "Max. tube capacity", "sub": "OD × wall, mild steel", "key": True, "cells": ["Ø1-1/2″ × 12 ga (38.1 × 2.5 mm)", "Ø2″ × 14 ga (50 × 2 mm)", "Ø1-1/2″ × 12 ga (38.1 × 2.5 mm)", "Ø1-1/2″ × 12 ga (38 × 2.5 mm)", "Ø1-1/2″ × 12 ga (38 × 2.5 mm)"]},
                    {"label": "Centreline radius (CLR)", "sub": "", "key": True, "cells": [clr("38-180"), clr("40-250"), clr("38-180"), clr("38-180"), clr("38-180")]},
                    {"label": "Working distance", "sub": "between the two bends", "key": True, "cells": [clr("170-1500"), clr("200-2300"), clr("170-1500"), clr("250-4200"), clr("320-4200")]},
                    {"label": "Tools stack", "sub": "Ø3/4″ / Ø1″ / Ø1-1/4″ / Ø1-1/2″", "key": False, "cells": ["3-4 / 2-3 / 1-2 / 1", "4-5 / 3-4 / 2-3 / 1-2", "3-4 / 2-3 / 1-2 / 1", "3-4 / 2-3 / 1-2 / 1", "3-4 / 2-3 / 1-2 / 1"]},
                    {"label": "Multi-plane", "sub": "", "key": False, "cells": ["—", "—", "Manual", "—", "Automatic"]},
                    {"label": "Axes", "sub": "", "key": False, "cells": ["1", "1", "1", "2", "3"]}]}],
                "models": [{"name": "F38", "glance": ["Ø1-1/2″ × 12 ga", "7.1″ (180 mm)", "6.7 – 59″ span", "Symmetric, hydraulic, 1 axis", "—"]}, {"name": "F50", "glance": ["Ø2″ × 14 ga", "9.8″ (250 mm)", "7.9 – 90.6″ span", "Symmetric, hydraulic, 1 axis", "—"]},
                           {"name": "F38-90", "glance": ["Ø1-1/2″ × 12 ga", "7.1″ (180 mm)", "6.7 – 59″ span", "Symmetric, manual multi-plane", "—"]}, {"name": "F38H-4A", "glance": ["Ø1-1/2″ × 12 ga", "7.1″ (180 mm)", "9.8 – 165″ span", "Symmetric, servo feed, 2 axes", "—"]},
                           {"name": "F38H-5A", "glance": ["Ø1-1/2″ × 12 ga", "7.1″ (180 mm)", "12.6 – 165″ span", "Symmetric, servo feed + rotation, 3 axes", "—"]}]}),
    # ---------------------------------------------------------------- end forming page
    dict(id="csm-ef", group="csm-form", page=P_FORM, brand=BRAND,
         name="EF six-station tube end formers and REF / ER grooving and end-finishing machines, Ø13/16″ to Ø2″",
         short="EF end formers · REF / ER",
         models_label="EF20 · EF30 · EF50 · EF20VH – EF50VH · REF30 · REF40 · ER30-5 · 9 models",
         summary="CSM's end-finishing machines for the tube that comes off its benders: the EF series carries six forming stations on one "
                 "hydraulic ram — expand, reduce, bead, flare and flange in sequence without a tool change — for tube to Ø13/16″, Ø1-3/16″ and "
                 "Ø2″, in a horizontal (plane) or vertical (VH) layout; the REF 30 and REF 40 roll a groove into the tube end for O-ring and "
                 "clamp connections; the ER 30-5 does end forming, chamfering and grooving on one machine — the complex end-finish station of "
                 "an automated bending cell. PLC control with touch-screen, hydraulic clamping, servo feeding on the ER.",
         headline="Six forming stations · Ø13/16″ – Ø2″ · grooving to Ø1-9/16″ · end forming + chamfering + grooving",
         features=["EF: six forming stations on one ram — expand, reduce, bead, flare, flange without a tool change; plane (horizontal) or VH (vertical) layout",
                   "REF: rotary grooving for O-ring and clamp grooves, 3/16″ – 1/4″ forming stroke", "ER 30-5: end forming, chamfering and grooving in one cycle; trolley platform for moving between cells",
                   "Hydraulic clamping and forming; PLC with touch-screen; working height 39 – 49″", VOLT],
         optional=["Forming tools to your tube end", "Integration into a bending cell with robot transfer", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"],
         images=["cs-ef30", "cs-ref40", "cs-ref20", "cs-ef30-tools", "cs-er30", "cs-end-finishing", "cs-ref-part"],
         videos=vids(("e9XHHIUkZ-w", "EF50-6 six-station pipe end former"), ("TJ05JjjU64E", "ER30-5 five-head end forming machine"), ("htrLpOzBoGo", "ER30-5 pipe end former"),
                    ("iZON_5GTBcM", "18 MBE bender and EF50 end former in one cell")),
         specs={"kind": "table", "glance_keys": ["capacity", "detail", "motor", "weight"], "caps": {}, "note": "Capacities are the maximum tube outside diameter; forming stroke on the REF / ER is the depth of the groove or form.",
                "tables": [{"title": "EF", "sub": "Six-station end formers", "models": ["EF20", "EF30", "EF50", "EF20VH", "EF30VH", "EF50VH"], "rows": [
                    {"label": "Max. tube capacity", "sub": "OD", "key": True, "cells": [od(20), od(30), od(50), od(20), od(30), od(50)]},
                    {"label": "Forming stations", "sub": "", "key": True, "cells": ["6"] * 6},
                    {"label": "Layout", "sub": "", "key": False, "cells": ["Horizontal"] * 3 + ["Vertical"] * 3},
                    {"label": "Working height", "sub": "", "key": False, "cells": [mm_in(1220), mm_in(1220), mm_in(1250), mm_in(1220), mm_in(1220), mm_in(1250)]},
                    {"label": "Total power", "sub": "", "key": False, "cells": [hp(5.5), hp(5.5), hp(7.5), hp(5.5), hp(5.5), hp(7.5)]},
                    {"label": "Max. pressure", "sub": "", "key": False, "cells": [psi(170), psi(170), psi(170), psi(140), psi(140), psi(170)]}]},
                    {"title": "REF / ER", "sub": "Grooving and complex end-finishing", "models": ["REF30", "REF40", "ER30-5"], "rows": [
                    {"label": "Max. tube capacity", "sub": "OD", "key": True, "cells": [od(30), f"Ø1-9/16″ (40 mm)", od(30)]},
                    {"label": "Max. forming stroke", "sub": "", "key": True, "cells": ["1/4″ (6.5 mm)", "3/16″ (5 mm)", "1/4″ (6.5 mm)"]},
                    {"label": "Operations", "sub": "", "key": False, "cells": ["Grooving", "Grooving", "End forming, chamfering, grooving"]},
                    {"label": "Working height", "sub": "", "key": False, "cells": [mm_in(1060), mm_in(1210), mm_in(1000)]},
                    {"label": "Total power", "sub": "", "key": False, "cells": [hp(3.7), hp(4.4), hp(5.5)]},
                    {"label": "Max. pressure", "sub": "", "key": False, "cells": [psi(100), psi(70), psi(170)]}]}],
                "models": [{"name": m, "glance": g} for m, g in [("EF20", ["Ø13/16″", "6 stations, horizontal", hp(5.5), "—"]), ("EF30", ["Ø1-3/16″", "6 stations, horizontal", hp(5.5), "—"]), ("EF50", ["Ø2″", "6 stations, horizontal", hp(7.5), "—"]),
                                                                  ("EF20VH", ["Ø13/16″", "6 stations, vertical", hp(5.5), "—"]), ("EF30VH", ["Ø1-3/16″", "6 stations, vertical", hp(5.5), "—"]), ("EF50VH", ["Ø2″", "6 stations, vertical", hp(7.5), "—"]),
                                                                  ("REF30", ["Ø1-3/16″", "grooving, 1/4″ stroke", hp(3.7), "—"]), ("REF40", ["Ø1-9/16″", "grooving, 3/16″ stroke", hp(4.4), "—"]), ("ER30-5", ["Ø1-3/16″", "forming + chamfer + groove", hp(5.5), "—"])]]}),
    # ---------------------------------------------------------------- cold saws page
    dict(id="csm-ct325", group="csm-saw", page=P_SAW, brand=BRAND,
         name="CT325 hydraulic circular saws with servo feed, Ø1/2″ to Ø4″ tube and bundles",
         short="CT325 circular saws",
         models_label="CT325 L · M · H · 3 models",
         summary="The automatic circular saw CSM builds for its bending cells: hydraulic down-feed of a Ø10 – 12-3/4″ blade driven through "
                 "planetary gears, hydraulic clamping, a servo carriage that feeds the tube to ±0.004″ and a PLC with touch-screen — round, "
                 "square, rectangular and angle sections, single or in bundles with the customised vises. Three spindle-speed ranges for "
                 "steel (L), stainless and alloy (M) and aluminum and non-ferrous (H), all at 3.8 HP.",
         headline="Ø1/2″ – Ø4″ · bundle cutting · servo feed ±0.004″ · 3 speed ranges",
         features=["Hydraulic down-feed; blade driven through planetary transmission gears for low energy use", "Hydraulic clamping; feeding by servo motor to ±0.004″ at 39 in/s",
                   "Standard vises for Ø1-3/4″ – Ø4″; customised vises for Ø1/2″ – Ø2-1/2″ and bundle cutting", "PLC control with touch-screen; standing pedestal with emergency stop and remote control", VOLT],
         optional=["Bundle-cutting vises", "Saw blades for steel, stainless and aluminum", "Integration into a bending cell", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"],
         images=["cs-ct325", "cs-ct325-bundle", "cs-ct325-parts"],
         videos=vids(("Bf866DAmzuk", "CT325 automatic cold saw"), ("gRXc_HnOVCQ", "CT325 automatic circular saw"), ("H8WEu6EmeRk", "CT325 M automatic cold saw")),
         specs={"kind": "table", "glance_keys": ["blade", "round", "square", "installed_power", "weight"], "caps": {}, "note": "Capacities for mild steel (40 kgf/mm²); the three types differ in spindle speed range only.",
                "tables": [{"title": "CT325", "sub": "Hydraulic circular saws with servo feed", "models": ["CT325 L", "CT325 M", "CT325 H"], "rows": [
                    {"label": "Capacity, mild steel", "sub": "standard vises / customised vises", "key": True, "cells": ["Ø1-3/4″ – 4″ (44 – 101.6 mm) / Ø1/2″ – 2-1/2″ (12 – 63.5 mm)"] * 3},
                    {"label": "Saw blade", "sub": "", "key": True, "cells": ["Ø9-7/8″ – 12-3/4″ (250 – 325 mm)"] * 3},
                    {"label": "Spindle speed", "sub": "", "key": True, "cells": ["22 – 62 rpm", "47 – 135 rpm", "80 – 220 rpm"]},
                    {"label": "Total power", "sub": "", "key": False, "cells": ["3.8 HP (2.8 kW)"] * 3},
                    {"label": "Feeding speed / accuracy", "sub": "", "key": False, "cells": ["39 in/s (1,000 mm/s) / ±0.004″ (±0.1 mm)"] * 3},
                    {"label": "Working height", "sub": "", "key": False, "cells": [mm_in(950)] * 3},
                    {"label": "Dimensions L × W × H", "sub": "", "key": False, "cells": [dims(1700, 760, 1600)] * 3},
                    {"label": "Weight", "sub": "", "key": False, "cells": [lb(800)] * 3}]}],
                "models": [{"name": "CT325 L", "glance": ["Ø9-7/8″ – 12-3/4″", "Ø4″ (Ø1/2″ bundles)", "—", "3.8 HP · 22 – 62 rpm", lb(800)]},
                           {"name": "CT325 M", "glance": ["Ø9-7/8″ – 12-3/4″", "Ø4″ (Ø1/2″ bundles)", "—", "3.8 HP · 47 – 135 rpm", lb(800)]},
                           {"name": "CT325 H", "glance": ["Ø9-7/8″ – 12-3/4″", "Ø4″ (Ø1/2″ bundles)", "—", "3.8 HP · 80 – 220 rpm", lb(800)]}]}),
    # ---------------------------------------------------------------- wire bending page
    dict(id="csm-wb", group="csm-wire", page=P_WIRE, brand=BRAND,
         name="WB 10-A and WB 14-A CNC wire bending machines, Ø5/32″ to Ø9/16″ wire from coil",
         short="WB wire benders",
         models_label="WB 10-A · WB 14-A · 2 models",
         summary="A 3D CNC wire bender fed from the coil: the decoiler, hydraulic straightener and servo feeder bring the wire to a servo bending head "
                 "that bends at up to 1,000°/s with ±0.01° repeatability, rotates the work-head 440°/s for the next plane and shifts between "
                 "concentric tools, then a hydraulic cutter drops the finished part — baskets, racks, handles, hooks, springs, brackets and display "
                 "frames in Ø5/32″ to Ø3/8″ (WB 10-A) or Ø1/4″ to Ø9/16″ (WB 14-A) wire. The customised work-head avoids interference on "
                 "complex shapes; the IPC control with a 15″ touch-screen simulates the part in 3D before the first wire is bent.",
         headline="3D CNC from the coil · Ø5/32″ – Ø9/16″ · 1,000°/s · ±0.01°",
         features=["Bending by servo motor — 1,000°/s (WB 10-A) / 600°/s (WB 14-A), ±0.01° repeatability", "Work-head rotation by servo motor, 440°/s, ±0.01°; tooling shift by servo motor, concentric tool design",
                   "Feeding by servo motor at 164 ft/min, ±0.004″; straightening by hydraulics; uncoiling by AC motor", "Cutting by hydraulics; customised work-head eliminates interference",
                   "IPC control with 15″ touch-screen and 3D simulation", VOLT],
         optional=["Tooling to your wire and radii", "Decoiler for large coils", "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase"],
         images=["cs-wb10", "cs-wb-line", "cs-wb-screen"],
         videos=vids(("1g-E_smNt4E", "WB 14-A automatic wire bender with reel and straightener"), ("0Heyxw1glOI", "WB 14-A — furniture and chair wire parts"), ("elmlupJS1Bw", "WB 14-A furniture wire bending"),
                    ("MieZrMWJ9u8", "WB 14 wire bender and end former — exhaust hangers"), ("iTKgAHpHLZw", "WB + EF wire bending and end forming line"), ("IRi4s7epjGs", "WB 14-A with EF50 — exhaust hanger line")),
         specs={"kind": "table", "glance_keys": ["capacity", "detail", "motor", "weight"], "caps": {}, "note": "Bending capacity is the wire diameter in mild steel; the WB 14-A bends the larger wire at 600°/s.",
                "tables": [{"title": "WB", "sub": "CNC wire bending machines", "models": ["WB 10-A", "WB 14-A"], "rows": [
                    {"label": "Bending capacity", "sub": "wire OD", "key": True, "cells": ["Ø5/32″ – 3/8″ (4 – 10 mm)", "Ø1/4″ – 9/16″ (6 – 14 mm)"]},
                    {"label": "Bending speed / repeatability", "sub": "", "key": True, "cells": ["1,000°/s · ±0.01°", "600°/s · ±0.01°"]},
                    {"label": "Feeding speed / repeatability", "sub": "", "key": False, "cells": ["164 ft/min (50 m/min) · ±0.004″ (±0.1 mm)"] * 2},
                    {"label": "Work-head rotation speed / repeatability", "sub": "", "key": False, "cells": ["440°/s · ±0.01°"] * 2},
                    {"label": "Max. pressure", "sub": "", "key": False, "cells": [psi(140)] * 2},
                    {"label": "Total power", "sub": "", "key": False, "cells": [hp(13.4), hp(14.9)]},
                    {"label": "Dimensions L × W × H", "sub": "", "key": False, "cells": [dims(3450, 1300, 1715)] * 2},
                    {"label": "Weight", "sub": "", "key": False, "cells": [lb(2400)] * 2}]}],
                "models": [{"name": "WB 10-A", "glance": ["Ø5/32″ – 3/8″ wire", "1,000°/s · 3D CNC", hp(13.4), lb(2400)]}, {"name": "WB 14-A", "glance": ["Ø1/4″ – 9/16″ wire", "600°/s · 3D CNC", hp(14.9), lb(2400)]}]}),
]
