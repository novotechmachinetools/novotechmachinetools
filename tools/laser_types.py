#!/usr/bin/env python3
"""The laser pages, one per kind of machine, under the two laser hubs (tools/laser_nav.py): five sheet-laser pages and two
tube-laser pages.  Each holds every family of that kind NovoTech sells, premium and value lines as sections, with the spec
tables, photos, videos and brochures of the families (family sets content/families/sheet-lasers.json and tube-lasers.json,
merged by tools/laser_hub.py — run that first):

    python3 tools/laser_hub.py && python3 tools/laser_types.py

The pages replace the supplier pages dener-fiber-lasers, novotech-fiber-lasers, senfeng-fiber-lasers, dener-tube-lasers,
novotech-tube-lasers and senfeng-tube-lasers (301s in src/root/.htaccess).  FAQ answers of the former pages are kept in
tools/laser_copy.json."""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category
import laser_nav as LN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY = json.load(open(os.path.join(ROOT, "tools", "laser_copy.json"), encoding="utf-8"))

BRAND_LINE = ("The premium lasers are built by Dener Makina in Kayseri, Turkey (Dener Canada parts in Mississauga, ON, Canada); NovoTech's own value line is built in "
              "China to our specification; the Senfeng value line in Jinan, China (CE / FDA / ETL). All sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Premium and value lines, one supplier", "text": "Every laser comes with a CSA-approved panel, a chiller, nesting software, a 1-year warranty, and installation, training, parts and remote diagnostics from Mississauga, ON, Canada — whichever line you choose."}
SHEET_RANGE = {"range_pick": [["working_area", "area"], "power", "speed", "accel", "load"], "range_cols": ["Working area", "Laser power", "Max. speed", "Acceleration", "Max. sheet load"]}
TUBE_RANGE = {"range_pick": [["tube", "round"], "power", "speed", "length", "load"], "range_cols": ["Round tube", "Laser power", "Max. speed", "Bar length", "Max. bar weight"]}


def faq(page, *questions):
    out = []
    for q in questions:
        hit = next((f for f in COPY[page]["faq"] if f["q"].startswith(q)), None)
        if not hit:
            raise SystemExit(f"FAQ not found on {page}: {q}")
        out.append(hit)
    return out


POWER_FAQ = faq("laser-cutting-machine", "What laser power do I need?")[0]
TABLE_FAQ = faq("laser-cutting-machine", "Which table size?")[0]
GAS_FAQ = faq("laser-cutting-machine", "What about assist gas and fume extraction?")[0]
SITE_FAQ = faq("laser-cutting-machine", "What does the machine need on site?")[0]
AUTO_FAQ = faq("laser-cutting-machine", "Can the laser be automated?")[0]

SHEET = {
    "enclosed-fiber-laser": dict(
        title="Enclosed Fiber Laser Cutting Machines for Sale in Canada — Exchange Table & Pallet Changer, 1.5–80 kW | NovoTech",
        meta="Enclosed fiber lasers sold, installed and supported in Canada: laser-safe cabin and exchange table or pallet changer, 4 × 4 ft compact machines to 8.5 × 41 ft, 1.5 to 80 kW — premium GFL and Smart closed-type made in Turkey, value-line ULE, H series and compact lasers. Every model in one table.",
        h1="Enclosed fiber laser cutting machines — exchange table and pallet changer, 4 × 4 ft to 8.5 × 41 ft, 1.5 to 80 kW",
        intro="An enclosed fiber laser cuts inside a laser-safe cabin with fume extraction, and its exchange table or pallet changer loads the next "
              "sheet while the first is being cut — the production laser that keeps cutting while the operator unloads, and the kind most shops "
              "buy from 5 × 10 ft up. NovoTech sells two lines in Canada, both on this page: the premium Dener lasers made in Turkey — the GFL with "
              "a space-frame gantry rated for 1.5 G and a pallet changer in 5 × 10 to 6.6 × 20 ft, 3 to 40 kW, and the Smart closed-type with a "
              "double exchange table in six sizes to 8.5 × 41 ft; and the value line — NovoTech's own ULE with a 15-second exchange table to 41 ft, "
              "the H series with pallet changer from 5 × 10 to 8.3 × 40 ft and 1.5 to 80 kW, and compact enclosed lasers of 4 × 4 and 5 × 10 ft "
              "from 1.5 kW. Every model is in the table below with its working area, power and speed, then each family with its full specification, "
              "photos and brochure. Every machine comes with a CSA-approved panel, chiller and nesting software, installed, trained and supported "
              "from Mississauga, ON, Canada. For a single-table machine at a lower price see the open-type lasers; for heavy plate the plate lasers.",
        points=["Premium: GFL 1.5 G with pallet changer, 5 × 10 to 6.6 × 20 ft, 3 – 40 kW; Smart closed-type with double table, six sizes to 8.5 × 41 ft",
                "Value: ULE enclosed lasers with 15 s exchange table 10 × 5 to 41 × 8.5 ft, 3 – 40 kW; H series with pallet changer to 8.3 × 40 ft and 80 kW",
                "Compact enclosed lasers 4 × 4 and 5 × 10 ft from 1.5 kW — the smallest production laser; towers and sheet storage for all"],
        hero="dn-gfl-3", minis=["vn-ule-1", "sf-h-1"],
        groups=[("ls-premium-gfl", "GFL production fiber lasers · premium line", "Dener's premium sheet laser: 1.5 G, pallet changer, 3 – 40 kW — built for a job shop that cuts all day."),
                ("ls-premium-closed", "Smart closed-type fiber lasers · premium line", "The economy line from the same Turkish factory: a double exchange table and 1 G in six sizes to 8.5 × 41 ft."),
                ("ls-value-ule", "ULE enclosed fiber lasers · value line", "NovoTech's own enclosed laser with a 15-second exchange table, 10 × 5 to 41 × 8.5 ft, 3 – 40 kW."),
                ("ls-value-h", "H series enclosed lasers with pallet changer · value line", "The widest range: 5 × 10 to 8.3 × 40 ft and 1.5 to 80 kW, with towers and storage."),
                ("ls-value-compact", "Compact enclosed lasers · value line", "4 × 4 and 5 × 10 ft machines from 1.5 kW — the enclosed laser for the small shop.")],
        faq=[{"q": "Exchange table or pallet changer — what is the difference?",
              "a": "Both load the next sheet while the first is cut. An exchange table (Smart closed-type, ULE, compact) has two tables that swap places in 15 – 25 seconds, one in the cabin cutting and one outside being loaded. A pallet changer (GFL, H series) lifts the pallet with the cut sheet out of the cabin and slides the loaded pallet in, which is the arrangement a loading tower and sheet storage connect to for lights-out production. For a few sheets an hour the exchange table is enough; for automation, the pallet changer."},
             {"q": "Premium line or value line?",
              "a": "The premium GFL and Smart closed-type are built by Dener in Turkey on stress-relieved frames — the GFL rated for 1.5 G — with Precitec heads, IPG / nLIGHT sources, longer life at high duty and Dener Canada parts in Mississauga, ON, Canada: the machines for two shifts a day. NovoTech's value-line ULE, the H series and the compact lasers are built in China with their own or Raycus sources in a wider range — 4 × 4 ft machines, 60 – 80 kW — at a lower price; NovoTech stocks the parts and does the service. Same cut quality at the same power."},
             POWER_FAQ, TABLE_FAQ, AUTO_FAQ, GAS_FAQ,
             faq("dener-fiber-lasers", "What is in a Dener laser as standard?")[0],
             SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "press-brake.html", "label": "Press brakes"},
                 {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring after laser cutting"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"}],
    ),
    "open-type-fiber-laser": dict(
        title="Open-Type Fiber Lasers for Sale in Canada — Single-Table & Semi-Closed, 5 × 10 to 85 ft, 1.5–60 kW | NovoTech",
        meta="Open-type fiber laser cutting machines sold, installed and supported in Canada: single-table lasers loaded from any side, 5 × 10 to 85 × 10.5 ft, semi-closed machines to 13 × 82 ft, 1.5 to 60 kW — premium Smart open and semi-closed made in Turkey, value-line ULF and NP. Every model in one table.",
        h1="Open-type fiber lasers — single-table and semi-closed, 5 × 10 to 85 × 10.5 ft, 1.5 to 60 kW",
        intro="An open-type fiber laser has a single table that is loaded by hand, forklift or crane from any side and stops while the sheet is "
              "changed — the lowest-priced fiber laser, the first laser for many shops, and the only kind that cuts 20 to 85 ft plate on one "
              "table. NovoTech sells two lines in Canada, both on this page: the premium Dener Smart open-type, 3 or 6 kW in 5 × 10 to 6.6 × 20 ft, "
              "and the Smart semi-closed single-table machines from 8.2 × 20 to 13 × 82 ft for long plate, all made in Turkey; and the value line "
              "— NovoTech's own ULF open lasers from 10 × 5 to 85 × 10.5 ft and 1.5 to 60 kW, and the NP series from 5 × 10 to 6.6 × 20 ft to "
              "12 kW. Every model is in the table below with its working area, power and speed, then each family with its full specification, "
              "photos and brochure. Every machine comes with a CSA-approved panel, chiller and nesting software, installed, trained and supported "
              "from Mississauga, ON, Canada. For a machine that cuts while you load, see the enclosed lasers; for heavy plate the plate lasers.",
        points=["Premium: Smart open-type 3 – 6 kW, 5 × 10 to 6.6 × 20 ft; Smart semi-closed single tables 8.2 × 20 to 13 × 82 ft, 3 – 40 kW",
                "Value: ULF open lasers 10 × 5 to 85 × 10.5 ft, 1.5 – 60 kW; NP series 5 × 10 to 6.6 × 20 ft, 3 – 12 kW",
                "Loaded from any side; partial enclosures and fume extraction under the table; towers for the semi-closed machines"],
        hero="vn-ulf-1", minis=["dn-smart-1", "sf-np-1"],
        groups=[("ls-premium-open", "Smart open-type fiber lasers · premium line", "The lowest-priced Dener laser: 3 or 6 kW, 5 × 10 to 6.6 × 20 ft, loaded from any side."),
                ("ls-premium-semi", "Smart semi-closed fiber lasers · premium line", "Very large single tables for long plate — 8.2 × 20 to 13 × 82 ft — from the same Turkish factory."),
                ("ls-value-ulf", "ULF open-type fiber lasers · value line", "NovoTech's own open laser in sixteen sizes, 10 × 5 to 85 × 10.5 ft, 1.5 to 60 kW."),
                ("ls-value-np", "NP open-type lasers · value line", "Single-table machines 5 × 10 to 6.6 × 20 ft, 3 to 12 kW — the entry laser.")],
        faq=[{"q": "Open-type or enclosed — which should I buy?",
              "a": "Open-type when the budget comes first, when sheets are loaded by forklift or crane from the side, or when the plate is longer than any exchange table: the machine stops while you change the sheet, which is fine for a few sheets an hour. Enclosed when you cut all day: the exchange table or pallet changer keeps the laser cutting while you load, and the cabin keeps fumes and the beam inside. Many shops start with an open-type laser and add an enclosed one later."},
             {"q": "Premium line or value line?",
              "a": "The premium Smart open and semi-closed lasers are built by Dener in Turkey with Precitec heads and IPG / nLIGHT sources and Dener Canada parts in Mississauga, ON, Canada. NovoTech's value-line ULF and the NP series are built in China with their own or Raycus sources, in more sizes — to 85 ft and 60 kW — at a lower price; NovoTech stocks the parts and does the service. Same cut quality at the same power; the premium machine lasts longer at high duty."},
             faq("novotech-fiber-lasers", "ULF-G or ULF-E?")[0],
             POWER_FAQ, TABLE_FAQ, GAS_FAQ, SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "press-brake.html", "label": "Press brakes"},
                 {"href": "cnc-plasma-table.html", "label": "CNC plasma tables"}, {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring after laser cutting"}],
    ),
    "large-format-plate-laser": dict(
        title="Large-Format Plate Lasers for Sale in Canada — Ground-Rail & Gantry Lasers to 10 × 164 ft, 6–60 kW | NovoTech",
        meta="Large-format fiber plate lasers sold, installed and supported in Canada: ground-rail lasers cutting 42.7 or 85.3 ft × 14.8 ft beds and gantry plate lasers to 10 × 164 ft with ±45° bevel heads and oxy-fuel, 6 to 60 kW. Every model in one table.",
        h1="Large-format plate lasers — ground-rail and gantry machines to 10 × 164 ft, 6 to 60 kW",
        intro="A large-format plate laser cuts heavy plate on a bed too long and too heavy for a cabinet machine: the gantry runs on ground rails "
              "or a long frame, the plate lies on a fixed bed loaded by crane, and the high-power source — 6 to 60 kW — cuts 1-1/2″ and beyond, "
              "with ±45° bevel heads for weld preparation and an oxy-fuel torch for the thickest plate. NovoTech sells two families in Canada, "
              "both on this page and both from the value line: the ULG ground-rail lasers with 42.7 or 85.3 ft beds up to 14.8 ft wide and 12 to "
              "60 kW, and the R / TX gantry plate lasers from 10 × 20 to 10 × 164 ft with 6 to 60 kW and bevel cutting. Every model is in the "
              "table below with its working area, power and speed, then each family with its full specification, photos and brochure. Every machine "
              "comes with a CSA-approved panel, chiller and nesting software, installed, trained and supported from Mississauga, ON, Canada. For "
              "sheet work on an exchange table see the enclosed lasers; for a single table to 85 ft the open-type lasers.",
        points=["ULG ground-rail lasers: 42.7 or 85.3 ft beds × up to 14.8 ft, 12 – 60 kW — plate loaded by crane, cut in sections",
                "R / TX gantry plate lasers: 10 × 20 to 10 × 164 ft, 6 – 60 kW, ±45° bevel heads, oxy-fuel option",
                "For shipyards, structural steel, heavy equipment and plate service centres — 1-1/2″ and beyond"],
        hero="vn-ulg-1", minis=["sf-r-1", "sf-tx-1"],
        groups=[("ls-value-ulg", "ULG ground-rail plate lasers · value line", "NovoTech's own ground-rail laser: 42.7 or 85.3 ft × up to 14.8 ft, 12 to 60 kW."),
                ("ls-value-r", "R / TX gantry plate lasers · value line", "Ultra-large plate lasers 10 × 20 to 10 × 164 ft, 6 – 60 kW, with ±45° bevel and oxy-fuel.")],
        faq=[faq("novotech-fiber-lasers", "When does a ground-rail laser make sense?")[0],
             faq("senfeng-fiber-lasers", "Plate gantries, bevels and oxy-fuel?")[0],
             POWER_FAQ, GAS_FAQ, SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "cnc-plasma-table.html", "label": "CNC plasma tables"}, {"href": "plate-beveler.html", "label": "Plate bevelers"},
                 {"href": "plate-rollers.html", "label": "Plate rollers"}, {"href": "press-brake.html", "label": "Press brakes"}],
    ),
    "sheet-and-tube-laser": dict(
        title="Sheet and Tube Combination Lasers for Sale in Canada — One Machine for Plate and Tube to Ø13.8″ | NovoTech",
        meta="Sheet-and-tube fiber lasers sold, installed and supported in Canada: a sheet laser with a rotary chuck beside the table — ULFT open and ULET enclosed to 85 ft sheet and Ø13.8″ tube, HM series to 8.3 × 20 ft sheet and Ø8.6″ × 20 ft tube, 1.5 to 40 kW. Every model in one table.",
        h1="Sheet and tube combination lasers — one machine for plate and tube to Ø13.8″",
        intro="A sheet-and-tube laser puts a rotary chuck and tube supports beside the cutting table, so the same head cuts flat sheet from the "
              "table and holes, copes and lengths in round, square and rectangular tube from the chuck — one machine, one source and one "
              "footprint for a shop that cuts both. NovoTech sells three families in Canada, all on this page and all from the value line: the "
              "open ULFT and the enclosed ULET, with sheet tables from 10 × 5 to 85 × 10.5 ft and tube to Ø13.8″, 1.5 to 40 kW; and the HM "
              "series with 5 × 10 to 8.3 × 20 ft tables and Ø8.6″ × 20 ft tube, 6 kW and up. Every model is in the table below with its working "
              "area, power and speed, then each family with its full specification, photos and brochure. Every machine comes with a CSA-approved "
              "panel, chiller and nesting software, installed, trained and supported from Mississauga, ON, Canada. For a dedicated tube machine "
              "with bundle loading see the tube laser cutters.",
        points=["ULFT open and ULET enclosed: sheet 10 × 5 to 85 × 10.5 ft (ULET to 41 × 8.5 ft) plus tube to Ø13.8″, 1.5 – 40 kW",
                "HM series: sheet 5 × 10 to 8.3 × 20 ft plus Ø8.6″ × 20 ft tube, from 6 kW",
                "One head, one source, one footprint — tube supports and chuck fold away when cutting sheet"],
        hero="vn-ulft-1", minis=["vn-ulet-1", "sf-hm-1"],
        groups=[("ls-value-ulft", "ULFT open sheet-and-tube lasers · value line", "The open ULF table with a rotary chuck beside it — sheet to 85 ft and tube to Ø13.8″."),
                ("ls-value-ulet", "ULET enclosed sheet-and-tube lasers · value line", "The enclosed ULE with exchange table and a tube chuck — sheet to 41 × 8.5 ft and tube to Ø13.8″."),
                ("ls-value-hm", "HM sheet and tube combination lasers · value line", "5 × 10 to 8.3 × 20 ft sheet plus Ø8.6″ × 20 ft tube, from 6 kW.")],
        faq=[faq("novotech-fiber-lasers", "Sheet and tube on one machine")[0],
             faq("senfeng-fiber-lasers", "What is the HM sheet-and-tube combination?")[0],
             {"q": "Combination laser or a separate tube laser?",
              "a": "A combination laser is the right buy when tube is a part of the work, not all of it: it cuts tube to Ø13.8″ with the same head and source, loaded one bar at a time by hand, and costs far less than two machines. A dedicated tube laser loads from a bundle, supports long bars at both ends, cuts faster and runs unattended — the machine when tube is the main product. The tube laser cutters have their own page."},
             POWER_FAQ, GAS_FAQ, SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "pipe-notcher.html", "label": "Tube notchers"},
                 {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "press-brake.html", "label": "Press brakes"}],
    ),
    "3d-laser-and-coil-fed-line": dict(
        title="3D Laser Cells & Coil-Fed Laser Cutting Lines for Sale in Canada, 1.5–80 kW | NovoTech",
        meta="Five-axis 3D fiber lasers and robot laser cells for formed parts, and coil-fed laser cutting lines that uncoil, level and cut 0.03″ sheet to 9/16″ plate without handling a sheet — sold, installed and supported in Canada, 1.5 to 80 kW.",
        h1="3D laser cells and coil-fed laser cutting lines",
        intro="Two lasers for work a flat-bed machine cannot do. A 3D laser cuts formed parts — stamped, drawn or bent — with a five-axis head "
              "on a gantry or a robot that follows the surface, trimming edges and cutting holes after forming. A coil-fed laser line uncoils, "
              "levels and feeds strip straight into the laser, so blanks are cut without a sheet ever being handled, stacked or scrapped at the "
              "edges — the line for high-volume parts. NovoTech sells both in Canada, on this page and from the value line: the five-axis SF3015TD "
              "and RC robot cells from 1.5 to 20 kW, and coil-fed lines for 0.03″ sheet to 9/16″ plate with 1.5 to 80 kW. Every model is in the "
              "table below with its working area, power and speed, then each family with its full specification, photos and brochure. Every "
              "machine comes with a CSA-approved panel, chiller and software, installed, trained and supported from Mississauga, ON, Canada.",
        points=["3D: five-axis SF3015TD gantry laser and RC robot cells, 1.5 – 20 kW — trimming and cutting formed parts",
                "Coil-fed lines: uncoiler, leveller, feeder and laser in one line, 0.03″ sheet to 9/16″ plate, 1.5 – 80 kW",
                "Part sorting, stacking and automation options; the lines for automotive, appliance, enclosure and HVAC volume"],
        hero="sf-3d-1", minis=["sf-coil-1", "sf-3d-2"],
        groups=[("ls-value-3d", "3D laser cutting cells · value line", "Five-axis gantry and robot cells for formed parts, 1.5 to 20 kW."),
                ("ls-value-coil", "Coil-fed laser cutting lines · value line", "Uncoil, level and cut in one line — 0.03″ sheet to 9/16″ plate, 1.5 to 80 kW.")],
        faq=[faq("senfeng-fiber-lasers", "When does a coil-fed line pay off?")[0],
             {"q": "Gantry five-axis or robot cell?",
              "a": "A five-axis gantry (SF3015TD) carries the head over a fixed table with the accuracy of a flat-bed laser — for larger formed parts and tight tolerances. A robot cell (RC) carries the head on a six-axis robot around a fixture — more reach around a deep part, a smaller footprint, and the cell can also weld; it is the usual choice for automotive and appliance trimming. Both are programmed offline from the 3D model."},
             POWER_FAQ, GAS_FAQ, SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "enclosed-fiber-laser.html", "label": "Enclosed fiber lasers"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"},
                 {"href": "press-brake.html", "label": "Press brakes"}],
    ),
}

TUBE = {
    "tube-laser-cutter": dict(
        title="Tube Laser Cutters for Sale in Canada — Two- & Three-Chuck, Ø0.3″ to 14″, 20–39 ft Bars | NovoTech",
        meta="Tube laser cutting machines sold, installed and supported in Canada: two- and three-chuck lasers for round, square and rectangular tube Ø0.3″ to 14″ on 20 to 39 ft bars, 1.5 to 40 kW, bundle loaders and ±45° bevel heads — premium E-FTL made in Turkey, value-line ULT, T, PLUS and GT. Every model in one table.",
        h1="Tube laser cutters — two- and three-chuck, Ø0.3″ to 14″, 20 to 39 ft bars, 1.5 to 40 kW",
        intro="A tube laser cutter holds the bar in two chucks — three on the zero-tail versions — turns and feeds it under the head and cuts "
              "lengths, holes, copes, slots and notches from the 3D model in one pass, with no saw, drill, notcher or layout; the bundle loader "
              "feeds the next bar. For tube to Ø14″ it is the machine most shops need. NovoTech sells two lines in Canada, both on this page: "
              "the premium Dener E-FTL made in Turkey, with 1 G servo chucks for Ø0.3″ to 13.8″ at 394 ft/min and ±0.05 mm, 3 to 20 kW; and the "
              "value line — NovoTech's own ULT with two or three pneumatic chucks for Ø0.4″ to 14.2″ on 20, 29.5 or 39 ft bars with 1.5 to 40 kW, "
              "the two-chuck T series from Ø0.5″ and 1.5 kW, and the high-speed PLUS and ±45° bevel-cutting GPLUS / GT. Every model is in the "
              "table below with its tube range, power, speed and bar length, then each family with its full specification, photos and brochure. "
              "Every machine comes with a CSA-approved panel, chiller and tube nesting software, installed, trained and supported from "
              "Mississauga, ON, Canada. For beams and pipe to Ø25″ and 49 ft see the heavy-duty tube lasers.",
        points=["Premium E-FTL: Ø0.3″ – 13.8″, 1 G servo chucks, 394 ft/min, ±0.05 mm, 3 – 20 kW, bars to 39 ft",
                "Value ULT: two or three chucks, Ø0.4″ – 14.2″, square to 13.8″, 20 – 39 ft bars to 2,205 lb, 1.5 – 40 kW; T series from Ø0.5″ and 1.5 kW",
                "PLUS high-speed and GPLUS / GT ±45° bevel lasers Ø0.5″ – 14″; bundle loaders, following supports and unloaders on every machine"],
        hero="dn-tube-2", minis=["vn-ult-1", "sf-t-1"],
        groups=[("lt-premium-eftl", "E-FTL tube lasers · premium line", "Dener's tube laser with 1 G servo chucks — Ø0.3″ to 13.8″, 3 to 20 kW, ±0.05 mm."),
                ("lt-value-ult", "ULT tube and pipe lasers · value line", "NovoTech's own two- and three-chuck tube lasers, Ø0.4″ to 14.2″, 20 – 39 ft bars, 1.5 to 40 kW."),
                ("lt-value-t", "T series two-chuck tube lasers · value line", "The entry tube laser from Ø0.5″ and 1.5 kW, 20 – 39 ft bars."),
                ("lt-value-plus", "PLUS high-speed and GT bevel-cutting tube lasers · value line", "Faster chucks and ±45° bevel cutting for weld preparation, Ø0.5″ to 14″.")],
        faq=[faq("tube-laser-cutting-machine", "What can a tube laser cut?")[0],
             faq("novotech-tube-lasers", "Two chucks or three?")[0],
             {"q": "Premium line or value line?",
              "a": "The premium E-FTL is built by Dener in Turkey with 1 G servo chucks, Precitec heads and ±0.05 mm, with Dener Canada parts in Mississauga, ON, Canada — for the shop that runs the tube laser all day. NovoTech's value-line ULT and the T / PLUS / GT are built in China with pneumatic chucks, in more sizes and powers at a lower price; NovoTech stocks the parts and does the service. The premium machine is faster between parts and holds tighter tolerance at high duty."},
             faq("dener-tube-lasers", "Which chuck size?")[0],
             faq("tube-laser-cutting-machine", "How is the tube loaded?")[0],
             faq("dener-tube-lasers", "Can it cut bevels and weld preparations?")[0],
             faq("tube-laser-cutting-machine", "What about software?")[0],
             faq("tube-laser-cutting-machine", "Floor space and power?")[0],
             VOLT_FAQ_GENERIC],
        related=[{"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"},
                 {"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "band-saw.html", "label": "Band saws"}],
    ),
    "heavy-duty-tube-laser": dict(
        title="Heavy-Duty Tube & Profile Lasers for Sale in Canada — Three & Four Chucks, to Ø25″ and 49 ft | NovoTech",
        meta="Heavy-duty tube laser cutting machines sold, installed and supported in Canada: three- and four-chuck lasers for structural tube, pipe, beams and profiles to Ø25″, bars to 49 ft and 6,600 lb, zero tailing, 3 to 40 kW — premium FTL made in Turkey, value-line NT / ST / HT and the H-beam profile line. Every model in one table.",
        h1="Heavy-duty tube and profile lasers — three and four chucks, to Ø25″ and 49 ft",
        intro="A heavy-duty tube laser carries beams, pipe and heavy profiles that a two-chuck machine cannot: three or four chucks hold a bar of "
              "up to 6,600 lb and 49 ft at both ends and in the middle, feed it through the cut without the tail dropping, and cut copes, holes "
              "and bevels in structural tube to Ø25″ straight from the steel-detailing model. NovoTech sells two lines in Canada, both on this "
              "page: the premium Dener FTL made in Turkey, for Ø0.6″ to 25.2″ and 12 m bars of 2,600 kg, 3 to 20 kW; and the value line — the "
              "zero-tailing NT and the three- and four-chuck ST / HT machines to Ø25″, 6,600 lb and 49 ft, plus the SF1500CH H-beam profile line. "
              "Every model is in the table below with its tube range, power, speed and bar length, then each family with its full specification, "
              "photos and brochure. Every machine comes with a CSA-approved panel, chiller and tube nesting software, installed, trained and "
              "supported from Mississauga, ON, Canada. For tube to Ø14″ see the tube laser cutters.",
        points=["Premium FTL: Ø0.6″ – 25.2″, bars to 39.4 ft and 5,732 lb, 3 – 20 kW, 1 G servo chucks, following supports",
                "Value NT / ST / HT: three and four chucks, zero tailing, to Ø25″, 6,600 lb and 49 ft, 3 – 40 kW; SF1500CH H-beam profile line",
                "Bundle loaders for heavy bars, ±45° bevel heads, STEP / IGES import from steel-detailing software"],
        hero="dn-tube-6", minis=["sf-nt-1", "sf-st-1"],
        groups=[("lt-premium-ftl", "FTL heavy tube lasers · premium line", "Dener's heavy machine for structural tube, pipe and beams — Ø0.6″ to 25.2″, 12 m bars of 2,600 kg."),
                ("lt-value-heavy", "NT, ST and HT three- and four-chuck tube lasers · value line", "Zero-tailing and heavy-bar machines to Ø25″, 6,600 lb and 49 ft, and the H-beam profile line.")],
        faq=[faq("senfeng-tube-lasers", "When do I need three or four chucks")[0],
             faq("senfeng-tube-lasers", "What is zero-tailing")[0],
             faq("dener-tube-lasers", "E-FTL or FTL?")[0],
             faq("senfeng-tube-lasers", "How is the tube loaded and unloaded?")[0],
             faq("dener-tube-lasers", "Can it cut bevels and weld preparations?")[0],
             faq("tube-laser-cutting-machine", "What about software?")[0],
             faq("tube-laser-cutting-machine", "Floor space and power?")[0],
             VOLT_FAQ_GENERIC],
        related=[{"href": "tube-laser-cutter.html", "label": "Tube laser cutters"}, {"href": "band-saw.html", "label": "Band saws"},
                 {"href": "plate-beveler.html", "label": "Plate bevelers"}, {"href": "large-format-plate-laser.html", "label": "Plate lasers"}],
    ),
}

VIDEO_DENER = {k: COPY["dener-fiber-lasers"].get(k) for k in ("intro_video", "intro_video_heading", "intro_video_text")}
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}


def build():
    manifest = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))
    for kind, pages, set_name, rng in (("sheet", SHEET, "sheet-lasers", SHEET_RANGE), ("tube", TUBE, "tube-lasers", TUBE_RANGE)):
        fs = json.load(open(os.path.join(ROOT, "content", "families", f"{set_name}.json"), encoding="utf-8"))
        fams = {fid: dict(fs["families"][fid], id=fid) for fid in fs["order"]}
        for slug, page in pages.items():
            members = [dict(fams[fid], group=g) for fid, g in LN.PAGES[kind][slug]]
            pdfs, seen = [], set()
            for f in members:
                pd = f.get("pdf")
                if pd and pd["file"] not in seen:
                    seen.add(pd["file"]); pdfs.append(pd)
            n = sum(len(f["specs"]["models"]) for f in members)
            for key in [page["hero"]] + page["minis"]:
                if key not in manifest:
                    raise SystemExit(f"{slug}: image key not in manifest: {key}")
            premium = any(f.get("brand") == "dener" for f in members)
            video = VIDEO_DENER if premium and VIDEO_DENER["intro_video"] and VIDEO_DENER["intro_video"]["thumb"] in manifest else NO_VIDEO
            p = {k: page[k] for k in ("title", "meta", "h1", "intro", "points", "hero", "minis", "groups", "faq")}
            p["related_pages"] = page["related"]
            p["related_title"] = "More laser and cutting machinery from NovoTech"
            write_category(slug, p, members, set_name, LN.SECTIONS[kind]["section"], hub=LN.hub(kind), siblings=LN.siblings(kind),
                           extra={"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **video,
                                  "nav_label": next(nav for s, _, _, _, nav, _ in LN.SECTIONS[kind]["subpages"] if s == slug),
                                  "catalogue_pdf": None, "catalogue_pdfs": pdfs, **rng,
                                  "range_lead": f"Every model on this page in one table — {n} machines. Each row links to the full specification below.",
                                  "range_caption": f"{page['h1'].split(' — ')[0]} supplied by NovoTech", "range_title": "Every model at a glance"})
            print(f"{slug}: {len(members)} families, {n} models, {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
