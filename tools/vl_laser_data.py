#!/usr/bin/env python3
"""NovoTech value-line fiber lasers — sold under NovoTech's name, built in China to NovoTech's specification.

Sheet lasers: ULF open-type single-table (G and E builds, plus the large-format E machines to 26 × 3.2 m), ULE enclosed with
exchange table, ULFT open-type and ULET enclosed sheet-and-tube combinations.  Tube lasers: ULT two-chuck and three-chuck
(zero-tail) machines in four chuck sizes.  Metric data from the supplier's website tables (October 2026), its 2025 series
brochures and the ULE 3015 quotation NovoTech received; shown as imperial (metric) like the rest of the site.  Model numbers
are the supplier's: the working area in decimetres (3015 = 3,000 × 1,500 mm nominal), on tube lasers the bar length and the
chuck size (ULT6024A = 6 m bars, Ø240 mm chuck, version A).

ULG ground-rail plate lasers: data and photos from the supplier's ULG web page (October 2026), added at the user's request.
Left out on purpose: the ULH H-beam laser (the user does not want it on the site) and the ULJM precision laser (its published
working area and axis strokes contradict each other).

Pages fed from here: novotech-fiber-lasers (under the laser-cutting-machine hub) and novotech-tube-lasers (under the
tube-laser-cutting-machine hub), both written by tools/vl_laser_pages.py from the 'dener' family set, which
tools/dener_pages.py writes with these families included (the hubs read every laser family from that set).
"""
from dener_data import inch, feet, weight, mmin, table, spec  # noqa: F401

BRAND = "novotech"
P_SHEET = "novotech-fiber-lasers"
P_TUBE = "novotech-tube-lasers"

VOLT = "CSA-approved electrical panel, 600 V 3-phase standard (208 / 240 / 480 V on request)"
NOTE_SHEET = ("Laser source power is chosen at order (Raycus, MAX or IPG); the model number gives the nominal working area in "
              "decimetres (3015 = 3,000 × 1,500 mm). Speeds and accelerations are no-load values; the table load is the "
              "largest sheet the table carries, on the ULE for both exchange tables together.")
NOTE_TUBE = ("The model number gives the bar length and the chuck: ULT6024A = 6 m (20 ft) bars and the Ø240 mm chuck, version A; "
             "every chuck size is built for 6, 9 or 12 m bars (ULT6…, ULT9…, ULT12…). A and B are two chuck versions of the "
             "same size. Square and rectangular tube is limited by the chuck's square capacity; laser power is chosen at order.")


# ------------------------------------------------------------------------------------------------ units
def n1(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def area(l, w, inches=True):
    """working area like the Dener tables — feet, the inches (left out on the very long plate tables), the millimetres"""
    return f"{feet(l)} × {feet(w)}" + (f" · {l / 25.4:.0f} × {w / 25.4:.0f}″" if inches else "") + f" ({l:,} × {w:,} mm)"


def dims(l, w, h, ft=False):
    """one unit per table: inches for the small machines, feet for the long ones"""
    if not ft:
        return f"{l / 25.4:.0f} × {w / 25.4:.0f} × {h / 25.4:.0f}″ ({l:,} × {w:,} × {h:,} mm)"
    return f"{n1(l / 304.8)} × {n1(w / 304.8)} × {n1(h / 304.8)} ft ({l:,} × {w:,} × {h:,} mm)"


def mm_in(mm, nd=1):
    return f"{mm / 25.4:.{nd}f}″ ({mm:,} mm)"


def dia(lo, hi):
    return f"Ø{lo / 25.4:.1f} – {hi / 25.4:.1f}″ (Ø{lo} – {hi} mm)"


def acc_m(mm):
    """positioning accuracy given per metre → per foot alongside"""
    return f"±{mm:g} mm/m (±{mm * 0.3048 / 25.4:.4f}″/ft)".replace("0.000", ".000").replace("(±.", "(±0.")


def acc(mm, per=""):
    return f"±{mm / 25.4:.4f}″ (±{mm:g} mm{per})"


# ------------------------------------------------------------------------------------------------ ULF open-type single table
ULF_G = [("ULF-3015G", 3100, 1530, 900, (4700, 2345, 1850)), ("ULF-4015G", 4100, 1530, 1200, (6000, 2345, 1850)),
         ("ULF-6015G", 6100, 1530, 1800, (8300, 2345, 1850)), ("ULF-4020G", 4100, 2050, 1600, (6000, 2916, 1850)),
         ("ULF-6020G", 6100, 2050, 2400, (8300, 2916, 1850))]
T_ULF_G = table("ULF-G open-type fiber lasers · 1.5 – 6 kW", "5 models · 10 × 5 to 20 × 6.7 ft · single table", [r[0] for r in ULF_G], [
    ("Working area", [area(r[1], r[2]) for r in ULF_G]),
    ("Laser power", "1.5 – 6 kW"),
    ("Max. speed", "no load", mmin(90)),
    ("Max. speed with Delta servos", mmin(70)),
    ("Max. acceleration", "single axis", "1.4 G"),
    ("Positioning accuracy", acc_m(0.03)),
    ("Repeat accuracy", acc_m(0.02)),
    ("Z travel", mm_in(150)),
    ("Max. table load", [weight(r[3]) for r in ULF_G]),
    ("Dimensions L × W × H", [dims(*r[4]) for r in ULF_G])])

ULF_E = [("ULF-3015E", 3100, 1530, 1100, (4700, 2345, 1950)), ("ULF-4015E", 4100, 1530, 1500, (6000, 2345, 1950)),
         ("ULF-6015E", 6100, 1530, 2200, (8300, 2345, 1950)), ("ULF-4022E", 4100, 2200, 2000, (6000, 3250, 1950)),
         ("ULF-6022E", 6100, 2200, 3000, (8300, 3250, 1950))]
T_ULF_E = table("ULF-E open-type fiber lasers · 1.5 – 12 kW", "5 models · 10 × 5 to 20 × 7.2 ft · heavier build, 1.7 G", [r[0] for r in ULF_E], [
    ("Working area", [area(r[1], r[2]) for r in ULF_E]),
    ("Laser power", "1.5 – 12 kW"),
    ("Max. speed", "no load", mmin(140)),
    ("Max. speed with Delta servos", mmin(100)),
    ("Max. acceleration", "axes combined", "1.7 G"),
    ("Max. table load", [weight(r[3]) for r in ULF_E]),
    ("Dimensions L × W × H", [dims(*r[4]) for r in ULF_E])])

# (model, L, W, Z, positioning, repeat, accel, load kg, dims)
ULF_L = [("ULF-6026E", 6100, 2600, 250, acc(0.03), acc(0.02), "1.7 G", 3900, (8700, 3800, 2050)),
         ("ULF-8026E", 8000, 2600, 250, acc(0.04), acc(0.02), "1.7 G", 5200, (11000, 3800, 2050)),
         ("ULF-13026E", 13000, 2600, 250, acc(0.07), acc(0.03), "1.7 G", 14000, (16300, 3750, 2450)),
         ("ULF-13032E", 13000, 3200, 200, acc(0.07), acc(0.03), "1.4 G", 18000, (16500, 4350, 2450)),
         ("ULF-26026E", 26000, 2600, 250, acc(0.07, " per 10 m"), acc(0.05), "1.7 G", 28000, (31000, 3750, 2450)),
         ("ULF-26032E", 26000, 3200, 200, acc(0.07, " per 10 m"), acc(0.05), "1.4 G", 36000, (31500, 4350, 2450))]
T_ULF_L = table("ULF-E large-format plate lasers · 6 – 60 kW", "6 models · 20 × 8.5 to 85 × 10.5 ft", [r[0] for r in ULF_L], [
    ("Working area", [area(r[1], r[2], inches=False) for r in ULF_L]),
    ("Laser power", "6 – 60 kW"),
    ("Max. speed", "no load", mmin(140)),
    ("Max. acceleration", [r[6] for r in ULF_L]),
    ("Positioning accuracy", [r[4] for r in ULF_L]),
    ("Repeat accuracy", [r[5] for r in ULF_L]),
    ("Z travel", [mm_in(r[3]) for r in ULF_L]),
    ("Max. table load", [weight(r[7]) for r in ULF_L]),
    ("Dimensions L × W × H", [dims(*r[8], ft=True) for r in ULF_L])])

# ------------------------------------------------------------------------------------------------ ULE enclosed, exchange table
# (model, L, W, load both tables kg (single chain), dims, delta speed)
ULE_S = [("ULE-3015E", 3100, 1550, 1500, (8800, 2950, 2300), 100), ("ULE-4015E", 4100, 1550, 1900, (10800, 2950, 2300), 100),
         ("ULE-4020E", 4100, 2050, 2600, (10800, 3500, 2300), None), ("ULE-6020E", 6100, 2050, 4000, (15000, 3500, 2300), None)]
T_ULE_S = table("ULE enclosed exchange-table fiber lasers · 3 – 20 kW", "4 models · 10 × 5 to 20 × 6.7 ft · table swap in 15 s", [r[0] for r in ULE_S], [
    ("Working area", [area(r[1], r[2]) for r in ULE_S]),
    ("Laser power", "3 – 20 kW"),
    ("Max. speed", "no load", mmin(140)),
    ("Max. speed with Delta servos", [mmin(r[5]) if r[5] else "—" for r in ULE_S]),
    ("Max. acceleration", "1.7 G"),
    ("Positioning accuracy", acc_m(0.03)),
    ("Repeat accuracy", acc_m(0.02)),
    ("Z travel", mm_in(300)),
    ("Max. table load", "both tables, single chain", [weight(r[3]) for r in ULE_S]),
    ("Max. table load, twin chain", "both tables", [weight(2 * r[3]) for r in ULE_S]),
    ("Table exchange", "15 s"),
    ("Dimensions L × W × H", [dims(*r[4], ft=True) for r in ULE_S])])
ULE_L = [("ULE-6026E", 6100, 2600, acc(0.03), acc(0.02), 6200, (15000, 4250, 2700)),
         ("ULE-8026E", 8100, 2600, acc(0.04), acc(0.02), 8200, (19500, 4250, 2700)),
         ("ULE-12526E", 12500, 2600, acc(0.03) + " · Y axis " + acc(0.06), acc(0.03), 12500, (27500, 4250, 2700))]
T_ULE_L = table("ULE large-format exchange-table fiber lasers · 6 – 40 kW", "3 models · 20 × 8.5 to 41 × 8.5 ft", [r[0] for r in ULE_L], [
    ("Working area", [area(r[1], r[2], inches=False) for r in ULE_L]),
    ("Laser power", "6 – 40 kW"),
    ("Max. speed", "no load", mmin(140)),
    ("Max. acceleration", "1.7 G"),
    ("Positioning accuracy", [r[3] for r in ULE_L]),
    ("Repeat accuracy", [r[4] for r in ULE_L]),
    ("Z travel", mm_in(420)),
    ("Max. table load", "both tables, single chain", [weight(r[5]) for r in ULE_L]),
    ("Max. table load, twin chain", "both tables", [weight(2 * r[5]) for r in ULE_L]),
    ("Table exchange", "15 s"),
    ("Dimensions L × W × H", [dims(*r[6], ft=True) for r in ULE_L])])

# ------------------------------------------------------------------------------------------------ ULG ground-rail plate lasers
# (model, L, W, repeat Y mm, speed m/min, accel G, load kg, dims) — supplier's web table, October 2026
ULG_A = [("ULG-13035A", 13000, 3500, 0.04, 80, 1.1, 35700, (16200, 5300, 1950)), ("ULG-13040A", 13000, 4000, 0.04, 70, 1.0, 40800, (16200, 5800, 1950)),
         ("ULG-13045A", 13000, 4500, 0.04, 60, 0.85, 45900, (16200, 6300, 1950)), ("ULG-26035A", 26000, 3500, 0.06, 80, 1.1, 71400, (30500, 5300, 1950)),
         ("ULG-26040A", 26000, 4000, 0.06, 70, 1.0, 81600, (31100, 5800, 1950)), ("ULG-26045A", 26000, 4500, 0.06, 60, 0.85, 91800, (31100, 6300, 1950))]
ULG_C = [("ULG-13035C", 13000, 3500, 0.05, 70, 0.8, 35700, (16450, 5400, 2200)), ("ULG-13040C", 13000, 4000, 0.05, 60, 0.7, 40800, (16450, 5900, 2200)),
         ("ULG-13045C", 13000, 4500, 0.05, 50, 0.6, 45900, (16450, 6390, 2200)), ("ULG-26035C", 26000, 3500, 0.07, 70, 0.8, 71400, (30700, 5390, 2200)),
         ("ULG-26040C", 26000, 4000, 0.07, 60, 0.7, 81600, (31100, 5890, 2200)), ("ULG-26045C", 26000, 4500, 0.07, 50, 0.6, 91800, (31100, 6390, 2200))]


def ulg_rows(rows, clearance):
    return [
        ("Working area", [area(r[1], r[2], inches=False) for r in rows]),
        ("Laser power", "12 – 60 kW"),
        ("Max. speed", "axes combined", [mmin(r[4]) for r in rows]),
        ("Max. acceleration", "axes combined", [f"{r[5]:g} G" for r in rows]),
        ("Positioning accuracy", acc_m(0.03)),
        ("Repeat accuracy", [f"X {acc(0.03)} · Y {acc(r[3])}" for r in rows]),
        ("Z travel", mm_in(250)),
        ("Clearance under the gantry", clearance),
        ("Max. table load", [weight(r[6]) for r in rows]),
        ("Dimensions L × W × H", [dims(*r[7], ft=True) for r in rows])]


T_ULG_A = table("ULG-A ground-rail plate lasers · 12 – 60 kW", "6 models · 42.7 or 85.3 ft long, 11.5 – 14.8 ft wide · to 262 ft/min and 1.1 G",
                [r[0] for r in ULG_A], ulg_rows(ULG_A, mm_in(190)))
T_ULG_C = table("ULG-C ground-rail plate lasers · 12 – 60 kW", "6 models · heavier gantry, 11.8″ under the beam with a 60 kW source",
                [r[0] for r in ULG_C], ulg_rows(ULG_C, f"{mm_in(190)} to 40 kW · {mm_in(300)} at 60 kW"))
NOTE_ULG = ("The model number gives the table in decimetres (13035 = 13,000 × 3,500 mm); other lengths are built to order — the photos show "
            "59 ft (18 m) and 66 ft (20 m) machines. Laser power is chosen at order. Speeds and accelerations are no-load values with the "
            "axes combined; the table load is the largest plate the support table carries.")

# ------------------------------------------------------------------------------------------------ sheet + tube combinations
TUBE_CHUCK = "Ø8.7″ or Ø13.8″ chuck (Ø220 / 350 mm); square tube to 12.6″ (320 mm) on the large chuck"
TUBE_LEN = "19.7, 29.5 or 39.4 ft (6, 9 or 12 m)"
T_ULFT = table("ULFT open-type sheet-and-tube fiber lasers", "13 table sizes · 10 × 5 to 85 × 10.5 ft · tube to Ø13.8″ · 1.5 – 60 kW", ["ULFT series"], [
    ("Working area", "sheet", "10 × 5 ft to 85 × 10.5 ft (3,000 × 1,500 – 26,000 × 3,200 mm)"),
    ("Table sizes", "sheet", "10 × 5, 13 × 5, 20 × 5, 13 × 6.6 and 20 × 6.6 ft; 20, 26, 43 or 85 ft × 8.5 or 10.5 ft (3 × 1.5 to 26 × 3.2 m)"),
    ("Tube capacity", "round / square", TUBE_CHUCK),
    ("Tube length", TUBE_LEN),
    ("Laser power", "1.5 – 60 kW"),
    ("Max. speed", "no load", mmin(140)),
    ("Max. acceleration", "1 – 1.5 G"),
    ("Positioning accuracy", acc_m(0.03)),
    ("Repeat accuracy", acc_m(0.02))])
T_ULET = table("ULET enclosed sheet-and-tube fiber lasers", "8 table sizes · 10 × 5 to 41 × 8.5 ft · tube to Ø13.8″ · 1.5 – 40 kW", ["ULET series"], [
    ("Working area", "sheet", "10 × 5 ft to 41 × 8.5 ft (3,000 × 1,500 – 12,500 × 2,600 mm)"),
    ("Table sizes", "sheet", "10 × 5, 13 × 5, 20 × 5, 13 × 6.6 and 20 × 6.6 ft; 20, 26 or 41 ft × 8.5 ft (3 × 1.5 to 12.5 × 2.6 m)"),
    ("Tube capacity", "round / square", TUBE_CHUCK),
    ("Tube length", TUBE_LEN),
    ("Laser power", "1.5 – 40 kW"),
    ("Max. speed", "no load", mmin(140)),
    ("Max. acceleration", "1 – 1.5 G"),
    ("Positioning accuracy", acc_m(0.03)),
    ("Repeat accuracy", acc_m(0.02)),
    ("Chuck", "pneumatic, three times faster than an electric chuck")])

# ------------------------------------------------------------------------------------------------ ULT tube lasers
# (chuck, round lo-hi mm, square mm, X, Z (2 chucks), X (3 chucks), Z (3 chucks), m/min, G, rpm, load kg, loader)
LOADER_220 = "pneumatic loader: round Ø0.4 – 8.7″ (Ø10 – 220 mm), square to 8.7″ diagonal"
ULT = [("016A", 10, 160, 160, 300, 250, None, None, 100, 1.2, 53.5, 150, "pneumatic loader: round Ø0.4 – 6.3″, square to 6.3″ diagonal (160 mm)"),
       ("016B", 10, 160, 160, 300, 250, None, None, 100, 1.2, 53.5, 160, "pneumatic loader: round Ø0.4 – 6.3″, square to 6.3″ diagonal (160 mm)"),
       ("024A", 10, 240, 227, 400, 300, 700, 350, 100, 1.0, 53.5, 400, LOADER_220 + " · 573 lb (260 kg) bars"),
       ("024B", 10, 230, 230, 400, 300, 700, 350, 100, 1.0, 53.5, 260, LOADER_220),
       ("028A", 10, 280, 275, 450, 300, 800, 350, 75, 0.8, 37.5, 600, "bundle feeding system or crane"),
       ("036A", 10, 360, 350, 550, 400, 1000, 400, 60, 0.6, 23, 1000, "bundle feeding system or crane")]


def ult_rows(rows, three):
    return [
        ("Round tube", [dia(r[1], r[2]) for r in rows]),
        ("Square tube", "max. side", [mm_in(r[3]) for r in rows]),
        ("Laser power", "1.5 – 40 kW"),
        ("Bar length", "19.7, 29.5 or 39.4 ft (6, 9 or 12 m)"),
        ("Max. tube weight", "on the chucks", [weight(r[11]) for r in rows]),
        ("Max. speed", [mmin(r[8]) for r in rows]),
        ("Max. acceleration", [f"{r[9]:g} G" for r in rows]),
        ("Chuck speed", [f"{r[10]:g} rpm" for r in rows]),
        ("Head travel X / Z", [f"{(r[6] if three else r[4]) / 25.4:.1f} / {(r[7] if three else r[5]) / 25.4:.1f}″ ({r[6] if three else r[4]} / {r[7] if three else r[5]} mm)" for r in rows]),
        ("Positioning accuracy", acc_m(0.04)),
        ("Repeat accuracy", acc_m(0.03)),
        ("Loading", [r[12] for r in rows])]


T_ULT2 = table("ULT two-chuck tube lasers", "6 chuck versions · Ø0.4 – 14.2″ · 20 – 39 ft bars · 1.5 – 40 kW", [f"ULT-{r[0]}" for r in ULT], ult_rows(ULT, False))
ULT3 = [r for r in ULT if r[6]]
T_ULT3 = table("ULT three-chuck tube lasers · zero-tail", "4 chuck versions · Ø0.4 – 14.2″ · the last part cut without a remnant", [f"ULT-{r[0]} · 3 chucks" for r in ULT3], ult_rows(ULT3, True))

# ------------------------------------------------------------------------------------------------ glance keys
LZ_GK = ["area", "power", "speed", "accel", "load"]
LZ_G_FROM = ["Working area", "Laser power", "Max. speed", "Max. acceleration", "Max. table load"]
TB_GK = ["round", "power", "speed", "length", "load"]
TB_G_FROM = ["Round tube", "Laser power", "Max. speed", "Bar length", "Max. tube weight"]

LZ_STD = ["Fiber laser source chosen at order — Raycus, MAX or IPG — with an autofocus cutting head (Raytools or BOCI) and capacitive height sensing",
          "Cypcut bus control with nesting, the cutting-parameter database and power-based speed adjustment; hand pendant",
          "Welded bed annealed and shot-blasted to relieve stress; Inovance or Delta servos, YYC racks, Hiwin linear guides, DESBOER gearboxes",
          "Zoned dust extraction under the table, automatic lubrication, Hanli water chiller, air-cooled electrical cabinet with Schneider components",
          VOLT, "1-year warranty; installation, operator training, parts and remote diagnostics from Mississauga, ON, Canada"]
LZ_OPT = ["Precitec ProCutter cutting head; IPG source; higher power at order", "Camera nesting over the table for remnants",
          "Sheet storage tower and gantry loading / unloading (flexible manufacturing system)", "Dust collector, air compressor and nitrogen generator sized to the machine",
          "Custom voltage: 208, 240 or 480 V 3-phase"]
TB_STD = ["Double-acting pneumatic self-centring chucks — the standard chuck clamps Ø0.6 to 8.7″ (15 – 220 mm) without changing the jaws",
          "Fiber laser source 1.5 – 40 kW (Raycus, MAX or IPG) with an autofocus tube cutting head and anti-collision protection",
          "Cypcut tube control with the cutting database and power-based speed adjustment",
          "Patented welded bed with servo-following tube supports; stress-relieved crossbeam with cushion pads and limit switches",
          "Delta servos, YYC rack and Hiwin guides; Hanli water chiller; unloading table", VOLT]
TB_OPT = ["Pneumatic loader or automatic bundle loader (bundles to 11,000 lb / 5 t) and feeding system",
          "Third chuck for zero-tail cutting; five-axis ±45° bevel head", "Dual Y-axis cutting for small tube", "TubesT nesting software",
          "Custom voltage: 208, 240 or 480 V 3-phase"]

# ------------------------------------------------------------------------------------------------ families
SHEET_FAMILIES = [
    dict(id="vn-ulf", group="laser-novotech", page=P_SHEET, brand=BRAND,
         name="ULF open-type single-table fiber lasers, 10 × 5 to 85 × 10.5 ft, 1.5 – 60 kW",
         short="ULF open-type lasers",
         models_label="ULF-3015G – 6020G · ULF-3015E – 6022E · ULF-6026E – 26032E · 16 models",
         summary="The open-type laser: a single table loaded from three sides, the source and cabinet built into the machine, and the "
                 "price that makes a first fiber laser possible. The ULF-G takes 1.5 to 6 kW at 295 ft/min and 1.4 G on 10 × 5 to "
                 "20 × 6.7 ft tables — the machine for a shop that cuts sheet and light plate a few hours a day. The ULF-E is the heavier build: "
                 "1.5 to 12 kW, 459 ft/min, 1.7 G, tables to 7.2 ft wide and up to 6,600 lb of plate. The large-format ULF-E machines "
                 "run 6 to 60 kW over plate tables from 20 × 8.5 to 85 × 10.5 ft for structural, trailer and heavy-equipment work, "
                 "with up to 79,000 lb (36 t) on the table.",
         features=["1.5 – 60 kW; 10 × 5 to 85 × 10.5 ft; 295 – 459 ft/min, 1.4 – 1.7 G; table loads to 79,000 lb"] + LZ_STD,
         optional=LZ_OPT,
         images=["vn-ulf-1", "vn-ulf-frame", "vn-ulf-beam", "vn-ulf-console", "vn-ulf-head", "vn-ulf-source", "vn-ulf-chiller", "vn-ipg", "vn-ulf-skyeye"],
         videos=[],
         specs=spec([T_ULF_G, T_ULF_E, T_ULF_L], LZ_GK, LZ_G_FROM, NOTE_SHEET)),
    dict(id="vn-ule", group="laser-novotech", page=P_SHEET, brand=BRAND,
         name="ULE enclosed fiber lasers with exchange table, 10 × 5 to 41 × 8.5 ft, 3 – 40 kW",
         short="ULE exchange-table lasers",
         models_label="ULE-3015E – 6020E · ULE-6026E – 12526E · 7 models",
         summary="The production laser: a full enclosure with laser-safe windows keeps the beam, sparks and fumes in, and two tables "
                 "swap in 15 seconds so the operator loads one sheet while the other is cut. Four sizes from 10 × 5 to 20 × 6.7 ft "
                 "take 3 to 20 kW with 11.8″ of Z travel; three large-format machines from 20 × 8.5 to 41 × 8.5 ft take 6 to 40 kW and "
                 "16.5″ of Z for heavy plate. 459 ft/min and 1.7 G, ±0.03 mm/m positioning, a bed flat to 0.05 mm per square metre "
                 "and a twin-chain exchange that doubles the table load. Ready for a sheet storage tower and gantry loading.",
         features=["3 – 40 kW; 10 × 5 to 41 × 8.5 ft; exchange tables, 15 s swap; 459 ft/min, 1.7 G; Z travel 11.8 – 16.5″"] + LZ_STD,
         optional=LZ_OPT,
         images=["vn-ule-1", "vn-ule-console", "vn-ule-bed", "vn-ule-frame", "vn-ule-servo", "vn-ule-rack", "vn-ule-cabinet", "vn-ule-chiller",
                 "vn-fms-tower", "vn-fms-gantry", "vn-precitec"],
         videos=[],
         specs=spec([T_ULE_S, T_ULE_L], LZ_GK, LZ_G_FROM, NOTE_SHEET)),
    dict(id="vn-ulg", group="laser-novotech", page=P_SHEET, brand=BRAND,
         name="ULG ground-rail plate lasers, 42.7 or 85.3 ft × up to 14.8 ft, 12 – 60 kW",
         short="ULG ground-rail lasers",
         models_label="ULG-13035A – 26045A · ULG-13035C – 26045C · 12 models",
         summary="For plate too long, too wide or too heavy for a table machine: the ULG's gantry runs on rails set in the floor beside a "
                 "separate plate-support table, so the table carries up to 202,000 lb (91.8 t) of plate without loading the motion "
                 "axes. Tables 42.7 or 85.3 ft long and 11.5, 13.1 or 14.8 ft wide, other lengths to order; 12 to 60 kW for thick "
                 "plate. Two gantries: the ULG-A runs to 262 ft/min and 1.1 G, the heavier ULG-C leaves 11.8″ under the beam with a "
                 "60 kW source. Loaded by crane, with zoned extraction along the whole table — the laser for structural steel, tower, "
                 "mining and heavy-equipment fabricators.",
         features=["12 – 60 kW; tables 42.7 or 85.3 ft × 11.5 – 14.8 ft, other lengths to order; table loads to 202,000 lb; to 262 ft/min, 1.1 G",
                   "Gantry on ground rails, separate from the plate-support table — the plate load never reaches the motion axes",
                   "Fiber laser source chosen at order — Raycus, MAX or IPG — with a high-power autofocus cutting head",
                   "Bus CNC with edge finding, nesting, common-line cutting and remnant functions; touchscreen console",
                   "Positioning ±0.03 mm/m over the whole table; transmission covers and automatic lubrication on the long axis",
                   "Zoned fume extraction along the table; replaceable support slats",
                   VOLT, "1-year warranty; installation, operator training, parts and remote diagnostics from Mississauga, ON, Canada"],
         optional=["Bevel cutting head", "MES connection and industry file interfaces", "Dust collector, compressor and gas supply sized to the machine",
                   "Custom voltage: 208, 240 or 480 V 3-phase"],
         images=["vn-ulg-1", "vn-ulg-installed", "vn-ulg-beam", "vn-ulg-rails", "vn-ulg-table", "vn-ulg-cutting", "vn-ulg-parts", "vn-ulg-console",
                 "vn-ulg-extraction", "vn-ulg-flanges"],
         videos=[],
         specs=spec([T_ULG_A, T_ULG_C], LZ_GK, LZ_G_FROM, NOTE_ULG)),
    dict(id="vn-ulft", group="laser-novotech", page=P_SHEET, brand=BRAND,
         name="ULFT open-type sheet-and-tube fiber lasers, 10 × 5 to 85 × 10.5 ft plus tube to Ø13.8″, 1.5 – 60 kW",
         short="ULFT sheet + tube lasers",
         models_label="ULFT 3015 – 26032 · 13 table sizes",
         summary="Sheet and tube on one open-type machine: the ULF table for sheet and plate, and along its side a rotary pneumatic "
                 "chuck and supports for round, square and rectangular tube to Ø8.7″ or Ø13.8″ in 20, 29.5 or 39 ft lengths. The same "
                 "source and head cut both, so a shop that cuts a few tubes a week does not need a second laser. Thirteen table sizes "
                 "from 10 × 5 to 85 × 10.5 ft, 1.5 to 60 kW, 459 ft/min.",
         features=["Sheet 10 × 5 to 85 × 10.5 ft; tube Ø8.7 / 13.8″ chuck, 20 – 39 ft; 1.5 – 60 kW; 459 ft/min, 1 – 1.5 G"] + LZ_STD,
         optional=LZ_OPT + ["Tube supports and unloading for 39 ft lengths"],
         images=["vn-ulft-1", "vn-ulft-chuck", "vn-ulft-frame", "vn-ulft-beam", "vn-ulft-head", "vn-ulft-sources"],
         videos=[],
         specs=spec([T_ULFT], LZ_GK, LZ_G_FROM, NOTE_SHEET)),
    dict(id="vn-ulet", group="laser-novotech", page=P_SHEET, brand=BRAND,
         name="ULET enclosed sheet-and-tube fiber lasers, 10 × 5 to 41 × 8.5 ft plus tube to Ø13.8″, 1.5 – 40 kW",
         short="ULET sheet + tube lasers",
         models_label="ULET 3015 – 12526 · 8 table sizes",
         summary="The enclosed version of the sheet-and-tube laser: the ULE cabin with its exchange table for sheet, and at the end "
                 "of the machine a pneumatic chuck — three times faster to clamp than an electric one — for round, square and "
                 "rectangular tube to Ø8.7″ or Ø13.8″ and 39 ft long. Eight table sizes from 10 × 5 to 41 × 8.5 ft, 1.5 to 40 kW; "
                 "quieter and cleaner than an open machine, for shops where the laser stands next to assembly or welding.",
         features=["Enclosed sheet 10 × 5 to 41 × 8.5 ft; tube Ø8.7 / 13.8″ chuck, 20 – 39 ft; 1.5 – 40 kW; 459 ft/min"] + LZ_STD,
         optional=LZ_OPT + ["Tube supports and unloading for 39 ft lengths"],
         images=["vn-ulet-1", "vn-ulet-chuck", "vn-ulet-beam", "vn-ulet-head", "vn-ulet-source"],
         videos=[],
         specs=spec([T_ULET], LZ_GK, LZ_G_FROM, NOTE_SHEET)),
]

TUBE_FAMILIES = [
    dict(id="vn-ult", group="tube-novotech", page=P_TUBE, brand=BRAND,
         name="ULT tube and pipe lasers, two or three chucks, Ø0.4 – 14.2″, 20 – 39 ft bars, 1.5 – 40 kW",
         short="ULT tube lasers",
         models_label="ULT-016A – 036A · two- and three-chuck · 10 versions",
         summary="The tube laser for round, square, rectangular, oval and open profiles: pneumatic self-centring chucks at both ends "
                 "of the bar, servo-following supports under it, and a 1.5 to 40 kW source that cuts holes, slots, copes and notches "
                 "and parts the tube in one pass. Four chuck sizes — Ø6.3″, 9.4″, 11″ and 14.2″ — for bars of 20, 29.5 or 39 ft and "
                 "up to 2,205 lb; 328 ft/min and 1.2 G on the small chucks. The three-chuck version takes over the bar as it "
                 "shortens, so the last part is cut with no remnant. Pneumatic loaders, bundle feeding, a ±45° five-axis bevel head "
                 "and TubesT nesting are options.",
         features=["Ø0.4 – 14.2″ round, square to 13.8″; bars 20 – 39 ft and to 2,205 lb; 1.5 – 40 kW; to 328 ft/min, 1.2 G"] + TB_STD,
         optional=TB_OPT,
         images=["vn-ult-1", "vn-ult-chuck", "vn-ult-frame", "vn-ult-beam", "vn-ult-head", "vn-ult-console", "vn-ult-loader", "vn-ult-zero",
                 "vn-ult-feeder", "vn-ult-dualy", "vn-ult-tubest"],
         videos=[],
         specs=spec([T_ULT2, T_ULT3], TB_GK, TB_G_FROM, NOTE_TUBE)),
]

ALL = SHEET_FAMILIES + TUBE_FAMILIES
