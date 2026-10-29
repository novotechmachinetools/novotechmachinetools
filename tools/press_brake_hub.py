#!/usr/bin/env python3
"""The press-brake hub (press-brake.html, hub.html template): a short page that sends the buyer to the right kind of
machine — hydraulic, electric or compact press brakes (tools/press_brake_nav.py) — with a comparison of the three, every family
by brand (the line-up, built by build.py), the whole range in one capacity table and the questions we get asked.

The hub reads the families the two supplier generators wrote (content/families/dener.json, value-sheet.json) into its own
set content/families/press-brakes.json, so run it AFTER tools/dener_pages.py and tools/vl_sheet_pages.py, and BEFORE
tools/press_brake_types.py (the three type pages):

    python3 tools/press_brake_hub.py && python3 tools/press_brake_types.py
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_families, write_hub  # noqa: F401
import press_brake_nav as PBN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "press-brakes"

# (family set, page slug, family ids in display order) — from the page map in press_brake_nav
SOURCES = PBN.family_sources()

HUB_PAGE = dict(
    title="Press Brakes for Sale in Canada — Hydraulic, Electric & Compact, 16–1,323 Tons | NovoTech",
    meta="Every press brake NovoTech sells in Canada, by kind: hydraulic CNC, hybrid and NC press brakes to 1,323 US tons, servo-electric and ball-screw press brakes to 220 tons and compact press brakes from 16 tons — every family by brand and the capacity table for the whole range.",
    h1="Press brakes — hydraulic, electric and compact, 16 to 1,323 US tons",
    intro="A press brake bends sheet and plate between a punch and a V-die; the control sets the back gauge, the ram depth and the angle, and the "
          "operator loads the sheet and presses the pedal. NovoTech sells three kinds in Canada, each on its own page: hydraulic press brakes — "
          "the lowest price per ton and full force over the whole stroke, from 33-ton NC machines to CNC brakes of 1,323 US tons and 26 ft, in a "
          "premium line made in Turkey and a value line built to our specification; electric press brakes, servo-driven with no hydraulic oil, "
          "3 to 220 US tons, twice the speed and about 70 % less power for sheet work; and compact press brakes from 16 to 66 tons over 2 to 8 ft "
          "for the sheet-metal shop. Below, the three kinds compared, every family by brand, every model in one table and the questions we get "
          "asked; every machine comes with a CSA-approved panel, a 1-year warranty and installation, training and parts "
          "from Mississauga, ON, Canada.",
    points=['<a href="hydraulic-press-brake.html">Hydraulic</a>: <a href="hydraulic-press-brake.html#pb-premium-group">CNC 55 – 1,323 US tons × 4 – 26 ft</a>, <a href="hydraulic-press-brake.html#pb-hybrid-group">XH hybrid with servo pump</a>, <a href="hydraulic-press-brake.html#pb-nc-group">NC torsion-bar from 33 tons</a>',
            '<a href="electric-press-brake.html">Electric</a>: <a href="electric-press-brake.html#dn-ddm">servo-electric 44 – 220 tons × 5 – 13 ft</a> and <a href="electric-press-brake.html#pb-value-electric-group">ball-screw 3 – 176 tons</a> — ±0.01 mm, no oil, power only while the ram moves',
            '<a href="compact-hydraulic-press-brakes.html">Compact</a>: <a href="compact-hydraulic-press-brakes.html#dn-xl-1560">Dener XL 1560, 66 tons × 5 ft</a>, <a href="compact-hydraulic-press-brakes.html#pb-compact-cnc-group">value-line WAD-50T CNC and WC67K-30T NC compacts</a>, <a href="compact-hydraulic-press-brakes.html#tt-hbv-group">HBV bending brakes 16 – 35 tons</a>'],
    hero="dn-xl-1", minis=["dn-ddm-2", "vl-wad-1"],
    range_cols=["Bending force", "Bending length", "Stroke", "Daylight", "Weight"],
    range_lead="Every press brake model NovoTech sells, in one table: bending force and length, ram stroke, daylight and weight. Each row links to the full specification table on the hydraulic, electric or compact page.",
    range_caption="Press brakes supplied by NovoTech — hydraulic and electric, premium and value lines",
    range_note="Bending force in US tons (metric tonnes); XH hybrid packages are fitted to the XL frames, so stroke and daylight are those of the XL of the same tonnage. "
               "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel; 208, 240 and 480 V on request.",
    faq=[{"q": "Hydraulic, hybrid or electric — which press brake should I buy?",
          "a": "Hydraulic gives the lowest price per ton and full force over the whole stroke — the machine for thick plate, long parts and the widest tonnage range (33 to 1,323 US tons here). A hybrid (the Dener XH) is a hydraulic brake with a servo-driven pump: 42 – 58 % less energy, faster, quieter, for a shop that runs the brake all day. An electric brake (Dener DDM, NovoTech WADG) has no oil at all: ±0.01 mm repeatability, bending speeds to 30 mm/s and about 70 % less power — usually the better buy for 16 ga to 1/4″ sheet in a job shop or a clean environment. Above about 150 tons and on 3/8″ plate, hydraulic still wins. For 4 – 5 ft work in sheet to 3/16″, the compact brakes on their own page are the right size."},
         {"q": "Premium line or value line?",
          "a": "Both kinds come in two lines, on the same page. The premium line is made in Turkey by Dener on the heaviest frame, with ESA or Delem controls, the longest options list and Dener Canada parts in Mississauga, ON, Canada — the machine for plate and production, two shifts a day. NovoTech's own value line is the same architecture — monoblock frame, Hawe servo valves, linear scales, Delem control — built in China to our specification at about two-thirds of the price: the right buy for a job shop that needs a 100 – 300 ton CNC brake, an electric brake for sheet or an NC brake for repeat parts. The compact page has the smallest of both lines — the Dener XL 1560 and the value-line WAD-50T and WC67K-30T — for HVAC, enclosures and brackets where a 100-ton machine is more than you need. All are installed and supported by the same NovoTech technicians."},
         {"q": "How much tonnage and length do I need?",
          "a": "Air bending takes F = S² × 2 × R ÷ (1.4 × V) tonnes per metre of bend — the sheet thickness S and the V opening V in millimetres, the tensile strength R = 47 kg/mm² for mild steel (70 for stainless, 25 for aluminum), the formula behind the EUROSTAMP and Dener bending charts; in inches and US tons per foot it reads 575 × t² ÷ V. With the standard V of about 8 × the thickness, 3 mm needs about 24 t/m (8 US tons per foot), 6 mm 48 t/m (16), 1/4″ 54 t/m (18), 3/8″ in a 3″ V 80 t/m (27) and 1/2″ in a 5″ V 85 t/m (29). Multiply by the bend length and add about 20 % in reserve: 3 m × 6 mm is a 175-ton press brake, 10 ft × 1/4″ a 200 – 220 US ton machine, 10 ft × 3/8″ a 300 – 320 ton machine and 13 ft × 1/2″ a 400 – 450 ton machine. The tonnage calculator in the buying guide on the press brake page does the arithmetic for your thickness and length; tell us your thickest and longest bend and we size the brake and the tooling."},
         {"q": "CNC or NC?",
          "a": "An NC brake positions the back gauge and the ram depth from a stored program, with the two cylinders kept in step by a torsion bar — rigid, cheap to maintain, right for the same parts in one material every day. A CNC brake measures the ram on linear scales and corrects it through servo valves, calculates the bend from the drawing, crowns the bed and changes material in the program — the machine for mixed work, tight angles and multi-bend parts. NovoTech's value line has both; the Dener CNC brakes come with 2D or 3D graphic controls. The buying guide below explains and compares every control."},
         {"q": "What tooling fits, and do you stock it?",
          "a": "European-style (Promecam / Amada) segmented tooling fits every line: the premium Dener brakes carry European-style top-tool holders, the value-line brakes their own clamping, and a sectioned punch set with a 2-V or 4-V die ships with every machine (a 4-V die with the Dener brakes, a 2-V die with the value line) — tell us which tooling standard your shop already has and we fit the holders to match. NovoTech stocks Eurostamp press brake tooling in Canada — punches, dies, radius, hemming and joggle tools, gooseneck and special profiles — and sizes it to your machine; quick-release, pneumatic and Wila hydraulic clamping and American-style adapters are options, not standard equipment."},
         {"q": "What about safety and the Ontario pre-start review?",
          "a": "Side guards, an enclosed rear guard, interlocked doors and an anti-panic foot pedal with emergency stop are standard; DSP or Fiessler laser finger protection and light curtains are options we recommend for every CNC machine. In Ontario a new press brake needs a pre-start health and safety review (PSR) under Regulation 851 before it runs."},
         {"q": "Do you deliver, install and service in Canada?",
          "a": "Yes — NovoTech sells, installs and supports press brakes across Canada and the United States. Installation, commissioning and operator training are free of charge in the Greater Toronto Area; outside the GTA our technicians do the same work at an additional charge. Dener Canada and NovoTech stock the parts in Canada. Every machine comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request), a 1-year warranty and remote diagnostics through the control."},
         {"q": "What does delivery cost, and who unloads the machine?", "a": "A press brake ordered from the factory (back-ordered) travels in its container straight from the port, customs and the rail yard to your plant door: in the Greater Toronto Area that delivery is free; outside the GTA the freight is quoted and charged. A machine from NovoTech's stock is loaded, shipped and unloaded at the buyer's cost. In every case unloading is the buyer's responsibility and expense — the crane or forklift, the rigging and moving the machine onto its foundation — so book a rigger for the delivery day; we are glad to recommend riggers who know press brakes and to tell you the weight and lifting points."},
         {"q": "Is the hydraulic oil included?", "a": "No — the hydraulic oil is bought by the customer. Before commissioning, fill the tank with ISO VG 46 anti-wear hydraulic oil (AW 46) in the quantity shown in the specification table for your model; our technician checks the level and bleeds the system during installation. Electric press brakes have no hydraulic oil at all."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about press brakes",
    related_pages=[{"href": "horizontal-press-brake.html", "label": "Horizontal press brakes — bar, pipe and busbar"}, {"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}, {"href": "panel-bender.html", "label": "CNC panel benders"},
                   {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "v-grooving-machine.html", "label": "V-grooving machines"}],
    related_title="Machinery that works alongside a press brake",
)

# the three kinds side by side, above the range table (hub.html renders page.compare)
COMPARE = {
    "title": "Which kind of press brake?",
    "lead": "The three kinds NovoTech sells, side by side. Tonnage, length and the material you bend decide; the pages explain each line and every model.",
    "cols": ["", "Hydraulic press brakes", "Electric press brakes", "Compact press brakes"],
    "rows": [
        ["Bends", "Sheet and plate, 16 ga to 1/2″ and beyond", "Sheet, 20 ga to 1/4″ (3/8″ on the largest)", "Sheet to 8 ga; plate to 3/16″ in short parts"],
        ["Force and length", "33 – 1,323 US tons × 4 – 26 ft", "3 – 220 US tons × 1.6 – 13 ft", "16 – 66 US tons × 2 – 8 ft"],
        ["Drive", "Hydraulic cylinders; XH hybrid adds a servo pump", "Servo motors and ball screws, no hydraulic oil", "Hydraulic cylinders, torsion bar; NC or 3-axis CNC"],
        ["Strengths", "Lowest price per ton, full force all stroke, widest range", "±0.01 mm, about twice the speed, ~70 % less power, clean and quiet", "Small footprint, low price, full press-brake tooling and controls"],
        ["Typical buyer", "Steel fabricators, plate work, production shops", "Job shops, sheet metal, enclosures, clean rooms", "HVAC, enclosures, brackets, signage, maintenance shops"],
        ["Page", {"href": "hydraulic-press-brake.html", "label": "Hydraulic press brakes"}, {"href": "electric-press-brake.html", "label": "Electric press brakes"}, {"href": "compact-hydraulic-press-brakes.html", "label": "Compact press brakes"}],
    ],
}



def build():
    fams = []
    for set_name, slug, ids in SOURCES:
        fs = json.load(open(os.path.join(ROOT, "content", "families", f"{set_name}.json"), encoding="utf-8"))["families"]
        for fid in ids:
            f = dict(fs[fid])
            f["page"] = slug
            f["group"] = PBN.group_of(fid)      # the section of the type page it sits in
            fams.append(f)
    write_families(SET, fams)
    pdfs = []
    seen = set()
    for f in fams:
        p = f.get("pdf")
        if p and p["file"] not in seen:
            seen.add(p["file"]); pdfs.append(p)
    subpages = [(s, title, image, blurb, nav) for s, title, image, blurb, nav, _ in PBN.SUBPAGES]
    write_hub(PBN.HUB, {**HUB_PAGE, "artifact_title": "Press Brakes", "nav_label": "All press brakes", "related_blurb": PBN.hub()["blurb"]},
              fams, SET, PBN.SECTION, subpages,
              extra={"catalogue_pdf": None, "catalogue_pdfs": pdfs, "range_pick": ["bending_force", "bending_length", "stroke", "daylight", "weight"],
                     "hero_brand_line": "The premium line is built by Dener Makina in Kayseri, Turkey; the NovoTech value line is built in China to our specification. All sold, installed and supported in Canada by NovoTech.",
                     "origin_feature": {"title": "Three kinds, two lines, one supplier", "text": "Hydraulic, electric or compact, premium or value — every press brake comes with a CSA-approved panel, a 1-year warranty and parts and technicians in Mississauga, ON, Canada."},
                     "intro_video": None, "intro_video_heading": None, "intro_video_text": None,
                     "related_pages": HUB_PAGE["related_pages"], "related_title": HUB_PAGE["related_title"],
                     "why_title": "Included with every press brake from NovoTech", "why_features": PBN.why_features(),
                     "hub_compact": True, "compare": COMPARE, "subpage_link": "all models, specifications and photos"})
    # the hub's subpages carry the line class for the cards (premium / value)
    path = os.path.join(ROOT, "content", "pages", f"{PBN.HUB}.json")
    page = json.load(open(path, encoding="utf-8"))
    for sp, (_, _, _, _, _, line) in zip(page["subpages"], PBN.SUBPAGES):
        if line:
            sp["line"] = line
        sp["cards_title"] = sp["title"].split(" — ")[0] + " — every family"
    json.dump(page, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"press-brake hub: {len(fams)} families on {len(subpages)} pages · {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
