#!/usr/bin/env python3
"""Add (or refresh) the Bekamak products defined in tools/bekamak_extra.py — the GANTRY 2200XS, the vertical
band saws and the bekamak.com-only models (BMSO 320S, TERRA 6, BMH 170, plus the BMSO 460CS / 1313CS inside the
CS family) — in content/families/bandsaw.json WITHOUT regenerating the file (tools/bandsaw_data.py is a first
pass only; the JSON carries later enrichments).  Registers their bekamak.com photos in tools/image_map.json and
builds the Standard / Optional Features tiles ("model_features") of the new models from the bekamak.com crawl
(/home/claude/bekamak/site/products.json + details.json), reusing a feature photo that is already on the site
(same picture under another bekamak.com file name) instead of adding it twice.

    python3 tools/bekamak_extra_apply.py        then: python3 tools/make_images.py --only <printed keys>
"""
import json
import os
import re
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bekamak_extra import EXTRA_MODELS, BANDSAW_FAMILIES, CS_ADDITIONS, IMG_OPTS  # noqa: E402
from bekamak_features import clean_title, image_key  # noqa: E402

BK = "/home/claude/bekamak/site"
SITE = json.load(open(os.path.join(BK, "products.json"), encoding="utf-8"))
DETAILS = json.load(open(os.path.join(BK, "details.json"), encoding="utf-8"))
IMG_DIR = os.path.join(BK, "img")
FAM_PATH = os.path.join(ROOT, "content", "families", "bandsaw.json")
MAP_PATH = os.path.join(ROOT, "tools", "image_map.json")
HASH_CACHE = os.path.join(BK, "det_hash.json")

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
    "BMSO 320S": [(0, "Bekamak BMSO 320S fully automatic servo-feed band saw, Ø12-5/8″ (320 mm), with the Omron touch-screen control"),
                  (1, "BMSO 320S — rear view: blade wheels, electrical cabinet and the servo shuttle vise")],
    "TERRA 6": [(0, "Bekamak TERRA 6 high-speed fully automatic band saw, Ø26″ (660 mm): enclosed cabin and PC-based control"),
                (1, "TERRA 6 — front quarter view of the cabin; blade speed to 1,970 ft/min (600 m/min)"), (2, "TERRA 6 — left side of the enclosure")],
    "BMH 170": [(1, "Bekamak BMH 170 hydraulic power hacksaw, Ø6-3/4″ (170 mm), with the vise and roller table"),
                (2, "BMH 170 — front quarter view with the material length stop"), (0, "BMH 170 — right side: reciprocating frame and hydraulic feed cylinder")],
}


def norm(t):
    return t.upper().replace("-", "").replace(" ", "")


def site_slug(name, site_by_name):
    """bekamak.com record for a model name; slugs with a random suffix (bmso-460cs-nc_HV61W) match by title."""
    return site_by_name.get(norm(name))


def photo_key(name, i):
    return "bk-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + f"-{i + 1}"


# ---- feature photos: reuse the picture when it is already on the site under another file name ------------------
def dhash(path, size=12):
    im = Image.open(path).convert("L").resize((size + 1, size), Image.LANCZOS)
    a = np.asarray(im).astype(int)
    return (a[:, 1:] > a[:, :-1]).flatten()


def existing_hashes(imap):
    cache = json.load(open(HASH_CACHE)) if os.path.exists(HASH_CACHE) else {}
    out = {}
    for k, e in imap.items():
        if not k.startswith("bk-det-"):
            continue
        src = e["src"] if os.path.isabs(e["src"]) else os.path.join(ROOT, e["src"])
        if not os.path.exists(src):
            continue
        if src not in cache:
            cache[src] = "".join("1" if b else "0" for b in dhash(src))
        out[k] = np.array([c == "1" for c in cache[src]])
    json.dump(cache, open(HASH_CACHE, "w"))
    return out


def feature_tiles(model, slug, imap, hashes, new_keys):
    """model_features entry for one model from the crawl: captions in products.json (text list, often doubled),
    photos in details.json ({title, file, kind})."""
    rec = SITE[slug]
    det = {(d["kind"], d["title"].strip().lower()): d["file"] for d in DETAILS.get(slug, [])}
    entry = {"model": model, "slug": slug, "standard": [], "optional": []}
    for kind, dkind in (("standard", "standard"), ("optional", "option")):
        seen, seen_imgs = set(), set()
        for raw in rec.get(kind, []):
            raw = raw.replace("​", "").strip()
            if not raw or "-->" in raw:
                continue
            title = clean_title(raw)
            if title.lower() in seen:
                continue
            seen.add(title.lower())
            key = None
            file = det.get((dkind, raw.lower()))
            if file and os.path.exists(os.path.join(BK, "img", "details", file)):
                src = os.path.join(BK, "img", "details", file)
                h = dhash(src)
                dup = next((k for k, hk in hashes.items() if (hk != h).sum() <= 8), None)
                key = dup or image_key(file)
                if key in seen_imgs:
                    continue
                seen_imgs.add(key)
                if key not in imap:
                    imap[key] = {"src": src, "alt": f"Bekamak {model} — {title[0].lower() + title[1:] if title[1:2].islower() else title}",
                                 "section": "bandsaw", "trim": False, "quality": 82}
                    hashes[key] = h
                    new_keys.append(key)
            entry[kind].append({"title": title, "image": key})
    return entry


def main():
    fam = json.load(open(FAM_PATH, encoding="utf-8"))
    imap = json.load(open(MAP_PATH, encoding="utf-8"))
    site_by_name = {norm(v["title"]): v for v in SITE.values()}
    slug_by_name = {norm(v["title"]): s for s, v in SITE.items()}
    hashes = existing_hashes(imap)
    keys = []

    def register_photos(name):
        rec = site_slug(name, site_by_name)
        if not rec:
            print("!! no bekamak.com page for", name); return []
        out = []
        for i, alt in PHOTOS.get(name, []):
            fn = rec["images"][i]
            key = photo_key(name, i)
            imap[key] = {"src": os.path.join(IMG_DIR, fn), "alt": alt, "section": "bandsaw", "trim": False, "quality": 82, **IMG_OPTS.get(name, {})}
            out.append(key); keys.append(key)
        return out

    for F in BANDSAW_FAMILIES:
        models, images, mf = [], [], []
        for name in F["models"]:
            models.append(dict(EXTRA_MODELS[name], name=name))
            images += register_photos(name)
            slug = slug_by_name.get(norm(name))
            if slug and name in ("BMSO 320S", "TERRA 6", "BMH 170"):
                mf.append(feature_tiles(name, slug, imap, hashes, keys))
        rec0 = site_slug(F["models"][0], site_by_name) or {}
        opt = []
        for it in rec0.get("optional", []):
            it = it.strip()
            if it and it not in opt and "-->" not in it:
                opt.append(it)
        old = fam["families"].get(F["id"], {})
        fam["families"][F["id"]] = {
            "id": F["id"], "brand": "bekamak", "line": "premium", "group": F["group"],
            **({"subgroup": F["subgroup"]} if F.get("subgroup") else {}),
            "name": F["name"], "short": F["short"], "models_label": " · ".join(F["models"]),
            "summary": F["summary"], "features": F["features"], "optional": F.get("optional", opt),
            "images": images, "videos": F.get("videos", []), "headline": F["headline"],
            "specs": {"kind": "bandsaw", "models": models},
            **({"model_features": mf} if mf else ({"model_features": old["model_features"]} if old.get("model_features") else {})),
        }
        if F["id"] not in fam["order"]:
            if F.get("after") and F["after"] in fam["order"]:
                fam["order"].insert(fam["order"].index(F["after"]) + 1, F["id"])
            else:
                # Bekamak families stay together, before the NovoTech value line
                last_bk = max(i for i, k in enumerate(fam["order"]) if fam["families"][k]["brand"] == "bekamak")
                fam["order"].insert(last_bk + 1, F["id"])
        print(f"{F['id']:26s} models={len(models)} images={len(images)} feature tiles={sum(len(e['standard']) + len(e['optional']) for e in mf)}")

    # ---- models added to catalogue-built families (BMSO 460CS / 1313CS in the CS family)
    for fid, add in CS_ADDITIONS.items():
        f = fam["families"][fid]
        names = [m["name"] for m in f["specs"]["models"]]
        for name, follows, photos in add["add"]:
            m = dict(EXTRA_MODELS[name], name=name)
            if name in names:
                f["specs"]["models"][names.index(name)] = m
            else:
                pos = names.index(follows) + 1 if follows in names else len(names)
                f["specs"]["models"].insert(pos, m); names.insert(pos, name)
            rec = site_slug(name, site_by_name)
            new_imgs = []
            for i, alt in photos:
                key = photo_key(name, i)
                imap[key] = {"src": os.path.join(IMG_DIR, rec["images"][i]), "alt": alt, "section": "bandsaw", "trim": False, "quality": 82}
                new_imgs.append(key); keys.append(key)
            f["images"] = [k for k in f["images"] if k not in new_imgs] + new_imgs
            slug = slug_by_name.get(norm(name))
            f.setdefault("model_features", [])
            f["model_features"] = [e for e in f["model_features"] if e["model"] != name]
            if slug:
                f["model_features"].append(feature_tiles(name, slug, imap, hashes, keys))
            # keep the feature tiles in spec-table order
            order = {n: i for i, n in enumerate(names)}
            f["model_features"].sort(key=lambda e: order.get(e["model"], 99))
        for k in ("models_label", "summary"):
            if add.get(k):
                f[k] = add[k]
        for v in add.get("videos", []):
            if v["id"] not in {x["id"] for x in f.get("videos", [])}:
                f.setdefault("videos", []).append(v)
        print(f"{fid:26s} models={len(f['specs']['models'])} images={len(f['images'])} videos={len(f.get('videos', []))}")

    json.dump(fam, open(FAM_PATH, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(imap, open(MAP_PATH, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("make_images keys:", ",".join(keys))


if __name__ == "__main__":
    main()
