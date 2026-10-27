#!/usr/bin/env python3
"""The press-brake hub (press-brake.html, hub.html template): three product pages — Dener CNC press brakes (premium line),
NovoTech CNC press brakes (value line, hydraulic + electric + NC) and the ISITAN compact hydraulic press brakes — introduced
separately with their family cards, plus the whole range in one capacity table, like the rebar hub.

The hub reads the families the three generators wrote (content/families/dener.json, value-sheet.json, edgebender.json) into
its own set content/families/press-brakes.json, so run it AFTER tools/dener_pages.py, tools/vl_sheet_pages.py and
tools/isitan_pressbrake.py:

    python3 tools/press_brake_hub.py
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_families, write_hub  # noqa: F401
import press_brake_nav as PBN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "press-brakes"

# (family set, page slug, family ids in display order)
SOURCES = [("dener", "dener-cnc-press-brakes", ["dn-xl-small", "dn-xl-large", "dn-xh", "dn-ddm", "dn-dds"]),
           ("value-sheet", "novotech-cnc-press-brakes", ["vl-wad-small", "vl-wad-large", "vl-wad-heavy", "vl-wadg", "vl-wadg-mini", "vl-nc-small", "vl-nc-large"]),
           ("edgebender", "compact-hydraulic-press-brakes", ["isitan-edgebender-cnc", "isitan-edgebender-nc"])]

HUB_PAGE = dict(
    title="Press Brakes for Sale in Canada, 22–1,323 Tons | NovoTech",
    meta="Every press brake NovoTech sells in Canada: Dener CNC hydraulic, hybrid and servo-electric brakes, NovoTech's value-line hydraulic and electric brakes, and ISITAN compact brakes — 22 to 1,323 US tons.",
    h1="Press brakes — CNC hydraulic, hybrid and electric, 22 to 1,323 US tons",
    intro="A press brake bends sheet and plate between a punch and a V-die; the control sets the back gauge, the ram depth and the angle, and the "
          "operator loads the sheet and presses the pedal. NovoTech sells three lines of press brakes in Canada, each on its own page: the "
          "Dener CNC press brakes — the premium line, made in Turkey, hydraulic XL to 661 US tons and 20 ft, the XH hybrid and the DDM "
          "servo-electric; NovoTech's own value-line CNC press brakes — hydraulic 55 to 331 tons and heavy-duty to 1,323 tons, electric servo "
          "brakes 3 to 176 tons and NC torsion-bar brakes from 33 tons, built in China to our specification; and the ISITAN compact hydraulic "
          "press brakes, 33 to 66 tons over 4 to 7 ft for the sheet-metal shop. Below, each line in brief and the whole range in one table; "
          "every machine comes with a CSA-approved panel, European-style tooling, a 1-year warranty and installation, training and parts "
          "from Mississauga, ON, Canada.",
    points=["Dener premium line: XL hydraulic 66 – 661 tons × 5 – 20 ft, XH hybrid, DDM servo-electric 44 – 220 tons, DDS from 22 tons",
            "NovoTech value line: hydraulic CNC 55 – 1,323 tons, electric 3 – 176 tons, NC 33 – 441 tons — Delem, Hawe, Estun",
            "ISITAN compact: 33 – 66 tons × 4.2 – 6.9 ft, NC or CNC with Cybelec — plus Eurostamp tooling stocked in Canada"],
    hero="dn-xl-1", minis=["vl-wad-1", "is-eb-1240-cnc"],
    range_cols=["Bending force", "Bending length", "Stroke", "Daylight", "Weight"],
    range_lead="Every press brake model NovoTech sells, in one table: bending force and length, ram stroke, daylight and weight. Each row links to the full specification table on the line's page.",
    range_caption="Press brakes supplied by NovoTech — Dener, NovoTech value line and ISITAN",
    range_note="Bending force in US tons (metric tonnes); XH hybrid packages are fitted to the XL frames, so stroke and daylight are those of the XL of the same tonnage. "
               "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel; 208, 240 and 480 V on request.",
    faq=[{"q": "Dener, NovoTech value line or ISITAN — which press brake should I buy?",
          "a": "By the work. For plate and production — 3/8″ and 1/2″ over 10 to 20 ft, two shifts, a long options list — the Dener XL and XH are the machines; they are built in Turkey on the heaviest frame, with ESA or Delem controls and Dener Canada parts in Mississauga, ON, Canada. The NovoTech value line is the same architecture — monoblock frame, Hawe servo valves, linear scales, Delem control — built in China to our specification at about two-thirds of the price: the right buy for a job shop that needs a 100 – 300 ton CNC brake, an electric brake for sheet, or an NC brake for repeat parts. The ISITAN Edgebenders are the compact 33 – 66 ton machines for HVAC, enclosures and brackets where a 100-ton brake is more than you need. All three are installed and supported by the same NovoTech technicians."},
         {"q": "Hydraulic, hybrid or electric?",
          "a": "Hydraulic gives the lowest price per ton and full force over the whole stroke — the machine for thick plate. A hybrid (Dener XH) is a hydraulic brake with a servo-driven pump: 42 – 58 % less energy, faster, quieter, for a shop that runs the brake all day. An electric brake (Dener DDM, NovoTech WADG) has no oil at all: ±0.01 mm repeatability, bending speeds to 30 mm/s and about 70 % less power — usually the better buy for 16 ga to 1/4″ sheet. Above about 150 tons and on 3/8″ plate, hydraulic still wins."},
         {"q": "How much tonnage and length do I need?",
          "a": "Air bending mild steel with the standard V = 8 × thickness die takes roughly 8 US tons per foot for 16 ga, 15 for 1/8″, 30 for 3/16″, 55 for 1/4″ and 130 tons per foot for 1/2″; stainless needs about 50 % more, aluminum about half. Add a foot of length to the longest part you bend. A 10 ft × 1/4″ shop is a 110 – 175 ton machine; 10 ft × 3/8″ a 220 – 250 ton machine; 13 ft × 1/2″ a 400 ton machine. Tell us your thickest and longest bend and we size the brake and the tooling."},
         {"q": "CNC or NC?",
          "a": "An NC brake positions the back gauge and the ram depth from a stored program, with the two cylinders kept in step by a torsion bar — rigid, cheap to maintain, right for the same parts in one material every day. A CNC brake measures the ram on linear scales and corrects it through servo valves, calculates the bend from the drawing, crowns the bed and changes material in the program — the machine for mixed work, tight angles and multi-bend parts. NovoTech's value line has both; Dener and ISITAN CNC brakes come with 2D or 3D graphic controls."},
         {"q": "What tooling fits, and do you stock it?",
          "a": "European-style (Promecam / Amada) segmented punches and dies with quick-release clamping are standard on every line, and a sectioned punch set with a 2-V die ships with each machine. NovoTech stocks Eurostamp press brake tooling in Canada — punches, dies, radius, hemming and joggle tools, gooseneck and special profiles — and sizes it to your machine; Wila hydraulic clamping and American-style adapters are options."},
         {"q": "What about safety and the Ontario pre-start review?",
          "a": "Side guards, an enclosed rear guard, interlocked doors and an anti-panic foot pedal with emergency stop are standard; DSP or Fiessler laser finger protection and light curtains are options we recommend for every CNC machine. In Ontario a new press brake needs a pre-start health and safety review (PSR) under Regulation 851 before it runs; NovoTech prepares the documentation for it."},
         {"q": "Do you deliver, install and service in Canada?",
          "a": "Yes — every press brake is shipped to Mississauga, ON, Canada, unloaded, levelled, commissioned and the operators trained by NovoTech; Dener Canada and NovoTech stock the parts here. Every machine comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request), a 1-year warranty and remote diagnostics through the control."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about press brakes",
    related_pages=[{"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}, {"href": "panel-bender.html", "label": "CNC panel benders"},
                   {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "horizontal-press-brake.html", "label": "Horizontal press brakes"}, {"href": "v-grooving-machine.html", "label": "V-grooving machines"}],
    related_title="Machinery that works alongside a press brake",
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
                     "hero_brand_line": "Dener Makina builds the premium line in Kayseri, Turkey; the NovoTech value line is built in China to our specification; ISITAN builds the compact brakes in Bursa, Turkey. All sold, installed and supported in Canada by NovoTech.",
                     "origin_feature": {"title": "Three lines, one supplier", "text": "Premium Dener, NovoTech's own value line and the ISITAN compact brakes — every one with a CSA-approved panel, European tooling, a 1-year warranty and parts and technicians in Mississauga, ON, Canada."},
                     "intro_video": None, "intro_video_heading": None, "intro_video_text": None,
                     "related_pages": HUB_PAGE["related_pages"], "related_title": HUB_PAGE["related_title"]})
    # the hub's subpages carry the line class for the cards (premium / value)
    path = os.path.join(ROOT, "content", "pages", f"{PBN.HUB}.json")
    page = json.load(open(path, encoding="utf-8"))
    for sp, (_, _, _, _, _, line) in zip(page["subpages"], PBN.SUBPAGES):
        if line:
            sp["line"] = line
        sp["cards_title"] = sp["title"].split(" — ")[0] + " — the line-up"
    json.dump(page, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"press-brake hub: {len(fams)} families on {len(subpages)} pages · {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
