#!/usr/bin/env python3
"""Cevisa (Vitoria, Spain) plate bevelling machines — sold under their own brand.  Page texts for plate-beveler (the old
site's URL, kept: it ranks for "plate beveling machine", "plate bevelling machine" and "plate cold bevelling machine"),
image registration (section 'cevisa') and the NovoTech-format brochure spec:

    python3 tools/cevisa_photos.py                   # cevisa.net cut-outs and catalogue photos → tools/src-images/cevisa
    python3 tools/cevisa_pages.py                    # image_map entries (tools/cevisa_keys.txt), the page, brochure spec
    python3 tools/make_images.py --only $(cat tools/cevisa_keys.txt)
    python3 tools/brochure/build_brochure.py tools/brochure/specs/cevisa.json
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401
import cevisa_data as D
import cevisa_photos as PH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "cevisa"
BRAND = D.BRAND
PDF_FILE = "files/NovoTech-Cevisa-Plate-Bevelling-Machines-2026.pdf"
PDF_LABEL = "Download the Cevisa plate beveller brochure"

BRAND_LINE = ("Cevisa bevellers are made in Vitoria, Spain, by CEVISA — plate bevelling machines since 1969, ISO 9001, exported to more "
              "than 60 countries. Sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in Spain by Cevisa", "text": "CEVISA has built self-feeding plate and tube bevellers in Vitoria, Spain, since 1969 — "
          "patented shearing and milling bevellers, an ISO 9001 quality system and 80 % of production exported to more than 60 countries."}
INTRO_VIDEO = {"intro_video": {"id": "5rcKh9djNxA", "title": "Cevisa bevelling machines — factory introduction", "thumb": "video-5rcKh9djNxA", "duration": "PT4M23S"},
               "intro_video_heading": "Inside the factory — Cevisa in Vitoria, Spain",
               "intro_video_text": "A tour of the Cevisa plant in Vitoria, where the shearing and milling bevellers on this page are designed and built."}


def pdf(fid=None):
    f = os.path.join(ROOT, "src", PDF_FILE)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": PDF_FILE, "label": PDF_LABEL, "size": size}


def families(page=None):
    return [dict(f, pdf=pdf(f["id"])) for f in D.FAMILIES if page is None or f["page"] == page]


PAGE = dict(
    title="Plate Beveling Machines, Plate 1/8″ – 4-3/4″ | NovoTech",
    meta="Self-feeding cold bevellers from Spain: Cevisa CHP shearing bevellers for V, X, K and Y bevels to 1-1/8″, and milling bevellers for Hardox to 3-15/16″.",
    h1="Plate bevelling machines — portable cold bevellers for plate and pipe, 1/8″ to 4-3/4″ thick",
    intro="A plate bevelling machine prepares plate and pipe edges for welding: it sits on the edge, feeds itself along it and cuts the "
          "bevel cold — V, X, K or Y, at the angle and depth the weld procedure calls for — so there is no flame cut to clean, no "
          "heat-affected zone, no slag and no hours of grinding. NovoTech sells the bevellers of CEVISA, built in Vitoria, Spain, since "
          "1969 and used by boiler and tank makers, structural fabricators, shipyards, wind-tower and offshore builders in more than 60 "
          "countries. On this page, small to large: the CHP 7, CHP 12 and CHP 12 INV standard shearing bevellers for plate, tube and "
          "discs from 1/8″ to 1-9/16″ thick; the CHP 12G, CHP 21G and CHP 21G INV with the bevel angle adjustable from 20° to 45°; the "
          "CHP 12G REV and CHP 21G REV that turn over to bevel the lower edge without turning the plate; and the CHP 30G, CHP 60G, CHP "
          "60G INV and CHP 100G milling bevellers, which machine bevels up to 3-15/16″ wide at 15° to 70° in any material — Hardox, "
          "Armox, duplex and stainless included — on plate up to 4-3/4″. Supplied with a CSA-approved panel, installed and supported "
          "from Mississauga, ON.",
    points=["Shearing bevellers CHP 7 – CHP 21G: plate and tube 1/8″ – 1-15/16″, bevels to 1-1/8″ at up to 8.5 ft/min",
            "Adjustable angle (20° – 45°), inverted (INV) and reversible (REV) models for X and K bevels without turning the plate",
            "Milling bevellers CHP 30G – CHP 100G: machined bevels to 3-15/16″, 15° – 70°, any material, plate to 4-3/4″"],
    hero="cv-chp12", minis=["cv-chp21g-rev", "cv-chp60g"],
    groups=[("cevisa-shear", "Cevisa shearing bevellers",
             "Self-feeding bevellers that shear the bevel off cold with a resharpenable cutter, small to large: standard, adjustable-angle "
             "and reversible models for plate and tube from 1/8″ to 1-15/16″.", BRAND),
            ("cevisa-mill", "Cevisa milling bevellers",
             "Portable milling machines that machine the bevel with an insert head — any material, 15° to 70°, transition and J bevels, "
             "on plate to 4-3/4″.", BRAND)],
    faq=[{"q": "What does a plate bevelling machine do?",
          "a": "It cuts the bevel a full-penetration weld needs on the edge of a plate or pipe — V, X, K or Y, at a set angle and depth — "
               "and feeds itself along the edge while it cuts. Compared with a cutting torch and a grinder it leaves a clean, even "
               "bevel with no heat-affected zone, no slag and no scale to grind off, ready to weld, and it does it at several feet a "
               "minute with one operator who does not have to hold or guide it."},
         {"q": "Shearing or milling beveller?",
          "a": "A shearing beveller (CHP 7 to CHP 21G) takes the bevel off with a resharpenable shear cutter: the fastest and lowest-cost "
               "bevel per foot in mild steel, stainless and aluminum, on plate and tube up to 1-15/16″ and bevels up to 1-1/8″. A "
               "milling beveller (CHP 30G, 60G, 100G) machines the bevel with a milling head: a machined finish in any material — "
               "Hardox, Armox, duplex, super duplex — at the same capacity, angles from 15° to 70°, transition and J bevels, and bevels "
               "up to 3-15/16″ wide on plate to 4-3/4″."},
         {"q": "Which size do I need?",
          "a": "Start from the widest bevel face and the thickest plate you prepare. CHP 7: bevels to 3/8″ on 1/8″ – 5/8″ plate and thin "
               "tube, also aluminum. CHP 12 / 12G: 11/16″ bevels on 1/4″ to 1-9/16″ (12G 1-3/16″). CHP 21G: 1-1/8″ bevels on 3/8″ – "
               "1-15/16″ plate, for continuous production. CHP 30G: 1-3/8″ machined bevels to 1-15/16″ plate; CHP 60G: 2-3/8″ on plate "
               "to 2-3/4″ (3-15/16″ special); CHP 100G: 3-15/16″ on plate to 4-3/4″. In stainless steel the shearing machines take "
               "80 – 90 % of their mild-steel bevel in several runs and about two-thirds in one run; the milling machines keep "
               "their full capacity."},
         {"q": "What do INV and REV mean?",
          "a": "An INV (inverted) machine works upside down and bevels the lower edge of the plate, so the lower half of an X or K bevel "
               "is cut without turning a heavy plate over; running an INV under its standard twin (CHP 12 + 12 INV, 21G + 21G INV, 60G + "
               "60G INV) cuts both bevels in one pass. A REV (reversible) machine turns over on its frame in under a minute and does "
               "both bevels by itself — one machine, one operator."},
         {"q": "Can it bevel pipe and discs?",
          "a": "Yes, the shearing models bevel tube and pipe as well as plate: from Ø3-15/16″ inside (Ø5-7/8″ on the CHP 21G family), on "
               "the inside or the outside, with the pipe horizontal or vertical, and discs and tank heads from Ø13-3/4″. The milling "
               "bevellers are for plate, flat bar and square bar."},
         {"q": "What does it cost to run?",
          "a": "Little: the shearing cutters last about 3,300 ft (1,000 m) of bevel and are resharpened, Cevisa rates the machines "
               "maintenance-free, and a 20 ft plate edge is bevelled in under three minutes on a CHP 12. The milling heads use standard "
               "indexable inserts. We quote cutters, inserts and angle devices with the machine."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about plate bevelling machines",
    related_pages=[{"href": "welding-positioners.html", "label": "Welding positioners"}, {"href": "pipe-notcher.html", "label": "Tube notchers"},
                   {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring & finishing"},
                   {"href": "plate-rollers.html", "label": "Plate rollers"}, {"href": "hydraulic-press.html", "label": "Hydraulic presses"}],
    related_title="More fabrication machinery from NovoTech",
)

# ------------------------------------------------------------------------------------------------ brochure
ABOUT_CEVISA = ("NovoTech sells, installs and supports Cevisa bevellers in Canada from Mississauga, Ontario — the machine and cutters chosen "
                "for your plates and bevels, a CSA-approved panel, operator training, a 1-year warranty and parts and technical support in "
                "Canada.")
BROCHURE = dict(
    title="Plate bevelling machines",
    subtitle="Cevisa CHP 7, CHP 12 and CHP 12 INV · CHP 12G, CHP 21G and CHP 21G INV adjustable · CHP 12G REV and CHP 21G REV reversible · CHP 30G, CHP 60G, CHP 60G INV and CHP 100G milling bevellers",
    cover_line="Cevisa · made in Spain · sold & serviced in Canada by NovoTech", range_label="Cevisa plate bevellers", about_for="Cevisa plate bevellers",
    about_kicker="Cevisa · Vitoria, Spain", about_title="Cold bevels for welding, from 1/8″ to 4-3/4″ plate",
    about_text=["CEVISA has designed and built self-feeding bevelling machines in Vitoria, Spain, since 1969, and exports 80 % of its "
                "production to more than 60 countries. Its shearing bevellers take the bevel off cold with a resharpenable cutter — V, X, "
                "K and Y bevels on plate, tube and discs up to 1-15/16″ thick — and its milling bevellers machine bevels up to 3-15/16″ "
                "wide in any material, from mild steel to Hardox, at 15° to 70°. Inverted and reversible models bevel the lower edge "
                "without turning the plate.", ABOUT_CEVISA],
    country="Spain", families=[f["id"] for f in D.FAMILIES], family_sets=["cevisa"],
    groups=[{"title": "Shearing bevellers", "families": ["cevisa-std", "cevisa-adj", "cevisa-rev"]}, {"title": "Milling bevellers", "families": ["cevisa-mill"]}],
    cover_photos=["cv-chp12", "cv-chp21g-rev", "cv-chp60g"], out="src/" + PDF_FILE)


def write_brochure_specs():
    d = os.path.join(ROOT, "tools", "brochure", "specs")
    spec = dict(BROCHURE, single_phase=False, year="2026", made_in="Made in Spain by Cevisa — ISO 9001")
    json.dump(spec, open(os.path.join(d, "cevisa.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "cevisa")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")]
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/cevisa/{key}{ext}", "alt": p["alt"], "section": "cevisa", "trim": False, "quality": 82,
                     "cutout": bool(p.get("cutout"))}
        keys.append(key)
    imap["cevisa-logo"] = {"src": "tools/src-images/cevisa-logo.png", "alt": "Cevisa", "section": "site", "trim": True, "quality": 90, "cutout": False}
    keys.append("cevisa-logo")
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "cevisa_keys.txt"), "w").write(",".join(keys))
    return keys


def video_ids():
    return list(dict.fromkeys([v["id"] for f in D.FAMILIES for v in f["videos"]] + [INTRO_VIDEO["intro_video"]["id"]]))


def build():
    fams = families(D.P_BEVEL)
    write_families(SET, fams)
    write_category(D.P_BEVEL, PAGE, fams, SET, "Plate bevelers",
                   extra={"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **INTRO_VIDEO, "catalogue_pdf": pdf(), "catalogue_pdfs": None,
                          "nav_label": "Plate bevelers"})
    keys = register_images()
    write_brochure_specs()
    used = {k for f in D.FAMILIES for k in f["images"]} | {PAGE["hero"]} | set(PAGE["minis"]) | set(BROCHURE["cover_photos"])
    unused = sorted(set(keys) - used - {"cevisa-logo"})
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        print("!! image keys without a photo (export still running?):", missing)
    open(os.path.join(ROOT, "tools", "cevisa_vids.txt"), "w").write(" ".join(video_ids()))
    print(f"title {len(PAGE['title'])} · meta {len(PAGE['meta'])}")
    print(f"cevisa: {len(D.FAMILIES)} families · {sum(len(f['specs']['models']) for f in D.FAMILIES)} models · images: {len(keys)} · videos: {len(video_ids())}")


if __name__ == "__main__":
    build()
