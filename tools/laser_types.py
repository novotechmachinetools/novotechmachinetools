#!/usr/bin/env python3
"""The laser pages, one per kind of machine (tools/laser_nav.py): five sheet-laser pages under the sheet-laser hub, and ONE
tube-laser page with no hub (the owner, Nov 1 2026).  Each holds every family of that kind NovoTech sells, premium and value lines as sections, with the spec
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

BRAND_LINE = ("The premium lasers are built by Dener Makina in Kayseri, Turkey; NovoTech's own value line is built in "
              "China to our specification; the Senfeng value line in Jinan, China (CE / FDA / ETL certified and CSA approved). All sold, installed and supported in Canada by NovoTech.")
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

# the small names under the hero pictures — what the machine is, not its model code (the owner, Nov 1 2026)

SHEET = {
    "fiber-laser-cutting-machine": dict(
        title="Fiber Laser Cutting Machines for Sale in Canada — Shuttle Table & Pallet Changer, 1.5–80 kW | NovoTech",
        meta="Fiber laser cutting machines sold, installed and supported in Canada: shuttle table or pallet changer, laser-safe cabin, 4 × 4 ft compact machines to 8.5 × 41 ft, 1.5 to 80 kW — premium GFL and Smart made in Turkey, value-line ULE, Senfeng H series, NP and compact lasers.",
        h1="Fiber laser cutting machines, 4 × 4 ft to 8.5 × 41 ft, 1.5 to 80 kW",
        intro="A fiber laser cutting machine cuts inside a laser-safe cabin with fume extraction, and its shuttle table or pallet changer loads "
              "the next sheet while the first is being cut — the production laser that keeps cutting while the operator unloads, and the kind "
              "most shops buy from 5 × 10 ft up. NovoTech sells two lines in Canada, both on this page: the premium Dener lasers made in Turkey "
              "— the GFL with a space-frame gantry rated for 1.5 G and a shuttle table in 5 × 10 to 6.6 × 20 ft, 3 to 40 kW, and the Smart "
              "with a shuttle table in six sizes to 8.5 × 41 ft; and the value line — NovoTech's own ULE with a 15-second shuttle "
              "table to 41 ft, the Senfeng H series with pallet changer from 5 × 10 to 8.3 × 40 ft and 1.5 to 80 kW, the NP single-table "
              "lasers with a cover on the gantry, and compact lasers of 4 × 4 and 5 × 10 ft from 1.5 kW. Each family below has its full specification table, photos and brochure. Every machine "
              "comes with a CSA-approved panel, chiller and nesting software, installed, trained and supported from Mississauga, ON, "
              "Canada. For long and heavy plate see the large-format plate lasers.",
        points=["Premium: GFL 1.5 G with shuttle table, 5 × 10 to 6.6 × 20 ft, 3 – 40 kW; Smart with shuttle table, six sizes to 8.5 × 41 ft",
                "Value: ULE with 15 s shuttle table 10 × 5 to 41 × 8.5 ft, 3 – 40 kW; Senfeng H series with pallet changer to 8.3 × 40 ft and 80 kW",
                "Senfeng compact G, N and NP 5 × 10 ft lasers from 1.5 kW, NP single tables with a gantry cover to 6.6 × 20 ft, and the 4 × 4 ft SF1313G; towers and storage"],
        hero="dn-gfl-1", minis=["vn-ule-1", "sf-h-1"],
        groups=[("ls-premium-gfl", "GFL production fiber lasers · premium line", "Dener's premium sheet laser: 1.5 G, shuttle table, 3 – 40 kW — built for a job shop that cuts all day."),
                ("ls-premium-closed", "Smart fiber lasers with shuttle table · premium line", "The economy line from the same Turkish factory: a shuttle table and 1 G in six sizes to 8.5 × 41 ft."),
                ("ls-value-ule", "ULE fiber lasers with shuttle table · value line", "NovoTech's own laser with a 15-second shuttle table, 10 × 5 to 41 × 8.5 ft, 3 – 40 kW."),
                ("ls-value-h", "H series lasers with pallet changer · value line", "The widest range: 5 × 10 to 8.3 × 40 ft and 1.5 to 80 kW, with towers and storage."),
                ("ls-value-compact", "Compact single-table lasers G, N and NP · value line", "Fully enclosed 5 × 10 ft single tables from 1.5 kW — the laser for the small shop."),
                ("ls-value-np", "NP lasers with gantry cover · value line", "Single tables 5 × 10 to 6.6 × 20 ft, 3 to 12 kW: the cover travels with the gantry, the table stays open for loading."),
                ("ls-value-1313g", "SF1313G 4 × 4 ft compact laser · value line", "The smallest enclosed laser, 1.5 to 3 kW, for small, thin parts.")],
        faq=[{"q": "Shuttle table or pallet changer — what is the difference?",
              "a": "Both load the next sheet while the first is cut. A shuttle table (GFL, Smart, ULE, compact) has two tables that swap places in 15 – 30 seconds, one in the cabin cutting and one outside being loaded. A pallet changer (Senfeng H series) lifts the pallet with the cut sheet out of the cabin and slides the loaded pallet in, which is the arrangement a loading tower and sheet storage connect to for lights-out production. For a few sheets an hour the shuttle table is enough; for automation, the pallet changer. Some makers call the shuttle table an exchange table, a double table or a dual table — it is the same thing."},
             {"q": "Premium line or value line?",
              "a": "The premium GFL and Smart are built by Dener in Turkey on stress-relieved frames — the GFL rated for 1.5 G — with Boji BLT autofocus heads and Raycus sources (Precitec and IPG on request), longer life at high duty and parts stocked in Canada: the machines for two shifts a day. NovoTech's value-line ULE and the Senfeng H series, NP and compact lasers are built in China with their own or Raycus sources in a wider range — 4 × 4 ft machines, 60 – 80 kW — at a lower price; NovoTech stocks the parts and does the service. Same cut quality at the same power."},
             POWER_FAQ, TABLE_FAQ, AUTO_FAQ, GAS_FAQ,
             faq("dener-fiber-lasers", "What is in a Dener laser as standard?")[0],
             SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "press-brake.html", "label": "Press brakes"},
                 {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring after laser cutting"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"}],
    ),
    "sheet-and-tube-laser": dict(
        title="Sheet and Tube Combination Lasers for Sale in Canada — One Machine for Sheet and Tube to Ø13.8″ | NovoTech",
        meta="Sheet-and-tube fiber lasers sold, installed and supported in Canada: a sheet laser with a rotary chuck beside the table — the ULET with shuttle table to 41 × 8.5 ft sheet and Ø13.8″ tube, and the HM series to 8.3 × 20 ft sheet and Ø8.6″ × 20 ft tube, 1.5 to 40 kW.",
        h1="Sheet and tube combination lasers — one machine for sheet and tube to Ø13.8″",
        intro="A sheet-and-tube laser puts a rotary chuck and tube supports beside the cutting table, so the same head cuts flat sheet from the "
              "table and holes, copes and lengths in round, square and rectangular tube from the chuck — one machine, one source and one "
              "footprint for a shop that cuts both. NovoTech sells two families in Canada, both on this page and both from the value line: "
              "the ULET with its shuttle table for sheet from 10 × 5 to 41 × 8.5 ft and tube to Ø13.8″, 1.5 to 40 kW; and the Senfeng HM "
              "series with a dual exchange table for 5 × 10 to 8.3 × 20 ft sheet and Ø8.6″ × 20 ft tube, 1.5 to 30 kW. Each family below has its full specification table, photos and brochure. Every machine "
              "comes with a CSA-approved panel, chiller and nesting software, installed, trained and supported from Mississauga, ON, Canada. "
              "For a dedicated tube machine with bundle loading see the tube laser cutters.",
        points=["ULET: sheet 10 × 5 to 41 × 8.5 ft on a shuttle table plus tube to Ø13.8″ and 40 ft, 1.5 – 40 kW",
                "HM series: sheet 5 × 10 to 8.3 × 20 ft on a dual exchange table plus Ø8.6″ × 20 ft tube, 1.5 – 30 kW",
                "One head, one source, one footprint — tube supports and chuck fold away when cutting sheet"],
        hero="sf-hm-1", minis=["vn-ulet-1", "vn-ulet-tube-head"],      # Senfeng large, the ULET small (the owner, Nov 1 2026)
        minis_same_h=True,      # the chuck close-up no bigger than the ULET beside it (the owner, Nov 1 2026)
        groups=[("ls-value-ulet", "ULET sheet-and-tube lasers with shuttle table · value line", "The ULE with shuttle table and a tube chuck — sheet to 41 × 8.5 ft and tube to Ø13.8″."),
                ("ls-value-hm", "HM sheet and tube combination lasers · value line", "5 × 10 to 8.3 × 20 ft sheet plus Ø8.6″ × 20 ft tube, 1.5 to 30 kW.")],
        faq=[faq("novotech-fiber-lasers", "Sheet and tube on one machine")[0],
             faq("senfeng-fiber-lasers", "What is the HM sheet-and-tube combination?")[0],
             {"q": "Combination laser or a separate tube laser?",
              "a": "A combination laser is the right buy when tube is a part of the work, not all of it: it cuts tube to Ø13.8″ with the same head and source, loaded one bar at a time by hand, and costs far less than two machines. A dedicated tube laser loads from a bundle, supports long bars at both ends, cuts faster and runs unattended — the machine when tube is the main product. The tube laser cutters have their own page."},
             POWER_FAQ, GAS_FAQ, SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "pipe-notcher.html", "label": "Tube notchers"},
                 {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "press-brake.html", "label": "Press brakes"}],
    ),
    "large-format-plate-laser": dict(
        title="Large-Format Plate Lasers for Sale in Canada — Semi-Closed, Ground-Rail & Gantry Lasers to 10 × 164 ft, 3–60 kW | NovoTech",
        meta="Large-format fiber plate lasers sold, installed and supported in Canada: Dener Smart semi-closed single tables to 13 × 82 ft, ground-rail lasers cutting 42.7 or 85.3 ft × 14.8 ft beds and gantry plate lasers to 10 × 164 ft with ±45° bevel heads and oxy-fuel, 3 to 60 kW.",
        h1="Large-format plate lasers — semi-closed, ground-rail and gantry machines to 10 × 164 ft, 3 to 60 kW",
        intro="A large-format plate laser cuts long and heavy plate on a bed too long and too heavy for a cabinet machine: the plate lies on a "
              "fixed single table loaded by crane or forklift from the side, the gantry runs over it on a long frame or on rails in the floor, "
              "and the cover that keeps the beam and the spatter in travels with the gantry — semi-closed. High-power sources of up to 60 kW "
              "cut 1-1/2″ and beyond, with ±45° bevel heads for weld preparation and an oxy-fuel torch for the thickest plate. NovoTech sells "
              "two lines in Canada, both on this page: the premium Dener Smart semi-closed lasers made in Turkey, single tables from 8.2 × 20 "
              "to 13 × 82 ft with 3 to 40 kW; and the value line — the ULG ground-rail lasers with 42.7 or 85.3 ft beds up to 14.8 ft wide "
              "and 12 to 60 kW, and the R / TX gantry plate lasers from 10 × 20 to 10 × 164 ft with 6 to 60 kW and bevel cutting. Each family below has its full specification table, photos and brochure. Every machine comes with a CSA-approved panel, chiller and nesting software, installed, trained and supported from "
              "Mississauga, ON, Canada. For sheet work on a shuttle table see the fiber laser cutting machines.",
        points=["Premium: Smart semi-closed single tables 8.2 × 20 to 13 × 82 ft, 3 – 40 kW, ±0.01 mm — the cabin travels with the gantry",
                "Value: ULG ground-rail lasers, 42.7 or 85.3 ft beds × up to 14.8 ft, 12 – 60 kW; R / TX gantry plate lasers 10 × 20 to 10 × 164 ft, 6 – 60 kW, ±45° bevel, oxy-fuel",
                "For shipyards, structural steel, heavy equipment and plate service centres — 1-1/2″ and beyond"],
        hero="vn-ulg-1", minis=["dn-smart-semi-1", "sf-r-1"],
        groups=[("ls-premium-semi", "Smart semi-closed fiber lasers · premium line", "Long single tables for plate — 8.2 × 20 to 13 × 82 ft — with the cabin on the gantry, from the same Turkish factory."),
                ("ls-value-ulg", "ULG ground-rail plate lasers · value line", "NovoTech's own ground-rail laser: 42.7 or 85.3 ft × up to 14.8 ft, 12 to 60 kW."),
                ("ls-value-r", "R / TX gantry plate lasers · value line", "Ultra-large plate lasers 10 × 20 to 10 × 164 ft, 6 – 60 kW, with ±45° bevel and oxy-fuel.")],
        faq=[{"q": "Semi-closed — what does it mean?",
              "a": "The table stays open and the cover rides on the gantry: the laser-safe cabin or hood moves with the cutting head over the plate, so the beam, the spatter and most of the fumes stay under it while the crane or forklift can reach the table from any side. It is the arrangement for plate too long or too heavy for a shuttle table; the fume extraction runs in zones under the slats along the whole bed."},
             faq("novotech-fiber-lasers", "When does a ground-rail laser make sense?")[0],
             faq("senfeng-fiber-lasers", "Plate gantries, bevels and oxy-fuel?")[0],
             POWER_FAQ, GAS_FAQ, SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "cnc-plasma-table.html", "label": "CNC plasma tables"}, {"href": "plate-beveler.html", "label": "Plate bevelers"},
                 {"href": "plate-rollers.html", "label": "Plate rollers"}, {"href": "press-brake.html", "label": "Press brakes"}],
    ),
    "3d-laser-cutting-machine": dict(
        title="3D Laser Cutting Machines for Sale in Canada — Five-Axis SF3015TD, 3–20 kW | NovoTech",
        meta="Five-axis 3D fiber laser that trims and cuts formed, stamped, drawn and bent parts and pipe fittings — the SF3015TD with endless C and ±135° A rotation over a 5 × 10 ft envelope, 3 to 20 kW, sold, installed and supported in Canada.",
        h1="3D laser cutting machines — five-axis SF3015TD, 5 × 10 ft, 3 to 20 kW",
        intro="A 3D laser cuts formed parts — stamped, drawn, hot-stamped or bent — with a five-axis head that follows the surface: it trims "
              "edges and cuts holes and slots after forming, where a flat-bed laser cannot reach and a trimming die would cost more than the "
              "run. NovoTech sells Senfeng's five-axis SF3015TD in Canada, from the value line: a 3 to 20 kW head with endless C rotation and "
              "±135° A swing over a 5 × 10 ft envelope, on a marble base, with a 180° dual-station rotary table and a fully enclosed cabin. "
              "The family below has its full specification table, photos and brochure. Every machine comes with a CSA-approved panel, chiller and "
              "offline programming software, installed, trained and supported from Mississauga, ON, Canada.",
        points=["SF3015TD five-axis laser: 5 × 10 ft envelope, 27.6″ Z, endless C and ±135° A, 328 ft/min, 3 – 20 kW",
                "Marble base and marble guide rails for accuracy; 180° dual-station rotary table or a servo shuttle table",
                "Offline programming from the 3D model; fully enclosed cabin with interlocked doors and a light curtain"],
        hero="sf-3d-1", minis=["sf-3d-3", "sf-3d-cut"],
        groups=[("ls-value-3d", "SF3015TD five-axis 3D laser · value line", "The five-axis laser for formed parts, 5 × 10 ft, 3 to 20 kW.")],
        faq=[{"q": "What parts suit a five-axis 3D laser?",
              "a": "Formed parts that a flat-bed laser cannot reach: hot-stamped and cold-pressed automotive parts such as pillars, door rings and bumper beams, drawn covers and housings, pipe fittings and exhaust parts, and stainless metalwork such as pots and trays. The SF3015TD trims edges and cuts holes and slots after forming in place of trimming and piercing dies; it is programmed offline from the 3D model, and its 180° dual-station table loads one part while the other is cut."},
             POWER_FAQ, GAS_FAQ, SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "fiber-laser-cutting-machine.html", "label": "Fiber laser cutting machines"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"},
                 {"href": "press-brake.html", "label": "Press brakes"}],
    ),
    "coil-fed-laser-cutting-line": dict(
        title="Coil-Fed Laser Cutting Lines for Sale in Canada — Thin, Aluminum and 9/16″ Coil, TOP Automated Line, 1.5–80 kW | NovoTech",
        meta="Five Senfeng coil-fed fiber laser lines sold, installed and supported in Canada: the SF1503CH for thin coil, the open-style SF15015C, the TOP line from coil to bent and welded parts, the SF1503CLH for aluminum coil and the SF2012CH for 5/16 – 9/16″ coil to 80 kW.",
        h1="Coil-fed laser cutting lines — uncoil, level and cut coil to 9/16″ plate, 1.5 to 80 kW",
        intro="A coil-fed laser line uncoils, levels and feeds strip straight into the laser, so blanks are cut without a sheet ever being "
              "handled, stacked or scrapped at the edges and with no limit on part length — and coil costs less than cut-to-length sheet. "
              "NovoTech sells five Senfeng lines in Canada, all on this page and from the value line: the SF1503CH for thin coil to 0.118″ "
              "on a 5 × 10 ft laser with 3 to 6 kW; the open-style SF15015C, the affordable line for 0.031 to 0.047″ coil; the TOP line "
              "that takes coil to cut, bent, welded and stacked parts; the SF1503CLH with a straightener made for aluminum coil; and the "
              "SF2012CH that levels and cuts 0.314 to 0.551″ coil from 22-ton coils with 12 to 80 kW. Each line below has its full "
              "specification table and photos. Every line comes with a CSA-approved panel, chiller and software, installed, trained and "
              "supported from Mississauga, ON, Canada.",
        points=["SF1503CH: thin coil 0.031 – 0.118″ to 16.5 US tons, 5 × 10 ft laser, 3 – 6 kW",
                "SF15015C: open-style line for 0.031 – 0.047″ coil in half the floor space, 1.5 – 3 kW",
                "TOP line: coil, laser, robot sorting, panel bending and welding in one unmanned line",
                "SF1503CLH: aluminum coil 0.023 – 0.118″ with a straightener built for aluminum, 6 kW",
                "SF2012CH: 5/16 – 9/16″ coil to 22 US tons on a 13 × 6.6 ft laser, 12 – 80 kW"],
        hero="sf-coil-1", minis=["sf-coil-2", "sf-coil-top"],
        groups=[("ls-value-coil", "SF1503CH coil-fed laser for thin coil · value line", "Thin coil 0.031 – 0.118″ to 16.5 US tons, 5 × 10 ft, 3 – 6 kW."),
                ("ls-value-coil-c", "SF15015C open-style thin-sheet coil line · value line", "The affordable line for 0.031 – 0.047″ coil, 1.5 – 3 kW."),
                ("ls-value-top", "TOP series automated metal processing line · value line", "Coil to cut, bent, welded and stacked parts in one line."),
                ("ls-value-clh", "SF1503CLH aluminum coil-fed laser · value line", "Aluminum coil 0.023 – 0.118″ with a straightener built for aluminum, 6 kW."),
                ("ls-value-coil-heavy", "SF2012CH coil-fed line for thick coil · value line", "5/16 – 9/16″ coil to 22 US tons, 13 × 6.6 ft, 12 – 80 kW.")],
        faq=[faq("senfeng-fiber-lasers", "When does a coil-fed line pay off?")[0],
             POWER_FAQ, GAS_FAQ, SITE_FAQ, VOLT_FAQ_GENERIC],
        related=[{"href": "fiber-laser-cutting-machine.html", "label": "Fiber laser cutting machines"}, {"href": "panel-bender.html", "label": "CNC panel benders"},
                 {"href": "press-brake.html", "label": "Press brakes"}],
    ),
}

TUBE = {
    # ONE page for every tube laser — no hub, no standard / heavy-duty split; the tube laser buying guide sits at its foot
    # (content/extra_groups/guide-tube-laser-cutting-machine.json) — the owner, Nov 1 2026.  The former tube-laser-cutter and
    # heavy-duty-tube-laser pages redirect here (src/root/.htaccess).
    "tube-laser-cutting-machine": dict(
        title="Tube Laser Cutting Machines for Sale in Canada — Ø0.3″ to 25.2″, 20 to 40 ft Tubes | NovoTech",
        meta="Every tube and profile laser NovoTech sells in Canada on one page, the series compared side by side: two-chuck, high-speed, bevel-cutting, three-chuck zero-tail and heavy-duty machines for tube to Ø25″ and 40 ft, 1.5 to 40 kW — premium E-FTL and FTL made in Turkey, value-line ULT, T, PLUS, GPLUS / GT, NT and ST — and the three ways to load them.",
        h1="Tube and profile laser cutting machines — Ø0.3″ to 25.2″, 20 to 40 ft tubes, 1.5 to 40 kW",
        intro="A tube laser cuts round, square, rectangular and open profiles to length and cuts the holes, copes, slots and notches in "
              "them in one pass — no saw, no drill, no notcher, no layout — straight from the 3D model. Every tube laser NovoTech sells "
              "in Canada is on this page, and the table below sets the series side by side: how many chucks, what tube, how long and "
              "heavy a bar, how fast, and how it is loaded. Two chucks hold the tube at both ends and leave a short tail on each bar — "
              "the Dener E-FTL made in Turkey, NovoTech's ULT, the Senfeng T series, the high-speed PLUS for small tube in volume and "
              "the GPLUS / GT that cut ±45° bevels. Three chucks cut the last part with zero tail and carry long, heavy tube: the "
              "Dener FTL to Ø25.2″, the ULT three-chuck, the Senfeng NT and the heavy ST to Ø25″ and 6,614 lb. Each machine can be "
              "loaded by hand or crane, or with a semi-automatic or fully automatic loader — explained below. Every machine comes "
              "with a CSA-approved panel, chiller and tube nesting software, a 1-year warranty and installation, training and parts "
              "from Mississauga, ON, Canada.",
        points=["Premium E-FTL Ø0.3″ – 13.8″, 1 G, ±0.05 mm, and premium FTL Ø0.6″ – 25.2″ with three chucks and zero tail, bars to 40 ft",
                "Value ULT Ø0.4″ – 14.2″ with two or three chucks; T series two-chuck Ø0.5″ – 14.1″; PLUS high-speed Ø0.4″ – 9.4″; GPLUS / GT ±45° bevel",
                "Three-chuck NT zero-tail Ø0.7″ – 14.1″ and heavy-duty ST Ø1.9″ – 25.1″, bars to 40 ft and 6,614 lb",
                "Loaded by hand, or with a semi-automatic or fully automatic loader — see the loading options"],
        hero="dn-tube-2", minis=["vn-ult-1", "sf-t-1"],
        groups=[("lt-premium-eftl", "E-FTL tube lasers · premium line", "Dener's fast tube laser, 1 G — Ø0.3″ to 13.8″, 3 to 20 kW, ±0.05 mm."),
                ("lt-premium-ftl", "FTL tube lasers · premium line", "Dener's three-chuck machine for pipe, structural tube and beams — Ø0.6″ to 25.2″, zero tail."),
                ("lt-value-ult", "ULT tube and pipe lasers · value line", "NovoTech's own two- and three-chuck tube lasers, Ø0.4″ to 14.2″, 20 – 40 ft tubes, 1.5 to 40 kW."),
                ("lt-value-t", "T series two-chuck tube lasers · value line", "The first tube laser of most shops: Ø0.5″ to 14″, 20 – 40 ft."),
                ("lt-value-plus", "PLUS high-speed tube lasers · value line", "240 rpm and 492 ft/min for small tube in volume."),
                ("lt-value-gt", "GPLUS / GT bevel-cutting tube lasers · value line", "±45° bevels for weld preparation, Ø0.6″ to 14.1″."),
                ("lt-value-nt", "NT three-chuck zero-tail tube lasers · value line", "The last part cut without a tail, 20 – 40 ft bars."),
                ("lt-value-st", "ST three-chuck heavy-duty tube lasers · value line", "Pipe and large tube to Ø25″ and 6,614 lb.")],
        compare=dict(
            title="Which tube laser? The series side by side",
            lead="The number of chucks decides what is left of each bar and how heavy a tube the machine carries; the chuck size decides the "
                 "largest tube; the loader decides how much of the operator's time each bar takes. Each row opens the machine's section "
                 "with its full specification table.",
            cols=["Machine", "Chucks", "Tube", "Bar length · max. tube weight", "Speed", "Loading", "Best for", ""],
            rows=[["E-FTL · premium", "2 servo chucks; ≥1.4″ (35 mm) tail", "Ø0.3 – 13.8″ (8 – 350 mm)", "23 – 40 ft (7 – 12 m) · to 3,968 lb (1,800 kg)", "394 ft/min (120 m/min), 1 G", "By hand; fully automatic loader optional (semi-automatic on the 120 / 180 chucks)", "Fast cutting of small and medium tube in volume", {"href": "#dn-eftl", "label": "E-FTL"}],
                  ["FTL · premium", "3 chucks; zero tail", "Ø0.6 – 25.2″ (15 – 640 mm)", "20 – 40 ft (6 – 12 m) · to 5,732 lb (2,600 kg)", "262 ft/min (80 m/min), 0.6 G", "By hand or crane; semi-automatic loader optional", "Pipe, structural tube and heavy sections", {"href": "#dn-ftl", "label": "FTL"}],
                  ["ULT · value", "2 pneumatic chucks, or 3 for zero tail", "Ø0.4 – 14.2″ (10 – 360 mm)", "20, 30 or 40 ft · to 2,205 lb (1,000 kg)", "328 ft/min (100 m/min), 1.2 G", "By hand; pneumatic loader or bundle feeding optional", "General fabrication; the three-chuck version where every inch of tube counts", {"href": "#vn-ult", "label": "ULT"}],
                  ["T series · value", "2 pneumatic chucks; short tail", "Ø0.5 – 14.1″", "20 – 40 ft · to 1,102 lb", "to 492 ft/min, 1.5 G", "By hand; semi-automatic or fully automatic loader optional", "The first tube laser of a job shop", {"href": "#sf-t", "label": "T series"}],
                  ["PLUS · value", "2 pneumatic chucks; very short to zero tail", "Ø0.4 – 9.4″", "20 – 23 ft · to 661 lb", "492 ft/min, 240 rpm, 1.5 G", "By hand; semi-automatic or fully automatic loader optional", "Small tube in volume — furniture, fitness, racking, automotive", {"href": "#sf-plus", "label": "PLUS"}],
                  ["GPLUS / GT · value", "2 chucks and a ±45° 3D head", "Ø0.6 – 14.1″", "20 ft · to 1,102 lb", "to 492 ft/min", "By hand; the GT usually with an automatic loader", "Weld preparations, mitres and bevelled ends", {"href": "#sf-gt", "label": "GPLUS / GT"}],
                  ["NT · value", "3 pneumatic chucks; zero tail", "Ø0.7 – 14.1″", "20 – 40 ft · to 1,543 lb", "246 ft/min, 0.8 G", "By hand or crane; semi-automatic or fully automatic loader optional", "Long bars and costly material — no remnant", {"href": "#sf-nt", "label": "NT"}],
                  ["ST · value", "3 heavy chucks", "Ø1.9 – 25.1″", "30 – 40 ft · to 6,614 lb", "to 197 ft/min", "Semi-automatic loading and unloading included; fully automatic optional", "Pipe, large tube and structural sections", {"href": "#sf-st", "label": "ST"}]],
            note="Ranges are for the series; each model's chuck size, bar length and weight are in its specification table. Tail: the piece "
                 "of each bar that a two-chuck machine cannot cut because the rear chuck holds it."),
        loading=dict(
            title="Loading the tube: by hand, semi-automatic or fully automatic",
            lead="Every tube laser on this page can be loaded three ways. The loader does not change what the machine can cut — it decides "
                 "how much of the operator's time each bar takes, and whether the machine keeps cutting while nobody stands at it.",
            cards=[dict(tag="Standard", title="By hand or crane — no loader", image="sf-t-1",
                        text="The operator lifts each tube onto the infeed supports — by hand for light tube, with a hoist or crane for heavy "
                             "bars. The rear chuck pulls it in, the chucks centre and clamp it, the following supports carry it and the machine "
                             "cuts the whole bar on its own; the finished parts drop onto the unloading rack.",
                        items=["Standard on the Senfeng T, PLUS, GPLUS / GT and NT, the NovoTech ULT and the Dener E-FTL and FTL",
                               "The lowest price and the shortest machine", "Any profile the chucks hold — angle, channel and special shapes too",
                               "Right for short runs, mixed jobs and light tube"]),
                   dict(tag="Option", title="Semi-automatic loader", image="sf-load-semi",
                        text="The operator lays a row of tubes on the loader's sloped rack or chains and keeps it filled; the loader separates "
                             "one tube at a time, lifts it to the chuck centre and feeds it in. A tube outside the loader's size or weight is "
                             "still loaded by hand.",
                        items=["Sloped loader: 17 – 20 ft (5.2 – 6.2 m) tubes up to 265 lb (120 kg) — round, square, rectangular and channel",
                               "Dual-arm chain loader: 13 – 20 ft (4 – 6.1 m) tubes up to 529 lb (240 kg) — also angle, channel and I-beam",
                               "Chain loader: 13 – 40 ft (4 – 12 m) tubes and profiles up to 1,543 lb (700 kg)",
                               "Takes special shapes and open profiles that a bundle loader cannot; included on the Senfeng ST"]),
                   dict(tag="Option", title="Fully automatic bundle loader", image="sf-load-auto",
                        text="The crane sets a whole bundle — up to 3 t (6,600 lb) — into the loader; it separates the tubes, aligns each one "
                             "and feeds it to the chuck with no operator, while the unloading system sorts the parts from the scrap. One person "
                             "runs the machine and prepares the next bundle while it cuts, and the machine keeps cutting through breaks.",
                        items=["Fully automatic loader: 11.5 – 20 ft (3.5 – 6.1 m) tubes, 15 – 30 ft (4.5 – 9 m) on the 9 m machines",
                               "Simplified fully automatic loader: the same 3 t bundle on a lighter frame, also for 20 – 40 ft (6 – 12 m) tubes",
                               "Round, square and rectangular tube of standard section, 265 – 573 lb (120 – 260 kg) per tube",
                               "The choice for production runs and two-shift work"])],
            note="Unloading: a 6.6 ft (2 m) unloading rack that sorts scrap from parts is standard on the Senfeng T and PLUS (10 or 13 ft "
                 "optional) and a 10 ft (3 m) unloading system on the NT (20 ft optional). Dener E-FTL: a fully automatic loader is optional "
                 "(the 120 and 180 chucks can also have a semi-automatic one); Dener FTL: a semi-automatic loader is optional; NovoTech ULT: "
                 "a pneumatic loader for tube to Ø8.7″ or a bundle feeding system."),
        faq=[{"q": "Two or three chucks — which should I buy?",
              "a": "By what you cut and what the leftover costs you. Two chucks hold the tube at both ends; the rear chuck has to keep hold "
                   "of the bar, so a short tail of every bar is scrap — fine for mild steel in short and medium runs, and the cheapest "
                   "machine: the Dener E-FTL, the NovoTech ULT and the Senfeng T, PLUS and GPLUS / GT. A third chuck takes over the bar as "
                   "it shortens, so the last part is cut with zero tail, and it supports long, heavy tube so it is cut straight: the "
                   "Dener FTL, the ULT three-chuck, the Senfeng NT and, for pipe and structural tube to Ø25″, the Senfeng ST. On 20 to "
                   "40 ft bars of stainless, aluminum or heavy-wall tube the saved material pays for the third chuck."},
             {"q": "Premium line or value line?",
              "a": "The premium Dener E-FTL and FTL are built in Turkey with servo-driven chucks (1 G on the E-FTL), a Maxphotonics fiber "
                   "source, a BOCI autofocus head and ±0.05 mm repeatability, with parts stocked in Canada — for the shop that runs the "
                   "tube laser all day. NovoTech's value-line ULT and the Senfeng T / PLUS / GT / NT / ST are built in China with "
                   "pneumatic chucks, in a wider range of sizes and powers at a lower price; NovoTech stocks the parts and does the "
                   "service. The premium machine is faster between parts and holds tighter tolerance at high duty."},
             faq("dener-tube-lasers", "E-FTL or FTL?")[0],
             {"q": "What can a tube laser cut?",
              "a": "Round, square, rectangular, oval and open profiles — angle, channel, flat bar — in mild steel, stainless, aluminum, copper and brass, from the chuck's minimum to its maximum size, in wall thicknesses to about 1/2″ (12 kW) or 3/4″ (20 kW). Holes, slots, copes for tube-to-tube joints, tabs and notches for folding, engraving — anything you can draw on the surface of the profile. A 5-axis or 45° bevel head adds weld preparations and mitred corners."},
             {"q": "Do I need an automatic loader?",
              "a": "Not to start: every machine here is loaded by hand or crane as standard, and the loader can usually be added later. A "
                   "semi-automatic loader is worth it once an operator spends more time lifting tube than watching the machine — the "
                   "operator keeps a rack or chain filled and the loader feeds one tube at a time, open profiles and special shapes "
                   "included. A fully automatic bundle loader takes a whole 3 t bundle from the crane and feeds round, square and "
                   "rectangular tube with nobody at the machine — the choice for production runs and two shifts."},
             faq("senfeng-tube-lasers", "What is zero-tailing")[0],
             faq("dener-tube-lasers", "Which chuck size?")[0],
             faq("dener-tube-lasers", "Can it cut bevels and weld preparations?")[0],
             {"q": "What about software?",
              "a": "The CNC imports STEP / IGES solid models of the tube parts, unfolds them onto the profile, nests them along the bar to use the remnant and writes the program — with the cutting database for the material and seam detection to orient welded tube. Offline programming on a PC is standard on both lines."},
             {"q": "Floor space and power?",
              "a": "A 23 ft (7 m) machine needs about 65 ft (20 m) of length including the loader and unloader; a 40 ft (12 m) machine about 100 ft (30 m). 600 V 3-phase with the supplied transformer or 480 V, a chiller (included), assist gas and a dust collector. We lay the machine out for your building before you order."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about tube lasers",
        related=[{"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"},
                 {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "pipe-notcher.html", "label": "Tube notchers"},
                 {"href": "tube-end-forming-machines.html", "label": "Tube end formers"}, {"href": "band-saw.html", "label": "Band saws"}],
        related_title="More tube machinery from NovoTech",
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
            pdfs, specs, seen = [], [], set()      # hero: brochures only (the owner, Nov 1 2026); specifications on the products' buttons
            for f in members:
                for pd in (f.get("pdf"), f.get("spec_pdf"), *(f.get("spec_pdfs") or [])):
                    if pd and pd["file"] not in seen:
                        seen.add(pd["file"]); (pdfs if pd is f.get("pdf") and not f.get("pdf_item_only") else specs).append(pd)
            n = sum(len(f["specs"]["models"]) for f in members)
            for key in [page["hero"]] + page["minis"]:
                if key not in manifest:
                    raise SystemExit(f"{slug}: image key not in manifest: {key}")
            premium = any(f.get("brand") == "dener" for f in members)
            video = VIDEO_DENER if premium and VIDEO_DENER["intro_video"] and VIDEO_DENER["intro_video"]["thumb"] in manifest else NO_VIDEO
            p = {k: page[k] for k in ("title", "meta", "h1", "intro", "points", "hero", "minis", "groups", "faq")}
            # the press brake page format (the owner, Nov 1 2026): every group under its brand's line header (Dener premium line,
            # NovoTech / Senfeng value line) with no lead line under the heading, and no page-level "every model" table — that
            # table is on the hub
            brand_of = {}
            for f in members:
                brand_of.setdefault(f["group"], set()).add(f.get("brand"))
            p["groups"] = []
            for g in page["groups"]:
                brands = brand_of.get(g[0], set())
                if len(brands) != 1 or None in brands:
                    raise SystemExit(f"{slug}: group {g[0]} has families of several brands or none: {brands}")
                p["groups"].append((g[0], g[1], "", next(iter(brands))))
            p["related_pages"] = page["related"]
            p["related_title"] = page.get("related_title", "More laser and cutting machinery from NovoTech")
            if page.get("faq_title"):
                p["faq_title"] = page["faq_title"]
            write_category(slug, p, members, set_name, LN.SECTIONS[kind]["section"], hub=LN.hub(kind), siblings=LN.siblings(kind),
                           extra={"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **video,
                                  "nav_label": next(nav for s, _, _, _, nav, _ in LN.SECTIONS[kind]["subpages"] if s == slug),
                                  "catalogue_pdf": None, "catalogue_pdfs": pdfs, "spec_downloads": specs,
                                  **({"hero_minis_same_h": True} if page.get("minis_same_h") else {}),
                                  **{k: page[k] for k in ("compare", "loading") if page.get(k)}})
            print(f"{slug}: {len(members)} families, {n} models, {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
