#!/usr/bin/env python3
"""Complete the Bekamak spec tables from the Technical Details tab on bekamak.com.

The catalogue PDF prints only some miter angles (0 / +45 / +60 / −45 on the small saws); the website
lists every angle the machine cuts at (0, ±30, ±45, ±60) for round, rectangular and square stock.
This script takes the capacities from bekamak.com for every model that has a product page
(tools/bekamak_crawl.py → /home/claude/bekamak/site/products.json) and fills the other rows only
where the catalogue left them empty, so no cell shows "—" when the manufacturer publishes a value.

Obvious typos on the site are corrected (a rectangular dimension at an angle can't exceed the
straight-cut dimension: "150 x 1000 mm" at +60° on the BMS 270DG is 150 x 100) and reported.

    python3 tools/bekamak_specs.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bekamak_features import slug_for, slug_index  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BK = "/home/claude/bekamak/site"


def num(t):
    m = re.search(r"([\d]+(?:[.,]\d+)?)", str(t))
    return float(m.group(1).replace(",", ".")) if m else None


def kw(t):
    """'1,5 kW' → 1.5 ; '1,1 - 1,5 kW' → '1.1-1.5' (the data format already used in the families)."""
    nums = re.findall(r"\d+(?:[.,]\d+)?", str(t))
    if not nums:
        return None
    vals = [float(x.replace(",", ".")) for x in nums]
    return vals[0] if len(vals) == 1 else f"{vals[0]:g}-{vals[1]:g}"


def fix_rect(rect, straight):
    """Divide a dimension by 10 when it is an obvious extra-zero typo (larger than the straight cut)."""
    if not rect or not straight:
        return rect, False
    fixed, note = list(rect), False
    for i in range(2):
        if fixed[i] > max(straight) * 1.05 and fixed[i] / 10 <= max(straight) * 1.05:
            fixed[i] = fixed[i] / 10; note = True
    return fixed, note


def main():
    products = json.load(open(os.path.join(BK, "products.json"), encoding="utf-8"))
    exact, relaxed = slug_index(products)
    fam_path = os.path.join(ROOT, "content", "families", "bandsaw.json")
    data = json.load(open(fam_path, encoding="utf-8"))
    changed = 0
    for fid, f in data["families"].items():
        if f.get("brand") != "bekamak":
            continue
        for m in f["specs"]["models"]:
            slug = slug_for(m["name"], exact, relaxed)
            sp = products.get(slug, {}).get("specs") if slug else None
            if not sp or not sp.get("capacity"):
                continue
            cap = m.setdefault("capacity_mm", {})
            straight = (sp["capacity"].get("0") or {}).get("rect")
            added = []
            for ang, c in sp["capacity"].items():
                rect, typo = fix_rect(c.get("rect"), straight)
                if typo:
                    print(f"  typo fixed on bekamak.com: {m['name']} {ang}° rect {c['rect']} → {rect}")
                vals = {"round": c.get("round"), "rect": rect, "square": c.get("square")}
                vals = {k: (int(v) if isinstance(v, float) and v.is_integer() else ([int(x) if float(x).is_integer() else x for x in v] if isinstance(v, list) else v)) for k, v in vals.items()}
                if ang not in cap:
                    added.append(ang)
                cap[ang] = vals
            rows = {k.lower(): v for k, v in sp.get("rows", {}).items()}
            if m.get("main_motor_kw") in (None, "") and rows.get("main drive motor"):
                m["main_motor_kw"] = kw(rows["main drive motor"])
            if m.get("hydraulic_motor_kw") in (None, "") and rows.get("hydraulic motor"):
                m["hydraulic_motor_kw"] = kw(rows["hydraulic motor"])
            if m.get("coolant_pump_kw") in (None, "") and rows.get("coolant pump"):
                m["coolant_pump_kw"] = kw(rows["coolant pump"])
            if not m.get("blade_speed_m_min") and rows.get("blade speed"):
                nums = re.findall(r"\d+(?:[.,]\d+)?", rows["blade speed"])
                m["blade_speed_m_min"] = "-".join(n.replace(",", ".") for n in nums) if nums else None
            if not m.get("band_mm") and rows.get("blade dimensions"):
                nums = re.findall(r"\d+(?:[.,]\d+)?", rows["blade dimensions"])
                if len(nums) == 3:
                    m["band_mm"] = [float(n.replace(",", ".")) if "," in n or "." in n else int(n) for n in nums]
            if not m.get("working_height_mm") and rows.get("working height"):
                m["working_height_mm"] = int(num(rows["working height"]))
            if not m.get("weight_kg") and rows.get("weight"):
                m["weight_kg"] = int(num(rows["weight"]))
            if not m.get("dims_mm") and all(rows.get(k) for k in ("length", "width", "height")):
                m["dims_mm"] = [int(num(rows[k])) for k in ("length", "width", "height")]
            # an accessory motor in the catalogue table is only "standard" when the accessory is: a chip
            # conveyor that bekamak.com lists under Optional Features gets its spec row marked (optional)
            other = m.get("other") or {}
            std_titles = " ".join(i["title"] for i in products[slug]["standard"]).lower()
            opt_titles = " ".join(i["title"] for i in products[slug]["optional"]).lower()
            for key in list(other):
                base = key.replace(" (optional)", "")
                if "chip conveyor" in base.lower():
                    optional = "chip conveyor" in opt_titles and "chip conveyor" not in std_titles
                    new_key = base + " (optional)" if optional else base
                    if new_key != key:
                        other[new_key] = other.pop(key)
                        print(f"  {m['name']}: spec row '{key}' → '{new_key}'")
            if added:
                changed += 1
                print(f"{fid:22s} {m['name']:16s} + angles {', '.join(added)}")
    json.dump(data, open(fam_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(changed, "models gained capacity rows")


if __name__ == "__main__":
    main()
