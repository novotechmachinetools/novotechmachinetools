#!/usr/bin/env python3
"""Add the Bekamak detail photos (control panel, vise, gearbox, blade tension, roller tables …) to the
band saw family galleries.

Source: /home/claude/bekamak/site/details.json + img/details/ (crawl_details.py — the lightbox gallery
behind each product photo on bekamak.com).  Each family gets the details of its models, de-duplicated,
titles cleaned up, the most useful first, at most MAX_PER_FAMILY.  Keys: bk-<family>-d<nn>.

    python3 tools/bekamak_details.py            → updates content/families/bandsaw.json + tools/image_map.json,
                                                  prints the keys for tools/make_images.py --only
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BK = "/home/claude/bekamak/site"
MAX_PER_FAMILY = 14

# extra Bekamak products whose details belong to a family (model names not in our tables)
EXTRA = {
    "bekamak-bmsy-dgh": ["bmsy-360dg-eco"],
    "bekamak-bmso-roller": ["bmso-320s"],
    "bekamak-bmsy-dg-nc": ["bmsy-560-dg"],
    "bekamak-bmsy-c": ["bmsy-820c"],
    "bekamak-bmsy-heavy": ["bmsy-1300c"],
    "bekamak-bmso-cgs": ["bmsy-540cgs"],
    "bekamak-bmso-c": ["bmso-820c_IBDzG"],
    "bekamak-bmso-cs": ["bmso-460cs-nc_HV61W"],
}
TITLES = {  # manufacturer's captions → clean English
    "control panel": "Control panel", "electrical panel": "Electrical panel",
    "hydromechnic blade tension": "Hydro-mechanical blade tension", "hydraulic blade tension": "Hydraulic blade tension",
    "hydraulic blade tention": "Hydraulic blade tension",
    "vise": "Vise", "vice": "Vise", "hydraulic vise": "Hydraulic vise", "hydraulic vice": "Hydraulic vise", "hydraulıc vıce": "Hydraulic vise",
    "second vice": "Second vise", "second vise": "Second vise", "multiple segments": "Multi-segment vise jaws",
    "gearbox": "Gearbox", "heavy duty gearbox": "Heavy-duty gearbox", "motor": "Motor",
    "inverter": "Inverter — variable blade speed", "coolant pump": "Coolant pump",
    "blade brush": "Blade brush", "blade brash": "Blade brush", "saw blade brush": "Blade brush", "motorized swarf brush": "Motorized swarf brush",
    "security switch": "Safety switch", "securty switch": "Safety switch",
    "adjustment shaft": "Material length stop rod", "metarial limit shaft": "Material length stop", "material lenght stop": "Material length stop",
    "adjustable material length stop": "Adjustable material length stop",
    "height adjustment switch": "Bow height adjustment switch", "height adjustment swich": "Bow height adjustment switch", "high adjustment": "Bow height adjustment",
    "optical height adjustment": "Optical bow height adjustment",
    "to adjust degree panel": "Angle adjustment scale", "digital angle display": "Digital angle display", "digital mitre adjustment": "Digital miter adjustment",
    "sensitive pressure": "Cutting pressure control", "pressure adjustment": "Cutting pressure adjustment", "cutting speed control": "Cutting speed control",
    "vibration cylinder": "Vibration damping cylinder",
    "mecanic top clamping": "Mechanical top clamp", "hydraulic top clamping": "Hydraulic top clamp", "hydraulic clamping for angle": "Hydraulic clamping for angle cuts",
    "lineer way": "Linear guides", "linear way": "Linear guides",
    "laser line pointer": "Laser line pointer", "lazer line pointer": "Laser line pointer",
    "2° inclined blade": "2° inclined blade", "cutting width adjustment lever": "Cutting width adjustment lever",
    "chip conveyor": "Chip conveyor", "microspray device": "Micro-spray lubrication",
    "3 mt material roller table": "10 ft (3 m) material roller table", "3 mt motorized roller table": "10 ft (3 m) motorized roller table",
    "1,2 mt roller table": "4 ft (1.2 m) roller table", "roller table": "Roller table",
}
# order of appearance in a gallery: the parts a buyer asks about first
PRIORITY = ["Control panel", "Electrical panel", "Hydraulic vise", "Vise", "Second vise", "Multi-segment vise jaws", "Hydraulic top clamp",
            "Mechanical top clamp", "Hydraulic clamping for angle cuts", "Heavy-duty gearbox", "Gearbox", "Motor", "Inverter — variable blade speed",
            "Hydraulic blade tension", "Hydro-mechanical blade tension", "Linear guides", "Cutting pressure control", "Cutting pressure adjustment",
            "Optical bow height adjustment", "Bow height adjustment switch", "Bow height adjustment", "Angle adjustment scale", "Digital angle display",
            "Digital miter adjustment", "Laser line pointer", "Chip conveyor", "Motorized swarf brush", "Blade brush", "Coolant pump",
            "Micro-spray lubrication", "Safety switch", "Material length stop", "Adjustable material length stop", "Material length stop rod",
            "Vibration damping cylinder", "2° inclined blade", "Cutting width adjustment lever", "Cutting speed control",
            "10 ft (3 m) motorized roller table", "10 ft (3 m) material roller table", "4 ft (1.2 m) roller table", "Roller table"]


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def main():
    fam_path = os.path.join(ROOT, "content", "families", "bandsaw.json")
    data = json.load(open(fam_path, encoding="utf-8"))
    fams = data["families"]
    details = json.load(open(os.path.join(BK, "details.json")))
    slugs = {}
    for s in details:
        base = re.sub(r"_[A-Za-z0-9]{5}$", "", s).replace("-nc", "").replace("-kabinli", "").replace("-cnc", "")
        slugs[norm(base)] = s
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    # drop earlier detail keys (re-run safe)
    for k in [k for k in imap if re.match(r"bk-.*-d\d\d$", k)]:
        del imap[k]
    new_keys = []
    for fid, f in fams.items():
        if f.get("brand") != "bekamak":
            continue
        f["images"] = [k for k in f["images"] if not re.match(r"bk-.*-d\d\d$", k)]
        items = {}   # file -> (title, model)
        pairs = [(m["name"], slugs.get(norm(m["name"]))) for m in f["specs"]["models"]]
        pairs += [(None, s) for s in EXTRA.get(fid, [])]
        for model, slug in pairs:
            if not slug:
                continue
            for it in details.get(slug, []):
                t = it["title"].strip()
                if not t or t.lower().startswith("saw blade"):
                    continue
                title = TITLES.get(t.lower(), t[:1].upper() + t[1:])
                if it["file"] not in items:
                    items[it["file"]] = (title, model or f["specs"]["models"][0]["name"])
        ordered = sorted(items.items(), key=lambda kv: (PRIORITY.index(kv[1][0]) if kv[1][0] in PRIORITY else 99, kv[1][0]))
        # one photo per title (the first model's), then the rest if room
        seen_titles, chosen, rest = set(), [], []
        for file, (title, model) in ordered:
            (chosen if title not in seen_titles else rest).append((file, title, model))
            seen_titles.add(title)
        chosen = (chosen + rest)[:MAX_PER_FAMILY]
        short = fid.replace("bekamak-", "")
        for i, (file, title, model) in enumerate(chosen, 1):
            key = f"bk-{short}-d{i:02d}"
            imap[key] = {"src": os.path.join(BK, "img", "details", file), "alt": f"Bekamak {model} — {title.lower() if title[1:2].islower() else title}", "section": "bandsaw", "trim": False, "quality": 82}
            f["images"].append(key)
            new_keys.append(key)
        print(f"{fid:24s} {len(chosen):2d} details: " + ", ".join(t for _, t, _ in chosen)[:120])
    json.dump(data, open(fam_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "bekamak_detail_keys.txt"), "w").write(",".join(new_keys))
    print(len(new_keys), "detail photos → tools/bekamak_detail_keys.txt")


if __name__ == "__main__":
    main()
