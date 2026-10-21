#!/usr/bin/env python3
"""Standard Features / Optional Features of every Bekamak model, from bekamak.com, into the family data.

bekamak.com shows two tabs per product — Standard Features and Optional Features — each a list of
captions with a detail photo behind most of them (control panel, vise, gearbox, roller table …).
tools/bekamak_crawl.py saves them in /home/claude/bekamak/site/products.json; this script attaches
them per model to content/families/bandsaw.json as

    "model_features": [{"model": "BMS 230DG", "slug": "bms-230-dg",
                        "standard": [{"title": "Control panel", "image": "bk-det-2012-11-12-695644"}, …],
                        "optional": [{"title": "Inverter — variable blade speed", "image": …}, {"title": "…", "image": null}]}]

and registers every feature photo once in tools/image_map.json (keys bk-det-<file>, shared between the
models that use the same photo).  The gallery keeps the machine views only; the detail photos that
used to be appended to the galleries (bk-<family>-dNN) are dropped, since they now appear under the
feature they illustrate.

    python3 tools/bekamak_features.py          → prints the new image keys for tools/make_images.py --only
"""
import json
import os
import re
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bekamak_details import TITLES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BK = "/home/claude/bekamak/site"
ALIASES = {  # family model name → bekamak.com slug where the names differ
    "BMSY 360DGH ECO": "bmsy-360dg-eco",
    "BMSO 540CGS": "bmsy-540cgs",
}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def slug_index(products):
    exact, relaxed = {}, {}
    for s in products:
        base = re.sub(r"_[A-Za-z0-9]{5}$", "", s)
        exact.setdefault(norm(base), s)
        relaxed.setdefault(norm(base.replace("-kabinli", "").replace("-cnc", "").replace("-nc", "")), s)
    return exact, relaxed


def slug_for(name, exact, relaxed):
    if name in ALIASES:
        return ALIASES[name]
    n = norm(name)
    return exact.get(n) or relaxed.get(n)


EXTRA_TITLES = {  # more of bekamak.com's captions → clean English (lower-case keys; see TITLES in bekamak_details.py)
    "3 mt motorized material roller table": "10 ft (3 m) motorized roller table", "3 mt roller table": "10 ft (3 m) material roller table",
    "3 mt. roller table": "10 ft (3 m) material roller table", "4 mt motorized roller table": "13 ft (4 m) motorized roller table",
    "45° / 60° 1,2 mt metarial roller table": "4 ft (1.2 m) roller table for 45° / 60° cuts", "1,2 mt metarial roller table": "4 ft (1.2 m) roller table",
    "15 kw main drive motor": "15 kW (20 HP) main motor", "optional main derive motor 15 kw": "15 kW (20 HP) main motor",
    "deflection control": "Blade deflection control", "cutting speed display": "Cutting speed display",
    "hexagonal vices": "Hexagonal vise jaws", "hexagonal vise": "Hexagonal vise jaws", "high vice": "High vise jaws", "high vise jaws": "High vise jaws",
    "split vice": "Split vise", "split vise": "Split vise", "hydraulic split vice": "Hydraulic split vise", "hydraulic split vise": "Hydraulic split vise",
    "double vise": "Double vise", "back open vice": "Rear-opening vise", "feeding vice": "Feeding vise", "feeding vise": "Feeding vise",
    "feeding vice 1000 mm stroke": "Feeding vise, 39″ (1000 mm) stroke", "hydraulic vise cylinder": "Hydraulic vise cylinder",
    "micro spray": "Micro-spray lubrication", "microspray coolant": "Micro-spray lubrication", "mikcrospray device": "Micro-spray lubrication",
    "mikrosprey device": "Micro-spray lubrication",
    "palet type chip conveyor": "Pallet-type chip conveyor", "pallet type chip conveyor": "Pallet-type chip conveyor", "chip conveyor motor": "Chip conveyor motor",
    "turn table": "Turntable", "nc rotation table": "NC rotation table", "1 programme with 10 steps": "1 program with 10 steps",
    "3 inclined blade": "3° inclined blade", "3° inclined blade": "3° inclined blade", "2° tilted head": "2° inclined head",
    "arm pull lamas": "Bow pull plates", "arm safety switch": "Bow safety switch", "arm tightening piston": "Bow clamping cylinder",
    "boron oil pump": "Coolant pump (boron oil)", "bow servo shaft": "Bow servo drive", "chip brush": "Chip brush",
    "cnc smart cutting controlling technical parameters for optimum cutting": "CNC smart cutting: parameters controlled for optimum cutting",
    "coolant pomp": "Coolant pump", "cover switch": "Cover safety switch", "cutting width adjustment arm": "Cutting width adjustment lever",
    "fixing hydraulically": "Hydraulic clamping", "hyd. clamping for angle": "Hydraulic clamping for angle cuts",
    "hydraulic blade tension and slippage sensor": "Hydraulic blade tension with slippage sensor",
    "hydraulic blade tension and stud control": "Hydraulic blade tension with stud control", "hydraulic blade tensioning": "Hydraulic blade tension",
    "hydromechanic blade tension": "Hydro-mechanical blade tension", "hydraulic carbide bearings": "Hydraulic carbide blade guides",
    "hydraulic tension-opening button": "Hydraulic tension release button", "input output feed rollers": "Infeed and outfeed rollers",
    "led lamp": "LED work light", "led light": "LED work light", "lever type control panel": "Lever-type control panel", "linear guide": "Linear guides",
    "material limit shaft": "Material length stop", "mechanic top clamping": "Mechanical top clamp", "motorized saw blade brush": "Motorized swarf brush",
    "omron control panel": "Omron control panel", "powerful gearbox": "Heavy-duty gearbox", "planetary gearbox": "Planetary gearbox",
    "proximity switch for sensing blade slippage": "Blade slippage sensor (proximity switch)", "proximity switch for sensing blade slipping": "Blade slippage sensor (proximity switch)",
    "saw blade 27": "Band saw blade 27 mm (1.06″) wide", "standing of the control pedal": "Control pedal stand",
    "touch screen control panel": "Touch-screen control panel", "touch screen": "Touch-screen control panel", "warning lamp": "Warning lamp",
    "automatic lubrication": "Automatic lubrication", "manual central lubrication": "Manual central lubrication", "cleaning hose": "Cleaning hose",
    "movable arm": "Movable arm", "optical rapid approach": "Optical rapid approach", "safety rope sensor": "Safety rope sensor", "servo motor": "Servo motor",
    "foot pedal": "Foot pedal", "tilt adjustment lever": "Tilt adjustment lever",
}
ACRONYMS = {"nc": "NC", "cnc": "CNC", "led": "LED", "kw": "kW", "hp": "HP"}


def clean_title(t):
    t = re.sub(r"\s+", " ", t).strip().rstrip(".")
    key = t.lower()
    if key in TITLES:
        return TITLES[key]
    if key in EXTRA_TITLES:
        return EXTRA_TITLES[key]
    m = re.match(r"^saw blade\s+(\d+)\s*mm$", t, re.I)
    if m:
        w = int(m.group(1))
        return f"Band saw blade {w} mm ({w / 25.4:.2f}″) wide"
    # generic tidy-ups: "3 Mt" → "10 ft (3 m)", Title Case → sentence case, acronyms kept
    t = re.sub(r"(\d+(?:[.,]\d+)?)\s*[Mm]t\b", lambda m: f"{round(float(m.group(1).replace(',', '.')) * 3.2808):g} ft ({m.group(1).replace(',', '.')} m)", t)
    words = [ACRONYMS.get(w.lower(), w.lower()) for w in t.split(" ")]
    out = " ".join(words)
    return out[:1].upper() + out[1:]


def yellow_share(path):
    """Share of the machine's pixels that are Bekamak yellow: a front view (yellow covers facing the
    camera) scores 0.1–0.4, the grey back of the machine under 0.05."""
    a = np.asarray(Image.open(path).convert("HSV")).astype(int)
    h, sat, v = a[..., 0], a[..., 1], a[..., 2]
    yellow = (h >= 25) & (h <= 48) & (sat > 120) & (v > 120)
    machine = (v < 235) | (sat > 30)
    return float(yellow.sum()) / max(int(machine.sum()), 1)


def front_views_first(keys, imap, thr=0.06):
    """House rule 3 (docs/images.md): photos of the front of the machine (yellow covers) come before the
    photos of its grey back; the order within each group is kept."""
    def src(k):
        p = imap[k]["src"]
        return p if os.path.isabs(p) else os.path.join(ROOT, p)
    scored = [(k, yellow_share(src(k))) for k in keys]
    return [k for k, y in scored if y >= thr] + [k for k, y in scored if y < thr]


def image_key(file):
    stem = os.path.splitext(file)[0].replace("bekamak_", "").replace("_", "-")
    if re.fullmatch(r"[0-9a-f]{32}", stem):
        stem = stem[:12]
    return "bk-det-" + stem


def main():
    products = json.load(open(os.path.join(BK, "products.json"), encoding="utf-8"))
    exact, relaxed = slug_index(products)
    fam_path = os.path.join(ROOT, "content", "families", "bandsaw.json")
    data = json.load(open(fam_path, encoding="utf-8"))
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    old_detail_keys = [k for k in imap if re.match(r"bk-.*-d\d\d$", k)]
    for k in old_detail_keys:
        del imap[k]
    new_keys, missing = [], []
    for fid, f in data["families"].items():
        if f.get("brand") != "bekamak":
            continue
        f["images"] = front_views_first([k for k in f["images"] if not re.match(r"bk-.*-d\d\d$", k)], imap)
        mf = []
        for m in f["specs"]["models"]:
            slug = slug_for(m["name"], exact, relaxed)
            if not slug or slug not in products:
                missing.append((fid, m["name"]))
                continue
            p = products[slug]
            entry = {"model": m["name"], "slug": slug, "standard": [], "optional": []}
            for kind in ("standard", "optional"):
                seen = set()
                for it in p[kind]:
                    title = clean_title(it["title"])
                    if title.lower() in seen:
                        continue
                    seen.add(title.lower())
                    key = None
                    if it["file"] and os.path.exists(os.path.join(BK, "img", "details", it["file"])):
                        key = image_key(it["file"])
                        if key not in imap:
                            imap[key] = {"src": os.path.join(BK, "img", "details", it["file"]),
                                         "alt": f"Bekamak {m['name']} — {title[0].lower() + title[1:] if title[1:2].islower() else title}",
                                         "section": "bandsaw", "trim": False, "quality": 82}
                            new_keys.append(key)
                    entry[kind].append({"title": title, "image": key})
            mf.append(entry)
        f["model_features"] = mf
        n_std = sum(len(e["standard"]) for e in mf); n_opt = sum(len(e["optional"]) for e in mf)
        print(f"{fid:24s} {len(mf)}/{len(f['specs']['models'])} models  {n_std:3d} standard  {n_opt:3d} optional")
    json.dump(data, open(fam_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "bekamak_detail_keys.txt"), "w").write(",".join(new_keys))
    print(len(new_keys), "feature photos → tools/bekamak_detail_keys.txt;", len(old_detail_keys), "old gallery detail keys removed")
    if missing:
        print("not on bekamak.com (catalogue-only models):", ", ".join(f"{f}/{m}" for f, m in missing))


if __name__ == "__main__":
    main()
