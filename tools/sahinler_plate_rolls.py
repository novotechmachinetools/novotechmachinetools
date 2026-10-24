"""Şahinler plate rolls — families appended to the İşitan hydraulic 4-roll and 3-roll pages (catalogue pages 3–21).
Imported by tools/isitan_plate_rolls.py; the İşitan families stay on top of each page, Şahinler groups below."""
from sahinler_lib import *  # noqa: F401,F403

SET = "plate-rolls"
P4, P3 = "hydraulic-4-roll-plate-rollers", "hydraulic-3-roll-plate-rollers"

IMAGES = {   # key -> alt is taken from tools/sahinler_photos.py; this list only orders the galleries
}

OPT_4R = ["Automation with NC or CNC control (ESA, Italy)", "Overhead crane and hydraulic side supports for large diameters", "Hydraulic plate ejector for series production",
          "Ground rolls for special jobs; infinitely variable speed", "Electronic roll balancing for parallel roll movement", VOLT]


def t_4rhss():
    return [plate_table(6, 0, "4R HSS 20 · 6.7 ft", "working length 80.7″ · 8 models"), plate_table(6, 1, "4R HSS 25 · 8.4 ft", "working length 100.4″ · 8 models"),
            plate_table(7, 0, "4R HSS 30 · 10.2 ft", "working length 122″ · models 280 – 460"), plate_table(7, 1, "4R HSS 30 · 10.2 ft (cont.)", "working length 122″ · models 500 – 680"),
            plate_table(8, 0, "4R HSS 40 · 13.5 ft", "working length 161.4″ · 8 models"), plate_table(8, 1, "4R HSS 60 · 20 ft", "working length 240.2″ · 7 models")]


def t_4rhsl():
    return [plate_table(12, 0, "4R HS-L · linear", "Ø3.9″ – 5.1″ rolls · 3.4 – 6.7 ft · 7 models")]


def t_4rhs():
    return [plate_table(12, 1, "4R HS 15 · 5.1 ft", "working length 61″ · 5 models"), plate_table(13, 0, "4R HS 20 · 6.7 ft", "working length 80.7″ · 6 models"),
            plate_table(13, 1, "4R HS 25 · 8.4 ft", "working length 100.4″ · 5 models"), plate_table(14, 0, "4R HS 30 · 10.2 ft", "working length 122″ · 5 models"),
            plate_table(14, 1, "4R HS 40 · 13.5 ft", "working length 161.4″")]


def t_4rh():
    return [plate_table(16, 0, "4RH · cassette type", "3.4 – 5.1 ft · 7 models")]


def t_4rhc():
    tb = table(21, 0)
    R = rows_of(tb)
    n = len(tb["models"])
    rows = [{"label": "Working length", "sub": "", "cells": [wl(R["Working length"][i], R["Working length in"][i]) for i in range(n)], "key": True},
            {"label": "Rolling capacity", "sub": "mild steel", "cells": [cap(c) for c in R["Rolling capacity (mild steel)"]], "key": True},
            {"label": "Largest roll Ø (cone end)", "sub": "", "cells": [inch(c) for c in R["Largest roll Ø (cone end)"]], "key": False},
            {"label": "Smallest roll Ø (cone end)", "sub": "", "cells": [inch(c) for c in R["Smallest roll Ø (cone end)"]], "key": False},
            {"label": "Min. rolling Ø", "sub": "", "cells": [inch(c) for c in R["Min. rolling Ø"]], "key": False},
            {"label": "Motor power", "sub": "", "cells": [motor(c) for c in R["Motor power"]], "key": False},
            {"label": "Rolling speed", "sub": "", "cells": [speed(c) for c in R["Rolling speed"]], "key": False},
            {"label": "Dimensions L × W × H", "sub": "", "cells": [dims(c) for c in R["Dimensions L × W × H"]], "key": False},
            {"label": "Weight", "sub": "", "cells": [weight(c) for c in R["Weight"]], "key": False}]
    return [{"title": "4R HC · conical", "sub": "3.4 – 5.1 ft · 3 models", "models": list(tb["models"]), "rows": rows}]


def t_3ruhs():
    return [plate_table(18, 0, "3R UHS 30 · 10.2 ft", "working length 122″ · 6 models")]


def t_3rhs():
    return [plate_table(20, 0, "3R HS 20 · 6.7 ft", "working length 80.7″ · 4 models"), plate_table(20, 1, "3R HS 25 · 8.4 ft", "working length 100.4″ · 4 models"),
            plate_table(20, 2, "3R HS 30 · 10.2 ft", "working length 122″ · 4 models")]


FAMILIES = [
    dict(id="sahinler-4r-hss", group="sahinler-4r", page=P4, brand="sahinler",
         name="4R HSS hydraulic heavy-duty 4-roll plate rolls",
         short="4R HSS heavy-duty 4-roll",
         models_label="4R HSS 20-280 – 4R HSS 60-620 · 42 models · 6.7 to 20 ft",
         summary="Şahinler's heavy-duty 4-roll plate bending machines for wind-tower, shipyard, pressure-vessel and pipeline work: "
                 "42 models from 6.7 ft to 20 ft that roll plate up to 3-3/8″ thick. The pinch roll and both side rolls travel on a "
                 "pyramid linear path on hydraulic cylinders, so the cylinders put all their force into the plate; the top roll is driven "
                 "by motor and planetary gearbox with two speeds. Three digital readouts, hydraulic roll balancing, a cone-bending device "
                 "and a hydraulic tilting drop-end are standard; NC or CNC control (ESA, Italy), overhead crane, side supports and a plate "
                 "ejector turn the machine into a wheel-rim or shell production line.",
         features=["Pinch and side rolls move on a pyramid linear path with hydraulic cylinders; linear guide system puts the full cylinder force into the plate",
                   "Top roll driven by motor and planetary gearbox, two-speed operation; overload protection",
                   "Three digital readouts for easy roll positioning; mobile control panel",
                   "Hydraulic roll balancing on Ø11″ – 18.1″ rolls, electronic balancing on Ø19.7″ – 26.8″ rolls; central lubrication (automatic on the large rolls)",
                   "Hydraulic tilting drop-end for easy removal of finished parts; cone-bending device",
                   "SAE 1050 (CK45-50) forged or hot-rolled, induction-hardened and polished rolls; welded steel frames; CE marked"],
         optional=OPT_4R + ["Accumulator system for rotating welded parts and welding safety system"],
         images=["sh-4rhss-30-380-nc", "sh-4rhss-heavy", "sh-4rhss-crane", "sh-4rhss-side-supports", "sh-4rhss-dro", "sh-4rhss-cone"],
         videos=vids(("TbSq2XpE5Zk", "4R HSS 30-350 NC heavy-duty plate roll with side supports and overhead support"), ("SpK80ozB2eQ", "4R HSS 40-550 plate roll — 13.5 ft"), ("pr9M1AlSgso", "4R HSS 60-400 — 20 ft 4-roll plate roll with NC control")),
         specs=plate_spec(t_4rhss()),
         headline="Working lengths 6.7 – 20 ft (2050 – 6100 mm) · rolls up to 3-3/8″ (85 mm) plate"),
    dict(id="sahinler-4r-hsl", group="sahinler-4r", page=P4, brand="sahinler",
         name="4R HS-L hydraulic 4-roll plate rolls — linear, wedge pinch",
         short="4R HS-L linear 4-roll",
         models_label="4R HS-L 10-100 – 4R HS-L 20-130 · 7 models · 3.4 to 6.7 ft",
         summary="Compact 4-roll plate rolls with Ø3.9″ – 5.1″ rolls for light and medium plate and stainless steel. The bottom pinch "
                 "roll rises on a hydraulic wedge system and the two side rolls work in double-pinch pyramid action, so both ends of the "
                 "sheet are pre-bent in one pass; the top roll is driven by a hydraulic motor through a planetary gearbox and the bottom "
                 "roll through a cardan joint. Three digital readouts, hydraulic drop-end, cone-bending device and two speeds are "
                 "standard — the 4R HS-L is also the base of Şahinler's automatic wheel-rim body rolling line.",
         features=["Bottom pinch roll on a hydraulic wedge system; two side rolls with double-pinch pyramid action — double pre-bend in one pass",
                   "Top roll driven by hydraulic motor and planetary gearbox; bottom roll by cardan-joint system through gears",
                   "Three digital readouts; mobile control panel; central lubrication; overload protection",
                   "Hydraulic drop-end; cone-bending device; two-speed operation",
                   "SAE 1050 (CK45-50) induction-hardened and polished rolls; welded steel frames; CE marked"],
         optional=["Automation with NC or CNC control", "Overhead crane and hydraulic side supports", "Hydraulic plate ejector — automatic wheel-rim body rolling",
                   "Ground rolls; infinitely variable speed; electronic roll balancing", VOLT],
         images=["sh-4rhs-30-190", "sh-4rhs-20-260-crane"],
         videos=vids(("-WSHmos5adM", "4R HS-L 10-110 NC 4-roll plate roll with automatic loading table and part ejector"), ("2TtFPY09kB8", "4R HS-L hydraulic 4-roll plate bending roll")),
         specs=plate_spec(t_4rhsl()),
         headline="Working lengths 3.4 – 6.7 ft (1050 – 2050 mm) · rolls up to 5/16″ (8 mm)"),
    dict(id="sahinler-4r-hs", group="sahinler-4r", page=P4, brand="sahinler",
         name="4R HS hydraulic 4-roll plate rolls — orbital",
         short="4R HS orbital 4-roll",
         models_label="4R HS 15-150 – 4R HS 40-260 · 22 models · 5.1 to 13.5 ft",
         summary="Mid-range 4-roll plate bending machines with Ø5.9″ – 10.2″ rolls: the pinch and side rolls move on an orbital path with "
                 "hydraulic cylinders, the top roll is driven by hydromotor and planetary gearbox and the bottom roll by gear and cardan "
                 "system. Hydraulic balancing keeps the rolls parallel; three digital readouts, cone-bending device and two speeds are "
                 "standard. From 5.1 ft to 13.5 ft and plate up to 1″ — the 4-roll machine of the general fabrication shop, available "
                 "with NC or CNC control, overhead crane and side supports.",
         features=["Pinch and side rolls move on an orbital path with hydraulic cylinders; hydraulic balancing system",
                   "Top roll driven by hydromotor and planetary gearbox; bottom roll by gear and cardan system",
                   "Three digital readouts for easy roll positioning; mobile control panel; overload protection",
                   "Hydraulic drop-end; cone-bending device; two-speed operation",
                   "SAE 1050 (CK45-50) forged or hot-rolled, induction-hardened and polished rolls; welded steel frames; CE marked"],
         optional=OPT_4R,
         images=["sh-4rhs-25-245", "sh-4rhs-cone-device"],
         videos=vids(("cLgF3gMPYNg", "4R HS 20-260 4-roll hydraulic plate bending roll"), ("cjPMo9s1Olo", "4R HS 20-245 4-roll plate roll with CNC control"), ("_2GhF396tTI", "4R HS 20-260 — conical bending")),
         specs=plate_spec(t_4rhs()),
         headline="Working lengths 5.1 – 13.5 ft (1550 – 4100 mm) · rolls up to 1″ (25 mm)"),
    dict(id="sahinler-4rh", group="sahinler-4r", page=P4, brand="sahinler",
         name="4RH NC cassette-type hydraulic 4-roll plate rolls",
         short="4RH cassette 4-roll",
         models_label="4RH 10-60 – 4RH 15-130 · 7 models · 3.4 to 5.1 ft",
         summary="Compact NC-controlled 4-roll machines for light plate, aluminum and stainless steel from 22 ga to 3/16″: all rolls move "
                 "with one hydraulic cylinder through a cassette-type frame, the top roll is driven by planetary gearbox and the bottom "
                 "and side rolls by gear system. NC control panel, feeding table and hydraulic drop-end are standard. The cassette design "
                 "is also built as special mass-production systems for the automotive sector — elliptical and cylindrical shapes such as "
                 "exhaust mufflers.",
         features=["NC control panel standard; mobile control panel", "Rolls move with one hydraulic cylinder through a cassette-type frame",
                   "Top roll driven by planetary gearbox; bottom and side rolls by gear system", "Feeding table; hydraulic drop-end for easy removal of finished parts",
                   "Welded steel frames; overload protection; CE marked", "Special cassette systems for mass production of mufflers and similar cylindrical / elliptical parts"],
         optional=[VOLT],
         images=["sh-4rh-10-90-nc", "sh-4rh-10-130-nc", "sh-4rh-10-90-detail", "sh-4rh-10-90-side"],
         videos=vids(("LBJZvmwwyNM", "4RH four-roll plate roll")),
         specs=plate_spec(t_4rh()),
         headline="Working lengths 3.4 – 5.1 ft (1050 – 1550 mm) · sheet up to 3/16″ (5 mm) · NC control standard"),
    dict(id="sahinler-4r-hc", group="sahinler-4r", page=P4, brand="sahinler",
         name="4R HC hydraulic 4-roll conical plate rolls",
         short="4R HC conical 4-roll",
         models_label="4R HC 10-155 · 10-185 · 15-185",
         summary="Purpose-built cone rolling machines: four polished, cone-machined rolls driven by a gear system from a single planetary "
                 "gearbox and hydromotor, with the pinch and side rolls on hydraulic cylinders. Five digital readouts set the roll "
                 "positions for repeat cones in light plate, aluminum and stainless steel up to 8 ga — hoppers, funnels, reducers and "
                 "lamp posts — with a hydraulic drop-end to release the finished cone.",
         features=["Special polished, cone-machined rolls — made for rolling cones", "Four rolls driven by a gear system from a single planetary gearbox and hydromotor",
                   "Pinch and side rolls move with hydraulic cylinders; 5 digital readouts for easy roll positioning", "Hydraulic drop-end; mobile control panel; manual central lubrication",
                   "SAE 1050 (CK45-50) induction-hardened and polished rolls; welded steel frames; overload protection"],
         optional=[VOLT],
         images=["sh-4rhc-10-155"],
         videos=vids(("ZbCcqb2ES9Y", "4R HC 10-155 cone plate rolling machine"), ("zh12gSVvWt4", "4R HC conical plate roll bending machine")),
         specs=plate_spec(t_4rhc(), NOTE_SIMPLE),
         headline="Working lengths 3.4 – 5.1 ft (1050 – 1550 mm) · cones in sheet to 8 ga (4 mm)"),
    dict(id="sahinler-3r-uhs", group="sahinler-3r", page=P3, brand="sahinler",
         name="3R UHS 3-roll hydraulic translating heavy-duty plate rolls",
         short="3R UHS heavy-duty 3-roll",
         models_label="3R UHS 30-450 – 3R UHS 30-680 · 6 models · 10.2 ft",
         summary="Three-roll plate rolls of the translating type: the two bottom rolls move horizontally, which gives a low working height, "
                 "a smaller foundation pit (none on the smaller models), the best pre-bending on every diameter and more plate thickness "
                 "than equivalent 3- or 4-roll machines — up to 3-1/2″ on the 3R UHS 30-680. Reducing the side-roll distance improves "
                 "pre-bending on small diameters, heavy cones are rolled in several strokes and the solid frame also works as a press "
                 "for re-rolling and calibrating tubes. Hydraulic drop-end, brake system, cone-bending device and electronic roll "
                 "balancing are standard.",
         features=["Horizontally moving bottom rolls — lower working height, smaller or no foundation pit, reduced overall dimensions",
                   "Best pre-bending on every required diameter; large working stroke; no need to tilt the top roll to remove finished tubes",
                   "Bends thicker plate than equivalent 3- or 4-roll machines; heavy cones produced in several strokes",
                   "Solid construction lets the machine work as a press brake for re-rolling and calibrating tubes",
                   "Two-speed operation; cone-bending device; electronic roll balancing; standard brake system; hydraulic drop-end",
                   "SAE 1050 (CK45-50) forged or hot-rolled, induction-hardened and polished rolls"],
         optional=["NC control system", "Overhead crane and hydraulic side supports for large diameters", VOLT],
         images=["sh-3ruhs-30-550"],
         videos=vids(("mU3ZumBNZ0I", "3R heavy-duty 3-roll plate bending roll, Ø500 mm rolls")),
         specs=plate_spec(t_3ruhs()),
         headline="Working length 10.2 ft (3100 mm) · rolls up to 3-1/2″ (90 mm) plate"),
    dict(id="sahinler-3r-hs", group="sahinler-3r", page=P3, brand="sahinler",
         name="3R HS 3-roll hydraulic plate rolls",
         short="3R HS hydraulic 3-roll",
         models_label="3R HS 20-210 – 3R HS 30-280 · 12 models · 6.7 to 10.2 ft",
         summary="Double-pinch 3-roll plate bending machines for light and medium plate, aluminum and stainless steel: the side rolls move "
                 "on an orbital path with hydraulic cylinders, all three rolls are driven by a single planetary gearbox and gear system "
                 "and hydraulic balancing keeps them parallel. Cone-bending device with ball bearing, hydraulic drop-end and extended "
                 "roll shafts for profile and pipe bending rolls are standard — one machine rolls cylinders, cones and, with the optional "
                 "roll set, angle and pipe.",
         features=["Side rolls move on an orbital path with hydraulic cylinders; hydraulic balancing for parallel roll movement",
                   "All 3 rolls driven by a single planetary gearbox and gear system", "Cone-bending device with ball bearing; hydraulic drop-end",
                   "Extended shafts for profile and pipe bending rolls", "Mobile control panel; overload protection",
                   "SAE 1050 (CK45-50) forged or hot-rolled, induction-hardened and polished rolls; welded steel frames; CE marked"],
         optional=["Profile bending roll set on the extended shafts", "Overhead crane and hydraulic side supports for large diameters", "Ground rolls; infinitely variable speed; electronic roll balancing", VOLT],
         images=["sh-3rhs-20-210", "sh-3rhs-detail", "sh-3rhs-drop-end"],
         videos=vids(("mLIkH1npMO0", "3R HS 20-300 three-roll hydraulic plate bender"), ("JjSbK3gadgk", "3R HS 25-300 three-roll plate roll — cylindrical and conical bending")),
         specs=plate_spec(t_3rhs()),
         headline="Working lengths 6.7 – 10.2 ft (2050 – 3100 mm) · rolls up to 1-1/8″ (30 mm)"),
]

GROUPS = {
    P4: ("sahinler-4r", "Şahinler hydraulic 4-roll plate rolls", "Heavy-duty 4R HSS to 20 ft and 3-3/8″ plate, linear 4R HS-L, orbital 4R HS, NC cassette-type 4RH and the 4R HC cone roll.", "sahinler"),
    P3: ("sahinler-3r", "Şahinler hydraulic 3-roll plate rolls", "3R UHS translating heavy-duty rolls to 3-1/2″ plate and the double-pinch 3R HS.", "sahinler"),
}
