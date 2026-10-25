#!/usr/bin/env python3
"""The shear hub (shear-cutting.html, hub.html template): four product pages — Dener hydraulic shears (premium), NovoTech
mechanical shears (premium, Saymak-built), NovoTech hydraulic shears (value, QC12K / Q11K) and NovoTech sheet metal shears
(value, TTMC-built) — introduced separately with their family cards, plus the whole range in one capacity table.

The hub reads the families the four generators wrote (content/families/shears.json, value-sheet.json, ttmc.json) into its
own set content/families/all-shears.json, so run it AFTER tools/saymak_pages.py, tools/dener_pages.py, tools/vl_sheet_pages.py
and tools/ttmc_pages.py:

    python3 tools/shear_hub.py
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_families, write_hub  # noqa: F401
import shear_nav as SN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "all-shears"

# (family set, page slug, family ids in display order)
SOURCES = [("shears", "dener-shears", ["dn-bs", "dn-das"]),
           ("shears", "novotech-mechanical-shears", ["nt-shear-srgm-h", "nt-shear-srgm", "nt-shear-srgm-hfr", "nt-shear-srgm-fr", "nt-shear-srgm-hcl", "nt-shear-srgm-cl"]),
           ("value-sheet", "hydraulic-shearing-machine", ["vl-qc12k", "vl-q11k"]),
           ("ttmc", "sheet-metal-shears", ["tt-ps", "tt-hq01", "tt-ths", "tt-hq11", "tt-q11", "tt-q11nc", "tt-q11-mech"])]

HUB_PAGE = dict(
    title="Metal Shear Machines, 16 ga to 1-9/16″ Plate | NovoTech",
    meta="Every metal shear sold by NovoTech in Canada: Dener hydraulic shears, NovoTech mechanical shears, value-line hydraulic plate shears and sheet metal shears.",
    h1="Metal shear machines — sheet metal shears, mechanical guillotines and hydraulic plate shears, 16 ga to 1-9/16″",
    intro="A metal shear (sheet metal shearing machine, guillotine shear, shear cutter) cuts plate and sheet to size in one stroke between a "
          "fixed bottom blade and a top blade on the moving beam — the first machine in every sheet-metal, HVAC, signage and fabrication shop, "
          "before the press brake. NovoTech sells four lines of shears in Canada, each on its own page: the Dener hydraulic shears — the premium "
          "plate shears made in Turkey, BS / BSY swing beam to 5/8″ and the DAS CNC guillotine to 3/4″ × 20 ft; NovoTech's premium-line "
          "mechanical shears — direct-gear SRGM guillotines, 1/8″ and 1/4″ to 13.8 ft, built in Turkey; NovoTech's value-line hydraulic shears "
          "— QC12K swing beam and Q11K guillotine from 5/32″ to 1-9/16″ and 26 ft, built in China with Estun controls; and NovoTech's value-line "
          "sheet metal shears — pneumatic, light hydraulic, electric and flywheel mechanical shears from 16 ga to 3/8″ for the sheet-metal "
          "shop. Below, each line in brief and every model in one table of capacity, length, strokes, motor and weight; every machine comes "
          "with a CSA-approved panel, a 1-year warranty and installation, training and parts from Mississauga, ON.",
    points=["Dener premium line: BS / BSY hydraulic swing beam 1/4″ – 5/8″ × 6.8 – 13.5 ft; DAS CNC guillotine with variable angle 1/4″ – 3/4″ × 10 – 20 ft",
            "NovoTech premium line: SRGM direct-gear mechanical shears 1/8″ × 3.6 – 10 ft and 1/4″ × 3.6 – 13.8 ft, 31 – 35 strokes/min, return-to-sender versions",
            "NovoTech value line: QC12K / Q11K hydraulic plate shears 5/32″ – 1-9/16″ × 8 – 26 ft; sheet metal shears 16 ga – 3/8″ × 39 – 120″"],
    hero="sm-srgm", minis=["dn-das-1", "vl-qc12k-1"],
    range_cols=["Capacity (mild steel)", "Shearing length", "Strokes / min", "Motor", "Weight"],
    range_lead="Every shear model NovoTech sells, in one table: mild-steel capacity, shearing length, strokes per minute, motor and weight. Each row links to the full specification table on the line's page.",
    range_caption="Metal shears supplied by NovoTech — Dener, NovoTech premium line and NovoTech value line",
    range_note="Capacities are the manufacturers' ratings for mild steel over the full blade length; count on about 60 % of the thickness in stainless steel. "
               "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel; 208, 240 and 480 V on request.",
    faq=[{"q": "Which line of shear should I buy?",
          "a": "By the material and the hours. For sheet to 1/4″ in a sheet-metal, HVAC or signage shop, the NovoTech sheet metal shears are the lowest-priced powered machines — pneumatic, hydraulic or electric, 39″ to 120″ — and the premium SRGM mechanical shears are the step up for a shop that shears all day: direct-gear drive, 31 – 35 strokes a minute, NC back gauge and photocell guard as standard. For plate from 5/32″ to 1-9/16″ the hydraulic shears take over: NovoTech's value-line QC12K swing beam and Q11K guillotine in the widest range of sizes, or the Dener BS and DAS — the premium plate shears, Turkish-built with the ESA CNC and Dener Canada parts in Mississauga. All four lines are installed and supported by the same NovoTech technicians; we quote across lines so you can compare."},
         {"q": "Mechanical or hydraulic shear — which is better?",
          "a": "For sheet to 1/4″ a mechanical shear is the faster and simpler machine: 30 – 55 strokes a minute from a motor and gearbox or flywheel, no hydraulic power pack, no oil to heat up, no valves or seals to service, and the same cut quality on the first and the thousandth stroke. Hydraulic shears earn their price from 3/8″ plate upwards, where the beam needs tonnage rather than speed — and in the light sizes a small hydraulic shear is the quietest, lowest-priced way to cut 14 ga to 5/32″ a few times an hour."},
         {"q": "Swing beam or guillotine?",
          "a": "On a swing beam shear the beam pivots on two bearings and the cylinders swing it through the cut — few parts, a low price and a rake angle fixed by the design, which is fine for plate. A guillotine shear carries the beam straight down on rollers with a variable rake angle, so the same machine cuts thin sheet flat and fast at a small angle and thick plate at a steeper one; it also keeps the blade gap set automatically. For a plate shop cutting mostly 3/8″ and up, a swing beam shear (Dener BS, NovoTech QC12K); for a job shop that cuts everything from 16 ga to 3/4″ and beyond, a guillotine (Dener DAS, NovoTech Q11K)."},
         {"q": "How is the capacity rated, and what about stainless and aluminum?",
          "a": "Capacities are the makers' ratings for mild steel (about 65,000 psi) over the full blade length. Stainless steel is harder to shear, so count on about 60 % of the mild-steel thickness — 14 ga stainless on a 1/8″ machine, 11 ga on a 1/4″ machine, 3/8″ on a 5/8″ machine; aluminum cuts to the full rated thickness and about 50 % more. Tell us your thickest material and we size the shear with a margin."},
         {"q": "Which length do I need?",
          "a": "The model number is the maximum shearing length in millimetres: 1250 – 1360 = 49 – 53.5″ (a 4 × 8 sheet cut across), 1500 – 1560 = 5 ft, 2000 – 2060 = 6.6 – 6.8 ft, 2500 – 2560 = 8.2 – 8.4 ft (a 4 × 8 sheet lengthwise), 3000 – 3200 = 10 – 10.5 ft (5 × 10 sheet), 4000 = 13 ft, 6000 = 20 ft plate. Most sheet-metal shops run an 8 or 10 ft machine so a full sheet is cut both ways; HVAC and signage shops are well served by 52 – 81″; plate shops buy 10 to 20 ft."},
         {"q": "What is the back gauge, and is it NC?",
          "a": "The back gauge is the stop behind the blade that sets the width of the cut strip. The value-line sheet metal shears have a manual gauge with counter, an electric gauge or a PLC-positioned gauge depending on the model; the SRGM and the hydraulic plate shears come with an NC back gauge — the operator keys in the dimension and the gauge moves there — and the Dener DAS with a 1 m ball-screw gauge set by the CNC together with the blade gap and the cutting angle."},
         {"q": "What about safety and the Ontario pre-start review?",
          "a": "Finger guards along the blade, rear guard fences or photocells / light curtains, an anti-repeat single-stroke control and a mobile foot pedal with emergency stop are standard or available on every line; we recommend the photocell or light-curtain rear guard on every powered shear. In Ontario a new shear needs a pre-start health and safety review (PSR) under Regulation 851 before it runs; NovoTech prepares the documentation for it."},
         {"q": "Do you deliver, install and service in Canada?",
          "a": "Yes — every shear is shipped to Mississauga, unloaded, levelled, commissioned and the operators trained by NovoTech; blades and parts for all four lines are stocked here. Every machine comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request) and a 1-year warranty."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about metal shears",
    related_pages=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "corner-notcher.html", "label": "Corner notchers"}, {"href": "circle-cutters-and-seamers.html", "label": "Circle shears & flanging machines"},
                   {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "plate-rollers.html", "label": "Plate rollers"}],
    related_title="More sheet-metal cutting and forming machinery from NovoTech",
)


def build():
    fams = []
    for set_name, slug, ids in SOURCES:
        fs = json.load(open(os.path.join(ROOT, "content", "families", f"{set_name}.json"), encoding="utf-8"))["families"]
        for fid in ids:
            f = dict(fs[fid])
            f["page"] = slug
            fams.append(f)
    write_families(SET, fams)
    pdfs, seen = [], set()
    for f in fams:
        p = f.get("pdf")
        if p and p["file"] not in seen:
            seen.add(p["file"]); pdfs.append(p)
    write_hub(SN.HUB, {**HUB_PAGE, "artifact_title": "Metal Shears", "nav_label": "All shears", "related_blurb": SN.hub()["blurb"]},
              fams, SET, SN.SECTION, SN.subpages(),
              extra={"catalogue_pdf": None, "catalogue_pdfs": pdfs, "range_pick": ["capacity", "length", "strokes", "motor", "weight"],
                     "hero_brand_line": "Dener Makina builds the premium hydraulic shears in Kayseri, Turkey; the premium-line mechanical shears are built in Turkey and the value-line shears in China, all to NovoTech's specification. Every line sold, installed and supported in Canada by NovoTech.",
                     "origin_feature": {"title": "Four lines, one supplier", "text": "Premium Dener and NovoTech mechanical shears from Turkey, NovoTech value-line hydraulic and sheet metal shears from China — every one with a CSA-approved panel, a 1-year warranty and parts and technicians in Mississauga, ON."},
                     "intro_video": None, "intro_video_heading": None, "intro_video_text": None,
                     "related_pages": HUB_PAGE["related_pages"], "related_title": HUB_PAGE["related_title"]})
    path = os.path.join(ROOT, "content", "pages", f"{SN.HUB}.json")
    page = json.load(open(path, encoding="utf-8"))
    for sp, line in zip(page["subpages"], SN.lines()):
        if line:
            sp["line"] = line
        sp["cards_title"] = sp["title"].split(" — ")[0] + " — the line-up"
    json.dump(page, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"shear hub: {len(fams)} families on {len(page['subpages'])} pages · {len(pdfs)} brochures · {sum(len(f['specs']['models']) for f in fams)} models")


if __name__ == "__main__":
    build()
