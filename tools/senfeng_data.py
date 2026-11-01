#!/usr/bin/env python3
"""Senfeng Laser (Jinan, China) — the value line below Dener on the laser pages, sold under the Senfeng brand.

Data from senfenglaserusa.com (imperial tables, the ones Senfeng USA publishes) with the metric figures from Senfeng's series
leaflets and the model numbers (3015 = 3,000 × 1,500 mm working area; 6024 = 6 m tube × Ø240 mm); shown as imperial (metric)
like the rest of the site.  The range is condensed — one family per machine type, every model of the type in its table.
Excluded on NovoTech's instruction: press brakes, CNC lathes and machining centres.

Pages fed from here: senfeng-fiber-lasers (sheet lasers, sheet + tube combo, large-format plate, 3D, coil-fed — under the
laser-cutting-machine hub) and senfeng-tube-lasers (two-chuck, high-speed / bevel, heavy-duty — under the tube-laser-cutting-machine
hub), both written by tools/senfeng_pages.py from the 'dener' family set; panel-bender (BDC, appended after the Dener group by
tools/dener_pages.py) and laser-welding-machine (handheld, robotic, cladding — tools/senfeng_pages.py).
"""
import re
from dener_data import inch, feet, length, tons, hp, speed, weight, dims, gal, mmin, table, spec, vids  # noqa: F401

BRAND = "senfeng"
P_LASER = "senfeng-fiber-lasers"
P_TUBE = "senfeng-tube-lasers"
P_PANEL = "panel-bender"
P_WELD = "laser-welding-machine"

VOLT = "208 / 240 / 480 / 600 V 3-phase 60 Hz (transformer supplied); single-phase not available"
# every Senfeng machine: "CE, FDA and ETL certified and CSA approved" (the owner, Nov 1 2026)
CERT = "CE, FDA and ETL certified and CSA approved"
POWER_NOTE = ("Laser source power is chosen at order (IPG, Raycus or Max sources); the model number is the metric working area "
              "(3015 = 3,000 × 1,500 mm) or, on tube lasers, the metric tube length × maximum diameter (6024 = 6 m × Ø240 mm). "
              "Speeds and accelerations are no-load values; platform loads are per table.")


def nom_ft(mm):
    """a table dimension in nominal feet (the owner, Nov 1 2026: "10 × 5 ft", not "9.8 ft × 4.9 ft · 118 × 59″"): whole feet when
    within 2 %, otherwise one decimal — 3,000 → 10, 1,500 → 5, 2,000 → 6.6, 2,500 → 8.2, 12,500 → 41"""
    f = mm / 304.8
    r = round(f)
    if r and abs(f - r) / r <= 0.02:
        return f"{r}"
    return f"{f:.1f}".rstrip("0").rstrip(".")


def area_in(l_in, w_in, model=None):
    """working area given in inches on the USA site → inches (or feet from 20 ft) with the metric size; the metric comes from the
    model number when it carries one (SF3015 → 3,000 × 1,500 mm), otherwise from the inches"""
    m = re.match(r"SF(\d{2,3})(\d{2})[A-Z]", model or "")
    if m:
        a, b = int(m.group(1)) * 100, int(m.group(2)) * 100
        L, W = max(a, b), min(a, b)  # SF1530 and SF3015 both mean 3,000 × 1,500 mm
    else:
        L, W = round(l_in * 25.4 / 10) * 10, round(w_in * 25.4 / 10) * 10
    return f"{nom_ft(L)} × {nom_ft(W)} ft ({L:,} × {W:,} mm)"          # nominal feet like the Dener tables (the owner, Nov 1 2026)


def n1(v):
    """one decimal, without a trailing .0"""
    return f"{v:.1f}".rstrip("0").rstrip(".")


def ftin(v_ft):
    return f"{v_ft:.1f} ft ({v_ft * 304.8 / 1000:.1f} m)"


def lb(v_lb):
    return f"{v_lb:,.0f} lb ({round(v_lb / 2.20462 / 10) * 10:,} kg)"


def ftmin(v):
    return f"{v:,.0f} ft/min ({round(v * 0.3048 / 5) * 5:g} m/min)"


def dims_in(l, w, h):
    return f"{l:.0f} × {w:.0f} × {h:.0f}″ ({round(l * 25.4 / 10) * 10:,} × {round(w * 25.4 / 10) * 10:,} × {round(h * 25.4 / 10) * 10:,} mm)"


def dims_ft(l, w, h):
    return f"{n1(l)} × {n1(w)} × {n1(h)} ft ({l * 0.3048:.1f} × {w * 0.3048:.1f} × {h * 0.3048:.1f} m)"


def dia(lo, hi):
    return f"Ø{lo:g} – {hi:g}″ (Ø{round(lo * 25.4):g} – {round(hi * 25.4):g} mm)"


def kw(lo, hi=None):
    return f"{lo:g} kW" if hi is None else f"{lo:g} – {hi:g} kW"


ACC = "±0.002″ (±0.05 mm) · repeat ±0.0008″ (±0.02 mm)"

# ------------------------------------------------------------------------------------------------ sheet lasers
# compact 5 × 10 ft single-table lasers G, N and NP: (model, kW lo, kW hi, L in, W in, speed ft/min, G, load lb, dims in (l,w,h), notes)
# — SF1530N and SF1530NP checked on senfenglaserusa.com (November 2026); the NP's Z travel, weight, protection, source, head and CNC
# from its 3 – 6 kW technical solution (the owner, Nov 1 2026).  The SF1313G has its own item below; the SFP precision lasers
# are no longer offered (the owner, Nov 1 2026).
COMPACT = [("SF1530G", 1.5, 4, 120, 60, 262, 1, 1543, (191, 159, 82), "full cover, single table"),
           ("SF1530N", 1.5, 12, 120, 60, 328, 1, 2425, (197, 91, 81), "full cover, pull-out single table"),
           ("SF1530NP", 1.5, 6, 119.2, 59.4, 328, 1, 2425, (193.7, 87.5, 91.2), "full cover, electric lifting door, integrated source")]
T_COMPACT = table("Compact single-table sheet lasers G · N · NP", "3 models · 5 × 10 ft · 1.5 – 12 kW", [r[0] for r in COMPACT], [
    ("Working area", [area_in(r[3], r[4], r[0]) for r in COMPACT]),
    ("Laser power", [kw(r[1], r[2]) for r in COMPACT]),
    ("Type", [r[9] for r in COMPACT]),
    ("Max. no-load speed", [ftmin(r[5]) for r in COMPACT]),
    ("Max. acceleration", [f"{r[6]:g} G" for r in COMPACT]),
    ("Positioning accuracy", [ACC] * len(COMPACT)),
    ("Max. table load", [lb(r[7]) for r in COMPACT]),
    ("Z travel", ["—", "—", "5.1″ (130 mm)"]),
    ("Machine weight", "by source power", ["—", "—", "10,381 lb (4,709 kg) at 3 kW · 11,530 lb (5,230 kg) at 6 kW with fire bricks"]),
    ("Laser source · cutting head", ["—", "—", "Maxphotonics · Raytools"]),
    ("CNC", ["FSCUT2000E", "FSCUT2000", "FSCUT"]),
    ("Power supply protection", ["—", "—", "IP54"]),
    ("Dimensions L × W × H", [dims_in(*r[8]) for r in COMPACT])])
# SF1313G 4 × 4 ft — its senfenglaserusa.com page and catalogue (the owner, Nov 1 2026)
T_1313G = table("SF1313G compact sheet laser", "4 × 4 ft · 1.5 – 3 kW · single table", ["SF1313G"], [
    ("Working area", ["4 × 4 ft (1,300 × 1,300 mm)"]),
    ("Laser power", ["1.5 – 3 kW"]),
    ("X / Y travel", ["4 × 4 ft"]),
    ("Z travel", ["4″ (100 mm)"]),
    ("Max. no-load speed", [ftmin(262)]),
    ("Max. acceleration", ["1 G"]),
    ("Positioning accuracy", [ACC]),
    ("Max. table load", ["485 lb (220 kg)"]),
    ("Max. cutting thickness", ["0.787″ (20 mm)"]),
    ("CNC", ["FSCUT2000"]),
    ("Dimensions L × W × H", ["118 × 85 × 79″ (2,985 × 2,160 × 2,000 mm)"])])

NP = [("SF3015NP", 120.1, 60.2, 2425, (177.2, 114.2, 82.7)), ("SF4015NP", 159.4, 60.2, 3086, (216.5, 114.2, 82.7)), ("SF4020NP", 159.4, 80, 4189, (216.5, 133.9, 74.8)),
      ("SF6015NP", 238.2, 60.2, 4630, (318.9, 114.2, 74.8)), ("SF6020NP", 238.2, 80, 6173, (318.9, 133.9, 74.8))]
T_NP = table("NP single-table sheet lasers with gantry cover", "5 models · 5 × 10 to 6.6 × 20 ft · 3 – 12 kW", [r[0] for r in NP], [
    ("Working area", [area_in(r[1], r[2], r[0]) for r in NP]),
    ("Laser power", ["3 – 12 kW"] * len(NP)),
    ("Max. no-load speed", [ftmin(394)] * len(NP)),
    ("Max. acceleration", ["1.2 G"] * len(NP)),
    ("Positioning accuracy", [ACC] * len(NP)),
    ("Max. table load", [lb(r[3]) for r in NP]),
    ("Dimensions L × W × H", [dims_in(*r[4]) for r in NP])])

HC = [("SF3015H", 120, 60.2, 2425, (27.9, 7.4, 7.1)), ("SF4015H", 159.4, 60.2, 3307, (35.8, 7.4, 7.2)), ("SF4020H", 159.4, 79.9, 4189, (36.2, 10.6, 7.4)),
      ("SF6015H", 238.1, 60.2, 4850, (48.3, 7.4, 7.2)), ("SF6020H", 238.1, 79.9, 6393, (48.8, 10.6, 7.4))]
T_HC = table("H series space-saver lasers · 1.5 – 12 kW", "5 models · 5 × 10 to 6.6 × 20 ft · pallet changer", [r[0] for r in HC], [
    ("Working area", [area_in(r[1], r[2], r[0]) for r in HC]),
    ("Laser power", ["1.5 – 12 kW"] * len(HC)),
    ("Max. no-load speed", [ftmin(426.5)] * len(HC)),
    ("Max. acceleration", ["1.2 G"] * len(HC)),
    ("Positioning accuracy", [ACC] * len(HC)),
    ("Max. table load", [lb(r[3]) for r in HC]),
    ("Z travel", ["8.7″ (220 mm)"] + ["—"] * 4),
    ("Machine weight", "by source power", ["11,552 – 11,729 lb (5,240 – 5,320 kg)"] + ["—"] * 4),
    ("Power supply protection", ["IP54"] + ["—"] * 4),
    ("Dimensions L × W × H", [dims_ft(*r[4]) for r in HC])])
H4 = [("SF3015H", 121.3, 60.2, 6614, (332.3, 89.4, 92.1)), ("SF4020H", 161.4, 80, 11023, (424.8, 125.2, 94.9)), ("SF6020H", 240.2, 80, 16645, (589.7, 125.2, 94.9)),
      ("SF6025H", 240.2, 100, 19842, (580.1, 148.9, 94.9)), ("SF8025H", 318.9, 100, 26455, (743.1, 148.9, 94.9)), ("SF12025H", 476.4, 100, 41579, (1093.3, 148.9, 94.9))]
T_H4 = table("H4 series high-power lasers · 6 – 30 kW", "6 models · 5 × 10 to 8.3 × 40 ft · pallet changer, 2 G", [r[0] for r in H4], [
    ("Working area", [area_in(r[1], r[2], r[0]) for r in H4]),
    ("Laser power", ["6 – 30 kW"] * len(H4)),
    ("Max. no-load speed", [ftmin(656)] * len(H4)),
    ("Max. acceleration", ["2.8 G"] + ["2 G"] * (len(H4) - 1)),
    ("Positioning accuracy", [ACC] + ["±0.004″ per 33 ft (±0.1 mm / 10 m) · repeat ±0.001″ (±0.02 mm)"] * (len(H4) - 1)),
    ("Max. table load", [lb(r[3]) for r in H4]),
    ("Z travel", ["15.4″ (390 mm)"] + ["—"] * (len(H4) - 1)),
    ("Machine weight", "by source power", ["13,735 – 15,763 lb (6,230 – 7,150 kg)"] + ["—"] * (len(H4) - 1)),
    ("Power supply protection", ["IP54"] + ["—"] * (len(H4) - 1)),
    ("Dimensions L × W × H", [dims_in(*r[4]) for r in H4])])
H5 = [("SF3015H5", 120, 60.2, "12 – 30 kW", 44092, (28.1, 9.4, 7.8)), ("SF4020H5", 159.4, 79.9, "40 – 80 kW", 66139, (35.2, 11.1, 7.8)), ("SF6025H5", 238.1, 99.6, "12 – 30 kW", 66139, (49.5, 12.7, 7.8))]
T_H5 = table("H5 heavy-load lasers · 12 – 80 kW", "3 models · hydraulic table lift to 30 t · 2″ plate", [r[0] for r in H5], [
    ("Working area", [area_in(r[1], r[2], r[0]) for r in H5]),
    ("Laser power", [r[3] for r in H5]),
    ("Max. no-load speed", [ftmin(656)] * 3),
    ("Positioning accuracy", [ACC] * 3),
    ("Hydraulic table lift", [lb(r[4]) for r in H5]),
    ("Dimensions L × W × H", [dims_ft(*r[5]) for r in H5])])

HM = [("SF3015HM", 120, 60.2, 6614, (30.3, 11.4, 7.7)), ("SF4020HM", 159.4, 79.9, 11023, (35.3, 14.1, 7.9)), ("SF6020HM", 238.1, 79.9, 16645, (49.1, 14.1, 7.9)), ("SF6025HM", 240.1, 99.6, 19842, (48.6, 16.0, 7.9))]
T_HM = table("HM sheet and tube combination lasers", "4 models · 5 × 10 to 8.3 × 20 ft sheet · Ø0.7 – 8.6″ × 20 ft tube · 6 – 30 kW", [r[0] for r in HM], [
    ("Sheet working area", [area_in(r[1], r[2], r[0]) for r in HM]),
    ("Tube diameter", [dia(0.7, 8.6)] * 4),
    ("Max. tube length", ["20 ft (6,000 mm)"] * 4),
    ("Laser power", ["6 – 30 kW"] * 4),
    ("Max. no-load speed", [ftmin(656)] * 4),
    ("Positioning accuracy", [ACC] * 4),
    ("Max. table load", [lb(r[3]) for r in HM]),
    ("Dimensions L × W × H", [dims_ft(*r[4]) for r in HM])])
# the medium-power SF3015HM, 1.5 – 6 kW, from its technical solution (the owner, Nov 1 2026)
T_HM_M = table("SF3015HM medium power, 1.5 – 6 kW", "from the SF3015HM technical solution · 5 kW steps 1.5 / 2 / 3 / 4 / 6 kW", ["SF3015HM 1.5 – 6 kW"], [
    ("Sheet working area", ["120.1 × 60.2″ (3,050 × 1,530 mm)"]), ("X / Y / Z travel", ["60.2 × 120.1 × 13.0″ (1,530 × 3,050 × 330 mm)"]),
    ("Tube diameter", ["Ø0.8 – 8.7″ (Ø20 – 220 mm)"]), ("Tube length", ["1.6 – 20 ft (500 – 6,000 mm)"]), ("Laser power", ["1.5 – 6 kW"]),
    ("Max. no-load speed", [ftmin(427)]), ("Max. acceleration", ["1 G"]), ("Positioning accuracy", [ACC]),
    ("Max. table load", ["2,425 lb (1,100 kg)"]), ("Machine weight", ["15,653 – 15,851 lb (7,100 – 7,190 kg)"]),
    ("Power supply protection", ["IP54"]), ("Dimensions L × W × H", [dims_ft(30.5, 11.4, 7.2)])])

R = [("SF6030R", 236.2, 118.1, "6 – 60 kW", 31184, (27.4, 15.6, 6.4)), ("SF8030R", 314.9, 118.1, "6 – 60 kW", 41570, (35.0, 15.6, 6.4)), ("SF12030R", 472.4, 118.1, "6 – 60 kW", 62355, (51.3, 15.6, 6.4)),
     ("SF14030R", 551.1, 118.1, "6 – 60 kW", 72741, (58.5, 15.6, 6.4)), ("SF24040R", 944.8, 157.4, "6 – 60 kW", 166156, (98.0, 15.6, 6.4)), ("SF30040R", 1181.1, 157.4, "6 – 60 kW", 103620, (121.3, 15.6, 6.4)),
     ("SF36030R", 1417.3, 118.1, "12 – 60 kW", 186982, (149.3, 15.6, 6.4)), ("SF50030R", 1968.5, 118.1, "12 – 60 kW", 259036, (206.7, 15.6, 6.4))]
T_R = table("R series ultra-large plate lasers", "8 models · 10 × 20 to 10 × 164 ft · 6 – 60 kW", [r[0] for r in R], [
    ("Working area", [area_in(r[1], r[2], r[0]) for r in R]),
    ("Laser power", [r[3] for r in R]),
    ("Max. no-load speed", [ftmin(393.7)] * len(R)),
    ("Positioning accuracy", ["±0.004″ per 33 ft (±0.1 mm / 10 m) · repeat ±0.002″ (±0.05 mm)"] * len(R)),
    ("Max. table load", [lb(r[4]) for r in R]),
    ("Dimensions L × W × H", [dims_ft(*r[5]) for r in R])])
TX = [("SF6030TX", 236.2, 118.1, 212.5, 78.7, 31184, (27.4, 15.6, 6.4)), ("SF8040TX", 314.9, 157.4, 291.3, 118.1, 55334, (35.0, 18.8, 6.4)), ("SF12030TX", 472.4, 118.1, 448.8, 78.7, 62355, (51.3, 15.6, 6.4)),
      ("SF14030TX", 551.1, 118.1, 527.5, 78.7, 72741, (58.5, 15.6, 6.4)), ("SF30040TX", 1181.1, 157.4, 1157.4, 118.1, 207235, (121.1, 18.8, 6.4)), ("SF36030TX", 1417.3, 118.1, 1393.7, 78.7, 186982, (149.3, 15.6, 6.4)),
      ("SF50030TX", 1968.5, 118.1, 1944.8, 78.7, 259036, (206.7, 15.6, 6.4))]
T_TX = table("TX series bevel plate lasers · ±45°", "7 models · 10 × 20 to 10 × 164 ft · 12 – 60 kW", [r[0] for r in TX], [
    ("Working area, straight cut", [area_in(r[1], r[2], r[0]) for r in TX]),
    ("Working area, bevel cut", [area_in(r[3], r[4], r[0]) for r in TX]),
    ("Laser power", ["12 – 60 kW"] * len(TX)),
    ("Bevel angle", ["±45°"] * len(TX)),
    ("Max. no-load speed", [ftmin(328)] * len(TX)),
    ("Max. table load", [lb(r[5]) for r in TX]),
    ("Dimensions L × W × H", [dims_ft(*r[6]) for r in TX])])
T_TXP = table("TXP laser and flame hybrid plate cutter", "1 model · 10 × 40 ft · 20 kW laser + oxy-fuel bevel torch", ["SF12030TXP"], [
    ("Working area, straight cut", [area_in(472.4, 118.1)]), ("Working area, bevel cut", [area_in(448.8, 78.7)]),
    ("Laser power", ["20 kW"]), ("Flame cutting", ["oxy-fuel torch for plate to 4″ (100 mm) with bevels"]),
    ("Max. no-load speed", [ftmin(328)]), ("Max. acceleration", ["0.8 G"]), ("Max. table load", [lb(62355)]), ("Dimensions L × W × H", [dims_ft(51.3, 15.6, 6.4)])])

T_3D = table("SF3015TD five-axis 3D laser", "1 model · 5 × 10 ft travel · 3 – 20 kW", ["SF3015TD"], [
    ("Travel range X × Y", [area_in(118.1, 59.0)]), ("Stroke X / Y / Z", ["118.1 × 59.1 × 27.6″ (3,000 × 1,500 × 700 mm)"]),
    ("Laser power", ["3 – 20 kW"]), ("A axis · C axis", ["±135° · n × 360° (endless)"]),
    ("Positioning accuracy", ["±0.004″ (±0.1 mm) · repeat ±0.002″ (±0.05 mm)"]), ("Max. no-load speed", [ftmin(328)]), ("Max. acceleration", ["1 G"]),
    ("Machine cooling", ["air-cooled"]), ("Worktable", ["180° dual-station rotary table, or dual-drive servo shuttle table"]),
    ("Dimensions L × W × H", [dims_ft(19.6, 9.1, 9.0)])])

# coil-fed lines, five series as Senfeng USA lists them (the owner, Nov 1 2026): the series pages on senfenglaserusa.com, the
# one-page leaflets and the "Sheet Coil Laser Blanking Line" brochure; where the pages and leaflets differ the USA page is used
CL_GK = ["thickness", "area", "power", "coil", "speed"]
CL_G_FROM = ["Coil thickness", "Working area", "Laser power", "Max. coil weight", "Max. feeding speed"]
T_COIL = table("SF1503CH coil-fed fiber laser", "1 model · thin coil 0.031 – 0.118″ · 5 × 10 ft · 3 – 6 kW", ["SF1503CH"], [
    ("Coil thickness", ["0.031 – 0.118″ (0.8 – 3 mm)"]), ("Working area", [area_in(118.1, 59.0)]),
    ("Coil inside Ø · max. outside Ø", ["Ø20″ (508 mm) · Ø55.1″ (1,400 mm)"]), ("Max. coil weight", ["16.5 US tons (15 t)"]),
    ("Max. feeding speed", [ftmin(49.2)]), ("Levelling accuracy", ["±0.00007 in/ft²"]), ("Laser power", ["3 – 6 kW"]),
    ("Positioning accuracy", [ACC])])
T_COIL_C = table("SF15015C open-style thin-sheet coil-fed laser", "1 model · coil 0.031 – 0.047″ · 5 × 10 ft · 1.5 – 3 kW", ["SF15015C"], [
    ("Coil thickness", ["0.031 – 0.047″ (0.8 – 1.2 mm)"]), ("Sheet width", ["31.4 – 59.0″ (800 – 1,500 mm)"]), ("Working area", [area_in(118.1, 59.0)]),
    ("Coil inside Ø · outside Ø", ["Ø20 or 24″ (508 / 610 mm) · Ø31.4 – 59.0″ (800 – 1,500 mm)"]),
    ("Max. coil weight", ["3, 8, 10 or 15 t (3.3 – 16.5 US tons)"]), ("Max. feeding speed", ["0 – 49 ft/min (0 – 15 m/min)"]),
    ("Sheet flatness", ["±0.079″ per ft² (±2 mm/m²)"]), ("Levelling rollers", ["11"]), ("Laser power", ["1.5 – 3 kW"]),
    ("Electro-optical efficiency", ["37 %"]), ("Positioning accuracy", [ACC])])
T_TOP = table("TOP series flexible metal processing line", "SF1503CH-TOP RC3000W · coil 0.024 – 0.079″ · 5 × 10 ft laser", ["SF1503CH-TOP RC3000W"], [
    ("Coil thickness", ["0.024 – 0.079″ (0.6 – 2 mm); max. coil 118.1 × 59.0 × 0.12″ (3,000 × 1,500 × 3 mm)"]),
    ("Coil width", ["23.6 – 59.1″ (600 – 1,500 mm)"]), ("Working area", [area_in(118.1, 59.0)]),
    ("Coil inside Ø · max. outside Ø", ["Ø20″ (508 mm) · Ø55.1″ (1,400 mm)"]), ("Max. coil weight", ["11 US tons (10 t)"]),
    ("Max. feeding speed", [ftmin(32.8)]), ("Levelling accuracy", ["±0.00007 in/ft²"]), ("Laser power", ["3 kW"]),
    ("Positioning accuracy", [ACC]),
    ("Stations", ["decoiler and leveller, laser cutting, robot unloading and sorting, panel bending, laser welding, stacking"])])
T_CLH = table("SF1503CLH aluminum coil-fed fiber laser", "1 model · aluminum coil 0.023 – 0.118″ · 6 kW", ["SF1503CLH"], [
    ("Coil thickness", ["0.023 – 0.118″ (0.6 – 3 mm)"]),
    ("Working area", [area_in(118.1, 59.0) + "; 19.7 × 4.9 ft (6,000 × 1,500 mm) long-table version"]),
    ("Coil inside Ø · max. outside Ø", ["Ø20″ (508 mm) · Ø55.1″ (1,400 mm)"]),
    ("Max. coil weight", ["11 US tons (10 t); 16.5 US tons (15 t) on the long-table version"]),
    ("Max. feeding speed", [ftmin(32.8)]), ("Levelling accuracy", ["±0.00005 in/ft²"]), ("Laser power", ["6 kW"]),
    ("Positioning accuracy", [ACC])])
T_COIL_HEAVY = table("SF2012CH coil-fed laser blanking line for thick coil", "1 model · coil 5/16 – 9/16″ · 13 × 6.6 ft · 12 – 80 kW", ["SF2012CH"], [
    ("Coil thickness", ["0.314 – 0.551″ (8 – 14 mm)"]), ("Working area", [area_in(157.4, 78.7)]),
    ("Coil inside Ø · outside Ø", ["Ø24 or 30″ (610 / 762 mm) · Ø39.3 – 70.8″ (1,000 – 1,800 mm)"]),
    ("Max. coil weight", ["22 US tons (20 t); the double-sided decoiler holds 66,138 lb (30 t)"]),
    ("Max. feeding speed", [ftmin(32.8)]), ("Levelling accuracy", ["±0.00019 in/ft²"]), ("Laser power", ["12 – 80 kW"]),
    ("Positioning accuracy", [ACC])])

# ------------------------------------------------------------------------------------------------ tube lasers
# (model, kW lo, kW hi, length lo ft, length hi ft, round lo, round hi, square hi, load lb, speed, rpm, dims)
T6 = [("SF6012T", 1.5, 3, 3.3, 21.3, 0.5, 4.7, 4.7, 265, 492, 180, (358.2, 70.8, 82.6)), ("SF6016T", 1.5, 3, 3.3, 21.3, 0.5, 6.6, 6.6, 353, 361, 140, (358.2, 70.8, 82.6)),
      ("SF6024T", 1.5, 6, 6.6, 21.3, 0.7, 9.0, 9.0, 573, 328, 100, (375.1, 76.7, 86.6)), ("SF6035T", 1.5, 6, 6.6, 20.3, 0.7, 14.1, 14.1, 1102, 197, 60, (374, 80.7, 100.3)),
      ("SF9024T", 1.5, 6, 6.6, 30, 0.7, 9.0, 9.0, 573, 328, 100, (493.3, 76.7, 86.6)), ("SF9035T", 1.5, 6, 6.6, 30, 0.7, 14.1, 14.1, 1102, 197, 60, (485, 80.7, 100.3)),
      ("SF12035T", 1.5, 6, 6.6, 40, 1.9, 13.7, 13.7, 1102, 197, 60, (603.5, 80.7, 100.3))]
T7 = [("SF7012T", 1.5, 3, 3.3, 23, 0.59, 4.72, 4.72, 265, 492, 180, (33.1, 5.9, 6.9)), ("SF7016T", 1.5, 3, 3.3, 23, 0.59, 6.69, 6.69, 353, 361, 140, (33.1, 5.9, 6.9)),
      ("SF7020T", 1.5, 6, 6.6, 23, 0.79, 8.66, 5.91, 441, 328, 100, (34.5, 6.4, 7.2)), ("SF7024T", 1.5, 6, 6.6, 23, 0.79, 9.06, 9.06, 573, 328, 100, (34.5, 6.4, 7.2)),
      ("SF7512T", 1.5, 3, 3.3, 24.6, 0.59, 4.72, 4.72, 265, 492, 180, (34.8, 5.9, 6.9)), ("SF7516T", 1.5, 3, 3.3, 24.6, 0.59, 6.69, 6.69, 353, 361, 140, (34.8, 5.9, 6.9)),
      ("SF7520T", 1.5, 6, 6.6, 24.6, 0.79, 8.66, 5.91, 441, 328, 100, (36.2, 6.4, 7.2)), ("SF7524T", 1.5, 6, 6.6, 24.6, 0.79, 9.06, 9.06, 573, 328, 100, (36.2, 6.4, 7.2))]


def tube_rows(data, dims_fn):
    return [("Tube length", [f"{r[3]:g} – {r[4]:g} ft ({round(r[3] * 304.8 / 100) / 10:g} – {round(r[4] * 304.8 / 100) / 10:g} m)" for r in data]),
            ("Round tube", [dia(r[5], r[6]) for r in data]),
            ("Square tube", [f"□{r[5]:g} – {r[7]:g}″ (□{round(r[5] * 25.4):g} – {round(r[7] * 25.4):g} mm)" for r in data]),
            ("Laser power", [kw(r[1], r[2]) for r in data]),
            ("Max. tube weight", [lb(r[8]) for r in data]),
            ("Max. no-load speed", [ftmin(r[9]) for r in data]),
            ("Max. chuck speed", [f"{r[10]} rpm" for r in data]),
            ("Positioning accuracy", ["±0.002″ (±0.05 mm) · repeat ±0.001″ (±0.03 mm)"] * len(data)),
            ("Dimensions L × W × H", [dims_fn(*r[11]) for r in data])]


T_T6 = table("T series two-chuck tube lasers · 20 – 40 ft", "7 models · Ø0.5 – 14.1″ · 1.5 – 6 kW", [r[0] for r in T6], tube_rows(T6, dims_in))
T_T7 = table("T series two-chuck tube lasers · 23 – 24.6 ft", "8 models · Ø0.6 – 9.1″ · 1.5 – 6 kW", [r[0] for r in T7], tube_rows(T7, dims_ft))

PLUS = [("SF6012PLUS", 3, 6, 3.3, 21.3, 0.5, 4.7, 4.7, 265, 394, 180, (29.8, 7.3, 7.5)), ("SF6016PLUS", 3, 6, 3.3, 21.3, 0.5, 6.6, 6.6, 331, 394, 180, (29.8, 7.3, 7.5)),
        ("SF6024PLUS", 3, 6, 3.3, 21.3, 0.7, 9.4, 9.4, 661, 492, 90, (30.5, 10.1, 8.2)), ("SF7012PLUS", 3, 6, 3.3, 23, 0.5, 4.7, 4.7, 265, 394, 180, (31.4, 7.3, 7.5))]
T_PLUS = table("PLUS series high-speed tube lasers", "4 models · Ø0.5 – 9.4″ · 20 – 23 ft · 3 – 6 kW", [r[0] for r in PLUS], tube_rows(PLUS, dims_ft))
GT = [("SF6012GPLUS", 1.5, 3, 3.3, 21.3, 0.6, 4.7, 4.7, 265, 492, 240, (358.3, 87.8, 90.6)), ("SF6024GT", 3, 6, 6.6, 21.3, 2.3, 9.0, 9.0, 573, 328, 100, (401.5, 89.7, 99.6)),
      ("SF6035GT", 3, 6, 6.6, 21, 3.1, 14.1, 14.1, 1102, 197, 60, (400.8, 88.8, 99.6))]
T_GT = table("GPLUS / GT bevel-cutting tube lasers · 45°", "3 models · Ø0.6 – 14.1″ · 20 ft · 1.5 – 6 kW", [r[0] for r in GT], tube_rows(GT, dims_in) + [("Bevel cutting", ["±45° on all four sides"] * 3)])

NT = [("SF6024NT", 3, 12, 9.8, 21.3, 0.7, 9.0, 9.0, 573, 246, 100, (543.3, 108.2, 124)), ("SF6035NT", 3, 6, 9.8, 20.3, 0.7, 14.1, 14.1, 1543, 197, 60, (543.3, 108.2, 131.8)),
      ("SF9024NT", 3, 6, 9.8, 30, 0.7, 9.0, 9.0, 573, 246, 100, (663.3, 108.2, 124)), ("SF9035NT", 3, 6, 9.8, 30, 0.7, 14.1, 14.1, 1543, 197, 60, (663.3, 108.2, 131.8)),
      ("SF12035NT", 3, 6, 9.8, 40, 1.9, 14.1, 14.1, 1543, 197, 60, (779.5, 108.2, 131.8))]
T_NT = table("NT series three-chuck zero-tailing tube lasers", "5 models · Ø0.7 – 14.1″ · 20 – 40 ft · 3 – 12 kW", [r[0] for r in NT], tube_rows(NT, dims_in))
ST = [("SF9035ST", 6, 20, 20, 30, 1.9, 14.1, 14.1, 2205, 197, 60, (60.7, 21.3, 14.7)), ("SF9050ST", 6, 20, 20, 30, 1.9, 19.6, 19.6, 4409, 131, 40, (62.3, 23.6, 13.7)),
      ("SF9056ST", 6, 20, 20, 30, 1.9, 22.0, 15.7, 3968, 98, 30, (62.3, 23.6, 13.7)), ("SF12035ST", 6, 20, 20, 40, 1.9, 14.1, 14.1, 2205, 197, 60, (70.5, 21.3, 14.7)),
      ("SF12050ST", 6, 20, 20, 40, 1.9, 19.6, 19.6, 4409, 131, 40, (72.1, 23.6, 13.7)), ("SF12056ST", 6, 20, 20, 40, 1.9, 22.0, 15.7, 3968, 98, 30, (72.1, 23.6, 13.7)),
      ("SF12065ST", 6, 20, 20, 40, 1.9, 25.1, 25.1, 6614, 98, 30, (72.1, 23.6, 13.7))]
T_ST = table("ST series three-chuck heavy-duty tube lasers", "7 models · Ø1.9 – 25.1″ · 30 – 40 ft · 6 – 20 kW", [r[0] for r in ST], tube_rows(ST, dims_ft))
HT = [("SF12035HT", 6, 20, 20, 40, 1.9, 14.1, 14.1, 2646, 197, 60, (93.5, 21.3, 14.7)), ("SF12050HT", 6, 20, 20, 40, 1.9, 19.6, 19.6, 4409, 131, 40, (95.1, 23.6, 13.7)),
      ("SF12056HT", 6, 20, 20, 40, 1.9, 22.0, 15.7, 3968, 98, 30, (95.1, 23.6, 13.7)), ("SF12065HT", 6, 20, 20, 40, 1.9, 25.1, 25.1, 6614, 98, 30, (95.1, 23.6, 13.7)),
      ("SF15056HT", 6, 20, 20, 49.2, 1.9, 22.0, 15.7, 3968, 98, 30, (118.1, 23.6, 13.7))]
T_HT = table("HT series four-chuck tube lasers", "5 models · Ø1.9 – 25.1″ · 39 – 49 ft · 6 – 20 kW", [r[0] for r in HT], tube_rows(HT, dims_ft))
T_CH = table("SF1500CH profile laser line for structural steel", "1 model · H-beams to 39 × 16 ft section, channels, angles · 12 – 30 kW", ["SF1500CH"], [
    ("Max. H-beam width · height", ["472″ (12,000 mm) · 197″ (5,000 mm)"]), ("Max. thickness", ["1.9″ (48 mm) straight · 1.3″ (32 mm) flange bevel"]),
    ("Laser power", ["12 – 30 kW"]), ("Positioning accuracy", ["±0.004″ (±0.1 mm) · repeat ±0.002″"]), ("Max. speed", [ftmin(164)]),
    ("Features", ["visual scanning of the beam, flange and web cutting, bevels, marking"])])

# ------------------------------------------------------------------------------------------------ welding & cladding
T_HW = table("S series portable air-cooled laser welders", "3 models · 0.8 – 1.5 kW · 99 – 121 lb", ["SF3S", "SF4S", "SF5S"], [
    ("Laser power", ["0.8 kW", "1.2 kW", "1.5 kW"]), ("Cooling", ["air-cooled — no chiller"] * 3), ("Wavelength", ["1,080 ± 10 nm"] * 3),
    ("Filler wire", ["0.03 – 0.06″ (0.8 – 1.6 mm)"] * 3), ("Welding gun", ["under 1.5 lb (0.7 kg)"] * 3), ("Gun cable", ["16.4 ft (5 m)", "23 ft (7 m)", "23 ft (7 m)"]),
    ("Machine weight", ["99 lb (45 kg)", "110 lb (50 kg)", "121 lb (55 kg)"]), ("Dimensions L × W × H", ["26.4 × 13.2 × 23.2″ (670 × 335 × 590 mm)"] * 3), ("Power supply", ["220 V single-phase"] * 3)])
T_HWM = table("HWM series handheld laser welders", "3 models · 1.5 – 3 kW · welds to 9/32″", ["SF1500HWM", "SF2000HWM", "SF3000HWM"], [
    ("Laser power", ["1.5 kW", "2 kW", "3 kW"]), ("Welding thickness", ["to 5/32″ (4 mm)", "to 3/16″ (5 mm)", "to 9/32″ (7 mm)"]), ("Wavelength", ["1,080 ± 10 nm"] * 3),
    ("Filler wire", ["0.03 – 0.06″ (0.8 – 1.6 mm)", "0.03 – 0.06″ (0.8 – 1.6 mm)", "0.03 – 0.08″ (0.8 – 2 mm)"]), ("Welding gun", ["under 1.5 lb (0.7 kg) · 4-in-1 head: weld, clean, cut, seam"] * 3),
    ("Gun cable", ["32.8 ft (10 m)"] * 3), ("Machine weight", ["485 lb (220 kg)", "485 lb (220 kg)", "584 lb (265 kg)"]),
    ("Dimensions L × W × H", ["37.6 × 28.2 × 42.5″ (954 × 715 × 1,080 mm)", "37.6 × 28.2 × 42.5″ (954 × 715 × 1,080 mm)", "47.6 × 28.2 × 42.5″ (1,210 × 715 × 1,080 mm)"]),
    ("Power supply", [VOLT] * 3)])
RW = [("SF1500RW", 1.5, 3, 2.2, 32.8), ("SF2000RW", 2, 4, 2.2, 32.8), ("SF3000RW", 3, 6, 2.2, 65.6), ("SF6000RW", 6, 7, 8, 65.6), ("SF12000RW", 12, 10, 8, 65.6), ("SF20000RW", 20, 14, 8, 65.6)]
T_RW = table("RW series robotic laser welding cells", "6 models · 1.5 – 20 kW · 6-axis robot", [r[0] for r in RW], [
    ("Laser power", [kw(r[1]) for r in RW]), ("Welding thickness", [f"to {r[2] / 25.4:.2g}″ ({r[2]} mm)" for r in RW]), ("Welding head", [f"to {r[3]:g} kg · wire feeder" for r in RW]),
    ("Robot", ["6 axes · 72″ (1,830 mm) reach · 25 kg payload"] * 6), ("Fiber length", [f"{r[4]:g} ft ({round(r[4] * 0.3048):g} m)" for r in RW]),
    ("Options", ["horizontal or dual-axis positioner, 7 – 9 axis cell with linear track, safety fencing"] * 6)])
T_ARC = table("Robotic arc welding machines", "3 models · 350 – 500 A MIG/MAG", ["SF-500RMW", "350CMW", "500CMW"], [
    ("Type", ["teaching-free robotic welder — scans the part and programs itself", "collaborative cobot welder on a mobile cart", "collaborative cobot welder on a mobile cart"]),
    ("Welding source", ["500 A MIG/MAG, water-cooled torch", "350 A, air-cooled torch", "500 A, water-cooled torch"]),
    ("Robot", ["6 axes · 83″ (2,116 mm) reach · 6 kg", "cobot · 53″ (1,350 mm) reach · 3 – 20 kg", "cobot · 53″ (1,350 mm) reach · 3 – 20 kg"]),
    ("Repeat accuracy", ["±0.003″ (±0.08 mm)", "±0.001″ (±0.03 mm)", "±0.001″ (±0.03 mm)"]),
    ("Welding table", ["3D fixture table (custom)", "59 × 59 × 26″ 3D flexible table", "59 × 59 × 26″ 3D flexible table"]),
    ("Total power", ["—", "16.5 kVA", "27 kVA"])])
T_CLAD = table("Laser cladding machines", "4 models · 6 / 12 kW · shafts, rolls, bores, on-site repair", ["SFR6063", "SFHS3050", "SFHS6050", "SFMR02"], [
    ("Type", ["robot cell with KUKA / FANUC robot", "lathe-type machine", "lathe-type machine", "portable robot system for on-site repair"]),
    ("Laser power", ["6 / 12 kW", "6 / 12 kW", "6 / 12 kW", "6 kW"]),
    ("Max. workpiece length", ["236″ (6,000 mm)", "118″ (3,000 mm)", "236″ (6,000 mm)", "robot reach 71″ (1,813 mm)"]),
    ("Max. swing · clamping Ø", ["Ø59 · Ø25″", "Ø31.5 · Ø31.5″", "Ø31.5 · Ø31.5″", "—"]),
    ("Max. table load", ["33,000 lb (15 t)", "4,400 lb (2 t)", "4,400 lb (2 t)", "—"]),
    ("Powder feeder", ["dual-cylinder pneumatic feeder, 20 – 300 µm powder, to 150 g/min"] * 4),
    ("Cladding head", ["high-speed cladding head; inner-bore head optional"] * 4)])

# ------------------------------------------------------------------------------------------------ panel benders
BDC = [("BDC1500", 59.06, 49.21, 13, 34.2, 13, (173, 78, 108)), ("BDC2000", 78.74, 49.21, 13, 36.5, 17, (196, 106, 116)), ("BDC2500", 98.43, 49.21, 13, 65, 22, (224, 125, 120)), ("BDC3200", 125.98, 49.21, 16, 80, 25, (259, 157, 129))]
T_BDC = table("BDC push-down automatic panel benders", "4 models · 59 – 126″ bend width · 14 ga mild steel", [r[0] for r in BDC], [
    ("Max. bending width", [f"{r[1]:.1f}″ ({round(r[1] * 25.4):,} mm)" for r in BDC]),
    ("Max. blank size L × W", [f"{r[1]:.0f} × {r[2]:.0f}″ ({round(r[1] * 25.4):,} × 1,250 mm)" for r in BDC]),
    ("Max. bending height", ["7.9″ (200 mm) · 11.8″ (300 mm) optional"] * 4),
    ("Max. thickness, mild steel", ["14 ga (2.0 mm)"] * 4), ("Max. thickness, stainless steel", ["16 ga (1.5 mm)"] * 4), ("Max. thickness, aluminum", ["3/32″ (2.5 mm)"] * 4),
    ("Min. thickness", ["0.014″ (0.35 mm)"] * 4), ("Bending speed", ["0.2 s per bend"] * 4), ("Servo axes", [str(r[3]) for r in BDC]),
    ("Installed power", [hp(r[4]) for r in BDC]), ("Dimensions L × W × H", [dims_in(*r[6]) for r in BDC]), ("Weight", [weight(r[5] * 1000) for r in BDC])])
T_BDC_S = table("BDC suction-cup panel benders", "2 models · 47 – 59″ bend width · thin sheet", ["BDC1200", "BDC1500"], [
    ("Max. bending width", ["47.2″ (1,200 mm)", "59.1″ (1,500 mm)"]), ("Max. blank size L × W", ["47 × 47″ (1,200 × 1,200 mm)", "59 × 49″ (1,500 × 1,250 mm)"]),
    ("Max. bending height", ["6.7″ (170 mm)"] * 2), ("Max. thickness, mild steel", ["20 ga (1.0 mm)"] * 2), ("Max. thickness, stainless steel", ["22 ga (0.8 mm)"] * 2),
    ("Max. thickness, aluminum", ["0.05″ (1.3 mm)"] * 2), ("Bending speed", ["0.2 s per bend"] * 2), ("Servo axes", ["10"] * 2), ("Installed power", [hp(30), hp(39)]),
    ("Dimensions L × W × H", [dims_ft(12.1, 5.9, 9.8), dims_ft(13.1, 6.5, 10.0)]), ("Weight", [weight(9000), weight(12000)])])

# ------------------------------------------------------------------------------------------------ glance keys
LZ_GK = ["area", "power", "speed", "load", "dims"]
LZ_G_FROM = ["Working area", "Laser power", "Max. no-load speed", "Max. table load", "Dimensions L × W × H"]
TB_GK = ["length", "round", "power", "load", "speed"]
TB_G_FROM = ["Tube length", "Round tube", "Laser power", "Max. tube weight", "Max. no-load speed"]
WD_GK = ["power", "thickness", "gun", "weight", "supply"]
WD_G_FROM = ["Laser power", "Welding thickness", "Welding gun", "Machine weight", "Power supply"]
PN_GK = ["bending_width", "thickness", "bending_height", "speed", "weight"]
PN_G_FROM = ["Max. bending width", "Max. thickness, mild steel", "Max. bending height", "Bending speed", "Weight"]

LZ_STD = ["Fiber laser source 1.5 – 80 kW (IPG, Raycus or Max) with the autofocus cutting head (Raytools / BOCI) and capacitive height sensing",
          "Bus-based CNC with a 21.5″ touchscreen (Cypcut / BOCHU), nesting software and a cutting-parameter database; one-click centring, collision avoidance",
          "Stress-relieved welded bed, aerospace-grade aluminum beam, Schneider servo drives, HIWIN / rack-and-pinion drives",
          "Zoned negative-pressure dust extraction under the table; double air ducts; water chiller included",
          "Intelligent air-cutting option: compressed air instead of nitrogen on sheet to about 3/8″", "CE, FDA and ETL certified and CSA approved; " + VOLT]
LZ_OPT = ["Loading / unloading unit, servo swing-arm loader or storage tower", "Automatic pallet changer (NP) and bevel head (R / TX)", "Dust collector and compressor sized to the machine",
          "Higher laser power at order; nitrogen generator", "Custom voltage transformer"]
TB_STD = ["Pneumatic self-centring chucks; following supports along the bed; automatic tube length measuring",
          "Fiber laser source 1.5 – 20 kW with autofocus head; bus-based CNC with tube nesting software and 3D import",
          "Safety fencing and light curtains; chip and part collection", "CE, FDA and ETL certified and CSA approved; " + VOLT]
TB_OPT = ["Automatic bundle loader and unloading conveyor", "45° bevel head (GPLUS / GT, ST / HT)", "Higher laser power; nitrogen generator; dust collector", "Custom voltage transformer"]

# ------------------------------------------------------------------------------------------------ intelligent air cutting
# the optional "AI Intelligent Air Cutting" tab on the H4, NP and R items (the owner, Nov 1 2026): from Senfeng's launch note,
# senfenglaser.com/knowledge/senfeng-intelligent-air-cutting and the three Senfeng USA air-cutting series pages
def air_tab(where):
    return dict(
        id="air-cut", label_pre="AI Intelligent", label_main="Air Cutting", title="AI Intelligent Air Cutting (optional)",
        lead="Senfeng's Intelligent Air Cutting, co-developed with BOCHU Automation for the H4, NP and R series from 6 to 60 kW, lets the "
             "laser cut with clean, dry compressed air from its own bus-connected compressor instead of bottled nitrogen or oxygen — and "
             "keeps oxygen and nitrogen for the jobs that need them. Hardware, control system, cutting software and service are upgraded "
             "together: faster, cleaner cuts at a much lower running cost, and simpler operation.",
        groups=[dict(title="Lower running cost", items=[
                    "Assist gas close to free — no nitrogen or oxygen to buy for most work; Senfeng quotes overall cutting expenses down by up to 92 %",
                    "15 kW high-efficiency air compressor with variable-frequency dust extraction: the whole machine uses 11.8 kWh less per "
                    "hour, 20.3 % less energy",
                    "Clean air protects the optics — protective-lens use drops from 5 a day to 2",
                    "No gas deliveries: no delays, shortages or price swings, even for shops far from a gas supplier"]),
                dict(title="Faster, cleaner cuts", items=[
                    "Carbon steel cuts much faster than with oxygen; thin-sheet throughput up by more than 30 %",
                    "Small heat-affected zone and little distortion, so less rework",
                    "Edges far less oxidized than oxygen cuts — many parts are welded or fitted straight from the machine, without grinding",
                    "Sharp corners without burning and well-formed small holes: a higher yield on complex parts",
                    "Little cutting fume, and no high-pressure gas cylinders to store or have inspected every year"]),
                dict(title="Everything on one control", items=[
                    "One screen starts and runs the laser, the air compressor and the dust collector",
                    "Variable-frequency dust extraction sets the fan to the material and the cutting speed",
                    "Sensors in the cutting head check the air for dirt, oil and moisture around the clock, and warn and stop the machine "
                    "before the lenses are damaged"]),
                dict(title="Control and AI", items=[
                    "Senfeng-exclusive BOCHU FSCUT8000 control, preloaded with the full 6 – 60 kW air-cutting process database",
                    "AI Process Cube (optional): scans the part and picks the best recipe from the process library in one click, reads a "
                    "photo of the cut edge for burrs, burning or incomplete cuts and corrects the parameters — setup time down by more "
                    "than 80 %, and new operators make good parts without an experienced programmer",
                    "Cuts carbon steel, stainless steel, aluminum and brass"])],
        note=where + " It needs Senfeng's intelligent air compressor and original Senfeng nozzles and lenses (third-party consumables "
                     "void the warranty). Ask NovoTech for sample cuts in your material and thickness.")


# ------------------------------------------------------------------------------------------------ families
LASER_FAMILIES = [
    dict(id="sf-compact", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="Compact single-table sheet lasers G, N and NP, 5 × 10 ft, 1.5 – 12 kW",
         short="Compact 5 × 10 ft lasers",
         models_label="SF1530G · SF1530N · SF1530NP",
         summary="The entry into production laser cutting: fully enclosed 5 × 10 ft single-table machines that ship in one 20 ft container "
                 "without disassembly, plug in and cut the day they arrive. The SF1530G takes 1.5 to 4 kW, the SF1530N with its pull-out "
                 "platform 1.5 to 12 kW — enough for 3/4″ mild steel at 6 kW — and the new-generation SF1530NP 1.5 to 6 kW, with the source "
                 "and a thermostatic electrical cabinet built in, an electric lifting door, integrated leg supports and a pick-up trolley "
                 "with an inner hopper. Smoke-free extraction through a double air duct with three zones and follow-up air valves, an "
                 "anti-burning platform, safety light curtains at the front and rear of the beam and smart cameras with a safety-lock "
                 "alarm; 328 ft/min, 1 G and 2,425 lb on the table (N and NP).",
         features=["1.5 – 12 kW; 5 × 10 ft single table; 262 – 328 ft/min, 1 G; 1,543 – 2,425 lb table load",
                   "SF1530NP: electric lifting door with CE protective acrylic laser shields and safety locks on both sides; source and "
                   "thermostatic electrical cabinet built in",
                   "Pull-out platform (N) or push-pull platform with integrated leg supports and a pick-up trolley with an inner hopper (NP)",
                   "Smoke-free extraction: double air duct, three zones and follow-up air valves; anti-burning platform protects the dust cover",
                   "Safety light curtains at the front and rear of the beam; smart cameras with a safety-lock alarm"] + LZ_STD,
         optional=LZ_OPT,
         extra_tabs=[air_tab("Offered on the compact machines with a 6 kW or larger source — the SF1530N and SF1530NP.")],   # (the owner, Nov 1 2026)
         images=["sf-1530np", "sf-1530np-showroom", "sf-1530np-side", "sf-1530np-2", "sf-1530np-trolley", "sf-1530np-head", "sf-1530np-safety",
                 "sf-1530np-cabinet", "sf-1530np-container",          # NP, then N, then G, each series together (the owner, Nov 1 2026)
                 "sf-1530n", "sf-1530n-rear", "sf-1530n-table",
                 "sf-1530g", "sf-1530g-table", "sf-1530-antiburn", "sf-1530-dust"],
         videos=[],
         # the SF1530NP 3 – 6 kW technical solution in NovoTech format (tools/brochure/senfeng_h_editions.py) — the owner, Nov 1 2026
         spec_pdf=dict(file="files/NovoTech-Senfeng-SF1530NP-Fiber-Laser-Technical-Specification-2026.pdf",
                       label="Download the SF1530NP full technical specification (3 – 6 kW)", size="PDF · 2.3 MB · imperial units",
                       cta="Download full technical specification"),
         specs=spec([T_COMPACT], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-np", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="NP single-table sheet lasers with gantry cover, 5 × 10 to 6.6 × 20 ft, 3 – 12 kW",
         short="NP lasers with gantry cover",
         models_label="SF3015NP – SF6020NP · 5 models",
         summary="A single-table laser with a laser cover on the gantry that travels with the head over the cut: the table stays open for "
                 "loading from three sides over ball-transfer units, the cover keeps the beam and the spatter in, and a built-in source and "
                 "cabinet and double ventilation ducts keep the machine clean. Five table sizes from 5 × 10 to 6.6 × 20 ft, 3 to 12 kW, 394 ft/min and 1.2 G; six 3015NP machines "
                 "fit in one 40 ft container, which is why it is the lowest-priced 12 kW laser in Senfeng's range. The intelligent "
                 "air-cutting package cuts sheet to 3/8″ on compressed air.",
         features=["3 – 12 kW; 5 × 10 to 6.6 × 20 ft; 394 ft/min, 1.2 G; 2,400 – 6,200 lb table load"] + LZ_STD,
         optional=LZ_OPT,
         extra_tabs=[air_tab("Offered on every NP size, SF3015NP to SF6020NP.")],
         images=["sf-np-1", "sf-np-2", "sf-np-3", "sf-np-4"],
         videos=[],
         specs=spec([T_NP], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-1313g", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="SF1313G compact fiber laser, 4 × 4 ft, 1.5 – 3 kW",
         short="4 × 4 ft SF1313G",
         models_label="SF1313G",
         summary="The smallest Senfeng laser, for the small shop: a fully enclosed single-table machine with a 4 × 4 ft working area and a "
                 "1.5 to 3 kW source that cuts small, thin and light parts at high precision. Laser energy is controlled to the sheet "
                 "thickness, so thin sheet comes out free of overburning and burr, and the compact custom source with anti-back-reflection "
                 "modules cuts aluminum, stainless, copper and brass with an electro-optical efficiency above 40 %. The sidewise push-pull "
                 "table saves floor space and makes loading easy, the zoned smoke exhaust follows the cut, and the whole machine — "
                 "118 × 85 × 79″ — ships in one 20 ft container without disassembly.",
         features=["1.5 – 3 kW; 4 × 4 ft (1,300 × 1,300 mm) single table; 262 ft/min; 485 lb table load; cuts sheet to 0.787″ (20 mm)",
                   "Fully enclosed with a top cover — no laser radiation outside the machine",
                   "Sidewise push-pull table: small footprint, easy loading and unloading",
                   "Zoned smoke exhaust synchronized with the cut keeps the shop clean",
                   "Compact custom source with anti-back-reflection modules for aluminum, stainless, copper and brass; electro-optical efficiency above 40 %",
                   "FSCUT2000 CNC with a cutting-process database for each thickness and material",
                   "Water chiller, transformer, voltage stabilizer and fan supplied",
                   CERT + "; " + VOLT],
         optional=["Dust collector and compressor sized to the machine", "Custom voltage transformer"],
         images=["sf-1313g-2", "sf-1313g-scene", "sf-1313g-front", "sf-1313g-3", "sf-1313g-4", "sf-1313g-head", "sf-1313g-samples",
                 "sf-1313g-table", "sf-1313g-container"],
         videos=[],
         # Senfeng's SF1313G catalogue in NovoTech format (tools/brochure/senfeng_h_editions.py) — the owner, Nov 1 2026
         pdf=dict(file="files/NovoTech-Senfeng-SF1313G-Fiber-Laser-2026.pdf", label="Download the SF1313G brochure", size="PDF · 1.3 MB · imperial units"),
         pdf_cta="Download SF1313G brochure",
         specs=spec([T_1313G], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-h", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="H series sheet lasers with pallet changer, 5 × 10 to 8.3 × 40 ft, 1.5 – 80 kW",
         short="H series production lasers",
         models_label="SF3015H – SF12025H · HC, H4 and H5 · 14 models",
         summary="Senfeng's production laser: a full-cover cabin, a double pallet changer that swaps tables in 20 seconds and a "
                 "thermally isolated hollow bed with graphite protection for high-power cutting. Three builds on the same platform — the "
                 "HC space saver with 1.5 to 12 kW in a 19 m² footprint, the fourth-generation H4 with 6 to 30 kW, 656 ft/min and up to 2.8 G on "
                 "tables to 8.3 × 40 ft, and the H5 heavy-load machine with hydraulic table lifts to 30 t for 40 to 80 kW sources and "
                 "2″ plate. CE / FDA / ETL certified and CSA approved, with loading towers, sheet storage and loading arms as options.",
         features=["Pallet changer, 20 s table exchange; 1.5 – 80 kW; 5 × 10 to 8.3 × 40 ft; to 656 ft/min and 2.8 G"] + LZ_STD,
         optional=LZ_OPT,
         extra_tabs=[air_tab("Offered on the H4 machines of this series.")],
         images=["sf-h-1", "sf-h-2", "sf-h5",                 # the owner's order, Nov 1 2026: machines, automation, air cutting, parts
                 "sf-h-tower", "sf-h-loader", "sf-h-swingarm", "sf-h-line",
                 "sf-h-air-1", "sf-h-air-2", "sf-h-air-3", "sf-h-air-4", "sf-h-air-5",
                 "sf-h-hollow-bed", "sf-h-beam", "sf-h-dust", "sf-h-door", "sf-h-zaxis", "sf-h-monitor", "sf-h-raycus",
                 "sf-h-max", "sf-h-boci", "sf-h-raytools", "sf-h-sample", "sf-h-sample-2"],
         videos=[],
         # Senfeng's two SF3015H technical solutions in NovoTech format (tools/brochure/senfeng_h_editions.py) — the owner, Nov 1 2026
         spec_pdfs=[dict(file="files/NovoTech-Senfeng-SF3015H-Medium-High-Power-Laser-Technical-Specification-2026.pdf",
                         label="Download the SF3015H medium and high power full technical specification (1.5 – 6 kW)",
                         size="PDF · 3.6 MB · imperial units", cta="Download full technical specification · 1.5 – 6 kW"),
                    dict(file="files/NovoTech-Senfeng-SF3015H-High-Power-Laser-Technical-Specification-2026.pdf",
                         label="Download the SF3015H high-power full technical specification (12 – 30 kW)",
                         size="PDF · 2.1 MB · imperial units", cta="Download full technical specification · 12 – 30 kW")],
         specs=spec([T_HC, T_H4, T_H5], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-hm", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="HM sheet and tube combination lasers, 5 × 10 to 8.3 × 20 ft sheet plus Ø8.6″ × 20 ft tube, 1.5 – 30 kW",
         short="Sheet + tube combo lasers",
         models_label="SF3015HM – SF6025HM · 4 models",
         # Senfeng USA's SF3015HM page and the SF3015HM technical solution (the owner, Nov 1 2026)
         summary="One machine for sheet and tube: the fully enclosed H series laser with a dual exchange table and, on the side, a rotary "
                 "chuck and tube supports for round, square and rectangular tube from Ø0.7 to 8.6″ and up to 20 ft long. The same source "
                 "and autofocus head serve both, so a shop cuts plate and tube on one machine at an affordable price, and the two exchange "
                 "tables load one sheet while the other is cut. Four sheet sizes from 5 × 10 to 8.3 × 20 ft with 6 to 30 kW, and the "
                 "SF3015HM also as a medium-power machine from 1.5 to 6 kW with its own full technical specification.",
         features=["Sheet 5 × 10 to 8.3 × 20 ft on a dual exchange table; tube Ø0.7 – 8.6″ × 20 ft; 1.5 – 30 kW; to 656 ft/min",
                   "Fully enclosed cabin around both tables — no laser radiation outside the machine",
                   "Autofocus cutting head sets the focus for each material and thickness",
                   "FSCUT3000 CNC for sheet and tube, with a cutting-process database for each thickness, sheet and tube",
                   "High-strength welded bed, annealed and aged; aircraft-grade aluminum beam; AVENTICS gas valves",
                   "Zoned negative-pressure dust extraction; modular sealed Z axis; water chiller included",
                   CERT + "; " + VOLT],
         optional=LZ_OPT + ["Tube bundle loader"],
         images=["sf-hm-1", "sf-hm-2", "sf-hm-3", "sf-hm-4", "sf-hm-5", "sf-hm-pdf", "sf-hm-head-6kw", "sf-hm-head-3kw", "sf-hm-source",
                 "sf-hm-bed", "sf-hm-beam", "sf-hm-gas", "sf-hm-dust", "sf-hm-zaxis"],
         videos=[],
         spec_pdf=dict(file="files/NovoTech-Senfeng-SF3015HM-Tube-Plate-Laser-Technical-Specification-2026.pdf",
                       label="Download the SF3015HM full technical specification (1.5 – 6 kW)", size="PDF · 3.3 MB · imperial units",
                       cta="Download full technical specification"),
         specs=spec([T_HM, T_HM_M], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-r", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="R / TX ultra-large plate lasers, 10 × 20 to 10 × 164 ft, 6 – 60 kW, ±45° bevel",
         short="Large-format plate lasers",
         models_label="SF6030R – SF50030R · SF6030TX – SF50030TX · SF12030TXP · 16 models",
         summary="For shipyards, structural steel, heavy equipment and bridge fabrication: gantry lasers with 10 and 13 ft wide tables from "
                 "20 to 164 ft long that replace plasma and flame cutting of plate to 2″ and beyond with 6 to 60 kW sources. The R series "
                 "cuts straight; the TX adds a ±45° bevel head for weld preparation in one pass; the TXP combines a 20 kW laser with an "
                 "oxy-fuel torch for plate to 4″ on the same table. Protective curtains, blow-suction dust collection under the slats and a "
                 "beam with a protective chamber are standard.",
         features=["10 × 20 to 10 × 164 ft tables; 6 – 60 kW; ±45° bevel (TX); laser + flame (TXP); 328 – 394 ft/min"] + LZ_STD,
         optional=LZ_OPT,
         extra_tabs=[air_tab("Offered on the R series plate lasers.")],
         images=["sf-r-1", "sf-tx-1", "sf-r-2", "sf-tx-2", "sf-txp", "sf-r-cut", "sf-tx-flame"],
         videos=[],
         specs=spec([T_R, T_TX, T_TXP], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-3d", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="3D laser cutting — five-axis SF3015TD, 5 × 10 ft, 3 – 20 kW",
         short="3D laser cutting",
         models_label="SF3015TD",
         # Senfeng USA's SF3015TD page, the SF3015TD leaflet and Senfeng's 3D five-axis catalogue; the RC robot cells are off the
         # site (the owner, Nov 1 2026)
         summary="Trimming and piercing formed parts: the SF3015TD carries a 3 to 20 kW five-axis head that turns endlessly (n × 360°) and "
                 "swings ±135° over a 5 × 10 ft envelope at 328 ft/min, so it cuts trim lines, holes and slots in hot-stamped, pressed and "
                 "drawn parts and pipe fittings where a flat-bed laser cannot reach — in place of trimming and piercing dies. A marble "
                 "base with marble guide rails and racks damps vibration for accuracy, the 180° dual-station rotary table loads one part "
                 "while the other is cut, and the fully enclosed cabin with interlocked doors and a light curtain keeps the operator out "
                 "of the work zone.",
         features=["Five-axis head: endless C rotation (n × 360°) and ±135° A swing; 3 – 20 kW; 5 × 10 ft travel, 27.6″ Z stroke; 328 ft/min, 1 G; air-cooled",
                   "Collision-proof, self-resetting 3D cutting head with autofocus and fast follow-up",
                   "Marble base with marble guide rails and racks — less resonance, more rigidity, higher positioning accuracy; modular build, easy to service",
                   "Senfeng 3D five-axis CNC with a cutting-process database, dual-screen monitoring, teaching, speed limiting and RTCP; offline "
                   "programming software from the 3D model; remote assistance module (optional)",
                   "180° dual-station rotary table, or a dual-drive servo high-speed shuttle table",
                   "Fully enclosed cabin with safety-interlocked doors and an intelligent light curtain",
                   "For hot-stamped and pressed automotive parts, pipe fittings, exhaust parts and stainless metalwork",
                   CERT + "; " + VOLT],
         optional=["Fixtures made for your parts", "Remote assistance module", "Dual-drive servo shuttle table in place of the rotary table"],
         images=["sf-3d-1", "sf-3d-2", "sf-3d-3", "sf-3d-rear", "sf-3d-head", "sf-3d-cut", "sf-3d-semi", "sf-3d-enclosed", "sf-3d-forming",
                 "sf-3d-pipe", "sf-3d-pressed", "sf-3d-metalwork"],
         videos=[],
         specs=spec([T_3D], ["area", "power", "speed", "axes", "dims"], ["Travel X × Y", "Laser power", "Max. no-load speed", "A axis · C axis", "Dimensions L × W × H"], POWER_NOTE)),
    dict(id="sf-coil", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="SF1503CH coil-fed fiber laser, thin coil 0.031 – 0.118″, 5 × 10 ft, 3 – 6 kW",
         short="SF1503CH coil-fed laser",
         models_label="SF1503CH",
         summary="Thin coil cut to net size with no sheet handling: a feeding trolley, single-support decoiler, leveller, positioning and "
                 "correction device and a 5 × 10 ft laser run on one control, so coil from 0.031 to 0.118″ (0.8 – 3 mm) and up to 16.5 US "
                 "tons goes from loading to finished blanks automatically. Levelling relieves the coil's internal stress for flatter sheet "
                 "and cleaner cuts, lead-screw correction rollers guide the strip without scratching it and position it without laser "
                 "edge-finding, and the line works at least 30 % faster than cutting sheets, with close to zero waste — on coil that costs "
                 "less than cut-to-length sheet. Made for high-variety, small-batch thin work: automotive sheet-metal parts, aluminum "
                 "veneer, electrical cabinets, metal doors, kitchenware and equipment enclosures.",
         features=["Coil 0.031 – 0.118″ (0.8 – 3 mm) to 16.5 US tons; 5 × 10 ft working area; feeding to 49 ft/min; 3 – 6 kW",
                   "Feeding trolley, single-support decoiler for 22,000 lb, auxiliary support, feeder, leveller, positioning and correction "
                   "device and laser on one electronic control",
                   "Stepless speed regulation: a geared motor drives the support roller so the strip hangs free between decoiler and feeder "
                   "and its stress is relieved",
                   "Ultra-precision correction: lead-screw-driven rollers straighten and guide the sheet without scratches and position it "
                   "without laser edge-finding",
                   "Process package for fast, mirror-finish cutting of thin stainless; at least 30 % faster than cutting sheets, close to zero waste",
                   CERT + "; " + VOLT],
         optional=["Automatic unloading, sorting and stacking", "Nesting software", "Custom voltage transformer"],
         images=["sf-coil-1", "sf-coil-ch-1", "sf-coil-ch-front", "sf-coil-ch-side", "sf-coil-ch-stack", "sf-coil-ch-sort", "sf-coil-scene", "sf-coil-parts"],
         videos=[],
         specs=spec([T_COIL], CL_GK, CL_G_FROM, POWER_NOTE)),
    dict(id="sf-coil-c", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="SF15015C open-style thin-sheet coil-fed laser, coil 0.031 – 0.047″, 5 × 10 ft, 1.5 – 3 kW",
         short="SF15015C thin-coil laser",
         models_label="SF15015C",
         summary="The affordable way into coil-fed cutting: an open-style, low-power line for regular-sized thin coil from 0.031 to 0.047″ "
                 "(0.8 – 1.2 mm) that loads, decoils, levels, feeds, cuts and unloads with basically no manual work. The leveller and the "
                 "cutter are built as one unit, so the line needs at most half the floor space of others and ships, installs and "
                 "commissions as one machine. Correcting rollers follow the coil's width for accurate positioning without scratches, the "
                 "control picks the assist gas and its pressure for each job, and Senfeng puts the total running cost about 10 % below "
                 "comparable lines — at least 30 % faster than before, with no coil wasted.",
         features=["Coil 0.031 – 0.047″ (0.8 – 1.2 mm), 31.4 – 59″ wide, 3 to 15 t; 5 × 10 ft working area; 1.5 – 3 kW at 37 % electro-optical efficiency",
                   "Fully automatic loading, decoiling, levelling, feeding, cutting and unloading — at least 30 % faster, no coil wasted",
                   "Leveller and cutter built as one unit: half the footprint, easier to ship, install and commission",
                   "Real-time correction rollers set the coil position by its width for accurate cuts without scratches",
                   "Assist gas and pressure chosen automatically; total running cost about 10 % below comparable lines",
                   "11 levelling rollers; feeding 0 – 49 ft/min",
                   CERT + "; " + VOLT],
         optional=["Longer unloading conveyor", "Custom voltage transformer"],
         images=["sf-coil-3", "sf-coil-c-1", "sf-coil-c-front", "sf-coil-c-2"],
         videos=[],
         specs=spec([T_COIL_C], CL_GK, CL_G_FROM, POWER_NOTE)),
    dict(id="sf-top", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="TOP series automated metal processing line — coil to cut, bent, welded and stacked parts",
         short="TOP automated line",
         models_label="SF1503CH-TOP RC3000W",
         summary="From coil to finished parts with no one at the machine: the TOP line puts a coil-fed laser, robot sorting, a panel "
                 "bending centre, a laser welding station and stacking in one line, so coil from 0.024 to 0.079″ is decoiled, levelled, "
                 "cut, unloaded, bent, welded and stacked in one run — 24/7 unmanned production at lower labour cost and consistent "
                 "quality. It is an open line: modules can be added for more processes as production changes, and any module or the whole "
                 "line connects to an MES for unified management. Several industrial robots move the parts and safety monitoring is built "
                 "in. For automotive, sheet-metal, furniture and signage work in mild and stainless steel, aluminum and brass.",
         features=["Coil 0.024 – 0.079″ (0.6 – 2 mm), 23.6 – 59.1″ wide, to 11 US tons; 5 × 10 ft laser, 3 kW; feeding to 33 ft/min",
                   "Decoiling, levelling, cutting, unloading, panel bending, laser welding and stacking in one line",
                   "Several industrial robots between the stations; built-in safety monitoring",
                   "Open line: add modules as production changes; each module or the whole line connects to an MES",
                   "High-power laser cutting, an automatic bending centre and a laser welding platform for the most output",
                   CERT + "; " + VOLT],
         optional=["Nesting software", "Film laminating", "Ink-jet marking", "Safety fencing"],
         images=["sf-coil-top", "sf-top-modules", "sf-top-1", "sf-top-3", "sf-top-cell", "sf-top-process", "sf-top-pendant"],
         videos=[],
         specs=spec([T_TOP], CL_GK, CL_G_FROM, POWER_NOTE)),
    dict(id="sf-coil-clh", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="SF1503CLH aluminum coil-fed fiber laser, coil 0.023 – 0.118″, 6 kW",
         short="SF1503CLH aluminum coil laser",
         models_label="SF1503CLH",
         summary="Made for aluminum coil: a decoiler, a high-precision straightener built for aluminum, a feeding system and a 6 kW laser "
                 "flatten the coil into sheet and cut it with no treatment in between, for coil from 0.023 to 0.118″ (0.6 – 3 mm). The "
                 "processes are coordinated so modules can be added for a chain from coil to finished product, the open system connects to "
                 "an MES, and a film laminating or a spraying machine can join the line. The laser source has protection against back "
                 "reflection for aluminum and other non-ferrous metals. For aluminum panels, kitchenware, doors, appliances and cabinets, "
                 "automotive components and construction machinery.",
         features=["Aluminum coil 0.023 – 0.118″ (0.6 – 3 mm) to 11 US tons; 10 × 5 ft working area (19.7 × 4.9 ft long-table version); 6 kW",
                   "High-precision straightener built for aluminum: the coil is flattened and cut with no treatment in between",
                   "Decoiler, straightener, feeding system and laser in one line; modules can be added from coil to finished product",
                   "Open system that connects to an MES",
                   "Laser source protected against back reflection from aluminum and other non-ferrous metals",
                   CERT + "; " + VOLT],
         optional=["Film laminating machine", "Spraying machine", "Custom voltage transformer"],
         images=["sf-coil-clh-1", "sf-coil-blank-line"],
         videos=[],
         specs=spec([T_CLH], CL_GK, CL_G_FROM, POWER_NOTE)),
    dict(id="sf-coil-2012", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="SF2012CH coil-fed laser blanking line for thick coil 5/16 – 9/16″, 13 × 6.6 ft, 12 – 80 kW",
         short="SF2012CH thick-coil line",
         models_label="SF2012CH",
         summary="Coil-fed cutting for medium-thick plate: Senfeng pushed coil thickness to 0.551″ (14 mm) and was the first to put it "
                 "into production. The SF2012CH combines a double-sided decoiler, a leveller, a 12 to 80 kW laser and automatic stacking for "
                 "0.314 to 0.551″ (8 – 14 mm) coil up to 22 US tons on a 13 × 6.6 ft working area. The double-sided decoiler holds up to "
                 "66,138 lb, so one loading runs for a long time; a positioning and correction device sets the plate precisely; the fully "
                 "enclosed laser keeps the fume in; and the line runs with close to zero waste. Coil costs less than cut plate, and the "
                 "line is made to the material. For sheet-metal processing, machinery, auto parts, electrical and elevator manufacturing, "
                 "petroleum and food machinery, and signage.",
         features=["Coil 0.314 – 0.551″ (8 – 14 mm) to 22 US tons; 13 × 6.6 ft (4,000 × 2,000 mm) working area; 12 – 80 kW; feeding to 33 ft/min",
                   "Double-sided decoiler holding up to 66,138 lb (30 t): one loading runs for hours",
                   "Plate positioning and correction device — a correction-roller slider and wheel set the plate precisely",
                   "Fully enclosed laser keeps the fume in; automatic stacking; fully automated for close to zero waste",
                   "Line made to the material: coil width, thickness and weight",
                   CERT + "; " + VOLT],
         optional=["Safety light curtain", "Nesting software", "Ink-jet marking", "Custom voltage transformer"],
         images=["sf-coil-2", "sf-coil-2012-1", "sf-coil-2012-2", "sf-coil-2012-3", "sf-coil-2012-4", "sf-coil-2012-5", "sf-coil-2012-decoiler",
                 "sf-coil-2012-head", "sf-coil-2012-waste"],
         videos=[],
         specs=spec([T_COIL_HEAVY], CL_GK, CL_G_FROM, POWER_NOTE)),
]

TUBE_FAMILIES = [
    dict(id="sf-t", group="tube-senfeng", page=P_TUBE, brand=BRAND,
         name="T series two-chuck tube lasers, Ø0.5 – 14″, 20 – 40 ft, 1.5 – 6 kW",
         short="T series tube lasers",
         models_label="SF6012T – SF12035T · SF7012T – SF7524T · 15 models",
         summary="The tube laser most shops start with: two pneumatic self-centring chucks, following supports, a 1.5 to 6 kW source and a "
                 "CNC with tube nesting that imports 3D files, cutting round, square, rectangular and profile tube to 14″ and 40 ft. "
                 "Fifteen models in two bed lengths — the 7 m / 7.5 m beds take 23 and 24.6 ft stock, the 6, 9 and 12 m beds 20, 29.5 "
                 "and 40 ft — with chucks for Ø4.7, 6.6, 9 and 14″. An automatic bundle loader and an unloading conveyor turn it into "
                 "an unattended cell.",
         features=["Ø0.5 – 14.1″ round, □0.5 – 14.1″ square; 20 – 40 ft; 1.5 – 6 kW; to 492 ft/min, 180 rpm"] + TB_STD,
         optional=TB_OPT,
         images=["sf-t-1", "sf-t-2", "sf-t-3", "sf-t-4", "sf-t-head", "sf-t-chuck", "sf-t-cutting", "sf-t-profiles", "sf-t-thickness"],
         videos=[],
         specs=spec([T_T6, T_T7], TB_GK, TB_G_FROM, POWER_NOTE)),
    dict(id="sf-plus", group="tube-senfeng", page=P_TUBE, brand=BRAND,
         name="PLUS high-speed and GPLUS / GT bevel-cutting tube lasers, Ø0.5 – 14″, 20 – 23 ft",
         short="High-speed & bevel tube lasers",
         models_label="SF6012PLUS – SF7012PLUS · SF6012GPLUS · SF6024GT · SF6035GT · 7 models",
         summary="The PLUS series is built for speed on small and medium tube: 394 to 492 ft/min, 180 rpm chucks and a 3 to 6 kW source for "
                 "furniture, fitness equipment and racking. The GPLUS and GT machines add a 45° bevel head that cuts weld preparations and "
                 "mitred corners on all four sides of the tube — the GPLUS for Ø0.6 to 4.7″ at 240 rpm, the GT for Ø2.3 to 14.1″ with a "
                 "bundle loader.",
         features=["PLUS: Ø0.5 – 9.4″, to 492 ft/min; GPLUS / GT: ±45° bevel, Ø0.6 – 14.1″; 1.5 – 6 kW"] + TB_STD,
         optional=TB_OPT,
         images=["sf-plus-1", "sf-gplus-1", "sf-gt-1", "sf-gt-2", "sf-plus-parts-1", "sf-plus-parts-2", "sf-plus-parts-3"],
         videos=[],
         specs=spec([T_PLUS, T_GT], TB_GK, TB_G_FROM, POWER_NOTE)),
    dict(id="sf-heavy", group="tube-senfeng", page=P_TUBE, brand=BRAND,
         name="NT / ST / HT three- and four-chuck tube lasers to Ø25″ and 49 ft, and the SF1500CH profile line",
         short="Heavy-duty tube lasers",
         models_label="SF6024NT – SF12035NT · SF9035ST – SF12065ST · SF12035HT – SF15056HT · SF1500CH · 18 models",
         summary="For long and heavy tube: the NT series puts a third chuck in the middle so the last piece is cut without a tail — zero "
                 "waste on 20 to 40 ft stock to Ø14″. The ST three-chuck and HT four-chuck machines carry tube to Ø25″ and 6,600 lb over "
                 "29 to 49 ft with 6 to 20 kW sources, bevel heads and automatic loaders, for structural steel, towers, cranes and "
                 "trailers. The SF1500CH is the profile line for H-beams to 39 × 16 ft section, channels and angles, with visual "
                 "scanning of each beam before cutting.",
         features=["NT: zero-tailing, Ø0.7 – 14.1″; ST / HT: Ø1.9 – 25.1″, 6 – 20 kW, to 6,600 lb; CH: H-beams to 1.9″ web"] + TB_STD,
         optional=TB_OPT,
         images=["sf-nt-1", "sf-st-1", "sf-ht-1", "sf-ch-1", "sf-nt-chucks", "sf-ht-tube", "sf-ch-scan", "sf-ch-render"],
         videos=[],
         specs=spec([T_NT, T_ST, T_HT, T_CH], TB_GK, TB_G_FROM, POWER_NOTE)),
]

PANEL_FAMILIES = [
    dict(id="sf-bdc", group="panel-senfeng", page=P_PANEL, brand=BRAND,
         name="BDC automatic panel benders, 47 – 126″ bend width — Senfeng",
         short="BDC panel benders",
         models_label="BDC1500 – BDC3200 push-down · BDC1200 / 1500 suction-cup · 6 models",
         summary="Senfeng's panel benders: the push-down BDC series with 13 to 16 servo axes bends mild steel to 14 ga, stainless to 16 ga "
                 "and aluminum to 3/32″ at 0.2 s per bend over 59 to 126″, with a 7.9″ bending height (11.8″ optional) and a sheet "
                 "manipulator that turns the blank for all four sides; the suction-cup BDC1200 and 1500 are the light machines for door "
                 "and appliance panels to 20 ga. Robot loading and unloading cells are available on the 1500 to 2500.",
         features=["0.2 s per bend; 14 ga mild steel; 59 – 126″ (push-down) or 47 – 59″ (suction-cup); auxiliary tools and clamps optional",
                   "Bus-based CNC with offline programming; automatic thickness compensation", "Safety fencing and light curtains", CERT + "; " + VOLT],
         optional=["6-axis robot loading / unloading cell (BDC1500 – 2500)", "Auxiliary bending tool and clamps", "300 mm bending height"],
         images=["sf-bdc-1", "sf-bdc-3", "sf-bdc-suction", "sf-bdc-robot", "sf-bdc-robot-2", "sf-bdc-tool", "sf-bdc-clamps", "sf-bdc-bends", "sf-bdc-parts", "sf-bdc-parts-2"],
         videos=[],
         specs=spec([T_BDC, T_BDC_S], PN_GK, PN_G_FROM, "Capacities are Senfeng's ratings; the model number is the metric bending width.")),
]

WELD_FAMILIES = [
    dict(id="sf-handheld", group="weld-handheld", page=P_WELD, brand=BRAND,
         name="Handheld laser welders, 0.8 – 3 kW — portable air-cooled S series and HWM series",
         short="Handheld laser welders",
         models_label="SF3S · SF4S · SF5S · SF1500HWM · SF2000HWM · SF3000HWM",
         summary="A handheld laser welder replaces TIG on stainless, aluminum, galvanized and carbon steel sheet: a 1.5 lb gun, a seam "
                 "five times faster than TIG, almost no heat distortion and no grinding afterwards — an operator learns it in a day. The "
                 "S series is the portable one: 0.8 to 1.5 kW, air-cooled, 99 to 121 lb on wheels, plugged into a 220 V outlet. The HWM "
                 "series brings 1.5 to 3 kW with a water chiller and a wire feeder for welds to 9/32″, and a 4-in-1 head that welds, "
                 "cleans, cuts and seam-welds. CE face shield, protective clothing and an optional welding booth come with it.",
         features=["S series: 0.8 / 1.2 / 1.5 kW air-cooled, 99 – 121 lb; HWM: 1.5 / 2 / 3 kW, welds to 9/32″, wire feeder",
                   "1.5 lb (0.7 kg) welding gun with wire feed; 16 – 33 ft cable", "Self-developed laser source and 4-in-1 welding head (weld, clean, cut, seam)",
                   "Safety: CE face shield, laser-resistant clothing and gloves supplied; optional booth with protective glass", "CE / FDA certified and CSA approved; S series 220 V single-phase, HWM 3-phase"],
         optional=["Laser welding booth", "Robot + handheld combination (robot CRP-RH18-20 with the same source)", "Cleaning head; extra wire feeder"],
         images=["sf-hwm-1", "sf-hw-1", "sf-hwm-gun", "sf-hw-gun", "sf-hwm-2", "sf-hw-weld", "sf-hwm-weld", "sf-hwm-weld-2", "sf-hw-safety", "sf-hw-booth", "sf-weld-samples"],
         videos=[],
         specs=spec([T_HW, T_HWM], WD_GK, WD_G_FROM, "Welding thickness is for a square butt weld in mild steel; stainless and aluminum run about 70 % of it.")),
    dict(id="sf-robot-weld", group="weld-robot", page=P_WELD, brand=BRAND,
         name="Robotic laser welding cells, 1.5 – 20 kW, and robotic arc welders",
         short="Robotic welding",
         models_label="SF1500RW – SF20000RW · SF-500RMW · 350CMW · 500CMW",
         summary="The RW series puts a fiber laser on a 6-axis robot with 72″ reach: 1.5 to 20 kW for sheet to 9/16″, with horizontal or "
                 "dual-axis positioners for tanks and tubes and 7 to 9-axis cells on a linear track. For MIG/MAG the RMW is a "
                 "teaching-free robot that scans the part and programs the weld itself, and the CMW is a collaborative robot on a mobile "
                 "cart with a 59 × 59″ 3D fixture table — 350 or 500 A, programmed by hand-guiding, moved to the job on wheels.",
         features=["RW: 6-axis robot, 1.5 – 20 kW, welds to 9/16″ (14 mm); positioners and linear tracks", "RMW: teaching-free 500 A MIG/MAG; CMW: cobot 350 / 500 A on a cart with 3D fixture table",
                   "Safety fencing, light curtains and fume extraction interfaces", CERT + "; " + VOLT],
         optional=["Horizontal or dual-axis positioner", "7 – 9 axis cells with linear track", "Second welding station; fume extraction"],
         images=["sf-rw-1", "sf-rw-2", "sf-rw-positioner", "sf-rw-cell", "sf-rmw-1", "sf-cmw-1", "sf-cmw-2"],
         videos=[],
         specs=spec([T_RW, T_ARC], ["power", "thickness", "robot", "fiber", "options"], ["Laser power", "Welding thickness", "Robot", "Fiber length", "Options"], "Robot reach and payload as listed; the RW cell is sized to the part at order.")),
    dict(id="sf-cladding", group="weld-cladding", page=P_WELD, brand=BRAND,
         name="Laser cladding machines, 6 / 12 kW — shafts, rolls, bores and on-site repair",
         short="Laser cladding",
         models_label="SFR6063 · SFHS3050 · SFHS6050 · SFMR02",
         summary="Laser cladding lays a metallurgically bonded wear or corrosion layer — up to 25/64″ thick — onto shafts, rolls, hydraulic "
                 "cylinders, valves and dies with far less heat than overlay welding and far better bonding than spraying. The SFR6063 "
                 "robot cell handles workpieces to 20 ft and 15 t on its table; the SFHS3050 and 6050 are lathe-type machines for shafts "
                 "to 10 and 20 ft; the SFMR02 is the portable system that goes to the machine for on-site repair. All with Senfeng's "
                 "high-speed cladding head, dual-cylinder powder feeder and an inner-bore head as an option.",
         features=["6 or 12 kW; high-speed cladding head; dual-cylinder pneumatic powder feeder, 20 – 300 µm, to 150 g/min", "KUKA / FANUC robot (SFR, SFMR) or lathe bed with Ø19.7″ three-jaw chuck (SFHS)",
                   "Coatings to 25/64″ (10 mm) with metallurgical bonding and small heat-affected zone", CERT + "; " + VOLT],
         optional=["Inner-bore cladding head", "Dual-axis positioner", "Powder recovery and fume extraction"],
         images=["sf-clad-1", "sf-clad-2", "sf-clad-3", "sf-clad-robot", "sf-clad-positioner", "sf-clad-head", "sf-clad-bore"],
         videos=[],
         specs=spec([T_CLAD], ["type", "power", "length", "load", "head"], ["Type", "Laser power", "Max. workpiece length", "Max. table load", "Cladding head"], "Workpiece sizes are the machine limits; cladding rates depend on the powder and layer thickness.")),
]

ALL = LASER_FAMILIES + TUBE_FAMILIES + PANEL_FAMILIES + WELD_FAMILIES

SERIES = {"sf-compact": "G · N · NP", "sf-1313g": "G", "sf-np": "NP", "sf-h": "H", "sf-hm": "HM", "sf-r": "R · TX · TXP", "sf-3d": "TD", "sf-coil": "CH", "sf-coil-c": "C", "sf-top": "TOP", "sf-coil-clh": "CLH", "sf-coil-2012": "CH",
          "sf-t": "T", "sf-plus": "PLUS · GT", "sf-heavy": "NT · ST · HT · CH", "sf-bdc": "BDC", "sf-handheld": "S · HWM", "sf-robot-weld": "RW · RMW · CMW", "sf-cladding": "SFR · SFHS · SFMR"}
for _f in ALL:
    _f["series"] = SERIES[_f["id"]]
