#!/usr/bin/env python3
"""NovoTech value-line shears for the sheet-metal shop, built in China by TTMC and sold under NovoTech's name without the
supplier's brand — the families only (content/families/ttmc.json); they are shown on the hydraulic and mechanical shear pages
(tools/shear_types.py; the sheet-metal-shears page was merged into the two, Nov 7 2026).  Photos from tools/ttmc_photos.py and
tools/ttmc_hires_photos.py (section 'shears').

    python3 tools/ttmc_photos.py                   # crops from the catalogue page rasters → tools/src-images/ttmc
    python3 tools/ttmc_pages.py                    # families + image_map entries (tools/ttmc_keys.txt)
    python3 tools/make_images.py --only $(cat tools/ttmc_keys.txt)
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401
import shear_nav as SN
import ttmc_data as D
import ttmc_photos as PH
import ttmc_hires_photos as HP   # the supplier's high-resolution shear photos (Oct 31 2026), in tools/src-images/ttmc-hires
import ttmc_more_data2 as D2   # EBQ01 motorized bench shears (value line, sample photos in section 'ttmc-more')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "ttmc"
BRAND = D.BRAND
PDF_FILE = "files/NovoTech-Sheet-Metal-Shears-2026.pdf"
BRAND_LINE = ("NovoTech's value-line sheet metal shears are built in China to NovoTech's specification and sold under NovoTech's name — "
              "with a CSA-approved panel, a 1-year warranty and parts and service from Mississauga, ON, Canada.")
ORIGIN = {"title": "NovoTech value line — built in China", "text": "Built by a sheet-metal machinery maker that exports shears, press brakes and notchers worldwide; "
          "inspected before shipping, wired for Canadian voltage with a CSA-approved panel, and supported by NovoTech's technicians in Mississauga, ON, Canada."}
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}

# the photos the shear pages lead with besides the family galleries (checked to exist below)
PAGE = dict(hero="tt-q11a", minis=["tt-hq11", "tt-q11nc"])

def pdf_entry(file=PDF_FILE, label="Download the sheet metal shears brochure"):
    f = os.path.join(ROOT, "src", file)
    if not os.path.exists(f):
        return None
    return {"file": file, "label": label, "size": f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units"}


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "ttmc")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")]
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/ttmc/{key}{ext}", "alt": p["alt"], "section": "shears", "trim": False, "quality": 82, "cutout": bool(p.get("cutout"))}
        keys.append(key)
    # the supplier's high-resolution photos (the owner's WeTransfer, Oct 31 2026) replace the catalogue crops, or add a photo for a model
    for key, p in HP.PHOTOS.items():
        if not key.startswith("tt-"):
            continue
        src = f"tools/src-images/ttmc-hires/{key}.jpg"
        if not os.path.exists(os.path.join(ROOT, src)):
            print("!! missing high-resolution photo for", key, "— run tools/ttmc_hires_photos.py", key)
            continue
        imap[key] = {"src": src, "alt": p["alt"], "section": "shears", "trim": True, "quality": 82, "cutout": not p.get("detail"), "cut_size": 1024}
        if key not in keys:
            keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "ttmc_keys.txt"), "w").write(",".join(keys))
    return keys


def build():
    pdf = pdf_entry()
    fams = [dict(f, pdf=pdf) for f in D.FAMILIES] + [dict(f) for f in D2.SHEAR]
    write_families(SET, fams)
    # the shear families are shown on the hydraulic and mechanical shear pages (tools/shear_types.py), not on a supplier page
    keys = register_images()
    used = {k for f in FAMILIES_IMAGES() for k in f} | {PAGE["hero"]} | set(PAGE["minis"])     # the bench shears' photos are registered by ttmc_more_pages.py
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on the page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    print(f"value-line shears · families: {len(fams)} · models: {sum(len(f['specs']['models']) for f in fams)} · images: {len(keys)}")


def FAMILIES_IMAGES():
    return [f["images"] for f in D.FAMILIES]


if __name__ == "__main__":
    build()
