#!/usr/bin/env python3
"""NovoTech mechanical shears page (novotech-mechanical-shears.html, under the shear-cutting hub): the direct-gear motorised
guillotine shears sold as NovoTech's premium line, made in Turkey — family set content/families/shears.json (which also holds the
Dener BS / DAS families for tools/dener_pages.py), photos from tools/saymak_photos.py (section 'shears').

    python3 tools/saymak_pages.py        # families + page + image_map entries (tools/saymak_keys.txt)
    python3 tools/make_images.py --only $(cat tools/saymak_keys.txt)
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401
from saymak_data import FAMILIES, P_SHEAR, BRAND
import dener_data as DN
import shear_nav as SN
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "shears"
SECTION = "Shears"
PDF_FILE = "files/NovoTech-Guillotine-Shears-2026.pdf"
PDF_DENER_FILE = "files/NovoTech-Dener-Hydraulic-Shears-2026.pdf"
BRAND_LINE = ("The SRGM guillotine shears are NovoTech's premium line: built in Turkey with European components to NovoTech's "
              "specification, and sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in Turkey", "text": "NovoTech's premium-line shears come from a Turkish builder that has made guillotine shears and "
          "sheet-metal machinery for more than 40 years — CE-certified, with European motors, gearboxes and electrical components."}

PAGE = dict(
    title="NovoTech Mechanical Shears, 1/8″ & 1/4″ · Premium Line",
    meta="Direct-gear SRGM guillotine shears made in Turkey: 1/8″ sheet to 10 ft and 1/4″ plate to 13.8 ft, 31 – 35 strokes/min, NC back gauge, return-to-sender.",
    h1="NovoTech mechanical guillotine shears — direct-gear SRGM, 1/8″ and 1/4″ to 13.8 ft, the premium line",
    intro="A metal shear (sheet metal shearing machine, guillotine shear, shear cutter) cuts plate and sheet to size in one stroke "
          "between a fixed bottom blade and a top blade on the moving beam — the first machine in every sheet-metal, HVAC, signage "
          "and fabrication shop, before the press brake. NovoTech's premium-line shears are direct-gear motorised guillotines: a "
          "4 to 15 HP motor drives the cutting beam through a gearbox and crank, with no hydraulic system to leak or warm up and no "
          "flywheel clutch to wear, for 31 to 35 strokes a minute. Six series, small to large: the light-type SRGM-H for 1/8″ (3 mm) "
          "mild steel and the SRGM for 1/4″ (6 mm) from 43″ to 13.8 ft; the SRGM-HFR and SRGM-FR with a return-to-sender sheet "
          "support that brings the cut piece back to the operator; and the SRGM-HCL and SRGM-CL built into cut-to-length coil lines. "
          "Welded steel frame, cutting beam in teflon slideways, high-carbon high-chrome blades with two and four cutting edges, "
          "front blade-gap adjustment, NC back gauge, shadow-line light and photocell guards. For plate from 1/4″ to 1-9/16″ see the Dener "
          "and NovoTech value-line hydraulic shears, for lighter sheet the value-line sheet metal shears — every line in one table on the "
          "shears overview. All supplied with a CSA-approved panel, installed and supported from Mississauga, ON, Canada.",
    points=["SRGM-H light type, 1/8″ × 3.6 – 10 ft, 35 strokes/min · SRGM standard, 1/4″ × 3.6 – 13.8 ft, 31 strokes/min",
            "SRGM-HFR / SRGM-FR with return-to-sender: the cut blank comes back to the front, off-cuts drop to the rear",
            "SRGM-HCL / SRGM-CL built into cut-to-length coil lines; Turkish-built with European motors, gearboxes and electrics"],
    hero="sm-srgm", minis=["sm-srgm-fr", "sm-srgm-h"],
    groups=[("shear-standard", "Direct-gear mechanical guillotine shears", "The light-type SRGM-H for 1/8″ sheet and the standard SRGM for 1/4″ plate, 43″ to 13.8 ft — the cutting beam driven through a gearbox, no hydraulics.", BRAND),
            ("shear-return", "Guillotine shears with return-to-sender", "The same two machines with a sheet support behind the blade that returns the cut piece to the operator — blanks and strips cut by one person.", BRAND),
            ("shear-line", "Shears for cut-to-length lines", "Open at the rear for the strip from a decoiler and straightener, cut to length by the line control.", BRAND)],
    faq=[{"q": "Mechanical or hydraulic shear — which is better?",
          "a": "For sheet to 1/4″ a direct-gear mechanical shear is the faster and simpler machine: 31 – 35 strokes a minute from a motor and gearbox, no hydraulic power pack, no oil to heat up, no valves or seals to service, and the same cut quality on the first and the thousandth stroke. Hydraulic shears earn their price from 3/8″ plate upwards, where the beam needs tonnage rather than speed — those are the Dener BS / DAS and the NovoTech value-line QC12K / Q11K on their own pages; the shears overview compares all four lines in one table."},
         {"q": "What does direct-gear mean?",
          "a": "The motor drives the cutting beam through a gearbox and crank directly — there is no flywheel and clutch between them, as on an older mechanical shear. The beam makes one stroke per pedal press, stops at top dead centre and cannot repeat a stroke on its own; the motor runs only while the beam cycles, which also makes the machine quiet and economical."},
         {"q": "How is the capacity rated, and what about stainless and aluminum?",
          "a": "Capacities are the maker's ratings for mild steel over the full blade length: 1/4″ (6 mm) on the SRGM 1100 and 1360, 3/16″ on the 1560, 5/32″ on the 2060 – 3200 and 1/8″ on the 4200; 1/8″ (3 mm) on the SRGM-H range. Stainless steel is harder to shear, so count on about 60 % of the mild-steel thickness — 14 ga stainless on a 1/8″ machine, 11 ga on a 1/4″ machine; aluminum cuts to the full rated thickness and more."},
         {"q": "Which length do I need — 4 ft, 5 ft, 8 ft, 10 ft?",
          "a": "The model number is the maximum shearing length in millimetres: 1100 = 43″, 1360 = 53.5″ (a 4 × 8 sheet cut across), 1560 = 61″ (5 ft), 2060 = 81″ (6.8 ft), 2560 = 101″ (8.4 ft, a 4 × 8 sheet lengthwise), 3060 = 10 ft, 3200 = 10.5 ft, 4200 = 13.8 ft. Most sheet-metal shops run a 2560 or 3060 so a full sheet is cut both ways; HVAC and signage shops are well served by the 1360 – 2060."},
         {"q": "What is the back gauge, and is it NC?",
          "a": "The back gauge is the stop behind the blade that sets the width of the cut strip. The SRGM, SRGM-FR and SRGM-HFR come with an NC-controlled back gauge with 29.5″ stroke — the operator keys in the dimension on the controller and the gauge moves there; a 39.4″ stroke, the ELGO P40T or FUJI Monitouch touch-screen control and a front-operated manual gauge with ball screw are options. The SRGM-H has a manual back gauge as standard and the NC gauge as an option."},
         {"q": "What does return-to-sender do?",
          "a": "On the FR and HFR series a sheet support behind the blade tilts after the cut and carries the cut piece back under the blade to the front of the machine, while off-cuts fall to the rear. One operator cuts blanks and strips without walking round the machine or needing a helper at the back — the biggest time saver on a shear that cuts small parts all day. The standard version is manual; the pneumatic version adds return-to-rear for scrap."},
         {"q": "How long do the blades last, and can they be turned?",
          "a": "The blades are high-carbon, high-chrome tool steel: the top blade has two cutting edges and the bottom blade four, so each is turned to a fresh edge before it needs regrinding. The blade gap is set from the front of the machine to the sheet thickness, which keeps the edges sharp and the cut burr-free. Replacement blades are stocked in Mississauga, ON, Canada."},
         {"q": "Can it cut at an angle?",
          "a": "Yes — the optional 0 – 180° angular cutting device on the table positions the sheet for mitre and trapezoid cuts against the squaring arm; the standard squaring arm has a T-slot, a stopper and a ruler for square cuts."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about metal shears",
    related_pages=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "compact-hydraulic-press-brakes.html", "label": "Compact hydraulic press brakes"},
                   {"href": "corner-notcher.html", "label": "Corner notchers"}, {"href": "circle-cutters-and-seamers.html", "label": "Circle shears & flanging machines"},
                   {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}],
    related_title="More sheet-metal cutting and forming machinery from NovoTech",
)


def pdf_entry(file=PDF_FILE, label="Download the mechanical guillotine shears brochure"):
    f = os.path.join(ROOT, "src", file)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": file, "label": label, "size": size}


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "saymak")
    keys = []
    for key, p in load_module("saymak_photos").PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")]
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        e = {"src": f"tools/src-images/saymak/{key}{ext}", "alt": p["alt"], "section": "shears", "trim": ext == ".png", "quality": 82}
        if p.get("cutout") is False:
            e["cutout"] = False
        e.update(p.get("imap", {}))
        imap[key] = e
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "saymak_keys.txt"), "w").write(",".join(keys))
    return keys


def build():
    pdf = pdf_entry()
    pdf_dn = pdf_entry(PDF_DENER_FILE, "Download the Dener hydraulic shears brochure")
    fams = [dict(f, pdf=pdf) for f in FAMILIES] + [dict(f, pdf=pdf_dn) for f in DN.SHEAR_FAMILIES]
    write_families(SET, fams)
    write_category(P_SHEAR, PAGE, fams, SET, SN.SECTION, hub=SN.hub(), siblings=SN.siblings(),
                   extra={"hero_brand_line": BRAND_LINE, "catalogue_pdf": pdf, "origin_feature": ORIGIN, "nav_label": "NovoTech mechanical shears"})
    keys = register_images()
    used = {k for f in FAMILIES for k in f["images"]} | {PAGE["hero"]} | set(PAGE["minis"])
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on the page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    print(f"shears page · families: {len(fams)} · models: {sum(len(f['specs']['models']) for f in fams)} · images: {len(keys)}")


if __name__ == "__main__":
    build()
