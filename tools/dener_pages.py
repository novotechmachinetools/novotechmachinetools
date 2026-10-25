#!/usr/bin/env python3
"""Dener pages: press-brake, laser-cutting-machine (sheet lasers), tube-laser-cutting-machine, panel-bender — family set
content/families/dener.json, photos from tools/dener_photos.py (section 'dener').  The Dener shears are appended to the
shears page by tools/saymak_pages.py (set 'shears').

    python3 tools/dener_photos.py                       # export the renders / frames to tools/src-images/dener
    python3 tools/dener_pages.py                        # families + pages + image_map entries (tools/dener_keys.txt)
    python3 tools/yt_thumbs.py $(cat tools/dener_vids.txt)
    python3 tools/make_images.py --only $(cat tools/dener_keys.txt)
"""
import json
import os
import shutil

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401
import dener_data as D
import dener_photos as PH
import vl_sheet_data as VL   # NovoTech value-line panel benders below the Dener machine on panel-bender.html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "dener"
BRAND = D.BRAND
SRC_PDF = "/home/claude/dener/"
PDF_PB_FILE = "files/NovoTech-Dener-Hydraulic-Press-Brakes-2026.pdf"
PDF_SERVO_FILE = "files/NovoTech-Dener-Servo-Press-Brakes-2026.pdf"
PDF_LASER_FILE = "files/NovoTech-Dener-Fiber-Lasers-2026.pdf"
PDF_TUBE_FILE = "files/NovoTech-Dener-Tube-Lasers-2026.pdf"
PDF_PANEL_FILE = "files/NovoTech-Dener-Panel-Bender-2026.pdf"
PDF_SHEAR_FILE = "files/NovoTech-Dener-Hydraulic-Shears-2026.pdf"
PDF_VL_PANEL_FILE = "files/NovoTech-Panel-Benders-Value-Line-2026.pdf"
COPY_PDFS = {PDF_PB_FILE: "nt-hydraulic-pb.pdf", PDF_SERVO_FILE: "pdf2/NovoTech_Dener_Servo_Press_Brakes (1).pdf", PDF_LASER_FILE: "nt-fiber-laser.pdf"}

BRAND_LINE = ("Dener Makina builds press brakes, shears and fiber lasers in Kayseri, Turkey — 52 years, exports to more than 100 countries, "
              "Dener Canada in Mississauga. Sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in Turkey by Dener Makina", "text": "Dener has built sheet-metal machinery in Kayseri since 1974 — a 1.3 million m² campus, "
          "its own design awards (Good Design, European Product Design, Design Turkey) and offices in the USA, Canada, Germany and India."}
INTRO_VIDEO = {"intro_video": {"id": "A1i_NljuVQo", "title": "DENER Group introduction video", "thumb": "video-A1i_NljuVQo", "duration": "PT2M52S"},
               "intro_video_heading": "Inside the factory — where the machines are built",
               "intro_video_text": "A tour of Dener Makina in Kayseri, Turkey, where the press brakes, shears and fiber lasers on this page are designed and built."}
CRUMBS_TAIL = []


def pdf(file, label):
    f = os.path.join(ROOT, "src", file)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": file, "label": label, "size": size}


PAGE_PB = dict(
    title="Hydraulic & Electric CNC Press Brakes, 22–661 Tons | NovoTech",
    meta="CNC press brakes made in Turkey, sold in Canada: XL hydraulic to 661 US tons × 20 ft, XH hybrid with servo pump, DDM servo-electric to 220 tons, DDS ball-screw from 22 tons. ESA and Delem controls.",
    h1="CNC press brakes — hydraulic, hybrid, servo-electric and ball-screw",
    intro="A press brake bends sheet and plate between a punch and a V-die; the CNC positions the back gauge and controls the ram depth, "
          "crowning and angle, so the operator loads the sheet and presses the pedal. NovoTech sells Dener press brakes in Canada — the "
          "XL hydraulic press brake in 18 models from 66 to 661 US tons and 5 to 20 ft, the XH hybrid that puts a servo pump on the same "
          "frame for 42 – 58 % less energy, the DDM servo-electric press brake with no hydraulic oil from 44 to 220 US tons, and the DDS "
          "ball-screw press brake from 22 US tons for small parts. ESA S640 / S875 or Delem DA-66S / 69S controls, European-style tooling, "
          "back gauges to 6 axes, crowning, angle measurement, sheet followers and robot cells. For a small shop there is also the İşitan "
          "compact hydraulic press brake. Installed and supported from Mississauga, ON, with a CSA-approved panel and Dener Canada parts.",
    points=["XL hydraulic: 18 models, 66 – 661 US tons × 5 – 20 ft; tandem to 60 ft and 1,800 tons",
            "XH hybrid: servo pump on the XL frame — 42 – 58 % less energy, faster approach and return",
            "DDM servo-electric 44 – 220 tons and DDS ball-screw 22 / 44 tons — no hydraulic oil"],
    hero="dn-xl-1", minis=["dn-ddm-2", "dn-xh-1"],
    groups=[("pb-hydraulic", "XL hydraulic CNC press brakes", "The standard: a monoblock frame, Hawe hydraulics and an ESA 2D control, 5 to 20 ft and 66 to 661 US tons.", BRAND),
            ("pb-hybrid", "XH hybrid press brakes", "The XL with a servo-driven pump — the same frame and cylinders, less energy, more speed, less noise.", BRAND),
            ("pb-servo", "Servo-electric and ball-screw press brakes", "No hydraulic oil: the DDM servo-electric brake for production to 220 tons and the DDS ball-screw brake for small parts.", BRAND)],
    faq=[{"q": "Hydraulic, hybrid or servo-electric — which press brake should I buy?",
          "a": "A hydraulic XL is the lowest price per ton and bends anything from 5 ft brackets to 20 ft, 1/2″ plate; it is the right machine when tonnage and length matter more than cycle time. The XH hybrid is the same machine with a servo pump: it costs a little more and pays it back in power (42 – 58 % less), speed and noise — the right choice for a shop that runs the brake all day. The DDM servo-electric brake has no oil at all, bends at twice the speed with 0.01 mm repeatability and draws power only while the ram moves — the choice for high-mix job shops and clean environments up to 220 US tons × 13 ft. Below 44 tons the DDS ball-screw brake is the compact, plug-in electric machine for boxes and brackets."},
         {"q": "How much tonnage do I need?",
          "a": "Air bending mild steel with the standard V = 8 × thickness die takes roughly 8 US tons per foot for 16 ga, 15 tons per foot for 1/8″, 30 for 3/16″, 55 for 1/4″ and 130 tons per foot for 1/2″; stainless needs about 50 % more, aluminum about half. A 10 ft × 1/4″ job is therefore a 135 – 175 ton machine, 10 ft × 1/2″ a 320 – 400 ton machine. Tell us the thickest and longest bend you make and we size the brake and the tooling."},
         {"q": "Which control comes with the machine?",
          "a": "The XL and DDS come with the 15″ ESA S640 2D graphic control: draw the profile, the control calculates the bend sequence, tonnage, back-gauge positions and crowning. The DDM comes with the 21″ ESA S875 W 3D control with 3D simulation and offline programming. Delem DA-66S (2D) and DA-69S (3D) are options on every machine, as is the ESA S875 W on the XL. All of them program in inches or millimetres and import DXF files."},
         {"q": "What is a hybrid press brake?",
          "a": "On a conventional hydraulic brake the motor and pump run at full speed all day, whether the ram moves or not. The XH hybrid replaces the AC motor and fixed pump with a servo motor driving an inverter pump: the pump turns only while the ram moves, at the speed the ram needs. Dener measures 42 – 58 % energy saving and 17 – 75 % faster approach and return against the XL of the same tonnage, with less heat in the oil and a quieter shop. Everything else — frame, cylinders, valves, tooling, controls — is the XL."},
         {"q": "What back gauge and axes are available?",
          "a": "Every machine has the Y1 and Y2 ram axes and an X back-gauge axis on a ball screw and linear guides; the DDM adds R (height) as standard. Options go up to the 6-axis ATF gauge with X1, X2, R1, R2, Z1 and Z2 — two independently positioned fingers for angled flanges — plus a CNC crowning axis and the Dual X-Prime fingers. The back gauge is set by the control for every bend of the program."},
         {"q": "Which tooling fits?",
          "a": "European-style (Promecam / Amada) segmented punches and dies with European-style holders are standard; Wila mechanical or hydraulic clamping, quick-release and pneumatic clamping are options, and American-style tooling can be fitted with an adapter. NovoTech stocks Eurostamp press brake tooling in Canada — punches, dies, radius tools, hemming and joggle tools — and sizes it to your machine."},
         {"q": "Do you deliver, install and service in Canada?",
          "a": "Yes. Machines ship from Kayseri to Mississauga; we unload, level, commission and train your operators, and Dener Canada stocks parts here. Every machine comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request), a 1-year warranty and remote diagnostics through the control."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about press brakes",
    related_pages=[{"href": "hydraulic-press-brake.html", "label": "Value-line hydraulic press brakes"}, {"href": "electric-press-brake.html", "label": "Value-line electric press brakes"},
                   {"href": "compact-hydraulic-press-brakes.html", "label": "Compact hydraulic press brakes"}, {"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"},
                   {"href": "panel-bender.html", "label": "CNC panel benders"}, {"href": "shear-cutting.html", "label": "Metal shears"},
                   {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}, {"href": "horizontal-press-brake.html", "label": "Horizontal press brakes"}],
    related_title="More bending and cutting machinery from NovoTech",
)

PAGE_LASER = dict(
    title="Fiber Laser Cutting Machines for Sheet Metal, 3–40 kW | NovoTech",
    meta="Sheet metal fiber laser cutting machines sold and installed in Canada: GFL production lasers with pallet changer and Smart closed, semi-closed and open lasers, 5 × 10 ft to 13 × 82 ft tables, 3 to 40 kW sources.",
    h1="Sheet metal fiber laser cutting machines — 5 × 10 ft to 13 × 82 ft, 3 to 40 kW",
    intro="A fiber laser cutting machine cuts sheet and plate from a DXF file with a focused beam — mild steel to 1-1/2″, stainless and aluminum "
          "to 1″ and more with the high-power sources — at speeds no plasma or punch can match, with a clean edge and no tooling. NovoTech sells "
          "Dener fiber lasers in Canada: the GFL production laser with a 1.5 G gantry and pallet changer in 5 × 10, 6.6 × 13 and 6.6 × 20 ft, "
          "and the Smart series — closed-type with double table in six sizes to 41 ft, semi-closed single table to 13 × 82 ft, and the open-type "
          "entry machine — all with IPG, Raycus or nLIGHT sources from 3 to 40 kW, Precitec autofocus heads and nesting software. Loading "
          "towers, sheet storage and bevel heads are available. Installed and supported from Mississauga, ON.",
    points=["GFL: 1.5 G, 394 ft/min, pallet changer — 5 × 10 to 6.6 × 20 ft, 3 – 40 kW",
            "Smart closed-type with double table in 6 sizes to 8.5 × 41 ft; semi-closed single table to 13 × 82 ft",
            "Smart open-type 3 – 6 kW entry machine; automation towers and storage for every model"],
    hero="dn-gfl-3", minis=["dn-smart-1", "dn-gfl-2"],
    groups=[("laser-gfl", "GFL production fiber lasers", "Dener's premium sheet laser: 1.5 G, pallet changer, 3 – 40 kW — built for a job shop that cuts all day.", BRAND),
            ("laser-smart", "Smart fiber lasers", "The value line from the same factory: closed, semi-closed and open machines in table sizes to 13 × 82 ft.", BRAND)],
    faq=[{"q": "What laser power do I need?",
          "a": "Power sets the thickness and the speed. As a guide for mild steel: 3 kW cuts 1/2″, 6 kW 3/4″ (and 1/4″ at over 300 in/min), 12 kW 1″, 20 kW 1-1/4″ and 30 – 40 kW 1-1/2″ and beyond; stainless and aluminum run about 20 – 30 % thinner at the same power, with nitrogen or air assist. Most Canadian job shops buying today choose 6 or 12 kW: thick enough for structural work, fast enough to pay for the machine on thin sheet. Tell us your material mix and we run the cutting chart for you."},
         {"q": "GFL or Smart — what is the difference?",
          "a": "Both come from Dener's Kayseri plant with the same sources, heads and software. The GFL is the production machine: a heavier stress-relieved frame and space-frame bridge rated for 1.5 G, a pallet changer and the full option list — the machine for two shifts a day. The Smart series is built to a lower price: the closed-type still has a double exchange table and 1 G, the semi-closed machines offer very large single tables, and the open-type is the entry-level 3 – 6 kW laser. Same cut quality; the GFL is faster between parts and lasts longer at high duty."},
         {"q": "Which table size?",
          "a": "The model number is the nominal working area in centimetres: 3015 = 10 × 5 ft (3,000 × 1,500 mm) — a standard 4 × 8 or 5 × 10 sheet; 4020 = 13 × 6.6 ft; 6020 = 20 × 6.6 ft for 6 × 20 plate; 6025 and 8025 = 20 and 26 ft × 8.2 ft; 12526 = 41 × 8.5 ft. The 5 × 10 machine is the Canadian standard; buy the 6020 if you cut 20 ft plate or want to nest several sheets without reloading."},
         {"q": "What about assist gas and fume extraction?",
          "a": "Oxygen gives the fastest cut and an oxide edge on mild steel; nitrogen a clean, paint-ready edge on all metals; compressed air at 16 bar replaces nitrogen on sheet to about 1/4″ and cuts the gas bill to near zero — the intelligent air-cutting package is an option. The machines have pneumatic extraction compartments under the table and connect to a dust collector, which we can supply."},
         {"q": "Can the laser be automated?",
          "a": "Yes — a loading / unloading tower that feeds the pallet changer, sheet storage with several shelves for lights-out production, part sorting, and bevel heads for weld preparation. The GFL and the closed-type Smart are prepared for the tower; ask us for the automation layout."},
         {"q": "What does the machine need on site?",
          "a": "A level floor, 600 V 3-phase (with the transformer we supply) or 480 V, a chiller (included), assist gas, a dust collector and a compressed-air supply for air cutting. A 6 kW 3015 draws about 30 kW in total. Delivery, installation and operator training are done by NovoTech from Mississauga."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about fiber laser cutting machines",
    related_pages=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "press-brake.html", "label": "CNC press brakes"},
                   {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring after laser cutting"}, {"href": "shear-cutting.html", "label": "Metal shears"},
                   {"href": "panel-bender.html", "label": "CNC panel bender"}],
    related_title="Machinery that works alongside a laser",
)

PAGE_TUBE = dict(
    title="Tube Laser Cutting Machines, Ø0.3″ to 25″ Tube & Profile | NovoTech",
    meta="Tube and profile fiber laser cutting machines sold and installed in Canada: E-FTL at 1 G for Ø0.3″ – 13.8″ and FTL to Ø25″ and 12 m bars, 3 to 20 kW, bundle loaders and bevel heads.",
    h1="Tube and profile laser cutting machines — Ø0.3″ to 25.2″, 3 to 20 kW",
    intro="A tube laser cuts round, square, rectangular and open profiles to length and cuts the holes, copes, slots and notches in them in one "
          "pass — no saw, no drill, no notcher, no layout — straight from the 3D model. NovoTech sells Dener tube lasers in Canada: the E-FTL "
          "with servo chucks accelerating at 1 G for tube from Ø0.3″ to 13.8″, and the heavy FTL for structural tube and pipe to Ø25.2″ and "
          "12 m bars weighing up to 2,600 kg. Both load from a bundle automatically, support the tube as it is cut, nest parts along the bar "
          "and unload finished pieces; 3 to 20 kW sources, bevel heads for weld preparations. For trailer, railing, furniture, agricultural, "
          "HVAC and steel-construction work. Installed and supported from Mississauga, ON.",
    points=["E-FTL: Ø0.3″ – 13.8″ (8 – 350 mm), 1 G, 394 ft/min, ±0.05 mm — four chuck sizes",
            "FTL: Ø0.6″ – 25.2″ (15 – 640 mm), bars to 39.4 ft and 5,732 lb — four chuck sizes",
            "3 – 20 kW sources, automatic bundle loader, following supports, 3D bevel head"],
    hero="dn-tube-2", minis=["dn-tube-6", "dn-tube-1"],
    groups=[("tube-eftl", "E-FTL tube lasers", "The fast tube laser for Ø0.3″ to 13.8″: 1 G servo axes, 394 ft/min, four chuck sizes.", BRAND),
            ("tube-ftl", "FTL heavy tube lasers", "For structural tube, pipe and profile to Ø25.2″ and 12 m bars of 2,600 kg.", BRAND)],
    faq=[{"q": "What can a tube laser cut?",
          "a": "Round, square, rectangular, oval and open profiles — angle, channel, flat bar — in mild steel, stainless, aluminum, copper and brass, from the chuck's minimum to its maximum size, in wall thicknesses to about 1/2″ (12 kW) or 3/4″ (20 kW). Holes, slots, copes for tube-to-tube joints, tabs and notches for folding, engraving — anything you can draw on the surface of the profile. The 5-axis head adds bevels for weld preparation."},
         {"q": "E-FTL or FTL?",
          "a": "The E-FTL is the fast machine for the sizes most fabricators use — railings, frames, furniture, trailers, exhaust — Ø0.3″ to 13.8″, accelerating at 1 G and running 394 ft/min on the small chucks. The FTL is built for weight: structural tube and pipe to Ø25.2″ and 12 m bars of 2,600 kg, with ±0.1 mm repeatability on the large chucks. Both take the same 3 – 20 kW sources and bundle loaders."},
         {"q": "How is the tube loaded?",
          "a": "From a bundle: the automatic loader separates one bar, measures it and feeds it to the rear chuck; the front chuck and following supports hold the bar as it is cut; finished parts drop onto the unloading table or conveyor and the remnant is ejected. One operator runs the machine while loading the next bundle. Loading lengths of 7, 9 and 12 m."},
         {"q": "What about software?",
          "a": "The CNC imports STEP / IGES solid models of the tube parts, unfolds them onto the profile, nests them along the bar to use the remnant and writes the program — with the cutting database for the material and the seam detection to orient welded tube. Offline programming on a PC is standard."},
         {"q": "Floor space and power?",
          "a": "A 7 m machine needs about 20 m (65 ft) of length including the loader and unloader; a 12 m machine about 30 m. 600 V 3-phase with the supplied transformer or 480 V, a chiller (included), assist gas and a dust collector. We lay the machine out for your building before you order."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about tube lasers",
    related_pages=[{"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"},
                   {"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "tube-end-forming-machines.html", "label": "Tube end formers"},
                   {"href": "band-saw.html", "label": "Band saws"}],
    related_title="More tube machinery from NovoTech",
)

PAGE_PANEL = dict(
    title="CNC Panel Benders, 63–165″ Wide, 0.2 s per Bend | NovoTech",
    meta="CNC panel benders sold in Canada: the Dener 79″ machine and NovoTech's value-line PB-M and PB-A, 63–165″, with automatic tool change — four sides, 0.2 s a bend.",
    h1="CNC panel benders — four-side bending with no tooling changes, 63 to 165″ bend width",
    intro="A panel bender is the machine that replaces a press brake for boxes, doors, enclosures, panels and HVAC parts: the blank is clamped "
          "by a blank-holder and a bending blade folds the flange up or down, hems it or forms a box corner in 0.2 s, while the manipulator "
          "turns the part to bend the next side — all four sides in one setup, no tooling changes, no skilled operator. NovoTech sells the "
          "Dener panel bender in Canada: blanks to 78.7 × 49.2″ (2,000 × 1,250 mm), flanges to 6.7″, 14 ga mild steel, 16 ga stainless and "
          "1/8″ aluminum, 15 servo axes with 0.001 mm positioning, 100 % electric at about 2.8 kW average draw. Automatic loading and "
          "unloading arms turn it into an unattended cell. Below it is NovoTech's own value line: the PB-M press-arm panel benders in nine sizes "
          "from 63 to 165″ and the PB-A with automatic tool change in four sizes to 126″, built in China to our specification with the same "
          "0.2 s bends and 14 ga capacity. All installed and supported from Mississauga, ON.",
    points=["Blanks to 78.7 × 49.2″, flanges to 6.7″ (11.8″ on request), 1 mm minimum radius, boxes from 5.5 × 7.5″ inside",
            "14 ga mild steel, 16 ga stainless, 1/8″ aluminum — 0.2 s per bend, 295 ft/min feeding",
            "Value line: PB-M 63 – 165″ in nine sizes, PB-A with 0.5 s automatic tool change to 126″; robot loading cells"],
    hero="dn-panel-1", minis=["dn-panel-2", "dn-panel-5"],
    groups=[("panel", "Dener CNC panel bender", "Fully servo-driven four-side bending cell with a 3D control — one model, 79 × 49″ blanks, made in Turkey.", BRAND),
            ("panel-value", "NovoTech value-line panel benders", "The PB-M press-arm machines in nine sizes and the PB-A with automatic tool change — 63 to 165″ bend width at a value-line price.", VL.BRAND)],
    faq=[{"q": "Panel bender or press brake?",
          "a": "A press brake bends one line at a time and the operator handles the part between bends; a panel bender clamps the blank once and forms every side — up, down, hems, box corners — automatically, in 0.2 s per bend and with the same accuracy on the first and the thousandth part. For boxes, doors, cabinets, enclosures, appliance and HVAC panels in sheet to 14 ga it is five to ten times faster than a brake and needs no skilled operator or tooling changes. For plate, long single bends, deep boxes or small batches of unusual parts the press brake stays the better machine — most shops run both."},
         {"q": "What sheet can it bend?",
          "a": "Mild steel to 14 ga (2.0 mm), stainless to 16 ga (1.5 mm), aluminum to 1/8″ (3.0 mm); blanks to 78.7 × 49.2″ (2,000 × 1,250 mm) and flange heights to 6.7″ (170 mm), 11.8″ on request; minimum bend radius 1 mm, minimum four-side box 5.5 × 7.5″ inside. Pre-painted and film-covered sheet is bent without marking thanks to the brush table and blade geometry."},
         {"q": "How is it programmed?",
          "a": "From the 3D model or a DXF on the 3D control: the software unfolds the part, sets the bending sequence and simulates it, with automatic compensation for springback. A new part is programmed in minutes and runs without test bends; programs can be prepared offline on a PC."},
         {"q": "Can it run unattended?",
          "a": "With the optional loading and unloading arms the machine takes blanks from a stack and places finished parts on a pallet, so it runs lights-out behind a laser. The 15-axis servo drive and the 2.8 kW average consumption make it the cheapest machine on the floor to keep running."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about panel benders",
    related_pages=[{"href": "press-brake.html", "label": "CNC press brakes"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "corner-notcher.html", "label": "Corner notchers"}],
    related_title="More sheet-metal machinery from NovoTech",
)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "dener")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")]
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/dener/{key}{ext}", "alt": p["alt"], "section": "dener", "trim": p.get("trim", False), "quality": 82, "cutout": False}
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "dener_keys.txt"), "w").write(",".join(keys))
    return keys


def copy_pdfs():
    for dst, src in COPY_PDFS.items():
        d = os.path.join(ROOT, "src", dst)
        if not os.path.exists(d):
            shutil.copy(SRC_PDF + src, d)


def build():
    copy_pdfs()
    pdf_pb = pdf(PDF_PB_FILE, "Download the hydraulic & hybrid press brake brochure")
    pdf_servo = pdf(PDF_SERVO_FILE, "Download the servo-electric press brake brochure")
    pdf_laser = pdf(PDF_LASER_FILE, "Download the fiber laser brochure")
    pdf_tube = pdf(PDF_TUBE_FILE, "Download the tube laser brochure")
    pdf_panel = pdf(PDF_PANEL_FILE, "Download the panel bender brochure")
    fams = []
    for f in D.PB_FAMILIES:
        fams.append(dict(f, pdf=pdf_servo if f["group"] == "pb-servo" else pdf_pb))
    fams += [dict(f, pdf=pdf_laser) for f in D.LASER_FAMILIES]
    fams += [dict(f, pdf=pdf_tube) for f in D.TUBE_FAMILIES]
    fams += [dict(f, pdf=pdf_panel) for f in D.PANEL_FAMILIES]
    pdf_vl_panel = pdf(PDF_VL_PANEL_FILE, "Download the value-line panel bender brochure")
    fams += [dict(f, pdf=pdf_vl_panel) for f in VL.PANEL_FAMILIES]
    write_families(SET, fams)
    common = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **INTRO_VIDEO}
    write_category(D.P_PB, PAGE_PB, fams, SET, "Press brakes", extra={**common, "nav_label": "CNC press brakes", "catalogue_pdf": None, "catalogue_pdfs": [pdf_pb, pdf_servo]})
    write_category(D.P_LASER, PAGE_LASER, fams, SET, "Sheet laser cutters", extra={**common, "nav_label": "Sheet laser cutters", "catalogue_pdf": pdf_laser})
    write_category(D.P_TUBE, PAGE_TUBE, fams, SET, "Tube laser cutters", extra={**common, "nav_label": "Tube laser cutters", "catalogue_pdf": pdf_tube})
    write_category(D.P_PANEL, PAGE_PANEL, fams, SET, "Panel benders", extra={**common, "nav_label": "Panel benders", "catalogue_pdf": None, "catalogue_pdfs": [pdf_panel, pdf_vl_panel],
                                                                                "hero_brand_line": "The Dener panel bender is made in Turkey by Dener Makina; the PB-M and PB-A carry the NovoTech name — built in China to North American standards. All sold, installed and supported in Canada by NovoTech."})
    keys = register_images()
    vl_keys = {k for f in VL.PANEL_FAMILIES for k in f["images"]}
    used = {k for f in fams + D.SHEAR_FAMILIES for k in f["images"]} - vl_keys
    for p in (PAGE_PB, PAGE_LASER, PAGE_TUBE, PAGE_PANEL):
        used |= {p["hero"]} | set(p["minis"])
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    vids = sorted({v["id"] for f in fams + D.SHEAR_FAMILIES for v in f["videos"] if f["id"] not in {x["id"] for x in VL.PANEL_FAMILIES}} | {INTRO_VIDEO["intro_video"]["id"]})
    open(os.path.join(ROOT, "tools", "dener_vids.txt"), "w").write(" ".join(vids))
    print(f"dener: {len(fams)} families on 4 pages + {len(D.SHEAR_FAMILIES)} shear families · images: {len(keys)} · videos: {len(vids)}")


if __name__ == "__main__":
    build()
