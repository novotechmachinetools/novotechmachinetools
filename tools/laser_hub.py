#!/usr/bin/env python3
"""The sheet-laser hub (hub.html template): laser-cutting-machine.html over the five sheet-laser pages — each line introduced with
its family cards, like the press-brake and rebar hubs.  The tube lasers have no hub: one page, tube-laser-cutting-machine.html,
written by tools/laser_types.py (the owner, Nov 1 2026); only their family set is written here.

The hubs read the families from content/families/dener.json (tools/dener_pages.py writes it, Senfeng and NovoTech value-line
families included) into their own sets content/families/sheet-lasers.json and tube-lasers.json, so run this AFTER
tools/dener_pages.py, tools/senfeng_pages.py and tools/vl_laser_pages.py:

    python3 tools/laser_hub.py
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_families, write_hub  # noqa: F401
import laser_nav as LN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BRAND_LINE = ("Dener Makina builds the premium lasers in Kayseri, Turkey (since 1974); NovoTech's own value line is built in "
              "China to our specification; Senfeng Laser builds its value line in Jinan, China (CE / FDA / ETL certified and CSA approved). All sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Premium and value lines, one supplier", "text": "Premium Dener lasers from Turkey, NovoTech's own value line and the Senfeng value line from China — every machine with a "
          "CSA-approved panel, a chiller, nesting software, a 1-year warranty, and installation, training, parts and remote diagnostics from Mississauga, ON, Canada."}

HUBS = {
    "sheet": dict(
        set="sheet-lasers", families=LN.families("sheet"),
        lineup_swaps=[["sf-np", "sf-hm"]],      # Senfeng line-up: H, HM, compact, then NP (the owner, Nov 1 2026)
        page=dict(
            title="Fiber Laser Cutting Machines for Sale in Canada — Shuttle Table, Sheet & Tube, Plate, 3D & Coil-Fed, 1.5–80 kW | NovoTech",
            meta="Every fiber laser NovoTech sells in Canada, by kind: lasers with shuttle table or pallet changer, sheet-and-tube combination lasers, large-format plate lasers to 10 × 164 ft, 3D laser cells and coil-fed lines — 1.5 to 80 kW, premium and value lines, the kinds compared and every model in one table.",
            h1="Laser cutting machines for sheet and plate, 1.5 to 80 kW",
            intro="A fiber laser cutting machine cuts sheet and plate from a DXF file with a focused beam — mild steel to 1-1/2″ and beyond with the "
                  "high-power sources, stainless and aluminum to 1″ — at speeds no plasma or punch can match, with a clean edge and no tooling. "
                  "NovoTech sells five kinds in Canada, each on its own page: fiber lasers with a shuttle table or pallet changer that load the "
                  "next sheet while the first is cut, the production machine from 4 × 4 ft compact models to 8.5 × 41 ft and 80 kW; sheet-and-tube "
                  "combination lasers with a rotary chuck beside the table; large-format plate lasers — semi-closed single tables, ground-rail and "
                  "gantry machines to 10 × 164 ft with bevel heads; 3D laser cells for formed parts; and coil-fed lines that cut straight from the "
                  "coil. Each kind comes in a premium line made in Turkey or a value line built to our specification, as sections on the same page. "
                  "Below, the kinds compared, the laser power guide and every model in one table of working area, power and speed; every machine "
                  "comes with a CSA-approved panel, chiller, nesting software, a 1-year warranty and installation, training and parts from "
                  "Mississauga, ON, Canada.",
            points=['<a href="fiber-laser-cutting-machine.html">Fiber lasers</a> with shuttle table or pallet changer, 4 × 4 ft compact to 8.5 × 41 ft, 1.5 – 80 kW — premium <a href="fiber-laser-cutting-machine.html#dn-gfl">GFL</a> / <a href="fiber-laser-cutting-machine.html#dn-smart-closed">Smart</a>, value <a href="fiber-laser-cutting-machine.html#vn-ule">ULE</a>, <a href="fiber-laser-cutting-machine.html#sf-h">H series</a>, <a href="fiber-laser-cutting-machine.html#sf-np">NP</a>, <a href="fiber-laser-cutting-machine.html#sf-compact">compact</a>',
                    '<a href="sheet-and-tube-laser.html">Sheet-and-tube lasers</a> to Ø13.8″ tube; <a href="large-format-plate-laser.html">large-format plate lasers</a> — Smart semi-closed to 13 × 82 ft, ground-rail and gantry machines to 10 × 164 ft with ±45° bevel',
                    '<a href="3d-laser-cutting-machine.html">Five-axis 3D lasers</a>; <a href="coil-fed-laser-cutting-line.html">coil-fed lines</a> to 9/16″ plate'],
            hero="dn-gfl-1", minis=["vn-ule-1", "sf-h-1"],
            range_cols=["Working area", "Laser power", "Max. speed", "Acceleration", "Max. sheet load"],
            range_pick=[["working_area", "area"], "power", "speed", "accel", "load"],
            range_lead="Every sheet laser model NovoTech sells, in one table: working area, laser power, axis speed, acceleration and the maximum sheet weight on the table, where the maker publishes them. Each row links to the full specification table on the line's page.",
            range_caption="Sheet and plate fiber lasers supplied by NovoTech — shuttle table, sheet-and-tube, large-format plate, 3D and coil-fed, premium and value lines",
            range_note="Working areas in feet and inches (millimetres); the model number is the nominal table in decimetres (3015 = 3,000 × 1,500 mm, 10 × 5 ft). Laser power as the sources offered on that model. "
                       "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel and transformer; 208, 240 and 480 V on request.",
            faq=[{"q": "Shuttle table, sheet-and-tube, plate, 3D or coil-fed — which laser should I buy?",
                  "a": "By how many sheets a day and what they are. A laser with a shuttle table or pallet changer keeps cutting while you load the next sheet and keeps fumes and the beam inside its cabin — the production machine, and the one most shops buy from 5 × 10 ft up. A large-format plate laser — a semi-closed single table, a ground-rail or a gantry machine — is for heavy plate and very long beds, with the cover travelling on the gantry, bevel heads and oxy-fuel. A sheet-and-tube laser adds a rotary chuck beside the table for a shop that cuts both and has room for one machine. 3D cells cut formed parts; coil-fed lines cut straight from the coil. Each kind has its own page with the premium and value lines side by side."},
                 {"q": "Premium line or value line?",
                  "a": "The premium Dener lasers are built in Turkey on frames rated for up to 1.5 G, with Boji BLT autofocus heads and Raycus sources (Precitec and IPG on request), the longest life at high duty and parts stocked in Canada — for two shifts a day. NovoTech's own value line and the Senfeng value line are built in China with their own or Raycus sources, in a wider range — 4 × 4 ft compact machines, 60 – 80 kW plate gantries, sheet-and-tube combos, coil-fed lines — at a lower price; NovoTech stocks the parts and does the service for all of them. Same cut quality at the same power; the premium machine is faster between parts and lasts longer at high duty."},
                 {"q": "What laser power do I need?",
                  "a": "Power sets the thickness and the speed. As a guide for mild steel: 3 kW cuts 1/2″, 6 kW 3/4″ (and 1/4″ at over 300 in/min), 12 kW 1″, 20 kW 1-1/4″ and 30 – 40 kW 1-1/2″ and beyond; stainless and aluminum run about 20 – 30 % thinner at the same power, with nitrogen or air assist. Most Canadian job shops buying today choose 6 or 12 kW: thick enough for structural work, fast enough to pay for the machine on thin sheet. Tell us your material mix and we run the cutting chart for you."},
                 {"q": "Which table size?",
                  "a": "The model number is the nominal working area in centimetres: 3015 = 10 × 5 ft (3,000 × 1,500 mm) — a standard 4 × 8 or 5 × 10 sheet; 4020 = 13 × 6.6 ft; 6020 = 20 × 6.6 ft for 6 × 20 plate; 6025 and 8025 = 20 and 26 ft × 8.2 ft; 12526 = 41 × 8.5 ft. The 5 × 10 machine is the Canadian standard; buy the 6020 if you cut 20 ft plate or want to nest several sheets without reloading; the 4 × 4 ft Senfeng compact is for small parts in a small shop."},
                 {"q": "Single table, shuttle table or pallet changer?",
                  "a": "A single-table machine (Senfeng NP and compact, and the large-format Smart semi-closed, ULG and R / TX plate lasers) stops while you unload and load — fine for a few sheets an hour, the lowest price, and the only way to carry very long or heavy plate. A shuttle table or pallet changer (Dener GFL and Smart with shuttle table, NovoTech ULE, Senfeng H series) swaps tables in 15 to 30 seconds, so the laser cuts while the operator loads: the difference between 40 and 70 % spindle time on a busy machine, and the base for a loading tower later."},
                 {"q": "What about assist gas and fume extraction?",
                  "a": "Oxygen gives the fastest cut and an oxide edge on mild steel; nitrogen a clean, paint-ready edge on all metals; compressed air at 16 bar replaces nitrogen on sheet to about 1/4″ and cuts the gas bill to near zero — the intelligent air-cutting package is an option on both lines. The machines have pneumatic extraction compartments under the table and connect to a dust collector, which we can supply."},
                 {"q": "Can the laser be automated?",
                  "a": "Yes — a loading / unloading tower that feeds the pallet changer, sheet storage with several shelves for lights-out production, part sorting, and bevel heads for weld preparation. The Dener GFL and the Smart with shuttle table, the NovoTech ULE and the Senfeng H series are prepared for the tower; the Senfeng coil-fed lines go further and cut straight from the coil. Ask us for the automation layout."},
                 {"q": "What does the machine need on site?",
                  "a": "A level floor, 600 V 3-phase (with the transformer we supply) or 480 V, a chiller (included), assist gas, a dust collector and a compressed-air supply for air cutting. A 6 kW 3015 draws about 46 kW in total (Dener's figure for the GFL) and needs roughly 33 × 20 ft with its shuttle table. Delivery, installation and operator training are done by NovoTech from Mississauga, ON, Canada, and the Ontario pre-start health and safety review is prepared by us."},
                 VOLT_FAQ_GENERIC],
            faq_title="Questions we get asked about laser cutting machines",
            related_pages=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"},
                           {"href": "press-brake.html", "label": "Press brakes"}, {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring after laser cutting"},
                           {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "panel-bender.html", "label": "CNC panel benders"}],
            related_title="Machinery that works alongside a laser",
            artifact_title="Sheet Laser Cutters", nav_label="All sheet lasers",
        )),
    # the tube lasers are one page, no hub (the owner, Nov 1 2026): only the family set is written here; the page is
    # tube-laser-cutting-machine.html in tools/laser_types.py
    "tube": dict(set="tube-lasers", families=LN.families("tube"), page=None),
}

COMPARE = {
    "sheet": {
        "title": "Which kind of laser?",
        "lead": "The five kinds NovoTech sells, side by side. Sheets per day, the longest plate and what else you cut decide the kind; each page lists every model, premium and value lines together.",
        "cols": ["Kind", "Loading", "Working area and power", "Best for", "Page"],
        "rows": [
            ["Fiber lasers with shuttle table", "Shuttle table or pallet changer, laser-safe cabin; NP and compact single tables", "4 × 4 to 8.5 × 41 ft, 1.5 – 80 kW", "Production: cuts while you load, two shifts a day", {"href": "fiber-laser-cutting-machine.html", "label": "Fiber laser cutters"}],
            ["Sheet-and-tube lasers", "Table plus a rotary chuck", "to 41 × 8.5 ft sheet, tube to Ø13.8″, 1.5 – 40 kW", "One machine for sheet and tube", {"href": "sheet-and-tube-laser.html", "label": "Sheet & tube lasers"}],
            ["Large-format plate lasers", "Single table loaded by crane; semi-closed cover on the gantry; bevel heads, oxy-fuel", "to 13 × 82 ft and 10 × 164 ft, 3 – 60 kW", "Heavy plate, shipyards, structural, very long beds", {"href": "large-format-plate-laser.html", "label": "Large-format lasers"}],
            ["3D laser cells", "Five-axis head over a dual-station table", "5 × 10 ft envelope, 3 – 20 kW", "Trimming and cutting formed parts", {"href": "3d-laser-cutting-machine.html", "label": "3D laser cells"}],
            ["Coil-fed laser lines", "Decoiler, leveller and laser on one control", "thin, aluminum and 9/16″ coil, 1.5 – 80 kW", "High-volume blanks straight from coil", {"href": "coil-fed-laser-cutting-line.html", "label": "Coil-fed laser lines"}],
        ],
    },
}


def build():
    src = json.load(open(os.path.join(ROOT, "content", "families", "dener.json"), encoding="utf-8"))["families"]
    for kind, h in HUBS.items():
        sec = LN.SECTIONS[kind]
        fams = [dict(src[fid], page=slug, group=LN.group_of(kind, fid)) for slug, ids in h["families"] for fid in ids]
        write_families(h["set"], fams)
        if not sec["hub"]:
            print(f"{h['set']}: {len(fams)} families (one page, no hub)")
            continue
        pdfs, specs, seen = [], [], set()      # hero: brochures only (the owner, Nov 1 2026)
        for f in fams:
            for p in (f.get("pdf"), f.get("spec_pdf"), *(f.get("spec_pdfs") or [])):
                if p and p["file"] not in seen:
                    seen.add(p["file"]); (pdfs if p is f.get("pdf") else specs).append(p)
        pg = h["page"]
        write_hub(sec["hub"], {**pg, "related_blurb": sec["blurb"]}, fams, h["set"], sec["section"], LN.subpages(kind),
                  extra={"catalogue_pdf": None, "catalogue_pdfs": pdfs, "spec_downloads": specs, "range_pick": pg["range_pick"], "hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN,
                         "intro_video": None, "intro_video_heading": None, "intro_video_text": None,
                         "related_pages": pg["related_pages"], "related_title": pg["related_title"],
                         "hub_compact": True, "compare": COMPARE[kind], "subpage_link": "all models, specifications and photos",
                         "lineup_swaps": h.get("lineup_swaps", [])})
        path = os.path.join(ROOT, "content", "pages", f"{sec['hub']}.json")
        page = json.load(open(path, encoding="utf-8"))
        for sp, line in zip(page["subpages"], LN.lines(kind)):
            if line:
                sp["line"] = line
            sp["cards_title"] = sp["title"].split(" — ")[0] + " — every family"
        json.dump(page, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"{sec['hub']}: {len(fams)} families on {len(page['subpages'])} pages · {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
