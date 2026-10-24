#!/usr/bin/env python3
"""Add (or refresh) the Bekamak products defined in tools/bekamak_extra.py — the GANTRY 2200XS and the vertical
band saws — in content/families/bandsaw.json WITHOUT regenerating the file (tools/bandsaw_data.py is a first
pass only; the JSON carries later enrichments).  Registers their bekamak.com photos in tools/image_map.json.

    python3 tools/bekamak_extra_apply.py        then: python3 tools/make_images.py --only <printed keys>
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bekamak_extra import EXTRA_MODELS, BANDSAW_FAMILIES, IMG_OPTS  # noqa: E402

SITE = json.load(open("/home/claude/bekamak/site/products.json", encoding="utf-8"))
IMG_DIR = "/home/claude/bekamak/site/img"
FAM_PATH = os.path.join(ROOT, "content", "families", "bandsaw.json")
MAP_PATH = os.path.join(ROOT, "tools", "image_map.json")

# which bekamak.com photos to show per model, in order (indexes into the crawl's image list), and their alts
PHOTOS = {
    "GANTRY 2200XS": [(0, "Bekamak GANTRY 2200XS gantry double-column band saw, Ø87″ (2200 mm) capacity, with the operator console")],
    "VB 0814-8": [(0, "Bekamak VB 0814-8 vertical block-cutting band saw: 26 ft block table and vertical saw head"), (1, "VB 0814-8 — saw head and chip conveyor at the end of the table")],
    "BMSY 613VT": [(2, "Bekamak BMSY 613VT vertical plate and block band saw, 23-5/8″ × 23-5/8″, with the control pendant"), (1, "BMSY 613VT — vertical blade, table and servo cutting feed"),
                   (0, "BMSY 613VT — right side with the table"), (3, "BMSY 613VT — front view"), (4, "BMSY 613VT — rear: blade wheel and hydraulic blade tension")],
    "BMSY 460VG": [(0, "Bekamak BMSY 460VG semi-automatic double-miter vertical band saw, Ø18″ (460 mm)"), (2, "BMSY 460VG — frame tilted for a miter cut"),
                   (3, "BMSY 460VG — right side with the hydraulic vise"), (1, "BMSY 460VG — front view"), (4, "BMSY 460VG — tilting frame at 60°, control panel"), (5, "BMSY 460VG — blade cover and nameplate")],
    "CROSS 0626VT": [(0, "Bekamak CROSS 0626VT fully automatic vertical plate band saw, 23-5/8″ × 102″ (600 × 2600 mm)"), (1, "CROSS 0626VT — feed table and vertical saw head from the rear"),
                     (2, "CROSS 0626VT — operator platform and feed table"), (3, "CROSS 0626VT — control panel on the operator platform"), (4, "CROSS 0626VT — hydraulic vises over the full table width"),
                     (5, "CROSS 0626VT — vise beam and feed table"), (6, "CROSS 0626VT — vertical blade head over the table")],
}


def norm(t):
    return t.upper().replace("-", "").replace(" ", "")


def main():
    fam = json.load(open(FAM_PATH, encoding="utf-8"))
    imap = json.load(open(MAP_PATH, encoding="utf-8"))
    site_by_name = {norm(v["title"]): v for v in SITE.values()}
    keys = []
    for F in BANDSAW_FAMILIES:
        models, images = [], []
        for name in F["models"]:
            models.append(dict(EXTRA_MODELS[name], name=name))
            rec = site_by_name.get(norm(name))
            if not rec:
                print("!! no bekamak.com page for", name); continue
            for i, alt in PHOTOS.get(name, []):
                fn = rec["images"][i]
                key = "bk-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + f"-{i + 1}"
                imap[key] = {"src": os.path.join(IMG_DIR, fn), "alt": alt, "section": "bandsaw", "trim": False, "quality": 82, **IMG_OPTS.get(name, {})}
                images.append(key); keys.append(key)
        rec0 = site_by_name.get(norm(F["models"][0])) or {}
        opt = []
        for it in rec0.get("optional", []):
            it = it.strip()
            if it and it not in opt and "-->" not in it:
                opt.append(it)
        fam["families"][F["id"]] = {
            "id": F["id"], "brand": "bekamak", "line": "premium", "group": F["group"],
            **({"subgroup": F["subgroup"]} if F.get("subgroup") else {}),
            "name": F["name"], "short": F["short"], "models_label": " · ".join(F["models"]),
            "summary": F["summary"], "features": F["features"], "optional": F.get("optional", opt),
            "images": images, "videos": F.get("videos", []), "headline": F["headline"],
            "specs": {"kind": "bandsaw", "models": models},
        }
        if F["id"] not in fam["order"]:
            # Bekamak families stay together, before the NovoTech value line
            last_bk = max(i for i, k in enumerate(fam["order"]) if fam["families"][k]["brand"] == "bekamak")
            fam["order"].insert(last_bk + 1, F["id"])
        print(f"{F['id']:26s} models={len(models)} images={len(images)}")
    json.dump(fam, open(FAM_PATH, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(imap, open(MAP_PATH, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("make_images keys:", ",".join(keys))


if __name__ == "__main__":
    main()
