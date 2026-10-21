#!/usr/bin/env python3
"""One-off correction of the hand-written Bekamak family bullets against bekamak.com (Oct 2026).

NovoTech's rule: a bullet in the family text names an accessory as standard only when the manufacturer
lists it under Standard Features for every model of the family (or the bullet says which models);
everything else goes in an "Options:" bullet, and "hydraulic head rotation" is claimed nowhere —
Bekamak miter heads are swung by hand (digital angle display / hydraulic angle clamping on some sizes);
only the 650DG and 750DG NC have NC-controlled rotation.  Applied to content/families/bandsaw.json
and to the same strings in tools/bandsaw_data.py so a regeneration keeps the corrections.

    python3 -I tools/bekamak_fix_claims.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEATURES = {
    "bekamak-bms-dg": [
        "Bow swivels left and right: miter cuts to +60° / −45°",
        "Hydraulic cylinder for controlled, adjustable descent",
        "Variable blade speed: two-speed motor on the BMS 230DG (inverter optional), stepless 15–120 m/min inverter standard on the BMS 270DG",
        "Manual vise with quick-approach; cutting-length stop",
        "Safety switches on the wheel cover and blade guard",
        "Electric coolant pump and blade brush",
        "Options: 10 ft (3 m) roller table, micro-spray lubrication",
    ],
    "bekamak-bmsy-dgh": [
        "Semi-automatic cycle: the bow descends at the set feed and returns after the cut; hydraulic vise on the DGH models (manual vise on the 230DG / 270DG)",
        "Double miter: +60° right and −45° left, head swung by hand on the angle scale",
        "Inverter drive for stepless blade speed 15–120 m/min (standard from the 270 up; optional on the 230DG / 230DGH)",
        "Hydro-mechanical blade tension with safety switch; blade brush; coolant pump",
        "Bow height-adjustment switch; cutting-pressure control on the 440DGH",
        "Heavy-duty gearbox from the 270 up; control panel",
        "Options: 10 ft (3 m) roller table, micro-spray lubrication; hydraulic top clamp, laser line pointer and motorized roller table on the 440DGH",
    ],
    "bekamak-bmso-roller": [
        "Automatic feeding by driven rollers; hydraulic vise on the 320 / 320L",
        "Piece counter and length setting on the control panel",
        "Automatic bow return; inverter blade speed (standard on the 320 / 320L, optional on the BMSO 230)",
        "Hydro-mechanical blade tension, blade brush, coolant pump, mechanical top clamp, 4 ft (1.2 m) roller table",
        "Options: hydraulic blade tension and chip conveyor (320 / 320L), micro-spray lubrication, 10 ft (3 m) roller table",
    ],
    "bekamak-bmso-ga": [
        "Encoder-measured roller feed with hydraulic feed vise; NC controller for length and quantity",
        "Single miter 0°–60°: the head is swung by hand and locked at the set angle",
        "Inverter blade speed, hydro-mechanical blade tension, heavy-duty gearbox",
        "Blade brush, coolant pump, mechanical top clamp, 4 ft (1.2 m) roller table standard",
        "Options: chip conveyor, micro-spray lubrication, 10 ft (3 m) roller table",
    ],
    "bekamak-bmso-gs": [
        "Servo shuttle-vise feed with ball screw: ±0.1 mm length accuracy",
        "NC control with multi-program job list (length × quantity)",
        "Single miter to 60°: the head is swung by hand on the angle scale",
        "Hydraulic vise, inverter blade speed, hydro-mechanical blade tension",
        "Options: hydraulic top clamp, hydraulic blade tension, multi-segment vise jaws, micro-spray lubrication, 10 ft (3 m) roller table",
    ],
    "bekamak-bmso-dgs": [
        "Motorized shuttle-vise feeding (39″ / 1000 mm stroke); touch-screen control with a 10-step program",
        "Double miter +60° / −45°, head swung by hand",
        "Hydraulic vise, hydro-mechanical blade tension, coolant pump",
        "Options: hydraulic top clamp, micro-spray lubrication, 10 ft (3 m) roller table",
    ],
    "bekamak-bmsy-cgh": [
        "Single miter 0°–60°: the head is swung by hand on the angle scale; digital angle display and hydraulic angle clamping on the 540CGH / 810CGH",
        "Twin-column bow guidance; hydraulic vise; automatic bow return",
        "Inverter blade speed, hydro-mechanical blade tension, 3° inclined blade, optical bow height adjustment",
        "Blade brush, coolant pump, cutting-pressure control",
        "Options: hydraulic top clamp, hydraulic blade tension, chip conveyor, laser line pointer, micro-spray lubrication, 10 ft (3 m) roller tables (plain or motorized)",
    ],
    "bekamak-bmsy-dg-nc": [
        "Double-miter head: NC-controlled rotation on the 650DG / 750DG NC, hand-swung turntable on the 440CDGH / 560DG",
        "Twin-column guidance, hydraulic vise, automatic bow return",
        "Inverter blade speed; hydraulic blade tension on the 650DG / 750DG, hydro-mechanical on the 440CDGH / 560DG",
        "Chip conveyor standard on the 650DG / 750DG (optional on the 560DG); options: hydraulic top clamp, laser line pointer, micro-spray lubrication, 10 ft (3 m) roller tables",
    ],
    "bekamak-bmso-c": [
        "Automatic roller feed with hydraulic feed vise",
        "Piece counter and length setting",
        "Twin-column guidance, hydraulic vise, inverter blade speed",
        "Hydro-mechanical blade tension, blade brush, coolant pump, 4 ft (1.2 m) roller table",
        "Options: hydraulic blade tension, chip conveyor, split vise (330C), laser line pointer, micro-spray lubrication, 10 ft (3 m) roller tables",
    ],
    "bekamak-bmso-cs": [
        "Servo shuttle-vise feed on ball screw; multi-program PLC touch screen",
        "Twin-column guidance; hydraulic vise on feed and cutting side",
        "Inverter blade speed; blade-slippage sensor; hydro-mechanical blade tension (hydraulic blade tension standard on the 570CS / 820CS, optional below)",
        "Chip conveyor on most sizes, blade brush, coolant pump",
        "Options: hydraulic top clamp, multi-segment (bundle) vise jaws, hexagonal vise jaws, micro-spray lubrication, 15 kW (20 HP) main motor, roller tables",
    ],
    "bekamak-bmso-cgs": [
        "Servo shuttle-vise feeding with NC job programming",
        "Miter head 0°–60° (CGS) or +60° / −45° (CDGS), swung by hand with digital angle display; hydraulic angle clamping on the 440CGS / 540CGS",
        "Twin-column guidance, hydraulic vise, inverter blade speed",
        "Hydro-mechanical blade tension, blade brush, coolant pump, 3° inclined blade",
        "Options: hydraulic blade tension, hydraulic top clamp, chip conveyor, laser line pointer, micro-spray lubrication, 10 ft (3 m) roller table",
    ],
    "bekamak-bmso-xs": [
        "Servo-driven bow feed and servo shuttle-vise material feed",
        "CNC control with cutting database and remote diagnostics",
        "Enclosed cabin design, carbide-blade capable, high blade speeds",
        "Hydraulic vises on both sides, hydraulic blade tension, LED work light",
        "Options: pallet-type chip conveyor, hydraulic top clamp, hexagonal vise jaws, 15 kW (20 HP) main motor, micro-spray lubrication",
    ],
    "bekamak-bmsy-heavy": [
        "Capacities from Ø43-3/4″ (1110 mm) to 59″ × 59″ (1500 × 1500 mm)",
        "Twin-column guidance with hydraulic vise and automatic bow return",
        "Heavy-duty gearbox and high-power main motor; inverter blade speed",
        "Hydraulic blade tension, chip conveyor, motorized swarf brush",
        "Options: second vise (standard on the 1515C), hydraulic top clamp, laser line pointer, micro-spray lubrication, 10–13 ft (3–4 m) motorized roller tables",
    ],
}

SUMMARY = {
    "bekamak-bmsy-dgh": "The most popular Bekamak pivot saws: automatic bow lift after every cut, with the head swivelling both ways for miters — right to 60°, left to 45°. DGH versions have a hydraulic vise; the DG versions clamp by hand. Sizes from Ø9″ (230 mm) to Ø17-3/8″ (440 mm).",
    "bekamak-bmso-gs": "NC automatic saws with servo-driven shuttle vise feeding and a single-miter head to 60° (set by hand on the angle scale); the GLS bow takes 24″ (610 mm) wide material.",
    "bekamak-bmsy-dg-nc": "Heavy double-column miter saws whose head swivels both ways; on the 650DG and 750DG NC versions the operator enters the angle and the saw positions itself. Ø14-1/8″ (360 mm) to Ø29-1/2″ (750 mm).",
    "bekamak-bmso-cgs": "Servo-feed automatic double-column saws with a miter head and digital angle display — single miter on the CGS, both sides on the CDGS — for unattended cutting of angled parts up to Ø21-1/4″ (540 mm).",
}

PAGE_TEXT = {  # exact phrases in tools/bandsaw_pages.py and the generated pages
    "Single- or double-miter heads to 60°; DGH models position the head hydraulically": "Single- or double-miter heads to 60°; DGH models add a hydraulic vise",
    "hydro-mechanical blade tension and hydraulic miter positioning on the DGH models.": "hydro-mechanical blade tension and a hydraulic vise on the DGH models.",
    "DGH models position the saw head hydraulically for miter angles instead of by hand, and include hydraulic head lifting — useful on the larger 320–440 mm machines where the bow is heavy.":
        "DGH models have a hydraulic vise — the DG versions clamp the material by hand. The rest of the saw is the same: double-miter head swung by hand on the angle scale, hydraulic feed cylinder and automatic bow return.",
}


def py_list(items):
    return "[" + ", ".join(json.dumps(i, ensure_ascii=False) for i in items) + "]"


def main():
    fam_path = os.path.join(ROOT, "content", "families", "bandsaw.json")
    data = json.load(open(fam_path, encoding="utf-8"))
    dp = os.path.join(ROOT, "tools", "bandsaw_data.py")
    src = open(dp, encoding="utf-8").read()
    for fid, feats in FEATURES.items():
        f = data["families"][fid]
        old = f["features"]
        f["features"] = feats
        old_lit, new_lit = "features=" + py_list(old), "features=" + py_list(feats)
        if old_lit in src:
            src = src.replace(old_lit, new_lit)
        else:
            print("!! bandsaw_data.py: features literal not found for", fid)
    for fid, summ in SUMMARY.items():
        f = data["families"][fid]
        old = f["summary"]
        f["summary"] = summ
        if json.dumps(old, ensure_ascii=False) in src:
            src = src.replace(json.dumps(old, ensure_ascii=False), json.dumps(summ, ensure_ascii=False))
        else:
            print("!! bandsaw_data.py: summary not found for", fid)
    json.dump(data, open(fam_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(dp, "w", encoding="utf-8").write(src)
    # page texts: generator + generated pages
    for path in [os.path.join(ROOT, "tools", "bandsaw_pages.py")] + [os.path.join(ROOT, "content", "pages", n) for n in ("bekamak-semi-automatic-band-saws.json", "band-saw.json", "bekamak-manual-band-saws.json")]:
        s = open(path, encoding="utf-8").read()
        for old, new in PAGE_TEXT.items():
            s = s.replace(old, new).replace(json.dumps(old, ensure_ascii=False)[1:-1], json.dumps(new, ensure_ascii=False)[1:-1])
        open(path, "w", encoding="utf-8").write(s)
    print("done")


if __name__ == "__main__":
    main()
