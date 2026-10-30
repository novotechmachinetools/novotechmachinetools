#!/usr/bin/env python3
"""The shear hub (shear-cutting.html, hub.html template): a short page that sends the buyer to the right kind of shear —
hydraulic shears, mechanical guillotine shears or sheet metal shears (tools/shear_nav.py) — with the three compared, the
whole range in one capacity table and the questions we get asked.

The hub reads the families the four supplier generators wrote (content/families/shears.json, value-sheet.json, ttmc.json)
into its own set content/families/all-shears.json, so run it AFTER tools/saymak_pages.py, tools/dener_pages.py,
tools/vl_sheet_pages.py and tools/ttmc_pages.py, and BEFORE tools/shear_types.py (the three pages):

    python3 tools/shear_hub.py && python3 tools/shear_types.py
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_families, write_hub  # noqa: F401
import shear_nav as SN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "all-shears"

# (family set, page slug, family ids in display order) — from the page map in shear_nav
SOURCES = SN.family_sources()

HUB_PAGE = dict(
    title="Metal Shears for Sale in Canada — Hydraulic, Mechanical & Sheet Metal Shears, 20 ga to 1-9/16″ | NovoTech",
    meta="Every metal shear NovoTech sells in Canada, by kind: hydraulic swing beam and guillotine plate shears to 1-9/16″, direct-gear and flywheel mechanical shears to 3/8″, and sheet metal shears for the HVAC and signage shop — the three kinds compared and every model in one table.",
    h1="Metal shears — hydraulic, mechanical and sheet metal shears, 20 ga to 1-9/16″",
    intro="A metal shear (sheet metal shearing machine, guillotine shear, shear cutter) cuts plate and sheet to size in one stroke between a "
          "fixed bottom blade and a top blade on the moving beam — the first machine in every sheet-metal, HVAC, signage and fabrication shop, "
          "before the press brake. NovoTech sells three kinds in Canada, each on its own page: hydraulic shears — swing beam and variable-rake "
          "guillotine plate shears from 12 ga to 1-9/16″ and 26 ft, in a premium line made in Turkey and a value line built to our "
          "specification; mechanical guillotine shears — direct-gear SRGM machines for 1/8″ and 1/4″ at 31 to 35 strokes a minute and flywheel "
          "shears to 3/8″, with no hydraulics at all; and sheet metal shears — pneumatic, electric and bench shears and a coil slitter for the "
          "sheet-metal shop. Below, the three kinds compared, every model in one table of capacity, length, strokes, motor and weight, and the "
          "questions we get asked; every machine comes with a CSA-approved panel, a 1-year warranty and installation, training and parts from "
          "Mississauga, ON, Canada.",
    points=['<a href="hydraulic-shearing-machine.html">Hydraulic</a>: swing beam 12 ga – 3/4″ × 4 – 20 ft and guillotine 1/4″ – 1-9/16″ × 8 – 26 ft; premium <a href="hydraulic-shearing-machine.html#dn-bs">BS / BSY</a> and <a href="hydraulic-shearing-machine.html#dn-das">DAS CNC</a>, value <a href="hydraulic-shearing-machine.html#vl-qc12k">QC12K</a> / <a href="hydraulic-shearing-machine.html#vl-q11k">Q11K</a>',
            '<a href="mechanical-guillotine-shear.html">Mechanical</a>: <a href="mechanical-guillotine-shear.html#sh-srgm-group">SRGM direct-gear guillotines</a> 1/8″ × 3.6 – 10 ft and 1/4″ × 3.6 – 13.8 ft, 31 – 35 strokes/min; <a href="mechanical-guillotine-shear.html#tt-q11-mech">flywheel shears to 3/8″</a>',
            '<a href="sheet-metal-shears.html">Sheet metal</a>: <a href="sheet-metal-shears.html#tt-ps">pneumatic 16 ga × 52″</a>, <a href="sheet-metal-shears.html#sh-electric-group">electric 14 ga – 5/32″ × 49 – 100″</a>, <a href="sheet-metal-shears.html#tt-bq01">bench shears</a>, <a href="sheet-metal-shears.html#tt-ps1220">48″ coil slitting and cut-to-length machine</a>'],
    hero="sm-srgm", minis=["dn-das-1", "tt-q11a"],
    range_cols=["Capacity (mild steel)", "Shearing length", "Strokes / min", "Motor", "Weight"],
    range_lead="Every shear model NovoTech sells, in one table: mild-steel capacity, shearing length, strokes per minute, motor and weight. Each row links to the full specification table on the hydraulic, mechanical or sheet metal shear page.",
    range_caption="Metal shears supplied by NovoTech — hydraulic, mechanical and sheet metal shears, premium and value lines",
    range_note="Capacities are the manufacturers' ratings for mild steel over the full blade length; count on about 60 % of the thickness in stainless steel. "
               "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel; 208, 240 and 480 V on request.",
    faq=[{"q": "Hydraulic, mechanical or sheet metal shear — which should I buy?",
          "a": "By the material and the hours. For sheet to 14 ga in a sheet-metal, HVAC or signage shop, the sheet metal shears are the lowest-priced powered machines — pneumatic, electric or bench, 26″ to 100″. For 1/8″ and 1/4″ all day, a mechanical guillotine shear is the faster and simpler machine: direct-gear drive, 31 – 35 strokes a minute, no hydraulics, with return-to-sender and cut-to-length versions. From 1/4″ plate up — 3/8″, 1/2″, to 1-9/16″ over 20 and 26 ft — the hydraulic shears are the machines, swing beam for the everyday plate shear and a variable-rake guillotine for production and thick plate; each comes in a premium and a value line on the same page. Every kind is installed and supported by the same NovoTech technicians."},
         {"q": "Premium line or value line?",
          "a": "The premium hydraulic shears (Dener BS / BSY and DAS CNC) and mechanical shears (SRGM) are built in Turkey on the heaviest frames with European hydraulics, motors and controls and parts in Mississauga, ON, Canada — for two shifts a day and the tightest cut. NovoTech's value line — the QC12K / Q11K hydraulic shears with Estun controls and the sheet metal shears — is built in China to our specification at about two-thirds of the price, the right buy for a job shop. Both lines are sections on the hydraulic shear page, so the comparison is side by side."},
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
          "a": "Finger guards along the blade, rear guard fences or photocells / light curtains, an anti-repeat single-stroke control and a mobile foot pedal with emergency stop are standard or available on every line; we recommend the photocell or light-curtain rear guard on every powered shear. In Ontario a new shear needs a pre-start health and safety review (PSR) under Regulation 851 before it runs."},
         {"q": "Do you deliver, install and service in Canada?",
          "a": "Yes — every shear is shipped to Mississauga, ON, Canada, unloaded, levelled, commissioned and the operators trained by NovoTech; blades and parts for all four lines are stocked here. Every machine comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request) and a 1-year warranty."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about metal shears",
    related_pages=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "corner-notcher.html", "label": "Corner notchers"}, {"href": "circle-cutters-and-seamers.html", "label": "Circle shears & flanging machines"},
                   {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "plate-rollers.html", "label": "Plate rollers"}],
    related_title="More sheet-metal cutting and forming machinery from NovoTech",
)

# the three kinds side by side, above the range table (hub.html renders page.compare)
COMPARE = {
    "title": "Which kind of shear?",
    "lead": "The three kinds NovoTech sells, side by side. Thickness, length and hours a day decide; the pages list every model of each kind, premium and value lines together.",
    "cols": ["", "Hydraulic shears", "Mechanical guillotine shears", "Sheet metal shears"],
    "rows": [
        ["Cuts", "Plate and sheet, 12 ga to 1-9/16″", "Sheet and light plate, 20 ga to 3/8″", "Sheet, 20 to 14 ga"],
        ["Length", "4 – 26 ft", "3.6 – 13.8 ft", "26 – 100″ (48″ coil slitter)"],
        ["Drive", "Hydraulic cylinders; swing beam or variable-rake guillotine", "Motor and gearbox (direct gear) or flywheel and clutch", "Pneumatic cylinder, electric motor or hand lever"],
        ["Speed", "8 – 22 strokes/min", "31 – 55 strokes/min", "to 25 strokes/min"],
        ["Strengths", "Tonnage for plate, variable rake, CNC gauges", "No hydraulics, fastest cycle, return-to-sender, coil lines", "Lowest price, shop air or single phase, small footprint"],
        ["Typical buyer", "Steel fabricators, plate shops, production", "Sheet-metal production, HVAC plants, coil processors", "HVAC, signage, roofing, repair and small shops"],
        ["Page", {"href": "hydraulic-shearing-machine.html", "label": "Hydraulic shears"}, {"href": "mechanical-guillotine-shear.html", "label": "Mechanical shears"}, {"href": "sheet-metal-shears.html", "label": "Sheet metal shears"}],
    ],
}


def build():
    fams = []
    for set_name, slug, ids in SOURCES:
        fs = json.load(open(os.path.join(ROOT, "content", "families", f"{set_name}.json"), encoding="utf-8"))["families"]
        for fid in ids:
            f = dict(fs[fid])
            f["page"] = slug
            f["group"] = SN.group_of(fid)      # the section of the type page it sits in
            fams.append(f)
    write_families(SET, fams)
    pdfs, seen = [], set()
    for f in fams:
        p = f.get("pdf")
        if p and p["file"] not in seen:
            seen.add(p["file"]); pdfs.append(p)
    write_hub(SN.HUB, {**HUB_PAGE, "artifact_title": "Metal Shears", "nav_label": "All shears", "related_blurb": SN.hub()["blurb"]},
              fams, SET, SN.SECTION, SN.subpages(),
              extra={"catalogue_pdf": None, "catalogue_pdfs": pdfs, "range_pick": [["capacity", "capacity_mild_steel"], ["length", "working_width"], "strokes", ["motor", "operation"], "weight"],
                     "hero_brand_line": "Dener Makina builds the premium hydraulic shears in Kayseri, Turkey; the premium-line mechanical shears are built in Turkey and the value-line shears in China, all to NovoTech's specification. Every line sold, installed and supported in Canada by NovoTech.",
                     "origin_feature": {"title": "Three kinds, two lines, one supplier", "text": "Hydraulic, mechanical or sheet metal shears in two lines: the premium line, built in Turkey, and the NovoTech value line, manufactured in China to high North American quality standards."},
                     "intro_video": None, "intro_video_heading": None, "intro_video_text": None,
                     "related_pages": HUB_PAGE["related_pages"], "related_title": HUB_PAGE["related_title"],
                     "hub_compact": True, "compare": COMPARE, "subpage_link": "all models, specifications and photos"})
    path = os.path.join(ROOT, "content", "pages", f"{SN.HUB}.json")
    page = json.load(open(path, encoding="utf-8"))
    for sp, line in zip(page["subpages"], SN.lines()):
        if line:
            sp["line"] = line
        sp["cards_title"] = sp["title"].split(" — ")[0] + " — every family"
    json.dump(page, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"shear hub: {len(fams)} families on {len(page['subpages'])} pages · {len(pdfs)} brochures · {sum(len(f['specs']['models']) for f in fams)} models")


if __name__ == "__main__":
    build()
