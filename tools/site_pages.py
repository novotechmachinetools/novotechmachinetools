#!/usr/bin/env python3
"""The site's own pages — home, products, contact, about, brochures, articles, privacy — written as content/pages/*.json, and
content/catalog.json: the product categories of the main menu in groups, with a one-line description of each.

    python3 tools/site_pages.py && python3 build.py
"""
import json
import os

import guides

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = json.load(open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8"))
HOME = {"label": "Home", "href": "index.html"}

# ------------------------------------------------------------------------------------------------ catalog
BLURBS = {
    "press-brake": "CNC hydraulic, hybrid and electric press brakes, 22 to 1,323 US tons — Dener premium and NovoTech value lines.",
    "panel-bender": "CNC panel benders that bend all four sides of a panel without tool changes, 47″ to 165″ bend width.",
    "v-grooving-machine": "CNC V-grooving machines for sharp architectural bends — horizontal to 20 ft, vertical to 1/4″ plate.",
    "folder-sheet-metal-brake": "Magnetic brakes, box and pan brakes, hand brakes, hydraulic, electric and CNC folders, roofing brakes and 3-in-1 machines.",
    "horizontal-press-brake": "NC hydraulic horizontal presses for bending, straightening and punching, 11 to 165 US tons.",
    "press-brake-tooling-punch-and-die": "EUROSTAMP punches, dies, holders and adapters for every clamping style, made in Italy.",
    "laser-cutting-machine": "Fiber laser cutting machines for sheet and plate, 4 × 4 ft to 10 × 164 ft beds, 1.5 to 80 kW.",
    "tube-laser-cutting-machine": "Tube and profile fiber lasers for Ø0.3″ to 25.2″, 20 to 49 ft bars, 1.5 to 40 kW.",
    "laser-welding-machine": "Handheld laser welders from 0.8 kW, robotic laser welding cells to 20 kW, and laser cladding.",
    "shear-cutting": "Sheet metal shears, mechanical guillotines and hydraulic plate shears, 16 ga to 1-9/16″.",
    "ironworker-machines": "Hydraulic ironworkers and punching machines that punch, shear, notch and bend in one machine.",
    "corner-notcher": "Hydraulic and pneumatic corner notchers for the corners of boxes, cabinets and panels.",
    "plate-beveler": "Cevisa portable cold bevellers for weld preparation on plate and pipe, 1/8″ to 4-3/4″ thick.",
    "band-saw": "Manual, semi-automatic and automatic metal-cutting band saws — Bekamak premium and NovoTech value lines.",
    "band-saw-blades": "WIKUS bimetal M42 and carbide-tipped band saw blades, welded to length for your saw.",
    "circular-cold-saws": "Circular cold saws from manual to CNC carbide — ISITAN, CSM, Bekamak and NovoTech value line — and abrasive saws.",
    "aluminum-and-pvc-upcut-saws": "Automatic upcut, double-head, glazing bead and miter saws for aluminum and PVC extrusions.",
    "plate-rollers": "Hydraulic 4-roll and 3-roll plate rollers, motorized plate rollers and slip rolls, from 22 ga sheet to heavy plate.",
    "angle-rolls": "Angle rolls, profile benders, ring rollers and tube rollers for angle, flat bar, pipe and profiles.",
    "hydraulic-press": "Shop and bench presses from 10 tons, H-frame, C-frame and four-column hydraulic presses to 551 US tons, production presses and orbital riveters.",
    "bead-rollers": "Bead rollers, beading machines and a lock seamer for HVAC duct and sheet metal work.",
    "lock-former": "Pittsburgh lock formers, roll formers, an electric seam closer and round duct beading and slitting machines for HVAC ductwork.",
    "circle-cutters-and-seamers": "Circle cutting and flanging machines for tank ends, dished heads and duct fittings.",
    "pipe-benders": "CNC, NC, all-electric and hydraulic pipe and tube benders, Ø15/32″ to Ø8-5/8″.",
    "pipe-notcher": "Tube notchers, hole-saw and end-mill notchers and belt tube-end grinders for frames, railings and roll cages.",
    "tube-end-forming-machines": "Wecotech tube end forming machines from Switzerland — expanding, reducing, beading and flanging.",
    "wire-bending-machines": "CSM CNC 3D wire benders fed from the coil, Ø5/32″ to Ø9/16″ wire.",
    "welding-positioners": "Welding positioners from 33 to 8,818 lb, turning rolls, pipe stands, a welding table and downdraft tables.",
    "corner-welding-machines": "Gecam TIG and plasma corner welders for bent boxes, cabinets and enclosures.",
    "sheet-metal-plate-deburring-edge-rounding-finishing-grinding": "Gecam wide-belt deburring, edge rounding, deslagging and brush machines, 5-7/8″ to 53-1/8″ wide.",
    "corner-grinding-machines": "Gecam corner grinders for the weld seams of boxes, cabinets, doors and tube frames.",
    "pipe-sanding-polishing-machines": "Automatic, orbital and centreless pipe sanders and polishers, Ø3/16″ to Ø15-3/4″.",
    "rebar-bender-and-cutter": "GMS rebar benders, stirrup benders, rebar cutters and automatic processing lines, made in Turkey.",
    "pvc-aluminum-window-machines": "Plastmak aluminum and PVC window and door machinery — welding, cleaning, CNC machining, assembly and complete lines.",
    "belt-grinder": "Metal belt grinders with 2 – 8″ belts, disc sanders, bench grinders, chamfering machines and dust collectors.",
    "drill-press": "Gear-head, column and variable-speed drill presses, 1/2″ to 2″ in steel, with power feed and tapping.",
    "milling-machine": "Turret, universal and heavy ISO50 milling machines, drilling-milling machines, keyseaters and a head resurfacer.",
    "cnc-machine-tools": "Dener CNC lathes, vertical and double-column machining centres and a surface grinder; value-line CNC lathe, VMCs and boring mills.",
    "cnc-plasma-table": "CNC plasma tables 2 × 2 ft to 5 × 10 ft and CNC plasma pipe cutters for Ø2 – 11-3/4″ pipe.",
    "power-hammer": "Pneumatic planishing hammers, electric power hammers, a diamond roller former and air forging hammers.",
    "woodworking-machinery": "Jointers, thickness planers, table saws, band saws, multifunction machines, mortisers, a lathe and dust collection.",
}
GROUPS = [
    ("bending", "Sheet metal bending", "Press brakes, panel benders, sheet metal brakes and the tooling that goes in them.",
     ["press-brake", "panel-bender", "v-grooving-machine", "folder-sheet-metal-brake", "horizontal-press-brake", "press-brake-tooling-punch-and-die"]),
    ("laser", "Laser cutting and laser welding", "Fiber lasers for sheet, plate and tube, and laser welding from handheld to robotic.",
     ["laser-cutting-machine", "tube-laser-cutting-machine", "laser-welding-machine"]),
    ("cutting", "Shearing, punching, plasma cutting and notching", "Shears, ironworkers, CNC plasma tables, notchers and plate bevellers.",
     ["shear-cutting", "ironworker-machines", "cnc-plasma-table", "corner-notcher", "plate-beveler"]),
    ("sawing", "Sawing", "Band saws, cold saws and the blades that go in them.",
     ["band-saw", "band-saw-blades", "circular-cold-saws", "aluminum-and-pvc-upcut-saws"]),
    ("rolling", "Rolling, pressing and forming", "Plate and section rolling, presses, HVAC forming machines and metal shaping.",
     ["plate-rollers", "angle-rolls", "hydraulic-press", "bead-rollers", "lock-former", "circle-cutters-and-seamers", "power-hammer"]),
    ("tube", "Tube and pipe", "Bending, notching and end forming of tube and pipe, and CNC wire bending.",
     ["pipe-benders", "pipe-notcher", "tube-end-forming-machines", "wire-bending-machines"]),
    ("finishing", "Deburring, grinding and finishing", "Deburring and edge rounding, belt grinders and sanders, corner grinding and pipe polishing.",
     ["sheet-metal-plate-deburring-edge-rounding-finishing-grinding", "belt-grinder", "corner-grinding-machines", "pipe-sanding-polishing-machines"]),
    ("machining", "Drilling, milling and CNC machining", "Drill presses, milling machines, CNC lathes, machining centres and surface grinders.",
     ["drill-press", "milling-machine", "cnc-machine-tools"]),
    ("welding", "Welding", "Positioners, turning rolls and corner welders that take the hand work out of repeat welds.",
     ["welding-positioners", "corner-welding-machines"]),
    ("rebar", "Rebar machinery", "Benders, cutters and processing lines for reinforcing steel.", ["rebar-bender-and-cutter"]),
    ("windows", "Aluminum and PVC window machinery", "Machines for window, door and curtain-wall fabricators.",
     ["pvc-aluminum-window-machines"]),
    ("wood", "Woodworking machinery", "Jointers, planers, saws and joinery machines for the cabinet shop and the joinery.",
     ["woodworking-machinery"]),
]
CARD_IMAGE = {"folder-sheet-metal-brake": "nt-card-roofing-brake", "lock-former": "nt-card-lock-former"}
FEATURED = ["press-brake", "laser-cutting-machine", "tube-laser-cutting-machine", "band-saw", "rebar-bender-and-cutter", "plate-rollers",
            "ironworker-machines", "shear-cutting", "pipe-benders", "panel-bender",
            "sheet-metal-plate-deburring-edge-rounding-finishing-grinding", "press-brake-tooling-punch-and-die"]

BRANDS = [
    {"name": "Dener", "country": "Turkey", "since": "1974", "logo": None, "href": "press-brake.html",
     "what": "CNC press brakes, panel benders, hydraulic shears, sheet and tube fiber lasers, CNC lathes, machining centres and surface grinders"},
    {"name": "GMS", "country": "Turkey", "since": "1960", "logo": None, "href": "rebar-bender-and-cutter.html",
     "what": "Rebar benders, stirrup benders, rebar cutters and automatic rebar processing lines"},
    {"name": "ISITAN", "country": "Turkey", "since": "1959", "logo": "isitan-logo", "href": "plate-rollers.html",
     "what": "Plate rollers, pipe benders, cold saws, tube notchers, bead rollers and circle cutters"},
    {"name": "Bekamak", "country": "Turkey", "since": "1990", "logo": "bekamak-logo", "href": "band-saw.html",
     "what": "Manual, semi-automatic and automatic band saws and automatic circular saws"},
    {"name": "Gecam", "country": "Italy", "since": None, "logo": "gecam-logo", "href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html",
     "what": "Deburring and edge rounding machines, corner grinders and corner welders"},
    {"name": "Eurofintec", "country": "Italy", "since": None, "logo": "eurofintec-logo", "href": "pipe-sanding-polishing-machines.html",
     "what": "Orbital, centreless and large-pipe sanders, tube brushing and tube-end deburring"},
    {"name": "EUROSTAMP", "country": "Italy", "since": "1970", "logo": "eurostamp-logo", "href": "press-brake-tooling-punch-and-die.html",
     "what": "Press brake punches, dies, holders and adapters for every clamping style"},
    {"name": "CSM", "country": "Taiwan", "since": "1982", "logo": "csm-logo", "href": "pipe-benders.html",
     "what": "CNC and hydraulic tube benders, CNC wire benders and automatic saws"},
    {"name": "Senfeng", "country": "China", "since": "2004", "logo": "senfeng-logo", "href": "laser-cutting-machine.html",
     "what": "Fiber laser cutting machines, laser welding and cladding, panel benders"},
    {"name": "Cevisa", "country": "Spain", "since": "1969", "logo": "cevisa-logo", "href": "plate-beveler.html",
     "what": "Shearing and milling plate bevellers for weld preparation"},
    {"name": "Plastmak", "country": "Turkey", "since": None, "logo": "plastmak-logo", "href": "pvc-aluminum-window-machines.html",
     "what": "Aluminum and PVC window and door machinery, from single machines to complete lines"},
    {"name": "Tubend", "country": "Turkey", "since": None, "logo": "tubend-logo", "href": "pipe-benders.html",
     "what": "Mandrel-less pipe benders and welding positioners"},
    {"name": "Wecotech", "country": "Switzerland", "since": None, "logo": None, "href": "tube-end-forming-machines.html",
     "what": "Tube end forming machines: expanders, reducers, inner and outer formers"},
    {"name": "WIKUS", "country": "Germany", "since": None, "logo": None, "href": "band-saw-blades.html",
     "what": "Bimetal and carbide-tipped band saw blades, welded to length"},
    {"name": "NovoTech premium line", "country": "Turkey", "since": None, "logo": "novotech-logo", "href": "plate-rollers.html",
     "what": "Plate rollers, angle rolls, ironworkers, hydraulic presses, shears and pipe polishers built to NovoTech's specification with European components"},
    {"name": "NovoTech value line", "country": "China", "since": None, "logo": "novotech-logo", "href": "hydraulic-press-brake.html",
     "what": "CNC press brakes, fiber lasers, shears, panel benders and band saws built to North American quality standards"},
]

# PDFs on the brochures page, in the order shown, under the catalog groups: file → title
BROCHURES = [
    ("bending", "NovoTech-Dener-Hydraulic-Press-Brakes-2026.pdf", "Dener hydraulic and hybrid CNC press brakes"),
    ("bending", "NovoTech-Dener-Servo-Press-Brakes-2026.pdf", "Dener servo-electric press brakes"),
    ("bending", "NovoTech-Hydraulic-Press-Brakes-2026.pdf", "NovoTech value-line hydraulic press brakes"),
    ("bending", "NovoTech-Electric-Press-Brakes-2026.pdf", "NovoTech value-line electric press brakes"),
    ("bending", "NovoTech-Dener-Panel-Bender-2026.pdf", "Dener CNC panel bender"),
    ("bending", "NovoTech-Panel-Benders-Value-Line-2026.pdf", "NovoTech value-line panel benders"),
    ("bending", "NovoTech-Senfeng-Panel-Benders-2026.pdf", "Senfeng panel benders"),
    ("bending", "NovoTech-V-Grooving-Machines-2026.pdf", "CNC V-grooving machines"),
    ("bending", "NovoTech-Horizontal-Press-Brakes-2026.pdf", "NovoTech premium-line horizontal press brakes"),
    ("bending", "NovoTech-Tubend-Presses-Benders-Positioners-2026.pdf", "Tubend pipe benders and welding positioners"),
    ("bending", "NovoTech-Press-Brake-Tooling-Catalogue-2026.pdf", "EUROSTAMP press brake tooling catalogue — inch edition"),
    ("laser", "NovoTech-Dener-Fiber-Lasers-2026.pdf", "Dener fiber laser cutting machines"),
    ("laser", "NovoTech-Fiber-Lasers-Value-Line-2026.pdf", "NovoTech value-line fiber lasers"),
    ("laser", "NovoTech-Senfeng-Fiber-Lasers-2026.pdf", "Senfeng fiber laser cutting machines"),
    ("laser", "NovoTech-Dener-Tube-Lasers-2026.pdf", "Dener tube laser cutting machines"),
    ("laser", "NovoTech-Tube-Lasers-Value-Line-2026.pdf", "NovoTech value-line tube lasers"),
    ("laser", "NovoTech-Senfeng-Tube-Lasers-2026.pdf", "Senfeng tube laser cutting machines"),
    ("laser", "NovoTech-Senfeng-Laser-Welding-Cladding-2026.pdf", "Senfeng laser welding and cladding machines"),
    ("cutting", "NovoTech-Dener-Hydraulic-Shears-2026.pdf", "Dener hydraulic guillotine shears"),
    ("cutting", "NovoTech-Guillotine-Shears-2026.pdf", "NovoTech premium-line mechanical guillotine shears"),
    ("cutting", "NovoTech-Hydraulic-Shearing-Machines-2026.pdf", "NovoTech value-line hydraulic shears"),
    ("cutting", "NovoTech-Sheet-Metal-Shears-2026.pdf", "NovoTech value-line sheet metal shears"),
    ("cutting", "NovoTech-Ironworkers-Punching-Machines-2026.pdf", "NovoTech premium-line ironworkers and punching machines"),
    ("cutting", "NovoTech-Cevisa-Plate-Bevelling-Machines-2026.pdf", "Cevisa plate bevelling machines"),
    ("sawing", "NovoTech-Bekamak-Band-Saws-Catalogue-2026.pdf", "Bekamak band saw and circular saw catalogue"),
    ("sawing", "NovoTech-Value-Line-Band-Saws-Catalogue-2026.pdf", "NovoTech value-line band saw catalogue"),
    ("rolling", "NovoTech-Plate-Rolls-Premium-Line-2026.pdf", "NovoTech premium-line plate rolls"),
    ("rolling", "NovoTech-Isitan-Sheet-Metal-Forming-Catalogue-2025.pdf", "ISITAN machinery catalogue"),
    ("rolling", "NovoTech-Angle-Rolls-Section-Benders-2026.pdf", "Angle rolls and section benders"),
    ("rolling", "NovoTech-Hydraulic-Shop-Presses-2026.pdf", "Hydraulic shop presses"),
    ("rolling", "NovoTech-Production-Hydraulic-Presses-2026.pdf", "Production hydraulic presses"),
    ("rolling", "NovoTech-Notchers-Circle-Cutters-Pipe-Polishers-Benders-2026.pdf", "Corner notchers, circle cutters, pipe polishers and benders"),
    ("tube", "NovoTech-CSM-Electric-Tube-Benders-2026.pdf", "CSM electric tube and wire benders"),
    ("tube", "NovoTech-CSM-Hydraulic-Tube-Benders-2026.pdf", "CSM hydraulic tube benders, end formers and saws"),
    ("tube", "NovoTech-Wecotech-Tube-End-Forming-2026.pdf", "Wecotech tube end forming machines"),
    ("finishing", "NovoTech-Gecam-Deburring-Finishing-Pipe-Sanding-2026.pdf", "Gecam and Eurofintec deburring, finishing and pipe sanding"),
    ("machining", "NovoTech-Dener-CNC-Lathes-2026.pdf", "Dener CNC lathes"),
    ("machining", "NovoTech-Dener-Machining-Centres-2026.pdf", "Dener vertical and double-column machining centres"),
    ("machining", "NovoTech-Dener-Surface-Grinder-2026.pdf", "Dener NC surface grinder"),
    ("rebar", "NovoTech-GMS-Rebar-Bending-Cutting-Machines-Catalogue.pdf", "GMS rebar bending and cutting machines"),
    ("windows", "NovoTech-Plastmak-Window-Machinery-2026.pdf", "Plastmak aluminum and PVC window machinery"),
]

COMMON_FAQ_HOURS = f"{SITE['hours']} Eastern"


def write(slug, data):
    data = {"slug": slug, **data}
    json.dump(data, open(os.path.join(ROOT, "content", "pages", slug + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def main():
    json.dump({"groups": [{"id": g, "title": t, "lead": l, "slugs": s} for g, t, l, s in GROUPS], "blurbs": BLURBS,
               "card_image": CARD_IMAGE, "featured": FEATURED, "brands": BRANDS,
               "brochures": [{"group": g, "file": "files/" + f, "title": t} for g, f, t in BROCHURES]},
              open(os.path.join(ROOT, "content", "catalog.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # ---------------------------------------------------------------------------------------------- home
    write("index", {
        "template": "home.html",
        "title": "Metal Fabrication Machinery Supplier in Canada | NovoTech",
        "meta_description": "Press brakes, fiber lasers, band saws, rebar benders, plate rollers, ironworkers and deburring machines — sold, installed and supported in Canada from Mississauga, ON, Canada.",
        "h1": "Metal fabrication machinery, sold and supported in Canada",
        "intro": "Press brakes, fiber lasers, band saws, rebar benders, plate rollers, ironworkers, deburring machines and press brake tooling "
                 "from manufacturers in Turkey, Italy, Spain, Switzerland, Germany, Taiwan and China. Every machine comes with a CSA-approved "
                 "panel, and NovoTech installs it, trains your operators and keeps the parts in Mississauga, Ontario, Canada.",
        "hero_image": "dn-xl-1",
        "hero_image_secondary": ["dn-gfl-3", "bk-hero-auto-350ga", "b-45x1"],
        "hero_points": ["Showroom and parts warehouse in Mississauga, Ontario, Canada",
                        "CSA-approved electrical panel and a 1-year warranty on every machine",
                        "Installation, operator training and technical support anywhere in Canada"],
        "breadcrumb": [{"label": "Home"}],
        "intro_video": {"id": "ZGo_n6-2_Qc", "thumb": "video-ZGo_n6-2_Qc", "title": "NovoTech Machine Tools — who we are and what we sell",
                        "duration": "PT2M55S"},
        "showroom": ["nt-showroom-building", "nt-showroom-band-saws", "nt-showroom-ironworkers", "nt-showroom-rebar"],
        "quote": {"intro": "Tell us what you need to cut, bend, roll or finish — material, thickness, length and how many parts — and we will "
                           "recommend the machine and come back with pricing, delivery and the right voltage for your shop."},
    })

    # ---------------------------------------------------------------------------------------------- products
    write("products", {
        "template": "products.html",
        "title": "Metal Fabrication Machines — All Products | NovoTech",
        "meta_description": "Every machine NovoTech sells in Canada: press brakes, lasers, shears, ironworkers, band saws, plate rollers, tube benders, deburring, rebar and window machinery.",
        "h1": "Metal fabrication machines — the full NovoTech range",
        "intro": "Thirty-four kinds of machine for sheet metal, plate, structural steel, tube, rebar and window fabrication. Each page has "
                 "the full specifications in inches and millimetres, photos, videos and a PDF brochure; every machine is supplied with a "
                 "CSA-approved panel and supported from Mississauga, Ontario, Canada.",
        "breadcrumb": [HOME, {"label": "Products"}],
        "quote": {"intro": "Not sure which machine fits the work? Describe the parts — material, thickness, length and quantity — and we "
                           "will recommend the machine and send pricing, delivery and voltage options."},
    })

    # ---------------------------------------------------------------------------------------------- contact
    write("contact-us", {
        "template": "contact.html",
        "title": "Contact NovoTech Machine Tools — Mississauga, ON, Canada | Quote",
        "meta_description": "Call +1 647 526 5510, email or visit the NovoTech showroom at 1365 Mid-Way Blvd, Mississauga, ON, Canada. Send your part drawings for a machine recommendation and quote.",
        "h1": "Contact NovoTech Machine Tools",
        "intro": "Send us drawings or photos of your parts and tell us what you need to make — we will recommend the right machine and "
                 "reply within one business day with pricing, delivery and voltage options. Or call us and talk to a product specialist.",
        "breadcrumb": [HOME, {"label": "Contact us"}],
        "map_query": "1365 Mid-Way Blvd, Unit 26, Mississauga, ON L5T 2J5, Canada",
        "whatsapp": "https://wa.me/16475265510",
        "visit": ["Our showroom and warehouse are at 1365 Mid-Way Blvd, Unit 26, in Mississauga, ON, Canada, with parking in front of the building.",
                  "Machines on the floor change as orders ship — call ahead and we will tell you what is in stock and make sure a "
                  "product specialist is there to run it for you.",
                  "Bring a sample part or drawing and we can talk through tooling, capacity and the options you need."],
        "quote": {"intro": "Attach part drawings, sketches or photos — PDF, DWG, DXF, STEP, JPG or PNG — and tell us the material, "
                           "thickness and quantities. We will recommend the machine and reply within one business day."},
    })

    # ---------------------------------------------------------------------------------------------- about
    write("about-us", {
        "template": "about.html",
        "title": "About NovoTech Machine Tools — Mississauga, Ontario, Canada",
        "meta_description": "NovoTech Machine Tools imports and supports metal fabrication machinery in Canada: Dener, GMS, ISITAN, Bekamak, Gecam, EUROSTAMP, CSM and more, from Mississauga, ON, Canada.",
        "h1": "About NovoTech Machine Tools",
        "intro": "NovoTech Machine Tools is a Canadian importer of metal fabrication machinery, based in Mississauga, Ontario, Canada. For more than "
                 "20 years we have worked with manufacturers we trust to bring Canadian shops machines that are built well, priced "
                 "right and supported here — with the parts, service and know-how to keep them running.",
        "hero_image": "nt-showroom-building",
        "breadcrumb": [HOME, {"label": "About us"}],
        "story": [
            {"title": "What we do",
             "text": ["We sell, install and support the machines that metal fabricators, steel service centres, rebar shops, HVAC "
                      "contractors and window manufacturers use every day: press brakes and panel benders, fiber lasers for sheet and "
                      "tube, shears and ironworkers, band saws and cold saws, plate rollers and section benders, tube benders, deburring "
                      "and finishing machines, rebar benders and cutters, aluminum and PVC window machinery, and press brake tooling.",
                      "Our customers range from one-person welding shops to production plants in the steel structure, automotive, "
                      "aerospace, die and mold, medical and general part production industries — in every province and territory."]},
            {"title": "How we work",
             "text": ["We start with your parts, not with a catalogue. Send us a drawing or a photo and tell us the material, thickness, "
                      "length and volume, and we will recommend the machine and the options that fit the work — and tell you when a "
                      "smaller machine will do the job.",
                      "Every machine we sell is fitted with a CSA-approved electrical panel for Canadian voltage and comes with a "
                      "one-year warranty. Our technicians commission machines, train operators and troubleshoot by video call, and spare "
                      "parts are stocked in Mississauga, ON, Canada."]},
            {"title": "Who we work with",
             "text": ["We have built long partnerships with manufacturers on several continents: Dener, GMS, ISITAN, Bekamak, Plastmak and "
                      "Tubend in Turkey; Gecam, Eurofintec and EUROSTAMP in Italy; Cevisa in Spain; Wecotech in Switzerland; WIKUS in "
                      "Germany; CSM in Taiwan; and Senfeng in China. Our own NovoTech premium line is built in Turkey to our "
                      "specification with European components, and the NovoTech value line is built to North American quality "
                      "standards."]},
            {"title": "Our mission",
             "text": ["To give every customer the right machine for the application at hand — and to stay with them after the sale, "
                      "with the parts, service and advice that keep the machine making money for years."]},
        ],
        "showroom": ["nt-showroom-building", "nt-showroom-band-saws", "nt-showroom-ironworkers", "nt-showroom-plate-rollers", "nt-showroom-rebar"],
        "videos": [
            {"id": "ZGo_n6-2_Qc", "thumb": "video-ZGo_n6-2_Qc", "title": "NovoTech Machine Tools — introduction", "duration": "PT2M55S"},
            {"id": "A1i_NljuVQo", "thumb": "video-A1i_NljuVQo", "title": "Dener Group — introduction", "duration": "PT2M52S"},
            {"id": "iliNCOM3m08", "thumb": "video-iliNCOM3m08", "title": "GMS — introduction", "duration": "PT2M32S"},
            {"id": "hlqm6ugPQzU", "thumb": "video-hlqm6ugPQzU", "title": "ISITAN — corporate introduction", "duration": "PT4M45S"},
            {"id": "6xEVXrP8h3k", "thumb": "video-6xEVXrP8h3k", "title": "Bekamak — corporate introduction", "duration": "PT3M4S"},
            {"id": "nnEMwdcC5kQ", "thumb": "video-nnEMwdcC5kQ", "title": "Gecam — corporate introduction", "duration": "PT2M27S"},
            {"id": "RTLFMt-ryOc", "thumb": "video-RTLFMt-ryOc", "title": "EUROSTAMP — press brake tooling introduction", "duration": "PT5M3S"},
        ],
        "quote": {"intro": "Tell us about your shop and the parts you make, and we will recommend the machine that fits — with pricing, "
                           "delivery and the right voltage option."},
    })

    # ---------------------------------------------------------------------------------------------- brochures
    write("brochures", {
        "template": "brochures.html",
        "title": "Machine Brochures & Catalogues — PDF Downloads | NovoTech",
        "meta_description": "Download NovoTech's PDF brochures: press brakes, fiber lasers, shears, band saws, plate rollers, tube benders, deburring, rebar, window machinery and press brake tooling.",
        "h1": "Brochures and catalogues",
        "intro": "Every brochure is a PDF with photos and full specifications in inches and millimetres, written for Canadian shops. "
                 "Download the ones you need, or ask us to email a printed-quality copy with prices.",
        "breadcrumb": [HOME, {"label": "Brochures"}],
        "quote": {"intro": "Tell us which brochure you are reading and the machine you are interested in, and we will send pricing, "
                           "delivery and the options that suit your work."},
    })

    # ---------------------------------------------------------------------------------------------- articles
    # the long guides kept from the old site, then one buying guide per product category (tools/guides.py), in topic sections
    older = [
        {"href": "band-saw.html#buying-guide", "title": "Band saw buying guide", "image": "bk-hero-auto-350ga", "group": "cutting",
         "featured": True,
         "text": "Horizontal and vertical, pivot and double-column, manual to fully automatic: how to choose a metal-cutting band saw, "
                 "and the blade, coolant and feed details that decide how well it cuts."},
        {"href": "plate-rollers.html#buying-guide", "title": "Plate roller buying guide", "image": "is-4rhms-3100-250", "group": "bending",
         "featured": True,
         "text": "3-roll and 4-roll machines, initial-pinch and double-pinch, how capacity is rated, cone bending, crowning, controls "
                 "and automation."},
        {"href": "ironworker-machines.html#buying-guide", "title": "Ironworker buying guide", "image": "sh-hkm115", "group": "punching",
         "featured": True,
         "text": "Punching and shearing tonnage, throat depth, stations and tooling: how to size an ironworker for the work in your "
                 "shop, and why not all tons are equal."},
        {"href": "press-brake-tooling-punch-and-die.html#tooling-guide", "title": "Press brake tooling guide", "image": "es-p-range",
         "group": "bending", "text": "Clamping styles, punch and die shapes, V-opening and tonnage, sectioned tools and horns: how to "
                                     "choose press brake punches and dies that fit your machine and your parts."},
        {"href": "the-benefits-of-using-a-rebar-bender-and-cutter-in-construction.html",
         "title": "The benefits of using a rebar bender and cutter in construction", "image": "b-45x1", "group": "rebar",
         "text": "Why contractors and rebar shops bend and cut on site and in the yard with machines instead of by hand: speed, "
                 "accuracy, safety and cost."},
    ]
    topic = dict(guides.TOPICS)
    place = {"band-saw.html#buying-guide": None,                                       # first in its section
             "plate-rollers.html#buying-guide": "horizontal-press-brake.html#buying-guide",
             "ironworker-machines.html#buying-guide": None,
             "press-brake-tooling-punch-and-die.html#tooling-guide": "press-brake.html#buying-guide",
             "the-benefits-of-using-a-rebar-bender-and-cutter-in-construction.html": "rebar-bender-and-cutter.html#buying-guide"}
    allcards = guides.cards()
    for a in older:
        a["topic"] = topic[a["group"]]
        after = place.get(a["href"])
        if after is None:
            first = next(i for i, c in enumerate(allcards) if c["group"] == a["group"])
            allcards.insert(first, a)
        else:
            allcards.insert(next(i for i, c in enumerate(allcards) if c["href"] == after) + 1, a)
    article_groups = [{"id": gid, "title": title, "articles": [a for a in allcards if a["group"] == gid]} for gid, title in guides.TOPICS]
    article_groups = [g for g in article_groups if g["articles"]]
    write("metal-fabricating-articles", {
        "template": "articles.html",
        "title": "Metal Fabrication Buying Guides & Articles | NovoTech",
        "meta_description": f"{len(allcards)} buying guides from NovoTech's technicians: press brakes, lasers, shears, band saws, plate "
                            "rollers, tube benders, ironworkers, presses, grinders, CNC machines, rebar and window machinery.",
        "h1": "Buying guides and articles",
        "intro": "What we explain to customers before they buy — how the machines work, how capacity is rated, which options matter and "
                 "which do not — written by NovoTech's sales engineers and technicians from years of installing machines in Canada. "
                 "Each guide sits at the bottom of its product page, next to the machines it describes.",
        "breadcrumb": [HOME, {"label": "Articles"}],
        "articles": [a for g in article_groups for a in g["articles"]],
        "article_groups": [{"id": g["id"], "title": g["title"], "count": len(g["articles"])} for g in article_groups],
        "quote": {"intro": "Have a question the guides do not answer? Tell us about your parts and we will recommend the machine."},
    })

    # ---------------------------------------------------------------------------------------------- rebar article (old URL kept)
    write("the-benefits-of-using-a-rebar-bender-and-cutter-in-construction", {
        "template": "article.html",
        "title": "Benefits of a Rebar Bender and Cutter in Construction | NovoTech",
        "meta_description": "Why contractors and rebar shops bend and cut rebar with machines: speed, safety and accuracy, the types of benders and cutters, and what to look for when you buy one.",
        "h1": "The benefits of using a rebar bender and cutter in construction",
        "intro": "Why contractors, precast plants and rebar shops bend and cut reinforcing bar with machines instead of by hand — and "
                 "what to look for when you choose a rebar bender and cutter.",
        "breadcrumb": [HOME, {"label": "Articles", "href": "metal-fabricating-articles.html"}, {"label": "Rebar bender and cutter benefits"}],
        "article": "rebar-bender-cutter-benefits.html",
        "hero_image": "rg-bending",
        "byline": "NovoTech Machine Tools — sales and service team",
        "related": [{"href": "rebar-bender-and-cutter.html", "label": "Rebar benders and cutters"},
                    {"href": "rebar-bender.html", "label": "Rebar benders"}, {"href": "rebar-cutter.html", "label": "Rebar cutters"},
                    {"href": "automatic-rebar-processing-lines.html", "label": "Automatic rebar processing lines"}],
        "quote": {"intro": "Tell us the bar sizes and grades you work with, the shapes and quantities, and the power you have on site — we will "
                           "recommend the bender and cutter and send pricing and delivery."},
    })

    # ---------------------------------------------------------------------------------------------- privacy
    write("privacy-policy", {
        "template": "privacy.html",
        "title": "Privacy Policy | NovoTech Machine Tools",
        "meta_description": "How NovoTech Machine Tools collects, uses and protects the information you send through this website, including quote requests, attachments and the AI machine finder.",
        "h1": "Privacy policy",
        "intro": "This policy explains what information NovoTech Machine Tools Inc. collects through novotechmachinetools.com, why we "
                 "collect it and how we protect it. It applies to this website only.",
        "breadcrumb": [HOME, {"label": "Privacy policy"}],
        "no_quote": True,
        "effective": "2026-10-27",
        "sections": [
            {"title": "Who we are",
             "text": [f"NovoTech Machine Tools Inc., {SITE['address']['street']}, {SITE['address']['city']}, {SITE['address']['region']} "
                      f"{SITE['address']['postal']}, Canada. Questions about this policy or your information can be sent to "
                      "info@NovoTechMachineTools.com or by phone to " + SITE["phone"] + "."]},
            {"title": "Information you send us",
             "text": ["When you send the quote form, we receive your name, email address and the optional company name, phone number, "
                      "machine of interest, message and any files you attach (drawings, photos or documents). The form is delivered to "
                      "our sales inbox by email.",
                      "When you call, email or message us on social media, we receive the information you choose to share."]},
            {"title": "How we use it",
             "text": ["We use your information to answer your request: to recommend machines, send quotations and brochures, arrange "
                      "delivery, installation, training, service and warranty work, and to keep a record of our business with you. "
                      "We do not sell or rent your information, and we do not add you to a mailing list without your consent."]},
            {"title": "Spam protection",
             "text": ["The quote form is protected by Google reCAPTCHA. reCAPTCHA collects hardware and software information, such as "
                      "device and application data, and sends it to Google to check that the form is sent by a person. Google's "
                      "Privacy Policy and Terms of Service apply to that check."],
             "links": [{"href": "https://policies.google.com/privacy", "label": "Google Privacy Policy"},
                       {"href": "https://policies.google.com/terms", "label": "Google Terms of Service"}]},
            {"title": "AI machine finder",
             "text": ["The AI machine finder sends the question you type, together with our machine catalogue, to Anthropic's Claude "
                      "service to write the answer. Do not type personal information into it. The questions are not used to identify "
                      "you; to protect the service from abuse, the server keeps a short-lived count of requests per IP address."]},
            {"title": "Videos and other services",
             "text": ["Product videos are embedded from YouTube in its privacy-enhanced mode (youtube-nocookie.com). A video loads "
                      "when it comes into view or when you press play, and YouTube's privacy policy then applies. Links to our pages "
                      "on YouTube, LinkedIn, Facebook, Instagram, X and TikTok take you to those services, whose own privacy policies "
                      "apply."]},
            {"title": "Cookies",
             "text": ["This website sets no cookies of its own and uses no advertising or analytics trackers. Google reCAPTCHA and "
                      "YouTube, described above, may set their own cookies when they load."]},
            {"title": "How long we keep it and how we protect it",
             "text": ["We keep enquiries and quotations for as long as we need them to serve you and to meet our legal and accounting "
                      "obligations, and then delete them. The website is served over HTTPS, and access to our email and records is "
                      "limited to the NovoTech staff who need it."]},
            {"title": "Your rights",
             "text": ["Under Canada's Personal Information Protection and Electronic Documents Act (PIPEDA) you can ask to see the "
                      "personal information we hold about you, ask us to correct it, or withdraw your consent and ask us to delete it, "
                      "subject to our legal obligations. Write to info@NovoTechMachineTools.com and we will reply within 30 days."]},
            {"title": "Changes to this policy",
             "text": ["We will post any change to this policy on this page with a new effective date."]},
        ],
    })
    print("site pages written")


if __name__ == "__main__":
    main()
