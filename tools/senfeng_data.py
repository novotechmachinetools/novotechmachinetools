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
POWER_NOTE = ("Laser source power is chosen at order (IPG, Raycus or Max sources); the model number is the metric working area "
              "(3015 = 3,000 × 1,500 mm) or, on tube lasers, the metric tube length × maximum diameter (6024 = 6 m × Ø240 mm). "
              "Speeds and accelerations are no-load values; platform loads are per table.")


def area_in(l_in, w_in, model=None):
    """working area given in inches on the USA site → inches (or feet from 20 ft) with the metric size; the metric comes from the
    model number when it carries one (SF3015 → 3,000 × 1,500 mm), otherwise from the inches"""
    m = re.match(r"SF(\d{2,3})(\d{2})[A-Z]", model or "")
    if m:
        a, b = int(m.group(1)) * 100, int(m.group(2)) * 100
        L, W = max(a, b), min(a, b)  # SF1530 and SF3015 both mean 3,000 × 1,500 mm
    else:
        L, W = round(l_in * 25.4 / 10) * 10, round(w_in * 25.4 / 10) * 10
    imp = f"{n1(l_in / 12)} × {n1(w_in / 12)} ft" if l_in >= 240 else f"{l_in:.0f} × {w_in:.0f}″"
    return f"{imp} ({L:,} × {W:,} mm)"


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
# compact: (model, kW lo, kW hi, L in, W in, speed ft/min, G, load lb, dims in (l,w,h), notes)
COMPACT = [("SF1313G", 1.5, 3, 51.2, 51.2, 262, 1, 485, (118, 85, 79), "enclosed, 4 × 4 ft, single table"),
           ("SF1530G", 1.5, 4, 120, 60, 262, 1, 1543, (191, 159, 82), "enclosed, single table"),
           ("SF1530N", 1.5, 12, 120, 60, 328, 1, 2425, (197, 91, 81), "enclosed, pull-out single table"),
           ("SF1530NP", 1.5, 6, 119.2, 59.4, 328, 1, 2425, (193.7, 87.5, 91.2), "fully enclosed, electric lifting door, integrated source")]
T_COMPACT = table("Compact enclosed sheet lasers", "4 models · 4 × 4 and 5 × 10 ft · 1.5 – 12 kW", [r[0] for r in COMPACT], [
    ("Working area", [area_in(r[3], r[4], r[0]) for r in COMPACT]),
    ("Laser power", [kw(r[1], r[2]) for r in COMPACT]),
    ("Type", [r[9] for r in COMPACT]),
    ("Max. no-load speed", [ftmin(r[5]) for r in COMPACT]),
    ("Max. acceleration", [f"{r[6]:g} G" for r in COMPACT]),
    ("Positioning accuracy", [ACC] * len(COMPACT)),
    ("Max. table load", [lb(r[7]) for r in COMPACT]),
    ("Dimensions L × W × H", [dims_in(*r[8]) for r in COMPACT])])
SFP = [("SFP600", 23.62, 1.4, (70.87, 56.3, 70.87)), ("SFP1010", 39.37, 3.0, (94.49, 82.28, 74.8)), ("SFP1250", 49.21, 3.5, (70.87, 56.3, 70.87))]
T_SFP = table("High-precision small-part lasers", "3 models · 24 – 49″ square tables · 1.5 – 3 kW", [r[0] for r in SFP], [
    ("Working area", [f"{r[1]:.1f} × {r[1]:.1f}″ ({round(r[1] * 25.4):,} × {round(r[1] * 25.4):,} mm)" for r in SFP]),
    ("Laser power", ["1.5 – 3 kW"] * 3),
    ("Z travel", ["3.9″ (100 mm)"] * 3),
    ("Positioning accuracy", ["±0.0008″ (±0.02 mm)", "±0.0012″ (±0.03 mm)", "±0.0008″ (±0.02 mm)"]),
    ("Repeat accuracy", ["±0.0002″ (±0.005 mm)"] * 3),
    ("Dimensions L × W × H", [dims_in(*r[3]) for r in SFP]),
    ("Weight", [weight(round(r[2] * 1000)) for r in SFP])])

NP = [("SF3015NP", 120.1, 60.2, 2425, (177.2, 114.2, 82.7)), ("SF4015NP", 159.4, 60.2, 3086, (216.5, 114.2, 82.7)), ("SF4020NP", 159.4, 80, 4189, (216.5, 133.9, 74.8)),
      ("SF6015NP", 238.2, 60.2, 4630, (318.9, 114.2, 74.8)), ("SF6020NP", 238.2, 80, 6173, (318.9, 133.9, 74.8))]
T_NP = table("NP open-type single-table sheet lasers", "5 models · 5 × 10 to 6.6 × 20 ft · 3 – 12 kW", [r[0] for r in NP], [
    ("Working area", [area_in(r[1], r[2], r[0]) for r in NP]),
    ("Laser power", ["3 – 12 kW"] * len(NP)),
    ("Max. no-load speed", [ftmin(394)] * len(NP)),
    ("Max. acceleration", ["1.2 G"] * len(NP)),
    ("Positioning accuracy", [ACC] * len(NP)),
    ("Max. table load", [lb(r[3]) for r in NP]),
    ("Dimensions L × W × H", [dims_in(*r[4]) for r in NP])])

HC = [("SF3015H", 120, 60.2, 2425, (27.9, 7.4, 7.1)), ("SF4015H", 159.4, 60.2, 3307, (35.8, 7.4, 7.2)), ("SF4020H", 159.4, 79.9, 4189, (36.2, 10.6, 7.4)),
      ("SF6015H", 238.1, 60.2, 4850, (48.3, 7.4, 7.2)), ("SF6020H", 238.1, 79.9, 6393, (48.8, 10.6, 7.4))]
T_HC = table("H series space-saver enclosed lasers · 1.5 – 12 kW", "5 models · 5 × 10 to 6.6 × 20 ft · pallet changer", [r[0] for r in HC], [
    ("Working area", [area_in(r[1], r[2], r[0]) for r in HC]),
    ("Laser power", ["1.5 – 12 kW"] * len(HC)),
    ("Max. no-load speed", [ftmin(426.5)] * len(HC)),
    ("Max. acceleration", ["1.2 G"] * len(HC)),
    ("Positioning accuracy", [ACC] * len(HC)),
    ("Max. table load", [lb(r[3]) for r in HC]),
    ("Dimensions L × W × H", [dims_ft(*r[4]) for r in HC])])
H4 = [("SF3015H", 121.3, 60.2, 6614, (332.3, 89.4, 92.1)), ("SF4020H", 161.4, 80, 11023, (424.8, 125.2, 94.9)), ("SF6020H", 240.2, 80, 16645, (589.7, 125.2, 94.9)),
      ("SF6025H", 240.2, 100, 19842, (580.1, 148.9, 94.9)), ("SF8025H", 318.9, 100, 26455, (743.1, 148.9, 94.9)), ("SF12025H", 476.4, 100, 41579, (1093.3, 148.9, 94.9))]
T_H4 = table("H4 series high-power enclosed lasers · 6 – 30 kW", "6 models · 5 × 10 to 8.3 × 40 ft · pallet changer, 2 G", [r[0] for r in H4], [
    ("Working area", [area_in(r[1], r[2], r[0]) for r in H4]),
    ("Laser power", ["6 – 30 kW"] * len(H4)),
    ("Max. no-load speed", [ftmin(656)] * len(H4)),
    ("Max. acceleration", ["2 G"] * len(H4)),
    ("Positioning accuracy", ["±0.004″ per 33 ft (±0.1 mm / 10 m) · repeat ±0.001″ (±0.02 mm)"] * len(H4)),
    ("Max. table load", [lb(r[3]) for r in H4]),
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
    ("Max. tube length", ["19.7 ft (6,000 mm)"] * 4),
    ("Laser power", ["6 – 30 kW"] * 4),
    ("Max. no-load speed", [ftmin(656)] * 4),
    ("Positioning accuracy", [ACC] * 4),
    ("Max. table load", [lb(r[3]) for r in HM]),
    ("Dimensions L × W × H", [dims_ft(*r[4]) for r in HM])])

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
T_TXP = table("TXP laser and flame hybrid plate cutter", "1 model · 10 × 39 ft · 20 kW laser + oxy-fuel bevel torch", ["SF12030TXP"], [
    ("Working area, straight cut", [area_in(472.4, 118.1)]), ("Working area, bevel cut", [area_in(448.8, 78.7)]),
    ("Laser power", ["20 kW"]), ("Flame cutting", ["oxy-fuel torch for plate to 4″ (100 mm) with bevels"]),
    ("Max. no-load speed", [ftmin(328)]), ("Max. acceleration", ["0.8 G"]), ("Max. table load", [lb(62355)]), ("Dimensions L × W × H", [dims_ft(51.3, 15.6, 6.4)])])

T_3D = table("SF3015TD five-axis 3D laser", "1 model · 5 × 10 ft travel · 3 – 20 kW", ["SF3015TD"], [
    ("Travel X × Y", [area_in(118.1, 59.0)]), ("Laser power", ["3 – 20 kW"]), ("A axis · C axis", ["±135° · n × 361°"]),
    ("Positioning accuracy", ["±0.004″ (±0.1 mm) · repeat ±0.002″ (±0.05 mm)"]), ("Max. no-load speed", [ftmin(328)]), ("Max. acceleration", ["1 G"]),
    ("Cooling", ["air-cooled head"]), ("Dimensions L × W × H", [dims_ft(19.6, 9.1, 9.0)])])
RC = [("SF1500RC", 1.5, 0.1, 32.8), ("SF2000RC", 2, 0.1, 32.8), ("SF3000RC", 3, 0.2, 65.6), ("SF6000RC", 6, 0.2, 65.6)]
T_RC = table("RC series robot laser cutting cells", "4 models · 6-axis robot · 1.5 – 6 kW", [r[0] for r in RC], [
    ("Laser power", [kw(r[1]) for r in RC]), ("Cutting thickness", [f"to {r[2]:g}″ ({round(r[2] * 25.4):g} mm)" for r in RC]),
    ("Robot", ["6 axes · 72.9″ (1,850 mm) reach · repeat ±0.0008″"] * 4), ("Fiber length", [f"{r[3]:g} ft ({round(r[3] * 0.3048):g} m)" for r in RC]),
    ("Robot weight", ["463 lb (210 kg)"] * 4)])

T_COIL = table("Coil-fed laser cutting lines", "3 lines · thin sheet to 9/16″ plate", ["SF15015C", "SF1503CH", "SF2012CH"], [
    ("Coil thickness", ["0.031 – 0.047″ (0.8 – 1.2 mm)", "to 1/8″ (3 mm)", "5/16″ – 9/16″ (8 – 14 mm)"]),
    ("Sheet width", ["31.4 – 59″ (800 – 1,500 mm)", "to 59″ (1,500 mm)", "to 78.7″ (2,000 mm)"]),
    ("Cutting area", ["open-type 5 × 10 ft laser", area_in(118.1, 59.0), area_in(157.4, 78.7)]),
    ("Laser power", ["1.5 – 6 kW", "3 – 6 kW", "12 – 80 kW"]),
    ("Coil inside Ø · max. outside Ø", ["20 / 24″ · 59″", "20″ · 55″", "24 / 30″ · 71″"]),
    ("Max. coil weight", ["3 – 15 t", "16.5 US tons (15 t)", "22 US tons (20 t)"]),
    ("Max. feeding speed", [ftmin(49.2), ftmin(49.2), ftmin(32.8)]),
    ("Levelling accuracy", ["±0.08″ per ft²", "±0.00007 in/ft²", "±0.0002 in/ft²"]),
    ("Positioning accuracy", ["—", "±0.00006 in/ft · repeat ±0.0008″", "±0.002″ · repeat ±0.0008″"])])

# ------------------------------------------------------------------------------------------------ tube lasers
# (model, kW lo, kW hi, length lo ft, length hi ft, round lo, round hi, square hi, load lb, speed, rpm, dims)
T6 = [("SF6012T", 1.5, 3, 3.3, 21.3, 0.5, 4.7, 4.7, 265, 492, 180, (358.2, 70.8, 82.6)), ("SF6016T", 1.5, 3, 3.3, 21.3, 0.5, 6.6, 6.6, 353, 361, 140, (358.2, 70.8, 82.6)),
      ("SF6024T", 1.5, 6, 6.6, 21.3, 0.7, 9.0, 9.0, 573, 328, 100, (375.1, 76.7, 86.6)), ("SF6035T", 1.5, 6, 6.6, 20.3, 0.7, 14.1, 14.1, 1102, 197, 60, (374, 80.7, 100.3)),
      ("SF9024T", 1.5, 6, 6.6, 29.5, 0.7, 9.0, 9.0, 573, 328, 100, (493.3, 76.7, 86.6)), ("SF9035T", 1.5, 6, 6.6, 29.5, 0.7, 14.1, 14.1, 1102, 197, 60, (485, 80.7, 100.3)),
      ("SF12035T", 1.5, 6, 6.6, 39.4, 1.9, 13.7, 13.7, 1102, 197, 60, (603.5, 80.7, 100.3))]
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


T_T6 = table("T series two-chuck tube lasers · 20 – 39 ft", "7 models · Ø0.5 – 14.1″ · 1.5 – 6 kW", [r[0] for r in T6], tube_rows(T6, dims_in))
T_T7 = table("T series two-chuck tube lasers · 23 – 24.6 ft", "8 models · Ø0.6 – 9.1″ · 1.5 – 6 kW", [r[0] for r in T7], tube_rows(T7, dims_ft))

PLUS = [("SF6012PLUS", 3, 6, 3.3, 21.3, 0.5, 4.7, 4.7, 265, 394, 180, (29.8, 7.3, 7.5)), ("SF6016PLUS", 3, 6, 3.3, 21.3, 0.5, 6.6, 6.6, 331, 394, 180, (29.8, 7.3, 7.5)),
        ("SF6024PLUS", 3, 6, 3.3, 21.3, 0.7, 9.4, 9.4, 661, 492, 90, (30.5, 10.1, 8.2)), ("SF7012PLUS", 3, 6, 3.3, 23, 0.5, 4.7, 4.7, 265, 394, 180, (31.4, 7.3, 7.5))]
T_PLUS = table("PLUS series high-speed tube lasers", "4 models · Ø0.5 – 9.4″ · 20 – 23 ft · 3 – 6 kW", [r[0] for r in PLUS], tube_rows(PLUS, dims_ft))
GT = [("SF6012GPLUS", 1.5, 3, 3.3, 21.3, 0.6, 4.7, 4.7, 265, 492, 240, (358.3, 87.8, 90.6)), ("SF6024GT", 3, 6, 6.6, 21.3, 2.3, 9.0, 9.0, 573, 328, 100, (401.5, 89.7, 99.6)),
      ("SF6035GT", 3, 6, 6.6, 21, 3.1, 14.1, 14.1, 1102, 197, 60, (400.8, 88.8, 99.6))]
T_GT = table("GPLUS / GT bevel-cutting tube lasers · 45°", "3 models · Ø0.6 – 14.1″ · 20 ft · 1.5 – 6 kW", [r[0] for r in GT], tube_rows(GT, dims_in) + [("Bevel cutting", ["±45° on all four sides"] * 3)])

NT = [("SF6024NT", 3, 12, 9.8, 21.3, 0.7, 9.0, 9.0, 573, 246, 100, (543.3, 108.2, 124)), ("SF6035NT", 3, 6, 9.8, 20.3, 0.7, 14.1, 14.1, 1543, 197, 60, (543.3, 108.2, 131.8)),
      ("SF9024NT", 3, 6, 9.8, 29.5, 0.7, 9.0, 9.0, 573, 246, 100, (663.3, 108.2, 124)), ("SF9035NT", 3, 6, 9.8, 29.5, 0.7, 14.1, 14.1, 1543, 197, 60, (663.3, 108.2, 131.8)),
      ("SF12035NT", 3, 6, 9.8, 39.4, 1.9, 14.1, 14.1, 1543, 197, 60, (779.5, 108.2, 131.8))]
T_NT = table("NT series three-chuck zero-tailing tube lasers", "5 models · Ø0.7 – 14.1″ · 20 – 39 ft · 3 – 12 kW", [r[0] for r in NT], tube_rows(NT, dims_in))
ST = [("SF9035ST", 6, 20, 19.6, 29.5, 1.9, 14.1, 14.1, 2205, 197, 60, (60.7, 21.3, 14.7)), ("SF9050ST", 6, 20, 19.6, 29.5, 1.9, 19.6, 19.6, 4409, 131, 40, (62.3, 23.6, 13.7)),
      ("SF9056ST", 6, 20, 19.6, 29.5, 1.9, 22.0, 15.7, 3968, 98, 30, (62.3, 23.6, 13.7)), ("SF12035ST", 6, 20, 19.6, 39.4, 1.9, 14.1, 14.1, 2205, 197, 60, (70.5, 21.3, 14.7)),
      ("SF12050ST", 6, 20, 19.6, 39.4, 1.9, 19.6, 19.6, 4409, 131, 40, (72.1, 23.6, 13.7)), ("SF12056ST", 6, 20, 19.6, 39.4, 1.9, 22.0, 15.7, 3968, 98, 30, (72.1, 23.6, 13.7)),
      ("SF12065ST", 6, 20, 19.6, 39.4, 1.9, 25.1, 25.1, 6614, 98, 30, (72.1, 23.6, 13.7))]
T_ST = table("ST series three-chuck heavy-duty tube lasers", "7 models · Ø1.9 – 25.1″ · 29 – 39 ft · 6 – 20 kW", [r[0] for r in ST], tube_rows(ST, dims_ft))
HT = [("SF12035HT", 6, 20, 19.6, 39.4, 1.9, 14.1, 14.1, 2646, 197, 60, (93.5, 21.3, 14.7)), ("SF12050HT", 6, 20, 19.6, 39.4, 1.9, 19.6, 19.6, 4409, 131, 40, (95.1, 23.6, 13.7)),
      ("SF12056HT", 6, 20, 19.6, 39.4, 1.9, 22.0, 15.7, 3968, 98, 30, (95.1, 23.6, 13.7)), ("SF12065HT", 6, 20, 19.6, 39.4, 1.9, 25.1, 25.1, 6614, 98, 30, (95.1, 23.6, 13.7)),
      ("SF15056HT", 6, 20, 19.6, 49.2, 1.9, 22.0, 15.7, 3968, 98, 30, (118.1, 23.6, 13.7))]
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
          "Intelligent air-cutting option: compressed air instead of nitrogen on sheet to about 3/8″", "CE, FDA and ETL certified; " + VOLT]
LZ_OPT = ["Loading / unloading unit, servo swing-arm loader or storage tower", "Automatic pallet changer (NP) and bevel head (R / TX)", "Dust collector and compressor sized to the machine",
          "Higher laser power at order; nitrogen generator", "Custom voltage transformer"]
TB_STD = ["Pneumatic self-centring chucks; following supports along the bed; automatic tube length measuring",
          "Fiber laser source 1.5 – 20 kW with autofocus head; bus-based CNC with tube nesting software and 3D import",
          "Safety fencing and light curtains; chip and part collection", "CE, FDA and ETL certified; " + VOLT]
TB_OPT = ["Automatic bundle loader and unloading conveyor", "45° bevel head (GPLUS / GT, ST / HT)", "Higher laser power; nitrogen generator; dust collector", "Custom voltage transformer"]

# ------------------------------------------------------------------------------------------------ families
LASER_FAMILIES = [
    dict(id="sf-compact", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="Compact enclosed sheet lasers, 4 × 4 and 5 × 10 ft, 1.5 – 12 kW",
         short="Compact sheet lasers",
         models_label="SF1313G · SF1530G · SF1530N · SF1530NP · SFP600 – 1250",
         summary="The entry into fiber laser cutting: single-table enclosed machines that ship in one container, plug in and cut the day they "
                 "arrive. The SF1313G is a 4 × 4 ft machine for small parts; the SF1530G, SF1530N and the fully enclosed SF1530NP with its "
                 "electric lifting door take a 5 × 10 ft sheet with 1.5 to 12 kW sources — enough for 3/4″ mild steel at 6 kW. The pull-out "
                 "table loads from the front with a forklift; the integrated source and cabinet keep the footprint under 200 × 90″. For "
                 "jewellery, electronics and precision small parts the SFP series adds 24 to 49″ square tables with ±0.005 mm repeatability.",
         features=["1.5 – 12 kW; 4 × 4 or 5 × 10 ft single table; 262 – 328 ft/min; 1,100 kg table load"] + LZ_STD,
         optional=LZ_OPT,
         images=["sf-1530np", "sf-1530n", "sf-1530g", "sf-1313g", "sf-1530n-table", "sf-1530np-2", "sf-1530np-head", "sf-sfp"],
         videos=[],
         specs=spec([T_COMPACT, T_SFP], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-np", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="NP open-type single-table sheet lasers, 5 × 10 to 6.6 × 20 ft, 3 – 12 kW",
         short="NP open-type lasers",
         models_label="SF3015NP – SF6020NP · 5 models",
         summary="The open-type laser for the shop that wants a 10 or 20 ft table without an enclosure: full visibility of the cut, loading from "
                 "three sides over ball-transfer units, a built-in source and cabinet, and double ventilation ducts that keep the open "
                 "machine clean. Five table sizes from 5 × 10 to 6.6 × 20 ft, 3 to 12 kW, 394 ft/min and 1.2 G; six 3015NP machines "
                 "fit in one 40 ft container, which is why it is the lowest-priced 12 kW laser in Senfeng's range. The intelligent "
                 "air-cutting package cuts sheet to 3/8″ on compressed air.",
         features=["3 – 12 kW; 5 × 10 to 6.6 × 20 ft; 394 ft/min, 1.2 G; 2,400 – 6,200 lb table load"] + LZ_STD,
         optional=LZ_OPT,
         images=["sf-np-1", "sf-np-2", "sf-np-3", "sf-np-4", "sf-np-scene"],
         videos=[],
         specs=spec([T_NP], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-h", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="H series enclosed sheet lasers with pallet changer, 5 × 10 to 8.3 × 40 ft, 1.5 – 80 kW",
         short="H series production lasers",
         models_label="SF3015H – SF12025H · HC, H4 and H5 · 14 models",
         summary="Senfeng's production laser: a fully enclosed cabin, a double pallet changer that swaps tables in 20 seconds and a "
                 "thermally isolated hollow bed with graphite protection for high-power cutting. Three builds on the same platform — the "
                 "HC space saver with 1.5 to 12 kW in a 19 m² footprint, the fourth-generation H4 with 6 to 30 kW, 656 ft/min and 2 G on "
                 "tables to 8.3 × 40 ft, and the H5 heavy-load machine with hydraulic table lifts to 30 t for 40 to 80 kW sources and "
                 "2″ plate. CE / FDA / ETL certified, with loading towers, sheet storage and loading arms as options.",
         features=["Pallet changer, 20 s table exchange; 1.5 – 80 kW; 5 × 10 to 8.3 × 40 ft; to 656 ft/min and 2 G"] + LZ_STD,
         optional=LZ_OPT,
         images=["sf-h-1", "sf-h-2", "sf-h-tower", "sf-h-loader", "sf-h-line", "sf-h5"],
         videos=[],
         specs=spec([T_HC, T_H4, T_H5], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-hm", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="HM sheet and tube combination lasers, 5 × 10 to 8.3 × 20 ft sheet plus Ø8.6″ × 20 ft tube, 6 – 30 kW",
         short="Sheet + tube combo lasers",
         models_label="SF3015HM – SF6025HM · 4 models",
         summary="One machine for sheet and tube: the enclosed H series laser with pallet changer and, on the side, a rotary chuck and tube "
                 "supports for round, square and rectangular tube from Ø0.7 to 8.6″ and up to 20 ft long. The same 6 to 30 kW source and "
                 "cutting head serve both; switching takes the time to load the tube. Four sheet sizes from 5 × 10 to 8.3 × 20 ft.",
         features=["Sheet 5 × 10 to 8.3 × 20 ft with pallet changer; tube Ø0.7 – 8.6″ × 20 ft; 6 – 30 kW; 656 ft/min"] + LZ_STD,
         optional=LZ_OPT + ["Tube bundle loader"],
         images=["sf-hm-1", "sf-hm-2", "sf-hm-3", "sf-hm-4"],
         videos=[],
         specs=spec([T_HM], LZ_GK, LZ_G_FROM, POWER_NOTE)),
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
         images=["sf-r-1", "sf-tx-1", "sf-r-2", "sf-tx-2", "sf-txp", "sf-r-cut", "sf-tx-flame"],
         videos=[],
         specs=spec([T_R, T_TX, T_TXP], LZ_GK, LZ_G_FROM, POWER_NOTE)),
    dict(id="sf-3d", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="3D laser cutting — five-axis SF3015TD and RC robot cells, 1.5 – 20 kW",
         short="3D laser cutting",
         models_label="SF3015TD · SF1500RC – SF6000RC",
         summary="Trimming and piercing formed parts: the SF3015TD five-axis machine moves a 3 to 20 kW head over a 5 × 10 ft envelope with "
                 "±135° A and endless C rotation at 328 ft/min for automotive, hot-stamping and pressing work; the RC series puts a 1.5 to "
                 "6 kW fiber head on a 6-axis robot with 72″ reach for parts to 0.2″ thick — the economical 3D cell for brackets, covers "
                 "and tube assemblies.",
         features=["Five-axis gantry 5 × 10 ft envelope, 3 – 20 kW, air-cooled head; robot cells 1.5 – 6 kW with 72″ reach"] + LZ_STD[:2],
         optional=["Rotary tables and fixtures", "Second robot station", "Safety enclosure with light curtains"],
         images=["sf-3d-1", "sf-3d-2", "sf-rc-1", "sf-rc-2", "sf-3d-head", "sf-3d-cut"],
         videos=[],
         specs=spec([T_3D, T_RC], ["area", "power", "speed", "axes", "dims"], ["Travel X × Y", "Laser power", "Max. no-load speed", "A axis · C axis", "Dimensions L × W × H"], POWER_NOTE)),
    dict(id="sf-coil", group="laser-senfeng", page=P_LASER, brand=BRAND,
         name="Coil-fed laser cutting lines, 0.03″ sheet to 9/16″ plate, 1.5 – 80 kW",
         short="Coil-fed laser lines",
         models_label="SF15015C · SF1503CH · SF2012CH · TOP line",
         summary="Cut straight from the coil: a decoiler, straightener and leveller feed the sheet onto the laser table so there is no sheet "
                 "handling, no offcuts and no limit on part length. The SF15015C runs thin coil (0.031 – 0.047″) through an open-type "
                 "laser; the SF1503CH takes coil to 1/8″ and 16.5 tons on a 5 × 10 ft machine; the SF2012CH levels and cuts 5/16″ to 9/16″ "
                 "plate from 22-ton coils with 12 to 80 kW. The TOP line adds robot sorting, panel bending and welding for a complete "
                 "coil-to-part cell.",
         features=["Decoiler, leveller and laser on one control; coil to 22 US tons; feeding to 49 ft/min; 1.5 – 80 kW"] + LZ_STD[:2],
         optional=["Robot sorting and stacking", "Panel bender and welding stations (TOP line)", "Stereo pallet racks"],
         images=["sf-coil-1", "sf-coil-2", "sf-coil-3", "sf-coil-top", "sf-coil-scene", "sf-coil-parts"],
         videos=[],
         specs=spec([T_COIL], ["thickness", "width", "power", "coil", "speed"], ["Coil thickness", "Sheet width", "Laser power", "Max. coil weight", "Max. feeding speed"], POWER_NOTE)),
]

TUBE_FAMILIES = [
    dict(id="sf-t", group="tube-senfeng", page=P_TUBE, brand=BRAND,
         name="T series two-chuck tube lasers, Ø0.5 – 14″, 20 – 39 ft, 1.5 – 6 kW",
         short="T series tube lasers",
         models_label="SF6012T – SF12035T · SF7012T – SF7524T · 15 models",
         summary="The tube laser most shops start with: two pneumatic self-centring chucks, following supports, a 1.5 to 6 kW source and a "
                 "CNC with tube nesting that imports 3D files, cutting round, square, rectangular and profile tube to 14″ and 39 ft. "
                 "Fifteen models in two bed lengths — the 7 m / 7.5 m beds take 23 and 24.6 ft stock, the 6, 9 and 12 m beds 20, 29.5 "
                 "and 39 ft — with chucks for Ø4.7, 6.6, 9 and 14″. An automatic bundle loader and an unloading conveyor turn it into "
                 "an unattended cell.",
         features=["Ø0.5 – 14.1″ round, □0.5 – 14.1″ square; 20 – 39 ft; 1.5 – 6 kW; to 492 ft/min, 180 rpm"] + TB_STD,
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
                 "waste on 20 to 39 ft stock to Ø14″. The ST three-chuck and HT four-chuck machines carry tube to Ø25″ and 6,600 lb over "
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
                   "Bus-based CNC with offline programming; automatic thickness compensation", "Safety fencing and light curtains; " + VOLT],
         optional=["6-axis robot loading / unloading cell (BDC1500 – 2500)", "Auxiliary bending tool and clamps", "300 mm bending height"],
         images=["sf-bdc-1", "sf-bdc-2", "sf-bdc-3", "sf-bdc-suction", "sf-bdc-robot", "sf-bdc-robot-2", "sf-bdc-tool", "sf-bdc-clamps", "sf-bdc-bends", "sf-bdc-parts", "sf-bdc-parts-2"],
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
                   "Safety: CE face shield, laser-resistant clothing and gloves supplied; optional booth with protective glass", "CE / FDA certified; S series 220 V single-phase, HWM 3-phase"],
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
                   "Safety fencing, light curtains and fume extraction interfaces; " + VOLT],
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
                   "Coatings to 25/64″ (10 mm) with metallurgical bonding and small heat-affected zone; " + VOLT],
         optional=["Inner-bore cladding head", "Dual-axis positioner", "Powder recovery and fume extraction"],
         images=["sf-clad-1", "sf-clad-2", "sf-clad-3", "sf-clad-robot", "sf-clad-positioner", "sf-clad-head", "sf-clad-bore"],
         videos=[],
         specs=spec([T_CLAD], ["type", "power", "length", "load", "head"], ["Type", "Laser power", "Max. workpiece length", "Max. table load", "Cladding head"], "Workpiece sizes are the machine limits; cladding rates depend on the powder and layer thickness.")),
]

ALL = LASER_FAMILIES + TUBE_FAMILIES + PANEL_FAMILIES + WELD_FAMILIES

SERIES = {"sf-compact": "G · N · NP · SFP", "sf-np": "NP", "sf-h": "H", "sf-hm": "HM", "sf-r": "R · TX · TXP", "sf-3d": "TD · RC", "sf-coil": "C · CH",
          "sf-t": "T", "sf-plus": "PLUS · GT", "sf-heavy": "NT · ST · HT · CH", "sf-bdc": "BDC", "sf-handheld": "S · HWM", "sf-robot-weld": "RW · RMW · CMW", "sf-cladding": "SFR · SFHS · SFMR"}
for _f in ALL:
    _f["series"] = SERIES[_f["id"]]
