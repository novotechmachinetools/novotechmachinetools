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

BRAND_LINE = ("Dener Makina builds the premium lasers in Kayseri, Turkey (since 1974, Dener Canada in Mississauga); NovoTech's own value line is built in "
              "China to our specification; Senfeng Laser builds its value line in Jinan, China (CE / FDA / ETL). All sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Three lines, one supplier", "text": "Premium Dener lasers from Turkey, NovoTech's own value line and the Senfeng value line from China — every machine with a "
          "CSA-approved panel, a chiller, nesting software, a 1-year warranty, and installation, training, parts and remote diagnostics from Mississauga, ON."}

HUBS = {
    "sheet": dict(
        set="sheet-lasers", families=[("dener-fiber-lasers", ["dn-gfl", "dn-smart-closed", "dn-smart-semi", "dn-smart-open"]),
                                      ("novotech-fiber-lasers", ["vn-ulf", "vn-ule", "vn-ulg", "vn-ulft", "vn-ulet"]),
                                      ("senfeng-fiber-lasers", ["sf-compact", "sf-np", "sf-h", "sf-hm", "sf-r", "sf-3d", "sf-coil"])],
        page=dict(
            title="Fiber Laser Cutting Machines, 1.5–80 kW, Canada | NovoTech",
            meta="Every sheet metal laser NovoTech sells: Dener GFL and Smart lasers 3–40 kW, NovoTech's own ULF and ULE value line to 60 kW, Senfeng from 4 × 4 ft to 80 kW.",
            h1="Laser cutting machines for sheet and plate — 4 × 4 ft to 10 × 164 ft, 1.5 to 80 kW",
            intro="A fiber laser cutting machine cuts sheet and plate from a DXF file with a focused beam — mild steel to 1-1/2″ and beyond with the "
                  "high-power sources, stainless and aluminum to 1″ — at speeds no plasma or punch can match, with a clean edge and no tooling. "
                  "NovoTech sells three lines of fiber lasers in Canada, each on its own page: the Dener lasers — the premium line, made in Turkey, "
                  "the GFL production laser with a 1.5 G gantry and pallet changer and the Smart series to 13 × 82 ft, 3 to 40 kW; NovoTech's own "
                  "value line — the open ULF single-table lasers, the enclosed ULE with a 15-second exchange table, the ULG ground-rail plate lasers, "
                  "the ULFT and ULET that cut sheet and tube on one machine, and plate tables to 85 ft with up to 60 kW; and the Senfeng lasers — a value line under its own brand, "
                  "from 4 × 4 ft compact machines and the NP open-type to the H series with pallet changer to 80 kW, plate gantries to 10 × 164 ft, "
                  "3D and coil-fed lines. Below, each line in brief, the "
                  "laser power guide, and every model in one table of working area, power and speed; every machine comes with a CSA-approved "
                  "panel, chiller, nesting software, a 1-year warranty and installation, training and parts from Mississauga, ON.",
            points=["Dener premium line: GFL 1.5 G with pallet changer, 5 × 10 to 6.6 × 20 ft; Smart closed, semi-closed and open lasers to 13 × 82 ft; 3 – 40 kW",
                    "NovoTech value line: open ULF from 10 × 5 ft, enclosed ULE with 15 s exchange table to 41 ft, ULG ground-rail to 85 × 14.8 ft, ULFT / ULET sheet + tube, 1.5 – 60 kW",
                    "Senfeng value line: compact 4 × 4 ft from 1.5 kW, NP open-type, H series with pallet changer to 80 kW, plate gantries to 164 ft, 3D, coil-fed"],
            hero="dn-gfl-3", minis=["vn-ule-1", "sf-h-1"],
            range_cols=["Working area", "Laser power", "Max. speed", "Acceleration", "Max. sheet load"],
            range_pick=[["working_area", "area"], "power", "speed", "accel", "load"],
            range_lead="Every sheet laser model NovoTech sells, in one table: working area, laser power, axis speed, acceleration and the maximum sheet weight on the table, where the maker publishes them. Each row links to the full specification table on the line's page.",
            range_caption="Sheet and plate fiber lasers supplied by NovoTech — Dener, NovoTech value line and Senfeng",
            range_note="Working areas in feet and inches (millimetres); the model number is the nominal table in decimetres (3015 = 3,000 × 1,500 mm, 10 × 5 ft). Laser power as the sources offered on that model. "
                       "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel and transformer; 208, 240 and 480 V on request.",
            faq=[{"q": "Dener, NovoTech or Senfeng — which laser should I buy?",
                  "a": "Dener is the premium line: Turkish-built, with Precitec heads, IPG / nLIGHT sources and a heavier frame rated for 1.5 G, Dener Canada parts in Mississauga and the longer life at high duty — the machine for a job shop that cuts two shifts a day. NovoTech's own value line is built in China to our specification — Raycus or IPG sources, Cypcut controls, Hiwin, YYC and Schneider components — at the lowest price of the three, in open, enclosed exchange-table, ground-rail and sheet-and-tube versions to 60 kW. Senfeng is a value line under its own brand from a very large Chinese manufacturer (about 15,000 machines a year) that builds its own sources and heads, CE / FDA / ETL certified, with the widest range: 4 × 4 ft compact machines, 80 kW, 3D and coil-fed lasers. All three are sold, installed and supported by NovoTech with the same CSA panel and warranty; we quote them side by side so you can compare."},
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
                  "a": "A level floor, 600 V 3-phase (with the transformer we supply) or 480 V, a chiller (included), assist gas, a dust collector and a compressed-air supply for air cutting. A 6 kW 3015 draws about 30 kW in total and needs roughly 33 × 20 ft with a pallet changer. Delivery, installation and operator training are done by NovoTech from Mississauga, and the Ontario pre-start health and safety review is prepared by us."},
                 VOLT_FAQ_GENERIC],
            faq_title="Questions we get asked about laser cutting machines",
            related_pages=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"},
                           {"href": "press-brake.html", "label": "Press brakes"}, {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring after laser cutting"},
                           {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "panel-bender.html", "label": "CNC panel benders"}],
            related_title="Machinery that works alongside a laser",
            artifact_title="Sheet Laser Cutters", nav_label="All sheet lasers",
        )),
    "tube": dict(
        set="tube-lasers", families=[("dener-tube-lasers", ["dn-eftl", "dn-ftl"]), ("novotech-tube-lasers", ["vn-ult"]),
                                     ("senfeng-tube-lasers", ["sf-t", "sf-plus", "sf-heavy"])],
        page=dict(
            title="Tube Laser Cutting Machines, Ø0.3″ to 25″, Canada | NovoTech",
            meta="Every tube laser NovoTech sells: Dener E-FTL and FTL to Ø25.2″, NovoTech's own ULT two- and three-chuck lasers to Ø14.2″, Senfeng from Ø0.5″ to 49 ft bars.",
            h1="Tube and profile laser cutting machines — Ø0.3″ to 25.2″, 20 to 49 ft bars, 1.5 to 40 kW",
            intro="A tube laser cuts round, square, rectangular and open profiles to length and cuts the holes, copes, slots and notches in them in one "
                  "pass — no saw, no drill, no notcher, no layout — straight from the 3D model. NovoTech sells three lines of tube lasers in Canada, "
                  "each on its own page: the Dener tube lasers — the premium line, made in Turkey, the E-FTL with 1 G servo chucks for Ø0.3″ to 13.8″ "
                  "and the heavy FTL for structural tube, pipe and beams to Ø25.2″ and 12 m bars of 2,600 kg; NovoTech's own ULT — the value line, "
                  "two or three pneumatic chucks for Ø0.4″ to 14.2″ on 20 to 39 ft bars with 1.5 to 40 kW; and the Senfeng tube lasers — a "
                  "value line under its own brand, from the Ø0.5″ two-chuck T series with 1.5 kW to the high-speed PLUS, the 45° bevel GT, the "
                  "zero-tailing NT and the three- and four-chuck ST / HT machines to Ø25″, 6,600 lb and 49 ft. For trailer, railing, furniture, "
                  "agricultural, HVAC and steel-construction work. Below, each line in brief and every model in one table of tube range, power, "
                  "speed and bar length; every machine comes with a CSA-approved panel, chiller, tube nesting software, a 1-year warranty and "
                  "installation, training and parts from Mississauga, ON.",
            points=["Dener premium line: E-FTL Ø0.3″ – 13.8″, 1 G, 394 ft/min, ±0.05 mm; FTL Ø0.6″ – 25.2″, bars to 39.4 ft and 5,732 lb",
                    "NovoTech value line: ULT two- and three-chuck lasers Ø0.4″ – 14.2″, square to 13.8″, 20 – 39 ft bars to 2,205 lb, 1.5 – 40 kW",
                    "Senfeng value line: T, PLUS and 45° bevel GT lasers Ø0.5″ – 14″; NT zero-tailing, ST / HT three- and four-chuck lasers to Ø25″ and 49 ft"],
            hero="dn-tube-2", minis=["vn-ult-1", "sf-t-1"],
            range_cols=["Round tube", "Laser power", "Max. speed", "Bar length", "Max. bar weight"],
            range_pick=[["tube", "round"], "power", "speed", "length", "load"],
            range_lead="Every tube laser model NovoTech sells, in one table: round tube range, laser power, axis speed, bar length and — for the NovoTech and Senfeng machines — the maximum bar weight. Each row links to the full specification table on the line's page.",
            range_caption="Tube and profile fiber lasers supplied by NovoTech — Dener, NovoTech value line and Senfeng",
            range_note="Round tube as the chuck's minimum to maximum diameter; square and rectangular tube is limited by the diagonal. Dener bar lengths list the bar weight with them. "
                       "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel and transformer; 208, 240 and 480 V on request.",
            faq=[{"q": "Dener, NovoTech or Senfeng — which tube laser should I buy?",
                  "a": "Dener's E-FTL and FTL are the premium machines — Turkish-built, 1 G servo chucks, Precitec heads, ±0.05 mm, Dener Canada parts in Mississauga — for the shop that runs the tube laser all day on precise work. NovoTech's own ULT is the value line we build to our specification: two or three pneumatic chucks for the Ø0.4 to 14.2″ tube most shops cut, at the lowest price of the three. Senfeng's tube lasers are a value line under their own brand: a 6 m two-chuck machine with a 1.5 kW source costs a fraction of a premium tube laser and cuts the railings, frames and furniture tube most shops run, and the range goes where few others do — zero-tailing three-chuck machines, four-chuck machines for 49 ft stock, Ø25″ pipe and the H-beam profile line. We quote all three so you can compare."},
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


def build():
    src = json.load(open(os.path.join(ROOT, "content", "families", "dener.json"), encoding="utf-8"))["families"]
    for kind, h in HUBS.items():
        sec = LN.SECTIONS[kind]
        fams = [dict(src[fid], page=slug) for slug, ids in h["families"] for fid in ids]
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
                         "related_pages": pg["related_pages"], "related_title": pg["related_title"]})
        path = os.path.join(ROOT, "content", "pages", f"{sec['hub']}.json")
        page = json.load(open(path, encoding="utf-8"))
        for sp, line in zip(page["subpages"], LN.lines(kind)):
            if line:
                sp["line"] = line
            sp["cards_title"] = sp["title"].split(" — ")[0] + " — the line-up"
        json.dump(page, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"{sec['hub']}: {len(fams)} families on {len(page['subpages'])} pages · {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
