#!/usr/bin/env python3
"""The CNC machine-tool hub (cnc-machine-tools.html, hub.html template): four product pages — Dener CNC lathes, Dener machining
centres and the Dener surface grinder (premium line, made in Turkey) and NovoTech's value-line CNC machine tools (built in China)
— introduced separately with their family cards, plus the whole range in one table.

The hub reads the families the generators wrote (content/families/dener-mt.json, ttmc-more.json) into its own set
content/families/machine-tools.json, so run it AFTER tools/dener_mt_pages.py and tools/ttmc_more_pages.py:

    python3 tools/machine_tools_hub.py
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_families, write_hub
import machine_tools_nav as MTN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "machine-tools"

# (family set, page slug, family ids in display order)
SOURCES = [("dener-mt", "dener-cnc-lathes", ["dn-ttc", "dn-tth"]),
           ("dener-mt", "dener-machining-centres", ["dn-tmc", "dn-tdc"]),
           ("dener-mt", "dener-surface-grinders", ["dn-tgh"]),
           ("ttmc-more", "novotech-cnc-machine-tools", ["tt-cnc-lathe", "tt-vmc", "tt-boring", "tt-cnc-slot"])]

HUB_PAGE = dict(
    title="CNC Lathes, Machining Centres & Surface Grinders | NovoTech",
    meta="CNC machine tools sold in Canada: Dener CNC lathes, TMC vertical and TDC double-column machining centres and the TGH surface "
         "grinder, and NovoTech's value-line CNC lathe, VMCs and boring mills.",
    h1="CNC machine tools — CNC lathes, vertical and double-column machining centres and surface grinders",
    intro="CNC machine tools turn, mill, drill, bore, tap and grind the parts a fabrication shop or a machine shop makes from bar, plate and "
          "castings. NovoTech sells two lines in Canada, each on its own pages: the Dener machine tools — the premium line, built in Kayseri, "
          "Turkey — with the TTC and TTH slant-bed CNC lathes from 6″ to 12″ chucks, the TMC vertical machining centres from 33.5 to 63″ of "
          "X travel, the TDC double-column machining centres to 161.4″ and 26,455 lb on the table, and the TGH-B 450 NC surface grinder; and "
          "NovoTech's own value-line CNC machine tools, built in China to our specification — a slant-bed CNC lathe with gang tooling, "
          "BT40 vertical machining centres, BT50 CNC boring and milling machines, a horizontal machining centre and slot machining centres. "
          "Below, each line in brief and every model in one table; every machine comes with a CSA-approved panel, a 1-year warranty and "
          "installation, training and parts from Mississauga, ON, Canada.",
    points=["Dener CNC lathes: TTC-6 / TTC-8 and TTH-8 / 10 / 12, Ø22 – 27.6″ swing, 6″ – 12″ chucks, Fanuc control, C-axis live tooling",
            "Dener machining centres: TMC 850 – 1600 (BBT40, X 33.5 – 63″) and TDC 2112 – 4120 double-column (BBT50, X to 161.4″); TGH-B 450 surface grinder",
            "NovoTech value line: CTK6416 CNC lathe, VMC8046 / VMC10562, TXK BT50 boring mills, TH-800 HMC — Mitsubishi, Fanuc or Siemens"],
    hero="dn-tmc-1", minis=["dn-ttc-1", "tm-vmc10562"],
    range_cols=["Table / swing", "Travels", "Spindle speed", "Spindle motor", "Weight"],
    range_lead="Every CNC machine tool NovoTech sells, in one table: the table or the swing over the bed, the travels, spindle speed and "
               "motor, and weight. Each row links to the full specification table on the line's page.",
    range_caption="CNC machine tools supplied by NovoTech — Dener and NovoTech value line",
    range_note="Travels are X × Y × Z for the machining centres, X / Z for the lathes and grinding length × width for the surface grinder. "
               "Spindle motors are given as continuous / maximum power where the maker rates both. Three-phase machines are supplied for "
               "600 V as standard with a CSA-approved panel; 208, 240 and 480 V on request.",
    faq=[{"q": "Dener or NovoTech value line — which should I buy?",
          "a": "By the work and the hours. The Dener machines are the premium line: built in Kayseri, Turkey, on stress-relieved Meehanite and "
               "slant-bed castings, with Fanuc or Mitsubishi controls, double-nut C3 ballscrews, roller guides and direct-drive spindles — "
               "the machines for two shifts and close tolerances, from a compact lathe to a 40-tonne double-column machining centre. "
               "NovoTech's value-line CNC machine tools are built in China to our specification at a lower price: the right buy for a job "
               "shop's first CNC lathe or VMC, for boring and milling large parts on a budget, or for special work such as slot machining. "
               "Both lines are installed and supported by the same NovoTech technicians, and we quote across lines so you can compare."},
         {"q": "Lathe, vertical machining centre, double-column or boring mill?",
          "a": "Round parts — shafts, pins, flanges, bushings — go on a CNC lathe; with a C-axis and live tools the lathe also drills and "
               "mills them. Prismatic parts — brackets, housings, plates, moulds — go on a vertical machining centre up to the size of its "
               "table. Parts too long, wide or heavy for a VMC go on a double-column machining centre, whose spindle travels on a cross rail "
               "between two columns over a long table. A boring and milling machine (or a horizontal machining centre) machines several faces "
               "of a large part in one setup with a rotary table and a horizontal spindle."},
         {"q": "Which control?",
          "a": "Dener lathes come with the Fanuc 0i-TF Plus, Dener machining centres with the Mitsubishi M80A and Navi-Mill conversational "
               "programming — each with the other make to order; NovoTech's value-line machines are built with Mitsubishi, Fanuc or Siemens. "
               "All run ISO G-code from any CAM system; we recommend the control your programmers already know."},
         {"q": "What do I need on the floor?",
          "a": "Three-phase power (25 to 43 kVA for the Dener lathes and TMC machining centres), shop air at 73 – 87 psi for the machining "
               "centres, and a level reinforced-concrete floor — the double-column and boring machines sit on a foundation built to the "
               "maker's drawing. We send the foundation drawing, the floor-space plan and the power requirements with the quote."},
         {"q": "Do you deliver, install and service in Canada?",
          "a": "Yes — every machine is shipped to Mississauga, ON, Canada, unloaded, levelled and commissioned, its geometry checked, and "
               "your operators and programmers trained by NovoTech; parts for both lines are stocked or ordered through us. Every machine "
               "comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request) and a 1-year warranty."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about CNC machine tools",
    related_pages=[{"href": "milling-machine.html", "label": "Milling machines"}, {"href": "drill-press.html", "label": "Drill presses"},
                   {"href": "band-saw.html", "label": "Band saws"}, {"href": "belt-grinder.html", "label": "Belt grinders and sanders"},
                   {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}],
    related_title="More metalworking machinery from NovoTech",
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
    write_hub(MTN.HUB, {**HUB_PAGE, "artifact_title": "CNC Machine Tools", "nav_label": "All CNC machine tools", "related_blurb": MTN.hub()["blurb"]},
              fams, SET, MTN.SECTION, MTN.subpages(),
              extra={"catalogue_pdf": None, "catalogue_pdfs": pdfs,
                     "range_pick": [["table", "swing_over_bed"], ["travel_x_y_z", "travel_x_z", "grinding_area"], ["spindle_speed", "spindle_speed_max"],
                                    ["spindle_motor", "motor"], "weight"],
                     "hero_brand_line": "Dener Makina builds the premium-line machine tools in Kayseri, Turkey; the value-line machines are built in China to NovoTech's specification. Every line sold, installed and supported in Canada by NovoTech.",
                     "origin_feature": {"title": "Two lines, one supplier", "text": "Premium Dener machine tools from Turkey and NovoTech value-line machines from China — every one with a CSA-approved panel, a 1-year warranty and parts and technicians in Mississauga, ON, Canada."},
                     "intro_video": {"id": "_bkvwzuOYW0", "title": "DENER machining centre and turning centre assembly line", "thumb": "video-_bkvwzuOYW0", "duration": "PT0M25S"},
                     "intro_video_heading": "Inside the factory — where the Dener machine tools are built",
                     "intro_video_text": "The assembly hall in Kayseri, Turkey, where Dener's machining centres and lathes are built up from their own castings.",
                     "related_pages": HUB_PAGE["related_pages"], "related_title": HUB_PAGE["related_title"],
                     "related_title_": MTN.RELATED_TITLE})          # build.py: the section pages' 'More … from NovoTech' (keeps 'CNC')
    path = os.path.join(ROOT, "content", "pages", f"{MTN.HUB}.json")
    page = json.load(open(path, encoding="utf-8"))
    for sp, line in zip(page["subpages"], MTN.lines()):
        if line:
            sp["line"] = line
        sp["cards_title"] = sp["title"].split(" — ")[0] + " — the line-up"
    json.dump(page, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"machine-tool hub: {len(fams)} families on {len(page['subpages'])} pages · {len(pdfs)} brochures · {sum(len(f['specs']['models']) for f in fams)} models")


if __name__ == "__main__":
    build()
