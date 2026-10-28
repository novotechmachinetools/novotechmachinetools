#!/usr/bin/env python3
"""The two laser hubs (hub.html template): laser-cutting-machine.html over dener-fiber-lasers + novotech-fiber-lasers +
senfeng-fiber-lasers, and tube-laser-cutting-machine.html over dener-tube-lasers + novotech-tube-lasers + senfeng-tube-lasers —
each line introduced with its family cards, plus the whole range in one capacity table, like the press-brake and rebar hubs.

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

BRAND_LINE = ("Dener Makina builds the premium lasers in Kayseri, Turkey (since 1974, Dener Canada in Mississauga, ON, Canada); NovoTech's own value line is built in "
              "China to our specification; Senfeng Laser builds its value line in Jinan, China (CE / FDA / ETL). All sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Premium and value lines, one supplier", "text": "Premium Dener lasers from Turkey, NovoTech's own value line and the Senfeng value line from China — every machine with a "
          "CSA-approved panel, a chiller, nesting software, a 1-year warranty, and installation, training, parts and remote diagnostics from Mississauga, ON, Canada."}

HUBS = {
    "sheet": dict(
        set="sheet-lasers", families=LN.families("sheet"),
        page=dict(
            title="Fiber Laser Cutting Machines for Sale in Canada — Enclosed, Open-Type, Plate & Tube, 1.5–80 kW | NovoTech",
            meta="Every fiber laser NovoTech sells in Canada, by kind: enclosed lasers with exchange table or pallet changer, open-type single-table lasers, large-format plate lasers to 10 × 164 ft, sheet-and-tube combination lasers, 3D cells and coil-fed lines — 1.5 to 80 kW, premium and value lines, the kinds compared and every model in one table.",
            h1="Laser cutting machines for sheet and plate — enclosed, open-type, plate and sheet-and-tube lasers, 1.5 to 80 kW",
            intro="A fiber laser cutting machine cuts sheet and plate from a DXF file with a focused beam — mild steel to 1-1/2″ and beyond with the "
                  "high-power sources, stainless and aluminum to 1″ — at speeds no plasma or punch can match, with a clean edge and no tooling. "
                  "NovoTech sells five kinds in Canada, each on its own page: enclosed lasers with a laser-safe cabin and an exchange table or pallet "
                  "changer, the production machine from 4 × 4 ft compact models to 8.5 × 41 ft and 80 kW; open-type single-table and semi-closed "
                  "lasers, the entry and long-plate machines to 85 ft; large-format plate lasers on ground rails or gantries to 10 × 164 ft with bevel "
                  "heads; sheet-and-tube combination lasers with a rotary chuck beside the table; and 3D laser cells and coil-fed lines. Each kind comes "
                  "in a premium line made in Turkey and a value line built to our specification, as sections on the same page. Below, the five kinds "
                  "compared, the laser power guide and every model in one table of working area, power and speed; every machine comes with a "
                  "CSA-approved panel, chiller, nesting software, a 1-year warranty and installation, training and parts from Mississauga, ON, Canada.",
            points=["Enclosed: exchange table or pallet changer, 4 × 4 ft compact to 8.5 × 41 ft, 1.5 – 80 kW — premium GFL / Smart closed, value ULE, H series, compact",
                    "Open-type and semi-closed: single tables 5 × 10 to 85 × 10.5 ft, 1.5 – 60 kW; plate lasers on ground rails and gantries to 10 × 164 ft with ±45° bevel",
                    "Sheet-and-tube lasers to Ø13.8″ tube; five-axis 3D cells and robot cells; coil-fed lines to 9/16″ plate"],
            hero="dn-gfl-3", minis=["vn-ule-1", "sf-h-1"],
            range_cols=["Working area", "Laser power", "Max. speed", "Acceleration", "Max. sheet load"],
            range_pick=[["working_area", "area"], "power", "speed", "accel", "load"],
            range_lead="Every sheet laser model NovoTech sells, in one table: working area, laser power, axis speed, acceleration and the maximum sheet weight on the table, where the maker publishes them. Each row links to the full specification table on the line's page.",
            range_caption="Sheet and plate fiber lasers supplied by NovoTech — enclosed, open-type, plate, sheet-and-tube, 3D and coil-fed, premium and value lines",
            range_note="Working areas in feet and inches (millimetres); the model number is the nominal table in decimetres (3015 = 3,000 × 1,500 mm, 10 × 5 ft). Laser power as the sources offered on that model. "
                       "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel and transformer; 208, 240 and 480 V on request.",
            faq=[{"q": "Enclosed, open-type, plate or sheet-and-tube — which laser should I buy?",
                  "a": "By how many sheets a day and what they are. An enclosed laser with an exchange table or pallet changer keeps cutting while you load the next sheet and keeps fumes and the beam inside — the production machine, and the one most shops buy from 5 × 10 ft up. An open-type single-table laser stops while you load but costs less and takes sheets from any side — the first laser, and the only kind for 20 to 85 ft plate on a single table. A ground-rail or gantry plate laser is for heavy plate and very long beds, with bevel heads and oxy-fuel. A sheet-and-tube laser adds a rotary chuck beside the table for a shop that cuts both and has room for one machine. 3D cells cut formed parts; coil-fed lines cut straight from the coil. Each kind has its own page with the premium and value lines side by side."},
                 {"q": "Premium line or value line?",
                  "a": "The premium Dener lasers are built in Turkey on frames rated for 1.5 G, with Precitec heads, IPG / nLIGHT sources, the longest life at high duty and Dener Canada parts in Mississauga, ON, Canada — for two shifts a day. NovoTech's own value line and the Senfeng value line are built in China with their own or Raycus sources, in a wider range — 4 × 4 ft compact machines, 60 – 80 kW plate gantries, sheet-and-tube combos, coil-fed lines — at a lower price; NovoTech stocks the parts and does the service for all of them. Same cut quality at the same power; the premium machine is faster between parts and lasts longer at high duty."},
                 {"q": "What laser power do I need?",
                  "a": "Power sets the thickness and the speed. As a guide for mild steel: 3 kW cuts 1/2″, 6 kW 3/4″ (and 1/4″ at over 300 in/min), 12 kW 1″, 20 kW 1-1/4″ and 30 – 40 kW 1-1/2″ and beyond; stainless and aluminum run about 20 – 30 % thinner at the same power, with nitrogen or air assist. Most Canadian job shops buying today choose 6 or 12 kW: thick enough for structural work, fast enough to pay for the machine on thin sheet. Tell us your material mix and we run the cutting chart for you."},
                 {"q": "Which table size?",
                  "a": "The model number is the nominal working area in centimetres: 3015 = 10 × 5 ft (3,000 × 1,500 mm) — a standard 4 × 8 or 5 × 10 sheet; 4020 = 13 × 6.6 ft; 6020 = 20 × 6.6 ft for 6 × 20 plate; 6025 and 8025 = 20 and 26 ft × 8.2 ft; 12526 = 41 × 8.5 ft. The 5 × 10 machine is the Canadian standard; buy the 6020 if you cut 20 ft plate or want to nest several sheets without reloading; the 4 × 4 ft Senfeng compact is for small parts in a small shop."},
                 {"q": "Single table, double table or pallet changer?",
                  "a": "A single-table machine (Dener Smart open and semi-closed, NovoTech ULF, Senfeng compact and NP) stops while you unload and load — fine for a few sheets an hour and the lowest price. A double table or pallet changer (Dener GFL and Smart closed, NovoTech ULE, Senfeng H series) swaps tables in 15 to 20 seconds, so the laser cuts while the operator loads: the difference between 40 and 70 % spindle time on a busy machine, and the base for a loading tower later."},
                 {"q": "What about assist gas and fume extraction?",
                  "a": "Oxygen gives the fastest cut and an oxide edge on mild steel; nitrogen a clean, paint-ready edge on all metals; compressed air at 16 bar replaces nitrogen on sheet to about 1/4″ and cuts the gas bill to near zero — the intelligent air-cutting package is an option on both lines. The machines have pneumatic extraction compartments under the table and connect to a dust collector, which we can supply."},
                 {"q": "Can the laser be automated?",
                  "a": "Yes — a loading / unloading tower that feeds the pallet changer, sheet storage with several shelves for lights-out production, part sorting, and bevel heads for weld preparation. The Dener GFL and closed-type Smart, the NovoTech ULE and the Senfeng H series are prepared for the tower; the Senfeng coil-fed lines go further and cut straight from the coil. Ask us for the automation layout."},
                 {"q": "What does the machine need on site?",
                  "a": "A level floor, 600 V 3-phase (with the transformer we supply) or 480 V, a chiller (included), assist gas, a dust collector and a compressed-air supply for air cutting. A 6 kW 3015 draws about 30 kW in total and needs roughly 33 × 20 ft with a pallet changer. Delivery, installation and operator training are done by NovoTech from Mississauga, ON, Canada, and the Ontario pre-start health and safety review is prepared by us."},
                 VOLT_FAQ_GENERIC],
            faq_title="Questions we get asked about laser cutting machines",
            related_pages=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"},
                           {"href": "press-brake.html", "label": "Press brakes"}, {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring after laser cutting"},
                           {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "panel-bender.html", "label": "CNC panel benders"}],
            related_title="Machinery that works alongside a laser",
            artifact_title="Sheet Laser Cutters", nav_label="All sheet lasers",
        )),
    "tube": dict(
        set="tube-lasers", families=LN.families("tube"),
        page=dict(
            title="Tube Laser Cutting Machines for Sale in Canada — Ø0.3″ to 25″, 20 to 49 ft Bars | NovoTech",
            meta="Every tube and profile laser NovoTech sells in Canada, by kind: tube laser cutters to Ø14″ with two or three chucks and heavy-duty three- and four-chuck machines to Ø25″ and 49 ft, 1.5 to 40 kW — premium and value lines, the two kinds compared and every model in one table.",
            h1="Tube and profile laser cutting machines — Ø0.3″ to 25.2″, 20 to 49 ft bars, 1.5 to 40 kW",
            intro="A tube laser cuts round, square, rectangular and open profiles to length and cuts the holes, copes, slots and notches in them in one "
                  "pass — no saw, no drill, no notcher, no layout — straight from the 3D model. NovoTech sells two kinds in Canada, each on its own "
                  "page: tube laser cutters for tube to Ø14″ with two or three chucks on 20 to 39 ft bars — the premium E-FTL with 1 G servo chucks "
                  "made in Turkey, NovoTech's value-line ULT and the T series, high-speed PLUS and bevel-cutting GT; and heavy-duty tube and profile "
                  "lasers with three and four chucks for structural tube, pipe and beams to Ø25″, 6,600 lb and 49 ft, plus the H-beam profile line. "
                  "For trailer, railing, furniture, agricultural, HVAC and steel-construction work. Below, the two kinds compared and every model in "
                  "one table of tube range, power, speed and bar length; every machine comes with a CSA-approved panel, chiller, tube nesting "
                  "software, a 1-year warranty and installation, training and parts from Mississauga, ON, Canada.",
            points=["Tube laser cutters: premium E-FTL Ø0.3″ – 13.8″, 1 G, ±0.05 mm; value ULT Ø0.4″ – 14.2″ two or three chucks; T / PLUS / GT Ø0.5″ – 14″ — 20 – 39 ft bars, 1.5 – 40 kW",
                    "Heavy-duty: premium FTL Ø0.6″ – 25.2″, bars to 39.4 ft and 5,732 lb; NT zero-tailing, ST / HT three- and four-chuck lasers to Ø25″, 6,600 lb and 49 ft",
                    "Bundle loaders, following supports, ±45° bevel heads, STEP / IGES import and tube nesting on every machine"],
            hero="dn-tube-2", minis=["vn-ult-1", "sf-t-1"],
            range_cols=["Round tube", "Laser power", "Max. speed", "Bar length", "Max. bar weight"],
            range_pick=[["tube", "round"], "power", "speed", "length", "load"],
            range_lead="Every tube laser model NovoTech sells, in one table: round tube range, laser power, axis speed, bar length and — for the NovoTech and Senfeng machines — the maximum bar weight. Each row links to the full specification table on the line's page.",
            range_caption="Tube and profile fiber lasers supplied by NovoTech — tube laser cutters and heavy-duty machines, premium and value lines",
            range_note="Round tube as the chuck's minimum to maximum diameter; square and rectangular tube is limited by the diagonal. Dener bar lengths list the bar weight with them. "
                       "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel and transformer; 208, 240 and 480 V on request.",
            faq=[{"q": "Tube laser cutter or heavy-duty tube laser — which should I buy?",
                  "a": "By the biggest bar you cut. A two- or three-chuck tube laser cutter covers tube to Ø14″ on 20 to 39 ft bars — railing, furniture, trailer, HVAC, agricultural and most steel-construction work — and is the machine most shops need; the premium E-FTL and the value-line ULT, T and PLUS are on one page, side by side. A heavy-duty machine with three or four chucks holds beams and pipe to Ø25″, bars of 2,600 – 3,000 kg and 49 ft, and cuts them without tailing — for structural steel, pipe and heavy profiles. Both kinds load from a bundle, support the bar as it is cut and take bevel heads."},
                 {"q": "Premium line or value line?",
                  "a": "The premium Dener E-FTL and FTL are built in Turkey with 1 G servo chucks, Precitec heads, ±0.05 mm and Dener Canada parts in Mississauga, ON, Canada — for the shop that runs the tube laser all day. NovoTech's value-line ULT and the Senfeng T / PLUS / GT / NT / ST / HT are built in China with pneumatic chucks, in a wider range of sizes and powers at a lower price; NovoTech stocks the parts and does the service. The premium machine is faster between parts and holds tighter tolerance at high duty."},
                 {"q": "What can a tube laser cut?",
                  "a": "Round, square, rectangular, oval and open profiles — angle, channel, flat bar — in mild steel, stainless, aluminum, copper and brass, from the chuck's minimum to its maximum size, in wall thicknesses to about 1/2″ (12 kW) or 3/4″ (20 kW). Holes, slots, copes for tube-to-tube joints, tabs and notches for folding, engraving — anything you can draw on the surface of the profile. A 5-axis or 45° bevel head adds weld preparations and mitred corners."},
                 {"q": "Two, three or four chucks?",
                  "a": "Two chucks (Dener E-FTL / FTL, NovoTech ULT, Senfeng T / PLUS) hold the bar at both ends and cover tube to Ø25″ — the machine most shops need. A third chuck in the middle (NovoTech ULT three-chuck, Senfeng NT) takes over the bar as it shortens, so the last part is cut without a tail. Three and four chucks on the heavy machines (Senfeng ST / HT) carry 49 ft bars of 6,600 lb without sag for structural sections and towers."},
                 {"q": "How is the tube loaded?",
                  "a": "From a bundle: the automatic loader separates one bar, measures it and feeds it to the rear chuck; the front chuck and following supports hold the bar as it is cut; finished parts drop onto the unloading table or conveyor and the remnant is ejected. One operator runs the machine while loading the next bundle. Loading lengths of 7, 9 and 12 m — or manual loading on the small Senfeng T series."},
                 {"q": "What about software?",
                  "a": "The CNC imports STEP / IGES solid models of the tube parts, unfolds them onto the profile, nests them along the bar to use the remnant and writes the program — with the cutting database for the material and seam detection to orient welded tube. Offline programming on a PC is standard on both lines."},
                 {"q": "Floor space and power?",
                  "a": "A 7 m machine needs about 20 m (65 ft) of length including the loader and unloader; a 12 m machine about 30 m. 600 V 3-phase with the supplied transformer or 480 V, a chiller (included), assist gas and a dust collector. We lay the machine out for your building before you order."},
                 VOLT_FAQ_GENERIC],
            faq_title="Questions we get asked about tube lasers",
            related_pages=[{"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"},
                           {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "pipe-notcher.html", "label": "Tube notchers"},
                           {"href": "tube-end-forming-machines.html", "label": "Tube end formers"}, {"href": "band-saw.html", "label": "Band saws"}],
            related_title="More tube machinery from NovoTech",
            artifact_title="Tube Laser Cutters", nav_label="All tube lasers",
        )),
}

COMPARE = {
    "sheet": {
        "title": "Which kind of laser?",
        "lead": "The five kinds NovoTech sells, side by side. Sheets per day, the longest plate and what else you cut decide the kind; each page lists every model, premium and value lines together.",
        "cols": ["Kind", "Loading", "Working area and power", "Best for", "Page"],
        "rows": [
            ["Enclosed lasers", "Exchange table or pallet changer, laser-safe cabin", "4 × 4 to 8.5 × 41 ft, 1.5 – 80 kW", "Production: cuts while you load, two shifts a day", {"href": "enclosed-fiber-laser.html", "label": "Enclosed lasers"}],
            ["Open-type and semi-closed lasers", "Single table loaded from any side", "5 × 10 to 85 × 10.5 ft, 1.5 – 60 kW", "First laser, long plate, lowest price", {"href": "open-type-fiber-laser.html", "label": "Open-type lasers"}],
            ["Large-format plate lasers", "Ground rails or gantry, bevel heads, oxy-fuel", "to 10 × 164 ft, 6 – 60 kW", "Heavy plate, shipyards, structural, very long beds", {"href": "large-format-plate-laser.html", "label": "Plate lasers"}],
            ["Sheet-and-tube lasers", "Table plus a rotary chuck", "to 85 ft sheet, tube to Ø13.8″, 1.5 – 40 kW", "One machine for sheet and tube", {"href": "sheet-and-tube-laser.html", "label": "Sheet & tube lasers"}],
            ["3D cells and coil-fed lines", "Five-axis head or robot; uncoiler and leveller", "1.5 – 80 kW", "Formed parts; high-volume blanks from coil", {"href": "3d-laser-and-coil-fed-line.html", "label": "3D & coil-fed lasers"}],
        ],
    },
    "tube": {
        "title": "Which kind of tube laser?",
        "lead": "The two kinds NovoTech sells, side by side. The biggest bar you cut decides; each page lists every model, premium and value lines together.",
        "cols": ["Kind", "Chucks", "Tube range and bars", "Best for", "Page"],
        "rows": [
            ["Tube laser cutters", "Two or three chucks", "Ø0.3″ – 14″, 20 – 39 ft bars, 1.5 – 40 kW", "Railing, furniture, trailer, HVAC, agricultural, most steel construction", {"href": "tube-laser-cutter.html", "label": "Tube laser cutters"}],
            ["Heavy-duty tube and profile lasers", "Three or four chucks, zero tailing", "Ø0.6″ – 25.2″, bars to 49 ft and 6,600 lb, 3 – 40 kW", "Structural tube, pipe, beams and heavy profiles", {"href": "heavy-duty-tube-laser.html", "label": "Heavy-duty tube lasers"}],
        ],
    },
}


def build():
    src = json.load(open(os.path.join(ROOT, "content", "families", "dener.json"), encoding="utf-8"))["families"]
    for kind, h in HUBS.items():
        sec = LN.SECTIONS[kind]
        fams = [dict(src[fid], page=slug, group=LN.group_of(kind, fid)) for slug, ids in h["families"] for fid in ids]
        write_families(h["set"], fams)
        pdfs, seen = [], set()
        for f in fams:
            p = f.get("pdf")
            if p and p["file"] not in seen:
                seen.add(p["file"]); pdfs.append(p)
        pg = h["page"]
        write_hub(sec["hub"], {**pg, "related_blurb": sec["blurb"]}, fams, h["set"], sec["section"], LN.subpages(kind),
                  extra={"catalogue_pdf": None, "catalogue_pdfs": pdfs, "range_pick": pg["range_pick"], "hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN,
                         "intro_video": None, "intro_video_heading": None, "intro_video_text": None,
                         "related_pages": pg["related_pages"], "related_title": pg["related_title"],
                         "hub_compact": True, "compare": COMPARE[kind], "subpage_link": "all models, specifications and photos"})
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
